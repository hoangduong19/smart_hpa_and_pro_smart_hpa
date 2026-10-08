# Run report: smarthpa | 2R-20% | run 1

- Started 2026-10-05 09:26:09 - finished 2026-10-05 09:41:39
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 353 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,434.22 |
| CPU Overutilization (%) - lower | 684.46 |
| Overutilization Time (min) - lower | 14.57 |
| CPU Overprovision (m) - lower | 86.20 |
| Overprovision Time (min) - higher | 0.64 |
| CPU Underprovision (m) - lower | 4,683.06 |
| Underprovision Time (min) - lower | 14.34 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62745 | 0 | 300 | 930 | 1300 | 69.76 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 192.92 | 158.05 | 14.34 | 5.38 | 0.64 | 1,426.91 | 14.34 |
| currencyservice | 1,129.46 | 34.81 | 14.57 | 3.40 | 0.40 | 841.93 | 14.34 |
| cartservice | 200.00 | 61.08 | 13.83 | 6.80 | 0.40 | 525.78 | 13.83 |
| adservice | 200.00 | 1.12 | 0.78 | 10.76 | 0.64 | 3.40 | 0.25 |
| checkoutservice | 100.00 | 67.31 | 13.83 | 5.38 | 0.64 | 294.62 | 13.83 |
| productcatalogservice | 100.00 | 136.38 | 14.07 | 5.38 | 0.64 | 629.46 | 14.07 |
| recommendationservice | 100.00 | 122.08 | 14.07 | 5.38 | 0.64 | 562.32 | 14.07 |
| paymentservice | 100.00 | 66.83 | 14.07 | 5.38 | 0.64 | 279.32 | 14.07 |
| shippingservice | 100.00 | 29.34 | 12.58 | 5.38 | 0.64 | 86.40 | 12.58 |
| emailservice | 100.00 | 6.89 | 4.89 | 5.38 | 0.64 | 31.73 | 4.89 |
| redis-cart | 111.84 | 0.57 | 0.54 | 27.56 | 5.36 | 1.19 | 0.39 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
