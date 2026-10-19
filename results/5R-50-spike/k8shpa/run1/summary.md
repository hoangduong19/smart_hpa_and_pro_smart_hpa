# Run report: k8shpa | 5R-50% | run 1

- Started 2026-10-19 12:00:25 - finished 2026-10-19 12:15:55
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 388 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,890.36 |
| CPU Overutilization (%) - lower | 158.61 |
| Overutilization Time (min) - lower | 13.04 |
| CPU Overprovision (m) - lower | 3,750.36 |
| Overprovision Time (min) - higher | 2.68 |
| CPU Underprovision (m) - lower | 784.54 |
| Underprovision Time (min) - lower | 12.31 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 53676 | 0 | 350 | 1000 | 1500 | 59.62 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 447.94 | 63.41 | 9.01 | 42.01 | 3.20 | 357.99 | 8.00 |
| currencyservice | 482.47 | 80.67 | 12.29 | 19.07 | 1.42 | 425.00 | 12.06 |
| cartservice | 488.66 | 0.87 | 0.27 | 661.86 | 14.99 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 800.00 | 14.99 | 0.00 | 0.00 |
| checkoutservice | 172.42 | 0.39 | 0.08 | 357.47 | 14.99 | 0.00 | 0.00 |
| productcatalogservice | 340.21 | 1.54 | 0.58 | 212.63 | 14.58 | 0.00 | 0.00 |
| recommendationservice | 316.49 | 4.18 | 1.22 | 236.34 | 14.04 | 1.55 | 0.22 |
| paymentservice | 172.16 | 2.05 | 0.74 | 351.55 | 14.99 | 0.00 | 0.00 |
| shippingservice | 100.00 | 5.52 | 1.76 | 389.43 | 14.99 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.99 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.99 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
