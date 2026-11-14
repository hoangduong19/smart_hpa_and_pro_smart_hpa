"""Randomized check that ProSmart HPA's Application Resource Manager keeps the application within its quota.

Replays the controller's Plan/Execute logic of prosmart_hpa.py (Algorithm 3 scaling decision, ARM activation,
application_resource_manager with balance(), "No Scale" keeps CR) on random states: random PDR per service and a random
PROPHET capacity prediction (-1..12 replicas) instead of the models. After every iteration the replicas running must
(1) fit in the scenario quota (maxR x request summed) and (2) not exceed the service's PmaxR.

Written 12/11 after ProSmart ran 30.5 pods on a 22-pod quota (see quota_check.py).
Run from prosmarthpa/:  D:\\prosmart-venv\\Scripts\\python.exe test_quota_invariant.py      (exit 1 on a violation)
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "smarthpa"))
import prosmart_hpa as p  # noqa: E402

REQ = {"adservice": 200, "cartservice": 200, "redis-cart": 70}
NAMES = list(p.MANAGERS.values())


def decision(pdr, cr, minr):
    # same as microservice_manager(): PDR is floored at minR, then Algorithm 3 lines 2-8
    pdr = max(minr, pdr)
    sd = "scale up" if pdr > cr else ("scale down" if pdr < cr and pdr >= minr else "no scale")
    return pdr, sd


def main(episodes=400, steps=50, seed=1):
    random.seed(seed)
    p.predict = lambda model, t, **kw: random.randint(-1, 12)
    bad = total = 0
    for _ in range(episodes):
        maxr = random.choice([2, 5, 10])
        quota = sum(maxr * REQ.get(n, 100) for n in NAMES)
        cr = {n: 1 for n in NAMES}
        for _ in range(steps):
            ms = []
            for n in NAMES:
                raw = random.choice([-1, 0, 1, 2, 3, 5, 8, 12, 20, 30]) if random.random() < .7 else cr[n] + random.randint(-3, 3)
                pdr, sd = decision(raw, cr[n], 1)
                ms.append(dict(name=n, cr=cr[n], spec=cr[n], pdr=pdr, sd=sd, maxr=maxr, minr=1, req=REQ.get(n, 100), p_time=0))
            if any(m["pdr"] > m["maxr"] for m in ms):            # main loop: ARM activation
                p.application_resource_manager(ms, {n: None for n in NAMES})
            else:
                for m in ms:
                    m["pmaxr"], m["res_sd"], m["res_dr"] = m["maxr"], m["sd"], m["pdr"]
            for m in ms:
                if m["res_sd"] == "no scale":
                    m["res_dr"] = m["cr"]
                cr[m["name"]] = m["res_dr"]
            total += 1
            used = sum(cr[n] * REQ.get(n, 100) for n in NAMES)
            if used > quota or any(m["res_dr"] > m["pmaxr"] for m in ms):
                bad += 1
                if bad <= 3:
                    print("VIOLATION", maxr, used, quota,
                          [(m["name"][:8], m["cr"], m["res_dr"], m["pmaxr"], m["pdr"], m["sd"]) for m in ms])
    print(f"{total} controller iterations, {bad} above the quota or above PmaxR")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
