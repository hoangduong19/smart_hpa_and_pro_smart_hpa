# Scaling stability: 5R-50% spike

From the Knowledge Base of 6 runs, summed over the 11 microservices. A scale reversal is a scale-up followed by a scale-down of the same service, or the reverse. maxR changes count quota moves (0 for K8s HPA, whose maxR is fixed).

## Consistency (Smart HPA vs K8s HPA, same run number)

Paired runs: [1, 2, 3]. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.

| Metric | Better is | Smart HPA better in | p | Per run (Smart HPA vs K8s HPA) |
|---|---|---|---|---|
| Replica changes (count) | lower | 0/3 | 0.100 | run1: 76.0 vs 11.0 ❌; run2: 97.0 vs 12.0 ❌; run3: 94.0 vs 14.0 ❌ |
| Scale reversals (count) | lower | 0/3 | 0.100 | run1: 31.0 vs 0.0 ❌; run2: 49.0 vs 0.0 ❌; run3: 48.0 vs 0.0 ❌ |
| maxR changes / quota moves (count) | lower | 0/3 | 0.100 | run1: 26.0 vs 0.0 ❌; run2: 20.0 vs 0.0 ❌; run3: 36.0 vs 0.0 ❌ |
| Largest replica swing of one service | lower | 0/3 | 0.100 | run1: 11.0 vs 2.0 ❌; run2: 10.0 vs 2.0 ❌; run3: 11.0 vs 3.0 ❌ |

## Mean ± standard deviation

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Replica changes (count) | 12.33 ± 1.53 (n=3) | 89.00 ± 11.36 (n=3) |
| Scale reversals (count) | 0.00 ± 0.00 (n=3) | 42.67 ± 10.12 (n=3) |
| maxR changes / quota moves (count) | 0.00 ± 0.00 (n=3) | 27.33 ± 8.08 (n=3) |
| Largest replica swing of one service | 2.33 ± 0.58 (n=3) | 10.67 ± 0.58 (n=3) |
