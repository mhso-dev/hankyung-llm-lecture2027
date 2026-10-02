# Ch 16 07절 「가드레일 실습」 신규 집필 기록

새로 만든 챕터 끝 실습 절입니다(규격 `textbook/QUALITY-UPGRADE.md` §7-2, PLAYBOOK §3, handoff 「§06 → 실습(07)」). 수정 전 원본이 없어 `qa/upgrade/before/`에 넣을 파일도 없습니다. 게이트는 처음부터 이 절 기준으로 잽니다.

- 작업 2026-09-23(12:05~12:40 UTC) · 생성기 `qa/upgrade/author_07.py`(본문과 노트북을 함께 씀, `--src-only`는 본문만, `AUTHOR07_NB_ONLY=1`은 노트북만, `author_06.py`가 본).
- 파일: `_src/07-가드레일-실습.html` · `labs/part4/ch16-guardrails/notebooks/07-가드레일-실습.ipynb` · 빌드 `07-가드레일-실습.html` · `figures/07-1`~`07-4` · `qa/upgrade/07-figures.md` · `qa/upgrade/review-pack/07-가드레일-실습.md`. 흔들림 확인 파일(`07-probe.md`)은 만들지 않았습니다(§3).
- **슬러그 `07-가드레일-실습`**: 규격 §7-2 「`{NN+1}-{챕터 이름}-실습`」. 챕터 이름이 「가드레일 · 안정화」처럼 둘일 때는 앞 챕터들이 핵심 말 하나로 줄였습니다(「오리엔테이션 · 개발환경」→`06-개발환경-실습`, 「LangGraph 기초 — 흐름을 그래프로」→`08-LangGraph-실습`, 「검색 품질 — 직접 구현하고 튜닝」→`13-검색-품질-실습`). 지시서의 `07-가드레일-실습`이 이 선례와 맞아 그대로 썼습니다(handoff의 `07-가드레일-안정화-실습` 안은 쓰지 않음).
- 제목 「가드레일 실습: 상담 질문 셋에 가리기·예약·감사 기록 붙이기」, `chapter.json`에 `format: experiment`로 더함. **`hours` 그대로**(「총 8h · 강의 3h · 실습 5h」, 01~06절 meta 합 강의 3h·실습 5h 그대로). 이 절 meta는 「실습 30분 · 새 용어 0」이고 챕터 시수에 더하지 않았습니다(Ch 13~15 선례). 제목에 「폴백」·「프롬프트」·「통합」을 넣지 않았습니다(handoff §06→07 6번).
- **서비스 모델 절**입니다. 설명만 고칠 때는 `mdpatch.py` → `run_section.sh … 07 --no-exec`.

## 1. 게이트

| 항목 | 값 |
|---|---|
| 게이트(첫 실행 전, 노트북·본문만 쓴 상태) | `upgrade_gates.py … --label wip-07 --section 07` → G1 0 · G2 0 · G3 0 · G4 0 · G5 0 · G6 0 · G7 14(그림 파일·설계표 없음). 사본 `~/ch16work/w07/gates-wip-07-07.preexec.json`(파일 `gates-wip-07-07.json`은 조립 함수를 고친 뒤 다시 잰 값 — 여전히 G1~G6 0). 게이트 때문에 다시 실행한 일 없음 |
| 게이트(최종, `--no-exec`) | **G1~G7 모두 0 · PASS**(`gates-wip-07.json`), 코드 셀 **24**(준비 셀 4: 설치·import(+도구 파일 일곱)·키·자리 찾기 — 모델 셀은 준비 셀 아님), 검사 문장 **344** |
| 셀 모양 | 비준비 셀 최대 **9줄**, 함수 본문 최대 **8줄**(`serve_all`), `note_event` 6 · `print_rows` 5 · `serve_question` 5 |
| 새 커널 | `PASS 07-가드레일-실습.ipynb: 24 cells`. 같은 코드(`code_sha256` `9739a77e…`)로 **새 커널 두 번** — 셀별 출력 글 **24/24 같음**(§4) |
| verify | `PASS 7 sections / 184 code cells (max 11 lines)` |
| 빌드 | 챕터 HTML 여덟 개(절 일곱 + `index.html`) `{{` 잔존 **0건**. 07절 HTML에 Mermaid `svg` 3 · 삽화 1 |
| 그림 | Mermaid 3장(`07-1`~`07-3`, 원본 폭 460·850·662, 빨강 0) · 삽화 1장(`07-4`, 2차 채택) |
| 요청 | 실행 한 번에 **모델 3번**(실행 1 두 번 + 실행 2 한 번), 임베딩 0. 규격 §7-2의 3~5번 안 |

- 게이트가 세지 않는 것도 직접 확인(`~/ch16work/w07/ast07.py`, 실행한 노트북 코드 셀 AST): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`+=`·클래스·`set`·`global`·`key=`/`reverse=`·`isinstance`·`enumerate`·`zip`·`next`·`sum`·`max`·`min`·`any`·`all`·`sorted`·`dict()`·`round`·`.get`·`setdefault`·`elif`·기본값 매개변수·타입힌트·데코레이터·맨 `raise`·한 줄 다중 대입·**파일 쓰기(`open(…, "w"/"a")`)** **0건**.
- 금지어 확장 목록(`~/ch16work/w07/ban16-07.py`, 06절 목록 그대로): `_src`·노트북 설명 「열」 1씩 = 고정 세 문장 「파일을 열면」. 그 밖 0건(「프롬프트」·「폴백」·「경로」·「반환」·「조각」·「레코드」·「캐시」·「묶음」·「강사 시연」 0). 삽화 `.prompt.md`의 「프롬프트」는 작업 기록 파일이라 대상 밖(01~06절과 같음).

## 2. 주제와 붙인 앞 절 기능 (b3 두 단락)

**주제**: 미르시립도서관 상담 창구에 들어온 질문 셋(가짜 개인정보가 하나씩 든 질문)을 차례로 처리한다. 질문마다 가리고, 예약한 뒤 모델에 보내고, 감사 기록 한 줄을 노트북 안 기록 목록에 남긴다. 예약에서 멈춘 질문도 남긴다. 실행 1은 호출 한도 2, 실행 2는 호출 한도 1. 끝에 두 기록을 지문으로 짝지어 결과가 달라진 줄을 원문 없이 찾는다.

- **붙인 기능 셋**(handoff §06→07·지시서 예시 「02 가리기 + 04 예약 + 05 감사 기록을 새 상담 질문 몇 개에」):
  1. **02절 가리기** — `mask_pii`(질문마다), `find_raw_values`(보낼 메시지·기록 목록에 원문 값이 남았는지).
  2. **04절 예약** — `make_budget`·`reserve`, 04절 정한 값(호출 한도 2·비용 상한 0.01·예상 비용 0.002).
  3. **05절 감사 기록** — 칸 넷(`event`·`query_hash`·`query_masked`·`detail`), `fingerprint_of`·`safe_detail`, 소금값 `ch16-session`, 사건 이름 `answer`·`stopped`.
  보낼 메시지는 06절 `build_rag_messages`(문서 구역)로 만듭니다 — 보낼 글을 만드는 자리라 붙인 기능 셋에 세지 않았습니다(b3·노트북 3절에 「보낼 글을 만드는 데만 쓰고 06절의 문서 검사와 격리는 쓰지 않는다」).
- **고른 까닭**(b3): 상담 창구가 질문마다 꼭 할 일은 개인정보 가리기, 호출 한도 지키기, 한 일 남기기이고, 이 셋이 02·04·05절 기능.
- **뺀 것과 까닭**(b3 두 단락):
  - 01 입력 검사·출력 검사 — 06절 한 흐름에 이미 들어 있고, 출력 검사는 모델이 적은 표시 꼴에 결과가 달려 있음.
  - 03 자르기·요약 — 질문이 하나씩 따로 오는 창구라 대화 기록이 없음(요약은 요청도 늘림).
  - 05 재시도·예비 흐름 — 실패 흉내를 다시 만들어야 하고 05절 되풀이.
  - 06 문서 검사·격리 — 06절 주제이고 이번 모델은 숨은 지시문을 따른 적이 없음(38번). 이 실습은 안내 문서 `E01`만 씀.
  - **06 `guarded_generate` 한 흐름** — 그대로 부르면 06절 조립 되풀이(규격 §7-2 5항). 06 한 흐름은 **예약에서 막히면 기록 없이 오류만 올리는 모양**(도구 파일 `guarded_generate`의 `reserve` 줄에 `try` 없음 — 06절은 그 자리를 실행하지 않았음)이라, 이 실습은 멈춘 질문도 `stopped`로 기록하는 조립을 새로 적었습니다. 04절 `ask_all`의 `break`(멈추면 뒤 질문을 보지 않음)와도 다르게 멈춘 뒤 다음 질문으로 넘어갑니다. 이 두 차이를 노트북 5절·b4 「멈춘 질문도 기록하기」에 적었습니다.
- **실행 1 / 실행 2**: 호출 한도 하나만 다름(2 → 1). 질문 셋·비용 상한·예상 비용·소금값·조립 함수 같음. 실행 전 예상을 노트북 6·7절에 적었고 두 실행 모두 예상과 같았습니다. 실행 2를 「올리기(3)」가 아니라 「내리기(1)」로 정한 까닭: 멈춘 질문이 둘이 되어 `serve_all`이 멈춘 뒤에도 다음 질문을 기록하는 모습이 실행으로 보이고, 요청도 5번이 아니라 3번으로 끝납니다(첫 설계 때 정함, 결과를 보고 고르지 않음).
- **손으로 적은 새 값**: 상담 질문 셋(이 절에서 실행 전에 적음)과 가짜 값 셋(02절 값 `test.user@example.com`·`010-0000-0000`·`1111-2222-3333-4444` — 주민등록번호 가짜 값은 쓰지 않음). 출력 줄 `질문 출처: 이 절에서 실행 전에 적은 글`·`가짜 값 출처: 02절에서 지어낸 값`과 b7 첫 항목에 밝혔습니다. 질문은 모두 `E01`이 답할 수 있는 휴관일 질문에 연락처·카드 번호를 붙인 모양입니다.

## 3. 흔들림 확인 — 하지 않음 (규격 §2-7 10번 끝)

- 핵심 관찰(받은 답 수·예약한 호출 수·기록 줄 수·사건 이름·원문 값 없음·지문 같음·달라진 줄)은 모두 `reserve`·`mask_pii`·`fingerprint_of`가 정하는 값이고, 모델 답은 기록에도 결론에도 들어가지 않습니다(04·05절 선례). 그래서 노트북 밖 5번 확인 대상이 아니라고 보고 `07-probe.md`를 만들지 않았습니다.
- 모델 답 문장은 6절 출력에만 두고, 결과 읽기 둘째 단락에 「이번 실행에서는 … 새 커널로 두 번 실행했을 때 두 답은 글자까지 같았습니다. 그래도 … 다를 수 있습니다」로 한정했습니다. 모델 답에 `assert` 0건(`assert`는 자리 찾기·키 확인 준비 셀과, 기록 목록 원문 확인 두 줄뿐 — 기록 목록은 코드가 정한 값).
- 탐색 실행은 없습니다(노트북 밖 요청 0번). 조립 함수 모양을 한 번 고쳤지만 **실행 전**이었습니다(§5).

## 4. 새 커널 두 번 실행 (셀별 대조)

| 실행 | UTC(첫 셀 입력 → 마지막 셀 응답) | 코드 | outputs | 비고 |
|---|---|---|---|---|
| **C(교재 출력)** | 12:15:24.76 → 12:15:29.96(5.20초) | `9739a77e4d6d693f…` | `01099ea54e68…` | `run_section.sh … 07`이 실행 |
| D | 12:15:49 → 12:15:56(5.39초) | `9739a77e…`(같음) | `f1abca864d94…` | C를 출력만 지운 사본 `~/ch16work/w07/nb-runD.ipynb`를 같은 가상환경·`PYTHONPATH`·`execute.py`로(대조 본 `cmpCD.py`) |

- **셀별 출력 글 24/24 같음**(모델 답 셀 포함). `outputs_sha256`이 다른 까닭은 설치 셀 하나의 출력 **조각 나눔**뿐입니다(C는 `Note: …` 줄과 판 번호 세 줄이 두 stream, D는 한 stream — 글자는 같음).
- 그림은 C·D를 마친 **뒤에** 처음 렌더했습니다. 결과 읽기의 `[[RUNSEC]]`·`[[READ_ANSWERS]]`와 본문의 `[[B6_TWICE]]`·`[[B7_FAIL]]`은 D 뒤 `mdpatch.py`로 채웠습니다(`reps07-a.json`, 재실행 없음). 그 뒤 `reps07-b.json`(오늘 볼 그림 alt·읽기)·`reps07-c.json`(문장 셋)도 설명만 고쳤고, 노트북 `code_sha256`·`outputs_sha256`은 C와 같습니다(마지막 `--no-exec` 뒤 다시 확인).
- **두 실행 모두 같음 → 결론·그림·정리에 씀**: `02절: find_raw_values mask_pii`·`04절: make_budget reserve`·`05절: fingerprint_of safe_detail`·`06절: build_rag_messages` · `모델 이름: gpt-5.4-mini` · `자료 파일의 문서 수: 2`·`고른 문서: E01 | 미르시립도서관 이용 안내` · `질문 수: 3` · 가린 질문 셋(`<EMAIL_MASKED>`·`<PHONE_MASKED>`·`<CARD_MASKED>`, 종류별 개수 하나씩) · `메시지 수: 2`·`사용자 메시지에 남은 원문 값: []` · `호출 한도: 2`·`비용 상한(달러): 0.01`·`요청 하나의 예상 비용(달러): 0.002`·`소금값: ch16-session` · 실행 1 `멈춘 까닭: 호출 한도를 넘습니다.`·`받은 답 수: 2`·`예약한 호출 수: 2`·`기록 줄 수: 3`, 기록 목록 `answer`(`'reserved_calls': 1`)·`answer`(`'reserved_calls': 2`)·`stopped`(`{'reason': '호출 한도를 넘습니다.', 'reserved_calls': 2}`), `기록에 남은 원문 값: []` · 실행 2 `멈춘 까닭:` 두 줄·`받은 답 수: 1`·`예약한 호출 수: 1`·`기록 줄 수: 3`, 기록 `answer`·`stopped`·`stopped`(둘 다 `'reserved_calls': 1`), `기록에 남은 원문 값: []` · 표 `실행 1 | 2 | 2 | 1 | 3`·`실행 2 | 1 | 1 | 2 | 3` · 짝짓기 `0 | True | answer | answer`·`1 | True | answer | stopped`·`2 | True | stopped | stopped` · `사건이 달라진 줄 수: 1`·달라진 질문 = 가린 둘째 질문.
- **두 번 같았지만 모델 출력이라 결론에 쓰지 않은 값**: 실행 1 받은 답 두 문장(「이번 주 월요일에는 미르시립도서관이 휴관하므로 책을 반납하러 갈 수 없습니다. [E01 p.1]」·「미르시립도서관은 공휴일이 월요일과 겹치면 다음 날인 화요일에도 휴관합니다. [E01 p.1]」). 실행 2의 답은 출력하지 않았습니다(받은 답 수만).
- 준비물 「노트북 전체가 약 5초」는 C의 셀 실행 기록(5.20초, 커널 기동 제외)에서 읽은 값입니다. 걸린 시간은 재지 않았습니다(b7).

## 5. 셀과 함수

1 준비(설치 / import `json`·`os` + `from guardrails import build_rag_messages, find_raw_values, fingerprint_of, make_budget, mask_pii, reserve, safe_detail` + 고정 세 문장) → 2 키와 모델 → 3 상황과 재료(자리 찾기·`E01` 고르기·질문 셋·가려 보기·메시지 미리 보기·정한 값) → 4 기록 장치(`note_event`·`print_rows`) → 5 조립(`serve_question`·`serve_all`) → 6 실행 1(예상 → 실행 → 기록 목록 → 받은 답 → 원문 확인) → 7 실행 2(예상 → 실행 → 기록 목록 → 원문 확인) → 8 두 실행 견주기(표 → 지문으로 짝짓기 → 달라진 줄) → 정리 세 줄. PLAYBOOK §3 차례(준비 → 주제 소개 → 재료 → 기록 장치 → 조립(배운 절을 주석으로) → 실행 1 → 실행 2 → 정리)와 같습니다.

- **새로 만든 함수 넷(노트북에만)**: `note_event(log, event, query, detail)` — **도구 파일 `record_event`에서 `write_audit_rows(log)` 한 줄만 뺀 함수**(인자·나머지 본문 AST 같음, `ast07.py`로 대조 — 본문 「05절 `record_event`에서 파일을 다시 쓰는 줄 하나만 뺀 함수」) · `print_rows(log)` · `serve_question(log, budget, question, documents, estimated_cost_usd)`(가리기 → 예약 → `model.invoke(build_rag_messages(…)).text` → `answer` 기록, 조립 함수 안에 02·04·05절 주석) · `serve_all(log, budget, questions, documents, estimated_cost_usd)`(예약 `ValueError`를 받아 `stopped` 기록 뒤 다음 질문).
- **첫 초안에서 실행 전에 고친 것**: `serve_question`이 예약 `ValueError`를 받아 `stopped`를 적고 `raise error`로 다시 올리는 판은 본문이 9줄이라(규격 8줄), `stopped` 기록을 `serve_all`의 `except`로 옮겼습니다(본문 5줄·8줄). 멈춘 질문은 원문 질문을 `note_event`에 넘기지만 `note_event`가 첫 줄에서 가립니다(05절 `record_event`와 같은 설계) — 노트북 5절·b4·복습 2에 적었습니다. 이 판으로 처음 실행했습니다(실행 뒤 코드 변경 0).
- 앞 절 노트북에만 있던 함수(`summarize_text`·`build_messages`·`ask_with_budget`·`ask_all`·`ask_primary`·`ask_backup`·`ask_model`)는 **다시 쓰지 않았습니다** — 모델은 조립 함수 안에서 `model.invoke(...).text`로 부릅니다(`model`은 2절 모델 셀의 전역 이름, 04절 `ask_with_budget`과 같은 방식). 그래서 규격 §2-7의 「노트북에만 있는 함수를 도구 파일로 옮기기」는 해당이 없었습니다.
- 새 문법·API·말 **0개**. 쓴 이름: `try/except ValueError as error`(03), 튜플 풀기(02), 딕셔너리 칸(04), `json.dumps(…, ensure_ascii=False)`(02·05), `range(len(…))`(01~04), `!=`(과정에서 Ch 14 10·Ch 15 01·03이 쓴 비교 — 이 챕터에서는 처음이라 노트북 8절에 한 문장). 말: 상담 창구(상황 설명)·기록 장치·조립 함수(Ch 15 09 실습 절 말)·기록 목록·가짜 값·지문·소금값·사건 이름·예약·호출 한도 모두 앞 절·앞 실습 절 말.

## 6. 도구 파일 (§2-7) — 고치지 않음

- `notebooks/guardrails.py` **`d6e56ea7…` 그대로**(06절 판), 테스트 `632ab36c…` 그대로, `pytest -q -p no:cacheprovider tests` → **7 passed**. 가져온 일곱 함수는 모두 06절까지 노트북 셀과 AST·본문 줄이 같은 판(06 진단 §4). 도구 파일을 고치지 않았으므로 01~06 노트북 사본 확인은 할 일이 없었습니다.

## 7. 함께 고친 파일

**챕터 안**
- `chapter.json` — 07절 추가(`hours`·`objectives` 그대로).
- `qa/public-files.json` — 명시 목록이라 07 노트북 한 줄(06 줄 아래).
- **06절 마지막 문장**(b8 「다음 학습과 이어지는 지점」·노트북 정리 셀·`author_06.py` 두 곳): 「07절 실습에서는 이 챕터에서 만든 검사들을 함께 붙여 실행합니다.」 → 「07절은 이 챕터를 마무리하는 실습 절입니다. 상담 질문 셋에 가리기·예약·감사 기록을 함께 붙여 실행합니다.」(`mdpatch.py` `reps06-e.json` → `run_section.sh … 06 --no-exec`). **06 노트북 `code_sha256` `ec73ec15…`·`outputs_sha256` `146573fc…` 그대로**, 바뀐 셀은 마지막 마크다운 하나, `runs/06-audit.jsonl` `736271dd…` 그대로, 06 게이트 0(검사 문장 403 → 405). 파일 해시: 노트북 `53655f31…` → `606b3fcf…`, `_src` `55edc7f1…` → `db5ed42e…`, 빌드 HTML `c8e89460…` → `9ea86126…`(다음 절 링크 「챕터 끝」 → 07절 링크도 함께). `pack.py … 06`으로 검토 묶음도 다시 만듦. `author_06.py`와 06 노트북·`_src`가 글자까지 같음을 다시 확인(생성기 `cells()`·`SRC_HTML` 대조).
- 새 파일: 노트북 07·`_src/07`·빌드 `07-가드레일-실습.html`·`figures/07-*`(mmd 3·svg 3·png 4·render.json 3·caption 4·prompt 1)·`qa/upgrade/author_07.py`·`07-figures.md`·`07-diagnosis.md`·`gates-wip-07.json`·`gates-wip-07-07.json`·`review-pack/07-가드레일-실습.md`. 챕터 `index.html`(07 링크) 다시 빌드. 01~05절 빌드 HTML은 다시 써졌지만 해시가 작업 전과 같습니다.
- `qa/upgrade/handoff.md` 「실습 → 챕터 검토」, `qa/upgrade/manifest-changes.md` 「07절 끝 대조」, `집필점검표.md` 품질 개선 표 07 행, `qa/verification.md` 품질 개선 검증 표 07 행.

**챕터 밖**
- `textbook/part4/public-files.json` — 07 노트북 한 줄(55행, 06 줄 아래).
- `labs/part4/ch16-guardrails/README.md` — 맨 아래 **07절 한 단락만** 더함(옛 문장 「06절 영향 미관찰」·「최대 140 출력 토큰」·도구 파일 소개 없음은 손대지 않음 — 마감 몫).
- `textbook/part4/index.html`·`textbook/downloads/part4-practice.zip` — `python3 textbook/part4/_build_index.py`로 다시 만듦(**`Part 4: 34 verified sections; 98 bundled files`**, zip `f8f28c17…` → `698a5077…`, index `b8e7936c…` → `0b91a328…`). 이 스크립트가 `textbook/part4/qa/integration-results.json`도 다시 씀. `_build_index.py`에는 **절 수 칸이 없어**(절 수는 `chapter.json`에서 셈, 25행 `3, 5`는 강의·실습 시수) 고치지 않았습니다.
- `textbook/_notebook/checks/notebook-contracts-part4-ch16-guardrails.json` — `verify.py --chapter`가 다시 씀(공용 검사 산출 파일).
- 공용 도구(`textbook/_notebook/`·`textbook/_template/`)의 코드는 고치지 않았습니다. `textbook/_notebook/build_index.py` 36행의 Ch 16 「6」은 **다른 챕터처럼 실습 절을 뺀 절 수**(Ch 1 5·Ch 13 7·Ch 14 9·Ch 15 8 모두 실습 절 제외)라 고치지 않았습니다. `textbook/qa/check_course_continuity.py`에는 Part 4 항목이 없어 고칠 해시 허용 목록이 없었습니다.

## 8. 검사 스크립트가 멈춘 자리

- `python3 textbook/part4/qa/check_delivery.py` — **111행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`**(`llm-practice.zip`)에서 멈춥니다(Ch 14 10·Ch 15 09 때와 같은 자리, 전체 마감 몫). 멈춰서 `qa/delivery-results.json`은 다시 쓰지 않았습니다.
  - 같은 대조를 따로 돌린 결과: **`part4-practice.zip`은 manifest 98항목 어긋남 0, part4 노트북 34개(07 포함)**. `llm-practice.zip`은 Part 1 파일 말고도 옛 `labs/part4/ch16-guardrails/guardrails.py`(01절에서 옮김)가 manifest에 있어 대조가 깨지고, part4 노트북 수도 34와 다릅니다(마감 몫).
  - 07·06·챕터 목차·Part 4 목차 쪽: 복습 문제 4개(3~5 안), 고정 블록 `b1`~`b10`, 로컬 링크 누락 0, 비밀값 노출 0(스크립트 함수로 따로 확인).
- **학생 묶음 확인**(규격 §7-2): 새 zip에서 ch16 폴더만 `/tmp/ch16-07-zip/`에 풀어, `notebooks/`를 작업 위치로 **`PYTHONPATH` 없이** 07 노트북의 모델을 부르지 않는 셀(가져오기·자리 찾기·`E01` 고르기·질문·가리기·메시지·정한 값·정의 넷)을 실행 → `찾은 프로젝트 맨 위: ../../../..`, `자료 파일의 문서 수: 2`, 도구 파일 가져오기 통과. 이어 예산을 미리 채운 상태로 `serve_all`을 불러 세 질문 모두 `stopped`·원문 값 `[]` 확인(모델 요청 0, 파일 쓰기 0). 커널은 `uv sync --locked`로 만든 `.venv`가 아니라 작업 가상환경입니다.
- `check_bundle_execution.py`는 **돌리지 않았습니다**(지시서 — 마감 몫). Part 6 묶음(`textbook/part6/_build_index.py`)도 돌리지 않았습니다(챕터 밖 — 07절은 도구 파일·테스트를 바꾸지 않아 Part 6 선행 파일 해시는 06절 끝과 같음).

## 9. 보호 파일 7개

`before-manifest.json` 7개 가운데 **3개가 manifest 값 그대로**(`retrieved-documents.json` `ae2fe4f4…`, Ch 15 파일 둘 `0177cebc…`·`dc48b1bc…`), **4개는 01~06절이 적어 둔 의도한 변경 값 그대로**(`runs/05-audit.jsonl` `92e3d109…`, `runs/06-audit.jsonl` `736271dd…`, `notebooks/guardrails.py` `d6e56ea7…`, 테스트 `632ab36c…`). **07절은 보호 파일을 하나도 바꾸지 않았습니다**(`manifest-changes.md` 「07절 끝 대조」). 새 커널 C·D·묶음 확인 전후 모두 같았습니다.

## 10. 요청 수 · 비용

- 노트북 실행 한 번 **3번**(규격 §7-2 범위 안). 작업 합계 **6번**(새 커널 C·D, 흔들림 확인 0, 묶음 확인 0). 모두 `gpt-5.4-mini`, 임베딩 0.
- 예상 비용 합계 **0.002달러 아래**(추정 — 요청 하나에 입력 약 160·출력 약 35토큰으로 어림, 2026-09-17 mini 요금 100만 토큰당 입력 0.75·출력 4.50달러. 이 절은 토큰 수를 출력하지 않아 재지 않음, 청구 금액 아님).
- 삽화 두 장 4크레딧(§11).

## 11. 그림 — `qa/upgrade/07-figures.md`

- Mermaid **3장**(규격 §7-2 넷 가운데 셋): `07-1`(b4 조립도 + 노트북 오늘 볼 그림, 폭 **460**, 상자 일곱 + 점선 갈래 하나) · `07-2`(b5 실행 1의 실제 순서, `sequenceDiagram`, 폭 **850**) · `07-3`(b6 실행 1·2 비교, 폭 **662**). 모두 868 아래, **빨강 0**(experiment — 예약 `ValueError`는 `serve_all`이 받아 노랑 메모). `07-2`는 첫 렌더 폭 937·라벨이 세로선과 겹쳐 `messageAlign: left` + 한 줄 라벨 + 오류 문구를 노란 메모로 옮겼고, `stopped` 기록을 `serve_all`이 남기므로 참여자 이름을 `serve_all` · `serve_question`으로 고쳤습니다. `07-3`은 노란 상자 글이 저절로 꺾여 `<br>`로 미리 나눴습니다. PNG를 직접 열어 본 **뒤에** alt·도식 읽기를 썼습니다(`.cache/ch16-07-view/v1-fig1~3`·`v2-fig2~3`·`v3-fig2`).
- 삽화 **1장** `07-4-천과-개찰구와-대장`: 「도장과 도장 대장」 계열 — 앞 삽화 소품(02 덮개 천·04 개찰구 막대·01/05 대장·손도장)을 한 탁자에. `nano_banana_pro`(응답 `nano_banana_2`) · 16:9 · 2k · `use_unlim: false` · count 1.
  - 1차 job `525a514a-a372-4009-988e-fd8d93459d0d` **검수 탈락**: 대장·손도장이 탁자 뒤 공중에 뜸, 틀이 탁자 길이 방향이라 「지나간다」가 안 읽힘, 멈춘 쪽지 천만 다른 색(관계와 무관한 색). 개수는 맞았음.
  - **2차 job `bff3b96c-f269-42cf-9de8-3aab38436dda` 채택**(재생성 1회 — 규격 상한). 원본 `a35d2786…`(2752 × 1536) → 저장 1100 × 614 `8e2e15ae…`. 결과 URL을 다시 받아 같은 폭으로 줄여 저장 PNG와 픽셀 대조: bbox `None`, 세 칸 extrema `(0, 0)`. 저장본과 같은 사본·원본 부분 확대(대장·개찰구)를 직접 열어 셌습니다 — **쪽지 셋(막대 앞 하나·너머 둘)·세 쪽지 모두 같은 하늘색 천·대장 왼쪽 쪽 줄 셋·손도장 하나**, 모두 탁자 위. 개찰구는 기둥 둘·가로대 둘 + 왼쪽으로 뻗은 막대 하나로 그려져 「길을 막는 막대 하나」로 읽었습니다. 서비스 쪽 실패 0회.
  - 크레딧 **2632.5 → 2628.5**(두 장 4크레딧, `balance` 전후).
- 설계표·`.prompt.md`에 탈락 까닭과 두 프롬프트를 적었습니다. 대장 줄 셋은 실행 1 기록 세 줄과 짝지어 그림 읽기 둘째 단락에 적었습니다(프롬프트로 정한 개수이고 출력 `기록 줄 수: 3`과 같음).

## 12. 강사 확인 대상

1. **붙인 조합(02 가리기 + 04 예약 + 05 감사 기록)과 뺀 것**(§2) — 06 `guarded_generate`를 쓰지 않고, 멈춘 질문도 기록하는 조립을 새로 적은 설계. 06 한 흐름이 예약에서 막히면 기록을 남기지 않는 모양이라는 것을 본문에 **코드로 읽은 사실**로 적었습니다(06절은 그 자리를 실행하지 않음).
2. **파일을 쓰지 않는 실습** — 감사 기록은 노트북 안 목록(`note_event` = `record_event`에서 파일 쓰기 한 줄만 뺀 함수). 커널을 다시 시작하면 기록이 사라진다는 점을 b7에.
3. **실행 2 = 호출 한도 1**(내리기) — 04·05절 값 바꿔 보기와 같은 방향이라 새로움이 적다고 볼 수 있습니다. 대신 기록 목록 짝짓기(지문)로 결과를 견줍니다.
4. **흔들림 확인을 하지 않은 판단**(§3) — 결론에 모델 답이 없어서.
5. 삽화 재생성 1회(§11)와 개찰구 모양(기둥 둘·가로대 둘 + 막대 하나).
6. 교재 출력 환경 `langchain-core 1.6.4`·`openai 3.19.0` ↔ 학생 잠금 `1.6.2`·`3.11.0`(잠금 판 동작은 확인하지 않음, 01~06절과 같음).
7. 한국어 감사 3단·삽화 판독은 별도 세션 몫.

## 13. 지우지 않은 것 (삭제 승인 대상)

- 프로젝트 `.cache/ch16-07-view/`(이 절이 새로 만든 폴더 — 스테이징용 PNG 사본 `v1-fig1~3.png`·`v2-fig2~3.png`·`v3-fig2.png`·`illu-job1-1100.png`·`illu-crop-ledger.png`·`illu-crop-table.png`·`illu-job2-1100.png`·`job2-crop-ledger.png`·`job2-crop-gate.png`·`illu-saved-copy.png`).
- `qa/upgrade/gates-wip-07-07.json`(첫 실행 전 G1·G2 확인). `qa/upgrade/gates-wip-07.json`은 `run_section.sh`가 쓰는 절 기록.
- 세션 홈 `~/ch16work/w07/`(`before/` 작업 전 사본 — 06 노트북·06 `_src`·06 빌드 HTML·`author_06.py`·`chapter.json`·`public-files.json` 두 벌·README·`집필점검표.md`·`verification.md`·`handoff.md`·`manifest-changes.md`·목차 HTML 둘·`part4-practice.before.zip` / `pre-hashes.txt` / `nb-runC.ipynb`·`nb-runD.ipynb`·`cmpCD.py`·`ast07.py`·`ban16-07.py` / `reps07-a·b·c.json`·`reps06-e.json` / `gates-wip-07-07.preexec.json` / `illu/`(원본 2752px `job1-orig.png`·`job2-orig.png`·`job2-again.png`, 줄인 사본 `job1-1100.png`·`job2-1100.png`·`saved.png`, 확대 `crop-ledger.png`·`crop-table.png`·`job2-crop-*.png`, `shrink.py`·`crop.py`·`crop2.py`·`cmp.py`·`cmp2.py`)). 마운트 폴더 밖이라 학생 묶음과 무관합니다.
- 기기 `/tmp/ch16-07-zip/`(묶음 확인용으로 푼 ch16 폴더와 `check.py`).

## 14. 챕터 마감 검토 반영 (2026-09-23)

검토 보고서 `review-round1-A.md`(A-n)·`review-round1-B.md`(B-n), 챕터 전체 기록은 `chapter-summary.md`와 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-23)」.

- **다시 실행하지 않았습니다**(`mdpatch.py` → `--no-exec`). `code_sha256` `9739a77e…`·`outputs_sha256` `01099ea5…` 그대로, 파일 쓰기 0.
- **B-8** `07-2` 점선 응답 `B-->>S: 예약한 호출 하나/둘`을 예산 쪽 노란 메모 `예산 칸 calls 1`·`calls 2`로(`reserve`는 값을 내놓지 않음 — 04절 5절 결과 읽기). 도식 읽기 「예약한 뒤」 + 「함수 `reserve`는 값을 내놓지 않고 예산 칸만 고치므로, 그 칸 값은 예산 아래 노란 메모에 적었습니다」, alt. 메모 값은 기록 칸 `'reserved_calls': 1`·`2`로 출력에서 확인한 값. 폭 850.
- **B-9** `07-1` 두 기록 상자 라벨을 처리로 「기록 한 줄 남기기 / note_event · answer」·「… · stopped」(파랑 그대로). 도식 읽기·alt(노트북 셀 1 포함). 폭 494, 노트북 첨부 `07-1` 새 PNG.
- **A-2** 셀 20 「지킬 말과 문서 구역」 → 「시스템 메시지 글과 문서 구역」. **A-5** `_src` b3의 고정 세 문장 → 「… 도구 파일 `guardrails.py`에서 그대로 가져옵니다」. **A-4** 노트북 한 문장. **A-7** 확인할 점·`07-3` 도식 읽기 「노트북 8절」. **B-1** b5 「예상 비용은 세 번을 합쳐 …」 → 「노트북을 한 번 실행하는 요금은 요금표로 어림해 …, 청구 금액과는 다를 수 있습니다」, 준비물·b7.
- 06 B-5 반영으로 06 정리가 「07절은 예약에서 멈춘 질문도 `stopped`로 남긴다」로 이어져, 07 b4 「06절 함수는 예약에서 막히면 기록 없이 오류만 올리는 모양」과 맞습니다.
