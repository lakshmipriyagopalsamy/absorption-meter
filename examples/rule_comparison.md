# Rework rule: legacy (v0.1/v0.2) against strict (v0.3)

Monthly means over 2024-07 to 2026-09. Replay verdicts count months from 2025-01, as hold / address / scale. The strict rule ignores maintenance titles and links fixes only through non-hub files; it was specified in [docs/METHOD-v0.3.md](../docs/METHOD-v0.3.md) before this comparison was run.

| Dataset | Changes | Hub files | Fix-like titles legacy → strict | AR_repo legacy → strict | Rework legacy → strict | Verdicts legacy → strict |
|---|---|---|---|---|---|---|
| homebrew (worked example) | 4,176 | 66 | 15% → 14% | 0.75 → 0.77 | 0.20 → 0.18 | 5/8/6 → 5/8/6 |
| biome | 3,684 | 370 | 45% → 38% | 0.44 → 0.64 | 0.49 → 0.30 | 2/14/3 → 4/11/4 |
| deno | 5,712 | 757 | 61% → 57% | 0.30 → 0.40 | 0.66 → 0.53 | 4/9/6 → 4/10/5 |
| excalidraw | 668 | 37 | 55% → 54% | 0.44 → 0.57 | 0.47 → 0.34 | 2/12/5 → 1/15/3 |
| fastapi | 1,563 | 71 | 11% → 9% | 0.87 → 0.89 | 0.11 → 0.08 | 2/10/7 → 2/10/7 |
| langchain | 5,978 | 269 | 39% → 30% | 0.56 → 0.69 | 0.38 → 0.24 | 0/8/11 → 0/9/10 |
| poetry | 568 | 109 | 34% → 27% | 0.87 → 0.90 | 0.11 → 0.09 | 2/7/10 → 3/6/10 |
| prefect | 3,091 | 104 | 22% → 20% | 0.77 → 0.79 | 0.18 → 0.16 | 0/10/9 → 0/10/9 |
| ruff | 8,954 | 186 | 15% → 14% | 0.50 → 0.53 | 0.43 → 0.40 | 0/17/2 → 0/17/2 |
| sentry-python | 1,901 | 67 | 25% → 22% | 0.67 → 0.72 | 0.30 → 0.24 | 3/14/2 → 4/13/2 |
| zed | 19,657 | 529 | 24% → 22% | 0.33 → 0.37 | 0.59 → 0.54 | 1/14/4 → 2/13/4 |
