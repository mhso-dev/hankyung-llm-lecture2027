# Ch 28 MCP — Model Context Protocol — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part6/ch28-mcp`(절 다섯 — 01·04·05 experiment, 02·03 paired) · `labs/part6/ch28-mcp`. 바로 앞 Ch 27(완료, 모델 결정 M2)을 잇는 Part 6 여덟째 챕터입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 40개, 500,480바이트 — 원본과 `cmp` 모두 같음) · `gates-before.json`(`495ac467…`) · `before-manifest.json`(226개, `e5259ab8…`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch28-mcp`(300MB, 사용자 디스크).
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(§0~§9 전부) · 계약 파일(`grep -n '^#'` 뒤 §3 Ch19~27 인계 줄·§4 도구 파일 줄·§5 묶음 줄·§8 기준 버전) · Ch 27 `chapter-summary.md`(전부)·`chapter-lead-notes.md`(전부)·`before-manifest.json`(모양) · Ch 19·21·23~26 요약의 Ch 28 줄 · Ch 2 12 노트북(비동기) · Ch 18 03 노트북(`await` 설명 선례) · Ch 19 03 노트북(`spec_length`) · Ch 6 01·Ch 16 01 `_src`(b3 대조) · Part 6 목록·묶음·검사 스크립트 · 챕터 `qa/` 기록·`집필점검표.md`·Part 6 `ch28-technical-review.md`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0건(단, `before/lab/` 빈 폴더를 만든 뒤 `rmdir`이 막혀 그 자리에 실습 폴더 사본 넷을 넣음 — 아래 §15), 노트북 실행 0건, 서비스 모델 요청 0건, `uv cache prune` 안 함. 확인은 기기 `/tmp/ch28-prep/exp/`의 작은 스크립트(`e0`~`e10`)와 설치판 소스·공식 문서로 했습니다. 띄운 MCP 서버(메모리 연결·stdio 하위 프로세스·127.0.0.1 HTTP)는 모두 스크립트 안에서 끝났고, 끝난 뒤 남은 서버 프로세스 0개를 확인했습니다. 모델 객체는 가짜 키 글로 **만들기만** 했습니다(`bind_tools` 명세 확인, 요청 0).
- `chapter.json` `hours` = 「총 16h · 강의 5h · 실습 11h」. 절 meta 강의 1h × 5 = **5h**, 실습 2·3·2·2·2 = **11h** — 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part6/_build_index.py` 26행 (5, 11)·`qa/check_scope.py` `EXPECTED` (5,11)·`SECTION_COUNTS` 5도 같습니다. 새 용어 meta 6·5·7·5·6 = 29(옛 생성기 값 — 실제 새 말 목록 없음).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-28)

| 절 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 MCP 구조와 capability 협상 | 4 | 90 | 4 | 0 | 0 | 0 | 6 | 27 | 3 | 40 |
| 02 FastMCP 로컬 서버 제작 | 4 | 88 | 8 | 2 | 0 | 0 | 6 | 25 | 3 | 44 |
| 03 stdio와 원격 전송·권한 경계 | 5 | 90 | 2 | 1 | 0 | 0 | 7 | 30 | 3 | 43 |
| 04 LangChain MCP 클라이언트 연동 | 3 | 80 | 3 | 1 | 0 | 0 | 5 | 29 | 3 | 41 |
| 05 도구 정의와 첫 호출 토큰 | 6 | 97 | 4 | 3 | 0 | 1 | 8 | 21 | 3 | 40 |
| **합계** | **22** | **445** | **21** | **7** | **0** | **1** | **32** | **132** | **15** | **208** |

- 통과 절 **0/5**. 코드 줄(주석·빈 줄·`%pip` 뺌) 01 42 · 02 56 · 03 46 · 04 37 · 05 98 = **279줄**(`/tmp/ch28-prep/ast_scan.py`).
- G1 21 = 리스트 내포식 10 · 제너레이터 식 6 · 조건 표현식 2(04 c5·05 c9) · 셀당 함수 둘 이상 3(02 c5·c7, 05 c5).
- G2 7 = 15줄 넘는 셀 7(02 c5 17·c9 18 · 03 c9 21 · 04 c5 18 · 05 c5 19·c7 16·c11 20).
- **G3 0이지만 실제로는 22셀 모두 틀 문장** — 첫 줄 주석이 모두 「# ○○에 필요한 값을 준비하고 결과를 확인합니다」(옛 생성기 틀, 규격 §2-5 결함). 게이트 패턴(「이 셀은 … 수행」)에 걸리지 않을 뿐입니다.
- G4 1 = 05 c11 `init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none")`에 `temperature` 없음. 가짜 모델 0.
- G5 32 = 절마다 제목 셀·핵심 그림 첨부 없음 10 + 결과 읽기 인용 없음 17 + 마지막 코드 셀 뒤 결과 읽기 없음 5.
- G6 132 = 70자 초과·영문 시작 조사·5문장 넘는 단락. §4 금지어는 G6가 대부분 세지 않음(§1 표).
- G7 15 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈, `/tmp/ch28-prep/ast_scan.py`)

- **`next(… for … if …)` + 별표 풀기 `[Path.cwd(), *Path.cwd().parents]`**: 01 c5 · 02 c9 · 03 c9 · 04 c5(서버 파일 찾기 — 과정 요약 2-2 금지 모양 그대로) · 05 c3(`.env` 찾기).
- **f-string**: 01 c5·02 c9 `assert` 메시지 `f"서버 파일을 찾지 못했습니다: {server_path}"` · 05 c7 `f"{_name}: {query}"` · **`course_server.py` 두 곳**(리소스·프롬프트 글, Ch 13~27 f-string 0건).
- **타입힌트**: 모든 `async def`의 반환 힌트 `tuple[list, list, list]`·`tuple[list[str], str]`·`tuple[object, list, object]` 등(과정 요약 2-1 「처음 쓰면 한 문장」 — Ch 19~27은 `@tool` 매개변수 `: str`만), 05 `schema_chars(tools: list) -> int`·`first_call(tools: list) -> dict`·`load_mcp_tools(server: object) -> list`.
- **비동기**: `async def` 9개(01 둘·02 셋·03·04·05 둘) · `await` · **`async with`**(01·02·03·04·05 — 과정 처음. Ch 2 12는 `async def`·`await`·`gather`·`to_thread`·파일 안 `asyncio.run()`만, `async with`는 안 가르침) · `ainvoke`(03·04 — 과정 처음, Ch 30 옛 판만 씀).
- **데코레이터**: `@after.tool`(02) · `@tool`(04·05) · `@small.tool`(05) · `course_server.py`의 `@mcp.tool(tags={...})`·`@mcp.resource("policy://handbook")`·`@mcp.prompt` — 「이 줄은 아래 함수를 ○○로 등록합니다」 설명 0곳(규격 §2-2 L6).
- **함수 안의 함수에 가까운 것**: 05 c7 — `for` 안에서 `async def read_only(query: str, _name: str = name)`(기본값 매개변수 + 루프 안 정의) + `read_only.__name__ = name`·`read_only.__doc__ = …`(속성 대입) + `large.tool(read_only, name=name)`.
- **그 밖**: `try/except ToolError` + `type(error).__name__`(02 c5) · `isinstance`(04 c5·05 c9) · `.get`(03 c7 `os.environ.get`·04 c5 `schema.get`) · `all(… for …)`(04 c7) · `sum(… for …)`·`round(…, 8)`·`1_000_000`(05 c13) · `sorted`(03 c7) · `dict(os.environ)`(03 c5) · `bool(…)`(04 c7) · `importlib.util.spec_from_file_location`·`module_from_spec`·`exec_module`(01·02 — 과정 처음) · 튜플 대입 `tools, resources, prompts = await discover()` · 한 셀에 판 확인·키 확인·`.env` 찾기(05 c3 15줄, 규격 §2-4 준비 네 셀과 다름) · `course_server.py` 제너레이터 식 `"\n".join(f"…" for topic, text in POLICIES.items())`·집합 `{"public", "read"}`.

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(한 번) | 서버를 띄우는 방법·끝내는 방법 | 파일 쓰기와 자리 | 손 값 | 금지어(`_src` b1~b9 / 노트북 md / 주석) | `assert`(무엇에) |
|---|---|---|---|---|---|---|---|
| 01 | `importlib`로 `course_server.py`를 읽어 FastMCP 서버 객체를 얻고, `fastmcp.Client(course_server.mcp)`로 도구·리소스·프롬프트 목록 셋(각 1)을 읽은 뒤 `call_tool`·`read_resource`·`get_prompt`로 한 번씩 씀. 본문은 **`initialize` → `initialized` 핸드셰이크**로 협상을 설명 | **0**(키·모델·`dotenv` 셀 없음 — 묶음 실행 검사 대상, §5) | **같은 프로세스 메모리 연결**(하위 프로세스·포트 없음), `async with Client(...)`를 벗어나면 끝 | `exec_module`이 실습 폴더에 `__pycache__/course_server.cpython-312.pyc`를 씀(지금 파일 09-10 15:52 — 이 절·02가 만든 것으로 보임, 연결 폴더) | b7 「2026-09-11 … 최신 발행 스펙은 2025-11-25」(**지금 틀림 — 2026-07-28 발행**, §6-1) | 반환 7/5 · 스키마 3/1 · 프로토콜 6/1 · 측정 2 · 명시 1 · 직렬화 1 · **프롬프트 12/6/1**(MCP 구성 요소 이름 — §10-2) · 식별 1 · 로그 1 · 토큰화 1 · 수치 1 · **하위 작업 1**(Ch 27 인계) · 인스턴스 0/1 · 제목 영어 「capability」 | 개수 튜플 `(1, 1, 1)` · 서버가 정한 글에 「14일」·「운영:」·「대출」(도구 함수가 정한 값 — 허용) |
| 02 **paired** | Before: 이름만 같은 일반 함수(데코레이터 없음)를 둔 서버 → `list_tools()` `[]`·`call_tool` → `ToolError` / After: `@after.tool` 등록 → `['lookup_policy']`·「14일」 / 완성 서버 세 구성 요소 확인 | **0** | 메모리 연결(`async with Client(before/after/course_server.mcp)`) | 01과 같은 `pyc`(c9 `exec_module`) | `_src` b5·b6 「**UnknownToolError**」(출력은 `ToolError`, 설치판 메시지 `Unknown tool: 'lookup_policy'`) · 「비교한 원인은 함수 등록 여부 하나」(**틀림** — Before 본문 `{"대출": "14일"}`·독스트링 없음 ↔ After 본문 글·독스트링이 다름) · b7 「학생 배포 파일은 … 다섯 개 노트북」 | 반환 8/3 · 스키마 3/1 · 프로토콜 3 · 측정 2 · 경로 1/1 · 프롬프트 5/3 · 인스턴스 4 · **장식자 4**(Ch 19 말은 「데코레이터 줄」) · 로그 2 · 표면 1/1 · 위장 1/1 · 배포 4 · 거부 0/1 · 제목 영어 「FastMCP」 | `before_names == []` · `after_names == ["lookup_policy"]` · 「14일」 in 결과 |
| 03 **paired** | Before: `dict(os.environ)` 개수·`OPENAI_API_KEY` 이름 포함 여부 출력만 / After: `{"PATH": …, "PYTHONUNBUFFERED": "1"}`만 담은 `safe_env` → `MCPAdapter({"mcpServers": {"course": {"command": sys.executable, "args": [...], "env": safe_env}}})`로 stdio 호출 / 전송별 경계 표(튜플 두 줄 출력) | **0**(키 셀 없음 — Before의 「키 이름 포함」은 `.env`를 읽지 않아 **`False`**) | **stdio 하위 프로세스**(`course_server.py`의 `mcp.run(transport="stdio")`). `async with`를 벗어나도 **하위 프로세스가 남음**(FastMCP `keep_alive` 기본 `True` — §6-4). HTTP는 실행하지 않음(설정 표만) | 없음(서버는 스크립트로 실행) | 「전체 환경 변수 개수: 60」(기기마다 다름) · 결과 출력의 `'id': 'lc_33b10a9c-…'`(**실행마다 새 값**) · b5·b6 「PATH와 PYTHONUNBUFFERED만 … 전달」(**틀림** — SDK 기본 여섯 이름이 더해져 서버는 일곱 이름을 받음, §6-4) | 검증 2/2 · 사전 2/4(→ 딕셔너리) · 엔드포인트 1 · 바인딩 1 · 노출 1/1 · 배포 3 · 측정 2 · 경로 1 · 제목 영어 「stdio」 | `len(unsafe_env) > 2` · `"OPENAI_API_KEY" not in safe_env`(**만든 대로 늘 참**) · 도구 이름 · 「20:00」 in `str(result)` · 표의 두 첫 칸이 다름(**늘 참**) |
| 04 | `MCPAdapter(server_path)`(Path → stdio)로 `list_tools()` → 입력 형식 딕셔너리의 `required` → `ainvoke({"topic": "운영"})` / 직접 `@tool`과 이름·입력 형식 있는지만 견줌 | **0** | stdio 하위 프로세스(03과 같음 — 남음) | 없음 | 결과의 `'id': 'lc_1fcdef69-…'`(실행마다 새 값) · b4 「커리큘럼의 langchain.mcp 표기는 확인 결과 유효합니다」(제작 이력 성격 — 규격 §4) · b3 「BaseTool」(Ch 19는 이 이름을 안 씀) | **반환 9/4** · **인터페이스 10/3/1** · 스키마 3/2 · 프로토콜 2 · 측정 3 · 캐시 2 · 경로 2 · 지연 1 · 인스턴스 2 · 인터셉터 1 · 배포 1/1 · 사전 0/1 · 제목 영어 「LangChain MCP」 | 이름 · `required == ["topic"]` · 「20:00」 · `all(...)`로 두 도구 모두 입력 형식이 있음 |
| 05 | 직접 `@tool` 1 ↔ 메모리 FastMCP 도구 1 ↔ 도구 5(루프 안 정의)를 `MCPAdapter`로 가져와 명세 글자 수(`schema_chars` — 자체 JSON)와 **첫 모델 요청**의 입력·출력 토큰·고른 도구, 예상 비용 | **3**(조건마다 1, `tool_choice="required"`) | 메모리 연결(`MCPAdapter(small)`·`MCPAdapter(large)` — FastMCP 객체), 하위 프로세스 없음 | 없음 | **b4 「같은 158 입력 토큰」·「316 토큰」**(한 번 실행 값을 핵심 개념 본문에 적음) · b7 「2026-09-11 … 단가 가정」 · 출력 `direct_1 289 · mcp_1 216 · mcp_5 1288`·`158/18 · 158/18 · 316/31`·`0.0007755` · b8 「**Ch37**에서는 …」(교재에 없는 챕터) | **측정 8/1** · **직렬화 8/4/1** · **스키마 7/2** · 필터링 3/1 · 토큰화 2 · 수치 2 · 공급자 1/1 · 추정 1 · 실측 0/2/1 · 프로토콜 1 · 반환 2/1 | 도구 5 > 1 글자 수 · 사용량이 있고 도구 요청이 있음 · **모델이 보고한 입력 토큰 5개 > 1개**(서비스 값) · 비용 < 1 |

- **서비스 요청 합계(한 번 실행)**: 01~04 **0** · 05 **3** = **3번**. 임베딩 0. 노트북 `%pip`은 다섯 절 모두 `"langchain[mcp]==1.4.0" langchain-openai==1.6.0 fastmcp==4.0.3 mcp==2.2.0 python-dotenv==1.2.3`(01~04도 `langchain-openai`·`dotenv`를 설치). 실습 폴더 dev에 `pip==26.2`, 잠금에 `pip 26.2` 있음(규격 §7-2 조건 충족).
- **`temperature=0`**: 0곳. **`reasoning_effort="none"`**: 05 한 곳. 모델 이름 `openai:gpt-5.4-mini`.
- **걸린 시간**: 어느 절도 재지 않음. 저장된 셀 기록(참고만): 01 1.0초 · 02 0.9초 · 03 1.4초(stdio 셀 0.89초) · 04 1.4초(0.85초) · 05 4.2초(모델 셀 3.08초).
- **흔들리는 값**: 03·04 결과 출력 속 내용 블록 `id`(`lc_<uuid>` — 인용하면 G5·재실행 대조가 깨짐) · 03 환경 변수 개수(기기) · 05 출력 토큰·고른 도구(도구 다섯 조건)·예상 비용 · 05 입력 토큰(같은 요청이면 같을 가능성이 크나 이번에 확인하지 않음 — §8).
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py` → `textbook/part5/_figure.py`) · 노트북 토큰 `{{notebook:slug}}`(01·04·05)·`|example`·`|failure`(02·03). Mermaid·삽화 0장. 챕터 공개 목록에 옛 SVG 다섯 줄이 **있음**(Ch 27과 다름 — 그림을 바꾸면 목록도).
- 노트북 `metadata.verification`: 다섯 모두 `passed`, 실행일 **2026-09-10**(05 16:09 · 01~04 16:36 UTC). `code_sha256` 앞 12자 01 **`a09d959cecc4`**(묶음 실행 계약 — §5) · 02 `55bbba9402b5` · 03 `2165ed1b94ce` · 04 `aa628c23c529` · 05 `497b3ecd342c`. 셀 수 10·10·12·8·14. 파일은 `part6-practice.zip`·`llm-practice.zip` 안 판과 바이트 같음.
- 노트북 설명 셀: 제목(질문 한 줄) · 「실행 환경 준비」 · 「패키지 버전 확인」 + `_src` b4 「코드 읽기와 비교 경계」와 같은 글(옛 도구가 끼움) · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물(요청 수·비용·시간)·실행일 문장 없음, 셀 첨부 그림 0.
- `_src` 틀(옛 생성기 `qa/author_ch28.py`): b4 「도식 읽기」 색 뜻 문장 · b5 첫 문장(「노트북은 다른 절의 변수에 의존하지 않습니다 …」) · **b8 세 항목이 다섯 절 같음** · **b10 참고 자료 셋이 다섯 절 같음**(스펙 2025-11-25 · FastMCP **v2** 문서 링크 · LangChain MCP, 확인 2026-09-11) · 02·03 b5 「확인할 점」과 b6 첫 단락이 글자까지 같음 · 복습 넷(05는 다섯).

## 2. 절별로 더 봐야 할 것

### 01 MCP 구조와 capability 협상
- **설치판 기본은 옛 핸드셰이크가 아님**: FastMCP 4.0.3 클라이언트 기본 `mode="auto"`는 `server/discover`를 먼저 보내고 **2026-07-28**(요청마다 판 번호·클라이언트 capability를 `_meta`에 싣는 방식)을 고름. 오간 메서드(서버 미들웨어로 기록, 두 번 같음): auto `server/discover → tools/list → resources/list → prompts/list → tools/call → resources/read → prompts/get` ↔ `mode="legacy"` `initialize → notifications/initialized → …`. 지금 b4·복습 1~3과 옛 그림은 legacy만 설명(§6-1).
- **결정적 값 후보(모델 없음, 두 번 같음)**: `client.protocol_version` `2026-07-28`(auto) ↔ `2025-11-25`(legacy) · `client.initialize_result is None` `True` ↔ `False` · `client.server_capabilities`(auto: `extensions`·`logging`·`prompts`·`resources`·`tools`, `listChanged` 모두 `false` / legacy: `listChanged` `true`) · `client.server_info` `{'name': '교육센터 자료실', 'version': '4.0.3'}` · `client.instructions` 「공개된 자료실 규정을 읽기 전용으로 제공합니다.」 · 세 목록 이름 · 세 사용 결과 글.
- **capability는 등록과 무관하게 늘 같음**: 도구만 둔 서버·빈 서버도 `prompts`·`resources`·`tools`를 알림(§6-2). 지금 b4 「서버가 resources capability를 알리지 않았다면 …」 장면은 FastMCP로 보일 수 없음(빈 목록 `[]`만 보임).
- 오간 메서드 목록을 노트북에서 보이려면 서버 미들웨어 **클래스 상속**(`fastmcp.server.middleware.Middleware.on_message`)이 필요 — 규격 조건부(상속이 학습 목표일 때만). 내장 `LoggingMiddleware`는 시각·`duration_ms`가 섞여 결정적이지 않음. → 대안: `protocol_version`·`initialize_result` 비교(상속 없음), 메서드 차례는 소스·설치판 확인으로 그림 회색·「소스 확인:」.
- b3 「Ch6에서 모델·프레임워크·하네스 계층을 구분」: Ch 6 01 계층 지도는 **프롬프트·컨텍스트·하네스·루프**(세 제품을 그 지도에 놓음) — 부분 참. 「Ch19에서 도구 이름·설명·입력 스키마가 모델 선택에 영향」: 부분 참(Ch 19 04는 설명만 바꿈 — Ch 19 요약 §13). 「Ch27에서는 파일시스템과 하위 작업 기능을 …」: 뜻으로 참, 「하위 작업」은 Ch 27 말이 아님(§4-1).
- **묶음 실행 검사 대상**(§5): 01은 키·모델·`dotenv`·하위 프로세스·포트 없이 돌아야 함.

### 02 FastMCP 로컬 서버 제작 (paired)
- Before 판정은 §7. 설치판에서 결정적으로 보이는 등록 효과(모델 없음, `e6_schema.py`): 매개변수 힌트 없음 → 입력 형식 `{"topic": {}}`(아무 값) · 독스트링 없음 → 설명 `None` · 반환 힌트 `-> str` → 출력 형식 `{"result": …}`(`x-fastmcp-wrap-result`)와 결과의 `structured_content` `{'result': '14일'}` · 입력 검사: 인자 없음 → `Missing required argument` · `{"topic": 3}` → `Input should be a valid string` · 없는 키 → `Unexpected keyword argument`(입력 형식 `additionalProperties: false`). Ch 19 「입력 검사 = 도구가 몸통 전에 인자를 봄」과 그대로 이어짐.
- **FastMCP의 도구 오류 기록이 표준 오류로 나감**: 서버 쪽에서 `Error calling tool …` + rich 추적이 찍힘(메모리 연결이면 같은 커널의 표준 오류 — 노트북 출력에 시각·경로가 섞일 수 있음). 결과 읽기 인용과 G5·재실행 대조를 해치지 않게 로그 수준을 낮추거나(`logging.getLogger("fastmcp")`) 오류 장면을 stdio 쪽에 둘지 정해야 함.
- b7 「stdio 서버에서 일반 print를 표준 출력에 쓰면 프로토콜 메시지를 손상할 수 있습니다」: 설치판에서 확인하면 **호출은 성공하고** 클라이언트가 그 줄을 건너뛰며 `Failed to parse JSONRPC message from server` 기록만 남음 — 그것도 네 번 중 세 번만 보임(흔들림). 결함 장면으로 쓰기 어렵고, 문장은 「기록을 남기며 그 줄을 버린다」 정도로 한정해야 참.
- `course_server.py`가 학생이 여는 파일인데 제너레이터 식·f-string·집합·데코레이터 셋이 있음(§0). 규격 §2-7 4번(도구 파일 금지 문법)을 서버 파일에도 적용할지 결정 — 고치면 zip·묶음 실행 검사(01이 이 파일을 읽음)·공개 목록 해시가 함께 바뀜.
- `mcp.run(transport="stdio")`는 **시작 배너와 PyPI 새 판 확인**(`https://pypi.org/pypi/fastmcp/json`, 네트워크)을 표준 오류로 냄 — 이번 확인에서 「Update available: 4.0.10」이 떴음. `show_banner=False`·`FASTMCP_CHECK_FOR_UPDATES` 설정 후보(03·04·06이 stdio로 이 파일을 띄움).

### 03 stdio와 원격 전송·권한 경계 (paired)
- Before 판정은 §7. 설치판 사실(`e3_stdio.py`, 부모에 가짜 변수 `CH28_DEMO_SECRET`를 넣고 서버 도구가 받은 **이름만** 돌려받음):
  - `MCPAdapter(Path("server.py"))`·`env` 없는 설정 → 서버가 받은 이름 **여섯** `HOME·LC_CTYPE·LOGNAME·PATH·SHELL·USER`(MCP SDK `get_default_environment()`, `mcp/client/stdio.py` 40~90행), 가짜 변수 없음.
  - 설정 `"env": dict(os.environ)` → 이름 19개(기기 값), **가짜 변수 있음**(누출 장면이 실제로 생김).
  - 설정 `"env": {"PYTHONUNBUFFERED": "1"}` → 기본 여섯 + 1 = **일곱**(`env`는 기본 위에 **더해짐** — `get_default_environment() | (server.env or {})`, 128행).
- **하위 프로세스 수명**: 기본 `keep_alive=True`라 `async with MCPAdapter(...)`를 벗어나도 서버가 남음(스크립트 안 자식 프로세스 1 → 2 → 3으로 쌓였다가 이벤트 루프가 닫힐 때 0). **노트북은 커널 루프가 계속 살아 있어 셀을 다시 돌릴 때마다 쌓임.** 설정에 `"keep_alive": False`(또는 `PythonStdioTransport(…, keep_alive=False)`)를 주면 블록을 벗어날 때 0(`e9_keepalive.py`). 블록 밖에서 도구를 부르면 그때 다시 띄움(도구가 클라이언트를 쥐고 있음 — `langchain/mcp/adapter.py` 236~238행 독스트링).
- **Streamable HTTP를 노트북에서 띄우는 두 방법**(모두 127.0.0.1, 모델 없음):
  - (가) 같은 루프의 작업 `asyncio.create_task(mcp.run_http_async(host="127.0.0.1", port=…, show_banner=False))` → 연결·도구 목록·호출은 됨. **`cancel()` 뒤에도 듣는 소켓이 남고** uvicorn 수명 주기 추적이 표준 오류에 찍힘(`e4b_listen.py`) — 노트북에서 정리가 깔끔하지 않음.
  - (나) **하위 프로세스** `subprocess.Popen([sys.executable, "-c", "… mcp.run(transport='http', host='127.0.0.1', port=…, show_banner=False)"])` → 연결·호출 → `terminate()`·`wait()` 반환 코드 `-15`, 포트 다시 묶을 수 있음, 자식 0(`e4c_sub.py`). 준비 시도 횟수(4)는 기기마다 달라 출력하지 않아야 함. `Popen`·`terminate`·`wait`는 Ch 23 04가 가르친 모양(`kill`·`wait`).
- **권한 경계를 결정적으로 보이는 방법**(§6-6): `FastMCP(…, auth=StaticTokenVerifier(tokens={…}))` + `@srv.tool(tags={"admin"}, auth=require_scopes("admin"))` → 토큰 없음: 연결 오류(`MCPError`, 날 HTTP 401·`WWW-Authenticate: Bearer`) · 읽기 토큰: 목록 `['lookup_policy']`, 관리 도구 호출 `ToolError: Unknown tool: 'reset_policy'` · 관리 토큰: 둘 다 보이고 호출 됨. 모두 두 번 같음. 원격 전송이 있어야 하므로 (나)와 함께.
- b3 「Ch16에서 허용 목록과 최소 권한을 다뤘고」: Ch 16의 허용 목록은 **출처 표시 허용 목록**(01)이고 「최소 권한」은 Ch 16 원고 0건 — 부분 참. 도구를 권한별로 고르는 선례는 **Ch 19 06 `pick_tools`(읽기 도구·쓰기 도구)**. 「Ch24에서 사람이 승인해야 하는 작업 경계를 확인했습니다」는 참(Ch 24 요약 §15).
- b4 「Streamable HTTP 전송은 하나의 MCP 엔드포인트에 HTTP POST와 선택적인 GET을 사용합니다」: 2025-11-25 기준. **2026-07-28은 GET 끝점·프로토콜 세션(`Mcp-Session-Id`)을 없앰**(POST만, 요청 머리 `MCP-Protocol-Version`·`Mcp-Method`·`Mcp-Name`). 「서버는 요청의 Origin을 검증해야 합니다」·「127.0.0.1에 바인딩」·「stdio 구현은 자격 정보를 환경에서 읽을 수 있습니다」는 2026-07-28에도 참(§15 참고 자료).

### 04 LangChain MCP 클라이언트 연동
- 설치판 `langchain.mcp`(베타 — 가져오면 `LangChainBetaWarning` 한 번): `MCPAdapter(target)` → FastMCP `Client`를 만들어 elicitation 처리(LangGraph `interrupt()`)를 붙임 · 문자열 대상은 `http`/`https` URL만(그 밖은 `ValueError` — `.py` 문자열이 하위 프로세스가 되지 않게, `adapter.py` 84~122행) · `list_tools()`는 매번 `async with self` 안에서 가져와 `as_langchain_tool`로 바꿈.
- **바뀐 도구의 모양(결정적)**: 종류 `StructuredTool` · `args_schema`는 **딕셔너리**(서버 입력 형식 그대로, `additionalProperties: false` 포함) · `response_format="content_and_artifact"` · `metadata={"mcp": {"tool": {"_meta": {"fastmcp": {"tags": ["public", "read"]}}}, "server": {"name": "교육센터 자료실", "version": "4.0.3"}}}` · **`coroutine`만 있음 → `.invoke()`는 `NotImplementedError: StructuredTool does not support sync invocation.`**(동기 그래프 `invoke`도 같은 오류) — MCP 도구를 부르려면 `ainvoke`/`await`가 반드시 필요.
- 도구 요청 모양으로 부르면 `ToolMessage`(`content` 내용 블록 목록 + `artifact={'structured_content': {'result': …}}`, `status='success'`) · 서버 도구가 `ValueError`를 내면 `status='error'`와 서버 오류 글(`handle_tool_error=_handle_mcp_tool_error`, `tools.py` 104~117·274~282행).
- **모델 없는 도구 실행 장면**(Ch 20 01 모양, `e8_toolnode.py`): `StateGraph(MessagesState)`에 `ToolNode(MCP 도구)` 하나 + 손으로 만든 `AIMessage(tool_calls=[…])` → `await graph.ainvoke(...)` → `ToolMessage call_a success …`·`call_b error …`(두 번 같음). `ToolNode`를 그래프 밖에서 바로 부르면 설정 키 오류.
- 출력에 `lc_<uuid>` 블록 id가 섞이므로 결과는 `result[0]["text"]`만 출력.
- 공식 문서의 옮기기 안내: `langchain-mcp-adapters`의 `MultiServerMCPClient` → `MCPAdapter` 하나, `load_mcp_tools()` → `MCPAdapter(...).list_tools()`, **도구 가로채기(interceptor) → LangChain `@wrap_tool_call` 미들웨어**(Ch 22), 프롬프트·리소스는 감싸지 않음. **잠금에 `langchain-mcp-adapters` 없음**(가져오면 `ModuleNotFoundError`) — 지시문이 말한 `MultiServerMCPClient`·`load_mcp_tools`는 이 챕터 잠금 판에서 쓸 수 없음.
- b3 「Ch19에서 @tool로 만든 BaseTool의 name, description, args_schema를 모델에 연결했습니다」: 뜻은 참(Ch 19 04), Ch 19는 `BaseTool`이라는 이름을 안 씀(종류 `StructuredTool`), `args_schema`는 02 — Ch 19 요약 §13.

### 05 도구 정의와 첫 호출 토큰
- 모델 없이 결정적으로 셀 수 있는 것: `model.bind_tools(tools).kwargs["tools"]`(Ch 19 04 모양)를 JSON 글로 바꾼 **명세 글자 수** — 같은 이름·설명이면 직접 도구 **223자** ↔ MCP 도구 **254자**(MCP 쪽은 `additionalProperties: false`가 더 붙음), `tiktoken` `o200k_base`로 세면 70 ↔ 77(참고값 — 제공자가 센 입력 토큰과 같은 값이 아님). Ch 19 03의 `spec_length(tools)`(`convert_to_openai_tool` + `json.dumps(..., ensure_ascii=False)`)가 바로 선례 — 지금 판의 자체 `schema_chars`(이름·설명·`model_json_schema()`)는 모델에 보내는 명세와 다르고(직접 도구 289 ↔ MCP 216으로 **거꾸로** 나옴) 조건 표현식·내포식을 씀.
- 저장 출력 `direct_1`·`mcp_1` 입력 토큰이 **둘 다 158**인데 명세 글자는 다름 → 제공자는 명세를 자기 방식으로 바꿔 세므로 글자 수와 입력 토큰은 다른 값(지금 b4·b7 설명과 맞음). 이 관찰을 결론에 쓰려면 모델 요청이 필요(§8).
- 지금 판 세 조건은 **두 가지가 함께 바뀜**(도구 이름 `direct_lookup` ↔ `lookup_policy`, 도구 수와 설명 글) — b7이 이미 한정. 이름·설명을 같게 두면 「MCP로 바꿔도 명세에 무엇이 더해지는가」만 가를 수 있음.
- `tool_choice="required"`는 과정 처음(Ch 20 「안 씀」 목록) — 쓰면 한 문장. 도구 하나 조건에서 고른 도구는 늘 그 도구(강제), 다섯 조건은 모델 판단.
- 05의 MCP 도구는 **메모리 연결**(FastMCP 객체)이라 「전송 바이트」는 이 셀에 없음 — b4·b7 「MCP JSON-RPC 전송 바이트는 usage_metadata에 포함되지 않습니다」는 참이나 이 절이 잰 값이 아님(재지 않았다고 적어야 함).
- 2026-07-28 부 변경: 서버는 `tools/list`를 **정해진 차례로** 내놓아야 함(SHOULD — 클라이언트 캐시·LLM 프롬프트 캐시 적중률), 목록 결과에 `ttlMs`·`cacheScope` — 도구 정의가 첫 요청 입력에 들어간다는 이 절 주제와 한 줄로 이어짐(실행하지 않음).
- b8 「Ch37에서는 MCP 도구 정의가 계기판의 컨텍스트 지표를 …」: 교재에 Ch 37이 없음(Part 7까지). `labs/part6/continuity-guide.md` 14행도 「Ch37의 비용·컨텍스트 측정」.

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part6/ch28-mcp/
  README.md (절별 키 필요 여부·「실패 진단 JSON」 언급·「어댑터 컨텍스트가 끝날 때 종료합니다」— keep_alive 사실과 어긋남)
  pyproject.toml   uv.lock (134 package 항목, export 133줄)
  course_server.py (읽기 전용 FastMCP 서버 — 도구 lookup_policy·리소스 policy://handbook·프롬프트 explain_policy, 맨 끝 mcp.run(transport="stdio"))
  __pycache__/course_server.cpython-312.pyc (09-10 15:52 — 01·02의 exec_module이 쓴 것으로 보임)
  notebooks/01~05-*.ipynb
  .venv/ (macOS 판 222MB, uv 0.11.6)
  (없음: data/ · runs/ · tests/ · 도구 파일 · 노트북 생성기)
```

- **노트북이 읽는 파일**: `course_server.py`(01·02는 `importlib`로 읽고, 03·04는 stdio로 실행) · 05만 `.env`. **쓰는 파일**: 01·02의 `exec_module`이 남기는 `pyc`(연결 폴더 `__pycache__`)뿐. SQLite 0(Ch 23 연결 폴더 멈춤 문제 해당 없음).
- **서버 파일 찾기**: 지금은 `Path("labs/part6/ch28-mcp/course_server.py")`를 작업 폴더와 그 부모에서 `next(...)`로 찾음 → `run_section.sh`(작업 폴더 = 저장소 맨 위)·학생(`notebooks/`)·묶음 실행 검사(`--cwd lab/notebooks`) 세 자리 모두에서 찾아짐. 금지 모양을 빼면 Ch 10~12 경로 셀(`candidates` + `for`·`break`) 모양으로 **세 자리 모두**에서 확인해야 함(후보 `"../course_server.py"`·`"labs/part6/ch28-mcp/course_server.py"`).
- **stdio 하위 프로세스의 작업 폴더·경로**: `MCPAdapter(Path(...))`는 부모 작업 폴더 기준 상대 경로를 그대로 넘김. 하위 프로세스는 `PYTHONPATH`를 받지 않음(기본 환경 여섯 이름) — 서버 파일이 노트북 폴더의 도구 파일을 가져오게 만들면 멈춤.
- **Ch 28 파일을 코드로 읽는 곳**(`grep -rn`, `textbook`·`labs`, `.venv` 제외):

| 자리 | 무엇을 | 성격 |
|---|---|---|
| `textbook/part6/public-files.json` 73~81행 | README·`course_server.py`·노트북 다섯·잠금 둘 = 9줄 | 묶음 허용 목록 |
| 챕터 `qa/public-files.json` | HTML 여섯(목차 포함)·**옛 SVG 다섯**·실습 파일 아홉 = 20줄 | `collect_public_files.py`가 Part 목록으로 모음 |
| 챕터 `qa/prerequisite-files.json` | **Ch 19 03~06 HTML·노트북 + `orders.csv` + `order_tools.py`**(Ch 19 마감이 더함) | 선행 묶음 — Ch 28 노트북이 코드로 읽지는 않음(`grep` 0) |
| `textbook/downloads/part6-practice.zip`(107항목)·`llm-practice.zip`(455항목) | Ch 28 9파일이 **디스크와 같음** | 묶음 |
| **Part 6 `qa/check_bundle_execution.py` 30~31행** | **Ch 28 01을 키 없이 실행** | **계약(§5)** |
| `textbook/part6/_build_index.py` 26행 · `_notebook/build_index.py` 60~61행 · `build_bundle.py` 26행 | (5, 11, 「MCP 서버와 클라이언트를 연결하고 도구 정의의 입력 토큰을 확인합니다.」) · (절 수 5, 「서버와 클라이언트를 직접 연결하고 도구 정의의 입력 토큰과 권한 경계를 확인합니다.」) · 공개 챕터 목록 | 실습 절을 붙이면 Part 목차 절 여섯(`build_index.py`는 실습 절을 빼고 세는 약속 — 5 그대로) |
| 옛 검사(고치지 않음, 기록만) | `check_scope.py` 13·15행 `EXPECTED` (5,11)·`SECTION_COUNTS` 5(실습 절을 붙이면 5 ≠ 6, 이미 Ch 21에서 멈춤) · `check_notebook_readiness.py`(노트북 47 단언 — 결과 파일을 먼저 씀 → 되돌림 선례) · `check_figures.py`(SVG마다 `.excalidraw` 짝) · `check_visual_reports.py` · `check_delivery.py`(`llm-practice.zip` Part 1 Stale) | Ch 21~27 선례대로 이미 어긋난 상태 |
| 기록만 | `final-artifact-hashes.json` Ch 28 줄 **37 — 15줄은 이미 옛 해시**(HTML 5·`_src` 5·노트북 5, 나머지 22 같음) · `notebook-executions.json`·`notebook-readiness.json`·`figure-consistency.json`(각 5) · `visual-results.json`(12) · `lesson-scope.json`·`prose-repetition-initial.json`(1) · `ch28-technical-review.md`(「개강 전 2026-07 발행 여부 다시 확인」) · `qa/ch28-before-path-repair/`(옛 노트북 01~03 사본) · `language/ch21-ch29-final.*` · Part 7 `existing-artifacts-before.json`(Ch 28 줄)·`before-integration/build_*.py` · `_notebook/checks/notebook-contracts-part6-ch28-mcp.json`·`checks/ch28-mcp/`(옛 화면 검사 PNG 넷·`visual-results.json`) · Ch 27 `before-manifest.json`(Ch 28 줄) · `.moai/…`(옛 계획) | — |

- **옛 생성기**:

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| **`qa/author_ch28.py`**(68,005바이트, `6806d465…`, Ch 28 전용) | `chapter.json`·`_src` 다섯·노트북 다섯(출력 없이) | 564~575행 `main()`이 **`chapter.json`까지 덮어씀**. 548행 `refuse_existing_drafts()`가 대상 파일이 있으면 멈춤(덮어쓰기 막음). 규격 §8대로 01절에서 첫머리 `raise SystemExit(...)`·마감에서 `mv -n` → `qa/upgrade/before/generators/blocked/`. 부르는 스크립트 0(`grep` — Ch 27 `before-manifest.json`만) |
| `figures/_gen_figures.py`(`dadf0c2b…`) | `NN-흐름.{svg,excalidraw,caption.md}` 15개(`textbook/part5/_figure.py`) | 사본 `before/generators/`·`before/figures/` |
| 공용 옛 생성기 | `textbook/part6/_author_ch21_ch29.py`는 **Ch 28 안 씀**(`grep` 0) | — |

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["langchain[mcp]==1.4.0", "langchain-openai==1.6.0", "fastmcp==4.0.3", "mcp==2.2.0", "python-dotenv==1.2.3"]`(**`langgraph`는 직접 고정하지 않음** — 잠금 1.2.11), dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `fastmcp 4.0.3`·`fastmcp-slim 4.0.3`·`mcp 2.2.0`·`mcp-types 2.2.0`·`langchain 1.4.0`(`mcp` 추가 설치 = `fastmcp`)·`langchain-core 1.6.2`·`langchain-openai 1.6.0`·`langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`·`langgraph-checkpoint 4.2.0`·`openai 3.11.0`·`pydantic 2.13.5`·`httpx 0.28.1`·`uvicorn 0.52.4`·`starlette 1.6.0`·`psutil 7.2.2`·`tiktoken 0.14.0`. **`langchain-mcp-adapters`·`numpy`·`deepagents` 없음.** `pyproject.toml`·`uv.lock` 수정 시각 09-10 그대로.
- **Ch 27 잠금과 견줌**: 겹치는 89개 **판 모두 같음**. Ch 28에만 45개(`fastmcp`·`mcp`·`mcp-types`·`uvicorn`·`starlette`·`sse-starlette`·`authlib`·`pyjwt`·`rich`·`cyclopts`·`pydantic-settings`·`keyring` 등), Ch 27에만 12개(`deepagents`·Anthropic·Google 계열). → Ch 27 `harness_tools.py`(가져오기 0)는 이 잠금에서도 import는 되지만, Ch 27 요약 §16-7대로 **파일째 가져오지 말고 함수만 같은 본문으로 옮김**. Ch 21 `runner_tools.py`는 맨 위 `numpy`라 import 자체가 멈춤.
- `mcp` SDK 2.x에서 옛 `mcp.server.fastmcp`는 **없음**(가져오면 「FastMCP was renamed to MCPServer (from mcp.server.mcpserver)」) — 인터넷 예제 대부분(`from mcp.server.fastmcp import FastMCP`)이 이 잠금에서 멈춘다는 사실을 b7에 한 줄 둘 후보. 이 챕터는 별도 패키지 `fastmcp`(4.0.3)를 씀.

## 4. 앞뒤 챕터 이음새

### 4-1. Ch 27 인계(요약 §16·§17, 계약 §3 Ch27 줄) 항목별 지금 상태

| 인계 항목 | 지금 Ch 28 원고·설치판 | 상태 |
|---|---|---|
| 01 b3 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다」 — 뜻으로 참, 「하위 작업」은 Ch 27 말 아님 | 그대로 | **고칠 자리** — Ch 27 말로: 「Ch 27에서는 파일 도구와 서브에이전트 위임을 미리 조립한 Deep Agent(하네스)를 썼습니다」 모양. 「하네스」는 Ch 6 01 뜻 그대로 |
| Ch 27 09 b8 「Ch 28 01절에서는 도구를 같은 프로그램 밖의 서버로 옮겨, 여러 클라이언트가 같은 방식으로 찾게 하는 MCP를 봅니다」(+ 01 슬러그 링크) | 01 b2와 맞음 | **01 슬러그 `01-MCP-구조와-capability-협상` 유지**, 01이 「밖의 서버」·「여러 클라이언트가 같은 방식으로 찾음」을 보임(메모리 연결만 보이면 「밖의 서버」가 약함 — 01에서 stdio까지 가면 묶음 실행 검사 조건과 부딪힘, §5) |
| ① 계약 파일 없음 · 파일은 상태 칸 `files`에만 | Ch 28 코드가 Ch 27 파일을 읽는 곳 0 | 어긋남 없음 |
| ② 사람 승인은 `interrupt_on`·결정 목록·`approve`만, 08 작은 그래프는 reject를 막지 않음 | Ch 28 원고에 Deep Agents 승인 언급 0. 단 **`langchain.mcp`는 서버가 입력을 요구하면 LangGraph `interrupt()`로 사람에게 묻는 elicitation을 기본으로 켬**(`adapter.py` 146~157행) | 새 장면을 넣는다면 Ch 24 `interrupt`·`Command(resume=)`와 이어지나 이번 서버는 입력을 요구하지 않아 실행되지 않음 — 「실행하지 않았습니다」로 |
| ③ 권한 규칙은 파일 도구 안 판정 — MCP 도구에 걸린다고 가정 금지 | 03·05는 서버 쪽 인가·도구 거르기로만 설명(Deep Agents 권한 언급 0) | 참. 권한을 보이면 **FastMCP 서버 쪽**(`auth=`·`require_scopes`·태그 끄기)이나 클라이언트 쪽 도구 거르기(Ch 19 06 `pick_tools`)·`@wrap_tool_call`(Ch 22)로 — Deep Agents `FilesystemPermission`으로 설명하지 말 것 |
| ④ 호출 한도는 invoke마다, 요약 요청은 한도 밖 | Ch 28에 호출 한도 없음(에이전트 실행 0) | 04·06에서 `create_agent`로 MCP 도구를 붙이면 Ch 22 04 `ModelCallLimitMiddleware(run_limit=N, exit_behavior="end")`를 붙이고 `ainvoke` 한 번마다 셈 |
| ⑤ 기본 미들웨어 다섯째는 이 과정 모델에서 하는 일 없음 | 해당 없음(Deep Agent 안 씀) | — |
| ⑥ 웹 검색·스킬·비동기 서브에이전트 실행 0 | Ch 28 원고가 전제하지 않음 | — |
| ⑦ `harness_tools.py`는 Ch 27에서만 | 도구 파일 없음 | 함수만 옮김(§9) |
| ⑧ 말: 「경로」·「반환」·「검증」·「프롬프트」(제목 밖)·「캐시」 단독 등 본문 0 | 「반환」 다섯 절 모두 · 「프롬프트」 01·02(MCP 구성 요소 이름) · 「검증」 03 · 「캐시」 04 · 「경로」 02·03·04 | **고칠 자리**(§10-2) |

### 4-2. 앞 챕터에서 가르친 것 (Ch 28이 전제할 수 있는 것)

| 챕터·절 | 가르친 것 | Ch 28과의 관계 |
|---|---|---|
| Ch 2 07·09·12 | 타입힌트·데코레이터(B만)·`async def`·셀 맨 위 `await`·`gather`·`to_thread`·파일 안 `asyncio.run()` | FastMCP 등록(힌트 → 입력 형식) · MCP 클라이언트 비동기. **`async with`·`ainvoke`는 가르치지 않음** |
| Ch 6 01 | 하네스·계층 지도(프롬프트·컨텍스트·하네스·루프) | 01 b3 대조(§2 01) |
| Ch 6 06 | `estimate_cost`·요금표·「예상 비용」 | 05 비용 |
| Ch 16 01·04 | 출처 표시 허용 목록 · 호출 한도·비용 상한 | 03 b3 「허용 목록」 뜻이 다름 |
| Ch 18 03 | `asyncio.to_thread`+`gather`, 셀 맨 위 `await`를 「노트북 도구(IPython)의 기능」으로 풂(과정 요약 2-10) | **`await` 설명 선례** |
| Ch 19 01~06 | `@tool`(세 문장 + Ch 2 09 링크)·독스트링 = 설명·입력 형식·**입력 검사**·도구 명세 글자 수(`spec_length`, 03)·`bind_tools`·`.kwargs["tools"]`·`tool_calls`·`usage_metadata`(04: 설명 길이에 따른 입력 토큰 177 → 330)·`ToolMessage`·결과 상태·`pick_tools`(읽기/쓰기 도구, 06) | 02 등록·05 명세와 토큰의 직접 선례, 03·05 권한 거르기 선례 |
| Ch 20 01 | 손으로 만든 `AIMessage(tool_calls=…)` + `ToolNode` 그래프 | 04 모델 없는 MCP 도구 실행(§2 04) |
| Ch 21 01 | `create_agent(model, tools=…, system_prompt=…)`(모델 **객체**) | 04·06에서 MCP 도구를 에이전트에 붙일 때 |
| Ch 22 01·02·04 | 훅·기록 훅·호출 한도·`@wrap_tool_call`(감싸기형 도구 훅) | MCP 도구 가로채기 = `@wrap_tool_call`(공식 옮기기 안내) · 요청 셈 |
| Ch 23 04 | `subprocess.Popen`·`kill`·`wait`·신호 파일 | 03 HTTP 서버를 하위 프로세스로 띄우고 끝낼 때 |
| Ch 24 01 | `interrupt`·`Command(resume=)`·승인 지점 | 03 b3(참) · `langchain.mcp` elicitation |
| Ch 27 01·04·06 | Deep Agent·파일 도구·서브에이전트 위임·안전 규칙 | 01 b3 |

### 4-3. 완료 챕터가 Ch 28에 기대는 문장 — 개선 뒤에도 참이어야 함

| 자리 | 문장 | 조건 |
|---|---|---|
| **Ch 27 09 `_src` b8(+ HTML 562행·노트북 09 셀 45·`qa/upgrade/author_09.py` 두 곳)** | 「Ch 28 01절에서는 도구를 같은 프로그램 밖의 서버로 옮겨, 여러 클라이언트가 같은 방식으로 찾게 하는 MCP를 봅니다」 + **01 슬러그 링크** | 01 슬러그 유지 · 01이 「서버로 옮김·같은 방식으로 찾음」을 보임 |
| Ch 19 요약 §13 「Ch 28 MCP」 표(다섯 줄) | 01 b2 참 · 01 b3 부분 참 · 02 b3 「Ch4 타입 힌트」 틀림·「장식자」 → 데코레이터 줄 · 04 b3 `BaseTool` 이름 · 05 b2 명세 글자 수로만 참 · 05 b3 참(**이 장면 때문에 Ch 19 04가 Part 6 선행 목록에 들어감**) | Ch 28 개선 때 맞춤 |
| Ch 24 요약 §15 193행 | 03 b3 「Ch24에서 사람이 승인해야 하는 작업 경계」 참 | — |
| Ch 21~27 요약 · 계약 §5 | 「`check_bundle_execution.py` PASS(Ch 24 01·Ch 28 01)」 · Ch 28 01 `a09d959cecc4…` 4셀 | **01을 바꾸면 이 기록들이 옛 값이 됨**(과거 기록이라 고치지 않고, 새 값은 Ch 28 마감 기록에) |
| `labs/part6/continuity-guide.md` 14행 | 「Ch19의 도구 정의와 호출 비용 \| Ch28 MCP 서버·클라이언트와 도구 정의 토큰 \| Ch37의 비용·컨텍스트 측정」 | 둘째 칸은 지금 원고와 맞음, 셋째 칸 Ch 37은 교재에 없음 — 마감 때 대조(보호 파일, 묶음에 들어감). 19행 「MCP 서버 등 별도 실행이 필요한 구성은 해당 README의 준비 절차」 |
| `textbook/part6/practice-start.md` 15행 · `_src/index.html` | 「Ch 26의 위임, Ch 27의 DeepAgents, Ch 28의 MCP로 연결」 | 참 |
| Ch 6·8·16·19~27 `_src` | Ch 28·MCP 언급은 Ch 27 09 b8뿐(`grep` — 옛 Excalidraw MCP 도구 기록·base64 우연 일치 제외) | — |

### 4-4. 뒤 챕터(대기)·Part·과정 파일이 Ch 28에 기대는 것 — 고치지 않음

- **Ch 29~31·34·Part 7 노트북·코드가 Ch 28 노트북·출력·서버 파일을 읽는 곳: 0**(`grep` — `course_server`·`ch28`·`MCP`). **Part 7 Ch 30 서빙은 Ch 28 서버를 쓰지 않음.** Part 7 선행 목록에 Ch 28 줄 0. → **산출 파일 계약 없음.**
- Ch 29 `_src`에 Ch 28 문장 0. Ch 28 05 b8 「Ch29에서는 최종 답만 보지 않고 도구 선택과 호출 순서를 포함한 실행 궤적을 평가합니다」는 Ch 29 목차 설명(「최종 답변·한 단계의 선택·전체 궤적을 평가」)과 맞음 — 실습 절을 붙이면 이 연결 문장은 06으로 옮겨감.
- `textbook/_notebook/build_index.py` 60~61행 설명 「… 도구 정의의 입력 토큰과 **권한 경계**를 확인합니다」 · Part 6 `_build_index.py` 26행 · `chapter.json` `objectives` 넷(「LangChain 1.4.0 MCPAdapter로 도구를 연결하고 첫 호출 입력 토큰을 측정」·「capability 협상」) — 마감 때 새 본문과 대조.

### 4-5. Part 6 묶음·목록·기록·검사

- Part 6 선행 목록(13줄)에 Ch 28 파일 0 · `existing-artifact-hashes.json` Ch 28 줄 0 · `final-artifact-hashes.json` 37줄(15줄 옛 해시, 기록만).
- 공개 목록 두 곳 + zip 두 개(§3). **묶음 실행 검사 계약 있음 — Ch 28 01**(§5).
- 도구 파일·06 실습 절·서버 파일 변경이 생기면 두 목록·zip·묶음 실행 검사를 함께(Ch 27 마감 모양 — `python3 textbook/part6/_build_index.py`를 마지막에 한 번 → `check_bundle_execution.py`).
- 옛 검사 스크립트(기록만, 고치지 않음): Ch 27 마감 기록대로 넷 모두 Ch 28에 닿기 전에 멈춤. 실습 절을 붙이면 `check_scope.py` `SECTION_COUNTS` 5 ≠ 6. 챕터 공개 목록의 옛 SVG 다섯 줄을 빼면 `check_figures.py`와 무관(이미 Ch 21에서 멈춤).

## 5. 묶음 실행 검사 계약 (Ch 28 01) — 가장 중요

- **스크립트**: `textbook/part6/qa/check_bundle_execution.py`(고치지 않음). `textbook/downloads/part6-practice.zip`을 `tempfile.TemporaryDirectory(prefix='part6-bundle-')`에 풀고, `('ch24-human-in-the-loop', '01-*.ipynb')`·**`('ch28-mcp', '01-*.ipynb')`** 차례로:
  1. zip 속 노트북 `metadata.verification.code_sha256`을 읽음.
  2. 풀린 실습 폴더에서 **`uv sync --locked`**(네트워크 또는 uv 캐시 필요 — 선례 `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink`, `TMPDIR`은 세션 홈 — 맥 마운트 밖).
  3. `uv run --project <lab> --with nbclient==0.11.0 --with python-dotenv==1.2.3 python textbook/_notebook/execute.py <notebook> --cwd <lab>/notebooks --kernel-python <lab>/.venv/bin/python` — **새 커널, 작업 폴더는 풀린 `notebooks/`**, 셀마다 240초 제한, `allow_errors=False`.
  4. `assert after['status'] == 'passed' and after['code_sha256'] == original` → `textbook/part6/qa/bundle-execution.json`에 `archive_sha256`·두 노트북 검증 칸을 **덮어씀**.
- **지금 값**: Ch 28 01 `code_sha256` **`a09d959cecc40a81924daa8ead1b2b69a6738f88b000aab45363f6d250c1687f`**(코드 셀 4) · `bundle-execution.json` **`4f39acac93d1d36cbf9fa7a878bc9124d55a6177c342aa553249a09ce27ab061`** · `part6-practice.zip` **`1a20c73c8dd533cc8e706f4be8ace65ebb6626412dd3a367001a414e50b7eddd`**(Ch 27 마감 값).
- **01이 지켜야 할 조건**(Ch 24 01·Ch 20 03 선례):
  - **키·모델 객체·`dotenv` 셀 없음** — 묶음에는 `.env`가 없음(`execute.py`의 `secret_values`는 가리기 전용). 모델 객체만 만들어도 키 없이 `OpenAIError`(Ch 27 01이 목록에 못 들어간 까닭).
  - **네트워크 없이 끝남** — `%pip install -q …`는 잠금 판이 이미 설치돼 있어 통과(지금 PASS). FastMCP 메모리 연결은 네트워크를 쓰지 않음. **stdio로 `course_server.py`를 띄우면 서버가 시작 배너와 PyPI 새 판 확인을 함**(§2 02) — 01에 넣으려면 `show_banner=False`·새 판 확인 끄기와 하위 프로세스 정리(`keep_alive=False`)를 함께. **HTTP 포트는 넣지 않는 편이 안전**(§2 03 (가) 정리 문제).
  - **작업 폴더가 `notebooks/`여도 서버 파일을 찾음** — 풀린 zip의 `…/labs/part6/ch28-mcp/course_server.py`(묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리 확인, 과정 요약 §3 경로 셀).
  - 도구 파일을 가져오면 그 파일이 zip에 들어가야 함(공개 목록 두 곳). 풀린 `notebooks/`가 작업 폴더라 `from … import …`는 그대로 찾음(`PYTHONPATH` 없이).
  - 파일 쓰기는 풀린 임시 폴더 안(`__pycache__` 등)이면 검사와 무관 — 단 저장소에서 실행할 때 연결 폴더에 `pyc`가 생기는 것은 따로 막을지 결정(§12-8).
  - 출력이 흔들려도 검사는 `code_sha256`만 봄(`outputs_sha256`은 기록만 — Ch 24 마감 때 설치 셀 스트림 나뉨으로 흔들렸음).
- **01을 고치면 해야 할 일**(Ch 24 01 선례 — 마감 때 다시 실행해 새 값): 절 작업 → 공개 목록 → **zip 다시 만들기** → `check_bundle_execution.py` 실행(환경 변수만, 스크립트 수정 0) → PASS 확인 → 새 `code_sha256`·`bundle-execution.json`·zip 해시를 챕터 요약·계약 §5에 적음. **Ch 24 01도 같은 실행에서 다시 PASS해야 함.** 01 준비물·README에 「키 없이 실행됨(묶음 실행 검사 대상)」.
- 01에 모델 장면이 필요하면 **01을 모델 없는 부분과 나누는 것은 불가**(검사는 노트북 전체를 돌림) — 모델 장면은 02 이후로.

## 6. 설치판 동작 — 소스와 모델 없는 확인 (2026-09-28, `fastmcp 4.0.3`·`mcp 2.2.0`·`mcp-types 2.2.0`·`langchain 1.4.0`·`langchain-core 1.6.2`·`langgraph 1.2.11`·`langchain-openai 1.6.0`)

### 6-1. 프로토콜 판과 협상 — **2026-07-28이 나와 있음**
- `mcp_types/version.py`: 알려진 판 `2024-11-05`·`2025-03-26`·`2025-06-18`·`2025-11-25`(**핸드셰이크 판** — `initialize`)·**`2026-07-28`(modern — 요청마다 판 번호를 싣는 상태 없는 방식)**.
- 공식 스펙 2026-07-28(확인 2026-09-28) 변경 요지: **`initialize`/`notifications/initialized` 핸드셰이크 없앰** — 모든 요청이 `_meta`의 `io.modelcontextprotocol/protocolVersion`·`clientCapabilities`를 실음 · 서버는 **`server/discover`**를 반드시 구현(판·capability·서버 정보), 클라이언트는 먼저 불러도 되고 안 불러도 됨 · 판이 안 맞으면 `UnsupportedProtocolVersionError`(`-32022`, 지원 판 목록) · Streamable HTTP의 **프로토콜 세션·GET 끝점 없앰**, 요청 머리 `MCP-Protocol-Version`·`Mcp-Method`·`Mcp-Name` 필수 · `subscriptions/listen` · 서버가 먼저 보내던 요청(sampling·roots·elicitation) → **여러 번 오가는 요청(MRTR, `InputRequiredResult`)** · 결과마다 `resultType` · Roots·Sampling·Logging은 **사용 중단 예고** · `tools/list` 정해진 차례(SHOULD).
- FastMCP 4.0.3 `Client(mode="auto")`(기본): stdio·메모리에서 `server/discover`로 떠보고 modern이면 채택, 아니면 `initialize`로 물러섬(`client.py` 839~889행). `mode="legacy"`는 옛 핸드셰이크 그대로. 같은 서버에 두 모드를 걸면 §2 01 값이 결정적으로 갈림.
- **지금 원고가 기준으로 삼은 판(2025-11-25)과 설치판 기본 동작(2026-07-28)이 다름** → 01 b4·b7·복습·그림, 03 b4, `chapter.json` 목표 「capability 협상」, 챕터 제목 영어 「capability 협상」 모두 판 기준을 정해야 함(§13-1). Part 6 `ch28-technical-review.md` 「개강 전 2026-07 발행 여부 … 다시 확인」의 답이 이것.

### 6-2. capability
- FastMCP 서버는 등록한 것이 없어도 `tools`·`resources`·`prompts`·`logging`을 늘 알림(modern은 여기에 `extensions: {"io.modelcontextprotocol/ui": {}}` — MCP Apps 확장). 빈 서버에 `list_resources()` → `[]`(오류 아님). → 「알리지 않은 기능을 쓰면 안 된다」는 규칙은 FastMCP 서버로 **보일 수 없음**(소스·스펙 문장으로만).
- 클라이언트 capability(요청 `_meta`)를 노트북에서 보이는 간단한 공개 API는 이번에 찾지 못함(`Context`에 `client_capabilities` 없음 — `e10_clientcaps.py`). `MCPAdapter`는 elicitation을 켠 클라이언트를 만듦(소스).

### 6-3. 도구 → LangChain 도구
- §2 04 요지. `MCPAdapter.list_tools(cache_mode="use")` — 목록 캐시는 클라이언트에 `cache=`를 줄 때만(기본 없음). 목록은 연결 시점에 가져온 것.
- 명세: `bind_tools`가 보내는 MCP 도구 명세 = 서버 입력 형식 그대로(`additionalProperties: false`, 칸 차례 `type·additionalProperties·properties·required`) ↔ 직접 `@tool`은 pydantic에서 만든 형식(`title` 빠짐). 같은 이름·설명에서 223자 ↔ 254자.
- `langchain.mcp`가 감싸지 않는 것(공식 옮기기 안내): 프롬프트·리소스 · sampling·roots · WebSocket. → 04·05·06에서 LangChain 쪽으로 넘어가는 것은 **도구뿐**(리소스·프롬프트는 FastMCP `Client`로만).

### 6-4. stdio 하위 프로세스 — 환경·수명
- 환경: §2 03(기본 여섯 이름, `env`는 더해짐, 전체 복사면 누출). `UvStdioTransport` 등 일부 전송은 `os.environ.copy()`를 씀(`stdio.py` 486~492·553~556·615~618행) — `MCPConfig`의 `command` 방식·`Path`는 해당 없음.
- 수명: 기본 `keep_alive=True`(`stdio.py` 64~66·92~95행) → 블록을 벗어나도 남음, 설정 `"keep_alive": False`면 정리. 스펙 2026-07-28 stdio 종료 절차는 「입력 스트림을 닫고 → 기다리고 → 안 끝나면 강제 종료」.
- 서버가 표준 출력에 `print`하면: 호출은 성공, 그 줄은 버려지고 기록만(흔들림, §2 02). 스펙은 「서버는 MCP 메시지가 아닌 것을 표준 출력에 쓰면 안 됨(MUST NOT)」.
- 서버 시작 배너·새 판 확인이 표준 오류로(§2 02). 저장 출력(03·04)에는 표준 오류 흐름이 없었음 — 새 커널 실행에서 다시 확인할 것.

### 6-5. Streamable HTTP
- §2 03 (가)·(나). FastMCP 4.0.3 `run_http_async(…, host_origin_protection=…, allowed_hosts=…, allowed_origins=…)`로 Host·Origin 검사를 켬(기본 `"auto"`). 이번에 날 요청으로 Origin 거절(403)을 깔끔하게 재현하지는 못함(요청 머리를 갖추지 않아 먼저 다른 오류) — 쓰려면 다시 확인.
- 경로 기본 `/mcp`. 클라이언트 쪽은 `MCPAdapter("http://127.0.0.1:포트/mcp")` 또는 토큰을 줄 때 `MCPAdapter(Client(url, auth="토큰"))`.

### 6-6. 권한 경계 구현 방법(설치판에 있는 것)
- **서버 쪽 인증**: `FastMCP(…, auth=StaticTokenVerifier(tokens={토큰: {"client_id": …, "scopes": [...]}}))`(개발·시험용 — 소스 경고 「Never use this in production」) · `JWTVerifier` · OAuth 공급자들(`fastmcp/server/auth/providers/`).
- **서버 쪽 도구별 인가**: `@mcp.tool(auth=require_scopes("admin"))` · `restrict_tag(tag, scopes=[...])` · 태그로 끄기 `server.disable(tags={...})`·`server.enable(tags={...}, only=True)`(생성자의 `include_tags`·`exclude_tags`는 없어짐 — `server.py` 174~175행 안내) · 인가 미들웨어 `AuthMiddleware`. 권한 없는 도구는 **목록에서 빠지고** 부르면 `Unknown tool`(§2 03).
- **클라이언트 쪽**: 도구 목록을 거른 뒤 `bind_tools`(Ch 19 06 `pick_tools` 모양, `metadata["mcp"]["tool"]["_meta"]["fastmcp"]["tags"]`로 태그 읽기 가능) · `@wrap_tool_call`(Ch 22). 클라이언트 거르기는 **보안 경계가 아님**(서버 인가를 대신하지 않음 — 05 b7과 맞음).
- **stdio**: 스펙 「stdio 구현은 이 인가 절차를 따르지 말고(SHOULD NOT) 환경에서 자격 정보를 가져옴」(2026-07-28 그대로) → 하위 프로세스 환경을 좁히는 것이 경계.

### 6-7. 공식 문서와 설치판의 차이 (2026-09-28 확인)
- b10 FastMCP 링크 `gofastmcp.com/v2/servers/server`는 **v2 문서** — 지금 문서는 FastMCP 4.0.x(클라이언트 `mode` 설명 있음, `keep_alive` 기본값 설명은 클라이언트 문서에 없음).
- LangChain MCP 문서: `pip install "langchain[mcp]"`·`langchain[mcp]>=1.4.0`·베타·`Path`는 stdio·문자열은 URL만·「도구가 클라이언트를 쥐어 블록을 벗어나도 쓸 수 있다」 — 설치판과 맞음. 예제 모델 이름은 Anthropic(이 과정은 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` 객체).
- FastMCP 새 판 4.0.10이 있음(배너 안내) — 잠금은 4.0.3.

## 7. paired 절 Before 결함 판정

| 절 | 지금 Before | 실제 결함 장면인가 | After가 그 결함을 고치는가 | 모델 없이 결정적으로 재현되는가 |
|---|---|---|---|---|
| 02 | 데코레이터 없는 일반 함수 → 목록 `[]` + `call_tool` → `ToolError`(`Unknown tool: 'lookup_policy'`) | **부분** — 라이브러리가 실제로 내는 오류이고 「등록을 빠뜨림」은 흔한 실수. 다만 Before 서버에는 함수를 붙일 방법 자체가 없어(서버 객체와 무관한 전역 함수) 결함이라기보다 「아무것도 없는 서버」에 가깝고, `_src`의 오류 이름(`UnknownToolError`)과 「원인 하나」 주장이 틀림 | 등록하면 목록·호출이 됨(참). 단 본문·독스트링도 함께 바뀜 | **예**(두 번 같음) |
| 03 | `dict(os.environ)` 개수와 키 이름 포함 여부 **출력만**(서버를 띄우지 않음) | **아니오** — 결함이 일어나지 않음: 서버에 넘기지 않았고, 저장 출력도 `OPENAI_API_KEY 이름 포함: False`. 설치판 기본은 이미 여섯 이름만 넘김(§6-4) | After 「PATH·PYTHONUNBUFFERED만 전달」은 **사실과 다름**(서버는 일곱 이름을 받음). 고친 것이 없음(Before가 결함을 만들지 않았으므로) | Before 출력 자체는 결정적이나 **기기마다 개수가 다름**(60) |

- **실제 결함 후보(모델 없음·결정적, 이번에 확인)**:
  - 02-A **입력 형식 없는 도구**: Before `@srv.tool` + `def lookup_policy(topic):`(힌트·독스트링 없음) → 목록의 입력 형식 `{"topic": {}}`·설명 `None`, `call_tool(…, {"topic": 3})`이 **몸통까지 들어가** `ToolError: Error calling tool 'lookup_policy': 3`(몸통의 `KeyError`) / After `topic: str` + 독스트링 → 입력 형식 `{"type": "string"}`·설명 있음, 같은 호출이 **몸통 전에** `1 validation error … Input should be a valid string`. Ch 19 「입력 검사」·「설명」과 바로 이어지고 원인이 「힌트·독스트링」 한 묶음. 서버 쪽 오류 기록이 표준 오류로 나오는 점만 처리(§2 02).
  - 02-B **등록 빠뜨림**(지금 판을 고쳐 쓰기): Before·After 본문·독스트링을 같게 두고 데코레이터 줄 하나만 다르게 → 「원인 하나」가 참이 됨. 결함 크기는 작음.
  - 03-A **환경 전체 전달**: 부모에 **가짜 변수 이름**(예 `CH28_DEMO_TOKEN`, 값은 교재용 글)을 넣고, Before 설정 `"env": dict(os.environ)` → 서버 도구가 받은 이름에 그 변수가 **있음**(`True`) / After `env` 없이(또는 필요한 이름만) → **없음**(`False`). 출력은 참·거짓과 이름만(개수는 기기 값이라 빼기). 서버 파일에 이름만 알려 주는 도구가 하나 더 필요(`course_server.py` 변경 또는 절 전용 서버 파일 — 파일 자리 결정).
  - 03-B **원격 서버 인증 없음**: Before 토큰 검사 없는 HTTP 서버 → 아무 클라이언트나 관리 도구 목록·호출 / After `StaticTokenVerifier` + `require_scopes("admin")` → 토큰 없으면 연결 거절, 읽기 토큰이면 관리 도구가 목록에 없음. 하위 프로세스·포트(§2 03 (나)) 필요, 셀 시간 수 초.
- 색: Before 결함 결과는 빨강(규격 §5-3·과정 요약 §8 — paired Before만).

## 8. 모델·비용 선택지와 흔들림 처리 (결정하지 않음 — 장단점만)

### 8-1. 모델 없이 결정적으로 보일 수 있는 것
- 01: 판 번호·capability·서버 정보·안내 글(auto ↔ legacy), 세 목록과 세 사용 결과.
- 02: 등록 전후 목록·입력 형식·설명·입력 검사 오류·출력 형식.
- 03: 하위 프로세스가 받은 환경 이름(참·거짓), `keep_alive` 켬·끔, HTTP 토큰 없음·읽기·관리 토큰의 목록과 호출 결과.
- 04: 바뀐 도구의 종류·입력 형식·메타데이터·`invoke` 불가(`NotImplementedError`)·`ToolNode` 그래프의 `success`/`error`.
- 05: 명세 글자 수(직접 ↔ MCP ↔ 도구 다섯), 명세에 더해진 칸.
- 모델이 있어야 보이는 것: 제공자가 센 **입력 토큰**(05 핵심), 모델이 MCP 도구를 **고르는** 장면(04·06), 에이전트가 MCP 도구 결과를 받아 답을 쓰는 장면.

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **M1 모델 없음** | 다섯 절 모두 위 구조만, 05는 명세 글자 수까지 | 결정적 · 비용 0 · 흔들림 0 · 키 셀 0 | `chapter.json` 목표 「첫 호출 입력 토큰을 측정」·05 제목과 어긋남 · 「LangChain 연동」이 모델 없이 끝남 |
| **M2′ 05만 모델** | 01~04 모델 없음, 05 앞 절반 명세 글자 수 + 뒤 절반 요청 3번 | 지금 설계와 가장 가까움 · 요청 최소 · 01~04 결정적 | 04 「LangChain 클라이언트 연동」이 에이전트 없이 끝남 |
| **M2 04·05 뒤 절반 모델**(Ch 25·26·27 틀) | 04 앞 절반 변환·`ToolNode` 그래프 + 뒤 절반 `create_agent(model, tools=MCP 도구)` `ainvoke`(요청 2) · 05 요청 3 | 04가 제목대로 모델까지 이어짐 · 구조 값은 결론·그림에 | `ainvoke`·호출 한도 등 새 이름 · 셀 수 늘어남(§2-7 「코드를 늘려 가면서 개선할 필요는 없다」) |
| **M3 모델 중심** | 02~05 모두 에이전트 실행 | 문서 예와 가까움 | 흔들림 최대 · 요청 최대 · 결정적 결함 장면(02·03)이 모델 판단에 기대게 됨 |

### 8-2. 흔들리는 값과 처리
- **흔들리는 값**: 출력 토큰 · 도구 다섯 조건에서 고른 도구 · 답 글 · 예상 비용 · (확인 전) 입력 토큰 · 결과 내용 블록 `id` · stdio 시작 배너·새 판 안내 · HTTP 준비 시도 횟수 · 환경 변수 개수.
- **입력 토큰**: 같은 요청(같은 메시지·같은 명세)이면 같을 가능성이 큼(과정 선례 Ch 8 06 「입력 토큰 수는 같음」) — **이번에 확인하지 않음**(모델 요청 금지). 결론(「직접 1 = MCP 1」·「5 > 1」)에 쓰려면 `05-probe.md` §0에 판단 규칙·그림 라벨 규칙을 **첫 요청 전에** 적고 노트북 밖 5번 + 새 커널 두 번(규격 §2-7 10번 끝, Ch 25·26 선례).
- **규격 §2-7 9번 끝**: 결론·그림 라벨·캡션·정리·복습에는 새 커널 두 번 모두 같은 값과 구조 값만. 출력 토큰·비용·고른 도구는 결과 읽기 둘째 단락·본문 표·「확인할 점」·b7에만 「이번 실행에서는」. 지금 b4처럼 핵심 개념에 158·316을 박아 두지 않음.
- **흔들림을 구조로 줄이는 방법**: 조건마다 도구 이름·설명을 같게(비교 변수 하나) · `tool_choice`로 강제(고른 도구 흔들림 제거, 새 이름 한 문장) · 결론을 「명세 글자 수 차이」(결정적)와 「입력 토큰 차이」(확인 뒤)로 나눔.

### 8-3. 서비스 요청·비용 어림 (요금표 2026-09-17 mini 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰 — 청구 금액 아님)
- **요청 하나의 크기**: 05 저장 출력 입력 158~316·출력 18~31토큰 → 요청당 약 0.0002~0.0004달러(지금 판 세 요청 합 `0.0007755`). 04 에이전트(도구 명세 + 시스템 메시지 + 도구 결과)는 요청당 입력 300~600토큰 어림 → 약 0.0005달러.
- **노트북 한 번**: M2′ 3번 · M2 5번(04 2 + 05 3) · **06 실습 절** 3~5번(규격 §7-2).
- **절별 누적(새 커널 두 번 + 노트북 밖 흔들림 확인 다섯 번 + 개발 시도)**: 05 ≈ 6 + 15 + 10 = 약 30요청 ≈ **0.01달러 안** · 04(M2) ≈ 4 + 10 + 10 = 약 25요청 ≈ 0.015달러 · 06 ≈ 10 + 25 + 10 = 약 45요청 ≈ 0.03달러. **절마다 1달러 안**, 챕터 전체 **약 60~100요청 · 0.02~0.06달러**. 임베딩 0. 삽화 약 12크레딧(여섯 장, 재생성 1회씩이면 최대 24).
- **실행 시간**: 저장 기록으로 절마다 5초 안. stdio 셀은 하위 프로세스 시작에 1초 안팎, HTTP 하위 프로세스 준비 수 초 — 셸 180초 안에 여유.

## 9. §2-7 판단 근거 — 도구 파일

### 사실
- 지금 다섯 노트북이 되풀이하는 코드: 판 확인 준비 셀(다섯 절 같은 글) · 서버 파일 찾기 + `importlib` 읽기(01·02 두 번, 03·04 찾기만) · 세 목록 이름 출력(01·02) · `MCPAdapter`로 도구 가져오기(03·04·05 — `load_mcp_tools`, 05는 함수로) · 결과 글 꺼내기(03·04 — 지금은 `str(result)` 통째).
- 개선하면 절 사이에 되풀이될 후보: **서버 파일 위치 찾기**(01~06) · **MCP 도구 가져오기**(`async def` — 04·05·06) · 결과 내용 블록의 글만 꺼내기(03·04·06) · 도구 명세 글자 수 **Ch 19 03 `spec_length`**(05·06) · **Ch 19 04·05 `tool_call_names`·`sum_usage`**, **Ch 6 06 `estimate_cost`**(05·06 — Ch 21·26·27 도구 파일과 같은 본문) · Ch 19 06 `show_messages`(04·06 에이전트를 쓰면) · 이 챕터 새 함수(환경 이름 비교, 세 목록 이름).
- **비동기 함수를 도구 파일에 둘 수 있는가**: 규격 §2-7 4번은 금지 문법(내포식·`lambda` 등)만 막음. `async def`는 L7 조건(라이브러리가 비동기만 제공)에 맞음 — 부르는 쪽은 여전히 `await`. 처음 가르친 절에서는 노트북에 적고 다음 절부터 가져옴(§2-7 3번).
- **서버 파일과 도구 파일의 관계**: `course_server.py`는 학생이 여는 **서버**(stdio로 실행되는 스크립트, 실습 폴더 맨 위, 공개 목록·zip·묶음 실행 검사 01이 읽음). 도구 파일은 **클라이언트 쪽 도움 함수**(`notebooks/`). 서버 파일이 도구 파일을 가져오면 stdio 하위 프로세스에서 멈춤(`PYTHONPATH` 없음) — 둘은 섞지 않는 편이 안전. 서버 파일을 `notebooks/`로 옮기면 `import course_server`가 세 자리 모두 되지만 공개 목록·zip·01 경로·README·05 설명이 함께 바뀜.
- **앞 챕터 도구 파일은 파일째 가져오지 않음**: Ch 27 `harness_tools.py`(import는 되나 요약 §16-7) · Ch 21 `runner_tools.py`(`numpy` 없음 → import 멈춤) · Ch 19 `order_tools.py`(`pandas` 없음). 쓸 함수만 같은 본문으로 옮기고 `# Ch N MM절에서 배웠습니다`.
- 과정의 도구 파일 이름(`find labs -name '*_tools.py'` + `guardrails.py`): `git_tools`·`data_tools`·`llm_tools`·`rag_tools`·`guardrails`·`agent_tools`·`workflow_tools`·`order_tools`·`graph_tools`·`runner_tools`·`checkpoint_tools`·`approval_tools`·`stream_tools`·`delegation_tools`·`harness_tools`. **안 겹치는 후보**: `mcp_tools.py`(겹치지 않으나 **「MCP 도구」(서버 도구)와 헷갈림**) · `connect_tools.py`(연결 — 챕터 소재) · `protocol_tools.py`(「프로토콜」 금지어 처리와 얽힘) · `bridge_tools.py`.
- 교훈(Ch 24 A-10·Ch 25~27 첫 판부터): 앞 절 생성기가 뒤 절이 함수를 더한 도구 파일을 덮어쓰지 않게 `strip_later_imports`·판마다 해시 대조·쓰기 가드 · 머리 설명 첫 줄을 「앞 챕터와 이 챕터에서 배운 함수」로.

### 선택지 (결정하지 않음 — 장단점만)

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 도구 파일 없음 | 절마다 노트북에 | 목록·zip 변경 없음 · 묶음 실행 검사 01에 새 파일 의존 없음 | 05·06이 Ch 6·19 함수(`estimate_cost`·`sum_usage`·`spec_length`)를 다시 적으면 §2-7 3번과 충돌 |
| B. 앞 챕터 함수만 | `spec_length`(Ch 19 03)·`tool_call_names`·`sum_usage`(Ch 19)·`estimate_cost`(Ch 6) — Ch 21/27 판 글자 그대로, import 0(`spec_length`만 `json`·`convert_to_openai_tool`) | §2-7 3번을 지킴 · 비동기 없음 · 01은 가져오지 않아도 됨 | 01~04가 거의 안 씀(05·06만) |
| C. B + 이 챕터 함수 | 서버 파일 찾기 · MCP 도구 가져오기(`async def`, `keep_alive=False` 설정 포함) · 결과 글 꺼내기 · 세 목록 이름 | 03~06 코드가 가장 짧음 · 하위 프로세스 정리 규칙을 한 곳에 | 처음 가르친 절은 노트북에 남아 판이 둘 · `async def`를 도구 파일에 숨김 · 01이 가져오면 묶음 실행 검사가 그 파일에 기댐 |

## 10. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 10-1. `async`/`await` (L7: 비동기가 학습 목표이거나 라이브러리가 비동기만 제공할 때)
- **사실**: FastMCP `Client`·`MCPAdapter`·MCP 도구 호출은 비동기만 제공(`invoke` → `NotImplementedError`, 동기 그래프 `invoke`도 같음). 노트북은 커널 루프가 이미 돌아 셀에서 `asyncio.run()`을 쓰면 `RuntimeError`(파일 안 `asyncio.run()`만 Ch 2 12가 가르침). 잠금에 `nest-asyncio2`가 있으나 과정 밖 이름. → **L7 조건 충족, 비동기는 피할 수 없음.**
- Ch 2 12가 가르친 것: `async def`(힌트 포함)·셀 맨 위 `await`·`gather`·`to_thread`. 가르치지 않은 것: **`async with`**(비동기 `with` — Ch 2 05 `with open`에 이어 한 문장) · `ainvoke`(Ch 30 옛 판만) · `async` 컨텍스트 관리자의 정리 시점.

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 셀 맨 위 `await` + `async with` | `async with MCPAdapter(...) as adapter:` 다음 줄 `tools = await adapter.list_tools()`를 셀에 바로 | 코드 가장 짧음 · Ch 18 03 설명 문장(「셀 맨 위에 await 줄을 바로 쓰는 것은 노트북 도구(IPython)의 기능」) 재사용 | `async with`를 한 문장으로 새로 풂 · 셀 밖 파이썬 파일에서는 그대로 안 됨(b7 한 줄) |
| B. `async def` 함수에 감싸 부름(지금 모양, 힌트 뺌) | 정의 셀 + 호출 셀(`result = await load_and_call()`) | Ch 2 12 모양 그대로 · 셀당 함수 하나 규칙과 맞음 | 셀 수 늘어남 · 함수 안에서도 `async with` 필요 |
| C. 도구 파일에 `async def`를 두고 가져옴 | `tools = await load_tools(target)` 한 줄 | 노트북에서 `async with`가 한 번만 보임 | 처음 가르치는 절은 노트북에 적어야 함 · 도구 파일이 비동기를 숨김 |
| D. 비동기를 피함 | 불가(위 사실) | — | — |

- 어느 쪽이든: MCP 도구 호출은 `await 도구.ainvoke(…)` 또는 `await graph.ainvoke(…)`/`await agent.ainvoke(…)` — 「`ainvoke`는 `invoke`의 비동기 판」 한 문장. 05의 모델 요청 `model.bind_tools(…).invoke(…)`는 동기로 됨(도구를 실행하지 않으므로).

### 10-2. 용어
- **「프롬프트」**(과정 금지어 — Ch 15~27 「제목에만」): MCP 구성 요소 이름 prompts. (가) 「프롬프트(prompts) — MCP의 구성 요소 이름」으로만 쓰고 Ch 7·15의 말과 다르다고 한 문장 / (나) 「메시지 틀(prompts)」처럼 한국어 이름 + 원어 한 번(지금 b4의 「재사용 메시지 틀」과 이어짐) — 코드 이름(`@mcp.prompt`·`get_prompt`)과 멀어짐.
- **「프로토콜」**: 챕터 제목 말. 새 용어로 뜻(「두 프로그램이 주고받는 메시지 약속」) → 일상 예 → 코드에서 보이는 모습으로 정의(규격 §4 세 문장) 또는 「통신 약속」.
- **「capability」**(01 제목·본문): 「지원 기능(capability)」·「기능 알림」 후보. 2026-07-28에서는 「협상」이 요청마다 판·기능을 싣는 모양으로 바뀜 → 제목 「capability 협상」 자체가 설치판과 어긋날 수 있음(강사 확인).
- 그 밖 금지어 → 대체어: 반환 → 내놓다 · 스키마 → 입력 형식(Ch 19)·출력 형식 · 직렬화 → JSON 글로 바꾸기 · 측정 → 재다·세다 · 검증 → 검사·확인(Ch 16) · 인터페이스 → 부르는 모양 · 인스턴스 → 객체 · 장식자 → 데코레이터 줄(Ch 19) · 사전 → 딕셔너리 · 엔드포인트 → MCP 주소 · 바인딩 → 묶기(「127.0.0.1에만 묶기」) · 필터링 → 거르기 · 공급자 → 제공자 · 캐시 단독 → 「목록 캐시」 등 한정어 · 로그 → 기록 · 지연 → 걸린 초 · 경로 → 파일 위치(Ch 27) · 세션 → (2026-07-28에서 없어짐 — 옛 판 설명에만) · 인터셉터 → `@wrap_tool_call` 훅(Ch 22) · 표면·위장·수치·실측 → 뺌 · 「하위 작업」 → 서브에이전트 위임(Ch 27).
- **한도 말 셋**(Ch 26 요약): 실행 한도·호출 한도·바퀴 한도 — 04·06에서 에이전트를 쓰면 섞지 않음.
- 새 말 후보(절 meta와 맞출 것): MCP·서버·클라이언트·호스트·도구/리소스/프롬프트(구성 요소)·서버 알림 글(instructions)·판 번호(protocol version)·전송(stdio·Streamable HTTP)·하위 프로세스·인증·인가·어댑터·도구 명세.

### 10-3. 파일 쓰기 자리
- 지금 판: 01·02 `exec_module`이 실습 폴더(연결 폴더)에 `pyc`를 씀. 그 밖 쓰기 0. 규격·선례(Ch 23·24·27)는 **쓰기는 임시 폴더**.
- 03-A처럼 절 전용 서버 파일이 필요하면 (가) `course_server.py`에 도구를 더함(묶음 실행 검사 01·zip·공개 목록 해시가 바뀜) / (나) 절 노트북이 임시 폴더에 서버 파일을 **써서** 띄움(Ch 23 04 worker 모양 — 「파일 쓰기」는 `"""…"""` + `with open`) / (다) 실습 폴더에 서버 파일을 더 둠(공개 목록 추가).
- `pyc`를 막으려면: `importlib` 대신 서버 파일을 가져오는 다른 모양(모듈 가져오기 + `sys.dont_write_bytecode`는 과정 밖) 또는 stdio로만 연결. 결정 필요(작은 일이나 연결 폴더 쓰기).

### 10-4. 제목·슬러그
- 챕터 「MCP — Model Context Protocol」(영어) · 01 「MCP 구조와 capability 협상」 · 02 「FastMCP 로컬 서버 제작」 · 03 「stdio와 원격 전송·권한 경계」 · 04 「LangChain MCP 클라이언트 연동」 · 05 「도구 정의와 첫 호출 토큰」. **01 슬러그는 Ch 27 09 b8 링크로 고정.** 02~05 슬러그는 Part 6 목차(다시 만들어짐)·공개 목록·옛 기록 파일만 적음 → 바꿀 수 있음(강사 확인). 선례대로 「제목에만 남음(강사 확인)」 + 본문 첫 자리 풀이가 가장 작은 변경.

### 10-5. 문법·셀 모양
- `@mcp.tool`·`@mcp.resource(...)`·`@mcp.prompt`·`@tool`: 처음 쓰는 자리마다 「이 줄은 아래 함수를 ○○로 등록합니다」(규격 §2-2 L6) + Ch 2 09 링크(A 트랙). FastMCP는 **매개변수 힌트가 입력 형식을 만드는 것이 학습 내용**이라 `: str` 힌트는 필수, 반환 힌트 `-> str`은 출력 형식을 만듦(`x-fastmcp-wrap-result`) — 쓸지 결정(Ch 19는 반환 힌트 안 가르침, Ch 22 도구 반환 힌트는 인계 사항).
- `next(...)`·별표 풀기·f-string·내포식·`isinstance`·`.get`·`all`·`sum`·`sorted` 없이(Ch 27 「쓰지 않은 것」) · 반환 힌트 튜플 없이 · 05 c7의 루프 안 정의 대신 함수 다섯 셀 또는 한 함수를 `large.tool(함수, name=…, description=…)`로 이름만 바꿔 등록(메서드 호출 — 루프 안 정의 없음) · 준비 네 셀 · 모델 셀 `nbkit.key_and_model_cells()`.
- `assert`: 모델이 보고한 토큰(05 `mcp_5 > mcp_1`)·모델이 고른 도구에 걸지 않음(흔들림 확인 전) · 만든 대로 늘 참인 `assert`(03 두 곳) 빼기 · 구조 값(목록 이름·판 번호·`status`·참거짓)에만.
- 결과 출력은 내용 블록 `id`가 섞이지 않게 글만.

## 11. 삽화 비유 계열 후보

**이미 쓴 계열**(계약 20행·과정 요약 §5·Ch 22~27 요약): Ch 3 창고 선반 · Ch 4 쟁반·카드 상자·서류철 · Ch 5 나무 쟁반·블록 · Ch 6 도서관 상담 창구(쟁반 = 하네스)·우편함·구슬·나무 레일·저울 · Ch 7·8 한 책상 색 약속 · Ch 10 도막 · Ch 11 흰 카드/색 딱지 · Ch 13 작업대·갈림길 나무 길 · Ch 14 나무판·마개 · Ch 15 사과·저울·바구니·모래시계 · Ch 16 쪽지·도장·개찰구·체 · Ch 17 눈 위 발자국 · Ch 18 도자기 가마·물레 · Ch 19 식당 주문 전표와 내주는 창 · Ch 20 자료실 승강 상자 · Ch 21 세탁기 · Ch 22 공항 검사·우편 가림막·전화 연결·방문자 명부·두 겹 봉투·서류함·메모 정리 책상 · Ch 23 체스판·즉석사진 · Ch 24 도미노 줄·비워 둔 자리 · Ch 25 대나무 홈통·물방울 · Ch 26 항구 예인선·바지선 · Ch 27 온실과 모종판(**02-5에 플러그 둘**, 08-6 자물쇠 문, 호스). 선례: 사람·손·동물·화면·글자·숫자·시계·화살표 없음. 지금 Ch 28 원고의 말 비유: 01 호텔 안내 데스크 · 02 게시판 · 03 전용 통로 · 04 플러그 변환기 · 05 메뉴판(모두 삽화 없음).

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. 규격 소켓 판과 끼우는 모듈** | 01 같은 모양 소켓이 줄지은 판에 모양이 다른 모듈 셋(도구·리소스·프롬프트 — 톱니·책·빈 틀 모양)이 같은 플러그로 꽂힘, 모듈 옆면 작은 표시등 칸(알린 기능) · 02 판 밖에 놓인 모듈(등록 안 함) ↔ 꽂힌 모듈 · 03 판 바로 옆 짧은 선(가까운 연결) ↔ 벽 구멍 너머로 이어진 긴 선과 덮개 달린 소켓(먼 연결·인가) · 04 모양이 다른 판에 끼우는 변환 어댑터 · 05 꽂힌 모듈 수만큼 길어지는 띠 | 「같은 규격으로 여러 기기를 잇는다」가 MCP 뜻과 가장 가까움 · 발견·등록·연결·변환이 한 판에서 읽힘 | Ch 27 02-5 플러그 둘·Ch 22 전화 연결과 소재가 가까움 · 화면 없는 모듈로 그려야 함(「no screens」) · 전선이 화살표로 읽히지 않게 |
| **B. 목공 드릴과 교환 비트 상자** | 01 뚜껑 안쪽에 비트 모양 홈이 찍힌 상자(무엇이 있는지 알림) · 02 상자 밖에 굴러다니는 비트 ↔ 홈에 끼운 비트 · 03 손 닿는 비트 상자 ↔ 벽 공구함의 잠긴 칸 · 04 규격이 다른 드릴에 끼우는 변환 척 · 05 칸이 늘수록 무거워 보이는 상자 | 「같은 육각 규격이면 어느 비트든 끼운다」가 선명 · 잠긴 칸으로 인가 | Ch 13 작업대·Ch 27 후보 B(공구 벽, 채택 안 됨)와 공구 계열 가까움 · 공구가 많으면 무관 요소 |
| **C. 우주 정거장 도킹 포트** | 01 규격이 같은 도킹 고리 둘이 마주 보는 장면(처음 만나 맞는지 확인) · 02 포트가 닫힌 모듈 ↔ 열린 포트 · 03 붙어 있는 모듈(가까운) ↔ 멀리 떠 있는 모듈과 닫힌 해치(먼·인가) · 04 모양이 다른 두 고리를 잇는 어댑터 링 | 운송·공구·식물 계열 0건 · 「규격 맞물림」과 「처음 만나 가능한 것을 확인」이 가장 잘 읽힘 | 우주 배경이 콘셉트 과해 보일 수 있음(평범한 발표 톤 선호) · 별·행성 등 무관 요소를 「no stars, no planets」로 빼야 함 · 먼 연결을 화살표 없이 보이기 어려움 |
| **D. 열쇠 꾸러미와 자물쇠 판**(권한 절 한정) | 03·06 판에 달린 자물쇠 여럿 중 꾸러미 열쇠로 열리는 것만 열린 상태(인가) · 01 열쇠 구멍 모양 목록(알린 기능) | 「인증 = 열쇠가 있음, 인가 = 어느 자물쇠가 열리나」가 한 장에 | Ch 27 08-6 자물쇠 문·Ch 16 개찰구와 겹침 — 한 계열 전체로는 약함, A·B·C와 섞어 03에만 |

- 스타일 문구는 규격 §5-4 그대로. 크레딧: 절마다 1장(01~06) 약 12크레딧, 재생성 1회씩이면 최대 24.

## 12. 위험과 깨진 것

1. **판 기준 어긋남** — 원고는 2025-11-25(`initialize` 핸드셰이크·HTTP GET·세션)를, 설치판 기본은 2026-07-28(`server/discover`·요청마다 판 번호·세션 없음)을 따름. 01 b7 「최신 발행 스펙은 2025-11-25」는 지금 틀림.
2. **paired Before가 결함을 만들지 않음** — 03 Before는 서버를 띄우지 않고 저장 출력이 「키 이름 포함: False」 · After 설명(두 이름만 전달)이 사실과 다름 · 02 오류 이름·「원인 하나」 틀림(§7).
3. **묶음 실행 검사 계약** — 01을 고치면 zip·`check_bundle_execution.py`·`bundle-execution.json`을 다시(§5). 01에 키·모델·`dotenv`·하위 프로세스(배너·새 판 확인 네트워크)·포트를 넣으면 멈추거나 흔들림.
4. **하위 프로세스가 남음** — stdio 기본 `keep_alive=True`로 노트북 셀을 다시 돌릴 때마다 서버가 쌓임(커널을 끝내야 정리). HTTP를 같은 루프 작업으로 띄우면 `cancel()` 뒤에도 듣는 소켓이 남음. 하위 프로세스 HTTP는 `terminate`·`wait`로 정리됨.
5. **비동기 문법** — `async with`·`ainvoke` 과정 처음, `invoke`는 MCP 도구에서 `NotImplementedError`(§10-1).
6. **흔들리는 출력** — 결과 내용 블록 `id`(`lc_<uuid>`) · 환경 변수 개수 · stdio 배너·새 판 안내·서버 오류 기록(rich, 시각)이 표준 오류로 · 표준 출력 `print` 기록이 네 번 중 세 번만 · 05 출력 토큰·고른 도구·비용 · (확인 전) 입력 토큰.
7. **모델 의존** — 05 핵심 관찰(직접 = MCP 입력 토큰, 다섯 > 하나)이 서비스 값. 흔들림 확인 전에는 결론·그림 라벨에 못 씀. 05 `temperature` 누락(G4), 모델 값 `assert`.
8. **파일 쓰기 자리** — 01·02 `exec_module`이 연결 폴더 `__pycache__`에 `pyc`(연결 폴더 삭제 막힘 — 쌓이기만 함). 03-A처럼 서버 파일을 늘리면 자리 결정.
9. **서비스 요청·비용** — 작음(챕터 약 0.02~0.06달러). 04·06에서 에이전트를 쓰면 호출 한도(Ch 22 04)를 붙이고 `ainvoke`마다 셈.
10. **네트워크** — stdio로 띄운 FastMCP 서버가 시작마다 PyPI에 새 판을 물음(오프라인이면 기다림 여부 확인 안 함). 묶음 실행 검사는 `uv sync --locked`에 네트워크·캐시 필요.
11. **설명과 설치판 차이** — `langchain-mcp-adapters`(`MultiServerMCPClient`·`load_mcp_tools`)는 잠금에 없음 · `mcp.server.fastmcp` 없음(`MCPServer`로 바뀜) · FastMCP 문서 링크 v2 · 「print가 프로토콜을 손상」은 설치판에서 호출 실패로 안 나타남 · capability를 알리지 않는 FastMCP 서버는 만들 수 없음.
12. **용어** — 「프롬프트」(MCP 구성 요소)·「프로토콜」·「capability」·「반환」·「스키마」·「직렬화」·「측정」·「인터페이스」·「장식자」·「하위 작업」 등(§10-2) · 제목 영어 넷.
13. **손 값** — 05 b4 158·316 · 01·05 날짜 2026-09-11 · 02 `UnknownToolError` · `qa/verification.md` 「모든 함수 인자·반환 타입을 표시」·「최대 셀 길이는 24줄」 · `집필점검표.md` 「코드 셀 25줄 이하」(옛 규칙) · README 「어댑터 컨텍스트가 끝날 때 종료합니다」(keep_alive와 어긋남)·「실패 진단 JSON」(없는 파일).
14. **앞 챕터 문장 대조** — 01 b3 Ch 6 계층·Ch 19 선택·Ch 27 하위 작업 · 02 b3 Ch 4 타입 힌트 · 03 b3 Ch 16 최소 권한 · 04 b3 `BaseTool` · 05 b2 선택 정보(§2·§4).
15. **뒤 챕터 계약** — 파일 계약 없음(Ch 29~31·34·Part 7 코드가 Ch 28 파일을 안 읽음). 문장만: Ch 27 09 b8(01 슬러그·「밖의 서버」) · `continuity-guide.md` 14행(Ch 37) · 목차 설명 둘.
16. **옛 생성기** — `qa/author_ch28.py`는 `chapter.json`까지 덮어쓰는 `main()`이 있음(대상 파일이 있으면 스스로 멈추지만 규격 §8대로 막고 옮길 대상). `figures/_gen_figures.py`도 같음.
17. **기기 디스크** — 루트 여유 **2.2G(작업 전후 같음)**, `/sessions` **832M(전후 같음)**. 가상환경 300MB는 사용자 디스크(`$ROOT/.cache/vm`)에, 기기 `/tmp/ch28-prep` 124KB. 새 커널 실행(`run_section.sh`)은 `.cache/vm/venv-ch28-mcp`를 자동으로 씀. 묶음 실행 검사는 풀린 폴더(`TMPDIR` = 세션 홈, 여유 832M)에서 `uv sync --locked`로 `.venv`를 만듦 — 선례의 `UV_LINK_MODE=symlink`면 캐시(사용자 디스크 `.cache/vm/bundle-check/uv-cache`)로의 링크라 작고, 링크 모드를 빼면 약 300MB라 Ch 24 01 환경과 합쳐 빠듯할 수 있음 — 실행 전 여유 확인.

## 13. 01절 작업자가 먼저 결정해야 할 것

1. **프로토콜 판 기준(§6-1)** — 2026-07-28(설치판 기본 `auto` — `server/discover`, 요청마다 판 번호·capability, 세션 없음)을 본문 기준으로 다시 쓸지, 2025-11-25 핸드셰이크를 `mode="legacy"` 비교(결정적 값: 판 번호·`initialize_result` 있음/없음·`listChanged`)로 둘지. 01 b7·03 b4·`chapter.json` 목표·01 제목 「capability 협상」·옛 그림이 모두 이 결정을 따름. 메서드 차례 목록은 상속이 필요해(서버 미들웨어) 소스 확인·회색으로 둘지도 함께.
2. **모델과 묶음 실행 검사(§5·§8)** — M1 / M2′(05만) / M2(04·05 뒤 절반) / M3 가운데 하나. **01은 키·모델·`dotenv`·포트 없이 메모리 연결로 유지**하는 것이 계약상 가장 안전(stdio를 넣으면 배너·새 판 확인·하위 프로세스 정리를 함께). 05 입력 토큰을 결론에 쓸지와 흔들림 확인 규칙(`05-probe.md` §0 — 첫 요청 전에).
3. **비동기 모양과 서버 수명(§10-1·§6-4)** — `await`·`async with`를 셀 맨 위에 둘지(A)·`async def`로 감쌀지(B)·도구 파일에 둘지(C). stdio는 `"keep_alive": False`(또는 전송 객체)로 셀마다 정리할지. 03에서 HTTP를 실행할지(하위 프로세스 `Popen` + `terminate`·`wait`, 127.0.0.1) 아니면 설정 표로 둘지. 결과는 내용 블록의 글만 출력.
4. **paired 02·03 Before 다시 설계(§7)** — 02: 힌트·독스트링 없는 도구(입력 형식 `{}` → 몸통까지 간 오류) ↔ 힌트·독스트링(몸통 전 입력 검사) / 또는 데코레이터 한 줄만 다르게. 03: 가짜 변수 이름으로 환경 전체 전달 누출(참·거짓) / 또는 HTTP 토큰 없음 ↔ `StaticTokenVerifier` + `require_scopes`. 서버 쪽 오류 기록(표준 오류) 처리와 절 전용 서버 파일 자리(§10-3)를 함께.
5. **용어·도구 파일·서버 파일 자리(§10-2·§9)** — 「프롬프트」(MCP 구성 요소)·「프로토콜」·「capability」 처리, 「하위 작업」 → 서브에이전트 위임 · 도구 파일 A/B/C와 이름(`mcp_tools.py`는 「MCP 도구」와 헷갈림 — `connect_tools.py` 등) · `course_server.py` 자리(맨 위 유지 ↔ `notebooks/`)와 금지 문법 정리 여부(zip·01 계약에 닿음) · 서버 파일 찾기를 `candidates` + `for`·`break`로 세 자리에서 확인 · **옛 생성기 `qa/author_ch28.py`·`figures/_gen_figures.py` 첫머리 막기**(설명 주석 + `raise SystemExit(...)`).

## 14. 챕터 마감으로 미룰 것

- **06 실습 절 신설**(규격 §7-2): 슬러그 후보 **`06-MCP-실습`**(챕터 짧은 이름 「MCP」 — `_notebook/build_index.py` 60행과 같음, 선례 `09-DeepAgents-실습`·`04-Streaming-실습`·`05-위임-구조-실습`) · 다른 후보 `06-MCP-서버-실습`. 제목 「MCP 실습: …」, `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 5·11h에 더하지 않음**). 새 문법·API 0, 요청 3~5번. 주제 예 — 자료실 규정 서버(`course_server.py`)를 stdio로 붙인 에이전트에 01~05 기능(발견·등록·환경 좁히기·도구 거르기·명세 글자 수)을 모으고, 실행 2는 값 하나만(예: 붙일 도구 태그 하나·`keep_alive`·허용 목록 하나) 바꿔 도구 목록과 첫 요청 입력을 견줌.
- 옛 생성기 `qa/author_ch28.py`(`6806d465…`)·`figures/_gen_figures.py`(`dadf0c2b…`) → `qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 기록).
- 옛 그림 15개(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~5) 삭제 승인 목록(사본 `before/figures/`) · **챕터 공개 목록의 옛 SVG 다섯 줄 빼기**(Ch 23·24 선례 — 파일은 그대로).
- `chapter.json` `objectives`(「capability 협상」·「LangChain 1.4.0 MCPAdapter로 … 첫 호출 입력 토큰을 측정」·「로컬·원격 전송의 인증과 최소 권한 경계」) · 절 제목 · `textbook/part6/_build_index.py` 26행 · `_notebook/build_index.py` 60~61행(절 수 5 그대로) · 챕터 목차를 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 여섯, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절마다 요청 수·키 필요 여부, 01은 키 없이 도는 묶음 실행 검사 대상, 하위 프로세스·포트를 띄우고 끝내는 절, 「예상 비용」, 도구 파일 단락, 없는 「실패 진단 JSON」 문장 빼기) · `labs/part6/continuity-guide.md` 14행(Ch 37) · `qa/research.md`·`verification.md`·`집필점검표.md`에 「개선 전 판」 표시.
- 공개 목록 두 곳에 06·(도구 파일·서버 파일) 줄 → `part6-practice.zip` 다시 만들기(마지막에 한 번) → **`check_bundle_execution.py`(Ch 24 01·Ch 28 01 PASS, 새 `code_sha256`·`bundle-execution.json`)** → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 묶음을 풀어 06 첫 셀 확인 · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py` 결과 파일 되돌림).
- **뒤 챕터 인계**(고치지 않음): Ch 29 연결 문장(05 b8 → 06) · `continuity-guide.md` · Part 6 소개·`practice-start.md`(참) · Ch 27 09 b8(01 슬러그·내용) · 과정 요약에 Ch 28 줄(용어·도구 파일·비동기 선례·판 기준).
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 222MB) · 실습 폴더 `__pycache__/course_server.cpython-312.pyc`(및 새 커널 실행이 만들 것) · `qa/upgrade/gates-wip-*.json` · `.cache/vm/venv-ch28-mcp`(300MB) · 기기 `/tmp/ch28-prep`(124KB — 확인 스크립트) · `qa/upgrade/before/lab/`(이번에 만든 폴더 — 원본 사본 넷이 들어 있어 지울 필요는 없음).

## 15. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 5 · `notebooks` 5 · `figures` 16(SVG·excalidraw·caption 각 5 + `_gen_figures.py`) · `generators` 2(`author_ch28.py`·`_gen_figures.py`) · `qa` 4(`public-files.json`·`prerequisite-files.json`·`research.md`·`verification.md`) · **`lab` 4**(`README.md`·`pyproject.toml`·`uv.lock`·`course_server.py`) · `chapter.json`·`_build.py`·`index.html`·`집필점검표.md` = **40개, 500,480바이트**. 원본과 `cmp` 모두 같음. Ch 27 모양을 따르되 실습 폴더 파일은 `lab/` 아래(처음에 빈 `lab/` 폴더를 만들었는데 `rmdir`이 막혀 그 폴더에 넣음 — 삭제 0). 절 HTML은 넣지 않음(보호 파일 목록에 해시) |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 208, 통과 0/5), `495ac467…` |
| `qa/upgrade/before-manifest.json` | sha256 **226개**(`e5259ab8…`) — ① 이 챕터 원고·실습 폴더 45(`_src`·HTML·목차·`chapter.json`·`_build.py`·점검표·그림 16·`qa/` 다섯·README·잠금 둘·서버 파일·노트북 다섯·`pyc`) ② 이 챕터가 읽거나 이어 쓸 앞 챕터 파일 67: Ch 19 01~07 HTML·`_src`·노트북·`order_tools.py`·`orders.csv` · Ch 20 01·`graph_tools.py` · Ch 21 01·`runner_tools.py` · Ch 22 01~04 · Ch 23 04·`checkpoint_tools.py` · Ch 24 01 · Ch 25·26 도구 파일 · Ch 27 `_src` 아홉·09 HTML·노트북·`author_09.py`·`harness_tools.py`·잠금 둘·`before-manifest.json` · Ch 16 01·Ch 6 01·06·Ch 2 09·12·Ch 18 03 ③ 챕터 요약 26 ④ Ch 28에 기대는 Part 6·7·과정 파일 64: Part 6 목록 둘·목차·소개 `_src`·`practice-start.md`·`qa/` 스크립트·JSON·MD 전부(`check_bundle_execution.py`·`bundle-execution.json` 포함)·언어 기록·`ch28-before-path-repair/` · 연속성 안내 · 목차 스크립트 둘·`build_bundle.py`·`textbook/index.html` · zip 둘 · Part 7 기록·목록 · 검사 기록(`notebook-contracts-part6-ch28-mcp.json`·`checks/ch28-mcp/`) · `check_course_continuity.py` · Ch 29 `_src` ⑤ 규격·과정 문서·공용 도구 24(`upgrade/`·게이트·`verify.py`·`execute.py`·`render.py`·`visual.cjs`·Mermaid 도구·`builder.py`·`_figure.py`·`.env.example`·`AGENTS.md`·`AUTHORING.md`). `upgrade-progress.md`는 넣지 않음(읽지 않음) |
| `qa/upgrade/chapter-lead-notes.md` | 이 파일 |
| `$ROOT/.cache/vm/venv-ch28-mcp` | Python 3.12.13 · 300MB |

### 가상환경 만든 방법과 결과
- Ch 27 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch28-mcp` → `uv pip install --python …/bin/python pip==26.2` → 잠금 목록 `uv export --project labs/part6/ch28-mcp --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일 그대로 — 수정 시각 09-10 그대로), 주석 줄만 뺀 133줄(`/tmp/ch28-prep/req-clean.txt`, 환경 표시 `; sys_platform == …` 유지) → **`bin/python -m pip install --no-cache-dir -q -r`**(한 호출, 170초 안에 끝남). 설치 오류 0, **`uv cache prune` 안 함**.
- 크기 어림(만들기 전): Ch 27 환경 292MB에서 Deep Agents·Anthropic·Google 계열이 빠지고 FastMCP·uvicorn·starlette·authlib 등이 더해져 비슷할 것, 사용자 디스크(여유 67G)라 기기 루트 여유(2.2G)·`/sessions`(832M)는 거의 그대로일 것 → 만듦. **전후 루트 2.2G · `/sessions` 832M 같음.**
- 결과: `pip freeze --all`과 잠금 대조 **판 차이 0**(설치 128 = 잠금 133 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`·`pywin32`·`pywin32-ctypes`(win32)·`httpx2-jsfetch`(emscripten); `jaraco.*` 셋은 이름 표기만 다름). `fastmcp 4.0.3`·`fastmcp-slim 4.0.3`·`mcp 2.2.0`·`mcp-types 2.2.0`·`langchain 1.4.0`·`langchain-core 1.6.2`·`langchain-openai 1.6.0`·`langgraph 1.2.11`·`openai 3.11.0`·`pydantic 2.13.5`·`httpx 0.28.1`·`uvicorn 0.52.4`·`starlette 1.6.0`·`anyio 4.15.1`·`python-dotenv 1.2.3`·`ipykernel 7.3.0`·`nbclient 0.11.0`·`pip 26.2`. `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인(`env -u OPENAI_API_KEY`): `langchain.mcp`(`MCPAdapter`·`MCPToolArtifact`·`as_langchain_tool` — 가져올 때 `LangChainBetaWarning`) · `fastmcp`·`fastmcp.client`·`fastmcp.client.transports`·`fastmcp.server.auth`(`StaticTokenVerifier`·`require_scopes`)·`fastmcp.server.middleware` · `mcp`·`mcp.types`·`mcp.client.stdio`·`mcp.client.streamable_http` · `dotenv`·`psutil`·`tiktoken` 모두 됨. **`langchain_mcp_adapters`·`mcp.server.fastmcp`·`numpy` 없음.** 모델 객체는 가짜 키 글로 만들기만(요청 0). 루트 `.env` 키 이름은 `OPENAI_API_KEY` 하나(값은 보지 않음). `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씀.
- 띄운 서버와 끝낸 방법: 메모리 연결(스크립트 안) · stdio 하위 프로세스(`env_server.py`·`course_server.py`·`print_*_server.py` — 스크립트의 이벤트 루프가 닫힐 때 정리) · 127.0.0.1 HTTP(같은 루프 작업 `cancel` / 하위 프로세스 `terminate`·`wait`). 끝난 뒤 남은 서버 프로세스 0(`ps` 확인). 확인 중 기기 셸 한 번이 `pkill -f` 패턴에 스스로 걸려 끝남(파일 영향 없음 — 다시 확인해 남은 프로세스 0).

### 참고 자료 (2026-09-28 확인)
- MCP 스펙 2026-07-28 `https://modelcontextprotocol.io/specification/2026-07-28` — 「Stateless, self-contained requests」·「Per-request capability negotiation」 · 클라이언트 기능은 Elicitation.
- 변경 요지 `…/2026-07-28/changelog` — 세션·`Mcp-Session-Id` 없앰(SEP-2567) · `initialize` 핸드셰이크 없앰, `_meta` 판 번호·클라이언트 capability(SEP-2575) · `server/discover` 필수 · `subscriptions/listen` · `ping`·`logging/setLevel` 없앰 · MRTR(SEP-2322) · `resultType` · `tools/list` 정해진 차례 · `Mcp-Method`·`Mcp-Name` 머리 · `ttlMs`·`cacheScope` · Roots·Sampling·Logging 사용 중단 예고.
- 판과 호환 `…/2026-07-28/basic/versioning`(요청 주소는 `…/basic/lifecycle`에서 이 문서로) — 「There is no negotiation handshake」 · `UnsupportedProtocolVersionError` `-32022` · modern·legacy·dual-era 표.
- 전송 `…/2026-07-28/basic/transports` · stdio `…/transports/stdio` — 「The server MUST NOT write anything to its stdout that is not a valid MCP message」·종료 절차·`server/discover` 떠보기 · Streamable HTTP `…/transports/streamable-http` — 「Servers MUST validate the Origin header」·「SHOULD bind only to localhost (127.0.0.1)」·「SHOULD implement proper authentication」·GET 끝점과 세션 없앰.
- 인가 `…/2026-07-28/basic/authorization` — 「Authorization is OPTIONAL」·HTTP는 따름(SHOULD)·「STDIO transport SHOULD NOT follow this specification, and instead retrieve credentials from the environment」·토큰 대상 확인·최소 권한 범위.
- LangChain MCP `https://docs.langchain.com/oss/python/langchain/mcp` — `langchain[mcp]>=1.4.0`·베타·`Path`는 stdio·문자열은 URL만 · 옮기기 `https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters` — `MultiServerMCPClient` → `MCPAdapter`, `load_mcp_tools()` → `list_tools()`, interceptor → `@wrap_tool_call`, 프롬프트·리소스 안 감쌈.
- FastMCP 클라이언트 `https://gofastmcp.com/clients/client` — FastMCP 4.0 문서, `mode="auto"`(기본)·`"legacy"`·판 고정.
- 설치판 소스: `langchain/mcp/__init__.py`(베타 경고) · `adapter.py` 47~69(대상 종류)·84~122(문자열은 URL만)·174~200(elicitation 켜기)·221~242(`list_tools`) · `tools.py` 89~117(오류 → `status="error"`)·212~282(`StructuredTool`, `coroutine`만) · `fastmcp/client/client.py` 312~330(`mode`)·666~720(era 공통 속성)·839~889(`_negotiate`) · `fastmcp/client/transports/stdio.py` 33~95(`keep_alive`)·235~260(`StdioServerParameters`)·486~492·553~556·615~618(`os.environ.copy()` 쓰는 전송) · `fastmcp/mcp_config.py` 180~224(`StdioMCPServer`의 `env`·`keep_alive`) · `mcp/client/stdio.py` 40~90(기본 환경)·93~128(`env` 더하기) · `mcp_types/version.py`(판 목록) · `fastmcp/server/mixins/transport.py` 258~290(`run_http_async`·Host/Origin 보호) · `fastmcp/server/auth/providers/jwt.py` 647~(`StaticTokenVerifier`) · `fastmcp/utilities/authorization.py` 143·197(`require_scopes`·`restrict_tag`) · `fastmcp/server/server.py` 174~175(태그 인자 안내)·1810~1860(`tool(…, tags=, auth=)`) · `fastmcp/settings.py` 312~330(배너·새 판 확인) · `fastmcp/utilities/version_check.py` 16(PyPI 주소).
- 모델 없는 확인 파일(기기 `/tmp/ch28-prep/exp/`): `e0_imports.py`(판·가져오기) · `e1_init.py`(auto ↔ legacy 판 번호·capability·서버 정보, 빈 서버) · `e2_wire.py`(오간 메서드 차례 — 미들웨어 기록, 두 번 같음)·`e2b_log.py`(내장 기록 미들웨어 — 시각 섞임) · `e3_stdio.py`(하위 프로세스 환경 이름·수명·동기 호출 불가) · `e4_http.py`(토큰 셋·관리 도구 숨김)·`e4b_listen.py`(같은 루프 HTTP 정리 문제)·`e4c_sub.py`(하위 프로세스 HTTP 정리) · `e5_stdout.py`(서버 `print`) · `e6_schema.py`·`e6b_nohint.py`(힌트·독스트링·입력 검사) · `e7_convert.py`(도구 변환·명세 글자 수·`ToolMessage`) · `e8_toolnode.py`(`ToolNode` 그래프) · `e9_keepalive.py`(`keep_alive=False`) · `e10_clientcaps.py`(클라이언트 capability — 못 봄). AST·금지어 세기 `ast_scan.py`·`banscan.py`, 보호 파일 `manifest.py`.
- 앞 챕터: Ch 2 12 노트북(비동기) · Ch 6 01 `_src`(계층 지도) · Ch 16 01 `_src`(허용 목록) · Ch 18 03 노트북(`await` 설명) · Ch 19 03 노트북(`spec_length`)·요약 §13 · Ch 24 요약 §15 · Ch 27 요약 §16·§17·09 `_src` b8 · Part 6 `ch28-technical-review.md`.
