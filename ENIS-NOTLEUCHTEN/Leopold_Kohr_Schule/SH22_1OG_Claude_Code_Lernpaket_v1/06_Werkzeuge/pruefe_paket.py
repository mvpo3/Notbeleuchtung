"""Check the package itself. Does NOT evaluate an engine or prove room accuracy."""
import argparse,json,gzip,sys
from pathlib import Path,PurePosixPath
from common import ROOT,read,sha256,write_report
def validate():
    errors=[];expected={}
    for line in (ROOT/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        digest,rel=line.split('  ',1)
        rp=PurePosixPath(rel)
        if rp.is_absolute() or '..' in rp.parts or rel in expected:
            errors.append('Unsafe/duplicate manifest path: '+rel);continue
        expected[rel]=digest
        path=ROOT/rel
        if path.is_symlink() or not path.is_file():errors.append('Missing/nonregular: '+rel)
        elif sha256(path)!=digest:errors.append('Checksum mismatch: '+rel)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.name not in ['SHA256SUMS.txt','.DS_Store']}
    if actual!=set(expected):errors.append('Inventory mismatch: '+str(sorted(actual.symmetric_difference(expected))))
    for rel in expected:
        try:
            if rel.endswith('.json'):read(rel)
            elif rel.endswith('.json.gz'):
                with gzip.open(ROOT/rel,'rt',encoding='utf-8') as f:json.load(f)
        except Exception as e:errors.append(f'Invalid JSON {rel}: {e}')
    cases=read('04_Daten/lernfaelle.json')['cases'];ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)):errors.append('Duplicate learning case ID')
    for c in cases:
        if not all(1<=n<=61 for n in c['book_pages']):errors.append('Invalid page: '+c['id'])
        if len(c['crop_pdf_pt'])!=4:errors.append('Invalid crop: '+c['id'])
    for r in read('04_Daten/regeln.json')['rules']:
        if any(x not in ids for x in r['examples']):errors.append('Unresolved rule case: '+r['id'])
    tests=read('04_Daten/prueffaelle.json')['tests']
    if len({t['id'] for t in tests})!=len(tests):errors.append('Duplicate regression ID')
    for t in tests:
        if t['case'] not in ids:errors.append('Unresolved regression case: '+t['id'])
    for f in read('04_Daten/quellen.json')['files']:
        if not (ROOT/f['path']).is_file() or sha256(ROOT/f['path'])!=f['sha256']:
            errors.append('Source/PDF changed: '+f['path'])
    for f in read('MANIFEST.json')['files']:
        if expected.get(f['path'])!=f['sha256']:errors.append('Manifest disagreement: '+f['path'])
    return {'check':'package_integrity_and_cross_references','passed':not errors,
            'checked_files':len(expected),'learning_cases':len(cases),'regression_probes':len(tests),
            'engine_tested':False,'errors':errors}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',help='Report outside the package')
    a=p.parse_args()
    try:r=validate()
    except Exception as e:r={'passed':False,'engine_tested':False,'errors':[str(e)]}
    write_report(r,a.out);sys.exit(0 if r['passed'] else 1)
