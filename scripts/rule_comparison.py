"""Compare the legacy (v0.1/v0.2) and strict (v0.3) rework rules on every committed real-world dataset:
the Homebrew worked example and the field tests. Writes examples/rule_comparison.{md,csv}.
See docs/METHOD-v0.3.md for the rules, which were specified before this comparison was run.
"""

from __future__ import annotations

import csv
import glob
import os
from collections import Counter
from datetime import datetime, timezone
from statistics import mean

from absorption_meter.dataset import load
from absorption_meter.metrics import hub_paths, is_fix, monthly
from absorption_meter.pairs import Settings, recommend

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRST, LAST = "2024-07", "2026-09"


def month_end(month: str) -> int:
    y, m = map(int, month.split("-"))
    y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return int(datetime(y, m, 1, tzinfo=timezone.utc).timestamp())


def summarize(changes, tags, drift, rule):
    full = monthly(changes, tags, drift, rework_rule=rule)
    rows = [r for r in full.months if FIRST <= r.month <= LAST and r.absorption_ratio is not None]
    verdicts = Counter()
    for r in full.months:
        if not ("2025-01" <= r.month <= LAST):
            continue
        cut = month_end(r.month)
        a = monthly([c for c in changes if c.timestamp < cut], [t for t in tags if t[0] < cut],
                    [d for d in drift if d.timestamp < cut], as_of=cut, rework_rule=rule)
        verdicts[recommend(a, Settings()).verdict] += 1
    return {
        "ar": round(mean(r.absorption_ratio for r in rows), 3),
        "rework": round(mean(r.rework_rate for r in rows), 3),
        "hold": verdicts["hold"], "address": verdicts["address"], "scale": verdicts["scale"],
    }


def main() -> None:
    datasets = [("homebrew (worked example)", os.path.join(ROOT, "examples", "homebrew", "changes.jsonl"))]
    datasets += [(os.path.basename(os.path.dirname(p)), p)
                 for p in sorted(glob.glob(os.path.join(ROOT, "examples", "field-tests", "*", "changes.jsonl.gz")))]
    out = []
    for name, path in datasets:
        _, changes, tags, drift = load(path)
        legacy, strict = summarize(changes, tags, drift, "legacy"), summarize(changes, tags, drift, "strict")
        fixes_l = sum(is_fix(c, "legacy") for c in changes)
        fixes_s = sum(is_fix(c, "strict") for c in changes)
        out.append({
            "dataset": name, "changes": len(changes), "hub_files": len(hub_paths(changes)),
            "fix_like_legacy": round(fixes_l / len(changes), 3), "fix_like_strict": round(fixes_s / len(changes), 3),
            "ar_legacy": legacy["ar"], "ar_strict": strict["ar"],
            "rework_legacy": legacy["rework"], "rework_strict": strict["rework"],
            "verdicts_legacy": f"{legacy['hold']}/{legacy['address']}/{legacy['scale']}",
            "verdicts_strict": f"{strict['hold']}/{strict['address']}/{strict['scale']}",
        })
    with open(os.path.join(ROOT, "examples", "rule_comparison.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    with open(os.path.join(ROOT, "examples", "rule_comparison.md"), "w") as fh:
        fh.write("# Rework rule: legacy (v0.1/v0.2) against strict (v0.3)\n\n")
        fh.write(f"Monthly means over {FIRST} to {LAST}. Replay verdicts count months from 2025-01, as hold / "
                 "address / scale. The strict rule ignores maintenance titles and links fixes only through non-hub "
                 "files; it was specified in [docs/METHOD-v0.3.md](../docs/METHOD-v0.3.md) before this comparison "
                 "was run.\n\n")
        fh.write("| Dataset | Changes | Hub files | Fix-like titles legacy → strict | AR_repo legacy → strict | "
                 "Rework legacy → strict | Verdicts legacy → strict |\n|---|---|---|---|---|---|---|\n")
        for r in out:
            fh.write(f"| {r['dataset']} | {r['changes']:,} | {r['hub_files']} | {r['fix_like_legacy']:.0%} → "
                     f"{r['fix_like_strict']:.0%} | {r['ar_legacy']:.2f} → {r['ar_strict']:.2f} | "
                     f"{r['rework_legacy']:.2f} → {r['rework_strict']:.2f} | {r['verdicts_legacy']} → "
                     f"{r['verdicts_strict']} |\n")
    print(f"compared {len(out)} datasets")


if __name__ == "__main__":
    main()
