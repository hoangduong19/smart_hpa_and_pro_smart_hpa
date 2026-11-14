# Run report: prosmarthpa-cv-w15 | 2R-20% | run 1

- Started 2026-11-12 22:53:35 - finished 2026-11-12 23:09:05
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 472 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,462.67 |
| CPU Overutilization (%) - lower | 413.70 |
| Overutilization Time (min) - lower | 14.57 |
| CPU Overprovision (m) - lower | 99.05 |
| Overprovision Time (min) - higher | 0.40 |
| CPU Underprovision (m) - lower | 4,533.69 |
| Underprovision Time (min) - lower | 14.57 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66768 | 0 | 200 | 680 | 1000 | 74.28 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 287.71 | 115.63 | 14.57 | 5.08 | 0.40 | 1,496.40 | 14.31 |
| currencyservice | 569.49 | 60.76 | 14.57 | 5.08 | 0.40 | 1,292.80 | 14.57 |
| cartservice | 200.00 | 60.68 | 13.82 | 11.44 | 0.47 | 514.41 | 13.82 |
| adservice | 200.00 | 0.00 | 0.00 | 10.17 | 0.40 | 0.00 | 0.00 |
| checkoutservice | 193.64 | 23.12 | 12.07 | 11.44 | 1.41 | 125.00 | 12.07 |
| productcatalogservice | 288.14 | 46.60 | 13.33 | 11.44 | 1.41 | 477.12 | 13.33 |
| recommendationservice | 194.07 | 46.66 | 13.31 | 8.47 | 0.90 | 336.86 | 13.31 |
| paymentservice | 194.07 | 34.19 | 13.58 | 8.47 | 0.90 | 211.44 | 13.58 |
| shippingservice | 100.00 | 26.05 | 12.57 | 5.93 | 0.66 | 79.66 | 12.57 |
| emailservice | 100.00 | 0.00 | 0.00 | 5.93 | 0.66 | 0.00 | 0.00 |
| redis-cart | 135.55 | 0.00 | 0.00 | 15.57 | 2.64 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
