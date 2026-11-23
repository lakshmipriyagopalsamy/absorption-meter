# Absorption report: demo team (synthetic)

849 mainline changes, 2024-01 to 2025-03. Rework window 14 days. Deployment frequency uses releases (tags). Pull-request data: no. Team data: yes.

## Decision

🔴 **Hold**: Production is rising while the absorption ratio falls: pause expansion and use the diagnostic matrix to identify the control requiring investment.

Suggested order: protect contracts and verify critical behavior first, and close telemetry gaps that block diagnosis; move simplification earlier when change cost is the dominant constraint. The order is a hypothesis, not a finding.

1. R2 · Contracts first: version the schemas that drifted and fail CI on breaking changes.
1. R4 · Telemetry: make instrumentation part of done; set SLOs and alerts on the new paths.
1. R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.

## Paired metrics

A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.

| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |
|---|---|---|---|---|
| Deployment frequency ↔ Rework rate | up (2.0 → 4.0) | up (0.11 → 0.27) | ⚠️ debt signal | Busier, not faster: more changes, and more of them need rework. |
| Lead time ↔ Decision latency + Change cost | n/a | up (1.2 → 1.8) | ⚠️ debt signal | Each change costs more (more areas or lines per change): look for hidden coupling. Add --github for decision latency. |
| Change failure rate ↔ Contract drift | flat (0.00 → 0.00) | up (0.00 → 0.63) | ⚠️ debt signal | Failure rate looks steady, but 2 contract change(s) in the last 3 months broke compatibility without a version bump: failures may be hiding downstream. |
| Recovery time ↔ Telemetry coverage | n/a | down (0.90 → 0.76) | ⚠️ debt signal | Recovery looks fine, but telemetry coverage is falling and failures take longer to detect. |

## Month by month

| Month | Changes | AR | Rework | Median lines | Areas/change | Reverts | Releases | Recovery h | Drift | Detect h | Telemetry |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-01 | 42 | 0.87 | 0.12 | 21 | 1.19 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-02 | 44 | 0.88 | 0.11 | 24 | 1.09 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-03 | 39 | 0.97 | 0.03 | 22 | 1.21 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-04 | 48 | 0.88 | 0.10 | 20 | 1.23 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-05 | 46 | 0.91 | 0.09 | 21 | 1.11 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-06 | 44 | 0.93 | 0.07 | 25 | 1.21 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-07 | 49 | 0.84 | 0.14 | 23 | 1.12 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-08 | 46 | 0.89 | 0.11 | 22 | 1.22 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-09 | 44 | 0.86 | 0.14 | 21 | 1.27 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-10 | 45 | 0.86 | 0.13 | 23 | 1.29 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-11 | 43 | 0.95 | 0.05 | 21 | 1.21 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2024-12 | 45 | 0.88 | 0.11 | 23 | 1.36 | 0.00 | 2 | – | 0 | 1.50 | 0.90 |
| 2025-01 | 102 | 0.82 | 0.17 | 36 | 1.87 | 0.00 | 4 | – | 0 | 2.30 | 0.83 |
| 2025-02 | 114 | 0.67 | 0.29 | 37 | 1.75 | 0.00 | 4 | – | 1 | 3.10 | 0.76 |
| 2025-03 | 98 | 0.64 | 0.37 | 36 | 1.85 | 0.00 | 4 | – | 1 | 3.90 | 0.69 |

## Contract drift

- 2025-02-13 `00000000` `orders/openapi.yaml`: version 1.4.0 → 1.4.0 (drift): removed-property at GET /orders/{id} 200.status
- 2025-03-13 `00000000` `billing/openapi.yaml`: version 1.4.0 → 1.4.0 (drift): removed-property at GET /billing/{id} 200.status

## Reading this report

AR (absorption ratio) is the size-weighted share of changes not reworked within the window. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each measure is compared with this repository's own trailing baseline. The most recent 14 days are left out of rework because their window hasn't closed.

_absorption-meter 0.1.0_
