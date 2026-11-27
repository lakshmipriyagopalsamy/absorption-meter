# Decision rules replayed month by month: https://github.com/getsentry/sentry-python

Dataset commit `566beb013a98`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 26 | 60.111 | 0.9013 | insufficient-data | – | – |
| 2025-02 | 49 | 128.997 | 0.7951 | insufficient-data | – | – |
| 2025-03 | 55 | 74.473 | 0.6914 | address | R3 | – |
| 2025-04 | 50 | 103.5 | 0.7454 | address | R3 | Deployment frequency |
| 2025-05 | 23 | 28.741 | 0.4256 | address | R3 | Deployment frequency |
| 2025-06 | 31 | 39.807 | 0.7972 | address | R3 | – |
| 2025-07 | 47 | 56.548 | 0.8184 | scale | R0 | – |
| 2025-08 | 20 | 60.315 | 0.9466 | address | R5 | Lead time |
| 2025-09 | 75 | 141.515 | 0.434 | address | R4 | – |
| 2025-10 | 63 | 138.853 | 0.5253 | address | R3 R4 R5 | Lead time |
| 2025-11 | 61 | 69.116 | 0.2949 | hold | R1 R3 R4 R5 | Lead time |
| 2025-12 | 50 | 158.298 | 0.7238 | hold | R1 R3 R5 | Lead time |
| 2026-01 | 72 | 136.022 | 0.4239 | address | R3 R5 | Lead time |
| 2026-02 | 65 | 174.697 | 0.258 | address | R3 R5 | Lead time |
| 2026-03 | 130 | 311.901 | 0.3798 | hold | R1 R3 R5 | Lead time |
| 2026-04 | 79 | 134.11 | 0.7407 | address | R5 | Lead time |
| 2026-05 | 108 | 212.908 | 0.3567 | address | R5 | Lead time |
| 2026-06 | 125 | 275.83 | 0.6425 | scale | R0 | – |
| 2026-07 | 105 | 147.403 | 0.4034 | address | R5 | Lead time |
| 2026-08 | 120 | 233.741 | 0.4017 | address | R5 | Lead time |
| 2026-09 | 178 | 612.997 | 0.7277 | address | R5 | Lead time |
| 2026-10 | 119 | 439.448 | 0.8348 | address | R5 | Lead time |
