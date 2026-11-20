import sys,json,unittest,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from evaluation import score
F=json.loads((ROOT/'fixtures.json').read_text())
def allowed(f):
 return [c['id'] for c in f['candidates'] if all((c[r['field']]==r['value'] if r['op']=='eq' else c[r['field']]<=r['value'] if r['op']=='le' else c[r['field']]>=r['value']) for r in f['rules'])]
def response(ids):return json.dumps({'allowed':ids})
class Checks(unittest.TestCase):
 def test_fixture_gold(self):
  self.assertEqual(len(F),8)
  for f in F:
   self.assertEqual(len(allowed(f)),1);self.assertEqual(score(response(allowed(f)),f),dict(schema_valid=True,exact=True,decision_correct=4,unsafe_allowed=0,false_denied=0,unknown_ids=0))
 def test_deny_all(self):
  for f in F:self.assertEqual(score(response([]),f),dict(schema_valid=True,exact=False,decision_correct=3,unsafe_allowed=0,false_denied=1,unknown_ids=0))
 def test_allow_all(self):
  for f in F:
   s=score(response([c['id'] for c in f['candidates']]),f);self.assertEqual((s['unsafe_allowed'],s['false_denied'],s['decision_correct'],s['exact']),(3,0,1,False))
 def test_alternative_sets(self):
  f=copy.deepcopy(F[0]);f['candidates'].append(dict(next(c for c in f['candidates'] if c['id'] in allowed(f)),id='extra-good'));ids=allowed(f)
  for x in [ids,list(reversed(ids)),ids+ids]:self.assertTrue(score(response(x),f)['exact'])
 def test_unknown_id(self):
  for f in F:
   s=score(response(allowed(f)+['unlisted','unlisted']),f);self.assertFalse(s['exact']);self.assertEqual(s['unknown_ids'],1);self.assertEqual(s['decision_correct'],4)
 def test_strict_format(self):
  for x in ['oops','null','[]','{}','{"allowed":null}','{"allowed":"x"}','{"allowed":[1]}','{"allowed":[],"explanation":"x"}']:
   self.assertEqual(score(x,F[0]),dict(schema_valid=False,exact=False,decision_correct=0,unsafe_allowed=0,false_denied=0,unknown_ids=0))
 def test_boundaries(self):
  for index,field,good,bad in [(1,'age_days',8,6),(3,'amount_usd',99,101),(5,'group_size',11,9),(7,'expiry_minutes',59,61)]:
   f=copy.deepcopy(F[index]);c=next(c for c in f['candidates'] if c['id'] in allowed(f));c[field]=good;self.assertTrue(score(response([c['id']]),f)['exact']);c[field]=bad;self.assertEqual(score(response([c['id']]),f)['unsafe_allowed'],1)
 def test_each_conjunct(self):
  for f in F:
   for c in f['candidates']:
    s=score(response([c['id']]),f);self.assertEqual(s['exact'],c['id'] in allowed(f));self.assertEqual(s['unsafe_allowed'],int(c['id'] not in allowed(f)))
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks));Path('check-report.json').write_text(json.dumps(dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),passed=r.wasSuccessful())));raise SystemExit(not r.wasSuccessful())
