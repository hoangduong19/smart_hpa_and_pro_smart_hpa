# Comparison: 2R-20-pilot2s-d5%

Runs found: k8shpa run1, smarthpa run1.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 1/1 | - | run1: 2,409.5 vs 2,116.6 ✅ |
| CPU Overutilization (%) | lower | 0/1 | - | run1: 587.5 vs 448.9 ❌ |
| Overutilization Time (min) | lower | 0/1 | - | run1: 14.7 vs 14.6 ❌ |
| CPU Overprovision (m) | lower | 1/1 | - | run1: 107.8 vs 414.9 ✅ |
| Overprovision Time (min) | higher | 1/1 | - | run1: 0.5 vs 0.4 ✅ |
| CPU Underprovision (m) | lower | 0/1 | - | run1: 4,237.3 vs 3,615.2 ❌ |
| Underprovision Time (min) | lower | 1/1 | - | run1: 14.4 vs 14.6 ✅ |
| p95 response time (ms) | lower | 1/1 | - | run1: 570.0 vs 820.0 ✅ |
| Failed requests (%) | lower | 0/1 | - | run1: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Supply CPU (m) | 2,116.63 (n=1) | 2,409.46 (n=1) |
| CPU Overutilization (%) | 448.92 (n=1) | 587.46 (n=1) |
| Overutilization Time (min) | 14.60 (n=1) | 14.73 (n=1) |
| CPU Overprovision (m) | 414.94 (n=1) | 107.84 (n=1) |
| Overprovision Time (min) | 0.39 (n=1) | 0.54 (n=1) |
| CPU Underprovision (m) | 3,615.17 (n=1) | 4,237.30 (n=1) |
| Underprovision Time (min) | 14.60 (n=1) | 14.42 (n=1) |
| p95 response time (ms) | 820.00 (n=1) | 570.00 (n=1) |
| Failed requests (%) | 0.00 (n=1) | 0.00 (n=1) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
