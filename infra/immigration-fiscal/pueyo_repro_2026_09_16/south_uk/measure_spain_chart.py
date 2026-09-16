from PIL import Image
import sys
p="/Users/alien/Projects/immigration-research/infra/immigration-fiscal/pueyo_repro_2026_09_16/source_thread/charts/2099900531606986915_0.jpg"
im=Image.open(p).convert("RGB"); W,H=im.size
print("size",W,H)
px=im.load()
# find bar rows: scan for rows with many non-white pixels in left panel region
def rowprofile(x0,x1):
    rows=[]
    for y in range(H):
        n=sum(1 for x in range(x0,x1,2) if sum(px[x,y])<720)
        rows.append(n)
    return rows
# detect distinct bar bands in right panel (x 740..1500)
rp=rowprofile(750,1500)
bands=[];iny=False
for y,n in enumerate(rp):
    if n>3 and not iny: iny=True; s=y
    elif n<=3 and iny: iny=False; bands.append((s,y-1))
print("right bands",[b for b in bands if b[1]-b[0]>5])
