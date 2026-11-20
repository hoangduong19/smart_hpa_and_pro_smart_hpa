"""Compare how ARM splits quota (maxR per service over time) in: the authors' recorded Smart HPA data (.pkl training
data, 10 runs), lab Smart HPA original code (0.67 user/s and 2 user/s), lab C4 (ARM waits 120 s).
Run from Demo/results. Prints one table per question."""
import glob
import numpy as np
import pandas as pd

SERV = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend",
        "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice"]


def lab_runs(pattern):
    runs = []
    for d in sorted(glob.glob(pattern)):
        frames = []
        for s in SERV:
            kb = pd.read_excel(f"{d}/knowledge_base/{s}.xlsx")
            frames.append(pd.DataFrame({"t": kb.iloc[:, 0], "service": s, "maxR": kb.iloc[:, 4]}))
        runs.append(pd.concat(frames))
    return runs


def author_runs():
    e2 = pd.read_csv("2R-20/comparison_prosmart_figs/evidence/e2_replay.csv")
    return [g.rename(columns={"maxR_recorded": "maxR"})[["t", "service", "maxR"]] for _, g in e2.groupby("run")]


GROUPS = {
    "Authors (.pkl, AWS)": author_runs(),
    "Lab original 0.67/s": lab_runs("2R-20/smarthpa/run*"),
    "Lab original 2/s": lab_runs("2R-20-pilot2s/smarthpa/run*"),
    "Lab C4 2/s": lab_runs("2R-20-pilot2s/smarthpa-warmup/run*") + lab_runs("2R-20-c4fresh/smarthpa-warmup/run*"),
}


def per_run(r):
    r = r.copy(); r["maxR"] = r.maxR.round().astype(int)
    changed = r[r.maxR != 2]
    first = changed.t.min() if len(changed) else np.nan
    late = r[r.t > 120]
    med = late.groupby("service").maxR.median()
    # quota moves = number of times a service's maxR changes value
    moves = sum((g.sort_values("t").maxR.diff().fillna(0) != 0).sum() for _, g in r.groupby("service"))
    moves_early = sum((g[g.t <= 120].sort_values("t").maxR.diff().fillna(0) != 0).sum() for _, g in r.groupby("service"))
    return dict(first_change_s=first, moves=moves, moves_t_le_120=moves_early, max_maxR=int(late.maxR.max()),
                at_1=int((med <= 1).sum()), currency=med["currencyservice"], frontend=med["frontend"]), med


rows, meds = [], {}
for g, runs in GROUPS.items():
    res = [per_run(r) for r in runs]
    df = pd.DataFrame([x[0] for x in res])
    meds[g] = pd.concat([x[1] for x in res], axis=1).median(axis=1)
    rows.append(dict(group=g, n=len(runs),
                     first_change_s=f"{df.first_change_s.median():.0f} ({df.first_change_s.min():.0f}-{df.first_change_s.max():.0f})",
                     moves_per_run=f"{df.moves.median():.0f}", moves_first_120s=f"{df.moves_t_le_120.median():.0f}",
                     peak_maxR=f"{df.max_maxR.median():.0f} ({df.max_maxR.min()}-{df.max_maxR.max()})",
                     svc_at_maxR1=f"{df.at_1.median():.0f}",
                     currency=f"{df.currency.median():g} ({df.currency.min():g}-{df.currency.max():g})",
                     frontend=f"{df.frontend.median():g} ({df.frontend.min():g}-{df.frontend.max():g})"))
pd.set_option("display.width", 250)
print("Q1-Q3. When ARM first moves quota, how often, how concentrated (maxR after 120 s, median over services/runs)")
print(pd.DataFrame(rows).to_string(index=False))

print("\nQ4. Median maxR per service after 120 s, and distance to the authors (sum |diff| over 11 services)")
m = pd.DataFrame(meds)
m.loc["DISTANCE to authors"] = (m.sub(m["Authors (.pkl, AWS)"], axis=0)).abs().sum()
print(m.to_string())

e1 = pd.read_csv("2R-20/comparison_prosmart_figs/evidence/e1_rule_check.csv")
print("\nQ5. Authors' data: Algorithm 2 says 'move quota' -> did it? split by time")
for lo, hi in [(0, 60), (60, 120), (120, 901)]:
    w = e1[(e1.t >= lo) & (e1.t < hi) & e1.transfer_required]
    print(f"  t {lo:>3}-{hi:<3}s: required {len(w):3d}, not moved within 15 s {int(w.violation.sum()):3d}")
