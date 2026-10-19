# Comparison: 5R-50% spike

Runs found: k8shpa run1, k8shpa run2, k8shpa run3, smarthpa run1, smarthpa run2, smarthpa run3.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 1/3 | 1.000 | run1: 2,735.1 vs 2,890.4 ❌; run2: 2,739.5 vs 2,583.9 ✅; run3: 2,670.5 vs 2,727.7 ❌ |
| CPU Overutilization (%) | lower | 3/3 | 0.100 | run1: 38.3 vs 158.6 ✅; run2: 47.2 vs 110.1 ✅; run3: 49.1 vs 129.2 ✅ |
| Overutilization Time (min) | lower | 3/3 | 0.100 | run1: 5.3 vs 13.0 ✅; run2: 6.5 vs 11.8 ✅; run3: 7.5 vs 13.0 ✅ |
| CPU Overprovision (m) | lower | 3/3 | 0.100 | run1: 2,552.4 vs 3,750.4 ✅; run2: 3,109.2 vs 3,947.6 ✅; run3: 2,965.6 vs 3,822.3 ✅ |
| Overprovision Time (min) | higher | 3/3 | 0.100 | run1: 15.0 vs 2.7 ✅; run2: 15.0 vs 7.2 ✅; run3: 15.0 vs 5.4 ✅ |
| CPU Underprovision (m) | lower | 3/3 | 0.100 | run1: 0.0 vs 784.5 ✅; run2: 0.0 vs 272.9 ✅; run3: 0.0 vs 395.2 ✅ |
| Underprovision Time (min) | lower | 3/3 | 0.100 | run1: 0.0 vs 12.3 ✅; run2: 0.0 vs 7.7 ✅; run3: 0.0 vs 9.5 ✅ |
| p95 response time (ms) | lower | 1/3 | 1.000 | run1: 1,200.0 vs 1,000.0 ❌; run2: 1,300.0 vs 1,600.0 ✅; run3: 1,800.0 vs 1,800.0 ➖ |
| Failed requests (%) | lower | 0/3 | 0.400 | run1: 0.0 vs 0.0 ❌; run2: 0.0 vs 0.0 ➖; run3: 0.1 vs 0.0 ❌ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Supply CPU (m) | 2,733.99 ± 153.31 (n=3) | 2,715.00 ± 38.63 (n=3) |
| CPU Overutilization (%) | 132.62 ± 24.45 (n=3) | 44.87 ± 5.76 (n=3) |
| Overutilization Time (min) | 12.59 ± 0.73 (n=3) | 6.43 ± 1.10 (n=3) |
| CPU Overprovision (m) | 3,840.08 ± 99.79 (n=3) | 2,875.74 ± 289.04 (n=3) |
| Overprovision Time (min) | 5.12 ± 2.29 (n=3) | 14.98 ± 0.01 (n=3) |
| CPU Underprovision (m) | 484.23 ± 267.17 (n=3) | 0.00 ± 0.00 (n=3) |
| Underprovision Time (min) | 9.86 ± 2.31 (n=3) | 0.00 ± 0.00 (n=3) |
| p95 response time (ms) | 1,466.67 ± 416.33 (n=3) | 1,433.33 ± 321.46 (n=3) |
| Failed requests (%) | 0.00 ± 0.00 (n=3) | 0.03 ± 0.04 (n=3) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
