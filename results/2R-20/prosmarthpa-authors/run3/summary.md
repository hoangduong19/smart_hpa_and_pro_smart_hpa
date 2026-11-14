# Run report: prosmarthpa-authors | 2R-20% | run 3

- Started 2026-11-13 04:11:11 - finished 2026-11-13 04:26:41
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 430 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,501.51 |
| CPU Overutilization (%) - lower | 373.62 |
| Overutilization Time (min) - lower | 14.39 |
| CPU Overprovision (m) - lower | 273.72 |
| Overprovision Time (min) - higher | 0.58 |
| CPU Underprovision (m) - lower | 3,480.23 |
| Underprovision Time (min) - lower | 14.39 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62861 | 0 | 300 | 970 | 1300 | 69.95 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 293.95 | 109.65 | 13.89 | 3.72 | 0.58 | 1,409.07 | 13.89 |
| currencyservice | 293.95 | 65.50 | 14.39 | 3.72 | 0.58 | 768.60 | 14.39 |
| cartservice | 393.95 | 24.68 | 11.90 | 10.70 | 0.58 | 242.79 | 11.90 |
| adservice | 393.95 | 0.33 | 0.50 | 203.26 | 14.47 | 4.19 | 0.50 |
| checkoutservice | 100.00 | 43.32 | 13.14 | 2.33 | 0.18 | 162.33 | 13.14 |
| productcatalogservice | 197.21 | 54.25 | 13.39 | 2.79 | 0.24 | 405.81 | 13.39 |
| recommendationservice | 196.98 | 42.85 | 12.90 | 3.72 | 1.08 | 298.60 | 12.90 |
| paymentservice | 196.98 | 33.04 | 13.64 | 3.02 | 0.58 | 188.84 | 13.64 |
| shippingservice | 196.98 | 0.00 | 0.00 | 20.23 | 2.82 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 2.33 | 0.18 | 0.00 | 0.00 |
| redis-cart | 137.56 | 0.00 | 0.00 | 17.91 | 3.16 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
