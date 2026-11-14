# Run report: prosmarthpa-cv-w30 | 2R-20% | run 2

- Started 2026-11-12 18:26:32 - finished 2026-11-12 18:42:05
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 253 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 3,001.86 |
| CPU Overutilization (%) - lower | 356.95 |
| Overutilization Time (min) - lower | 14.78 |
| CPU Overprovision (m) - lower | 132.02 |
| Overprovision Time (min) - higher | 0.42 |
| CPU Underprovision (m) - lower | 4,947.83 |
| Underprovision Time (min) - lower | 14.55 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67027 | 0 | 190 | 640 | 1000 | 74.56 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 518.18 | 65.69 | 14.55 | 6.32 | 0.42 | 1,386.17 | 14.43 |
| currencyservice | 932.41 | 49.00 | 14.78 | 9.09 | 0.42 | 1,890.91 | 14.55 |
| cartservice | 308.30 | 36.03 | 13.53 | 12.65 | 0.42 | 458.50 | 13.53 |
| adservice | 200.00 | 0.00 | 0.00 | 15.02 | 0.47 | 0.00 | 0.00 |
| checkoutservice | 137.94 | 34.10 | 13.53 | 7.51 | 0.55 | 182.61 | 13.53 |
| productcatalogservice | 154.55 | 73.18 | 14.50 | 5.53 | 0.36 | 461.26 | 14.50 |
| recommendationservice | 189.33 | 42.75 | 13.26 | 6.32 | 0.46 | 292.89 | 13.26 |
| paymentservice | 192.09 | 34.18 | 13.77 | 7.91 | 0.72 | 204.74 | 13.77 |
| shippingservice | 103.56 | 20.96 | 9.60 | 6.32 | 0.42 | 66.80 | 11.14 |
| emailservice | 146.25 | 1.07 | 0.56 | 49.80 | 7.35 | 3.95 | 0.56 |
| redis-cart | 119.25 | 0.00 | 0.00 | 5.53 | 0.59 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
