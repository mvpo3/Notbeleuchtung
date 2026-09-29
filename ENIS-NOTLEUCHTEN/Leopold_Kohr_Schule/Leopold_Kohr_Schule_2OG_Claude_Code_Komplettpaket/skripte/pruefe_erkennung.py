#!/usr/bin/env python3
"""Validate result format and references; this is not recognition-quality scoring."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
def validate_result(data):
    import jsonschema
    schema=json.loads((ROOT/'schemata/ERKENNUNGSERGEBNIS.schema.json').read_text(encoding='utf-8'))
    errors=[e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(data)]
    if errors:return errors
    objects={o['id']:o for o in data['objects']}
    if len(objects)!=len(data['objects']):errors.append('Objekt-IDs sind nicht eindeutig.')
    ids=[c['id'] for c in data['connections']]
    if len(set(ids))!=len(ids):errors.append('Verbindungs-IDs sind nicht eindeutig.')
    aids=[a['example_id'] for a in data['assessments']]
    if len(set(aids))!=len(aids):errors.append('Beispielbewertungen sind nicht eindeutig.')
    expected={e['id'] for e in json.loads((ROOT/'daten/03_BEISPIELE.json').read_text(encoding='utf-8'))['examples']}
    if set(aids)!=expected:errors.append('Alle 25 Beispiele müssen mit einem Status aufgeführt werden.')
    for o in data['objects']:
        g=o['geometry'];polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates'] if g['type']=='MultiPolygon' else []
        for poly in polys:
            for ring in poly:
                if ring[0]!=ring[-1]:errors.append(o['id']+': Polygonring ist nicht geschlossen.')
    for c in data['connections']:
        for field in ['from_object','to_object','via_object']:
            if c[field] is not None and c[field] not in objects:errors.append(c['id']+': unbekannte Referenz '+field)
        if c['from_object']==c['to_object']:errors.append(c['id']+': identische Enden.')
        if c['status']=='rejected' and c['walkable'] is True:errors.append(c['id']+': abgelehnte Verbindung ist nicht zugleich begehbar.')
        via=objects.get(c['via_object'])
        if c['status']=='confirmed' and via and via['kind']!=c['kind']:errors.append(c['id']+': bestätigte Verbindung und via-Bauteilklasse passen nicht zusammen.')
        if c['status']=='confirmed' and c['kind'] in ['stairs','elevator'] and (c['target_floor'] is None or c['height_delta_m'] is None):errors.append(c['id']+': bestätigter Höhenwechsel benötigt Zielgeschoss und Höhendifferenz.')
    status=data['run']['status']
    if status=='nicht_ausgefuehrt':
        if data['objects'] or data['connections']:errors.append('Nicht ausgeführte Vorlage darf keine erkannten Objekte/Verbindungen behaupten.')
        if any(a['outcome']!='nicht_geprueft' for a in data['assessments']):errors.append('Nicht ausgeführte Vorlage darf keine bewerteten Engine-Ergebnisse enthalten.')
    if status=='ausgefuehrt':
        for field in ['engine_name','executed_at','command']:
            if not data['run'][field]:errors.append('Ausgeführter Lauf benötigt '+field+'.')
    return errors
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('file',type=Path);a=ap.parse_args()
    try:
        d=json.loads(a.file.read_text(encoding='utf-8'));errors=validate_result(d)
    except (ValueError,ImportError,OSError) as e:
        print(str(e),file=sys.stderr);return 2
    print(json.dumps({'format_ok':not errors,'run_status':d.get('run',{}).get('status'),'errors':errors,'quality_verified':False,'note':'Formatprüfung ist kein Nachweis korrekter Räume oder Wege.'},ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
