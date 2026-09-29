from pathlib import Path
import json,math,re,hashlib
import fitz
from shapely.geometry import shape,mapping,box,Polygon,LineString,Point
from shapely.ops import unary_union
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from lessons import L

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'_build'; R.mkdir(parents=True,exist_ok=True)
O=ROOT/'reproduziert';O.mkdir(parents=True,exist_ok=True)
FONT=ROOT/'skripte/fonts/DejaVuSans.ttf';BOLD=FONT.with_name('DejaVuSans-Bold.ttf')
C={'red':(.82,.045,.13),'blue':(.025,.34,.72),'orange':(.78,.36,.02),'purple':(.46,.19,.64),'green':(.02,.48,.27),'ink':(.08,.17,.22)}
def setup(p):p.insert_font(fontname='dv',fontfile=str(FONT));p.insert_font(fontname='dvb',fontfile=str(BOLD))
def txt(p,pt,s,size=19,color='ink',bold=False):p.insert_text(pt,s,fontsize=size,fontname='dvb' if bold else 'dv',color=C.get(color,color))
def tb(p,rect,s,size=18,color='ink',bold=False):
 font=fitz.Font(fontfile=str(BOLD if bold else FONT))
 longest=max(font.text_length(word,fontsize=size) for word in s.split())
 size=min(size,size*(rect[2]-rect[0]-2)/max(longest,1))
 z=p.insert_textbox(fitz.Rect(rect),s,fontsize=size,fontname='dvb' if bold else 'dv',color=C.get(color,color),lineheight=1.2)
 if z<0:raise ValueError((s,z,rect))
def drawgeom(p,g,fill=None,color=None,width=1,alpha=1):
 if g.is_empty:return
 sh=p.new_shape()
 for q in g.geoms if hasattr(g,'geoms') else [g]:
  if q.geom_type!='Polygon':continue
  for ring in [q.exterior,*q.interiors]:sh.draw_polyline(list(ring.coords))
 sh.finish(fill=fill,color=color,width=width,fill_opacity=alpha,even_odd=True);sh.commit()
def arrow(p,a,b,col,width=2):
 p.draw_line(a,b,color=C[col],width=width);dx,dy=b[0]-a[0],b[1]-a[1];le=max(1,math.hypot(dx,dy));ux,uy=dx/le,dy/le
 pts=[b,(b[0]-ux*10-uy*4.5,b[1]-uy*10+ux*4.5),(b[0]-ux*10+uy*4.5,b[1]-uy*10-ux*4.5),b]
 s=p.new_shape();s.draw_polyline(pts);s.finish(fill=C[col],color=C[col]);s.commit()

# Keep original vectors; remove electrical overlays and the old revision cloud.
clean=fitz.open(str(ROOT/'quellen/Schule_SH22_2_OG.pdf'));pg=clean[0]
res=clean.xref_object(int(clean.xref_get_key(pg.xref,'Resources')[1].split()[0]));refs={k:int(v) for k,v in re.findall(r'/(MC\d+)\s+(\d+)\s+0\s+R',res)};ocg=clean.get_ocgs()
hide={k for k,v in refs.items() if ocg[v]['name'].startswith('e_') or ocg[v]['name']=='x_aenderungen'}
for xref in pg.get_contents():
 keep=[]
 for b in re.split(b'(?=\nq\n)',clean.xref_stream(xref)):
  tag=re.search(rb'/OC /(MC\d+) BDC',b)
  if tag and tag[1].decode() in hide:continue
  keep.append(b.replace(b'.5019608 .5019608 .5019608',b'.25 .25 .25'))
 clean.update_stream(xref,b''.join(keep))
clean.save(R/'architecture.pdf',garbage=4,deflate=True);clean.close();clean=fitz.open(R/'architecture.pdf')
wg=shape(json.loads((R/'walls.geojson').read_text()));fg=shape(json.loads((R/'furniture.geojson').read_text()))
reg=json.loads((R/'registration.json').read_text());S,TX,TY=reg['s'],reg['tx'],reg['ty']
def xy(x,y):return TX+x*S,TY-y*S
lines=json.loads((R/'lines.json').read_text());arcdata={a['handle']:a for a in json.loads((R/'arcs.json').read_text())}
def arcpts(h):
 a=arcdata[h];cx,cy=a['c'];mx,my=a['major'];ratio=a['ratio'];n=max(20,int((a['end']-a['start'])*40))
 return [xy(cx+mx*math.cos(t)-my*ratio*math.sin(t),cy+my*math.cos(t)+mx*ratio*math.sin(t)) for t in [a['start']+(a['end']-a['start'])*i/n for i in range(n+1)]]

# Supplement the narrow fixed partitions with their two original boundary lines.
thin=[]
for a,b,c,d,layer,h in lines:
 if layer=='129 Wand Innen Trennwand WC' and math.hypot(c-a,d-b)>900:
  # Only the paired, vertical fixed cabin boundaries; swinging leaves are shorter.
  u,v=xy(a,b);x,y=xy(c,d)
  if abs(x-u)<.1 and (abs(u-1276.4)<2 or abs(u-1325.7)<2 or abs(u-1375.1)<2 or abs(u-1226.9)<2) and 655<min(v,y)<660:
   thin.append(LineString([(u,v),(x,y)]).buffer(.65,cap_style=2))
wg=unary_union([wg,*thin]);(R/'walls_final.geojson').write_text(json.dumps(mapping(wg)))
wall=fitz.open();p=wall.new_page(width=4268,height=2953);p.show_pdf_page(p.rect,clean,0)
drawgeom(p,wg,fill=(1,.03,.07),color=C['red'],width=1.25,alpha=.17)
wall.save(R/'walls_final.pdf',garbage=4,deflate=True)

floorparts=[
 ('Innen West oben',box(77,82,1537,505)),('Innen West Mitte',box(77,505,1544,1469)),
 ('Innen West unten',box(77,1469,510,1820)),('Stiege 2 unteres Podest',box(1123,1469,1544,1593)),
 ('Mitte oben',box(1560,608,2691,1030)),('Mitte Umgang',box(1558,1030,2690,1590)),
 ('Mitte Klassen',box(1702,1624,2285,2012)),('Ost oben und Mitte',box(2715,609,4185,2086)),
 ('Ost Klasse Süd',box(3755,2086,4185,2256)),('Ost Erschließung Süd',box(3150,2086,3735,2112)),
 ('Ost Klasse 2.11',box(2717,2020,3130,2527)),
 ('Außen West',Polygon([(77,1838),(515,1838),(515,1491),(1095,1491),(1095,1610),(1545,1610),(1545,1950),(77,1950)])),
 ('Außen Podest Stiege 4',box(1545,1610,1690,1760)),
 ('Außen Mitte links',box(1518,1760,1690,2320)),('Außen Mitte unten',box(1690,2040,2550,2320)),
 ('Außen Mitte rechts',box(2308,1614,2692,2040)),('Außen Ost Streifen',box(2550,2040,2692,2880)),
 ('Außen Ost unten',box(2692,2550,4185,2880)),('Außen Ost Freiklasse',box(3170,2130,3730,2550)),
 ('Außen Ost Rand',box(3730,2280,4185,2550)),
 # Only explicitly located door passages join adjoining regions.
 ('Tür Mitte West',box(1530,1040,1570,1130)),('Tür Mitte Ost',box(2680,1265,2730,1342)),
 ('Tür Klasse Mitte',box(1750,1580,1830,1640)),('Tür Klasse Südost',box(3040,2000,3120,2040)),
]
excluded=[
 ('Umwehrter Bereich Mitte mit Brücke',box(1732,1144,2538,1477)),
 ('Umwehrter Bereich West außen',box(750,1603,978,1825)),
 ('Umwehrter Bereich Mitte außen',box(2295,1614,2545,2029)),
 ('Umwehrter Bereich Ost außen',box(3300,2420,3635,2700)),
 ('Wartungssteg West Kern',box(657,788,977,903)),
 ('Wartungssteg West Nord',Polygon([(1437,612),(1540,612),(1540,872),(1437,872)])),
 ('Wartungssteg Ost Kern',box(3306,1345,3620,1434)),
 ('Wartungssteg Ost Süd',box(2965,1805,3130,2002)),
 ('Technische Fortsetzung Ost',box(3048,1650,3130,1805)),
 ('Aufzug West',box(1220,1247,1309,1393)),('Aufzug Ost',box(2960,1660,3048,1806)),
 ('Technischer Bereich West',box(1257,1400,1307,1570)),
]
barriersegs=[]
for a,b,c,d,layer,h in lines:
 if layer in ['160 Fassade Pfosten-Riegel vorgehaengt','440 Gelaender','140 Bruestung'] and math.hypot(c-a,d-b)>80:
  barriersegs.append(LineString([xy(a,b),xy(c,d)]).buffer(.8,cap_style=2))
barriers=unary_union(barriersegs+[box(538,1482,1104,1497),box(1558,1018,1770,1037),box(1878,1018,2350,1037),box(2440,1018,2692,1037)])
obstacles=unary_union([wg,fg,barriers,*[g for n,g in excluded]])
floor=unary_union([g for n,g in floorparts]).difference(obstacles).buffer(0)
(R/'floor.geojson').write_text(json.dumps({'type':'Feature','properties':{'floor':'2OG','meaning':'Lerninterpretation von Bodenbereichen, keine vermessene Körperfreiraummaske'},'geometry':mapping(floor)}))
(R/'floor_provenance.json').write_text(json.dumps({'regions':[{'name':n,'geometry':mapping(g)} for n,g in floorparts],'excluded':[{'name':n,'geometry':mapping(g)} for n,g in excluded]},ensure_ascii=False))
walk=fitz.open();p=walk.new_page(width=4268,height=2953);p.show_pdf_page(p.rect,clean,0)
drawgeom(p,floor,fill=(.30,.86,.47),alpha=.36,width=0)
circulation=unary_union([box(512,500,634,1457),box(982,505,1107,1457),box(638,513,979,630),box(638,1268,1105,1457),box(1560,1036,2690,1138),box(1560,1140,1725,1590),box(2547,1140,2690,1590),box(1730,1480,2545,1590),box(3160,1040,3290,2108),box(3630,1040,3734,2108),box(3290,1050,3630,1150),box(3290,1785,3630,2108)])
drawgeom(p,circulation.intersection(floor),fill=(.05,.67,.30),alpha=.17,width=0)
# The source treppe paths are re-drawn in black without changing their dash pattern.
for path in clean[0].get_drawings():
 if path.get('layer')!='410 treppe':continue
 sh=p.new_shape()
 for item in path['items']:
  if item[0]=='l':sh.draw_line(item[1],item[2])
  elif item[0]=='c':sh.draw_bezier(*item[1:])
  elif item[0]=='re':sh.draw_rect(item[1])
 sh.finish(color=(0,0,0) if path.get('color') is not None else None,fill=(0,0,0) if path.get('fill') is not None else None,width=path.get('width') or .4,dashes=path.get('dashes'),closePath=path.get('closePath',False),lineCap=max(path.get('lineCap') or (0,)),lineJoin=int(path.get('lineJoin') or 0),even_odd=bool(path.get('even_odd')));sh.commit()
walk.save(R/'green.pdf',garbage=4,deflate=True)
for name,doc in [('walls',wall),('green',walk)]:doc[0].get_pixmap(matrix=fitz.Matrix(.5,.5)).save(R/(name+'_qa.png'))
print('BASES READY',flush=True)

# All panels are vector pages with closed feature frames AND arrows.
panels=fitz.open();sources={'clean':clean,'walls':wall,'green':walk};records=[]
for lesson in L:
 p=panels.new_page(width=1400,height=960);setup(p);p.draw_rect(p.rect,fill=(.965,.979,.985),color=None)
 roi=fitz.Rect(lesson['roi']);area=fitz.Rect(224,75,1176,887);sc=min(area.width/roi.width,area.height/roi.height)
 dst=fitz.Rect(700-roi.width*sc/2,481-roi.height*sc/2,700+roi.width*sc/2,481+roi.height*sc/2)
 p.draw_rect(dst+(-2,-2,2,2),fill=(1,1,1),color=(.72,.78,.81),width=1)
 p.show_pdf_page(dst,sources[lesson['base']],0,clip=roi)
 def pt(q):return dst.x0+(q[0]-roi.x0)*sc,dst.y0+(q[1]-roi.y0)*sc
 for typ,col,data in lesson['traces']:
  points=arcpts(data) if typ=='arc' else data;s=p.new_shape();s.draw_polyline([pt(q) for q in points]);s.finish(color=C[col],width=3.6,dashes='[7 5] 0' if typ=='dash' else None,closePath=False);s.commit()
 for j,(title,desc,col,target,frame) in enumerate(lesson['calls']):
  side=j%2;row=j//2;x=10 if side==0 else 1188;y=115+row*350
  rr=fitz.Rect(x,y,x+200,y+206);p.draw_rect(rr,fill=(1,1,1),color=C[col],width=1.4)
  tb(p,(x+12,y+12,x+188,y+81),title,19,col,True);tb(p,(x+12,y+84,x+188,y+194),desc,17.5)
  a=pt(frame[:2]);b=pt(frame[2:]);p.draw_rect(fitz.Rect(a,b),color=C[col],width=2.6)
  end=pt(target);arrow(p,(x+200 if side==0 else x,y+155),end,col);p.draw_circle(end,4,color=C[col],fill=(1,1,1),width=1.8)
  records.append({'id':lesson['id'],'heading':title,'text':desc,'color':col,'target_pdf_pt':target,'closed_frame_pdf_pt':frame})
 txt(p,(235,34),lesson['id']+' | Markierungen am Originalausschnitt',22,bold=True)
 txt(p,(235,935),'Geschlossener Rahmen + Pfeil: erklärter Bereich. Farblinien: hervorgehobene Merkmale.',17)
panels.save(R/'panels.pdf',garbage=4,deflate=True)
(R/'lessons.json').write_text(json.dumps(L,ensure_ascii=False,indent=2));(R/'annotations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('PANELS READY',len(L),flush=True)

# A3 landscape book. Embed the source forms once and reuse them for every crop.
pdfmetrics.registerFont(TTFont('DV',str(FONT)));pdfmetrics.registerFont(TTFont('DVB',str(BOLD)))
PAGE=(1190.55,841.89);INK=colors.HexColor('#17313d');TEAL=colors.HexColor('#087969')
body=ParagraphStyle('body',fontName='DV',fontSize=12,leading=17,textColor=INK)
small=ParagraphStyle('small',parent=body,fontSize=10,leading=14)
head=ParagraphStyle('head',parent=body,fontName='DVB',fontSize=13,leading=18,textColor=TEAL)
c=canvas.Canvas(str(R/'layout.pdf'),pagesize=PAGE,pageCompression=1);placements=[];n=0;toc=[]
def para(s,x,y,w,style=body):
 q=Paragraph(s,style);_,h=q.wrap(w,1200);q.drawOn(c,x,y-h);return y-h
def page(title,tag):
 global n;n+=1;toc.append([1,title,n]);c.setFillColor(INK);c.rect(0,827,1191,15,fill=1,stroke=0);c.setFillColor(TEAL);c.setFont('DVB',11);c.drawString(32,801,tag);c.setFillColor(INK);c.setFont('DVB',23);c.drawString(32,764,title)
 c.setFont('DV',9);c.drawString(32,25,'LEOPOLD-KOHR-SCHULE | SH22-LKS | 2. OG | Lernfassung zur Kontrolle | 21.09.2026');c.drawRightString(1158,25,f'{n:02}');c.setStrokeColor(colors.HexColor('#cedcdf'));c.line(32,52,1158,52)
def vector(src,pno,rect,clip=None):placements.append((n-1,src,pno,rect,clip))
def done():c.showPage()
page('2. Obergeschoss: Mauern sind rot markiert.','01 / GESAMTPLAN')
vector('walls',0,(27,103,1163,754));para('Rot markiert die erkennbaren Wandkörper und massiven Stützen. Geländer, Brüstungen, Fenster und Wartungsbereiche werden gesondert erklärt. Details sind auf den Folgeseiten vergrößert.',32,88,1126,small);done()
page('2. Obergeschoss: Geh- und Bodenflächen in Grün','02 / GESAMTPLAN')
vector('green',0,(27,103,1163,754));para('Grün: interpretierte Bodenflächen, einschließlich Treppen. Schwarz: Originalkanten, Stufen und Bruchlinien. Ausgesparte Sonderbereiche sind nicht automatisch gewöhnliche Gehwege. Keine vermessene Körperfreiraummaske.',32,88,1126,small);done()
page('So liest du die Markierungen und ihre Begründung','03 / FARBEN, RAHMEN UND ORIGINALBELEGE')
y=710
for h,t in [
 ('Rot: Wandkörper und feste massive Hindernisse','Die Übersicht markiert Materialbereiche mit geschlossenen Konturen. Auf jeder Detailseite steht zusätzlich ein geschlossener rechteckiger Rahmen um das erklärte Stück. Ein Pfeil ordnet die Begründung zu.'),
 ('Blau, Orange und Violett: konkret beschriftete Merkmale','Die Farbe allein ist keine Bauteilklasse. Die Beschriftung nennt jeweils Blatt, Rahmen, Bogen, Höhenbezug oder feste Grenze. Tür- und Fensterbögen werden direkt am Original nachgezeichnet.'),
 ('Grün: flächiger Boden mit ausgesparten Hindernissen','Die Füllung folgt erkennbaren Innen- und Außenböden. Wände, Schächte, erfasste Einbauten und feste Grenzabschnitte sind ausgespart. Dunkleres Grün hebt Erschließungsbeispiele hervor; es ist keine Breitenmessung.'),
 ('Sackgasse: betretbar, aber kein Durchgang','Ein Endraum kann betreten werden. Am festen Abschluss geht es nicht weiter; zurück führt derselbe Zugang. Er darf nicht mit einer unzugänglichen Fläche verwechselt werden.'),
 ('Treppen und andere Ebenen','Die Stufen bleiben schwarz sichtbar. Auf- und Abstieg brauchen einen Startpunkt, einen Lauf und Höhenbelege. Ein Pfeil auf dem Papier allein benennt noch kein Zielgeschoss.'),
 ('Quelle und Interpretation','Alle Planausschnitte stammen aus Schule_SH22_2_OG.pdf; Texte und Geometrie wurden mit der zugehörigen 2OG-DXF abgeglichen. Die allgemeine Treppen-Seitenansicht am Ende ist ausdrücklich ein Schema. Diese Lernfassung ist keine geprüfte Wegfreigabe.')]:
 y=para(h,40,y,1100,head);y=para(t,40,y-6,1100)-21
assert y>60,y;done()
regions=[('West','Linker Gebäudeflügel, innere Kerne und Außenbereich',[20,20,1600,1990]),('Mitte','Werkbereiche, Umgang, Klassen und Terrasse',[1510,560,2730,2330]),('Ost','Rechter Gebäudeflügel, Stiege 1 und Außenbereich',[2680,560,4230,2930])]
for name,desc,roi in regions:
 page('Mauern im Bereich '+name,'ÜBERSICHT / VON AUSSEN NACH INNEN');vector('walls',0,(28,111,883,747),roi)
 y=710
 for h,t in [('Orientierung',desc+'.'),('Was rot bedeutet','Die rote Umrandung folgt den erkennbaren Materialbereichen. Breite Außenaufbauten, Innenwände, dünne Trennwände und massive Stützen sind eingeschlossen.'),('Öffnungen erhalten','Fenster, Türflügel und deren Schwenkbögen werden nicht zu durchgehenden Mauern geschlossen.'),('Grenzen anders benennen','Eine Absturzsicherung, Brüstung oder ein Glasabschluss kann einen Weg sperren. Die Bauteilklasse wird trotzdem vom Mauerwerk getrennt.')]:y=para(h,903,y,250,head);y=para(t,903,y-5,250)-19
 done()
for i,l in enumerate(L):
 page(l['title'],l['id']+' / '+l['topic'].upper());vector('panels',i,(20,112,857,710))
 y=721
 for h,t in l['sections']:y=para(h,873,y,282,head);y=para(t,873,y-6,282)-19
 assert y>85,(l['id'],y)
 para('Original: Schule_SH22_2_OG.pdf, Blatt 1. Rahmen sind Erklärhilfen und keine exakt vermessenen Objektgrenzen.',35,95,800,small);done()
for name,desc,roi in regions:
 page('Grüne Flächen im Bereich '+name,'GEHFLÄCHEN / VERGRÖSSERTE KONTROLLE');vector('green',0,(28,111,883,747),roi)
 y=710
 for h,t in [('Flächig statt als Linie',desc+'. Grün zeigt die erkennbaren Bodenbereiche.'),('Körperweg','Ein Weg braucht zusammenhängenden Boden, ausreichend Platz und eine belegte Öffnung. Durch Mauer, Glas oder Absturzsicherung geht es nicht weiter.'),('Treppen bleiben lesbar','Die grüne Füllung liegt unter den wieder sichtbaren schwarzen Stufen- und Bruchlinien.'),('Offene Punkte','Nicht alle Möbelkonturen sind geschlossen. Türzustände, tatsächliche freie Breiten und die Anschlussniveaus der Brücke sind gesondert zu prüfen.')]:y=para(h,903,y,250,head);y=para(t,903,y-5,250)-19
 done()
page('Treppe von der Seite: was im Grundriss fehlt','SCHEMA / KEIN GEBÄUDESCHNITT')
# Exact vector educational diagram, deliberately not a fabricated building section.
x0,y0=95,285;dx,dy=85,42
c.setStrokeColor(INK);c.setLineWidth(3);p=c.beginPath();p.moveTo(x0-30,y0)
for i in range(6):p.lineTo(x0+i*dx,y0+i*dy);p.lineTo(x0+i*dx,y0+(i+1)*dy);p.lineTo(x0+(i+1)*dx,y0+(i+1)*dy)
p.lineTo(x0+6*dx+95,y0+6*dy);c.drawPath(p)
c.setFont('DVB',14);c.drawString(78,244,'unteres Podest');c.drawString(548,563,'oberes Podest')
c.setStrokeColor(colors.HexColor('#178750'));c.setLineWidth(3);c.line(149,395,559,599);c.line(559,599,541,577);c.line(559,599,531,595);c.setFillColor(TEAL);c.drawString(302,535,'aufwärts');c.setFillColor(INK)
c.setStrokeColor(colors.HexColor('#bd6209'));c.line(98,328,181,328);c.line(98,318,98,338);c.line(181,318,181,338);c.setFont('DV',12);c.drawString(99,345,'Auftritt a')
c.line(199,289,199,326);c.line(191,289,207,289);c.line(191,326,207,326);c.drawString(211,301,'Steigung s')
y=710
for h,t in [('Was eine Stufe macht','Jede Steigung erhöht das Niveau. Der Auftritt ist der waagerechte Trittteil. Das Schema zeigt sechs Beispielstufen, nicht die Anzahl eines konkreten Gebäudelaufs.'),('Beispiel aus diesem Plan','13 STG 15/30 ergibt 13 × 0,15 m = 1,95 m Höhenunterschied. 26 STG mit 15 cm ergeben 3,90 m. Die Werte stammen aus den Beschriftungen.'),('Rauf und runter','Von der unteren Fläche zur höheren führt der Weg aufwärts. Derselbe Lauf kann rückwärts abwärts benutzt werden, sofern er zugänglich ist.'),('Was zur Zuordnung noch nötig ist','Die Anschlusshöhen und das Nachbargeschoss bestätigen erst, welches Podest zum 2. OG gehört. Blattoben oder Blattunten ersetzt diese Zuordnung nicht.')]:y=para(h,790,y,355,head);y=para(t,790,y-6,355)-22
para('Schema ohne Maßstab. Stufen, Podeste und Pfeil dienen nur dazu, den Höhenwechsel zu erklären.',56,180,690,small);done()
page('So soll Claude Code dieses Wissen umsetzen','LERNREGELN / FÜR DIE SPÄTERE DATEIÜBERGABE')
y=711
for h,t in [('1. Quelle und Geschoss festhalten','Nur die hier genannte 2OG-PDF und die zugehörige DXF verwenden. Originaldateien erhalten und jede Ableitung an ihre Quelle binden.'),('2. Bauteile mit Belegen erkennen','Wandkörper, Stützen, Türen, Fenster, Glasgrenzen, Geländer, Brüstungen, Treppen, Schächte und Wartungsbereiche getrennt erfassen. Zu jedem Objekt Kontur, Originaltext und Begründung speichern.'),('3. Wände nicht aus beliebigen Linien erzeugen','Material, Kanten, Anschluss und Kontext zusammen auswerten. Möbelraster, Gefällelinien, Türbögen, Treppenbruch und Decken-/Voutenlinien sind keine pauschalen Mauerbelege.'),('4. Boden und Verbindungen getrennt modellieren','Bodenbereiche ergeben noch keine Route. Öffnungen verbinden Bereiche; Wände und feste Grenzen sperren Verbindungen. Ein Endraum bleibt erreichbar, obwohl er keine Durchgangsroute bietet.'),('5. Körperfreiraum und Höhen prüfen','An jeder Engstelle Türöffnung, Hindernisse und benötigte Körperbreite prüfen. Treppen erhalten einen Höhenwechsel; nicht belegte Anschlussgeschosse bleiben ungeklärt.'),('6. Ergebnisse kontrollierbar ausgeben','Farbiges Kontroll-PDF, Objekt- und Verbindungsdaten sowie offene Fragen gemeinsam erzeugen. Lernmarkierungen nicht als fehlerfreie Trainingsmaske importieren. Eine Erkennungs-Engine wurde für diese Lernfassung noch nicht ausgeführt.')]:
 y=para(h,40,y,1100,head);y=para(t,40,y-5,1100)-18
assert y>80,y
para('Quellen: Schule_SH22_2_OG.pdf | 20220225-SH22-LKS-GE-AP-02-01-A-2OG.dxf. Stand: 21.09.2026. Dieses PDF dient deiner Kontrolle; das vollständige ZIP folgt erst nach deinem Go.',40,82,1100,small);done()
c.save();book=fitz.open(R/'layout.pdf');docs={'walls':wall,'green':walk,'panels':panels}
for dest,src,pno,rect,clip in placements:book[dest].show_pdf_page(fitz.Rect(rect),docs[src],pno,clip=fitz.Rect(clip) if clip else None)
book.set_toc(toc);book.set_metadata({'title':'Leopold-Kohr-Schule - 2. OG - Lernbuch zur Raumerkennung','author':'SH22-LKS | Lernmaterial für Claude Code','subject':'Mauern, Türen, Fenster, Gehflächen und Treppen mit Vektormarkierungen'})
target=O/'Leopold_Kohr_Schule_2OG_Lernbuch_zur_Kontrolle.pdf';book.save(target,garbage=4,deflate=True)
assert all(not p.get_images() for p in book),'Rasterbilder in finalem PDF'
checks={'pages':len(book),'vector_only':True,'detail_pages':len(L),'closed_frames':len(records),'registration':reg,'file':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_pdf_sha256':hashlib.sha256((ROOT/'quellen/Schule_SH22_2_OG.pdf').read_bytes()).hexdigest(),'source_dxf_sha256':hashlib.sha256((ROOT/'quellen/20220225-SH22-LKS-GE-AP-02-01-A-2OG.dxf').read_bytes()).hexdigest()}
(R/'checks.json').write_text(json.dumps(checks,indent=2));print('BOOK READY',json.dumps(checks),flush=True)
