# Run report: smarthpa | 5R-50% | run 5

- Started 2026-10-07 14:17:17 - finished 2026-10-07 14:32:47
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 282 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 4,095.53 |
| CPU Overutilization (%) - lower | 148.09 |
| Overutilization Time (min) - lower | 14.52 |
| CPU Overprovision (m) - lower | 829.86 |
| Overprovision Time (min) - higher | 5.14 |
| CPU Underprovision (m) - lower | 241.49 |
| Underprovision Time (min) - lower | 9.85 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 64848 | 0 | 230 | 880 | 1300 | 72.15 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 1,036.17 | 25.22 | 7.94 | 50.71 | 2.24 | 39.01 | 4.50 |
| currencyservice | 1,265.60 | 22.45 | 6.23 | 27.30 | 0.89 | 18.79 | 2.55 |
| cartservice | 354.61 | 13.23 | 3.48 | 83.69 | 1.36 | 38.30 | 2.70 |
| adservice | 200.00 | 0.00 | 0.00 | 107.80 | 1.83 | 0.00 | 0.00 |
| checkoutservice | 180.50 | 4.42 | 1.19 | 89.01 | 4.23 | 7.80 | 1.02 |
| productcatalogservice | 340.43 | 35.05 | 8.94 | 85.11 | 4.96 | 62.41 | 8.52 |
| recommendationservice | 265.25 | 44.73 | 11.22 | 71.28 | 4.31 | 71.28 | 9.85 |
| paymentservice | 182.98 | 2.99 | 0.76 | 83.33 | 3.99 | 3.90 | 0.50 |
| shippingservice | 100.00 | 0.00 | 0.00 | 79.43 | 3.23 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 83.69 | 3.73 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 68.51 | 4.48 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
