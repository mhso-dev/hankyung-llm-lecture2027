# 01절 진단 — 비동기 라우팅과 스키마 (paired)

- 작업일: 2026-09-29 · 작업자: 01절 작업자(Part 7 첫 절) · 생성기 `qa/upgrade/author_01.py`(`772e9440…` — 마지막 치환 뒤)
- 읽은 것: 준비 노트 `chapter-lead-notes.md` 전부 · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 규격 전부 · 과정 요약(§1~§9) · 계약(Part 7·Ch 21~29 줄) · Ch 29 `chapter-summary.md` · Ch 28 `author_01.py`·`author_02.py`·Ch 29 `author_04.py`(파일 위치 셀) · Ch 29 `handoff.md`(챕터 공통·§01 → §02 본) · Ch 2 12 `_src`(Ch 30 1절 문장·차단 호출) · Ch 4 04·Ch 6 03·Ch 15 08·Ch 19 02·Ch 21 01·Ch 28 03·Ch 29 05 `_src`(이어 쓴 말 확인). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-01.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 1 · 1 · 5 · 0 · 6 · 11 · 3 = **27** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(`count_code.py`) | 5 · 27 | **22 · 110** |
| 검사 문장 | 86 | **388** |

- 첫 실행 전 `upgrade_gates.py … --label wip-01 --section 01`: G1·G2 **0**(G6 5 — 긴 문장 둘·영문 시작 셋, G7 3 — 그림 전) → 고친 뒤 G6 0.
- AST 따로(`/tmp/ch30-01/tools/extra_check.py` — Ch 29 도구 복사): 걸린 것은 **챕터 예외뿐** — 데코레이터 줄 셋(`@demo_app.get`·`@before_app.post`·`@after_app.post`) · `async def` 셋 · 처리 함수 매개변수 힌트 둘(`body: dict`·`body: ChatRequest`) · `method:get` 셋(요청 방식 GET을 보내는 메서드 `demo_client.get`·앱 객체 `demo_app.get` — 딕셔너리 `.get` 아님, 거짓 양성). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`try`·`while`·별표 풀기·대입 풀기·기본값 매개변수·내놓는 값 힌트·클래스·셀 맨 위 await·`asyncio` **0**. 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **8줄** · 함수 본문 최대 **5줄**(처리 함수) · 셀당 정의 하나.
- 금지어(`/tmp/ch30-01/tools/ban30.py` — Ch 29 `ban29.py` + Ch 30 목록): 본문·노트북 마크다운·주석·`.mmd`·캡션에서 걸린 것은 **허용한 것뿐** — 「라우팅」·「스키마」(제목 둘 + 본문 b2·노트북 1절의 「제목의 ○○은」 풀이 한 번씩, 강사 확인) · 「이벤트 루프」(Ch 2 12 말 — 「이벤트」 단독 0) · 「헤더」(「응답 머리(헤더)」 첫 풀이 한 번 + 주석 한 번) · 「로그」는 「프로그램」 거짓 양성. 「되돌려 받는」(「돌려」)은 고침.

## 수정 전 주요 문제 (옛 판 — `before/_src/01-…html`·`before/notebooks/01-…ipynb`)

1. **paired Before가 결함이 아님** — 빈 글 422는 검사가 제대로 막은 장면이고 After는 입력 글만 바꿈(코드 고침 없음, 규격 §5-3·§6 어긋남).
2. **준비 셀이 루트 커널에서 멈춤**(`run_section.sh` 커널은 프로젝트 맨 위) — `next((p for p in (start, *start.parents) …), None)`(제너레이터 식·별표 풀기·한 글자 `p`) + `os.chdir`.
3. 코드 셀 첫 줄 주석 0 · 결과 읽기 셀 0 · 제목 셀·그림 첨부 없음 · 한 셀에 클래스·앱·처리 함수·클라이언트 모두.
4. 틀린 말·사실: b3 「Ch21에서 Agent 실행 객체」(Ch 21 말 아님 → 「에이전트 그래프」) · 「Ch25에서는 결과가 조각으로」(「조각」 = Ch 5 토큰) · b4 비유 「식당의 주문표」(Ch 19 비유와 겹침) · 도식 읽기 틀 색 문장(과정 색 규칙과 다름) · b4 「422는 … 모델 비용을 발생시키지 않습니다」(모델 없이 보인 적 없음).
5. 금지어: 반환·스키마·필드·검증·경로(URL)·라우트·사전·쿼리·병렬·직렬화·결정적·측정·로그·조각·실행 객체·주문표.
6. 참고 자료 둘(확인 2026-09-11)·복습 한 줄 해설.

## 바꾼 것

- **paired 설계(챕터 리드 결정 5)**: Before = 요청 본문을 딕셔너리(`body: dict`)로 받고 응답 형식이 없는 처리 함수 → **빈 질문이 몸통까지 들어가 200**, 답 `'질문을 확인했습니다: '`, 몸통에 들어온 값 `['']`, 응답 본문에 앱 안쪽 키 `messages`(빨강 둘) ↔ After = 같은 몸통 + 매개변수 힌트 `body: ChatRequest`(실습 폴더 `schemas.py`) + `response_model=ChatResponse` → **같은 요청이 몸통 전에 422**(`string_too_short`·`['body', 'question']`·`{'min_length': 1}`), 몸통에 들어온 값 `[]`, 맞는 질문은 칸 둘만(`답이 Before와 같은가: True`). 값 바꿔 보기 = 질문 공백 한 칸 → 두 앱 모두 200·몸통까지(입력 형식의 한계 — Ch 28 02 「주차」와 같은 구조).
- **몸통의 「에이전트 자리」**: 모델을 부르지 않는 평범한 동기 함수 `make_result(question)`(키 `messages`·`answer` = `agent_service/agent.py` 상태 형식 칸 이름) — 가짜 채팅 모델 아님, 본문·노트북이 「그 자리에 평범한 함수를 둔다」고 밝힘. 03이 이 자리를 실습 폴더 그래프로 바꿈(handoff).
- **예시 부분**: 파일 위치 셀(과정 표준) → `runpy.run_path`로 `schemas.py`만 읽기 → `model_json_schema()`로 입력 형식 규칙·응답 형식 칸 → 앱 객체 `FastAPI(title=…)` → GET `/health` 처리 함수(`async def`, 데코레이터 줄 세 문장 + Ch 2 09 링크) → 시험용 클라이언트 200 → 없는 요청 주소 404·다른 요청 방식 405(`allow: GET`) → `make_result` 정의·호출(동기 호출 설명 — Ch 2 12 b8 조건).
- **파일 위치 셀(챕터 리드 결정 1)**: 후보 `".."`(notebooks·묶음) · `"."`(실습 폴더 맨 위) · `"labs/part7/ch30-fastapi-serving"`(프로젝트 맨 위) + `os.path.exists(candidate + "/agent_service/schemas.py")` + `assert`. **고른 후보는 출력하지 않음**(커널마다 달라서 — 두 커널 셀별 출력이 같게).
- 노트북: 제목 셀(할 일 셋·준비물·기준 버전·강의와 실습 범위) · 오늘 볼 그림(01-1 첨부) · 설명 → 코드 → 결과 읽기 · 정리 세 줄 + 02 예고. 설치 셀 `fastapi==0.135.0`·`httpx==0.28.1`·`pydantic==2.12.5`·`starlette==1.6.0`(잠금 판, 이 절이 쓰는 넷). 키 셀 없음.
- 본문 b1~b10 새로(b3 = Ch 4 04·Ch 15 08·Ch 28 03 / Ch 6 03·Ch 2 10·Ch 19 02·Ch 28 02 / Ch 2 12·Ch 2 09·Ch 21 01, b10 = FastAPI 문서 다섯(2026-09-29 확인) + 설치판 소스 행). 복습 넷 → **다섯**(해설 포함). meta 「강의 1.25h | 실습 2.5h」 그대로(챕터 시수 합 유지), 「새 용어 6」(앱 객체·요청 방식·처리 함수·시험용 클라이언트·상태 코드 422·응답 형식 — 입력 형식은 이어 씀).
- 그림: Mermaid **5장**(01-1 b4·노트북 · 01-2 b4 · 01-3 b5 · 01-4·01-5 b6 — viewBox 폭 451·478·310·655·301, 모두 868 이하) + 삽화 **1장**(01-6, 재생성 0). 옛 `{{svg:01-흐름}}` 토큰 제거, 옛 그림 파일 셋(`01-흐름.svg·.excalidraw·.caption.md`)은 그대로.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-01/exp/`)

- `x1_app.py`: `body: dict` 처리 함수는 빈 글·공백·501글자·모양 틀린 `thread_id` 모두 200·몸통까지 · `body: ChatRequest`는 빈 글 `string_too_short`, 501글자 + `bad id!` → `string_too_long`·`string_pattern_mismatch` 둘, 공백 한 칸은 200 · `GET /v1/chat` 404 `{'detail': 'Not Found'}` · `POST /health` 405 + `allow: GET` · `response_model`이 키 `messages`를 거름 · Before OpenAPI 본문 `{'additionalProperties': True, 'type': 'object', 'title': 'Body'}`(노트북에는 싣지 않음).
- `x2_block.py`(ASGI 전송 + `httpx.AsyncClient`, 다섯 번씩): `async def` + `time.sleep(0.3)` → `['느린 시작', '느린 끝', '빠른 요청']` 5/5 · `await asyncio.sleep(0.3)` → `['느린 시작', '빠른 요청', '느린 끝']` 5/5 · `def` + `time.sleep(0.3)` → `['느린 시작', '빠른 요청', '느린 끝']` 5/5(빠른 요청은 0.05초 뒤에 보냄). → b7 첫 항목·복습 5의 근거(「노트북 밖에서 다섯 번」).
- 설치판 소스(fastapi 0.135.0): `routing.py` 315~325(비동기 → `await`, 동기 → `run_in_threadpool`) · 452~462(본문을 입력 형식으로 읽고 `if not errors:`) · 630~634(처리 함수 부름) · 651(응답 형식 `serialize_response`) · 675~679(`RequestValidationError`) · `exception_handlers.py` 20~26(422 + `detail`) · starlette 1.6.0 `testclient.py` 377(`class TestClient(httpx.Client)`).
- 공식 문서(2026-09-29 WebFetch): Request Body(양식 클래스 매개변수 → 본문, 단일 자료형 → 쿼리) · Response Model(검사·거르기, 보안에 중요) · Handling Errors(`RequestValidationError`, 기본 422·`detail` — **예시의 오류 종류가 `type_error.integer` 같은 옛 이름 ↔ 설치판 `string_too_short`**, 출력 기준으로 씀) · Concurrency and async/await(`def` 처리 함수는 바깥 스레드에서 부르고 기다림, await 없는 라이브러리는 `def`) · Testing(HTTPX 바탕).
- IPython 커널 `sys.path`에 `''`가 있음(0번 자리는 아님) → `os.chdir(실습 폴더)` 뒤 `from agent_service.app import app` 가져오기가 됨 · **`agent_service/__init__.py`의 `from .app import app` 때문에 속성 `agent_service.app`은 모듈이 아니라 FastAPI 객체**(`import agent_service.app` 뒤 `agent_service.app.get_agent` → `AttributeError`) — 02 인계.

## 실행 (새 커널)

| 실행 | 자리 | 키 | 결과 |
|---|---|---|---|
| 시험 tryA(`/tmp/ch30-01/tryA` 사본, `execute.py --cwd` 프로젝트 맨 위) | 루트 커널 | `OPENAI_API_KEY` 지움 | PASS 22셀 |
| 시험 tryB(사본, `--cwd` 실습 폴더 `notebooks/`) | 학생 커널 | 지움 | PASS 22셀, 셀별 22/22 같음 |
| 묶음 모양(`/tmp/ch30-01/bundle/part7-practice/labs/part7/ch30-fastapi-serving/` — `schemas.py`와 노트북만, `--cwd notebooks/`, `PYTHONPATH` 없음, `.env` 닿지 않음) | 묶음 커널 | 지움 | PASS 22셀, 셀별 22/22 같음, `outputs_sha256`도 같음, pyc 0 |
| **A**(`run_section.sh … 01`, 2026-09-29T06:32:54Z) | 루트 커널 | 지움 | PASS 22셀(그림 첨부 단계에서 멈춤 — 01-1 PNG 전) |
| **B**(A 사본, `uv run … execute.py --cwd notebooks/`, 06:33:07Z) | 학생 커널 | 지움 | PASS 22셀 |

- **A ↔ B 셀별 출력 22/22 같음**, `code_sha256` `861cacdb64be1cf3bf7a5e8e712eab20cc46488075e16225f7f182699fb3337f` · `outputs_sha256` `87ea510f027a766becb9c3e031690b996b3f266d918be96ef7d73b9d136e7542` 둘 다 같음(B는 그림 전). 그 뒤 `--no-exec` 넷(렌더·첨부·빌드)에서 노트북 코드·출력·`executed_at` 그대로(첨부만 더함) — 노트북 파일 `efbadc6b…` → **`c94af127a4b781d3a1344d34407e20381b2f1d9bc4486b1fa55e8949cd70312c`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에 새로 생긴 파일 0(`find -newer`, 노트북 01 말고) · `.failure.json` 0 · 표준 오류 출력 0(starlette `TestClient`의 anyio 별칭 경고는 노트북 커널에서 보이지 않음 — 모듈 밖 경고라 기본 필터가 숨김) · 설치 셀 출력에 pip 안내 한 줄(`Note: you may need to restart the kernel …`).
- **모델 요청 0** · 서버 프로그램·포트·자식 프로세스 0 · 남은 프로세스 0(노트북 밖 확인도 같은 프로세스 ASGI 전송만 — uvicorn을 띄우지 않음).

## 묶음 실행 검사 계약 (챕터 리드 결정 2)

- 01은 키·모델 객체·`dotenv`·포트·자식 프로세스·도구 파일 없이 돎(위 묶음 모양 실행 PASS). 읽는 파일 `agent_service/schemas.py`는 Part 7 공개 목록 두 곳과 `part7-practice.zip`에 있음(`part7-practice/labs/part7/ch30-fastapi-serving/agent_service/schemas.py`).
- **01 노트북이 바뀌어 `part7-practice.zip`·`textbook/part7/qa/bundle-execution.json`(Ch 30 01 `code_sha256` 옛 값 `7bd57d1f…` → 새 `861cacdb…`)은 낡음** — zip 다시 만들기와 Part 7 `check_bundle_execution.py`(실행기 = Ch 31 맥 `.venv`라 이 기기에서 그대로 못 돎)는 마감 몫.

## 앱 파일 고침 · `app.openapi()` 대조 · `tests/`

- **01은 앱 파일을 고치지 않음**(읽는 `schemas.py`는 과정 문법 안 — 양식 클래스 칸 셋 `Field(…)`, f-string·힌트 문제 없음). `app.py`·`agent.py`·`live_agent.py`의 문법 고침은 그 파일을 처음 가져오는 절(02~) 몫.
- 기준값(02가 대조할 것): `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = 실습 폴더 `openapi.json`(바이트 같음) · 정렬 직렬화(`sort_keys=True`) `d2fb94f6…`(4825자).
- `pytest -q -p no:cacheprovider`(가상환경, 쓰기 0): **6 passed, 1 warning**(anyio 별칭 경고) — 준비 노트와 같음.

## 고친 틀린 사실

- 「Ch21에서 Agent 실행 객체」 → 「Ch 21 01절에서는 함수 `create_agent`로 에이전트 그래프를 만들었습니다」(Ch 21 인계).
- 「Ch25에서는 결과가 조각으로」 → 문장 뺌(01은 스트리밍을 다루지 않음).
- 「잘못된 입력은 모델 비용을 발생시키지 않습니다」 → 「몸통에서 에이전트를 불렀다면 빈 질문으로 모델 요청이 나갔을 자리」(모델 없이 보인 범위로 한정).
- 도식 읽기 틀 색 문장 → 그림마다 색·방향을 그림에 맞춰 새로.
- 「비동기 함수 안에서 동기 HTTP 클라이언트나 긴 파일 처리를 호출하면 이벤트 루프가 멈출 수 있습니다」(근거 없음) → 노트북 밖 5/5 확인 + FastAPI 문서 + Ch 2 12 Before로 근거를 밝힘.

## 옛 생성기 막기 (챕터 리드 결정 10)

맨 위에 설명 주석 세 줄 + `raise SystemExit(…)` 한 줄(`from __future__` 줄이 있으면 그 뒤, 독스트링 한 줄이면 독스트링 뒤)만 더함. 사본 `/tmp/ch30-01/pre/`와 `diff` — 더한 줄 넷, 지운 줄 0. `/tmp/ch30-01/blocktest/` 사본 실행으로 여섯 모두 안내 글 + 종료 코드 1 확인.

| 파일 | 전 | 후 |
|---|---|---|
| `textbook/part7/ch30-fastapi-serving/_src/_generate.py` | `79c8c6f6…` | `4e6dab19fc250cf8ef36c052e2cf9a532bd182328c4c1c29662ea40c5cb98703` |
| `labs/part7/ch30-fastapi-serving/notebooks/_generate.py` | `a9640d09…` | `6c589718167c5de6f9a0ba8bd9ea2dfb81cd66047f6f8dd9d30649c980ee9e2f` |
| `textbook/part7/ch30-fastapi-serving/figures/_gen_figures.py` | `dbd4ec67…` | `acbc975a44a5e22685f8a27b08b51bd05071a8bee727fbbc9236a0b1b8ae2499` |
| `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part7_apply_depth.py` | `3c217354…` | `f60d72879e16c1dd34d6b5d11966197485f0d8d9e5e9e648a6ebae7918804256` |
| `.moai/…/part7_review_fixes.py` | `eadfd1c2…` | `8cb946ea63a04d35ee1f1a981e7bdf5ff85507edc76b1aa04ea7c36759ebc922` |
| `.moai/…/part7_final_repairs.py` | `05c32efe…` | `b171658fd1dee5ba857e68f743360bc1fd0f44ef543c6eb070bbc713a0dea8aa` |

- `.moai` 셋은 Ch 30~34 `_src`·노트북을 쓰는 스크립트라 **Ch 31~34에도 해당**(막았을 뿐 내용 그대로 — 옮기거나 지울지는 사용자·강사). 옮기기(`mv -n` → `qa/upgrade/before/generators/blocked/`)는 마감 몫. **Part 7 `qa/check_figures.py` 20행이 `figures/_gen_figures.py`가 있는지 `assert`** — 옮기면 그 검사가 멈춤(마감 때 함께 판단).

## 그림

- Mermaid 다섯: 설계표 `01-figures.md`(렌더 전 작성) → `.mmd`·캡션 → 첫 렌더에서 라벨 넷이 가운데에서 끊겨(01-2 「검사」·01-3 칸 이름·01-4 `response_model=ChatRes / ponse`·01-5 「검사」) `<br>`로 미리 나눠 다시 렌더 → PNG 다섯을 직접 열어 확인(색·방향·점선 갈래·빨강은 01-4 Before 결과 둘뿐·보라 0). G7 라벨 숫자(200·404·405·422·500) 모두 출력에 있음.
- 삽화 01-6: `01-6-…prompt.md` 상태 줄 — job **`ee525ed0-f27f-41d4-8cb1-996627058ebc`** 채택(1차, 재생성 0) · 거래 2026-09-29T06:35:38.172555Z 「Nano Banana Pro −2」 한 줄(잔액 2295 → 2293, 앞 거래 03:44:07Z는 Ch 29 05) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 저장 PNG `d1fbb0ff…`(1100 × 614)와 채택 결과를 다시 받아 줄인 그림 픽셀 대조 bbox `None`·최대 차이 0 · 저장본 사본을 열어 창고 하나·문 둘·선로 둘·빈 화차 둘·파란 틀 하나·차단봉 하나를 세고 그림 읽기를 씀. 그림과 프롬프트의 차이(짐칸 모양 화차·원근으로 오른쪽 화차가 큼·오른쪽 화차가 선로에서 조금 비켜남)는 prompt 상태 줄에, 크기는 그림 읽기에 「짝짓지 않음」.

## 검사

- `run_section.sh … 01 --no-exec`: 렌더 다섯 · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 62 code cells (max 14 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `01-비동기-라우팅과-스키마.html`(`498a9891…`): `{{` **0** · `[[` 0 · 인라인 SVG 5 · 삽화 JPEG 1 · b5 노트북 셀 12 · b6 노트북 셀 10.
- `pack.py … 01` → `qa/upgrade/review-pack/01-비동기-라우팅과-스키마.md`.
- 보호 파일 255개: `manifest-changes.md` — 같음 243 · 바뀜 12(모두 이 절 작업 — 01 HTML·`_src`·노트북·옛 생성기 여섯·`verify.py`가 다시 쓴 `notebook-contracts-part7-ch30-fastapi-serving.json`·덧붙인 `집필점검표.md`·`qa/verification.md`) · 없어짐 0.

## 완료 챕터 문장 참·거짓 (이 절 쪽 조건)

| 문장 | 판정 |
|---|---|
| Ch 2 12 b8 「Ch 30 1절은 비동기 함수 안의 동기 호출이 이벤트 루프를 멈출 수 있다고 설명합니다」 | **참** — 01 b4 「비동기 처리 함수와 그 안의 동기 호출」·노트북 3절 `make_result` 결과 읽기·b7 첫 항목(노트북 밖 5/5)·복습 5 |
| Ch 2 12 b8 「Ch 30 3절은 await로 Agent 실행을 기다립니다」 | 03 몫(01은 `ainvoke` 0 — 인계) |
| Ch 2 11 b8 「Ch 30 2절 … 대체 설정이 다음 질문까지 이어지는 실패」 | 02 몫(인계) |
| Ch 25 04 b8(04 custom·09 messages, 슬러그 04·09) | 04·09 몫, 슬러그 그대로 |
| Ch 29 05 b8 「Part 7 Ch 30 01절에서는 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다」 + 01 슬러그 링크 | **참** — 슬러그 `01-비동기-라우팅과-스키마` 그대로, b2 「Ch 29 05절 끝에서 예고한 대로, 이 절은 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다」·b1·b4 |

## 챕터 밖 수정

- `.moai/…/part7_apply_depth.py`·`part7_review_fixes.py`·`part7_final_repairs.py`(막기만, 위 표) · `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀, `73214e89…` → `7f44e87a…`) · 사용자 디스크 `.cache/ch30-01-view/illu-1-1100.png`(삽화 보기 사본 — 새로 만든 폴더). 공용 도구·규격·과정 문서·Part 7 목록·zip·검사 스크립트·Ch 31 이후 파일은 고치지 않음.

## 강사 확인 대상

1. 제목 말 「라우팅」·「스키마」(제목에만 두고 b2·노트북 1절에서 한 번씩 풂) · 챕터 제목 「서빙」.
2. 01 Before를 「입력 형식 없는 처리 함수(`body: dict`)」로 바꾼 것 · 몸통에 모델 없는 함수 `make_result`를 둔 것(가짜 모델이 아님을 본문에 밝힘).
3. 새 용어 「요청 방식」·「처리 함수」·「시험용 클라이언트」·「앱 객체」·「응답 형식」(용어 표는 handoff).
4. FastAPI 처리 함수 매개변수 힌트·데코레이터 줄·`async def` 챕터 예외.
5. 비동기 차단 호출을 노트북에서 실행하지 않고 노트북 밖 5/5와 문서로만 밝힌 것.
6. 삽화 01-6(화차 모양·원근 — 그림 읽기에 밝힘), 비유 계열 「화물 열차와 번호판 차량」을 연 것.
7. 코드 양 27 → 110줄(셀 5 → 22 — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와의 균형).

## 남은 것 (마감 몫)

- `part7-practice.zip` 다시 만들기 → Part 7 `check_bundle_execution.py`(사본·환경 변수로) → `bundle-execution.json` 새 해시.
- 옛 생성기 셋 옮기기 · `.moai` 셋 처분(사용자·강사) · 옛 그림 `01-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-01-01.json` · 기기 `/tmp/ch30-01/`(사본·실험·삽화 원본, 약 7MB) · 사용자 디스크 `.cache/ch30-01-view/`(0.6MB).
