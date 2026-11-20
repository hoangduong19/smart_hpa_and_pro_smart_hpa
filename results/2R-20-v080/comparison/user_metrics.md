# User-side metrics: 2R-20-v080%

From `locust_stats_history.csv` of 2 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Mean ± standard deviation

| Metric | K8s HPA |
|---|---|
| Median response time, high load (ms) | 321.47 ± 45.49 (n=2) |
| p95 response time, high load (ms) | 972.10 ± 85.27 (n=2) |
| p99 response time, high load (ms) | 1,279.35 ± 153.05 (n=2) |
| p95 response time, ramp (ms) | 662.43 ± 105.84 (n=2) |
| Time with p95 > 1000 ms, high load (%) | 18.00 ± 13.89 (n=2) |
| Throughput, high load (requests/s) | 84.15 ± 1.37 (n=2) |
| Failed requests (count) | 0.00 ± 0.00 (n=2) |
| p95 home page, high load (ms) | 1,073.89 ± 113.99 (n=2) |
| p95 checkout, high load (ms) | 567.18 ± 115.68 (n=2) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
