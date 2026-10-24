# Run report: prosmarthpa-rerun | 2R-20% | run 2

- Started 2026-10-24 12:54:32 - finished 2026-10-24 13:10:06
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 422 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,122.63 |
| CPU Overutilization (%) - lower | 418.85 |
| Overutilization Time (min) - lower | 14.75 |
| CPU Overprovision (m) - lower | 86.71 |
| Overprovision Time (min) - higher | 0.47 |
| CPU Underprovision (m) - lower | 6,528.20 |
| Underprovision Time (min) - lower | 14.50 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66737 | 0 | 200 | 660 | 1000 | 74.19 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 522.51 | 82.51 | 14.59 | 4.50 | 0.38 | 1,865.40 | 14.22 |
| currencyservice | 849.05 | 63.50 | 14.75 | 4.74 | 0.47 | 2,329.15 | 14.50 |
| cartservice | 383.89 | 34.23 | 12.76 | 13.27 | 0.59 | 602.84 | 13.99 |
| adservice | 200.00 | 2.91 | 2.27 | 10.43 | 0.22 | 9.48 | 0.78 |
| checkoutservice | 149.53 | 37.37 | 13.73 | 4.74 | 0.47 | 177.25 | 13.73 |
| productcatalogservice | 194.79 | 82.64 | 13.99 | 5.21 | 0.52 | 691.23 | 13.99 |
| recommendationservice | 194.55 | 59.89 | 13.51 | 6.16 | 0.98 | 450.47 | 13.51 |
| paymentservice | 192.18 | 40.20 | 14.02 | 7.58 | 0.93 | 263.27 | 14.02 |
| shippingservice | 170.38 | 14.24 | 9.54 | 5.45 | 0.72 | 133.41 | 12.70 |
| emailservice | 132.23 | 1.36 | 1.01 | 16.82 | 2.71 | 5.69 | 0.83 |
| redis-cart | 133.53 | 0.00 | 0.00 | 7.80 | 1.29 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
