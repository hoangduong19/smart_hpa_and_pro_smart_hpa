# Run report: smarthpa | 2R-20% | run 8

- Started 2026-11-20 10:37:52 - finished 2026-11-20 10:53:24
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 482 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,372.74 |
| CPU Overutilization (%) - lower | 479.28 |
| Overutilization Time (min) - lower | 14.56 |
| CPU Overprovision (m) - lower | 64.27 |
| Overprovision Time (min) - higher | 0.67 |
| CPU Underprovision (m) - lower | 4,581.54 |
| Underprovision Time (min) - lower | 14.31 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 74240 | 0 | 220 | 680 | 1100 | 82.53 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 385.06 | 110.98 | 14.56 | 4.15 | 0.42 | 1,859.13 | 14.31 |
| currencyservice | 479.25 | 39.61 | 14.56 | 4.15 | 0.42 | 559.34 | 14.31 |
| cartservice | 200.00 | 75.73 | 14.31 | 8.30 | 0.42 | 655.60 | 14.31 |
| adservice | 200.00 | 2.68 | 2.01 | 8.30 | 0.42 | 10.79 | 0.99 |
| checkoutservice | 194.61 | 37.06 | 14.31 | 4.98 | 0.67 | 222.61 | 14.06 |
| productcatalogservice | 384.85 | 41.91 | 14.09 | 4.15 | 0.42 | 503.53 | 13.82 |
| recommendationservice | 100.00 | 130.02 | 14.31 | 4.77 | 0.50 | 604.15 | 14.31 |
| paymentservice | 100.00 | 0.00 | 0.00 | 4.98 | 0.67 | 0.00 | 0.00 |
| shippingservice | 100.00 | 37.57 | 13.82 | 4.77 | 0.50 | 149.59 | 13.82 |
| emailservice | 100.00 | 3.61 | 2.61 | 4.98 | 0.67 | 16.80 | 2.61 |
| redis-cart | 128.96 | 0.09 | 0.06 | 10.75 | 2.16 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
