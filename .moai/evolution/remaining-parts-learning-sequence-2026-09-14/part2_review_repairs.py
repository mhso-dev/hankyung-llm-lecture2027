raise SystemExit("옛 Part 2 보조 스크립트(part2_review_repairs.py)입니다. 실행하면 Ch 6~8 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")
from pathlib import Path
import json
helpers=Path(__file__).with_name('refine_part2.py').read_text().split("change_md('ch06-langchain-start','05'")[0]
exec(helpers)
ch='ch07-prompt-engineering'
replace_html(ch,'06','자기 일관성(Self-Consistency)은 같은 조건에서 여러 최종 답을 얻고 집계하여, 한 번의 생성에 의존하는 정도를 줄이는 전략입니다.','자기 일관성(Self-Consistency)은 하나의 문제에 대해 다양한 추론 경로를 표집한 뒤, 각 경로가 도달한 최종 답을 집계하는 전략입니다. 이 절은 그중 최종 답의 집계 원리를 배우기 위해 분류 라벨만 반복 생성하는 축소 실습을 사용합니다. 추론 경로를 생성·수집하는 원 기법 전체를 구현하지는 않습니다.')
change_md(ch,'06',9,addition='Self-Consistency는 다양한 추론 경로를 표집한 뒤 각 경로의 최종 답을 집계하는 기법입니다. 이 노트북은 내부 추론을 수집하지 않고 최종 라벨만 반복 생성·집계하는 축소 실습으로, 원 기법의 전체 절차를 재현하지 않습니다.')
change_md(ch,'06',11,oldpart='이것은 최종 라벨 합의를 읽는 축소 실습입니다. 연구에서 다루는 여러 추론 경로의 표집 전체를 구현하지 않습니다.',newpart='Self-Consistency의 원 기법은 여러 추론 경로를 표집하고 최종 답을 집계합니다. 여기서는 최종 라벨 합의만 읽는 축소 실습이므로 추론 경로 표집을 구현하지 않습니다.')
p=next(Path('labs/part2',ch,'notebooks').glob('07-*'));n=json.loads(p.read_text());old=''.join(n['cells'][0]['source']);new=old.replace('파싱과 필드 품질','파싱과 필드 존재');assert old!=new;n['cells'][0]['source']=new.splitlines(keepends=True);p.write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n');g=p.parents[1]/'_make_notebooks.py';s=g.read_text();assert '파싱과 필드 품질' in s;g.write_text(s.replace('파싱과 필드 품질','파싱과 필드 존재'))
replace_html('ch08-context-engineering','06','파이썬 반복문가','파이썬 반복문이')
print('Part2 review first findings repaired')
