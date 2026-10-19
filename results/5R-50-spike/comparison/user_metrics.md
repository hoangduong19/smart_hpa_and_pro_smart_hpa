# User-side metrics: 5R-50% spike

From `locust_stats_history.csv` of 6 runs. Spikes = minute 3-7 + 10-13, first minute of a spike = 3-4 + 10-11, base load after a spike = 7-10 + 13-15. Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Median response time, spikes (ms) | lower | 2/3 | 1.000 | run1: 345.9 vs 430.5 ✅; run2: 608.4 vs 461.4 ❌; run3: 490.1 vs 563.7 ✅ |
| p95 response time, spikes (ms) | lower | 2/3 | 1.000 | run1: 1,222.2 vs 1,052.9 ❌; run2: 1,392.3 vs 1,752.4 ✅; run3: 1,789.4 vs 1,800.3 ✅ |
| p99 response time, spikes (ms) | lower | 1/3 | 1.000 | run1: 1,584.1 vs 1,357.0 ❌; run2: 1,732.1 vs 2,059.3 ✅; run3: 2,260.7 vs 2,153.2 ❌ |
| p95 response time, first minute of a spike (ms) | lower | 2/3 | 1.000 | run1: 1,286.3 vs 1,006.1 ❌; run2: 1,208.1 vs 1,451.5 ✅; run3: 1,876.2 vs 1,983.1 ✅ |
| p95 response time, base load after a spike (ms) | lower | 1/3 | 1.000 | run1: 521.7 vs 383.0 ❌; run2: 522.2 vs 612.2 ✅; run3: 747.2 vs 648.1 ❌ |
| Time with p95 > 1000 ms, spikes (%) | lower | 1/3 | 1.000 | run1: 55.9 vs 44.8 ❌; run2: 70.4 vs 92.3 ✅; run3: 92.0 vs 85.3 ❌ |
| Throughput, spikes (requests/s) | higher | 2/3 | 1.000 | run1: 102.5 vs 100.5 ✅; run2: 93.9 vs 94.5 ❌; run3: 94.0 vs 91.4 ✅ |
| Failed requests (count) | lower | 0/3 | 0.400 | run1: 1.0 vs 0.0 ❌; run2: 0.0 vs 0.0 ➖; run3: 38.0 vs 0.0 ❌ |
| p95 checkout, spikes (ms) | lower | 2/3 | 1.000 | run1: 757.3 vs 996.6 ✅; run2: 1,134.6 vs 867.9 ❌; run3: 930.5 vs 989.4 ✅ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Median response time, spikes (ms) | 485.22 ± 69.74 (n=3) | 481.47 ± 131.43 (n=3) |
| p95 response time, spikes (ms) | 1,535.19 ± 418.39 (n=3) | 1,467.96 ± 291.05 (n=3) |
| p99 response time, spikes (ms) | 1,856.51 ± 435.11 (n=3) | 1,858.99 ± 355.72 (n=3) |
| p95 response time, first minute of a spike (ms) | 1,480.25 ± 489.15 (n=3) | 1,456.84 ± 365.27 (n=3) |
| p95 response time, base load after a spike (ms) | 547.79 ± 143.84 (n=3) | 596.99 ± 130.05 (n=3) |
| Time with p95 > 1000 ms, spikes (%) | 74.12 ± 25.62 (n=3) | 72.76 ± 18.18 (n=3) |
| Throughput, spikes (requests/s) | 95.49 ± 4.63 (n=3) | 96.80 ± 4.96 (n=3) |
| Failed requests (count) | 0.00 ± 0.00 (n=3) | 13.00 ± 21.66 (n=3) |
| p95 checkout, spikes (ms) | 951.30 ± 72.34 (n=3) | 940.79 ± 188.84 (n=3) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
