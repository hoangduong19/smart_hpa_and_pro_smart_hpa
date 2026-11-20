# Run report: smarthpa | 2R-20% | run 6

- Started 2026-11-20 08:50:27 - finished 2026-11-20 09:05:59
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 459 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,362.22 |
| CPU Overutilization (%) - lower | 612.02 |
| Overutilization Time (min) - lower | 14.63 |
| CPU Overprovision (m) - lower | 69.48 |
| Overprovision Time (min) - higher | 0.57 |
| CPU Underprovision (m) - lower | 4,448.80 |
| Underprovision Time (min) - lower | 14.40 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 72508 | 0 | 210 | 800 | 3600 | 80.58 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 353.38 | 123.95 | 14.63 | 3.27 | 0.34 | 1,880.61 | 14.40 |
| currencyservice | 876.47 | 20.56 | 12.40 | 3.27 | 0.34 | 157.73 | 12.17 |
| cartservice | 200.00 | 73.33 | 14.37 | 13.07 | 0.34 | 647.06 | 14.37 |
| adservice | 200.00 | 4.25 | 2.56 | 11.33 | 0.34 | 20.48 | 1.32 |
| checkoutservice | 100.00 | 68.69 | 14.37 | 5.23 | 0.57 | 291.50 | 14.37 |
| productcatalogservice | 100.00 | 153.45 | 14.37 | 5.23 | 0.57 | 710.68 | 14.37 |
| recommendationservice | 100.00 | 129.86 | 14.37 | 5.23 | 0.57 | 598.04 | 14.37 |
| paymentservice | 100.00 | 0.00 | 0.00 | 5.23 | 0.57 | 0.00 | 0.00 |
| shippingservice | 100.00 | 34.95 | 13.66 | 5.23 | 0.57 | 129.63 | 13.66 |
| emailservice | 100.00 | 2.79 | 2.02 | 5.23 | 0.57 | 13.07 | 2.02 |
| redis-cart | 132.37 | 0.21 | 0.12 | 7.17 | 1.32 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
