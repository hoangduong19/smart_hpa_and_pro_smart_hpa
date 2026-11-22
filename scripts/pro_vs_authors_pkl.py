"""Lab ProSmart Knowledge Base vs the authors' recorded data (history of their released PROPHET models = Fig. 8 ProSHPA,
E9): mean DR (demand models) and maxR (capacity models) per service, Overprov/Underprov from each, and demand by time.
Run from Demo/results with D:\prosmart-venv:  python ../scripts/pro_vs_authors_pkl.py [pattern]
"""
import glob, pickle, statistics, sys
import pandas as pd
from openpyxl import load_workbook

PAT = sys.argv[1] if len(sys.argv) > 1 else "2R-20-v081w5pro/prosmarthpa-authors/run*"
D = "../Pro_Smart_HPA/ProSmart_HPA/ProSmart HPA Codebase/"
DEM = D + "Microservice Managers/Trained PROPHET models - Resource Demand Prediction/{}_Demand_Model.pkl"
CAP = D + "Trained PROPHET models - Resource Capacity Prediction/{}_capacity_model.pkl"
S = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice",
     "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice"]
REQ = {"adservice": 200, "cartservice": 200, "redis-cart": 70}
BINS = [0, 30, 60, 100, 150, 200, 300, 450, 600, 750, 901]
out, prof = [], []
for s in S:
    d = pickle.load(open(DEM.format(s), "rb")).history
    c = pickle.load(open(CAP.format(s), "rb")).history
    n = min(len(d), len(c)); dy, cy, r = d.y.values[:n], c.y.values[:n], REQ.get(s, 100)
    L = []
    for f in sorted(glob.glob(f"{PAT}/knowledge_base/{s}.xlsx")):
        L += [x for x in list(load_workbook(f, read_only=True).active.iter_rows(values_only=True))[1:]
              if x[0] is not None and x[3] is not None]
    m = lambda i: statistics.mean(x[i] for x in L)
    out.append(dict(service=s, authors_DR=dy.mean(), lab_DR=m(3), authors_maxR=cy.mean(), lab_maxR=m(4),
                    authors_overprov=statistics.mean(max(a - b, 0) for a, b in zip(cy, dy)) * r,
                    lab_overprov=statistics.mean(max(x[4] - x[3], 0) for x in L) * r,
                    authors_underprov=statistics.mean(max(b - a, 0) for a, b in zip(cy, dy)) * r,
                    lab_underprov=statistics.mean(max(x[3] - x[4], 0) for x in L) * r, lab_cpu=m(1)))
    d["sec"] = (d.ds - pd.Timestamp(0)).dt.total_seconds()
    l = pd.DataFrame([(x[0], x[3]) for x in L], columns=["t", "D"])
    a = d.groupby(pd.cut(d.sec, BINS, right=False), observed=False).y.mean()
    b = l.groupby(pd.cut(l.t, BINS, right=False), observed=False).D.mean()
    for (iv, x), y in zip(a.items(), b):
        prof.append(dict(service=s, bin=str(iv), authors_DR=x, lab_DR=y))
df = pd.DataFrame(out); pd.set_option("display.width", 200)
print(df.round(2).to_string(index=False))
print("TOTAL overprov authors/lab", round(df.authors_overprov.sum(), 1), round(df.lab_overprov.sum(), 1),
      "| underprov", round(df.authors_underprov.sum(), 1), round(df.lab_underprov.sum(), 1))
print(pd.DataFrame(prof).pivot(index="service", columns="bin", values="lab_DR").round(1).to_string())
base = PAT.split("/")[0]
df.round(3).to_csv(f"{base}/pro_vs_authors_pkl.csv", index=False)
pd.DataFrame(prof).round(3).to_csv(f"{base}/pro_vs_authors_pkl_by_time.csv", index=False)
