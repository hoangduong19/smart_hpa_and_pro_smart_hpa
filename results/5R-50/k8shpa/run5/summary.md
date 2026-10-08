# Run report: k8shpa | 5R-50% | run 5

- Started 2026-10-07 13:56:11 - finished 2026-10-07 14:11:41
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 375 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,596.13 |
| CPU Overutilization (%) - lower | 154.55 |
| Overutilization Time (min) - lower | 14.41 |
| CPU Overprovision (m) - lower | 3,618.40 |
| Overprovision Time (min) - higher | 1.94 |
| CPU Underprovision (m) - lower | 366.67 |
| Underprovision Time (min) - lower | 13.04 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 58213 | 0 | 430 | 1500 | 2000 | 64.76 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 450.40 | 81.20 | 14.16 | 39.47 | 2.09 | 362.13 | 12.39 |
| currencyservice | 370.93 | 52.12 | 14.16 | 29.87 | 1.18 | 4.53 | 0.65 |
| cartservice | 345.07 | 3.58 | 1.27 | 657.07 | 14.98 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 800.00 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 179.20 | 1.98 | 0.44 | 317.33 | 14.98 | 0.00 | 0.00 |
| productcatalogservice | 337.33 | 7.33 | 1.88 | 153.60 | 14.98 | 0.00 | 0.00 |
| recommendationservice | 258.13 | 8.18 | 2.29 | 226.40 | 14.98 | 0.00 | 0.00 |
| paymentservice | 185.07 | 0.15 | 0.25 | 314.67 | 14.98 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.98 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.98 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
