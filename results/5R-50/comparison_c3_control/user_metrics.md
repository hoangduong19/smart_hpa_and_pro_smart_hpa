# User-side metrics: 5R-50%

From `locust_stats_history.csv` of 13 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (Smart HPA + priority vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs Smart HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.056 | run1: 223.8 vs 265.1 ✅; run2: 191.3 vs 262.0 ✅; run3: 197.8 vs 343.1 ✅; run4: 266.1 vs 298.2 ✅; run5: 197.3 vs 258.8 ✅ |
| p95 response time, high load (ms) | lower | 4/5 | 0.151 | run1: 760.7 vs 944.6 ✅; run2: 590.8 vs 1,202.8 ✅; run3: 661.8 vs 1,198.5 ✅; run4: 1,356.4 vs 1,183.1 ❌; run5: 689.9 vs 896.2 ✅ |
| p99 response time, high load (ms) | lower | 4/5 | 0.151 | run1: 1,060.3 vs 1,286.5 ✅; run2: 889.5 vs 1,614.3 ✅; run3: 952.3 vs 1,644.1 ✅; run4: 1,714.1 vs 1,548.9 ❌; run5: 989.1 vs 1,223.5 ✅ |
| p95 response time, ramp (ms) | lower | 5/5 | 0.016 | run1: 634.7 vs 776.7 ✅; run2: 500.6 vs 660.5 ✅; run3: 458.9 vs 667.6 ✅; run4: 552.6 vs 796.9 ✅; run5: 541.6 vs 590.2 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 5/5 | 0.016 | run1: 9.1 vs 24.8 ✅; run2: 1.7 vs 43.7 ✅; run3: 6.6 vs 12.2 ✅; run4: 14.9 vs 52.4 ✅; run5: 4.0 vs 20.1 ✅ |
| Throughput, high load (requests/s) | higher | 4/5 | 0.151 | run1: 87.5 vs 85.3 ✅; run2: 89.7 vs 84.2 ✅; run3: 88.7 vs 85.3 ✅; run4: 83.2 vs 83.3 ❌; run5: 88.7 vs 85.4 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 1.0 vs 0.0 ❌; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 44.0 ✅; run4: 13.0 vs 1.0 ❌; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 4/5 | 0.151 | run1: 901.8 vs 1,136.3 ✅; run2: 698.6 vs 1,486.1 ✅; run3: 784.9 vs 1,387.1 ✅; run4: 1,571.9 vs 1,415.5 ❌; run5: 843.3 vs 1,071.7 ✅ |
| p95 checkout, high load (ms) | lower | 5/5 | 0.008 | run1: 647.1 vs 701.4 ✅; run2: 494.5 vs 739.2 ✅; run3: 580.5 vs 750.2 ✅; run4: 593.2 vs 816.6 ✅; run5: 517.4 vs 709.0 ✅ |

## Consistency (Smart HPA + quota fix vs Smart HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + quota fix better in | p | Per run (Smart HPA + quota fix vs Smart HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 3/3 | 0.036 | run1: 195.4 vs 265.1 ✅; run2: 178.9 vs 262.0 ✅; run3: 197.5 vs 343.1 ✅ |
| p95 response time, high load (ms) | lower | 3/3 | 0.036 | run1: 713.0 vs 944.6 ✅; run2: 569.8 vs 1,202.8 ✅; run3: 674.8 vs 1,198.5 ✅ |
| p99 response time, high load (ms) | lower | 3/3 | 0.036 | run1: 1,042.8 vs 1,286.5 ✅; run2: 860.9 vs 1,614.3 ✅; run3: 967.8 vs 1,644.1 ✅ |
| p95 response time, ramp (ms) | lower | 3/3 | 0.071 | run1: 630.1 vs 776.7 ✅; run2: 519.8 vs 660.5 ✅; run3: 495.6 vs 667.6 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 3/3 | 0.036 | run1: 6.6 vs 24.8 ✅; run2: 0.8 vs 43.7 ✅; run3: 4.2 vs 12.2 ✅ |
| Throughput, high load (requests/s) | higher | 3/3 | 0.036 | run1: 88.6 vs 85.3 ✅; run2: 89.9 vs 84.2 ✅; run3: 88.6 vs 85.3 ✅ |
| Failed requests (count) | lower | 1/3 | 0.464 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 44.0 ✅ |
| p95 home page, high load (ms) | lower | 3/3 | 0.036 | run1: 882.3 vs 1,136.3 ✅; run2: 701.8 vs 1,486.1 ✅; run3: 811.1 vs 1,387.1 ✅ |
| p95 checkout, high load (ms) | lower | 3/3 | 0.036 | run1: 524.7 vs 701.4 ✅; run2: 446.0 vs 739.2 ✅; run3: 501.5 vs 750.2 ✅ |

## Consistency (Smart HPA + priority vs Smart HPA + quota fix, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs Smart HPA + quota fix) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 0/3 | 0.250 | run1: 223.8 vs 195.4 ❌; run2: 191.3 vs 178.9 ❌; run3: 197.8 vs 197.5 ❌ |
| p95 response time, high load (ms) | lower | 1/3 | 0.571 | run1: 760.7 vs 713.0 ❌; run2: 590.8 vs 569.8 ❌; run3: 661.8 vs 674.8 ✅ |
| p99 response time, high load (ms) | lower | 1/3 | 0.571 | run1: 1,060.3 vs 1,042.8 ❌; run2: 889.5 vs 860.9 ❌; run3: 952.3 vs 967.8 ✅ |
| p95 response time, ramp (ms) | lower | 2/3 | 1.000 | run1: 634.7 vs 630.1 ❌; run2: 500.6 vs 519.8 ✅; run3: 458.9 vs 495.6 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 0/3 | 0.571 | run1: 9.1 vs 6.6 ❌; run2: 1.7 vs 0.8 ❌; run3: 6.6 vs 4.2 ❌ |
| Throughput, high load (requests/s) | higher | 1/3 | 0.786 | run1: 87.5 vs 88.6 ❌; run2: 89.7 vs 89.9 ❌; run3: 88.7 vs 88.6 ✅ |
| Failed requests (count) | lower | 0/3 | 0.464 | run1: 1.0 vs 0.0 ❌; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 2/3 | 0.786 | run1: 901.8 vs 882.3 ❌; run2: 698.6 vs 701.8 ✅; run3: 784.9 vs 811.1 ✅ |
| p95 checkout, high load (ms) | lower | 0/3 | 0.250 | run1: 647.1 vs 524.7 ❌; run2: 494.5 vs 446.0 ❌; run3: 580.5 vs 501.5 ❌ |

## Mean ± standard deviation

| Metric | Smart HPA | Smart HPA + quota fix | Smart HPA + priority |
|---|---|---|---|
| Median response time, high load (ms) | 285.41 ± 35.91 (n=5) | 190.60 ± 10.19 (n=3) | 215.25 ± 31.05 (n=5) |
| p95 response time, high load (ms) | 1,085.02 ± 151.43 (n=5) | 652.55 ± 74.13 (n=3) | 811.92 ± 310.38 (n=5) |
| p99 response time, high load (ms) | 1,463.45 ± 194.64 (n=5) | 957.17 ± 91.40 (n=3) | 1,121.07 ± 337.23 (n=5) |
| p95 response time, ramp (ms) | 698.37 ± 86.49 (n=5) | 548.50 ± 71.69 (n=3) | 537.67 ± 65.63 (n=5) |
| Time with p95 > 1000 ms, high load (%) | 30.65 ± 16.81 (n=5) | 3.88 ± 2.89 (n=3) | 7.26 ± 5.09 (n=5) |
| Throughput, high load (requests/s) | 84.70 ± 0.96 (n=5) | 89.03 ± 0.74 (n=3) | 87.54 ± 2.58 (n=5) |
| Failed requests (count) | 9.00 ± 19.57 (n=5) | 0.00 ± 0.00 (n=3) | 2.80 ± 5.72 (n=5) |
| p95 home page, high load (ms) | 1,299.36 ± 183.35 (n=5) | 798.42 ± 90.94 (n=3) | 960.10 ± 350.16 (n=5) |
| p95 checkout, high load (ms) | 743.26 ± 45.74 (n=5) | 490.74 ± 40.48 (n=3) | 566.56 ± 61.26 (n=5) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
