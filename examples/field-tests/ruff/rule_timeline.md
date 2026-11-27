# Decision rules replayed month by month: https://github.com/astral-sh/ruff

Dataset commit `ee3883e05955`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 336 | 802.732 | 0.7976 | insufficient-data | – | – |
| 2025-02 | 268 | 631.854 | 0.7601 | insufficient-data | – | – |
| 2025-03 | 292 | 658.72 | 0.8163 | address | R5 | Lead time |
| 2025-04 | 379 | 834.494 | 0.6059 | address | R2 | Change failure rate |
| 2025-05 | 376 | 961.444 | 0.5127 | address | R2 | Change failure rate |
| 2025-06 | 337 | 547.145 | 0.5167 | address | R2 | Change failure rate |
| 2025-07 | 354 | 748.331 | 0.4492 | address | R2 | Change failure rate |
| 2025-08 | 297 | 672.31 | 0.3462 | address | R3 | – |
| 2025-09 | 266 | 567.73 | 0.4055 | address | R3 R4 | – |
| 2025-10 | 288 | 660.157 | 0.4407 | address | R3 | – |
| 2025-11 | 293 | 641.325 | 0.548 | address | R5 | – |
| 2025-12 | 384 | 1050.5 | 0.3801 | address | R5 | Lead time |
| 2026-01 | 419 | 843.128 | 0.4233 | address | R3 R5 | Lead time |
| 2026-02 | 336 | 714.953 | 0.5555 | scale | R0 | – |
| 2026-03 | 341 | 908.373 | 0.5019 | scale | R0 | – |
| 2026-04 | 313 | 839.428 | 0.4196 | address | R5 | Lead time |
| 2026-05 | 234 | 445.475 | 0.6087 | address | R5 | Lead time |
| 2026-06 | 476 | 1085.135 | 0.5814 | address | R3 | – |
| 2026-07 | 448 | 960.408 | 0.5292 | address | R3 | – |
| 2026-08 | 445 | 981.964 | 0.5267 | address | R3 R5 | Lead time |
| 2026-09 | 410 | 1045.651 | 0.4405 | address | R3 R5 | Lead time |
| 2026-10 | 341 | 733.27 | 0.6339 | address | R5 | Lead time |
