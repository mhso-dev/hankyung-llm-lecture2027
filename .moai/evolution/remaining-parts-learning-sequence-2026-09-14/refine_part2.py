raise SystemExit("옛 Part 2 보조 스크립트(refine_part2.py)입니다. 실행하면 Ch 6~8 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")
from pathlib import Path
import ast,json,re
ROOT=Path.cwd()
def change_md(ch,prefix,index,addition=None,oldpart=None,newpart=None):
 p=next((ROOT/'labs/part2'/ch/'notebooks').glob(prefix+'-*.ipynb'));n=json.loads(p.read_text());c=n['cells'][index];assert c['cell_type']=='markdown'
 old=''.join(c['source']);
 if addition and addition in old:return
 if oldpart and oldpart not in old and newpart in old:return
 new=old+'\n\n'+addition if addition else old.replace(oldpart,newpart);assert old!=new,(p,index)
 g=p.parents[1]/'_make_notebooks.py';s=g.read_text();nodes=[a for a in ast.walk(ast.parse(s)) if isinstance(a,ast.Constant) and a.value==old]
 if nodes:
  assert len(nodes)==1 or prefix=="01"
  a=nodes[0];lines=s.splitlines(keepends=True);start=sum(len(l.encode()) for l in lines[:a.lineno-1])+a.col_offset;end=sum(len(l.encode()) for l in lines[:a.end_lineno-1])+a.end_col_offset
  d=s.encode();g.write_text((d[:start]+repr(new).encode()+d[end:]).decode())
 else:
  # Shared markdown constant may already have been updated for a sibling notebook.
  assert any(isinstance(a,ast.Constant) and a.value==new for a in ast.walk(ast.parse(s))),(g,index)
 c['source']=new.splitlines(keepends=True);p.write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n')
def replace_html(ch,prefix,old,new):
 p=next((ROOT/'textbook/part2'/ch/'_src').glob(prefix+'-*.html'));s=p.read_text();
 if new in s:return
 assert old in s,(p,old);p.write_text(s.replace(old,new))
change_md('ch06-langchain-start','05',5,oldpart='모델 객체에 타임아웃과 최대 재시도 횟수가 설정되었음을 직렬화 가능한 설정에서 확인합니다.',newpart='앞 셀에서 타임아웃과 최대 재시도 횟수를 지정했습니다. 다음 셀은 모델 객체의 타입과 정상 요청의 응답을 확인합니다. 직렬화된 설정이나 실제 타임아웃 발생을 검사하는 셀은 아닙니다.')
p=next(Path('labs/part2/ch06-langchain-start/notebooks').glob('01-*'));n=json.loads(p.read_text());idx=next(i-1 for i,c in enumerate(n['cells']) if c['cell_type']=='code' and 'raise TypeError' in ''.join(c['source']))
change_md('ch06-langchain-start','01',idx,addition='다음 셀의 `all()`·`isinstance()`·`raise TypeError`는 이 수업에서 직접 작성한 문자열 입력 검사입니다. 실제 API를 호출하기 전에 실행하며 LangChain 내부에서 발생한 예외를 관찰한 결과가 아닙니다. LangChain의 모든 메시지 내용 형식을 문자열로 제한하는 일반 규칙으로 해석하지 않습니다.')
replace_html('ch06-langchain-start','01','<h2 id="b6">','<p>아래 실패는 수업에서 직접 작성한 문자열 검사로 확인합니다. <code>all()</code>과 <code>isinstance()</code>의 결과에 따라 코드가 직접 <code>TypeError</code>를 발생시키며, LangChain 내부 검증이나 실제 API 오류를 재현한 결과가 아닙니다. 이 절의 텍스트 입력을 확인하는 제한된 검사입니다.</p>\n<h2 id="b6">')
for p in sorted(Path('labs/part2/ch07-prompt-engineering/notebooks').glob('[0-9]*.ipynb')):
 change_md('ch07-prompt-engineering',p.name[:2],7,addition='`run(messages)`는 이 노트북에서 작성하는 보조 함수입니다. 역할·내용 목록을 받아 `model.invoke()`를 한 번 실행하고, 답 문자열·사용량·경과 초를 담은 딕셔너리를 반환합니다. `def` 셀은 함수를 정의할 뿐이며 뒤에서 `run(...)`을 호출할 때 모델 요청이 시작됩니다. `mention_flags(text)`는 지정 단어가 문자열에 있는지 표시한 딕셔너리를 반환합니다. 답의 뜻을 판단하는 모델 호출은 포함하지 않습니다.')
change_md('ch07-prompt-engineering','03',13,oldpart='세 조건의 원문과 점수',newpart='세 조건의 원문과 확인 표시')
replace_html('ch07-prompt-engineering','05','세 사실의 존재만','세 문자열의 포함 여부만')
replace_html('ch07-prompt-engineering','06','독립 표본을 모으려면 앞 호출의 답을 다음 호출 메시지에 넣지 않고, 모델과 프롬프트, 질문, 생성 설정을 유지해야 합니다.','이번에는 앞 호출의 답을 다음 호출 메시지에 넣지 않고 같은 모델·프롬프트·질문·생성 설정으로 각각 호출합니다. 응답을 서로 전달하지 않는 구조이며, 이것만으로 표본의 통계적 독립성을 확인한 것은 아닙니다.')
p=next(Path('textbook/part2/ch07-prompt-engineering/_src').glob('08-*'));s=p.read_text();s=s.replace('Ch 6의 03절에서 JSON 변환을 배웠습니다.','Ch 4의 05절에서 JSON 변환을 배웠습니다.');p.write_text(s)
change_md('ch08-context-engineering','01',13,addition='`get_encoding("o200k_base")`는 지정한 토큰화 규칙을 불러오고 `encode(prompt)`는 문자열을 토큰 ID 목록으로 바꿉니다. 여기서 세는 대상은 `prompt` 문자열뿐입니다. 뒤의 system 메시지와 메시지 형식까지 포함한 실제 입력 사용량은 응답의 `usage_metadata`에서 따로 확인합니다.')
change_md('ch08-context-engineering','02',9,addition='`Path(gettempdir()) / "ch08-memory.json"`은 임시 폴더에 파일 이름을 연결한 경로입니다. `json.dumps()`는 목록을 JSON 문자열로 바꾸고 `write_text()`가 그 문자열을 저장합니다. 고정 파일 이름이므로 이 셀을 다시 실행하면 같은 이름의 기록을 덮어씁니다. 장기 보존이나 여러 사용자의 저장을 설계한 예제는 아닙니다.')
change_md('ch08-context-engineering','03',15,addition='`loan_messages`와 `closure_messages`는 서로 다른 입력 목록입니다. 각각 필요한 규정만 포함한 뒤 별도로 호출합니다. 뒤의 `assert`는 특정 출처 ID가 다른 입력에 없는지 확인할 뿐, 모든 정보 유출 가능성을 검사하지 않습니다.')
change_md('ch08-context-engineering','04',22,addition='`eligible`은 기준일 전에 시행된 후보 목록입니다. `max(eligible, key=effective_date)`는 각 후보를 `effective_date()`에 넘겨 얻은 날짜 문자열을 비교합니다. 함수 이름을 넘기므로 비교할 때마다 필요한 후보의 날짜를 읽습니다. 후보가 비어 있거나 서로 다른 날짜 형식이 섞인 경우는 이 예제의 입력에 없으며 실제 처리에서는 별도 분기가 필요합니다.')
change_md('ch08-context-engineering','06',24,addition='아래 딕셔너리의 “연장 예외”는 실제로 “연장” 문자열이 있는지만 검사합니다. 예약이 없다는 조건과 1회·7일 제한을 모두 확인하는 검사가 아니므로 답 원문에서 별도로 읽습니다. “출처”도 `E01` 포함만 보므로 페이지가 정확한지까지 자동 판정하지 않습니다.')
ch='ch08-context-engineering'
for old,new in [('고정된 파이썬 함수','고정된 파이썬 반복문'),('고정 함수','고정 코드'),('함수가 해당 문서를 가져옵니다','반복문이 해당 문서를 찾습니다'),('ID를 함수가 읽습니다','ID를 반복문에서 비교합니다'),('ID와 고정 함수','ID와 고정 코드')]:
 p=next((Path('textbook/part2')/ch/'_src').glob('06-*'));s=p.read_text();p.write_text(s.replace(old,new))
replace_html(ch,'06','05절에서는 입력이 모델 한도 안에 있어도, 모델이 긴 자료 속 근거를 언제나 같은 수준으로 활용한다고 가정할 수 없음을 확인했습니다.','05절에서는 길이를 달리한 세 조건의 답을 관찰했고, 이번 실행에서는 성능 저하를 확인하지 못했습니다. 이 결과를 모든 긴 문서의 과제로 확대할 수는 없습니다.')
replace_html(ch,'04','LangChain 팀이 여러 실패 사례를 설명하려고 붙인 이름입니다.','LangChain 팀이 Drew Breunig의 글을 인용하여 여러 실패 사례를 설명할 때 소개한 이름입니다.')
print('part2 targeted refinements complete')
