import copy
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pruefe_erkennung import evaluate

# Deliberately synthetic tests of the checker, never source-plan recognition results.
CASES=[{'case_id':'SYN-F01','expected_claims':{'normal_walking_portal':False,'classification':'window'}}]
SOURCES=[{'source_id':'ORIGINAL_PDF','sha256':'a'*64},{'source_id':'ORIGINAL_DXF','sha256':'b'*64}]
def report():
    ev={'source_id':'ORIGINAL_PDF','source_locator':'synthetic fixture location','engine_reference':'synthetic fixture object','explanation':'Synthetic checker test only; not an engine run.'}
    return {'schema_version':'1.0.0','run_id':'synthetic-run','engine_revision':'synthetic-revision','source_hashes':{s['source_id']:s['sha256'] for s in SOURCES},'results':[{'case_id':'SYN-F01','status':'observed','claims':{'normal_walking_portal':False,'classification':'window'},'evidence_by_claim':{'normal_walking_portal':[ev],'classification':[ev]}}]}
class CheckReport(unittest.TestCase):
    def test_valid_synthetic_contract(self):self.assertTrue(evaluate(report(),CASES,SOURCES)['passed'])
    def test_unrun_fails(self):
        r=report();r['results'][0]['status']='not_run';self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_false_portal_claim_fails(self):
        r=report();r['results'][0]['claims']['normal_walking_portal']=True;self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_missing_claim_is_not_false(self):
        r=report();del r['results'][0]['claims']['normal_walking_portal'];self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_zero_is_not_false(self):
        r=report();r['results'][0]['claims']['normal_walking_portal']=0;self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_missing_evidence_fails(self):
        r=report();r['results'][0]['evidence_by_claim']={};self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_wrong_source_fails(self):
        r=report();r['source_hashes']['ORIGINAL_PDF']='c'*64;self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_duplicate_fails(self):
        r=report();r['results'].append(copy.deepcopy(r['results'][0]));self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_missing_case_fails(self):
        r=report();r['results']=[];self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_unknown_case_fails(self):
        r=report();r['results'][0]['case_id']='other';self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_bad_evidence_structure_fails(self):
        r=report();r['results'][0]['evidence_by_claim']['classification']='not a record';self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
    def test_null_run_metadata_fails(self):
        r=report();r['engine_revision']=None;self.assertFalse(evaluate(r,CASES,SOURCES)['passed'])
if __name__=='__main__':unittest.main()
