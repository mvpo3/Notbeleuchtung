#!/usr/bin/env python3
"""Erklärrahmen und Originalbögen aus den gespeicherten Koordinaten rendern.

Ohne Argument werden die 21 in Revision 4 bearbeiteten Details erneuert.
Die übrigen gelieferten Detailbilder bleiben erhalten. --vector erzeugt alle
29 Details als gemeinsame PDF mit Vektorlinien und eingebetteten Schriften.
"""
from pathlib import Path
import json
import math
import sys
import fitz

ROOT = Path(__file__).resolve().parents[1]
COL = {'red': (.82,.06,.15), 'blue': (.02,.34,.77),
       'orange': (.84,.36,.02), 'purple': (.47,.19,.65),
       'green': (.02,.51,.26), 'ink': (.08,.16,.20)}
GREEN_IDS = {'EG-15','EG-16','EG-17','EG-19','EG-20','EG-21',
             'EG-22','EG-23','EG-24','EG-25','EG-26'}

def main():
    data = json.loads((ROOT/'daten/13_BILDANNOTATIONEN_EG.json').read_text())
    lessons = json.loads((ROOT/'daten/04_BEISPIELE_EG.json').read_text())['examples']
    changed = {v['example_id'] for v in data['closed_frames'] + data['source_arc_highlights']}
    vector = '--vector' in sys.argv
    selected = set(sys.argv[1:]) - {'--vector'}
    selected = selected or ({l['id'] for l in lessons} if vector else changed)
    assert selected <= ({l['id'] for l in lessons} if vector else changed)
    vector_document = fitz.open() if vector else None
    docs = {
        'walls': fitz.open(ROOT/'plaene/Leopold_Kohr_Schule_EG_Mauern_rot_v1.pdf'),
        'clean': fitz.open(ROOT/'plaene/EG_Architekturbasis_Lernansicht.pdf'),
        'green': fitz.open(ROOT/'plaene/EG_Gehflaechen_Basis.pdf')}
    boldfont = fitz.Font(fontfile=str(ROOT/'skripte/fonts/DejaVuSans-Bold.ttf'))
    normalfont = fitz.Font(fontfile=str(ROOT/'skripte/fonts/DejaVuSans.ttf'))
    for lesson in lessons:
        ident = lesson['id']
        if ident not in selected:
            continue
        roi = fitz.Rect(lesson['roi'])
        src = docs['green' if ident in GREEN_IDS else 'walls' if lesson['base']=='walls' else 'clean']
        doc = vector_document if vector else fitz.open()
        pg = doc.new_page(width=1400,height=960)
        pg.insert_font(fontname='dv',fontfile=str(ROOT/'skripte/fonts/DejaVuSans.ttf'))
        pg.insert_font(fontname='dvb',fontfile=str(ROOT/'skripte/fonts/DejaVuSans-Bold.ttf'))
        pg.draw_rect(pg.rect,fill=(.967,.98,.985),color=None)
        area = fitz.Rect(224,80,1176,880)
        scale = min(area.width/roi.width,area.height/roi.height)
        w,h = roi.width*scale,roi.height*scale
        dst = fitz.Rect(700-w/2,480-h/2,700+w/2,480+h/2)
        pg.draw_rect(dst+(-2,-2,2,2),fill=(1,1,1),color=(.76,.8,.82),width=1)
        pg.show_pdf_page(dst,src,0,clip=roi)
        def uv(x,y):return (dst.x0+x*dst.width,dst.y0+y*dst.height)
        def ap(x,y):return (dst.x0+(x-roi.x0)*scale,dst.y0+(y-roi.y0)*scale)
        def line(points,color,width=3.1,closed=False):
            shape = pg.new_shape()
            shape.draw_polyline(points)
            shape.finish(color=COL[color],width=width,closePath=closed,lineJoin=0)
            shape.commit()
        for color,points in data['line_highlights_normalized'].get(ident,[]):
            line([uv(*p) for p in points],color)
        if ident=='EG-09':
            # Bereits in der vorherigen Fassung vorhandene didaktische Türmarkierungen.
            cx,cy,r = 1414.58,1086.05,51.023
            pg.draw_line(ap(cx,cy),ap(cx,cy-r),color=COL['blue'],width=3.8)
            line([ap(cx+r*math.cos(t),cy+r*math.sin(t))
                  for t in [-math.pi/2+i*math.pi/2/60 for i in range(61)]],'orange',3.8)
            pg.draw_line(ap(cx,cy),ap(cx+r,cy),color=COL['purple'],width=3.5,dashes='[7 5] 0')
            pg.draw_line(ap(cx,cy+5),ap(cx+r,cy+5),color=COL['green'],width=4)
            pg.draw_circle(ap(cx,cy),5,color=COL['blue'],fill=(1,1,1),width=2)
        for curve in data['source_arc_highlights']:
            if curve['example_id']==ident:
                line([ap(*p) for p in curve['points']],curve['color'],3.6)
        for frame in data['closed_frames']:
            if frame['example_id']==ident:
                line([ap(*p) for p in frame['polygon_pdf_pt']],frame['color'],3.5,True)
        annotations = [a for a in data['annotations'] if a['example_id']==ident]
        for j,a in enumerate(annotations):
            side,row = j%2,j//2
            x,y = (10 if side==0 else 1188),75+row*265
            col = a['color']
            pg.draw_rect(fitz.Rect(x,y,x+200,y+174),fill=(1,1,1),color=COL[col],width=1.5)
            for text,box,font,size in [
                (a['heading'],(x+12,y+11,x+188,y+68),'dvb',19),
                (a['explanation'],(x+12,y+71,x+188,y+164),'dv',17.5)]:
                ff = boldfont if font=='dvb' else normalfont
                size = min(size,172/max(ff.text_length(word,fontsize=1) for word in text.split()))
                ret = pg.insert_textbox(fitz.Rect(box),text,fontname=font,fontsize=size,
                                        color=COL[col if font=='dvb' else 'ink'],lineheight=1.13)
                assert ret >= 0, (ident,text,ret)
            endpoint = ap(*a['target_pdf_pt'])
            start = (x+200 if side==0 else x,y+139)
            pg.draw_line(start,endpoint,color=COL[col],width=2)
            dx,dy = endpoint[0]-start[0],endpoint[1]-start[1]
            norm = math.hypot(dx,dy); ux,uy = dx/norm,dy/norm
            points = [endpoint,(endpoint[0]-10*ux+4.5*uy,endpoint[1]-10*uy-4.5*ux),
                      (endpoint[0]-10*ux-4.5*uy,endpoint[1]-10*uy+4.5*ux)]
            sh = pg.new_shape();sh.draw_polyline(points)
            sh.finish(color=COL[col],fill=COL[col],closePath=True);sh.commit()
            pg.draw_circle(endpoint,4.8,color=COL[col],fill=(1,1,1),width=2)
        pg.insert_text((235,33),ident+' | Originalausschnitt mit direkt zugeordneten Merkmalen',
                       fontname='dvb',fontsize=21,color=COL['ink'])
        pg.insert_text((235,932),'Rahmen: erklärter Bereich. Farblinien: Originalmerkmale. Pfeile: Zuordnung.',
                       fontname='dv',fontsize=18,color=COL['ink'])
        if not vector:
            pg.get_pixmap(matrix=fitz.Matrix(1.75,1.75)).save(ROOT/'bilder'/f'{ident}.png')
            doc.close()
        print('DETAIL',ident,flush=True)
    if vector:
        target=ROOT/'plaene/EG_Erklaerte_Details_Vektor.pdf'
        vector_document.subset_fonts()
        vector_document.save(target,garbage=4,deflate=True)
        vector_document.close()
        print('VECTOR_PANELS',target,flush=True)
    for doc in docs.values():doc.close()

if __name__=='__main__':main()
