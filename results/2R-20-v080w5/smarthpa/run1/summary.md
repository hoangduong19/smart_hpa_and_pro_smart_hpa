# Run report: smarthpa | 2R-20% | run 1

- Started 2026-11-20 03:35:45 - finished 2026-11-20 03:51:15
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 493 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,455.44 |
| CPU Overutilization (%) - lower | 651.70 |
| Overutilization Time (min) - lower | 14.68 |
| CPU Overprovision (m) - lower | 59.51 |
| Overprovision Time (min) - higher | 0.51 |
| CPU Underprovision (m) - lower | 4,976.06 |
| Underprovision Time (min) - lower | 14.46 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 76648 | 0 | 170 | 580 | 1200 | 85.27 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 383.98 | 125.08 | 14.68 | 2.64 | 0.28 | 2,126.77 | 14.46 |
| currencyservice | 943.81 | 26.54 | 14.68 | 2.64 | 0.28 | 309.13 | 14.21 |
| cartservice | 200.00 | 73.04 | 14.42 | 5.27 | 0.28 | 611.76 | 14.42 |
| adservice | 200.00 | 1.98 | 1.43 | 9.33 | 0.51 | 9.33 | 0.74 |
| checkoutservice | 100.00 | 64.70 | 14.17 | 4.67 | 0.51 | 265.92 | 14.17 |
| productcatalogservice | 100.00 | 153.13 | 14.42 | 4.67 | 0.51 | 708.32 | 14.42 |
| recommendationservice | 100.00 | 144.60 | 14.42 | 4.67 | 0.51 | 680.53 | 14.42 |
| paymentservice | 100.00 | 1.02 | 0.77 | 4.67 | 0.51 | 4.87 | 0.77 |
| shippingservice | 100.00 | 42.12 | 13.93 | 4.67 | 0.51 | 176.88 | 13.93 |
| emailservice | 100.00 | 19.26 | 12.73 | 4.67 | 0.51 | 82.56 | 12.73 |
| redis-cart | 127.65 | 0.23 | 0.14 | 11.64 | 2.04 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
