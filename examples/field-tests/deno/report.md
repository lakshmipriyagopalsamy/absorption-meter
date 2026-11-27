# Absorption report: https://github.com/denoland/deno

5712 mainline changes, 2024-07 to 2026-10. Rework window 14 days (strict rule). Deployment frequency uses releases (tags). Pull-request data: no. Team data: no.

## Decision

🟡 **Address**: Absorption is holding, but an indicator has moved: fix it before scaling further.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | down (4.2 → 0.00) | flat (0.26 → 0.33) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | up (92.0 → 136.2) | ✅ no signal | Change cost is steady. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | n/a | flat (0.00 → 0.00) | … not enough data | Needs 9 months of history. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 184 | 0.26 | 0.66 | 0.33 | 0.19 | 54 | 2.28 | 0.02 | 1 | – | 0 |
| 2024-08 | 257 | 0.27 | 0.66 | 0.40 | 0.17 | 56 | 1.84 | 0.01 | 1 | – | 0 |
| 2024-09 | 321 | 0.35 | 0.58 | 0.31 | 0.21 | 54 | 1.98 | 0.00 | 0 | – | 0 |
| 2024-10 | 221 | 0.44 | 0.49 | 0.47 | 0.24 | 36 | 1.85 | 0.02 | 1 | – | 0 |
| 2024-11 | 182 | 0.38 | 0.53 | 0.28 | 0.25 | 62 | 2.21 | 0.00 | 1 | – | 0 |
| 2024-12 | 118 | 0.41 | 0.51 | 0.35 | 0.22 | 74 | 2.24 | 0.01 | 0 | – | 0 |
| 2025-01 | 156 | 0.43 | 0.53 | 0.40 | 0.26 | 72 | 2.22 | 0.00 | 0 | – | 0 |
| 2025-02 | 161 | 0.36 | 0.57 | 0.41 | 0.20 | 60 | 1.99 | 0.01 | 1 | – | 0 |
| 2025-03 | 93 | 0.50 | 0.40 | 0.49 | 0.28 | 49 | 2.02 | 0.00 | 0 | – | 0 |
| 2025-04 | 214 | 0.44 | 0.49 | 0.40 | 0.18 | 44 | 1.97 | 0.00 | 2 | 2.99 | 0 |
| 2025-05 | 195 | 0.43 | 0.49 | 0.53 | 0.21 | 40 | 1.83 | 0.01 | 4 | 12 | 0 |
| 2025-06 | 214 | 0.32 | 0.60 | 0.30 | 0.17 | 78 | 2 | 0.01 | 2 | – | 0 |
| 2025-07 | 125 | 0.32 | 0.59 | 0.40 | 0.17 | 70 | 2.33 | 0.00 | 4 | 153 | 0 |
| 2025-08 | 117 | 0.30 | 0.62 | 0.37 | 0.11 | 59 | 2.13 | 0.00 | 2 | – | 0 |
| 2025-09 | 133 | 0.46 | 0.47 | 0.26 | 0.33 | 67 | 2.19 | 0.01 | 3 | 163 | 0 |
| 2025-10 | 103 | 0.53 | 0.41 | 0.26 | 0.29 | 59 | 2.24 | 0.02 | 4 | 91 | 0 |
| 2025-11 | 118 | 0.41 | 0.49 | 0.34 | 0.19 | 58 | 1.99 | 0.03 | 0 | – | 0 |
| 2025-12 | 120 | 0.40 | 0.53 | 0.23 | 0.23 | 60 | 2.23 | 0.03 | 3 | 21 | 0 |
| 2026-01 | 134 | 0.44 | 0.49 | 0.22 | 0.24 | 78 | 2.21 | 0.00 | 4 | 129 | 0 |
| 2026-02 | 202 | 0.40 | 0.54 | 0.24 | 0.21 | 68 | 2.15 | 0.01 | 5 | 142 | 0 |
| 2026-03 | 386 | 0.33 | 0.63 | 0.30 | 0.22 | 109 | 2.08 | 0.00 | 9 | 35 | 0 |
| 2026-04 | 352 | 0.27 | 0.68 | 0.15 | 0.16 | 56 | 1.97 | 0.01 | 4 | 145 | 0 |
| 2026-05 | 506 | 0.22 | 0.72 | 0.24 | 0.12 | 98 | 1.96 | 0.00 | 2 | 122 | 0 |
| 2026-06 | 588 | 0.26 | 0.71 | 0.24 | 0.15 | 126 | 2.03 | 0.00 | 3 | 146 | 0 |
| 2026-07 | 306 | 0.49 | 0.48 | 0.41 | 0.23 | 94 | 1.94 | 0.00 | 2 | 165 | 0 |
| 2026-08 | 150 | 0.62 | 0.34 | 0.36 | 0.14 | 124 | 1.93 | 0.00 | 0 | – | 0 |
| 2026-09 | 34 | 0.86 | 0.15 | 0.37 | – | 156 | 1.79 | 0.00 | 0 | – | 0 |
| 2026-10 | 22 | 0.92 | 0.09 | 0.25 | – | 128 | 2.23 | 0.00 | 0 | – | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.3.0_
