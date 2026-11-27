"""Generate the 'absorbed or unexamined?' demo (deterministic).

A small fictional team adopts AI-assisted development in January 2025. Output nearly doubles and
short-term rework stays low, so AR_repo looks healthy. But review bandwidth doesn't keep up: more pull
requests merge with no review, and defects start reaching the field weeks later, outside the git window.
v0.2.0 should flag this with cautions and rules R3 and R6, while AR_repo alone would say "scale".

Usage: python examples/unexamined/make_unexamined.py   (writes changes.jsonl, prs.json, team.csv here)
"""

from __future__ import annotations

import json
import os
import random
from datetime import datetime, timedelta, timezone

from absorption_meter.dataset import save
from absorption_meter.gitlog import Change, FileChange

HERE = os.path.dirname(os.path.abspath(__file__))
AREAS = ["app", "sync", "firmware", "ui"]


def month_start(i: int) -> datetime:
    y, m = divmod(i, 12)
    return datetime(2024 + y, m + 1, 1, tzinfo=timezone.utc)


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    rng = random.Random(20260127)
    changes, prs = [], []
    seq = number = 0
    for i in range(15):                         # Jan 2024 .. Mar 2025
        after = i >= 12                         # AI adoption in January 2025
        n = rng.randint(28, 32) if not after else rng.randint(52, 58)
        reviewed_p = 0.95 if not after else max(0.35, 0.95 - 0.2 * (i - 11))
        start = month_start(i)
        for _ in range(n):
            seq += 1
            number += 1
            merged = start + timedelta(days=rng.uniform(0, 20))
            area = rng.choice(AREAS)
            lines = int(rng.lognormvariate(3.2, 0.5))
            files = [FileChange(f"{area}/mod{rng.randint(1, 30)}.py", lines, rng.randint(0, 4)),
                     FileChange(f"tests/test_{area}.py", max(2, lines // 4), 0)]
            sha = f"{seq:040x}"
            changes.append(Change(sha, int(merged.timestamp()), [f"{seq - 1:040x}"], "", "change", "", files))
            reviewed = rng.random() < reviewed_p
            created = merged - timedelta(hours=rng.uniform(4, 30))
            prs.append({
                "number": number, "created_at": iso(created), "merged_at": iso(merged),
                "first_review_at": iso(created + timedelta(hours=rng.uniform(1, 6))) if reviewed else None,
                "review_rounds": rng.randint(1, 3) if reviewed else 0,
                "review_comments": rng.randint(1, 6) if reviewed else 0,
                "additions": lines, "deletions": files[0].deleted, "merge_commit_sha": sha,
            })
            if rng.random() < 0.08:              # short-term rework stays low before and after adoption
                seq += 1
                fix_at = merged + timedelta(days=rng.uniform(1, 6))
                changes.append(Change(f"{seq:040x}", int(fix_at.timestamp()), [sha], "", "fix", "",
                                      [FileChange(files[0].path, 3, 2)]))
    changes.sort(key=lambda c: c.timestamp)
    as_of = int((month_start(15) + timedelta(days=20)).timestamp())
    save(os.path.join(HERE, "changes.jsonl"), changes, [], [], source="small team (synthetic): absorbed or unexamined?",
         commit="synthetic", as_of=as_of)
    with open(os.path.join(HERE, "prs.json"), "w") as fh:
        json.dump(sorted(prs, key=lambda p: p["merged_at"]), fh, indent=0)
        fh.write("\n")
    with open(os.path.join(HERE, "team.csv"), "w") as fh:
        fh.write("month,escaped_defects,days_to_first_defect\n")
        for i in range(15):
            escaped = 1 if i < 12 else 2 + 2 * (i - 11)          # field defects rise after adoption
            days = 30 if i < 12 else max(8, 30 - 7 * (i - 11))   # and arrive sooner
            fh.write(f"{month_start(i):%Y-%m},{escaped},{days}\n")
    print(f"wrote {len(changes)} changes and {len(prs)} pull requests")


if __name__ == "__main__":
    main()
