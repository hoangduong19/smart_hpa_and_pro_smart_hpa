# Run report: smarthpa-prio | 2R-20% | run 1

- Started 2026-10-13 16:25:13 - finished 2026-10-13 16:40:44
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 332 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,441.93 |
| CPU Overutilization (%) - lower | 627.68 |
| Overutilization Time (min) - lower | 14.54 |
| CPU Overprovision (m) - lower | 81.87 |
| Overprovision Time (min) - higher | 0.68 |
| CPU Underprovision (m) - lower | 6,726.20 |
| Underprovision Time (min) - lower | 14.27 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 61097 | 0 | 370 | 1200 | 1600 | 67.90 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 567.77 | 87.41 | 14.54 | 3.92 | 0.42 | 2,064.76 | 14.03 |
| currencyservice | 381.93 | 121.38 | 14.54 | 3.92 | 0.42 | 2,059.64 | 14.27 |
| cartservice | 382.53 | 39.01 | 13.77 | 16.87 | 0.92 | 501.81 | 13.31 |
| adservice | 200.00 | 21.69 | 12.56 | 7.83 | 0.42 | 167.47 | 12.07 |
| checkoutservice | 190.66 | 31.04 | 12.74 | 8.73 | 1.14 | 173.49 | 12.51 |
| productcatalogservice | 193.37 | 79.51 | 14.27 | 6.02 | 0.68 | 653.31 | 14.19 |
| recommendationservice | 100.00 | 134.61 | 14.03 | 3.92 | 0.42 | 629.52 | 14.03 |
| paymentservice | 100.00 | 69.70 | 14.03 | 5.72 | 0.63 | 303.31 | 14.03 |
| shippingservice | 100.00 | 33.83 | 12.55 | 5.72 | 0.63 | 130.12 | 12.55 |
| emailservice | 100.00 | 9.25 | 6.47 | 5.72 | 0.63 | 42.77 | 6.47 |
| redis-cart | 125.66 | 0.28 | 0.18 | 13.49 | 2.91 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
