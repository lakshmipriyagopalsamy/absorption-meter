"""Optional pull-request data from the GitHub REST API.

Adds the decision-side measures that git history can't show: time to first
review, lead time from PR opened to merged, review comments per changed line,
the share of PRs merged without review, and, per merged change, whether
someone other than the author reviewed it (for examined absorption).

Uses a token from ``GITHUB_TOKEN`` when set (needed for private repositories and
higher rate limits). Each PR costs two API calls beyond the listing, so the
number of PRs read is capped.
"""

from __future__ import annotations

import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from statistics import median
from typing import Any, Callable, Dict, List, Optional

API = "https://api.github.com"
Fetch = Callable[[str], Any]

_BOT = re.compile(r"(\[bot\]$|dependabot|renovate)", re.IGNORECASE)


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


def http_fetch(token: Optional[str] = None) -> Fetch:
    token = token or os.environ.get("GITHUB_TOKEN")

    def fetch(url: str) -> Any:
        request = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "absorption-meter",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        })
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    return fetch


def fetch_merged_prs(
    owner_repo: str,
    since: Optional[str] = None,
    max_prs: int = 300,
    fetch: Optional[Fetch] = None,
) -> List[Dict[str, Any]]:
    """Return merged PRs (newest first) with the fields the metrics need."""
    fetch = fetch or http_fetch()
    since_dt = datetime.strptime(since, "%Y-%m-%d") if since else None
    prs: List[Dict[str, Any]] = []
    page = 1
    while len(prs) < max_prs:
        listing = fetch(
            f"{API}/repos/{owner_repo}/pulls?state=closed&sort=created&direction=desc&per_page=100&page={page}"
        )
        if not listing:
            break
        stop = False
        for item in listing:
            created = _parse_time(item.get("created_at"))
            if since_dt and created and created < since_dt:
                stop = True
                break
            if not item.get("merged_at"):
                continue
            author = (item.get("user") or {}).get("login", "")
            if _BOT.search(author):
                continue
            prs.append(_enrich(owner_repo, item, author, fetch))
            if len(prs) >= max_prs:
                break
        if stop:
            break
        page += 1
    return prs


def _enrich(owner_repo: str, item: Dict[str, Any], author: str, fetch: Fetch) -> Dict[str, Any]:
    number = item["number"]
    detail = fetch(f"{API}/repos/{owner_repo}/pulls/{number}")
    reviews = fetch(f"{API}/repos/{owner_repo}/pulls/{number}/reviews?per_page=100") or []
    others = [r for r in reviews if (r.get("user") or {}).get("login") != author and r.get("submitted_at")]
    first_review = min((_parse_time(r["submitted_at"]) for r in others), default=None)
    return {
        "number": number,
        "created_at": item.get("created_at"),
        "merged_at": item.get("merged_at"),
        "first_review_at": first_review.strftime("%Y-%m-%dT%H:%M:%SZ") if first_review else None,
        "review_rounds": len(others),
        "review_comments": int(detail.get("review_comments") or 0),
        "additions": int(detail.get("additions") or 0),
        "deletions": int(detail.get("deletions") or 0),
        "merge_commit_sha": detail.get("merge_commit_sha") or item.get("merge_commit_sha"),
    }


def pr_monthly(prs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Optional[float]]]:
    """Aggregate PRs by the month they were merged."""
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for pr in prs:
        merged = _parse_time(pr.get("merged_at"))
        if merged:
            groups.setdefault(merged.strftime("%Y-%m"), []).append(pr)

    result: Dict[str, Dict[str, Optional[float]]] = {}
    for month, items in groups.items():
        lead, first_review = [], []
        lines = comments = unreviewed = 0
        sizes = []
        for pr in items:
            created, merged = _parse_time(pr["created_at"]), _parse_time(pr["merged_at"])
            if created and merged:
                lead.append((merged - created).total_seconds() / 3600)
            reviewed = _parse_time(pr.get("first_review_at"))
            if created and reviewed:
                first_review.append((reviewed - created).total_seconds() / 3600)
            if not pr.get("review_rounds"):
                unreviewed += 1
            size = pr.get("additions", 0) + pr.get("deletions", 0)
            sizes.append(size)
            lines += size
            comments += pr.get("review_comments", 0)
        result[month] = {
            "prs": len(items),
            "median_lead_hours": round(median(lead), 2) if lead else None,
            "median_first_review_hours": round(median(first_review), 2) if first_review else None,
            "review_comments_per_100_lines": round(100 * comments / lines, 3) if lines else None,
            "unreviewed_share": round(unreviewed / len(items), 4),
            "median_pr_lines": float(median(sizes)) if sizes else None,
        }
    return result


def reviewed_map(prs: List[Dict[str, Any]]) -> Dict[str, bool]:
    """Map each PR's merge (or squash) commit sha to whether someone other than the author reviewed it."""
    return {pr["merge_commit_sha"]: bool(pr.get("review_rounds"))
            for pr in prs if pr.get("merge_commit_sha")}


def earliest_merge(prs: List[Dict[str, Any]]) -> Optional[int]:
    """Timestamp of the oldest merged PR read (PR data is complete only after this)."""
    times = [_parse_time(pr.get("merged_at")) for pr in prs]
    times = [t for t in times if t]
    return int(min(times).replace(tzinfo=timezone.utc).timestamp()) if times else None


def merge_into(analysis, monthly_prs: Dict[str, Dict[str, Optional[float]]]) -> None:
    """Copy PR measures into an Analysis's month rows."""
    for row in analysis.months:
        values = monthly_prs.get(row.month)
        if values:
            for key, value in values.items():
                setattr(row, key, value)
    analysis.pr_data = bool(monthly_prs)
