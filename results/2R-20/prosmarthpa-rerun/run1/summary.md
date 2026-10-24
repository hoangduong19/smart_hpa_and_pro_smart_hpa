# Run report: prosmarthpa-rerun | 2R-20% | run 1

- Started 2026-10-24 12:29:32 - finished 2026-10-24 12:45:02
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 411 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,107.49 |
| CPU Overutilization (%) - lower | 393.22 |
| Overutilization Time (min) - lower | 14.59 |
| CPU Overprovision (m) - lower | 96.86 |
| Overprovision Time (min) - higher | 0.48 |
| CPU Underprovision (m) - lower | 5,791.00 |
| Underprovision Time (min) - lower | 14.51 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65363 | 0 | 210 | 790 | 1100 | 72.66 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 539.42 | 76.44 | 14.59 | 4.62 | 0.40 | 1,727.49 | 14.26 |
| currencyservice | 843.07 | 50.64 | 14.51 | 7.06 | 0.48 | 1,809.00 | 14.51 |
| cartservice | 383.94 | 32.60 | 12.27 | 18.98 | 0.67 | 591.73 | 14.01 |
| adservice | 200.00 | 4.46 | 3.51 | 10.71 | 0.22 | 31.14 | 2.75 |
| checkoutservice | 133.82 | 38.78 | 13.51 | 5.60 | 0.73 | 175.43 | 13.51 |
| productcatalogservice | 194.65 | 78.81 | 13.81 | 4.87 | 0.48 | 651.34 | 13.76 |
| recommendationservice | 194.40 | 58.89 | 13.76 | 5.60 | 0.73 | 443.80 | 13.76 |
| paymentservice | 194.40 | 36.93 | 13.54 | 5.60 | 0.73 | 232.60 | 13.54 |
| shippingservice | 161.80 | 13.89 | 9.02 | 5.60 | 0.73 | 120.19 | 12.21 |
| emailservice | 131.87 | 1.78 | 1.29 | 19.22 | 2.95 | 8.27 | 1.13 |
| redis-cart | 130.12 | 0.00 | 0.00 | 9.03 | 1.58 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
