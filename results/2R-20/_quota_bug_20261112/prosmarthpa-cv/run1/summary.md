# Run report: prosmarthpa-cv | 2R-20% | run 1

- Started 2026-11-12 14:33:34 - finished 2026-11-12 14:49:05
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 295 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,817.49 |
| CPU Overutilization (%) - lower | 371.72 |
| Overutilization Time (min) - lower | 14.82 |
| CPU Overprovision (m) - lower | 135.02 |
| Overprovision Time (min) - higher | 0.52 |
| CPU Underprovision (m) - lower | 5,069.83 |
| Underprovision Time (min) - lower | 14.48 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67275 | 0 | 180 | 610 | 980 | 74.79 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 628.81 | 55.05 | 14.24 | 9.49 | 0.76 | 1,308.47 | 13.84 |
| currencyservice | 651.53 | 67.14 | 14.82 | 11.53 | 0.52 | 1,973.22 | 14.48 |
| cartservice | 309.15 | 36.30 | 13.55 | 18.98 | 0.39 | 481.36 | 13.55 |
| adservice | 200.00 | 7.89 | 4.22 | 6.10 | 0.17 | 53.56 | 3.19 |
| checkoutservice | 114.24 | 37.38 | 13.31 | 8.47 | 0.64 | 161.02 | 13.31 |
| productcatalogservice | 168.47 | 69.19 | 14.31 | 6.78 | 0.44 | 499.66 | 14.31 |
| recommendationservice | 188.14 | 44.98 | 13.81 | 6.78 | 0.44 | 325.08 | 13.56 |
| paymentservice | 191.19 | 33.42 | 13.56 | 8.81 | 0.69 | 209.15 | 13.56 |
| shippingservice | 112.54 | 19.80 | 8.05 | 6.78 | 0.44 | 54.24 | 10.25 |
| emailservice | 135.25 | 0.57 | 0.35 | 42.03 | 7.63 | 4.07 | 0.35 |
| redis-cart | 118.17 | 0.00 | 0.00 | 9.25 | 1.31 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
