# Run report: k8shpa | 2R-20% | run 2

- Started 2026-11-19 10:04:26 - finished 2026-11-19 10:19:57
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 472 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,125.30 |
| CPU Overutilization (%) - lower | 498.10 |
| Overutilization Time (min) - lower | 14.77 |
| CPU Overprovision (m) - lower | 407.08 |
| Overprovision Time (min) - higher | 0.20 |
| CPU Underprovision (m) - lower | 4,069.07 |
| Underprovision Time (min) - lower | 14.77 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67027 | 0 | 420 | 1200 | 1600 | 74.61 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 196.40 | 164.97 | 14.77 | 1.69 | 0.20 | 1,492.16 | 14.54 |
| currencyservice | 196.40 | 99.20 | 14.77 | 1.69 | 0.20 | 861.65 | 14.77 |
| cartservice | 389.41 | 29.48 | 14.03 | 13.14 | 0.70 | 286.44 | 13.78 |
| adservice | 200.00 | 0.00 | 0.00 | 200.00 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 194.92 | 29.84 | 14.27 | 4.45 | 0.70 | 155.72 | 14.19 |
| productcatalogservice | 195.76 | 68.24 | 14.54 | 3.60 | 0.43 | 530.93 | 14.46 |
| recommendationservice | 194.70 | 69.33 | 14.27 | 4.45 | 0.70 | 544.70 | 14.02 |
| paymentservice | 194.70 | 35.33 | 14.54 | 3.60 | 0.43 | 193.22 | 14.02 |
| shippingservice | 193.01 | 1.32 | 0.76 | 6.36 | 1.19 | 4.24 | 0.68 |
| emailservice | 100.00 | 0.40 | 0.26 | 98.09 | 14.71 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
