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
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 3,080.7 vs 2,693.3 ✅; run2: 2,953.0 vs 2,693.6 ✅; run3: 3,113.8 vs 2,696.9 ✅; run4: 3,107.8 vs 2,693.7 ✅; run5: 3,068.3 vs 2,695.3 ✅ |
| CPU Overutilization (%) | lower | 4/5 | 0.222 | run1: 391.3 vs 397.3 ✅; run2: 451.8 vs 502.2 ✅; run3: 421.8 vs 484.9 ✅; run4: 407.1 vs 403.0 ❌; run5: 366.8 vs 488.0 ✅ |
| Overutilization Time (min) | lower | 2/5 | 0.460 | run1: 14.7 vs 14.8 ✅; run2: 14.5 vs 14.8 ✅; run3: 14.8 vs 14.5 ❌; run4: 14.6 vs 14.5 ❌; run5: 14.8 vs 14.5 ❌ |
| CPU Overprovision (m) | lower | 5/5 | 0.008 | run1: 74.6 vs 308.0 ✅; run2: 85.7 vs 172.0 ✅; run3: 65.8 vs 167.2 ✅; run4: 68.6 vs 308.9 ✅; run5: 70.6 vs 182.4 ✅ |
| Overprovision Time (min) | higher | 2/5 | 1.000 | run1: 0.5 vs 0.2 ✅; run2: 0.5 vs 0.4 ✅; run3: 0.4 vs 0.5 ❌; run4: 0.4 vs 0.4 ❌; run5: 0.5 vs 0.5 ❌ |
| CPU Underprovision (m) | lower | 1/5 | 0.056 | run1: 5,906.0 vs 4,030.8 ❌; run2: 6,852.0 vs 5,399.7 ❌; run3: 6,247.9 vs 5,257.8 ❌; run4: 6,369.9 vs 4,084.8 ❌; run5: 5,179.4 vs 5,196.9 ✅ |
| Underprovision Time (min) | lower | 2/5 | 0.889 | run1: 14.5 vs 14.8 ✅; run2: 14.5 vs 14.6 ✅; run3: 14.6 vs 14.5 ❌; run4: 14.6 vs 14.5 ❌; run5: 14.5 vs 14.5 ❌ |
| p95 response time (ms) | lower | 2/5 | 0.548 | run1: 780.0 vs 1,000.0 ✅; run2: 720.0 vs 670.0 ❌; run3: 850.0 vs 810.0 ❌; run4: 840.0 vs 1,000.0 ✅; run5: 800.0 vs 800.0 ➖ |
| Failed requests (%) | lower | 0/5 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖ |

## Consistency (ProSmart HPA, authors' models vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs Smart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 2,693.3 vs 2,434.2 ✅; run2: 2,693.6 vs 2,450.8 ✅; run3: 2,696.9 vs 2,449.4 ✅; run4: 2,693.7 vs 2,259.3 ✅; run5: 2,695.3 vs 2,449.6 ✅ |
| CPU Overutilization (%) | lower | 5/5 | 0.008 | run1: 397.3 vs 684.5 ✅; run2: 502.2 vs 662.8 ✅; run3: 484.9 vs 674.8 ✅; run4: 403.0 vs 621.6 ✅; run5: 488.0 vs 677.7 ✅ |
| Overutilization Time (min) | lower | 3/5 | 0.421 | run1: 14.8 vs 14.6 ❌; run2: 14.8 vs 14.6 ❌; run3: 14.5 vs 14.9 ✅; run4: 14.5 vs 14.7 ✅; run5: 14.5 vs 14.7 ✅ |
| CPU Overprovision (m) | lower | 0/5 | 0.008 | run1: 308.0 vs 86.2 ❌; run2: 172.0 vs 70.2 ❌; run3: 167.2 vs 70.8 ❌; run4: 308.9 vs 80.8 ❌; run5: 182.4 vs 80.9 ❌ |
| Overprovision Time (min) | higher | 0/5 | 0.008 | run1: 0.2 vs 0.6 ❌; run2: 0.4 vs 0.6 ❌; run3: 0.5 vs 0.6 ❌; run4: 0.4 vs 0.6 ❌; run5: 0.5 vs 0.5 ❌ |
| CPU Underprovision (m) | lower | 3/5 | 0.548 | run1: 4,030.8 vs 4,683.1 ✅; run2: 5,399.7 vs 5,648.0 ✅; run3: 5,257.8 vs 5,118.8 ❌; run4: 4,084.8 vs 5,437.6 ✅; run5: 5,196.9 vs 5,054.8 ❌ |
| Underprovision Time (min) | lower | 0/5 | 0.008 | run1: 14.8 vs 14.3 ❌; run2: 14.6 vs 14.4 ❌; run3: 14.5 vs 14.4 ❌; run4: 14.5 vs 14.4 ❌; run5: 14.5 vs 14.4 ❌ |
| p95 response time (ms) | lower | 4/5 | 0.143 | run1: 1,000.0 vs 930.0 ❌; run2: 670.0 vs 990.0 ✅; run3: 810.0 vs 1,000.0 ✅; run4: 1,000.0 vs 1,200.0 ✅; run5: 800.0 vs 1,200.0 ✅ |
| Failed requests (%) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.1 ✅; run5: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | Smart HPA | ProSmart HPA | ProSmart HPA, authors' models |
|---|---|---|---|
| Supply CPU (m) | 2,408.67 ± 83.76 (n=5) | 3,064.71 ± 65.22 (n=5) | 2,694.54 ± 1.51 (n=5) |
| CPU Overutilization (%) | 664.26 ± 25.13 (n=5) | 407.77 ± 31.94 (n=5) | 455.07 ± 50.61 (n=5) |
| Overutilization Time (min) | 14.69 ± 0.11 (n=5) | 14.69 ± 0.14 (n=5) | 14.62 ± 0.16 (n=5) |
| CPU Overprovision (m) | 77.81 ± 6.99 (n=5) | 73.06 ± 7.75 (n=5) | 227.69 ± 73.95 (n=5) |
| Overprovision Time (min) | 0.59 ± 0.04 (n=5) | 0.45 ± 0.06 (n=5) | 0.41 ± 0.12 (n=5) |
| CPU Underprovision (m) | 5,188.44 ± 371.27 (n=5) | 6,111.06 ± 621.44 (n=5) | 4,794.01 ± 676.35 (n=5) |
| Underprovision Time (min) | 14.39 ± 0.04 (n=5) | 14.53 ± 0.06 (n=5) | 14.57 ± 0.12 (n=5) |
| p95 response time (ms) | 1,064.00 ± 127.00 (n=5) | 798.00 ± 52.15 (n=5) | 856.00 ± 142.58 (n=5) |
| Failed requests (%) | 0.01 ± 0.03 (n=5) | 0.00 ± 0.00 (n=5) | 0.00 ± 0.00 (n=5) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
