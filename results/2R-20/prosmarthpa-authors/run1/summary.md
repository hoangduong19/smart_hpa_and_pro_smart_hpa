# Run report: prosmarthpa-authors | 2R-20% | run 1

- Started 2026-11-13 03:28:44 - finished 2026-11-13 03:44:14
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 419 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,500.74 |
| CPU Overutilization (%) - lower | 369.26 |
| Overutilization Time (min) - lower | 14.46 |
| CPU Overprovision (m) - lower | 287.85 |
| Overprovision Time (min) - higher | 0.53 |
| CPU Underprovision (m) - lower | 3,401.91 |
| Underprovision Time (min) - lower | 14.46 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62421 | 0 | 300 | 980 | 1400 | 69.44 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 293.79 | 108.07 | 13.96 | 4.06 | 0.53 | 1,380.43 | 13.96 |
| currencyservice | 293.79 | 65.58 | 14.46 | 4.06 | 0.53 | 767.54 | 14.46 |
| cartservice | 393.79 | 24.32 | 12.46 | 18.14 | 1.52 | 230.55 | 12.46 |
| adservice | 393.79 | 0.18 | 0.50 | 198.57 | 14.48 | 1.43 | 0.50 |
| checkoutservice | 100.00 | 42.51 | 13.46 | 2.15 | 0.17 | 161.58 | 13.46 |
| productcatalogservice | 197.14 | 53.97 | 13.46 | 3.82 | 1.03 | 398.81 | 13.46 |
| recommendationservice | 196.90 | 42.44 | 13.22 | 3.82 | 1.03 | 292.60 | 13.22 |
| paymentservice | 196.90 | 32.19 | 13.46 | 5.73 | 0.77 | 168.97 | 13.46 |
| shippingservice | 197.14 | 0.00 | 0.00 | 23.15 | 3.03 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 2.15 | 0.17 | 0.00 | 0.00 |
| redis-cart | 137.49 | 0.00 | 0.00 | 22.22 | 3.92 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
