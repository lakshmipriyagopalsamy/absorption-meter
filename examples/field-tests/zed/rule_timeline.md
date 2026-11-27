# Decision rules replayed month by month: https://github.com/zed-industries/zed

Dataset commit `da3a2740330a`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 672 | 1262.98 | 0.4078 | insufficient-data | – | – |
| 2025-02 | 773 | 1386.888 | 0.2423 | insufficient-data | – | – |
| 2025-03 | 877 | 1724.471 | 0.3151 | hold | R1 R3 R5 | Lead time |
| 2025-04 | 924 | 2080.107 | 0.3001 | hold | R1 R3 R5 | Lead time |
| 2025-05 | 911 | 1946.617 | 0.3286 | address | R5 | Lead time |
| 2025-06 | 772 | 1704.042 | 0.3892 | address | R5 | Lead time |
| 2025-07 | 698 | 1463.617 | 0.3741 | address | R5 | Lead time |
| 2025-08 | 802 | 1604.324 | 0.1695 | address | R5 | Lead time |
| 2025-09 | 765 | 1495.092 | 0.4018 | scale | R0 | – |
| 2025-10 | 879 | 1873.052 | 0.2407 | address | R3 | – |
| 2025-11 | 764 | 1563.019 | 0.4025 | scale | R0 | – |
| 2025-12 | 738 | 2124.83 | 0.3046 | scale | R0 | – |
| 2026-01 | 808 | 1743.434 | 0.2322 | scale | R0 | – |
| 2026-02 | 935 | 1870.374 | 0.2799 | address | R5 | Lead time |
| 2026-03 | 933 | 1974.751 | 0.3241 | address | R5 | Lead time |
| 2026-04 | 865 | 2012.969 | 0.2024 | address | R5 | Lead time |
| 2026-05 | 644 | 1541.354 | 0.4755 | address | R5 | Lead time |
| 2026-06 | 628 | 1754.373 | 0.4481 | address | R5 | – |
| 2026-07 | 631 | 1462.916 | 0.354 | address | R5 | – |
| 2026-08 | 392 | 742.239 | 0.5688 | address | R5 | – |
| 2026-09 | 420 | 1051.096 | 0.4755 | address | R5 | – |
| 2026-10 | 449 | 1220.243 | 0.4724 | address | R5 | – |
