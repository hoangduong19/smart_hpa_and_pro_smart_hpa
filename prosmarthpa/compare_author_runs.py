"""ProSmart HPA on the cluster with our PROPHET models vs the authors' models (2R-20%): how the replicas end up.

Reads the runs written by run_experiment.ps1 (-Autoscaler prosmarthpa / prosmarthpa-authors):
  - cluster_metrics.csv: replicas per deployment over time (what really ran),
  - controller.out.log: per cycle and service CR->DR/maxR(pdr X), X = predicted desired replicas at t + 25 s.

Usage:
  python compare_author_runs.py      # writes results/2R-20/comparison_prophet_authors/replicas.csv, replicas.md, fig_replicas.png
"""

import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from train_prophet import DEMO_DIR, MICROSERVICES

SCENARIO = "2R-20"
RUNS = [1, 2, 3, 4, 5]
STEADY_FROM_SEC = 300               # end of the 5-minute ramp
TOTAL_QUOTA = 22                    # 11 services x maxR 2
VERSIONS = {"prosmarthpa": ("Our models", "#2ca02c"),
            "prosmarthpa-authors": ("Authors' models", "#d62728")}
OUT_DIR = DEMO_DIR / "results" / SCENARIO / "comparison_prophet_authors"
CYCLE = re.compile(r"^\s*([\d.]+)s ARM=\d (.*)$")
SERVICE = re.compile(r"([\w-]+):(\d+)->(\d+)/(\d+)\(pdr (\d+)\)")


def run_dir(version, run):
    return DEMO_DIR / "results" / SCENARIO / version / f"run{run}"


def load_replicas(version, run):
    df = pd.read_csv(run_dir(version, run) / "cluster_metrics.csv")
    return df.pivot_table(index="elapsed_sec", columns="deployment", values="spec_replicas")


def load_cycles(version, run):
    rows = []
    for line in (run_dir(version, run) / "controller.out.log").read_text(encoding="utf-8").splitlines():
        m = CYCLE.match(line)
        if not m:
            continue
        for s, cr, dr, max_r, pdr in SERVICE.findall(m.group(2)):
            rows.append({"t": float(m.group(1)), "service": s, "cr": int(cr), "dr": int(dr),
                         "max_r": int(max_r), "pdr": int(pdr)})
    return pd.DataFrame(rows)


def steady_table():
    rows = []
    for version, (label, _) in VERSIONS.items():
        cycles = pd.concat([load_cycles(version, r) for r in RUNS])
        cycles = cycles[cycles["t"] >= STEADY_FROM_SEC]
        replicas = pd.concat([load_replicas(version, r) for r in RUNS])
        replicas = replicas[replicas.index >= STEADY_FROM_SEC]
        for s in MICROSERVICES:
            c = cycles[cycles["service"] == s]
            rows.append({"models": label, "service": s, "pdr_mean": c["pdr"].mean(),
                         "maxR_min": c["max_r"].min(), "maxR_max": c["max_r"].max(),
                         "replicas_min": replicas[s].min(), "replicas_max": replicas[s].max()})
    return pd.DataFrame(rows)


def plot(path):
    panels = [("frontend", "frontend"), ("currencyservice", "currencyservice"), (None, "Total over 11 services")]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    for ax, (s, title) in zip(axes, panels):
        for version, (label, color) in VERSIONS.items():
            for i, run in enumerate(RUNS):
                r = load_replicas(version, run)
                y = r.sum(axis=1) if s is None else r[s]
                ax.plot(r.index / 60, y.values, color=color, alpha=0.6, lw=1.2,
                        label=f"{label} (5 runs)" if i == 0 else None)
        if s is None:
            ax.axhline(TOTAL_QUOTA, color="black", ls="--", lw=1, label=f"Total quota ({TOTAL_QUOTA} replicas)")
        ax.set_title(title)
        ax.set_xlabel("Time (min)")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Running replicas")
    axes[2].legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table = steady_table()
    table.to_csv(OUT_DIR / "replicas.csv", index=False)
    plot(OUT_DIR / "fig_replicas.png")

    lines = ["# ProSmart HPA replicas: our models vs the authors' models (2R-20%)", "",
             f"Runs {RUNS}, from minute {STEADY_FROM_SEC // 60}. pdr = predicted desired replicas (t + 25 s).", "",
             "```", table.round(2).to_string(index=False), "```", ""]
    (OUT_DIR / "replicas.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
