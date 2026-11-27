# Absorption report: https://github.com/python-poetry/poetry

568 mainline changes, 2024-07 to 2026-10. Rework window 14 days (strict rule). Deployment frequency uses releases (tags). Pull-request data: no. Team data: no.

## Decision

🟢 **Scale cautiously**: The absorption ratio (AR_repo) is steady or rising and no indicator has fired: conditions support cautiously expanding AI-assisted delivery while monitoring the paired indicators. A steady ratio is not proof of safety.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | flat (0.50 → 0.67) | down (0.27 → 0.16) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | flat (1.5 → 1.6) | ✅ no signal | Change cost is steady. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | n/a | flat (0.00 → 0.00) | … not enough data | Needs 9 months of history. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 9 | 0.71 | 0.22 | 0.00 | 0.44 | 73 | 2.44 | 0.00 | 0 | – | 0 |
| 2024-08 | 10 | 1.00 | 0.00 | 0.33 | 0.10 | 30 | 1.60 | 0.00 | 0 | – | 0 |
| 2024-09 | 23 | 0.71 | 0.26 | 0.27 | 0.26 | 39 | 1.65 | 0.00 | 0 | – | 0 |
| 2024-10 | 32 | 0.95 | 0.03 | 0.25 | 0.53 | 27 | 1.97 | 0.00 | 0 | – | 0 |
| 2024-11 | 38 | 0.85 | 0.13 | 0.15 | 0.50 | 66 | 1.58 | 0.00 | 0 | – | 0 |
| 2024-12 | 12 | 1.00 | 0.00 | 0.14 | 0.42 | 46 | 1.67 | 0.00 | 0 | – | 0 |
| 2025-01 | 101 | 0.61 | 0.33 | 0.26 | 0.10 | 32 | 1.56 | 0.00 | 2 | 156 | 0 |
| 2025-02 | 25 | 0.69 | 0.24 | 0.19 | 0.04 | 43 | 1.88 | 0.00 | 2 | 31 | 0 |
| 2025-03 | 17 | 0.97 | 0.06 | 0.57 | 0.18 | 15 | 1.29 | 0.00 | 1 | – | 0 |
| 2025-04 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 51 | 1.50 | 0.00 | 0 | – | 0 |
| 2025-05 | 13 | 1.00 | 0.00 | 0.17 | 0.08 | 16 | 1.46 | 0.00 | 1 | – | 0 |
| 2025-06 | 5 | 1.00 | 0.00 | 0.00 | 0.20 | 11 | 1.20 | 0.00 | 0 | – | 0 |
| 2025-07 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 24 | 1.67 | 0.00 | 0 | – | 0 |
| 2025-08 | 19 | 1.00 | 0.00 | 0.20 | 0.16 | 26 | 1.90 | 0.00 | 0 | – | 0 |
| 2025-09 | 15 | 1.00 | 0.00 | 0.33 | 0.07 | 22 | 1.33 | 0.00 | 2 | – | 0 |
| 2025-10 | 5 | 1.00 | 0.00 | 0.33 | 0.20 | 8.00 | 1.40 | 0.00 | 0 | – | 0 |
| 2025-11 | 18 | 0.94 | 0.06 | 0.08 | 0.22 | 92 | 2 | 0.00 | 0 | – | 0 |
| 2025-12 | 22 | 0.75 | 0.23 | 0.11 | 0.32 | 56 | 1.96 | 0.00 | 0 | – | 0 |
| 2026-01 | 14 | 1.00 | 0.00 | 0.14 | 0.43 | 16 | 1.50 | 0.00 | 2 | 49 | 0 |
| 2026-02 | 11 | 0.90 | 0.09 | 0.20 | 0.36 | 18 | 1.36 | 0.00 | 1 | – | 0 |
| 2026-03 | 27 | 0.84 | 0.15 | 0.25 | 0.26 | 38 | 1.59 | 0.00 | 0 | – | 0 |
| 2026-04 | 21 | 0.89 | 0.10 | 0.21 | 0.24 | 49 | 1.76 | 0.00 | 0 | – | 0 |
| 2026-05 | 38 | 0.86 | 0.08 | 0.20 | 0.00 | 19 | 1.37 | 0.00 | 2 | 144 | 0 |
| 2026-06 | 17 | 0.87 | 0.12 | 0.25 | 0.29 | 38 | 1.65 | 0.00 | 0 | – | 0 |
| 2026-07 | 4 | 1.00 | 0.00 | 0.50 | 0.25 | 34 | 1.50 | 0.00 | 0 | – | 0 |
| 2026-08 | 15 | 0.86 | 0.13 | 0.11 | 0.57 | 59 | 1.53 | 0.00 | 0 | – | 0 |
| 2026-09 | 38 | 0.88 | 0.08 | 0.22 | – | 28 | 1.47 | 0.00 | 2 | 13 | 0 |
| 2026-10 | 12 | 1.00 | 0.00 | 0.14 | – | 17 | 1.83 | 0.00 | 0 | – | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.3.0_
