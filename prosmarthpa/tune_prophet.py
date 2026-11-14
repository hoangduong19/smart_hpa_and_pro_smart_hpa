"""Tune and train the 22 PROPHET models of ProSmart HPA with cross-validation, as the paper says (Section 5.1:
"We tune the hyperparameters of these models using a cross-validation approach"; the paper does not say which one).

Cross-validation = leave-one-run-out over our Smart HPA 2R-20% runs. A run is one 15-min time series; rows of the same
run are strongly correlated, so a run is never split between training and testing. The score is what the managers use
the model for: at every 5 s grid time t >= 10 s predict y(t + 25 s) from what is known at t, round up (math.ceil),
mean absolute error in replicas (train_prophet.predict_ahead).

Grid (Prophet's documented tuning range): changepoint_prior_scale x regressor prior_scale. Seasonality parameters are
not tuned: a 15-min series has no daily/weekly seasonality and Prophet disables it.

Two outputs:
  1. Nested cross-validation (evaluation only, nothing saved): for each held-out run r, pick the grid point by
     leave-one-run-out over the other runs, fit on them with that point, test on r. The held-out run never influences
     the choice, so the error is not optimistic. Compared on the same folds with Prophet defaults (how models_3runs was
     trained) and with "same as now" (reactive baseline).
  2. Final models: grid point chosen by leave-one-run-out over all runs, fit on all runs, saved to --out with
     tuning.csv (score of every grid point) and best_params.csv.

Usage (prophet venv):
  python tune_prophet.py --runs 1 2 3 4 5 --out models_5runs_cv
"""

import argparse
import itertools
import logging
import os
import pickle
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from train_prophet import MICROSERVICES, MODELS, fit, load_run, predict_ahead

GRID = {"changepoint_prior_scale": [0.001, 0.01, 0.05, 0.1, 0.5],
        "regressor_prior_scale": [0.01, 0.1, 1.0, 10.0]}
POINTS = [dict(zip(GRID, v)) for v in itertools.product(*GRID.values())]
DEFAULT = {"changepoint_prior_scale": 0.05, "regressor_prior_scale": 10.0}     # Prophet defaults
SUFFIX = {"demand": "Demand_Model", "capacity": "capacity_model"}


def quiet():
    logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
    logging.getLogger("prophet").setLevel(logging.WARNING)
    warnings.filterwarnings("ignore")


def errors(model, test, kind):
    pred = predict_ahead(model, test, kind, "reg")
    e = pred["predicted"].values - pred["actual"].values
    p = np.ceil(pred["persistence"].values) - pred["actual"].values
    return e, p


def work(args):
    """all fits of one (service, kind): every grid point on every training set that leaves out 1 or 2 runs"""
    quiet()
    service, kind, scenario, runs = args
    data = {r: load_run(scenario, r, service) for r in runs}
    # err[(frozenset left out, point index, test run)] = error array; persistence per test run
    err, persistence = {}, {}
    leave_outs = [frozenset([r]) for r in runs] + [frozenset(c) for c in itertools.combinations(runs, 2)]
    for out in leave_outs:
        train = pd.concat([data[r] for r in runs if r not in out])
        for i, point in enumerate(POINTS):
            model = fit(train, kind, "reg", point)
            for r in out:
                e, p = errors(model, data[r], kind)
                err[(out, i, r)] = e
                persistence[r] = p
    mae = {k: np.abs(v).mean() for k, v in err.items()}
    rows = []

    # 1. nested CV: outer test run r, inner leave-one-run-out over the other runs picks the point
    for r in runs:
        others = [s for s in runs if s != r]
        inner = [np.mean([mae[(frozenset([r, s]), i, s)] for s in others]) for i in range(len(POINTS))]
        best = int(np.argmin(inner))
        d = POINTS.index(DEFAULT)
        for name, e in [("tuned (nested CV)", err[(frozenset([r]), best, r)]),
                        ("Prophet defaults", err[(frozenset([r]), d, r)]),
                        ("same as now", persistence[r])]:
            rows.append({"service": service, "kind": kind, "test_run": r, "model": name,
                         "mae": np.abs(e).mean(), "under_pct": 100 * (e < 0).mean(), "n": len(e),
                         **({k: POINTS[best][k] for k in GRID} if name.startswith("tuned") else {})})

    # 2. final choice: leave-one-run-out over all runs
    tuning = [{"service": service, "kind": kind, **point,
               "cv_mae": np.mean([mae[(frozenset([r]), i, r)] for r in runs])} for i, point in enumerate(POINTS)]
    best = POINTS[int(np.argmin([t["cv_mae"] for t in tuning]))]
    model = fit(pd.concat(data.values()), kind, "reg", best)
    return service, kind, rows, tuning, best, pickle.dumps(model)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="2R-20")
    parser.add_argument("--runs", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    parser.add_argument("--out", default="models_5runs_cv")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    args = parser.parse_args()
    out = Path(__file__).resolve().parent / args.out
    if out.exists() and any(out.glob("*.pkl")):
        raise SystemExit(f"{out} already has models; pick another --out")
    out.mkdir(parents=True, exist_ok=True)

    jobs = [(s, k, args.scenario, args.runs) for s in MICROSERVICES for k in MODELS]
    print(f"{len(jobs)} models x {len(POINTS)} grid points, runs {args.runs}, {args.workers} workers")
    t0 = time.time()
    nested, tuning, best_rows = [], [], []
    with ProcessPoolExecutor(args.workers) as pool:
        for service, kind, rows, tune, best, blob in pool.map(work, jobs):
            nested += rows
            tuning += tune
            best_rows.append({"service": service, "kind": kind, **best})
            (out / f"{service}_{SUFFIX[kind]}.pkl").write_bytes(blob)
            print(f"  {service:22s} {kind:8s} best {best}  ({time.time() - t0:.0f}s)")

    nested = pd.DataFrame(nested)
    nested.to_csv(out / "nested_cv.csv", index=False)
    pd.DataFrame(tuning).to_csv(out / "tuning.csv", index=False)
    pd.DataFrame(best_rows).to_csv(out / "best_params.csv", index=False)
    summary = (nested.assign(err_sum=nested["mae"] * nested["n"], under_sum=nested["under_pct"] * nested["n"])
               .groupby(["kind", "model"])[["err_sum", "under_sum", "n"]].sum())
    summary["mae"] = summary["err_sum"] / summary["n"]
    summary["under_pct"] = summary["under_sum"] / summary["n"]
    print("\nNested CV, all services and held-out runs pooled (replicas):")
    print(summary[["mae", "under_pct"]].round(2).to_string())
    print(f"\nModels and tables written to {out}")


if __name__ == "__main__":
    main()
