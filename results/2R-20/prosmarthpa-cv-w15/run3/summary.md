# Run report: prosmarthpa-cv-w15 | 2R-20% | run 3

- Started 2026-11-13 02:25:09 - finished 2026-11-13 02:40:39
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 429 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,397.97 |
| CPU Overutilization (%) - lower | 450.89 |
| Overutilization Time (min) - lower | 14.61 |
| CPU Overprovision (m) - lower | 77.90 |
| Overprovision Time (min) - higher | 0.62 |
| CPU Underprovision (m) - lower | 4,093.54 |
| Underprovision Time (min) - lower | 14.35 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67634 | 0 | 190 | 560 | 900 | 75.20 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.94 | 142.49 | 14.35 | 5.59 | 0.62 | 1,274.59 | 14.35 |
| currencyservice | 756.88 | 46.66 | 14.61 | 5.59 | 0.62 | 1,140.09 | 14.35 |
| cartservice | 200.00 | 54.22 | 13.61 | 10.72 | 0.41 | 431.24 | 13.61 |
| adservice | 200.00 | 0.00 | 0.00 | 9.79 | 0.36 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 47.72 | 13.61 | 6.06 | 0.87 | 195.34 | 13.61 |
| productcatalogservice | 288.81 | 38.02 | 13.11 | 10.72 | 1.35 | 364.57 | 13.11 |
| recommendationservice | 194.41 | 48.29 | 13.61 | 7.93 | 0.87 | 349.88 | 13.61 |
| paymentservice | 193.94 | 35.36 | 13.60 | 6.06 | 0.87 | 218.18 | 13.60 |
| shippingservice | 100.00 | 23.48 | 12.09 | 5.59 | 0.62 | 75.76 | 12.09 |
| emailservice | 100.00 | 0.00 | 0.00 | 5.59 | 0.62 | 0.00 | 0.00 |
| redis-cart | 70.00 | 14.64 | 10.35 | 4.24 | 0.87 | 43.89 | 10.35 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
