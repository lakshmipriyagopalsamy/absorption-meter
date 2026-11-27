# Decision rules replayed month by month: https://github.com/fastapi/fastapi

Dataset commit `05e6df7e906c`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 70 | 117.751 | 1.0 | insufficient-data | – | – |
| 2025-02 | 57 | 70.408 | 1.0 | insufficient-data | – | – |
| 2025-03 | 26 | 37.072 | 1.0 | address | R5 | Lead time |
| 2025-04 | 10 | 24.242 | 1.0 | scale | R0 | – |
| 2025-05 | 26 | 44.032 | 1.0 | scale | R0 | – |
| 2025-06 | 37 | 45.128 | 1.0 | address | R5 | – |
| 2025-07 | 31 | 47.294 | 1.0 | address | R3 | – |
| 2025-08 | 20 | 26.527 | 1.0 | scale | R0 | – |
| 2025-09 | 47 | 28.133 | 1.0 | address | R5 | Lead time |
| 2025-10 | 39 | 68.345 | 0.8091 | address | R3 R5 | Lead time |
| 2025-11 | 39 | 67.583 | 0.8646 | hold | R1 R3 R5 | Lead time |
| 2025-12 | 126 | 342.307 | 0.6783 | hold | R1 R3 R5 | Lead time |
| 2026-01 | 35 | 105.334 | 0.944 | scale | R0 | – |
| 2026-02 | 147 | 426.585 | 0.7297 | address | R5 | Lead time |
| 2026-03 | 53 | 82.927 | 0.8194 | address | R5 | Lead time |
| 2026-04 | 20 | 49.316 | 0.829 | address | R3 R5 | Lead time |
| 2026-05 | 46 | 28.364 | 1.0 | address | R5 | Lead time |
| 2026-06 | 73 | 198.941 | 0.7271 | scale | R0 | – |
| 2026-07 | 105 | 245.832 | 0.898 | scale | R0 | – |
| 2026-08 | 22 | 60.769 | 0.9397 | address | R3 R4 | – |
| 2026-09 | 6 | – | – | scale | R0 | – |
| 2026-10 | 54 | 46.328 | 0.7298 | address | R5 | – |
