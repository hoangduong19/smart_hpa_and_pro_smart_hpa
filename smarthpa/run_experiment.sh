#!/usr/bin/env bash
# Linux port of run_experiment.ps1 for the experiment-runner VM (exp-runner, 192.168.161.13). Runs ONE experiment
# run end to end, same steps as the PowerShell version:
#   1. check kubectl targets the k3s lab cluster
#   2. reset: delete HPAs, scale every deployment to 1, wait until clean, restart pods near their memory limit, cool down
#   3. start the autoscaler under test (smarthpa | smarthpa-prio | smarthpa-flat | prosmarthpa* | k8shpa)
#   4. start cluster_recorder.py and Locust at the same time
#   5. stop everything, remove HPAs, copy Knowledge Base + logs to results/<scenario>[-spike][-<tag>]/<autoscaler>/run<N>/
#
# Run on the VM, from any directory:
#   ./run_experiment.sh --autoscaler k8shpa --scenario 2R-20% --run 1 --spawn-rate 2 --tag pilot2s
#   ./run_experiment.sh --autoscaler smarthpa --scenario 5R-50% --run 0 --duration 300 --users 100 --cooldown 60
# Exit code: 0 ok, 1 failed run (data moved to _failed_run<N>_<time>), 2 replicas above quota (controller bug).
set -uo pipefail

AUTOSCALER=""; SCENARIO=""; RUN=""
USERS=200; SPAWN_RATE=0.67; DURATION=900; COOLDOWN=300; SHAPE="ramp"; TAG=""
TARGET_HOST="http://192.168.161.10"; EXPECTED_CONTEXT="k3s-lab"; FORCE=0; KUBECTL_DELAY=0; ARM_WARMUP=""
POD_WARMUP=0; POD_WARMUP_USERS=50
while [ $# -gt 0 ]; do
    case "$1" in
        --autoscaler) AUTOSCALER="$2"; shift 2 ;;
        --scenario) SCENARIO="$2"; shift 2 ;;
        --run) RUN="$2"; shift 2 ;;
        --users) USERS="$2"; shift 2 ;;
        --spawn-rate) SPAWN_RATE="$2"; shift 2 ;;
        --duration) DURATION="$2"; shift 2 ;;
        --cooldown) COOLDOWN="$2"; shift 2 ;;
        --shape) SHAPE="$2"; shift 2 ;;
        --tag) TAG="$2"; shift 2 ;;
        --kubectl-delay) KUBECTL_DELAY="$2"; shift 2 ;;   # SMARTHPA_KUBECTL_DELAY_SEC, see config.py
        --arm-warmup) ARM_WARMUP="$2"; shift 2 ;;        # SMARTHPA_ARM_WARMUP_SEC, improvement C4, see config.py
        --pod-warmup) POD_WARMUP="$2"; shift 2 ;;        # seconds of light load on the fresh pods before the cooldown
        --pod-warmup-users) POD_WARMUP_USERS="$2"; shift 2 ;;
        --host) TARGET_HOST="$2"; shift 2 ;;
        --force) FORCE=1; shift ;;
        *) echo "Unknown argument $1" >&2; exit 1 ;;
    esac
done
case "$AUTOSCALER" in
    smarthpa|smarthpa-warmup|smarthpa-prio|smarthpa-flat|prosmarthpa|prosmarthpa-authors|prosmarthpa-rerun|prosmarthpa-cv|prosmarthpa-cv-w5|prosmarthpa-cv-w10|prosmarthpa-cv-w15|prosmarthpa-cv-w20|prosmarthpa-cv-w30|k8shpa) ;;
    *) echo "--autoscaler missing or unknown: '$AUTOSCALER'" >&2; exit 1 ;;
esac
[[ "$SCENARIO" =~ ^([0-9]+)R-([0-9]+)%$ ]] || { echo "--scenario must look like 2R-20%" >&2; exit 1; }
MAXR="${BASH_REMATCH[1]}"; THRESHOLD="${BASH_REMATCH[2]}"
[[ "$RUN" =~ ^[0-9]+$ ]] || { echo "--run must be a number" >&2; exit 1; }
case "$SHAPE" in ramp|spike) ;; *) echo "--shape must be ramp or spike" >&2; exit 1 ;; esac

CODE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$HOME/venvs/smarthpa/bin/python"
LOCUST="$HOME/venvs/smarthpa/bin/locust"
PROSMART_PY="$HOME/venvs/prosmart/bin/python"          # prophet needs numpy < 2 / pandas 2.x, kept apart
export PATH="$HOME/bin:$PATH"                           # kubectl (k3s binary, same version as the cluster)
SCENARIO_DIR="${SCENARIO%\%}"
[ "$SHAPE" != "ramp" ] && SCENARIO_DIR+="-$SHAPE"
[ -n "$TAG" ] && SCENARIO_DIR+="-$TAG"                  # e.g. pilot runs, kept out of the official comparison
REL_OUT="../results/$SCENARIO_DIR/$AUTOSCALER/run$RUN"
OUT_DIR="$CODE_DIR/$REL_OUT"

log() { echo "[$(date +%H:%M:%S)] $*"; }

# ---------------------------------------------------------------- 1. Safety checks
CTX="$(kubectl config current-context)" || { log "ERROR: kubectl not configured"; exit 1; }
[ "$CTX" = "$EXPECTED_CONTEXT" ] || { log "ERROR: kubectl context is '$CTX', expected '$EXPECTED_CONTEXT'"; exit 1; }
if [ -d "$OUT_DIR" ] && [ "$FORCE" -eq 0 ]; then log "ERROR: $OUT_DIR already exists, use --force or another --run"; exit 1; fi
if [ "$AUTOSCALER" = "prosmarthpa-authors" ]; then MODEL_SET="authors"
elif [[ "$AUTOSCALER" == prosmarthpa-cv* ]]; then MODEL_SET="cv"
else MODEL_SET="ours"; fi
if [[ "$AUTOSCALER" == prosmarthpa* ]] && [ "$MODEL_SET" != "authors" ]; then
    MODEL_DIR="models"; [ "$MODEL_SET" = "cv" ] && MODEL_DIR="models_5runs_cv"
    N_MODELS=$(ls "$CODE_DIR/../prosmarthpa/$MODEL_DIR"/*.pkl 2>/dev/null | wc -l)
    [ "$N_MODELS" -eq 22 ] || { log "ERROR: expected 22 PROPHET models in prosmarthpa/$MODEL_DIR, found $N_MODELS"; exit 1; }
fi
WINDOW=25
[[ "$AUTOSCALER" =~ ^prosmarthpa-cv-w([0-9]+)$ ]] && WINDOW="${BASH_REMATCH[1]}"
ARM="paper"; [ "$AUTOSCALER" = "smarthpa-prio" ] && ARM="priority"; [ "$AUTOSCALER" = "smarthpa-flat" ] && ARM="flat"
# improvement C4: smarthpa-warmup = authors' ARM after a warm-up without quota exchange (default 120 s)
[ -z "$ARM_WARMUP" ] && { [ "$AUTOSCALER" = "smarthpa-warmup" ] && ARM_WARMUP=120 || ARM_WARMUP=0; }
LOAD="$USERS users @ $SPAWN_RATE/s, kubectl delay ${KUBECTL_DELAY}s"; [ "$SHAPE" = "spike" ] && LOAD="spike shape (locustfile_spike.py)"
log "Context $CTX | $AUTOSCALER | $SCENARIO (maxR=$MAXR, threshold=$THRESHOLD%) | run $RUN | $LOAD | ${DURATION}s | out $SCENARIO_DIR"

cd "$CODE_DIR" || exit 1
PIDS=()
FAILED=0; QUOTA_BUG=0; CONTROLLER_EXIT=""; MONITOR_ERRORS=0; STARTED_AT=""; FINISHED_AT=""

wait_clean() {   # every deployment at 1 ready replica, no terminating / pending pod (600 s max)
    local deadline=$(( $(date +%s) + 600 )) state
    while true; do
        state=$( { kubectl get deployments -o json && echo '#####' && kubectl get pods -o json; } | "$PY" -c '
import json, sys
deps, pods = sys.stdin.read().split("#####")
deps, pods = json.loads(deps)["items"], json.loads(pods)["items"]
nr = sum(1 for d in deps if d["spec"].get("replicas") != 1 or d["status"].get("readyReplicas") != 1)
term = sum(1 for p in pods if p["metadata"].get("deletionTimestamp"))
pend = sum(1 for p in pods if p["status"].get("phase") == "Pending")
print("ok" if nr == term == pend == 0 and len(pods) == len(deps) else f"notReady={nr} terminating={term} pending={pend}", len(deps))
' ) || state="kubectl-error 0"
        [ "${state%% *}" = "ok" ] && { N_DEPLOYMENTS="${state##* }"; return 0; }
        [ "$(date +%s)" -gt "$deadline" ] && { log "ERROR: cluster did not settle within 600s ($state)"; return 1; }
        sleep 5
    done
}

write_run_info() {
    AUTOSCALER="$AUTOSCALER" SCENARIO="$SCENARIO" RUN="$RUN" MAXR="$MAXR" THRESHOLD="$THRESHOLD" USERS="$USERS" \
    SPAWN_RATE="$SPAWN_RATE" DURATION="$DURATION" COOLDOWN="$COOLDOWN" SHAPE="$SHAPE" TAG="$TAG" TARGET_HOST="$TARGET_HOST" \
    CTX="$CTX" STARTED_AT="$STARTED_AT" FINISHED_AT="$FINISHED_AT" CONTROLLER_EXIT="$CONTROLLER_EXIT" \
    MONITOR_ERRORS="$MONITOR_ERRORS" WINDOW="$WINDOW" MODEL_SET="$MODEL_SET" KUBECTL_DELAY="$KUBECTL_DELAY" ARM_WARMUP="$ARM_WARMUP" POD_WARMUP="$POD_WARMUP" POD_WARMUP_USERS="$POD_WARMUP_USERS" \
    APP_IMAGE="$(kubectl get deployment adservice -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null)" \
    "$PY" - "$OUT_DIR/run_info.json" <<'PYEOF'
import json, os, sys
e = os.environ
info = {"autoscaler": e["AUTOSCALER"], "scenario": e["SCENARIO"], "run": int(e["RUN"]), "max_replicas": int(e["MAXR"]),
        "cpu_threshold": int(e["THRESHOLD"]), "users": int(e["USERS"]), "spawn_rate": float(e["SPAWN_RATE"]),
        "duration_sec": int(e["DURATION"]), "cooldown_sec": int(e["COOLDOWN"]), "shape": e["SHAPE"], "host": e["TARGET_HOST"],
        "kube_context": e["CTX"], "started_at": e["STARTED_AT"], "runner": "exp-runner VM (run_experiment.sh)"}
if e["TAG"]: info["tag"] = e["TAG"]
info["kubectl_delay_sec"] = float(e["KUBECTL_DELAY"])
info["arm_warmup_sec"] = float(e["ARM_WARMUP"])
info["pod_warmup_sec"] = int(e["POD_WARMUP"]); info["pod_warmup_users"] = int(e["POD_WARMUP_USERS"])
info["app_image_tag"] = e["APP_IMAGE"].rsplit(":", 1)[-1] if e["APP_IMAGE"] else ""
if e["AUTOSCALER"].startswith("prosmarthpa"):
    info["prediction_window_sec"] = int(e["WINDOW"]); info["prophet_models"] = e["MODEL_SET"]
    info["prophet_rounding"] = e.get("PROSMART_ROUNDING", "round")      # 20/11 E13; runs before 20/11 used ceil
info["monitor_kubectl_errors"] = int(e["MONITOR_ERRORS"])
if e["FINISHED_AT"]: info["finished_at"] = e["FINISHED_AT"]
if e["CONTROLLER_EXIT"] != "": info["controller_exit_code"] = int(e["CONTROLLER_EXIT"])
json.dump(info, open(sys.argv[1], "w"), indent=4)
PYEOF
}

cleanup_and_collect() {
    # ------------------------------------------------------------ 5. Clean up and collect
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then log "Stopping process group $pid"; kill -TERM -- "-$pid" 2>/dev/null; fi
    done
    sleep 2
    for pid in "${PIDS[@]}"; do kill -KILL -- "-$pid" 2>/dev/null; done
    if [ "$AUTOSCALER" = "k8shpa" ]; then
        if kubectl delete hpa --all --ignore-not-found >/dev/null; then log "Deleted Kubernetes HPAs"
        else log "WARNING: could not delete HPAs, the next run's reset will retry"; fi
    fi
    [ -d "$OUT_DIR" ] || return
    [ -d "$CODE_DIR/Knowledge Base" ] && cp -r "$CODE_DIR/Knowledge Base" "$OUT_DIR/knowledge_base"
    kubectl get pods -o wide > "$OUT_DIR/pods_at_end.txt" 2>&1
    [ -n "$STARTED_AT" ] && write_run_info
    if [ "$FAILED" -eq 0 ] && [ -f "$OUT_DIR/locust_stats_history.csv" ]; then
        "$PY" "$CODE_DIR/check_run.py" "$OUT_DIR" | while IFS= read -r l; do log "$l"; done
        local code=${PIPESTATUS[0]}
        [ "$code" -ne 0 ] && FAILED=1
        [ "$code" -eq 2 ] && QUOTA_BUG=1     # replicas above the scenario quota: controller bug, run_batch.sh stops
    fi
    if [ "$FAILED" -ne 0 ]; then
        local failed_dir; failed_dir="$(dirname "$OUT_DIR")/_failed_run${RUN}_$(date +%Y%m%d-%H%M)"
        mv "$OUT_DIR" "$failed_dir"
        log "RUN FAILED - data moved to $failed_dir (see controller.err.log). Rerun this run number."
        return
    fi
    log "Results saved to $OUT_DIR"
    [ -f "$OUT_DIR/locust_stats_history.csv" ] || return
    "$PY" "$CODE_DIR/make_run_report.py" "$OUT_DIR" || log "WARNING: make_run_report.py failed; data is saved, rerun it by hand"
    local scen_path; scen_path="$(dirname "$(dirname "$OUT_DIR")")"
    local compare_args=("$CODE_DIR/make_comparison.py" "$scen_path"); [ "$RUN" -eq 0 ] && compare_args+=("--include-trials")
    local sets=("")
    case "$AUTOSCALER" in
        smarthpa-prio) sets=("--c3" "--c3-control") ;;
        smarthpa-flat) sets=("--c3-control") ;;
        prosmarthpa-authors) sets=("--prophet-authors" "--prophet-sameday") ;;
        prosmarthpa-rerun) sets=("--prophet-sameday") ;;
        prosmarthpa-cv) sets=("--prophet-cv") ;;
    esac
    for s in "${sets[@]}"; do
        if [ -n "$s" ]; then "$PY" "${compare_args[@]}" "$s"; "$PY" "$CODE_DIR/make_user_metrics.py" "$scen_path" "$s"
        else "$PY" "${compare_args[@]}"; "$PY" "$CODE_DIR/make_user_metrics.py" "$scen_path"; fi
    done
}

on_signal() { log "Interrupted"; FAILED=1; cleanup_and_collect; exit 1; }
trap on_signal INT TERM

run() {
    # ------------------------------------------------------------ 2. Reset
    log "Reset: deleting HPAs, scaling all deployments to 1"
    kubectl delete hpa --all --ignore-not-found >/dev/null
    kubectl scale deployment --all --replicas=1 >/dev/null || { log "ERROR: kubectl scale failed"; return 1; }
    wait_clean || return 1
    # every run starts from fresh pods, the same for every autoscaler (19/11: in C4 run 1 a currencyservice pod kept
    # from earlier runs used 181% CPU vs 101% in every comparable run; replaces the 12/11 rule that only restarted
    # pods above 75% of their memory limit)
    log "Restarting every deployment (fresh pods)"
    local deps; deps=$(kubectl get deployment -o name) || { log "ERROR: kubectl get deployment failed"; return 1; }
    # shellcheck disable=SC2086
    kubectl rollout restart $deps >/dev/null || { log "ERROR: kubectl rollout restart failed"; return 1; }
    for d in $deps; do kubectl rollout status "$d" --timeout=600s >/dev/null 2>&1 || log "WARN: $d not rolled out after 600s"; done
    sleep 5
    wait_clean || return 1
    # 20/11 (E10): on fresh pods the cold JVM of adservice reaches 26-62% CPU at t = 25-55 s, so K8s HPA scales it to 2
    # pods and it stays there (2 x 11%), while warm pods stay at 1 pod (~15%), as adservice does in the paper's K8s HPA.
    # Light load with no autoscaler running (HPAs deleted above, every deployment at 1 replica), then the usual cooldown.
    if [ "$POD_WARMUP" -gt 0 ]; then
        log "Pod warm-up: $POD_WARMUP_USERS users for ${POD_WARMUP}s, no autoscaler running"
        # same spawn rate as the measured run (20/11: 50 users @ 5/s for 120 s was too light, adservice still jumped to
        # 37-46% when the measured load passed 150 users and K8s HPA scaled it to 2 pods)
        "$LOCUST" -f locustfile.py -u "$POD_WARMUP_USERS" -r "$SPAWN_RATE" --host "$TARGET_HOST" --headless -t "${POD_WARMUP}s" \
            --only-summary > "/tmp/pod_warmup_run${RUN}.log" 2>&1 || log "WARN: warm-up Locust exited non-zero (see /tmp/pod_warmup_run${RUN}.log)"
        wait_clean || return 1
    fi
    log "Cluster clean: $N_DEPLOYMENTS deployments x 1 fresh replica. Cooling down ${COOLDOWN}s"
    sleep "$COOLDOWN"

    # ------------------------------------------------------------ 3. Prepare outputs and autoscaler
    rm -rf "$OUT_DIR"; mkdir -p "$OUT_DIR"
    rm -rf "$CODE_DIR/Knowledge Base"; cp -r "$CODE_DIR/kb_template" "$CODE_DIR/Knowledge Base"
    export SMARTHPA_SCENARIO="$SCENARIO" SMARTHPA_DURATION="$DURATION" PROSMART_MODELS="$MODEL_SET" \
           PROSMART_WINDOW="$WINDOW" SMARTHPA_ARM="$ARM" PYTHONIOENCODING=utf-8 \
           SMARTHPA_KUBECTL_DELAY_SEC="$KUBECTL_DELAY" SMARTHPA_ARM_WARMUP_SEC="$ARM_WARMUP"
    local controller_script controller_py="$PY"
    if [ "$AUTOSCALER" = "k8shpa" ]; then
        local deps; deps=$(kubectl get deployments -o jsonpath='{.items[*].metadata.name}') || return 1
        for d in $deps; do
            # kubectl >= 1.33 uses --cpu=<N>% (without % the value is read as milliCPU)
            kubectl autoscale deployment "$d" "--cpu=${THRESHOLD}%" --min=1 "--max=$MAXR" >/dev/null || return 1
        done
        log "Created $(echo $deps | wc -w) Kubernetes HPAs (cpu=$THRESHOLD%, max=$MAXR)"
        controller_script="k8shpa_observer.py"
    elif [[ "$AUTOSCALER" == prosmarthpa* ]]; then
        controller_script="../prosmarthpa/prosmart_hpa.py"; controller_py="$PROSMART_PY"
    else
        controller_script="Microservice_Capacity_Analyzer.py"
    fi
    STARTED_AT="$(date '+%Y-%m-%d %H:%M:%S')"

    # ------------------------------------------------------------ 4. Start recorder, Locust and controller together
    log "Starting $controller_script, cluster_recorder.py and Locust"
    setsid "$PY" cluster_recorder.py "$REL_OUT/cluster_metrics.csv" $((DURATION + 30)) 15 2> "$OUT_DIR/recorder.err.log" &
    PIDS+=($!)
    local load_args=(-f locustfile.py -u "$USERS" -r "$SPAWN_RATE"); [ "$SHAPE" = "spike" ] && load_args=(-f locustfile_spike.py)
    setsid "$LOCUST" "${load_args[@]}" --host "$TARGET_HOST" --headless -t "${DURATION}s" --csv "$REL_OUT/locust" \
        --csv-full-history --only-summary > "$OUT_DIR/locust.out.log" 2> "$OUT_DIR/locust.err.log" &
    PIDS+=($!)
    setsid "$controller_py" "$controller_script" > "$OUT_DIR/controller.out.log" 2> "$OUT_DIR/controller.err.log" &
    local controller_pid=$!
    PIDS+=($controller_pid)

    local t0; t0=$(date +%s)
    while kill -0 "$controller_pid" 2>/dev/null; do
        sleep 30
        # progress display only: a blip here must not kill the run (the controller has its own kubectl retry)
        local replicas
        if ! replicas=$(kubectl get deployments --request-timeout=10s -o jsonpath='{range .items[*]}{.metadata.name}={.spec.replicas} {end}' 2>/dev/null); then
            MONITOR_ERRORS=$((MONITOR_ERRORS + 1)); replicas="WARNING: kubectl unreachable ($MONITOR_ERRORS so far)"
        fi
        log "$(printf '%4d' $(( $(date +%s) - t0 )))s | $replicas"
    done
    wait "$controller_pid"; CONTROLLER_EXIT=$?
    log "Controller exited with code $CONTROLLER_EXIT"
    [ "$MONITOR_ERRORS" -gt 0 ] && log "WARNING: kubectl was unreachable $MONITOR_ERRORS time(s) during the run"
    # recorder and Locust end on their own timers; give them up to 120 s
    local deadline=$(( $(date +%s) + 120 ))
    for pid in "${PIDS[@]}"; do
        while kill -0 "$pid" 2>/dev/null && [ "$(date +%s)" -lt "$deadline" ]; do sleep 2; done
    done
    FINISHED_AT="$(date '+%Y-%m-%d %H:%M:%S')"
    [ "$CONTROLLER_EXIT" -eq 0 ] || return 1
    return 0
}

run || FAILED=1
cleanup_and_collect
if [ "$FAILED" -ne 0 ]; then [ "$QUOTA_BUG" -eq 1 ] && exit 2; exit 1; fi
exit 0
