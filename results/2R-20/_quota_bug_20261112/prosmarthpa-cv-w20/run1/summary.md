# Run report: prosmarthpa-cv-w20 | 2R-20% | run 1

- Started 2026-11-12 15:58:14 - finished 2026-11-12 16:13:44
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 316 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,126.01 |
| CPU Overutilization (%) - lower | 352.84 |
| Overutilization Time (min) - lower | 14.71 |
| CPU Overprovision (m) - lower | 121.65 |
| Overprovision Time (min) - higher | 0.78 |
| CPU Underprovision (m) - lower | 5,937.97 |
| Underprovision Time (min) - lower | 14.20 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67639 | 0 | 190 | 660 | 1100 | 75.24 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 619.62 | 60.29 | 14.71 | 5.06 | 0.28 | 1,440.51 | 14.20 |
| currencyservice | 734.18 | 69.36 | 14.71 | 5.70 | 0.61 | 2,454.43 | 14.20 |
| cartservice | 319.62 | 38.13 | 13.95 | 16.46 | 0.46 | 514.56 | 13.95 |
| adservice | 200.00 | 0.78 | 0.50 | 16.46 | 0.46 | 0.00 | 0.00 |
| checkoutservice | 190.82 | 24.62 | 11.95 | 9.18 | 1.04 | 222.78 | 13.45 |
| productcatalogservice | 282.91 | 50.70 | 13.45 | 8.86 | 1.01 | 626.27 | 13.45 |
| recommendationservice | 188.92 | 49.03 | 13.20 | 8.86 | 0.88 | 357.28 | 13.20 |
| paymentservice | 190.82 | 38.86 | 14.20 | 8.54 | 0.78 | 250.95 | 13.95 |
| shippingservice | 136.39 | 19.64 | 10.35 | 8.54 | 0.78 | 62.97 | 10.39 |
| emailservice | 137.34 | 1.41 | 0.59 | 22.47 | 3.41 | 8.23 | 0.59 |
| redis-cart | 125.38 | 0.00 | 0.00 | 11.52 | 1.60 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
