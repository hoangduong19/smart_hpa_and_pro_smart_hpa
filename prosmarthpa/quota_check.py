"""Do the auto-scalers keep the application within its total CPU quota?

The scenario quota is maxR x request summed over the 11 services (2R-20%: 2 replicas each = 2540 m). Smart HPA and
ProSmart HPA move quota between services, but the total must stay the same. For every run this script compares, in
the hold phase (t > 300 s), the replicas actually running (Knowledge Base column C) with the quota and with the
capacity the controller recorded (column E: maxR, or PmaxR when ProSmart's ARM ran).

Found 12/11: ProSmart HPA ran 30.5 pods on a 22-pod quota, because its balancing step cut PmaxR below the replicas
already running and Algorithm 4 lines 19-20 answer that with "No Scale" (fixed in prosmart_hpa.py, balance()).

Run from prosmarthpa/:  D:\\prosmart-venv\\Scripts\\python.exe quota_check.py [--scenario 2R-20] [--autoscalers ...]
Output: results/<scenario>/comparison_prosmart_figs/quota_check.csv (one row per run)
"""
import argparse
import csv
import glob
import os
import statistics as st
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "smarthpa"))
from make_run_report import CPU_REQUEST, SERVICES, load_kb  # noqa: E402

HOLD_FROM_SEC = 300
MAXR = {"2R": 2, "5R": 5, "10R": 10}


def run_dirs(scenario_dir, autoscaler):
    # run0 (trial runs) included so a smoke test can be checked; runs without hold-phase data are skipped in main
    return sorted(d for d in glob.glob(os.path.join(scenario_dir, autoscaler, "run*"))
                  if os.path.exists(os.path.join(d, "knowledge_base")))


def check(run_dir, quota_m):
    kb = {s: load_kb(run_dir, s) for s in SERVICES}
    n = min(len(v["t"]) for v in kb.values())
    idx = [i for i in range(n) if kb["frontend"]["t"][i] > HOLD_FROM_SEC]
    if not idx:
        return None
    running = [sum(kb[s]["supply"][i] for s in SERVICES) for i in idx]          # replicas x request, in m
    recorded = [sum(kb[s]["capacity"][i] for s in SERVICES) for i in idx]
    above_capacity = [any(kb[s]["supply"][i] > kb[s]["capacity"][i] for s in SERVICES) for i in idx]
    return {"running_pods_mean": round(st.mean(sum(kb[s]["supply"][i] / CPU_REQUEST.get(s, 100) for s in SERVICES)
                                               for i in idx), 1),
            "running_m_mean": round(st.mean(running)), "running_m_max": max(running),
            "recorded_capacity_m_mean": round(st.mean(recorded)), "quota_m": quota_m,
            "pct_time_above_quota": round(100 * st.mean(r > quota_m for r in running), 1),
            "pct_time_a_service_above_its_capacity": round(100 * st.mean(above_capacity), 1)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="2R-20")
    parser.add_argument("--autoscalers", nargs="+", default=["k8shpa", "smarthpa", "prosmarthpa", "prosmarthpa-authors",
                                                              "prosmarthpa-cv", "prosmarthpa-cv-w5", "prosmarthpa-cv-w10",
                                                              "prosmarthpa-cv-w15", "prosmarthpa-cv-w20",
                                                              "prosmarthpa-cv-w30"])
    args = parser.parse_args()
    scenario_dir = DEMO_DIR / "results" / args.scenario
    maxr = MAXR[args.scenario.split("-")[0]]
    quota_m = sum(maxr * CPU_REQUEST.get(s, 100) for s in SERVICES)

    rows = []
    for a in args.autoscalers:
        for d in run_dirs(str(scenario_dir), a):
            result = check(d, quota_m)
            if result:
                rows.append({"autoscaler": a, "run": os.path.basename(d), **result})
    out = scenario_dir / "comparison_prosmart_figs" / "quota_check.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"quota {quota_m} m; hold phase t > {HOLD_FROM_SEC} s")
    for r in rows:
        print(f"{r['autoscaler']:22s} {r['run']:5s} pods {r['running_pods_mean']:5.1f}  running {r['running_m_mean']:5d} m"
              f" (max {r['running_m_max']:5.0f})  above quota {r['pct_time_above_quota']:5.1f}% of time")
    print(f"Written to {out}")
