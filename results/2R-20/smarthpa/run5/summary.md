# Run report: smarthpa | 2R-20% | run 5

- Started 2026-10-12 11:53:37 - finished 2026-10-12 12:09:07
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 354 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,449.63 |
| CPU Overutilization (%) - lower | 677.66 |
| Overutilization Time (min) - lower | 14.65 |
| CPU Overprovision (m) - lower | 80.93 |
| Overprovision Time (min) - higher | 0.52 |
| CPU Underprovision (m) - lower | 5,054.80 |
| Underprovision Time (min) - lower | 14.43 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 61103 | 0 | 350 | 1200 | 1700 | 67.95 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 279.10 | 136.79 | 14.65 | 2.54 | 0.30 | 1,760.73 | 14.39 |
| currencyservice | 1,057.63 | 32.79 | 13.39 | 2.54 | 0.30 | 788.98 | 13.17 |
| cartservice | 200.00 | 62.18 | 13.89 | 10.17 | 0.30 | 539.55 | 13.89 |
| adservice | 200.00 | 2.34 | 1.73 | 13.56 | 0.52 | 9.60 | 0.73 |
| checkoutservice | 100.00 | 56.21 | 13.67 | 4.24 | 0.52 | 239.83 | 13.67 |
| productcatalogservice | 100.00 | 150.11 | 14.39 | 4.24 | 0.52 | 696.89 | 14.39 |
| recommendationservice | 100.00 | 127.27 | 14.14 | 4.24 | 0.52 | 587.85 | 14.14 |
| paymentservice | 100.00 | 63.55 | 13.89 | 4.24 | 0.52 | 264.69 | 13.89 |
| shippingservice | 100.00 | 30.55 | 12.41 | 4.24 | 0.52 | 97.74 | 12.41 |
| emailservice | 100.00 | 15.74 | 10.67 | 4.24 | 0.52 | 68.93 | 10.67 |
| redis-cart | 112.91 | 0.12 | 0.10 | 26.69 | 5.29 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
