# Run report: prosmarthpa-authors | 2R-20% | run 6

- Started 2026-11-22 05:37:19 - finished 2026-11-22 05:52:51
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 412 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,501.29 |
| CPU Overutilization (%) - lower | 522.50 |
| Overutilization Time (min) - lower | 14.71 |
| CPU Overprovision (m) - lower | 183.69 |
| Overprovision Time (min) - higher | 0.25 |
| CPU Underprovision (m) - lower | 4,764.81 |
| Underprovision Time (min) - lower | 14.71 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69940 | 0 | 340 | 1000 | 1300 | 77.74 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 294.17 | 140.19 | 14.42 | 3.64 | 0.54 | 1,858.50 | 14.42 |
| currencyservice | 197.09 | 97.96 | 14.42 | 2.91 | 0.54 | 861.17 | 14.42 |
| cartservice | 394.17 | 28.38 | 13.41 | 12.62 | 0.79 | 263.11 | 13.41 |
| adservice | 394.17 | 0.14 | 0.25 | 127.18 | 9.72 | 0.97 | 0.25 |
| checkoutservice | 197.09 | 35.17 | 13.92 | 2.91 | 0.54 | 191.26 | 13.92 |
| productcatalogservice | 197.33 | 85.47 | 14.71 | 2.67 | 0.25 | 700.24 | 14.71 |
| recommendationservice | 197.09 | 72.05 | 14.42 | 2.91 | 0.54 | 564.56 | 14.42 |
| paymentservice | 197.09 | 37.39 | 14.17 | 2.91 | 0.54 | 215.29 | 14.17 |
| shippingservice | 195.63 | 4.25 | 2.93 | 4.37 | 1.10 | 20.15 | 2.93 |
| emailservice | 100.00 | 21.51 | 12.93 | 2.18 | 0.18 | 89.56 | 12.93 |
| redis-cart | 137.45 | 0.00 | 0.00 | 19.37 | 4.54 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
