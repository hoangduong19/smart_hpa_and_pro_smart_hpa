# Run report: smarthpa | 5R-50% | run 4

- Started 2026-10-05 11:59:20 - finished 2026-10-05 12:14:50
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 308 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,891.43 |
| CPU Overutilization (%) - lower | 143.16 |
| Overutilization Time (min) - lower | 13.75 |
| CPU Overprovision (m) - lower | 837.08 |
| Overprovision Time (min) - higher | 5.09 |
| CPU Underprovision (m) - lower | 326.95 |
| Underprovision Time (min) - lower | 9.90 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 63381 | 1 | 280 | 1100 | 1500 | 70.46 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 913.64 | 46.46 | 12.05 | 45.13 | 2.71 | 120.78 | 9.78 |
| currencyservice | 1,182.47 | 47.97 | 12.21 | 22.73 | 0.70 | 124.03 | 9.39 |
| cartservice | 357.14 | 1.17 | 0.50 | 99.35 | 1.96 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 123.38 | 2.17 | 0.00 | 0.00 |
| checkoutservice | 181.17 | 0.33 | 0.15 | 85.39 | 3.97 | 0.00 | 0.00 |
| productcatalogservice | 346.10 | 13.69 | 3.64 | 76.62 | 4.71 | 24.03 | 3.27 |
| recommendationservice | 260.06 | 31.91 | 8.15 | 77.60 | 3.33 | 56.17 | 7.58 |
| paymentservice | 180.84 | 0.63 | 0.25 | 82.47 | 3.47 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.99 | 0.28 | 76.62 | 2.96 | 1.95 | 0.28 |
| emailservice | 100.00 | 0.00 | 0.00 | 80.52 | 3.20 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 67.27 | 4.46 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
