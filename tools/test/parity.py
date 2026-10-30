# Every face of an exported OBJ faces out? A ray from just in front of each
# face (along its normal) must go through the model an even number of times.
# (Overlapping solids confuse it: test one solid, or one prefab, at a time.)
#   python3 tools/test/parity.py X.obj
import sys, random, math
v=[];F=[]
for l in open(sys.argv[1]):
    p=l.split()
    if not p: continue
    if p[0]=='v': v.append(tuple(map(float,p[1:4])))
    if p[0]=='f': F.append([int(q.split('/')[0])-1 for q in p[1:]])
sub=lambda a,b:(a[0]-b[0],a[1]-b[1],a[2]-b[2])
cr=lambda a,b:(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
dt=lambda a,b:a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
tri=[(v[f[0]],v[f[1]],v[f[2]]) for f in F]
pre=[(a,sub(b,a),sub(c,a)) for a,b,c in tri]
def hits(o,d):
    n=0
    for a,e1,e2 in pre:
        p=cr(d,e2);det=dt(e1,p)
        if abs(det)<1e-12: continue
        s=sub(o,a);u=dt(s,p)/det
        if u<0 or u>1: continue
        q=cr(s,e1);w=dt(d,q)/det
        if w<0 or u+w>1: continue
        if dt(e2,q)/det>1e-6: n+=1
    return n
random.seed(1);bad=0
for a,e1,e2 in pre:
    nn=cr(e1,e2);l=math.sqrt(dt(nn,nn));nn=(nn[0]/l,nn[1]/l,nn[2]/l)
    m=tuple(a[i]+(e1[i]+e2[i])/3 for i in range(3)); o=tuple(m[i]+nn[i]*1e-4 for i in range(3))
    d=tuple(nn[i]+random.gauss(0,.05) for i in range(3))
    if hits(o,d)%2: bad+=1
print(sys.argv[1].split('/')[-1],"tris",len(tri),"facing wrong (odd crossings):",bad)
