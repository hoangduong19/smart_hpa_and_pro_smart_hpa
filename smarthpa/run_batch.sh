#!/usr/bin/env bash
# Linux port of run_batch.ps1 for the exp-runner VM. Runs <scenario>:<run> pairs back to back with run_experiment.sh,
# each autoscaler in the given order; skips runs whose results folder exists; retries a failed run up to --max-attempts
# times after the cluster answers again; stops at once on exit code 2 (replicas above quota = controller bug).
# Also logs a ping per second to the 3 nodes (results/ping_<date>.csv, same columns as the Windows runs).
#
# Run it inside tmux so it survives a lost SSH session:
#   tmux new -s batch './run_batch.sh --pairs 2R-20%:1 --autoscalers k8shpa,smarthpa --spawn-rate 2 --tag pilot2s'
set -uo pipefail

PAIRS=""; AUTOSCALERS="k8shpa,smarthpa"; MAX_ATTEMPTS=3; SHAPE="ramp"; TAG=""; EXTRA=()
while [ $# -gt 0 ]; do
    case "$1" in
        --pairs) PAIRS="$2"; shift 2 ;;
        --autoscalers) AUTOSCALERS="$2"; shift 2 ;;
        --max-attempts) MAX_ATTEMPTS="$2"; shift 2 ;;
        --shape) SHAPE="$2"; EXTRA+=(--shape "$2"); shift 2 ;;
        --tag) TAG="$2"; EXTRA+=(--tag "$2"); shift 2 ;;
        --spawn-rate|--users|--duration|--cooldown|--kubectl-delay|--arm-warmup|--pod-warmup|--pod-warmup-users) EXTRA+=("$1" "$2"); shift 2 ;;
        *) echo "Unknown argument $1" >&2; exit 1 ;;
    esac
done
[ -n "$PAIRS" ] || { echo "--pairs required, e.g. 2R-20%:1,2R-20%:2" >&2; exit 1; }

CODE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS="$CODE_DIR/../results"
export PATH="$HOME/bin:$PATH"
log() { echo "[$(date +%H:%M:%S)] [batch] $*"; }

PING_CSV="$RESULTS/ping_$(date +%Y%m%d-%H%M).csv"
mkdir -p "$RESULTS"
echo "time,ip,ok,ms" > "$PING_CSV"
( while true; do
    for ip in 192.168.161.10 192.168.161.11 192.168.161.12; do
        out=$(ping -c 1 -W 1 "$ip" 2>/dev/null | sed -n 's/.*time=\([0-9.]*\).*/\1/p')
        if [ -n "$out" ]; then echo "$(date +%Y-%m-%dT%H:%M:%S),$ip,True,${out%.*}"; else echo "$(date +%Y-%m-%dT%H:%M:%S),$ip,False,"; fi
    done >> "$PING_CSV"
    sleep 1
  done ) &
PING_PID=$!
trap 'kill $PING_PID 2>/dev/null' EXIT

wait_cluster() {   # 3 successful kubectl calls in a row, give up after 30 min
    local ok=0 since; since=$(date +%s)
    while [ $ok -lt 3 ]; do
        if kubectl get nodes --request-timeout=5s >/dev/null 2>&1; then ok=$((ok + 1)); else ok=0; fi
        [ $ok -lt 3 ] && sleep 10
        if [ $(( $(date +%s) - since )) -gt 1800 ]; then log "Cluster unreachable for 30 min, stopping batch"; exit 1; fi
    done
}

suffix=""; [ "$SHAPE" != "ramp" ] && suffix+="-$SHAPE"; [ -n "$TAG" ] && suffix+="-$TAG"
log "Pairs: $PAIRS | autoscalers: $AUTOSCALERS | options: ${EXTRA[*]:-none} | ping log $(basename "$PING_CSV")"
IFS=',' read -ra pair_list <<< "$PAIRS"
IFS=',' read -ra as_list <<< "$AUTOSCALERS"
for p in "${pair_list[@]}"; do
    scenario="${p%%:*}"; run="${p##*:}"
    for a in "${as_list[@]}"; do
        out_dir="$RESULTS/${scenario%\%}$suffix/$a/run$run"
        if [ -d "$out_dir" ]; then log "=== $a | $scenario | run $run already done, skipping ==="; continue; fi
        for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
            wait_cluster
            log "=== $a | $scenario | run $run | attempt $attempt/$MAX_ATTEMPTS ==="
            "$CODE_DIR/run_experiment.sh" --autoscaler "$a" --scenario "$scenario" --run "$run" "${EXTRA[@]}"
            code=$?
            [ $code -eq 0 ] && break
            log "Run failed (exit $code)"
            if [ $code -eq 2 ]; then log "Replicas above the quota (check_run.py): controller bug, stopping batch"; exit 2; fi
            if [ "$attempt" -eq "$MAX_ATTEMPTS" ]; then log "All $MAX_ATTEMPTS attempts failed, stopping batch"; exit 1; fi
        done
    done
done
log "Batch finished"
