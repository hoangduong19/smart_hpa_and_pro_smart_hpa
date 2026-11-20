"""Pass/fail check of a pilot (K8s HPA vs Smart HPA, 2R-20%) against the paper's trend, with criteria fixed BEFORE
looking at the pilot data (19/11, plan: spawn 2 user/s like the paper instead of 0.67 user/s).

Paper, Fig. 8 (2R-20%, application level): Smart HPA is better than K8s HPA on all four CPU metrics:
    Supply CPU 2427.1 vs 2053.5 m (higher), CPU Overutilization 381.6 vs 383.3 % (lower),
    CPU Underprovision 4994.9 vs 5089.8 m (lower), CPU Overprovision 82.7 vs 437.4 m (lower).
Section 5.2 adds the time metrics: Overutilization Time and Underprovision Time also lower (1.004x, 1.01x).
A pilot run PASSES only if Smart HPA has the paper's direction on all seven Table 1 metrics, AND the mechanism found on 19/11 is gone:
currencyservice no longer holds maxR >= 9 after t = 60 s, and fewer than 5 services are stuck at maxR 1.

Usage: python pilot_check.py ../results/2R-20-pilot2s
"""

import sys
from pathlib import Path

import pandas as pd

PAPER = {  # metric: (K8s HPA, Smart HPA, better); None = paper gives only the direction, not the value
    "supply_cpu_m": (2053.5, 2427.1, "higher"),
    "cpu_overutilization_pct": (383.3, 381.6, "lower"),
    "cpu_underprovision_m": (5089.8, 4994.9, "lower"),
    "cpu_overprovision_m": (437.4, 82.7, "lower"),
    # Table 1 time metrics, Section 5.2 text for 2R-20%: "1.004x reduction in CPU Overutilization and Time, and a
    # 1.01x reduction in CPU Underprovision and Time"; Overprovision Time = time with no service underprovisioned,
    # so it moves opposite to Underprovision Time (higher is better). A tie counts as FAIL.
    "overutilization_time_min": (None, None, "lower"),
    "underprovision_time_min": (None, None, "lower"),
    "overprovision_time_min": (None, None, "higher"),
}
SERVICES = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend",
            "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice"]


def quota_split(run_dir):
    """median maxR per service after t = 60 s, from the Smart HPA Knowledge Base"""
    out = {}
    for s in SERVICES:
        kb = pd.read_excel(run_dir / "knowledge_base" / f"{s}.xlsx")
        t, maxr = kb.iloc[:, 0], kb.iloc[:, 4]
        out[s] = float(maxr[t > 60].median())
    return out


def app_metrics(scen_dir, autoscaler):
    """APPLICATION row of every run<N>/metrics.csv of one autoscaler (works for variants make_comparison.py skips)"""
    rows = []
    for f in sorted((scen_dir / autoscaler).glob("run*/metrics.csv")):
        m = pd.read_csv(f)
        rows.append(m[m.microservice == "APPLICATION"].iloc[0])
    return pd.DataFrame(rows).set_index("run") if rows else pd.DataFrame()


def main(scen_dir, smart_name="smarthpa"):
    scen_dir = Path(scen_dir)
    k8s = app_metrics(scen_dir, "k8shpa")
    smart = app_metrics(scen_dir, smart_name)
    common = sorted(set(k8s.index) & set(smart.index))
    if not common:
        raise SystemExit(f"no run number with both k8shpa and {smart_name}")
    all_pass = True
    for r in common:
        print(f"\n=== run {r}: {smart_name} vs K8s HPA (paper direction must hold on all 7 Table 1 metrics)")
        print(f"{'metric':26s} {'K8s':>9s} {'Smart':>9s} {'Smart/K8s':>9s} {'paper':>7s}  result")
        for m, (pk, ps, better) in PAPER.items():
            k, s = k8s.at[r, m], smart.at[r, m]
            ok = s > k if better == "higher" else s < k
            all_pass &= ok
            paper_ratio = f"{ps / pk:7.3f}" if pk else f"{better:>7s}"
            ratio = f"{s / k:9.3f}" if k else f"{'-':>9s}"
            result = "PASS" if ok else ("FAIL (tie)" if s == k else "FAIL")
            print(f"{m:26s} {k:9.2f} {s:9.2f} {ratio} {paper_ratio}  {result}")
        split = quota_split(scen_dir / smart_name / f"run{r}")
        curr, at_one = split["currencyservice"], [s for s, v in split.items() if v <= 1]
        mech_ok = curr < 9 and len(at_one) < 5
        all_pass &= mech_ok
        print(f"quota after 60 s: currency maxR {curr:g}, at maxR 1: {len(at_one)} ({', '.join(at_one) or '-'})"
              f"  {'PASS' if mech_ok else 'FAIL'}")
        print("maxR by service: " + ", ".join(f"{s[:6]} {v:g}" for s, v in split.items()))
    print(f"\nPILOT {'PASS' if all_pass else 'FAIL'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--smart=")]
    smart = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--smart=")), "smarthpa")
    sys.exit(main(args[0] if args else "../results/2R-20-pilot2s", smart))
