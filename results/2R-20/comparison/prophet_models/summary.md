# Authors' PROPHET models vs ours (2R-20%)

## 1. What the authors trained on

- 1810 rows = 10 runs x 181 points (5 s grid, 0-900 s)
- total maxR over the 11 services: 22 to 22 on every row
- rows where some service maxR differs from 2 (quota moved): 1800

## 2. Training data vs our Smart HPA Knowledge Base (runs [1, 2, 3, 4, 5]), DR mean from minute 5

```
              service  authors_DR_steady  ours_DR_steady  diff_pct  authors_maxR_min  authors_maxR_max  ours_maxR_min  ours_maxR_max
            adservice               2.00            1.17    -41.28               2.0               2.0            1.0            2.0
          cartservice               3.70            4.26     15.08               2.0               2.0            1.0            2.0
      checkoutservice               2.89            4.45     53.82               2.0               2.0            1.0            2.0
      currencyservice              11.04           20.92     89.41               2.0               3.0            2.0           12.0
         emailservice               1.38            1.73     25.51               1.0               2.0            1.0            2.0
             frontend              18.35           24.55     33.81               2.0               3.0            2.0            5.0
       paymentservice               2.98            4.39     47.17               2.0               2.0            1.0            2.0
productcatalogservice               7.15            9.28     29.66               2.0               2.0            1.0            2.0
recommendationservice               7.18            8.24     14.74               2.0               2.0            1.0            2.0
           redis-cart               2.00            1.97     -1.46               2.0               2.0            2.0            2.0
      shippingservice               1.95            2.48     27.18               2.0               2.0            1.0            2.0
```

## 3. Prediction error at t + 25 s on runs [4, 5] (replicas)

```
    kind       model  mae  under_pct
  demand     authors 1.93      41.87
  demand        ours 0.96      14.65
  demand same_as_now 0.58      22.83
capacity     authors 1.23      13.64
capacity        ours 0.42       0.84
capacity same_as_now 0.04       0.48
```
