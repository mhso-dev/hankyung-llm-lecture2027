# 04절 설치판 모양 확인 (모델 없음 · 연습용 서버 · 2026-09-30)

- 목적: handoff §03 → §04 3·4항의 Before 결함(겹친 다시 보내기 9 ↔ 3)과 값 바꿔 보기(한꺼번에 보내는 수)가 이 설치판에서 **매번 같게** 나는지, 설계를 정하기 전에 다섯 번 확인. 서비스 요청 0(모델 객체는 가짜 키 `not-a-real-key` + `base_url` = `127.0.0.1` 연습용 서버), `OPENAI_API_KEY`를 지운 환경(`env -u OPENAI_API_KEY`), `PYTHONDONTWRITEBYTECODE=1`, 가상환경 `.cache/vm/venv-ch34-cost-rate-limits`(openai 3.13.0 · langchain-openai 1.6.0 · langchain-core 1.6.2 · tenacity 9.1.4 · httpx 0.28.1 · Python 3.12.13). 흔들리는 값은 걸린 초뿐이라 설계에서 출력하지 않기로 함(결론·라벨·`assert` 금지 — 규격 §3).
- 판단 규칙(첫 실행 전에 정함): 서버 요청 수·오류 이름·클라이언트 `max_retries`·한꺼번에 처리 중이던 수의 가장 큰 값·서버 종료 코드가 다섯 번 모두 같으면 결론·그림 라벨에 쓸 수 있음. 하나라도 다르면 그 값은 결론에 쓰지 않음. 걸린 초는 기록만.

## 1. 설계 초안 확인 (`probe04.py` `b7194945…` · 서버 초안 `always_429_server-draft04.py` `54bbd613…` · 기록 `probe-04.jsonl` `2b9c93e7…`)

- 서버 초안: 함수 하나 `wsgiref`, 모든 요청에 429, `/reset`이면 비우고 나머지 주소는 모두 셈(머리 `practice-count`). 자식 프로세스(`stdout`·`stderr` 버림), 포트 5804n.
- 첫 확인 1번(00:3x, 포트 58034, 기록은 셸 출력만) + 기록한 다섯 번(00:37:17Z·00:37:48Z·00:38:19Z·00:38:59Z·00:39:32Z) — **여섯 번 모두 같음**, 표준 오류 0바이트:

| 확인한 것 | 값(6/6) | 걸린 초(흔들림 — 기록만) |
|---|---|---|
| 기본 모델 객체(`max_retries` 적지 않음) 한 번 | 오류 `OpenAIRateLimitError` · 서버 요청 3 · `max_retries` None / 클라이언트 2 | 1.24~1.45 |
| `max_retries=0` 한 번 | 요청 1 · 클라이언트 0 | 0.0 |
| Before: 기본 모델 + `with_retry(retry_if_exception_type=(ModelRateLimitError,), stop_after_attempt=3)` | **요청 9** · 호출 객체 `RunnableRetry` | 7.73~8.61 |
| After: `max_retries=0` + 같은 `with_retry` | **요청 3** | 3.64~4.76 |
| 문의 여섯 `RunnableLambda(ask_and_count).batch` 설정 없음 | 한꺼번에 처리 중이던 수 6 · 요청 18 · 오류 6 | 4.33~4.76 |
| 같은 여섯 `config={"max_concurrency": 2}` | 한꺼번에 처리 중이던 수 2 · 요청 18 | 12.13~13.15 |
| 서버 끄기 | 종료 코드 −15 · 포트 닫힘 | — |

- 오류 계보(`__mro__` 앞 여섯): `OpenAIRateLimitError` → `RateLimitError` → `APIStatusError` → `APIError` → `OpenAIError` → `ModelRateLimitError` · `error.response.status_code` 429 · 오류 글 `Error code: 429 - {...}`(노트북에는 출력하지 않음).

## 2. 설계 확정과 바꾼 점

- 서버: **모델에 보내는 요청(주소 끝 `/chat/completions`)만 셈**, `/reset`은 0으로 맞춤, `/count`는 세지 않고 알려 줌(값 바꿔 보기에서 요청 수를 따로 묻기 위해). 오류 글 코드 `practice_429`. 여전히 모든 응답이 429(답 글 없음).
- 값 바꿔 보기: 문의 여섯 → **02 문의 글 다섯**(과정 자료 이어 쓰기 · Python 3.12 기본 일꾼 수 `min(32, CPU 수 + 4)`는 CPU 하나여도 5라, 설정 없음의 5가 어느 컴퓨터에서도 같음).
- 셀마다 `/reset` 뒤 부르고 `/count`로 셈 → 앞 셀이 뒤 셀의 수를 바꾸지 않음.

## 3. 최종 모양 확인 (생성기 `author_04.py`가 쓴 노트북 사본 · `/tmp/ch34-04/tryA/lab/notebooks` · `execute.py --cwd` 그 폴더 · `PYTHONPATH` 없음)

| 회차 | `executed_at` | `code_sha256` | 셀별 출력 글(1회차와 견줌) |
|---|---|---|---|
| 1 | 2026-09-30T01:00:58Z | `85149d05fc2b…` | — (`outputs_sha256` `19201b0a9600…`) |
| 2 | 01:01:48Z | 같음 | 24/24 같음(`%pip` 셀 출력이 스트림 둘로 나뉘어 해시만 다름 `a835adab…`) |
| 3 | 01:02:21Z | 같음 | 24/24 같음(`19201b0a…`) |
| 4 | 01:03:09Z | 같음 | 24/24 같음(`19201b0a…`) |
| 5 | 01:03:45Z | 같음 | 24/24 같음(스트림 나뉨 `f74dfd6e…`) |

- 다섯 번 모두: 기본 3 · `max_retries=0` 1 · Before 9 · After 3 · 곱셈 대조 `True` 둘 · Before ÷ After 3 · 문의 다섯 설정 없음 5/15 · `max_concurrency` 2 → 2/15 · 받은 오류 수 5 · 종료 코드 −15 · 포트 닫힘 `False`. 실행마다 남은 서버 프로세스 0·대기 포트 0, `__pycache__` 0.
- 이 표는 새 커널 A(01:04:46Z)·B(01:05:31Z)와 별개인 사본 실행입니다(A·B도 24/24 같음 — `04-diagnosis.md` §6).
