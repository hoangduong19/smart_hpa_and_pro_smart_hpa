# Scaling stability: 2R-20%

From the Knowledge Base of 20 runs, summed over the 11 microservices. A scale reversal is a scale-up followed by a scale-down of the same service, or the reverse. maxR changes count quota moves (0 for K8s HPA, whose maxR is fixed).

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Replica changes (count) | lower | 5/5 | 0.008 | run1: 4.0 vs 8.0 ✅; run2: 5.0 vs 8.0 ✅; run3: 5.0 vs 8.0 ✅; run4: 7.0 vs 10.0 ✅; run5: 6.0 vs 9.0 ✅ |
| Scale reversals (count) | lower | 0/5 | 0.444 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 2.0 vs 0.0 ❌; run5: 1.0 vs 0.0 ❌ |
| maxR changes / quota moves (count) | lower | 0/5 | 0.008 | run1: 10.0 vs 0.0 ❌; run2: 12.0 vs 0.0 ❌; run3: 11.0 vs 0.0 ❌; run4: 10.0 vs 0.0 ❌; run5: 12.0 vs 0.0 ❌ |
| Largest replica swing of one service | lower | 0/5 | 0.008 | run1: 8.0 vs 0.0 ❌; run2: 4.0 vs 0.0 ❌; run3: 9.0 vs 0.0 ❌; run4: 1.0 vs 0.0 ❌; run5: 8.0 vs 0.0 ❌ |

## Consistency (ProSmart HPA, authors' models vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs Smart HPA) |
|---|---|---|---|---|
| Replica changes (count) | lower | 0/5 | 0.008 | run1: 9.0 vs 4.0 ❌; run2: 9.0 vs 5.0 ❌; run3: 9.0 vs 5.0 ❌; run4: 9.0 vs 7.0 ❌; run5: 11.0 vs 6.0 ❌ |
| Scale reversals (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 2.0 ✅; run5: 2.0 vs 1.0 ❌ |
| maxR changes / quota moves (count) | lower | 5/5 | 0.008 | run1: 6.0 vs 10.0 ✅; run2: 6.0 vs 12.0 ✅; run3: 6.0 vs 11.0 ✅; run4: 6.0 vs 10.0 ✅; run5: 6.0 vs 12.0 ✅ |
| Largest replica swing of one service | lower | 5/5 | 0.016 | run1: 0.0 vs 8.0 ✅; run2: 0.0 vs 4.0 ✅; run3: 0.0 vs 9.0 ✅; run4: 0.0 vs 1.0 ✅; run5: 1.0 vs 8.0 ✅ |

## Consistency (ProSmart HPA (CV models) vs Smart HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs Smart HPA) |
|---|---|---|---|---|
| Replica changes (count) | lower | 0/5 | 0.333 | run1: 6.0 vs 4.0 ❌; run2: 6.0 vs 5.0 ❌; run3: 5.0 vs 5.0 ➖; run4: 9.0 vs 7.0 ❌; run5: 6.0 vs 6.0 ➖ |
| Scale reversals (count) | lower | 2/5 | 0.444 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 2.0 ✅; run5: 0.0 vs 1.0 ✅ |
| maxR changes / quota moves (count) | lower | 1/5 | 0.571 | run1: 12.0 vs 10.0 ❌; run2: 9.0 vs 12.0 ✅; run3: 12.0 vs 11.0 ❌; run4: 11.0 vs 10.0 ❌; run5: 13.0 vs 12.0 ❌ |
| Largest replica swing of one service | lower | 4/5 | 0.175 | run1: 6.0 vs 8.0 ✅; run2: 1.0 vs 4.0 ✅; run3: 3.0 vs 9.0 ✅; run4: 4.0 vs 1.0 ❌; run5: 1.0 vs 8.0 ✅ |

## Consistency (ProSmart HPA (CV models) vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs K8s HPA) |
|---|---|---|---|---|
| Replica changes (count) | lower | 5/5 | 0.040 | run1: 6.0 vs 8.0 ✅; run2: 6.0 vs 8.0 ✅; run3: 5.0 vs 8.0 ✅; run4: 9.0 vs 10.0 ✅; run5: 6.0 vs 9.0 ✅ |
| Scale reversals (count) | lower | 0/5 | - | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 0.0 ➖ |
| maxR changes / quota moves (count) | lower | 0/5 | 0.008 | run1: 12.0 vs 0.0 ❌; run2: 9.0 vs 0.0 ❌; run3: 12.0 vs 0.0 ❌; run4: 11.0 vs 0.0 ❌; run5: 13.0 vs 0.0 ❌ |
| Largest replica swing of one service | lower | 0/5 | 0.008 | run1: 6.0 vs 0.0 ❌; run2: 1.0 vs 0.0 ❌; run3: 3.0 vs 0.0 ❌; run4: 4.0 vs 0.0 ❌; run5: 1.0 vs 0.0 ❌ |

## Consistency (ProSmart HPA, authors' models vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA, authors' models better in | p | Per run (ProSmart HPA, authors' models vs K8s HPA) |
|---|---|---|---|---|
| Replica changes (count) | lower | 1/5 | 0.119 | run1: 9.0 vs 8.0 ❌; run2: 9.0 vs 8.0 ❌; run3: 9.0 vs 8.0 ❌; run4: 9.0 vs 10.0 ✅; run5: 11.0 vs 9.0 ❌ |
| Scale reversals (count) | lower | 0/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 2.0 vs 0.0 ❌ |
| maxR changes / quota moves (count) | lower | 0/5 | 0.008 | run1: 6.0 vs 0.0 ❌; run2: 6.0 vs 0.0 ❌; run3: 6.0 vs 0.0 ❌; run4: 6.0 vs 0.0 ❌; run5: 6.0 vs 0.0 ❌ |
| Largest replica swing of one service | lower | 0/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 1.0 vs 0.0 ❌ |

## Consistency (ProSmart HPA (CV models) vs ProSmart HPA, authors' models, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | ProSmart HPA (CV models) better in | p | Per run (ProSmart HPA (CV models) vs ProSmart HPA, authors' models) |
|---|---|---|---|---|
| Replica changes (count) | lower | 4/5 | 0.040 | run1: 6.0 vs 9.0 ✅; run2: 6.0 vs 9.0 ✅; run3: 5.0 vs 9.0 ✅; run4: 9.0 vs 9.0 ➖; run5: 6.0 vs 11.0 ✅ |
| Scale reversals (count) | lower | 1/5 | 1.000 | run1: 0.0 vs 0.0 ➖; run2: 0.0 vs 0.0 ➖; run3: 0.0 vs 0.0 ➖; run4: 0.0 vs 0.0 ➖; run5: 0.0 vs 2.0 ✅ |
| maxR changes / quota moves (count) | lower | 0/5 | 0.008 | run1: 12.0 vs 6.0 ❌; run2: 9.0 vs 6.0 ❌; run3: 12.0 vs 6.0 ❌; run4: 11.0 vs 6.0 ❌; run5: 13.0 vs 6.0 ❌ |
| Largest replica swing of one service | lower | 0/5 | 0.024 | run1: 6.0 vs 0.0 ❌; run2: 1.0 vs 0.0 ❌; run3: 3.0 vs 0.0 ❌; run4: 4.0 vs 0.0 ❌; run5: 1.0 vs 1.0 ➖ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA | ProSmart HPA (CV models) | ProSmart HPA, authors' models |
|---|---|---|---|---|
| Replica changes (count) | 8.60 ± 0.89 (n=5) | 5.40 ± 1.14 (n=5) | 6.40 ± 1.52 (n=5) | 9.40 ± 0.89 (n=5) |
| Scale reversals (count) | 0.00 ± 0.00 (n=5) | 0.60 ± 0.89 (n=5) | 0.00 ± 0.00 (n=5) | 0.40 ± 0.89 (n=5) |
| maxR changes / quota moves (count) | 0.00 ± 0.00 (n=5) | 11.00 ± 1.00 (n=5) | 11.40 ± 1.52 (n=5) | 6.00 ± 0.00 (n=5) |
| Largest replica swing of one service | 0.00 ± 0.00 (n=5) | 6.00 ± 3.39 (n=5) | 3.00 ± 2.12 (n=5) | 0.20 ± 0.45 (n=5) |
