#!/usr/bin/env python3
"""Verify this package's checksums, source binding and learning-data links."""
from pathlib import Path
import argparse,json,hashlib,sys,re,datetime
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--erweitert',action='store_true');ap.add_argument('--bericht',type=Path)
    args=ap.parse_args();errors=[];checks=0
    def check(ok,message):
        nonlocal checks;checks+=1
        if not ok:errors.append(message)
    manifest=read('MANIFEST.json');files=manifest['files']
    paths=[x['path'] for x in files];check(len(set(paths))==len(paths),'Doppelte Manifestpfade.')
    for item in files:
        p=ROOT/item['path'];check(p.resolve().is_relative_to(ROOT.resolve()),'Unsicherer Pfad '+item['path'])
        check(p.is_file(),'Fehlt: '+item['path'])
        if p.is_file():check(sha(p)==item['sha256'],'Hashabweichung: '+item['path'])
    sums=ROOT/'PRUEFSUMMEN.txt'
    if sums.exists():
        for line in sums.read_text(encoding='utf-8').splitlines():
            if not line:continue
            expected,rel=line.split('  ',1);p=ROOT/rel
            check(p.resolve().is_relative_to(ROOT.resolve()),'Unsicherer Prüfsummenpfad '+rel)
            check(p.is_file() and sha(p)==expected,'Prüfsumme falsch: '+rel)
    for rel in paths:
        if rel.endswith(('.json','.geojson')):
            try:read(rel);check(True,'JSON '+rel)
            except (ValueError,OSError) as e:check(False,'JSON '+rel+': '+str(e))
    for source in read('daten/01_QUELLEN.json')['sources']:
        check(sha(ROOT/source['path'])==source['sha256'],'Quellenbindung '+source['path'])
    examples=read('daten/03_BEISPIELE.json')['examples'];anns=read('daten/04_ANNOTATIONEN.json')['annotations'];frames=read('daten/05_ERKLAERRAHMEN.geojson')['features'];ids={e['id'] for e in examples}
    check(len(examples)==25 and len(ids)==25,'25 eindeutige Beispiele erwartet.')
    check(len(anns)==100 and len(frames)==100,'100 Annotationen/Rahmen erwartet.')
    amap={a['id']:a for a in anns};fmap={f['id']:f for f in frames}
    for i,e in enumerate(examples):
        check(e['book_page']==i+7,'Buchseite falsch: '+e['id'])
        check(e['detail_page']==i+1,'Detailseite falsch: '+e['id'])
        check(len(e['annotations'])==4,'Vier Erklärungen erwartet: '+e['id'])
        check(e['ground_truth'] is False,'Beispiel darf keine exakte Maske behaupten.')
        for key in ['source_pdf','source_dxf','book_pdf','detail_pdf','image']:check((ROOT/e[key]).is_file(),'Beispielpfad fehlt: '+e[key])
        for ident in e['annotations']:
            check(ident in amap and ident in fmap,'Erklärung fehlt: '+ident)
            if ident in fmap:
                ring=fmap[ident]['geometry']['coordinates'][0];check(len(ring)==5 and ring[0]==ring[-1],'Rahmen nicht geschlossen: '+ident)
    raw_arcs={a['handle'] for a in read('daten/roh/arcs.json')}
    for e in examples:
        for t in e['traces']:
            if t['type']=='arc':check(t['source_handle'] in raw_arcs,'Bogenhandle fehlt: '+str(t['source_handle']))
    cases=read('daten/11_PRUEFFAELLE.json')['cases'];check({c['example_id'] for c in cases}==ids,'Prüffälle unvollständig.')
    # Follow relative Markdown links; directory links are allowed.
    for rel in paths:
        if rel.endswith('.md'):
            text=(ROOT/rel).read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)]+)\)',text):
                if '://' in target or target.startswith('#'):continue
                p=(ROOT/rel).parent/target.split('#',1)[0];check(p.exists(),'Defekter Link in '+rel+': '+target)
    if args.erweitert:
        import fitz
        from shapely.geometry import shape
        from pruefe_erkennung import validate_result
        pdfs={x['path']:x.get('pages') for x in files if x['path'].endswith('.pdf')}
        for name,count in pdfs.items():
            with fitz.open(ROOT/name) as d:
                check(len(d)==count,'PDF-Seitenzahl falsch: '+name)
                check(not any(p.get_images() for p in d),'Rasterbild in Vektor-PDF: '+name)
        for rel in paths:
            if rel.endswith('.geojson'):
                d=read(rel);fs=d['features'] if d.get('type')=='FeatureCollection' else [d]
                for f in fs:
                    g=shape(f['geometry'] if f.get('type')=='Feature' else f);check(g.is_valid and not g.is_empty,'Ungültige/leere Geometrie in '+rel)
        errs=validate_result(read('vorlagen/ERGEBNIS_VORLAGE.json'));check(not errs,'Ergebnisvorlage: '+str(errs))
    result={'status':'bestanden' if not errors else 'fehlgeschlagen','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'file_count_manifest':len(files),'examples':len(examples),'closed_frames':len(frames),'extended':args.erweitert,'recognition_engine_run':False,'recognition_quality_verified':False,'errors':errors}
    if args.bericht:
        target=args.bericht if args.bericht.is_absolute() else ROOT/args.bericht;target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
