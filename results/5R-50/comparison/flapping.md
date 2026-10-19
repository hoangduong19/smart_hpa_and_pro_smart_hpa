# Scaling stability: 5R-50%

From the Knowledge Base of 10 runs, summed over the 11 microservices. A scale reversal is a scale-up followed by a scale-down of the same service, or the reverse. maxR changes count quota moves (0 for K8s HPA, whose maxR is fixed).

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3, 4, 5]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Replica changes (count) | lower | 0/5 | 0.008 | run1: 28.0 vs 15.0 ❌; run2: 29.0 vs 19.0 ❌; run3: 55.0 vs 16.0 ❌; run4: 31.0 vs 18.0 ❌; run5: 42.0 vs 13.0 ❌ |
| Scale reversals (count) | lower | 0/5 | 0.008 | run1: 4.0 vs 0.0 ❌; run2: 4.0 vs 1.0 ❌; run3: 19.0 vs 0.0 ❌; run4: 10.0 vs 1.0 ❌; run5: 8.0 vs 0.0 ❌ |
| maxR changes / quota moves (count) | lower | 0/5 | 0.008 | run1: 27.0 vs 0.0 ❌; run2: 22.0 vs 0.0 ❌; run3: 42.0 vs 0.0 ❌; run4: 28.0 vs 0.0 ❌; run5: 37.0 vs 0.0 ❌ |
| Largest replica swing of one service | lower | 0/5 | 0.008 | run1: 11.0 vs 3.0 ❌; run2: 14.0 vs 3.0 ❌; run3: 13.0 vs 3.0 ❌; run4: 11.0 vs 3.0 ❌; run5: 13.0 vs 3.0 ❌ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Replica changes (count) | 16.20 ± 2.39 (n=5) | 37.00 ± 11.51 (n=5) |
| Scale reversals (count) | 0.40 ± 0.55 (n=5) | 9.00 ± 6.16 (n=5) |
| maxR changes / quota moves (count) | 0.00 ± 0.00 (n=5) | 31.20 ± 8.11 (n=5) |
| Largest replica swing of one service | 3.00 ± 0.00 (n=5) | 12.40 ± 1.34 (n=5) |
