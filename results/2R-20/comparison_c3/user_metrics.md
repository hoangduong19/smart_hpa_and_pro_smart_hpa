# User-side metrics: 2R-20%

From `locust_stats_history.csv` of 13 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

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

## Consistency (Smart HPA + priority vs Smart HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs Smart HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 0/3 | 0.250 | run1: 398.9 vs 334.7 ❌; run2: 431.1 vs 336.0 ❌; run3: 407.1 vs 339.5 ❌ |
| p95 response time, high load (ms) | lower | 0/3 | 1.000 | run1: 1,240.1 vs 1,028.1 ❌; run2: 1,198.4 vs 1,141.8 ❌; run3: 1,076.2 vs 1,056.5 ❌ |
| p99 response time, high load (ms) | lower | 2/3 | 0.786 | run1: 1,523.6 vs 1,342.3 ❌; run2: 1,478.7 vs 1,493.4 ✅; run3: 1,346.3 vs 1,349.4 ✅ |
| p95 response time, ramp (ms) | lower | 2/3 | 1.000 | run1: 812.0 vs 657.8 ❌; run2: 678.7 vs 694.8 ✅; run3: 700.4 vs 806.7 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 0/3 | 0.393 | run1: 87.5 vs 23.9 ❌; run2: 79.6 vs 31.7 ❌; run3: 45.9 vs 42.2 ❌ |
| Throughput, high load (requests/s) | higher | 0/3 | 0.143 | run1: 80.2 vs 82.2 ❌; run2: 79.6 vs 82.6 ❌; run3: 81.0 vs 82.9 ❌ |
| Failed requests (count) | lower | 0/3 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 2/3 | 0.786 | run1: 1,430.9 vs 1,208.4 ❌; run2: 1,320.9 vs 1,359.3 ✅; run3: 1,211.0 vs 1,221.9 ✅ |
| p95 checkout, high load (ms) | lower | 0/3 | 0.250 | run1: 889.0 vs 670.0 ❌; run2: 899.1 vs 731.2 ❌; run3: 823.5 vs 789.8 ❌ |

## Consistency (Smart HPA + priority vs K8s HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 3/3 | 0.071 | run1: 398.9 vs 425.3 ✅; run2: 431.1 vs 467.4 ✅; run3: 407.1 vs 443.5 ✅ |
| p95 response time, high load (ms) | lower | 3/3 | 0.036 | run1: 1,240.1 vs 1,387.2 ✅; run2: 1,198.4 vs 1,427.0 ✅; run3: 1,076.2 vs 1,346.1 ✅ |
| p99 response time, high load (ms) | lower | 3/3 | 0.036 | run1: 1,523.6 vs 1,694.8 ✅; run2: 1,478.7 vs 1,775.0 ✅; run3: 1,346.3 vs 1,599.8 ✅ |
| p95 response time, ramp (ms) | lower | 1/3 | 0.393 | run1: 812.0 vs 788.2 ❌; run2: 678.7 vs 670.1 ❌; run3: 700.4 vs 843.7 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 3/3 | 0.036 | run1: 87.5 vs 95.3 ✅; run2: 79.6 vs 98.8 ✅; run3: 45.9 vs 94.4 ✅ |
| Throughput, high load (requests/s) | higher | 3/3 | 0.036 | run1: 80.2 vs 77.6 ✅; run2: 79.6 vs 76.4 ✅; run3: 81.0 vs 78.3 ✅ |
| Failed requests (count) | lower | 0/3 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 3/3 | 0.036 | run1: 1,430.9 vs 1,601.0 ✅; run2: 1,320.9 vs 1,666.2 ✅; run3: 1,211.0 vs 1,530.3 ✅ |
| p95 checkout, high load (ms) | lower | 0/3 | 0.250 | run1: 889.0 vs 768.7 ❌; run2: 899.1 vs 885.2 ❌; run3: 823.5 vs 751.7 ❌ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA | Smart HPA + priority |
|---|---|---|---|
| Median response time, high load (ms) | 456.34 ± 23.12 (n=5) | 363.50 ± 45.57 (n=5) | 412.37 ± 16.71 (n=3) |
| p95 response time, high load (ms) | 1,426.15 ± 61.04 (n=5) | 1,237.75 ± 247.35 (n=5) | 1,171.56 ± 85.22 (n=3) |
| p99 response time, high load (ms) | 1,723.66 ± 77.48 (n=5) | 1,577.28 ± 288.31 (n=5) | 1,449.54 ± 92.15 (n=3) |
| p95 response time, ramp (ms) | 793.50 ± 72.32 (n=5) | 757.55 ± 80.35 (n=5) | 730.34 ± 71.51 (n=3) |
| Time with p95 > 1000 ms, high load (%) | 97.30 ± 2.25 (n=5) | 46.71 ± 25.57 (n=5) | 70.99 ± 22.12 (n=3) |
| Throughput, high load (requests/s) | 76.94 ± 1.01 (n=5) | 81.75 ± 1.13 (n=5) | 80.26 ± 0.67 (n=3) |
| Failed requests (count) | 0.00 ± 0.00 (n=5) | 8.80 ± 19.68 (n=5) | 0.00 ± 0.00 (n=3) |
| p95 home page, high load (ms) | 1,633.95 ± 67.66 (n=5) | 1,439.83 ± 267.00 (n=5) | 1,320.97 ± 109.96 (n=3) |
| p95 checkout, high load (ms) | 822.34 ± 58.52 (n=5) | 774.81 ± 115.63 (n=5) | 870.53 ± 41.03 (n=3) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
