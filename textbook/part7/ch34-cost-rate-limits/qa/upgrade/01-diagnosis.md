# 01절 진단과 개선 기록 — 프롬프트 캐시 계측 (experiment, 실제 모델)

- 작업일 2026-09-29(UTC 21:4x~22:5x). 생성기 `qa/upgrade/author_01.py`(`5dcc6aec…`). 규격 `textbook/QUALITY-UPGRADE.md` §2·§2-7·§3·§4·§5-3·§5-4·§6. 챕터 리드 결정은 `qa/upgrade/handoff.md` 「챕터 공통」.
- 이 절은 **이번 품질 개선의 마지막 챕터 첫 절**이고, 챕터 공통(용어 표·도구 파일 첫 판·색·비유 계열)을 엽니다.

## 1. 게이트 전후

| | 코드 셀 | 코드 줄 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 5 | 38 | 79 | 5 | 3 | 5 | 1 | 6 | 10 | 3 | **33** |
| 수정 뒤(`gates-wip-01.json`, `--no-exec`) | **22** | 112 | **366** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 코드 줄은 `count_code.py`(주석·빈 줄 뺌). 도구 파일 `cost_tools.py` 코드 줄 10(따로). 준비 셀 밖 셀 최대 7줄 · 함수 본문 최대 4줄 · 호출 깊이 최대 2(AST 따로 — `/tmp/ch34-01/pregate.py`, 사본 `.cache/ch34-01/tools/pregate.py`).
- AST 따로 0건: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·별표 풀기·`+=`·대입 풀기(for 포함)·`while`·`try`·`raise`·클래스·데코레이터·힌트·기본값 매개변수·`key=`/`reverse=`·`set`·`next`·`enumerate`·`zip`·`sum`·`max`·`min`·`all`·`any`·`isinstance`·`getattr`·`sorted`·노트북 `.get`·한 글자 변수·비동기. 처음 쓰는 이름은 결과 읽기에서 한 문장씩: `uuid.uuid4().hex`·`str.find`·`//`·`%`·`round`·`response_metadata["token_usage"]`.
- 과정 금지어(산문, 코드 백틱 뺌): 0건 — 예외 한 곳씩(노트북 1절 첫 문장·본문 b2) 「제목의 프롬프트 캐시 계측은, …」(제목 풀이 문장, Ch 15 03·Ch 30 선례 — **강사 확인**). 사용자가 금지한 표현(과정 규칙) 0건.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2-01·§12 확인)

1. 준비 셀이 `Path.cwd()`에서 위로 `ch34-cost-rate-limits`를 찾음 → 루트 커널(`run_section.sh`)에서 `FileNotFoundError` · `next(… for …)`·`(here, *here.parents)`·조건 표현식·한 글자 변수 `p`.
2. 모델 셀에 `temperature=0` 없음(G4), 대신 `seed=34`·`max_tokens=40`·`max_retries=1` · 한 셀에 요청 두 번 + 파일 쓰기 + 세미콜론(15줄).
3. **흔들리는 값에 `assert`**(`records[1]["cached_read"] >= 1024`) · 결과를 `runs/cache-measurement.json`에 씀(실행마다 해시가 바뀌어 공개 목록·zip과 어긋남).
4. **틀린 사실**: b3 「Ch 15에서는 추적 항목에서 캐시 읽기와 생성을 구분했습니다」(거짓 — Ch 15 05·06은 캐시 입력 토큰 수만) · b6·[9]·목표 3 「LangChain `usage_metadata`에서 별도 생성 값을 얻지 못해 None」(부정확 — 설치판은 서버가 `cache_write_tokens`를 보내면 `cache_creation`에 담음, 이번 응답에서 그 값이 None) · b4 「자동 캐싱이 1,024토큰 이상의 프롬프트에서 적용」(GPT-5.6 이후 규칙 — 앞 모델은 설정마다 다름) · b10 `…/prompt-cache-diagnostics` 404.
5. 금지어: 「캐시」 단독 24·「접두어」 14·「적중」 5·「프롬프트」 4·「지연」·「반환」·「측정」·「추정」·「메타데이터」·「대시보드」·「식별자」·「필드」·「보장」·「계측」·「냉·온」, 비유 「신청서」(Ch 6 「신청서 양식」과 겹침).
6. 결과 읽기 0 · 첫 줄 주석 0 · 제목 셀·그림 0 · 준비물(요청 수·비용)·실행일 없음 · Mermaid 0·삽화 0·설계표 없음.

## 3. 설계 (챕터 리드 결정 1~4·12·13 적용)

- **모델**: 과정 표준 셀(`nbkit.model_source` — `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`), 요청은 글 하나로 `invoke`(Ch 6 01). 요청 **넷**(실행 1 A·B + 실행 2 C·D).
- **실험(experiment)**: 가설(공식 안내 「Cache reuse requires the entire rendered prefix to match」·「place those at the end rather than the beginning」) → 실행 1(문의 글을 정책 글 **뒤에**) → 실행 2(**값 하나만 — 문의 글의 자리를 정책 글 앞으로**) → 결과 표(5절) → 요금 어림(6·7절) → 결론.
  - 공통: 규칙 문장(60자) × 100 = 정책 글 6000자(설치판 tiktoken으로 약 3,100토큰 — 노트북 밖, Ch 6 06 80번보다 김) · 문의 글 둘(첫 글자부터 다름, 한 낱말 답) · **실험 번호** `"실험 번호 " + uuid.uuid4().hex`(38자, 출력하지 않음 — 앞 실행 캐시와 맞지 않게, Ch 6 06의 「작성 시각」과 같은 목적) · `make_request(mark, first_text, second_text)`(번호 + 줄바꿈 + 앞 글 + 줄바꿈 + 뒤 글).
  - `prompt_cache_key`는 쓰지 않음(개념을 늘리지 않으려고 — b7에 「이번에 실행하지 않았습니다」).
- **흔들림 확인(첫 요청 전 §0)**: `qa/upgrade/probe/01-probe.md` — §0 저장 **22:30:10Z**(저장 시각 줄 22:30:16Z), 첫 요청 **22:30:24Z**. 5회차 × 4 = **20번**(22:30:22Z~22:30:53Z, 오류 0).
  - **설계로 정한 값 5/5**: A·C·D 캐시 입력 `0` · 키 `cache_creation` 없음(20/20) · 사용량 원본 `cache_write_tokens` `None`(20/20) · 128의 배수·≤ 입력(20/20) · 같은 회차 안 A = C·B = D 입력 토큰 수.
  - **서비스 판단 값 5/5**: B 캐시 입력 > 0(다섯 번 모두 `2816`).
  - 판단: 입력 그대로. 결론·그림 라벨은 설계로 정한 값 + 「B > 0」(5/5 **그리고** 새 커널 두 번 — 아래 4)만, B의 수·토큰·요금·답 글은 결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만.
- **파일 쓰기 없앰**(챕터 리드 결정 3): 노트북 쓰기 0 — `runs/cache-measurement.json`은 옛 파일 그대로(`60c66098…`, 전후 같음). 공개 목록 두 곳의 그 줄·삭제 승인은 **마감 몫**(01은 기록만).
- **파일 위치 셀 — 넣지 않음**: 01은 실습 폴더의 파일을 **읽지 않음**(도구 파일은 가져오기로만 — 학생은 `notebooks/`에서, 교재 출력은 `run_section.sh`가 노트북 폴더를 `PYTHONPATH`에 더함). 옛 준비 셀(폴더 찾기)은 `runs/` 쓰기용이라 함께 뺌. 뒤 절이 실습 폴더 파일을 읽으면 Ch 30 과정 표준 파일 위치 셀(세 자리)을 그 절이 넣음(handoff).
- **도구 파일 `notebooks/cost_tools.py` 첫 판**(이름 겹침 없음 — 준비 노트 §8): Ch 6 06 `estimate_cost`를 Ch 29 `eval_tools.py`(마감 판 `d624b8f3…`)에서 설명 주석·본문 글자 그대로(주석 `# Ch 6 06절에서 배웠습니다 — Ch 29 도구 파일 eval_tools.py의 같은 이름 함수를 옮겼습니다`). **01 판 `af9e128825c0888311dd254337a5ba8c5f3469824fb5fff6da5e340830bdb207`**, 함수 하나, 가져오기 0, 코드 줄 10.
  - 대조 사슬(생성기 `check_tools()`): Ch 29 파일 해시 확인 → 블록 글자 대조 → AST 같음 → **Ch 6 06 노트북 셀 함수와 AST 같음·def~return 글자 같음**. 쓰기 가드 `write_tools()`: 없거나 01 판과 같을 때만 쓰고, `strip_later_imports()` 뒤 01 판으로 시작하는 긴 판은 건너뜀, 그 밖은 멈춤. 뒤 절 생성기는 `author_01.TOOLS01`·`TOOLS_HEAD`·`strip_later_imports`·`check_tools`·`file_block`을 가져다 씀.
  - 가져오는 셀 결과 읽기에 고정 세 문장 + 커널 폴더 한 문장 + 실행 도구 한 문장(Ch 30 09 모양).
  - 공개 목록 두 곳에 한 줄: 챕터 `qa/public-files.json`(`44f3c331…` → `cfbb3767…`, 05 노트북 줄 뒤) · Part `textbook/part7/public-files.json`(`d822ee88…` → `46cb1691…`, 정렬 자리 106행) — `collect_public_files.py`와 같은 셈을 메모리에서 해 결과가 같음을 확인(스크립트는 실행하지 않음 — 선행 목록을 다시 쓰므로). **`part7-practice.zip`은 다시 만들지 않음**(마감 몫).
- **준비 셀**: 설치 `%pip`(langchain 1.4.0·langchain-openai 1.6.0·python-dotenv 1.2.3 — 잠금과 같음, dev `pip==26.2` 있음) → 가져오기(`uuid`·`init_chat_model`·`from cost_tools import estimate_cost`) → 키 셀(`nbkit.KEY`) → 모델 셀(보이게).

## 4. 실행

- 첫 실행 전: `/tmp/ch34-01/tryA`에서 모델 요청 셀을 뺀 사본(결정적 셀 13개 + 시험 셀)을 `notebooks/` 자리 커널로 실행 — PASS, 요청 0 · 게이트 `--label wip-01 --section 01` G1·G2 0(G6 1은 자리 표시 글, G7은 그림 전).
- **새 커널 A**(`run_section.sh`, 프로젝트 맨 위 커널, `executed_at` **2026-09-29T22:43:28Z**) — PASS 22셀, `code_sha256` `f5a17ed5befb…`, `outputs_sha256` `0a7c2201e492…`(그림 첨부 단계에서 멈춤 — 그림 전이라 예상한 일, 실행·저장은 끝난 뒤).
- **새 커널 B**(생성기 `--nb-copy /tmp/ch34-01/B` 사본, `--cwd labs/…/notebooks` 학생 자리, `PYTHONPATH` 없이, 22:43:50Z) — PASS 22셀, `code_sha256` 같음, `outputs_sha256` `e7b20c677578…`.
- **셀별 출력 22개 가운데 15개 같음**. 다른 일곱 = 입력 토큰 수가 든 셀과 그 수로 셈한 셀: [10]·[12]·[14]·[15] 입력 토큰 3166·3170 ↔ 3163·3167 · [17] 표 · [21] 요금 표 · [22] 합 0.002892·0.004792 ↔ 0.002887·0.004788. 까닭: 맨 앞 실험 번호(무작위 32글자)가 토큰 몇 개로 나뉘는지가 실행마다 다름. **캐시 입력(A·C·D 0, B 2816)·128로 나눈 나머지 0·몫 22·키 없음·원본 칸·참·거짓 값(`True`·`False`)·답 글(배송·환불)은 두 커널 모두 같음**.
- 흔들리는 값 채우기: 생성기·노트북 마크다운·`_src`의 `[[…]]` 자리 20개를 A 출력으로 `mdpatch.py`(치환 목록 `.cache/ch34-01/reps1.json`·`reps2.json`) — 재실행 없음. 채운 뒤 생성기 메모리 실행 결과가 노트북 셀 47/47·`_src`와 글자까지 같음(`genmatch.py`), 노트북 코드·출력은 A 그대로(22/22).
- 저장 출력: Traceback·임시 파일 위치·응답 ID·시각·키 0(모듈 이름 `uuid` 한 번은 가져온 이름 출력).

## 5. 교재 출력 값 (A)

| 요청 | 입력 | 캐시 입력 | 128 나머지 | 답 | 예상 비용(할인) | 할인 없이 |
|---|---|---|---|---|---|---|
| 실행 1 첫 요청(뒤에) | 3166 | 0 | 0 | 배송 | 0.002393 | 0.002393 |
| 실행 1 둘째 요청(뒤에) | 3170 | **2816** | 0 | 환불 | **0.000499** | 0.0024 |
| 실행 2 첫 요청(앞에) | 3166 | 0 | 0 | 배송 | 0.002393 | 0.002393 |
| 실행 2 둘째 요청(앞에) | 3170 | 0 | 0 | 환불 | 0.0024 | 0.0024 |

- 합 실행 1 0.002892 ↔ 실행 2 0.004792(`실행 1의 합이 더 적은가: True` — 둘째 단락·b6 표만). 몫 22.
- **결정적 값(결론·그림 라벨)**: 두 실행 첫 요청 0 · 실행 2 둘째 요청 0 · 네 요청 나머지 0 · 키 `cache_creation` 없음 · `cache_write_tokens` None · 같은 문의 글끼리 입력 토큰 수 같음 `True True` · 정책 글 6000자·번호 38자·요청 글 6097자·자리 39·97 · 요금표. **서비스 판단 값(한정어와 함께 결론)**: 실행 1 둘째 요청 캐시 입력 > 0(흔들림 확인 다섯 번과 두 커널). **흔들린 값(둘째 단락·표·확인할 점·b7)**: 입력 토큰 수·캐시 입력 수 2816·몫·출력 토큰·답 글·예상 비용·합.

## 6. 서비스 요청 수와 요금표 어림 (청구 금액 아님, 요금 `https://developers.openai.com/api/docs/models/gpt-5.4-mini` 2026-09-29 확인 — 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰)

| 단계 | 요청 | 어림 |
|---|---|---|
| 노트북 밖 흔들림 확인(5회차 × 4) | 20 | 약 0.038달러 |
| 새 커널 A | 4 | 0.007684달러(노트북 합 0.002892 + 0.004792) |
| 새 커널 B | 4 | 0.007675달러 |
| 모델 없는 준비(소스·tiktoken·마른 실행·tryA) | 0 | 0 |
| **합** | **28** | **약 0.054달러** |

- 노트북 한 번 = 요청 4 · 약 0.0077달러(준비물 「0.01달러보다 적음」). 절 1달러 상한 안. 서비스 오류 0.

## 7. 고친 틀린 사실과 앞 챕터 이음

- b3 「Ch 15에서 캐시 읽기와 생성을 구분」 → 「Ch 15 05·06은 캐시 입력 토큰 수만 적었고, 캐시 쓰기 토큰은 다루지 않았습니다」.
- 「LangChain이 캐시 생성 값을 못 줌」 → 사용량 원본(`response_metadata["token_usage"]["prompt_tokens_details"]`)을 출력해 `cache_write_tokens: None`을 보이고, 설치판이 `cached_tokens` → `cache_read`, `cache_write_tokens` → `cache_creation`(None이면 키를 만들지 않음 — `chat_models/base.py` 4339~4385)으로 옮긴다는 사실을 「소스로 확인」으로 가름. 공식 안내: 캐시 쓰기 요금은 GPT-5.6 이후만(앞 모델 「No additional cache-write charge」).
- 「1,024토큰 이상에서 적용」 → 「GPT-5.6 앞 모델은 설정마다 다름」 + Ch 6 06 탐색(50번 약 1,250토큰에서 0) 이음.
- 옛 b10 404 링크 뺌. 참고 자료 넷(Prompt caching·GPT-5.4 mini·LangChain Messages·설치판 소스), 모두 2026-09-29 확인.
- 이음: Ch 6 06(캐시 입력·`estimate_cost`·요금표 키·긴 시스템 메시지 두 번·맨 앞 작성 시각) · Ch 6 01(글 하나로 invoke) · Ch 15 05(첫 요청에도 캐시 입력)·06(캐시 입력만큼 예상 비용 줄어듦) · Ch 5(토큰) · Ch 28·30 접근 토큰과 다른 말.

## 8. 그림

- 설계표 `qa/upgrade/01-figures.md`(작업 차례로는 설계표를 쓴 뒤 렌더 — 다만 설계표에 쓴 시각 줄이 없고 첫 렌더 뒤 메모를 덧붙여, 파일 시각으로는 확인되지 않음: 마감 검토 C-5) · Mermaid **4장**(01-1 요청 글의 두 차례 588 · 01-2 실행 1의 두 요청 241 · 01-3 사용량 칸이 옮겨지는 자리 746 · 01-4 문의 글의 자리만 바꾼 두 실행 554 — viewBox 폭, 모두 868 이하, PNG를 열어 확인, 두 장은 `<br>`로 고쳐 다시 렌더) · 빨강 0 · 보라는 01-2 모델만.
- 삽화 **1장** `01-5-미리-채워-둔-배터리`(비유 계열 **「충전 거치대와 배터리」** — 01이 엶): job **`168634ae-564d-4b38-9b95-54e91ed80670`** 1차 채택(재생성 0) · 거래 2026-09-29T22:46:51.829523Z 「Nano Banana Pro −2」 → **이 절 2크레딧**(잔액 2247 → 2245) · `jobs_wait` 모델 표시 `nano_banana_2`(요청 `nano_banana_pro` — 기록만) · 원본 `18a599b7…`(2752 × 1536) → 저장 1100 × 614 `353a9510…` · 결과 URL 다시 받아 픽셀 대조 bbox `None`·최대 차이 0 · 저장 PNG를 열어 셈(위 초록 다섯·주황 하나 / 아래 주황 여섯). 거의 흰 가로줄 108 / 614.
- 캡션 파일 다섯이 생성기 `FIGn_CAP`·`ILLU_CAP`과 같음.

## 9. 검사

- `run_section.sh … 01 --no-exec`: 렌더 → 첨부 1 → 빌드 → `verify.py --chapter` **PASS 5 sections / 43 code cells (max 19 lines)**(19줄은 02~05 옛 판) → 게이트 wip **G1~G7 0 PASS**.
- 빌드한 `01-프롬프트-캐시-계측.html` `{{` 0건 · 다른 절 HTML·`index.html` 바이트 같음(보호 파일 대조).
- `visual.cjs`는 이 절에서 돌리지 않음(챕터 마감 몫).
- `pack.py` → `qa/upgrade/review-pack/01-프롬프트-캐시-계측.md`.

## 10. 옛 생성기

- `figures/_gen_figures.py`(막혀 있지 않던 판 `a0f6ef78…` — 사본 `.cache/ch34-01/pre/_gen_figures.py.before`, 준비 담당 사본 `before/generators/_gen_figures.py`) 맨 위(`from __future__` 뒤)에 설명 주석 셋 + `raise SystemExit(…)` → **`61b360825b662f97a79c9e3cedf441566f47c587c42518db3ec09256fcaa8fd6`**. `diff`로 네 줄만 더한 것 확인, `/tmp`에서 실행해 안내 글 + 종료 코드 1(옛 그림 파일 그대로). 챕터·실습 폴더의 다른 옛 생성기(`_generate.py`·`qa/author_ch34.py`) 없음. `.moai` part7 셋은 Ch 30 01이 막은 판 그대로(`f60d7287…`·`8cb946ea…`·`b171658f…` 확인). 옮기기(`mv -n` → `before/generators/blocked/`)는 마감(Part 7 `check_figures.py` 20행).

## 11. 보호 파일 (`before-manifest.json` 191개)

- **같음 182 · 바뀜 9 · 없어짐 0** — 모두 의도한 변경(`manifest-changes.md` — 01 본문·HTML·노트북·옛 생성기·공개 목록 둘·`집필점검표.md`·`qa/verification.md`·노트북 계약 JSON). 옛 `runs/` 셋은 같음.

## 12. 챕터 밖 수정

- `textbook/part7/public-files.json`(도구 파일 한 줄) · `textbook/_notebook/checks/notebook-contracts-part7-ch34-cost-rate-limits.json`(`verify.py --chapter`가 다시 씀, `573426ca…` → `63f32135…`). 그 밖 챕터 밖 파일·공용 도구 고침 0.

## 13. 강사 확인 대상

1. 제목의 「프롬프트 캐시」·「계측」은 제목에만 두고 본문 첫 자리에서 한 문장으로 풂(금지어 예외 한 곳씩) · 본문 말 「캐시 입력」·「공통 앞부분」·「바뀌는 글」·「캐시 쓰기 토큰」·「실험 번호」(새 용어 4 — meta 그대로).
2. 정책 글 길이(규칙 문장 100번·약 3,100토큰)와 문의 글 둘은 **흐름을 보여 주려고 정한 예** — 탐색 요청 없이 Ch 6 06 선례(80번에서 캐시 입력)보다 길게 정함.
3. 코드 양 38 → 112줄 · 코드 셀 5 → 22(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줄 것).
4. `prompt_cache_key`·보관 시간·캐시 쓰기 요금(GPT-5.6 이후)은 실행하지 않고 b7에 문서 문장으로만.
5. 삽화: 배터리 모양은 모두 같고 표시등 색으로만 채움을 보임, 표시등이 작음.

## 14. 지워야 하지만 지우지 않은 것 (삭제 승인 대상)

- `qa/upgrade/gates-wip-01-01.json`·`gates-wip-01.json`(게이트 중간 결과 — `gates-after.json`으로 갈음할 것).
- 기기 `/tmp/ch34-01/`(탐색·흔들림 확인 스크립트·마른 실행 `dry.jsonl`·`tryA/`·`nbA0/`·`B/`(새 커널 B 사본)·`illu/`(원본 PNG 둘)·`gen/`(생성기 조각)·치환 목록).
- 연결 폴더 `.cache/ch34-01/`(`pre/` 사본 넷 — 막기 전 옛 생성기·mdpatch 전 A 노트북·공개 목록 둘 · `tools/` 검사 스크립트 셋 · `reps1.json`·`reps2.json`) · `.cache/ch34-01-view/`(삽화 보기 사본).
- 옛 `runs/cache-measurement.json`(01이 더는 쓰지 않음 — 공개 목록·zip·`final-artifact-hashes.json` 줄과 함께 마감이 처분) · 옛 그림 `figures/01-cache-flow.{svg,excalidraw}`(본문 참조 0 — 마감이 다른 절 옛 그림과 함께).
- `__pycache__`·`.pyc` 새로 만든 것 0(모든 파이썬 호출 `PYTHONDONTWRITEBYTECODE=1`, 실습 폴더 `notebooks/`에 `__pycache__` 없음 확인).

## 15. 기기 디스크

- 루트(`/`, `/tmp` 포함) 여유 **1.5G → 1.5G**(작업 전후, `/tmp/ch34-01` 수 MB) · 연결 폴더(사용자 디스크) 여유 **73G → 73G**.
