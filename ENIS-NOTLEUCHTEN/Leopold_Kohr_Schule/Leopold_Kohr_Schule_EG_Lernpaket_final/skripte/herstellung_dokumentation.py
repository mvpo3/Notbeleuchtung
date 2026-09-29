from pathlib import Path
import json,math,shutil,hashlib,zipfile,sys
import fitz
from shapely.geometry import Polygon,LineString,box,shape,mapping
from shapely.ops import unary_union,polygonize,transform
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from PIL import Image
from annotation_data import C,EXTRA
W=Path.cwd(); OLD=W/'output/pdf/Leopold_Kohr_Schule_EG_Lernpaket_v1'; ROOT=W/'output/pdf/Leopold_Kohr_Schule_EG_Lernpaket_final'; TMP=W/'tmp/eg_v2';OUT=ROOT.parent
BOOK='Leopold_Kohr_Schule_EG_Lernbuch_final.pdf'; WALK='Leopold_Kohr_Schule_EG_Gehflaechen_gruen.pdf'
if not ROOT.exists():shutil.copytree(OLD,ROOT)
for n in ['MANIFEST.json','PRUEFSUMMEN.txt','PRUEFUNG.json','Leopold_Kohr_Schule_EG_Lernbuch_v1.pdf','Raumerkennungenis_EG_Arbeitsstand_2026-09-21.md']:
 (ROOT/n).unlink(missing_ok=True)
font=ROOT/'skripte/fonts/DejaVuSans.ttf';bold=ROOT/'skripte/fonts/DejaVuSans-Bold.ttf'
# Locate the already bundled font names.
if not font.exists():
 font=next((ROOT/'skripte').rglob('DejaVuSans.ttf'));bold=next((ROOT/'skripte').rglob('DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DV',str(font)));pdfmetrics.registerFont(TTFont('DVB',str(bold)))
COL={'red':(0.82,.06,.15),'blue':(.02,.34,.77),'orange':(.84,.36,.02),'purple':(.47,.19,.65),'green':(.02,.51,.26),'ink':(.08,.16,.20)}
def js(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def md(p,d):(ROOT/p).write_text(d.strip()+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def setup(p):
 p.insert_font(fontname='dv',fontfile=str(font));p.insert_font(fontname='dvb',fontfile=str(bold))
def tx(p,point,text,size=20,col='ink',bold=False):p.insert_text(point,text,fontname='dvb' if bold else 'dv',fontsize=size,color=COL.get(col,col))
def textblock(p,rect,text,size=19,col='ink',bold=False):
 z=p.insert_textbox(fitz.Rect(rect),text,fontname='dvb' if bold else 'dv',fontsize=size,lineheight=1.22,color=COL.get(col,col))
 if z<0:raise ValueError((text,z,rect))
def poly_draw(p,g,fill,color=None,width=0,opacity=1):
 if g.is_empty:return
 sh=p.new_shape()
 for a in (list(g.geoms) if hasattr(g,'geoms') else [g]):
  if not isinstance(a,Polygon):continue
  for ring in [a.exterior,*a.interiors]:sh.draw_polyline(list(ring.coords))
 sh.finish(fill=fill,color=color,width=width,fill_opacity=opacity,even_odd=True);sh.commit()
def arrow(p,a,b,col,width=2):
 c=COL[col];p.draw_line(a,b,color=c,width=width)
 dx,dy=b[0]-a[0],b[1]-a[1];d=max(1,math.hypot(dx,dy));ux,uy=dx/d,dy/d;v=9
 q=[b,(b[0]-ux*v-uy*v*.5,b[1]-uy*v+ux*v*.5),(b[0]-ux*v+uy*v*.5,b[1]-uy*v-ux*v*.5)]
 s=p.new_shape();s.draw_polyline(q+[b]);s.finish(color=c,fill=c);s.commit()
clean=fitz.open(ROOT/'plaene/EG_Architekturbasis_Lernansicht.pdf');walls=fitz.open(ROOT/'plaene/Leopold_Kohr_Schule_EG_Mauern_rot_v1.pdf')
S=.056691975091847105;TX=3398.78476561896;TY=2928.9804439164363
def topdf(x,y,z=None):return TX+x*S,TY-y*S
def tocad(x,y,z=None):return (x-TX)/S,(TY-y)/S
wallmeta=json.loads((ROOT/'daten/06_MAUER_MARKIERUNGEN_EG.geojson').read_text())
wg=unary_union([transform(topdf,shape(f['geometry'])) for f in wallmeta['features']])
# All main floor parts and the separate annex; hall volumes deliberately outside.
regions=[
 ('G01','Verwaltung',Polygon([(939,923),(2420,923),(2420,1578),(1371,1578),(1371,1830),(1038,1830),(1038,1420),(939,1420)])),
 ('G02','Stiege 6 und Vorbereich',box(933,1424,1009,1834)),
 ('G03','Linke Erschließung',box(2440,1018,2564,1578)),
 ('G04','Schulwart, Windfang, Halle, Bibliothek und Musik',box(2580,861,3413,2309)),
 ('G05','Rechte Erschließung',box(3440,1036,3565,1998)),
 ('G06','Rechte Nebenräume und Stiege 1',Polygon([(3582,1445),(5054,1445),(5054,1994),(4515,1994),(4515,2010),(3582,2010)])),
 ('G07','Speiseraum und Küche',Polygon([(3440,2010),(5055,2010),(5055,2804),(4620,2804),(4620,2714),(3440,2714)])),
 ('G08','Außentreppe 4',box(1818,2060,2370,2180)),
 ('G09','Außentreppe 3',box(2870,2577,3412,2697)),
 ('G10','Nebengebäude',Polygon([(48,3290),(398,3168),(644,3410),(661,3458),(161,3630)])),
 ]
# Portal strips only where the source shows a passage; no all-purpose wall closing.
portals=[box(2404,1245,2455,1334),box(2548,1070,2590,1230),box(3404,1070,3450,1230),box(3558,1510,3595,1608),box(3428,2020,3450,2130)]
# The supports and closed furniture footprints remain unfilled.
lines=json.loads((W/'tmp/eg/lines.json').read_text())
flines=[LineString([(a,b),(c,d)]) for a,b,c,d,layer,h in lines if layer in ['510 Moeblierung','530 Kueche','540 Sanitaereinrichtung'] and math.hypot(c-a,d-b)>1]
# Snap endpoints to 1 mm for drawing fragment tolerance; no semantics inferred from a single line.
flines=[LineString([(round(x),round(y)) for x,y in l.coords]) for l in flines]
fpol=[p for p in polygonize(unary_union(flines)) if 20000<p.area<20000000]
furniture=unary_union([transform(topdf,p) for p in fpol])
shafts=unary_union([box(2090,1266,2160,1384),box(3850,1676,3942,1805)])
# Thin fixed glass partitions: subtract the solid spans; source doors remain independent.
barriers=unary_union([
 box(2995,874,3004,1018),
 box(2580,1594,2670,1603),box(2780,1594,3000,1603),box(3000,1594,3100,1603),box(3210,1594,3413,1603),
 box(2590,1020,2778,1028),box(2860,1020,2920,1028), # solid segments below school caretaker
 ])
obstacles=unary_union([wg,furniture,shafts,barriers])
features=[]
for ident,name,g in regions:
 q=g.difference(obstacles).buffer(0)
 features.append({'type':'Feature','id':ident,'properties':{'name':name,'klasse':'Bodenbereich_Lerninterpretation','ground_truth':False,'koerperfreiraum_bestaetigt':False},'geometry':mapping(q)})
allgreen=unary_union([shape(f['geometry']) for f in features]+[p.difference(obstacles) for p in portals])
# Green is a documented reading of the floor drawing, not a generated route authorization.
js('daten/12_GEHFLaECHEN_EG.geojson',{'type':'FeatureCollection','coordinate_reference':'PDF_Punkte_Originalblatt_5227x3727_Ursprung_links_oben','hinweis':'Manuell interpretierte Bodenbereiche mit ausgesparten Materialkonturen, Schächten, festen Glasabschnitten und geschlossenen Möbelkonturen. Keine exakte Körperfreiraummaske.','features':features})
js('daten/12a_GEHFLAECHEN_HERKUNFT.json',{'floor':'EG','methode':'Manuelle Bereichsumrisse, Abzug der dokumentierten Lern-Wandkonturen sowie gesonderter Sperrflächen und geschlossener CAD-Einbaukonturen.','originale_unveraendert':True,'mobiliar_polygonanzahl':len(fpol),'dunkelgruen':'zusammenhaengende_Erschliessungsbeispiele','hellgruen':'Bodenbereiche_mit_erkennbaren_Hindernissen_ausgespart','amber':'Geschossboden_ungeklaert','keine_gemessene_Koerperhuelle':True,'keine_automatische_Sackgasseninventur':True,'treppen_zielgeschoss_bestaetigt':False,'engine_ausgefuehrt':False})
walk=fitz.open();p=walk.new_page(width=5227,height=3727);p.show_pdf_page(p.rect,clean,0);setup(p)
poly_draw(p,allgreen,(.43,.88,.58),opacity=.37)
# Stronger green in visible circulation, while maintaining the same obstacles.
circs=[box(940,1093,1660,1412),box(1660,1093,2090,1246),box(2438,1040,2564,1578),box(2580,1040,3413,1593),box(3440,1040,3565,1998),box(3582,1445,4110,1645),box(3950,1770,4130,2008),box(4100,1856,4505,1909)]
cg=unary_union(circs).intersection(allgreen);poly_draw(p,cg,(.08,.73,.30),opacity=.20)
# Amber wash on the hall footprints; these cannot become an EG through-route.
for r in [box(944,92,2410,887),box(3610,621,5048,1390)]:
 poly_draw(p,r,(1,.77,.32),opacity=.15)
 for x in range(int(r.bounds[0])-600,int(r.bounds[2]),90):
  seg=LineString([(x,r.bounds[1]),(x+900,r.bounds[3])]).intersection(r)
  if not seg.is_empty:p.draw_line(seg.coords[0],seg.coords[-1],color=(.79,.52,.1),width=.6,stroke_opacity=.3)
# Copy native PDF staircase paths in black. Keep every original gap and curve.
# DXF linetype names alone do not reconstruct the plotted segmented appearance.
for path in clean[0].get_drawings():
 if path.get('layer')!='410 treppe':continue
 sh=p.new_shape()
 for item in path['items']:
  if item[0]=='l':sh.draw_line(item[1],item[2])
  elif item[0]=='c':sh.draw_bezier(*item[1:])
 sh.finish(color=(0,0,0) if path.get('color') is not None else None,
           fill=(0,0,0) if path.get('fill') is not None else None,
           width=path.get('width') or .4,dashes=path.get('dashes'),
           closePath=path.get('closePath',False),lineCap=max(path.get('lineCap') or (0,)),
           lineJoin=int(path.get('lineJoin') or 0),even_odd=bool(path.get('even_odd')))
 sh.commit()
walk.save(ROOT/'plaene/EG_Gehflaechen_Basis.pdf',garbage=4,deflate=True)
walkdetail=fitz.open(ROOT/'plaene/EG_Gehflaechen_Basis.pdf')
# Fixed barriers and selected dead-end stop marks, each explicitly interpretable.
for a,b in [((2999,874),(2999,1018)),((1417,934),(1493,934))]:p.draw_line(a,b,color=COL['purple'],width=3)
def maplabel(point,title,sub,w=480):
 x,y=point;p.draw_rect(fitz.Rect(x,y,x+w,y+100),fill=(1,1,1),color=(.72,.79,.76),width=1.2)
 tx(p,(x+14,y+36),title,26,'ink',True);tx(p,(x+14,y+74),sub,21,'ink')
maplabel((1260,425),'Hallenbereich: Bodenhöhe prüfen','Keinen EG-Durchgang daraus ableiten.',650)
maplabel((3900,940),'Hallenbereich: Bodenhöhe prüfen','Fensterangaben beziehen sich auf UG.',660)
# Place callout in empty margin, pointing at IKT room end.
maplabel((1470,1900),'Sackgassen-Beispiel: IKT 0.21','Ein Zugang: hinein und zurück.',650)
arrow(p,(1660,1900),(1450,977),'orange',3)
p.draw_line((1422,939),(1489,939),color=COL['red'],width=4)
for x,y,n in [(3610,1830,1),(2210,1450,2),(3030,2600,3),(1950,2080,4),(4960,2240,5),(923,1660,6)]:
 p.draw_rect(fitz.Rect(x,y,x+105,y+42),fill=(1,1,1),color=None);tx(p,(x+5,y+29),'ST '+str(n),23,'ink',True)
p.draw_rect(fitz.Rect(2630,0,5170,510),fill=(1,1,1),color=None)
tx(p,(2690,90),'EG: GEHFLÄCHEN IN GRÜN',65,'ink',True)
for i,t in enumerate(['Grün: aus dem Plan interpretierte Boden- und Treppenbereiche.', 'Schwarz: Originalkanten und Stufen; Violett: ausgewählte feste Abschlüsse.', 'Ocker schraffiert: Boden auf EG-Niveau nicht belegt.', 'Sackgasse bleibt begehbar; am Abschluss führt nur der Rückweg weiter.', 'Türflächen gelten bei geöffneter Tür. Weiß ist keine automatische Sperre.', 'Keine exakte Körperfreiraummaske; offene Möbelkonturen können unvollständig sein.']):
 tx(p,(2690,166+i*48),t,26,'ink')
for i,t in enumerate(['Original: Schule_SH22_EG.pdf | Lernrevision mit Flächen statt Routenlinie', 'Große Gänge sind flächig grün; Möbel, Wände und Schächte bleiben ablesbar.', 'Treppen: Zielgeschoss / Auf- und Abstieg erst mit Schnitt und Nachbargeschoss bestätigen.', 'Dies ist eine Lernzeichnung zum Planlesen, keine geprüfte Weg- oder Fluchtwegfreigabe.']):
 tx(p,(2300,3450+i*52),t,27,'ink')
walk.save(ROOT/'plaene'/WALK,garbage=4,deflate=True)
p.get_pixmap(matrix=fitz.Matrix(.58,.58)).save(ROOT/'bilder/00b_EG_Gehflaechen_Gesamt.png')
print('GREEN_DONE',len(features),len(fpol),flush=True)

lessons=json.loads((OLD/'daten/04_BEISPIELE_EG.json').read_text())['examples']
lessons.extend(EXTRA)
for l in lessons:
 l['sections']=[[h,t.replace('Die blaue Markierung A','Die Markierung').replace('Markierung A','Die Markierung').replace('Suchrahmen A','Der markierte Bereich').replace('Rahmen A','Die Markierung').replace('Die grüne Linie','Die grüne Bodenfläche').replace('grüne Linie','grüne Bodenfläche').replace('Der dünne grüne Strich','Die grüne Füllung')] for h,t in l['sections']]
# Direct feature tracings in crop-normalized coordinates.
H={
 'EG-07':[('red',[(.706,.50),(.706,.90)]),('orange',[(.798,.49),(.798,.93)]),('blue',[(.04,.833),(.70,.833)])],
 'EG-08':[('red',[(.445,.18),(.445,.316)]),('red',[(.445,.56),(.445,.746)]),('blue',[(.445,.316),(.65,.316)])],
 'EG-10':[('blue',[(.211,.50),(.211,.76)]),('blue',[(.797,.50),(.797,.76)]),('green',[(.215,.775),(.796,.775)])],
 'EG-11':[('blue',[(.112,.196),(.39,.196)]),('blue',[(.112,.835),(.39,.835)]),('orange',[(.73,.815),(.77,.815)])],
 'EG-12':[('blue',[(.16,.64),(.525,.64)]),('purple',[(.24,.516),(.409,.516)])],
 'EG-13':[('blue',[(.09,.266),(.24,.266)]),('purple',[(.086,.517),(.23,.517)])],
 'EG-14':[('purple',[(.923,.234),(.923,.731)]),('red',[(.263,.72),(.40,.72)])],
 'EG-16':[('red',[(.30,.097),(.80,.097)]),('green',[(.39,.84),(.39,.69)])],
 'EG-17':[('purple',[(.05,.21),(.95,.21)])],
 'EG-18':[('orange',[(.26,.358),(.337,.358)]),('red',[(.51,.449),(.687,.449)])],
 'EG-20':[('blue',[(.534,.574),(.80,.574)]),('orange',[(.665,.68),(.665,.171)]),('purple',[(.22,.393),(.506,.31)])],
 'EG-21':[('blue',[(.10,.318),(.45,.318)]),('purple',[(.48,.293),(.839,.373)])],
 'EG-22':[('blue',[(.324,.391),(.515,.391)]),('orange',[(.418,.187),(.418,.655)])],
 'EG-23':[('blue',[(.28,.377),(.532,.377)]),('orange',[(.445,.195),(.445,.655)])],
 'EG-24':[('blue',[(.55,.224),(.55,.723)]),('orange',[(.25,.48),(.87,.48)])],
 'EG-25':[('blue',[(.53,.27),(.53,.82)]),('orange',[(.205,.55),(.90,.55)])],
 'EG-27':[('red',[(.65,.1),(.65,.50)]),('blue',[(.607,.10),(.607,.90)]),('orange',[(.774,.10),(.774,.90)])],
 'EG-28':[('blue',[(.03,.674),(.648,.674),(.648,.10)]),('red',[(.03,.929),(.86,.929),(.86,.10)])],
}
# Data records include feature target positions, callout text, and source crop.
annotation_records=[]
for l in lessons:
 ident=l['id'];roi=fitz.Rect(l['roi']);isgreen=ident in ['EG-15','EG-16','EG-17','EG-19','EG-20','EG-21','EG-22','EG-23','EG-24','EG-25','EG-26']
 src=walkdetail if isgreen else (walls if l['base']=='walls' else clean)
 doc=fitz.open();pg=doc.new_page(width=1400,height=960);setup(pg)
 pg.draw_rect(pg.rect,fill=(.967,.98,.985),color=None)
 area=fitz.Rect(224,80,1176,880);sc=min(area.width/roi.width,area.height/roi.height)
 iw,ih=roi.width*sc,roi.height*sc;dst=fitz.Rect(area.x0+(area.width-iw)/2,area.y0+(area.height-ih)/2,area.x0+(area.width+iw)/2,area.y0+(area.height+ih)/2)
 pg.draw_rect(dst+(-2,-2,2,2),fill=(1,1,1),color=(.76,.8,.82),width=1)
 pg.show_pdf_page(dst,src,0,clip=roi)
 def uv(u,v):return (dst.x0+u*dst.width,dst.y0+v*dst.height)
 def abspt(x,y):return uv((x-roi.x0)/roi.width,(y-roi.y0)/roi.height)
 for col,pts in H.get(ident,[]):
  ss=pg.new_shape();ss.draw_polyline([uv(*q) for q in pts]);ss.finish(color=COL[col],width=3,closePath=False);ss.commit()
 if ident=='EG-09':
  cx,cy,r=1414.58,1086.05,51.023
  pg.draw_line(abspt(cx,cy),abspt(cx,cy-r),color=COL['blue'],width=3.8)
  pts=[abspt(cx+r*math.cos(t),cy+r*math.sin(t)) for t in [-math.pi/2+i*math.pi/2/60 for i in range(61)]]
  ss=pg.new_shape();ss.draw_polyline(pts);ss.finish(color=COL['orange'],width=3.8,closePath=False);ss.commit()
  pg.draw_line(abspt(cx,cy),abspt(cx+r,cy),color=COL['purple'],width=3.5,dashes='[7 5] 0')
  pg.draw_line(abspt(cx,cy+5),abspt(cx+r,cy+5),color=COL['green'],width=4)
  pg.draw_circle(abspt(cx,cy),5,color=COL['blue'],fill=(1,1,1),width=2)
 for j,(title,desc,target,col) in enumerate(C[ident]):
  side=j%2;row=j//2;x=10 if side==0 else 1188;y=75+row*265
  rr=fitz.Rect(x,y,x+200,y+174);pg.draw_rect(rr,fill=(1,1,1),color=COL[col],width=1.5)
  ts=min(20,20*172/max(fitz.Font(fontfile=str(bold)).text_length(word,fontsize=20) for word in title.split()))
  textblock(pg,(x+12,y+11,x+188,y+65),title,ts,col,True)
  textblock(pg,(x+12,y+68,x+188,y+162),desc,18,'ink')
  t=uv(*target);a=(x+200 if side==0 else x,y+139)
  arrow(pg,a,t,col,2.0);pg.draw_circle(t,4.8,color=COL[col],fill=(1,1,1),width=2)
  annotation_records.append({'example_id':ident,'heading':title,'explanation':desc,'color':col,'target_pdf_pt':[roi.x0+target[0]*roi.width,roi.y0+target[1]*roi.height],'source_pdf':'Schule_SH22_EG.pdf','page':1,'target_accuracy':'visueller_Zeiger_keine_Vermessung'})
 tx(pg,(235,33),ident+' | Originalausschnitt mit direkt zugeordneten Merkmalen',21,'ink',True)
 tx(pg,(235,932),'Pfeile: erklärende Zuordnung. Farblinien: hervorgehobene Originalmerkmale.',18,'ink')
 name='bilder/'+ident+'.png'
 if '--reuse' not in sys.argv or ident in {'EG-19','EG-20','EG-21','EG-22','EG-23','EG-24','EG-25'}:pg.get_pixmap(matrix=fitz.Matrix(1.75,1.75)).save(ROOT/name)
 doc.close()
 l['image']=name;l['annotation_count']=len(C[ident]);l['markers']=[];l['source_pdf']='quellen/Schule_SH22_EG.pdf';l['source_dxf']='quellen/20220225-SH22-LKS-GE-AP-EG-01-C.dxf';l['pdf_page']=1;l['roi_unit']='PDF_point_top_left_origin';l['geometry_type']='Suchbereich_keine_Objektgrenze';l['status']='am_Originalplan_visuell_interpretiert_kein_Engine_Test';l['cad_bbox_mm']=[*tocad(roi.x0,roi.y1),*tocad(roi.x1,roi.y0)]
 print('DETAIL',ident,flush=True)
js('daten/13_BILDANNOTATIONEN_EG.json',{'schema':'rivoplan.eg.annotations/2','annotations':annotation_records,'line_highlights_normalized':H,'note':'Farbige Pfeile sind Kommentarlinien; nicht als ursprüngliche CAD-Bauteile importieren.'})
js('daten/04_BEISPIELE_EG.json',{'schema':'rivoplan.eg_lernpaket.examples/2','examples':lessons})
# Book: use large pages so callout text remains readable at normal zoom.
PAGE=(1190.55,841.89);INK=colors.HexColor('#15333d');TEAL=colors.HexColor('#087f72')
body=ParagraphStyle('body',fontName='DV',fontSize=12,leading=17,textColor=INK)
small=ParagraphStyle('small',parent=body,fontSize=9.5,leading=13)
head=ParagraphStyle('head',parent=body,fontName='DVB',fontSize=13.5,leading=18,textColor=TEAL)
def para(c,t,x,y,w,style=body):
 p=Paragraph(t,style);_,h=p.wrap(w,1000);p.drawOn(c,x,y-h);return y-h
n=0;c=canvas.Canvas(str(ROOT/BOOK),pagesize=PAGE,pageCompression=1);c.setTitle('EG Lernbuch - direkt beschriftete Originaldetails und grüne Gehflächen');c.setAuthor('Rivoplan | SH22-LKS | EG')
def page(title,tag):
 global n;n+=1
 c.setFillColor(INK);c.rect(0,827,1191,15,fill=1,stroke=0)
 c.setFont('DVB',11);c.setFillColor(TEAL);c.drawString(32,799,tag)
 c.setFont('DVB',25);c.setFillColor(INK);c.drawString(32,763,title)
 c.setFont('DV',9);c.drawString(32,24,'RIVOPLAN | Leopold-Kohr-Schule | EG | Überarbeitete Lernfassung | 21.09.2026');c.drawRightString(1157,24,f'{n:02}')
 c.setStrokeColor(colors.HexColor('#cadadf'));c.line(32,51,1157,51)
def img(path,x,y,w,h):
 im=Image.open(path);a,b=im.size;f=min(w/a,h/b);dw,dh=a*f,b*f;c.drawImage(str(path),x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')
def done():c.showPage()
page('Erdgeschoss: Mauern sind rot markiert.','01 / DER AUSGANGSPLAN BLEIBT ERHALTEN')
img(ROOT/'bilder/00_EG_Mauern_Gesamt.png',30,90,1128,654)
para(c,'Rot umfasst die erkennbaren Mauerkörper und massiven Pfeiler. Auf den folgenden Seiten zeigen Pfeile und farbige Linien die einzelnen Erkennungsmerkmale.',32,77,1124,small);done()
page('Erdgeschoss: Boden- und Gehbereiche flächig grün','02 / GESAMTPLAN MIT TREPPEN UND SACKGASSEN-BEISPIEL')
img(ROOT/'bilder/00b_EG_Gehflaechen_Gesamt.png',30,90,1128,654)
para(c,'Grün zeigt interpretierte Bodenflächen. Schwarz erhält die Stufenkanten. Ocker markiert ungeklärte EG-Bodenhöhe. Die große Plan-PDF liegt zusätzlich unter plaene/.',32,77,1124,small);done()
page('Was die Farben und Pfeile genau bedeuten','03 / LESEREGELN')
y=710
for h,t in [('Rot: fester Wandkörper','Zwei Begrenzungen, Materialdarstellung und Anschlüsse gemeinsam lesen. Auch breite Außenaufbauten, dünne Trennwände und massive Stützen versperren einen Durchgang.'),('Blau / Orange / Violett: Merkmal am Original','Blau hebt häufig eine Kante, einen Rahmen oder ein Türblatt hervor. Orange zeigt Bogen, Richtung oder Beleg. Violett kennzeichnet feste Glasabschlüsse, Höhenbezüge oder eine ausdrücklich gedachte Schließlage. Jeder Pfeil hat seine eigene Beschriftung.'),('Grün: Bodenfläche und Verbindung','Die Gänge sind flächig eingefärbt. Raum- und Treppenböden werden ebenfalls sichtbar. Wandkonturen, Schächte, feste Glasabschnitte und geschlossene Einbaukonturen sind ausgespart. Offene Möbelkonturen, lichte Breiten und reale Türzustände sind damit noch nicht vollständig geprüft.'),('Sackgasse: hinein möglich, durchgehen nicht','Ein Raum mit nur einem Zugang kann betreten werden. Am geschlossenen Wandende geht es nicht weiter; zurück führt derselbe Zugang. Das ist etwas anderes als eine völlig unzugängliche Fläche.'),('Treppen: Grundriss und Höhe zusammen lesen','Schwarze Querlinien sind Stufen. Laufpfeile und Bruchlinien bleiben erhalten. Ob ein konkreter Anschluss ins UG oder OG führt, wird erst durch Schnitte, Höhen und den Plan des Nachbargeschosses bestätigt.'),('Original und Lernmarkierung trennen','Alle Planbeispiele stammen aus derselben EG-DXF/PDF wie zuvor. Nur die allgemeine Treppen-Seitenansicht ist ein ausdrücklich bezeichnetes Schema. Markierungen und Bodenflächen sind Lerninterpretationen, keine millimetergenaue Trainingsmaske.')]:
 y=para(c,h,40,y,1100,head);y=para(c,t,40,y-5,1100)-21
assert y>60,y
done()
for l in lessons:
 page(l['title'],l['id']+' / '+l['topic'].upper())
 img(ROOT/l['image'],24,145,797,598)
 y=721
 for h,t in l['sections']:
  y=para(c,h,846,y,309,head);y=para(c,t,846,y-7,309)-20
 assert y>80,(l['id'],y)
 tip='Die Pfeilspitze zeigt die konkrete Stelle im Original. Die farbige Kommentarlinie ist selbst kein Bauteil.'
 if l['id']=='EG-09':tip='Gedachte Schließlage ist violett gestrichelt. Sie wurde zum Erklären ergänzt. DL 90/220 bleibt eine Planangabe; Türzustand und nutzbare Breite gesondert prüfen.'
 if l['id'].startswith('EG-2') and l['id'] not in ['EG-26','EG-27','EG-28']:tip='Grün zeigt den Lauf-/Bodenbereich, Schwarz die Originalstufen. Der Laufpfeil ist kein Ersatz für belegte Geschosshöhen.'
 para(c,tip,35,120,772,small)
 para(c,'Quelle: Schule_SH22_EG.pdf, Seite 1 | Ausschnitt '+l['id']+' | PDF-Suchbereich '+str(l['roi'])+' pt.',35,75,1110,small)
 done()
# Dedicated walk detail pages, with large green areas and source-scale labels.
for ident,title,roi,description in [
 ('G-A','Gehflächen: Verwaltung und geschlossene Raumenden',[890,900,2465,1890],'Die umlaufende Erschließung um den Kopierraum ist grün. Durch die Türöffnungen gelangt man in die angrenzenden Räume. IKT 0.21 hat nur einen sichtbaren normalen Zugang: hinein und auf demselben Weg zurück. Grün wird an Wandkörpern unterbrochen; es überspringt keine Fenster.'),
 ('G-B','Gehflächen: Windfang, Eingangshalle und Anschlüsse',[2410,800,3590,2340],'Die Eingangshalle bleibt auch unter dem gezeichneten Deckenrechteck grün. Die Linien des Deckenbauteils schneiden den Boden nicht in einzelne Räume. Feste Glasfelder sind keine Durchgänge. Verbindungen an Schiebetüren gelten bei geöffneter Tür.'),
 ('G-C','Gehflächen: Nebenräume, Speiseraum und Treppen',[3430,1400,5160,2870],'Bodenflächen und Erschließung sind grün. Geschlossene Tisch- und Einbaukonturen sind als Hindernisse ausgespart; die schwarzen Originalumrisse bleiben sichtbar. Die Treppen behalten ihre Stufen. Weiß bedeutet hier: ausgespart oder ungeklärt, nicht pauschal unzugänglich.'),
 ('G-D','Gehflächen: separat dargestelltes Nebengebäude',[0,3110,730,3727],'Auch im schräg gezeichneten Nebengebäude sind Bodenbereiche grün. Wandkörper, feste Trennungen und erkennbare Einbauten unterbrechen die Fläche. Türöffnungen sind lokale Zugänge. Ein Außenweg zum Hauptgebäude lässt sich aus der versetzten Blattdarstellung nicht ableiten.')]:
 d=fitz.open();pp=d.new_page(width=1100,height=760);pp.show_pdf_page(pp.rect,walk,0,clip=fitz.Rect(roi));f=ROOT/'bilder'/f'{ident}.png';pp.get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(f);d.close()
 page(title,ident+' / GRÜNE FLÄCHEN VERGRÖSSERT');img(f,35,155,1118,588);para(c,description,40,132,1105);done()
# Precise didactic vector schematic, explicitly not a construction section.
page('Treppen verstehen: Grundriss und Seitenansicht','S-01 / ALLGEMEINES SCHEMA - KEIN GEBÄUDESCHNITT')
c.setFillColor(colors.HexColor('#e0f3e4'));c.rect(50,408,490,260,fill=1,stroke=0)
c.setStrokeColor(colors.black);c.setLineWidth(1)
for i in range(9):c.line(85+i*48,420,85+i*48,655)
c.setStrokeColor(colors.HexColor('#cc6810'));c.setLineWidth(2);c.line(97,530,485,530);c.line(485,530,472,538);c.line(485,530,472,522)
c.setStrokeColor(colors.HexColor('#8051a8'));c.line(205,412,250,662);c.line(213,412,258,662)
para(c,'GRUNDRISS: schwarze Querlinien = Stufenkanten; orange Linie = Lauflinie; violette Schräge = Darstellungsbruch.',55,384,495,body)
# Side profile, four steps, rise and tread dimensions.
c.setStrokeColor(colors.black);c.setLineWidth(2);x,y=650,438;path=c.beginPath();path.moveTo(x,y)
for i in range(5):path.lineTo(x+72*i,y+35*i);path.lineTo(x+72*i,y+35*(i+1));path.lineTo(x+72*(i+1),y+35*(i+1))
c.drawPath(path)
c.setStrokeColor(colors.HexColor('#0c853f'));c.setLineWidth(3);c.line(660,468,999,632);c.line(999,632,982,631);c.line(999,632,990,618)
para(c,'Aufstieg: von niedrig zu hoch',725,685,390,head)
c.setStrokeColor(colors.HexColor('#155dca'));c.line(870,578,942,578);c.line(942,578,942,613)
para(c,'Auftritt a',860,559,180,small);para(c,'Steigung h',978,600,170,small)
para(c,'SEITENANSICHT: Jede Stufe verbindet zwei Höhen. Beim Abstieg wird dieselbe Folge umgekehrt benutzt.',638,384,500,body)
y=285
for h,t in [('Beispiel aus dem EG: 13 STG 15/30','13 Steigungen; 15 cm Steigungshöhe und 30 cm Auftritt im Plantext. Rechnerischer Höhenunterschied dieses Laufs: 13 × 15 cm = 195 cm. Das ist noch keine absolute Geschosshöhe.'),('19 STG 16,2/27 bei Stiege 5 und 6','Rechnerisch 19 × 16,2 cm = 307,8 cm, sofern die Beschriftung für den vollständigen Lauf gilt. Ob dessen Fußpunkt im UG liegt, muss ein Schnitt oder der Nachbarplan belegen.'),('Durchgezogen und gestrichelt','Die Original-Linienart beibehalten: Sichtbare und verdeckte Teile unterscheiden sich nach Plankonvention. Keine zusätzlichen gestrichelten Stufen erfinden. Die Farben dieser Schemazeichnung sind reine Lernhilfen.')]:
 y=para(c,h,45,y,1090,head);y=para(c,t,45,y-5,1090)-14
assert y>57,y
done()
page('Wann eine grüne Fläche wirklich ein Körperweg ist','G-PRÜFUNG / KONKRETE SCHRITTE FÜR CLAUDE CODE')
y=710
for h,t in [('1. Boden und Geschoss belegen','Nur eine Fläche mit passendem Boden kann einen Weg bilden. Hallendarstellungen mit UG-Höhenbezug nicht allein wegen des Blatttitels zu einer EG-Verbindung machen.'),('2. Hindernisse abziehen','Wandkörper, Stützen, feste Glasabschlüsse, Schächte und tatsächliche Einbauten vollständig berücksichtigen. Die grünen Lernflächen und roten Konturen sind keine exakt geprüfte Kollisionsgeometrie.'),('3. Öffnungen mit beiden Seiten verbinden','Ein Portal muss durch den Wandaufbau reichen und auf beiden Seiten an einen Bodenbereich anschließen. Türbögen bleiben Bewegungssymbole. Fenster mit Brüstung und technische Durchbrüche verbinden den Fußweg nicht.'),('4. Körperabstand berücksichtigen','Für eine konkrete Körperbreite die nutzbare Fläche um den benötigten Abstand zu Hindernissen verkleinern oder eine Körperhülle kollisionsfrei prüfen. Körpergröße und gewünschte Durchgangsbreite sind konfigurierbare Eingaben, keine aus der Farbe ablesbaren Werte.'),('5. Sackgassen im Verbindungsgraphen prüfen','Räume und Bereiche sind Knoten, belegte Portale sind Kanten. Ein Raum mit einem Anschluss ist ein Kandidat für einen Endbereich. Keine zusätzliche Kante durch seine Rückwand erfinden. Eine komplette Sackgassenliste setzt das vollständige Portalverzeichnis voraus.'),('6. Treppe als Höhenverbindung behandeln','Grundrissfläche, Stufenfolge, Podest, Laufrichtung und beide Endhöhen verbinden. Ein gezeichneter Pfeil allein gibt kein abgesichertes Zielgeschoss. Das EG-Paket lässt die Übergabe an UG/OG deshalb ausdrücklich offen.')]:
 y=para(c,h,42,y,1100,head);y=para(c,t,42,y-6,1100)-20
assert y>60,y
done()
page('Dateien, Belege und verbleibende Grenzen','ABSCHLUSS / REPRODUZIERBARE ÜBERGABE')
y=710
for h,t in [('Gleiche Originale','quellen/Schule_SH22_EG.pdf und die Original-DXF wurden unverändert übernommen. Das bestehende rote Gesamtblatt bleibt erhalten. Das neue Lernbuch ersetzt die vorige Fassung.'),('28 beschriftete Originalbeispiele','daten/04_BEISPIELE_EG.json enthält Ausschnitte, Texte und Bildpfade. daten/13_BILDANNOTATIONEN_EG.json beschreibt die farbigen Zeiger mit Zielkoordinaten. Die vier zusätzlichen Gehflächenausschnitte zeigen den grünen Gesamtplan vergrößert.'),('Grüne Flächen nachvollziehen','daten/12_GEHFLaECHEN_EG.geojson enthält interpretierte Bodenbereiche in PDF-Punkten. Herkunft, ausgeschlossene Merkmale und Grenzen stehen daneben. Die Flächen sind nicht trainingsfertig und nicht für lichte Breiten freigegeben.'),('Treppen abgleichen','Die sechs Anlagen-IDs der bestehenden Übergabedatei bleiben unverändert. Zielgeschoss und Endpunkthöhen bleiben bis zum Abgleich mit UG/OG oder Gebäudeschnitten unbekannt. Das seitliche Treppenschema ist keine vermessene Darstellung dieses Gebäudes.'),('Prüfung','PDF-Seiten werden gerendert und visuell kontrolliert; Paketdateien, Bildpfade und Prüfsummen werden geprüft. Die Rivoplan-Engine wurde nicht geändert oder ausgeführt. Es gibt keinen nachgewiesenen Erkennungsgewinn und keine Wegfreigabe.'),('Claude Code starten','00_START_HIER.md lesen. Danach den Arbeitsauftrag und die Datenverträge lesen. Erklärende Farblinien, Pfeile, Schließlagen und grüne Flächen dürfen nicht als ursprüngliche CAD-Geometrie eingelesen werden.')]:
 y=para(c,h,42,y,1100,head);y=para(c,t,42,y-6,1100)-20
assert y>60,y
done();c.save();print('BOOK_PAGES',n,flush=True)
# Mirror all new explanatory material and keep old technical rules/test specifications.
full=['# EG - überarbeitetes Lernwissen','Mauern, Türen, Fenster, grüne Bodenflächen, Sackgassen und Treppen. Gleiche Originalquelle wie v1.']
for l in lessons:
 full += ['## '+l['id']+' - '+l['title'],'!['+l['title']+']('+l['image']+')','Original-PDF, Seite 1. Suchbereich in pt: '+str(l['roi'])]
 for a,b in l['sections']:full+=['### '+a,b]
 full+=['### Direkt eingezeichnete Merkmale']+[f'- {a}: {b} (Farbe: {d})' for a,b,t,d in C[l['id']]]
full+=['## Gehflächen','![Grüner Gesamtplan](bilder/00b_EG_Gehflaechen_Gesamt.png)','Gänge sind flächig grün. Bodenbereiche sind manuell am Plan interpretiert. Erkannte Materialkonturen, feste Glasspannen, Liftschächte und geschlossene CAD-Einbaukonturen sind ausgespart. Offene Möbelumrisse können unvollständig sein. Keine exakt geprüfte Körperfreiraummaske.','## Sackgassen','IKT 0.21 illustriert einen Raum mit nur einem sichtbaren normalen Zugang. Betretbar, aber nicht zum Durchqueren geeignet. Kein vollständiges Sackgasseninventar: Dafür muss zuerst jedes Portal und jeder Außenanschluss geprüft werden.','## Treppen in Seitenansicht','Allgemeines Schema im Lernbuch: Höhe ergibt sich aus Steigung × Anzahl; horizontale Entwicklung aus Auftritten. 13 × 15 cm = 195 cm, 19 × 16,2 cm = 307,8 cm. Die absolute Lage zu EG/UG/OG bleibt ohne Schnitt oder Höhenbeleg offen. Durchgezogene und gestrichelte Originalstriche werden nicht durch erfundene Linientypen ersetzt.']
md('01_LERNWISSEN_EG.md','\n\n'.join(full))
md('00_START_HIER.md',f'''# SH22-LKS / EG - finales überarbeitetes Lernpaket

## Zuerst ansehen
1. `{BOOK}`: {n} Seiten. Erst roter Mauerplan, dann grüner Gehflächenplan, anschließend direkt beschriftete Originaldetails mit Farben und Pfeilen.
2. `plaene/Leopold_Kohr_Schule_EG_Mauern_rot_v1.pdf`: unveränderte große Maueransicht.
3. `plaene/{WALK}`: großer Gesamtplan mit flächigem Grün und schwarzen Originalstufen.

## Claude Code
`02_CLAUDE_AUFTRAG_EG.md` lesen, danach `01_LERNWISSEN_EG.md`, `11_DATENVERTRAG_EG.md` und `14_AENDERUNGEN_UND_GEHFLAECHEN.md`.

Die gleichen Originale liegen unter `quellen/`. 28 Beispiele mit {len(annotation_records)} beschrifteten Zeigern stehen in `daten/04_BEISPIELE_EG.json` und `daten/13_BILDANNOTATIONEN_EG.json`. Die vier zusätzlichen grünen Übersichten liegen unter `bilder/G-A.png` bis `G-D.png`.

`daten/12_GEHFLaECHEN_EG.geojson` verwendet Original-PDF-Punkte mit Ursprung links oben; die rote GeoJSON verwendet lokale DXF-Millimeter. Nie ohne Transformation vermischen.

## Prüfen
`python3 skripte/pruefe_paket.py` prüft das Paket. Das ist kein Raumerkennungstest. Die 20 vorhandenen Prüffälle sind weiterhin Spezifikationen, nicht ausgeführt.

## Grenzen
Die Zeichnungen vermitteln Erkennungsmerkmale. Rote Umrandungen und grüne Flächen sind keine millimetergenaue Ground-Truth. Möbelkonturen können unvollständig sein. Höhenanschlüsse der Treppen und reale Türzustände bleiben offen. Keine vollständige Sackgasseninventur, keine Wegfreigabe, keine Engine-Ausführung.
''')
md('14_AENDERUNGEN_UND_GEHFLAECHEN.md','''# Änderungen gegenüber v1

- Rotes Ausgangsblatt und Originaldateien unverändert übernommen.
- Alle 26 bisherigen Beispiele erhalten direkt zugeordnete Farbpfeile und Beschriftungen; zwei zusätzliche Mauer-Nahaufnahmen.
- Türbeispiel mit farbigem Türblatt, Viertelbogen, Bandpunkt, Portal und ausdrücklich ergänzter gestrichelter Schließlage.
- Fensterrahmen, Fensterbögen und Brüstungshöhen direkt bezeichnet.
- Grüner Gesamtplan statt einzelner grüner Routenlinie; vier große Bereichsausschnitte.
- Schwarze Original-Stufenkanten über der grünen Füllung, erläuterte Treppenbrüche und Laufsymbole.
- Allgemeines Grundriss-/Seitenansicht-Schema einer Treppe, eindeutig als nicht gebäudespezifisch gekennzeichnet.

## Gehflächen als Interpretation
Die grüne Füllung bedeutet: im Plan als Bodenbereich interpretiert. Sie ist kein Nachweis, dass jede grüne Stelle mit einer beliebigen Körperbreite betreten werden kann. Wände, Schächte, feste Glasabschnitte und geschlossene Einbaukonturen wurden ausgespart. Aus offenen CAD-Linienzügen können unvollständige Möbelhindernisse entstehen. Sporthallen bleiben wegen ungeklärtem EG-Bodenniveau ocker markiert. Ungefärbte Außenflächen wurden nicht als zusammenhängende Außenwege geprüft.

## Sackgassen
Das Beispiel IKT 0.21 ist direkt markiert. Ein vollständiges Inventar aller Sackgassen ist ohne vollständige Portal- und Außenanschlussprüfung nicht belegt. Claude soll alle Portalverbindungen als Graph prüfen, offene Zustände kennzeichnen und einen Endraum nicht als unbetretbar klassifizieren.

## Treppen
Querlinien sind Stufen, nicht einzelne Raumwände. Die Lauflinie und Pfeilspitze beschreiben die Plankonvention. Blatt-unten bedeutet nicht Höhen-abwärts. Zielgeschoss, Endhöhen und Richtung nur aus Schnitt, Planlegende, Höhenkoten und Nachbargeschoss gemeinsam bestätigen. Das Lernschema erklärt den Zusammenhang zwischen Grundriss und Höhenverlauf; es ersetzt keinen Gebäudeschnitt.
''')
p=ROOT/'02_CLAUDE_AUFTRAG_EG.md';s=p.read_text().replace('Die grüne Linie ist ein lokales Anschauungsbeispiel und kein freigegebener Fluchtweg.','Die grünen Flächen sind interpretierte Bodenbereiche, keine exakte Körperfreiraummaske. Pfeile, Markierungen und gedachte Schließlagen sind Kommentare und keine Original-CAD-Bauteile.');p.write_text(s+'\n\n## Ergänzung der überarbeiteten Fassung\nLies `14_AENDERUNGEN_UND_GEHFLAECHEN.md` und `daten/13_BILDANNOTATIONEN_EG.json`. Verwende die Bildpfeile zum Auffinden konkreter Merkmale. Prüfe Portalverbindungen und Körperabstände am Original, bevor grüne Bereiche zu echten Routen werden.\n')
p=ROOT/'11_DATENVERTRAG_EG.md';p.write_text(p.read_text()+'\n\n## Revision: grüne Flächen und Bildpfeile\n`12_GEHFLaECHEN_EG.geojson`: PDF-Punkte, Ursprung links oben, Originalblatt 5227 × 3727 pt. `13_BILDANNOTATIONEN_EG.json`: visuelle Zeigerziele im selben System. Rote Wandkonturen bleiben DXF-mm. Beide sind illustrative Geometrie. Kein automatischer Import als Trainingsmaske.\n')
src=json.loads((ROOT/'daten/08_QUELLEN_EG.json').read_text());src['display_changes']=['Elektrische Überlagerungen ausgeblendet','Architektur abgedunkelt','Unveränderte rote Lernkonturen','Direkte farbige Merkmal-Linien, Textkarten und Pfeile','Grüne interpretierte Bodenflächen mit ausgesparten Hindernissen; Originalstufen schwarz'];js('daten/08_QUELLEN_EG.json',src)
# New examples join the already established rules.
rules=json.loads((ROOT/'daten/03_REGELN_EG.json').read_text())
for r in rules['rules']:r['examples']=[l['id'] for l in lessons if r['id'] in l['rules']]
js('daten/03_REGELN_EG.json',rules)
# Durable authoring records; original hand-curated masks and annotations remain available.
shutil.copy2(TMP/'annotation_data.py',ROOT/'skripte/annotation_data.py')
md('skripte/README.md','''# Werkzeuge
`pruefe_paket.py` prüft alle Dateien anhand des Manifests und die Beispiel-Bildbezüge.
`lese_beispiel.py EG-09` zeigt das jeweilige Originalbeispiel.
`baue_lernbuch.py` baut eine lesbare Alternativfassung aus den fertigen Bildern und Textdaten; das ausgelieferte Final-PDF ist die visuell geprüfte Hauptfassung.
`annotation_data.py` enthält die kuratierten Pfeiltexte und normierten Zielpunkte. JSON mit absoluten Original-PDF-Koordinaten steht unter daten/13_BILDANNOTATIONEN_EG.json.
''')
# Replace stale old 31-page narrative validation record.
md('10_PRUEFBERICHT_EG.md',f'''# Prüfung der überarbeiteten Fassung

{n} PDF-Seiten; 28 annotierte Originalbeispiele; {len(annotation_records)} direkt beschriftete Pfeile; vier zusätzliche grüne Ausschnitte und eine allgemeine Treppen-Seitenansicht.

Dateipfade, JSON-Verknüpfungen, Originalprüfsummen, PDF-Textgrenzen und gerenderte Seiten werden vor Auslieferung geprüft. `PRUEFUNG.json` dokumentiert die abschließenden technischen Paketprüfungen.

Keine Rivoplan-Engine ausgeführt. Keine Aussage über Erkennungsquote. Keine vollständige Objekt- oder Sackgasseninventur. Keine Wegfreigabe.
''')
# Portable alternative book builder from included images and JSON, without external scratch dependencies.
shutil.copy2(ROOT/BOOK,OUT/BOOK);shutil.copy2(ROOT/'plaene'/WALK,OUT/WALK)
print('FINISHED',ROOT,flush=True)
