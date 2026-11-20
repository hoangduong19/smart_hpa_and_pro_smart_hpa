# Run report: k8shpa | 2R-20% | run 1

- Started 2026-11-20 02:17:58 - finished 2026-11-20 02:33:29
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 439 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,285.10 |
| CPU Overutilization (%) - lower | 482.04 |
| Overutilization Time (min) - lower | 14.67 |
| CPU Overprovision (m) - lower | 331.66 |
| Overprovision Time (min) - higher | 0.32 |
| CPU Underprovision (m) - lower | 3,968.34 |
| Underprovision Time (min) - lower | 14.67 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 71658 | 0 | 330 | 810 | 1200 | 79.69 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.39 | 165.51 | 14.67 | 3.19 | 0.32 | 1,488.61 | 14.67 |
| currencyservice | 193.39 | 92.50 | 14.67 | 3.19 | 0.32 | 750.34 | 14.67 |
| cartservice | 385.88 | 36.36 | 14.42 | 12.30 | 0.57 | 430.52 | 14.16 |
| adservice | 381.78 | 1.67 | 0.97 | 101.14 | 7.68 | 10.48 | 0.97 |
| checkoutservice | 192.94 | 35.24 | 14.42 | 5.47 | 0.57 | 196.81 | 13.91 |
| productcatalogservice | 193.17 | 73.32 | 14.42 | 5.47 | 0.57 | 579.95 | 14.42 |
| recommendationservice | 192.94 | 66.32 | 14.42 | 5.47 | 0.57 | 511.62 | 14.16 |
| paymentservice | 141.69 | 0.44 | 0.37 | 95.90 | 14.25 | 0.00 | 0.00 |
| shippingservice | 191.12 | 0.46 | 0.19 | 7.29 | 1.33 | 0.00 | 0.00 |
| emailservice | 125.06 | 2.22 | 1.50 | 71.53 | 10.56 | 0.00 | 0.00 |
| redis-cart | 93.76 | 8.00 | 5.00 | 20.73 | 4.54 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
