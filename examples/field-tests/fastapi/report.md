# Absorption report: https://github.com/fastapi/fastapi

1563 mainline changes, 2024-07 to 2026-10. Rework window 14 days. Deployment frequency uses releases (tags). Pull-request data: no. Team data: no.

## Decision

🟡 **Address**: Absorption is holding, but an indicator has moved: fix it before scaling further.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | flat (8.7 → 14.0) | down (0.69 → 0.28) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | up (1.5 → 2.0) | ✅ no signal | Change cost is steady. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.47 → 0.56) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | flat (23.0 → 4.8) | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 46 | 0.95 | 0.04 | 0.80 | 0.30 | 18 | 1.26 | 0.00 | 1 | – | 0 |
| 2024-08 | 99 | 0.77 | 0.16 | 0.83 | 0.38 | 12 | 1.29 | 0.00 | 3 | – | 0 |
| 2024-09 | 52 | 0.65 | 0.35 | 0.58 | 0.25 | 25 | 1.60 | 0.04 | 7 | 61 | 0 |
| 2024-10 | 125 | 0.74 | 0.22 | 0.77 | 0.09 | 32 | 1.14 | 0.00 | 4 | 64 | 0 |
| 2024-11 | 97 | 0.74 | 0.27 | 0.71 | 0.01 | 55 | 1.06 | 0.00 | 1 | – | 0 |
| 2024-12 | 55 | 0.99 | 0.02 | 0.67 | 0.05 | 76 | 1.15 | 0.00 | 1 | – | 0 |
| 2025-01 | 70 | 0.95 | 0.04 | 0.93 | 0.00 | 200 | 1.24 | 0.00 | 2 | – | 0 |
| 2025-02 | 57 | 0.98 | 0.02 | 0.57 | 0.02 | 74 | 1.14 | 0.02 | 2 | 27 | 0 |
| 2025-03 | 26 | 0.98 | 0.04 | 0.50 | 0.04 | 88 | 1.31 | 0.00 | 2 | – | 0 |
| 2025-04 | 10 | 1.00 | 0.00 | 0.00 | 0.00 | 68 | 1.50 | 0.00 | 0 | – | 0 |
| 2025-05 | 26 | 1.00 | 0.00 | – | 0.00 | 82 | 1.23 | 0.00 | 0 | – | 0 |
| 2025-06 | 37 | 0.97 | 0.03 | 0.70 | 0.22 | 21 | 1.22 | 0.00 | 2 | – | 0 |
| 2025-07 | 31 | 1.00 | 0.00 | 1.00 | 0.26 | 41 | 1.45 | 0.00 | 2 | 97 | 0 |
| 2025-08 | 20 | 0.85 | 0.10 | 0.50 | 0.05 | 51 | 1.45 | 0.00 | 0 | – | 0 |
| 2025-09 | 47 | 0.90 | 0.15 | 0.58 | 0.21 | 30 | 1.53 | 0.00 | 4 | 0.67 | 0 |
| 2025-10 | 39 | 0.72 | 0.18 | 0.64 | 0.13 | 12 | 1.67 | 0.00 | 10 | 37 | 0 |
| 2025-11 | 39 | 0.83 | 0.13 | 0.61 | 0.41 | 12 | 1.69 | 0.00 | 7 | 131 | 0 |
| 2025-12 | 126 | 0.76 | 0.18 | 0.51 | 0.40 | 38 | 1.67 | 0.00 | 20 | 6.96 | 0 |
| 2026-01 | 35 | 0.96 | 0.03 | 0.75 | 0.26 | 58 | 1.20 | 0.00 | 0 | – | 0 |
| 2026-02 | 147 | 0.75 | 0.18 | 0.68 | 0.20 | 43 | 1.63 | 0.00 | 18 | 24 | 0 |
| 2026-03 | 53 | 0.93 | 0.08 | 0.85 | 0.23 | 213 | 1.25 | 0.00 | 3 | 8.84 | 0 |
| 2026-04 | 20 | 0.88 | 0.10 | 0.64 | 0.55 | 54 | 2.10 | 0.00 | 4 | – | 0 |
| 2026-05 | 46 | 1.00 | 0.00 | 0.57 | 0.39 | 46 | 1.39 | 0.00 | 2 | 1.46 | 0 |
| 2026-06 | 73 | 0.72 | 0.32 | 0.71 | 0.25 | 42 | 1.47 | 0.00 | 6 | 80 | 0 |
| 2026-07 | 105 | 0.79 | 0.18 | 0.67 | 0.28 | 35 | 1.45 | 0.00 | 19 | 1.05 | 0 |
| 2026-08 | 22 | 0.95 | 0.05 | 0.80 | – | 36 | 1.32 | 0.00 | 0 | – | 0 |
| 2026-09 | 6 | 0.63 | 0.17 | 0.00 | – | 60 | 2.17 | 0.00 | 3 | 8.01 | 0 |
| 2026-10 | 54 | 0.73 | 0.21 | 0.05 | – | 162 | 2.46 | 0.00 | 39 | 1.58 | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.2.1_
