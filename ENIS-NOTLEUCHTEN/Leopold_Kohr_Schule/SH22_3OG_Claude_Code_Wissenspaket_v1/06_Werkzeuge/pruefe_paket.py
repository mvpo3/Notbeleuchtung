#!/usr/bin/env python3
"""Offline integrity and internal consistency checks; no engine invocation."""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()
def main():
    errors=[]
    def check(ok,msg):
        if not ok:errors.append(msg)
    try:
        m=load('MANIFEST.json'); paths=set()
        for item in m['files']:
            name=item['path'];p=ROOT/name
            check(name not in paths,'Doppelter Dateieintrag: '+name);paths.add(name)
            check(p.is_file(),'Datei fehlt: '+name)
            if p.is_file():
                check(p.stat().st_size==item['bytes'],'Dateigröße abweichend: '+name)
                check(digest(p)==item['sha256'],'SHA-256 abweichend: '+name)
        sums={}
        for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
            value,name=line.split('  ',1);sums[name]=value
        check(set(sums)==paths|{'MANIFEST.json'},'SHA256SUMS-Inventar stimmt nicht.')
        for name,value in sums.items():
            p=ROOT/name
            if p.is_file():check(digest(p)==value,'Prüfsumme stimmt nicht: '+name)
        examples=load('04_Daten/lernbeispiele.json')['examples'];ex={e['example_id']:e for e in examples}
        check(len(examples)==len(ex)==32,'Es müssen 32 eindeutige Lernbeispiele sein.')
        index=load('04_Daten/seitenindex.json')['pages']
        check([p['page'] for p in index]==list(range(1,88)),'Seitenindex nicht 1..87.')
        features=load('04_Daten/linienbelege.json')['features'];byid={f['feature_id']:f for f in features}
        check(len(features)==len(byid)==134,'Es müssen 134 eindeutige Merkmale sein.')
        declared={f['feature_id'] for e in examples for f in e['features']}
        check(declared==set(byid),'Merkmale in Text und Geometrie stimmen nicht überein.')
        for e in examples:
            a,z=e['pdf_pages'];check(1<=a<z<=87,'Ungültige Seiten '+e['example_id'])
            check(index[a-1]['example_id']==index[z-1]['example_id']==e['example_id'],'Falscher Seitenverweis '+e['example_id'])
            check((ROOT/e['knowledge_file']).is_file(),'MD fehlt '+e['example_id'])
            x0,y0,x1,y1=e['view_crop_xyxy'];check(0<=x0<x1<=2000 and 0<=y0<y1<=1384,'Ausschnitt außerhalb '+e['example_id'])
            check(bool(e['reasoning']) and bool(e['unknown_properties']),'Begründung/offener Punkt fehlt '+e['example_id'])
        for f in features:
            check(f['example_id'] in ex,'Merkmal verweist auf unbekannten Fall.')
            pts=[f['arrow_target_xy']]
            if f['point_marker_xy']:pts.append(f['point_marker_xy'])
            for t in f['traces']:
                check(t['kind'] in ('polyline','cubic_bezier'),'Unbekannte Kurvenart.')
                check(len(t['points'])==4 if t['kind']=='cubic_bezier' else len(t['points'])>=2,'Ungültige Kurvenpunkte.')
                check(t['origin'] in ('original_pdf_path','manual_teaching_mark'),'Unbekannte Markierungsherkunft.')
                pts.extend(t['points'])
            check(all(len(p)==2 and 0<=p[0]<=2000 and 0<=p[1]<=1384 for p in pts),'Beleg außerhalb des Plans: '+f['feature_id'])
        rules=load('04_Daten/erkennungsregeln.json')['rules'];cases=load('05_Pruefung/akzeptanzfaelle.json')['cases'];opens=load('04_Daten/offene_punkte.json')['items']
        for name,rows in [('Regeln',rules),('Sollfälle',cases),('Offene Punkte',opens)]:
            check(len(rows)==32 and {r['example_id'] for r in rows}==set(ex),name+' sind unvollständig.')
        check(all(c['evaluation_status']=='not_run' and c['expected_claims'] for c in cases),'Sollfälle enthalten unzulässigen Ergebnisstatus.')
        template=load('05_Pruefung/ergebnis_vorlage.json')
        check({r['case_id'] for r in template['results']}=={c['case_id'] for c in cases},'Vorlage enthält andere Fälle.')
        check(all(r['status']=='not_run' and r['claims']=={} for r in template['results']),'Vorlage behauptet einen ausgeführten Lauf.')
        sources=load('04_Daten/quellen.json')['sources'];sd={s['source_id']:s for s in sources}
        for s in sources:check(digest(ROOT/s['path'])==s['sha256'],'Quellenhash falsch '+s['source_id'])
        check(sd['LEHRBUCH']['sha256']=='108f4c5b5524baf6673cce3a75e2007598db25f5511a6771e4be785bfea6d040','Freigegebene PDF verändert.')
        check(load('04_Daten/linienbelege.json')['source_hash']==sd['ORIGINAL_PDF']['sha256'],'Markierungen gehören zu anderer Quelle.')
        fr=load('04_Daten/dxf_textfragmente.json')['fragments'];check(len(fr)==2774 and len({t['fragment_id'] for t in fr})==2774,'Textfragmente fehlen/doppelt.')
        for p in ROOT.rglob('*.json'):
            if '__pycache__' not in p.parts:json.loads(p.read_text(encoding='utf-8'))
    except (OSError,ValueError,KeyError,TypeError,IndexError) as exc:errors.append(str(exc))
    print(json.dumps({'passed':not errors,'errors':errors,'scope':'Paketkonsistenz, keine Software-Erkennungsleistung'},ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
