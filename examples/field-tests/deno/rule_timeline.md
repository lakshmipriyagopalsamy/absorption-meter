# Decision rules replayed month by month: https://github.com/denoland/deno

Dataset commit `ddbb5004864c`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 156 | 339.775 | 0.3043 | insufficient-data | – | – |
| 2025-02 | 161 | 350.5 | 0.1873 | insufficient-data | – | – |
| 2025-03 | 93 | 175.821 | 0.2944 | address | R3 | – |
| 2025-04 | 214 | 407.435 | 0.3573 | scale | R0 | – |
| 2025-05 | 195 | 466.711 | 0.3402 | address | R3 | Deployment frequency |
| 2025-06 | 214 | 529.993 | 0.2188 | scale | R0 | – |
| 2025-07 | 125 | 291.741 | 0.2024 | address | R3 | – |
| 2025-08 | 117 | 246.949 | 0.3003 | scale | R0 | – |
| 2025-09 | 133 | 364.63 | 0.3331 | address | R5 | – |
| 2025-10 | 103 | 194.457 | 0.3605 | address | R4 | – |
| 2025-11 | 118 | 256.902 | 0.3843 | address | R4 | – |
| 2025-12 | 120 | 405.672 | 0.2893 | scale | R0 | – |
| 2026-01 | 134 | 263.601 | 0.2988 | scale | R0 | – |
| 2026-02 | 202 | 366.973 | 0.231 | scale | R0 | – |
| 2026-03 | 386 | 1171.505 | 0.1839 | hold | R1 R3 R5 | Lead time |
| 2026-04 | 352 | 384.838 | 0.2384 | hold | R1 R3 R5 | Lead time |
| 2026-05 | 506 | 1339.09 | 0.1241 | hold | R1 R3 R5 | Lead time |
| 2026-06 | 588 | 2003.389 | 0.1937 | hold | R1 R3 R4 R5 | Lead time |
| 2026-07 | 306 | 965.755 | 0.3787 | address | R5 | Lead time |
| 2026-08 | 150 | 421.64 | 0.5842 | address | R3 R4 R5 | Lead time |
| 2026-09 | 34 | 124.963 | 0.7874 | address | R3 R5 | – |
| 2026-10 | 22 | 54.643 | 0.9205 | address | R5 | – |
