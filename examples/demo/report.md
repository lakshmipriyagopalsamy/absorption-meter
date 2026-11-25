# Absorption report: demo team (synthetic)

841 mainline changes, 2024-01 to 2025-03. Rework window 14 days. Deployment frequency uses releases (tags). Pull-request data: no. Team data: yes.

## Decision

🔴 **Hold**: Production is rising while the absorption ratio (AR_repo) falls: pause expansion and use the diagnostic matrix to identify the control requiring investment.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R2 · Contracts first: version the schemas that drifted and fail CI on breaking changes.
1. R4 · Telemetry: make instrumentation part of done; set SLOs and alerts on the new paths.
1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Verification effectiveness | up (2.0 → 4.0) | up (0.30 → 0.61) | ⚠️ debt signal | Busier, not faster: deployments are rising while verification weakens. Rework, the corroborating outcome, is rising too. |
| Lead time ↔ Decision latency + Change cost | n/a | up (1.9 → 2.3) | ⚠️ debt signal | Each change costs more (more areas or lines per change): look for hidden coupling. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.00 → 0.00) | up (0.00 → 0.64) | ⚠️ debt signal | Failure rate looks steady, but 2 contract change(s) in the last 3 months broke compatibility without a version bump: failures may be hiding downstream. |
| Recovery time ↔ Telemetry coverage | n/a | down (0.90 → 0.76) | ⚠️ debt signal | Recovery looks fine, but telemetry coverage is falling and failures take longer to detect. |

## Month by month

| Month | Changes | AR_repo | Rework | Untested | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift | Detect h | Telemetry |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-01 | 40 | 0.95 | 0.05 | 0.33 | 32 | 1.93 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-02 | 45 | 0.86 | 0.13 | 0.29 | 32 | 2 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-03 | 46 | 0.89 | 0.11 | 0.26 | 21 | 1.96 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-04 | 48 | 0.80 | 0.19 | 0.35 | 27 | 1.77 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-05 | 42 | 0.95 | 0.05 | 0.26 | 35 | 1.88 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-06 | 47 | 0.92 | 0.09 | 0.30 | 26 | 1.87 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-07 | 45 | 0.93 | 0.07 | 0.18 | 29 | 2.07 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-08 | 44 | 0.88 | 0.11 | 0.30 | 30 | 2 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-09 | 48 | 0.89 | 0.10 | 0.29 | 26 | 1.92 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-10 | 43 | 0.92 | 0.07 | 0.35 | 25 | 1.93 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-11 | 43 | 0.88 | 0.12 | 0.44 | 20 | 1.77 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-12 | 41 | 0.91 | 0.07 | 0.27 | 26 | 1.98 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2025-01 | 101 | 0.80 | 0.19 | 0.44 | 39 | 2.58 | 0.00 | 4 | – | 0 | 2.30 | 0.83 |
| 2025-02 | 100 | 0.74 | 0.23 | 0.67 | 41 | 2.22 | 0.00 | 4 | – | 1 | 3.10 | 0.76 |
| 2025-03 | 108 | 0.67 | 0.32 | 0.72 | 36 | 2.01 | 0.00 | 4 | – | 1 | 3.90 | 0.69 |

## Contract drift

- 2025-02-13 `00000000` `orders/openapi.yaml`: version 1.4.0 → 1.4.0 (drift): removed-property at GET /orders/{id} 200.status
- 2025-03-13 `00000000` `billing/openapi.yaml`: version 1.4.0 → 1.4.0 (drift): removed-property at GET /billing/{id} 200.status

## Reading this report

AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not reworked within the window. The full model's AR also requires a first-run CI pass, which version control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

_absorption-meter 0.1.1_
