import csv,collections,glob,statistics,sys
for pat in sys.argv[1:]:
  for run in sorted(glob.glob(pat)):
    try: rows=list(csv.DictReader(open(run+"/pod_metrics.csv")))
    except FileNotFoundError: continue
    def summ(app):
        pods=collections.OrderedDict()
        for r in rows:
            if r["app"]==app: pods.setdefault(r["pod"],[]).append(r)
        s=[]
        for p,rs in pods.items():
            late=[int(r["cpu_m"]) for r in rs if float(r["elapsed_sec"])>150]
            s.append(f'{rs[0]["node"][-7:]}:{statistics.mean(late) if late else 0:.0f}m(from {float(rs[0]["elapsed_sec"]):.0f}s)')
        return " ".join(s)
    print(f"{run:34s} redis[{summ('redis-cart')}]  email[{summ('emailservice')}]  cart[{summ('cartservice')}]")
