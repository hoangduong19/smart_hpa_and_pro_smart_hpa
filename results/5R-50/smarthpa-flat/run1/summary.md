# Run report: smarthpa-flat | 5R-50% | run 1

- Started 2026-10-15 14:01:06 - finished 2026-10-15 14:16:36
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 161 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 4,365.65 |
| CPU Overutilization (%) - lower | 90.56 |
| Overutilization Time (min) - lower | 11.10 |
| CPU Overprovision (m) - lower | 1,801.12 |
| Overprovision Time (min) - higher | 13.61 |
| CPU Underprovision (m) - lower | 18.63 |
| Underprovision Time (min) - lower | 1.38 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66768 | 0 | 190 | 720 | 1100 | 74.34 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 968.32 | 24.91 | 7.88 | 124.84 | 7.29 | 2.48 | 0.52 |
| currencyservice | 1,616.15 | 24.99 | 6.43 | 92.55 | 6.75 | 4.35 | 0.52 |
| cartservice | 356.52 | 8.73 | 2.72 | 190.06 | 2.87 | 0.00 | 0.00 |
| adservice | 204.97 | 2.61 | 0.71 | 243.48 | 3.37 | 6.21 | 0.51 |
| checkoutservice | 180.12 | 4.41 | 1.77 | 154.66 | 5.94 | 2.48 | 0.52 |
| productcatalogservice | 324.22 | 7.42 | 2.04 | 166.46 | 10.48 | 0.00 | 0.00 |
| recommendationservice | 255.28 | 10.88 | 4.76 | 214.29 | 11.25 | 1.86 | 0.51 |
| paymentservice | 178.26 | 3.33 | 1.78 | 145.96 | 5.48 | 0.00 | 0.00 |
| shippingservice | 111.80 | 3.28 | 1.62 | 131.06 | 3.66 | 1.24 | 0.36 |
| emailservice | 100.00 | 0.00 | 0.00 | 131.68 | 3.66 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 206.09 | 14.99 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
