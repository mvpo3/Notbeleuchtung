#!/usr/bin/env python3
"""Optional full Draft 2020-12 validation using jsonschema."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    try:from jsonschema import Draft202012Validator
    except ImportError:
        print('Optionale Bibliothek jsonschema fehlt. Paketprüfung ist ohne sie möglich.',file=sys.stderr);return 2
    def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
    pairs=load('07_Schemata/zuordnung.json')['validations'];errors=[]
    for p in (ROOT/'07_Schemata').glob('*.schema.json'):Draft202012Validator.check_schema(load(p.relative_to(ROOT)))
    for pair in pairs:
        validator=Draft202012Validator(load(pair['schema']))
        errors.extend([pair['data']+' '+str(list(e.path))+': '+e.message for e in validator.iter_errors(load(pair['data']))])
    print(json.dumps({'passed':not errors,'validated_files':len(pairs),'errors':errors},ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
