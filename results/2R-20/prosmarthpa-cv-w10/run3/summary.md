# Run report: prosmarthpa-cv-w10 | 2R-20% | run 3

- Started 2026-11-13 02:04:04 - finished 2026-11-13 02:19:34
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 419 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,452.82 |
| CPU Overutilization (%) - lower | 432.56 |
| Overutilization Time (min) - lower | 14.55 |
| CPU Overprovision (m) - lower | 100.43 |
| Overprovision Time (min) - higher | 0.69 |
| CPU Underprovision (m) - lower | 4,466.11 |
| Underprovision Time (min) - lower | 14.29 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66889 | 0 | 200 | 680 | 1000 | 74.38 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 286.63 | 114.93 | 14.55 | 5.49 | 0.44 | 1,478.04 | 14.29 |
| currencyservice | 657.76 | 51.98 | 14.55 | 6.44 | 0.69 | 1,139.62 | 14.29 |
| cartservice | 200.00 | 59.35 | 14.04 | 12.41 | 0.52 | 508.83 | 14.04 |
| adservice | 200.00 | 0.00 | 0.00 | 15.75 | 0.44 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 45.53 | 13.30 | 6.92 | 0.95 | 174.46 | 13.30 |
| productcatalogservice | 287.11 | 47.45 | 13.05 | 9.07 | 1.20 | 491.41 | 13.05 |
| recommendationservice | 193.56 | 52.11 | 13.81 | 6.44 | 0.69 | 374.94 | 13.81 |
| paymentservice | 192.60 | 35.47 | 13.84 | 7.64 | 0.84 | 221.48 | 13.84 |
| shippingservice | 100.00 | 25.73 | 12.31 | 6.44 | 0.69 | 77.33 | 12.31 |
| emailservice | 100.00 | 0.00 | 0.00 | 6.44 | 0.69 | 0.00 | 0.00 |
| redis-cart | 135.16 | 0.00 | 0.00 | 17.37 | 2.94 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
