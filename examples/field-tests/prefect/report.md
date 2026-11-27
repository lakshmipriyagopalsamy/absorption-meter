# Absorption report: https://github.com/prefecthq/prefect

3091 mainline changes, 2024-07 to 2026-10. Rework window 14 days. Deployment frequency uses releases (tags). Pull-request data: no. Team data: no.

## Decision

🟢 **Scale cautiously**: The absorption ratio (AR_repo) is steady or rising and no indicator has fired: conditions support cautiously expanding AI-assisted delivery while monitoring the paired indicators. A steady ratio is not proof of safety.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | down (4.2 → 3.0) | flat (0.15 → 0.21) | ✅ no signal | Verification keeps pace with deployment. |
| Lead time ↔ Decision latency + Change cost | n/a | flat (1.8 → 1.7) | ✅ no signal | Change cost is steady. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | down (0.42 → 0.11) | flat (0.16 → 0.00) | ✅ no signal | No silent contract changes. |
| Recovery time ↔ Telemetry coverage | n/a | n/a | … not enough data | Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Late rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-07 | 177 | 0.69 | 0.24 | 0.42 | 0.29 | 47 | 1.45 | 0.00 | 0 | – | 0 |
| 2024-08 | 172 | 0.69 | 0.22 | 0.33 | 0.31 | 28 | 1.53 | 0.00 | 0 | – | 0 |
| 2024-09 | 163 | 0.67 | 0.25 | 0.31 | 0.26 | 30 | 1.56 | 0.00 | 4 | 166 | 0 |
| 2024-10 | 162 | 0.58 | 0.30 | 0.36 | 0.21 | 20 | 1.62 | 0.00 | 9 | 16 | 1 |
| 2024-11 | 115 | 0.62 | 0.31 | 0.31 | 0.23 | 66 | 1.55 | 0.00 | 4 | 97 | 1 |
| 2024-12 | 190 | 0.70 | 0.24 | 0.39 | 0.25 | 110 | 1.63 | 0.01 | 6 | 90 | 0 |
| 2025-01 | 227 | 0.79 | 0.18 | 0.42 | 0.41 | 95 | 1.45 | 0.00 | 5 | 166 | 3 |
| 2025-02 | 214 | 0.72 | 0.25 | 0.37 | 0.35 | 73 | 1.45 | 0.00 | 10 | 57 | 0 |
| 2025-03 | 158 | 0.64 | 0.29 | 0.37 | 0.21 | 44 | 1.53 | 0.00 | 7 | 107 | 0 |
| 2025-04 | 138 | 0.81 | 0.15 | 0.32 | 0.20 | 83 | 1.55 | 0.00 | 7 | 91 | 1 |
| 2025-05 | 72 | 0.83 | 0.12 | 0.33 | 0.33 | 54 | 1.71 | 0.00 | 5 | 108 | 0 |
| 2025-06 | 96 | 0.61 | 0.26 | 0.40 | 0.22 | 88 | 1.58 | 0.00 | 3 | 114 | 0 |
| 2025-07 | 98 | 0.83 | 0.14 | 0.20 | 0.34 | 74 | 1.74 | 0.00 | 4 | 118 | 0 |
| 2025-08 | 83 | 0.77 | 0.18 | 0.31 | 0.30 | 49 | 1.76 | 0.00 | 4 | 163 | 0 |
| 2025-09 | 94 | 0.75 | 0.21 | 0.23 | 0.36 | 68 | 1.72 | 0.00 | 5 | 154 | 0 |
| 2025-10 | 96 | 0.82 | 0.16 | 0.24 | 0.29 | 66 | 1.74 | 0.00 | 6 | 146 | 0 |
| 2025-11 | 67 | 0.81 | 0.16 | 0.26 | 0.24 | 64 | 1.57 | 0.00 | 5 | 76 | 0 |
| 2025-12 | 87 | 0.87 | 0.11 | 0.29 | 0.33 | 43 | 1.54 | 0.00 | 5 | 156 | 0 |
| 2026-01 | 100 | 0.85 | 0.16 | 0.14 | 0.29 | 81 | 1.80 | 0.00 | 6 | 139 | 0 |
| 2026-02 | 106 | 0.58 | 0.32 | 0.26 | 0.14 | 208 | 1.93 | 0.00 | 5 | 133 | 0 |
| 2026-03 | 103 | 0.87 | 0.11 | 0.15 | 0.30 | 120 | 1.72 | 0.00 | 4 | 168 | 1 |
| 2026-04 | 35 | 0.82 | 0.14 | 0.08 | 0.29 | 80 | 1.77 | 0.00 | 4 | 166 | 0 |
| 2026-05 | 80 | 0.84 | 0.12 | 0.12 | 0.25 | 182 | 1.88 | 0.00 | 4 | 166 | 0 |
| 2026-06 | 47 | 0.78 | 0.19 | 0.22 | 0.15 | 100 | 1.77 | 0.00 | 4 | 131 | 0 |
| 2026-07 | 34 | 0.95 | 0.03 | 0.05 | 0.32 | 58 | 1.53 | 0.00 | 4 | 168 | 0 |
| 2026-08 | 46 | 0.86 | 0.09 | 0.27 | – | 44 | 1.54 | 0.00 | 3 | 142 | 0 |
| 2026-09 | 38 | 0.98 | 0.03 | 0.29 | – | 33 | 1.63 | 0.00 | 3 | – | 0 |
| 2026-10 | 93 | 0.78 | 0.25 | 0.09 | – | 70 | 2.02 | 0.00 | 3 | – | 0 |

## Contract drift

- 2024-10-31 `525d8422` `schemas/settings.schema.json`: version https://github.com/PrefectHQ/prefect/schemas/settings.schema.json → https://github.com/PrefectHQ/prefect/schemas/settings.schema.json (drift): removed-property at $.async_fetch_state_result; removed-property at $.experimental_warn
- 2024-11-15 `8dd8f3c4` `schemas/settings.schema.json`: version https://github.com/PrefectHQ/prefect/schemas/settings.schema.json → https://github.com/PrefectHQ/prefect/schemas/settings.schema.json (drift): removed-property at $.experiments.worker_logging_to_api_enabled
- 2025-01-06 `e32921df` `schemas/settings.schema.json`: version https://github.com/PrefectHQ/prefect/schemas/settings.schema.json → https://github.com/PrefectHQ/prefect/schemas/settings.schema.json (drift): removed-property at $.experiments.telemetry_enabled
- 2025-01-17 `ea877227` `schemas/settings.schema.json`: version https://github.com/PrefectHQ/prefect/schemas/settings.schema.json → https://github.com/PrefectHQ/prefect/schemas/settings.schema.json (drift): removed-property at $.server.database.sqlalchemy_max_overflow; removed-property at $.server.database.sqlalchemy_pool_size
- 2025-01-17 `adf10331` `schemas/settings.schema.json`: version https://github.com/PrefectHQ/prefect/schemas/settings.schema.json → https://github.com/PrefectHQ/prefect/schemas/settings.schema.json (drift): removed-property at $.server.database.connection_app_name
- 2025-04-30 `a82ec550` `schemas/settings.schema.json`: version https://github.com/PrefectHQ/prefect/schemas/settings.schema.json → https://github.com/PrefectHQ/prefect/schemas/settings.schema.json (drift): removed-property at $.server.services.flow_run_notifications
- 2026-03-10 `ce087d52` `schemas/settings.schema.json`: version https://github.com/PrefectHQ/prefect/schemas/settings.schema.json → https://github.com/PrefectHQ/prefect/schemas/settings.schema.json (drift): removed-property at $.server.services.event_persister.batch_size_delete

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced later. Late rework (fixes 15-90 days after merging, shown once that window has closed), examined absorption and unreviewed share (with --github), and escaped defects (team data) help tell the two apart; when they point the other way, the report lists cautions.

_absorption-meter 0.2.1_
