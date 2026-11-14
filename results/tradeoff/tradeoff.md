# Trade-off against K8s HPA

## 2R-20%

| Metric | K8s HPA | Smart HPA | ProSmart HPA, authors' models | ProSmart HPA, our models |
|---|---|---|---|---|
| Supply CPU (m) | 2,140.55 | 2,408.67 (+12.5%, 1/5, p=0.016) | 2,501.62 (+16.9%, 0/5, p=0.008) | 2,402.82 (+12.3%, 0/5, p=0.008) |
| Running pods, high load | 19.57 | 23.56 (+20.4%, 0/5, p=0.008) | 22.00 (+12.4%, 0/5, p=0.008) | 22.90 (+17.0%, 0/5, p=0.008) |
| Throughput per reserved vCPU (req/s) | 36.01 | 33.96 (-5.7%, 1/5, p=0.151) | 33.25 (-7.7%, 0/5, p=0.016) | 35.79 (-0.6%, 2/5, p=0.548) |
| Replica changes per run | 8.60 | 5.40 (-37.2%, 5/5, p=0.008) | 9.40 (+9.3%, 1/5, p=0.119) | 6.40 (-25.6%, 5/5, p=0.040) |
| Scale reversals (flapping) per run | 0.00 | 0.60 (0/5, p=0.444) | 0.40 (0/5, p=1.000) | 0.00 (0/5, p=1.000) |
| Quota moves per run | 0.00 | 11.00 (0/5, p=0.008) | 6.00 (0/5, p=0.008) | 11.40 (0/5, p=0.008) |
| Failed requests (all runs) | 0.00 | 44.00 | 89.00 | 0.00 |
| Runs with failed requests | 0.00 | 1.00 | 1.00 | 0.00 |
| Highest failure rate in one run (%) | 0.00 | 0.07 | 0.14 | 0.00 |
| CPU Overutilization (%) | 464.42 | 664.26 (+43.0%, 0/5, p=0.008) | 377.81 (-18.6%, 5/5, p=0.008) | 479.16 (+3.2%, 2/5, p=0.841) |
| CPU Underprovision (m) | 3,727.88 | 5,188.44 (+39.2%, 0/5, p=0.008) | 3,513.32 (-5.8%, 4/5, p=0.151) | 4,217.38 (+13.1%, 1/5, p=0.151) |
| Control loop period, median (s) | - | 2.62 | 2.04 | 1.78 |
| p95 (ms) | 1,426.15 | 1,237.75 (-13.2%, 4/5, p=0.151) | 975.69 (-31.6%, 5/5, p=0.008) | 854.63 (-40.1%, 5/5, p=0.008) |
| Time with p95 > 1 s (%) | 97.30 | 46.71 (-52.0%, 5/5, p=0.008) | 32.05 (-67.1%, 5/5, p=0.008) | 19.91 (-79.5%, 5/5, p=0.008) |
| Throughput (req/s) | 76.94 | 81.75 (+6.2%, 5/5, p=0.008) | 83.19 (+8.1%, 5/5, p=0.008) | 85.99 (+11.8%, 5/5, p=0.008) |

## 5R-50%

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Supply CPU (m) | 2,718.22 | 3,897.78 (+43.4%, 0/5, p=0.008) |
| Running pods, high load | 27.73 | 41.88 (+51.0%, 0/5, p=0.008) |
| Throughput per reserved vCPU (req/s) | 29.96 | 21.78 (-27.3%, 0/5, p=0.008) |
| Replica changes per run | 16.20 | 37.00 (+128.4%, 0/5, p=0.008) |
| Scale reversals (flapping) per run | 0.40 | 9.00 (+2150.0%, 0/5, p=0.008) |
| Quota moves per run | 0.00 | 31.20 (0/5, p=0.008) |
| Failed requests (all runs) | 99.00 | 45.00 |
| Runs with failed requests | 1.00 | 2.00 |
| Highest failure rate in one run (%) | 0.17 | 0.07 |
| CPU Overutilization (%) | 212.57 | 160.44 (-24.5%, 5/5, p=0.056) |
| CPU Underprovision (m) | 915.73 | 388.91 (-57.5%, 5/5, p=0.056) |
| Control loop period, median (s) | - | 2.63 |
| p95 (ms) | 1,396.89 | 1,085.02 (-22.3%, 3/5, p=0.841) |
| Time with p95 > 1 s (%) | 51.10 | 30.65 (-40.0%, 2/5, p=0.595) |
| Throughput (req/s) | 81.40 | 84.70 (+4.1%, 3/5, p=0.421) |

## 5R-50% spike

| Metric | K8s HPA | Smart HPA |
|---|---|---|
| Supply CPU (m) | 2,733.99 | 2,715.00 (-0.7%, 2/3, p=1.000) |
| Running pods, high load | 28.03 | 30.65 (+9.3%, 0/3, p=0.100) |
| Throughput per reserved vCPU (req/s) | 34.96 | 35.65 (+2.0%, 2/3, p=0.700) |
| Replica changes per run | 12.33 | 89.00 (+621.6%, 0/3, p=0.100) |
| Scale reversals (flapping) per run | 0.00 | 42.67 (0/3, p=0.100) |
| Quota moves per run | 0.00 | 27.33 (0/3, p=0.100) |
| Failed requests (all runs) | 0.00 | 39.00 |
| Runs with failed requests | 0.00 | 2.00 |
| Highest failure rate in one run (%) | 0.00 | 0.08 |
| CPU Overutilization (%) | 132.62 | 44.87 (-66.2%, 3/3, p=0.100) |
| CPU Underprovision (m) | 484.23 | 0.00 (-100.0%, 3/3, p=0.100) |
| Control loop period, median (s) | - | 2.82 |
| p95 (ms) | 1,535.19 | 1,467.96 (-4.4%, 2/3, p=1.000) |
| Time with p95 > 1 s (%) | 74.12 | 72.76 (-1.8%, 1/3, p=1.000) |
| Throughput (req/s) | 95.49 | 96.80 (+1.4%, 2/3, p=1.000) |

Cells: value over runs (change vs K8s HPA, runs better than K8s HPA in the same run number, exact two-sided Mann-Whitney U p). 5R-50% spike: user metrics of the spike phase. Control loop: K8s HPA runs inside the cluster, its observer's period is not a control loop, so it is left out.
