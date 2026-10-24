# User-side metrics: 2R-20%

From `locust_stats_history.csv` of 12 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (ProSmart HPA vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA better in | p | Per run (ProSmart HPA vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 3/5 | 0.310 | run1: 223.5 vs 331.2 ✅; run2: 214.2 vs 195.5 ❌; run3: 268.2 vs 258.8 ❌; run4: 206.6 vs 314.6 ✅; run5: 221.6 vs 229.3 ✅ |
| p95 response time, high load (ms) | lower | 2/5 | 0.841 | run1: 813.0 vs 1,139.2 ✅; run2: 756.4 vs 679.0 ❌; run3: 852.1 vs 831.5 ❌; run4: 940.3 vs 1,038.5 ✅; run5: 933.3 vs 839.5 ❌ |
| p99 response time, high load (ms) | lower | 2/5 | 0.841 | run1: 1,109.4 vs 1,445.8 ✅; run2: 1,018.6 vs 949.6 ❌; run3: 1,121.0 vs 1,090.3 ❌; run4: 1,283.9 vs 1,313.6 ✅; run5: 1,235.2 vs 1,150.3 ❌ |
| p95 response time, ramp (ms) | lower | 3/5 | 0.690 | run1: 569.6 vs 669.2 ✅; run2: 468.1 vs 474.4 ✅; run3: 627.5 vs 617.3 ❌; run4: 614.9 vs 691.0 ✅; run5: 654.0 vs 520.0 ❌ |
| Time with p95 > 1000 ms, high load (%) | lower | 3/5 | 0.690 | run1: 12.7 vs 38.5 ✅; run2: 7.7 vs 0.0 ❌; run3: 12.0 vs 11.6 ❌; run4: 14.8 vs 38.8 ✅; run5: 10.6 vs 12.1 ✅ |
| Throughput, high load (requests/s) | higher | 3/5 | 0.310 | run1: 87.6 vs 82.2 ✅; run2: 87.6 vs 88.9 ❌; run3: 85.3 vs 85.3 ✅; run4: 86.9 vs 82.2 ✅; run5: 86.3 vs 86.6 ❌ |
| Failed requests (count) | lower | 0/5 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 2/5 | 1.000 | run1: 989.9 vs 1,236.0 ✅; run2: 913.3 vs 840.2 ❌; run3: 1,015.5 vs 968.6 ❌; run4: 1,163.2 vs 1,236.5 ✅; run5: 1,130.5 vs 1,006.0 ❌ |
| p95 checkout, high load (ms) | lower | 3/5 | 0.548 | run1: 650.8 vs 707.7 ✅; run2: 528.1 vs 427.5 ❌; run3: 616.9 vs 584.5 ❌; run4: 575.2 vs 640.2 ✅; run5: 563.6 vs 642.1 ✅ |

## Consistency (ProSmart HPA, rerun 24/10 vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, rerun 24/10 better in | p | Per run (ProSmart HPA, rerun 24/10 vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 1/2 | 0.571 | run1: 230.0 vs 331.2 ✅; run2: 220.1 vs 195.5 ❌ |
| p95 response time, high load (ms) | lower | 1/2 | 0.381 | run1: 824.3 vs 1,139.2 ✅; run2: 679.5 vs 679.0 ❌ |
| p99 response time, high load (ms) | lower | 1/2 | 0.571 | run1: 1,102.1 vs 1,445.8 ✅; run2: 980.5 vs 949.6 ❌ |
| p95 response time, ramp (ms) | lower | 1/2 | 0.571 | run1: 588.6 vs 669.2 ✅; run2: 490.6 vs 474.4 ❌ |
| Time with p95 > 1000 ms, high load (%) | lower | 1/2 | 0.381 | run1: 9.6 vs 38.5 ✅; run2: 6.4 vs 0.0 ❌ |
| Throughput, high load (requests/s) | higher | 1/2 | 0.571 | run1: 86.4 vs 82.2 ✅; run2: 87.9 vs 88.9 ❌ |
| Failed requests (count) | lower | 0/2 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 2/2 | 0.571 | run1: 1,016.1 vs 1,236.0 ✅; run2: 798.8 vs 840.2 ✅ |
| p95 checkout, high load (ms) | lower | 1/2 | 0.381 | run1: 511.6 vs 707.7 ✅; run2: 555.0 vs 427.5 ❌ |

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
| Median response time, high load (ms) | 226.83 ± 24.06 (n=5) | 225.05 ± 7.05 (n=2) | 265.88 ± 56.98 (n=5) |
| p95 response time, high load (ms) | 859.02 ± 78.76 (n=5) | 751.89 ± 102.35 (n=2) | 905.54 ± 182.65 (n=5) |
| p99 response time, high load (ms) | 1,153.62 ± 105.91 (n=5) | 1,041.29 ± 85.94 (n=2) | 1,189.91 ± 193.64 (n=5) |
| p95 response time, ramp (ms) | 586.82 ± 73.06 (n=5) | 539.59 ± 69.33 (n=2) | 594.39 ± 94.06 (n=5) |
| Time with p95 > 1000 ms, high load (%) | 11.56 ± 2.62 (n=5) | 8.00 ± 2.25 (n=2) | 20.21 ± 17.52 (n=5) |
| Throughput, high load (requests/s) | 86.74 ± 0.96 (n=5) | 87.12 ± 1.06 (n=2) | 85.06 ± 2.91 (n=5) |
| Failed requests (count) | 0.00 ± 0.00 (n=5) | 0.00 ± 0.00 (n=2) | 0.00 ± 0.00 (n=5) |
| p95 home page, high load (ms) | 1,042.47 ± 103.09 (n=5) | 907.46 ± 153.71 (n=2) | 1,057.47 ± 174.43 (n=5) |
| p95 checkout, high load (ms) | 586.92 ± 47.77 (n=5) | 533.31 ± 30.73 (n=2) | 600.41 ± 106.05 (n=5) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
