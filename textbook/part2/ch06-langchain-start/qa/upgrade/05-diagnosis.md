# 05-타임아웃-재시도-폴백 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 05, `figures/05-resilience.*`). 챕터 전체 수정 전 게이트는 01절 때 남긴 `gates-before.json`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 1 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 11 | 0 |
| G6 | 20 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 8 | 19(준비 3) |
| 검사한 문장 | 153 | 419 |

G8: `run_section.sh` 새 커널 PASS(2026-09-17, 19 코드 셀, `outputs_sha256` `46a75a0a…`), `verify.py --chapter` PASS(6절 99 코드 셀), `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch06-05/vis/` 사본으로 실행, 작은 글자·대비·잘림·SVG 경계·가로 스크롤·깨진 그림·복사 0). HTML 출력 칸 17개(출력 있는 코드 셀 17개와 같음, 04절의 칸 나뉨 없음).

## 수정 전 주요 문제

- G1: `lambda value: f"대체 경로: {value}"`. 사다리 밖(게이트가 세지 않은 것): 한 셀에 함수 정의 + `RunnableLambda` 두 개, 딕셔너리 카운터 `+=`, `raise TimeoutError`·`raise AssertionError` + try `else`, 키 셀 `raise FileNotFoundError`/`RuntimeError`, 문자열 하나로 `invoke("…")`(01~04는 튜플 목록), f-string 안 식
- G4: 모델 셀에 `temperature=0` 없음(`max_tokens=180, timeout=30, max_retries=1`)
- G5: 제목 셀·핵심 그림·결과 읽기 없음(11). G6: 영문 시작·70자 초과·5문장 단락(20). G7: Mermaid 0(옛 Excalidraw 1), 삽화 0, 설계표 없음
- 규격 §3 「실패 장면은 실제 조건으로」와 어긋남: 실패는 모두 수업 코드가 직접 `raise`한 `TimeoutError`(가짜 실패 함수). 실제 API 호출은 성공 1번뿐이라 `timeout=30`·`max_retries=1`이 한 일을 하나도 보이지 않음
- 앞 절과 어긋남(인계 §04 → §05): b3 「앞 절에서 … 조각이 일부 도착한 뒤 연결이 끊길 수도 있으므로 완료 상태를 따로 기록해야 했습니다」(04는 끊김·완료 상태를 실행하지 않았고 「조각」 금지) · 「첫 절의 모델 초기화에서는 timeout=30과 max_retries=1을 코드에 직접 적었습니다」(개선된 01~04는 두 인자를 쓰지 않음)
- 내용: `max_retries=1`을 「첫 요청 뒤 한 번 더」로 설명했지만 적지 않았을 때의 값(설치 판에서 openai 기본 2, 시간 제한 없음)은 다루지 않음. 지수 대기·지터·과금·멱등성·문제 상황 표 등 대부분 실행하지 않은 동작. 누적 시도 2회가 Before·After 호출 합이라는 해석이 헷갈림

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 nbkit `RUN_DATE` = 2026-09-17). 모든 모델 생성 줄에 `temperature=0`
- 데이터 유지: 개선 전 질문 「재시도는 왜 횟수를 제한해야 하나요? 한 문장으로 답하세요.」를 02·04절 system 「한 문장의 한국어로 답하세요.」 + user 「재시도 횟수를 제한해야 하는 이유를 설명하세요.」 튜플 목록으로. 정상 호출 `timeout=30`·`max_retries=1`, `with_retry(retry_if_exception_type=…, stop_after_attempt=…)`, `with_fallbacks([…], exceptions_to_handle=…)`, `RunnableLambda`, paired 형식 유지
- 실패를 실제 조건으로: 직접 `raise`한 `TimeoutError` 대신 `timeout=0.001`인 모델 객체 `tiny_model`이 openai 클라이언트에서 실제로 받은 시간 초과(`OpenAITimeoutError` = `openai.APITimeoutError` + `langchain_core.exceptions.ModelTimeoutError`). 02절 `ModelNotFoundError`와 같은 곳에서 불러옴. 대체 경로는 가짜 문자열 대신 02절 `gpt-5.4-nano` 실제 호출
- 기본 경로: 준비(버전 6줄·`import time`·import·키·모델) → 2 튜플 목록 → 3 적지 않은 두 값(`model.request_timeout`·`max_retries` None, `root_client.timeout` None·`max_retries` 2) → 4 `timeout=30, max_retries=1` 모델 → 답·`stop`·응답한 모델 `gpt-5.4-mini-2026-03-17` → 5 `timeout=0.001, max_retries=0` 모델 → `OpenAITimeoutError`·`Request timed out.`·`is_retryable` True·걸린 초 0.0 → 6 값 바꿔 보기 1 `max_retries` 적지 않음 → 걸린 초 1.3(openai 대기 두 번) → 7 함수 `ask_current_model(input_messages)`(바깥 이름 `current_model`·`attempt_log`, Ch 5 08 방식) → `RunnableLambda(…).with_retry((ModelTimeoutError,), 3)` → `RunnableRetry` → 시도 3·걸린 초 4.5(assert 3) → 8 값 바꿔 보기 2 `current_model = typo_model`(`gpt-5.4-mimi`) → `OpenAIModelNotFoundError`·`is_retryable` False·시도 1(assert) → 9 Before 폴백 없음 → `받은 답: None` → 10 After `tiny_model.with_fallbacks([fallback_model(nano, 30초, 재시도 1)], exceptions_to_handle=(ModelTimeoutError,))` → `RunnableWithFallbacks` → `AIMessage`·기본 경로 `gpt-5.4-mini`·응답한 모델 `gpt-5.4-nano-2026-03-17`(assert `"nano" in`) → 같은 폴백을 `typo_model`에 → `OpenAIModelNotFoundError`·`받은 답: None`(assert)
- 시도 수: 노트북 13번(답 2 = mini 1·nano 1, 404 2, 시간 초과 9 — 6절 3번은 소스 기준). 새 커널 실행 2번 = 26 + 탐색(`/tmp/ch06-05/probe1·2·3.py`: 답 2, 404 2, 시간 초과 13) → 답을 받은 서비스 요청 합계 6
- 새 커널 실행 2번의 이유: 첫 실행은 `오늘 볼 그림` PNG가 없어 첨부 단계에서 멈춤(실행 자체는 PASS). 그림을 만든 뒤 다시 실행하자 7절 걸린 초가 3.2 → 4.5로 바뀌어 결과 읽기·본문·05-2·05-3 라벨·캡션·설계표를 `mdpatch.py`와 치환으로 마지막 출력에 맞춤. 6절 1.3은 두 번 같음
- 라이브러리 확인(설치 버전 소스): langchain-openai 1.6.0 `request_timeout`(alias `timeout`)·`max_retries` 기본 None, `max_retries`가 None이면 클라이언트에 넘기지 않고 `timeout`은 None 그대로 넘김 → openai 3.10.0 `DEFAULT_MAX_RETRIES = 2`, 요청 extensions timeout 네 값 모두 None(탐색 probe3로 확인). openai `_retry_request`는 시간 초과·연결 오류·408·409·429·5xx만 재시도, 대기 `min(0.5 × 2^n, 8) × (0.75~1)`(첫 0.375~0.5초, 둘째 0.75~1초). langchain-openai `_handle_openai_api_error`가 `APITimeoutError` → `OpenAITimeoutError`, `NotFoundError` → `OpenAIModelNotFoundError`. langchain-core 1.6.2 `ModelError.is_retryable` False, `ModelTimeoutError`·`ModelRateLimitError`·`ModelAPIError`·`ModelConnectionError` True. `with_retry` 기본 `(Exception,)`·`wait_exponential_jitter=True`·`stop_after_attempt=3`, `Retrying(reraise=True)`. tenacity 9.1.4 `wait_exponential_jitter` `initial × 2^(시도 번호−1) + uniform(0, 1)`(첫 1~2초, 둘째 2~3초). `RunnableWithFallbacks.invoke`는 `exceptions_to_handle`만 받고 나머지는 바로 다시 냄, 모두 실패하면 `first_error`
- 온라인 문서(2026-09-17 확인): LangChain Models 「기본 6번 재시도」 → 설치 판 출력 2와 다름(b7), openai-python README 「기본 2번 재시도·10분 시간 제한」 → 설치 판 조합의 모델 객체는 None(b7), with_retry·with_fallbacks reference 인자·기본값은 소스와 같음
- 01~04절 인계 반영: 튜플 목록·라벨 줄, 「모델 객체를 만들 때 요청 0번」(01)·「인자를 더해 새 모델 객체」(01 출력 상한 12), 02 `ModelNotFoundError`·`gpt-5.4-mimi`·`gpt-5.4-nano` 재사용, 03 호출 객체 `RunnableSequence`와 `RunnableRetry`·`RunnableWithFallbacks`를 같은 「호출 객체」로, 04 「모르는 값은 None」과 받는 도중 오류 미실행을 b3·b7에 이음. 개선 전 b3의 두 문장(「조각」·완료 상태, 「첫 절에서 timeout·max_retries를 적었다」)을 없애고 「01~04는 두 인자를 적지 않았고 이 절에서 처음 적는다」로 고침. 04 인계의 「05 「시도」와 04 「요청 1번」은 같은 셈 방식」 → 시도 = 요청을 한 번 보내 보는 일, 시간 초과 시도가 서버에 닿았는지는 알 수 없다고 적음. 청크를 「조각」으로 부르지 않음(05는 청크를 쓰지 않음, 삽화 그림 읽기에서 04 구슬 = 청크와 구분). 03 「칸(필드)」 안 씀. temperature 0 ≠ `do_sample=False` 한 문장
- 규격 §2-2: `@` 줄·`BaseModel` 없음. Python 새 모양은 모두 배운 것 또는 한 문장 풀이: 원소 하나짜리 튜플 `(ModelTimeoutError,)`(한 문장), `round(값, 1)`(Ch 5 08), 바깥 목록에 `append`하는 함수·바깥 이름 바꾸기(Ch 5 08), `time.perf_counter()`(Ch 2 12), `print("오류 메시지:", error)`(01). `lambda`·`+=`·`raise`·try `else`·f-string·문자열 `invoke`·`isinstance`·`startswith`는 코드에서 뺌
- 본문 10블록 다시 씀: 이 절의 질문, 앞에서 배운 내용 표(01·02·03·04, Ch 2 04·05·12, Ch 5 08), 비유(막힌 레일과 옆길), 타임아웃과 적지 않은 값, 재시도와 다시 시도할 오류(`is_retryable`), 폴백과 응답한 모델, 용어 표 7개, 실행 예제 뒤 「다시 시도한 순서」·「다시 시도하는 두 자리」(겹친 재시도 3 × 3 = 9는 소스 계산·미실행), 일부러 실패해 보기(Before/After/After 확인), 주의 메모 10개, 복습 5문제, 참고 자료 5개
- 뺀 것: 문제 상황 6행 표(대부분 미실행), 과금·멱등성의 단정 문장(→ 「이번 출력으로 알 수 없음·실행하지 않음」), 지수 대기 설명 중 실행하지 않은 인자(`exponential_jitter_params`), 로컬 시뮬레이션 전체
- 그림: Mermaid 4장(05-1 세 가지 장치 TB 두 갈래, 05-2 다시 시도 순서 sequenceDiagram, 05-3 다시 시도 비교, 05-4 Before/After 세 칸), 삽화 1장(05-5 막힌 길과 옆길, job 059a0a41-a739-4fde-affa-e2062fc5c922, 2크레딧, 1회 생성 통과, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:05-resilience}}`은 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본). 04와 같이 기기에서 job 결과를 받아 줄임(원본 SHA-256 앞 16자 `46a0b39482c8d1f4`)

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1.md`): **accept**(하 3, 공통 C-1·C-5 반영 전제). 반영 결과: C-1 준비물 요금 문장, C-5 범위 단락(강의 3~5·7·9·10절, 6·8절 값 바꿔 보기는 실습 시간, 검토 예시에 없던 4절은 강의에 넣음, **강사 확인 대상**), 05-1 [25] 새 단락 「코드 첫 줄 주석의 시도 3번은 소스로 계산한 최대 횟수이고, 이 셀이 센 값은 아닙니다.」(주석 자체는 재실행이 필요해 그대로, 다음 재실행 때 `author_05.py` 주석 수정), 05-2 [13] `root_client`는 읽기만, 05-3 [43] 「설치한 langchain-core 1.6.2 소스로 보면 … 이 경우는 이번에 실행하지 않았습니다.」 결정 Q5 권고대로(`timeout=0.001`·`root_client` 유지). 반영 방법: `mdpatch.py` → `run_section.sh … 05 --no-exec`(노트북 재실행 없음, 코드 셀·출력 그대로), 마감 게이트 `gates-after.json` G1~G7 0.
- 리뷰 묶음(반영 뒤 다시 만듦): `qa/upgrade/review-pack/`, 반영 전 묶음 `qa/upgrade/before/review-round1/review-pack/`
- 검토자가 볼 곳: (1) `timeout=0.001`을 「서버가 제시간에 답하지 못한 상황」의 대역으로 쓴 판단과, 시간 초과 시도가 서버에 닿았는지 모른다는 문장(b7), (2) 3절 `model.root_client`(openai 클라이언트) 속성을 기본 경로에서 꺼내 보인 수준과 「None = 시간 제한 없음」이 소스·요청 extensions 확인에 기댄 점, (3) 6절 「걸린 초 1.3이 대기 두 번과 맞음」·7절 4.5초 해석이 재실행마다 바뀌는 시간 값에 기댄 점(assert는 시도 수만)

## 남은 것

- 기기 `/tmp/ch06-05`(탐색 스크립트·visual 사본·치환 json·삽화 원본)는 정리 대상
- 옛 도식 `figures/05-resilience.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 챕터 루트 `verification.md`·`집필점검표.md` 위쪽 05 행(2026-09-09 기록)은 개선 전 기록이라 챕터 마감 때 갱신
- 강사 확인
