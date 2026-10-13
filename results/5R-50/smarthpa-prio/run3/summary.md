# Run report: smarthpa-prio | 5R-50% | run 3

- Started 2026-10-13 18:10:57 - finished 2026-10-13 18:26:27
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 249 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 4,534.66 |
| CPU Overutilization (%) - lower | 76.17 |
| Overutilization Time (min) - lower | 11.06 |
| CPU Overprovision (m) - lower | 1,650.04 |
| Overprovision Time (min) - higher | 13.53 |
| CPU Underprovision (m) - lower | 15.66 |
| Underprovision Time (min) - lower | 1.44 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 67142 | 0 | 190 | 650 | 1100 | 74.66 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 999.20 | 22.06 | 6.76 | 138.96 | 9.95 | 0.00 | 0.00 |
| currencyservice | 1,662.65 | 27.73 | 7.23 | 79.12 | 7.00 | 6.02 | 0.46 |
| cartservice | 364.66 | 7.43 | 2.01 | 364.66 | 12.66 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 116.47 | 1.73 | 0.00 | 0.00 |
| checkoutservice | 171.89 | 0.47 | 0.26 | 247.79 | 14.97 | 0.00 | 0.00 |
| productcatalogservice | 340.16 | 3.82 | 1.48 | 154.62 | 12.74 | 0.00 | 0.00 |
| recommendationservice | 322.49 | 6.55 | 2.46 | 111.65 | 5.66 | 2.81 | 0.61 |
| paymentservice | 200.00 | 6.67 | 1.94 | 104.82 | 3.95 | 4.42 | 0.60 |
| shippingservice | 103.61 | 1.45 | 0.55 | 88.76 | 2.95 | 2.41 | 0.49 |
| emailservice | 100.00 | 0.00 | 0.00 | 106.02 | 3.71 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 137.19 | 14.97 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
