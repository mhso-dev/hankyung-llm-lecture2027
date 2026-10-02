# 09절 진단 — 실제 Agent HTTP 통합 (experiment)

- 작업일: 2026-09-29 · 작업자: 09절 작업자 · 생성기 `qa/upgrade/author_09.py`(`0ef09813…` — `mdpatch.py` 두 번 뒤 값) · 흔들림 확인 `qa/upgrade/09-probe.md`·`probe/probe09.py`·`probe/probe-09.jsonl`
- 읽은 것: `handoff.md`(머리·챕터 공통 전부·§07 → §08·§08 → §09 전부) · 준비 노트 `chapter-lead-notes.md`(§0·§1 09 줄·§2 09·§8·§9·참고 자료) · `08-diagnosis.md`·`08-figures.md` · `author_08.py`(전부)·`author_06.py`(도구 파일 06 판 사슬·`check_tools06`·06 함수 셀 글)·`author_04.py`(`TOOLS_HEAD`·`strip_later_imports`·가드)·`author_07.py`(`__main__`) · Ch 28 `04-probe.md`·`probe/probe04.py` · Ch 29 `author_04.py`(요청 수 셈 줄) · Ch 25 02 노트북(모드 messages·칸 metadata·사용량 든 청크) · `AGENT-BRIEF.md`·`PLAYBOOK.md`·규격 전부 · 과정 요약(§2-16~2-20·§3·§6·§8·§9) · 옛 09 `_src`·노트북(`before/`) · 실습 폴더 `live_agent.py`·`app.py`·`__init__.py`·`pyproject.toml`·`uv.lock`·`tests/test_app.py`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-09.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 5 · 2 · 6 · 0 · 8 · 19 · 3 = **43** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(주석·빈 줄·`%` 줄 뺌, `extra_check.py`) | 6 · 54 | **23 · 150** |
| 검사 문장 | 102 | **395** |

- 첫 실행 전 `upgrade_gates.py … --label wip-09 --section 09`: 1회차 G1·G2 0, G6 8(70자 넘는 문장 다섯 — b4·b7 둘·b8 머리 포함·준비물 패키지 줄 / 영문 시작 조사 셋 「temperature를」·복습 해설 코드 시작·「token이」) → 문장을 나누고 「모델 설정 temperature를」·「두 설정은 …」·「사건 이름 가운데 token이 아닌 것은」으로 · 2회차 G6 1(준비물 「기준 버전」 단락 여섯 문장) → 한 문장을 다음 단락으로 · 3회차 G1~G6 0(G7 3은 그림 전이라 당연). 새 커널 A 뒤 G5 4(STREAM_JOIN 결과 읽기 첫 단락에 출력 인용 없음 · COLLECT 첫 단락 `event[0]`·`event[1]` · 결과 표 첫 단락 `09:00~18:00`이 그 셀 출력에 없음) → `mdpatch.py`로 마크다운만(라벨 `token 사건 수:`·`이어 붙인 글:` 인용 · 「앞 값과 뒤 값」 · 인용 뺌) → **G1~G7 0 PASS**.
- AST 따로(`/tmp/ch30-09/tools/extra_check.py` — 08 도구 그대로): 걸린 것은 **챕터 예외 하나뿐** — 셀 맨 위 `async for` 하나(COLLECT, 04절 모양). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`getattr`·`isinstance`·`while`·`try`·`raise`·별표 풀기·대입 풀기(for 포함)·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·클래스·데코레이터·딕셔너리 `.get`·`.items`·`sorted`·`set`·`join`·`asyncio`·셀 맨 위 await **0**. 호출 깊이 최대 **2**(첫 판 3 — `list(live_agent.get_graph().nodes)` → `graph_view`로 나눔) · 준비 셀 밖 셀 최대 **9줄** · 함수 본문 최대 **7줄**(`node_order`) · 셀당 정의 하나. 도구 파일 09 판은 `async def zero_timeout`(06 판 그대로)만.
- 금지어(`/tmp/ch30-09/tools/ban30.py` — `_src`·노트북 마크다운·코드 주석·`.mmd`·캡션·alt): 걸린 것은 **허용한 것과 거짓 양성뿐** — 「노드」(Ch 13 말, 03~08과 같음) · 「스트림」·「청크」(「스트림 청크」·「스트림 사건」 — Ch 25 02 말, 「스트림 청크」는 09에서 씀 — 04 결정) · 「의존성」(02 말) · 「Agent」(제목 풀이 「제목의 Agent는」 한 번 + 참고 자료 원제목 「LangChain Agents」 + 노트북 제목 셀) · 「로그」(← 「프로그램」) · 「트리」(← 「스트리밍」). 1회차의 「안내 글」(키 셀 결과 읽기) → 「키를 적으라는 글」. 「엔드포인트」·「경로」·「라우트」·「스키마」·「필드」·「헤더」·「반환」·「검증」·「측정」·「지연」·「결정적」·「보장」·「메타데이터」·「조각」·「토큰」 단독·「평가셋」·사용자가 금지한 표현·「쉽게·간단히·당연히」 **0**.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/09-…ipynb`·`before/_src/09-*.html`)

1. **규격 §3 위반**: 모델 글 `assert '18:00' in response.json()['answer']`·`assert '18:00' in live_answer` · 모델이 고른 인자 `assert tool_call['args']['day'] == '월요일'`.
2. **모델 설정이 앱 파일 안에 `reasoning_effort` 없이**(`live_agent.py` 18~22행 `temperature=0, timeout=30`) — 노트북에 모델 셀이 없어 게이트 G4도 보지 못함.
3. 궤적 셀이 HTTP를 거치지 않은 **따로 실행**(`await live_agent.ainvoke`)인데, 앞 HTTP 호출과 같은 궤적처럼 읽힘(마크다운 한 문장만) · `next(… for … getattr …)`·`isinstance`·`re.split` 내포식·`''.join`·`import json, re` 한 줄 · 한 글자 변수 `b`.
4. 준비 셀이 루트 커널에서 멈춤(`next(…)` 제너레이터 식·별표 풀기·`Path.cwd().resolve()`) · 첫 줄 주석·결과 읽기 0 · 키 셀이 과정 표준 모양이 아님(`bool(os.getenv(…))`, `assert has_key` 안내 글 없음).
5. **b6 「Ch29 평가셋으로 도구 선택과 최종 답을 반복 평가하고」(거짓 — Ch 29에 평가셋·반복 평가 없음)** · **b8 「Ch31에서는 실제 Agent 실행과 이벤트를 데이터베이스에 저장해 프로세스 재시작 뒤에도 복구합니다」(거짓 — Ch 31 `_src` 다섯은 SQLAlchemy 비동기 PostgreSQL·트랜잭션·Alembic·커넥션 풀·pgvector 체크포인터)** · b3 「모델 메시지 청크와 실행 메타데이터」(Ch 25 말은 「스트림 청크」·「칸 `metadata`」) · b4 비유 「무대 장치 점검」(챕터 계열 밖) · 「서비스 운영 인계」(실행 안 한 운영 설명 — 계기판·오류율·OpenAPI에서 교육용 경로 빼기) · 도식 읽기 틀 색 문장 · 「엔드포인트」·「경로」·「라우트」·「결정적」·「검증」·「반환」·「지연」·「측정」·본문 「Agent」.
6. `/v1/chat/live`가 시간 제한 오류를 504로 바꾸지 않는 점(500) 언급 없음 · `TestClient`의 스트림은 끝까지 모아 줌(옛 판 「실시간으로 보이는 지연을 측정하지 않습니다」 한 문장).

## 바꾼 것

- **모델 설정(챕터 결정 M0)**: 앱 파일 `live_agent.py` 18~23행에 `reasoning_effort="none",`(21행)을 더해 과정 표준 `temperature=0`·`reasoning_effort="none"`과 같게(`timeout=30`은 그대로 22행). 노트북은 2절에서 8~12행(도구)·15~28행(모델·`create_agent`)을 글로 읽어 보임(06절 `SOURCE_RESUME` 모양) + 결과 읽기에 실행일 문장. **게이트 G4는 노트북에 `init_chat_model` 셀이 없어 앱 파일 안 설정을 보지 못함**(G4 0은 「셀 없음」의 0 — 설정 확인은 노트북 셀 [8] 출력 줄 20·21행과 탐색 `x1_shape.py`의 모델 객체 속성 `reasoning_effort` `none`·`temperature` `0.0`·`request_timeout` `30.0`).
- **키**: 과정 표준 `nbkit.KEY`(값 출력 0, `assert has_key, "…"`). 키 없는 환경에서는 이 셀의 `assert`가 멈춰 모델 요청 0 — 결과 읽기 한 문장 + b7(셀을 건너뛰면 `build_live_agent()`가 `OpenAIError`(Missing credentials)로 멈추고 시험용 클라이언트도 그 오류를 올림 — 노트북 밖 키 없는 프로세스로 확인, 요청 0).
- **설치 셀**: 07·08의 여섯 + `langchain-openai==1.6.0`(실습 앱이 모델을 부름) + `python-dotenv==1.2.1`(키 셀, 잠금 판). `run_section.sh`의 `--with python-dotenv==1.2.3` 덧씌우기 환경에서는 `%pip`이 1.2.1을 **그 실행의 임시 환경**(`/tmp/uv-cache/builds-v0/.tmp…`)에만 넣고, 공용 캐시(`archive-v0/…` 의 1.2.3)는 그대로임을 노트북 밖에서 확인(설치 뒤 `version` 1.2.1·캐시 목록 그대로). 두 커널 출력 `python-dotenv: 1.2.1`.
- **요청 셋과 요청 수**: 3절 `POST /v1/chat/live` · 4절 `POST /v1/chat/live/stream` · 5절 같은 에이전트 객체의 직접 `astream(…, stream_mode="messages")` — 5절은 「3·4절의 요청과 따로 한 번 더 실행하는 것이라, 앞 실행과 같은 차례라고 할 수 없습니다」로 밝힘. 요청 수는 5절에서 **사용량이 든 스트림 청크 수 `2`**(Ch 25 02 — 응답 하나에 사용량 든 청크 하나)와 **Ch 29 04 셈 「노드 tools 사건 수 + 1」 `2`**로 셈. 3·4절은 응답 본문에 사용량이 없어 「도구를 한 번 불렀다면 두 번씩」(셈)으로만. 준비물 「도구를 한 번씩 부르면 여섯 번」.
- **모델 글 `assert` 0**: 옛 판 셋을 뺌. 흔들리는 값(답 글·SSE 사건 수·token 수·스트림 사건 수·글자 수)은 출력은 하되 결과 읽기 둘째 단락·b6 표 「글자 수(교재 출력, 실행마다 다를 수 있음)」·「확인할 점」·b7에만.
- **Ch 25 04 b8 조건**(「09절은 모드 messages의 스트림 청크를 같은 메서드로 받아 서버 응답으로 보냅니다」): 4절이 앱 127~154행(134~137행 `runtime.astream(…, stream_mode="messages")`·138행 노드 조건·140~147행 token 사건)을 출력하고, 그 요청 주소로 받은 SSE 사건(첫 `token`·끝 `done`·`live-1:0`)을 읽음 · 「스트림 청크」는 이 절에서 씀(용어 표 「다시 쓰는 말」 — 스트림 청크·칸 `metadata`·도구 메시지). **참**.
- **실험(5절)**: 가설 = Ch 25 02 그래프는 모델 노드 하나였고, 에이전트 그래프에는 `model`·`tools`가 있음 → 모드 messages가 노드 tools의 도구 메시지도 내놓는다면, 남길 노드에 `tools`를 더할 때 도구 결과 글이 답 앞에 붙을 것. 같은 사건 목록에 **남길 노드 이름 목록 하나만** 실행 1 `["model"]`(앱 138행 조건) ↔ 실행 2 `["model", "tools"]`. 결과: 노드 차례 `['model', 'tools', 'model']` · tools 사건 `ToolMessage lookup_library_hours 09:00~18:00` · 실행 1 `False` ↔ 실행 2 `True`·「실행 1 글 앞에 도구 결과 글을 붙인 것과 같은가」 `True`·글자 수 차이 `11` = `len('09:00~18:00')`. 결론 = 앱 138행이 도구 메시지를 걸러 받는 쪽이 답 글만 이어 붙이게 함(「모델이 도구를 한 번 부른 실행에서 본 것」 한정). 모델 요청 추가 없음. 빨강 0.
- **말**: 새 용어 **0**(meta 「새 용어 0」) — 스트림 청크·칸 `metadata`(Ch 25 02)·도구 메시지(Ch 19 05)를 「이 절에서 다시 쓰는 말」 표로. 제목의 「Agent」·「HTTP」·「통합」은 1절·b2 첫 자리에서 풂. 「엔드포인트」·「경로」 → 「요청 주소」 · 본문 「Agent」 → 「에이전트」 · 「메타데이터」 → 「칸 `metadata`」.
- **도구 파일 09 판**(아래) · 노트북 함수 둘 새로(`node_order(message_events)` — Ch 25 02 `mode_order`와 같은 모양으로 짝의 뒤 값에서 노드 이름 · `stream_text(message_events, node_names)` — 속성 `text`로 글 블록만 이음, 앱 140~141행과 같은 일: 노트북 밖에서 사건마다 `text` = 글 블록 이은 글 5/5 `True`, langchain-core 1.6.2 `messages/base.py` 262~291행).
- **b4 비유**: 「무대 장치 점검」 → 챕터 계열 「화물 열차와 번호판 차량」의 「실제 화물을 실은 열차」 — 갈림길이 짐 칸만 큰 선로로, 확인 결과 칸 하나는 옆 선로에(비유와 다른 점: 앱은 모아 두지 않고 건너뜀 · 짐 칸 수는 실행마다 다름).
- 본문 b1~b10 새로(b3 = Ch 21 01 `create_agent` + 02 제공 함수 + 05 비동기 제너레이터 함수 + 06 함수 넷 + Ch 25 02 messages·스트림 청크·칸 `metadata` + Ch 29 04 요청 수 셈 / b10 = LangChain Agents·LangGraph Streaming·OpenAI Reasoning models(셋 모두 2026-09-29 WebFetch) + 설치판 langgraph `pregel/_messages.py`·langchain-core `messages/base.py` 행 + 실습 폴더 행). 복습 넷 → **다섯**(해설 포함). meta 「강의 1h | 실습 2h」 그대로(챕터 시수 합 유지).
- 옛 `{{svg:09-흐름}}` 토큰 제거, 옛 그림 파일 셋(`09-흐름.svg·.excalidraw·.caption.md`)은 그대로.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-09/exp/`)

- `x1_shape.py`(가짜 키 글 한 줄을 프로세스에만 — 요청 0): `app.openapi()` `06e5d1b9…` · `build_live_agent()` 두 번 같은 객체·노드 넷 · 도구 직접 월 `09:00~18:00`·일 「해당 요일의 운영 시간 정보가 없습니다」 · 모델 객체 `reasoning_effort` `none`(설정 없으면 `None`)·`temperature` `0.0`·`request_timeout` `30.0`·`stream_usage` `True` · `ToolMessage.text`·`content_blocks` · 도구 요청 청크 `text` 빈 글 · **모델 없는 그래프에서 노드가 `ToolMessage`를 내놓으면 모드 messages가 `(ToolMessage, metadata)` 하나를 내놓음(노드 `tools`)** — 설치판 langgraph 1.2.11 `pregel/_messages.py` 67행(「stream messages from LLMs and nodes」)·97~104행(`_emit` 한 번만)·106~121행·223~246행(`on_chain_end` — 노드가 끝날 때 내놓은 메시지 가운데 보지 않은 것을 내보냄). LangGraph 문서의 스트리밍 안내는 이 경우를 적지 않음 → b4·b7에 「설치판의 출력을 기준으로」.
- `x1_shape.py nokey`: 키 없는 프로세스 → `build_live_agent()` `OpenAIError` · 시험용 클라이언트도 같은 오류(요청 0).
- `x2_timeout.py`(노트북 밖 대역 객체 — `types.SimpleNamespace(ainvoke=…, astream=…)`, 곧바로 `TimeoutError`, `get_live_agent` 재정의, 기록기 수준 CRITICAL): `/v1/chat/live` **500** · `/v1/chat/live/stream` 200 + `event: error`·`live_stream_failed`. 대역 객체는 노트북에 쓰지 않음(가짜 모델 아님, 탐색만) — b7·복습 3에 「노트북 밖에서 대역 객체로」.
- uv 덧씌우기 환경에서 `%pip install python-dotenv==1.2.1`(위 「설치 셀」).

## 흔들림 확인 (`09-probe.md`)

- **§0 저장 2026-09-29T11:18:44Z**(파일 수정 시각 같음) → §0 저장 시각 줄을 덧붙인 뒤 스크립트를 부름. 11:18:53Z~54Z 두 번은 스크립트의 `ROOT` 자리 잘못(`parents[5]`)으로 `os.chdir`에서 멈춤 — 키도 읽지 않아 **요청 0**. 고친 뒤 **첫 요청 회차 1 시작 11:19:07Z**(§0 23초 뒤) · 회차 5 끝 11:19:57Z.
- 5/5 같음: 구조 값 전부 · 모델 판단 값(도구 인자 (a)·(b)·(c) `월요일` 한 번씩·노드 차례·tools 사건 하나·모델 id 2·사용량 든 청크 2·실행 1이 도구 글로 시작하지 않음·길이 차 11) · 모델 글(답 32자·SSE 21·token 20·스트림 사건 35·입력 378/출력 42 토큰). → 입력 그대로, 결론은 구조 값 + 「도구를 한 번 부른 실행」 한정어 값.
- **측정용 덧붙임 하나가 세지 못함**: `httpx` `send` 감싸기로 모델 요청을 세려 했으나 단계마다 0 — 설치판 openai 3.13.0은 `httpx2`로 요청(`openai/_base_client.py` 37행). (a)·(b) 요청 수는 도구 함수 기록(한 번씩) + 셈으로 2씩, (c)는 모델 id·사용량 든 청크로 직접 2. 다시 보내지 않음.

## 실행 (새 커널)

| 실행 | 자리 | 키 | 모델 요청 | 결과 |
|---|---|---|---|---|
| 시험 tryA(`/tmp/ch30-09/tryA`, 모델을 부르는 셀과 그 뒤 셀 열 개를 뺀 결정적 셀 13, 기본 `--cwd`·`PYTHONPATH` = `notebooks/`, 11:36:00Z) | 루트 커널 | 있음(값 출력 0) | 0 | PASS 13셀 |
| 시험 tryB(같은 사본, `--cwd` 실습 폴더 `notebooks/`, `PYTHONPATH` 지움, 11:36:13Z) | 학생 커널 | 있음 | 0 | PASS 13셀, tryA와 13/13 같음 |
| **A**(`run_section.sh … 09`, `executed_at` 2026-09-29T11:36:42.005746Z) | 루트 커널 | 있음 | 6(셈) | PASS 23셀(그림 첨부 단계에서 멈춤 — 09-1 PNG 전) |
| **B**(A 사본 `/tmp/ch30-09/B`, `execute.py --cwd notebooks/`, `PYTHONPATH` 지움, 11:37:44Z) | 학생 커널 | 있음 | 6(셈) | PASS 23셀 |

- 시험 실행 전에 노트북 밖에서 5절 셀 여섯(`node_order`·노드 차례·요청 수·`stream_text`·실행 1·2·결과 표)의 코드만 손으로 만든 메시지 목록으로 한 번 돌려 봄(요청 0 — 노트북에는 쓰지 않음).
- **A ↔ B 셀별 출력 글자 23/23 같음 — 모델을 부르는 셀(11·13·14·15·16·18·19·21·22·23)까지**(이은 글 해시 `398570cd694a0685` 같음) · `code_sha256` `30c6e2033d0518565ead41e63a41ca65493df53e739d9850782751d101e9204f` 같음 · **`outputs_sha256`은 다름**(A `ead89bbaaee08d9d2b940250d8fcf1ba7a7074a4450d02f942b187be44239c65` · B `05da1acccc45ff96c041ad8edcad2d312cdf71c3535a0e72f9ae96c9b4fd5f35`) — 까닭: 설치 셀 [1] 표준 출력 스트림이 A 190 + 21글자·B 66 + 145글자로 나뉨(합친 글 같음 — 02~08 선례). 갈린 셀 **0**. 모델 글이 두 커널에서 같았지만 결론에는 쓰지 않음(규격 §2-7 9번 끝 — 흔들림 값).
- A 뒤 `mdpatch.py` 두 번(① 「오늘 볼 그림」 셀의 alt·그림 읽기를 설계 글로 ② G5 셋 — 마크다운만) · `--no-exec` 둘(렌더·첨부·빌드) — 노트북 코드·출력·`executed_at` 그대로(A 사본과 `cmpout` 23/23·`outputs_sha256` `ead89bba…` 같음) · 생성기 `cells()`와 저장 노트북 셀 글 49/49 같음(대조) — 노트북 파일 **`f9db00d5b1c5067d52e6691a2c6c477d843e8e0037796c87861be6d1adb6423e`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에서 새로 생기거나 바뀐 파일은 `live_agent.py`·노트북 09·`serve_tools.py`뿐(`find -newer` — pyc 0, `__pycache__` 안 파일은 09-11 것 그대로) · `.failure.json` 0 · 노트북 표준 오류 0·Traceback 0·`/var/folders` 0 · 서버 프로그램·포트·자식 프로세스 0 · 남은 프로세스 0(`ps` — uvicorn·ipykernel·jupyter·probe·node 없음).

## 서비스 요청 수 · 비용 어림

| 무엇 | 요청 |
|---|---|
| 모델 없는 탐색(`x1`·`x2`·dry 셋)·스크립트 첫 두 번(멈춤)·시험 tryA·tryB | 0 |
| 흔들림 확인 5회 × ((a) 2 + (b) 2 + (c) 2) | 약 30((c) 10은 직접 셈) |
| 새 커널 A · B | 6 · 6(5절 2씩은 직접 셈) |
| **합계** | **약 42** |

- 요금표 2026-09-17 `gpt-5.4-mini` 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰(청구 금액 아님): 에이전트 실행 하나(요청 2) = 입력 378·출력 42 토큰(흔들림 확인 (c)) → 약 0.00047달러 → 노트북 한 번(실행 셋) 약 0.0014달러(준비물 「0.002달러보다 적습니다」) → 이 절 전체(실행 21번) 약 **0.01달러**. 절 상한 1달러 안.

## 앱 파일 · `app.openapi()` 대조 · `tests/`

- `live_agent.py` `586a6a69b97eec7b39b482cc0130ce6b4837c5bce5fe635bc3abc9195a7849b6` → **`a7002c819e7b1ba9540316307954b26c4875e80b6d632e3e914bd1e7c5fd8266`**(21행 한 줄 더함, 23행부터 한 줄씩 밀림 — 옛 사본 `/tmp/ch30-09/live_agent.before.py`).
- `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **전후 모두 `06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 `True` · 정렬 직렬화 `d2fb94f6…` 4825자 · `pytest -q -p no:cacheprovider` **전후 6 passed, 1 warning**(테스트는 live 요청 주소를 부르지 않음) · `app.py` `3455d405…`·`agent.py` `a6c42e63…`·`schemas.py` `ed77b197…`·`__init__.py` `1c7d7aef…`·`tests/test_app.py` `f8611741…` 그대로.
- 01~08 노트북 코드·출력에 `live_agent.py`의 줄 없음(검색 — 02는 `app.py`의 `LiveAgentDep = …` 줄만 출력) → 다시 실행한 절 없음. 생성 SDK·`client/*.ts`·`openapi.json` 그대로.

## 도구 파일 — 09 판

- `serve_tools.py` 06 판 `e1a1464d…` → **09 판 `ff663039e6480e540085187772cbc4b9222eeb4c83c2788b13f0be716b6c6d88`**: 머리 설명 뒤 `import json` 한 줄(`author_04.strip_later_imports`가 빼는 자리) + 06 판 함수 여섯 그대로 + **06절 노트북 함수 넷 `read_events`·`event_names`·`token_values`·`ended_with_done`**(`author_06.DEF_READ`·`DEF_NAMES`·`DEF_VALUES`·`DEF_DONE` 셀 글 그대로, 주석 첫 줄 「# Ch 30 06절에서 배웠습니다 — 06절 노트북의 같은 이름 함수를 옮겼습니다」). `token_values`가 `json.loads`를 써서 가져오기 줄이 필요(06 노트북에서는 노트북의 `import json`을 씀).
- 사슬(`author_09.py`의 `MOVED09`·`TOOLS09`·`check_tools09`): `author_06.check_tools06()` 통과 · `strip_later_imports(09 판)`이 06 판으로 시작·04 판으로 시작 · 함수 차례 = `TOOL_ORDER06` + 넷 · 가져오기는 `json` 하나(`from` 0) · 옮긴 셀 글이 06 노트북 코드 셀과 문자열로 같음·AST 같음 · 쓰기 가드(06 판이거나 09 판일 때만 씀, 09 판으로 시작하는 더 긴 판은 건너뜀, 그 밖은 멈춤)·`--tools-copy`. **04 생성기 가드**(`strip_later_imports` 뒤 04 판으로 시작하고 04 판과 다름 → 건너뜀)·**06 생성기 가드**(06 판과 다르고 앞머리가 06 판 → 건너뜀) 확인.
- **07·08 생성기 `__main__` 고침**: 「디스크 파일 == 06 판」 `assert`가 09 판에서 멈추므로, 「가져오기 줄을 빼면 06 판으로 시작」으로(`author_07.py` `2aebd450…` → `3eddb10a…` · `author_08.py` `64752ad1…` → `d446971b…`, 주석 한 줄 더함). 두 생성기는 실행하지 않고 조건만 확인.
- **가져오는 노트북 영향**: 04·06·07 노트북 사본(`/tmp/ch30-09/chain`)을 09 판으로 다시 실행(키 뺀 환경) → PASS, 셀별 23/23·26/26·21/21 같음(`outputs_sha256` 차이는 설치 셀 스트림 나뉨뿐 — 06 사본은 기록된 B 값 `08fa05f6…`와 같음). 실습 폴더의 세 노트북은 그대로. 08은 가져오지 않음.
- 가져오는 셀(준비 셀, `os.chdir` 전) 결과 읽기에 고정 세 문장 + 커널 폴더 문장 둘(06 글) · 공개 목록 두 곳은 줄 그대로(파일 해시만 바뀜).

## 고친 틀린 사실

- **b6 「Ch29 평가셋으로 도구 선택과 최종 답을 반복 평가하고」(거짓)** → 「이 절은 모델이 쓴 답 글이 맞는지 판정하지 않았습니다. 궤적이나 답을 평가하려면 Ch 29 01절의 궤적 맞춰 보기나 03절의 평가 모델 판정을 씁니다」(03 b7과 같은 말, 링크).
- **b8 「Ch31에서는 실제 Agent 실행과 이벤트를 데이터베이스에 저장해 프로세스 재시작 뒤에도 복구합니다」(거짓)** → 「Ch 31은 PostgreSQL 데이터베이스의 표와 체크포인터를 다룹니다. 이 절의 에이전트 실행과 보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」(06 b7과 같은 뜻, Ch 31 01 링크) — 노트북 정리 끝도 같은 두 문장. 실습 절이 생기면 그 작업자가 「다음 학습」을 실습 절로 고침(PLAYBOOK §3).
- b3 「모델 메시지 청크와 실행 메타데이터」 → 「스트림 청크와 칸 `metadata`의 짝」(Ch 25 02 말).
- 「엔드포인트」·「경로」·「라우트」·본문 「Agent」 → 「요청 주소」·「처리 함수」·「에이전트」 · 「결정적 그래프」 → 「모델을 쓰지 않는 그래프」.
- 옛 b4 「노트북은 월요일 질문의 답에 도구가 반환한 18:00이 포함되는지 검사합니다」 → 모델 글 `assert` 빼고, 도구 결과는 도구를 직접 부른 출력과 노드 tools 사건으로.
- 옛 「서비스 운영 인계」(계기판·오류율·첫 token 지연 측정·OpenAPI에서 교육용 경로 빼기) → 실행하지 않은 운영 설명이라 뺌.

## 그림

- Mermaid 넷(`09-figures.md` 설계표를 렌더 전에 씀 → `.mmd`·캡션 → 렌더 → PNG 넷을 직접 열어 확인): 첫 렌더에서 09-1 두 상자가 `~~~` 때문에 어긋나고 09-2 라벨 하나가 저절로 줄바꿈 → 고쳐 다시 렌더(보기 사본 `.cache/ch30-09-view/f1-v2.png`·`f2-v2.png`로 확인 — 같은 이름 PNG는 읽기 도구가 앞 판을 보여 줘서 이름을 바꿔 봄). 최종 viewBox 폭 **519 · 531 · 249 · 614**, 끊긴 라벨 0. 색: 시험용 클라이언트·5절 직접 실행·실행 2 노드 목록 파랑 · 실습 앱 줄·제공 함수·도구 노드 초록 · **보라 = 에이전트 그래프·노드 model(실제로 부른 모델)** · 출력 노랑 · 라이브러리 사건 짝·건너뛰는 갈래·두 실행 공통 목록 회색 · **빨강 0**. 라벨의 노드 차례·요청 수 2·tools 글은 §0 규칙대로 「도구를 한 번 부른 실행」 한정어가 든 09-3·09-4에만.
- 삽화 09-5: **1차 job `9d9e5210-7fbe-47ed-9820-8ec4d0eb7ed4` 탈락**(갈색 뚜껑 없는 짐칸 — 03절 소품 되풀이, 거래 11:41:51.872594Z −2) → **2차 job `d61314ff-bb6a-4ebc-aa24-08b1aa1ee773` 채택**(재생성 1회 — 한도 안, 거래 11:43:08.928671Z −2) · **이 절 몫 4크레딧**(잔액 2273 → 2269, 앞 거래 10:52:17Z는 08절) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 원본 `95df06fa…`(2752 × 1536) → 저장 PNG **`ef760939c3e8c799740aa8a2bf154eb28da59d19684eac610c3777a308aefc45`**(1100 × 614) · 결과를 다시 받아 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0 · 저장본과 같은 보기 사본을 열어 **연한 노란색 사과 칸 넷**·**남색 닫힌 칸 하나**(옆 선로)·기관차·사람·글자·숫자·화살표 없음을 세고 그림 읽기를 씀. 거의 흰 가로줄 **119 / 614**(1차 0 — 2차는 위쪽 왼편이 비어 있음, 06 115·07 109 선례 안). 01~08 소품 되풀이 없음(1차에서 걸린 갈색 칸을 뺌).

## 검사

- `run_section.sh … 09 --no-exec`(마지막): 렌더(도장 같아 건너뜀) · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 208 code cells (max 12 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `09-실제-Agent-HTTP-통합.html`(`2d3a2669…`): `{{` **0** · `[[` 0 · 인라인 SVG 4 · 삽화 JPEG 1.
- `pack.py … 09` → `qa/upgrade/review-pack/09-실제-Agent-HTTP-통합.md`(`1f580c16…`).
- 보호 파일 255개: `manifest-changes.md` 「09절 뒤」에 덧붙임(같음 216·바뀜 39 = 01~08 기록 값 32 + 09 작업 7·없어짐 0).

## 완료 챕터·뒤 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

`grep -rn 'Ch *30' textbook/part1 part2 part5 part6 part7 --include=*.html | grep -v ch30-fastapi`(qa 사본 뺌):

| 문장 | 판정 |
|---|---|
| **Ch 25 04 b8** 「Ch 30 04절은 모드 custom의 사건을 비동기 메서드 astream으로 받아 이어 붙입니다. 09절은 모드 messages의 스트림 청크를 같은 메서드로 받아 서버 응답으로 보냅니다」 | **참** — 4절 앱 134~137행 `astream(…, stream_mode="messages")`·140~147행 스트림 청크 글 → token 사건 · 요청 주소로 받은 SSE 사건 출력 · 슬러그 그대로 |
| **Ch 29 05 b8** 「Part 7 Ch 30 01절에서는 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다」 | 09와 무관 — 참(01 끝남) |
| Ch 1 01 과정 지도 · Ch 2 11 b8(2절)·12 b8(1·3절)·Ch 2 `index.html` · Part 7 소개 | 09와 무관 — 참 |
| Ch 31 01 b2·b3 「Ch30에서 FastAPI 요청 함수/경로 함수를 비동기로」 · Ch 32 01·02 「Ch30의 서비스」 · Ch 34 04 b3 | 글만(대기 챕터, 고치지 않음) — 09와 무관. Ch 31이 Ch 30의 실행·사건 저장을 잇는 문장은 없음(09 b8과 맞음) |
| 같은 챕터 03 b7 「모델을 부르는 에이전트는 09절에서 씁니다」 · 08 b8·노트북 정리 끝 「09절에서는 실제로 모델을 부르는 에이전트를 요청 주소 /v1/chat/live로 부릅니다」 · 04 6절(앱 134·136행 출력만) | **참** — 3절 `POST /v1/chat/live` |

## 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀 — `cd2ea427…`) · 사용자 디스크 `.cache/ch30-09-view/`(보기 사본 넷 — 새로 만든 폴더). 공용 도구·규격·과정 문서·zip·검사 스크립트·`app.py`·TS 파일·생성 SDK·`openapi.json`·공개 목록·Ch 31 이후 파일은 고치지 않음. 챕터 안 앞 절 파일은 `author_07.py`·`author_08.py`의 `__main__` 확인 줄만(도구 파일 사슬).

## 강사 확인 대상

1. 앱 파일 `live_agent.py`에 `reasoning_effort="none"`을 더한 것(챕터 결정 M0 — 응답 문서·테스트 영향 0) · 게이트 G4가 앱 파일 안 설정을 보지 못하는 점.
2. 실험 변수를 「남길 노드 이름 목록」으로 고르고, 앱을 고치지 않고 노트북에서 같은 사건 목록에 두 조건을 적용한 것(앱 138행이 없을 때의 SSE 응답은 실행하지 않음 — b6에 밝힘).
3. 모드 messages가 노드 tools의 도구 메시지도 내놓는다는 사실이 LangGraph 문서에 없고 설치판(1.2.11) 소스·출력 기준인 점.
4. 3·4절 HTTP 실행의 요청 수를 셈으로만 적은 것(응답에 사용량 없음) · 5절이 따로 실행이라는 점.
5. 두 커널과 흔들림 확인에서 모델 글까지 모두 같았지만 결론에 쓰지 않은 것(규격 §2-7 9번 끝) · b6 표에 글자 수 32·43을 「교재 출력」으로 둔 것.
6. `/v1/chat/live`의 시간 제한 → 500을 노트북 밖 대역 객체로만 확인한 것(앱을 고치지 않음 — 504로 바꿀지는 실습 폴더 판단).
7. 삽화 2차의 위쪽 흰 여백(119/614) — 재생성 한도를 1차 소품 되풀이 때문에 씀.

## 남은 것 (마감 몫)

- `part7-practice.zip`에 09 노트북 새 판·`live_agent.py`·`serve_tools.py` 09 판 반영(마감 때 한 번) · 09는 Part 7 묶음 실행 검사 대상 아님(01만, 키 필요).
- 옛 그림 `09-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- `run_section.sh`의 `--with python-dotenv==1.2.3`과 잠금 1.2.1 차이(기록만 — 공용 도구).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-09-09.json` · 기기 `/tmp/ch30-09/`(약 14MB — 탐색 스크립트·dry 사본·시험 tryA·tryB·A·B 사본·도구 사슬 사본 `chain/`·삽화 원본 셋 `illu/`·도구 복사본·`live_agent.before.py`·`nb09-before-author.ipynb`·`A-before-mdpatch.ipynb`) · 사용자 디스크 `.cache/ch30-09-view/`(보기 사본 넷, 약 1.9MB).
