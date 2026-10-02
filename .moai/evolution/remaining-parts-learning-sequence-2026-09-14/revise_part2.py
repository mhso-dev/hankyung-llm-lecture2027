raise SystemExit("옛 Part 2 보조 스크립트(revise_part2.py)입니다. 실행하면 Ch 6 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")
from pathlib import Path
import ast,html,json,re
ROOT=Path(__file__).resolve().parents[3]
QA=Path(__file__).resolve().parent
changes=json.loads((QA/"part2-edits.json").read_text()) if (QA/"part2-edits.json").exists() else []
def markup(text):
 return re.sub(r'`([^`]+)`',lambda m:'<code>'+html.escape(m[1])+'</code>',html.escape(text).replace('&lt;code&gt;','<code>'))
def para(text):
 parts=re.split(r'(`[^`]+`)',text)
 return '<p>'+''.join('<code>'+html.escape(p[1:-1])+'</code>' if p.startswith('`') and p.endswith('`') else html.escape(p) for p in parts)+'</p>'
def apply(ch,prefix,heading,paragraphs,anchor,md_cell,md_extra):
 src=next((ROOT/'textbook/part2'/ch/'_src').glob(prefix+'-*.html'))
 nbp=ROOT/'labs/part2'/ch/'notebooks'/(src.stem+'.ipynb')
 nb=json.loads(nbp.read_text());s=src.read_text()
 marker='<!-- learning-sequence-20260914-'+prefix+' -->'
 if marker in s:return
 block=marker+'\n<h3>'+heading+'</h3>\n'+'\n'.join(para(p) for p in paragraphs)+'\n'
 assert s.count(anchor)==1,(src,anchor,s.count(anchor))
 s=s.replace(anchor,block+anchor)
 old=''.join(nb['cells'][md_cell]['source']);assert nb['cells'][md_cell]['cell_type']=='markdown'
 new=old+'\n\n'+'\n\n'.join(md_extra)
 nb['cells'][md_cell]['source']=new.splitlines(keepends=True)
 gen=ROOT/'labs/part2'/ch/'_make_notebooks.py';gs=gen.read_text();tree=ast.parse(gs);nodes=[n for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value==old]
 if len(nodes)==1:
  n=nodes[0];lines=gs.splitlines(keepends=True);start=sum(len(l.encode()) for l in lines[:n.lineno-1])+n.col_offset;end=sum(len(l.encode()) for l in lines[:n.end_lineno-1])+n.end_col_offset
  data=gs.encode();gs=(data[:start]+repr(new).encode()+data[end:]).decode();ast.parse(gs);gen.write_text(gs)
 else:
  changes.append({'generator_sync_pending':str(gen.relative_to(ROOT)),'section':src.stem,'old':old,'new':new})
 src.write_text(s);nbp.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
 changes.append({'section':src.stem,'source':str(src.relative_to(ROOT)),'notebook':str(nbp.relative_to(ROOT)),'first_use_heading':heading,'markdown_cell':md_cell,'code_changed':False})

ch='ch06-langchain-start'
apply(ch,'01','입력 목록에서 응답 객체까지 한 줄씩 읽기',[
'이 실습에서 먼저 연결할 이름은 `model`, `messages`, `response` 세 개입니다. `model`은 요청을 보낼 방법과 설정을 가진 객체이고, `messages`는 이번에 전달할 역할과 내용의 목록이며, `response`는 호출이 끝난 뒤 받은 응답 객체입니다. 모델 객체를 만든 뒤 질문 문자열을 바꾸는 것만으로 서버가 실행되지는 않습니다. `response = model.invoke(messages)`의 오른쪽 호출이 끝나야 왼쪽 이름에 결과가 대입됩니다.',
'`("system", "두 문장 이내의 한국어로 답하세요.")`에서 첫 값은 메시지 역할이고 둘째 값은 실제 문장입니다. `system`은 이 예제의 공통 지시, `user`는 현재 질문을 나타냅니다. 목록 순서가 전달 순서이며, `messages[0]`은 첫 메시지를 다시 사용합니다. 출력용 `[role for role, _ in messages]`는 각 튜플을 두 값으로 나누고 역할만 새 목록에 모읍니다. 밑줄 이름은 둘째 값을 이 계산에서 사용하지 않겠다는 관례입니다.',
'가령 같은 모델 객체로 도서관 규정을 요약한 뒤 상품 후기를 분류한다고 생각해 봅니다. 바뀌는 것은 매번 넘기는 메시지 목록입니다. 앞 요청의 응답을 다음 목록에 넣지 않으면 이 호출 코드는 두 요청을 하나의 대화로 연결하지 않습니다. 여러 질문을 보냈다는 사실과 대화 이력을 전달했다는 사실을 구분하면 다음 절의 메시지 역할을 이해할 수 있습니다.'
],'<h3>같은 모델도 호출 방법에 따라',5,[
'`model`은 호출 설정을 가진 객체, `messages`는 이번 입력, `response`는 완료된 호출의 반환값입니다. `init_chat_model()`은 객체를 준비하고, `model.invoke(messages)`가 질문을 실제 전송합니다. `response.text`는 텍스트를 읽는 속성이므로 뒤에 호출 괄호를 붙이지 않습니다.',
'메시지는 `(역할, 내용)` 튜플의 목록입니다. 여기서 `system`은 공통 지시이고 `user`는 이번 질문입니다. `[role for role, _ in messages]`는 튜플을 역할과 내용으로 나누어 역할만 모으는 목록 표현식입니다. `_`도 변수 이름이지만 이 자리에서는 내용 값을 사용하지 않는다는 관례로 씁니다.',
'같은 모델 객체에 다른 질문 목록을 넘길 수 있습니다. 이전 답까지 이어서 대화하려면 그 답을 다음 입력 목록에 직접 포함해야 합니다. 아래의 질문 변경은 같은 호출 방법의 재사용을 확인하며 대화 기억 기능을 시험하지 않습니다.'
])
apply(ch,'02','역할 이름과 메시지 객체의 관계',[
'`SystemMessage("한 문장으로 답하세요.")`는 역할을 클래스로 명시한 메시지 객체를 만듭니다. 여기서 괄호 안 문장은 `content`에 해당합니다. 같은 내용을 튜플 `("system", "한 문장으로 답하세요.")`로 적으면 모델 통합이 메시지 형식으로 읽습니다. 객체 생성과 모델 호출은 별개이므로 `SystemMessage`나 `HumanMessage`를 생성하기만 해서는 답이 나오지 않습니다.',
'사용자 입력을 뜻하는 튜플의 `user`와 `HumanMessage`의 `type`에 나타나는 `human`은 이 실습에서 같은 역할을 표현하는 서로 다른 표기입니다. 클래스 이름, 객체의 타입 표시, 제공자에게 전달되는 역할 필드가 항상 같은 문자열인 것은 아닙니다. 아래 출력에서 `system`, `human`을 본 뒤 메시지 내용을 읽으면 두 표현을 대응시킬 수 있습니다.',
'예를 들어 번역 서비스에서는 공통 번역 규칙을 system에, 번역할 문장을 user에 둡니다. 여러 사람의 문의를 처리할 때도 공통 규칙과 매번 바뀌는 내용을 따로 만들 수 있습니다. 이전 답을 assistant 메시지로 포함하는 것은 대화 흐름을 제공하는 방법입니다. 그 답이 정확한 근거인지는 별도로 판단해야 하며, 이전 답에 있던 오류를 사실로 확정하지 않습니다.'
],'<h2 id="b5">',9,[
'`SystemMessage(...)`와 `HumanMessage(...)`는 전달할 메시지 객체를 생성하며 여기서는 서버를 호출하지 않습니다. 문자열은 각 객체의 내용입니다. 객체의 `.type`은 역할 종류를 표시합니다. 사용자 역할을 튜플로 쓸 때의 `user`가 `HumanMessage.type`에서는 `human`으로 표시됩니다.',
'번역 규칙을 공통 system 메시지로 두고 여러 번역 대상 문장만 바꿀 수도 있습니다. 객체 형식은 역할과 내용을 분리해 읽기 위한 표현이며, 메시지 클래스 자체가 응답을 더 정확하게 만드는 설정은 아닙니다. 아래 셀은 역할 목록만 출력하므로 튜플과 객체 방식의 모델 응답 품질을 비교한 실험으로 해석하지 않습니다.'
])
apply(ch,'03','with_structured_output의 준비와 실행 구분',[
'이 메서드는 이 절에서 처음 배웁니다. `model.with_structured_output(StudyCard)`에서 점 앞의 `model`은 준비한 채팅 모델이고, 괄호 안의 `StudyCard`는 만들어 달라는 카드의 형식입니다. `StudyCard()`처럼 빈 카드 객체를 만드는 호출이 아니라 클래스 자체를 전달합니다. LangChain이 필드 설명과 제약을 읽어 모델 호출에 적용할 수 있도록 하기 위한 것입니다.',
'반환된 `structured_model`은 나중에 실행할 수 있는 호출 객체입니다. 이 줄만으로 학습 카드가 생성되지 않습니다. 다음 `structured_model.invoke("AIMessage를 설명하세요")`가 요청을 실행하고, 성공하면 읽고 검증한 `StudyCard` 인스턴스를 반환합니다. 따라서 `card.difficulty`로 필드 값을 읽고 `card.model_dump()`로 딕셔너리 표현을 얻습니다. `invoke()`의 입력은 카드에 넣을 내용을 요청하는 문장이고, 스키마 자체와 역할이 다릅니다.',
'학습 카드와 주문 입력을 비교하면 같은 원리가 더 분명해집니다. 카드에서는 난이도 범위가 중요하고 주문에서는 품명이 비어 있지 않은지와 수량이 양수인지가 중요합니다. 아래 주문 예시는 개발자가 직접 만든 JSON을 읽어 검증합니다. 주문을 모델이 추출했다고 가정하지 않으며, 필드 규칙을 바꿔도 실제 재고나 주문의 존재 여부까지 확인되는 것은 아닙니다.'
],'<h3>스키마 표현은',5,[
'스키마는 받을 항목과 형식의 정의입니다. `class StudyCard(BaseModel):`는 Pydantic의 검증 기능을 물려받은 클래스입니다. `concept: str`은 문자열 필드, `difficulty: int`는 정수 필드이며 `Field(ge=1, le=3)`는 1 이상 3 이하라는 범위를 선언합니다. `description`은 필드 의미를 설명하는 문자열입니다. Ch 2의 선택 B 경로를 읽지 않았더라도 이 선언을 카드의 각 칸과 허용값으로 읽을 수 있습니다.',
'`model.with_structured_output(StudyCard)`는 이 절에서 처음 사용하는 메서드입니다. 카드 인스턴스가 아닌 클래스 `StudyCard`를 넘겨 출력 형식을 설정한 호출 객체를 만듭니다. 실제 생성은 다음 셀의 `structured_model.invoke(...)`에서 이루어집니다. 성공하면 `AIMessage` 대신 `StudyCard`를 받으며, `model_dump()`로 그 필드들을 딕셔너리로 읽습니다.',
'같은 셀의 `diagnostic_model`은 뒤의 오류 관찰에 사용할 두 번째 호출 객체입니다. `include_raw=True`를 주면 이후 호출 결과가 `raw`·`parsed`·`parsing_error` 키를 가진 딕셔너리가 됩니다. 먼저 기본 `structured_model`의 카드 반환을 읽고, 그다음 원본 응답과 오류를 함께 확인하는 확장 경로를 비교합니다.'
])
apply(ch,'04','청크 하나와 최종 응답을 구분해 읽기',[
'청크(chunk)는 스트림에서 한 번 전달받는 응답 조각입니다. `model.stream(messages)`는 조각을 차례로 읽을 수 있는 반복자를 제공하며, `for chunk in ...`가 이를 순서대로 읽습니다. 각 `chunk`는 `AIMessageChunk`이고 `.text`는 그 조각의 텍스트입니다. 청크 경계가 단어·문장·토큰 하나의 경계와 항상 같다고 가정하지 않습니다.',
'예를 들어 화면에 “대출은”과 “ 3권까지입니다.”가 순서대로 도착한다면, 첫 조각만으로 최대 권수를 정할 수 없습니다. 이 문장은 원리를 설명하기 위한 가정입니다. 실제 예제에서는 저장된 `chunks` 목록을 읽고 각 조각을 `+`로 결합합니다. 이는 단순 문자열 덧붙이기와 달리 메시지 조각의 자료를 병합하는 연산이며, 최종 변수도 `AIMessageChunk`입니다.',
'`print(..., end="", flush=True)`의 `end`는 매 출력 뒤의 줄바꿈을 없애고 `flush`는 출력 버퍼에 남기지 않고 표시하도록 요청합니다. 두 인자는 모델의 생성 설정이 아니라 Python 화면 출력 설정입니다. 채팅 화면은 조각이 올 때마다 표시할 수 있지만, 결과를 파일에 저장하거나 구조를 검사하는 단계는 완료된 내용을 대상으로 해야 하는 경우가 많습니다.'
],'<h2 id="b5">',5,[
'청크는 한 번 전달된 응답 조각입니다. `stream()`에서 읽는 각 값은 `AIMessageChunk`이며 `for` 반복문이 순서대로 소비합니다. `.text`가 비어 있는 조각도 있으므로 청크 수가 곧 글자 수나 토큰 수는 아닙니다.',
'`end=""`는 조각 사이의 자동 줄바꿈을 없애고 `flush=True`는 Python 출력이 바로 표시되도록 요청합니다. 생성 모델의 설정이 아닙니다. `chunks.append(chunk)`는 나중에 결합할 원본 조각을 순서대로 남깁니다.',
'안내문에서 권수나 예외 조건이 마지막에 나올 수 있으므로 앞 조각만 보고 최종 답을 확정하지 않습니다. 아래에서는 같은 스트림의 조각을 결합한 뒤, 별도의 `invoke()` 호출에서 받은 응답과 타입을 비교합니다. 두 호출의 문구가 같을 필요는 없습니다.'
])
apply(ch,'05','Python 함수를 Runnable로 감싸는 이유',[
'`Runnable`은 LangChain에서 같은 호출 방식으로 실행할 수 있는 구성 요소를 가리킵니다. 앞 절의 모델에는 이미 `invoke()`가 있습니다. 우리가 작성한 일반 함수 `fail_primary`에는 그 메서드가 없으므로 `RunnableLambda(fail_primary)`로 감싸서 `primary.invoke("질문")`으로 실행할 수 있게 합니다. 함수 이름을 전달하는 순간에 함수가 실행되지는 않습니다.',
'여기서 `lambda value: f"대체 경로: {value}"`는 입력 하나를 받아 문자열 하나를 만드는 짧은 함수 표현식입니다. 콜론 앞은 매개변수, 뒤는 반환할 값입니다. 이를 감싼 `fallback`도 호출 객체이므로 `with_fallbacks([fallback])`의 목록에 넣을 수 있습니다. 이 목록은 대체 응답 문자열 목록이 아니라 오류가 날 때 실행할 객체 목록입니다.',
'예를 들어 규정 조회가 일시적으로 실패했을 때 같은 조회를 한 번 더 실행하면 재시도입니다. 사전에 확인한 점검 안내문을 반환하면 폴백입니다. 후자는 사용자가 읽을 응답을 제공하지만 규정 조회를 성공시킨 것은 아닙니다. 예제의 시도 횟수는 함수 실행 횟수이며, 실제 네트워크 장애율이나 서비스 복구율을 뜻하지 않습니다.'
],'<h3>서로 다른 세 개의 제한</h3>',7,[
'`Runnable`은 `invoke()`처럼 공통 방식으로 실행할 수 있는 LangChain 구성 요소입니다. `RunnableLambda(fail_primary)`는 Python 함수 자체를 받아 그 호출 방식을 연결합니다. 괄호 안에 `fail_primary()`처럼 실행 결과를 넣지 않습니다. 실제 함수 실행은 `primary.invoke(...)`에서 시작됩니다.',
'`lambda value: f"대체 경로: {value}"`는 입력 `value`로 문자열을 만들어 반환하는 짧은 함수입니다. `with_fallbacks([fallback])`는 기본 호출에 실패했을 때 실행할 객체 목록을 받습니다. `with_retry()`와 `with_fallbacks()`로 호출 객체를 구성한 다음 `invoke()`해야 설정한 제어 흐름이 실행됩니다.',
'아래 함수가 직접 `TimeoutError`를 발생시키므로 오류 처리 흐름을 반복 관찰할 수 있습니다. 정해 둔 점검 안내를 반환하는 것과 원래 조회가 복구된 것은 다른 결과입니다. 기록의 시도 횟수를 실제 제공자 요청 횟수로 바꾸어 해석하지 않습니다.'
])
apply(ch,'06','측정 기록의 값과 상태를 함께 읽기',[
'`usage_metadata`는 응답 객체에 붙은 사용량 자료입니다. 사용자 질문 문자열의 길이를 센 값과 구분합니다. `usage.get("input_tokens")`는 딕셔너리에서 해당 키의 값을 읽고 키가 없으면 `None`을 반환합니다. 사용량 전체가 없을 때 `answer.usage_metadata or {}`는 계산이 중단되지 않도록 빈 딕셔너리를 준비하지만, 토큰을 0개 사용했다는 측정값을 새로 만드는 것은 아닙니다.',
'`time.perf_counter()`는 두 시점 사이에 지난 시간을 재기 위한 시계입니다. 날짜를 뜻하지 않습니다. 시작값을 저장하고 호출 반환 뒤 값에서 빼면 경과 초를 얻습니다. 예를 들어 차이가 1.5초라면 1000을 곱해 1500밀리초로 나타냅니다. 이 계산 예와 아래 실행에 저장된 실제 지연값은 구분합니다.',
'개념 설명 요청과 상품명 추출 요청을 각각 측정한다고 생각해 봅니다. 둘 다 입력·출력 토큰과 지연을 기록할 수 있지만 성공 기준은 다릅니다. 전자는 설명의 사실성과 이해 가능성을, 후자는 필요한 필드의 정확성을 확인해야 합니다. 공통 숫자를 같은 열에 모으는 것은 기록 형식을 통일하는 일이며 서로 다른 과제를 같은 난이도로 만드는 일은 아닙니다.'
],'<h2 id="b5">',7,[
'`time.perf_counter()`의 두 값을 빼면 그 사이의 경과 초를 얻고, 1000을 곱하면 밀리초입니다. 달력의 날짜와 구분하는 측정용 시계입니다. `usage_metadata`는 제공자가 응답에 담아 준 사용량 자료이며 질문 문자열의 글자 수가 아닙니다.',
'`usage.get("input_tokens")`는 키가 없으면 `None`입니다. `answer.usage_metadata or {}`는 자료가 없을 때 빈 딕셔너리를 준비하므로 다음 필드 확인이 가능합니다. 이 빈 자료를 사용량 0으로 판정하지 않습니다. 실행 상태를 먼저 읽은 뒤 실제 보고된 숫자만 비교합니다.',
'설명문 생성과 주문 정보 추출은 같은 기록 형식을 사용할 수 있지만 성공 기준이 다릅니다. 측정 열을 통일했다는 이유만으로 두 과제의 속도나 토큰 수를 모델 순위로 바꾸지 않습니다.'
])
(QA/'part2-edits.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print('revised',sum('source' in x for x in changes),'sections','generator pending',sum('generator_sync_pending'in x for x in changes))
