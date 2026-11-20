"""Fig. 8 comparison (2R-20%) computed the way the authors computed Fig. 8: their ProSmart package script
`Results Analysis/Results_Analysis.py`, applied to every autoscaler.

Differences from smarthpa/make_run_report.py (which follows the Smart HPA package script, used for Fig. 6):
  * CPU Overutilization sample = CPU% - threshold when CPU% > threshold, else 0 (ProSmart script line 98; E7).
  * Demand = Knowledge Base column D (reactive DR = ceil(CR x CPU% / threshold)) for every autoscaler, ProSmart included.
    Checked 20/11 (E8 resolved): the authors' demand data behind Fig. 8 ProSHPA (the .pkl training data, equal to Fig. 8
    ProSHPA per service, E9) follows the user ramp with no look-ahead (frontend mean of 10 runs 1.5 / 4.1 / 13.0 at
    t = 10 / 30 / 100 s, 20 / 60 / 200 users), while a 25 s prediction from their own model is already 6 / 8 / 15.
    So it is measured demand, not the predicted DR. --prosmart-demand G (column G, predicted DR before the ARM) is
    kept only as a sensitivity check.
Supply = mean(CR x request), Overprovision = mean(max(maxR - DR, 0) x request), Underprovision = mean(max(DR - maxR, 0)
x request), per microservice, summed over the 11 microservices, then averaged over runs (as the authors do).

Usage (from Demo/results):
  python ../prosmarthpa/fig8_compare.py --k8s "2R-20-v080w5/k8shpa/run*" --smart "2R-20-v080w5/smarthpa/run*" \
      [--prosmart "2R-20-v080w5/prosmarthpa-authors/run*"] [--out 2R-20-v080w5/comparison/fig8_compare.csv]
"""
import argparse
import glob
import os
import statistics

from openpyxl import load_workbook

REQUEST = {"adservice": 200, "cartservice": 200, "redis-cart": 70}        # all other services: 100m
THRESHOLD = 20
METRICS = ["supply", "overutil", "overprov", "underprov"]
LABEL = {"supply": "Supply CPU (m)", "overutil": "CPU Overutilization", "overprov": "CPU Overprovision (m)",
         "underprov": "CPU Underprovision (m)"}
# paper Fig. 8 application totals (paper_fig8_values.csv, read from the PDF's vector bars)
PAPER = {"ProSHPA": {"supply": 2479.68, "overutil": 284.62, "overprov": 59.31, "underprov": 3728.85},
         "SHPA": {"supply": 2427.08, "overutil": 381.56, "overprov": 82.67, "underprov": 4994.87},
         "KHPA": {"supply": 2053.49, "overutil": 383.26, "overprov": 437.36, "underprov": 5089.84}}


def run_metrics(run_dir, demand_col):
    """per-microservice metrics of one run; demand_col is the 0-based Knowledge Base column holding DR"""
    out = {}
    for f in sorted(glob.glob(os.path.join(run_dir, "knowledge_base", "*.xlsx"))):
        service = os.path.basename(f)[:-5]
        req = REQUEST.get(service, 100)
        rows = [r for r in list(load_workbook(f, read_only=True).active.iter_rows(values_only=True))[1:]
                if r[0] is not None and r[4] is not None and r[demand_col] is not None]
        out[service] = {
            "supply": statistics.mean(r[2] * req for r in rows),
            "overutil": statistics.mean(r[1] - THRESHOLD if r[1] > THRESHOLD else 0 for r in rows),
            "overprov": statistics.mean(max(r[4] - r[demand_col], 0) * req for r in rows),
            "underprov": statistics.mean(max(r[demand_col] - r[4], 0) * req for r in rows),
        }
    return out


def app_totals(pattern, demand_col):
    runs = sorted(d for d in glob.glob(pattern) if os.path.isdir(os.path.join(d, "knowledge_base")))
    totals = [{m: sum(s[m] for s in run_metrics(r, demand_col).values()) for m in METRICS} for r in runs]
    return runs, totals


def pct(a, b):
    return 100 * (a / b - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k8s", required=True)
    ap.add_argument("--smart", required=True)
    ap.add_argument("--prosmart")
    ap.add_argument("--prosmart-demand", choices=["D", "G"], default="D")
    ap.add_argument("--out")
    a = ap.parse_args()
    sets = {"KHPA": (a.k8s, 3), "SHPA": (a.smart, 3)}
    if a.prosmart:
        sets["ProSHPA"] = (a.prosmart, 3 if a.prosmart_demand == "D" else 6)
    data = {k: app_totals(p, col) for k, (p, col) in sets.items()}
    mean = {k: {m: statistics.mean(t[m] for t in tot) for m in METRICS} for k, (_, tot) in data.items()}

    for k, (runs, tot) in data.items():
        print(f"{k}: {len(runs)} runs")
        for r, t in zip(runs, tot):
            print(f"   {r}: " + "  ".join(f"{m} {t[m]:.0f}" for m in METRICS))
    pairs = [("SHPA", "KHPA")] + ([("ProSHPA", "SHPA"), ("ProSHPA", "KHPA")] if a.prosmart else [])
    rows = []
    print(f"\n{'metric':24s} {'pair':16s} {'paper %':>8s} {'lab %':>8s}  same direction")
    for m in METRICS:
        for x, y in pairs:
            p, l = pct(PAPER[x][m], PAPER[y][m]), pct(mean[x][m], mean[y][m])
            same = (p > 0) == (l > 0)
            rows.append({"metric": m, "pair": f"{x} vs {y}", "paper_pct": round(p, 2), "lab_pct": round(l, 2),
                         "lab_" + x: round(mean[x][m], 1), "lab_" + y: round(mean[y][m], 1), "same_direction": same})
            print(f"{LABEL[m]:24s} {x + ' vs ' + y:16s} {p:+8.1f} {l:+8.1f}  {'yes' if same else 'NO'}")
    if a.out:
        import csv
        os.makedirs(os.path.dirname(a.out), exist_ok=True)
        keys = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("metric", "pair", "paper_pct", "lab_pct"), k))
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(f"\nwritten {a.out}")


if __name__ == "__main__":
    main()
