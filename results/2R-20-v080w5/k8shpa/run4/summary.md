# Run report: k8shpa | 2R-20% | run 4

- Started 2026-11-20 06:36:30 - finished 2026-11-20 06:52:02
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 447 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,239.02 |
| CPU Overutilization (%) - lower | 485.48 |
| Overutilization Time (min) - lower | 14.69 |
| CPU Overprovision (m) - lower | 348.01 |
| Overprovision Time (min) - higher | 0.53 |
| CPU Underprovision (m) - lower | 4,087.47 |
| Underprovision Time (min) - lower | 14.44 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73580 | 0 | 270 | 710 | 1300 | 81.86 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.51 | 168.90 | 14.69 | 2.68 | 0.28 | 1,526.62 | 14.44 |
| currencyservice | 193.51 | 90.75 | 14.69 | 2.68 | 0.28 | 740.94 | 14.44 |
| cartservice | 386.13 | 38.80 | 14.44 | 14.77 | 0.53 | 462.64 | 13.94 |
| adservice | 363.31 | 1.21 | 0.95 | 106.49 | 8.31 | 2.68 | 0.27 |
| checkoutservice | 193.06 | 36.65 | 14.18 | 6.71 | 0.79 | 217.23 | 13.94 |
| productcatalogservice | 193.29 | 69.90 | 14.44 | 4.92 | 0.53 | 550.56 | 14.44 |
| recommendationservice | 193.06 | 71.08 | 14.44 | 4.92 | 0.53 | 562.19 | 14.18 |
| paymentservice | 100.00 | 0.00 | 0.00 | 100.00 | 14.97 | 0.00 | 0.00 |
| shippingservice | 191.28 | 5.58 | 3.70 | 7.16 | 1.28 | 24.61 | 3.44 |
| emailservice | 100.00 | 1.74 | 1.25 | 91.72 | 13.72 | 0.00 | 0.00 |
| redis-cart | 131.86 | 0.87 | 0.83 | 5.95 | 1.29 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
