# Run report: smarthpa-flat | 5R-50% | run 2

- Started 2026-10-15 14:43:35 - finished 2026-10-15 14:59:09
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 164 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 4,317.56 |
| CPU Overutilization (%) - lower | 79.31 |
| Overutilization Time (min) - lower | 11.64 |
| CPU Overprovision (m) - lower | 1,839.57 |
| Overprovision Time (min) - higher | 14.50 |
| CPU Underprovision (m) - lower | 6.10 |
| Underprovision Time (min) - lower | 0.49 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67935 | 0 | 170 | 560 | 980 | 75.58 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 944.51 | 23.57 | 7.29 | 137.80 | 8.94 | 0.00 | 0.00 |
| currencyservice | 1,470.12 | 28.31 | 7.20 | 116.46 | 8.66 | 5.49 | 0.49 |
| cartservice | 398.78 | 10.18 | 3.08 | 167.07 | 2.61 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 223.17 | 2.48 | 0.00 | 0.00 |
| checkoutservice | 177.44 | 3.74 | 1.40 | 195.12 | 9.06 | 0.61 | 0.25 |
| productcatalogservice | 364.02 | 4.57 | 1.66 | 130.49 | 5.56 | 0.00 | 0.00 |
| recommendationservice | 287.20 | 4.68 | 2.25 | 202.44 | 13.64 | 0.00 | 0.00 |
| paymentservice | 168.29 | 1.06 | 0.49 | 146.95 | 4.64 | 0.00 | 0.00 |
| shippingservice | 137.20 | 3.20 | 1.28 | 140.85 | 4.10 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 145.73 | 4.16 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 233.48 | 14.99 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
