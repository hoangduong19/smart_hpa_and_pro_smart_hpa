# Run report: prosmarthpa | 2R-20% | run 3

- Started 2026-10-08 15:40:21 - finished 2026-10-08 15:55:51
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 430 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,113.84 |
| CPU Overutilization (%) - lower | 421.85 |
| Overutilization Time (min) - lower | 14.82 |
| CPU Overprovision (m) - lower | 65.84 |
| Overprovision Time (min) - higher | 0.39 |
| CPU Underprovision (m) - lower | 6,247.91 |
| Underprovision Time (min) - lower | 14.57 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 64413 | 0 | 270 | 850 | 1200 | 71.66 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 543.26 | 80.29 | 14.57 | 4.42 | 0.39 | 1,817.44 | 14.30 |
| currencyservice | 761.16 | 59.22 | 14.82 | 6.28 | 0.36 | 1,973.95 | 14.57 |
| cartservice | 388.37 | 36.66 | 13.05 | 13.49 | 0.64 | 626.51 | 14.05 |
| adservice | 200.00 | 1.81 | 1.20 | 4.19 | 0.17 | 13.95 | 0.95 |
| checkoutservice | 194.42 | 32.41 | 12.57 | 5.81 | 0.70 | 196.51 | 12.57 |
| productcatalogservice | 195.12 | 84.18 | 13.80 | 5.81 | 0.91 | 698.37 | 13.80 |
| recommendationservice | 194.88 | 59.64 | 13.56 | 5.12 | 0.66 | 458.14 | 13.56 |
| paymentservice | 194.88 | 41.38 | 14.06 | 5.12 | 0.66 | 273.49 | 14.06 |
| shippingservice | 174.19 | 18.53 | 11.82 | 5.12 | 0.66 | 153.95 | 12.51 |
| emailservice | 134.88 | 7.73 | 4.46 | 5.12 | 0.66 | 35.58 | 4.34 |
| redis-cart | 132.67 | 0.00 | 0.00 | 5.37 | 0.96 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
