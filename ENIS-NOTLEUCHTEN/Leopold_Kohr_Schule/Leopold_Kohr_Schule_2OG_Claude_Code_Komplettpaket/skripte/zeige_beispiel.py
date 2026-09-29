#!/usr/bin/env python3
"""Show one learning example and nearby original CAD text. No recognition run."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('id',nargs='?',help='z.B. D01; ohne ID: Liste aller Beispiele')
    ap.add_argument('--text-limit',type=int,default=70)
    args=ap.parse_args()
    examples=json.loads((ROOT/'daten/03_BEISPIELE.json').read_text(encoding='utf-8'))['examples']
    if not args.id:
        print('\n'.join(f"{e['id']}: {e['title']} (Buch S. {e['book_page']})" for e in examples));return
    hits=[e for e in examples if e['id']==args.id.upper()]
    if not hits:ap.error('Unbekannte Beispiel-ID.')
    e=hits[0];x0,y0,x1,y1=e['roi_pdf_pt']
    texts=json.loads((ROOT/'daten/roh/texts_pdf.json').read_text(encoding='utf-8'))
    near=[t for t in texts if x0<=t['u']<=x1 and y0<=t['v']<=y1]
    anns=json.loads((ROOT/'daten/04_ANNOTATIONEN.json').read_text(encoding='utf-8'))['annotations']
    result={'example':e,'annotations':[a for a in anns if a['example_id']==e['id']],'nearby_original_text_count':len(near),'nearby_original_texts':near[:max(0,args.text_limit)],'note':'Räumliche Nähe ist ein Suchhinweis; Textzuordnung zusätzlich konstruktiv prüfen.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
