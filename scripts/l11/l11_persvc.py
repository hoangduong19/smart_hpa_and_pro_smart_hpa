import csv,glob,os,statistics,sys
# run from Demo/results: python ../scripts/l11/l11_persvc.py "2R-20-v080w5/k8shpa/run*" KHPA
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "prosmarthpa"))
from fig8_compare import run_metrics
paper={}
for r in csv.DictReader(open("2R-20/comparison_prosmart_figs/paper_fig8_values.csv")):
    paper[(r["metric"],r["column"],r["service"])]=float(r["value"])
col=sys.argv[2]; runs=sorted(d for d in glob.glob(sys.argv[1]) if os.path.exists(d+"/run_info.json"))
per=[run_metrics(r,3) for r in runs]
print(col,[os.path.basename(r) for r in runs])
print(f"{'service':22s} {'paperSup':>8s} {'labSup':>7s}  runs                    | {'pDR>1%':>6s} pOverprov labOverprov")
for s in sorted(per[0]):
    vals=[p[s]["supply"] for p in per]
    ps=paper.get(("supply_cpu_m",col,s),0)
    print(f"{s:22s} {ps:8.0f} {statistics.mean(vals):7.0f}  {' '.join(f'{v:5.0f}' for v in vals):24s}| ov {paper.get(('cpu_overprovision_m',col,s),0):6.1f} {statistics.mean(p[s]['overprov'] for p in per):6.1f}  ou {paper.get(('cpu_overutilization_pct',col,s),0):6.2f} {statistics.mean(p[s]['overutil'] for p in per):6.2f}")
