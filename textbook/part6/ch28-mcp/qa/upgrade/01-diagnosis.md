# 01절 진단과 개선 기록 — MCP 구조와 capability 협상 (experiment)

- 작업일 2026-09-28 · 작업자: 01절 담당(모델 요청 **0**) · 생성기 `qa/upgrade/author_01.py`(`71b1f594…`) · 슬러그 그대로(Ch 27 09 b8 링크).
- 읽은 것: 준비 노트(`chapter-lead-notes.md` 전부) · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 전부 · 과정 요약(§0~§9) · 계약 §3 Ch27 줄·§4·§5(묶음) · Ch 27 `chapter-summary.md`·`handoff.md`(챕터 공통·§01→§02) · 본 생성기 Ch 27 `author_01.py`(전부)·Ch 24 `author_01.py`(머리·준비물). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 4 | 90 | 4 | 0 | 0(실제로는 넷 모두 틀 문장) | 0 | 6 | 27 | 3 | **40** |
| 첫 실행 전(`gates-wip-01-01.json` 첫 판) | 25 | 365 | 0 | 0 | 0 | 0 | 0 | 8 → 1 → 0 | (그림 전) | — |
| 후(`gates-wip-01.json`, `--no-exec`) | **25** | **374** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 8건(긴 문장 여섯 — 괄호 뒤 「).」로 두 문장이 하나로 세진 것 하나 포함, 코드 이름으로 시작한 문장 둘)을 실행 전에 고쳤습니다. 정리 첫 줄은 노트북 쪽 「1. 」이 붙어 70자를 넘어 한 번 더 줄였습니다.
- 코드 줄(`count_code.py`, 주석·빈 줄 뺌) **43 → 131**(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」 — 옛 판은 셀 넷에 `async def` 둘·내포식·`next`로 몰아 적었고, 새 판은 셀 25개로 나눔. 강사 확인 대상).
- AST 따로(`/tmp/ch28-01/tools/extra_check.py` — Ch 27 판 복사): 금지 문법 0건, 허용 표시 하나(`sorted(empty_caps)` 키워드 없음 — Ch 10 이후 가르친 모양). 호출 깊이 최대 2(`depth.py`). 준비 셀 밖 셀 최대 **9줄**, 함수 본문 최대 **8줄**(`read_negotiation`), 셀당 정의 하나. `async with` 9곳·`await` 13곳(모두 셀 맨 위 — `async def` 0), 클래스·데코레이터·힌트·`try`·f-string·`importlib` 0.

## 2. 수정 전 주요 문제 (옛 판 — `qa/upgrade/before/`)

1. **판 기준이 설치판과 어긋남**: 본문 b4·b5·옛 그림이 `initialize` → `initialized` 핸드셰이크만 설명, b7 「2026-09-11 공식 사이트에서 확인한 최신 발행 스펙은 2025-11-25」 → **틀림**. 2026-09-28 규격 문서는 현재 판을 **2026-07-28**로 적고(`/specification/versioning`), 설치판 fastmcp 4.0.3 기본 `mode="auto"`도 2026-07-28(`server/discover`)을 고름.
2. b4 「서버가 resources capability를 알리지 않았다면 클라이언트는 resources/list를 사용할 수 있다고 가정해서는 안 됩니다」 — 규격 문장(옛 판 lifecycle 「Only use capabilities that were successfully negotiated」)으로는 참이나 **FastMCP 서버로는 그 장면을 만들 수 없음**(빈 서버도 세 칸을 알림 — 6절 출력). 본문이 이 사실을 말하지 않았음.
3. 코드: `next(… for … if …)` + 별표 풀기 `[Path.cwd(), *Path.cwd().parents]`(과정 요약 2-2 금지 모양) · f-string `assert` 메시지 · 반환 힌트 튜플 `tuple[list, list, list]` · `async def` 둘 + `async with`·`await`를 풀이 한 단락으로만 · 튜플 대입 · `importlib`(`spec_from_file_location`·`exec_module`) → **실습 폴더에 `__pycache__/course_server.cpython-312.pyc`를 씀**(연결 폴더). 첫 줄 주석 넷 모두 옛 생성기 틀 문장.
4. 문장: 「반환」 7·「스키마」 3·「프로토콜」 6·「프롬프트」(구성 요소 이름) 12·「측정」·「직렬화」·「식별」·「로그」·「하위 작업」(Ch 27 말 아님) · 제목 영어 「capability」를 본문에서 풀지 않음 · b3 「Ch6에서 모델·프레임워크·하네스 계층」(Ch 6 01 계층 지도는 프롬프트·컨텍스트·하네스·루프 — 부분 참).
5. 노트북 설명: 결과 읽기 0 · 준비물(요청 수·비용·시간) 없음 · 셀 첨부 그림 0 · 복습 해설 한 줄.

## 3. 바꾼 것 — 노트북 차례 (코드 셀 25, 마크다운 28)

| 절 | 셀 | 하는 일 |
|---|---|---|
| 준비 | 1 설치(setup) · 2 가져오기(setup) | `fastmcp==4.0.3`·`mcp==2.2.0`만(이 절이 쓰는 패키지, 잠금 판). **키 셀·모델·`dotenv` 없음**(묶음 실행 검사 계약). 가져오기 `json`·`os`·`runpy`·`Client`·`FastMCP` |
| 2 서버 파일 읽기 | 3 파일 위치 후보 셋(`candidates` + `for`·`break`, Ch 10 01 모양) · 4 `runpy.run_path` → `server = server_names["mcp"]` · 5 파일이 만든 이름·`lookup_policy의 종류: function` | 후보 `../course_server.py`(notebooks)·`course_server.py`(실습 폴더 맨 위)·`labs/part6/ch28-mcp/course_server.py`(저장소·묶음 맨 위) — 세 자리 확인(§6) |
| 3 기본 모드로 연결 | 6 `async with Client(server) as client:` 판 번호·블록 밖 `None`·`False` · 7 정의 `read_negotiation(client)`(한국어 키 딕셔너리 다섯) · 8 협상 결과 + `model_dump(exclude_none=True, by_alias=True)` · 9 기능 목록 JSON(`sort_keys=True`) | `async with`·await·`asyncio.run`을 첫 자리에서 한 문장씩 |
| 4 구성 요소 셋 | 10 세 목록 수 · 11 정의 `names_of(items)` · 12 이름·자료 주소 · 13 도구 설명·`input_schema` · 14 `call_tool` · 15 `read_resource` · 16 `get_prompt` | `Tool.inputSchema`는 설치판에서 사용 중단 경고가 나서 `input_schema`로 |
| 5 값 바꿔 보기 | 17 `Client(server, mode="legacy")` 협상 결과 · 18 기능 목록 JSON · 19 정의 `compare_rows` · 20 두 협상 결과 나란히 · 21 정의 `change_flags` · 22 `listChanged`·`extensions` 나란히 · 23 옛 판 모드 세 목록·도구 결과 · 24 같은가 넷 | 바꾼 값은 `mode` 하나 |
| 6 빈 서버 | 25 `FastMCP("빈 자료실")` 기능 목록 키·세 목록 | 「알리지 않은 기능」 장면을 만들 수 없다는 사실을 출력으로 |

- 첫 줄 주석은 셀마다 그 셀이 하는 일. 결과 읽기 첫 단락의 숫자 든 백틱 인용은 모두 출력에 글자 그대로(G5). 여러 줄 출력은 라벨 줄 따로(딕셔너리·JSON·자료 글).
- 출력에 실행마다 바뀌는 값 없음(ID·시각·메모리 주소·임시 폴더 0). 다만 셀 3 「고른 파일 위치」는 작업 폴더에 따라 달라짐(교재 출력 = 저장소 맨 위 → 셋째 후보, `notebooks/` → 첫 후보) — 결과 읽기 둘째 문장에 밝힘.

## 4. 챕터 리드 결정 적용

1. **묶음 실행 검사 계약**: 키·모델 객체·`dotenv`·포트·stdio 하위 프로세스·도구 파일 0, 메모리 연결만. `code_sha256` `a09d959cecc4…` → **`2407c4c571382b4f55de5aae1c30de28f4810518cc62e29fb6526524b5ca7b21`**(코드 셀 4 → 25). zip·`check_bundle_execution.py`는 **다시 돌리지 않았음**(마감 몫 — zip 안은 아직 옛 01, 지금 검사는 옛 zip으로 계속 PASS할 상태). §6의 묶음 모양 사본 실행으로 미리 확인.
2. **명세 판**: 본문은 설치판이 고르는 2026-07-28 기준, 2025-11-25는 `mode="legacy"` 비교. 두 모드의 판 번호·초기화 결과 유무·서버 정보·기능 목록(`listChanged`·`extensions`)을 모델 없이 결정적으로 출력(§6 두 커널 같음). 옛 b7 「최신 스펙 2025-11-25」는 b7 첫 항목에서 사실대로(현재 판 2026-07-28, 2026-09-28 확인). FastMCP 서버가 등록과 상관없이 세 칸을 알림은 6절 빈 서버 출력 + b7(설치판 mcp 2.2.0 `server/lowlevel/server.py` 596~607행).
3. **모델 M2 — 01 몫 요청 0**. 가짜 채팅 모델 0.
4. **비동기**: Ch 2 12(`async def`·await·`gather`·`to_thread`·파일 안 `asyncio.run()`) 확인 뒤 셀 맨 위 `async with`·await만. 풀이: `async with` = Ch 2 05 `with open`처럼 블록을 벗어날 때 연결을 닫는 줄(여는 일·닫는 일도 기다려야 해서 `async`) · 셀 맨 위 await = 노트북 도구(IPython)의 기능(Ch 18 03 선례) · `asyncio.run()`은 노트북 셀에서 `RuntimeError`(작은 노트북으로 노트북 밖 확인 — `RuntimeError: asyncio.run() cannot be called from a running event loop`) · `ainvoke`·`async def`는 이 절에 없음(04가 처음).
5. **하위 프로세스·포트 정리 규칙(02~06)**: 01은 쓰지 않음. 노트북 밖 확인 `/tmp/ch28-01/exp/x3_stdio_env.py` — MCP 설정 `{"command": sys.executable, "args": [서버 파일], "keep_alive": False, "env": {"FASTMCP_SHOW_SERVER_BANNER": "false", "FASTMCP_CHECK_FOR_UPDATES": "off", "FASTMCP_LOG_LEVEL": "WARNING"}}` → 블록 안 자식 프로세스 1 → 블록 뒤 0, **표준 오류 0줄**. `env` 없이는 배너 + `Update available: 4.0.10`(PyPI 확인 — 설치판 `utilities/version_check.py`, 결과를 `fastmcp.settings.home`의 `version_cache.json`에 남김) + `INFO Starting MCP server …`(시각 섞임) 27줄. 세 이름은 설치판 `settings.py`(`env_prefix="FASTMCP_"`, 312~340행)에서 확인. 규칙 전문은 `handoff.md`.
6. **paired 02·03 설계** → `handoff.md` 「§01 → §02」·「챕터 공통」. 02 Before/After 현상은 노트북 밖 `/tmp/ch28-01/exp/x4_hint.py`로 다시 확인(힌트 없음 입력 형식 `{'topic': {}}`·설명 `None`·`{"topic": 3}` → `ToolError: Error calling tool 'lookup_policy': 3` ↔ 힌트 `topic: str` → `1 validation error … Input should be a valid string`, 서버 오류 기록 32줄이 표준 오류로 → `logging.getLogger("fastmcp").setLevel(logging.CRITICAL)`이면 0줄).
7. **용어** → §7.
8. **도구 파일**: 01은 만들지 않음(앞 챕터 함수를 쓰지 않고, 묶음 계약). 이름 후보 `connect_tools.py` — 과정의 도구 파일 이름(`agent`·`approval`·`checkpoint`·`data`·`delegation`·`git`·`graph`·`harness`·`llm`·`order`·`rag`·`runner`·`stream`·`workflow`_tools)과 겹치지 않음(`find labs -name '*_tools.py'`).
9. **pyc**: 막는 쪽 — `importlib` 대신 **`runpy.run_path`**(표준 라이브러리 함수 하나, 파일이 만든 이름을 딕셔너리로 내놓음 — 새 이름 한 문장). 노트북 밖 확인: `env -u PYTHONDONTWRITEBYTECODE`로 사본 폴더에서 `runpy.run_path` → `__pycache__` 없음 ↔ `importlib` → `course_server.cpython-312.pyc` 생김. 묶음 모양 사본 새 커널 실행(`PYTHONDONTWRITEBYTECODE` 없이)도 pyc 0개. 까닭: 연결 폴더는 삭제가 막혀 pyc가 쌓이기만 함, `.gitignore`(`labs/**/__pycache__/`·`*.pyc`)와 묶음 허용 목록이 이미 빼지만 쓰지 않는 쪽이 깨끗함. `run_name`이 `"<run_path>"`라 서버 파일 끝 `if __name__ == "__main__":`(stdio 실행)은 돌지 않음(본문에 한 문장). **서버 파일은 고치지 않음**(02~05·묶음 계약 영향 0). 옛 판이 남긴 pyc(09-10 15:52)는 그대로(삭제 승인 대상).
10. **옛 생성기**: `qa/author_ch28.py`·`figures/_gen_figures.py` 맨 위 설명 주석 셋 + `raise SystemExit(...)`(원본 사본 `/tmp/ch28-01/pre/`·`qa/upgrade/before/generators/`와 `diff` — 네 줄씩만 더함). 실행하면 종료 코드 1로 멈춤 확인. 해시 `6806d465…` → `41a3af28…` · `dadf0c2b…` → `5bb85474…`. 옮기기(`mv -n`)는 마감.
11. 슬러그 다섯 그대로. 절 제목 「MCP 구조와 capability 협상」은 제목에만(강사 확인).
12. **문법 범위**: §1 AST.
13. **비유 계열 「우주 정거장 도킹 포트」** 01이 엶(§10).
14. 준비 셀 과정 표준(설치·가져오기, 키 셀 없음).

## 5. 설치판·명세 확인 (2026-09-28)

- WebFetch: `https://modelcontextprotocol.io/specification/versioning`(「The current protocol version is 2026-07-28」) · `…/specification/2026-07-28`(Hosts·Clients·Servers, JSON-RPC 2.0, 「Stateless, self-contained requests」·「Per-request capability negotiation」, 서버 기능 Resources·Prompts·Tools) · `…/2026-07-28/changelog`(SEP-2575 — `initialize`/`notifications/initialized` 없앰, `_meta` 판 번호·클라이언트 기능 목록, `server/discover` MUST, `subscriptions/listen`, SEP-2567 세션 없앰) · `…/2026-07-28/basic/versioning`(「There is no negotiation handshake」, `-32022`, Modern/Legacy/Dual-era 표) · `…/2026-07-28/server/discover`(판 목록·기능 목록·서버 정보·사용 설명, 서버 정보는 보안 판단에 쓰지 말 것) · `…/2026-07-28/server/tools`(`listChanged` 알림은 `subscriptions/listen` 연결로) · `…/2025-11-25/basic/lifecycle`(`initialize` 요청·응답·알림, 「Only use capabilities that were successfully negotiated」) · `https://gofastmcp.com/clients/client`(FastMCP 4.0.0 문서 — `mode` auto·legacy·판 고정, 메모리 연결).
- 공식 문서와 설치판 차이: 없음(판 번호·`mode` 동작·`initialize_result` 없음이 문서와 출력이 같음). FastMCP 문서 판(4.0.0)은 설치판(4.0.3)보다 앞선 판 표시. 옛 원고 b10의 `gofastmcp.com/v2/servers/server`(v2 문서) 링크는 뺌.
- 설치판 소스 행(본문 b7·b10): fastmcp 4.0.3 `client/client.py` 312~318(`mode` 설명)·837~889(`_negotiate`) · `server/low_level.py` 465~469(옛 판용 `NotificationOptions(… True)`) · `server/server.py` 425(서버 판 = `fastmcp.__version__`) · mcp 2.2.0 `server/lowlevel/server.py` 585~587(현재 판 `listChanged` = `subscriptions/listen`을 받는가)·596~607(목록 처리기가 있으면 칸) · `mcp_types/version.py` 24~41(알려진 판 다섯·현재 판) · `mcp/server/fastmcp.py` 10행(옛 이름 가져오면 「FastMCP was renamed to MCPServer」).
- 오간 첫 요청 차례(노트북 밖 `/tmp/ch28-01/exp/x2_more.py` — 서버 `Middleware.on_message`로 적음, 두 번 같음): auto `server/discover → tools/list → resources/list → prompts/list → tools/call → resources/read → prompts/get` ↔ legacy `initialize → notifications/initialized → (같음)`. 상속이 필요해 노트북에 넣지 않음(규격 조건부).

## 6. 새 커널 두 번 · 키 없는 실행 · 네트워크

- **A(교재 출력)**: `run_section.sh … 01` → `PASS 01-MCP-구조와-capability-협상.ipynb: 25 cells`, `executed_at` 2026-09-28T19:32:15Z, `code_sha256` `2407c4c57138…`, `outputs_sha256` `32ff72d6ace0…`. 표준 오류 흐름 0(모든 셀 stdout만).
- **B(사본, 그림·삽화 전)**: `/tmp/ch28-01/B/` 19:32:41Z PASS 25셀 — 셀별 출력 글 **25/25 같음**(출력 글 연결 해시 A·B 모두 `2bcfd9f35f364502`). `outputs_sha256`만 `c08e168fdb24…`로 다름 — 설치 셀의 스트림 두 개(Note 줄 · 판 번호 줄)가 B에서 한 스트림으로 합쳐짐(글자는 같음, Ch 24 마감 선례).
- **키 없는·네트워크 없는 묶음 모양 실행**: `/tmp/ch28-01/bundle/part6-practice/labs/part6/ch28-mcp/`(서버 파일 + 노트북만)에서 `env -u OPENAI_API_KEY` + `HTTP(S)_PROXY=http://127.0.0.1:9`(닿지 않는 프록시)·`UV_OFFLINE=1`·`--cwd …/notebooks`·`--kernel-python` 실습 가상환경 → **PASS 25셀**, `code_sha256` 같음, 셀별 24/25 같음(다른 하나는 셀 3 `고른 파일 위치: ../course_server.py` — 작업 폴더 차이, 예정대로). 두 번째 실행은 `PYTHONDONTWRITEBYTECODE` 없이 → PASS, 사본 폴더에 pyc·`__pycache__` 0. `.env` 없는 폴더라 FastMCP 설정도 `.env`를 읽지 않음. `uv sync --locked`(묶음 검사 2단계)는 이번에 돌리지 않음 — 마감의 `check_bundle_execution.py` 몫.
- 실습 폴더 `__pycache__/course_server.cpython-312.pyc` 수정 시각 09-10 15:52 그대로(A·B·사본 실행 뒤).

## 7. 용어 (새 용어 meta 6)

| 말 | 뜻(첫 자리) | 코드에서 |
|---|---|---|
| MCP(Model Context Protocol) | 모델이 쓸 도구와 자료를 다른 프로그램에서 가져오는 통신 규약(「MCP는」으로 문장을 시작하지 않음) | 서버 파일 · `Client` |
| 통신 규약(protocol) | 두 프로그램이 주고받을 메시지의 모양과 차례를 정한 약속 — 「프로토콜」은 본문 0(제목 영어 이름 안에만) | 첫 요청 `server/discover` · `initialize`(노트북 밖) |
| MCP 서버 · 클라이언트(+ 호스트 한 문장) | 내놓는 쪽 / 요청을 보내는 쪽 · 호스트 = 모델을 쓰는 응용 프로그램(이 절은 노트북이 대신) | `server` · `Client(server)` |
| 판 번호(protocol version) | 두 쪽이 어느 판의 규격 문서로 말할지 정한 값, 날짜로 부름 · 현재 판 = 2026-07-28 · 옛 판 = 2025-11-25 | `client.protocol_version` |
| 기능 목록(capability) | 서버가 어떤 종류의 요청을 받는지 알리는 딕셔너리(권한·등록 항목 아님) — 「capability」는 제목·b2 첫 풀이·용어 표에만 | `client.server_capabilities` |
| 자료(resources) · 메시지 틀(prompts) | 주소(URI)로 읽는 글 / 빈자리에 값을 넣어 받는 메시지(Ch 7 04 틀·빈자리) — 「리소스」·「프롬프트」는 본문 0 | `policy://handbook` · `explain_policy` |
| (새 용어 밖) 기본 모드 · 옛 판 모드 | 인자 `mode`의 기본값 `auto` / 값 `"legacy"` | `Client(server, mode="legacy")` |
| (새 용어 밖) 초기화 결과 · 사용 설명 · 서버 판 | `initialize_result` / `instructions`(「안내 글」은 Ch 27 05 뜻이라 쓰지 않음) / `server_info.version` | 3·5절 |
| (새 용어 밖) 연결 | 「세션」 대신 | `async with` 블록 |

- 대체어 적용: 반환 → 내놓다 · 스키마 → 입력 형식(Ch 19) · 검증 → 검사 · 경로 → 파일 위치 · 세션 → 연결 · 로그 → 기록 · 직렬화 → JSON 글로 바꾸기 · 캐시 → 쓰지 않음.
- 금지어 검사 `/tmp/ch28-01/tools/ban28.py`(ban27 + 프로토콜·세션·핸드셰이크·리소스·인스턴스·스펙·레거시·안내 글·capability·JSON-RPC 자리 확인) — 노트북 설명·주석·`_src`·캡션·`.mmd`: 걸림은 ① 「프로그램」 속 「로그」(거짓 양성) ② 「capability」 제목·메타 슬러그·b2 첫 풀이·용어 표(의도) ③ 「JSON-RPC」 첫 풀이·참고 자료(이름) ④ **b3 「네 칸(프롬프트·컨텍스트·하네스·루프)」 — Ch 6 01 계층 이름을 그대로 인용**(챕터 리드 결정 7 「Ch 6 계층 문장은 실제 계층대로」에 따름, 이 한 곳 예외 — 강사 확인). 「한 겹 더」 0.

## 8. 옛 원고의 틀린 사실과 고친 방식

| 옛 문장 | 사실 | 새 판 |
|---|---|---|
| b7 「2026-09-11 … 최신 발행 스펙은 2025-11-25」 | 현재 판 2026-07-28(규격 문서 2026-09-28 확인), 설치판 기본도 그 판 | b2·b4·b7에 현재 판 기준, 옛 판은 `mode="legacy"` 비교 |
| b4·옛 그림 「연결이 시작되면 initialize 요청과 응답으로 … 교환」 | 옛 판만. 현재 판은 요청마다 판 번호·기능 목록, `server/discover` | b4 「두 판의 협상」 두 단락 + 5절 출력 |
| b4 「resources capability를 알리지 않았다면 …」(장면으로 암시) | 규격 문장은 참, FastMCP 서버로는 재현 불가 | 6절 빈 서버 출력 + b7 한 항목 |
| b3 「Ch6에서 모델·프레임워크·하네스 계층」 | Ch 6 01 계층 지도 = 프롬프트·컨텍스트·하네스·루프 | b3 실제 네 칸 |
| b3 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스」 | 뜻으로 참, 「하위 작업」은 Ch 27 말 아님 | 「파일 도구와 서브에이전트 위임을 미리 조립해 둔 Deep Agent(하네스)」 |
| b3 「Ch19에서 도구 이름·설명·입력 스키마가 모델 선택에 영향」 | 부분 참(Ch 19 04는 설명만 바꿈) | 「04절에서는 설명만 바꾼 두 판을 모델에게 알려, 고른 도구와 입력 토큰을 견주었습니다」 |
| b7 「JSON-RPC 메시지와 모델에게 전달되는 프롬프트는 같은 데이터가 아닙니다 …」 | 참이나 이 절이 잰 값 아님 | 뺌(05 몫) |
| b10 FastMCP v2 문서 링크 · 확인 2026-09-11 | 설치판 4.0.3 — 4.0 문서 | FastMCP 4.0 Client 문서, 확인 2026-09-28 |

## 9. 그림 (Mermaid 4 + 삽화 1)

- 설계표 `01-figures.md`. 원본 viewBox 폭: 01-1 **275** · 01-2 **271** · 01-3 **319** · 01-4 **437**(모두 868 이하). PNG 넷 직접 확인(`.cache/ch28-01-view/`). 첫 렌더에서 01-2 `async with Client server as client`·01-3 공통 상자·01-4 상자 셋이 단어 가운데서 끊겨 `<br>`로 미리 나누고 다시 렌더(라벨 값 변경 0).
- 색: 초록 = 서버 파일·빈 서버(자료·우리가 만든 객체) · 파랑 = 우리가 부른 코드 · 노랑 = 출력 값 · 회색 = 노트북 밖·소스 확인·두 모드 공통 · **보라 0 · 빨강 0**. 나란한 상자는 `~~~`, 개수는 한글, 라벨 대괄호·따옴표 0, subgraph 제목 `<br>` 0, 노드 id `call`·`end` 0, 노드 7개 이하(01-3 일곱).
- G7 라벨 숫자(`2026-07-28`·`2025-11-25`)는 출력에 있음. 01-3 첫 요청 상자는 「노트북 밖 확인」, 01-2는 「설치판 소스와 노트북 밖 확인」, 01-4 규칙 상자는 「소스 확인」.
- **차례 기록**: `.mmd` 넷은 새 커널 A 전에 탐색 출력 값으로 적었고 `run_section.sh`가 A 직후 렌더했습니다. 라벨 값은 A·B 출력과 모두 맞았고, 설계표는 B·삽화 뒤에 적었습니다(규격 §5-2 「그림을 만들기 전에 설계표」와 차례가 어긋남 — Ch 27 09 B-10과 같은 [하] 기록).

## 10. 삽화 — 「우주 정거장 도킹 포트」 계열을 엶

- 01-5 `도킹-고리-셋과-우주선-둘` — 정거장 모듈 하나(서버) · 앞면 고리 셋(구성 요소 셋) · 우주선 둘(인자 `mode`만 다른 클라이언트 둘), 두 우주선의 똑같은 회색 고리(같은 통신 규약).
- `generate_image` 한 번, `params` `{"model":"nano_banana_pro",…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}` → **job `381d8fc4-4bc3-40bb-a8ad-70efbfbbd61c` 1차 채택(재생성 0)**. `jobs_wait` 모델 표시 **`nano_banana_2`**(요청 `nano_banana_pro`와 다름 — 기록만, 거래 표시 「Nano Banana Pro」).
- 크레딧: 생성 전 잔액 2321(바로 앞 거래 16:51:59Z는 다른 세션), 이 절 거래 **2026-09-28T19:33:39.592199Z 「Nano Banana Pro −2」 한 줄 = 2크레딧**.
- 원본 `0f96d678…`(2752 × 1536) → 폭 1100(LANCZOS) `a8c60275…`(1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄인 그림과 저장 PNG 픽셀 대조: bbox `None`, 최대 차이 0. 저장 PNG 사본을 직접 열어 개수(정거장 하나·고리 셋·우주선 둘)를 세고 그림 읽기·alt를 씀.
- 그림과 비유의 차이(그림 읽기·prompt 파일에 밝힘): 우주선 고리가 정거장 고리보다 작게 그려져 「같은 규격」이 크기로 보이지 않음 → 고리의 색·크기·거리는 짝짓지 않는다고 적음 · 우주선 몸체가 컵 모양에 가깝고 가운데 여백이 넓음(강사 확인).

## 11. 완료·대기 챕터 문장

- **Ch 27 09 b8** 「Ch 28 01절에서는 도구를 같은 프로그램 밖의 서버로 옮겨, 여러 클라이언트가 같은 방식으로 찾게 하는 MCP를 봅니다」 + 01 슬러그 링크 → **참**(슬러그 그대로 · 01 b2가 같은 말로 이음 · 도구가 노트북 밖 서버 파일의 서버 객체에 있고 클라이언트가 MCP 요청으로만 부름 · 모드가 다른 두 클라이언트가 같은 목록·결과를 받음 5절 `True` 넷). 단 01은 **같은 프로세스 메모리 연결**이라, 다른 프로그램(하위 프로세스)으로 띄우는 장면은 03 몫(01 b4 「비유와 다른 점」에 밝힘).
- **Ch 6 01** 계층 지도(프롬프트·컨텍스트·하네스·루프, MCP 언급 0) → 01 b3가 실제 네 칸으로 인용, 참. Ch 6 01 파일은 고치지 않음.
- **Ch 19 요약 §13 「Ch 28 MCP」 01 두 줄**(b2 참 · b3 부분 참) → 새 b3은 Ch 19 01(`@tool`·이름·설명·입력 형식)·04(설명만 바꾼 두 판) 그대로라 참.
- Ch 27 요약 §16·§17 「Ch 28 01 b3 하위 작업」 → 고침(서브에이전트 위임).
- 계약 §5 「`check_bundle_execution.py` PASS(Ch 24 01·Ch 28 01) · Ch 28 01 `a09d959cecc4…` 4셀」 → **이제 옛 값**(과거 기록이라 고치지 않음, 새 값 `2407c4c57138…` 25셀은 마감 기록에).

## 12. 챕터 밖 수정

- **없음**(과정 문서·공용 도구·Part 6 목록·zip·검사 스크립트·Ch 27 파일 0). 예외: `run_section.sh`의 `verify.py --chapter`가 `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json`을 다시 씀(선례와 같음).
- 실습 폴더(챕터 몫): 01 노트북만. `course_server.py`·README·잠금 그대로.

## 13. 보호 파일

- `before-manifest.json` 226개 대조 → 바뀐 6개(01 `_src`·HTML·노트북 · 옛 생성기 둘 · notebook-contracts), 없어진 것 0 → `manifest-changes.md` 「01절 뒤」.

## 14. 남은 것 · 지우지 않은 것 · 강사 확인

- **마감 몫**: 옛 생성기 둘 `mv -n` → `qa/upgrade/before/generators/blocked/` · 공개 목록 → `part6-practice.zip` 다시 → **`check_bundle_execution.py`(Ch 24 01·Ch 28 01 — 새 01 `code_sha256` `2407c4c57138…`)** · `chapter.json` `objectives` 「capability 협상」(판 기준 문장과 대조) · 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}`(본문 참조 0 — 챕터 공개 목록 줄 빼기는 마감) · `집필점검표.md`·`qa/verification.md`의 옛 판 표시.
- **지워야 하지만 지우지 않은 것**(삭제 승인 대상): 실습 폴더 `labs/part6/ch28-mcp/__pycache__/course_server.cpython-312.pyc`(옛 판 09-10) · `qa/upgrade/gates-wip-01-01.json`·`gates-wip-01.json` · 사용자 디스크 `.cache/ch28-01-view/`(그림 확인 사본 다섯, 약 1MB) · 기기 `/tmp/ch28-01/`(탐색 스크립트 `exp/`·사본 `B/`·`bundle/`·`mini/`·`illu/`·`pre/`·`tools/`) · venv 안 `mcp/server/__pycache__/fastmcp.cpython-312.pyc`(준비 단계 흔적으로 보임 — 이 절은 만들지 않음). FastMCP 버전 확인 캐시(`fastmcp.settings.home/version_cache.json`, 기기 사용자 데이터 폴더 — x3 탐색 `env` 없는 실행이 만들었을 수 있음, 연결 폴더 밖).
- **강사 확인 대상**: 제목 말 「capability」(본문은 「기능 목록」)·「협상」(현재 판에는 첫 협상 요청이 없음 — 본문은 요청마다 판 번호를 싣는 것까지 협상으로 설명) · b3 Ch 6 계층 이름 인용(「프롬프트」 한 곳) · 코드 줄 43 → 131·코드 셀 4 → 25 · 01이 FastMCP 서버 객체를 하나 만듦(6절 빈 서버 — 02 주제의 한 줄 앞당김) · 삽화 우주선 몸체·여백·고리 크기 · 새 용어 6.

## 마감 반영 (2026-09-28, 검토 1차 A-1~A-4)

- **다시 실행하지 않았습니다**(마크다운만 — 생성기 문자열 치환 → 달라진 마크다운 셀만 노트북에 옮김 → `_src` → `run_section.sh … 01 --no-exec`). `code_sha256` `2407c4c57138…`·`outputs_sha256` `32ff72d6ace0…`·`executed_at` 19:32:15Z 그대로, 노트북 파일 `049d4608` → `ee6068c3`. **묶음 실행 검사 계약 그대로** — 마감 zip(`5002dce3…`)으로 `check_bundle_execution.py` PASS(`bundle-execution.json` `fc4e1b78…`).
- **A-1**: b8 「다음 학습과 이어지는 지점」·노트북 정리 끝 「02절에서는 서버 파일에 도구를 붙이는 줄을」 → 「서버에」(02는 노트북에서 만든 서버 객체에 붙임).
- **A-2**: (가) b4 비유 「정거장에 무엇이 있는지를」 → 「정거장이 어떤 종류의 짐을 받는지를」(기능 목록은 등록 항목이 아님 — 목표 셋째와 맞춤) · (나) b2 「Ch 19부터 Ch 27까지 도구는 모두 노트북 안의 파이썬 함수였습니다」 → 「Ch 19부터 Ch 27까지 쓴 도구는 모두 에이전트와 같은 프로그램 안에서 돌았습니다」(Ch 27 기본 파일 도구 포함).
- **A-3**: 셀 20 결과 읽기에 셋째 단락 — 칸 `extensions`는 현재 판에 새로 생긴 칸 · 안의 `io.modelcontextprotocol/ui`는 도구·자료에 화면 정보를 싣는 확장 이름이고 설치판 fastmcp가 늘 알림(`server/low_level.py` 574행) · 현재 판 변경 목록은 기록 기능을 더 쓰지 말라고 표시했지만 설치판 서버는 칸 `logging`을 알림 · 알림과 기록은 실행하지 않음. 셀 38 결과 읽기에 「칸 `extensions`는 현재 판에 새로 생긴 칸이라, 설치판 SDK가 옛 판 응답에서는 이 칸을 뺍니다」(`server/low_level.py` 562~564행 설명 「the SDK's pre-2026 version sieve strips capabilities.extensions on legacy eras」). 「사용 중단」은 과정 금지어 검사에 걸려(「중단」) 「더 쓰지 말라고 표시」로 씀.
- **A-4**(기록만): 01 그림 설계표를 렌더 뒤에 적은 차례(§9에 이미 적음) — `chapter-summary.md` 절차 메모에 한 줄. 라벨 값은 A·B 출력과 맞음(검토 확인).
- 서버 파일 `course_server.py` 문법 고침(마감, `5dc77333…`): 01이 읽는 서버 이름·사용 설명·판·기능 목록(두 모드)·세 목록·자료 글·메시지 틀 글·도구 결과·파일이 만든 이름 여섯이 옛 판과 글자까지 같음(`/tmp/ch28-close/srv/srvcmp.py` — 18항목 10,787바이트 같음). 01 출력은 바뀌지 않으므로 다시 실행하지 않음.
- 게이트 G1~G7 0(`gates-after.json`).
