# Run report: prosmarthpa-cv | 2R-20% | run 2

- Started 2026-11-12 20:45:36 - finished 2026-11-12 21:01:06
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 503 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,404.19 |
| CPU Overutilization (%) - lower | 455.74 |
| Overutilization Time (min) - lower | 14.57 |
| CPU Overprovision (m) - lower | 68.17 |
| Overprovision Time (min) - higher | 0.41 |
| CPU Underprovision (m) - lower | 4,430.48 |
| Underprovision Time (min) - lower | 14.57 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66151 | 0 | 200 | 740 | 1100 | 73.56 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 287.67 | 116.25 | 14.57 | 4.77 | 0.41 | 1,494.83 | 14.57 |
| currencyservice | 762.43 | 45.23 | 14.57 | 5.57 | 0.65 | 1,059.44 | 14.33 |
| cartservice | 200.00 | 60.24 | 13.56 | 13.52 | 0.43 | 516.90 | 13.56 |
| adservice | 200.00 | 0.00 | 0.00 | 9.54 | 0.41 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 48.21 | 13.56 | 5.17 | 0.45 | 199.40 | 13.56 |
| productcatalogservice | 194.83 | 58.29 | 13.82 | 5.17 | 0.45 | 446.72 | 13.82 |
| recommendationservice | 194.63 | 49.93 | 13.57 | 5.37 | 0.67 | 361.83 | 13.57 |
| paymentservice | 194.63 | 35.55 | 13.81 | 5.37 | 0.67 | 227.04 | 13.81 |
| shippingservice | 100.00 | 24.79 | 12.32 | 4.97 | 0.43 | 77.14 | 12.32 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.97 | 0.43 | 0.00 | 0.00 |
| redis-cart | 70.00 | 17.27 | 11.07 | 3.76 | 0.67 | 47.18 | 11.07 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
