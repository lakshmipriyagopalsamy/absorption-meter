# Absorption report: https://github.com/getsentry/sentry-python

1901 mainline changes, 2024-07 to 2026-10. Rework window 14 days. Deployment frequency uses releases (tags). Pull-request data: no. Team data: no.

## Decision

🟡 **Address**: Absorption is holding, but an indicator has moved: fix it before scaling further.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | flat (2.8 → 3.3) | down (0.39 → 0.18) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | up (1.7 → 2.1) | ⚠️ debt signal | Each change costs more (more areas or lines per change): look for hidden coupling. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.11 → 0.07) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 80 | 0.72 | 0.28 | 0.42 | 0.30 | 21 | 1.62 | 0.01 | 5 | – | 0 |
| 2024-08 | 27 | 0.77 | 0.22 | 0.29 | 0.37 | 51 | 2.04 | 0.04 | 1 | – | 0 |
| 2024-09 | 33 | 0.74 | 0.24 | 0.38 | 0.42 | 35 | 1.67 | 0.00 | 1 | – | 0 |
| 2024-10 | 56 | 0.70 | 0.20 | 0.41 | 0.41 | 16 | 1.57 | 0.00 | 3 | – | 0 |
| 2024-11 | 26 | 0.81 | 0.12 | 0.50 | 0.38 | 27 | 1.77 | 0.04 | 2 | – | 0 |
| 2024-12 | 28 | 0.87 | 0.18 | 0.42 | 0.50 | 28 | 1.71 | 0.04 | 2 | 17 | 0 |
| 2025-01 | 26 | 0.93 | 0.08 | 0.47 | 0.50 | 32 | 1.73 | 0.00 | 1 | – | 0 |
| 2025-02 | 49 | 0.77 | 0.18 | 0.54 | 0.45 | 43 | 2.08 | 0.00 | 2 | – | 0 |
| 2025-03 | 55 | 0.72 | 0.24 | 0.67 | 0.35 | 22 | 1.64 | 0.04 | 5 | 50 | 0 |
| 2025-04 | 50 | 0.76 | 0.24 | 0.51 | 0.46 | 20 | 1.86 | 0.02 | 4 | 22 | 0 |
| 2025-05 | 23 | 0.67 | 0.22 | 0.47 | 0.35 | 18 | 1.65 | 0.00 | 3 | 0.84 | 0 |
| 2025-06 | 31 | 0.78 | 0.26 | 0.44 | 0.48 | 45 | 2.03 | 0.03 | 3 | – | 0 |
| 2025-07 | 47 | 0.85 | 0.13 | 0.55 | 0.49 | 16 | 1.57 | 0.00 | 5 | 23 | 0 |
| 2025-08 | 20 | 0.94 | 0.10 | 0.39 | 0.70 | 48 | 2.05 | 0.00 | 2 | 146 | 0 |
| 2025-09 | 75 | 0.59 | 0.37 | 0.70 | 0.33 | 27 | 2.09 | 0.00 | 6 | 98 | 0 |
| 2025-10 | 63 | 0.55 | 0.38 | 0.34 | 0.43 | 49 | 2.32 | 0.00 | 5 | 124 | 0 |
| 2025-11 | 61 | 0.45 | 0.52 | 0.34 | 0.39 | 34 | 2.03 | 0.00 | 3 | – | 0 |
| 2025-12 | 50 | 0.74 | 0.24 | 0.33 | 0.52 | 48 | 1.80 | 0.00 | 2 | – | 0 |
| 2026-01 | 72 | 0.40 | 0.51 | 0.32 | 0.31 | 61 | 1.72 | 0.01 | 3 | – | 0 |
| 2026-02 | 65 | 0.43 | 0.52 | 0.60 | 0.32 | 65 | 1.54 | 0.00 | 2 | – | 0 |
| 2026-03 | 130 | 0.49 | 0.48 | 0.45 | 0.35 | 62 | 1.59 | 0.00 | 4 | – | 0 |
| 2026-04 | 79 | 0.49 | 0.43 | 0.36 | 0.35 | 51 | 1.62 | 0.01 | 1 | – | 0 |
| 2026-05 | 108 | 0.46 | 0.49 | 0.38 | 0.39 | 95 | 1.60 | 0.01 | 3 | 94 | 0 |
| 2026-06 | 125 | 0.69 | 0.24 | 0.36 | 0.55 | 37 | 1.80 | 0.00 | 4 | – | 0 |
| 2026-07 | 105 | 0.41 | 0.54 | 0.20 | 0.22 | 125 | 1.86 | 0.00 | 3 | 144 | 0 |
| 2026-08 | 120 | 0.58 | 0.45 | 0.27 | – | 124 | 2.22 | 0.00 | 3 | – | 0 |
| 2026-09 | 178 | 0.79 | 0.19 | 0.12 | – | 280 | 2.06 | 0.00 | 5 | 6.12 | 0 |
| 2026-10 | 119 | 0.83 | 0.12 | 0.16 | – | 58 | 1.92 | 0.00 | 2 | – | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.2.1_
