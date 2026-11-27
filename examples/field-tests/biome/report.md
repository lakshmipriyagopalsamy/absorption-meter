# Absorption report: https://github.com/biomejs/biome

3684 mainline changes, 2024-07 to 2026-10. Rework window 14 days. Deployment frequency uses merged changes. Pull-request data: no. Team data: no.

## Decision

🔴 **Hold**: Production is rising while the absorption ratio (AR_repo) falls: pause expansion and use the diagnostic matrix to identify the control requiring investment.

**Cautions: AR_repo may overstate absorption**

- Late rework, fixes 15-90 days after merging, is rising (up (0.29 → 0.36)): defects are surfacing after the rework window, so AR_repo may overstate absorption. Consider a longer --rework-window.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R3 · Automated verification: acceptance tests from the spec, property or mutation tests where verification is weakest and rework is highest.
1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | up (149.7 → 270.0) | down (0.27 → 0.18) | ✅ no signal | Verification keeps pace with deployment. Rework, the corroborating outcome, is rising too. |
| Lead time ↔ Decision latency + Change cost | n/a | up (1.9 → 2.2) | ⚠️ debt signal | Each change costs more (more areas or lines per change): look for hidden coupling. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.00 → 0.00) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 102 | 0.45 | 0.50 | 0.40 | 0.24 | 116 | 1.47 | 0.00 | 0 | – | 0 |
| 2024-08 | 103 | 0.33 | 0.61 | 0.49 | 0.17 | 85 | 1.67 | 0.00 | 0 | – | 0 |
| 2024-09 | 185 | 0.38 | 0.57 | 0.42 | 0.11 | 52 | 1.54 | 0.00 | 0 | – | 0 |
| 2024-10 | 121 | 0.28 | 0.65 | 0.42 | 0.07 | 73 | 1.88 | 0.00 | 0 | – | 0 |
| 2024-11 | 82 | 0.46 | 0.54 | 0.45 | 0.20 | 75 | 1.57 | 0.00 | 0 | – | 0 |
| 2024-12 | 20 | 0.49 | 0.50 | 0.33 | 0.20 | 52 | 1.65 | 0.00 | 0 | – | 0 |
| 2025-01 | 26 | 0.74 | 0.19 | 0.30 | 0.23 | 21 | 1.23 | 0.00 | 0 | – | 0 |
| 2025-02 | 60 | 0.37 | 0.50 | 0.46 | 0.30 | 46 | 2.08 | 0.00 | 0 | – | 0 |
| 2025-03 | 129 | 0.45 | 0.48 | 0.48 | 0.37 | 69 | 1.72 | 0.00 | 0 | – | 0 |
| 2025-04 | 134 | 0.37 | 0.52 | 0.37 | 0.36 | 98 | 1.61 | 0.00 | 0 | – | 0 |
| 2025-05 | 157 | 0.37 | 0.59 | 0.38 | 0.31 | 136 | 1.73 | 0.00 | 0 | – | 0 |
| 2025-06 | 167 | 0.26 | 0.71 | 0.45 | 0.17 | 22 | 1.70 | 0.01 | 0 | – | 0 |
| 2025-07 | 132 | 0.45 | 0.51 | 0.36 | 0.30 | 83 | 1.98 | 0.00 | 0 | – | 0 |
| 2025-08 | 102 | 0.37 | 0.54 | 0.36 | 0.16 | 48 | 1.72 | 0.00 | 0 | – | 0 |
| 2025-09 | 75 | 0.77 | 0.20 | 0.42 | 0.52 | 106 | 1.93 | 0.00 | 0 | – | 0 |
| 2025-10 | 67 | 0.49 | 0.40 | 0.48 | 0.28 | 50 | 1.90 | 0.00 | 0 | – | 0 |
| 2025-11 | 134 | 0.47 | 0.46 | 0.32 | 0.25 | 101 | 2.13 | 0.00 | 0 | – | 0 |
| 2025-12 | 102 | 0.48 | 0.42 | 0.26 | 0.25 | 66 | 2.16 | 0.00 | 0 | – | 0 |
| 2026-01 | 78 | 0.54 | 0.40 | 0.27 | 0.29 | 124 | 2.21 | 0.00 | 0 | – | 0 |
| 2026-02 | 105 | 0.51 | 0.44 | 0.36 | 0.29 | 106 | 2.06 | 0.00 | 0 | – | 0 |
| 2026-03 | 181 | 0.50 | 0.47 | 0.28 | 0.34 | 125 | 1.92 | 0.00 | 0 | – | 0 |
| 2026-04 | 191 | 0.40 | 0.55 | 0.27 | 0.31 | 168 | 1.84 | 0.00 | 0 | – | 0 |
| 2026-05 | 145 | 0.34 | 0.61 | 0.19 | 0.24 | 126 | 1.73 | 0.00 | 0 | – | 0 |
| 2026-06 | 124 | 0.52 | 0.40 | 0.33 | 0.37 | 82 | 1.95 | 0.00 | 0 | – | 0 |
| 2026-07 | 152 | 0.46 | 0.47 | 0.19 | 0.35 | 237 | 1.80 | 0.00 | 0 | – | 0 |
| 2026-08 | 183 | 0.35 | 0.57 | 0.20 | 0.37 | 173 | 2.12 | 0.00 | 0 | – | 0 |
| 2026-09 | 252 | 0.35 | 0.56 | 0.18 | – | 182 | 2.06 | 0.00 | 0 | – | 0 |
| 2026-10 | 375 | 0.24 | 0.71 | 0.17 | – | 313 | 2.32 | 0.00 | 0 | – | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.2.1_
