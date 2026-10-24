# User-side metrics: 2R-20%

From `locust_stats_history.csv` of 15 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (ProSmart HPA vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA better in | p | Per run (ProSmart HPA vs Smart HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.008 | run1: 223.5 vs 334.7 ✅; run2: 214.2 vs 336.0 ✅; run3: 268.2 vs 339.5 ✅; run4: 206.6 vs 441.8 ✅; run5: 221.6 vs 365.5 ✅ |
| p95 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 813.0 vs 1,028.1 ✅; run2: 756.4 vs 1,141.8 ✅; run3: 852.1 vs 1,056.5 ✅; run4: 940.3 vs 1,623.0 ✅; run5: 933.3 vs 1,339.3 ✅ |
| p99 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 1,109.4 vs 1,342.3 ✅; run2: 1,018.6 vs 1,493.4 ✅; run3: 1,121.0 vs 1,349.4 ✅; run4: 1,283.9 vs 2,036.2 ✅; run5: 1,235.2 vs 1,665.1 ✅ |
| p95 response time, ramp (ms) | lower | 5/5 | 0.008 | run1: 569.6 vs 657.8 ✅; run2: 468.1 vs 694.8 ✅; run3: 627.5 vs 806.7 ✅; run4: 614.9 vs 774.9 ✅; run5: 654.0 vs 853.5 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 5/5 | 0.008 | run1: 12.7 vs 23.9 ✅; run2: 7.7 vs 31.7 ✅; run3: 12.0 vs 42.2 ✅; run4: 14.8 vs 45.9 ✅; run5: 10.6 vs 89.7 ✅ |
| Throughput, high load (requests/s) | higher | 5/5 | 0.008 | run1: 87.6 vs 82.2 ✅; run2: 87.6 vs 82.6 ✅; run3: 85.3 vs 82.9 ✅; run4: 86.9 vs 80.5 ✅; run5: 86.3 vs 80.6 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 44.0 ✅; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 5/5 | 0.008 | run1: 989.9 vs 1,208.4 ✅; run2: 913.3 vs 1,359.3 ✅; run3: 1,015.5 vs 1,221.9 ✅; run4: 1,163.2 vs 1,841.2 ✅; run5: 1,130.5 vs 1,568.3 ✅ |
| p95 checkout, high load (ms) | lower | 5/5 | 0.008 | run1: 650.8 vs 670.0 ✅; run2: 528.1 vs 731.2 ✅; run3: 616.9 vs 789.8 ✅; run4: 575.2 vs 967.0 ✅; run5: 563.6 vs 716.0 ✅ |

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

## Consistency (ProSmart HPA, authors' models vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs Smart HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.008 | run1: 331.2 vs 334.7 ✅; run2: 195.5 vs 336.0 ✅; run3: 258.8 vs 339.5 ✅; run4: 314.6 vs 441.8 ✅; run5: 229.3 vs 365.5 ✅ |
| p95 response time, high load (ms) | lower | 4/5 | 0.056 | run1: 1,139.2 vs 1,028.1 ❌; run2: 679.0 vs 1,141.8 ✅; run3: 831.5 vs 1,056.5 ✅; run4: 1,038.5 vs 1,623.0 ✅; run5: 839.5 vs 1,339.3 ✅ |
| p99 response time, high load (ms) | lower | 4/5 | 0.032 | run1: 1,445.8 vs 1,342.3 ❌; run2: 949.6 vs 1,493.4 ✅; run3: 1,090.3 vs 1,349.4 ✅; run4: 1,313.6 vs 2,036.2 ✅; run5: 1,150.3 vs 1,665.1 ✅ |
| p95 response time, ramp (ms) | lower | 4/5 | 0.032 | run1: 669.2 vs 657.8 ❌; run2: 474.4 vs 694.8 ✅; run3: 617.3 vs 806.7 ✅; run4: 691.0 vs 774.9 ✅; run5: 520.0 vs 853.5 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 4/5 | 0.095 | run1: 38.5 vs 23.9 ❌; run2: 0.0 vs 31.7 ✅; run3: 11.6 vs 42.2 ✅; run4: 38.8 vs 45.9 ✅; run5: 12.1 vs 89.7 ✅ |
| Throughput, high load (requests/s) | higher | 5/5 | 0.095 | run1: 82.2 vs 82.2 ✅; run2: 88.9 vs 82.6 ✅; run3: 85.3 vs 82.9 ✅; run4: 82.2 vs 80.5 ✅; run5: 86.6 vs 80.6 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 44.0 ✅; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 4/5 | 0.095 | run1: 1,236.0 vs 1,208.4 ❌; run2: 840.2 vs 1,359.3 ✅; run3: 968.6 vs 1,221.9 ✅; run4: 1,236.5 vs 1,841.2 ✅; run5: 1,006.0 vs 1,568.3 ✅ |
| p95 checkout, high load (ms) | lower | 4/5 | 0.016 | run1: 707.7 vs 670.0 ❌; run2: 427.5 vs 731.2 ✅; run3: 584.5 vs 789.8 ✅; run4: 640.2 vs 967.0 ✅; run5: 642.1 vs 716.0 ✅ |

## Mean ± standard deviation

| Metric | Smart HPA | ProSmart HPA | ProSmart HPA, authors' models |
|---|---|---|---|
| Median response time, high load (ms) | 363.50 ± 45.57 (n=5) | 226.83 ± 24.06 (n=5) | 265.88 ± 56.98 (n=5) |
| p95 response time, high load (ms) | 1,237.75 ± 247.35 (n=5) | 859.02 ± 78.76 (n=5) | 905.54 ± 182.65 (n=5) |
| p99 response time, high load (ms) | 1,577.28 ± 288.31 (n=5) | 1,153.62 ± 105.91 (n=5) | 1,189.91 ± 193.64 (n=5) |
| p95 response time, ramp (ms) | 757.55 ± 80.35 (n=5) | 586.82 ± 73.06 (n=5) | 594.39 ± 94.06 (n=5) |
| Time with p95 > 1000 ms, high load (%) | 46.71 ± 25.57 (n=5) | 11.56 ± 2.62 (n=5) | 20.21 ± 17.52 (n=5) |
| Throughput, high load (requests/s) | 81.75 ± 1.13 (n=5) | 86.74 ± 0.96 (n=5) | 85.06 ± 2.91 (n=5) |
| Failed requests (count) | 8.80 ± 19.68 (n=5) | 0.00 ± 0.00 (n=5) | 0.00 ± 0.00 (n=5) |
| p95 home page, high load (ms) | 1,439.83 ± 267.00 (n=5) | 1,042.47 ± 103.09 (n=5) | 1,057.47 ± 174.43 (n=5) |
| p95 checkout, high load (ms) | 774.81 ± 115.63 (n=5) | 586.92 ± 47.77 (n=5) | 600.41 ± 106.05 (n=5) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
