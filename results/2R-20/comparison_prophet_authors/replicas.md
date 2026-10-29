# ProSmart HPA replicas: our models vs the authors' models (2R-20%)

Runs [1, 2, 3, 4, 5], from minute 5. pdr = predicted desired replicas (t + 25 s).

```
         models               service  pdr_mean  maxR_min  maxR_max  replicas_min  replicas_max
     Our models             adservice      1.89         1         1           1.0           1.0
     Our models           cartservice      4.46         1         1           2.0           2.0
     Our models       checkoutservice      4.45         1         2           1.0           2.0
     Our models       currencyservice     25.12         3         7           6.0           9.0
     Our models          emailservice      2.22         1         2           1.0           2.0
     Our models              frontend     31.84         2         6           6.0           6.0
     Our models        paymentservice      4.70         2         2           2.0           2.0
     Our models productcatalogservice      9.29         2         2           2.0           2.0
     Our models recommendationservice      7.94         2         2           2.0           2.0
     Our models            redis-cart      2.69         2         2           2.0           2.0
     Our models       shippingservice      2.83         1         2           1.0           2.0
Authors' models             adservice      2.34         2         2           2.0           2.0
Authors' models           cartservice      4.00         2         2           2.0           2.0
Authors' models       checkoutservice      3.00         2         2           2.0           2.0
Authors' models       currencyservice     11.66         2         2           3.0           3.0
Authors' models          emailservice      2.00         1         2           2.0           2.0
Authors' models              frontend     19.00         2         3           3.0           3.0
Authors' models        paymentservice      3.17         2         2           2.0           2.0
Authors' models productcatalogservice      8.00         2         2           2.0           2.0
Authors' models recommendationservice      8.00         2         2           2.0           2.0
Authors' models            redis-cart      2.00         2         2           2.0           2.0
Authors' models       shippingservice      2.00         2         2           2.0           2.0
```
