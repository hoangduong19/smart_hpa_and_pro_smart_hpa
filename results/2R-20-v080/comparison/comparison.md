# Comparison: 2R-20-v080%

Runs found: k8shpa run1, k8shpa run2.

## Mean ± standard deviation

| Metric | K8s HPA |
|---|---|
| Supply CPU (m) | 2,283.47 ± 36.37 (n=2) |
| CPU Overutilization (%) | 474.15 ± 6.13 (n=2) |
| Overutilization Time (min) | 14.62 ± 0.05 (n=2) |
| CPU Overprovision (m) | 388.57 ± 47.21 (n=2) |
| Overprovision Time (min) | 0.37 ± 0.05 (n=2) |
| CPU Underprovision (m) | 3,964.10 ± 31.12 (n=2) |
| Underprovision Time (min) | 14.62 ± 0.05 (n=2) |
| p95 response time (ms) | 790.00 ± 127.28 (n=2) |
| Failed requests (%) | 0.00 ± 0.00 (n=2) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
