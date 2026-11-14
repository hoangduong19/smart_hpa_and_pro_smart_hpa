# Run report: prosmarthpa-cv | 2R-20% | run 1

- Started 2026-11-12 20:24:26 - finished 2026-11-12 20:39:56
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 507 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,416.00 |
| CPU Overutilization (%) - lower | 543.52 |
| Overutilization Time (min) - lower | 14.68 |
| CPU Overprovision (m) - lower | 63.98 |
| Overprovision Time (min) - higher | 0.41 |
| CPU Underprovision (m) - lower | 4,376.80 |
| Underprovision Time (min) - lower | 14.59 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65907 | 0 | 210 | 770 | 1100 | 73.26 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 287.97 | 121.30 | 14.68 | 3.75 | 0.32 | 1,573.77 | 14.48 |
| currencyservice | 944.97 | 37.99 | 14.42 | 8.68 | 0.47 | 908.68 | 14.27 |
| cartservice | 200.00 | 54.54 | 13.93 | 9.47 | 0.43 | 441.42 | 13.68 |
| adservice | 200.00 | 1.66 | 1.00 | 7.50 | 0.32 | 11.44 | 1.00 |
| checkoutservice | 100.00 | 47.29 | 13.68 | 5.52 | 0.52 | 186.59 | 13.68 |
| productcatalogservice | 100.00 | 120.45 | 14.41 | 4.73 | 0.43 | 555.82 | 14.41 |
| recommendationservice | 100.00 | 94.99 | 13.93 | 4.73 | 0.43 | 426.43 | 13.93 |
| paymentservice | 194.28 | 30.90 | 13.68 | 5.72 | 0.58 | 169.82 | 13.68 |
| shippingservice | 100.00 | 24.74 | 12.18 | 4.73 | 0.43 | 76.33 | 12.18 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.73 | 0.43 | 0.00 | 0.00 |
| redis-cart | 88.78 | 9.66 | 5.79 | 4.42 | 0.65 | 26.51 | 5.75 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
