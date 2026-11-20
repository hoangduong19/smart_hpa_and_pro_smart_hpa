# Run report: smarthpa-warmup | 2R-20% | run 5

- Started 2026-11-19 20:09:02 - finished 2026-11-19 20:24:34
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 518 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,389.69 |
| CPU Overutilization (%) - lower | 397.43 |
| Overutilization Time (min) - lower | 14.76 |
| CPU Overprovision (m) - lower | 132.74 |
| Overprovision Time (min) - higher | 0.22 |
| CPU Underprovision (m) - lower | 3,409.27 |
| Underprovision Time (min) - lower | 14.76 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 71428 | 0 | 330 | 820 | 1200 | 79.44 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 340.73 | 75.13 | 14.25 | 6.18 | 0.74 | 939.00 | 14.25 |
| currencyservice | 195.95 | 98.98 | 14.76 | 2.12 | 0.22 | 861.58 | 14.76 |
| cartservice | 387.64 | 29.92 | 14.30 | 8.49 | 0.49 | 277.99 | 14.05 |
| adservice | 237.45 | 2.92 | 2.51 | 8.49 | 0.49 | 21.62 | 2.27 |
| checkoutservice | 193.24 | 31.68 | 13.95 | 6.37 | 1.04 | 179.54 | 13.75 |
| productcatalogservice | 193.44 | 53.22 | 14.25 | 6.18 | 0.74 | 377.80 | 14.25 |
| recommendationservice | 193.24 | 65.25 | 14.25 | 6.18 | 0.74 | 502.32 | 14.25 |
| paymentservice | 194.02 | 38.60 | 14.50 | 4.25 | 0.49 | 240.93 | 14.28 |
| shippingservice | 192.66 | 0.09 | 0.05 | 6.95 | 1.49 | 0.00 | 0.00 |
| emailservice | 191.31 | 1.64 | 0.75 | 7.53 | 1.74 | 8.49 | 0.60 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.99 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
