# 03절 진단과 개선 기록 — stdio와 원격 전송·권한 경계 (paired)

- 작업일 2026-09-28 · 작업자: 03절 담당(모델 요청 **0**) · 생성기 `qa/upgrade/author_03.py`(`91b4a00b…`) · 슬러그 그대로.
- 읽은 것: `handoff.md`(챕터 공통·§02→§03 전부, 나머지 훑음) · `chapter-lead-notes.md`(전부) · `01-diagnosis.md`(훑음)·`02-diagnosis.md`(전부) · `author_02.py`(전부)·`author_01.py`(셀 글) · 도구 파일 본 Ch 27 `author_02.py`(대조 사슬 부분) · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md` 전부 · 과정 요약(§1·§2·§3·§5·§6 — Ch 16·19·22·23·27 줄) · 계약 §3 Ch27 줄 · Ch 27 요약 §16 · Ch 3 01·05·Ch 4 04·Ch 6 01·Ch 16 01·Ch 19 06·Ch 23 04·Ch 27 08 `_src`(b3 대조) · Ch 4 04·Ch 6 01·Ch 23 04 노트북(모양 선례). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 5 | 90 | 2 | 1 | 0(실제로는 다섯 모두 틀 문장) | 0 | 7 | 30 | 3 | **43** |
| 첫 실행 전(`gates-wip-03-03.json`) | 25 | 431 | 0 | 0 | 0 | 0 | 0 | 14 → 0 | (그림 전) | — |
| 후(`gates-wip-03.json`, `--no-exec`) | **25** | **456** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 14건: 70자 넘는 문장 8(b1 목표·b7·b10 참고 자료 넷·설치 셀 설명) · 영문으로 시작해 조사가 붙은 문장 6(「HTTP로 띄운」·「`블록 안에서…`과」·「FastMCP의」·「SDK가」·「SDK의」·「After의」). 실행 전에 모두 고쳤습니다. 과정 금지어 검사(`ban28.py`)에서 「안내 글」(Ch 27 05 뜻)·「확인해야」 두 곳도 고쳤습니다.
- 코드 줄(주석·빈 줄·`%pip` 뺌) **46 → 146**(코드 셀 5 → 25 — 옛 판은 셀 다섯에 stdio 호출만 몰아 적고, HTTP·권한은 실행하지 않는 설정 표였음. 이번 판은 stdio Before·After·값 바꿔 보기와 HTTP 인증·인가를 실제로 실행. 강사 확인 대상).
- AST 따로(`/tmp/ch28-03/tools/extra_check.py` — 02 판 + 03 허용 표시): 금지 문법 0건. 허용 표시 — 노트북 `while` 하나·`with socket.socket()` 하나(`wait_for_port`, Ch 23 04 `wait_for_signal` 모양) · `try` 하나(`except MCPError`, 접근 토큰 없는 연결 셀) · 도구 파일 `async def`·`try`(02 셀 글 그대로) · 서버 파일 데코레이터 셋(`@mcp.tool` 둘·`@mcp.tool(auth=require_scopes("admin"))`)과 `sorted(os.environ)`(키워드 없음). 매개변수 힌트는 서버 파일 도구의 `name: str`·`topic: str`·`text: str`뿐(챕터 공통 MCP 도구 예외), 내놓는 값 힌트 0. 호출 깊이 최대 2(`depth.py`), 준비 셀 밖 셀 최대 10줄(HTTP 서버 띄우는 셀), 함수 본문 최대 8줄(`wait_for_port`), 셀당 정의 하나. f-string·내포식·`next`·`importlib`·클래스·`asyncio.run`·노트북 데코레이터 0.
- 금지어 검사(`ban28.py` — 01 판 그대로): 노트북 설명·주석·`_src`·캡션·`.mmd`·서버 파일·도구 파일 걸림은 「프로그램」 속 「로그」(거짓 양성)뿐. 사용자가 금지한 표현 0. 「토큰」은 「접근 토큰」으로 한정(과정의 「토큰」 = 모델 입력 토큰과 겹치지 않게). **마감 정정**: 절 작업 뒤에도 b10 두 곳·03-4 칸 제목·그 alt 한 곳에 「토큰」 단독 넷이 남아 있었고(검토 A-10), 마감에서 모두 「접근 토큰」으로 고쳤습니다.

## 2. 수정 전 주요 문제 (옛 판 — `qa/upgrade/before/`)

1. **paired Before가 결함을 만들지 않음**: 옛 Before는 서버를 띄우지 않고 `dict(os.environ)`의 개수와 `OPENAI_API_KEY` 이름 포함 여부만 출력(`False` — 키를 읽지 않은 노트북이라). 개수(60)는 기기 값.
2. **틀린 사실**: After 설명 「PATH와 PYTHONUNBUFFERED **두 이름만** 전달」 — 서버는 SDK 기본 이름에 더해 받음(옛 설정이면 일곱). 옛 `assert "OPENAI_API_KEY" not in safe_env`·표 두 첫 칸 다름은 **만든 대로 늘 참**.
3. **실행 안 한 원격·권한**: HTTP·인증·인가는 튜플 두 줄 설정 표로만. b4 「Streamable HTTP … POST와 선택적인 GET」·세션은 옛 판(2025-11-25) 문장. b3 「Ch16에서 허용 목록과 최소 권한」 — Ch 16 원고에 「최소 권한」 0건. b8 「BaseTool로 변환」(Ch 19는 안 쓰는 이름). b10 스펙 2025-11-25·확인 2026-09-11.
4. **정리 문제**: stdio 기본 `keep_alive=True`로 블록 뒤 서버가 남음, 결과 출력에 실행마다 바뀌는 내용 블록 `id`(`lc_<uuid>`), 틀 문장 첫 줄 주석, 결과 읽기 0, `next`·별표 풀기·f-string·반환 힌트, 금지어(검증·사전·엔드포인트·바인딩·노출·배포·측정·경로).

## 3. 바꾼 것 — 노트북 차례 (코드 셀 25, 마크다운 30)

| 절 | lesson_part | 셀 | 하는 일 |
|---|---|---|---|
| 1 준비 | example | 1 설치(setup) · 2 가져오기(setup) | `fastmcp==4.0.3`·`mcp==2.2.0`·`httpx==0.28.1`·`psutil==7.2.2`(넷 모두 잠금 판 — httpx·psutil은 잠금의 간접 의존) · `from connect_tools import call_tool_row, names_of` + 고정 세 문장 + `PYTHONPATH` 한 문장 |
| 2 서버 파일을 자식 프로세스로 띄우기 | example | 3 파일 위치(01 셀 글 그대로 — `author_01.FIND_FILE`, 생성기가 문자열 대조) · 4 연습 서버 파일 둘 위치(`os.path.dirname`·`join`) · 5 조용히 하는 세 이름 · 6 정의 `stdio_config(server_path, env)` · 7 stdio 연결 → `['lookup_policy']`·자식 `1` → `0` · 8 `call_tool_row(설정, "lookup_policy", {"topic": "대출"})` → 01 4절과 같은 글·자식 `0` | 02가 실행하지 않고 넘긴 `mcp.run(transport="stdio")`를 실행. `if __name__ == "__main__":` 한 문장 |
| 3 Before | before | 9 가짜 이름·값(`CH28_DEMO_TOKEN = "교재용-가짜-값"`) · 10 `dict(os.environ)` + 세 이름 → 가짜 이름 `True` · 11 받지 못한 노트북 이름 수 `0` · 12 `env_value` → `['교재용-가짜-값']` | **실제 결함**(빨강은 이 결과만). Before 이름 목록은 출력하지 않음 |
| 4 After | after | 13 세 이름만 → `False`·`서버가 받은 이름 수: 10`·목록 · 14 `['없음']` | 목록 = 적은 셋 + SDK 기본 여섯 + `LC_CTYPE` |
| 5 값 바꿔 보기 | after | 15 세 이름 + 가짜 이름 하나 → `11`·`['교재용-가짜-값']` · 16 `del os.environ[fake_name]` → `False`·자식 `0` | 적은 이름만 더해짐. HTTP 서버를 띄우기 전에 가짜 이름을 지움(Popen은 환경을 통째로 넘김) |
| 6 HTTP로 띄운 서버와 인증 | after | 17 정의 `wait_for_port(port, limit_seconds)` · 18 `subprocess.Popen` → 준비 `True`·자식 `1` · 19 접근 토큰 없음 → `MCPError`·`Server returned an error response` · 20 `httpx.post` → `401`·`Bearer` | 127.0.0.1 고정 포트, 서버 기록 버림 |
| 7 접근 토큰의 범위와 인가 | after | 21 `StreamableHttpTransport(…, auth=…)` 둘 · 읽기 토큰 목록 `['lookup_policy']` · 22 쓰기 도구 → `ToolError`·`Unknown tool: 'update_policy'` · 읽기 결과 · 23 관리 토큰 목록 둘·쓰기 결과 `규정을 바꿨습니다: 운영` · 24 읽기 토큰이 바뀐 글(21:00) · 25 `terminate`·`wait` → `-15`·자식 `0`·포트 `False` | `call_tool_row`에 전송 객체를 넘김(재사용 두 번 이상 확인) |

- 출력에 흔들리는 값 없음(포트 번호·준비 시도 횟수·PID·시각·임시 폴더 이름 0). 셀 3 「고른 파일 위치」는 작업 폴더에 따라 다름(결과 읽기에 밝힘). 셀 13 목록은 기기에 따라 다를 수 있음(결과 읽기·b7에 밝힘).

## 4. 챕터 리드 결정 적용

1. **paired 설계 — (가) 중심 + (나) 이어 보이기(셀 25로 한도 안)**: 01 b4·b7·02 b4·b8이 「다른 프로그램이나 멀리 있는 서버에 붙는 장면」과 「누가 어떤 도구를 부를 수 있는지(인증·권한)」를 **둘 다 03으로** 넘겨, 하나만 하면 앞 절 문장이 거짓이 됨. 둘 다 노트북 밖에서 두 번 이상 결정적(`/tmp/ch28-03/exp/p1_stdio.py`·`p2_http.py`)이라 (가)를 Before·After·값 바꿔 보기로(3~5절), (나)를 after 부분의 권한 경계로(6·7절) 이음. (나)에는 결함 장면이 없어 빨강 0(받은 거절은 노랑).
2. **가짜 변수 정직성**: 이름·값 모두 노트북이 정한 교재용 글(준비물·셀 주석·결과 읽기에 공개). 루트 `.env`·키 셀 0, 실제 키 값·이름 출력 0(노트북·HTML·사본 B에서 `OPENAI`·`API_KEY`·`sk-` 0건 확인). Before 이름 목록은 출력하지 않고 참거짓·빠진 수만. After 목록은 기본 목록과 적은 이름뿐이라 출력.
3. **정리 규칙**: stdio 설정마다 `"keep_alive": False` + FASTMCP 세 이름(표준 오류 흐름 0 — A·B 모두 셀 출력에 stderr 0). HTTP는 `subprocess.Popen`(stdout·stderr 버림, `show_banner=False`라 새 판 확인 없음 — `fastmcp/utilities/cli.py` 201~205행이 시작 안내 안에서만 확인) → `terminate`·`wait` `-15`. 자식 프로세스 수를 노트북 출력으로 보임(psutil `0 → 1 → 0`, HTTP도 `1 → 0`). 끝난 뒤 기기 `pgrep -af 'course_server|env_server|auth_server'` 0·포트 58028 닫힘.
4. **하위 프로세스 기록**: 커널 `logging`이 닿지 않으므로 stdio는 `FASTMCP_LOG_LEVEL`, HTTP는 `DEVNULL`. 클라이언트 쪽(같은 커널) fastmcp 기록은 이번 셀들에서 0줄이라 02의 기록기 셀을 두지 않음.
5. **Ch 27 권한 규칙과 가르기**: b3 「Ch 27 08절의 권한 규칙은 Deep Agent의 파일 도구 안에서 판정했고, MCP 도구에는 걸리지 않습니다. 이 절의 권한은 MCP 서버가 접근 토큰을 보고 정하는 서버 쪽 경계입니다.」
6. **b3**: 「Ch16 최소 권한」 → Ch 16 01 출처 표시 허용 목록(After의 넘길 이름 목록과 모양이 같고 쓰임이 다르다고 한 문장) · Ch 19 06 `pick_tools`(클라이언트 쪽 거르기 ↔ 서버 쪽 인가) · Ch 3 01·05(`.env` 무시 규칙)·Ch 6 01(`load_dotenv`로 키가 노트북 환경 변수가 됨, 「환경 변수 전체를 출력해 문제를 찾지 않습니다」) · Ch 23 04(`Popen`·`kill`·`wait`, 「자식 프로세스」) · Ch 4 04(`httpx.get`·상태 코드) · 02 입력 검사 ↔ 03 인증·인가. 옛 「Ch24 사람 승인 경계」는 이번 본문이 쓰지 않아 뺌(참이지만 이 절 장면과 무관).
7. **stdio 제목 그대로**: 1절·b2 첫 자리에서 「표준 입력·출력(standard input/output)을 줄인 말」.
8. **서버 파일 자리 — 실습 폴더 맨 위에 두 파일**(`env_server.py` `8b4c40bc…`·`auth_server.py` `8f41e542…`): Ch 23 worker 둘(실습 폴더 맨 위) 선례. 노트북이 실행 때 만드는 자료가 아니라 학생이 여는 서버 스크립트이고, 셀에 문자열로 두면 셀 10줄을 넘으며 노트북이 파일을 쓰게 됨(이번 노트북 쓰기 0). `course_server.py`는 고치지 않음(`d7f7e8b9…` 그대로 — 01 묶음 계약·01 출력 인용·02 6절 영향 0). 두 파일은 도구 파일을 가져오지 않음. 생성기 `write_guarded`가 없거나 같을 때만 씀.
9. **도구 파일 `notebooks/connect_tools.py` 첫 판**(`9139c4f8410c8e799d838bbf0addb6ca42713869d7d51f6244eb41c6d96ef6e4`, 함수 둘·가져오기 둘) — 아래 §10.
10. **비유**: 「우주 정거장 도킹 포트」 — 가운데 몸체 · 짧은 통로 모듈(stdio)과 통로 속 상자(넘기는 환경 변수) · 긴 통로 끝 모듈의 닫힌 해치와 옆 초록 판(인증). 01·02 소품과 Ch 27 08 자물쇠 문·열쇠 되풀이 0.

## 5. 설치판·명세 확인 (2026-09-28, fastmcp 4.0.3·mcp 2.2.0·httpx 0.28.1·psutil 7.2.2·ipykernel 7.3.0)

- 노트북 밖 탐색(`/tmp/ch28-03/exp/`, `PYTHONDONTWRITEBYTECODE=1`): `p1_stdio.py`(course 서버 stdio·자식 1→0·env 서버 Before `True`·빠진 이름 0·가짜 값 / After `False`·아홉 이름 / 값 바꿔 보기 열 — **스크립트에는 `TERM`이 없어 노트북보다 하나 적음**, 표준 오류 0줄) · `p2_http.py`(토큰 없음·틀린 토큰 `MCPError`, 읽기 `['lookup_policy']`·`Unknown tool`, 관리 둘·쓰기 결과·바뀐 글, 전송 객체 재사용 두 번, `-15`·자식 0·포트 닫힘) · `p3_err.py`(`MCPError(-32603, 'Server returned an error response', None)`, 원인 칸 없음) · `p4_raw.py`(직접 POST: 토큰 없음 401·`Bearer`·본문 빈 글 / 틀린 토큰 401·`error="invalid_token"` 긴 설명 / 읽기 토큰은 헤더 없는 날 요청이라 400) · `p5_keep.py`(`keep_alive` 빼면 블록 뒤 자식 1이 남음 — 설정 딕셔너리로 새 `Client`를 세 번 열어도 1에서 더 쌓이지는 않음. 준비 노트 e9의 「1→2→3 쌓임」은 `MCPAdapter`로 본 값이라 본문에는 「하나가 남았다」까지만 적음).
- **`LC_CTYPE`의 출처**: `env -i PATH=/usr/bin python -c …` → `['LC_CTYPE', 'PATH']`, `PYTHONCOERCECLOCALE=0`이면 `LC_CTYPE` 없음, `LANG=C.UTF-8`이면 없음 → 문자 인코딩 이름이 없을 때 Python이 시작하며 만드는 이름(C 로케일 강제 변환). 노트북·교재 기기 커널은 `LANG`이 있지만 After 서버에는 넘어가지 않아 서버 쪽에서 생김.
- **`TERM`의 출처**: ipykernel 7.3.0 `zmqshell.py` 583~587행 `init_environment`가 커널 환경에 `TERM=xterm-color`(와 `CLICOLOR` 등)를 넣음 → 노트북에서는 SDK 기본 여섯이 모두 있어 After 열 이름.
- **인계 값 바로잡음**: 챕터 공통·§02→§03의 「SDK 기본 여섯 이름(`HOME·LC_CTYPE·LOGNAME·PATH·SHELL·USER`)」은 스크립트에서 서버가 **받은** 이름이었음. 설치판 mcp 2.2.0 `client/stdio.py` 40~57행의 기본 목록은 **`HOME·LOGNAME·PATH·SHELL·TERM·USER`**(Windows는 다른 열두 이름), 75~90행이 있는 것만 모으고, 128행 `get_default_environment() | (server.env or {})`가 더함 → §03→§04에 적음.
- 401 자리: 서버 fastmcp `server/auth/middleware.py` 81~83행(헤더 `Authorization` 없음 → `_send_missing_auth` 401·`Bearer`) · 클라이언트 mcp `client/streamable_http.py` 383~412행(400 이상·JSON-RPC 오류 본문 없음 → `INTERNAL_ERROR` `Server returned an error response`). 범위 부족: fastmcp `server/server.py` 905~914행(인가 실패 도구 → `None`, 「consistent with list filtering」) → `Unknown tool`. `StaticTokenVerifier` 경고 `server/auth/providers/jwt.py` 662행. `require_scopes` `utilities/authorization.py` 143행. `keep_alive` 기본 `client/transports/stdio.py` 64~66행·끊기 92~95행. `UvStdioTransport` 등이 `env_vars`를 주면 `os.environ.copy()` 486~492·553~556·615~618행.
- **규격과 설치판 차이(b7에 적음)**: MCP 인가 문서는 실행 중 범위 부족에 **403 + `insufficient_scope`**를 권함(SHOULD) ↔ 설치판 FastMCP는 도구를 목록에서 빼고 불러도 없는 도구(`Unknown tool`)로 대함(FastMCP 권한 문서 「hidden from list responses and direct access returns not-found」와 맞음).
- WebFetch(확인 2026-09-28): MCP 2026-07-28 `basic/transports`·`transports/stdio`(자식 프로세스·표준 출력은 MCP 메시지만·표준 오류 기록 허용·종료 절차) · `transports/streamable-http`(MCP 주소 하나·POST·GET 통로와 세션 없앰·`MCP-Protocol-Version`·`Mcp-Method`·`Mcp-Name`·Origin 403·127.0.0.1·인증) · `basic/authorization`(선택·HTTP는 따름·stdio는 환경에서 자격 정보·요청마다 `Authorization: Bearer`·틀린 토큰 401·범위 부족 403) · FastMCP `clients/transports`(작은 허용 목록 + `env` 더하기·`keep_alive` 기본 참 — 「MCPConfig」를 표준이라 부르지 않아 본문은 「FastMCP 설정 딕셔너리의 모양」) · `servers/authorization` · `servers/auth/token-verification`.

## 6. 새 커널 두 번 · 프로세스

- **A(교재 출력)**: `run_section.sh … 03` 두 번째 실행 → `PASS 03-stdio와-원격-전송-권한-경계.ipynb: 25 cells`, `executed_at` 2026-09-28T20:49:51Z, `code_sha256` **`04c437f720bc172fab27aa73a9e33448fadcae43246909ec0b0c06cc8ccd4ed0`**, `outputs_sha256` `2e1405dc…`. 첫 실행(20:48:37Z)도 PASS(같은 코드 — 설명의 이름 수를 고쳐 다시 씀). 그림 첨부 단계에서 멈춤(03-1 PNG가 아직 없음 — 의도한 차례).
- **B(사본, 그림·삽화 전)**: `/tmp/ch28-03/B/`, `--tools-copy`로 디스크 도구 파일 복사(`cmp` 같음), `PYTHONPATH=/tmp/ch28-03/B` → 20:50:12Z PASS 25셀 — 셀별 출력 글 **25/25 같음**(`cmpout.py`, 출력 글 연결 해시 A·B 모두 `2990776bc39697e8`). `outputs_sha256`만 `bea178c8…`로 다름(설치 셀 스트림 나뉨 — 01·02 선례).
- 그 뒤 코드는 바꾸지 않음(설명만 — 「오늘 볼 그림」 셀 alt·읽기를 `mdpatch.py` 한 번, `code_sha256` 그대로 확인). 서버 프로세스: 탐색 스크립트·A·B 모두 끝남 · `pgrep` 0 · 포트 58028 닫힘. 노트북이 연결 폴더에 쓴 것: 커널이 도구 파일을 가져오며 만든 `notebooks/__pycache__/connect_tools.cpython-312.pyc` 하나(§14).

## 7. 옛 원고의 틀린 사실과 고친 방식

| 옛 문장 | 사실 | 새 판 |
|---|---|---|
| Before 「전체 환경을 복사하므로 … 비밀 이름까지 포함될 수 있습니다」(서버를 띄우지 않고 `False` 출력) | 결함이 일어나지 않았음 | 가짜 이름·값을 넣고 실제로 서버를 띄워 `True`·가짜 값 읽힘 |
| After 「PATH와 PYTHONUNBUFFERED만 … env에 전달」 | SDK 기본 이름에 더해짐(옛 설정이면 일곱) | 4·5절 출력 — 세 이름만 적어도 열 이름, 하나 더 적으면 열하나 · b4·b6 「적은 이름만 기본 이름에 더해짐」 |
| `assert "OPENAI_API_KEY" not in safe_env` · 표 첫 칸 다름 | 만든 대로 늘 참 | 뺌 — `assert`는 파일을 찾았는가·서버가 포트를 열었는가 둘뿐 |
| b3 「Ch16에서 허용 목록과 최소 권한」 | Ch 16은 출처 표시 허용 목록, 「최소 권한」 0건 | Ch 16 01·Ch 19 06·Ch 27 08로 |
| b4 「하나의 MCP 엔드포인트에 HTTP POST와 선택적인 GET」 | 2025-11-25 문장 | 2026-07-28 — POST만·GET 통로와 `Mcp-Session-Id` 없앰·요청 헤더 셋 |
| 원격은 「실행하지 않는 설정 표」 | — | 127.0.0.1 HTTP 서버를 띄워 401·범위별 목록·호출을 출력 |
| b8 「LangChain BaseTool로 변환」 | Ch 19는 이 이름을 안 씀(종류 `StructuredTool`) | 「LangChain 도구로 바꾸고, 에이전트에 붙여 봅니다」 |
| b10 스펙 2025-11-25·FastMCP v2 링크·확인 2026-09-11 | 설치판 4.0.3·현재 판 2026-07-28 | MCP 2026-07-28 셋·FastMCP 문서 셋·소스 행, 확인 2026-09-28 |

## 8. 그림 (Mermaid 4 + 삽화 1)

- 설계표 `03-figures.md`(**렌더 전에 적음**). 원본 viewBox 폭: 03-1 **598**(처음 `flowchart TB`로 칸이 세로로 쌓여 311 × 973 → `flowchart LR` + 칸 안 `TB`로 나란히) · 03-2 **528** · 03-3 **613** · 03-4 **831**(처음 900 → 칸 제목·상자 글을 줄여 다시). PNG 넷 직접 확인(스테이징 사본). 03-3 회색 상자 「도구 env_names · env_value」가 가운데서 끊겨 `<br>`로 미리 나눔.
- 색: 초록 = 서버 프로세스·받은 값·HTTP 서버 · 파랑 = 설정·클라이언트 코드 · 노랑 = 출력 값과 받은 거절(`MCPError`·401·`Unknown tool`) · 회색 = 두 설정 공통·설치판 서버가 하는 일(인증과 인가) · **보라 0 · 빨강 1상자(03-3 Before 결과)**. 갈래는 점선(03-2 `call_tool_row`), 나란한 칸은 `~~~`, 라벨 대괄호·따옴표 0, subgraph 제목 `<br>` 0, 노드 id `call`·`end` 0, 노드 7개 이하. G7 라벨 숫자 `10`·`401`·`127.0.0.1`은 출력·본문에 있음. 03-4 「왼쪽·가운데·오른쪽 칸」은 칸 셋이 실제로 가로로 놓인 그림이라 그대로 씀.

## 9. 삽화 — 03-5 짧은 통로와 긴 통로

- `generate_image` 한 번(재생성 0), `params` `{"model":"nano_banana_pro",…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `jobs_wait` 모델 표시 `nano_banana_2`(기록만).
- **1차 job `fbf5ee68-4c2e-4961-a1dd-765567c3483f` 채택**(거래 2026-09-28T20:52:26.477598Z −2). 원본 `134bd016…`(2752 × 1536) → 폭 1100(LANCZOS) `5f1cb86b…`(1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄인 그림과 저장 PNG 픽셀 대조: bbox `None`, 최대 차이 0. **크레딧: 생성 전 바로 앞 거래 20:10:56Z는 02 몫 · 이 절 거래 한 줄 = 2크레딧 · 잔액 조회 2313.**
- 저장 PNG 사본을 직접 열어 셈: 회색 팔각형 몸체 하나 · 짧은 투명 통로로 붙은 흰 모듈 하나와 통로 속 파란 상자 둘 · 긴 투명 통로 끝 흰 모듈 하나 · 닫힌 둥근 해치 하나 · 초록 네모 판 하나. 글자·숫자·사람·화살표·별·자물쇠·열쇠·고리·우주선 0.
- 그림과 비유의 차이(그림 읽기·`prompt.md`에 적음, 강사 확인): 닫힌 해치가 통로 끝 안쪽에 작게 그려져 눈에 덜 띔 · 몸체가 팔각형이고 두께가 있어 너트처럼 보일 수 있음 · 위아래 흰 여백 조금 · 상자 수·통로 길이는 어떤 값과도 짝짓지 않음.

## 10. 서버 파일·도구 파일·01·02·뒤 절 영향

- **도구 파일 `labs/part6/ch28-mcp/notebooks/connect_tools.py` 첫 판** `9139c4f8410c8e799d838bbf0addb6ca42713869d7d51f6244eb41c6d96ef6e4`:

| 함수 | 배운 곳 | 옮긴 것 | 가져오는 절 |
|---|---|---|---|
| `names_of(items)` | Ch 28 01절 4절 | 01 노트북 셀의 주석·본문 글자 그대로(`author_01.DEF_NAMES`, 셀 글 해시 `e82a3d82…` 고정) | 03 |
| `async def call_tool_row(server, tool_name, arguments)` | Ch 28 02절 2절 | 02 노트북 셀의 주석·본문 글자 그대로(`author_02.DEF_CALL`, `06e71031…` 고정) — 서버 객체·MCP 설정 딕셔너리·전송 객체 모두 받음(이번에 실행으로 확인) | 03 |

  - 가져오기 줄 `from fastmcp import Client`·`from fastmcp.exceptions import ToolError` → 가져오는 노트북 설치 셀에 `fastmcp==4.0.3`. 첫 줄 「앞 챕터와 이 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다」.
  - **생성기 대조 사슬(첫 판부터)**: `TOOLS_HEAD` + `TOOLS_IMPORTS` + 셀 글 블록 둘 · `check_tools()`(함수 이름 차례·가져오기 둘·셀 글 해시 고정·디스크 01·02 노트북 코드 셀에 그 글이 있는지·AST 대조) · **쓰기 가드** `write_tools()`(없거나 `== TOOLS`면 씀, `later_version()` — 머리 설명으로 시작하고 이 판의 함수 블록을 모두 담은 뒤 절 판 — 이면 건너뜀, 둘 다 아니면 멈춤) · `--tools-copy DIR`은 **디스크 판** 복사.
  - **묶음 목록**: 챕터 `qa/public-files.json`에 세 줄(`env_server.py`·`auth_server.py`·`notebooks/connect_tools.py`) → `python3 -B textbook/part6/qa/collect_public_files.py` → Part 목록 `textbook/part6/public-files.json` `e43894fa…`(02 뒤까지 그대로) → `7b66b4f9…`(차이는 세 줄뿐, 선행 목록 바이트 같음). **zip은 마감에서**.
- **01**: 도구 파일을 가져오지 않음(묶음 계약 그대로), 다시 실행하지 않음(`code_sha256` `2407c4c57138…` 그대로). 01이 03에 기대는 문장 — 「다른 프로그램이나 멀리 있는 서버에 붙는 장면은 03절」·「권한은 03절」·「누가 어떤 도구를 부를 수 있는지는 03절의 인증·권한 몫」 **모두 참**.
- **02**: 다시 실행하지 않음(`687062053d18…` 그대로, 02는 `call_tool_row`를 자기 셀에 둔 채). 02가 03에 기대는 문장 — b7 「`mcp.run(transport="stdio")` … 다른 프로그램으로 띄우는 장면은 03절」·정리·b8 「서버를 다른 프로그램으로 띄워 연결 … 넘기는 값과 권한의 경계」 **참**(2·3~5·6~7절). 02 b4 「누가 어떤 도구를 부를 수 있는지는 03절」도 참.
- **04·05**: 서버 파일 `course_server.py` 그대로라 옛 판 영향 없음. 04가 `stdio_config`를 다시 쓰면 도구 파일에 더함(§03→§04).

## 11. 완료·대기 챕터 문장

- `grep -rn 'Ch *28' textbook/part6/ch29-*/_src textbook/part7`(지시 명령 그대로) **0건** — Ch 29·Part 7 본문·기록이 03에 기대는 문장 없음. Part 7 Ch 30 07 「인증·CORS·타임아웃」은 Ch 28을 가리키지 않고 인증(「요청 주체를 확인」, Bearer 헤더)을 스스로 다시 풂 — 03의 인증 정의와 뜻이 같아 어긋남 없음(고치지 않음, 기록만). Part 7 `qa/` 기록 셋의 「MCP」 글자는 옛 작업 메모.
- 계약 §3 Ch27 줄 「권한 규칙은 파일 도구 안 판정 — MCP 도구에 걸린다고 가정 금지」 → b3에서 그대로 가름(참).

## 12. 챕터 밖 수정

- `textbook/part6/public-files.json`(`collect_public_files.py`가 다시 씀 — 03 줄 셋 더함, 선례: Ch 27 02 도구 파일) · `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json`(`run_section.sh`의 `verify.py --chapter`가 다시 씀 — 선례와 같음). 그 밖 0.
- 실습 폴더(챕터 몫): 03 노트북 · 새 파일 셋(`env_server.py`·`auth_server.py`·`notebooks/connect_tools.py`) · `notebooks/__pycache__/connect_tools.cpython-312.pyc`(커널 가져오기). `course_server.py`·README·잠금 그대로.

## 13. 보호 파일

- `before-manifest.json` 226개 대조 → `manifest-changes.md` 「03절 뒤」. 바뀐 것 16(02 뒤 11 + 03 5), 없어진 것 0.

## 14. 남은 것 · 지우지 않은 것 · 강사 확인

- **지워야 하지만 지우지 않은 것**(삭제 승인 대상): `labs/part6/ch28-mcp/notebooks/__pycache__/connect_tools.cpython-312.pyc`(A 실행이 만듦 — 연결 폴더, 공개 목록 밖) · `qa/upgrade/gates-wip-03-03.json`·`gates-wip-03.json` · 사용자 디스크 `.cache/ch28-03-view/illu-1-1100.png`(그림 확인 사본) · 기기 `/tmp/ch28-03/`(탐색 스크립트 `exp/`·사본 `B/`·삽화 원본 `illu/`·검사 도구 `tools/`·`reps1.json`·공개 목록 전 사본 둘) · 옛 그림 `figures/03-흐름.{svg,excalidraw,caption.md}`(본문 참조 0 — 챕터 공개 목록의 옛 SVG 줄 빼기는 마감).
- **강사 확인 대상**: 코드 줄 46 → 146·코드 셀 5 → 25(원격·권한을 실제로 실행) · 서버 파일 둘을 실습 폴더 맨 위에 둔 결정(학생 묶음에 두 파일 더함) · 연습 서버의 `env_value` 도구(값을 보여 주려고 둔 도구 — 파일 머리에 「실제 서버에는 두지 않음」) · HTTP 고정 포트 58028(**마감 정정**: 절 작업 때 적은 「다른 프로그램이 쓰면 셀 멈춤」은 사실과 달랐음 — 포트가 이미 쓰이면 준비 확인이 곧바로 참이 되어 셀이 지나가고 앞 프로그램과 이야기함, 검토 A-7. 마감 재실행에서 띄우기 전 포트 확인과 띄운 뒤 `poll()` 확인을 더해, 이제는 포트가 쓰이면 셀이 멈춤) · %pip에 httpx·psutil(잠금의 간접 의존) · 새 용어 6(전송·환경 변수·인증·인가·접근 토큰·범위)과 이어 쓴 「자식 프로세스」(인계의 「하위 프로세스」 대신 Ch 23 04 말 — 과정 요약 §5 「여기 없는 말을 새로 만들지 않음」) · 「토큰」을 모두 「접근 토큰」으로 · 삽화의 작은 해치·팔각형 몸체 · 절 제목 영어 「stdio」(본문 첫 자리에서 풂).
- **마감 몫**: 공개 목록 → `part6-practice.zip`(새 파일 셋 포함) → `check_bundle_execution.py`(01만 검사 — 03 파일은 01이 읽지 않음) · README(「03·04절은 로컬 stdio 하위 프로세스를 … 어댑터 컨텍스트가 끝날 때 종료」·학생 배포 파일 목록에 새 파일 셋·「실패 진단 JSON」) · `chapter.json` 목표 「로컬·원격 전송의 인증과 최소 권한 경계」(본문은 「권한 경계」 — 「최소 권한」은 규격 인가 문서의 범위 선택 원칙 말로만 참).

## 마감 반영 (2026-09-28, 검토 1차 A-7~A-14·B-12 — **03 다시 실행**)

- **다시 실행한 까닭**: A-8·B-12(설치 셀에 도구 파일이 가져오는 `langchain-core`가 없음 — 규격 §2-7 6번, Ch 21 numpy 선례) · A-7(고정 포트가 이미 쓰이면 셀이 멈추지 않고 앞 프로그램과 이야기함) · A-9(기기마다 다른 이름 수 출력) · A-12(HTTP 서버를 노트북 환경 통째로 띄움). 모두 모델 요청 0·결정적. 01 묶음 계약에 닿지 않음.
- **코드 고침**(`author_03.py` 문자열): 설치 셀 `"langchain-core==1.6.2"` 더함(판 출력 한 줄) · 가져오기 `from mcp.client.stdio import get_default_environment`(준비 셀) · After 셀에서 `서버가 받은 이름 수` 줄을 빼고 목록 라벨을 `서버 프로세스의 환경 변수 이름:`으로(`LC_CTYPE`은 받은 이름이 아니라 서버 쪽 Python이 만든 이름) · 값 바꿔 보기 셀은 이름 수 대신 `서버가 받은 이름에 가짜 이름이 있는가: True`·`After보다 늘어난 이름 수: 1`(같은 기기에서 두 설정의 목록을 견준 차 — 기기와 상관없이 1) · HTTP 띄우기를 **두 셀로**: `HTTP_PLAN`(주소·명령·`http_env = get_default_environment()` + 조용히 하는 세 이름 · 띄우기 전 `wait_for_port(auth_port, check_limit)`이 거짓인지 `assert`, 9줄) → `START_HTTP`(`Popen(command, env=http_env, …)` · 준비 확인 뒤 `auth_process.poll() is None`을 함께 `assert`, 10줄) · 마지막 셀의 겹친 `check_limit = 1` 줄 뺌. 코드 셀 25 → **26**, 셀 55 → 57, 코드 줄 147 → **158**(`count_code.py` — 절 작업 기록의 146은 셈 방식 차이), 함수 본문 한도·셀 10줄·호출 깊이 2 지킴.
- **새 커널 두 번**: A(`execute.py`, 23:43:29Z) · B(사본 `/tmp/ch28-close/B03` + `author_03.py --tools-copy` — 도구 파일 05 판 `570ed3cc…`, 23:44:09Z) 셀별 출력 **26/26 같음**, `outputs_sha256`도 같음. 새 `code_sha256` **`0935bc12bf4e11a50469785ccfdb59ef63db16a32a341d2869c87412019ba258`** · `outputs_sha256` **`8bcb244ff474652b3ba7c7c79cb785b901fc2f8e5c40c6748483618109b6efde`**(옛 `04c437f720bc…`·`2e1405dcafea…`). 노트북 파일 → `c1f22daa`. 끝난 뒤 서버·커널 프로세스 0, 포트 닫힘, 실습 폴더 pyc 새로 생기지 않음(`PYTHONDONTWRITEBYTECODE=1`).
- **바뀐 출력과 인용**: 설치 셀 `langchain-core: 1.6.2` · After `서버 프로세스의 환경 변수 이름:` 아래 목록(열 이름 — 옛 출력과 같은 목록) · 값 바꿔 보기 세 줄 · `띄우기 전에 이 포트에서 듣는 프로그램이 있는가: False` · `띄운 서버가 살아 있는가: True`. 그대로인 값: 2절 자식 1·0·대출 결과 글, Before `True`·`0`·`['교재용-가짜-값']`, After `False`·`['없음']`, `MCPError`·`Server returned an error response`·`401`·`Bearer`·`['lookup_policy']`·`Unknown tool: 'update_policy'`·관리 토큰 둘·`-15`·자식 0·포트 닫힘. 이 값을 인용한 본문·그림·캡션·정리·복습을 모두 다시 대조함(`서버가 받은 이름 수`·「열 이름」·「열한」 0건).
- **A-9 글**: 결론·그림 라벨·확인할 점·복습·정리에서 이름 수를 뺌 — 03-3 After 라벨 「받은 이름 수 10」 → 「적은 세 이름과 기본 이름」(다시 렌더), 확인할 점 → `After보다 늘어난 이름 수: 1`, 복습 3(「왜 적지 않은 이름도 있었나요?」 — 교재 출력 Linux 커널·Windows 목록 다름·`LC_CTYPE`), 정리 2(노트북·b8) → 「세 이름만 넘긴 서버는 가짜 이름을 받지 않았습니다」, b6 비교 표·둘째 단락, b7 첫 항목에 Windows 기본 목록 열둘(`APPDATA`·`SYSTEMROOT` 등 — 설치판 mcp 2.2.0 `client/stdio.py` 40~57행).
- **A-7 글**: 6절 설명(대기 함수는 누가 듣는지 가리지 않음 · 다른 프로그램이 쥐면 새 서버는 포트를 못 열고 앞 프로그램이 답함) · 두 셀의 결과 읽기(이 셀만 두 번 실행하면 앞 서버가 남고 `auth_process`는 끝난 서버를 가리킴 → 마지막 셀로 끈 뒤 앞 셀부터, 끄지 못했으면 커널 다시 시작) · b7 포트 항목. 커널을 다시 시작했을 때 남은 서버가 함께 끝나는지는 실행하지 않았고, 남았으면 앞 셀의 확인이 멈춰 포트 번호를 바꾸라고 알림.
- **A-12**: b7 「이 절은 HTTP 서버에도 SDK 기본 이름과 조용히 하는 세 이름만 넘겼습니다」(`client/stdio.py` 75~90행 `get_default_environment`).
- **A-10**: b10 「틀린 접근 토큰」·「접근 토큰을 글 그대로」 · 03-4 칸 제목 「접근 토큰 없음」(다시 렌더)·그 alt. 서버 파일 `auth_server.py` 머리 설명의 「관리 범위가 있는 토큰에만」·주석 「토큰마다」는 서버 파일이라 그대로(해시 `8f41e542…`, 앞 줄이 「접근 토큰」을 먼저 밝힘).
- **A-11**: b7 「접근 토큰의 범위에 따라 도구 목록을 다르게 내놓는 것은 규격 Tools 문서가 허용합니다. 숨긴 도구를 부를 때 MCP 인가 문서는 상태 코드 403을 권합니다. 설치판 FastMCP는 없는 도구와 같은 글을 보냈습니다」.
- **A-13**: b3 「Ch 27 08절의 권한 규칙은 Deep Agent의 파일 도구 안에서만 판정했고, 우리가 만든 도구에는 걸리지 않았습니다. 그래서 MCP 도구에도 걸린다고 보지 않고, 이 챕터에서는 그 조합을 실행하지 않았습니다」.
- **A-14**: b4 비유 둘째 단락 끝 「가운데 몸체는 서버를 띄우고 값을 넘기는 노트북(클라이언트) 자리라, 01절 비유에서 서버였던 정거장과는 자리가 다릅니다」 · 삽화 그림 읽기 셋째 문장 「…가운데 몸체는 노트북 자리입니다」(문장 수 다섯 그대로).
- 서버 파일 `course_server.py` 새 판(마감 문법 고침)으로 다시 실행 — 2절 stdio 연결 결과(도구 이름·대출 글)가 옛 출력과 같음. 도구 파일은 05 판 그대로(`later_version` → 건너뜀), 서버 파일 둘은 생성기 판과 같음(`same`).
- 게이트 G1~G7 0(첫 `--no-exec`에서 G6 4 — 긴 문장 둘·다섯 문장 넘는 단락 둘 — 고친 뒤 0). AST 따로 금지 문법 0(허용 표시 `while`·`with socket.socket()`·`try` 그대로), 호출 깊이 최대 2, 금지어 0(「프로그램」 거짓 양성 말고).
