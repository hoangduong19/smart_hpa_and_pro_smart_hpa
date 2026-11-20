"""E6 (20/11): does fixing the two places where the authors' ARM code departs from Algorithm 2 of the paper reproduce
the authors' recorded quota behaviour?  Offline replay of the authors' DR series (same loop as E2 in
evidence_authors.py) through (a) the published ARM code and (b) the same code with only these two lines changed:

  D1  Algorithm 2 lines 24-25: no residual left for an underprovisioned service -> UmaxR = maxR.
      Code: if CR >= maxR it sets ARM_maxR = CR (capacity follows the running pods, not maxR).
  D2  Algorithm 2 lines 35-36: elif TotalR in [1, ResidualR) -> UmaxR = floor(TotalR) + DR.
      Code (Adaptive_Resource_Manager.py, overprovisioned loop): `elif Remaining_replicas >= 1 and ARM_maxR < maxR`,
      where ARM_maxR is left over from the previous service in the loop, so a donor that should get residual back
      is cut to DR and that residual is never handed out again (quota leaks out of the system).

Checks against the authors' data: rows where all 11 maxR match, per-service match, and the total quota (sum maxR,
the authors' data has 22 on every row).  Usage (prophet venv, from prosmarthpa/): python arm_fix_replay.py
"""
import math

import pandas as pd

from evidence_authors import ORDER, OUT, REQUEST, SLA_MAXR, load_authors   # also puts ../smarthpa on sys.path
import Adaptive_Resource_Manager as published                              # noqa: E402  the authors' code


def arm_fixed(microservices_data):
    """The authors' Adaptive_Resource_Manager with D1 and D2 changed to Algorithm 2; everything else identical."""
    under, over = [], []
    for d in microservices_data:                       # d = [name, SD, DR, CR, request, maxR]
        if d[2] > d[5]:
            req_r = d[2] - d[5]
            under.append([d[0], req_r, req_r * d[4], d[4], d[3], d[5]])
        else:
            res_r = d[5] - d[2]
            over.append([d[0], res_r * d[4], d[1], d[2], d[3], d[4], d[5]])
    total = sum(o[1] for o in over)
    decision = []
    for u in sorted(under, key=lambda x: x[2], reverse=True):
        possible = total / u[3]
        if possible >= u[1]:
            feas = umax = u[1] + u[5]
            decision.append([u[0], "scale up", feas, umax, u[3]])
            total -= u[1] * u[3]
        elif 1 <= possible < u[1]:
            feas = umax = math.floor(possible) + u[5]
            decision.append([u[0], "scale up", feas, umax, u[3]])
            total -= math.floor(possible) * u[3]
        else:
            if u[4] < u[5]:
                action, feas = "scale up", u[5]
            else:
                action, feas = "no scale", u[4]
            umax = u[5]                                # D1: Algorithm 2 line 25, UmaxR = maxR (code: = CR)
            decision.append([u[0], action, feas, umax, u[3]])
    for o in sorted(over, key=lambda x: x[1]):
        desired, maxr, req = o[3], o[6], o[5]
        remaining = math.floor(total / req)
        if desired + remaining >= maxr:
            umax = maxr
        elif remaining >= 1:                           # D2: Algorithm 2 line 35, TotalR in [1, ResidualR)
            umax = desired + remaining
        else:
            umax = desired
        total -= (umax - desired) * req
        decision.append([o[0], o[2], desired, umax, req])
    return decision


def replay(df, arm):
    """same loop as evidence_authors.e2_replay, with the ARM function as a parameter"""
    res = []
    for run, g in df.groupby("run"):
        dr = g.pivot(index="t", columns="service", values="DR")
        mr = g.pivot(index="t", columns="service", values="maxR")
        saved, cr = None, {s: 1 for s in ORDER}
        for t in dr.index:
            data = [[s, "no scale", int(math.ceil(dr.at[t, s] - 1e-9)), cr[s], REQUEST[s], SLA_MAXR] for s in ORDER]
            if any(d[2] > d[5] for d in data):
                if saved:
                    for d in data:
                        d[5] = saved[d[0]]
                saved = {x[0]: x[3] for x in arm(data)}
            else:
                saved = None
            cap = saved or {s: SLA_MAXR for s in ORDER}
            for s in ORDER:
                cr[s] = max(1, min(int(math.ceil(dr.at[t, s] - 1e-9)), cap[s]))
                res.append({"run": run, "t": t, "service": s, "recorded": mr.at[t, s], "replay": cap[s]})
    return pd.DataFrame(res)


def summary(rep, name):
    rep = rep.assign(rec=rep.recorded.round().astype(int))
    eq = rep.rec == rep.replay
    rows = eq.groupby([rep.run, rep.t]).all()
    tot = rep.groupby(["run", "t"]).replay.sum()
    late = rep[rep.t > 120]
    med = late.groupby(["run", "service"]).replay.median().unstack()
    return {"ARM code": name, "rows all 11 match": f"{rows.mean():.1%}", "service-rows match": f"{eq.mean():.1%}",
            "total maxR (authors 22): median": f"{tot.median():g}", "min": int(tot.min()),
            "peak maxR": int(late.replay.max()), "currency maxR after 120 s": f"{med.currencyservice.median():g}",
            "frontend": f"{med.frontend.median():g}", "services at maxR 1": f"{(med <= 1).sum(axis=1).median():g}"}


def main():
    df = load_authors()
    pub, fix = replay(df, published.Adaptive_Resource_Manager), replay(df, arm_fixed)
    rec = df.assign(replay=df.maxR.round().astype(int), recorded=df.maxR)
    table = pd.DataFrame([summary(rec[["run", "t", "service", "recorded", "replay"]], "authors' recorded data"),
                          summary(pub, "published code"), summary(fix, "published + D1/D2 fixed")])
    pd.set_option("display.width", 250)
    print(table.to_string(index=False))
    per_service = pd.DataFrame({
        "published": pub.assign(e=pub.recorded.round() == pub.replay).groupby("service").e.mean(),
        "D1/D2 fixed": fix.assign(e=fix.recorded.round() == fix.replay).groupby("service").e.mean()})
    print("\nper-service match with the authors' recorded maxR\n" + (per_service * 100).round(0).to_string())
    table.to_csv(OUT / "e6_arm_fix_replay.csv", index=False)
    fix.to_csv(OUT / "e6_replay_fixed.csv", index=False)


if __name__ == "__main__":
    main()
