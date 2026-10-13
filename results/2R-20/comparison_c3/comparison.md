# Comparison: 2R-20%

Runs found: k8shpa run1, k8shpa run2, k8shpa run3, k8shpa run4, k8shpa run5, smarthpa run1, smarthpa run2, smarthpa run3, smarthpa run4, smarthpa run5, smarthpa-prio run1, smarthpa-prio run2, smarthpa-prio run3.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 4/5 | 0.016 | run1: 2,434.2 vs 2,079.9 ✅; run2: 2,450.8 vs 2,086.8 ✅; run3: 2,449.4 vs 2,076.8 ✅; run4: 2,259.3 vs 2,308.9 ❌; run5: 2,449.6 vs 2,150.3 ✅ |
| CPU Overutilization (%) | lower | 0/5 | 0.008 | run1: 684.5 vs 463.7 ❌; run2: 662.8 vs 457.8 ❌; run3: 674.8 vs 468.1 ❌; run4: 621.6 vs 462.1 ❌; run5: 677.7 vs 470.3 ❌ |
| Overutilization Time (min) | lower | 2/5 | 0.690 | run1: 14.6 vs 14.7 ✅; run2: 14.6 vs 14.6 ❌; run3: 14.9 vs 14.7 ❌; run4: 14.7 vs 14.3 ❌; run5: 14.7 vs 14.7 ✅ |
| CPU Overprovision (m) | lower | 5/5 | 0.008 | run1: 86.2 vs 444.6 ✅; run2: 70.2 vs 438.8 ✅; run3: 70.8 vs 432.1 ✅; run4: 80.8 vs 274.2 ✅; run5: 80.9 vs 367.8 ✅ |
| Overprovision Time (min) | higher | 4/5 | 0.151 | run1: 0.6 vs 0.3 ✅; run2: 0.6 vs 0.4 ✅; run3: 0.6 vs 0.3 ✅; run4: 0.6 vs 0.7 ❌; run5: 0.5 vs 0.3 ✅ |
| CPU Underprovision (m) | lower | 0/5 | 0.008 | run1: 4,683.1 vs 3,743.8 ❌; run2: 5,648.0 vs 3,682.2 ❌; run3: 5,118.8 vs 3,725.7 ❌; run4: 5,437.6 vs 3,729.2 ❌; run5: 5,054.8 vs 3,758.5 ❌ |
| Underprovision Time (min) | lower | 4/5 | 0.151 | run1: 14.3 vs 14.7 ✅; run2: 14.4 vs 14.6 ✅; run3: 14.4 vs 14.7 ✅; run4: 14.4 vs 14.3 ❌; run5: 14.4 vs 14.7 ✅ |
| p95 response time (ms) | lower | 5/5 | 0.008 | run1: 930.0 vs 1,300.0 ✅; run2: 990.0 vs 1,300.0 ✅; run3: 1,000.0 vs 1,300.0 ✅; run4: 1,200.0 vs 1,400.0 ✅; run5: 1,200.0 vs 1,400.0 ✅ |
| Failed requests (%) | lower | 0/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.1 vs 0.0 ❌; run5: 0.0 vs 0.0 ➖ |

## Consistency (Smart HPA + priority vs Smart HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs Smart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 1/3 | 1.000 | run1: 2,441.9 vs 2,434.2 ✅; run2: 2,450.0 vs 2,450.8 ❌; run3: 2,444.0 vs 2,449.4 ❌ |
| CPU Overutilization (%) | lower | 3/3 | 0.071 | run1: 627.7 vs 684.5 ✅; run2: 595.8 vs 662.8 ✅; run3: 600.7 vs 674.8 ✅ |
| Overutilization Time (min) | lower | 2/3 | 1.000 | run1: 14.5 vs 14.6 ✅; run2: 14.7 vs 14.6 ❌; run3: 14.8 vs 14.9 ✅ |
| CPU Overprovision (m) | lower | 1/3 | 1.000 | run1: 81.9 vs 86.2 ✅; run2: 72.7 vs 70.2 ❌; run3: 74.7 vs 70.8 ❌ |
| Overprovision Time (min) | higher | 1/3 | 0.571 | run1: 0.7 vs 0.6 ✅; run2: 0.5 vs 0.6 ❌; run3: 0.5 vs 0.6 ❌ |
| CPU Underprovision (m) | lower | 2/3 | 1.000 | run1: 6,726.2 vs 4,683.1 ❌; run2: 4,860.1 vs 5,648.0 ✅; run3: 4,919.3 vs 5,118.8 ✅ |
| Underprovision Time (min) | lower | 1/3 | 0.571 | run1: 14.3 vs 14.3 ✅; run2: 14.5 vs 14.4 ❌; run3: 14.5 vs 14.4 ❌ |
| p95 response time (ms) | lower | 0/3 | 0.429 | run1: 1,200.0 vs 930.0 ❌; run2: 1,200.0 vs 990.0 ❌; run3: 1,000.0 vs 1,000.0 ➖ |
| Failed requests (%) | lower | 0/3 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖ |

## Consistency (Smart HPA + priority vs K8s HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA + priority better in | p | Per run (Smart HPA + priority vs K8s HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 3/3 | 0.036 | run1: 2,441.9 vs 2,079.9 ✅; run2: 2,450.0 vs 2,086.8 ✅; run3: 2,444.0 vs 2,076.8 ✅ |
| CPU Overutilization (%) | lower | 0/3 | 0.036 | run1: 627.7 vs 463.7 ❌; run2: 595.8 vs 457.8 ❌; run3: 600.7 vs 468.1 ❌ |
| Overutilization Time (min) | lower | 1/3 | 0.393 | run1: 14.5 vs 14.7 ✅; run2: 14.7 vs 14.6 ❌; run3: 14.8 vs 14.7 ❌ |
| CPU Overprovision (m) | lower | 3/3 | 0.036 | run1: 81.9 vs 444.6 ✅; run2: 72.7 vs 438.8 ✅; run3: 74.7 vs 432.1 ✅ |
| Overprovision Time (min) | higher | 3/3 | 0.161 | run1: 0.7 vs 0.3 ✅; run2: 0.5 vs 0.4 ✅; run3: 0.5 vs 0.3 ✅ |
| CPU Underprovision (m) | lower | 0/3 | 0.036 | run1: 6,726.2 vs 3,743.8 ❌; run2: 4,860.1 vs 3,682.2 ❌; run3: 4,919.3 vs 3,725.7 ❌ |
| Underprovision Time (min) | lower | 3/3 | 0.143 | run1: 14.3 vs 14.7 ✅; run2: 14.5 vs 14.6 ✅; run3: 14.5 vs 14.7 ✅ |
| p95 response time (ms) | lower | 3/3 | 0.018 | run1: 1,200.0 vs 1,300.0 ✅; run2: 1,200.0 vs 1,300.0 ✅; run3: 1,000.0 vs 1,300.0 ✅ |
| Failed requests (%) | lower | 0/3 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA | Smart HPA + priority |
|---|---|---|---|
| Supply CPU (m) | 2,140.55 ± 98.83 (n=5) | 2,408.67 ± 83.76 (n=5) | 2,445.30 ± 4.20 (n=3) |
| CPU Overutilization (%) | 464.42 ± 4.94 (n=5) | 664.26 ± 25.13 (n=5) | 608.04 ± 17.19 (n=3) |
| Overutilization Time (min) | 14.58 ± 0.16 (n=5) | 14.69 ± 0.11 (n=5) | 14.67 ± 0.12 (n=3) |
| CPU Overprovision (m) | 391.49 ± 72.51 (n=5) | 77.81 ± 6.99 (n=5) | 76.42 ± 4.82 (n=3) |
| Overprovision Time (min) | 0.40 ± 0.16 (n=5) | 0.59 ± 0.04 (n=5) | 0.55 ± 0.12 (n=3) |
| CPU Underprovision (m) | 3,727.88 ± 28.63 (n=5) | 5,188.44 ± 371.27 (n=5) | 5,501.86 ± 1,060.72 (n=3) |
| Underprovision Time (min) | 14.58 ± 0.16 (n=5) | 14.39 ± 0.04 (n=5) | 14.42 ± 0.13 (n=3) |
| p95 response time (ms) | 1,340.00 ± 54.77 (n=5) | 1,064.00 ± 127.00 (n=5) | 1,133.33 ± 115.47 (n=3) |
| Failed requests (%) | 0.00 ± 0.00 (n=5) | 0.01 ± 0.03 (n=5) | 0.00 ± 0.00 (n=3) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
