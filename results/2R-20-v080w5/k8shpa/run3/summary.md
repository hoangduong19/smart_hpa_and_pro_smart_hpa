# Run report: k8shpa | 2R-20% | run 3

- Started 2026-11-20 05:42:53 - finished 2026-11-20 05:58:24
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 488 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,117.34 |
| CPU Overutilization (%) - lower | 498.23 |
| Overutilization Time (min) - lower | 14.56 |
| CPU Overprovision (m) - lower | 491.11 |
| Overprovision Time (min) - higher | 0.41 |
| CPU Underprovision (m) - lower | 4,117.21 |
| Underprovision Time (min) - lower | 14.56 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 76506 | 0 | 190 | 480 | 1100 | 85.07 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.88 | 174.49 | 14.56 | 3.89 | 0.41 | 1,591.39 | 14.56 |
| currencyservice | 194.88 | 90.60 | 14.56 | 3.89 | 0.41 | 747.54 | 14.56 |
| cartservice | 389.34 | 32.38 | 14.06 | 15.16 | 0.91 | 345.90 | 14.06 |
| adservice | 288.93 | 0.48 | 0.25 | 184.43 | 13.98 | 0.00 | 0.00 |
| checkoutservice | 194.67 | 40.53 | 14.06 | 5.12 | 0.91 | 260.45 | 13.81 |
| productcatalogservice | 195.08 | 67.18 | 14.56 | 3.89 | 0.41 | 532.58 | 14.45 |
| recommendationservice | 194.88 | 69.99 | 14.06 | 5.12 | 0.91 | 550.82 | 14.06 |
| paymentservice | 100.00 | 0.41 | 0.26 | 98.16 | 14.71 | 0.00 | 0.00 |
| shippingservice | 194.67 | 21.41 | 13.06 | 5.12 | 0.91 | 88.52 | 12.81 |
| emailservice | 100.00 | 0.77 | 0.50 | 96.31 | 14.47 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.97 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
