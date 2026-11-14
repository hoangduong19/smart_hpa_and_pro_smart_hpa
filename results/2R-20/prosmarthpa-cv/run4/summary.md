# Run report: prosmarthpa-cv | 2R-20% | run 4

- Started 2026-11-12 21:27:55 - finished 2026-11-12 21:43:25
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 522 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,408.31 |
| CPU Overutilization (%) - lower | 438.00 |
| Overutilization Time (min) - lower | 14.65 |
| CPU Overprovision (m) - lower | 67.22 |
| Overprovision Time (min) - higher | 0.60 |
| CPU Underprovision (m) - lower | 4,320.92 |
| Underprovision Time (min) - lower | 14.40 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66489 | 0 | 190 | 750 | 1100 | 74.00 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 290.04 | 108.65 | 14.40 | 4.79 | 0.60 | 1,383.14 | 14.15 |
| currencyservice | 667.82 | 51.32 | 14.65 | 5.56 | 0.60 | 1,136.21 | 14.40 |
| cartservice | 200.00 | 55.38 | 13.65 | 9.20 | 0.41 | 472.41 | 13.65 |
| adservice | 200.00 | 0.00 | 0.00 | 8.05 | 0.34 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 49.07 | 13.42 | 5.17 | 0.85 | 208.05 | 13.42 |
| productcatalogservice | 290.42 | 42.30 | 13.42 | 9.58 | 1.35 | 410.54 | 13.42 |
| recommendationservice | 195.21 | 49.69 | 13.66 | 6.90 | 0.85 | 357.47 | 13.66 |
| paymentservice | 194.83 | 36.55 | 14.15 | 4.79 | 0.60 | 222.99 | 13.90 |
| shippingservice | 100.00 | 26.78 | 12.40 | 4.79 | 0.60 | 79.69 | 12.40 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.79 | 0.60 | 0.00 | 0.00 |
| redis-cart | 70.00 | 18.26 | 11.41 | 3.62 | 0.85 | 50.42 | 11.41 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
