# Redraws the two result figures of the paper (Ahmad et al., JSS 2025) from our runs, in the paper's layout, so the
# report can put ours next to theirs:
#   results/fig6_services.png    paper Fig. 6: per scenario, Supply CPU / CPU Overutilization / CPU Overprovision /
#                                CPU Underprovision as columns stacked by microservice, Smart HPA vs K8s HPA, with the
#                                matching time metric under each column. Values = mean over runs.
#   results/fig6_services.csv    the numbers behind fig6 (table view), per scenario, autoscaler and microservice
#   results/<scenario>/comparison/fig7_timeline.png
#                                paper Fig. 7: (a)/(b) CPU demand (solid) vs capacity (dashed) over time,
#                                (c)/(d) CPU utilization vs threshold, Smart HPA left, K8s HPA right.
#                                Mean over runs on a 5 s grid (the paper's curves are smooth, most likely averaged too);
#                                --run N draws a single run instead (fig7_timeline_runN.png).
#
# Differences from the paper's drawing, on purpose (dataviz rules: at most 8 categorical colors, color follows the
# entity in every figure):
#   - Fig. 6 colors 7 microservices; payment, shipping, email and redis-cart are summed as "other services" (they are
#     small in every metric except Overprovision, where they are the idle donors).
#   - Fig. 7 colors the 4 services the paper's story is about (frontend and currency receive quota, cart and adservice
#     give it away); the other 7 are thin gray lines for context.
#
# Run folders: run<N> with N >= 1 (run0 = smoke test, skipped), as in make_comparison.py.
#
# Usage: python make_paper_figs.py <results dir> [--run N]

import bisect
import csv
import glob
import json
import os
import re
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from make_run_report import SERVICES, load_kb

AUTOSCALERS = [("smarthpa", "Smart HPA"), ("k8shpa", "K8s HPA")]      # paper order: Smart HPA first

# Reference palette (dataviz skill, light mode), categorical slots 1-7 in slot order = stacking order (adjacent pairs
# validated). adservice takes slot 7 (violet) rather than 4 (yellow) because Fig. 7 draws it as a line next to
# currency (orange), and yellow/orange fail the all-pairs check.
SURFACE, INK, INK_2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e6e5e0"
OTHER_COLOR = "#c3c2b7"
NAMED = [
    ("frontend", "frontend", "#2a78d6"),
    ("currencyservice", "currency", "#eb6834"),
    ("cartservice", "cart", "#1baf7a"),
    ("checkoutservice", "checkout", "#eda100"),
    ("productcatalogservice", "productcatalog", "#e87ba4"),
    ("recommendationservice", "recommendation", "#008300"),
    ("adservice", "adservice", "#4a3aa7"),
]
OTHER = [s for s in SERVICES if s not in {n for n, _, _ in NAMED}]
COLOR = {n: c for n, _, c in NAMED}
SHORT = {n: l for n, l, _ in NAMED}
FOCUS = ["frontend", "currencyservice", "cartservice", "adservice"]

# (resource metric, panel title, time metric shown under the column or None)
FIG6_PANELS = [
    ("supply_cpu_m", "Supply CPU (m) - higher is better", None),
    ("cpu_overutilization_pct", "CPU Overutilization (%) - lower", "overutilization_time_min"),
    ("cpu_overprovision_m", "CPU Overprovision (m) - lower", "overprovision_time_min"),
    ("cpu_underprovision_m", "CPU Underprovision (m) - lower", "underprovision_time_min"),
]

GRID_SEC, DURATION_SEC = 5, 900


def run_dirs(scenario_dir, autoscaler):
    out = []
    for d in glob.glob(os.path.join(scenario_dir, autoscaler, "run*")):
        m = re.search(r"run(\d+)$", d)
        if m and int(m.group(1)) >= 1 and os.path.exists(os.path.join(d, "metrics.csv")):
            out.append((int(m.group(1)), d))
    return sorted(out)


def scenarios(results_dir):
    return sorted(d for d in glob.glob(os.path.join(results_dir, "*"))
                  if os.path.isdir(d) and all(run_dirs(d, a) for a, _ in AUTOSCALERS))


def style_axis(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=8, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- Fig. 6

def mean_metrics(scenario_dir, autoscaler):
    """{microservice or APPLICATION: {metric: mean over runs}}, number of runs"""
    acc = {}
    dirs = run_dirs(scenario_dir, autoscaler)
    for _, d in dirs:
        for r in csv.DictReader(open(os.path.join(d, "metrics.csv"), newline="")):
            for k, v in r.items():
                if k not in ("autoscaler", "scenario", "run", "microservice"):
                    acc.setdefault(r["microservice"], {}).setdefault(k, []).append(float(v))
    return {s: {k: statistics.mean(v) for k, v in m.items()} for s, m in acc.items()}, len(dirs)


def stack_groups(per_service, key):
    groups = [(SHORT[n], COLOR[n], per_service[n][key]) for n, _, _ in NAMED]
    groups.append(("other services", OTHER_COLOR, sum(per_service[s][key] for s in OTHER)))
    return groups


def fig6(results_dir, scen_dirs):
    fig, axes = plt.subplots(len(scen_dirs), 4, figsize=(15, 4.3 * len(scen_dirs) + 1.2), facecolor=SURFACE, squeeze=False)
    fig.suptitle("Results per scenario, stacked by microservice (paper Fig. 6 layout) - mean over runs",
                 x=0.01, ha="left", fontsize=14, color=INK, fontweight="bold")
    rows = []
    for row, sd in zip(axes, scen_dirs):
        scenario = os.path.basename(sd) + "%"
        data = {a: mean_metrics(sd, a) for a, _ in AUTOSCALERS}
        ns = ", ".join(f"{name} n={data[a][1]}" for a, name in AUTOSCALERS)
        for ax, (key, title, tkey) in zip(row, FIG6_PANELS):
            style_axis(ax)
            ticks = []
            for i, (a, name) in enumerate(AUTOSCALERS):
                per_service = data[a][0]
                bottom = 0
                for label, color, v in stack_groups(per_service, key):
                    # 2px surface-colored edge = the gap between stacked segments
                    ax.bar(i, v, bottom=bottom, width=0.5, color=color, edgecolor=SURFACE, linewidth=1.5)
                    bottom += v
                    rows.append([scenario, a, label, key, round(v, 3)])
                total = per_service["APPLICATION"][key]
                ax.text(i, total, f"{total:,.0f}", ha="center", va="bottom", fontsize=9, color=INK)
                ticks.append(name + (f"\n{per_service['APPLICATION'][tkey]:.2f} min" if tkey else ""))
                if tkey:
                    rows.append([scenario, a, "APPLICATION", tkey, round(per_service["APPLICATION"][tkey], 3)])
            ax.set_xticks([0, 1])
            ax.set_xticklabels(ticks, fontsize=9, color=INK)
            ax.set_xlim(-0.6, 1.6)
            ax.set_ylim(0, max(data[a][0]["APPLICATION"][key] for a, _ in AUTOSCALERS) * 1.12 or 1)   # room for the totals
            ax.set_title(title, fontsize=10, color=INK, loc="left")
        row[0].text(0, 1.16, f"{scenario}  ({ns})", transform=row[0].transAxes, fontsize=12, color=INK, fontweight="bold")
    handles = [Patch(color=c, label=l) for _, l, c in NAMED] + [Patch(color=OTHER_COLOR, label="other services (" + ", ".join(s.replace("service", "") for s in OTHER) + ")")]
    fig.legend(handles=handles, loc="lower center", ncol=8, frameon=False, fontsize=9, labelcolor=INK,
               handlelength=1.2, columnspacing=1.4)
    fig.text(0.5, 0.045, "Number under a column = the matching time metric (Overutilization / Overprovision / Underprovision Time). "
             "Overprovision Time: higher is better.", ha="center", fontsize=9, color=INK_2)
    fig.tight_layout(rect=(0, 0.07, 1, 0.95), h_pad=3)
    fig.savefig(os.path.join(results_dir, "fig6_services.png"), dpi=130, facecolor=SURFACE)
    plt.close(fig)
    with open(os.path.join(results_dir, "fig6_services.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "autoscaler", "microservice", "metric", "mean_over_runs"])
        w.writerows(rows)


# ---------------------------------------------------------------- Fig. 7

def resample(t, values, grid):
    """step-hold: value of the last KB row at or before each grid time"""
    out = []
    for g in grid:
        i = bisect.bisect_right(t, g) - 1
        out.append(values[max(i, 0)])
    return out


def timeline(scenario_dir, autoscaler, only_run):
    """{service: {"demand"|"capacity"|"cpu_pct": series on the grid}} averaged over runs, number of runs"""
    grid = list(range(0, DURATION_SEC + 1, GRID_SEC))
    dirs = [d for n, d in run_dirs(scenario_dir, autoscaler) if only_run is None or n == only_run]
    out = {}
    for s in SERVICES:
        per_run = {k: [] for k in ("demand", "capacity", "cpu_pct")}
        for d in dirs:
            kb = load_kb(d, s)
            for k in per_run:
                per_run[k].append(resample(kb["t"], kb[k], grid))
        out[s] = {k: [statistics.mean(col) for col in zip(*v)] for k, v in per_run.items()}
    return [g / 60 for g in grid], out, len(dirs)


def end_labels(ax, t, series, services):
    """service name at the right end of its line, skipped when it would collide with a label already placed"""
    lo, hi = ax.get_ylim()
    placed = []
    for s in sorted(services, key=lambda s: -series[s][-1]):
        y = series[s][-1]
        if all(abs(y - p) > 0.045 * (hi - lo) for p in placed):
            ax.text(t[-1] + 0.15, y, SHORT[s], fontsize=8, color=INK_2, va="center", ha="left")
            placed.append(y)


def fig7(scenario_dir, threshold, only_run):
    scenario = os.path.basename(scenario_dir) + "%"
    data = {a: timeline(scenario_dir, a, only_run) for a, _ in AUTOSCALERS}
    fig, axes = plt.subplots(2, 2, figsize=(15, 9.5), facecolor=SURFACE, sharex=True)
    how = f"run {only_run}" if only_run else "mean over runs (" + ", ".join(f"{n} n={data[a][2]}" for a, n in AUTOSCALERS) + ")"
    fig.suptitle(f"{scenario}: CPU demand, capacity and utilization over time (paper Fig. 7 layout) - {how}",
                 x=0.01, ha="left", fontsize=14, color=INK, fontweight="bold")
    letters = iter("abcd")
    for row, kind in enumerate(("demand", "cpu_pct")):
        ymax = 0
        for col, (a, name) in enumerate(AUTOSCALERS):
            ax = axes[row][col]
            style_axis(ax)
            t, series, _ = data[a]
            for s in [x for x in SERVICES if x not in FOCUS] + FOCUS:          # focus lines drawn on top
                color, width = (COLOR[s], 2) if s in FOCUS else (OTHER_COLOR, 1)
                if kind == "demand":
                    ax.plot(t, series[s]["demand"], color=color, linewidth=width, solid_capstyle="round")
                    ax.plot(t, series[s]["capacity"], color=color, linewidth=width * 0.8, linestyle=(0, (4, 2)))
                    ymax = max(ymax, max(series[s]["demand"]), max(series[s]["capacity"]))
                else:
                    ax.plot(t, series[s]["cpu_pct"], color=color, linewidth=width, solid_capstyle="round")
                    ymax = max(ymax, max(series[s]["cpu_pct"]))
            if kind == "cpu_pct":
                ax.axhline(threshold, color=INK, linewidth=1.2, linestyle=(0, (2, 2)))
            title = "CPU demand vs CPU capacity (milliCPU)" if kind == "demand" else "CPU utilization (% of request)"
            ax.set_title(f"({next(letters)}) {name} - {title}", fontsize=11, color=INK, loc="left")
            ax.set_xlim(0, 15)
        for col, (a, _) in enumerate(AUTOSCALERS):
            ax = axes[row][col]
            ax.set_ylim(0, ymax * 1.08)
            t, series, _ = data[a]
            end_labels(ax, t, {s: series[s]["demand" if kind == "demand" else "cpu_pct"] for s in FOCUS}, FOCUS)
    for ax in axes[1]:
        ax.set_xlabel("Test time (min)", fontsize=9, color=INK_2)
    handles = [Line2D([], [], color=COLOR[s], linewidth=2, label=SHORT[s]) for s in FOCUS]
    handles += [Line2D([], [], color=OTHER_COLOR, linewidth=1, label="other 7 services"),
                Line2D([], [], color=INK_2, linewidth=2, label="CPU demand (solid)"),
                Line2D([], [], color=INK_2, linewidth=1.6, linestyle=(0, (4, 2)), label="CPU capacity (dashed)"),
                Line2D([], [], color=INK, linewidth=1.2, linestyle=(0, (2, 2)), label=f"CPU threshold {threshold}%")]
    fig.legend(handles=handles, loc="lower center", ncol=8, frameon=False, fontsize=9, labelcolor=INK)
    fig.tight_layout(rect=(0, 0.04, 0.98, 0.95))
    name = f"fig7_timeline_run{only_run}.png" if only_run else "fig7_timeline.png"
    out_dir = os.path.join(scenario_dir, "comparison")
    os.makedirs(out_dir, exist_ok=True)
    fig.savefig(os.path.join(out_dir, name), dpi=130, facecolor=SURFACE)
    plt.close(fig)


def main():
    results_dir = os.path.normpath(sys.argv[1])
    only_run = int(sys.argv[sys.argv.index("--run") + 1]) if "--run" in sys.argv else None
    scen_dirs = scenarios(results_dir)
    if not scen_dirs:
        print(f"No scenario with runs of both autoscalers under {results_dir}")
        return
    fig6(results_dir, scen_dirs)
    for sd in scen_dirs:
        first = run_dirs(sd, "smarthpa")[0][1]
        threshold = int(json.load(open(os.path.join(first, "run_info.json"), encoding="utf-8-sig"))["cpu_threshold"])
        fig7(sd, threshold, only_run)
    print(f"Figures written: {os.path.join(results_dir, 'fig6_services.png')} and fig7_timeline per scenario")


if __name__ == "__main__":
    main()
