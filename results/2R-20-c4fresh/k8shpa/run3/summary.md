# Run report: k8shpa | 2R-20% | run 3

- Started 2026-11-19 18:20:05 - finished 2026-11-19 18:35:36
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 522 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,362.15 |
| CPU Overutilization (%) - lower | 600.74 |
| Overutilization Time (min) - lower | 14.81 |
| CPU Overprovision (m) - lower | 203.14 |
| Overprovision Time (min) - higher | 0.18 |
| CPU Underprovision (m) - lower | 5,021.65 |
| Underprovision Time (min) - lower | 14.81 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73441 | 0 | 260 | 760 | 1000 | 81.67 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.87 | 158.61 | 14.56 | 4.02 | 0.44 | 1,430.65 | 14.56 |
| currencyservice | 195.98 | 187.92 | 14.81 | 1.72 | 0.18 | 1,688.89 | 14.81 |
| cartservice | 387.74 | 28.96 | 13.80 | 8.05 | 0.44 | 280.46 | 13.56 |
| adservice | 366.28 | 4.41 | 2.49 | 74.71 | 5.75 | 41.38 | 2.25 |
| checkoutservice | 193.68 | 34.19 | 14.32 | 6.13 | 0.68 | 189.46 | 13.98 |
| productcatalogservice | 193.68 | 80.12 | 14.32 | 6.13 | 0.68 | 642.91 | 14.32 |
| recommendationservice | 193.68 | 67.96 | 14.56 | 4.02 | 0.44 | 527.59 | 14.32 |
| paymentservice | 193.68 | 36.82 | 14.32 | 6.13 | 0.68 | 216.09 | 13.98 |
| shippingservice | 189.46 | 0.63 | 0.36 | 7.66 | 1.17 | 0.00 | 0.00 |
| emailservice | 184.10 | 1.12 | 0.51 | 14.56 | 2.19 | 4.21 | 0.33 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.99 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
