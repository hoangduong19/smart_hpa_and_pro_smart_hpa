# Run report: k8shpa | 5R-50% | run 4

- Started 2026-10-07 13:34:57 - finished 2026-10-07 13:50:33
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 386 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,654.46 |
| CPU Overutilization (%) - lower | 202.11 |
| Overutilization Time (min) - lower | 13.91 |
| CPU Overprovision (m) - lower | 3,697.62 |
| Overprovision Time (min) - higher | 2.58 |
| CPU Underprovision (m) - lower | 843.01 |
| Underprovision Time (min) - lower | 12.38 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 63469 | 0 | 290 | 1000 | 1400 | 70.91 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 417.36 | 83.88 | 13.67 | 71.24 | 2.81 | 419.95 | 11.81 |
| currencyservice | 423.32 | 88.02 | 13.91 | 56.48 | 1.69 | 423.06 | 12.38 |
| cartservice | 333.68 | 1.45 | 0.49 | 675.65 | 14.96 | 0.00 | 0.00 |
| adservice | 277.20 | 1.25 | 0.73 | 790.16 | 14.96 | 0.00 | 0.00 |
| checkoutservice | 175.13 | 0.58 | 0.25 | 323.83 | 14.96 | 0.00 | 0.00 |
| productcatalogservice | 306.99 | 7.42 | 1.90 | 179.79 | 14.96 | 0.00 | 0.00 |
| recommendationservice | 275.65 | 17.77 | 5.28 | 198.70 | 14.96 | 0.00 | 0.00 |
| paymentservice | 175.13 | 1.74 | 0.50 | 321.76 | 14.96 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.96 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 14.96 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 14.96 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
