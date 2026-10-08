# Run report: smarthpa | 5R-50% | run 3

- Started 2026-10-05 08:44:41 - finished 2026-10-05 09:00:17
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 293 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,582.29 |
| CPU Overutilization (%) - lower | 159.61 |
| Overutilization Time (min) - lower | 14.13 |
| CPU Overprovision (m) - lower | 773.24 |
| Overprovision Time (min) - higher | 4.79 |
| CPU Underprovision (m) - lower | 418.09 |
| Underprovision Time (min) - lower | 10.20 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 64706 | 44 | 210 | 760 | 1600 | 72.18 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 670.65 | 56.13 | 12.96 | 54.27 | 2.50 | 208.87 | 10.14 |
| currencyservice | 1,118.77 | 29.61 | 7.74 | 60.41 | 3.02 | 84.30 | 5.01 |
| cartservice | 357.68 | 4.33 | 1.78 | 66.21 | 0.99 | 8.19 | 0.77 |
| adservice | 200.00 | 2.30 | 0.50 | 76.45 | 0.99 | 4.10 | 0.24 |
| checkoutservice | 181.57 | 12.65 | 3.36 | 87.37 | 3.76 | 21.84 | 2.71 |
| productcatalogservice | 340.27 | 8.71 | 2.27 | 79.18 | 4.01 | 16.04 | 1.47 |
| recommendationservice | 260.41 | 39.56 | 9.87 | 48.81 | 1.86 | 66.89 | 8.50 |
| paymentservice | 182.94 | 6.32 | 2.21 | 77.47 | 3.27 | 7.85 | 0.96 |
| shippingservice | 100.00 | 0.00 | 0.00 | 82.59 | 3.04 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 76.45 | 2.50 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 64.03 | 3.78 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
