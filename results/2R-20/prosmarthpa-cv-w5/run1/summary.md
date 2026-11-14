# Run report: prosmarthpa-cv-w5 | 2R-20% | run 1

- Started 2026-11-12 22:11:17 - finished 2026-11-12 22:26:48
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 503 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,472.49 |
| CPU Overutilization (%) - lower | 445.71 |
| Overutilization Time (min) - lower | 14.78 |
| CPU Overprovision (m) - lower | 102.41 |
| Overprovision Time (min) - higher | 0.45 |
| CPU Underprovision (m) - lower | 2,201.79 |
| Underprovision Time (min) - lower | 14.55 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 59352 | 0 | 400 | 1200 | 1400 | 66.02 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 100.00 | 172.76 | 14.27 | 4.77 | 0.45 | 795.03 | 14.27 |
| currencyservice | 858.65 | 23.76 | 14.53 | 6.96 | 0.45 | 191.25 | 14.30 |
| cartservice | 388.87 | 19.93 | 11.53 | 6.36 | 0.47 | 159.44 | 11.31 |
| adservice | 200.00 | 0.00 | 0.00 | 5.17 | 0.22 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 38.04 | 13.53 | 4.77 | 0.45 | 162.23 | 13.53 |
| productcatalogservice | 288.87 | 27.05 | 13.02 | 10.74 | 1.47 | 175.15 | 13.02 |
| recommendationservice | 100.00 | 87.48 | 13.78 | 5.37 | 0.53 | 391.65 | 13.78 |
| paymentservice | 100.00 | 58.37 | 14.02 | 4.97 | 0.48 | 250.30 | 14.02 |
| shippingservice | 100.00 | 18.33 | 12.04 | 4.97 | 0.48 | 76.74 | 12.04 |
| emailservice | 100.00 | 0.00 | 0.00 | 4.77 | 0.45 | 0.00 | 0.00 |
| redis-cart | 136.10 | 0.00 | 0.00 | 43.56 | 8.95 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
