# Decision rules replayed month by month: https://github.com/excalidraw/excalidraw

Dataset commit `f4e5226a3d84`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 36 | 54.955 | 0.7425 | insufficient-data | – | – |
| 2025-02 | 18 | 58.571 | 0.9098 | insufficient-data | – | – |
| 2025-03 | 28 | 61.238 | 0.4557 | address | R5 | Lead time |
| 2025-04 | 23 | 55.884 | 0.4713 | address | R5 | Lead time |
| 2025-05 | 39 | 97.049 | 0.3936 | address | R3 | – |
| 2025-06 | 24 | 105.577 | 0.325 | hold | R1 R3 R5 | Lead time |
| 2025-07 | 14 | 26.366 | 1.0 | address | R5 | Lead time |
| 2025-08 | 16 | 30.4 | 0.123 | address | R3 R5 | Lead time |
| 2025-09 | 23 | 29.974 | 0.0733 | address | R3 | – |
| 2025-10 | 12 | 27.574 | 0.4109 | address | R3 | – |
| 2025-11 | 17 | 52.655 | 0.6509 | address | R3 | – |
| 2025-12 | 14 | 39.58 | 0.7853 | address | R3 | – |
| 2026-01 | 38 | 73.982 | 0.6082 | address | R5 | Lead time |
| 2026-02 | 24 | 40.518 | 0.2749 | scale | R0 | – |
| 2026-03 | 27 | 65.737 | 0.5149 | scale | R0 | – |
| 2026-04 | 7 | 9.708 | 1.0 | scale | R0 | – |
| 2026-05 | 15 | 57.473 | 0.8427 | address | R5 | Lead time |
| 2026-06 | 19 | 47.808 | 0.7535 | address | R5 | Lead time |
| 2026-07 | 38 | 151.098 | 0.4543 | address | R5 | Lead time |
| 2026-08 | 23 | 110.374 | 0.5307 | address | R5 | Lead time |
| 2026-09 | 38 | 65.69 | 0.5405 | address | R5 | Lead time |
| 2026-10 | 30 | 68.68 | 0.1311 | address | R3 R5 | Lead time |
