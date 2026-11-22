# Run report: prosmarthpa-authors | 2R-20% | run 5

- Started 2026-11-22 05:10:27 - finished 2026-11-22 05:25:57
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 416 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,501.66 |
| CPU Overutilization (%) - lower | 509.28 |
| Overutilization Time (min) - lower | 14.81 |
| CPU Overprovision (m) - lower | 170.14 |
| Overprovision Time (min) - higher | 0.16 |
| CPU Underprovision (m) - lower | 4,728.12 |
| Underprovision Time (min) - lower | 14.81 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69640 | 0 | 380 | 990 | 1400 | 77.43 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 294.23 | 136.72 | 14.55 | 3.61 | 0.41 | 1,800.00 | 14.55 |
| currencyservice | 197.12 | 98.72 | 14.81 | 1.92 | 0.16 | 862.02 | 14.81 |
| cartservice | 394.23 | 32.41 | 13.56 | 9.62 | 0.41 | 342.31 | 13.56 |
| adservice | 394.23 | 0.00 | 0.00 | 122.60 | 9.72 | 0.00 | 0.00 |
| checkoutservice | 197.36 | 30.40 | 13.56 | 3.12 | 0.75 | 173.56 | 13.56 |
| productcatalogservice | 197.12 | 76.49 | 14.55 | 2.88 | 0.41 | 610.34 | 14.55 |
| recommendationservice | 197.12 | 76.05 | 14.55 | 2.88 | 0.41 | 612.02 | 14.55 |
| paymentservice | 197.12 | 38.89 | 14.55 | 2.88 | 0.41 | 242.31 | 14.55 |
| shippingservice | 195.67 | 0.00 | 0.00 | 4.33 | 1.22 | 0.00 | 0.00 |
| emailservice | 100.00 | 19.61 | 12.30 | 2.16 | 0.18 | 85.58 | 12.30 |
| redis-cart | 137.48 | 0.00 | 0.00 | 14.13 | 3.45 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
