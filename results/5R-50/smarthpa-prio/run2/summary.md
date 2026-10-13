# Run report: smarthpa-prio | 5R-50% | run 2

- Started 2026-10-13 17:49:44 - finished 2026-10-13 18:05:18
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 258 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 4,918.45 |
| CPU Overutilization (%) - lower | 76.53 |
| Overutilization Time (min) - lower | 11.24 |
| CPU Overprovision (m) - lower | 1,304.73 |
| Overprovision Time (min) - higher | 11.63 |
| CPU Underprovision (m) - lower | 43.41 |
| Underprovision Time (min) - lower | 3.33 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67904 | 0 | 190 | 580 | 990 | 75.52 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 1,123.26 | 21.99 | 6.62 | 72.48 | 5.15 | 8.14 | 0.75 |
| currencyservice | 1,762.02 | 25.03 | 6.54 | 56.20 | 5.11 | 12.79 | 1.47 |
| cartservice | 438.76 | 6.13 | 1.74 | 276.74 | 8.59 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 105.43 | 1.90 | 0.00 | 0.00 |
| checkoutservice | 174.81 | 0.43 | 0.10 | 206.20 | 14.96 | 0.00 | 0.00 |
| productcatalogservice | 408.14 | 4.60 | 1.10 | 87.98 | 5.03 | 3.88 | 0.47 |
| recommendationservice | 318.22 | 9.54 | 2.92 | 96.51 | 5.23 | 9.30 | 1.36 |
| paymentservice | 223.26 | 5.60 | 1.60 | 105.43 | 4.12 | 3.10 | 0.52 |
| shippingservice | 100.00 | 3.21 | 0.76 | 74.42 | 2.16 | 6.20 | 0.76 |
| emailservice | 100.00 | 0.00 | 0.00 | 91.47 | 3.41 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 131.86 | 14.96 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
