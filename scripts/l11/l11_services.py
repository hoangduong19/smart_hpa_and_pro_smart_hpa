import glob, os, statistics, sys
from openpyxl import load_workbook
REQ={"adservice":200,"cartservice":200,"redis-cart":70}
for pat in sys.argv[1:]:
  for run in sorted(glob.glob(pat)):
    out=[]
    for svc in ["redis-cart","emailservice","cartservice"]:
        f=os.path.join(run,"knowledge_base",svc+".xlsx")
        if not os.path.exists(f): continue
        rows=[r for r in list(load_workbook(f,read_only=True).active.iter_rows(values_only=True))[1:] if r[0] is not None and r[4] is not None]
        req=REQ.get(svc,100)
        sup=statistics.mean(r[2]*req for r in rows)
        cpu=statistics.mean(r[1] for r in rows)
        usage=statistics.mean(r[1]*r[2]*req/100 for r in rows)  # mean used millicores
        first2=next((round(r[0]) for r in rows if r[2]>=2),None)
        late=[r for r in rows if r[0]>300]
        late_use=statistics.mean(r[1]*r[2]*req/100 for r in late)
        out.append(f"{svc[:6]} sup {sup:5.0f} cpu% {cpu:5.1f} use {usage:4.1f}m late {late_use:4.1f}m 2pod@{first2}")
    print(run, " | ".join(out))
