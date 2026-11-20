# Run report: k8shpa | 2R-20% | run 2

- Started 2026-11-20 04:02:34 - finished 2026-11-20 04:18:05
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 468 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,148.08 |
| CPU Overutilization (%) - lower | 475.96 |
| Overutilization Time (min) - lower | 14.50 |
| CPU Overprovision (m) - lower | 417.41 |
| Overprovision Time (min) - higher | 0.47 |
| CPU Underprovision (m) - lower | 3,931.41 |
| Underprovision Time (min) - lower | 14.50 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 72562 | 0 | 270 | 820 | 1400 | 80.72 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.80 | 173.02 | 14.50 | 4.27 | 0.47 | 1,576.71 | 14.50 |
| currencyservice | 193.80 | 91.17 | 14.50 | 4.27 | 0.47 | 746.37 | 14.50 |
| cartservice | 385.90 | 33.37 | 14.25 | 12.82 | 0.72 | 381.62 | 13.77 |
| adservice | 285.47 | 1.18 | 0.75 | 162.82 | 12.46 | 0.00 | 0.00 |
| checkoutservice | 192.74 | 31.34 | 14.00 | 7.05 | 0.97 | 173.93 | 13.86 |
| productcatalogservice | 193.16 | 69.76 | 14.25 | 6.41 | 0.72 | 549.36 | 14.25 |
| recommendationservice | 192.95 | 58.21 | 14.25 | 6.41 | 0.72 | 443.59 | 14.00 |
| paymentservice | 100.00 | 0.00 | 0.00 | 100.00 | 14.97 | 0.00 | 0.00 |
| shippingservice | 192.09 | 13.26 | 9.02 | 7.48 | 1.22 | 59.83 | 8.96 |
| emailservice | 100.00 | 0.83 | 0.52 | 96.15 | 14.44 | 0.00 | 0.00 |
| redis-cart | 118.16 | 3.83 | 2.59 | 9.72 | 2.19 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
