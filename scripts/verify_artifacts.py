"""Offline integrity and specialized premise audits; does not run UPPAAL."""
from pathlib import Path
import argparse, collections, hashlib, importlib.util, json, re, sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok, message):
    if not ok: raise ValueError(message)
def load(name):
    path = ROOT/'scripts/kernels'/f'{name}.py'
    spec = importlib.util.spec_from_file_location('artifact_'+name,path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def certificates():
    rec, srv, cap, obs = (load(n) for n in ['receipt','service','capacity','observers'])
    root = ET.parse(ROOT/'models/S/model.xml').getroot()
    q = (ROOT/'queries/S/completion-safety.q').read_text(encoding='utf-8')
    receipt = rec.check_premises(root,q,read('proofs/completion-safety/premises.json'))
    service = srv.analyze(root,read('proofs/service-feasibility/premises.json'))
    service['causal_dependency']={k:receipt[k] for k in ['premises_supported','query_atoms']}
    service['rational_examples']=srv.rational_examples()
    observer = obs.audit(root,q,read('proofs/observer-erasure/premises.json'))
    reduced = obs.erase(root,observer)
    require(reduced == (ROOT/'models/R/model.xml').read_bytes(),'observer erasure does not reproduce the recorded R bytes')
    observer['reduced_sha256']=hashlib.sha256(reduced).hexdigest()
    family=[]
    for n in range(1,5):
        premises=cap.check_structure((ROOT/f'models/F/n{n}/model.xml').read_bytes(),
          (ROOT/f'queries/F/n{n}/p4/shared-capacity.q').read_text(encoding='utf-8'),n)
        family.append({'N':n,'process_count':premises.processes,'abstract_graph':cap.explore(premises)})
    capacity={'evidence_kind':'static_validation','models':family,'property_verdict':None,
              'independent_scientific_acceptance':'pending'}
    return {'completion-safety':receipt,'service-feasibility':service,
            'observer-erasure':observer,'shared-capacity':capacity}
def check_records():
    rows=read('results/index.json'); index=read('models/index.json')
    for key,m in index.items():require(digest(ROOT/m['path'])==m['sha256'],'model hash mismatch: '+key)
    for r in rows:
        require(digest(ROOT/r['model_path'])==r['model_hash'],'result model mismatch: '+r['run_id'])
        if r.get('query_path'):
            require(digest(ROOT/r['query_path'])==r['query_hash'],'result query mismatch: '+r['run_id'])
        for k in ['stdout_path','stderr_path','memory_samples_path']:
            if r.get(k):require((ROOT/r[k]).is_file(),'missing '+k+': '+r['run_id'])
        for k in ['trace_paths','telemetry_paths','evidence_paths']:
            for f in r.get(k,[]):require((ROOT/f).is_file(),'missing evidence: '+f)
        if r.get('status') in ['timeout','memory_limit','error']:
            require(r.get('verdict') is None and r.get('property_verdict') is None,'inconclusive run has a verdict: '+r['run_id'])
    f=[r for r in rows if r['model_path'].startswith('models/F/')]
    require(len(f)==90,'finite-family attempt count differs')
    counts=collections.Counter((r['status'],r.get('property_verdict')) for r in f)
    require(counts=={('timeout',None):72,('success','satisfied'):12,('success','violated'):6},'finite-family verdict counts differ')
    for r in f:
        text=(ROOT/r['stdout_path']).read_text(encoding='utf-8')
        if r['status']=='success':
            matches=re.findall(r'Formula is (NOT )?satisfied',text)
            require(len(matches)==1 and ('violated' if matches[0] else 'satisfied')==r['property_verdict'],'stdout verdict differs: '+r['run_id'])
    require(len([r for r in rows if r['model_path']=='models/R/model.xml'])==4,'diagnostic count differs')
    require(len([r for r in rows if r['model_path']=='models/S/model.xml' and r['status']=='timeout'])==11,'full-model timeout count differs')
    return {'record_count':len(rows),'finite_family_attempts':len(f),'finite_family_positive':12,
      'finite_family_negative':6,'finite_family_timeouts':72,'native_verifier_invoked':False}
def integrity():
    manifest=read('MANIFEST.json'); expected={x['path']:x['sha256'] for x in manifest['files']}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and '.git' not in p.parts and '__pycache__' not in p.parts and p.name!='MANIFEST.json'}
    require(actual==set(expected),'manifest file set differs: '+str(sorted(actual ^ set(expected))))
    for path,h in expected.items():require(digest(ROOT/path)==h,'manifest hash mismatch: '+path)
    return len(expected)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--refresh-certificates',action='store_true',help='write deterministic static certificates')
    args=ap.parse_args()
    try:
        if not args.refresh_certificates: count=integrity()
        artifacts=certificates()
        for name,j in artifacts.items():
            text=json.dumps(j,indent=2,sort_keys=True)+'\n';path=ROOT/'results/static'/f'{name}.json'
            if args.refresh_certificates:
                path.parent.mkdir(exist_ok=True,parents=True);path.write_text(text,encoding='utf-8',newline='\n')
            else:require(path.read_text(encoding='utf-8')==text,'static certificate differs: '+name)
        summary=check_records()
        if not args.refresh_certificates: summary['hashed_files']=count
        summary['static_checks']='passed';print(json.dumps(summary,indent=2))
    except (ValueError,OSError,KeyError,ET.ParseError) as e:
        print('CHECK FAILED: '+str(e),file=sys.stderr);return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
