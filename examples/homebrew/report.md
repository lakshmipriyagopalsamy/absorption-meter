# Absorption report: https://github.com/Homebrew/brew

4176 mainline changes, 2024-07 to 2026-10. Rework window 14 days. Deployment frequency uses releases (tags). Pull-request data: no. Team data: no.

## Decision

🟡 **Address**: Absorption is holding, but an indicator has moved: fix it before scaling further.

In this order (contracts define what to verify, verification what to observe; the order is a hypothesis):

1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Rework rate | flat (5.8 → 6.7) | flat (0.29 → 0.25) | ✅ no signal | Rework keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | up (38.5 → 59.3) | ⚠️ debt signal | Each change costs more (more areas or lines per change): look for hidden coupling. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.65 → 0.74) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | flat (96.0 → 102.0) | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR | Rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 167 | 0.66 | 0.28 | 10 | 1.14 | 0.00 | 5 | 145 | 0 |
| 2024-08 | 148 | 0.78 | 0.20 | 14 | 1.20 | 0.00 | 6 | 100 | 0 |
| 2024-09 | 129 | 0.81 | 0.15 | 8.00 | 1.13 | 0.00 | 6 | 104 | 0 |
| 2024-10 | 76 | 0.99 | 0.01 | 14 | 1.13 | 0.00 | 4 | 161 | 0 |
| 2024-11 | 57 | 0.88 | 0.09 | 18 | 1.05 | 0.00 | 5 | 76 | 0 |
| 2024-12 | 70 | 0.90 | 0.07 | 11 | 1.13 | 0.00 | 6 | 109 | 0 |
| 2025-01 | 61 | 0.79 | 0.15 | 9.00 | 1.25 | 0.00 | 5 | 77 | 0 |
| 2025-02 | 87 | 0.62 | 0.31 | 16 | 1.34 | 0.00 | 3 | 155 | 0 |
| 2025-03 | 125 | 0.78 | 0.14 | 12 | 1.31 | 0.00 | 5 | 97 | 0 |
| 2025-04 | 105 | 0.78 | 0.16 | 12 | 1.26 | 0.00 | 6 | 113 | 0 |
| 2025-05 | 74 | 0.96 | 0.04 | 9.50 | 1.23 | 0.00 | 4 | 141 | 0 |
| 2025-06 | 121 | 0.80 | 0.14 | 22 | 1.22 | 0.00 | 4 | 92 | 0 |
| 2025-07 | 99 | 0.73 | 0.22 | 15 | 1.19 | 0.00 | 5 | 61 | 0 |
| 2025-08 | 188 | 0.63 | 0.29 | 18 | 1.17 | 0.00 | 8 | 54 | 0 |
| 2025-09 | 130 | 0.60 | 0.28 | 12 | 1.34 | 0.00 | 8 | 95 | 0 |
| 2025-10 | 123 | 0.72 | 0.25 | 10 | 1.26 | 0.00 | 4 | 142 | 0 |
| 2025-11 | 125 | 0.88 | 0.08 | 13 | 1.34 | 0.00 | 5 | 90 | 0 |
| 2025-12 | 133 | 0.86 | 0.13 | 24 | 1.20 | 0.00 | 5 | 155 | 0 |
| 2026-01 | 84 | 0.89 | 0.12 | 17 | 1.18 | 0.00 | 4 | 140 | 0 |
| 2026-02 | 86 | 0.75 | 0.21 | 29 | 1.13 | 0.00 | 3 | 157 | 0 |
| 2026-03 | 162 | 0.78 | 0.15 | 20 | 1.20 | 0.00 | 5 | 80 | 0 |
| 2026-04 | 170 | 0.65 | 0.26 | 34 | 1.20 | 0.00 | 5 | 109 | 0 |
| 2026-05 | 264 | 0.48 | 0.42 | 62 | 1.47 | 0.00 | 6 | 74 | 0 |
| 2026-06 | 275 | 0.56 | 0.39 | 40 | 1.26 | 0.00 | 8 | 78 | 0 |
| 2026-07 | 361 | 0.67 | 0.28 | 47 | 1.32 | 0.00 | 8 | 78 | 0 |
| 2026-08 | 245 | 0.68 | 0.27 | 55 | 1.33 | 0.00 | 6 | 130 | 0 |
| 2026-09 | 317 | 0.65 | 0.30 | 64 | 1.34 | 0.00 | 10 | 49 | 0 |
| 2026-10 | 194 | 0.78 | 0.18 | 59 | 1.34 | 0.00 | 4 | 127 | 0 |

## Reading this report

AR (absorption ratio) is the size-weighted share of changes not reworked within the window. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

_absorption-meter 0.1.0_
