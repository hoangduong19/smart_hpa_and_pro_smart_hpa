# Run report: smarthpa | 2R-20% | run 4

- Started 2026-10-12 10:50:22 - finished 2026-10-12 11:05:52
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 319 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,259.34 |
| CPU Overutilization (%) - lower | 621.56 |
| Overutilization Time (min) - lower | 14.69 |
| CPU Overprovision (m) - lower | 80.85 |
| Overprovision Time (min) - higher | 0.57 |
| CPU Underprovision (m) - lower | 5,437.62 |
| Underprovision Time (min) - lower | 14.42 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 61781 | 44 | 270 | 1200 | 3400 | 68.67 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 384.64 | 113.41 | 14.69 | 2.82 | 0.30 | 1,898.12 | 13.92 |
| currencyservice | 664.26 | 46.08 | 14.42 | 5.02 | 0.57 | 943.89 | 14.42 |
| cartservice | 200.00 | 64.66 | 13.46 | 10.03 | 0.30 | 540.44 | 13.46 |
| adservice | 200.00 | 7.15 | 5.15 | 9.40 | 0.52 | 54.55 | 4.40 |
| checkoutservice | 100.00 | 62.23 | 13.44 | 5.02 | 0.57 | 264.26 | 13.44 |
| productcatalogservice | 194.36 | 75.43 | 13.80 | 5.02 | 0.57 | 614.42 | 13.70 |
| recommendationservice | 100.00 | 127.16 | 13.92 | 5.02 | 0.57 | 585.58 | 13.92 |
| paymentservice | 100.00 | 77.10 | 13.67 | 5.02 | 0.57 | 337.62 | 13.67 |
| shippingservice | 100.00 | 33.87 | 12.72 | 5.02 | 0.57 | 138.56 | 12.72 |
| emailservice | 100.00 | 14.26 | 9.17 | 5.02 | 0.57 | 60.19 | 9.17 |
| redis-cart | 116.08 | 0.20 | 0.16 | 23.48 | 4.77 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
