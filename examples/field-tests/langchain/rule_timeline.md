# Decision rules replayed month by month: https://github.com/langchain-ai/langchain

Dataset commit `30c4e38d71c2`. Each row uses only history up to the end of that month, and P and AR include only changes whose 14-day rework window had fully elapsed by then; later changes enter once their window matures. Baseline: mean/SD, last 3 months vs the 6 before.

| As of | Changes | P | AR | Verdict | Rules | Pairs signalling debt |
|---|---|---|---|---|---|---|
| 2025-01 | 225 | 337.314 | 0.623 | insufficient-data | – | – |
| 2025-02 | 216 | 336.53 | 0.4875 | insufficient-data | – | – |
| 2025-03 | 236 | 293.011 | 0.7365 | scale | R0 | – |
| 2025-04 | 231 | 499.213 | 0.5617 | scale | R0 | – |
| 2025-05 | 192 | 333.257 | 0.8236 | scale | R0 | – |
| 2025-06 | 164 | 217.794 | 0.7178 | scale | R0 | – |
| 2025-07 | 282 | 568.409 | 0.3598 | scale | R0 | – |
| 2025-08 | 161 | 324.879 | 0.7122 | address | R3 | – |
| 2025-09 | 238 | 548.747 | 0.5749 | address | R3 R5 | Lead time |
| 2025-10 | 342 | 1046.684 | 0.2335 | address | R5 | Lead time |
| 2025-11 | 138 | 351.192 | 0.388 | address | R3 R5 | Lead time |
| 2025-12 | 194 | 378.351 | 0.3943 | address | R3 | – |
| 2026-01 | 169 | 430.242 | 0.5249 | address | R5 | Lead time |
| 2026-02 | 151 | 275.785 | 0.5076 | scale | R0 | – |
| 2026-03 | 145 | 240.524 | 0.6006 | scale | R0 | – |
| 2026-04 | 124 | 228.96 | 0.6001 | scale | R0 | – |
| 2026-05 | 90 | 148.435 | 0.7099 | scale | R0 | – |
| 2026-06 | 144 | 367.869 | 0.3765 | scale | R0 | – |
| 2026-07 | 75 | 145.324 | 0.8233 | scale | R0 | – |
| 2026-08 | 144 | 286.728 | 0.561 | address | R5 | Lead time |
| 2026-09 | 86 | 111.325 | 0.6209 | address | R5 | – |
| 2026-10 | 63 | 108.086 | 0.6954 | scale | R0 | – |
