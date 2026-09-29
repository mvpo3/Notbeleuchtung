from pathlib import Path
import json,math,re
import fitz,ezdxf,numpy as np,contourpy
from PIL import Image,ImageDraw
from scipy import ndimage
from shapely.geometry import Polygon,LineString,mapping,shape
from shapely.ops import unary_union,polygonize

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'_build';R.mkdir(parents=True,exist_ok=True)
L=json.loads((R/'lines.json').read_text());T=json.loads((R/'texts.json').read_text())
# Independently register the two X_Geometrie line segments of this floor.
cad=np.array([[27929.70331501603,30156.87762998333],[27929.70331501603,29998.71860863354],[-18046.51491702778,34055.98877577223],[-18325.7892035889,34055.98877577223]])
pdf=np.array([[4113.564453125,1214.234619140625],[4113.564453125,1223.1990966796875],[1507.6351318359375,993.233154296875],[1491.8057861328125,993.233154296875]])
A=[];b=[]
for (x,y),(u,v) in zip(cad,pdf):A.extend([[x,1,0],[-y,0,1]]);b.extend([u,v])
S,TX,TY=np.linalg.lstsq(A,b,rcond=None)[0]
(R/'registration.json').write_text(json.dumps({'s':S,'tx':TX,'ty':TY,'residual_pt':float(np.max(np.abs(np.array(A)@np.array([S,TX,TY])-b)))}))
def xy(x,y):return TX+x*S,TY-y*S
for t in T:t['u'],t['v']=xy(t['x'],t['y'])
(R/'texts_pdf.json').write_text(json.dumps(T,ensure_ascii=False))
print('REGISTRATION',S,TX,TY,flush=True)

# Closed visual wall envelopes from material marks. Door arcs are not input.
step=10.;xmin=-44500.;ymax=51500.;w=7600;h=5200
im=Image.new('1',(w,h));dr=ImageDraw.Draw(im);ids=[]
layers={r[4] for r in L if 'Wand' in r[4] or r[4]=='150 Stuetze'}
for x1,y1,x2,y2,layer,handle in L:
 if layer not in layers:continue
 dx,dy=x2-x1,y2-y1;le=math.hypot(dx,dy);angle=math.degrees(math.atan2(dy,dx))%180
 axis=min(abs(angle-v) for v in [0.004,90.004,179.999])<.08
 if .1<le<250 and not axis or ('Bekleidung' in layer or 'Vorsatzschale' in layer) and 10<le<220:
  dr.line(((x1-xmin)/step,(ymax-y1)/step,(x2-xmin)/step,(ymax-y2)/step),fill=1);ids.append(handle)
d=ezdxf.readfile(str(ROOT/'quellen/20220225-SH22-LKS-GE-AP-02-01-A-2OG.dxf'));m=d.modelspace();thin=[];furn=[]
for e in m:
 if e.dxftype()=='ELLIPSE' and e.dxf.layer in layers and e.dxf.major_axis.magnitude<250:
  pts=[((p.x-xmin)/step,(ymax-p.y)/step) for p in e.flattening(5)]
  if len(pts)>1:dr.line(pts,fill=1);ids.append(e.dxf.handle)
 if e.dxftype()=='SOLID' and e.dxf.layer in ['129 Wand Innen Trennwand WC']:
  pts=[xy(p.x,p.y) for p in e.vertices()];g=Polygon(pts)
  if g.is_valid and g.area>0:thin.append(g)
 if e.dxf.layer in ['510 Moeblierung','511 Moeblierung eingebaut','540 Sanitaereinrichtung','530 Kueche','516 Pflanztröge'] and e.dxftype() in ['LINE','ELLIPSE','CIRCLE']:
  from ezdxf.path import make_path
  pts=[xy(p.x,p.y) for p in make_path(e).flattening(2)]
  if len(pts)>1:furn.append(LineString([(round(x,1),round(y,1)) for x,y in pts]))
mask=ndimage.binary_closing(ndimage.binary_dilation(np.asarray(im,dtype=bool),iterations=3),iterations=4)
labels,n=ndimage.label(mask);sizes=np.bincount(labels.ravel());good=sizes>40;good[0]=False;mask=good[labels]
gen=contourpy.contour_generator(z=mask.astype(np.uint8),fill_type='OuterOffset');points,offsets=gen.filled(.5,1.5)
polys=[]
for pts,off in zip(points,offsets):
 rings=[[xy(xmin+x*step,ymax-y*step) for x,y in pts[a:b]] for a,b in zip(off[:-1],off[1:])]
 g=Polygon(rings[0],rings[1:]).simplify(.7,preserve_topology=True).buffer(0)
 if g.area>13:polys.append(g)
walls=unary_union(polys+thin)
(R/'walls.geojson').write_text(json.dumps(mapping(walls)))
(R/'wall_provenance.json').write_text(json.dumps({'step_mm':step,'handles':ids,'thin_solids':len(thin),'method':'Materialdarstellung mit geschlossenem Erklärumriss; keine exakte Bauteilgeometrie'}))
fg=unary_union([p for p in polygonize(unary_union(furn)) if 15<p.area<65000])
(R/'furniture.geojson').write_text(json.dumps(mapping(fg)))
print('WALLS',len(polys),'THIN',len(thin),'FURNITURE',len(fg.geoms) if hasattr(fg,'geoms') else 1,flush=True)
p=fitz.open(R/'clean.pdf');pg=p[0];sh=pg.new_shape()
for g in walls.geoms if hasattr(walls,'geoms') else [walls]:
 for ring in [g.exterior,*g.interiors]:sh.draw_polyline(list(ring.coords))
sh.finish(color=(.82,.035,.10),fill=(1,.03,.07),width=1.1,fill_opacity=.17,even_odd=True);sh.commit()
p.save(R/'walls.pdf',garbage=4,deflate=True)
pg.get_pixmap(matrix=fitz.Matrix(.45,.45)).save(R/'walls.png')
print('DONE',flush=True)
