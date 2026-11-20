# Run report: smarthpa | 2R-20% | run 5

- Started 2026-11-20 07:56:51 - finished 2026-11-20 08:12:21
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 490 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,449.80 |
| CPU Overutilization (%) - lower | 636.63 |
| Overutilization Time (min) - lower | 14.78 |
| CPU Overprovision (m) - lower | 67.06 |
| Overprovision Time (min) - higher | 0.63 |
| CPU Underprovision (m) - lower | 5,439.80 |
| Underprovision Time (min) - lower | 14.33 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 76617 | 0 | 190 | 510 | 1000 | 85.18 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 1,033.47 | 53.81 | 14.78 | 1.84 | 0.18 | 1,844.90 | 14.33 |
| currencyservice | 287.76 | 81.19 | 14.54 | 4.08 | 0.42 | 966.94 | 14.28 |
| cartservice | 200.00 | 77.61 | 14.28 | 8.16 | 0.42 | 678.37 | 14.28 |
| adservice | 200.00 | 9.33 | 6.52 | 8.16 | 0.42 | 60.41 | 4.51 |
| checkoutservice | 100.00 | 69.17 | 14.03 | 5.92 | 0.63 | 291.43 | 14.03 |
| productcatalogservice | 100.00 | 168.40 | 14.28 | 5.92 | 0.63 | 791.84 | 14.28 |
| recommendationservice | 100.00 | 130.45 | 14.28 | 4.08 | 0.42 | 606.53 | 14.28 |
| paymentservice | 100.00 | 0.34 | 0.24 | 5.92 | 0.63 | 1.63 | 0.24 |
| shippingservice | 100.00 | 41.27 | 14.03 | 5.92 | 0.63 | 174.49 | 14.03 |
| emailservice | 100.00 | 4.97 | 3.51 | 5.92 | 0.63 | 23.27 | 3.51 |
| redis-cart | 128.57 | 0.09 | 0.05 | 11.14 | 1.93 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
