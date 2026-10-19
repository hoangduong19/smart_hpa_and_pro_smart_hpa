# Run report: k8shpa | 5R-50% | run 2

- Started 2026-10-19 12:42:42 - finished 2026-10-19 12:58:13
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 373 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,583.94 |
| CPU Overutilization (%) - lower | 110.07 |
| Overutilization Time (min) - lower | 11.75 |
| CPU Overprovision (m) - lower | 3,947.56 |
| Overprovision Time (min) - higher | 7.25 |
| CPU Underprovision (m) - lower | 272.92 |
| Underprovision Time (min) - lower | 7.72 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 51002 | 0 | 380 | 1600 | 2300 | 56.63 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 433.78 | 48.87 | 8.53 | 76.14 | 6.50 | 221.45 | 7.25 |
| currencyservice | 406.70 | 43.81 | 10.75 | 34.58 | 2.94 | 51.47 | 3.49 |
| cartservice | 345.84 | 0.93 | 0.47 | 714.75 | 14.96 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 800.00 | 14.96 | 0.00 | 0.00 |
| checkoutservice | 173.19 | 0.00 | 0.00 | 358.98 | 14.96 | 0.00 | 0.00 |
| productcatalogservice | 319.30 | 6.62 | 2.02 | 229.22 | 14.96 | 0.00 | 0.00 |
| recommendationservice | 262.20 | 8.60 | 2.97 | 296.78 | 14.46 | 0.00 | 0.00 |
| paymentservice | 172.92 | 1.24 | 0.75 | 357.10 | 14.96 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.96 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.96 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.96 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
