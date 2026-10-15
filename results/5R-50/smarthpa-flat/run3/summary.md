# Run report: smarthpa-flat | 5R-50% | run 3

- Started 2026-10-15 15:26:19 - finished 2026-10-15 15:41:54
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 157 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 4,236.88 |
| CPU Overutilization (%) - lower | 90.05 |
| Overutilization Time (min) - lower | 11.68 |
| CPU Overprovision (m) - lower | 1,932.36 |
| Overprovision Time (min) - higher | 14.13 |
| CPU Underprovision (m) - lower | 6.37 |
| Underprovision Time (min) - lower | 0.78 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67044 | 0 | 190 | 670 | 1000 | 74.52 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 917.83 | 26.31 | 7.11 | 122.93 | 7.58 | 0.00 | 0.00 |
| currencyservice | 1,543.95 | 31.36 | 7.75 | 107.01 | 8.06 | 2.55 | 0.25 |
| cartservice | 363.06 | 11.21 | 4.22 | 183.44 | 2.59 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 245.86 | 2.98 | 0.00 | 0.00 |
| checkoutservice | 171.97 | 2.75 | 1.16 | 201.91 | 10.87 | 1.27 | 0.25 |
| productcatalogservice | 338.22 | 5.46 | 1.22 | 154.78 | 7.52 | 0.00 | 0.00 |
| recommendationservice | 256.69 | 8.69 | 3.28 | 227.39 | 13.71 | 0.00 | 0.00 |
| paymentservice | 171.34 | 1.62 | 1.20 | 144.59 | 4.29 | 0.00 | 0.00 |
| shippingservice | 103.82 | 2.66 | 0.96 | 140.13 | 3.62 | 2.55 | 0.78 |
| emailservice | 100.00 | 0.00 | 0.00 | 152.87 | 3.89 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 251.46 | 14.91 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
