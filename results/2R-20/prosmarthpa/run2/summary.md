# Run report: prosmarthpa | 2R-20% | run 2

- Started 2026-10-08 15:19:33 - finished 2026-10-08 15:35:03
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 417 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,953.00 |
| CPU Overutilization (%) - lower | 451.77 |
| Overutilization Time (min) - lower | 14.49 |
| CPU Overprovision (m) - lower | 85.68 |
| Overprovision Time (min) - higher | 0.50 |
| CPU Underprovision (m) - lower | 6,852.04 |
| Underprovision Time (min) - lower | 14.49 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66234 | 0 | 200 | 720 | 1100 | 73.65 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 553.96 | 79.50 | 14.24 | 6.00 | 0.75 | 1,850.36 | 14.24 |
| currencyservice | 581.06 | 95.11 | 14.49 | 6.95 | 0.50 | 2,543.88 | 14.49 |
| cartservice | 388.01 | 39.03 | 13.01 | 18.23 | 0.75 | 690.65 | 14.24 |
| adservice | 223.50 | 2.07 | 2.01 | 12.95 | 0.37 | 11.03 | 1.22 |
| checkoutservice | 193.53 | 30.35 | 11.99 | 5.52 | 0.67 | 175.30 | 11.99 |
| productcatalogservice | 194.24 | 78.79 | 13.74 | 5.76 | 0.57 | 647.00 | 13.74 |
| recommendationservice | 194.00 | 59.15 | 13.75 | 6.00 | 0.75 | 455.16 | 13.75 |
| paymentservice | 194.24 | 45.72 | 13.93 | 5.76 | 0.57 | 315.59 | 13.93 |
| shippingservice | 170.02 | 16.35 | 10.32 | 6.00 | 0.75 | 139.09 | 12.20 |
| emailservice | 131.18 | 5.20 | 2.98 | 6.00 | 0.75 | 22.30 | 2.85 |
| redis-cart | 129.26 | 0.51 | 0.51 | 6.55 | 1.49 | 1.68 | 0.51 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
