# Run report: k8shpa | 2R-20% | run 3

- Started 2026-10-05 10:28:27 - finished 2026-10-05 10:43:58
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 409 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,076.85 |
| CPU Overutilization (%) - lower | 468.09 |
| Overutilization Time (min) - lower | 14.66 |
| CPU Overprovision (m) - lower | 432.10 |
| Overprovision Time (min) - higher | 0.31 |
| CPU Underprovision (m) - lower | 3,725.67 |
| Underprovision Time (min) - lower | 14.66 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 59674 | 0 | 400 | 1300 | 1700 | 66.36 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.40 | 154.36 | 14.66 | 2.93 | 0.31 | 1,375.31 | 14.41 |
| currencyservice | 193.40 | 97.62 | 14.66 | 2.93 | 0.31 | 830.07 | 14.66 |
| cartservice | 373.11 | 24.83 | 12.61 | 23.96 | 1.58 | 229.83 | 12.13 |
| adservice | 200.00 | 0.00 | 0.00 | 201.47 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 191.20 | 30.23 | 12.83 | 7.09 | 1.09 | 161.86 | 12.65 |
| productcatalogservice | 193.15 | 73.42 | 14.41 | 5.38 | 0.57 | 576.77 | 14.14 |
| recommendationservice | 190.95 | 55.32 | 14.14 | 6.85 | 0.84 | 402.20 | 13.39 |
| paymentservice | 190.95 | 28.17 | 13.90 | 6.85 | 0.84 | 144.74 | 13.15 |
| shippingservice | 180.68 | 2.29 | 1.46 | 13.45 | 2.07 | 4.89 | 0.75 |
| emailservice | 100.00 | 1.85 | 1.36 | 91.20 | 13.61 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
