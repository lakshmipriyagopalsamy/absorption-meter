"""Generate the synthetic demo dataset (deterministic).

A fictional team: twelve steady months, then AI-assisted development from
January 2025. Production roughly doubles; changes grow and touch more of the
system; fewer arrive with tests and more are reworked; two API changes break compatibility without
a version bump; telemetry coverage slips. Every pair and most rules fire.

Usage: python examples/demo/make_demo.py   (writes changes.jsonl and team.csv here)
"""

from __future__ import annotations

import os
import random
from datetime import datetime, timedelta, timezone

from absorption_meter.contracts import Breaking, DriftEvent
from absorption_meter.dataset import save
from absorption_meter.gitlog import Change, FileChange

HERE = os.path.dirname(os.path.abspath(__file__))
AREAS = ["api", "billing", "orders", "web", "shared", "infra"]


def month_start(i: int) -> datetime:
    y, m = divmod(i, 12)
    return datetime(2024 + y, m + 1, 1, tzinfo=timezone.utc)


def main() -> None:
    rng = random.Random(20260101)
    changes = []
    drift = []
    seq = 0
    for i in range(15):                      # Jan 2024 .. Mar 2025
        after = i >= 12                      # AI adoption in January 2025
        n = rng.randint(38, 44) if not after else rng.randint(78, 92)
        rework_p = 0.10 if not after else 0.10 + 0.07 * (i - 11)
        start = month_start(i)
        for _ in range(n):
            seq += 1
            when = start + timedelta(days=rng.uniform(0, 20))
            areas = rng.sample(AREAS, rng.choice([1, 1, 1, 2]) if not after else rng.choice([1, 2, 2, 3]))
            lines = int(rng.lognormvariate(3.0 if not after else 3.6, 0.6))
            files = [FileChange(f"{a}/file{rng.randint(1, 40)}.py", lines // len(areas) + 1, rng.randint(0, 5))
                     for a in areas]
            with_tests = 0.80 if not after else 0.80 - 0.15 * (i - 11)   # verification weakens after adoption
            if rng.random() < with_tests:
                files.append(FileChange(f"tests/test_{areas[0]}.py", max(3, lines // 3), 0))
            sha = f"{seq:040x}"
            changes.append(Change(sha, int(when.timestamp()), [f"{seq - 1:040x}"], "", "change", "", files))
            if rng.random() < rework_p:
                seq += 1
                fix_at = when + timedelta(days=rng.uniform(1, 7.5))
                changes.append(Change(f"{seq:040x}", int(fix_at.timestamp()), [sha], "", "fix", "",
                                      [FileChange(files[0].path, 3, 2)]))
    for i, month in ((13, "orders"), (14, "billing")):
        t = int((month_start(i) + timedelta(days=12)).timestamp())
        drift.append(DriftEvent(f"{900000 + i:040x}", t, f"{month}/openapi.yaml", "1.4.0", "1.4.0",
                                [Breaking("removed-property", f"GET /{month}/{{id}} 200.status")]))
    changes.sort(key=lambda c: c.timestamp)
    tags = [(int((month_start(i) + timedelta(days=d)).timestamp()), f"v1.{i * 10 + p}.0")
            for i in range(15) for p, d in enumerate([5, 19] if i < 12 else [3, 9, 15, 21])]
    save(os.path.join(HERE, "changes.jsonl"), changes, tags, drift, source="demo team (synthetic)", commit="synthetic")

    with open(os.path.join(HERE, "team.csv"), "w") as fh:
        fh.write("month,telemetry_coverage,time_to_detect_hours\n")
        for i in range(15):
            cov = 0.90 if i < 12 else round(0.90 - 0.07 * (i - 11), 2)
            ttd = 1.5 if i < 12 else round(1.5 + 0.8 * (i - 11), 1)
            fh.write(f"{month_start(i):%Y-%m},{cov},{ttd}\n")
    print(f"wrote {len(changes)} changes, {len(drift)} drift events")


if __name__ == "__main__":
    main()
