# Absorption report: https://github.com/astral-sh/ruff

8954 mainline changes, 2024-07 to 2026-10. Rework window 14 days (strict rule). Deployment frequency uses releases (tags). Pull-request data: no. Team data: no.

## Decision

🟡 **Address**: Absorption is holding, but an indicator has moved: fix it before scaling further.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | flat (4.2 → 4.3) | flat (0.83 → 0.86) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | up (81.9 → 114.7) | ⚠️ debt signal | Each change costs more (more areas or lines per change): look for hidden coupling. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.43 → 0.47) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | flat (151.0 → 143.7) | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 207 | 0.73 | 0.22 | 0.64 | 0.32 | 46 | 1.22 | 0.00 | 5 | 98 | 0 |
| 2024-08 | 236 | 0.65 | 0.29 | 0.57 | 0.23 | 56 | 1.24 | 0.00 | 6 | 141 | 0 |
| 2024-09 | 165 | 0.48 | 0.45 | 0.73 | 0.15 | 60 | 1.19 | 0.00 | 5 | 115 | 0 |
| 2024-10 | 179 | 0.39 | 0.53 | 0.75 | 0.18 | 54 | 1.23 | 0.00 | 3 | 167 | 2 |
| 2024-11 | 295 | 0.49 | 0.43 | 0.56 | 0.21 | 60 | 1.23 | 0.00 | 4 | 158 | 0 |
| 2024-12 | 239 | 0.67 | 0.30 | 0.63 | 0.32 | 69 | 1.18 | 0.00 | 3 | 166 | 0 |
| 2025-01 | 336 | 0.75 | 0.20 | 0.57 | 0.38 | 64 | 1.19 | 0.00 | 6 | 48 | 0 |
| 2025-02 | 268 | 0.74 | 0.22 | 0.60 | 0.34 | 75 | 1.19 | 0.00 | 5 | 54 | 0 |
| 2025-03 | 292 | 0.53 | 0.39 | 0.82 | 0.27 | 56 | 1.17 | 0.00 | 5 | 84 | 0 |
| 2025-04 | 379 | 0.44 | 0.47 | 0.80 | 0.16 | 67 | 1.19 | 0.00 | 5 | 154 | 1 |
| 2025-05 | 376 | 0.46 | 0.45 | 0.74 | 0.24 | 58 | 1.26 | 0.00 | 5 | 153 | 1 |
| 2025-06 | 337 | 0.53 | 0.38 | 0.67 | 0.27 | 41 | 1.19 | 0.00 | 3 | 164 | 0 |
| 2025-07 | 354 | 0.42 | 0.47 | 0.80 | 0.18 | 54 | 1.18 | 0.00 | 5 | 148 | 0 |
| 2025-08 | 297 | 0.37 | 0.55 | 0.79 | 0.19 | 74 | 1.20 | 0.00 | 4 | 164 | 0 |
| 2025-09 | 266 | 0.48 | 0.46 | 0.78 | 0.23 | 50 | 1.21 | 0.00 | 4 | 163 | 0 |
| 2025-10 | 288 | 0.47 | 0.47 | 0.76 | 0.20 | 74 | 1.26 | 0.00 | 5 | 166 | 0 |
| 2025-11 | 293 | 0.46 | 0.46 | 0.81 | 0.29 | 91 | 1.26 | 0.00 | 4 | 152 | 0 |
| 2025-12 | 384 | 0.40 | 0.53 | 0.82 | 0.22 | 77 | 1.20 | 0.00 | 3 | 166 | 0 |
| 2026-01 | 419 | 0.44 | 0.47 | 0.83 | 0.18 | 67 | 1.26 | 0.00 | 3 | 168 | 0 |
| 2026-02 | 336 | 0.54 | 0.38 | 0.76 | 0.28 | 68 | 1.26 | 0.00 | 5 | 161 | 0 |
| 2026-03 | 341 | 0.52 | 0.40 | 0.76 | 0.22 | 85 | 1.25 | 0.01 | 4 | 164 | 0 |
| 2026-04 | 313 | 0.46 | 0.47 | 0.81 | 0.22 | 104 | 1.25 | 0.00 | 4 | 164 | 0 |
| 2026-05 | 234 | 0.69 | 0.25 | 0.84 | 0.40 | 73 | 1.19 | 0.00 | 3 | 168 | 0 |
| 2026-06 | 476 | 0.59 | 0.36 | 0.89 | 0.36 | 80 | 1.20 | 0.00 | 5 | 83 | 0 |
| 2026-07 | 448 | 0.55 | 0.38 | 0.88 | 0.31 | 81 | 1.15 | 0.00 | 4 | 165 | 0 |
| 2026-08 | 445 | 0.48 | 0.42 | 0.86 | 0.13 | 121 | 1.27 | 0.00 | 4 | 156 | 0 |
| 2026-09 | 410 | 0.51 | 0.42 | 0.85 | – | 121 | 1.24 | 0.00 | 4 | 154 | 0 |
| 2026-10 | 341 | 0.63 | 0.30 | 0.87 | – | 102 | 1.18 | 0.00 | 5 | 122 | 0 |

## Contract drift

- 2024-10-08 `d1e15f62` `ruff.schema.json`: version None → None (drift): removed-property at $.tab-size
- 2024-10-08 `9218d6be` `ruff.schema.json`: version None → None (drift): removed-property at $.allowed-unused-imports
- 2025-04-26 `6044f041` `knot.schema.json`: version None → None (drift): removed-property at $.respect-ignore-files
- 2025-05-26 `62ef96f5` `ty.schema.json`: version None → None (drift): removed-property at $.respect-ignore-files

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.3.0_
