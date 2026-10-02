# 04절 진단과 개선 기록 — 백오프 큐 동시성 (paired · 모델 없음)

- 작업일 2026-09-30(UTC 00:3x~01:2x). 생성기 `qa/upgrade/author_04.py`(`ed37ec90…`, 84,949바이트). 규격 `textbook/QUALITY-UPGRADE.md` §2·§2-7·§3·§4·§5-3·§5-4·§6·§8. 1차 지시서 `qa/upgrade/handoff.md` 「챕터 공통」·「§03 → §04」(12항). 설치판 모양 확인 `qa/upgrade/probe/04-shape.md`.
- 서비스 요청 **0**(모델 객체는 가짜 키 `not-a-real-key` + `base_url` = `127.0.0.1` 연습용 서버) · 키 셀 없음 · 모든 실행은 `env -u OPENAI_API_KEY`·`PYTHONDONTWRITEBYTECODE=1`. 삽화 4크레딧(재생성 1).

## 1. 게이트 전후

| | 코드 셀 | 코드 줄 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 5 | 50 | 70 | 5 | 9 | 5 | 0 | 7 | 9 | 3 | **38** |
| 그림 전(`gates-wip-04-04.json`, 첫 실행 전) | 24 | — | 405 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3 |
| 수정 뒤(`gates-wip-04.json`, `--no-exec`) | **24** | 150 | **427** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 코드 줄은 `count_code.py`(주석·빈 줄·`%` 줄 뺌). 준비 셀 밖 셀 최대 10줄(`INQUIRIES` — 문의 글 목록 일곱 줄 포함) · 함수 본문 최대 7줄(`ask_and_count`) · 호출 깊이 최대 2(AST 따로 — `.cache/ch34-01/tools/pregate.py`).
- AST 따로: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·별표 풀기·`+=`·대입 풀기·`while`(노트북)·`raise`·클래스·데코레이터·힌트·기본값 매개변수·`key=`/`reverse=`·`set`·`next`·`enumerate`·`zip`·`sum`·`min`·`all`·`any`·`isinstance`·`getattr`·노트북 딕셔너리 `.get`·한 글자 변수·비동기 **0건**. 도구가 잡은 다섯은 의도한 것: `try` 둘(오류 이름 하나만 받는 정의 셀 `send_once`·`ask_and_count` — 규격 L3, Ch 6 05 모양) · `max` 둘(한꺼번에 처리 중이던 수의 가장 큰 값 — 결과 읽기에서 한 문장) · `dict.get` 하나는 **`httpx.get`**(딕셔너리 `.get` 아님, 거짓 양성).
- 과정 금지어(산문, 코드 백틱 뺌): 걸린 것은 슬러그·링크 주소(`…폴백….html`·`…스키마.html`·`04-백오프-큐-동시성`)와 「프로그램」 속 「로그」(거짓 양성)뿐. 「백오프」·「큐」·「동시성」은 **제목 풀이 한 곳**(노트북 1절 첫 단락·본문 b2 둘째 단락)과 「(지수 백오프)」 괄호에만(01·03 선례 — 강사 확인). 「지터」·「배치」·「헤더」·「엔드포인트」·「미들웨어」(산문)·「되돌리다」·「최대」 0. 사용자가 금지한 표현(과정 규칙) 0건(생성기·노트북·본문·그림·서버 파일·기록 파일).

## 2. 수정 전 주요 문제 (옛 판 2026-09-14 저장)

1. 커널 안 스레드 서버 — `BaseHTTPRequestHandler`를 이어받은 클래스 `Handler`, 클래스 변수 `count`로 **처음 두 요청만 429, 그 뒤 200**(정해 둔 성공을 주는 흉내 서버).
2. **Before가 After 결과를 정함**: 서버 수가 커널 전체에 하나라 Before의 `urlopen` 한 번이 첫 429를 써 버리고, After(`fetch_with_backoff`)는 429 한 번 뒤 200 — After만 따로 돌리면 결과가 달라짐(같은 조건 비교 아님).
3. `asyncio.Queue` 6 + `Semaphore(2)` + 일꾼 셋(`global`·`while`·세미콜론·한 줄 다중 대입) · 작업 대신 `asyncio.sleep(0.03)` · 기본값 매개변수·`raise`·지터 `random.uniform` · 대기 `[0.052]`를 출력(흔들리는 값) · 「대기 발생 작업: 6」(`perf_counter` 차는 늘 0보다 큼 — 뜻 없는 값) · `server.shutdown()` 뒤 정리 확인 없음.
4. b6 「응답 헤더의 재시도 안내와 SDK의 내장 재시도 정책도 함께 확인합니다」 — 확인하지 않은 말 · b3에 Ch 6 05·Ch 22 04 이음 없음 · 옛 b4 그림이 「로컬 429 응답」을 빨강으로 칠함(과정 색 규칙 위반) · 결과 읽기 0 · 첫 줄 주석 0 · 그림 설계표 0 · 금지어 「Rate limit」·「동시성」·「세마포어」·「지터」·「큐」·「측정」·「최대」·「헤더」·「반환」 등.

## 3. 틀린 사실과 고친 것

| 옛 글 | 사실 | 고친 곳 |
|---|---|---|
| b6 「실제 운영에서는 응답 헤더의 재시도 안내와 SDK의 내장 재시도 정책도 함께 확인합니다」 | 옛 노트북은 SDK 재시도도 머리도 쓰지 않음 | 3절 출력(클라이언트 `max_retries: 2`·서버 요청 3) + 설치판 소스 행(b4·b10 — `_constants.py` 8행, `_base_client.py` 763·801·808·811·815·847행) · 머리 `Retry-After` 따르기는 「노트북에서 실행하지 않았습니다」 |
| b3 「Ch 16에서는 호출 한도와 재시도 함수를 직접 만들었습니다」 | Ch 16 04 호출 한도는 **앱이 정한** 상한(요청 제한과 다름) · 재시도 함수는 Ch 16 05(실패 흉내) | b3 표·문단: Ch 6 05(곱은 셈만, 429 실행 안 함) · Ch 22 04(「곱해질 수 있습니다」) · Ch 16 04(호출 한도 ≠ 요청 제한) · Ch 16 05(실패 흉내) · Ch 28 03 · 02 · 03 |
| b3 「Ch 30에서는 FastAPI 비동기 요청 처리를 배웠습니다」 | 참(Ch 30 요약 246행) — 새 판은 비동기를 쓰지 않음 | 「Ch 30에서는 FastAPI 처리 함수를 비동기로 써서, 요청을 받는 서버 쪽을 만들었습니다 … 비동기 문법은 쓰지 않습니다」 |
| 옛 b4 그림 「빨간 상자의 로컬 429 응답」 | 받은 429는 Before 결함 결과가 아님 | 새 그림: 받은 오류·429는 노랑, 빨강은 Before 결과(서버 요청 아홉 번) 둘뿐 |
| b9 「통제된 로컬 서버에서 HTTP 429 처리만 재현」 | 옛 서버는 200도 보냄 | 연습용 서버는 **늘 429만** — 흉내임을 본문·그림·서버 파일에 밝힘 |
| (기록) handoff·`probe/01-probe.md`·`probe/03-probe.md` 「`openai/_constants.py` 7행」 | 설치판 openai 3.13.0에서 `DEFAULT_MAX_RETRIES = 2`는 **8행**(7행은 `DEFAULT_TIMEOUT`) — 이 절에서 다시 확인(03 진단과 같음) | 04 본문·노트북은 8행. **01·03 학생 글(`_src`·노트북)에는 이 행 번호가 없음**(`grep` 0 — 강사 확인 대상 아님). 흔들림 확인 기록 파일은 고치지 않음 |

## 4. 설계 (handoff §03 → §04 12항 그대로)

- **Before = 겹친 다시 보내기**(실제 결함, 매번 같음): 과정 표준 설정 모델 객체(`base_url` = 연습용 서버, 가짜 키, `max_retries` 적지 않음 → 클라이언트 2)에 `with_retry(retry_if_exception_type=(ModelRateLimitError,), stop_after_attempt=3)` → **서버 요청 9**(빨강). **After** = `max_retries=0` + 같은 `with_retry` → **3**. 예시 부분(3절)에서 모델 객체 한 번의 요청 수 3·1을 먼저 세고, Before·After 뒤에 곱셈 대조(`3 × 3 = 9`·`1 × 3 = 3` 모두 `True`).
- **연습용 서버** `labs/…/notebooks/always_429_server.py`(`3f25ebd8…`, 1,927바이트): 함수 `app` 하나 + `wsgiref.simple_server.make_server("127.0.0.1", 포트, app)`, 클래스·데코레이터·f-string 0, 함수 본문 8줄. **모든 응답이 429**(답 글 없음 — 오류 JSON `{"error": {"message": "연습용 서버는 늘 429를 보냅니다.", "code": "practice_429"}}`), 주소 끝 `/chat/completions`만 셈 · `/reset`은 0으로 맞춤 · `/count`는 세지 않고 알려 줌 · 센 수는 머리 `practice-count`. `retry-after`·`retry-after-ms`는 **보내지 않음**(SDK가 제 기다리는 시간 규칙을 씀 — 본문에 적음). 노트북은 자식 프로세스로 띄움(`stdout`·`stderr` `DEVNULL` — `wsgiref`가 요청마다 남기는 줄이 저장 출력에 들어가지 않게), Ch 28 규칙(띄우기 전 포트 빔 `wait_for_port(…, 1)` → `False` · 띄운 뒤 `poll() is None` · 끝 셀 `terminate()`·`wait(timeout=10)` → −15 · 포트 닫힘 `False`). 포트 58034는 코드에만(저장 출력에 포트·주소·임시 위치 0 — `grep` 확인).
- **셀마다 새로 셈**: 요청 셀은 모두 `httpx.post(base_url + "/reset")` → 부름 → `read_count(base_url)`(`/count`). 옛 판의 「앞 셀이 뒤 결과를 바꿈」 결함 고침.
- **값 바꿔 보기(After 쪽)**: 02 문의 글 다섯(글자까지 같음 — 생성기 `check_inputs()`)을 `RunnableLambda(ask_and_count).batch` — 설정 없음 → 한꺼번에 처리 중이던 수의 가장 큰 값 **5** · `config={"max_concurrency": 2}` → **2**, 서버 요청 **15** 두 번 모두, 받은 오류 5. 동기 `batch`(`async`/`await` 없음). `wsgiref`는 한 번에 한 요청만 처리하므로 동시 수는 **클라이언트 쪽 함수**가 셈(`active`·`peaks` 목록 — Ch 6 05 `ask_current_model`처럼 셀 바깥 이름을 씀). 문의마다 `with_retry`의 기다림이 있어 겹침이 생김. Python 3.12 기본 일꾼 수 `min(32, CPU 수 + 4)`가 CPU 하나여도 5라 「설정 없음 5」는 컴퓨터와 상관없이 같음(소스). 02 b4 마지막 단락(메서드 `batch` ≠ 일괄 처리)을 가리킴. 빨강 없음.
- **말**: 요청 제한(rate limit — Ch 6 05) · 다시 보내기(재시도 — Ch 6 05 「다시 시도」와 같은 뜻) · 새 용어 다섯(meta 「새 용어 5」): 연습용 서버 · 겹친 다시 보내기 · 기다리는 시간을 두 배씩 늘리기(지수 백오프) · 한꺼번에 보내는 수 · 대기열 — 뜻·일상 예·코드 모습 세 문장. `InMemoryRateLimiter`를 쓰지 않아 「허락 표(토큰)」는 꺼내지 않음. 대체 모델은 말하지 않음(03 b7과 부딪힐 자리 없음). 「폴백」 0.
- **흔들리는 값**: 기다린 초·걸린 초만 — **출력하지 않음**(결론·라벨·`assert` 0). 노트북의 `assert`는 준비 셀 셋(실습 폴더 찾음·포트 빔·서버 준비/살아 있음)뿐.

## 5. 설치판 모양 확인 (`probe/04-shape.md`)

- 설계 초안(서버 초안 · 문의 여섯) 여섯 번 같음(00:3x + 00:37:17Z~00:39:32Z 다섯 번 기록 `probe-04.jsonl`): 3 · 1 · **9** · **3** · 6/18 · 2/18 · 종료 −15, 표준 오류 0바이트. 걸린 초만 흔들림(Before 7.73~8.61초 등 — 기록만).
- 최종 모양(생성기가 쓴 노트북 사본, `/tmp/ch34-04/tryA`) **다섯 번 셀별 24/24 같음**(01:00:58Z~01:03:45Z, `code_sha256` 모두 `85149d05…`).

## 6. 실행

- 첫 실행 전: `--nb-copy` 사본으로 `pregate.py`(G1~G6 0) → 사본 실행 tryA(PASS) → 실습 폴더에 쓰기(`author_04.py`) → `upgrade_gates.py --label wip-04 --section 04`(G1~G6 0 · G7 3 — `gates-wip-04-04.json`).
- **새 커널 A**(`env -u OPENAI_API_KEY … run_section.sh … 04`, 루트 커널, `executed_at` **2026-09-30T01:04:46Z**) — PASS 24셀, `code_sha256` `85149d05fc2b…`, `outputs_sha256` `19201b0a9600…`. 그림 첨부 단계에서 멈춤(실행·저장은 끝남, 사본 `.cache/ch34-04/pre/A-04.ipynb`).
- **새 커널 B**(`author_04.py --nb-copy /tmp/ch34-04/B`, `execute.py --cwd labs/…/notebooks`, `env -u PYTHONPATH -u OPENAI_API_KEY`, **01:05:31Z**) — PASS 24셀, `code_sha256` 같음, `outputs_sha256` `a835adab6805…`, **셀별 출력 글 24/24 같음**(`cmpout.py`). 해시 차이는 첫 셀 `%pip` 출력이 스트림 둘로 나뉜 것뿐(03 진단과 같은 현상). B는 학생 자리(`notebooks/` 커널, `PYTHONPATH` 없음)에서 도구 파일 04 판과 서버 파일을 찾음.
- 그 뒤 마크다운만 `mdpatch.py` 두 번(「시도 3번까지」 → 「시도 세 번까지」 그림 alt 한 곳 · Ch 6 05 노트북 7절 문장 바로잡기) → `--src-only` → `run_section.sh … --no-exec` 세 번 — 노트북 코드·출력·`verification`은 A 그대로. 생성기 `cells()`와 실습 폴더 노트북 셀 53개 글이 모두 같음(`--nb-copy` 대조, 마지막 01:1xZ).
- 실행마다 남은 연습용 서버 프로세스 0 · 127.0.0.1:58034 대기 0(`ps`·`ss`) · 실습 폴더 `__pycache__` 새로 생긴 것 0(`.venv` 밖 `find`).

## 7. 교재 출력 값 (A = B, 매번 같음)

| 셀 | 값 | 자리 |
|---|---|---|
| 6 연습용 서버 확인 | 상태 코드 `429` · 머리 `practice-count` `0` · 오류 글 | 결과 읽기·그림(04-1) |
| 10·12 모델 객체 | `max_retries` None/클라이언트 `2` · `0`/`0` | 결론·그림(04-2) |
| 11·13 한 번 부름 | `OpenAIRateLimitError` · `429` · 서버 요청 **3** · **1** | 결론·그림(04-2) |
| 15·16 Before | 서버 요청 **9** · 3 × 3 = 9 `True` | **빨강**(04-3·04-4) |
| 18·19 After | 서버 요청 **3** · 1 × 3 = 3 `True` · Before ÷ After `3` | 노랑(04-4) |
| 22·23 값 바꿔 보기 | 받은 오류 5 · 한꺼번에 처리 중이던 수 **5** → **2** · 서버 요청 **15** 두 번 | 노랑(04-5) |
| 24 서버 끄기 | 종료 코드 `-15` · 포트 열림 `False` | 결과 읽기 |

## 8. 서비스 요청 수와 비용

- OpenAI 서비스 요청 **0**(노트북·확인·새 커널 모두 — 요청은 `127.0.0.1` 연습용 서버로만). 요금 0. 키 값을 읽거나 출력한 일 0(노트북은 `.env`를 읽지 않음, 실행 환경에서 `OPENAI_API_KEY`를 지움).
- 연습용 서버가 받은 요청: 노트북 한 번 = 3 + 1 + 9 + 3 + 15 + 15 = 46(+ 센 수 맞추기·묻기 요청 — 세지 않음).

## 9. 실습 폴더 파일 쓰기 0

- 노트북 코드는 파일을 쓰지 않음. 이 절에서 바뀐 실습 폴더 파일은 대상 노트북 `04-백오프-큐-동시성.ipynb`(`84a8c57e…`) · 도구 파일 `cost_tools.py`(02 판 → 04 판) · **새 서버 파일 `always_429_server.py`**(생성기가 씀, 공개 목록 두 곳에 줄) 셋. 옛 `runs/` 셋·`data/` 셋 해시 그대로.

## 10. 도구 파일 `labs/part7/ch34-cost-rate-limits/notebooks/cost_tools.py` — 04 판

- **04 판 `7de7225aa8801bb465b5013962128bce0688991d32b52c9b0cfc4aa88e32ff1b`**(4,330바이트) = 02 판(`72429dfa…`)의 머리 설명 + 가져오기 줄 `import json`·**`import socket`·`import time`** + 02 판 함수 다섯(글자 그대로) + **Ch 28 03절 `wait_for_port(port, limit_seconds)`**(Ch 28 03 노트북 셀 def~return·첫 줄 설명 주석 글자 그대로, 주석 `# Ch 28 03절에서 배웠습니다 — Ch 28 03절 노트북 셀의 같은 이름 함수를 옮겼습니다`). 이 절 노트북이 실제로 쓰는 앞 챕터 평범한 함수는 이 하나(포트 빔 확인·서버 준비·서버 끈 뒤 확인 세 곳) — Ch 28 도구 파일 `connect_tools.py`에는 없고 Ch 28 03 노트북에서만 가르친 함수.
- 대조 사슬(`author_04.check_tools04()` — 실행마다): `author_02.check_tools02()`(01 → 02 사슬) · 02 판 해시 · `strip_later_imports(04 판)`이 02 판·01 판으로 시작 · 함수 차례 여섯 · 가져오기 셋 · `wait_for_port` def~return 글자·AST가 Ch 28 03 노트북(`c1f22daa…` 고정) 셀과 같음 · 02 판 함수 다섯 def~return 같음 · 금지 문법 0(`while`은 `wait_for_port` 안 하나 — Ch 28 03 셀 그대로).
- 쓰기 가드: 없거나 01·02·04 판일 때만 쓰고, 04 판으로 시작하는 더 긴 판은 건너뜀. **`author_04.py --guard-check`로 확인**: 01 `write_tools()` → `skip` · 02 `write_tools()` → `skip` · 03 `check_tools03()` 통과 · 파일 해시 전후 같음(`7de7225a…`).
- 가져오는 절: 01(`estimate_cost`)·02(함수 다섯)·03(`estimate_cost`)·**04(`wait_for_port`)**. 04 준비 셀 결과 읽기에 고정 세 문장 + 커널 폴더 한 문장 + 실행 도구 한 문장.
- 공개 목록 줄은 01이 넣은 그대로(파일 이름 같음).

## 11. 문서·소스 확인 (2026-09-30)

- WebFetch: `https://developers.openai.com/api/docs/guides/rate-limits` — 「Rate limits are defined at the organization level and at the project level … vary by the model」 · 「unsuccessful requests contribute to your per-minute limit, so continuously resending a request won't work」 · `Retry-After`(예 56) · 「Each official OpenAI SDK automatically retries eligible `429` and `503` responses」 · 지수 백오프 + 무작위 값 권함 · `slow_down`(429)·`rate_limit_exceeded`는 사라지는 중. `https://docs.langchain.com/oss/python/langchain/models` — 「By default, models retry up to **6 times** for network errors, rate limits (429), and server errors (5xx)」 · 「Retries use exponential backoff with jitter」 · `batch()`와 `max_concurrency`. **안내(6) ↔ 설치판 출력(클라이언트 2·요청 3)** — 교재는 출력 기준, b7에 두 사실 함께.
- 설치판 소스 행(모두 이 절에서 다시 확인): openai 3.13.0 `_constants.py` 8행 `DEFAULT_MAX_RETRIES = 2` · 11~13행 `INITIAL_RETRY_DELAY = 0.5`·`MAX_RETRY_DELAY = 8.0`·`MAX_RETRY_AFTER_DELAY = 2 * 60` · `_base_client.py` 488~489행 `x-stainless-retry-count` · 753행 `_parse_retry_after_header`(763행 `retry-after-ms` 먼저) · 801행 0초 초과 120초 이하면 서버 대기를 따름 · 808행 `min(0.5 × 2^n, 8)` · 811행 `1 − 0.25 × random()` · 815행 `_should_retry`(817행 120초 넘으면 다시 보내지 않음·826행 `x-should-retry`·847행 429) · 1167행 `time.sleep` / langchain-openai 1.6.0 `chat_models/base.py` 594행 `OpenAIRateLimitError(openai.RateLimitError, ModelRateLimitError)` · 666행 변환 시 `response=e.response` 유지 · 838행 `max_retries: int | None = None` · 1371~1372행 / langchain-core 1.6.2 `runnables/base.py` 2101~2107행 `with_retry` 기본값(`wait_exponential_jitter=True`·`stop_after_attempt=3`) · 931·978행 `batch` → `get_executor_for_config` · `runnables/config.py` 672~673행 `max_workers=config.get("max_concurrency")` · `runnables/retry.py` 142~144행·186행 `reraise=True` / tenacity 9.1.4 `wait.py` 256~259·267~270행(처음 1초·두 배·무작위 0~1초) / Python 3.12.13 `concurrent/futures/thread.py` 146행 `min(32, (os.cpu_count() or 1) + 4)` · 154행 `queue.SimpleQueue()`.

## 12. 그림

- 설계표 `qa/upgrade/04-figures.md`(**2026-09-30T01:06:39Z**, 렌더 전에 씀 — `.mmd`는 그 뒤) · Mermaid **5장**: 04-1 다시 보내기가 놓이는 두 곳(viewBox 폭 267) · 04-2 모델 객체 한 번의 요청 수(685) · 04-3 Before에서 요청 아홉이 나오는 차례(274) · 04-4 두 곳과 한 곳의 다시 보내기(612) · 04-5 한꺼번에 보내는 수만 바꾼 두 실행(656) — 모두 868 이하, PNG를 열어 확인, 04-1·04-4·04-5는 자동 줄바꿈을 `<br>`로 미리 나눠 다시 렌더. **보라 0** · **빨강은 Before 결과 상자 둘뿐**(04-3·04-4 왼쪽) · 받은 오류·429는 노랑 · 연습용 서버 상자에 「늘 429를 보내는 연습용 서버」 · 소스로만 본 대기열은 회색 · 라벨에 기다린 초·걸린 초 없음 · 개수는 한글(세 번·아홉 번·열다섯 번·다섯·둘), 설정 값·상태 코드·주소는 숫자(게이트 G7 0). 노트북에는 04-1만 첨부(「오늘 볼 그림」).
- 삽화 **1장** `04-6-꽂는-자리-둘과-줄-선-배터리`(비유 계열 「충전 거치대와 배터리」의 「칸 수 제한」): **1차 job `a58166e5-05f7-4511-a42c-9558d050acd8` 탈락**(거래 2026-09-30T01:08:49.355202Z −2 — 충전기가 빵 굽는 기계처럼 보이고 배터리가 둥근 판처럼 보여 「배터리를 채운다」가 읽히지 않음) → **2차 job `c3c6d588-5c49-40a2-83a5-bbd45fdd7723` 채택**(재생성 1, 거래 01:09:57.552211Z −2). **이 절 4크레딧**(잔액 2239 → 2235, 생성 전 마지막 거래는 03절 00:14:54Z). `jobs_wait` 모델 표시 `nano_banana_2`(요청 `nano_banana_pro`, 거래 표시 「Nano Banana Pro」 — 기록만). 원본 `d3e191d4…`(2752 × 1536) → 저장 1100 × 614 `47429083ad70a0c15cdc1b5c431dad094c01e11e95bedf9ea336a6d78f753f29`, 거의 흰 가로줄 135/614. 결과 URL을 다시 받아 픽셀 대조 bbox `None`·가장 큰 차이 0 · 저장 PNG와 같은 보기 사본을 열어 셈: 크림색 충전기 · 꽂는 자리 **둘** 모두 산호색 배터리(은색 단자 뚜껑) · 앞면 큰 표시등 **둘 파랑** · 옆에 한 줄로 선 배터리 **셋**(작은 표시등 **꺼짐**) · 사람·글자·숫자·화살표·전선 없음. 설계와 다른 점(충전기가 배터리보다 큼·줄 선 배터리가 조금 짧아 보임)은 `.prompt.md`에.
- 캡션 파일 여섯이 생성기 `FIGn_CAP`·`ILLU_CAP`과 같음.

## 13. 검사

- `run_section.sh … 04 --no-exec`: 렌더 → 첨부 1 → 빌드 → `verify.py --chapter` **PASS 5 sections / 103 code cells (max 13 lines)** → 게이트 wip **G1~G7 0 PASS**(검사 문장 427 — 노트북 237·본문 190).
- 빌드한 `04-백오프-큐-동시성.html`(`a08ef897…`) `{{` 0건 · 도식 읽기 5 · 그림 읽기 1 · 다른 절 HTML(01 `b226aecb…`·02 `70053245…`·03 `e1c7bcb6…`·05)·`index.html` 바이트 같음(보호 파일 대조).
- `visual.cjs`는 이 절에서 돌리지 않음(챕터 마감 몫). `pack.py` → `qa/upgrade/review-pack/04-백오프-큐-동시성.md`.

## 14. 보호 파일 (`before-manifest.json` 191개)

- **같음 173 · 바뀜 18 · 없어짐 0**. 바뀜 18 = 03절 뒤 15 + 04에서 처음 바뀐 셋(04 `_src`·HTML·노트북) — 공개 목록 두 곳·`집필점검표.md`·`qa/verification.md`·노트북 계약은 03 뒤 해시에서 다시 바뀜. 표는 `manifest-changes.md` 「04절 뒤」. 옛 `runs/` 셋·05 파일·옛 그림(`04-rate-limit-flow.{svg,excalidraw}` 포함)·`index.html`·`chapter.json`·실습 폴더 README·잠금은 같음.

## 15. 챕터 밖 수정

- `textbook/part7/public-files.json`(서버 파일 한 줄, 정렬 자리 109행 — `collect_public_files.py`와 같은 셈을 메모리에서 해 결과가 같음(115줄), 스크립트는 실행 안 함, `ea0bd104…` → `4825cd14219acc655209b20649252d0ca90617f29a9cf99fb379258554f5a480`) · `textbook/_notebook/checks/notebook-contracts-part7-ch34-cost-rate-limits.json`(`verify.py --chapter`가 다시 씀, `e83756c5…` → `a56edaf5c9b877e2ad3c53aea795e65aace443ad6ac0e095c6762e2f1527c5ac`). 그 밖 챕터 밖 파일·공용 도구 고침 0. Ch 6 05·Ch 16·Ch 22 04·Ch 28 03·Ch 30 파일은 읽기만. **`part7-practice.zip`·`llm-practice.zip`·`final-artifact-hashes.json`은 다시 만들지 않음(마감 몫)**.

## 16. 완료 챕터가 Ch 34에 기대는 문장 (고치지 않음, 참·거짓만)

- `grep -rn 'Ch *34' textbook/part1 part2 part3 part5 part6 part7 --include=*.html`(ch34 밖): Part 7 소개(`_src/index.html`·`index.html`) 「Ch34의 사용량 관리로 이어집니다」 — **참**(04는 요청 수를 셈) · Ch 33 04(`_src`·HTML) 「Ch34에서 p95 계산을 더 자세히 다룹니다」 — 05(옛 판) 기준 **참**(04와 무관, 05 몫) · Ch 27 08 — 그림 base64 안 글자, **거짓 양성**.
- 이 절이 기대는 앞 챕터 문장은 본문·노트북을 열어 확인: Ch 6 05(클라이언트 `max_retries: 2` 출력 · `with_retry(retry_if_exception_type=…, stop_after_attempt=3)` · 「최대 3 × 3 = 9번」 셈 · 「노트북 7절은 안쪽에서 다시 시도하지 않는 모델(max_retries: 0)」 · 「요청 제한(429)·서버 오류(5xx)·인증 실패(401)는 이번에 실행하지 않았습니다」) · Ch 22 04(「시도 횟수가 곱해질 수 있습니다」) · Ch 16 04(「호출 한도 … 우리 코드가 정한 규칙」) · Ch 16 05(「실패 흉내」) · Ch 28 03(`wait_for_port`·`Popen`·`poll`·`terminate`·`wait`, 종료 코드 −15, httpx) · 02 b4 마지막 단락 · Ch 30 요약 246행.
- 03 b8·정리 「04절은 요청 제한(429)을 받았을 때 다시 보내는 횟수와 한꺼번에 보내는 수를 다룹니다」 — 새 04와 맞음(03 고치지 않음).

## 17. 강사 확인 대상

1. **연습용 서버는 흉내**: 이 절의 429는 제공자가 보낸 것이 아님(Ch 16 05 「실패 흉내」 선례). 결함 자체(겹친 다시 보내기 9)는 실제 설치판 코드 동작이고 매번 같음. 제공자의 실제 429·`Retry-After` 따르기는 실행하지 않음.
2. 제목 풀이 한 곳(노트북 1절·본문 b2 「제목의 백오프는 …」 — 01·03 선례).
3. 서버 파일을 `notebooks/`(노트북 옆)에 둠 — Ch 28은 실습 폴더 맨 위에 둠. 공개 목록 두 곳에 줄을 넣었고, 묶음 다시 만들기는 마감 몫.
4. 새 용어 meta 「새 용어 5」(옛 판과 같은 수 — 챕터 합 22 그대로).

## 18. 남은 것과 지우지 않은 것 (삭제 금지 — 기록만)

- 기기 `/tmp/ch34-04/`: `probe.py`·`always_429_server.py`(초안)·`probe-runs.jsonl`·`probe-stderr.txt`(0바이트) · `gen/`(생성기 조각 p1~p6) · `fix1.py`·`reps1.json`·`reps2.json` · `nb0/`·`chk/`·`chk2/`(생성기 사본 대조) · `tryA/lab/notebooks/`(사본 실행 다섯 — 노트북 다섯·도구 파일·서버 파일) · `B/`(새 커널 B 사본) · `illu/`(1차·2차 원본·다시 받은 원본·1100 사본) · `04-figures.md`·`04-shape.md`·`04-diagnosis.md`(쓰기 전 사본).
- `$ROOT/.cache/ch34-04/pre/A-04.ipynb`(새 커널 A 사본) · `$ROOT/.cache/ch34-04-view/illu-1-1100.png`·`illu-2-1100.png`(삽화 보기 사본).
- 챕터 `figures/04-rate-limit-flow.{svg,excalidraw}`(옛 그림 — 본문에서 빠짐, 처분은 마감).
- 기기 디스크 여유: 루트(`/`, `/tmp` 포함) **1.5G → 1.5G**(작업 전후) · 연결 폴더(사용자 디스크) **73G → 73G**.
