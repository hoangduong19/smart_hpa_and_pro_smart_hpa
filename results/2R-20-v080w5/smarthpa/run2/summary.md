# Run report: smarthpa | 2R-20% | run 2

- Started 2026-11-20 04:29:23 - finished 2026-11-20 04:44:55
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 465 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,478.97 |
| CPU Overutilization (%) - lower | 494.92 |
| Overutilization Time (min) - lower | 14.57 |
| CPU Overprovision (m) - lower | 55.78 |
| Overprovision Time (min) - higher | 0.66 |
| CPU Underprovision (m) - lower | 4,767.74 |
| Underprovision Time (min) - lower | 14.32 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 75030 | 0 | 220 | 610 | 1100 | 83.40 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 386.45 | 127.31 | 14.57 | 3.66 | 0.40 | 2,188.60 | 14.32 |
| currencyservice | 671.61 | 28.68 | 14.57 | 3.66 | 0.40 | 330.75 | 14.32 |
| cartservice | 200.00 | 75.18 | 14.32 | 10.32 | 0.40 | 643.01 | 14.32 |
| adservice | 200.00 | 2.74 | 1.71 | 7.31 | 0.40 | 18.49 | 1.23 |
| checkoutservice | 195.05 | 34.15 | 14.07 | 4.52 | 0.66 | 190.75 | 13.82 |
| productcatalogservice | 290.97 | 58.45 | 14.57 | 3.66 | 0.40 | 629.25 | 14.30 |
| recommendationservice | 100.00 | 125.89 | 14.32 | 4.30 | 0.48 | 583.66 | 14.32 |
| paymentservice | 100.00 | 0.00 | 0.00 | 4.52 | 0.66 | 0.00 | 0.00 |
| shippingservice | 100.00 | 42.06 | 13.82 | 4.52 | 0.66 | 181.51 | 13.82 |
| emailservice | 100.00 | 0.36 | 0.23 | 4.52 | 0.66 | 1.72 | 0.23 |
| redis-cart | 134.88 | 0.09 | 0.07 | 4.82 | 1.15 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
