# Run report: smarthpa-warmup | 2R-20% | run 1

- Started 2026-11-19 17:14:42 - finished 2026-11-19 17:30:13
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 512 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,392.46 |
| CPU Overutilization (%) - lower | 416.96 |
| Overutilization Time (min) - lower | 14.67 |
| CPU Overprovision (m) - lower | 134.65 |
| Overprovision Time (min) - higher | 0.33 |
| CPU Underprovision (m) - lower | 3,759.96 |
| Underprovision Time (min) - lower | 14.67 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69303 | 0 | 380 | 1000 | 1400 | 77.04 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 428.32 | 75.84 | 14.67 | 3.12 | 0.33 | 1,157.23 | 14.67 |
| currencyservice | 194.92 | 97.47 | 14.67 | 3.12 | 0.33 | 851.95 | 14.67 |
| cartservice | 388.67 | 27.47 | 14.42 | 10.16 | 0.57 | 244.14 | 14.17 |
| adservice | 240.62 | 4.34 | 2.98 | 10.16 | 0.57 | 37.50 | 2.72 |
| checkoutservice | 193.95 | 34.02 | 14.17 | 5.66 | 0.83 | 187.11 | 13.84 |
| productcatalogservice | 194.53 | 68.08 | 14.42 | 5.08 | 0.57 | 541.60 | 14.42 |
| recommendationservice | 194.34 | 62.18 | 14.42 | 5.08 | 0.57 | 468.95 | 14.17 |
| paymentservice | 193.75 | 38.24 | 14.17 | 5.66 | 0.83 | 228.71 | 14.17 |
| shippingservice | 193.36 | 0.10 | 0.05 | 6.25 | 1.32 | 0.00 | 0.00 |
| emailservice | 100.00 | 9.21 | 6.14 | 10.35 | 2.01 | 42.77 | 6.14 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 15.00 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
