# Independent cluster snapshot recorder, run alongside BOTH autoscalers.
# Every INTERVAL seconds it appends one row per deployment to a CSV: spec/ready replicas, the HPA's own view
# (if an HPA exists), and cluster-wide Pending / Terminating pod counts. Used to check the "no Pending pods" criterion
# and to cross-check the Knowledge Base, independently of the Smart HPA code.
#
# Usage: python cluster_recorder.py <output.csv> <duration_sec> [interval_sec]

import csv
import json
import subprocess
import sys
import time


def kubectl_json(*args):
    out = subprocess.run(["kubectl", *args, "-o", "json"], capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip())
    return json.loads(out.stdout)


def snapshot():
    deploys = kubectl_json("get", "deployments")["items"]
    pods = kubectl_json("get", "pods")["items"]
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
    start = time.time()
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        while (elapsed := time.time() - start) < duration:
            stamp = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                for row in snapshot():
                    writer.writerow({"elapsed_sec": round(elapsed, 1), "timestamp": stamp, **row})
            except Exception as exc:                       # keep recording even if one kubectl call fails
                print(f"[recorder] {stamp} snapshot failed: {exc}", file=sys.stderr, flush=True)
            f.flush()
            time.sleep(max(0.0, interval - (time.time() - start - elapsed)))


if __name__ == "__main__":
    main()
