#!/usr/bin/env python3
"""Paketkonsistenz prüfen. Führt KEINE Raumerkennung aus."""
from pathlib import Path
import json, hashlib, sys

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 errors=[]; checks=[]
 def check(ok,msg):
  (checks if ok else errors).append(msg)
 sources=read('daten/08_QUELLEN_EG.json')
 for s in sources['sources']:
  p=ROOT/s['path'];check(p.is_file(),f"Quelle vorhanden: {s['path']}")
  if p.is_file():check(digest(p)==s['sha256'],f"Originalprüfsumme: {s['path']}")
 rules=read('daten/03_REGELN_EG.json')['rules']; examples=read('daten/04_BEISPIELE_EG.json')['examples']
 tests=read('daten/05_PRUEFFAELLE_EG.json')['tests'];stairs=read('daten/07_TREPPEN_UEBERGABE_EG.json')['stairs']
 rids={r['id'] for r in rules};eids={e['id'] for e in examples};tids={t['id'] for t in tests}
 check(len(rids)==len(rules)==27,'27 eindeutige Regel-IDs')
 check(len(eids)==len(examples)==29,'29 eindeutige Beispiel-IDs')
 check(len(tids)==len(tests)==20,'20 eindeutige Prüffall-IDs')
 check(len(stairs)==6,'Sechs Treppenanlagen')
 for e in examples:
  check(set(e['rules'])<=rids,f"Regelbezüge: {e['id']}")
  check((ROOT/e['image']).is_file(),f"Bild vorhanden: {e['id']}")
  x0,y0,x1,y1=e['roi'];check(0<=x0<x1<=5227 and 0<=y0<y1<=3727,f"Suchbereich innerhalb Originalseite: {e['id']}")
  check(e['geometry_type']=='Suchbereich_keine_Objektgrenze',f"Suchbereich korrekt bezeichnet: {e['id']}")
 for r in rules:check(set(r['examples'])<=eids and len(r['examples'])>0,f"Regel hat reale Beispiele: {r['id']}")
 for t in tests:
  check(t['example_id'] in eids and t['rule_id'] in rids,f"Prüffallbezüge: {t['id']}")
  check(t['status']=='Spezifikation_nicht_ausgefuehrt',f"Kein erfundener Teststatus: {t['id']}")
 for s in stairs:
  check(s['example_id'] in eids,f"Treppenbeleg: {s['anlage_id']}")
  check(s['verbindung_bestaetigt'] is False and s['zielgeschoss'] is None,f"Offener Höhenanschluss: {s['anlage_id']}")
 wall=read('daten/06_MAUER_MARKIERUNGEN_EG.geojson')
 check(wall['coordinate_reference']['unit']=='mm' and not wall['coordinate_reference']['georeferenced'],'Lokale Millimeter statt Geo-Koordinaten')
 for f in wall['features']:
  check(not f['properties']['produktiv_importieren'] and not f['properties']['ground_truth'],f"Lernkontur ohne Sollgeometrie-Freigabe: {f['id']}")
 annotation_data=read('daten/13_BILDANNOTATIONEN_EG.json')
 anns=annotation_data['annotations']
 for a in anns:
  check(a['example_id'] in eids,'Pfeilbezug: '+a['example_id'])
  x,y=a['target_pdf_pt'];check(0<=x<=5227 and 0<=y<=3727,'Pfeilziel im Originalblatt: '+a['example_id'])
 frames=annotation_data['closed_frames'];frame_by_id={f['id']:f for f in frames}
 check(len(frames)==len(frame_by_id)==38,'38 eindeutige geschlossene Erklärrahmen')
 for f in frames:
  points=f['polygon_pdf_pt']
  check(f['example_id'] in eids and len(points)==5 and points[0]==points[-1],f"Geschlossener Vierseitenrahmen: {f['id']}")
  check(all(0<=x<=5227 and 0<=y<=3727 for x,y in points),f"Rahmen innerhalb Originalblatt: {f['id']}")
  check(f['role']=='Erklaerrahmen_keine_Objektgrenze',f"Rahmen korrekt als Lernmarkierung bezeichnet: {f['id']}")
  check(all(any(a['example_id']==f['example_id'] and a['heading']==h and f['id'] in a.get('frame_ids',[]) for a in anns) for h in f['headings']),f"Rahmen mit Textzuordnung: {f['id']}")
 for a in anns:
  for fid in a.get('frame_ids',[]):
   check(fid in frame_by_id and frame_by_id[fid]['example_id']==a['example_id'],'Gültiger Pfeil-Rahmen-Bezug: '+fid)
 curves=annotation_data['source_arc_highlights']
 check(len(curves)==11,'11 zusätzliche Originalbogen-Nachzeichnungen')
 for c in curves:
  check(c['example_id'] in eids and len(c['points'])>2 and c['type']=='ELLIPSE' and bool(c['handle']),f"Quellbogen mit Bezug und Handle: {c['example_id']}/{c['handle']}")
  check(all(0<=x<=5227 and 0<=y<=3727 for x,y in c['points']),f"Quellbogen innerhalb Originalblatt: {c['handle']}")
 greens=read('daten/12_GEHFLaECHEN_EG.geojson')['features']
 for g in greens:check(not g['properties']['ground_truth'],'Grün ist Lerninterpretation: '+g['id'])
 # Optional file-format checks. Their absence is visible in the report.
 optional=[]
 try:
  import fitz
  for file,n in [('Leopold_Kohr_Schule_EG_Lernbuch_final.pdf',39),('plaene/Leopold_Kohr_Schule_EG_Gehflaechen_gruen.pdf',1),('plaene/Leopold_Kohr_Schule_EG_Mauern_rot_v1.pdf',1),('plaene/EG_Erklaerte_Details_Vektor.pdf',29)]:
   d=fitz.open(ROOT/file);check(len(d)==n,f"PDF-Seitenzahl {file}: {n}")
   check(all(len(pg.get_images())==0 for pg in d),f"Vektorausgabe ohne Rasterbilder: {file}")
   d.close()
 except ImportError:optional.append('PDF-Prüfung nicht ausgeführt: PyMuPDF fehlt')
 try:
  from PIL import Image
  for e in examples:
   with Image.open(ROOT/e['image']) as im:im.verify()
  check(True,'Alle 29 Beispielbilder lesbar')
 except ImportError:optional.append('Bildprüfung nicht ausgeführt: Pillow fehlt')
 if (ROOT/'PRUEFSUMMEN.txt').exists():
  for line in (ROOT/'PRUEFSUMMEN.txt').read_text().splitlines():
   h,p=line.split('  ',1);target=ROOT/p
   check(target.is_file() and digest(target)==h,f"Paketprüfsumme: {p}")
 report={'kind':'Paketkonsistenzpruefung','engine_tests_executed':False,
 'result':'bestanden' if not errors else 'fehlgeschlagen','checks_passed':len(checks),
 'checks':checks,'errors':errors,'optional_not_run':optional,
 'meaning':'Nur Dateistruktur und Bezüge geprüft; kein Nachweis korrekter Raumerkennung.'}
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
