# Ch 21 검토 1차 — A (01~03절 + 챕터 공통)

검토일 2026-09-25 · 읽기 전용 · 노트북 재실행 0건

- 범위: `_src/01~03-*.html`, `labs/part6/ch21-create-agent/notebooks/01~03-*.ipynb`, `notebooks/runner_tools.py`(`f4113158…`, 188줄, 함수 열다섯), `pyproject.toml`·`uv.lock`, `figures/01-*`~`03-*`, `qa/upgrade/01~03-{diagnosis,figures,probe}.md`·`chapter-lead-notes.md`·`handoff.md`(챕터 공통 ~ §03 → §04)·`review-pack/01~03`, 과정 요약 §2-11·§2-12·§5, Ch 20 요약 §13, Ch 22 01·02, `textbook/downloads/part6-practice.zip`(목록만).
- 방법: 노트북 출력 글자 대조(파이썬), `upgrade_gates.check_section()`을 파일 쓰기 없이 직접 호출, AST 검사(노트북·도구 파일), 설치판 소스 행 확인, 가짜 키 글자로 **모델을 부르지 않는** 확인 세 가지(요청 본문 만들기 `_get_request_payload`, `ToolNode`만 넣은 작은 그래프로 경고·오류 재현), 공식 문서 WebFetch 셋(Structured output · Models · Tools). 임시 결과는 기기 `/tmp/reviewA21/`.

## 요약

| 절 | 판정 | 상 | 중 | 하 |
|---|---|---|---|---|
| 01 create_agent와 ReAct 루프 | accept with fixes | 0 | 0 | 2 |
| 02 구조화 출력 두 전략 | accept with fixes | 0 | 2 | 4 |
| 03 AgentState와 context_schema | accept with fixes | 0 | 0 | 3 (Ch 22·Ch 30 몫 둘 포함) |
| 챕터 공통(도구 파일·설치·그림·묶음) | accept with fixes | 0 | 1 | 3 |
| **합** | | **0** | **3** | **12** |

- 게이트: 세 절 모두 `check_section()` 직접 호출에서 G1~G7 **0건**(코드 셀 23·28·24, 문장 392·381·354).
- 사실 대조: 세 절 `_src` 본문(참고 자료 블록 제외)의 백틱 인용 중 숫자 든 값 **전부** 노트북 출력에 있음. 그림 12장 라벨 숫자 **전부** 출력에 있음. 출력에 없는 숫자는 챕터·절 번호·날짜·Python 판·소스 행 번호뿐.
- 흔들린 값(답 글·양식 칸 값·출력 토큰·예상 비용)은 세 절 모두 결과 읽기 둘째 단락에만 있고, 첫 단락·표·그림·정리·복습에는 없음(03의 A/B 불일치 넷 — 답 글 둘·`45`↔`44`·`0.000522`↔`0.000517` — 도 둘째 단락에만).
- 가장 무거운 것: **A-12**(01~04 설치 셀에 `numpy` 없음 — 설치 셀만으로 만든 환경에서 가져오기 셀이 멈춤, 규격 §2-7 6번) · **A-3**(02 노트북 5절 「`strict=True`를 더해 양식을 꼭 지키게 요청」은 설치판 요청 본문과 공식 문서와 다름) · **A-4**(02 11절 「표시가 참이면 제공자, 아니면 도구 전략」은 설치판 규칙의 절반 — 모델 이름 목록 단계가 빠짐).
- 다시 실행해야 하는 것은 **A-12 하나**(고치기로 정하면 01 5번·02 6번·03 4번·04 0번 요청). 나머지는 설명 셀·`_src`·`.mmd`·`chapter.json`만 고치는 일이라 `mdpatch.py` → `run_section.sh … --no-exec`·다시 렌더·`_build.py`로 됩니다.

## 발견 (절별)

### 01 create_agent와 ReAct 루프

**[하] A-1 도구 파일 설명이 05·06이 함수를 더한 뒤의 파일과 어긋남**
- 문제: 01은 도구 파일이 Ch 20 함수 다섯뿐이던 때(`eb408639…`)에 쓰였습니다. 지금 파일은 함수 열다섯·`import json`·`import numpy as np`(`f4113158…`)인데, 01 문장은 파일 전체가 Ch 20 함수 다섯인 것처럼 읽힙니다.
- 근거: `_src/01` b7 「도구 파일 `runner_tools.py`의 함수 다섯은 Ch 20 `graph_tools.py`의 본문을 글자 그대로 옮긴 것입니다.」 · 노트북 01 셀 [6] 「이 파일은 Ch 20 도구 파일 `graph_tools.py`와 다른 파일입니다. 이 챕터 노트북이 쓰는 함수만 Ch 20 파일에서 본문을 글자 그대로 옮겼습니다.」 · `runner_tools.py` 1~13행 독스트링(05·06·01·02 함수 설명)과 111~188행(Ch 14·15 함수 여덟).
- 권하는 고침: b7 「이 절이 가져오는 함수 넷과 그 안에서 쓰는 `tool_call_names`는 …」로 범위를 좁힘. 셀 [6] 둘째 문장 「이 절이 쓰는 함수는 Ch 20 파일에서 본문을 글자 그대로 옮긴 것이고, 뒤 절이 쓰는 함수도 같은 파일에 더해집니다」 꼴.
- 다시 실행: 아니요(`--no-exec`).

**[하] A-2 절 제목 표기 「create agent」·「context schema」(밑줄 빠짐)가 빌드 HTML 제목에 그대로 나감**
- 문제: 학생이 보는 HTML `<title>`·`<h1>`은 함수 이름과 다른 글자입니다. 같은 챕터 07 제목은 「create_agent 실습…」이라 챕터 안에서도 다릅니다. 노트북 제목 셀은 `# create_agent와 ReAct 루프`·`# AgentState와 context_schema`.
- 근거: `chapter.json` sections[0] 「create agent와 ReAct 루프」, [2] 「AgentState와 context schema」 · 빌드 `01-*.html` `<title>create agent와 ReAct 루프 — …` · `03-*.html` `<title>AgentState와 context schema — …`.
- 권하는 고침: `chapter.json` 제목 글자만 밑줄로(슬러그는 그대로) → `_build.py`·Part 목차. 01 진단 §11-1·03 진단 §12-4에 이미 「마감 몫」으로 적혀 있음.
- 다시 실행: 아니요.

### 02 구조화 출력 두 전략

**[중] A-3 「OpenAI 계열 모델이면 `strict=True`를 더해, 양식을 꼭 지키게 요청합니다」는 설치판 동작과 다름**
- 문제: 설치판에서 `strict=True`는 **함께 싣는 함수 도구(`lookup_policy`)의 명세**에 붙고, 양식(`response_format`) 쪽은 `ProviderStrategy`의 `strict` 기본값(주지 않음)에 따라 **`"strict": false`로 나갑니다.** 노트북 문장은 소스로만 본 동작을 반대로 읽었습니다.
- 근거:
  - 노트북 02 셀 [24] 둘째 단락 「OpenAI 계열 모델이면 설정 `strict=True`를 더해, 양식을 꼭 지키게 요청합니다.」(빌드 `02-*.html`에도 들어감).
  - `langchain/agents/factory.py` 1392~1394행 주석 「Redundantly set strict=True **on tools** for OpenAI-compatible models」, 1400행 `bind_kwargs["strict"] = True`.
  - `langchain/agents/structured_output.py` 280~293·307~308행 — `ProviderStrategy(schema, *, strict=None)`, `strict`를 줄 때만 `json_schema["strict"] = True`.
  - `langchain_openai/chat_models/base.py` 2433~2436행(도구는 `strict=True`로 변환) · 2482~2494행(`create_agent` 모양의 `response_format`이면 `strict`를 `json_schema`의 값으로 다시 읽어 `None` → `_convert_to_openai_response_format`에서 `False`).
  - 모델을 부르지 않는 확인(`/tmp/reviewA21/strict_check.py`, 가짜 키 글자, `_get_request_payload`): `tools strict: [True]` · `response_format … "strict": false …` · `parallel_tool_calls in payload: False`.
  - 공식 문서(docs.langchain.com Structured output, 2026-09-25): ProviderStrategy `strict` 「Defaults to `None` (disabled).」
- 권하는 고침: 「OpenAI 계열 모델이면 함께 싣는 도구 명세에 `strict=True`를 붙입니다(1392~1400행). 양식 자체를 꼭 지키게 하는 설정은 `ProviderStrategy(…, strict=True)`이고, 이 절은 주지 않아 기본값으로 보냈습니다.」 두 문장. 인계 「§01 → §02」 3항의 「strict=True를 더 붙임」도 같은 뜻으로 고쳐 두면 뒤 작업이 같은 오해를 되풀이하지 않습니다(07·마감 확인용).
- 다시 실행: 아니요(설명 셀만, `--no-exec`). 출력·결론·그림에는 닿지 않음.

**[중] A-4 양식 클래스를 그대로 넘겼을 때 전략을 고르는 규칙이 반쪽만 적힘**
- 문제: 설치판 `_supports_provider_strategy`는 기능 표 `structured_output`이 참이면 제공자 전략을 고르고, **참이 아니면 모델 이름을 정해 둔 목록과 한 번 더 견줍니다.** 그 목록에 `gpt-5.4-mini`가 들어 있어, 이 모델은 표시가 거짓이어도 제공자 전략이 골라집니다. 노트북의 「아니면 도구 전략」·「표시가 거짓인 모델에서는 도구 전략이 골라지고」는 값 바꿔 보기 해석의 일반 규칙으로 틀립니다.
- 근거: 노트북 02 셀 [54] 「소스로 보면 이 값이 참이면 제공자 전략을, 아니면 도구 전략을 고릅니다.」 · 셀 [60] 「표시가 거짓인 모델에서는 도구 전략이 골라지고, 그 경우는 이번에 실행하지 않았습니다.」 · `factory.py` 583~596행(기능 표 참이면 `True`) · 598~605행(아니면 `FALLBACK_MODELS_WITH_STRUCTURED_OUTPUT` 정규식과 견줌) · 174~194행 목록, 186행 `r"(^|[/:.])gpt-5\.4-(mini|nano)($|[-/:])"`.
- 권하는 고침: 셀 [54] 「이 값이 참이면 제공자 전략을 고릅니다. 참이 아니면 정해 둔 모델 이름 목록(174~194행)과 한 번 더 견주고, 거기에도 없으면 도구 전략을 고릅니다.」 · 셀 [60] 「기능 표와 이름 목록 어디에도 없는 모델에서는 도구 전략이 골라지고, …」. `_src` b4 「모델이 제공자 전략을 지원하지 않을 때 … 도구 전략」과 복습 4 해설은 그대로 참.
- 다시 실행: 아니요.

**[하] A-5 b6 표 「양식 클래스 그대로 · 양식 값이 온 자리 = 마지막 응답의 내용 글」은 노트북이 출력하지 않은 값**
- 문제: 11절은 메시지 칸 네 줄과 `structured_response`의 종류만 출력했고, 마지막 응답의 내용 글은 출력하지 않았습니다. 표 칸은 노트북 밖 확인(`02-probe.md` AS 「PS와 같음」)과 소스 추론입니다. 같은 표의 입력 토큰 칸은 「세지 않음」으로 정직하게 적어 서로 다릅니다.
- 근거: `_src/02` b6 표 셋째 줄 「마지막 응답의 내용 글」 · 노트북 셀 [57]·[59] 출력(내용 글 없음) · 02 진단 §6 표는 같은 칸을 「마지막 응답이 요청 0건(메시지 칸)」으로 좁혀 적음.
- 권하는 고침: 표 칸을 「마지막 응답(요청 0건) — 글은 출력하지 않음」으로. 그림 02-4 오른쪽 칸은 이미 양식 값 자리를 적지 않아 그대로.
- 다시 실행: 아니요.

**[하] A-6 그림 02-1 노란 상자에 소스로만 본 사실 「모델 노드가 붙인」이 섞임**
- 문제: 규격 §5-3(노랑은 출력 확인 값만, 소스는 「소스 확인 ·」 또는 회색). 도구 메시지 글 「Returning structured response」는 출력이지만 「모델 노드가 붙인」은 소스(1255~1276행)로만 본 것입니다. 같은 사실을 02-3은 「소스 확인 ·」 메모로 따로 적어 두 그림이 다릅니다.
- 근거: `figures/02-1-….mmd` `t3["모델 노드가 붙인 도구 메시지<br>Returning structured<br>response"]:::measure` · `02-3-….mmd` `Note over M: 소스 확인 · 모델 노드가 검사해 …` · 노트북 셀 [34] 「설치판 소스(`factory.py` 1255~1276행)로 보면, 이 도구 메시지는 … 모델 노드가 만듭니다.」
- 권하는 고침: 라벨을 「마지막 도구 메시지<br>Returning structured<br>response」로(누가 붙였는지는 02-3이 맡음), alt·도식 읽기 한 곳씩 맞춤.
- 다시 실행: 아니요(다시 렌더·노트북 첨부 교체·빌드).

**[하] A-7 b7 「`tools_to_model`이 끝으로 가는 것은 … 한 응답에 함께 올 때입니다」가 01의 「둘뿐」과 부딪힘**
- 문제: 01 셀 [24]는 끝으로 가는 경우를 「부르자마자 끝내는 설정의 도구」와 「구조화 출력용 도구」 둘로 적었습니다. 02 b7·셀 [36]은 조건 없이 한 경우만 적어, 나란히 읽으면 `return_direct` 경우가 사라집니다.
- 근거: `_src/02` b7 다섯째 줄 · 노트북 02 셀 [36] 「소스 2028~2030행으로 보면, `tools_to_model`이 끝으로 가는 것은 두 요청이 한 응답에 함께 올 때입니다.」 · `factory.py` 2018~2026행(모든 도구가 `return_direct`) · 2028~2030행(양식 도구 메시지가 있을 때).
- 권하는 고침: 「양식 도구 쪽에서 `tools_to_model`이 끝으로 가는 것은 …」 또는 「이 그래프에서는 …」으로 범위를 적음.
- 다시 실행: 아니요.

**[하] A-8 「기능 표」가 `_src` 본문에서 풀이 없이 쓰임**
- 문제: b1 학습 목표·b6·복습 4·b10이 「기능 표」를 쓰지만 `_src` 산문에는 뜻이 없고, 노트북 11절(셀 [52])에만 「모델 객체의 속성 `profile`에 담긴 딕셔너리」가 있습니다. 용어 표 밖 「일반 말」로 정한 것은 맞지만 처음 읽는 자리(b1)에서 무엇인지 알 수 없습니다.
- 근거: `_src/02` b1 셋째 항목 · b6 둘째 단락 · b9 4번 해설 · 노트북 셀 [52]. 공식 문서(Models, 2026-09-25)는 `model.profile`을 「supported features」 딕셔너리로 설명 — 이름을 쓰는 것 자체는 공개 API라 문제없음.
- 권하는 고침: b4 「비교와 경계」 마지막 문장에 「모델 객체의 기능 표(속성 `profile`, 지원하는 기능을 적은 딕셔너리)」를 한 번 풂.
- 다시 실행: 아니요.

### 03 AgentState와 context_schema

**[하] A-9 「노트북 밖에서 모델 없이 확인」 두 곳의 확인 방법과 「경고 두 줄」**
- 문제: 두 사실(대괄호 없는 `ToolRuntime`의 경고, 실행 정보를 빼면 오류)은 **참**입니다(아래 재현). 다만 03이 실제로 쓴 확인 대본(`probe/check03_warn_variants.py`·`check03_inject_flow.py`)은 `GenericFakeChatModel`을 상속한 대본 모델로 `create_agent` 흐름을 돌렸습니다. 규격 §3이 「가짜 모델」로 따로 부르는 것을 학생 본문에서는 「모델 없이」로 적어, 검토자가 방법을 되짚기 어렵습니다. 또 경고는 두 **건**이고 한 건이 여러 줄로 찍힙니다.
- 근거: 노트북 03 셀 [24] 「이 판에서는 그때 라이브러리 안에서 Pydantic 경고 두 줄이 함께 나와 … 노트북 밖에서 모델 없이 확인했고」 · `_src/03` b7 다섯째·여섯째 줄 · `probe/check03_warn_variants.py` 25~27행 `class ScriptModel(GenericFakeChatModel)`. 재현(모델·대본 모델 없이 `ToolNode`만 넣은 `StateGraph(LibraryState, context_schema=MemberContext)`, `/tmp/reviewA21/warn_repro.py`·`noctx.py`): `plain_tool | warnings: 2 | … | args: {} | spec: {'properties': {}, 'type': 'object'}`(두 건 모두 `UserWarning … PydanticSerializationUnexpectedValue(Expected \`none\` … field_name='context' …)`) · `generic_tool | warnings: 0` · 실행 정보를 빼면 `TypeError 'NoneType' object is not subscriptable`.
- 권하는 고침: 학생 본문은 「노트북 밖에서 모델을 부르지 않고 확인했습니다」와 「경고 두 건」으로. 03 진단 §3·`03-probe.md` §0-1에 대본 모델을 썼다는 사실은 이미 있으니 그대로 두고, 도구 실행 노드만으로도 같은 결과가 난다는 이 재현을 한 줄 더하면 근거가 단단해짐.
- 다시 실행: 아니요.

**[하] A-10 (Ch 22 몫) Ch 22 01 노트북 「타입 힌트는 … 실행 결과는 바꾸지 않습니다」가 03과 Ch 20 02의 가르침과 부딪힘**
- 문제: 03은 매개변수 표시 `ToolRuntime`을 라이브러리가 읽어 값을 넣고 명세에서 뺀다고 가르치고(출력 `check_my_loan | 입력 형식의 인자: [] | 명세의 인자: []`), 대괄호 유무가 경고를 바꾼다고 적었습니다. Ch 20 02의 받을 오류 표시 `error: ValueError`도 동작을 바꿉니다. 바로 다음 챕터 Ch 22 01 첫머리의 일반 문장은 이와 반대로 읽힙니다.
- 근거: `labs/part6/ch22-middleware/notebooks/01-미들웨어와-6개-훅.ipynb` 설명 셀(셀 4) 「타입 힌트는 함수가 받는 값의 종류를 적어 두는 표시입니다. 실행 결과는 바꾸지 않습니다.」 · 03 진단 §11·§12-3(「훅 힌트에 한정하면 참」, 고치지 않음).
- 권하는 고침: Ch 22 01 문장을 「이 훅 함수들의 타입 힌트는 …」으로 범위를 좁힘(설명 셀만 — `--no-exec`). 03 진단의 판단(훅 힌트에는 참)에는 동의하지만, 학생은 Ch 21 03 → Ch 22 01 차례로 읽으므로 한 구절을 고치는 쪽을 권합니다.
- 다시 실행: 아니요(Ch 22 쪽 설명 셀만).

**[하] A-11 (Ch 30 몫) Ch 30 01 「Ch21에서 Agent 실행 객체를 만들었습니다」가 03의 「실행 객체」와 뜻이 다름**
- 문제: 03은 「실행 객체」를 **도구 매개변수 `runtime`에 들어오는 객체**로 정했습니다(handoff 「03절에서 더한 것」 일반 말). Ch 30 01은 같은 말을 **에이전트 그래프**에 씁니다. 03 진단 §11 표에 이 줄이 없습니다.
- 근거: `textbook/part7/ch30-fastapi-serving/_src/01-비동기-라우팅과-스키마.html` 4행 b3 · `_generate.py` 11행 · 노트북 03 셀 [22] 「이 절에서는 이 표시를 실행 객체 표시라고 부릅니다」.
- 권하는 고침: Ch 30 작업 때 「Ch21에서 에이전트 그래프(`create_agent`의 결과)를 만들었습니다」로. Ch 21 파일은 고치지 않음 — 챕터 요약 「뒤 챕터 인계」에 한 줄.
- 다시 실행: 아니요.

### 챕터 공통

**[중] A-12 01~04 설치 셀에 `numpy`가 없는데 도구 파일 맨 위가 `import numpy as np`**
- 문제: 01~04 노트북은 가져오기 셀에서 `runner_tools`를 가져오므로 NumPy가 반드시 필요합니다. 그런데 설치 셀은 NumPy를 적지 않고, 준비물은 「첫 셀에서 패키지 다섯을 설치합니다」라고 적습니다. 규격 §2-7 6번(「`%pip`에 `numpy`를 적고 판은 실습 폴더 잠금과 같게」) 위반입니다.
- 영향(모델 없이 판단): 안내대로 실습 폴더에서 `uv sync --locked`로 만든 `.venv`에서는 멈추지 않습니다(`pyproject.toml` `numpy>=2.0`, 잠금 `numpy 2.5.3`, 기기 venv에서 `notebooks/`를 작업 폴더로 두고 가져오기 줄 둘을 실행해 `OK`). 설치 셀만으로 환경을 만들면 **멈춥니다**: 01 설치 셀 다섯 패키지(`langchain`·`langchain-core`·`langchain-openai`·`langgraph`·`python-dotenv`)의 잠금 의존 닫힘에 `numpy`가 없고(`uv.lock`에서 `numpy`를 요구하는 항목은 프로젝트 자신뿐), NumPy가 없는 상태를 흉내 내 가져오면 `ModuleNotFoundError import of numpy halted`가 납니다. 02·03·04도 같은 가져오기 줄이라 같은 자리(가져오기 셀)에서 멈춥니다. 05·06·07 설치 셀은 `"numpy==2.5.3"`을 적었습니다.
- 근거: `runner_tools.py` 17행 · 01 셀 [3] `%pip install -q "langchain==1.4.0" … "python-dotenv==1.2.3"`(02는 + `pydantic`, 03 = 01, 04는 + `langgraph-prebuilt`·`pydantic`) · 05·06·07 설치 셀 `"numpy==2.5.3"` · 05 진단 §5 「01~04 영향」 · handoff 284·344행(강사 확인 대상으로 올라가 있음).
- 권하는 고침: 01~04 설치 셀에 `"numpy==2.5.3"`을 더하고 판 출력 줄·준비물 「패키지 다섯」→「여섯」(02·04는 판 수에 맞게)과 결과 읽기 첫 줄을 새 출력으로. 다시 실행하지 않기로 정하면, 적어도 01 준비물에 「도구 파일이 NumPy를 가져오므로 실습 폴더 `.venv`(잠금에 NumPy 있음)로 실행합니다」 한 문장을 넣어 규격 예외를 학생에게 밝혀야 합니다.
- 다시 실행: **예**(설치 셀 코드가 바뀜 — 01 5번 · 02 6번 · 03 4번 · 04 0번 요청, 규격 §2-7 9번대로 새 커널 두 번). 다시 실행하면 01~03 둘째 단락 값(답 글·출력 토큰·예상 비용)이 바뀔 수 있고, 03은 이미 A/B에서 넷이 갈렸음.

**[하] A-13 챕터 안 그림 색이 `create_agent` 상자에서 갈림(01-1·05-1 파랑 ↔ 07-1 회색)**
- 문제: 규격 §5-3 「같은 요소는 … 같은 색」은 절 안 규칙이지만, 실습 절 07-1은 01·02·03 부품을 조립해 보이는 그림이라 학생이 01-1과 나란히 봅니다. 같은 `create_agent` 한 줄이 두 색입니다.
- 근거: `figures/01-1-….mmd` `mk["create_agent 한 줄"]:::flow` · `05-1-….mmd` `mk["create_agent<br>…"]:::flow` · `07-1-….mmd` `mk["create_agent 한 번<br>…"]`(클래스 없음) · `07-figures.md` 5행(01-1과 다르다는 것을 알고 둠)·07 진단 §12-4.
- 권하는 고침: 07-1 `mk`를 `:::flow`로(01·05 쪽이 둘이라 맞추기 쉬움) — 07 몫(검토 B와 겹치면 B 판단 우선).
- 다시 실행: 아니요(다시 렌더).

**[하] A-14 (마감 몫) 묶음 목록·실습 폴더 README가 지금 챕터와 다름**
- 문제: 학생 묶음 `part6-practice.zip`(2026-09-25 05:57)에는 Ch 21 파일 12개가 모두 들어 있고 디스크 파일과 해시가 같습니다(도구 파일 `f4113158…` 포함). 그러나 허용 목록 두 곳에는 07 노트북이 없고(챕터 `qa/public-files.json`은 07 HTML도 없음), README는 옛 판입니다.
- 근거: `textbook/part6/public-files.json` 2~12행(01~06 노트북·도구 파일·잠금 — 07 없음) · 챕터 `qa/public-files.json`(HTML 01~06·노트북 01~06) · zip 목록에 `notebooks/07-create-agent-실습.ipynb` 있음 · README 「절당 예상 비용은 1달러 미만입니다」, 01~06 도구 파일·`uv sync --locked`·`notebooks/`에서 열기 단락 없음.
- 권하는 고침: 두 목록에 07 줄을 더하고 `check_delivery.py`로 확인 · README 다시 쓰기(handoff 345행 목록 그대로). 06 계약 파일 `data/rag-comparison.json`은 목록에 이미 있음.
- 다시 실행: 아니요.

**[하] A-15 (05 몫) 도구 파일로 옮기며 줄인 주석을 진단에 적지 않음**
- 문제: 도구 파일 함수 열다섯은 모두 처음 가르친 곳과 **def 줄~끝 줄 글자와 AST가 같습니다**(아래 「확인한 것」). 다만 `cosine_distance`는 Ch 14 판 주석 둘째 줄 「Ch 12 01절 판은 바깥 이름 similarity_top을 읽었고, 이 판은 같은 값 1을 함수 안에서 정합니다」를 잃었고, `search_hits`는 주석 두 줄을 다시 썼습니다. 규격 §4(2026-09-20, Ch 14 검토 A A-3)는 옮기며 줄인 주석을 진단과 챕터 요약에 한 줄로 적게 합니다. 05 진단 §5는 「주석 머리는 이 파일 모양으로 다시 적고」까지만 적었습니다.
- 근거: `runner_tools.py` 122~127행 ↔ `labs/part4/ch14-rag-patterns/notebooks/rag_tools.py`의 `cosine_distance` 위 주석 두 줄 · `search_hits` 위 주석(Ch 14 「06절에서 배웠습니다 — …」·「06절 판은 바깥 이름 embedding_model·doc_vectors·doc_ids·top_all을 읽었고 …」) ↔ 이 파일 153~155행.
- 권하는 고침: 05 진단 §5와 챕터 요약에 한 줄씩(코드는 그대로 두어도 됨 — 사라진 줄은 Ch 12 판 차이 설명이라 이 파일에서는 필요가 적음).
- 다시 실행: 아니요.

## 확인한 것 (문제 없음)

- **모델 설정**: 01~03 모든 `create_agent` 호출(01 1곳 · 02 3곳 · 03 2곳)이 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`로 만든 **모델 객체**를 받음(AST). 가짜 키 글자로 만든 요청 본문에 `temperature`·`reasoning_effort`가 들어가고 `parallel_tool_calls` 키는 없음. 키는 노트북이 과정 표준 `find_dotenv(usecwd=True)`, 흔들림 대본 셋은 루트 `.env`(`load_dotenv(ROOT / ".env")`)에서만, 키 값 출력 0. 노트북·대본에 시간 재기(`perf_counter` 등)·`draw_mermaid_png`·`stream` 0건(준비물 「10초 안에」는 셀 실행 기록 값).
- **Ch 20 인계**: `POLICIES` 셀은 Ch 20 01과 01·02·03 모두 문자열까지 같음, 도구 셀은 주석 한 줄만 다르고 01·02·03끼리는 같음(01 셀 [14]이 그 한 줄을 밝힘). 01 셀 [41]은 Ch 20 01 9절 셀과 글자까지 같음. 02 시스템 메시지 글 = 01. Ch 20 01 출력(구조 문자열 `tools --> model`, `고정 엣지로 적은 수: 2`, 표 2·1·3 / 1·0·2)과 01 본문 표·그림 01-4 회색 상자 값 일치. `tools_condition` 미사용은 출력과 `factory.py` 28행 둘 다. 「여럿 담기 값을 보내지 않음」은 1431~1436행·1476행(`tool_choice=None` — 진단·인계가 적은 1474행은 두 줄 위 `response_format` 줄, 학생 본문에는 없음)과 요청 본문으로 확인. b6 둘째 단락 「한 가지만 바꾼 비교가 아닙니다」 공개 있음. Ch 20 요약 §13 1~9 반영(5·6은 b7 한 줄씩).
- **설치판 행 번호**: `factory.py` 28 · 995~996 · 1024~1036 · 1089 · 1174~1192 · 1204~1219 · 1255~1276 · 1357~1367 · 1391~1404 · 1423 · 1431~1436 · 1450~1454 · 1678~1685 · 1702~1705 · 1923~1975(`Send("tools", [tool_call])` 1964) · 1953~1968 · 2004~2037 · 2028~2030 · 916~922, `middleware/types.py` 349~355, `tool_node.py` 802~817·1663~1720, `langchain_core/tools/base.py` 331~340, `graph.py` 639·`graph_mermaid.py` 422~423, `langchain_openai/…/base.py` 2427~2428 — 모두 본문 설명과 맞음. 01 b7 「오류 처리 인자 기본값이면 `ValueError`가 올라와 멈출 것으로 보임」은 `_default_handle_tool_errors`(383~391행)와 맞고 「실행하지 않았습니다」로 한정됨.
- **02 비교 값**: 메시지 5 대 4, 응답 2·2, 도구 메시지 2·1, 입력 토큰 572(261+311)·768(359+409)은 노트북 출력·밖 다섯 번·A/B에서 같음. 입력 토큰 차이의 원인은 셀 [50]·b6·b7 모두 「나눠 세지 않았다」로만 적음(원인을 가른 것처럼 쓴 자리 0). `tools_to_model` 갈 곳 출력 해석(도구 전략 `['model', '__end__']` ↔ 제공자 `['model']`, 「실제로 그 갈래로 끝난 장면은 없음」) 맞음. 값 바꿔 보기 해석 「그래프는 도구 전략 모양, 메시지 칸은 제공자 모양」은 출력과 소스(1024~1036·1357~1367행)로 맞음(규칙 서술만 A-4). 「스키마」 0건, 원어 schema 노트북·`_src` 한 번씩, 「프로필」 0건(「기능 표」). `profile`은 공식 Models 문서의 공개 속성. `pydantic==2.13.5`는 잠금 판과 같음.
- **03**: `LibraryState(AgentState)`는 `AgentState`가 `TypedDict`(`types.py` 349행)라 사실상 칸만 적은 `TypedDict` 양식 — G1이 이름 목록(`SCHEMA_BASES`)으로만 봐서 잡는 것이고, `upgrade_allow=["class_def"]`는 그 셀 하나에만 있고 그 셀의 다른 검사는 그대로 받음(범위 넘지 않음). `MemberContext(TypedDict)`는 G1 허용 모양. `runtime.context["…"]` 딕셔너리 읽기, `invoke(…, context={…})`, 도구 명세에서 `runtime`이 빠지는 출력, `AgentState is middleware.AgentState` → `True`(Ch 22 01이 `langchain.agents.middleware`에서 가져오는 것과 같은 클래스), Ch 20 01 우리 상태 형식 `AgentState`와의 구분(셀 [16]·b3), 「실행 정보」와 Ch 8 01 「컨텍스트(모델이 받은 글 전체)」 구분 한 문장(셀 [20]·b4) 모두 있음. `ToolRuntime[MemberContext]` 대괄호의 까닭(경고 2건 ↔ 0건)은 모델 없이 재현됨(A-9), 공식 Tools 문서도 컨텍스트를 읽는 도구를 `ToolRuntime[UserContext]`로 적음.
- **도구 파일**: 함수 열다섯 모두 처음 가르친 곳과 def 줄~끝 줄 **글자와 AST가 같음** — Ch 20 `graph_tools.py` 다섯 · Ch 21 01 노트북 `agent_row` · 02 노트북 `print_branches` · Ch 14 `rag_tools.py` 여섯(`find_gold_rank` 포함) · Ch 15 `rag_tools.py` 둘(`build_judge_prompt`·`judge_once` — `estimate_cost`·`find_gold_rank`는 Ch 15 판과도 같음). 함수마다 「# Ch NN MM절에서 배웠습니다 — …」 주석. 도구 파일 AST: 금지 문법·f-string·반환 힌트·기본값 매개변수·튜플 풀기 0, 예외는 `estimate_cost`의 `.get` 둘(Ch 6 06 원본). 01~03이 가져오는 이름(`call_id_lists`·`estimate_cost`·`show_messages`·`sum_usage`·`agent_row`·`print_branches`)이 지금 파일에 있고 `notebooks/`에서 가져오기 됨, 실습 폴더 맨 위에서는 `ModuleNotFoundError`(준비 셀 결과 읽기의 「커널이 `notebooks/` 폴더에서 시작해야」와 맞음). 고정 세 문장 01·02·03 셀 [6]에 있음. 묶음 목록 두 곳에 도구 파일 줄 있음.
- **코드 사다리(노트북 AST)**: 01~03 f-string·내포식·`lambda`·조건 표현식·`next`·`sum`·`sorted`·`enumerate`·`getattr`·`isinstance`·`+=`·튜플 풀기·`try`·기본값 매개변수·반환 힌트 0. 힌트는 `topic: str`·양식 칸·`ToolRuntime[MemberContext]`만. 두 겹 호출 0(한 겹 `round(estimate_cost(…), 6)`만, 02·03). 클래스 셋(`PolicyAnswer(BaseModel)`·`LibraryState(AgentState)`·`MemberContext(TypedDict)`) 모두 칸만. 처음 쓴 속성 `builder`·`channels`·`nodes["tools"].runnable`·`branches[…][…].ends`·`profile`·`ToolRuntime`은 모두 처음 쓰는 자리 앞 설명 셀에서 한 문장씩 풂(`builder` 계열은 공식 문서에 없는 속성 — 01 진단 §11-3 강사 확인 대상).
- **assert**: 01 호출 ID 짝 · 02 `structured_response` 종류·호출 ID 짝 · 03 `ticket_no` 값·도구 메시지 속 이용자 번호(도구 몸통이 만든 글, 도구 메시지가 있을 때만)·호출 ID 짝 — 모델 글에 건 것 0.
- **흔들림 확인**: 01(L·G·T 각 5/5), 02(TS·PS·AS 각 5/5), 03(R0·R3 각 5/5) 모두 규칙을 첫 요청 전에 적었고(`NN-probe.md` §0 시각이 요청보다 앞섬), 결론에 쓴 모양(메시지 종류·수·도구 이름과 인자·응답 수·입력 토큰)이 다섯 번과 A/B에서 같음. 탐색으로 고른 입력 없음 — 질문·시스템 메시지 글·양식·실행 정보 값은 확인 전에 정했고 b7 「흐름을 보여 주려고 정한 예」 있음.
- **그림**: Mermaid 12장 원본 폭 326~860(모두 868 이하), 빨강 0, 보라는 sequenceDiagram `box Lavender` 띠만(01-3·02-3·03-3), 조건 함수는 상자 없이 점선 라벨, 나란한 칸은 `~~~`, `.caption.md` 15개가 `_src` 캡션과 같음, alt·도식 읽기가 `.mmd`와 맞음(A-6 한 곳 말고). 삽화 셋은 `.prompt.md`의 채택 기록·그림 읽기가 서로 맞음(글로 판단).
- **용어·금지어**: 01~03 `_src`·노트북 설명 셀·코드 주석·캡션·`.mmd`에서 handoff 금지어 목록 + 「지시」·「주입」·「런타임」·「프로필」·「네이티브」 등 0건(허용 말 「캐시 입력」, 제목·원어 풀이 한 번씩 말고). 용어 표 셋(각 3개, meta 「새 용어 3」과 같음)이 과정 요약 §5 Ch 7·8·13·16·19·20 말과 부딪히지 않음. b8 다음 절 문장 01→02·02→03·03→04가 다음 절 내용과 맞음. 뒤 챕터 문장: Ch 22 01 `_src` 4·9행, Ch 27 01·02 b3, Ch 30 03·09 b3는 뜻이 참(Ch 30 03 「사전」은 Ch 30 몫), Ch 30 01만 A-11.
- **시수**: 01~06 meta 강의 합 6h·실습 합 10h = `chapter.json` 「강의 6h · 실습 10h」, 07은 30분(더하지 않음).

## 사람이 정해야 할 것

1. **A-12 NumPy**: 01~04 설치 셀에 `"numpy==2.5.3"`을 더하고 다시 실행할지(요청 15번 + 04 0번, 01~03 둘째 단락 값이 바뀔 수 있음), 아니면 「`.venv`로 실행」 안내 한 문장으로 예외를 밝히고 두는지.
2. **03 `ToolRuntime[MemberContext]` 대괄호**(챕터 리드 결정의 예외): 까닭(대괄호 없으면 Pydantic 경고 2건)은 모델 없이 재현됐고 공식 문서 모양과 같음 — 검토 A는 그대로 두는 쪽을 권함.
3. **03 `upgrade_allow=["class_def"]`**: `AgentState`가 `TypedDict`라 규격 L5 뜻 안이라고 보고 셀 예외로 두는지, 게이트 `SCHEMA_BASES`에 `AgentState`를 더하는지(게이트를 바꾸면 전 챕터 재검사).
4. **A-10 Ch 22 01 문장**을 설명 셀만 고쳐(`--no-exec`) 범위를 좁힐지, 03 진단대로 기록만 둘지.
5. **공식 문서에 없는 속성**(`builder`·`channels`·`nodes[…].runnable`·`branches[…][…].ends`)을 결정적 비교의 근거로 계속 쓸지 — 판을 잠가 두어 지금은 돌지만, 판을 올리면 먼저 깨질 자리.
6. **코드 줄 증가**(01 39→124 · 02 33→157 · 03 35→129): 절마다 되풀이되는 사용량·예상 비용 셀 둘(+ 결과 읽기)은 02·03에서 결론에 닿지 않음(「어느 전략이 싸다고 말하지 않습니다」). 02·03에서 빼거나 한 셀로 줄일지(빼면 다시 실행).
7. **A-13 그림 색**: `create_agent` 상자를 챕터 전체에서 파랑(우리가 적은 한 줄)으로 맞출지, 회색(라이브러리)으로 맞출지.
8. **02-5 삽화**(02 진단 §12-3): 오른쪽 셔츠가 개어진 채가 아니라 틈에서 늘어져 나와 비유 「개어진 채 나온다」와 어긋남 — 다시 만들지(2크레딧), 그림 읽기대로 둘지.
9. **A-2 제목**: 「create_agent」·「AgentState」·「context_schema」를 제목에 API 이름 그대로 둘지(밑줄 표기 포함) — handoff 챕터 리드 결정 10의 강사 확인 대상.
