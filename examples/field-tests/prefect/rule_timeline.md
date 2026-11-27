# Decision rules replayed month by month: https://github.com/prefecthq/prefect

Dataset commit `5f7d879aa163`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 227 | 575.014 | 0.7521 | insufficient-data | – | – |
| 2025-02 | 214 | 454.194 | 0.7326 | insufficient-data | – | – |
| 2025-03 | 158 | 351.18 | 0.6051 | address | R2 | – |
| 2025-04 | 138 | 409.854 | 0.7656 | address | R2 | – |
| 2025-05 | 72 | 181.43 | 0.875 | address | R2 | Change failure rate |
| 2025-06 | 96 | 203.541 | 0.7078 | address | R2 | Change failure rate |
| 2025-07 | 98 | 245.665 | 0.8488 | scale | R0 | – |
| 2025-08 | 83 | 129.574 | 0.907 | scale | R0 | – |
| 2025-09 | 94 | 223.165 | 0.7612 | address | R4 R5 | – |
| 2025-10 | 96 | 243.921 | 0.9104 | address | R4 | – |
| 2025-11 | 67 | 144.639 | 0.7799 | scale | R0 | – |
| 2025-12 | 87 | 228.129 | 0.8554 | scale | R0 | – |
| 2026-01 | 100 | 244.998 | 0.9149 | scale | R0 | – |
| 2026-02 | 106 | 253.702 | 0.7967 | address | R5 | Lead time |
| 2026-03 | 103 | 307.09 | 0.8984 | address | R2 R5 | Lead time; Change failure rate |
| 2026-04 | 35 | 67.826 | 0.6271 | address | R2 R5 | Lead time; Change failure rate |
| 2026-05 | 80 | 248.874 | 0.7972 | address | R2 R4 | Change failure rate |
| 2026-06 | 47 | 125.313 | 0.8724 | scale | R0 | – |
| 2026-07 | 34 | 71.077 | 1.0 | scale | R0 | – |
| 2026-08 | 46 | 80.097 | 0.8477 | scale | R0 | – |
| 2026-09 | 38 | 65.263 | 1.0 | scale | R0 | – |
| 2026-10 | 93 | 113.835 | 0.7843 | scale | R0 | – |
