# Absorption report: https://github.com/zed-industries/zed

19657 mainline changes, 2024-07 to 2026-10. Rework window 14 days. Deployment frequency uses merged changes. Pull-request data: no. Team data: no.

## Decision

🟡 **Address**: Absorption is holding, but an indicator has moved: fix it before scaling further.

**Cautions: AR_repo may overstate absorption**

- Late rework, fixes 15-90 days after merging, is rising (up (0.21 → 0.33)): defects are surfacing after the rework window, so AR_repo may overstate absorption. Consider a longer --rework-window.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | down (772.7 → 420.3) | down (0.90 → 0.87) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | up (74.6 → 129.3) | ✅ no signal | Change cost is steady. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.00 → 0.00) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 740 | 0.40 | 0.52 | 0.92 | 0.35 | 23 | 1.18 | 0.00 | 0 | – | 0 |
| 2024-08 | 616 | 0.28 | 0.62 | 0.93 | 0.20 | 30 | 1.14 | 0.01 | 0 | – | 0 |
| 2024-09 | 514 | 0.30 | 0.60 | 0.90 | 0.18 | 23 | 1.19 | 0.00 | 0 | – | 0 |
| 2024-10 | 542 | 0.28 | 0.60 | 0.91 | 0.15 | 25 | 1.16 | 0.01 | 0 | – | 0 |
| 2024-11 | 516 | 0.45 | 0.48 | 0.92 | 0.30 | 32 | 1.20 | 0.01 | 0 | – | 0 |
| 2024-12 | 449 | 0.44 | 0.48 | 0.97 | 0.36 | 31 | 1.19 | 0.01 | 0 | – | 0 |
| 2025-01 | 672 | 0.31 | 0.61 | 0.94 | 0.27 | 31 | 1.17 | 0.01 | 0 | – | 0 |
| 2025-02 | 773 | 0.24 | 0.68 | 0.94 | 0.15 | 29 | 1.21 | 0.01 | 0 | – | 0 |
| 2025-03 | 877 | 0.32 | 0.60 | 0.93 | 0.20 | 36 | 1.16 | 0.01 | 0 | – | 0 |
| 2025-04 | 924 | 0.30 | 0.62 | 0.93 | 0.22 | 46 | 1.16 | 0.01 | 0 | – | 0 |
| 2025-05 | 911 | 0.31 | 0.61 | 0.93 | 0.24 | 41 | 1.15 | 0.01 | 0 | – | 0 |
| 2025-06 | 772 | 0.33 | 0.58 | 0.92 | 0.28 | 40 | 1.15 | 0.01 | 0 | – | 0 |
| 2025-07 | 698 | 0.37 | 0.56 | 0.93 | 0.32 | 40 | 1.18 | 0.00 | 0 | – | 0 |
| 2025-08 | 802 | 0.16 | 0.76 | 0.90 | 0.13 | 55 | 1.17 | 0.01 | 0 | – | 0 |
| 2025-09 | 765 | 0.37 | 0.55 | 0.95 | 0.28 | 34 | 1.21 | 0.01 | 0 | – | 0 |
| 2025-10 | 879 | 0.24 | 0.68 | 0.95 | 0.19 | 38 | 1.20 | 0.01 | 0 | – | 0 |
| 2025-11 | 764 | 0.38 | 0.54 | 0.95 | 0.27 | 40 | 1.16 | 0.00 | 0 | – | 0 |
| 2025-12 | 738 | 0.35 | 0.57 | 0.95 | 0.27 | 42 | 1.18 | 0.01 | 0 | – | 0 |
| 2026-01 | 808 | 0.25 | 0.67 | 0.90 | 0.18 | 59 | 1.18 | 0.01 | 0 | – | 0 |
| 2026-02 | 935 | 0.28 | 0.64 | 0.92 | 0.18 | 59 | 1.19 | 0.01 | 0 | – | 0 |
| 2026-03 | 933 | 0.26 | 0.68 | 0.91 | 0.18 | 66 | 1.17 | 0.00 | 0 | – | 0 |
| 2026-04 | 865 | 0.23 | 0.73 | 0.92 | 0.14 | 77 | 1.19 | 0.00 | 0 | – | 0 |
| 2026-05 | 644 | 0.44 | 0.49 | 0.89 | 0.30 | 80 | 1.15 | 0.00 | 0 | – | 0 |
| 2026-06 | 628 | 0.40 | 0.53 | 0.89 | 0.26 | 80 | 1.18 | 0.00 | 0 | – | 0 |
| 2026-07 | 631 | 0.36 | 0.58 | 0.89 | 0.23 | 86 | 1.17 | 0.00 | 0 | – | 0 |
| 2026-08 | 392 | 0.52 | 0.42 | 0.87 | 0.50 | 104 | 1.22 | 0.00 | 0 | – | 0 |
| 2026-09 | 420 | 0.41 | 0.51 | 0.87 | – | 122 | 1.35 | 0.00 | 0 | – | 0 |
| 2026-10 | 449 | 0.45 | 0.49 | 0.87 | – | 161 | 1.22 | 0.00 | 0 | – | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.2.1_
