# Decision rules replayed month by month: https://github.com/Homebrew/brew

Dataset commit `3e47189a707c`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: median/MAD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 61 | 89.957 | 0.9071 | insufficient-data | – | – |
| 2025-02 | 87 | 169.365 | 0.7491 | insufficient-data | – | – |
| 2025-03 | 125 | 165.795 | 0.8267 | address | R5 | Lead time |
| 2025-04 | 105 | 173.549 | 0.8673 | address | R5 | Lead time |
| 2025-05 | 74 | 88.921 | 1.0 | address | R5 | Lead time |
| 2025-06 | 121 | 212.003 | 0.7726 | scale | R0 | – |
| 2025-07 | 99 | 165.791 | 0.9308 | address | R5 | Lead time |
| 2025-08 | 188 | 312.409 | 0.5244 | address | R3 R5 | Lead time |
| 2025-09 | 130 | 221.646 | 0.6244 | address | R3 | – |
| 2025-10 | 123 | 242.583 | 0.7565 | address | R3 | – |
| 2025-11 | 125 | 252.539 | 0.8493 | address | R3 | – |
| 2025-12 | 133 | 281.806 | 0.881 | scale | R0 | – |
| 2026-01 | 84 | 121.005 | 0.8776 | scale | R0 | – |
| 2026-02 | 86 | 183.011 | 0.7008 | address | R4 R5 | – |
| 2026-03 | 162 | 266.368 | 0.7297 | address | R5 | – |
| 2026-04 | 170 | 400.443 | 0.6653 | address | R5 | Lead time |
| 2026-05 | 264 | 553.737 | 0.5135 | hold | R1 R3 R5 | Lead time |
| 2026-06 | 275 | 680.343 | 0.5606 | hold | R1 R3 R5 | Lead time |
| 2026-07 | 361 | 696.331 | 0.7135 | hold | R1 R3 R5 | Lead time |
| 2026-08 | 245 | 492.508 | 0.6387 | hold | R1 R3 R5 | Lead time |
| 2026-09 | 317 | 960.155 | 0.8661 | address | R5 | Lead time |
| 2026-10 | 194 | 433.971 | 0.7769 | address | R5 | Lead time |
