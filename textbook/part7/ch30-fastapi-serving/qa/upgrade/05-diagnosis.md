# 05절 진단 — POST SSE 이벤트 설계 (experiment)

- 작업일: 2026-09-29 · 작업자: 05절 작업자 · 생성기 `qa/upgrade/author_05.py`(`0c46b5d2…` — 마지막 `mdpatch` 뒤)
- 읽은 것: `handoff.md`(머리·챕터 공통 전부·§04 → §05 전부, 앞 인계 훑음) · 준비 노트 `chapter-lead-notes.md`(머리·§0·§1·§2 04·05·06·07·§7-1~7-6·§8) · `04-diagnosis.md` · `author_04.py`(전부)·`author_01.py`(`FIND_LAB` 대조)·`author_02.py`·`author_03.py`(인증 머리·`TestClient` 셀) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 규격 전부 · 과정 요약(§1·§2-16·§2-19·§5 용어) · Ch 25 01·02 `_src`(스트림 사건·진행 값·스트림 청크·모드 차례) · 옛 05 `_src`·노트북(`before/`). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다. Ch 28 03 생성기는 읽지 않았습니다 — 이 절은 자식 프로세스를 띄우지 않기로 정해 정리 규칙이 필요 없었습니다(아래).

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-05.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 2 · 2 · 4 · 0 · 6 · 21 · 3 = **38** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(주석·빈 줄·`%` 줄 뺌, `extra_check.py`) | 4 · 30 | **25 · 158** |
| 검사 문장 | 79 | **410** |

- 첫 실행 전 `upgrade_gates.py … --label wip-05 --section 05`: G1·G2 **0**(G6 3 — 70자 넘는 문장 하나·영문으로 시작하는 문장 둘, G7 3 — 그림 전) → 고친 뒤 G6 0.
- AST 따로(`/tmp/ch30-05/tools/extra_check.py` — 04 도구 그대로): 걸린 것은 **챕터 허용 범위뿐** — 셀 맨 위 `async for` 하나(코드 셀 [7], 처리 함수가 내놓은 값을 꺼냄) · 처리 함수 `stream_answer`(코드 셀 [18] — `async def`·매개변수 힌트 `body: ChatRequest`·안의 `async for`·`yield` 둘 — FastAPI 처리 함수 예외·비동기 생성기 `yield`는 이 절 몫). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`while`·`try`·별표 풀기·대입 풀기(for 포함)·`+=`·기본값 매개변수·내놓는 값 힌트·클래스·데코레이터·가짜 에이전트·`asyncio`·`join`·딕셔너리 `.get`·`.items`·셀 맨 위 await **0**. 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **10줄**(코드 셀 [17]) · 함수 본문 최대 **7줄**(`stream_answer`) · 셀당 정의 하나.
- 금지어(`/tmp/ch30-05/tools/ban30.py` — 04 도구 그대로, `_src`·노트북 마크다운·코드 주석·`.mmd`·캡션·alt): 걸린 것은 **허용한 것과 거짓 양성뿐** — 「노드」(Ch 13 말, 03·04와 같음) · 「스트림」(「스트림 사건」·「스트림 청크」 — Ch 25 말) · 「청크」(「스트림 청크」 한 번, b3의 Ch 25 02 되짚기) · 「이벤트」(제목 풀이 「제목의 이벤트는 …」 `_src` 한 번·노트북 한 번 + 노트북 제목 셀) · 「의존성」(02 용어) · 「토큰」(「접근 토큰」 — Ch 28 말) · 「로그」(「프로그램」). 「필드」·「식별자」·「프록시」·「직렬화」·「파싱」·「버퍼」·「헤더」·「택배」·「반환」·「검증」·「지연」·「측정」·「결정적」·「조각」·사용자가 금지한 표현·「쉽게·간단히·당연히」·「토큰」 단독·「Agent」(본문) **0**.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/05-…ipynb`·`before/_src/05-*.html`)

1. 준비 셀이 루트 커널에서 멈춤(`next((p for p in (start, *start.parents) …), None)` + `os.chdir`) — 01~04와 같은 문제. `TestClient`로 첫·끝 블록만 `assert`, 처리 함수 `chat_stream`의 줄·`yield`를 읽지 않음.
2. `[b for b in re.split(r'\r?\n\r?\n', …) if b]`(내포식·한 글자 변수·`re`) · `text.count('event: token')` · 질문 길이별 token 수 3·4(노드의 공백 나누기 규칙 확인이고, 값 여러 개를 바꿈).
3. b3 「04절에서 astream 청크를 읽었고 Ch25에서 진행 이벤트와 토큰 이벤트를 분리했습니다」 — Ch 25 말이 아니고, Ch 25가 가른 것은 모드(진행 값·스트림 청크)임. b4 비유 「택배 상자 운송장」(Ch 20 금지 계열 「택배 송장」·챕터 금지어 「택배」).
4. 「이벤트」 17·「필드」 7·「식별자」 6·「프록시」·「버퍼」·「헤더」·「직렬화」·「파싱」·「재연결」 · b4 「네이티브 응답은 캐시 방지, 프록시 버퍼링 방지, 연결 유지 ping을 처리합니다 … 로드 밸런서와 CDN이 …」(실행하지 않은 설명) · 「서비스 설계 판단」 긴 단락(progress·출처·여러 서버 인스턴스 — 실행 안 함) · 도식 읽기 틀 색 문장(「보라색 상자는 Agent 실행」 — 모델 없는 절에 보라).
5. 첫 줄 주석·결과 읽기 0 · 제목 셀·그림 첨부 없음 · 참고 자료 둘(확인 2026-09-11, 설명 없음) · 복습 해설 한 줄 · b8이 학습 목표를 그대로 되풀이.

## 바꾼 것

- **04 b8 조건(handoff §04 → §05 1)**: 「05절에서는 처리 함수 `chat_stream`이 이 진행 값을 SSE 응답으로 보내는 모양을 봅니다. 사건마다 이름과 번호를 붙여 보내는 방법입니다」 → **참**. 2절 앱 파일 95~124행 출력(데코레이터 줄 `response_class=EventSourceResponse`·114~116행 `yield ServerSentEvent(data=chunk, event="token", id=…)`·118행 `done`) → `chat_stream`을 HTTP 없이 바로 불러 `async_generator`(02가 제공 함수를 직접 부른 모양) → 셀 맨 위 `async for`로 `ServerSentEvent` 일곱(`token` 여섯·사건 번호 `sse-1:0`~`sse-1:5`·`done` 하나는 번호 `None`) → 3절 시험용 클라이언트 POST → `200`·`text/event-stream; charset=utf-8`·응답 머리 셋 → 본문 글 그대로 → `split_sse`로 SSE 사건 일곱(빈 줄로 나눈 글 여덟, 끝이 빈 글) → `parse_sse`로 칸 딕셔너리(칸 이름 `['event', 'data', 'id']`, 끝 사건은 `id` 없음) → 자리 표 → `json.loads`(한글이 `질` 유니코드 번호로 적힌 JSON 글 → `{'token': '질문을 '}`) → token 사건 data 여섯이 처리 함수가 내놓은 data와 같음 `True`.
- **비동기 생성기 `yield`(A 트랙 첫 풀이, handoff §04 → §05 8)**: 뜻(정의 줄 `async def` + 몸통 `yield` = 비동기 제너레이터 함수, 부르면 비동기 제너레이터) → 일상 예(빵을 한 판 구울 때마다 진열대에 내놓고 멈춘 자리에서 이어 굽기 — 04의 「오븐에서 빵이 한 판 나올 때마다 기다렸다가 진열대에 올리기」와 짝, 04는 받는 쪽·05는 내놓는 쪽) → 코드(`chat_stream`·`stream_answer`) + B 트랙 Ch 2 09 한 문장 · Python 언어 참조 6.2.9.3.
- **`asyncio.timeout` 첫 풀이**(쓰는 절 — 앱 109행을 학생에게 보이므로): 「들여 쓴 줄 전체에 시간 제한 · 정한 초를 넘기면 그 일을 취소하고 `TimeoutError`로 바꿈(Python 문서) · 02의 `wait_for`와 같은 일을 여러 줄을 감싸는 모양으로」 + 「이 절에서는 시간 제한을 넘기는 장면을 실행하지 않았고, 06절에서 봅니다」.
- **실험(experiment, 값 하나만 — handoff §04 → §05 6 ①)**: 앱 `chat_stream`에서 시간 제한·이어 받기·접근 토큰·오류 처리를 뺀 작은 처리 함수 `stream_answer` 하나를 **새 앱 객체 둘에 `add_api_route`로 이음** — 실행 1은 `response_class=EventSourceResponse`, 실행 2는 그 인자만 뺌(요청 주소·요청 방식·함수·질문 같음). 같은 함수 객체를 두 번 잇으려고 데코레이터 줄 대신 `add_api_route`를 씀(데코레이터 줄이 안에서 부르는 메서드 — 설치판 소스 행으로 밝힘). 가설은 FastAPI 문서 SSE 쪽·JSON Lines 쪽에서. 결과: 실행 1 `3절 앱 응답 본문과 같은가: True`·`event:` 줄 7 ↔ 실행 2 `application/jsonl`·응답 머리 `['content-type']`·`event:` 줄 0·줄 7·첫 줄 키 여섯(`ServerSentEvent`의 칸 전부, 적지 않은 셋은 `None`)·응답 문서 본문 종류 `['text/event-stream']` ↔ `['application/jsonl']`(항목 형식 칸 넷 ↔ `{}`) · 결과 표. **결론은 종류·개수만**(매번 같은 값). 옛 「질문 길이별 token 수」는 쓰지 않음(04 4절이 「사건 수 = 답의 낱말 수」로 이미 보임).
- **도착 시각 주장 없음(handoff §04 → §05 4)**: 시험용 클라이언트가 본문을 끝까지 모아 준다는 사실을 3절 결과 읽기·b4 비유의 다른 점·b7·05-3 도식 읽기에 밝힘(starlette 1.6.0 `testclient.py` 296·341·365행 — 설치판 소스). **uvicorn 자식 프로세스는 띄우지 않음** — 이 절은 차례(응답 글에 적힌 차례)만 주장하고, 도착 차례는 주장하지 않으므로 필요 없음. 그래서 포트·`terminate()` 셀 0, Ch 28 03 정리 규칙을 쓸 자리 없음.
- **말(handoff §04 → §05 5)**: 아래 「정한 SSE 말」. 새 용어 **4**(meta 「새 용어 4」): SSE(Server-Sent Events)·SSE 사건·비동기 제너레이터 함수(async generator function)·JSON 줄 형식(JSON Lines). 「사건 이름」·「사건 번호」는 SSE 사건의 칸 풀이로 셈하지 않음. 「본문 종류」는 응답 머리 칸 `content-type`의 출력 라벨(한 문장 풀이).
- 노트북: 제목 셀(할 일 셋·준비물·기준 버전·강의와 실습 범위) · 오늘 볼 그림(05-1 첨부) · 설명 → 코드 → 결과 읽기 · 실험(가설·실행 1·실행 2·결과 표·결론) · 정리 세 줄 + 06 예고. 설치 셀은 04와 같은 여섯(잠금 판). 키 셀 없음. 파일 위치 셀은 01절 셀 글 그대로(생성기 `__main__`에서 `author_01.py`와 문자열 대조 `assert`). 도구 파일은 가져오지 않음(제목 셀에 「앞 챕터에서 배운 함수는 이 절에서 쓰지 않아, 도구 파일도 가져오지 않습니다」).
- 본문 b1~b10 새로(b3 = 04절 / Ch 25 01·02 / 01절·02절 / Ch 6 04·Ch 2 12·Ch 15 02 · b10 = FastAPI SSE·FastAPI Stream JSON Lines·WHATWG HTML Server-sent events·MDN EventSource()·Python asyncio.timeout·Python 비동기 생성기 함수(여섯 모두 2026-09-29 WebFetch) + 설치판 소스 행 + 실습 파일 행). 복습 넷 → **다섯**(해설 포함). meta 「강의 1.25h | 실습 2.75h」 그대로(챕터 시수 합 유지).
- 그림: Mermaid **4장**(05-1 b4 · 05-2 b4 · 05-3 b5 · 05-4 b6 — viewBox 폭 271·217·498·589, 모두 868 이하) + 삽화 **1장**(05-5, 재생성 1회). 옛 `{{svg:05-흐름}}` 토큰 제거, 옛 그림 파일 셋(`05-흐름.svg·.excalidraw·.caption.md`)은 그대로.
- 설명만 고친 뒤(유니코드 번호 표현·b6 문서 근거·b3 한 글자) `mdpatch.py`로 생성기·노트북 마크다운·`_src`를 함께 고침 — 코드·출력·`executed_at` 그대로(A 사본과 `cmpout` 25/25·`outputs_sha256` 같음), 생성기 `cells()`와 노트북 셀 글 53/53 같음 확인.

## 정한 SSE 말 (handoff 용어 표에 덧붙임)

| 말 | 뜻 | 코드에서 |
|---|---|---|
| **SSE(Server-Sent Events)** | 서버가 한 응답 안에서 사건을 하나씩 글로 적어 보내는 형식 — 본문 종류 `text/event-stream` | `response_class=EventSourceResponse` |
| **SSE 사건** | SSE 응답 본문에서 빈 줄로 끝나는 줄 묶음 하나(줄마다 칸 이름·쌍점과 공백·값). 제목의 「이벤트」 → 본문은 이 말. **04 「스트림 사건」(메서드가 내놓는 파이썬 값)과 가름** — `chat_stream`은 스트림 사건 하나를 SSE 사건 하나로 바꿔 보냄 | 코드 이름 `event`·`ServerSentEvent`·줄 머리 `event:`는 그대로 |
| **사건 이름 · 사건 번호 · 칸 `data`** | SSE 사건의 칸 `event`(`token`·`done`, 06의 `error`) · 칸 `id`(`sse-1:0` — 스레드 이름 + `:` + 0부터 센 자리, `done`에는 없음) · 칸 `data`(늘 JSON 글, 한글은 `\u` 유니코드 번호) | `item.event`·`item.id`·`item.data` · `parse_sse` 딕셔너리 키 |
| **비동기 제너레이터 함수** | 정의 줄 `async def` + 몸통 `yield` — 부르면 비동기 제너레이터(04 말), 꺼낼 때마다 다음 `yield`까지 실행 | `chat_stream`·`stream_answer` |
| **JSON 줄 형식(JSON Lines)** | 한 줄에 JSON 글 하나 — 본문 종류 `application/jsonl`(`response_class` 없이 `yield`만 쓴 처리 함수) | 실행 2 |
| **본문 종류** | 응답 머리 칸 `content-type`의 출력 라벨(「미디어 타입」 대신) | `response.headers["content-type"]` |
| (이어 씀) 「필드」 → 「칸」, 「헤더」 → 「응답 머리」·「요청 머리」, 「식별자」 → 「사건 번호」, 「파싱」 → 「칸으로 나누기·읽기」, 「직렬화」 → 「JSON 글로 적기·바꾸기」, 「프록시」 → 「중간 서버」, 「keep-alive ping」 → 「쉼 신호 줄 `: ping`」 | — | — |

- 「조각」 0 · 「스트림 청크」는 b3의 Ch 25 02 되짚기 한 번뿐(09 몫 유지) · 「진행 값」·「스트림 사건」·「비동기 제너레이터」·「비동기 반복」은 04 말 그대로.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-05/exp/`)

- `p1_shape.py`(설계 확인): 앱 `POST /v1/chat/stream` 본문 글 전문(`repr`) · 빈 줄로 나눈 글 8·끝 빈 글 · `chat_stream` 직접 부르기 `async_generator`·`ServerSentEvent` 일곱 · 작은 판 두 앱 — 실행 1 본문 = 앱 본문 `True`, 실행 2 `application/jsonl`·줄 일곱·키 여섯 · OpenAPI `text/event-stream` + `itemSchema`(칸 넷) ↔ `application/jsonl` + `itemSchema: {}` · 앱 `openapi()`의 스트림 응답 = 실행 1과 같은 모양.
- `t_timeout.ipynb`(설치판 ipykernel 7.3.0 커널): 셀 맨 위 `async for`로 `chat_stream`(안에 `asyncio.timeout`)을 꺼내도 됨 — `asyncio.timeout`은 작업(task) 안에서만 되는데, 노트북 셀 맨 위에서도 PASS·일곱 값.
- `p3_scene.py`(노트북 장면 전체 스물넷 셀, 셀 맨 위 자리는 `asyncio.run` 안 비동기 함수, 5번): 출력 md5 **5/5 같음**(`8e59350ed17378d79c1506926cbb5262`), 표준 오류 0.
- `p6_next.py`(06 인계용, 5번, 출력 md5 5/5 `ea534422…`): 아래 「§05 → §06」 사실 — 시간 제한 0 재정의 스트림 · `Last-Event-ID` 다섯 경우 · `logger.exception` Traceback 25줄.
- 설치판 소스(fastapi 0.135.0 — `__init__.py` 3행): `sse.py` 20행 `EventSourceResponse`(23~27행 「Works with any HTTP method」)·42행 `ServerSentEvent`(칸 `data`·`raw_data`·`event`·`id`·`retry`·`comment`)·146~214행 `format_sse_event`(199~207행 차례 event → data → id → retry, 212~214행 끝 빈 줄)·218행 `KEEPALIVE_COMMENT = b": ping\n\n"`·222행 `_PING_INTERVAL = 15.0` · `routing.py` 491~522행 SSE로 바꿈·507행 `json.dumps(jsonable_encoder(item.data))`(기본 `ensure_ascii=True` → 한글 `\u` 번호)·572·574행 응답 머리 둘·576~608행 JSON 줄 형식·926~931행 `is_sse_stream`·`is_json_stream`(`response_class`로 가름) · `openapi/utils.py` 361~375행 jsonl·376~395행 SSE `itemSchema` · `applications.py` 1162행 `add_api_route`·2315행 `post` → 2667행 `self.router.post` · `routing.py` 2546행 `post` → 2901행 `api_route` → 1375행 `api_route`의 데코레이터가 1406행 `self.add_api_route` · starlette 1.6.0 `testclient.py` 296·341·343~344·351·365행(본문을 `BytesIO`에 모은 뒤 `ByteStream`으로 응답).
- 공식 문서(2026-09-29 WebFetch): FastAPI SSE — 「To stream SSE with FastAPI, use yield in your path operation function and set response_class=EventSourceResponse」·「SSE works with any HTTP method」·「The data field is always encoded as JSON」·ping 15초·`Cache-Control: no-cache`·`X-Accel-Buffering: no`·「Added in FastAPI 0.135.0」 · FastAPI Stream JSON Lines — `response_class` 없이 `yield`면 `application/jsonl`, 힌트 없으면 `jsonable_encoder`, 「Added in FastAPI 0.134.0」 · WHATWG HTML Server-sent events — 빈 줄에서 사건을 내보냄·첫 쌍점 앞이 칸 이름·앞 공백 하나 뺌·`event`·`data`·`id`·`retry` 외 무시·쌍점으로 시작하는 줄은 주석·UTF-8 · MDN `EventSource()` constructor(최종 수정 2025-06-23) — 매개변수 `url`과 `options.withCredentials`뿐. **MDN 두 쪽 모두 「GET만 보낸다」·「요청 머리를 못 정한다」를 글로 적지 않음** → 본문은 「생성자가 주소와 선택 칸 `withCredentials`만 받는다 → 요청 본문과 요청 머리를 적을 자리가 없다」로만 씀(README의 「EventSource는 POST 본문과 인증 헤더를 다루지 못하므로」와 같은 뜻, 문서가 적은 범위로 한정) · Python 3.12 `asyncio.timeout`(3.11에서 들어옴, 넘기면 작업 취소 → `TimeoutError`) · Python 3.12 언어 참조 6.2.9.3 Asynchronous generator functions.

## 실행 (새 커널)

| 실행 | 자리 | 키 | 결과 |
|---|---|---|---|
| 시험 tryA(`/tmp/ch30-05/tryA` 사본, `execute.py` 기본 `--cwd` = 프로젝트 맨 위, `PYTHONPATH` = `notebooks/`, 08:53:12Z) | 루트 커널 | `OPENAI_API_KEY` 지움 | PASS 25셀 |
| 시험 tryB(사본, `--cwd` 실습 폴더 `notebooks/`, `PYTHONPATH` 지움, 08:53:21Z) | 학생 커널 | 지움 | PASS 25셀, tryA와 셀별 25/25·`outputs_sha256` 같음 |
| **A**(`run_section.sh … 05`, `executed_at` 2026-09-29T08:53:39.632140Z) | 루트 커널 | 지움 | PASS 25셀(그림 첨부 단계에서 멈춤 — 05-1 PNG 전) |
| **B**(A 사본 `/tmp/ch30-05/B`, `uv run … execute.py --cwd notebooks/`, `PYTHONPATH` 지움, 08:53:58Z) | 학생 커널 | 지움 | PASS 25셀 |

- **A ↔ B 셀별 출력 글자 25/25 같음**(이은 글 해시 `653b3caecff3da96` 같음), `code_sha256` `662e8a3e9119dd8a0fff854ed51daebb3c356aab56fa4ba5de4857d1fc2ed9a0` 같음. **`outputs_sha256`은 다름**(A `85e481f72c0f433f484ea2fd050395a4b798177c7acfd686a7d1e7543835525e` · B `b85bad7480cfcb43d4a36bd51794b220bd4eba086942a4efa5236086304c4bde`) — 까닭: 설치 셀 [1]의 표준 출력 스트림이 A는 66 + 100글자, B는 149 + 17글자 자리로 둘로 나뉨(합친 글은 같음, 02·03 선례). 요청 0이라 셀 [2]~[25] 출력 구조까지 같음. 초 값을 출력하는 셀 없음.
- 그 뒤 `--no-exec` 넷(렌더·첨부·빌드)과 `mdpatch` 한 번에서 노트북 코드·출력·`executed_at` 그대로(첨부·마크다운만 바뀜 — A 사본과 `cmpout` 25/25·`outputs_sha256` 같음) — 노트북 파일 **`ef770d54660155a40a86ece1ba5093833fc2d303587710825be62b8cf046c1b5`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에 새로 생긴 파일은 노트북 05뿐(`find -newer` — `agent_service/__pycache__` 그대로, pyc 0) · `.failure.json` 0 · 노트북 표준 오류 출력 0(커널 TCP 경고는 실행기 쪽) · 설치 셀 출력에 pip 안내 한 줄.
- **모델 요청 0** · 서버 프로그램·포트·자식 프로세스 0 · 남은 프로세스 0(`ps` — uvicorn·ipykernel·jupyter 없음).

## 앱 파일 고침 · `app.openapi()` 대조 · `tests/`

- **05는 앱 파일을 고치지 않음.** 2절이 `app.py` 95~124행을 글로 읽어 출력만 함 — 96행 f-string·101~106행 힌트·106행 `-> AsyncIterable[ServerSentEvent]`·117행 `index += 1`·119행 `except Exception`은 출력된 앱 파일 줄로 두고, 결과 읽기는 99·109·113·114~118행만 풂(117행은 「자리 번호를 하나씩 키움」). 고치면 `app.openapi()`·02(`Depends(` 줄·`chat` 정의 줄)·03(`chat` 소스)·04(줄 번호 110·111·134·136)·05(95~124행) 출력이 함께 바뀜.
- 확인: `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 · `pytest -q -p no:cacheprovider` **6 passed, 1 warning** · 앱 파일 해시 `app.py` `3455d405…`·`agent.py` `a6c42e63…`·`live_agent.py` `586a6a69…`·`schemas.py` `ed77b197…`·`__init__.py` `1c7d7aef…`·`tests/test_app.py` `f8611741…` 그대로. `openapi.json`·생성 SDK 손대지 않음.

## 도구 파일 — 덧붙이지 않음

- **만들지·덧붙이지 않음**: 이 절은 앞 챕터에서 배운 함수(`positions_of`·`mode_order` 등)를 쓰지 않음 — 모드 목록을 받지 않고 SSE 글을 다룸. 그래서 `from serve_tools import …` 줄·고정 세 문장·커널 폴더 문장도 없음. 도구 파일 `notebooks/serve_tools.py`는 04 판 그대로(`e0a3a382260364dcd233abdc6e9e583600aca110da1aee056b6e2d5d08d7e0bb`, 생성기가 읽기만 하고 해시를 출력). 공개 목록 두 곳도 그대로.
- 이 절이 **처음 가르친 함수 셋**(`split_sse(body_text)` — 빈 줄로 나눠 빈 글을 뺀 목록 · `parse_sse(sse_text)` — 줄마다 `split(": ", 1)`로 칸 딕셔너리 · `count_event_lines(body_text)` — `event: `로 시작하는 줄 수)은 **노트북에 둠**(규격 §2-7 3번). 06이 다시 쓰면 06이 04 대조 사슬(`author_04.TOOLS`로 시작·`strip_later_imports`·쓰기 가드·`--tools-copy`)로 옮김 — 주석 첫 줄 모양 「# Ch 30 05절에서 배웠습니다 — …」.

## 고친 틀린 사실

- b3 「04절에서 astream 청크를 읽었고 Ch25에서 진행 이벤트와 토큰 이벤트를 분리했습니다」 → 04절(진행 값·`async for`·앱 110·111행) + Ch 25 01(스트림 사건·진행 값) + Ch 25 02(한 실행에서 모드 셋, 사건 짝의 모드 이름으로 진행 값과 스트림 청크를 가름·모드 차례) + 「이 절의 SSE 사건은 모드 이름 대신 칸 `event`에 사건 이름을 적어 가름」.
- b4 비유 「택배 상자에는 종류, 번호, 내용이 적힌 운송장」 → 챕터 계열 「화물 열차와 번호판 차량」(이름판 = 사건 이름·번호판 = 사건 번호·짐 = 칸 `data`·번호판 없는 끝 칸 = `done`) + 비유와 다른 점 셋.
- b4 「로컬 TestClient 성공은 운영 프록시를 검증하지 않습니다」·「네이티브 응답은 캐시 방지, 프록시 버퍼링 방지, 연결 유지 ping을 처리합니다」 → 출력으로 본 응답 머리 둘(`no-cache`·`no`)과 문서 설명으로 한정, ping은 「설치판 소스·문서로만, 이 절 응답에는 없음」.
- b4 「서비스 설계 판단」(progress·출처·여러 서버 인스턴스·완료 사건의 사용량) · b7 「식별자에는 개인정보나 토큰을 넣지 않습니다」·「손상된 이벤트도 처리합니다」 → 실행하지 않은 설명이라 뺌. 사건 번호에 스레드 이름이 들어간다는 사실만(출력 `sse-1:0`).
- b6 「이벤트 필드 설계가 유지됨을 보여 주지만 실제 모델의 토큰 경계는 측정하지 않습니다」(질문 둘의 token 수) → 인자 하나만 바꾼 실험의 결과(종류·개수)로.
- 「이벤트」·「필드」·「엔드포인트」(옛 판에 없음)·「경로」(옛 판 0 — 새로 쓰지 않음) → 위 「정한 SSE 말」. 도식 읽기 틀 색 문장 → 그림마다 새로, 보라 0·빨강 0.

## 그림

- Mermaid 넷: 설계표 `05-figures.md`(렌더 전 작성) → `.mmd`·캡션 → 렌더 → PNG 넷을 직접 열어 확인(`.cache/ch30-05-view/` 사본): 끊긴 라벨 0(긴 코드 처음부터 `<br>`), 05-3·05-4 두 갈래·두 칸이 나란함(04-4 본 — `~~~` 안 씀), 색은 설계표대로(초록 요청 본문·앱 줄 / 파랑 우리 함수·바꾼 값 / 노랑 출력 / 회색 라이브러리), 보라 0·빨강 0. 다시 렌더한 것 없음(05-3 도식 읽기에만 「본문을 끝까지 모아 받음은 설치판 starlette 소스로 본 동작」 한 문장을 더함 — 파란 우리 줄 상자라 노랑 규칙과 어긋나지 않음). 라벨 숫자는 사건 번호 `sse-1:0`·`sse-1:5`와 본문 종류 글뿐(출력에 있음).
- 삽화 05-5: `05-5-…prompt.md` 상태 줄 — **2차 job `c1305011-96f8-4680-af9d-b00658587772` 채택**(재생성 1회 — 1차 `262db619-003e-4c20-9757-5b23ae54e936`은 하늘색 칸이 붙어 셋으로 그려져 「칸 하나 = 사건 하나」가 안 읽히고 양끝 칸이 잘림, 흰 여백 약 25% → 탈락) · 거래 2026-09-29T08:56:21.752543Z·08:57:46.544682Z 「Nano Banana Pro −2」 두 줄(**이 절 몫 4크레딧**, 잔액 2283 → 2279, 앞 거래 08:20:53Z는 Ch 30 04) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 저장 PNG `eb733ea5…`(1100 × 614)와 채택 결과를 다시 받아 줄인 그림 픽셀 대조 bbox `None`·최대 차이 0 · 저장본 사본을 열어 하늘색 짐칸 여섯(칸마다 초록 네모 판 하나·흰 동그라미 판 하나)·연한 주황 끝 칸 하나(갈색 네모 판 하나, 동그라미 판 없음)·기관차 없음을 세고 그림 읽기를 씀. **거의 흰 가로줄 6 / 614**(04 채택본 423) — 비스듬한 구도(handoff 권고). 01~04 소품 되풀이 없음, **번호판을 처음 그림**(글자·숫자 없는 흰 동그라미).

## 검사

- `run_section.sh … 05 --no-exec`: 렌더 넷 · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 138 code cells (max 14 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `05-POST-SSE-이벤트-설계.html`(`79fb9423…`): `{{` **0** · `[[` 0 · 인라인 SVG 4 · 삽화 JPEG 1 · 노트북 셀 25.
- `pack.py … 05` → `qa/upgrade/review-pack/05-POST-SSE-이벤트-설계.md`.
- 보호 파일 255개: `manifest-changes.md` 「05절 뒤」에 덧붙임.

## 완료 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

`grep -rn 'Ch *30' textbook/part1 part2 part5 part6 part7 --include=*.html | grep -v ch30-fastapi`(최종 HTML·`_src`만 봄, `qa/` 옛 사본 뺌):

| 문장 | 판정 |
|---|---|
| Ch 25 04 b8 「Ch 30 04절은 모드 custom의 사건을 비동기 메서드 astream으로 받아 이어 붙입니다. 09절은 모드 messages의 스트림 청크를 같은 메서드로 받아 서버 응답으로 보냅니다」 | 05와 무관(04 참·09 몫) — 05는 모드 `custom`만 씀 |
| Ch 29 05 b8(01 슬러그 「요청과 응답의 모양」) | 05와 무관 — 참(01 끝남) |
| Ch 2 12 b8(1절·3절)·Ch 2 11 b8(2절)·Ch 2 `index.html` 「비동기 대기는 … Ch 30의 FastAPI에서 다시 사용」 | 05와 무관 — 참(05도 `async def`·`async for`를 씀) |
| Ch 1 01 과정 지도 「Part 7 서비스화와 배포 Ch 30~34」 | 참(구성만) |
| Part 7 소개 「Ch30의 요청·응답 형식에서 시작해 …」 | 참 |
| Ch 31 01 b2·b3(「Ch30에서 FastAPI 요청 함수·경로 함수를 비동기로」)·Ch 32 01·02·Ch 34 04 b3 | 글만(참 — 대기 챕터, 고치지 않음. Ch 31 01 b3 「경로 함수」는 Ch 30 말 「처리 함수」와 다름 — 04 기록 그대로) |

- 「SSE」·「Server-Sent」를 쓰는 완료 챕터 최종 `_src` 문장 없음(옛 Ch 25 사본 `part6/qa/language/ch25-*`에만 「Ch30에서는 … FastAPI SSE로 브라우저에 전송하고 연결 종료와 재접속」 — 최종본 아님).

## 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀 — `d05dc920…`) · 사용자 디스크 `.cache/ch30-05-view/`(그림 보기 사본 여섯 — 새로 만든 폴더). 공용 도구·규격·과정 문서·zip·검사 스크립트·앱 파일·도구 파일·공개 목록·Ch 31 이후 파일은 고치지 않음.

## 강사 확인 대상

1. 새 말 「SSE 사건」(제목 「이벤트」의 본문 말 — 04 「스트림 사건」과 가름)·「사건 이름」·「사건 번호」·「JSON 줄 형식」·출력 라벨 「본문 종류」(`content-type`).
2. 실험을 옛 「질문 길이별 token 수」에서 인자 `response_class` 하나로 바꾼 것 · 같은 함수를 두 번 잇으려고 데코레이터 줄 대신 `add_api_route`를 쓴 것(이 절 실험에서만, 실습 앱은 데코레이터 줄).
3. 비동기 생성기 `yield`의 A 트랙 첫 풀이 자리(05) · `asyncio.timeout`은 풀이만 하고 실행하지 않은 것(06 몫).
4. 도착 차례를 보이는 서버 프로그램(uvicorn 자식 프로세스)을 쓰지 않은 것 — 이 절은 응답 글에 적힌 차례만 주장.
5. MDN이 「GET만」을 글로 적지 않아, 브라우저 `EventSource` 설명을 「생성자가 주소와 `withCredentials`만 받는다」로 한정한 것.
6. 「노드」 말(03·04와 같음) · 코드 양 30 → 158줄(셀 4 → 25).

## 남은 것 (마감 몫)

- `part7-practice.zip`에 05 노트북 새 판 반영(마감 때 한 번) · 05는 Part 7 묶음 실행 검사 대상 아님(01만).
- 옛 그림 `05-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-05-05.json` · 기기 `/tmp/ch30-05/`(사본·실험·삽화 원본 둘·생성기 조각, 약 13MB) · 사용자 디스크 `.cache/ch30-05-view/`(보기 사본 여섯).
