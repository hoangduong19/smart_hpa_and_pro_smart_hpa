# Comparison: 2R-20%

Runs found: prosmarthpa run1, prosmarthpa run2, prosmarthpa run3, prosmarthpa run4, prosmarthpa run5, prosmarthpa-authors run1, prosmarthpa-authors run2, prosmarthpa-authors run3, prosmarthpa-authors run4, prosmarthpa-authors run5, smarthpa run1, smarthpa run2, smarthpa run3, smarthpa run4, smarthpa run5.

## Consistency (ProSmart HPA vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA better in | p | Per run (ProSmart HPA vs Smart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 3,080.7 vs 2,434.2 ✅; run2: 2,953.0 vs 2,450.8 ✅; run3: 3,113.8 vs 2,449.4 ✅; run4: 3,107.8 vs 2,259.3 ✅; run5: 3,068.3 vs 2,449.6 ✅ |
| CPU Overutilization (%) | lower | 5/5 | 0.008 | run1: 391.3 vs 684.5 ✅; run2: 451.8 vs 662.8 ✅; run3: 421.8 vs 674.8 ✅; run4: 407.1 vs 621.6 ✅; run5: 366.8 vs 677.7 ✅ |
| Overutilization Time (min) | lower | 3/5 | 1.000 | run1: 14.7 vs 14.6 ❌; run2: 14.5 vs 14.6 ✅; run3: 14.8 vs 14.9 ✅; run4: 14.6 vs 14.7 ✅; run5: 14.8 vs 14.7 ❌ |
| CPU Overprovision (m) | lower | 4/5 | 0.310 | run1: 74.6 vs 86.2 ✅; run2: 85.7 vs 70.2 ❌; run3: 65.8 vs 70.8 ✅; run4: 68.6 vs 80.8 ✅; run5: 70.6 vs 80.9 ✅ |
| Overprovision Time (min) | higher | 0/5 | 0.008 | run1: 0.5 vs 0.6 ❌; run2: 0.5 vs 0.6 ❌; run3: 0.4 vs 0.6 ❌; run4: 0.4 vs 0.6 ❌; run5: 0.5 vs 0.5 ❌ |
| CPU Underprovision (m) | lower | 0/5 | 0.032 | run1: 5,906.0 vs 4,683.1 ❌; run2: 6,852.0 vs 5,648.0 ❌; run3: 6,247.9 vs 5,118.8 ❌; run4: 6,369.9 vs 5,437.6 ❌; run5: 5,179.4 vs 5,054.8 ❌ |
| Underprovision Time (min) | lower | 0/5 | 0.008 | run1: 14.5 vs 14.3 ❌; run2: 14.5 vs 14.4 ❌; run3: 14.6 vs 14.4 ❌; run4: 14.6 vs 14.4 ❌; run5: 14.5 vs 14.4 ❌ |
| p95 response time (ms) | lower | 5/5 | 0.008 | run1: 780.0 vs 930.0 ✅; run2: 720.0 vs 990.0 ✅; run3: 850.0 vs 1,000.0 ✅; run4: 840.0 vs 1,200.0 ✅; run5: 800.0 vs 1,200.0 ✅ |
| Failed requests (%) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.1 ✅; run5: 0.0 vs 0.0 ➖ |

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

## Consistency (ProSmart HPA, authors' models vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs Smart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 2,500.7 vs 2,434.2 ✅; run2: 2,504.3 vs 2,450.8 ✅; run3: 2,501.5 vs 2,449.4 ✅; run4: 2,501.7 vs 2,259.3 ✅; run5: 2,499.8 vs 2,449.6 ✅ |
| CPU Overutilization (%) | lower | 5/5 | 0.008 | run1: 369.3 vs 684.5 ✅; run2: 376.3 vs 662.8 ✅; run3: 373.6 vs 674.8 ✅; run4: 373.2 vs 621.6 ✅; run5: 396.6 vs 677.7 ✅ |
| Overutilization Time (min) | lower | 5/5 | 0.008 | run1: 14.5 vs 14.6 ✅; run2: 14.4 vs 14.6 ✅; run3: 14.4 vs 14.9 ✅; run4: 14.4 vs 14.7 ✅; run5: 14.5 vs 14.7 ✅ |
| CPU Overprovision (m) | lower | 0/5 | 0.008 | run1: 287.9 vs 86.2 ❌; run2: 264.2 vs 70.2 ❌; run3: 273.7 vs 70.8 ❌; run4: 266.9 vs 80.8 ❌; run5: 284.4 vs 80.9 ❌ |
| Overprovision Time (min) | higher | 1/5 | 0.341 | run1: 0.5 vs 0.6 ❌; run2: 0.6 vs 0.6 ❌; run3: 0.6 vs 0.6 ❌; run4: 0.6 vs 0.6 ✅; run5: 0.5 vs 0.5 ❌ |
| CPU Underprovision (m) | lower | 5/5 | 0.008 | run1: 3,401.9 vs 4,683.1 ✅; run2: 3,470.8 vs 5,648.0 ✅; run3: 3,480.2 vs 5,118.8 ✅; run4: 3,434.2 vs 5,437.6 ✅; run5: 3,779.4 vs 5,054.8 ✅ |
| Underprovision Time (min) | lower | 2/5 | 0.690 | run1: 14.5 vs 14.3 ❌; run2: 14.4 vs 14.4 ❌; run3: 14.4 vs 14.4 ✅; run4: 14.4 vs 14.4 ✅; run5: 14.5 vs 14.4 ❌ |
| p95 response time (ms) | lower | 3/5 | 0.214 | run1: 980.0 vs 930.0 ❌; run2: 990.0 vs 990.0 ➖; run3: 970.0 vs 1,000.0 ✅; run4: 1,000.0 vs 1,200.0 ✅; run5: 870.0 vs 1,200.0 ✅ |
| Failed requests (%) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.1 ✅; run5: 0.1 vs 0.0 ❌ |

## Mean ± standard deviation

| Metric | Smart HPA | ProSmart HPA | ProSmart HPA, authors' models |
|---|---|---|---|
| Supply CPU (m) | 2,408.67 ± 83.76 (n=5) | 3,064.71 ± 65.22 (n=5) | 2,501.62 ± 1.67 (n=5) |
| CPU Overutilization (%) | 664.26 ± 25.13 (n=5) | 407.77 ± 31.94 (n=5) | 377.81 ± 10.83 (n=5) |
| Overutilization Time (min) | 14.69 ± 0.11 (n=5) | 14.69 ± 0.14 (n=5) | 14.43 ± 0.07 (n=5) |
| CPU Overprovision (m) | 77.81 ± 6.99 (n=5) | 73.06 ± 7.75 (n=5) | 275.43 ± 10.44 (n=5) |
| Overprovision Time (min) | 0.59 ± 0.04 (n=5) | 0.45 ± 0.06 (n=5) | 0.55 ± 0.06 (n=5) |
| CPU Underprovision (m) | 5,188.44 ± 371.27 (n=5) | 6,111.06 ± 621.44 (n=5) | 3,513.32 ± 151.98 (n=5) |
| Underprovision Time (min) | 14.39 ± 0.04 (n=5) | 14.53 ± 0.06 (n=5) | 14.43 ± 0.07 (n=5) |
| p95 response time (ms) | 1,064.00 ± 127.00 (n=5) | 798.00 ± 52.15 (n=5) | 962.00 ± 52.63 (n=5) |
| Failed requests (%) | 0.01 ± 0.03 (n=5) | 0.00 ± 0.00 (n=5) | 0.03 ± 0.06 (n=5) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
