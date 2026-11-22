# Run report: prosmarthpa-authors | 2R-20% | run 2

- Started 2026-11-22 03:49:54 - finished 2026-11-22 04:05:25
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 459 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,502.70 |
| CPU Overutilization (%) - lower | 457.81 |
| Overutilization Time (min) - lower | 14.78 |
| CPU Overprovision (m) - lower | 276.12 |
| Overprovision Time (min) - higher | 0.27 |
| CPU Underprovision (m) - lower | 4,202.40 |
| Underprovision Time (min) - lower | 14.72 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 70406 | 0 | 320 | 980 | 1300 | 78.26 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 294.34 | 122.17 | 14.52 | 3.70 | 0.47 | 1,591.72 | 14.52 |
| currencyservice | 197.17 | 98.22 | 14.78 | 2.18 | 0.20 | 856.43 | 14.52 |
| cartservice | 394.34 | 26.18 | 13.28 | 10.02 | 0.47 | 244.01 | 13.28 |
| adservice | 394.34 | 0.41 | 0.50 | 177.78 | 13.00 | 5.23 | 0.50 |
| checkoutservice | 197.39 | 30.67 | 13.77 | 3.05 | 0.75 | 170.15 | 13.77 |
| productcatalogservice | 197.39 | 75.81 | 14.72 | 2.61 | 0.27 | 607.63 | 14.72 |
| recommendationservice | 197.17 | 67.81 | 14.52 | 2.83 | 0.47 | 526.58 | 14.52 |
| paymentservice | 197.17 | 35.40 | 14.02 | 2.83 | 0.47 | 195.42 | 14.02 |
| shippingservice | 195.86 | 0.00 | 0.00 | 6.32 | 1.45 | 0.00 | 0.00 |
| emailservice | 100.00 | 1.13 | 0.79 | 1.96 | 0.17 | 5.23 | 0.79 |
| redis-cart | 137.56 | 0.00 | 0.00 | 62.83 | 13.53 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
