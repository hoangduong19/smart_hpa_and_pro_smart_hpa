# Run report: prosmarthpa | 2R-20% | run 1

- Started 2026-10-08 14:58:47 - finished 2026-10-08 15:14:17
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 414 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,080.65 |
| CPU Overutilization (%) - lower | 391.33 |
| Overutilization Time (min) - lower | 14.72 |
| CPU Overprovision (m) - lower | 74.61 |
| Overprovision Time (min) - higher | 0.51 |
| CPU Underprovision (m) - lower | 5,906.04 |
| Underprovision Time (min) - lower | 14.45 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65964 | 0 | 200 | 780 | 1200 | 73.37 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 536.96 | 71.71 | 14.20 | 6.04 | 0.76 | 1,578.74 | 14.20 |
| currencyservice | 758.21 | 62.53 | 14.72 | 6.04 | 0.51 | 2,115.70 | 14.45 |
| cartservice | 387.92 | 33.25 | 12.70 | 12.08 | 0.76 | 580.68 | 14.20 |
| adservice | 200.00 | 11.09 | 6.55 | 6.76 | 0.25 | 85.02 | 5.80 |
| checkoutservice | 193.48 | 27.95 | 12.20 | 8.70 | 1.26 | 156.04 | 12.20 |
| productcatalogservice | 194.20 | 77.88 | 13.78 | 5.07 | 0.51 | 630.92 | 13.70 |
| recommendationservice | 193.96 | 55.18 | 13.70 | 6.04 | 0.76 | 411.35 | 13.70 |
| paymentservice | 193.96 | 35.66 | 13.70 | 6.04 | 0.76 | 218.36 | 13.70 |
| shippingservice | 160.63 | 11.62 | 7.08 | 5.07 | 0.51 | 107.49 | 11.91 |
| emailservice | 135.02 | 4.44 | 2.77 | 6.52 | 0.76 | 21.74 | 2.60 |
| redis-cart | 126.30 | 0.00 | 0.00 | 6.26 | 1.05 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
