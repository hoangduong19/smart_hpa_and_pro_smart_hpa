# Run report: prosmarthpa-authors | 2R-20% | run 3

- Started 2026-10-24 11:20:00 - finished 2026-10-24 11:35:30
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 429 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,696.85 |
| CPU Overutilization (%) - lower | 484.86 |
| Overutilization Time (min) - lower | 14.48 |
| CPU Overprovision (m) - lower | 167.16 |
| Overprovision Time (min) - higher | 0.51 |
| CPU Underprovision (m) - lower | 5,257.81 |
| Underprovision Time (min) - lower | 14.48 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 64649 | 0 | 240 | 810 | 1200 | 71.94 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 292.31 | 134.43 | 14.48 | 2.56 | 0.51 | 1,823.31 | 14.48 |
| currencyservice | 294.87 | 122.21 | 14.48 | 3.26 | 0.51 | 1,670.16 | 14.48 |
| cartservice | 394.87 | 31.02 | 12.98 | 10.72 | 0.74 | 342.66 | 12.72 |
| adservice | 394.87 | 0.21 | 0.50 | 55.94 | 3.94 | 1.40 | 0.50 |
| checkoutservice | 197.44 | 24.98 | 12.48 | 10.26 | 1.75 | 122.61 | 12.48 |
| productcatalogservice | 197.44 | 74.75 | 13.73 | 2.56 | 0.51 | 601.63 | 13.73 |
| recommendationservice | 197.44 | 58.81 | 13.71 | 2.56 | 0.51 | 441.49 | 13.71 |
| paymentservice | 197.44 | 37.17 | 13.24 | 2.80 | 0.74 | 237.30 | 13.24 |
| shippingservice | 197.67 | 1.29 | 0.98 | 15.38 | 2.50 | 6.06 | 0.98 |
| emailservice | 194.64 | 0.00 | 0.00 | 49.18 | 6.29 | 11.19 | 1.65 |
| redis-cart | 137.88 | 0.00 | 0.00 | 11.91 | 2.40 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
