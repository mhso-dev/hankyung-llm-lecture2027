# 04절 진단과 개선 기록 — LangChain MCP 클라이언트 연동 (experiment)

- 작업일 2026-09-28 · 작업자: 04절 담당 · 생성기 `qa/upgrade/author_04.py`(`51958a06…`) · 흔들림 확인 `qa/upgrade/04-probe.md`·`probe/probe04.py`·`probe/probe-04-P.jsonl` · 슬러그 그대로.
- 읽은 것: `handoff.md`(챕터 공통·§03→§04 전부, 나머지 훑음) · `chapter-lead-notes.md`(§0·§1·§2 04·§6·§8·§9·§10-2·§11·§12) · `01~03-diagnosis.md`(03 전부) · `author_03.py`(전부)·`author_01.py`·`author_02.py`(셀 글·도우미) · Ch 27 `author_02.py`(대조 사슬·모델 셀)·`probe/probe02.py`·`02-probe.md` · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md` 전부 · 과정 요약 §1·§2-11~2-18·§3·§5·§6·§7·§8·§9 · Ch 20 01 노트북 코드(모양 선례) · Ch 21 `runner_tools.py`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 3 | 80 | 3 | 1 | 0(실제로는 셋 모두 틀 문장) | 0 | 5 | 29 | 3 | **41** |
| 첫 실행 전(`--label wip-04`) | 25 | — | 0 | 0 | 0 | 0 | 0 | 2 → 0 | 3(그림 전) | — |
| 후(`gates-wip-04.json`, `--no-exec`) | **25** | **400** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 2건: 영문으로 시작해 조사가 붙은 문장 둘(b4 「`ainvoke`는」 → 「메서드 `ainvoke`는」, 노트북 「langchain-core의」 → 「패키지 langchain-core의」). 실행 전에 고쳤습니다. **기록 파일 주의**: `gates-wip-04-04.json`은 첫 실행 전 값(G6 2·G7 3)을 담았다가, 그림 뒤 같은 이름으로 다시 돌려 지금은 0건 판입니다(첫 실행 전 값은 이 표에만 남음).
- 코드 줄(`count_code.py` — 주석·빈 줄 빼고 `%pip` 셈) **38 → 163**(코드 셀 3 → 25). 옛 판은 셀 셋에 변환·호출·비교를 몰아 적었고, 새 판은 변환 모양·부르기·자식 프로세스·도구 실행 노드·에이전트 실행을 셀마다 나눠 실행(강사 확인 대상). 도구 파일 `connect_tools.py` 코드 줄 48(03 판보다 함수 넷).
- AST 따로(`/tmp/ch28-04/tools/extra_check.py` — 03 판 + 도구 파일 `estimate_cost` `.get` 두 줄 허용 표시): 금지 문법 0건. 허용 표시 — 노트북 `try` 하나(`except NotImplementedError`, Ch 26 선례) · 도구 파일 `async def`·`try`(02 셀 글 그대로)·`estimate_cost`의 `.get` 둘(Ch 6 06·Ch 21 판 본문). 노트북 데코레이터·클래스·타입힌트 0. 호출 깊이 최대 2(`depth.py`), 준비 셀 밖 셀 최대 10줄(`AINVOKE`·`IN_BLOCK`·`COUNT`), 셀당 정의 0(노트북에 새 함수 없음). f-string·내포식·`next`·`importlib`·`asyncio.run`·`while` 0.
- 금지어 검사(`/tmp/ch28-04/tools/ban28.py` — 01 판 그대로): 노트북 설명·주석·`_src`·캡션·`.mmd` **0건**. 도구 파일은 Ch 21 판 글자 그대로 옮긴 주석의 「캐시 입력」 셋(Ch 6 06 말)과 변수 `total`만 걸림(옮긴 글이라 고치지 않음). 사용자가 금지한 표현 0. 「어댑터」는 클래스 이름 `MCPAdapter`로만, 「MessagesState」·「인터페이스」 본문 0.

## 2. 수정 전 주요 문제 (옛 판 — `qa/upgrade/before/`)

1. **모델·에이전트 없음**: 제목이 「연동」인데 변환한 도구를 `ainvoke`로 한 번 부르고, 직접 `@tool`과 `name`·`bool(args_schema)`만 견줌(`all(...)` — 만든 대로 늘 참). 에이전트에 붙이는 장면 0(03 b8 「에이전트에 붙여 봅니다」가 거짓이 될 자리).
2. **서버가 남음**: `MCPAdapter(Path(...))` → `keep_alive` 기본 `True`라 목록을 받은 뒤에도 자식 프로세스 하나가 남고, 시작 안내·새 판 확인(PyPI)이 표준 오류로(노트북 밖 `x3_block.py`로 다시 확인).
3. **흔들리는 출력**: 결과 출력에 실행마다 바뀌는 내용 블록 `id`(`lc_1fcdef69-…`)를 그대로 찍음.
4. **틀린·옛 문장**: b3 「BaseTool」(Ch 19는 이 이름을 안 씀 — 종류 `StructuredTool`) · b4 「커리큘럼의 langchain.mcp 표기는 확인 결과 유효합니다」(제작 이력) · 「반환 도구는 invoke나 ainvoke로 호출」(**`invoke`는 `NotImplementedError`**) · 「어댑터가 연결 수명과 도구 캐시 정책을 관리」(설치판은 부를 때마다 여닫음, 목록 캐시는 클라이언트에 줄 때만) · b10 스펙 2025-11-25·FastMCP v2 링크·확인 2026-09-11.
5. **문법·셀**: `next(… for …)`+별표 풀기·조건 표현식·`isinstance`·`.get`·반환 힌트 `tuple[list, dict, object]`·튜플 대입·한 셀 15줄·틀 문장 첫 줄 주석, 결과 읽기 0, 금지어(반환·인터페이스·스키마·프로토콜·측정·캐시·경로·인스턴스·인터셉터·사전).

## 3. 바꾼 것 — 노트북 차례 (코드 셀 25, 마크다운 29)

| 절 | 셀 | 하는 일 |
|---|---|---|
| 1 준비 | 1 설치(setup — 여덟 판, 잠금과 같음) · 2 가져오기(setup — `warnings.filterwarnings("ignore", category=LangChainBetaWarning)` 뒤 `langchain.mcp`, 도구 파일 함수 다섯) · 3 키(setup, nbkit) · 4 모델(nbkit, `temperature=0`·`reasoning_effort="none"`) | 베타 경고 줄에 커널 임시 파일 이름이 들어가 두 커널 대조를 깨므로 한 종류만 끔(노트북 밖 `nbtest.ipynb`로 확인) |
| 2 바꾸기 | 5 파일 위치(01 셀 글 그대로 — `author_01.FIND_FILE`) · 6 조용히 하는 세 이름(03 셀 글 그대로 — `author_03.QUIET`) · 7 `MCPAdapter(stdio_config(…)).list_tools()` → `['lookup_policy']`·자식 `0` · 8 종류 `StructuredTool`·설명·입력 형식 `dict`(01 4절 출력과 글자까지 같음) · 9 `content_and_artifact`·서버 정보·꼬리표 `['public', 'read']` | 모델 없음 |
| 3 부르기 | 10 `invoke` → `NotImplementedError`·`StructuredTool does not support sync invocation.` · 11 `ainvoke` → `list`·블록 1·키 `['type', 'text', 'id']`·글·자식 `0` · 12 `async with adapter:` 안 → `1`·`1`·같은 프로세스 `True`·블록 뒤 `0` | 블록 `id`·`pid` 값은 출력하지 않음(키 이름과 같은가만) |
| 4 도구 실행 노드 | 13 `StateGraph(MessagesState)` + `ToolNode(mcp_tools)` → `['tools']` · 14 손으로 만든 `AIMessage`(`call_a` 운영·`call_b` 주차) · 15 `await tool_graph.ainvoke` → `AIMessage`·`ToolMessage`·`ToolMessage`·자식 `0` · 16 `call_a success`·`call_b error`·서버 오류 글(02 6절과 같음) · 17 아티팩트 `{'structured_content': {'result': …}}`·`None` | Ch 20 01 모양. `MessagesState`는 과정 처음 — 「라이브러리 상태 형식」(Ch 21 03 말) + 칸 `messages` + Ch 13 04 `add_messages` 한 문장 |
| 5 에이전트(실제 모델) | 18 `ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")` · 19 `create_agent(model, tools=mcp_tools, system_prompt=agent_rule, middleware=[call_limit])` → 노드 여섯 · 20 `await mcp_agent.ainvoke` → 메시지 `4`·자식 `0` · 21 종류·도구 요청·결과 상태 · 22 도구 인자·도구 메시지 글 · 23 셈 `1`·`2`·`True` · 24 답 글 · 25 토큰·예상 비용 | 모델 요청 2번. `show_messages`는 쓰지 않음(도구 메시지 내용의 블록 `id`) — 같은 차례로 내용만 뺀 셀 |

## 4. 챕터 리드 결정 적용

1. **연결 방법 — 설치판 `langchain.mcp.MCPAdapter`**: 설치판 langchain 1.4.0에서 다시 확인(`adapter.py` 47~57 대상 종류에 `MCPConfig`·`dict` 있음, 84~122 글자 대상은 주소만). `langchain_mcp_adapters`는 `ModuleNotFoundError`(다시 확인). 03 설정 한 벌(`stdio_config` — `keep_alive: False` + FASTMCP 세 이름)을 그대로 넘김.
2. **공식 문서와의 차이(b7에 사실대로)**: LangChain MCP 문서(확인 2026-09-28)는 `MCPAdapter`를 권하고 예는 `Path("weather_server.py")`(「one subprocess per adapter」) → 이 절은 설정 딕셔너리(문서도 `MCPConfig` 대상을 적음, 예는 연결 안내 문서). `Path`로 넘기면 목록 뒤 자식 1이 남고 배너·새 판 확인이 찍힘(노트북 밖). 연결 안내 문서의 「each time a tool is invoked, it opens the client, runs the MCP call, and releases it」·「keep the adapter's context open … reuses the existing connection」은 3절 출력과 맞음. 옮기기 안내의 「isError=True → ToolMessage status='error'」도 4절 출력과 맞음. 문서 예의 모델 이름(Anthropic 문자열)은 쓰지 않고 과정 표준 모델 객체.
3. **앞 절반 모델 없음(결정적, 요청 0)**: 2~4절 모두 서버·도구가 주고받은 값. 모델 객체는 준비에서 만들기만 함.
4. **도구가 호출될 때마다 자식 프로세스가 끝나는지(03 인계 3번 — 이 절이 확인)**: 노트북 — 목록 뒤 `0`, 블록 밖 `ainvoke` 뒤 `0`(앞 셀까지 0이고 결과 글은 서버가 냄 → 호출 때 떠서 끝남), 블록 안에서는 같은 프로세스 `True`·블록 뒤 `0`, 그래프·에이전트 실행 뒤 `0`. 노트북 밖(`x1_shape.py`) — 블록 밖 호출 두 번 동안 자식 번호를 5ms마다 모으니 서로 다른 둘(부를 때마다 새 서버), 실행 뒤 0. 끝난 뒤 기기 `pgrep -af 'course_server|env_server|auth_server'` 0.
5. **뒤 절반 실제 모델 + 호출 한도 + 흔들림**: `04-probe.md` §0을 21:11:15Z에 적고(파일 수정 시각 같음) 첫 요청이 든 회차 1은 21:11:24Z 시작 — §0이 먼저. 다섯 번 모두 구조 값·모델 판단 값 같음(도구 `lookup_policy` 한 번·`success`·메시지 넷·요청 2·자식 0) → 입력 그대로. 흔들린 값은 답 글(한 번)·출력 토큰(32↔37)·예상 비용. `assert`는 파일 찾기 셀(01 셀 글)과 키 셀뿐.
6. **실행마다 다른 ID 빼기**: 내용 블록 `id`는 키 이름만(`['type', 'text', 'id']`), 글은 `text`·`.text`로만. 호출 ID는 손으로 정한 `call_a`·`call_b`만 출력(모델이 만든 호출 ID 0). `pid`는 같은가만.
7. **용어**: 01 표·금지어 그대로 + 새 말 넷(LangChain 도구로 바꾸기·비동기로 부르기 `ainvoke`·내용 블록·아티팩트, meta 「새 용어 4」). 이어 쓴 말: 도구 실행 노드·결과 상태·도구 속성 `handle_tool_error`(Ch 19 06 오류 담기 설정)·라이브러리 상태 형식(Ch 21 03)·호출 한도(Ch 22 04)·훅 노드(Ch 22 01)·자식 프로세스(Ch 23 04)·입력 형식(Ch 19).
8. **b3(새로)**: Ch 19 01(`@tool` 종류 `StructuredTool`, `invoke`)·02(`BaseModel`)·05(`ToolMessage`)·06(`handle_tool_error`·`error`) · Ch 20 01(손으로 만든 응답·`ToolNode`) · Ch 21 01(`create_agent` 모델 객체) · Ch 22 04 호출 한도(Ch 26·27이 늘 붙임) · Ch 27 02 셈 · Ch 2 12 · 01~03절. 옛 「BaseTool」 뺌. **b10(새로)**: LangChain MCP·Connections·옮기기 안내·FastMCP transports(확인 2026-09-28) + 설치판 소스 행.
9. **비유**: 「우주 정거장 도킹 포트」 — 둥근 구멍의 조종석 캡슐(에이전트)·한쪽 둥글고 한쪽 네모인 이음 부품(`MCPAdapter`)·네모 자리 짐 모듈(MCP 서버의 도구). 01~03 소품 되풀이 0(§9).

## 5. 설치판·명세 확인 (2026-09-28, langchain 1.4.0·langchain-core 1.6.2·langgraph 1.2.11·fastmcp 4.0.3·mcp 2.2.0·psutil 7.2.2)

- 노트북 밖 탐색(`/tmp/ch28-04/exp/`, `PYTHONDONTWRITEBYTECODE=1`, 키 없음·요청 0): `x1_shape.py`(가져오기 경고 한 번·`StructuredTool`·`args_schema` dict·`content_and_artifact`·`metadata`·`invoke` 오류·`ainvoke` 블록·자식 수·블록 안 재사용·도구 요청 모양 `ainvoke` → `ToolMessage`·`ToolNode` 그래프 success/error·동기 `graph.invoke` → `NotImplementedError`) · `nbtest.ipynb`+`run_nbtest.py`(베타 경고는 셀 표준 오류에 `…/ipykernel_9/342157256.py:2:` 줄로 찍힘 · 서버 오류 rich 기록은 셀 출력이 아니라 커널 쪽 표준 오류로 감) · `x2_agent_shape.py`(가짜 키 글, 요청 0 — 노드 여섯·호출 한도 속성·`bind_tools` 명세의 `parameters`가 서버 입력 형식 그대로) · `x3_block.py`(블록 안 세 번 모두 같은 프로세스 · `Path` 대상은 목록·호출 뒤 자식 1, 배너·`Update available: 4.0.10`·`INFO Starting MCP server` 표준 오류) · `x4_spec.py`(05 인계 참고 — MCP 도구의 `convert_to_openai_tool` 명세 JSON 글 252자).
- 소스 행: `langchain/mcp/__init__.py` 26~30(베타 경고 `warnings.warn`, `stacklevel=2`는 29행 — **마감 정정**: 절 작업 때 적은 「24~28」은 22~25행 설명 주석이 섞인 범위였음, 검토 B-2. 9~12행 독스트링도 같은 줄로 끄는 방법을 적음) · `adapter.py` 84~122·146~151·174~200·221~242(236~238 「tools stay callable after this adapter's context exits」) · `tools.py` 104~117(`_handle_mcp_tool_error`)·261~272(`async with client:` 부를 때마다)·274~282(`StructuredTool(… coroutine=…, response_format="content_and_artifact", handle_tool_error=…)`) · `elicitation.py` 312~375(`MCPAdapter`가 만든 클라이언트는 `session.call_tool` 경로 — 되묻는 요청이면 `interrupt()`) · langchain-core `messages/tool.py` 73~79(아티팩트 「not meant to be sent to the model」) · langchain `agents/middleware/model_call_limit.py` 213·253(비동기 훅) · fastmcp `server/server.py` 1541(`logger.exception` — 도구 오류 기록 ERROR 수준, `WARNING`으로 막히지 않음) · fastmcp `client/transports/stdio.py` 64~66(`keep_alive` 기본 `True`).
- WebFetch(확인 2026-09-28): `docs.langchain.com/oss/python/langchain/mcp` · `…/langchain/mcp/connections`(「One session per invocation」 절) · `…/migrate/langchain-mcp-adapters`(`MultiServerMCPClient` → `MCPAdapter`, `load_mcp_tools()` → `list_tools()`, interceptor → `@wrap_tool_call`, 프롬프트·리소스 안 감쌈, `handle_tool_errors` 인자 없어지고 isError는 늘 `status='error'`).

## 6. 흔들림 확인과 새 커널 두 번 · 프로세스

- **흔들림(노트북 밖 5번, `04-probe.md`)**: §0 21:11:15Z → 첫 요청이 든 회차 1 시작 21:11:24Z → 21:11:40Z 끝. 요청 10번, 서비스 오류 0. 구조 값·모델 판단 값 5/5 같음. 입력 토큰 430(187 + 243) 5/5 같음(04 결론에는 쓰지 않음 — 05 인계 참고).
- **A(교재 출력)**: `run_section.sh … 04` → `PASS 04-LangChain-MCP-클라이언트-연동.ipynb: 25 cells`, `executed_at` 2026-09-28T21:25:47Z, `code_sha256` **`7bd03afa0ca1c1395be1e4831265378ce11680a6e85ddbb8d536c0468f047bcb`**, `outputs_sha256` `2f63c724…`. 그림 첨부 단계에서 멈춤(04-1 PNG가 아직 없음 — 의도한 차례).
- **B(사본, 그림·삽화 전)**: `/tmp/ch28-04/B/`, `--tools-copy`로 디스크 도구 파일 복사(`cmp` 같음), `PYTHONPATH=/tmp/ch28-04/B` → 21:26:15Z PASS 25셀 — 셀별 출력 글 **25/25 같음**(`cmpout.py`, 출력 글 연결 해시 `75679231ce49c687` 둘 다) · 이번에는 `outputs_sha256`까지 `2f63c724…`로 같음(모델 답 글·토큰도 두 번 같았음).
- 그 뒤 코드는 바꾸지 않음(설명만 — 자리 표시 다섯 `mdpatch.py` 한 번, 그림 alt 한 곳·비유 단락 `--src-only`. `code_sha256` 그대로 확인). 서버 프로세스: 탐색·흔들림·A·B 모두 끝남 · `pgrep` 0. 노트북이 연결 폴더에 쓴 것: 커널이 도구 파일을 가져오며 다시 만든 `notebooks/__pycache__/connect_tools.cpython-312.pyc`(21:25, 도구 파일이 바뀌어 새로 씀).

## 7. 결정적 값과 흔들린 값의 자리

- **결론·그림 라벨·정리·복습(두 커널 같음 + 구조 값)**: `StructuredTool`·`dict`·`content_and_artifact`·꼬리표·`NotImplementedError`·자식 `0`/`1`·같은 프로세스 `True`·`call_a success`/`call_b error`·서버 오류 글·아티팩트·노드 이름·셈 「도구를 요청한 응답 수 + 1」 `True`.
- **모델 판단 값(5/5 + 두 커널 같음 → 한정어와 함께)**: 도구 `lookup_policy` 한 번 요청·결과 메시지 넷·요청 수 2 — 결과 읽기 첫 단락(출력 그대로)·b6 해석(「어느 도구를 몇 번 부를지는 모델이 고르는 값이라, 결론은 요청 수 셈」)·04-4 라벨(캡션·alt에 「에이전트가 MCP 도구를 한 번 부른 실행」).
- **흔들리는 값(둘째 단락·b6 표 맨 아래 줄·b7에만 「이번 실행에서는」)**: 도구 인자 `{'topic': '운영'}` · 도구 메시지 글 · 답 글 「토요일은 17:00까지 운영합니다」 · 입력 430·출력 32 토큰 · 예상 비용 0.000467달러.

## 8. 옛 원고의 틀린 사실과 고친 방식

| 옛 문장 | 사실 | 새 판 |
|---|---|---|
| b4 「반환 도구는 invoke나 ainvoke로 호출」 | `invoke`는 `NotImplementedError` | 3절 출력으로 보이고 「비동기로만 부르는 도구」 |
| b3 「Ch19에서 @tool로 만든 BaseTool」 | Ch 19 01 출력은 종류 `StructuredTool` | Ch 19 01의 `StructuredTool`과 같은 종류, 입력 형식은 딕셔너리 |
| b4 「연결 수명과 도구 캐시 정책은 어댑터가 관리」 | 도구는 부를 때마다 연결을 여닫음(`tools.py` 266행), 목록 캐시는 클라이언트 설정일 때만 | 「부를 때마다 여는 연결」 소제목·3절 출력 |
| `MCPAdapter(Path(...))` | `keep_alive` 기본 `True`라 자식이 남음 | 03 설정 딕셔너리(`keep_alive: False`), b7에 문서 예와의 차이 |
| 결과 출력 `'id': 'lc_…'` | 실행마다 바뀜 | 키 이름과 글만 |
| `assert all(has_schema …)` | 만든 대로 늘 참 | 뺌 |
| b4 「langchain.mcp 표기는 확인 결과 유효」 | 제작 이력 | 뺌(규격 §4) |
| b10 스펙 2025-11-25·FastMCP v2·확인 2026-09-11 | 현재 문서 | LangChain MCP 문서 셋·FastMCP transports·설치판 소스, 확인 2026-09-28 |

## 9. 그림 (Mermaid 4 + 삽화 1)

- 설계표 `04-figures.md`(렌더 전 21:27:20Z에 적음). 원본 viewBox 폭: 04-1 **371**(처음 276 — `tn ~~~ ag`가 두 끝 상자를 위아래로 쌓아, 빼서 나란히) · 04-2 **635** · 04-3 **464**(처음 301 — `ok ~~~ ng`도 같은 까닭으로 빼고 `ok ~~~ after0`·`ng ~~~ after0`) · 04-4 **861**(처음 931 → `width: 130`·`actorMargin: 40` init과 메시지 「ToolMessage success」·메모 세 줄로 줄임). PNG 넷 직접 확인(스테이징 사본).
- 색: 초록 = 서버 파일·서버 프로세스 · 파랑 = 설정·`MCPAdapter`·손으로 만든 응답·그래프·`ToolNode`·`create_agent` · 노랑 = 출력 값과 받은 오류(`NotImplementedError`·`status error`) · **보라 = 04-4 모델 띠 하나(`box Lavender`)** · 회색 = 04-4 세로선 머리(기본) · **빨강 0**. 갈래는 점선(04-1·04-2·04-3), 라벨 대괄호·따옴표 0, subgraph 제목 `<br>` 0, 노드 id `call`·`end` 0(`after0`), 노드 7개 이하.

## 10. 삽화 — 04-5 이음 부품으로 이은 모듈

- `generate_image` 두 번(재생성 1회 — 한도 안), `params` `{"model":"nano_banana_pro",…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `jobs_wait` 모델 표시 `nano_banana_2`(기록만).
- 1차 job `c08dddec-daf8-4af3-9e32-dbf61c45b3af` **탈락**(가운데 부품 양쪽 끝이 둥글어 「둥근 쪽 ↔ 네모 쪽」이 안 읽힘, 세 물건이 떨어져 있음) — 거래 21:29:23.737805Z −2.
- **2차 job `f18b3bd2-fb5a-462f-b93b-dbb7ed6f9834` 채택** — 거래 21:30:25.941493Z −2. 원본 `7ed2c5c5…`(2752 × 1536) → 폭 1100(LANCZOS) `57631b9e…`(1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄인 그림과 저장 PNG 픽셀 대조: bbox `None`, 최대 차이 0. **크레딧: 생성 전 바로 앞 거래 20:52:26Z는 03 몫(잔액 2313) · 이 절 거래 두 줄 = 4크레딧 · 잔액 조회 2309.**
- 저장 PNG 사본(`.cache/ch28-04-view/illu-2-1100.png`, `cmp` 같음)을 직접 열어 셈: 흰 캡슐 하나(둥근 창 하나, 둥근 끝이 왼쪽·넓은 둥근 구멍이 오른쪽) · 청록 부품 하나(왼쪽 절반 끝이 둥근 원통 — 캡슐 구멍 안, 오른쪽 절반 네모 덩어리) · 연노랑 짐 모듈 하나(모서리를 깎은 상자, 옆면 칸 둘, 왼쪽 끝에 네모 쪽이 꽂힘). 글자·숫자·사람·손·화살표·별·화면·전선·플러그 0.
- 그림과 비유의 차이(그림 읽기·`prompt.md`, 강사 확인): 모듈 쪽 네모 자리는 부품에 가려 테두리만 보이고 둥글게 보임 · 모듈 모서리가 깎여 팔각 기둥처럼 보일 수 있음(03 회색 팔각형 몸체와 색·쓰임 다름) · 부품이 고리가 아니라 덩어리라 본문을 「이음 부품」으로 바꾸고 파일 이름도 `mv -n`으로 바꿈(삭제 0) · 위아래 흰 여백 조금.

## 11. 도구 파일·서버 파일·앞 절 영향

- **도구 파일 `labs/part6/ch28-mcp/notebooks/connect_tools.py` 04 판** `cc066bd7fac0985313305fa6dfc9d3144cbd6c64f98ef2fd679b2c496b99edb3`(03 판 `9139c4f8…`에서):

| 함수 | 배운 곳 | 옮긴 것 | 가져오는 절 |
|---|---|---|---|
| `names_of(items)` | Ch 28 01절 4절 | 03 판 그대로 | 03·04 |
| `async def call_tool_row(server, tool_name, arguments)` | Ch 28 02절 2절 | 03 판 그대로 | 03 |
| `stdio_config(server_path, env)` | **Ch 28 03절 2절** | 03 노트북 셀 글 그대로(`author_03.DEF_CONFIG`, 디스크 03 노트북 코드 셀에 있음 확인·AST 같음) — 이 판에서 더함, 가져오기에 `import sys` | 04 |
| `tool_call_names(response)` | Ch 19 04절 | Ch 21 `runner_tools.py`(`f4113158…`) 설명 주석·본문 글자 그대로(Ch 27 `harness_tools.py` `7a40d994…` 판과도 같음) — 이 판에서 더함 | 04 |
| `sum_usage(messages)` | Ch 19 05절 | 같음 — 이 판에서 더함 | 04 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06절 | 같음 — 이 판에서 더함 | 04 |

  - **대조 사슬**: `author_04.py`가 `import author_03` → 03 판 해시 고정(`9139c4f8…`) · 머리 설명(`TOOLS_HEAD`)과 03 블록 둘 글자 그대로 · 가져오기 블록에만 `import sys` · `check_tools()`(함수 이름 차례 여섯·가져오기 셋·03 셀 글 디스크 대조·Ch 21·Ch 27 판 대조·AST) · 쓰기 가드 `write_tools()`(없거나 · 03 판이거나 · 이 판이면 씀, `later_version()` — 머리 설명으로 시작하고 04 블록을 모두 담은 긴 판 — 이면 건너뜀, 그 밖이면 멈춤) · `--tools-copy`는 디스크 판. **03 생성기 `later_version()`이 이 판을 「뒤 절 판」으로 봄**(확인 `True`) → 03을 다시 돌려도 덮어쓰지 않음.
  - `show_messages`(Ch 19 06)는 옮기지 않음 — MCP 도구 메시지 내용에 블록 `id`가 있어 5절은 내용을 뺀 셀을 따로 둠.
  - 공개 목록: 도구 파일 줄은 03이 이미 올림 → 04 목록 변경 없음. zip은 마감. 가져오는 노트북 설치 셀에 `fastmcp==4.0.3`(파일이 `Client`·`ToolError`를 가져옴) 있음.
- **서버 파일**: `course_server.py`(`d7f7e8b9…`)·`env_server.py`·`auth_server.py` 그대로. 04는 `course_server.py`만 씀(`env_server.py`의 `env_value`는 붙이지 않음). `auth_server.py`를 `MCPAdapter`에 넘기는 장면은 실행하지 않음(§03→§04 8번 — 05·마감 판단).
- **01·02·03**: 다시 실행하지 않음(01 `2407c4c57138…`·02 `687062053d18…`·03 `04c437f720bc…` 그대로). 03 노트북은 도구 파일 04 판에서도 `call_tool_row, names_of`를 그대로 가져옴(가져오기 줄 `import sys`만 더해짐 — 새 커널로 다시 돌리지는 않음). 03이 04에 기대는 문장 — 정리·b8 「04절에서는 서버의 MCP 도구를 LangChain 도구로 바꾸고, 에이전트에 붙여 봅니다」 **참**(2절 변환·5절 `create_agent`).

## 12. 뒤 챕터·완료 챕터 문장

- `grep -rn 'Ch *28' textbook/part6/ch29-*/_src textbook/part7`(지시 명령 그대로) **0건** — 뒤 챕터가 04에 기대는 문장 없음(03 기록과 같음). Part 7 `qa/` 기록의 「MCP」 글자는 옛 작업 메모(고치지 않음).
- 05 옛 b3 「앞 절에서 MCPAdapter가 MCP 도구를 BaseTool로 변환했습니다」 — 「BaseTool」은 틀림(`StructuredTool`), 05가 고칠 몫(§04→§05).

## 13. 서비스 요청·비용

- 노트북 한 번 **2번**(5절 에이전트 실행 — 도구를 한 번 부른 실행). 이번 작업 누계 **14번**: 흔들림 확인 10 + A 2 + B 2(탐색 스크립트 요청 0, 가짜 키 글 조립만). 예상 비용(요금표 2026-09-17 mini 0.75·0.075·4.50달러/100만 토큰, 청구 금액 아님, 노트북 셈): 흔들림 0.002357 + A 0.000467 + B 0.000467 = **약 0.0033달러**. 임베딩 0.

## 14. 남은 것 · 지우지 않은 것 · 강사 확인

- 생성기 `author_04.py` 최종 해시·보호 파일 대조는 `manifest-changes.md` 「04절 뒤」.
- **지워야 하지만 지우지 않은 것**(삭제 승인 대상): `labs/part6/ch28-mcp/notebooks/__pycache__/connect_tools.cpython-312.pyc`(A 실행이 다시 씀) · `qa/upgrade/gates-wip-04-04.json`·`gates-wip-04.json` · 사용자 디스크 `.cache/ch28-04-view/`(`illu-1-1100.png` 탈락본·`illu-2-1100.png` 채택본 사본) · 기기 `/tmp/ch28-04/`(탐색 `exp/`·사본 `B/`·삽화 원본 `illu/`·흔들림 원본 `probe/`·검사 도구 `tools/`·`reps1.json`) · 옛 그림 `figures/04-흐름.{svg,excalidraw,caption.md}`(본문 참조 0 — 챕터 공개 목록의 옛 SVG 줄 빼기는 마감).
- **강사 확인 대상**: 코드 줄 38 → 163·코드 셀 3 → 25 · 새 말 넷(바꾸기·비동기로 부르기·내용 블록·아티팩트) · `MessagesState` 과정 첫 사용(한 문장 — Ch 20·21은 안 씀) · `langchain_core._api`에서 경고 종류를 가져와 끄는 가져오기 줄(문서가 적은 방법, 모듈 이름에 밑줄) · 설치 셀 여덟(`langchain-core`·`langgraph`·`psutil`은 잠금의 간접 의존 — 직접 가져와서 적음) · `show_messages` 대신 내용을 뺀 셀(도구 파일 함수를 쓰지 않은 자리) · 삽화의 가려진 네모 자리·깎인 모서리 · 절 제목 영어 「LangChain MCP」(본문 첫 자리에서 풂).
- **마감 몫**: README 「03·04절은 로컬 stdio 하위 프로세스를 … 어댑터 컨텍스트가 끝날 때 종료」(설정에 따라 다름 — 04는 부를 때마다) · `chapter.json` 목표 「LangChain 1.4.0 MCPAdapter로 … 첫 호출 입력 토큰을 측정」(04·05 나눔) · 공개 목록 옛 SVG 줄.

## 마감 반영 (2026-09-28, 검토 1차 B-1~B-3·B-11)

- **다시 실행하지 않았습니다**(모델 절 — 마크다운만). `code_sha256` `7bd03afa0ca1…`·`outputs_sha256` `2f63c7240617…`·`executed_at` 21:25:47Z 그대로, 노트북 파일 `13b49a27` → `78cbb550`.
- **B-1**: b4 「서버에 도구 호출 요청을 보내는」·「도구 호출 요청 하나를」 → 「도구를 부르는 요청」(02 말 — 「도구 호출 요청」은 모델 응답의 `tool_calls` 한 뜻으로만).
- **B-2**: b7 「설치판 소스 `langchain/mcp/__init__.py` 24~28행」 → 26~30행 + 「같은 파일 9~12행의 설명도 이 가져오기 줄과 같은 줄로 끄는 방법을 적습니다」 · 문서 예 `Path("server.py")`·「서버 파일 하나에 자식 프로세스 하나」 → `Path("weather_server.py")`처럼·「어댑터 하나에 자식 프로세스 하나」(문서 원문 「one subprocess per adapter」). 생성기 머리 설명과 §5 행 번호도 고침.
- **B-3**: 셀 6 「5절에서 씁니다」 → 「4·5절에서 씁니다」(`tool_call_names`는 4절 셀 30에서 먼저 씀) · 셀 4·27의 「라이브러리 상태 형식 `MessagesState`」 → 「LangGraph가 미리 만들어 둔 `MessagesState`」 + 「Ch 21 03절의 `AgentState`보다 칸이 적어, 칸 `messages` 하나만 둔 형식입니다」(과정의 「라이브러리 상태 형식」은 Ch 21 03 `AgentState` 한 뜻). 셀 27은 단락을 나눔(G6).
- **B-11**(챕터 리드 결정 — 05·06 판단 그대로, 04는 같은 태도로 글만): b6 값 표에서 입력 토큰 줄을 떼어 「입력 토큰(실행 합) | `430` | 서비스가 센 값 — 노트북 밖 다섯 번·두 커널 같음, 이 절의 주제가 아니라 결론에 쓰지 않고 05절에서 조건을 바꿔 셈」 · 맨 아래 줄은 「도구 인자 · 답 글 · 출력 토큰 · 예상 비용」 · 표 아래 단락과 COST 결과 읽기 둘째 단락도 같은 뜻으로. 강사 확인 대상(Ch 26 04·Ch 27 03은 둘째 단락에 둔 선례와 갈림).
- 서버 파일 `course_server.py` 문법 고침(마감): stdio로 받은 도구 명세(252자)·`args_schema`·꼬리표·`ainvoke` 결과 글이 옛 판과 같음(`srvcmp.py`) — 04 출력은 바뀌지 않음.
- 게이트 G1~G7 0.
