# User-side metrics: 2R-20-c4fresh%

From `locust_stats_history.csv` of 7 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Mean ± standard deviation

| Metric | K8s HPA |
|---|---|
| Median response time, high load (ms) | 319.12 ± 32.74 (n=7) |
| p95 response time, high load (ms) | 912.55 ± 94.37 (n=7) |
| p99 response time, high load (ms) | 1,133.81 ± 107.12 (n=7) |
| p95 response time, ramp (ms) | 850.73 ± 63.32 (n=7) |
| Time with p95 > 1000 ms, high load (%) | 18.16 ± 10.82 (n=7) |
| Throughput, high load (requests/s) | 83.24 ± 1.64 (n=7) |
| Failed requests (count) | 0.00 ± 0.00 (n=7) |
| p95 home page, high load (ms) | 1,029.98 ± 106.45 (n=7) |
| p95 checkout, high load (ms) | 579.64 ± 65.54 (n=7) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
