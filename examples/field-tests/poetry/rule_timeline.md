# Decision rules replayed month by month: https://github.com/python-poetry/poetry

Dataset commit `3cc663a73852`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 101 | 175.977 | 0.6622 | insufficient-data | – | – |
| 2025-02 | 25 | 71.402 | 0.6228 | insufficient-data | – | – |
| 2025-03 | 17 | 22.225 | 0.9376 | hold | R1 R3 | Deployment frequency |
| 2025-04 | 4 | – | – | scale | R0 | – |
| 2025-05 | 13 | 27.107 | 1.0 | scale | R0 | – |
| 2025-06 | 5 | 3.951 | 1.0 | scale | R0 | – |
| 2025-07 | 3 | 4.754 | 1.0 | scale | R0 | – |
| 2025-08 | 19 | 33.842 | 1.0 | scale | R0 | – |
| 2025-09 | 15 | 32.235 | 1.0 | scale | R0 | – |
| 2025-10 | 5 | – | – | scale | R0 | – |
| 2025-11 | 18 | 22.851 | 1.0 | address | R5 | Lead time |
| 2025-12 | 22 | 23.578 | 0.7812 | address | R3 R5 | Lead time |
| 2026-01 | 14 | 27.388 | 1.0 | hold | R1 R3 R5 | Lead time |
| 2026-02 | 11 | 16.983 | 0.7906 | address | R3 | – |
| 2026-03 | 27 | 12.731 | 1.0 | scale | R0 | – |
| 2026-04 | 21 | 59.108 | 0.8481 | scale | R0 | – |
| 2026-05 | 38 | 83.88 | 0.7915 | hold | R1 | – |
| 2026-06 | 17 | 30.871 | 0.7375 | scale | R0 | – |
| 2026-07 | 4 | – | – | address | R3 | – |
| 2026-08 | 15 | 33.951 | 1.0 | address | R3 | – |
| 2026-09 | 38 | 47.999 | 0.8056 | address | R3 | – |
| 2026-10 | 12 | 9.085 | 1.0 | scale | R0 | – |
