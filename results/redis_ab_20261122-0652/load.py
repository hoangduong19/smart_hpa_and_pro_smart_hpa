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
