# Absorption report: https://github.com/excalidraw/excalidraw

668 mainline changes, 2024-07 to 2026-10. Rework window 14 days (strict rule). Deployment frequency uses merged changes. Pull-request data: no. Team data: no.

## Decision

🟡 **Address**: Absorption is holding, but an indicator has moved: fix it before scaling further.

**Cautions: AR_repo may overstate absorption**

- Late rework, fixes 15-90 days after merging, is rising (up (0.23 → 0.41)): defects are surfacing after the rework window, so AR_repo may overstate absorption. Consider a longer --rework-window.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R3 · Automated verification: acceptance tests from the spec, property or mutation tests where verification is weakest and rework is highest.
1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | flat (21.7 → 30.3) | down (0.48 → 0.26) | ✅ no signal | Verification keeps pace with deployment. Rework, the corroborating outcome, is rising too. |
| Lead time ↔ Decision latency + Change cost | n/a | up (92.8 → 285.2) | ⚠️ debt signal | Each change costs more (more areas or lines per change): look for hidden coupling. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.00 → 0.00) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 21 | 0.50 | 0.38 | 0.84 | 0.14 | 22 | 1.57 | 0.00 | 0 | – | 0 |
| 2024-08 | 45 | 0.54 | 0.36 | 0.72 | 0.20 | 42 | 1.40 | 0.00 | 0 | – | 0 |
| 2024-09 | 30 | 0.64 | 0.23 | 0.67 | 0.27 | 26 | 1.43 | 0.00 | 0 | – | 0 |
| 2024-10 | 17 | 0.44 | 0.41 | 0.50 | 0.24 | 100 | 1.59 | 0.00 | 0 | – | 0 |
| 2024-11 | 21 | 0.79 | 0.10 | 0.86 | 0.14 | 11 | 1.43 | 0.00 | 0 | – | 0 |
| 2024-12 | 11 | 0.84 | 0.18 | 0.70 | 0.27 | 23 | 1 | 0.00 | 0 | – | 0 |
| 2025-01 | 36 | 0.66 | 0.31 | 0.75 | 0.22 | 44 | 1.06 | 0.00 | 0 | – | 0 |
| 2025-02 | 18 | 0.64 | 0.28 | 0.72 | 0.44 | 140 | 1.72 | 0.00 | 0 | – | 0 |
| 2025-03 | 28 | 0.57 | 0.29 | 0.73 | 0.11 | 34 | 1.46 | 0.00 | 1 | – | 0 |
| 2025-04 | 23 | 0.43 | 0.39 | 0.57 | 0.26 | 69 | 1.30 | 0.00 | 0 | – | 0 |
| 2025-05 | 39 | 0.41 | 0.41 | 0.71 | 0.23 | 25 | 1.13 | 0.00 | 0 | – | 0 |
| 2025-06 | 24 | 0.39 | 0.58 | 0.48 | 0.12 | 245 | 1.38 | 0.00 | 0 | – | 0 |
| 2025-07 | 14 | 0.80 | 0.14 | 0.54 | 0.14 | 40 | 1.07 | 0.00 | 0 | – | 0 |
| 2025-08 | 16 | 0.34 | 0.50 | 0.60 | 0.12 | 72 | 1.19 | 0.00 | 0 | – | 0 |
| 2025-09 | 23 | 0.39 | 0.48 | 0.78 | 0.22 | 30 | 1.13 | 0.00 | 0 | – | 0 |
| 2025-10 | 12 | 0.52 | 0.33 | 0.91 | 0.33 | 31 | 1 | 0.00 | 0 | – | 0 |
| 2025-11 | 17 | 0.58 | 0.29 | 0.88 | 0.24 | 37 | 1.47 | 0.00 | 0 | – | 0 |
| 2025-12 | 14 | 0.61 | 0.29 | 0.64 | 0.29 | 52 | 1.21 | 0.00 | 0 | – | 0 |
| 2026-01 | 38 | 0.62 | 0.32 | 0.71 | 0.26 | 53 | 1.29 | 0.00 | 0 | – | 0 |
| 2026-02 | 24 | 0.49 | 0.46 | 0.67 | 0.12 | 28 | 1.12 | 0.00 | 0 | – | 0 |
| 2026-03 | 27 | 0.52 | 0.33 | 0.54 | 0.19 | 54 | 1.30 | 0.00 | 0 | – | 0 |
| 2026-04 | 7 | 0.65 | 0.29 | 0.67 | 0.29 | 63 | 1.29 | 0.00 | 0 | – | 0 |
| 2026-05 | 15 | 0.87 | 0.13 | 0.36 | 0.53 | 86 | 1.33 | 0.00 | 0 | – | 0 |
| 2026-06 | 19 | 0.57 | 0.37 | 0.29 | 0.37 | 109 | 1.21 | 0.00 | 0 | – | 0 |
| 2026-07 | 38 | 0.55 | 0.37 | 0.34 | 0.32 | 217 | 1.26 | 0.00 | 0 | – | 0 |
| 2026-08 | 23 | 0.58 | 0.39 | 0.38 | – | 145 | 1.22 | 0.00 | 0 | – | 0 |
| 2026-09 | 38 | 0.38 | 0.53 | 0.23 | – | 358 | 1.10 | 0.00 | 0 | – | 0 |
| 2026-10 | 30 | 0.13 | 0.83 | 0.17 | – | 352 | 1.33 | 0.00 | 0 | – | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.3.0_
