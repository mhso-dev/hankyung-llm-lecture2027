# Ch 15 09절 「평가 심화 실습」 신규 집필 기록

새로 만든 챕터 끝 실습 절입니다(규격 `textbook/QUALITY-UPGRADE.md` §7-2, PLAYBOOK §3, handoff 「§08 → 실습(09)」). 수정 전 원본이 없어 `qa/upgrade/before/`에 넣을 파일도 없습니다. 게이트는 처음부터 이 절 기준으로 잽니다.

- 파일: `_src/09-평가-심화-실습.html` · `labs/part4/ch15-evaluation-advanced/notebooks/09-평가-심화-실습.ipynb` · `qa/upgrade/author_09.py`(본문과 노트북을 함께 씀, `--src-only`는 본문만, `AUTHOR09_NB_ONLY=1`은 노트북만) · `figures/09-1`~`09-5` · `qa/upgrade/09-figures.md` · `qa/upgrade/09-probe.md` · `qa/upgrade/review-pack/09-평가-심화-실습.md`
- 슬러그 `09-평가-심화-실습`, 제목 「평가 심화 실습: 입력 파일에서 두 줄씩 골라 회귀와 비용 보기」, `chapter.json`에 `format: experiment`로 더함. **`hours`는 그대로**(「총 16h · 강의 8h · 실습 8h」, 01~08절 meta 합 16h 그대로). 이 절 meta는 「실습 30분 · 새 용어 0」이고 챕터 시수에 더하지 않았습니다(Ch 13·14 선례).
- **서비스 모델 절**입니다. 설명만 고칠 때는 `mdpatch.py` → `run_section.sh … 09 --no-exec`.

## 1. 게이트

| 항목 | 값 |
|---|---|
| 게이트(첫 실행 전, 노트북·본문만 쓴 상태) | G1 0 · G2 0 · G3 0 · G4 0 · G5 0 · G6 0 · G7 18(그림 파일 없음) — **첫 실행 전에 `upgrade_gates.py … --section 09`로 G1~G6 0을 먼저 확인**, 게이트 때문에 다시 실행한 일 없음 |
| 게이트(최종) | **G1~G7 모두 0 · PASS**(`gates-wip-09.json`), 코드 셀 **23**(준비 셀 4: 설치·import·키·자리 찾기 + 기본 경로 19, 그 가운데 모델 셀 1), 검사 문장 **359** |
| 셀 모양 | 기본 경로 셀 최대 **9줄**(`BODY_CHECK`), 함수 본문 최대 **8줄**(`check_question`·`print_costs`), 코드 줄(주석·빈 줄 제외) 139 |
| 새 커널 | `PASS 09-평가-심화-실습.ipynb: 23 cells`. 같은 코드(`code_sha256` `f9aad94b…`)로 **새 커널 두 번**(A 19:02:43·B 19:02:56 UTC 시작) — 셀별 출력 **21/23 같음**, 다른 두 셀은 비용 표(§4) |
| verify | `PASS 9 sections / 233 code cells (max 13 lines)` |
| 빌드 | HTML 열 개(절 아홉 + `index.html`) 모두 `{{` 잔존 **0건**. `_build.py`를 두 번 돌려 열 개의 sha256이 같았습니다. 09절 HTML에 Mermaid `svg` 4 · 삽화 1 |
| 그림 | Mermaid 4장(`09-1`~`09-4`, 폭 466·382·502·450) · 삽화 1장(`09-5`, 1차 채택) |
| 요청 | 실행 한 번에 **모델 4번**(실행 1 두 번 + 실행 2 두 번), 임베딩 0, 파일 올리기·일괄 작업 0. 규격 §7-2의 3~5번 안 |

- AST로 따로 센 금지 문법(f-string·`key=`·`reverse=`·`set`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`setdefault`·`.get`·`+=`·한 줄 다중 대입·튜플 풀기·기본값 매개변수·타입힌트·내포식·`lambda`·조건 표현식·클래스·세미콜론) **0건**(`/tmp/ch15-08/astcheck.py`).
- 금지어(07·08절 목록 + 「폴백」·「묶음」): 본문·노트북 설명·코드 주석·`print` 라벨 **0건**. 첫 초안의 「이 페이지의 출력은」(「페이지」 — 앞 절 목록의 금지어)은 「교재 출력은」으로, 「학생 묶음에 들어 있고」는 「내려받은 실습 자료에 들어 있습니다」로 첫 실행 전에 고쳤습니다. 「묶음」을 일괄 처리 뜻으로 쓴 곳은 없습니다.

## 2. 주제와 붙인 앞 절 기능 (b3 한 단락)

**주제**: 08절 입력 파일을 일괄 처리로 맡기기 전에, 요청 식별자의 질문 번호로 두 줄(이전 판·이후 판)만 골라 파일에 적힌 판정 요청 글을 평가 모델에 하나씩 보낸다. 받은 점수로 07절 짝지어 보는 검사를 걸고, 받은 사용량으로 06절처럼 요청마다 예상 비용을 센다.

- **붙인 기능 셋**(handoff 12번 제안 그대로):
  1. **08절 입력 파일 읽기** — `read_jsonl`(도구 파일로 옮김)과 요청 식별자 `split("-")`, 보내지 않은 줄 찾기 `ids_not_in`(도구 파일로 옮김).
  2. **07절 회귀 스위트** — `broken_cases`·`check_by_case`(안에서 `check_by_average`, 셋 모두 도구 파일로 옮김).
  3. **06절 요청 한 번 비용** — `usage_metadata`·요금표 `mini_prices`(2026-09-17)·Ch 6 06절 `estimate_cost`(06절이 이미 도구 파일에 옮김).
  바탕은 02절 근거 충실도 판정 머리글 `rag-judge-v1.0.0`(입력 파일 본문에 이미 든 요청 글)과 `json.loads(reply.text)`.
- **고른 까닭**(b3): 입력 파일을 맡기기 전에 할 일은 「요청이 판정되는지」와 「비용이 얼마인지」 보는 것이고, 판정은 07절 검사로, 비용은 06절 방법으로 본다.
- **뺀 것과 까닭**(b3 두 단락):
  - 01절 실패 로그 — 검색 쪽 기록이라 판정 흐름에 들어갈 자리가 없음.
  - 02절 네 평가 — 넷을 모두 걸면 요청이 네 배. 입력 파일에 든 근거 충실도 하나만.
  - 03절 머리글 두 판·04절 일치율 — 새 판 `rag-judge-v1.1.0`의 Q090이 실행 때마다 갈렸고(`fix-03-04-probe.md`), 일치율에는 제시 라벨이 따로 필요.
  - 05절 걸린 시간 — 재지 않음(규격 §3, 05절 몫).
  - 06절 백분위수 — 요청 네 번으로는 분포를 볼 수 없음. 대화 목록을 다시 정하면 06절 되풀이.
  - **07절처럼 두 판 여섯 줄을 모두 보내는 설계** — 07절 실험 되풀이(규격 §7-2 5항). 두 줄씩 골라 보내 「고른 사례에 따라 검사 결과가 뒤집힌다」를 보이고, 끝에 두 실행을 모아 07절 결론(사례 전체로 판정)으로 이음.
- **실행 1 / 실행 2**: 고른 질문 번호 하나만 다름(`Q090` → `Q002`). 입력 파일·모델·요금표·조립 함수 같음. 두 사례는 **07절 결과를 보고 판정이 반대로 움직인 두 사례를 고른 예**(b4 「두 번의 실행」·b7에 적음).

## 3. 흔들림 먼저 확인 (규격 §2-7 10번 끝) — `09-probe.md`

- 핵심 관찰(실행 1 통과 True ↔ 실행 2 통과 False, 합치면 False)이 네 판정에 기대므로, 노트북 실행 **전에** 네 요청(입력 파일 본문 그대로)을 따로 다섯 번씩 보냈습니다(18:52:09–18:52:30 UTC, 기준은 첫 요청 전 18:52:04에 파일로 적음).
- 결과: **old-Q090 0 ×5 · new-Q090 1 ×5 · old-Q002 1 ×5 · new-Q002 0 ×5** — 07절까지의 관찰과 같아 입력을 바꾸지 않았습니다. 노트북 A·B도 네 점수 모두 같았습니다.
- 학생 본문 b7: 「노트북을 쓰기 전에 네 요청을 따로 다섯 번씩 보냈습니다. 판정이 흔들리는지 보려는 확인이었고 다섯 번 모두 같은 점수였습니다. 그래도 같은 요청의 판정이 실행한 때에 따라 달라질 수 있습니다.」 확인 실행의 숫자(스무 번)는 노트북 출력에 없어 본문에 넣지 않았습니다.
- 참고(한 번 본 모양): 확인 실행에서 네 요청 모두 **첫 요청만 캐시 입력 0**, 둘째부터 2816·1792. 까닭은 확인하지 않았습니다.

## 4. 새 커널 두 번 실행 (셀별 대조)

| 실행 | 때(UTC) | 코드 | outputs | 비고 |
|---|---|---|---|---|
| A | 19:02:43 시작 · 19:02:49 끝 | `f9aad94b…` | `e6bd1bfe…` | 결과 읽기의 모델 값 자리는 `[[READ_…]]` 자리표시로 두고 실행 |
| B | 19:02:56 시작 · 19:03:02 끝 | `f9aad94b…`(같음) | `5c2e1f66…` | **교재 출력**. 결과 읽기는 B 뒤 `mdpatch.py`로 채움(재실행 없음, 채운 뒤 셀별 출력 23/23 그대로) |

- **A·B 셀별 출력 21/23 같음.** 다른 두 셀은 실행 1·2의 비용 표(`print_costs`) — **출력 토큰 수**(A 38·56 / 41·47 ↔ B 48·61 / 45·50)와 그에 따른 **예상 비용**(A 합 0.0015069·0.0009693 ↔ B 0.0015744·0.0010008달러). 입력 토큰 수(3248·3266·1995·1995)와 캐시 입력 토큰 수(2816·2816·1792·1792)는 두 실행에서 같았습니다.
- **두 실행 모두 같음 → 결론·그림·정리에 씀**: `읽은 줄 수: 6`, 요청 식별자 여섯, `첫 줄 요청 주소: /v1/chat/completions`, `첫 줄 본문 설정: gpt-5.4-mini 0 none`, `모델 이름과 temperature가 같은 줄 수: 6`, `old-Q090 | 5093`·`new-Q090 | 5117`, 실행 1 `{'Q090': 0}` → `{'Q090': 1}`·깨진 사례 `[]`·통과 `True`, 실행 2 `{'Q002': 1}` → `{'Q002': 0}`·깨진 사례 `['Q002']`·통과 `False`, 입력 토큰 3248·3266·1995·1995, `보낸 요청 수: 4`, `보내지 않은 요청: ['old-Q006', 'new-Q006']`, 합친 점수 `{'Q090': 0, 'Q002': 1}`·`{'Q090': 1, 'Q002': 0}`·깨진 사례 `['Q002']`·통과 `False`.
- **결론·그림에 쓰지 않은 값**: 출력 토큰 수·예상 비용(두 실행에서 다름), 캐시 입력 토큰 수(두 실행에서 같았지만 06절 실행 A는 0, 확인 실행 첫 요청도 0 — 흔들리는 값으로 봄). 결과 읽기 둘째 단락 「이번 실행에서 …」에만 B 값을 적고 「새 커널로 두 번 실행했을 때 입력 토큰 수는 같았고, 출력 토큰 수와 예상 비용은 달랐습니다」를 붙였습니다. 본문 b6·b7·복습 4번도 같은 태도.
- 실행 시간: execute 한 번 `real` 약 6초(커널 시작·설치 셀 포함) — 준비물 「1분 안에 끝났습니다」.
- `assert`는 **코드가 정한 값**에만 둘(`len(sent_ids) == 4`, `unsent_ids == ["old-Q006", "new-Q006"]`) + 자리 찾기 셀·키 셀. 모델 판정·비용에는 0건.

## 5. 셀과 함수

1 준비(설치 세 패키지 / import `json`·`os`·`init_chat_model` + `from rag_tools import broken_cases, check_by_case, estimate_cost, ids_not_in, read_jsonl`, 고정 세 문장) → 2 키와 모델 → 3 입력 파일 읽기(자리 찾기·`read_jsonl`·본문 설정과 모델 객체 견주기) → 4 요금표와 줄 고르기(`mini_prices`·`lines_for`·Q090 두 줄 미리 보기) → 5 기록 장치와 조립(`send_lines`·`scores_for`·`check_question`·`print_costs`) → 6 실행 1(Q090, 요청 2)·검사·비용 → 7 실행 2(Q002, 요청 2)·검사·비용 → 8 두 실행 견주기·보내지 않은 줄·두 실행 모으기 → 정리 세 줄.

- **이 절이 새로 만든 함수 다섯(노트북에만 있음)**: `lines_for(lines, qid)` · `send_lines(judge_model, chosen_lines)`(응답 객체를 요청 식별자별로 — 06절 `replies` 모양) · `scores_for(replies, version_tag)` · `check_question(judge_model, lines, qid)`(조립, 줄 고르기 → 보내기 → 두 판 점수 → 07절 검사) · `print_costs(replies, prices)`(기록 장치).
- **파일의 요청을 보내는 방법**: 줄마다 `body.messages[0].content`(판정 요청 글)만 `model.invoke()`로 보냅니다. 본문의 설정 칸(`model`·`temperature`·`reasoning_effort`)은 보내지 않고, 같은 설정으로 만든 모델 객체가 요청을 보냅니다 — 그래서 3절에서 본문 모델 이름·temperature와 모델 객체를 견주는 셀을 두었습니다(여섯 줄 모두 같음, `0 == 0.0`). 08절이 설치판 소스로 확인한 대로 이 요청은 같은 주소 `/v1/chat/completions`·같은 칸 이름으로 나갑니다(본문 b4·노트북 3절 한 문장).
- 새 문법·새 API **0개**. 쓴 이름은 02절 `json.loads(reply.text)`, 05·06절 `usage_metadata`·`input_token_details["cache_read"]`, 06절 `estimate_cost`·요금표, 07절 `broken_cases`·`check_by_case`, 08절 `read_jsonl`·`split("-")`·`ids_not_in`·`body.messages[0].content`, 04절 `copy()`, 목록 `+`(08절). 새 말도 0개(「이전 판·이후 판·깨진 사례·짝지어 보는 검사·판 표시·요청 식별자·입력 파일·예상 비용·캐시 입력」 모두 앞 절 말).
- 「값 바꿔 보기」 소절은 따로 두지 않았습니다 — 실행 2가 값 하나(고른 질문 번호)만 바꾼 실행입니다(§7-2 구성, Ch 14 10 선례).

## 6. 도구 파일 (§2-7) — 07절 셋·08절 둘을 더함

- `labs/part4/ch15-evaluation-advanced/notebooks/rag_tools.py` 끝에 **07절 `check_by_average`·`broken_cases`·`check_by_case`**와 **08절 `read_jsonl`·`ids_not_in`**을 옮겼습니다. `def` 줄부터 `return`까지 07·08 노트북 셀과 **문자열 대조 `True`·AST 같음**(다섯 모두). 주석은 도구 파일 형식 `# Ch 15 07절에서 배웠습니다 — …`·`# Ch 15 08절에서 배웠습니다 — …`(노트북 셀 첫 줄 주석 문장을 이어 붙임). 기존 함수 열은 고치지 않았습니다(`diff`로 뒤에 더한 줄만 확인). 맨 위 `import json`·`import math` 그대로.
- 해시 `123a0b62…` → **`6c59d0f239370dbc208a7ca2be71fbe2147574e2ea13d5d044ce0ced5afdbea1`**.
- 노트북에서 가져오는 이름은 다섯(`broken_cases, check_by_case, estimate_cost, ids_not_in, read_jsonl`, 알파벳 순). `check_by_average`는 `check_by_case` 안에서만 불려 가져오지 않습니다(결과 읽기에 한 문장).
- **앞 노트북 확인(새 커널 사본, 모델 요청 0번, `/tmp/ch15-09/`)** — 07절 `make_checks.py` 방법(요청 셀과 그 값을 셀 밖에서 받아 쓰는 셀만 뺌, 정의 셀은 남김): 01 **30/30**(뺀 셀 0) · 03 **18/18**(7) · 04 **19/19**(8) · 05 **11/11**(12) · 06 **25/25**(3) · 07 **17/17**(8) 셀별 출력이 원본과 같음. 08은 모델 셀이 없어 통째로, **입력 파일을 다시 쓰므로 학생 묶음 모양의 임시 폴더**(`/tmp/ch15-09/bundle/…`, `--cwd notebooks`, `PYTHONPATH` 없음)에서 실행 — **25/26 같음**(다른 한 셀은 `찾은 프로젝트 맨 위: ../../../..`, 기대한 차이), 임시 폴더에 쓴 파일 해시 `0177cebc…` 같음. 02는 `rag_tools`를 가져오지 않습니다. 07·08 노트북은 자기 셀에서 같은 함수를 다시 정의하므로 도구 파일 판과 부딪히지 않습니다.
- 도구 파일은 이미 두 묶음 허용 목록에 있습니다.

## 7. 함께 고친 파일

**챕터 안**
- `chapter.json` — 09절 추가(`hours`·`objectives` 그대로).
- `qa/public-files.json` — 명시 목록이라 09 노트북 한 줄을 08 줄 아래에(18행).
- **08절 마지막 문장**(b8 「다음 학습과 이어지는 지점」·노트북 정리 셀·`author_08.py` 두 곳): 「09절은 이 챕터에서 배운 것을 함께 쓰는 실습 절입니다.」 → 「09절은 이 챕터를 마무리하는 실습 절입니다. 이 입력 파일에서 두 줄씩 골라 평가 모델에 보내고 판정과 예상 비용을 봅니다.」(`mdpatch.py` → `run_section.sh … 08 --no-exec`). 08 노트북 `code_sha256` `b86060ce…`·`outputs_sha256` `8dff52a6…` 그대로, 셀별 출력 26/26 그대로, 입력 파일 `0177cebc…` 그대로, 08 게이트 0. 파일 해시: 노트북 `4841ff03…` → `7f766679…`, `_src` `07e7ea22…` → `918405ef…`, 빌드 HTML `dc499bf2…` → `b2dd47a7…`. `pack.py … 08`로 검토 묶음도 다시 만듦.
- `labs/…/notebooks/rag_tools.py`(§6) · 새 파일: 노트북 09·`_src/09`·빌드 `09-평가-심화-실습.html`·`figures/09-*`(mmd 4·svg 4·png 5·render.json 4·caption 5·prompt 1)·`qa/upgrade/author_09.py`·`09-figures.md`·`09-probe.md`·`09-diagnosis.md`·`gates-wip-09.json`·`review-pack/09-평가-심화-실습.md`. 챕터 `index.html`(09 링크) 다시 빌드.
- `labs/part4/ch15-evaluation-advanced/README.md` — 맨 아래 **09절 한 단락만** 더함(그 밖의 옛 문장 — 첫 줄 「8개 노트북」·「Ch12의 공개 학습용 검색 로그」·「운영 judge 모델은 `[[미정: judge 모델]]`」 — 은 손대지 않음, handoff 「실습 → 챕터 검토」 §5 마감 목록).
- `handoff.md` 「실습 → 챕터 검토」, `집필점검표.md` 품질 개선 표 09 행, `qa/verification.md` 09 행과 메모.

**챕터 밖**
- `textbook/part4/public-files.json` — 09 노트북 한 줄(42행).
- `textbook/part4/index.html`·`textbook/downloads/part4-practice.zip` — `python3 textbook/part4/_build_index.py`로 다시 만듦(`Part 4: 33 verified sections; 97 bundled files`). `_build_index.py`에는 **절 수 칸이 없어**(절 수는 `chapter.json`에서 셈) 고치지 않았습니다. `textbook/part4/qa/integration-results.json`도 이 스크립트가 다시 씀.
- `textbook/_notebook/checks/notebook-contracts-part4-ch15-evaluation-advanced.json` — `verify.py --chapter`가 다시 씀(공용 검사 산출 파일, 09 항목이 더해짐).
- 공용 도구(`textbook/_notebook/`·`textbook/_template/`)의 코드는 고치지 않았습니다. `textbook/qa/check_course_continuity.py`에는 Part 4 항목이 없어 고칠 해시 허용 목록이 없었습니다.

## 8. 검사 스크립트가 멈춘 자리

- `python3 textbook/part4/qa/check_delivery.py` — **`part4-practice.zip` 대조는 지나갑니다**(manifest 97항목 어긋남 0, part4 노트북 33개, 09 노트북 포함 — 같은 대조를 스크립트로 따로 확인). 그다음 `llm-practice.zip`의 **111행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`**에서 멈춥니다(Ch 14 10절 때와 같은 자리, 전체 마감 몫). 멈춰서 `qa/delivery-results.json`은 다시 쓰지 않았습니다.
- `python3 textbook/part4/qa/check_bundle_execution.py` — **첫 대상 ch13 실습 폴더의 `uv sync --locked`에서 멈춤**: torch·nvidia 패키지(약 2.9GB)를 내려받다 `/tmp/uv-cache/.tmp…/triton/_C/libtriton.so`: **No space left on device**. ch15 08은 실행되지 않았고 `qa/bundle-execution.json`도 쓰지 않았습니다. **디스크**: 실행 전 루트 여유 1.3G → 실행 뒤 **약 255M**(uv가 남긴 `/tmp/uv-cache/.tmp*` 부분 내려받기, 지우지 않음 — §12).
  - 대신한 확인: 새 `part4-practice.zip`에서 ch15 실습 폴더만 `/tmp/ch15-09/zipcheck/`에 풀어, `notebooks/`를 작업 위치로 **API 키 환경 변수·`PYTHONPATH` 없이** 08 노트북을 새 커널로 실행 → **PASS 26 cells**, `code_sha256` 같음, 쓴 파일 `0177cebc…` 같음. 커널은 `uv sync --locked`로 만든 `.venv`가 아니라 작업 가상환경(`.cache/vm/venv-ch15-evaluation-advanced`)을 썼습니다. 같은 폴더에서 09가 쓰는 자리 찾기·`read_jsonl`(여섯 줄)·도구 파일 함수 가져오기도 확인(모델 요청 0번).
- Part 7 묶음(`textbook/part7/_build_index.py`)은 챕터 밖이라 돌리지 않았습니다 — 08절이 입력 파일을 다시 써서 `part7-practice.zip`의 그 한 항목이 여전히 Stale입니다(08 진단 §3-1). 09절은 그 파일을 바꾸지 않았습니다.

## 9. 보호 파일 36개

- `before-manifest.json` 36개 가운데 **35개가 기록 값 그대로**, **`runs/batch-eval-input.jsonl` 하나만 다르고 08절이 쓴 값 그대로**(`0177cebc207151657385a7a11ec2147b0bc45edc2b35f09c7f6fb2b7f8988e3e`). 작업 전·끝 모두 같은 상태입니다. **09절은 파일을 쓰지 않았습니다**(입력 파일·자료 파일 읽기만, `data/evaluation-cases.json` `dc48b1bc…` 그대로, 머리 칸 값 출력·인용 0).

## 10. 요청 수 · 비용

- 노트북 실행 한 번 **4번**(규격 §7-2 범위 안). 작업 합계 **28번**: 흔들림 확인 20 + 새 커널 A·B 8. 모두 `gpt-5.4-mini`, 임베딩 0, 파일 올리기·일괄 작업 0, 도구 파일 확인 사본 0.
- 예상 비용(2026-09-17 단가, 실제 사용량으로 셈): 확인 20번 약 0.0188달러 + A 0.0024762 + B 0.0025752 = **약 0.024달러**. 청구 금액이 아닙니다. 준비물 「미화 0.01달러 아래」는 실행 한 번 기준(A·B 모두 약 0.0025, 캐시 입력이 없다고 쳐도 약 0.009).
- 걸린 시간은 재지 않았습니다(b7).

## 11. 강사 확인 대상

1. **두 사례를 07절 결과를 보고 골랐습니다**(판정이 반대로 움직인 Q090·Q002). 「두 줄만 보낸 검사 결과는 고른 사례에 달렸다」를 보이려는 정한 예이고 b4·b7에 밝혔습니다. 수업 설계에 맞는지.
2. **파일의 요청을 일괄 처리가 아니라 하나씩(`invoke`) 보냈습니다.** 본문 설정 칸은 보내지 않고 같은 설정의 모델 객체가 보냅니다. 일괄 처리로 받은 판정이 같은지는 여전히 확인하지 않았습니다(08절 강사 확인 3번과 같음).
3. **비용 값은 결론·그림에 넣지 않았습니다**(출력 토큰·예상 비용이 두 실행에서 다름, 캐시 입력은 06절에서 흔들림). 조립도의 「요청마다 예상 비용」은 값 없이 이름만.
4. `check_bundle_execution.py`가 **디스크 부족**으로 ch13 단계에서 멈춰 ch15 08을 실행하지 못했습니다(대신 zip에서 푼 ch15 폴더로 확인, §8). 디스크 정리(삭제 승인)가 필요합니다.
5. 교재 출력 환경 `langchain-core 1.6.3`·`openai 3.16.2` ↔ 학생 잠금 `1.6.2`·`3.11.0`(02~08절과 같은 차이).
6. 한국어 감사 3단·삽화 판정은 별도 세션 몫입니다.

## 12. 지우지 않은 것(삭제 승인 대상)

- **`/tmp/uv-cache/.tmp*`**(check_bundle_execution.py의 ch13 `uv sync --locked`가 디스크 부족으로 멈추며 남긴 부분 내려받기, `/tmp/uv-cache` 전체 약 2.8G, 루트 여유 약 255M) — 기기 임시 폴더. **정리가 필요합니다.**
- `/tmp/ch15-09/`(기준·확인 `criteria.md`·`criteria.time`·`probe.py`·`probe-log.jsonl`, 실행 사본 `runA.ipynb`·`runB.ipynb`, 도구 파일 확인 사본 `check01`·`check03`~`check07.ipynb`·`make_checks.py`·`bundle/`(08 확인), zip 확인 폴더 `zipcheck/`, 고침 목록 `reps1`~`reps3.py/json`·`reps08.json`, 생성기 조각 `gen/`, 금지어 스크립트 `banned.py`, 삽화 원본·대조용 `job1-orig.png`·`job1-again.png`·`job1-1100.png`, 기록 사본 `집필점검표.before.md`·`verification.before.md`·`handoff.before.md`·`README.before.md`·`chapter.before.json`·`ch-public-files.before.json`·`part4-public-files.before.json`·`rag_tools.before.py`·`nb08.before.ipynb`·`src08.before.html`·`author_08.before.py`, 해시 `pre-hashes.txt`·`build1.txt`·`build2.txt`, 묶음 실행 출력 `bundle-exec.out`).
- `.cache/ch15-09/`(그림 확인용 PNG `fig09-1-a`·`-b`, `fig09-2-a`, `fig09-3-a`, `fig09-4-a`, `illu-job1.png`).
- `qa/upgrade/gates-wip-09.json`은 챕터 마감의 `gates-after.json`으로 갈음됩니다.

## 13. 검토 1차 반영 (2026-09-21 챕터 마감)

- **B-13** 「두 실행」이 두 뜻(실행 1·2 ↔ 새 커널 두 번)으로 쓰인 세 자리를 새 커널 쪽 말로 바꿨습니다: b6 「출력 토큰 수와 예상 비용은 새 커널로 두 번 실행했을 때 달랐습니다」, b7 「캐시 입력 토큰 수는 새 커널로 두 번 실행했을 때 같았지만 …」, 복습 4번 질문 「새 커널로 두 번 실행했을 때 비용 표에서 같았던 값과 달랐던 값은 무엇입니까?」·해설 「새 커널로 두 번 실행했을 때 입력 토큰 수는 같았고, 출력 토큰 수와 예상 비용은 달랐습니다. 캐시 입력 토큰 수도 두 번 같았지만 06절에서 실행마다 달라 결론에 쓰지 않았습니다.」(A·B 대조: 입력 3248·3266·1995·1995 같음, 출력 38·56·41·47 ↔ 48·61·45·50, 캐시 입력 2816·2816·1792·1792 같음 — `handoff.md` 「실습 → 챕터 검토」 §2). 이제 「두 실행」은 이 절에서 실행 1·2만 가리킵니다.
- **B-14** 「파일의 요청이 그대로 판정되는지」(본문 설정 칸은 보내지 않음) → 「파일에 든 판정 요청 글이 판정되는지」(b2·b6·노트북 [셀 12]).
- **B-15** 두 사례를 07절 결과를 보고 골랐다는 사실을 노트북 [셀 32]에 「실행 1·2가 고를 두 사례 Q090·Q002는 흐름을 보여 주려고 07절 결과를 보고 정한 예입니다.」로 더했습니다(「## 6.」 단락은 이미 다섯 문장이라 앞 단락에 둠).
- **B-16**(09가 07을 되풀이하는 정도): 받아들였습니다. 파일 읽기·요청마다 비용·일부만 보낸 결과로는 이후 판을 정할 수 없다는 흐름이 더해졌습니다. 강사 확인 대상에 올렸습니다(`chapter-summary.md` §11).
- 노트북은 다시 실행하지 않았습니다. 이 절 노트북의 `code_sha256`·`outputs_sha256`은 작업 전과 같고 설명 셀만 바뀌었습니다(`mdpatch.py` → `run_section.sh … --no-exec`). 생성기 `author_NN.py`의 `SRC_HTML`·`cells()` 설명 셀이 `_src`·노트북과 글자까지 같은 것을 마감 대조로 확인했습니다. 게이트 G1~G7 0.
