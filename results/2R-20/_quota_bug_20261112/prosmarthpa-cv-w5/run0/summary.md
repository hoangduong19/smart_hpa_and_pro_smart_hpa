# Run report: prosmarthpa-cv-w5 | 2R-20% | run 0

- Started 2026-11-12 14:18:08 - finished 2026-11-12 14:21:39
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 100 users, spawn rate 0.67/s, 180 s
- Knowledge Base rows: 83 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,529.04 |
| CPU Overutilization (%) - lower | 164.11 |
| Overutilization Time (min) - lower | 2.61 |
| CPU Overprovision (m) - lower | 309.64 |
| Overprovision Time (min) - higher | 0.37 |
| CPU Underprovision (m) - lower | 1,889.16 |
| Underprovision Time (min) - lower | 2.61 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 5012 | 0 | 130 | 430 | 960 | 28.06 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 238.55 | 47.00 | 2.61 | 21.69 | 0.37 | 528.92 | 2.61 |
| currencyservice | 614.46 | 35.66 | 2.61 | 24.10 | 0.75 | 548.19 | 1.88 |
| cartservice | 349.40 | 9.80 | 1.44 | 45.78 | 0.40 | 233.73 | 2.20 |
| adservice | 356.63 | 4.72 | 0.48 | 48.19 | 0.75 | 171.08 | 1.59 |
| checkoutservice | 175.90 | 3.99 | 0.35 | 25.30 | 1.13 | 80.72 | 1.59 |
| productcatalogservice | 174.70 | 27.42 | 2.26 | 22.89 | 0.72 | 157.83 | 2.22 |
| recommendationservice | 174.70 | 17.02 | 1.37 | 24.10 | 0.75 | 92.77 | 1.37 |
| paymentservice | 174.70 | 14.95 | 1.37 | 25.30 | 1.13 | 59.04 | 1.37 |
| shippingservice | 100.00 | 3.54 | 0.35 | 21.69 | 0.37 | 16.87 | 0.35 |
| emailservice | 100.00 | 0.00 | 0.00 | 25.30 | 0.44 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 25.30 | 1.38 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
