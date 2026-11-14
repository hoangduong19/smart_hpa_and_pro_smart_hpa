# Run report: prosmarthpa-cv-w30 | 2R-20% | run 3

- Started 2026-11-13 03:07:34 - finished 2026-11-13 03:23:04
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 439 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,384.35 |
| CPU Overutilization (%) - lower | 441.51 |
| Overutilization Time (min) - lower | 14.81 |
| CPU Overprovision (m) - lower | 80.80 |
| Overprovision Time (min) - higher | 0.70 |
| CPU Underprovision (m) - lower | 3,229.48 |
| Underprovision Time (min) - lower | 14.30 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 61501 | 0 | 310 | 1200 | 1600 | 68.42 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 473.80 | 67.38 | 14.05 | 13.21 | 0.65 | 1,261.96 | 14.05 |
| currencyservice | 747.84 | 28.00 | 14.81 | 3.42 | 0.33 | 295.90 | 14.30 |
| cartservice | 200.00 | 48.38 | 14.05 | 10.02 | 0.39 | 381.78 | 13.82 |
| adservice | 200.00 | 0.00 | 0.00 | 15.03 | 0.45 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 39.31 | 13.31 | 6.61 | 0.60 | 153.08 | 13.31 |
| productcatalogservice | 100.00 | 108.09 | 14.30 | 5.01 | 0.39 | 483.14 | 14.30 |
| recommendationservice | 100.00 | 84.50 | 13.82 | 5.01 | 0.39 | 378.82 | 13.82 |
| paymentservice | 192.71 | 29.78 | 13.55 | 7.29 | 0.70 | 157.18 | 13.55 |
| shippingservice | 100.00 | 21.79 | 12.07 | 5.01 | 0.39 | 74.26 | 12.07 |
| emailservice | 100.00 | 0.00 | 0.00 | 5.24 | 0.45 | 0.00 | 0.00 |
| redis-cart | 70.00 | 14.28 | 10.30 | 4.94 | 0.65 | 43.37 | 10.30 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
