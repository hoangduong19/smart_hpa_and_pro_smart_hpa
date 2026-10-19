# Run report: k8shpa | 5R-50% | run 3

- Started 2026-10-19 13:24:55 - finished 2026-10-19 13:40:25
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 378 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,727.67 |
| CPU Overutilization (%) - lower | 129.18 |
| Overutilization Time (min) - lower | 12.97 |
| CPU Overprovision (m) - lower | 3,822.33 |
| Overprovision Time (min) - higher | 5.42 |
| CPU Underprovision (m) - lower | 395.24 |
| Underprovision Time (min) - lower | 9.55 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 49494 | 0 | 460 | 1800 | 2600 | 55.00 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 435.45 | 57.80 | 10.25 | 57.41 | 5.39 | 246.83 | 7.80 |
| currencyservice | 411.11 | 56.19 | 12.48 | 31.22 | 2.73 | 146.83 | 5.02 |
| cartservice | 389.95 | 5.59 | 1.74 | 696.83 | 14.97 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 800.00 | 14.97 | 0.00 | 0.00 |
| checkoutservice | 171.43 | 0.37 | 0.07 | 358.47 | 14.97 | 0.00 | 0.00 |
| productcatalogservice | 362.70 | 2.95 | 1.07 | 203.44 | 11.97 | 0.00 | 0.00 |
| recommendationservice | 315.87 | 5.27 | 1.51 | 237.30 | 14.21 | 1.59 | 0.25 |
| paymentservice | 171.16 | 1.02 | 0.48 | 357.67 | 14.97 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.97 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.97 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.97 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
