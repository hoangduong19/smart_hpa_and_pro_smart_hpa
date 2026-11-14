# Run report: prosmarthpa-cv | 2R-20% | run 3

- Started 2026-11-12 21:06:45 - finished 2026-11-12 21:22:15
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 527 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,387.08 |
| CPU Overutilization (%) - lower | 468.60 |
| Overutilization Time (min) - lower | 14.54 |
| CPU Overprovision (m) - lower | 76.32 |
| Overprovision Time (min) - higher | 0.51 |
| CPU Underprovision (m) - lower | 3,462.45 |
| Underprovision Time (min) - lower | 14.48 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 61383 | 0 | 300 | 1100 | 1500 | 68.28 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 474.38 | 72.34 | 14.54 | 6.83 | 0.69 | 1,358.25 | 14.30 |
| currencyservice | 749.72 | 26.58 | 14.48 | 9.49 | 0.76 | 305.12 | 14.23 |
| cartservice | 200.00 | 50.53 | 13.49 | 10.25 | 0.45 | 415.56 | 13.49 |
| adservice | 200.00 | 0.00 | 0.00 | 10.63 | 0.51 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 42.60 | 13.49 | 6.64 | 0.67 | 160.91 | 13.49 |
| productcatalogservice | 100.00 | 116.81 | 14.48 | 5.12 | 0.45 | 536.81 | 14.48 |
| recommendationservice | 100.00 | 90.23 | 14.23 | 5.12 | 0.45 | 402.47 | 14.23 |
| paymentservice | 192.98 | 30.45 | 13.49 | 7.02 | 0.76 | 161.86 | 13.49 |
| shippingservice | 100.00 | 23.50 | 12.25 | 5.12 | 0.45 | 77.23 | 12.25 |
| emailservice | 100.00 | 0.00 | 0.00 | 5.31 | 0.51 | 0.00 | 0.00 |
| redis-cart | 70.00 | 15.55 | 10.25 | 4.78 | 0.69 | 44.23 | 10.25 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
