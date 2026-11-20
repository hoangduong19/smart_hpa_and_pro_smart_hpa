# Run report: smarthpa | 2R-20% | run 1

- Started 2026-11-19 08:56:23 - finished 2026-11-19 09:11:53
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 185 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,409.46 |
| CPU Overutilization (%) - lower | 587.46 |
| Overutilization Time (min) - lower | 14.73 |
| CPU Overprovision (m) - lower | 107.84 |
| Overprovision Time (min) - higher | 0.54 |
| CPU Underprovision (m) - lower | 4,237.30 |
| Underprovision Time (min) - lower | 14.42 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 76532 | 0 | 190 | 570 | 1100 | 85.06 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.05 | 141.35 | 14.42 | 3.78 | 0.54 | 1,263.24 | 14.42 |
| currencyservice | 1,051.35 | 38.23 | 14.73 | 1.62 | 0.23 | 936.22 | 14.42 |
| cartservice | 200.00 | 58.08 | 14.19 | 6.49 | 0.23 | 475.68 | 14.19 |
| adservice | 200.00 | 0.00 | 0.00 | 3.24 | 0.23 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 46.36 | 14.19 | 3.78 | 0.54 | 184.86 | 14.19 |
| productcatalogservice | 100.00 | 109.48 | 14.19 | 3.78 | 0.54 | 491.35 | 14.19 |
| recommendationservice | 100.00 | 125.06 | 14.19 | 3.78 | 0.54 | 579.46 | 14.19 |
| paymentservice | 194.05 | 37.23 | 14.42 | 3.78 | 0.54 | 214.59 | 14.11 |
| shippingservice | 100.00 | 31.68 | 13.67 | 3.78 | 0.54 | 91.89 | 13.67 |
| emailservice | 100.00 | 0.00 | 0.00 | 3.78 | 0.54 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.96 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
