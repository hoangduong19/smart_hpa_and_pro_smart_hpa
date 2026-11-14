# User-side metrics: 2R-20%

From `locust_stats_history.csv` of 12 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (ProSmart HPA vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA better in | p | Per run (ProSmart HPA vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.016 | run1: 223.5 vs 316.1 ✅; run2: 214.2 vs 319.5 ✅; run3: 268.2 vs 314.3 ✅; run4: 206.6 vs 328.1 ✅; run5: 221.6 vs 256.1 ✅ |
| p95 response time, high load (ms) | lower | 4/5 | 0.056 | run1: 813.0 vs 1,004.3 ✅; run2: 756.4 vs 1,034.0 ✅; run3: 852.1 vs 980.6 ✅; run4: 940.3 vs 1,041.3 ✅; run5: 933.3 vs 818.2 ❌ |
| p99 response time, high load (ms) | lower | 4/5 | 0.310 | run1: 1,109.4 vs 1,261.6 ✅; run2: 1,018.6 vs 1,283.3 ✅; run3: 1,121.0 vs 1,239.9 ✅; run4: 1,283.9 vs 1,309.0 ✅; run5: 1,235.2 vs 1,095.4 ❌ |
| p95 response time, ramp (ms) | lower | 4/5 | 0.222 | run1: 569.6 vs 655.1 ✅; run2: 468.1 vs 610.4 ✅; run3: 627.5 vs 679.0 ✅; run4: 614.9 vs 628.9 ✅; run5: 654.0 vs 622.5 ❌ |
| Time with p95 > 1000 ms, high load (%) | lower | 5/5 | 0.008 | run1: 12.7 vs 37.1 ✅; run2: 7.7 vs 38.6 ✅; run3: 12.0 vs 28.8 ✅; run4: 14.8 vs 35.8 ✅; run5: 10.6 vs 19.9 ✅ |
| Throughput, high load (requests/s) | higher | 5/5 | 0.016 | run1: 87.6 vs 82.2 ✅; run2: 87.6 vs 82.8 ✅; run3: 85.3 vs 82.7 ✅; run4: 86.9 vs 82.2 ✅; run5: 86.3 vs 86.1 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 89.0 ✅ |
| p95 home page, high load (ms) | lower | 4/5 | 0.095 | run1: 989.9 vs 1,185.3 ✅; run2: 913.3 vs 1,226.7 ✅; run3: 1,015.5 vs 1,154.5 ✅; run4: 1,163.2 vs 1,237.0 ✅; run5: 1,130.5 vs 992.4 ❌ |
| p95 checkout, high load (ms) | lower | 3/5 | 0.690 | run1: 650.8 vs 611.7 ❌; run2: 528.1 vs 585.6 ✅; run3: 616.9 vs 635.0 ✅; run4: 575.2 vs 672.5 ✅; run5: 563.6 vs 459.1 ❌ |

## Consistency (ProSmart HPA, rerun 24/10 vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, rerun 24/10 better in | p | Per run (ProSmart HPA, rerun 24/10 vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 2/2 | 0.095 | run1: 230.0 vs 316.1 ✅; run2: 220.1 vs 319.5 ✅ |
| p95 response time, high load (ms) | lower | 2/2 | 0.190 | run1: 824.3 vs 1,004.3 ✅; run2: 679.5 vs 1,034.0 ✅ |
| p99 response time, high load (ms) | lower | 2/2 | 0.190 | run1: 1,102.1 vs 1,261.6 ✅; run2: 980.5 vs 1,283.3 ✅ |
| p95 response time, ramp (ms) | lower | 2/2 | 0.095 | run1: 588.6 vs 655.1 ✅; run2: 490.6 vs 610.4 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 2/2 | 0.095 | run1: 9.6 vs 37.1 ✅; run2: 6.4 vs 38.6 ✅ |
| Throughput, high load (requests/s) | higher | 2/2 | 0.095 | run1: 86.4 vs 82.2 ✅; run2: 87.9 vs 82.8 ✅ |
| Failed requests (count) | lower | 0/2 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 2/2 | 0.190 | run1: 1,016.1 vs 1,185.3 ✅; run2: 798.8 vs 1,226.7 ✅ |
| p95 checkout, high load (ms) | lower | 2/2 | 0.381 | run1: 511.6 vs 611.7 ✅; run2: 555.0 vs 585.6 ✅ |

## Consistency (ProSmart HPA, rerun 24/10 vs ProSmart HPA, same run number)

Paired runs: [1, 2]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, rerun 24/10 better in | p | Per run (ProSmart HPA, rerun 24/10 vs ProSmart HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 0/2 | 0.857 | run1: 230.0 vs 223.5 ❌; run2: 220.1 vs 214.2 ❌ |
| p95 response time, high load (ms) | lower | 1/2 | 0.381 | run1: 824.3 vs 813.0 ❌; run2: 679.5 vs 756.4 ✅ |
| p99 response time, high load (ms) | lower | 2/2 | 0.190 | run1: 1,102.1 vs 1,109.4 ✅; run2: 980.5 vs 1,018.6 ✅ |
| p95 response time, ramp (ms) | lower | 0/2 | 0.571 | run1: 588.6 vs 569.6 ❌; run2: 490.6 vs 468.1 ❌ |
| Time with p95 > 1000 ms, high load (%) | lower | 2/2 | 0.190 | run1: 9.6 vs 12.7 ✅; run2: 6.4 vs 7.7 ✅ |
| Throughput, high load (requests/s) | higher | 1/2 | 0.571 | run1: 86.4 vs 87.6 ❌; run2: 87.9 vs 87.6 ✅ |
| Failed requests (count) | lower | 0/2 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 1/2 | 0.571 | run1: 1,016.1 vs 989.9 ❌; run2: 798.8 vs 913.3 ✅ |
| p95 checkout, high load (ms) | lower | 1/2 | 0.190 | run1: 511.6 vs 650.8 ✅; run2: 555.0 vs 528.1 ❌ |

## Mean ± standard deviation

| Metric | ProSmart HPA | ProSmart HPA, rerun 24/10 | ProSmart HPA, authors' models |
|---|---|---|---|
| Median response time, high load (ms) | 226.83 ± 24.06 (n=5) | 225.05 ± 7.05 (n=2) | 306.82 ± 28.85 (n=5) |
| p95 response time, high load (ms) | 859.02 ± 78.76 (n=5) | 751.89 ± 102.35 (n=2) | 975.69 ± 91.31 (n=5) |
| p99 response time, high load (ms) | 1,153.62 ± 105.91 (n=5) | 1,041.29 ± 85.94 (n=2) | 1,237.85 ± 83.65 (n=5) |
| p95 response time, ramp (ms) | 586.82 ± 73.06 (n=5) | 539.59 ± 69.33 (n=2) | 639.19 ± 27.62 (n=5) |
| Time with p95 > 1000 ms, high load (%) | 11.56 ± 2.62 (n=5) | 8.00 ± 2.25 (n=2) | 32.05 ± 7.76 (n=5) |
| Throughput, high load (requests/s) | 86.74 ± 0.96 (n=5) | 87.12 ± 1.06 (n=2) | 83.19 ± 1.64 (n=5) |
| Failed requests (count) | 0.00 ± 0.00 (n=5) | 0.00 ± 0.00 (n=2) | 17.80 ± 39.80 (n=5) |
| p95 home page, high load (ms) | 1,042.47 ± 103.09 (n=5) | 907.46 ± 153.71 (n=2) | 1,159.19 ± 98.90 (n=5) |
| p95 checkout, high load (ms) | 586.92 ± 47.77 (n=5) | 533.31 ± 30.73 (n=2) | 592.77 ± 81.25 (n=5) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
