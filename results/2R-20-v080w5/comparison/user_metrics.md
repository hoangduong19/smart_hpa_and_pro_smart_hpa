# User-side metrics: 2R-20-v080w5%

From `locust_stats_history.csv` of 16 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5, 6, 7, 8]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 7/8 | 0.050 | run1: 188.2 vs 288.9 ✅; run2: 238.3 vs 289.1 ✅; run3: 203.4 vs 197.7 ❌; run4: 288.8 vs 292.1 ✅; run5: 191.0 vs 217.2 ✅; run6: 237.7 vs 278.4 ✅; run7: 235.6 vs 267.1 ✅; run8: 238.1 vs 301.4 ✅ |
| p95 response time, high load (ms) | lower | 5/8 | 0.878 | run1: 663.8 vs 687.1 ✅; run2: 723.5 vs 871.6 ✅; run3: 605.8 vs 534.9 ❌; run4: 829.4 vs 864.2 ✅; run5: 653.5 vs 605.2 ❌; run6: 1,491.0 vs 816.0 ❌; run7: 793.8 vs 816.9 ✅; run8: 731.4 vs 787.6 ✅ |
| p99 response time, high load (ms) | lower | 4/8 | 0.959 | run1: 975.3 vs 924.7 ❌; run2: 991.7 vs 1,173.0 ✅; run3: 854.0 vs 772.1 ❌; run4: 1,113.8 vs 1,189.6 ✅; run5: 967.3 vs 849.6 ❌; run6: 1,995.5 vs 1,095.8 ❌; run7: 1,102.0 vs 1,105.0 ✅; run8: 973.1 vs 1,081.9 ✅ |
| p95 response time, ramp (ms) | lower | 5/8 | 0.574 | run1: 416.1 vs 448.5 ✅; run2: 488.8 vs 761.5 ✅; run3: 497.0 vs 505.3 ✅; run4: 651.9 vs 644.5 ❌; run5: 446.5 vs 552.0 ✅; run6: 661.7 vs 833.7 ✅; run7: 792.1 vs 555.6 ❌; run8: 824.1 vs 733.7 ❌ |
| Time with p95 > 1000 ms, high load (%) | lower | 4/8 | 0.798 | run1: 13.5 vs 13.5 ❌; run2: 11.3 vs 19.3 ✅; run3: 6.8 vs 5.8 ❌; run4: 11.1 vs 13.7 ✅; run5: 7.3 vs 3.9 ❌; run6: 26.0 vs 14.8 ❌; run7: 7.7 vs 7.8 ✅; run8: 6.5 vs 9.9 ✅ |
| Throughput, high load (requests/s) | higher | 5/8 | 0.442 | run1: 89.2 vs 85.8 ✅; run2: 87.2 vs 84.8 ✅; run3: 89.5 vs 89.7 ❌; run4: 85.2 vs 85.6 ❌; run5: 89.7 vs 88.2 ✅; run6: 83.4 vs 85.8 ❌; run7: 86.9 vs 85.7 ✅; run8: 86.8 vs 85.5 ✅ |
| Failed requests (count) | lower | 0/8 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖; run6: 0.0 vs 0.0 ➖; run7: 0.0 vs 0.0 ➖; run8: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 1/8 | 0.721 | run1: 701.1 vs 694.5 ❌; run2: 808.6 vs 944.3 ✅; run3: 637.1 vs 564.7 ❌; run4: 969.7 vs 961.1 ❌; run5: 749.2 vs 649.1 ❌; run6: 1,777.3 vs 886.7 ❌; run7: 918.3 vs 900.4 ❌; run8: 828.0 vs 824.6 ❌ |
| p95 checkout, high load (ms) | lower | 6/8 | 0.382 | run1: 533.2 vs 557.6 ✅; run2: 502.1 vs 595.2 ✅; run3: 499.6 vs 422.4 ❌; run4: 574.1 vs 576.2 ✅; run5: 440.2 vs 411.8 ❌; run6: 509.9 vs 562.2 ✅; run7: 492.6 vs 500.7 ✅; run8: 471.2 vs 549.0 ✅ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Median response time, high load (ms) | 266.48 ± 38.18 (n=8) | 227.65 ± 32.98 (n=8) |
| p95 response time, high load (ms) | 747.93 ± 124.92 (n=8) | 811.52 ± 284.26 (n=8) |
| p99 response time, high load (ms) | 1,023.96 ± 155.11 (n=8) | 1,121.60 ± 362.51 (n=8) |
| p95 response time, ramp (ms) | 629.36 ± 136.21 (n=8) | 597.27 ± 157.62 (n=8) |
| Time with p95 > 1000 ms, high load (%) | 11.11 ± 5.15 (n=8) | 11.27 ± 6.47 (n=8) |
| Throughput, high load (requests/s) | 86.40 ± 1.67 (n=8) | 87.23 ± 2.20 (n=8) |
| Failed requests (count) | 0.00 ± 0.00 (n=8) | 0.00 ± 0.00 (n=8) |
| p95 home page, high load (ms) | 803.16 ± 148.41 (n=8) | 923.66 ± 361.60 (n=8) |
| p95 checkout, high load (ms) | 521.89 ± 70.14 (n=8) | 502.83 ± 39.80 (n=8) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
