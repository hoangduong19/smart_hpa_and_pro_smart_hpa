# Run report: prosmarthpa-cv-w10 | 2R-20% | run 1

- Started 2026-11-12 15:15:53 - finished 2026-11-12 15:31:26
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 320 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,879.78 |
| CPU Overutilization (%) - lower | 342.58 |
| Overutilization Time (min) - lower | 14.59 |
| CPU Overprovision (m) - lower | 143.66 |
| Overprovision Time (min) - higher | 0.51 |
| CPU Underprovision (m) - lower | 4,709.06 |
| Underprovision Time (min) - lower | 14.45 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67812 | 0 | 190 | 590 | 1000 | 75.41 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 397.19 | 76.61 | 14.59 | 6.88 | 0.37 | 1,353.75 | 14.33 |
| currencyservice | 817.19 | 51.51 | 14.59 | 9.69 | 0.63 | 1,699.69 | 14.33 |
| cartservice | 380.00 | 27.08 | 13.09 | 18.12 | 0.63 | 466.88 | 13.83 |
| adservice | 200.00 | 0.51 | 0.23 | 13.75 | 0.37 | 0.00 | 0.00 |
| checkoutservice | 134.69 | 31.88 | 13.09 | 9.38 | 0.83 | 172.81 | 13.09 |
| productcatalogservice | 190.31 | 60.54 | 13.63 | 9.06 | 0.63 | 460.62 | 13.58 |
| recommendationservice | 191.25 | 43.39 | 13.47 | 10.31 | 0.76 | 313.12 | 13.47 |
| paymentservice | 190.94 | 30.82 | 13.34 | 13.75 | 1.13 | 186.25 | 13.34 |
| shippingservice | 115.62 | 19.67 | 8.57 | 9.06 | 0.63 | 53.12 | 10.23 |
| emailservice | 129.38 | 0.56 | 0.50 | 21.56 | 3.69 | 2.81 | 0.50 |
| redis-cart | 133.22 | 0.00 | 0.00 | 22.09 | 2.63 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
