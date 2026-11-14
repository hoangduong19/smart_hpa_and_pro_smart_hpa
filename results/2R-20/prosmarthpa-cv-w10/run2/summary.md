# Run report: prosmarthpa-cv-w10 | 2R-20% | run 2

- Started 2026-11-13 00:18:25 - finished 2026-11-13 00:33:55
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 491 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,477.05 |
| CPU Overutilization (%) - lower | 400.31 |
| Overutilization Time (min) - lower | 14.64 |
| CPU Overprovision (m) - lower | 77.21 |
| Overprovision Time (min) - higher | 0.60 |
| CPU Underprovision (m) - lower | 3,016.29 |
| Underprovision Time (min) - lower | 14.37 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 63913 | 0 | 290 | 910 | 1300 | 71.09 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.70 | 138.79 | 14.64 | 4.07 | 0.33 | 1,236.25 | 14.37 |
| currencyservice | 765.38 | 25.34 | 14.64 | 5.30 | 0.60 | 285.95 | 14.37 |
| cartservice | 200.00 | 50.05 | 13.87 | 9.78 | 0.33 | 383.30 | 13.87 |
| adservice | 200.00 | 0.00 | 0.00 | 8.15 | 0.33 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 45.82 | 13.13 | 4.68 | 0.60 | 172.51 | 13.13 |
| productcatalogservice | 289.41 | 36.09 | 13.14 | 5.50 | 0.88 | 318.13 | 13.14 |
| recommendationservice | 195.32 | 50.08 | 13.39 | 5.09 | 0.85 | 364.15 | 13.39 |
| paymentservice | 195.52 | 32.71 | 13.39 | 4.89 | 0.63 | 179.23 | 13.39 |
| shippingservice | 100.00 | 21.43 | 11.88 | 4.68 | 0.60 | 76.78 | 11.88 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.68 | 0.60 | 0.00 | 0.00 |
| redis-cart | 136.72 | 0.00 | 0.00 | 20.39 | 3.83 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
