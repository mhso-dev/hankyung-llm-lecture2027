# Ch 17 Agent 개요 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part5/ch17-agent-overview`(절 다섯, 모두 experiment) · `labs/part5/ch17-agent-overview`. **Part 5의 첫 챕터**입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본) · `gates-before.json` · `before-manifest.json` · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch17-agent-overview`
- 읽은 것: 규격 `QUALITY-UPGRADE.md` · `AGENT-BRIEF.md` · `PLAYBOOK.md` · `qa/upgrade-course-summary.md` · `qa/upgrade-contracts.md`(§1·§3·§4·§5·§8) · Ch 16 `chapter-summary.md`(§13·§14) · Ch 16 `chapter-lead-notes.md`·`before-manifest.json`·`gates-before.json`(모양)
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 파일 삭제 0건. 모델·임베딩 호출 0건. 노트북 실행 0건.
- `chapter.json` `hours` = 「총 8h · 강의 5h · 실습 3h」. 절 meta 합은 강의 1×5 = **5h**, 실습 0.5×4 + 1(05절) = **3h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part5/_build_index.py`(5, 3)·`qa/check_scope.py` `EXPECTED`(5, 3)도 같습니다.

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-23)

| 절 | 형식 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 워크플로우와 에이전트 경계 | experiment | 5 | 83 | 2 | 0 | 0 | 0 | 7 | 12 | 3 | 24 |
| 02 워크플로우가 충분한 조건 | experiment | 5 | 81 | 6 | 0 | 0 | 0 | 7 | 14 | 3 | 30 |
| 03 모델-도구 루프와 정지 조건 | experiment | 5 | 80 | 3 | 0 | 0 | 0 | 7 | 16 | 3 | 29 |
| 04 자율성의 대가 | experiment | 5 | 79 | 8 | 1 | 0 | 0 | 7 | 10 | 3 | 29 |
| 05 제품 트레이스와 자율성 진단 | experiment | 5 | 93 | 7 | 2 | 0 | 0 | 7 | 17 | 3 | 36 |
| **합계** | | **25** | **416** | **26** | **3** | **0** | **0** | **35** | **69** | **15** | **148** |

- 통과 절 **0/5**.
- **G3 0건은 착시입니다.** 코드 셀 25개 **모두** 첫 줄이 같은 틀 문장 `# 이 셀의 계산과 출력에서 현재 단계의 결과를 확인합니다.`입니다. 게이트 정규식(`이 셀은 … (수행|출력)합니다`)이 「이 셀의 …확인합니다」를 잡지 못합니다. 규격 §2-5 결함 25건이고, 제 역할을 하는 주석은 04 cell[3] 둘째 줄 하나뿐입니다. 고친 뒤에도 게이트가 이 틀을 잡지 못하므로 사람이 봐야 합니다.
- G4 0건 = 가짜 모델도 없고 **모델 호출 자체가 없음**(`temperature`·`reasoning_effort` 해당 없음).
- G1 26건 = 제너레이터 식 17 · 리스트 내포식 4 · 딕셔너리 내포식 1 · 집합 내포식 1 · 조건 표현식 2 · `lambda` 1.
- G2 3건 = 한 글자 `e`(04 cell[9] · 05 cell[7]) · 두 겹 호출(05 cell[11]).
- G5 35건 = 절마다 `title_cell_missing` · `core_figure_attachment_missing` + 코드 셀 다섯 모두 결과 읽기 인용 없음.
- G6 69건 = 70자 넘는 문장 42 · 영문으로 시작해 조사가 붙은 문장 21 · 빽빽한 단락 6.
- G7 15건 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 금지·미교육 문법 (AST로 따로 셈)

- **클래스 정의 3개**: `Case(TypedDict)`(01 cell[5]) · `TraceEvent(TypedDict)`(03 cell[5]) · `CostEvent(TypedDict)`(04 cell[3], 준비 셀 안). 과정에서 클래스는 Ch 13 상태 형식뿐이고 Ch 14~16은 0건입니다.
- **타입힌트**: 함수 넷 모두 인자·반환(`Mapping[str, object]`·`list[bool]`·`str | None`·`dict[str, int]`), 변수 주석 10곳(`cases: list[Case] = …` 등)과 TypedDict 칸 주석 12곳. Ch 13~16은 0건입니다.
- **기본값 매개변수**: 03 `stop_reason(events, max_steps=6, max_cost=4)`.
- **딕셔너리 합치기 `|`**: 01 cell[9] `cases[0] | {"tool_count": 3}`.
- **별표 풀기**: 자리 찾기 셀 다섯의 `(start, *start.parents)`, `print(*cases, sep="\n")`(01 cell[5] · 04 cell[5]).
- **`next(… for … if …)`**: 자리 찾기 셀 다섯(규격 §2-3 명시 금지).
- **f-string 안 계산**: 02 cell[9] `f"{delta:.1f}"`(형식 지정 + 조건 표현식과 `isinstance`).
- **처음 쓰면 풀어야 하는 이름**(과정 0건): `Counter`·`Mapping`(01) · `zip`·중첩 풀기 `for (_, weight), answer in zip(…)`·`isinstance`(02) · `any`(03) · `max(…, key=…)`·`sorted`(04) · `all`(05) · `is True`/`is None`/`is False` 비교 · `dict()`.
- **인코딩 없는 파일 읽기**: 05 `(LAB / …).read_text()` 셋 · `csv.DictReader((LAB / …).open())`. 과정 관례는 `with open(…, encoding="utf-8")`입니다.
- **한 셀에 함수 정의와 호출**: 01 cell[7] · 02 cell[7] · 03 cell[7] · 04 cell[7](규격 §2-2 「정의 셀과 호출 셀을 나눕니다」).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 호출 | 손으로 적은 값·가짜 기록 | 금지 문법(셀) | 금지어(`_src` 블록 / 노트북) | `assert`(무엇에 걸렸나) |
|---|---|---|---|---|---|---|
| 01 | 시스템 사례 넷을 칸 넷(`name`·`steps`·`decision_owner`·`unknown_steps`)으로 적고, `architecture(case)`가 「`decision_owner == "model"` 그리고 `unknown_steps is True`」일 때만 「에이전트 후보」로 나눔(2/2). 환불 사례에 `tool_count` 3을 덧붙여도 분류가 그대로 → 「도구 수 ≠ 결정권」 | **0** | 사례 넷 전부(단계 수 4·None·3·None, 결정 주체, 단계를 모름 여부), `tool_count: 3` | cell[3] 제너레이터·`next`·별표 · cell[5] TypedDict 클래스·변수 주석·`int \| None`·`print(*…, sep=)` · cell[7] 정의+호출 한 셀·타입힌트·`is True` · cell[9] 딕셔너리 `\|` · cell[11] `Counter`+제너레이터·`dict()` | 경로 b4×5·b7·b8×2·b9 / md 2 · 반환 b4×2 / md 2 · 검증 b2·b3·b8 · 분기 b6 / md 1 · 사전 b4 / md 1 · 노드·엣지 b3(Ch 13 되짚기) · 라우팅 b4·b7·b9 · 페이지 b9×4 | 2개 — `architecture(refund) == "워크플로우"`(손 값) · `counts == {…: 2, …: 2}`(손 값 집계) |
| 02 | 진단 질문 다섯과 가중치(2·1·1·1·1, 최대 6)를 튜플로 적고 두 가상 프로젝트의 참/거짓 응답으로 `workflow_score` 6·1점 → 「워크플로우 우선」/「제한된 에이전트 검토」(기준 4). 모델 판단 두 단계를 더한 가상 시나리오의 호출·지연·비용 차이를 계산. 기준 3·4·5로 바꿔도 추천이 같음 | **0** | 가중치·응답 목록, **`fixed_scenario = {"calls": 2, "latency_s": 2.4, "cost_units": 2}` · `agentic_scenario = {4, 5.9, 5}` — 잰 적 없는 지연·비용** | cell[3] 제너레이터·`next`·별표 · cell[5] `sum(… for _, weight in …)` · cell[7] 정의+호출 한 셀·`zip`·중첩 풀기·**조건 표현식**·타입힌트 · cell[9] `isinstance`·**조건 표현식·f-string 형식 지정** · cell[11] **딕셔너리 내포식** | 임계값 b4·b5·b7 / md 2·출력 「임계값 3·4·5」 · 경로 b1·b4×3·b5 / md 1 · 분기 b4·b7×2 · 검증 b4×2·b9 / md 1 · 사전 b4 / md 1 · 페이지 b9×4 · b3 「계획 비용과 최대 호출 수」(Ch 16 옛 말) | 4개 — 손 응답 점수 6·1, 손 시나리오 차 2·3 |
| 03 | 모델·도구가 번갈아 나오는 사건 다섯(`step`·`actor`·`event`·`progress`·`cost`)에 `stop_reason(events, max_steps=6, max_cost=4)`을 적용(완료 → 사람 확인 → 최대 단계 → 예산 순서로 검사). 완료 사건을 뺀 목록은 `None`(실행 중), 손으로 만든 세 목록이 「최대 단계」·「예산」·「사람 확인」. **루프를 실제로 반복하지 않는 판정기** | **0** | 사건 다섯 + 덧붙인 사건 넷(`progress` 0.20~1.00, `cost` 0~2) | cell[3] 제너레이터·`next`·별표 · cell[5] TypedDict·변수 주석(15줄) · cell[7] 정의+호출 한 셀(15줄)·**기본값 매개변수**·`str \| None`·`any`·`sum` 제너레이터 둘 · cell[9] `is None` · cell[11] 목록을 줄 이어 붙이기·`.9` 표기·튜플 풀기 | 반환 b4×5·b8·b9 / md 2 · 경로 b2×3·b4·b5·b6×3·b8 · 노드·엣지 b3 · 「하드 리밋」 b4 · 시뮬레이션 b1·b4 / md 2 · b3 「최대 호출 수」(Ch 16 옛 말) | 4개 — 손 사건 목록 판정(`None`·「최대 단계」·「예산」·「사람 확인」) |
| 04 | 「같은 답에 닿았다」고 가정한 합성 궤적 둘(워크플로우 3사건 / 에이전트 후보 5사건)의 `ms`·`cost`를 `metrics()`로 합해 단계 3·5, 1,170ms·2,990ms, 비용 단위 2·4, 검색 0·2. 가장 긴 사건(`max(key=lambda)`)과 반복 사건(집합 내포식), 손으로 적은 둘째 경로와 `==` 비교(`False`) | **0** | **사건별 `ms` 240·900·30 / 650·380·720·410·830과 `cost` — 잰 적 없는 지연**, 둘째 경로 목록 | cell[3] 제너레이터·`next`·TypedDict(준비 셀 안) · cell[5] 변수 주석·`print(*…)`(15줄) · cell[7] 정의+호출 한 셀·`sum` 제너레이터 셋·타입힌트 · cell[9] **`lambda`·집합 내포식·제너레이터 겹침·한 글자 `e`·`sorted`·`max(key=)`** · cell[11] 리스트 내포식 | 경로 b1·b2·b4×6·b6×3·b8·b9 / md 6·출력 「첫 경로:」 등 · 궤적(새 용어) · 반환 b4×2 / md 2 · 집합 b4 / md 1(「집합 표현식」을 설명) · 사전 b4 · 마스킹 b7·b9 · 프롬프트 b7 · b3 「계획 비용 상한을 분리」(Ch 16 옛 말, 틀린 설명) | 3개 — 손 값 합 1170, 단계 5, 손 목록 둘이 다름 |
| 05 | 공개 궤적 추출본 둘(SWE-agent 14사건 · mini-SWE-agent 10사건, 원본 커밋·URL·SHA-256·MIT)을 읽어 사건 순서·실패 뒤 다음 행동·코드가 정한 경계를 출력. 제품 문서 단서 셋(Codex·Claude Code·Deep Research, `local_execution: false`)과 증거 수준을 가르고, 진단 예시(「워크플로우 유지」)와 빈 진단표 9행을 읽음 | **0**(실행 중 외부 서비스 0 — URL은 자료에 적혀 있을 뿐) | 자료 파일 넷(보호). 손 값은 없음 | cell[3] 제너레이터·`next`·별표 · cell[5] assert 안 리스트 내포식·`all(제너레이터)`·`" → ".join(제너레이터)` · cell[7] 리스트 내포식 둘·한 글자 `e` · cell[9] `all(… is False …)` · cell[11] 겹친 호출 `list(csv.DictReader((LAB / …).open()))`·인코딩 없음 | 경로 b4×2·b6·b8·b9×2 / 출력 라벨 「경로:」 · 분기 b4·b8 / 출력(자료 값) · 반환 b6 / 출력(자료 값) · 거부 b6 / 출력(자료 값 「편집 거부 뒤」) · 검증 b3 / 출력(자료 값 「출처 검증 실패」) · 옵션·스팬·트레이스·대시보드 b4 · 출력 라벨 「하드코딩 경계:」 · 페이지 b2·b9×4 | 6개 — 모두 **자료 파일 값**(사건 수 `[14, 10]`, 해시 길이 64, 10번째 `failure`, 마지막 `unconfirmed`, `local_execution is False`, `recommended_architecture`) |

- **서비스 요청 합계 0번**, 임베딩 0, 외부 서비스·Docker·DB 0. **걸린 시간·비용을 재는 코드 0**(02·04의 초·ms·비용 단위는 모두 손으로 적은 값).
- 모델 문장에 건 `assert` 0건(모델이 없음). `assert` 19개가 모두 손 값·자료 값에 걸려 있습니다.
- 준비 셀: `%pip` 셀·키 셀·모델 셀 **없음**. 다섯 노트북 모두 표준 라이브러리만 씁니다(`collections`·`pathlib`·`sys`·`typing`·`csv`·`json`).
- **옛 그림 토큰**: 절마다 `{{svg:NN-흐름}}` 하나(b4 「도식 읽기」). 노트북 토큰은 `{{notebook:slug}}` 하나씩(experiment, `chapter.json`과 같음). Mermaid·삽화 0장.
- 노트북 `metadata.verification`: 다섯 모두 `passed`, 실행일 **2026-09-10**(macOS, Python 3.12.13). `code_sha256` 앞 12자 01 `9b92476f297c` · 02 `c626eca10528` · 03 `5e71259f56e5` · 04 `e7075ed080fa` · 05 `ee9e78fec69c`.
- 코드 줄(주석·빈 줄 뺌): 37·40·51·49·34 = **211줄**, 셀 최대 15줄(03 cell[5]·[7], 04 cell[5]).
- 노트북 설명 셀: 절마다 8개(제목 · 실행 환경 준비 · 코드를 읽기 전에 · 소제목 넷 · 다른 상황에 적용하기). 「코드를 읽기 전에」·「다른 상황에 적용하기」는 `_src` b4와 **같은 글**(`revision: 2026-09-14-first-use-depth`).
- 복습 문제 절마다 4개(`check_delivery.py`의 3~5 안). 해설 20개 끝이 모두 「오답 시 다시 볼 곳: 이 페이지의 핵심 개념과 실험 결과 해석」 틀입니다(「페이지」 금지어 + 틀 문장).

## 2. 절별로 더 봐야 할 것

### 01 워크플로우와 에이전트 경계
- 준비 셀이 실습 폴더 자리를 찾지만 **01~04는 자료 파일을 읽지 않습니다**(찾은 자리를 한 줄 출력만 함). 자리 찾기 셀이 필요한 절은 05뿐입니다.
- 분류 규칙이 손으로 적은 칸(`decision_owner`)을 그대로 읽습니다. 「로그에서 누가 정했는지 읽는다」(b4 판단 절차)가 아니라 「칸 값을 읽는다」에 머뭅니다.
- b2 「중간 프로젝트에서는 검색, 생성, 출처 검증 순서를 모두 코드로 작성했습니다」 — **과정 요약·계약 파일에 「중간 프로젝트」가 없습니다**(커리큘럼 v6·Ch 1 01·Ch 9 목차에만 나옴). 학생이 무엇을 만들었다고 전제할지 확인이 필요합니다. 02·05 사례(「사내 규정 질의응답」·「중간 프로젝트 규정 RAG」)와 진단 예시 파일도 같은 전제입니다.
- **「경로」가 이 챕터의 중심 말**(워크플로우 = 「미리 작성한 코드 경로」)인데 Ch 13 금지어입니다(§7-12).

### 02 워크플로우가 충분한 조건
- b6 「호출 수 2회, **지연 3.5초**, 비용 단위가 3만큼 더 컸습니다」 — 잰 적 없는 시간을 값으로 적습니다(「합성」 표시는 있음). 과정 규칙 「재지 않은 시간·속도를 단정하지 않는다」(규격 §3)와 부딪힙니다.
- 기준 3·4·5 **모두 같은 추천** → 「민감도 확인」 실험이 대비를 보이지 못합니다(값을 바꿔도 아무것도 안 바뀜). 값 바꿔 보기를 살리려면 경계에 걸리는 사례가 필요합니다.
- b7 「Ch 20에서 고정 분기와 모델 분기를 실제로 실행해 … 측정」 — Ch 20 04절 「if 분기와 모델 선택 비교」가 있음을 확인했습니다(내용은 대조하지 않음, Ch 20은 미개선).

### 03 모델-도구 루프와 정지 조건
- 제목 불일치: `chapter.json`·HTML 「모델 도구 루프와 정지 조건」 ↔ 노트북 첫 셀 「모델·도구·루프와 정지 조건」.
- b4 「도식 읽기」가 스스로 「반복 경로 자체를 표현한 도식은 아닙니다」라고 적습니다 — **루프 절인데 그림에 루프가 없습니다.**
- `stop_reason`은 검사 순서대로 **하나만** 내놓습니다. b7·복습 3은 「발생한 모든 사건을 보존」을 요구하지만 코드는 보여 주지 않습니다.
- 「예산」 정지는 Ch 16 04 `make_budget`·`reserve`(호출 한도·비용 상한을 한 예산 딕셔너리에 예약)와 개념이 겹칩니다. 지금 03은 Ch 16 함수를 부르지 않고, 누적 `cost` 합으로 따로 판정합니다.
- b3 「실제 ToolNode와 조건부 엣지는 Ch 20에서 처음 직접 조립합니다」 · README 「자율 도구 에이전트를 구현하지 않습니다」 — 도구 호출 루프(Ch 19 `@tool`·`bind_tools`, Ch 20 `ToolNode`)를 앞당기지 않게 설계 범위를 지켜야 합니다.

### 04 자율성의 대가
- 사건별 `ms`, 「가장 긴 사건은 830ms의 완료 생성」, 1,170ms·2,990ms가 모두 손 값입니다. **Ch 15 05·06이 `time.perf_counter`·`usage_metadata`·대화당 비용·백분위수를 가르쳤으므로** 이 절은 실제로 잴 수 있는 자리이고, 시간·비용이 주제라 Ch 15 05·06처럼 「재지 않는다」 규칙의 예외 후보입니다(§8-1).
- b4 「코드를 읽기 전에」가 `max(..., key=...)`와 「집합 표현식」을 설명합니다 — 금지 문법을 본문이 가르칩니다.
- b7 「마스킹」(Ch 16 말은 「가리기(마스킹)」) · 「프롬프트」.
- 출력 줄 「Ch 29에서는 이런 중간 궤적을 별도 평가합니다」·b3 「Ch 29」 — Ch 29 02절 「궤적 매칭 네 모드」가 있음을 확인했습니다(내용 대조 안 함). b3 「Ch 15에서는 p50·p95·p99」는 Ch 15 06 본문에 있습니다(확인).

### 05 제품 트레이스와 자율성 진단
- b6가 **13문장 한 단락**(G6 dense). 「원래 입력 23÷0」은 자료 파일·출력에 없는 값입니다(원시 파일에만 있음 — 자료 `evidence`에는 `ZeroDivisionError`와 `output 8.2`만). 규격 §2-6·G5 대조 밖에 있는 인용입니다.
- 자료 값이 대부분 **영어**(`action`·`evidence`, 예: `edit without indentation`) → 출력이 영어 사건 이름으로 채워집니다. 한국어로 바꾸려면 보호 파일을 고쳐야 합니다(§7-5).
- 자료 속 금지어가 출력으로 나옵니다: 「출처 **검증** 실패」·「답과 출처를 **반환**」·「고정 **분기**와 모델 분기」·「편집 **거부** 뒤」·라벨 「하드코딩 경계:」.
- 제품 문서 확인일이 모두 **2026-09-10**(Codex·Claude Code CLI·Deep Research·SWE-agent·mini-SWE-agent). 원시 궤적 해시는 `textbook/part5/qa/ch17-source-evidence.json`에 2026-09-10 확인 기록이 있습니다.
- `textbook/part5/qa/check_bundle_execution.py`가 **이 노트북을 묶음에서 API 키 없이** 실행합니다(§4-1).

## 3. 실습 폴더 구조

```
labs/part5/ch17-agent-overview/
  README.md (1485B)   pyproject.toml   uv.lock
  author_chapter.py   (60KB 옛 생성기 — 자료 넷·노트북 다섯·_src 다섯을 씀)
  data/autonomy-diagnostic-example.json · autonomy-diagnostic-sheet.csv
       product-trace-evidence.json · public-trace-extracts.json
  notebooks/01~05-*.ipynb
  __pycache__/author_chapter.cpython-312.pyc · .ruff_cache/ · .venv/ (macOS 판, 105MB)
  (없음: tests/ · runs/ · 모듈 · 도구 파일)
```

### 3-1. `data/` — 코드로 읽는 곳

| 파일 | 크기·내용 | **코드로 읽는 곳** | 쓰는 곳 |
|---|---|---|---|
| `autonomy-diagnostic-example.json` | 715B. 칸 11개(`project`·`goal`·`path_predefined`·…·`recommended_architecture` 「워크플로우 유지」·`reason`·`next_measurement` 「Ch 20에서 …」). 값에 「출처 검증 실패」·「반환」·「분기」 | **05 cell[11]** `json.loads((LAB / …).read_text())` | 옛 생성기 `write_data()`만 |
| `autonomy-diagnostic-sheet.csv` | 594B. 칸 `id`·`question`·`answer`·`evidence`, 9행(질문 8 + 「권장 구조와 근거」), 답 칸 비어 있음 | **05 cell[11]** `csv.DictReader(…open())` | 같음 |
| `product-trace-evidence.json` | 2587B. 제품 셋, `local_execution: false`, `checked` 2026-09-10, `observable_events`·`limitation` | **05 cell[9]** | 같음 |
| `public-trace-extracts.json` | 6035B. 궤적 둘(14·10사건), 원본 SHA-256 `8856076e…`·`86d060a4…`, `recovery_pairs`·`hardcoded_boundary`·`interpretation_limit` | **05 cell[5]·cell[7]** | 같음 |

- **01~04는 자료 파일을 하나도 읽지 않습니다**(모든 값이 셀 안 손 값).
- 이 네 파일을 코드로 읽는 곳은 **05 노트북뿐**입니다(`grep` — `textbook`·`labs`·`.moai`). `textbook/part5/public-files.json`·챕터 `qa/public-files.json`·`textbook/part5/qa/final-manifest.json`은 경로·해시만 적습니다.
- 원시 궤적 원본(`.traj`)은 저장소에 없습니다(추출본만).

### 3-2. 옛 생성기

| 파일 | 무엇을 | 부르는 곳 |
|---|---|---|
| `labs/part5/ch17-agent-overview/author_chapter.py`(60KB) | `write_data()`·`write_notebooks()`·`write_sources()` — **실행하면 보호 자료 넷과 노트북·`_src`를 옛 판으로 덮어씁니다** | 0(`__main__`만) |
| `textbook/part5/ch17-agent-overview/figures/_gen_figures.py` | `NN-흐름.svg`·`.excalidraw`·`.caption.md` 생성(독립 — `textbook/part5/_figure.py`를 쓰지 않음) | 0 |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part5_enrich.py` | Ch 17 `_src`·노트북에 「코드를 읽기 전에」·「다른 상황에 적용하기」 블록을 끼워 넣은 옛 도구 | 0(기록만, 막지 않음 — Ch 16 선례 `part4_final_repairs.py`와 같음) |

→ 규격 §8 1번대로 **01절 작업 때 앞의 둘 첫머리에 설명 주석 + `raise SystemExit(...)`**, 챕터 마감 때 `qa/upgrade/before/generators/blocked/`로 `mv -n`(사본은 이미 `before/generators/`).

### 3-3. 판 (`pyproject.toml` · `uv.lock`)

- `requires-python = ">=3.12,<3.13"`, **`dependencies = []`**, dev `ipykernel==7.3.0` · `nbclient==0.11.0` · `pip==26.2` · `ruff==0.15.6`, `[tool.uv] package = false`.
- `uv.lock`: dev 넷과 의존 36개(`ipython 9.17.1`·`jupyter-client 8.10.0`·`pyzmq 27.2.0`·`tornado 6.5.8` 등). **`langchain`·`langchain-openai`·`python-dotenv`·`openai`가 없습니다** → 모델을 부르려면 의존성 추가 + `uv lock` + `%pip` 셀 + README + 묶음 재생성(규격 §7-2 `%pip` 항목).
- Part 5 다른 챕터 잠금(참고): Ch 18 `openai==2.29.0`(SDK 직접) · Ch 19·20 `langchain==1.4.0`·**`langchain-openai==1.6.0`** · Ch 20 `langgraph==1.2.11`. Ch 16 잠금은 `langchain-openai==1.6.1`입니다.
- 실습 폴더 `.venv`: **macOS 판**(`home = /Users/mhso/.local/share/uv/python/cpython-3.12-macos-aarch64-none/bin`, uv 0.11.6). 기기 VM에서 `bin/python` 링크가 끊겨 쓸 수 없습니다 → 삭제 승인 대상(Ch 16과 같음).

## 4. Part 5 이음새와 앞 챕터 의존

### 4-1. Part 5 공용 파일

| 파일 | Ch 17 관련 내용 | 고치면 따라오는 것 |
|---|---|---|
| `textbook/part5/public-files.json`(6줄) | Ch 17 자료 넷 + Ch 19 `orders.csv` + `labs/part5/continuity-guide.md` | 도구 파일을 만들면 여기와 챕터 `qa/public-files.json` 두 곳에 줄 추가(규격 §2-7 6) |
| 챕터 `qa/public-files.json`(12줄) | README·`pyproject.toml`·`uv.lock`·자료 넷·노트북 다섯, 제외 `author_chapter.py` | 실습 절·도구 파일 줄 |
| `textbook/_notebook/build_bundle.py` | 노트북은 **`_src/NN-*.html` 슬러그로 자동 선택**, 실습 폴더마다 `pyproject.toml`·`uv.lock`·README, 자료는 `textbook/part5/public-files.json` | 실습 절 `_src`를 만들면 노트북이 자동으로 묶음에 들어감 |
| `textbook/part5/_build_index.py` | `CHAPTERS` Ch 17 `(5, 3, '실행 기록에서 다음 처리를 정하는 주체를 구분하고, 자신의 프로젝트에 필요한 자율성 범위를 정합니다.')`, 머리 「총 48시간 · 강의 18시간 · 실습 30시간」 고정, 모든 절 `verify_lesson`, `part5-practice.zip`(+ `labs/part1/ch04-data-tools/`) | 마감 때 설명 한 줄 대조·재실행 |
| `prerequisite-files.json` | **Part 5에는 없습니다**(Part 6·7에만) | — |
| `qa/check_delivery.py` | 챕터 수 4, 절마다 b1~b10·복습 3~5, `part5-practice.zip`·`llm-practice.zip` 바이트 대조(`llm-practice.zip`은 Stale — 알려진 멈춤) | — |
| `qa/check_bundle_execution.py` | 묶음을 풀어 **Ch 17 05**(+ Ch 19 01 · Ch 20 03)를 `uv sync --locked` 뒤 `--cwd notebooks`로 **API 키 없이** 새 커널 실행, `code_sha256`이 원본과 같아야 통과 | 05가 모델을 부르면 키가 없어 멈춤. 05가 도구 파일을 가져오면 묶음 `notebooks/`에 있어야 함 |
| `qa/check_scope.py` | `EXPECTED` Ch 17 (5, 3), **`SECTION_COUNTS` Ch 17 = 5**, meta 정규식 `강의 Nh`·`실습 Nh`·`새 용어 N`(7 이하) | 실습 절 meta 「실습 30분」은 `Missing scope`로 멈춤, 절 수 6이면 실패 |
| `qa/check_notebook_readiness.py` | Part 5 노트북 **21개**, 함수마다 **타입힌트 필수**, 노트북마다 `assert` 1개 이상, 셀 25줄 이하 | 과정 관례(타입힌트 0)와 반대. **Part 6 판도 Ch 22 개선 뒤 그대로**(47개·ch22 8절) → 선례는 고치지 않고 기록만 |
| `qa/check_figures.py` | `ch*/figures/[0-9]*.svg`마다 `.excalidraw` 짝 요구 | Mermaid `NN-k-이름.svg`는 짝이 없어 멈춤. Part 4 판도 같은 식이고 Ch 13~16이 고치지 않음 |
| `qa/finalize_evidence.py` | ch18·19·20 언어 검토 해시 + `textbook/part5/_src/index.html` `160d1523…` · `practice-start.md` `5ca16b81…` · `labs/part5/continuity-guide.md` `e0ddb44f…`를 assert(**지금 셋 모두 일치**) | Ch 17 마감에서 `continuity-guide.md`를 고치면 이 스크립트가 멈춤(Ch 16은 Part 4 판을 고쳤음) |
| `labs/part5/continuity-guide.md` · `textbook/part5/_src/index.html` · `practice-start.md` | Ch 17 설명 한 단락·한 문장씩(「어떤 판단을 모델에 맡길지」·「에이전트를 도입할 필요가 없다고 결론 내릴 수도」) | 마감 때 대조 |
| `textbook/_notebook/build_index.py` 38행 | `('17', 'Agent 개요', 'part5/ch17-agent-overview', 5, …)` 절 수 5 | 실습 절 뒤 6. 참고: 같은 파일 Ch 13(30행 7)·Ch 16(36행 6)도 지금 절 수(8·7)와 다름 — 앞 챕터 마감에서 고치지 않음 |
| QA 옛 기록(2026-09-10·14) | `bundle-execution.json`(archive `19acb30a…` ≠ 지금 zip `73746333…`)·`final-manifest.json`·`lesson-scope.json`·`notebook-readiness.json`·`figure-consistency.json`·`language/ch17-*` | 옛 기록, 고치지 않음 |

### 4-2. Ch 17 파일을 읽는 다른 챕터·검사

- **코드로 읽는 곳은 없습니다.** Ch 17 자료는 Ch 17 05 노트북만 읽습니다. 산출 파일(`runs/`)도 없습니다 → 규격 §7-2 「뒤 챕터가 읽는 산출 파일」 걱정은 없습니다.
- **문장으로 기대는 곳**(개선 뒤에도 이 내용이 남아야 뒤 챕터 문장이 맞음 — Ch 18~20은 아직 미개선):
  - Ch 18 04 b3: 「Ch 17에서는 모델이 흐름을 얼마나 결정하는지 자율성의 기준으로 살펴봤습니다.」
  - Ch 20 01 b3: 「Ch17에서는 모델·도구·반복·정지 조건이 에이전트의 구성 요소라는 사실과 자율성의 비용을 확인했습니다.」
  - Ch 20 03 b3: 「Ch17에서 정지 조건 없는 자율성은 비용과 예측 불가능성을 키운다고 배웠습니다.」
  - `labs/part5/continuity-guide.md`: 「자율성을 진단한 결과, 에이전트를 도입할 필요가 없다고 결론 내릴 수도 있습니다.」
- Part 6·7 `_src`는 Ch 17을 부르지 않습니다(0건).

### 4-3. Ch 17이 앞 챕터 파일을 읽는가

- **0건.** 다섯 노트북 모두 표준 라이브러리와 자기 `data/`만 씁니다. Ch 16 `notebooks/guardrails.py`·`runs/`, Ch 15 도구 파일, Ch 13 LangGraph를 부르지 않습니다(Ch 16 요약 §13-2와 같음).
- 문장으로만 부릅니다: 01 b3(Ch 9 첫 RAG · Ch 13 StateGraph 노드·엣지 · Ch 16) · 02 b3(Ch 11·Ch 15 「측정이 튜닝보다 먼저」 · Ch 16) · 03 b3(Ch 13 · Ch 16 · Ch 20) · 04 b3(Ch 15 p50·p95·p99 · Ch 16 · Ch 29) · 05 b3(앞 네 절 · 중간 프로젝트 · Ch 20) · 01 b7(Ch 18 오케스트레이터-워커).

### 4-4. Ch 16 대응표의 옛 말 — Ch 17 자리 (모두 그대로 있음을 확인)

| 자리 | 지금 문장 | 옛 말 → Ch 16 말 |
|---|---|---|
| 01 b3 | 「Ch 16은 입력 검증, 예산 상한, 재시도와 감사 기록을 모델 바깥 코드에 두었습니다.」 | 입력 검증 → **입력 검사** · 예산 상한 → **호출 한도와 비용 상한**(한 **예산** 딕셔너리) |
| 02 b3 | 「Ch 16에서는 호출 전에 계획 비용과 최대 호출 수를 확인했습니다.」 | 계획 비용 → **예상 비용**(04절이 정한 값 0.002달러, 청구 금액 아님) · 최대 호출 수 → **호출 한도** · 확인 → **부르기 전에 예약** |
| 03 b3 | 「Ch 13에서는 … Ch 16에서는 최대 호출 수와 비용 상한을 모델 호출 전에 검사했습니다.」 | 최대 호출 수 → **호출 한도** |
| 04 b3 | 「Ch 15에서는 … Ch 16에서는 호출 수와 계획 비용 상한을 분리했습니다.」 | 계획 비용 상한 → **비용 상한** · 「분리」는 틀림(한 딕셔너리에 함께) |
| 말 전반 | 04 b7·b9 「마스킹」 · 01 b2·b3·b8 / 02 b4·b9 / 03 b7 / 05 b3 「검증」 · 05 b6 「거부」 · 04 b7 「프롬프트」 · 05 자료 「출처 검증 실패」 | 가리기(마스킹) · 검사(출처 검사) · 막습니다 · (시스템 메시지 글 등). 「폴백」·「감사 로그」·「지킬 말」·「프롬프트 인젝션」은 Ch 17에 없음 |

- Ch 16 요약 §14 「Ch 17이 전제하면 안 되는 것」(실제 요금으로 센 비용·걸린 시간 · 모델이 숨은 지시를 따르는 장면 · 실제 서비스 오류 재시도 · 한 흐름 안 재시도·예비 모델·출력 검사 · 미들웨어)과 지금 Ch 17 본문은 부딪히지 않습니다. 다만 02·04의 손으로 적은 초·ms를 「잰 값」처럼 쓰면 첫 항목과 어긋납니다.

## 5. §2-7 판단 근거 — 도구 파일

### 사실
1. **앞 챕터 함수를 다시 쓰는 곳 0.** 노트북 함수는 넷(`architecture` 01 · `workflow_score` 02 · `stop_reason` 03 · `metrics` 04)이고 각각 한 절에서만 정의·사용합니다.
2. **챕터 안 되풀이는 자리 찾기 준비 셀 다섯뿐**(7~10줄). 그중 01~04는 자료를 안 읽어 셀 자체가 필요 없고, 과정 관례상 자리 찾기는 도구 파일이 아니라 셀(후보 셋 + `for`·`break`)로 둡니다.
3. 벡터 계산이 없어 NumPy 대상도 없습니다.
4. 05는 03·04 함수를 쓰지 않습니다(공개 궤적에 `stop_reason`·`metrics`를 대지 않음).
5. Ch 16 `guardrails.py`의 `make_budget`·`reserve`는 03 「예산」 정지와 뜻이 겹치지만 Ch 17은 부르지 않습니다.

### 선택지 (결정하지 않음 — 장단점만)

**A. 도구 파일을 만들지 않는다**(Ch 1·2·4·6·22 선례)
- 장점: 파일·묶음 목록 두 곳·README·`check_bundle_execution.py`가 움직이지 않음. 지금 코드 211줄에 옮길 되풀이가 없어 규격 §2-7 3항(「챕터 전체가 줄지 않으면 만들지 않음」)에 그대로 맞음.
- 단점: 06 실습 절이 01~04 함수를 다시 쓰면 06에 다시 적어야 함(넷이면 약 30줄), 아니면 06을 새 함수 없이 설계해야 함.

**B. `notebooks/trace_tools.py`**(이름 후보: `trace_tools.py` — 사건 기록 읽기가 챕터 중심 / `agent_tools.py` — Part 5 뒤 챕터와 이름이 겹칠 위험 / `autonomy_tools.py` — 진단표 중심)
- 담을 것: 03 `stop_reason`·04 `metrics`(+ 01 `architecture`·02 `workflow_score`). 가져가는 절: 05(공개 궤적에 03·04 판정기를 대 보는 설계를 고를 때) · 06.
- 장점: 「같은 판정기를 실제 공개 기록에 대 본다」 흐름이 생기고 06이 짧아짐.
- 단점: 05 자료 모양(`step`·`action`·`outcome`)이 03·04 사건 칸(`actor`·`event`·`cost`)과 달라 인자 모양을 맞춰야 함. 가져가는 절이 06 하나뿐이면 A와 줄 수 차이가 작음. 묶음 목록 두 곳과 `check_bundle_execution.py`(05가 가져오면)에 영향.

**C. 모델 호출을 넣는 설계라면**(§8-1 (나)·(다)) — 모델 부르기·사건 한 줄 남기기 같은 공통 함수(예: `ask_next_step`·`note_event`)가 01·03·04·06에 되풀이될 수 있어 도구 파일 효과가 커집니다. Ch 16 `make_budget`·`reserve`를 예산 정지에 다시 쓰면 도구 파일에 `# Ch 16 04절에서 배웠습니다`로 옮겨야 합니다(Ch 16 요약 §13-2 「Ch 17 규격에 맞게 따로 정하세요」). 단점은 B와 같고, 모델 호출이 05에 들어가면 `check_bundle_execution.py`가 멈춥니다.

→ **결정 기준**: 06 실습 절이 앞 절 함수를 몇 개 다시 쓰는지 + §8-1(모델 호출 여부). 01절에서 정해 `handoff.md`에 적어야 01~04 함수 인자 모양이 갈라지지 않습니다.

## 6. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약·계약 §1 + Part 1~4·Ch 22 `figures/*.prompt.md` 파일 이름): 카드·카드 상자·책상·봉투·칸막이 상자·공책·장부·잠긴 상자·주머니·띠·문패·서랍·표찰·쟁반·끈·서가·단추·과일(사과)·자물쇠·관·깔때기·**나무 길·갈림길·세 갈래 길(Ch 13)·막힌 길과 옆길(Ch 6 05)**·작업대·표지판·칸 상자·나무판·마개·바구니·저울·동전·모래시계·궤짝·선반·눈금·스티커·도장·도장 대장·덮개 천·두루마리·개찰구·체·조약돌·구슬·우편함·명찰·클립보드·**공항 검사 지점(Ch 22 01)**·교통카드 개찰구·방문자 명부·서류함·안내 데스크·**택배 상자(Ch 3 01)**·자물쇠·깃발·블록·퍼즐 조각·빵 칼·돋보기.
- Ch 17 옛 본문 비유(공항 수하물 벨트 · 버스 노선표와 복구 차량 · 탐사팀 · 택배 배송 기록 · 경기 중계 하이라이트)는 공항·택배가 앞 삽화와 겹칩니다. **「길·갈림길」 계열은 Ch 13이 썼으므로** 「누가 다음 걸음을 정하나」를 길 그림으로 그리면 겹칩니다.

| 후보 | 그림 요소 | 맞는 절 | 겹침 점검 |
|---|---|---|---|
| **눈 위 발자국** | 빈 눈밭에 곧게 이어진 발자국 한 줄 / 멈췄다 돌아가며 고리를 그린 발자국 한 줄 | 01(누가 다음 걸음을 정했나) · 04(고리 = 반복·긴 기록) · 05(발자국만 보고 알 수 있는 것과 없는 것) | 겹침 없음. 「길」 계열과 가르려면 길·표지판·울타리 없이 눈밭과 발자국만 |
| **로봇 청소기와 충전대** | 바닥 위 청소기와 지나간 자국, 벽의 충전대(완료), 막대 칸으로 된 배터리(예산), 문턱 앞에 멈춘 모습(사람 확인) | 03(모델-도구 루프와 정지 조건) | 겹침 없음. 화면·표시 글자 금지(「no display, no symbols」), 배터리는 막대 칸 모양으로 |
| **자판기와 가게 점원** | 버튼을 누르면 정해진 칸에서 물건이 나오는 자판기 / 손님 말을 듣고 선반을 살펴 물건을 고르는 점원 | 01 · 02(자판기로 충분한 물건) | 자판기는 없음. 「동전」(Ch 11·15)은 그리지 않고 버튼에 글자 없음 |
| **오르골 원통과 손으로 치는 건반** | 핀이 박힌 원통(미리 정한 차례) / 소리를 듣고 다음 음을 고르는 손 | 01 · 02 | 겹침 없음. 관계가 추상적이라 「그림만 보고 관계가 읽히는가」 탈락 위험이 위 셋보다 큼 |
| (보조) 장난감 기차 선로와 전환 손잡이 | 선로 위 기차, 사람이 미리 돌려 둔 전환 손잡이 | 01 | Ch 13 갈림길과 겹칠 수 있어 뒤로 |

- 한 계열로 챕터를 이을지(예: 발자국 01·04·05 + 로봇 청소기 03 + 자판기 02), 절마다 다를지는 01 작업자가 정합니다.

## 7. 위험과 깨진 것

1. **G3 착시** — 25셀 모두 틀 문장(§0). 게이트가 0이라 놓치기 쉽습니다.
2. **손으로 적은 지연·비용** — 02 `latency_s` 2.4·5.9, 04 `ms` 240~900과 결과 해석 「지연 3.5초 더 컸다」·「1,170ms·2,990ms」·「가장 긴 사건 830ms」. Ch 12~16이 지킨 「걸린 시간을 재지 않았습니다」와 부딪힙니다. 「합성」이라고 밝혔어도 그림 라벨·결론에 넣으면 잰 값으로 읽힙니다.
3. **모델 호출 0** — 규격 §3은 가짜 모델만 금지하므로 위반은 아닙니다(Ch 13 01~06도 0번). 그러나 Part 5 첫 챕터가 「에이전트」를 손 기록으로만 보입니다. 모델을 넣으면 `pyproject.toml`(지금 `dependencies = []`)·`uv.lock`·`%pip` 셀·README·묶음 재생성·`check_bundle_execution.py`(05)가 함께 움직이고, Ch 18(오케스트레이터)·Ch 19(`@tool`)·Ch 20(`ToolNode`)을 앞당기지 않게 범위를 정해야 합니다.
4. **흔들림 확인 대상(모델을 넣을 때만)** — 01 「모델이 다음 행동을 고르는가」, 03 「모델이 스스로 끝내는가 / 최대 단계에 걸리는가」, 04 「에이전트 쪽이 검색을 더 하는가 · 단계 수 · 토큰 · 걸린 시간」은 모두 모델 답에 달려 다시 실행하면 뒤집힐 수 있습니다 → 규격 §2-7 10번 끝(노트북 밖 5번)을 먼저. **지금 판(모델 없음)은 다섯 절 모두 결정적**이고 흔들릴 값이 없습니다.
5. **보호 자료 속 금지어·영어** — 05 출력에 「출처 검증 실패」·「답과 출처를 반환」·「고정 분기와 모델 분기」·「편집 거부 뒤」·영어 사건 이름. 바꾸면 보호 파일 변경(`before-manifest.json` 대조 · `manifest-changes.md`) + 공개 원문 해시(`ch17-source-evidence.json`)와의 관계를 README·본문에 적어야 합니다. 두면 결과 읽기에서 풀어야 합니다.
6. **05 b6 「23÷0」** — 자료·출력에 없는 값(원시 파일에만). 「8.2」·「344」·「345」는 자료 `evidence`에 있음.
7. **옛 생성기 `author_chapter.py`가 보호 자료 넷을 덮어씀** — 01 작업 첫머리에 `raise SystemExit`.
8. **Part 5 옛 검사 스크립트 넷이 개선 결과와 충돌**(§4-1): `check_figures.py`(Mermaid SVG에 `.excalidraw` 요구) · `check_scope.py`(절 수 5 · 실습 절 meta 정규식) · `check_notebook_readiness.py`(타입힌트 필수 · 21개 · 노트북마다 `assert`) · `finalize_evidence.py`(`continuity-guide.md` 해시 고정). Part 4·6 선례는 고치지 않고 기록만 남겼습니다.
9. **`check_bundle_execution.py`** — 05를 묶음에서 키 없이 실행하고 `code_sha256`을 원본과 대조. 05 설계(모델 호출·도구 파일 가져오기)가 이 검사에 직접 걸립니다.
10. **인코딩 없는 파일 읽기**(05) — Windows 학생 기기에서 한국어 JSON·CSV가 기본 인코딩(cp949)으로 읽혀 깨질 수 있습니다.
11. **자리 찾기 셀**(`next(… for …)`·`(start, *start.parents)`) — 규격 §2-3 금지. 01~04는 필요 없고, 05·(06)만 과정 관례(후보 셋 + `for`·`break`, 「notebooks 폴더나 실습 폴더 맨 위」)로 바꾸면 됩니다.
12. **「경로」가 챕터 핵심어인데 Ch 13 금지어** — `_src` 42곳 + 노트북 설명 12곳 + 출력 라벨. 새 용어 「경로 예측 가능성」(02)·「경로 편차」(04)도 걸립니다. 「분기」 6·「반환」 12·「임계값」 3·「검증」 8·「사전」(dict) 3도 함께 정해야 합니다.
13. **비용**: 지금 0달러. 모델을 넣어도 `gpt-5.4-mini` 한 요청 요금 어림은 0.001달러 아래 수준(Ch 16 14번 요청 합이 0.01달러 아래)이라 절당 1달러 상한과 거리가 멉니다. 외부 서비스·Docker·DB 없음. 루트 `.env`에 `OPENAI_API_KEY` **이름** 있음(값은 보지 않음).
14. **판 차이(모델을 넣을 때)**: Ch 16 잠금 `langchain-openai 1.6.1` ↔ Ch 19·20 잠금 `1.6.0`. Part 5 안에서 어느 쪽을 따를지.
15. 옛 그림 03이 루프를 그리지 않음(b4 본문이 한계를 적음). 04·05 「도식 읽기」의 색 설명(초록 입력·파랑 코드·보라 모델·노랑 측정)은 옛 SVG 기준.
16. 참고 자료 영어 제목 줄이 G6 긴 문장으로 셈(05 두 줄) — Ch 5 03-6 방식(`<li><div><a>원제목</a></div>확인일</li>`).
17. 복습 해설 20개가 모두 「이 페이지의 핵심 개념과 실험 결과 해석」 틀(「페이지」 금지어).
18. **디스크**: 기기 루트(`/`·`/tmp`) 여유 약 **2.5G**(`/tmp/mmd` 471M · `/tmp/pptr-cache` 658M · `/tmp/uv-cache` 165M 포함). 가상환경은 마운트 폴더 `.cache/vm`(131MB). Mermaid 도구(`/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`·`/tmp/pw`)는 지금 있습니다.

## 8. 01절 작업자가 먼저 결정해야 할 것

1. **실제 모델을 부를지, 어느 절에서** — (가) 지금처럼 0번(Ch 13 01~06 선례): 손 값은 「이 절에서 정한 예」로 밝히고 합성 초·ms는 빼거나 단위 없는 정한 수로. (나) 04만 실제로 잼(Ch 15 05·06처럼 시간·비용이 주제인 절의 예외 — `time.perf_counter`·`usage_metadata`, 흔들린 값은 「이번 실행에서는」). (다) 01·03에도 모델이 다음 행동을 **글로만** 고르는 장면(도구 실행·`bind_tools` 없이 — Ch 19·20을 앞당기지 않게). 고른 것에 따라 `pyproject.toml`·`uv.lock`·README·묶음·`check_bundle_execution.py`(05)가 따라옵니다.
2. **「경로」 대체어와 챕터 용어 표** — 워크플로우 정의(「미리 작성한 코드 경로」)·「경로 예측 가능성」·「경로 편차」와 「분기」·「반환」·「임계값」·「검증」·「사전」을 무엇으로 부를지, 「궤적(trajectory)」·「트레이스」·「스팬」을 어떤 한국어로 먼저 풀지 01에서 정해 `handoff.md`에 적기. 뒤 챕터(Ch 18 04·Ch 20 01·03 b3)가 쓰는 「결정 주체·정지 조건·자율성의 비용」은 남기기.
3. **손 기록의 모양과 칸 이름** — 01 사례 칸, 03 사건 칸(`actor`·`progress`·`cost`), 04 사건 칸(`ms`·`cost`)을 뒤 절·실습 절이 같은 모양으로 이어 쓰도록 한 번에 정하기(과정 관례: 클래스·타입힌트 없이 한국어 키 딕셔너리). 특히 04 `ms`를 둘지(§7-2).
4. **§2-7 도구 파일** — A(만들지 않음) / B(`trace_tools.py`) / C(모델 호출 공통 함수 포함). 06 실습 절이 쓸 함수 목록을 미리 정해야 합니다.
5. **05 보호 자료를 고칠지** — 영어 사건 이름·자료 속 금지어를 두고 결과 읽기로 풀지, 자료를 한국어로 바꿔(보호 파일 변경) 출력을 고칠지. 「23÷0」처럼 출력에 없는 값을 본문에 둘지. 05를 `check_bundle_execution.py`가 키 없이 돌릴 수 있게 둘지.

## 9. 챕터 마감으로 미룰 것

- **06 실습 절 신설**(규격 §7-2). 주제 후보: 「규정 RAG 한 요청의 사건 기록에 01~04 판정(결정 주체·워크플로우 적합·정지 이유·단계/비용 셈)을 차례로 대 보고, 값 하나(최대 단계 또는 결정 주체)만 바꿔 다시」. Part 3·4 실습 절처럼 **파일을 쓰지 않는 쪽**이 안전. 따라오는 것: `chapter.json` 절 추가 · 실습 절 meta 「실습 30분」(시수 더하지 않음) · `textbook/part5/_build_index.py` 재실행(목차·zip·`integration-results.json`) · 챕터 `qa/public-files.json` · `textbook/_notebook/build_index.py` 38행 5 → 6 · README · `check_scope.py`·`check_notebook_readiness.py`는 선례대로 기록만.
- `chapter.json` `objectives` 네 줄과 `_build_index.py` Ch 17 설명 한 줄 대조(「다음 처리를 정하는 주체」·「자율성 범위」·「추적 단서」).
- 옛 생성기 둘 `mv -n` → `qa/upgrade/before/generators/blocked/`.
- **옛 그림 열다섯**(`figures/0N-흐름.{svg,excalidraw,caption.md}`) + `figures/_gen_figures.py` 삭제 승인 목록(사본 `before/figures/`), `textbook/part5/qa/figure-consistency.json`·`check_figures.py` 상태 기록.
- `labs/part5/continuity-guide.md` Ch 17 단락 · `textbook/part5/_src/index.html` · `practice-start.md` Ch 17 문장 대조(고치면 `finalize_evidence.py` 해시 assert가 멈춤을 기록).
- `qa/verification.md` · `집필점검표.md` · 실습 폴더 README 다시 쓰기(「외부 API를 호출하거나 자율 도구 에이전트를 구현하지 않습니다」·「25개 코드 셀, 최대 17줄」·옛 실행 명령 — 도구 파일이 생기면 `--cwd …/notebooks`).
- `part5-practice.zip` 재생성, `check_bundle_execution.py`·`check_delivery.py` 실행(`llm-practice.zip` Stale에서 멈춤 예상).
- Ch 18 04·Ch 20 01·03 b3, `continuity-guide.md`가 기대는 말(§4-2)과 개선된 Ch 17 본문 대조.
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 105MB)·`__pycache__`·`.ruff_cache` · `qa/upgrade/gates-wip-*.json` · `.cache/vm/venv-ch17-agent-overview`(빈 껍데기 `ipykernel-7.3.0.data/`·`ipython-9.17.1.data/` 포함) · 기기 `/tmp/ch17-prep`(이 준비 작업의 스캔 스크립트·잠금 목록).

## 10. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 5 · `notebooks` 5 · `figures` 16(SVG·excalidraw·caption 각 5 + `_gen_figures.py`) · `generators` 2(`author_chapter.py`·`_gen_figures.py`) · `data` 4 · `pyproject.toml` · `uv.lock` · `README.md` · `chapter.json` = **36개, 388KB**. 원본과 `cmp` 같음(원본은 그대로). 챕터에 `tests/`·`runs/`·모듈이 없어 그 폴더는 없음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 148) |
| `qa/upgrade/before-manifest.json` | 보호 파일 11개의 sha256 — Ch 17 자료 넷(05가 읽음) · Ch 16 마감 판 다섯(`notebooks/guardrails.py` `d4f76099…` · `tests/test_guardrails.py` `632ab36c…` · `data/retrieved-documents.json` `ae2fe4f4…` · `runs/05-audit.jsonl` `92e3d109…` · `runs/06-audit.jsonl` `736271dd…` — Ch 16 요약의 마감 해시와 같음) · Part 5 묶음에 함께 들어가는 `labs/part5/ch19-model-tools/data/orders.csv`와 원본 `labs/part1/ch04-data-tools/data/orders.csv`(바이트 같음 `f2d1e3ee…`) |
| `$ROOT/.cache/vm/venv-ch17-agent-overview` | Python 3.12.13 · 131MB |

### 가상환경 만든 방법과 걸린 것

- `export UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy` → `uv venv --python 3.12 $ROOT/.cache/vm/venv-ch17-agent-overview`.
- 잠금 판 목록: `uv export --project labs/part5/ch17-agent-overview --frozen --no-hashes --all-groups --no-emit-project`(dev 넷 + 의존, 실습 폴더 파일은 바꾸지 않음).
- **`uv pip install -r`이 마운트 폴더에서 멈췄습니다**: `failed to remove directory …/ipykernel-7.3.0.data: Operation not permitted`(Ch 16의 `jsonpatch` 멈춤과 같은 원인). 우회: `uv pip install pip==26.2` → **`$V/bin/python -m pip install -r`**(주석 뺀 목록).
- 결과: `pip freeze`를 잠금과 대조해 **판 차이 0**(`ipykernel 7.3.0` · `nbclient 0.11.0` · `pip 26.2` · `ruff 0.15.6` · `ipython 9.17.1` · `jupyter-client 8.10.0` · `pyzmq 27.2.0` · `tornado 6.5.8` 등). `pip check` 이상 없음. 확인은 import만(`ipykernel`·`nbclient`·`nbformat`·`jupyter_client`·`IPython`·`zmq`)과 `ruff --version`. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- **`langchain`·`langchain-openai`·`python-dotenv`·`openai`는 넣지 않았습니다**(`pyproject.toml`에 없음). 모델을 부르기로 하면 `$V/bin/python -m pip install langchain==1.4.0 langchain-openai==1.6.1 python-dotenv==1.2.3`(Ch 16 판 — §7-14 참고) 뒤 진단에 적으세요. `run_section.sh`는 `--with python-dotenv==1.2.3`·`--with pillow`를 따로 붙입니다(`UV_NO_SYNC=1`).
- 남은 흔적: 빈 껍데기 `…/site-packages/ipykernel-7.3.0.data/`·`ipython-9.17.1.data/`(파일 0개, 마운트 폴더라 지울 수 없음). 두 패키지는 정상 설치돼 있습니다.
