"""Redraw the ProSmart HPA figures of the paper (Ahmad et al., JSS 2025) from our data, so the report can put ours next
to theirs:

  fig5_model_fit.png   paper Fig. 5: PROPHET model fit = training data (dots), predicted data (line), confidence
                       interval (band), recommendationservice demand model as in the paper. (a) the authors' released
                       model on its own training data (stored in the .pkl), (b) our first model (models/, Smart HPA
                       2R-20% run 1-3, Prophet defaults), (c) our model tuned by CV (models_5runs_cv/, run 1-5).
  fig5_model_fit.csv   in-sample error of each panel: MAE (replicas) and share of training points inside the band
  fig8_services_<tag>.png  paper Fig. 8: Supply CPU / CPU Overutilization / CPU Underprovision / CPU Overprovision,
                       ProSmart HPA vs Smart HPA vs K8s HPA, columns stacked by microservice, mean over runs, with the
                       change of ProSmart HPA relative to each other autoscaler above that column (as the paper does).
                       tag cv = ProSmart HPA runs with the CV models (prosmarthpa-cv), 3runs = first models (prosmarthpa)
  fig8_services_<tag>.csv  the numbers behind fig8, per autoscaler and microservice
  fig9_window.png      paper Fig. 9: the same 4 metrics per prediction window (5-30 s), stacked by microservice, red line
                       = whole application. Drawn once runs of at least 2 windows exist (prosmarthpa-cv-w<N> + prosmarthpa-cv).
  fig9_window.csv      the numbers behind fig9

Offline only (no cluster). Same colors as smarthpa/make_paper_figs.py (Fig. 6), so a service has one color in the report.
Unlike the paper's Fig. 8, CPU Overutilization is in % (our metric, as in Fig. 6), not mCPU.

Usage (prophet venv, from prosmarthpa/):
  D:\\prosmart-venv\\Scripts\\python.exe make_prosmart_figs.py [--scenario 2R-20] [--with-authors] [--prosmart prosmarthpa-cv|prosmarthpa]
  --with-authors adds a 4th column to Fig. 8: ProSmart HPA run with the authors' models (prosmarthpa-authors)
"""

import argparse
import csv
import logging
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

from train_prophet import DEMO_DIR, MODELS, load_run
from compare_author_models import AUTHOR_MODELS, SUFFIX, load_model

sys.path.insert(0, str(DEMO_DIR / "smarthpa"))
from make_paper_figs import (INK, INK_2, NAMED, OTHER, OTHER_COLOR, SURFACE, mean_metrics,  # noqa: E402
                             run_dirs, stack_groups, style_axis)

logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
logging.getLogger("prophet").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=FutureWarning)

# paper Fig. 5 shows the demand model of recommendationservice
FIG5_SERVICE = "recommendationservice"
HERE = Path(__file__).resolve().parent
# (title, model folder or None = authors, training runs)
FIG5_MODELS = [("Authors' model (time only), trained on their 10 Smart HPA runs", None, None),
               ("Our first model (models/), Smart HPA run 1-3, Prophet defaults", HERE / "models", [1, 2, 3]),
               ("Our model (models_5runs_cv/), Smart HPA run 1-5, tuned by CV", HERE / "models_5runs_cv", [1, 2, 3, 4, 5])]
LINE, BAND = "#2a78d6", "#2a78d6"   # categorical slot 1 (blue); band = same hue, low alpha

# ProSmart HPA run folder -> (label, file tag): prosmarthpa-cv = models_5runs_cv (current), prosmarthpa = models/ (first)
PROSMART = {"prosmarthpa-cv": ("ProSmart HPA\n(CV models)", "cv"), "prosmarthpa": ("ProSmart HPA\n(first models)", "3runs")}
OTHERS = [("smarthpa", "Smart HPA"), ("k8shpa", "K8s HPA")]                     # paper order: ProSmart, Smart, K8s
AUTHORS_COLUMN = ("prosmarthpa-authors", "ProSmart HPA\n(authors' models)")

# paper Fig. 8 panel order: Supply, Overutilization (top), Underprovision, Overprovision (bottom)
FIG8_PANELS = [
    ("supply_cpu_m", "Supply CPU (m) - higher is better", True),
    ("cpu_overutilization_pct", "CPU Overutilization (%) - lower is better", False),
    ("cpu_underprovision_m", "CPU Underprovision (m) - lower is better", False),
    ("cpu_overprovision_m", "CPU Overprovision (m) - lower is better", False),
]
GOOD, BAD = "#008300", "#c0392b"


# ---------------------------------------------------------------- Fig. 5

def fit_authors(service):
    """authors' time-only model on the training data stored inside its .pkl"""
    model = load_model(AUTHOR_MODELS["demand"] / f"{service}_{SUFFIX['demand']}.pkl")
    hist = model.history[["ds", "y"]].copy()
    fc = model.predict(hist[["ds"]])
    return hist["ds"], hist["y"].values, fc, model.interval_width


def fit_ours(service, folder, runs):
    """our model (time + regressors) on its training runs; the forecast uses the regressors of each training row"""
    model = load_model(folder / f"{service}_{SUFFIX['demand']}.pkl")
    spec = MODELS["demand"]
    # Prophet.predict() returns rows sorted by ds: sort first so forecast row i matches data row i
    data = pd.concat([load_run("2R-20", r, service) for r in runs]).sort_values("ds", kind="stable")
    fc = model.predict(data[["ds"] + spec["regressors"]])
    return data["ds"], data[spec["y"]].values, fc, model.interval_width


def fig5(out_dir):
    fig, axes = plt.subplots(1, len(FIG5_MODELS), figsize=(6 * len(FIG5_MODELS), 5.4), facecolor=SURFACE,
                             sharey=True, layout="constrained")
    fig.suptitle(f"PROPHET model fit, {FIG5_SERVICE} Desired Replicas (paper Fig. 5 layout)", x=0.01, ha="left",
                 fontsize=14, color=INK, fontweight="bold")
    stats = []
    for i, (ax, (title, folder, runs)) in enumerate(zip(axes, FIG5_MODELS)):
        style_axis(ax)
        ds, y, fc, width = fit_authors(FIG5_SERVICE) if folder is None else fit_ours(FIG5_SERVICE, folder, runs)
        t = (pd.to_datetime(ds) - pd.Timestamp(0)).dt.total_seconds().values / 60
        # forecast per row; with regressors several rows share a time -> show the mean line and band per time
        f = pd.DataFrame({"t": t, "yhat": fc["yhat"].values, "lo": fc["yhat_lower"].values,
                          "hi": fc["yhat_upper"].values}).groupby("t").mean()
        ax.scatter(t, y, s=6, color=INK_2, alpha=0.55, linewidths=0, zorder=2)
        ax.fill_between(f.index, f["lo"], f["hi"], color=BAND, alpha=0.18, linewidth=0, zorder=1)
        ax.plot(f.index, f["yhat"], color=LINE, linewidth=2, zorder=3)
        ax.set_xlim(0, 15)
        ax.set_ylim(bottom=0)
        ax.set_title(f"({'abc'[i]}) {title}", fontsize=10, color=INK, loc="left", wrap=True)
        ax.set_xlabel("Time (minutes)", fontsize=9, color=INK_2)
        inside = (y >= fc["yhat_lower"].values) & (y <= fc["yhat_upper"].values)
        mae = np.abs(fc["yhat"].values - y).mean()
        stats.append({"model": folder.name if folder else "authors", "service": FIG5_SERVICE,
                      "train_runs": "authors' 10" if folder is None else " ".join(map(str, runs)), "points": len(y),
                      "mae_replicas": round(mae, 3), "inside_band_pct": round(100 * inside.mean(), 1),
                      "interval_width": width})
        ax.text(0.99, 0.03, f"MAE {mae:.2f} replicas, {100 * inside.mean():.0f}% of points in band",
                transform=ax.transAxes, ha="right", fontsize=9, color=INK_2)
    axes[0].set_ylabel("Desired Replica count", fontsize=9, color=INK_2)
    handles = [Line2D([], [], marker="o", linestyle="", markersize=5, color=INK_2, label="Training data"),
               Line2D([], [], color=LINE, linewidth=2, label="Predicted data"),
               Patch(color=BAND, alpha=0.18, label=f"Confidence interval ({int(stats[0]['interval_width'] * 100)}%)")]
    fig.legend(handles=handles, loc="outside lower center", ncol=3, frameon=False, fontsize=10, labelcolor=INK)
    fig.text(0.5, -0.1, "In-sample fit (the data the model was trained on), as in the paper. (b), (c): line and band "
             "are averaged over the runs at each time, because the forecast depends on each run's regressors;\n"
             "those regressors are observed at the same time as y here, so (b) and (c) look closer than the models "
             "can predict 25 s ahead (see models_5runs_cv/nested_cv.csv).",
             ha="center", va="top", fontsize=9, color=INK_2)
    fig.savefig(out_dir / "fig5_model_fit.png", dpi=130, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    pd.DataFrame(stats).to_csv(out_dir / "fig5_model_fit.csv", index=False)
    return pd.DataFrame(stats)


# ---------------------------------------------------------------- Fig. 8

def fig8(scenario_dir, out_dir, autoscalers, tag):
    data = {a: mean_metrics(str(scenario_dir), a) for a, _ in autoscalers}
    scenario = scenario_dir.name + "%"
    ns = ", ".join(f"{name.splitlines()[0]}{' (authors)' if a.endswith('authors') else ''} n={data[a][1]}"
                   for a, name in autoscalers)
    fig, axes = plt.subplots(2, 2, figsize=(4 + 2.6 * len(autoscalers) * 2, 10), facecolor=SURFACE)
    fig.suptitle(f"{scenario}: ProSmart HPA vs Smart HPA vs K8s HPA, stacked by microservice (paper Fig. 8 layout)",
                 x=0.01, ha="left", fontsize=14, color=INK, fontweight="bold")
    fig.text(0.01, 0.925, f"Mean over runs ({ns}). Above a column: change of ProSmart HPA relative to that column "
             "(green = ProSmart better, red = worse).", fontsize=10, color=INK_2)
    rows = []
    for ax, (key, title, higher_better) in zip(axes.flat, FIG8_PANELS):
        style_axis(ax)
        totals = []
        for i, (a, name) in enumerate(autoscalers):
            per_service = data[a][0]
            bottom = 0
            for label, color, v in stack_groups(per_service, key):
                ax.bar(i, v, bottom=bottom, width=0.55, color=color, edgecolor=SURFACE, linewidth=1.5)
                bottom += v
                rows.append([scenario, a, label, key, round(v, 3)])
            totals.append(per_service["APPLICATION"][key])
            rows.append([scenario, a, "APPLICATION", key, round(totals[-1], 3)])
        top = max(totals)
        pro = totals[0]
        for i, total in enumerate(totals):
            ax.text(i, total + top * 0.015, f"{total:,.0f}", ha="center", va="bottom", fontsize=9, color=INK)
            if i == 0:
                continue
            change = 100 * (pro - total) / total
            better = change > 0 if higher_better else change < 0
            ax.text(i, total + top * 0.075, f"ProSmart {change:+.1f}%", ha="center", va="bottom", fontsize=9,
                    color=GOOD if better else BAD, fontweight="bold")
        ax.set_xticks(range(len(autoscalers)))
        ax.set_xticklabels([n for _, n in autoscalers], fontsize=9, color=INK)
        ax.set_xlim(-0.6, len(autoscalers) - 0.4)
        ax.set_ylim(0, top * 1.2)
        ax.set_title(title, fontsize=11, color=INK, loc="left")
    handles = [Patch(color=c, label=l) for _, l, c in NAMED] + [
        Patch(color=OTHER_COLOR, label="other services (" + ", ".join(s.replace("service", "") for s in OTHER) + ")")]
    fig.legend(handles=handles, loc="lower center", ncol=8, frameon=False, fontsize=9, labelcolor=INK,
               handlelength=1.2, columnspacing=1.4)
    fig.tight_layout(rect=(0, 0.04, 1, 0.91), h_pad=3)
    name = f"fig8_services_{tag}" + ("_with_authors" if len(autoscalers) > 3 else "")
    fig.savefig(out_dir / f"{name}.png", dpi=130, facecolor=SURFACE)
    plt.close(fig)
    with open(out_dir / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "autoscaler", "microservice", "metric", "mean_over_runs"])
        w.writerows(rows)


# ---------------------------------------------------------------- Fig. 9

# prediction window (s) -> run folder, all with the CV models; 25 s = prosmarthpa-cv
# (run_experiment.ps1 -Autoscaler prosmarthpa-cv-w<N>)
WINDOWS = [(5, "prosmarthpa-cv-w5"), (10, "prosmarthpa-cv-w10"), (15, "prosmarthpa-cv-w15"), (20, "prosmarthpa-cv-w20"),
           (25, "prosmarthpa-cv"), (30, "prosmarthpa-cv-w30")]
APP_LINE = "#c0392b"


def fig9(scenario_dir, out_dir):
    done = [(w, a) for w, a in WINDOWS if run_dirs(str(scenario_dir), a)]
    if len(done) < 2:
        print(f"Fig. 9 skipped: runs for {len(done)} window(s) only ({[w for w, _ in done]} s), need at least 2")
        return
    data = {a: mean_metrics(str(scenario_dir), a) for _, a in done}
    scenario = scenario_dir.name + "%"
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), facecolor=SURFACE)
    fig.suptitle(f"{scenario}: ProSmart HPA (CV models) with changing prediction window size (paper Fig. 9 layout)",
                 x=0.01, ha="left", fontsize=14, color=INK, fontweight="bold")
    fig.text(0.01, 0.925, "Mean over runs (" + ", ".join(f"{w}s n={data[a][1]}" for w, a in done) + "). Red line = "
             "whole application (top of the stack).", fontsize=10, color=INK_2)
    rows = []
    for ax, (key, title, _) in zip(axes.flat, FIG8_PANELS):
        style_axis(ax)
        totals = []
        for i, (w, a) in enumerate(done):
            per_service = data[a][0]
            bottom = 0
            for label, color, v in stack_groups(per_service, key):
                ax.bar(i, v, bottom=bottom, width=0.6, color=color, edgecolor=SURFACE, linewidth=1.5)
                bottom += v
                rows.append([scenario, w, a, label, key, round(v, 3)])
            totals.append(per_service["APPLICATION"][key])
            rows.append([scenario, w, a, "APPLICATION", key, round(totals[-1], 3)])
        ax.plot(range(len(done)), totals, color=APP_LINE, linewidth=2, marker="o", markersize=8,
                markeredgecolor=SURFACE, markeredgewidth=2, zorder=5)
        best = min(range(len(totals)), key=lambda i: -totals[i] if key == "supply_cpu_m" else totals[i])
        for i, t in enumerate(totals):
            ax.text(i, t * 1.03, f"{t:,.0f}", ha="center", va="bottom", fontsize=9, color=INK,
                    fontweight="bold" if i == best else "normal")
        ax.set_xticks(range(len(done)))
        ax.set_xticklabels([str(w) for w, _ in done], fontsize=10, color=INK)
        ax.set_xlabel("Prediction Window Size (sec)", fontsize=9, color=INK_2)
        ax.set_ylim(0, max(totals) * 1.15)
        ax.set_title(title, fontsize=11, color=INK, loc="left")
    handles = [Patch(color=c, label=l) for _, l, c in NAMED] + [
        Patch(color=OTHER_COLOR, label="other services"),
        Line2D([], [], color=APP_LINE, linewidth=2, marker="o", label="App CPU")]
    fig.legend(handles=handles, loc="lower center", ncol=9, frameon=False, fontsize=9, labelcolor=INK,
               handlelength=1.4, columnspacing=1.4)
    fig.tight_layout(rect=(0, 0.04, 1, 0.91), h_pad=3)
    fig.savefig(out_dir / "fig9_window.png", dpi=130, facecolor=SURFACE)
    plt.close(fig)
    with open(out_dir / "fig9_window.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "window_sec", "autoscaler", "microservice", "metric", "mean_over_runs"])
        w.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="2R-20")
    parser.add_argument("--with-authors", action="store_true")
    parser.add_argument("--prosmart", choices=list(PROSMART), help="ProSmart runs for Fig. 8 "
                        "(default: prosmarthpa-cv once it has runs, otherwise prosmarthpa)")
    args = parser.parse_args()
    scenario_dir = DEMO_DIR / "results" / args.scenario
    out_dir = scenario_dir / "comparison_prosmart_figs"
    out_dir.mkdir(parents=True, exist_ok=True)

    prosmart = args.prosmart or ("prosmarthpa-cv" if run_dirs(str(scenario_dir), "prosmarthpa-cv") else "prosmarthpa")
    label, tag = PROSMART[prosmart]
    print(f"Fig. 8 uses {prosmart} {label.splitlines()[1]}")
    autoscalers = [(prosmart, label)] + OTHERS + ([AUTHORS_COLUMN] if args.with_authors else [])
    missing = [a for a, _ in autoscalers if not run_dirs(str(scenario_dir), a)]
    if missing:
        sys.exit(f"No runs for {missing} under {scenario_dir}")
    fig8(scenario_dir, out_dir, autoscalers, tag)
    fig9(scenario_dir, out_dir)
    print(fig5(out_dir).to_string(index=False))
    print(f"Figures written to {out_dir}")
