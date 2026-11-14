"""How much does the prediction window change what ProSmart HPA predicts?

ProSmart HPA (prosmart_hpa.py) asks the demand model for y at ds = ceil(t/5)*5 + window, with the regressors
(cpu_pct, current_replicas) observed now, at t. Only ds moves with the window. This script replays every
5-s point of the Smart HPA runs through the demand models exactly like the controller (same rounding, ceil of yhat)
for windows 5..30 s and reports how often the predicted desired replicas (PDR) differ between windows.

Run from prosmarthpa/:  D:\\prosmart-venv\\Scripts\\python.exe window_sensitivity.py [--scenario 2R-20] [--runs 1 2 3 4 5]
Output: results/<scenario>/comparison_prosmart_figs/window_sensitivity.csv
"""
import argparse
import logging
import math

import numpy as np
import pandas as pd

from compare_author_models import AUTHOR_MODELS, SUFFIX, load_model
from train_prophet import DEMO_DIR, load_run

logging.getLogger("cmdstanpy").setLevel(logging.WARNING)

SERVICES = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend",
            "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice"]
WINDOWS = [5, 10, 15, 20, 25, 30]
STEP, START, DURATION = 5, 10, 900


def p_time(t, window):
    return min(math.ceil(t / STEP) * STEP + window, DURATION)


def ours(service):
    import pickle
    with open(DEMO_DIR / "prosmarthpa" / "models_5runs_cv" / f"{service}_Demand_Model.pkl", "rb") as f:
        return pickle.load(f)


def pdr_table(model, data, with_regressors):
    out = {}
    for w in WINDOWS:
        future = pd.DataFrame({"ds": pd.to_datetime([p_time(t, w) for t in data["t"]], unit="s")})
        if with_regressors:
            future["cpu_pct"] = data["cpu_pct"].values
            future["current_replicas"] = data["current_replicas"].values
        out[w] = np.ceil(model.predict(future)["yhat"].values)
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="2R-20")
    parser.add_argument("--runs", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    args = parser.parse_args()

    rows = []
    for service in SERVICES:
        data = pd.concat([load_run(args.scenario, r, service) for r in args.runs])
        data = data[data["t"] > START].reset_index(drop=True)
        for label, model, reg in [("ours_cv", ours(service), True),
                                  ("authors", load_model(AUTHOR_MODELS["demand"] / f"{service}_{SUFFIX['demand']}.pkl"), False)]:
            model.uncertainty_samples = 0
            pdr = pdr_table(model, data, reg)
            for w in WINDOWS:
                rows.append({"model": label, "service": service, "window_sec": w, "points": len(data),
                             "pct_points_pdr_differs_from_5s": round(100 * np.mean(pdr[w] != pdr[5]), 1),
                             "mean_abs_diff_vs_5s": round(float(np.mean(np.abs(pdr[w] - pdr[5]))), 3)})
    table = pd.DataFrame(rows)
    out = DEMO_DIR / "results" / args.scenario / "comparison_prosmart_figs" / "window_sensitivity.csv"
    table.to_csv(out, index=False)
    summary = table.groupby(["model", "window_sec"])[["pct_points_pdr_differs_from_5s", "mean_abs_diff_vs_5s"]].mean()
    print(summary.round(2).to_string())
    print(f"Written to {out}")
