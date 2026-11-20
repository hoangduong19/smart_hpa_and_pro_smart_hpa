# Run report: k8shpa | 2R-20% | run 2

- Started 2026-11-19 17:36:29 - finished 2026-11-19 17:52:01
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 517 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,386.44 |
| CPU Overutilization (%) - lower | 489.78 |
| Overutilization Time (min) - lower | 14.69 |
| CPU Overprovision (m) - lower | 190.17 |
| Overprovision Time (min) - higher | 0.29 |
| CPU Underprovision (m) - lower | 3,917.41 |
| Underprovision Time (min) - lower | 14.69 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69772 | 0 | 360 | 990 | 1300 | 77.62 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.62 | 158.15 | 14.69 | 2.71 | 0.29 | 1,416.63 | 14.44 |
| currencyservice | 193.62 | 98.47 | 14.69 | 2.71 | 0.29 | 846.42 | 14.69 |
| cartservice | 386.46 | 27.88 | 14.19 | 10.44 | 0.54 | 259.96 | 13.69 |
| adservice | 358.61 | 3.23 | 2.27 | 114.89 | 8.44 | 21.66 | 1.50 |
| checkoutservice | 193.23 | 28.02 | 14.19 | 6.58 | 0.79 | 133.08 | 13.94 |
| productcatalogservice | 193.42 | 62.50 | 14.44 | 5.03 | 0.54 | 469.44 | 14.19 |
| recommendationservice | 193.23 | 66.73 | 14.46 | 4.84 | 0.52 | 518.57 | 14.19 |
| paymentservice | 193.04 | 38.15 | 14.19 | 6.58 | 0.79 | 243.91 | 14.19 |
| shippingservice | 187.04 | 1.40 | 0.74 | 6.96 | 1.28 | 0.00 | 0.00 |
| emailservice | 163.25 | 4.76 | 2.75 | 20.50 | 3.02 | 7.74 | 0.41 |
| redis-cart | 130.93 | 0.50 | 0.24 | 8.94 | 2.03 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
