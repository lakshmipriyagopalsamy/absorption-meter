"""Replay the decision rules month by month, as a team would have seen them.

For each month, the analysis uses only the history up to the end of that month
(so rework windows still open at that point are censored, as they would have
been). Writes a Markdown timeline and a CSV of the monthly measures.

Usage: python scripts/rule_timeline.py DATASET.jsonl OUT_DIR [--from YYYY-MM] [--robust]
"""

from __future__ import annotations

import argparse
import csv
import os
from datetime import datetime, timezone

from absorption_meter.dataset import load
from absorption_meter.metrics import monthly
from absorption_meter.pairs import DEBT, Settings, evaluate, recommend


def month_end(month: str) -> int:
    y, m = map(int, month.split("-"))
    y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return int(datetime(y, m, 1, tzinfo=timezone.utc).timestamp())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("out_dir")
    ap.add_argument("--from", dest="start", help="first month to evaluate (YYYY-MM)")
    ap.add_argument("--robust", action="store_true")
    args = ap.parse_args()

    meta, changes, tags, drift = load(args.dataset)
    settings = Settings(robust=args.robust)
    full = monthly(changes, tags, drift)
    os.makedirs(args.out_dir, exist_ok=True)

    with open(os.path.join(args.out_dir, "monthly.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["month", "changes", "production", "absorption_ratio", "rework_rate", "median_lines",
                    "mean_dirs", "releases", "patch_release_rate", "contract_drift"])
        for r in full.months:
            w.writerow([r.month, r.changes, r.production, r.absorption_ratio, r.rework_rate, r.median_lines,
                        r.mean_dirs, r.releases, r.patch_release_rate, r.contract_drift])

    rows = []
    for r in full.months:
        if args.start and r.month < args.start:
            continue
        cut = month_end(r.month)
        upto = [c for c in changes if c.timestamp < cut]
        a = monthly(upto, [t for t in tags if t[0] < cut], [d for d in drift if d.timestamp < cut], as_of=cut)
        rec = recommend(a, settings)
        pairs = [p.pair.split(" ↔")[0] for p in evaluate(a, settings) if p.status == DEBT]
        last = a.months[-1]
        rows.append((r.month, last.changes, last.production, last.absorption_ratio, rec.verdict,
                     " ".join(rec.rules) or "–", "; ".join(pairs) or "–"))

    with open(os.path.join(args.out_dir, "timeline.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["as_of", "verdict", "rules", "pairs_signalling_debt"])
        for m, n, p, ar, verdict, rules, pairs in rows:
            w.writerow([m, verdict, rules, pairs])

    with open(os.path.join(args.out_dir, "rule_timeline.md"), "w") as fh:
        fh.write(f"# Decision rules replayed month by month: {meta.get('source', '')}\n\n")
        fh.write(f"Dataset commit `{meta.get('commit', '')[:12]}`. Each row uses only history up to the end of "
                 f"that month, and P and AR include only changes whose 14-day rework window had fully elapsed "
                 f"by then; later changes enter once their window matures. Baseline: "
                 f"{'median/MAD' if args.robust else 'mean/SD'}, last 3 months vs the 6 before.\n\n")
        fh.write("| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |\n|---|---|---|---|---|---|---|\n")
        for m, n, p, ar, verdict, rules, pairs in rows:
            fh.write(f"| {m} | {n} | {p if p is not None else '–'} | {ar if ar is not None else '–'} | "
                     f"{verdict} | {rules} | {pairs} |\n")
    print(f"wrote {args.out_dir}/monthly.csv and rule_timeline.md ({len(rows)} months)")


if __name__ == "__main__":
    main()
