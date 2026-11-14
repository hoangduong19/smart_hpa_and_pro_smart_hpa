# Run report: prosmarthpa-cv | 2R-20% | run 0

- Started 2026-11-12 19:42:25 - finished 2026-11-12 19:57:55
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 509 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,388.27 |
| CPU Overutilization (%) - lower | 517.97 |
| Overutilization Time (min) - lower | 14.66 |
| CPU Overprovision (m) - lower | 70.90 |
| Overprovision Time (min) - higher | 0.48 |
| CPU Underprovision (m) - lower | 4,518.15 |
| Underprovision Time (min) - lower | 14.52 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65433 | 0 | 210 | 750 | 1100 | 72.75 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 287.23 | 119.98 | 14.66 | 3.93 | 0.33 | 1,549.90 | 14.40 |
| currencyservice | 843.81 | 41.81 | 14.66 | 7.07 | 0.60 | 1,014.15 | 14.40 |
| cartservice | 200.00 | 58.69 | 13.90 | 11.00 | 0.60 | 489.98 | 13.90 |
| adservice | 200.00 | 0.32 | 0.23 | 9.43 | 0.52 | 2.75 | 0.23 |
| checkoutservice | 100.00 | 47.26 | 13.40 | 6.09 | 0.67 | 188.41 | 13.40 |
| productcatalogservice | 100.00 | 123.26 | 14.15 | 4.72 | 0.42 | 563.06 | 14.15 |
| recommendationservice | 194.70 | 50.69 | 13.53 | 5.89 | 0.73 | 374.07 | 13.53 |
| paymentservice | 192.53 | 33.96 | 13.40 | 7.47 | 0.85 | 208.45 | 13.40 |
| shippingservice | 100.00 | 25.05 | 12.41 | 4.72 | 0.42 | 78.98 | 12.41 |
| emailservice | 100.00 | 0.00 | 0.00 | 5.50 | 0.60 | 0.00 | 0.00 |
| redis-cart | 70.00 | 16.97 | 11.15 | 5.09 | 0.80 | 48.41 | 11.15 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
