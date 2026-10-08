# Run report: k8shpa | 5R-50% | run 3

- Started 2026-10-02 16:13:49 - finished 2026-10-02 16:29:19
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 354 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,737.80 |
| CPU Overutilization (%) - lower | 223.41 |
| Overutilization Time (min) - lower | 14.18 |
| CPU Overprovision (m) - lower | 3,560.79 |
| Overprovision Time (min) - higher | 2.32 |
| CPU Underprovision (m) - lower | 857.91 |
| Underprovision Time (min) - lower | 12.67 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 57609 | 99 | 340 | 1400 | 6700 | 64.08 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 450.28 | 85.61 | 13.51 | 42.37 | 1.90 | 432.77 | 12.42 |
| currencyservice | 449.72 | 89.60 | 14.18 | 35.59 | 1.15 | 425.14 | 12.42 |
| cartservice | 349.72 | 2.19 | 1.00 | 654.80 | 14.98 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 800.00 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 175.14 | 3.32 | 0.94 | 328.81 | 14.98 | 0.00 | 0.00 |
| productcatalogservice | 350.85 | 28.12 | 7.43 | 112.71 | 7.76 | 0.00 | 0.00 |
| recommendationservice | 309.60 | 13.15 | 3.27 | 185.59 | 14.51 | 0.00 | 0.00 |
| paymentservice | 182.49 | 1.42 | 0.25 | 320.90 | 14.98 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.98 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.98 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
