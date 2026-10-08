#!/usr/bin/env bash
# Kéo trước mọi image của Online Boutique + ServiceLB vào node hiện tại, có retry.
# Lý do: mạng hay reset kết nối HTTPS nên kubelet kéo image rất chậm / thất bại.
# Kéo sẵn trên CẢ 3 node còn giúp thí nghiệm: khi autoscaler đặt pod mới lên node nào
# thì pod khởi động ngay, thời gian khởi động không bị lẫn thời gian tải image.
# Manifest không đặt imagePullPolicy, tag cố định (không phải :latest) → IfNotPresent → dùng image có sẵn.
#
# Chạy trên từng node:  bash /tmp/prepull-images.sh

set -u

IMAGES=(
  docker.io/rancher/klipper-lb:v0.4.17
  docker.io/library/redis:alpine
)
for s in emailservice checkoutservice recommendationservice frontend paymentservice \
         productcatalogservice cartservice currencyservice shippingservice adservice; do
  IMAGES+=("gcr.io/google-samples/microservices-demo/$s:v0.8.1")
done

MAX_TRIES=40

sudo -v || exit 1   # hỏi mật khẩu sudo một lần ở đầu

failed=()
for img in "${IMAGES[@]}"; do
  if sudo k3s crictl inspecti "$img" >/dev/null 2>&1; then
    echo "[có sẵn] $img"
    continue
  fi
  ok=0
  for i in $(seq "$MAX_TRIES"); do
    if sudo k3s crictl pull "$img" >/dev/null 2>&1; then
      echo "[OK]     $img (lần $i)"
      ok=1
      break
    fi
    echo "  thử lại $i/$MAX_TRIES: $img"
    sleep 3
  done
  [ "$ok" -eq 1 ] || failed+=("$img")
done

echo
echo "== $(hostname): image đã có =="
sudo k3s crictl images | grep -E "microservices-demo|redis|klipper-lb"

if [ "${#failed[@]}" -gt 0 ]; then
  echo
  echo "!! Chưa kéo được (chạy lại script): ${failed[*]}"
  exit 1
fi
echo
echo "== $(hostname): XONG, đủ ${#IMAGES[@]} image =="
