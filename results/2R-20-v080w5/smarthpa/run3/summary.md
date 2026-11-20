# Run report: smarthpa | 2R-20% | run 3

- Started 2026-11-20 06:09:42 - finished 2026-11-20 06:25:12
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 494 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,370.63 |
| CPU Overutilization (%) - lower | 636.26 |
| Overutilization Time (min) - lower | 14.66 |
| CPU Overprovision (m) - lower | 60.79 |
| Overprovision Time (min) - higher | 0.59 |
| CPU Underprovision (m) - lower | 5,718.22 |
| Underprovision Time (min) - lower | 14.41 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 76277 | 0 | 200 | 510 | 1100 | 84.82 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 854.66 | 61.98 | 14.66 | 3.24 | 0.34 | 1,939.27 | 14.16 |
| currencyservice | 288.87 | 90.05 | 14.66 | 3.24 | 0.34 | 1,097.17 | 14.41 |
| cartservice | 200.00 | 83.11 | 14.41 | 6.48 | 0.34 | 728.34 | 14.41 |
| adservice | 200.00 | 12.04 | 7.99 | 10.12 | 0.55 | 86.64 | 6.24 |
| checkoutservice | 194.33 | 41.29 | 13.97 | 5.26 | 0.59 | 265.18 | 13.92 |
| productcatalogservice | 100.00 | 170.93 | 14.41 | 5.06 | 0.55 | 805.06 | 14.41 |
| recommendationservice | 100.00 | 123.63 | 14.41 | 5.06 | 0.55 | 566.19 | 14.41 |
| paymentservice | 100.00 | 0.38 | 0.25 | 5.06 | 0.55 | 1.82 | 0.25 |
| shippingservice | 100.00 | 40.52 | 13.92 | 5.06 | 0.55 | 172.06 | 13.92 |
| emailservice | 100.00 | 12.22 | 8.47 | 5.26 | 0.59 | 56.48 | 8.47 |
| redis-cart | 132.77 | 0.10 | 0.05 | 6.94 | 1.34 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
