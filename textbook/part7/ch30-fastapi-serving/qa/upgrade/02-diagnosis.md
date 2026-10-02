# 02절 진단 — 의존성으로 Agent 주입 (paired)

- 작업일: 2026-09-29 · 작업자: 02절 작업자 · 생성기 `qa/upgrade/author_02.py`(`ae0b50ed…` — 마지막 치환 뒤)
- 읽은 것: `handoff.md`(챕터 공통·§01 → §02 전부) · 준비 노트 `chapter-lead-notes.md`(§0·§1·§2 02·§3·§4·§5·§7·§8·§12·§15) · `01-diagnosis.md`·`01-figures.md`·`author_01.py`(전부) · Ch 28 `author_02.py`(파일 위치 셀 대조 본) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 규격 전부 · 과정 요약 §1·§2-13~§2-20·§3·§5·§6·§7·§8·§9 · Ch 2 11·12 `_src`(Ch 30 문장·테스트 격리) · Ch 13 02·Ch 16 05·Ch 23 03·Ch 28 01 `_src`(이어 쓴 말). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다. Ch 27·29 도구 파일 사슬은 도구 파일을 만들지 않아 보지 않았습니다.

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-02.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 3 · 1 · 5 · 0 · 6 · 13 · 3 = **31** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(`count_code.py`) | 5 · 29 | **24 · 105** |
| 검사 문장 | 84 | **403** |

- 첫 실행 전 `upgrade_gates.py … --label wip-02 --section 02`: G1·G2 **0**(G6 5 — 긴 문장 하나·영문 시작 셋·다섯 문장 넘는 단락 하나, G7 3 — 그림 전) → 고친 뒤 G6 0.
- AST 따로(`/tmp/ch30-02/tools/extra_check.py` — 01 도구 복사): 걸린 것은 **챕터 예외와 허용 범위뿐** — 데코레이터 줄 하나(`@demo_app.get`) · 처리 함수 매개변수 힌트 하나(`limit: LimitDep`) · `async def` 다섯(제공 함수 `get_limit`·`get_short_limit`·`zero_timeout`·`two_second_timeout`, 처리 함수 `show_limit`) · 셀 맨 위 await 다섯 줄(셀 셋 — handoff 비동기 표 「Ch 28 이어 씀」) · `method:get` 셋(요청 방식 GET을 보내는 `demo_client.get`·앱 객체 `demo_app.get` — 딕셔너리 `.get` 아님, 거짓 양성). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`try`·`while`·별표 풀기·대입 풀기·기본값 매개변수(`x=Depends(f)` 모양 안 씀)·내놓는 값 힌트·변수 힌트·클래스·가짜 에이전트·`asyncio` **0**. 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **8줄** · 함수 본문 최대 **2줄** · 셀당 정의 하나.
- 금지어(`/tmp/ch30-02/tools/ban30.py` — 01 도구 그대로): 본문·노트북 마크다운·주석·`.mmd`·캡션·alt에서 걸린 것은 **허용한 것뿐** — 「주입」·「Agent」(제목 + 본문 b2·노트북 1절의 「제목의 ○○은」 풀이 한 번씩, 강사 확인) · 「토큰」(모두 「접근 토큰」 — 한정어 없는 「토큰」 0, 정규식 대조) · 「의존성」(이 절의 새 용어 — FastAPI 원어, 01 목록에 있던 주의 말) · 「로그」는 「프로그램」, 「열」은 「파일을 열 때」 거짓 양성. 「스트림」 한 곳(b7)은 고침. 「사용자가 금지한 표현(과정 규칙)」·「쉽게·간단히·당연히」 0.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/02-…ipynb`·`before/_src/02-*.html`)

1. **가짜 객체 클래스** `class StubAgent`(`ainvoke`가 `{'answer': '대체 응답'}`) + `lambda: StubAgent()` — 규격 §3 「정해 둔 응답을 내보내는 클래스」에 가깝고 G1 셋(`class_def`·`lambda`·준비 셀 제너레이터 식).
2. 준비 셀이 루트 커널에서 멈춤(`next((p for p in (start, *start.parents) …), None)` + `os.chdir`) — 01과 같은 문제.
3. 코드 셀 첫 줄 주석 0 · 결과 읽기 셀 0 · 제목 셀·그림 첨부 없음 · 한 셀에 가져오기·클래스·재정의·클라이언트.
4. 틀린 말·사실: b3 「Ch23의 체크포인터처럼 **생성 비용**과 수명주기가 다른 객체」(Ch 23 인계 — Ch 23은 생성 비용을 재지 않음) · b4 「`yield` 의존성으로 열고 정리」·「`Protocol`로 필요한 메서드를 선언」(실행 안 한 설명) · b4 비유 「공구 대여 창구」(「창구」 — Ch 30 금지 소품) · 「대체 Agent를 넣어도 경로, 스키마, 인증, 응답 변환은 실제 코드 그대로 실행」(가짜 객체 전제) · 도식 읽기 틀 색 문장.
5. 금지어: 주입(제목에도 — Ch 21 금지어)·반환·검증·라우트·세션·인터페이스·수명주기·보장·명시·지연·식별자·경로·스키마.
6. 참고 자료 둘(확인 2026-09-11, 설명 없음)·복습 한 줄 해설 넷.

## 바꾼 것

- **paired 설계(handoff §01 → §02 2·3·8)**: Before = 실습 앱의 제공 함수 `get_timeout`을 **0.0을 내놓는 이름 있는 `async def zero_timeout`**으로 재정의(클래스·`lambda`·가짜 에이전트 없음) → 첫 테스트 질문 **504**(`{'detail': 'Agent 응답 시간이 초과되었습니다'}` — 재정의가 뜻한 결과, 노랑) → **다음 테스트가 새 `TestClient(app)`로 보낸 보통 질문도 504, 재정의 딕셔너리 키 수 1**(Before 결함 결과, 빨강 — 재정의가 클라이언트가 아니라 앱 객체 속성이라는 사실을 출력으로) ↔ After = `app.dependency_overrides.clear()` → 키 수 0 → 같은 질문 **200** `질문을 확인했습니다: 대출 기간을 알려 주세요`. 값 바꿔 보기 = 재정의 딕셔너리의 값만 2.0을 내놓는 `two_second_timeout`으로 → **200인데 키 수 1**(남은 재정의가 상태 코드로 안 보임 — 한계, 빨강 0) → 마지막 셀에서 두 앱 모두 비움(키 수 0·0).
- **예시 부분(2절)**: 연습 앱 `demo_app` + 제공 함수 `get_limit`(요청마다 목록 `provider_calls`에 이름을 적음, 2.0) + `LimitDep = Annotated[float, Depends(get_limit)]`(Ch 13 02 표시 `Annotated` 이음 · FastAPI 문서의 이름에 담는 모양 = 실습 앱 `TimeoutDep` 모양 · 기본값 모양 `x=Depends(f)`는 과정 금지 문법이라 안 씀) + 처리 함수 `show_limit(limit: LimitDep)` → 요청 두 번에 기록 `['get_limit', 'get_limit']` · 재정의 `get_limit` → `get_short_limit`(0.5) → `{'limit': 0.5}`·기록 `[]`·키 수 1(「남은 재정의는 4절에서」).
- **실습 앱 가져오기(3절 — 02가 처음, handoff §01 → §02 4)**: 01 파일 위치 셀 글 그대로(생성기 `__main__`에서 `author_01.py`와 문자열 대조 `assert`) → `os.chdir(lab_path)` + `from agent_service.app import app, get_agent, get_timeout` → 앱 파일을 글로 읽어 `Depends(`가 든 줄 다섯과 `async def chat(` 정의 줄 출력(매개변수 넷 풀이 — `body` 입력 형식·`runtime`·`_token`·`timeout`, `-> ChatResponse`는 Ch 2 07 내놓는 값 힌트) → 셀 맨 위 await로 `get_timeout()` → `2.0`, `get_agent()` 두 번 → **같은 객체 `True`**(객체의 수명 — Ch 23 03 이음) → 접근 토큰 없이 **401** `{'detail': '인증 정보가 올바르지 않습니다'}` → 요청 머리의 칸 `Authorization`에 교재용 접근 토큰 → **200**.
- **「생성 비용」(Ch 23 인계) 고침**: 수명만 씀 — 결정적 그래프는 `agent.py` 46행이 파일을 가져올 때 한 번 컴파일(출력 `True`), 모델 에이전트는 `live_agent.py` 15~16행 `@lru_cache(maxsize=1)`로 첫 요청 때 한 번(설치판 소스로만 — 「노트북에서는 실행하지 않았습니다」), `lifespan` 없음, 「그래프를 만드는 데 걸린 시간은 재지 않았습니다」. `yield` 의존성·`Protocol`은 뺌.
- **「주입」**: 제목에만(강사 확인). 본문은 「처리 함수에 값을 넘겨 주기」·「바꿔 끼우기(재정의)」. b2·노트북 1절에 「제목의 주입(injection)은 … 원어」 한 번. 「의존성(dependency)」 첫 자리 세 문장(뜻 → 도서관 책 신청 예 → `Depends(get_limit)`).
- **`asyncio.wait_for` 첫 풀이 한 문장**(노트북 4절 결과 읽기·b4 「시간 제한과 상태 코드 504」) + 504 뜻 + `except TimeoutError`(Ch 16 05). 노트북은 `asyncio`를 가져오지 않음(앱 파일 78~80행이 씀).
- 노트북: 제목 셀(할 일 셋·준비물·기준 버전·강의와 실습 범위) · 오늘 볼 그림(02-1 첨부) · 설명 → 코드 → 결과 읽기 · 정리 세 줄 + 03 예고. 설치 셀 `fastapi==0.135.0`·`httpx==0.28.1`·`pydantic==2.12.5`·`starlette==1.6.0`·**`langgraph==1.2.11`·`langchain==1.4.0`**(잠금 판 — 앱 파일이 가져옴, 모델 객체는 만들지 않음). 키 셀 없음.
- 본문 b1~b10 새로(b3 = 01절 / Ch 13 02·Ch 2 12·Ch 28 01·Ch 16 05 / **Ch 2 11 테스트 격리**(B 트랙 — 뜻을 한 문장으로 다시) / **Ch 23 03 객체의 수명**·Ch 28 03 접근 토큰, b10 = FastAPI 문서 둘 + Python asyncio 문서(2026-09-29 확인) + 설치판 소스 행 둘). 복습 넷 → **다섯**(해설 포함). meta 「강의 1h | 실습 2.5h」 그대로(챕터 시수 합 유지), 「새 용어 4」(의존성·제공 함수·재정의(재정의 딕셔너리)·상태 코드 504 — 요청 머리는 01 응답 머리를 이은 말로 셈하지 않음).
- 그림: Mermaid **5장**(02-1 b4·노트북 · 02-2 b4 · 02-3 b5 · 02-4·02-5 b6 — viewBox 폭 453·416·456·657·297, 모두 868 이하) + 삽화 **1장**(02-6, 재생성 1회). 옛 `{{svg:02-흐름}}` 토큰 제거, 옛 그림 파일 셋(`02-흐름.svg·.excalidraw·.caption.md`)은 그대로.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-02/exp/`)

- `p1_scene.py`(노트북 장면 전체를 스크립트로, 5번): 출력 md5 **5/5 같음** — 연습 앱 `200 {'limit': 2.0}` 두 번·기록 둘 / 재정의 `{'limit': 0.5}`·기록 `[]`·키 수 1 / 실습 앱 키 수 0·`get_timeout` 2.0·같은 그래프 `True` / 401(`www-authenticate` 머리 없음 — 07 몫) / 200 / 재정의 504 → 새 클라이언트 504·키 수 1 → `clear()` 0·200 / 2초 재정의 200·키 수 1. 표준 오류 0.
- `p2_invoke.py`(03 인계용, 3번 같음): 실습 그래프에 동기 `invoke` → `TypeError: No synchronous function provided to "answer".` + 둘째 줄 `Either initialize with a synchronous function or invoke via the async API (ainvoke, astream, etc.)` · `asyncio.run(agent.ainvoke({"messages": ["세 단어 질문"]}))` → 키 `['answer', 'messages']`·답 `질문을 확인했습니다: 세 단어 질문`.
- 설치판 소스(fastapi 0.135.0): `applications.py` 969~984(속성 `dependency_overrides` = 딕셔너리, 설명 글 「This is for testing」) · `dependencies/utils.py` 629~643(요청마다 딕셔너리에서 원래 함수를 찾아 바꿔 낌 — `getattr(provider, "dependency_overrides", {})`를 요청 때 읽음) · 675~676(비동기 제공 함수 `await call(...)`) · `routing.py` 452~462(`solve_dependencies` 뒤 `if not errors:` — 의존성이 먼저). Python 3.12.13 `asyncio/tasks.py` 507~517(시간 제한 0 이하 → 작업을 기다리지 않고 취소 → `TimeoutError`).
- 공식 문서(2026-09-29 WebFetch): FastAPI Dependencies(요청마다 제공 함수를 부르고 결과를 매개변수에 넣음 · `Depends`에는 함수를 부르지 않고 넘김 · `CommonsDep = Annotated[dict, Depends(common_parameters)]` 「type alias」) · Testing Dependencies with Overrides(키 = 원래 제공 함수, 값 = 바꿔 낄 함수 · 비우기 예 `app.dependency_overrides = {}` · 「set the override at the beginning of the test … and reset it at the end」 — 노트북은 `clear()`, 문서 방법은 실행 안 함을 b7에) · Python asyncio `wait_for`(시간 제한이 지나면 작업을 취소하고 `TimeoutError`, 0 이하 동작은 문서에 없음 → 설치판 소스로).

## 실행 (새 커널)

| 실행 | 자리 | 키 | 결과 |
|---|---|---|---|
| 시험 tryA(`/tmp/ch30-02/try` 사본, `execute.py` 기본 `--cwd` = 프로젝트 맨 위, `PYTHONPATH` = `notebooks/`) | 루트 커널 | `OPENAI_API_KEY` 지움 | PASS 24셀 |
| 시험 tryB(사본, `--cwd` 실습 폴더 `notebooks/`) | 학생 커널 | 지움 | PASS 24셀, 셀별 24/24 같음, `outputs_sha256`까지 같음 |
| **A**(`run_section.sh … 02`, 시작 07:10:32Z · `executed_at` 2026-09-29T07:10:35Z) | 루트 커널 | 지움 | PASS 24셀(그림 첨부 단계에서 멈춤 — 02-1 PNG 전) |
| **B**(A 사본, `uv run … execute.py --cwd notebooks/`, 07:10:45Z) | 학생 커널 | 지움 | PASS 24셀 |

- **A ↔ B 셀별 출력 글자 24/24 같음**, `code_sha256` `c52cc10f20174814794fa5777b3b7e0770f2201aada1275662980fdc31abe2fc` 같음. **`outputs_sha256`은 다름**(A `2003205a3569603a5593a4766bb5cecd9e428b763200a5ac7de9c413b321fd40` · B `83a49271…`) — 설치 셀 출력이 B에서 스트림 둘(`fastapi` 줄 뒤에서 나뉨)로 저장되었을 뿐 글자는 같음(과정 요약 §9 「`outputs_sha256`은 흔들리므로 셀별 출력 글자 해시로 대조」). 시험 tryA·tryB는 `outputs_sha256`까지 같았음.
- 그 뒤 `--no-exec` 셋(렌더·첨부·빌드)에서 노트북 코드·출력·`executed_at` 그대로(첨부만 더함 — A 사본과 `cmpout` 24/24·`outputs_sha256` 같음, 생성기로 다시 만든 셀 글과도 53/53 같음) — 노트북 파일 **`b705c8aafca8680ae133653b19acd8954d59bc667bc429eeff04bc0c7df2f9a7`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에 새로 생긴 파일 0(`find -newer` — 노트북 02 말고, 앱을 가져와도 `agent_service/__pycache__` 그대로) · `.failure.json` 0 · 표준 오류 출력 0 · 설치 셀 출력에 pip 안내 한 줄.
- **모델 요청 0** · 서버 프로그램·포트·자식 프로세스 0 · 남은 프로세스 0(같은 프로세스 `TestClient`만).

## 앱 파일 고침 · `app.openapi()` 대조 · `tests/`

- **02는 앱 파일을 고치지 않음.** 이 절이 읽고 풀이하는 줄(`app.py` 29~38 제공 함수·63~67 이름 다섯·75~83 `chat`)은 과정이 푼 모양(`Annotated`·`Depends`·`async def`·내놓는 값 힌트 Ch 2 07)이고, 남은 금지 문법(`str | None` 기본값 매개변수·f-string·`try`·`removeprefix`·`raise … from`·`except Exception`·`.get`·`+=`·`AsyncIterable`)은 06(이어 받기 `get_resume_index`)·07(`require_token` — 07 After가 `HTTPBearer`로 바꿀 자리)·05·09(스트림·모델 처리 함수) 줄이라 그 절 몫. `get_timeout`의 `-> float` 하나만 고치는 것은 OpenAPI 중립이지만 절 몫 줄과 따로 고칠 까닭이 적어 두었음(기록).
- 확인: `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 · `pytest -q -p no:cacheprovider` **6 passed, 1 warning** · 앱 파일 해시 `app.py` `3455d405…`·`agent.py` `a6c42e63…`·`live_agent.py` `586a6a69…` 그대로. `openapi.json`·생성 SDK 손대지 않음.
- **주의(뒤 절 인계)**: 02 노트북 3절이 `app.py`에서 `Depends(`가 든 줄과 `async def chat(` 줄을 출력함 — 뒤 절이 그 줄을 바꾸면 02를 다시 실행하고 결과 읽기(이름 다섯·매개변수 넷)를 고쳐야 함.

## 도구 파일

- **만들지 않음** — 02는 앞 챕터에서 배운 평범한 함수를 쓰지 않음(01 `make_result`는 실습 앱이 대신함). 인증 머리 딕셔너리 `auth_headers`는 노트북 값(handoff §01 → §02 10). `serve_tools.py` 이름은 그대로 비어 있음.

## 고친 틀린 사실

- b3 「Ch23의 체크포인터처럼 생성 비용과 수명주기가 다른 객체」 → 「Ch 23 03절에서는 객체의 수명을 배웠습니다」 + 수명만(출력 `True`·소스 줄), 「걸린 시간은 재지 않았습니다」.
- b4 「`yield` 의존성으로 열고 정리」·「`Protocol`로 … 타입 검사」 → 뺌(실행 안 함).
- 「대체 Agent를 넣어도 … 실제 코드 그대로」(가짜 객체 전제) → 가짜 객체 없이 실제 조건(시간 제한 0)으로.
- 「테스트할 때도 실제 모델을 호출해야 하므로 느리고」(재지 않은 시간) → 뺌.
- 도식 읽기 틀 색 문장 → 그림마다 색·방향을 그림에 맞춰 새로.

## 그림

- Mermaid 다섯: 설계표 `02-figures.md`(렌더 전 작성) → `.mmd`·캡션 → 렌더 한 번 → PNG 다섯을 직접 열어 확인(색·방향·점선 갈래·빨강은 02-4 Before 결과 하나뿐·보라 0, 긴 코드 `dependency_overrides.clear()`는 `<br>`로 미리 나눔). 색 배정: 실습 앱 파일의 함수 초록 · 노트북에서 만든 함수 파랑(같은 요소는 다섯 장 모두 같은 색). G7 라벨 숫자(0.0·0.5·1·2.0·200·401·504·0) 모두 출력에 있음.
- 삽화 02-6: `02-6-…prompt.md` 상태 줄 — **1차 job `1a81d545-d48f-4766-8baf-140f2639c982` 탈락**(아래 선로에 짐칸 셋·주황 기관차 둘이 이어져 기관차 모두 넷 · 위쪽 빈 띠) → **2차 job `d90885eb-7e9f-4f36-8a63-0ce5e08e3c36` 채택**(재생성 1회, 서비스 쪽 실패 0) · 거래 2026-09-29T07:12:45.025669Z·07:14:00.857586Z 「Nano Banana Pro −2」 두 줄(**이 절 몫 4크레딧**, 잔액 2293 → 2289, 앞 거래 06:35:38Z는 Ch 30 01) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 저장 PNG `787953183138563bcf6b08f1269a6586c64549798c1b15d6035b94d63c8a67f7`(1100 × 614)와 채택 결과를 다시 받아 줄인 그림 픽셀 대조 bbox `None`·최대 차이 0 · 저장본 사본을 열어 선로 셋·열차 둘·초록 짐칸 넷·주황 기관차 둘·파란 기관차 하나·멈춤 막이 하나를 세고 그림 읽기를 씀. 01 소품(창고·파란 틀·차단봉·빈 화차) 되풀이 없음, 번호판 없음. 파란 기관차가 크게 그려진 점은 그림 읽기에 「크기는 짝짓지 않음」.

## 검사

- `run_section.sh … 02 --no-exec`: 렌더 다섯 · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 81 code cells (max 14 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `02-의존성으로-Agent-주입.html`: `{{` **0** · `[[` 0 · 인라인 SVG 5 · 삽화 JPEG 1 · b5 노트북 셀 15 · b6 노트북 셀 9.
- `pack.py … 02` → `qa/upgrade/review-pack/02-의존성으로-Agent-주입.md`.
- 보호 파일 255개: `manifest-changes.md` 「02절 뒤」에 덧붙임.

## 완료 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

| 문장 | 판정 |
|---|---|
| **Ch 2 11 b8** 「Ch 30 2절에서는 한 테스트가 남긴 대체 설정이 다음 질문까지 이어지는 실패를 다룹니다」(`_src`·HTML) | **참** — 02 Before가 첫 테스트가 남긴 재정의(= 대체 설정)로 다음 테스트의 질문이 504를 받는 장면 · b3가 「그 절 끝에서 예고한 대로」로 받음 |
| Ch 2 12 b8 「Ch 30 1절은 비동기 함수 안의 동기 호출이 …」 | 참(01 끝남 — 02는 건드리지 않음) |
| Ch 2 12 b8 「Ch 30 3절은 await로 Agent 실행을 기다립니다」 | 03 몫 — 02 b8·정리가 「03절 … 비동기 그래프를 await로 기다려 부르는 방법」으로 예고 |
| Ch 2 `_src/index.html` 「비동기 대기는 Ch 18의 API 호출과 Ch 30의 FastAPI에서 다시 사용」 | 참(01·02 `async def`·await) |
| Ch 25 04 b8(04 custom·09 messages) · Ch 29 05 b8(01 슬러그) | 02와 무관 — 슬러그 그대로 |
| Ch 31 01 b2·b3 「Ch30에서 FastAPI 요청 함수를 비동기로 작성」·Ch 34 04 b3·Part 7 소개 | 글만(참 — 대기 챕터, 고치지 않음). Ch 31 01 b3 「FastAPI 경로 함수」(「경로」)는 Ch 31 몫 |
| Ch 32 01·02 b3 「Ch30의 서비스 구현이 아직 없어도」·「Ch30에서 만든 서비스가 있다면」 | 글만(의존 없음 — 준비 노트 §5-4와 같음) |

## 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀) · 사용자 디스크 `.cache/ch30-02-view/`(삽화 보기 사본 두 장 — 새로 만든 폴더). 공용 도구·규격·과정 문서·Part 7 목록·zip·검사 스크립트·앱 파일·Ch 31 이후 파일은 고치지 않음.

## 강사 확인 대상

1. 제목 말 「주입」·「Agent」(제목에만 두고 b2·노트북 1절에서 한 번씩 풂).
2. 새 용어 「의존성」·「제공 함수」·「재정의(재정의 딕셔너리)」·「요청 머리」(용어 표는 handoff).
3. 셀 맨 위 await 셋(제공 함수를 직접 불러 값 보기 — Ch 28 01 이음) · 표시 `Annotated`를 이름에 담는 모양(`LimitDep`, 기본값 모양 대신).
4. 앱 파일 `app.py`를 이 절에서 고치지 않은 것(남은 금지 문법은 05·06·07·09 몫) · 노트북이 앱 파일 줄을 출력하는 것(뒤 절 결합).
5. 값 바꿔 보기를 「원래와 같은 2초를 내놓는 재정의」로 한 것(한계를 보이는 장면).
6. 삽화 02-6(재생성 1회 — 기관차 크기 차이는 그림 읽기에 밝힘).
7. 코드 양 29 → 105줄(셀 5 → 24).

## 남은 것 (마감 몫)

- `part7-practice.zip`에 02 노트북 새 판 반영(마감 때 한 번) · 02는 Part 7 묶음 실행 검사 대상 아님(01만).
- 옛 그림 `02-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-02-02.json` · 기기 `/tmp/ch30-02/`(사본·실험·삽화 원본 둘, 약 12MB) · 사용자 디스크 `.cache/ch30-02-view/`(1.2MB).
