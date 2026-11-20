# Run report: k8shpa | 2R-20% | run 5

- Started 2026-11-19 19:47:15 - finished 2026-11-19 20:02:46
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 507 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,337.38 |
| CPU Overutilization (%) - lower | 469.22 |
| Overutilization Time (min) - lower | 14.73 |
| CPU Overprovision (m) - lower | 257.18 |
| Overprovision Time (min) - higher | 0.27 |
| CPU Underprovision (m) - lower | 3,692.50 |
| Underprovision Time (min) - lower | 14.73 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 71529 | 0 | 300 | 870 | 1200 | 79.54 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.49 | 146.95 | 14.73 | 2.56 | 0.27 | 1,304.73 | 14.47 |
| currencyservice | 193.49 | 98.88 | 14.73 | 2.56 | 0.27 | 842.01 | 14.73 |
| cartservice | 386.59 | 27.50 | 14.49 | 5.13 | 0.27 | 248.92 | 13.99 |
| adservice | 373.57 | 7.61 | 3.99 | 108.88 | 7.75 | 55.62 | 2.98 |
| checkoutservice | 193.10 | 32.34 | 14.22 | 6.71 | 0.78 | 179.68 | 13.97 |
| productcatalogservice | 193.10 | 57.36 | 14.22 | 6.71 | 0.78 | 437.08 | 14.22 |
| recommendationservice | 192.90 | 53.30 | 14.22 | 6.71 | 0.78 | 378.30 | 13.97 |
| paymentservice | 193.29 | 37.49 | 14.47 | 4.93 | 0.53 | 224.46 | 14.22 |
| shippingservice | 192.90 | 4.68 | 3.21 | 6.90 | 1.02 | 21.70 | 2.96 |
| emailservice | 100.00 | 0.37 | 0.24 | 98.22 | 14.75 | 0.00 | 0.00 |
| redis-cart | 124.95 | 2.73 | 1.52 | 7.87 | 2.03 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
