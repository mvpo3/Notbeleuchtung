#!/usr/bin/env python3
"""Finales Lernbuch mit originalen Vektorplänen und Vektorbeschriftungen setzen."""
from pathlib import Path
import json,fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'_neu_erstellt';TARGET.mkdir(exist_ok=True)
BOOK='Leopold_Kohr_Schule_EG_Lernbuch_final.pdf'
WALK='Leopold_Kohr_Schule_EG_Gehflaechen_gruen.pdf'
font=ROOT/'skripte/fonts/DejaVuSans.ttf';bold=font.with_name('DejaVuSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('DV',str(font)));pdfmetrics.registerFont(TTFont('DVB',str(bold)))
walk=fitz.open(ROOT/'plaene'/WALK)
lessons=json.loads((ROOT/'daten/04_BEISPIELE_EG.json').read_text())['examples']
# Book: use large pages so callout text remains readable at normal zoom.
PAGE=(1190.55,841.89);INK=colors.HexColor('#15333d');TEAL=colors.HexColor('#087f72')
body=ParagraphStyle('body',fontName='DV',fontSize=12,leading=17,textColor=INK)
small=ParagraphStyle('small',parent=body,fontSize=9.5,leading=13)
head=ParagraphStyle('head',parent=body,fontName='DVB',fontSize=13.5,leading=18,textColor=TEAL)
def para(c,t,x,y,w,style=body):
 p=Paragraph(t,style);_,h=p.wrap(w,1000);p.drawOn(c,x,y-h);return y-h
placements=[]
panel_page={l['id']:i for i,l in enumerate(lessons)}
green_rois={'G-A':[890,900,2465,1890],'G-B':[2410,800,3590,2340],
 'G-C':[3430,1400,5160,2870],'G-D':[0,3110,730,3727]}
layout_path=TARGET/'_layout.pdf'
n=0;c=canvas.Canvas(str(layout_path),pagesize=PAGE,pageCompression=1);c.setTitle('EG Lernbuch - scharfe Vektorpläne mit Erklärrahmen');c.setAuthor('Rivoplan | SH22-LKS | EG')
def page(title,tag):
 global n;n+=1
 c.setFillColor(INK);c.rect(0,827,1191,15,fill=1,stroke=0)
 c.setFont('DVB',11);c.setFillColor(TEAL);c.drawString(32,799,tag)
 c.setFont('DVB',25);c.setFillColor(INK);c.drawString(32,763,title)
 c.setFont('DV',9);c.drawString(32,24,'RIVOPLAN | Leopold-Kohr-Schule | EG | Nach deinen Seitenkorrekturen überarbeitet | 21.09.2026');c.drawRightString(1157,24,f'{n:02}')
 c.setStrokeColor(colors.HexColor('#cadadf'));c.line(32,51,1157,51)
def img(path,x,y,w,h):
 stem=Path(path).stem
 if stem=='00_EG_Mauern_Gesamt':source='plaene/Leopold_Kohr_Schule_EG_Mauern_rot_v1.pdf';pno=0;clip=None;a,b=5227,3727
 elif stem=='00b_EG_Gehflaechen_Gesamt':source='plaene/'+WALK;pno=0;clip=None;a,b=5227,3727
 elif stem in panel_page:source='plaene/EG_Erklaerte_Details_Vektor.pdf';pno=panel_page[stem];clip=None;a,b=1400,960
 elif stem in green_rois:source='plaene/EG_Gehflaechen_Basis.pdf';pno=0;clip=green_rois[stem];a,b=1100,760
 else:raise ValueError('Kein Vektorbezug: '+str(path))
 f=min(w/a,h/b);dw,dh=a*f,b*f;left=x+(w-dw)/2;bottom=y+(h-dh)/2
 placements.append((n-1,source,pno,[left,PAGE[1]-bottom-dh,left+dw,PAGE[1]-bottom],clip))
def done():c.showPage()
page('Erdgeschoss: Mauern sind rot markiert.','01 / DER AUSGANGSPLAN BLEIBT ERHALTEN')
img(ROOT/'bilder/00_EG_Mauern_Gesamt.png',30,90,1128,654)
para(c,'Rot umfasst die erkennbaren Mauerkörper und massiven Pfeiler. Auf den Detailseiten erhält jedes erklärte Wandstück einen geschlossenen Rahmen und einen zugeordneten Pfeil.',32,77,1124,small);done()
page('Erdgeschoss: Boden- und Gehbereiche flächig grün','02 / GESAMTPLAN MIT TREPPEN UND SACKGASSEN-BEISPIEL')
img(ROOT/'bilder/00b_EG_Gehflaechen_Gesamt.png',30,90,1128,654)
para(c,'Grün zeigt interpretierte Bodenflächen. Schwarz erhält die Stufenkanten. Ocker markiert ungeklärte EG-Bodenhöhe. Die große Plan-PDF liegt zusätzlich unter plaene/.',32,77,1124,small);done()
page('Was Farben, Rahmen und Pfeile bedeuten','03 / LESEREGELN')
y=710
for h,t in [('Rahmen + Pfeil: welches Wandstück ist gemeint?','Ein geschlossener farbiger Rechteckrahmen umfasst das erklärte Wandstück. Der Pfeil verbindet es mit der Beschriftung. Bei schrägen Wänden ist der Rahmen mitgedreht. Die Rahmen sind Lernmarkierungen; ihre Kanten sind keine zusätzlichen Mauern.'),('Rot: fester Wandkörper','Zwei Begrenzungen, Materialdarstellung und Anschlüsse gemeinsam lesen. Auch breite Außenaufbauten, dünne Trennwände und massive Stützen versperren einen Durchgang.'),('Blau / Orange / Violett: Merkmal am Original','Blau hebt häufig eine Kante, einen Rahmen oder ein Türblatt hervor. Orange zeigt Bogen, Richtung oder Beleg. Violett kennzeichnet feste Glasabschlüsse, Höhenbezüge oder eine ausdrücklich gedachte Schließlage. Jeder Pfeil hat seine eigene Beschriftung.'),('Grün: Bodenfläche und Verbindung','Die Gänge sind flächig eingefärbt. Raum- und Treppenböden werden ebenfalls sichtbar. Wandkonturen, Schächte, feste Glasabschnitte und erkennbare Möbel- und Einbaukonturen sind ausgespart. Die markierten Möbel und Waschbecken sind zusätzlich ausgespart. Lichte Breiten und reale Türzustände benötigen weiterhin eine eigene Prüfung.'),('Sackgasse: hinein möglich, durchgehen nicht','Ein Raum mit nur einem Zugang kann betreten werden. Am geschlossenen Wandende geht es nicht weiter; zurück führt derselbe Zugang. Das ist etwas anderes als eine völlig unzugängliche Fläche.'),('Treppen: Grundriss und Höhe zusammen lesen','Schwarze Querlinien sind Stufen. Laufpfeile und Bruchlinien bleiben erhalten. Ob ein konkreter Anschluss ins UG oder OG führt, wird erst durch Schnitte, Höhen und den Plan des Nachbargeschosses bestätigt.'),('Original und Lernmarkierung trennen','Alle Planbeispiele stammen aus derselben EG-DXF/PDF wie zuvor. Nur die allgemeine Treppen-Seitenansicht ist ein ausdrücklich bezeichnetes Schema. Markierungen und Bodenflächen sind Lerninterpretationen, keine millimetergenaue Trainingsmaske.')]:
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
 tip='Geschlossene Rahmen umfassen den erklärten Bereich. Pfeile ordnen den Text zu; farbige Linien heben die Originalmerkmale hervor.'
 if l['id']=='EG-29':tip='Die Kabine ist über ihre Türseite zugänglich. Schacht und Technikabstände ergeben keinen frei begehbaren Ring um die Kabine.'
 if l['id']=='EG-09':tip='Gedachte Schließlage ist violett gestrichelt. Sie wurde zum Erklären ergänzt. DL 90/220 bleibt eine Planangabe; Türzustand und nutzbare Breite gesondert prüfen.'
 if l['id'] in ['EG-20','EG-21','EG-22','EG-23','EG-24','EG-25']:tip='Grün zeigt den Lauf-/Bodenbereich, Schwarz die Originalstufen. Der Laufpfeil ist kein Ersatz für belegte Geschosshöhen.'
 para(c,tip,35,120,772,small)
 para(c,'Quelle: Schule_SH22_EG.pdf, Seite 1 | Ausschnitt '+l['id']+' | PDF-Suchbereich '+str(l['roi'])+' pt.',35,75,1110,small)
 done()
# Dedicated walk detail pages, with large green areas and source-scale labels.
for ident,title,roi,description in [
 ('G-A','Gehflächen: Verwaltung und geschlossene Raumenden',[890,900,2465,1890],'Die umlaufende Erschließung um den Kopierraum ist grün. Durch die Türöffnungen gelangt man in die angrenzenden Räume. IKT 0.21 hat nur einen sichtbaren normalen Zugang: hinein und auf demselben Weg zurück. Grün wird an Wandkörpern unterbrochen; es überspringt keine Fenster.'),
 ('G-B','Gehflächen: Windfang, Eingangshalle und Anschlüsse',[2410,800,3590,2340],'Die Eingangshalle bleibt auch unter dem gezeichneten Deckenrechteck grün. Die Linien des Deckenbauteils schneiden den Boden nicht in einzelne Räume. Feste Glasfelder sind keine Durchgänge. Verbindungen an Schiebetüren gelten bei geöffneter Tür.'),
 ('G-C','Gehflächen: Nebenräume, Speiseraum und Treppen',[3430,1400,5160,2870],'Bodenflächen und Erschließung sind grün. Tisch-, Sitzmöbel- und Einbaukonturen sind als Hindernisse ausgespart; die schwarzen Originalumrisse bleiben sichtbar. Die Treppen behalten ihre Stufen. Weiß bedeutet hier: ausgespart oder ungeklärt, nicht pauschal unzugänglich.'),
 ('G-D','Gehflächen: separat dargestelltes Nebengebäude',[0,3110,730,3727],'Auch im schräg gezeichneten Nebengebäude sind Bodenbereiche grün. Die drei markierten Einzelmöbel, die länglichen Einbauten, Waschbecken und WC-Gegenstände sind weiß ausgespart. Schwarze Originalkonturen bleiben erkennbar; grün ist der Boden dazwischen. Türöffnungen sind lokale Zugänge. Ein Außenweg zum Hauptgebäude lässt sich aus der versetzten Blattdarstellung nicht ableiten.')]:
 d=fitz.open();pp=d.new_page(width=1100,height=760);pp.show_pdf_page(pp.rect,walk,0,clip=fitz.Rect(roi));f=ROOT/'bilder'/f'{ident}.png';None;d.close()
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
for h,t in [('Gleiche Originale','quellen/Schule_SH22_EG.pdf und die Original-DXF wurden unverändert übernommen. Das bestehende rote Gesamtblatt bleibt erhalten. Das neue Lernbuch ersetzt die vorige Fassung.'),('29 beschriftete Originalbeispiele','daten/04_BEISPIELE_EG.json enthält Ausschnitte, Texte und Bildpfade. daten/13_BILDANNOTATIONEN_EG.json enthält 120 Zeiger, 38 geschlossene Erklärrahmen und 11 zusätzlich farbig nachgezogene Originalbögen mit Quell-Handles. Die vier zusätzlichen Gehflächenausschnitte zeigen den grünen Gesamtplan vergrößert.'),('Grüne Flächen nachvollziehen','daten/12_GEHFLaECHEN_EG.geojson enthält interpretierte Bodenbereiche in PDF-Punkten. Herkunft, ausgeschlossene Merkmale und Grenzen stehen daneben. Die Flächen sind nicht trainingsfertig und nicht für lichte Breiten freigegeben.'),('Treppen abgleichen','Die sechs Anlagen-IDs der bestehenden Übergabedatei bleiben unverändert. Zielgeschoss und Endpunkthöhen bleiben bis zum Abgleich mit UG/OG oder Gebäudeschnitten unbekannt. Das seitliche Treppenschema ist keine vermessene Darstellung dieses Gebäudes.'),('Prüfung','PDF-Seiten werden gerendert und visuell kontrolliert; Paketdateien, Bildpfade und Prüfsummen werden geprüft. Die Rivoplan-Engine wurde nicht geändert oder ausgeführt. Es gibt keinen nachgewiesenen Erkennungsgewinn und keine Wegfreigabe.'),('Claude Code starten','00_START_HIER.md lesen. Danach den Arbeitsauftrag und die Datenverträge lesen. Erklärende Rechteckrahmen, Farblinien, Pfeile, Schließlagen und grüne Flächen dürfen nicht als ursprüngliche CAD-Geometrie eingelesen werden.')]:
 y=para(c,h,42,y,1100,head);y=para(c,t,42,y-6,1100)-20
assert y>60,y
done();c.save()
book=fitz.open(layout_path);sources={}
for page_number,source,pno,rect,clip in placements:
 if source not in sources:sources[source]=fitz.open(ROOT/source)
 book[page_number].show_pdf_page(fitz.Rect(rect),sources[source],pno,
  clip=fitz.Rect(clip) if clip else None)
assert all(len(p.get_images())==0 for p in book),'Gerasterte Bilddaten im Vektor-Lernbuch'
book.subset_fonts();book.save(TARGET/BOOK,garbage=4,deflate=True)
for source in sources.values():source.close()
book.close();layout_path.unlink();print('BOOK_PAGES',n,'VECTOR_PLACEMENTS',len(placements),flush=True)

print(TARGET/BOOK)
