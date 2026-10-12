# Comparison: 5R-50%

Runs found: k8shpa run1, k8shpa run2, k8shpa run3, k8shpa run4, k8shpa run5, smarthpa run1, smarthpa run2, smarthpa run3, smarthpa run4, smarthpa run5.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5].

| Metric | Better is | Smart HPA better in | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | run1: 3,900.9 vs 2,652.5 ✅; run2: 4,018.7 vs 2,950.2 ✅; run3: 3,582.3 vs 2,737.8 ✅; run4: 3,891.4 vs 2,654.5 ✅; run5: 4,095.5 vs 2,596.1 ✅ |
| CPU Overutilization (%) | lower | 5/5 | run1: 141.9 vs 215.3 ✅; run2: 209.5 vs 267.5 ✅; run3: 159.6 vs 223.4 ✅; run4: 143.2 vs 202.1 ✅; run5: 148.1 vs 154.5 ✅ |
| Overutilization Time (min) | lower | 4/5 | run1: 14.4 vs 14.5 ✅; run2: 14.3 vs 14.6 ✅; run3: 14.1 vs 14.2 ✅; run4: 13.8 vs 13.9 ✅; run5: 14.5 vs 14.4 ❌ |
| CPU Overprovision (m) | lower | 5/5 | run1: 750.7 vs 3,622.5 ✅; run2: 716.5 vs 3,441.8 ✅; run3: 773.2 vs 3,560.8 ✅; run4: 837.1 vs 3,697.6 ✅; run5: 829.9 vs 3,618.4 ✅ |
| Overprovision Time (min) | higher | 5/5 | run1: 4.5 vs 1.5 ✅; run2: 4.1 vs 0.7 ✅; run3: 4.8 vs 2.3 ✅; run4: 5.1 vs 2.6 ✅; run5: 5.1 vs 1.9 ✅ |
| CPU Underprovision (m) | lower | 5/5 | run1: 381.2 vs 1,035.4 ✅; run2: 576.8 vs 1,475.6 ✅; run3: 418.1 vs 857.9 ✅; run4: 326.9 vs 843.0 ✅; run5: 241.5 vs 366.7 ✅ |
| Underprovision Time (min) | lower | 5/5 | run1: 10.4 vs 13.5 ✅; run2: 10.9 vs 14.3 ✅; run3: 10.2 vs 12.7 ✅; run4: 9.9 vs 12.4 ✅; run5: 9.8 vs 13.0 ✅ |
| p95 response time (ms) | lower | 3/5 | run1: 900.0 vs 910.0 ✅; run2: 1,000.0 vs 640.0 ❌; run3: 760.0 vs 1,400.0 ✅; run4: 1,100.0 vs 1,000.0 ❌; run5: 880.0 vs 1,500.0 ✅ |
| Failed requests (%) | lower | 1/5 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.1 vs 0.2 ✅; run4: 0.0 vs 0.0 ❌; run5: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Supply CPU (m) | 2,718.22 ± 139.17 (n=5) | 3,897.78 ± 195.78 (n=5) |
| CPU Overutilization (%) | 212.57 ± 40.67 (n=5) | 160.44 ± 28.29 (n=5) |
| Overutilization Time (min) | 14.32 ± 0.28 (n=5) | 14.23 ± 0.30 (n=5) |
| CPU Overprovision (m) | 3,588.22 ± 95.21 (n=5) | 781.48 ± 51.64 (n=5) |
| Overprovision Time (min) | 1.81 ± 0.73 (n=5) | 4.73 ± 0.42 (n=5) |
| CPU Underprovision (m) | 915.73 ± 399.35 (n=5) | 388.91 ± 124.27 (n=5) |
| Underprovision Time (min) | 13.17 ± 0.74 (n=5) | 10.25 ± 0.42 (n=5) |
| p95 response time (ms) | 1,090.00 ± 356.09 (n=5) | 928.00 ± 128.53 (n=5) |
| Failed requests (%) | 0.03 ± 0.08 (n=5) | 0.01 ± 0.03 (n=5) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
