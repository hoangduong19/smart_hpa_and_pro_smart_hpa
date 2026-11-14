# Run report: prosmarthpa-cv-w10 | 2R-20% | run 2

- Started 2026-11-12 17:22:50 - finished 2026-11-12 17:38:20
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 256 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,932.62 |
| CPU Overutilization (%) - lower | 341.48 |
| Overutilization Time (min) - lower | 14.81 |
| CPU Overprovision (m) - lower | 149.73 |
| Overprovision Time (min) - higher | 0.42 |
| CPU Underprovision (m) - lower | 5,210.16 |
| Underprovision Time (min) - lower | 14.56 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 68095 | 0 | 170 | 580 | 990 | 75.71 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 422.66 | 72.27 | 14.56 | 9.77 | 0.42 | 1,439.06 | 14.30 |
| currencyservice | 800.00 | 58.72 | 14.81 | 3.91 | 0.18 | 1,920.70 | 14.56 |
| cartservice | 293.75 | 40.70 | 13.55 | 21.09 | 0.48 | 496.88 | 13.55 |
| adservice | 200.00 | 0.61 | 0.75 | 19.53 | 0.42 | 5.47 | 0.75 |
| checkoutservice | 187.50 | 23.47 | 12.29 | 12.11 | 1.03 | 212.50 | 13.93 |
| productcatalogservice | 278.12 | 41.43 | 13.05 | 11.33 | 0.91 | 503.12 | 13.55 |
| recommendationservice | 184.77 | 45.22 | 13.55 | 10.94 | 0.69 | 314.45 | 13.41 |
| paymentservice | 189.06 | 39.19 | 14.05 | 10.94 | 0.69 | 262.11 | 14.05 |
| shippingservice | 116.80 | 19.28 | 8.19 | 10.94 | 0.69 | 53.52 | 10.17 |
| emailservice | 127.34 | 0.59 | 0.50 | 17.58 | 2.19 | 2.34 | 0.50 |
| redis-cart | 132.62 | 0.00 | 0.00 | 21.60 | 2.70 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
