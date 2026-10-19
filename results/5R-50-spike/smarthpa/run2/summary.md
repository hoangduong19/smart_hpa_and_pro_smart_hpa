# Run report: smarthpa | 5R-50% | run 2

- Started 2026-10-19 13:03:51 - finished 2026-10-19 13:19:21
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 226 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,739.47 |
| CPU Overutilization (%) - lower | 47.16 |
| Overutilization Time (min) - lower | 6.48 |
| CPU Overprovision (m) - lower | 3,109.20 |
| Overprovision Time (min) - higher | 14.98 |
| CPU Underprovision (m) - lower | 0.00 |
| Underprovision Time (min) - lower | 0.00 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 50712 | 0 | 480 | 1300 | 2000 | 56.31 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 573.89 | 11.75 | 3.41 | 346.90 | 11.69 | 0.00 | 0.00 |
| currencyservice | 677.43 | 14.34 | 3.20 | 161.06 | 11.37 | 0.00 | 0.00 |
| cartservice | 283.19 | 5.95 | 2.51 | 373.45 | 10.98 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 244.25 | 4.42 | 0.00 | 0.00 |
| checkoutservice | 134.07 | 1.03 | 0.64 | 365.04 | 14.98 | 0.00 | 0.00 |
| productcatalogservice | 239.82 | 2.54 | 0.98 | 257.52 | 14.98 | 0.00 | 0.00 |
| recommendationservice | 226.55 | 9.83 | 2.92 | 399.12 | 14.22 | 0.00 | 0.00 |
| paymentservice | 134.51 | 1.73 | 0.88 | 297.79 | 12.51 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 122.12 | 3.66 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 261.95 | 14.98 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
