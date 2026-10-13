# Run report: smarthpa-prio | 2R-20% | run 3

- Started 2026-10-13 17:07:26 - finished 2026-10-13 17:22:56
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 327 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,443.98 |
| CPU Overutilization (%) - lower | 600.68 |
| Overutilization Time (min) - lower | 14.77 |
| CPU Overprovision (m) - lower | 74.68 |
| Overprovision Time (min) - higher | 0.46 |
| CPU Underprovision (m) - lower | 4,919.27 |
| Underprovision Time (min) - lower | 14.52 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 61626 | 0 | 370 | 1000 | 1400 | 68.53 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.50 | 163.20 | 14.52 | 3.98 | 0.46 | 1,472.78 | 14.52 |
| currencyservice | 764.53 | 49.61 | 14.77 | 1.83 | 0.21 | 1,194.19 | 14.52 |
| cartservice | 378.59 | 35.21 | 14.00 | 17.74 | 1.21 | 389.60 | 13.53 |
| adservice | 200.00 | 8.07 | 5.77 | 3.67 | 0.21 | 50.15 | 3.74 |
| checkoutservice | 187.77 | 32.28 | 13.02 | 11.62 | 1.70 | 189.60 | 12.92 |
| productcatalogservice | 193.58 | 73.06 | 14.25 | 5.81 | 0.72 | 577.37 | 14.16 |
| recommendationservice | 100.00 | 132.40 | 14.25 | 3.98 | 0.46 | 620.80 | 14.25 |
| paymentservice | 100.00 | 71.76 | 14.25 | 3.98 | 0.46 | 312.54 | 14.25 |
| shippingservice | 100.00 | 30.03 | 12.52 | 3.98 | 0.46 | 90.52 | 12.52 |
| emailservice | 100.00 | 4.76 | 3.31 | 3.98 | 0.46 | 21.71 | 3.31 |
| redis-cart | 125.02 | 0.28 | 0.17 | 14.13 | 2.96 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
