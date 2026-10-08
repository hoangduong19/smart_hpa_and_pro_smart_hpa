# Run report: smarthpa | 2R-20% | run 3

- Started 2026-10-05 10:49:08 - finished 2026-10-05 11:04:39
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 336 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,449.40 |
| CPU Overutilization (%) - lower | 674.84 |
| Overutilization Time (min) - lower | 14.87 |
| CPU Overprovision (m) - lower | 70.83 |
| Overprovision Time (min) - higher | 0.59 |
| CPU Underprovision (m) - lower | 5,118.75 |
| Underprovision Time (min) - lower | 14.41 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 63032 | 0 | 300 | 1000 | 1400 | 70.08 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 289.29 | 130.38 | 14.59 | 3.57 | 0.41 | 1,710.42 | 14.35 |
| currencyservice | 1,047.62 | 37.19 | 14.87 | 1.19 | 0.13 | 905.95 | 14.41 |
| cartservice | 200.00 | 61.81 | 14.13 | 8.93 | 0.36 | 514.88 | 14.13 |
| adservice | 200.00 | 3.80 | 2.85 | 6.55 | 0.36 | 13.10 | 1.01 |
| checkoutservice | 100.00 | 69.08 | 14.13 | 5.06 | 0.59 | 302.08 | 14.13 |
| productcatalogservice | 100.00 | 151.93 | 14.13 | 3.27 | 0.36 | 707.44 | 14.13 |
| recommendationservice | 100.00 | 119.78 | 14.13 | 3.27 | 0.36 | 553.27 | 14.13 |
| paymentservice | 100.00 | 61.73 | 14.13 | 3.57 | 0.41 | 260.42 | 14.13 |
| shippingservice | 100.00 | 32.24 | 12.85 | 3.27 | 0.36 | 120.24 | 12.85 |
| emailservice | 100.00 | 6.78 | 4.87 | 5.06 | 0.59 | 30.95 | 4.87 |
| redis-cart | 112.50 | 0.13 | 0.10 | 27.08 | 5.12 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
