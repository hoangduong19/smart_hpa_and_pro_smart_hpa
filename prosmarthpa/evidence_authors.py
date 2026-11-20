"""Evidence that the authors' published Smart HPA data (2R-20%) does not follow their own Algorithm 2 / released code,
and that one value of paper Fig. 8 is impossible under the paper's own formulas. Offline, reproducible, no cluster.

Source of the authors' data: the training data stored inside their 22 released PROPHET models (model.history), which
the paper (Section 5.1) says are trained on the Knowledge Base of Smart HPA runs: 10 runs x 181 points on a 5 s grid,
columns Desired Replicas (DR, demand models) and Max. Replicas (maxR, capacity models). Total maxR = 22 on every row,
so the data is from Smart HPA (quota exchange), not K8s HPA.

E1  Algorithm 2 rule check, independent of any code. Paper Section 3.3.2 / Algorithm 2 lines 14-29: when a service
    is underprovisioned (DR > maxR) and other services hold residual replicas, the Resource Balancer moves residual
    quota to it. Conservative test on the authors' rows: a service needs >= 1 FULL replica (DR >= maxR + 1) and the
    other services hold >= 1 FULL spare replica's worth of CPU (sum floor(maxR - DR) x request >= its request).
    If no underprovisioned service gains maxR within the next 15 s (3 grid points), the row is a violation.
E2  Replay: the authors' own DR series fed, row by row, through the authors' released ARM code
    (smarthpa/Adaptive_Resource_Manager.py, identical to the replication package) and Capacity Analyzer loop logic;
    the maxR it produces is compared with the maxR the authors recorded.
E3  Fig. 8, K8s HPA, frontend demand = 2692.6 m. K8s HPA caps frontend at maxR = 2 pods, CPU limit 200 m = 200 % of the
    100 m request, threshold 20 %: DR = ceil(CR x CPU% / 20) <= ceil(2 x 200 / 20) = 20 -> demand <= 2000 m.
    The same figure gives frontend CPU Overutilization 147.2 %, which implies DR ~ ceil(2 x 147 / 20) = 15 (~1500 m).

Limits (state them in the report): the .pkl data is resampled by the authors to a 5 s grid (linear interpolation),
so DR values can be fractional between two loop iterations; E1 uses whole replicas only for that reason. E2 has to
model current replicas (CR) from DR and maxR, because CR is not in the .pkl.

Usage (prophet venv, from prosmarthpa/):  python evidence_authors.py
Output: results/2R-20/comparison_prosmart_figs/evidence/ (3 figures, 3 CSV, evidence.md)
"""

import math
import sys
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
from compare_author_models import author_history, MICROSERVICES      # noqa: E402
from train_prophet import DEMO_DIR                                    # noqa: E402

sys.path.insert(0, str(DEMO_DIR / "smarthpa"))
from Adaptive_Resource_Manager import Adaptive_Resource_Manager       # noqa: E402  the authors' Algorithm 2 code

OUT = DEMO_DIR / "results" / "2R-20" / "comparison_prosmart_figs" / "evidence"
REQUEST = {s: 100 for s in MICROSERVICES} | {"adservice": 200, "cartservice": 200, "redis-cart": 70}
SLA_MAXR = 2
# order of the managers in Microservice_Capacity_Analyzer.py (ARM sorts, ties keep this order)
ORDER = ["frontend", "adservice", "cartservice", "currencyservice", "checkoutservice", "emailservice",
         "paymentservice", "shippingservice", "productcatalogservice", "recommendationservice", "redis-cart"]
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
AUTHORS, REPLAY, DEMAND, PAPER, LIMIT, LAB = "#eb6834", "#2a78d6", "#a3a29c", "#eb6834", "#0b0b0b", "#2a78d6"


def load_authors():
    """long table: run, t, service, DR, maxR (rows of each t are the 10 runs in the same order)"""
    rows = []
    for s in MICROSERVICES:
        d, c = author_history("demand", s), author_history("capacity", s)
        assert len(d) == 1810 and (d.t.values == c.t.values).all()
        rows.append(pd.DataFrame({"run": np.arange(len(d)) % 10 + 1, "t": d.t.values, "service": s,
                                  "DR": d.y.values, "maxR": c.y.values}))
    df = pd.concat(rows)
    per_row = df.pivot_table(index=["run", "t"], columns="service", values="maxR").sum(axis=1)
    assert (per_row.round(6) == 22).all(), "total maxR is not 22 on every row: run split is wrong"
    return df


def e1_rule_check(df):
    out = []
    for run, g in df.groupby("run"):
        dr = g.pivot(index="t", columns="service", values="DR")
        mr = g.pivot(index="t", columns="service", values="maxR")
        times = list(dr.index)
        for k, t in enumerate(times):
            need = [s for s in MICROSERVICES if dr.at[t, s] >= mr.at[t, s] + 1]
            spare_cpu = sum(math.floor(max(mr.at[t, s] - dr.at[t, s], 0) + 1e-9) * REQUEST[s]
                            for s in MICROSERVICES if s not in need)
            required = bool(need) and spare_cpu >= min(REQUEST[s] for s in need)
            later = times[k + 1:k + 4]
            moved = any(mr.at[u, s] > mr.at[t, s] + 1e-9 for u in later for s in need)
            out.append({"run": run, "t": t, "transfer_required": required, "quota_moved_within_15s": moved,
                        "violation": required and not moved, "needy": " ".join(need), "spare_cpu_m": spare_cpu})
    return pd.DataFrame(out)


def e2_replay(df):
    res = []
    for run, g in df.groupby("run"):
        dr = g.pivot(index="t", columns="service", values="DR")
        mr = g.pivot(index="t", columns="service", values="maxR")
        saved, cr = None, {s: 1 for s in ORDER}
        for t in dr.index:
            data = [[s, "no scale", int(math.ceil(dr.at[t, s] - 1e-9)), cr[s], REQUEST[s], SLA_MAXR] for s in ORDER]
            if any(d[2] > d[5] for d in data):                    # Capacity Analyzer: resource-constrained -> ARM
                if saved:
                    for d in data:
                        d[5] = saved[d[0]]
                saved = {x[0]: x[3] for x in Adaptive_Resource_Manager(data)}
            else:
                saved = None
            cap = saved or {s: SLA_MAXR for s in ORDER}
            for s in ORDER:
                cr[s] = max(1, min(int(math.ceil(dr.at[t, s] - 1e-9)), cap[s]))
                res.append({"run": run, "t": t, "service": s, "maxR_recorded": mr.at[t, s], "maxR_replay": cap[s]})
    return pd.DataFrame(res)


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def fig_e2(df, rep, path):
    services = ["currencyservice", "frontend", "shippingservice", "emailservice"]
    fig, axes = plt.subplots(2, 2, figsize=(11, 6.4), sharex=True, facecolor=SURFACE)
    for ax, s in zip(axes.flat, services):
        style(ax)
        r = rep[rep.service == s].groupby("t")[["maxR_recorded", "maxR_replay"]].mean()
        d = df[df.service == s].groupby("t").DR.mean()
        ax.plot(d.index, d.values, color=DEMAND, linewidth=1.5, linestyle=(0, (4, 2)), label="Demand DR (authors' data)")
        ax.plot(r.index, r.maxR_replay, color=REPLAY, linewidth=2, label="maxR from the authors' ARM code (replay)")
        ax.plot(r.index, r.maxR_recorded, color=AUTHORS, linewidth=2, label="maxR the authors recorded")
        ax.set_title(s, fontsize=10, color=INK, loc="left")
        ax.set_ylim(0, max(4, float(np.nanmax([r.values.max(), d.max()])) + 1))
    for ax in axes[1]:
        ax.set_xlabel("Time since load start (s)", fontsize=9, color=INK_2)
    for ax in axes[:, 0]:
        ax.set_ylabel("Replicas (mean of 10 runs)", fontsize=9, color=INK_2)
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, fontsize=9)
    fig.suptitle("E2: authors' recorded maxR vs maxR their own ARM code produces from the same demand (2R-20%)",
                 fontsize=11, color=INK, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def fig_e1(chk, path):
    per_run = chk.groupby("run").agg(required=("transfer_required", "sum"), violations=("violation", "sum"))
    fig, ax = plt.subplots(figsize=(9, 4), facecolor=SURFACE)
    style(ax)
    x = np.arange(len(per_run))
    ax.bar(x - 0.2, per_run.required, width=0.38, color=REPLAY, label="Rows where Algorithm 2 requires a quota transfer")
    ax.bar(x + 0.2, per_run.violations, width=0.38, color=AUTHORS, label="... and no quota moved within 15 s")
    ax.set_xticks(x, [f"run {r}" for r in per_run.index])
    ax.set_ylabel("Rows (5 s each, 181 per run)", fontsize=9, color=INK_2)
    ax.legend(frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(0, -0.12), ncol=2)
    tot_r, tot_v = int(per_run.required.sum()), int(per_run.violations.sum())
    ax.set_title(f"E1: Algorithm 2 rule broken in {tot_v}/{tot_r} rows ({tot_v / max(tot_r, 1):.0%}) of the authors' Smart HPA data",
                 fontsize=11, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return per_run


def fig_e3(path):
    labels = ["Paper Fig. 8 (K8s HPA)", "Maximum possible\n(2 pods x 200% / 20%)", "Implied by paper's own\nOverutilization 147.2%",
              "Lab K8s HPA (5 runs)"]
    values = [2692.6, 2000.0, 1500.0, 1578.6]
    colors = [PAPER, LIMIT, DEMAND, LAB]
    fig, ax = plt.subplots(figsize=(9, 3.6), facecolor=SURFACE)
    style(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    y = np.arange(len(values))[::-1]
    ax.barh(y, values, height=0.55, color=colors)
    for yi, v in zip(y, values):
        ax.text(v + 30, yi, f"{v:,.0f} m", va="center", fontsize=9, color=INK)
    ax.axvline(2000, color=LIMIT, linewidth=1, linestyle=(0, (4, 2)))
    ax.set_yticks(y, labels, fontsize=9, color=INK)
    ax.set_xlim(0, 3100)
    ax.set_xlabel("frontend CPU demand under K8s HPA, 2R-20% (milliCPU)", fontsize=9, color=INK_2)
    ax.set_title("E3: paper value is above the maximum the paper's own formula allows", fontsize=11, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_authors()
    chk = e1_rule_check(df)
    chk.to_csv(OUT / "e1_rule_check.csv", index=False)
    per_run = fig_e1(chk, OUT / "e1_rule_check.png")
    rep = e2_replay(df)
    rep.to_csv(OUT / "e2_replay.csv", index=False)
    fig_e2(df, rep, OUT / "e2_replay.png")
    fig_e3(OUT / "e3_fig8_frontend.png")
    pd.DataFrame([{"source": "paper Fig. 8 K8s HPA frontend demand", "value_m": 2692.6},
                  {"source": "max possible: ceil(2 x 200 / 20) x 100 m", "value_m": 2000.0},
                  {"source": "implied by paper frontend Overutilization 147.2 %: ceil(2 x 147.2 / 20) x 100 m", "value_m": 1500.0},
                  {"source": "lab K8s HPA, 5 runs", "value_m": 1578.6}]).to_csv(OUT / "e3_fig8_frontend.csv", index=False)

    rows = rep.assign(eq=rep.maxR_replay.round() == rep.maxR_recorded.round()).groupby(["run", "t"]).eq.all()
    agree = rows.mean()
    svc_agree = rep.assign(eq=rep.maxR_replay.round() == rep.maxR_recorded.round()).groupby("service").eq.mean()
    tot_r, tot_v = int(per_run.required.sum()), int(per_run.violations.sum())
    first = chk[chk.violation].sort_values(["run", "t"]).groupby("run").first()
    md = [
        "# Evidence: the authors' Smart HPA data vs their Algorithm 2 / code (2R-20%)", "",
        f"Data: training data inside the authors' 22 released PROPHET models, 10 runs x 181 points (5 s grid).", "",
        "## E1. Algorithm 2 rule check (no code involved)",
        f"- Rows where a service needs >= 1 full replica and other services hold >= 1 full spare replica: **{tot_r}**",
        f"- ... of which no quota moved within 15 s: **{tot_v} ({tot_v / max(tot_r, 1):.0%})**",
        f"- Per run: " + ", ".join(f"run {r}: {int(v)}/{int(q)}" for r, (q, v) in per_run.iterrows()),
        f"- First violation per run (t, underprovisioned services): " +
        "; ".join(f"run {r}: {row.t:.0f} s ({row.needy})" for r, row in first.iterrows()), "",
        "## E2. Replay through the authors' released ARM code",
        f"- Rows where replayed maxR equals recorded maxR for all 11 services: **{agree:.1%}**",
        "- Per service agreement: " + ", ".join(f"{s} {v:.0%}" for s, v in svc_agree.items()), "",
        "## E3. Paper Fig. 8, K8s HPA, frontend demand",
        "- Paper: 2692.6 m. Maximum possible with maxR 2, CPU limit 200 % of request, threshold 20 %: 2000 m.",
        "- The same figure's frontend Overutilization 147.2 % implies about 1500 m. Lab (5 runs): 1578.6 m.", "",
        "## Limits",
        "- The .pkl data is the authors' 5 s resampling (linear interpolation); E1 counts whole replicas only.",
        "- E2 models current replicas from DR and maxR (not stored in the .pkl).",
        "- None of this shows which code the authors ran; it shows their published data cannot come from the published code.",
    ]
    (OUT / "evidence.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    print(f"\nWritten to {OUT}")


if __name__ == "__main__":
    main()
