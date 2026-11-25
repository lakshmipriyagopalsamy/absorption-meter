# Performance

`scripts/benchmark.py` times the analysis (monthly table, rework detection, paired metrics and decision
rules) on synthetic histories: about 40 changes a day over 400 files, 1–4 files per change, 15% fix-like
messages and 1% reverts. Reading history with `git log` is not included.

Measured on 24 Nov 2026 (absorption-meter 0.1.1, Python 3.9.6, Apple Silicon laptop):

| Changes | Months | Time (s) | Peak memory (MB) |
|---:|---:|---:|---:|
| 5,000 | 5 | 0.09 | 1 |
| 25,000 | 21 | 0.46 | 8 |
| 100,000 | 83 | 1.84 | 32 |
| 250,000 | 206 | 4.60 | 73 |

Time grows linearly with history length. The rework detector indexes earlier changes by file and
commit prefix, so each fix or revert looks back only at changes that share a file within the window.
For comparison, the Homebrew/brew example (4,176 changes) analyzes in well under a second.

Run it yourself: `python scripts/benchmark.py 5000 25000 100000`.
