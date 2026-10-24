# Run report: prosmarthpa-authors | 2R-20% | run 2

- Started 2026-10-24 10:58:50 - finished 2026-10-24 11:14:20
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 394 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,693.58 |
| CPU Overutilization (%) - lower | 502.19 |
| Overutilization Time (min) - lower | 14.82 |
| CPU Overprovision (m) - lower | 172.01 |
| Overprovision Time (min) - higher | 0.41 |
| CPU Underprovision (m) - lower | 5,399.75 |
| Underprovision Time (min) - lower | 14.57 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67221 | 0 | 190 | 670 | 970 | 74.76 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 292.64 | 125.38 | 14.55 | 2.79 | 0.43 | 1,689.34 | 14.55 |
| currencyservice | 294.42 | 123.56 | 14.82 | 1.78 | 0.16 | 1,696.45 | 14.57 |
| cartservice | 394.42 | 33.97 | 13.80 | 9.14 | 0.43 | 379.70 | 13.80 |
| adservice | 394.42 | 0.82 | 0.48 | 88.32 | 7.18 | 6.60 | 0.48 |
| checkoutservice | 197.21 | 28.54 | 12.55 | 4.57 | 1.18 | 153.81 | 12.55 |
| productcatalogservice | 197.46 | 86.28 | 13.80 | 3.05 | 0.76 | 713.96 | 13.80 |
| recommendationservice | 197.21 | 59.02 | 13.64 | 4.31 | 0.84 | 450.51 | 13.64 |
| paymentservice | 197.21 | 41.26 | 13.88 | 2.79 | 0.43 | 266.24 | 13.88 |
| shippingservice | 197.46 | 2.72 | 2.06 | 13.45 | 2.17 | 12.94 | 2.06 |
| emailservice | 194.16 | 0.61 | 0.36 | 32.74 | 3.80 | 30.20 | 4.92 |
| redis-cart | 136.98 | 0.00 | 0.00 | 9.06 | 1.30 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
