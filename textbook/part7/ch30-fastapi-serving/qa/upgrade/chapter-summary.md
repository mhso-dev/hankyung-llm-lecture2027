# Ch 30 FastAPI로 Agent 서빙 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part7/ch30-fastapi-serving` 01~09절(품질 개선) + **10절 챕터 끝 실습 절 신설**(`10-FastAPI-서빙-실습`), 노트북 `labs/part7/ch30-fastapi-serving/notebooks/01~10-*.ipynb`, 도구 파일 `notebooks/serve_tools.py`, 실습 앱 패키지 `agent_service/`(가르치는 대상 — 도구 파일과 별개). **뒤 챕터가 읽는 계약 파일(산출 파일)은 없습니다**(노트북 파일 쓰기 0 — 08도 `openapi.json`을 쓰지 않고 글만 견줌).
- 기간: 2026-09-29(준비 조사 · 01~09절 개선 · 10절 신설 · 검토 1차 · 챕터 마감). 상태: **완료(강사 확인 대기)**. Part 7 첫 챕터(다음은 Ch 31 DB와 상태 영속화).
- 게이트: 수정 전 아홉 절 합계 **292**(G1 19 · G2 11 · G3 45 · G4 0 · G5 61 · G6 129 · G7 27 — 01 27 · 02 31 · 03 29 · 04 26 · 05 38 · 06 25 · 07 41 · 08 32 · 09 43, `gates-before.json`) → 마감 뒤 **10/10 PASS, G1~G7 모두 0**(`gates-after.json` `43c8ceb8…`, 검사 문장 388·403·361·367·414·433·424·402·401·333 = **3,926**).
- 코드 셀 5·5·5·4·4·5·7·4·6 = 45 → **22·24·22·23·25·26·21·22·23 + 10 새 절 21 = 229**(`verify.py --chapter` → `PASS 10 sections / 229 code cells (max 12 lines)`). 코드 줄(`count_code.py`, 주석·빈 줄 뺌) 27·29·25·29·30·32·53·26·54 = 305 → **110·105·100·111·159·152·123·137·151 + 10 116 = 1,264**, 도구 파일 66줄. Mermaid **42장**(01~03 다섯씩 · 04~09 넷씩 · 10 셋), 삽화 **10장**(절마다 하나, Higgsfield — 재생성 5회, 30크레딧, 마감 0), 복습 문제는 HTML에만.
- **모델 요청**: 01~08·10은 모델 없음(시험용 클라이언트 `TestClient` + 모델을 쓰지 않는 그래프). **09만 실제 `gpt-5.4-mini`**(`temperature=0`·`reasoning_effort="none"` — 앱 파일 `live_agent.py`). 노트북 한 번 **0·0·0·0·0·0·0·0·6·0 = 6번**. 작업 전체(흔들림 확인 + 새 커널 A·B — `09-diagnosis.md` 「서비스 요청 수」로 다시 셈) **09 약 42번, 나머지 0**, 마감 **0번**.
- 화면 검사 `visual.cjs`: HTML **열한 개**(열 절 + `index.html`) × 1280px·390px = **22행 PASS**(기기 `/tmp/pw` playwright·`/tmp/pw-browsers` chromium — Ch 26 마감이 설치한 것을 환경 변수 `NODE_PATH`·`PLAYWRIGHT_BROWSERS_PATH`·`LD_LIBRARY_PATH`만 주고 원본 그대로).
- **마감에서 다시 실행한 노트북: 없음**(두 검토자 판단 — 모든 지적이 글·그림 고침으로 풀림). 열 노트북 모두 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같습니다(§21).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 29 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-29)」) → 절별 `NN-diagnosis.md`·`10-design.md`·`09-probe.md` → 검토 `review-round1-A.md`(01~05·공통)·`review-round1-B.md`(06~10) → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 비동기 라우팅과 스키마 | FastAPI 앱 객체 `FastAPI(title=…)` · 요청 주소 데코레이터 줄 `@app.get`·`@app.post` · `async def` 처리 함수(동기 처리 함수는 다른 스레드 — `routing.py` 322~325) · 시험용 클라이언트 `TestClient(app)` · 처리 함수 매개변수 힌트 `body: ChatRequest`(Pydantic 양식 클래스, 파일 위치 셀 + `runpy.run_path`로 `schemas.py`만 읽음) → 맞지 않으면 처리 함수 전에 **422**(`detail` 칸 `type`·`loc`·`msg`·`input`·`ctx`, `string_too_short`) · `response_model=ChatResponse`(내보낼 칸만) · 404·405 · 비동기 함수 안 동기 호출이 이벤트 루프를 멈춘다는 설명(노트북 밖 5/5) | `make_result`(모델 없는 몸통 — 노트북) | 앱 객체 · 요청 방식 · 처리 함수 · 시험용 클라이언트 · 상태 코드 422 · 응답 형식 (6) |
| 02 의존성으로 Agent 주입 | `Annotated[float, Depends(get_limit)]` · 제공 함수 · 셀 맨 위 `await`(제공 함수 직접 부르기 — IPython 기능) · `app.dependency_overrides[…] = …` → **남은 재정의로 다음 테스트의 새 `TestClient`도 504**(Before) → `.clear()`(After) · `asyncio.wait_for` 첫 풀이(부르지 않음) · 504 | **`zero_timeout`**(06이 도구 파일로) · `get_limit`·`two_second_timeout`(노트북) | 의존성 · 제공 함수 · 재정의(재정의 딕셔너리) · 상태 코드 504 (4) |
| 03 ainvoke 요청 응답 | `ainvoke`(말은 Ch 28 04 이어 씀) — 부르기만 하면 `coroutine` → `await` → `dict`(칸 `messages`·`answer`) · 비동기 노드 그래프에 동기 `invoke`·`stream` → `TypeError`(langgraph `_internal/_runnable.py` 566~567·377~382) · 동기 노드 그래프는 둘 다(569~574) · `try`/`except TypeError` 둘 | `sync_answer_node`(노트북) | 비동기 노드·동기 노드 (1) |
| 04 astream과 응답 스트림 | `astream(…, stream_mode="custom")` → `async_generator`(비동기 제너레이터 — Ch 6 04 이음) · 셀 맨 위 `async for` · 다시 꺼내면 0 · `async def collect_events_async` · 모드 목록 `["custom", "updates"]` → 사건 6 → 7, `updates` 자리 `[7]` · 걸린 시간 안 잼(b2는 차례로) | **`join_tokens`**(06이 도구 파일로) · `collect_events_async`(노트북) · 도구 파일 첫 판 **`positions_of`·`mode_order`**(Ch 25) | 비동기 제너레이터 · 비동기 반복 (2) |
| 05 POST SSE 이벤트 설계 | `response_class=EventSourceResponse` · `ServerSentEvent`(칸 `event`·`id`·`data`) · 비동기 생성기 `yield`(비동기 제너레이터 함수 첫 풀이) · 앱 `chat_stream`을 HTTP 없이 불러 `ServerSentEvent` 일곱 · 본문을 빈 줄로 나눠 SSE 사건 일곱 → 칸 딕셔너리 → `json.loads`(한글은 유니코드 이스케이프로 나감 — 마감 A-1) · `asyncio.timeout` 첫 풀이(실행 안 함) · 실험: 인자 `response_class`만 뺌(같은 처리 함수를 새 앱 객체 둘에 `add_api_route`) → `text/event-stream`·`event:` 줄 7 ↔ `application/jsonl`·0 | **`split_sse`·`parse_sse`**(06이 도구 파일로) · `stream_answer`·`count_event_lines`(노트북) | SSE · SSE 사건 · 비동기 제너레이터 함수 · JSON 줄 형식 (4) |
| 06 fetch 재연결과 오류 이벤트 | 요청 머리 `Last-Event-ID`로 이어 받기(`sse-1:1` → `sse-1:2`부터, 앞머리 다름·수 아님 400, 범위 밖 `sse-1:99`는 `done`만) · 0초 재정의 → 200 + 오류 사건 `error`(`stream_failed`) · Before `status_says_ok`(상태 코드만) `True`(빨강) ↔ After `ended_with_done` `False` · 기록기 수준 올림 · TS `client/stream.ts` 11~30행 글로 읽기(노트북에서 `node` 부르지 않음) | **`read_events`·`event_names`·`token_values`·`ended_with_done`**(09가 도구 파일로) · **`last_event_id`**(10이 도구 파일로) · `status_says_ok`(노트북) · 도구 파일 06 판 | 이어 받기 · 오류 사건 · 함수 fetch (3) |
| 07 인증 CORS 타임아웃 | `client.options(…)` 사전 요청 · 응답 머리 `access-control-allow-origin`·`…-credentials` · Before ① 세 칸 `"*"` + `allow_credentials=True` 새 앱 → 모르는 출처를 그대로 허용(빨강) ② 실습 앱 401에 `WWW-Authenticate` 없음(빨강) ↔ After 출처를 적은 실습 앱 400 `Disallowed CORS origin` · `HTTPBearer()` 새 앱 401 + `Bearer` · 사전 요청 없는 POST는 서버가 실행(CORS는 브라우저 규칙) · 0초 → 504, 접근 토큰 없으면 0초에도 401 | **`header_or_none`**(10이 도구 파일로) · `whoami`(노트북) | CORS · 출처 · 사전 요청 · 자격 증명 (4) |
| 08 OpenAPI와 TS SDK | `app.openapi()`(`3.1.0`·요청 주소 다섯·`$ref`·`operationId`·SSE `itemSchema`·두 번째 부르기 같은 객체) = 실습 폴더 `openapi.json`(`06e5d1b9…`, 쓰지 않고 견줌) · 생성 SDK를 파이썬으로 줄만 찾음(함수 다섯 — JSON 셋 형식·SSE 둘 `Promise<void>`) · 실험: 인자 `dependencies`만 `require_token` → `HTTPBearer()` → 보안 방식 칸 생김·응답 코드 `['200', '422']` → `['200']`, 상태 코드는 401/200 같음 | `print_lines_with`(노트북) | 응답 문서 · 생성 SDK (2) |
| 09 실제 Agent HTTP 통합 | 실제 모델 에이전트(`create_agent` + 도구 `lookup_library_hours`) · `POST /v1/chat/live`(칸 둘) · `POST /v1/chat/live/stream`(모드 `messages`, 앱 138행 노드 조건 — 스트림 청크를 SSE 사건으로) · 실험: 같은 사건 목록에 남길 노드 목록만 `["model"]` → `["model", "tools"]` → 도구 결과 글로 시작 `False` → `True` · 요청 수 셈(Ch 29 04 · 사용량 든 청크 수) · 모델 글 `assert` 0 | `node_order`·`stream_text`(노트북) · 도구 파일 09 판 | 0(스트림 청크·칸 `metadata`·도구 메시지는 이어 씀) |
| 10 FastAPI 서빙 실습 | **새 문법·새 라이브러리 함수·새 말 0**(01~09 노트북·도구 파일 09 판과 AST 대조) | 조립 `send_preflight`·`send_question`·`events_of`·`record_step`·`print_log`·`start_flow`·`resume_flow`(노트북) · 도구 파일 10 판 | 0 |

- 새 용어 합계 **26개**(절 meta 「새 용어」 6·4·1·2·4·3·4·2·0·0).
- **허용한 문법**(노트북): 함수(셀당 하나, 본문 8줄 이하) · 여러 줄 `if`·`for`·`break` · 목록 `append` · 딕셔너리 여러 줄 · `assert`(파일 위치 셀·09 키 셀) · 키워드 인자 · **챕터 예외**(요청 주소 데코레이터 줄 · `async def` 처리 함수·제공 함수 · 처리 함수 매개변수 힌트 · 셀 맨 위 `await`·`async for` · 비동기 생성기 `yield`(05 노트북 `stream_answer`) · 03 `try` 둘). 마감 AST 따로(`extra_check.py`) 걸린 것은 이 예외와 요청 방식 `.get` 거짓 양성뿐, 호출 깊이 최대 2, 준비 셀 밖 셀 최대 10줄(05·08).
- **쓰지 않은 것**(열 노트북·도구 파일 0건): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`getattr`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`sorted`·`key=`·`set`·노트북 딕셔너리 `.get`·`.items`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·대입 풀기·별표 풀기·`while`·세미콜론·`isinstance`·노트북 클래스(양식 클래스는 실습 폴더 파일에서만)·가짜 모델 클래스.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 2 11·12**: 대체 설정이 다음 질문까지 이어지는 실패(02 Before — Ch 2 11 b8 참) · 비동기 함수·코루틴·이벤트 루프·차단 호출(01 설명, 03 `await` — Ch 2 12 b8 두 문장 참).
- **Ch 4 04**: GET·상태 코드(요청 방식·상태 코드의 바탕).
- **Ch 6 03·04·05**: 양식 클래스(Pydantic) · 제너레이터(04 「비동기 제너레이터」의 바탕) · `timeout`.
- **Ch 13 02**: `Annotated`(02 의존성 표시).
- **Ch 15 02·08**: `json.loads`(05) · 요청 주소·요청 본문(말).
- **Ch 16 05**: `TimeoutError`(02·06).
- **Ch 19 01·05·06**: 입력 형식(01) · 도구 메시지·`@tool`(09 실습 앱).
- **Ch 20 01**: `class AgentState`(03이 이름 셋을 가름 — Ch 20 01·Ch 21 03·실습 파일).
- **Ch 21 01**: `create_agent`·에이전트 그래프(09, 「실행 객체」 대신).
- **Ch 23 01·03·06**: 체크포인터·`thread_id`(05 「스레드 이름」의 뜻 — 마감 A-4) · 객체의 수명(02) · 멱등성(06 b3·b7).
- **Ch 24 01**: 중복 실행 방지 원칙(06 — Ch 24 `author_01.py` 28행 주석 참).
- **Ch 25 01·02·04**: 스트림 사건·진행 값·갱신·모드 차례(04) · 스트림 청크·칸 `metadata`(09) · 도구 파일 `stream_tools.py`의 `positions_of`·`mode_order`(04가 글자 그대로 옮김) · Ch 25 04 b8(04 custom·09 messages — 참).
- **Ch 28 01·02·03·04**: 파일 위치 셀·`runpy.run_path`·「노트북 도구(IPython)의 기능」 · 기록기·`body_inputs` 모양 · 접근 토큰·401·`WWW-Authenticate`(07이 견줌) · `ainvoke` 첫 풀이(03이 이어 씀).
- **Ch 29 01·03·04·05**: 궤적 맞춰 보기·평가 모델 판정(03 b7·09 b6 — 「평가셋」 대신) · 요청 수 셈 「도구를 요청한 응답 수 + 1」(09) · 05 b8(01 슬러그 — 참).
- 소재: 도서관 질문 「반납 기한을 알려 주세요」(03~07·10) · 09 「한빛도서관 월요일 운영 시간은?」 · 실습 앱의 모델을 쓰지 않는 그래프(`agent.py` — 질문 앞에 「질문을 확인했습니다: 」를 붙여 답함, 질문에 「오류」가 들면 일부러 예외).

## 3. 절별 과제·값 (새 커널 두 번에서 같았던 값 — 결론·그림에 쓴 값)

| 절 | 과제·입력 | 두 커널이 같았던 값 |
|---|---|---|
| 01 | Before `body: dict` ↔ After `body: ChatRequest` + `response_model` · 빈 질문 · 값 바꿔 보기 공백 한 칸 | Before 200·몸통에 들어온 값 `['']` ↔ After 422 `string_too_short`·`['body', 'question']`·`[]` · 공백 한 칸 → 두 앱 200·몸통까지 · 22/22 |
| 02 | `get_timeout` → `zero_timeout` 재정의 → 다음 테스트 새 `TestClient` · `clear()` · 값 바꿔 보기 2초 | 첫 504(노랑) → 다음 질문도 504·키 수 1(빨강) → `clear()` 뒤 0·200 · 2초 재정의 200인데 키 수 1 · 24/24 |
| 03 | 비동기 노드 그래프에 동기 `invoke`·`stream` ↔ `ainvoke` · 값 바꿔 보기 노드 함수 `def` | `TypeError` 첫 줄 `No synchronous function provided to "answer".` · `coroutine` → `dict`·칸 `['messages', 'answer']`·HTTP 답과 같음 `True` · 22/22 |
| 04 | `astream` 모드 `custom` → 모드 목록에 `updates`를 더함 | 사건 6 → 7 · `updates` 자리 `[7]` · 다시 꺼내면 0 · 이은 글 같음 · 23/23(`outputs_sha256` `e7a37a53…`까지) |
| 05 | 앱 `chat_stream` 바로 부르기 · POST SSE · 실험 `response_class` 뺌 | `ServerSentEvent` 일곱 · 200·`text/event-stream; charset=utf-8` · SSE 사건 일곱(token 여섯 + 번호 없는 `done`) · `event:` 줄 7 ↔ 0·`application/jsonl` · 25/25 |
| 06 | 0초 재정의 Before/After · `Last-Event-ID` 이어 받기 · `sse-1:99` | Before `True`(빨강) ↔ After `False` · `sse-1:2`부터·이은 글 같음 `True` ↔ 머리 없이 `False` · 400 두 글 · `sse-1:99` → `['done']` 인데 `True`(한계) · 26/26 |
| 07 | `wide_app` 사전 요청·POST · 실습 앱 401 · 출처를 적은 설정 · `HTTPBearer` · 사전 요청 없는 POST | `https://evil.example` 200·`true`(빨강) ↔ 400·`Disallowed CORS origin` · 401 `WWW-Authenticate: None`(빨강) ↔ `Bearer` · 사전 요청 없는 POST 200·허용 출처 `None` · 0초 504, 접근 토큰 없으면 401 · 21/21 |
| 08 | `app.openapi()` 읽기 · 실험 `dependencies` 바꿈 | 요청 주소 다섯·`3.1.0`·`06e5d1b9…` = 파일 `True` · 보안 방식 칸 `False` → `True`·`['200','422']` → `['200']` · 22/22 |
| 09 | `/v1/chat/live`·`/v1/chat/live/stream`·직접 `astream` messages · 남길 노드 목록 | (5/5 + 두 커널) 도구 `lookup_library_hours`·인자 `{'day': '월요일'}` · 노드 차례 `['model', 'tools', 'model']` · 도구 결과 글로 시작 `False` → `True` · 요청 수 `2` · 23/23(모델 셀까지) |
| 10 | §12 | §12 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀 — 세부는 handoff 「용어 표」)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 요청 주소(Ch 15 08 이음) · **요청 방식** · **앱 객체** · **처리 함수** · **시험용 클라이언트** | 「경로」·「엔드포인트」·「라우트」·「경로 연산」 대신 · 요청 방식 = 파이썬 「메서드」와 가름 · 처리 함수 = FastAPI path operation function | `/v1/chat` · `FastAPI(…)` · `TestClient(app)` |
| 01 | 요청 주소와 처리 함수 잇기 | 제목의 「라우팅」 — **Ch 18 「라우팅」(갈래로 보내기)과 다른 뜻** | 데코레이터 줄 |
| 01 | 입력 형식(Ch 19 이음) · **상태 코드 422** · **응답 형식** | 「스키마」 대신 | `body: ChatRequest` · `response_model=ChatResponse` |
| 01·02 | 응답 머리 · 요청 머리 | 「헤더」 대신 | `response.headers[…]` · `headers=auth_headers` |
| 02 | **의존성**·**제공 함수**·**재정의(재정의 딕셔너리)**·**상태 코드 504** | 제목의 「주입」은 FastAPI 문서의 말 injection을 옮긴 말(마감 A-5) — 본문은 「처리 함수에 값을 넘겨 주기」 | `Depends(…)` · `app.dependency_overrides` · `.clear()` |
| 03 | **비동기 노드·동기 노드** · (이어 씀) 비동기로 부르기(ainvoke)·결과 딕셔너리 | 「노드」는 Ch 13 말(강사 확인) | `answer_node` · `await agent.ainvoke(…)` |
| 04 | **비동기 제너레이터**·**비동기 반복** · (이어 씀) 스트림 사건·진행 값·갱신 | 「조각」 대신 스트림 사건·진행 값 · **「스트림 청크」는 09에서만**(Ch 25 02 messages) | `async_generator` · `async for` |
| 05 | **SSE**·**SSE 사건**·**비동기 제너레이터 함수**·**JSON 줄 형식** · 풀이로만 사건 이름·사건 번호·칸 `data`·본문 종류 | 「이벤트」 대신 SSE 사건(04 스트림 사건과 가름) · 「스레드 이름」은 칸 `thread_id`의 대화(Ch 23 01) — **01·03의 「다른 스레드」(Ch 2 12 실행 흐름)와 다른 뜻을 05 노트북 [12]·b4·b7에 한 문장씩(마감 A-4)** | `EventSourceResponse` · `sse-1:0` |
| 06 | **이어 받기**·**오류 사건**·**함수 fetch** | 제목의 「재연결」 → 이어 받기 | `Last-Event-ID` · `error` |
| 07 | **CORS**·**출처**·**사전 요청**·**자격 증명** · 풀이로만 허용 출처·CORS 층·보안 객체 | 「사전 요청」은 Ch 29 금지어 「사전」(딕셔너리)과 다른 낱말(강사 확인) · 「미들웨어」(Ch 22) 대신 CORS 층 · 자격 증명 = 브라우저가 스스로 붙이는 쿠키 같은 값(마감 B-9 — 스크립트가 적는 접근 토큰과 가름) | `client.options(…)` · `HTTPBearer()` |
| 08 | **응답 문서**·**생성 SDK** | 본문의 OpenAPI·SDK 대신 · 생성 SDK = `client/generated/`의 파일 열여덟(TS 파일 열하나와 설명 문서 일곱 — 마감 B-2) | `app.openapi()` · `client/generated/` |
| 09·10 | (새 말 0) | 스트림 청크·칸 `metadata`·도구 메시지(09) · 「단계 기록」·「기록 목록」(10 — 06 「기록기」와 가름) | — |

- **대체어 전부**는 handoff 「용어 표」 아래 목록. 본문 금지어: 「결정적」(→ 매번 같은 값)·「스키마」·「헤더」·「반환」·「검증」·「경로」·「라우트」·「엔드포인트」·「필드」·「실행 객체」·「페이로드」·「메타데이터」·「미들웨어」·「조각」·「토큰」 단독·본문 「Agent」·「서빙」(제목 밖)·「대역 객체」(마감 B-12에서 「따로 만든 시험용 객체」로) + 사용자가 금지한 표현(과정 규칙).
- 뒤 챕터에 넘길 말 문제: **「스레드」 두 뜻**(Ch 2 12 실행 흐름 ↔ Ch 23 대화) — 과정 요약에 올릴지 강사 확인(§17).

## 5. 비동기 허용 범위 (Ch 28 이음 + 이 챕터에서 늘어난 것)

| 문법 | 처음 풀이한 절 | 조건 |
|---|---|---|
| 셀 맨 위 `await`·`async with` | Ch 28(이어 씀) · 02가 제공 함수를 직접 불러 값 보기(await 셋) | 「노트북 도구(IPython)의 기능」 한 문장 · `asyncio.run`은 셀에서 쓰지 않음 |
| `async def` 처리 함수·제공 함수 | 01 | 셀당 정의 하나 · 동기 처리 함수는 다른 스레드(`routing.py` 322~325) |
| 비동기 함수 안 동기 호출 | 01(설명 — 노트북 밖 5/5, 실행 안 함) | Ch 2 12 b8 참 |
| `ainvoke` | Ch 28 04(말) → 03(부르기만 → `coroutine` → `await` → `dict`) | Ch 2 12 b8 「3절은 await로」 참 |
| `async for`·`astream` | 04 | 모드 목록이면 짝 `event[0]`·`event[1]`(대입 풀기 금지) |
| 비동기 생성기 `yield` | 05 | 처리 함수 예외 안(노트북 `stream_answer`) |
| `asyncio.wait_for`·`asyncio.timeout` | 02(`wait_for` 풀이)·05(`timeout` 풀이) → 06이 0초로 실행 | 앱 파일에 있음(`app.py` 78·109행) · 0초 이하면 곧바로 취소(Python 3.12.13 `asyncio/tasks.py` 507~517) |
| `httpx.AsyncClient`·`ASGITransport` | 노트북에서 쓰지 않음(01 노트북 밖 확인에만) | 스트림을 끝까지 모아 줌 — 도착 시각 주장 금지 |

- **스트리밍 사실**: 시험용 클라이언트는 앱이 응답을 다 보낸 뒤 본문을 한꺼번에 줍니다(starlette `testclient.py` 296·341·365). 그래서 열 절 모두 도착 시각·「실시간」·걸린 시간을 주장하지 않고, 적힌 차례만 봅니다(04 b2는 「진행 값이 끝 사건보다 먼저」라는 차례로 씀).

## 6. 앱 파일 문법 예외와 `app.openapi()` 대조 규칙 (검토 A-14 — 규격은 고치지 않음)

- **규칙(이 챕터 결정)**: 실습 앱 파일(`agent_service/*.py`)은 가르치는 대상이고 힌트가 입력·응답 형식을 정하므로, 아래 다섯은 과정 문법 사다리 밖이어도 그대로 둡니다. ① FastAPI 처리 함수·제공 함수의 매개변수 힌트(`body: ChatRequest`·`Annotated[str | None, Header()] = None` 등) ② Pydantic 양식 클래스(칸만) ③ 요청 주소 데코레이터 줄(`@app.get`·`@app.post`) ④ `async def` ⑤ 비동기 생성기 `yield`(`chat_stream`).
- **근거 자리**: 규격 `QUALITY-UPGRADE.md`에는 §2-12가 없습니다(검토 A-14 — 기록 몇 곳이 「§2-12」라고 적은 것은 틀림). 근거는 규격 §2-2 사다리의 L5(클래스)·L6(데코레이터)·L7(비동기가 학습 목표) 행과 과정 요약 §2-19의 Ch 28 「MCP 도구 매개변수 힌트」 예외입니다. **L5·L6·L7로 이미 되는 것**: 양식 클래스(칸만)·데코레이터 줄·`async def`. **이 챕터가 새로 넓힌 것**: 처리 함수·제공 함수의 매개변수 힌트와 비동기 생성기 `yield`. 규격에 한 줄로 반영할지는 최종 점검표 「사람이 정할 것」에 올림(§17·§20).
- **그 밖의 앱 파일 문법**(f-string·`str | None`·`removeprefix`·`raise … from` 등)은 과정 문법으로 고칠 수 있으나, **`app.openapi()` 결과가 바이트까지 같을 때만** 고칩니다. 기준값: `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`**(= 실습 폴더 `openapi.json`) · 정렬 직렬화 `d2fb94f6…`(4825자) · `pytest -q -p no:cacheprovider` **6 passed, 1 warning**. 02~10 노트북이 앱 줄 번호를 출력하므로(02 `Depends(` 줄 · 06 41~53·107~117 · 07 19~26·56~60 · 09 86~92·127~154 · 10 99~105) 줄 수를 바꾸는 고침은 하지 않습니다. 06·07은 출력한 앱 줄의 과정 밖 모양을 「뜻만 봅니다」로 풀었습니다(마감 B-8 — `str | None`·`= None`·`-> int`·`-> str` 풀이 더함).
- **마감에서 고친 앱 파일**: `agent.py` 17·38행 설명 글만(검토 A-10 — §21) — 같은 줄 안, 노트북 출력에 그 줄 없음, `app.openapi()` `06e5d1b9…`·6 passed 그대로를 `/tmp` 사본에서 먼저 확인.

## 7. 파일 위치 셀과 묶음 계약 (01)

- **파일 위치 셀**(과정 표준 — 01 셀 글, 02~10 문자열 대조로 같음): 후보 `".."`·`"."`·`"labs/part7/ch30-fastapi-serving"`에서 `agent_service/schemas.py`가 있는 곳을 고르고, 고른 후보는 출력하지 않음(커널마다 달라서). 02~는 뒤 셀에서 `os.chdir(lab_path)` + `from agent_service.app import app, …`(`import agent_service.app` 뒤 속성 접근은 `AttributeError` — `__init__.py`가 `app`을 가져옴).
- **도구 파일을 가져오는 04·06·07·09·10**은 파일 위치 셀보다 앞 준비 셀에서 `from serve_tools import …`를 하므로, 실습 폴더 맨 위에서 연 커널은 파일 위치 셀의 안내 전에 `ModuleNotFoundError`로 멈춥니다. 셀 코드는 챕터 계약이라 그대로 두고, 다섯 절 파일 위치 셀 결과 읽기에 그 사실을 한 문장씩 더함(마감 A-13) · README 「준비」에도 적음.
- **묶음 실행 검사 계약**: Part 7 `check_bundle_execution.py` 27행 `smoke_sections`가 **Ch 30 01**을 실행 → 01은 키·모델 객체·`dotenv`·포트·자식 프로세스·도구 파일 없이(같은 프로세스 `TestClient`, `runpy`로 `schemas.py`만). 01 `code_sha256` **`861cacdb64be1cf3bf7a5e8e712eab20cc46488075e16225f7f182699fb3337f`**. 01에 모델·키·도구 파일 가져오기를 넣지 말 것. 10(키·서버·모델 없음)은 목록 후보(스크립트 수정 필요 — §20).

## 8. 비유 가족 「화물 열차와 번호판 차량」 (삽화 열)

- 01-6 규격 틀이 없는 선로와 있는 선로(입력 형식) · 02-6 주황 기관차를 단 두 열차(남은 재정의) · 03-6 한꺼번에 돌아온 화물 열차(`ainvoke` 결과) · 04-5 한 칸씩 들어오는 화물 열차(스트림 사건·진행 값) · 05-5 이름판과 번호판을 단 화물 칸(SSE 사건·사건 번호) · 06-5 끊긴 자리에서 이어 온 열차(이어 받기) · 07-5 꼬리표 색이 맞는 트럭만 실은 짐(허용 출처 — 번호판 차량 처음) · 08-5 모형을 보고 만든 화물 칸(응답 문서·생성 SDK) · 09-5 짐 칸만 나가는 갈림길(노드 조건) · 10-4 세 가지 칸을 이은 열차(실습 흐름).
- **「짐칸」 짝**: 02(처리 함수)·03(결과 딕셔너리의 칸)은 다른 것과 짝지었고, 04·05부터 「짐칸 하나 = 사건 하나」 — 04 b4에 「02·03절에서는 짐칸을 처리 함수와 결과의 칸에 짝지었지만, 이 절부터는 짐칸 하나가 스트림 사건 하나입니다」를 더함(마감 A-6, 그림·02·03 글 그대로).
- 사람·손·글자·숫자·화살표·표지판·화면 없음 · 스타일 문구 규격 §5-4 · `nano_banana_pro` 16:9 2k · 작업 조회 결과의 모델 표시 `nano_banana_2`(기록만) · 흰 여백 넓은 채택본(03-6 위쪽 약 4분의 1·04-5 위아래)은 강사 확인 · 10-4 선로는 곧은 비스듬한 선(alt를 「비스듬히 곧게 뻗은」으로 — 마감 B-17).

## 9. 색 규칙 (Mermaid 42장)

- 보낸 요청·실습 폴더 파일·코드로 적은 자료 **초록(tool)** · 우리가 만든 앱 객체·처리 함수·함수 호출과 **값 바꿔 보기·실험에서 바꾼 값 파랑(flow)** · 출력으로 확인한 상태 코드·칸·받은 422(Before 아닌 결과) **노랑(measure)** · 라이브러리가 처리 함수 앞뒤에서 하는 일·두 조건 공통 값·설치판 소스로만 본 것 **회색** · **보라는 09의 실제 모델만** · **빨강은 paired Before 결함 결과만**(01-4 둘·02-4·03-4·06-4·07-3·07-4 하나씩).
- 마감에서 바로잡음: **10-3 실행 2의 접근 토큰 상자 초록 → 파랑**(08-4·09-4와 같게 — 검토 B-15) · 10-2 「첫 요청 200 · SSE 사건 일곱」 → 「첫 요청 200」(사건 일곱은 3절 값 — B-16) · 06-2 서로 다른 요청의 결과 둘을 처리 함수 상자에서 나란히 갈라지게(B-7). SVG 폭 최대 814(08-2), 868 이하.

## 10. 결정적 값과 흔들린 값

- 01~08·10: 모델을 쓰지 않는 그래프와 시험용 클라이언트라 상태 코드·칸·사건 수·사건 번호·판정이 매번 같음(새 커널 두 번 셀별 출력 같음, `outputs_sha256`이 갈린 절은 설치 셀 출력이 둘로 나뉜 모양 차이뿐).
- 09: 흔들림 확인 노트북 밖 5번(`09-probe.md` §0 11:18:44Z → 첫 요청 11:19:07Z) + 새 커널 두 번에서 구조 값·도구 인자·노드 차례·모델 글까지 같았음(질문 하나로만 확인). 결론·그림 라벨은 구조 값과 「도구를 한 번 부른 실행」 한정어가 붙은 값만 — 답 글·사건 수(21·20·35)·글자 수(32·43)는 결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만. 모델 글 `assert` 0.

## 11. 모델 요청 수와 예상 비용 (기록으로 다시 셈)

| 절 | 노트북 한 번 | 작업 전체 |
|---|---|---|
| 01~08 | 0 | 0 |
| 09 | 6(에이전트 실행 셋 × 요청 둘, 도구를 한 번씩 부를 때 — 5절만 사용량 든 청크로 직접 셈) | 약 42(흔들림 확인 5회 × 6 = 약 30 + 새 커널 A·B 6·6, 탐색·시험 실행 0) |
| 10 | 0 | 0(노트북 밖 5/5·새 커널 두 번·묶음 실행 모두 모델 없음) |
| 마감 | — | 0 |

- 요금표(2026-09-17) `gpt-5.4-mini` 입력 0.75·캐시 0.075·출력 4.50달러/100만 토큰으로 어림(청구 금액 아님): 실행 하나(요청 2) 약 0.00047달러 → 09 노트북 한 번 약 0.0014달러(준비물 「0.002달러보다 적습니다」) → 09 작업 전체 약 0.01달러. 절 상한 1달러 안.
- 10 실습 절 모델 요청 0은 규격 §7-2 「3~5번」과 다름(Ch 23·24 선례 — 강사 확인).

## 12. 10절 실습 절 — 끊긴 SSE 응답을 이어 받는 흐름에서 접근 토큰 하나만 바꾸기

- 도서관 웹 화면(허용 출처 `http://localhost:5173`)이 질문 「반납 기한을 알려 주세요」(스레드 `web-1`)를 `POST /v1/chat/stream`으로 받다가 SSE 사건 둘 뒤 끊겨 이어 받는 한 요청 흐름. 붙인 기능 05 SSE 응답·06 이어 받기·07 사전 요청과 접근 토큰 — 모두 실행 1 안에서 씀. 뺀 것과 까닭은 b3·`10-design.md` §2.
- 실행 1(교재용 접근 토큰): 기록 넷(사전 요청 · 첫 요청 · 사전 요청(이어 받기) · 이어 받기) 모두 `200 | http://localhost:5173` · `web-1:1` → `web-1:2` · 이은 사건 일곱 · done `True` · 기준 글과 같음 `True`. 실행 2(`Bearer wrong-token`만 바꿈): 사전 요청 200 · 첫 요청 401(허용 출처 붙음) · 기록 둘 · done `False`.
- **두 번째 사전 요청**(검토 B-1 — 코드 그대로): 첫 사전 요청의 답에 이미 허용 요청 머리 `Last-Event-ID`(07 출력)와 담아 둘 시간 600초(starlette `cors.py` 26·56행 기본값 — 노트북은 출력하지 않음)가 붙어 오고, 브라우저는 그 시간 안에 다시 묻지 않을 수 있음(MDN Access-Control-Max-Age, 2026-09-29 확인). 이 흐름은 **담아 둔 답이 없는 경우를 흉내 내어** 한 번 더 보낸다고 셀 [30]·10-2 도식 읽기·b7·복습 3에 한정(강사 확인 — 흐름에서 뺄지는 코드·기록·그림 셋을 바꿔야 해 마감에서 하지 않음).
- 코드 셀 21 · 코드 줄 116 · 검사 문장 333 · Mermaid 3 + 삽화 1 · meta 「실습 30분 · 새 용어 0」(챕터 시수 32h에 더하지 않음 — 01~09 meta 합 강의 10h·실습 22h = `chapter.json`) · `code_sha256` `7541bca1…`·`outputs_sha256` `defaca81…`.

## 13. 도구 파일 `notebooks/serve_tools.py` — 함수 표·해시 변천·생성기 대조 사슬

| 함수 | 배운 곳 | 옮긴 절(판) | 가져오는 절 |
|---|---|---|---|
| `positions_of(events, mode)` | Ch 25 01 | 04(첫 판) | 04 |
| `mode_order(events)` | Ch 25 02 | 04(첫 판) | 04 |
| `zero_timeout()`(`async def`) | Ch 30 02 | 06 | 06·07 |
| `join_tokens(stream_values)` | Ch 30 04 | 06 | 06·09·10 |
| `split_sse(body_text)`·`parse_sse(sse_text)` | Ch 30 05 | 06 | 06 |
| `read_events(body_text)`·`event_names(events)`·`token_values(events)`·`ended_with_done(events)` | Ch 30 06 | 09(+ `import json`) | 09·10 |
| `last_event_id(events)` | Ch 30 06 | 10 | 10 |
| `header_or_none(response, name)` | Ch 30 07 | 10 | 10 |

- 해시 변천: 04 **`e0a3a382…`** → 06 **`e1a1464d…`** → 09 **`ff663039…`** → 10 **`2f66bc6b504295f8a5293acd69de8e8104208827d7bae42c16c28729091508e1`**(마감 그대로, 66줄, 표준 라이브러리 `json`만 가져옴 — 설치 셀에 더할 것 없음). 함수마다 위 주석에 배운 곳, 셀 글은 처음 가르친 노트북 코드 셀과 글자까지 같음(검토 A·B 대조).
- **생성기 대조 사슬**(마감에서 모두 통과): `author_04`(`TOOLS_HEAD`·`TOOLS`·`check_tools`·`strip_later_imports`·쓰기 가드·`--tools-copy`) → `author_06`(`MOVED`·`TOOLS06`·`check_tools06`·가드) → `author_07`·`author_08` `__main__`(「가져오기 줄을 빼면 06 판으로 시작」) → `author_09`(`MOVED09`·`TOOLS09`·`check_tools09`·가드) → `author_10`(`MOVED10`·`TOOLS10`·`check_tools10`·`check_older_guards()`·가드). 디스크 파일 = `author_10.TOOLS10` `True`. **뒤에서 도구 파일을 바꾸면 `author_10.TOOLS10`으로 시작하는지 대조**(가져오기 줄을 더하면 `import json` 줄 다음에).
- **머리 설명 어긋남**(검토 A-9·B-18 — 고치지 않음): 1행 「앞 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다」는 04 판 글이라, 지금 함수 열둘 가운데 열은 이 챕터 02·04·05·06·07절 함수 · `zero_timeout` 위 주석 「…함수를 정의합니다」·`ended_with_done` 위 「After 판정:」은 셀 글을 그대로 옮긴 결과. 고치면 `author_04.TOOLS_HEAD`부터 06·09·10 판·가드·`check_older_guards()`·공개 목록 해시·zip이 함께 바뀜 → **Ch 24~29와 같은 전체 마감 한 항목**(최종 점검표 §2-13 6번에 Ch 30 줄).
- 앱 패키지 `agent_service/`는 도구 파일이 아니라 가르치는 대상(노트북이 가져와 줄을 출력함).
- **전체 마감 2026-09-30: 머리 줄 고침, 새 해시 `333e9a62eae2f692536dad18137464fa48a6e3366cd4d7b591e96c3888abe01d`**(검토 A-9·B-18 · 체크리스트 §2-13 6번). 1행 「앞 챕터에서 배운 평범한 함수를」 → 「앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를」, 7행(Ch 25 줄) 뒤에 「이 챕터 02·04·05·06·07절 노트북에서 처음 적은 함수 열은 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.」 한 줄(머리 설명 10 → 11줄 — 함수 열의 설명 주석+본문이 그 절 노트북 코드 셀에 글자 그대로 있음을 다시 확인). 나머지 머리 줄·`import json`·함수 열둘 본문은 AST·글자 같음. **그대로 둔 것**: `zero_timeout` 위 「시험용으로, 시간 제한 0초를 내놓는 함수를 정의합니다」·`ended_with_done` 위 「After 판정: …」(02·06 셀 글 그대로 — 규격 §2-7 글자 그대로, 새 머리 줄이 그 까닭을 말함 · 셀과 함께 바꿀지는 다음 재실행 몫). 생성기 안 판: 04 `e0a3a382…` → `63cd2864…` · 06 `e1a1464d…` → `39e56276…` · 09 `ff663039…` → `6117e78b…` · 10 = 디스크. 고친 생성기: `author_04.TOOLS_HEAD` 한 곳뿐(`author_06.TOOLS06`·`author_09.TOOLS09`·`author_10.TOOLS10`·`strip_later_imports`·`check_tools`·`check_tools06`·`check_tools09`·`check_tools10`·`check_older_guards()`·04/06/09/10 쓰기 가드·07/08 `__main__` 확인은 이 상수를 따라감, 챕터 안 판 해시 고정값 없음 — 앞서 Ch 25 머리 줄 고침으로 `author_04.STREAM_TOOLS_SHA`도 새 값). 조건 넷: (가) 노트북 열 마크다운·출력과 `_src`·HTML·README에 머리 글·판 해시 0 · (나) 열 생성기를 파일 쓰기를 가로챈 채(`.cache/final-close/2-tools-head/tools/dryrun.py`) `--src-only`(01~10)와 인자 없는 모드(04~10)로 돌림 → `_src` 열 바이트 같음, 04·06·09 가드 `skip`, 10 가드는 같은 글, 대조 함수 다섯 통과, `cells()`가 노트북과 49·53·49·49·53·57·47·47·49·45셀 같음 · (다) 도구 파일을 가져오는 모델 없는 04·06·07·10 사본(`.cache/final-close/2-tools-head/ch30/notebooks`, 키 없이, 커널 자리는 교재 출력 때와 같은 저장소 맨 위)을 새 커널로 돌려 셀별 23/23·26/26·21/21·21/21(06·07·10은 설치 셀 스트림 나뉨만) — 01~03·05·08은 도구 파일을 가져오지 않음, 모델 절 09는 가져오는 이름 다섯이 새 파일에 있고 함수 본문 AST가 옛 파일과 같음만 확인 · (라) 이 줄·handoff·계약 §4. 노트북 `code_sha256`·`outputs_sha256` 전후 같음.

## 14. 묶음·검사

- **묶음**: `python3 -B textbook/part7/_build_index.py`(README·`chapter.json`·목차 줄·continuity-guide·노트북·앱 파일을 모두 고친 뒤 마지막에 한 번) → **`Part 7: 30 verified sections; 110 bundled files`**, `part7-practice.zip` `1b3d4287…`(10절 작업 중간 판) → **`007f13875f117c4b452e7600d2055aee1198cc8e194cbf7b76043a9d7dc38951`**(113항목·110파일, **Ch 30 42파일이 디스크와 모두 같음**, `continuity-guide.md` 같음, `__pycache__`·`.pyc`·`.venv`·`.pytest_cache`·`.env`·`.openapi-generator/`·옛 `_generate.py` 0). `textbook/part7/index.html` `2eea2b9a` → `f5e86b4a`(Ch 30 설명 한 줄만) · `qa/integration-results.json` `b78c0f3e` → `70f89984`(`bundle_sha256`만). 공개 목록: 챕터 `qa/public-files.json` 42줄(도구 파일·10 노트북·`live_agent.py`·`agent.py` 있음, 옛 그림 줄·옛 생성기 줄 없음 — 그대로 `2aa4049b`) · Part 목록 `collect_public_files.py`로 다시 모아 **바이트 같음**(`12565fee`, `Explicit public files: 109; prerequisites: 1`).
- **묶음 실행 검사**: Part 7 `check_bundle_execution.py`는 **스크립트를 고치지 않고는 이 기기에서 돌 수 없음** — 노트북 실행기를 `labs/part7/ch31-database/.venv/bin/python`(맥 `.venv`, `/Users/mhso/.local/share/uv/python/…` 로 가는 링크)으로 박아 두어 환경 변수·인자로 바꿀 수 없고, 다섯 실습 폴더마다 `uv sync --locked`로 `.venv`를 만들어 기기 디스크(여유 약 1.5G)도 빠듯함. 그래서 **같은 일을 손으로**: 새 zip을 `/tmp/ch30-close/bundle`에 풀고 Ch 30 가상환경(`execute.py --cwd <풀린 notebooks> --kernel-python <venv python>`, `OPENAI_API_KEY` 지움, `PYTHONDONTWRITEBYTECODE=1`)으로 **01 PASS 22셀·10 PASS 21셀**, 저장 노트북과 셀별 출력 글자 **22/22·21/21 같음**(01 `outputs_sha256`은 설치 셀 출력이 나뉜 모양만 달라 `2004af60…`, 10은 `defaca81…` 그대로), `code_sha256` 같음, 풀린 폴더에 `__pycache__`·`.failure.json` 0. **`bundle-execution.json`(`65daf4ac…`)은 옛 zip 기준 그대로**(Ch 30 01 `code_sha256` `7bd57d1f…`·2026-09-11) — 전체 마감 몫(최종 점검표).
- **전달 검사**(Part 7 `check_delivery.py`, 고치지 않음): 절 30·링크 검사까지 지나 **`existing-artifacts-before.json`의 없는 파일(`textbook/part2/ch07-prompt-engineering/_src/index-body.html`)에서 `FileNotFoundError`로 멈춤**(알려진 일, 결과 파일 쓰기 전 — `qa/` 바이트 같음). 그 대조와 `llm-practice.zip`을 뺀 사본(`.cache/ch30-close/dx/check_delivery_noprior.py` — 바꾼 줄 넷: 루트·`prior`·zip 목록·결과 파일 자리)은 **절 30 · 코드 셀 325 · 깨진 링크 0 · `part7-practice.zip` 110파일 모두 디스크와 같음** 통과.
- **화면 검사** `visual.cjs`: **22행 PASS**(`textbook/_notebook/checks/ch30-fastapi-serving/visual-results.json` + 스크린숏 넷 새로). Part 7 공용 `qa/visual-results.json`은 **Ch 30 줄만 20 → 22**(`b377b3ea` → `b73d3e84`, 다른 챕터 줄 52 그대로).
- **옛 검사 스크립트(고치지 않음)**: `check_figures.py` — 옮기기 전 **PASS 29쌍**(Ch 30 옛 그림 아홉 쌍 포함, `figure-consistency.json` 바이트 같음) → 옛 생성기를 옮긴 뒤 **20행 `assert (figures / '_gen_figures.py').is_file()`에서 Ch 30 폴더로 멈춤**(알려진 충돌 — 결과 파일 쓰기 전) · `check_secrets.py` — **PASS 175파일·묶음 둘**, 결과 파일 `secret-scan.json`을 새로 써서(`source_files` 171 → 175) **실행 전 사본으로 되돌림** · `check_special_secret.py` — Ch 32 도커 PostgreSQL 검사라 돌리지 않음 · `collect_public_files.py` — 바이트 같음 · `check_bundle_execution.py` — 위.
- 게이트 `upgrade_gates.py … --label after` **10/10 PASS · G1~G7 0** · AST 따로(`extra_check.py`) 챕터 예외만·깊이 2 · `verify.py --chapter` **PASS 10 sections / 229 code cells (max 12 lines)**(계약 파일 `909267d7` 그대로) · 빌드 HTML 열하나 `{{`·`[[` **0건** · 인용 대조(§21).

## 15. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part7/ch30-fastapi-serving/notebooks/01~10-*.ipynb` | 01~10절 · **마감** | 실습 폴더(챕터 몫). 마감은 **마크다운 셀만**(재실행 0): 02 `b705c8aa`→`5f76e97b` · 04 `14427e45`→`3db234d4` · 05 `ef770d54`→`ec9713f1` · 06 `dafe2576`→`a262ab40` · 07 `4f57e333`→`648784d0` · 08 `767cdff1`→`f3f2723d` · 09 `f321fbe1`→`f3231412` · 10 `abb88056`→`c5bc7ed1` · 01 `c94af127`·03 `86aa1b08` 그대로. 열 노트북 `code_sha256`·`outputs_sha256`·`executed_at` 전후 같음 |
| `labs/part7/ch30-fastapi-serving/README.md` | 10절(한 단락) · **마감(전체)** | `e58431d2`(원본) → `0d8a6020` → **`96b70010…`**: 노트북 열 표·절별 설치 판·**모델 요청 01~08·10 0 · 09 6**·예상 비용(요금표 어림, 청구 금액 아님)·키는 `.env`의 `OPENAI_API_KEY`에서만(프로젝트 맨 위, 묶음이면 `part7-practice/`)·`uv sync --locked`·`notebooks/`에서 열기(도구 파일을 가져오는 다섯 절)·앱 패키지와 `tests/`(`uv run pytest -q`)·교재용 접근 토큰·서버 `uv run uvicorn agent_service.app:app --host 127.0.0.1 --port 8000`·TS 시험 **`node client/test_stream.ts`**(06 확인 명령, Node 22.23.2)·생성 SDK **`-i openapi.json … -o client/generated`**와 `tsc`가 **같은 폴더**를 검사·생성기 판 7.25.0(`openapitools.json` 고정, npm 감싸개 2.41.0은 고정 안 함)·`typescript@7.0.2`(교재 확인 판을 명령에 적음)·Java 11 이상(OpenJDK 11.0.32.1)·도구 파일 단락(규격 §2-7 고정 문장·함수 열둘의 배운 절·가져오는 절)·10 실습 단락. 옛 「결정적 LangGraph」·「교육용 토큰」·「헤더」·「스키마」·`uv sync`·`fastapi dev`·`npx tsx`·`-o generated-sdk` 뺌, 묶음 밖 파일을 가리키지 않음 |
| `labs/part7/ch30-fastapi-serving/agent_service/agent.py` | **마감(검토 A-10)** | 17·38행 설명 글만(`a6c42e63` → **`b8f73eb2…`**): 「외부 API 없이 서비스 계층을 검증할 수 있는 교육용 답을 만듭니다」 → 「모델 없이 서비스를 시험할 수 있게 정해 둔 말로 답을 만듭니다」 · 「실제 LangGraph 실행 객체를 구성합니다」 → 「노드 하나인 에이전트 그래프를 만들어 컴파일합니다」. 줄 수 46 그대로, 노트북 출력에 두 줄 없음, `app.openapi()` `06e5d1b9…` = `openapi.json`·정렬 `d2fb94f6…`·`pytest` 6 passed(`/tmp` 사본에서 먼저, 고친 뒤 다시) |
| `labs/part7/ch30-fastapi-serving/notebooks/_generate.py` → `textbook/part7/ch30-fastapi-serving/qa/upgrade/before/generators/blocked/notebooks_generate.py` | 01절(막음) · **마감(`mv -n`)** | `6c589718…` 같음 |
| `labs/part7/continuity-guide.md` | **마감** | 7행 「Ch2의 비동기 함수와 Ch25의 스트리밍 \| Ch30 HTTP 요청과 SSE 이벤트 \| …」 → 「Ch2의 비동기 함수, Ch19의 입력 형식, Ch25의 스트림 사건, Ch28의 ainvoke와 접근 토큰 \| Ch30 처리 함수와 의존성, ainvoke·astream, SSE 사건의 이어 받기와 오류 사건, CORS·시간 제한, 응답 문서와 생성 SDK \| …」 · 8행 「Ch21의 에이전트, Ch23의 저장 상태 \| Ch30의 호출 경계와 Ch31의 데이터 저장 \| …」 → 「Ch21의 에이전트, Ch23의 체크포인터 \| Ch30에서 HTTP 요청 주소로 부르는 에이전트(상태는 저장하지 않음)와 Ch31의 데이터·체크포인트 저장 \| …」(`b9ce0017` → `17b07239`, 보호 파일, 묶음에 들어감) |
| `textbook/part7/_build_index.py` | **마감** | 19행 ch30 설명 → 「처리 함수의 입력 형식과 의존성 재정의에서 시작해 ainvoke·astream과 SSE 사건의 이어 받기·오류 사건을 보고, CORS·접근 토큰·시간 제한과 응답 문서·생성 SDK를 확인한 뒤, 실제 에이전트를 HTTP로 부르고 한 요청 흐름을 잇는 실습을 합니다.」(시수 10·22 그대로, `1e6f3498` → `43525ed4`, 보호 파일) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | **마감** | 65행 Ch 30 설명 → 「처리 함수의 입력 형식과 의존성 재정의, ainvoke·astream과 SSE 사건의 이어 받기를 보고, CORS·접근 토큰·시간 제한과 응답 문서·생성 SDK를 확인합니다.」 **절 수 9 그대로**. 다시 만든 `index.html`에서 바뀐 것은 Ch 30 설명 한 줄(`b21bb749` → `db6ad12f` · `fc7fdde3` → `80aad0d4`, 보호 파일) |
| `textbook/part7/index.html` · `textbook/downloads/part7-practice.zip` · `textbook/part7/qa/integration-results.json` | 10절 + **마감** | §14 |
| `textbook/part7/qa/visual-results.json` · `textbook/_notebook/checks/ch30-fastapi-serving/visual-results.json`(+ 스크린숏 넷) | **마감** | §14 |
| `textbook/part7/qa/secret-scan.json` | **마감(되돌림)** | `check_secrets.py`가 새로 써서 실행 전 사본으로 되돌림(내용 변경 0) |
| `textbook/part7/qa/figure-consistency.json` | **마감(같음)** | `check_figures.py`가 다시 썼으나 바이트 같음 |
| `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀 — 마감 뒤 `909267d7` 그대로 |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 30 행 한 줄 · §2-13 6번에 Ch 30 줄, §2-18 Ch 30 항목, §3·§4 Ch 30 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md`(오케스트레이터 몫) · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`render_mermaid.py`·`attach_figures.py`·`count_code.py`) · Part 7 검사 스크립트 전부(`check_bundle_execution.py`·`check_delivery.py`·`check_figures.py`·`check_secrets.py`·`check_special_secret.py`·`collect_public_files.py`) · `bundle-execution.json`·`delivery-results.json`·`existing-artifacts-before.json`·`final-artifact-hashes.json` · 공개 목록 두 곳(바이트 같음) · 도구 파일(해시 고정 `2f66bc6b…`) · 앱 파일 `app.py`·`schemas.py`·`live_agent.py`·`__init__.py`·`tests/`·TS·생성 SDK·`openapi.json`·`pyproject.toml`·`uv.lock` · 삽화(Higgsfield 0) · `.moai` part7 스크립트 셋(01이 막은 판 그대로) · **Ch 31 이후 파일 전부**(Part 7 목차·묶음·공개 목록·기록·`continuity-guide.md` Ch 30 줄 말고 — Ch 31 01·05·Ch 32 01·02·Ch 34 04는 읽기만) · `llm-practice.zip` · claude.ai 프로젝트 문서.
- **파일을 지운 것은 없습니다.** 옮긴 것은 옛 생성기 셋(`mv -n`, 해시 같음 — §20). 옮긴 뒤 게이트(`gates-after.json`)·`_build_index.py`·손 묶음 실행·`check_delivery.py` 사본이 통과(`_build.py`·`run_section.sh --no-exec`는 옮기기 전에 돌렸고 옛 생성기를 부르지 않음 — `grep`으로 부르는 스크립트는 Part 7 `check_figures.py` 20행뿐).
- **보호 파일 255개(`before-manifest.json`)**: `manifest-changes.md` 「마감 뒤」 — §21.

## 16. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `fastapi[standard-no-fastapi-cloud-cli]==0.135.0`·`httpx==0.28.1`·`langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`pydantic==2.12.5`·`python-dotenv==1.2.1`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`pytest==9.0.2`·`pytest-asyncio==1.3.0`): `starlette 1.6.0`·`langchain-core 1.6.2`·`openai 3.13.0`(요청은 `httpx2` 2.12.0으로 — 09 요청 수 감시가 0을 낸 까닭)·`uvicorn 0.52.4`. 노트북 `%pip`: 01 넷 · 02~08·10 여섯 · 09 여덟.
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch30-fastapi-serving`(잠금 판). 실행일 2026-09-29(01 06:32 · 02 07:10 · 03 07:42 · 04 08:16 · 05 08:53 · 06 09:32 · 07 10:12 · 08 10:49 · 09 11:36 · 10 12:23 UTC — 마감 재실행 없음). 모델 `gpt-5.4-mini`(09만).
- 노트북 밖 도구(README 명령 — 노트북에서 실행하지 않음): Node.js 22.23.2(`node client/test_stream.ts` — 06) · OpenAPI Generator 7.25.0(npm 감싸개 2.41.0, OpenJDK 11.0.32.1 — 08) · `typescript` 7.0.2(08).
- 참고 자료(절 작업·검토·마감 WebFetch 2026-09-29): FastAPI SSE·CORS·Testing Dependencies·Stream JSON Lines·Concurrency · MDN `EventSource()`·CORS·**Access-Control-Max-Age**(마감 — 10 b7·b10) · WHATWG SSE · LangGraph Streaming · LangChain Agents · OpenAI `gpt-5.4-mini` · OpenAPI Generator 설치(Java 11) · RFC 9110.

## 17. 강사 확인 대상

1. **제목의 영어와 말**: 챕터 「FastAPI로 Agent 서빙」 · 01 「라우팅」·「스키마」 · 02 「주입」 · 03 「ainvoke」 · 04 「astream」 · 05 「이벤트」 · 06 「fetch」·「재연결」·「이벤트」 · 07 「CORS」·「타임아웃」 · 08 「OpenAPI」·「TS SDK」 · 09 「Agent」·「HTTP」·「통합」 · **10 긴 제목**(「서빙」). 본문 첫 자리에서 「제목의 ○○은 …」으로 한 번씩 풂. 슬러그 01·04·09는 Ch 25·29 링크로 고정.
2. **코드 양**(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」, 검토 A-11): 코드 줄 305 → 1,264(01 110·02 105·03 100·04 111·05 159·06 152·07 123·08 137·09 151·10 116) + 도구 파일 66줄 · 코드 셀 45 → 229. 줄인다면 05 4절 응답 문서 비교(`itemSchema`, 셀 [49]·[50])를 08로 넘기는 안(05 재실행 — 모델 없음).
3. **새 용어 26개**와 말: 「사전 요청」(Ch 29 금지어 「사전」과 다른 낱말) · 「CORS 층」(「미들웨어」 대신) · 「노드」(Ch 29 금지 목록에 있으나 씀) · 「스트림 청크」를 09에서만 · **「스레드」 두 뜻**(Ch 2 12 실행 흐름 ↔ Ch 23 대화 — 05에 가르는 문장만 둠, 과정 요약에 올릴지).
4. **앱 파일 문법 예외**(§6)와 그 근거를 규격·과정 요약에 적을지 · 06·07이 출력한 앱 줄의 과정 밖 문법(f-string·`removeprefix`·`str | None`·`raise … from`)을 「뜻만 봅니다」로 둔 판단 · 05 실험의 새 API 이름 `add_api_route`.
5. **도구 파일에 `async def zero_timeout`**(L7 조건 안이라 둠) · 도구 파일 머리 설명(§13 — 전체 마감 항목).
6. **09 판단**: 앱 파일 `live_agent.py`의 모델 설정(09가 21행 `reasoning_effort="none"`을 더함 — 게이트 G4는 앱 파일 안 설정을 보지 못함) · 흔들림 확인을 질문 하나로만 한 것 · 3·4절 요청 수를 셈으로만 · `/v1/chat/live`의 시간 제한 오류가 504가 아니라 500(서버 오류를 올리지 않게 설정한 시험용 클라이언트에서 — 마감 B-10) · 45.0초가 코드에 박혀 재정의 불가.
7. **10 판단**: **두 번째 사전 요청**(검토 B-1 — 설명만 「담아 둔 답이 없는 경우를 흉내 냄」으로 한정, 흐름에서 뺄지) · **모델 요청 0**(규격 §7-2 「3~5번」과 다름, Ch 23·24 선례) · 바꾼 값 접근 토큰(07 401의 되풀이 — 「새로 볼 것」을 실행이 보인 만큼만).
8. **07 paired After ②**: 실습 앱의 401 결함(Before ②)을 같은 앱에서 고친 판이 없고, After는 새 앱의 `HTTPBearer`(검토 B 사람이 정할 것 2).
9. **그림 색**: 실험에서 바꾼 값 파랑(10-3을 마감에서 파랑으로 — 챕터 약속, 08-4·09-4와 같게).
10. **삽화 열 장**: 03-6 위쪽 약 4분의 1·04-5 위아래 흰 여백(재생성 한도를 써 관계가 맞는 1차 채택) · 06-5 계단 모양 안 나옴 · 07-5 자루 넷(설계 셋) · 10-4 곧은 선로(alt 고침) · 작업 조회 결과의 모델 표시 `nano_banana_2`와 요청 `nano_banana_pro`가 다름(기록만).
11. **README 판 적기**: `typescript@7.0.2`를 명령에 적음(교재 확인 판) · npm 감싸개 `@openapitools/openapi-generator-cli`는 판을 적지 않음(생성기 판은 `openapitools.json` 7.25.0) — 둘 다 적을지.
12. **`chapter.json` 학습 목표 셋 → 여덟**(「라우트」·「이벤트」·「재연결」·「OpenAPI」·「타임아웃」·「Agent」를 뺌, 10 실습 줄 더함, `hours` 그대로 32h = 강의 10h + 실습 22h = 01~09 meta 합) · `_build_index.py`·`build_index.py`·`continuity-guide.md` Ch 30 문구 · README 다시 쓴 범위.
13. **`.moai` part7 스크립트 셋**: 01이 맨 위 `raise SystemExit`로 막음 — Ch 31~34도 다루므로 처분은 사용자·강사.
14. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: 브라우저 CORS 동작·사전 요청 담아 두기, 삽화 PNG 눈 판독(검토 A), Windows·macOS 실제 실행, 학생 `uv sync --locked` `.venv` 첫 셀).

## 18. Ch 31이 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 10 b8·노트북 정리 끝(마감 B-3): 「Ch 31은 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다. Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장합니다. 이 챕터의 실습 앱에 붙이는 일은 다루지 않습니다. 보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다.」 — Ch 31 `_src`·05 노트북(`PostgresSaver.from_conn_string`·`compile(checkpointer=saver)`, Ch 30 앱·`fastapi` 가져오기 0)으로 확인. 06 b7 「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」와 같은 뜻, 08·09에는 Ch 31 문장 없음(09 b8은 10절을 가리킴).
- Ch 31 01 b2·b3 「Ch30에서 FastAPI 요청 함수/경로 함수를 비동기로 작성했습니다」 — **참**(01 `async def` 처리 함수). 말 「요청 함수」·「경로 함수」는 Ch 30 말이 아님(Ch 30은 「처리 함수」, 「경로」는 금지어) — Ch 31 개선 때 맞출 것(§19).
- 말: 처리 함수·요청 주소·요청 방식·의존성·제공 함수·재정의·요청 머리·응답 머리·SSE 사건·사건 번호·이어 받기·오류 사건·사전 요청·허용 출처·CORS 층·응답 문서·생성 SDK·시험용 클라이언트.

### 전제하면 안 되는 것 (Ch 31 파일은 고치지 않았습니다)

1. **Ch 30은 SSE 사건·에이전트 실행을 저장하지 않습니다**: 데이터베이스·파일·`runs/` 0, 계약 파일 0. 이어 받기는 서버가 그래프를 처음부터 다시 실행하고 앞 자리를 건너뛰는 방식(저장한 사건을 다시 보내는 것이 아님 — 06·10 b7).
2. **실습 앱은 체크포인터를 쓰지 않습니다**(`agent.checkpointer` `None` — 06 출력) · `thread_id`는 사건 번호 앞머리(`web-1:0`)와 응답 본문에만 · `lifespan` 없음 · 연결 풀·트랜잭션·SQLAlchemy·Alembic·pgvector 0. **Ch 31 05의 `PostgresSaver`는 Ch 30 앱과 이어지지 않습니다**(Ch 31 05는 제 그래프에 붙임).
3. **모델은 09만**(`live_agent.py` `openai:gpt-5.4-mini`, `temperature=0`·`reasoning_effort="none"`·`timeout=30`) — `/v1/chat`·`/v1/chat/stream`은 모델을 쓰지 않는 그래프. 10 실습도 모델 요청 0.
4. 인증은 요청 머리 매개변수 `authorization`을 읽는 제공 함수 `require_token`(환경 변수 `DEMO_API_TOKEN`이 없으면 `local-demo-token`) — **응답 문서에 보안 방식 칸 없음**(`HTTPBearer`는 07·08 노트북의 새 앱에서만), 401에 `WWW-Authenticate` 없음, CORS 허용 출처는 `http://localhost:5173` 하나.
5. 시간 제한: `/v1/chat` 504(`asyncio.wait_for`, 제공 함수 `get_timeout` 2.0) · `/v1/chat/stream` 200 + 오류 사건 `stream_failed` · `/v1/chat/live` 500(45.0 고정) · `/v1/chat/live/stream` 오류 사건 `live_stream_failed`.
6. 노트북은 모두 같은 프로세스의 시험용 클라이언트로 요청(서버 프로그램 0 — uvicorn은 06 TS 시험을 노트북 밖에서 한 번) → 도착 시각·「실시간」·걸린 시간 주장 없음. 브라우저에서 CORS를 실행한 적 없음.
7. **앱 파일 문법 예외는 이 챕터 결정**(§6) — 규격에 없음. Ch 31이 SQLAlchemy 모델 클래스·비동기 세션을 쓰려면 그 챕터가 따로 정할 것.
8. 도구 파일 `serve_tools.py`(10 판)는 Ch 30 실습 폴더에만 — 다른 챕터 폴더에서 파일째 가져오지 말 것(잠금이 다름).

## 19. 뒤 챕터 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 30 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 31(대기) | 01 b2 「Ch30에서 FastAPI 요청 함수를 비동기로 작성했습니다」 · b3 「Ch30에서는 FastAPI 경로 함수를 비동기로 작성했습니다」 | 참 · 말만 다름 | Ch 30 말 「처리 함수」(「경로」는 금지어) | Ch 31 개선 때 「처리 함수」로 |
| Ch 31 | 05 「에이전트 서비스는 검색 문서와 실행 상태를 같은 PostgreSQL에 저장할 수 있습니다」 | 참(Ch 31 제 그래프) | Ch 30 10 b8이 이 사실을 가리킴 | 없음 |
| Ch 32(대기) | 01 「Ch30의 서비스 구현이 아직 없어도 실습할 수 있도록」 · 02 「아직 작성 중인 Ch30 파일을 요구하지 않습니다」 | 「아직 없어도」·「작성 중인」은 옛 사정 | Ch 30 실습 앱은 있음(요청 주소 다섯) · Ch 32는 제 `app.py`로 독립 | Ch 32 개선 때 「Ch 30 실습 앱과 따로」로 |
| Ch 34(대기) | 04 b3 「Ch 30에서는 FastAPI 비동기 요청 처리를 배웠습니다」 | 참 | 01~05 비동기 처리 함수·`ainvoke`·`astream` | 없음 |
| 과정 요약(오케스트레이터) | §5 용어 · §2-19 예외 · §7 실습 절 선례 | Ch 30 줄 없음 | §4 용어(「스레드」 두 뜻 포함) · §5 비동기 허용 범위 · §6 앱 파일 문법 예외 · 10 모델 0 실습 | Part 7 누적 문서 |
| `upgrade-contracts.md` | §5 묶음 | 옛 zip | 새 zip `007f1387…` · `bundle-execution.json`은 옛 값(Ch 30 01 `7bd57d1f…` → 지금 `861cacdb…`) | 전체 마감 |
| 전체 마감 | `llm-practice.zip` 안 Ch 30 | 옛 판 | `part7-practice.zip`은 새 판 42파일이 디스크와 같음 | 전체 묶음 재생성 때 대조 |

## 20. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-18)

1. **옛 그림 스물일곱 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~9 — 세어 27개·약 180KB, 본문 참조 0, 공개 목록 줄 없음, 사본 `qa/upgrade/before/figures/`, 캡션에 「헤더」·「식별자」·「이벤트」·「반환」·「명시」·「라우트」·「Agent」). Part 7 `check_figures.py`가 `.excalidraw` 짝과 `_gen_figures.py`를 요구하는 것과 함께 정할 것.
2. **`gates-wip-*.json` 스물하나 삭제 승인**(`gates-wip-01-01`~`10-10`·`01`~`10`·`ch30-after10` — `gates-after.json` 10/10으로 갈음, 절 번호 아홉은 마감 `run_section.sh`가 다시 씀).
3. **캐시·임시 삭제 승인**: 챕터 `qa/upgrade/__pycache__/author_05.cpython-310.pyc`(70,814바이트, 09:01 — 검토 A-12) · 실습 폴더 `agent_service/__pycache__/`(pyc 다섯)·`tests/__pycache__/`(pyc 둘 — 모두 2026-09-11 macOS 판)·`.pytest_cache/`(16KB) · 실습 폴더 `notebooks/__pycache__/`는 **없음**(모든 실행 `PYTHONDONTWRITEBYTECODE=1`) · 실습 폴더 `.venv`(macOS 판 171MB) · `.cache/vm/venv-ch30-fastapi-serving`(254MB) · `.cache/ch30-01-view`~`ch30-10-view`(약 13MB) · `.cache/ch30-close/`(마감 전 사본 `pre/`·`qa-pre-checks/`·`qa-pre-delivery/`·확인 스크립트 `tools/`·치환 목록 `reps/`·전달 검사 사본 `dx/`·로그 `log/`, 약 26MB) · 기기 `/tmp/ch30-prep`(80KB)·`/tmp/ch30-01`~`/tmp/ch30-10`(약 297MB — **`/tmp/ch30-08/npm-cache` 191MB 포함**)·`/tmp/ch30-close`(약 5MB — 앱 사본 `app`·`app2`, 묶음 풀기 `bundle`, 사전 게이트 `pregate`) · `/tmp/reviewA30`·`/tmp/reviewB30`(검토 재현 파일, 약 2MB).
4. **묶음 실행 검사**: `check_bundle_execution.py` 실행기(`labs/part7/ch31-database/.venv/bin/python` — 맥 링크)를 고치거나 기기 판으로 바꾼 뒤 새 zip(`007f1387…`)으로 다시 돌려 `bundle-execution.json`(지금 옛 zip·Ch 30 01 `7bd57d1f…` 기준)을 갱신. **10을 목록에 넣을지**(키·서버·모델 없음 — 넣으면 계약이 생김).
5. **Part 7 옛 검사 스크립트(고치지 않음)**: `check_figures.py` 20행 — 옛 생성기를 옮겨 Ch 30에서 멈춤(옛 그림 삭제와 함께 검사 쪽을 고칠지) · `check_delivery.py` — `existing-artifacts-before.json`의 없는 파일(Part 2 Ch 7 `index-body.html`)에서 멈춤, `llm-practice.zip`도 대조 대상 · `check_secrets.py` — 통과하나 결과 파일을 새로 씀(되돌림).
6. **도구 파일 머리 설명**: §2-13 6번 Ch 24~29 한 항목에 Ch 30 줄(§13).
7. **앱 파일 문법 예외를 규격에 반영할지**(§6 — 규격 §2-2 L5·L6·L7 + 과정 요약 §2-19 근거, 새로 넓힌 것은 처리 함수·제공 함수 매개변수 힌트와 비동기 생성기 `yield`).
8. **`.moai` part7 스크립트 셋**(`part7_apply_depth.py`·`part7_review_fixes.py`·`part7_final_repairs.py` — 01이 맨 위 `raise SystemExit`로 막음, Ch 31~34도 다룸): 옮길지·지울지 사용자·강사.
9. **README 판**: `typescript@7.0.2`는 명령에 적고 npm 감싸개는 적지 않음 — 둘 다 적을지(§17-11).
10. **옛 기록 파일**: `qa/research.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용 그대로 — 뒤 둘은 끝 「마감」 절) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음) · `figures/*.prompt.md`(생성 기록 — 10-4에 마감 한 줄).
11. **과정 요약·계약(누적 문서 몫)**: §19 과정 문서 줄 · 도구 파일 `serve_tools.py`(`2f66bc6b…`, 함수 열둘)는 과정 요약에 아직 없음 · `run_section.sh`의 `--with python-dotenv==1.2.3` ↔ 잠금 1.2.1(공용 도구, 기록만).
12. **뒤 챕터 문장**(§19): Ch 31 01 「요청 함수·경로 함수」 · Ch 32 01·02 「아직 없어도·작성 중인 Ch30 파일」.
13. **2차 검토**: 두 검토의 「확인하지 못한 것」과 §17-14.

## 21. 검토 1차와 반영 (2026-09-29 마감)

- 판정: **A(01~05·공통) 상 1 · 중 1 · 하 12**, **B(06~10) 중 4 · 하 14**. 합 **[상] 1 · [중] 5 · [하] 26 = 32건**.
- **[상] 1건 반영 — A-1**(05 인용): 셀 [22]의 `data: {"token": "…"}` 인용·셀 [34]의 `칸 data의 글: …` 인용을 **출력 글자 그대로**(한글 대신 유니코드 이스케이프 — 백슬래시·u·네 자리)로, 「`질`처럼 유니코드 번호로」를 「「질」이 이스케이프 모양으로 적히듯, 유니코드 번호로」로(뜻이 거꾸로 읽히지 않게). `author_05.py` 450·455·504행 → 메모리 치환 도구(아래) → `--no-exec` → `_build.py`. 본문 `_src`에는 한글이 든 `data` 인용이 없었음(노트북 셀이 빌드 HTML에 들어감). 인용 대조를 **숫자 없는 백틱 인용까지** 열 절 전부 다시 돌림(`.cache/ch30-close/tools/quotes30.py` — 노트북 마크다운 1,330·`_src` 1,255): **출력 값 인용인데 출력에 없는 것 0건**(남은 108건은 파일 이름·설치판 파일·API 이름·노트북 밖 확인 값(01 `string_too_long`·06 `sse-1:-1`·08 `GET /v1/ping` 등, 본문이 「노트북 밖에서」로 한정)·다른 절 출력 인용(06 [30]이 05 출력 `{'token': '질문을 '}`를 가리킴)).
- **[중] 5건 모두 반영**: **A-8**(README 전체 — §15) · **B-1**(10 두 번째 사전 요청 — 코드 그대로, 셀 [30]·10-2 도식 읽기·b7(새 목록 항목)·복습 3 물음·해설·b10 참고 자료(MDN Access-Control-Max-Age, starlette `cors.py` 26·56행)를 「첫 답에 이미 `Last-Event-ID`·600초 → 브라우저는 다시 묻지 않을 수 있음 → 담아 둔 답이 없는 경우를 흉내 냄」으로. b3은 두 번째 사전 요청의 까닭을 적지 않아 고칠 곳 없음) · **B-2**(08 b4 말뜻 표·노트북 [26] 「파일 열여덟(TS 파일 열하나와 설명 문서 일곱)」, 08 진단 같은 말) · **B-3**(10 b8·노트북 [44] — §18) · **B-4**(07 b8·노트북 [46] 「응답 문서를 실습 폴더의 파일과 견주고」).
- **[하] 26건 가운데 22건 반영**: A-2(05 b7·b10 「1192행이 `routing.py` 1292행의 같은 이름 메서드를 부르고 데코레이터 줄도 그 메서드를」, 노트북 [40] 「같은 이름의 메서드」) · A-3(01-5 도식 읽기 「After 앱의 입력 형식에 대한 사실」) · A-4(05 노트북 [12]·b4·b7에 「스레드 = 칸 `thread_id`의 대화(Ch 23 01), 01·03의 실행 흐름 스레드(Ch 2 12)와 다른 뜻」 — 01에는 더하지 않음, 06·09·10의 「스레드 이름」은 05 정의를 이어 씀) · A-5(02 노트북 [2]·b2 「FastAPI 문서의 말 injection을 옮긴 말」) · A-6(04 b4 한 문장 — §8) · A-7(`04-figures.md` 04-5 행) · **A-10**(`agent.py` 17·38행 — §15, 조건 모두 맞음) · A-13(04·06·07·09·10 파일 위치 셀 결과 읽기에 한 문장 — 셀 코드 그대로) · A-14(§6에 규칙, 규격 반영은 사람이 정할 것) · B-5(06 b7 실제 방법 — uvicorn·`node client/test_stream.ts`) · B-6(06 [40] 「실습 폴더 `README.md`에 있습니다」) · B-7(06-2 다시 그림 — §9) · B-8(06 [26] `str | None`·`= None`·`-> int` 풀이, 07 [12] 「06절에서 본 모양」) · B-9(07 [29] 스크립트가 적는 접근 토큰 ↔ 브라우저가 붙이는 쿠키) · B-10(09 b7 「서버 오류를 올리지 않게 설정하자 500, 기본 설정에서는 오류가 그대로」·복습 3) · B-11(09 [40] 셈의 조건 두 문장) · B-12(09 「대역 객체」 → 「따로 만든 시험용 객체」 — 본문 셋 모두) · B-13(`09-probe.md` 탐색 차례) · B-14(10 [2] 「라이브러리 이름과 문법만, 흐름을 잇는 함수만 새로」) · B-15(10-3 실행 2 파랑) · B-16(10-2 「첫 요청 200」) · B-17(10-4 alt 「비스듬히 곧게」).
- **미반영 4건과 까닭**: ① **A-9·B-18 도구 파일 머리 설명** — 챕터 리드 결정(도구 파일 해시 `2f66bc6b…` 고정, 바꾸면 04→06→09→10 생성기 대조 사슬·공개 목록·zip 해시가 함께 바뀜) → Ch 24~29와 함께 전체 마감 한 항목(§20-6) ② **A-11 코드 양** — 강사 확인(§17-2), 줄이려면 05 코드 셀을 바꿔 다시 실행해야 함 ③ **A-12 `qa/upgrade/__pycache__/`** — 지우지 않고 삭제 승인 목록(§20-3). 그 밖에 **B-1의 「흐름에서 두 번째 사전 요청 빼기」 선택지**는 코드 셀을 바꿔야 해 반영하지 않고 설명만 고침(강사 확인 §17-7).
- **마감이 더 고친 것(검토 밖, README 다시 쓰기에 딸린 사실 맞춤)**: 08 b7 「README의 TS 검사 명령 `npx --package typescript@latest tsc …`는 판을 고정하지 않아」 → 「판을 적은 `npx --package typescript@7.0.2 tsc …`」 · 08 b7 「README는 시험 파일을 `tsx`로 실행하라고 적고」 → 「README의 시험 명령은 직접 적은 시험 파일 `client/test_stream.ts`를 Node.js가 바로 읽는 방식으로 실행, 06절에서 통과」 · **사용자가 금지한 표현(과정 규칙) 바꿈**: 챕터·실습 폴더 전체 `grep`에서 글자 그대로 나온 세 곳 — `qa/upgrade/02-diagnosis.md` 16행·`03-diagnosis.md` 16행·`handoff.md` 107행(금지어 목록 줄) → 「사용자가 금지한 표현(과정 규칙)」(원고·노트북·생성기에는 없었음, `before/` 사본에도 없음 — 기기 `/tmp/ch30-01/tools/ban30.py`의 금지어 목록은 챕터 밖 도구라 그대로).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자 — 모두 같음, `executed_at` 같음, `metadata.verification`과 다시 셈한 값 같음): 01 `861cacdb64be`/`87ea510f027a` · 02 `c52cc10f2017`/`2003205a3569` · 03 `eb33867b5939`/`5d7bc81af099` · 04 `2b5a740d6f1d`/`e7a37a53a546` · 05 `662e8a3e9119`/`85e481f72c0f` · 06 `21a623d11a53`/`e1b573c11c41` · 07 `e9a38985d456`/`ff1e1ec601d4` · 08 `eddd600d09d6`/`3ac7d06e34cb` · **09 `30c6e2033d05`/`ead89bbaaee0`** · 10 `7541bca126e4`/`defaca81a09f`.
- **다시 렌더한 `.mmd`**: 06-2(B-7) · 10-2(B-16) · 10-3(B-15) — 셋 모두 본문에만 있는 그림(노트북 첨부 아님), PNG를 열어 확인. 캡션 파일은 생성기 `FIGn_CAP`과 모두 같음(`capsync30.py`).
- 고친 방법: `.cache/ch30-close/tools/gapply30.py`(Ch 29 `gapply29.py` 판 — 생성기 문자열 치환 수를 확인하고, 바뀐 생성기를 메모리에서 실행해 **코드 셀이 노트북과 한 글자라도 다르면 멈추고**, 달라진 마크다운 셀만 노트북에 옮긴 뒤(첨부·메타데이터 그대로) `src_html()`로 `_src`) · `pregate30.py`(쓰기 전 G1~G6를 `/tmp` 임시 노트북으로) → `run_section.sh … NN --no-exec`(01·02·04~10) · `genmatch30.py`(열 생성기 셀·`src_html()` = 노트북·`_src`) · `bandiff30.py`(금지어 수 전후 — 늘어난 것은 「사전 요청」·「노드」·「접근 토큰」 같은 허용 말뿐) · `manifest_check30.py`.
- **보호 파일 255개**: **같음 197 · 바뀜 55 · 옮김 3**(10절 뒤 210 · 45 · 0) — 바뀜 가운데 44가 마감에서 바뀜(파일별 표는 `manifest-changes.md` 「마감 뒤」), 모두 의도한 변경.

## 22. 절차 메모

- 마감은 기기 셸 한 곳에서만 작업(`mcp__remote-devices__device_bash`, 셸 호출마다 `timeout` 170 안팎). 모델 요청 0 · 삽화 생성 0 · 파일 삭제 0 · 모든 파이썬 호출 `PYTHONDONTWRITEBYTECODE=1`(실습 폴더·`qa/` pyc 새로 0 — 챕터 `qa/upgrade/__pycache__/`의 pyc 하나는 절 작업 때 것) · 키 값 출력 0(`.env`를 열지 않음, 앱·묶음 실행은 `OPENAI_API_KEY`를 지우고) · 서버 0 · 남은 프로세스 0.
- **도구 호출 글에 백슬래시·u·네 자리 16진수를 그대로 적으면 전달 과정에서 한글로 바뀝니다**(05 A-1 치환 파일이 처음에 한글로 바뀜) — 파이썬에서 `chr(92)`로 이어 만들어 씀.
- 챕터 폴더 전체를 `grep`할 때 `.venv`를 빼야 셸 시간 제한에 걸리지 않음.
