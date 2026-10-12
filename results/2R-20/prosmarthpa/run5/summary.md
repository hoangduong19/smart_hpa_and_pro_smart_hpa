# Run report: prosmarthpa | 2R-20% | run 5

- Started 2026-10-12 12:14:44 - finished 2026-10-12 12:30:14
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 447 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,068.28 |
| CPU Overutilization (%) - lower | 366.83 |
| Overutilization Time (min) - lower | 14.80 |
| CPU Overprovision (m) - lower | 70.56 |
| Overprovision Time (min) - higher | 0.45 |
| CPU Underprovision (m) - lower | 5,179.42 |
| Underprovision Time (min) - lower | 14.53 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65401 | 0 | 200 | 800 | 1200 | 72.74 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 530.43 | 72.08 | 14.61 | 4.25 | 0.37 | 1,556.82 | 14.28 |
| currencyservice | 849.89 | 47.89 | 14.80 | 4.47 | 0.45 | 1,635.79 | 14.53 |
| cartservice | 384.79 | 27.62 | 12.05 | 17.90 | 0.60 | 492.17 | 14.03 |
| adservice | 200.00 | 0.33 | 0.24 | 8.95 | 0.45 | 3.13 | 0.24 |
| checkoutservice | 100.00 | 44.61 | 13.05 | 4.47 | 0.45 | 171.59 | 13.05 |
| productcatalogservice | 195.08 | 71.91 | 13.78 | 4.92 | 0.50 | 574.27 | 13.78 |
| recommendationservice | 194.85 | 59.26 | 13.79 | 5.15 | 0.70 | 454.59 | 13.79 |
| paymentservice | 194.85 | 30.78 | 13.05 | 5.15 | 0.70 | 172.93 | 13.05 |
| shippingservice | 166.89 | 6.44 | 3.80 | 5.15 | 0.70 | 93.06 | 12.22 |
| emailservice | 134.68 | 5.92 | 4.07 | 5.15 | 0.70 | 25.06 | 3.93 |
| redis-cart | 116.82 | 0.00 | 0.00 | 5.01 | 1.00 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
