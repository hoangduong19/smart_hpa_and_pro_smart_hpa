# Run report: smarthpa | 2R-20% | run 1

- Started 2026-11-20 02:41:47 - finished 2026-11-20 02:57:19
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 464 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,395.17 |
| CPU Overutilization (%) - lower | 578.58 |
| Overutilization Time (min) - lower | 14.76 |
| CPU Overprovision (m) - lower | 44.31 |
| Overprovision Time (min) - higher | 0.50 |
| CPU Underprovision (m) - lower | 5,959.05 |
| Underprovision Time (min) - lower | 14.50 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 75033 | 0 | 190 | 610 | 1200 | 83.48 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 774.57 | 75.89 | 14.74 | 2.59 | 0.26 | 2,276.51 | 14.25 |
| currencyservice | 293.10 | 72.82 | 14.74 | 2.59 | 0.26 | 849.78 | 14.50 |
| cartservice | 200.00 | 90.29 | 14.50 | 5.17 | 0.26 | 805.60 | 14.50 |
| adservice | 200.00 | 16.12 | 8.73 | 10.78 | 0.50 | 113.36 | 7.99 |
| checkoutservice | 196.34 | 36.48 | 13.84 | 3.02 | 0.50 | 214.01 | 13.76 |
| productcatalogservice | 197.20 | 103.90 | 14.29 | 2.37 | 0.23 | 885.34 | 14.25 |
| recommendationservice | 100.00 | 123.61 | 14.25 | 3.02 | 0.50 | 562.72 | 14.25 |
| paymentservice | 100.00 | 0.93 | 0.51 | 3.02 | 0.50 | 3.88 | 0.51 |
| shippingservice | 100.00 | 40.44 | 13.76 | 3.02 | 0.50 | 169.61 | 13.76 |
| emailservice | 100.00 | 18.00 | 11.74 | 3.02 | 0.50 | 78.23 | 11.74 |
| redis-cart | 133.97 | 0.09 | 0.06 | 5.73 | 1.24 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
