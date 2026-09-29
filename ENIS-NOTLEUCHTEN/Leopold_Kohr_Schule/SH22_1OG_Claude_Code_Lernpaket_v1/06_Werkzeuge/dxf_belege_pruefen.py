"""Check source handles, text and DXF-to-PDF registration on explicit anchors."""
import argparse,math,sys
import ezdxf
from common import ROOT,read,sha256,write_report
from koordinaten import transform
def run():
    source=ROOT/'02_Originalquellen/20220225-SH22-LKS-GE-AP-01-01-A-1OG.dxf'
    meta=read('04_Daten/koordinaten.json');errors=[]
    if sha256(source)!=meta['source_dxf_sha256']:
        return {'passed':False,'errors':['Source SHA-256 mismatch']}
    d=ezdxf.readfile(source);anchors=read('04_Daten/quellanker.json');maximum=0
    for a in anchors['anchors']:
        e=d.entitydb.get(a['handle'])
        if e is None or e.dxftype()!='LINE':errors.append('Missing LINE '+a['handle']);continue
        for key,point in [('pdf_a',e.dxf.start),('pdf_b',e.dxf.end)]:
            error=math.dist(transform(point.x,point.y,'cad_to_pdf'),a[key]);maximum=max(maximum,error)
            if error>1e-6:errors.append('Registration mismatch '+a['handle'])
    for a in anchors['text_assertions']:
        e=d.entitydb.get(a['handle'])
        if e is None or e.dxftype()!='MTEXT' or e.plain_text().strip()!=a['expected_text']:
            errors.append('Source text mismatch '+a['handle'])
    if d.header.get('$INSUNITS')!=meta['dxf_header_INSUNITS']:errors.append('Unit header changed')
    return {'passed':not errors,'line_anchors':len(anchors['anchors']),
      'text_anchors':len(anchors['text_assertions']),'max_registration_error_pdf_pt':maximum,
      'header_INSUNITS':d.header.get('$INSUNITS'),'metric_dimensions_independently_verified':False,
      'engine_tested':False,'errors':errors}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out');a=p.parse_args()
    r=run();write_report(r,a.out);sys.exit(0 if r['passed'] else 1)
