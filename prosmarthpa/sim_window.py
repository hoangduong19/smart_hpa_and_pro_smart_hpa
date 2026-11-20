"""(20/11, Fig. 9 check) Offline estimate: how much can the prediction window (5-30 s) change ProSmart's Table 1 metrics with the authors'
time-only PROPHET models, and what does ceil vs round do?  Rough model, not a substitute for runs.

True demand per service (replica units at the 20 % threshold, i.e. total CPU / 20 % of one request) = mean over the
lab K8s HPA 2 user/s runs (v080w5) of CR x CPU% / 20, which is capped by the CPU limit there (a lower bound).
Controller every 1.5 s: PDR = R(model_d(t+w)) (>= minR 1), PmaxR = R(model_c(t+w)) floored at committed replicas,
balanced to the 22-replica quota as in prosmart_hpa.balance(); executed replicas follow Algorithm 4 lines 15-20; a new
pod serves load 15 s after it is created. CPU% = demand x 20 / ready pods, capped at the limit (200 %, 150 % for
cart/ad, 178 % redis). Metrics as in fig8_compare.py (reactive DR = ceil(CR x CPU% / 20)).
"""
import glob, logging, math, os, sys
logging.disable(logging.WARNING)
import numpy as np, pandas as pd
from openpyxl import load_workbook
sys.path.insert(0, r"d:/Nam 4 - HK1/Các Chuyên đề/Demo/prosmarthpa")
from compare_author_models import AUTHOR_MODELS, SUFFIX, load_model

R = r"d:/Nam 4 - HK1/Các Chuyên đề/Demo/results/"
SV = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "paymentservice",
      "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice"]
REQ = {"adservice": 200, "cartservice": 200, "redis-cart": 70}
LIMIT = {"adservice": 150, "cartservice": 150, "redis-cart": 178}
DT, START, READY = 1.5, 10, 15
T = np.arange(0, 900, DT)

# true demand curves
dem = {}
for s in SV:
    acc = []
    for run in glob.glob(R + "2R-20-v080w5/k8shpa/run*"):
        rows = [x for x in list(load_workbook(f"{run}/knowledge_base/{s}.xlsx", read_only=True).active.iter_rows(values_only=True))[1:] if x[0] is not None]
        tt = np.array([x[0] for x in rows]); u = np.array([x[2] * x[1] / 20 for x in rows])
        acc.append(np.interp(T, tt, u))
    dem[s] = np.mean(acc, axis=0)

md = {s: load_model(AUTHOR_MODELS["demand"] / f"{s}_{SUFFIX['demand']}.pkl") for s in SV}
mc = {s: load_model(AUTHOR_MODELS["capacity"] / f"{s}_{SUFFIX['capacity']}.pkl") for s in SV}
grid = np.arange(0, 905, 5)
yd = {s: md[s].predict(pd.DataFrame({"ds": pd.to_datetime(grid, unit="s")}))["yhat"].values for s in SV}
yc = {s: mc[s].predict(pd.DataFrame({"ds": pd.to_datetime(grid, unit="s")}))["yhat"].values for s in SV}


def simulate(w, rnd):
    R_ = (lambda v: int(round(v))) if rnd == "round" else (lambda v: int(math.ceil(v)))
    pods = {s: [] for s in SV}                      # creation times of pods beyond the first
    cr = {s: 1 for s in SV}
    acc = {k: 0.0 for k in ("supply", "overutil", "overprov", "underprov")}
    for i, t in enumerate(T):
        ready = {s: 1 + sum(1 for c in pods[s] if t - c >= READY) for s in SV}
        cpu = {s: min(dem[s][i] * 20 / ready[s], LIMIT.get(s, 200)) for s in SV}
        ms = []
        for s in SV:
            pt = min(math.ceil(t / 5) * 5 + w, 900)
            pdr = max(1, R_(yd[s][pt // 5])) if t > START else cr[s]
            sd = "up" if pdr > cr[s] else ("down" if pdr < cr[s] else "no")
            ms.append(dict(s=s, pdr=pdr, cr=cr[s], sd=sd, maxr=2, req=REQ.get(s, 100), pt=pt))
        if any(m["pdr"] > m["maxr"] for m in ms):
            for m in ms:
                committed = max(m["pdr"], 1) if m["sd"] == "down" else m["cr"]
                m["pm"] = max(committed, R_(yc[m["s"]][m["pt"] // 5]))
            # balance to 22 replicas x request (same idea as prosmart_hpa.balance)
            def ar():
                a = sum((m["pm"] - 2) * m["req"] for m in ms if m["pm"] > 2); r = sum((2 - m["pm"]) * m["req"] for m in ms if m["pm"] < 2)
                return a, r
            a, r = ar()
            for m in sorted(ms, key=lambda m: (m["pm"] - m["pdr"]) * m["req"], reverse=True):
                if a <= r: break
                com = max(m["pdr"], 1) if m["sd"] == "down" else m["cr"]
                spare = m["pm"] - max(m["pdr"], com)
                if spare > 0:
                    m["pm"] -= min(spare, math.ceil((a - r) / m["req"])); a, r = ar()
            for m in sorted(ms, key=lambda m: (m["pdr"] - 2) * m["req"]):
                if a <= r: break
                com = max(m["pdr"], 1) if m["sd"] == "down" else m["cr"]
                if m["pm"] > com:
                    m["pm"] -= min(m["pm"] - com, math.ceil((a - r) / m["req"])); a, r = ar()
            for m in ms:
                m["res"] = m["pdr"] if m["pm"] >= m["pdr"] else (m["pm"] if m["cr"] < m["pm"] else m["cr"])
        else:
            for m in ms:
                m["pm"], m["res"] = 2, m["pdr"]
        for m in ms:
            s = m["s"]
            if m["res"] > cr[s]:
                pods[s] += [t] * (m["res"] - cr[s])
            elif m["res"] < cr[s]:
                pods[s] = sorted(pods[s])[: m["res"] - 1]
            cr[s] = m["res"]
            req = m["req"]; dr = math.ceil(ready[s] * cpu[s] / 20)
            acc["supply"] += cr[s] * req
            acc["overutil"] += max(cpu[s] - 20, 0)
            acc["overprov"] += max(m["pm"] - dr, 0) * req
            acc["underprov"] += max(dr - m["pm"], 0) * req
    return {k: v / len(T) for k, v in acc.items()}


for rnd in ("ceil", "round"):
    print(f"--- rounding: {rnd}")
    for w in (5, 10, 15, 20, 25, 30):
        r = simulate(w, rnd)
        print(f"  window {w:2d}s: " + "  ".join(f"{k} {v:7.1f}" for k, v in r.items()))
print("paper Fig 9 overutil 348/331/320/306/285/318, underprov 4309/4109/4082/3811/3725/4273, overprov 70/64/62/61/59/65")
