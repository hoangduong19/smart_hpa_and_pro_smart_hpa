# Run report: prosmarthpa-authors | 2R-20% | run 4

- Started 2026-11-13 04:32:25 - finished 2026-11-13 04:47:55
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 430 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,501.74 |
| CPU Overutilization (%) - lower | 373.20 |
| Overutilization Time (min) - lower | 14.36 |
| CPU Overprovision (m) - lower | 266.91 |
| Overprovision Time (min) - higher | 0.61 |
| CPU Underprovision (m) - lower | 3,434.19 |
| Underprovision Time (min) - lower | 14.36 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62645 | 0 | 300 | 1000 | 1400 | 69.69 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 293.95 | 108.98 | 14.36 | 3.95 | 0.61 | 1,390.93 | 14.36 |
| currencyservice | 293.95 | 65.74 | 14.36 | 3.95 | 0.61 | 769.30 | 14.36 |
| cartservice | 393.95 | 25.67 | 12.87 | 9.30 | 1.11 | 233.02 | 12.62 |
| adservice | 393.95 | 0.26 | 0.50 | 198.60 | 14.47 | 2.79 | 0.50 |
| checkoutservice | 100.00 | 43.65 | 13.38 | 2.09 | 0.17 | 169.53 | 13.38 |
| productcatalogservice | 197.21 | 53.60 | 13.35 | 3.72 | 1.11 | 394.19 | 13.35 |
| recommendationservice | 196.98 | 43.40 | 13.11 | 3.72 | 1.11 | 299.07 | 13.11 |
| paymentservice | 196.98 | 31.90 | 13.38 | 3.02 | 0.61 | 175.35 | 13.38 |
| shippingservice | 197.21 | 0.00 | 0.00 | 20.00 | 2.84 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 2.09 | 0.17 | 0.00 | 0.00 |
| redis-cart | 137.56 | 0.00 | 0.00 | 16.44 | 2.92 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
