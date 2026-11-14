# Run report: prosmarthpa-cv-w20 | 2R-20% | run 2

- Started 2026-11-13 01:00:45 - finished 2026-11-13 01:16:15
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 481 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,451.35 |
| CPU Overutilization (%) - lower | 400.35 |
| Overutilization Time (min) - lower | 14.74 |
| CPU Overprovision (m) - lower | 97.59 |
| Overprovision Time (min) - higher | 0.53 |
| CPU Underprovision (m) - lower | 3,065.28 |
| Underprovision Time (min) - lower | 14.47 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 63722 | 0 | 290 | 910 | 1300 | 70.89 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.14 | 137.93 | 14.49 | 6.24 | 0.50 | 1,231.60 | 14.23 |
| currencyservice | 656.76 | 29.89 | 14.74 | 3.12 | 0.25 | 383.78 | 14.25 |
| cartservice | 386.28 | 24.06 | 13.23 | 13.72 | 0.76 | 217.05 | 13.23 |
| adservice | 200.00 | 0.00 | 0.00 | 12.47 | 0.50 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 42.65 | 13.23 | 6.86 | 0.76 | 161.33 | 13.23 |
| productcatalogservice | 193.35 | 60.42 | 13.73 | 6.65 | 0.55 | 458.21 | 13.73 |
| recommendationservice | 193.14 | 49.58 | 13.73 | 6.86 | 0.76 | 356.34 | 13.73 |
| paymentservice | 193.35 | 31.52 | 13.70 | 6.65 | 0.55 | 177.34 | 13.70 |
| shippingservice | 100.00 | 24.30 | 12.48 | 6.44 | 0.52 | 79.63 | 12.48 |
| emailservice | 100.00 | 0.00 | 0.00 | 6.44 | 0.52 | 0.00 | 0.00 |
| redis-cart | 135.34 | 0.00 | 0.00 | 22.12 | 4.01 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
