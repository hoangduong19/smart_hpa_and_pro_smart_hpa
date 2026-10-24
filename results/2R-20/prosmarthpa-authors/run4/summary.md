# Run report: prosmarthpa-authors | 2R-20% | run 4

- Started 2026-10-24 11:43:50 - finished 2026-10-24 11:59:20
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 473 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,693.72 |
| CPU Overutilization (%) - lower | 402.97 |
| Overutilization Time (min) - lower | 14.54 |
| CPU Overprovision (m) - lower | 308.92 |
| Overprovision Time (min) - higher | 0.43 |
| CPU Underprovision (m) - lower | 4,084.78 |
| Underprovision Time (min) - lower | 14.54 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62281 | 0 | 300 | 1000 | 1400 | 69.29 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 293.23 | 120.44 | 14.54 | 2.96 | 0.43 | 1,614.59 | 14.54 |
| currencyservice | 294.08 | 65.70 | 14.54 | 3.81 | 0.43 | 867.44 | 14.54 |
| cartservice | 394.08 | 25.52 | 12.05 | 8.46 | 0.76 | 252.01 | 12.05 |
| adservice | 394.08 | 0.00 | 0.00 | 200.00 | 14.97 | 0.00 | 0.00 |
| checkoutservice | 197.25 | 21.18 | 11.54 | 5.29 | 1.43 | 86.68 | 11.54 |
| productcatalogservice | 197.25 | 73.60 | 13.79 | 2.75 | 0.25 | 586.26 | 13.79 |
| recommendationservice | 197.04 | 59.47 | 14.04 | 2.96 | 0.43 | 447.78 | 14.04 |
| paymentservice | 197.04 | 36.44 | 13.54 | 3.59 | 0.85 | 224.52 | 13.54 |
| shippingservice | 197.25 | 0.00 | 0.00 | 15.01 | 2.43 | 0.00 | 0.00 |
| emailservice | 194.93 | 0.63 | 0.37 | 54.33 | 6.56 | 5.50 | 0.84 |
| redis-cart | 137.48 | 0.00 | 0.00 | 9.77 | 1.85 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
