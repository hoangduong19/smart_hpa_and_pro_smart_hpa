# Run report: prosmarthpa-cv-w30 | 2R-20% | run 1

- Started 2026-11-12 16:19:24 - finished 2026-11-12 16:34:57
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 341 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,888.91 |
| CPU Overutilization (%) - lower | 379.02 |
| Overutilization Time (min) - lower | 14.55 |
| CPU Overprovision (m) - lower | 126.77 |
| Overprovision Time (min) - higher | 0.47 |
| CPU Underprovision (m) - lower | 4,655.72 |
| Underprovision Time (min) - lower | 14.44 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66923 | 0 | 190 | 650 | 980 | 74.44 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 422.58 | 74.77 | 14.55 | 5.57 | 0.36 | 1,339.00 | 14.44 |
| currencyservice | 934.31 | 42.85 | 14.55 | 12.61 | 0.62 | 1,522.58 | 14.28 |
| cartservice | 305.57 | 39.61 | 13.55 | 14.08 | 0.36 | 508.50 | 13.55 |
| adservice | 200.00 | 0.00 | 0.00 | 11.14 | 0.36 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 46.79 | 13.29 | 7.04 | 0.62 | 195.31 | 13.29 |
| productcatalogservice | 163.93 | 72.89 | 14.28 | 5.57 | 0.36 | 485.04 | 14.28 |
| recommendationservice | 190.32 | 46.00 | 13.28 | 6.16 | 0.41 | 330.50 | 13.28 |
| paymentservice | 192.96 | 33.54 | 13.79 | 7.04 | 0.62 | 208.50 | 13.79 |
| shippingservice | 109.38 | 22.33 | 8.25 | 5.57 | 0.36 | 65.40 | 10.93 |
| emailservice | 143.40 | 0.25 | 0.26 | 43.99 | 6.60 | 0.88 | 0.26 |
| redis-cart | 126.45 | 0.00 | 0.00 | 8.01 | 1.10 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
