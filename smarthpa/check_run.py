# Checks that one finished run (results/<scenario>/<autoscaler>/run<N>/) was not damaged by the laptop losing its
# connection to the cluster. Such a run shows up as Locust windows with almost no requests (connect timeouts) while all
# users are active, a high failure rate, or gaps in cluster_metrics.csv. Exit code 1 = invalid, the reason is printed.
#
# Thresholds (calibrated on the runs of 05/10: a 2-minute outage gave 2.2% failures and 7 empty windows; normal runs
# stay below 0.2% failures with no empty window):
#   - a 10 s window with < 10% of the median request count while >= 75% of the users are active (the last window,
#     cut short when Locust stops, is ignored)
#   - failed requests > 1%
#   - more than 4 failed cluster_recorder snapshots (about 1 minute of missing cluster metrics)
#
# Quota check (added 12/11 after ProSmart HPA ran 30.5 pods on a 22-pod quota for a whole batch): the replicas the
# auto-scaler runs (Knowledge Base column C x CPU request, summed over the services) must stay within the scenario
# quota (maxR x request summed). Above it in more than 5% of the controller iterations = a controller bug, not a
# connection problem: exit code 2, so run_batch.ps1 stops at once instead of retrying the same bug.
#
# Usage: python check_run.py <run_dir>

import csv
import os
import re
import statistics
import sys

from make_run_report import CPU_REQUEST, SERVICES, load_kb

WINDOW_SEC = 10
MAX_FAIL_PCT = 1.0
MAX_RECORDER_FAILURES = 4
MAX_ABOVE_QUOTA_PCT = 5.0


def check_quota(run_dir):
    m = re.search(r"(\d+)R-\d+", os.path.abspath(run_dir).replace("\\", "/"))
    if not m or not os.path.isdir(os.path.join(run_dir, "knowledge_base")):
        return []
    quota = sum(int(m.group(1)) * CPU_REQUEST.get(s, 100) for s in SERVICES)
    kb = {s: load_kb(run_dir, s) for s in SERVICES}
    n = min(len(v["t"]) for v in kb.values())
    if n == 0:
        return []
    running = [sum(kb[s]["supply"][i] for s in SERVICES) for i in range(n)]
    above = sum(r > quota for r in running)
    if 100 * above / n > MAX_ABOVE_QUOTA_PCT:
        return [f"QUOTA: replicas above the {quota} m quota in {above}/{n} iterations (max {max(running):.0f} m)"]
    return []


def check(run_dir):
    with open(os.path.join(run_dir, "locust_stats_history.csv"), newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["Name"] == "Aggregated"]
    if len(rows) < 2:
        return ["locust_stats_history.csv has no data"]

    t0 = int(rows[0]["Timestamp"])
    max_users = max(int(r["User Count"]) for r in rows)
    windows = {}                                    # window index -> [requests, max users]
    for prev, cur in zip(rows, rows[1:]):
        w = windows.setdefault((int(cur["Timestamp"]) - t0) // WINDOW_SEC, [0, 0])
        w[0] += int(cur["Total Request Count"]) - int(prev["Total Request Count"])
        w[1] = max(w[1], int(cur["User Count"]))
    last = max(windows)
    steady = {k: v[0] for k, v in windows.items() if v[1] >= 0.75 * max_users and k != last}

    problems = []
    if steady:
        median = statistics.median(steady.values())
        empty = sorted(k * WINDOW_SEC for k, n in steady.items() if n < 0.1 * median)
        if empty:
            problems.append(f"{len(empty)} window(s) of {WINDOW_SEC}s with almost no requests at t={empty}s "
                            f"(median {median:.0f} requests per window)")

    total = int(rows[-1]["Total Request Count"])
    failed = int(rows[-1]["Total Failure Count"])
    if total and 100 * failed / total > MAX_FAIL_PCT:
        problems.append(f"{failed}/{total} requests failed ({100 * failed / total:.2f}% > {MAX_FAIL_PCT}%)")

    recorder_log = os.path.join(run_dir, "recorder.err.log")
    if os.path.exists(recorder_log):
        with open(recorder_log, encoding="utf-8", errors="ignore") as f:
            n = f.read().count("snapshot failed")
        if n > MAX_RECORDER_FAILURES:
            problems.append(f"{n} cluster_recorder snapshots failed (> {MAX_RECORDER_FAILURES})")
    return problems


if __name__ == "__main__":
    quota_problems = check_quota(sys.argv[1])
    problems = check(sys.argv[1]) + quota_problems
    for p in problems:
        print(f"INVALID: {p}")
    if not problems:
        print("Run check passed")
    sys.exit(2 if quota_problems else 1 if problems else 0)
