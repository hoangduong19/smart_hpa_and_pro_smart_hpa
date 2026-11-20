# Run report: smarthpa-warmup | 2R-20% | run 1

- Started 2026-11-19 09:28:30 - finished 2026-11-19 09:44:00
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 472 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,419.45 |
| CPU Overutilization (%) - lower | 488.76 |
| Overutilization Time (min) - lower | 14.84 |
| CPU Overprovision (m) - lower | 109.79 |
| Overprovision Time (min) - higher | 0.38 |
| CPU Underprovision (m) - lower | 4,736.44 |
| Underprovision Time (min) - lower | 14.59 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 73655 | 0 | 230 | 760 | 1300 | 81.88 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 195.97 | 155.01 | 14.59 | 3.39 | 0.38 | 1,396.82 | 14.59 |
| currencyservice | 456.57 | 87.07 | 14.84 | 1.27 | 0.13 | 1,482.63 | 14.59 |
| cartservice | 388.14 | 33.26 | 14.07 | 13.14 | 0.89 | 364.83 | 13.82 |
| adservice | 200.00 | 0.00 | 0.00 | 23.31 | 2.02 | 0.00 | 0.00 |
| checkoutservice | 194.28 | 27.40 | 14.07 | 5.30 | 0.89 | 121.40 | 14.02 |
| productcatalogservice | 196.19 | 69.58 | 14.59 | 3.39 | 0.38 | 541.74 | 14.54 |
| recommendationservice | 194.92 | 73.91 | 14.32 | 4.03 | 0.65 | 586.02 | 14.18 |
| paymentservice | 194.70 | 37.14 | 14.32 | 4.03 | 0.65 | 219.07 | 14.07 |
| shippingservice | 194.28 | 4.79 | 3.18 | 5.30 | 0.89 | 22.25 | 3.12 |
| emailservice | 100.00 | 0.37 | 0.27 | 11.65 | 2.02 | 1.69 | 0.27 |
| redis-cart | 104.41 | 0.23 | 0.14 | 35.00 | 7.71 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
