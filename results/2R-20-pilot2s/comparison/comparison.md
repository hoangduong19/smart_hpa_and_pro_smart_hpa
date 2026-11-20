# Comparison: 2R-20-pilot2s%

Runs found: k8shpa run1, k8shpa run2, smarthpa run1.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 1/1 | - | run1: 2,471.8 vs 2,295.9 ✅ |
| CPU Overutilization (%) | lower | 0/1 | - | run1: 526.4 vs 486.4 ❌ |
| Overutilization Time (min) | lower | 0/1 | - | run1: 14.7 vs 14.6 ❌ |
| CPU Overprovision (m) | lower | 1/1 | - | run1: 53.6 vs 352.0 ✅ |
| Overprovision Time (min) | higher | 1/1 | - | run1: 0.6 vs 0.3 ✅ |
| CPU Underprovision (m) | lower | 0/1 | - | run1: 4,610.6 vs 3,920.4 ❌ |
| Underprovision Time (min) | lower | 1/1 | - | run1: 14.4 vs 14.6 ✅ |
| p95 response time (ms) | lower | 0/1 | - | run1: 1,400.0 vs 1,200.0 ❌ |
| Failed requests (%) | lower | 0/1 | - | run1: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Supply CPU (m) | 2,210.58 ± 120.61 (n=2) | 2,471.80 (n=1) |
| CPU Overutilization (%) | 492.27 ± 8.25 (n=2) | 526.40 (n=1) |
| Overutilization Time (min) | 14.70 ± 0.10 (n=2) | 14.69 (n=1) |
| CPU Overprovision (m) | 379.52 ± 38.98 (n=2) | 53.59 (n=1) |
| Overprovision Time (min) | 0.27 ± 0.10 (n=2) | 0.57 (n=1) |
| CPU Underprovision (m) | 3,994.75 ± 105.10 (n=2) | 4,610.61 (n=1) |
| Underprovision Time (min) | 14.70 ± 0.10 (n=2) | 14.43 (n=1) |
| p95 response time (ms) | 1,200.00 ± 0.00 (n=2) | 1,400.00 (n=1) |
| Failed requests (%) | 0.00 ± 0.00 (n=2) | 0.00 (n=1) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
