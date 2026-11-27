"""Summarize the field tests: before vs after each project's AI adoption marker, and what the replayed
rules said. Reads examples/field-tests/*/{markers.json,monthly.csv,timeline.csv}; writes summary.csv and
summary.md there. Projects without a marker use July 2025 as a reference point, for comparison only.
"""

from __future__ import annotations

import csv
import json
import os
from collections import Counter
from statistics import mean, median

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FT = os.path.join(ROOT, "examples", "field-tests")
REFERENCE = "2025-07"
LAST = "2026-09"          # last month whose changes have all matured by the 1 Nov 2026 analysis date


def shift(month: str, k: int) -> str:
    y, m = map(int, month.split("-"))
    m += k
    y, m = y + (m - 1) // 12, (m - 1) % 12 + 1
    return f"{y:04d}-{m:02d}"


def avg(rows, key):
    vals = [float(r[key]) for r in rows if r.get(key) not in ("", None)]
    return round(mean(vals), 3) if vals else None


def med(rows, key):
    vals = [float(r[key]) for r in rows if r.get(key) not in ("", None)]
    return round(median(vals), 1) if vals else None


def main() -> None:
    out = []
    for name in sorted(os.listdir(FT)):
        d = os.path.join(FT, name)
        if not os.path.isfile(os.path.join(d, "markers.json")):
            continue
        mk = json.load(open(os.path.join(d, "markers.json")))
        monthly = list(csv.DictReader(open(os.path.join(d, "monthly.csv"))))
        timeline = list(csv.DictReader(open(os.path.join(d, "timeline.csv"))))
        marker = mk["adoption_marker"]
        m0 = marker[:7] if marker else REFERENCE
        before = [r for r in monthly if shift(m0, -6) <= r["month"] < m0]
        after = [r for r in monthly if shift(m0, 1) <= r["month"] <= LAST]
        verdicts = Counter(r["verdict"] for r in timeline if shift(m0, 1) <= r["as_of"] <= LAST)
        rules = Counter(x for r in timeline if shift(m0, 1) <= r["as_of"] <= LAST for x in r["rules"].split() if x != "–")
        n_after = sum(verdicts.values())
        p_b, p_a = avg(before, "production"), avg(after, "production")
        out.append({
            "project": name,
            "group": "AI marker" if marker else "no marker (reference Jul 2025)",
            "marker": marker or "",
            "months_after": n_after,
            "P_before": round(p_b) if p_b else None, "P_after": round(p_a) if p_a else None,
            "P_change": f"{(p_a / p_b - 1):+.0%}" if p_b and p_a else "",
            "AR_before": avg(before, "absorption_ratio"), "AR_after": avg(after, "absorption_ratio"),
            "rework_before": avg(before, "rework_rate"), "rework_after": avg(after, "rework_rate"),
            "median_lines_before": round(med(before, "median_lines")) if med(before, "median_lines") else None,
            "median_lines_after": round(med(after, "median_lines")) if med(after, "median_lines") else None,
            "hold_months_after": verdicts.get("hold", 0),
            "address_months_after": verdicts.get("address", 0),
            "scale_months_after": verdicts.get("scale", 0),
            "top_rules_after": " ".join(f"{k}×{v}" for k, v in rules.most_common(3)),
            "ai_signed_share_after": mk.get("ai_signed_share_after"),
        })

    with open(os.path.join(FT, "summary.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    def f(v, pct=False):
        if v in (None, ""):
            return "–"
        return f"{v:.0%}" if pct else (f"{v:.2f}" if isinstance(v, float) and v < 10 else str(v))

    with open(os.path.join(FT, "summary.md"), "w") as fh:
        fh.write("# Field tests: before and after AI adoption\n\n")
        fh.write("Six months before each project's first AI-instruction file against the months after it, up to "
                 f"{LAST} (the last month fully matured by the 1 November 2026 analysis date). Verdicts come from "
                 "the month-by-month replay, which uses only history available at the time. Projects without a "
                 f"marker use {REFERENCE} as a reference point. Descriptive only: projects differ, and an "
                 "instructions file does not measure how much code AI wrote.\n\n")
        fh.write("| Project | Marker | P before → after | AR_repo before → after | Rework before → after | "
                 "Median lines before → after | Replay verdicts after (hold / address / scale) | Most frequent rules | "
                 "AI-signed commits after |\n|---|---|---|---|---|---|---|---|---|\n")
        for r in out:
            fh.write(f"| {r['project']} | {r['marker'] or 'none'} | {f(r['P_before'])} → {f(r['P_after'])} "
                     f"({r['P_change']}) | {f(r['AR_before'])} → {f(r['AR_after'])} | {f(r['rework_before'])} → "
                     f"{f(r['rework_after'])} | {f(r['median_lines_before'])} → {f(r['median_lines_after'])} | "
                     f"{r['hold_months_after']} / {r['address_months_after']} / {r['scale_months_after']} | "
                     f"{r['top_rules_after'] or '–'} | {f(r['ai_signed_share_after'], pct=True)} |\n")
    print(f"wrote summary for {len(out)} projects")


if __name__ == "__main__":
    main()
