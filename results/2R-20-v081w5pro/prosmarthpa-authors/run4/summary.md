# Run report: prosmarthpa-authors | 2R-20% | run 4

- Started 2026-11-22 04:43:35 - finished 2026-11-22 04:59:07
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 443 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,503.23 |
| CPU Overutilization (%) - lower | 496.29 |
| Overutilization Time (min) - lower | 14.44 |
| CPU Overprovision (m) - lower | 181.24 |
| Overprovision Time (min) - higher | 0.53 |
| CPU Underprovision (m) - lower | 4,564.79 |
| Underprovision Time (min) - lower | 14.44 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 70897 | 0 | 310 | 910 | 1300 | 78.84 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 294.58 | 133.73 | 14.44 | 3.39 | 0.53 | 1,758.24 | 14.44 |
| currencyservice | 197.29 | 98.25 | 14.44 | 2.71 | 0.53 | 869.75 | 14.44 |
| cartservice | 394.58 | 29.35 | 14.18 | 5.87 | 0.53 | 285.78 | 14.18 |
| adservice | 394.58 | 0.14 | 0.25 | 149.44 | 11.18 | 1.81 | 0.25 |
| checkoutservice | 197.29 | 35.74 | 13.94 | 2.71 | 0.53 | 206.32 | 13.94 |
| productcatalogservice | 197.52 | 69.69 | 14.18 | 2.48 | 0.24 | 548.53 | 14.18 |
| recommendationservice | 197.29 | 71.68 | 14.44 | 2.71 | 0.53 | 565.01 | 14.44 |
| paymentservice | 197.29 | 38.89 | 14.44 | 2.71 | 0.53 | 247.18 | 14.44 |
| shippingservice | 195.49 | 0.00 | 0.00 | 4.51 | 1.09 | 0.00 | 0.00 |
| emailservice | 100.00 | 18.82 | 11.92 | 2.03 | 0.18 | 82.17 | 11.92 |
| redis-cart | 137.31 | 0.00 | 0.00 | 2.69 | 0.87 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
