"""Registration between this exact source DXF and its PDF, not a metric survey."""
import argparse
from common import read,write_report
def transform(x,y,direction):
    a=read('04_Daten/koordinaten.json')['parameters']
    if direction=='cad_to_pdf':return [a['ox']+a['sx']*x,a['oy']-a['sy']*y]
    return [(x-a['ox'])/a['sx'],(a['oy']-y)/a['sy']]
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('direction',choices=['cad_to_pdf','pdf_to_cad'])
    p.add_argument('x',type=float);p.add_argument('y',type=float)
    a=p.parse_args();write_report({'direction':a.direction,'point':transform(a.x,a.y,a.direction)})
