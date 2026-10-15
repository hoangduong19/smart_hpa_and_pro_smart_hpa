# Run report: smarthpa-prio | 5R-50% | run 4

- Started 2026-10-15 14:22:17 - finished 2026-10-15 14:37:51
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 167 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,883.77 |
| CPU Overutilization (%) - lower | 76.84 |
| Overutilization Time (min) - lower | 9.94 |
| CPU Overprovision (m) - lower | 2,304.43 |
| Overprovision Time (min) - higher | 14.75 |
| CPU Underprovision (m) - lower | 1.20 |
| Underprovision Time (min) - lower | 0.23 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 63765 | 13 | 190 | 770 | 4200 | 70.95 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 877.25 | 23.16 | 6.65 | 171.26 | 9.18 | 0.00 | 0.00 |
| currencyservice | 1,226.95 | 23.53 | 5.56 | 187.43 | 10.71 | 0.00 | 0.00 |
| cartservice | 359.28 | 7.04 | 2.54 | 568.86 | 14.98 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 160.48 | 2.70 | 0.00 | 0.00 |
| checkoutservice | 179.04 | 3.51 | 1.77 | 305.99 | 14.75 | 0.00 | 0.00 |
| productcatalogservice | 334.73 | 3.89 | 0.86 | 161.68 | 10.33 | 0.00 | 0.00 |
| recommendationservice | 255.09 | 9.98 | 2.97 | 194.61 | 11.88 | 1.20 | 0.23 |
| paymentservice | 173.05 | 3.88 | 1.53 | 132.34 | 4.93 | 0.00 | 0.00 |
| shippingservice | 108.38 | 1.86 | 0.53 | 128.74 | 3.93 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 141.32 | 4.22 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 151.74 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
