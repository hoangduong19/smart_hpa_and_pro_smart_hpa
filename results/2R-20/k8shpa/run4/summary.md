# Run report: k8shpa | 2R-20% | run 4

- Started 2026-10-12 10:29:03 - finished 2026-10-12 10:44:34
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 383 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,308.90 |
| CPU Overutilization (%) - lower | 462.13 |
| Overutilization Time (min) - lower | 14.29 |
| CPU Overprovision (m) - lower | 274.18 |
| Overprovision Time (min) - higher | 0.68 |
| CPU Underprovision (m) - lower | 3,729.24 |
| Underprovision Time (min) - lower | 14.29 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 58310 | 0 | 420 | 1400 | 1800 | 65.12 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 190.34 | 154.30 | 14.29 | 6.79 | 0.68 | 1,393.47 | 14.29 |
| currencyservice | 190.34 | 94.29 | 14.29 | 6.79 | 0.68 | 810.18 | 14.29 |
| cartservice | 379.11 | 25.54 | 13.02 | 27.15 | 0.95 | 237.08 | 11.99 |
| adservice | 379.63 | 2.79 | 2.31 | 75.20 | 5.23 | 20.37 | 1.80 |
| checkoutservice | 186.16 | 25.68 | 12.68 | 10.18 | 1.46 | 119.06 | 12.04 |
| productcatalogservice | 190.08 | 66.80 | 14.29 | 6.79 | 0.68 | 520.37 | 13.77 |
| recommendationservice | 189.82 | 59.36 | 13.28 | 9.92 | 1.21 | 460.84 | 13.03 |
| paymentservice | 189.56 | 30.30 | 13.25 | 9.92 | 1.21 | 164.23 | 12.75 |
| shippingservice | 185.90 | 0.00 | 0.00 | 16.45 | 2.94 | 0.00 | 0.00 |
| emailservice | 157.96 | 3.08 | 2.00 | 34.99 | 5.22 | 3.66 | 0.50 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
