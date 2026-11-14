# Run report: prosmarthpa-cv-w10 | 2R-20% | run 1

- Started 2026-11-12 22:32:27 - finished 2026-11-12 22:47:57
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 473 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,389.66 |
| CPU Overutilization (%) - lower | 495.86 |
| Overutilization Time (min) - lower | 14.69 |
| CPU Overprovision (m) - lower | 89.68 |
| Overprovision Time (min) - higher | 0.51 |
| CPU Underprovision (m) - lower | 5,572.60 |
| Underprovision Time (min) - lower | 14.47 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 68769 | 0 | 150 | 500 | 980 | 76.49 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 284.57 | 121.04 | 14.42 | 5.92 | 0.56 | 1,573.57 | 14.42 |
| currencyservice | 660.04 | 74.73 | 14.69 | 9.09 | 0.51 | 1,959.62 | 14.47 |
| cartservice | 201.27 | 60.70 | 13.67 | 16.91 | 0.63 | 517.12 | 13.67 |
| adservice | 200.00 | 0.00 | 0.00 | 14.38 | 0.29 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 49.41 | 13.17 | 5.92 | 0.56 | 205.07 | 13.17 |
| productcatalogservice | 286.89 | 52.19 | 13.17 | 6.77 | 0.94 | 565.75 | 13.17 |
| recommendationservice | 193.45 | 52.26 | 13.67 | 6.55 | 0.82 | 383.72 | 13.67 |
| paymentservice | 193.45 | 37.81 | 13.17 | 6.55 | 0.82 | 236.79 | 13.17 |
| shippingservice | 100.00 | 28.58 | 12.44 | 6.34 | 0.61 | 80.34 | 12.44 |
| emailservice | 100.00 | 0.00 | 0.00 | 5.92 | 0.56 | 0.00 | 0.00 |
| redis-cart | 70.00 | 19.13 | 11.43 | 5.33 | 0.93 | 50.61 | 11.43 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
