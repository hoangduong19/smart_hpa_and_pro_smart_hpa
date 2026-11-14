# Run report: prosmarthpa-cv-w15 | 2R-20% | run 2

- Started 2026-11-12 17:43:59 - finished 2026-11-12 17:59:33
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 183 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,805.46 |
| CPU Overutilization (%) - lower | 308.08 |
| Overutilization Time (min) - lower | 14.61 |
| CPU Overprovision (m) - lower | 203.39 |
| Overprovision Time (min) - higher | 0.52 |
| CPU Underprovision (m) - lower | 4,479.78 |
| Underprovision Time (min) - lower | 14.35 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69205 | 10 | 110 | 510 | 900 | 76.96 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 554.10 | 48.55 | 14.61 | 7.10 | 0.26 | 1,056.83 | 14.35 |
| currencyservice | 748.09 | 51.78 | 14.35 | 14.21 | 0.52 | 1,901.09 | 14.35 |
| cartservice | 287.43 | 33.49 | 13.58 | 29.51 | 0.56 | 398.91 | 13.58 |
| adservice | 200.00 | 0.25 | 0.25 | 28.42 | 0.52 | 2.19 | 0.25 |
| checkoutservice | 118.03 | 33.09 | 13.08 | 16.39 | 0.86 | 165.57 | 13.08 |
| productcatalogservice | 184.70 | 53.91 | 13.35 | 15.30 | 0.79 | 422.95 | 13.35 |
| recommendationservice | 184.70 | 38.36 | 13.33 | 15.30 | 0.79 | 268.31 | 13.33 |
| paymentservice | 181.42 | 32.46 | 13.32 | 18.58 | 1.04 | 209.29 | 13.32 |
| shippingservice | 115.85 | 15.74 | 7.62 | 15.30 | 0.79 | 53.01 | 10.96 |
| emailservice | 120.22 | 0.44 | 0.50 | 29.51 | 5.89 | 1.64 | 0.50 |
| redis-cart | 110.93 | 0.00 | 0.00 | 13.77 | 1.13 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
