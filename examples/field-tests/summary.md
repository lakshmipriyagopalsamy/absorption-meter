# Field tests: before and after AI adoption

Six months before each project's first AI-instruction file against the months after it, up to 2026-09 (the last month fully matured by the 1 November 2026 analysis date). Verdicts come from the month-by-month replay, which uses only history available at the time. Projects without a marker use 2025-07 as a reference point. Descriptive only: projects differ, and an instructions file does not measure how much code AI wrote.

| Project | Marker | P before → after | AR_repo before → after | Rework before → after | Median lines before → after | Replay verdicts after (hold / address / scale) | Most frequent rules | AI-signed commits after |
|---|---|---|---|---|---|---|---|---|
| biome | 2025-07-31 | 474 → 654 (+38%) | 0.43 → 0.47 | 0.50 → 0.46 | 58 → 115 | 1 / 11 / 2 | R5×11 R3×3 R0×2 | 4% |
| deno | 2025-11-06 | 602 → 1251 (+108%) | 0.29 → 0.33 | 0.65 → 0.64 | 63 → 96 | 4 / 3 / 3 | R5×7 R3×6 R1×4 | 15% |
| excalidraw | 2025-05-25 | 88 → 99 (+13%) | 0.53 → 0.43 | 0.40 → 0.50 | 39 → 58 | 2 / 10 / 4 | R5×9 R3×7 R0×4 | 4% |
| fastapi | none | 153 → 213 (+39%) | 0.98 → 0.83 | 0.02 → 0.13 | 78 → 42 | 2 / 7 / 5 | R5×8 R0×5 R3×5 | – |
| langchain | 2025-07-21 | 652 → 540 (-17%) | 0.63 → 0.53 | 0.32 → 0.40 | 10 → 25 | 0 / 8 / 6 | R5×6 R0×6 R3×4 | 2% |
| poetry | none | 91 → 64 (-30%) | 0.87 → 0.88 | 0.12 → 0.10 | 24 → 31 | 2 / 6 / 6 | R3×7 R0×6 R5×3 | – |
| prefect | 2025-06-16 | 691 → 322 (-53%) | 0.75 → 0.83 | 0.21 → 0.14 | 78 → 68 | 0 / 6 / 9 | R0×9 R5×4 R4×3 | 53% |
| ruff | 2026-01-04 | 1311 → 1663 (+27%) | 0.41 → 0.51 | 0.52 → 0.42 | 74 → 83 | 0 / 6 / 2 | R5×4 R3×4 R0×2 | 3% |
| sentry-python | 2025-06-24 | 125 → 365 (+191%) | 0.79 → 0.59 | 0.19 → 0.37 | 25 → 51 | 3 / 10 / 2 | R5×12 R3×6 R4×3 | 5% |
| zed | 2025-04-17 | 2293 → 2956 (+29%) | 0.34 → 0.33 | 0.57 → 0.59 | 31 → 59 | 0 / 13 / 4 | R5×12 R0×4 R3×1 | 2% |
