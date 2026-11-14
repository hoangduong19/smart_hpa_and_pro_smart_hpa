# Run report: prosmarthpa-cv-w15 | 2R-20% | run 2

- Started 2026-11-13 00:39:35 - finished 2026-11-13 00:55:05
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 474 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,371.90 |
| CPU Overutilization (%) - lower | 509.71 |
| Overutilization Time (min) - lower | 14.58 |
| CPU Overprovision (m) - lower | 86.16 |
| Overprovision Time (min) - higher | 0.41 |
| CPU Underprovision (m) - lower | 4,363.73 |
| Underprovision Time (min) - lower | 14.58 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66548 | 0 | 200 | 650 | 1000 | 74.04 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 284.18 | 113.22 | 14.58 | 5.27 | 0.41 | 1,455.27 | 14.31 |
| currencyservice | 833.33 | 41.80 | 14.58 | 5.27 | 0.41 | 990.72 | 14.58 |
| cartservice | 200.00 | 57.35 | 13.81 | 13.92 | 0.68 | 477.64 | 13.81 |
| adservice | 200.00 | 0.00 | 0.00 | 10.55 | 0.41 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 46.05 | 13.58 | 8.44 | 0.84 | 184.18 | 13.58 |
| productcatalogservice | 100.00 | 126.39 | 14.31 | 6.96 | 0.68 | 580.17 | 14.31 |
| recommendationservice | 193.25 | 51.58 | 13.69 | 6.75 | 0.56 | 377.43 | 13.69 |
| paymentservice | 191.14 | 31.00 | 13.62 | 8.86 | 0.89 | 174.68 | 13.62 |
| shippingservice | 100.00 | 25.45 | 12.31 | 6.96 | 0.68 | 75.95 | 12.31 |
| emailservice | 100.00 | 0.00 | 0.00 | 6.96 | 0.68 | 0.00 | 0.00 |
| redis-cart | 70.00 | 16.87 | 11.32 | 6.20 | 0.89 | 47.70 | 11.32 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
