# 02절 진단과 개선 기록 — FastMCP 로컬 서버 제작 (paired)

- 작업일 2026-09-28 · 작업자: 02절 담당(모델 요청 **0**) · 생성기 `qa/upgrade/author_02.py`(`1c89a565…`, 설명 `mdpatch` 두 번 뒤 값) · 슬러그 그대로.
- 읽은 것: `handoff.md`(챕터 공통·§01→§02 전부) · `chapter-lead-notes.md`(전부) · `01-diagnosis.md`·`01-figures.md` · `author_01.py`(전부) · paired 본 Ch 24 `author_01.py`(머리·그림·`cells` 경계·`src_html`) · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md` 전부 · 과정 요약 전부(Ch 2 07·Ch 19 01·02·04·paired 선례) · Ch 2 07 `_src`(타입힌트는 값을 검사하지 않음) · Ch 19 01·02·03 `_src`(데코레이터 세 문장·입력 검사·몸통) · Ch 19 요약 §1·§13. 도구 파일 본 Ch 27 `author_02.py`는 이 절이 도구 파일을 만들지 않아 대조 사슬 모양만 확인했습니다. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 4 | 88 | 8 | 2 | 0(실제로는 넷 모두 틀 문장) | 0 | 6 | 25 | 3 | **44** |
| 첫 실행 전(`gates-wip-02-02.json`) | 24 | — | 0 | 0 | 0 | 0 | 0 | 11 → 0 | (그림 전) | — |
| 후(`gates-wip-02.json`, `--no-exec`) | **24** | **376** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 11건: 영문으로 시작해 조사가 붙은 문장 9(「After는」·「Before의」·「FastMCP가」 등 → 「After 도구는」·「서버 클래스 FastMCP가」) · 70자 넘는 문장 2. 실행 전에 고쳤습니다. 그림 뒤 G6 3건(그림 읽기 한 문장 · 도식 읽기 한 문장 · b7에 새로 쓴 「After의」)도 고쳤습니다.
- 코드 줄(`count_code.py`, 주석·빈 줄 뺌) **57 → 125**(코드 셀 4 → 24 — 옛 판은 셀 넷에 `async def` 셋·내포식·`next`·셀당 함수 둘로 몰아 적었음. 강사 확인 대상).
- AST 따로(`/tmp/ch28-02/tools/extra_check.py` — 01 판 + 02 허용 표시): 금지 문법 0건. 허용 표시 여섯 — 데코레이터 `@practice.tool`·`@before.tool`·`@after.tool`(서버 객체 메서드 줄, 첫 자리 설명 있음) · `async def call_tool_row` 하나 · 그 안의 `try`/`except ToolError` 하나 · 평범한 함수 `count_rules`의 독스트링(데코레이터 줄 하나만 다른 두 판을 만들려고 같은 독스트링을 둠). 매개변수 힌트는 After 도구의 `topic: str` 하나(챕터 공통 「MCP 도구 매개변수 힌트 예외」), 내놓는 값 힌트 0. 호출 깊이 최대 2(`depth.py`), 준비 셀 밖 셀 최대 9줄(After 거절 셀), 함수 본문 최대 7줄(`call_tool_row`), 셀당 정의 하나. f-string·내포식·`next`·`importlib`·클래스·`asyncio.run` 0.
- 금지어 검사(`/tmp/ch28-02/tools/ban28.py` — 01 판 그대로): 노트북 설명·주석·`_src`·캡션·`.mmd` 걸림은 「프로그램」 속 「로그」(거짓 양성)뿐. 「반환 힌트」 → 「내놓는 값 힌트」, 「기본 경로(A 트랙)」 → 「A 트랙」으로 고침. 「한 겹 더」 0.

## 2. 수정 전 주요 문제 (옛 판 — `qa/upgrade/before/`)

1. **틀린 사실 둘**: `_src` b5·b6 「call_tool은 **UnknownToolError**를 발생시킵니다」 — 설치판에는 그 이름이 없고 실제 오류는 `ToolError`(`fastmcp.exceptions`, 글 `Unknown tool: 'lookup_policy'`) · 「비교한 원인은 함수 등록 여부 하나입니다」 — Before 몸통 `{"대출": "14일"}[topic]`·독스트링 없음 ↔ After 몸통 글·독스트링이 달라 원인이 하나가 아님.
2. **paired Before가 약함**: 서버 객체와 상관없는 전역 함수 → 「아무것도 붙이지 않은 서버」와 같음(01 6절 빈 서버가 이미 보임).
3. b3 「Ch4에서 함수와 타입 힌트를」 → 타입힌트는 Ch 2 07 · 「장식자」 → Ch 19 말은 「데코레이터 줄」 · b10 FastMCP **v2** 문서 링크·확인 2026-09-11 · b7 「stdio에서 print가 프로토콜 메시지를 손상」(설치판에서는 호출이 성공하고 그 줄만 버려짐 — 준비 노트 §2 02, 이 절 범위 밖이라 뺌) · b8 세 항목이 다섯 절 같은 틀 문장.
4. 코드: `importlib`(실습 폴더에 pyc) · `next(… for …)`+별표 풀기 · f-string `assert` · 반환 힌트 튜플 · 내포식 · 셀당 함수 둘(c5·c7) · 첫 줄 주석 모두 옛 생성기 틀 문장 · 결과 읽기 0 · 준비물 없음.

## 3. 바꾼 것 — 노트북 차례 (코드 셀 24, 마크다운 29)

| 절 | lesson_part | 셀 | 하는 일 |
|---|---|---|---|
| 1 준비 | example | 1 설치(setup) · 2 가져오기(setup) · 3 기록기 수준 | `fastmcp==4.0.3`·`mcp==2.2.0`만. 가져오기 `logging`·`os`·`runpy`·`Client`·`FastMCP`·`ToolError`. 셀 3 `logging.getLogger("fastmcp").setLevel(logging.CRITICAL)` → `fastmcp 기록기의 수준: CRITICAL` |
| 2 서버를 만들고 도구 붙이기 | example | 4 규정 딕셔너리 둘 · 5 `practice = FastMCP("연습 자료실")` · 6 정의 `count_rules`(줄 없음) · 7 정의 `async def call_tool_row(server, tool_name, arguments)` · 8 목록 0·`Unknown tool: 'count_rules'` · 9 정의 `@practice.tool` + 같은 함수 · 10 목록 1·이름·설명·입력 형식 · 11 결과 `['2']`·`function`·`2` | **데코레이터 줄 하나만 다른 두 판**(옛 판 「원인 하나」를 참이 되게) · 데코레이터 세 문장 + Ch 2 09 · Ch 19 01 `@tool`과 같은 점·다른 점(이름에 함수가 남음 · 서버마다 따로) |
| 3 Before | before | 12 `before = FastMCP("힌트 없는 자료실")` + `body_inputs = []` + `@before.tool def lookup_policy(topic)` · 13 설명 `None`·`'topic': {}` · 14 `"대출"` → 결과·몸통 `['대출']` · 15 `3` → `Error calling tool 'lookup_policy': 3`·몸통 `[3]` | **실제 결함**(몸통까지 들어간 잘못된 값, 뜻 모를 글) |
| 4 After | after | 16 같은 몸통 + `topic: str` + 독스트링 · 17 `'topic': {'type': 'string'}`·설명 · 18 `3` → 줄 수 4·앞 세 줄·몸통 `[]` · 19 `"대출"` → Before와 같은 글 `True` | 몸통 전 입력 검사(Ch 19 02) |
| 5 값 바꿔 보기 | after | 20 `"주차"` 두 도구 → 둘 다 `'주차'`·몸통 `['주차', '주차']` | 힌트는 자료형만 — 허용 값은 몸통 몫 |
| 6 서버 파일의 붙이는 줄 | after | 21 파일 위치(01 셀 글 그대로 — 생성기가 `author_01.py`와 문자열 대조) · 22 `runpy.run_path` · 23 입력 형식·출력 형식·꼬리표 · 24 `"주차"` → `topic은 대출, 운영, 연체 중 하나여야 합니다.` | `@mcp.tool(tags=…)`·`@mcp.resource(...)`·`@mcp.prompt`·`-> str`·`mcp.run(...)` 한 문장씩 |

- 몸통에 들어왔는지는 노트북 전역 목록 `body_inputs`로 봅니다. 동기 도구는 FastMCP가 AnyIO 작업 스레드에서 돌리지만(`server.tool(..., run_in_thread=True)` 기본, 노트북 밖 `p3.py`에서 스레드 이름 `AnyIO worker thread` 확인) 같은 커널의 같은 목록에 적힙니다. 호출 셀마다 첫 줄에서 비움.
- 출력에 흔들리는 값 없음(ID·시각·메모리 주소·임시 폴더·포트 0). pydantic 안내 주소 줄(판 `2.13` 섞임)은 출력하지 않고 줄 수 `4`만. 셀 21 「고른 파일 위치」는 작업 폴더에 따라 다름(결과 읽기에 밝힘).

## 4. 챕터 리드 결정 적용

1. **paired Before = 실제 결함**: 힌트 없는 `@before.tool` → 입력 형식 `{'topic': {}}`·설명 `None` → `{"topic": 3}`이 몸통까지(`[3]`) → `ToolError: Error calling tool 'lookup_policy': 3`(**빨강은 이 결과만**) / After `topic: str` + 독스트링 → `1 validation error for call[lookup_policy]`·`topic`·`Input should be a valid string [type=string_type, input_value=3, input_type=int]`(노랑)·몸통 `[]`. 도구 이름·몸통 같음, 서버 이름만 다름. 입력 형식 비교를 결정적으로 출력(셀 13·17).
2. **서버 오류 기록**: `logging.getLogger("fastmcp").setLevel(logging.CRITICAL)`(셀 3). 노트북 밖 다시 잼(`/tmp/ch28-02/exp/p6.py`, 표준 오류를 파일로 — rich 폭 80칸): Before 잘못된 호출 하나 **27줄**(시각·파일 위치·`server.py:1541` 추적) · After 거절 하나 **경고 5줄**(`WARNING Invalid arguments for tool …`, `server.py:1505`) · 수준을 올리면 0줄. **01 인계의 「32줄」은 두 호출을 한 스크립트에서 부른 합**(27 + 5)이라 본문에는 나눠 적었습니다.
3. **모델 없음·메모리 연결·`runpy.run_path`**(pyc 0 — 실습 폴더 `__pycache__/course_server.cpython-312.pyc` 09-10 15:52 그대로).
4. **MCP 도구 매개변수 힌트 예외**: `topic: str` 하나, 내놓는 값 힌트 없음. 까닭 한 문장(4절 머리 — Ch 2 07 힌트·Ch 19 01 `@tool` 입력 형식과 이음). 서버 파일의 `-> str`은 6절 「서버 파일에 있는 줄」로 한 문장 + 출력 형식 출력(`x-fastmcp-wrap-result`).
5. **「FastMCP」 제목 그대로**, 1절·b2 첫 자리에서 「패키지 fastmcp와 그 안의 서버 클래스 이름」·「로컬 서버 = 같은 컴퓨터에서 도는 서버, 이 절은 같은 노트북 안」.
6. **비동기**: 01이 푼 셀 맨 위 `async with`·await + 이 절이 처음 쓰는 `async def` 하나(「함수 안에서 await를 쓰므로 Ch 2 12절처럼」 한 문장). `ainvoke`·`asyncio.run` 0.
7. **데코레이터 첫 자리**: 셀 9 앞 설명(「이 줄은 아래 함수를 서버 `practice`의 도구로 등록합니다」 + 뜻 → 일상 예 → 이 절 코드 + Ch 2 09·Ch 19 01) · 셀 12·16 뒤 「이 셀의 `@before.tool`/`@after.tool` 줄은 …」.
8. **도구 파일 만들지 않음**: 앞 챕터 함수·01 함수(`names_of`·`read_negotiation`·`compare_rows`·`change_flags`)를 쓰지 않음(도구 하나짜리 서버라 `tools[0].name`·`len`으로 충분). 이 절이 처음 가르친 `call_tool_row`를 03 이후가 다시 쓰면 그 절이 `connect_tools.py` 첫 판을 만듦(→ `handoff.md` §02→§03).
9. **용어**: 01 표 그대로 + 이 절 새 말 **4**(FastMCP 서버 클래스 · 도구 붙이기(등록) · 기록기·기록 수준 · 출력 형식). 이어 쓴 말: 데코레이터 줄(Ch 19) · 도구 몸통·입력 검사(Ch 19 02) · 입력 형식(Ch 19) · 연결·메모리 연결(01). 「스키마」·「반환」·「장식자」·「프로토콜」·「세션」·「리소스」·「로그」 본문 0.
10. **비유**: 「우주 정거장 도킹 포트」 — 벽판의 해치 둘(두꺼운 테두리 없는 둥근 구멍 ↔ 연파랑 네모 테두리) · 같은 주황 공 모양 모듈 둘(값 3). 01 소품(원통 정거장·고리 셋·우주선 둘) 되풀이 0.

## 5. 설치판·명세 확인 (2026-09-28, fastmcp 4.0.3·mcp 2.2.0·pydantic 2.13.5)

- 노트북 밖 탐색(`/tmp/ch28-02/exp/`, `PYTHONDONTWRITEBYTECODE=1`): `p1.py`(두 판 × 여덟 인자 — `3`·`"주차"`·`{}`·없는 키·목록·`3.0`·`True`) · `p2.py`(서버 파일 도구의 출력 형식·꼬리표·`"주차"` 글·메시지 틀 인자 `PromptArgument(name='topic', required=True)`·자료 설명, **`PYTHONHASHSEED` 0~3 네 번 모두 꼬리표 `['public', 'read']`**) · `p3.py`(줄 없는 판·붙인 판·스레드 이름) · `p4.py`·`p6.py`(표준 오류 줄 수) · `p5.py`(`call_tool_mcp`로 받은 결과 그대로 — 없는 도구·입력 검사·몸통 오류 **셋 모두 `isError: True` 결과**).
- **규격과 설치판 차이(b7에 적음)**: MCP 2026-07-28 Tools 문서는 없는 도구를 **통신 규약 오류**(JSON-RPC `-32602`)로 보낸다고 적지만, 설치판 서버는 `isError` 결과로 보냄 → 클라이언트는 `ToolError`. 입력 검사 오류는 규격대로 도구 실행 오류(`isError`) — 「모델이 고쳐 다시 보낼 수 있게」.
- WebFetch: `https://gofastmcp.com/servers/tools`(함수 이름 → 도구 이름·독스트링 → 설명·매개변수와 힌트 → 입력 형식 · 「validates these parameters against your function's signature」 · 반환 힌트 → 출력 형식·글 같은 값은 `result`로 감쌈 · 「you should use standard Python type annotations」 · 판 표시는 기능별 「New in version 2.x·3.x」뿐, 문서 판 번호 없음) · `https://modelcontextprotocol.io/specification/2026-07-28/server/tools`(`inputSchema`·`outputSchema` · 오류 두 종류 · 「Servers MUST: Validate all tool inputs」 · 매개변수 없는 도구 권장 `{"type": "object", "additionalProperties": false}` — 셀 10 출력과 맞음).
- 설치판 소스 행: `server/server.py` 1485~1489(없는 도구)·1491~1506(입력 검사 오류, 경고 기록)·1541~1555(몸통 오류 기록·글, `mask_error_details` 기본 거짓이라 오류 글이 붙음) · `tools/function_parsing.py` 304(독스트링)·338~340(입력 형식)·377~(반환 힌트 → 출력 형식)·494(`x-fastmcp-wrap-result`) · `server/providers/local_provider/decorators/tools.py` 317~321(함수에 `__fastmcp__` 표시를 달고 도구를 올린 뒤 **같은 함수를 내놓음**) · `client/mixins/tools.py` 368~373(`is_error`면 `ToolError(첫 글)`) · `server/server.py` 1851~1885(`tool` 데코레이터 부르는 모양 — 괄호 없이·이름·함수 직접).

## 6. 새 커널 두 번 · 프로세스

- **A(교재 출력)**: `run_section.sh … 02` → `PASS 02-FastMCP-로컬-서버-제작.ipynb: 24 cells`, `executed_at` 2026-09-28T20:07:54Z, `code_sha256` **`687062053d18b995c2744c9a216ced3d27c16e339007376e9cf0e9ad06b699b3`**, `outputs_sha256` `ba81122826a6…`. 표준 오류 흐름 0. 첫 실행은 그림 첨부 단계에서 멈춤(02-1 PNG가 아직 없음 — 의도한 차례, 실행 결과는 저장됨).
- **B(사본, 그림·삽화 전)**: `/tmp/ch28-02/B/` 20:08:13Z PASS 24셀 — 셀별 출력 글 **24/24 같음**(`cmpout.py`, 출력 글 연결 해시 A·B 모두 `f7014ba92af42934`). `outputs_sha256`만 `54276d33485c…`로 다름 — 설치 셀의 스트림 둘이 B에서 하나로 합쳐짐(글자는 같음, 01·Ch 24 선례).
- 그 뒤 노트북 코드는 바꾸지 않음(설명만 `mdpatch.py` 두 번 — `code_sha256` 그대로 확인). 서버 프로세스: 띄우지 않음(메모리 연결만) · 탐색 스크립트는 모두 끝남 · `pgrep -af course_server` 0.

## 7. 옛 원고의 틀린 사실과 고친 방식

| 옛 문장 | 사실 | 새 판 |
|---|---|---|
| b5·b6 「call_tool은 UnknownToolError를 발생시킵니다」 | 오류 종류 `ToolError`, 글 `Unknown tool: '…'` | 2절 셀 8 출력 + 결과 읽기 · b7 「받은 오류는 모두 `ToolError`」 |
| b5·b6 「비교한 원인은 함수 등록 여부 하나입니다」 | 몸통·독스트링도 달랐음 | 2절 — 몸통·독스트링 같고 **데코레이터 줄 하나만** 다른 두 판 · paired는 힌트·독스트링 한 묶음(몸통·이름 같음)이라고 b6에 |
| b3 「Ch4에서 함수와 타입 힌트」 | Ch 2 07(타입힌트는 값을 검사하지 않음) | b3 Ch 2 07 · 3절 머리 |
| b2·b3 「장식자(decorator)」 | Ch 19 말 「데코레이터 줄」 | 데코레이터 줄 |
| b4 「이 블록이 있어야 다른 클라이언트가 파일을 하위 프로세스로 실행할 수 있습니다」 | 이 절은 실행하지 않음 | 6절·b7 「이 절에서 실행하지 않았고, 03절」 |
| b7 「stdio에서 print가 프로토콜 메시지를 손상」 | 설치판에서는 호출 성공·그 줄만 버림(흔들림) | 뺌(이 절 범위 밖) |
| b10 FastMCP v2 문서 · 확인 2026-09-11 | 설치판 4.0.3 | FastMCP Tools 문서·MCP 2026-07-28 Tools · 확인 2026-09-28 · 소스 행 |

## 8. 그림 (Mermaid 4 + 삽화 1)

- 설계표 `02-figures.md`(**렌더 전에 적음** — 01의 [하] 기록과 달리 규격 §5-2 차례). 원본 viewBox 폭: 02-1 **275** · 02-2 **654** · 02-3 **646** · 02-4 **668**(모두 868 이하). PNG 넷 직접 확인(`.cache/ch28-02-view/`). 02-2 회색 상자가 「몸통 ·」 뒤에서 끊겨 `<br>`로 미리 나누고 다시 렌더(라벨 값 변경 0).
- 색: 초록 = 서버 객체·넣은 값 · 파랑 = 우리가 쓴 함수·데코레이터 줄·도구가 한 일 · 노랑 = 출력 값과 받은 오류(`Unknown tool`·After 거절·「주차」 글) · 회색 = 두 판·두 도구 공통 · **보라 0 · 빨강 1상자(02-3 Before 결과)**. 나란한 칸 둘은 좌우 배치(도식 읽기·alt에 「왼쪽 칸·오른쪽 칸」), 칸 안은 차례라 화살표, 02-1 도구 정의 세 칸은 `~~~`. 라벨 대괄호·따옴표·중괄호 0, subgraph 제목 `<br>` 0, 노드 id `call`·`end` 0, 노드 7개 이하(02-3 일곱). G7 라벨 숫자 0·1·2·3 출력에 있음.

## 9. 삽화 — 02-5 테두리 없는 해치와 네모 테두리 해치

- `generate_image` 두 번(재생성 1회), `params` `{"model":"nano_banana_pro",…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `jobs_wait` 모델 표시 `nano_banana_2`(기록만).
- **1차 job `79ce6b3a-9048-4f2b-b564-6a9413b2dd5d` 탈락**(거래 20:09:54.768060Z −2) — 두 공이 모두 구멍 가장자리에 반쯤 걸친 같은 자리라 「안까지 ↔ 앞에서 걸림」이 갈리지 않음. 원본 `3c6f6922…`.
- **2차 job `32561605-9da5-48e2-81fe-fba7c96d2130` 채택**(거래 20:10:56.320706Z −2). 원본 `58ac1e2c…`(2752 × 1536) → 폭 1100(LANCZOS) `c015d8b5…`(1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄인 그림과 저장 PNG 픽셀 대조: bbox `None`, 최대 차이 0. **크레딧: 생성 전 잔액 2319(바로 앞 거래 19:33:39Z는 01 몫) · 이 절 거래 두 줄 = 4크레딧 · 잔액 2315.**
- 저장 PNG 사본을 직접 열어 셈: 벽판 하나 · 해치 둘(왼쪽 가는 선만 둘린 크고 어두운 둥근 구멍 / 오른쪽 두꺼운 연파랑 네모 테두리와 작은 네모 구멍) · 주황 공 둘(왼쪽 구멍 안쪽 오른쪽 아래 / 오른쪽 테두리 앞, 구멍보다 큼). 글자·숫자·사람·화살표·별·고리·우주선 0.
- 그림과 비유의 차이: **왼쪽 공이 오른쪽 공보다 작게 그려짐**(프롬프트는 같은 크기) → 「작아서 들어갔다」로 읽힐 수 있어 그림 읽기에 「공의 크기와 해치의 크기는 어떤 값과도 짝짓지 않습니다」 · 왼쪽 구멍 둘레의 가는 선 → 본문 「두꺼운 테두리 없이」 · 벽판 좌우 흰 여백 조금(강사 확인).

## 10. 서버 파일·01·뒤 절 영향

- **`course_server.py` 고치지 않음**(`d7f7e8b9…` 그대로) → 01 출력·묶음 실행 검사 계약·zip·공개 목록 해시 영향 0. 01 노트북 다시 실행하지 않음(`code_sha256` `2407c4c57138…` 그대로).
- 01이 02에 기대는 문장: 「붙이는 줄(`@mcp.tool` 등)은 02절에서 배웁니다」 **참**(6절) · 「이 입력 형식은 … 힌트 `topic: str`에서 만들어졌고, 02절에서 자세히 봅니다」 **참**(4·6절) · 「도구를 붙이는 방법은 02절에서 배웁니다」 **참**(2절) · 01 b8·정리 「02절에서는 **서버 파일에** 도구를 붙이는 줄을 직접 씁니다」 — **부분 참**: 02는 서버 파일이 아니라 노트북의 서버 객체에 같은 줄을 씀(02 2절 머리 「서버 파일에 있던 붙이는 줄을 노트북에 직접 씁니다」로 이음). 01 두 곳을 「서버에 도구를 붙이는 줄」로 바꾸면 참(설명만 — `mdpatch.py`·`--no-exec`, 01 `code_sha256` 영향 없음) → **강사 확인·마감 몫**(이 절은 01을 고치지 않음).
- 03~05: 서버 파일 그대로라 영향 없음. 02가 새로 연 `call_tool_row`를 뒤 절이 쓰면 도구 파일 첫 판(인계).

## 11. 완료·대기 챕터 문장

- `grep -rn 'Ch *28' textbook/part6/ch29-*/_src textbook/part7`(`.json` 뺌) **0건** — Ch 29·Part 7 본문이 02에 기대는 문장 없음(Part 7 `qa/` 기록 파일 셋의 `ch28` 글자는 옛 기록).
- Ch 19 요약 §13 「Ch 28 02 b3 『Ch4에서 타입 힌트』 틀림·『장식자』 → 데코레이터 줄」 → **고침**(b3 Ch 2 07 · 데코레이터 줄). Ch 19 파일은 고치지 않음.

## 12. 챕터 밖 수정

- **없음**. 예외: `run_section.sh`의 `verify.py --chapter`가 `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json`을 다시 씀(선례와 같음).
- 실습 폴더(챕터 몫): 02 노트북만. `course_server.py`·README·잠금·도구 파일 그대로.

## 13. 보호 파일

- `before-manifest.json` 226개 대조 → `manifest-changes.md` 「02절 뒤」(바뀐 파일 목록·까닭). 없어진 것 0.

## 14. 남은 것 · 지우지 않은 것 · 강사 확인

- **지워야 하지만 지우지 않은 것**(삭제 승인 대상): `qa/upgrade/gates-wip-02-02.json`(첫 실행 전 게이트 — 라벨 `wip-02`) · `gates-wip-02.json` · 사용자 디스크 `.cache/ch28-02-view/`(그림 확인 사본 여섯, 약 1.9MB) · 기기 `/tmp/ch28-02/`(탐색 스크립트 `exp/`·사본 `B/`·삽화 원본 `illu/`·검사 도구 `tools/`·`reps*.json`) · 옛 그림 `figures/02-흐름.{svg,excalidraw,caption.md}`(본문 참조 0 — 챕터 공개 목록 줄 빼기는 마감) · 실습 폴더 옛 pyc(09-10, 01 기록과 같음).
- **강사 확인 대상**: 코드 줄 57 → 125·코드 셀 4 → 24 · 예시 부분의 데코레이터 줄 비교(평범한 함수에 독스트링을 둠) · `body_inputs` 목록(값이 몸통까지 왔는지 보려고 더한 줄) · 새 용어 4 · 01 b8·정리 「서버 파일에」(부분 참, §10) · 삽화 왼쪽 공 크기·여백 · 절 제목 영어 「FastMCP」(본문 첫 자리에서 풂).

## 마감 반영 (2026-09-28, 검토 1차 A-5·A-6)

- **다시 실행하지 않았습니다**(마크다운만). `code_sha256` `687062053d18…`·`outputs_sha256` `ba81122826a6…`·`executed_at` 20:07:54Z 그대로, 노트북 파일 `19d05788` → `46231dee`.
- **A-5**(한 조건 원칙 — 코드는 그대로, 공개): b6 첫 단락에 「이 가운데 값 3의 결과를 가른 것은 입력 형식의 `topic` 칸을 만든 힌트이고, 독스트링은 도구 설명만 바꿨습니다」(단락을 둘로 나눔) · 셀 40 결과 읽기 둘째 단락에 「두 판은 힌트와 독스트링이 함께 달랐지만, 거절을 가른 것은 입력 형식의 `topic` 칸입니다. 독스트링은 도구 설명만 바꿨습니다」. 근거는 3·4절 출력(입력 형식은 `topic` 칸만 다르고 `required`·`additionalProperties`는 같음). Before에도 같은 독스트링을 두고 힌트만 빼는 (나) 안은 02 재실행이라 하지 않음 — 강사 확인 대상.
- **A-6**: 셀 25(3절 머리)에 「Ch 19 01절 7절은 힌트를 빼면 입력 형식에서 자료형이 빠지는 것까지 보고, 잘못된 값은 넣어 보지 않았습니다. 이 절 3·4절이 그 값을 넣어 봅니다」(새 단락).
- 서버 파일 `course_server.py` 문법 고침(마감): 6절이 읽는 도구 입력 형식·출력 형식·꼬리표·「주차」 오류 글·메시지 틀 인자가 옛 판과 같음(`srvcmp.py`). 6절이 파일 줄을 읽는 곳은 데코레이터 줄과 `-> str`뿐이고 둘 다 그대로.
- 게이트 G1~G7 0.
