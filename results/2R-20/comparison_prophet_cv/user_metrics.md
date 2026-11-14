# User-side metrics: 2R-20%

From `locust_stats_history.csv` of 20 runs. Ramp = minute 0-5, high load = minute 5-15 (all users active). Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). SLO: p95 of at most 1000 ms.

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

## Consistency (ProSmart HPA, authors' models vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs Smart HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.008 | run1: 316.1 vs 334.7 ✅; run2: 319.5 vs 336.0 ✅; run3: 314.3 vs 339.5 ✅; run4: 328.1 vs 441.8 ✅; run5: 256.1 vs 365.5 ✅ |
| p95 response time, high load (ms) | lower | 5/5 | 0.032 | run1: 1,004.3 vs 1,028.1 ✅; run2: 1,034.0 vs 1,141.8 ✅; run3: 980.6 vs 1,056.5 ✅; run4: 1,041.3 vs 1,623.0 ✅; run5: 818.2 vs 1,339.3 ✅ |
| p99 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 1,261.6 vs 1,342.3 ✅; run2: 1,283.3 vs 1,493.4 ✅; run3: 1,239.9 vs 1,349.4 ✅; run4: 1,309.0 vs 2,036.2 ✅; run5: 1,095.4 vs 1,665.1 ✅ |
| p95 response time, ramp (ms) | lower | 5/5 | 0.016 | run1: 655.1 vs 657.8 ✅; run2: 610.4 vs 694.8 ✅; run3: 679.0 vs 806.7 ✅; run4: 628.9 vs 774.9 ✅; run5: 622.5 vs 853.5 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 3/5 | 0.310 | run1: 37.1 vs 23.9 ❌; run2: 38.6 vs 31.7 ❌; run3: 28.8 vs 42.2 ✅; run4: 35.8 vs 45.9 ✅; run5: 19.9 vs 89.7 ✅ |
| Throughput, high load (requests/s) | higher | 4/5 | 0.222 | run1: 82.2 vs 82.2 ✅; run2: 82.8 vs 82.6 ✅; run3: 82.7 vs 82.9 ❌; run4: 82.2 vs 80.5 ✅; run5: 86.1 vs 80.6 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 44.0 ✅; run5: 89.0 vs 0.0 ❌ |
| p95 home page, high load (ms) | lower | 5/5 | 0.095 | run1: 1,185.3 vs 1,208.4 ✅; run2: 1,226.7 vs 1,359.3 ✅; run3: 1,154.5 vs 1,221.9 ✅; run4: 1,237.0 vs 1,841.2 ✅; run5: 992.4 vs 1,568.3 ✅ |
| p95 checkout, high load (ms) | lower | 5/5 | 0.016 | run1: 611.7 vs 670.0 ✅; run2: 585.6 vs 731.2 ✅; run3: 635.0 vs 789.8 ✅; run4: 672.5 vs 967.0 ✅; run5: 459.1 vs 716.0 ✅ |

## Consistency (ProSmart HPA (CV models) vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs Smart HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 4/5 | 0.056 | run1: 235.0 vs 334.7 ✅; run2: 216.6 vs 336.0 ✅; run3: 340.5 vs 339.5 ❌; run4: 199.5 vs 441.8 ✅; run5: 238.6 vs 365.5 ✅ |
| p95 response time, high load (ms) | lower | 4/5 | 0.032 | run1: 771.5 vs 1,028.1 ✅; run2: 762.5 vs 1,141.8 ✅; run3: 1,122.5 vs 1,056.5 ❌; run4: 767.7 vs 1,623.0 ✅; run5: 848.9 vs 1,339.3 ✅ |
| p99 response time, high load (ms) | lower | 4/5 | 0.032 | run1: 1,030.6 vs 1,342.3 ✅; run2: 1,002.5 vs 1,493.4 ✅; run3: 1,382.2 vs 1,349.4 ❌; run4: 1,059.6 vs 2,036.2 ✅; run5: 1,119.1 vs 1,665.1 ✅ |
| p95 response time, ramp (ms) | lower | 5/5 | 0.032 | run1: 595.7 vs 657.8 ✅; run2: 526.2 vs 694.8 ✅; run3: 695.7 vs 806.7 ✅; run4: 538.6 vs 774.9 ✅; run5: 529.9 vs 853.5 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 4/5 | 0.095 | run1: 6.1 vs 23.9 ✅; run2: 4.4 vs 31.7 ✅; run3: 66.1 vs 42.2 ❌; run4: 7.1 vs 45.9 ✅; run5: 16.0 vs 89.7 ✅ |
| Throughput, high load (requests/s) | higher | 4/5 | 0.056 | run1: 87.1 vs 82.2 ✅; run2: 87.4 vs 82.6 ✅; run3: 81.0 vs 82.9 ❌; run4: 87.9 vs 80.5 ✅; run5: 86.5 vs 80.6 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 44.0 ✅; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 4/5 | 0.032 | run1: 929.8 vs 1,208.4 ✅; run2: 914.6 vs 1,359.3 ✅; run3: 1,301.4 vs 1,221.9 ❌; run4: 957.2 vs 1,841.2 ✅; run5: 1,036.2 vs 1,568.3 ✅ |
| p95 checkout, high load (ms) | lower | 5/5 | 0.008 | run1: 519.1 vs 670.0 ✅; run2: 492.5 vs 731.2 ✅; run3: 645.5 vs 789.8 ✅; run4: 502.5 vs 967.0 ✅; run5: 545.9 vs 716.0 ✅ |

## Consistency (ProSmart HPA (CV models) vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.008 | run1: 235.0 vs 425.3 ✅; run2: 216.6 vs 467.4 ✅; run3: 340.5 vs 443.5 ✅; run4: 199.5 vs 459.5 ✅; run5: 238.6 vs 486.0 ✅ |
| p95 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 771.5 vs 1,387.2 ✅; run2: 762.5 vs 1,427.0 ✅; run3: 1,122.5 vs 1,346.1 ✅; run4: 767.7 vs 1,483.1 ✅; run5: 848.9 vs 1,487.3 ✅ |
| p99 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 1,030.6 vs 1,694.8 ✅; run2: 1,002.5 vs 1,775.0 ✅; run3: 1,382.2 vs 1,599.8 ✅; run4: 1,059.6 vs 1,768.4 ✅; run5: 1,119.1 vs 1,780.3 ✅ |
| p95 response time, ramp (ms) | lower | 5/5 | 0.016 | run1: 595.7 vs 788.2 ✅; run2: 526.2 vs 670.1 ✅; run3: 695.7 vs 843.7 ✅; run4: 538.6 vs 827.8 ✅; run5: 529.9 vs 837.7 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 5/5 | 0.008 | run1: 6.1 vs 95.3 ✅; run2: 4.4 vs 98.8 ✅; run3: 66.1 vs 94.4 ✅; run4: 7.1 vs 99.2 ✅; run5: 16.0 vs 98.8 ✅ |
| Throughput, high load (requests/s) | higher | 5/5 | 0.008 | run1: 87.1 vs 77.6 ✅; run2: 87.4 vs 76.4 ✅; run3: 81.0 vs 78.3 ✅; run4: 87.9 vs 76.7 ✅; run5: 86.5 vs 75.8 ✅ |
| Failed requests (count) | lower | 0/5 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖ |
| p95 home page, high load (ms) | lower | 5/5 | 0.008 | run1: 929.8 vs 1,601.0 ✅; run2: 914.6 vs 1,666.2 ✅; run3: 1,301.4 vs 1,530.3 ✅; run4: 957.2 vs 1,685.6 ✅; run5: 1,036.2 vs 1,686.6 ✅ |
| p95 checkout, high load (ms) | lower | 5/5 | 0.008 | run1: 519.1 vs 768.7 ✅; run2: 492.5 vs 885.2 ✅; run3: 645.5 vs 751.7 ✅; run4: 502.5 vs 853.7 ✅; run5: 545.9 vs 852.5 ✅ |

## Consistency (ProSmart HPA, authors' models vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs K8s HPA) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 5/5 | 0.008 | run1: 316.1 vs 425.3 ✅; run2: 319.5 vs 467.4 ✅; run3: 314.3 vs 443.5 ✅; run4: 328.1 vs 459.5 ✅; run5: 256.1 vs 486.0 ✅ |
| p95 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 1,004.3 vs 1,387.2 ✅; run2: 1,034.0 vs 1,427.0 ✅; run3: 980.6 vs 1,346.1 ✅; run4: 1,041.3 vs 1,483.1 ✅; run5: 818.2 vs 1,487.3 ✅ |
| p99 response time, high load (ms) | lower | 5/5 | 0.008 | run1: 1,261.6 vs 1,694.8 ✅; run2: 1,283.3 vs 1,775.0 ✅; run3: 1,239.9 vs 1,599.8 ✅; run4: 1,309.0 vs 1,768.4 ✅; run5: 1,095.4 vs 1,780.3 ✅ |
| p95 response time, ramp (ms) | lower | 5/5 | 0.016 | run1: 655.1 vs 788.2 ✅; run2: 610.4 vs 670.1 ✅; run3: 679.0 vs 843.7 ✅; run4: 628.9 vs 827.8 ✅; run5: 622.5 vs 837.7 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 5/5 | 0.008 | run1: 37.1 vs 95.3 ✅; run2: 38.6 vs 98.8 ✅; run3: 28.8 vs 94.4 ✅; run4: 35.8 vs 99.2 ✅; run5: 19.9 vs 98.8 ✅ |
| Throughput, high load (requests/s) | higher | 5/5 | 0.008 | run1: 82.2 vs 77.6 ✅; run2: 82.8 vs 76.4 ✅; run3: 82.7 vs 78.3 ✅; run4: 82.2 vs 76.7 ✅; run5: 86.1 vs 75.8 ✅ |
| Failed requests (count) | lower | 0/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 89.0 vs 0.0 ❌ |
| p95 home page, high load (ms) | lower | 5/5 | 0.008 | run1: 1,185.3 vs 1,601.0 ✅; run2: 1,226.7 vs 1,666.2 ✅; run3: 1,154.5 vs 1,530.3 ✅; run4: 1,237.0 vs 1,685.6 ✅; run5: 992.4 vs 1,686.6 ✅ |
| p95 checkout, high load (ms) | lower | 5/5 | 0.008 | run1: 611.7 vs 768.7 ✅; run2: 585.6 vs 885.2 ✅; run3: 635.0 vs 751.7 ✅; run4: 672.5 vs 853.7 ✅; run5: 459.1 vs 852.5 ✅ |

## Consistency (ProSmart HPA (CV models) vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Median response time, high load (ms) | lower | 4/5 | 0.151 | run1: 235.0 vs 316.1 ✅; run2: 216.6 vs 319.5 ✅; run3: 340.5 vs 314.3 ❌; run4: 199.5 vs 328.1 ✅; run5: 238.6 vs 256.1 ✅ |
| p95 response time, high load (ms) | lower | 3/5 | 0.222 | run1: 771.5 vs 1,004.3 ✅; run2: 762.5 vs 1,034.0 ✅; run3: 1,122.5 vs 980.6 ❌; run4: 767.7 vs 1,041.3 ✅; run5: 848.9 vs 818.2 ❌ |
| p99 response time, high load (ms) | lower | 3/5 | 0.222 | run1: 1,030.6 vs 1,261.6 ✅; run2: 1,002.5 vs 1,283.3 ✅; run3: 1,382.2 vs 1,239.9 ❌; run4: 1,059.6 vs 1,309.0 ✅; run5: 1,119.1 vs 1,095.4 ❌ |
| p95 response time, ramp (ms) | lower | 4/5 | 0.151 | run1: 595.7 vs 655.1 ✅; run2: 526.2 vs 610.4 ✅; run3: 695.7 vs 679.0 ❌; run4: 538.6 vs 628.9 ✅; run5: 529.9 vs 622.5 ✅ |
| Time with p95 > 1000 ms, high load (%) | lower | 4/5 | 0.151 | run1: 6.1 vs 37.1 ✅; run2: 4.4 vs 38.6 ✅; run3: 66.1 vs 28.8 ❌; run4: 7.1 vs 35.8 ✅; run5: 16.0 vs 19.9 ✅ |
| Throughput, high load (requests/s) | higher | 4/5 | 0.151 | run1: 87.1 vs 82.2 ✅; run2: 87.4 vs 82.8 ✅; run3: 81.0 vs 82.7 ❌; run4: 87.9 vs 82.2 ✅; run5: 86.5 vs 86.1 ✅ |
| Failed requests (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 89.0 ✅ |
| p95 home page, high load (ms) | lower | 3/5 | 0.222 | run1: 929.8 vs 1,185.3 ✅; run2: 914.6 vs 1,226.7 ✅; run3: 1,301.4 vs 1,154.5 ❌; run4: 957.2 vs 1,237.0 ✅; run5: 1,036.2 vs 992.4 ❌ |
| p95 checkout, high load (ms) | lower | 3/5 | 0.421 | run1: 519.1 vs 611.7 ✅; run2: 492.5 vs 585.6 ✅; run3: 645.5 vs 635.0 ❌; run4: 502.5 vs 672.5 ✅; run5: 545.9 vs 459.1 ❌ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA | ProSmart HPA (CV models) | ProSmart HPA, authors' models |
|---|---|---|---|---|
| Median response time, high load (ms) | 456.34 ± 23.12 (n=5) | 363.50 ± 45.57 (n=5) | 246.05 ± 55.07 (n=5) | 306.82 ± 28.85 (n=5) |
| p95 response time, high load (ms) | 1,426.15 ± 61.04 (n=5) | 1,237.75 ± 247.35 (n=5) | 854.63 ± 153.91 (n=5) | 975.69 ± 91.31 (n=5) |
| p99 response time, high load (ms) | 1,723.66 ± 77.48 (n=5) | 1,577.28 ± 288.31 (n=5) | 1,118.80 ± 153.44 (n=5) | 1,237.85 ± 83.65 (n=5) |
| p95 response time, ramp (ms) | 793.50 ± 72.32 (n=5) | 757.55 ± 80.35 (n=5) | 577.20 ± 71.97 (n=5) | 639.19 ± 27.62 (n=5) |
| Time with p95 > 1000 ms, high load (%) | 97.30 ± 2.25 (n=5) | 46.71 ± 25.57 (n=5) | 19.91 ± 26.18 (n=5) | 32.05 ± 7.76 (n=5) |
| Throughput, high load (requests/s) | 76.94 ± 1.01 (n=5) | 81.75 ± 1.13 (n=5) | 85.99 ± 2.81 (n=5) | 83.19 ± 1.64 (n=5) |
| Failed requests (count) | 0.00 ± 0.00 (n=5) | 8.80 ± 19.68 (n=5) | 0.00 ± 0.00 (n=5) | 17.80 ± 39.80 (n=5) |
| p95 home page, high load (ms) | 1,633.95 ± 67.66 (n=5) | 1,439.83 ± 267.00 (n=5) | 1,027.82 ± 159.94 (n=5) | 1,159.19 ± 98.90 (n=5) |
| p95 checkout, high load (ms) | 822.34 ± 58.52 (n=5) | 774.81 ± 115.63 (n=5) | 541.10 ± 61.79 (n=5) | 592.77 ± 81.25 (n=5) |

Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time).
