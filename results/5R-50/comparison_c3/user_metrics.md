# User-side metrics: 5R-50%

From `locust_stats_history.csv` of 15 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 3/5 | 0.841 | run1: 265.1 vs 251.4 ❌; run2: 262.0 vs 226.5 ❌; run3: 343.1 vs 722.9 ✅; run4: 298.2 vs 300.5 ✅; run5: 258.8 vs 495.1 ✅ |
| p95 response time, high load (ms) | lower | 3/5 | 0.841 | run1: 944.6 vs 1,039.8 ✅; run2: 1,202.8 vs 725.2 ❌; run3: 1,198.5 vs 2,663.6 ✅; run4: 1,183.1 vs 1,012.5 ❌; run5: 896.2 vs 1,543.2 ✅ |
| p99 response time, high load (ms) | lower | 3/5 | 0.841 | run1: 1,286.5 vs 1,406.4 ✅; run2: 1,614.3 vs 1,068.0 ❌; run3: 1,644.1 vs 3,090.6 ✅; run4: 1,548.9 vs 1,291.3 ❌; run5: 1,223.5 vs 1,865.4 ✅ |
| p95 response time, ramp (ms) | lower | 2/5 | 0.841 | run1: 776.7 vs 557.0 ❌; run2: 660.5 vs 615.8 ❌; run3: 667.6 vs 1,064.7 ✅; run4: 796.9 vs 698.3 ❌; run5: 590.2 vs 831.4 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 2/5 | 0.595 | run1: 24.8 vs 24.8 ➖; run2: 43.7 vs 4.6 ❌; run3: 12.2 vs 86.8 ✅; run4: 52.4 vs 40.7 ❌; run5: 20.1 vs 98.6 ✅ |
| Throughput, high load (requests/s) | higher | 3/5 | 0.421 | run1: 85.3 vs 84.9 ✅; run2: 84.2 vs 87.8 ❌; run3: 85.3 vs 74.5 ✅; run4: 83.3 vs 84.1 ❌; run5: 85.4 vs 75.6 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 44.0 vs 99.0 ✅; run4: 1.0 vs 0.0 ❌; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 3/5 | 0.841 | run1: 1,136.3 vs 1,279.7 ✅; run2: 1,486.1 vs 887.8 ❌; run3: 1,387.1 vs 2,757.3 ✅; run4: 1,415.5 vs 1,174.9 ❌; run5: 1,071.7 vs 1,765.4 ✅ |
| p95 checkout, high load (ms) | lower | 2/5 | 0.690 | run1: 701.4 vs 642.1 ❌; run2: 739.2 vs 548.9 ❌; run3: 750.2 vs 1,476.0 ✅; run4: 816.6 vs 689.2 ❌; run5: 709.0 vs 953.5 ✅ |

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

## Consistency (Smart HPA + priority vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.032 | run1: 223.8 vs 251.4 ✅; run2: 191.3 vs 226.5 ✅; run3: 197.8 vs 722.9 ✅; run4: 266.1 vs 300.5 ✅; run5: 197.3 vs 495.1 ✅ |
| p95 response time, high load (ms) | lower | 4/5 | 0.095 | run1: 760.7 vs 1,039.8 ✅; run2: 590.8 vs 725.2 ✅; run3: 661.8 vs 2,663.6 ✅; run4: 1,356.4 vs 1,012.5 ❌; run5: 689.9 vs 1,543.2 ✅ |
| p99 response time, high load (ms) | lower | 4/5 | 0.056 | run1: 1,060.3 vs 1,406.4 ✅; run2: 889.5 vs 1,068.0 ✅; run3: 952.3 vs 3,090.6 ✅; run4: 1,714.1 vs 1,291.3 ❌; run5: 989.1 vs 1,865.4 ✅ |
| p95 response time, ramp (ms) | lower | 4/5 | 0.032 | run1: 634.7 vs 557.0 ❌; run2: 500.6 vs 615.8 ✅; run3: 458.9 vs 1,064.7 ✅; run4: 552.6 vs 698.3 ✅; run5: 541.6 vs 831.4 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 5/5 | 0.056 | run1: 9.1 vs 24.8 ✅; run2: 1.7 vs 4.6 ✅; run3: 6.6 vs 86.8 ✅; run4: 14.9 vs 40.7 ✅; run5: 4.0 vs 98.6 ✅ |
| Throughput, high load (requests/s) | higher | 4/5 | 0.095 | run1: 87.5 vs 84.9 ✅; run2: 89.7 vs 87.8 ✅; run3: 88.7 vs 74.5 ✅; run4: 83.2 vs 84.1 ❌; run5: 88.7 vs 75.6 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 1.0 vs 0.0 ❌; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 99.0 ✅; run4: 13.0 vs 0.0 ❌; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 4/5 | 0.095 | run1: 901.8 vs 1,279.7 ✅; run2: 698.6 vs 887.8 ✅; run3: 784.9 vs 2,757.3 ✅; run4: 1,571.9 vs 1,174.9 ❌; run5: 843.3 vs 1,765.4 ✅ |
| p95 checkout, high load (ms) | lower | 4/5 | 0.095 | run1: 647.1 vs 642.1 ❌; run2: 494.5 vs 548.9 ✅; run3: 580.5 vs 1,476.0 ✅; run4: 593.2 vs 689.2 ✅; run5: 517.4 vs 953.5 ✅ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA | Smart HPA + priority |
|---|---|---|---|
| Median response time, high load (ms) | 399.27 ± 209.39 (n=5) | 285.41 ± 35.91 (n=5) | 215.25 ± 31.05 (n=5) |
| p95 response time, high load (ms) | 1,396.89 ± 766.88 (n=5) | 1,085.02 ± 151.43 (n=5) | 811.92 ± 310.38 (n=5) |
| p99 response time, high load (ms) | 1,744.34 ± 806.86 (n=5) | 1,463.45 ± 194.64 (n=5) | 1,121.07 ± 337.23 (n=5) |
| p95 response time, ramp (ms) | 753.43 ± 202.17 (n=5) | 698.37 ± 86.49 (n=5) | 537.67 ± 65.63 (n=5) |
| Time with p95 > 1000 ms, high load (%) | 51.10 ± 40.33 (n=5) | 30.65 ± 16.81 (n=5) | 7.26 ± 5.09 (n=5) |
| Throughput, high load (requests/s) | 81.40 ± 5.95 (n=5) | 84.70 ± 0.96 (n=5) | 87.54 ± 2.58 (n=5) |
| Failed requests (count) | 19.80 ± 44.27 (n=5) | 9.00 ± 19.57 (n=5) | 2.80 ± 5.72 (n=5) |
| p95 home page, high load (ms) | 1,573.01 ± 733.75 (n=5) | 1,299.36 ± 183.35 (n=5) | 960.10 ± 350.16 (n=5) |
| p95 checkout, high load (ms) | 861.95 ± 374.72 (n=5) | 743.26 ± 45.74 (n=5) | 566.56 ± 61.26 (n=5) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
