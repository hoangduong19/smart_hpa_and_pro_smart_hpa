# Comparison: 2R-20%

Runs found: prosmarthpa run1, prosmarthpa run2, prosmarthpa run3, prosmarthpa run4, prosmarthpa run5, prosmarthpa-authors run1, prosmarthpa-authors run2, prosmarthpa-authors run3, prosmarthpa-authors run4, prosmarthpa-authors run5, prosmarthpa-rerun run1, prosmarthpa-rerun run2.

## Consistency (ProSmart HPA vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA better in | p | Per run (ProSmart HPA vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 3,080.7 vs 2,693.3 ✅; run2: 2,953.0 vs 2,693.6 ✅; run3: 3,113.8 vs 2,696.9 ✅; run4: 3,107.8 vs 2,693.7 ✅; run5: 3,068.3 vs 2,695.3 ✅ |
| CPU Overutilization (%) | lower | 4/5 | 0.222 | run1: 391.3 vs 397.3 ✅; run2: 451.8 vs 502.2 ✅; run3: 421.8 vs 484.9 ✅; run4: 407.1 vs 403.0 ❌; run5: 366.8 vs 488.0 ✅ |
| Overutilization Time (min) | lower | 2/5 | 0.460 | run1: 14.7 vs 14.8 ✅; run2: 14.5 vs 14.8 ✅; run3: 14.8 vs 14.5 ❌; run4: 14.6 vs 14.5 ❌; run5: 14.8 vs 14.5 ❌ |
| CPU Overprovision (m) | lower | 5/5 | 0.008 | run1: 74.6 vs 308.0 ✅; run2: 85.7 vs 172.0 ✅; run3: 65.8 vs 167.2 ✅; run4: 68.6 vs 308.9 ✅; run5: 70.6 vs 182.4 ✅ |
| Overprovision Time (min) | higher | 2/5 | 1.000 | run1: 0.5 vs 0.2 ✅; run2: 0.5 vs 0.4 ✅; run3: 0.4 vs 0.5 ❌; run4: 0.4 vs 0.4 ❌; run5: 0.5 vs 0.5 ❌ |
| CPU Underprovision (m) | lower | 1/5 | 0.056 | run1: 5,906.0 vs 4,030.8 ❌; run2: 6,852.0 vs 5,399.7 ❌; run3: 6,247.9 vs 5,257.8 ❌; run4: 6,369.9 vs 4,084.8 ❌; run5: 5,179.4 vs 5,196.9 ✅ |
| Underprovision Time (min) | lower | 2/5 | 0.889 | run1: 14.5 vs 14.8 ✅; run2: 14.5 vs 14.6 ✅; run3: 14.6 vs 14.5 ❌; run4: 14.6 vs 14.5 ❌; run5: 14.5 vs 14.5 ❌ |
| p95 response time (ms) | lower | 2/5 | 0.548 | run1: 780.0 vs 1,000.0 ✅; run2: 720.0 vs 670.0 ❌; run3: 850.0 vs 810.0 ❌; run4: 840.0 vs 1,000.0 ✅; run5: 800.0 vs 800.0 ➖ |
| Failed requests (%) | lower | 0/5 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖ |

## Consistency (ProSmart HPA, rerun 24/10 vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, rerun 24/10 better in | p | Per run (ProSmart HPA, rerun 24/10 vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 2/2 | 0.095 | run1: 3,107.5 vs 2,693.3 ✅; run2: 3,122.6 vs 2,693.6 ✅ |
| CPU Overutilization (%) | lower | 2/2 | 0.381 | run1: 393.2 vs 397.3 ✅; run2: 418.9 vs 502.2 ✅ |
| Overutilization Time (min) | lower | 2/2 | 0.857 | run1: 14.6 vs 14.8 ✅; run2: 14.8 vs 14.8 ✅ |
| CPU Overprovision (m) | lower | 2/2 | 0.095 | run1: 96.9 vs 308.0 ✅; run2: 86.7 vs 172.0 ✅ |
| Overprovision Time (min) | higher | 2/2 | 0.857 | run1: 0.5 vs 0.2 ✅; run2: 0.5 vs 0.4 ✅ |
| CPU Underprovision (m) | lower | 0/2 | 0.095 | run1: 5,791.0 vs 4,030.8 ❌; run2: 6,528.2 vs 5,399.7 ❌ |
| Underprovision Time (min) | lower | 2/2 | 0.857 | run1: 14.5 vs 14.8 ✅; run2: 14.5 vs 14.6 ✅ |
| p95 response time (ms) | lower | 2/2 | 0.143 | run1: 790.0 vs 1,000.0 ✅; run2: 660.0 vs 670.0 ✅ |
| Failed requests (%) | lower | 0/2 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖ |

## Consistency (ProSmart HPA, rerun 24/10 vs ProSmart HPA, same run number)

Paired runs: [1, 2]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, rerun 24/10 better in | p | Per run (ProSmart HPA, rerun 24/10 vs ProSmart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 2/2 | 0.381 | run1: 3,107.5 vs 3,080.7 ✅; run2: 3,122.6 vs 2,953.0 ✅ |
| CPU Overutilization (%) | lower | 1/2 | 1.000 | run1: 393.2 vs 391.3 ❌; run2: 418.9 vs 451.8 ✅ |
| Overutilization Time (min) | lower | 1/2 | 0.857 | run1: 14.6 vs 14.7 ✅; run2: 14.8 vs 14.5 ❌ |
| CPU Overprovision (m) | lower | 0/2 | 0.095 | run1: 96.9 vs 74.6 ❌; run2: 86.7 vs 85.7 ❌ |
| Overprovision Time (min) | higher | 0/2 | 0.857 | run1: 0.5 vs 0.5 ❌; run2: 0.5 vs 0.5 ❌ |
| CPU Underprovision (m) | lower | 2/2 | 1.000 | run1: 5,791.0 vs 5,906.0 ✅; run2: 6,528.2 vs 6,852.0 ✅ |
| Underprovision Time (min) | lower | 0/2 | 0.857 | run1: 14.5 vs 14.5 ❌; run2: 14.5 vs 14.5 ❌ |
| p95 response time (ms) | lower | 1/2 | 0.381 | run1: 790.0 vs 780.0 ❌; run2: 660.0 vs 720.0 ✅ |
| Failed requests (%) | lower | 0/2 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | ProSmart HPA | ProSmart HPA, rerun 24/10 | ProSmart HPA, authors' models |
|---|---|---|---|
| Supply CPU (m) | 3,064.71 ± 65.22 (n=5) | 3,115.06 ± 10.70 (n=2) | 2,694.54 ± 1.51 (n=5) |
| CPU Overutilization (%) | 407.77 ± 31.94 (n=5) | 406.04 ± 18.13 (n=2) | 455.07 ± 50.61 (n=5) |
| Overutilization Time (min) | 14.69 ± 0.14 (n=5) | 14.67 ± 0.11 (n=2) | 14.62 ± 0.16 (n=5) |
| CPU Overprovision (m) | 73.06 ± 7.75 (n=5) | 91.78 ± 7.18 (n=2) | 227.69 ± 73.95 (n=5) |
| Overprovision Time (min) | 0.45 ± 0.06 (n=5) | 0.48 ± 0.01 (n=2) | 0.41 ± 0.12 (n=5) |
| CPU Underprovision (m) | 6,111.06 ± 621.44 (n=5) | 6,159.60 ± 521.28 (n=2) | 4,794.01 ± 676.35 (n=5) |
| Underprovision Time (min) | 14.53 ± 0.06 (n=5) | 14.50 ± 0.01 (n=2) | 14.57 ± 0.12 (n=5) |
| p95 response time (ms) | 798.00 ± 52.15 (n=5) | 725.00 ± 91.92 (n=2) | 856.00 ± 142.58 (n=5) |
| Failed requests (%) | 0.00 ± 0.00 (n=5) | 0.00 ± 0.00 (n=2) | 0.00 ± 0.00 (n=5) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
