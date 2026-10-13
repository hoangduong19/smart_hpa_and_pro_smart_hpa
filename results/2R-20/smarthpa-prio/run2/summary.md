# Run report: smarthpa-prio | 2R-20% | run 2

- Started 2026-10-13 16:46:22 - finished 2026-10-13 17:01:52
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 326 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,450.00 |
| CPU Overutilization (%) - lower | 595.76 |
| Overutilization Time (min) - lower | 14.71 |
| CPU Overprovision (m) - lower | 72.70 |
| Overprovision Time (min) - higher | 0.50 |
| CPU Underprovision (m) - lower | 4,860.12 |
| Underprovision Time (min) - lower | 14.47 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 61033 | 0 | 390 | 1200 | 1600 | 67.90 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.48 | 157.18 | 14.47 | 4.60 | 0.50 | 1,419.94 | 14.47 |
| currencyservice | 763.19 | 49.25 | 14.71 | 2.45 | 0.26 | 1,194.79 | 14.47 |
| cartservice | 380.98 | 34.03 | 13.94 | 15.34 | 1.03 | 383.44 | 13.72 |
| adservice | 200.00 | 7.87 | 5.11 | 4.91 | 0.26 | 57.67 | 4.20 |
| checkoutservice | 189.88 | 33.17 | 13.45 | 9.51 | 1.26 | 185.28 | 13.22 |
| productcatalogservice | 194.79 | 70.07 | 14.24 | 4.60 | 0.50 | 557.98 | 14.14 |
| recommendationservice | 100.00 | 135.03 | 14.18 | 4.60 | 0.50 | 636.20 | 14.18 |
| paymentservice | 100.00 | 71.35 | 13.94 | 4.60 | 0.50 | 302.15 | 13.94 |
| shippingservice | 100.00 | 29.37 | 12.44 | 4.60 | 0.50 | 84.66 | 12.44 |
| emailservice | 100.00 | 8.32 | 5.75 | 4.60 | 0.50 | 38.04 | 5.75 |
| redis-cart | 126.69 | 0.13 | 0.09 | 12.88 | 2.75 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
