# Run report: k8shpa | 2R-20% | run 1

- Started 2026-11-19 07:33:17 - finished 2026-11-19 07:48:48
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 460 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,295.87 |
| CPU Overutilization (%) - lower | 486.43 |
| Overutilization Time (min) - lower | 14.64 |
| CPU Overprovision (m) - lower | 351.96 |
| Overprovision Time (min) - higher | 0.34 |
| CPU Underprovision (m) - lower | 3,920.43 |
| Underprovision Time (min) - lower | 14.64 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67126 | 0 | 410 | 1200 | 1800 | 74.64 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.70 | 159.63 | 14.64 | 3.04 | 0.34 | 1,429.13 | 14.64 |
| currencyservice | 193.70 | 98.58 | 14.64 | 3.04 | 0.34 | 844.35 | 14.64 |
| cartservice | 386.52 | 28.66 | 14.15 | 12.61 | 0.60 | 267.83 | 13.65 |
| adservice | 386.09 | 1.01 | 0.75 | 134.78 | 9.97 | 7.83 | 0.49 |
| checkoutservice | 193.26 | 28.07 | 14.38 | 5.43 | 0.60 | 133.04 | 13.88 |
| productcatalogservice | 193.48 | 71.73 | 14.38 | 5.43 | 0.60 | 560.00 | 14.13 |
| recommendationservice | 193.26 | 64.44 | 14.38 | 5.43 | 0.60 | 494.13 | 14.13 |
| paymentservice | 193.26 | 33.74 | 14.38 | 5.43 | 0.60 | 182.17 | 14.13 |
| shippingservice | 192.61 | 0.58 | 0.70 | 6.74 | 1.10 | 1.96 | 0.26 |
| emailservice | 100.00 | 0.00 | 0.00 | 100.00 | 14.98 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
