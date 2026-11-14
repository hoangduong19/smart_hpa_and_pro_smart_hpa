# Run report: prosmarthpa-cv-w30 | 2R-20% | run 2

- Started 2026-11-13 01:21:55 - finished 2026-11-13 01:37:25
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 480 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,403.54 |
| CPU Overutilization (%) - lower | 546.87 |
| Overutilization Time (min) - lower | 14.65 |
| CPU Overprovision (m) - lower | 70.67 |
| Overprovision Time (min) - higher | 0.60 |
| CPU Underprovision (m) - lower | 4,356.15 |
| Underprovision Time (min) - lower | 14.39 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67034 | 0 | 190 | 670 | 1100 | 74.54 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 287.71 | 113.35 | 14.65 | 4.17 | 0.34 | 1,452.92 | 14.22 |
| currencyservice | 951.25 | 37.94 | 14.65 | 10.42 | 0.60 | 935.00 | 14.39 |
| cartservice | 200.00 | 54.52 | 13.89 | 10.00 | 0.34 | 464.58 | 13.89 |
| adservice | 200.00 | 0.32 | 0.24 | 15.00 | 0.34 | 2.92 | 0.24 |
| checkoutservice | 100.00 | 46.09 | 13.65 | 5.21 | 0.45 | 180.42 | 13.65 |
| productcatalogservice | 100.00 | 124.23 | 14.39 | 4.17 | 0.34 | 560.62 | 14.39 |
| recommendationservice | 100.00 | 94.83 | 13.89 | 4.17 | 0.34 | 426.46 | 13.89 |
| paymentservice | 194.58 | 34.88 | 13.90 | 5.42 | 0.60 | 212.08 | 13.90 |
| shippingservice | 100.00 | 25.11 | 12.39 | 4.17 | 0.34 | 76.67 | 12.39 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.17 | 0.34 | 0.00 | 0.00 |
| redis-cart | 70.00 | 15.59 | 10.63 | 3.79 | 0.60 | 44.48 | 10.63 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
