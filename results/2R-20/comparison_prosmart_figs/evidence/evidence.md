# Evidence: the authors' Smart HPA data vs their Algorithm 2 / code (2R-20%)

Data: training data inside the authors' 22 released PROPHET models, 10 runs x 181 points (5 s grid).

## E1. Algorithm 2 rule check (no code involved)
- Rows where a service needs >= 1 full replica and other services hold >= 1 full spare replica: **140**
- ... of which no quota moved within 15 s: **102 (73%)**
- Per run: run 1: 11/11, run 2: 8/11, run 3: 8/14, run 4: 5/15, run 5: 10/15, run 6: 10/14, run 7: 10/14, run 8: 10/15, run 9: 13/14, run 10: 17/17
- First violation per run (t, underprovisioned services): run 1: 20 s (currencyservice); run 2: 5 s (currencyservice); run 3: 10 s (currencyservice); run 4: 15 s (currencyservice); run 5: 5 s (currencyservice); run 6: 25 s (currencyservice); run 7: 15 s (currencyservice); run 8: 20 s (currencyservice); run 9: 10 s (currencyservice); run 10: 10 s (currencyservice)

## E2. Replay through the authors' released ARM code
- Rows where replayed maxR equals recorded maxR for all 11 services: **0.8%**
- Per service agreement: adservice 71%, cartservice 70%, checkoutservice 41%, currencyservice 1%, emailservice 100%, frontend 25%, paymentservice 23%, productcatalogservice 70%, recommendationservice 41%, redis-cart 100%, shippingservice 1%

## E3. Paper Fig. 8, K8s HPA, frontend demand
- Paper: 2692.6 m. Maximum possible with maxR 2, CPU limit 200 % of request, threshold 20 %: 2000 m.
- The same figure's frontend Overutilization 147.2 % implies about 1500 m. Lab (5 runs): 1578.6 m.

## E4. How ARM splits quota: authors vs lab original vs lab C4 (20/11)
Script `prosmarthpa/arm_behaviour.py`, output `e4_arm_behaviour.txt`. maxR from the authors' .pkl (10 runs), lab
Smart HPA original (5 runs at 0.67 user/s, 1 run at 2 user/s), lab C4 = ARM waits 120 s (9 runs at 2 user/s).
- **Authors:** in every run ARM moves exactly **one** replica of quota at t = 10-15 s (emailservice 2 -> 1, frontend
  2 -> 3; run 3: currency 2 -> 3), then only that one replica moves back and forth between frontend and currency
  (18-46 times per run). The other 9 services never leave maxR 2. Peak maxR 3.
- **Lab original:** first move at 18-24 s (same timing as the authors), but ARM keeps moving: currencyservice reaches
  maxR 7-12, 6-8 services drop to maxR 1.
- **Lab C4:** first move at 120 s (by construction), then frontend maxR 4-5, adservice and emailservice 1, rest 2;
  about 4 moves per run, then frozen.
- Distance of the median split after 120 s to the authors (sum of |maxR difference| over 11 services):
  lab original 16 (0.67/s) and 12 (2/s), **C4 3**.
- Conclusion: the authors' ARM did NOT wait; it moved quota as early as the lab original. What differs is the
  **size** of the transfer: one replica (authors) vs up to nine (lab). With only one replica moved, the authors'
  Smart HPA stays very close to K8s HPA (all maxR 2), consistent with the paper's "on par" result at 2R-20%.
  C4 ends with a split close to the authors' (distance 3) but by a different mechanism (delay, not small transfers);
  it is not the authors' algorithm.
- **Same input, published code (from `e2_replay.csv`, t > 120 s):** feeding the authors' own DR series through their
  released ARM code gives currencyservice maxR 3-7, frontend 2-6, peak maxR 5-8 and 4-7 services at maxR 1 in every
  run, i.e. large transfers like the lab original, not the one-replica moves the authors recorded. So matching the
  lab load/DR to the authors' would not make the published code behave like the authors' data: the lab behaviour
  is what the published code does, even on the authors' own inputs.

## E5. Paper Fig. 8 per service vs lab: which column does the lab miss? (20/11)
Script `prosmarthpa/fig8_per_service_check.py`, output `e5_fig8_per_service.csv`.
- **Smart HPA column: the lab original code at spawn 2 user/s (like the paper) matches it closely.** Supply:
  currency 664 vs 673 m, frontend 430 vs 485 m, email/shipping 100 vs 100 m. Underprovision: cart 606 vs 596,
  checkout 206 vs 225, frontend 1951 vs 1810, productcatalog 623 vs 630, recommendation 623 vs 605, shipping 127 vs
  113 m. So Fig. 8 SHPA has the large quota transfer to currency that the published code makes (E2, lab), not the
  one-replica moves of the .pkl (E4). Only 1 lab run at 2 user/s so far.
- **K8s HPA column is where the lab differs:** frontend Underprovision 2500 m in the paper vs 1379 m in the lab, and
  2500 m is above the physical maximum (DR <= 2 x 200 % / 20 % = 20 replicas -> (20 - 2) x 100 m = 1800 m).
- With the paper's K8s frontend at that maximum, the paper's own K8s Underprovision is <= 4390 m, so the paper's
  own Smart/K8s >= 1.138 (published 0.981), i.e. Smart HPA worse than K8s HPA, the lab's direction
  (lab Smart original 2 user/s vs K8s: 1.11).
- C4 moves away from Fig. 8 (currency supply 195 m vs 664 m in the paper).

## E6. Fixing the code where it departs from Algorithm 2 (20/11)
Script `prosmarthpa/arm_fix_replay.py`, output `e6_arm_fix_replay.csv`, `e6_replay_fixed.csv`.
Line-by-line check of `Adaptive_Resource_Manager.py` against Algorithm 2 (paper p. 6) finds two departures:
D1 (lines 24-25: code sets UmaxR = CR when CR >= maxR, paper UmaxR = maxR) and D2 (line 35: code tests
`ARM_maxR < maxR` with ARM_maxR left over from the previous service, paper tests TotalR in [1, ResidualR)).
Replaying the authors' DR series through the code with D1 and D2 changed to Algorithm 2 gives **exactly the same
result** as the published code: 0.8% of rows match, currency maxR 5.5 after 120 s, peak 8, 5 services at maxR 1,
total quota 22 (min 21, so no real leak). So an ARM that follows Algorithm 2 as written also makes large transfers
on the authors' own inputs; the one-replica behaviour in the authors' data does not follow from Algorithm 2 (with E1).
Together with E5 (lab Smart HPA column already matches Fig. 8), no fix on the Smart HPA side can produce the
paper's Smart vs K8s trend at 2R-20%.

## E7. Fig. 8 uses a different CPU Overutilization formula (20/11)
The authors' two analysis scripts disagree. Smart HPA package, `Results Analysis Script/Results_Analysis.py`:
Overutilization sample = CPU% when CPU% > threshold, else 0 (the lab's `make_run_report.py` uses this). ProSmart package,
`Results Analysis/Results_Analysis.py` line 98, the script behind Fig. 8: sample = **CPU% - threshold** when CPU% >
threshold, else 0. Table 1 ("CPU utilization exceeding a threshold") allows both readings.
Lab Knowledge Base recomputed with the ProSmart formula (sum over 11 services, mean over runs):
| | K8s HPA | Smart HPA | Smart/K8s |
|---|---|---|---|
| Paper Fig. 8 | 383.3 | 381.6 | 0.996 |
| Lab, CPU% formula (K8s 7 runs, Smart original 2 user/s 1 run) | 513.8 | 526.4 | 1.025 |
| Lab, ProSmart formula, same runs | 373.6 | 371.3 | 0.994 |
Other lab ratios with the ProSmart formula: C4/K8s 0.728; at 0.67 user/s ProSmart/K8s 0.783 (paper 0.743),
ProSmart/Smart 0.518 (paper 0.746). Supply, Overprovision and Underprovision use the same formula in both scripts
(request mapping per service checked: correct), so Underprovision still differs (lab Smart/K8s 1.11, paper 0.981).
Fig. 8 is drawn by `Results Visualization/Results_Plots.py` from `Compiled Results.xlsx` (not in the package) with a
hard-coded list of sheet names, so the per-service labels in Fig. 8 cannot be checked.
Limit: Smart HPA original at 2 user/s has 1 run so far.

## Limits
- The .pkl data is the authors' 5 s resampling (linear interpolation); E1 counts whole replicas only.
- E2 models current replicas from DR and maxR (not stored in the .pkl).
- None of this shows which code the authors ran; it shows their published data cannot come from the published code.
## E8–E15 (20/11, phiên tìm nguyên nhân Smart/K8s và rà ProSmart)
Bảng tổng hợp có trạng thái: `plan.md` mục 13b. Script chấm Fig. 8: `prosmarthpa/fig8_compare.py`.

- **E8 (cột demand của ProSmart):** dữ liệu demand của tác giả (`.pkl`, trung bình 10 lần) đi cùng số user, không nhìn
  trước 25 s: frontend 1,5 / 4,1 / 13,0 ở giây 10 / 30 / 100 (20 / 60 / 200 user), trong khi `ceil(model(t+25))` là
  6 / 8 / 15. → DR đo được, giống cột D của lab. Giữ cột D.
- **E9 (.pkl = cột ProSHPA Fig. 8):** tính từ `.pkl` (DR của model demand, maxR của model capacity): Underprovision /
  Overprovision 3708 / 44 so với Fig. 8 ProSHPA 3729 / 59; theo service: frontend 1392 / 1402, currency 860 / 850,
  payment 111 / 111, cart 320 / 321. Fig. 9 ở 25 s cũng bằng các số này.
- **E10 (image v0.8.0):** gói Smart HPA ghim v0.8.0, gói ProSmart và lab v0.8.1 (hai manifest chỉ khác tag image).
  K8s 2 user/s: payment CPU 37,6% → 11,1%, thời gian > 20% 95% → 6%, Supply 194 → 139m (`2R-20-v080`, 2 lần),
  100m với làm ấm (`2R-20-v080w5`); bài 101m.
- **E11 (adservice khởi động lạnh):** pod mới vọt 26–62% CPU ở giây 25–55 → K8s HPA lên 2 pod và kẹt (2 × 11%); pod ấm
  (`2R-20-pilot2s` run2) giữ 1 pod ~15%. Làm ấm 50 user / 120 s chưa đủ (vọt 46% ở giây 80); 200 user / 300 s: adservice
  200m (bài 206m), K8s Supply 2140–2148 (bài 2053).
- **E12 (600 user):** Fig. 4 của bài (ảnh): 600 user @ 2/s, ~235 req/s. Lab 200 user: 86 req/s (0,43 req/s/user, bài
  0,39) nhưng CPU từng service ≈ bài. 600 user ở lab: recommendationservice trượt liveness 1 s (exit 137, CrashLoopBackOff),
  controller crash `int('')` → hủy (`2R-20-v080w5u600`).
- **E13 (làm tròn PROPHET):** model capacity của tác giả với `ceil`: tổng maxR 23,5 (quota 22), currency 3 (ghi nhận
  2,1), email 1,48 (1,0); với `round`: tổng 22, từng service khớp. Model demand với `ceil`: adservice / email / redis
  vượt maxR 39 / 94 / 17% số điểm (ghi nhận 2 / 7 / 0%); với `round`: 0 / 0 / 0%. Bài (Algorithm 3, 4) không nói làm tròn.
- **E14 (Fig. 8 trộn phiên bản):** payment DR trong dữ liệu ProSmart của tác giả 3,10; lab K8s v0.8.1 4,40, ProSmart lab
  v0.8.1 4,03, K8s v0.8.0 1,01; cột SHPA/KHPA của bài payment 100–101m, Underprovision ≈ 0 (nhẹ, như v0.8.0).
- **E15 (ARM dùng số CPU cũ):** Smart gốc v0.8.0 làm ấm, cả 5 lần productcatalog/recommendation bị hạ maxR 1:
  run1 giây 30,5 (6% đo từ giây 17; 2 s sau 32–34%), run2 recom giây 28,7 (6%; sau 36%), run3 giây 32,8 (prodcat 1% đo
  từ giây 0, 2,4 s sau 50%; recom 9%, sau 26%). metrics-server v0.9.0 `--metric-resolution=15s`; pod sẵn sàng ≤ 15 s
  (bài ~15 s); `pilot2s-d5` (kubectl delay 0,9 s, vòng 4,8 s) vẫn mất quota ở giây 32,3 (13%, 6%). Mô phỏng window
  (`prosmarthpa/sim_window.py`): với model tác giả, window 5–30 s đổi chỉ số < 0,2%.

## E16. L11: Supply K8s dư so với bài: adservice và redis-cart, không phải email (20/11)

- **Theo service** (`scripts/l11/l11_persvc.py`, K8s `2R-20-v080w5` run1–3, lab TB / bài KHPA): adservice 258 / 206
  (200, 285, 289), redis-cart 107 / 70 (134, 118, 70), email 121 / 138 (164, 100, 100), shipping 193 / 186, cart 387 /
  387, các service khác ±3. Tổng lab 2135, bài 2056.
- **Pod thứ 2 không nhận tải** (`scripts/l11/l11_pods.py`, `pod_metrics.csv` mọi tag): redis 2–3m, email 2–5m, cart
  2–4m trong mọi lần chạy; pod đầu giữ hết tải (client giữ kết nối cố định: gRPC HTTP/2, cartservice 1 kết nối Redis).
  CPU TB chia đôi nên HPA không hạ lại: 1 mẫu vượt ngưỡng là kẹt 2 pod hết run. Bài cũng có (cart 387 = 2 pod).
- **Redis 1 pod sát ngưỡng ở lab** (`scripts/l11/l11_services.py`): CPU TB 14–20% trên 32 lần chạy; 9/16 run K8s
  vượt ngưỡng; bài KHPA 0/10 (Supply 70,01, Overprovision 69,4 → DR = 2 chỉ 0,8% mẫu, Overutilization 0,02).
- **Image khác** (`E16_redis_images.txt`): lab `redis:alpine` không ghim = Redis 8.10.2 (09/2026) + 4 module tự nạp;
  helm chart gói Smart HPA ghim 7.0.11 (06/2023), gói ProSmart ghim 7.2.3 (12/2023), không module.
- **Chưa chứng minh** Redis 8 + module là lý do redis nặng hơn: cần A/B `scripts/redis_ab.sh` (chưa chạy).
- **adservice:** run2/run3 lên 2 pod ở giây 129–132 (một mẫu 24%), làm ấm (E11) chỉ đỡ 1/3 run.

## E17 (22/11): ProSmart `v081w5pro` so với dữ liệu tác giả
- maxR theo service của lab ProSmart = dữ liệu capacity của tác giả (ad/cart/checkout/payment/prodcat/recom/redis/shipping 2,0; currency 2,0/2,1; email 1,02/1,01; frontend 2,98/2,89). Supply lab 2502 / bài 2480.
- Demand (DR, cột D) lab / tác giả: adservice 1,20/2,00, frontend 20,49/16,78, checkout 3,84/2,73, payment 4,19/3,07, prodcat 8,09/6,62, recom 7,50/6,50, cart 3,41/3,57, currency 10,60/10,69, email 1,58/1,28, shipping 1,99/1,87.
- Overprov ProSmart lab 210,6 / tác giả 44,3 / bài 59,3; adservice lab 162,2 / tác giả 4,6. Underprov lab 4545,6 / tác giả 3707,9 / bài 3728,8.
- Dữ liệu: `results/2R-20-v081w5pro/pro_vs_authors_pkl_7runs.csv`, `pro_persvc_7runs.csv`. Script: `scripts/pro_persvc.py`; `scripts/pro_vs_authors_pkl.py` (đọc `history` của model tác giả, có bảng theo thời gian); `scripts/pro_rawcap.py`: PmaxR thô của model capacity tác giả = cột E lab ở mọi dòng.
- locustfile lab = `Benchmark Application/Load Test Script/Load Test Script.py` của cả hai gói (md5 3a31575c).

## E18 (22/11): L12/L13 tách ramp / số user / CPU mỗi request
Script `scripts/l12_l13_cpu_per_req.py`, CSV `results/2R-20-v081w5pro/l12_l13_cpu_per_req.csv`. Mức ổn định t ≥ 300 s.
- Ramp (lab 2/s so với tác giả): phần chênh DR nằm ở t < 300 s ≤ 17% (frontend 0,65 / 3,73), checkout 0,02, payment −0,27.
- Số user: cùng locustfile → cùng tỉ lệ request; lab 82,5 req/s, bài ~235 req/s → đổi số user nhân đều mọi service.
- CPU mỗi request lab ÷ tác giả: ad 1,78, redis 2,34, currency 2,70, cart 2,73, recom 3,11, frontend 3,33, prodcat 3,41, shipping 3,41, email 3,47, checkout 4,17, payment 4,47.
- adservice lab 37,6m / 2 pod → DR 1; DR 2 cần ≥ 44m; tác giả 40–80m.
- Cùng lab, cùng 200 user/83 req/s: bộ 0,67/s so với 2/s prodcat 133/159m, recom 109/146m.
- Giới hạn: millicore tác giả suy từ DR (khoảng ±1 bậc); req/s tác giả từ Fig. 4.
