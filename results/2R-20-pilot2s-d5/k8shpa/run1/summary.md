# Run report: k8shpa | 2R-20% | run 1

- Started 2026-11-19 08:35:13 - finished 2026-11-19 08:50:43
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 178 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,116.63 |
| CPU Overutilization (%) - lower | 448.92 |
| Overutilization Time (min) - lower | 14.60 |
| CPU Overprovision (m) - lower | 414.94 |
| Overprovision Time (min) - higher | 0.39 |
| CPU Underprovision (m) - lower | 3,615.17 |
| Underprovision Time (min) - lower | 14.60 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73050 | 0 | 270 | 820 | 1300 | 81.26 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 194.94 | 141.70 | 14.60 | 2.81 | 0.39 | 1,258.99 | 14.60 |
| currencyservice | 194.94 | 98.52 | 14.60 | 2.81 | 0.39 | 857.87 | 14.60 |
| cartservice | 387.64 | 28.92 | 14.00 | 14.61 | 0.98 | 275.28 | 13.76 |
| adservice | 200.00 | 0.00 | 0.00 | 200.00 | 14.98 | 0.00 | 0.00 |
| checkoutservice | 193.26 | 22.72 | 13.76 | 5.62 | 0.98 | 91.57 | 13.27 |
| productcatalogservice | 194.38 | 56.02 | 14.60 | 2.81 | 0.39 | 407.87 | 14.00 |
| recommendationservice | 194.38 | 67.34 | 14.28 | 5.06 | 0.70 | 530.34 | 14.00 |
| paymentservice | 193.82 | 33.43 | 14.00 | 5.62 | 0.98 | 193.26 | 14.00 |
| shippingservice | 193.26 | 0.25 | 0.49 | 5.62 | 0.98 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 100.00 | 14.98 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 14.98 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
