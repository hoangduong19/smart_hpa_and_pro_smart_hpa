# Run report: smarthpa-warmup | 2R-20% | run 4

- Started 2026-11-19 19:25:27 - finished 2026-11-19 19:40:58
- Scenario 2R-20%: maxR = 2, CPU threshold = 20%
- Load: 200 users, spawn rate 2.0/s, 900 s
- Knowledge Base rows: 502 loop iterations
- Max unschedulable pods during run: 0

## Application level (Table 1 metrics)

| Metric | Value |
|---|---|
| Supply CPU (m) - higher is better | 2,471.00 |
| CPU Overutilization (%) - lower | 414.43 |
| Overutilization Time (min) - lower | 14.64 |
| CPU Overprovision (m) - lower | 56.57 |
| Overprovision Time (min) - higher | 0.33 |
| CPU Underprovision (m) - lower | 3,723.90 |
| Underprovision Time (min) - lower | 14.64 |

## Load test totals (Locust)

| Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) | Requests/s |
|---|---|---|---|---|---|
| 69074 | 0 | 340 | 1100 | 1400 | 76.79 |

## Per microservice

| Microservice | Supply (m) | Overutil (%) | Overutil time (min) | Overprov (m) | Overprov time (min) | Underprov (m) | Underprov time (min) |
|---|---|---|---|---|---|---|---|
| frontend | 418.13 | 73.71 | 14.64 | 3.19 | 0.33 | 1,089.44 | 14.64 |
| currencyservice | 195.22 | 97.59 | 14.39 | 3.98 | 0.58 | 844.02 | 14.39 |
| cartservice | 392.03 | 29.41 | 13.89 | 6.37 | 0.33 | 280.08 | 13.64 |
| adservice | 256.57 | 4.00 | 2.99 | 6.37 | 0.33 | 32.27 | 2.23 |
| checkoutservice | 195.42 | 34.39 | 14.09 | 4.18 | 0.88 | 192.83 | 14.03 |
| productcatalogservice | 196.22 | 66.36 | 14.16 | 3.19 | 0.33 | 512.95 | 14.09 |
| recommendationservice | 195.22 | 66.62 | 14.39 | 3.98 | 0.58 | 513.15 | 14.09 |
| paymentservice | 195.22 | 39.08 | 14.39 | 3.98 | 0.58 | 245.42 | 14.09 |
| shippingservice | 194.22 | 0.23 | 0.12 | 4.78 | 1.32 | 0.00 | 0.00 |
| emailservice | 100.00 | 2.94 | 2.09 | 9.56 | 2.01 | 13.75 | 2.09 |
| redis-cart | 132.75 | 0.09 | 0.05 | 6.97 | 2.06 | 0.00 | 0.00 |

Figures: `fig_demand_capacity.png`, `fig_cpu_utilization.png`, `fig_load.png`.
