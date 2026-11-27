# Absorption report: small team (synthetic): absorbed or unexamined?

571 mainline changes, 2024-01 to 2025-03. Rework window 14 days. Deployment frequency uses merged changes. Pull-request data: yes. Team data: yes.

## Decision

🟡 **Address**: Absorption is holding, but an indicator has moved: fix it before scaling further.

**Cautions: AR_repo may overstate absorption**

- Examined absorption is falling (down (0.82 → 0.47)) while AR_repo holds: more of the absorbed change was merged without review, so low rework may mean unexamined rather than absorbed.
- The share of pull requests merged without review is rising (up (0.05 → 0.45)).
- Late rework, fixes 15-90 days after merging, is rising (up (0.04 → 0.09)): defects are surfacing after the rework window, so AR_repo may overstate absorption. Consider a longer --rework-window.
- Escaped defects per 100 changes are rising (up (3.1 → 9.7)).
- Defects are reaching users sooner after release (down (30.0 → 16.0) days).

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R3 · Automated verification: acceptance tests from the spec, property or mutation tests where verification is weakest and rework is highest.
1. R6 · Governance: cap PR size and require a decision record for high-risk changes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | up (32.0 → 61.3) | flat (0.07 → 0.09) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | flat (15.4 → 16.6) | flat (3.5 → 3.6) | ✅ no signal | Decisions and change cost keep pace. |
| Change failure rate ↔ Contract drift | flat (0.00 → 0.00) | flat (0.00 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift | Lead h | 1st review h | Comments/100 lines | Unreviewed | Examined AR | Escaped defects | Days to 1st defect |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-01 | 35 | 0.88 | 0.11 | 0.11 | 0.00 | 31 | 1.89 | 0.00 | 0 | – | 0 | 20 | 3.48 | 12 | 0.06 | – | 1 | 30 |
| 2024-02 | 32 | 0.84 | 0.16 | 0.09 | 0.03 | 25 | 1.91 | 0.00 | 0 | – | 0 | 19 | 3.45 | 12 | 0.03 | 0.76 | 1 | 30 |
| 2024-03 | 33 | 0.91 | 0.09 | 0.06 | 0.06 | 29 | 1.94 | 0.00 | 0 | – | 0 | 16 | 3.40 | 9.67 | 0.03 | 0.85 | 1 | 30 |
| 2024-04 | 30 | 0.90 | 0.10 | 0.07 | 0.00 | 32 | 1.93 | 0.00 | 0 | – | 0 | 12 | 3.98 | 10 | 0.00 | 0.86 | 1 | 30 |
| 2024-05 | 31 | 0.97 | 0.03 | 0.03 | 0.03 | 25 | 1.97 | 0.00 | 0 | – | 0 | 12 | 3.49 | 13 | 0.10 | 0.85 | 1 | 30 |
| 2024-06 | 34 | 0.90 | 0.09 | 0.09 | 0.00 | 28 | 1.91 | 0.00 | 0 | – | 0 | 12 | 3.81 | 9.73 | 0.06 | 0.82 | 1 | 30 |
| 2024-07 | 31 | 0.83 | 0.16 | 0.10 | 0.10 | 30 | 1.90 | 0.00 | 0 | – | 0 | 16 | 3.80 | 8.81 | 0.07 | 0.70 | 1 | 30 |
| 2024-08 | 33 | 0.97 | 0.03 | 0.03 | 0.03 | 35 | 1.97 | 0.00 | 0 | – | 0 | 14 | 4.18 | 8.90 | 0.09 | 0.86 | 1 | 30 |
| 2024-09 | 32 | 0.90 | 0.09 | 0.09 | 0.06 | 30 | 1.91 | 0.00 | 0 | – | 0 | 14 | 3.09 | 11 | 0.00 | 0.85 | 1 | 30 |
| 2024-10 | 35 | 0.89 | 0.11 | 0.09 | 0.03 | 24 | 1.91 | 0.00 | 0 | – | 0 | 14 | 3.68 | 10 | 0.00 | 0.85 | 1 | 30 |
| 2024-11 | 29 | 0.96 | 0.03 | 0.03 | 0.03 | 29 | 1.97 | 0.00 | 0 | – | 0 | 18 | 3.51 | 13 | 0.07 | 0.86 | 1 | 30 |
| 2024-12 | 32 | 0.91 | 0.09 | 0.09 | 0.16 | 28 | 1.91 | 0.00 | 0 | – | 0 | 16 | 2.69 | 12 | 0.03 | 0.82 | 1 | 30 |
| 2025-01 | 61 | 0.83 | 0.15 | 0.11 | 0.08 | 26 | 1.89 | 0.00 | 0 | – | 0 | 19 | 3.85 | 9.75 | 0.22 | 0.59 | 4 | 23 |
| 2025-02 | 59 | 0.91 | 0.08 | 0.07 | – | 28 | 1.93 | 0.00 | 0 | – | 0 | 14 | 3.18 | 7.80 | 0.40 | 0.58 | 6 | 16 |
| 2025-03 | 64 | 0.89 | 0.11 | 0.09 | – | 28 | 1.91 | 0.00 | 0 | – | 0 | 17 | 3.75 | 4.22 | 0.72 | 0.23 | 8 | 9.00 |

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.2.1_
