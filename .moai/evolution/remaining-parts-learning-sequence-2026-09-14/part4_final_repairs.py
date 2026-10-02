raise SystemExit("옛 Part 4 보조 스크립트(part4_final_repairs.py)입니다. 실행하면 Ch 15·16 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")
from pathlib import Path
import ast,importlib.util,json
p=Path('labs/part4/notebook_guidance.py');s=p.read_text().replace('if source.lstrip().startswith("%pip"):', 'if executable_source.lstrip().startswith("%pip"):');p.write_text(s)
spec=importlib.util.spec_from_file_location('guidance',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
changed=[]
for p in Path('labs/part4').glob('ch*/notebooks/[0-9]*.ipynb'):
 nb=json.loads(p.read_text());dirty=False
 for i,c in enumerate(nb['cells']):
  if c['cell_type']!='code':continue
  source=''.join(c['source']);clean='\n'.join(x for x in source.splitlines() if not x.lstrip().startswith('#'))
  if clean.lstrip().startswith('%pip'):
   prior=nb['cells'][i-1];assert prior['cell_type']=='markdown';old=''.join(prior['source']);new=old.split('\n\n**이 셀의 코드 읽기.**',1)[0].rstrip()+mod.explain_code(source)+'\n'
   if new!=old:prior['source']=new.splitlines(keepends=True);dirty=True
 if dirty:p.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n');changed.append(str(p))
g=Path('labs/part4/ch16-guardrails/author_chapter.py');tree=ast.parse(g.read_text());base=next(x.value for x in ast.walk(tree) if isinstance(x,ast.Constant) and isinstance(x.value,str) and x.value.startswith('## 보호 경로를 순서대로 실행'))
p=next(Path('labs/part4/ch16-guardrails/notebooks').glob('06-*'));nb=json.loads(p.read_text());c=nb['cells'][13];old=''.join(c['source']);tail=old[old.index('\n\n**이 셀의 코드 읽기.**'):];c['source']=(base+tail).splitlines(keepends=True);p.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
old='앞 절에서 평가 대상과 평가 모델 결과를 레코드로 묶었습니다. 이제 같은 레코드에 실행 경로를 추가합니다.'
new='04절에서는 평가 대상과 평가 모델 결과를 레코드로 묶었습니다. 이번 절은 별도의 합성 실행 기록을 만들어 단계별 소요 시간과 부모·자식 관계를 관찰합니다. 앞 절의 파일을 읽어 같은 레코드에 경로를 추가하는 코드는 아닙니다.'
for p in [next(Path('textbook/part4/ch15-evaluation-advanced/_src').glob('05-*')),Path('textbook/part4/ch15-evaluation-advanced/_author.py')]:
 s=p.read_text();assert old in s;p.write_text(s.replace(old,new))
print('pip guidance repaired',len(changed))
