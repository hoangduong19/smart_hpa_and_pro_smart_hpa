# Run report: k8shpa | 2R-20% | run 8

- Started 2026-11-20 10:11:02 - finished 2026-11-20 10:26:33
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 476 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,096.89 |
| CPU Overutilization (%) - lower | 475.18 |
| Overutilization Time (min) - lower | 14.73 |
| CPU Overprovision (m) - lower | 393.61 |
| Overprovision Time (min) - higher | 0.50 |
| CPU Underprovision (m) - lower | 3,798.11 |
| Underprovision Time (min) - lower | 14.49 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73088 | 0 | 290 | 760 | 1300 | 81.27 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.07 | 149.74 | 14.49 | 4.62 | 0.50 | 1,338.24 | 14.49 |
| currencyservice | 193.70 | 99.83 | 14.73 | 2.52 | 0.26 | 836.97 | 14.49 |
| cartservice | 385.29 | 34.92 | 14.24 | 22.27 | 0.75 | 405.46 | 13.74 |
| adservice | 200.00 | 3.17 | 2.25 | 183.61 | 13.76 | 0.00 | 0.00 |
| checkoutservice | 193.28 | 38.11 | 14.49 | 4.62 | 0.50 | 233.61 | 14.24 |
| productcatalogservice | 193.28 | 60.81 | 14.49 | 4.62 | 0.50 | 459.87 | 14.49 |
| recommendationservice | 192.65 | 58.59 | 14.49 | 4.62 | 0.50 | 431.93 | 14.24 |
| paymentservice | 100.00 | 0.00 | 0.00 | 100.00 | 14.99 | 0.00 | 0.00 |
| shippingservice | 192.86 | 19.61 | 12.99 | 6.51 | 0.75 | 85.71 | 12.72 |
| emailservice | 182.77 | 1.83 | 1.01 | 17.86 | 2.76 | 6.30 | 0.38 |
| redis-cart | 70.00 | 8.58 | 5.94 | 42.35 | 9.05 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
