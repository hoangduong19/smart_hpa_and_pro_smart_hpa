# Run report: prosmarthpa-cv-w30 | 2R-20% | run 1

- Started 2026-11-12 23:36:05 - finished 2026-11-12 23:51:35
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 482 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,390.33 |
| CPU Overutilization (%) - lower | 528.16 |
| Overutilization Time (min) - lower | 14.59 |
| CPU Overprovision (m) - lower | 77.55 |
| Overprovision Time (min) - higher | 0.69 |
| CPU Underprovision (m) - lower | 4,437.10 |
| Underprovision Time (min) - lower | 14.28 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 63871 | 0 | 270 | 1000 | 1400 | 71.05 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 568.05 | 65.00 | 14.02 | 11.62 | 0.93 | 1,440.04 | 13.78 |
| currencyservice | 752.28 | 44.20 | 14.53 | 11.20 | 0.69 | 997.93 | 14.28 |
| cartservice | 200.00 | 55.61 | 14.03 | 9.13 | 0.38 | 454.77 | 14.03 |
| adservice | 200.00 | 0.00 | 0.00 | 9.54 | 0.43 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 42.68 | 13.29 | 6.22 | 0.59 | 159.96 | 13.29 |
| productcatalogservice | 100.00 | 124.56 | 14.03 | 4.56 | 0.38 | 581.33 | 14.03 |
| recommendationservice | 100.00 | 90.77 | 13.78 | 4.56 | 0.38 | 413.49 | 13.78 |
| paymentservice | 100.00 | 63.41 | 13.78 | 6.43 | 0.61 | 264.52 | 13.78 |
| shippingservice | 100.00 | 24.72 | 12.31 | 4.56 | 0.38 | 76.56 | 12.31 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.77 | 0.43 | 0.00 | 0.00 |
| redis-cart | 70.00 | 17.22 | 11.29 | 4.94 | 0.73 | 48.51 | 11.29 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
