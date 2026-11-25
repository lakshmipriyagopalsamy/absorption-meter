"""Time and memory of the analysis on synthetic histories of increasing size.

Usage: python scripts/benchmark.py [N ...]   (default: 5000 25000 100000)

Synthetic histories: ~40 changes a day over 400 files, 1-4 files per change, 15% fix-like messages,
1% reverts. Reading the history from git is not included; that is bounded by `git log` itself.
"""

from __future__ import annotations

import platform
import random
import sys
import time
import tracemalloc

from absorption_meter.gitlog import Change, FileChange
from absorption_meter.metrics import monthly
from absorption_meter.pairs import evaluate, recommend

DAY = 86400


def history(n: int, seed: int = 1):
    rng = random.Random(seed)
    out, t = [], 1_700_000_000
    for i in range(n):
        t += rng.randint(0, DAY // 20)
        body = f"This reverts commit {out[-rng.randint(1, min(50, len(out)))].sha}." if out and rng.random() < 0.01 else ""
        subject = "fix: defect" if rng.random() < 0.15 else "change"
        files = [FileChange(f"pkg{rng.randint(1, 20)}/m{rng.randint(1, 20)}.py", rng.randint(1, 80), rng.randint(0, 20))
                 for _ in range(rng.randint(1, 4))]
        out.append(Change(f"{rng.getrandbits(160):040x}", t, [], "", subject, body, files))
    return out


def main(sizes):
    print(f"Python {platform.python_version()} on {platform.machine()} ({platform.system()})")
    print("| Changes | Months | Time (s) | Peak memory (MB) |\n|---:|---:|---:|---:|")
    for n in sizes:
        changes = history(n)
        tracemalloc.start()
        start = time.perf_counter()
        a = monthly(changes)
        evaluate(a)
        recommend(a)
        elapsed = time.perf_counter() - start
        peak = tracemalloc.get_traced_memory()[1] / 1e6
        tracemalloc.stop()
        print(f"| {n:,} | {len(a.months)} | {elapsed:.2f} | {peak:.0f} |")


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]] or [5000, 25000, 100000])
