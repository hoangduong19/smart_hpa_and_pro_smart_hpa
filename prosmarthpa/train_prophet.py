"""Train the 22 PROPHET models of ProSmart HPA from our own Smart HPA Knowledge Base runs.

How the authors built theirs (read from the released .pkl files, prophet 1.1.4):
  * one model per microservice for demand (y = "Desired Replicas") and one for capacity (y = "Max. Replicas")
  * training data = Knowledge Base of 10 Smart HPA runs of 2R-20%, each resampled to a 5 s grid 0..900 s
    (181 points x 10 runs = 1810 rows, values linearly interpolated -> non-integer y)
  * ds = 1970-01-01 00:00:00 + test time, linear growth, default hyper-parameters, NO extra regressors

The paper (Section 5.1) instead says the models use regressors (CPU usage, CPU threshold, current replicas).
Both variants are supported:
  --mode time  : like the released .pkl files (time only)
  --mode reg   : like the paper text (time + regressors observed at prediction time)   [default, used for our runs]

Regressors that are constant in a scenario (CPU threshold, SLA maxR) carry no information and are left out.

Usage:
  python train_prophet.py --scenario 2R-20 --runs 1 2 3            # train on all runs, save models/
  python train_prophet.py --scenario 2R-20 --runs 1 2 3 --evaluate # leave-one-run-out check, no models saved
"""

import argparse
import logging
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from prophet import Prophet

logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
logging.getLogger("prophet").setLevel(logging.WARNING)

DEMO_DIR = Path(__file__).resolve().parent.parent
MICROSERVICES = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend",
                 "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice"]

GRID_STEP_SEC = 5
TEST_DURATION_SEC = 900
PREDICTION_WINDOW_SEC = 25          # best window in the paper (Section 5.3)
PREDICTION_START_SEC = 10           # ProSmart managers only predict after 10 s of load

KB_COLUMNS = {"Test Time (sec)": "t", "CPU Usage Percentage": "cpu_pct", "Current Replicas": "current_replicas",
              "Desired Replicas": "desired", "Max. Replicas": "max_replicas"}

# target column and regressors per model kind
MODELS = {
    "demand":   {"y": "desired",      "regressors": ["cpu_pct", "current_replicas"]},
    "capacity": {"y": "max_replicas", "regressors": ["desired", "current_replicas"]},
}


def load_run(scenario, run, service):
    """One Smart HPA run of one microservice, resampled to the 5 s grid like the authors' training data."""
    path = DEMO_DIR / "results" / scenario / "smarthpa" / f"run{run}" / "knowledge_base" / f"{service}.xlsx"
    kb = pd.read_excel(path).rename(columns=KB_COLUMNS)[list(KB_COLUMNS.values())].dropna()
    kb = kb.sort_values("t")
    grid = np.arange(0, TEST_DURATION_SEC + 1, GRID_STEP_SEC)
    out = pd.DataFrame({"t": grid})
    for col in ["cpu_pct", "current_replicas", "desired", "max_replicas"]:
        out[col] = np.interp(grid, kb["t"], kb[col].astype(float))
    out["ds"] = pd.to_datetime(out["t"], unit="s")
    out["run"] = run
    return out


def fit(train, kind, mode):
    spec = MODELS[kind]
    model = Prophet()                                   # default hyper-parameters, as in the released models
    columns = ["ds", spec["y"]]
    if mode == "reg":
        for reg in spec["regressors"]:
            model.add_regressor(reg)
        columns += spec["regressors"]
    model.fit(train[columns].rename(columns={spec["y"]: "y"}))
    return model


def predict_ahead(model, test, kind, mode):
    """At every grid time t >= 10 s predict y(t + 25 s) using only what is known at t (as the managers do)."""
    spec = MODELS[kind]
    now = test[test["t"] >= PREDICTION_START_SEC].copy()
    target_t = np.minimum(np.ceil(now["t"] / GRID_STEP_SEC) * GRID_STEP_SEC + PREDICTION_WINDOW_SEC, TEST_DURATION_SEC)
    future = pd.DataFrame({"ds": pd.to_datetime(target_t, unit="s").values})
    if mode == "reg":
        for reg in spec["regressors"]:
            future[reg] = now[reg].values               # regressor values observed now, not in the future
    yhat = model.predict(future)["yhat"].values
    actual = np.interp(target_t, test["t"], test[spec["y"]])
    return pd.DataFrame({"t": now["t"].values, "target_t": target_t, "actual": actual,
                         "predicted": np.ceil(yhat),       # managers use math.ceil(yhat)
                         "persistence": now[spec["y"]].values})  # reactive baseline: value now


def evaluate(scenario, runs, modes):
    rows = []
    for service in MICROSERVICES:
        data = pd.concat([load_run(scenario, r, service) for r in runs])
        for kind in MODELS:
            for mode in modes:
                for test_run in runs:
                    train = data[data["run"] != test_run]
                    test = data[data["run"] == test_run]
                    pred = predict_ahead(fit(train, kind, mode), test, kind, mode)
                    rows.append({"service": service, "kind": kind, "mode": mode, "test_run": test_run,
                                 "mae_model": (pred["predicted"] - pred["actual"]).abs().mean(),
                                 "mae_persistence": (np.ceil(pred["persistence"]) - pred["actual"]).abs().mean()})
    res = pd.DataFrame(rows)
    summary = res.groupby(["kind", "mode", "service"])[["mae_model", "mae_persistence"]].mean().round(2)
    print(summary.to_string())
    print()
    print(res.groupby(["kind", "mode"])[["mae_model", "mae_persistence"]].mean().round(2).to_string())
    return res


def train_and_save(scenario, runs, mode, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for service in MICROSERVICES:
        data = pd.concat([load_run(scenario, r, service) for r in runs])
        for kind, suffix in [("demand", "Demand_Model"), ("capacity", "capacity_model")]:
            model = fit(data, kind, mode)
            with open(out_dir / f"{service}_{suffix}.pkl", "wb") as f:
                pickle.dump(model, f)
            print(f"saved {service}_{suffix}.pkl  ({len(data)} rows, mode={mode})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="2R-20")
    parser.add_argument("--runs", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--mode", choices=["time", "reg"], default="reg")
    parser.add_argument("--evaluate", action="store_true", help="leave-one-run-out check of both modes")
    parser.add_argument("--out", default=str(Path(__file__).resolve().parent / "models"))
    args = parser.parse_args()

    if args.evaluate:
        result = evaluate(args.scenario, args.runs, ["time", "reg"])
        result.to_csv(Path(__file__).resolve().parent / "train_evaluation.csv", index=False)
    else:
        train_and_save(args.scenario, args.runs, args.mode, Path(args.out))
