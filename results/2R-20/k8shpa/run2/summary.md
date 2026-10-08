# Run report: k8shpa | 2R-20% | run 2

- Started 2026-10-05 09:46:55 - finished 2026-10-05 10:02:25
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 394 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,086.75 |
| CPU Overutilization (%) - lower | 457.82 |
| Overutilization Time (min) - lower | 14.61 |
| CPU Overprovision (m) - lower | 438.78 |
| Overprovision Time (min) - higher | 0.37 |
| CPU Underprovision (m) - lower | 3,682.23 |
| Underprovision Time (min) - lower | 14.61 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 58692 | 0 | 410 | 1300 | 1800 | 65.33 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 192.39 | 153.93 | 14.38 | 6.09 | 0.60 | 1,390.61 | 14.38 |
| currencyservice | 193.15 | 95.76 | 14.61 | 3.81 | 0.37 | 823.35 | 14.61 |
| cartservice | 383.25 | 25.38 | 12.84 | 16.24 | 1.38 | 227.41 | 12.34 |
| adservice | 200.00 | 0.00 | 0.00 | 202.54 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 191.37 | 29.67 | 13.11 | 8.12 | 1.37 | 158.12 | 12.60 |
| productcatalogservice | 192.13 | 62.42 | 14.10 | 7.11 | 0.87 | 482.74 | 13.85 |
| recommendationservice | 191.62 | 58.51 | 14.10 | 7.11 | 0.87 | 436.80 | 13.35 |
| paymentservice | 191.88 | 30.19 | 13.35 | 7.87 | 1.13 | 163.20 | 13.10 |
| shippingservice | 180.96 | 0.78 | 0.42 | 15.48 | 2.86 | 0.00 | 0.00 |
| emailservice | 100.00 | 1.19 | 0.77 | 94.42 | 14.21 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
