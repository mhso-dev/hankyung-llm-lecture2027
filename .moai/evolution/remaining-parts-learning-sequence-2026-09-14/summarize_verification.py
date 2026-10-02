"""Collect current, fingerprint-checked delivery evidence for the revision."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from language_corpus import corpus

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
visual=[];language=[];final_files={}
chapters=sorted(ROOT.glob('textbook/part[2-7]/ch*'))
for ch in chapters:
 state=json.loads((HERE/f'{ch.name}-visual-state.json').read_text())
 current={p.name:digest(p) for p in sorted(ch.glob('*.html'))}
 assert state['exit_code']==0 and state['files']==current,f'Stale visual: {ch.name}'
 results=json.loads((ROOT/'textbook/_notebook/checks'/ch.name/'visual-results.json').read_text())
 assert len(results)==2*len(current) and all(r['passed'] for r in results),ch
 visual.append({'directory':str(ch.relative_to(ROOT)),'cases':len(results),'passed':True})
 paths=sorted(p.relative_to(ROOT) for p in (ch/'_src').glob('[0-9]*.html'))
 paths+=sorted(p.relative_to(ROOT) for p in (ROOT/'labs'/ch.parent.name/ch.name/'notebooks').glob('[0-9]*.ipynb'))
 before,after=corpus(paths,HERE/'before-language'),corpus(paths,ROOT)
 fp=hashlib.sha256((before+'\0'+after).encode()).hexdigest()
 folder=HERE/'language'/ch.name
 ls=json.loads((folder/'run-state.json').read_text())
 assert ls['fingerprint']==fp and ls['metric_exit_codes']==[0,0],f'Stale language: {ch.name}'
 gate=json.loads((folder/'gates.json').read_text())
 assert gate['verdict'] in ('PASS','WARN'),(ch,gate['verdict'])
 language.append({'chapter':ch.name,'verdict':gate['verdict'],'warnings':{k:v['note'] for k,v in gate['axes'].items() if v['status']=='WARN'},'corpus_sha256':digest(folder/'final.md')})
 for rel in paths:final_files[str(rel)]=digest(ROOT/rel)
 for p in ch.glob('*.html'):final_files[str(p.relative_to(ROOT))]=digest(p)
for name,path in [(f'part{p}',ROOT/f'textbook/part{p}') for p in range(2,8)]+[('global',ROOT/'textbook')]:
 state=json.loads((HERE/f'{name}-index-visual-state.json').read_text())
 current={p.name:digest(p) for p in sorted(path.glob('*.html'))}
 assert state['exit_code']==0 and state['files']==current,f'Stale index visual: {name}'
 results=json.loads((ROOT/'textbook/_notebook/checks'/path.name/'visual-results.json').read_text())
 assert len(results)==2*len(current) and all(r['passed'] for r in results),name
 visual.append({'directory':str(path.relative_to(ROOT)),'cases':len(results),'passed':True})
 for p in path.glob('*.html'):final_files[str(p.relative_to(ROOT))]=digest(p)
for p in sorted(HERE.glob('review-part*.md')):
 text=p.read_text();assert 'corrected' in text,p
 final_files[str(p.relative_to(ROOT))]=digest(p)
for p in sorted((ROOT/'textbook/downloads').glob('*.zip')):final_files[str(p.relative_to(ROOT))]=digest(p)
write('visual-summary.json',{'cases':sum(r['cases'] for r in visual),'passed':True,'directories':visual})
write('language-summary.json',{'chapters':len(language),'verdict_counts':dict(Counter(r['verdict'] for r in language)),'external_spelling':'skipped: skill commercial bulk restriction; independent local review applied','rows':language})
write('final-artifacts.json',final_files)
print(json.dumps({'visual_cases':sum(r['cases'] for r in visual),'language':dict(Counter(r['verdict'] for r in language)),'artifact_hashes':len(final_files)},ensure_ascii=False))
