# Comparison: 2R-20-v080w5%

Runs found: k8shpa run1, k8shpa run2, k8shpa run3, k8shpa run4, k8shpa run5, k8shpa run6, k8shpa run7, k8shpa run8, smarthpa run1, smarthpa run2, smarthpa run3, smarthpa run4, smarthpa run5, smarthpa run6, smarthpa run7, smarthpa run8.

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5, 6, 7, 8]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 8/8 | 0.000 | run1: 2,455.4 vs 2,139.8 ✅; run2: 2,479.0 vs 2,148.1 ✅; run3: 2,370.6 vs 2,117.3 ✅; run4: 2,475.2 vs 2,239.0 ✅; run5: 2,449.8 vs 2,339.2 ✅; run6: 2,362.2 vs 2,356.1 ✅; run7: 2,457.8 vs 2,233.7 ✅; run8: 2,372.7 vs 2,096.9 ✅ |
| CPU Overutilization (%) | lower | 0/8 | 0.015 | run1: 651.7 vs 510.0 ❌; run2: 494.9 vs 476.0 ❌; run3: 636.3 vs 498.2 ❌; run4: 614.9 vs 485.5 ❌; run5: 636.6 vs 507.6 ❌; run6: 612.0 vs 549.6 ❌; run7: 627.7 vs 474.8 ❌; run8: 479.3 vs 475.2 ❌ |
| Overutilization Time (min) | lower | 3/8 | 0.593 | run1: 14.7 vs 14.6 ❌; run2: 14.6 vs 14.5 ❌; run3: 14.7 vs 14.6 ❌; run4: 14.7 vs 14.7 ❌; run5: 14.8 vs 14.7 ❌; run6: 14.6 vs 14.8 ✅; run7: 14.6 vs 14.8 ✅; run8: 14.6 vs 14.7 ✅ |
| CPU Overprovision (m) | lower | 8/8 | 0.000 | run1: 59.5 vs 384.0 ✅; run2: 55.8 vs 417.4 ✅; run3: 60.8 vs 491.1 ✅; run4: 52.2 vs 348.0 ✅; run5: 67.1 vs 319.7 ✅; run6: 69.5 vs 243.8 ✅; run7: 59.5 vs 366.8 ✅; run8: 64.3 vs 393.6 ✅ |
| Overprovision Time (min) | higher | 7/8 | 0.001 | run1: 0.5 vs 0.4 ✅; run2: 0.7 vs 0.5 ✅; run3: 0.6 vs 0.4 ✅; run4: 0.5 vs 0.5 ❌; run5: 0.6 vs 0.3 ✅; run6: 0.6 vs 0.4 ✅; run7: 0.6 vs 0.2 ✅; run8: 0.7 vs 0.5 ✅ |
| CPU Underprovision (m) | lower | 1/8 | 0.001 | run1: 4,976.1 vs 4,297.5 ❌; run2: 4,767.7 vs 3,931.4 ❌; run3: 5,718.2 vs 4,117.2 ❌; run4: 5,348.1 vs 4,087.5 ❌; run5: 5,439.8 vs 4,185.6 ❌; run6: 4,448.8 vs 4,712.4 ✅; run7: 4,579.6 vs 3,885.0 ❌; run8: 4,581.5 vs 3,798.1 ❌ |
| Underprovision Time (min) | lower | 7/8 | 0.001 | run1: 14.5 vs 14.6 ✅; run2: 14.3 vs 14.5 ✅; run3: 14.4 vs 14.6 ✅; run4: 14.5 vs 14.4 ❌; run5: 14.3 vs 14.7 ✅; run6: 14.4 vs 14.6 ✅; run7: 14.4 vs 14.8 ✅; run8: 14.3 vs 14.5 ✅ |
| p95 response time (ms) | lower | 3/8 | 0.899 | run1: 580.0 vs 670.0 ✅; run2: 610.0 vs 820.0 ✅; run3: 510.0 vs 480.0 ❌; run4: 760.0 vs 710.0 ❌; run5: 510.0 vs 500.0 ❌; run6: 800.0 vs 700.0 ❌; run7: 750.0 vs 710.0 ❌; run8: 680.0 vs 760.0 ✅ |
| Failed requests (%) | lower | 0/8 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖; run6: 0.0 vs 0.0 ➖; run7: 0.0 vs 0.0 ➖; run8: 0.0 vs 0.0 ➖ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Supply CPU (m) | 2,208.76 ± 99.68 (n=8) | 2,427.84 ± 50.16 (n=8) |
| CPU Overutilization (%) | 497.12 ± 25.62 (n=8) | 594.17 ± 67.41 (n=8) |
| Overutilization Time (min) | 14.68 ± 0.11 (n=8) | 14.66 ± 0.08 (n=8) |
| CPU Overprovision (m) | 370.56 ± 72.32 (n=8) | 61.07 ± 5.72 (n=8) |
| Overprovision Time (min) | 0.40 ± 0.11 (n=8) | 0.59 ± 0.06 (n=8) |
| CPU Underprovision (m) | 4,126.84 ± 288.30 (n=8) | 4,982.48 ± 468.75 (n=8) |
| Underprovision Time (min) | 14.59 ± 0.11 (n=8) | 14.39 ± 0.06 (n=8) |
| p95 response time (ms) | 668.75 ± 119.34 (n=8) | 650.00 ± 114.14 (n=8) |
| Failed requests (%) | 0.00 ± 0.00 (n=8) | 0.00 ± 0.00 (n=8) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
