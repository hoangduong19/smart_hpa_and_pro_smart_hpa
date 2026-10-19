# Combines every run of one scenario into trend charts, rebuilt after each run so the trend is visible as data grows.
# Reads results/<scenario>/<autoscaler>/run<N>/metrics.csv (+ locust_stats.csv) and writes results/<scenario>/comparison/:
#   all_runs.csv        one row per run: Table 1 application-level metrics + p95 latency + failure rate
#   fig_runs.png        one panel per metric, x = run number, the autoscalers' points of the same run joined
#                       by a line -> if every line tilts the same way, the trend is consistent across runs
#   fig_means.png       mean of each metric per autoscaler (paper Fig. 6 style) with every run drawn as a dot
#   comparison.md       per-run table + consistency table ("Smart HPA better in k/n runs", with the exact
#                       Mann-Whitney U p-value of the two groups of runs) + mean +/- std
#
# Autoscalers without runs in the scenario are left out (ProSmart HPA only runs in 2R-20%).
# Runs are paired by run number. Trial runs (run0) are skipped unless --include-trials is given.
#
# With --c3 the autoscalers are K8s HPA, Smart HPA and Smart HPA + priority (improvement C3) and the output folder is
# results/<scenario>/comparison_c3, so the default comparison keeps its three autoscalers and its numbers.
# With --c3-control they are Smart HPA, its control run (C3 code, every weight 1, no headroom: only the W9 fix) and
# Smart HPA + priority, written to results/<scenario>/comparison_c3_control.
#
# Usage: python make_comparison.py <results/<scenario> dir> [--include-trials] [--c3 | --c3-control]

import csv
import glob
import itertools
import os
import re
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AUTOSCALERS = [("k8shpa", "K8s HPA"), ("smarthpa", "Smart HPA"), ("prosmarthpa", "ProSmart HPA")]
C3_AUTOSCALERS = [("k8shpa", "K8s HPA"), ("smarthpa", "Smart HPA"), ("smarthpa-prio", "Smart HPA + priority")]
C3_CONTROL_AUTOSCALERS = [("smarthpa", "Smart HPA"), ("smarthpa-flat", "Smart HPA + quota fix"), ("smarthpa-prio", "Smart HPA + priority")]
NAME = dict(AUTOSCALERS + C3_AUTOSCALERS + C3_CONTROL_AUTOSCALERS)
# (autoscaler, baseline) pairs for the consistency tables, shown when both have runs
COMPARISONS = [("smarthpa", "k8shpa"), ("prosmarthpa", "smarthpa"), ("prosmarthpa", "k8shpa"),
               ("smarthpa-prio", "smarthpa"), ("smarthpa-prio", "k8shpa"),
               ("smarthpa-flat", "smarthpa"), ("smarthpa-prio", "smarthpa-flat")]
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
COLOR = {"k8shpa": "#eb6834", "smarthpa": "#2a78d6", "prosmarthpa": "#1baf7a", "smarthpa-prio": "#1baf7a", "smarthpa-flat": "#eb6834"}
MARKER = {"k8shpa": "s", "smarthpa": "o", "prosmarthpa": "^", "smarthpa-prio": "D", "smarthpa-flat": "v"}   # shape as a second channel, so identity is not color alone
# ProSmart HPA and Smart HPA + priority share the third hue, and the control run borrows K8s HPA's: they are never
# drawn together (no fourth hue of the palette stays distinguishable from the first three when every pair of points
# can meet, as in fig_runs.png)


def output_folder(argv):
    """Name of the output folder under the scenario; --c3 / --c3-control also switch AUTOSCALERS to that set."""
    if "--c3-control" in argv:
        AUTOSCALERS[:] = C3_CONTROL_AUTOSCALERS
        return "comparison_c3_control"
    if "--c3" not in argv:
        return "comparison"
    AUTOSCALERS[:] = C3_AUTOSCALERS
    return "comparison_c3"


def scenario_label(scenario_dir):
    """results/5R-50 -> '5R-50%', results/5R-50-spike -> '5R-50% spike' (improvement C2)."""
    name, spike, _ = os.path.basename(scenario_dir).partition("-spike")
    return name + "%" + (" spike" if spike else "")


def run_dirs(scenario_dir, include_trials):
    """(autoscaler, run number, run directory) of every finished run of the scenario."""
    for a, _ in AUTOSCALERS:
        for path in glob.glob(os.path.join(scenario_dir, a, "run*", "metrics.csv")):
            run_dir = os.path.dirname(path)
            n = int(re.search(r"run(\d+)$", run_dir).group(1))
            if n == 0 and not include_trials:
                continue
            yield a, n, run_dir


def load_runs(scenario_dir, include_trials):
    runs = {}                                            # (autoscaler, run) -> metrics dict
    for a, n, run_dir in run_dirs(scenario_dir, include_trials):
        app = [r for r in csv.DictReader(open(os.path.join(run_dir, "metrics.csv"), newline="")) if r["microservice"] == "APPLICATION"][0]
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


def mann_whitney_p(x, y):
    """Exact two-sided Mann-Whitney U p-value (rank-sum permutation test, mid-ranks for ties). With 5 runs per
    autoscaler the smallest possible value is 2/252 = 0.008, reached when the two groups do not overlap."""
    pooled = sorted(x + y)
    if len(x) < 2 or len(y) < 2 or len(pooled) > 20 or pooled[0] == pooled[-1]:
        return None
    rank = {v: sum(i + 1 for i, p in enumerate(pooled) if p == v) / pooled.count(v) for v in set(pooled)}
    ranks = [rank[v] for v in x + y]
    expected = len(x) * (len(pooled) + 1) / 2
    observed = abs(sum(ranks[:len(x)]) - expected)
    sums = [abs(sum(c) - expected) for c in itertools.combinations(ranks, len(x))]
    return sum(1 for d in sums if d >= observed - 1e-9) / len(sums)


def consistency_lines(runs, comparisons, metrics):
    lines = []
    for a, b in comparisons:
        paired = paired_runs(runs, a, b)
        lines += ["", f"## Consistency ({NAME[a]} vs {NAME[b]}, same run number)", "",
                  f"Paired runs: {paired or 'none yet'}. p = exact two-sided Mann-Whitney U over all runs of the two autoscalers.", "",
                  f"| Metric | Better is | {NAME[a]} better in | p | Per run ({NAME[a]} vs {NAME[b]}) |", "|---|---|---|---|---|"]
        for key, label, hib in metrics:
            cells, wins = [], 0
            for n in paired:
                s, k = runs[(a, n)][key], runs[(b, n)][key]
                w = better(key, hib, s, k)
                wins += bool(w)
                cells.append(f"run{n}: {s:,.1f} vs {k:,.1f} {'✅' if w else ('➖' if w is None else '❌')}")
            p = mann_whitney_p(*[[m[key] for (aa, _), m in sorted(runs.items()) if aa == g] for g in (a, b)])
            lines.append(f"| {label} | {'higher' if hib else 'lower'} | {wins}/{len(paired)} | "
                         f"{'-' if p is None else f'{p:.3f}'} | {'; '.join(cells)} |")
    return lines


def means_lines(runs, present, metrics):
    lines = ["", "## Mean ± standard deviation", "", "| Metric | " + " | ".join(NAME[a] for a in present) + " |",
             "|---|" + "---|" * len(present)]
    for key, label, _ in metrics:
        row = []
        for a in present:
            vals = [m[key] for (aa, _), m in runs.items() if aa == a]
            row.append(f"{statistics.mean(vals):,.2f}" + (f" ± {statistics.stdev(vals):,.2f}" if len(vals) > 1 else "") + f" (n={len(vals)})")
        lines.append(f"| {label} | " + " | ".join(row) + " |")
    return lines


def fig_runs(runs, present, comparisons, scenario, out, metrics=METRICS):
    fig, axes = plt.subplots(3, 3, figsize=(15, 10.5), facecolor=SURFACE)
    fig.suptitle(f"{scenario}: every run, {' vs '.join(NAME[a] for a in present)} (same run joined)", x=0.01, ha="left",
                 fontsize=14, color=INK, fontweight="bold")
    for ax in axes.flatten()[len(metrics):]:
        ax.set_visible(False)
    for ax, (key, label, hib) in zip(axes.flatten(), metrics):
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
    scenario = scenario_label(scenario_dir)
    out_dir = os.path.join(scenario_dir, output_folder(sys.argv))
    runs = load_runs(scenario_dir, include_trials)
    if not runs:
        print(f"No runs with metrics.csv under {scenario_dir}")
        return
    present = [a for a, _ in AUTOSCALERS if any(aa == a for aa, _ in runs)]
    comparisons = [(a, b) for a, b in COMPARISONS if a in present and b in present]

    os.makedirs(out_dir, exist_ok=True)

    keys = [k for k, _, _ in METRICS]
    with open(os.path.join(out_dir, "all_runs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "autoscaler", "run"] + keys)
        for (a, n), m in sorted(runs.items(), key=lambda x: (x[0][1], x[0][0])):
            w.writerow([scenario, a, n] + [round(m[k], 3) for k in keys])

    lines = [f"# Comparison: {scenario}", "",
             f"Runs found: {', '.join(f'{a} run{n}' for a, n in sorted(runs))}."]
    lines += consistency_lines(runs, comparisons, METRICS) + means_lines(runs, present, METRICS)
    lines += ["", "Figures: `fig_runs.png` (per run, consistency), `fig_means.png` (means, paper Fig. 6 style)."]
    with open(os.path.join(out_dir, "comparison.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    fig_runs(runs, present, comparisons, scenario, os.path.join(out_dir, "fig_runs.png"))
    fig_means(runs, present, scenario, os.path.join(out_dir, "fig_means.png"))
    print(f"Comparison written to {out_dir}")


if __name__ == "__main__":
    main()
