# Run report: smarthpa-warmup | 2R-20% | run 2

- Started 2026-11-19 10:25:47 - finished 2026-11-19 10:41:18
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 480 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,377.50 |
| CPU Overutilization (%) - lower | 400.96 |
| Overutilization Time (min) - lower | 14.65 |
| CPU Overprovision (m) - lower | 151.67 |
| Overprovision Time (min) - higher | 0.34 |
| CPU Underprovision (m) - lower | 3,710.83 |
| Underprovision Time (min) - lower | 14.65 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67401 | 0 | 390 | 1200 | 1700 | 74.94 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 452.71 | 73.09 | 14.65 | 2.92 | 0.34 | 1,197.50 | 14.65 |
| currencyservice | 195.21 | 99.12 | 14.65 | 2.92 | 0.34 | 857.92 | 14.65 |
| cartservice | 388.75 | 26.96 | 14.40 | 11.67 | 0.60 | 240.42 | 13.89 |
| adservice | 200.00 | 0.45 | 0.24 | 25.00 | 2.00 | 3.75 | 0.24 |
| checkoutservice | 194.58 | 29.80 | 13.90 | 5.00 | 0.60 | 163.33 | 13.85 |
| productcatalogservice | 194.58 | 66.61 | 14.40 | 5.00 | 0.60 | 518.12 | 14.40 |
| recommendationservice | 194.38 | 66.21 | 14.40 | 5.00 | 0.60 | 511.25 | 14.15 |
| paymentservice | 194.38 | 35.87 | 14.40 | 5.00 | 0.60 | 205.62 | 14.15 |
| shippingservice | 192.92 | 0.09 | 0.06 | 6.67 | 1.10 | 0.00 | 0.00 |
| emailservice | 100.00 | 2.76 | 1.95 | 12.50 | 2.00 | 12.92 | 1.95 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 15.00 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
