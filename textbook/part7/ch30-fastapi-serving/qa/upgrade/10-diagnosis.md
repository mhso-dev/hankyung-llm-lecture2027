# 10절 진단 — FastAPI 서빙 실습 (experiment · 챕터 끝 실습 절, 새로 만듦)

- 작업일: 2026-09-29 · 작업자: 실습 절 작업자 · 생성기 `qa/upgrade/author_10.py`(`7b533d50…` — `mdpatch.py` 두 번·직접 치환 뒤 값) · 설계 `qa/upgrade/10-design.md`(노트북 만들기 전에 씀) · 그림 설계표 `qa/upgrade/10-figures.md`(렌더 전에 씀)
- 읽은 것: 규격 `QUALITY-UPGRADE.md` §7-2(먼저)·§2·§2-7(9번 끝·10번 끝)·§3·§4·§5-3·§5-4·§6 · `handoff.md`(머리·챕터 공통 전부·§09 → 실습 절 전부·나머지 절 인계 훑음) · `09-diagnosis.md`(전부)·01~08 진단 「남은 것」 · 준비 노트 §14·§15 · `author_04.py`(가드·`strip_later_imports`)·`author_06.py`(사슬·`DEF_LAST`·06 노트북)·`author_07.py`(`DEF_HEADER`·`__main__`)·`author_08.py`(`__main__`)·`author_09.py`(전부) · 06·07 노트북(코드 셀·출력) · 앞 실습 절 선례 Ch 29 `handoff.md` 「실습 → 챕터 검토」·Ch 24 `author_04.py`·`_src/04`·Ch 28 `review-round1-B.md`(06 — B-9·B-10)·Ch 26 검토 B-7·Ch 27 검토 B-7·B-10 · `AGENT-BRIEF.md`·`PLAYBOOK.md`(§3) · 실습 폴더 `app.py`·`agent.py`·`schemas.py`·`README.md` · Part 7 `_build_index.py`·`collect_public_files.py`·`check_figures.py`·`build_bundle.practice_files` · 설치판 starlette 1.6.0 `middleware/cors.py`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트

| 항목 | 첫 실행 전(`gates-wip-10-10.json`) | 끝(`gates-wip-10.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 0 · 0 · 0 · 0 · 0 · 3 · 3 | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(주석·빈 줄·`%` 줄 뺌) | 21 · 115 | **21 · 115** |
| 검사 문장 | 294 | **318** |

- 첫 실행 전 G1·G2 0(G5는 출력 전이라 셈 없음) · G6 3(b10 한 문장 70자 넘음·영문 시작 「CORS와」 · URL 뒤 마침표가 URL과 함께 빠져 두 문장이 한 문장으로 셈) → 문장을 나누고 URL을 문장 끝에 두지 않음 · G7 3은 그림 전이라 당연. 렌더 뒤 G6 1(10-3 도식 읽기 한 문장) → 나눔 · 삽화 뒤 G6 1(「그림 읽기 —」 머리가 첫 문장 글자 수에 들어감) → 줄임. 챕터 전체 `gates-wip-ch30-after10.json` **10/10 PASS**.
- AST 따로(`/tmp/ch30-10/tools/extra_check.py` — 09 도구 그대로): 걸린 것 **0** — f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`getattr`·`isinstance`·`while`·`try`·별표 풀기·대입 풀기(for 포함)·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·클래스·데코레이터·딕셔너리 `.get`·`.items`·`sorted`·`set`·`await`·`async` 모두 0. 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **9줄** · 함수 본문 최대 **8줄**(`resume_flow` — 주석 뺌) · 셀당 정의 하나 · 한 글자 변수 0.
- **01~09 대조(`/tmp/ch30-10/tools/inventory30.py` — Ch 29 `inventory29.py`를 Ch 30 01~09 노트북 + 도구 파일 09 판으로 바꿈)**: 노드 종류·내장 이름·속성·키워드 인자·연산자·문자열 첨자 **새로 씀 0**. 가져온 이름에서 새것은 `serve_tools.header_or_none`·`serve_tools.last_event_id` 둘뿐(06·07 노트북이 정의한 함수를 도구 파일로 옮긴 것). `is None`(연산자 `Is`)·목록 슬라이스 `[0:2]`·목록 `+`·`client.options`는 06·07에 있는 모양.
- 금지어(`/tmp/ch30-10/tools/ban_ctx.py` — `ban30.py` 목록에서 허용 문맥 「사전 요청」·「접근 토큰」·「스트림 사건」 등을 뺌; `_src`·노트북 마크다운·코드 주석·`.mmd`·캡션·alt): 남은 것은 **「서빙」 셋**(노트북 제목 셀 · 제목 풀이 「제목의 서빙은 …」 두 곳 — 챕터 공통 8 「제목 말은 첫 자리에서 한 번 풂」)과 **그림 파일 이름 「…접근-토큰만-…」**(파일 이름 — 산문 아님)뿐. 1회차에 걸린 「스트림 흐름」(「스트림」 단독) → 「SSE 응답을 받는 흐름」.

## 설계 (자세한 것은 `10-design.md`)

- **한 요청 흐름**: 도서관 웹 화면(허용 출처 `http://localhost:5173` — 앱 21행) → 사전 요청(07) → 접근 토큰을 실은 첫 요청 SSE 응답(05·07) → 앞 사건 둘에서 끊김(06 노트북 2절 자리) → 요청 머리 이름에 `Last-Event-ID`를 더한 사전 요청(07) → 이어 받기(06) → 판정 `ended_with_done`(06)·`join_tokens`(04). 기록 장치 `record_step`·`print_log`(단계마다 [이름, 상태 코드, 허용 출처]). 조립 함수 둘 `start_flow(token, log_rows)`·`resume_flow(token, received, log_rows)`.
- **붙인 기능 셋이 모두 흐름 안에서 쓰임(실행 1)**: 05 SSE 응답(첫 요청·이어 받기 응답을 `read_events`로) · 06 이어 받기(`last_event_id` → 요청 머리 `Last-Event-ID` → `web-1:2`부터, 판정) · 07 사전 요청·허용 출처 응답 머리(`header_or_none`)·접근 토큰. 실행 2에서는 흐름이 첫 요청의 401에서 멈춰 이어 받기 두 단계를 보내지 않음(판정은 빈 목록으로 `False` — 06 함수가 그대로 쓰임).
- **실행 2 = 접근 토큰 하나**(`Bearer local-demo-token` → `Bearer wrong-token`, 07절 노트북 2절 값). 07이 틀린 접근 토큰에 401을 이미 보였으므로 b2·노트북 7절 「새로 볼 것」은 실행이 보인 만큼만(Ch 26 05 검토 B-7): 사전 요청은 두 실행 모두 200(흐름의 사전 요청에는 `Authorization`이 없고 CORS 층이 앱으로 넘기지 않음 — 설치판 `cors.py` 91~94행) · 401 응답에도 허용 출처 응답 머리(156~174행 — 상태 코드를 보지 않음) · 흐름이 이어 받기로 가지 않음 · 판정 `False`. 다른 후보(허용 출처 하나·`Last-Event-ID` 하나·시간 제한 0초)를 뺀 까닭은 `10-design.md` §2.
- **뺀 것과 까닭(b3 한 단락)**: 01 422·03 JSON 요청 주소(SSE 흐름 하나에 모음) · 02·06 시간 제한 재정의(06에서 견줌) · 07 `HTTPBearer` 새 앱(실습 앱을 고치지 않음) · 04 `astream`(앱이 안에서 부름) · 08 응답 문서(요청 흐름 밖) · 09 실제 모델(매번 같은 값으로 결론).
- **손으로 적은 값**(모두 실행 전에 정함 — 출력 라벨과 b7에 출처): 질문(03~07) · 출처(앱 21행) · 교재용 접근 토큰(앱 57행) · 틀린 접근 토큰(07 노트북 2절) · 스레드 이름 `web-1`(이 절에서 정함) · 끊기는 자리 2(06 노트북 2절) · 사전 요청 머리 이름 글(07 + `Last-Event-ID`).
- **말**: 새 용어 0(meta 「실습 30분 · 새 용어 0」) — 사전 요청·허용 출처·출처·CORS 층(07) · SSE 사건·사건 번호·칸(05) · 이어 받기(06) · 접근 토큰(Ch 28·02·07) · 제공 함수·재정의 딕셔너리(02) · 시험용 클라이언트(01)를 같은 뜻으로. 「스트림 사건」(04 — 파이썬 값)은 쓰지 않고 HTTP 쪽은 모두 「SSE 사건」. 「기록기」(logger, 06) 대신 이 절의 장치는 「단계 기록」·「기록 목록」. 「토큰」 단독 0. 제목 말 「서빙」은 b2·노트북 1절에서 「제목의 서빙은 만든 에이전트를 웹 앱에 올려, 요청에 답하게 하는 일입니다」로 한 번 풂.
- **모델 요청 0**(키 셀 없음, `env -u OPENAI_API_KEY`) — 규격 §7-2 「모델 호출 3~5번」과 다름 → b3 한 단락·강사 확인(Ch 23 07·Ch 24 04 선례). 앱 기록기 `logger.exception`을 지나는 길이 없어(401은 제공 함수가 `HTTPException`으로 올림) 06절의 기록기 수준 셀은 두지 않음 — 노트북 밖 5번·새 커널 두 번 모두 표준 오류 0.

## 노트북 밖 확인 · 실행 (새 커널)

| 실행 | 자리 | 키 | 모델 요청 | 결과 |
|---|---|---|---|---|
| 탐색 `p1_flow.py`(12:06Z, 한 번) | 기기 프로세스 | 없음 | 0 | 흐름·접근 토큰 없음(401·허용 출처 같음 — 노트북에 안 씀)·SSE 응답 머리 이름 일곱·사전 요청 본문 `OK`·`access-control-max-age: 600` |
| **노트북 밖 5번** `p2_cells.py`(12:10:44Z~47Z) | 기기 프로세스(계획한 코드 셀 스물을 한 프로세스에서) | 없음 | 0 | **5/5 md5 `1c88ed7bbfef…` 같음 · 표준 오류 0** · 뒤 `app.openapi()` `06e5d1b9…`·재정의 키 0 |
| 시험 tryA(`/tmp/ch30-10/tryA`, 12:22:45Z) | 루트 커널 | 없음 | 0 | PASS 21셀 |
| 시험 tryB(같은 사본, `--cwd notebooks/`, `PYTHONPATH` 지움, 12:22:52Z) | 학생 커널 | 없음 | 0 | PASS 21셀 · tryA와 21/21 같음 |
| **A**(`run_section.sh … 10`, `executed_at` 2026-09-29T12:23:31.330151Z) | 루트 커널 | 없음 | 0 | PASS 21셀(그림 첨부 단계에서 멈춤 — 10-1 PNG 전) |
| **B**(A 사본 `/tmp/ch30-10/B`, `execute.py --cwd notebooks/`, `PYTHONPATH` 지움, 12:23:43Z) | 학생 커널 | 없음 | 0 | PASS 21셀 |
| 묶음 풀어 실행(`part7-practice.zip` `1b3d4287…` → `/tmp/ch30-10/bundle`, `notebooks/` 커널, `PYTHONPATH` 없음) | 학생 묶음 자리 | 없음 | 0 | PASS 21셀 · A와 21/21 같음 |

- **A ↔ B 셀별 출력 글자 21/21 같음**(이은 글 해시 `6a9b1956b63ea98c`) · `code_sha256` **`7541bca126e47b28036a5564576f893be984ef227ed6f8a8e742e3a80bf6d451`** 같음 · `outputs_sha256` 다름(A **`defaca81a09f89a958ad5b1fa29449795556e220350e4c2a37a31ad616517f72`** · B `91beb8dee89ae8beaa6b0ccace594cba67bce6ec9cbdc80db887e2dce4932260` = tryB 값) — 까닭: 설치 셀 [1] 표준 출력이 A 두 덩어리(66 + 100글자)·B 한 덩어리(166글자)(합친 글 같음 — 02~09 선례). **갈린 셀 0.** 새 커널 두 번째 실행 B(12:23:43Z)는 설계표·`.mmd`·첫 렌더보다 먼저 돌림.
- A 뒤 `mdpatch.py` 두 번(① b6 실행 문장 자리 표시 → 실제 문장 — 생성기·`_src`만 ② 그림 셋의 alt·도식 읽기 — 노트북 「오늘 볼 그림」 셀 포함) · 생성기 직접 치환(노트북에 없는 `_src` 글만 — 삽화 alt·캡션·그림 읽기, b4 비유·b4·b6 문장, 10-3 도식 읽기) → `--src-only` → `--no-exec`. 첫 실행 전 치환(G6 둘·「스트림 흐름」)은 A보다 앞. 노트북 코드·출력·`executed_at` 그대로(A 사본과 21/21·`outputs_sha256` `defaca81…` 같음) · 생성기 `cells()`와 저장 노트북 셀 글 45/45 같음 — 노트북 파일 **`abb8805641584f01a5d1e620b61e49e46f92e7a8926e8a976bd5352a506a7c14`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에서 새로 생기거나 바뀐 파일은 노트북 10·`serve_tools.py`·`README.md`뿐(pyc 0·`.failure.json` 0) · 노트북 표준 오류 0·Traceback 0·임시 폴더 위치 0·실행마다 다른 ID·시각·포트 0 · 서버 프로그램·포트·자식 프로세스 0 · 남은 프로세스 0(`ps` — uvicorn·ipykernel·jupyter·node·execute 없음).

## 확인한 값 (결론·그림·정리·복습에 쓴 값 — 모두 매번 같은 값)

- 기준 응답: `상태 코드: 200` · `허용 출처: http://localhost:5173` · 사건 이름 token 여섯 + `done` · 이어 붙인 글 `질문을 확인했습니다: 반납 기한을 알려 주세요 `(끝 공백 하나 — 04와 같음).
- 실행 1: 기록 네 줄 `사전 요청 | 200 | http://localhost:5173` · `첫 요청 | 200 | …` · `사전 요청(이어 받기) | 200 | …` · `이어 받기 | 200 | …` · 끊기기 전 `['token', 'token']`·`web-1:1` → 이어 받은 첫 번호 `web-1:2` · 이은 사건 일곱 · `마지막 사건이 done인가: True` · `기준 응답의 글과 같은가: True`.
- 실행 2: 기록 두 줄 `사전 요청 | 200 | http://localhost:5173` · `첫 요청 | 401 | http://localhost:5173` · 본문 `{'detail': '인증 정보가 올바르지 않습니다'}` · 받은 사건 `0`·번호 `None` · 이은 사건 `0` · `False` · 글자 수 `0` · `False`.
- 두 실행 표: 사전 요청 200·200 · 첫 요청 200·401 · 허용 출처 같음 · 기록한 단계 수 4·2 · done `True`·`False` · 같음 `True`·`False`.
- 흔들리는 값: 없음(모델 없음 · 시각·ID·포트 출력 없음).

## 서비스 요청 수 · 비용

- 모델 요청 **0**(노트북 밖 탐색·5번·시험 둘·A·B·묶음 실행·앞 노트북 사본 셋 모두 키 없는 환경). 비용 0. Higgsfield 삽화 2회 생성 4크레딧(아래).

## 앱 파일 · `app.openapi()` · `tests/`

- 앱 파일 고침 **0**: `app.py` `3455d405…` · `agent.py` `a6c42e63…` · `schemas.py` `ed77b197…` · `__init__.py` `1c7d7aef…` · `live_agent.py` `a7002c81…` · `tests/test_app.py` `f8611741…` · `openapi.json` `06e5d1b9…` 그대로. `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 `True`(노트북 밖, 끝에 다시 확인) · `pytest -q -p no:cacheprovider` **6 passed, 1 warning**(pyc 0). 노트북은 `app.py` 99~105행을 글로 읽기만 함.

## 도구 파일 — 10 판

- `serve_tools.py` 09 판 `ff663039…` → **10 판 `2f66bc6b504295f8a5293acd69de8e8104208827d7bae42c16c28729091508e1`**: 09 판 끝에 **06절 `last_event_id(events)`**(`author_06.DEF_LAST`)·**07절 `header_or_none(response, name)`**(`author_07.DEF_HEADER`)를 그 절 노트북 셀 글 그대로(주석 첫 줄 「# Ch 30 06절에서 배웠습니다 — 06절 노트북의 같은 이름 함수를 옮겼습니다」·「# Ch 30 07절에서 배웠습니다 — 07절 노트북의 같은 이름 함수를 옮겼습니다」). 가져오기 줄 더하지 않음(`import json` 하나 그대로) · 두 함수 모두 인자만 씀.
- 사슬(`author_10.py`의 `MOVED10`·`TOOLS10`·`check_tools10`·`check_older_guards`·`write_tools`·`--tools-copy`): `author_09.check_tools09()`(→ 06 → 04 사슬) 통과 · `TOOLS10.startswith(TOOLS09)` · 함수 차례 = `TOOL_ORDER09` + 둘 · 가져오기 `json` 하나 · 옮긴 셀 글이 06·07 노트북 코드 셀과 문자열로 같음·AST 같음 · `# Ch 30 ` 주석 열 개. 쓰기 가드: 09 판이거나 10 판일 때만 씀, 10 판으로 시작하는 더 긴 판은 건너뜀, 그 밖은 멈춤. `--tools-copy`는 10 판 글을 사본 폴더에 씀.
- **앞 생성기의 대조 줄**: 04 가드(`strip_later_imports` 뒤 04 판으로 시작 + 04 판과 다름 → 건너뜀) · 06 가드(04·06 판과 다름 + strip 뒤 06 판으로 시작 → 건너뜀) · 09 가드(06·09 판과 다름 + 09 판으로 시작 → 건너뜀) · 07·08 `__main__`(strip 뒤 06 판으로 시작 → 통과)이 **10 판에서도 그대로 맞아 고치지 않음** — `author_10.check_older_guards()`가 같은 조건을 10 판에 대 봄(그 생성기는 실행하지 않음). `author_04`·`06`·`07`·`08` 파일 해시 그대로(`45d6eb6d…`·`b4cc80fd…`·`3eddb10a…`·`d446971b…`).
- **가져오는 앞 노트북 영향**: 04·06·07 노트북 사본(`/tmp/ch30-10/chain`)을 10 판으로 다시 실행(키 뺀 환경) → PASS, 셀별 **23/23·26/26·21/21 같음**(06은 `outputs_sha256` `e1b573c1…`까지 같음, 04·07 차이는 설치 셀 스트림 나뉨뿐). 실습 폴더의 세 노트북은 다시 저장하지 않음. **09는 다시 실행하지 않고** 가져오는 이름 다섯(`ended_with_done, event_names, join_tokens, read_events, token_values`)이 10 판에 그대로 있음을 글로 확인. 05·08은 가져오지 않음. 06·07 노트북은 자기 셀의 `last_event_id`·`header_or_none` 정의를 그대로 둠(처음 가르친 절).
- 공개 목록 두 곳: 도구 파일 줄은 이미 있음(파일 해시만 바뀜) · 10 노트북 줄 더함(아래).

## 09 노트북 · 본문 (다시 실행하지 않음)

- 09 b8 「다음 학습과 이어지는 지점」과 노트북 정리 끝 두 문장(Ch 31 문장)을 10절로: 「<a>10절</a>에서는 05~07절의 사전 요청·SSE 응답·이어 받기를 한 흐름으로 이어 실행합니다. 접근 토큰 하나만 바꾼 실행과 견주고, 모델은 부르지 않습니다」(노트북은 같은 두 문장). Ch 31 두 문장은 10절 b8·노트북 정리 끝으로 옮김(같은 글).
- 방법: `mdpatch.py … 09` 두 번(생성기 모양·`_src` 모양·노트북 모양 짝 셋 + 생성기에 `L_10` 한 줄 · 두 번째는 G6 70자 줄임) → `author_09.py --src-only`(결과가 `mdpatch.py` 판과 바이트 같음) → `run_section.sh … 09 --no-exec`(09 게이트 0). **09 노트북 `code_sha256` `30c6e2033d05…`·`outputs_sha256` `ead89bbaaee0…`·`executed_at` 11:36:42Z 그대로**, 셀별 출력 23/23 같음, 메타데이터 같음, 바뀐 셀은 마크다운 셀 48 하나 · 생성기 `cells()`와 저장 노트북 49/49 같음. 09 노트북 `f9db00d5…` → `f321fbe1…` · `_src/09` `78f86211…` → `23ec49e1…` · HTML `2d3a2669…` → `dafde498…` · `author_09.py` `0ef09813…` → `4beb7945…`.

## 그림

- 설계표 `10-figures.md`를 새 커널 A·B 뒤, 렌더 전에 씀. Mermaid 셋: **10-1 조립도**(`flowchart TB`, 노드 7 — 재료·우리 함수 넷·CORS 층·실습 앱) · **10-2 실행 1 실제 순서**(`flowchart TB` 한 줄 여섯) · **10-3 실행 1·2 비교**(`flowchart TB` 공통 상자 + 칸 둘, 노드 5). 첫 렌더에서 라벨 여섯이 낱말 자리에서 저절로 줄바꿈(끊김 없음) → 모두 `<br>`로 미리 나눠 다시 렌더(보기 사본 `.cache/ch30-10-view/10-N-v2.png`를 열어 확인 — 같은 이름 PNG는 읽기 도구가 앞 판을 보여 줘서 이름을 바꿈). 최종 viewBox 폭 **511 · 265 · 659**(868 이하), 끊긴 라벨 0. 색: 재료·실습 앱 처리 함수·두 접근 토큰 **초록** · 우리 함수·끊김 자리·판정 **파랑** · 단계 결과·판정 출력 **노랑**(401도 받은 오류라 노랑) · CORS 층·두 실행 공통 **회색** · **보라 0 · 빨강 0**. 갈래(요청을 보냄)는 점선, 두 칸은 공통 상자에서 화살표만. 라벨 숫자는 출력(200·401·5173·`web-1:1`·`web-1:2`)이나 본문(절 번호·앱 19~26행)에 있는 것만.
- 삽화 10-4: **1차 job `97fb9b4b-3e07-49b2-81dc-983fb190263f` 탈락**(선로가 고리 모양, 칸 차례가 섞이고 산호색 칸 둘이 떨어져 그려짐 — 「세 종류가 차례로 한 열차」가 안 읽힘, 거래 12:27:55.767824Z −2) → **2차 job `a5351a85-82f9-4b7f-b64d-41f72c9aab31` 채택**(재생성 1회 — 한도 안, 거래 12:29:22.775608Z −2) · **이 절 몫 4크레딧**(잔액 2269 → 2265, 앞 거래 11:43:08Z는 09절) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 원본 `b80fa428…`(2752 × 1536, RGBA 알파 모두 255) → 저장 PNG **`f25780a4097885ad7216e74544f09caf809d885dc862089d370fff06d28580ef`**(1100 × 614, RGB) · 결과를 다시 받아 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0 · 저장본과 같은 보기 사본을 열어 **검은 기관차 하나·연보라 닫힌 칸 둘·흰 둥근 통 칸 둘·산호색 덮개 칸 둘**을 세고 그림 읽기를 씀. 거의 흰 가로줄 106/614·흰 픽셀 비율 0.863(선 그림). 짐칸 색을 프롬프트에 이름으로 정함(09 교훈) · 01~09 소품 되풀이 없음(설계와 다른 점: 곡선 대신 거의 곧은 비스듬한 선로 — 09-5처럼 비스듬, 자갈 없음).

## 검사

- `run_section.sh … 10 --no-exec`(마지막): 렌더 도장 같아 건너뜀 · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 10 sections / 229 code cells (max 12 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `10-FastAPI-서빙-실습.html`(`90e7da8a…`): `{{` **0** · `[[` 0 · 인라인 SVG 3 · 삽화 JPEG 1. 09 HTML도 `{{` 0.
- `pack.py … 10` → `qa/upgrade/review-pack/10-FastAPI-서빙-실습.md`(`d397c737…`) · 09 묶음 다시(`7c7c06f4…`).
- 보호 파일 255개: 같음 **210** · 바뀜 **45** · 없어짐 0 — `manifest-changes.md` 「10절 뒤」(09 뒤 값 31 그대로 + 이 절 14).

## 챕터 밖 수정

- `labs/part7/ch30-fastapi-serving/README.md`(10절 한 단락만) · `labs/…/notebooks/serve_tools.py`(10 판) · `textbook/part7/public-files.json`(`collect_public_files.py` — 10 노트북 한 줄) · `textbook/part7/prerequisite-files.json`(같은 스크립트가 다시 씀 — 바이트 같음) · `textbook/part7/index.html`·`textbook/downloads/part7-practice.zip`·`textbook/part7/qa/integration-results.json`(`_build_index.py` 한 번, `Part 7: 30 verified sections; 110 bundled files`) · `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py`가 씀) · 사용자 디스크 `.cache/ch30-10-view/`(보기 사본 다섯 — 새 폴더).
- 고치지 않음: 공용 도구·규격·과정 문서·검사 스크립트(`check_bundle_execution.py`·`check_delivery.py`·`check_figures.py`·`visual.cjs`)·`textbook/_notebook/build_index.py`(64행 Ch 30 절 수 9 — 실습 절을 빼고 세는 과정 약속)·`check_course_continuity.py`(Part 7을 보지 않음)·앱 파일·TS 파일·생성 SDK·`openapi.json`·`pyproject.toml`·`uv.lock`·01~08 노트북·`_src`·`author_01~08.py`·Ch 31 이후 파일·claude.ai 프로젝트 문서.

## 강사 확인 대상

1. **모델 요청 0**인 실습 절(규격 §7-2 「모델 호출 3~5번」과 다름 — 챕터 결정 M0·09 인계 권고·Ch 23·24 선례).
2. 실행 2의 바꾼 값을 **접근 토큰**으로 고른 것 — 07이 틀린 접근 토큰 401을 이미 보여 「새로 볼 것」을 사전 요청·허용 출처 머리·흐름이 멈추는 자리로 한정함.
3. 이어 받기 앞에 **사전 요청을 한 번 더 보내는 흐름** — 요청 머리 `Last-Event-ID`를 더 싣기 때문이라는 흐름 설계이고, 브라우저가 사전 요청을 언제 다시 보내는지(담아 두는 시간 `access-control-max-age: 600` 등)는 실행하지 않음(b7에 밝힘).
4. 「화면이 401을 읽을 수 있다」를 07절 규칙과 설치판 `cors.py` 소스로 말하고 브라우저에서는 실행하지 않은 것.
5. 도구 파일로 옮긴 06 `last_event_id`·07 `header_or_none` — 06·07 노트북에는 정의가 그대로 남음(처음 가르친 절).
6. 제목 말 「서빙」을 b2·노트북 1절에서 한 번 풀어 쓴 것(금지어 「서빙」(제목 밖)의 예외 — 챕터 공통 8 「제목 말 첫 자리 풀이」).
7. 삽화의 흰 픽셀 비율 0.863(선 그림 — 거의 흰 가로줄 106/614은 06~09와 비슷) · 곡선을 바랐으나 비스듬한 곧은 선로.

## 남은 것 (마감 몫 — `handoff.md` 「실습 → 챕터 검토」 5에 모음)

- `part7-practice.zip`은 이 절의 `_build_index.py` 실행이 한 번 다시 만듦(`1b3d4287…`, Ch 30 01~10 새 판·도구 파일 10 판). README 다시 쓰기·`objectives` 뒤 마감에서 한 번 더 · `bundle-execution.json`은 옛 값(Ch 30 01 `code_sha256` 옛 `7bd57d1f…`) — Part 7 `check_bundle_execution.py`는 Ch 30 01만(실습 절을 넣으려면 스크립트 수정 — 후보로만 기록, 고치지 않음).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-10-10.json`·`gates-wip-ch30-after10.json` · 기기 `/tmp/ch30-10/`(탐색 스크립트·5번 출력·시험 tryA·tryB·A·B 사본·도구 사본·`chain/` 사본 셋·`bundle/` 푼 묶음(약 2MB)·`nb09/` 사본·삽화 원본 셋 `illu/`·`README.before.md` 등) · 사용자 디스크 `.cache/ch30-10-view/`(보기 사본 다섯).
- 작업 중 잘못 넣은 셸 명령 한 번(`rm -rf /dev/null` — 묶음 폴더를 만들기 전 줄에 들어감): 권한이 없어 아무것도 지워지지 않았고 `/dev/null`이 그대로인 것을 바로 확인함(연결 폴더·작업 파일 삭제 0).
