# Run report: k8shpa | 2R-20% | run 5

- Started 2026-11-20 07:30:01 - finished 2026-11-20 07:45:33
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 472 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,339.15 |
| CPU Overutilization (%) - lower | 507.60 |
| Overutilization Time (min) - lower | 14.74 |
| CPU Overprovision (m) - lower | 319.70 |
| Overprovision Time (min) - higher | 0.26 |
| CPU Underprovision (m) - lower | 4,185.59 |
| Underprovision Time (min) - lower | 14.74 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 75379 | 0 | 210 | 500 | 1100 | 83.84 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.28 | 176.68 | 14.74 | 2.33 | 0.26 | 1,609.11 | 14.48 |
| currencyservice | 194.07 | 92.51 | 14.74 | 2.33 | 0.26 | 754.24 | 14.74 |
| cartservice | 387.71 | 35.85 | 14.48 | 8.90 | 0.52 | 411.44 | 14.23 |
| adservice | 327.97 | 0.52 | 0.51 | 180.08 | 13.47 | 0.00 | 0.00 |
| checkoutservice | 193.86 | 33.34 | 14.48 | 4.45 | 0.52 | 182.42 | 13.98 |
| productcatalogservice | 194.07 | 84.87 | 14.48 | 4.45 | 0.52 | 692.16 | 14.48 |
| recommendationservice | 193.86 | 59.59 | 14.48 | 4.45 | 0.52 | 443.64 | 14.48 |
| paymentservice | 139.19 | 1.05 | 0.56 | 94.07 | 14.16 | 2.12 | 0.31 |
| shippingservice | 191.53 | 21.37 | 13.74 | 5.93 | 0.76 | 88.35 | 12.98 |
| emailservice | 188.56 | 1.27 | 1.27 | 8.26 | 1.50 | 2.12 | 0.42 |
| redis-cart | 134.07 | 0.55 | 0.26 | 4.45 | 1.26 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
