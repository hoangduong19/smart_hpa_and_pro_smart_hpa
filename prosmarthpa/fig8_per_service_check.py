"""E5 (20/11): paper Fig. 8 (2R-20%) per service vs lab runs, for Supply CPU, CPU Overutilization, CPU Underprovision.
Question: which column of the paper does the lab fail to reproduce, Smart HPA or K8s HPA?
Also bounds the paper's K8s frontend Underprovision: Underprovision = mean(max(DR - maxR, 0) x request) and
DR <= maxR x (CPU limit / request) / threshold = 2 x 200 / 20 = 20 replicas, so <= (20 - 2) x 100 m = 1800 m.
Run from Demo/results. Writes 2R-20/comparison_prosmart_figs/evidence/e5_fig8_per_service.csv"""
import glob

import pandas as pd

EVID = "2R-20/comparison_prosmart_figs/evidence"
paper = pd.read_csv("2R-20/comparison_prosmart_figs/paper_fig8_values.csv")
LAB = {
    "lab_K8s_2s": "2R-20-c4fresh/k8shpa/run*/metrics.csv",                 # 7 runs, fresh pods
    "lab_Smart_original_2s": "2R-20-pilot2s/smarthpa/run*/metrics.csv",   # authors' code, spawn 2/s like the paper
    "lab_C4_2s": "2R-20-c4fresh/smarthpa-warmup/run*/metrics.csv",
    "lab_Smart_original_0.67s": "2R-20/smarthpa/run*/metrics.csv",
}
out = []
for m in ["supply_cpu_m", "cpu_overutilization_pct", "cpu_underprovision_m"]:
    t = paper[paper.metric == m].pivot(index="service", columns="column", values="value")[["KHPA", "SHPA"]]
    t.columns = ["paper_K8s", "paper_Smart"]
    for name, pat in LAB.items():
        files = glob.glob(pat)
        t[f"{name} (n={len(files)})"] = pd.concat(pd.read_csv(f) for f in files).groupby("microservice")[m].mean()
    print(f"\n{m}\n{t.round(0).to_string()}")
    out.append(t.assign(metric=m))
pd.concat(out).to_csv(f"{EVID}/e5_fig8_per_service.csv")

u = paper[paper.metric == "cpu_underprovision_m"].pivot(index="service", columns="column", values="value")
bound = 1800.0
k_app, s_app, k_fe = u.at["APPLICATION", "KHPA"], u.at["APPLICATION", "SHPA"], u.at["frontend", "KHPA"]
k_capped = k_app - k_fe + bound
print(f"\nPaper K8s frontend Underprovision {k_fe:.0f} m > physical max {bound:.0f} m")
print(f"Paper K8s application Underprovision with frontend at the max: <= {k_capped:.0f} m "
      f"-> paper Smart/K8s >= {s_app / k_capped:.3f} (published {s_app / k_app:.3f})")
