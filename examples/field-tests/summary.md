# Field tests: before and after AI adoption

Six months before each project's first AI-instruction file against the months after it, up to 2026-09 (the last month fully matured by the 1 November 2026 analysis date). Verdicts come from the month-by-month replay, which uses only history available at the time. Projects without a marker use 2025-07 as a reference point. Descriptive only: projects differ, and an instructions file does not measure how much code AI wrote.

| Project | Marker | P before → after | AR_repo before → after | Rework before → after | Median lines before → after | Replay verdicts after (hold / address / scale) | Most frequent rules | AI-signed commits after |
|---|---|---|---|---|---|---|---|---|
| biome | 2025-07-31 | 474 → 654 (+38%) | 0.60 → 0.62 | 0.33 → 0.33 | 58 → 115 | 2 / 9 / 3 | R5×11 R0×3 R3×3 | 4% |
| deno | 2025-11-06 | 602 → 1251 (+108%) | 0.40 → 0.43 | 0.53 → 0.53 | 63 → 96 | 4 / 3 / 3 | R3×7 R5×7 R1×4 | 15% |
| excalidraw | 2025-05-25 | 88 → 99 (+13%) | 0.66 → 0.55 | 0.26 → 0.36 | 39 → 58 | 1 / 12 / 3 | R5×9 R3×6 R0×3 | 4% |
| fastapi | none | 153 → 213 (+39%) | 0.99 → 0.85 | 0.01 → 0.10 | 78 → 42 | 2 / 7 / 5 | R5×8 R0×5 R3×5 | – |
| langchain | 2025-07-21 | 652 → 540 (-17%) | 0.78 → 0.64 | 0.17 → 0.28 | 10 → 25 | 0 / 8 / 6 | R5×6 R0×6 R3×4 | 2% |
| poetry | none | 91 → 64 (-30%) | 0.88 → 0.91 | 0.10 → 0.07 | 24 → 31 | 2 / 6 / 6 | R0×6 R3×6 R5×3 | – |
| prefect | 2025-06-16 | 691 → 322 (-53%) | 0.78 → 0.84 | 0.18 → 0.12 | 78 → 68 | 0 / 6 / 9 | R0×9 R5×4 R4×3 | 53% |
| ruff | 2026-01-04 | 1311 → 1663 (+27%) | 0.43 → 0.54 | 0.49 → 0.38 | 74 → 83 | 0 / 6 / 2 | R5×4 R3×4 R0×2 | 3% |
| sentry-python | 2025-06-24 | 125 → 365 (+191%) | 0.86 → 0.64 | 0.10 → 0.31 | 25 → 51 | 4 / 10 / 1 | R5×12 R3×8 R1×4 | 5% |
| zed | 2025-04-17 | 2293 → 2956 (+29%) | 0.37 → 0.37 | 0.54 → 0.56 | 31 → 59 | 0 / 13 / 4 | R5×12 R0×4 R3×1 | 2% |
