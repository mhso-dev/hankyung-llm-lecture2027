# 01절 진단과 개선 기록 — 입출력과 출처 검증 (paired)

- 작업 2026-09-23 · 규격 `textbook/QUALITY-UPGRADE.md`(§2·§2-7·§3·§4·§5·§6·§7-2·§8) · 생성기 `qa/upgrade/author_01.py`(노트북 + `_src` 함께).
- 1차 자료: `qa/upgrade/chapter-lead-notes.md`(준비 담당 조사) + 챕터 리드 결정 9개(이 파일 §3·`handoff.md` 「챕터 공통」).
- **작업은 두 판으로 이어졌습니다.** 첫 판(08:32~08:51 UTC)이 도구 파일 이동·생성기·흔들림 확인·그림·삽화·묶음까지 마치고 끊겼고, 두 번째 판(08:52~ UTC)이 첫 판 결과를 모두 다시 읽어 확인한 뒤 코드 두 곳과 설명을 고쳐 **새 커널 두 번을 다시** 돌리고 기록을 마감했습니다(§13).

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 7 | 85 | 5 | 2 | 6 | 0 | 9 | 14 | 3 | **39** |
| 수정 뒤(`gates-wip-01.json`, `--no-exec`) | **27** | **333** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 `upgrade_gates.py … --label wip-01 --section 01`(G1·G2 먼저 잡기) → `gates-wip-01-01.json` 0건.
- `verify.py --chapter` → `PASS 6 sections / 63 code cells (max 25 lines)`(25줄은 아직 고치지 않은 02~06절 몫, 01절 셀은 최대 10줄). 빌드 HTML `01-입출력-출처-검증.html`의 `{{` 잔존 **0건**.

## 2. 수정 전 주요 문제

1. **한 셀에 함수 둘**(`validate_query`·`validate_answer`) + 그 셀에서 바로 모델 호출, 15줄 초과. 내포식 2·제너레이터 식·`set` 리터럴·f-string 2·타입힌트·`import re`.
2. **모델 답에 건 `assert` 둘**(`"[E01 p.1]" in answer.text`, `citations == ["[E01 p.1]"]`) — 규격 §3 위반, 다시 실행하면 멈출 자리.
3. 모델 설정에 **`reasoning_effort="none"` 없음**, `max_tokens=140`·`timeout=30`·`max_retries=0`.
4. 코드 셀 40/43개(챕터)에 첫 줄 주석 없음, 제목 셀·핵심 그림 첨부·결과 읽기 인용 없음(G5 9건).
5. 금지어 「반환」 3 · 「거부」 5 · 「정규화」 1, 긴 문장·영문 시작 문장(G6 14건).
6. 그림은 옛 `{{svg:01-흐름}}` 한 장, Mermaid·삽화 0장.
7. 실습 폴더 `guardrails.py`는 노트북이 한 번도 가져오지 않는 「두 번째 정본」이었고 클래스 3개·`@dataclass`·`@staticmethod`·`TypeVar`·내포식·f-string이 가득했습니다.

## 3. 챕터 리드 결정의 반영

| 결정 | 이 절에서 한 일 |
|---|---|
| 1. `guardrails.py` → `notebooks/guardrails.py`(도구 파일) | §4 |
| 2. PII 네 가지(이메일·전화번호·주민등록번호·카드 번호) | 도구 파일 `mask_pii`가 넷을 셈(테스트 2 통과). 02절 몫 → `handoff.md` |
| 3. `re`는 이 챕터에서 처음, `re.sub`·`re.findall`만 | **01절은 `re`를 쓰지 않음** — 출처 표시 뽑기를 `split("[")`·`split("]")`로 적음(b7 한 줄 「정규 표현식은 02절에서 처음 씁니다」). 도구 파일은 `re.findall`·`re.sub`만, 플래그 없음 |
| 4. 클래스·`@dataclass` 없음 | 도구 파일 클래스 0개(`GuardrailError`·`CallBudget`·`AuditLogger` → 함수와 딕셔너리). 테스트 최소 수정 §4-3 |
| 5. 모델이 쓴 글에 `assert` 금지 | 노트북 `assert`는 손 확인 셀의 세 줄(손으로 적은 글자에 대한 검사 함수 동작)과 자리 찾기 셀 하나뿐. 모델 답은 출력으로만 보임 |
| 6. `runs/` 덮어쓰기 | 01절은 파일을 쓰지 않음. 도구 파일 `write_audit_rows`가 `"w"`로 전체를 다시 씀(05·06절 몫 → 인계) |
| 7. 제목 금지어(05 「폴백」·06 「프롬프트」) 그대로 | 01절 해당 없음. 강사 확인 대상에 올림(§11) |
| 8. `key_and_model_cells("openai:gpt-5.4-mini")` | 그대로(`temperature=0`·`reasoning_effort="none"`). **`max_tokens=140`·`timeout=30`·`max_retries=0`은 쓰지 않음** — 답이 한 문장이라 출력 상한이 필요 없고(아홉 번 모두 한 문장), `max_retries=0`은 통신 오류 한 번에 노트북을 멈추게 하며, 규격 §3 기본 형태와 Ch 15 아홉 절을 그대로 잇기 위해서 |
| 9. 비유 계열 「도장과 도장 대장」 | 01절이 엶: 쪽지 세 장 = 검사할 답 셋, 도장 무늬 = 출처 표시, 대장 = 허용 목록, 손도장 = 표시를 찍는 쪽(삽화 `01-5`) |

## 4. 도구 파일 구조 작업 (§2-7)

### 4-1. 이동과 해시

| 파일 | 전 | 후 |
|---|---|---|
| 도구 파일 | `labs/part4/ch16-guardrails/guardrails.py` `d48a5869fad27e79…`(201줄) | **`labs/part4/ch16-guardrails/notebooks/guardrails.py`** `453d41c0149ab6e0e06545a65c265cf1e4005e03dae4ecf41df6e446b9f154fe` (`mv -n` 뒤 `ls`로 확인, 첫 판 `17968c63…` → 두 번째 판에서 함수 둘 나눔) |
| 테스트 | `tests/test_guardrails.py` `f0a512d68949c3b2…` | `632ab36c7a841c0e5b055a00cb155dbaa35e10d4df708287d9a43a86206fcf59` |
| `pyproject.toml` | `pythonpath = ["."]` | `pythonpath = ["notebooks"]`(`07695285…`) |

- `pytest -q tests` → **7 passed**(가상환경 `.cache/vm/venv-ch16-guardrails`, `-p no:cacheprovider`).
- 원본 사본: `qa/upgrade/before/guardrails.py`·`before/tests/`·`before/pyproject.toml`(준비 담당). 새 경로·새 해시 기록은 `qa/upgrade/manifest-changes.md`(manifest 원본은 고치지 않음).

### 4-2. 다시 쓴 도구 파일

- 함수 **26개**, 클래스 0 · 데코레이터 0 · 내포식 0 · `lambda` 0 · 조건 표현식 0 · f-string 0 · 기본값 매개변수 0 · 타입힌트 0 · 키워드 전용 인자 0(AST 확인). 함수 본문 최대 **9줄**(`summarize_history`·`reserve`·`retry_with_fallback`·`guarded_generate`). 두 번째 판에서 `safe_detail`(13줄)을 `safe_detail`·`safe_dict_of`·`safe_list_of`로, `guarded_generate`(12줄)에서 `quarantine_check`를 떼어 10줄 안으로 맞췄습니다.
- `import`는 `hashlib`·`json`·`math`·`os`·`re`(`re.findall`·`re.sub`만). numpy 없음.
- 함수마다 첫 줄 주석 `# Ch 16 NN절에서 배웁니다 — …`(01절 다섯은 「배웠습니다」). 노트북 판과 글자까지 맞추는 일은 그 절 작업자 몫.
- **01절 함수 다섯은 노트북 셀과 AST가 같습니다**(`validate_query`·`find_source_marks`·`unknown_marks`·`validate_answer`·`allowed_marks_of`, 비교 스크립트로 확인). 01 노트북은 도구 파일을 **가져오지 않습니다**(처음 가르치는 절이라). 02절부터 `from guardrails import …`.

### 4-3. 테스트를 고친 곳과 까닭(확인하는 성질은 그대로)

| 고친 곳 | 까닭 |
|---|---|
| import 줄: `AuditLogger`·`CallBudget`·`GuardrailError` → `make_audit_log`·`make_budget`·`record_event`·`reserve` | 결정 4(클래스 없음) |
| `pytest.raises(GuardrailError, …)` 7곳 → `ValueError` | 옛 `GuardrailError`는 `ValueError`의 자식 클래스였음. 메시지 `match=`는 그대로 |
| `validate_query(q)` → `validate_query(q, 500)` | 기본값 매개변수·키워드 전용 인자를 없앰(G1) |
| `validate_answer(ans, {("E01", 1)})` → `validate_answer(ans, ["[E01 p.1]"])` | `set` 리터럴을 쓰지 않고 허용 목록을 표시 글 목록으로 |
| `CallBudget(…)`·`budget.reserve(x)` → `make_budget(…)`·`reserve(budget, x)` | 결정 4 |
| `retry_with_fallback(primary, fb, wait=…)` → `retry_with_fallback(primary, fb, 2, …)` | 기본값 매개변수 없앰(옛 기본값 2 그대로 넘김) |
| `logger.record(…)` → `record_event(logger, …)` | 결정 4 |
| `guarded_generate(…)`에 `estimated_cost_usd=0.001, max_chars=500` 더함 | 기본값 매개변수 없앰(옛 기본값 그대로 넘김) |

- 테스트 이름 7개·검사하는 동작(공백 정리·빈 질문·허용 밖 출처·PII 넷의 개수·기록 경계·호출/비용 상한·`nan`/`inf`/음수·재시도 뒤 예비 답·감사 기록의 원문 없음·지어낸 출처 막기와 `blocked_output`·의심 문서 호출 전 격리와 `blocked_document`)은 그대로입니다. 테스트 파일 안의 `lambda`·내포식·`iter`/`next`는 학생 노트북이 아니라 그대로 두었습니다.

### 4-4. 옛 모듈과 동작이 달라진 곳(테스트가 보지 않는 곳 — 뒤 절 인계)

- 출처 표시: 옛 판은 정규식 `\[([A-Z]\d{2}) p\.(\d+)\]`로 **모양이 맞는 표시만** 뽑았고, 새 판은 **대괄호 안 글 전부**를 표시로 봅니다(b7에 한 줄).
- 재시도 대기: 옛 판 `0.05 × 2^(n−1)`초(지수로 늘림)·`retryable` 인자 → 새 판 **고정 0.05초**(`RETRY_WAIT_SECONDS`)·`TimeoutError`만.
- 감사 기록: 옛 판 `"a"`(덧붙이기) → 새 판 **기록 목록 전체를 `"w"`로 다시 씀**(결정 6).
- 문서 검사: 옛 판 정규식 넷(`re.I`, 「이전 … 무시」처럼 12자 안의 짝) → 새 판 **말 목록 일곱 개를 소문자로 바꾼 본문에서 찾기**(더 넓게 걸림).
- PII 정규식: 옛 판의 앞뒤 경계(`(?<!\d)`·`(?![\w.])`)를 뺐고 카드 번호는 `\d{4}` 네 묶음으로 바꿨습니다(테스트 2는 통과, 경계 사례는 02절이 판단).
- 통합 함수: 옛 판의 `model_error` 기록(모델 호출 예외)이 빠졌습니다. 06절이 되살릴지 판단.
- 오류 문장: 「질문은 N자 이하여야 합니다」 → 「질문이 너무 깁니다. 정한 상한: N」 등(테스트의 `match=` 말은 모두 남음).

### 4-5. 참조 파일 (챕터 밖 수정 — §9)

`textbook/part4/public-files.json` · `ch16-guardrails/qa/public-files.json` · `textbook/part6/prerequisite-files.json` · `textbook/part6/ch22-middleware/qa/prerequisite-files.json` · `textbook/part4/qa/check_bundle_execution.py` 51행 경로. `check_bundle_execution.py`는 **돌리지 않았습니다**(마감 몫). 읽어서 확인한 것: 묶음을 푼 실습 폴더에서 `uv sync --locked` → `uv run python -m pytest -q`(실습 폴더 맨 위, `pyproject.toml`의 `pythonpath = ["notebooks"]`로 도구 파일을 찾음) → 해시는 `ROOT/labs/part4/ch16-guardrails/notebooks/guardrails.py`를 그때 읽어 계산(값을 적어 두는 곳 없음).

### 4-6. Ch 22 본문이 Ch 16을 인용하는 자리

- `_src/01`(두 곳)·`02`(여러 곳)·`03`·`04`·`05`·`06`을 `grep`으로 모두 읽었습니다. **파일 경로(`guardrails.py`·`labs/…`)를 적은 문장은 0건**이라 고치지 않았습니다. Ch 22 노트북에도 `guardrails`·`ch16` 문자열 0건.
- 뜻 대조: 「Ch16 02절에서 정규식으로 이메일·전화번호·주민등록번호·카드 번호를 …」(결정 2와 맞음), 「Ch16 04절과 05절에서는 호출 한도와 재시도를 함수로 직접 만들었습니다」·「Ch16 04절에서는 비용 상한을 넘으면 호출을 멈추는 함수를 만들었습니다」(결정 4 — 클래스를 함수로 바꾼 뒤 오히려 더 맞음), 「Ch16 03절에서는 대화 기록을 자르고 요약하는 함수를 직접 만들었습니다」·「Ch16 05절에서 재시도와 함께 감사 로그를 직접 남겼습니다」 — 02~05절 작업자가 이 뜻을 지켜야 합니다(인계).
- 옛 경로가 남은 기록 파일(고치지 않음): `ch16-guardrails/qa/technical-review.md`(2026-09-10 검토 기록) · `textbook/part6/ch22-middleware/qa/research.md` 24행 · **`textbook/part6/qa/final-artifact-hashes.json` 351행**(옛 경로·옛 해시, 이 파일을 읽는 스크립트는 `textbook` 안에 없음 — 마감 확인 대상).

## 5. 설계 — paired

- 공통 재료(노트북 1~5절): 자료 파일 `data/retrieved-documents.json`(문서 둘)에서 `E01`만 이 절의 검색 결과로 고름 → 이 절에서 정한 값(`max_chars = 500`, 시스템 메시지 글) → 질문 넷(모델에게 보낼 질문 하나 + 검사용 셋: 빈칸 붙은 질문 23자·빈 질문 3자·700자 질문) → **모델 요청 한 번** → 이 절에서 손으로 적은 합성 답 둘(`[E02 p.1]`을 적은 답, 표시 없는 답)과 모델 답 = 검사 대상 답 셋.
- **Before**(`lesson_part="before"`): 검사 없이 받는 흐름 — 질문 셋·답 셋을 그대로 목록에 담음 → `막은 질문 수: 0`·`막은 답 수: 0`이 결함(그림 `01-3` 왼쪽 칸 빨강 두 상자).
- **After**(`lesson_part="after"`): 입력 검사 `validate_query`(빈칸 정리·빈 질문·상한) → 질문 둘을 막음, 출력 검사 `validate_answer`(= `find_source_marks` + `unknown_marks`, 허용 목록은 `allowed_marks_of(retrieved)`) → 답 둘을 막음. 손으로 적은 글자에 `assert` 세 줄.
- **대조 대상**: 답의 출처 표시를 **이번 검색 결과 문서로 만든 허용 목록 `['[E01 p.1]']`**과 글자끼리 견줌. 합성 가짜 표시 `[E02 p.1]`은 자료 파일에 없는 문서 ID로 손으로 적음(노트북 5절 출력과 b7에 「이 절에서 손으로 적은 답」).
- **값 바꿔 보기**: 허용 목록을 손으로 `[E02 p.1]`까지 넓히면 같은 합성 답이 통과(`넓힌 목록에서 남은 밖 표시: []`).
- 노트북은 설명하려고 요청(5절)과 검사(7~9절)를 나눴습니다. 본문 「두 검사가 맡는 자리」에 그 차이를 한 단락으로 적었습니다(구조 도식 `01-1`은 검사를 붙인 뒤의 차례).

## 6. 흔들림 확인 (규격 §2-7 10번 끝) — `qa/upgrade/01-probe.md`

- 노트북 실행 **전에** 같은 요청(시스템 메시지 + `E01` 문서 + 질문)을 노트북 밖에서 **다섯 번** 보냈습니다: 다섯 번 모두 답 끝에 `[E01 p.1]`, 답 글자 수만 72·73(마침표 차이). 입력은 그대로 두었습니다.
- 노트북 새 커널 네 번(A·B·C·D)도 모두 `[E01 p.1]` — 아홉 번 모두 같은 표시·같은 문장, 마침표만 갈림. 본문 b7에 「노트북을 쓰기 전에 같은 요청을 따로 다섯 번 보냈습니다…」와 「같은 요청도 실행한 때에 따라 답 문장이 달라질 수 있습니다」를 적었습니다.

## 7. 실행값 (교재 코드 새 커널 두 번 — C 09:06:27 · D 09:06:44 UTC)

- `code_sha256` `3538ba129a33e2e4e17a44844580ff745d89da430481b2e8f7f1b89bb18c8d23`(두 번 같음). `outputs_sha256` C `afe9c2ca…` · D `c2aeed27…` → **셀별 출력 글자 24/27 같음**. 다른 셋(코드 셀 10·14·25 = 5절 모델 답, 6절 내보낸 답 표 첫 줄, 9절 통과한 답)은 **모델 답 끝 마침표 하나**만 다릅니다(C 있음, D 없음). **교재 출력은 C**(`run_section.sh`가 실행한 판).
- 두 번 모두 같은 값(본문·그림·정리에 쓴 값): `자료 파일의 문서 수: 2` · `이번 검색 결과의 문서 수: 1` · `정한 질문 글자 수 상한: 500` · `질문별 글자 수: 23 3 700` · 답 끝 `[E01 p.1]` · Before `막은 질문 수: 0`·`막은 답 수: 0` · After `막은 질문: 질문이 비어 있습니다.`·`막은 질문: 질문이 너무 깁니다. 정한 상한: 500`·`검사를 통과한 질문 수: 1`·`정리 전 글자 수: 23`·`정리 뒤 글자 수: 15` · 뽑은 표시 `['[E01 p.1]']`·`['[E02 p.1]']`·`[]` · `허용 목록: ['[E01 p.1]']` · `막은 답: 검색 결과에 없는 출처: [E02 p.1]`·`막은 답: 답에 [문서ID p.쪽] 출처 표시가 없습니다.`·`검사를 통과한 답 수: 1` · 값 바꿔 보기 `넓힌 목록에서 남은 밖 표시: []`·`이번 검색 결과 목록에서 남은 밖 표시: ['[E02 p.1]']`.
- 흔들린 값(모델 답 문장·글자 수)은 결과 읽기에 「실행마다 문장이 다를 수 있습니다」로만 두고 그림·캡션·정리·복습에 넣지 않았습니다.
- 준비물 「노트북 전체가 약 5초」는 C의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답 4.57초, 커널 기동 제외)에서 읽은 값입니다(Ch 15 선례). b7 「걸린 시간과 비용은 재지 않았습니다」는 코드로 잰 것이 없다는 뜻입니다.

## 8. 서비스 요청과 비용

- 노트북 한 번 실행에 **1번**(`gpt-5.4-mini`, 임베딩 0) — 준비물·b5에 적음. 일반 절이라 요청 수만으로 강사 확인 대상에 올리지 않습니다(규격 §7-2).
- 이 절 작업 전체 **9번**: 흔들림 확인 5 + 노트북 A·B(첫 판) + C·D(두 번째 판). 첫 판에서 이보다 더 실행했는지는 남은 기록(`~/ch16work/nb-runA*.ipynb`·`nb-runB.ipynb`)으로 확인할 수 없었습니다. 예상 비용 합계 약 **0.003달러**(요청 하나에 입력 약 150·출력 약 40토큰으로 셈, 청구 금액 아님).

## 9. 그림 — `qa/upgrade/01-figures.md`

- Mermaid **4장**: `01-1`(b4, 원본 폭 432) · `01-2`(b5, 521) · `01-3`(b6, 573, **빨강은 Before 결함 두 상자뿐**) · `01-4`(b6 값 바꿔 보기, 450). 네 장 모두 PNG를 직접 열어 도식 읽기와 맞는지 봤습니다. 두 번째 판에서 `01-3` 오른쪽 칸 제목을 「After · 출력 검사를 붙인 흐름」으로 고쳐 다시 렌더했습니다. 옛 `figures/01-흐름.*`은 그대로 둠(본문 참조 0).
- 삽화 **1장** `01-5-쪽지-세-장과-도장-대장`: `nano_banana_pro`(응답 모델 이름 `nano_banana_2`) · 16:9 · 2k · **1차 job `daf169d3-aa44-4f22-a3d1-7c96494049a4` 채택**(재생성 없음) · 2크레딧 · 잔액 2644.5 → **2642.5**(두 번째 판에서 `balance`로 확인). 원본 `cc4224b3…`(2752×1536) → 저장 1100×614 `0df47a1f…`. 두 번째 판에서 결과 원본을 같은 폭으로 줄여 저장 PNG와 다시 픽셀 대조: bbox `None`, 세 칸 extrema `(0, 0)`. 저장 PNG를 직접 열어 그림 읽기(쪽지 셋·파란 둥근 무늬/붉은 네모 무늬/무늬 없음·대장의 파란 둥근 무늬 하나·손도장)와 맞는지 봤습니다.

## 10. 검사

- 게이트 0건(§1) · `verify.py --chapter` PASS · `{{` 0건 · 새 커널 두 번(§7) · `pytest` 7 passed · 생성기 `SRC_HTML`·`cells()`가 `_src`·노트북 설명 셀·코드와 같음(첨부 그림과 `lesson_part` 경계 분할만 다름) · 금지어 직접 `grep`(「조각」 두 곳을 두 번째 판에서 고침, 나머지 0).
- `_build.py`를 한 번 더 돌려 챕터 HTML 일곱 개의 sha256이 모두 같았고 일곱 개 모두 `{{` 0건.
- `pack.py` → `qa/upgrade/review-pack/01-입출력-출처-검증.md`.
- 보호 파일 7개: §12.

## 11. 강사 확인 대상

1. **05·06절 제목의 금지어**(「폴백」·「프롬프트」) — 결정 7대로 이번에 바꾸지 않음(파일 이름·목차·묶음 목록 파급).
2. **테스트 파일을 고친 것**(§4-3) — 확인하는 성질은 같고 부르는 모양만 바뀜.
3. **도구 파일의 동작 차이**(§4-4) — 특히 문서 검사가 말 목록으로 넓어진 것과 `model_error` 기록이 빠진 것(06절 판단).
4. **합성 답 둘은 이 절에서 손으로 적은 답**(`[E02 p.1]`은 자료 파일에 없는 문서) — 본문·노트북에 밝힘.
5. **모델 설정에서 `max_tokens`·`timeout`·`max_retries`를 뺀 것**(§3 결정 8).
6. 교재 출력 환경 `langchain-core 1.6.4`·`openai 3.19.0` ↔ 학생 잠금 `1.6.2`·`3.11.0`(잠금 판 동작은 확인하지 않음).
7. 한국어 감사 3단·삽화 판독은 별도 세션 몫.

## 12. 보호 파일 7개 (`before-manifest.json`, 원본은 고치지 않음)

| 파일 | 상태 |
|---|---|
| `labs/part4/ch16-guardrails/data/retrieved-documents.json` | 같음 `ae2fe4f4…` |
| `labs/part4/ch16-guardrails/runs/05-audit.jsonl` | 같음 `0d7d9da8…` |
| `labs/part4/ch16-guardrails/runs/06-audit.jsonl` | 같음 `9d705d17…` |
| `labs/part4/ch16-guardrails/guardrails.py` | **의도한 이동** → `notebooks/guardrails.py` `453d41c0…`(옛 자리에는 없음) |
| `labs/part4/ch16-guardrails/tests/test_guardrails.py` | **의도한 변경** `632ab36c…`(§4-3) |
| `labs/part4/ch15-evaluation-advanced/runs/batch-eval-input.jsonl` | 같음 `0177cebc…` |
| `labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json` | 같음 `dc48b1bc…` |

기록: `qa/upgrade/manifest-changes.md`.

## 13. 두 번째 판에서 고친 것 (첫 판 결과를 다시 읽고)

- **코드 두 곳**(다시 실행한 까닭): 질문 셀 `"도서관 휴관일" * 100` → `repeat_count = 100`(규격 §2-3 「식 안의 숫자」, Ch 15 B-6 선례) · 손 확인 셀 `500` → `max_chars`. 출력은 첫 판과 같음.
- **설명**: 「조각」(Ch 5 토큰 전용 금지어) 두 곳 → 「나눈 글」 · 처음 쓰는 `raise`·`" ".join(목록)`·`not 빈 글`·글 곱하기·역할 딕셔너리 메시지(Ch 5 04·Ch 6 01)를 한 문장씩 · 「~하고, ~하고, ~합니다」 세 가지 잇기 한 문장을 둘로 · Before 결과 읽기의 「그대로 모델에 나갑니다」(실행하지 않은 동작) → 「보낼 목록에 그대로 들어갑니다 / 실제로 보내지는 않았습니다」.
- **본문**: b3 앞 내용 대조를 바로잡음 — 첫 판의 「Ch 9 05절에서 답 끝에 출처를 적게 했다」·「Ch 12에서 쪽 번호를 남겨 두었다」는 실제 절과 맞지 않아, **Ch 8 02절 출처 표시 → Ch 9 01절 `find_cited_marks()`(목록의 표시 가운데 답에 든 것만 모음) → Ch 9 04절 「목록에 없는 표시는 결과에 나오지 않는다」**로 고치고 이 절이 방향을 거꾸로 잡는다고 적음(두 절 `_src`·노트북에서 확인). b2·b6·b7의 질문 쪽 문장을 「실행하지 않았다」에 맞춤. 「두 검사가 맡는 자리」에 노트북 차례와 그림 차례의 차이 한 단락. 그림 설명의 「갈래」(점선 뜻) → 「화살표가 둘로 나뉩니다」. b10 참고 자료 설명을 확인한 문서 내용(역할 딕셔너리 꼴, `text`)에 맞춤(2026-09-23 두 문서 모두 열림 확인).
- **도구 파일**: 함수 본문 10줄 넘는 둘을 나눔, 02~06절 주석을 「배웁니다」로.

## 14. 지우지 않은 것 (삭제 승인 대상)

- `labs/part4/ch16-guardrails/__pycache__/guardrails.cpython-312.pyc`(옮기기 전 모듈의 바이트코드) · `labs/…/notebooks/__pycache__/` · `labs/…/tests/__pycache__/`(테스트 실행이 만든 것).
- `qa/upgrade/gates-wip-01-01.json`(첫 실행 전 G1·G2 확인, `gates-after.json`으로 갈음될 것).
- `qa/upgrade/__pycache__/`(두 번째 판에서 생성기를 `importlib`로 읽어 `_src`·노트북과 대조할 때 생김) · 기기 `/tmp/ch16-01-html-before.txt`(`_build.py` 두 번 해시 대조용).
- 작업 사본: 세션 홈 `~/ch16work/`(`probe01.py`·`nb-runA-input.ipynb`·`nb-runA.ipynb`·`nb-runB.ipynb`·`reps01.json`·`illu/` 원본 2752px 둘과 줄인 사본, `w2/`의 패치 스크립트·`nb-runC.ipynb`·`nb-runD.ipynb`·고치기 전 사본 둘). 마운트 폴더 밖이라 학생 묶음과 무관합니다.
- 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}`(마감에서 삭제 승인, 사본 `before/figures/`).

## 15. 챕터 마감 검토 반영 (2026-09-23)

검토 보고서 `review-round1-A.md`(A-n)·`review-round1-B.md`(B-n), 챕터 전체 기록은 `chapter-summary.md`와 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-23)」.

- **다시 실행했습니다(검토 A-2·A-10, 챕터 리드 결정)** — 출력 라벨 둘을 바꾸려고 생성기를 고친 뒤 새 커널 두 번: C 13:14:05·D 13:14:17 UTC(`run_section.sh` 대신 같은 환경 변수로 `author_01.py` → `execute.py`, D는 세션 홈 `~/ch16work/close/nb01-D.ipynb` 사본). `code_sha256` `3538ba12…` → **`2f3497f840d5…`**, `outputs_sha256` C(교재 출력) **`b0cdc5312314…`** · D `7d741188e5b6…`. 셀별 출력 **24/27 같음**, 다른 셋(셀 23·33·57)은 모델 답 끝 마침표 하나(전과 같은 모양). 모델 요청 2번(C·D) 더.
  - 라벨: `지킬 말:` → **`시스템 메시지:`**(과정에서 「지킬 말」은 Ch 8 03의 「꼭 남아야 할 말 목록」), `그대로 보낸 질문 수:` → **`보낼 목록에 담은 질문 수:`**(실제로 보내지 않았으므로). 주석 셋(정한 값·요청 셀·Before 질문 셀)과 설명 셀 넷을 같은 뜻으로.
  - 본문·노트북의 인용 값은 새 출력과 다시 대조했습니다(`_src` `<code>` 가운데 출력·코드에 없는 것은 앞 챕터 인용 `[E01 p.3]`·`find_cited_marks()`·`try/except 이름 as error`뿐, 결과 읽기 첫 단락 숫자 인용 0건 어긋남, 게이트 G5 0).
- **A-7** 본문의 노트북 절 번호를 「노트북 5절」·「노트북 7~9절」·「노트북 3절」·「노트북 9절」로.
- **A-8** 「허용 목록」을 세 그림 모두 **노랑**(출력으로 확인한 값 `허용 목록: ['[E01 p.1]']`·`넓힌 허용 목록: …`)으로 — `01-1` 초록 → 노랑, `01-4` 두 목록 파랑 → 노랑(두 판은 라벨로 가름), `01-2`는 이미 노랑. alt·도식 읽기·「오늘 볼 그림」 읽기 함께.
- **A-9** `01-3` 칸 안 화살표를 「받은 답 셋」에서 두 결과로 나란히(`b1 --> b2`·`b1 --> b3`, After도 같게). 폭이 953이 되어 라벨을 줄임(「내보낸 답 셋」·「막은 답 둘 / 목록 밖 출처 / 출처 표시 없음」) → 원본 폭 **856**.
- **B-1**(챕터 전체에 맞춤) 준비물·b5 「예상 비용은 미화 0.01달러 아래」 → 「노트북을 한 번 실행하는 요금은 요금표로 어림해 미화 0.01달러 아래」, b7 「요청 수와 요금 어림만」.
- 그림 다시 렌더 `01-1`·`01-2`·`01-3`·`01-4`(폭 432·531·856·450), PNG 넷을 직접 열어 도식 읽기와 맞는 것을 확인. 노트북 첨부 `01-1` 새 PNG.
