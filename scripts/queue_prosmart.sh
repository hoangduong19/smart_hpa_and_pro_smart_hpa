#!/usr/bin/env bash
# After the Smart/K8s batch v080w5b: switch the app to v0.8.1 (ProSmart package manifest), then 8 ProSmart HPA runs
# with the authors' models, round (E13), window 25 s, 200 users @ 2/s, pod warm-up 200 users / 300 s.
export PATH=$HOME/bin:$PATH
cd ~/Demo/smarthpa || exit 1
while tmux has-session -t v080w5b 2>/dev/null; do sleep 30; done
echo "Smart/K8s batch finished at $(date +%H:%M:%S)"
for s in emailservice checkoutservice recommendationservice frontend paymentservice productcatalogservice cartservice currencyservice shippingservice adservice; do
  kubectl set image deployment/$s server=gcr.io/google-samples/microservices-demo/$s:v0.8.1 >/dev/null || echo "FAIL set image $s"
done
for s in emailservice checkoutservice recommendationservice frontend paymentservice productcatalogservice cartservice currencyservice shippingservice adservice; do
  kubectl rollout status deployment/$s --timeout=300s >/dev/null 2>&1 || echo "NOT READY $s"
done
kubectl get deploy -o custom-columns=N:.metadata.name,IMG:.spec.template.spec.containers[0].image | grep -c v0.8.1
tmux new -d -s prosmart "./run_batch.sh --pairs 2R-20%:1,2R-20%:2,2R-20%:3,2R-20%:4,2R-20%:5,2R-20%:6,2R-20%:7,2R-20%:8 --autoscalers prosmarthpa-authors --spawn-rate 2 --pod-warmup 300 --pod-warmup-users 200 --tag v081w5pro 2>&1 | tee ~/Demo/results/batch_prosmart_\$(date +%Y%m%d-%H%M).log"
tmux ls
echo QUEUED_PROSMART
