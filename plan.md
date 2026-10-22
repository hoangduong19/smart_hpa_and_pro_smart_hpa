# Bài tập lớn: Tái hiện và cải tiến Smart HPA trên cluster k3s

> **Bài báo:** H. Ahmad, C. Treude, M. Wagner, C. Szabo, *Towards resource-efficient reactive and proactive auto-scaling for microservice architectures*, Journal of Systems and Software 225 (2025) 112390. DOI: 10.1016/j.jss.2025.112390
> **Người thực hiện:** Nhóm. **Hoàng Quốc Dương** phụ trách phần demo (hạ tầng, chạy hệ thống, chạy thí nghiệm, demo khi bảo vệ)
> **Cập nhật lần cuối:** 15/10/2026
> **Trạng thái tổng:** 🟡 Giai đoạn 1–6 xong (20/20 lần chạy hợp lệ: 2R-20% 5 cặp, 5R-50% 5 cặp; lần 4–5 của 2R-20% chạy 12/10). Giai đoạn 6b ProSmart HPA xong (5/5 lần 2R-20% hợp lệ, 08/10 và 12/10). Giai đoạn 7: C1 xong phần phân tích (12/10); C3 xong (13/10 và 15/10: 5R-50% 5 lần + 3 lần đối chứng, 2R-20% 3 lần); C2 xong (19/10: 5R-50% tải đột biến, 3 cặp). Tiếp theo: báo cáo
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
| | *(tiếp theo)* chạy ProSmart 2R-20% với `.pkl` của tác giả làm đối chứng | |

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