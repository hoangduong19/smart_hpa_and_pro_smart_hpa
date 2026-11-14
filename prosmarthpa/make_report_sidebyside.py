"""Side-by-side figures for the ProSmart HPA section of the report: the paper's figure on the left, ours on the right.

The paper (Ahmad et al., JSS 2025) draws Fig. 8 and Fig. 9 as vector graphics: each of their 4 panels is cut out of the
PDF at 300 dpi and put next to the same panel drawn from our runs, one metric per row, so the trend can be read across.
Our panels use the paper's own colors per microservice (sampled from its legend) and its stacking order, so a service
has the same color on both sides.

  fig5_sidebyside.png   paper Fig. 5 (PROPHET model fit, recommendationservice) | (a) the authors' released model on
                        its own training data, (b) our model tuned by CV (models_5runs_cv) on Smart HPA run 1-5
  fig8_sidebyside.png   paper Fig. 8 (ProSHPA / SHPA / KHPA, 2R-20%, 25 s) | ProSmart with the authors' models,
                        ProSmart with our CV models, Smart HPA, K8s HPA (mean of 5 runs each)
  fig9_sidebyside.png   paper Fig. 9 (6 prediction windows) | ProSmart with our CV models per window (n = 3, 25 s n = 5),
                        hollow dots = the application total of each run
  sidebyside_trend.csv  for every Fig. 8 comparison: the paper's change, ours (both model sets), runs better, p,
                        and whether the direction matches the paper
  sidebyside_fig9.csv   per window: mean, min, max of the application total per metric, Kruskal-Wallis p across windows
  paper_fig8_values.csv, paper_fig9_values.csv   the paper's own numbers per microservice, read from the vector
                        rectangles of its Fig. 8 and Fig. 9 (checked against the values printed in its text)
  paper_vs_ours_by_service.csv   per microservice: the paper's Fig. 8 and ours, 4 metrics and the CPU demand
  pod_ready_lag.csv     every scale-up of the Smart HPA 2R-20% runs: seconds until the new pods are ready (the paper
                        sets the window from pod start-up and termination times)

Usage (prophet venv, from prosmarthpa/):  D:\\prosmart-venv\\Scripts\\python.exe make_report_sidebyside.py
Output: results/2R-20/comparison_prosmart_figs/
"""

import csv
import itertools
import statistics as st
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import pymupdf

from make_prosmart_figs import FIG5_MODELS, FIG5_SERVICE, fit_authors, fit_ours
from train_prophet import DEMO_DIR
from window_stats import kruskal

sys.path.insert(0, str(DEMO_DIR / "smarthpa"))
from make_paper_figs import INK, INK_2, SURFACE, mean_metrics, run_dirs, style_axis  # noqa: E402

PAPER = DEMO_DIR / "Towards-resource-efficient-reactive-and-proactive-auto-scaling-for-microservice-architectures.pdf"
SCENARIO_DIR = DEMO_DIR / "results" / "2R-20"
OUT = SCENARIO_DIR / "comparison_prosmart_figs"

# paper legend order = stacking order (bottom to top); colors sampled from the legend of Fig. 8 / Fig. 9
SERVICES = [("frontend", "frontend", "#7f3c8c"), ("adservice", "adservice", "#10a578"), ("cartservice", "cart", "#3869ac"),
            ("checkoutservice", "checkout", "#f1b700"), ("currencyservice", "currency", "#e63f73"),
            ("paymentservice", "payment", "#7fba59"), ("emailservice", "email", "#e5830e"),
            ("productcatalogservice", "productcatalogue", "#008694"),
            ("recommendationservice", "recommendation", "#a55626"), ("shippingservice", "shipping", "#f87b71"),
            ("redis-cart", "redis", "#a4aa98")]
APP_LINE, GOOD, BAD = "#e8231c", "#1a7f37", "#c0392b"

# panels in the paper's order; crop boxes in PDF points (x0, y0, x1, y1), measured on the rendered pages
METRICS = [("supply_cpu_m", "Supply CPU (m)", True),
           ("cpu_overutilization_pct", "CPU Overutilization (%)", False),
           ("cpu_underprovision_m", "CPU Underprovision (m)", False),
           ("cpu_overprovision_m", "CPU Overprovision (m)", False)]
FIG8_PAGE, FIG9_PAGE = 14, 15
FIG8_CROPS = [(146, 52, 293, 168), (292, 52, 443, 168), (146, 168, 293, 279), (292, 168, 443, 279)]
FIG9_CROPS = [(146, 52, 293, 174), (292, 52, 443, 174), (146, 174, 293, 296), (292, 174, 443, 296)]
FIG5_PAGE, FIG5_BOX = 11, (306, 216, 558, 334)

# Fig. 8 columns: (run folder, tick label)
FIG8_COLUMNS = [("prosmarthpa-authors", "ProSHPA\nmodel tác giả"), ("prosmarthpa-cv", "ProSHPA\nmodel nhóm"),
                ("smarthpa", "SHPA"), ("k8shpa", "KHPA")]
# change of ProSmart HPA reported by the paper (Section 5.3), sign = ProSmart relative to the other autoscaler
PAPER_CHANGE = {("smarthpa", "supply_cpu_m"): +2.17, ("smarthpa", "cpu_overutilization_pct"): -25.40,
                ("smarthpa", "cpu_underprovision_m"): -25.34, ("smarthpa", "cpu_overprovision_m"): -28.24,
                ("k8shpa", "supply_cpu_m"): +20.75, ("k8shpa", "cpu_overutilization_pct"): -25.73,
                ("k8shpa", "cpu_underprovision_m"): -26.73, ("k8shpa", "cpu_overprovision_m"): -86.43}
WINDOWS = [(5, "prosmarthpa-cv-w5"), (10, "prosmarthpa-cv-w10"), (15, "prosmarthpa-cv-w15"),
           (20, "prosmarthpa-cv-w20"), (25, "prosmarthpa-cv"), (30, "prosmarthpa-cv-w30")]

LEFT_HEAD = "Bài báo [1] (AWS EKS, 10 lần chạy)"
RIGHT_HEAD = "Nhóm (cluster k3s)"


# ---------------------------------------------------------------- helpers

def paper_crop(page, box, dpi=300):
    doc = pymupdf.open(PAPER)
    pix = doc[page - 1].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*box))
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]


def show_paper(ax, img):
    ax.imshow(img, interpolation="lanczos")
    ax.set_axis_off()


# ---------------------------------------------------------------- the paper's numbers, read from its vector figures

TICK_COLOR = (0x2a, 0x3f, 0x5f)      # axis label glyphs in the paper's figures
# tick step of each panel's y axis (read off the labels: e.g. Fig. 8 Supply 0.0, 500, 1.0k ... 2.5k)
FIG8_STEPS = [500, 100, 1000, 100]
FIG9_STEPS = [500, 100, 1000, 20]


def _rgb(color):
    return tuple(int(round(255 * v)) for v in color)


def _nearest_service(rgb):
    def dist(hexc):
        c = tuple(int(hexc[i:i + 2], 16) for i in (1, 3, 5))
        return sum((a - b) ** 2 for a, b in zip(c, rgb))
    name, _, color = min(SERVICES, key=lambda s: dist(s[2]))
    return name if dist(color) < 400 else None


def paper_values(page, crops, steps, columns):
    """Every stacked segment of the paper's bar charts: the PDF stores each one as a filled rectangle, so its height is
    exact. Scale: distance between consecutive y-axis labels = one tick step; zero = bottom of the bars.
    Returns rows (metric, column, service, value)."""
    drawings = pymupdf.open(PAPER)[page - 1].get_drawings()
    rows = []
    for (key, _, _), box, step in zip(METRICS, crops, steps):
        box = pymupdf.Rect(*box)
        bars = [(dr["rect"], _nearest_service(_rgb(dr["fill"]))) for dr in drawings
                if dr.get("fill") and dr["rect"].intersects(box) and dr["rect"].width > 8]
        bars = [(r, s) for r, s in bars if s]
        left = min(r.x0 for r, _ in bars)
        glyphs = [dr["rect"] for dr in drawings if dr.get("fill") and dr["rect"].intersects(box)
                  and _rgb(dr["fill"]) == TICK_COLOR and dr["rect"].x1 < left and dr["rect"].height < 6]
        # one label per tick; its glyphs share a baseline (y1); "500" and "1.0k" differ in height, so not the centre
        baselines = []
        for y in sorted(g.y1 for g in glyphs):
            if not baselines or y - baselines[-1] > 1.5:
                baselines.append(y)
        gaps = [b - a for a, b in zip(baselines, baselines[1:])]
        assert max(gaps) - min(gaps) < 0.3, (key, baselines)
        per_pt = step / st.mean(gaps)
        zero = max(r.y1 for r, _ in bars)
        xs = sorted({round(r.x0) for r, _ in bars})
        assert len(xs) == len(columns), (key, xs)
        for r, s in bars:
            rows.append((key, columns[xs.index(round(r.x0))], s, (r.y1 - r.y0) * per_pt))
    return rows


def paper_tables():
    """paper_fig8_values.csv / paper_fig9_values.csv: per metric, column and microservice, plus the application total.
    Checked against the numbers the paper prints in its text."""
    out = {}
    for name, page, crops, steps, columns in (("fig8", FIG8_PAGE, FIG8_CROPS, FIG8_STEPS, ["ProSHPA", "SHPA", "KHPA"]),
                                              ("fig9", FIG9_PAGE, FIG9_CROPS, FIG9_STEPS, [5, 10, 15, 20, 25, 30])):
        df = pd.DataFrame(paper_values(page, crops, steps, columns), columns=["metric", "column", "service", "value"])
        df = df.groupby(["metric", "column", "service"], as_index=False).value.sum()
        total = df.groupby(["metric", "column"], as_index=False).value.sum().assign(service="APPLICATION")
        df = pd.concat([df, total]).round(2)
        df.to_csv(OUT / f"paper_{name}_values.csv", index=False)
        out[name] = df
    app = lambda f, m, c: out[f].query("metric == @m and column == @c and service == 'APPLICATION'").value.iloc[0]
    # values printed in the paper's Section 5.3 text
    checks = [("fig8", "cpu_overutilization_pct", "ProSHPA", 284.62), ("fig8", "supply_cpu_m", "ProSHPA", 2479.64),
              ("fig9", "cpu_overutilization_pct", 5, 347.65), ("fig9", "cpu_overutilization_pct", 25, 284.62),
              ("fig9", "cpu_overutilization_pct", 30, 317.56), ("fig9", "supply_cpu_m", 5, 2474.18),
              ("fig9", "supply_cpu_m", 25, 2479.64)]
    for f, m, c, v in checks:
        got = app(f, m, c)
        print(f"paper check {f} {m} {c}: read {got:.1f}, text {v} ({100 * (got / v - 1):+.1f}%)")
    for m, other, pct in (("supply_cpu_m", "SHPA", 2.17), ("cpu_overutilization_pct", "SHPA", -25.40),
                          ("cpu_underprovision_m", "KHPA", -26.73), ("cpu_overprovision_m", "KHPA", -86.43)):
        got = 100 * (app("fig8", m, "ProSHPA") / app("fig8", m, other) - 1)
        print(f"paper check fig8 {m} ProSHPA vs {other}: read {got:+.2f}%, text {pct:+.2f}%")
    by_service(out["fig8"])
    fig9_gap(out["fig9"])
    return out


GAP_SERVICES = ["checkoutservice", "paymentservice", "cartservice"]


def fig9_gap(paper):
    """paper_vs_ours_fig9_overutil.csv: per window, CPU Overutilization of the application in the paper and ours, the
    gap, and how much of it comes from checkout, payment and cart (the services that carry more load on our cluster)."""
    p = paper[paper.metric == "cpu_overutilization_pct"]
    rows = []
    for w, a in WINDOWS:
        mm = mean_metrics(str(SCENARIO_DIR), a)[0]
        pw = p[p.column == w].set_index("service").value
        ours = sum(mm[s]["cpu_overutilization_pct"] for s, _, _ in SERVICES)
        three = sum(mm[s]["cpu_overutilization_pct"] - pw.get(s, 0) for s in GAP_SERVICES)
        rows.append({"window_sec": w, "paper": round(pw["APPLICATION"], 1), "ours": round(ours, 1),
                     "gap": round(ours - pw["APPLICATION"], 1), "gap_checkout_payment_cart": round(three, 1)})
    pd.DataFrame(rows).to_csv(OUT / "paper_vs_ours_fig9_overutil.csv", index=False)


def by_service(paper):
    """paper_vs_ours_by_service.csv: per microservice, the paper's Fig. 8 value and ours (ProSHPA = our run with the
    authors' models), for the 4 metrics and the demand behind them (supply + underprovision - overprovision)."""
    ours = {"ProSHPA": "prosmarthpa-authors", "SHPA": "smarthpa", "KHPA": "k8shpa"}
    p = paper.pivot_table(index=["column", "service"], columns="metric", values="value").fillna(0)
    rows = []
    for col, a in ours.items():
        mm = mean_metrics(str(SCENARIO_DIR), a)[0]
        for s in [x for x, _, _ in SERVICES] + ["APPLICATION"]:
            pv = p.loc[(col, s)]
            ov = {k: (sum(mm[x][k] for x, _, _ in SERVICES) if s == "APPLICATION" else mm[s][k])
                  for k, _, _ in METRICS}
            row = {"column": col, "service": s}
            for k, _, _ in METRICS:
                row[f"paper_{k}"], row[f"ours_{k}"] = round(pv[k], 1), round(ov[k], 1)
            row["paper_demand_m"] = round(pv.supply_cpu_m + pv.cpu_underprovision_m - pv.cpu_overprovision_m, 1)
            row["ours_demand_m"] = round(ov["supply_cpu_m"] + ov["cpu_underprovision_m"] - ov["cpu_overprovision_m"], 1)
            rows.append(row)
    pd.DataFrame(rows).to_csv(OUT / "paper_vs_ours_by_service.csv", index=False)


def run_totals(autoscaler):
    """{run: {metric: application total}} = sum over the 11 services of metrics.csv"""
    out = {}
    for n, d in run_dirs(str(SCENARIO_DIR), autoscaler):
        rows = [r for r in csv.DictReader(open(Path(d) / "metrics.csv", newline=""))
                if r["microservice"] != "APPLICATION"]
        out[n] = {k: sum(float(r[k]) for r in rows) for k, _, _ in METRICS}
    return out


def mann_whitney_p(a, b):
    """exact two-sided Mann-Whitney U p-value (no ties expected in these totals)"""
    n, values = len(a), a + b
    u_obs = sum((x > y) + 0.5 * (x == y) for x in a for y in b)
    mean_u = len(a) * len(b) / 2
    us = []
    for idx in itertools.combinations(range(len(values)), n):
        g1 = [values[i] for i in idx]
        g2 = [values[i] for i in range(len(values)) if i not in idx]
        us.append(sum((x > y) + 0.5 * (x == y) for x in g1 for y in g2))
    return sum(abs(u - mean_u) >= abs(u_obs - mean_u) - 1e-9 for u in us) / len(us)


def stack(ax, x, per_service, key, width):
    bottom = 0.0
    for name, _, color in SERVICES:
        v = per_service[name][key]
        ax.bar(x, v, bottom=bottom, width=width, color=color, edgecolor="white", linewidth=0.6)
        bottom += v
    return bottom


def legend(fig, with_line=False, y=0.005):
    handles = [Patch(color=c, label=l) for _, l, c in SERVICES]
    if with_line:
        handles.append(Line2D([], [], color=APP_LINE, marker="o", linewidth=2, label="App CPU (TB)"))
        handles.append(Line2D([], [], color=INK_2, marker="o", markerfacecolor="none", linestyle="",
                              label="từng lần chạy"))
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, y), ncol=7, frameon=False, fontsize=8.5,
               handlelength=1.2, columnspacing=1.2, labelcolor=INK)


def headers(fig, gs_left, gs_right):
    fig.text(gs_left, 0.985, LEFT_HEAD, ha="center", va="top", fontsize=10.5, fontweight="bold", color=INK)
    fig.text(gs_right, 0.985, RIGHT_HEAD, ha="center", va="top", fontsize=10.5, fontweight="bold", color=INK)


# ---------------------------------------------------------------- Fig. 8

def fig8():
    data = {a: mean_metrics(str(SCENARIO_DIR), a) for a, _ in FIG8_COLUMNS}
    totals = {a: run_totals(a) for a, _ in FIG8_COLUMNS}
    fig = plt.figure(figsize=(8.8, 11.9), facecolor="white")
    gs = fig.add_gridspec(4, 2, width_ratios=[1, 1.25], left=0.01, right=0.99, top=0.945, bottom=0.085,
                          wspace=0.12, hspace=0.32)
    headers(fig, 0.01 + 0.98 * 1 / 2.25 / 2, 0.99 - 0.98 * 1.25 / 2.25 / 2)
    ns = {a: len(totals[a]) for a, _ in FIG8_COLUMNS}
    trend = []
    for row, ((key, title, higher), box) in enumerate(zip(METRICS, FIG8_CROPS)):
        show_paper(fig.add_subplot(gs[row, 0]), paper_crop(FIG8_PAGE, box))
        ax = fig.add_subplot(gs[row, 1])
        style_axis(ax)
        tops = [stack(ax, i, data[a][0], key, 0.55) for i, (a, _) in enumerate(FIG8_COLUMNS)]
        top = max(tops)
        for i, t in enumerate(tops):
            ax.text(i, t + top * 0.012, f"{t:,.0f}", ha="center", va="bottom", fontsize=8.5, color=INK)
        # above Smart HPA and K8s HPA: change of each ProSmart variant vs that column, as the paper annotates
        for j, (other, _) in enumerate(FIG8_COLUMNS[2:], start=2):
            for k, (pro, short) in enumerate([("prosmarthpa-authors", "TG"), ("prosmarthpa-cv", "N")]):
                mp, mo = st.mean(v[key] for v in totals[pro].values()), st.mean(v[key] for v in totals[other].values())
                change = 100 * (mp / mo - 1)
                better = change > 0 if higher else change < 0
                pairs = [r for r in totals[pro] if r in totals[other]]
                wins = sum((totals[pro][r][key] > totals[other][r][key]) == higher for r in pairs)
                p = mann_whitney_p([v[key] for v in totals[pro].values()], [v[key] for v in totals[other].values()])
                paper = PAPER_CHANGE[(other, key)]
                trend.append({"metric": key, "prosmart": pro, "vs": other, "paper_change_pct": paper,
                              "our_change_pct": round(change, 2), "runs_better": f"{wins}/{len(pairs)}",
                              "p_mann_whitney": round(p, 3), "same_direction_as_paper": (change > 0) == (paper > 0)})
                ax.text(j, tops[j] + top * (0.13 + 0.085 * (1 - k)), f"{short} {change:+.1f}%", ha="center",
                        va="bottom", fontsize=8.5, fontweight="bold", color=GOOD if better else BAD)
        ax.set_xticks(range(len(FIG8_COLUMNS)))
        ax.set_xticklabels([f"{lbl}" for _, lbl in FIG8_COLUMNS], fontsize=8.5, color=INK)
        ax.set_xlim(-0.6, len(FIG8_COLUMNS) - 0.4)
        ax.set_ylim(0, top * 1.38)
        ax.tick_params(axis="y", labelsize=8)
        ax.set_title(f"{title}, {'cao hơn tốt hơn' if higher else 'thấp hơn tốt hơn'}", fontsize=9.5, color=INK,
                     loc="left")
    legend(fig, y=0.012)
    fig.text(0.5, 0.0, f"Bên phải: TB {ns['prosmarthpa-authors']} lần/cấu hình. TG / N: ProSmart (model tác giả / model nhóm) "
             "so với cột đó; xanh = tốt hơn, đỏ = kém hơn.",
             ha="center", va="bottom", fontsize=8.5, color=INK_2)
    fig.savefig(OUT / "fig8_sidebyside.png", dpi=220, facecolor="white")
    plt.close(fig)
    pd.DataFrame(trend).to_csv(OUT / "sidebyside_trend.csv", index=False)
    return pd.DataFrame(trend)


# ---------------------------------------------------------------- Fig. 9

def fig9():
    data = {a: mean_metrics(str(SCENARIO_DIR), a) for _, a in WINDOWS}
    totals = {w: run_totals(a) for w, a in WINDOWS}
    fig = plt.figure(figsize=(8.8, 12.2), facecolor="white")
    gs = fig.add_gridspec(4, 2, width_ratios=[1, 1.25], left=0.01, right=0.99, top=0.945, bottom=0.085,
                          wspace=0.12, hspace=0.42)
    headers(fig, 0.01 + 0.98 * 1 / 2.25 / 2, 0.99 - 0.98 * 1.25 / 2.25 / 2)
    rows = []
    for row, ((key, title, higher), box) in enumerate(zip(METRICS, FIG9_CROPS)):
        show_paper(fig.add_subplot(gs[row, 0]), paper_crop(FIG9_PAGE, box))
        ax = fig.add_subplot(gs[row, 1])
        style_axis(ax)
        means = [stack(ax, i, data[a][0], key, 0.62) for i, (_, a) in enumerate(WINDOWS)]
        for i, (w, _) in enumerate(WINDOWS):
            runs = [v[key] for v in totals[w].values()]
            ax.scatter([i + 0.42] * len(runs), runs, s=16, facecolors="none", edgecolors=INK_2, linewidths=0.9,
                       zorder=6)
            rows.append({"metric": key, "window_sec": w, "n": len(runs), "mean": round(st.mean(runs), 1),
                         "min": round(min(runs), 1), "max": round(max(runs), 1)})
        h, p = kruskal([[v[key] for v in totals[w].values()] for w, _ in WINDOWS])
        for r in rows[-len(WINDOWS):]:
            r["kruskal_h"], r["kruskal_p"] = round(h, 2), round(p, 3)
        ax.plot(range(len(WINDOWS)), means, color=APP_LINE, linewidth=1.5, marker="o", markersize=4.5, zorder=5)
        top = max(max(v[key] for v in totals[w].values()) for w, _ in WINDOWS)
        for i, m in enumerate(means):
            ax.text(i, m + top * 0.02, f"{m:,.0f}", ha="center", va="bottom", fontsize=8, color=INK,
                    bbox=dict(boxstyle="square,pad=0.1", facecolor="white", edgecolor="none", alpha=0.8), zorder=7)
        ax.set_xticks(range(len(WINDOWS)))
        ax.set_xticklabels([f"{w}\n(n={len(totals[w])})" for w, _ in WINDOWS], fontsize=8, color=INK)
        ax.set_xlabel("Prediction window (giây)", fontsize=8.5, color=INK_2)
        ax.set_xlim(-0.6, len(WINDOWS) - 0.3)
        ax.set_ylim(0, top * 1.15)
        ax.tick_params(axis="y", labelsize=8)
        ax.set_title(f"{title}; Kruskal-Wallis p = {p:.3f}".replace(".", ","), fontsize=9.5, color=INK, loc="left")
    legend(fig, with_line=True, y=0.012)
    fig.text(0.5, 0.0, "Bên phải: ProSmart HPA, model nhóm; cột = TB, chấm rỗng = tổng ứng dụng từng lần chạy.", ha="center", va="bottom", fontsize=8.5, color=INK_2)
    fig.savefig(OUT / "fig9_sidebyside.png", dpi=220, facecolor="white")
    plt.close(fig)
    pd.DataFrame(rows).to_csv(OUT / "sidebyside_fig9.csv", index=False)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- Fig. 5

def fig5():
    fig = plt.figure(figsize=(8.8, 4.6), facecolor="white")
    gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1], left=0.01, right=0.99, top=0.9, bottom=0.12,
                          wspace=0.1, hspace=0.45)
    headers(fig, 0.01 + 0.98 * 1.15 / 2.15 / 2, 0.99 - 0.98 * 1 / 2.15 / 2)
    show_paper(fig.add_subplot(gs[:, 0]), paper_crop(FIG5_PAGE, FIG5_BOX))
    panels = [(FIG5_MODELS[0], "(a) Model tác giả (file .pkl), trên dữ liệu train của chính nó"),
              (FIG5_MODELS[2], "(b) Model nhóm (tinh chỉnh bằng CV), Smart HPA run 1–5")]
    for row, ((_, folder, runs), title) in enumerate(panels):
        ax = fig.add_subplot(gs[row, 1])
        style_axis(ax)
        ds, y, fc, width = fit_authors(FIG5_SERVICE) if folder is None else fit_ours(FIG5_SERVICE, folder, runs)
        t = (pd.to_datetime(ds) - pd.Timestamp(0)).dt.total_seconds().values / 60
        f = pd.DataFrame({"t": t, "yhat": fc["yhat"].values, "lo": fc["yhat_lower"].values,
                          "hi": fc["yhat_upper"].values}).groupby("t").mean()
        ax.scatter(t, y, s=1.5, color="#222222", alpha=0.6, linewidths=0, zorder=2)
        ax.fill_between(f.index, f["lo"], f["hi"], color="#2a78d6", alpha=0.2, linewidth=0, zorder=1)
        ax.plot(f.index, f["yhat"], color="#2a78d6", linewidth=1.8, zorder=3)
        mae = np.abs(fc["yhat"].values - y).mean()
        ax.text(0.99, 0.05, f"MAE {mae:.2f} replica".replace(".", ","), transform=ax.transAxes, ha="right",
                fontsize=8, color=INK_2)
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 12)
        ax.set_title(title, fontsize=8.5, color=INK, loc="left")
        ax.set_ylabel("Desired Replicas", fontsize=8, color=INK_2)
        ax.tick_params(labelsize=7.5)
        if row == 1:
            ax.set_xlabel("Thời gian (phút)", fontsize=8, color=INK_2)
    handles = [Line2D([], [], marker="o", linestyle="", markersize=4, color="#222222", label="Dữ liệu train"),
               Line2D([], [], color="#2a78d6", linewidth=2, label="Dự đoán"),
               Patch(color="#2a78d6", alpha=0.2, label="Khoảng tin cậy 80%")]
    fig.legend(handles=handles, loc="lower right", bbox_to_anchor=(0.99, 0.0), ncol=3, frameon=False, fontsize=8)
    fig.text(0.01, 0.02, f"{FIG5_SERVICE}, model nhu cầu (demand).", fontsize=8, color=INK_2)
    fig.savefig(OUT / "fig5_sidebyside.png", dpi=220, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- pod start-up on our cluster

def pod_ready_lag(autoscaler="smarthpa"):
    """The paper picks the window from pod start-up (15 s) and termination (30 s) times. For every scale-up in
    cluster_metrics.csv (spec_replicas rises), seconds until ready_replicas reaches the new value. The recorder
    samples every ~15 s, so 15 s means 'ready by the next sample'."""
    lags = []
    for n, d in run_dirs(str(SCENARIO_DIR), autoscaler):
        df = pd.read_csv(Path(d) / "cluster_metrics.csv")
        for dep, g in df.groupby("deployment"):
            g = g.sort_values("elapsed_sec").reset_index(drop=True)
            for i in range(1, len(g)):
                if g.spec_replicas[i] > g.spec_replicas[i - 1]:
                    ready = g[(g.index >= i) & (g.ready_replicas >= g.spec_replicas[i])]
                    if len(ready):
                        lags.append({"run": n, "deployment": dep, "scaled_at_sec": g.elapsed_sec[i],
                                     "ready_after_sec": ready.elapsed_sec.iloc[0] - g.elapsed_sec[i]})
    out = pd.DataFrame(lags)
    out.to_csv(OUT / "pod_ready_lag.csv", index=False)
    step = pd.read_csv(Path(run_dirs(str(SCENARIO_DIR), autoscaler)[0][1]) / "cluster_metrics.csv")
    step = step.groupby("deployment").elapsed_sec.diff().median()
    print(f"pod ready lag ({autoscaler}): {len(out)} scale-ups, median {out.ready_after_sec.median():.0f} s, "
          f"max {out.ready_after_sec.max():.0f} s (recorder step {step:.0f} s)")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print(fig8().to_string(index=False))
    print(fig9().to_string(index=False))
    fig5()
    pod_ready_lag()
    paper_tables()
    print(f"Written to {OUT}")
