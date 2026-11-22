#!/usr/bin/env bash
# L11 / E16: does the lab's redis-cart image (redis:alpine unpinned = Redis 8.10.2 with 4 bundled modules loaded by the
# entrypoint) use more CPU per cart operation than the image the Smart HPA package pins (redis:alpine@sha256:121bac94 =
# Redis 7.0.11, no modules)?
# Three standalone Redis pods on ONE node, same manifest as redis-cart (requests 70m, limits 125m, emptyDir /data):
#   r7     = 7.0.11 (Smart HPA helm chart digest), command redis-server directly: the 7.0.11 entrypoint only chowns /data
#            and drops to the redis user (no modules), and its chown fails under capabilities: drop ALL (22/11: exit 1)
#   r8     = 8.10.2 (digest running in the lab), default entrypoint -> loads rejson, redisearch, redistimeseries, redisbloom
#   r8nomod= 8.10.2, command redis-server directly (entrypoint bypassed -> no modules): separates "modules" from "version"
# One client pod (emailservice:v0.8.0 image, already on the nodes, has python) keeps ONE persistent connection per target,
# like cartservice (StackExchange.Redis multiplexer), and sends the cartservice command mix at a fixed rate:
#   GetCart  -> HMGET <user> absexp sldexp data
#   SetCart  -> EVALSHA of the Microsoft.Extensions.Caching.StackExchangeRedis 7.0.8 SetScript (HSET + EXPIRE)
# CPU is read from the container cgroup (cpu.stat usage_usec, exact) and from metrics-server (what the HPA sees).
# Does not touch the app's redis-cart. Run only when no experiment is running (cluster otherwise idle).
# Usage (on exp-runner): ~/redis_ab.sh [RATE_OPS_PER_S=115] [SET_SHARE=0.15] [MEASURE_S=300] [NODE=k3s-worker1]
set -u
export PATH=$HOME/bin:$PATH
RATE=${1:-115}; SET_SHARE=${2:-0.15}; MEASURE=${3:-300}; NODE=${4:-k3s-worker1}
OUT=~/Demo/results/redis_ab_$(date +%Y%m%d-%H%M); mkdir -p "$OUT"
R7=redis@sha256:121bac949fb5f623b9fa0b4e4c9fb358ffd045966e754cfa3eb9963f3af2fe3b
R8=redis@sha256:3811787313eba226a2ef38658c6ccb91cd5e110edc89c37767de373120a0e5a0
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$OUT/log.txt"; }
if tmux ls 2>/dev/null | grep -qE "v080w5b|prosmart|qpro"; then log "an experiment tmux session is running, abort"; exit 1; fi

log "redis-cart command mix since its pod start (for checking SET_SHARE):"
P=$(kubectl get pods -l app=redis-cart -o name | head -1)
kubectl exec "$P" -- redis-cli info commandstats > "$OUT/redis-cart_commandstats.txt" 2>&1; cat "$OUT/redis-cart_commandstats.txt" | tee -a "$OUT/log.txt"
kubectl exec "$P" -- redis-cli info server | grep -E "redis_version|uptime_in_seconds" | tee -a "$OUT/log.txt"
kubectl exec "$P" -- redis-cli module list | tee -a "$OUT/log.txt"

redis_pod() {  # name image command-override(yes/no)
  local cmd=""; [ "$3" = yes ] && cmd='    command: ["redis-server"]'
  cat <<EOF
apiVersion: v1
kind: Pod
metadata: {name: $1, labels: {app: redis-ab, ab: $1}}
spec:
  nodeName: $NODE
  containers:
  - name: redis
    image: $2
$cmd
    securityContext: {allowPrivilegeEscalation: false, capabilities: {drop: [ALL]}, privileged: false, readOnlyRootFilesystem: true}
    ports: [{containerPort: 6379}]
    volumeMounts: [{mountPath: /data, name: redis-data}]
    resources: {limits: {memory: 256Mi, cpu: 125m}, requests: {cpu: 70m, memory: 200Mi}}
  volumes: [{name: redis-data, emptyDir: {}}]
EOF
}
{ redis_pod r7 $R7 yes; echo ---; redis_pod r8 $R8 no; echo ---; redis_pod r8nomod $R8 yes; } > "$OUT/pods.yaml"
kubectl apply -f "$OUT/pods.yaml" | tee -a "$OUT/log.txt"
kubectl wait --for=condition=Ready pod/r7 pod/r8 pod/r8nomod --timeout=300s | tee -a "$OUT/log.txt" || exit 1
for p in r7 r8 r8nomod; do
  echo "$p: $(kubectl exec $p -- redis-cli info server | grep redis_version | tr -d '\r') modules: $(kubectl exec $p -- redis-cli module list | grep -c '^name' )" | tee -a "$OUT/log.txt"
done
IPS=$(for p in r7 r8 r8nomod; do echo -n "$p=$(kubectl get pod $p -o jsonpath='{.status.podIP}'),"; done)

cpu_usec() { kubectl exec "$1" -- cat /sys/fs/cgroup/cpu.stat | awk '/^usage_usec/{print $2}'; }
measure() {  # label seconds -> mean millicores per pod from cgroup + metrics-server samples
  local t0 a7 a8 an; t0=$(date +%s.%N); a7=$(cpu_usec r7); a8=$(cpu_usec r8); an=$(cpu_usec r8nomod)
  local end=$(( $(date +%s) + $2 ))
  while [ "$(date +%s)" -lt $end ]; do kubectl top pod r7 r8 r8nomod --no-headers 2>/dev/null | sed "s/^/$1 $(date +%s) /" >> "$OUT/top.txt"; sleep 15; done
  local t1 b7 b8 bn; t1=$(date +%s.%N); b7=$(cpu_usec r7); b8=$(cpu_usec r8); bn=$(cpu_usec r8nomod)
  awk -v l="$1" -v dt="$(awk -v a="$t0" -v b="$t1" 'BEGIN{print b-a}')" -v a="$a7 $a8 $an" -v b="$b7 $b8 $bn" 'BEGIN{split(a,x," ");split(b,y," ");
    printf "%s cgroup mean CPU (m): r7 %.2f  r8 %.2f  r8nomod %.2f  (%.0f s)\n", l, (y[1]-x[1])/dt/1000, (y[2]-x[2])/dt/1000, (y[3]-x[3])/dt/1000, dt}' | tee -a "$OUT/log.txt"
}
log "idle baseline"; sleep 30; measure idle 120

cat > "$OUT/load.py" <<'EOF'
import os, socket, time, random, hashlib, sys
SCRIPT = ("redis.call('HSET', KEYS[1], 'absexp', ARGV[1], 'sldexp', ARGV[2], 'data', ARGV[4])\n"
          "if ARGV[3] ~= '-1' then\n  redis.call('EXPIRE', KEYS[1], ARGV[3])\nend\nreturn 1")
SHA = hashlib.sha1(SCRIPT.encode()).hexdigest()
def cmd(*a):
    a = [x if isinstance(x, bytes) else str(x).encode() for x in a]
    return b"*%d\r\n" % len(a) + b"".join(b"$%d\r\n%s\r\n" % (len(x), x) for x in a)
def reply(f):
    line = f.readline()
    t, rest = line[:1], line[1:-2]
    if t == b"$":
        n = int(rest); return None if n < 0 else f.read(n + 2)[:-2]
    if t == b"*":
        n = int(rest); return [reply(f) for _ in range(max(n, 0))]
    if t == b"-": raise RuntimeError(rest)
    return rest
targets = []
for kv in os.environ["TARGETS"].strip(",").split(","):
    name, ip = kv.split("=")
    s = socket.create_connection((ip, 6379)); s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    f = s.makefile("rb"); s.sendall(cmd("SCRIPT", "LOAD", SCRIPT)); reply(f); targets.append((name, s, f))
rate, share, dur = float(os.environ["RATE"]), float(os.environ["SET_SHARE"]), float(os.environ["DURATION"])
users = ["%08x-%04x" % (random.getrandbits(32), i) for i in range(2000)]
cart = os.urandom(60)                                         # serialized Hipstershop.Cart of a few items ~ 40-80 B
t0 = time.monotonic(); n = 0; last = t0
while time.monotonic() - t0 < dur:
    u = random.choice(users); setop = random.random() < share
    for name, s, f in targets:
        s.sendall(cmd("EVALSHA", SHA, 1, u, -1, -1, -1, cart) if setop else cmd("HMGET", u, "absexp", "sldexp", "data"))
        reply(f)
    n += 1
    nxt = t0 + n / rate; d = nxt - time.monotonic()
    if d > 0: time.sleep(d)
    if time.monotonic() - last > 30: last = time.monotonic(); print(f"{n / (last - t0):.1f} ops/s per target", flush=True)
print(f"done {n} ops per target, {n / (time.monotonic() - t0):.1f} ops/s", flush=True)
EOF
kubectl create configmap redis-ab-load --from-file=load.py="$OUT/load.py" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
DUR=$((MEASURE + 90))
cat <<EOF | kubectl apply -f - | tee -a "$OUT/log.txt"
apiVersion: v1
kind: Pod
metadata: {name: redis-ab-client, labels: {app: redis-ab}}
spec:
  restartPolicy: Never
  nodeName: k3s-master
  containers:
  - name: load
    image: gcr.io/google-samples/microservices-demo/emailservice:v0.8.0
    command: ["python", "-u", "/load/load.py"]
    env: [{name: TARGETS, value: "$IPS"}, {name: RATE, value: "$RATE"}, {name: SET_SHARE, value: "$SET_SHARE"}, {name: DURATION, value: "$DUR"}]
    volumeMounts: [{mountPath: /load, name: load}]
  volumes: [{name: load, configMap: {name: redis-ab-load}}]
EOF
kubectl wait --for=condition=Ready pod/redis-ab-client --timeout=300s >/dev/null || { kubectl logs redis-ab-client | tee -a "$OUT/log.txt"; exit 1; }
log "load $RATE ops/s per target, SET share $SET_SHARE, warm 60 s then measure $MEASURE s"; sleep 60
measure load "$MEASURE"
kubectl logs redis-ab-client | tee -a "$OUT/log.txt"
for p in r7 r8 r8nomod; do echo "$p $(kubectl exec $p -- redis-cli info commandstats | grep -E 'cmdstat_(hmget|evalsha|hset|expire):' | tr -d '\r' | tr '\n' ' ')" | tee -a "$OUT/log.txt"; done
kubectl delete pod r7 r8 r8nomod redis-ab-client --wait=false >/dev/null; kubectl delete configmap redis-ab-load >/dev/null
log "results in $OUT (log.txt: cgroup means; top.txt: metrics-server samples)"
