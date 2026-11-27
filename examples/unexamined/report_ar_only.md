# Absorption report: small team (synthetic): absorbed or unexamined?

571 mainline changes, 2024-01 to 2025-03. Rework window 14 days (strict rule). Deployment frequency uses merged changes. Pull-request data: no. Team data: no.

## Decision

🟢 **Scale cautiously**: The absorption ratio (AR_repo) is steady or rising and no indicator has fired: conditions support cautiously expanding AI-assisted delivery while monitoring the paired indicators. A steady ratio is not proof of safety.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | up (32.0 → 61.3) | flat (0.07 → 0.09) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | flat (1.9 → 1.9) | ✅ no signal | Change cost is steady. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.00 → 0.00) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-01 | 35 | 0.88 | 0.11 | 0.11 | – | 31 | 1.89 | 0.00 | 0 | – | 0 |
| 2024-02 | 32 | 0.84 | 0.16 | 0.09 | – | 25 | 1.91 | 0.00 | 0 | – | 0 |
| 2024-03 | 33 | 0.91 | 0.09 | 0.06 | – | 29 | 1.94 | 0.00 | 0 | – | 0 |
| 2024-04 | 30 | 0.90 | 0.10 | 0.07 | – | 32 | 1.93 | 0.00 | 0 | – | 0 |
| 2024-05 | 31 | 0.97 | 0.03 | 0.03 | – | 25 | 1.97 | 0.00 | 0 | – | 0 |
| 2024-06 | 34 | 0.90 | 0.09 | 0.09 | – | 28 | 1.91 | 0.00 | 0 | – | 0 |
| 2024-07 | 31 | 0.83 | 0.16 | 0.10 | – | 30 | 1.90 | 0.00 | 0 | – | 0 |
| 2024-08 | 33 | 0.97 | 0.03 | 0.03 | – | 35 | 1.97 | 0.00 | 0 | – | 0 |
| 2024-09 | 32 | 0.90 | 0.09 | 0.09 | – | 30 | 1.91 | 0.00 | 0 | – | 0 |
| 2024-10 | 35 | 0.89 | 0.11 | 0.09 | – | 24 | 1.91 | 0.00 | 0 | – | 0 |
| 2024-11 | 29 | 0.96 | 0.03 | 0.03 | – | 29 | 1.97 | 0.00 | 0 | – | 0 |
| 2024-12 | 32 | 0.91 | 0.09 | 0.09 | – | 28 | 1.91 | 0.00 | 0 | – | 0 |
| 2025-01 | 61 | 0.83 | 0.15 | 0.11 | – | 26 | 1.89 | 0.00 | 0 | – | 0 |
| 2025-02 | 59 | 0.91 | 0.08 | 0.07 | – | 28 | 1.93 | 0.00 | 0 | – | 0 |
| 2025-03 | 64 | 0.89 | 0.11 | 0.09 | – | 28 | 1.91 | 0.00 | 0 | – | 0 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-14 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.3.0_
