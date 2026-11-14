# Run report: prosmarthpa-cv-w5 | 2R-20% | run 1

- Started 2026-11-12 14:54:43 - finished 2026-11-12 15:10:14
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 319 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,030.91 |
| CPU Overutilization (%) - lower | 332.37 |
| Overutilization Time (min) - lower | 14.73 |
| CPU Overprovision (m) - lower | 137.84 |
| Overprovision Time (min) - higher | 0.49 |
| CPU Underprovision (m) - lower | 4,766.14 |
| Underprovision Time (min) - lower | 14.50 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66724 | 0 | 200 | 710 | 1000 | 74.17 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 498.43 | 65.25 | 14.73 | 4.70 | 0.26 | 1,310.34 | 14.20 |
| currencyservice | 808.15 | 47.00 | 14.46 | 8.78 | 0.53 | 1,613.17 | 14.46 |
| cartservice | 381.19 | 27.63 | 12.20 | 18.81 | 0.79 | 487.77 | 13.93 |
| adservice | 200.00 | 0.39 | 0.50 | 17.55 | 0.53 | 3.76 | 0.50 |
| checkoutservice | 190.60 | 24.88 | 12.20 | 9.72 | 0.92 | 222.88 | 13.70 |
| productcatalogservice | 190.60 | 63.20 | 14.23 | 8.78 | 0.53 | 497.49 | 13.97 |
| recommendationservice | 190.91 | 46.83 | 13.66 | 9.09 | 0.56 | 342.32 | 13.66 |
| paymentservice | 191.54 | 35.15 | 13.75 | 10.03 | 0.76 | 222.57 | 13.75 |
| shippingservice | 110.34 | 21.38 | 8.66 | 9.40 | 0.79 | 62.07 | 10.65 |
| emailservice | 135.74 | 0.64 | 0.51 | 18.81 | 2.53 | 3.76 | 0.51 |
| redis-cart | 133.42 | 0.00 | 0.00 | 22.16 | 3.28 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
