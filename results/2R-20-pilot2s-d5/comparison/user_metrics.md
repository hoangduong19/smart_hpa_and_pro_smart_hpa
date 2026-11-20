# User-side metrics: 2R-20-pilot2s-d5%

From `locust_stats_history.csv` of 2 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 1/1 | - | run1: 201.8 vs 267.0 ✅ |
| p95 response time, high load (ms) | lower | 1/1 | - | run1: 659.9 vs 828.3 ✅ |
| p99 response time, high load (ms) | lower | 1/1 | - | run1: 956.4 vs 1,170.1 ✅ |
| p95 response time, ramp (ms) | lower | 1/1 | - | run1: 465.0 vs 859.8 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 1/1 | - | run1: 9.4 vs 11.3 ✅ |
| Throughput, high load (requests/s) | higher | 1/1 | - | run1: 89.4 vs 85.9 ✅ |
| Failed requests (count) | lower | 0/1 | - | run1: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 1/1 | - | run1: 808.6 vs 1,054.0 ✅ |
| p95 checkout, high load (ms) | lower | 1/1 | - | run1: 442.6 vs 481.0 ✅ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Median response time, high load (ms) | 266.96 (n=1) | 201.85 (n=1) |
| p95 response time, high load (ms) | 828.29 (n=1) | 659.95 (n=1) |
| p99 response time, high load (ms) | 1,170.12 (n=1) | 956.44 (n=1) |
| p95 response time, ramp (ms) | 859.80 (n=1) | 465.02 (n=1) |
| Time with p95 > 1000 ms, high load (%) | 11.26 (n=1) | 9.40 (n=1) |
| Throughput, high load (requests/s) | 85.92 (n=1) | 89.39 (n=1) |
| Failed requests (count) | 0.00 (n=1) | 0.00 (n=1) |
| p95 home page, high load (ms) | 1,054.00 (n=1) | 808.59 (n=1) |
| p95 checkout, high load (ms) | 481.04 (n=1) | 442.57 (n=1) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
