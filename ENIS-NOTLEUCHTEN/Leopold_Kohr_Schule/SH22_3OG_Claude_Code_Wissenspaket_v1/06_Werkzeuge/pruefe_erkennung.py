#!/usr/bin/env python3
"""Checks actual adapter reports. Does not run or simulate the recognition engine."""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def exact(actual,expected):
    if isinstance(expected,bool):
        return isinstance(actual,bool) and actual is expected
    if isinstance(expected,(int,float)):
        return isinstance(actual,(int,float)) and not isinstance(actual,bool) and actual==expected
    return type(actual) is type(expected) and actual==expected

def evaluate(report,cases,sources):
    errors=[]; outcomes=[]; seen=set()
    if not isinstance(report,dict):
        return {'passed':False,'errors':['Bericht muss ein JSON-Objekt sein.'],'cases':[]}
    if report.get('schema_version')!='1.0.0':errors.append('schema_version fehlt oder ist unbekannt.')
    for k in ('run_id','engine_revision'):
        if not isinstance(report.get(k),str) or not report[k].strip():errors.append(k+' fehlt; kein nachgewiesener Engine-Lauf.')
    hashes=report.get('source_hashes',{})
    if not isinstance(hashes,dict):hashes={};errors.append('source_hashes ist kein Objekt.')
    for s in sources:
        if s['source_id'] in ('ORIGINAL_PDF','ORIGINAL_DXF') and hashes.get(s['source_id'])!=s['sha256']:
            errors.append('Quellenhash stimmt nicht: '+s['source_id'])
    expected={c['case_id']:c for c in cases}
    rows=report.get('results',[])
    if not isinstance(rows,list):rows=[];errors.append('results muss eine Liste sein.')
    for row in rows:
        if not isinstance(row,dict):errors.append('Fall ist kein Objekt.');continue
        cid=row.get('case_id')
        if not isinstance(cid,str) or cid not in expected:errors.append('Unbekannter Fall: '+str(cid));continue
        if cid in seen:errors.append('Doppelter Fall: '+cid);continue
        seen.add(cid);faults=[]
        if row.get('status')!='observed':faults.append('Nicht ausgeführt/beobachtet.')
        claims=row.get('claims',{});ev=row.get('evidence_by_claim',{})
        if not isinstance(claims,dict):claims={};faults.append('claims muss ein Objekt sein.')
        if not isinstance(ev,dict):ev={};faults.append('evidence_by_claim muss ein Objekt sein.')
        for key,want in expected[cid]['expected_claims'].items():
            if key not in claims:faults.append('Aussage fehlt: '+key)
            elif not exact(claims[key],want):faults.append(f'{key}: gemeldet {claims[key]!r}, erwartet {want!r}')
            evidence=ev.get(key)
            valid=False
            if isinstance(evidence,list):
                for item in evidence:
                    if not isinstance(item,dict):continue
                    if item.get('source_id') not in ('ORIGINAL_PDF','ORIGINAL_DXF'):continue
                    if all(isinstance(item.get(k),str) and len(item[k].strip())>=8 for k in ('source_locator','engine_reference','explanation')):
                        valid=True
            if not valid:faults.append('Konkreter Quellen-/Engine-Beleg fehlt: '+key)
        outcomes.append({'case_id':cid,'passed':not faults,'errors':faults})
    for cid in expected:
        if cid not in seen:outcomes.append({'case_id':cid,'passed':False,'errors':['Fall fehlt.']})
    good=sum(x['passed'] for x in outcomes)
    return {'passed':not errors and good==len(expected),'expected_cases':len(expected),'reported_cases':len(rows),'passed_cases':good,'failed_or_unrun_cases':len(expected)-good,'errors':errors,'cases':outcomes,'scope':'Prüfung gemeldeter Aussagen und Belegstruktur; keine unabhängige Verifikation der Geometrie oder Wahrheit der Belegtexte.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('report',type=Path);args=ap.parse_args()
    try:
        result=evaluate(read(args.report),read(ROOT/'05_Pruefung/akzeptanzfaelle.json')['cases'],read(ROOT/'04_Daten/quellen.json')['sources'])
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(str(exc),file=sys.stderr);return 1
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
