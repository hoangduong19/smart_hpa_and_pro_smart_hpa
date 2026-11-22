# Run report: prosmarthpa-authors | 2R-20% | run 1

- Started 2026-11-22 03:23:02 - finished 2026-11-22 03:38:33
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 440 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,503.59 |
| CPU Overutilization (%) - lower | 486.49 |
| Overutilization Time (min) - lower | 14.41 |
| CPU Overprovision (m) - lower | 218.23 |
| Overprovision Time (min) - higher | 0.57 |
| CPU Underprovision (m) - lower | 4,485.45 |
| Underprovision Time (min) - lower | 14.41 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 71105 | 0 | 310 | 900 | 1300 | 79.08 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 294.55 | 133.61 | 14.19 | 3.41 | 0.57 | 1,757.95 | 14.19 |
| currencyservice | 197.27 | 98.17 | 14.41 | 2.73 | 0.57 | 865.91 | 14.41 |
| cartservice | 394.55 | 27.60 | 13.94 | 6.82 | 0.57 | 240.45 | 13.94 |
| adservice | 394.55 | 0.39 | 0.23 | 185.91 | 13.75 | 5.45 | 0.23 |
| checkoutservice | 197.50 | 35.87 | 13.91 | 2.50 | 0.26 | 197.05 | 13.91 |
| productcatalogservice | 197.50 | 72.14 | 14.19 | 2.50 | 0.26 | 567.50 | 14.19 |
| recommendationservice | 197.27 | 72.68 | 14.41 | 2.73 | 0.57 | 577.05 | 14.41 |
| paymentservice | 197.27 | 39.32 | 14.41 | 2.73 | 0.57 | 242.95 | 14.41 |
| shippingservice | 195.68 | 0.00 | 0.00 | 4.32 | 1.13 | 0.00 | 0.00 |
| emailservice | 100.00 | 6.71 | 4.52 | 2.05 | 0.18 | 31.14 | 4.52 |
| redis-cart | 137.45 | 0.00 | 0.00 | 2.55 | 0.83 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
