#!/usr/bin/env python3
"""Render a stored learning reference; not a recognition engine output."""
import argparse,base64,html,json,textwrap,math
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
COLORS={'red':'#D11121','blue':'#1267B6','purple':'#841FAC','orange':'#BF5904','cyan':'#008594','green':'#006E3B','gray':'#57666E'}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('example');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    try:import fitz
    except ImportError:
        print('Optionale Bibliothek PyMuPDF fehlt.',file=sys.stderr);return 2
    def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
    examples={e['example_id']:e for e in load('04_Daten/lernbeispiele.json')['examples']}
    if args.example not in examples:ap.error('Unbekannte Beispiel-ID')
    e=examples[args.example];features={f['feature_id']:f for f in load('04_Daten/linienbelege.json')['features']}
    x0,y0,x1,y1=e['view_crop_xyxy'];width,height=x1-x0,y1-y0;scale=min(830/width,700/height)
    origin=[30+(830-width*scale)/2,150+(700-height*scale)/2]
    def xy(p):return origin[0]+(p[0]-x0)*scale,origin[1]+(p[1]-y0)*scale
    notes=[];y=164
    for f in e['features']:
        lines=textwrap.wrap(f['title'],56)+['']+textwrap.wrap(f['explanation'],65)
        notes.append((f,lines,y));y+=len(lines)*20+28
    h=max(910,y+45);svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1540" height="{h}" viewBox="0 0 1540 {h}">', '<rect width="100%" height="100%" fill="white"/>', '<style>text{font-family:Arial,sans-serif;fill:#193440}</style>',f'<text x="30" y="42" font-family="DejaVu Sans,sans-serif" font-size="25" font-weight="bold">{html.escape(e["title"])}</text>',f'<text x="30" y="78" font-family="DejaVu Sans,sans-serif" font-size="16">Quellenbeleg · PDF {e["pdf_pages"]} · kein Engine-Ergebnis · Koordinaten plan_norm_2000</text>']
    doc=fitz.open(ROOT/'02_Originale/Schule_SH22_3_OG.pdf');rect=fitz.Rect(x0,y0,x1,y1)*(4268/2000)
    pix=doc[0].get_pixmap(matrix=fitz.Matrix(scale*2000/4268*1.8,scale*2000/4268*1.8),clip=rect,alpha=False)
    data=base64.b64encode(pix.tobytes('png')).decode();doc.close()
    svg.append(f'<image x="{origin[0]}" y="{origin[1]}" width="{width*scale}" height="{height*scale}" href="data:image/png;base64,{data}"/>')
    for f,lines,ny in notes:
        detail=features[f['feature_id']];color=COLORS[f['color']];dash=' stroke-dasharray="6 4"' if detail['dashed'] else ''
        for tr in detail['traces']:
            pp=[xy(p) for p in tr['points']]
            if tr['kind']=='cubic_bezier':
                cmd='M '+','.join(map(str,pp[0]))+' C '+' '.join(','.join(map(str,p)) for p in pp[1:])
            else:cmd='M '+' L '.join(','.join(map(str,p)) for p in pp)
            svg.append(f'<path d="{cmd}" fill="none" stroke="{color}" stroke-width="2.6"{dash}/>')
        if detail['point_marker_xy']:
            px,py=xy(detail['point_marker_xy']);svg.append(f'<circle cx="{px}" cy="{py}" r="5" stroke="{color}" fill="none" stroke-width="2.6"/>')
        tx,ty=xy(detail['arrow_target_xy']);sx,sy=888,ny-6;marker='a'+f['feature_id']
        svg.append(f'<defs><marker id="{marker}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{color}"/></marker></defs>')
        svg.append(f'<path d="M{sx},{sy} L{tx},{ty}" stroke="{color}" stroke-width="1" fill="none"/>')
        length=math.hypot(tx-sx,ty-sy)
        if length>0:
            ux,uy=(tx-sx)/length,(ty-sy)/length
            points=[(tx,ty),(tx-9*ux+3.5*uy,ty-9*uy-3.5*ux),(tx-9*ux-3.5*uy,ty-9*uy+3.5*ux)]
            coords=' '.join(str(a)+','+str(b) for a,b in points)
            svg.append(f'<polygon points="{coords}" fill="{color}"/>')
        svg.append(f'<line x1="914" x2="955" y1="{ny-24}" y2="{ny-24}" stroke="{color}" stroke-width="4"/>')
        for k,line in enumerate(lines):svg.append(f'<text x="914" y="{ny+k*20}" font-family="DejaVu Sans,sans-serif" font-size="16">{html.escape(line)}</text>')
    svg.append(f'<text x="30" y="{h-24}" font-family="DejaVu Sans,sans-serif" font-size="14">Original-PDF bleibt unverändert. Markierte Originalrechtecke sind Bauteilgeometrie; keine ergänzten Suchkästen.</text></svg>')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text('\n'.join(svg),encoding='utf-8');print(args.output);return 0
if __name__=='__main__':raise SystemExit(main())
