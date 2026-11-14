# Run report: prosmarthpa-cv | 2R-20% | run 5

- Started 2026-11-12 21:49:05 - finished 2026-11-12 22:04:35
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 463 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,398.51 |
| CPU Overutilization (%) - lower | 489.95 |
| Overutilization Time (min) - lower | 14.57 |
| CPU Overprovision (m) - lower | 82.42 |
| Overprovision Time (min) - higher | 0.68 |
| CPU Underprovision (m) - lower | 4,496.24 |
| Underprovision Time (min) - lower | 14.31 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65571 | 0 | 210 | 810 | 1200 | 72.93 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 382.29 | 94.06 | 14.19 | 6.05 | 0.81 | 1,534.34 | 14.14 |
| currencyservice | 663.50 | 50.43 | 14.57 | 7.13 | 0.68 | 1,127.21 | 14.31 |
| cartservice | 388.34 | 28.05 | 12.83 | 11.66 | 0.68 | 300.65 | 12.83 |
| adservice | 200.00 | 0.00 | 0.00 | 20.73 | 0.42 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 46.36 | 13.33 | 5.62 | 0.47 | 182.72 | 13.33 |
| productcatalogservice | 194.38 | 63.50 | 13.58 | 5.62 | 0.47 | 492.66 | 13.58 |
| recommendationservice | 100.00 | 94.79 | 14.06 | 5.18 | 0.42 | 428.51 | 14.06 |
| paymentservice | 100.00 | 69.52 | 14.06 | 5.83 | 0.68 | 298.27 | 14.06 |
| shippingservice | 100.00 | 25.79 | 12.32 | 5.18 | 0.42 | 82.07 | 12.32 |
| emailservice | 100.00 | 0.36 | 0.26 | 5.18 | 0.42 | 1.73 | 0.26 |
| redis-cart | 70.00 | 17.10 | 11.05 | 4.23 | 0.70 | 48.08 | 11.05 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
