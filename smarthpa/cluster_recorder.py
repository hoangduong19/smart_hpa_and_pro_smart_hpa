# Independent cluster snapshot recorder, run alongside BOTH autoscalers.
# Every INTERVAL seconds it appends one row per deployment to a CSV: spec/ready replicas, the HPA's own view
# (if an HPA exists), and cluster-wide Pending / Terminating pod counts. Used to check the "no Pending pods" criterion
# and to cross-check the Knowledge Base, independently of the Smart HPA code.
#
# Since 19/11 it also writes pod_metrics.csv next to the output: one row per pod per snapshot with CPU / memory from
# `kubectl top pods`, node, restarts and pod age. Diagnostic only (C4 run 1: one currencyservice pod used 181% CPU vs
# 101% in every comparable run and nothing recorded why). A failed `kubectl top` is logged as "pod metrics
# unavailable", which check_run.py does not count as a failed snapshot (metrics-server lags new pods by ~1 min).
#
# Usage: python cluster_recorder.py <output.csv> <duration_sec> [interval_sec]

import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

POD_FIELDS = ["elapsed_sec", "timestamp", "pod", "app", "node", "cpu_m", "memory_mi", "memory_limit_mi", "restarts",
              "age_sec"]
_UNIT_MI = {"Ki": 1 / 1024, "Mi": 1, "Gi": 1024}


def kubectl_json(*args):
    out = subprocess.run(["kubectl", *args, "-o", "json"], capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip())
    return json.loads(out.stdout)


def _mi(value):
    m = re.fullmatch(r"(\d+)(Ki|Mi|Gi)", value or "")
    return round(float(m.group(1)) * _UNIT_MI[m.group(2)], 1) if m else ""


def pod_rows(pods):
    """per-pod CPU / memory from metrics-server, joined with app label, node, restarts and age"""
    out = subprocess.run(["kubectl", "top", "pods", "--no-headers"], capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip())
    usage = {}
    for line in out.stdout.splitlines():
        c = line.split()
        if len(c) >= 3 and c[1].endswith("m"):
            usage[c[0]] = (int(c[1][:-1]), _mi(c[2]))
    now = datetime.now(timezone.utc)
    rows = []
    for p in pods:
        name = p["metadata"]["name"]
        if name not in usage:
            continue
        start = p["status"].get("startTime")
        age = (now - datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds() if start else ""
        rows.append({"pod": name, "app": p["metadata"].get("labels", {}).get("app", ""),
                     "node": p["spec"].get("nodeName", ""), "cpu_m": usage[name][0], "memory_mi": usage[name][1],
                     "memory_limit_mi": _mi(p["spec"]["containers"][0].get("resources", {}).get("limits", {}).get("memory")),
                     "restarts": sum(s.get("restartCount", 0) for s in p["status"].get("containerStatuses", [])),
                     "age_sec": round(age) if age != "" else ""})
    return rows


def snapshot():
    deploys = kubectl_json("get", "deployments")["items"]
    pods = kubectl_json("get", "pods")["items"]
    snapshot.pods = pods                                   # reused by pod_rows() for the same snapshot
    try:
        hpas = {h["spec"]["scaleTargetRef"]["name"]: h for h in kubectl_json("get", "hpa")["items"]}
    except RuntimeError:
        hpas = {}

    pending = sum(1 for p in pods if p["status"].get("phase") == "Pending")
    # Phase "Pending" also covers pods that are scheduled but still starting (ContainerCreating). Only pods the
    # scheduler could not place (PodScheduled=False) mean the cluster ran out of capacity.
    unschedulable = sum(1 for p in pods if any(c.get("type") == "PodScheduled" and c.get("status") == "False"
                                               for c in p["status"].get("conditions", [])))
    terminating = sum(1 for p in pods if p["metadata"].get("deletionTimestamp"))

    rows = []
    for d in deploys:
        name = d["metadata"]["name"]
        hpa = hpas.get(name)
        rows.append({
            "deployment": name,
            "spec_replicas": d["spec"].get("replicas"),
            "ready_replicas": d["status"].get("readyReplicas", 0),
            "available_replicas": d["status"].get("availableReplicas", 0),
            "hpa_desired": hpa["status"].get("desiredReplicas") if hpa else "",
            "hpa_max": hpa["spec"].get("maxReplicas") if hpa else "",
            "pending_pods_total": pending,
            "unschedulable_pods_total": unschedulable,
            "terminating_pods_total": terminating,
        })
    return rows


def main():
    out_path = sys.argv[1]
    duration = float(sys.argv[2])
    interval = float(sys.argv[3]) if len(sys.argv) > 3 else 15.0

    fields = ["elapsed_sec", "timestamp", "deployment", "spec_replicas", "ready_replicas", "available_replicas",
              "hpa_desired", "hpa_max", "pending_pods_total", "unschedulable_pods_total", "terminating_pods_total"]
    pod_path = os.path.join(os.path.dirname(out_path), "pod_metrics.csv")
    start = time.time()
    with open(out_path, "w", newline="") as f, open(pod_path, "w", newline="") as pf:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        pod_writer = csv.DictWriter(pf, fieldnames=POD_FIELDS)
        pod_writer.writeheader()
        while (elapsed := time.time() - start) < duration:
            stamp = time.strftime("%Y-%m-%d %H:%M:%S")
            snapshot.pods = None
            try:
                for row in snapshot():
                    writer.writerow({"elapsed_sec": round(elapsed, 1), "timestamp": stamp, **row})
            except Exception as exc:                       # keep recording even if one kubectl call fails
                print(f"[recorder] {stamp} snapshot failed: {exc}", file=sys.stderr, flush=True)
            if snapshot.pods is not None:
                try:
                    for row in pod_rows(snapshot.pods):
                        pod_writer.writerow({"elapsed_sec": round(elapsed, 1), "timestamp": stamp, **row})
                except Exception as exc:                   # not a failed snapshot for check_run.py
                    print(f"[recorder] {stamp} pod metrics unavailable: {exc}", file=sys.stderr, flush=True)
            f.flush()
            pf.flush()
            time.sleep(max(0.0, interval - (time.time() - start - elapsed)))


if __name__ == "__main__":
    main()
