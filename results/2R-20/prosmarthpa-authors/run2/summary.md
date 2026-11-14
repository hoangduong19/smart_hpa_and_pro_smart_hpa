# Run report: prosmarthpa-authors | 2R-20% | run 2

- Started 2026-11-13 03:49:58 - finished 2026-11-13 04:05:28
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 425 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,504.28 |
| CPU Overutilization (%) - lower | 376.30 |
| Overutilization Time (min) - lower | 14.41 |
| CPU Overprovision (m) - lower | 264.24 |
| Overprovision Time (min) - higher | 0.56 |
| CPU Underprovision (m) - lower | 3,470.82 |
| Underprovision Time (min) - lower | 14.41 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62989 | 0 | 300 | 990 | 1400 | 70.09 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 294.35 | 108.73 | 13.91 | 3.53 | 0.56 | 1,383.06 | 13.91 |
| currencyservice | 294.35 | 65.82 | 14.41 | 3.53 | 0.56 | 774.82 | 14.41 |
| cartservice | 394.35 | 26.62 | 12.66 | 5.65 | 0.56 | 266.82 | 12.16 |
| adservice | 394.35 | 0.30 | 0.50 | 198.59 | 14.22 | 4.24 | 0.50 |
| checkoutservice | 100.00 | 44.66 | 13.41 | 2.12 | 0.17 | 166.82 | 13.41 |
| productcatalogservice | 197.41 | 53.94 | 13.41 | 2.59 | 0.22 | 393.41 | 13.41 |
| recommendationservice | 197.18 | 43.49 | 13.66 | 2.82 | 0.56 | 304.47 | 13.66 |
| paymentservice | 197.18 | 32.72 | 13.41 | 2.82 | 0.56 | 177.18 | 13.41 |
| shippingservice | 197.41 | 0.00 | 0.00 | 22.35 | 3.05 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 2.12 | 0.17 | 0.00 | 0.00 |
| redis-cart | 137.69 | 0.00 | 0.00 | 18.12 | 3.16 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
