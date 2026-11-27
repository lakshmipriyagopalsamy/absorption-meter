# Decision rules replayed month by month: https://github.com/biomejs/biome

Dataset commit `f50b26295e4e`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 26 | 39.247 | 1.0 | insufficient-data | – | – |
| 2025-02 | 60 | 59.294 | 0.8042 | insufficient-data | – | – |
| 2025-03 | 129 | 315.085 | 0.5891 | scale | R0 | – |
| 2025-04 | 134 | 291.725 | 0.5441 | address | R3 R5 | Lead time |
| 2025-05 | 157 | 419.052 | 0.4605 | address | R3 R5 | Lead time |
| 2025-06 | 167 | 149.908 | 0.4012 | hold | R1 R3 R5 | Lead time |
| 2025-07 | 132 | 402.058 | 0.411 | hold | R1 R3 | – |
| 2025-08 | 102 | 287.671 | 0.6654 | scale | R0 | – |
| 2025-09 | 75 | 260.287 | 0.9515 | scale | R0 | – |
| 2025-10 | 67 | 106.972 | 0.9025 | scale | R0 | – |
| 2025-11 | 134 | 351.783 | 0.3818 | address | R5 | – |
| 2025-12 | 102 | 238.047 | 0.6637 | address | R5 | Lead time |
| 2026-01 | 78 | 151.72 | 0.8499 | address | R5 | Lead time |
| 2026-02 | 105 | 147.34 | 0.6587 | address | R5 | Lead time |
| 2026-03 | 181 | 557.268 | 0.5819 | address | R5 | Lead time |
| 2026-04 | 191 | 528.474 | 0.4228 | hold | R1 R3 R5 | Lead time |
| 2026-05 | 145 | 510.478 | 0.4236 | hold | R1 R3 R5 | Lead time |
| 2026-06 | 124 | 323.008 | 0.6066 | address | R3 R5 | Lead time |
| 2026-07 | 152 | 373.283 | 0.4483 | address | R5 | Lead time |
| 2026-08 | 183 | 529.311 | 0.4515 | address | R5 | Lead time |
| 2026-09 | 252 | 772.823 | 0.3874 | address | R5 | Lead time |
| 2026-10 | 375 | 1100.299 | 0.4884 | hold | R1 R3 R5 | Lead time |
