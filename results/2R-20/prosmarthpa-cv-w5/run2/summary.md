# Run report: prosmarthpa-cv-w5 | 2R-20% | run 2

- Started 2026-11-12 23:57:15 - finished 2026-11-13 00:12:45
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 497 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,464.95 |
| CPU Overutilization (%) - lower | 413.18 |
| Overutilization Time (min) - lower | 14.73 |
| CPU Overprovision (m) - lower | 110.85 |
| Overprovision Time (min) - higher | 0.48 |
| CPU Underprovision (m) - lower | 2,126.56 |
| Underprovision Time (min) - lower | 14.51 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 58777 | 0 | 460 | 1100 | 1300 | 65.38 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 100.00 | 174.65 | 14.47 | 5.23 | 0.48 | 804.43 | 14.47 |
| currencyservice | 946.88 | 21.71 | 14.73 | 7.44 | 0.48 | 112.07 | 14.51 |
| cartservice | 200.00 | 42.90 | 13.74 | 6.04 | 0.26 | 314.29 | 13.74 |
| adservice | 200.00 | 0.00 | 0.00 | 12.07 | 0.26 | 0.00 | 0.00 |
| checkoutservice | 194.16 | 15.63 | 10.97 | 10.26 | 1.21 | 66.80 | 10.97 |
| productcatalogservice | 100.00 | 74.12 | 14.22 | 5.43 | 0.52 | 333.00 | 14.22 |
| recommendationservice | 193.96 | 40.56 | 13.24 | 6.04 | 0.77 | 279.07 | 13.24 |
| paymentservice | 194.16 | 27.89 | 13.43 | 5.84 | 0.57 | 150.10 | 13.43 |
| shippingservice | 100.00 | 15.72 | 10.98 | 5.43 | 0.52 | 66.80 | 10.98 |
| emailservice | 100.00 | 0.00 | 0.00 | 5.23 | 0.48 | 0.00 | 0.00 |
| redis-cart | 135.77 | 0.00 | 0.00 | 41.83 | 8.50 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
