# Run report: prosmarthpa-authors | 2R-20% | run 7

- Started 2026-11-22 06:04:06 - finished 2026-11-22 06:19:38
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 413 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,501.21 |
| CPU Overutilization (%) - lower | 491.73 |
| Overutilization Time (min) - lower | 14.74 |
| CPU Overprovision (m) - lower | 221.11 |
| Overprovision Time (min) - higher | 0.25 |
| CPU Underprovision (m) - lower | 4,498.06 |
| Underprovision Time (min) - lower | 14.74 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 68407 | 0 | 390 | 1100 | 1800 | 76.03 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 294.19 | 133.09 | 14.47 | 3.63 | 0.52 | 1,741.89 | 14.47 |
| currencyservice | 197.09 | 98.04 | 14.74 | 2.66 | 0.25 | 862.23 | 14.47 |
| cartservice | 394.19 | 29.09 | 14.22 | 11.14 | 0.52 | 266.34 | 13.98 |
| adservice | 394.19 | 0.21 | 0.25 | 183.54 | 13.23 | 2.91 | 0.25 |
| checkoutservice | 197.34 | 35.62 | 13.98 | 2.66 | 0.25 | 191.04 | 13.98 |
| productcatalogservice | 197.34 | 81.36 | 14.74 | 2.66 | 0.25 | 662.71 | 14.74 |
| recommendationservice | 197.09 | 64.79 | 13.98 | 2.91 | 0.52 | 496.13 | 13.98 |
| paymentservice | 197.09 | 38.08 | 14.22 | 2.91 | 0.52 | 222.76 | 14.22 |
| shippingservice | 195.40 | 1.90 | 1.29 | 4.12 | 1.02 | 8.47 | 1.23 |
| emailservice | 100.00 | 9.54 | 6.25 | 2.18 | 0.19 | 43.58 | 6.25 |
| redis-cart | 137.29 | 0.00 | 0.00 | 2.71 | 0.83 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
