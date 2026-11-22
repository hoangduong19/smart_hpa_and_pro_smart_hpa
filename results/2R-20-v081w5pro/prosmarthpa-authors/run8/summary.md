# Run report: prosmarthpa-authors | 2R-20% | run 8

- Started 2026-11-22 06:30:59 - finished 2026-11-22 06:46:29
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 393 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,499.67 |
| CPU Overutilization (%) - lower | 485.40 |
| Overutilization Time (min) - lower | 14.69 |
| CPU Overprovision (m) - lower | 153.31 |
| Overprovision Time (min) - higher | 0.28 |
| CPU Underprovision (m) - lower | 4,527.23 |
| Underprovision Time (min) - lower | 14.69 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66337 | 0 | 440 | 1400 | 1900 | 73.75 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 293.89 | 134.03 | 14.33 | 4.07 | 0.64 | 1,762.60 | 14.33 |
| currencyservice | 196.95 | 97.79 | 14.33 | 3.05 | 0.64 | 853.94 | 14.33 |
| cartservice | 393.89 | 31.66 | 14.33 | 9.16 | 0.64 | 325.70 | 14.33 |
| adservice | 393.89 | 0.56 | 0.49 | 116.03 | 8.46 | 8.14 | 0.49 |
| checkoutservice | 197.20 | 32.74 | 13.84 | 2.80 | 0.28 | 184.99 | 13.84 |
| productcatalogservice | 197.20 | 80.68 | 14.69 | 2.80 | 0.28 | 653.18 | 14.69 |
| recommendationservice | 196.95 | 67.25 | 13.84 | 3.05 | 0.64 | 520.10 | 13.84 |
| paymentservice | 196.95 | 32.73 | 14.33 | 3.05 | 0.64 | 181.68 | 14.33 |
| shippingservice | 195.42 | 0.00 | 0.00 | 4.58 | 1.19 | 0.00 | 0.00 |
| emailservice | 100.00 | 7.97 | 5.75 | 2.04 | 0.18 | 36.90 | 5.75 |
| redis-cart | 137.33 | 0.00 | 0.00 | 2.67 | 0.85 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
