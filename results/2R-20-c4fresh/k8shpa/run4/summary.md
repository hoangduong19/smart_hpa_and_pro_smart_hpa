# Run report: k8shpa | 2R-20% | run 4

- Started 2026-11-19 19:03:40 - finished 2026-11-19 19:19:11
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 508 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,362.72 |
| CPU Overutilization (%) - lower | 491.56 |
| Overutilization Time (min) - lower | 14.62 |
| CPU Overprovision (m) - lower | 274.92 |
| Overprovision Time (min) - higher | 0.35 |
| CPU Underprovision (m) - lower | 3,974.80 |
| Underprovision Time (min) - lower | 14.62 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 70299 | 0 | 310 | 980 | 1200 | 78.21 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.70 | 153.99 | 14.62 | 3.35 | 0.35 | 1,382.48 | 14.62 |
| currencyservice | 193.70 | 99.75 | 14.62 | 3.35 | 0.35 | 858.66 | 14.62 |
| cartservice | 387.01 | 28.07 | 14.14 | 11.42 | 0.35 | 251.18 | 13.38 |
| adservice | 364.96 | 1.64 | 1.54 | 134.65 | 9.72 | 9.06 | 1.00 |
| checkoutservice | 193.50 | 31.12 | 13.63 | 5.51 | 0.60 | 174.80 | 13.37 |
| productcatalogservice | 193.50 | 76.48 | 14.38 | 5.51 | 0.60 | 618.50 | 14.38 |
| recommendationservice | 193.50 | 62.49 | 14.38 | 5.51 | 0.60 | 469.69 | 14.12 |
| paymentservice | 193.31 | 36.79 | 14.38 | 5.51 | 0.60 | 208.27 | 14.38 |
| shippingservice | 192.91 | 0.09 | 0.18 | 6.69 | 1.11 | 0.00 | 0.00 |
| emailservice | 186.61 | 1.15 | 0.77 | 23.43 | 3.89 | 2.17 | 0.49 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
