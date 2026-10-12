# User-side metrics: 2R-20%

From `locust_stats_history.csv` of 15 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.016 | run1: 334.7 vs 425.3 ✅; run2: 336.0 vs 467.4 ✅; run3: 339.5 vs 443.5 ✅; run4: 441.8 vs 459.5 ✅; run5: 365.5 vs 486.0 ✅ |
| p95 response time, high load (ms) | lower | 4/5 | 0.151 | run1: 1,028.1 vs 1,387.2 ✅; run2: 1,141.8 vs 1,427.0 ✅; run3: 1,056.5 vs 1,346.1 ✅; run4: 1,623.0 vs 1,483.1 ❌; run5: 1,339.3 vs 1,487.3 ✅ |
| p99 response time, high load (ms) | lower | 4/5 | 0.222 | run1: 1,342.3 vs 1,694.8 ✅; run2: 1,493.4 vs 1,775.0 ✅; run3: 1,349.4 vs 1,599.8 ✅; run4: 2,036.2 vs 1,768.4 ❌; run5: 1,665.1 vs 1,780.3 ✅ |
| p95 response time, ramp (ms) | lower | 3/5 | 0.548 | run1: 657.8 vs 788.2 ✅; run2: 694.8 vs 670.1 ❌; run3: 806.7 vs 843.7 ✅; run4: 774.9 vs 827.8 ✅; run5: 853.5 vs 837.7 ❌ |
| Time with p95 > 1000 ms, high load (%) | lower | 5/5 | 0.008 | run1: 23.9 vs 95.3 ✅; run2: 31.7 vs 98.8 ✅; run3: 42.2 vs 94.4 ✅; run4: 45.9 vs 99.2 ✅; run5: 89.7 vs 98.8 ✅ |
| Throughput, high load (requests/s) | higher | 5/5 | 0.008 | run1: 82.2 vs 77.6 ✅; run2: 82.6 vs 76.4 ✅; run3: 82.9 vs 78.3 ✅; run4: 80.5 vs 76.7 ✅; run5: 80.6 vs 75.8 ✅ |
| Failed requests (count) | lower | 0/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 44.0 vs 0.0 ❌; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 4/5 | 0.222 | run1: 1,208.4 vs 1,601.0 ✅; run2: 1,359.3 vs 1,666.2 ✅; run3: 1,221.9 vs 1,530.3 ✅; run4: 1,841.2 vs 1,685.6 ❌; run5: 1,568.3 vs 1,686.6 ✅ |
| p95 checkout, high load (ms) | lower | 3/5 | 0.310 | run1: 670.0 vs 768.7 ✅; run2: 731.2 vs 885.2 ✅; run3: 789.8 vs 751.7 ❌; run4: 967.0 vs 853.7 ❌; run5: 716.0 vs 852.5 ✅ |

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

## Consistency (ProSmart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA better in | p | Per run (ProSmart HPA vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.008 | run1: 223.5 vs 425.3 ✅; run2: 214.2 vs 467.4 ✅; run3: 268.2 vs 443.5 ✅; run4: 206.6 vs 459.5 ✅; run5: 221.6 vs 486.0 ✅ |
| p95 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 813.0 vs 1,387.2 ✅; run2: 756.4 vs 1,427.0 ✅; run3: 852.1 vs 1,346.1 ✅; run4: 940.3 vs 1,483.1 ✅; run5: 933.3 vs 1,487.3 ✅ |
| p99 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 1,109.4 vs 1,694.8 ✅; run2: 1,018.6 vs 1,775.0 ✅; run3: 1,121.0 vs 1,599.8 ✅; run4: 1,283.9 vs 1,768.4 ✅; run5: 1,235.2 vs 1,780.3 ✅ |
| p95 response time, ramp (ms) | lower | 5/5 | 0.008 | run1: 569.6 vs 788.2 ✅; run2: 468.1 vs 670.1 ✅; run3: 627.5 vs 843.7 ✅; run4: 614.9 vs 827.8 ✅; run5: 654.0 vs 837.7 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 5/5 | 0.008 | run1: 12.7 vs 95.3 ✅; run2: 7.7 vs 98.8 ✅; run3: 12.0 vs 94.4 ✅; run4: 14.8 vs 99.2 ✅; run5: 10.6 vs 98.8 ✅ |
| Throughput, high load (requests/s) | higher | 5/5 | 0.008 | run1: 87.6 vs 77.6 ✅; run2: 87.6 vs 76.4 ✅; run3: 85.3 vs 78.3 ✅; run4: 86.9 vs 76.7 ✅; run5: 86.3 vs 75.8 ✅ |
| Failed requests (count) | lower | 0/5 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 5/5 | 0.008 | run1: 989.9 vs 1,601.0 ✅; run2: 913.3 vs 1,666.2 ✅; run3: 1,015.5 vs 1,530.3 ✅; run4: 1,163.2 vs 1,685.6 ✅; run5: 1,130.5 vs 1,686.6 ✅ |
| p95 checkout, high load (ms) | lower | 5/5 | 0.008 | run1: 650.8 vs 768.7 ✅; run2: 528.1 vs 885.2 ✅; run3: 616.9 vs 751.7 ✅; run4: 575.2 vs 853.7 ✅; run5: 563.6 vs 852.5 ✅ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA | ProSmart HPA |
|---|---|---|---|
| Median response time, high load (ms) | 456.34 ± 23.12 (n=5) | 363.50 ± 45.57 (n=5) | 226.83 ± 24.06 (n=5) |
| p95 response time, high load (ms) | 1,426.15 ± 61.04 (n=5) | 1,237.75 ± 247.35 (n=5) | 859.02 ± 78.76 (n=5) |
| p99 response time, high load (ms) | 1,723.66 ± 77.48 (n=5) | 1,577.28 ± 288.31 (n=5) | 1,153.62 ± 105.91 (n=5) |
| p95 response time, ramp (ms) | 793.50 ± 72.32 (n=5) | 757.55 ± 80.35 (n=5) | 586.82 ± 73.06 (n=5) |
| Time with p95 > 1000 ms, high load (%) | 97.30 ± 2.25 (n=5) | 46.71 ± 25.57 (n=5) | 11.56 ± 2.62 (n=5) |
| Throughput, high load (requests/s) | 76.94 ± 1.01 (n=5) | 81.75 ± 1.13 (n=5) | 86.74 ± 0.96 (n=5) |
| Failed requests (count) | 0.00 ± 0.00 (n=5) | 8.80 ± 19.68 (n=5) | 0.00 ± 0.00 (n=5) |
| p95 home page, high load (ms) | 1,633.95 ± 67.66 (n=5) | 1,439.83 ± 267.00 (n=5) | 1,042.47 ± 103.09 (n=5) |
| p95 checkout, high load (ms) | 822.34 ± 58.52 (n=5) | 774.81 ± 115.63 (n=5) | 586.92 ± 47.77 (n=5) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
