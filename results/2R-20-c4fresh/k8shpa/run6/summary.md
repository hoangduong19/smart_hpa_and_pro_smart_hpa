# Run report: k8shpa | 2R-20% | run 6

- Started 2026-11-19 20:30:51 - finished 2026-11-19 20:46:22
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 502 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,324.48 |
| CPU Overutilization (%) - lower | 484.13 |
| Overutilization Time (min) - lower | 14.79 |
| CPU Overprovision (m) - lower | 265.02 |
| Overprovision Time (min) - higher | 0.41 |
| CPU Underprovision (m) - lower | 3,868.33 |
| Underprovision Time (min) - lower | 14.56 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 70983 | 0 | 310 | 970 | 1300 | 78.98 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.82 | 148.47 | 14.56 | 3.98 | 0.41 | 1,329.88 | 14.56 |
| currencyservice | 196.02 | 98.25 | 14.79 | 1.79 | 0.18 | 865.34 | 14.56 |
| cartservice | 387.65 | 26.13 | 14.15 | 7.97 | 0.41 | 217.13 | 13.90 |
| adservice | 375.70 | 6.36 | 3.25 | 105.18 | 7.14 | 45.42 | 2.51 |
| checkoutservice | 193.63 | 31.17 | 13.90 | 3.98 | 0.41 | 170.72 | 13.30 |
| productcatalogservice | 193.63 | 70.09 | 14.31 | 6.18 | 0.66 | 557.97 | 14.31 |
| recommendationservice | 193.63 | 58.80 | 14.31 | 6.18 | 0.66 | 443.03 | 13.96 |
| paymentservice | 193.63 | 38.11 | 14.31 | 6.18 | 0.66 | 237.05 | 14.31 |
| shippingservice | 192.63 | 0.57 | 0.33 | 6.57 | 1.18 | 1.79 | 0.23 |
| emailservice | 100.00 | 0.88 | 0.55 | 95.82 | 14.43 | 0.00 | 0.00 |
| redis-cart | 104.16 | 5.30 | 3.15 | 21.20 | 4.71 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
