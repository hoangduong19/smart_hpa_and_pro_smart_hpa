# Run report: prosmarthpa-cv | 2R-20% | run 3

- Started 2026-11-12 18:47:45 - finished 2026-11-12 19:03:15
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 230 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,957.17 |
| CPU Overutilization (%) - lower | 359.86 |
| Overutilization Time (min) - lower | 14.70 |
| CPU Overprovision (m) - lower | 113.70 |
| Overprovision Time (min) - higher | 0.36 |
| CPU Underprovision (m) - lower | 4,896.09 |
| Underprovision Time (min) - lower | 14.60 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66451 | 0 | 190 | 700 | 1100 | 73.84 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 510.00 | 66.11 | 14.43 | 7.39 | 0.53 | 1,393.04 | 14.39 |
| currencyservice | 929.13 | 46.54 | 14.48 | 5.65 | 0.26 | 1,800.00 | 14.38 |
| cartservice | 301.74 | 38.67 | 13.92 | 13.91 | 0.36 | 476.52 | 13.92 |
| adservice | 200.00 | 1.29 | 1.48 | 11.30 | 0.26 | 12.17 | 1.48 |
| checkoutservice | 122.17 | 38.00 | 13.18 | 7.39 | 0.39 | 182.17 | 13.18 |
| productcatalogservice | 149.13 | 72.76 | 13.92 | 7.39 | 0.53 | 453.48 | 13.92 |
| recommendationservice | 188.26 | 43.96 | 13.92 | 8.70 | 0.65 | 304.35 | 13.92 |
| paymentservice | 191.74 | 32.43 | 13.43 | 8.26 | 0.78 | 207.39 | 13.43 |
| shippingservice | 111.74 | 19.64 | 9.64 | 7.39 | 0.53 | 65.22 | 11.11 |
| emailservice | 136.09 | 0.47 | 0.21 | 28.70 | 4.01 | 1.74 | 0.21 |
| redis-cart | 117.17 | 0.00 | 0.00 | 7.61 | 0.88 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
