# Run report: prosmarthpa-cv-w20 | 2R-20% | run 3

- Started 2026-11-13 02:46:19 - finished 2026-11-13 03:01:49
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 431 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,402.95 |
| CPU Overutilization (%) - lower | 450.74 |
| Overutilization Time (min) - lower | 14.81 |
| CPU Overprovision (m) - lower | 56.33 |
| Overprovision Time (min) - higher | 0.40 |
| CPU Underprovision (m) - lower | 3,048.14 |
| Underprovision Time (min) - lower | 14.59 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 64023 | 0 | 290 | 880 | 1300 | 71.21 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.43 | 136.98 | 14.54 | 4.87 | 0.45 | 1,222.74 | 14.29 |
| currencyservice | 949.42 | 22.30 | 14.81 | 6.96 | 0.40 | 127.61 | 14.59 |
| cartservice | 200.00 | 47.17 | 13.80 | 4.64 | 0.19 | 375.87 | 13.80 |
| adservice | 200.00 | 0.00 | 0.00 | 4.64 | 0.19 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 41.34 | 13.30 | 4.87 | 0.60 | 158.70 | 13.30 |
| productcatalogservice | 194.66 | 58.35 | 13.80 | 5.34 | 0.50 | 450.35 | 13.80 |
| recommendationservice | 194.43 | 47.79 | 13.55 | 5.57 | 0.70 | 343.62 | 13.55 |
| paymentservice | 100.00 | 63.34 | 14.29 | 5.57 | 0.70 | 260.09 | 14.29 |
| shippingservice | 100.00 | 22.37 | 12.04 | 5.34 | 0.50 | 74.25 | 12.04 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.64 | 0.40 | 0.00 | 0.00 |
| redis-cart | 70.00 | 11.09 | 8.24 | 3.90 | 0.70 | 34.92 | 8.24 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
