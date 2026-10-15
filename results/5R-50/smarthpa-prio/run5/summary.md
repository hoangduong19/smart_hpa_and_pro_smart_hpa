# Run report: smarthpa-prio | 5R-50% | run 5

- Started 2026-10-15 15:04:50 - finished 2026-10-15 15:20:35
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 162 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,912.59 |
| CPU Overutilization (%) - lower | 72.05 |
| Overutilization Time (min) - lower | 9.75 |
| CPU Overprovision (m) - lower | 2,287.96 |
| Overprovision Time (min) - higher | 14.98 |
| CPU Underprovision (m) - lower | 0.00 |
| Underprovision Time (min) - lower | 0.00 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66944 | 0 | 190 | 710 | 1100 | 74.49 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 909.26 | 23.30 | 6.46 | 176.54 | 10.77 | 0.00 | 0.00 |
| currencyservice | 1,265.43 | 24.93 | 6.53 | 129.01 | 10.15 | 0.00 | 0.00 |
| cartservice | 338.27 | 4.74 | 1.78 | 553.09 | 14.98 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 202.47 | 3.15 | 0.00 | 0.00 |
| checkoutservice | 175.93 | 3.18 | 1.19 | 316.67 | 14.98 | 0.00 | 0.00 |
| productcatalogservice | 327.78 | 5.22 | 1.85 | 166.67 | 10.94 | 0.00 | 0.00 |
| recommendationservice | 250.62 | 8.05 | 3.38 | 177.78 | 10.10 | 0.00 | 0.00 |
| paymentservice | 170.37 | 0.74 | 0.49 | 142.59 | 5.10 | 0.00 | 0.00 |
| shippingservice | 104.94 | 1.90 | 0.58 | 129.63 | 3.90 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 135.80 | 3.90 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 157.72 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
