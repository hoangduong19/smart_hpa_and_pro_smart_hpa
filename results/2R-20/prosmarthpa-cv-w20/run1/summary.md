# Run report: prosmarthpa-cv-w20 | 2R-20% | run 1

- Started 2026-11-12 23:14:55 - finished 2026-11-12 23:30:25
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 489 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,407.01 |
| CPU Overutilization (%) - lower | 400.71 |
| Overutilization Time (min) - lower | 14.65 |
| CPU Overprovision (m) - lower | 74.48 |
| Overprovision Time (min) - higher | 0.60 |
| CPU Underprovision (m) - lower | 3,466.81 |
| Underprovision Time (min) - lower | 14.39 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62861 | 0 | 300 | 980 | 1300 | 69.94 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 289.78 | 108.37 | 14.39 | 4.91 | 0.60 | 1,386.71 | 14.14 |
| currencyservice | 667.28 | 29.70 | 14.65 | 4.09 | 0.33 | 388.34 | 14.39 |
| cartservice | 200.00 | 53.36 | 13.89 | 9.41 | 0.40 | 435.99 | 13.89 |
| adservice | 200.00 | 0.00 | 0.00 | 14.72 | 0.33 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 43.44 | 13.40 | 5.32 | 0.84 | 168.92 | 13.40 |
| productcatalogservice | 290.18 | 44.39 | 13.40 | 10.02 | 1.35 | 436.61 | 13.40 |
| recommendationservice | 195.09 | 49.78 | 13.65 | 7.16 | 0.85 | 357.87 | 13.65 |
| paymentservice | 194.68 | 32.09 | 13.65 | 5.32 | 0.84 | 170.14 | 13.65 |
| shippingservice | 100.00 | 24.84 | 12.41 | 4.91 | 0.60 | 79.14 | 12.41 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.91 | 0.60 | 0.00 | 0.00 |
| redis-cart | 70.00 | 14.73 | 9.91 | 3.72 | 0.84 | 43.09 | 9.91 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
