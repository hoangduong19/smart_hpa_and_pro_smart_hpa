"""Per-service Overutilization / Underprovision (Fig. 8 formulas) for lab 2R-20-v080w5 vs paper Fig. 8.
Shows which column (KHPA or SHPA) and which services carry the Smart/K8s gap. Run from Demo/results:
  python ../scripts/l5_l4_persvc.py
"""
import csv, glob, statistics, sys
sys.path.insert(0, "../prosmarthpa")
from fig8_compare import run_metrics

COL_D = 3  # Knowledge Base column D (0-based) = reactive DR, as fig8_compare default
paper = {}  # a bar missing from the paper figure = 0
for r in csv.DictReader(open("2R-20/comparison_prosmart_figs/paper_fig8_values.csv", encoding="utf-8")):
    paper[(r["metric"], r["column"], r["service"])] = float(r["value"])
PM = {"overutil": "cpu_overutilization_pct", "underprov": "cpu_underprovision_m"}

def lab(pattern):
    runs = [run_metrics(d, COL_D) for d in sorted(glob.glob(pattern))]
    svcs = runs[0].keys()
    return {s: {m: statistics.mean(r[s][m] for r in runs) for m in PM} for s in svcs}, runs

K, Kr = lab("2R-20-v080w5/k8shpa/run*")
S, Sr = lab("2R-20-v080w5/smarthpa/run*")
for m in PM:
    pm = PM[m]
    print(f"\n== {m}   (lab = mean {len(Kr)} K8s / {len(Sr)} Smart runs)")
    print(f"{'service':24}{'K8s lab':>9}{'K8s bai':>9}{'Smart lab':>10}{'Smart bai':>10}")
    tot = [0, 0, 0, 0]
    for s in sorted(K):
        v = [K[s][m], paper.get((pm, "KHPA", s), 0.0), S[s][m], paper.get((pm, "SHPA", s), 0.0)]
        tot = [a + b for a, b in zip(tot, v)]
        print(f"{s:24}" + "".join(f"{x:>9.1f} " for x in v))
    print(f"{'TOTAL':24}" + "".join(f"{x:>9.1f} " for x in tot))
    nf = [t - x for t, x in zip(tot, [K['frontend'][m], paper[(pm,'KHPA','frontend')], S['frontend'][m], paper[(pm,'SHPA','frontend')]])]
    print(f"{'TOTAL w/o frontend':24}" + "".join(f"{x:>9.1f} " for x in nf))
    print(f"Smart/K8s: lab {tot[2]/tot[0]-1:+.1%}  bai {tot[3]/tot[1]-1:+.1%} | w/o frontend: lab {nf[2]/nf[0]-1:+.1%}  bai {nf[3]/nf[1]-1:+.1%}")
