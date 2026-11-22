# Run report: prosmarthpa-authors | 2R-20% | run 3

- Started 2026-11-22 04:16:44 - finished 2026-11-22 04:32:15
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 435 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,502.94 |
| CPU Overutilization (%) - lower | 493.19 |
| Overutilization Time (min) - lower | 14.34 |
| CPU Overprovision (m) - lower | 217.75 |
| Overprovision Time (min) - higher | 0.63 |
| CPU Underprovision (m) - lower | 4,612.18 |
| Underprovision Time (min) - lower | 14.34 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 71193 | 0 | 310 | 870 | 1200 | 79.20 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 294.48 | 135.72 | 14.34 | 3.45 | 0.63 | 1,788.05 | 14.34 |
| currencyservice | 197.24 | 98.12 | 14.34 | 2.76 | 0.63 | 863.22 | 14.34 |
| cartservice | 394.48 | 34.57 | 14.34 | 5.52 | 0.63 | 393.10 | 13.85 |
| adservice | 394.48 | 0.00 | 0.00 | 185.29 | 13.98 | 0.00 | 0.00 |
| checkoutservice | 197.47 | 31.69 | 13.59 | 3.91 | 1.12 | 181.61 | 13.59 |
| productcatalogservice | 197.24 | 74.57 | 14.34 | 2.76 | 0.63 | 593.56 | 14.34 |
| recommendationservice | 197.24 | 66.90 | 13.85 | 2.76 | 0.63 | 526.90 | 13.85 |
| paymentservice | 197.24 | 34.48 | 13.85 | 2.76 | 0.63 | 189.66 | 13.85 |
| shippingservice | 195.63 | 0.10 | 0.06 | 3.91 | 1.12 | 0.00 | 0.00 |
| emailservice | 100.00 | 17.04 | 10.98 | 2.07 | 0.18 | 76.09 | 10.98 |
| redis-cart | 137.43 | 0.00 | 0.00 | 2.57 | 0.83 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
