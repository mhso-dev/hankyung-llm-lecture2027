# Ch 28 MCP — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part6/ch28-mcp` 01~05절(품질 개선) + **06절 챕터 끝 실습 절 신설**(`06-MCP-실습`), 노트북 `labs/part6/ch28-mcp/notebooks/01~06-*.ipynb`, 도구 파일 `notebooks/connect_tools.py`, 실습 폴더 맨 위 서버 파일 셋(`course_server.py`·`env_server.py`·`auth_server.py`). 뒤 챕터가 읽는 계약 파일(산출 파일)은 없습니다.
- 기간: 2026-09-28(준비 조사 · 01~05절 개선 · 06절 신설 · 검토 1차 · 챕터 마감 — 마감 검사는 2026-09-29 00시 UTC 무렵 끝남). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 다섯 절 합계 **208**(G1 21 · G2 7 · G3 0 · G4 1 · G5 32 · G6 132 · G7 15 — 01 40 · 02 44 · 03 43 · 04 41 · 05 40, `gates-before.json`) → 마감 뒤 **6/6 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 378·381·483·405·412·369 = **2,428**).
- 코드 셀 4·4·5·3·6 = 22 → **25·24·26·25·28 + 06 새 절 24 = 152**(`verify.py --chapter` → `PASS 6 sections / 152 code cells (max 16 lines)`). 코드 줄(`count_code.py`, 주석·빈 줄 뺌) 43·57·47·38·99 = 284 → **131·125·158·163·173 + 06 137 = 887**, 도구 파일 57줄(파일 103줄). Mermaid **23장**(01~05 넷씩 · 06 셋), 삽화 **6장**(절마다 하나, Higgsfield — 02·04 재생성 1회씩, 16크레딧, 마감 0), 복습 문제는 HTML에만.
- **모델 요청**: 01·02·03은 모델 없음(결정적). 04·05는 앞 절반이 모델 없는 구조, 5절만 실제 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`), 06은 실습 절. 노트북 한 번 **0 · 0 · 0 · 2 · 5 · 4 = 11**번. 작업 전체(노트북 밖 흔들림 확인 + 새 커널 A·B — `probe/*.jsonl`과 노트북 출력으로 다시 셈, §9) **01 0 · 02 0 · 03 0 · 04 14 · 05 35 · 06 28 = 77번**, 마감 **0번**.
- 화면 검사 `visual.cjs`: HTML **일곱 개**(여섯 절 + `index.html`) × 1280px·390px = **14행 PASS**(기기 `/tmp/pw` playwright·`/tmp/pw-browsers` chromium-headless-shell — Ch 26 마감이 설치한 것을 환경 변수 `NODE_PATH`·`PLAYWRIGHT_BROWSERS_PATH`·`LD_LIBRARY_PATH`만 주고 원본 그대로).
- **마감에서 다시 실행한 노트북: 03 하나**(모델 없음 — 설치 셀·포트 확인·환경 변수·이름 수, §19). 01·02·04·05·06은 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같습니다(마크다운·첨부 그림만).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 27 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-28)」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」)·`NN-probe.md`(04~06 노트북 밖 흔들림 확인) → 검토 `review-round1-A.md`(01~03·공통)·`review-round1-B.md`(04~06) → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 MCP 구조와 capability 협상 | 서버 파일 읽기 `runpy.run_path(server_file)["mcp"]`(pyc 0) · 메모리 연결 `async with Client(server) as client:` + 블록 안 await(셀 맨 위 await — IPython 기능, `asyncio.run` 안 씀) · `client.protocol_version`(**현재 판 2026-07-28**)·`initialize_result`(`None`)·`server_capabilities.model_dump(exclude_none=True, by_alias=True)`·`server_info`·`instructions` · 목록 요청 `list_tools`·`list_resources`·`list_prompts` · `call_tool`·`read_resource`·`get_prompt` · `Tool.input_schema` · 값 바꿔 보기 `Client(server, mode="legacy")` → **옛 판 2025-11-25**(`initialize` 결과 있음·`listChanged` `true`·`extensions` 없음) · 빈 서버 `FastMCP("빈 자료실")`의 기능 목록 세 칸 | **`names_of`**(03이 도구 파일로) · `read_negotiation`·`compare_rows`·`change_flags`(노트북) | MCP · 통신 규약 · MCP 서버·클라이언트 · 판 번호 · 기능 목록 · 자료·메시지 틀 (6) |
| 02 FastMCP 로컬 서버 제작 (paired) | 서버 객체 `FastMCP("…")` · 데코레이터 줄 `@practice.tool`·`@before.tool`·`@after.tool`(서버 객체 메서드) · 함수 이름·독스트링·매개변수 힌트 → 도구 이름·설명·입력 형식 · 몸통 전 입력 검사(`1 validation error`) ↔ 힌트 없는 도구는 값 3이 몸통까지(`Error calling tool 'lookup_policy': 3`) · `try/except ToolError` · 기록기 `logging.getLogger("fastmcp").setLevel(logging.CRITICAL)` · 서버 파일의 `-> str`(출력 형식 `x-fastmcp-wrap-result`)·꼬리표·`@mcp.resource`·`@mcp.prompt`·`mcp.run` 한 문장씩 | **`async def call_tool_row(server, tool_name, arguments)`**(03이 도구 파일로) · `count_rules`·`lookup_policy` 판 셋(노트북) | FastMCP(서버 클래스) · 도구 붙이기(등록) · 기록기·기록 수준 · 출력 형식 (4) |
| 03 stdio와 원격 전송·권한 경계 (paired) | stdio 설정 딕셔너리 `{"mcpServers": {"server": {"command", "args", "env", "keep_alive": False}}}` · `psutil.Process().children()`(자식 1 → 0) · FASTMCP 조용히 하는 세 이름 · Before `env`에 `dict(os.environ)` ↔ After 세 이름 ↔ 값 바꿔 보기(가짜 이름 하나 더) · `os.environ[…]`·`del` · `subprocess.Popen(command, env=…, stdout=DEVNULL, stderr=DEVNULL)`·`poll()`·`terminate()`·`wait(timeout=…)` · `mcp.client.stdio.get_default_environment()`(마감) · `socket.socket()`·`connect_ex` · `StreamableHttpTransport(url, auth="…")` · `MCPError`(연결 거절) · `httpx.post` → `401`·`WWW-Authenticate: Bearer` · 서버 파일의 `StaticTokenVerifier`·`@mcp.tool(auth=require_scopes("admin"))` | **`stdio_config`**(04가 도구 파일로) · `wait_for_port(port, limit_seconds)`(노트북, `while` — Ch 23 04 `wait_for_signal` 모양) · 서버 파일 둘 `env_server.py`·`auth_server.py` | 전송 · 환경 변수 · 인증 · 인가 · 접근 토큰 · 범위 (6) + 이어 쓴 「자식 프로세스」(Ch 23 04) |
| 04 LangChain MCP 클라이언트 연동 | `langchain.mcp.MCPAdapter(stdio_config(…))`(베타 — `warnings.filterwarnings("ignore", category=LangChainBetaWarning)` 뒤 가져옴)·`list_tools()` → `StructuredTool`(입력 형식 `dict`, `response_format="content_and_artifact"`, `metadata["mcp"]`) · `invoke` → `NotImplementedError: StructuredTool does not support sync invocation.` · **`ainvoke`**(내용 블록 목록 — 블록 `id`는 출력하지 않음) · `async with adapter:` 안에서는 서버 하나를 이어 씀 · `StateGraph(MessagesState)` + `ToolNode` + 손으로 만든 `AIMessage(tool_calls=…)` → `status='success'`/`'error'`·아티팩트 · `create_agent(model, tools=…, system_prompt=…, middleware=[ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")])` → `await ainvoke` | 새 함수 0(도구 파일에 **`stdio_config`·`tool_call_names`·`sum_usage`·`estimate_cost`**를 더함) | LangChain 도구로 바꾸기 · 비동기로 부르기 · 내용 블록 · 아티팩트 (4) |
| 05 도구 정의와 첫 호출 토큰 | `convert_to_openai_tool` 도구 명세(칸 `parameters` = 서버 입력 형식 `True`) · `json.dumps(…, ensure_ascii=False)` 글자 수 · 직접 `@tool("lookup_policy")`(같은 이름·설명) · `@longer.tool`(설명만 늘림)·`@server.tool` 둘(서버 파일 객체에 커널 안에서 더함, 파일 그대로) · `MCPAdapter(FastMCP 객체)` 메모리 연결 · `model.bind_tools(tools)` → `invoke(first_messages)` 첫 요청 · `usage_metadata["input_tokens"]` | **`spec_length`**(Ch 19 03 셀 글 그대로 — 05가 도구 파일에 더함) | 첫 요청 · 도구 정의 몫 (2) + 이어 쓴 「도구 명세」(Ch 19 03) |
| 06 MCP 실습 | **새 문법·새 API·새 말 0**(01~05 노트북·도구 파일과 AST 대조) | 조립 `async def run_agent(chosen_tools)` · `show_requests(messages)` · `count_asked(messages)`(노트북) | 0 |

- 새 용어 합계 **22개**(절 meta 「새 용어」 6·4·6·4·2·0).
- **이 챕터에서 허용한 문법**: 셀 맨 위 `async with`·await(01~) · `async def` 셀당 하나(02 `call_tool_row`·06 `run_agent`) · 데코레이터 `@srv.tool`(02·05·06)·`@tool("이름")`(05) · **MCP 도구 함수의 매개변수 단순 힌트**(`: str` — 입력 형식을 정하는 것이 학습 내용, 챕터 예외, 내놓는 값 힌트 없음) · `try/except 이름`(02 `ToolError`·03 `MCPError`·04 `NotImplementedError`) · `while`(03 `wait_for_port` 하나)·`with socket.socket()` 하나 · 도구 파일 `estimate_cost`의 `.get` 둘(Ch 6 06 본문 그대로). 마감 AST 따로(`extra_check.py`) 금지 문법 0.
- **쓰지 않은 것**(여섯 절·도구 파일 0건): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·대입 풀기·별표 풀기·세미콜론·`isinstance`·`importlib`·클래스·`asyncio.run`·`nest_asyncio`·`tool_choice`·`show_messages`. 서버 파일 `course_server.py`의 f-string·제너레이터 식은 마감에서 고침(§12).
- 셀 모양: 준비 셀 밖 셀 10줄 이하, 함수 본문 8줄 이하, 셀당 정의 하나, 첫 줄 주석 100%, 호출 깊이 최대 2. `assert`는 파일 찾기·서버 준비·키 셀에만(모델 판단·모델 글에 0). 출력하지 않는 값: 내용 블록 `id`·모델 호출 ID·pid·포트 번호·시각·준비 시도 횟수·기기 환경 변수 개수(03 마감에서 개수 출력 뺌).

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 2 05·07·09·12**: `with open`(→ `async with` 풀이) · 타입힌트는 검사하지 않는 표시(02 b3) · 데코레이터(02 첫 자리 세 문장 + 링크, A 트랙) · `async def`·파일의 `asyncio.run`(01·02).
- **Ch 3 01·05 · Ch 6 01**: `.env` 무시 규칙 · 키 셀 `load_dotenv()`·「환경 변수 전체를 출력해 문제를 찾지 않습니다」(03 b3) · Ch 6 01 계층 지도(01 b3 인용 — 「프롬프트」 한 곳 예외) · `usage_metadata`(05).
- **Ch 4 04**: `httpx.get`·상태 코드(03 6절 `httpx.post`·401).
- **Ch 6 06**: 「예상 비용」(요금표 어림, 청구 금액 아님)·`estimate_cost`(도구 파일 — Ch 21 판 본문).
- **Ch 7 04**: 틀과 빈자리(01 「메시지 틀」 풀이).
- **Ch 13 04**: `add_messages` 규칙(04 `MessagesState` 한 문장).
- **Ch 16 01**: 출처 표시 허용 목록(03 b3 — 답을 검사하는 목록 ↔ 서버에 넘길 값을 고르는 목록으로 가름). 「최소 권한」은 Ch 16 원고 0건이라 쓰지 않음.
- **Ch 18 03**: 셀 맨 위 await(01 첫 풀이의 선례).
- **Ch 19 01·02·03·04·05·06**: `@tool`·독스트링·힌트 → 입력 형식(02) · 01 7절 「힌트를 빼면」(02 마감 A-6) · 몸통 전 입력 검사(02) · `spec_length`·도구 명세(05 — 셀 글 그대로 도구 파일로) · `bind_tools`·`tool_call_names`·설명 두 판(04·05) · `sum_usage`(04·06) · `pick_tools` 읽기·쓰기 도구(03 b3 — 클라이언트 쪽 거르기 ↔ 서버 쪽 인가).
- **Ch 20 01**: 손으로 만든 도구 요청·`ToolNode`(04 4절).
- **Ch 21 01·03 · Ch 21 `runner_tools.py`**: `create_agent`(모델 객체) · 「라이브러리 상태 형식」 = `AgentState`(04 마감 B-3에서 `MessagesState`와 가름) · 도구 파일 함수 셋의 원본(`f4113158…` — 파일째 가져오지 않음, `numpy`로 멈춤).
- **Ch 22 04**: `ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")`(04·06, Ch 26·27 안전 규칙 — invoke 한 번마다 셈).
- **Ch 23 04**: `Popen`·`kill`·`wait`·`wait_for_signal`·「자식 프로세스」(03 — 인계의 「하위 프로세스」 대신).
- **Ch 27 08·09**: 권한 규칙은 파일 도구 안에서만 판정(03 b3 — MCP 도구에 걸린다고 보지 않음, 마감 A-13) · 09 b8이 01 슬러그로 이음(01 b2가 받음).
- 소재: **교육센터 자료실 규정**(대출·운영·연체 — Ch 21·26·27 이음). 03 연습 서버의 가짜 환경 변수 `CH28_DEMO_TOKEN = "교재용-가짜-값"`과 가짜 접근 토큰 `reader-token-demo`·`admin-token-demo`는 모두 노트북·서버 파일이 정한 교재용 값.

## 3. 절별 과제·값 (새 커널 두 번과 노트북 밖 흔들림 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값·두 커널과 흔들림 확인 5/5가 같았던 값(결론·그림에 쓴 값) |
|---|---|---|
| 01 | `course_server.py`를 `runpy`로 읽은 서버 · 기본 모드 ↔ `mode="legacy"` · 빈 서버 | 판 번호 `2026-07-28` ↔ `2025-11-25` · 초기화 결과 없음 ↔ 있음 · `listChanged` `false` 셋 ↔ `true` 셋 · `extensions` 있음 ↔ 없음 · 서버 판 `4.0.3`·사용 설명 같음 · 도구·자료·메시지 틀 하나씩(`lookup_policy`·`policy://handbook`·`explain_policy`) · 빈 서버 기능 목록 키 다섯·세 목록 `[] [] []` · 요청 0 · 새 커널 25/25 |
| 02 | 힌트·독스트링 없는 Before ↔ `topic: str` + 독스트링 After · 값 3 · 값 바꿔 보기 `"주차"` · 서버 파일 도구 | Before `'topic': {}`·설명 `None`·값 3이 몸통까지(`Error calling tool 'lookup_policy': 3`·몸통 `[3]`) ↔ After `{'type': 'string'}`·`1 validation error for call[lookup_policy]`·`Input should be a valid string`·몸통 `[]` · `"주차"`는 둘 다 몸통까지 · 서버 파일 도구 `topic은 대출, 운영, 연체 중 하나여야 합니다.` · 요청 0 · 새 커널 24/24 |
| 03 | stdio(`keep_alive: False`) · Before 환경 통째로 ↔ After 세 이름 ↔ 가짜 이름 하나 더 · 127.0.0.1 HTTP(고정 포트 58028) · 접근 토큰 없음·읽기·관리 | 블록 안 자식 `1` → 블록 뒤 `0` · 대출 결과 글 01과 같음 · Before 가짜 이름 `True`·받지 못한 노트북 이름 수 `0`·`['교재용-가짜-값']` ↔ After `False`·`['없음']` · 값 바꿔 보기 `True`·`After보다 늘어난 이름 수: 1` · 띄우기 전 포트 `False`·준비 `True`·살아 있음 `True`·자식 `1` · `MCPError`·`Server returned an error response`·`401`·`Bearer` · 읽기 토큰 `['lookup_policy']`·`Unknown tool: 'update_policy'` · 관리 토큰 둘·`규정을 바꿨습니다: 운영`·읽기 토큰도 바뀐 글 · `-15`·자식 `0`·포트 닫힘 · 요청 0 · **마감 새 커널 26/26** |
| 04 | `MCPAdapter(stdio_config(…))` · 손 요청 `call_a` 운영·`call_b` 주차 · 에이전트(호출 한도 3) · 질문 「교육센터 자료실은 토요일에 몇 시까지 운영하나요?」 | `StructuredTool`·`dict` · `NotImplementedError` · `ainvoke` 뒤 자식 `0` · 블록 안 `1`·`1`·같은 프로세스 `True`·블록 뒤 `0` · `call_a success`·`call_b error`(서버 글) · (5/5) 메시지 넷·도구 요청 `lookup_policy` 한 번·요청 `2` = 도구를 요청한 응답 수 `1` + 1 · 새 커널 25/25 |
| 05 | 명세 · 직접 도구 · 설명을 늘린 도구 · 도구 셋 · 조건 다섯의 첫 요청(도구 부르지 않음) | 명세 `252`·직접 `221`(차 31 = `additionalProperties`)·설명 `299`(+47 = 설명 +47)·도구 셋 `252·503·685` · (5/5 + 두 커널) 입력 토큰 `56`·`187`·`187`·`218`·`252` → 도구 정의 몫 `131`·`131`·`162`·`196` · 새 커널 26/28(갈린 둘은 도구 없는 요청의 답 글·출력 토큰·비용) |
| 06 | §10 | §10 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | MCP(Model Context Protocol) | 모델이 쓸 도구와 자료를 다른 프로그램에서 가져오는 통신 규약(「MCP는」으로 문장을 시작하지 않음) | 서버 파일 · `Client` |
| 01 | 통신 규약(protocol) | 두 프로그램이 주고받을 메시지의 모양과 차례를 정한 약속 — 「프로토콜」은 본문 0 | `server/discover`·`initialize` |
| 01 | MCP 서버 · 클라이언트(+ 호스트 한 문장) | 도구·자료·메시지 틀을 내놓는 쪽 / 요청을 보내는 쪽 · 호스트 = 모델을 쓰는 응용 프로그램(01~03은 노트북이 대신) | `server` · `Client(server)` |
| 01 | 판 번호 | 두 쪽이 어느 판의 규격 문서로 말할지 정한 값, 날짜로 부름 · **현재 판 2026-07-28** · 옛 판 2025-11-25 | `client.protocol_version` |
| 01 | 기능 목록(capability) | 서버가 어떤 종류의 요청을 받는지 알리는 딕셔너리 — 권한도, 등록 항목도 아님(「capability」는 제목·첫 풀이·용어 표에만) | `client.server_capabilities` |
| 01 | 자료(resources) · 메시지 틀(prompts) | 주소로 읽는 글 / 빈자리에 값을 넣어 받는 메시지 — 「리소스」·「프롬프트」 본문 0 | `policy://handbook` · `explain_policy` |
| 02 | FastMCP · 도구 붙이기(등록) · 기록기·기록 수준 · 출력 형식 | 서버 클래스 / 데코레이터 줄로 서버 도구 목록에 올림 / 라이브러리 기록을 내보내는 객체와 그 문턱 / 도구가 내놓는 값의 모양(`-> str`) | `FastMCP("…")` · `@srv.tool` · `logging.getLogger("fastmcp")` |
| 03 | 전송 · 환경 변수 · 인증 · 인가 · **접근 토큰** · 범위 | stdio·Streamable HTTP / 프로그램이 시작할 때 받는 이름과 값 / 누구인지 확인 / 무엇을 허락할지 / 누구인지 알리는 글(**「토큰」 단독은 모델 입력 토큰과 겹쳐 본문 0** — 마감 A-10으로 넷을 더 고침) / 접근 토큰이 허락받은 일의 이름 | `stdio_config` · `env` · 401 · `require_scopes` · `reader-token-demo` · `read`·`admin` |
| 04 | LangChain 도구로 바꾸기 · 비동기로 부르기 · 내용 블록 · 아티팩트 | `MCPAdapter`가 MCP 도구를 `StructuredTool`로 / `invoke`의 비동기 판 `ainvoke` / 도구 메시지 내용의 한 칸(글·`id`) / 모델에게 보내지 않는 구조화 결과 | `list_tools()` · `ainvoke` · `result[0]["text"]` · `artifact` |
| 05 | 첫 요청 · 도구 정의 몫 | 도구를 한 번도 부르기 전 대화를 시작하는 모델 요청 / 같은 메시지로 보낸 두 요청 가운데 도구를 알린 요청이 더 쓴 입력 토큰(**06의 「늘어난 입력 토큰」과 다른 말**) | `first_messages` · 131 |
| (이어 씀) | 자식 프로세스 · 도구 명세 · 입력 형식·입력 검사 · 데코레이터 줄 · 호출 한도 · 도구 호출 요청 | Ch 23 04 · Ch 19 03 · Ch 19(「스키마」 금지) · Ch 19 · Ch 22 04 · Ch 19 04 — **「도구 호출 요청」은 모델 응답의 `tool_calls` 한 뜻**(서버로 가는 요청은 「도구를 부르는 요청」, 마감 B-1) | — |
| (이어 씀) | 라이브러리 상태 형식 | Ch 21 03 `AgentState` 한 뜻 — 04의 `MessagesState`는 「LangGraph가 미리 만들어 둔 상태 형식」(마감 B-3) | — |

- 대체어: 반환 → 내놓다 · 스키마 → 입력 형식 · 검증 → 검사 · 경로 → 파일 위치 · 세션 → 연결 · 로그 → 기록 · 직렬화 → JSON 글로 바꾸기 · 측정 → 재다·세다 · 인스턴스 → 객체 · 엔드포인트 → MCP 주소 · 하위 프로세스 → 자식 프로세스 · 반환 힌트 → 내놓는 값 힌트 · 캐시 입력(Ch 6 06 말 그대로, 「캐시」 단독 금지) · 사용 중단 → 「더 쓰지 말라고 표시」(「중단」이 과정 금지어 목록에 걸림 — 마감 A-3).
- **쓰지 않는 말**(여섯 절 설명·주석·캡션·`.mmd`·README 참 금지어 0 — 제목·슬러그·코드 백틱 말고): Ch 27 목록 + 「프로토콜」·「세션」·「핸드셰이크」·「리소스」·「인스턴스」·「스펙」·「레거시」·「안내 글」(Ch 27 05 뜻)·「궤적」 · 사용자가 금지한 표현. 「capability」는 제목·첫 풀이·용어 표에만. 마감이 더한 문장의 걸림은 거짓 양성(「프로그램」 속 「로그」)뿐(`ban28.py` 전후 대조).

## 5. 비유 가족 「우주 정거장 도킹 포트」 (삽화 여섯)

- 01-5 도킹 고리 셋과 우주선 둘(정거장 = MCP 서버, 고리 셋 = 구성 요소 셋, 우주선 둘 = 인자 `mode`만 다른 클라이언트) · 02-5 테두리 없는 해치와 네모 테두리 해치(테두리 = 매개변수 힌트로 만든 입력 형식, 공 = 값 3) · 03-5 짧은 통로와 긴 통로(stdio ↔ HTTP, 해치 옆 판 = 인증 — **가운데 몸체는 서버를 띄우고 값을 넘기는 노트북(클라이언트) 자리라 01의 정거장(서버)과 자리가 다름**, 마감 A-14) · 04-5 이음 부품으로 이은 모듈(`MCPAdapter`) · 05-5 모듈 수만큼 쌓이는 설명서(도구 명세 — 도구 정의 몫은 세 배가 되지 않음) · 06-4 받침대에 꽂은 통 하나와 셋(격납고 = 서버, 로봇 팔 = 조립 함수, 통 = 붙인 도구).
- 사람·손·글자·숫자·화살표·별·행성·화면·전선 없음. 짝짓지 않는 요소(수·크기·길이·겹침·여백)는 그림 읽기에 밝힘. 작업 조회 결과의 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만). 삽화는 마감에서 다시 만들지 않음(Higgsfield 0).

## 6. 색 규칙 (Mermaid 23장)

- 자료·파일·우리가 만든 서버 객체 **초록(tool)** · 우리가 부른 코드·클래스·만든 함수·블록·바꾼 값 **파랑(flow)** · 출력으로 확인한 값·받아 출력한 오류 **노랑(measure)** · 노트북 밖·설치판 소스로만 확인한 것·두 조건 공통 값 **회색(클래스 없음)** · **보라 = 그 절에서 실제로 부른 모델만**(04-4·05-3·06-2 — 01~03과 앞 절반 그림 보라 0) · **빨강 = paired Before 결함 결과만**(02-3·03-3 Before 상자 하나씩, 01·04~06 0).
- **마감 정정(B-10)**: 06-1의 `MCPAdapter`(회색)·바꾸는 값 `tool_count`(초록)와 06-3의 두 실행 상자(초록)를 파랑으로 — 04-1·05-1·05-2와 같은 색. 06 설계표의 「라이브러리 클래스 회색·바꾼 값 초록」 배정은 챕터 공통 규칙에 없던 갈래라 규칙 쪽으로 맞춤.
- 원본 viewBox 폭 모두 868 이하(최대 861 — 04-4·06-2, 다음 03-4 831). 라벨에 출력 토큰·비용·답 글·도구 인자 없음. 입력 토큰 라벨(05-3·05-4·06-2·06-3)은 흔들림 확인 5/5 **그리고** 새 커널 두 번 같을 때만. **기기마다 다른 값(03 이름 수)은 라벨에서 뺌**(마감 A-9).
- **마감에서 다시 렌더한 `.mmd` 넷**: `03-3`(After 라벨) · `03-4`(칸 제목 「접근 토큰 없음」) · `06-1`·`06-3`(색 — 06-1은 노트북 첨부 교체). 모두 PNG 직접 확인, 폭 639·831·521·455.

## 7. 결정적 값과 흔들린 값

- **결정적 값**(결론·그림·정리·복습에 쓴 값): §3 표 전부. 01~03은 모델이 없어 모두 결정적이고 새 커널 두 번 셀별 출력이 같음. 04·05·06의 모델 판단 값(도구를 요청한 응답·요청 수·고른 도구)은 노트북 밖 흔들림 확인 5/5와 두 커널에서 같을 때만 「흔들림 확인 다섯 번과 두 커널에서 모두」로 한정해 씀. 결론 문장의 중심은 셈: **요청 수 = 도구를 요청한 응답 수 + 1**(04·06).
- **입력 토큰을 결론에 쓴 판단(검토 B-11 — 챕터 리드 결정)**: **05·06은 입력 토큰이 그 절의 주제**이고 5/5·두 커널 같아(05 스물다섯 요청·06 스무 요청 모두 같은 값) **한정어와 함께 결론·그림·정리·복습에** 둠(Ch 19 04가 입력 토큰 177 ↔ 330을 그림·정리에 쓴 선례와 같은 쪽). **04는 입력 토큰(430)이 주제가 아니라 b6 표·결과 읽기 둘째 단락에만** — 마감에서 b6 표의 입력 토큰 줄을 흔들리는 값 줄(도구 인자·답 글·출력 토큰·비용)과 떼어 「노트북 밖 다섯 번·두 커널 같음, 주제가 아니라 결론에 쓰지 않고 05절에서 셈」으로. Ch 26 04·Ch 27 03(같은 조건의 입력 토큰을 둘째 단락에만)과 갈리므로 **강사 확인 대상**, 과정 요약 §7에 적용 선례 한 줄(「입력 토큰이 그 절의 주제이고 5/5·두 커널 같으면 한정어와 함께 결론·그림·정리·복습에(Ch 19 04·Ch 28 05·06), 주제가 아닌 절은 표·둘째 단락에(Ch 26·27·Ch 28 04)」)을 더하는 것은 전체 마감 몫(§18).
- **흔들린 값 — 결론·그림·정리·복습에 쓰지 않음**(결과 읽기 둘째 단락·b6 표·b7에만): 답 글(04·05 도구 없는 요청·06) · 출력 토큰(04 32 ↔ 노트북 밖 37 · 05 도구 없는 요청 29 ↔ 30) · 예상 비용 · 도구 인자(노트북 밖 `{'topic': '운영'}` — 06은 출력하지 않음). 05 도구 없는 요청은 노트북 밖 다섯 번 가운데 셋이 서버 규정에 없는 토요일 시각을 적음(b7, 마감 B-5에서 출력에 없는 백틱 값 뺌).
- **기기마다 다른 값**: 03 서버 프로세스의 환경 변수 이름 목록(교재 출력 Linux 커널 열 이름 — `TERM`은 ipykernel이 넣고 `LC_CTYPE`은 서버 쪽 Python이 만듦, Windows는 기본 목록부터 다름) — **마감 재실행에서 이름 수 출력을 빼고**, 결론 값은 가짜 이름 `True`/`False`·읽은 값·「After보다 늘어난 이름 수: 1」로 · 01~06 「고른 파일 위치」(작업 폴더마다 — 결과 읽기에 밝힘).
- **노트북 밖에서만 본 값(b7에 「노트북 밖」 표시)**: `keep_alive` 기본값이면 블록 뒤 자식 1이 남음 · 스크립트에서는 `TERM`이 없어 이름이 하나 적음 · `LC_CTYPE` 생성과 끄는 설정 · `env` 없는 stdio 서버의 시작 안내·새 판 확인 27줄 · 02 서버 오류 기록 27줄·5줄 · 없는 도구도 설치판은 `isError` 결과 · 포트를 다른 프로그램이 쥐면 준비 확인이 곧바로 참(검토 A 재현 — 마감 코드가 막음) · `Path` 대상 `MCPAdapter`의 자식 남음(04 b7).
- **재지 않은 것·실행하지 않은 것**: 걸린 시간(모든 절) · Windows·macOS 실행 · 알림(`listChanged`)·기록 받기 · `Origin` 검사 · OAuth 2.1 인가 절차 · 규격 판 헤더 출력 · 인자 `mode` 외 연결 모양 · `UvStdioTransport` 등 다른 전송 · 요청 셋 이상인 에이전트 실행·도구를 여러 번 부르는 실행 · 커널을 다시 시작할 때 남은 HTTP 서버가 끝나는지(03 마감).

## 8. 비동기 허용 범위와 자식 프로세스·포트 정리 규칙

- **비동기**: 셀 맨 위 `async with Client(...)`·블록 안 await(01이 첫 풀이 — `with open`처럼 닫는 줄, IPython의 셀 맨 위 await, 파일에서는 `async def` + `asyncio.run`, 노트북 셀에서 `asyncio.run` 안 씀) · `async def`는 함수 안에서 await가 필요할 때만 셀당 하나(02 `call_tool_row`·06 `run_agent`) · `ainvoke`(04 첫 자리 — MCP 도구는 비동기 몸통만 있어 `invoke`가 `NotImplementedError`) · `asyncio.gather`·`create_task`·`nest_asyncio` 안 씀.
- **stdio**: MCP 설정 한 벌에 **`"keep_alive": False`**(연결을 닫을 때 서버도 끝남 — 기본 `True`면 셀을 다시 돌릴 때마다 쌓임) + **`"env"`에 FASTMCP 세 이름**(`FASTMCP_SHOW_SERVER_BANNER=false`·`FASTMCP_CHECK_FOR_UPDATES=off`·`FASTMCP_LOG_LEVEL=WARNING` — 표준 오류 0줄·네트워크 없음). 칸 `env`는 SDK 기본 이름(설치판 mcp 2.2.0 `client/stdio.py` 40~57행 **`HOME·LOGNAME·PATH·SHELL·TERM·USER`**, Windows는 다른 열둘, 있는 것만 — 75~90행 `get_default_environment`) 위에 더해짐(128행). **노트북 환경을 통째로 넘기지 않음**(03 Before 결함).
- **HTTP(03)**: 같은 루프 작업으로 띄우면 소켓이 남아 **자식 프로세스**(`subprocess.Popen`)로, **`127.0.0.1`만**, `show_banner=False`, 서버 기록 버림. **마감 규칙(A-7·A-12)**: ① 띄우기 전에 포트가 비었는지(`wait_for_port(auth_port, check_limit)`이 거짓인지 `assert`) ② `Popen(…, env=http_env)` — `get_default_environment()` + 세 이름만 ③ 띄운 뒤 준비 확인과 **`auth_process.poll() is None`**을 함께 `assert` ④ 마지막 셀 `terminate()`·`wait()`(종료 코드 `-15`)·자식 0·포트 닫힘. 띄우는 셀만 두 번 실행하면 앞 서버가 남으므로 마지막 셀로 끈 뒤 앞 셀부터(끄지 못했으면 커널을 다시 시작 — 남았으면 앞 셀이 포트 번호를 바꾸라고 알림). 포트 번호·준비 시도 횟수는 출력하지 않음.
- **메모리 연결 서버의 오류 기록**: 같은 커널 표준 오류로 가므로 `logging.getLogger("fastmcp").setLevel(logging.CRITICAL)`(02·05). stdio 서버의 도구 오류 기록(ERROR)은 `WARNING` 설정으로 막히지 않지만 셀 출력이 아니라 커널 쪽 표준 오류로 감(04 확인).
- 끝나면 남은 서버 프로세스 0(`pgrep -af 'course_server|env_server|auth_server' | grep -v pgrep`) — 마감도 03 A·B·서버 파일 대조·묶음 실행 검사·화면 검사 뒤 모두 0.

## 9. 모델 요청 수와 예상 비용

| 절 | 노트북 한 번 | 흔들림 확인(노트북 밖) | 새 커널 A + B | 작업 전체 | 예상 비용 어림(작업 전체) |
|---|---|---|---|---|---|
| 01 | 0 | 0 | 0 + 0 | **0** | 0 |
| 02 | 0 | 0 | 0 + 0 | **0** | 0 |
| 03 | 0 | 0 | 0 + 0(마감 재실행도 0) | **0** | 0 |
| 04 | 2 | 10(5회 × 2) | 2 + 2 | **14** | 약 0.0033달러 |
| 05 | 5 | 25(조건 다섯 × 5회) | 5 + 5 | **35** | 약 0.0080달러 |
| 06 | 4(2 + 2) | 20(두 실행 × 5회 × 2) | 4 + 4 | **28** | 약 0.0073달러 |
| 합 | 11 | 55 | 22 | **77**(마감 0) | **약 0.019달러** |

- 다시 센 방법: `probe/probe-04-P.jsonl`(회차 다섯, `requests` 2씩) · `probe-05-P.jsonl`(요청 줄 스물다섯) · `probe-06-P.jsonl`(실행 열, `requests_detail` 2씩)과 노트북 출력(04 `모델 요청 수: 2`, 05 입력 토큰 줄 다섯, 06 `모델 요청 수: 2` 둘) — 인계의 절별 값과 같음. 탐색 스크립트는 가짜 키 글로 요청 0.
- 예상 비용은 과정 요금표(2026-09-17, mini 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰)로 어림한 값이고 청구 금액이 아님(흔들림 확인 기록의 `cost`·`cost_notebook_way` 합 + A·B 출력). 절마다 1달러 안. 06은 실습 절 기준 3~5번 안(4번).

## 10. 06절 실습 절 주제와 결과

- 제목 「**MCP 실습: 에이전트에 붙이는 MCP 도구를 하나에서 셋으로 늘리기**」, 슬러그 `06-MCP-실습`, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~05 meta 합 강의 1h × 5 = **5h** · 실습 2·3·2·2·2 = **11h** = `chapter.json` 「총 16h · 강의 5h · 실습 11h」(`_build_index.py`도 5·11).
- 붙인 앞 절 기능 셋(두 실행 모두 흐름 안에서 쓰임): **02** 서버 객체에 데코레이터 줄로 도구 붙이기(`runpy`로 읽은 서버 객체에 `@server.tool` 둘 — 05 4절 셀 글 그대로, 파일 그대로) · **04** `MCPAdapter` 메모리 연결 → `create_agent` + 호출 한도 3 → `await ainvoke`, 셈 · **05** `spec_length`·`usage_metadata["input_tokens"]`(요청마다). 뺀 것: 03 전송·접근 토큰 · 04 손 요청 · 05 직접 도구·설명을 늘린 도구 · 01 기능 목록.
- 실행 1(`tool_count = 1`, 명세 252자) → 실행 2(**값 하나 `tool_count = 3`**, 685자). 모델 요청 **4번**(2 + 2). b2 「새로 볼 것」은 05가 재지 않은 **둘째 요청과 실행 합**만(첫 요청 187·252는 「05절 5절에서 본 값과 같음」 — Ch 26 B-7 교훈).
- 결과(새 커널 두 번 24/24 같음·`outputs_sha256`까지 + 노트북 밖 5회차, 두 실행 모두 5/5): 두 실행 모두 메시지 넷·`lookup_policy` 한 번·요청 2·셈 `True`, 도구 셋을 붙여도 `lookup_policy`만 부름 · 요청마다 입력 토큰 **187·243 ↔ 252·308** → `늘어난 입력 토큰: 65` 두 줄 · 합 430 · 560 · 차 130 → **「흔들림 확인 다섯 번과 두 커널에서 모두, 도구 셋을 붙인 실행은 첫 요청과 둘째 요청에서 입력 토큰이 65씩 많았다」**(둘째 요청에도 붙인 도구 명세가 실림 — 설치판 `factory.py` 1431~1438·1500~1505행과 맞음). 04 5절(stdio, 도구 하나)의 입력 토큰 합도 그 절의 이번 실행에서 430(마감 B-7 — 06 b7).
- 코드 셀 24(실습 선례 19~28) · 코드 줄 137 · 함수 본문 4·7·6줄. `assert`는 파일 찾기·키 셀뿐.

## 11. 도구 파일 `notebooks/connect_tools.py` — 함수 표·해시 변천·생성기 대조 사슬

| 함수(인자) | 배운 곳 | 가져오는 절 | 하는 일 |
|---|---|---|---|
| `names_of(items)` | **Ch 28 01 노트북 4절** | 03·04·05·06 | 목록의 항목마다 이름 칸 `name`을 모음 |
| `async def call_tool_row(server, tool_name, arguments)` | **Ch 28 02 노트북 2절** | 03 | 도구 하나를 부르고 결과·오류를 딕셔너리로(`try/except ToolError`) — 서버 객체·MCP 설정 딕셔너리·`StreamableHttpTransport` 모두 받음 |
| `stdio_config(server_path, env)` | **Ch 28 03 노트북 2절** | 04·05 | 서버 파일 하나를 stdio로 띄우는 설정 한 벌(`keep_alive: False`) |
| `tool_call_names(response)` | Ch 19 04 | 04·05·06 | 응답 하나의 도구 호출 요청 이름 목록 |
| `sum_usage(messages)` | Ch 19 05 | 04·06 | 목록 안 응답마다 요청 하나·토큰 합 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06 | 04·05·06 | 예상 비용(`.get` 둘 — 허용 표시) |
| `spec_length(tools)` | Ch 19 03 | 05·06 | 도구 명세 JSON 글의 글자 수 합 |

- 함수마다 `# Ch NN MM절에서 배웠습니다 — …` 주석, 가져오기 줄 `json`·`sys`·`fastmcp`(`Client`·`ToolError`)·`langchain_core`(`convert_to_openai_tool`), 노트북 전역 이름 기대기 0, 금지 문법 0. 앞 셋은 01·02·03 노트북 셀과 주석·본문이 글자 같음, 가운데 셋은 Ch 21 `runner_tools.py`(`f4113158…`)와 같은 본문, `spec_length`는 Ch 19 03 셀(`8afb6cff…`)과 글자 같음. **이 파일을 가져오는 03~06 설치 셀에 `fastmcp==4.0.3`·`langchain-core==1.6.2`**(03은 마감에서 더함 — 규격 §2-7 6번). **01은 가져오지 않음**(묶음 실행 검사 계약), 서버 파일도 가져오지 않음(자식 프로세스는 `PYTHONPATH`를 받지 않음).
- **해시 변천**: 없음 → 03 `9139c4f8…`(`names_of`·`call_tool_row`) → 04 `cc066bd7…`(+ `stdio_config`·`tool_call_names`·`sum_usage`·`estimate_cost`, `import sys`) → 05 **`570ed3cc607871a374ac1d5d7fc3ba6435908669ae79f48908535787d16f204c`**(+ `spec_length`, `import json`·`convert_to_openai_tool`) → 06 그대로 → **마감 그대로**(챕터 리드 결정). 03 마감 재실행도 이 05 판으로 실행(B는 `--tools-copy`).
- **머리 설명**: 첫 줄 「앞 챕터와 이 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다」 + 가져오는 법·같은 폴더·함수마다 배운 곳 주석·「이 챕터 앞 절 노트북에서 옮긴 함수는 셀 글 그대로」·인자로만 받음·서버 파일은 가져오지 않음. 함수 전부를 두루 가리키는 말이라 **지금 판과 어긋나지 않음** — Ch 24~27 「도구 파일 머리 설명」 전체 마감 항목에 Ch 28은 덧붙이지 않음(README가 함수 일곱의 배운 절·가져오는 절을 적음).
- **생성기 대조 사슬**(마감에서 다시 확인 — 모두 통과, 쓰기 없음, `.cache/ch28-close/tools/chain28.py`): `author_03.TOOLS`(`TOOLS_HEAD` + 01·02 셀 글, 원본 해시 고정) → `author_04.TOOLS`(03 판 + `import sys` + 03 셀·Ch 21 판 셋) → `author_05.TOOLS`(04 판 + 가져오기 둘 + Ch 19 03 셀) = **디스크 파일**. `author_03.later_version(디스크)`·`author_04.later_version(디스크)` 참 → 03·04를 다시 돌려도 덮어쓰지 않음(03 마감 재실행에서 `skip` 확인), 05 쓰기 가드 「같은 판」, 01·02·06은 도구 파일을 쓰지 않음. 여섯 생성기 `cells()`가 노트북과 53·53·57·54·60·52셀 차이 0, `src_html()` = `_src` 6/6, `check_tools`·`check_same_as_prev`·`check_same_as_probe` 통과. **주의**: 04~06 키 셀 결과 읽기의 실행일 문장은 `nbkit.RUN_DATE`(= 오늘)라, 날짜가 바뀐 뒤 대조할 때는 `UPGRADE_RUN_DATE=2026-09-28`을 줘야 차이 0(마감 대조가 2026-09-29 UTC에 걸쳐 확인함 — 노트북 글은 실행일 2026-09-28 그대로). 설명만 고칠 때는 `--src-only`(또는 마감의 `gapply.py`) → `run_section.sh … NN --no-exec`.

## 12. 서버 파일 셋과 묶음·검사 (마감)

| 서버 파일 | 해시 | 쓰는 절 | 비고 |
|---|---|---|---|
| `course_server.py` | `d7f7e8b9…` → **`5dc7733364210325e3ebd734495a908f7dc7ab28f4c0dc22c645c094456953d9`**(마감) | 01·02·05·06 메모리(`runpy`) · 03·04·05 stdio | 도구 `lookup_policy`(`tags={"public","read"}`·`-> str`)·자료 `policy://handbook`·메시지 틀 `explain_policy`. **마감 문법 고침(A-17)**: 자료 함수의 f-string + 제너레이터 식 → 빈 목록 + `for` + `append` + `"\n".join`, 메시지 틀의 f-string → 글 이어 붙이기. 모듈 이름(파일이 만든 이름 여섯) 그대로 |
| `env_server.py` | `8b4c40bc…`(그대로) | 03 stdio | 도구 `env_names`·`env_value`(연습용 — 파일 머리에 「실제 서버에는 두지 않음」) |
| `auth_server.py` | `8f41e542…`(그대로) | 03 HTTP | `StaticTokenVerifier`(개발·시험용)·`require_scopes("admin")`, 포트는 명령 줄 첫 인자 |

- **서버 파일 문법 고침의 근거**(모델 요청 0, 파일 쓰기 0 — `/tmp/ch28-close/srv/srvcmp.py`): 옛 판·새 판을 임시 폴더에 두고 01~06이 쓰는 입력으로 대조 — 파일이 만든 이름 · 자료·메시지 틀 함수 직접 호출(주제 넷 + 빈 글) · 메모리 연결 기본·옛 판 모드의 판 번호·기능 목록·서버 정보·사용 설명·세 목록(모델 덤프)·`read_resource`·`get_prompt`(주제 넷)·`call_tool`(대출·운영·연체·주차·3) · `MCPAdapter` 메모리 연결의 명세 JSON(252자)·`args_schema`·꼬리표·`ainvoke`(운영) · stdio(`keep_alive: False` + 세 이름) 목록·자료·메시지 틀·호출·`MCPAdapter` 명세 → **18항목 10,787바이트 글자까지 같음**. 그래서 01(묶음 계약)·02·04·05·06 출력은 바뀌지 않고 다시 실행하지 않음. 03은 새 판으로 다시 실행해 2절 stdio 결과가 옛 출력과 같음을 확인. 남은 줄(데코레이터 인자·`-> str`·독스트링·집합 `{"public", "read"}`)은 02가 「서버 파일에 있는 줄」로 푼 모양이라 그대로. 다른 서버 파일 둘은 금지 문법 0(AST).
- **묶음**: `python3 textbook/part6/_build_index.py`(README·노트북·서버 파일·`chapter.json`·목차 줄·continuity-guide를 모두 고친 뒤 마지막에 한 번) → **`Part 6: 55 verified sections; 108 bundled files`**, `part6-practice.zip` `1a4059ab…` → **`5002dce3666f6198ce06225a8518ce1acbd473862d5d2f40dbb61d42b7bfbcfe`**(111항목, **Ch 28 13파일과 `continuity-guide.md`가 모두 디스크와 같음**, `__pycache__`·`.env`·`.venv` 0). 공개 목록: 챕터 목록 옛 SVG 다섯 줄 뺌(`68b20d31` → `e0533bb7`), Part 목록은 `collect_public_files.py`로 다시 모아 바이트 같음(`498845c7`, `Explicit public files: 92; prerequisites: 13`) — 도구 파일·서버 파일 셋·06 노트북 줄 있음.
- **묶음 실행 검사 계약**(Part 6 `check_bundle_execution.py` — 목록은 Ch 24 01·Ch 28 01): `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink` 환경 변수만(스크립트 수정 0, `TMPDIR`은 세션 홈 `/sessions/…/tmp` — 맥 마운트 밖, 키 환경 변수 지움) → **PASS**(Ch 24 01 `7187f7a39f3f…` 28셀 · **Ch 28 01 `2407c4c571382b4f55de5aae1c30de28f4810518cc62e29fb6526524b5ca7b21` 25셀**, 작업 폴더 = 풀린 `notebooks/`, `uv sync --locked`). `bundle-execution.json` `4f39acac`(옛 zip·옛 01 `a09d959cecc4…` 4셀) → **`fc4e1b78540d93d07631c4310b6d992fdb0e693620425c3d9b537b8a01e64870`**(`archive_sha256` = 새 zip). **01 계약**: 키·모델 객체·`dotenv`·포트·자식 프로세스·도구 파일 없이 메모리 연결만, 파일 위치 첫 후보 `../course_server.py`. 01 코드 셀을 바꾸면 이 값이 바뀜.
- **전달 검사**(Part 6 `check_delivery.py`): 117행 `llm-practice.zip`의 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤(알려진 일, `delivery-results.json` `3cc2d143…` 안 바뀜). 그 zip을 뺀 사본(`.cache/ch28-close/dx/check_delivery_nollm.py` — 바꾼 줄 셋: 루트·zip 목록·결과 파일 자리)은 **HTML 66 · 로컬 링크 1,530 · 누락 0 · 절 55 · 코드 셀 1,266 · 복습 216문항 오류 0 · SVG 241 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` 111항목(part6 노트북 55)** 통과.
- **화면 검사** `visual.cjs`(1280px·390px): **14행 PASS**(`textbook/_notebook/checks/ch28-mcp/visual-results.json` + 스크린숏 넷 새로). Part 6 공용 `qa/visual-results.json`은 **Ch 28 줄만** 12 → 14(06 두 줄, 새 HTML 해시), `screens` 128 → 130, 다른 챕터 줄 116개 그대로.
- **옛 검사 스크립트(고치지 않음, 돌려서 멈춘 자리만 기록)**: Part 6 `check_scope.py` — Ch 21 07 `Missing scope`에서 멈춤(Ch 28에 닿기 전, **`SECTION_COUNTS` ch28 5 ≠ 6**도 남음) · `check_figures.py` — Ch 21 `01-1-….svg`의 `.excalidraw` 짝 · `check_notebook_readiness.py` — `assert len(reports) == 47`(Part 6 노트북 55), **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림**(`b3d69e9c…`) · `check_visual_reports.py` — `ch22-middleware` · `textbook/qa/check_course_continuity.py`(시스템 파이썬 3.10에 `tomllib`이 없어 챕터 가상환경 3.12로) — 212행 `llm-practice.zip` Part 1 Stale에서 멈춤(`textbook/qa/*.json` 안 바뀜).

## 13. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part6/ch28-mcp/notebooks/01~06-*.ipynb` | 01~06절 · **마감** | 실습 폴더(챕터 몫) — §1. 마감: **03만 다시 실행**(`code_sha256` `04c437f720bc…` → `0935bc12bf4e…`, 파일 `3ea536db` → `c1f22daa`), 나머지는 마크다운만(코드·출력·`executed_at` 그대로) — 01 `049d4608`→`ee6068c3` · 02 `19d05788`→`46231dee` · 04 `13b49a27`→`78cbb550` · 05 `9b4b0138`→`d4db557b` · 06 `4ad6dfbd`→`bad09ea5`(06-1 첨부 교체). 도구 파일 그대로 `570ed3cc…` |
| `labs/part6/ch28-mcp/course_server.py` | **마감** | 문법만(`d7f7e8b9` → `5dc77333`, 값 같음 — §12). 보호 파일 |
| `labs/part6/ch28-mcp/README.md` | 06절(06 단락) · **마감(전체)** | `5b72cb94…`(원본) → `9cd50583…` → **`2de0808f136f…`**: 노트북 여섯, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절별 설치 판, **모델 요청 01 0 · 02 0 · 03 0 · 04 2 · 05 5 · 06 4**, 01~03 키 없음·04~06 키 필요, 01은 묶음 실행 검사 대상(키·모델·도구 파일·자식 프로세스 없음), 예상 비용(요금표 어림, 청구 금액 아님), 키는 프로젝트 맨 위(학생 묶음이면 `part6-practice/`) `.env`의 `OPENAI_API_KEY`에서만, 서버 파일 셋, 자식 프로세스·포트 정리(`keep_alive: False`·마지막 셀·세 이름만·포트 확인), 도구 파일 단락(규격 §2-7 고정 문장 뜻·함수 일곱·배운 절·가져오는 절·가져오는 패키지), 절마다 하는 일, 06 단락. 옛 「어댑터 컨텍스트」·「실패 진단 JSON」·「리소스·프롬프트·측정·의존성·하위 프로세스」 모두 뺌, 묶음 밖 파일을 가리키지 않음, 참 금지어 0(「프로그램」 거짓 양성 말고) |
| `textbook/part6/ch28-mcp/chapter.json` | 06절 · **마감** | 06 절(06절) · `objectives` 넷 → **다섯**(§15), `hours` 그대로(`f4b0bbc6` → **`e2eaf6c8`**, 보호 파일) |
| `textbook/part6/ch28-mcp/index.html` | 06절 · **마감** | `_build.py`(목표 다섯, `a3b20d23` → `5e7123eb`) |
| `textbook/part6/ch28-mcp/qa/public-files.json` | 03·06절 · **마감** | 서버 파일 둘·도구 파일(03)·06 HTML·노트북(06) · **옛 SVG 다섯 줄 뺌**(마감, `68b20d31` → `e0533bb7`, 파일 그대로) |
| `textbook/part6/public-files.json` | 03·06절 | `collect_public_files.py` — 마감에서 다시 돌려 **바이트 같음**(`498845c7`), `prerequisite-files.json` 같음 |
| `textbook/part6/_build_index.py` | **마감** | ch28 설명 「MCP 서버와 클라이언트를 연결하고 도구 정의의 입력 토큰을 확인합니다.」 → 「서버 파일의 MCP 서버에 메모리로 붙어 판 번호와 기능 목록을 보고, 서버 객체에 도구를 붙여 입력 검사를 확인하며, 서버를 자식 프로세스와 HTTP 서버로 띄워 넘기는 환경 변수와 접근 토큰의 범위를 견준 뒤, MCPAdapter로 바꾼 도구를 에이전트에 붙여 도구 정의가 더하는 입력 토큰을 세고, 에이전트에 붙이는 도구 수를 바꾸는 실습을 합니다.」(시수 5·11 그대로, → `2020202a`, 보호 파일) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | **마감** | Ch 28 설명 「서버와 클라이언트를 직접 연결하고 도구 정의의 입력 토큰과 권한 경계를 확인합니다.」 → 「서버에 도구를 붙여 기능 목록과 입력 검사를 보고, 전송마다 넘기는 값과 접근 토큰의 범위, 도구 정의가 더하는 입력 토큰을 확인합니다.」. **절 수 5는 그대로**(실습 절을 빼고 세는 과정 약속). 스크립트를 돌리기 전 옛 스크립트 출력이 지금 `index.html`과 바이트까지 같았고(`.cache/ch28-close/index-old-script.html`), 다시 만든 뒤 바뀐 것은 Ch 28 설명 하나(`→ cde0dc13` · `2c14ab24` → `64bfbb36`, 보호 파일) |
| `labs/part6/continuity-guide.md` | **마감** | 14행 Ch 28 줄 「Ch19의 도구 정의와 호출 비용 \| Ch28 MCP 서버·클라이언트와 도구 정의 토큰 \| Ch37의 비용·컨텍스트 측정」 → 「Ch19의 도구 정의·입력 검사·호출 비용, Ch21·22의 에이전트와 호출 한도, Ch23의 자식 프로세스 \| Ch28 MCP 서버와 클라이언트, 서버에 도구 붙이기와 입력 검사, stdio·HTTP 전송에서 넘기는 환경 변수와 접근 토큰의 범위, `MCPAdapter`로 바꾼 도구와 도구 정의가 더하는 입력 토큰 \| Ch30 FastAPI 서빙의 요청 헤더 인증」(없는 「Ch37」·금지어 「측정」 뺌 — Ch 30 07이 `Authorization: Bearer` 인증을 다룸을 확인, → `f549f3ad`, 보호 파일, 묶음에 들어감) |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | 06절 + **마감** | §12 — `index.html` `a4964c57` → `4e3d5941`(Ch 28 섹션 설명 한 줄만), zip → `5002dce3`, `integration-results.json` `8cc9b160` → `7a46d6c8` |
| `textbook/part6/qa/bundle-execution.json` | **마감** | §12(`4f39acac` → `fc4e1b78`) |
| `textbook/part6/qa/visual-results.json` · `textbook/_notebook/checks/ch28-mcp/visual-results.json`(+ 스크린숏 넷) | **마감** | §12 — 공용 파일은 Ch 28 줄만 12 → 14·`screens` 130(`→ 24d74549`, 보호 파일), 챕터 결과 `→ 831667dd`, 스크린숏 넷(index·01 × 1280·390) 새로 찍음(보호 파일) |
| `textbook/part6/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 다시 써서 실행 전 사본으로 되돌림(내용 변경 0, `b3d69e9c…`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(마감 뒤 `1613295a…`) |
| **`qa/author_ch28.py` → `qa/upgrade/before/generators/blocked/author_ch28.py`** | 01절(막음) · **마감(`mv -n`)** | `41a3af28bfed25ea4f147cb42c4a247d837c9bb47a5bac1ee51dd751f77dbbac` 같음(01절이 첫머리에 `raise SystemExit`). 부르는 빌드·검사 스크립트 0(`grep` — 기록 문서·`before-manifest.json`뿐) |
| **`figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/_gen_figures.py`** | 01절(막음) · **마감(`mv -n`)** | `5bb85474bbd9c0f65e2a844dfb918e1b404d7bd5e0b85e94b2587beff5f6fa2d` 같음. 부르는 스크립트 0. `before/generators/`의 두 원본 사본(막기 전)은 그대로 |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` · `textbook/qa/upgrade-contracts.md` | **마감** | 진행표 Ch 28 행 한 줄 · 체크리스트 §2-16 Ch 28 항목, §3·§4 Ch 28 줄 · 계약 §5 「Ch28 마감 뒤」 한 줄(묶음 실행 검사 01 새 값) |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약 · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`render_mermaid.py`·`attach_figures.py`) · Part 6 옛 검사 스크립트와 `check_*`·`collect_public_files.py` · `textbook/qa/check_course_continuity.py` · Part 6 `_src/index.html`·`practice-start.md`(Ch 28 문장 참 — 「Ch 28의 MCP로 연결 범위를 넓힙니다」) · `textbook/part6/qa/final-artifact-hashes.json`·`notebook-executions.json`·`ch28-technical-review.md`·`ch28-before-path-repair/`(옛 기록) · 실습 폴더 `pyproject.toml`·`uv.lock` · 도구 파일(해시 고정) · 서버 파일 둘(`env_server.py`·`auth_server.py`) · 삽화 · **Ch 29 이후 파일 전부**(Part 6 목차·묶음·공개 목록·기록·`continuity-guide.md` Ch 28 줄 말고 — Ch 30 07은 읽기만) · `llm-practice.zip`·`delivery-results.json` · claude.ai 프로젝트 문서.
- **파일을 지운 것은 없습니다.** 옮긴 것은 옛 생성기 둘(`mv -n`, 해시 같음). 옮긴 뒤 `_build.py`·`verify.py`·게이트·묶음 검사 통과. 마감이 기기에 만든 것: `/tmp/ch28-close/`(03 수정 스크립트 `m03.py`·시험 판 `author_03.try.py`·사본 `B03/`·서버 파일 대조 `srv/`·코드 줄 사본 `cc/`·`cc3/`·목차 사본, 약 0.8MB) · `.cache/ch28-close/`(마감 전 사본 `pre/`·확인 스크립트 `tools/`·치환 목록 `reps/`·옛 검사 결과 `oldcheck/`·`llm-practice.zip`을 뺀 전달 검사 사본 `dx/`·로그 `log/`·해시 기록, 약 5MB).
- **보호 파일 226개(`before-manifest.json`)**: `manifest-changes.md` 「마감 뒤」.

## 14. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `langchain[mcp]==1.4.0`·`langchain-openai==1.6.0`·`fastmcp==4.0.3`·`mcp==2.2.0`·`python-dotenv==1.2.3`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`): `langchain-core 1.6.2`·`langgraph 1.2.11`·`httpx 0.28.1`·`psutil 7.2.2`·`pydantic 2.13.5`. 노트북 `%pip`: 01·02 둘 · 03 다섯(마감 `langchain-core` 더함) · 04 여덟 · 05·06 여섯(잠금 판).
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch28-mcp`(잠금 판). 실행일 2026-09-28(01 19:32 · 02 20:07 · 03 **23:43(마감 재실행)** · 04 21:25 · 05 22:08 · 06 22:42 UTC). 모델 `gpt-5.4-mini`.
- 설치판 소스 행(검토 A·B와 마감이 다시 확인): mcp 2.2.0 `client/stdio.py` 40~57(기본 이름·win32 분기)·75~90(`get_default_environment`)·128 · `client/streamable_http.py` 383~412 · fastmcp 4.0.3 `server/low_level.py` 562~564(옛 판에서 `extensions`를 뺀다는 설명)·574(`io.modelcontextprotocol/ui`)·`apps/config.py` 1~18 · `client/transports/stdio.py` 64~66·92~95·486~492·553~556·615~618 · `server/server.py` 905~914·1541 · `server/auth/middleware.py` 81~83 · `server/auth/providers/jwt.py` 662 · `utilities/cli.py` 201~205 · langchain 1.4.0 `langchain/mcp/__init__.py` **9~12(끄는 방법)·17·26~30(경고 — 마감 B-2)** · `adapter.py` 84~122(글자 대상은 주소, 오류 안내의 `Path('server.py')`는 101~105)·174~200·221~242 · `tools.py` 104~117·261~282 · `agents/factory.py` 1431~1438·1500~1505 · `agents/middleware/types.py` 349~354(`AgentState` 칸 셋 — 마감 B-3) · ipykernel 7.3.0 `zmqshell.py` 583~587.
- 참고 자료(2026-09-28 확인 — 절 작업·검토 WebFetch): MCP versioning(현재 판 2026-07-28)·changelog(`server/discover`·세션 없앰·`Mcp-Method`·`Mcp-Name`·기록 기능 사용 중단 SEP-2577)·Tools(범위에 따른 목록 차이 MAY·정해진 차례 SHOULD·인자 없는 도구 `additionalProperties: false`)·stdio·Streamable HTTP·Authorization(403 `insufficient_scope`·stdio는 환경에서 자격 정보) · FastMCP Client(4.0 `mode`)·Transports(허용 목록·`keep_alive` 기본 참)·Authorization·Token Verification · LangChain MCP(`Path("weather_server.py")`·어댑터 하나에 자식 하나)·Connections·Migrate · OpenAI Function calling(토큰 한도에 닿으면 함수 수·설명 줄이기 제안 — 마감 B-6).

## 15. 강사 확인 대상

1. **제목 말**: 01 「capability 협상」(현재 판은 첫 협상 요청이 없음 — 본문은 요청마다 판 번호를 싣는 것까지 협상으로 설명) · 02 「FastMCP」 · 03 「stdio」 · 04 「LangChain MCP」 · 05 「첫 호출」(본문 「첫 요청」) · **06 긴 제목**(「MCP 실습: 에이전트에 붙이는 MCP 도구를 하나에서 셋으로 늘리기」)·슬러그. 슬러그 01은 Ch 27 09 b8이 링크해 고정.
2. **`chapter.json` 학습 목표 넷 → 다섯**(01 연결·기능 목록 · 02 도구 붙이기·입력 검사 · 03 전송·환경 변수·접근 토큰 범위 · 04~05 `MCPAdapter`·도구 정의 몫 · 06 실습 — 「리소스」·「프롬프트」·「capability」·「측정」·「최소 권한」을 뺌, `hours` 그대로) · `_build_index.py`·`build_index.py`·`continuity-guide.md` Ch 28 문구(뒤 칸 「Ch30 FastAPI 서빙의 요청 헤더 인증」) · README 다시 쓴 범위.
3. **입력 토큰 결론 판단**(B-11): 05·06은 한정어와 함께 결론에, 04는 표·둘째 단락(마감에서 표 줄 분리) — Ch 26 04·Ch 27 03과 갈림. 과정 요약 §7 적용 선례 한 줄(§7·§18).
4. **코드 양**(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」): 코드 줄 284 → 887(01 131·02 125·03 158·04 163·05 173·06 137) + 도구 파일 57 · 코드 셀 22 → 152 · 03 마감 재실행으로 셀 25 → 26(포트 확인 셀). 여섯 노트북이 같은 8줄 파일 위치 셀(후보 셋)을 되풀이 — 학생 자리(`notebooks/`) 하나로 줄일지(검토 A 「사람이 정해야 할 것」 4).
5. **02 paired 한 조건 원칙**(A-5): 힌트와 독스트링을 함께 바꾼 Before·After를 코드 그대로 두고 글로 공개(거절을 가른 것은 입력 형식의 `topic` 칸) — Before에도 독스트링을 두고 02를 다시 실행할지.
6. **03**: 서버 파일 둘을 실습 폴더 맨 위에 둔 결정(학생 묶음에 두 파일) · 연습 서버의 `env_value` 도구 · 고정 포트 58028(마감에서 포트 확인·`poll()` 셀을 더함 — 셀 하나 늘어남) · `%pip`에 `httpx`·`psutil`(잠금의 간접 의존 — `pyproject.toml` 직접 의존 아님)·`langchain-core`(도구 파일 몫, 마감) · 마감에서 쓴 새 이름 `get_default_environment`(SDK 기본 이름을 HTTP 서버에도 — 과정 처음) · Windows 학생 안내 범위(기본 목록 열둘·종료 코드·자식 수 — b7·복습 3에 한 문장씩) · 새 용어 6·「자식 프로세스」 이어 씀 · 「토큰」을 모두 「접근 토큰」으로 · 삽화 팔각형 몸체.
7. **04**: 새 말 넷(특히 「아티팩트」 — 한 셀·용어 표에서만 쓰임, 셋으로 줄일지) · `MessagesState` 과정 첫 사용 · `langchain_core._api`에서 경고 종류를 가져와 끄는 가져오기 줄(문서 9~12행이 적은 방법) · 설치 셀 여덟 · `show_messages` 대신 내용을 뺀 셀.
8. **05**: 도구 없는 요청의 답 글을 출력한 셀(두 커널에서 갈림·규정에 없는 시각이 나올 수 있음) · 직접 도구 `@tool("lookup_policy")`로 파이썬 이름과 가름 · 서버 파일 객체에 커널 안에서 도구를 더 붙인 셀 · 새 말 둘.
9. **06**: 코드 셀 24 · 바꾼 값을 05가 이미 첫 요청으로 견준 도구 수로 두고 「새로 볼 것」을 둘째 요청·실행 합으로 한정 · 새 함수 셋을 노트북에 · 05 `@server.tool` 정의 둘을 노트북에 다시 적음(서버 객체에 묶여 도구 파일로 못 옮김) · 삽화 격납고가 창고처럼 보임 · 05 b8의 Ch 29 링크를 06 b8로 옮김 · **06-1·06-3 색을 챕터 공통 규칙으로 바꿈**(B-10 — 과제 지시의 「라이브러리 클래스 회색」 배정을 버림).
10. **서버 파일 `course_server.py` 문법 고침**(A-17 — 챕터 리드 결정대로 값 대조 뒤 고침): 학생 묶음 파일 해시가 바뀜(`5dc77333…`).
11. **삽화 여섯**: 01 우주선 몸체·여백·고리 크기 · 02 왼쪽 공 크기·여백 · 03 작은 해치·팔각형 · 04 가려진 네모 자리·깎인 모서리 · 05 책 모양·겹친 모듈·여백 · 06 격납고 · **작업 조회 결과의 모델 표시 `nano_banana_2`와 요청 `nano_banana_pro`가 다름**(기록만).
12. **01 b3 Ch 6 계층 이름 인용**(「프롬프트」 한 곳 — 금지어 예외) · 01이 빈 FastMCP 서버 객체를 하나 만듦(02 주제의 한 줄 앞당김).
13. **01 그림 설계표를 렌더 뒤에 적은 차례**(A-4 — 기록만, §20).
14. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: 삽화 직접 판독 일부, Windows·macOS 실제 실행, `%pip`만으로 만든 새 환경, 학생 `uv sync --locked` `.venv` 첫 셀).

## 16. Ch 29가 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 06 b8 「Ch 29 01절은 평가 방법 세 가지를 견줍니다」(Ch 29 01 링크 — Ch 29 01 b2 Final Response·Single step·Trajectory와 맞음을 검토 B가 확인). Ch 29 01 b3은 Ch 11·Ch 21만 전제해 Ch 28 산출 파일에 기대지 않음.
- 말: 도구 명세·입력 토큰·출력 토큰·요청 수 셈(「요청 수 = 도구를 요청한 응답 수 + 1」 — 한도에 닿지 않은 한 번 실행) · 호출 한도(Ch 22 04 — invoke 한 번마다).

### 전제하면 안 되는 것 (Ch 29 파일은 고치지 않았습니다)

1. **Ch 28은 뒤 챕터가 읽는 산출 파일을 만들지 않았습니다**(`runs/` 없음, 노트북 파일 쓰기 0 — 03의 HTTP·stdio 서버와 04~06의 자식 프로세스·메모리 연결 모두 끝나면 남는 것 0).
2. **도구 파일 `connect_tools.py`는 Ch 28 실습 폴더에만** 있습니다(05 판 `570ed3cc…`, `fastmcp`·`langchain_core`를 가져옴). Ch 29 실습 폴더와 잠금이 다르면 파일째 가져오지 말 것.
3. **MCP 연결은 설치판 langchain 1.4.0의 `langchain.mcp.MCPAdapter`(베타 — 경고 한 종류를 끔)만** 썼습니다. `langchain-mcp-adapters`(`MultiServerMCPClient`·`load_mcp_tools`)는 잠금에 없어 쓰지 않았습니다. LangChain 쪽으로 넘어간 것은 **도구뿐**이고, 자료·메시지 틀은 FastMCP `Client`로만(01) 봤습니다.
4. **에이전트 실행은 도구를 한 번 부르는 짧은 실행(요청 2)만** 했습니다(04 한 번, 06 두 번 — 질문은 모두 「교육센터 자료실은 토요일에 몇 시까지 운영하나요?」). 도구를 여러 번 부르는 실행·요청이 셋 이상인 실행·서브에이전트·사람 승인은 Ch 28에서 실행하지 않았습니다. 「요청마다 늘어난 입력 토큰 65·65」도 두 요청 실행의 값입니다.
5. **입력 토큰 값(56·187·218·252·243·308·430·560 등)은 `gpt-5.4-mini`·2026-09-28·설치판 판의 값**입니다. 05의 **「도구 정의 몫」은 도구 없는 요청과의 차**이고, 06의 「늘어난 입력 토큰」(도구 하나 ↔ 셋)과 다른 말입니다.
6. **평가·궤적은 Ch 28에서 다루지 않았습니다**(「궤적」은 Ch 28 금지어). 에이전트 결과를 채점하거나 기록을 남기는 코드는 Ch 28에 없습니다.
7. **접근 토큰(`StaticTokenVerifier`)은 교재용**(소스 경고 「Never use this in production」)이고 HTTP 서버는 127.0.0.1 자식 프로세스로만 띄웠습니다. 운영용 인증·원격 서버·OAuth 절차를 Ch 28이 다뤘다고 전제하지 말 것.
8. **Deep Agents 권한 규칙(Ch 27)이 MCP 도구에 걸린다고 보지 않았고, 그 조합은 실행하지 않았습니다**(03 b3 — 마감 A-13).
9. **말**: 「프로토콜」·「세션」·「리소스」·「프롬프트」(제목 밖)·「스키마」·「반환」·「측정」은 본문 0. 모델 토큰은 「입력 토큰」·「출력 토큰」, 인증 토큰은 「접근 토큰」. 「도구 호출 요청」은 모델 응답의 `tool_calls` 한 뜻. 규격 판은 현재 판 2026-07-28 기준(2025-11-25는 비교로만). 06 소재(도구 셋 서버·`tool_count`)를 Ch 29가 이어 쓴다는 약속은 없습니다.

## 17. 뒤 챕터 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 28 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 29(대기) | 01 b2·b3 | 평가 방법 셋 · Ch 11·21 전제 | 06 b8이 「Ch 29 01절은 평가 방법 세 가지를 견줍니다」로만 이음(앞당겨 가르치지 않음) | Ch 29 01이 그 문장과 맞게 남을 것 · Ch 28 파일에 기대지 말 것(§16) |
| Ch 30(Part 7, 대기) | 07 「인증 CORS 타임아웃」 · 02 `Authorization: Bearer local-demo-token` | 「토큰」 단독 · 문자열 비교 인증 | Ch 28 03은 같은 헤더 인증을 **「접근 토큰」**으로 부르고, 없거나 틀리면 **401**·`WWW-Authenticate: Bearer`, 교재용 `StaticTokenVerifier`(실제 서비스에 쓰지 않음)·범위 `read`/`admin`으로 인가 | Ch 30 개선 때 「접근 토큰」 말·401 설명을 Ch 28 03과 맞출지 확인(「토큰」 단독은 모델 입력 토큰과 겹침). Part 7에서 MCP를 쓰는 절은 없음(`grep` 0) |
| Part 6 | `continuity-guide.md` 14행 | (마감에서 고침) | — | 없음 |
| Part 6 목차 | `_src/index.html`·`practice-start.md` 15행 | 「Ch 28의 MCP로 연결 범위를 넓힙니다」 | 참 | 없음 |
| 과정 요약 | §7 결론 자리 색인 | 「결론은 요청 수 셈, 토큰·비용은 둘째 단락·표에만(Ch26 04·05)」 | 05·06은 입력 토큰을 한정어와 함께 결론에(§7) | 적용 선례 한 줄 — 전체 마감(누적 문서 몫) |
| 전체 마감 | `llm-practice.zip` 안 Ch 28 | 옛 판(노트북 다섯·옛 README — 도구 파일·서버 파일 둘·06 없음) | `part6-practice.zip`은 새 판 13항목이 디스크와 같음 | 전체 묶음 재생성 때 Ch 28 13항목 대조 |
| Part 6·7 기록 | `textbook/part6/qa/final-artifact-hashes.json`·`notebook-executions.json`·`notebook-readiness.json`·`ch28-technical-review.md`·`ch28-before-path-repair/` | Ch 28 옛 해시·옛 판(06 없음) | 기록 파일(계약·검사 입력 아님) | 고치지 않음 — Part 6 마감 때 |

## 18. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-16)

1. **옛 그림 열다섯 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~5 — 세어 15개, 본문 참조 0, 캡션에 「리소스」·「프롬프트」·「프로토콜」·「capability」·「장식자」·「검증」·「인터페이스」·「BaseTool」, 사본 `qa/upgrade/before/figures/`, **챕터 공개 목록의 옛 SVG 다섯 줄은 마감에서 뺌**). Part 6 옛 검사 `check_figures.py`가 `.excalidraw` 짝을 요구하는 것과 함께 정할 것.
2. **`gates-wip-*.json` 열셋 삭제 승인**(`gates-wip-01-01`~`06-06`·`01`~`06`·`ch28-after06` — `gates-after.json` 6/6으로 갈음, 절 번호 여섯은 마감 `run_section.sh --no-exec`가 다시 씀).
3. **캐시·임시 삭제 승인**: 실습 폴더 `notebooks/__pycache__/connect_tools.cpython-312.pyc`(05 A 22:08 — 06·마감은 만들지 않음)·`labs/part6/ch28-mcp/__pycache__/course_server.cpython-312.pyc`(**옛 `course_server` pyc, 09-10 — 옛 판 모듈 가져오기 흔적**) · 실습 폴더 `labs/part6/ch28-mcp/.venv`(macOS 판 222MB) · `.cache/vm/venv-ch28-mcp`(302MB) · `.cache/ch28-0N-view/`(N=1~6, 약 5.8MB) · `.cache/ch28-close/`(약 5MB) · 기기 `/tmp/ch28-prep`·`/tmp/ch28-01`~`/tmp/ch28-06`(약 50MB)·`/tmp/ch28-close`(약 0.8MB) · `/tmp/reviewA28`·`/tmp/reviewB28`(검토 재현 파일) · **FastMCP 판 확인 캐시** 기기 세션 홈 `~/.local/share/fastmcp/version_cache.json`(연결 폴더 밖 — 01 탐색의 `env` 없는 stdio 실행이 만든 것으로 보임) · venv 안 `mcp/server/__pycache__/fastmcp.cpython-312.pyc`(준비 단계 흔적 — 01 진단 §14) · 공용 `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`·`/tmp/uv-cache`·`/tmp/pw`·`/tmp/pw-browsers`·`/tmp/npm-cache-ch26close`(Ch 26 마감이 설치, 마감이 그대로 씀).
4. **코드 쪽 다음 재실행 몫**: 없음(03은 마감에서 다시 실행해 코드 쪽 지적을 모두 반영). 강사가 정하면 — 02 Before에도 독스트링을 두고 힌트만 뺀 판(A-5 (나), 02 재실행) · 파일 위치 셀 후보 줄이기(여섯 절) · 04 「아티팩트」 용어 줄이기.
5. **도구 파일 머리 설명**: 지금 판과 어긋나지 않아 Ch 24~27 한 항목(§2-13 6번)에 덧붙이지 않음(§11).
6. **Part 6 옛 검사 스크립트(고치지 않음)**: `check_scope.py` `SECTION_COUNTS` ch28 **5 ≠ 6**(Ch 21 07에서 먼저 멈춤) · `check_figures.py`·`check_notebook_readiness.py`(47 ≠ 55 — 결과 파일 되돌림)·`check_visual_reports.py` · `textbook/qa/check_course_continuity.py`(212행 `llm-practice.zip` Stale, 시스템 파이썬에 `tomllib` 없음) — §12.
7. **`llm-practice.zip`**: §12 · 안 Ch 28은 옛 판(§17).
8. **기록 파일의 옛 해시(계약·검사 입력 아님 — 고치지 않음)**: `textbook/part6/qa/final-artifact-hashes.json`(Ch 28 줄, 옛 생성기 옛 자리 포함) · `notebook-executions.json`·`notebook-readiness.json`(Ch 28 다섯 — 06 없음) · `ch28-technical-review.md`·`ch28-before-path-repair/` · **Part 6 공용 `visual-results.json`**: Ch 28 줄은 마감에서 14줄로 새로 모음, 다른 챕터 줄은 옛 HTML 해시 그대로 — Part 6 마감 때 다시 모을 것. **`textbook/_notebook/build_index.py`** 절 수(Ch 28 5 — 실습 절 뺀 수) — 전체 목차 마감 때. Ch 21~27 요약의 「Ch 28 01 `a09d959cecc4…` 4셀」(옛 값 — 기록이라 그대로, 새 값은 계약 §5·이 문서 §12).
9. **과정 요약(누적 문서 몫)**: Ch 28 용어(§4 — 특히 「접근 토큰」·「도구 정의 몫」 ≠ 「늘어난 입력 토큰」·「도구 호출 요청」 한 뜻·「라이브러리 상태 형식」 = `AgentState`)·자식 프로세스·포트 정리 규칙(§8)·입력 토큰 결론 적용 선례(§7)·도구 파일 `connect_tools.py`(`570ed3cc…`, 함수 일곱)는 과정 요약에 아직 넣지 않음(Part 6 마감 오케스트레이터).
10. **옛 기록 파일**: `qa/research.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용 그대로 — 뒤 둘은 끝에 「마감」 절) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음) · `figures/0N-…prompt.md`(생성 기록 — 03-5 prompt에 몸체 자리 설명 없음, 그대로).
11. **실습 폴더 잠금**: `pyproject.toml`·`uv.lock` 그대로. `httpx`·`psutil`을 직접 의존에 올릴지는 강사 확인(§15-6).
12. **2차 검토**: 두 검토의 「확인하지 못한 것」과 §15-14.

## 19. 검토 1차와 반영 (2026-09-28 마감)

- 판정: **A(01~03·공통) 중 5 · 하 14**, **B(04~06·마감 몫) 중 3 · 하 10**. 합 **[중] 8 · [하] 24**, [상] 0.
- **[중] 8건 모두 반영**:
  - **A-7** 03 고정 포트 — 띄우기 전 포트 확인 셀(`HTTP_PLAN`)과 띄운 뒤 `poll() is None` 확인(`START_HTTP`), 본문·결과 읽기·b7을 실제 동작대로(**03 재실행**).
  - **A-8·B-12** 03 설치 셀 `langchain-core==1.6.2`(Ch 21 numpy 선례, **03 재실행**).
  - **A-9** 기기마다 다른 이름 수를 결론·그림 라벨·확인할 점·복습·정리에서 빼고 코드 출력도 고침(가짜 이름 `True`/`False`·읽은 값·「After보다 늘어난 이름 수: 1」), `LC_CTYPE`은 서버 쪽 Python이 만든 이름으로(**03 재실행** + 03-3 다시 렌더).
  - **A-15·B-13** 실습 폴더 README 전체 다시 씀(§13).
  - **A-16·B-13** zip을 마지막에 한 번 다시 만들고 묶음 실행 검사 PASS(Ch 28 01 `2407c4c57138…`이 `bundle-execution.json`에 적힘 — §12). B-13 (다) `objectives` 다섯.
  - **B-11** 05·06 판단 그대로 · 04 b6 표 입력 토큰 줄 분리(글만) · 05 핵심 개념 한정어 셋(B-4와 함께) — 강사 확인.
- **[하] 24건 모두 처리**(고침 22 · 기록만 2): A-1(01 「서버에」) · A-2(01 비유·b2) · A-3(01 셀 20·38 `extensions`·`logging`·UI 확장) · **A-4(01 설계표 차례 — 기록만)** · A-5(02 공개 문장, 코드 그대로) · A-6(02 Ch 19 01 7절 이음) · A-10(03 「접근 토큰」 넷, 03-4 다시 렌더) · A-11(03 b7 Tools 문서 허용·403) · A-12(03 HTTP 서버 `env` 좁힘 — 03 재실행) · A-13(03 b3 Ch 27 권한) · A-14(03 비유 몸체 자리) · A-17(`course_server.py` 문법 — 값 대조 뒤 고침) · **A-18(handoff 틀린 목록 두 곳에 「→ §03 → §04 9번에서 바로잡음」 — 기록 고침)** · A-19(pyc·옛 그림·objectives — 공개 목록 줄 빼고 삭제 승인 목록·objectives) · B-1(04 「도구를 부르는 요청」) · B-2(04 b7 행 번호·문서 예·9~12행) · B-3(04 셀 6·4·27) · B-4(05 한정어) · B-5(05 셀 47 백틱 값) · B-6(05 b10·06 b7 「토큰 한도에 닿으면」) · B-7(06 b7 04 합 430) · B-8(06 b6 표·b4) · B-9(06 셀 6) · B-10(06-1·06-3 색, 다시 렌더). 기록만으로 끝낸 것은 A-4(규격 차례 어긋남 — 되돌릴 수 없음)와 A-18(인계 문서 표시)뿐이고, 둘 다 권고가 「기록」이었음.
- **미반영 건**: 없음. 권고 가운데 택하지 않은 쪽 — A-5 (나)(Before에 독스트링을 두고 02 재실행 — 챕터 리드 결정대로 (가) 공개 문장, 02 코드·출력 그대로) · A-12 (나)(글만) 대신 (가)(코드) · A-9 「출력은 그대로 두고 글만」 대신 출력 줄을 없앰(03 재실행 묶음에 넣음 — 챕터 리드 결정).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자): 01 `2407c4c57138`/`32ff72d6ace0` 같음 · 02 `687062053d18`/`ba81122826a6` 같음 · **03 `04c437f720bc`/`2e1405dcafea` → `0935bc12bf4e`/`8bcb244ff474`**(A 23:43:29Z · B 23:44:09Z, 26/26 같음) · 04 `7bd03afa0ca1`/`2f63c7240617` 같음 · 05 `b99a57642e5d`/`a080eff183cf` 같음 · 06 `b36b5fc9b595`/`0190ea6d7d62` 같음. 다섯 노트북 `executed_at` 같음, `metadata.verification`과 다시 계산한 값이 같음.
- 고친 방법: `.cache/ch28-close/tools/gapply.py`(생성기 문자열 치환 — 치환 수가 다르면 멈춤, 바뀐 생성기를 실행해 **코드 셀이 노트북과 한 글자라도 다르면 멈추고**, 달라진 마크다운 셀만 노트북에 옮긴 뒤(첨부·메타데이터 그대로) `src_html()`로 `_src`) → `run_section.sh … NN --no-exec` · 03은 `/tmp/ch28-close/m03.py`(생성기 치환 35건, 수가 다르면 멈춤) → `author_03.py` 전체 → `execute.py` A → 사본 B(`--tools-copy`) → 셀별 대조 → `--no-exec` · `.mmd` 넷 `render_mermaid.py --only`(바뀐 것만) · `capsync.py`(캡션 파일 = 생성기 `FIGn_CAP`, 여섯 절 같음) · `chain28.py`(생성기 대조 사슬).
- 검사: `upgrade_gates.py … --label after` **6/6 PASS, G1~G7 0** · AST 따로 금지 문법 0(여섯 노트북·도구 파일·서버 파일 셋 — `course_server.py`의 f-string 둘·제너레이터 식 하나가 사라짐) · 호출 깊이 최대 2 · `verify.py --chapter` **PASS 6 sections / 152 code cells (max 16 lines)** · 빌드 HTML 일곱 `{{`·`[[` **0건** · `visual.cjs` **14행 PASS** · Part 6 `check_bundle_execution.py` **PASS** · Part 6 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(그 zip을 뺀 대조 통과) · 옛 검사 넷·과정 연속성 검사는 Ch 28 전에 멈춤(§12) · 금지어 전후 대조(`ban28.py`) 새 걸림은 거짓 양성뿐 · 보호 파일 226개 — `manifest-changes.md` 「마감 뒤」.

## 20. 절차 메모

- **01 그림 설계표를 렌더 뒤에 적음**(검토 A-4 — 01 진단 §9에 스스로 적음). 렌더 뒤 라벨·색 변경 0, 라벨 값은 A·B 출력과 맞음. 02·03·04·05·06은 렌더 전에 적었다고 진단에 적음(04·05·06은 설계표 파일에 렌더 결과를 덧붙여 수정 시각만으로는 확인할 수 없음 — 검토 B).
- **흔들림 확인 §0 작성 시각**: 04·05·06 모두 §0 시각이 첫 요청 기록(21:11:24Z·21:52:29Z·22:30:05Z)보다 앞선다고 적었고 검토 B가 대조. 05 §0 참고값 정정은 §1에 까닭과 함께.
- **날짜가 바뀐 뒤의 생성기 대조**: 마감 검사가 2026-09-29 UTC로 넘어가 `nbkit.RUN_DATE`가 바뀌었음 — 04~06 키 셀 결과 읽기의 실행일 문장만 생성기와 달라져, `UPGRADE_RUN_DATE=2026-09-28`로 대조(차이 0). 마감의 생성기 치환은 모두 날짜가 바뀌기 전에 끝나 노트북 글은 실행일 2026-09-28 그대로.
- 마감은 기기 셸 한 곳에서만 작업(`mcp__remote-devices__device_bash`), 셸 호출마다 `timeout` 170 안팎. 모델 요청 0 · 삽화 생성 0 · 파일 삭제 0 · 모든 파이썬 호출 `PYTHONDONTWRITEBYTECODE=1`(실습 폴더·`qa/` pyc 새로 0). 키 값은 출력하지 않음(`.env`를 열지 않음, 묶음 실행 검사는 키 환경 변수를 지우고).
