# Run report: smarthpa | 2R-20% | run 4

- Started 2026-11-20 07:03:16 - finished 2026-11-20 07:18:47
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 462 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,475.19 |
| CPU Overutilization (%) - lower | 614.86 |
| Overutilization Time (min) - lower | 14.73 |
| CPU Overprovision (m) - lower | 52.16 |
| Overprovision Time (min) - higher | 0.52 |
| CPU Underprovision (m) - lower | 5,348.05 |
| Underprovision Time (min) - lower | 14.47 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73041 | 0 | 270 | 760 | 1300 | 81.22 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 957.79 | 59.23 | 14.73 | 2.16 | 0.26 | 1,948.92 | 14.22 |
| currencyservice | 290.04 | 64.22 | 14.47 | 4.33 | 0.52 | 726.84 | 14.47 |
| cartservice | 200.00 | 78.31 | 14.47 | 4.76 | 0.26 | 670.13 | 14.47 |
| adservice | 200.00 | 13.33 | 8.71 | 8.23 | 0.48 | 103.03 | 7.44 |
| checkoutservice | 195.24 | 35.84 | 14.04 | 4.33 | 0.52 | 205.19 | 13.98 |
| productcatalogservice | 100.00 | 172.52 | 14.47 | 4.11 | 0.48 | 816.45 | 14.47 |
| recommendationservice | 100.00 | 133.57 | 14.47 | 4.11 | 0.48 | 623.59 | 14.47 |
| paymentservice | 100.00 | 0.00 | 0.00 | 4.11 | 0.48 | 0.00 | 0.00 |
| shippingservice | 100.00 | 39.72 | 13.73 | 4.11 | 0.48 | 175.76 | 13.73 |
| emailservice | 100.00 | 18.02 | 11.69 | 4.33 | 0.52 | 78.14 | 11.69 |
| redis-cart | 132.12 | 0.09 | 0.06 | 7.58 | 1.51 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
