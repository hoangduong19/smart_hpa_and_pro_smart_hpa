# Run report: smarthpa | 5R-50% | run 0

- Started 2026-10-02 14:18:41 - finished 2026-10-02 14:22:29
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 100 users, spawn rate 2/s, 180 s
- Knowledge Base rows: 58 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 1,570.00 |
| CPU Overutilization (%) - lower | 83.74 |
| Overutilization Time (min) - lower | 1.78 |
| CPU Overprovision (m) - lower | 4,514.48 |
| Overprovision Time (min) - higher | 2.99 |
| CPU Underprovision (m) - lower | 0.00 |
| Underprovision Time (min) - lower | 0.00 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 6532 | 35 | 210 | 1100 | 2100 | 37.41 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 220.69 | 22.55 | 1.02 | 243.10 | 1.98 | 0.00 | 0.00 |
| currencyservice | 210.34 | 46.93 | 1.32 | 270.69 | 2.20 | 0.00 | 0.00 |
| cartservice | 200.00 | 0.00 | 0.00 | 679.31 | 2.14 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 731.03 | 2.39 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 0.00 | 0.00 | 400.00 | 2.99 | 0.00 | 0.00 |
| productcatalogservice | 127.59 | 2.62 | 0.09 | 368.97 | 2.99 | 0.00 | 0.00 |
| recommendationservice | 125.86 | 2.79 | 0.49 | 368.97 | 2.99 | 0.00 | 0.00 |
| paymentservice | 115.52 | 8.84 | 0.55 | 372.41 | 2.99 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 2.99 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 2.99 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 2.99 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
