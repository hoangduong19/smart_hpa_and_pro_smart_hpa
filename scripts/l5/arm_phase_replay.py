"""L5 evidence: offline closed-loop replay of the ORIGINAL Smart HPA control loop (2R-20%), varying only the phase of
the metrics-server scrapes (one phase per node, uniform 0-15 s).

What is the authors' code, unchanged:
  * Adaptive_Resource_Manager() is imported from smarthpa/Adaptive_Resource_Manager.py (Algorithm 2 as published).
  * The Monitor/Analyse arithmetic (current_cpu = ceil(mean(pod millicores)), DR = ceil(CR * int(cpu%) / threshold),
    scaling_action rules) and the main loop (Microservice_Capacity_Analyzer.py: maxR carried over from
    ARM_saved_decision, ARM called when any DR > maxR, Execute = kubectl scale) are copied line by line.
  * Monitor's wait `while Available_Replicas != Operational_Replicas` (ready pods vs pods listed by kubectl top) is
    kept: the whole iteration (pool.map over 11 managers) waits for the slowest manager.
What is simulated (environment, not the team's code):
  * metrics-server: --metric-resolution=15s; each node scrapes at its own phase; a pod is listed by `kubectl top`
    from the 2nd scrape after its container started; the value is its mean usage between the last two scrapes.
  * pods: ready READY_S after `kubectl scale` (lab/paper ~15 s), a removed pod stays listed until its node's next scrape.
  * load: per-service total CPU demand D_s(t) = median of the 12 lab runs v080w5 (pod_metrics.csv, sum over pods),
    split equally over ready pods, each pod capped at its CPU limit (lab = Smart HPA helm chart).
Metrics are computed from the simulated Knowledge Base rows exactly as prosmarthpa/fig8_compare.py does
(Overutilization = CPU% - threshold, demand = column D).

Usage (from Demo/results):  python ../scripts/l5/arm_phase_replay.py [--n 200] [--noise 0.0] [--placement fixed|random]
"""
import argparse
import glob
import math
import os
import random
import statistics
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "smarthpa"))
from Adaptive_Resource_Manager import Adaptive_Resource_Manager  # noqa: E402  (authors' Algorithm 2, unchanged)

SERV = ["frontend", "adservice", "cartservice", "currencyservice", "checkoutservice", "emailservice", "paymentservice",
        "shippingservice", "productcatalogservice", "recommendationservice", "redis-cart"]   # authors' pool.map order
REQ = {"adservice": 200, "cartservice": 200, "redis-cart": 70}                            # others 100m
LIM = {"adservice": 300, "cartservice": 300, "redis-cart": 125}                           # others 200m
NODES = ["k3s-master", "k3s-worker1", "k3s-worker2"]
TARGET, MAXR, MINR, DUR = 20, 2, 1, 900
SCRAPE = 15.0
READY_S = 13.0          # kubectl scale -> pod Ready (lab cluster_metrics; paper "about 15 s")
START_S = 2.0           # kubectl scale -> container running (first cAdvisor point possible)
ITER_S = 1.7            # one controller iteration (lab Knowledge Base: median 1.5-1.9 s)
POLL_S = 0.35           # one Monitor re-poll (kubectl get deployment + kubectl top)
P_MISS = 0.0            # share of scrapes after which a pod's value is NOT refreshed (lab KB: 16% of intervals ~30 s)
FRONTEND_STEADY = 580.0  # frontend demand when not CPU-limited (Smart runs with 4-11 frontend pods: 477-626 m)


def demand_curves(lab_glob):
    acc = []
    for d in sorted(glob.glob(lab_glob)):
        pm = pd.read_csv(f"{d}/pod_metrics.csv")
        acc.append(pm.groupby(["elapsed_sec", "app"]).cpu_m.sum().unstack())
    med = pd.concat(acc).groupby(level=0).median()
    med = med[med.index <= 300]
    t = med.index.values - 7.5            # a 15 s window reported at t is centred ~7.5 s earlier
    curves = {s: (t, med[s].values.astype(float)) for s in SERV}
    tf, vf = curves["frontend"]
    curves["frontend"] = (tf, vf * FRONTEND_STEADY / vf[-1])   # lab frontend was CPU-limited in K8s runs
    return curves


def demand_from_kb(run_dir):
    """per-run demand: total millicores the controller saw (CPU% x CR x request, Knowledge Base columns B, C), one
    point per change of the value (= a new 15 s metrics-server window), placed at the window centre ~7.5 s earlier.
    Where a service sat at its CPU limit the true demand is >= this value (capped)."""
    curves = {}
    for s in SERV:
        kb = pd.read_excel(f"{run_dir}/knowledge_base/{s}.xlsx").iloc[:, :3]
        kb.columns = ["t", "cpu", "cr"]
        kb = kb.dropna()
        tot = kb.cpu / 100 * REQ.get(s, 100) * kb.cr
        ch = tot.ne(tot.shift())
        t, v = kb.t[ch].values - 7.5, tot[ch].values.astype(float)
        curves[s] = (np.append(t, DUR + 60), np.append(v, v[-1]))
    return curves


class Pod:
    def __init__(self, svc, node, t_scale, initial=False):
        self.svc, self.node = svc, node
        self.start = -1e9 if initial else t_scale + START_S
        self.ready = -1e9 if initial else t_scale + READY_S
        self.end = 1e9


class Cluster:
    def __init__(self, curves, phases, placement, noise, rng, strict=False):
        self.curves, self.phase, self.noise, self.rng, self.strict = curves, phases, noise, rng, strict
        self.rr = 0
        self.uid = 0
        self.miss_seed = rng.random()
        self.pods = {s: [Pod(s, placement[s], 0, initial=True)] for s in SERV}
        for k, s in enumerate(SERV):
            self.pods[s][0].uid = -1 - k
        self.spec = {s: 1 for s in SERV}
        self.cache = {}

    def D(self, s, t):
        tt, vv = self.curves[s]
        return float(np.interp(t, tt, vv))

    def n_ready(self, s, t):
        return sum(1 for p in self.pods[s] if p.ready <= t < p.end)

    def pod_usage(self, p, a, b):
        """mean millicores of pod p over [a, b]"""
        key = (id(p), a, b)
        if key in self.cache:
            return self.cache[key]
        vals = []
        for tau in np.arange(a, b, 0.5):
            if p.ready <= tau < p.end:
                n = self.n_ready(p.svc, tau)
                vals.append(min(self.D(p.svc, tau) / n, LIM.get(p.svc, 200)))
            else:
                vals.append(1.0)
        u = statistics.mean(vals) * (1 + self.noise * self.rng.gauss(0, 1) if self.noise else 1)
        self.cache[key] = max(int(round(u)), 0)
        return self.cache[key]

    def last_scrape(self, node, t):
        ph = self.phase[node]
        return ph + SCRAPE * math.floor((t - ph) / SCRAPE)

    def missed(self, p, sk):
        if P_MISS <= 0:
            return False
        return random.Random(f"{self.miss_seed}-{p.uid}-{round(sk, 3)}").random() < P_MISS

    def top(self, s, t):
        """pods listed by `kubectl top pods -l app=s` at time t, with their millicores"""
        out = []
        for p in self.pods[s]:
            last = self.last_scrape(p.node, t)
            if p.end <= last:                                 # gone after the next scrape
                continue
            sk = last
            while sk >= p.start and self.missed(p, sk):       # value not refreshed at this scrape
                sk -= SCRAPE
            sp = sk - SCRAPE
            while sp >= p.start and self.missed(p, sp):
                sp -= SCRAPE
            if sp >= p.start:                                 # two points while alive
                out.append(self.pod_usage(p, sp, sk))
        return out

    def available(self, s, t):
        return self.n_ready(s, t)

    def scale(self, s, n, t):
        alive = [p for p in self.pods[s] if p.end > t]
        if n > len(alive):
            for _ in range(n - len(alive)):
                if self.strict:                      # deterministic round-robin placement of new pods
                    node = NODES[self.rr % len(NODES)]; self.rr += 1
                else:
                    node = self.rng.choice(NODES)
                self.pods[s].append(Pod(s, node, t)); self.uid += 1; self.pods[s][-1].uid = self.uid
        elif n < len(alive):
            for p in sorted(alive, key=lambda p: -p.start)[: len(alive) - n]:   # newest first, as ReplicaSet does
                p.end = t
        self.spec[s] = n


def monitor_analyse(cl, s, t):
    """authors' Monitor() + Analyse() for one manager; returns (data, cpu%, t_done)"""
    while True:
        avail = cl.available(s, t)
        listed = cl.top(s, t)
        if avail == len(listed) and avail > 0:
            break
        t += POLL_S
    current_cpu = math.ceil(statistics.mean(listed))
    req = REQ.get(s, 100)
    cpu_percentage = (current_cpu / req) * 100
    previous_desired = cl.spec[s]
    desired = math.ceil(int(avail) * (int(cpu_percentage) / int(TARGET)))
    if previous_desired != desired and desired > avail and desired >= MINR:
        action = "scale up"
    elif previous_desired != desired and desired < avail and desired >= MINR:
        action = "scale down"
    else:
        action = "no scale"
    return [s, action, desired, avail, req, MAXR], cpu_percentage, t + 0.5


def run_once(curves, seed, noise, placement_mode, fixed_placement, strict=False):
    rng = random.Random(seed)
    phases = {n: rng.uniform(0, SCRAPE) for n in NODES}
    placement = fixed_placement if placement_mode == "fixed" else {s: rng.choice(NODES) for s in SERV}
    cl = Cluster(curves, phases, placement, noise, rng, strict)
    kb = {s: [] for s in SERV}          # rows: t, cpu%, CR, DR, maxR  (Knowledge Base columns A-E)
    ARM_saved_decision = [[]]
    t = 0.0 if strict else rng.uniform(0, ITER_S)   # controller start offset vs Locust start (environment timing)
    while t < DUR:
        res = [monitor_analyse(cl, s, t) for s in SERV]
        microservices_data = [r[0] for r in res]
        cr_dr = {d[0]: (d[3], d[2]) for d in microservices_data}   # before the loop below overwrites d[3] (authors' aliasing)
        t_end = max(r[2] for r in res) + (ITER_S - 0.5)
        # ---- Microservice Capacity Analyzer, copied from Microservice_Capacity_Analyzer.py ----
        ARM_decision = []
        for i in range(len(microservices_data)):
            if microservices_data[i][2] > microservices_data[i][5]:
                for i2 in range(len(microservices_data)):
                    for j in range(len(ARM_saved_decision)):
                        if ARM_saved_decision[j] and microservices_data[i2][0] == ARM_saved_decision[j][0]:
                            microservices_data[i2][5] = ARM_saved_decision[j][3]
                ARM_decision = Adaptive_Resource_Manager(microservices_data)
                ARM_saved_decision = ARM_decision
                break
        if len(ARM_decision) == 0:
            ARM_saved_decision = microservices_data
            for i in range(len(microservices_data)):
                for j in range(len(ARM_saved_decision)):
                    if microservices_data[i][0] == ARM_saved_decision[j][0]:
                        ARM_saved_decision[j][3] = microservices_data[i][5]
            for (d, cpu, _) in zip(microservices_data, [r[1] for r in res], res):
                kb[d[0]].append((t, cpu, None, None, d[5]))
                if d[1] != "no scale":
                    cl.scale(d[0], d[2], t_end)
        else:
            cpu_of = {r[0][0]: r[1] for r in res}
            for dec in ARM_decision:            # [name, action, feasible replicas, ARM_maxR, request]
                kb[dec[0]].append((t, cpu_of[dec[0]], None, None, dec[3]))
                if dec[1] != "no scale":
                    cl.scale(dec[0], dec[2], t_end)
        # CR, DR as stored by the managers (column C, D) = values computed this iteration
        for name, (cr, dr) in cr_dr.items():
            row = kb[name][-1]
            kb[name][-1] = (row[0], row[1], cr, dr, row[4])
        t = t_end
    return phases, kb


def fig8_metrics(kb):
    tot = {"supply": 0, "overutil": 0, "overprov": 0, "underprov": 0}
    for s, rows in kb.items():
        req = REQ.get(s, 100)
        tot["supply"] += statistics.mean(r[2] * req for r in rows)
        tot["overutil"] += statistics.mean(r[1] - TARGET if r[1] > TARGET else 0 for r in rows)
        tot["overprov"] += statistics.mean(max(r[4] - r[3], 0) * req for r in rows)
        tot["underprov"] += statistics.mean(max(r[3] - r[4], 0) * req for r in rows)
    return tot


def split_after(kb, t0=60):
    return {s: statistics.mean(r[2] for r in kb[s] if r[0] >= t0) for s in SERV}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab", default="2R-20-v080w5/*/run*")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--noise", type=float, default=0.0)
    ap.add_argument("--placement", choices=["fixed", "random"], default="fixed")
    ap.add_argument("--strict", action="store_true",
                    help="only the 3 node scrape phases vary: controller offset 0, new pods round-robin, no noise")
    ap.add_argument("--out", default="2R-20-v080w5/l5_phase_replay.csv")
    ap.add_argument("--p-miss", type=float, default=0.0, help="share of scrapes that do not refresh a pod's value")
    ap.add_argument("--traces", help="glob of run dirs: replay each run's own demand trace (Knowledge Base) --n times")
    a = ap.parse_args()
    global P_MISS
    P_MISS = a.p_miss
    if a.traces:
        return per_trace(a)
    curves = demand_curves(a.lab)
    pm = pd.read_csv("2R-20-v080w5/smarthpa/run2/pod_metrics.csv")     # initial placement of a real run
    fixed = pm[pm.elapsed_sec == 0].groupby("app").node.first().to_dict()
    rows = []
    for k in range(a.n):
        phases, kb = run_once(curves, k, 0.0 if a.strict else a.noise, "fixed" if a.strict else a.placement, fixed,
                              a.strict)
        m, sp = fig8_metrics(kb), split_after(kb)
        rows.append({"seed": k, **{f"phase_{n}": round(v, 2) for n, v in phases.items()}, **m,
                     **{f"R_{s}": round(v, 2) for s, v in sp.items()}})
    df = pd.DataFrame(rows)
    df.to_csv(a.out, index=False)
    short = {"currencyservice": "cur", "frontend": "fro", "productcatalogservice": "pc", "recommendationservice": "rec"}
    print(f"{a.n} replays, noise {a.noise}, placement {a.placement}, strict {a.strict} -> {a.out}")
    print("currency pods after 60 s: " + df.R_currencyservice.round().value_counts().sort_index().to_string().replace(chr(10), ', '))
    print("pods after 60 s (mean over replays; share of replays with >= 2 pods):")
    for s, n in short.items():
        print(f"  {n:4} mean {df[f'R_{s}'].mean():.2f}   >=2 pods in {(df[f'R_{s}'] >= 1.5).mean():.0%}")
    print("Fig. 8 Overutilization (sum of 11 services):  min %.0f  p10 %.0f  median %.0f  p90 %.0f  max %.0f" %
          tuple(np.percentile(df.overutil, [0, 10, 50, 90, 100])))
    kp = df.R_productcatalogservice >= 1.5
    print("  prodcat kept (>=2 pods): n=%d  Overutil mean %.0f | prodcat 1 pod: n=%d  Overutil mean %.0f" %
          (kp.sum(), df.overutil[kp].mean() if kp.any() else float('nan'), (~kp).sum(), df.overutil[~kp].mean()))
    print("means: supply %.0f  overutil %.0f  overprov %.0f  underprov %.0f" %
          (df.supply.mean(), df.overutil.mean(), df.overprov.mean(), df.underprov.mean()))


def per_trace(a):
    pm = pd.read_csv("2R-20-v080w5/smarthpa/run2/pod_metrics.csv")
    rows = []
    for d in sorted(glob.glob(a.traces)):
        curves = demand_from_kb(d)
        cm = pd.read_csv(f"{d}/cluster_metrics.csv"); cm = cm[cm.elapsed_sec >= 60]
        real = cm.groupby("deployment").spec_replicas.mean()
        p0 = pd.read_csv(f"{d}/pod_metrics.csv"); fixed = p0[p0.elapsed_sec == 0].groupby("app").node.first().to_dict()
        for k in range(a.n):
            phases, kb = run_once(curves, k, 0.0, "fixed", fixed, a.strict)
            m, sp = fig8_metrics(kb), split_after(kb)
            rows.append({"trace": d, "seed": k, **m, **{f"R_{s}": round(v, 2) for s, v in sp.items()},
                         **{f"real_{s}": round(real[s], 2) for s in SERV}})
    df = pd.DataFrame(rows)
    df.to_csv(a.out, index=False)
    print(f"{a.n} phase draws per trace, strict {a.strict}, p_miss {P_MISS}, own initial pod placement -> {a.out}")
    print(f"{'trace':28}{'real cur/fro/pc/rec':>22}{'sim cur>=7':>11}{'sim pc kept':>12}{'sim Overutil':>13}")
    for d, g in df.groupby("trace", sort=False):
        r = g.iloc[0]
        real = "/".join(f"{r[f'real_{s}']:.0f}" for s in ["currencyservice", "frontend", "productcatalogservice",
                                                          "recommendationservice"])
        print(f"{d:28}{real:>22}{(g.R_currencyservice >= 6.5).mean():>11.0%}{(g.R_productcatalogservice >= 1.5).mean():>12.0%}"
              f"{g.overutil.mean():>9.0f} ({g.overutil.min():.0f}-{g.overutil.max():.0f})")
    print(f"ALL: currency >= 7 in {(df.R_currencyservice >= 6.5).mean():.0%}, prodcat kept in "
          f"{(df.R_productcatalogservice >= 1.5).mean():.0%}, Overutil mean {df.overutil.mean():.0f}")


if __name__ == "__main__":
    main()
