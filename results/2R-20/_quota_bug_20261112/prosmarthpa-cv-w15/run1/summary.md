# Run report: prosmarthpa-cv-w15 | 2R-20% | run 1

- Started 2026-11-12 15:37:05 - finished 2026-11-12 15:52:35
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 306 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,905.33 |
| CPU Overutilization (%) - lower | 354.97 |
| Overutilization Time (min) - lower | 14.55 |
| CPU Overprovision (m) - lower | 145.59 |
| Overprovision Time (min) - higher | 0.43 |
| CPU Underprovision (m) - lower | 5,230.72 |
| Underprovision Time (min) - lower | 14.55 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 68371 | 0 | 170 | 540 | 900 | 76.02 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 366.01 | 90.15 | 14.55 | 8.50 | 0.43 | 1,564.05 | 14.30 |
| currencyservice | 799.67 | 55.17 | 14.55 | 8.50 | 0.43 | 1,769.28 | 14.55 |
| cartservice | 313.73 | 37.93 | 13.79 | 18.95 | 0.50 | 483.01 | 13.79 |
| adservice | 200.00 | 0.22 | 0.25 | 16.99 | 0.43 | 1.96 | 0.25 |
| checkoutservice | 189.54 | 21.41 | 12.04 | 10.46 | 0.93 | 202.61 | 13.79 |
| productcatalogservice | 280.39 | 49.13 | 13.29 | 10.13 | 0.91 | 613.40 | 13.79 |
| recommendationservice | 190.20 | 46.79 | 13.54 | 9.80 | 0.68 | 335.29 | 13.54 |
| paymentservice | 190.20 | 33.68 | 13.55 | 9.80 | 0.68 | 206.54 | 13.55 |
| shippingservice | 117.65 | 20.20 | 7.82 | 9.80 | 0.68 | 53.59 | 10.11 |
| emailservice | 132.35 | 0.29 | 0.25 | 32.35 | 5.48 | 0.98 | 0.25 |
| redis-cart | 125.59 | 0.00 | 0.00 | 10.29 | 1.24 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
