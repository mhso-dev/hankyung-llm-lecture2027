# 07절 진단 — 인증 CORS 타임아웃 (paired)

- 작업일: 2026-09-29 · 작업자: 07절 작업자 · 생성기 `qa/upgrade/author_07.py`(`2aebd450…`)
- 읽은 것: `handoff.md`(머리·챕터 공통 전부·§06 → §07 전부, §01~§05 인계 훑음) · 준비 노트 `chapter-lead-notes.md`(§1 07 줄·§2 07·§3·§7-3·§7-4·§7-5·§7-6·참고 자료) · `06-diagnosis.md` · `06-figures.md` · `author_06.py`(전부 — 도구 파일 06 판·`check_tools06`·`FIND_LAB`·`table_html`·`html_text`) · `author_01.py`(`FIND_LAB` 자리)·`author_02.py`(`Annotated` 풀이·b3 모양)·`author_05.py`(`add_api_route` 풀이·「응답 문서(OpenAPI)」 말) · Ch 28 03 노트북 6절(`WWW-Authenticate 헤더: Bearer` 출력·결과 읽기)과 `_src`(인증·인가·접근 토큰 풀이) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 규격 전부 · 과정 요약(§1 Ch 16·Ch 28 줄, §2-19, Ch 16·22·28 용어 줄) · Ch 16 01·04 `_src` 학습 목표 · Ch 22 01 `_src` b4(훅·감싸기형 훅) · 옛 07 `_src`·노트북(`before/`) · 옛 08 `_src`(b3·b4·b6 — 08 인계용). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-07.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 4 · 1 · 7 · 0 · 10 · 16 · 3 = **41** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(주석·빈 줄·`%` 줄 뺌, `extra_check.py`) | 7 · 53 | **21 · 122** |
| 검사 문장 | 86 | **420** |

- 첫 실행 전 `upgrade_gates.py … --label wip-07 --section 07`: G1·G2 **0**, G6 4(70자 넘는 문장 넷 — b6 두 곳·b10 한 곳·노트북 사전 요청 풀이) → 문장을 나누고 단락을 둘로 나눠 G6 0. G7 3은 그림 전이라 당연(그림 뒤 0).
- AST 따로(`/tmp/ch30-07/tools/extra_check.py` — 06 도구 그대로): 걸린 것은 **챕터 허용 범위와 거짓 양성뿐** — 코드 셀 [18] 요청 주소 데코레이터 줄 `@bearer_app.get("/whoami")`·`async def whoami`·처리 함수 매개변수 힌트 `cred: BearerDep`(챕터 예외 셋) · `method:get` 둘(`@bearer_app.get`·`bearer_client.get` — 요청 방식 GET, 01 거짓 양성). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`while`·`try`·`raise`·별표 풀기·대입 풀기(for 포함)·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·클래스·가짜 에이전트·`asyncio`·셀 맨 위 await·`join`·딕셔너리 `.get`·`.items` **0**. 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **8줄** · 함수 본문 최대 **3줄**(`header_or_none`) · 셀당 정의 하나.
- 금지어(`/tmp/ch30-07/tools/ban30.py` — `_src`·노트북 마크다운·코드 주석·`.mmd`·캡션·alt): 걸린 것은 **허용한 것과 거짓 양성뿐** — 「사전」(모두 「사전 요청」 — 이 절이 정한 말, 아래 「말」) · 「토큰」(모두 「접근 토큰」 — 따로 세어 앞이 「접근 」 아닌 것 0) · 「의존성」(02 말) · 「로그」(← 「프로그램」). 「미들웨어」·「헤더」·「Agent」(본문)·「스트림」·「이벤트」·「노출」·「명시」·「돌려」·「반환」·「검증」·「최대」·「결정적」·「알 수 있습니다」·사용자가 금지한 표현·「쉽게·간단히·당연히」 **0**(링크 주소·코드 출력 안의 것 뺌). 옛 캡션 `07-흐름.caption.md`의 「명시」·「Agent」는 쓰지 않는 옛 그림 파일.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/07-…ipynb`·`before/_src/07-*.html`)

1. **가짜 클래스 `class SlowAgent`**(`ainvoke`·`astream` + `asyncio.sleep(0.05)`·`yield`) + `lambda` 둘로 `get_agent`·`get_timeout` 재정의 — 규격 §3 「정해 둔 응답을 내는 클래스」 · G1 넷. **저장 출력에 `logger.exception` Traceback 전문**(`[사용자 폴더]/…`·`/var/folders/…/ipykernel_…` 파일 위치).
2. **Before가 결함 장면이 아님**: 모르는 출처 사전 요청 → 400·허용 머리 없음(CORS 층이 제대로 막은 장면), After = 접근 토큰을 붙인 다른 요청 200(고친 것 없음).
3. 준비 셀이 루트 커널에서 멈춤(`next((p for p in (start, *start.parents) …), None)` + `os.chdir`) — 01~06과 같은 문제. 첫 줄 주석·결과 읽기 0. 한 셀 10~11줄.
4. b3 「Ch16에서 입력 검증과 비용 상한을, Ch22에서 호출 전후 처리를 배웠습니다」(「검증」 금지어 · 막연함) · b4 비유 「건물 출입구」(챕터 금지어 「출입구」, Ch 22 공항 검사·Ch 28 건물 입구 출입증 계열과 겹침) · b4·b7 실행하지 않은 운영 설명(토큰 발급·만료·회전·폐기, 요청 ID, 계층별 timeout, 사용자별 연결 상한, 403 설계, 하위 공급자 취소 「측정」) · 「토큰」 단독 7·「로그」·「검증」·「timeout」·「헤더」·「Agent」 · 도식 읽기 틀 색 문장(「보라색 상자는 Agent 실행」 — 모델 없는 절) · 복습 넷(해설 한 줄) · 참고 자료 둘(2026-09-11, 설명 없음).

## 바꾼 것

- **06 b8 조건(handoff §06 → §07 1)**: 「07절에서는 접근 토큰 검사와 다른 출처의 요청을 다루는 설정, 시간 제한을 함께 봅니다」 → **참**. 2절 `require_token`(56~60행)·요청 머리 셋 401·401·200 → 3절 시간 제한 0초 504 → 4절 CORS 설정(19~26행)·사전 요청 → 5·6절 Before·After → 7절 값 바꿔 보기.
- **paired Before = 실제 결함 둘(handoff §06 → §07 2 ①·②)**:
  - ① 노트북의 새 앱 객체 `wide_app` — `CORSMiddleware(allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])` + 실습 앱의 처리 함수 `chat`을 `add_api_route`로 이음(05 풀이 이어 씀) → `https://evil.example` 사전 요청 **`상태 코드: 200`·`허용 출처: https://evil.example`·`자격 증명 허용: true`**, 이어 보낸 POST(교재용 접근 토큰) **200·답·같은 두 응답 머리**(받은 결함 결과 — 빨강). **문서와 설치판이 다름**: FastAPI CORS 문서(2026-09-29 WebFetch)는 「None of allow_origins, allow_methods and allow_headers can be set to ['*'] if allow_credentials is set to True」 ↔ 설치판 starlette 1.6.0 `middleware/cors.py` 37행(`preflight_explicit_allow_origin = not allow_all_origins or allow_credentials`)·116~120행(사전 요청에 받은 출처를 적음)·166~168행(보통 요청에도) — 오류 없이 받은 출처를 그대로 적음. 본문은 출력 기준으로 쓰고 둘 다 밝힘(b6·b7). MDN CORS(최종 수정 2026-09-04)의 「자격 증명이 있으면 `*` 대신 출처를 이름으로」 조건을 받은 출처를 옮겨 적어 맞추는 셈이라는 한 문장.
  - ② **실습 앱 401의 응답 머리** — `상태 코드: 401`·**`WWW-Authenticate: None`**·`응답 머리 이름: ['content-length', 'content-type']`(빨강). RFC 9110 15.5.2 「The server MUST send a WWW-Authenticate header field」(2026-09-29 WebFetch)·MDN 401(최종 수정 2026-06-22). Ch 28 03 노트북 6절 출력 `WWW-Authenticate 헤더: Bearer`와 견줌.
- **After(노랑)**: ① **출처를 적은 실습 앱**(19~26행 — 허용 출처 `http://localhost:5173`·요청 방식·요청 머리를 이름으로) → 같은 사전 요청 `상태 코드: 400`·`응답 본문: Disallowed CORS origin`·`허용 출처: None`(자격 증명 머리 `true`는 설정 값이 늘 붙음 — `cors.py` 42~43·62~63행, 본문 b7에 밝힘) · 허용 출처 POST `200`·`허용 출처: http://localhost:5173`(After가 허용 출처를 막지 않음) · ② **노트북의 새 앱 `bearer_app` + `HTTPBearer()`**(`BearerDep = Annotated[object, Depends(bearer)]` — 02 모양, 처리 함수 `whoami(cred: BearerDep)`) → 머리 없음·`Basic abc` **`401 | Bearer | {'detail': 'Not authenticated'}`** · **`Bearer abc` → `200 | None | {'scheme': 'Bearer'}`**(보안 객체는 방식 이름만 보고 글은 견주지 않음 — 설치판 fastapi `security/http.py` 303~316행, After의 한계로 공개) · 응답 문서: 실습 앱 `securitySchemes` 없음 `False`·새 앱 `{'HTTPBearer': {'type': 'http', 'scheme': 'bearer'}}`·실습 앱 `/v1/chat` 매개변수 `authorization header`.
- **값 바꿔 보기(한계, 빨강 0)**: 사전 요청 없이 5절의 모르는 출처 POST를 출처를 적은 실습 앱에 → **`상태 코드: 200`·답·`허용 출처: None`** — 서버는 그대로 실행(**CORS는 브라우저가 지키는 규칙, 서버 보호 수단 아님** 한 문장 + 「서버를 지키는 일은 접근 토큰 검사」). 브라우저에서는 실행하지 않았다고 밝힘.
- **예시 부분(handoff §06 → §07 2 ③·5)**: 시간 제한 0초 → **도구 파일 `zero_timeout`**(06 판 그대로 가져옴, 고정 세 문장 + 커널 폴더 문장 둘 — 06 글) · 같은 셀에서 `clear()` → `접근 토큰이 있는 요청: 504 {'detail': 'Agent 응답 시간이 초과되었습니다'}` · **`접근 토큰이 없는 요청: 401 …`**(제공 함수가 몸통보다 먼저 멈춤 — 옛 b4 「인증 실패는 Agent 호출 전에」를 출력으로 뒷받침) · `비운 뒤 재정의 딕셔너리의 키 수: 0`. **`/v1/chat` 504는 앱이 기록하지 않아**(노트북 밖 표준 오류 0) 기록기 수준을 올리는 셀을 두지 않음 — 저장 출력 Traceback 0·`/var/folders` 0. 옛 `SlowAgent` 클래스·`lambda` 둘은 없앰.
- **말(handoff §06 → §07 3)**: 새 용어 **4**(meta 「새 용어 4」): **CORS**(제목 말 — 4절·용어 표 첫 자리에서 「제목의 CORS는 Cross-Origin Resource Sharing의 머리글자」 + 뜻 → 경비실·우편물 예 → 19~26행) · **출처(origin)**(방식·호스트 이름·포트 — 아파트 동·호수 예) · **사전 요청(preflight request)**(요청 방식 OPTIONS — 짐 부치기 전 전화 예) · **자격 증명(credentials)**(쿠키와 인증 정보 — 회원 카드 예). 「허용 출처」는 풀이로(새 말로 셈 안 함). 「토큰」 단독 → 「접근 토큰」(Ch 28 03) · 「인증」은 Ch 28 03 풀이 그대로(「요청을 보낸 쪽이 누구인지 확인하는 일」) · 「타임아웃」 → 제목에만, 본문 「시간 제한」 · 「헤더」 → 「요청 머리·응답 머리」 · **「미들웨어」 0** — `CORSMiddleware`는 코드 이름, 본문은 「CORS 층」·「이 설정을 맡은 층을 앱 객체 앞에 끼워 넣습니다」(강사 확인) · 「사전 요청」은 Ch 29 금지어 「사전」(← 딕셔너리)과 다른 낱말이라 씀(강사 확인) · 「보안 도구 클래스 `HTTPBearer`」·「보안 객체」는 풀이.
- **b3 고침(handoff §06 → §07 4)**: 옛 「Ch16에서 입력 검증과 비용 상한을, Ch22에서 호출 전후 처리」 → Ch 16 01(빈 질문·너무 긴 질문을 모델을 부르기 전에 막음 — 그 절 학습 목표)·Ch 16 04(호출 한도·비용 상한을 넘는 요청을 모델 부르기 전에 멈춤)를 「이 절의 접근 토큰 검사도 그래프를 기다리기 전에 401로 멈춤」과 이음 · Ch 22 01(감싸기형 훅은 호출 하나를 앞뒤로 감쌈)을 「CORS 설정 층도 처리 함수 앞에서 요청을 보고, 나가는 응답에 응답 머리를 덧붙임」(`cors.py` 91~94·152~174행)과 이음 · 02절(교재용 접근 토큰·401 한 번·`zero_timeout` 504·재정의는 같은 셀에서 비움) · 06절(제공 함수가 처리 함수보다 먼저 불려 응답 전에 멈춤) · Ch 28 03(인증·접근 토큰·401과 `WWW-Authenticate: Bearer`).
- **b4 비유(handoff §06 → §07 3)**: 「건물 출입구」 → 챕터 계열 **「화물 열차와 번호판 차량」 — 번호판 차량(트럭)을 처음 씀**: 짐칸(서버)·짐(응답)·꼬리표(응답 머리 `access-control-allow-origin`)·번호판 색(출처)·트럭 회사(브라우저) · 「찾아온 트럭의 번호판 색을 꼬리표에 그대로 적어 주는 역」이 Before · 비유와 다른 점(서버는 꼬리표가 맞지 않아도 답을 보냄·막는 쪽은 브라우저뿐·서버는 접근 토큰 검사가 지킴·브라우저에서 실행하지 않음).
- **실행하지 않은 운영 설명(handoff §06 → §07 「고칠 틀린 사실」)**: 접근 토큰 발급·만료·회전·폐기 → b7 「접근 토큰을 만들고 바꾸고 없애는 일은 이 절에서 다루지 않았습니다」 · 요청 ID·계층별 timeout·사용자별 연결 상한·403 설계·네트워크 패널 → 뺌 · 하위 공급자 취소 → b7 「모델을 부르는 그래프라면 끊은 뒤 모델 쪽 요청도 멈추는지 따로 확인해야 … 실행하지 않았습니다」 · `HTTPException`의 `headers` 인자로 401에 머리를 붙이는 방법 → FastAPI Handling Errors 문서로만(「이 노트북에서는 실행하지 않았습니다」).
- 노트북: 제목 셀(할 일 셋·준비물·기준 버전·강의와 실습 범위) · 오늘 볼 그림(07-1 첨부) · 1 준비(설치 여섯·가져오기 + 도구 파일·파일 위치 셀·앱 가져오기) · 2 접근 토큰 검사 · 3 시간 제한 · 4 CORS와 사전 요청 · 5 Before · 6 After · 7 값 바꿔 보기 · 정리 세 줄 + 08 예고. 파일 위치 셀은 01절 셀 글 그대로(`author_06.FIND_LAB` → 생성기 `__main__`에서 `author_01.py`와 문자열 대조 `assert`). 설치 셀은 06과 같은 여섯(잠금 판). 키 셀 없음.
- 본문 b1~b10 새로(b10 = FastAPI CORS·MDN CORS·MDN 401·RFC 9110 15.5.2·FastAPI Security Tools HTTPBearer·FastAPI Handling Errors(여섯 모두 2026-09-29 WebFetch, MDN은 최종 수정일 함께) + 설치판 starlette `cors.py`·fastapi `security/http.py` 행 + 실습 파일 행). 복습 넷 → **다섯**(해설 포함). meta 「강의 1h | 실습 2.5h」 그대로(챕터 시수 합 유지).
- 옛 `{{svg:07-흐름}}` 토큰 제거, 옛 그림 파일 셋(`07-흐름.svg·.excalidraw·.caption.md`)은 그대로.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-07/exp/`)

- `p1_scene.py`(노트북 장면 전체 + 덧붙여 본 값, 5번): 출력 md5 **5/5 같음**(`6c2a30e81060b212b9818e47eb373035`), 표준 오류 0. 덧붙여 본 값: 모든 출처 앱의 사전 요청 허용 요청 머리는 요청한 `Authorization, Content-Type`을 그대로, 허용 요청 방식은 일곱 전부(`cors.py` 28~29행) · 허용 출처 사전 요청의 `vary: Origin` · 실습 앱 사전 요청 400 응답의 응답 머리 이름 여섯(`access-control-allow-origin` 없음) · 새 앱 응답 문서 `/whoami` GET `security: [{'HTTPBearer': []}]` · 실습 앱 `/v1/chat` 매개변수 `{'name': 'authorization', 'in': 'header', 'required': False, …}`.
- `p2_openapi.py`: `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 `True` · 정렬 직렬화 `d2fb94f6…`(4825자) · `openapi` `3.1.0` · 요청 주소 다섯(`/health`·`/v1/chat`·`/v1/chat/live`·`/v1/chat/stream`·`/v1/chat/live/stream`) · `securitySchemes` 없음.
- 공식 문서(2026-09-29 WebFetch): FastAPI CORS(출처 정의·`allow_credentials=True`면 세 칸 모두 `['*']` 불가·사전 요청 200/400 「for informational purposes」·기본값 `allow_methods ['GET']`·`max_age 600`·credentials 「Authorization headers, Cookies, etc」) · MDN CORS(최종 수정 2026-09-04 — CORS 정의·사전 요청 `OPTIONS`·단순 요청 조건(요청 머리 `Authorization`·본문 종류 `application/json`은 조건 밖)·자격 증명 요청에 `*` 금지·허용 출처 머리가 없으면 자격 증명 요청의 응답을 무시) · MDN 401(최종 수정 2026-06-22) · RFC 9110 15.5.2 · FastAPI Security Tools(HTTPBearer — 결과는 `scheme`·`credentials`, 글을 견준다는 설명 없음) · FastAPI Handling Errors 「Add custom headers」.
- 설치판 소스 행(본문에 적은 것): starlette 1.6.0 `middleware/cors.py` 12(늘 허락하는 요청 머리 넷)·35~37·42~43·62~63·91~94·116~122·143~148(주석 「its up to the browser to enforce the CORS policy」)·166~168 · fastapi 0.135.0 `security/http.py` 84~92(401 + `WWW-Authenticate`)·303~316(방식 이름만 견줌) · 실습 `app.py` 19~26·56~60·78~82.

## 실행 (새 커널)

| 실행 | 자리 | 키 | 결과 |
|---|---|---|---|
| 시험 tryA(`/tmp/ch30-07/tryA` 사본, `execute.py` 기본 `--cwd` = 프로젝트 맨 위, `PYTHONPATH` = `notebooks/`, 10:12:01Z) | 루트 커널 | `OPENAI_API_KEY` 지움 | PASS 21셀 |
| 시험 tryB(사본, `--cwd` 실습 폴더 `notebooks/`, `PYTHONPATH` 지움, 10:12:13Z) | 학생 커널 | 지움 | PASS 21셀, tryA와 셀별 21/21 같음 |
| **A**(`run_section.sh … 07`, `executed_at` 2026-09-29T10:12:30.060336Z) | 루트 커널 | 지움 | PASS 21셀(그림 첨부 단계에서 멈춤 — 07-1 PNG 전) |
| **B**(A 사본 `/tmp/ch30-07/B`, `execute.py --cwd notebooks/`, `PYTHONPATH` 지움, 10:12:39Z) | 학생 커널 | 지움 | PASS 21셀 |

- **A ↔ B 셀별 출력 글자 21/21 같음**(이은 글 해시 `a796947c41e44e3c` 같음), `code_sha256` `e9a38985d45644592aec280ab9c9589765bd187500af2e55f4f3fbd3f679ca5c` 같음. **`outputs_sha256`은 다름**(A `ff1e1ec601d4deb85681ecb65ca53a3d86589bf0e6206f97344d8c3e22263fc4` · B `1a61016d54d14a25ae5428121749084f60e98fa8fdac856055bbc16dc17a0376`) — 까닭: 설치 셀 [1]의 표준 출력 스트림이 A는 66 + 100글자 둘로 나뉨, B·tryA는 166글자 하나(합친 글은 같음 — 02·03·05·06 선례, tryB는 A처럼 나뉨). 요청 0이라 셀 [2]~[21] 출력은 구조까지 같음. 초·ID·포트를 출력하는 셀 없음.
- 그 뒤 `--no-exec` 셋(렌더·첨부·빌드)과 `--src-only` 둘에서 노트북 코드·출력·`executed_at` 그대로(A 사본과 `cmpout` 21/21·`outputs_sha256` 같음) — 노트북 파일 **`4f57e3336d2a2536c91536fee22a48f46f8bb6a9e7e4970ec88310752a09ef88`**. `mdpatch`는 쓰지 않음.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에 새로 생기거나 바뀐 파일은 노트북 07뿐(`find -newer` — `agent_service/__pycache__` 그대로, pyc 0) · `.failure.json` 0 · 노트북 표준 오류 출력 0·`Traceback` 0·`/var/folders` 0 · 설치 셀 출력에 pip 안내 한 줄.
- **모델 요청 0** · 서버 프로그램·포트·자식 프로세스·브라우저·node 0 · 남은 프로세스 0(`ps` — uvicorn·node·ipykernel·jupyter 없음).

## 앱 파일 고침 · `app.openapi()` 대조 · `tests/`

- **07은 앱 파일을 고치지 않음.** 2절이 `app.py` 56~60행을, 4절이 19~26행을 글로 읽어 출력만 함 — 56행 `str | None`·기본값 `= None`·`-> str`, 58행 f-string은 출력된 앱 파일 줄로 두고 뜻만 풂(「58행의 f-string은 이 과정의 노트북에서 쓰지 않는 모양이라, 뜻만 봅니다」 — 06 모양). **401에 `WWW-Authenticate`를 붙이도록 앱을 고치지 않은 까닭**: `require_token`을 `HTTPBearer`로 바꾸면 응답 문서에 `securitySchemes`가 생기고 `/v1/chat` 등의 매개변수 `authorization`이 빠져 `openapi.json`(`06e5d1b9…`)·생성 SDK(`client/generated/apis/DefaultApi.ts`의 `authorization?: string | null` 매개변수 넷)·TS 시험·02~06 출력(줄 번호)이 바뀜 — 노트북의 작은 앱으로만 보임(handoff §06 → §07 2 ②). `HTTPException(…, headers=…)`로 머리만 붙이는 방법은 응답 문서를 바꾸지 않을 수 있으나 실행하지 않음(강사 확인).
- 확인: `app.openapi()` 직렬화 sha256 **`06e5d1b9…`** = `openapi.json` 바이트 같음 · `pytest -q -p no:cacheprovider` **6 passed, 1 warning** · 앱 파일 해시 `app.py` `3455d405…`·`agent.py` `a6c42e63…`·`live_agent.py` `586a6a69…`·`schemas.py` `ed77b197…`·`__init__.py` `1c7d7aef…`·`tests/test_app.py` `f8611741…` 그대로. `openapi.json`·생성 SDK·`client/*.ts` 손대지 않음.

## 도구 파일 — 바꾸지 않음

- 이 절이 쓰는 앞 절 함수는 02절 `zero_timeout` 하나 — 06 판 도구 파일(`e1a1464d0f647e0b2ca99fd14338eeb22c596effd405b5acf2ee49ac1d2c704d`)에 이미 있어 `from serve_tools import zero_timeout`만. 06 노트북 함수(`read_events`·`event_names`·`last_event_id`·`token_values`·`status_says_ok`·`ended_with_done`)는 07이 쓰지 않아 옮기지 않음(SSE 응답을 읽지 않음).
- 이 절이 처음 가르친 함수 `header_or_none(response, name)`(응답 머리 한 칸, 없으면 `None`)은 07 노트북에 둠 — 08이 다시 쓰면 08이 옮김(`author_06.TOOLS06`으로 시작하는 판 + 07 노트북 셀과 문자열 대조).
- 생성기 `__main__`: `author_06.check_tools06()`(06 판 대조 사슬 그대로 통과) + 디스크 파일이 `author_06.TOOLS06`과 같은지 `assert` — 도구 파일을 쓰는 줄은 없음. 04·06 노트북 영향 없음(파일 그대로). 공개 목록 두 곳 그대로.

## 고친 틀린 사실

- b3 「Ch16에서 입력 검증과 비용 상한을, Ch22에서 호출 전후 처리」 → Ch 16 01·04·Ch 22 01이 실제로 가르친 것(위 「b3 고침」).
- b4 「건물 출입구」 비유 → 화물 열차와 번호판 차량 계열.
- Before(모르는 출처 사전 요청 400 — 제대로 막은 장면) → 실제 결함 둘(모든 출처 + 자격 증명 / 401에 `WWW-Authenticate` 없음). After(접근 토큰을 붙인 다른 요청) → 출처를 적은 설정·`HTTPBearer`.
- 「SlowAgent + 0.01초 → 504·스트림 error」(가짜 클래스) → 도구 파일 `zero_timeout`으로 `/v1/chat` 504만(스트림 쪽은 06 결과를 「06절에서 본 것처럼」 한 문장).
- 옛 b4 「단일 ainvoke는 아직 헤더를 보내지 않아 504로 바꿀 수 있습니다」 → 참(말만 고침 — 「그래프를 다 기다린 뒤에 응답을 시작하므로」) · 「CORS는 브라우저 정책이며 서버 간 호출 인증을 대신하지 않습니다」 → 참(7절 출력으로 뒷받침) · 「인증 실패는 Agent 호출 전에 끝나야」 → 3절 출력(0초에도 401)으로 뒷받침.
- 실행하지 않은 운영 설명 → 뺌 또는 「실행하지 않았습니다」(위).

## 그림

- Mermaid 넷: 설계표 `07-figures.md`(렌더 전 작성) → `.mmd`·캡션 → 렌더 → PNG 넷을 직접 열어 확인(stage 사본): 첫 렌더에서 라벨 여섯이 낱말 자리에서 저절로 줄바꿈(끊김은 아님) → 넷 모두 `<br>`로 미리 나눠 다시 렌더 → 07-1(`flowchart TB` 한 줄 다섯 + 점선 갈래 둘, viewBox 폭 **610**) · 07-2(한 줄 넷, 폭 **266**) · 07-3(공통 상자 + 칸 둘, 폭 **619**) · 07-4(공통 상자 + 칸 둘, 오른쪽 칸 안 `~~~`, 폭 **669**) — 모두 868 이하, 끊긴 라벨 0, 색은 설계표대로(초록 보낸 요청·실습 앱 파일 / 파랑 `wide_app` 설정 / 노랑 출력 / 회색 CORS 층·브라우저 / **빨강 07-3 Before 결과·07-4 Before 401 둘** / 보라 0). 라벨 숫자는 출력에 있는 200·400·401·504·0·5173뿐(설치판 소스 줄 번호는 라벨에 안 씀).
- 삽화 07-5: **1차 job `58026534-d2dd-4032-a405-ad344ea9562b` 채택(재생성 0)** · 거래 2026-09-29T10:15:02.663841Z 「Nano Banana Pro −2」(**이 절 몫 2크레딧**, 잔액 2277 → 2275, 앞 거래 09:35:17Z는 Ch 30 06) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 원본 `4533d86a…`(2752 × 1536) → 저장 PNG `10981ab5f082757275862cd482c80b12ef7082dc9ea4ebe2d09cae2b7208e1a1`(1100 × 614) · 결과를 다시 받아 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0 · 저장본 사본과 원본 확대 둘을 열어 은색 짐칸 하나(옆문 열림)·트럭 둘·노란 트럭(번호판 노란색, 흰 자루 **넷**, 보이는 꼬리표 **셋** 모두 노란색)·파란 트럭(번호판 파란색, 빈 짐칸)·사람·글자·숫자·화살표 없음을 세고 그림 읽기를 씀. **거의 흰 가로줄 109 / 614**(06 115). **설계와 다른 점**: 자루 셋 → 넷(보이는 꼬리표 셋) · 차체 색도 번호판과 같은 색 — 자루 수는 어떤 값과도 짝짓지 않았고 관계(꼬리표 색이 맞는 트럭만 실음)가 그대로 읽혀 채택. 그림은 After 설정의 모습이라고 그림 읽기에 밝힘. 01~06 소품 되풀이 없음, 번호판 차량(트럭)을 처음 그림.

## 검사

- `run_section.sh … 07 --no-exec`(마지막): 렌더(도장이 같아 다시 그리지 않음) · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 173 code cells (max 14 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `07-인증-CORS-타임아웃.html`(`7e3fc234…`): `{{` **0** · `[[` 0 · 인라인 SVG 4 · 삽화 JPEG 1.
- `pack.py … 07` → `qa/upgrade/review-pack/07-인증-CORS-타임아웃.md`(`73439143…`).
- 보호 파일 255개: `manifest-changes.md` 「07절 뒤」에 덧붙임.

## 완료 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

`grep -rn 'Ch *30' textbook/part1 part2 part5 part6 part7 --include=*.html | grep -v ch30-fastapi`(`qa/` 뺌) + `CORS`·`WWW-Authenticate`·`local-demo-token`으로 챕터 밖 검색:

| 문장 | 판정 |
|---|---|
| Ch 2 11 b8(2절)·Ch 2 12 b8(1절·3절)·Ch 2 `index.html` 「Ch 30의 FastAPI에서 다시 사용」 | 07과 무관 — 참 |
| Ch 29 05 b8(01) · Ch 1 01 과정 지도 · Part 7 소개 「Ch30의 요청·응답 형식에서 시작해 …」 | 07과 무관 — 참 |
| Ch 28 03 HTML(임베드 노트북 출력 `WWW-Authenticate 헤더: Bearer`) | 07이 기대는 쪽 — 참(07 b3·5절이 그 출력을 가리킴) |
| Ch 24 `author_01.py` 28행 주석(Ch 30 06) | 07과 무관 — 참(06 판정 그대로) |
| Ch 31 01 b2·b3 「Ch30에서는 FastAPI 경로 함수를 비동기로」 · Ch 32 01·02 「Ch30의 서비스」 · Ch 34 04 b3 | 글만(대기 챕터, 고치지 않음 — Ch 31 「경로 함수」는 이 챕터 말로는 「처리 함수」) |

- 완료·대기 챕터에서 Ch 30 07(CORS·인증·401)을 가리키는 문장 없음(Part 7 목차의 절 제목만).

## 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀 — `86a79ba4…`) · 사용자 디스크 `.cache/ch30-07-view/`(삽화 보기 사본 셋 — 새로 만든 폴더). 공용 도구·규격·과정 문서·zip·검사 스크립트·앱 파일·TS 파일·도구 파일·공개 목록·Ch 31 이후 파일은 고치지 않음.

## 강사 확인 대상

1. 새 말 「CORS」·「출처」·「사전 요청」·「자격 증명」과, 「사전 요청」을 Ch 29 금지어 「사전」(딕셔너리)과 다른 낱말로 쓴 것 · 「미들웨어」 대신 「CORS 층」(`CORSMiddleware`는 코드 이름)으로 부른 것 · 제목 「인증 CORS 타임아웃」 그대로(본문 첫 자리 풀이).
2. Before를 결함 둘(모든 출처 + 자격 증명 / `WWW-Authenticate` 없는 401)로 세운 것 — ②의 After가 실습 앱을 고친 판이 아니라 노트북의 작은 앱(`HTTPBearer`)인 것과, 그 After의 한계(`Bearer abc` → 200)를 같은 셀에서 공개한 것.
3. FastAPI 문서(「불가」)와 설치판 starlette 1.6.0(받은 출처를 그대로 적음)이 다른 것을 출력 기준으로 쓰고 둘 다 밝힌 것.
4. 실습 앱의 401에 `WWW-Authenticate`를 붙이지 않고 둔 것(08 `openapi.json`·생성 SDK와 어긋나지 않게) — 붙인다면 `HTTPException(headers=…)` 방법이 응답 문서를 바꾸는지 08 이후에 확인할 일.
5. 삽화 자루 수가 설계(셋)와 다른 넷인데 재생성하지 않은 것(값과 짝짓지 않음).
6. 앱 파일 56·58행(`str | None`·기본값·f-string)을 고치지 않고 「뜻만 봅니다」로 둔 것(고치면 02~06 출력이 바뀜).

## 남은 것 (마감 몫)

- `part7-practice.zip`에 07 노트북 새 판 반영(마감 때 한 번) · 07은 Part 7 묶음 실행 검사 대상 아님(01만).
- 옛 그림 `07-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-07-07.json` · 기기 `/tmp/ch30-07/`(사본 넷·실험·삽화 원본 둘·도구 복사본, 약 8MB) · 사용자 디스크 `.cache/ch30-07-view/`(보기 사본 셋).
