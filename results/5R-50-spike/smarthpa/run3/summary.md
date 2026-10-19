# Run report: smarthpa | 5R-50% | run 3

- Started 2026-10-19 13:46:05 - finished 2026-10-19 14:01:35
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 215 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,670.47 |
| CPU Overutilization (%) - lower | 49.13 |
| Overutilization Time (min) - lower | 7.51 |
| CPU Overprovision (m) - lower | 2,965.58 |
| Overprovision Time (min) - higher | 14.99 |
| CPU Underprovision (m) - lower | 0.00 |
| Underprovision Time (min) - lower | 0.00 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 50569 | 38 | 390 | 1800 | 2600 | 56.16 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 633.02 | 13.92 | 3.95 | 156.74 | 7.72 | 0.00 | 0.00 |
| currencyservice | 523.72 | 15.47 | 3.16 | 86.05 | 6.13 | 0.00 | 0.00 |
| cartservice | 285.58 | 3.05 | 1.53 | 345.12 | 7.07 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 398.14 | 6.06 | 0.00 | 0.00 |
| checkoutservice | 137.67 | 1.15 | 0.45 | 361.40 | 14.99 | 0.00 | 0.00 |
| productcatalogservice | 268.84 | 3.47 | 1.36 | 228.37 | 12.15 | 0.00 | 0.00 |
| recommendationservice | 210.70 | 8.38 | 2.73 | 302.33 | 13.81 | 0.00 | 0.00 |
| paymentservice | 140.93 | 3.68 | 1.72 | 355.35 | 14.99 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 212.09 | 7.32 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 240.00 | 8.82 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.99 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
