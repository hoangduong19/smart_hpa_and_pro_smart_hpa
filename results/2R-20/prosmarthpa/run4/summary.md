# Run report: prosmarthpa | 2R-20% | run 4

- Started 2026-10-12 11:11:28 - finished 2026-10-12 11:27:03
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 452 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,107.79 |
| CPU Overutilization (%) - lower | 407.08 |
| Overutilization Time (min) - lower | 14.60 |
| CPU Overprovision (m) - lower | 68.61 |
| Overprovision Time (min) - higher | 0.37 |
| CPU Underprovision (m) - lower | 6,369.91 |
| Underprovision Time (min) - lower | 14.60 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65707 | 0 | 200 | 840 | 1300 | 73.08 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 552.88 | 74.74 | 14.60 | 4.20 | 0.37 | 1,677.65 | 14.60 |
| currencyservice | 754.42 | 71.67 | 14.60 | 4.20 | 0.37 | 2,482.52 | 14.60 |
| cartservice | 390.27 | 31.34 | 13.37 | 12.39 | 0.63 | 525.22 | 14.08 |
| adservice | 200.00 | 9.22 | 6.57 | 8.41 | 0.37 | 57.52 | 4.28 |
| checkoutservice | 195.13 | 29.12 | 12.62 | 11.28 | 1.62 | 156.64 | 12.62 |
| productcatalogservice | 195.35 | 75.41 | 14.17 | 4.20 | 0.37 | 610.84 | 14.12 |
| recommendationservice | 195.13 | 64.36 | 13.83 | 4.87 | 0.63 | 508.19 | 13.83 |
| paymentservice | 195.13 | 32.88 | 13.33 | 4.87 | 0.63 | 201.55 | 13.33 |
| shippingservice | 171.02 | 10.49 | 7.33 | 4.87 | 0.63 | 117.04 | 12.54 |
| emailservice | 138.27 | 7.84 | 4.75 | 4.20 | 0.37 | 32.74 | 4.61 |
| redis-cart | 120.18 | 0.00 | 0.00 | 5.11 | 1.04 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
