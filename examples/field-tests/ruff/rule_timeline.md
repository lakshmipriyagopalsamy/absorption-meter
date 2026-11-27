# Decision rules replayed month by month: https://github.com/astral-sh/ruff

Dataset commit `ee3883e05955`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 336 | 802.732 | 0.7879 | insufficient-data | – | – |
| 2025-02 | 268 | 631.854 | 0.6612 | insufficient-data | – | – |
| 2025-03 | 292 | 658.72 | 0.6391 | address | R5 | Lead time |
| 2025-04 | 379 | 834.494 | 0.3919 | address | R2 | Change failure rate |
| 2025-05 | 376 | 961.444 | 0.4707 | address | R2 | Change failure rate |
| 2025-06 | 337 | 547.145 | 0.5013 | address | R2 | Change failure rate |
| 2025-07 | 354 | 748.331 | 0.4322 | address | R2 | Change failure rate |
| 2025-08 | 297 | 672.31 | 0.3347 | address | R3 | – |
| 2025-09 | 266 | 567.73 | 0.3456 | address | R3 R4 | – |
| 2025-10 | 288 | 660.157 | 0.4011 | address | R3 | – |
| 2025-11 | 293 | 641.325 | 0.5349 | address | R5 | – |
| 2025-12 | 384 | 1050.5 | 0.3737 | address | R5 | Lead time |
| 2026-01 | 419 | 843.128 | 0.3735 | address | R3 R5 | Lead time |
| 2026-02 | 336 | 714.953 | 0.5472 | scale | R0 | – |
| 2026-03 | 341 | 908.373 | 0.4661 | scale | R0 | – |
| 2026-04 | 313 | 839.428 | 0.4196 | address | R5 | Lead time |
| 2026-05 | 234 | 445.475 | 0.5926 | address | R5 | Lead time |
| 2026-06 | 476 | 1085.135 | 0.5233 | address | R3 | – |
| 2026-07 | 448 | 960.408 | 0.5292 | address | R3 | – |
| 2026-08 | 445 | 981.964 | 0.4791 | address | R3 R5 | Lead time |
| 2026-09 | 410 | 1045.651 | 0.4261 | address | R3 R5 | Lead time |
| 2026-10 | 341 | 733.27 | 0.6167 | address | R5 | Lead time |
