# Run report: k8shpa | 2R-20% | run 6

- Started 2026-11-20 08:23:37 - finished 2026-11-20 08:39:08
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 436 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,356.10 |
| CPU Overutilization (%) - lower | 549.63 |
| Overutilization Time (min) - lower | 14.83 |
| CPU Overprovision (m) - lower | 243.81 |
| Overprovision Time (min) - higher | 0.40 |
| CPU Underprovision (m) - lower | 4,712.39 |
| Underprovision Time (min) - lower | 14.59 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73528 | 0 | 260 | 700 | 1400 | 81.76 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 195.41 | 177.18 | 14.59 | 3.90 | 0.40 | 1,619.27 | 14.59 |
| currencyservice | 195.87 | 120.64 | 14.83 | 1.61 | 0.17 | 1,046.10 | 14.59 |
| cartservice | 390.37 | 43.03 | 14.33 | 8.72 | 0.66 | 567.89 | 14.33 |
| adservice | 383.94 | 0.85 | 0.75 | 97.25 | 7.52 | 0.00 | 0.00 |
| checkoutservice | 195.41 | 40.70 | 14.59 | 3.90 | 0.40 | 268.81 | 14.08 |
| productcatalogservice | 195.64 | 75.10 | 14.59 | 3.90 | 0.40 | 591.51 | 14.33 |
| recommendationservice | 195.41 | 68.92 | 14.33 | 4.36 | 0.66 | 534.17 | 14.08 |
| paymentservice | 100.00 | 0.00 | 0.00 | 100.00 | 14.99 | 0.00 | 0.00 |
| shippingservice | 195.18 | 19.39 | 12.35 | 4.59 | 0.91 | 84.63 | 12.10 |
| emailservice | 174.31 | 3.58 | 2.47 | 10.78 | 2.17 | 0.00 | 0.00 |
| redis-cart | 134.54 | 0.22 | 0.12 | 4.82 | 1.65 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
