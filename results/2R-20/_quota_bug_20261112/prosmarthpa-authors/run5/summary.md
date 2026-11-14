# Run report: prosmarthpa-authors | 2R-20% | run 5

- Started 2026-10-24 12:05:00 - finished 2026-10-24 12:20:30
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 0.67/s, 900 s
- Knowledge Base rows: 449 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,695.28 |
| CPU Overutilization (%) - lower | 488.02 |
| Overutilization Time (min) - lower | 14.49 |
| CPU Overprovision (m) - lower | 182.36 |
| Overprovision Time (min) - higher | 0.51 |
| CPU Underprovision (m) - lower | 5,196.88 |
| Underprovision Time (min) - lower | 14.49 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 65576 | 0 | 210 | 800 | 1200 | 72.94 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 291.98 | 122.43 | 14.49 | 2.67 | 0.51 | 1,636.53 | 14.49 |
| currencyservice | 294.65 | 119.18 | 14.49 | 3.34 | 0.51 | 1,622.49 | 14.49 |
| cartservice | 394.65 | 32.03 | 13.24 | 12.03 | 1.01 | 350.11 | 13.24 |
| adservice | 394.65 | 1.33 | 0.97 | 85.08 | 6.47 | 10.69 | 0.97 |
| checkoutservice | 197.55 | 26.86 | 12.25 | 5.57 | 1.26 | 149.67 | 12.25 |
| productcatalogservice | 197.55 | 85.83 | 13.99 | 2.45 | 0.23 | 705.35 | 13.99 |
| recommendationservice | 197.33 | 57.49 | 13.72 | 3.12 | 0.77 | 433.41 | 13.72 |
| paymentservice | 197.33 | 39.24 | 13.72 | 2.67 | 0.51 | 253.45 | 13.72 |
| shippingservice | 197.33 | 3.63 | 2.50 | 10.47 | 2.00 | 17.15 | 2.50 |
| emailservice | 194.43 | 0.00 | 0.00 | 46.55 | 5.73 | 18.04 | 3.06 |
| redis-cart | 137.82 | 0.00 | 0.00 | 8.42 | 1.91 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
