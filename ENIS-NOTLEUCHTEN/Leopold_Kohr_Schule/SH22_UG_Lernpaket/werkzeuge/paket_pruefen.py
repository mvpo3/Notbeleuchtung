#!/usr/bin/env python3
"""Checks package integrity and references. Does not test room-recognition code."""
from pathlib import Path
import hashlib, json, re, sys

root=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
def fail(message):raise AssertionError(message)
manifest=read('MANIFEST.json')
for item in manifest['files']:
    p=root/item['path']
    assert p.is_file(),f'Missing: {item["path"]}'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],f'Hash differs: {item["path"]}'
    assert p.stat().st_size==item['bytes'],f'Size differs: {item["path"]}'
for p in root.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
crops=read('daten/ausschnitte.json')['crops']
for c in crops:
    x0,y0,x1,y1=c['clip_pdf_points']
    assert 0<=x0<x1<=4651 and 0<=y0<y1<=3205,c['id']
    for k in ['source_pdf','original_png','marked_png']:assert (root/c[k]).is_file(),c[k]
cases=read('daten/lernfaelle.json')['cases']
ids=[c['id'] for c in cases]
assert len(ids)==len(set(ids))
assert set(ids)=={x['id'] for x in read('pruefung/erwartungen.json')['cases']}
for c in cases:
    assert c['floor']=='UG'
    assert c['implementation_test_run'] is False
    assert (root/c['lesson_file']).is_file()
    assert c['id'] in {x['id'] for x in crops}
    assert (root/c['annotated_image']).is_file(),c['id']
    assert 1<=c['book_page']<c['annotated_book_page']<=54,c['id']
annotations=read('daten/bildmarkierungen.json')['annotations']
assert {a['case_id'] for a in annotations}==set(ids)
assert len(annotations)==len(cases)==19
by_id={c['id']:c for c in cases}
for a in annotations:
    assert (root/a['image']).is_file(),a['case_id']
    assert a['book_page']==by_id[a['case_id']]['annotated_book_page']
    for label in a['callouts']:
        assert all(0<=v<=1 for v in label['target']),a['case_id']
green_crops=read('daten/gruene_ausschnitte.json')
assert (root/green_crops['source_pdf']).is_file()
assert len(green_crops['crops'])==8
for c in green_crops['crops']:
    assert (root/c['image']).is_file(),c['id']
    x0,y0,x1,y1=c['clip_pdf_points']
    assert 0<=x0<x1<=4651 and 0<=y0<y1<=3205,c['id']
assert len(read('daten/gruene_flaechen.json')['dead_end_examples'])==6
for path in root.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        if not target.startswith(('https:','http:','#')):
            assert (path.parent/target.split('#')[0]).exists(),f'{path.name}: {target}'
window=read('daten/fensterstatus.json')
assert window['confirmed_window_annotations']==[]
assert read('daten/wegebeispiel.json')['body_clearance_verified'] is False
print(json.dumps({'result':'passed','files_hashed':len(manifest['files']),'learning_cases':len(cases),'annotated_cases':len(annotations),'crop_references':len(crops),'green_crops':8,'source_floor':'UG','scope':'Package integrity and references only; no model or repository execution.'},ensure_ascii=False,indent=2))
