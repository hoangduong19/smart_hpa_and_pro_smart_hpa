"""ProSmart Overprovision/Underprovision when column E is the RAW capacity prediction (what the authors' released
manager writes: Application_Resource_Manager.py Analyse -> Plan, no floor at the running replicas) instead of the lab
value max(committed, PmaxR) (prosmart_hpa.py committed(), 12/11 fix).

For every Knowledge Base row with ARM active (column J = 1) the authors' capacity model is re-run with the same inputs
the controller used (time = column I, desired = PDR column G, current_replicas = column C, round as PROSMART_ROUNDING);
rows with ARM off keep the SLA maxR, as in the authors' manager. Demand = column D (as fig8_compare.py).
Run from Demo/results with D:\\prosmart-venv:  python ../scripts/pro_rawcap.py [pattern] [--csv out.csv]
"""
import argparse, glob, math, os, statistics, sys
import pandas as pd
from openpyxl import load_workbook

sys.path.insert(0, "../prosmarthpa")
os.environ.setdefault("PROSMART_AUTHOR_MODELS", "1")
REQUEST = {"adservice": 200, "cartservice": 200, "redis-cart": 70}
SERV = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend",
        "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice"]
MODEL_DIR = "../Pro_Smart_HPA/ProSmart_HPA/ProSmart HPA Codebase/Trained PROPHET models - Resource Capacity Prediction"

ap = argparse.ArgumentParser()
ap.add_argument("pattern", nargs="?", default="2R-20-v081w5pro/prosmarthpa-authors/run*")
ap.add_argument("--csv")
a = ap.parse_args()

import pickle
models = {}
for s in SERV:
    f = os.path.join(MODEL_DIR, f"{s}_capacity_model.pkl")
    if not os.path.exists(f):
        f = f"../prosmarthpa/models/{s}_capacity_model.pkl"
    m = pickle.load(open(f, "rb"))
    for attr, value in {"scaling": "absmax", "y_min": 0.0, "holidays_mode": m.seasonality_mode}.items():
        if not hasattr(m, attr):
            setattr(m, attr, value)
    models[s] = m

out = []
for d in sorted(glob.glob(a.pattern)):
    for s in SERV:
        rows = [r for r in list(load_workbook(f"{d}/knowledge_base/{s}.xlsx", read_only=True).active.iter_rows(values_only=True))[1:]
                if r[0] is not None and r[3] is not None and r[4] is not None]
        req = REQUEST.get(s, 100)
        arm = [i for i, r in enumerate(rows) if r[9] == 1]
        raw = [r[4] for r in rows]  # placeholder; ARM-off rows: column E = SLA maxR already
        if arm:
            fut = pd.DataFrame({"ds": pd.to_datetime([rows[i][8] for i in arm], unit="s"),
                                "desired": [rows[i][6] for i in arm], "current_replicas": [rows[i][2] for i in arm]})
            yhat = models[s].predict(fut)["yhat"].tolist()
            for i, y in zip(arm, yhat):
                raw[i] = max(0, int(round(y)))
        D = [r[3] for r in rows]
        E = [r[4] for r in rows]
        mean = statistics.mean
        out.append({"run": os.path.basename(d), "service": s,
                    "E_lab": mean(E), "E_raw": mean(raw), "CR": mean(r[2] for r in rows), "D": mean(D),
                    "overprov_lab": mean(max(e - x, 0) for e, x in zip(E, D)) * req,
                    "overprov_raw": mean(max(e - x, 0) for e, x in zip(raw, D)) * req,
                    "underprov_lab": mean(max(x - e, 0) for e, x in zip(E, D)) * req,
                    "underprov_raw": mean(max(x - e, 0) for e, x in zip(raw, D)) * req,
                    "raw_below_CR_pct": 100 * mean(1 if e < r[2] else 0 for e, r in zip(raw, rows))})
df = pd.DataFrame(out)
svc = df.groupby("service").mean(numeric_only=True)
pd.set_option("display.width", 200)
print(svc.round(2).to_string())
tot = df.groupby("run")[["overprov_lab", "overprov_raw", "underprov_lab", "underprov_raw"]].sum()
print("\nper run totals\n", tot.round(1).to_string())
print("\nmean totals\n", tot.mean().round(1).to_string())
if a.csv:
    df.to_csv(a.csv, index=False)
