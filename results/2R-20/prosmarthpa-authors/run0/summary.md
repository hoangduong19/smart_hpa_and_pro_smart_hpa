# Run report: prosmarthpa-authors | 2R-20% | run 0

- Started 2026-10-24 10:06:39 - finished 2026-10-24 10:10:10
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 100 users, spawn rate 0.67/s, 180 s
- Knowledge Base rows: 69 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,527.83 |
| CPU Overutilization (%) - lower | 216.09 |
| Overutilization Time (min) - lower | 2.40 |
| CPU Overprovision (m) - lower | 496.96 |
| Overprovision Time (min) - higher | 0.59 |
| CPU Underprovision (m) - lower | 2,120.29 |
| Underprovision Time (min) - lower | 2.40 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 4632 | 20 | 230 | 850 | 1600 | 25.92 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 268.12 | 60.22 | 2.40 | 13.04 | 0.59 | 750.72 | 2.40 |
| currencyservice | 272.46 | 58.25 | 2.22 | 18.84 | 0.78 | 763.77 | 2.22 |
| cartservice | 373.91 | 9.42 | 1.00 | 26.09 | 0.59 | 81.16 | 0.76 |
| adservice | 373.91 | 2.42 | 0.50 | 144.93 | 2.08 | 34.78 | 0.50 |
| checkoutservice | 188.41 | 5.74 | 0.49 | 34.78 | 1.59 | 26.09 | 0.49 |
| productcatalogservice | 188.41 | 33.91 | 1.90 | 11.59 | 0.25 | 220.29 | 1.90 |
| recommendationservice | 186.96 | 25.72 | 1.62 | 13.04 | 0.59 | 146.38 | 1.62 |
| paymentservice | 186.96 | 17.87 | 1.41 | 13.04 | 0.59 | 82.61 | 1.41 |
| shippingservice | 188.41 | 0.00 | 0.00 | 81.16 | 2.18 | 0.00 | 0.00 |
| emailservice | 172.46 | 2.54 | 0.35 | 82.61 | 1.72 | 14.49 | 0.35 |
| redis-cart | 127.83 | 0.00 | 0.00 | 57.83 | 2.34 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
