# Run report: k8shpa | 2R-20% | run 2

- Started 2026-11-20 01:42:42 - finished 2026-11-20 01:58:12
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 468 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,309.19 |
| CPU Overutilization (%) - lower | 469.82 |
| Overutilization Time (min) - lower | 14.66 |
| CPU Overprovision (m) - lower | 355.19 |
| Overprovision Time (min) - higher | 0.33 |
| CPU Underprovision (m) - lower | 3,942.09 |
| Underprovision Time (min) - lower | 14.66 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 71250 | 0 | 330 | 880 | 1400 | 79.25 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.80 | 163.52 | 14.66 | 3.21 | 0.33 | 1,469.23 | 14.66 |
| currencyservice | 193.38 | 88.79 | 14.41 | 5.34 | 0.58 | 738.25 | 14.41 |
| cartservice | 387.18 | 36.61 | 14.41 | 12.82 | 0.33 | 426.92 | 13.66 |
| adservice | 383.76 | 3.04 | 2.24 | 127.35 | 9.26 | 23.08 | 1.74 |
| checkoutservice | 193.59 | 35.78 | 13.91 | 5.34 | 0.58 | 208.97 | 13.64 |
| productcatalogservice | 193.59 | 68.22 | 14.41 | 5.34 | 0.58 | 541.24 | 14.14 |
| recommendationservice | 193.38 | 65.90 | 14.38 | 5.56 | 0.61 | 519.44 | 14.38 |
| paymentservice | 137.61 | 1.58 | 1.00 | 92.95 | 13.99 | 2.14 | 0.40 |
| shippingservice | 189.74 | 3.09 | 2.18 | 8.76 | 1.35 | 12.82 | 2.00 |
| emailservice | 111.54 | 2.92 | 1.97 | 81.20 | 12.28 | 0.00 | 0.00 |
| redis-cart | 131.62 | 0.38 | 0.18 | 7.33 | 1.85 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
