"""Compare the authors' 22 released PROPHET models with ours, as evidence for retraining them.

Three checks, all offline (no cluster):
  1. What the authors trained on: the training data stored inside each .pkl (model.history).
     If the total maxR over the 11 services is the same on every row while single services change,
     the data comes from Smart HPA (quota exchange), not from K8s HPA (fixed maxR).
  2. Authors' training data vs our Smart HPA Knowledge Base, per service (demand level, maxR range).
  3. Prediction error on Smart HPA runs not used to train our models (run 4-5): predict y(t + 25 s)
     like the managers do, authors' models (time only) vs ours (reg) vs the "same as now" baseline.

The authors pickled with prophet 1.1.4; on 1.1.5 three attributes are missing and are set to the 1.1.4 behaviour.

Usage:
  python compare_author_models.py      # writes results/2R-20/comparison/prophet_models/
"""

import logging
import pickle
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from train_prophet import DEMO_DIR, MICROSERVICES, load_run, predict_ahead

logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=FutureWarning)

SCENARIO = "2R-20"
OUR_RUNS = [1, 2, 3, 4, 5]          # all our Smart HPA 2R-20% runs (data comparison)
TEST_RUNS = [4, 5]                  # not used to train prosmarthpa/models (trained on run 1-3)
STEADY_FROM_SEC = 300               # end of the 5-minute ramp

AUTHOR_DIR = DEMO_DIR / "Pro_Smart_HPA" / "ProSmart_HPA" / "ProSmart HPA Codebase"
AUTHOR_MODELS = {
    "demand":   AUTHOR_DIR / "Microservice Managers" / "Trained PROPHET models - Resource Demand Prediction",
    "capacity": AUTHOR_DIR / "Trained PROPHET models - Resource Capacity Prediction",
}
OUR_MODELS = DEMO_DIR / "prosmarthpa" / "models"
SUFFIX = {"demand": "Demand_Model", "capacity": "capacity_model"}
OUT_DIR = DEMO_DIR / "results" / SCENARIO / "comparison" / "prophet_models"


def load_model(path):
    with open(path, "rb") as f:
        model = pickle.load(f)
    for attr, value in {"scaling": "absmax", "y_min": 0.0, "holidays_mode": model.seasonality_mode}.items():
        if not hasattr(model, attr):
            setattr(model, attr, value)
    return model


def author_history(kind, service):
    """Training data inside one of the authors' .pkl: columns t (s) and y."""
    h = load_model(AUTHOR_MODELS[kind] / f"{service}_{SUFFIX[kind]}.pkl").history
    return pd.DataFrame({"t": (h["ds"] - pd.Timestamp(0)).dt.total_seconds(), "y": h["y"].values})


def check_training_source():
    caps = pd.DataFrame({s: author_history("capacity", s)["y"].values for s in MICROSERVICES})
    total = caps.sum(axis=1)
    return {"rows": len(caps), "runs": len(caps) // 181,
            "total_maxR_min": total.min(), "total_maxR_max": total.max(),
            "rows_with_quota_moved": int((caps != 2).any(axis=1).sum())}


def compare_data():
    rows = []
    for s in MICROSERVICES:
        dem, cap = author_history("demand", s), author_history("capacity", s)
        ours = pd.concat([load_run(SCENARIO, r, s) for r in OUR_RUNS])
        a_steady = dem[dem["t"] >= STEADY_FROM_SEC]["y"].mean()
        o_steady = ours[ours["t"] >= STEADY_FROM_SEC]["desired"].mean()
        rows.append({"service": s,
                     "authors_DR_steady": a_steady, "ours_DR_steady": o_steady,
                     "diff_pct": 100 * (o_steady / a_steady - 1),
                     "authors_maxR_min": cap["y"].min(), "authors_maxR_max": cap["y"].max(),
                     "ours_maxR_min": ours["max_replicas"].min(), "ours_maxR_max": ours["max_replicas"].max()})
    return pd.DataFrame(rows)


def evaluate():
    errors = {}
    for s in MICROSERVICES:
        for kind in SUFFIX:
            authors = load_model(AUTHOR_MODELS[kind] / f"{s}_{SUFFIX[kind]}.pkl")
            ours = load_model(OUR_MODELS / f"{s}_{SUFFIX[kind]}.pkl")
            for run in TEST_RUNS:
                test = load_run(SCENARIO, run, s)
                pa = predict_ahead(authors, test, kind, "time")
                po = predict_ahead(ours, test, kind, "reg")
                for name, pred in [("authors", pa["predicted"]), ("ours", po["predicted"]),
                                   ("same_as_now", np.ceil(pa["persistence"]))]:
                    errors.setdefault((kind, name), []).append(pred.values - pa["actual"].values)
    rows = []
    for (kind, name), parts in errors.items():
        e = np.concatenate(parts)
        rows.append({"kind": kind, "model": name, "mae": np.abs(e).mean(), "under_pct": 100 * (e < 0).mean()})
    return pd.DataFrame(rows)


def plot(path):
    panels = [("frontend", "demand", "frontend: Desired Replicas"),
              ("currencyservice", "demand", "currencyservice: Desired Replicas"),
              ("currencyservice", "capacity", "currencyservice: maxR")]
    column = {"demand": "desired", "capacity": "max_replicas"}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    for ax, (s, kind, title) in zip(axes, panels):
        a = author_history(kind, s).groupby("t")["y"].mean()
        o = pd.concat([load_run(SCENARIO, r, s) for r in OUR_RUNS]).groupby("t")[column[kind]].mean()
        ax.plot(a.index / 60, a.values, color="#d62728", label="Training data of the authors' model (10 runs)")
        ax.plot(o.index / 60, o.values, color="#1f77b4", label="Smart HPA on our cluster (5 runs)")
        ax.set_title(title)
        ax.set_xlabel("Time (min)")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Replicas (mean over runs)")
    axes[0].legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source = check_training_source()
    data = compare_data()
    errors = evaluate()
    data.to_csv(OUT_DIR / "data_comparison.csv", index=False)
    errors.to_csv(OUT_DIR / "offline_errors.csv", index=False)
    plot(OUT_DIR / "fig_author_vs_group.png")

    lines = ["# Authors' PROPHET models vs ours (2R-20%)", "",
             "## 1. What the authors trained on", "",
             f"- {source['rows']} rows = {source['runs']} runs x 181 points (5 s grid, 0-900 s)",
             f"- total maxR over the 11 services: {source['total_maxR_min']:g} to {source['total_maxR_max']:g} on every row",
             f"- rows where some service maxR differs from 2 (quota moved): {source['rows_with_quota_moved']}",
             "", f"## 2. Training data vs our Smart HPA Knowledge Base (runs {OUR_RUNS}), DR mean from minute 5", "",
             "```", data.round(2).to_string(index=False), "```",
             "", f"## 3. Prediction error at t + 25 s on runs {TEST_RUNS} (replicas)", "",
             "```", errors.round(2).to_string(index=False), "```", ""]
    (OUT_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
