import sys
def load(f):
    v=[];F=[]
    for l in open(f):
        p=l.split()
        if not p: continue
        if p[0]=='v': v.append(list(map(float,p[1:4])))
        if p[0]=='f': F.append([int(q.split('/')[0])-1 for q in p[1:]])
    return v,F
sub=lambda a,b:[a[i]-b[i] for i in range(3)]
cross=lambda a,b:[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
dot=lambda a,b:sum(a[i]*b[i] for i in range(3))
for f in sys.argv[1:]:
    v,F=load(f); tris=F[:12] if 'toggle' in f else F
    pts=[v[i] for t in tris for i in t]; c=[sum(p[i] for p in pts)/len(pts) for i in range(3)]
    out=inn=0
    for t in tris:
        a,b,cc=v[t[0]],v[t[1]],v[t[2]]
        n=cross(sub(b,a),sub(cc,a)); m=[(a[i]+b[i]+cc[i])/3 for i in range(3)]
        if dot(n,sub(m,c))>0: out+=1
        else: inn+=1
    print(f.split('/')[-1],'outward',out,'inward',inn)
