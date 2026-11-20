# Run report: smarthpa-warmup | 2R-20% | run 2

- Started 2026-11-19 17:58:17 - finished 2026-11-19 18:13:48
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 514 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,397.24 |
| CPU Overutilization (%) - lower | 416.25 |
| Overutilization Time (min) - lower | 14.76 |
| CPU Overprovision (m) - lower | 131.09 |
| Overprovision Time (min) - higher | 0.24 |
| CPU Underprovision (m) - lower | 3,769.84 |
| Underprovision Time (min) - lower | 14.76 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 70009 | 0 | 310 | 1000 | 1200 | 77.87 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 435.80 | 73.26 | 14.51 | 4.47 | 0.49 | 1,151.17 | 14.51 |
| currencyservice | 195.72 | 98.11 | 14.76 | 2.33 | 0.24 | 858.56 | 14.76 |
| cartservice | 389.88 | 29.31 | 14.32 | 8.95 | 0.49 | 288.33 | 14.06 |
| adservice | 234.24 | 5.11 | 3.27 | 8.95 | 0.49 | 37.74 | 2.51 |
| checkoutservice | 194.55 | 28.52 | 14.25 | 5.06 | 0.74 | 135.80 | 13.92 |
| productcatalogservice | 195.14 | 69.71 | 14.51 | 4.47 | 0.49 | 551.75 | 14.45 |
| recommendationservice | 194.94 | 64.29 | 14.51 | 4.47 | 0.49 | 484.24 | 14.25 |
| paymentservice | 194.94 | 36.81 | 14.51 | 4.47 | 0.49 | 211.67 | 14.25 |
| shippingservice | 192.02 | 0.09 | 0.05 | 7.59 | 1.48 | 0.00 | 0.00 |
| emailservice | 100.00 | 11.02 | 7.27 | 10.31 | 2.01 | 50.58 | 7.27 |
| redis-cart | 70.00 | 0.00 | 0.00 | 70.00 | 15.00 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
