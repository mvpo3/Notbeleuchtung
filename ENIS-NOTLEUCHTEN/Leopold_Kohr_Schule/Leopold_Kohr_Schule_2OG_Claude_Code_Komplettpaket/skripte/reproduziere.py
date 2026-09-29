#!/usr/bin/env python3
"""Rebuild learning diagrams in _build/ and reproduziert/. No production detector."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    for name in ['extrahiere_dxf.py','bereite_geometrie_vor.py','baue_lernbuch.py']:
        print('Starte '+name,flush=True)
        subprocess.run([sys.executable,str(ROOT/'skripte'/name)],cwd=ROOT,check=True)
    print('Lernansichten reproduziert: '+str(ROOT/'reproduziert'))
    print('Die freigegebenen PDFs unter pdf/ wurden nicht verändert.')
if __name__=='__main__':main()
