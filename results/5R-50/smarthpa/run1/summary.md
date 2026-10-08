# Run report: smarthpa | 5R-50% | run 1

- Started 2026-10-02 15:05:12 - finished 2026-10-02 15:20:42
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 304 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,900.92 |
| CPU Overutilization (%) - lower | 141.88 |
| Overutilization Time (min) - lower | 14.44 |
| CPU Overprovision (m) - lower | 750.72 |
| Overprovision Time (min) - higher | 4.51 |
| CPU Underprovision (m) - lower | 381.25 |
| Underprovision Time (min) - lower | 10.43 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 64884 | 0 | 240 | 900 | 1400 | 72.11 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 845.39 | 55.06 | 12.34 | 37.17 | 1.72 | 246.71 | 10.43 |
| currencyservice | 1,193.09 | 27.33 | 6.83 | 28.62 | 2.19 | 35.20 | 3.99 |
| cartservice | 350.00 | 3.66 | 0.94 | 58.55 | 0.81 | 7.89 | 0.49 |
| adservice | 200.00 | 0.00 | 0.00 | 90.13 | 1.34 | 0.00 | 0.00 |
| checkoutservice | 179.61 | 0.37 | 0.09 | 89.80 | 3.96 | 0.00 | 0.00 |
| productcatalogservice | 419.08 | 1.43 | 0.45 | 78.29 | 4.51 | 0.00 | 0.00 |
| recommendationservice | 262.17 | 43.88 | 10.62 | 82.24 | 3.96 | 72.70 | 10.18 |
| paymentservice | 181.58 | 2.35 | 0.99 | 79.61 | 3.46 | 3.62 | 0.49 |
| shippingservice | 100.00 | 7.79 | 1.98 | 68.42 | 2.14 | 15.13 | 1.98 |
| emailservice | 100.00 | 0.00 | 0.00 | 69.74 | 2.46 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 68.16 | 4.40 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
