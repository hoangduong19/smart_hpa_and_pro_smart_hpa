# Comparison: 2R-20%

Runs found: k8shpa run1, k8shpa run2, k8shpa run3, smarthpa run1, smarthpa run2, smarthpa run3. Paired runs: [1, 2, 3].

## Consistency (Smart HPA vs K8s HPA, same run number)

| Metric | Better is | Smart HPA better in | Per run (Smart vs K8s) |
|---|---|---|---|
| Supply CPU (m) | higher | 3/3 | run1: 2,434.2 vs 2,079.9 ✅; run2: 2,450.8 vs 2,086.8 ✅; run3: 2,449.4 vs 2,076.8 ✅ |
| CPU Overutilization (%) | lower | 0/3 | run1: 684.5 vs 463.7 ❌; run2: 662.8 vs 457.8 ❌; run3: 674.8 vs 468.1 ❌ |
| Overutilization Time (min) | lower | 1/3 | run1: 14.6 vs 14.7 ✅; run2: 14.6 vs 14.6 ❌; run3: 14.9 vs 14.7 ❌ |
| CPU Overprovision (m) | lower | 3/3 | run1: 86.2 vs 444.6 ✅; run2: 70.2 vs 438.8 ✅; run3: 70.8 vs 432.1 ✅ |
| Overprovision Time (min) | higher | 3/3 | run1: 0.6 vs 0.3 ✅; run2: 0.6 vs 0.4 ✅; run3: 0.6 vs 0.3 ✅ |
| CPU Underprovision (m) | lower | 0/3 | run1: 4,683.1 vs 3,743.8 ❌; run2: 5,648.0 vs 3,682.2 ❌; run3: 5,118.8 vs 3,725.7 ❌ |
| Underprovision Time (min) | lower | 3/3 | run1: 14.3 vs 14.7 ✅; run2: 14.4 vs 14.6 ✅; run3: 14.4 vs 14.7 ✅ |
| p95 response time (ms) | lower | 3/3 | run1: 930.0 vs 1,300.0 ✅; run2: 990.0 vs 1,300.0 ✅; run3: 1,000.0 vs 1,300.0 ✅ |
| Failed requests (%) | lower | 0/3 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Supply CPU (m) | 2,081.16 ± 5.07 (n=3) | 2,444.79 ± 9.18 (n=3) |
| CPU Overutilization (%) | 463.21 ± 5.15 (n=3) | 674.02 ± 10.88 (n=3) |
| Overutilization Time (min) | 14.64 ± 0.03 (n=3) | 14.70 ± 0.16 (n=3) |
| CPU Overprovision (m) | 438.49 ± 6.25 (n=3) | 75.76 ± 9.05 (n=3) |
| Overprovision Time (min) | 0.33 ± 0.04 (n=3) | 0.61 ± 0.03 (n=3) |
| CPU Underprovision (m) | 3,717.22 ± 31.62 (n=3) | 5,149.92 ± 483.21 (n=3) |
| Underprovision Time (min) | 14.64 ± 0.03 (n=3) | 14.38 ± 0.04 (n=3) |
| p95 response time (ms) | 1,300.00 ± 0.00 (n=3) | 973.33 ± 37.86 (n=3) |
| Failed requests (%) | 0.00 ± 0.00 (n=3) | 0.00 ± 0.00 (n=3) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
