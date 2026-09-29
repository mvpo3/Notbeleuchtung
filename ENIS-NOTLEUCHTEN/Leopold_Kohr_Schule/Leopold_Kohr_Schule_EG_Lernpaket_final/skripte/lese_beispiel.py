#!/usr/bin/env python3
"""Quellengebundenen Suchbereich anzeigen, ohne eine Engine zu behaupten."""
from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:raise SystemExit('Aufruf: python3 skripte/lese_beispiel.py EG-09')
sources=json.loads((ROOT/'daten/08_QUELLEN_EG.json').read_text())
for s in sources['sources']:
 if hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()!=s['sha256']:
  raise SystemExit('Quellprüfsumme stimmt nicht: '+s['path'])
examples=json.loads((ROOT/'daten/04_BEISPIELE_EG.json').read_text())['examples']
matches=[e for e in examples if e['id']==sys.argv[1]]
if not matches:raise SystemExit('Unbekannte Beispiel-ID')
print(json.dumps(matches[0],ensure_ascii=False,indent=2))
