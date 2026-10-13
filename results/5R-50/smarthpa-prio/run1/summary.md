# Run report: smarthpa-prio | 5R-50% | run 1

- Started 2026-10-13 17:28:35 - finished 2026-10-13 17:44:05
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 223 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 4,379.42 |
| CPU Overutilization (%) - lower | 71.10 |
| Overutilization Time (min) - lower | 10.36 |
| CPU Overprovision (m) - lower | 1,800.99 |
| Overprovision Time (min) - higher | 14.66 |
| CPU Underprovision (m) - lower | 0.90 |
| Underprovision Time (min) - lower | 0.25 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65934 | 1 | 200 | 780 | 1200 | 73.38 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 1,018.83 | 20.37 | 5.60 | 117.49 | 7.89 | 0.00 | 0.00 |
| currencyservice | 1,436.32 | 26.30 | 5.84 | 223.77 | 11.39 | 0.90 | 0.25 |
| cartservice | 392.83 | 10.85 | 2.77 | 326.46 | 9.07 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 144.39 | 2.81 | 0.00 | 0.00 |
| checkoutservice | 171.30 | 0.99 | 0.36 | 294.17 | 14.90 | 0.00 | 0.00 |
| productcatalogservice | 383.86 | 4.26 | 1.29 | 110.31 | 5.73 | 0.00 | 0.00 |
| recommendationservice | 321.52 | 2.25 | 1.03 | 117.94 | 5.71 | 0.00 | 0.00 |
| paymentservice | 184.75 | 6.08 | 2.02 | 108.97 | 4.33 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 107.62 | 3.07 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 113.00 | 3.07 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 136.86 | 14.90 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
