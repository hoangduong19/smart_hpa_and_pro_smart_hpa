# Comparison: 2R-20%

Runs found: prosmarthpa run1, prosmarthpa run2, prosmarthpa run3, prosmarthpa run4, prosmarthpa run5, prosmarthpa-authors run1, prosmarthpa-authors run2, prosmarthpa-authors run3, prosmarthpa-authors run4, prosmarthpa-authors run5, prosmarthpa-rerun run1, prosmarthpa-rerun run2.

## Consistency (ProSmart HPA vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA better in | p | Per run (ProSmart HPA vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 3,080.7 vs 2,500.7 ✅; run2: 2,953.0 vs 2,504.3 ✅; run3: 3,113.8 vs 2,501.5 ✅; run4: 3,107.8 vs 2,501.7 ✅; run5: 3,068.3 vs 2,499.8 ✅ |
| CPU Overutilization (%) | lower | 1/5 | 0.222 | run1: 391.3 vs 369.3 ❌; run2: 451.8 vs 376.3 ❌; run3: 421.8 vs 373.6 ❌; run4: 407.1 vs 373.2 ❌; run5: 366.8 vs 396.6 ✅ |
| Overutilization Time (min) | lower | 0/5 | 0.016 | run1: 14.7 vs 14.5 ❌; run2: 14.5 vs 14.4 ❌; run3: 14.8 vs 14.4 ❌; run4: 14.6 vs 14.4 ❌; run5: 14.8 vs 14.5 ❌ |
| CPU Overprovision (m) | lower | 5/5 | 0.008 | run1: 74.6 vs 287.9 ✅; run2: 85.7 vs 264.2 ✅; run3: 65.8 vs 273.7 ✅; run4: 68.6 vs 266.9 ✅; run5: 70.6 vs 284.4 ✅ |
| Overprovision Time (min) | higher | 0/5 | 0.032 | run1: 0.5 vs 0.5 ❌; run2: 0.5 vs 0.6 ❌; run3: 0.4 vs 0.6 ❌; run4: 0.4 vs 0.6 ❌; run5: 0.5 vs 0.5 ❌ |
| CPU Underprovision (m) | lower | 0/5 | 0.008 | run1: 5,906.0 vs 3,401.9 ❌; run2: 6,852.0 vs 3,470.8 ❌; run3: 6,247.9 vs 3,480.2 ❌; run4: 6,369.9 vs 3,434.2 ❌; run5: 5,179.4 vs 3,779.4 ❌ |
| Underprovision Time (min) | lower | 1/5 | 0.056 | run1: 14.5 vs 14.5 ✅; run2: 14.5 vs 14.4 ❌; run3: 14.6 vs 14.4 ❌; run4: 14.6 vs 14.4 ❌; run5: 14.5 vs 14.5 ❌ |
| p95 response time (ms) | lower | 5/5 | 0.008 | run1: 780.0 vs 980.0 ✅; run2: 720.0 vs 990.0 ✅; run3: 850.0 vs 970.0 ✅; run4: 840.0 vs 1,000.0 ✅; run5: 800.0 vs 870.0 ✅ |
| Failed requests (%) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.1 ✅ |

## Consistency (ProSmart HPA, rerun 24/10 vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, rerun 24/10 better in | p | Per run (ProSmart HPA, rerun 24/10 vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 2/2 | 0.095 | run1: 3,107.5 vs 2,500.7 ✅; run2: 3,122.6 vs 2,504.3 ✅ |
| CPU Overutilization (%) | lower | 0/2 | 0.190 | run1: 393.2 vs 369.3 ❌; run2: 418.9 vs 376.3 ❌ |
| Overutilization Time (min) | lower | 0/2 | 0.095 | run1: 14.6 vs 14.5 ❌; run2: 14.8 vs 14.4 ❌ |
| CPU Overprovision (m) | lower | 2/2 | 0.095 | run1: 96.9 vs 287.9 ✅; run2: 86.7 vs 264.2 ✅ |
| Overprovision Time (min) | higher | 0/2 | 0.381 | run1: 0.5 vs 0.5 ❌; run2: 0.5 vs 0.6 ❌ |
| CPU Underprovision (m) | lower | 0/2 | 0.095 | run1: 5,791.0 vs 3,401.9 ❌; run2: 6,528.2 vs 3,470.8 ❌ |
| Underprovision Time (min) | lower | 0/2 | 0.381 | run1: 14.5 vs 14.5 ❌; run2: 14.5 vs 14.4 ❌ |
| p95 response time (ms) | lower | 2/2 | 0.095 | run1: 790.0 vs 980.0 ✅; run2: 660.0 vs 990.0 ✅ |
| Failed requests (%) | lower | 0/2 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖ |

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
| Supply CPU (m) | 3,064.71 ± 65.22 (n=5) | 3,115.06 ± 10.70 (n=2) | 2,501.62 ± 1.67 (n=5) |
| CPU Overutilization (%) | 407.77 ± 31.94 (n=5) | 406.04 ± 18.13 (n=2) | 377.81 ± 10.83 (n=5) |
| Overutilization Time (min) | 14.69 ± 0.14 (n=5) | 14.67 ± 0.11 (n=2) | 14.43 ± 0.07 (n=5) |
| CPU Overprovision (m) | 73.06 ± 7.75 (n=5) | 91.78 ± 7.18 (n=2) | 275.43 ± 10.44 (n=5) |
| Overprovision Time (min) | 0.45 ± 0.06 (n=5) | 0.48 ± 0.01 (n=2) | 0.55 ± 0.06 (n=5) |
| CPU Underprovision (m) | 6,111.06 ± 621.44 (n=5) | 6,159.60 ± 521.28 (n=2) | 3,513.32 ± 151.98 (n=5) |
| Underprovision Time (min) | 14.53 ± 0.06 (n=5) | 14.50 ± 0.01 (n=2) | 14.43 ± 0.07 (n=5) |
| p95 response time (ms) | 798.00 ± 52.15 (n=5) | 725.00 ± 91.92 (n=2) | 962.00 ± 52.63 (n=5) |
| Failed requests (%) | 0.00 ± 0.00 (n=5) | 0.00 ± 0.00 (n=2) | 0.03 ± 0.06 (n=5) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
