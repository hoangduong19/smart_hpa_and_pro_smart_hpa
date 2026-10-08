# Run report: smarthpa | 2R-20% | run 2

- Started 2026-10-05 10:07:41 - finished 2026-10-05 10:23:11
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 344 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,450.76 |
| CPU Overutilization (%) - lower | 662.76 |
| Overutilization Time (min) - lower | 14.64 |
| CPU Overprovision (m) - lower | 70.23 |
| Overprovision Time (min) - higher | 0.61 |
| CPU Underprovision (m) - lower | 5,647.97 |
| Underprovision Time (min) - lower | 14.38 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 62766 | 0 | 300 | 990 | 1500 | 69.78 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 478.49 | 95.92 | 14.64 | 2.91 | 0.34 | 1,927.91 | 14.20 |
| currencyservice | 854.65 | 44.52 | 14.64 | 2.91 | 0.34 | 1,087.50 | 14.38 |
| cartservice | 200.00 | 66.90 | 13.88 | 5.81 | 0.34 | 573.84 | 13.88 |
| adservice | 200.00 | 4.50 | 3.26 | 7.56 | 0.34 | 32.56 | 2.49 |
| checkoutservice | 100.00 | 66.81 | 13.64 | 4.94 | 0.61 | 296.80 | 13.64 |
| productcatalogservice | 100.00 | 150.68 | 14.12 | 4.65 | 0.56 | 696.51 | 14.12 |
| recommendationservice | 100.00 | 125.95 | 14.12 | 4.65 | 0.56 | 578.78 | 14.12 |
| paymentservice | 100.00 | 65.17 | 14.12 | 4.94 | 0.61 | 280.23 | 14.12 |
| shippingservice | 100.00 | 32.14 | 12.61 | 4.94 | 0.61 | 127.03 | 12.61 |
| emailservice | 100.00 | 10.03 | 7.48 | 4.94 | 0.61 | 46.80 | 7.48 |
| redis-cart | 117.62 | 0.12 | 0.09 | 21.98 | 4.08 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
