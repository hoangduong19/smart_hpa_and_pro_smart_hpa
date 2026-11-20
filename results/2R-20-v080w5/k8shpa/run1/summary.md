# Run report: k8shpa | 2R-20% | run 1

- Started 2026-11-20 03:08:54 - finished 2026-11-20 03:24:25
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 446 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,139.84 |
| CPU Overutilization (%) - lower | 510.01 |
| Overutilization Time (min) - lower | 14.62 |
| CPU Overprovision (m) - lower | 384.04 |
| Overprovision Time (min) - higher | 0.37 |
| CPU Underprovision (m) - lower | 4,297.53 |
| Underprovision Time (min) - lower | 14.62 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 74053 | 0 | 260 | 670 | 1100 | 82.36 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 193.05 | 177.77 | 14.60 | 4.04 | 0.39 | 1,623.54 | 14.60 |
| currencyservice | 193.05 | 91.33 | 14.62 | 3.81 | 0.37 | 741.26 | 14.62 |
| cartservice | 385.20 | 40.74 | 14.35 | 20.63 | 0.64 | 514.80 | 14.10 |
| adservice | 200.00 | 0.79 | 0.49 | 193.27 | 14.49 | 0.00 | 0.00 |
| checkoutservice | 192.60 | 36.02 | 14.10 | 7.17 | 0.88 | 214.13 | 13.85 |
| productcatalogservice | 192.83 | 78.49 | 14.37 | 6.28 | 0.62 | 642.60 | 14.37 |
| recommendationservice | 192.83 | 64.07 | 14.35 | 6.50 | 0.64 | 483.18 | 14.10 |
| paymentservice | 100.00 | 0.33 | 0.24 | 98.43 | 14.74 | 0.00 | 0.00 |
| shippingservice | 192.38 | 16.88 | 11.05 | 7.40 | 1.13 | 75.78 | 10.80 |
| emailservice | 164.35 | 3.22 | 2.01 | 31.17 | 4.86 | 2.24 | 0.53 |
| redis-cart | 133.57 | 0.38 | 0.41 | 5.34 | 1.38 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
