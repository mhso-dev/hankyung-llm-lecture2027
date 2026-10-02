# Ch30 실행 검증

> **맨 위 「실제 결과」~「최종 경로 재검증」은 개선 전 판(2026-09-11)의 기록입니다.** 품질 개선 기록은 아래 「품질 개선 NN절」과 끝 「마감」 절, 챕터 요약 `qa/upgrade/chapter-summary.md`에 있습니다.

- 실행일: 2026-09-11
- 환경: Python 3.12.13, FastAPI 0.135.0, LangChain 1.4.0, LangGraph 1.2.11, OpenAPI Generator 7.25.0, Node 25.9.0

## 실제 결과

- 01절: 정상 본문은 200, 빈 문자열은 Pydantic 최소 길이 제약으로 422였습니다.
- 02절: 의존성 대체 중에는 `대체 응답`, 해제 뒤에는 실제 LangGraph 답을 받았습니다.
- 03절: 실제 `ainvoke` 결과에 messages와 answer가 있었고 교육용 오류 조건은 RuntimeError를 냈습니다.
- 04절: 실제 `astream(stream_mode="custom")` 조각을 결합해 최종 문장을 복원했습니다.
- 05절: POST SSE의 첫 이벤트는 token과 `sse-1:0`, 마지막 이벤트는 done이었습니다.
- 06절: `resume-1:0`을 Last-Event-ID로 보낸 뒤 첫 재개 ID는 `resume-1:1`이었습니다. 스트림 오류는 HTTP 200 안의 error 이벤트로 받았습니다.
- 07절: 인증 누락 401, 미허용 출처의 CORS 헤더 누락, 지연 Agent의 단일 응답 504와 스트림 error 이벤트를 확인했습니다.
- 08절: OpenAPI의 `/v1/chat` 요청과 응답이 ChatRequest와 ChatResponse를 참조했습니다.
- 09절: 실제 OpenAI Agent가 `lookup_library_hours`를 `day=월요일`로 호출했고 ToolMessage는 `09:00~18:00`이었습니다. JSON과 모델 token SSE를 결합한 답 모두 18:00을 포함했습니다.

## 자동 검증

- `execute.py`: 9개 노트북, 코드 셀 45개, 최대 14줄 통과.
- `verify.py --chapter`: 9개 절, 코드 셀 45개 통과.
- `pytest -q`: 6 passed. Starlette TestClient 내부의 anyio 별칭 DeprecationWarning 1건이 있습니다.
- OpenAPI Generator 7.25.0: SSE `itemSchema` 검증 경고 뒤 TypeScript fetch SDK 생성 완료.
- TypeScript `tsc --noEmit`: 생성 SDK, `stream.ts`, `test_stream.ts` 통과.
- 실제 TS fetch 클라이언트: normal 이벤트 token 5회 뒤 done, 첫 ID `web-01:0`, 재개 첫 ID `web-01:1`, 오류 요청 error 이벤트 확인.
- 화면: 1280px·390px의 10개 페이지에서 작은 글자, 대비, 잘림, 화면 밖 요소, SVG 경계, 가로 스크롤, 깨진 이미지, 복사 오류가 모두 0입니다.
- 도식: SVG·Excalidraw 9쌍을 동일 명세에서 생성했습니다.

## 해석 제한과 확인 필요 항목

OpenAPI Generator는 FastAPI 네이티브 SSE의 `itemSchema`를 아직 표준 속성으로 인정하지 않아 `--skip-validate-spec`가 필요했습니다. 생성된 일반 JSON SDK는 컴파일했으며 SSE 재연결은 직접 작성한 fetch 클라이언트로 실행했습니다. 실제 클라우드 프록시, 장시간 연결, 공급자 장애, 여러 인스턴스 사이 이벤트 재생은 확인하지 않았습니다. 한국어 최종 감사는 별도 모델이 완료했으며 Part 7 통합 검증 기록에서 판정을 확인할 수 있습니다. 실제 API 호출 비용은 1달러 미만으로 예상하며 키 값은 출력하지 않았습니다.

## 최종 경로 재검증

준비 셀은 현재·상위 폴더에서 `agent_service`가 있는 챕터를 찾고 작업 폴더를 설정합니다. 노트북 폴더에서 9개 모두 실제 새 커널로 다시 실행했으며 API 호출을 포함합니다. 최종 ZIP의 01절도 추출된 노트북 폴더에서 실행했습니다. 감사 완료 본문은 유지했습니다.

## 품질 개선 01절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/01-diagnosis.md`에 있습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T06:32:54Z) · B(사본, `notebooks/` 커널, 06:33:07Z) — PASS 22셀, 셀별 출력 22/22 같음, `code_sha256` `861cacdb…`·`outputs_sha256` `87ea510f…` 둘 다 같음. 두 실행 모두 `OPENAI_API_KEY`를 지운 환경.
- 키 없는 묶음 모양 실행(`part7-practice/labs/part7/ch30-fastapi-serving/` 모양 — `schemas.py`와 노트북만, `.env` 닿지 않음, `PYTHONPATH` 없음): PASS 22셀, 셀별 22/22 같음.
- 모델 요청 0 · 서버 프로그램·포트·자식 프로세스 0 · 실습 폴더에 새로 생긴 파일 0(노트북 01 말고) · pyc 0.
- 게이트 G1~G7 0(`gates-wip-01.json`) · `verify.py --chapter` PASS 9 sections / 62 code cells · 빌드 HTML `{{` 0.
- Before `body: dict` 빈 질문 → 200·몸통에 들어온 값 `['']` ↔ After `body: ChatRequest` → 422 `string_too_short`·몸통에 들어온 값 `[]`.
- 실습 폴더 `pytest -q -p no:cacheprovider`: 6 passed, 1 warning(앱 파일 그대로). `app.openapi()` 직렬화 = `openapi.json`(`06e5d1b9…`) 바이트 같음.

## 품질 개선 02절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/02-diagnosis.md`에 있습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T07:10:35Z) · B(사본, `notebooks/` 커널, 07:10:45Z) — PASS 24셀, 셀별 출력 글자 24/24 같음, `code_sha256` `c52cc10f…` 같음. `outputs_sha256`은 A `2003205a…` · B `83a49271…`로 다름(설치 셀 출력이 B에서 스트림 둘로 나뉘어 저장 — 글자는 같음). 시험 실행 둘(`/tmp` 사본, 같은 두 자리)은 `outputs_sha256`까지 같았음. 모든 실행 `OPENAI_API_KEY`를 지운 환경.
- 노트북 밖 같은 장면(`/tmp/ch30-02/exp/p1_scene.py`) 5번 출력 md5 모두 같음.
- 모델 요청 0 · 서버 프로그램·포트·자식 프로세스 0 · 실습 폴더에 새로 생긴 파일 0(노트북 02 말고, 앱을 가져와도 pyc 0) · 표준 오류 출력 0.
- 게이트 G1~G7 0(`gates-wip-02.json`) · `verify.py --chapter` PASS 9 sections / 81 code cells · 빌드 HTML `{{` 0 · 인라인 SVG 5 · 삽화 1.
- Before 재정의(`get_timeout` → `zero_timeout`) 첫 테스트 504 → 다음 테스트(새 `TestClient`) 504·키 수 1 ↔ After `clear()` → 키 수 0·200.
- 실습 폴더 앱 파일 고침 0 — `pytest -q -p no:cacheprovider`: 6 passed, 1 warning · `app.openapi()` 직렬화 = `openapi.json`(`06e5d1b9…`) 바이트 같음.

## 품질 개선 03절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/03-diagnosis.md`에 있습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T07:42:43Z) · B(사본, `notebooks/` 커널, 07:42:53Z) — PASS 22셀, 셀별 출력 글자 22/22 같음, `code_sha256` `eb33867b…` 같음. `outputs_sha256`은 A `5d7bc81a…` · B `7510b28b…`로 다름(설치 셀 출력이 두 스트림으로 나뉜 자리만 다름 — 글자는 같음). 시험 실행 둘(`/tmp` 사본, 같은 두 자리)도 셀별 22/22 같음. 모든 실행 `OPENAI_API_KEY`를 지운 환경.
- 노트북 밖 같은 장면(`/tmp/ch30-03/exp/p3_scene.py`, await 자리는 `asyncio.run`) 5번 출력 md5 모두 같음.
- 모델 요청 0 · 서버 프로그램·포트·자식 프로세스 0 · 실습 폴더에 새로 생긴 파일 0(노트북 03 말고, 앱을 가져와도 pyc 0) · 표준 오류 출력 0 · 남은 프로세스 0.
- 게이트 G1~G7 0(`gates-wip-03.json`) · `verify.py --chapter` PASS 9 sections / 98 code cells · 빌드 HTML `{{` 0 · 인라인 SVG 5 · 삽화 1.
- Before 동기 `invoke` → `TypeError`(글 두 줄) · 동기 `stream` → 같은 오류 ↔ After `ainvoke` 부르기만 → `coroutine` → `await` → `dict`·칸 `['messages', 'answer']`·2절 HTTP 답과 같음 `True`.
- 실습 폴더 앱 파일 고침 0 — `pytest -q -p no:cacheprovider`: 6 passed, 1 warning · `app.openapi()` 직렬화 = `openapi.json`(`06e5d1b9…`) 바이트 같음.

## 품질 개선 04절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/04-diagnosis.md`에 있습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T08:16:51Z) · B(사본, `notebooks/` 커널, 08:17:02Z) — PASS 23셀, 셀별 출력 23/23 같음, `code_sha256` `2b5a740d…`·`outputs_sha256` `e7a37a53…` 모두 같음. 시험 실행 둘(`/tmp` 사본, 같은 두 자리)도 셀별 23/23 같음. 모든 실행 `OPENAI_API_KEY`를 지운 환경.
- 노트북 밖 같은 장면(`/tmp/ch30-04/exp/p3_scene.py`, 셀 맨 위 await·async for 자리는 `asyncio.run`) 5번 출력 md5 모두 같음(`1a5a0d72…`).
- 모델 요청 0 · 서버 프로그램·포트·자식 프로세스 0 · 실습 폴더에 새로 생긴 파일은 노트북 04와 도구 파일 `notebooks/serve_tools.py`(`e0a3a382…`)뿐(앱·도구 파일을 가져와도 pyc 0) · 표준 오류 출력 0 · 남은 프로세스 0.
- 게이트 G1~G7 0(`gates-wip-04.json`) · `verify.py --chapter` PASS 9 sections / 117 code cells · 빌드 HTML `{{` 0 · 인라인 SVG 4 · 삽화 1.
- 실행 1 모드 `custom` → 사건 6(모두 `dict`) ↔ 실행 2 모드 목록 `custom`·`updates` → 사건 7(모두 짝), `custom` 자리 `[1, 2, 3, 4, 5, 6]`·`updates` 자리 `[7]`, 진행 값만 이어 붙인 글 같음 `True`.
- 실습 폴더 앱 파일 고침 0 — `pytest -q -p no:cacheprovider`: 6 passed, 1 warning · `app.openapi()` 직렬화 = `openapi.json`(`06e5d1b9…`) 바이트 같음.

## 품질 개선 05절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/05-diagnosis.md`에 있습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T08:53:39Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 지움, 08:53:58Z) — PASS 25셀, 셀별 출력 글자 25/25 같음(이은 글 해시 `653b3cae…`), `code_sha256` `662e8a3e…` 같음, `outputs_sha256`은 설치 셀 스트림이 두 커널에서 다른 자리로 나뉘어 다름(A `85e481f7…` · B `b85bad74…` — 02·03 선례). 시험 실행 둘(`/tmp` 사본, 같은 두 자리)은 `outputs_sha256`까지 A와 같음. 모든 실행 `OPENAI_API_KEY`를 지운 환경.
- 노트북 밖 같은 장면(`/tmp/ch30-05/exp/p3_scene.py`, 셀 맨 위 async for 자리는 `asyncio.run`) 5번 출력 md5 모두 같음(`8e59350e…`), 표준 오류 0.
- 모델 요청 0 · 서버 프로그램·포트·자식 프로세스 0 · 실습 폴더에 새로 생긴 파일은 노트북 05뿐(pyc 0) · 노트북 표준 오류 출력 0 · 남은 프로세스 0.
- 게이트 G1~G7 0(`gates-wip-05.json`) · `verify.py --chapter` PASS 9 sections / 138 code cells · 빌드 HTML `{{` 0 · 인라인 SVG 4 · 삽화 1.
- 실행 1 `response_class=EventSourceResponse` → `text/event-stream; charset=utf-8`·SSE 사건 7·`event:` 줄 7·앱 응답 본문과 같음 `True` ↔ 실행 2 인자만 뺌 → `application/jsonl`·JSON 줄 7·`event:` 줄 0·응답 머리 1.
- 실습 폴더 앱 파일 고침 0 — `pytest -q -p no:cacheprovider`: 6 passed, 1 warning · `app.openapi()` 직렬화 = `openapi.json`(`06e5d1b9…`) 바이트 같음 · 도구 파일 `serve_tools.py` 그대로(`e0a3a382…`).

## 품질 개선 06절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/06-diagnosis.md`에 있습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T09:32:33Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 지움, 09:32:44Z) — PASS 26셀, 셀별 출력 글자 26/26 같음(이은 글 해시 `8d0059bb…`), `code_sha256` `21a623d1…` 같음, `outputs_sha256`은 A의 설치 셀 스트림이 둘로 나뉘어 다름(A `e1b573c1…` · B `08fa05f6…` — 02·03·05 선례). 시험 실행 둘(`/tmp` 사본, 같은 두 자리)은 `outputs_sha256`까지 B와 같음. 모든 실행 `OPENAI_API_KEY`를 지운 환경.
- 노트북 밖 같은 장면(`/tmp/ch30-06/exp/p1_scene.py`, 셀 맨 위 await 자리는 `asyncio.run`) 5번 출력 md5 모두 같음(`438a7bf7…`), 표준 오류 0(기록기 수준을 올리지 않으면 25줄).
- 모델 요청 0 · 노트북 안 서버 프로그램·포트·자식 프로세스 0 · 실습 폴더에서 바뀐 파일은 노트북 06·도구 파일뿐(pyc 0) · 노트북 표준 오류 출력 0 · 남은 프로세스 0.
- 게이트 G1~G7 0(`gates-wip-06.json`) · `verify.py --chapter` PASS 9 sections / 159 code cells · 빌드 HTML `{{` 0 · 인라인 SVG 4 · 삽화 1.
- Before 시간 제한 0초 → `상태 코드: 200`·사건 `['error']`·token 0 → 상태 코드만 본 판정 `True` ↔ After 마지막 사건이 `done`인가 `False`(첫 응답은 둘 다 `True`) · 값 바꿔 보기 `sse-1:99` → `['done']`·After `True` · 이어 받기 `sse-1:1` → `sse-1:2`부터·이어 붙인 글 같음 `True` ↔ 요청 머리 없이 `False`.
- 실습 폴더 앱 파일 고침 0 — `pytest -q -p no:cacheprovider`: 6 passed, 1 warning · `app.openapi()` 직렬화 = `openapi.json`(`06e5d1b9…`) 바이트 같음 · 도구 파일 `serve_tools.py` 04 판 `e0a3a382…` → 06 판 `e1a1464d…`(함수 넷 덧붙임) — 04 노트북 사본을 06 판으로 다시 실행해 23/23·`outputs_sha256` 같음.
- TS 시험(노트북 밖): uvicorn `127.0.0.1:8000` + Node v22.23.2 `node client/test_stream.ts` → 종료 코드 0·`{"normal":[…5 token…,"done"],"firstId":"web-01:0","resumedFirstId":"web-01:1","failed":["error"]}` · uvicorn −15 · 포트 다시 빔 · 남은 프로세스 0.

## 품질 개선 07절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/07-diagnosis.md`에 있습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T10:12:30Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 지움, 10:12:39Z) — PASS 21셀, 셀별 출력 글자 21/21 같음(이은 글 해시 `a796947c…`), `code_sha256` `e9a38985…` 같음, `outputs_sha256`은 A의 설치 셀 스트림이 둘로 나뉘어 다름(A `ff1e1ec6…` · B `1a61016d…` — 02·03·05·06 선례). 시험 실행 둘(`/tmp` 사본, 같은 두 자리)도 셀별 21/21 같음. 모든 실행 `OPENAI_API_KEY`를 지운 환경.
- 노트북 밖 같은 장면(`/tmp/ch30-07/exp/p1_scene.py`) 5번 출력 md5 모두 같음(`6c2a30e8…`), 표준 오류 0.
- 모델 요청 0 · 서버 프로그램·포트·자식 프로세스·브라우저 0 · 실습 폴더에서 바뀐 파일은 노트북 07뿐(pyc 0) · 노트북 표준 오류 출력 0·Traceback 0·`/var/folders` 0 · 남은 프로세스 0.
- 게이트 G1~G7 0(`gates-wip-07.json`) · `verify.py --chapter` PASS 9 sections / 173 code cells · 빌드 HTML `{{` 0 · 인라인 SVG 4 · 삽화 1.
- Before ① 세 칸 모두 `"*"` + 자격 증명 → `https://evil.example` 사전 요청 `200`·허용 출처 `https://evil.example`·자격 증명 `true`, POST도 같음 · ② 실습 앱 401 `WWW-Authenticate: None` ↔ After ① 실습 앱 `400`·`Disallowed CORS origin`·허용 출처 `None`, 허용 출처 POST `200` · ② `HTTPBearer` 새 앱 `401 | Bearer`, `Bearer abc` → `200`(글은 안 봄) · 값 바꿔 보기 사전 요청 없는 모르는 출처 POST → 실습 앱 `200`·허용 출처 `None` · 예시 0초 → `504`, 접근 토큰 없으면 `401`.
- 실습 폴더 앱 파일 고침 0 — `pytest -q -p no:cacheprovider`: 6 passed, 1 warning · `app.openapi()` 직렬화 = `openapi.json`(`06e5d1b9…`) 바이트 같음 · 도구 파일 `serve_tools.py` 06 판 `e1a1464d…` 그대로(`zero_timeout`만 가져옴).

## 품질 개선 08절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/08-diagnosis.md`에 있습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T10:49:45Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 지움, 10:49:56Z) — PASS 22셀, 셀별 출력 글자 22/22 같음(이은 글 해시 `9aba2b6a…`), `code_sha256` `eddd600d…` 같음, `outputs_sha256`은 B의 설치 셀 스트림이 둘로 나뉘어 다름(A `3ac7d06e…` · B `205265b0…` — 02·03·05·06·07 선례). 시험 실행 둘(`/tmp` 사본, 같은 두 자리, 10:49:28Z·10:49:37Z)도 셀별 22/22 같음. 모든 실행 `OPENAI_API_KEY`를 지운 환경.
- 노트북 밖 같은 장면(`/tmp/ch30-08/exp/p5_nb.py` — 노트북 코드 셀 21개를 이은 파일) 5번 출력 md5 모두 같음(`312e2d36…`), 표준 오류 0.
- 모델 요청 0 · 서버 프로그램·포트·자식 프로세스·브라우저·`node`·`npx` 0(노트북 안) · 실습 폴더에서 바뀐 파일은 노트북 08뿐(pyc 0, `openapi.json` 쓰지 않음) · 노트북 표준 오류 출력 0·Traceback 0·`/var/folders` 0.
- 게이트 G1~G7 0(`gates-wip-08.json`) · `verify.py --chapter` PASS 9 sections / 191 code cells · 빌드 HTML `{{` 0 · 인라인 SVG 4 · 삽화 1.
- 응답 문서 `3.1.0`·요청 주소 5·`/v1/chat` `$ref` 둘·`operationId: chat_v1_chat_post` · `ChatRequest` = `model_json_schema()` `True` · 같은 객체 `True` · `/openapi.json` 같은 딕셔너리 `True` · 새로 만든 글 = `openapi.json` `True`(9987자) · 생성기 7.25.0 · SSE 요청 주소 둘의 함수 `Promise<void>` · 실험 실행 1 보안 방식 칸 `False`·응답 코드 `['200', '422']` ↔ 실행 2 `True`·`security` `[{'HTTPBearer': []}]`·`['200']`, 상태 코드 `401`/`401`·`200`/`200`.
- 실습 폴더 앱 파일 고침 0 — `pytest -q -p no:cacheprovider`: 6 passed, 1 warning · `app.openapi()` 직렬화 = `openapi.json`(`06e5d1b9…`) 바이트 같음 · 생성 SDK·`client/*.ts` 그대로 · 도구 파일 `serve_tools.py` 06 판 `e1a1464d…` 그대로(08은 가져오지 않음).
- 노트북 밖(`/tmp/ch30-08/sdk`): README 명령으로 생성(`openapi-generator-cli` 2.41.0 → jar 7.25.0, OpenJDK 11.0.32.1) — `itemSchema` 경고 두 줄·종료 0, 같은 폴더에 두 번째 생성 결과가 실습 폴더 `client/generated/`와 `diff -r` 같음 · `npx --package typescript@latest tsc …`(7.0.2) 종료 0·출력 없음.

## 품질 개선 09절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/09-diagnosis.md`, 흔들림 확인은 `qa/upgrade/09-probe.md`에 있습니다.

- 흔들림 확인(노트북 밖, `qa/upgrade/probe/probe09.py`, 프로세스 다섯): §0 저장 2026-09-29T11:18:44Z → 첫 요청 11:19:07Z. 구조 값·모델 판단 값·모델 글 모두 5/5 같음(답 글 32자·SSE 사건 21·스트림 사건 35·노드 차례 model → tools → model·도구 인자 `월요일`·tools 글 `09:00~18:00`·「실행 2 글 = 도구 글 + 실행 1 글」 `True`). 요청 약 30번.
- 모델 셀 없는 시험 실행 둘(`/tmp/ch30-09/tryA`·`tryB`, 결정적 셀 13개, 11:36:00Z·11:36:13Z) — PASS·셀별 13/13 같음·모델 요청 0.
- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T11:36:42Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 지움, 11:37:44Z) — PASS 23셀, **셀별 출력 글자 23/23 같음(모델 셀 포함, 이은 글 해시 `398570cd…`)**, `code_sha256` `30c6e203…` 같음, `outputs_sha256`은 설치 셀 스트림 나뉨으로 다름(A `ead89bba…` · B `05da1acc…`). 모델 요청 A 6 · B 6(도구를 한 번씩 부를 때). 키는 루트 `.env`에서만, 출력은 `True`뿐.
- 게이트 G1~G7 0(`gates-wip-09.json`, 검사 문장 395) · `verify.py --chapter` PASS 9 sections / 208 code cells · 빌드 HTML `{{` 0 · 인라인 SVG 4 · 삽화 1.
- 실습 폴더 앱 파일: `live_agent.py` 21행 `reasoning_effort="none"` 한 줄 더함(`586a6a69…` → `a7002c81…`) — `app.openapi()` 직렬화 sha256 전후 `06e5d1b9…` 같음(= `openapi.json`) · 정렬 직렬화 `d2fb94f6…` 4825자 같음 · `pytest -q -p no:cacheprovider` 전후 6 passed, 1 warning · 01~08 노트북은 `live_agent.py`의 줄을 출력하지 않음(02는 `app.py`의 `LiveAgentDep` 줄만).
- 도구 파일 `serve_tools.py` 09 판 `ff663039…`(06 판 뒤 06절 함수 넷 + `import json`) — 04·06·07 노트북 사본을 09 판으로 다시 실행해 셀별 출력 23/23·26/26·21/21 같음(`outputs_sha256` 차이는 설치 셀 스트림 나뉨뿐).
- 실습 폴더에서 바뀐 파일은 `live_agent.py`·노트북 09·`serve_tools.py`뿐(pyc 0) · 노트북 표준 오류 0·Traceback 0·`/var/folders` 0 · 서버 프로그램·포트·자식 프로세스 0 · 남은 프로세스 0.

## 품질 개선 10절 — 챕터 끝 실습 절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 10절은 품질 개선 때 새로 만든 절이고, 세부는 `qa/upgrade/10-design.md`(설계·노트북 밖 확인)·`qa/upgrade/10-diagnosis.md`에 있습니다.

- 노트북 밖 확인(`/tmp/ch30-10/exp/p2_cells.py` — 계획한 코드 셀 스무 개를 한 프로세스에서, 키 뺌, `PYTHONDONTWRITEBYTECODE=1`): 2026-09-29T12:10:44Z~47Z **5/5 출력 md5 `1c88ed7bbfef…` 같음 · 표준 오류 0바이트** · 뒤에 `app.openapi()` sha256 `06e5d1b9…`·재정의 딕셔너리 키 0. 모델 요청 0.
- 시험 실행 둘(`/tmp/ch30-10/tryA`·`tryB`, 12:22:45Z·12:22:52Z) — PASS 21셀·셀별 21/21 같음.
- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T12:23:31Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 지움, 12:23:43Z) — PASS 21셀, **셀별 출력 글자 21/21 같음**(이은 글 해시 `6a9b1956…`), `code_sha256` `7541bca1…` 같음, `outputs_sha256`은 설치 셀 표준 출력이 A에서 두 덩어리(66 + 100글자)·B에서 한 덩어리(166)라 다름(A `defaca81…` · B `91beb8de…`). 키 없는 환경(`env -u OPENAI_API_KEY`).
- 묶음을 풀어 학생 자리에서 실행: `part7-practice.zip`(`1b3d4287…`)의 Ch 30 폴더를 `/tmp/ch30-10/bundle`에 풀고 10 노트북을 `notebooks/` 커널(`PYTHONPATH` 없음)로 실행 — PASS 21셀·A와 21/21 같음.
- 게이트 G1~G7 0(`gates-wip-10.json`, 검사 문장 318 · 챕터 전체 `gates-wip-ch30-after10.json` 10/10 PASS) · `verify.py --chapter` PASS 10 sections / 229 code cells · 빌드 HTML `{{` 0·`[[` 0 · 인라인 SVG 3 · 삽화 1.
- 실습 폴더 앱 파일·`openapi.json`·테스트 그대로(`app.openapi()` `06e5d1b9…` = `openapi.json` · `pytest -q -p no:cacheprovider` 6 passed, 1 warning) · 실습 폴더에서 바뀐 파일은 노트북 10·`serve_tools.py`(10 판 `2f66bc6b…`)·`README.md`(10절 한 단락)뿐(pyc 0·`.failure.json` 0) · 노트북 표준 오류 0·Traceback 0·임시 폴더 위치 0 · 서버 프로그램·포트·자식 프로세스 0.
- 도구 파일 10 판으로 04·06·07 노트북 사본을 다시 실행해 셀별 23/23·26/26·21/21 같음(`/tmp/ch30-10/chain`, 앞 노트북은 다시 저장하지 않음) · 09 노트북은 다시 실행하지 않고 가져오는 이름 다섯이 10 판에 그대로 있음을 글로 확인.
- 09 노트북: b8·정리 끝 두 문장만 10절로(`mdpatch.py` 두 번 + `author_09.py --src-only` + `run_section.sh … 09 --no-exec`) — `code_sha256` `30c6e203…`·`outputs_sha256` `ead89bba…`·`executed_at` 11:36:42Z 그대로, 바뀐 셀은 마크다운 셀 48 하나.

## 마감 — 검토 반영과 챕터 마감 (2026-09-29)

- 검토 1차 A(01~05·공통 — 상 1·중 1·하 12)와 B(06~10 — 중 4·하 14)를 반영했습니다. 반영 28건, 미반영 4건(도구 파일 머리 설명 A-9·B-18은 전체 마감 항목, 코드 양 A-11은 강사 확인, `qa/upgrade/__pycache__/` A-12는 삭제 승인 목록). 세부는 `qa/upgrade/chapter-summary.md` §21과 `handoff.md` 끝 절.
- **노트북 재실행 0**: 열 노트북 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같음(09 `30c6e2033d05…`/`ead89bbaaee0…`). 바뀐 것은 마크다운 셀뿐(02 [2] · 04 [8] · 05 [12]·[22]·[34]·[40] · 06 [8]·[26]·[40] · 07 [8]·[12]·[29]·[46] · 08 [26] · 09 [10]·[40] · 10 [2]·[8]·[30]·[44]).
- 생성기 열 개를 고친 글로 메모리에서 실행해 셀·`src_html()`이 노트북·`_src`와 글자까지 같음(49/53/49/49/53/57/47/47/49/45) · 도구 파일 대조 사슬(`author_04`·`06`·`09`·`10`·07·08 `__main__` 조건) 통과 · 디스크 도구 파일 = `TOOLS10`(`2f66bc6b…`).
- 인용 대조(숫자 없는 백틱 인용 포함, 열 절 노트북 마크다운 1,330·`_src` 1,255): 출력 값을 인용했는데 출력에 없는 것 0건(남은 108건은 파일 이름·설치판 파일·API 이름·노트북 밖 확인 값·다른 절 출력 인용).
- `upgrade_gates.py --label after` 10/10 PASS·G1~G7 0 · `verify.py --chapter` PASS 10 sections / 229 code cells (max 12 lines) · `visual.cjs` 22행 PASS · 빌드 HTML `{{`·`[[` 0 · `app.openapi()` `06e5d1b9…` = `openapi.json`·`pytest` 6 passed(`agent.py` 설명 글 두 줄 고친 뒤).
- 묶음: `part7-practice.zip` `007f1387…`(113항목, Ch 30 42파일 = 디스크). `check_bundle_execution.py`는 실행기가 Ch 31 맥 `.venv`라 이 기기에서 돌 수 없어, 새 zip을 풀어 01·10을 키 없이 손으로 실행(PASS 22셀·21셀, 저장 노트북과 셀별 출력 같음). `bundle-execution.json`은 옛 zip 기준 그대로.
- 모델 요청 0 · 삽화 생성 0 · 파일 삭제 0 · 옛 생성기 셋 `qa/upgrade/before/generators/blocked/`로 `mv -n`.
