# Run report: smarthpa | 2R-20% | run 7

- Started 2026-11-20 09:44:10 - finished 2026-11-20 09:59:41
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 485 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,457.77 |
| CPU Overutilization (%) - lower | 627.68 |
| Overutilization Time (min) - lower | 14.64 |
| CPU Overprovision (m) - lower | 59.53 |
| Overprovision Time (min) - higher | 0.59 |
| CPU Underprovision (m) - lower | 4,579.65 |
| Underprovision Time (min) - lower | 14.41 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73856 | 0 | 230 | 750 | 1200 | 82.13 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 384.54 | 116.95 | 14.64 | 3.30 | 0.36 | 1,968.66 | 14.41 |
| currencyservice | 942.47 | 19.20 | 12.13 | 3.30 | 0.36 | 104.95 | 11.91 |
| cartservice | 200.00 | 68.23 | 14.13 | 6.60 | 0.36 | 582.27 | 14.13 |
| adservice | 200.00 | 7.44 | 5.05 | 6.60 | 0.36 | 45.77 | 3.48 |
| checkoutservice | 100.00 | 73.45 | 14.13 | 5.15 | 0.59 | 314.02 | 14.13 |
| productcatalogservice | 100.00 | 163.99 | 14.38 | 5.15 | 0.59 | 764.95 | 14.38 |
| recommendationservice | 100.00 | 131.95 | 14.38 | 5.15 | 0.59 | 612.58 | 14.38 |
| paymentservice | 100.00 | 0.00 | 0.00 | 5.15 | 0.59 | 0.00 | 0.00 |
| shippingservice | 100.00 | 38.22 | 14.13 | 5.15 | 0.59 | 149.07 | 14.13 |
| emailservice | 100.00 | 7.73 | 5.40 | 5.15 | 0.59 | 36.08 | 5.40 |
| redis-cart | 130.76 | 0.53 | 0.50 | 8.80 | 1.60 | 1.30 | 0.41 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
