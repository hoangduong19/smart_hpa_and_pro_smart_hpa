# Trade-off of Smart HPA and ProSmart HPA against plain Kubernetes HPA: what they cost against what they give.
#
# Cost types (one table each in the report, Section 8.2):
#   resources      Supply CPU (= CPU request of the running pods, what they reserve on the nodes), running pods in the
#                  high-load phase, and requests served per reserved vCPU (is the extra CPU used?)
#   stability      replica changes, scale reversals (flapping), quota moves: make_flapping.py, read from flapping.csv
#   reliability    failed requests per run, from Locust's own totals (locust_stats.csv, Aggregated row)
#   paper metrics  CPU Overutilization and Underprovision, which quota exchange can make worse
#   control loop   median time between two iterations of the control loop (Knowledge Base timestamps, frontend)
# Benefits: user-side p95, time with p95 > 1 s and throughput (make_user_metrics.py).
#
# Reads, per scenario, results/<scenario>/<comparison>/{all_runs,user_metrics,flapping}.csv and every run folder:
#   2R-20%        comparison_prophet_cv  K8s HPA, Smart HPA, ProSmart HPA with the authors' and with our models
#   5R-50%        comparison             K8s HPA, Smart HPA (ProSmart HPA was run at 2R-20% only)
#   5R-50% spike  comparison             K8s HPA, Smart HPA; user metrics of the spike phase (C2)
# Writes results/tradeoff/tradeoff.csv (scenario, metric, autoscaler: value over runs, change vs K8s HPA, runs better
# than K8s HPA in the same run number, exact two-sided Mann-Whitney U p) and tradeoff.md.
#
# CPU Overprovision of the paper is capacity (maxR x request) minus demand: quota nobody uses, not CPU taken from the
# nodes, so it is not a cost here.
#
# Usage: python make_tradeoff.py      (from smarthpa/, so make_run_report can be imported)

import csv
import itertools
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_run_report import load_kb  # noqa: E402

DEMO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(DEMO, "results")
HIGH_LOAD_FROM_SEC = 300

# (label, folder, comparison folder, autoscalers, user_metrics column renames for the spike phase)
SCENARIOS = [
    ("2R-20%", "2R-20", "comparison_prophet_cv", ["k8shpa", "smarthpa", "prosmarthpa-authors", "prosmarthpa-cv"], {}),
    ("5R-50%", "5R-50", "comparison", ["k8shpa", "smarthpa"], {}),
    ("5R-50% spike", "5R-50-spike", "comparison", ["k8shpa", "smarthpa"],
     {"p95_spike_ms": "p95_high_ms", "rps_spike": "rps_high"}),
]
NAME = {"k8shpa": "K8s HPA", "smarthpa": "Smart HPA", "prosmarthpa-authors": "ProSmart HPA, authors' models",
        "prosmarthpa-cv": "ProSmart HPA, our models"}

# (group, key, label, True if higher is better, aggregate over runs: mean, sum, max or count of runs > 0)
METRICS = [
    ("resources", "supply_cpu_m", "Supply CPU (m)", False, "mean"),
    ("resources", "pods_high_load", "Running pods, high load", False, "mean"),
    ("resources", "rps_per_vcpu", "Throughput per reserved vCPU (req/s)", True, "mean"),
    ("stability", "replica_changes", "Replica changes per run", False, "mean"),
    ("stability", "scale_reversals", "Scale reversals (flapping) per run", False, "mean"),
    ("stability", "maxr_changes", "Quota moves per run", False, "mean"),
    ("reliability", "failed", "Failed requests (all runs)", False, "sum"),
    ("reliability", "failed_runs", "Runs with failed requests", False, "count"),
    ("reliability", "failure_pct", "Highest failure rate in one run (%)", False, "max"),
    ("paper", "cpu_overutilization_pct", "CPU Overutilization (%)", False, "mean"),
    ("paper", "cpu_underprovision_m", "CPU Underprovision (m)", False, "mean"),
    ("loop", "loop_period_s", "Control loop period, median (s)", False, "mean"),
    ("user", "p95_high_ms", "p95 (ms)", False, "mean"),
    ("user", "slo_violation_pct", "Time with p95 > 1 s (%)", False, "mean"),
    ("user", "rps_high", "Throughput (req/s)", True, "mean"),
]


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def per_run(rows, key):
    return {(r["autoscaler"], int(r["run"])): float(r[key]) for r in rows if r.get(key) not in (None, "")}


def run_dir(folder, autoscaler, run):
    return os.path.join(RES, folder, autoscaler, f"run{run}")


def pods_high_load(folder, autoscaler, run):
    by_t = {}
    with open(os.path.join(run_dir(folder, autoscaler, run), "cluster_metrics.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if float(r["elapsed_sec"]) >= HIGH_LOAD_FROM_SEC:
                by_t[r["elapsed_sec"]] = by_t.get(r["elapsed_sec"], 0) + int(r["spec_replicas"])
    return st.mean(by_t.values())


def locust_totals(folder, autoscaler, run):
    """(requests, failures) of the whole run, Locust's Aggregated row"""
    for r in read(os.path.join(run_dir(folder, autoscaler, run), "locust_stats.csv")):
        if r["Name"] == "Aggregated":
            return int(r["Request Count"]), int(r["Failure Count"])
    raise ValueError(f"no Aggregated row in {folder}/{autoscaler}/run{run}")


def loop_period(folder, autoscaler, run):
    t = load_kb(run_dir(folder, autoscaler, run), "frontend")["t"]
    return st.median(b - a for a, b in zip(t, t[1:]))


def mann_whitney_p(a, b):
    values, n = a + b, len(a)
    u = lambda g1, g2: sum((x > y) + 0.5 * (x == y) for x in g1 for y in g2)
    obs, mu = u(a, b), len(a) * len(b) / 2
    us = [u([values[i] for i in idx], [values[i] for i in range(len(values)) if i not in idx])
          for idx in itertools.combinations(range(len(values)), n)]
    return sum(abs(x - mu) >= abs(obs - mu) - 1e-9 for x in us) / len(us)


def main():
    out, lines = [], ["# Trade-off against K8s HPA", ""]
    for label, folder, comparison, autoscalers, renames in SCENARIOS:
        base = os.path.join(RES, folder, comparison)
        user = [{renames.get(k, k): v for k, v in r.items()} for r in read(os.path.join(base, "user_metrics.csv"))]
        tables = [read(os.path.join(base, "all_runs.csv")), user, read(os.path.join(base, "flapping.csv"))]
        data = {}
        for _, key, _, _, _ in METRICS:
            for t in tables:
                if t and key in t[0]:
                    data[key] = per_run(t, key)
        runs = sorted(k for k in data["supply_cpu_m"] if k[0] in autoscalers)
        data["pods_high_load"] = {k: pods_high_load(folder, *k) for k in runs}
        data["loop_period_s"] = {k: loop_period(folder, *k) for k in runs if k[0] != "k8shpa"}
        totals = {k: locust_totals(folder, *k) for k in runs}
        data["failed"] = {k: f for k, (_, f) in totals.items()}
        data["failed_runs"] = {k: float(f > 0) for k, (_, f) in totals.items()}
        data["failure_pct"] = {k: 100 * f / n for k, (n, f) in totals.items()}
        data["rps_per_vcpu"] = {k: data["rps_high"][k] / (data["supply_cpu_m"][k] / 1000)
                                for k in runs if k in data.get("rps_high", {})}
        lines += [f"## {label}", "", "| Metric | " + " | ".join(NAME[a] for a in autoscalers) + " |",
                  "|---|" + "---|" * len(autoscalers)]
        for group, key, name, higher, agg in METRICS:
            vals = {a: {r: v for (aa, r), v in data.get(key, {}).items() if aa == a} for a in autoscalers}
            cells = []
            for a in autoscalers:
                v = vals[a]
                if not v:
                    cells.append("-")
                    continue
                value = {"mean": lambda x: st.mean(x), "sum": sum, "max": max, "count": sum}[agg](list(v.values()))
                row = {"scenario": label, "group": group, "metric": key, "label": name, "autoscaler": a,
                       "n": len(v), "value": round(value, 4)}
                k8s = vals["k8shpa"]
                if a != "k8shpa" and agg == "mean" and k8s:
                    base_mean = st.mean(k8s.values())
                    pairs = [r for r in v if r in k8s]
                    wins = sum((v[r] > k8s[r]) == higher and v[r] != k8s[r] for r in pairs)
                    p = mann_whitney_p(list(v.values()), list(k8s.values()))
                    row.update(runs_better=f"{wins}/{len(pairs)}", p_vs_k8s=round(p, 3))
                    if base_mean:
                        change = 100 * (value / base_mean - 1)
                        row["change_vs_k8s_pct"] = round(change, 2)
                        cells.append(f"{value:,.2f} ({change:+.1f}%, {wins}/{len(pairs)}, p={p:.3f})")
                    else:
                        cells.append(f"{value:,.2f} ({wins}/{len(pairs)}, p={p:.3f})")
                else:
                    cells.append(f"{value:,.2f}")
                out.append(row)
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
        lines.append("")
    os.makedirs(os.path.join(RES, "tradeoff"), exist_ok=True)
    keys = ["scenario", "group", "metric", "label", "autoscaler", "n", "value", "change_vs_k8s_pct", "runs_better",
            "p_vs_k8s"]
    with open(os.path.join(RES, "tradeoff", "tradeoff.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(out)
    lines.append("Cells: value over runs (change vs K8s HPA, runs better than K8s HPA in the same run number, exact "
                 "two-sided Mann-Whitney U p). 5R-50% spike: user metrics of the spike phase. Control loop: K8s HPA "
                 "runs inside the cluster, its observer's period is not a control loop, so it is left out.")
    with open(os.path.join(RES, "tradeoff", "tradeoff.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
