# Run report: k8shpa | 2R-20% | run 1

- Started 2026-10-05 09:05:28 - finished 2026-10-05 09:20:58
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 425 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,079.88 |
| CPU Overutilization (%) - lower | 463.70 |
| Overutilization Time (min) - lower | 14.65 |
| CPU Overprovision (m) - lower | 444.59 |
| Overprovision Time (min) - higher | 0.31 |
| CPU Underprovision (m) - lower | 3,743.76 |
| Underprovision Time (min) - lower | 14.65 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 59250 | 0 | 400 | 1300 | 1700 | 65.89 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.41 | 155.86 | 14.63 | 3.29 | 0.33 | 1,402.82 | 14.38 |
| currencyservice | 193.41 | 98.11 | 14.65 | 3.06 | 0.31 | 830.59 | 14.65 |
| cartservice | 376.94 | 26.91 | 13.63 | 22.59 | 1.33 | 248.00 | 12.90 |
| adservice | 200.00 | 0.00 | 0.00 | 200.00 | 14.96 | 0.00 | 0.00 |
| checkoutservice | 190.59 | 30.17 | 13.15 | 8.94 | 1.33 | 167.06 | 12.90 |
| productcatalogservice | 191.29 | 64.56 | 14.13 | 6.82 | 0.83 | 500.71 | 13.93 |
| recommendationservice | 190.82 | 56.18 | 13.13 | 8.94 | 1.33 | 424.24 | 13.11 |
| paymentservice | 190.59 | 29.91 | 13.63 | 8.94 | 1.33 | 168.47 | 13.38 |
| shippingservice | 182.82 | 1.22 | 0.71 | 15.76 | 2.59 | 1.88 | 0.27 |
| emailservice | 100.00 | 0.79 | 0.51 | 96.24 | 14.45 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.96 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
