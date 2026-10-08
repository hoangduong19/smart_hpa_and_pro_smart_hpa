# Run report: k8shpa | 5R-50% | run 1

- Started 2026-10-02 14:44:26 - finished 2026-10-02 14:59:56
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 395 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,652.53 |
| CPU Overutilization (%) - lower | 215.32 |
| Overutilization Time (min) - lower | 14.50 |
| CPU Overprovision (m) - lower | 3,622.53 |
| Overprovision Time (min) - higher | 1.46 |
| CPU Underprovision (m) - lower | 1,035.44 |
| Underprovision Time (min) - lower | 13.53 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 64520 | 0 | 220 | 910 | 1400 | 71.74 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 450.89 | 92.79 | 14.21 | 38.48 | 1.74 | 492.15 | 12.81 |
| currencyservice | 461.77 | 100.32 | 14.50 | 22.78 | 0.69 | 543.29 | 13.53 |
| cartservice | 343.80 | 6.50 | 1.79 | 632.91 | 14.98 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 800.00 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 170.38 | 1.88 | 0.53 | 327.59 | 14.98 | 0.00 | 0.00 |
| productcatalogservice | 330.38 | 3.87 | 0.87 | 164.30 | 14.98 | 0.00 | 0.00 |
| recommendationservice | 250.63 | 5.93 | 1.63 | 238.48 | 14.98 | 0.00 | 0.00 |
| paymentservice | 174.68 | 4.04 | 0.96 | 317.97 | 14.98 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.98 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.98 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
