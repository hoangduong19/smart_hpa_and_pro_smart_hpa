"""Slide-ready evidence figures that follow the questions a reader asks while looking at Fig. 8:
  01 Fig. 8 paper vs lab (which bars differ)  ->  02 the 12 comparisons, which ones differ, which figure explains each
  03.. one figure per differing cell: header = the cell (paper % vs lab %), one chart, one sentence "why".
Inputs are CSVs written by the analysis scripts (re-run those first):
  pro_persvc.py          -> 2R-20-v081w5pro/pro_persvc_8runs.csv     (lab vs paper per column / service / metric)
  pro_vs_authors_pkl.py  -> 2R-20-v081w5pro/pro_vs_authors_pkl.csv   (lab ProSmart vs authors' recorded data)
  l12_l13_cpu_per_req.py -> 2R-20-v081w5pro/l12_l13_cpu_per_req.csv  (CPU per request, ramp share)
  l5rm_phase_replay.py   -> 2R-20-v080w5/l5_trace_miss16.csv         (Smart HPA replay over scrape phases)
Run from Demo/results:  python ../scripts/make_evidence_figs.py   -> 2R-20-v081w5pro/evidence_figs/*.png
"""
import glob, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, "../prosmarthpa")
from fig8_compare import app_totals

OUT = "2R-20-v081w5pro/evidence_figs"; os.makedirs(OUT, exist_ok=True)
for f in glob.glob(f"{OUT}/*.png"):
    os.remove(f)
LAB, PAPER, REF = "#2a78d6", "#eb6834", "#52514e"   # validated categorical slots 1-2; reference ink
INK, MUTED, GRID, BAD, BAD_BG = "#0b0b0b", "#52514e", "#e6e5e1", "#b3261e", "#fbe9e7"
GOOD = "#1e7b34"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.8,
                     "axes.axisbelow": True, "figure.dpi": 150, "savefig.bbox": "tight", "legend.frameon": False})
SHORT = {"adservice": "ad", "cartservice": "cart", "checkoutservice": "checkout", "currencyservice": "currency",
         "emailservice": "email", "frontend": "frontend", "paymentservice": "payment",
         "productcatalogservice": "prodcat", "recommendationservice": "recom", "redis-cart": "redis",
         "shippingservice": "shipping"}
ORDER = list(SHORT)
COLS = {"KHPA": "K8s HPA", "SHPA": "Smart HPA", "ProSHPA": "ProSmart HPA"}
MET = {"supply": "Supply CPU (m)", "overutil": "CPU Overutilization", "overprov": "CPU Overprovision (m)",
       "underprov": "CPU Underprovision (m)"}

P = pd.read_csv("2R-20-v081w5pro/pro_persvc_8runs.csv")
A = pd.read_csv("2R-20-v081w5pro/pro_vs_authors_pkl.csv").set_index("service")
C = pd.read_csv("2R-20-v081w5pro/l12_l13_cpu_per_req.csv").set_index("service")


def cell(metric, column):
    d = P[(P.metric == metric) & (P.column == column)].set_index("service").loc[ORDER]
    return d.lab, d.paper


TOT = {(m, c): tuple(x.sum() for x in cell(m, c)) for m in MET for c in COLS}   # (lab, paper)
pct = lambda a, b: 100 * (a / b - 1)


def ratio(m, x, y):
    (lx, px), (ly, py) = TOT[(m, x)], TOT[(m, y)]
    return pct(px, py), pct(lx, ly)


def header(fig, question, paper_v, lab_v, answer):
    """Top band: the Fig. 8 cell being explained (what the lecturer points at), then the one-sentence answer."""
    h = fig.get_size_inches()[1]
    lines = answer.count("\n") + 1
    y = 1.0
    fig.text(0.01, y, answer, ha="left", va="bottom", fontsize=11.5, color=INK, linespacing=1.45)
    y += (lines * 0.25 + 0.12) / h
    fig.text(0.01, y, f"Ô lệch ở Fig. 8: {question}   ·   bài {paper_v}   ·   lab {lab_v}", ha="left", va="bottom",
             fontsize=13, fontweight="bold", color=BAD,
             bbox=dict(boxstyle="round,pad=0.45", fc=BAD_BG, ec="none"))


def source(fig, text, y=-0.05):
    fig.text(0.01, y, "Nguồn: " + text, ha="left", fontsize=8.5, color=MUTED)


def label(ax, b, text, color=INK, inside=False):
    ax.annotate(text, (b.get_x() + b.get_width() / 2, b.get_height()), ha="center",
                va="top" if inside else "bottom", xytext=(0, -3 if inside else 2), textcoords="offset points",
                color="white" if inside else color, fontsize=10, fontweight="bold" if inside else "normal")


def pair_bars(ax, labels, lab, paper, lab_name="Lab", paper_name="Bài (Fig. 8)", fmt="{:.0f}", label_idx=()):
    x = range(len(labels)); w = 0.38
    b1 = ax.bar([i - w / 2 - 0.01 for i in x], lab, w, color=LAB, label=lab_name)
    b2 = ax.bar([i + w / 2 + 0.01 for i in x], paper, w, color=PAPER, label=paper_name)
    for i in label_idx:
        for b, v, ha, dx in ((b1[i], lab[i], "right", 1), (b2[i], paper[i], "left", -1)):
            ax.annotate(fmt.format(v), (b.get_x() + b.get_width() / 2 + dx * b.get_width() / 2, b.get_height()), ha=ha,
                        va="bottom", fontsize=10, color=INK, xytext=(0, 2), textcoords="offset points")
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, rotation=30, ha="right", rotation_mode="anchor")
    ax.set_ylim(0, max(max(lab), max(paper)) * 1.25)
    ax.legend(loc="upper left", ncol=2)
    return b1, b2


# ============================================================ 01: Fig. 8 paper vs lab, totals per autoscaler
fig, axs = plt.subplots(1, 4, figsize=(15, 4))
for ax, m in zip(axs, MET):
    lab = [TOT[(m, c)][0] for c in COLS]; pap = [TOT[(m, c)][1] for c in COLS]
    x = range(3); w = 0.38
    b1 = ax.bar([i - w / 2 - 0.01 for i in x], lab, w, color=LAB, label="Lab")
    b2 = ax.bar([i + w / 2 + 0.01 for i in x], pap, w, color=PAPER, label="Bài")
    for bs, vs in ((b1, lab), (b2, pap)):
        for b, v in zip(bs, vs):
            ax.annotate(f"{v:.0f}", (b.get_x() + b.get_width() / 2, v), ha="center", va="bottom", fontsize=8.5,
                        color=INK, xytext=(0, 1), textcoords="offset points")
    ax.set_xticks(list(x)); ax.set_xticklabels(["K8s", "Smart", "ProSmart"])
    ax.set_title(MET[m], loc="left", fontsize=11, color=INK); ax.set_ylim(0, max(lab + pap) * 1.18)
axs[0].legend(loc="upper left", ncol=2)
fig.text(0.01, 1.08, "Fig. 8 (2R-20%): bài báo và lab, tổng 11 service", fontsize=14, fontweight="bold", color=INK)
fig.text(0.01, 1.0, "Lab = TB 8 lần mỗi autoscaler, cùng code tác giả, cùng load script. Hình sau chỉ ra 4 so sánh lệch chiều và hình giải thích từng ô.",
         fontsize=10.5, color=MUTED)
source(fig, "K8s, Smart: 2R-20-v080w5 (v0.8.0); ProSmart: 2R-20-v081w5pro (v0.8.1, model PROPHET tác giả); bài: Fig. 8 đọc từ hình vector; prosmarthpa/fig8_compare.py", -0.06)
fig.savefig(f"{OUT}/01_fig8_bai_vs_lab.png"); plt.close(fig)

# ============================================================ 02: the 12 comparisons
ROWS = [("supply", "SHPA", "KHPA", "09"), ("overutil", "SHPA", "KHPA", "05"), ("overprov", "SHPA", "KHPA", ""),
        ("underprov", "SHPA", "KHPA", "04"),
        ("supply", "ProSHPA", "SHPA", ""), ("overutil", "ProSHPA", "SHPA", ""), ("overprov", "ProSHPA", "SHPA", "06"),
        ("underprov", "ProSHPA", "SHPA", "08"),
        ("supply", "ProSHPA", "KHPA", "09"), ("overutil", "ProSHPA", "KHPA", "08"), ("overprov", "ProSHPA", "KHPA", "06"),
        ("underprov", "ProSHPA", "KHPA", "07")]
fig, ax = plt.subplots(figsize=(13, 6.2)); ax.axis("off"); ax.grid(False)
hdr = ["Chỉ số", "So sánh", "Bài", "Lab", "Chiều", "Giải thích"]
xs = [0.0, 0.25, 0.47, 0.57, 0.68, 0.79]
yy = 0.95
for x, t in zip(xs, hdr):
    ax.text(x, yy, t, fontsize=11, fontweight="bold", color=MUTED, transform=ax.transAxes)
step = 0.075
for k, (m, x_, y_, figno) in enumerate(ROWS):
    yy = 0.95 - step * (k + 1)
    p, l = ratio(m, x_, y_)
    same = (p > 0) == (l > 0)
    far = abs(l - p) > 5
    if not same:
        ax.add_patch(plt.Rectangle((-0.01, yy - 0.022), 1.0, step * 0.9, transform=ax.transAxes, color=BAD_BG, ec="none"))
    vals = [MET[m].replace(" (m)", ""), f"{COLS[x_].replace(' HPA', '')} so với {COLS[y_].replace(' HPA', '')}",
            f"{p:+.1f}%", f"{l:+.1f}%",
            "✗ ngược" if not same else ("✓ đúng, % xa" if far else "✓ đúng"),
            f"hình {figno}" if figno else "—"]
    for x, t in zip(xs, vals):
        col = BAD if (t.startswith("✗")) else (GOOD if t.startswith("✓") else INK)
        ax.text(x, yy, t, fontsize=11, color=col, transform=ax.transAxes,
                fontweight="bold" if t.startswith("✗") else "normal")
n_same = sum((ratio(m, x_, y_)[0] > 0) == (ratio(m, x_, y_)[1] > 0) for m, x_, y_, _ in ROWS)
fig.text(0.01, 1.0, f"12 so sánh của Fig. 8: {n_same} đúng chiều, {12 - n_same} ngược chiều (tô đỏ)",
         fontsize=14, fontweight="bold", color=INK)
fig.text(0.01, 0.955, "Mỗi ô lệch có một hình giải thích ngay sau. Hình 03: lab chạy code tác giả cho đúng cách chia quota của tác giả.",
         fontsize=10.5, color=MUTED)
source(fig, "% = (cột thứ nhất ÷ cột thứ hai − 1); số tổng như hình 01; prosmarthpa/fig8_compare.py", 0.02)
fig.savefig(f"{OUT}/02_bang_12_so_sanh.png"); plt.close(fig)

# ============================================================ 03: lab runs the authors' code like the authors
sl, sp = cell("supply", "ProSHPA")
a = A.loc[ORDER]
fig, axs = plt.subplots(1, 2, figsize=(13, 4.2))
pair_bars(axs[0], [SHORT[s] for s in ORDER], a.lab_maxR.tolist(), a.authors_maxR.tolist(), "Lab", "Tác giả (dữ liệu .pkl)",
          "{:.1f}", label_idx=[ORDER.index("frontend")])
axs[0].set_title("ProSmart: quota mỗi service (maxR TB, số pod)", loc="left", fontsize=11, color=INK)
pair_bars(axs[1], [SHORT[s] for s in ORDER], sl.tolist(), sp.tolist(), label_idx=[ORDER.index("frontend")])
axs[1].set_title("ProSmart: Supply CPU mỗi service (m)", loc="left", fontsize=11, color=INK)
fig.text(0.01, 1.08, "Trước hết: lab chạy code tác giả ra đúng cách chia quota của tác giả", fontsize=14,
         fontweight="bold", color=INK)
fig.text(0.01, 1.0, f"Từng service cùng số pod; tổng Supply lab {sl.sum():.0f}m, bài {sp.sum():.0f}m ({pct(sl.sum(), sp.sum()):+.1f}%). "
         "→ Các ô lệch không đến từ thuật toán, mà từ tải CPU đo được (hình 06–08).", fontsize=10.5, color=MUTED)
source(fig, "8 lần 2R-20-v081w5pro (model PROPHET tác giả); maxR tác giả = dữ liệu train model capacity; scripts/pro_vs_authors_pkl.py, pro_persvc.py")
fig.savefig(f"{OUT}/03_code_tac_gia_chay_giong.png"); plt.close(fig)

# ============================================================ 04: Underprovision Smart vs K8s  (L4)
kl, kp = cell("underprov", "KHPA"); s_l, s_p = cell("underprov", "SHPA")
p, l = ratio("underprov", "SHPA", "KHPA")
wo = lambda a_, b_: pct(a_.drop("frontend").sum(), b_.drop("frontend").sum())
fig, axs = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [1, 1.3]})
ax = axs[0]
bars = ax.bar(["Lab", "Bài"], [kl["frontend"], kp["frontend"]], 0.5, color=[LAB, PAPER])
ax.axhline(1800, color=REF, ls="--", lw=1.5)
ax.text(1.32, 1800, "Tối đa có thể\n1800m", va="center", fontsize=10, color=INK)
for b in bars: label(ax, b, f"{b.get_height():.0f}m")
ax.set_xlim(-0.5, 2.2); ax.set_title("Underprovision frontend, cột K8s HPA (m)", loc="left", fontsize=11, color=INK)
ax = axs[1]
lab_v = [l, wo(s_l, kl)]; pap_v = [p, wo(s_p, kp)]
x = [0, 1]; w = 0.36
for xs_, vals, col, nm in ((-w / 2 - 0.01, lab_v, LAB, "Lab"), (w / 2 + 0.01, pap_v, PAPER, "Bài")):
    bs = ax.bar([i + xs_ for i in x], vals, w, color=col, label=nm)
    for b, v in zip(bs, vals):
        ax.annotate(f"{v:+.1f}%", (b.get_x() + b.get_width() / 2, max(v, 0)), ha="center", va="bottom",
                    xytext=(0, 2), textcoords="offset points", color=INK)
ax.axhline(0, color=MUTED, lw=1); ax.set_xticks(x); ax.set_xticklabels(["Như Fig. 8", "Bỏ ô frontend"])
ax.set_ylim(-5, 27); ax.legend(loc="upper center", ncol=2)
ax.set_title("Underprovision Smart HPA so với K8s HPA", loc="left", fontsize=11, color=INK)
header(fig, "Underprovision, Smart so với K8s", f"{p:+.1f}%", f"{l:+.1f}%",
       "Vì sao: ô frontend của K8s trong bài (2500m) lớn hơn mức tối đa có thể (frontend 2 pod → thiếu tối đa 18 pod × 100m = 1800m).\n"
       "Bỏ riêng ô đó ra thì lab và bài cùng chiều, cùng cỡ.")
source(fig, "lab 8 cặp 2R-20-v080w5; tối đa: DR ≤ 2 pod × 200% / 20% = 20, thiếu ≤ 20 − 2 = 18 pod; scripts/pro_persvc.py (E3, E5)")
fig.savefig(f"{OUT}/04_underprov_smart_k8s.png"); plt.close(fig)

# ============================================================ 05: Overutilization Smart vs K8s  (L5)
sim = pd.read_csv("2R-20-v080w5/l5_trace_miss16.csv")
_, smart_tot = app_totals("2R-20-v080w5/smarthpa/run*", 3)
real = [t["overutil"] for t in smart_tot]
p, l = ratio("overutil", "SHPA", "KHPA")
paper_smart = TOT[("overutil", "SHPA")][1]; lm = sum(real) / len(real)
fig, ax = plt.subplots(figsize=(11, 4.2))
ax.hist(sim.overutil, bins=30, color=LAB, alpha=0.85, edgecolor="white", linewidth=1.5,
        label=f"Code tác giả, mô phỏng {len(sim)} lần")
ax.axvline(paper_smart, color=PAPER, lw=2.5)
ax.text(paper_smart, ax.get_ylim()[1] * 0.97, f" Bài {paper_smart:.0f}", color=INK, va="top", fontsize=10.5)
ax.axvline(lm, color=REF, lw=2, ls="--")
ax.text(lm, ax.get_ylim()[1] * 0.97, f" Lab TB {lm:.0f}", color=INK, va="top", fontsize=10.5)
ax.plot(real, [ax.get_ylim()[1] * 0.04] * len(real), "o", ms=9, color=INK, mec="white", mew=2, label="8 lần lab đo thật")
ax.set_xlabel("CPU Overutilization của Smart HPA"); ax.set_ylabel("Số lần mô phỏng")
ax.legend(loc="upper right", bbox_to_anchor=(1, 0.80))
header(fig, "Overutilization, Smart so với K8s", f"{p:+.1f}%", f"{l:+.1f}%",
       "Vì sao: Smart HPA chia quota một lần quanh giây 30 theo số đo CPU lúc đó; số đo cũ hay mới tùy lúc metrics-server lấy mẫu.\n"
       f"Chạy lại đúng code tác giả, chỉ đổi lúc lấy mẫu: kết quả từ {sim.overutil.min():.0f} đến {sim.overutil.max():.0f}, chứa cả mức bài lẫn mức lab.")
source(fig, "scripts/l5rm_phase_replay.py (hàm ARM import thẳng từ code Smart HPA của tác giả, tải = 8 lần lab 2R-20-v080w5)")
fig.savefig(f"{OUT}/05_overutil_smart_k8s.png"); plt.close(fig)

# ============================================================ 06: Overprovision ProSmart vs Smart  (L12)
ol, op = cell("overprov", "ProSHPA")
p, l = ratio("overprov", "ProSHPA", "SHPA"); p2, l2 = ratio("overprov", "ProSHPA", "KHPA")
ad_m = C.loc["adservice", "l2_m_ss"]
fig, axs = plt.subplots(1, 2, figsize=(13, 4.2), gridspec_kw={"width_ratios": [2.2, 1]})
pair_bars(axs[0], [SHORT[s] for s in ORDER], ol.tolist(), op.tolist(), label_idx=[ORDER.index("adservice")])
axs[0].set_title("Overprovision ProSmart mỗi service (m)", loc="left", fontsize=11, color=INK)
ax = axs[1]
ax.barh(["Tác giả", "Lab"], [60, ad_m], 0.5, color=[PAPER, LAB])
ax.errorbar([60], [0], xerr=[[20], [20]], fmt="none", ecolor=INK, capsize=5, lw=1.2)
ax.axvline(44, color=REF, ls="--", lw=1.5); ax.text(45, 0.5, "cần ≥ 44m\nđể DR = 2", fontsize=10, color=INK, va="center")
ax.annotate(f"{ad_m:.0f}m → DR 1", (ad_m, 1), xytext=(18, 0), textcoords="offset points", va="center", ha="left",
            color=INK)
ax.annotate("40–80m → DR 2", (80, 0), xytext=(4, 0), textcoords="offset points", va="center", color=INK)
ax.set_xlim(0, 120); ax.grid(axis="x"); ax.grid(axis="y", visible=False)
ax.set_title("CPU adservice (2 pod, m)", loc="left", fontsize=11, color=INK)
header(fig, "Overprovision, ProSmart so với Smart", f"{p:+.1f}%", f"{l:+.1f}%",
       f"Vì sao: cả phần lệch nằm ở một service, adservice ({ol['adservice']:.0f}m so với {op['adservice']:.0f}m); bỏ adservice: lab {ol.drop('adservice').sum():.0f}m, bài {op.drop('adservice').sum():.0f}m.\n"
       f"adservice lab dùng {ad_m:.0f}m, hơi dưới ngưỡng làm tròn 44m → demand 1 pod trong khi quota 2 pod → 1 pod bị tính là dư. (Cũng là lý do ProSmart/K8s {l2:+.0f}% thay vì {p2:+.0f}%.)")
source(fig, "8 lần 2R-20-v081w5pro; CPU lab = pod_metrics.csv sau giây 300; tác giả suy từ demand DR = 2,0 (khoảng 40–80m); DR = ceil(2 × int(CPU%) / 20)")
fig.savefig(f"{OUT}/06_overprov_prosmart.png"); plt.close(fig)

# ============================================================ 07: Underprovision ProSmart vs K8s  (L13 = L4 + ProSmart column)
p, l = ratio("underprov", "ProSHPA", "KHPA")
ul, up = cell("underprov", "ProSHPA")
pk_wo = (pct(ul.drop("frontend").sum(), kl.drop("frontend").sum()), pct(up.drop("frontend").sum(), kp.drop("frontend").sum()))
fig, axs = plt.subplots(1, 2, figsize=(13, 4.2), gridspec_kw={"width_ratios": [1, 2.2]})
ax = axs[0]
d = ul - up
items = [("Cột K8s bài:\nô frontend 2500m", kp["frontend"] - kl["frontend"]),
         ("Cột ProSmart lab:\nnặng hơn bài", ul.sum() - up.sum())]
bs = ax.bar([t for t, _ in items], [v for _, v in items], 0.55, color=[PAPER, LAB])
for b, (_, v) in zip(bs, items): label(ax, b, f"{v:+.0f}m")
ax.set_title("Hai nguồn lệch (m)", loc="left", fontsize=11, color=INK); ax.tick_params(axis="x", labelsize=9.5)
pair_bars(axs[1], [SHORT[s] for s in ORDER], ul.tolist(), up.tolist(),
          label_idx=[ORDER.index(s) for s in ("checkoutservice", "paymentservice")])
axs[1].set_title("Underprovision ProSmart mỗi service (m)", loc="left", fontsize=11, color=INK)
header(fig, "Underprovision, ProSmart so với K8s", f"{p:+.1f}%", f"{l:+.1f}%",
       "Vì sao: hai nguồn cộng lại. (1) Cột K8s của bài có ô frontend không thể có (hình 04), làm mẫu số của bài to ra.\n"
       f"(2) Cột ProSmart của lab thiếu nhiều hơn bài ở frontend, checkout, payment, prodcat, recom, vì lab tốn CPU mỗi request hơn (hình 08).")
source(fig, "8 lần ProSmart 2R-20-v081w5pro, 8 lần K8s 2R-20-v080w5; scripts/pro_persvc.py")
fig.savefig(f"{OUT}/07_underprov_prosmart_k8s.png"); plt.close(fig)

# ============================================================ 08: CPU per request (cause of L12/L13 and of the % gaps)
c = C.loc[ORDER].sort_values("cpu_per_req_ratio_l2")
med = c.cpu_per_req_ratio_l2.median()
fig, ax = plt.subplots(figsize=(12, 4.3))
bars = ax.bar([SHORT[s] for s in c.index], c.cpu_per_req_ratio_l2, 0.6,
              color=[LAB if abs(v - med) < 0.5 else ("#1a4f8f" if v > med else "#8bb8ee") for v in c.cpu_per_req_ratio_l2])
ax.axhline(med, color=REF, ls="--", lw=1.5)
ax.text(-0.4, med + 0.55, f"mức chung {med:.1f}× (đường đứt)\nlab chạy 200 user thay 600 để bù mức này", va="bottom",
        ha="left", fontsize=10, color=INK)
ax.set_ylim(0, 5)
for b, v in zip(bars, c.cpu_per_req_ratio_l2):
    ax.annotate(f"{v:.1f}×", (b.get_x() + b.get_width() / 2, v), ha="center", va="bottom", xytext=(0, 2),
                textcoords="offset points", color=INK, fontsize=9.5)
ax.set_ylabel("CPU mỗi request: lab ÷ tác giả")
ramp = 100 * c.loc["frontend", "ramp_part_l2"] / (c.loc["frontend", "l2_D_full"] - c.loc["frontend", "auth_D_full"])
p1, l1 = ratio("overutil", "ProSHPA", "KHPA"); p2, l2 = ratio("underprov", "ProSHPA", "SHPA")
header(fig, "% của các ô ProSmart (vd. Overutil ProSmart/K8s)", f"{p1:+.0f}%", f"{l1:+.0f}%",
       f"Vì sao: máy lab tốn CPU mỗi request khác máy AWS của tác giả, khác theo service; số user chỉ bù được mức chung. (Underprov ProSmart/Smart: bài {p2:+.0f}%, lab {l2:+.0f}%.)\n"
       f"Service dưới mức chung (ad) nhẹ hơn bài; trên mức chung (checkout, payment) nặng hơn bài. Ramp 5 phút so với 100 s chỉ giải thích ≤ {ramp:.0f}%.")
source(fig, "lab 8 lần 2R-20-v081w5pro sau giây 300 (pod_metrics.csv, Locust 82 req/s); tác giả: demand .pkl, ~235 req/s (Fig. 4); scripts/l12_l13_cpu_per_req.py")
fig.savefig(f"{OUT}/08_cpu_moi_request.png"); plt.close(fig)

# ============================================================ 09: Supply % (K8s column heavier than the paper)
kl_s, kp_s = cell("supply", "KHPA")
p1, l1 = ratio("supply", "SHPA", "KHPA"); p2, l2 = ratio("supply", "ProSHPA", "KHPA")
diff = (kl_s - kp_s).sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(11, 4.0))
bs = ax.bar([SHORT[s] for s in diff.index], diff.values, 0.6, color=[LAB if v > 0 else "#8bb8ee" for v in diff.values])
for b, v in zip(bs, diff.values):
    if abs(v) > 8: label(ax, b, f"{v:+.0f}m")
ax.axhline(0, color=MUTED, lw=1); ax.set_ylabel("Supply K8s: lab − bài (m)")
ax.tick_params(axis="x", rotation=30)
header(fig, "Supply, Smart/K8s và ProSmart/K8s (đúng chiều, % nhỏ hơn)", f"{p1:+.1f}%; {p2:+.1f}%", f"{l1:+.1f}%; {l2:+.1f}%",
       f"Vì sao: cột K8s của lab dùng nhiều CPU hơn bài ({kl_s.sum():.0f}m so với {kp_s.sum():.0f}m), chủ yếu ở adservice và redis-cart:\n"
       "hai service này chạy sát ngưỡng 20%, chỉ một lần vượt là pod thứ 2 bật lên và giữ đến hết lần chạy (adservice: Java khởi động chậm).\n"
       "Đã thử và loại: phiên bản Redis (cùng tải, 7.0.11 của tác giả 18,3m ≥ 8.10.2 của lab 16,5m).")
source(fig, "8 lần K8s 2R-20-v080w5; scripts/pro_persvc.py; L3 (E11), L11 (E16); Redis A/B: scripts/redis_ab.sh, results/redis_ab_20261122-0652")
fig.savefig(f"{OUT}/09_supply_k8s.png"); plt.close(fig)
print("written", sorted(os.listdir(OUT)))
