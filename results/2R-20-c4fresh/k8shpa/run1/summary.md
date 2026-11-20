# Run report: k8shpa | 2R-20% | run 1

- Started 2026-11-19 16:52:53 - finished 2026-11-19 17:08:24
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 485 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,443.98 |
| CPU Overutilization (%) - lower | 610.56 |
| Overutilization Time (min) - lower | 14.86 |
| CPU Overprovision (m) - lower | 149.65 |
| Overprovision Time (min) - higher | 0.39 |
| CPU Underprovision (m) - lower | 5,165.77 |
| Underprovision Time (min) - lower | 14.59 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 71555 | 0 | 300 | 870 | 1300 | 79.61 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 195.46 | 161.14 | 14.59 | 3.51 | 0.39 | 1,464.74 | 14.59 |
| currencyservice | 196.08 | 191.46 | 14.86 | 1.03 | 0.12 | 1,716.91 | 14.59 |
| cartservice | 390.52 | 34.11 | 14.34 | 7.01 | 0.39 | 386.39 | 13.84 |
| adservice | 378.97 | 6.99 | 3.49 | 96.08 | 6.62 | 55.26 | 2.99 |
| checkoutservice | 195.26 | 32.46 | 14.35 | 4.12 | 0.63 | 175.46 | 14.09 |
| productcatalogservice | 195.26 | 70.73 | 14.35 | 4.12 | 0.63 | 554.85 | 14.35 |
| recommendationservice | 195.26 | 68.95 | 14.59 | 3.51 | 0.39 | 540.41 | 14.35 |
| paymentservice | 195.26 | 40.94 | 14.59 | 3.51 | 0.39 | 267.84 | 14.09 |
| shippingservice | 191.55 | 1.20 | 0.69 | 7.01 | 1.37 | 3.92 | 0.51 |
| emailservice | 179.18 | 1.29 | 0.98 | 14.85 | 2.63 | 0.00 | 0.00 |
| redis-cart | 131.20 | 1.28 | 0.98 | 4.91 | 1.37 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
