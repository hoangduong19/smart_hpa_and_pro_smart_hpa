# Run report: smarthpa-warmup | 2R-20% | run 3

- Started 2026-11-19 18:41:52 - finished 2026-11-19 18:57:23
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 504 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,469.15 |
| CPU Overutilization (%) - lower | 431.00 |
| Overutilization Time (min) - lower | 14.58 |
| CPU Overprovision (m) - lower | 58.87 |
| Overprovision Time (min) - higher | 0.41 |
| CPU Underprovision (m) - lower | 3,622.02 |
| Underprovision Time (min) - lower | 14.58 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 70476 | 0 | 350 | 900 | 1300 | 78.37 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 276.59 | 114.98 | 14.58 | 3.97 | 0.41 | 1,228.97 | 14.58 |
| currencyservice | 195.24 | 97.56 | 14.58 | 3.97 | 0.41 | 853.37 | 14.58 |
| cartservice | 390.48 | 29.70 | 14.58 | 7.94 | 0.41 | 275.00 | 14.33 |
| adservice | 306.35 | 5.45 | 4.45 | 7.94 | 0.41 | 36.90 | 3.18 |
| checkoutservice | 194.64 | 29.42 | 14.03 | 4.96 | 0.96 | 155.36 | 13.98 |
| productcatalogservice | 195.44 | 57.44 | 14.58 | 3.97 | 0.41 | 428.77 | 14.50 |
| recommendationservice | 194.44 | 56.54 | 14.33 | 4.76 | 0.66 | 416.47 | 14.03 |
| paymentservice | 194.44 | 37.41 | 14.33 | 4.76 | 0.66 | 218.06 | 14.33 |
| shippingservice | 194.05 | 1.56 | 1.01 | 5.56 | 1.41 | 6.94 | 0.96 |
| emailservice | 192.06 | 0.83 | 0.49 | 6.75 | 1.91 | 2.18 | 0.34 |
| redis-cart | 135.42 | 0.10 | 0.05 | 4.31 | 1.66 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
