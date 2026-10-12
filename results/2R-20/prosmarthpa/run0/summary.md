# Run report: prosmarthpa | 2R-20% | run 0

- Started 2026-10-08 14:49:07 - finished 2026-10-08 14:52:38
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 100 users, spawn rate 0.67/s, 180 s
- Knowledge Base rows: 100 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,382.50 |
| CPU Overutilization (%) - lower | 166.63 |
| Overutilization Time (min) - lower | 2.32 |
| CPU Overprovision (m) - lower | 517.70 |
| Overprovision Time (min) - higher | 0.83 |
| CPU Underprovision (m) - lower | 1,791.00 |
| Underprovision Time (min) - lower | 2.17 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 4737 | 0 | 170 | 450 | 770 | 27.02 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 480.00 | 21.54 | 2.08 | 69.00 | 1.10 | 331.00 | 1.59 |
| currencyservice | 508.00 | 33.20 | 2.32 | 26.00 | 0.63 | 718.00 | 2.08 |
| cartservice | 328.00 | 5.61 | 0.57 | 130.00 | 0.92 | 154.00 | 1.89 |
| adservice | 328.00 | 7.15 | 0.82 | 70.00 | 0.87 | 174.00 | 1.59 |
| checkoutservice | 100.00 | 16.93 | 1.33 | 29.00 | 0.67 | 57.00 | 1.33 |
| productcatalogservice | 100.00 | 40.71 | 1.77 | 36.00 | 0.92 | 184.00 | 1.77 |
| recommendationservice | 165.00 | 12.70 | 1.49 | 35.00 | 0.83 | 58.00 | 1.49 |
| paymentservice | 100.00 | 26.54 | 1.77 | 29.00 | 0.67 | 105.00 | 1.77 |
| shippingservice | 100.00 | 2.26 | 0.32 | 29.00 | 0.67 | 10.00 | 0.32 |
| emailservice | 100.00 | 0.00 | 0.00 | 29.00 | 0.67 | 0.00 | 0.00 |
| redis-cart | 73.50 | 0.00 | 0.00 | 35.70 | 1.57 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
