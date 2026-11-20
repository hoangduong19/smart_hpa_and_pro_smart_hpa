# Run report: k8shpa | 2R-20% | run 1

- Started 2026-11-20 01:20:53 - finished 2026-11-20 01:36:24
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 482 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,257.76 |
| CPU Overutilization (%) - lower | 478.49 |
| Overutilization Time (min) - lower | 14.58 |
| CPU Overprovision (m) - lower | 421.95 |
| Overprovision Time (min) - higher | 0.40 |
| CPU Underprovision (m) - lower | 3,986.10 |
| Underprovision Time (min) - lower | 14.58 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73130 | 0 | 280 | 700 | 1200 | 81.35 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.81 | 171.26 | 14.58 | 3.94 | 0.40 | 1,556.85 | 14.58 |
| currencyservice | 194.81 | 91.92 | 14.58 | 3.94 | 0.40 | 758.51 | 14.58 |
| cartservice | 389.63 | 34.38 | 14.58 | 15.77 | 0.40 | 386.72 | 14.08 |
| adservice | 389.63 | 2.10 | 1.98 | 128.22 | 9.21 | 17.01 | 1.47 |
| checkoutservice | 194.61 | 34.07 | 14.08 | 5.19 | 0.91 | 188.80 | 13.98 |
| productcatalogservice | 195.02 | 70.64 | 14.58 | 3.94 | 0.40 | 558.71 | 14.47 |
| recommendationservice | 194.81 | 65.57 | 14.58 | 3.94 | 0.40 | 501.87 | 14.08 |
| paymentservice | 140.04 | 1.00 | 0.70 | 95.85 | 14.29 | 2.07 | 0.45 |
| shippingservice | 194.40 | 3.29 | 2.27 | 5.60 | 1.41 | 15.56 | 2.27 |
| emailservice | 100.00 | 0.35 | 0.26 | 98.34 | 14.73 | 0.00 | 0.00 |
| redis-cart | 70.00 | 3.91 | 2.74 | 57.22 | 12.25 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
