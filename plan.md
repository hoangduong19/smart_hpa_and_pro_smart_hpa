# Bài tập lớn: Tái hiện và cải tiến Smart HPA trên cluster k3s

> **Bài báo:** H. Ahmad, C. Treude, M. Wagner, C. Szabo, *Towards resource-efficient reactive and proactive auto-scaling for microservice architectures*, Journal of Systems and Software 225 (2025) 112390. DOI: 10.1016/j.jss.2025.112390
> **Người thực hiện:** Nhóm. **Hoàng Quốc Dương** phụ trách phần demo (hạ tầng, chạy hệ thống, chạy thí nghiệm, demo khi bảo vệ)
> **Cập nhật lần cuối:** 20/11/2026
> **Trạng thái tổng:** 🟡 Giai đoạn 1–6 xong (20/20 lần chạy hợp lệ: 2R-20% 5 cặp, 5R-50% 5 cặp; lần 4–5 của 2R-20% chạy 12/10). Giai đoạn 6b ProSmart HPA xong (5/5 lần 2R-20% hợp lệ, 08/10 và 12/10). Giai đoạn 7: C1 xong phần phân tích (12/10); C3 xong (13/10 và 15/10: 5R-50% 5 lần + 3 lần đối chứng, 2R-20% 3 lần); C2 xong (19/10: 5R-50% tải đột biến, 3 cặp). 19/11: tìm ra vì sao 2R-20% lệch bài (ARM chia quota ở giây 20–45 rồi đóng băng; bằng chứng số liệu tác giả trái Algorithm 2), dựng VM `exp-runner` chạy thí nghiệm, thử cải tiến C4 "ARM chờ ổn định" (1/2 lần đạt 7/7). Tiếp theo: chạy lại C4 với pod mới, rồi báo cáo 20/11: Smart/K8s chuyển sang image v0.8.0 + làm ấm pod (K8s khớp Fig. 8, trừ ô frontend Underprovision của bài); đã đủ 8 cặp `v080w5` (Smart/K8s: Supply +9,9%, Overutilization +23,5%, Overprovision −83,5%, Underprovision +20,7%; bằng chứng L4/L5 ở Nhật ký 20/11 (10)–(14)); ProSmart đã sửa làm tròn, chờ chạy trên v0.8.1. Các quyết định đã chốt: xem Nhật ký 20/11 (5).
> **Yêu cầu của giảng viên:** chạy nhiều lần, mỗi lần ra con số khác nhau cũng được, nhưng **xu hướng phải giống nhau ở mọi lần chạy**.

---

## Mục lục

1. [Mục tiêu và phạm vi](#1-mục-tiêu-và-phạm-vi)
2. [Tóm tắt bài báo (những gì cần nắm)](#2-tóm-tắt-bài-báo-những-gì-cần-nắm)
3. [Môi trường và kiến trúc demo](#3-môi-trường-và-kiến-trúc-demo)
4. [Trạng thái hiện tại](#4-trạng-thái-hiện-tại)
5. [Kế hoạch chi tiết theo giai đoạn](#5-kế-hoạch-chi-tiết-theo-giai-đoạn)
6. [Thiết kế thí nghiệm](#6-thiết-kế-thí-nghiệm)
7. [Phần cải tiến](#7-phần-cải-tiến)
8. [Checklist đảm bảo kết quả hợp lệ](#8-checklist-đảm-bảo-kết-quả-hợp-lệ)
9. [Xử lý sự cố thường gặp](#9-xử-lý-sự-cố-thường-gặp)
10. [Rủi ro và phương án dự phòng](#10-rủi-ro-và-phương-án-dự-phòng)
11. [Khung báo cáo và slide](#11-khung-báo-cáo-và-slide)
12. [Lịch trình đề xuất](#12-lịch-trình-đề-xuất)
13. [Câu hỏi còn mở](#13-câu-hỏi-còn-mở)
    - 13b. [Các điểm lệch so với bài báo và bằng chứng](#13b-các-điểm-lệch-so-với-bài-báo-và-bằng-chứng-2r-20-fig-89-cập-nhật-2011)
14. [Nhật ký tiến độ](#14-nhật-ký-tiến-độ)
15. [Tài liệu tham khảo](#15-tài-liệu-tham-khảo)

---

## 1. Mục tiêu và phạm vi

### Mục tiêu
1. **Tái hiện** thí nghiệm so sánh Smart HPA và Kubernetes HPA ở quy mô nhỏ (cluster 3 node trên laptop). Mục tiêu là **thấy lại xu hướng** của bài báo, không cần trùng con số.
2. **Cải tiến**: phân tích điểm yếu của bài báo, đề xuất và thử nghiệm 2 cải tiến.
3. **Demo** trực tiếp khi bảo vệ (10–15 phút).

### Trong phạm vi
- Smart HPA (bản reactive), so với K8s HPA mặc định.
- Kịch bản **5R-50%** (chính) và **2R-20%** (phụ).
- **ProSmart HPA** ở 2R-20%, window 25s (tái hiện mục 5.3 bài báo). Model PROPHET train lại từ Knowledge Base các lần chạy Smart HPA 2R-20% của nhóm. Chi tiết ở [mục 2, phần ProSmart HPA](#prosmart-hpa) và Giai đoạn 6b. *(08/10: trước đây để ngoài phạm vi, nay đưa vào.)*
- 2 cải tiến (xem [mục 7](#7-phần-cải-tiến)).

### Ngoài phạm vi
- ProSmart HPA với 6 prediction window (5–30s) như bài báo: chỉ chạy window 25s.
- 9 kịch bản đầy đủ, 10 lần chạy mỗi kịch bản như bài báo (~60 giờ chạy).

### Tiêu chí "thành công"

> ⭐ **Tiêu chí quan trọng nhất (yêu cầu của giảng viên):** xu hướng phải **nhất quán ở từng lần chạy**, không chỉ ở giá trị trung bình. Ví dụ: ở 5R-50%, *lần nào* Smart HPA cũng phải có Underprovision thấp hơn K8s HPA. Con số mỗi lần khác nhau là bình thường. Cách kiểm tra xem ở [mục 6, phần "Phân tích tính nhất quán"](#phân-tích-tính-nhất-quán-giữa-các-lần-chạy).

| Tiêu chí | Cách kiểm tra |
|---|---|
| Xu hướng giống nhau ở **mọi lần chạy** | Bảng nhất quán theo từng lần (mục 6) |
| Ở 5R-50%, Smart HPA cho `frontend` vượt 5 replica, K8s HPA thì không | `kubectl get deploy` trong lúc chạy, log knowledge base |
| Smart HPA có CPU Underprovision và Overutilization thấp hơn K8s HPA | Script phân tích |
| Smart HPA có Supply CPU cao hơn K8s HPA | Script phân tích |
| Ở 2R-20%, hai bên gần ngang nhau | Script phân tích |
| Không có pod `Pending` trong mọi lần chạy | `kubectl get pods` |

### Phân công nhóm (đề xuất)

> ⚠️ Chưa biết số thành viên. Bảng dưới chia theo **vai trò**; nếu nhóm 3 người thì gộp vai trò C và D.

| Vai trò | Người | Việc chính | Đầu ra giao cho nhóm |
|---|---|---|---|
| **A. Demo & hạ tầng** | **Dương** | Dựng cluster, deploy Online Boutique, chạy Smart HPA và K8s HPA, chạy toàn bộ thí nghiệm, demo khi bảo vệ, quay video demo dự phòng | Thư mục `results/` (CSV mọi lần chạy), nhật ký chạy, ảnh chụp màn hình, video |
| **B. Code & cải tiến** | *(thành viên 2)* | Đọc và sửa code Smart HPA cho hợp k3s, viết script ghi metric, script chạy tự động; code cải tiến C3 (ưu tiên) và kiểu tải C2 (`LoadTestShape`) | Code đã test, đưa cho Dương chạy trên cluster |
| **C. Phân tích dữ liệu** | *(thành viên 3)* | Tính 7 chỉ số + latency (C1), bảng từng lần chạy, phân tích nhất quán, kiểm định thống kê, vẽ biểu đồ | Bảng số liệu + biểu đồ cho báo cáo và slide |
| **D. Báo cáo & slide** | *(thành viên 4)* | Tóm tắt bài báo, cơ sở lý thuyết, phân tích điểm yếu (W1–W8), ghép báo cáo, làm slide | Báo cáo hoàn chỉnh, slide |

**Phụ thuộc giữa các vai trò:**
```
B (sửa code Smart HPA) ──► A (chạy thử trên cluster) ──► A (chạy 16 lần) ──► C (phân tích) ──► D (báo cáo, slide)
B (code cải tiến) ───────► A (chạy thí nghiệm cải tiến) ─────────────────► C ──► D
D (lý thuyết, tóm tắt bài báo) có thể làm song song ngay từ đầu
```

**Những thứ Dương cần chuẩn bị riêng cho phần demo:**
- [ ] Cluster chạy ổn định, có checklist khởi động lại nhanh (bật 3 VM → kiểm tra node → kiểm tra pod) để dùng ngay trước giờ bảo vệ.
- [ ] Script demo rút gọn (5–7 phút, 5R-50%).
- [ ] Màn hình chia 3 ô đã sắp sẵn: `kubectl get deploy`, `kubectl top pods`, Locust.
- [ ] Video demo quay trước, phòng khi chạy trực tiếp lỗi.
- [ ] Tập trả lời câu hỏi kỹ thuật: vì sao dùng k3s, vì sao 3 node, vì sao 200 users, khác paper ở đâu, chuyển quota hoạt động thế nào.
- [ ] Tập demo ít nhất 2 lần trước buổi bảo vệ, trên đúng laptop sẽ dùng.

**Quy ước chung cho nhóm:**
- Một repo Git chung (code, script, file kế hoạch này, kết quả).
- Đặt tên file kết quả theo [cấu trúc thư mục ở mục 6](#cấu-trúc-thư-mục-kết-quả).
- Nhật ký tiến độ (mục 14) ai làm gì cũng ghi vào.

---

## 2. Tóm tắt bài báo (những gì cần nắm)

### Vấn đề
- K8s HPA scale mỗi microservice **độc lập** và bị chặn bởi **maxR** (số replica tối đa) riêng của từng service.
- Khi tải cao: service bận bị kẹt ở maxR (thiếu tài nguyên), trong khi service rảnh vẫn giữ quota thừa.
- Pod khởi động hoặc tắt mất vài chục giây, nên HPA phản ứng chậm.

### Giải pháp: Smart HPA
Kiến trúc **phân cấp 2 tầng** dựa trên vòng điều khiển **MAPE-K** (Monitor, Analyze, Plan, Execute + Knowledge Base):

| Thành phần | Vai trò | Ghi chú |
|---|---|---|
| **Microservice Manager** (1 cái cho mỗi service, phi tập trung) | Tính số replica mong muốn `DR = ceil(CR × CMV/TMV)` (Algorithm 1), quyết định scale up/down | Giống công thức của K8s HPA |
| **Microservice Capacity Analyzer** | Kiểm tra `DR ≤ maxR` cho mọi service | Nếu có service nào `DR > maxR` thì gọi tầng trên |
| **Application Resource Manager** (tập trung, chỉ bật khi thiếu tài nguyên) | Algorithm 2: tìm service thừa và thiếu, **chuyển quota maxR** từ service thừa sang service thiếu | Ưu tiên service thiếu nhiều nhất trước |

**Điểm mấu chốt:** tổng quota của cả ứng dụng không đổi. Smart HPA chỉ **phân phối lại** quota giữa các service.

### ProSmart HPA
- Mở rộng MAPE-K thành **MAPE-KI** (thêm thành phần Intelligence).
- Dùng PROPHET dự đoán trước nhu cầu replica (PDR) và capacity (PmaxR), để bù độ trễ khởi động pod.
- Prediction window tốt nhất là **25s** (nằm giữa thời gian startup 15s và termination 30s).
- 22 model PROPHET (11 demand + 11 capacity) được train trên **dữ liệu Knowledge Base của các lần chạy Smart HPA** (mục 5.1 bài báo). Nhóm train lại từ chính dữ liệu Smart HPA 2R-20% nhóm tự chạy.
- **Algorithm 3** (Microservice Manager): `PDR = PROPHET(RM, RMT, CR)`; so `PDR` với `CR` để ra scale up/down/no scale; nếu `PDR > maxR` thì gọi ARM.
- **Algorithm 4** (Application Resource Manager): `PmaxR = PROPHET(PDR, maxR, CR)` cho cả 11 service; cân bằng phần quota thêm và bớt (lấy từ service thừa nhiều nhất, cấp cho service thiếu nhiều nhất) để tổng quota không đổi; rồi ra `ResDR`, `ResSD` cho từng service.

#### Replication package của ProSmart không khớp với bài báo (kiểm tra 08/10)
Đã mở 22 file `.pkl` bằng prophet 1.1.5 (tác giả train bằng 1.1.4, pickle tạo ngày 17–18/04/2024):

| Nguồn | Nội dung | Kiểu model |
|---|---|---|
| Bài báo, mục 5.1 | "with additional regressors such as CPU usage, CPU threshold value, and current allocated resources"; tune bằng cross-validation | Có regressor |
| Code `Analyse` trong repo | Chuẩn bị regressor `current_replicas`, `cpu_percentage`, `target_cpu` rồi đưa vào `predict()` | Có regressor |
| 22 file `.pkl` trong repo | `extra_regressors = []`, tham số mặc định (25 changepoint, prior 0.05), không seasonality | **Chỉ theo thời gian** |

- Dữ liệu train trong `.pkl`: 1810 dòng = **10 lần chạy × 181 điểm** (lưới 5s, 0–900s), giá trị nội suy tuyến tính; `ds = 1970-01-01 + giây kể từ lúc bắt đầu tải`. Demand học cột `Desired Replicas`, capacity học cột `Max. Replicas`.
- Capacity trong dữ liệu của tác giả gần như không đổi (maxR 2–3, `emailservice` về 1), tức là ARM của tác giả ở 2R-20% gần như không chuyển quota. Dữ liệu của nhóm thì `currencyservice` lên 12, `productcatalogservice` còn 1.
- Code ProSmart trong repo **không chạy được**, có ít nhất 7 lỗi: `Analyse` khai báo 7 tham số nhưng gọi với 6; `pd.concat` nhận số thay vì Series; ARM gọi `predict(future)` thay vì `futures` (thiếu regressor); tên `productcatalogueservice` sai; mảng `np.zeros` chứa chuỗi `scaling_action`; import vòng giữa ARM và các manager; `Main.py` gọi hàm `redis` không tồn tại và lặp `for _ in pool` sai.
- **Cách nhóm làm:** viết lại controller theo Algorithm 3–4, dùng lại phần Monitor của code Smart HPA đã chạy ổn; train model theo mô tả trong bài (có regressor, gọi là `reg`). Kiểu chỉ theo thời gian như `.pkl` gọi là `time`.

#### Kiểm tra model trước khi chạy cluster (08/10, `prosmarthpa\train_prophet.py --evaluate`)
Train trên 2 lần chạy Smart HPA 2R-20%, thử trên lần còn lại (đổi vai đủ 3 lượt). Ở mỗi thời điểm `t ≥ 10s`, đoán giá trị lúc `t + 25s`, làm tròn lên như code gốc. Mốc so sánh: đoán "25 giây sau giống bây giờ". Sai số trung bình tính bằng số replica:

| Model | `time` | `reg` | Đoán "giống bây giờ" |
|---|---|---|---|
| Demand | 1.06 | 0.84 | **0.47** |
| Capacity | 0.55 | 0.38 | **0.04** |

Tách theo pha (demand, `reg`): lúc tải tăng (phút 0–5) Prophet đoán thiếu **15%** số lần so với 33% của cách "giống bây giờ"; lúc ổn định (phút 5–15) là 7% so với 16%. Prophet đoán dư trung bình 0.2–0.6 replica.

**Kỳ vọng:** ProSmart scale sớm hơn nên có thể giảm Underprovision lúc tải tăng, nhưng có thể tăng Overprovision. Ở 2R-20%, quota 2 replica chặn gần như suốt 15 phút nên lợi ích có thể nhỏ. Kết quả thật phải chờ chạy cluster.

### Cấu trúc thí nghiệm của bài báo (đã đối chiếu PDF, file `Demo\Towards-resource-efficient-...pdf`)
> Bài 2025 là bản mở rộng của bài ICSA 2024 (Smart HPA). Cái mới của bài 2025 là ProSmart HPA (mục 1, danh sách 7 điểm khác biệt (i)–(vii)). **Baseline của cả bài là Kubernetes HPA** (mục 5).

| Phần | So sánh | Kịch bản | Số lần chạy | Kết quả |
|---|---|---|---|---|
| **5.2** (phần lớn bài) | Smart HPA vs **K8s HPA** | Cả 9 kịch bản | 10 lần/kịch bản | Smart HPA tốt hơn ở mọi kịch bản; rõ nhất 5R-50%, gần ngang ở 2R-20% |
| **5.3** | ProSmart HPA vs Smart HPA vs K8s HPA | **Chỉ 2R-20%**, thử 6 prediction window (5–30s) | 10 lần/window | ProSmart tốt nhất ở window 25s (bảng dưới) |

**ProSmart HPA (window 25s, 2R-20%), mức cải thiện:**

| Chỉ số | so với Smart HPA | so với K8s HPA |
|---|---|---|
| CPU Overutilization | giảm 25.40% | giảm 25.73% |
| CPU Underprovision | giảm 25.34% | giảm 26.73% |
| CPU Overprovision | giảm 28.24% | giảm 86.43% |
| Supply CPU | tăng 2.17% | tăng 20.75% |

Lý do chọn 2R-20% cho ProSmart: đó là kịch bản Smart HPA yếu nhất (gần ngang K8s HPA) vì không còn quota thừa để chuyển.

### Chỉ số đánh giá (Table 1 của bài báo)
| Chỉ số | Ý nghĩa | Tốt khi |
|---|---|---|
| Supply CPU (milliCPU) | CPU của các replica đang được cấp | Cao |
| CPU Overutilization (%) | CPU % (so với request) lúc vượt ngưỡng, lúc dưới ngưỡng tính 0; mức ứng dụng = tổng 11 service nên có thể > 100% | Thấp |
| Overutilization Time (phút) | Thời gian có ít nhất 1 service vượt ngưỡng | Thấp |
| CPU Overprovision (milliCPU) | CPU thừa = capacity − demand | Thấp |
| Overprovision Time (phút) | Thời gian không service nào thiếu CPU | Cao |
| CPU Underprovision (milliCPU) | CPU thiếu = demand − capacity | Thấp |
| Underprovision Time (phút) | Thời gian có ít nhất 1 service thiếu CPU | Thấp |

### Kết quả chính cần đối chiếu
> ✅ Đã đối chiếu: các con số dưới đây nằm đúng trong bài 2025, mục 5.2 và Fig. 6–7.

| Kịch bản | Kết quả trong bài báo (Smart HPA so với K8s HPA) |
|---|---|
| **5R-50%** (tốt nhất) | Underprovision: **0** so với 934.04m (13.46 phút). Overutilization: 19.30% so với 98.06% (giảm **5.08x**). Overutilization Time giảm **1.98x** |
| **2R-20%** (khó nhất) | Gần ngang nhau: chỉ cải thiện ~1.004x đến 1.01x |
| **10R-20%** | Supply CPU cao hơn **1.83x** (11188.76m so với 6110.41m) |

Trong 5R-50% (Fig. 7): khoảng phút 1.5, `frontend` vượt capacity 500m và nhận quota từ `adservice`. Khoảng phút 2, `currency` nhận quota từ `cart`. Sau đó lấy tiếp từ `email` và `shipping`.

---

## 3. Môi trường và kiến trúc demo

### Máy host
| Thông số | Giá trị |
|---|---|
| Máy | Dell Precision 7670 |
| CPU | Intel i9-12950HX (16 nhân / 24 luồng) |
| RAM | 32GB |
| GPU | NVIDIA RTX A2000 8GB (không dùng) |
| OS | Windows |
| Ảo hóa | VMware Workstation Pro |

### Cluster
| Máy ảo | Hostname | IP | vCPU | RAM | Ổ đĩa | Vai trò |
|---|---|---|---|---|---|---|
| VM1 | `k3s-master` | `192.168.161.10` | 4 | 4GB | 30GB | Control plane + chạy pod |
| VM2 | `k3s-worker1` | `192.168.161.11` | 4 | 4GB | 30GB | Worker |
| VM3 | `k3s-worker2` | `192.168.161.12` | 4 | 4GB | 30GB | Worker |

Tổng: 12 vCPU, 12GB RAM cho cluster. Máy host còn khoảng 20GB RAM cho Windows, Python và Locust.

| Thông số mạng | Giá trị |
|---|---|
| Kiểu mạng VMware | NAT (VMnet8) |
| Dải mạng | `192.168.161.0/24` |
| Gateway | `192.168.161.2` |
| DNS | `192.168.161.2`, `8.8.8.8` |
| IP của Windows trên VMnet8 | `192.168.161.1` |
| Card mạng trong VM | `ens33` |
| File cấu hình IP | `/etc/netplan/01-static.yaml` (quyền 600, đọc phải dùng `sudo`) |
| OS trong VM | Ubuntu Server 24.04.5 LTS |
| User | `duong` |

> 📝 Mạng hiện tại **chặn ping ra internet**, nhưng HTTPS vẫn hoạt động. Để kiểm tra internet, dùng `curl -I https://google.com` thay cho `ping`.

### Sơ đồ
```
┌──────────────────────────── Windows (host) ─────────────────────────────┐
│                                                                          │
│   PowerShell / Python                                                    │
│   ├─ kubectl (điều khiển cluster)                                        │
│   ├─ Smart HPA (Main.py + Microservice Managers + App Resource Manager)  │
│   ├─ Script ghi metric (cho lần chạy K8s HPA)                            │
│   └─ Locust (tạo tải → http://192.168.161.10)                            │
│                         │  VMnet8 NAT 192.168.161.0/24                   │
│   ┌─────────────────────┼──────────────────────────────────────────┐    │
│   │  k3s-master .10     │   k3s-worker1 .11     k3s-worker2 .12    │    │
│   │  ├ API server :6443 │   ├ pod ...           ├ pod ...          │    │
│   │  ├ metrics-server   │   └ ...               └ ...              │    │
│   │  ├ ServiceLB :80    │                                          │    │
│   │  └ pod ...          │   Online Boutique: 11 microservice       │    │
│   └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
```

### Khác biệt so với bài báo (dùng cho báo cáo)
| Yếu tố | Bài báo | Bài tập này |
|---|---|---|
| Hạ tầng | 10 node AWS EC2 t3.medium | 3 VM VMware trên 1 laptop |
| Kubernetes | Amazon EKS, K8s 1.24 | k3s `v1.36.5+k3s1` (bản phân phối đạt chứng nhận CNCF, K8s 1.36) |
| Nơi chạy autoscaler + Locust | Máy local, kết nối AWS qua internet | Chính máy host, mạng nội bộ |
| Tải | 600 users, spawn 2/s | ~200 users, ramp trong 5 phút |
| Kịch bản | 9 (2R/5R/10R × 20/50/80%) | 2 (5R-50%, 2R-20%) |
| Số lần chạy | 10 lần/kịch bản | 5 lần/kịch bản |
| ProSmart HPA | Có, 6 window, model train trên 10 lần chạy | Window 25s, model train lại trên 3 lần chạy Smart HPA 2R-20% của nhóm, có regressor theo mô tả trong bài |

---

## 4. Trạng thái hiện tại

Chú thích: ✅ xong · ⚠️ cần xác nhận · ⬜ chưa làm

### Giai đoạn 1: Hạ tầng
| # | Việc | Trạng thái | Ghi chú |
|---|---|---|---|
| 1.1 | Kiểm tra máy host, cài VMware Workstation Pro | ✅ | |
| 1.2 | Tải ISO Ubuntu Server 24.04.5 | ✅ | `D:\ubuntu-24.04.5-live-server-amd64.iso` |
| 1.3 | Tạo VM `k3s-master` (4 vCPU, 30GB, NAT) | ✅ | Ổ không dùng LVM |
| 1.4 | Cài Ubuntu, tạo user `duong`, cài OpenSSH | ✅ | Không cài snap nào |
| 1.5 | SSH từ Windows vào VM | ✅ | |
| 1.6 | `apt upgrade`, tắt swap, tắt cloud-init network | ✅ | Đã chạy trên master trước khi clone, nên 2 worker cũng có |
| 1.7 | Đặt IP tĩnh `.10` cho master, thêm `/etc/hosts` | ✅ | Gateway OK, HTTPS OK |
| 1.8 | Clone full 2 worker | ✅ | |
| 1.9 | Worker1: hostname, machine-id, IP `.11` | ✅ | |
| 1.10 | Worker2: hostname, machine-id, IP `.12` | ✅ | |
| 1.11 | Chốt RAM cho 3 VM | ✅ | **4GB mỗi máy**. Nếu chưa chỉnh trong VMware thì chỉnh khi máy đang tắt |
| 1.12 | Bật cả 3 máy, kiểm tra cấu hình, ping lẫn nhau | ✅ | Hostname, IP, swap, cloud-init, machine-id, đồng bộ giờ, internet đều đạt |

### Giai đoạn 2: Cài k3s
| # | Việc | Trạng thái | Ghi chú |
|---|---|---|---|
| 2.1 | Cài k3s server trên master | ✅ | `v1.36.5+k3s1`, `--disable traefik`. Phải tải binary có retry rồi cài với `INSTALL_K3S_SKIP_DOWNLOAD=true` (xem mục 5.2, mục 9) |
| 2.2 | Join worker1, worker2 | ✅ | 3 node `Ready`, cùng phiên bản, containerd 2.3.4 |
| 2.3 | Pod hệ thống `kube-system` Running, `kubectl top nodes` có số liệu | ✅ | `coredns`, `local-path-provisioner`, `metrics-server` Running; không có traefik. Lúc rảnh: master 43m CPU / 701Mi RAM, worker ~10m / ~320Mi |
| 2.4 | Copy kubeconfig về Windows, chạy `kubectl` từ Windows | ✅ | `$HOME\.kube\config`, server `https://192.168.161.10:6443`. File chứa khóa admin, **không** đưa vào Git |

### Các giai đoạn sau
| Giai đoạn | Trạng thái |
|---|---|
| 2. Cài k3s, cấu hình kubectl trên Windows | ✅ |
| 3. Deploy Online Boutique | ✅ 11/11 Running, web `http://192.168.161.10` OK, checkout OK, `kubectl top pods` có số liệu, resource khớp bài báo |
| 4. Chạy được Smart HPA | ✅ Code đã sửa ở `Demo\smarthpa\`, chạy trên Windows (Python 3.11, venv `D:\smarthpa-venv`) |
| 5. Chuẩn bị baseline K8s HPA + công cụ ghi metric | ✅ `k8shpa_observer.py`, `cluster_recorder.py`, `run_experiment.ps1`, `run_batch.ps1`, `check_run.py`, `make_run_report.py`, `make_comparison.py` |
| 6. Chạy thí nghiệm tái hiện | ✅ 20/20 lần hợp lệ (5R-50% 5 cặp, xong 07/10; 2R-20% 5 cặp, xong 12/10), xem [ma trận chạy](#ma-trận-chạy-xen-kẽ-để-giảm-sai-lệch-theo-thời-gian) |
| 6b. ProSmart HPA (2R-20%, window 25s) | ✅ 5/5 lần hợp lệ (08/10 và 12/10), xem [Giai đoạn 6b](#56b-giai-đoạn-6b-prosmart-hpa-2r-20-window-25s) |
| 7. Cải tiến | 🟡 C1 xong phần phân tích (12/10); C3 xong, 11/11 lần hợp lệ kể cả 3 lần đối chứng ở 5R-50% (13/10 và 15/10); C2 xong, 6/6 lần 5R-50% tải đột biến hợp lệ (19/10). **Tiếp theo: báo cáo** |
| 8. Phân tích, báo cáo, slide | ⬜ |

---

## 5. Kế hoạch chi tiết theo giai đoạn

### 5.1. Giai đoạn 1: Hoàn tất hạ tầng

**a) Đặt RAM 4GB:** tắt cả 3 VM, vào *VM → Settings → Memory*, đặt **4096MB** cho mỗi máy. Mức này đủ cho cả 2R và 5R.

**b) Bật cả 3 VM.** Trên **mỗi máy**, kiểm tra nhanh (bước chuẩn bị đã làm trước khi clone nên phần này chỉ để chắc chắn):
```bash
hostname                                       # đúng tên máy
ip -4 a show ens33 | grep inet                 # đúng IP
free -h                                        # dòng Swap phải là 0B
cat /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg   # phải có network: {config: disabled}
curl -sI https://google.com | head -1          # HTTP/2 301 → có internet
```

Nếu thiếu bước nào, chạy bù:
```bash
sudo apt update && sudo apt upgrade -y
sudo swapoff -a && sudo sed -i '/swap/ s/^/#/' /etc/fstab
echo 'network: {config: disabled}' | sudo tee /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
```

**c) Trên master, kiểm tra kết nối nội bộ:**
```bash
ping -c 2 k3s-worker1
ping -c 2 k3s-worker2
```

**Hoàn thành khi:** 3 máy đúng hostname và IP, swap tắt, có internet, ping thấy nhau.

---

### 5.2. Giai đoạn 2: Cài k3s

**a) Master** (`ssh duong@192.168.161.10`):
```bash
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik --write-kubeconfig-mode 644" sh -
kubectl get nodes                                  # k3s-master Ready
sudo cat /var/lib/rancher/k3s/server/node-token    # copy token
```
- `--disable traefik`: bắt buộc. Traefik chiếm cổng 80, sẽ xung đột với frontend của Online Boutique.
- `--write-kubeconfig-mode 644`: cho phép chạy `kubectl` không cần `sudo` và copy file cấu hình dễ hơn.

> ⚠️ **Mạng hiện tại hay cắt kết nối HTTPS** (`curl: (35) Connection reset`), nên lệnh cài một dòng ở trên bị lỗi `Download failed`. Cách đã dùng thành công: tải trước có retry, kiểm tra checksum, rồi cài từ file có sẵn.
> ```bash
> # Trên mỗi máy (hoặc tải ở 1 máy rồi scp sang máy khác qua mạng nội bộ, nhanh hơn nhiều)
> cd /tmp
> R="--retry 10 --retry-all-errors --retry-delay 3 --speed-limit 1000 --speed-time 30"
> curl -fL $R -o k3s-install.sh https://get.k3s.io
> curl -fL $R -C - -o k3s https://github.com/k3s-io/k3s/releases/download/v1.36.5%2Bk3s1/k3s
> curl -fL $R -o sha256sum-amd64.txt https://github.com/k3s-io/k3s/releases/download/v1.36.5%2Bk3s1/sha256sum-amd64.txt
> grep ' k3s$' sha256sum-amd64.txt | sha256sum -c        # phải in "k3s: OK"
> sudo install -m 755 /tmp/k3s /usr/local/bin/k3s
>
> # Master
> INSTALL_K3S_SKIP_DOWNLOAD=true INSTALL_K3S_EXEC="--disable traefik --write-kubeconfig-mode 644" sh /tmp/k3s-install.sh
> # Worker
> INSTALL_K3S_SKIP_DOWNLOAD=true K3S_URL=https://192.168.161.10:6443 K3S_TOKEN=<TOKEN> sh /tmp/k3s-install.sh
> ```
> Token **không** ghi vào file này hay repo Git; cần thì lấy lại bằng `sudo cat /var/lib/rancher/k3s/server/node-token`.

**b) Mỗi worker** (`ssh duong@192.168.161.11`, rồi `.12`):
```bash
curl -sfL https://get.k3s.io | K3S_URL=https://192.168.161.10:6443 K3S_TOKEN=<TOKEN> sh -
```

**c) Kiểm tra trên master:**
```bash
kubectl get nodes -o wide     # 3 node Ready
kubectl top nodes             # có số CPU/RAM (metrics-server có sẵn trong k3s, đợi ~1 phút)
```

**d) Điều khiển cluster từ Windows** (PowerShell):
```powershell
winget install Kubernetes.kubectl          # nếu chưa có kubectl
mkdir $HOME\.kube -Force
scp duong@192.168.161.10:/etc/rancher/k3s/k3s.yaml $HOME\.kube\config
notepad $HOME\.kube\config                 # sửa 127.0.0.1 thành 192.168.161.10
kubectl get nodes                          # 3 node Ready
```

**Hoàn thành khi:** `kubectl get nodes` và `kubectl top nodes` chạy được từ Windows.

---

### 5.3. Giai đoạn 3: Deploy Online Boutique

```powershell
# Repo đã clone vào: D:\Nam 4 - HK1\Các Chuyên đề\Demo\Pro_Smart_HPA\ProSmart_HPA
cd "D:\Nam 4 - HK1\Các Chuyên đề\Demo\Pro_Smart_HPA\ProSmart_HPA\Benchmark Application"
kubectl apply -f .\release\kubernetes-manifests.yaml
kubectl get pods -o wide -w              # đợi tất cả Running (mạng chập chờn: có thể 20–40 phút)
```
> ✅ **Đã đọc manifest** `release\kubernetes-manifests.yaml`: 11 Deployment + Service, image `gcr.io/google-samples/microservices-demo/*:v0.8.1` (redis dùng `redis:alpine` từ Docker Hub). **Không có `loadgenerator`** nên không cần xóa. `frontend-external` kiểu `LoadBalancer` cổng 80 → k3s ServiceLB mở cổng 80 trên các node. Resource khớp bài báo:
>
> | Service | CPU request / limit | RAM request / limit |
> |---|---|---|
> | emailservice, checkoutservice, frontend, paymentservice, productcatalogservice, currencyservice, shippingservice | 100m / 200m | 64Mi / 128Mi |
> | recommendationservice | 100m / 200m | 220Mi / 450Mi |
> | cartservice | 200m / 300m | 64Mi / 128Mi |
> | adservice | 200m / 300m | 180Mi / 300Mi |
> | redis-cart | 70m / 125m | 200Mi / 256Mi |
>
> Tổng RAM request ở 1 replica mỗi service ≈ 1.1GB, dư sức cho 3 node × 4GB.

**Kiểm tra:**
```powershell
kubectl get svc frontend-external        # EXTERNAL-IP là IP các node
kubectl top pods
```
Mở trình duyệt vào **http://192.168.161.10**, thấy trang shop, thử thêm hàng vào giỏ và checkout.

**Ghi lại resource request/limit** (đưa vào báo cáo, phải khớp bài báo: phần lớn service 100m/200m, `cart` và `adservice` 200m/300m, `redis` 70m/125m):
```powershell
kubectl get deploy -o custom-columns="NAME:.metadata.name,CPU_REQ:.spec.template.spec.containers[0].resources.requests.cpu,CPU_LIM:.spec.template.spec.containers[0].resources.limits.cpu,MEM_REQ:.spec.template.spec.containers[0].resources.requests.memory"
```

**Hoàn thành khi:** 11 deployment Running, web truy cập được, `kubectl top pods` có số liệu.

---

### 5.4. Giai đoạn 4: Chạy được Smart HPA

**a) Lấy code.** Repo GitHub ở trên là của **ProSmart HPA**. Code **Smart HPA** nằm trong replication package trên figshare: https://doi.org/10.6084/m9.figshare.25393408. Tải cả hai về, ưu tiên dùng code Smart HPA.

**b) Môi trường Python trên Windows:**
```powershell
py -3.11 -m venv D:\smarthpa-venv
D:\smarthpa-venv\Scripts\Activate.ps1
pip install kubernetes pandas numpy locust
# + các thư viện khác thấy ở đầu các file .py
```

**c) Đọc và sửa code.** Danh sách cần kiểm tra khi mở code:
> Code Smart HPA đã tải về `Demo\HussainAhmad05-Smart_HPA-196c63d\` (commit `196c63d`). Đã đọc 02/10:
- [x] Cách đọc metric: `kubectl top pods -l app=<svc>` qua `subprocess`; replica lấy bằng `kubectl get deployment -o jsonpath`. Label `app=` khớp cluster.
- [x] Cách scale: `kubectl scale deployment <svc> --replicas=N` (`os.system`).
- [x] Không có lệnh `aws` nào. Chỉ cần kubeconfig trỏ vào k3s.
- [x] Đường dẫn: tương đối `./Knowledge Base/<svc>.xlsx` → phải chạy từ trong thư mục code.
- [x] maxR / TMV: **hard-code ở dòng 70–72 của cả 11 file manager** (`target_cpu = 50`, `max_replica = 5`, `min_replica = 1`). Đổi kịch bản phải sửa 22 dòng → gom về 1 file config.
- [x] Chu kỳ lặp: **không có sleep**, mỗi vòng = thời gian 11 manager chạy xong; tổng 900s hard-code trong `Microservice Capacity Analyzer.py`.
- [x] Có `if __name__ == '__main__':`. Nhưng mỗi vòng tạo **Pool 11 process mới**; trên Windows (spawn) mỗi process import lại numpy/matplotlib → vòng lặp chậm hơn trên Linux, cần đo.
- [x] Tên deployment khớp (`redis-cart` nằm trong file `rediscart.py`).
- [x] Knowledge base: file `.xlsx` rỗng, cột A thời gian, B CPU%, C current replicas, D desired replicas, E maxR, F scaling action. `Results_Analysis.py` đọc đúng các cột này từ `./Test/<N> Replicas + <T>%/Run <k>/<svc>.xlsx`.
- [ ] **Lỗi phải sửa mới chạy được:** (1) code import `Adaptive_Resource_Manager` nhưng file tên có dấu cách `Adaptive Resource Manager.py`; (2) manager nằm trong thư mục con, phải để chung thư mục với Capacity Analyzer; (3) máy chưa cài Python (chỉ có alias Microsoft Store); thư viện cần: `openpyxl numpy psutil matplotlib locust`.
- [ ] **Ghi chú cho báo cáo (giữ nguyên để tái hiện đúng):** `Adaptive Resource Manager.py:101` so sánh `ARM_maxR` còn sót từ service trước thay vì `possible_RR` → có thể trả quota cho service thừa ít hơn mức có thể (**đã đối chiếu: lệch so với Algorithm 2 dòng 35 trong bài**, bài ghi điều kiện `TotalR ∈ [1, ResidualR)`); bài mô tả tải "600 user, mỗi 2 giây thêm 1 user, đủ 600 sau 5 phút" nhưng 300s / 2s chỉ được 150 user, còn Locust `spawn rate 2` nghĩa là 2 user/giây (đủ 600 sau 5 phút) → mô tả trong bài tự mâu thuẫn; Smart HPA không có stabilization window khi scale down (K8s HPA có 300s); hàm `Monitor` lặp chờ đến khi `kubectl top` thấy đủ số pod → lúc pod đang khởi động/tắt thì cả vòng bị chặn.
- [ ] **Cho Giai đoạn 5:** package không có logger cho K8s HPA → tự viết logger ghi cùng định dạng xlsx. Cột D phải là desired **chưa bị chặn bởi maxR** (`ceil(CR × CPU%/TMV)`), nếu lấy `desiredReplicas` của HPA thì Underprovision của K8s HPA luôn = 0.

**d) Chạy thử ngắn** (5R-50%, Locust 5 phút, 100 users):
```powershell
# Cửa sổ 1
python Main.py
# Cửa sổ 2
locust -f Load_Test_Script.py --host=http://192.168.161.10 --headless -u 100 -r 1 -t 5m
# Cửa sổ 3: quan sát
while ($true) { cls; kubectl get deploy; kubectl top pods; sleep 3 }
```

**Hoàn thành khi:** thấy Smart HPA scale được, và khi `frontend` cần hơn 5 replica thì Application Resource Manager chuyển quota (log hoặc knowledge base có ghi lại).

---

### 5.5. Giai đoạn 5: Baseline K8s HPA và công cụ ghi metric

**a) Bật K8s HPA** (ví dụ 5R-50%):
```powershell
kubectl get deploy -o name | ForEach-Object { kubectl autoscale $_ --cpu=50% --min=1 --max=5 }
kubectl get hpa
```
Với 2R-20%: `--cpu=20% --max=2`.
> ⚠️ kubectl 1.36 đã bỏ `--cpu-percent`, phải dùng `--cpu=50%`. **Bắt buộc có dấu `%`**, thiếu thì `50` bị hiểu là 50 milliCPU. Script `smarthpa\run_experiment.ps1` đã làm sẵn bước này.

**b) Script ghi metric.** Smart HPA tự ghi dữ liệu vào knowledge base, còn **K8s HPA thì không**. Cần một script độc lập, chạy trong **cả hai loại lần chạy** để dữ liệu cùng định dạng. Mỗi 15 giây ghi vào CSV:

| Cột | Nguồn |
|---|---|
| `timestamp` | |
| `deployment` | |
| `replicas` (CR) | `kubectl get deploy` |
| `cpu_usage_m` (tổng mọi pod) | `kubectl top pods` / Metrics API |
| `cpu_request_m` (1 replica) | spec của deployment |
| `max_replicas` (maxR) | HPA spec (K8s) / knowledge base (Smart HPA) |
| `pending_pods` | `kubectl get pods` |

Từ đó tính được **demand**, **capacity** (= maxR × request), **supply** (= replicas × request), rồi suy ra các chỉ số ở Table 1.
> 💬 Có thể nhờ Claude viết script này (`metrics_recorder.py`) khi tới giai đoạn này.

**c) Script reset** giữa các lần chạy:
```powershell
kubectl delete hpa --all
kubectl get deploy -o name | ForEach-Object { kubectl scale $_ --replicas=1 }
Start-Sleep -Seconds 300     # đợi CPU nguội và pod cũ tắt hẳn
kubectl get pods             # không còn pod Terminating
```

---

### 5.6. Giai đoạn 6: Chạy thí nghiệm tái hiện

Xem [mục 6](#6-thiết-kế-thí-nghiệm). ✅ Đã có script tự động trong `Demo\smarthpa\`:
- `run_experiment.ps1`: một lần chạy (reset → cooldown 300s → autoscaler + recorder + Locust 15 phút → dọn dẹp → `check_run.py` → báo cáo + so sánh). Lần hỏng bị chuyển sang `_failed_run<N>_...` và trả exit 1.
- `run_batch.ps1`: chạy theo cặp (K8s HPA rồi Smart HPA), **bỏ qua lần đã có kết quả**, chờ cluster kết nối lại được rồi **tự chạy lại tối đa 3 lần** nếu hỏng.
- `check_run.py`: loại lần chạy bị mất kết nối (cửa sổ 10s gần như không có request khi đủ user, lỗi > 1%, hoặc recorder mất > 1 phút số liệu).

```powershell
cd "D:\Nam 4 - HK1\Các Chuyên đề\Demo\smarthpa"
.\run_batch.ps1 -Pairs "5R-50%:4","5R-50%:5"      # phần còn thiếu, R14 tự được bỏ qua
```

### 5.6b. Giai đoạn 6b: ProSmart HPA (2R-20%, window 25s)

| # | Việc | Trạng thái | Ghi chú |
|---|---|---|---|
| 6b.1 | venv riêng `D:\prosmart-venv` (Python 3.11, prophet 1.1.5, cmdstanpy < 1.3, numpy < 2, pandas 2.x) | ✅ | Tách khỏi `smarthpa-venv` (pandas 3.0) |
| 6b.2 | Kiểm tra 22 model `.pkl` của tác giả | ✅ | Không có regressor, khác bài báo (mục 2) |
| 6b.3 | `prosmarthpa\train_prophet.py`: train 22 model từ `results\2R-20\smarthpa\run1..3\knowledge_base`, kiểm tra chéo `--evaluate` | ✅ | Kết quả ở mục 2. Chọn `--mode reg` |
| 6b.4 | Viết controller ProSmart theo Algorithm 3–4: `prosmarthpa\prosmart_hpa.py`; `run_experiment.ps1 -Autoscaler prosmarthpa` | ✅ | Monitor là hàm `Monitor()` của Smart HPA (không sửa). KB cột D vẫn là DR phản ứng như Smart/K8s HPA để chỉ số so sánh được; PDR ở cột G, `ResDR` ở H, thời điểm dự đoán ở I, ARM bật/tắt ở J |
| 6b.5 | Chạy thử `run0` (100 users, 3 phút), rồi 5 lần chính thức (200 users, 15 phút) | ✅ | `run0` 08/10 14:49; run1–3 08/10 14:53–15:56; run4–5 12/10 (xen kẽ với K8s HPA và Smart HPA), cả 5 hợp lệ. **Chạy đúng Algorithm 4**, kể cả khi vượt quota (W8) |
| 6b.6 | So sánh ProSmart vs Smart HPA vs K8s HPA bằng `make_comparison.py` | ✅ | `results\2R-20\comparison\comparison.md`. Kết quả ở mục "Kết quả ProSmart" ngay dưới |

#### Kết quả ProSmart HPA (2R-20%, 5 lần: run1–3 ngày 08/10, run4–5 ngày 12/10)

| Chỉ số | K8s HPA | Smart HPA | ProSmart HPA | ProSmart so với Smart (nhóm) | Bài báo |
|---|---|---|---|---|---|
| Supply CPU (m) | 2,141 | 2,409 | **3,065** | +27.2%, nhất quán 5/5 | +2.17% |
| CPU Overutilization (%) | 464 | 664 | **408** | −38.6%, 5/5 | −25.40% |
| CPU Overprovision (m) | 391 | 78 | 73 | −6.1%, 4/5 | −28.24% |
| CPU Underprovision (m) | 3,728 | 5,188 | 6,111 | **+17.8% (kém hơn)**, 0/5 | −25.34% |
| Overutilization Time (phút) | 14.58 | 14.69 | 14.69 | ngang, 3/5 | – |
| Underprovision Time (phút) | 14.58 | 14.39 | 14.53 | kém hơn chút, 0/5 | – |
| p95 response time (ms) | 1,340 | 1,064 | **798** | −25.0%, 5/5 | không đo |

- **Khớp bài báo:** Overutilization giảm, nhất quán 5/5 lần (cả so với Smart HPA lẫn K8s HPA). Latency p95 tốt nhất trong 3 autoscaler.
- **Lệch bài báo:** Underprovision tăng thay vì giảm; Overprovision gần như không giảm.
- **Run4–5 chạy xen kẽ cùng ngày với Smart HPA và K8s HPA** (12/10) cho cùng kết luận như run1–3 (ProSmart chạy 08/10, hai autoscaler kia chạy 05/10), nên chênh lệch không phải do khác ngày chạy.
- **Lý do chính là W8:** supply ProSmart 2,953–3,114m, vượt quota 2,540m (+16–23%) ở cả 5 lần. Phần CPU thêm này giúp Overutilization và latency. Đồng thời ARM hạ capacity (cột E) của các service bị lấy quota nhưng không scale chúng xuống, nên chỉ số Underprovision (= demand − capacity) tăng dù pod vẫn chạy.
- Cần nói rõ trong báo cáo: ProSmart tốt hơn ở một số chỉ số nhưng không phải trong cùng mức tài nguyên, nên tuyên bố "resource-efficient" không được xác nhận trên cluster của nhóm.

```powershell
cd "D:\Nam 4 - HK1\Các Chuyên đề\Demo\prosmarthpa"
D:\prosmart-venv\Scripts\python.exe train_prophet.py --evaluate              # kiểm tra chéo, ghi train_evaluation.csv
D:\prosmart-venv\Scripts\python.exe train_prophet.py --mode reg --runs 1 2 3 # train và lưu 22 model vào models\
```

### 5.7. Giai đoạn 7: Cải tiến

Xem [mục 7](#7-phần-cải-tiến).

### 5.8. Giai đoạn 8: Phân tích, báo cáo, slide

- Dùng (hoặc chỉnh lại) script trong `Results Analysis` của repo để tính chỉ số.
- Vẽ biểu đồ theo kiểu Fig. 6 (cột so sánh) và Fig. 7 (đường demand/capacity theo thời gian).
- Viết báo cáo theo [mục 11](#11-khung-báo-cáo-và-slide).

---

## 6. Thiết kế thí nghiệm

### Biến
| Loại | Biến | Giá trị |
|---|---|---|
| Biến độc lập | Autoscaler | K8s HPA, Smart HPA; thêm ProSmart HPA (chỉ ở 2R-20%) |
| Biến độc lập | Kịch bản (maxR, threshold) | 5R-50%, 2R-20% |
| Cố định | Ứng dụng | Online Boutique, request/limit mặc định |
| Cố định | Tải | Locust, 200 users, ramp 5 phút, giữ 10 phút, tổng 15 phút |
| Cố định | Cluster | 3 node, cấu hình như mục 3 |
| Biến phụ thuộc | 7 chỉ số ở Table 1 (+ latency nếu làm cải tiến C1) | |

### Cấu hình Locust
Bài báo dùng 600 users, spawn 2 user/s, nghĩa là ramp đúng 5 phút. Với 200 users, để giữ ramp 5 phút thì spawn rate = 200/300 ≈ **0.67 user/s**:
```powershell
locust -f Load_Test_Script.py --host=http://192.168.161.10 `
  --headless -u 200 -r 0.67 -t 15m `
  --csv=results\<kịch_bản>\<autoscaler>\run<N>\locust --csv-full-history
```
> Trước khi chạy chính thức, thử 1 lần với 200 users. Nếu CPU laptop vượt khoảng 80% hoặc Locust cảnh báo CPU cao, giảm xuống 150.

### Ma trận chạy (xen kẽ để giảm sai lệch theo thời gian)
| Mã | Kịch bản | Autoscaler | Lần | Trạng thái |
|---|---|---|---|---|
| R01 | 5R-50% | K8s HPA | 1 | ✅ 02/10 14:44 |
| R02 | 5R-50% | Smart HPA | 1 | ✅ 02/10 15:05 |
| R03 | 5R-50% | K8s HPA | 2 | ✅ 02/10 15:32 |
| R04 | 5R-50% | Smart HPA | 2 | ✅ 02/10 15:53 |
| R05 | 5R-50% | K8s HPA | 3 | ✅ 02/10 16:13 |
| R06 | 5R-50% | Smart HPA | 3 | ✅ 05/10 08:44 (chạy lại; lần 02/10 lỗi kubectl) |
| R07 | 2R-20% | K8s HPA | 1 | ✅ 05/10 09:05 |
| R08 | 2R-20% | Smart HPA | 1 | ✅ 05/10 09:26 |
| R09 | 2R-20% | K8s HPA | 2 | ✅ 05/10 09:46 |
| R10 | 2R-20% | Smart HPA | 2 | ✅ 05/10 10:07 |
| R11 | 2R-20% | K8s HPA | 3 | ✅ 05/10 10:28 |
| R12 | 2R-20% | Smart HPA | 3 | ✅ 05/10 10:49 |

**Khuyến nghị thêm 4 lần cho kịch bản chính** (vì giảng viên chấm tính nhất quán giữa các lần chạy, 5 lần thuyết phục hơn 3 lần):

| Mã | Kịch bản | Autoscaler | Lần | Trạng thái |
|---|---|---|---|---|
| R13 | 5R-50% | K8s HPA | 4 | ✅ 07/10 13:50 (05/10 hỏng 3 lần do mất kết nối) |
| R14 | 5R-50% | Smart HPA | 4 | ✅ 05/10 11:59 |
| R15 | 5R-50% | K8s HPA | 5 | ✅ 07/10 14:11 (05/10 hỏng khi tạo HPA) |
| R16 | 5R-50% | Smart HPA | 5 | ✅ 07/10 14:32 |

**Thêm 2 cặp cho 2R-20% (12/10), chạy xen kẽ cùng ProSmart HPA:**

| Mã | Kịch bản | Autoscaler | Lần | Trạng thái |
|---|---|---|---|---|
| R17 | 2R-20% | K8s HPA | 4 | ✅ 12/10 10:29 |
| R18 | 2R-20% | Smart HPA | 4 | ✅ 12/10 10:50 |
| R19 | 2R-20% | K8s HPA | 5 | ✅ 12/10 11:32 |
| R20 | 2R-20% | Smart HPA | 5 | ✅ 12/10 11:53 |

**ProSmart HPA (Giai đoạn 6b):**

| Mã | Kịch bản | Autoscaler | Lần | Trạng thái |
|---|---|---|---|---|
| P1 | 2R-20% | ProSmart HPA | 1 | ✅ 08/10 14:58 |
| P2 | 2R-20% | ProSmart HPA | 2 | ✅ 08/10 15:19 |
| P3 | 2R-20% | ProSmart HPA | 3 | ✅ 08/10 15:40 |
| P4 | 2R-20% | ProSmart HPA | 4 | ✅ 12/10 11:11 (sau R18) |
| P5 | 2R-20% | ProSmart HPA | 5 | ✅ 12/10 12:14 (sau R20) |

### Kết quả (5R-50%: 07/10/2026; 2R-20%: 12/10/2026; từ `results\<kịch bản>\comparison\comparison.md`)

**5R-50%** (5 cặp, đủ): Smart HPA tốt hơn ở **6/7 chỉ số Table 1 trong 5/5 lần**; Overutilization Time 4/5 (run 5: 14,52 so với 14,41 phút, gần như ngang) → nhất quán, khớp xu hướng bài báo.

| Chỉ số (TB ± ĐLC) | K8s HPA (n=5) | Smart HPA (n=5) | Smart tốt hơn |
|---|---|---|---|
| CPU Underprovision | 916 ± 399m | 389 ± 124m | 5/5 |
| Underprovision Time | 13,17 ± 0,74 phút | 10,25 ± 0,42 phút | 5/5 |
| CPU Overprovision | 3588 ± 95m | 781 ± 52m | 5/5 |
| Overprovision Time | 1,81 ± 0,73 phút | 4,73 ± 0,42 phút | 5/5 |
| Supply CPU | 2718 ± 139m | 3898 ± 196m | 5/5 |
| CPU Overutilization | 213 ± 41% | 160 ± 28% | 5/5 |
| Overutilization Time | 14,32 ± 0,28 phút | 14,23 ± 0,30 phút | 4/5 |
| p95 latency | 1090 ± 356 ms | 928 ± 129 ms | 3/5 |

Hình theo bố cục bài báo (`make_paper_figs.py`): `results\fig6_services.png` (Fig. 6, cột chồng theo microservice, cả 2 kịch bản) và `results\<kịch bản>\comparison\fig7_timeline.png` (Fig. 7, lưới 2×2, trung bình các lần chạy).

Khác bài: Smart HPA vẫn còn Underprovision (bài = 0) vì tổng quota toàn ứng dụng đã dùng hết; Overutilization Time gần ngang.

**2R-20%** (5 cặp; run4–5 thêm ngày 12/10): **không "gần ngang nhau" như bài**. Smart HPA tốt hơn ở Overprovision (78 so với 391m) và p95 latency (1064 so với 1340 ms) trong 5/5 lần; ở Supply CPU (2409 so với 2141m), Overprovision Time và Underprovision Time trong 4/5 lần; nhưng **kém hơn ở CPU Underprovision (5188 so với 3728m) và CPU Overutilization (664 so với 464%) trong 5/5 lần**. Nguyên nhân: ARM chia quota tham lam lúc tải tăng rồi giữ nguyên (W4, xem nhật ký 08/10). Giữ nguyên và phân tích trong báo cáo.

Lần ngược hướng duy nhất là **run 4** (cặp đầu tiên sau khi bật VM ngày 12/10), ở 3 chỉ số trên: K8s HPA scale `adservice` lên 2 replica (supply 2309m, các lần khác 2077–2150m), còn ARM của Smart HPA chia quota khác các lần khác (`currency` 664m, các lần khác 855–1129m; supply 2259m, các lần khác 2434–2451m). Không có pod `Unschedulable`, 0 ping mất, nên giữ lại và nêu trong báo cáo.

Mỗi lần khoảng 20 phút (15 phút tải + 5 phút reset). 12 lần mất khoảng **4 giờ**, 16 lần khoảng **5,5 giờ**. Nên chạy qua đêm bằng script tự động.

### Phân tích tính nhất quán giữa các lần chạy

Đây là phần **trả lời trực tiếp yêu cầu của giảng viên**. Ngoài bảng trung bình, báo cáo cần có:

**1. Bảng kết quả từng lần chạy** (ví dụ cho 5R-50%, chỉ số CPU Underprovision):

| Lần | K8s HPA | Smart HPA | Chênh lệch | Smart HPA tốt hơn? |
|---|---|---|---|---|
| 1 | … m | … m | … | ✅ / ❌ |
| 2 | … m | … m | … | ✅ / ❌ |
| 3 | … m | … m | … | ✅ / ❌ |
| … | | | | |
| **TB ± ĐLC** | … ± … | … ± … | | |

Lập một bảng như vậy cho mỗi chỉ số chính: Underprovision, Overutilization, Supply CPU, Overutilization Time, cộng p95 latency nếu làm C1.

**2. Bảng tổng hợp tính nhất quán:**

| Chỉ số | Hướng mong đợi | Số lần đúng hướng | Kết luận |
|---|---|---|---|
| CPU Underprovision | Smart HPA thấp hơn | …/5 | Nhất quán nếu 5/5 |
| CPU Overutilization | Smart HPA thấp hơn | …/5 | |
| Supply CPU | Smart HPA cao hơn | …/5 | |
| Overutilization Time | Smart HPA thấp hơn | …/5 | |

**3. Biểu đồ:**
- **Biểu đồ cột có thanh sai số** (trung bình ± độ lệch chuẩn) cho từng chỉ số.
- **Biểu đồ điểm theo từng lần chạy**: trục x là lần chạy, mỗi lần 2 điểm (K8s HPA, Smart HPA) nối bằng một đoạn thẳng. Nhìn vào là thấy ngay lần nào cũng cùng một hướng. Đây là biểu đồ minh họa yêu cầu của giảng viên rõ nhất.
- **Biểu đồ demand/capacity theo thời gian** (kiểu Fig. 7) của 2–3 lần chạy đặt cạnh nhau, cho thấy hành vi lặp lại (frontend nhận quota vào khoảng cùng một thời điểm).

**4. Chỉ số bổ sung:**
- **Hệ số biến thiên** CV = ĐLC / TB cho mỗi chỉ số. CV nhỏ (dưới khoảng 15%) nghĩa là kết quả ổn định giữa các lần.
- **Kiểm định Mann-Whitney U** (hoặc Wilcoxon cho cặp) giữa hai autoscaler. Với 5 lần chạy mỗi bên, p < 0.05 là khác biệt có ý nghĩa thống kê.

**5. Kịch bản 2R-20%:** theo bài báo, xu hướng mong đợi là **gần ngang nhau**. Kết quả của nhóm thì không ngang (xem phần Kết quả ở trên): Smart HPA tốt hơn ở một số chỉ số và kém hơn ở CPU Underprovision, CPU Overutilization. Vì vậy "nhất quán" ở đây nghĩa là **với từng chỉ số, hướng chênh lệch giống nhau ở mọi lần chạy**, kể cả các chỉ số Smart HPA kém hơn (5/5 lần). Cần giải thích rõ điều này và chỗ lệch so với bài báo trong báo cáo.

**Nếu có lần chạy đi ngược xu hướng:** không xóa đi. Kiểm tra nhật ký xem lần đó có bất thường không (pod Pending, laptop bận, mạng chập chờn). Nếu tìm ra nguyên nhân thì ghi rõ và chạy bù một lần. Nếu không tìm ra thì giữ lại và thảo luận trong báo cáo, cách xử lý trung thực này được đánh giá cao hơn.

### Quy trình một lần chạy
1. Reset (mục 5.5c), kiểm tra mọi deployment = 1 replica, không pod Pending/Terminating.
2. Bật autoscaler (K8s HPA: `kubectl autoscale`; Smart HPA: `python Main.py`).
3. Bật script ghi metric.
4. Chạy Locust 15 phút.
5. Dừng autoscaler và script ghi metric.
6. Kiểm tra file kết quả đủ, ghi chú bất thường vào [nhật ký](#14-nhật-ký-tiến-độ).

### Cấu trúc thư mục kết quả
```
results/
├── 5R-50/
│   ├── k8shpa/
│   │   ├── run1/  locust_stats.csv, locust_stats_history.csv, locust_failures.csv, cluster_metrics.csv
│   │   ├── run2/
│   │   └── run3/
│   └── smarthpa/
│       ├── run1/  ... + knowledge_base.*
│       ├── run2/
│       └── run3/
└── 2R-20/
    └── ...
```

---

## 7. Phần cải tiến

### Điểm yếu của bài báo (dùng cho phần phân tích trong báo cáo)
| # | Điểm yếu | Bằng chứng trong bài |
|---|---|---|
| W1 | Không đo chỉ số phía người dùng (latency, lỗi, vi phạm SLA) | Chỉ có các chỉ số CPU ở Table 1. Mục 6 tự nhận là hướng tương lai |
| W2 | Chỉ thử một kiểu tải (tăng dần rồi giữ cao) | Mục 7 (Threats to validity) thừa nhận chưa thử tải bursty |
| W3 | Baseline có thể chưa công bằng: K8s HPA bị chặn maxR riêng, còn Smart HPA dùng chung "quỹ" quota | Algorithm 2 |
| W4 | Chia quota tham lam theo mức thiếu, không xét độ quan trọng của service | Algorithm 2, dòng 17 (sort giảm dần theo lượng thiếu) |
| W5 | Tuyên bố "giảm communication overhead" nhưng không đo | Mục 1, mục 3.2 |
| W6 | Chỉ báo cáo trung bình, không có độ lệch chuẩn hay kiểm định thống kê | Mục 5.2 |
| W7 | Replication package của ProSmart không tái hiện được trực tiếp: 22 model `.pkl` không có regressor như mô tả ở mục 5.1, code không chạy được (ít nhất 7 lỗi) | Mở `.pkl` thấy `extra_regressors = []`; danh sách lỗi ở mục 2, phần ProSmart HPA. *Đây là điểm yếu về tính tái hiện, dùng cho phần phân tích, không phải cải tiến* |
| W8 | ProSmart có thể dùng **vượt tổng quota**: Algorithm 4 dòng 19–20 (`ResSD = No Scale, ResDR = CR`) giữ nguyên replica của service bị ARM hạ capacity xuống dưới số replica hiện tại, trong khi phần quota đó đã cấp cho service khác | Cả 5 lần chạy 2R-20%: supply 2,953–3,114m so với quota 2R là 2,540m (+16–23%); lần chạy thử `run0` (08/10) cũng vậy (3,070m). Tổng capacity (cột E) không lần nào vượt 2,540m, nhưng khoảng 23% số dòng Knowledge Base có capacity thấp hơn số replica đang chạy. Smart HPA không bị (supply trung bình 2,409m). Ảnh hưởng đến tính công bằng khi so sánh và đến tuyên bố "resource-efficient" |
| W9 | Code ARM của Smart HPA (replication package) **làm mất quota** ở 5R-50%: tổng capacity (Σ maxR × CPU request) giảm dần và không quay lại, trái với ý "tổng quota của ứng dụng không đổi" | Knowledge Base của cả 5 lần Smart HPA 5R-50%: tổng capacity bắt đầu 6.350m, kết thúc 3.970–4.770m (mất 25–37%). Ở 2R-20% không bị (2.540m suốt lần chạy, trừ run 4 còn 2.340m). Chưa tách được nguyên nhân chính xác: dòng 101 của `Adaptive_Resource_Manager.py` (lệch Algorithm 2, mục 5.4c) và phần quota lẻ nhỏ hơn 1 replica không trả lại được đều có thể gây ra. Phát hiện 13/10 khi làm C3. Lần chạy đối chứng 15/10 xác nhận: chỉ cần sửa W9 (không có ưu tiên), Underprovision ở 5R-50% đã giảm từ 389 xuống 10m (mục 7, C3) |

### Các cải tiến đề xuất (chọn 2)

#### C1. Đo chỉ số phía người dùng (giải quyết W1, độ khó ⭐)
- **Làm gì:** từ `locust_stats_history.csv`, lấy p50/p95/p99 latency, requests/s, failures/s theo thời gian.
- **Chỉ số mới:**
  - p95 latency trung bình trong pha tải cao (phút 5–15).
  - Tỉ lệ thời gian vi phạm SLO, ví dụ % thời gian p95 > 500ms (ngưỡng chốt sau khi chạy thử; đã chốt 1000 ms, xem kết quả bên dưới).
  - Tổng số request lỗi.
- **Giả thuyết:** Smart HPA giảm underprovision nên latency của `frontend` cũng thấp hơn.
- **Công sức:** chỉ cần thêm phần phân tích, không phải chạy thêm thí nghiệm.

##### Kết quả C1 (12/10, ✅ xong phần phân tích)

Script `smarthpa\make_user_metrics.py`, tự chạy ở cuối `run_experiment.ps1`. Đầu ra ở `results\<kịch bản>\comparison\`: `user_metrics.md`, `user_metrics.csv`, `fig_user_runs.png` (từng lần chạy), `fig_user_timeline.png` (p95 và throughput theo thời gian).

- **Cách tính:** Locust ghi mỗi giây một dòng, các cột percentile tính trên khoảng 10 giây gần nhất. Giá trị của một pha là trung bình các dòng trong pha đó. Pha tăng tải = phút 0–5, pha tải cao = phút 5–15.
- **Ngưỡng SLO chốt là p95 ≤ 1000 ms.** Ngưỡng 500 ms dự kiến ban đầu không dùng được: gần như mọi lần chạy đều vi phạm 98–100% thời gian nên không phân biệt được autoscaler nào.
- 9 chỉ số: median / p95 / p99 pha tải cao, p95 pha tăng tải, % thời gian vi phạm SLO, throughput, số request lỗi, p95 trang chủ (`GET /`), p95 checkout (`POST /cart/checkout`).
- Cột **p** là kiểm định Mann-Whitney U chính xác, hai phía (giải quyết W6). Cột này cũng đã thêm vào `comparison.md` cho 7 chỉ số Table 1. Với 5 lần mỗi bên, p nhỏ nhất có thể là 0,008 (hai nhóm không chồng nhau).

**2R-20%** (trung bình 5 lần; "x/5" là số lần tốt hơn K8s HPA):

| Chỉ số (pha tải cao) | K8s HPA | Smart HPA | ProSmart HPA |
|---|---|---|---|
| Median (ms) | 456 | 364 (5/5, p = 0,016) | 227 (5/5, p = 0,008) |
| p95 (ms) | 1.426 | 1.238 (4/5, p = 0,151) | 859 (5/5, p = 0,008) |
| % thời gian p95 > 1000 ms | 97,3 | 46,7 (5/5, p = 0,008) | 11,6 (5/5, p = 0,008) |
| Throughput (request/s) | 76,9 | 81,8 (5/5, p = 0,008) | 86,7 (5/5, p = 0,008) |
| Request lỗi (tổng 5 lần) | 0 | 44 (chỉ ở run 4) | 0 |

- Thứ tự ProSmart → Smart HPA → K8s HPA lặp lại ở cả 9 chỉ số trừ request lỗi. ProSmart tốt hơn Smart HPA 5/5 lần ở cả 8 chỉ số còn lại (p = 0,008).
- Smart HPA tốt hơn K8s HPA về phía người dùng **dù kém hơn ở CPU Underprovision và CPU Overutilization** (mục 6). Chỉ số CPU của Table 1 và trải nghiệm người dùng không đi cùng hướng ở kịch bản này, đúng điểm yếu W1.
- Lần ngược hướng của Smart HPA ở p95 là run 4, cũng là lần có 44 request lỗi 500.
- Lợi thế của ProSmart không cùng mức tài nguyên: nó dùng vượt quota 16–23% (W8).

**5R-50%** (K8s HPA so với Smart HPA, trung bình ± ĐLC):

| Chỉ số (pha tải cao) | K8s HPA | Smart HPA | Smart tốt hơn | p |
|---|---|---|---|---|
| p95 (ms) | 1.397 ± 767 | 1.085 ± 151 | 3/5 | 0,841 |
| % thời gian p95 > 1000 ms | 51,1 ± 40,3 | 30,7 ± 16,8 | 2/5 (1 lần bằng) | 0,595 |
| Throughput (request/s) | 81,4 ± 6,0 | 84,7 ± 1,0 | 3/5 | 0,421 |

- **Giả thuyết không được xác nhận ở 5R-50%:** không chỉ số phía người dùng nào nhất quán (cao nhất 3/5, mọi p ≥ 0,42), dù 6/7 chỉ số CPU nhất quán 5/5. Smart HPA chỉ ổn định hơn giữa các lần chạy (ĐLC p95 151 so với 767 ms).
- Trung bình của K8s HPA bị kéo lên bởi run 3 (p95 2.664 ms, 99 request lỗi) và run 5 (1.543 ms). Chưa tìm nguyên nhân hai lần này; cả hai đã qua `check_run.py`.

#### C2. Thử tải đột biến (giải quyết W2, độ khó ⭐⭐)
- **Làm gì:** viết lớp `LoadTestShape` trong Locust, ví dụ:
  ```python
  from locust import LoadTestShape

  class SpikeShape(LoadTestShape):
      # (thời điểm kết thúc tính bằng giây, số users, spawn rate)
      stages = [
          (180, 50, 5),    # 0–3 phút: tải nền
          (420, 250, 50),  # 3–7 phút: tăng vọt
          (600, 50, 50),   # 7–10 phút: giảm đột ngột
          (780, 250, 50),  # 10–13 phút: tăng vọt lần 2
          (900, 50, 50),   # 13–15 phút: giảm
      ]
      def tick(self):
          t = self.get_run_time()
          for end, users, rate in self.stages:
              if t < end:
                  return users, rate
          return None
  ```
- **Thí nghiệm thêm:** 5R-50% × 2 autoscaler × 3 lần = 6 lần (~2 giờ).
- **Giả thuyết cần kiểm tra:** khi tải lên xuống liên tục, Smart HPA có bị chuyển quota qua lại liên tục (flapping) không? Độ trễ khởi động pod ảnh hưởng thế nào?
- **Kết quả (19/10, 5R-50%, 3 cặp, `resultsR-50-spike\comparison`):**
  - **Tài nguyên:** Smart HPA tốt hơn 3/3 ở 6/7 chỉ số (p = 0,100, nhỏ nhất có thể với 3 vs 3): Overutilization 44,9 so với 132,6%, thời gian Overutilization 6,4 so với 12,6 phút, Underprovision 0 so với 484m, Overprovision 2.876 so với 3.840m.
  - **Người dùng:** gần như hòa, không chỉ số nào nhất quán 3/3 (p95 lúc spike 1.468 so với 1.535 ms, thời gian p95 > 1 s 73 so với 74%).
  - **Flapping (`make_flapping.py`, có):** Smart HPA đổi replica 89 lần so với 12, đảo chiều scale 43 so với 0, chuyển quota 27 lần, một service dao động tới 11 replica (K8s HPA 2–3). K8s HPA có cửa sổ ổn định 5 phút khi scale down nên không đảo chiều trong 15 phút.
  - **Request lỗi:** Smart HPA run3 có 38 lỗi, K8s HPA 0. Không phải do mạng (0 ping mất 13:55–14:00). Hai đợt, đều trùng lúc Smart HPA scale down: (1) 13:56:11, 32 lỗi `RemoteDisconnected` trong 1 giây, đúng lúc `frontend` 5 → 4 trong chuỗi đảo chiều 4→5→4→5→4 (13:55:35–13:56:20); (2) 13:59:40–41, 6 lỗi 500 ở `/cart`, `/setCurrency`, `/product`, đúng lúc thu hẹp mạnh sau spike thứ 2 (`frontend` 12 → 9 → 5, `productcatalog` 4 → 1, `currency` 8 → 6, `cart` 2 → 1 trong 30 giây). Có thể pod bị xoá khi đang xử lý request (chưa kiểm tra log pod).

#### C3. Chia quota theo độ ưu tiên (giải quyết W4, độ khó ⭐⭐⭐)
- **Làm gì:** sửa Microservice Resource Balancer (Algorithm 2):
  - Gán trọng số `w_i` theo vai trò trong luồng người dùng (dựa trên Fig. 3). Ví dụ: `frontend` = 3; `checkout`, `cart`, `productcatalog`, `currency` = 2; còn lại = 1.
  - Dòng 17: sắp xếp service thiếu theo `w_i × RequiredRes_i` thay vì chỉ `RequiredRes_i`.
  - Khi lấy quota từ service thừa: lấy từ service **trọng số thấp** trước, và để lại một khoảng dự phòng (headroom, ví dụ 1 replica) cho service trọng số cao.
- **Thí nghiệm thêm:** chạy biến thể "Smart HPA + ưu tiên" ở 5R-50% (và 2R-20%, nơi thiếu tài nguyên nặng nhất nên ưu tiên có tác dụng rõ nhất), 3 lần mỗi kịch bản.
- **Chỉ số để so:** latency của luồng chính (trang chủ, checkout), các chỉ số CPU của nhóm service quan trọng.

##### Kết quả C3 (13/10 và 15/10, 11/11 lần hợp lệ, có lần chạy đối chứng)

Code: `smarthpa\Priority_Resource_Manager.py`, bật bằng `run_experiment.ps1 -Autoscaler smarthpa-prio` (biến môi trường `SMARTHPA_ARM=priority`). ARM gốc không sửa. Kết quả ở `results\<kịch bản>\smarthpa-prio\run<N>` và `results\<kịch bản>\comparison_c3\` (K8s HPA, Smart HPA, Smart HPA + ưu tiên); thư mục `comparison` cũ không đổi.

Lần chạy đối chứng: `-Autoscaler smarthpa-flat` (`SMARTHPA_ARM=flat`), cùng code nhưng mọi trọng số = 1 và không dự phòng, nên tắt điểm 1–3 dưới đây, chỉ còn điểm 4 (sửa W9); thứ tự chia khi đó giống Algorithm 2. Kết quả ở `results\5R-50\smarthpa-flat\run1..3` và `results\5R-50\comparison_c3_control\` (Smart HPA, đối chứng, Smart HPA + ưu tiên).

Bốn điểm khác ARM gốc:
1. Service thiếu được xếp theo `trọng số × CPU còn thiếu` (trọng số như trên: `frontend` 3; `checkout`, `cart`, `productcatalog`, `currency` 2; còn lại 1).
2. Service thừa có trọng số ≥ 2 giữ lại 1 replica dự phòng, không đưa vào quỹ chung.
3. Quota còn lại trả về service trọng số cao trước.
4. Mỗi vòng chia lại từ **tổng quota của ứng dụng**, nên phần quota lẻ chưa trả được ở vòng trước được chia tiếp ở vòng sau. Điểm này sửa W9, **không thuộc ý tưởng ưu tiên**.

Kiểm tra offline: 2.000 kịch bản ngẫu nhiên × 300 vòng ở mỗi kịch bản, tổng capacity không lần nào vượt quota.

**5R-50%** (Smart HPA n=5 chạy 02–07/10; C3 n=5: run1–3 ngày 13/10, run4–5 ngày 15/10; đối chứng n=3 ngày 15/10, chạy xen kẽ với C3 run4–5 theo thứ tự đối chứng 1, C3 4, đối chứng 2, C3 5, đối chứng 3):

| Chỉ số | Smart HPA (n=5) | Đối chứng: chỉ sửa W9 (n=3) | C3: sửa W9 + ưu tiên (n=5) | C3 so với đối chứng | p (C3 vs đối chứng) |
|---|---|---|---|---|---|
| CPU Underprovision (m) | 389 ± 124 | **10 ± 7** | 12 ± 19 | ngang | 0,571 |
| Underprovision Time (phút) | 10,25 ± 0,42 | **0,88 ± 0,45** | 1,05 ± 1,39 | ngang | 0,786 |
| CPU Overutilization (%) | 160 ± 28 | 87 ± 6 | **75 ± 3** | thấp hơn: cả 5 lần C3 thấp hơn cả 3 lần đối chứng | 0,036 |
| Overutilization Time (phút) | 14,23 ± 0,30 | 11,47 ± 0,33 | **10,47 ± 0,66** | thấp hơn, có chồng lấn (11,2 so với 11,1) | 0,071 |
| Supply CPU (m) | 3.898 ± 196 | 4.307 ± 65 | 4.326 ± 437 | ngang | 0,786 |
| CPU Overprovision (m) | **781 ± 52** | 1.858 ± 67 | 1.870 ± 429 | ngang | 0,786 |
| p95 pha tải cao (ms) | 1.085 ± 151 | **653 ± 74** | 812 ± 310 | ngang (C3 run 4 bị chập mạng, xem dưới) | 0,571 |
| % thời gian p95 > 1000 ms | 30,7 ± 16,8 | **3,9 ± 2,9** | 7,3 ± 5,1 | ngang | 0,571 |
| Throughput (request/s) | 84,7 ± 1,0 | **89,0 ± 0,7** | 87,5 ± 2,6 | ngang | 0,786 |

- **C3 so với Smart HPA gốc (n=5 mỗi bên):** tốt hơn 5/5 lần ở Underprovision, Underprovision Time, Overutilization, Overutilization Time, Overprovision Time và p95 (p = 0,008; p95 0,032); kém hơn 5/5 ở CPU Overprovision; Supply CPU chỉ 3/5 (run 4–5: 3.884 và 3.913m so với 3.891 và 4.096m).
- **Phần lớn cải thiện là do sửa W9, không phải do ưu tiên.** Đối chứng đã đưa Underprovision từ 389 xuống 10m, Underprovision Time từ 10,25 xuống 0,88 phút, p95 từ 1.085 xuống 653 ms, nhất quán 3/3 (p = 0,036). Thêm ưu tiên (C3) không làm tốt hơn đối chứng ở các chỉ số này.
- Nguyên nhân: tổng capacity cuối lần chạy của Smart HPA gốc là 3.970–4.770m, của đối chứng 6.310–6.350m, của C3 6.340m (quota 6.350m). Không mất quota thì có thêm 1.600–2.400m để chia (maxR cuối lần chạy của đối chứng và C3: `frontend` 14–16, `currency` 17–23). Overprovision cao hơn cũng do vậy: capacity − demand lớn hơn.
- **Ưu tiên chỉ giảm thêm Overutilization:** từ 87% xuống 75% (−12 điểm %), Overutilization Time từ 11,47 xuống 10,47 phút. Phía người dùng không tốt hơn đối chứng: median và p95 checkout của C3 còn hơi cao hơn (p = 0,25).
- **Không lệch theo ngày ở các chỉ số Table 1:** C3 run 4–5 (15/10) cho Overutilization 77% và 72%, Underprovision 1m và 0m; run 1–3 (13/10) là 71–77% và 1–43m.
- **Kết luận cho báo cáo:** ở 5R-50%, đóng góp chính của C3 là phát hiện và sửa W9. Smart HPA sau khi sửa đạt Underprovision gần 0, đúng con số bài báo công bố (0m) mà code gốc trong replication package không đạt được. Quy tắc ưu tiên chỉ đóng góp phần nhỏ (Overutilization).

**2R-20%** (C3 n=3 chạy 13/10; Smart HPA n=5 chạy 05/10 và 12/10):

| Chỉ số | Smart HPA | Smart HPA + ưu tiên | C3 tốt hơn (ghép run 1–3) | p |
|---|---|---|---|---|
| CPU Overutilization (%) | 664 ± 25 | 608 ± 17 | 3/3 | 0,071 |
| CPU Underprovision (m) | 5.188 ± 371 | 5.502 ± 1.061 | 2/3 | 1,000 |
| Median pha tải cao (ms) | 364 ± 46 | 412 ± 17 | 0/3 | 0,250 |
| p95 pha tải cao (ms) | 1.238 ± 247 | 1.172 ± 85 | 0/3 | 1,000 |
| % thời gian p95 > 1000 ms | 46,7 ± 25,6 | 71,0 ± 22,1 | 0/3 | 0,393 |
| Throughput (request/s) | 81,8 ± 1,1 | 80,3 ± 0,7 | 0/3 | 0,143 |
| p95 checkout (ms) | 775 ± 116 | 871 ± 41 | 0/3 | 0,250 |

- **Giả thuyết không được xác nhận ở 2R-20%.** Không chỉ số nào khác biệt có ý nghĩa (mọi p > 0,05). Phía người dùng hơi kém hơn Smart HPA gốc ở cả 3 lần (median, throughput, checkout), dù vẫn tốt hơn K8s HPA 3/3 ở median, p95 và throughput.
- Ở đây so sánh sạch: Smart HPA gốc không mất quota ở 2R-20% (W9), nên chênh lệch là do quy tắc ưu tiên.
- **Nguyên nhân:** ưu tiên chỉ có tác dụng khi nhiều service thiếu *cùng lúc*. Ở run 2 và run 3, `currency` (trọng số 2) thiếu trước, trong khoảng 20 giây đầu, nên lấy gần hết quỹ (lên 8 replica). `frontend` (trọng số 3) thiếu muộn hơn và không còn gì để nhận: nó kẹt ở **2 replica**, CPU 180–192% (sát limit 200%), trong khi cần 18–20; Smart HPA gốc cho `frontend` 2–5 replica. Quy tắc dự phòng giữ `cart`, `checkout`, `productcatalog` ở 2 replica (gốc: 1), nhưng phần quota đó lấy từ quỹ mà `frontend` cần.
- Run 1 chia khác hẳn vì hai service thiếu gần như cùng lúc nên `frontend` được xếp trước (`frontend` 6, `currency` 4 với CPU 136%); lần này có Underprovision 6.726m, cao nhất trong 3 lần. Kết quả phụ thuộc thứ tự service nào thiếu trước, đúng điểm yếu W4 mà C3 định sửa nhưng chưa sửa được.
- **Hướng sửa (chưa làm):** cho service trọng số cao hơn lấy lại quota mà service trọng số thấp hơn đã *mượn* vượt maxR ban đầu, có giới hạn để không làm service kia thiếu ngược lại.

**Lưu ý khi dùng số liệu:** C3 chạy khác ngày với Smart HPA và K8s HPA (không xen kẽ). Mục 6 đã ghi nhận p95 lệch giữa các ngày chạy, nên chênh lệch nhỏ ở 2R-20% không đủ tin; chênh lệch lớn ở 5R-50% thì ít bị ảnh hưởng. Cả 6 lần ngày 13/10: 0 pod `Unschedulable`, 0 request lỗi trừ 1 request ở 5R-50% run 1, 0/8.488 ping mất trên mỗi node (`results\ping_20261013.csv`). 5 lần ngày 15/10 (`results\ping_20261015.csv`, log `results\batch_20261015.log`): 0 pod `Unschedulable`, 0 request lỗi, 0 ping mất, **trừ C3 run 4**: hai lần chập mạng khoảng 5 giây lúc 14:32:56 và 14:33:35 (phút 12–13 của lần chạy), mất 15 ping trên cả 3 node (`.10`: 8, `.11`: 3, `.12`: 4), 13/63.765 request lỗi (0,02%, `500` và `RemoteDisconnected`). Lần này vẫn qua `check_run.py`, không rớt tải nên giữ lại (R06 ngày 05/10 có 44 lỗi cũng đã giữ). Tuy vậy p95/p99 pha tải cao của run 4 (1.356 / 1.714 ms) bị ảnh hưởng, nên không dùng số phía người dùng của run 4 để kết luận.

#### Phương án chọn
| Phương án | Gồm | Phù hợp khi |
|---|---|---|
| A (an toàn) | C1 + C2 | Ít thời gian, làm một mình |
| B (điểm cao) | C1 + C3 | Có thời gian sửa thuật toán |
| C (đầy đủ) | C1 + C2 + C3 | Làm nhóm hoặc còn nhiều thời gian |

> ✅ **Nhóm đang làm theo nhóm → đề xuất phương án C.** C1 do vai trò C (phân tích) làm, C2 và C3 do vai trò B (code) viết; Dương chạy trên cluster. Nếu thiếu thời gian thì bỏ C2 trước.

Bổ sung rẻ, nên làm kèm bất kỳ phương án nào: báo cáo **độ lệch chuẩn** và **kiểm định Mann-Whitney U** giữa hai autoscaler (giải quyết W6).

---

## 8. Checklist đảm bảo kết quả hợp lệ

Trước **mỗi** lần chạy:
- [ ] Không có pod `Pending`, `Terminating` hay `CrashLoopBackOff`.
- [ ] Mọi deployment đang ở 1 replica.
- [ ] Chỉ có **một** autoscaler đang chạy: không còn HPA cũ khi chạy Smart HPA, không còn `Main.py` khi chạy K8s HPA.
- [ ] Cấu hình maxR và threshold đúng kịch bản.
- [ ] Script ghi metric đang chạy.
- [ ] Laptop không làm việc nặng khác (tắt game, render, nhiều tab trình duyệt).
- [ ] Các VM khác (Controller, Compute…) đã tắt.

Trong lúc chạy:
- [ ] Theo dõi `kubectl get pods | findstr Pending`, phải luôn trống. Nếu có, **hủy lần chạy đó**.

Sau khi chạy:
- [ ] File CSV đủ và không rỗng.
- [ ] Ghi chú bất thường vào nhật ký.

---

## 9. Xử lý sự cố thường gặp

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| `ping 8.8.8.8` không trả lời | Mạng chặn ICMP | Dùng `curl -I https://google.com` để kiểm tra |
| `curl: (35) Recv failure: Connection reset` khi tải từ GitHub hoặc mirror (cả Windows lẫn VM) | Mạng chập chờn, cắt kết nối HTTPS ngẫu nhiên. Không phải chặn DNS (đã thử DoH 1.1.1.1 vẫn lỗi) | Thêm `--retry 10 --retry-all-errors --retry-delay 3` cho `curl`; với k3s thì tải trước rồi cài bằng `INSTALL_K3S_SKIP_DOWNLOAD=true` (mục 5.2) |
| `curl` đứng im ở một % nào đó, tốc độ 0 | Kết nối bị treo, `curl` mặc định không tự hủy | `Ctrl+C`, chạy lại với `-C - --speed-limit 1000 --speed-time 30`; hoặc `scp` file từ máy đã tải xong qua mạng nội bộ |
| Dán nhiều lệnh một lúc, lệnh đầu hỏi `yes/no` hoặc mật khẩu thì hỏng | Các dòng dán sau bị đọc làm câu trả lời | Dán từng lệnh một; với `ssh`/`scp` thêm `-o StrictHostKeyChecking=accept-new` |
| SSH báo `REMOTE HOST IDENTIFICATION HAS CHANGED` | VM được clone nên host key trùng hoặc đổi | `ssh-keygen -R 192.168.161.1x` |
| Đọc file netplan báo `Permission denied` | File có quyền 600 | Thêm `sudo` |
| 2 VM cùng IP | Bật clone khi chưa đổi IP | Tắt một máy, sửa netplan, đổi machine-id |
| Worker không join cluster | Sai token, sai IP master, đồng hồ lệch | Kiểm tra `sudo systemctl status k3s-agent`, `sudo journalctl -u k3s-agent -f` |
| `kubectl top` báo `metrics not available` | metrics-server chưa sẵn sàng | Đợi 1–2 phút; `kubectl -n kube-system get pods` |
| Không vào được web frontend | Traefik chiếm cổng 80 | Cài lại k3s với `--disable traefik` |
| Pod `Pending` | Thiếu CPU hoặc RAM trên node | `kubectl describe pod <tên>` xem lý do; tăng RAM/vCPU hoặc giảm kịch bản |
| Pod `ImagePullBackOff` | Mạng chậm hoặc lỗi kéo image (ở đây: mạng reset kết nối tới gcr.io, docker.io) | Chạy `bash /tmp/prepull-images.sh` trên từng node (script ở `scripts/`), rồi `kubectl delete pod <tên>` để pod khởi động lại ngay |
| `multiprocessing` lỗi trên Windows | Thiếu `if __name__ == "__main__":` | Bọc code khởi chạy trong khối đó |
| `kubectl`/Locust từ Windows báo `Unable to connect to the server: dial tcp 192.168.161.10:6443` giữa lúc chạy, trong khi VM vẫn chạy | Kết nối host → VM (VMnet8) bị gián đoạn vài chục giây; thường trùng lúc Wi-Fi laptop chập (05/10) | Không chạy thí nghiệm khi mạng chập chờn; cắm dây mạng nếu được. `run_batch.ps1` tự chờ cluster và chạy lại, `check_run.py` tự loại lần chạy bị ảnh hưởng |
| `kubectl` báo không kết nối được ngay khi mở máy | 3 VM đang tắt | `D:\Workstation\vmrun.exe -T ws start "D:\VM\k3s-master\k3s-master.vmx" nogui` (tương tự cho 2 worker), chờ khoảng 1 phút |
| Kết quả giữa các lần chạy chênh nhiều | Laptop bận, reset chưa đủ lâu | Tăng thời gian reset, tắt ứng dụng khác, chạy thêm lần |

---

## 10. Rủi ro và phương án dự phòng

| Rủi ro | Khả năng | Ảnh hưởng | Dự phòng |
|---|---|---|---|
| Code Smart HPA khó chạy trên k3s hoặc Windows | Trung bình | Cao | Viết lại Algorithm 1 + 2 bằng Python (khoảng 200 dòng); thuật toán đơn giản, mô tả đầy đủ trong bài báo |
| Laptop không đủ tải 200 users | Thấp | Trung bình | Giảm còn 150 hoặc 100 users |
| Thiếu RAM, pod Pending ở 5R | Trung bình (nếu để 2GB/VM) | Cao | Tăng lên 4GB/VM |
| Xu hướng không giống bài báo | Thấp–trung bình | Trung bình | Phân tích nguyên nhân trong báo cáo; đây vẫn là kết quả có giá trị |
| Có lần chạy đi ngược xu hướng | Trung bình | Cao (liên quan trực tiếp yêu cầu chấm) | Giảm nhiễu: tắt ứng dụng khác, reset đủ lâu, xen kẽ thứ tự chạy. Có lần lệch thì điều tra nguyên nhân, chạy bù nếu tìm ra lỗi, không xóa dữ liệu (mục 6) |
| Demo trực tiếp lỗi khi bảo vệ | Trung bình | Cao | Quay video demo trước; kết quả và biểu đồ chuẩn bị sẵn trong slide |
| Hết thời gian | Trung bình | Cao | Ưu tiên: tái hiện 5R-50% → C1 → C2/C3 → 2R-20% |

---

## 11. Khung báo cáo và slide

### Báo cáo
1. **Giới thiệu:** microservice, auto-scaling, hạn chế của K8s HPA.
2. **Cơ sở lý thuyết:** HPA, MAPE-K, các loại scaling policy (threshold, fuzzy, queuing, control theory, AI); kiến trúc tập trung, phi tập trung và phân cấp.
3. **Tóm tắt bài báo:** Smart HPA (Algorithm 1, 2), ProSmart HPA (MAPE-KI, PROPHET), kết quả chính.
4. **Môi trường thí nghiệm:** cluster, Online Boutique, Locust, bảng khác biệt với bài báo.
5. **Kết quả tái hiện:** bảng và biểu đồ so sánh, đối chiếu với bài báo, giải thích chỗ khớp và chỗ lệch.
6. **Phân tích điểm yếu và đề xuất cải tiến:** W1–W8, chi tiết các cải tiến đã chọn.
7. **Kết quả cải tiến.**
8. **Thảo luận:** hạn chế của chính bài tập này (quy mô nhỏ, ít lần chạy…).
9. **Kết luận và hướng phát triển.**
10. **Phụ lục:** lệnh dựng cluster, cấu hình, mã nguồn.

### Slide (khoảng 15 slide)
1. Tiêu đề
2. Vấn đề: K8s HPA bị chặn maxR
3. Ý tưởng Smart HPA (sơ đồ 2 tầng)
4. Algorithm 2 minh họa bằng ví dụ (frontend lấy quota từ adservice)
5. ProSmart HPA (1 slide)
6. Môi trường thí nghiệm (sơ đồ cluster)
7. Kịch bản và chỉ số
8–9. Kết quả tái hiện
10. Điểm yếu của bài báo
11–12. Cải tiến và kết quả
13. **Demo** (live hoặc video)
14. Kết luận
15. Q&A

### Kịch bản demo khi bảo vệ (10–15 phút)
1. Cho xem `kubectl get nodes -o wide`: 3 node.
2. Mở web shop.
3. Chạy Smart HPA và Locust (rút còn 5–7 phút, 5R-50%).
4. Màn hình chia 3 ô: `kubectl get deploy`, `kubectl top pods`, biểu đồ Locust.
5. Chỉ thời điểm `frontend` vượt 5 replica nhờ nhận quota. `kubectl get pods -o wide` cho thấy pod rải ra các node.
6. Chuyển sang slide kết quả đã chuẩn bị.

---

## 12. Lịch trình đề xuất

> ⚠️ Lịch dưới đây **giả định khoảng 2 tuần** từ 02/10/2026. Sẽ chỉnh lại khi biết hạn nộp.

| Ngày | Giai đoạn | Đầu ra |
|---|---|---|
| 02/10 (T6) | GĐ1 xong, GĐ2 | Cluster 3 node Ready |
| 03/10 (T7) | GĐ3, bắt đầu GĐ4 | Online Boutique chạy, đã đọc code Smart HPA |
| 04–05/10 | GĐ4, GĐ5 | Smart HPA chạy được; script ghi metric và reset |
| 06/10 | GĐ6 (chạy qua đêm hoặc trong ngày) | 16 lần chạy tái hiện (5 lần cho 5R-50%, 3 lần cho 2R-20%) |
| 07/10 | Phân tích kết quả tái hiện + **phân tích nhất quán** | Bảng từng lần chạy, biểu đồ có thanh sai số, biểu đồ theo từng lần |
| 08–10/10 | GĐ7: cải tiến | Code cải tiến + kết quả |
| 11–13/10 | GĐ8: báo cáo | Bản nháp báo cáo |
| 14–15/10 | Slide, quay video demo, tập thuyết trình | Bản hoàn chỉnh |
| 16/10 | Dự phòng | |

---

## 13. Câu hỏi còn mở

Cần trả lời để chốt kế hoạch:

| # | Câu hỏi | Ảnh hưởng tới |
|---|---|---|
| Q1 | **Hạn nộp** bài tập lớn là ngày nào? Có buổi bảo vệ hoặc demo trực tiếp không? | Lịch trình (mục 12) |
| Q2 | Nhóm có **mấy người**? Tên từng người để điền vào bảng phân công | Phân công (mục 1) |
| ~~Q3~~ | ~~RAM mỗi VM~~ | ✅ Đã trả lời: **4GB** |
| ~~Q4~~ | ~~Lệnh chuẩn bị đã chạy trước khi clone chưa~~ | ✅ Đã trả lời: **rồi** |
| ~~Q5~~ | ~~Yêu cầu bắt buộc của giảng viên~~ | ✅ Đã trả lời: không có yêu cầu đặc biệt về công cụ; yêu cầu **chạy nhiều lần, con số khác nhau nhưng xu hướng phải giống nhau ở mỗi lần** |
| Q6 | Muốn chọn cải tiến nào (C1, C2, C3)? Đã làm cả ba: C1 (12/10), C3 (13/10, 15/10), C2 (19/10) | Mục 7 |
| ~~Q7~~ | ~~Python sẽ chạy trên Windows hay trong VM~~ | ✅ Đã trả lời: chạy trên **Windows** (venv `D:\smarthpa-venv`, `D:\prosmart-venv`) |

---

## 13b. Các điểm lệch so với bài báo và bằng chứng (2R-20%, Fig. 8/9; cập nhật 20/11)

Quy tắc: mọi điểm không giống xu hướng/% của bài mà **không phải lỗi của nhóm** phải có bằng chứng (số liệu + dữ liệu/lần chạy + script). Chi tiết E1–E15: `resultsR-20\comparison_prosmart_figs\evidence\evidence.md`.

| # | Điểm lệch / vấn đề | Nguyên nhân | Bằng chứng (số liệu, dữ liệu, script) | Trạng thái |
|---|---|---|---|---|
| L1 | Overutilization Smart/K8s (lab dùng CPU%) | Fig. 8 tính `CPU% − ngưỡng` (script ProSmart của tác giả), khác script Smart HPA | `Pro_Smart_HPA\...\Results Analysis\Results_Analysis.py` dòng 98; tính lại: K8s 373,6 / Smart 371,3 = 0,994 (bài 0,996) (E7) | ✅ Sửa cách chấm: `prosmarthpaig8_compare.py` |
| L2 | Supply K8s cao hơn bài (payment 2 pod) | Lab dùng image v0.8.1 (gói ProSmart); cột SHPA/KHPA của bài là v0.8.0 (gói Smart HPA) | payment CPU 37,6% (v0.8.1) → 11,1% (v0.8.0), Supply 194 → 139/100m; bài 101m (tag `v080`, `v080w5`) (E10) | ✅ Smart/K8s chạy v0.8.0 |
| L3 | Supply K8s cao hơn bài (adservice 2 pod) | Java khởi động lạnh vì lab khởi động lại pod trước mỗi lần chạy | Pod mới vọt 26–62% CPU ở giây 25–55; pod ấm (pilot2s run2) giữ 1 pod ~15%; làm ấm 200 user/300 s → adservice 200m (bài 206m) (E11) | ⚠️ `--pod-warmup 300 --pod-warmup-users 200` chỉ đỡ một phần: K8s v080w5 run2/run3 adservice vẫn lên 2 pod ở giây 129–132 (một mẫu 24% = 1,2 × ngưỡng), Supply 285/289m; chỉ run1 giữ 1 pod (E16) |
| L4 | Underprovision Smart/K8s (bài −1,9%, lab +18–25%) | Ô frontend K8s 2500m của bài không thể xảy ra | Mức tối đa (20 − 2) × 100 = 1800m (DR ≤ 2 × 200% / 20%); Overutilization frontend 147 của chính bài → CPU ~167% → ~1500m; lab frontend CPU 147–161%, max 179%; bỏ frontend: K8s lab 2674 so với bài 2590; phụ lục online (figshare 28028417) cùng số 2500 (E3, E5, 20/11 (2)) | ❌ Không sửa được, báo cáo là lỗi của bài |
| L5 | Overutilization Smart/K8s còn lệch (sau 3 cặp +23%) | ARM hạ productcatalog/recommendation xuống 1 pod ở giây 28–33 dựa trên số CPU cũ 10–33 s; mỗi lần chạy khác nhau | 5/5 lần mất quota dùng số cũ (6%, 6%, 6%, 1%, 9%), 2–10 s sau là 26–50% (DR 2–3); run2 giữ prodcat → Overutilization 359 (bài 382); metrics-server 15 s chuẩn, pod start 15 s = bài, `--kubectl-delay 0.9` không đỡ (pilot2s-d5); bài trung bình prodcat 1,76 / recom 1,47 pod (E15) | 🟡 Có bằng chứng độ nhạy theo pha: `scripts\l5rm_phase_replay.py --strict`, chỉ đổi pha scrape → prodcat giữ/mất, Overutilization 336–504 (bài 382, lab 454–499), xem Nhật ký 20/11 (11); đường tải từng lần + lỡ scrape 16%: 7/8 đường tải cho cả mức bài (≤ 382) lẫn mức lab (≥ 454), TB mô phỏng 454 = lab 448 (20/11 (14)). 8 cặp xong: +23,5%, prodcat giữ 2/8; nếu vẫn lệch: khác biệt thời điểm AWS không đo được, kèm bảng 5 lần |
| L6 | Tải: bài 600 user, lab 200 user | CPU mỗi request ở lab ~2,7 lần; 200 user lab ≈ trạng thái CPU của bài ở 600 user | Fig. 4 (ảnh trong PDF): 600 user @ 2/s, ~235 req/s; lab 200 user = 86 req/s nhưng CPU từng service ≈ bài; thử 600 user: recommendationservice trượt liveness 1 s, CrashLoopBackOff, controller crash (tag `v080w5u600`, `_failed_*`, `_aborted_*`) | ✅ Giữ 200 user @ 2/s (giải thích trong báo cáo) |
| L7 | ProSmart dùng `ceil` khi làm tròn PROPHET | Bài không quy định; `ceil` làm model tác giả mâu thuẫn với dữ liệu train của chính nó | Capacity: tổng maxR 23,5 trên quota 22 (currency 3 so với 2,1 ghi nhận, email 1,48 so với 1,0); demand: adservice/email/redis vượt maxR 39/94/17% so với ghi nhận 2/7/0%; `round` khớp (E13) | ✅ `PROSMART_ROUNDING=round` (mặc định) |
| L8 | Fig. 8 so ProSmart với Smart/K8s trên 2 phiên bản ứng dụng | Cột ProSHPA = dữ liệu ProSmart (v0.8.1); SHPA/KHPA = bài Smart HPA (v0.8.0) | payment DR: dữ liệu ProSmart tác giả 3,1; lab v0.8.1 4,0–4,4; v0.8.0 1,0; cột SHPA/KHPA payment 1 pod; manifest gói ProSmart v0.8.1, gói Smart HPA v0.8.0 (E14); ProSHPA = `.pkl` (E9: 3708/44 so với 3729/59) | ✅ ProSmart chạy v0.8.1 (chờ chạy); ghi rõ trong báo cáo |
| L9 | Cột demand cho ProSmart (nghi vấn) | Không lệch: dữ liệu tác giả là DR đo được | Demand tác giả theo số user, không nhìn trước 25 s (frontend 1,5/4,1/13 ở giây 10/30/100; dự đoán 25 s là 6/8/15) (E8) | ✅ Giữ cột D |
| L10 | Fig. 9 không có chữ U | Model công bố chỉ theo thời gian; window chỉ dịch thời điểm | Mô phỏng `prosmarthpa\sim_window.py`: window 5–30 s đổi chỉ số < 0,2% (dịch vụ nặng có PDR > PmaxR từ giây 15 với mọi window); bài ở 25 s = dữ liệu train; Fig. 9 cũ của lab (model lab) cũng không có chữ U | ❌ Không chạy (quyết định 20/11); nếu cần: 5 s & 30 s × 2 lần |
| L11 | Supply K8s còn hơn bài ~80m (3 cặp v080w5: lab 2135, bài 2056) | Theo service (lab TB / bài): adservice 258/206 (+52, xem L3), **redis-cart 107/70 (+37)**, email 121/138 (−17, không phải dư), shipping 193/186, còn lại ±3 (cart 387 = 387). **Redis:** lab chạy `redis:alpine` không ghim = **Redis 8.10.2** (build 21/09/2026) và entrypoint tự nạp 4 module (rejson, redisearch, redistimeseries, redisbloom); gói Smart HPA ghim **7.0.11** (06/2023), gói ProSmart ghim **7.2.3** (12/2023), không module. Ở 1 pod redis lab chạy sát ngưỡng → lên 2 pod; pod thứ 2 không nhận tải (kết nối cố định) nên không bao giờ xuống | Redis 1 pod: CPU TB 14–20% trên 32 lần chạy lab; **9/16 run K8s vượt ngưỡng**, bài 0/10 (Supply 70,01; DR = 2 chỉ 0,8% mẫu). Pod thứ 2 của redis/email/cart luôn 2–5m (`pod_metrics.csv`, mọi tag). Digest: lab `38117873…` = 8.10.2; helm Smart HPA `121bac94…` = 7.0.11; ProSmart `a3e82d34…` = 7.2.3 (config image trên Docker Hub; layer 8.10.2 chứa `usr/local/lib/redis/modules/*.so`, `docker-entrypoint.sh` thêm `--loadmodule`). Script: `scripts/l11/l11_services.py`, `l11_pods.py`, `l11_persvc.py` (chạy từ `results/`); digest: `evidence/E16_redis_images.txt` (E16) | ⏳ Giả thuyết chính Redis 8 + module; **chờ A/B `scripts/redis_ab.sh`** (7.0.11 / 8.10.2 / 8.10.2 không module, cùng node, cùng tải cartservice) — cần người dùng bảo chạy |
| — | Đã loại (không phải nguyên nhân) | VM bị xếp vào E-core; độ trễ controller (EKS qua AWS CLI); thiếu dữ liệu thời gian của tác giả | VM 0,233 s so với máy thật 0,243 s (cùng bài đo); `pilot2s-d5` vẫn mất quota; figshare 25393408 = code, 28028417 = hình | — |

---

## 14. Nhật ký tiến độ

| Thời gian | Việc đã làm | Kết quả / ghi chú |
|---|---|---|
| 30/09/2026 | Đọc bài báo, tìm hiểu replication package | Chọn phương án VMware nhiều node + k3s |
| 02/10 08:28 | Tạo VM `k3s-master` (Ubuntu Server 24.04.5) | Bỏ LVM, cài OpenSSH, không cài snap |
| 02/10 08:40 | SSH từ Windows vào master | ✅ |
| 02/10 08:41 | Lấy thông tin mạng | Dải `192.168.161.0/24`, gateway `.2`, card `ens33` |
| 02/10 ~08:44 | Đặt IP tĩnh `192.168.161.10` | Gateway OK; ping internet bị chặn nhưng HTTPS OK |
| 02/10 ~08:49 | Clone full `k3s-worker1`, `k3s-worker2` | ✅ |
| 02/10 08:51 | Sửa worker1: hostname, machine-id, IP `.11` | ✅ |
| 02/10 08:54 | Sửa worker2: hostname, machine-id, IP `.12` | ✅ |
| 02/10 09:11 | Chốt cấu hình và yêu cầu | RAM 4GB/VM; lệnh chuẩn bị đã chạy trước khi clone; yêu cầu chấm: xu hướng nhất quán giữa các lần chạy → thêm phần phân tích nhất quán, khuyến nghị 5 lần cho 5R-50% |
| 02/10 09:13 | Xác định cách làm | Làm theo nhóm, Dương phụ trách demo → thêm bảng phân công theo vai trò, chọn phương án cải tiến C |
| 02/10 ~09:20 | Bật 3 máy, kiểm tra cấu hình; cài SSH key từ Windows | Cả 3 máy đạt mọi mục kiểm tra (bước 1.12) |
| 02/10 ~09:30 | Cài k3s bằng lệnh một dòng | ❌ `Download failed`: mạng cắt HTTPS ngẫu nhiên (Windows cũng bị; DoH không giúp; mirror Rancher CN cũng bị) |
| 02/10 ~09:50 | Tải k3s có retry trên từng VM, kiểm tra sha256, cài với `INSTALL_K3S_SKIP_DOWNLOAD=true` | Master bị treo khi tải → `scp` file từ worker2 sang. ✅ |
| 02/10 09:58 | Kiểm tra `kubectl get nodes -o wide` | ✅ 3 node Ready, `v1.36.5+k3s1`, IP `.10/.11/.12` |
| 02/10 11:15 | Kiểm tra pod `kube-system`, `kubectl top nodes` trên master | ✅ 3 pod hệ thống Running, metrics-server có số liệu cho cả 3 node |
| 02/10 11:25 | Copy kubeconfig về Windows, chạy `kubectl get nodes`, `kubectl top nodes` từ PowerShell | ✅ **Xong Giai đoạn 2** |
| 02/10 | Clone repo ProSmart_HPA vào `Demo\Pro_Smart_HPA\ProSmart_HPA`, đọc manifest | Dùng `release\kubernetes-manifests.yaml`; resource khớp bài báo; không có loadgenerator |
| 02/10 ~11:45 | `kubectl apply -f release\kubernetes-manifests.yaml` | Sau 11 phút chỉ 2/11 Running; còn lại + svclb `ImagePullBackOff` do mạng reset kết nối tới gcr.io/docker.io → viết `scripts/prepull-images.sh` (kéo image có retry, chạy trên cả 3 node) |
| 02/10 | Chạy `prepull-images.sh` trên 3 node, xóa pod kẹt | Cả 3 node đủ 12 image (một số image phải thử 2–4 lần); 11/11 pod Running, rải trên cả 3 node |
| 02/10 ~13:40 | Kiểm tra Giai đoạn 3 | `frontend-external` có EXTERNAL-IP `.10/.11/.12`; web shop mở được; thêm vào giỏ + checkout qua curl ra "Your order is complete"; `kubectl top pods` có số liệu (lúc rảnh 1–2m CPU mỗi pod); CPU/RAM request/limit khớp bảng mục 5.3. ✅ **Xong Giai đoạn 3** |
| 02/10 | Tải package Smart HPA (`HussainAhmad05-Smart_HPA-196c63d`), đọc code theo checklist 5.4c | Chỉ dùng kubectl, không phụ thuộc AWS. 3 lỗi phải sửa mới chạy được (tên file import, cấu trúc thư mục, chưa có Python). Ghi chú chi tiết ở mục 5.4c |
| 02/10 | Đọc toàn bộ PDF bài báo 2025 | Baseline là K8s HPA. Mục 5.2: Smart HPA vs K8s HPA, 9 kịch bản. Mục 5.3: ProSmart vs cả hai, chỉ 2R-20%. Các con số trong mục 2 khớp bài. Lỗi ARM dòng 101 xác nhận lệch Algorithm 2. Cập nhật mục 2 |
| 02/10 ~14:10 | Cài Python 3.11.9 (winget), venv `D:\smarthpa-venv`. Tạo `Demo\smarthpa\`: code Smart HPA đã sửa (kịch bản lấy từ `config.py`), `k8shpa_observer.py` (ghi KB cho K8s HPA bằng chính code Monitor/Analyse của Smart HPA, không scale), `cluster_recorder.py`, `run_experiment.ps1` (reset → chạy → lưu `results\`) | Smart HPA chạy được trên Windows, mỗi vòng ~2s lúc rảnh, ~3.6s lúc có tải |
| 02/10 14:18–14:27 | Chạy thử `run0` cả hai autoscaler, 5R-50%, 100 users, 3 phút | Script chạy trọn vẹn. Smart HPA: ARM lấy quota của `adservice`, `cartservice` cho `currencyservice` (lên 10 replica). Nhưng tải 100 users/3 phút quá nhẹ: K8s HPA không chạm maxR nên Underprovision cả hai = 0. Smart HPA scale down quá gắt (currency 10→1→4), 35 lỗi 500/6532 request, Overutilization cao hơn K8s HPA. "Pending" trong recorder là pod đang khởi động, không phải thiếu tài nguyên → thêm cột `unschedulable_pods_total` |
| 02/10 | Thêm `make_run_report.py` (mỗi lần chạy: `metrics.csv`, `summary.md`, 3 biểu đồ) và `make_comparison.py` (gộp mọi lần chạy của 1 kịch bản: `results\<kịch bản>\comparison\` gồm `fig_runs.png`, `fig_means.png`, `comparison.md`, `all_runs.csv`). Cả hai tự chạy ở cuối `run_experiment.ps1` | `Results_Analysis.py` gốc của tác giả không chạy được (gán vào list rỗng → IndexError) nên viết lại phần tính thời gian; công thức 7 chỉ số giữ đúng như code gốc |
| 02/10 14:39–15:20 | R01 (K8s HPA) + R02 (Smart HPA), 5R-50%, 200 users, 15 phút — cấu hình chính thức | **200 users đủ tải.** K8s HPA: `frontend`, `currency` cần ~1200m nhưng kẹt ở 500m; Underprovision 1035m trong 13.53 phút (bài: 934m / 13.46 phút). Smart HPA: frontend lên 10 replica, currency lên 14, lấy quota từ ad/cart/email/shipping/checkout/payment/redis; **tốt hơn ở cả 8 chỉ số** (Underprov 381 vs 1035m, Overprov 751 vs 3623m, Supply 3901 vs 2653m). Khác bài: Smart HPA vẫn còn Underprovision (bài = 0) vì tổng quota toàn app đã dùng hết; Overutilization Time gần ngang (14.4 vs 14.5). Cả hai 0 lỗi, p95 ~900ms |
| 02/10 15:27–16:41 | `run_batch.ps1` (chạy theo cặp, có giờ dừng): R03, R04, R05 xong. **R06 (Smart HPA run 3) lỗi** sau ~1 phút tải: một lệnh `kubectl get deployment recommendationservice` trả lỗi, code gốc không xử lý lỗi nên cả Smart HPA dừng. Batch không nhận ra lỗi và chạy tiếp sang 2R-20% run 1 → dừng tay lúc 16:41 (đang cooldown, chưa tạo tải, không còn HPA/tiến trình sót) | Dữ liệu R06 chuyển sang `results\5R-50\smarthpa\_failed_run3_20261002-1634` (giữ để tra cứu, không tính). Sửa: `config.py` thêm retry 5 lần cho kubectl (áp dụng cho cả 2 autoscaler); `run_experiment.ps1` coi controller lỗi là lần chạy hỏng → chuyển thư mục sang `_failed_...` và trả exit 1 để batch dừng. **Kết quả 2 cặp hợp lệ: Smart HPA tốt hơn ở cả 7 chỉ số Table 1 trong 2/2 lần**; p95 latency 1/2 |
| 05/10 08:35 | 3 VM đang tắt → bật bằng `D:\Workstation\vmrun.exe -T ws start <vmx> nogui` | 3 node Ready, 11/11 pod Running sau khoảng 1 phút, không còn HPA cũ |
| 05/10 08:39–11:04 | R06 (chạy lại) rồi `run_batch.ps1` R07–R12 | ✅ Cả 7 lần hợp lệ. R06 có một lần chập mạng ngắn lúc 08:51 (44/64.706 request lỗi, 0,07%, không rớt tải) → giữ |
| 05/10 11:13 | R13 (K8s HPA 5R-50% run 4) hỏng | `kubectl` từ Windows mất kết nối tới `192.168.161.10` (master vẫn chạy bình thường, k3s không restart). Vòng lặp theo dõi trong `run_experiment.ps1` không có retry nên cả lần chạy hỏng; `Move-Item` sang `_failed` cũng lỗi vì tiến trình con của Pool còn giữ file log. **Sửa:** vòng theo dõi chịu được lỗi mạng (đếm vào `monitor_kubectl_errors`), dừng tiến trình bằng `taskkill /T`, thử `Move-Item` 6 lần, log xóa HPA trung thực |
| 05/10 11:33–12:21 | Chạy lại R13, R14, R15 | R13 "chạy xong" nhưng mất kết nối 3 lần (11:46, 11:48, 11:50): 2,2% request lỗi (`ConnectTimeout`), khoảng 3 phút gần như không có tải → **không hợp lệ, đã xóa**. R14 ✅ sạch (1 lỗi). R15 hỏng 12:20 khi tạo HPA |
| 05/10 13:30 | Rà lại toàn bộ 14 lần đã lưu bằng số liệu Locust | Chỉ R13 hỏng. Thêm `check_run.py` (tự loại lần chạy mất kết nối) và cho `run_batch.ps1` bỏ qua lần đã có, chờ cluster, tự chạy lại tối đa 3 lần. Đã xóa mọi thư mục `_failed_*` |
| 05/10 13:42–13:50 | Chạy lại R13 → hỏng lần nữa lúc 13:48 khi tạo HPA | **Tạm dừng** vì mạng chập chờn. Đã dừng hết tiến trình, cluster sạch (0 HPA, 11 deployment × 1), 3 VM vẫn bật |
| | **Nguyên nhân mất kết nối (chưa chắc chắn):** đi qua VMnet8 chứ không qua Wi-Fi, nhưng 3/4 lần trùng sự kiện driver Wi-Fi Intel AX211 (Netwtw14 7021/7003) vài giây trước đó; lần 13:48 không có sự kiện Wi-Fi. Lần sau chạy nên ghi ping mỗi giây tới `.10/.11/.12` để xác định | |
| 07/10 | Thêm `make_paper_figs.py`: vẽ lại Fig. 6 (cột chồng theo microservice) và Fig. 7 (2×2 demand/capacity + CPU, Smart cạnh K8s) theo bố cục bài báo | Hình 2R-20% cho thấy nguyên nhân Smart HPA kém hơn: ARM lấy quota của productcatalog/recommendation (supply ~190m → 100m) dồn cho currency, khiến hai service này quá tải (CPU ~175%) |
| 07/10 13:24–13:29 | 3 VM đang tắt → bật bằng `vmrun ... nogui` | 3 node Ready, 11/11 pod Running, 0 HPA |
| 07/10 13:29–14:32 | `run_batch.ps1 -Pairs "5R-50%:4","5R-50%:5"`: R13, R15, R16 (R14 có sẵn, bỏ qua), đồng thời ghi ping mỗi giây vào `results\ping_20261007.csv` | ✅ Cả 3 lần qua `check_run.py`, 0 request lỗi, 0/5008 ping mất trên mỗi node. **Xong toàn bộ 16 lần chạy** |
| 08/10 | Tạo git local ở `Demo\` (commit đầu `597db72`); bỏ qua `Pro_Smart_HPA\` (clone có `.git` riêng, commit `49a45c3`), `smarthpa\Knowledge Base\`, `__pycache__` | |
| 08/10 | Xem lại nguyên nhân Smart HPA thua K8s HPA ở 2R-20% (Overutilization 674 vs 463%, Underprovision 5150 vs 3718m) | Không phải do máy: không có pod `Unschedulable` ở cả 6 lần, supply chỉ ~2.4/12 core. Lỗi ARM dòng 101 **không ảnh hưởng ở 2R** (maxR = 2, `Desired = 1` nên luôn rơi vào nhánh `if` đầu hoặc `else`). Nguyên nhân: ARM chia quota tham lam lúc tải tăng (~phút 1), `currency` lên maxR 12, `productcatalog` còn 1, rồi giữ nguyên đến hết lần chạy (W4). Không cần chạy lại |
| 08/10 | Quyết định làm **ProSmart HPA** (Giai đoạn 6b). Tạo `D:\prosmart-venv`, mở 22 model `.pkl` của tác giả, viết `prosmarthpa\train_prophet.py`, kiểm tra chéo | Model tác giả không có regressor, khác bài báo và code (W7). Prophet đoán kém hơn cách "giống bây giờ" về sai số trung bình nhưng ít đoán thiếu hơn hẳn. Chọn `reg` (theo bài báo). Chi tiết ở mục 2 |
| 08/10 | Viết `prosmarthpa\prosmart_hpa.py` (Algorithm 3–4), thêm `-Autoscaler prosmarthpa` vào `run_experiment.ps1`, sửa `make_comparison.py` cho 3 autoscaler | Kiểm tra offline: phần chia quota (Plan_A) không vượt tổng quota trong 20.000 trường hợp ngẫu nhiên; chạy lại so sánh 5R-50%/2R-20% không đổi số |
| 08/10 14:35–14:47 | 3 VM đang tắt → bật bằng `vmrun ... nogui` | 3 node Ready. Deployment còn ở mức scale của lần chạy trước (45 pod), `run_experiment.ps1` tự reset về 1 |
| 08/10 14:48–14:53 | `run0` ProSmart 2R-20% (100 users, 3 phút) | ✅ Exit 0, 0 request lỗi, 0 pod `Unschedulable`, mỗi vòng ~0.9s (Smart HPA ~2s), ARM bật từ giây 12. **Phát hiện W8:** supply lên 3,070m > quota 2,540m do nhánh "no scale" của Algorithm 4. Quyết định: chạy đúng bài báo, ghi W8 vào báo cáo |
| 08/10 14:53–15:56 | ProSmart 2R-20% run1–3 (200 users, 15 phút), chạy tuần tự bằng `run_experiment.ps1 -Autoscaler prosmarthpa` | ✅ Cả 3 hợp lệ, 0 request lỗi, 0 pod `Unschedulable`. So với Smart HPA: Overutilization −37% (3/3), p95 −20% (3/3), Underprovision +23% (0/3), supply vượt quota 16–23% ở cả 3 lần (W8). Chi tiết ở Giai đoạn 6b. **Xong Giai đoạn 6b** |
| 12/10 10:17 | 3 VM đang tắt → bật bằng `vmrun ... nogui`. Thêm tham số `-Autoscalers` cho `run_batch.ps1` (mặc định vẫn `k8shpa,smarthpa`) để batch chạy được cả ProSmart | 3 node Ready sau vài giây |
| 12/10 10:23–12:30 | `run_batch.ps1 -Pairs "2R-20%:4,2R-20%:5" -Autoscalers "k8shpa,smarthpa,prosmarthpa"`: 6 lần xen kẽ cùng ngày, ghi ping mỗi giây vào `results\ping_20261012.csv`. ProSmart dùng nguyên 22 model train từ run1–3 | ✅ Cả 6 lần hợp lệ ngay lần thử đầu, 0 pod `Unschedulable`, 0/7542 ping mất trên mỗi node. Smart HPA run4 có 44/61.781 request lỗi 500 (0,07%) trong 2 giây lúc 11:01, không phải do mạng → giữ. Kết luận không đổi so với n=3; run 4 ngược hướng ở Supply / Overprovision Time / Underprovision Time (mục 6). p95 của Smart HPA và K8s HPA hôm nay cao hơn 05/10 (1200 và 1400 ms so với 930–1000 và 1300 ms) |
| 12/10 | Đối chiếu lại plan với `results\` và code sau đợt chạy 12/10 | Số liệu khớp; sửa `currency` ở run 4 (so với 855–1129m, không phải ~1058m), cập nhật mục 4, ma trận chạy, W8. `run_batch.ps1`: `-PairMinutes` mặc định tính theo số autoscaler (21 phút mỗi cái). `train_prophet.py`: mặc định `--mode reg` để train lại không vô tình ghi đè bằng model chỉ theo thời gian |
| 12/10 | Tắt 3 VM (`vmrun ... stop soft`). **C1:** viết `make_user_metrics.py` (9 chỉ số phía người dùng từ `locust_stats_history.csv`, 2 hình), thêm p-value Mann-Whitney U vào `make_comparison.py` (W6), gắn vào cuối `run_experiment.ps1` | 2R-20%: ProSmart → Smart HPA → K8s HPA, nhất quán 5/5 ở hầu hết chỉ số. 5R-50%: không chỉ số phía người dùng nào nhất quán (cao nhất 3/5). Ngưỡng SLO chốt 1000 ms. Chi tiết ở mục 7, phần C1. Số trong `all_runs.csv` và các hình cũ không đổi sau khi sửa `make_comparison.py` |
| 13/10 ~16:00 | **C3:** viết `smarthpa\Priority_Resource_Manager.py` (chia quota theo trọng số, mục 7), thêm `-Autoscaler smarthpa-prio` vào `run_experiment.ps1`, thêm `--c3` cho `make_comparison.py` và `make_user_metrics.py` (đầu ra riêng ở `comparison_c3`). Soi lại Knowledge Base các lần cũ | Phát hiện **W9**: ARM gốc làm mất 25–37% quota ở 5R-50% (cả 5 lần), không bị ở 2R-20%. Kiểm tra offline bản mới: không vượt quota trong 2.000 kịch bản × 300 vòng. Chạy lại `comparison` mặc định: không file kết quả nào đổi |
| 13/10 16:10–16:19 | 3 VM đang tắt → bật bằng `vmrun ... nogui`. `run0` C3 2R-20% (100 users, 3 phút) | ✅ Exit 0, 0 request lỗi, tổng capacity giữ 2.540m. `frontend` chỉ lên 3 replica vì `currency` lấy quota trước |
| 13/10 16:19–18:26 | `run_batch.ps1 -Pairs "2R-20%:1,2R-20%:2,2R-20%:3,5R-50%:1,5R-50%:2,5R-50%:3" -Autoscalers "smarthpa-prio"`, ghi ping mỗi giây vào `results\ping_20261013.csv`; log ở `results\batch_20261013.log` | ✅ Cả 6 lần hợp lệ ngay lần thử đầu, 0 pod `Unschedulable`, 0/8.488 ping mất trên mỗi node. **5R-50%:** tốt hơn Smart HPA gốc 3/3 ở mọi chỉ số trừ Overprovision (Underprovision 20 so với 389m, p95 671 so với 1.085 ms), nhưng lẫn với việc sửa W9. **2R-20%:** không cải thiện, phía người dùng hơi kém hơn 3/3. Chi tiết ở mục 7, phần C3. Chưa chạy Smart HPA gốc cùng ngày |
| 13/10 18:40 | Đối chiếu lại mục 7 (C3) và nhật ký 13/10 với `results\` sau khi batch xong | Số liệu khớp `comparison_c3\comparison.md`, `user_metrics.md`, `run_info.json` và file ping. Cluster không kết nối được từ Windows (`kubectl` timeout tới `192.168.161.10:6443`); file ping dừng ghi lúc 18:29:02. Chưa kiểm tra 3 VM đang tắt hay mất mạng, nên chưa xác nhận trạng thái HPA/deployment sau lần chạy cuối. Code và kết quả C3 chưa commit (nhánh `prosmart-2r20`) |
| 15/10 | **Đối chứng C3:** thêm `SMARTHPA_ARM=flat` (`Priority_Resource_Manager.py` với mọi trọng số 1, không dự phòng), `-Autoscaler smarthpa-flat` trong `run_experiment.ps1`, `--c3-control` trong `make_comparison.py` và `make_user_metrics.py` (đầu ra `comparison_c3_control`); `run_experiment.ps1` với `smarthpa-prio` giờ dựng lại cả `comparison_c3` lẫn `comparison_c3_control` | Kiểm tra offline: không vượt quota trong 2.000 kịch bản × 300 vòng ở cả 5R-50% và 2R-20%. Chạy lại mọi `comparison*` với dữ liệu cũ: không file nào đổi |
| 15/10 13:52–13:55 | 3 VM đang tắt → bật bằng `vmrun ... nogui` | 3 node Ready, 0 HPA. Deployment còn ở mức scale của lần C3 cuối ngày 13/10 (`frontend` 14, `currency` 22), `run_experiment.ps1` tự reset về 1. Vậy lần mất kết nối 13/10 18:40 là do VM đã tắt hoặc mất mạng sau batch, không ảnh hưởng kết quả |
| 15/10 13:55–15:42 | 5 lần 5R-50% xen kẽ: đối chứng 1 → C3 4 → đối chứng 2 → C3 5 → đối chứng 3 (mỗi lần một `run_batch.ps1`), ghi ping mỗi giây vào `results\ping_20261015.csv`; log ở `results\batch_20261015.log` | ✅ Cả 5 lần hợp lệ ngay lần thử đầu, 0 pod `Unschedulable`. C3 run 4 có 2 lần chập mạng khoảng 5 giây (15 ping mất, 13 request lỗi), giữ lại. **Kết luận:** phần lớn cải thiện của C3 ở 5R-50% đến từ việc sửa W9 (đối chứng: Underprovision 10m, p95 653 ms); ưu tiên chỉ giảm thêm Overutilization 87% → 75% (p = 0,036). Chi tiết ở mục 7, phần C3 |
| 19/10 | **C2:** `smarthpa\locustfile_spike.py` (`LoadTestShape`: 50 users, spike 250 ở phút 3–7 và 10–13), `-Shape spike` trong `run_experiment.ps1` và `run_batch.ps1` (kết quả ở `resultsR-50-spike`), pha spike trong `make_user_metrics.py`, `make_flapping.py` (đếm đổi replica, đảo chiều scale, chuyển quota từ Knowledge Base) | |
| 19/10 11:45–11:53 | `run0` Smart HPA 5R-50% spike (240 s), log ở `results\c2_run0_20261019.log` | ✅ Exit 0, qua `check_run.py` |
| 19/10 11:54–14:01 | `run_batch.ps1 -Pairs "5R-50%:1","5R-50%:2","5R-50%:3" -Shape spike`, ghi ping mỗi giây vào `results\ping_20261019.csv`; log ở `resultsatch_20261019.log` | ✅ Cả 6 lần hợp lệ ngay lần thử đầu. Smart HPA tốt hơn 3/3 về tài nguyên, hòa về người dùng, nhưng flapping rõ (43 so với 0 lần đảo chiều). Smart HPA run3 có 38 request lỗi trùng hai lần scale down, không phải do mạng → giữ. Chi tiết ở mục 7, phần C2 |
| 22/10 | Thầy hỏi vì sao train lại model PROPHET. `prosmarthpa\compare_author_models.py` (kết quả ở `results\2R-20\comparison\prophet_models\`): đọc dữ liệu train trong 22 `.pkl` của tác giả, so với Knowledge Base Smart HPA của nhóm, thử dự đoán trên run 4–5. Báo cáo thêm Bảng 5.4, Hình 5.6 ở mục 5.3 (bảng sau đánh số lại 5.5, 5.6), sửa mục 4.3, Bảng 4.4, mục 8.2, Phụ lục A | Model tác giả train từ Smart HPA của họ (tổng maxR = 22 ở cả 1.810 dòng, quota có chuyển). Nhu cầu ở pha ổn định của nhóm cao hơn 15–89% ở 9/11 service; maxR của nhóm 1–12 so với 1–3. Model tác giả đoán sai 1,93 replica, đoán thiếu 42%; model nhóm 0,96 và 15%. Chưa chạy đối chứng `.pkl` tác giả trên cluster (để 23/10) |
| 24/10 | **Đối chứng model tác giả:** `PROSMART_MODELS=authors` trong `prosmart_hpa.py` (nạp 22 `.pkl` gốc, vá thuộc tính prophet 1.1.4 như `compare_author_models.py`), `-Autoscaler prosmarthpa-authors` trong `run_experiment.ps1`, `--prophet-authors` trong `make_comparison.py` và `make_user_metrics.py` (đầu ra `results\2R-20\comparison_prophet_authors`) | Chạy lại mọi `comparison` mặc định: không file nào đổi |
| 24/10 10:01–10:10 | 3 VM đang tắt → bật bằng `vmrun ... nogui`. `run0` ProSmart model tác giả 2R-20% (100 users, 3 phút), log ở `results\prophet_authors_run0_20261024.log` | ✅ Exit 0, qua `check_run.py`. Model tác giả chỉ theo thời gian nên đoán `frontend` 17, `currency` 11 replica dù chỉ 100 users |
| 24/10 10:11–11:35 | `run_batch.ps1 -Pairs "2R-20%:1,2R-20%:2,2R-20%:3" -Autoscalers "prosmarthpa-authors"`, ghi ping mỗi giây vào `results\ping_20261024.csv`; log ở `results\batch_20261024.log` | ✅ 3/3 hợp lệ. Run 2 lần đầu mất kết nối TCP tới `.10` (cổng 80 và 6443) khoảng 80 giây lúc 10:49–10:50 (ping vẫn 0 mất) → `check_run.py` loại (1,18% lỗi, 5 khung rỗng), giữ ở `_failed_run2_20261024-1053`, batch tự chạy lại. `make_run_report.py` báo lỗi ở cuối mỗi lần do in đường dẫn tiếng Việt khi stdout chuyển vào file (cp1252); file đã ghi đủ, chạy lại tay với `PYTHONIOENCODING=utf-8`. **Kết quả:** model tác giả đoán mọi service đều cần vượt maxR nên ARM không có service nào để lấy quota, gần như mọi service đứng ở 2 replica cả lần chạy (supply 2.695 ± 2m, n=3). So với model nhóm (n=5, chạy 08/10 và 12/10): model nhóm supply cao hơn 3/3 (3.065 so với 2.695m), Overprovision thấp hơn 3/3 (73 so với 216m, p = 0,036), Overutilization thấp hơn 3/3 (408 so với 461%, p = 0,25), nhưng Underprovision cao hơn 0/3 (6.111 so với 4.896m); p95 không rõ hướng (1/3). Khác ngày chạy nên phía người dùng chỉ để tham khảo |
| 24/10 11:38–12:20 | `run_batch.ps1 -Pairs "2R-20%:4,2R-20%:5" -Autoscalers "prosmarthpa-authors"` với `PYTHONIOENCODING=utf-8`, ping ở `results\ping_20261024b.csv`, log ở `results\batch_20261024b.log` | ✅ Cả 2 lần hợp lệ ngay lần đầu, 0 request lỗi, 0/2.509 ping mất. **n = 5, model nhóm so với model tác giả:** Supply 3.065 so với 2.695m (5/5, p = 0,008), Overprovision 73 so với 228m (5/5, p = 0,008), Overutilization 408 so với 455% (4/5, p = 0,22), Underprovision 6.111 so với 4.794m (model nhóm kém hơn 4/5, p = 0,056), p95 798 so với 856 ms (2/5, p = 0,55). Model tác giả vẫn tốt hơn Smart HPA ở Supply và Overutilization 5/5 (p = 0,008) |
| 24/10 12:24–13:10 | **Kiểm tra hiệu ứng ngày chạy:** `-Autoscaler prosmarthpa-rerun` (vẫn model nhóm, kết quả riêng ở `results\2R-20\prosmarthpa-rerun\` để không đổi số của `comparison` đang dùng trong báo cáo), `--prophet-sameday` trong `make_comparison.py` / `make_user_metrics.py` (đầu ra `comparison_prophet_sameday`). `run_batch.ps1 -Pairs "2R-20%:1,2R-20%:2" -Autoscalers "prosmarthpa-rerun"`: run 1 xong 12:45 (log `results\batch_20261024c.log`, ping `ping_20261024c.csv`); dừng batch lúc 12:45 trước khi run 2 tạo tải để người dùng tắt mạng; run 2 chạy lại 12:49–13:10 (log `batch_20261024d.log`, ping `ping_20261024d.csv`) | ✅ 2/2 hợp lệ, 0 request lỗi, 0 ping mất. **Hiệu ứng ngày nhỏ:** model nhóm 24/10 so với 08/10 và 12/10: Supply 3.115 so với 3.065m, Underprovision 6.160 so với 6.111m, Overprovision 92 so với 73m, p95 725 so với 798 ms (đều nằm trong dải các lần cũ hoặc sát). **Cùng ngày 24/10, model nhóm (n=2) so với model tác giả (n=5):** cùng hướng như so khác ngày: Supply 2/2, Overprovision 2/2, Overutilization 2/2 tốt hơn, Underprovision 0/2; p95 2/2 tốt hơn (725 so với 856 ms) nhưng n = 2 nên p ≥ 0,095 |
| 24/10 | Đưa kết quả 24/10 vào báo cáo. `prosmarthpa\compare_author_runs.py` (số replica theo thời gian và pdr từ `controller.out.log`, kết quả ở `results\2R-20\comparison_prophet_authors\replicas.*`, `fig_replicas.png`). Báo cáo: mục 5.3 thêm Bảng 5.6 (model nhóm so với model tác giả, n=5), Hình 5.7 (replica theo thời gian), Bảng 5.7 (chạy lại cùng ngày), bảng nhất quán đánh số lại 5.8; sửa mục 1.3, 4.3, Bảng 4.3, Bảng 4.4, mục 8.1, 8.2, 9 (49 lần chạy hợp lệ), Phụ lục A; xuất lại PDF | Model tác giả đoán cả 11 service cần ≥ 2 replica ở pha ổn định (adservice 2,3) nên ARM gần như không chuyển quota: frontend, currency 3 replica, còn lại 2 (24 pod, cả 5 lần). Model nhóm đoán adservice 1,9 nên ARM lấy quota cho frontend 6, currency 6–9 (28–31 pod) |
| 12/11 | **Hình ProSmart theo bài báo:** `prosmarthpa\make_prosmart_figs.py` vẽ Fig. 5 (model fit, recommendationservice như bài), Fig. 8 (ProSmart / Smart / K8s, cột chồng theo service), Fig. 9 (6 prediction window) vào `resultsR-20\comparison_prosmart_figs\`. Window đọc từ `PROSMART_WINDOW` (mặc định 25) | Fig. 8 với model đầu (n=5): khớp bài ở Supply (+27% so với Smart), Overutilization (−39%), Overprovision (−6%, yếu); ngược bài ở Underprovision (+18%), phần tăng chủ yếu ở `currencyservice`. Fig. 9 chưa có dữ liệu |
| 12/11 | **Train lại theo mục 5.1 bài báo.** Bài không ghi số lần chạy dùng để train (10 lần suy từ `.pkl`: 1.810 dòng) nhưng ghi "tune the hyperparameters ... using a cross-validation approach"; model đầu dùng tham số mặc định. `prosmarthpa	une_prophet.py`: lưới `changepoint_prior_scale` 0,001–0,5 × `prior_scale` regressor 0,01–10, leave-one-run-out trên Smart HPA 2R-20% run 1–5, nested CV để đánh giá; model ở `prosmarthpa\models_5runs_cv\` (`models\` giữ nguyên = model đầu) | Sai số t+25s (replica, nested CV): demand đã tinh chỉnh 0,88, mặc định 0,85, "giống bây giờ" 0,51; capacity 0,45 / 0,44 / 0,04. Trên run 4–5: model đầu (3 lần) 0,96, mặc định train 4 lần 0,93 → thêm dữ liệu và tinh chỉnh đều không cải thiện. Chọn dùng model đã tinh chỉnh vì đúng quy trình bài báo |
| 12/11 | **Kế hoạch chạy cluster (chốt trước khi chạy):** `-Autoscaler prosmarthpa-cv` (25s, model CV) và `prosmarthpa-cv-w5/w10/w15/w20/w30`; `PROSMART_MODELS=cv`, `run_info.json` ghi `prediction_window_sec`, `prophet_models`. 6 window × run 1–3, riêng 25s thêm run 4–5 (20 lần, ~7 giờ). So sánh `--prophet-cv` → `comparison_prophet_cv`. **Luật chạy bổ sung:** window nào có trung bình chỉ số (Overutilization, Underprovision, Overprovision) chênh với 25s dưới 10% thì chạy thêm run 4–5 cho window đó. Kiểm định: Kruskal-Wallis trên 6 window + xu hướng theo từng số thứ tự lần chạy; không kiểm định từng cặp (3 lần: p nhỏ nhất 0,10) | Dừng lúc 19:10 sau 13/20 lần (tất cả đạt `check_run`), vì phát hiện bug vượt quota ở dòng dưới. Lần chạy dở: `prosmarthpa-cv-w5\_aborted_run3_20261112-1910` |
| 12/11 | **Bug: ProSmart HPA chạy vượt quota.** Ở pha giữ tải (t > 300 s), 2R-20% (quota 2540m = 22 pod): K8s 19–21 pod, Smart HPA 22–24 pod, không bao giờ vượt; mọi lần ProSmart vượt quota 100% thời gian: model đầu 28.7–30.6 pod, model tác giả 24.0, model CV 29.2–32.4. Nguyên nhân (log `controller.out.log` prosmarthpa-cv run1): PROPHET dự đoán PmaxR currencyservice = 8 suốt lần chạy, nhưng bước cân bằng (tự thêm, bài không nói cách xử lý khi không service nào thừa) cắt nó xuống 2–4 dù đang chạy 7 pod; Algorithm 4 dòng 19–20 gặp PmaxR < CR thì "No Scale" nên 7 pod giữ nguyên, trong khi frontend nhận phần quota đó và scale lên thật. Hệ quả: Supply +20.7% so với Smart (bài +2.17%) và Underprovision của ProSmart (cột E ghi PmaxR thấp hơn số pod thật) không so được. Ngoài ra `window_sensitivity.py`: đổi window 5→30s chỉ đổi PDR rất ít (frontend +0.48, currencyservice +0.14 replica trong pha tăng tải, thực tế tăng +1.94, +1.13 sau 25s) | Sửa `prosmart_hpa.py` (giữ nguyên dòng 19–20 của bài): (1) `committed()` = số pod service giữ lại sau Execute (CR, hoặc PDR nếu scale down); PmaxR không bao giờ thấp hơn mức này, cả ở dự đoán PROPHET lẫn hai bước cân bằng, nên quota chỉ được chuyển khi pod thật được giải phóng; (2) PDR < minR (PROPHET ra 0 với service rảnh) lấy minR, nếu không service đang giữ quota sẽ "No Scale" mãi. Kiểm tra: `prosmarthpa	est_quota_invariant.py` (20.000 vòng ngẫu nhiên): code cũ vượt quota 15.408 vòng, code mới 0. Chốt chặn: `check_run.py` báo QUOTA (exit 2) nếu pod vượt quota > 5% số vòng, `run_batch.ps1` dừng ngay không chạy lại. Bằng chứng: `prosmarthpa\quota_check.py` → `comparison_prosmart_figs\quota_check.csv`. Toàn bộ kết quả ProSmart trước bản sửa (prosmarthpa, prosmarthpa-authors, prosmarthpa-cv*) cần chạy lại (đã chuyển vào `resultsR-20\_quota_bug_20261112\`). Chạy thử trên cluster (prosmarthpa-cv run0): lần 1 hỏng vì paymentservice OOMKilled (128Mi, cùng pod chạy ~5h) và metrics-server mất số liệu ~1 phút; sửa: reset trong `run_experiment.ps1` xoá pod dùng ≥ 75% giới hạn RAM, `config.py` thử lại kubectl 20 × 3 s. Lần 2 đạt: 23 pod (2470m), 0% thời gian vượt quota |
| 12/11 | **Bước 2 xong (22:05): prosmarthpa-cv (bản sửa), 25 s, run 1–5, cả 5 lần qua check_run (gồm kiểm tra quota).** Pha giữ tải: 22.0–23.4 pod, 0% thời gian vượt quota (`quota_check.csv`). Fig. 8 (tổng ứng dụng, trung bình 5 lần, `make_prosmart_figs.py` → `fig8_services_cv.csv`): ProSmart so Smart HPA: Supply −0.2% (bài báo +2.17%), Overutilization −27.9% (−25.4%), Underprovision −18.7% (−25.34%), Overprovision −7.9% (−28.24%): cùng chiều cả 4. Theo từng lần: Overutilization ProSmart 438–544 so Smart 622–684, Underprovision 3462–4496 so 4683–5648, không chồng nhau; Overprovision 64–82 so 70–86, chồng nhau. ProSmart so K8s HPA: Supply +12.3% (+20.75%), Overprovision −81.7% (−86.43%) cùng chiều; Overutilization +3.2% (−25.73%), Underprovision +13.1% (−26.73%) ngược chiều, vì trên lab K8s HPA đã thấp hơn Smart HPA ở hai chỉ số này (K8s 458–470 / 3682–3758). Tiếp: bước 3 (5 window × run 1–3) và bước 4 (model tác giả × run 1–5) chạy qua đêm, deadline 05:50 |
| 13/11 | **Bước 3 + 4 xong qua đêm (22:05 → 05:09), 20/20 lần qua check_run, không lần nào phải chạy lại.** Quota: cả 20 lần 22–24 pod, 0% thời gian vượt (`quota_check.csv`). Số theo từng lần: `prosmarthpa\window_stats.py` → `window_stats_runs.csv`. **Fig. 9 (window 5/10/15/20/25/30 s, n = 3/3/3/3/5/3), Overutilization ứng dụng:** 419 / 443 / 458 / 417 / 479 / 506 %. Bài báo có đáy ở 25 s (347.65 → 284.62 → 317.56); lab không có hình chữ U, 25 s gần tệ nhất. Kruskal-Wallis giữa 6 window: Supply p = 0.19, Overutilization p = 0.14, Underprovision p = 0.27 (không khác); Overprovision p = 0.035 (giảm dần từ 110 ở 5 s xuống ~72–76 ở 20–30 s), nhưng 4 phép thử thì Bonferroni cần p < 0.0125. Khớp với phát lại offline (`window_sensitivity.py`): window gần như không đổi dự đoán vì chỉ ds dịch theo window, các biến hồi quy lấy tại t. Lưu ý: 25 s chạy 20:18–22:05, các window khác chạy qua đêm (xen kẽ theo run). **Fig. 8 với model tác giả (prosmarthpa-authors, bản sửa, run 1–5):** so Smart HPA: Supply +3.9% (bài báo +2.17%), Overutilization −43.1% (−25.4%), Underprovision −32.3% (−25.34%), Overprovision +254% (−28.24%, ngược chiều: adservice giữ 2 pod 200m gần như rảnh, Smart HPA chỉ 78m); so K8s HPA: Supply +16.9% (+20.75%), Overutilization −18.6% (−25.73%), Underprovision −5.8% (−26.73%), Overprovision −29.6% (−86.43%): **cùng chiều cả 4**. Model CV chỉ cùng chiều 2/4 so K8s. Dải từng lần (tác giả): Overutilization 369–397, Underprovision 3402–3779, Supply 2500–2504. Các lần tác giả cũ (dính bug) đã chuyển vào `_quota_bug_20261112\prosmarthpa-authors\` |
| 14/11 | **Báo cáo mục 5.3 viết lại theo kết quả 12–13/11.** `prosmarthpa\make_report_sidebyside.py` cắt Fig. 5/8/9 từ PDF bài báo (Fig. 8, 9 là vector, cắt từng ô ở 300 dpi) và đặt cạnh ô của nhóm, cùng màu từng service (lấy từ legend bài báo): `fig5_sidebyside.png`, `fig8_sidebyside.png`, `fig9_sidebyside.png`, `sidebyside_trend.csv`, `sidebyside_fig9.csv`, `pod_ready_lag.csv`. `make_comparison.py --prophet-cv` thêm cột prosmarthpa-authors. Báo cáo: 5.3.1 sửa lỗi quota, 5.3.2 Fig. 5 (Hình 5.7), 5.3.3 Fig. 8 (Bảng 5.5, 5.6, Hình 5.8), 5.3.4 Fig. 9 (Hình 5.9, Bảng 5.7), 5.3.5 tóm tắt; bỏ Bảng 5.5–5.7, Hình 5.7 cũ (dính bug); Hình 5.4 thay bản chỉ K8s/Smart; Bảng 7.1, Hình 7.1 (C1) thay số ProSmart mới; sửa 1.2, 1.3, 4.3, Bảng 4.3, 4.4, W7, W8, 8.1, 8.2, 9, Phụ lục A (62 lần chạy hợp lệ) | Model tác giả cùng chiều bài báo 7/8 so sánh của Fig. 8 (lệch: Overprovision so Smart, adservice giữ 2 pod, 201/275m); model nhóm 5/8. ARM với model tác giả chuyển quota ở giây 10–11, maxR cố định từ giây 32–45. Fig. 5: dữ liệu trong hình bài báo tới 12 replica, file .pkl 1–9 → hình không vẽ từ model công bố. Pod sẵn sàng ≤ 15 s ở 25/25 lần scale up (Smart HPA) |
| 14/11 (2) | **Giải thích độ lớn khác bài báo + bảng đánh đổi.** `make_report_sidebyside.py` đọc số của bài báo từ hình vector (Fig. 8, 9 lưu từng khối màu là hình chữ nhật; thang từ baseline nhãn trục): `paper_fig8_values.csv`, `paper_fig9_values.csv`, khớp số in trong bài (284,62; 347,65; 317,56; 2.479,64; lệch ≤ 0,1%), `paper_vs_ours_by_service.csv`, `paper_vs_ours_fig9_overutil.csv`. `smarthpa\make_tradeoff.py` → `results	radeoff	radeoff.csv/.md`; `make_flapping.py --prophet-cv`. Báo cáo: 5.3.3 thêm “Vì sao con số tuyệt đối khác bài báo” + Bảng 5.7 (Overutilization theo service), bảng window thành 5.8, bảng nhất quán thành 5.9; mục mới 8.2 Đánh đổi, mỗi loại theo khuôn “là gì → bảng → nhận xét”: 8.2.1 tài nguyên (Bảng 8.1), 8.2.2 flapping và chuyển quota (8.2), 8.2.3 request lỗi (8.3, từ Aggregated của locust_stats), 8.2.4 chỉ số CPU bài báo xấu đi (8.4), 8.2.5 chi phí riêng ProSmart (8.5: dữ liệu train, sai số, adservice, chu kỳ vòng điều khiển từ Knowledge Base), 8.2.6 tổng hợp (8.6); hạn chế thành 8.3; thêm ý vào 1.3 và 9; Phụ lục A thêm `make_tradeoff.py` (51 trang) | Overutilization cao hơn bài báo không do cách tính (cùng định nghĩa `Results_Analysis.py` của tác giả): checkout, payment, cart chiếm 78/93 điểm chênh (ProSmart), 64/81 (K8s), 74–113 ở mọi window; paymentservice trên cluster tác giả gần như không tải (3m ở K8s, 98m ở Smart) so với 345–380m. Đánh đổi: 2R-20% +12–17% CPU đổi p95 −13–40%, req/vCPU −0,6 đến −7,7%, flapping ≤ 0,6; 5R-50% Smart +43% CPU, flapping 9/lần, req/vCPU −27% (p = 0,008), lợi ích người dùng p ≥ 0,42; tải đột biến: CPU như nhau nhưng flapping 43/lần. Request lỗi hiếm (≤ 0,17%/lần chạy) và K8s HPA cũng có (99 ở 5R-50% run 3). Chu kỳ vòng điều khiển ProSmart 1,8–2,0 s, Smart 2,6 s → PROPHET không làm chậm |
| 19/11 | **Tìm nguyên nhân ProSmart so với K8s HPA ngược bài báo ở 2R-20%.** ProSmart/K8s = (ProSmart/Smart) × (Smart/K8s). Đối chiếu code `smarthpa\` với replication package (diff): ARM giống hệt, Capacity Analyzer và 11 manager chỉ khác chỗ đọc `config.py` | Lệch gốc nằm ở **Smart HPA so với K8s HPA**: Overutilization 1,43 (bài 0,996), Underprovision 1,39 (bài 0,981); ProSmart so với Smart đã cùng chiều bài (−28%, −19%). Knowledge Base 5 lần Smart HPA: ARM chia quota ở giây 20–45 khi mới ~15–30 user (spawn 0,67/s): `currency` maxR 9–12, 7–8 service còn maxR 1, rồi **đóng băng đến 900 s**. DR của `currency` vọt 17–35 ngay sau khi scale up (CPU pod mới cao). Ở 5R-50% (Fig. 7) thứ tự cũng ngược bài: `currency` nhận quota ở giây 42–50, `frontend` ở 134–150 (bài: frontend ~1,5 phút, currency ~2 phút) |
| 19/11 | **Bằng chứng số liệu tác giả không khớp thuật toán của họ.** `prosmarthpa\evidence_authors.py` → `results\2R-20\comparison_prosmart_figs\evidence\` (`e1_rule_check`, `e2_replay`, `e3_fig8_frontend` .png/.csv, `evidence.md`). Nguồn: dữ liệu train trong 22 `.pkl` (10 lần × 181 điểm, tổng maxR = 22 mọi dòng) | **E1** (không dùng code, theo mục 3.3.2 / Algorithm 2): 102/140 trường hợp (73%) một service thiếu ≥ 1 replica trong khi service khác thừa ≥ 1 replica mà không chuyển quota trong 15 s, cả 10 lần, lần nào cũng bắt đầu ở `currency` giây 5–25. **E2**: đưa DR của tác giả qua code ARM của tác giả, maxR khớp 0,8% số dòng (currency 1%, shipping 1%). **E3**: Fig. 8 K8s HPA frontend demand 2.692,6m > mức tối đa 2.000m theo công thức của bài (maxR 2, limit 200%, ngưỡng 20%); Overutilization 147,2% cùng hình cho ~1.500m; lab 1.578,6m. Giới hạn (ghi trong `evidence.md`): `.pkl` đã lấy mẫu lại lưới 5 s nên E1 chỉ đếm replica trọn; E2 phải ước lượng CR. Kết luận nói đúng mức: số liệu công bố không sinh ra được từ code/thuật toán công bố, không nói "code sai" |
| 19/11 | **Sửa VM.** 3 VM bị tắt đột ngột khi đang chạy (sau batch 13/11, log VMware dừng ngang, còn file `.lck`) → VMware báo "virtual disk needs repair", không clone/bật được. Sao lưu 3 ổ (24,6 GB, so từng byte khớp) rồi `vmware-vdiskmanager -R`: cả 3 "successfully repaired"; xoá bản sao lưu sau khi cluster chạy ổn. Xoá 3 VM không thuộc bài (DevStack-Lab2, Controller, Compute) theo yêu cầu | Cluster: 3 node Ready, 28 pod Running. Ổ D còn trống 75 GB. Lưu ý: luôn tắt VM đúng cách (`vmrun stop soft`) trước khi tắt máy |
| 19/11 | **VM thứ 4 `exp-runner`** (clone worker1, `192.168.161.13`, 4 vCPU, 6 GB, không join k3s) để chạy Smart HPA, ProSmart và Locust ngay trong mạng ảo, không qua Windows. `setup_exp_runner.sh` (chạy bằng sudo): gỡ k3s-agent, `~/bin/kubectl` = binary k3s v1.36.5, đổi hostname, machine-id, SSH host key, IP. Python 3.12 của Ubuntu (tải Python 3.11 bị chặn) + `~/venvs/smarthpa`, `~/venvs/prosmart` đúng phiên bản gói như Windows; code ở `~/Demo`. `smarthpa\run_experiment.sh`, `run_batch.sh`: bản bash của `.ps1`, thêm `--tag` (kết quả chạy thử ở `results/<kịch bản>-<tag>`), batch tự ghi ping giữa các VM. Mật khẩu sudo của `exp-runner` đã đặt lại, lưu ngoài repo | Chạy thử ngắn (2 phút, 50 user) Smart HPA và K8s HPA: exit 0, qua `check_run`. Vòng lặp Smart HPA trên Linux 1,4 s (Windows 2–2,6 s). **Thử tắt Wi-Fi giữa batch:** SSH Windows → VM timeout, ping giữa các VM 0/778 mất, batch không bị ảnh hưởng → xác nhận các lần mất kết nối trước đây (05/10, 24/10) là do đường Windows → VM |
| 19/11 | **Chạy thử 2R-20% trên `exp-runner`, giữ nguyên thuật toán.** Chấm bằng `smarthpa\pilot_check.py`, luật chốt trước khi có dữ liệu: cả 7 chỉ số Table 1 của Smart so với K8s cùng chiều bài (Fig. 8 + mục 5.2: Supply cao hơn; Overutilization, Underprovision, Overprovision, Overutilization Time, Underprovision Time thấp hơn; Overprovision Time cao hơn; bằng nhau = không đạt) và `currency` maxR < 9, < 5 service ở maxR 1 sau giây 60. Kết quả trên VM ở `~/Demo/results/2R-20-pilot2s`, `2R-20-pilot2s-d5` (chưa chép về Windows) | Script chấm thử trên dữ liệu cũ: không đạt đúng như mong đợi. **Spawn 2 user/s** (200 user, như bài): Smart/K8s Overutilization 1,08, Underprovision 1,18, Overutilization Time 1,003 → **4/7**; `currency` maxR 7, `frontend` 5. **Thêm độ trễ 0,9 s mỗi lệnh kubectl** (`SMARTHPA_KUBECTL_DELAY_SEC`, vòng 4,8 s, mô phỏng tác giả gọi AWS qua internet): 1,31 / 1,17 → 4/7, `currency` 11, `frontend` 2. Kết quả phụ thuộc service nào vượt ngưỡng trước ở giây ~20. 600 user không thử: 60 giây đầu giống hệt spawn 2/s |
| 19/11 | **Cải tiến C4 "ARM chờ ổn định"** (của nhóm, tác giả không có): `SMARTHPA_ARM_WARMUP_SEC` trong `config.py`, `Microservice_Capacity_Analyzer.py` (trong thời gian chờ không gọi ARM, mỗi service scale trong maxR gốc như K8s HPA; mặc định 0 = bản gốc, kết quả cũ không đổi); autoscaler `smarthpa-warmup` (mặc định 120 s). Báo cáo phải tách: phần tái hiện dùng code tác giả không sửa, C4 nằm ở phần cải tiến | Run 1: hết 120 s `currency` thiếu nhiều nhất (DR 20) nên nhận quota (maxR 5) → Overutilization 1,005, Underprovision **1,21** (riêng `currency` +638/816m; Smart phục vụ thêm 10% request, p50 230 so với 410 ms nên demand đo được tăng), **4/7**. Run 2: `frontend` nhận quota (maxR 5), `currency` giữ 2 → **7/7 đạt** (Overutilization 0,81, Underprovision 0,91), giống `.pkl` của tác giả. Nguyên nhân run 1: `currency` dùng 181% CPU/pod ở giây 60–120, so với 101% ở mọi lần khác cùng 2 pod, cùng tải → chưa rõ vì sao (không có số liệu từng pod). Chưa nhất quán: 1/2 lần đạt |
| 19/11 | **Chuẩn bị chạy lại cho sạch.** `cluster_recorder.py` ghi thêm `pod_metrics.csv` (CPU, RAM / giới hạn, node, restart, tuổi từng pod, 15 s/lần; lỗi ghi là "pod metrics unavailable", `check_run` không tính). `run_experiment.sh`: reset khởi động lại toàn bộ pod (`kubectl rollout restart deployment --all`) trước cooldown, bỏ luật chỉ restart pod dùng ≥ 75% RAM. `run_experiment.ps1` chưa sửa (từ nay chạy trên VM) | Kiểm tra (chỉ đọc): nhiều pod đã sống rất lâu qua các lần chạy: checkout 48 ngày (9 lần restart), shipping 42 ngày, email và redis-cart 38 ngày → các lần chạy trước bắt đầu từ trạng thái pod khác nhau. **Tiếp theo:** chạy lại C4 (và K8s) với pod mới, xem tỉ lệ đạt; chép kết quả chạy thử từ VM về `results\` |
| 20/11 | **Batch đêm C4 với pod mới** trên `exp-runner` (19/11 23:47 → 20/11 04:52): 2R-20%, run 1–7, `k8shpa` và `smarthpa-warmup` (warmup 120 s), 200 user @ 2/s, tag `c4fresh`; mỗi lần reset đều khởi động lại toàn bộ pod. Sửa `run_experiment.sh`: `kubectl rollout restart deployment --all` báo "unknown flag: --all" (kubectl v1.36) → restart theo tên từng deployment. Kết quả và log đã chép về `results\2R-20-c4fresh`. Chấm bằng `pilot_check.py --smart=smarthpa-warmup` | 14/14 lần exit 0, không pod nào restart. **Luật chốt trước (đủ 7/7 chỉ số + cơ chế): đạt 1/7 lần** (run 3 đạt 7/7; run 1, 2, 4, 5 đạt 4/7; run 6 đạt 5/7; run 7 đạt 3/7). Theo từng chỉ số: Overutilization và Overprovision thấp hơn K8s **7/7 lần**; Supply cao hơn và Underprovision thấp hơn **6/7** (run 1 và run 7 trượt). Trung bình 7 lần, Smart/K8s: Supply 1,027, Overutilization 0,804, Underprovision 0,880, Overprovision 0,424 → **cả 4 chỉ số CPU của Fig. 8 đúng chiều bài**. Ba chỉ số thời gian trượt nhiều: Overutilization Time 3/7, Underprovision Time 1/7, Overprovision Time 1/7. Ở mọi lần, cả hai bên gần như kéo dài suốt 15 phút, chỉ chênh vài giây (trung bình 0,996 / 1,001 / 0,988; nhỏ hơn bước lấy mẫu 15 s); số liệu bài cũng chỉ chênh 1,004 / 1,01. **Cơ chế: đạt 7/7**: `currency` maxR 2 ở mọi lần (trước C4 là 7–12), `frontend` nhận quota (4–5) ở 6/7 lần, run 3 chia đều maxR 2. `pod_metrics.csv`: CPU/pod của `currency` ở giây 60–120 khoảng 100m ở cả 7 lần C4, nên hiện tượng 181% của run 1 hôm 19/11 không lặp lại. Ngược lại, **K8s run 1 và 3 có `currency` khoảng 170m/pod** (chạm giới hạn 200m), đúng 2 lần K8s có Overutilization (611, 601) và Underprovision (5166, 5022) cao bất thường so với khoảng 450–490 / 3500–3970 ở các lần khác → phương sai nằm ở baseline K8s, không phải ở C4 (độ lệch chuẩn Underprovision: K8s 653, C4 155). **Tiếp theo:** quyết định cách báo cáo các chỉ số thời gian (trong lab chúng gần như bão hoà); chưa rõ vì sao `currency` của K8s đôi khi lên 170m/pod |
| 20/11 | **So hành vi ARM và Fig. 8 theo từng service** (chỉ phân tích, không chạy): bằng chứng E4, E5 trong `results\2R-20\comparison_prosmart_figs\evidence\evidence.md`; script `prosmarthpa\arm_behaviour.py`, `prosmarthpa\fig8_per_service_check.py` | **E4:** `.pkl` của tác giả chuyển quota sớm (giây 10–15) nhưng chỉ đúng 1 replica (`email` → `frontend`/`currency`). Đưa chính DR của tác giả qua code ARM công bố lại cho chuyển lớn (`currency` maxR 3–7, đỉnh 5–8), giống lab → chỉnh tải không làm code gốc chuyển ít như `.pkl`. C4 chia quota gần `.pkl` (khoảng cách 3 so với 12–16) nhưng bằng cơ chế khác, không phải thuật toán tác giả. **E5:** cột Smart HPA của Fig. 8 **khớp Smart HPA gốc chạy ở 2 user/s** theo từng service (Supply `currency` 664 so với 673m, `frontend` 430 so với 485m; Underprovision `cart`, `checkout`, `frontend`, `productcatalog`, `recommendation`, `shipping` lệch 1–14%). Chỗ lab khác bài là **cột K8s HPA**: Underprovision của `frontend` trong bài 2.500m, vượt mức tối đa có thể 1.800m (DR ≤ 2 × 200% / 20% = 20). Nếu lấy đúng mức tối đa, chính số liệu của bài cho Smart/K8s ≥ 1,138 (bài công bố 0,981), cùng chiều với lab (1,11). C4 thì lệch xa Fig. 8 (`currency` 195 so với 664m). **Kết luận:** không sửa code. Code gốc ở 2 user/s đã tái hiện cột Smart HPA của bài; phần "Smart ≈ K8s" của bài dựa vào một giá trị K8s không thể xảy ra. **Tiếp theo (chưa chạy, chờ người dùng bảo):** Smart HPA gốc, 2R-20%, run 1–7, spawn 2/s, pod mới, cùng thư mục với K8s đêm qua để so được với nhau. Trên `exp-runner`, trong `~/Demo/smarthpa`: `tmux new -d -s batch "./run_batch.sh --pairs 2R-20%:1,2R-20%:2,2R-20%:3,2R-20%:4,2R-20%:5,2R-20%:6,2R-20%:7 --autoscalers smarthpa --spawn-rate 2 --tag c4fresh 2>&1 \| tee ~/Demo/results/batch_orig2s_$(date +%Y%m%d-%H%M).log"` (khoảng 2 giờ 40; batch tự bỏ qua `k8shpa` đã có). Sau đó chạy `pilot_check.py ../results/2R-20-c4fresh` và `fig8_per_service_check.py` (đổi đường dẫn `lab_Smart_original_2s` sang `2R-20-c4fresh/smarthpa`) |
| 20/11 | **Kế hoạch: thử 600 user đúng như bài** (chưa chạy, người dùng sẽ tự chạy hoặc bảo chạy). Bài ghi 600 user, spawn 2/s; lab đang chạy 200 user. Chỉ số là trung bình 15 phút, mà sau giây 100 tải gấp 3 nên kết quả có thể khác, dù 100 giây đầu (lúc ARM chia quota) giống 200 user. Cluster đủ sức: ở 200 user ứng dụng dùng 1,1–1,5 / 12 core, node bận nhất 0,78 / 4 core; ở 600 user ứng dụng tối đa khoảng 5 core vì bị chặn bởi `limits` và quota (ước tính); máy thật i9-12950HX 24 luồng, 32 GB, 4 VM cộng lại 16 vCPU. Theo dõi CPU của Locust trên `exp-runner` (200 user khoảng 80 request/s). **1 cặp** (K8s + Smart HPA gốc), khoảng 45 phút. Trên `exp-runner`, trong `~/Demo/smarthpa`: `tmux new -d -s batch "./run_batch.sh --pairs 2R-20%:1 --autoscalers k8shpa,smarthpa --users 600 --spawn-rate 2 --tag u600 2>&1 \| tee ~/Demo/results/batch_u600_$(date +%Y%m%d-%H%M).log"`. Chấm bằng `pilot_check.py ../results/2R-20-u600` (chỉ số CPU và Smart/K8s so với bài: Supply 1,182, Overutilization 0,996, Underprovision 0,981, Overprovision 0,189), và so từng service với Fig. 8. Nếu đúng chiều và gần % bài thì chạy thêm các cặp | |
| 20/11 | **Đối chiếu code tác giả với bài để tìm chỗ sai** (chỉ phân tích): E6, E7 trong `evidence.md`; script `prosmarthpa\arm_fix_replay.py` | **E6:** ARM có 2 chỗ khác Algorithm 2 (D1 ở dòng 24–25; D2 ở dòng 35, dùng `ARM_maxR` còn sót từ service xử lý trước). Sửa cả 2 theo bài rồi chạy lại dữ liệu tác giả: kết quả **y hệt** code công bố (khớp 0,8%, quota không hao) → không phải nguyên nhân. **E7:** script tính chỉ số trong gói ProSmart (dùng để vẽ Fig. 8) tính Overutilization = **CPU% − ngưỡng**; gói Smart HPA và lab tính = CPU%. Tính lại theo công thức ProSmart: K8s 373,6, Smart HPA gốc 2 user/s 371,3 → **0,994** (bài 383,3 / 381,6 = 0,996). Underprovision vẫn lệch (cả hai script cùng công thức; lab 1,11, bài 0,981). File tạo tải, CPU request, biến môi trường giống tác giả; image lab v0.8.1, của tác giả khoảng v0.8.0 (cùng code nghiệp vụ). `Compiled Results.xlsx` (nguồn số liệu của Fig. 8) không có trong gói. **Tiếp theo:** chạy Smart HPA gốc (7 lần) rồi ProSmart (7 lần) ở 2 user/s, pod mới, tag `c4fresh`; khi so với Fig. 8 thì tính Overutilization theo công thức ProSmart | |
| 20/11 (2) | **Tìm nguyên nhân Supply và Underprovision lệch (Smart so với K8s, Fig. 8)**, chạy thử trên `exp-runner` (giờ VM là UTC, giờ Việt Nam = UTC+7). Script mới `prosmarthpaig8_compare.py` (tính Fig. 8 đúng cách tác giả) | **E9:** Underprovision/Overprovision cột ProSHPA Fig. 8 trùng dữ liệu train trong `.pkl` của tác giả (3708/44 so với 3729/59; frontend 1392 so với 1402) → `.pkl` là dữ liệu ProSmart 25 s, không phải Smart HPA độc lập. **Supply:** chênh nằm ở cột K8s (lab chạy payment, adservice 2 pod; bài 1 pod). **E10:** đổi image sang **v0.8.0** (manifest gói Smart HPA; lab đang dùng v0.8.1 của gói ProSmart) → payment CPU 37,6% → 11,1%, Supply payment 194 → 139m (tag `v080`). **E11:** adservice lên 2 pod do Java khởi động lạnh (pod mới vọt 26–62% ở giây 25–55); thêm `--pod-warmup`/`--pod-warmup-users` vào `run_experiment.sh`, `run_batch.sh` (Locust tải trước khi chưa có autoscaler, rồi cooldown như cũ; `run_info.json` ghi thêm `pod_warmup_*`, `app_image_tag`). 50 user/120 s chưa đủ (tag `v080w`); **200 user/300 s** (tag `v080w5`) → adservice 1 pod, payment 100m; K8s Supply 2140–2148 (bài 2053), Overprovision 384–417 (bài 437). **Underprovision:** lệch hoàn toàn ở ô frontend K8s 2500m của bài (vượt mức tối đa 1800m, mâu thuẫn Overutilization frontend 147 của chính bài); bỏ frontend thì K8s lab 2674 so với bài 2590 |
| 20/11 (3) | **Smart so với K8s ở điều kiện mới** (v0.8.0, làm ấm pod, 200 user @ 2/s, thuật toán gốc, không C4), 2 cặp, chấm như Fig. 8 (Overutilization = CPU% − ngưỡng) | Smart/K8s (bài / trung bình 2 cặp): Supply +18,2 / **+15,1%**; Overutilization −0,4 / +18,6% (cặp 1 +32,2%, **cặp 2 +3,8%**); Overprovision −81,1 / **−85,6%**; Underprovision −1,9 / +18,4% (do ô frontend). ARM chốt cách chia quota trong 30 s đầu rồi đóng băng, mỗi lần một khác (currency maxR 3/7/10, trung bình 6,67; bài 6,64 pod); số pod lẻ trong bài là trung bình 10 lần → cần đủ lần chạy. **Đã loại:** VM chạy trên E-core (VM nhanh bằng máy thật); **600 user như bài** (Fig. 4: 600 user, ~235 req/s; lab 200 user = 86 req/s nhưng CPU% từng service đã bằng bài) → recommendationservice trượt liveness 1 s, CrashLoopBackOff, controller crash `int('')`; đã hủy (tag `v080w5u600`, thư mục `_failed_*`, `_aborted_*`), cluster đã dọn. **Đang chạy:** batch `v080w5b` run 3–8 (K8s + Smart gốc), bắt đầu 12:31, dự kiến xong **17:55** giờ Việt Nam → đủ 8 cặp, chấm bằng `fig8_compare.py` |
| 20/11 (4) | **Rà ProSmart trước khi chạy** (chưa chạy) | **E8 đã giải quyết:** demand trong dữ liệu tác giả đi cùng số user, không nhìn trước 25 s (frontend 1,5/4,1/13 ở giây 10/30/100; dự đoán 25 s của chính model họ 6/8/15) → là DR đo được, cột D của lab đúng. **E13 (đã sửa `prosmart_hpa.py`, biến `PROSMART_ROUNDING`, mặc định `round`; `run_info.json` ghi `prophet_rounding`):** bài không quy định làm tròn; với `ceil` (code tác giả) model capacity của tác giả cho tổng maxR 23,5 trên quota 22 (currency 3 so với 2,1 ghi nhận), model demand đẩy adservice/email/redis vượt maxR 39/94/17% (ghi nhận 2/7/0%); với `round` khớp dữ liệu tác giả. Test quota đạt. **E14:** Fig. 8 trộn 2 phiên bản ứng dụng: dữ liệu ProSmart của tác giả có payment DR 3,1 (lab v0.8.1: 4,0–4,4; v0.8.0: 1,0), cột SHPA/KHPA payment nhẹ → ProSmart chạy **v0.8.1** (manifest gói ProSmart), Smart/K8s v0.8.0; phải ghi rõ trong báo cáo. **Fig. 9:** mô phỏng với model tác giả (chỉ theo thời gian) → window 5–30 s đổi chỉ số < 0,2% → chữ U của bài không tái tạo được bằng model công bố; muốn thử phải dùng model demand có biến đầu vào (lab train) + capacity của tác giả. Chọn model tác giả cho Fig. 8 (tái tạo đúng hành vi tác giả, không có tham số lab tự chọn). Dự kiến (mô phỏng thô): so với Smart Supply +2,0%, Overutilization −25,2%; rủi ro Overprovision so với Smart và Underprovision so với K8s. **Chờ người dùng bảo chạy:** `queue_prosmart.sh` (đổi image sang v0.8.1, 8 lần `prosmarthpa-authors`, 25 s, tag `v081w5pro`), nếu chạy ngay sau batch thì xong khoảng 21:40 giờ Việt Nam |
| 20/11 (5) | **Các quyết định đã chốt (để tiếp tục ở chat mới)** | **Mục tiêu:** xu hướng và % chênh giữa các HPA giống Fig. 8 (2R-20%): Smart/K8s Supply +18,2%, Overutilization −0,4%, Underprovision −1,9%, Overprovision −81,1%; ProSmart/Smart +2,17 / −25,40 / −25,34 / −28,24%; ProSmart/K8s +20,75 / −25,73 / −26,73 / −86,43%. Làm Smart chuẩn trước, ProSmart sau. **Nguyên tắc:** không dùng C4; giữ code tác giả, chỉ sửa khi chứng minh được lab khác tác giả/bài; không chỉnh tham số để ra số; chỉ chạy khi người dùng bảo "chạy đi" (xếp lịch trước cũng phải được bảo). **Đã chốt:** (1) Smart HPA và K8s HPA chạy **image v0.8.0** + **làm ấm pod** `--pod-warmup 300 --pod-warmup-users 200`, 200 user @ 2/s (không dùng 600 user: lab quá tải). (2) Chấm Fig. 8 bằng `prosmarthpaig8_compare.py` (Overutilization = CPU% − ngưỡng; demand = cột D cho cả 3 autoscaler). (3) ProSmart dùng **model PROPHET của tác giả** (`prosmarthpa-authors`, window 25 s), làm tròn **`round`** (E13), chạy trên **image v0.8.1** (E14), cùng tải và làm ấm; 8 lần (tag `v081w5pro`). Không train lại model lab cho Fig. 8 (capacity sẽ học kiểu dồn quota của Smart). (4) **Không chạy Fig. 9** (chữ U): model tác giả chỉ theo thời gian, mô phỏng `prosmarthpa\sim_window.py` cho thấy đổi window < 0,2%; nếu sau cần bằng chứng chạy thật thì phương án rẻ: window 5 s và 30 s × 2 lần (~1 giờ 50). (5) Nếu sau ProSmart vẫn còn ô lệch: báo giảng viên kèm bảng khớp/lệch + nguyên nhân + bằng chứng (ô frontend K8s 2500m không thể có; Fig. 9 do model công bố chỉ theo thời gian; Fig. 8 trộn v0.8.0/v0.8.1; Smart chia quota khác nhau mỗi lần). **Việc tiếp theo:** (a) batch `v080w5b` (K8s + Smart gốc, run 3–8) tự chạy trên `exp-runner`, xong ~17:55 giờ Việt Nam (10:55 UTC); chép `~/Demo/results/2R-20-v080w5` về `results\` và chạy `python ..\prosmarthpaig8_compare.py --k8s "2R-20-v080w5/k8shpa/run*" --smart "2R-20-v080w5/smarthpa/run*"` (từ `results\`, venv `D:\smarthpa-venv`). (b) Khi người dùng bảo chạy ProSmart: trên `exp-runner` `tmux new -d -s qpro "~/queue_prosmart.sh > ~/queue_prosmart.log 2>&1"` (script trong repo: `scripts\queue_prosmart.sh`; chờ batch `v080w5b` xong, đổi image sang v0.8.1, chạy 8 lần), xong ~21:40. Chấm: thêm `--prosmart "2R-20-v081w5pro/prosmarthpa-authors/run*"`. (c) Sau ProSmart: đổi image về v0.8.0 nếu còn chạy Smart/K8s; soạn bảng tổng hợp báo giảng viên. Lưu ý: giờ VM là UTC; SSH Windows → node .10–.12 bị chặn, đi qua `exp-runner` (.13); dừng batch bằng Ctrl-C trong tmux không dừng tiến trình `setsid` (phải kill theo PID nhóm) |
| 20/11 (6) | **Vì sao ARM ở lab hạ productcatalog/recommendation xuống 1 pod (lý do chính khiến Overutilization, Underprovision Smart/K8s lệch)** | Sau 3/8 cặp (`fig8_compare.py`): Supply +14,0% (bài +18,2), Overprovision −86,4% (−81,1), Overutilization +23,2% (−0,4), Underprovision +25,2% (−1,9). Cách chia sau giây 60 (currency/frontend/prodcat/recom): run1 10/4/1/1, run2 7/4/**3**/1 (Overutilization 359, sát bài 382), run3 3/9/1/1; bài trung bình 6,6/4,3/**1,8/1,5** pod. **E15:** cả 5 lần prodcat/recom mất quota, ARM dùng số CPU **cũ 10–33 s** (run1 giây 30,5: 6% đo từ giây 17, 2 s sau là 32–34% = DR 2; run2 recom giây 28,7: 6%, sau là 36%; run3 prodcat giây 32,8: 1% đo từ giây 0, 2,4 s sau là 50% = DR 3). Quyết định lớn xảy ra khi pod mới của currency/frontend có số đo (~13 s sau lần scale đầu ở giây 17); lúc đó số của prodcat/recom chưa cập nhật nên chúng bị coi là thừa; sau đó cách chia đóng băng. **Không phải lỗi lab:** metrics-server v0.9.0 `--metric-resolution=15s` (chuẩn, như EKS); pod sẵn sàng ≤ 15 s (bài ghi ~15 s); code ARM/Monitor giống tác giả; làm chậm controller giống tác giả (`--kubectl-delay 0.9`, vòng 4,8 s, lần `pilot2s-d5` 19/11) vẫn mất quota ở giây 32,3 với số cũ 13%/6%. Phụ lục online của tác giả (figshare 28028417) chỉ là hình (= cột SHPA/KHPA Fig. 8), không có dữ liệu thời gian. → Kết quả phụ thuộc pha cập nhật số đo quanh giây 30, ngẫu nhiên mỗi lần; việc hợp lệ còn lại là đủ 8 cặp rồi so tỉ lệ prodcat giữ 2 pod (bài ~3/4, lab 1/3 hiện tại). Nếu vẫn thấp: báo là khác biệt thời điểm của môi trường AWS không đo được, kèm bảng 5 lần mất quota |
| 20/11 (7) | **Vận hành và file đã đổi trong phiên 20/11** | **VM:** cả 4 VM đang tắt → bật bằng `D:\Workstationmrun.exe -T ws start D:\VM\<tên>\<tên>.vmx nogui` (k3s-master, k3s-worker1, k3s-worker2, exp-runner). SSH từ Windows tới node .10–.12 bị chặn, đi qua `exp-runner` (.13). **Image:** kéo trước v0.8.0 bằng DaemonSet tạm `prepull-v080` (không cần sudo), rồi `kubectl set image deployment/<svc> server=...:v0.8.0`; cluster đang ở **v0.8.0**. **Code:** `smarthpa
un_experiment.sh` (+`--pod-warmup`, `--pod-warmup-users`, warm-up dùng spawn rate của lần đo; `run_info.json` thêm `pod_warmup_*`, `app_image_tag`, `prophet_rounding`), `smarthpa
un_batch.sh` (chuyển tiếp 2 cờ mới), `prosmarthpa\prosmart_hpa.py` (`round`), mới: `prosmarthpaig8_compare.py`, `prosmarthpa\sim_window.py`, `scripts\queue_prosmart.sh` (cũng ở VM `~/queue_prosmart.sh`, chưa chạy). **Các tag kết quả:** `2R-20-v080` (K8s v0.8.0, không làm ấm, 2 lần), `2R-20-v080w` (làm ấm 50 user/120 s: K8s 1, Smart 1, không so được), `2R-20-v080w5` (chính thức: làm ấm 200/300 s, run 1–8 đang chạy), `2R-20-v080w5u600` (hủy), `2R-20-pilot2s-d5` (chép về từ VM). **Sự cố:** lệnh dừng batch có `pkill -f` khớp chính shell → đã dừng trước khi chạy, dùng script `~/switch_batch.sh`; Ctrl-C trong tmux không dừng tiến trình `setsid` (Locust/controller/recorder) → phải kill theo PID nhóm, xóa HPA, scale về 1. **Ghi nhớ:** giờ VM là UTC (Việt Nam = UTC+7). Ảnh Fig. 4 của bài trích từ PDF (raster), Fig. 8/9 đọc từ hình vector (`paper_fig8_values.csv`, `paper_fig9_values.csv`) |
| 20/11 (8) | **Tìm nguyên nhân L11 (Supply K8s dư so với bài)** trong lúc batch `v080w5b` chạy (lúc 07:00 UTC đang Smart run4), chỉ đọc dữ liệu, không `exec` vào pod đang đo | **Theo service, 3 cặp K8s v080w5:** dư thực sự là adservice +52 (run2/3 lên 2 pod ở giây ~130) và redis-cart +37; email **không** dư (121 so với bài 138; chỉ run1 lên 2 pod) → ghi chú L11 cũ (dựa trên run1) chưa đúng. **Cơ chế chung (cũng có ở bài, vd. cart 387 = 387):** redis/email/cart có pod thứ 2 luôn rỗi 2–5m vì client giữ kết nối cố định (gRPC HTTP/2; cartservice 1 kết nối Redis) → CPU TB chia đôi, HPA không hạ lại. Nên chỉ cần 1 mẫu vượt ngưỡng là service kẹt 2 pod đến hết run. **Khác lab/bài:** redis 1 pod ở lab CPU 14–20% (ngưỡng 20%), 9/16 run K8s vượt; bài 0/10. **Image redis:** lab `redis:alpine` không ghim → 8.10.2 + 4 module tự nạp (RedisJSON, RediSearch, TimeSeries, Bloom); gói Smart HPA ghim 7.0.11, gói ProSmart ghim 7.2.3, không module (E16). Cùng loại lỗi với payment v0.8.1 (L2). **Đã viết, chưa chạy:** `scripts/redis_ab.sh` (3 pod Redis 7.0.11 / 8.10.2 / 8.10.2 bỏ module cùng node `k3s-worker1`, manifest như redis-cart, 1 client giữ 1 kết nối/đích gửi HMGET + EVALSHA của `Microsoft.Extensions.Caching.StackExchangeRedis` 7.0.8 ở 115 lệnh/s, đo cgroup `usage_usec` + metrics-server; ~10 phút; tự hủy nếu có tmux thí nghiệm). Nếu 8.10.2 nặng hơn rõ: ghim redis-cart `redis@sha256:121bac94…` (7.0.11) cho Smart/K8s, `a3e82d34…` (7.2.3) cho ProSmart, và quyết định có chạy lại 8 cặp không (8 cặp hiện tại đều Redis 8.10.2). **Ước tính tác động (3 cặp, giả sử redis 1 pod cả Smart lẫn K8s):** redis đóng góp ~0 vào Overutilization (K8s 0,1) và Underprovision (0) → Smart/K8s Overutilization +23,2% và Underprovision +25,2% **không đổi**; Supply +14,0 → +13,1% (bài +18,2), Overprovision −86,4 → −74,4% (bài −81,1), vẫn đúng chiều. Sửa redis chỉ để đúng phiên bản, không sửa được L4/L5 |
| 20/11 (9) | **Chấm tạm 6/8 cặp `v080w5`** (batch `v080w5b` đang chạy K8s run7, dự kiến xong 17:52 giờ VN). Đã chép lại run3–6 cả hai bên từ VM (bản k8shpa/run4 cũ trên Windows chép khi run đang chạy). Lệnh: từ `results\`, `python ..\prosmarthpaig8_compare.py --k8s "2R-20-v080w5/k8shpa/run*" --smart "2R-20-v080w5/smarthpa/run*" --out 2R-20-v080w5/fig8_6pairs` | Smart/K8s (bài / lab 6 cặp): Supply +18,2 / **+9,4%** ✅ chiều; Overprovision −81,1 / **−83,4%** ✅; Overutilization −0,4 / **+23,6%** ❌; Underprovision −1,9 / **+21,2%** ❌. So với 3 cặp: Supply tụt +14,0 → +9,4% vì **K8s Supply run4–6 tăng** (2239/2339/2356 so với 2117–2148): adservice TB sau giây 60 là 1,8/1,7/2,0 pod (run1–3: 1,1–1,4), redis-cart 1,9–2,0, email run5–6 1,8–1,9 → L3 (làm ấm không giữ adservice 1 pod) và L11 (redis) nặng hơn. **L5 không đỡ:** cách chia sau giây 60 (currency/frontend/prodcat/recom): run4 3/10/1/1, run5 3/11/1/1, run6 9,2/3,8/1/1; **prodcat giữ 2+ pod chỉ 1/6 lần** (run2), recom 0/6; bài TB 1,8/1,5. Các lần có Overutilization gần bài nhất vẫn chỉ run2 (359). Mọi K8s run đều 2 pod cho currency/frontend/prodcat/recom |
| 20/11 (10) | **Kiểm tra bằng chứng L4/L5 trên 6 cặp `v080w5`: chênh nằm ở cột nào, service nào** (chỉ phân tích). Script `scripts\l5_l4_persvc.py` (chạy từ `results\`, dùng `run_metrics` của `fig8_compare.py`, so với `2R-20\comparison_prosmart_figs\paper_fig8_values.csv`; cột thiếu trong hình bài = 0) | **Underprovision (L4), có bằng chứng:** Smart lab 5116 / bài 4995 (+2,4%); K8s bỏ frontend lab 2631 / bài 2590 (+1,6%); **Smart/K8s bỏ frontend: lab +18,9%, bài +17,5%** → toàn bộ chênh +21,2% so với −1,9% nằm ở **một ô** K8s frontend: lab 1591, bài 2500 (mức tối đa có thể 1800, E3/E5). **Overutilization (L5), bằng chứng chưa đủ:** cột K8s khớp (lab 372,3 / bài 383,3, −2,9%; frontend 155/147, currency 77/80); chênh nằm ở **cột Smart** (lab 460,2 / bài 381,6, +20,6%): productcatalog 127/73, recommendation 112/89, cart 58/44, shipping 22/14, frontend 72/100 (lab cho frontend nhiều pod hơn). Theo từng lần: run2 (prodcat 3 pod) 359 ≈ bài; 5 lần prodcat 1 pod 454–499 → chỉ số quyết định bởi cách ARM chia quota quanh giây 30. Đã có: cấu hình khớp bài/tác giả (metrics-server 15 s, pod start 15 s, code ARM giữ nguyên, `--kubectl-delay` không đỡ; E15), code công bố chạy trên DR của chính tác giả cũng chuyển quota lớn như lab (E4). **Chưa có:** bằng chứng trực tiếp vì sao lần chạy của tác giả giữ prodcat/recom thường hơn (không có dữ liệu thời gian của tác giả) → hiện chỉ báo được là "đã loại các nguyên nhân phía lab đo được", chưa phải chứng minh |
| 20/11 (11) | **L5: phát lại vòng điều khiển Smart HPA gốc offline, chỉ đổi pha scrape của metrics-server.** Script `scripts\l5rm_phase_replay.py` (chạy từ `results\`, ~0,5 s/lần). Giữ nguyên của tác giả: hàm `Adaptive_Resource_Manager` import thẳng từ `smarthpa\`, logic Monitor/Analyse (ceil mean millicore, DR = ceil(CR × int(cpu%)/20)), vòng chính (maxR lấy từ `ARM_saved_decision`, gọi ARM khi DR > maxR), vòng chờ `Available != Operational` làm cả iteration đứng. Mô phỏng môi trường: metrics-server 15 s, mỗi node một pha; pod có trong `kubectl top` từ lần scrape thứ 2 sau khi chạy; pod Ready sau 13 s; tải mỗi service = trung vị tổng CPU của 12 run `v080w5` (`pod_metrics.csv`), chia đều cho pod Ready, chặn ở limit (lab = helm chart Smart HPA: 200m, ad/cart 300m, redis 125m); frontend không bị chặn 580m. Chấm như `fig8_compare.py`. 300 lần mỗi biến thể; CSV: `resultsR-20-v080w5\l5_phase_{strict,fixed,random,random_noise}.csv` | **`--strict` (chỉ 3 pha node thay đổi; controller lệch 0, pod mới round-robin, không nhiễu):** productcatalog giữ ≥ 2 pod ở **57%** số lần, recommendation 61%; **Overutilization 336–504** (p10 339, trung vị 370, p90 466). Giữ prodcat: TB **354**; mất prodcat: TB **448** → khớp lab thật (run2 giữ prodcat 359; 5 lần mất 454–499) và bao cả số bài (SHPA 382). Thêm lệch controller + node pod mới ngẫu nhiên (`fixed`): 328–504; thêm vị trí pod ban đầu ngẫu nhiên (`random`): 311–526, giữ prodcat 50%; thêm nhiễu CPU 10%: 295–526, 49%. Supply mô phỏng 2419–2429 (lab Smart 2432), Underprovision 5183–5242 (lab 5116) → mô hình tải sát lab. **Kết luận:** cùng code tác giả, cùng tải, chỉ đổi pha scrape (do môi trường quyết định, nhóm không điều khiển) đã đủ đẩy Overutilization từ mức bài sang mức lab; so với K8s lab 372: giữ prodcat −4,8%, mất prodcat +20%. **Giới hạn (phải ghi khi báo):** (1) mô phỏng chưa tái tạo `currency` 7–10 pod như run1/2/6 thật (mô phỏng 2–6, chủ yếu 2–4; tải currency thật có đỉnh lúc khởi động mà trung vị làm mất); (2) tỉ lệ giữ prodcat là của mô hình, không suy ra được tỉ lệ thật của lab (1/6) hay của tác giả; với p = 0,57, xác suất ≤ 1/6 lần là 5,7%, nên lab có thể còn yếu tố khác làm mất prodcat thường hơn. Bằng chứng này chứng minh **độ nhạy theo pha**, không chứng minh tác giả có pha nào |
| 20/11 (12) | **So trước/sau các lần sửa, theo từng cột Fig. 8** (chấm bằng `fig8_compare.py`, demand cột D). A = ban đầu (0,67 user/s, v0.8.1, `2R-20`, 5 cặp); B = spawn 2/s, v0.8.1 (K8s `c4fresh` 7 lần, Smart `pilot2s*` 2 lần); C = v0.8.0 + làm ấm 200/300 s (`v080w5`, 7 cặp) | Cột K8s (Supply / Overutil / Overprov / Underprov; bài 2053 / 383 / 437 / 5090): A 2141 / 333 / 391 / 3728; B 2368 / 374 / 225 / 4166; **C 2225 / 368 / 367 / 4174**. Cột Smart (bài 2427 / 382 / 83 / 4995): A 2409 / 504 / 78 / 5188; B 2441 / 403 / 81 / 4424; **C 2436 / 464 / 61 / 5040**. Smart/K8s Overutil A +51,2 → B +7,9 → C +26,1% (bài −0,4); Underprov +39,2 → +6,2 → +20,7% (bài −1,9). **Đọc:** các lần sửa nhắm cột K8s (phiên bản app, Java khởi động lạnh, tốc độ spawn), không nhắm 2 ô ❌; cột K8s C khớp Overutil (−4%), Smart C khớp Supply (+0,4%) và Underprov (+0,9%). B có tỉ lệ đẹp hơn nhưng sai lý do: K8s bị thổi phồng (payment v0.8.1, adservice lạnh: Supply 2368, Overprov 225 so với bài 437) và chỉ 2 lần Smart. 2 ô ❌ còn lại: Underprov do ô K8s frontend 2500 không thể có (L4), Overutil do cột Smart (464 so với 382, ARM chia quota, L5) |
| 20/11 (13) | **Batch `v080w5b` xong (10:53 UTC = 17:53 VN): đủ 8 cặp**, 16/16 lần "Run check passed", không chạy lại. Đã chép về `resultsR-20-v080w5` (cả `comparison\`, `batch_v080w5b_20261120-0531.log`, `ping_20261120-0531.csv`). Chấm: `fig8_compare.py ... --out 2R-20-v080w5/fig8_8pairs` | Smart/K8s (bài / lab 8 cặp): Supply +18,2 / **+9,9%** ✅; Overutilization −0,4 / **+23,5%** ❌; Overprovision −81,1 / **−83,5%** ✅; Underprovision −1,9 / **+20,7%** ❌. Overutilization K8s 378/346/364/362/371/413/340/331 (TB 363, bài 383); Smart 499/359/481/454/491/476/484/341 (TB 448, bài 382). Smart run8 chia currency 5 / frontend 4 / **prodcat 4** / recom 1 → Overutil 341. Prodcat giữ ≥ 2 pod **2/8 lần** (run2, run8) = đúng 2 lần Overutil thấp nhất |
| 20/11 (14) | **L5: phát lại với đường tải riêng của từng lần chạy + lỡ scrape** (`scripts\l5rm_phase_replay.py --traces ... --strict [--p-miss 0.16]`, 40 pha × 8 đường tải × 2 biến thể, ~3 phút/biến thể). Đường tải = tổng millicore controller thấy trong Knowledge Base của chính lần đó (CPU% × CR × request, mỗi lần đổi giá trị = 1 điểm, đặt lùi 7,5 s). **Lỡ scrape:** đo trên KB 7 cặp, khoảng giữa 2 lần số đo đổi giá trị: p10 14,0 s, trung vị 15,2 s, **p90 29,9 s, 16% > 20 s** (vd. k8s run2 prodcat đổi ở 12,9 rồi 43,0 s, đúng lúc ARM chia quota) → mô phỏng: mỗi lần scrape có 16% không cập nhật giá trị của pod. CSV: `resultsR-20-v080w5\l5_trace_miss0.csv`, `l5_trace_miss16.csv`, `l5_trace_run8_miss{0,0.16}.csv` | **Currency khớp theo từng lần:** lần thật currency 9–10 pod (run1/6/7) → mô phỏng currency ≥ 7 ở 68–98% số pha; lần thật 3 pod (run3/4/5) → 2–30% → việc currency giành quota do đường tải của lần đó. **Overutilization TB mô phỏng 443 (không lỡ) / 454 (lỡ 16%), lab 448.** **Cùng đường tải, cùng code, chỉ đổi pha: 7/8 đường tải cho cả Overutil ≤ 382 (mức bài) lẫn ≥ 454 (mức lab)**; khoảng mỗi đường tải rộng 120–245 (vd. run6 272–503, run4 346–623); riêng run5 không xuống ≤ 382 (min 388–403). **Còn lệch:** mô phỏng giữ prodcat 64% / 57% số pha, lab 2/8 → P(≤ 2/8) = 3,0% / 6,7%; lỡ scrape giải thích một phần. **Kết luận dùng được:** với điều kiện lab, code tác giả cho Overutil Smart TB ~450 (đúng như lab đo); muốn ra 382 như bài cần môi trường có pha/độ trễ số đo thuận lợi hơn — khác biệt môi trường, không phải code nhóm. Không chứng minh được pha của tác giả |

---

## 15. Tài liệu tham khảo

- Bài báo: https://doi.org/10.1016/j.jss.2025.112390
- Replication package ProSmart HPA: https://github.com/HussainAhmad05/ProSmart_HPA
- Replication package Smart HPA: https://doi.org/10.6084/m9.figshare.25393408
- Bài Smart HPA gốc (ICSA 2024): https://doi.org/10.1109/ICSA59870.2024.00013
- Figure chi tiết (online appendix): https://doi.org/10.6084/m9.figshare.28028417
- Online Boutique: https://github.com/GoogleCloudPlatform/microservices-demo
- k3s: https://docs.k3s.io
- Locust (bao gồm LoadTestShape): https://docs.locust.io
- Kubernetes HPA: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/  