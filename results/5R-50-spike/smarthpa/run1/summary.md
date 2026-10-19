# Run report: smarthpa | 5R-50% | run 1

- Started 2026-10-19 12:21:33 - finished 2026-10-19 12:37:03
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 249 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,735.06 |
| CPU Overutilization (%) - lower | 38.32 |
| Overutilization Time (min) - lower | 5.31 |
| CPU Overprovision (m) - lower | 2,552.45 |
| Overprovision Time (min) - higher | 14.97 |
| CPU Underprovision (m) - lower | 0.00 |
| Underprovision Time (min) - lower | 0.00 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 54478 | 1 | 280 | 1200 | 1800 | 60.46 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 591.57 | 11.63 | 3.81 | 340.16 | 8.73 | 0.00 | 0.00 |
| currencyservice | 693.57 | 11.90 | 3.31 | 166.67 | 11.70 | 0.00 | 0.00 |
| cartservice | 286.75 | 2.87 | 1.81 | 347.79 | 8.96 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 244.18 | 3.32 | 0.00 | 0.00 |
| checkoutservice | 133.33 | 1.41 | 1.06 | 202.41 | 10.82 | 0.00 | 0.00 |
| productcatalogservice | 230.92 | 1.54 | 0.70 | 246.18 | 13.23 | 0.00 | 0.00 |
| recommendationservice | 187.95 | 6.55 | 2.69 | 311.65 | 11.78 | 0.00 | 0.00 |
| paymentservice | 130.92 | 1.96 | 0.97 | 202.41 | 11.27 | 0.00 | 0.00 |
| shippingservice | 110.04 | 0.45 | 0.12 | 155.42 | 6.47 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 125.30 | 3.82 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 210.28 | 10.83 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
