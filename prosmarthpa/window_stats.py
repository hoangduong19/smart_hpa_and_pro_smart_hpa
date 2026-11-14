"""Per-run numbers behind Fig. 8 and Fig. 9 of the ProSmart HPA reproduction (2R-20%).

For each run, the application totals of results/<scenario>/<autoscaler>/run<N>/metrics.csv (sum over the 11 services,
the application row excluded): Supply, CPU Overutilization, Underprovision, Overprovision.
  - Fig. 9: does the prediction window change the result? Per-run values per window and a Kruskal-Wallis test across
    the 6 windows (H with tie correction, chi-square p-value with k-1 degrees of freedom; with 3-5 runs per window
    the p-value is approximate).
  - Fig. 8: ProSmart HPA (CV models and the authors' models) against Smart HPA and K8s HPA, mean and range over runs.

Run from prosmarthpa/:  D:\\prosmart-venv\\Scripts\\python.exe window_stats.py [--scenario 2R-20]
Output: results/<scenario>/comparison_prosmart_figs/window_stats_runs.csv (one row per run)
"""
import argparse
import csv
import math
import os
import statistics as st
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
METRICS = ["supply_cpu_m", "cpu_overutilization_pct", "cpu_underprovision_m", "cpu_overprovision_m"]
WINDOWS = {5: "prosmarthpa-cv-w5", 10: "prosmarthpa-cv-w10", 15: "prosmarthpa-cv-w15", 20: "prosmarthpa-cv-w20",
           25: "prosmarthpa-cv", 30: "prosmarthpa-cv-w30"}
BASELINES = ["prosmarthpa-cv", "prosmarthpa-authors", "smarthpa", "k8shpa"]


def run_totals(scenario_dir, autoscaler):
    out = {}
    for r in range(1, 21):            # run0 = trial runs, never analysed
        f = scenario_dir / autoscaler / f"run{r}" / "metrics.csv"
        if not f.exists():
            continue
        rows = [x for x in csv.DictReader(open(f)) if x["microservice"].lower() not in ("application", "app", "total")]
        out[r] = {m: sum(float(x[m]) for x in rows) for m in METRICS}
    return out


def chi2_sf(x, k):
    # survival function of the chi-square distribution, k degrees of freedom (series for integer k)
    if x <= 0:
        return 1.0
    if k % 2 == 0:
        term = total = math.exp(-x / 2)
        for i in range(1, k // 2):
            term *= (x / 2) / i
            total += term
        return total
    total = math.erfc(math.sqrt(x / 2))
    term = math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    for i in range(1, (k + 1) // 2):
        total += term
        term *= x / (2 * i + 1)
    return total


def kruskal(groups):
    values = sorted((v, g) for g, vs in enumerate(groups) for v in vs)
    n = len(values)
    ranks, i, ties = [0.0] * n, 0, 0.0
    while i < n:
        j = i
        while j + 1 < n and values[j + 1][0] == values[i][0]:
            j += 1
        for t in range(i, j + 1):
            ranks[t] = (i + j) / 2 + 1
        ties += (j - i + 1) ** 3 - (j - i + 1)
        i = j + 1
    rank_sum = [0.0] * len(groups)
    for (v, g), rk in zip(values, ranks):
        rank_sum[g] += rk
    h = 12 / (n * (n + 1)) * sum(rs ** 2 / len(gr) for rs, gr in zip(rank_sum, groups)) - 3 * (n + 1)
    h /= 1 - ties / (n ** 3 - n)
    return h, chi2_sf(h, len(groups) - 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="2R-20")
    args = parser.parse_args()
    scenario_dir = DEMO_DIR / "results" / args.scenario

    rows = []
    print("Fig. 9: application totals per run, by prediction window")
    windows = {w: run_totals(scenario_dir, a) for w, a in WINDOWS.items()}
    for m in METRICS:
        print(f"  {m}")
        for w, runs in windows.items():
            vals = [v[m] for v in runs.values()]
            print(f"    {w:2d} s  n={len(vals)}  mean {st.mean(vals):7.1f}  runs {[round(v) for v in vals]}")
        h, p = kruskal([[v[m] for v in runs.values()] for runs in windows.values()])
        print(f"    Kruskal-Wallis across windows: H = {h:.2f}, p = {p:.3f}")

    print("\nFig. 8: application totals, mean [min-max] over runs")
    base = {a: run_totals(scenario_dir, a) for a in BASELINES}
    for a, runs in base.items():
        for r, v in runs.items():
            rows.append({"autoscaler": a, "window_sec": 25 if a.startswith("prosmart") else "", "run": r,
                         **{m: round(v[m], 3) for m in METRICS}})
    for w, runs in windows.items():
        if w != 25:
            rows += [{"autoscaler": WINDOWS[w], "window_sec": w, "run": r, **{m: round(v[m], 3) for m in METRICS}}
                     for r, v in runs.items()]
    mean = {a: {m: st.mean(v[m] for v in runs.values()) for m in METRICS} for a, runs in base.items()}
    for a in ("prosmarthpa-cv", "prosmarthpa-authors"):
        print(f"  {a} (n={len(base[a])})")
        for m in METRICS:
            vals = [v[m] for v in base[a].values()]
            print(f"    {m:24s} {mean[a][m]:7.1f} [{min(vals):.0f}-{max(vals):.0f}]"
                  f"  vs Smart HPA {100 * (mean[a][m] / mean['smarthpa'][m] - 1):+6.1f}%"
                  f"  vs K8s HPA {100 * (mean[a][m] / mean['k8shpa'][m] - 1):+6.1f}%")

    out = scenario_dir / "comparison_prosmart_figs" / "window_stats_runs.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWritten to {out}")
