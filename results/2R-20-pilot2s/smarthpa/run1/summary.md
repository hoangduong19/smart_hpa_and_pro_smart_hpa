# Run report: smarthpa | 2R-20% | run 1

- Started 2026-11-19 07:55:04 - finished 2026-11-19 08:10:36
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 462 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,471.80 |
| CPU Overutilization (%) - lower | 526.40 |
| Overutilization Time (min) - lower | 14.68 |
| CPU Overprovision (m) - lower | 53.59 |
| Overprovision Time (min) - higher | 0.57 |
| CPU Underprovision (m) - lower | 4,610.61 |
| Underprovision Time (min) - lower | 14.43 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65460 | 0 | 460 | 1400 | 2100 | 72.78 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 485.28 | 90.92 | 14.68 | 2.81 | 0.31 | 1,810.17 | 14.43 |
| currencyservice | 672.73 | 31.76 | 14.68 | 2.81 | 0.31 | 439.83 | 14.43 |
| cartservice | 200.00 | 68.61 | 14.43 | 5.63 | 0.31 | 595.67 | 14.43 |
| adservice | 200.00 | 1.67 | 1.23 | 5.63 | 0.31 | 12.55 | 1.00 |
| checkoutservice | 100.00 | 55.04 | 14.18 | 3.68 | 0.57 | 225.11 | 14.18 |
| productcatalogservice | 196.54 | 77.87 | 14.25 | 2.81 | 0.31 | 630.09 | 14.18 |
| recommendationservice | 100.00 | 131.61 | 14.43 | 2.81 | 0.31 | 605.19 | 14.43 |
| paymentservice | 194.37 | 33.19 | 14.43 | 3.68 | 0.57 | 176.84 | 14.18 |
| shippingservice | 100.00 | 35.13 | 13.94 | 3.68 | 0.57 | 113.42 | 13.94 |
| emailservice | 100.00 | 0.36 | 0.28 | 3.68 | 0.57 | 1.73 | 0.28 |
| redis-cart | 122.88 | 0.23 | 0.16 | 16.36 | 3.07 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
