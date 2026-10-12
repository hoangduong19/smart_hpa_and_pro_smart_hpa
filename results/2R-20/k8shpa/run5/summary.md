# Run report: k8shpa | 2R-20% | run 5

- Started 2026-10-12 11:32:35 - finished 2026-10-12 11:48:05
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 407 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,150.34 |
| CPU Overutilization (%) - lower | 470.33 |
| Overutilization Time (min) - lower | 14.67 |
| CPU Overprovision (m) - lower | 367.79 |
| Overprovision Time (min) - higher | 0.33 |
| CPU Underprovision (m) - lower | 3,758.48 |
| Underprovision Time (min) - lower | 14.67 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 58032 | 0 | 440 | 1400 | 1800 | 64.56 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.37 | 154.96 | 14.67 | 3.19 | 0.33 | 1,390.42 | 14.67 |
| currencyservice | 193.61 | 98.65 | 14.67 | 3.19 | 0.33 | 839.80 | 14.67 |
| cartservice | 376.41 | 26.43 | 13.14 | 16.71 | 1.60 | 226.04 | 12.64 |
| adservice | 200.00 | 0.00 | 0.00 | 200.00 | 14.99 | 0.00 | 0.00 |
| checkoutservice | 186.73 | 25.93 | 12.90 | 7.37 | 1.60 | 114.00 | 12.23 |
| productcatalogservice | 193.37 | 68.66 | 14.40 | 5.65 | 0.59 | 535.14 | 14.14 |
| recommendationservice | 192.87 | 62.27 | 14.14 | 6.63 | 0.85 | 476.17 | 13.64 |
| paymentservice | 193.12 | 31.03 | 13.40 | 6.63 | 0.85 | 169.04 | 13.15 |
| shippingservice | 186.49 | 0.38 | 0.50 | 11.79 | 2.10 | 0.00 | 0.00 |
| emailservice | 164.37 | 2.02 | 1.00 | 36.61 | 5.82 | 7.86 | 0.47 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.99 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
