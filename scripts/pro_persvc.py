"""Per-service Fig. 8 metrics (fig8_compare formulas, demand = KB column D) for lab KHPA / SHPA / ProSHPA vs paper.
Shows which column and which services carry each ProSmart gap. Run from Demo/results:
  python ../scripts/pro_persvc.py [--pro "2R-20-v081w5pro/prosmarthpa-authors/run*"] [--csv out.csv]
"""
import argparse, csv, glob, statistics, sys
sys.path.insert(0, "../prosmarthpa")
from fig8_compare import run_metrics

ap = argparse.ArgumentParser()
ap.add_argument("--k8s", default="2R-20-v080w5/k8shpa/run*")
ap.add_argument("--smart", default="2R-20-v080w5/smarthpa/run*")
ap.add_argument("--pro", default="2R-20-v081w5pro/prosmarthpa-authors/run*")
ap.add_argument("--csv")
a = ap.parse_args()

paper = {}  # a bar missing from the paper figure = 0
for r in csv.DictReader(open("2R-20/comparison_prosmart_figs/paper_fig8_values.csv", encoding="utf-8")):
    paper[(r["metric"], r["column"], r["service"])] = float(r["value"])
PM = {"supply": "supply_cpu_m", "overutil": "cpu_overutilization_pct",
      "overprov": "cpu_overprovision_m", "underprov": "cpu_underprovision_m"}
COLS = {"KHPA": a.k8s, "SHPA": a.smart, "ProSHPA": a.pro}

lab, nruns = {}, {}
for c, pat in COLS.items():
    runs = [run_metrics(d, 3) for d in sorted(glob.glob(pat))]
    nruns[c] = len(runs)
    lab[c] = {s: {m: statistics.mean(r[s][m] for r in runs) for m in PM} for s in runs[0]}
svcs = sorted(lab["KHPA"])
rows = []
for m, pm in PM.items():
    print(f"\n== {m}   runs: " + ", ".join(f"{c} {n}" for c, n in nruns.items()))
    print(f"{'service':24}" + "".join(f"{c+' lab':>12}{c+' bai':>12}" for c in COLS))
    tot = {c: [0.0, 0.0] for c in COLS}
    for s in svcs:
        line = f"{s:24}"
        for c in COLS:
            l, p = lab[c][s][m], paper.get((pm, c, s), 0.0)
            tot[c][0] += l; tot[c][1] += p
            line += f"{l:>12.1f}{p:>12.1f}"
            rows.append({"metric": m, "column": c, "service": s, "lab": round(l, 2), "paper": p})
        print(line)
    print(f"{'TOTAL':24}" + "".join(f"{tot[c][0]:>12.1f}{tot[c][1]:>12.1f}" for c in COLS))
    for x, y in [("ProSHPA", "SHPA"), ("ProSHPA", "KHPA")]:
        print(f"  {x}/{y}: lab {tot[x][0]/tot[y][0]-1:+.1%}  bai {tot[x][1]/tot[y][1]-1:+.1%}")
if a.csv:
    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
