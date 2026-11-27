"""Precision of rework links from hand labels, with 95% Wilson intervals and inter-rater agreement.

Reads labelled CSVs exported from the labelling page (<project>_strict.labels.<labeller>.csv) or filled-in
sample CSVs (column "real_fix (yes/no)"). For each project and labeller: precision = yes / (yes + no);
"unsure" and blank rows are reported but not counted. When two labellers labelled the same links, also
reports raw agreement and Cohen's kappa on the links both answered yes or no.

Usage: python scripts/precision_results.py LABEL_FILES... [--out results.md]
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import re
from collections import defaultdict

NAME = re.compile(r"^(?P<project>.+?)_strict(?:\.labels\.(?P<who>[^.]+))?\.csv$")


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (None, None)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def read(path):
    out = {}
    for row in csv.DictReader(open(path, newline="")):
        v = (row.get("real_fix (yes/no)") or "").strip().lower()
        out[(row["earlier_commit"], row["fix_commit"])] = v
    return out


def kappa(a, b):
    keys = [k for k in a if k in b and a[k] in ("yes", "no") and b[k] in ("yes", "no")]
    if not keys:
        return None, None, 0
    agree = sum(a[k] == b[k] for k in keys) / len(keys)
    pa, pb = sum(a[k] == "yes" for k in keys) / len(keys), sum(b[k] == "yes" for k in keys) / len(keys)
    pe = pa * pb + (1 - pa) * (1 - pb)
    return agree, (agree - pe) / (1 - pe) if pe < 1 else 1.0, len(keys)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out")
    args = ap.parse_args()
    data = defaultdict(dict)                       # project -> labeller -> labels
    for f in args.files:
        m = NAME.match(os.path.basename(f))
        if not m:
            raise SystemExit(f"unexpected file name: {f}")
        data[m["project"]][m["who"] or "unnamed"] = read(f)

    lines = ["# Rework precision: hand-labelled links\n",
             "Precision = links labelled yes ÷ links labelled yes or no. Unsure and blank links are shown but not "
             "counted. 95% Wilson intervals.\n",
             "| Project | Labeller | Labelled | Yes | No | Unsure | Precision (95% CI) |", "|---|---|---|---|---|---|---|"]
    pooled = defaultdict(lambda: [0, 0])
    for project in sorted(data):
        for who, labels in sorted(data[project].items()):
            vals = list(labels.values())
            y, n, u = vals.count("yes"), vals.count("no"), vals.count("unsure")
            lo, hi = wilson(y, y + n)
            pooled[who][0] += y
            pooled[who][1] += y + n
            prec = f"{y / (y + n):.0%} ({lo:.0%}–{hi:.0%})" if y + n else "–"
            lines.append(f"| {project} | {who} | {y + n + u} of {len(vals)} | {y} | {n} | {u} | {prec} |")
    for who, (y, t) in sorted(pooled.items()):
        lo, hi = wilson(y, t)
        lines.append(f"| **all projects** | {who} | {t} | {y} | {t - y} | | **{y / t:.0%} ({lo:.0%}–{hi:.0%})** |" if t else
                     f"| **all projects** | {who} | 0 | | | | – |")
    pairs = [(p, sorted(d)) for p, d in sorted(data.items()) if len(d) >= 2]
    if pairs:
        lines += ["", "## Agreement between labellers", "", "| Project | Labellers | Links both answered | Agreement | Cohen's κ |",
                  "|---|---|---|---|---|"]
        for p, whos in pairs:
            a, b = data[p][whos[0]], data[p][whos[1]]
            agree, k, n = kappa(a, b)
            lines.append(f"| {p} | {whos[0]}, {whos[1]} | {n} | {agree:.0%} | {k:.2f} |" if n else f"| {p} | {whos[0]}, {whos[1]} | 0 | – | – |")
    text = "\n".join(lines) + "\n"
    if args.out:
        open(args.out, "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
