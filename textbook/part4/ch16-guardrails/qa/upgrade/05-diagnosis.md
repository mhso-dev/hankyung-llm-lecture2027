# 05절 진단과 개선 기록 — 재시도·폴백과 감사 로그 (experiment)

- 작업 2026-09-23(10:50~11:20 UTC) · 규격 `textbook/QUALITY-UPGRADE.md`(§2·§2-7(9번 끝·10번 끝)·§3·§4·§5-3·§5-4·§6·§7-2) · 생성기 `qa/upgrade/author_05.py`(노트북 + `_src` 함께, `author_03.py`가 experiment 본, `author_04.py`가 최근 판).
- 1차 지시서: `qa/upgrade/handoff.md` 「챕터 공통」·「§04 → §05」, 챕터 리드 결정 1~9.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 7 | 105 | 5 | 2 | 7 | 0 | 9 | 27 | 3 | **53** |
| 수정 뒤(`gates-wip-05.json`, `--no-exec`) | **29**(준비 4) | **437** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 `upgrade_gates.py … --label wip-05 --section 05`(G1·G2 먼저) → `gates-wip-05-05.json`: G1 0, **G2 1**(`print("첫 줄의 칸:", list(….keys()))` 두 겹 중첩 호출 → 이름 `first_keys`에 담음), G3~G5 0, **G6 1**(b8 「다음 학습과 이어지는 지점 — …」 70자 넘음 → 「실제 호출로」를 뺌, 노트북 정리도 같게), G7 18(그림을 아직 안 만든 탓). 둘을 생성기에서 고친 뒤 실행했습니다.
- `--no-exec` 게이트 첫 판에서 0건. `verify.py --chapter` → `PASS 6 sections / 138 code cells (max 21 lines)`(21줄은 아직 고치지 않은 06절 몫, 05절 셀은 최대 **10줄** — 4절 한 번 부르기·9절 값 바꿔 보기). 빌드 HTML 일곱 개 `{{` 잔존 **0건**.
- 게이트가 세지 않는 것도 직접 확인(실행한 노트북 코드 셀 AST): f-string·`+=`·내포식·제너레이터 식·`lambda`·조건 표현식·`key=`/`reverse=`·`set`·`setdefault`·`.get`·기본값 매개변수·타입힌트·데코레이터·클래스·한 줄 다중 대입·`elif`·`enumerate`·`zip`·`next`·`sum`·`max`·`min`·`any`·`all`·`sorted`·**`isinstance`** **0건**, 셀 코드 최대 10줄, 함수 본문 최대 **7줄**(`retry_with_fallback`·`record_event`).
- 금지어 확장 목록(`~/ch16work/w05/ban16-05.py`, 04절 목록 그대로) — `_src`의 「폴백」 2 = 노트북 토큰 속 파일 이름 1 + **b4 풀이 1곳**(「제목의 폴백(fallback)은 Ch 6 05절에서 본 말입니다」), 노트북 「폴백」 2 = 제목 1 + **4절 풀이 1곳**. 「열」 1 = 고정 세 문장 「파일을 열면」. 그 밖 0건. 옛 `figures/05-흐름.caption.md`(본문 참조 0)의 「경로」·「반환」·「폴백」은 옛 파일이라 그대로. 삽화 `.prompt.md`의 「프롬프트」는 작업 기록 파일이라 대상 밖(03·04절과 같음).

## 2. 수정 전 주요 문제

1. **`lambda: "폴백 답"`**(과정 전체에서 드문 금지 문법), 한 셀에 함수 둘(`retry_with_fallback` + `flaky`, `permanent_failure` + `fallback_model`), 22줄 셀, `from typing import Callable`·타입힌트·기본값 매개변수(`attempts: int = 2`)·`state["calls"] += 1`, **딕셔너리 내포식**(`safe_audit`의 `detail`), `import hashlib, json, re` 한 줄, `hashlib.sha256((…).encode()).hexdigest()[:12]` 세 겹 연결.
2. 가리기가 노트북 안의 **옛 정규식 두 줄**(이메일 `[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}`, 전화번호 `01\d[ -]?…`)이라 02절 `mask_pii`(네 가지)·도구 파일과 다른 판이었습니다. 질문 `test@example.com 문의`는 테스트용 값이었습니다.
3. 실패 장면 둘이 모두 「합성 시간 초과」인데 흉내라는 사실이 출력·본문에 드러나지 않았고, 실제 모델 요청은 「서비스 지연 안내를 한 문장으로 작성하세요」(챕터 자료와 무관)로 예비 답을 만드는 한 번뿐이었습니다. 모델 설정 `max_tokens=140`·`timeout=30`·`max_retries=0`, `reasoning_effort="none"` 없음.
4. 감사 기록 파일을 `unlink` → `write_text` 한 줄로 썼고, 무엇을 남기고 무엇을 빼는지(모델 답 문장)와 04절 예산과의 관계가 없었습니다.
5. 첫 줄 주석·제목 셀·결과 읽기 없음(G3 7·G5 9), 금지어 「폴백」 15·「경로」 14·「반환」 7·「캐시」·「프롬프트」, 70자 넘는 문장·영문 시작 문장(G6 27). 그림은 옛 `{{svg:05-흐름}}` 한 장.

## 3. 챕터 리드 결정의 반영

| 결정 | 이 절에서 한 일 |
|---|---|
| 1. 도구 파일 `notebooks/guardrails.py` | 준비 셀 `from guardrails import find_raw_values, make_budget, mask_pii, reserve`(알파벳 순) + 고정 세 문장(설치 셀 결과 읽기 셋째 단락, `_src` b3에도). 이 절이 처음 가르치는 여섯 함수는 노트북 안에 적고 도구 파일과 맞춤(§4) |
| 2. PII 네 가지 | 02절 `mask_pii`를 그대로 가져와 질문·기록 칸 모두 네 가지로 가림(질문에는 02절 가짜 값 둘 `test.user@example.com`·`010-0000-0000`, 가짜임을 설명) |
| 3. `re` | 이 절 노트북은 `re`를 직접 쓰지 않음(도구 파일 `mask_pii` 안에서만) |
| 4. 클래스 없음 | 클래스 0. 감사 기록 = 딕셔너리 칸 셋 `path`·`salt`·`rows`(04절 예산처럼) |
| 5. 모델 글에 `assert` 금지 | `assert`는 공용 키 확인 준비 셀·자리 찾기 셀과 8절 손 확인(다시 쓴 파일 내용이 같은지·원문이 없는지)뿐. 모델 답은 출력으로만 |
| 6. `runs/` 덮어쓰기 | `write_audit_rows`가 여는 방식 `"w"`로 기록 목록 전체를 다시 씀. 새 커널 두 번 뒤 파일 해시 같음(§7) |
| 7. 제목 금지어 | 제목 「재시도·폴백과 감사 로그」 그대로. 본문 풀이 한 곳씩(노트북 4절·`_src` b4) 뒤로는 「예비 흐름·예비 모델·예비 답」, 「감사 로그」도 「감사 기록(audit log)」으로 풀어 씀. 강사 확인 대상 |
| 8. 모델 설정 | `key_and_model_cells("openai:gpt-5.4-mini")` + 예비 모델 셀 `init_chat_model("openai:gpt-5.4-nano", temperature=0, reasoning_effort="none")`. `max_retries`·`timeout`을 적지 않음(재시도 주제지만 실패는 이 절의 흉내 함수가 내므로 모델 객체 설정과 겹치지 않게, b7에 모델 객체의 기본 재시도 2와 곱해질 수 있음을 적음 — Ch 22 04 b7과 같은 방향) |
| 9. 비유 「도장과 도장 대장」 | 같은 탁자 위 **번진 파란 도장과 초록 예비 도장**(삽화 `05-5`) + 01절 대장 + 02절 덮개 천 |

## 4. 도구 파일 맞추기 (§2-7)

- `notebooks/guardrails.py` `e3762ee3…`(04절 끝) → **`c873875a0ecdc647dac8906882ee02b862dbeb50fa812ae11931cafed8891c47`**. 원본 사본 `~/ch16work/w05/guardrails.before-05.py`(세션 홈).
- **노트북 셀 ↔ 도구 파일: AST 같음 · 주석 줄을 뺀 본문 줄 글자까지 같음**(`~/ch16work/w05/astcmp05.py`): `retry_with_fallback`(본문 7줄)·`fingerprint_of`(4)·`safe_detail`(3)·`make_audit_log`(1)·`write_audit_rows`(5)·`record_event`(7). 02~04절 여덟 함수(`find_raw_values`·`mask_pii`·`split_history`·`history_text`·`trim_history`·`summarize_history`·`make_budget`·`reserve`)도 다시 대조해 같음. 주석 여섯 + `RETRY_WAIT_SECONDS` 「# Ch 16 05절에서 배웠습니다 — …」.
- 바꾼 것(테스트가 보지 않는 곳):
  - `retry_with_fallback` — `attempts < 1` 검사 두 줄을 뺌(본문 9 → 7줄, 규격 8줄). 이제 `attempts`가 0이면 기본 흐름을 부르지 않고 곧바로 예비 흐름(시도 번호 1)을 부릅니다. 테스트 5는 그 검사를 보지 않습니다(04절이 `reserve`의 `return budget`을 뺀 것과 같은 판단).
  - **`fingerprint_of(salt, text)` 새 함수** — 옛 `record_event` 한 줄 `hashlib.sha256(salted.encode("utf-8")).hexdigest()[:12]`를 Ch 15 03 선례대로 세 줄(바이트 → `hashlib.sha256` → `hexdigest()`)로 풀어 따로 둠.
  - **`safe_detail` 다시 씀, `safe_dict_of`·`safe_list_of` 뺌** — 옛 판은 `isinstance` 셋 + 세 함수가 서로 부르는 재귀였습니다. 새 판은 「값을 `json.dumps`로 글 하나로 펴서 `mask_pii`로 가린 뒤 `json.loads`로 다시 읽기」 세 줄이라 `isinstance`·재귀 없이 안쪽 목록·딕셔너리까지 가립니다(테스트 5 중첩 `{"nested": ["010-1234-5678"]}` 통과, 노트북 6절 `가린 뒤: {'route': 'fallback', 'notes': ['연락처 <PHONE_MASKED>']}`). **알려진 한계**(본문에 쓰지 않음): 칸에 전화번호 모양의 **긴 정수**(예: 10자리 넘게 이어진 `01…` 숫자)가 있으면 JSON 숫자 자리가 표식으로 바뀌어 `json.loads`가 `JSONDecodeError`를 냅니다. 옛 판은 숫자 칸을 가리지 않았습니다. 이 챕터가 기록하는 칸(흐름 이름·시도 번호·예약한 호출 수·종류별 개수·문서 ID 목록·까닭 글)에는 그런 숫자가 없습니다.
  - `write_audit_rows` — 폴더 만들기(`os.path.dirname`·`if folder:`·`os.makedirs(…, exist_ok=True)`) 세 줄을 빼고 `import os`도 뺌(본문 8 → 5줄). 폴더는 부르는 쪽이 Ch 15 08 모양(`os.path.exists` → `os.makedirs`)으로 먼저 만듭니다(05 노트북 7절). 테스트는 `tmp_path`(이미 있는 폴더)를 쓰므로 영향 없음. **06절이 이 함수로 `runs/`에 쓰려면 폴더를 먼저 만들어야 합니다**(인계).
  - `record_event` — 지문 줄을 `fingerprint_of` 부르기로 바꿈(칸 차례 `event`·`query_hash`·`query_masked`·`detail` 그대로, 테스트 5·6·7이 보는 `query_masked`·사건 이름 그대로).
- `pytest -q -p no:cacheprovider tests` → **7 passed**. 테스트 파일은 고치지 않았습니다(`632ab36c…` 그대로).
- **01~04 노트북이 깨지지 않는지**: 네 노트북 사본에서 `%pip` 셀과 모델 요청 셀(및 그 결과를 쓰는 셀)을 빼고 새 커널로 실행(`~/ch16work/w05/nocall_check.py`, 04는 `ask_all(` 셀도 뺌) → 01 코드 셀 18·02 24·03 18·04 20 **오류 0**, 서비스 요청 0번. 네 노트북은 바뀐 함수를 쓰지 않습니다(02 `validate_query`, 03 `find_raw_values`만 가져옴).
- 챕터 밖: 도구 파일 해시를 적어 둔 곳은 `check_bundle_execution.py`(돌릴 때 계산, 마감 몫)뿐. Ch 22 노트북·본문은 이 함수들을 부르지 않습니다(`grep`).

## 5. 설계 — experiment

### 5-1. 실패 장면: 이 절에서 만든 실패 흉내 + 실제 모델 요청 (인계 핵심 결정)

- **까닭**: (1) 실제 짧은 시간 제한(`timeout=0.001`)으로 만든 시간 초과는 몇 번째 시도에서 날지·회복될지 정할 수 없어 「한 번 실패 뒤 두 번째 시도에서 답함」을 두 번 실행에서 같게 보일 수 없습니다(Ch 22 04 b6도 「잠깐 느렸다가 회복되는 실제 장애에서 재시도가 성공하는 경우는 이번에 관찰하지 않았습니다」). (2) 설치판에서 확인한 결과 **`openai.APITimeoutError`(→ `APIConnectionError → APIError → OpenAIError`)도, LangChain이 감싼 `OpenAITimeoutError`(→ … `ModelTimeoutError → ModelError → LangChainException`)도 파이썬 `TimeoutError`를 이어받지 않아** 테스트 5가 보는 `TimeoutError`만 받는 재시도 함수가 받지 못합니다(작업 가상환경 langchain-openai 1.6.1·openai 3.19.0·langchain-core 1.6.4에서 `__mro__` 출력). 받을 오류를 바꾸면 테스트 5·도구 파일이 함께 바뀌고 설명할 오류 종류가 늘어납니다.
- **설계**: 기본 흐름 `ask_primary()`는 첫 줄에서 예약한 뒤 `failure_plan["tries"]`를 하나 늘리고, `fail_times` 이하이면 `raise TimeoutError("이 절에서 만든 실패 흉내입니다.")`, 그 뒤에는 **실제 기본 모델**(`gpt-5.4-mini`)을 부릅니다. 예비 흐름 `ask_backup()`은 예약 뒤 **실제 예비 모델**(`gpt-5.4-nano` — Ch 6 05 대체 모델·Ch 22 04 예비 모델과 같은 이름, 변수 `backup_model`도 Ch 22 04와 같음)을 부릅니다. 규격 §3의 「도구 함수 안의 실제 예외」에 해당합니다. 흉내라는 사실은 오류 메시지 출력(`오류 메시지: 이 절에서 만든 실패 흉내입니다.`)·노트북 4절·`_src` b4 「실패는 이 절에서 흉내 냅니다」·b7 첫 줄·복습 1에 밝혔고, 실제 서비스 오류를 받으려면 받을 오류 이름을 바꿔야 한다는 점은 b4·b7 설명으로만 두었습니다(「이번에 실행하지 않았습니다」).
- **두 실행**: 실패 흉내 한 번(첫 실행 → `primary`·시도 번호 2) / 두 번(둘째 실행 → `fallback`·3), 시도 횟수 2로 같음. 「두 번째 모델로 바꿔 부르기」는 둘째 실행에서 실제로 한 번.
- 예비 흐름을 모델 없는 고정 글로 두는 판(옛 첫 실험)은 쓰지 않았습니다 — Ch 22 04 「폴백은 첫 모델이 실패하면 예비 모델로 바꿔 부릅니다」와 이어지게, 예비 흐름도 실제 모델 요청으로 두었습니다.

### 5-2. 재시도와 04절 예산

- **시도마다 먼저 예약**(기본 흐름·예비 흐름 모두 첫 줄 `reserve`). 까닭: 04절 b7 「예약은 요청을 보내기 전에 적습니다. 그래서 요청이 실패해도 예약한 호출 수와 예상 비용은 그대로 남습니다」와, 실제 시간 초과는 요청이 이미 나간 뒤에 난다는 점. 실패 흉내는 요청을 보내지 않지만 실제와 같게 예약한다고 본문·b7에 적었습니다.
- 호출 한도 3(= 기본 흐름 둘 + 예비 흐름 하나), 비용 상한 0.01, 예상 비용 0.002는 04절 값 이어 씀(정한 값, 청구 금액 아님). 4절 한 번 부르기 `예약한 호출 수: 1`(실패한 시도도 예약이 남음), 5절 `2`·`3`.
- 값 바꿔 보기(9절): 호출 한도만 2 → 기본 흐름 두 번이 한도를 다 써서 **예비 흐름의 예약이 `ValueError("호출 한도를 넘습니다.")`**. 재시도 함수는 `TimeoutError`만 받으므로 셀의 `except ValueError`가 받아 사건 `stopped`로 기록(`'reserved_calls': 2`), **모델 요청 0번**. 「시도 횟수를 늘리면 호출 한도에 먼저 닿을 수 있다」(b4)를 실행으로 보였습니다.

### 5-3. 감사 기록 파일 `runs/05-audit.jsonl`

- 덮어쓰기(`"w"`), 한 줄 칸 넷 `event`·`query_hash`·`query_masked`·`detail`. `detail`은 **결정적인 칸만** — `route`·`attempt`·`reserved_calls`(answer) / `reason`·`reserved_calls`(stopped). **모델 답 문장은 넣지 않음**: 새 커널 두 번 해시가 같아야 하고, 답에도 개인정보가 섞일 수 있어서(본문 b4·노트북 6절에 까닭).
- 질문은 원문 `question`을 넘기고 `record_event` 안에서 `mask_pii`로 가린 뒤, **가린 질문**에 소금값 `ch16-session`을 붙여 지문 12글자(원문이 지문에도 들어가지 않음 — Ch 22 06 b7 「전화번호처럼 경우의 수가 적은 값은 … 원문을 찾을 수 있습니다」 걱정을 피함). 소금값은 코드에 그대로 적었다고 b7(Ch 22 06 b7과 같은 말).
- 최종 파일 3줄(answer·answer·stopped), 해시 **`92e3d109ecc13e2b712fbce70d6002182b68762337c6d92fa70ee847a35d3ac7`**(옛 `0d7d9da8…` 1줄에서 의도한 변경, `manifest-changes.md`). 7절에서 다시 읽어 `파일의 줄 수: 2`·`파일에 남은 원문 값: []`, 8절에서 같은 목록으로 다시 써 `처음 읽은 내용과 같은가: True`(`assert` 둘).
- **읽는 쪽**: `grep -rln '05-audit'`(textbook·qa·AGENTS.md·CLAUDE.md·_workspace, labs는 `.venv`·캐시 빼고) → 05 노트북 자신과 실행을 막은 옛 생성기 `labs/…/author_chapter.py`, 이 챕터 기록 문서뿐. 검사 스크립트·뒤 챕터가 읽지 않습니다. `runs/`는 학생 묶음 제외(`qa/public-files.json` `excluded`).

### 5-4. 그 밖

- 처음 쓴 파이썬(한 문장씩): `time.sleep(초)`(함수를 괄호 없이 넘김 — 03절) · `return 값, 값, 값` 세 값 튜플과 튜플 셋 풀기(02절에 이음) · `except TimeoutError:`(`as` 없이, 받을 이름만) · 함수 안 `return`이 `for`·`try` 안에서 함수를 끝냄 · 지문 앞 12글자 `[:12]` · 여는 방식 `"w"`로 목록 전체 다시 쓰기 · `json.loads`(Ch 15 02)로 가린 글 다시 읽기 · `str.count`(Ch 15 08). `raise`(01)·`try/except ValueError as error`(03)·`type(error).__name__`(03)·딕셔너리 칸 고치기(04)·대문자 이름(02)은 앞 절 모양 그대로.
- 기본 흐름·예비 흐름 함수는 인자가 없고 노트북 이름 `budget`·`failure_plan`·`messages`·`model`/`backup_model`을 씀(재시도 함수가 인자 없는 함수를 받으므로, 04절 `ask_with_budget`이 전역 `model`을 쓴 것과 같은 판단). 노트북 5절 결과 읽기에 한 문장으로 적었습니다. 이 두 함수는 도구 파일에 옮기지 않았습니다(노트북 전역에 기대므로, 규격 §2-7 4번).
- 용어: 새 말 다섯 — **실패 흉내·기본 흐름·예비 흐름(예비 모델·예비 답)·감사 기록(audit log)·소금값(salt)**. 이어 쓴 말 — 재시도·시도·시도 횟수(Ch 6 05), 폴백(Ch 6 05, 제목 풀이 한 곳), 예비 모델(Ch 22 04 말), 지문(Ch 7 08·Ch 15 03), 기록 한 줄(02), 예약·예산·호출 한도(04), 가리기·표식·가짜 값(02). 「경로」 대신 「흐름」·「쪽」, 「반환」 대신 「내놓습니다」.

## 6. 흔들림 확인 — 하지 않음 (`05-probe.md` 없음)

- 핵심 관찰(받은 흐름 `primary`/`fallback`, 시도 번호 2·3, 예약한 호출 수 1·2·3·2, 기록 줄 수·원문 없음·다시 쓴 내용 같음, 멈춘 까닭)은 **실패 흉내 횟수와 `reserve`가 정하는 값**이라 모델 답 문장에 기대지 않습니다. 모델 요청이 통신 오류로 실패하지 않는 한 같습니다. 예비 흐름에서 쓰는 것은 **대체 호출이 답을 내놓았는지(성공 여부)**뿐이고 답 문장은 결론·그림·기록에 쓰지 않았습니다 → 규격 §2-7 10번 끝의 노트북 밖 다섯 번 확인 대상이 아니라고 판단했습니다(04절과 같은 판단).
- 노트북을 서비스에 보내기 전에 **가짜 모델 객체로 로직만 한 번 확인**했습니다(세션 스크립트, 노트북 셀 글을 `exec`하되 두 모델 셀을 `.invoke`가 고정 글을 내놓는 작업용 객체로 바꾸고 `root_path`를 `/tmp/ch16-05-dry`로 돌림 — 교재에는 쓰지 않음, 서비스 요청 0번, 실제 `runs/`는 건드리지 않음). 그때 파일 해시도 `92e3d109…`로 실제 실행과 같았습니다(파일에 모델 답이 없다는 확인).
- 모델 답 문장은 결과 읽기 둘째 단락과 `_src` b6·b7에만 두었습니다: 새 커널 두 번 모두 기본 모델 답 끝 `[E01 p.1]`, **예비 답 끝 `[E01 1쪽]`**(시스템 메시지가 정한 꼴과 다름). b7에 「예비 모델의 답은 모양이 다를 수 있어 예비 답에도 01절 출력 검사를 거는 편이 안전하고, 이 절은 그 검사를 실행하지 않았다」를 적었습니다(정리·복습·그림에는 넣지 않음).

## 7. 실행값 (교재 코드 새 커널 두 번 — C 11:07:49~54 · D 11:08:15~19 UTC)

- `code_sha256` `d0fa62992aa0423aa55aeb2863fb31aa994089c43b8500d645e649f93962863e`(두 번 같음). `outputs_sha256` **C·D 모두 `fcfa38794e1257b0abd371f721d347c1a60f873bcd5f49cc4ce8bff559150dd7`** → 셀별 출력 **29/29 같음**(모델 답 두 셀 포함). **`runs/05-audit.jsonl`도 C 뒤·D 뒤 모두 `92e3d109…`**(C 뒤 사본 `~/ch16work/w05/05-audit.runC.jsonl`과 `cmp` 같음). **교재 출력은 C**(`run_section.sh`가 실행한 판). D는 C를 출력만 지운 사본 `~/ch16work/w05/nb-runD.ipynb`를 같은 가상환경·`PYTHONPATH`·`execute.py`로 실행(대조 본 `~/ch16work/w05/cmpCD.py`). 그림 첨부·`mdpatch.py` 뒤에도 노트북 코드·출력이 C와 같음을 다시 확인했습니다.
- 두 번 모두 같은 값(본문·그림·정리에 쓴 값): `불러온 앞 절 함수: find_raw_values make_budget mask_pii reserve`·`모델 이름: gpt-5.4-mini`·`예비 모델 이름: gpt-5.4-nano`·`자료 파일의 문서 수: 2`·`이번 검색 결과의 문서 수: 1`·`종류별 개수: {'email': 1, 'phone': 1, 'rrn': 0, 'card': 0}`·`메시지 수: 2`·`보낼 메시지에 남은 원문 값 수: 0`·`기본 흐름 시도 횟수: 2`·`시도 사이에 쉬는 초: 0.05`·`호출 한도: 3`·`비용 상한(달러): 0.01`·`요청 하나의 예상 비용(달러): 0.002`·4절 `오류 종류: TimeoutError`·`오류 메시지: 이 절에서 만든 실패 흉내입니다.`·`기본 흐름 시도 수: 1`·`예약한 호출 수: 1`·5절 `받은 흐름: primary`·`답을 받은 시도 번호: 2`·`예약한 호출 수: 2` / `받은 흐름: fallback`·`답을 받은 시도 번호: 3`·`예약한 호출 수: 3`·6절 `지문 글자 수: 12`·`… 두 지문이 같은가: True`·`소금값만 바꾼 지문과 같은가: False`·`가린 뒤: {'route': 'fallback', 'notes': ['연락처 <PHONE_MASKED>']}`·7절 `감사 기록 줄 수: 2`·`첫 줄의 칸: ['event', 'query_hash', 'query_masked', 'detail']`·`파일의 줄 수: 2`·`파일에 남은 원문 값: []`·8절 `다시 쓴 뒤 파일의 줄 수: 2`·`처음 읽은 내용과 같은가: True`·9절 `마지막 기록 칸: {'reason': '호출 한도를 넘습니다.', 'reserved_calls': 2}`·`감사 기록 줄 수: 3`.
- 두 번 같았지만 모델 출력에 달린 값(결과 읽기 둘째 단락·b6·b7에만, 「이번 실행에서는」·「새 커널 두 번 실행에서는」): 기본 모델 답 「미르시립도서관은 매주 월요일과 법정 공휴일에 휴관하며, 공휴일이 월요일과 겹치면 다음 날인 화요일에도 휴관합니다. [E01 p.1]」, 예비 답 같은 문장 + `[E01 1쪽]`.
- 준비물 「노트북 전체가 약 5초」는 C의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답 5.29초, 커널 기동 제외, D는 3.86초)에서 읽은 값입니다(`[[RUNSEC]]` → `mdpatch.py`). 쉬는 시간 0.05초는 정한 값이고 걸린 시간은 재지 않았습니다(b7).
- 실행 뒤 `mdpatch.py` 두 번(`~/ch16work/w05/reps05-a.json`·`reps05-b.json`)으로 설명만 고쳤습니다: 준비물 초, 5절 결과 읽기 둘째 단락 둘(모델 답), 그림 alt 두 곳(05-1 「한쪽/다른 쪽」 → 「왼쪽/오른쪽」, 05-4 왼쪽 위 상자에서 뺀 「예약 둘」), 삽화 alt·캡션·그림 읽기·비유 두 단락(PNG를 본 뒤), 도식 읽기 넷, b6 두 문장, b7 한 줄(예비 답 모양). 노트북 코드·출력은 그대로입니다.

## 8. 서비스 요청과 비용

- 노트북 한 번 실행에 **2번**(5절 첫 실행 `gpt-5.4-mini` 1 + 둘째 실행 `gpt-5.4-nano` 1, 임베딩 0) — 준비물·b5에 적음. 4절 한 번 부르기·9절 값 바꿔 보기는 0번(실패 흉내·예약에서 멈춤). 일반 절이라 요청 수만으로 강사 확인 대상에 올리지 않습니다(규격 §7-2).
- 이 절 작업 전체 **4번**: 노트북 C 2 + D 2(흔들림 확인·사전 점검 요청 없음, 가짜 객체 로직 확인은 0번). 01~04 사본 확인 0번. 예상 비용 합계 약 **0.002달러 아래**(요청 하나에 입력 약 130·출력 약 60토큰으로 어림 — 이 절은 토큰 수를 출력하지 않아 04절 첫 응답 122·53을 본보기로 씀, nano도 mini 요금 100만 토큰당 입력 0.75·출력 4.50달러로 크게 잡음, 청구 금액 아님, 재지 않음).

## 9. 그림 — `qa/upgrade/05-figures.md`

- Mermaid **4장**: `05-1`(b4 + 노트북 오늘 볼 그림, 원본 폭 363) · `05-2`(b5, 260, 상자 일곱 한 줄) · `05-3`(b6, **첫 판 회색 상자 글이 저절로 꺾여 `<br>` 두 번으로 나눠 v3**, 617) · `05-4`(b6 값 바꿔 보기, **첫 판 627 → 612** — 5절 둘째 실행 출력에 없는 「예약 둘」을 왼쪽 위 상자에서 뺌). 모두 868 아래, **빨강 0**(experiment). 네 장 모두 PNG를 직접 열어 본 **뒤에** alt·도식 읽기를 썼습니다(`.cache/ch16-05-view/v1-fig1~4.png`·`v2-fig3~4.png`·`v3-fig3.png`). `05-1`은 두 갈래가 노트북 5절 두 실행에서 하나씩 실제로 실행돼 실선이고 「화살표가 둘로 나뉩니다」로 적었으며, 기본 모델(짧은 라벨)이 왼쪽에 놓여 그대로 「왼쪽 … 오른쪽」으로 적었습니다.
- 삽화 **1장** `05-5-번진-도장과-예비-도장`: `nano_banana_pro`(응답 `nano_banana_2`) · 16:9 · 2k · `use_unlim: false` · count 1. **job `d72aa128-3afc-4921-a39e-b081b40c9daf` 1차 채택**(서비스 쪽 실패 0회, 검수 탈락 재생성 0회) · 2크레딧 · 잔액 **2636.5 → 2634.5**(`balance` 전후). 원본 `d98985cc…`(2752×1536) → 저장 1100×614 `7761648f…`. 결과 URL을 다시 받아 같은 폭으로 줄여 저장 PNG와 픽셀 대조: bbox `None`, 세 칸 extrema `(0, 0)`. 저장 PNG 다른 이름 사본과 원본 부분 확대(쪽지·대장)를 직접 열어 그림 읽기를 썼습니다 — **번진 파란 무늬 둘(겹쳐 찍힘)·또렷한 초록 무늬 하나·손도장 둘(파란 바닥·초록 바닥)**은 프롬프트와 같았고, 대장은 오른쪽 쪽에만 **줄 넷**, 천은 **아래 두 줄의 뒤쪽**을 덮어(프롬프트 「마지막 줄 앞머리」와 다름) 그림대로 적었습니다. 대장 줄 넷은 파일 줄 수(셋)와 짝짓지 않았습니다.
- 옛 `figures/05-흐름.{svg,excalidraw,caption.md}`은 그대로 둠(본문 참조 0, 마감에서 삭제 승인 대상).

## 10. 검사

- 게이트 0건(§1) · `verify.py --chapter` PASS · `{{` 0건 · 새 커널 두 번 **29/29** + 감사 기록 파일 해시 같음(§7) · `pytest` 7 passed · 05절 여섯 함수 노트북 ↔ 도구 파일 AST·본문 줄 같음(02~04 여덟 함수 다시 대조 같음) · 01~04 사본 새 커널 오류 0 · 금지어 확장 검사(§1) · AST 금지 문법 0건(§1).
- 참고 자료 네 문서를 기기 셸 `curl`로 열어 확인(2026-09-23): Python 3.12 `time.sleep`(「Suspend execution of the calling thread for the given number of seconds.」) · Built-in Exceptions `TimeoutError`(「Raised when a system function timed out at the system level.」) · `hashlib`(`sha256`·`hexdigest()`) · OWASP Logging Cheat Sheet(「personal data (e.g. personal names, telephone numbers, email addresses)」를 기록에서 빼거나 가릴 값으로 적음).
- 설치판 확인: 위 §5-1의 두 시간 초과 오류 `__mro__`, `ChatOpenAI.max_retries` 기본 `None` → openai 클라이언트 `max_retries` 2(`DEFAULT_MAX_RETRIES = 2`, 가짜 키로 모델 객체만 만들어 확인, 요청 0번).
- `pack.py` → `qa/upgrade/review-pack/05-재시도-폴백과-감사-로그.md`.
- 보호 파일 7개: §12.

## 11. 강사 확인 대상

1. **제목 「폴백」 유지**(챕터 리드 결정 7) — 본문은 노트북 4절·`_src` b4에서 「폴백(fallback)」을 한 번씩 풀고 뒤로는 「예비 흐름·예비 모델·예비 답」. 「감사 로그」도 제목에만 두고 본문은 「감사 기록(audit log)」.
2. **실패 장면을 이 절에서 만든 실패 흉내 함수로 둔 설계**(§5-1) — 실제 서비스 시간 초과는 이 함수가 받지 못한다는 사실을 b4·b7에 적고, 받을 오류를 바꾼 판은 실행하지 않음.
3. **예비 모델 `gpt-5.4-nano`를 두 번째 모델로 더함**(모델 요청 2번). 예비 답 끝 출처 표시가 두 번 모두 `[E01 1쪽]`이었고 b6·b7에 「두 번 실행에서는」으로 적음(01절 출력 검사를 예비 답에 걸면 막혔을 모양이지만 실행하지 않음).
4. **실패한 시도도 예약한 판단**(§5-2) — 실패 흉내는 요청을 보내지 않지만 실제와 같게 예약. 값 바꿔 보기에서 예비 흐름이 예약에서 막힘.
5. **도구 파일 변경**(§4) — `retry_with_fallback` 검사 두 줄 뺌, `fingerprint_of` 새로, `safe_detail` JSON 글 가리기로 바꾸고 `safe_dict_of`·`safe_list_of` 뺌(긴 정수 칸 한계), `write_audit_rows` 폴더 만들기·`import os` 뺌.
6. **보호 파일 `runs/05-audit.jsonl`을 새 모양 3줄로 다시 씀**(`0d7d9da8…` → `92e3d109…`, 읽는 쪽 없음).
7. 기본 흐름·예비 흐름 함수가 노트북 전역 이름에 기대는 모양(인자 없는 함수를 넘기는 재시도 함수 때문).
8. 삽화의 번진 무늬 둘이 겹쳐 그려진 것이 「두 번 찍음」으로 읽히는지, 천이 줄 뒤쪽을 덮은 것.
9. 교재 출력 환경 `langchain-core 1.6.4`·`openai 3.19.0` ↔ 학생 잠금 `1.6.2`·`3.11.0`(잠금 판 동작은 확인하지 않음, 01~04절과 같음).
10. 한국어 감사 3단·삽화 판독은 별도 세션 몫.

## 12. 보호 파일 7개 (`before-manifest.json`, 원본은 고치지 않음)

| 파일 | 상태 |
|---|---|
| `labs/part4/ch16-guardrails/data/retrieved-documents.json` | 같음 `ae2fe4f4…` |
| `labs/part4/ch16-guardrails/runs/05-audit.jsonl` | **05절 의도한 변경** `0d7d9da8…` → `92e3d109…`(3줄, 새 커널 두 번 같음, §5-3) |
| `labs/part4/ch16-guardrails/runs/06-audit.jsonl` | 같음 `9d705d17…` |
| `labs/part4/ch16-guardrails/guardrails.py` | 01절 이동(옛 자리 없음) → `notebooks/guardrails.py` **05절 의도한 변경** `c873875a…`(§4) |
| `labs/part4/ch16-guardrails/tests/test_guardrails.py` | 01절 판 그대로 `632ab36c…` |
| `labs/part4/ch15-evaluation-advanced/runs/batch-eval-input.jsonl` | 같음 `0177cebc…` |
| `labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json` | 같음 `dc48b1bc…` |

기록: `qa/upgrade/manifest-changes.md`(05절 줄 둘과 「05절 끝 대조」 덧붙임).

## 13. 챕터 밖

- **고친 파일 0개.** Ch 22는 읽기만 했습니다.
- Ch 22 인용과의 대조: 04 b3 「Ch16 04절과 05절에서는 호출 한도와 재시도를 함수로 직접 만들었습니다」(맞음 — `retry_with_fallback`을 노트북에서 정의·설명) · 06 b3 「Ch16 05절에서 재시도와 함께 감사 로그를 직접 남겼습니다」(맞음 — `record_event`·`write_audit_rows`를 노트북에서 정의하고 5절 재시도 결과와 9절 예약에서 멈춘 일을 같은 파일에 남김) · 04 b3 「Ch6 05절에서 … 예비 모델을 LangChain 모델 설정으로 다뤘습니다」·04 본문 「폴백은 첫 모델이 실패하면 예비 모델로 바꿔 부릅니다」(같은 말 「예비 모델」, 같은 이름 `gpt-5.4-nano`·`backup_model`) · 04 b7 「모델 객체의 `max_retries` 설정과 재시도 미들웨어를 함께 쓰면 시도 횟수가 곱해질 수 있습니다」(이 절 b7도 같은 방향) · 06 본문 지문·소금값 설명(「같은 글은 항상 같은 지문」·「비밀 설정에 둡니다」)과 같은 뜻. Ch 22 노트북·코드는 이 절 함수들을 부르지 않습니다.
- 학생 묶음 허용 목록: 새로 읽는 파일 없음(자료 파일은 이미 목록에), 쓰는 `runs/`는 묶음 제외 — 학생 묶음에서는 7절 셀이 `runs` 폴더를 먼저 만듭니다. `part4-practice.zip`·`part6-practice.zip`은 다시 만들지 않았습니다(마감 몫).

## 14. 지우지 않은 것 (삭제 승인 대상)

- 프로젝트 `.cache/ch16-05-view/`(이 절이 새로 만든 폴더 — 스테이징용 PNG 사본 `v1-fig1~4.png`·`v2-fig3~4.png`·`v3-fig3.png`·`illu-job1-1100.png`·`illu-crop-ledger.png`·`illu-crop-slip.png`).
- `qa/upgrade/gates-wip-05-05.json`(첫 실행 전 G1·G2 확인).
- 세션 홈 `~/ch16work/w05/`(`guardrails.before-05.py`·`src05-before.html`·`nb05-before.ipynb`·`05-audit.before.jsonl`·`05-audit.runC.jsonl`·`parts/p1~p4.py`(생성기 조각)·`astcmp05.py`·`ban16-05.py`·`nocall_check.py`·`nocall-01~04.ipynb`·`nb-runC.ipynb`·`nb-runD.ipynb`·`cmpCD.py`·`reps05-a.json`·`reps05-b.json`·`illu/`(원본 2752px `job1-orig.png`·`job1-again.png`, 줄인 사본, `shrink.py`·`cmp.py`·`crop.py`·확대 둘)). 마운트 폴더 밖이라 학생 묶음과 무관합니다.
- 기기 `/tmp/ch16-05-dry/`(가짜 객체 로직 확인용 자료 사본과 그때 쓴 `runs/05-audit.jsonl`), `/tmp/ch16-05-ref-*.html` 넷(참고 자료 확인용).
- 옛 그림 `figures/05-흐름.{svg,excalidraw,caption.md}`(마감에서 삭제 승인, 사본 `before/figures/`).

## 15. 챕터 마감 검토 반영 (2026-09-23)

검토 보고서 `review-round1-A.md`(A-n)·`review-round1-B.md`(B-n), 챕터 전체 기록은 `chapter-summary.md`와 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-23)」.

- **다시 실행하지 않았습니다**(`mdpatch.py` → `--no-exec`). `code_sha256` `d0fa6299…`·`outputs_sha256` `fcfa3879…`·`runs/05-audit.jsonl` `92e3d109…` 그대로.
- **B-3** 「실제 시간 초과는 요청이 이미 나간 뒤에 납니다」 단정을 「나간 뒤에 날 수도 있습니다」로(b4 + 「시간 초과가 난 요청에 요금이 붙었는지는 이번에 확인하지 않았습니다」, b7 + 「실제 시간 초과가 언제 나는지는 이번에 확인하지 않았습니다」, 복습 3 해설 「… 날 수도 있어, 실패한 시도도 호출 한 번으로 세는 편이 안전하기 때문입니다」, 셀 32 둘째 단락).
- **B-4** `05-1` 파란 상자 「재시도 함수 / 기본 흐름을 두 번까지」(「시도마다 먼저 예약」 뺌). 도식 읽기에 「예약은 재시도 함수가 아니라, 넘겨받은 흐름 함수 `ask_primary`·`ask_backup`가 첫 줄에서 합니다」, alt(노트북 셀 1 포함). 폭 363.
- **A-2** 설명 셀 18·40, b6·b7의 「지킬 말」 → 「시스템 메시지(글)」. 출력 라벨 `지킬 말:`과 코드 주석(셀 19)은 그대로, 셀 20 결과 읽기에 04절과 같은 두 문장. **다음 재실행 때 생성기 라벨·주석.**
- **A-5** `_src` b3의 고정 세 문장을 빼고 「이 절은 02절 함수 둘과 04절 함수 둘을 도구 파일 `guardrails.py`에서 가져옵니다」(빌드 HTML에 한 번). **A-4** 노트북 고정 세 문장 뒤 한 문장.
- **A-7** b5·확인할 점·`05-3`·`05-4` 도식 읽기·alt, 그림 `05-2` 라벨·`05-3`·`05-4` 칸 제목(「노트북 N절」). **B-1**.
- 그림 다시 렌더 `05-1`·`05-2`·`05-3`·`05-4`(폭 363·260·617·612), PNG 넷을 직접 열어 확인. 노트북 첨부 `05-1` 새 PNG.
