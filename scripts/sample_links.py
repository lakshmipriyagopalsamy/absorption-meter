"""Draw a random sample of rework links for hand-labelling (precision check, docs/METHOD-v0.3.md).

Each row is one link: an earlier change and the later fix that marked it as reworked, with the shared
files and GitHub links to both commits. Open both, then mark `real_fix` yes if the fix repairs something
the earlier change introduced or broke, no if the link is coincidental. Precision = yes / labelled rows.

Usage: python scripts/sample_links.py DATASET OUT.csv [--rule strict|legacy] [--n 30] [--seed 1]
"""

from __future__ import annotations

import argparse
import csv
import random

from absorption_meter.dataset import load
from absorption_meter.metrics import DAY, hub_paths, is_fix


def links(changes, rule="strict", window_days=14):
    ordered = sorted(changes, key=lambda c: c.timestamp)
    hubs = hub_paths(ordered) if rule == "strict" else set()
    out = []
    for j, fix in enumerate(ordered):
        if not is_fix(fix, rule):
            continue
        fix_paths = set(fix.paths) - hubs
        for i in range(j - 1, -1, -1):
            earlier = ordered[i]
            if fix.timestamp - earlier.timestamp > window_days * DAY:
                break
            shared = fix_paths & (set(earlier.paths) - hubs)
            if shared:
                out.append((earlier, fix, sorted(shared)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("out")
    ap.add_argument("--rule", default="strict", choices=("strict", "legacy"))
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    meta, changes, _, _ = load(args.dataset)
    repo = meta.get("source", "").rstrip("/")
    pool = links(changes, args.rule)
    sample = random.Random(args.seed).sample(pool, min(args.n, len(pool)))
    with open(args.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["earlier_commit", "fix_commit", "days_apart", "shared_files", "real_fix (yes/no)", "note"])
        for earlier, fix, shared in sample:
            w.writerow([f"{repo}/commit/{earlier.sha}", f"{repo}/commit/{fix.sha}",
                        round((fix.timestamp - earlier.timestamp) / DAY, 1), "; ".join(shared[:5]), "", ""])
    print(f"{args.out}: {len(sample)} of {len(pool)} {args.rule} links")


if __name__ == "__main__":
    main()
