# Run report: k8shpa | 5R-50% | run 0

- Started 2026-10-02 14:23:51 - finished 2026-10-02 14:27:21
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 100 users, spawn rate 2/s, 180 s
- Knowledge Base rows: 86 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 1,910.70 |
| CPU Overutilization (%) - lower | 94.23 |
| Overutilization Time (min) - lower | 2.67 |
| CPU Overprovision (m) - lower | 4,266.05 |
| Overprovision Time (min) - higher | 2.97 |
| CPU Underprovision (m) - lower | 0.00 |
| Underprovision Time (min) - lower | 0.00 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 6768 | 0 | 240 | 790 | 1400 | 37.92 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 356.98 | 23.30 | 1.26 | 101.16 | 0.92 | 0.00 | 0.00 |
| currencyservice | 301.16 | 60.09 | 2.67 | 84.88 | 0.82 | 0.00 | 0.00 |
| cartservice | 200.00 | 0.00 | 0.00 | 800.00 | 2.97 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 800.00 | 2.97 | 0.00 | 0.00 |
| checkoutservice | 100.00 | 0.00 | 0.00 | 400.00 | 2.97 | 0.00 | 0.00 |
| productcatalogservice | 162.79 | 4.13 | 0.25 | 331.40 | 2.97 | 0.00 | 0.00 |
| recommendationservice | 160.47 | 4.69 | 0.52 | 331.40 | 2.97 | 0.00 | 0.00 |
| paymentservice | 159.30 | 2.02 | 0.50 | 337.21 | 2.97 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 2.97 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 2.97 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 2.97 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
