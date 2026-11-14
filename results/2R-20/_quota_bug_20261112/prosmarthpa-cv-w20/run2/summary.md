# Run report: prosmarthpa-cv-w20 | 2R-20% | run 2

- Started 2026-11-12 18:05:12 - finished 2026-11-12 18:20:46
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 218 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,090.50 |
| CPU Overutilization (%) - lower | 360.54 |
| Overutilization Time (min) - lower | 14.58 |
| CPU Overprovision (m) - lower | 148.30 |
| Overprovision Time (min) - higher | 0.37 |
| CPU Underprovision (m) - lower | 5,613.76 |
| Underprovision Time (min) - lower | 14.51 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67769 | 0 | 190 | 580 | 930 | 75.38 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 610.55 | 60.18 | 14.58 | 6.88 | 0.30 | 1,449.08 | 14.31 |
| currencyservice | 814.68 | 62.56 | 14.58 | 10.55 | 0.45 | 2,406.42 | 14.12 |
| cartservice | 312.84 | 34.99 | 13.55 | 13.76 | 0.30 | 461.47 | 13.33 |
| adservice | 307.34 | 0.83 | 0.52 | 16.51 | 0.57 | 76.15 | 5.32 |
| checkoutservice | 144.50 | 30.47 | 13.33 | 8.72 | 0.87 | 173.39 | 13.33 |
| productcatalogservice | 153.21 | 75.53 | 14.01 | 8.26 | 0.57 | 488.99 | 14.01 |
| recommendationservice | 187.61 | 44.23 | 13.28 | 8.72 | 0.61 | 318.35 | 13.25 |
| paymentservice | 192.20 | 31.29 | 14.02 | 7.80 | 0.37 | 175.23 | 14.02 |
| shippingservice | 109.63 | 20.16 | 8.18 | 8.26 | 0.57 | 62.84 | 10.94 |
| emailservice | 139.45 | 0.30 | 0.25 | 49.54 | 7.88 | 1.83 | 0.25 |
| redis-cart | 118.49 | 0.00 | 0.00 | 9.31 | 1.41 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
