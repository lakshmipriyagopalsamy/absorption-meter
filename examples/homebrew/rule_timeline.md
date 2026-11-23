# Decision rules replayed month by month: https://github.com/Homebrew/brew

Dataset commit `3e47189a707c`. Each row uses only history up to the end of that month. Baseline: mean/SD, last 3 months vs the 6 before. The newest month's absorption ratio is provisional: its rework window is still open.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 61 | 89.957 | 0.9071 | insufficient-data | – | – |
| 2025-02 | 87 | 169.365 | 0.7491 | insufficient-data | – | – |
| 2025-03 | 125 | 165.795 | 0.7671 | address | R5 | Lead time |
| 2025-04 | 105 | 164.367 | 0.8241 | address | R3 R5 | Lead time |
| 2025-05 | 74 | 84.577 | 1.0 | scale | R0 | – |
| 2025-06 | 121 | 192.703 | 0.7897 | scale | R0 | – |
| 2025-07 | 99 | 165.791 | 0.9308 | scale | R0 | – |
| 2025-08 | 188 | 282.911 | 0.5119 | hold | R1 R3 R5 | Lead time |
| 2025-09 | 130 | 221.646 | 0.6244 | address | R3 | Deployment frequency |
| 2025-10 | 123 | 235.769 | 0.7568 | hold | R1 R3 | Deployment frequency |
| 2025-11 | 125 | 218.119 | 0.8255 | scale | R0 | – |
| 2025-12 | 133 | 272.993 | 0.8772 | scale | R0 | – |
| 2026-01 | 84 | 117.603 | 0.8893 | scale | R0 | – |
| 2026-02 | 86 | 183.011 | 0.6793 | address | R4 R5 | – |
| 2026-03 | 162 | 262.379 | 0.7256 | address | R5 | Lead time |
| 2026-04 | 170 | 391.818 | 0.6546 | address | R5 | Lead time |
| 2026-05 | 264 | 549.503 | 0.5145 | hold | R1 R3 R5 | Lead time |
| 2026-06 | 275 | 666.321 | 0.5515 | hold | R1 R3 R5 | Deployment frequency; Lead time |
| 2026-07 | 361 | 696.331 | 0.7135 | hold | R1 R3 R5 | Deployment frequency; Lead time |
| 2026-08 | 245 | 492.508 | 0.6387 | address | R3 R5 | Deployment frequency; Lead time |
| 2026-09 | 317 | 960.155 | 0.5864 | address | R5 | Lead time |
| 2026-10 | 194 | 433.971 | 0.7769 | address | R5 | Lead time |
