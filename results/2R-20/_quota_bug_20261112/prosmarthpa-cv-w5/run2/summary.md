# Run report: prosmarthpa-cv-w5 | 2R-20% | run 2

- Started 2026-11-12 17:01:41 - finished 2026-11-12 17:17:11
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 320 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,896.88 |
| CPU Overutilization (%) - lower | 344.73 |
| Overutilization Time (min) - lower | 14.65 |
| CPU Overprovision (m) - lower | 128.03 |
| Overprovision Time (min) - higher | 0.32 |
| CPU Underprovision (m) - lower | 4,290.00 |
| Underprovision Time (min) - lower | 14.65 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67659 | 0 | 180 | 550 | 960 | 75.25 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 300.31 | 94.69 | 14.39 | 6.56 | 0.59 | 1,200.94 | 14.39 |
| currencyservice | 840.94 | 44.58 | 14.65 | 5.62 | 0.32 | 1,306.88 | 14.65 |
| cartservice | 308.12 | 37.19 | 13.90 | 20.62 | 0.32 | 468.12 | 13.90 |
| adservice | 200.00 | 0.00 | 0.00 | 11.25 | 0.32 | 0.00 | 0.00 |
| checkoutservice | 193.75 | 25.47 | 12.38 | 8.44 | 0.93 | 221.88 | 13.39 |
| productcatalogservice | 286.88 | 40.10 | 13.16 | 6.56 | 0.59 | 486.88 | 13.64 |
| recommendationservice | 192.81 | 45.51 | 13.40 | 8.44 | 1.10 | 320.94 | 13.40 |
| paymentservice | 193.75 | 36.53 | 13.39 | 6.25 | 0.38 | 225.94 | 13.39 |
| shippingservice | 109.06 | 19.99 | 6.86 | 6.56 | 0.59 | 54.06 | 10.09 |
| emailservice | 135.62 | 0.68 | 0.32 | 25.62 | 4.01 | 4.38 | 0.32 |
| redis-cart | 135.62 | 0.00 | 0.00 | 22.09 | 3.08 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
