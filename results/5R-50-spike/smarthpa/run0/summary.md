# Run report: smarthpa | 5R-50% | run 0

- Started 2026-10-19 11:46:46 - finished 2026-10-19 11:53:17
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 240 s
- Knowledge Base rows: 53 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 1,700.19 |
| CPU Overutilization (%) - lower | 125.42 |
| Overutilization Time (min) - lower | 2.95 |
| CPU Overprovision (m) - lower | 4,161.13 |
| Overprovision Time (min) - higher | 3.90 |
| CPU Underprovision (m) - lower | 0.00 |
| Underprovision Time (min) - lower | 0.00 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 26671 | 3 | 220 | 880 | 1500 | 68.29 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 273.58 | 25.34 | 1.67 | 194.34 | 3.31 | 0.00 | 0.00 |
| currencyservice | 303.77 | 59.11 | 2.37 | 188.68 | 1.72 | 0.00 | 0.00 |
| cartservice | 211.32 | 12.94 | 0.84 | 558.49 | 2.46 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 649.06 | 2.86 | 0.00 | 0.00 |
| checkoutservice | 105.66 | 2.64 | 0.12 | 390.57 | 3.90 | 0.00 | 0.00 |
| productcatalogservice | 124.53 | 9.38 | 0.75 | 362.26 | 3.90 | 0.00 | 0.00 |
| recommendationservice | 107.55 | 8.89 | 0.59 | 377.36 | 3.90 | 0.00 | 0.00 |
| paymentservice | 103.77 | 7.11 | 0.59 | 386.79 | 3.90 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 388.68 | 3.90 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 384.91 | 3.83 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 3.90 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
