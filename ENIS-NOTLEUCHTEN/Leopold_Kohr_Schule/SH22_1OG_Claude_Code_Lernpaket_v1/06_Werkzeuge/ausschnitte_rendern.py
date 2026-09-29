"""Render one original plan crop and the matching explained book page."""
import argparse
from pathlib import Path
import fitz
from common import ROOT,read
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--dpi',type=int,default=144)
    a=p.parse_args();cases={c['id']:c for c in read('04_Daten/lernfaelle.json')['cases']}
    if a.case not in cases:p.error('Unknown case; use an ID from lernfaelle.json')
    if not 72<=a.dpi<=400:p.error('DPI must be between 72 and 400')
    c=cases[a.case];a.out.mkdir(parents=True,exist_ok=True);scale=fitz.Matrix(a.dpi/72,a.dpi/72)
    with fitz.open(ROOT/'02_Originalquellen/Schule_SH22_1_OG.pdf') as d:
        d[0].get_pixmap(matrix=scale,clip=fitz.Rect(c['crop_pdf_pt'])).save(a.out/(a.case+'_Original.png'))
    with fitz.open(ROOT/'01_PDF/SH22_1OG_Lernbuch.pdf') as d:
        d[c['book_pages'][-1]-1].get_pixmap(matrix=scale).save(a.out/(a.case+'_Erklaerung.png'))
    print('Original and explanation saved:',a.out.resolve())
