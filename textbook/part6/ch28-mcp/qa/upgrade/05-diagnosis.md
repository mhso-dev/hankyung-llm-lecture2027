# 05절 진단과 개선 기록 — 도구 정의와 첫 호출 토큰 (experiment, 본문 마지막 절)

- 작업일 2026-09-28 · 작업자: 05절 담당 · 생성기 `qa/upgrade/author_05.py`(`df4d186d…`) · 흔들림 확인 `qa/upgrade/05-probe.md`·`probe/probe05.py`(`8ab1193a…`)·`probe/probe-05-P.jsonl`(`1d29a28f…`) · 슬러그 그대로.
- 읽은 것: `handoff.md`(챕터 공통·§04→§05 전부, 나머지 훑음) · `chapter-lead-notes.md`(§0·§1·§2 05·§4-4·§8·§9) · `04-diagnosis.md`·`04-probe.md`(전부) · `author_04.py`(전부)·`author_03.py`(도구 파일 사슬)·`author_02.py`(셀 글) · `probe/probe04.py` · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md` §1~§10 · 과정 요약(Ch 5·6·19·27 줄, §2-11·2-18·결론 태도) · Ch 19 03 노트북(`spec_length` 셀)·Ch 19 04·Ch 27 03·Ch 6 06·Ch 5 01 `_src`(b3 대조) · Ch 29 01 `_src`(b8). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 6 | 97 | 4 | 3 | 0(실제로는 여섯 모두 틀 문장) | 1 | 8 | 21 | 3 | **40** |
| 첫 실행 전(`--label wip-05`) | 28 | — | 0 | 0 | 0 | 0 | 0 | 7 → 0 | 3(그림 전) | — |
| 후(`gates-wip-05.json`·`gates-wip-05-05.json`, `--no-exec`) | **28** | **410** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 7건: 70자 넘는 문장 5(b7·b10의 규격·소스 행 문장 — 괄호 「(SHOULD).」 뒤가 한 문장으로 이어짐) · 영문 시작 2(「MCP로 …」 → 「MCP 서버에서 …」). 실행 전에 고쳤습니다. `gates-wip-05-05.json`은 첫 실행 전 값을 담았다가 그림 뒤 같은 이름으로 다시 돌려 지금은 0건 판입니다.
- 코드 줄(`count_code.py` — 주석·빈 줄 빼고 `%pip` 셈) **99 → 173**(코드 셀 6 → 28). 도구 파일 `connect_tools.py` 코드 줄 57(04 판보다 함수 하나·가져오기 둘). 옛 판은 한 셀에 판 확인·키·`.env` 찾기(15줄)·서버 둘과 도구 다섯·요청 셋을 몰아 적었고, 새 판은 명세 모양·글자 수·바꾼 조건·첫 요청을 셀마다 나눠 실행(강사 확인 대상).
- AST 따로(`/tmp/ch28-05/tools/extra_check.py` — 04 판 + 데코레이터 허용 표시 `tool('lookup_policy')`·`longer.tool`·`server.tool`): 금지 문법 0건. 허용 표시 — 노트북 데코레이터 넷(직접 도구 `@tool("lookup_policy")` — Ch 19 04 공개 이름 선례 · 연습 서버 `@longer.tool` · 서버 객체 `@server.tool` 둘 — 02 선례)과 그 함수 매개변수 단순 힌트·독스트링(챕터 예외) · 도구 파일 `async def`·`try`(02 셀 글)·`estimate_cost`의 `.get` 둘(Ch 6 06·Ch 21 판). 노트북 `try` 0·클래스 0. 호출 깊이 최대 2(`depth.py`), 준비 셀 밖 셀 최대 10줄(`TABLE`·`COST`), 셀당 정의 하나.
- 금지어(`ban28.py` — 01 판 그대로): 노트북 설명·주석·`_src`·캡션·`.mmd` 걸린 것 3 — 모두 「캐시 입력」(Ch 6 06 말, 「캐시」 단독 아님). 모델 답 글 속 「명시」는 결과 읽기 둘째 단락에서 백틱으로 인용(모델이 쓴 글). 사용자가 금지한 표현(「한 겹 더」 등) 0.

## 2. 수정 전 주요 문제 (옛 판 — `qa/upgrade/before/`)

1. **G4 `temperature` 누락**: `init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none")`.
2. **한 번 실행한 값을 핵심 개념 본문에**: b4 「같은 158 입력 토큰」·「316 토큰」(흔들림 확인 없이 결론처럼) · b6 「직접 도구 한 개와 MCP 도구 한 개는 같은 input_tokens」.
3. **모델 값 `assert`**: `measurements["mcp_5"]["input_tokens"] > measurements["mcp_1"]["input_tokens"]` · `usage is not None and reply.tool_calls`(모델 판단) · `total_cost < 1.0`.
4. **자체 `schema_chars`**: 이름·설명·`model_json_schema()`를 `sort_keys=True`로 JSON 글로 — 모델에 보내는 명세와 달라 직접 도구 289 ↔ MCP 216으로 **거꾸로** 나옴(명세로 세면 221 ↔ 252) · 조건 표현식·내포식·`isinstance`.
5. **세 조건이 여러 가지가 함께 바뀜**: 도구 이름(`direct_lookup` ↔ `lookup_policy`)·도구 수·설명 글(다섯 도구는 짧은 설명)·`tool_choice="required"`(과정 처음, 풀이 0). 루프 안 `async def read_only(query: str, _name: str = name)`(기본값 매개변수·루프 안 정의)·`read_only.__name__ = …` 속성 대입·f-string·반환 힌트 `-> list`·`-> dict`.
6. **틀린·옛 문장**: b3 「MCPAdapter가 MCP 도구를 **BaseTool**로 변환」(`StructuredTool`) · b2 「Ch19에서 도구 개수가 늘면 **선택 정보**가 커진다」(Ch 19 03은 명세 글자 수로만 — 토큰은 안 셈) · b2 「프로토콜 도입 자체」 · b4·b7·복습 「MCP JSON-RPC 전송 바이트는 usage_metadata에 포함되지 않습니다」(참이나 이 절이 잰 값이 아님, 메모리 연결이라 전송 자체가 없었음) · b8 「**Ch37**에서는 …」(교재에 없는 챕터) · b8 정리 셋이 이 절과 무관(「인증과 인가를 통과한 범위」 등) · b10 스펙 2025-11-25·FastMCP **v2** 링크·확인 2026-09-11 · b7 「2026-09-11 … 단가 가정」.
7. **문법·셀**: `next`+별표 풀기(`.env` 찾기)·틀 문장 첫 줄 주석 여섯·결과 읽기 0·코드 셀 15~20줄 셋·`1_000_000`·`round(…, 8)`·`sum(… for …)`, 금지어(측정 8·직렬화 8·스키마 7·필터링·토큰화·수치·공급자·추정·실측·프로토콜·반환).

## 3. 바꾼 것 — 노트북 차례 (코드 셀 28, 마크다운 32)

| 절 | 셀 | 하는 일 |
|---|---|---|
| 1 준비 | 1 설치(setup — 여섯 판, 잠금과 같음, 04와 달리 `langgraph`·`psutil` 없음) · 2 가져오기(setup — 04처럼 베타 경고 한 종류만 끔, `json`·`runpy`·`tool`·`convert_to_openai_tool`·`FastMCP`, 도구 파일 함수 다섯) · 3 키(nbkit) · 4 모델(nbkit, `temperature=0`·`reasoning_effort="none"`) | 요청 없음 |
| 2 도구 정의 → 도구 명세 | 5 파일 위치(01 셀 글 그대로) · 6 조용히 하는 세 이름(03 셀 글 그대로) · 7 `MCPAdapter(stdio_config(…)).list_tools()` → `['lookup_policy']`·입력 형식 · 8 `convert_to_openai_tool` → 칸 `['type', 'function']`·`['name', 'description', 'parameters']`·`parameters` = 입력 형식 `True` · 9 JSON 글·`글자 수: 252`·`spec_length` 252 · 10 `model.bind_tools(mcp_tools).kwargs["tools"]` = 명세 `True`(요청 0) | 모델 없음 |
| 3 직접 도구 | 11 `runpy.run_path` → 서버 객체·규정 딕셔너리(02 6절 모양) · 12 `@tool("lookup_policy") def direct_lookup(topic: str)`(같은 이름·설명) · 13 이름·설명 같음 `True`·`additionalProperties` 없음·221 ↔ 252·차 31 | 모델 없음 |
| 4 설명 길이·도구 수 | 14 `longer = FastMCP("설명을 늘린 자료실")` + `@longer.tool` 설명 두 문장 더함 · 15 메모리 연결 `MCPAdapter(longer)` → 입력 형식 같음 `True`·설명 같음 `False` · 16 299·늘어난 명세 47 = 늘어난 설명 47 `True` · 17·18 `@server.tool` `search_topics(word: str)`·`show_topics()`(서버 파일은 그대로) · 19 `MCPAdapter(server)` → 도구 셋·첫 명세 = 2절 명세 `True` · 20 도구 1·2·3 → 252·503·685 | 모델 없음 |
| 5 첫 요청 입력 토큰(실제 모델) | 21 `first_messages`(04 에이전트와 같은 시스템 메시지 글·질문) · 22 도구 없음 `model.invoke` → 56·답 글 · 23 MCP 도구 하나 187 · 24 직접 도구 하나 187 · 25 설명을 늘린 도구 218 · 26 도구 셋 252 · 27 도구 정의 몫 131·131·162·196 · 28 출력 토큰·예상 비용 합 | 모델 요청 5번(도구는 부르지 않음, `tool_choice` 없음) |

## 4. 챕터 리드 결정 적용

1. **앞 절반 모델 없음(결정적, 요청 0)**: Ch 19 03 `spec_length`(셀 글 그대로 도구 파일에 더함)로 MCP 도구 명세 글자 수, 입력 형식 모양·설명 길이·도구 수를 **하나씩** 바꾼 조건(바꾸는 것 하나 — 이름·설명·입력 형식이 같은지 코드로 확인). 자체 `schema_chars`는 뺐습니다. 04 인계 참고값 252는 새 커널 두 번에서도 252. 준비 노트의 「직접 223 ↔ MCP 254」는 다른 설명 글로 잰 값이라 쓰지 않음(이번 설명 글로는 221 ↔ 252).
2. **뒤 절반 실제 모델**: 과정 표준 모델 객체(nbkit)·`temperature=0`. 조건 다섯(도구 없음 · MCP 하나 · 직접 하나 · 설명을 늘린 하나 · MCP 셋)에 같은 `first_messages`로 `bind_tools(...).invoke` 한 번씩. **MCP 도구가 비동기뿐이어도 모델의 동기 `invoke`로 첫 요청을 보낼 수 있음**(도구 몸통을 부르지 않음 — 04 인계 3번 확인, 새 커널 두 번 PASS).
3. **흔들림(노트북 밖 조건마다 5번)**: `05-probe.md` §0을 **21:52:17Z**에 적고(파일 수정 시각 같음) 첫 요청이 든 회차 1은 **21:52:29Z** 시작 — §0이 12초 먼저. 입력 토큰 다섯 조건 모두 5/5 같음(56·187·187·218·252), 새 커널 A·B도 같은 값 → 결론·정리·복습·그림 라벨에 「흔들림 확인 다섯 번과 두 커널에서 모두」 한정어와 함께 씀. 옛 158·316은 어디에도 쓰지 않음.
4. **`assert`**: 파일 찾기 셀(01 셀 글)과 키 셀뿐. 모델 값·구조 값 비교는 참거짓 출력으로만.
5. **「예상 비용」**: Ch 6 06 뜻 그대로 도구 파일 `estimate_cost`(응답의 `usage_metadata`를 그대로 넘겨 캐시 입력 칸까지 셈) + 요금표 2026-09-17 mini 0.75·0.075·4.50, 「청구 금액 아님」.
6. **b3·b8·b10**: b3 새로(Ch 5 01·Ch 6 01·02·06·Ch 19 01·03·04·Ch 27 03·01~04절) — 「BaseTool」 뺌. **b8 「Ch37」 → Ch 29 01**(평가 방법 세 가지를 견준다고만 — 앞당겨 가르치지 않음, 「궤적」은 금지어라 안 씀). 06 실습 절이 생기면 이 링크를 06으로 고칠 몫(인계). b10 새로(MCP 2026-07-28 Tools·OpenAI Function calling·LangChain MCP·설치판 소스 행, 확인 2026-09-28).
7. **용어**: 01 표·금지어 그대로 + 새 말 둘(**첫 요청** · **도구 정의 몫** — meta 「새 용어 2」), 이어 쓴 말 **도구 명세**·명세 글자 수(Ch 19 03). 모델 토큰은 「입력 토큰」·「출력 토큰」(03의 「접근 토큰」과 가름).
8. **비유**: 「우주 정거장 도킹 포트」 — 관제실이 보급선을 부를 때마다 모듈마다 설명서 한 권씩 먼저 실어 보냄 → 모듈 수만큼 짐이 늘어남. 비유와 다른 점(글자 수와 입력 토큰은 같은 비율이 아님 · 직접 도구는 31자 짧아도 같은 입력 토큰) b4에.

## 5. 설치판·명세 확인 (2026-09-28, langchain 1.4.0·langchain-core 1.6.2·langchain-openai 1.6.0·fastmcp 4.0.3·mcp 2.2.0)

- 노트북 밖 탐색 `/tmp/ch28-05/exp/x1_spec.py`(`PYTHONDONTWRITEBYTECODE=1`, 모델 객체는 가짜 키 글로 만들기만, **요청 0**): MCP 명세 252·`parameters` = `args_schema` · 직접 `@tool("lookup_policy")` 221(키 차례 `properties·required·type`, 차 31 = `, "additionalProperties": false` 글자 수) · 설명을 늘린 판(탐색 때는 **다른 설명 글** — 313·+61, 노트북 글로는 299·+47) · `@server.tool`은 함수를 그대로 내놓음(`function`) · 메모리 연결 도구 셋 차례 `lookup_policy·search_topics·show_topics`(붙인 차례와 알파벳 차례가 같게 이름 지음) · 셋 가운데 첫 명세 = stdio 명세 `True` · `bind_tools(...).kwargs["tools"]` = 명세 · `_get_request_payload` 모양은 chat completions(`messages`·`tools`), Responses API 아님(`_use_responses_api` `False`) — 이 도구 칸이 그대로 실림.
- 소스 행: langchain-core `utils/function_calling.py` 345~352(딕셔너리 입력 형식 ↔ 양식 클래스 갈래, 121~151 딕셔너리는 제목 칸만 빼고 옮김) · langchain `agents/factory.py` 998~1004(`system_prompt` → `SystemMessage`)·1431~1438(모델 부를 때마다 `bind_tools(final_tools, tool_choice=request.tool_choice)`)·1500~1505(비동기 — 시스템 메시지를 맨 앞에 두고 `ainvoke`) → 04 에이전트 첫 요청과 05 MCP 하나 조건은 같은 모양(소스로만 — 04 흔들림 확인의 첫 요청 입력 토큰 187과 05 MCP 하나 187이 같은 수인 것은 진단에만 적음, 본문에는 교재에 없는 값이라 안 씀).
- WebFetch(확인 2026-09-28): MCP `specification/2026-07-28/server/tools`(「Servers SHOULD return tools in a deterministic order … improves LLM prompt cache hit rates when tools are included in model context」·「The set MAY vary by the authorization presented on the request」·인자 없는 도구 `{"type":"object","additionalProperties":false}` Recommended) · OpenAI `developers.openai.com/api/docs/guides/function-calling`(「Functions are injected into the system message in a syntax the model has been trained on … billed as input tokens」, 처음 싣는 함수 수·설명 줄이기 권고 — `platform.openai.com` 주소는 503) · LangChain MCP(「discovers a server's tools and adapts them into LangChain tools」, `langchain.mcp`는 베타).

## 6. 흔들림 확인과 새 커널 두 번 · 프로세스

- **흔들림(노트북 밖 조건마다 5번, `05-probe.md`)**: §0 21:52:17Z → 첫 요청 21:52:29Z → 21:52:51Z 끝. 요청 25번, 서비스 오류 0. 입력 토큰 5/5(다섯 조건 모두) · 도구를 알린 네 조건은 다섯 번 모두 `lookup_policy` `{'topic': '운영'}`·출력 18 · 도구 없음 조건은 출력 26~40·답 글 다섯 번 모두 다름(셋은 규정에 없는 「오전 9시부터 오후 1시까지」, 둘은 「확인되지 않음」). §0 괄호의 long 참고값 313은 탐색의 다른 글로 잰 값 — §1에 바로잡음(입력은 §0 본문대로).
- **A(교재 출력)**: `run_section.sh … 05` → `PASS 05-도구-정의와-첫-호출-토큰.ipynb: 28 cells`, `executed_at` 2026-09-28T22:08:27Z, `code_sha256` **`b99a57642e5d4b491129209a59dbed2f909a8510b0b546d949620de1e91b885f`**, `outputs_sha256` `a080eff1…`. 그림 첨부 단계에서 멈춤(05-1 PNG가 아직 없음 — 의도한 차례).
- **B(사본, 그림·삽화 전)**: `/tmp/ch28-05/B/`, `--tools-copy`로 디스크 도구 파일 복사(`cmp` 같음), `PYTHONPATH=/tmp/ch28-05/B` → 22:08:54Z PASS 28셀, `code_sha256` 같음 — 셀별 출력 글 **26/28 같음**(`cmpout.py`). **갈린 두 셀**: 코드 22(도구 없는 요청의 답 글 — A 「규정에서 확인되는 자료만으로는 … 명시되어 있지 않습니다.」 ↔ B 「… 오전 9시부터 오후 1시까지 운영합니다.」) · 코드 28(그 요청의 출력 토큰 29 ↔ 30 → 예상 비용 합 0.00113 ↔ 0.001134). 모델이 쓰는 글이라 갈림. 입력 토큰 다섯 셀·도구 호출 요청·구조 값은 두 번 같음.
- 그 뒤 코드는 바꾸지 않음(설명만 — 자리 표시 여섯 `mdpatch.py` 한 번, 05-1 alt 한 곳 `mdpatch.py`, 그림 alt·삽화 글 `--src-only`. `code_sha256` 그대로 확인). 서버 프로세스: 탐색·흔들림·A·B 모두 끝남 · `pgrep -af 'course_server|env_server|auth_server'` 0. 노트북이 연결 폴더에 쓴 것: 커널이 도구 파일을 가져오며 다시 쓴 `notebooks/__pycache__/connect_tools.cpython-312.pyc`(22:08). `runpy.run_path`는 `course_server.cpython-312.pyc`를 쓰지 않음(09-10 15:52 그대로).

## 7. 결정적 값과 흔들린 값의 자리

- **결론·그림 라벨·정리·복습(구조 값)**: 명세 칸·`parameters` = 입력 형식 `True`·명세 글자 수 252·221·299·503·685·차 31·47 = 47 `True`·첫 명세 같음 `True`·`bind_tools` 도구 칸 = 명세 `True`.
- **서비스 값(5/5 + 두 커널 같음 → 한정어와 함께)**: 입력 토큰 56·187·187·218·252 · 도구 정의 몫 131·131·162·196 · 「직접 ↔ MCP 차이 0」·「셋의 몫은 하나의 세 배가 아님」 — 결과 읽기 첫 단락(출력 그대로)·b6·05-3·05-4 라벨(캡션·alt에 한정어)·정리 2·3·복습 3·4.
- **흔들리는 값(둘째 단락·b6 표 맨 아래 줄·b7에만 「이번 실행에서는」)**: 도구 호출 요청(`lookup_policy` — 5/5·두 커널 같았지만 모델이 고르는 값이라 결론에 안 씀) · 도구 없는 요청의 답 글 · 출력 토큰 29·18·18·18·18 · 예상 비용 합 0.00113달러.

## 8. 옛 원고의 틀린 사실과 고친 방식

| 옛 문장 | 사실 | 새 판 |
|---|---|---|
| b3 「MCPAdapter가 MCP 도구를 BaseTool로 변환」 | 04 출력 종류는 `StructuredTool` | b3 「`StructuredTool`로 바꿨고, 입력 형식은 딕셔너리 그대로」 |
| b4 「같은 158 입력 토큰」·「316 토큰」 | 흔들림 확인 없이 한 번 본 값 · 조건이 여럿 함께 바뀜 | 조건을 하나씩 바꾸고 5/5 + 두 커널 같은 값만 한정어와 함께(56·187·187·218·252) |
| `schema_chars` 직접 289 ↔ MCP 216 | 모델에 보내는 명세와 다른 JSON — 명세로 세면 221 ↔ 252 | Ch 19 03 `spec_length`(도구 파일) |
| 모델 값 `assert`(입력 토큰 부등식·`tool_calls` 있음) | 서비스·모델 값 | 뺌, 참거짓·값 출력만 |
| b2 「Ch19에서 도구 개수가 늘면 선택 정보가 커진다」 | Ch 19 03은 명세 글자 수만(309→610→923), 토큰은 안 셈 | b3 「그 절은 모델을 부르지 않아 토큰 수는 세지 않았습니다」 |
| 「MCP JSON-RPC 전송 바이트는 usage_metadata에 포함되지 않습니다」 | 참이나 이 절이 잰 값이 아님 | b7 「주고받은 메시지의 크기를 재지 않았습니다 … 목록 요청은 들어가지 않습니다」 |
| b8 「Ch37에서는 …」 | 교재에 Ch 37 없음 | Ch 29 01 링크(06 실습 절이 생기면 06으로) |
| b10 스펙 2025-11-25·FastMCP v2·확인 2026-09-11 | 현재 판 2026-07-28 | MCP 2026-07-28 Tools·OpenAI·LangChain MCP·설치판 소스, 확인 2026-09-28 |
| G4 `temperature` 누락 | 과정 표준 | nbkit 모델 셀 |

## 9. 그림 (Mermaid 4 + 삽화 1)

- 설계표 `05-figures.md`(렌더 전 22:10:11Z에 적음). 원본 viewBox 폭: 05-1 **420** · 05-2 **714** · 05-3 **466** · 05-4 **693** — 모두 868 이하. 첫 렌더는 `%% classes` 줄을 빠뜨려 넷 모두 회색 → 줄을 넣고 다시 렌더(05-1은 명세 상자 라벨을 `<br>`로 미리 나눔, alt도 맞춤). PNG 넷 직접 확인(스테이징 사본 `.cache/ch28-05-view/`): 05-1 점선 둘이 나란한 노란 상자 둘로 · 05-2 점선 셋 → 파란 상자 셋 → 노란 상자 셋 · 05-3 칸 둘(파랑 → 보라 → 노랑)이 맨 아래 노란 상자로 모임 · 05-4 노란 상자 다섯, 점선 셋. 단어 가운데 끊긴 라벨 0.
- 색: 초록 = 서버 파일 · 파랑 = `MCPAdapter`·`convert_to_openai_tool`·바꾼 조건·요청 코드 · 노랑 = 출력 값 · **보라 = 05-3 모델 상자 둘(실제로 부른 `gpt-5.4-mini`)뿐** · **빨강 0**. 갈래는 점선, 라벨 대괄호·따옴표 0, subgraph 0, 노드 id `call`·`end` 0, 노드 7개 이하. 나란한 상자에 `~~~`는 쓰지 않았습니다(점선 갈래로 나란히 놓였고, 04에서 `~~~`가 상자를 위아래로 쌓은 적이 있어서). 라벨 숫자는 모두 출력에 있음(5.4는 모델 이름 출력).

## 10. 삽화 — 05-5 모듈 수만큼 쌓이는 설명서

- `generate_image` **한 번**(재생성 0), `params` `{"model":"nano_banana_pro",…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `jobs_wait` 모델 표시 `nano_banana_2`(기록만).
- **1차 job `ec17f0a9-5ffa-4c96-9163-441329e06a8c` 채택** — 거래 2026-09-28T22:11:53.752923Z −2. 원본 `eb49458a…`(2752 × 1536) → 폭 1100(LANCZOS) `d88fff1c…`(1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄인 그림과 저장 PNG 픽셀 대조: bbox `None`, 최대 차이 0. **크레딧: 생성 전 바로 앞 거래 21:30:25Z는 04 몫(잔액 2309) · 이 절 거래 한 줄 = 2크레딧 · 잔액 2307(계산).**
- 저장 PNG 사본(`.cache/ch28-05-view/illu-1-1100.png`, `cmp` 같음)을 직접 열어 셈: 가운데 가는 회색 세로선 하나 · 왼쪽 짧은 회색 격자 트러스 하나 + 산호색 모듈 하나 + 산호색 책 한 권 · 오른쪽 긴 트러스 하나 + 산호색·민트색·연보라 모듈 셋 + 같은 세 색 책 세 권(연보라 위·민트·산호 아래). 글자·숫자·사람·손·화살표·별·화면·전선·원통·캡슐·고리·우주선 0.
- 그림과 비유의 차이(그림 읽기·`prompt.md`, 강사 확인): 설명서가 책 모양 · 보급선·실어 보내는 장면 없음 · 오른쪽 모듈이 조금 겹쳐 보임 · 책 더미 두께는 모듈 수에 비례해 보이지만 5절 도구 정의 몫은 셋이어도 세 배가 아님(그림 읽기에 밝힘) · 위아래 흰 여백 조금.

## 11. 도구 파일·서버 파일·앞 절 영향

- **도구 파일 `labs/part6/ch28-mcp/notebooks/connect_tools.py` 05 판** `570ed3cc607871a374ac1d5d7fc3ba6435908669ae79f48908535787d16f204c`(04 판 `cc066bd7…`에서):

| 함수 | 배운 곳 | 옮긴 것 | 가져오는 절 |
|---|---|---|---|
| `names_of(items)` | Ch 28 01절 4절 | 04 판 그대로 | 03·04·05 |
| `async def call_tool_row(server, tool_name, arguments)` | Ch 28 02절 2절 | 04 판 그대로 | 03 |
| `stdio_config(server_path, env)` | Ch 28 03절 2절 | 04 판 그대로 | 04·05 |
| `tool_call_names(response)` | Ch 19 04절 | 04 판 그대로 | 04·05 |
| `sum_usage(messages)` | Ch 19 05절 | 04 판 그대로 | 04 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06절 | 04 판 그대로 | 04·05 |
| `spec_length(tools)` | **Ch 19 03절** | **Ch 19 03 노트북 셀 글 그대로**(`8afb6cff…` — 주석 둘 포함, 디스크 셀에 있음·AST 같음) — 이 판에서 더함, 가져오기 `import json`·`from langchain_core.utils.function_calling import convert_to_openai_tool` | 05 |

  - **대조 사슬**: `author_05.py`가 `import author_04` → 04 판 해시 고정(`cc066bd7…`) · 머리 설명(`author_03.TOOLS_HEAD`)과 04 블록 여섯 글자 그대로 · 가져오기 블록에만 두 줄 · `check_tools()`(함수 차례 일곱·가져오기 다섯·Ch 19 03 셀 해시·디스크 셀 대조·AST) · **`author_03.later_version(TOOLS)`·`author_04.later_version(TOOLS)` 둘 다 참 확인** → 03·04를 다시 돌려도 덮어쓰지 않음 · 쓰기 가드 `write_tools()`(없거나 · 03·04 판이거나 · 이 판이면 씀, 뒤 판이면 건너뜀, 그 밖이면 멈춤) · `--tools-copy`는 디스크 판.
  - **03 노트북 설치 셀과의 관계(마감 확인)**: 05 판이 `langchain_core`를 가져오므로, 이 파일을 가져오는 03 노트북의 설치 셀(`fastmcp`·`mcp`·`httpx`·`psutil`)에 `langchain-core`가 없음(규격 §2-7 6번). 실습 폴더 잠금에는 `langchain[mcp]==1.4.0`이 있어 `uv sync --locked` 커널에서 03·04·05의 가져오기 줄이 모두 됨(노트북 밖 확인). 03은 이 작업 범위 밖이라 고치지 않음 — 마감에서 03 설치 셀에 `langchain-core==1.6.2`를 더할지(03 다시 실행 필요) 정할 몫.
  - 공개 목록: 도구 파일 줄은 03이 이미 올림 → 05 목록 변경 없음. zip은 마감.
- **서버 파일**: `course_server.py`(`d7f7e8b9…`)·`env_server.py`·`auth_server.py` 그대로. 05는 `course_server.py`를 stdio로 띄우고(2절) `runpy.run_path`로 읽어 커널 안 객체에만 도구 둘을 붙임(파일 그대로).
- **01~04**: 다시 실행하지 않음(01 `2407c4c57138…`·02 `687062053d18…`·03 `04c437f720bc…`·04 `7bd03afa0ca1…` 그대로). 04가 05에 기대는 문장 — 정리·b8 「05절에서는 도구 정의가 모델의 첫 요청 입력 토큰에 얼마나 더해지는지 셉니다」 **참**(5절 도구 정의 몫) · 2절 「모델에게 보내는 도구 정의에 이 딕셔너리가 어떻게 실리는지는 05절에서 봅니다」 **참**(2절 `parameters` = 입력 형식 `True`) · 5절 COST 결과 읽기 「첫 요청의 입력 토큰은 05절에서 따로 셉니다」 **참**.

## 12. 뒤 챕터·과정 파일 문장

- `grep -rn 'Ch *28' textbook/part6/ch29-*/_src textbook/part7`(지시 명령 그대로) **0건** — 뒤 챕터가 05에 기대는 문장 없음. Ch 29 01 b3은 「Ch11 평가셋과 Ch21 에이전트」만. Part 7 `qa/before-integration/`의 「ch28」 글자는 옛 작업 기록(고치지 않음).
- `textbook/part6/_build_index.py` 26행 「MCP 서버와 클라이언트를 연결하고 도구 정의의 입력 토큰을 확인합니다」 **참** · `textbook/_notebook/build_index.py` 61행 「… 도구 정의의 입력 토큰과 권한 경계를 확인합니다」 **참**(05·03) · `labs/part6/continuity-guide.md` 14행 「Ch28 MCP 서버·클라이언트와 도구 정의 토큰 | **Ch37**의 비용·컨텍스트 측정」 — 앞 칸 참, 「Ch37」은 교재에 없음(마감) · `chapter.json` `objectives` 셋째 「LangChain 1.4.0 MCPAdapter로 도구를 연결하고 첫 호출 입력 토큰을 측정」(「측정」 금지어·04·05 나눔)·넷째 「최소 권한」(Ch 16 원고 0건 — 03 기록) — 마감.

## 13. 서비스 요청·비용

- 노트북 한 번 **5번**(5절 첫 요청 다섯, 도구 실행 0). 이번 작업 누계 **35번**: 흔들림 확인 25 + A 5 + B 5(탐색 스크립트 요청 0 — 가짜 키 글). 예상 비용(요금표 2026-09-17 mini 0.75·0.075·4.50달러/100만 토큰, 청구 금액 아님): 흔들림 0.005724 + A 0.00113 + B 0.001134 = **약 0.0080달러**. 임베딩 0.

## 14. 남은 것 · 지우지 않은 것 · 강사 확인

- 보호 파일 대조는 `manifest-changes.md` 「05절 뒤」.
- **지워야 하지만 지우지 않은 것**(삭제 승인 대상): `labs/part6/ch28-mcp/notebooks/__pycache__/connect_tools.cpython-312.pyc`(A 실행이 22:08에 다시 씀) · `qa/upgrade/gates-wip-05-05.json`·`gates-wip-05.json` · 사용자 디스크 `.cache/ch28-05-view/`(그림 확인 사본 다섯 — Mermaid PNG 넷·삽화 1100 사본) · 기기 `/tmp/ch28-05/`(탐색 `exp/`·사본 `B/`·삽화 원본 `illu/`·흔들림 원본 `probe/`·검사 도구 `tools/`·`reps1.json`·`reps2.json`) · 옛 그림 `figures/05-흐름.{svg,excalidraw,caption.md}`(본문 참조 0 — 챕터 공개 목록의 옛 SVG 줄 빼기는 마감).
- **강사 확인 대상**: 코드 줄 99 → 173·코드 셀 6 → 28 · 새 말 둘(첫 요청·도구 정의 몫 — 「몫」은 Ch 20 04 「입력 몫」과 같은 쓰임) · 직접 도구를 `@tool("lookup_policy")`로 만들어 파이썬 이름 `direct_lookup`과 가른 것 · 서버 파일이 만든 객체에 커널 안에서 도구를 더 붙인 셀(파일 그대로) · 도구 없는 요청의 답 글을 출력한 셀(두 커널에서 갈림 — 도구 없이 규정에 없는 시각을 적는 장면이 나올 수 있음) · 입력 토큰을 한정어와 함께 결론에 쓴 것(Ch 27 03은 같은 5/5·두 커널 값을 둘째 단락에만 둠 — 이 절은 챕터 리드 결정대로 결론에) · 도구 파일 05 판이 `langchain_core`를 가져와 03 설치 셀과 어긋남(§11) · 삽화의 책 모양·겹친 모듈·여백 · 절 제목의 「첫 호출」(본문은 「첫 요청」 — 과정 말 「모델 요청」과 맞춤, 제목은 슬러그라 그대로).

## 마감 반영 (2026-09-28, 검토 1차 B-4~B-6·B-11)

- **다시 실행하지 않았습니다**(모델 절 — 마크다운만). `code_sha256` `b99a57642e5d…`·`outputs_sha256` `a080eff183cf…`·`executed_at` 22:08:27Z 그대로, 노트북 파일 `9b4b0138` → `d4db557b`.
- **B-4·B-11**(입력 토큰 결론 판단은 그대로 — 핵심 개념 세 곳에 한정어): b4 비유 「다른 점」 → 「…명세가 31자 짧았습니다. 그래도 입력 토큰은 MCP 도구와 같았고, 흔들림 확인 다섯 번과 두 커널에서 모두 그랬습니다」 · 용어 표 「도구 정의 몫」 끝에 「흔들림 확인 다섯 번과 두 커널에서 모두 같은 값이었습니다」 · 삽화 그림 읽기 「그림의 책 더미와 달리, 흔들림 확인 다섯 번과 두 커널에서 모두 도구 셋의 정의 몫은 세 배가 되지 않았습니다」.
- **B-5**: 셀 47 둘째 단락의 출력에 없는 백틱 값(`오전 9시부터 오후 1시까지`)을 빼고 「다시 실행한 새 커널과 노트북 밖 다섯 번 가운데 셋에서는 서버 규정에 없는 토요일 시각을 적었습니다」.
- **B-6**: b10 OpenAI 함수 호출 문서 → 「토큰 한도에 닿으면 처음에 싣는 함수 수를 줄이거나 설명을 줄이라고 제안합니다」.
- 서버 파일 `course_server.py` 문법 고침(마감): 명세 글자 수 252(메모리·stdio)가 옛 판과 같음 — 05 출력은 바뀌지 않음.
- 게이트 G1~G7 0.
