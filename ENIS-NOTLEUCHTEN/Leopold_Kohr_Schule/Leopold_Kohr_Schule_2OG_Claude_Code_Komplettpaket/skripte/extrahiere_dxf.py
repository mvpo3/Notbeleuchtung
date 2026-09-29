"""Reproduce the preparation inputs from the original 2OG DXF/PDF."""
from pathlib import Path
import json,ezdxf,shutil
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'_build';R.mkdir(parents=True,exist_ok=True)
d=ezdxf.readfile(str(ROOT/'quellen/20220225-SH22-LKS-GE-AP-02-01-A-2OG.dxf'))
texts=[];lines=[];arcs=[]
for e in d.modelspace():
 t=e.dxftype()
 if t in ['TEXT','MTEXT']:
  p=e.dxf.insert;texts.append({'text':e.plain_text() if t=='MTEXT' else e.dxf.text,'x':p.x,'y':p.y,'layer':e.dxf.layer,'handle':e.dxf.handle,'height':e.dxf.char_height if t=='MTEXT' else e.dxf.height})
 elif t=='LINE':
  a,b=e.dxf.start,e.dxf.end;lines.append([a.x,a.y,b.x,b.y,e.dxf.layer,e.dxf.handle])
 elif t=='ELLIPSE':
  c=e.dxf.center;a=e.dxf.major_axis;arcs.append({'c':[c.x,c.y],'major':[a.x,a.y],'ratio':e.dxf.ratio,'start':e.dxf.start_param,'end':e.dxf.end_param,'layer':e.dxf.layer,'handle':e.dxf.handle})
for name,data in [('texts',texts),('lines',lines),('arcs',arcs)]:
 (R/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
# Only used for the temporary preview in prepare.py; build.py creates its own
# original vector architecture view with selected overlay layers removed.
shutil.copyfile(str(ROOT/'quellen/Schule_SH22_2_OG.pdf'),R/'clean.pdf')
print('DXF inputs extracted.')
