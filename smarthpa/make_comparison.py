# Combines every run of one scenario into trend charts, rebuilt after each run so the trend is visible as data grows.
# Reads results/<scenario>/<autoscaler>/run<N>/metrics.csv (+ locust_stats.csv) and writes results/<scenario>/comparison/:
#   all_runs.csv        one row per run: Table 1 application-level metrics + p95 latency + failure rate
#   fig_runs.png        one panel per metric, x = run number, the autoscalers' points of the same run joined
#                       by a line -> if every line tilts the same way, the trend is consistent across runs
#   fig_means.png       mean of each metric per autoscaler (paper Fig. 6 style) with every run drawn as a dot
#   comparison.md       per-run table + consistency table ("Smart HPA better in k/n runs") + mean +/- std
#
# Autoscalers without runs in the scenario are left out (ProSmart HPA only runs in 2R-20%).
# Runs are paired by run number. Trial runs (run0) are skipped unless --include-trials is given.
#
# Usage: python make_comparison.py <results/<scenario> dir> [--include-trials]

import csv
import glob
import os
import re
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AUTOSCALERS = [("k8shpa", "K8s HPA"), ("smarthpa", "Smart HPA"), ("prosmarthpa", "ProSmart HPA")]
NAME = dict(AUTOSCALERS)
# (autoscaler, baseline) pairs for the consistency tables, shown when both have runs
COMPARISONS = [("smarthpa", "k8shpa"), ("prosmarthpa", "smarthpa"), ("prosmarthpa", "k8shpa")]
# (key, label, True if higher is better)
METRICS = [
    ("supply_cpu_m", "Supply CPU (m)", True),
    ("cpu_overutilization_pct", "CPU Overutilization (%)", False),
    ("overutilization_time_min", "Overutilization Time (min)", False),
    ("cpu_overprovision_m", "CPU Overprovision (m)", False),
    ("overprovision_time_min", "Overprovision Time (min)", True),
    ("cpu_underprovision_m", "CPU Underprovision (m)", False),
    ("underprovision_time_min", "Underprovision Time (min)", False),
    ("p95_ms", "p95 response time (ms)", False),
    ("failure_pct", "Failed requests (%)", False),
]

# Reference palette (dataviz skill, light mode), categorical slots 1-3.
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
COLOR = {"k8shpa": "#eb6834", "smarthpa": "#2a78d6", "prosmarthpa": "#1baf7a"}
MARKER = {"k8shpa": "s", "smarthpa": "o", "prosmarthpa": "^"}   # shape as a second channel, so identity is not color alone


def load_runs(scenario_dir, include_trials):
    runs = {}                                            # (autoscaler, run) -> metrics dict
    for a, _ in AUTOSCALERS:
        for path in glob.glob(os.path.join(scenario_dir, a, "run*", "metrics.csv")):
            run_dir = os.path.dirname(path)
            n = int(re.search(r"run(\d+)$", run_dir).group(1))
            if n == 0 and not include_trials:
                continue
            app = [r for r in csv.DictReader(open(path, newline="")) if r["microservice"] == "APPLICATION"][0]
            m = {k: float(app[k]) for k, _, _ in METRICS if k in app}
            total = [r for r in csv.DictReader(open(os.path.join(run_dir, "locust_stats.csv"), newline="")) if r["Name"] == "Aggregated"][0]
            m["p95_ms"] = float(total["95%"])
            m["failure_pct"] = 100 * float(total["Failure Count"]) / max(float(total["Request Count"]), 1)
            runs[(a, n)] = m
    return runs


def style_axis(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=8, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def better(key, higher_is_better, smart, k8s):
    if smart == k8s:
        return None
    return (smart > k8s) == higher_is_better


def paired_runs(runs, a, b):
    return sorted(n for (aa, n) in runs if aa == a and (b, n) in runs)


def fig_runs(runs, present, comparisons, scenario, out):
    fig, axes = plt.subplots(3, 3, figsize=(15, 10.5), facecolor=SURFACE)
    fig.suptitle(f"{scenario}: every run, {' vs '.join(NAME[a] for a in present)} (same run joined)", x=0.01, ha="left",
                 fontsize=14, color=INK, fontweight="bold")
    for ax, (key, label, hib) in zip(axes.flatten(), METRICS):
        style_axis(ax)
        for n in sorted({n for (_, n) in runs}):
            vals = [runs[(a, n)][key] for a in present if (a, n) in runs]
            if len(vals) > 1:
                ax.plot([n, n], [min(vals), max(vals)], color=GRID, linewidth=2, zorder=1)
        for a in present:
            pts = sorted((n, m[key]) for (aa, n), m in runs.items() if aa == a)
            ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=60, color=COLOR[a], marker=MARKER[a],
                       edgecolors=SURFACE, linewidths=2, zorder=3, label=NAME[a])
        tags = []
        for a, b in comparisons:
            paired = paired_runs(runs, a, b)
            wins = [better(key, hib, runs[(a, n)][key], runs[(b, n)][key]) for n in paired]
            tags.append(f"{NAME[a]} better than {NAME[b]} {sum(1 for w in wins if w)}/{len(paired)}")
        tag = "\n".join(tags) if tags else "no paired runs yet"
        ax.set_title(f"{label} - {'higher' if hib else 'lower'} is better", fontsize=10, color=INK, loc="left")
        ax.set_xlabel(tag, fontsize=9, color=INK_2, loc="left")      # below the axis, so it never covers a point
        ns = sorted({n for (_, n) in runs})
        ax.set_xticks(ns)
        ax.set_xticklabels([f"run {n}" for n in ns])
        ax.set_ylim(bottom=0)
        ax.margins(x=0.15)
    axes.flatten()[0].legend(loc="lower left", frameon=False, fontsize=9, labelcolor=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out, dpi=130, facecolor=SURFACE)
    plt.close(fig)


def fig_means(runs, present, scenario, out):
    fig, axes = plt.subplots(3, 3, figsize=(15, 10.5), facecolor=SURFACE)
    fig.suptitle(f"{scenario}: mean over runs (bars) and each run (dots)", x=0.01, ha="left",
                 fontsize=14, color=INK, fontweight="bold")
    for ax, (key, label, hib) in zip(axes.flatten(), METRICS):
        style_axis(ax)
        for i, a in enumerate(present):
            vals = [m[key] for (aa, _), m in runs.items() if aa == a]
            mean = statistics.mean(vals)
            ax.bar(i, mean, width=0.55, color=COLOR[a], alpha=0.35, edgecolor=COLOR[a], linewidth=1.5)
            ax.scatter([i] * len(vals), vals, s=36, color=COLOR[a], marker=MARKER[a], edgecolors=SURFACE, linewidths=1.5, zorder=3)
            sd = statistics.stdev(vals) if len(vals) > 1 else 0
            ax.text(i, mean, f"{mean:,.1f}" + (f"\n±{sd:,.1f}" if sd else ""), ha="center", va="bottom", fontsize=8, color=INK)
        ax.set_xticks(range(len(present)))
        ax.set_xticklabels([NAME[a] for a in present], fontsize=9, color=INK)
        ax.set_title(f"{label} - {'higher' if hib else 'lower'} is better", fontsize=10, color=INK, loc="left")
        ax.set_ylim(bottom=0)
        ax.margins(y=0.2)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out, dpi=130, facecolor=SURFACE)
    plt.close(fig)


def main():
    scenario_dir = os.path.normpath(sys.argv[1])
    include_trials = "--include-trials" in sys.argv
    scenario = os.path.basename(scenario_dir) + "%"
    runs = load_runs(scenario_dir, include_trials)
    if not runs:
        print(f"No runs with metrics.csv under {scenario_dir}")
        return
    present = [a for a, _ in AUTOSCALERS if any(aa == a for aa, _ in runs)]
    comparisons = [(a, b) for a, b in COMPARISONS if a in present and b in present]

    out_dir = os.path.join(scenario_dir, "comparison")
    os.makedirs(out_dir, exist_ok=True)

    keys = [k for k, _, _ in METRICS]
    with open(os.path.join(out_dir, "all_runs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "autoscaler", "run"] + keys)
        for (a, n), m in sorted(runs.items(), key=lambda x: (x[0][1], x[0][0])):
            w.writerow([scenario, a, n] + [round(m[k], 3) for k in keys])

    lines = [f"# Comparison: {scenario}", "",
             f"Runs found: {', '.join(f'{a} run{n}' for a, n in sorted(runs))}."]
    for a, b in comparisons:
        paired = paired_runs(runs, a, b)
        lines += ["", f"## Consistency ({NAME[a]} vs {NAME[b]}, same run number)", "",
                  f"Paired runs: {paired or 'none yet'}.", "",
                  f"| Metric | Better is | {NAME[a]} better in | Per run ({NAME[a]} vs {NAME[b]}) |", "|---|---|---|---|"]
        for key, label, hib in METRICS:
            cells, wins = [], 0
            for n in paired:
                s, k = runs[(a, n)][key], runs[(b, n)][key]
                w = better(key, hib, s, k)
                wins += bool(w)
                cells.append(f"run{n}: {s:,.1f} vs {k:,.1f} {'✅' if w else ('➖' if w is None else '❌')}")
            lines.append(f"| {label} | {'higher' if hib else 'lower'} | {wins}/{len(paired)} | {'; '.join(cells)} |")
    lines += ["", "## Mean ± standard deviation", "", "| Metric | " + " | ".join(NAME[a] for a in present) + " |",
              "|---|" + "---|" * len(present)]
    for key, label, _ in METRICS:
        row = []
        for a in present:
            vals = [m[key] for (aa, _), m in runs.items() if aa == a]
            row.append(f"{statistics.mean(vals):,.2f}" + (f" ± {statistics.stdev(vals):,.2f}" if len(vals) > 1 else "") + f" (n={len(vals)})")
        lines.append(f"| {label} | " + " | ".join(row) + " |")
    lines += ["", "Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style)."]
    with open(os.path.join(out_dir, "comparison.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    fig_runs(runs, present, comparisons, scenario, os.path.join(out_dir, "fig_runs.png"))
    fig_means(runs, present, scenario, os.path.join(out_dir, "fig_means.png"))
    print(f"Comparison written to {out_dir}")


if __name__ == "__main__":
    main()
