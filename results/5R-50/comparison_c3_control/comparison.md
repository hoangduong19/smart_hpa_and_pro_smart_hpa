# Comparison: 5R-50%

Runs found: smarthpa run1, smarthpa run2, smarthpa run3, smarthpa run4, smarthpa run5, smarthpa-flat run1, smarthpa-flat run2, smarthpa-flat run3, smarthpa-prio run1, smarthpa-prio run2, smarthpa-prio run3, smarthpa-prio run4, smarthpa-prio run5.

## Consistency (Smart HPA + priority vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs Smart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 3/5 | 0.222 | run1: 4,379.4 vs 3,900.9 ✅; run2: 4,918.4 vs 4,018.7 ✅; run3: 4,534.7 vs 3,582.3 ✅; run4: 3,883.8 vs 3,891.4 ❌; run5: 3,912.6 vs 4,095.5 ❌ |
| CPU Overutilization (%) | lower | 5/5 | 0.008 | run1: 71.1 vs 141.9 ✅; run2: 76.5 vs 209.5 ✅; run3: 76.2 vs 159.6 ✅; run4: 76.8 vs 143.2 ✅; run5: 72.1 vs 148.1 ✅ |
| Overutilization Time (min) | lower | 5/5 | 0.008 | run1: 10.4 vs 14.4 ✅; run2: 11.2 vs 14.3 ✅; run3: 11.1 vs 14.1 ✅; run4: 9.9 vs 13.8 ✅; run5: 9.8 vs 14.5 ✅ |
| CPU Overprovision (m) | lower | 0/5 | 0.008 | run1: 1,801.0 vs 750.7 ❌; run2: 1,304.7 vs 716.5 ❌; run3: 1,650.0 vs 773.2 ❌; run4: 2,304.4 vs 837.1 ❌; run5: 2,288.0 vs 829.9 ❌ |
| Overprovision Time (min) | higher | 5/5 | 0.008 | run1: 14.7 vs 4.5 ✅; run2: 11.6 vs 4.1 ✅; run3: 13.5 vs 4.8 ✅; run4: 14.7 vs 5.1 ✅; run5: 15.0 vs 5.1 ✅ |
| CPU Underprovision (m) | lower | 5/5 | 0.008 | run1: 0.9 vs 381.2 ✅; run2: 43.4 vs 576.8 ✅; run3: 15.7 vs 418.1 ✅; run4: 1.2 vs 326.9 ✅; run5: 0.0 vs 241.5 ✅ |
| Underprovision Time (min) | lower | 5/5 | 0.008 | run1: 0.2 vs 10.4 ✅; run2: 3.3 vs 10.9 ✅; run3: 1.4 vs 10.2 ✅; run4: 0.2 vs 9.9 ✅; run5: 0.0 vs 9.8 ✅ |
| p95 response time (ms) | lower | 5/5 | 0.032 | run1: 780.0 vs 900.0 ✅; run2: 580.0 vs 1,000.0 ✅; run3: 650.0 vs 760.0 ✅; run4: 770.0 vs 1,100.0 ✅; run5: 710.0 vs 880.0 ✅ |
| Failed requests (%) | lower | 1/5 | 0.841 | run1: 0.0 vs 0.0 ❌; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.1 ✅; run4: 0.0 vs 0.0 ❌; run5: 0.0 vs 0.0 ➖ |

## Consistency (Smart HPA + quota fix vs Smart HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + quota fix better in | p | Per run (Smart HPA + quota fix vs Smart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 3/3 | 0.036 | run1: 4,365.7 vs 3,900.9 ✅; run2: 4,317.6 vs 4,018.7 ✅; run3: 4,236.9 vs 3,582.3 ✅ |
| CPU Overutilization (%) | lower | 3/3 | 0.036 | run1: 90.6 vs 141.9 ✅; run2: 79.3 vs 209.5 ✅; run3: 90.1 vs 159.6 ✅ |
| Overutilization Time (min) | lower | 3/3 | 0.036 | run1: 11.1 vs 14.4 ✅; run2: 11.6 vs 14.3 ✅; run3: 11.7 vs 14.1 ✅ |
| CPU Overprovision (m) | lower | 0/3 | 0.036 | run1: 1,801.1 vs 750.7 ❌; run2: 1,839.6 vs 716.5 ❌; run3: 1,932.4 vs 773.2 ❌ |
| Overprovision Time (min) | higher | 3/3 | 0.036 | run1: 13.6 vs 4.5 ✅; run2: 14.5 vs 4.1 ✅; run3: 14.1 vs 4.8 ✅ |
| CPU Underprovision (m) | lower | 3/3 | 0.036 | run1: 18.6 vs 381.2 ✅; run2: 6.1 vs 576.8 ✅; run3: 6.4 vs 418.1 ✅ |
| Underprovision Time (min) | lower | 3/3 | 0.036 | run1: 1.4 vs 10.4 ✅; run2: 0.5 vs 10.9 ✅; run3: 0.8 vs 10.2 ✅ |
| p95 response time (ms) | lower | 3/3 | 0.036 | run1: 720.0 vs 900.0 ✅; run2: 560.0 vs 1,000.0 ✅; run3: 670.0 vs 760.0 ✅ |
| Failed requests (%) | lower | 1/3 | 0.464 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.1 ✅ |

## Consistency (Smart HPA + priority vs Smart HPA + quota fix, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs Smart HPA + quota fix) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 3/3 | 0.786 | run1: 4,379.4 vs 4,365.7 ✅; run2: 4,918.4 vs 4,317.6 ✅; run3: 4,534.7 vs 4,236.9 ✅ |
| CPU Overutilization (%) | lower | 3/3 | 0.036 | run1: 71.1 vs 90.6 ✅; run2: 76.5 vs 79.3 ✅; run3: 76.2 vs 90.1 ✅ |
| Overutilization Time (min) | lower | 3/3 | 0.071 | run1: 10.4 vs 11.1 ✅; run2: 11.2 vs 11.6 ✅; run3: 11.1 vs 11.7 ✅ |
| CPU Overprovision (m) | lower | 3/3 | 0.786 | run1: 1,801.0 vs 1,801.1 ✅; run2: 1,304.7 vs 1,839.6 ✅; run3: 1,650.0 vs 1,932.4 ✅ |
| Overprovision Time (min) | higher | 1/3 | 0.786 | run1: 14.7 vs 13.6 ✅; run2: 11.6 vs 14.5 ❌; run3: 13.5 vs 14.1 ❌ |
| CPU Underprovision (m) | lower | 1/3 | 0.571 | run1: 0.9 vs 18.6 ✅; run2: 43.4 vs 6.1 ❌; run3: 15.7 vs 6.4 ❌ |
| Underprovision Time (min) | lower | 1/3 | 0.786 | run1: 0.2 vs 1.4 ✅; run2: 3.3 vs 0.5 ❌; run3: 1.4 vs 0.8 ❌ |
| p95 response time (ms) | lower | 1/3 | 0.571 | run1: 780.0 vs 720.0 ❌; run2: 580.0 vs 560.0 ❌; run3: 650.0 vs 670.0 ✅ |
| Failed requests (%) | lower | 0/3 | 0.464 | run1: 0.0 vs 0.0 ❌; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | Smart HPA | Smart HPA + quota fix | Smart HPA + priority |
|---|---|---|---|
| Supply CPU (m) | 3,897.78 ± 195.78 (n=5) | 4,306.70 ± 65.07 (n=3) | 4,325.78 ± 437.00 (n=5) |
| CPU Overutilization (%) | 160.44 ± 28.29 (n=5) | 86.64 ± 6.35 (n=3) | 74.54 ± 2.74 (n=5) |
| Overutilization Time (min) | 14.23 ± 0.30 (n=5) | 11.47 ± 0.33 (n=3) | 10.47 ± 0.66 (n=5) |
| CPU Overprovision (m) | 781.48 ± 51.64 (n=5) | 1,857.68 ± 67.47 (n=3) | 1,869.63 ± 428.98 (n=5) |
| Overprovision Time (min) | 4.73 ± 0.42 (n=5) | 14.08 ± 0.45 (n=3) | 13.91 ± 1.39 (n=5) |
| CPU Underprovision (m) | 388.91 ± 124.27 (n=5) | 10.37 ± 7.16 (n=3) | 12.23 ± 18.60 (n=5) |
| Underprovision Time (min) | 10.25 ± 0.42 (n=5) | 0.88 ± 0.45 (n=3) | 1.05 ± 1.39 (n=5) |
| p95 response time (ms) | 928.00 ± 128.53 (n=5) | 650.00 ± 81.85 (n=3) | 698.00 ± 84.08 (n=5) |
| Failed requests (%) | 0.01 ± 0.03 (n=5) | 0.00 ± 0.00 (n=3) | 0.00 ± 0.01 (n=5) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
