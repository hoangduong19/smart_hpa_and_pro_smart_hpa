"""L12/L13: why lab ProSmart demand (KB column D) differs from the authors' recorded demand (.pkl = Fig. 8 ProSHPA).
Separates three candidate causes per service:
  (a) ramp length   : lab 2 user/s (ramp 100 s, v081w5pro) vs lab 0.67 user/s (ramp 300 s = paper's 5-min ramp,
                      2R-20/prosmarthpa-authors) -> same 200 users, so steady state (t >= 300 s) must agree if only the
                      ramp differs; the ramp part of the gap = gap(full run) - gap(t >= 300 s)
  (b) user count    : paper 600 users / ~235 req/s (Fig. 4, E12), lab 200 users / measured req/s
  (c) CPU per request: steady-state millicores / req/s, lab (pod_metrics.csv, exact) vs authors (from their DR)
Authors' millicores are estimated from DR: DR = ceil(CR x int(cpu%) / 20) -> total m in ((DR-1), DR] x 20 % x request;
the same estimator is applied to the lab DR to check it against the measured millicores.
Run from Demo/results with the smarthpa or prosmart venv (needs pandas, openpyxl; pickle needs prophet -> prosmart venv):
  python ../scripts/l12_l13_cpu_per_req.py
"""
import glob, os, pickle, statistics
import pandas as pd
from openpyxl import load_workbook

S = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice",
     "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice"]
REQ = {"adservice": 200, "cartservice": 200, "redis-cart": 70}
LIMIT = {"adservice": 300, "cartservice": 300, "redis-cart": 125}
DEM = ("../Pro_Smart_HPA/ProSmart_HPA/ProSmart HPA Codebase/Microservice Managers/"
       "Trained PROPHET models - Resource Demand Prediction/{}_Demand_Model.pkl")
SETS = {"lab 2/s (v081w5pro)": "2R-20-v081w5pro/prosmarthpa-authors/run*",
        "lab 0.67/s (2R-20)": "2R-20/prosmarthpa-authors/run[1-9]"}
PAPER_RPS = 235.0    # paper Fig. 4, 600 users (E12)
T0 = 300             # steady state: after the paper's 5-min ramp


def kb(run, s):
    rows = [r for r in list(load_workbook(f"{run}/knowledge_base/{s}.xlsx", read_only=True).active.iter_rows(values_only=True))[1:]
            if r[0] is not None and r[3] is not None]
    return pd.DataFrame([(r[0], r[1], r[2], r[3], r[4]) for r in rows], columns=["t", "cpu", "cr", "D", "E"])


def lab_set(pattern):
    runs = sorted(d for d in glob.glob(pattern) if os.path.isdir(f"{d}/knowledge_base"))
    out = {s: [] for s in S}; rps, users = [], []
    for d in runs:
        h = pd.read_csv(f"{d}/locust_stats_history.csv"); h = h[h.Name == "Aggregated"]
        h["t"] = h.Timestamp - h.Timestamp.iloc[0]
        rps.append(h[h.t >= T0]["Requests/s"].mean()); users.append(h[h.t >= T0]["User Count"].mean())
        pm = pd.read_csv(f"{d}/pod_metrics.csv") if os.path.exists(f"{d}/pod_metrics.csv") else None
        for s in S:
            k = kb(d, s)
            if pm is not None:
                p = pm[pm.app == s].groupby("elapsed_sec").agg(m=("cpu_m", "sum"), pods=("pod", "count")).reset_index()
            else:  # older runs: no pod_metrics.csv -> millicores the controller saw (KB CPU% x CR x request)
                p = pd.DataFrame({"elapsed_sec": k.t, "m": k.cpu * k.cr * REQ.get(s, 100) / 100, "pods": k.cr})
            ss = p[p.elapsed_sec >= T0]
            out[s].append(dict(D_full=k.D.mean(), D_ss=k[k.t >= T0].D.mean(), E_ss=k[k.t >= T0].E.mean(),
                               cr_ss=k[k.t >= T0].cr.mean(), m_ss=ss.m.mean(), pods_ss=ss.pods.mean(),
                               perpod_max=(ss.m / ss.pods).max()))
    agg = {s: pd.DataFrame(v).mean().to_dict() for s, v in out.items()}
    return len(runs), statistics.mean(rps), statistics.mean(users), agg


def authors():
    res = {}
    for s in S:
        h = pickle.load(open(DEM.format(s), "rb")).history
        sec = (h.ds - pd.Timestamp(0)).dt.total_seconds()
        res[s] = dict(D_full=h.y.mean(), D_ss=h.y[sec >= T0].mean())
    return res


A = authors()
L = {name: lab_set(p) for name, p in SETS.items()}
rows = []
for s in S:
    r = REQ.get(s, 100); unit = 0.2 * r          # millicores per DR step
    a = A[s]
    row = {"service": s, "auth_D_full": a["D_full"], "auth_D_ss": a["D_ss"],
           "auth_m_ss_lo": (a["D_ss"] - 1) * unit, "auth_m_ss_hi": a["D_ss"] * unit}
    for name, (n, rps, users, agg) in L.items():
        g = agg[s]; tag = "l2" if "2/s" in name else "l067"
        row.update({f"{tag}_D_full": g["D_full"], f"{tag}_D_ss": g["D_ss"], f"{tag}_m_ss": g["m_ss"],
                    f"{tag}_pods_ss": g["pods_ss"], f"{tag}_perpod_max_pct_limit": 100 * g["perpod_max"] / LIMIT.get(s, 200),
                    f"{tag}_m_est_lo": (g["D_ss"] - 1) * unit, f"{tag}_m_est_hi": g["D_ss"] * unit,
                    f"{tag}_m_per_rps": g["m_ss"] / rps})
    row["auth_m_per_rps_mid"] = (row["auth_m_ss_lo"] + row["auth_m_ss_hi"]) / 2 / PAPER_RPS
    row["ratio_D_ss_l2_vs_auth"] = row["l2_D_ss"] / a["D_ss"]
    row["ratio_D_ss_l067_vs_auth"] = row["l067_D_ss"] / a["D_ss"]
    row["ramp_part_l2"] = (row["l2_D_full"] - a["D_full"]) - (row["l2_D_ss"] - a["D_ss"])
    row["cpu_per_req_ratio_l2"] = row["l2_m_per_rps"] / row["auth_m_per_rps_mid"]
    rows.append(row)
df = pd.DataFrame(rows).set_index("service")
for name, (n, rps, users, _) in L.items():
    print(f"{name}: {n} runs, steady state (t >= {T0} s) {users:.0f} users, {rps:.1f} req/s")
print(f"paper: 600 users, ~{PAPER_RPS:.0f} req/s (Fig. 4)\n")
pd.set_option("display.width", 250)
cols = ["auth_D_full", "l2_D_full", "l067_D_full", "auth_D_ss", "l2_D_ss", "l067_D_ss", "ratio_D_ss_l2_vs_auth",
        "ramp_part_l2", "l2_pods_ss", "l2_m_ss", "l2_m_est_lo", "l2_m_est_hi", "l2_perpod_max_pct_limit",
        "auth_m_ss_lo", "auth_m_ss_hi", "l2_m_per_rps", "auth_m_per_rps_mid", "cpu_per_req_ratio_l2"]
print(df[cols].round(2).T.to_string())
df.round(4).to_csv("2R-20-v081w5pro/l12_l13_cpu_per_req.csv")
