# User-side metrics: 2R-20-pilot2s%

From `locust_stats_history.csv` of 3 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 0/1 | - | run1: 488.4 vs 421.0 ❌ |
| p95 response time, high load (ms) | lower | 0/1 | - | run1: 1,642.1 vs 1,352.9 ❌ |
| p99 response time, high load (ms) | lower | 0/1 | - | run1: 2,026.7 vs 1,647.7 ❌ |
| p95 response time, ramp (ms) | lower | 0/1 | - | run1: 1,082.5 vs 1,039.7 ❌ |
| Time with p95 > 1000 ms, high load (%) | lower | 0/1 | - | run1: 89.1 vs 72.4 ❌ |
| Throughput, high load (requests/s) | higher | 0/1 | - | run1: 75.5 vs 78.2 ❌ |
| Failed requests (count) | lower | 0/1 | - | run1: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 0/1 | - | run1: 1,898.2 vs 1,526.6 ❌ |
| p95 checkout, high load (ms) | lower | 0/1 | - | run1: 849.4 vs 749.0 ❌ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Median response time, high load (ms) | 425.85 ± 6.81 (n=2) | 488.45 (n=1) |
| p95 response time, high load (ms) | 1,312.29 ± 57.50 (n=2) | 1,642.11 (n=1) |
| p99 response time, high load (ms) | 1,600.33 ± 66.94 (n=2) | 2,026.71 (n=1) |
| p95 response time, ramp (ms) | 1,055.68 ± 22.66 (n=2) | 1,082.54 (n=1) |
| Time with p95 > 1000 ms, high load (%) | 74.38 ± 2.80 (n=2) | 89.10 (n=1) |
| Throughput, high load (requests/s) | 78.32 ± 0.16 (n=2) | 75.55 (n=1) |
| Failed requests (count) | 0.00 ± 0.00 (n=2) | 0.00 (n=1) |
| p95 home page, high load (ms) | 1,486.50 ± 56.77 (n=2) | 1,898.23 (n=1) |
| p95 checkout, high load (ms) | 729.96 ± 26.95 (n=2) | 849.35 (n=1) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
