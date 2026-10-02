# 08절 진단 — OpenAPI와 TS SDK (experiment)

- 작업일: 2026-09-29 · 작업자: 08절 작업자 · 생성기 `qa/upgrade/author_08.py`(`64752ad1…`)
- 읽은 것: `handoff.md`(머리·챕터 공통 전부·§07 → §08 전부, §01~§06 인계 훑음) · 준비 노트 `chapter-lead-notes.md`(§0·§1 08 줄·§2 08·09·§7-1~7-6·§8) · `07-diagnosis.md`·`07-figures.md`·`07-5 prompt` · `author_07.py`(전부)·`author_05.py`(experiment 모양·실행 1·2·결과 표)·`author_06.py`(도구 파일 06 판·`check_tools06`·`FIND_LAB`)·`author_04.py`(`TOOLS`·가드) · `AGENT-BRIEF.md`·`PLAYBOOK.md`·규격 전부(§2·§2-7·§3·§4·§5·§6·§7·§8) · 과정 요약(§2-11 Ch 19·§3·§8·§9) · Ch 19 02 `_src` 학습 목표·노트북(`model_json_schema()` 셀) · 06 `_src`(함수 fetch 풀이·b7 Ch 31 문장) · 옛 08 `_src`·노트북(`before/`) · 실습 폴더 `app.py`·`schemas.py`·`live_agent.py`·README·`openapitools.json`·`pyproject.toml`·생성 SDK `DefaultApi.ts`·`models/ChatRequest.ts`·`.openapi-generator/FILES`·`VERSION` · Part 7 공개 목록·`part7-practice.zip` 목록 · 옛 09 노트북 코드(인계용). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-08.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 1 · 1 · 4 · 0 · 6 · 17 · 3 = **32** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(주석·빈 줄·`%` 줄 뺌, `extra_check.py`) | 4 · 26 | **22 · 136** |
| 검사 문장 | 80 | **401** |

- 첫 실행 전 `upgrade_gates.py … --label wip-08 --section 08`: **G1·G2 0**, G6 14(영문 시작 조사 「SSE로」·「JSON으로」·「README는」·「FastAPI가」·코드 시작 하나, 70자 넘는 문장 둘, 게이트 금지어 「돌려 보」 둘) → 「SSE 사건으로 답하는」·「JSON 글로 답하는」·「실습 폴더 README는」·「라이브러리 FastAPI가」·「실행해 보니」로 고치고 문장을 나눠 두 번째 검사에서 G6 0. G7 3은 그림 전이라 당연(그림 뒤 0).
- AST 따로(`/tmp/ch30-08/tools/extra_check.py` — 07 도구 그대로): 걸린 것은 **거짓 양성뿐** — `method:get` 다섯(`client.get`·`header_client.get`·`bearer_client.get` — 요청 방식 GET, 01 거짓 양성). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`while`·`try`·`raise`·별표 풀기·대입 풀기(for 포함)·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·클래스·데코레이터·`async def`·셀 맨 위 await·`asyncio`·`sorted`·`join`·딕셔너리 `.get`·`.items` **0**(챕터 예외도 0). 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **10줄**(`RUN2`·`RUN_REQUESTS`) · 함수 본문 최대 **3줄**(`print_lines_with`) · 셀당 정의 하나.
- 금지어(`/tmp/ch30-08/tools/ban30.py` — `_src`·노트북 마크다운·코드 주석·`.mmd`·캡션·alt): 걸린 것은 **허용한 것과 거짓 양성뿐** — 「토큰」(모두 「접근 토큰」 — 앞이 「접근 」 아닌 것 0을 따로 셈) · 「의존성」(02 말) · 「로그」(← 「프로그램」). 「스키마」·「경로」·「엔드포인트」·「라우트」·「필드」·「헤더」·「인터페이스」·「캐시」·「스트림」·「이벤트」·「반환」·「검증」·「보장」·「명시」·「노출」·「사전」·「Agent」(본문)·「돌려」·사용자가 금지한 표현·「쉽게·간단히·당연히」 **0**(코드·링크 주소·출력 안의 것 뺌).

## 수정 전 주요 문제 (옛 판 — `before/notebooks/08-…ipynb`·`before/_src/08-*.html`)

1. **실습 폴더 `openapi.json`을 다시 씀**(`path.write_text(json.dumps(schema, ensure_ascii=False, indent=2))`) · **저장 출력에 `path.resolve()` 사용자 폴더 위치**(`[사용자 폴더]/working/claude/projects/…/openapi.json`).
2. 실험이 실험이 아님: 「같은 앱 객체에서 두 번 만든 정렬 직렬화가 같다」(`동일: True 문자 수: 4885`, `ensure_ascii` 기본값) — 값을 바꾸지 않은 성질 확인.
3. 준비 셀이 루트 커널에서 멈춤(`next((p for p in (start, *start.parents) …), None)` + `os.chdir`) — 01~07과 같은 문제. 첫 줄 주석·결과 읽기 0. `assert` 셋(`` 끝 글자 등).
4. b3 「01절의 Pydantic 모델, 05절의 SSE 응답, 07절의 인증을 한 문서로 모아」 — 실습 앱 인증은 요청 머리 매개변수라 응답 문서에 보안 방식 칸이 없음(07 출력 `False`) · b4 비유 「건축 도면」 · 실행하지 않은 설명(「TypeScript 타입이 빌드 오류를 줄이지만」·「CI에서 검사」·「operationId를 명시적으로 관리」·「생성물 컴파일은 … 증거」) · 도식 읽기 틀 색 문장(「보라색 상자는 Agent 실행」 — 모델 없는 절) · **b8 「Ch31에서는 이벤트를 데이터베이스에 저장해 프로세스 재시작 뒤에도 복구합니다」(거짓)** · 「스키마」·「라우트」·「경로」·「필드」·「검증」·「보장」·「사전」·「명시」·「헤더」 · 복습 넷(해설 한 줄) · 참고 자료 둘(2026-09-11, 설명 없음).

## 바꾼 것

- **07 b8 조건(handoff §07 → §08 1)**: 「08절에서는 앱 객체가 만든 응답 문서를 파일로 쓰고, 그 문서로 만든 TS 코드를 봅니다」 → **대체로 참 — 단 「파일로 쓰고」는 한정**: 08은 파일을 쓰지 않고, 파일에 쓸 글(`json.dumps(openapi_doc, ensure_ascii=False, indent=2)`)을 만들어 실습 폴더 `openapi.json`과 견줌(`두 글이 같은가: True`) + 결과 읽기에 「파일로 쓸 때는 이 글을 `with open(…, "w", encoding="utf-8")`로 연 파일에 적습니다」(실행하지 않은 모양으로 한 문장). 07 `_src` b8은 고치지 않음(이 절 하나만 — 강사 확인 1).
- **응답 문서 읽기(2절 — 코드 셀 [5]~[11])**: 맨 위 칸 `['openapi', 'info', 'paths', 'components']`·`OpenAPI 판: 3.1.0`·칸 info(앱 17행 제목·판 `1.0.0`) · 요청 주소 다섯과 요청 방식(`/openapi.json`은 목록에 없음 — 설치판 `applications.py` 1117행) · `/v1/chat` POST 칸 다섯·`operationId: chat_v1_chat_post`·요청 본문 형식 `{'$ref': '#/components/schemas/ChatRequest'}`·`응답 코드: ['200', '422']`·200 `ChatResponse`·매개변수 `authorization header` · 형식 이름 다섯·꼭 채울 칸 둘·`'maxLength': 500`·`'minLength': 1`·`pattern`·**`model_json_schema()로 만든 딕셔너리와 같은가: True`(Ch 19 02 방법과 잇기)** · `/v1/chat: ['application/json'] ['schema']` ↔ `/v1/chat/stream: ['text/event-stream'] ['itemSchema']` · 두 번째 부르기 같은 객체 `True`·`openapi_schema`도 같은 객체 `True`(1절 출력 `None` → 담아 둠, `applications.py` 1083~1084행) · 시험용 클라이언트 `/openapi.json` `200`·`application/json`·같은 딕셔너리 `True`. 옛 b6 「두 직렬화가 같았다」는 이 「같은 객체」 한 셀로 낮춤.
- **`openapi.json`(3절 — 셀 [12])**: **쓰지 않음**. 새로 만든 글·파일 글 `9987`자·`두 글이 같은가: True`·`ensure_ascii`를 뺀 글과는 `False`·파일 첫 세 줄. 파일 해시 `06e5d1b9…` 그대로(보호 파일 목록 값과 같음).
- **생성 SDK 읽기(4절 — 셀 [13]~[18])**: 노트북 함수 `print_lines_with(text_lines, word)`(정의 셀) · `openapitools.json` → `생성기 판: 7.25.0` · `DefaultApi.ts` 머리 주석 7·10·12행(문서 판 `1.0.0`·생성기가 만듦·「Do not edit the class manually」) · 함수 다섯의 이름과 내놓는 값(140·278행 `Promise<void>` · 190·328행 `Promise<ChatResponse>` · 227행 `Promise<HealthResponse>`) · 응답 감싸기 134·272행 `VoidApiResponse` ↔ 184·221·322행 `JSONApiResponse` · 요청 인자 선언 넷(37·52·63·74행)과 `authorization?: string | null`(45·60·71·82행) · `models/ChatRequest.ts` 25·29행(`question`·`threadId`)·52·68행(`thread_id` ↔ `threadId`)·글자 수 조건 줄 0. **`.openapi-generator/FILES`·`VERSION`은 학생 묶음에 없어(공개 목록 18줄 = 생성 파일 18) 읽지 않음** — 생성기 판은 묶음에 있는 `openapitools.json`에서. 노트북은 `node`·`npx`를 부르지 않음(파이썬으로 파일만 읽음).
- **실험(5절 — 셀 [19]~[22], handoff §07 → §08 5)**: 가설 = 07의 두 앱은 인증 방식 말고도 처리 함수·요청 주소·요청 방식이 달랐으므로, 같은 처리 함수 `health`(실습 앱)를 같은 요청 주소 `GET /v1/ping`으로 새 앱 객체 둘에 `add_api_route` — **바꾼 값 = 인자 `dependencies`에 적은 것 하나**: 실행 1 `[Depends(require_token)]`(실습 앱 제공 함수) ↔ 실행 2 `[Depends(bearer)]`(`bearer = HTTPBearer()`). 결과(매번 같은 값): 보안 방식 칸 `False` ↔ `True`(`{'HTTPBearer': {'type': 'http', 'scheme': 'bearer'}}`) · 요청 주소의 칸 `['summary', 'operationId', 'parameters', 'responses']` ↔ `['summary', 'operationId', 'responses', 'security']`(`[{'HTTPBearer': []}]`) · 응답 코드 `['200', '422']` ↔ `['200']`(설치판 `openapi/utils.py` 457~470행 — 매개변수·요청 본문이 있을 때만 422) · 요청 상태 코드는 같음(머리 없음 `401 | 401` — 본문 글만 다름, 교재용 접근 토큰 `200 | 200`). 결론 = 상태 코드는 같아도 응답 문서가 달라짐, 실습 앱은 실행 1 모양이라 생성 SDK도 접근 토큰을 요청마다 인자로 받음. 빨강 0(받은 오류도 없음).
- **말(handoff §07 → §08 7)**: 새 용어 **2**(meta 「새 용어 2」): **응답 문서(OpenAPI 문서)**(05 b7·07이 먼저 쓴 말 — 첫 풀이: 뜻 → 축소 모형 예 → `app.openapi()`·`openapi.json`) · **생성 SDK**(뜻 → 공장이 모형만 보고 칸을 만드는 예 → `client/generated/` 파일 열여덟 — TS 파일 열하나와 설명 문서 `docs/*.md` 일곱, 마감 검토 B-2로 본문 「TS 파일 열여덟」을 바로잡음). 제목의 「OpenAPI」·「TS」(TypeScript)·「SDK」(Software Development Kit)는 1절·b2 첫 자리에서 풂. 풀이로만: 키 `$ref`·칸 `operationId`·생성기·인자 `dependencies`·보안 방식 칸·연산자 `is`·`json.load`·`strip`·`rstrip`·`split`·`Promise`·`void`. 「스키마」 → 입력 형식·응답 형식·형식(`schemas`·`itemSchema`·`model_json_schema`는 코드) · 「경로」·「엔드포인트」 → 요청 주소 · 「인터페이스」 → TS 선언 `interface` · 「캐시」 → 담아 둠 · 「스트림 함수」 → SSE 사건으로 답하는 요청 주소의 함수. handoff 용어 표·대체어·meta 줄에 덧붙임.
- **b4 비유**: 「건축 도면」 → 챕터 계열 「화물 열차와 번호판 차량」의 「편성도」를 **축소 모형**으로(모형 칸 다섯 = 요청 주소 다섯, 단색 셋/줄무늬 둘 = `schema`/`itemSchema`, 공장 = 생성기, 실제 칸 = 생성 SDK 함수, 바닥만 있는 칸 = `Promise<void>`) · 비유와 다른 점(문서는 앱 객체가 코드에서 만듦 · 생성기가 줄무늬를 모른다는 것은 노트북 밖 경고로만 · 노트북에서 생성기 실행 안 함).
- 노트북: 제목 셀(할 일 셋·준비물·기준 버전·강의와 실습 범위) · 오늘 볼 그림(08-1 첨부) · 1 준비(설치 여섯·가져오기·파일 위치 셀·앱 가져오기 — **도구 파일 가져오지 않음**) · 2 응답 문서 · 3 파일과 견주기 · 4 생성 SDK · 5 실험(가설 → 실행 1 → 실행 2 → 요청 → 결과 표 → 결론) · 정리 세 줄 + 09 예고. 파일 위치 셀은 01절 셀 글 그대로(`author_06.FIND_LAB` → `__main__`에서 `author_01.py`와 문자열 대조 `assert`). 설치 셀은 07과 같은 여섯(잠금 판). 키 셀 없음.
- 본문 b1~b10 새로(b3 = 01절 입력 형식·응답 형식 + Ch 19 02 `model_json_schema()` + 05절 SSE 본문 종류 + 06절 `stream.ts`·`fetch` + 07절 `HTTPBearer` 보안 방식 칸·실습 앱은 없음 / b10 = FastAPI First Steps·Generating SDKs·Dependencies in path operation decorators·OpenAPI Generator typescript-fetch·OpenAPI Generator CLI(다섯 모두 2026-09-29 WebFetch) + 설치판 fastapi `applications.py`·`openapi/utils.py`·`utils.py` 행 + 실습 폴더 파일 행). 복습 넷 → **다섯**(해설 포함). meta 「강의 0.75h | 실습 2h」 그대로(챕터 시수 합 유지).
- 옛 `{{svg:08-흐름}}` 토큰 제거, 옛 그림 파일 셋(`08-흐름.svg·.excalidraw·.caption.md`)은 그대로.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-08/exp/`)

- `p1_scene.py`(설계용 탐색): 위 2~5절 값 전부 + 덧붙여 본 값(`sort_keys=True` 정렬 직렬화 `d2fb94f6…` 4825자 · 기본 `ensure_ascii` 길이 4885 = 옛 판 값 · 두 실행 문서 정렬 직렬화 다름 `False`).
- `p3_stale.py`: 문서를 만든 뒤 데코레이터 줄로 요청 주소를 더하면 `app.openapi()`의 `paths`에 없음(`['/one']`, 라우트는 둘) — b7에 「노트북 밖에서 한 번 확인」.
- `p4_schema.py`: `ChatRequest.model_json_schema() == components['ChatRequest']` `True`·`ChatResponse`도 `True`(키 차례만 다름).
- **`p5_nb.py`(노트북 코드 셀 21개를 이은 파일, `sys.path`에 `''` — IPython 커널처럼) 5번: 출력 md5 5/5 같음(`312e2d3633591efef30490851c1964af`), 표준 오류 0**, 실습 폴더 새 파일 0.
- 공식 문서(2026-09-29 WebFetch): FastAPI First Steps(OpenAPI = API의 요청 주소·매개변수·주고받는 자료를 적는 규격, `/openapi.json`, 클라이언트 코드 생성) · FastAPI Generating SDKs(`operationId` = 함수 이름·요청 주소·요청 방식, 예 `createItemItemsPost`·OpenAPI Generator·Hey API, 백엔드를 바꾸면 다시 생성) · FastAPI Dependencies in path operation decorators(`dependencies` = `Depends()` 목록, 값은 안 쓰지만 실행·오류로 멈춤) · OpenAPI Generator typescript-fetch(Fetch API TS 코드, BearerToken 지원, `modelPropertyNaming` 기본 camelCase, OpenAPI 3.1·SSE 언급 없음) · OpenAPI Generator CLI README(JDK 11 최소, `openapitools.json`에 판).
- 설치판 소스 행(본문에 적은 것): fastapi 0.135.0 `applications.py` 1069(`openapi`)·1083~1084(없을 때만 만듦)·1117(`include_in_schema=False`) · `openapi/utils.py` 289~296(`security`)·457~470(422)·573~575(`securitySchemes`) · `utils.py` 95~100(`generate_unique_id`) · 실습 `app.py` 17행.

## 생성기·`tsc` 시험 (노트북 밖, `/tmp/ch30-08/sdk`)

- 디스크: 시작 루트 여유 **1,789,706,240 B**(1.7G) · npm 정보만 본 뒤 결정(의존 17개 + jar 32MB 어림 — 수백 MB 아래) · npm 캐시는 `npm_config_cache=/tmp/ch30-08/npm-cache`.
- `npx -y @openapitools/openapi-generator-cli version`(2.41.0) → jar **7.25.0** 받음(10:32:44Z~50Z) · 입력은 실습 폴더 `openapi.json`·`openapitools.json` 사본(해시 `06e5d1b9…`·`108e89e1…`, 사본의 `openapitools.json`은 실행 뒤에도 같음).
- README 명령 그대로(`generate --skip-validate-spec -i openapi.json -g typescript-fetch -o generated-sdk`, OpenJDK 11.0.32.1): 종료 0 · 경고 `attribute paths.'/v1/chat/live/stream'(post).responses.200.content.'text/event-stream'.itemSchema is unexpected`와 `/v1/chat/stream` 같은 줄 · 「OpenAPI 3.1 support is still in beta」 경고. **빈 폴더 첫 생성은 `.openapi-generator/FILES`에 `.openapi-generator-ignore` 한 줄 더(19줄)**, **같은 폴더에 두 번째 생성 → 실습 폴더 `client/generated/`와 `diff -r` 같음(21개 모두)** — 지금 생성 SDK는 지금 `openapi.json`과 생성기 7.25.0으로 다시 만든 글과 같음.
- 실행 1·2 문서(`/tmp/ch30-08/sdk/run1.json`·`run2.json`)로 한 번씩 생성: 실행 1 함수 `healthV1PingGet(requestParameters)`에 `authorization?: string | null` · 실행 2 함수 `healthV1PingGet(initOverrides?)`에 인자 없음, `this.configuration.accessToken` → `headerParameters["Authorization"] = \`Bearer ${tokenString}\`` — b6에 「노트북 밖에서 한 번, 생성기 7.25.0」으로 한정해 적음.
- `npx -y --package typescript@latest tsc --version` → **7.0.2** · README 검사 명령(`--noEmit --target ES2022 --moduleResolution bundler --module ESNext --allowImportingTsExtensions client/generated/index.ts client/stream.ts client/test_stream.ts`, `client/` 사본) → **종료 0·출력 없음**(10:33:17Z~19Z). 판 고정 없음은 README·마감 몫(기록만).
- `node`(v22.23.2)로 `client/generated/index.ts`를 바로 import → `ERR_MODULE_NOT_FOUND`(확장자 없는 `'../runtime'`) — b7에 적음. `tsx`는 실행하지 않음.
- 끝 루트 여유 **1,578,618,880 B**(1.47G) — 줄어든 약 211MB는 `/tmp/ch30-08`(201MB, 그 가운데 npm 캐시 191MB·삽화 원본 9MB) 등. 남은 java·node 프로세스 0.

## 실행 (새 커널)

| 실행 | 자리 | 키 | 결과 |
|---|---|---|---|
| 시험 tryA(`/tmp/ch30-08/tryA` 사본, `execute.py` 기본 `--cwd` = 프로젝트 맨 위, `PYTHONPATH` = `notebooks/`, 10:49:28Z) | 루트 커널 | `OPENAI_API_KEY` 지움 | PASS 22셀 |
| 시험 tryB(사본, `--cwd` 실습 폴더 `notebooks/`, `PYTHONPATH` 지움, 10:49:37Z) | 학생 커널 | 지움 | PASS 22셀, tryA와 셀별 22/22 같음 |
| **A**(`run_section.sh … 08`, `executed_at` 2026-09-29T10:49:45.977429Z) | 루트 커널 | 지움 | PASS 22셀(그림 첨부 단계에서 멈춤 — 08-1 PNG 전) |
| **B**(A 사본 `/tmp/ch30-08/B`, `execute.py --cwd notebooks/`, `PYTHONPATH` 지움, 10:49:56Z) | 학생 커널 | 지움 | PASS 22셀 |

- **A ↔ B 셀별 출력 글자 22/22 같음**(이은 글 해시 `9aba2b6a7cdffe1e` 같음), `code_sha256` `eddd600d09d66bd083137169d4dfa874017bd318d77192f55457d0b80be7c2d0` 같음. **`outputs_sha256`은 다름**(A `3ac7d06e34cb59a8210a3fabc20679f095cb7f9b59545707e14f9239fc3dea51` = tryA · B `205265b0bb538fdc67c0c37bbca26b3ff846f3e3ff010c121cff826d14f19e5b` = tryB) — 까닭: 설치 셀 [1]의 표준 출력 스트림이 B는 66 + 100글자 둘로 나뉨, A는 166글자 하나(합친 글은 같음 — 02·03·05·06·07 선례). 요청 0이라 셀 [2]~[22] 출력은 구조까지 같음. 초·ID·포트·임시 위치를 출력하는 셀 없음.
- 그 뒤 `--no-exec` 셋(렌더·첨부·빌드)·`--src-only` 셋·`mdpatch.py` 한 번(4절 앞 설명 한 문장 「Java로 돌아서」 → 「Java 프로그램이라서」 — 마크다운만)에서 노트북 코드·출력·`executed_at` 그대로(A 사본과 `cmpout` 22/22·`outputs_sha256` 같음) · 생성기 `cells()`와 저장 노트북의 마크다운 25·코드 22 셀 글 모두 같음(대조) — 노트북 파일 **`767cdff1a91168d100d8612be63be2ac1a2177dcfcad246af8ac970448e3b55a`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에 새로 생기거나 바뀐 파일은 노트북 08뿐(`find -newer` — `openapi.json`·`__pycache__` 그대로, pyc 0) · `.failure.json` 0 · 노트북 표준 오류 출력 0·`Traceback` 0·`/var/folders` 0 · 설치 셀 출력에 pip 안내 한 줄.
- **모델 요청 0** · 서버 프로그램·포트·자식 프로세스·브라우저·node 0(노트북 안) · 남은 프로세스 0(`ps` — uvicorn·node·java·ipykernel·jupyter 없음).

## 앱 파일 · `app.openapi()` 대조 · `tests/`

- **08은 앱 파일·`openapi.json`·생성 SDK·`client/*.ts`를 고치지 않음.** 실험은 노트북의 새 앱 객체 둘(실습 앱의 `health`·`require_token`을 가져와 이음).
- 확인: `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 `True` · 정렬 직렬화 `d2fb94f6…`(4825자) · `pytest -q -p no:cacheprovider` **6 passed, 1 warning** · 앱 파일 해시 `app.py` `3455d405…`·`agent.py` `a6c42e63…`·`live_agent.py` `586a6a69…`·`schemas.py` `ed77b197…`·`__init__.py` `1c7d7aef…`·`tests/test_app.py` `f8611741…` 그대로.

## 도구 파일 — 바꾸지 않음(가져오지도 않음)

- 이 절은 앞 절에서 배운 함수(`zero_timeout`·`split_sse` 등, 07 `header_or_none`)를 쓰지 않아 `serve_tools.py`를 가져오지 않음 — 06 판 `e1a1464d0f647e0b2ca99fd14338eeb22c596effd405b5acf2ee49ac1d2c704d` 그대로. 생성기 `__main__`: `author_06.check_tools06()`(06 판 대조 사슬 통과) + 디스크 파일 = `author_06.TOOLS06` `assert` — 쓰는 줄 없음. 04·06·07 노트북 영향 없음(파일 그대로). 공개 목록 두 곳 그대로.
- 07 `header_or_none`은 08이 쓰지 않아 옮기지 않음 · 08이 처음 쓴 `print_lines_with(text_lines, word)`는 08 노트북에 둠(09가 다시 쓰면 09가 옮김).

## 고친 틀린 사실

- **b8 「Ch31에서는 이벤트를 데이터베이스에 저장해 프로세스 재시작 뒤에도 복구합니다」(거짓)** → 빼고 「09절에서는 실제로 모델을 부르는 에이전트를 요청 주소 `/v1/chat/live`로 부릅니다」(08 주제와 무관해 Ch 31 문장은 두지 않음 — 06 b7이 Ch 31 사실을 이미 적음).
- b3 「07절의 인증을 한 문서로 모아」 → 「07절에서는 `HTTPBearer`를 쓴 새 앱의 응답 문서에만 보안 방식 칸이 있었습니다. 실습 앱은 접근 토큰을 요청 머리 매개변수 `authorization`으로 받아, 보안 방식 칸이 없었습니다」 + 실험으로 까닭을 보임.
- b6 「같은 앱 객체의 두 직렬화 결과는 같았습니다」(실험 아님) → 2절 「같은 객체」 한 셀 + 5절 의존성 하나를 바꾼 실험.
- 「TypeScript 타입이 빌드 오류를 줄이지만」·「CI에서 검사」·「operationId를 명시적으로 관리」·「생성물 컴파일은 … 증거」 → 뺌 · `tsc`·생성은 「노트북 밖에서 실행한 결과」로 b7에 한정 · 「SSE는 생성 지원이 제한적」 → 생성 SDK 함수 `Promise<void>`·`VoidApiResponse` 출력 + 노트북 밖 생성기 경고.
- 저장 출력의 사용자 폴더 위치(`path.resolve()`) → 0.

## 그림

- Mermaid 넷: 설계표 `08-figures.md`(렌더 전 작성) → `.mmd`·캡션 → 렌더 → PNG 넷을 직접 열어 확인(stage 사본): 첫 렌더에서 08-2 아래 상자 라벨 하나가 저절로 줄바꿈(끊김 아님) → `<br>`로 미리 나눠 다시 렌더 → 08-1(`flowchart TB` 한 줄 여섯, viewBox 폭 **244**) · 08-2(위 하나 → 넷 → 아래 하나, 폭 **814**) · 08-3(위 둘 → 생성기 → 아래 둘 + 점선 갈래, 폭 **530**) · 08-4(공통 상자 + 칸 둘 + 공통 상자, 폭 **631**) — 모두 868 이하, 끊긴 라벨 0, 색은 설계표대로(초록 실습 앱·파일·`require_token`·`client/stream.ts` / 파랑 새 앱 객체·바꾼 값 보안 객체 / 노랑 출력 / 회색 FastAPI가 적는 일·생성기(노트북 밖)·두 실행 공통 상태 코드 / **보라 0·빨강 0**). 라벨 숫자는 출력에 있는 `3.1.0`·`7.25.0`·200·422·401·500뿐(소스·TS 줄 번호는 라벨에 안 씀).
- 삽화 08-5: **1차 job `ee589176-cd27-4481-8d0e-a5ddede7df50` 채택(재생성 0)** · 거래 2026-09-29T10:52:17.842524Z 「Nano Banana Pro −2」(**이 절 몫 2크레딧**, 잔액 2275 → 2273, 앞 거래 10:15:02Z는 Ch 30 07) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 원본 `311b5a7c…`(2752 × 1536) → 저장 PNG `eca09ae9b8d5793697226a76a59602b12f47263d097f02666d437b569f45c631`(1100 × 614) · 결과를 다시 받아 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0 · 저장본과 같은 보기 사본·원본 위·아래 절반 확대를 열어 모형 칸 **다섯**(올리브색 셋·흰·회색 빗금 둘)·실제 칸 **다섯** 같은 차례(올리브색 덮개 칸 셋·바닥과 바퀴만 있는 빈 칸 둘)·기관차·사람·글자·숫자·화살표 없음을 세고 그림 읽기를 씀. **거의 흰 가로줄 21 / 614**(07 109). 설계와 다른 점: 모형 칸은 닫힌 상자 모양(실제 칸과 모양 다름 — 색·차례·개수로 짝) · 빈 칸 바닥은 크림색(값과 짝짓지 않음). 01~07 소품 되풀이 없음.

## 검사

- `run_section.sh … 08 --no-exec`(마지막): 렌더(도장이 같아 다시 그리지 않음) · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 191 code cells (max 14 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `08-OpenAPI와-TS-SDK.html`(`4318e86e…`): `{{` **0** · `[[` 0 · 인라인 SVG 4 · 삽화 JPEG 1.
- `pack.py … 08` → `qa/upgrade/review-pack/08-OpenAPI와-TS-SDK.md`(`4b2e5b20…`).
- 보호 파일 255개: `manifest-changes.md` 「08절 뒤」에 덧붙임(같음 220·바뀜 35 = 01~07 기록 값 29 + 08 작업 6·없어짐 0).

## 완료 챕터·뒤 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

`grep -rn 'Ch *30' textbook/part1 part2 part5 part6 part7 --include=*.html | grep -v ch30-fastapi` + `OpenAPI`·`openapi`·`SDK`로 Part 7 챕터 밖 검색:

| 문장 | 판정 |
|---|---|
| Ch 1 01 과정 지도(Part 7 · Ch 30~34) · Ch 2 11 b8(2절)·12 b8(1·3절)·Ch 2 `index.html` · Ch 29 05 b8(01) · Part 7 소개 「Ch30의 요청·응답 형식에서 시작해 …」 | 08과 무관 — 참 |
| Ch 31 01 b2·b3 「Ch30에서 FastAPI 요청 함수/경로 함수를 비동기로」 · Ch 32 01·02 「Ch30의 서비스」 · Ch 34 04 b3 「Ch 30에서는 FastAPI 비동기 요청 처리」 | 글만(대기 챕터, 고치지 않음) — 08과 무관 |
| Ch 34 04 b7 「SDK의 내장 재시도 정책」 | 모델 제공자 SDK 뜻 — 08 「생성 SDK」와 다른 뜻(대기 챕터, 기록만) |

- 완료·대기 챕터에서 Ch 30 08(OpenAPI·생성 SDK)을 가리키는 문장 없음(Part 7 목차의 절 제목만).
- 같은 챕터 07 b8 「파일로 쓰고」 → 대체로 참(위 「바꾼 것」 첫 줄) · 05 b7 「응답 문서(OpenAPI)는 08절에서 자세히 봅니다」 → 참 · 07 노트북 6절 「응답 문서는 앱 객체가 요청 주소와 입력 형식을 모아 적은 문서이고, 08절에서 자세히 봅니다」 → 참.

## 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀 — `0c0bedac…`) · 사용자 디스크 `.cache/ch30-08-view/`(삽화 보기 사본 셋 — 새로 만든 폴더). 공용 도구·규격·과정 문서·zip·검사 스크립트·앱 파일·TS 파일·생성 SDK·`openapi.json`·도구 파일·공개 목록·Ch 31 이후 파일은 고치지 않음.

## 강사 확인 대상

1. 07 b8 「응답 문서를 파일로 쓰고」와 달리 08은 `openapi.json`을 쓰지 않고 글만 견준 것(handoff 권고) — 07 b8을 「파일과 견주고」로 고칠지(마감 또는 강사).
2. 새 말 「응답 문서」(05·07이 먼저 쓴 이름을 이어 씀 — 요청 모양도 적는 문서라 「API 설명 문서」 같은 이름이 나을 수 있음)·「생성 SDK」 · 제목 「OpenAPI와 TS SDK」 그대로(본문 첫 자리 풀이).
3. 실험 변수를 「인증을 적는 자리(인자 `dependencies`의 제공 함수 ↔ 보안 객체)」로 고른 것과, 그 앱을 실습 앱이 아니라 노트북의 새 앱 객체 둘로 만든 것(실습 앱을 바꾸면 `openapi.json`·생성 SDK·TS 시험이 바뀜).
4. 노트북 밖에서만 본 사실(생성기 재생성 = 생성 SDK 같음·`tsc` 7.0.2 통과·실행 2 문서의 `accessToken`·`ERR_MODULE_NOT_FOUND`·문서를 만든 뒤 이은 요청 주소가 빠짐)을 본문 b6·b7에 「노트북 밖에서 한 번」·「이 노트북에서는 실행하지 않았습니다」로 적은 것.
5. README `npx --package typescript@latest tsc`의 판 고정 없음(지금 7.0.2)과 `openapi-generator-cli` 판 고정 없음(지금 2.41.0 — jar는 `openapitools.json` 7.25.0으로 고정) — README 고침은 마감 몫.
6. 삽화의 모형 칸 모양이 실제 칸과 다른데 재생성하지 않은 것(색·차례·개수로 짝이 읽힘).

## 남은 것 (마감 몫)

- `part7-practice.zip`에 08 노트북 새 판 반영(마감 때 한 번) · 08은 Part 7 묶음 실행 검사 대상 아님(01만).
- 옛 그림 `08-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-08-08.json` · 기기 `/tmp/ch30-08/`(약 201MB — npm 캐시 `npm-cache/` 191MB(생성기 jar 32MB·typescript 7.0.2 포함)·생성 결과 `sdk/`(생성 SDK 넷·로그)·삽화 원본 둘 `illu/`·사본 넷·실험 스크립트·도구 복사본·`handoff.before.md`) · 사용자 디스크 `.cache/ch30-08-view/`(보기 사본 셋, 1.6MB).
