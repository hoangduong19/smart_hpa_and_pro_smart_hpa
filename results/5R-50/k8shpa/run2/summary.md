# Run report: k8shpa | 5R-50% | run 2

- Started 2026-10-02 15:32:16 - finished 2026-10-02 15:47:46
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 353 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,950.17 |
| CPU Overutilization (%) - lower | 267.48 |
| Overutilization Time (min) - lower | 14.62 |
| CPU Overprovision (m) - lower | 3,441.76 |
| Overprovision Time (min) - higher | 0.74 |
| CPU Underprovision (m) - lower | 1,475.64 |
| Underprovision Time (min) - lower | 14.25 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 66511 | 0 | 200 | 640 | 1100 | 74.09 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 448.16 | 99.46 | 13.90 | 43.63 | 2.19 | 569.12 | 12.81 |
| currencyservice | 462.32 | 137.75 | 14.62 | 26.06 | 0.74 | 906.52 | 14.25 |
| cartservice | 471.95 | 4.49 | 1.45 | 626.63 | 15.00 | 0.00 | 0.00 |
| adservice | 200.00 | 0.00 | 0.00 | 803.40 | 15.00 | 0.00 | 0.00 |
| checkoutservice | 179.60 | 9.35 | 2.33 | 302.55 | 15.00 | 0.00 | 0.00 |
| productcatalogservice | 411.90 | 4.81 | 1.17 | 84.42 | 5.76 | 0.00 | 0.00 |
| recommendationservice | 322.95 | 4.61 | 1.52 | 171.67 | 15.00 | 0.00 | 0.00 |
| paymentservice | 183.29 | 7.00 | 2.27 | 303.40 | 15.00 | 0.00 | 0.00 |
| shippingservice | 100.00 | 0.00 | 0.00 | 400.00 | 15.00 | 0.00 | 0.00 |
| emailservice | 100.00 | 0.00 | 0.00 | 400.00 | 15.00 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 280.00 | 15.00 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
