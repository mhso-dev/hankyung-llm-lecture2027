from pathlib import Path
import concurrent.futures,hashlib,json,subprocess,sys
from language_corpus import corpus,ROOT,HERE
SKILL=Path('/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-humanize/references')
def run(ch):
 paths=sorted(p.relative_to(ROOT) for p in (ch/'_src').glob('[0-9]*.html'))
 paths+=sorted(p.relative_to(ROOT) for p in (ROOT/'labs'/ch.parent.name/ch.name/'notebooks').glob('[0-9]*.ipynb'))
 folder=HERE/'language'/ch.name;folder.mkdir(parents=True,exist_ok=True)
 before,after=corpus(paths,HERE/'before-language'),corpus(paths,ROOT)
 fingerprint=hashlib.sha256((before+'\0'+after).encode()).hexdigest()
 stamp=folder/'run-state.json'
 if stamp.exists() and json.loads(stamp.read_text()).get('fingerprint')==fingerprint:return (ch.name,'unchanged')
 (folder/'01_input.txt').write_text(before);(folder/'final.md').write_text(after)
 codes=[]
 for name,input_path in [('before','01_input.txt'),('after','final.md')]:
  p=subprocess.run([sys.executable,str(SKILL/'metrics.py'),'--input',str(folder/input_path),'--genre','essay','--output',str(folder/(name+'-metrics.json'))],capture_output=True,text=True)
  codes.append(p.returncode)
  if p.returncode: (folder/(name+'-error.txt')).write_text(p.stderr)
 p=subprocess.run([sys.executable,str(SKILL/'verify_gates.py'),'--before',str(folder/'01_input.txt'),'--after',str(folder/'final.md'),'--genre','essay','--json'],capture_output=True,text=True)
 (folder/'gates.json').write_text(p.stdout)
 if p.stderr:(folder/'gate-stderr.txt').write_text(p.stderr)
 stamp.write_text(json.dumps({'fingerprint':fingerprint,'metric_exit_codes':codes,'gate_exit_code':p.returncode},indent=2))
 return ch.name,p.returncode
selected=set(sys.argv[1:]);chapters=[c for c in sorted(ROOT.glob('textbook/part[2-7]/ch*')) if not selected or c.name[:4] in selected]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(run,chapters):print(*result,flush=True)
