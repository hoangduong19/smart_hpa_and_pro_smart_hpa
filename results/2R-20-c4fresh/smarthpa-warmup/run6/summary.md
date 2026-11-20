# Run report: smarthpa-warmup | 2R-20% | run 6

- Started 2026-11-19 20:52:39 - finished 2026-11-19 21:08:10
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 486 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,440.56 |
| CPU Overutilization (%) - lower | 388.41 |
| Overutilization Time (min) - lower | 14.61 |
| CPU Overprovision (m) - lower | 83.09 |
| Overprovision Time (min) - higher | 0.37 |
| CPU Underprovision (m) - lower | 3,522.43 |
| Underprovision Time (min) - lower | 14.61 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69062 | 0 | 350 | 1100 | 1400 | 76.73 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 433.74 | 74.08 | 14.61 | 3.70 | 0.37 | 1,157.00 | 14.61 |
| currencyservice | 195.68 | 97.43 | 14.61 | 3.70 | 0.37 | 849.59 | 14.61 |
| cartservice | 388.48 | 24.67 | 13.62 | 8.64 | 0.62 | 214.40 | 13.36 |
| adservice | 235.39 | 4.48 | 3.48 | 8.64 | 0.62 | 35.80 | 3.23 |
| checkoutservice | 193.83 | 27.22 | 14.11 | 5.76 | 0.88 | 116.87 | 13.78 |
| productcatalogservice | 195.88 | 66.12 | 14.61 | 3.70 | 0.37 | 508.44 | 14.57 |
| recommendationservice | 194.44 | 59.61 | 14.36 | 4.32 | 0.62 | 454.32 | 14.21 |
| paymentservice | 194.24 | 34.35 | 14.36 | 4.32 | 0.62 | 186.01 | 14.11 |
| shippingservice | 193.21 | 0.09 | 0.05 | 6.38 | 1.37 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 10.29 | 2.01 | 0.00 | 0.00 |
| redis-cart | 115.66 | 0.36 | 0.22 | 23.62 | 5.09 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
