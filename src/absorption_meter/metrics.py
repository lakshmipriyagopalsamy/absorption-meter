"""Monthly delivery and absorption metrics computed from repository history.

Every measure here is a *proxy*: an observable stand-in for a concept that a
repository doesn't record directly. Each function says what it approximates and
what it misses.
"""

from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean, median
from typing import Dict, List, Optional, Sequence, Tuple

from .contracts import DriftEvent
from .gitlog import Change, month_of

DAY = 86400

# A follow-up change whose subject matches this is treated as a fix.
FIX_PATTERN = re.compile(
    r"\b(fix(e[sd])?|bug(fix)?|hotfix|regression|revert(ed|s)?|broke(n)?|rollback|roll back|patch(ed)?)\b",
    re.IGNORECASE,
)
_SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


@dataclass
class MonthStats:
    month: str
    changes: int = 0
    median_lines: Optional[float] = None
    median_files: Optional[float] = None
    mean_dirs: Optional[float] = None
    rework_rate: Optional[float] = None
    revert_rate: Optional[float] = None
    # Absorption: P = size-weighted changes whose rework window has closed,
    # A = the part of P that was not reworked. AR = A / P.
    production: Optional[float] = None
    absorbed: Optional[float] = None
    absorption_ratio: Optional[float] = None
    releases: int = 0
    patch_release_rate: Optional[float] = None
    recovery_hours: Optional[float] = None
    contract_drift: int = 0
    contract_drift_per_100: Optional[float] = None
    # Team-reported (from --team-metrics); git can't see these.
    time_to_detect_hours: Optional[float] = None
    telemetry_coverage: Optional[float] = None
    # Filled from pull-request data when available.
    prs: Optional[int] = None
    median_lead_hours: Optional[float] = None
    median_first_review_hours: Optional[float] = None
    review_comments_per_100_lines: Optional[float] = None
    unreviewed_share: Optional[float] = None
    median_pr_lines: Optional[float] = None


@dataclass
class Analysis:
    months: List[MonthStats]
    total_changes: int
    first: Optional[str]
    last: Optional[str]
    rework_window_days: int
    releases_used: bool
    drift_events: List[DriftEvent] = field(default_factory=list)
    pr_data: bool = False
    team_data: bool = False


def size_weight(change: Change) -> float:
    """Weight of a change in P and A: log(1 + lines), so that one very large
    change can't dominate a month."""
    return math.log1p(max(change.lines, 0)) or 1.0


def _shares_path(a: Change, b: Change) -> bool:
    return bool(set(a.paths) & set(b.paths))


def rework_flags(changes: Sequence[Change], window_days: int = 14) -> Dict[str, bool]:
    """Flag each change that was reworked within ``window_days``.

    A change counts as reworked if a later change reverts it, or if a later change
    that looks like a fix touches at least one of the same files. This is an
    SZZ-style approximation: it misses fixes with uninformative messages and can
    count unrelated fixes to a busy file.
    """
    ordered = sorted(changes, key=lambda c: c.timestamp)
    flags: Dict[str, bool] = {}
    window = window_days * DAY
    for i, change in enumerate(ordered):
        reworked = False
        for later in ordered[i + 1:]:
            if later.timestamp - change.timestamp > window:
                break
            reverted = later.reverted_sha
            if reverted and (change.sha.startswith(reverted) or reverted.startswith(change.sha[:7])):
                reworked = True
                break
            if FIX_PATTERN.search(later.subject) and _shares_path(change, later):
                reworked = True
                break
        flags[change.sha] = reworked
    return flags


def release_failures(tags: Sequence[Tuple[int, str]], window_days: int = 7) -> List[Tuple[int, bool, Optional[float]]]:
    """For each semantic-version release, whether a patch release followed quickly.

    A patch release of the same major.minor within ``window_days`` is the proxy for
    a failed release, and the hours until that patch is the proxy for recovery
    time. Not every patch release fixes a failure, and not every failure gets a
    patch release, so read the trend, not the level.
    """
    parsed = []
    for ts, name in tags:
        m = _SEMVER.match(name)
        if m:
            parsed.append((ts, tuple(int(x) for x in m.groups())))
    parsed.sort()
    result = []
    for i, (ts, (major, minor, patch)) in enumerate(parsed):
        patches = [
            ts2 for ts2, (ma, mi, pa) in parsed[i + 1:]
            if 0 < ts2 - ts <= window_days * DAY and (ma, mi) == (major, minor) and pa > patch
        ]
        hours = round((min(patches) - ts) / 3600, 2) if patches else None
        result.append((ts, bool(patches), hours))
    return result


def _month_range(first: str, last: str) -> List[str]:
    y, m = map(int, first.split("-"))
    ly, lm = map(int, last.split("-"))
    months = []
    while (y, m) <= (ly, lm):
        months.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return months


def monthly(
    changes: Sequence[Change],
    tags: Sequence[Tuple[int, str]] = (),
    drift_events: Sequence[DriftEvent] = (),
    rework_window_days: int = 14,
    min_releases: int = 6,
) -> Analysis:
    """Aggregate changes into a contiguous month-by-month table."""
    if not changes:
        return Analysis([], 0, None, None, rework_window_days, False, list(drift_events))

    flags = rework_flags(changes, rework_window_days)
    last_ts = max(c.timestamp for c in changes)
    # Changes too recent for their rework window to have closed are right-censored.
    censor_after = last_ts - rework_window_days * DAY
    reverted = {c.reverted_sha for c in changes if c.reverted_sha}

    first_m, last_m = changes[0].month, changes[-1].month
    by_month: Dict[str, List[Change]] = {m: [] for m in _month_range(first_m, last_m)}
    for c in changes:
        by_month[c.month].append(c)

    releases = [r for r in release_failures(tags) if first_m <= month_of(r[0]) <= last_m]
    releases_used = len(releases) >= min_releases

    rows = []
    for month, items in by_month.items():
        row = MonthStats(month=month, changes=len(items))
        if items:
            row.median_lines = float(median(c.lines for c in items))
            row.median_files = float(median(len(c.files) for c in items))
            row.mean_dirs = round(mean(len(c.top_dirs) for c in items), 3)
            observable = [c for c in items if c.timestamp <= censor_after]
            if observable:
                row.rework_rate = round(sum(flags[c.sha] for c in observable) / len(observable), 4)
                row.revert_rate = round(
                    sum(any(c.sha.startswith(r) for r in reverted) for c in observable) / len(observable), 4
                )
                row.production = round(sum(size_weight(c) for c in observable), 3)
                row.absorbed = round(sum(size_weight(c) for c in observable if not flags[c.sha]), 3)
                row.absorption_ratio = round(row.absorbed / row.production, 4) if row.production else None
        month_releases = [(failed, hours) for ts, failed, hours in releases if month_of(ts) == month]
        row.releases = len(month_releases)
        if month_releases:
            row.patch_release_rate = round(sum(f for f, _ in month_releases) / len(month_releases), 4)
            hours = [h for _, h in month_releases if h is not None]
            if hours:
                row.recovery_hours = float(median(hours))
        row.contract_drift = sum(1 for e in drift_events if e.is_drift and month_of(e.timestamp) == month)
        if items:
            row.contract_drift_per_100 = round(100 * row.contract_drift / len(items), 3)
        rows.append(row)

    return Analysis(
        months=rows,
        total_changes=len(changes),
        first=first_m,
        last=last_m,
        rework_window_days=rework_window_days,
        releases_used=releases_used,
        drift_events=list(drift_events),
    )


def drop_incomplete_last_month(analysis: Analysis, now: Optional[datetime] = None) -> Analysis:
    """Remove the final month if it is the current, unfinished calendar month."""
    now = now or datetime.now(tz=timezone.utc)
    if analysis.months and analysis.months[-1].month == now.strftime("%Y-%m"):
        analysis.months = analysis.months[:-1]
        analysis.last = analysis.months[-1].month if analysis.months else None
    return analysis


TEAM_COLUMNS = {
    "recovery_hours": float,
    "time_to_detect_hours": float,
    "telemetry_coverage": float,
    "change_failure_rate": float,
    "deployments": int,
}


def load_team_metrics(analysis: Analysis, path: str) -> None:
    """Merge team-reported monthly measures from a CSV file.

    Columns: ``month`` (YYYY-MM) plus any of ``recovery_hours``,
    ``time_to_detect_hours``, ``telemetry_coverage`` (0-1, share of changes that
    ship with instrumentation), ``change_failure_rate`` (0-1) and ``deployments``.
    Team values replace the repository proxies for the same month.
    """
    rows = {r.month: r for r in analysis.months}
    with open(path, newline="", encoding="utf-8") as fh:
        for record in csv.DictReader(fh):
            row = rows.get((record.get("month") or "").strip())
            if row is None:
                continue
            for column, cast in TEAM_COLUMNS.items():
                value = (record.get(column) or "").strip()
                if not value:
                    continue
                if column == "change_failure_rate":
                    row.patch_release_rate = float(value)
                elif column == "deployments":
                    row.releases = int(value)
                else:
                    setattr(row, column, cast(value))
    analysis.team_data = True
    if any(r.releases for r in analysis.months):
        analysis.releases_used = True
