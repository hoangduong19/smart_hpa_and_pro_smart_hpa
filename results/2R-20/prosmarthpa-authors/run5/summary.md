# Run report: prosmarthpa-authors | 2R-20% | run 5

- Started 2026-11-13 04:53:33 - finished 2026-11-13 05:09:04
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 428 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,499.81 |
| CPU Overutilization (%) - lower | 396.64 |
| Overutilization Time (min) - lower | 14.52 |
| CPU Overprovision (m) - lower | 284.44 |
| Overprovision Time (min) - higher | 0.46 |
| CPU Underprovision (m) - lower | 3,779.44 |
| Underprovision Time (min) - lower | 14.52 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 64711 | 89 | 230 | 870 | 1300 | 71.99 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 293.93 | 111.75 | 14.24 | 3.74 | 0.46 | 1,432.94 | 14.24 |
| currencyservice | 293.22 | 81.75 | 14.52 | 3.74 | 0.46 | 1,005.14 | 14.35 |
| cartservice | 393.93 | 25.49 | 12.28 | 9.81 | 0.96 | 264.49 | 12.03 |
| adservice | 393.93 | 0.00 | 0.00 | 206.07 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 44.32 | 13.52 | 2.34 | 0.18 | 164.72 | 13.52 |
| productcatalogservice | 196.96 | 57.06 | 13.78 | 3.27 | 0.74 | 422.66 | 13.78 |
| recommendationservice | 196.96 | 43.50 | 13.32 | 7.24 | 0.92 | 302.57 | 13.32 |
| paymentservice | 196.96 | 32.77 | 13.28 | 4.67 | 0.68 | 186.92 | 13.28 |
| shippingservice | 197.20 | 0.00 | 0.00 | 21.26 | 2.70 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 2.34 | 0.18 | 0.00 | 0.00 |
| redis-cart | 136.73 | 0.00 | 0.00 | 19.95 | 3.13 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
