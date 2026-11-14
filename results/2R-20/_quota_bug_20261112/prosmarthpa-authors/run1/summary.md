# Run report: prosmarthpa-authors | 2R-20% | run 1

- Started 2026-10-24 10:16:31 - finished 2026-10-24 10:32:05
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 425 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,693.27 |
| CPU Overutilization (%) - lower | 397.29 |
| Overutilization Time (min) - lower | 14.76 |
| CPU Overprovision (m) - lower | 308.02 |
| Overprovision Time (min) - higher | 0.21 |
| CPU Underprovision (m) - lower | 4,030.82 |
| Underprovision Time (min) - lower | 14.76 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62289 | 0 | 300 | 1000 | 1400 | 69.31 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 292.71 | 120.41 | 14.51 | 2.82 | 0.47 | 1,612.71 | 14.51 |
| currencyservice | 294.35 | 66.15 | 14.76 | 2.35 | 0.21 | 868.94 | 14.76 |
| cartservice | 394.35 | 25.08 | 12.51 | 9.88 | 0.47 | 242.82 | 12.27 |
| adservice | 394.35 | 0.00 | 0.00 | 204.24 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 197.18 | 21.72 | 12.23 | 6.82 | 0.95 | 92.00 | 12.23 |
| productcatalogservice | 197.41 | 70.10 | 13.76 | 2.59 | 0.28 | 553.65 | 13.76 |
| recommendationservice | 197.18 | 56.43 | 13.58 | 4.24 | 0.91 | 422.59 | 13.58 |
| paymentservice | 197.18 | 35.68 | 13.58 | 2.82 | 0.47 | 216.47 | 13.58 |
| shippingservice | 197.41 | 0.64 | 0.53 | 16.00 | 2.45 | 3.06 | 0.53 |
| emailservice | 194.12 | 1.09 | 0.34 | 44.24 | 5.57 | 18.59 | 2.09 |
| redis-cart | 137.04 | 0.00 | 0.00 | 12.02 | 2.11 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
