# Run report: smarthpa-warmup | 2R-20% | run 7

- Started 2026-11-19 21:36:15 - finished 2026-11-19 21:51:46
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 498 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,454.58 |
| CPU Overutilization (%) - lower | 427.65 |
| Overutilization Time (min) - lower | 14.70 |
| CPU Overprovision (m) - lower | 70.94 |
| Overprovision Time (min) - higher | 0.27 |
| CPU Underprovision (m) - lower | 3,848.80 |
| Underprovision Time (min) - lower | 14.70 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69717 | 0 | 370 | 1000 | 1500 | 77.52 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 361.85 | 85.70 | 14.45 | 4.82 | 0.52 | 1,167.67 | 14.45 |
| currencyservice | 195.38 | 99.65 | 14.70 | 2.61 | 0.27 | 865.86 | 14.70 |
| cartservice | 388.76 | 30.36 | 14.25 | 9.64 | 0.52 | 295.18 | 13.70 |
| adservice | 230.92 | 8.06 | 5.22 | 9.64 | 0.52 | 63.86 | 4.70 |
| checkoutservice | 193.98 | 31.58 | 14.20 | 5.62 | 0.77 | 171.08 | 13.87 |
| productcatalogservice | 194.58 | 67.25 | 14.45 | 4.82 | 0.52 | 527.51 | 14.37 |
| recommendationservice | 193.78 | 66.98 | 14.20 | 5.62 | 0.77 | 533.13 | 13.90 |
| paymentservice | 194.38 | 37.27 | 14.45 | 4.82 | 0.52 | 222.89 | 14.20 |
| shippingservice | 193.37 | 0.09 | 0.05 | 6.22 | 1.27 | 0.00 | 0.00 |
| emailservice | 176.31 | 0.51 | 0.51 | 8.84 | 1.76 | 1.61 | 0.35 |
| redis-cart | 131.29 | 0.20 | 0.11 | 8.29 | 2.24 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
