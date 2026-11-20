# Run report: k8shpa | 2R-20% | run 7

- Started 2026-11-20 09:17:19 - finished 2026-11-20 09:32:50
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 468 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,233.68 |
| CPU Overutilization (%) - lower | 474.85 |
| Overutilization Time (min) - lower | 14.75 |
| CPU Overprovision (m) - lower | 366.75 |
| Overprovision Time (min) - higher | 0.22 |
| CPU Underprovision (m) - lower | 3,885.04 |
| Underprovision Time (min) - lower | 14.75 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73580 | 0 | 250 | 710 | 1100 | 81.81 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 195.94 | 169.46 | 14.75 | 2.14 | 0.22 | 1,532.48 | 14.75 |
| currencyservice | 195.09 | 90.57 | 14.50 | 4.27 | 0.48 | 750.43 | 14.50 |
| cartservice | 390.17 | 34.12 | 14.50 | 8.55 | 0.48 | 397.86 | 14.25 |
| adservice | 322.22 | 0.77 | 0.50 | 156.41 | 11.71 | 0.00 | 0.00 |
| checkoutservice | 194.87 | 33.86 | 14.25 | 4.91 | 0.73 | 185.04 | 14.12 |
| productcatalogservice | 195.30 | 66.66 | 14.50 | 4.27 | 0.48 | 516.03 | 14.45 |
| recommendationservice | 194.66 | 57.89 | 14.50 | 4.27 | 0.48 | 423.93 | 14.25 |
| paymentservice | 100.00 | 0.00 | 0.00 | 100.00 | 14.98 | 0.00 | 0.00 |
| shippingservice | 194.23 | 15.98 | 10.81 | 5.34 | 0.98 | 72.86 | 10.76 |
| emailservice | 181.20 | 1.59 | 0.71 | 19.44 | 3.25 | 6.41 | 0.36 |
| redis-cart | 70.00 | 3.96 | 3.03 | 57.14 | 11.94 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
