# Run report: k8shpa | 2R-20% | run 7

- Started 2026-11-19 21:14:28 - finished 2026-11-19 21:29:59
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 514 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,355.99 |
| CPU Overutilization (%) - lower | 450.56 |
| Overutilization Time (min) - lower | 14.67 |
| CPU Overprovision (m) - lower | 233.81 |
| Overprovision Time (min) - higher | 0.30 |
| CPU Underprovision (m) - lower | 3,522.18 |
| Underprovision Time (min) - lower | 14.67 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69587 | 0 | 330 | 970 | 1400 | 77.39 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.39 | 149.74 | 14.67 | 2.92 | 0.30 | 1,327.04 | 14.67 |
| currencyservice | 193.58 | 98.63 | 14.67 | 2.92 | 0.30 | 849.81 | 14.67 |
| cartservice | 386.77 | 23.68 | 13.92 | 8.56 | 0.55 | 189.49 | 13.66 |
| adservice | 375.88 | 6.28 | 3.78 | 86.77 | 6.06 | 43.19 | 3.01 |
| checkoutservice | 193.19 | 27.46 | 14.16 | 6.61 | 0.81 | 126.46 | 13.91 |
| productcatalogservice | 193.39 | 56.48 | 14.40 | 5.25 | 0.57 | 414.20 | 14.16 |
| recommendationservice | 193.00 | 54.14 | 14.43 | 5.06 | 0.54 | 387.94 | 14.16 |
| paymentservice | 193.39 | 32.83 | 14.40 | 5.25 | 0.57 | 182.49 | 14.16 |
| shippingservice | 193.00 | 0.38 | 0.49 | 6.81 | 1.06 | 1.56 | 0.24 |
| emailservice | 170.43 | 0.94 | 0.56 | 33.66 | 5.30 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.97 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
