"""Evaluate selected learning probes, not all rooms or overall product readiness."""
import argparse,json,sys,math
from pathlib import Path
from shapely.geometry import shape,Point,LineString
from jsonschema import Draft202012Validator
from common import read,write_report

def evaluate(result,case=None):
    errors=sorted(Draft202012Validator(read('05_Schemas/engine_ergebnis.schema.json')).iter_errors(result),
                  key=lambda e:str(list(e.path)))
    if errors:raise ValueError('Schema: '+'; '.join(str(list(e.path))+': '+e.message for e in errors[:8]))
    suite=read('04_Daten/prueffaelle.json')
    if result['source_dxf_sha256']!=suite['source_dxf_sha256']:raise ValueError('Wrong source DXF hash')
    features=result['features'];known={f['id'] for f in features}
    if len(known)!=len(features):raise ValueError('Duplicate feature IDs')
    shapes={}
    for f in features:
        g=shape(f['geometry'])
        if g.is_empty or not g.is_valid or not all(math.isfinite(x) for x in g.bounds):
            raise ValueError('Invalid geometry: '+f['id'])
        if f['class'] in ['wall','room','walkable_area','furniture'] and g.geom_type not in ['Polygon','MultiPolygon']:
            raise ValueError('Area geometry required: '+f['id'])
        shapes[f['id']]=g
    if len({p['id'] for p in result['portals']})!=len(result['portals']):raise ValueError('Duplicate portal IDs')
    for p in result['portals']:
        if len(set(p['connects']))!=2 or any(x not in known for x in p['connects']):
            raise ValueError('Portal needs two distinct, existing adjacent area IDs: '+p['id'])
        if any(next(f for f in features if f['id']==x)['class'] not in ['room','walkable_area'] for x in p['connects']):
            raise ValueError('Portal references a non-area feature: '+p['id'])
        if math.dist(*p['segment'])==0:raise ValueError('Zero-length portal: '+p['id'])
    def at(f,p):
        g=shapes[f['id']];q=Point(p)
        return g.covers(q) or (g.geom_type in ['LineString','MultiLineString'] and g.distance(q)<=.5)
    def classified(cl):return [f for f in features if f['class']==cl and f['evidence']['status']!='uncertain']
    results=[]
    tests=[t for t in suite['tests'] if case is None or t['case']==case]
    if not tests:raise ValueError('No probes for selected case')
    for t in tests:
        kind=t['kind'];observed=None
        if kind=='walkable_at':
            observed=any(at(f,t['point']) for f in classified('walkable_area'))
            passed=observed==t['expected']
        elif kind=='class_at':
            observed=any(at(f,t['point']) for f in classified(t['expected_class']))
            passed=observed==t['expected']
        elif kind=='source_class':
            found=set(h for f in classified(t['expected_class']) for h in f['evidence']['source_handles'])
            observed=sorted(set(t['source_handles'])&found);passed=set(t['source_handles'])<=found
        elif kind=='label_binding':
            observed=[f['id'] for f in classified(t['expected_class'])
                      if set(t['label_handles'])<=set(f['evidence']['label_handles'])]
            passed=bool(observed)
        elif kind=='portal_matches':
            a,b=t['segment'];observed=[]
            for p in result['portals']:
                if p['status']=='uncertain' or p['kind']!='door':continue
                x,y=p['segment']
                distance=min(max(math.dist(a,x),math.dist(b,y)),max(math.dist(a,y),math.dist(b,x)))
                if distance<=t['tolerance_pdf_pt']:observed.append(p['id'])
            passed=bool(observed)
        elif kind=='no_portal_near':
            observed=[p['id'] for p in result['portals']
                      if LineString(p['segment']).distance(Point(t['point']))<=t['tolerance_pdf_pt']
                      and p['status']!='uncertain']
            passed=not observed
        elif kind=='height_transition':
            observed=[f['id'] for f in classified(t['expected_class']) if at(f,t['point'])
                      and f.get('properties',{}).get('height_transition') is True]
            passed=bool(observed)
        else:raise ValueError('Unsupported probe kind: '+kind)
        results.append({'id':t['id'],'case':t['case'],'passed':passed,'observed':observed})
    count=sum(x['passed'] for x in results)
    # Empty output must never receive credit from negative-only probes.
    complete=bool(features) and count==len(results)
    return {'check':'selected_learning_regressions','all_selected_passed':complete,
      'passed':count,'total':len(results),'case_filter':case,'source_dxf_sha256':result['source_dxf_sha256'],
      'engine_name':result['engine_name'],'full_room_recognition_verified':False,
      'note':'A pass applies only to these probes. It is not a complete floor, routing or metric acceptance.',
      'results':results}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('engine_result',type=Path)
    p.add_argument('--case');p.add_argument('--out');a=p.parse_args()
    try:
        with a.engine_result.open(encoding='utf-8') as f:result=json.load(f)
        report=evaluate(result,a.case);code=0 if report['all_selected_passed'] else 1
    except Exception as e:report={'all_selected_passed':False,'input_error':str(e)};code=2
    write_report(report,a.out);sys.exit(code)
