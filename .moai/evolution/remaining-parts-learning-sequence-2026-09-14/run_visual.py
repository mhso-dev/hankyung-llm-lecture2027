from pathlib import Path
import concurrent.futures,hashlib,json,os,subprocess
ROOT=Path.cwd();QA=ROOT/'.moai/evolution/remaining-parts-learning-sequence-2026-09-14'
env=dict(os.environ);env['NODE_PATH']='/Users/mhso/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'
def run(ch):
 files=sorted(ch.glob('*.html'));fingerprint={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 stamp=QA/(ch.name+'-visual-state.json')
 if stamp.exists():
  old=json.loads(stamp.read_text())
  if old.get('files')==fingerprint and old.get('exit_code')==0:return(ch.name,'unchanged PASS')
 with (QA/(ch.name+'-visual.log')).open('w') as log:
  p=subprocess.run(['node','textbook/_notebook/visual.cjs',str(ch)],stdout=log,stderr=subprocess.STDOUT,env=env)
 result={'chapter':str(ch),'files':fingerprint,'exit_code':p.returncode};stamp.write_text(json.dumps(result,indent=2));return(ch.name,p.returncode)
chapters=sorted(ROOT.glob('textbook/part[2-7]/ch*'))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(run,chapters):print(*result,flush=True)
