# Comparison: 2R-20%

Runs found: k8shpa run1, k8shpa run2, k8shpa run3, k8shpa run4, k8shpa run5, prosmarthpa-authors run1, prosmarthpa-authors run2, prosmarthpa-authors run3, prosmarthpa-authors run4, prosmarthpa-authors run5, prosmarthpa-cv run1, prosmarthpa-cv run2, prosmarthpa-cv run3, prosmarthpa-cv run4, prosmarthpa-cv run5, smarthpa run1, smarthpa run2, smarthpa run3, smarthpa run4, smarthpa run5.

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

## Consistency (ProSmart HPA, authors' models vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs Smart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 2,500.7 vs 2,434.2 ✅; run2: 2,504.3 vs 2,450.8 ✅; run3: 2,501.5 vs 2,449.4 ✅; run4: 2,501.7 vs 2,259.3 ✅; run5: 2,499.8 vs 2,449.6 ✅ |
| CPU Overutilization (%) | lower | 5/5 | 0.008 | run1: 369.3 vs 684.5 ✅; run2: 376.3 vs 662.8 ✅; run3: 373.6 vs 674.8 ✅; run4: 373.2 vs 621.6 ✅; run5: 396.6 vs 677.7 ✅ |
| Overutilization Time (min) | lower | 5/5 | 0.008 | run1: 14.5 vs 14.6 ✅; run2: 14.4 vs 14.6 ✅; run3: 14.4 vs 14.9 ✅; run4: 14.4 vs 14.7 ✅; run5: 14.5 vs 14.7 ✅ |
| CPU Overprovision (m) | lower | 0/5 | 0.008 | run1: 287.9 vs 86.2 ❌; run2: 264.2 vs 70.2 ❌; run3: 273.7 vs 70.8 ❌; run4: 266.9 vs 80.8 ❌; run5: 284.4 vs 80.9 ❌ |
| Overprovision Time (min) | higher | 1/5 | 0.341 | run1: 0.5 vs 0.6 ❌; run2: 0.6 vs 0.6 ❌; run3: 0.6 vs 0.6 ❌; run4: 0.6 vs 0.6 ✅; run5: 0.5 vs 0.5 ❌ |
| CPU Underprovision (m) | lower | 5/5 | 0.008 | run1: 3,401.9 vs 4,683.1 ✅; run2: 3,470.8 vs 5,648.0 ✅; run3: 3,480.2 vs 5,118.8 ✅; run4: 3,434.2 vs 5,437.6 ✅; run5: 3,779.4 vs 5,054.8 ✅ |
| Underprovision Time (min) | lower | 2/5 | 0.690 | run1: 14.5 vs 14.3 ❌; run2: 14.4 vs 14.4 ❌; run3: 14.4 vs 14.4 ✅; run4: 14.4 vs 14.4 ✅; run5: 14.5 vs 14.4 ❌ |
| p95 response time (ms) | lower | 3/5 | 0.214 | run1: 980.0 vs 930.0 ❌; run2: 990.0 vs 990.0 ➖; run3: 970.0 vs 1,000.0 ✅; run4: 1,000.0 vs 1,200.0 ✅; run5: 870.0 vs 1,200.0 ✅ |
| Failed requests (%) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.1 ✅; run5: 0.1 vs 0.0 ❌ |

## Consistency (ProSmart HPA (CV models) vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs Smart HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 1/5 | 0.151 | run1: 2,416.0 vs 2,434.2 ❌; run2: 2,404.2 vs 2,450.8 ❌; run3: 2,387.1 vs 2,449.4 ❌; run4: 2,408.3 vs 2,259.3 ✅; run5: 2,398.5 vs 2,449.6 ❌ |
| CPU Overutilization (%) | lower | 5/5 | 0.008 | run1: 543.5 vs 684.5 ✅; run2: 455.7 vs 662.8 ✅; run3: 468.6 vs 674.8 ✅; run4: 438.0 vs 621.6 ✅; run5: 490.0 vs 677.7 ✅ |
| Overutilization Time (min) | lower | 4/5 | 0.246 | run1: 14.7 vs 14.6 ❌; run2: 14.6 vs 14.6 ✅; run3: 14.5 vs 14.9 ✅; run4: 14.7 vs 14.7 ✅; run5: 14.6 vs 14.7 ✅ |
| CPU Overprovision (m) | lower | 3/5 | 0.222 | run1: 64.0 vs 86.2 ✅; run2: 68.2 vs 70.2 ✅; run3: 76.3 vs 70.8 ❌; run4: 67.2 vs 80.8 ✅; run5: 82.4 vs 80.9 ❌ |
| Overprovision Time (min) | higher | 2/5 | 0.381 | run1: 0.4 vs 0.6 ❌; run2: 0.4 vs 0.6 ❌; run3: 0.5 vs 0.6 ❌; run4: 0.6 vs 0.6 ✅; run5: 0.7 vs 0.5 ✅ |
| CPU Underprovision (m) | lower | 5/5 | 0.008 | run1: 4,376.8 vs 4,683.1 ✅; run2: 4,430.5 vs 5,648.0 ✅; run3: 3,462.4 vs 5,118.8 ✅; run4: 4,320.9 vs 5,437.6 ✅; run5: 4,496.2 vs 5,054.8 ✅ |
| Underprovision Time (min) | lower | 2/5 | 0.421 | run1: 14.6 vs 14.3 ❌; run2: 14.6 vs 14.4 ❌; run3: 14.5 vs 14.4 ❌; run4: 14.4 vs 14.4 ✅; run5: 14.3 vs 14.4 ✅ |
| p95 response time (ms) | lower | 4/5 | 0.056 | run1: 770.0 vs 930.0 ✅; run2: 740.0 vs 990.0 ✅; run3: 1,100.0 vs 1,000.0 ❌; run4: 750.0 vs 1,200.0 ✅; run5: 810.0 vs 1,200.0 ✅ |
| Failed requests (%) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.1 ✅; run5: 0.0 vs 0.0 ➖ |

## Consistency (ProSmart HPA (CV models) vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs K8s HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 2,416.0 vs 2,079.9 ✅; run2: 2,404.2 vs 2,086.8 ✅; run3: 2,387.1 vs 2,076.8 ✅; run4: 2,408.3 vs 2,308.9 ✅; run5: 2,398.5 vs 2,150.3 ✅ |
| CPU Overutilization (%) | lower | 2/5 | 0.841 | run1: 543.5 vs 463.7 ❌; run2: 455.7 vs 457.8 ✅; run3: 468.6 vs 468.1 ❌; run4: 438.0 vs 462.1 ✅; run5: 490.0 vs 470.3 ❌ |
| Overutilization Time (min) | lower | 3/5 | 0.690 | run1: 14.7 vs 14.7 ❌; run2: 14.6 vs 14.6 ✅; run3: 14.5 vs 14.7 ✅; run4: 14.7 vs 14.3 ❌; run5: 14.6 vs 14.7 ✅ |
| CPU Overprovision (m) | lower | 5/5 | 0.008 | run1: 64.0 vs 444.6 ✅; run2: 68.2 vs 438.8 ✅; run3: 76.3 vs 432.1 ✅; run4: 67.2 vs 274.2 ✅; run5: 82.4 vs 367.8 ✅ |
| Overprovision Time (min) | higher | 4/5 | 0.079 | run1: 0.4 vs 0.3 ✅; run2: 0.4 vs 0.4 ✅; run3: 0.5 vs 0.3 ✅; run4: 0.6 vs 0.7 ❌; run5: 0.7 vs 0.3 ✅ |
| CPU Underprovision (m) | lower | 1/5 | 0.151 | run1: 4,376.8 vs 3,743.8 ❌; run2: 4,430.5 vs 3,682.2 ❌; run3: 3,462.4 vs 3,725.7 ✅; run4: 4,320.9 vs 3,729.2 ❌; run5: 4,496.2 vs 3,758.5 ❌ |
| Underprovision Time (min) | lower | 4/5 | 0.151 | run1: 14.6 vs 14.7 ✅; run2: 14.6 vs 14.6 ✅; run3: 14.5 vs 14.7 ✅; run4: 14.4 vs 14.3 ❌; run5: 14.3 vs 14.7 ✅ |
| p95 response time (ms) | lower | 5/5 | 0.008 | run1: 770.0 vs 1,300.0 ✅; run2: 740.0 vs 1,300.0 ✅; run3: 1,100.0 vs 1,300.0 ✅; run4: 750.0 vs 1,400.0 ✅; run5: 810.0 vs 1,400.0 ✅ |
| Failed requests (%) | lower | 0/5 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖ |

## Consistency (ProSmart HPA, authors' models vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs K8s HPA) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 5/5 | 0.008 | run1: 2,500.7 vs 2,079.9 ✅; run2: 2,504.3 vs 2,086.8 ✅; run3: 2,501.5 vs 2,076.8 ✅; run4: 2,501.7 vs 2,308.9 ✅; run5: 2,499.8 vs 2,150.3 ✅ |
| CPU Overutilization (%) | lower | 5/5 | 0.008 | run1: 369.3 vs 463.7 ✅; run2: 376.3 vs 457.8 ✅; run3: 373.6 vs 468.1 ✅; run4: 373.2 vs 462.1 ✅; run5: 396.6 vs 470.3 ✅ |
| Overutilization Time (min) | lower | 4/5 | 0.151 | run1: 14.5 vs 14.7 ✅; run2: 14.4 vs 14.6 ✅; run3: 14.4 vs 14.7 ✅; run4: 14.4 vs 14.3 ❌; run5: 14.5 vs 14.7 ✅ |
| CPU Overprovision (m) | lower | 5/5 | 0.032 | run1: 287.9 vs 444.6 ✅; run2: 264.2 vs 438.8 ✅; run3: 273.7 vs 432.1 ✅; run4: 266.9 vs 274.2 ✅; run5: 284.4 vs 367.8 ✅ |
| Overprovision Time (min) | higher | 4/5 | 0.151 | run1: 0.5 vs 0.3 ✅; run2: 0.6 vs 0.4 ✅; run3: 0.6 vs 0.3 ✅; run4: 0.6 vs 0.7 ❌; run5: 0.5 vs 0.3 ✅ |
| CPU Underprovision (m) | lower | 4/5 | 0.151 | run1: 3,401.9 vs 3,743.8 ✅; run2: 3,470.8 vs 3,682.2 ✅; run3: 3,480.2 vs 3,725.7 ✅; run4: 3,434.2 vs 3,729.2 ✅; run5: 3,779.4 vs 3,758.5 ❌ |
| Underprovision Time (min) | lower | 4/5 | 0.151 | run1: 14.5 vs 14.7 ✅; run2: 14.4 vs 14.6 ✅; run3: 14.4 vs 14.7 ✅; run4: 14.4 vs 14.3 ❌; run5: 14.5 vs 14.7 ✅ |
| p95 response time (ms) | lower | 5/5 | 0.008 | run1: 980.0 vs 1,300.0 ✅; run2: 990.0 vs 1,300.0 ✅; run3: 970.0 vs 1,300.0 ✅; run4: 1,000.0 vs 1,400.0 ✅; run5: 870.0 vs 1,400.0 ✅ |
| Failed requests (%) | lower | 0/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.1 vs 0.0 ❌ |

## Consistency (ProSmart HPA (CV models) vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Supply CPU (m) | higher | 0/5 | 0.008 | run1: 2,416.0 vs 2,500.7 ❌; run2: 2,404.2 vs 2,504.3 ❌; run3: 2,387.1 vs 2,501.5 ❌; run4: 2,408.3 vs 2,501.7 ❌; run5: 2,398.5 vs 2,499.8 ❌ |
| CPU Overutilization (%) | lower | 0/5 | 0.008 | run1: 543.5 vs 369.3 ❌; run2: 455.7 vs 376.3 ❌; run3: 468.6 vs 373.6 ❌; run4: 438.0 vs 373.2 ❌; run5: 490.0 vs 396.6 ❌ |
| Overutilization Time (min) | lower | 0/5 | 0.008 | run1: 14.7 vs 14.5 ❌; run2: 14.6 vs 14.4 ❌; run3: 14.5 vs 14.4 ❌; run4: 14.7 vs 14.4 ❌; run5: 14.6 vs 14.5 ❌ |
| CPU Overprovision (m) | lower | 5/5 | 0.008 | run1: 64.0 vs 287.9 ✅; run2: 68.2 vs 264.2 ✅; run3: 76.3 vs 273.7 ✅; run4: 67.2 vs 266.9 ✅; run5: 82.4 vs 284.4 ✅ |
| Overprovision Time (min) | higher | 1/5 | 0.635 | run1: 0.4 vs 0.5 ❌; run2: 0.4 vs 0.6 ❌; run3: 0.5 vs 0.6 ❌; run4: 0.6 vs 0.6 ❌; run5: 0.7 vs 0.5 ✅ |
| CPU Underprovision (m) | lower | 1/5 | 0.056 | run1: 4,376.8 vs 3,401.9 ❌; run2: 4,430.5 vs 3,470.8 ❌; run3: 3,462.4 vs 3,480.2 ✅; run4: 4,320.9 vs 3,434.2 ❌; run5: 4,496.2 vs 3,779.4 ❌ |
| Underprovision Time (min) | lower | 1/5 | 0.548 | run1: 14.6 vs 14.5 ❌; run2: 14.6 vs 14.4 ❌; run3: 14.5 vs 14.4 ❌; run4: 14.4 vs 14.4 ❌; run5: 14.3 vs 14.5 ✅ |
| p95 response time (ms) | lower | 4/5 | 0.151 | run1: 770.0 vs 980.0 ✅; run2: 740.0 vs 990.0 ✅; run3: 1,100.0 vs 970.0 ❌; run4: 750.0 vs 1,000.0 ✅; run5: 810.0 vs 870.0 ✅ |
| Failed requests (%) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.1 ✅ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA | ProSmart HPA (CV models) | ProSmart HPA, authors' models |
|---|---|---|---|---|
| Supply CPU (m) | 2,140.55 ± 98.83 (n=5) | 2,408.67 ± 83.76 (n=5) | 2,402.82 ± 10.86 (n=5) | 2,501.62 ± 1.67 (n=5) |
| CPU Overutilization (%) | 464.42 ± 4.94 (n=5) | 664.26 ± 25.13 (n=5) | 479.16 ± 40.66 (n=5) | 377.81 ± 10.83 (n=5) |
| Overutilization Time (min) | 14.58 ± 0.16 (n=5) | 14.69 ± 0.11 (n=5) | 14.60 ± 0.06 (n=5) | 14.43 ± 0.07 (n=5) |
| CPU Overprovision (m) | 391.49 ± 72.51 (n=5) | 77.81 ± 6.99 (n=5) | 71.62 ± 7.55 (n=5) | 275.43 ± 10.44 (n=5) |
| Overprovision Time (min) | 0.40 ± 0.16 (n=5) | 0.59 ± 0.04 (n=5) | 0.52 ± 0.12 (n=5) | 0.55 ± 0.06 (n=5) |
| CPU Underprovision (m) | 3,727.88 ± 28.63 (n=5) | 5,188.44 ± 371.27 (n=5) | 4,217.38 ± 426.98 (n=5) | 3,513.32 ± 151.98 (n=5) |
| Underprovision Time (min) | 14.58 ± 0.16 (n=5) | 14.39 ± 0.04 (n=5) | 14.47 ± 0.12 (n=5) | 14.43 ± 0.07 (n=5) |
| p95 response time (ms) | 1,340.00 ± 54.77 (n=5) | 1,064.00 ± 127.00 (n=5) | 834.00 ± 151.10 (n=5) | 962.00 ± 52.63 (n=5) |
| Failed requests (%) | 0.00 ± 0.00 (n=5) | 0.01 ± 0.03 (n=5) | 0.00 ± 0.00 (n=5) | 0.03 ± 0.06 (n=5) |

Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style).
