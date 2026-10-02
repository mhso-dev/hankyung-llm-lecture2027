# 03절 진단 — ainvoke 요청 응답 (paired)

- 작업일: 2026-09-29 · 작업자: 03절 작업자 · 생성기 `qa/upgrade/author_03.py`(`a63b9ebe…` — 마지막 치환 뒤)
- 읽은 것: `handoff.md`(챕터 공통·§01 → §02·§02 → §03 전부) · 준비 노트 `chapter-lead-notes.md`(§0·§1·§2 03·§3·§4·§7·§8) · `02-diagnosis.md` · `author_02.py`(전부)·`author_01.py`(`FIND_LAB` 대조) · Ch 28 `author_04.py`(`try` 셀 본) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 규격 전부 · 과정 요약(Ch 13·21·25·28·29 줄, §4 용어·금지어) · Ch 21 `chapter-summary.md`(같은 이름 `AgentState`) · Ch 2 12·Ch 28 04 `_src`(이어 쓴 말·완료 챕터 문장) · Ch 13 01·Ch 21 01·Ch 25 01 노트북(`invoke`·`stream` 모양). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다. Ch 27·29 도구 파일 사슬은 도구 파일을 만들지 않아 보지 않았습니다.

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-03.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 1 · 1 · 5 · 0 · 7 · 12 · 3 = **29** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(`count_code.py`) | 5 · 25 | **22 · 100** |
| 검사 문장 | 82 | **361** |

- 첫 실행 전 `upgrade_gates.py … --label wip-03 --section 03`: G1·G2 **0**(G6 2 — 영문으로 시작하는 문장 둘(「await를 붙이자」·확인할 점 첫머리 백틱), G7 3 — 그림 전) → 고친 뒤 G6 0.
- AST 따로(`/tmp/ch30-03/tools/extra_check.py` — 02 도구 복사): 걸린 것은 **챕터 예외와 허용 범위뿐** — 셀 맨 위 await 셋(셀 [6] `await get_agent()`·[15] `await pending`·[20] `await sync_graph.ainvoke` — handoff 비동기 표 「Ch 28 이어 씀」) · `try` 둘(Before 셀 [11]·[13], `except TypeError as error` — Ch 2 05, Ch 28 04 선례) · `async def` 하나(제공 함수 `get_sync_graph`). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`while`·별표 풀기·대입 풀기·기본값 매개변수·힌트(매개변수·내놓는 값·변수)·클래스·데코레이터·가짜 에이전트·`asyncio`·딕셔너리 `.get` **0**. 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **8줄** · 함수 본문 최대 **2줄** · 셀당 정의 하나.
- 금지어(`/tmp/ch30-03/tools/ban30.py` — 01 도구 그대로, `.mmd`·캡션·alt 포함): 걸린 것은 **허용한 것뿐** — 「노드」(Ch 13 01 용어 — Ch 25·28 04 본문이 씀, 이 절의 오류 글이 노드 이름을 가리켜 뺄 수 없음, **강사 확인**) · 「이벤트」(「이벤트 루프」 — Ch 2 12 말) · 「스트림」(「스트림 사건」 — Ch 25 말 셋, b3·노트북 4절·다음 절 예고) · 「의존성」(02 용어) · 「토큰」(「접근 토큰」 한 곳) · 「로그」(「프로그램」 거짓 양성) · 「Agent」(주석의 `AgentState` 거짓 양성). 「사용자가 금지한 표현(과정 규칙)」·「쉽게·간단히·당연히」·「실행 객체」·「평가셋」·「택배」·「창구」·「상태 사전」 0.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/03-…ipynb`·`before/_src/03-*.html`)

1. **Before가 결함이 아님**: 「오류」 글자 질문 → `RuntimeError 교육용 스트림 오류`는 앱 코드(`agent.py` 18~19행)가 **일부러 던지는 예외**이고, After는 질문만 바꿈(고친 것 없음) — 규격 §3 「실패 장면은 실제로 일어나는 조건으로」와 어긋남.
2. 준비 셀이 루트 커널에서 멈춤(`next((p for p in (start, *start.parents) …), None)` + `os.chdir`) — 01·02와 같은 문제. HTTP를 부르지 않아 절 제목의 「요청 응답」이 코드에 없음.
3. 셀 맨 위 `await`를 풀이 없이 씀 · `try` 셀의 `failed` 변수가 예외가 안 나면 정의되지 않는 모양 · `sorted`·`assert` 모델 없는 값 · 코드 셀 첫 줄 주석 0 · 결과 읽기 0 · 제목 셀·그림 첨부 없음.
4. 틀린 말·사실: b7 **「실제 모델 품질은 Ch29 평가셋으로 확인합니다」**(Ch 29에 평가셋 없음 — Ch 29 인계 §16-1) · b3 **「상태 사전」**(금지어)·**「Ch25에서는 단일 실행과 스트리밍이 같은 실행 객체의 다른 소비 방법」**(「실행 객체」 — Ch 21 인계 틀린 말, 「소비」 — Ch 25 인계) · b4 **「택배 창구·송장 번호」** 비유(Ch 20 금지 계열 「택배 송장」·Ch 30 금지 「창구」) · b4 「DNS, 공급자 대기열 … 지연 원인」·「모델과 도구별 소요 시간도 측정해야」·「전체 요청 45초 안에서 모델 30초, 도구 10초」(실행 안 한 설계 설명) · 도식 읽기 틀 색 문장(「파란 상자는 데이터, 보라색 상자는 Agent 실행」 — 모델 없는 절에 보라).
5. 금지어: 반환 7/4·사전 3/2·로그 4/1·이벤트 2/2·조각 2/1·명시 2·직렬화·지연·측정·보장·식별자 1·평가셋 1·택배 1(준비 노트 §1).
6. 참고 자료 둘(확인 2026-09-11, 설명 없음)·복습 한 줄 해설 넷.

## 바꾼 것

- **paired 설계(handoff §02 → §03 2)**: Before = 실습 그래프(노드 함수 `answer_node`가 `async def` 하나 — `agent.py` 23행)를 Ch 13 01·Ch 21 01의 동기 메서드 `invoke`로 → **`TypeError`**, 오류 글 두 줄 `No synchronous function provided to "answer".` / `Either initialize with a synchronous function or invoke via the async API (ainvoke, astream, etc.)`(한 줄씩 출력) · Ch 25 01의 동기 `stream`도 → `TypeError`·**오류 글이 invoke 때와 같은가 `True`**·스트림 사건 0개(Before 결함 결과 — 받아 출력했어도 빨강). After = `ainvoke`를 **부르기만 → `coroutine`**(Ch 2 12 모양) → **`await pending` → `dict`·칸 `['messages', 'answer']`·답 `질문을 확인했습니다: 반납 기한을 알려 주세요`** → 2절 HTTP 응답과 **두 답이 같은가 `True`**, 응답 본문의 칸 `['answer', 'thread_id']`(칸 `messages` 없음). 옛 「오류」 글자 장면은 쓰지 않고 b7에 「교재용으로 일부러 넣은 줄」 한 줄.
- **예시 부분(2·3절)**: `inspect.getsource(chat)`로 처리 함수 `chat`의 소스 아홉 줄을 그대로 출력(앱 파일 78~80행 `runtime.ainvoke({"messages": [body.question]})` — 02 b8 「03절에서는 처리 함수 몸통이 에이전트 그래프를 부르는 줄을 봅니다」와 Ch 2 12 b8 「Ch 30 3절은 await로 Agent 실행을 기다립니다」가 참이 되는 자리) · `await get_agent()`가 가져온 `agent`와 같은 객체 `True` · `TestClient` POST `/v1/chat`(02 인증 머리 `auth_headers` 그대로) → **200**·`{'answer': '질문을 확인했습니다: 반납 기한을 알려 주세요', 'thread_id': 'ainvoke-01'}` · 그래프 파일 세 줄(`class AgentState(TypedDict):`·`async def answer_node(…)`·`graph.add_node("answer", answer_node)`) · `inspect.iscoroutinefunction(answer_node)` `True`(설치판 langgraph가 같은 함수로 확인 — `_internal/_runnable.py` 528~536행) · 처리 함수와 같은 모양의 입력.
- **값 바꿔 보기(6절)**: 노드 함수만 `def`로(`sync_answer_node` — 같은 답 규칙, 실습 파일의 상태 형식 `AgentState`, Ch 13 01 모양으로 컴파일) → 비동기 함수인가 `False` → `invoke` 답 · `await ainvoke` 답(**invoke 답과 같음 `True`·실습 그래프의 답과 같음 `True`**) → 02절 재정의로 `get_agent` 대신 `get_sync_graph`(동기 노드 그래프를 내놓는 이름 있는 `async def`)를 넘겨 같은 요청 → **200·2절 응답 본문과 같음 `True`**, 같은 셀 끝에서 `clear()`(키 수 `0` — 02 Before 교훈). 가짜 에이전트 아님(노드가 코드인 진짜 LangGraph — handoff §01 → §02 2). 빨강 0.
- **「ainvoke」 말**: 첫 풀이가 아니라 Ch 28 04 이어 씀(노트북 1절 「제목의 ainvoke는 Ch 28 04절에서 본 비동기로 부르기입니다」·b2·용어 표 「Ch 28 04절에서 이어 씀」). 새로 푼 것은 이 그래프에 동기 부르기가 안 되는 까닭(노드 함수의 정의 줄 — 설치판 소스 행)뿐.
- **새 용어 1**: 「비동기 노드 · 동기 노드」(뜻 → 전기 열차 예 → 이 절 코드). meta 「강의 1h | 실습 2.5h」 그대로(챕터 시수 합 유지).
- 노트북: 제목 셀(할 일 셋·준비물·기준 버전·강의와 실습 범위) · 오늘 볼 그림(03-1 첨부) · 설명 → 코드 → 결과 읽기 · 정리 세 줄 + 04 예고. 설치 셀은 02와 같은 여섯(잠금 판 — `agent_service.agent`만 가져와도 `__init__.py`가 앱 전체를 가져옴). 키 셀 없음. 파일 위치 셀은 01절 셀 글 그대로(생성기 `__main__`에서 `author_01.py`와 문자열 대조 `assert`).
- 본문 b1~b10 새로(b3 = 01·02절 / Ch 13 01·Ch 21 01(동기 `invoke`)·Ch 25 01(동기 `stream`) / Ch 2 12(코루틴·await·이벤트 루프 — 링크)·**Ch 28 04(`ainvoke`, 그 절 오류는 `NotImplementedError`로 다름을 밝힘)** / Ch 2 05(`try`) · b10 = LangGraph 문서 Use the graph API의 Async 절·Python asyncio 문서(둘 다 2026-09-29 WebFetch) + 설치판 소스 행 둘 + 실습 파일 행). 복습 넷 → **다섯**(해설 포함).
- 그림: Mermaid **5장**(03-1 b4·노트북 · 03-2 b4 · 03-3 b5 · 03-4·03-5 b6 — viewBox 폭 273·271·486·659·306, 모두 868 이하) + 삽화 **1장**(03-6, 재생성 0). 옛 `{{svg:03-흐름}}` 토큰 제거, 옛 그림 파일 셋(`03-흐름.svg·.excalidraw·.caption.md`)은 그대로.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-03/exp/`)

- `p3_scene.py`(노트북 장면 전체를 파이썬 파일로 — await 자리는 `asyncio.run`, 5번): 출력 md5 **5/5 같음**(`502fa1e6…`), 표준 오류 0 — 그래프 종류 `CompiledStateGraph`·노드 `['__start__', 'answer']` / `get_agent()`가 `agent`와 같음 `True` / `chat` 소스 아홉 줄 / HTTP 200·칸 `['answer', 'thread_id']` / 그래프 파일 세 줄 / `invoke`·`stream` 모두 `TypeError`·같은 두 줄 / `coroutine` → `dict`·칸 `['messages', 'answer']` / 같은 답 `True` / 동기 노드 그래프 `invoke`·`ainvoke` 같음 `True`. 실습 폴더에 새 파일 0.
- 설치판 소스(langgraph 1.2.11): `_internal/_runnable.py` 528~536(`is_async_callable` = `inspect.iscoroutinefunction`) · 566~567(비동기 함수 → `RunnableCallable(None, thing)` — 동기 자리 비움) · 569~574(동기 함수 → 동기 함수 + `run_in_executor`로 감싼 비동기 판) · 377~382(`invoke`에서 동기 자리가 비었으면 `TypeError` — 두 줄 글) · 452~455(`ainvoke`는 비동기 판이 없으면 `invoke`) · `graph/state.py` `add_node`(884~910 `coerce_to_runnable`) · `pregel/main.py` 3836 `invoke` → 3891·3913 `self.stream(` · 4013 `ainvoke` → 4068·4090 `self.astream(`.
- 공식 문서(2026-09-29 WebFetch): LangGraph Use the graph API — Async 절 「Update nodes use async def instead of def」·「Invoke the graph with .ainvoke or .astream as desired」(동기 부르기가 오류라는 문장은 문서에 없음 → 설치판 소스와 출력으로) · Python 3.12 asyncio Coroutines and Tasks 「Note that simply calling a coroutine will not schedule it to be executed」.

## 실행 (새 커널)

| 실행 | 자리 | 키 | 결과 |
|---|---|---|---|
| 시험 tryA(`/tmp/ch30-03/tryA` 사본, `execute.py` 기본 `--cwd` = 프로젝트 맨 위, `PYTHONPATH` = `notebooks/`) | 루트 커널 | `OPENAI_API_KEY` 지움 | PASS 22셀 |
| 시험 tryB(사본, `--cwd` 실습 폴더 `notebooks/`) | 학생 커널 | 지움 | PASS 22셀, 셀별 22/22 같음(`outputs_sha256`은 설치 셀 스트림 나뉨으로 다름) |
| **A**(`run_section.sh … 03`, 시작 07:42:41Z · `executed_at` 2026-09-29T07:42:43Z) | 루트 커널 | 지움 | PASS 22셀(그림 첨부 단계에서 멈춤 — 03-1 PNG 전) |
| **B**(A 사본, `uv run … execute.py --cwd notebooks/`, 07:42:53Z) | 학생 커널 | 지움 | PASS 22셀 |

- **A ↔ B 셀별 출력 글자 22/22 같음**(이은 글 해시 `f37184f27a7057b5` 같음), `code_sha256` `eb33867b5939602dd85bd68b32ea5331a1d9f944453da26372ba231d9da5d8ba` 같음. **`outputs_sha256`은 다름**(A `5d7bc81af09991040f44da15b7bafa0f816d71887b09041483babfb1aa5461c2` · B `7510b28b4263906a75170191c6760ce21c540f8d84b2c77814c04f93dfd40cde`) — 설치 셀 출력이 두 스트림으로 나뉜 자리만 다름(A는 `starlette` 줄 뒤, B는 pip 안내 줄 뒤에서 나뉨 — 글자는 같음, 02 선례). 요청 0이라 셀 [2]~[22] 출력은 모두 같음.
- 그 뒤 `--no-exec` 셋(렌더·첨부·빌드)에서 노트북 코드·출력·`executed_at` 그대로(첨부만 더함 — A 사본과 `cmpout` 22/22·`outputs_sha256` 같음, 생성기로 다시 만든 셀 글과도 49/49 같음) — 노트북 파일 **`86aa1b08f8d93eb680338ce781b0b32af49c34c242af8a23e76309ec038aac5b`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에 새로 생긴 파일 0(`find -newer` — 노트북 03 말고, `agent_service/__pycache__` 그대로) · `.failure.json` 0 · 표준 오류 출력 0(커널 TCP 경고는 실행기 쪽) · 설치 셀 출력에 pip 안내 한 줄.
- **모델 요청 0** · 서버 프로그램·포트·자식 프로세스 0 · 남은 프로세스 0(`ps` — ipykernel·uvicorn·python 없음).

## 앱 파일 고침 · `app.openapi()` 대조 · `tests/`

- **03은 앱 파일을 고치지 않음.** 이 절이 출력하는 `chat` 소스(75~83행)에는 `try`·`raise … from exc`·`-> ChatResponse`가 있지만, 모두 과정이 푼 모양(Ch 2 05 `try`·Ch 16 05 `except TimeoutError`·Ch 2 07 내놓는 값 힌트)이고 02 노트북이 같은 줄(`async def chat(`)을 출력함 — 바꾸면 02 다시 실행과 결과 읽기 고침이 듦(handoff §02 → §03 8). 본문은 `raise … from exc`를 풀지 않고 「02절에서 본 504 자리」로만 가리킴.
- 확인: `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 · `pytest -q -p no:cacheprovider` **6 passed, 1 warning** · 앱 파일 해시 `app.py` `3455d405…`·`agent.py` `a6c42e63…`·`live_agent.py` `586a6a69…`·`schemas.py` `ed77b197…`·`__init__.py` `1c7d7aef…` 그대로. `openapi.json`·생성 SDK 손대지 않음.

## 도구 파일

- **만들지 않음** — 03은 앞 챕터에서 배운 평범한 함수를 쓰지 않음(쓰는 것은 LangGraph·FastAPI·`inspect` 라이브러리 함수와 노트북 값뿐). `serve_tools.py` 이름은 그대로 비어 있음. 인증 머리 `auth_headers`는 02처럼 노트북 값.

## 고친 틀린 사실

- b7 「실제 모델 품질은 Ch29 평가셋으로 확인」 → 「모델을 부르는 에이전트의 답은 실행마다 달라질 수 있어 … Ch 29 01절의 궤적 맞춰 보기나 03절의 평가 모델 판정을 씁니다. 모델을 부르는 에이전트는 09절에서 씁니다」(Ch 29가 실제로 가르친 것, 링크).
- b3 「Ch21에서 Agent의 입력과 결과가 상태 사전」 → 뺌. 결과는 「결과 딕셔너리」로, 실습 파일의 `AgentState`는 **과정의 셋째 같은 이름**으로 밝힘(b4 「결과 딕셔너리와 응답 본문」·노트북 3절 — Ch 20 01 우리 상태 형식·Ch 21 03 라이브러리 상태 형식과 칸이 다름).
- b3 「Ch25에서는 단일 실행과 스트리밍이 같은 실행 객체의 다른 소비 방법」 → 뺌. Ch 25 01의 동기 `stream`은 「스트림 사건을 차례로 내놓는 동기 메서드」로만 이어 씀(「실행 객체」·「소비」 0).
- b4 비유 「택배 창구·송장 번호」 → 챕터 계열 「화물 열차」(돌아온 열차의 짐칸 둘·손수레 위 상자 하나).
- b4 「기다리는 동안 이벤트 루프는 다른 요청을 처리」(보이지 않은 동작) → Ch 2 12에서 본 사실로만 이어 쓰고, 「이 절에서는 요청 둘을 함께 보내 보지 않았습니다」.
- b4 시간 상한 45초·모델 30초·도구 10초·「소요 시간도 측정」 → 뺌(실행 안 한 설계, `asyncio.wait_for`는 02가 풂).
- 도식 읽기 틀 색 문장 → 그림마다 색·방향을 그림에 맞춰 새로, 보라 0.

## 그림

- Mermaid 다섯: 설계표 `03-figures.md`(렌더 전 작성) → `.mmd`·캡션 → 렌더 → PNG 다섯을 직접 열어 확인 → **긴 라벨 셋이 가운데 끊겨(03-1 「기다림」·03-3 「둠」·03-5 「부름」) `<br>`로 미리 나눠 다시 렌더**(03-2·03-4는 그대로) → 다시 열어 확인(색·방향·점선 갈래·빨강은 03-4 Before 결과 하나뿐·보라 0). G7 라벨 숫자(200·`/v1/chat`) 출력에 있음.
- 삽화 03-6: `03-6-…prompt.md` 상태 줄 — **1차 job `1b5d4a73-4a3e-46c3-860e-aec3d5217188` 채택**(재생성 0, 서비스 쪽 조회 502 한 번 — 생성 요청은 한 번) · 거래 2026-09-29T07:45:24.270179Z 「Nano Banana Pro −2」 한 줄(**이 절 몫 2크레딧**, 잔액 2289 → 2287, 앞 거래 07:14:00Z는 Ch 30 02) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 저장 PNG `9eb4fef4024772e8e2a0eea91df755d1ec208bbb10bc5fcf2260ec6e5d236812`(1100 × 614)와 채택 결과를 다시 받아 줄인 그림 픽셀 대조 bbox `None`·최대 차이 0 · 저장본 사본을 열어 선로 하나·기관차 하나·짐칸 둘(빈 것 하나·꾸러미 든 것 하나)·손수레 하나·큰 상자 하나를 세고 그림 읽기를 씀. 01·02 소품 되풀이 없음, 번호판 없음. 손수레 자리가 프롬프트(빈 짐칸 바로 앞)와 조금 달라 「짐칸 앞 땅」으로 적음.

## 검사

- `run_section.sh … 03 --no-exec`: 렌더 다섯 · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 98 code cells (max 14 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `03-ainvoke-요청-응답.html`(`361440fd…`): `{{` **0** · `[[` 0 · 인라인 SVG 5 · 삽화 JPEG 1 · 노트북 셀 22.
- `pack.py … 03` → `qa/upgrade/review-pack/03-ainvoke-요청-응답.md`.
- 보호 파일 255개: `manifest-changes.md` 「03절 뒤」에 덧붙임.

## 완료 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

| 문장 | 판정 |
|---|---|
| **Ch 2 12 b8** 「Ch 30 3절은 await로 Agent 실행을 기다립니다」(`_src`·HTML) | **참** — 03 노트북 5절이 `ainvoke`를 부르기만 해 코루틴을 받고 `await pending`으로 그래프 실행을 기다림, 2절 `chat` 소스가 `await asyncio.wait_for(runtime.ainvoke(…))` |
| Ch 2 12 b8 「Ch 30 1절은 비동기 함수 안의 동기 호출이 …」 | 참(01 끝남 — 03 b7이 차단 호출을 한 번 이어 가리킴) |
| Ch 2 11 b8 「Ch 30 2절 … 대체 설정이 다음 질문까지」 | 참(02 끝남 — 03은 재정의를 같은 셀에서 비움) |
| Ch 2 `_src/index.html` 「비동기 대기는 … Ch 30의 FastAPI에서 다시 사용」 | 참 |
| Ch 25 04 b8 「Ch 30 04절은 모드 custom의 사건을 비동기 메서드 astream으로 받아 이어 붙입니다」 | 04 몫 — 03 b8·노트북 정리가 같은 말로 예고, 03은 `astream`을 부르지 않음(오류 글에 이름만 나옴) |
| Ch 29 05 b8(01 슬러그) | 03과 무관 — 슬러그 그대로 |
| Ch 4 04 language 스냅숏 「비동기 웹 서비스에서는 Ch 30의 실행 환경에 맞춰 AsyncClient」 | 옛 스냅숏(`qa/language/after/`) — 03은 `httpx.AsyncClient`를 쓰지 않음, 기록만 |
| Ch 31 01 b2·b3·Ch 34 04 b3·Part 7 소개 | 글만(참 — 대기 챕터, 고치지 않음) |

## 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀 — `d65ee56d…`) · 사용자 디스크 `.cache/ch30-03-view/`(삽화 보기 사본 한 장 — 새로 만든 폴더). 공용 도구·규격·과정 문서·Part 7 목록·zip·검사 스크립트·앱 파일·Ch 31 이후 파일은 고치지 않음.

## 강사 확인 대상

1. 「노드」 말(Ch 13 용어 — Ch 29 금지 목록에는 있으나 이 절의 오류 글·설명이 노드를 가리킴) · 새 용어 「비동기 노드·동기 노드」.
2. Before에 동기 `stream`까지 넣은 것(Ch 25 01 모양 — 04 `astream` 첫 풀이의 앞 장면).
3. 값 바꿔 보기에서 02절 재정의로 동기 노드 그래프를 처리 함수에 넘긴 것(같은 셀에서 `clear()`).
4. `inspect`(`getsource`·`iscoroutinefunction`)를 이 절에서 처음 씀(Ch 21 04가 `inspect`를 씀) · 셀 맨 위 await 셋·`try` 둘.
5. 앱 파일을 고치지 않은 것(02와 같은 까닭).
6. 삽화 03-6(재생성 0 — 위쪽 흰 여백 약 4분의 1).
7. 코드 양 25 → 100줄(셀 5 → 22).

## 남은 것 (마감 몫)

- `part7-practice.zip`에 03 노트북 새 판 반영(마감 때 한 번) · 03은 Part 7 묶음 실행 검사 대상 아님(01만).
- 옛 그림 `03-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-03-03.json` · 기기 `/tmp/ch30-03/`(사본·실험·삽화 원본 둘, 약 8MB) · 사용자 디스크 `.cache/ch30-03-view/`(656KB).
