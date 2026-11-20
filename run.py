import json,hashlib,subprocess,sys,time,platform,urllib.request
from pathlib import Path
from datetime import datetime,timezone
from request import build
from evaluation import score
ROOT=Path(__file__).resolve().parent
MODELS=['qwen2.5:7b','qwen3:8b']
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def api(route,body=None):
 data=None if body is None else json.dumps(body).encode()
 with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434'+route,data=data,headers={'Content-Type':'application/json'}),timeout=90) as r:return json.load(r)
def idle(allowed):
 for _ in range(80):
  v=api('/api/ps')['models']
  if all(m.get('name',m.get('model')) in allowed for m in v):return v
  time.sleep(.25)
 raise RuntimeError('Other model resident; no eviction or parallel measurement')
def freeze():
 assert not (ROOT/'frozen.json').exists()
 tags={m['name']:m for m in api('/api/tags')['models']};assert all(m in tags for m in MODELS)
 dump(ROOT/'evidence/models.json',{m:{'installed':tags[m],'show':api('/api/show',{'model':m})} for m in MODELS})
 dump(ROOT/'evidence/versions.json',{'ollama':api('/api/version'),'python':sys.version,'platform':platform.platform(),'invariant':subprocess.check_output(['invariant','--version'],text=True).strip()})
 files=['PROTOCOL.md','fixtures.json','schedule.json','request.py','evaluation.py','tests/run_checks.py','run.py','audit.py','CANDIDATES.json','SOURCES.json','evidence/models.json','evidence/versions.json']
 dump(ROOT/'frozen.json',{'frozen_at':datetime.now(timezone.utc).isoformat(),'planned':64,'sha256':{n:sha(ROOT/n) for n in files}})
def measure():
 folder=ROOT/'results/primary';assert not folder.exists(),'Refuse replay/overwrite'
 frozen=json.loads((ROOT/'frozen.json').read_text())
 for n,h in frozen['sha256'].items():assert sha(ROOT/n)==h,n
 installed={m['name']:m['digest'] for m in api('/api/tags')['models']};manifest=json.loads((ROOT/'evidence/models.json').read_text());assert all(installed[m]==manifest[m]['installed']['digest'] for m in MODELS)
 fixtures={f['id']:f for f in json.loads((ROOT/'fixtures.json').read_text())};schedule=json.loads((ROOT/'schedule.json').read_text());summaries={};prior=None
 folder.mkdir(parents=True);(folder/'issued').mkdir();state={'status':'running','planned':64,'completed':0,'started_at':datetime.now(timezone.utc).isoformat(),'implementation_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()};dump(folder/'run.json',state)
 try:
  idle(set())
  with (folder/'raw.jsonl').open('x') as out:
   for cell in schedule:
    if prior and prior!=cell['model']:
     dump(folder/'unload-between.json',api('/api/generate',{'model':prior,'keep_alive':0,'stream':False}));idle(set())
    resident=idle({cell['model']});prior=cell['model'];key=(cell['model'],cell['fixture_id']);fixture=fixtures[cell['fixture_id']]
    req=build(cell,fixture,summaries.get(key));rec=dict(cell,request=req,resident_before=resident,issued_at=datetime.now(timezone.utc).isoformat(),status='issued');dump(folder/'issued'/(cell['id']+'.json'),rec)
    start=time.monotonic()
    try:
     response=api('/api/chat',req);rec.update(status='responded',response=response,wall_seconds=time.monotonic()-start)
     assert response.get('done') is True and response.get('model')==cell['model']
     if cell['kind']=='summary':summaries[key]=response['message']['content'];rec['summary_words']=len(summaries[key].split())
     else:rec['score']=score(response['message']['content'],fixture)
    except Exception as e:rec.update(status='error',error=type(e).__name__,detail=str(e)[:300]);out.write(json.dumps(rec)+'\n');out.flush();raise
    out.write(json.dumps(rec,ensure_ascii=False)+'\n');out.flush();state['completed']+=1;dump(folder/'run.json',state);print(json.dumps({'completed':state['completed'],'id':cell['id']}),flush=True)
  state['status']='completed'
 except Exception as e:state.update(status='incomplete',error=type(e).__name__,detail=str(e)[:300]);raise
 finally:
  state['finished_at']=datetime.now(timezone.utc).isoformat();dump(folder/'run.json',state)
  if prior:dump(folder/'unload-final.json',api('/api/generate',{'model':prior,'keep_alive':0,'stream':False}))
if __name__=='__main__':
 if sys.argv[1]=='freeze':freeze()
 elif sys.argv[1]=='measure':measure()
 else:raise SystemExit('freeze or measure')
