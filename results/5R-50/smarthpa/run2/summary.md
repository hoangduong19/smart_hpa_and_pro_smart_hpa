# Run report: smarthpa | 5R-50% | run 2

- Started 2026-10-02 15:53:02 - finished 2026-10-02 16:08:32
- Scenario 5R-50%: maxR = 5, CPU threshold = 50%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 310 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 4,018.71 |
| CPU Overutilization (%) - lower | 209.47 |
| Overutilization Time (min) - lower | 14.28 |
| CPU Overprovision (m) - lower | 716.52 |
| Overprovision Time (min) - higher | 4.13 |
| CPU Underprovision (m) - lower | 576.77 |
| Underprovision Time (min) - lower | 10.87 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 63887 | 0 | 240 | 1000 | 1600 | 71.01 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 851.94 | 56.06 | 13.22 | 37.42 | 1.83 | 246.13 | 10.41 |
| currencyservice | 1,359.03 | 52.15 | 13.69 | 31.94 | 2.03 | 140.00 | 10.66 |
| cartservice | 356.77 | 12.37 | 3.13 | 66.45 | 0.84 | 34.84 | 2.36 |
| adservice | 200.00 | 0.00 | 0.00 | 82.58 | 1.12 | 0.00 | 0.00 |
| checkoutservice | 182.58 | 4.88 | 1.38 | 81.61 | 3.59 | 8.71 | 1.23 |
| productcatalogservice | 350.32 | 31.99 | 8.51 | 70.32 | 4.13 | 57.74 | 8.10 |
| recommendationservice | 263.87 | 40.86 | 10.64 | 71.29 | 3.35 | 70.00 | 9.89 |
| paymentservice | 184.19 | 8.51 | 2.28 | 79.68 | 4.13 | 14.19 | 2.02 |
| shippingservice | 100.00 | 2.65 | 0.79 | 61.94 | 2.32 | 5.16 | 0.79 |
| emailservice | 100.00 | 0.00 | 0.00 | 70.97 | 3.12 | 0.00 | 0.00 |
| redis-cart | 70.00 | 0.00 | 0.00 | 62.32 | 3.83 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
