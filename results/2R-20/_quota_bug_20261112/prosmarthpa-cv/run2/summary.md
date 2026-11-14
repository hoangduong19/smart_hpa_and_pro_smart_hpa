# Run report: prosmarthpa-cv | 2R-20% | run 2

- Started 2026-11-12 16:40:31 - finished 2026-11-12 16:56:02
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 294 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,999.08 |
| CPU Overutilization (%) - lower | 374.75 |
| Overutilization Time (min) - lower | 14.76 |
| CPU Overprovision (m) - lower | 152.31 |
| Overprovision Time (min) - higher | 0.50 |
| CPU Underprovision (m) - lower | 5,059.18 |
| Underprovision Time (min) - lower | 14.50 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67349 | 0 | 190 | 630 | 980 | 74.89 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 347.62 | 93.09 | 14.50 | 8.50 | 0.50 | 1,540.82 | 14.50 |
| currencyservice | 1,004.08 | 43.45 | 14.76 | 6.80 | 0.54 | 1,643.88 | 14.25 |
| cartservice | 312.93 | 38.28 | 13.75 | 16.33 | 0.44 | 489.80 | 13.75 |
| adservice | 200.00 | 0.00 | 0.00 | 25.17 | 0.44 | 0.00 | 0.00 |
| checkoutservice | 189.80 | 22.32 | 12.02 | 9.86 | 0.84 | 204.76 | 13.25 |
| productcatalogservice | 179.25 | 70.41 | 14.25 | 8.16 | 0.44 | 540.48 | 14.25 |
| recommendationservice | 187.76 | 48.35 | 13.75 | 8.16 | 0.44 | 347.96 | 13.62 |
| paymentservice | 189.46 | 36.29 | 13.25 | 9.86 | 0.84 | 226.53 | 13.25 |
| shippingservice | 114.97 | 22.00 | 8.30 | 8.16 | 0.44 | 61.90 | 10.63 |
| emailservice | 142.52 | 0.56 | 0.50 | 38.44 | 5.17 | 3.06 | 0.50 |
| redis-cart | 130.71 | 0.00 | 0.00 | 12.86 | 1.93 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
