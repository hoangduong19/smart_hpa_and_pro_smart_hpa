# Run report: prosmarthpa-cv-w5 | 2R-20% | run 3

- Started 2026-11-13 01:42:59 - finished 2026-11-13 01:58:30
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 446 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,438.23 |
| CPU Overutilization (%) - lower | 399.35 |
| Overutilization Time (min) - lower | 14.72 |
| CPU Overprovision (m) - lower | 116.08 |
| Overprovision Time (min) - higher | 0.51 |
| CPU Underprovision (m) - lower | 4,376.01 |
| Underprovision Time (min) - lower | 14.47 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66098 | 0 | 200 | 660 | 1000 | 73.54 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 283.86 | 114.43 | 14.47 | 6.95 | 0.51 | 1,479.60 | 14.47 |
| currencyservice | 559.87 | 60.07 | 14.72 | 3.36 | 0.26 | 1,249.33 | 14.47 |
| cartservice | 200.00 | 54.60 | 13.47 | 21.97 | 0.58 | 467.71 | 13.47 |
| adservice | 200.00 | 0.00 | 0.00 | 13.90 | 0.51 | 0.00 | 0.00 |
| checkoutservice | 191.70 | 20.52 | 11.71 | 8.30 | 1.02 | 96.19 | 11.71 |
| productcatalogservice | 284.30 | 45.94 | 13.22 | 8.07 | 0.80 | 476.68 | 13.22 |
| recommendationservice | 192.15 | 47.27 | 13.47 | 7.85 | 0.77 | 344.17 | 13.47 |
| paymentservice | 192.15 | 31.17 | 13.22 | 7.85 | 0.77 | 185.43 | 13.22 |
| shippingservice | 100.00 | 25.35 | 12.46 | 7.85 | 0.77 | 76.91 | 12.46 |
| emailservice | 100.00 | 0.00 | 0.00 | 7.85 | 0.77 | 0.00 | 0.00 |
| redis-cart | 134.19 | 0.00 | 0.00 | 22.13 | 3.51 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
