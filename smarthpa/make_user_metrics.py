# User-side metrics of one scenario (plan.md section 7, improvement C1): what the load test's users experienced,
# which the paper's Table 1 (CPU metrics only) does not measure.
# Reads results/<scenario>/<autoscaler>/run<N>/locust_stats_history.csv and writes results/<scenario>/comparison/:
#   user_metrics.csv        one row per run
#   user_metrics.md         per-run consistency tables (with Mann-Whitney U p-value) + mean +/- std
#   fig_user_runs.png       one panel per metric, every run (same layout as fig_runs.png)
#   fig_user_timeline.png   p95 response time and throughput over the test, median of the runs of each autoscaler
#
# Locust writes one history row per second; with --csv-full-history its percentile columns cover the last ~10 s
# (not the whole test), so they follow the load. A phase value below is the mean of those per-second values.
#   ramp phase       0-5 min, users rise from 0 to the maximum
#   high-load phase  5-15 min, all users active
# A spike scenario (folder name ending in -spike, improvement C2, stages from locustfile_spike.py) uses other phases:
#   spike phase      both 250-user stages (3-7 and 10-13 min)
#   spike onset      the first minute of each spike, while the autoscaler is still reacting
#   base after spike the 50-user stages after a spike (7-10 and 13-15 min), when replicas and quota should come back
#
# Usage: python make_user_metrics.py <results/<scenario> dir> [--include-trials] [--c3]     (--c3: see make_comparison.py)

import csv
import os
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from make_comparison import (AUTOSCALERS, COMPARISONS, COLOR, GRID, INK, INK_2, MARKER, NAME, SURFACE,
                             consistency_lines, fig_runs, means_lines, output_folder, run_dirs, scenario_label,
                             style_axis)

RAMP_END_SEC = 300              # 200 users at 0.67 users/s
SLO_P95_MS = 1000               # service-level objective for the SLO metric: p95 response time of at most 1 s
BIN_SEC = 15                    # resolution of the timeline figure
HOME, CHECKOUT = ("GET", "/"), ("POST", "/cart/checkout")

# phase -> list of (start s, end s); the ramp load of the paper
PHASES = {"ramp": [(0, RAMP_END_SEC)], "high": [(RAMP_END_SEC, float("inf"))]}

# (key, label, True if higher is better)
METRICS = [
    ("p50_high_ms", "Median response time, high load (ms)", False),
    ("p95_high_ms", "p95 response time, high load (ms)", False),
    ("p99_high_ms", "p99 response time, high load (ms)", False),
    ("p95_ramp_ms", "p95 response time, ramp (ms)", False),
    ("slo_violation_pct", f"Time with p95 > {SLO_P95_MS} ms, high load (%)", False),
    ("rps_high", "Throughput, high load (requests/s)", True),
    ("failed_requests", "Failed requests (count)", False),
    ("p95_home_high_ms", "p95 home page, high load (ms)", False),
    ("p95_checkout_high_ms", "p95 checkout, high load (ms)", False),
]


def spike_phases():
    from locustfile_spike import STAGES
    starts = [0] + [end for end, _, _ in STAGES[:-1]]
    stages = [(start, end, users) for start, (end, users, _) in zip(starts, STAGES)]
    peak = max(users for _, _, users in stages)
    spikes = [(a, b) for a, b, u in stages if u == peak]
    return {"spike": spikes,
            "onset": [(a, a + 60) for a, _ in spikes],
            "base": [(a, b) for a, b, u in stages if u < peak and a >= spikes[0][1]]}


SPIKE_METRICS = [
    ("p50_spike_ms", "Median response time, spikes (ms)", False),
    ("p95_spike_ms", "p95 response time, spikes (ms)", False),
    ("p99_spike_ms", "p99 response time, spikes (ms)", False),
    ("p95_onset_ms", "p95 response time, first minute of a spike (ms)", False),
    ("p95_base_ms", "p95 response time, base load after a spike (ms)", False),
    ("slo_violation_pct", f"Time with p95 > {SLO_P95_MS} ms, spikes (%)", False),
    ("rps_spike", "Throughput, spikes (requests/s)", True),
    ("failed_requests", "Failed requests (count)", False),
    ("p95_checkout_spike_ms", "p95 checkout, spikes (ms)", False),
]


def load_history(run_dir):
    """(method, name) -> rows of one endpoint, with t = seconds since the first history row."""
    series = {}
    with open(os.path.join(run_dir, "locust_stats_history.csv"), newline="", encoding="utf-8") as f:
        t0 = None
        for r in csv.DictReader(f):
            t0 = int(r["Timestamp"]) if t0 is None else t0
            series.setdefault((r["Type"], r["Name"]), []).append({
                "t": int(r["Timestamp"]) - t0,
                "requests": int(r["Total Request Count"]), "failures": int(r["Total Failure Count"]),
                "rps": float(r["Requests/s"]),
                **{p: (None if r[p] == "N/A" else float(r[p])) for p in ("50%", "95%", "99%")}})
    return series


def in_phase(rows, intervals):
    return [r for r in rows if any(a <= r["t"] < b for a, b in intervals)]


def phase_mean(rows, column, intervals):
    return statistics.mean(r[column] for r in in_phase(rows, intervals) if r[column] is not None)


def phase_rps(rows, intervals):
    """Requests per second over the phase, from the cumulative request count of each interval."""
    requests = seconds = 0
    for interval in intervals:
        part = in_phase(rows, [interval])
        requests += part[-1]["requests"] - part[0]["requests"]
        seconds += part[-1]["t"] - part[0]["t"]
    return requests / seconds


def slo_violation_pct(rows, intervals):
    p95 = [r["95%"] for r in in_phase(rows, intervals) if r["95%"] is not None]
    return 100 * sum(1 for v in p95 if v > SLO_P95_MS) / len(p95)


def user_metrics(series):
    total = series[("", "Aggregated")]
    return {
        "p50_high_ms": phase_mean(total, "50%", PHASES["high"]),
        "p95_high_ms": phase_mean(total, "95%", PHASES["high"]),
        "p99_high_ms": phase_mean(total, "99%", PHASES["high"]),
        "p95_ramp_ms": phase_mean(total, "95%", PHASES["ramp"]),
        "slo_violation_pct": slo_violation_pct(total, PHASES["high"]),
        "rps_high": phase_rps(total, PHASES["high"]),
        "failed_requests": total[-1]["failures"],
        "p95_home_high_ms": phase_mean(series[HOME], "95%", PHASES["high"]),
        "p95_checkout_high_ms": phase_mean(series[CHECKOUT], "95%", PHASES["high"]),
    }


def spike_user_metrics(series, phases):
    total = series[("", "Aggregated")]
    return {
        "p50_spike_ms": phase_mean(total, "50%", phases["spike"]),
        "p95_spike_ms": phase_mean(total, "95%", phases["spike"]),
        "p99_spike_ms": phase_mean(total, "99%", phases["spike"]),
        "p95_onset_ms": phase_mean(total, "95%", phases["onset"]),
        "p95_base_ms": phase_mean(total, "95%", phases["base"]) if phases["base"] else float("nan"),
        "slo_violation_pct": slo_violation_pct(total, phases["spike"]),
        "rps_spike": phase_rps(total, phases["spike"]),
        "failed_requests": total[-1]["failures"],
        "p95_checkout_spike_ms": phase_mean(series[CHECKOUT], "95%", phases["spike"]),
    }


def binned(rows, column):
    """bin start (s) -> mean of the column in that bin."""
    bins = {}
    for r in rows:
        if r[column] is not None:
            bins.setdefault(r["t"] // BIN_SEC * BIN_SEC, []).append(r[column])
    return {t: statistics.mean(v) for t, v in bins.items()}


def fig_timeline(histories, present, scenario, out, spikes=None):
    panels = [("95%", "p95 response time (ms)"), ("rps", "Throughput (requests/s)")]
    fig, axes = plt.subplots(2, 1, figsize=(11, 7.5), facecolor=SURFACE, sharex=True)
    fig.suptitle(f"{scenario}: what users experienced over the test (line = median of the runs, band = min to max)",
                 x=0.01, ha="left", fontsize=13, color=INK, fontweight="bold")
    for ax, (column, label) in zip(axes, panels):
        style_axis(ax)
        ends, peak, highest = [], 0, 0
        for a in present:
            runs = [binned(h[("", "Aggregated")], column) for (aa, _), h in sorted(histories.items()) if aa == a]
            # the last bin is cut short when Locust stops, so it is left out
            ts = sorted(t for t in set.intersection(*[set(r) for r in runs]) if t < max(max(r) for r in runs))
            x = [(t + BIN_SEC / 2) / 60 for t in ts]
            mid = [statistics.median(r[t] for r in runs) for t in ts]
            upper = [max(r[t] for r in runs) for t in ts]
            ax.fill_between(x, [min(r[t] for r in runs) for t in ts], upper, color=COLOR[a], alpha=0.14, linewidth=0)
            ax.plot(x, mid, color=COLOR[a], linewidth=2, label=f"{NAME[a]} (n={len(runs)})")
            ax.scatter(x[::8], mid[::8], s=34, color=COLOR[a], marker=MARKER[a], edgecolors=SURFACE, linewidths=1.5, zorder=3)
            ends.append([statistics.mean(mid[-8:]), a])
            peak, highest = max(peak, max(mid)), max(highest, max(upper))
        # a single run's spike (a few seconds of errors) would flatten every line, so the axis follows the median
        # lines and says how far the clipped band goes
        top = min(1.8 * peak, 1.08 * highest)
        ax.set_ylim(0, top)
        if highest > top:
            ax.text(14.9, top * 0.97, f"band clipped, highest value in one run: {highest:,.0f}", fontsize=8, color=INK_2, ha="right", va="top")
        # direct labels at the right edge, pushed apart so they never overlap
        ends.sort()
        for i in range(1, len(ends)):
            ends[i][0] = max(ends[i][0], ends[i - 1][0] + 0.055 * top)
        for y, a in ends:
            ax.text(15.15, y, NAME[a], fontsize=9, color=INK, va="center")
        if spikes:
            for a, b in spikes:
                ax.axvspan(a / 60, b / 60, color=GRID, alpha=0.5, linewidth=0, zorder=0)
                ax.text(a / 60 + 0.1, top * 0.97, "spike", fontsize=8, color=INK_2, va="top")
        else:
            ax.axvline(RAMP_END_SEC / 60, color=INK_2, linewidth=1, linestyle=":")
            ax.text(RAMP_END_SEC / 60 + 0.1, top * 0.97, "all users active", fontsize=8, color=INK_2, va="top")
        if column == "95%":
            ax.axhline(SLO_P95_MS, color=INK_2, linewidth=1, linestyle="--")
            ax.text(0.05, SLO_P95_MS + top * 0.015, f"SLO {SLO_P95_MS} ms", fontsize=8, color=INK_2)
        ax.set_title(label, fontsize=10, color=INK, loc="left")
    axes[0].legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=9, labelcolor=INK, ncol=len(present))
    axes[1].set_xlabel("Test time (min)", fontsize=9, color=INK_2)
    axes[1].set_xlim(0, 15)
    axes[1].set_xticks(range(0, 16))
    fig.tight_layout(rect=(0, 0, 0.93, 0.95))
    fig.savefig(out, dpi=130, facecolor=SURFACE)
    plt.close(fig)


def main():
    scenario_dir = os.path.normpath(sys.argv[1])
    scenario = scenario_label(scenario_dir)
    out_dir = os.path.join(scenario_dir, output_folder(sys.argv))
    histories = {(a, n): load_history(d) for a, n, d in run_dirs(scenario_dir, "--include-trials" in sys.argv)}
    if not histories:
        print(f"No runs under {scenario_dir}")
        return
    spike = scenario_dir.endswith("-spike")
    phases = spike_phases() if spike else PHASES
    metrics = SPIKE_METRICS if spike else METRICS
    if spike:
        # trial runs stop early; keep only the part of each phase the shortest run reached
        last = min(h[("", "Aggregated")][-1]["t"] for h in histories.values())
        phases = {k: [(a, min(b, last)) for a, b in v if a < last] for k, v in phases.items()}
        runs = {k: spike_user_metrics(h, phases) for k, h in histories.items()}
    else:
        runs = {k: user_metrics(h) for k, h in histories.items()}
    present = [a for a, _ in AUTOSCALERS if any(aa == a for aa, _ in runs)]
    comparisons = [(a, b) for a, b in COMPARISONS if a in present and b in present]

    os.makedirs(out_dir, exist_ok=True)
    keys = [k for k, _, _ in metrics]
    with open(os.path.join(out_dir, "user_metrics.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "autoscaler", "run"] + keys)
        for (a, n), m in sorted(runs.items(), key=lambda x: (x[0][1], x[0][0])):
            w.writerow([scenario, a, n] + [round(m[k], 3) for k in keys])

    minutes = lambda v: " + ".join(f"{a / 60:g}-{b / 60:g}" for a, b in v)
    phase_text = (f"Spikes = minute {minutes(phases['spike'])}, first minute of a spike = {minutes(phases['onset'])}, "
                  f"base load after a spike = {minutes(phases['base'])}. " if spike else
                  "Ramp = minute 0-5, high load = minute 5-15 (all users active). ")
    lines = [f"# User-side metrics: {scenario}", "",
             f"From `locust_stats_history.csv` of {len(runs)} runs. {phase_text}"
             f"Response-time values are means of Locust's per-second percentiles (each over the last ~10 s). "
             f"SLO: p95 of at most {SLO_P95_MS} ms."]
    lines += consistency_lines(runs, comparisons, metrics) + means_lines(runs, present, metrics)
    lines += ["", "Figures: `fig_user_runs.png` (per run, consistency), `fig_user_timeline.png` (p95 and throughput over time)."]
    with open(os.path.join(out_dir, "user_metrics.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    fig_runs(runs, present, comparisons, scenario, os.path.join(out_dir, "fig_user_runs.png"), metrics)
    fig_timeline(histories, present, scenario, os.path.join(out_dir, "fig_user_timeline.png"),
                 phases["spike"] if spike else None)
    print(f"User-side metrics written to {out_dir}")


if __name__ == "__main__":
    main()
