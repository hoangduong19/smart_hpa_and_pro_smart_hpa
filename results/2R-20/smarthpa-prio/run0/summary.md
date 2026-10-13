# Run report: smarthpa-prio | 2R-20% | run 0

- Started 2026-10-13 16:15:09 - finished 2026-10-13 16:18:41
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 100 users, spawn rate 0.67/s, 180 s
- Knowledge Base rows: 66 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,077.58 |
| CPU Overutilization (%) - lower | 233.67 |
| Overutilization Time (min) - lower | 2.48 |
| CPU Overprovision (m) - lower | 374.55 |
| Overprovision Time (min) - higher | 0.71 |
| CPU Underprovision (m) - lower | 1,745.45 |
| Underprovision Time (min) - lower | 2.25 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 4618 | 0 | 210 | 760 | 1200 | 26.16 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 239.39 | 58.32 | 2.48 | 21.21 | 0.48 | 637.88 | 2.25 |
| currencyservice | 509.09 | 30.79 | 2.48 | 21.21 | 0.48 | 310.61 | 2.25 |
| cartservice | 339.39 | 9.59 | 0.98 | 42.42 | 0.48 | 57.58 | 0.74 |
| adservice | 200.00 | 24.11 | 2.25 | 42.42 | 0.48 | 218.18 | 2.25 |
| checkoutservice | 153.03 | 6.00 | 0.57 | 43.94 | 1.46 | 21.21 | 0.49 |
| productcatalogservice | 166.67 | 32.02 | 2.25 | 30.30 | 0.71 | 207.58 | 1.99 |
| recommendationservice | 100.00 | 37.53 | 1.99 | 21.21 | 0.48 | 171.21 | 1.99 |
| paymentservice | 100.00 | 30.30 | 1.99 | 30.30 | 0.71 | 100.00 | 1.99 |
| shippingservice | 100.00 | 5.02 | 0.49 | 21.21 | 0.48 | 21.21 | 0.49 |
| emailservice | 100.00 | 0.00 | 0.00 | 30.30 | 0.71 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 2.96 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
