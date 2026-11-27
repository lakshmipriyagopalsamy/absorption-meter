# Absorption report: https://github.com/langchain-ai/langchain

5980 mainline changes, 2024-07 to 2026-10. Rework window 14 days. Deployment frequency uses merged changes. Pull-request data: no. Team data: no.

## Decision

🟢 **Scale cautiously**: The absorption ratio (AR_repo) is steady or rising and no indicator has fired: conditions support cautiously expanding AI-assisted delivery while monitoring the paired indicators. A steady ratio is not proof of safety.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | flat (121.5 → 97.7) | down (0.46 → 0.42) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | flat (1.0 → 1.1) | ✅ no signal | Change cost is steady. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.00 → 0.00) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 547 | 0.46 | 0.49 | 0.58 | 0.25 | 23 | 1.12 | 0.00 | 0 | – | 0 |
| 2024-08 | 489 | 0.58 | 0.37 | 0.64 | 0.27 | 26 | 1.10 | 0.00 | 0 | – | 0 |
| 2024-09 | 319 | 0.56 | 0.38 | 0.61 | 0.27 | 12 | 1.10 | 0.00 | 0 | – | 0 |
| 2024-10 | 252 | 0.60 | 0.34 | 0.57 | 0.24 | 17 | 1.09 | 0.00 | 0 | – | 0 |
| 2024-11 | 250 | 0.60 | 0.33 | 0.64 | 0.24 | 9.00 | 1.18 | 0.00 | 0 | – | 0 |
| 2024-12 | 313 | 0.71 | 0.27 | 0.55 | 0.29 | 16 | 1.14 | 0.00 | 0 | – | 0 |
| 2025-01 | 225 | 0.58 | 0.32 | 0.64 | 0.28 | 7.00 | 1.13 | 0.00 | 0 | – | 0 |
| 2025-02 | 216 | 0.57 | 0.41 | 0.63 | 0.22 | 14 | 1.22 | 0.00 | 0 | – | 0 |
| 2025-03 | 236 | 0.67 | 0.30 | 0.59 | 0.31 | 10 | 1.11 | 0.00 | 0 | – | 0 |
| 2025-04 | 231 | 0.57 | 0.36 | 0.49 | 0.31 | 28 | 1.17 | 0.00 | 0 | – | 0 |
| 2025-05 | 192 | 0.77 | 0.17 | 0.60 | 0.41 | 8.00 | 1.09 | 0.00 | 0 | – | 0 |
| 2025-06 | 164 | 0.61 | 0.38 | 0.61 | 0.36 | 10 | 1.07 | 0.00 | 0 | – | 0 |
| 2025-07 | 282 | 0.37 | 0.56 | 0.44 | 0.27 | 20 | 1.12 | 0.00 | 0 | – | 0 |
| 2025-08 | 161 | 0.62 | 0.35 | 0.51 | 0.29 | 15 | 1.14 | 0.00 | 0 | – | 0 |
| 2025-09 | 238 | 0.53 | 0.43 | 0.39 | 0.21 | 31 | 1.11 | 0.00 | 0 | – | 0 |
| 2025-10 | 342 | 0.25 | 0.63 | 0.40 | 0.18 | 24 | 1.09 | 0.00 | 0 | – | 0 |
| 2025-11 | 138 | 0.51 | 0.40 | 0.46 | 0.39 | 25 | 1.05 | 0.00 | 0 | – | 0 |
| 2025-12 | 194 | 0.35 | 0.55 | 0.56 | 0.32 | 26 | 1.01 | 0.00 | 0 | – | 0 |
| 2026-01 | 169 | 0.51 | 0.46 | 0.54 | 0.23 | 27 | 1.04 | 0.01 | 0 | – | 0 |
| 2026-02 | 151 | 0.51 | 0.44 | 0.49 | 0.35 | 21 | 1.04 | 0.00 | 0 | – | 0 |
| 2026-03 | 145 | 0.61 | 0.31 | 0.49 | 0.35 | 18 | 1.06 | 0.00 | 0 | – | 0 |
| 2026-04 | 124 | 0.58 | 0.39 | 0.49 | 0.36 | 22 | 1.01 | 0.00 | 0 | – | 0 |
| 2026-05 | 90 | 0.72 | 0.19 | 0.44 | 0.34 | 25 | 1.01 | 0.00 | 0 | – | 0 |
| 2026-06 | 144 | 0.42 | 0.47 | 0.41 | 0.22 | 30 | 1.03 | 0.00 | 0 | – | 0 |
| 2026-07 | 75 | 0.67 | 0.24 | 0.45 | 0.31 | 18 | 1.03 | 0.00 | 0 | – | 0 |
| 2026-08 | 144 | 0.59 | 0.38 | 0.29 | 0.33 | 38 | 1.02 | 0.00 | 0 | – | 0 |
| 2026-09 | 86 | 0.58 | 0.35 | 0.46 | – | 28 | 1.09 | 0.00 | 0 | – | 0 |
| 2026-10 | 63 | 0.70 | 0.26 | 0.52 | – | 6.00 | 1.05 | 0.00 | 0 | – | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.2.1_
