# Ch 20 ToolNode — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part5/ch20-tool-node`(절 넷 — 01·04 experiment, 02·03 paired) · `labs/part5/ch20-tool-node`. Part 5의 넷째(마지막) 챕터이고 **Ch 19 바로 뒤**입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 34개) · `gates-before.json` · `before-manifest.json`(50개) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch20-tool-node`.
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(§2·§2-7·§3·§5-3·§5-4·§6·§7·§7-2·§8) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약 `qa/upgrade-course-summary.md`(§1·§2 전부·§3·§5·§6·§9) · 계약 `qa/upgrade-contracts.md`(§3 Ch17~19 줄·§4 Ch19 줄·§5 Ch17~19 줄·§8) · Ch 19 `chapter-summary.md`(전부, 특히 §13) · Ch 19 `chapter-lead-notes.md`·`before-manifest.json` · Ch 13 `chapter-summary.md` §1~§4와 01~04·08 노트북의 상태 정의 셀 · Ch 19 `order_tools.py` · Ch 21 01 노트북 도구 셀 · Part 5·6 묶음·검사 스크립트.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 파일 삭제 0건. 모델 호출 0건. 노트북 실행 0건. 모델을 부르지 않는 확인만 했습니다(§5 — import, 설치판 소스 읽기, `/tmp/ch20-prep/`의 작은 그래프로 `recursion_limit`·`ToolNode` 오류 처리 동작 보기, 키는 `env -u OPENAI_API_KEY`로 뺀 채).
- `chapter.json` `hours` = 「총 8h · 강의 3h · 실습 5h」. 절 meta 합 강의 1 + 0.75 + 0.75 + 0.5 = **3h**, 실습 1.5 + 1.25 + 1 + 1.25 = **5h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part5/_build_index.py` 25행 (3, 5)·`qa/check_scope.py` `EXPECTED` (3, 5)도 같습니다. 새 용어 meta 5 + 4 + 4 + 5 = **18**.

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-24)

| 절 | 형식 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 ToolNode와 tools_condition | experiment | 8 | 97 | 7 | 5 | 0 | 2 | 7 | 28 | 3 | 52 |
| 02 도구 오류와 ToolMessage | paired | 7 | 82 | 1 | 1 | 0 | 2 | 7 | 25 | 3 | 39 |
| 03 recursion_limit과 명시적 종료 | paired | 5 | 78 | 1 | 0 | 0 | 0 | 5 | 20 | 3 | 29 |
| 04 if 분기와 모델 선택 비교 | experiment | 12 | 95 | 14 | 13 | 0 | 2 | 5 | 25 | 3 | 62 |
| **합계** | | **32** | **352** | **23** | **19** | **0** | **6** | **24** | **98** | **12** | **182** |

- 통과 절 **0/4**. 코드 줄(`count_code.py`) 88·93·39·144 = **364줄**. **01·02·04에 글자까지 같은 셀 세 벌이 138줄(38%)**: 설치·키 셀 14줄 × 3 · 모델·비용 함수 셀 19줄 × 3 · 규정 자료 + `lookup_policy` 도구 셀 13줄 × 3.
- G1 23 = 제너레이터 식 12 · 내포식 6(리스트 2·딕셔너리 3·집합 1) · 한 셀에 함수 둘 이상 4 · 조건 표현식 1(03). 04에 14건이 몰림.
- G2 19 = 한 글자 이름 15(`m` 7·`r` 6·`q`·`b`) · 15줄 넘는 셀 4(01·02·04의 모델·비용 셀 19줄, 04 집계 셀).
- G3 0 — 그러나 **첫 줄 주석이 모두 틀 문장**입니다(「# ○○에 필요한 연산을 실행합니다.」, 32셀 전부 소제목만 바꾼 꼴). 규격 §2-5 「어느 셀에나 붙일 수 있는 문장은 결함」에 해당하는데 G3 패턴이 못 잡습니다. 2~3줄마다 이유 주석은 0.
- **G4 6 가운데 `fake_model` 3은 착시입니다.** 01·02·04 모델 셀이 반환 힌트용으로 `from langchain_core.language_models import BaseChatModel`을 가져와 걸렸습니다(가짜 모델 클래스는 없음). `temperature_missing` 3은 진짜입니다 — `init_chat_model(f'openai:{MODEL_NAME}', reasoning_effort='none')`에 **`temperature=0`이 없습니다**(`reasoning_effort="none"`은 있음). 03은 모델을 부르지 않습니다.
- G5 24 = 절마다 `title_cell_missing`·`core_figure_attachment_missing` 8 + 결과 읽기 인용 없음 16(결과 읽기 셀 자체가 0).
- G6 98 = 70자 초과 41 · 영문으로 시작해 조사가 붙은 문장 **55** · 빽빽한 단락 2.
- G7 12 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 금지·미교육 문법 (AST로 따로 셈)

- **f-string 10곳**: 모델 문자열 `f'openai:{MODEL_NAME}'`(01·02·04) · 도구 오류 글 `f'지원하지 않는 주제: {topic}'`(01·02·04) · 02 `f'{type(error).__name__}: {error}'`(**f-string 안 계산**)·`f'규정 조회 실패: {error}. …'` · 03 `f'tick:{next_count}'` · 04 `f'{question} 반드시 …'`. Ch 13~19는 f-string 0건입니다.
- **타입힌트**: 함수 정의 19개(절마다 다시 적은 것 포함) 모두에 매개변수·반환 힌트(`-> dict`·`-> str`·`-> BaseChatModel`·`-> tuple[AIMessage, float]`·`-> Literal['tick', '__end__']`, `model: Any`·`messages: list`·`state: AgentState` 등). Ch 13은 노드 함수에 힌트 0(`def normalize(state):`), Ch 19는 `@tool` 함수 매개변수의 `: str`만 허용했습니다.
- **클래스**: 상태 형식 셋 — 01 `AgentState(TypedDict)`(`messages: Annotated[list[AnyMessage], add_messages]`·`trace: list[str]`) · 03 `LoopState`(`count: int`·`trace: list[str]`) · 04 `CompareState`(위 둘 + `measurements: list[dict]`·`strategy: Literal['fixed', 'agent']`). 02는 라이브러리 `MessagesState`를 씀. 필드만 적어 규격 L5 안이고, `TypedDict`·`Annotated`·`add_messages`·`AnyMessage`는 Ch 13 01·02·04가 가르친 모양 그대로입니다(§4-2). 상태 칸의 `Literal`·`list[dict]`는 Ch 13 0건.
- **데코레이터**: 맨 `@tool` 셋(01·02·04, 같은 셀) — Ch 19 01이 가르친 모양.
- **처음 쓰면 풀어야 하거나 과정이 안 쓴 이름**: `[Path.cwd(), *Path.cwd().parents]`(별표 풀기, 01·02·04 준비 셀) · `enumerate`·`getattr`·`any`(01·04) · `sum(생성기)`(01·04) · `{**total, …}`·`{**usage_of(reply), …}`(딕셔너리 풀기, 01·04) · `collections.defaultdict`·`statistics.mean`·`.items()`(04) · `from typing import Any`(01·02·04, 한 곳에서만 씀) · `MessagesState`(02) · `GraphRecursionError`·설정 딕셔너리 `{'recursion_limit': 4}`(03) · `'__end__'` 문자열(03 반환 힌트·04 `path_map`) · `+=`(모델·비용 셀).
- **한 셀에 함수 둘·정의와 호출 섞임**: 01·02·04 모델 셀(`usage_of`+`make_model`) · 01 c10(상태 클래스 + 모델 객체 + 노드) · 02 c14(처리 함수 정의 + ToolNode + 그래프 + 실행 + 출력) · 03 c6(클래스 + 노드 + 그래프) · 03 c10(조건 함수 + 그래프) · 04 c18(`mark_tools`+`answer`).
- **줄 길이**: 04 c16 `choose` 본문 9줄(10줄 한도 근처)·c22 `run_branch` 본문 13줄(**L2 10줄 초과**, G1·G2가 안 셈).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(이번 출력) | 손 값 | 금지 문법(셀) | 금지어(`_src` 블록 / 노트북 md 수) | `assert`(무엇에) |
|---|---|---|---|---|---|---|
| 01 | 자료실 규정 딕셔너리 셋(대출·운영·연체) + `@tool lookup_policy(topic: str)`(없는 주제면 `ValueError`) · 직접 정의한 `AgentState`(메시지 칸에 `add_messages`, `trace` 칸은 규칙 없음) · `StateGraph`에 `model` 노드(`bind_tools`한 모델)와 `ToolNode(TOOLS)`, `add_conditional_edges('model', tools_condition)`, `tools → model` · 구조 문자열 출력 · 대출 질문 → Human·AI(`tool_calls` `lookup_policy {'topic': '대출'}`)·Tool·AI 네 메시지, `trace ['model', 'model']` · 인사 질문 → Human·AI 둘 | **3**(대출 2 + 인사 1) | 규정 글 셋 · 요금 0.75·4.50 · 질문 둘 | c4 별표 풀기 · c6 f-string·힌트·함수 둘·19줄 · c8 f-string·힌트 · c10 클래스·힌트 · c14 `enumerate`·`getattr`·제너레이터·`m` · c16 내포식 셋·`**`·`sum` · c18 제너레이터·`any` | 분기 b2·b4×2 · 병렬 b2 · 필드 b4×2 · 반환 b5 / 1 · 추정 비용·지연 b6 / 2 · 측정 b6 · 캐시 b7 · 경로 / 2 · trace b1·b4·b5×3·b6 / 2 | 4 — `any ToolMessage`(**모델 답**) · `trace == ['model', 'model']`(**모델 답**) · 비용 < 1(**잰 값**) · 인사 흐름에 ToolMessage 없음(**모델 답**) + 준비·함수 안 3 |
| 02 | 같은 도구 · 코드로 만든 `AIMessage(tool_calls=[{… 'topic': '주차', 'id': 'call_bad_1'}])` 하나를 `MessagesState` 그래프(START → tools → END) 둘에 넣음 · Before `ToolNode(TOOLS, handle_tool_errors=False)` → `ValueError: 지원하지 않는 주제: 주차`(받아 출력) · After `handle_tool_errors=handle_policy_error`(`error: ValueError` 힌트) → ToolMessage `tool_call_id: call_bad_1`·안내 글 · 이어서 모델이 Human·AI·Tool 세 메시지를 읽고 답 | **1** | 요금 · `'주차'`·`'call_bad_1'` · 질문 | c6 위와 같음 · c12 f-string 안 계산·`try` 안 변수를 밖에서 씀 · c14 f-string·힌트·정의+실행 한 셀 | 반환 b4·b5 · 전파 b2·b4·b5 / 3 · 추정 비용·지연 b6 / 1 · 측정 b6 · 경로 b7 · 로그 b7 · docstring·Pydantic·스키마 b3 · 택배 송장 b4 | 3 — `startswith('ValueError:')`·`tool_call_id == 'call_bad_1'`(결정적) · `reply.text and 비용 < 1`(**모델 답**·잰 값) |
| 03 | 모델 없는 그래프 · `LoopState` · Before `tick → tick` 순환을 `{'recursion_limit': 4}`로 → `GraphRecursionError`(받아 출력, 첫 줄 `Recursion limit of 4 reached without hitting a stop condition. …`) · After 조건 함수 `stop_or_continue`(count ≥ 3이면 `END`) → `count: 3`·`trace ['tick:1', 'tick:2', 'tick:3']`·구조 문자열 | **0** | 한도 4 · 기준 3 | c6 클래스·힌트·f-string·정의+그래프 · c8 `try` 밖 변수 · c10 **조건 표현식**·`Literal` 반환 힌트·`'__end__'` | 분기 b8×2 · 경로 b2·b5·b7·b8 / 1 · 반환 b5×3·b6·b7 / 2 · 프롬프트·지연 b2 · 지연 b8 · 최대 b1·b5·b8·b9 / 1 · trace b5·b6·b9 · super-step ×7 / 1 · 비상 차단기 b4×2 | 3 — 오류 이름 · `count == 3` · 흔적 3개(모두 결정적) |
| 04 | 질문 셋 · 키워드 규칙 `fixed_topic`(연체 → 운영/시간 → 나머지 대출) · `CompareState.strategy`로 한 그래프에서 `choose` 노드가 fixed면 코드로 `AIMessage(tool_calls=[… 'id': 'fixed_call'])`, agent면 `bind_tools` 모델 · `add_conditional_edges('choose', tools_condition, {'tools': 'mark_tools', '__end__': '__end__'})` → 흔적용 `mark_tools` → `ToolNode` → `answer`(도구 없는 모델) · 질문 글 끝에 「반드시 제공된 규정 조회 도구로 확인한 뒤 한 문장으로 답하세요.」 · 3질문 × 2방법 × 2번 = 12실행 · 호출·그래프 전체 `perf_counter` · 방법별 평균 입력·출력 토큰·걸린 초·비용 합·답 글 종류 수 | **18**(fixed 6 = 답 1 × 6 · agent 12 = 고르기 1 + 답 1 × 6) | 질문 셋 · 키워드 셋 · 반복 2 · 요금 | c6 · c10 힌트 `tuple[AIMessage, float]`·`Any` · c14 클래스 `Literal` · c16 `**`·함수 9줄 · c18 함수 둘·`**` · c20 `'__end__'` · c22 **본문 13줄**·f-string·제너레이터 넷·`any`·`sum`·`m` · c24 제너레이터·`r` · c26 16줄·딕셔너리 내포식 둘·집합 내포식·제너레이터 넷·`defaultdict`·`mean`·한 글자 여섯 | **제목 「분기」** · 분기 b1×2·b2·b3×2·b5×3·b9×2 / 3 · 경로 b1~b9 23곳 / 13 · 추정 비용 b1·b6 / 2 · 지연 b1·b4·b5·b6×2·b8·b9 / 5 · 측정 b3·b5×2 / 3 · 측정표 b3 · 병렬 b3 · 사전·반환·바인딩·벽시계 b5 · 집합 b5 / 2 · 프롬프트 b6 / 2 · trace b1·b4·b6·b8 / 1 · 변동 ×6 / 3 | 2 — 실행마다 `any ToolMessage`(agent는 **모델 답**) · 비용 합 < 1(**잰 값**) + 준비·함수 안 3 |

- **모델 요청 합계(노트북 한 번씩, 교재 출력 기준) 3 + 1 + 0 + 18 = 22번**, 모두 `gpt-5.4-mini`(`init_chat_model`), 임베딩 0. 출력한 「추정 비용」 01 `0.000503`(대출 두 요청만, 인사 요청은 안 셈) · 02 `0.00049125` · 04 `0.003314` ≈ **0.0043달러**(캐시 입력 할인 없는 요금표 어림, 청구 금액 아님). 과정 말은 **「예상 비용」(Ch 6 06 `estimate_cost` = 사용량 × 요금표, 캐시 입력 0.075 칸 포함)**이고 「추정 비용」은 Ch 18 금지어.
- **`temperature=0` 0곳, `reasoning_effort="none"` 셋 모두(01·02·04)**. 모델 이름은 `f'openai:{MODEL_NAME}'`(과정 관례는 `"openai:gpt-5.4-mini"` 글자 그대로 + `nbkit.key_and_model_cells()`).
- **걸린 시간을 01·02·04 모두 잽니다**(`perf_counter`) — 01 `latency_sec: 1.963`(대출 흐름) · 02 `1.356`(답 요청) · 04 요청마다 + 그래프 전체, 평균 `1.077`·`1.462`. `_src` b6가 이 값을 결론 문장에 씁니다(01·02는 주제가 아닌 절).
- **`%pip` 셀**: 01·02·04 `%pip install -q langgraph==1.2.11 langchain==1.4.0 langchain-openai==1.6.0 python-dotenv==1.2.3` · 03 `langgraph==1.2.11`만. 실습 폴더 dev에 `pip==26.2`·잠금에 `pip 26.2` 있음(규격 §7-2 조건 충족).
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나. 노트북 토큰은 01·04 `{{notebook:slug}}`, 02·03 `{{notebook:slug|example}}`+`|failure}}`(`chapter.json` 형식과 같음). Mermaid·삽화 0장. 옛 그림 `01-흐름`은 조건 함수 `tools_condition`을 노드와 같은 상자로 그림(규격 §5-3 Ch 13 03-1 규칙과 어긋남), `02-흐름`은 SPEC이 `None`(생성기 안에서 따로 그림).
- 노트북 `metadata.verification`: 넷 모두 `passed`, 실행일 **2026-09-10**(01 06:13 · 02 06:13 · 03 05:47 · 04 06:13 UTC). `code_sha256` 앞 12자 01 `68c4bf20e983` · 02 `8c8f4a55f657` · 03 `50ae424d8b20` · 04 `fbc24b0065ed`. 노트북 파일 해시 `f7001dac…`·`821d3ac8…`·`463f121b…`·`1bc14de6…`(`part5-practice.zip` 안 판과 같음. `textbook/part6/qa/existing-artifact-hashes.json` 136~139행의 옛 값 `7d3ff8a7…` 등은 이미 다름 — 기록 파일).
- 노트북 설명 셀: 제목 + 질문 한 줄 · 「실행 환경 준비」 · 「패키지와 환경 준비」 · 「코드를 읽기 전에」(`_src` b4 뒤 단락과 같은 글, `revision: 2026-09-14-first-use-depth`) · 소제목 한 줄씩 · 「다른 상황에 적용하기」. **결과 읽기 셀 0.** 「이 노트북에서 할 일」·준비물(호출 수·비용)·실행일 문장 없음.
- `_src` 틀: b10 참고 자료 여섯이 네 절 모두 같음(확인일 2026-09-10) · 복습 문제 01~03 넷, 04 다섯 · b7 요금 「2026-09-10 공개 단가」(과정 요금표는 2026-09-17, 값은 같음).

## 2. 절별로 더 봐야 할 것

### 01 ToolNode와 tools_condition (experiment)
- **핵심 관찰 셋이 모델 답에 걸려 있습니다**: 대출 질문에서 도구를 부르는가, 한 번만 부르는가(`trace == ['model', 'model']`), 인사 질문에서 부르지 않는가. 셋 모두 `assert`로 걸려 모델이 다르게 답하면 셀이 멈춥니다 → 규격 §3 「`assert`는 매번 같아야 하는 값에만」과 부딪힘. 먼저 노트북 밖 다섯 번(규격 §2-7 10번 끝).
- **실행 흔적 칸이 모델 노드만 적습니다.** `ToolNode`는 `trace` 칸을 쓰지 않아 흔적은 `['model', 'model']`이고, 도구 실행은 ToolMessage로만 보입니다(b5 「확인할 점」이 그렇게 풂). Ch 13 02 약속(「규칙을 적은 칸에는 노드가 자기 몫만」)과 달리 `trace` 칸에 규칙이 없고 노드가 `state['trace'] + ['model']`로 앞 흔적을 이어 붙입니다(Ch 13 01절 판 모양 — 02절이 「하지 말라」고 가르침). 04는 흔적용 빈 노드 `mark_tools`를 따로 끼워 넣었습니다.
- **Ch 19 05 `ask_until_answer`(바퀴 한도 `turn_limit`, 평범한 함수)와 같은 일을 그래프로 옮긴 절**입니다. 지금 본문에는 이 대응이 없습니다(b2는 「`tool_calls`를 해석해 도구 함수를 호출」까지만). 대응표(모델 요청 = `model` 노드, `run_tool_calls` = `ToolNode`, 「도구 호출 요청이 없으면 멈춤」 = `tools_condition` → 끝, `messages.append` = `add_messages`)를 둘지 결정.
- 비용 함수 `usage_of`는 캐시 입력 칸이 없는 이 챕터만의 판입니다(Ch 6 06 `estimate_cost`와 다름). 인사 요청의 비용은 세지 않습니다(b6 「두 모델 호출」).
- b3 「Ch13에서 StateGraph, **MessagesState**와 add_messages 리듀서, 조건부 엣지를 배웠습니다」 — **Ch 13은 `MessagesState`를 쓰지 않았습니다**(Ch 13 `_src`·노트북 grep 0). 04절 `ChatState`에 `add_messages`를 적는 모양을 배웠습니다. b3 「구성 요소」·「자율성의 비용」(계약 §3 — Ch 17 말은 루프 네 가지·자율성의 대가) · b2 「단계·분기·병렬 실행」(Ch 18 말은 단계 잇기·갈래·함께 보내기).
- b4 비유 「도서관 상담 직원이 … 규정 담당자에게 조회를 요청」은 도구 설명 「교육센터 자료실 규정」과 장소 이름이 어긋납니다.
- 모델 셀이 가져오는 `Any`는 쓰지 않습니다(01·02). `graph.get_graph().draw_mermaid()` 출력은 Ch 13 01이 가르친 구조 문자열입니다.

### 02 도구 오류와 ToolMessage (paired)
- **Before·After 모두 모델 없이 결정적**입니다(코드로 만든 도구 호출 요청 `call_bad_1`). 모델 요청은 After 끝의 답 한 번뿐이고, 그 답 글에는 `assert reply.text`만 걸림. 모델이 이런 잘못된 요청을 만드는지는 재지 않는다고 b6가 밝힘 — 태도는 맞음.
- **Before 설정 `handle_tool_errors=False`는 기본값이 아닙니다.** 설치판 기본값은 `_default_handle_tool_errors`이고, 이 함수는 **인자 검사 오류(`ToolInvocationError`)만 도구 메시지로 바꾸고 `ValueError`는 그대로 올립니다**(§5-2). 그래서 이 절의 `ValueError` 장면은 기본값에서도 같게 멈춥니다. 반대로 **기본값은 Ch 19가 「흐름 안에서는 받지 못해 멈춘다」고 한 입력 검사 오류를 도구 메시지(`status: error`)로 바꿉니다** — Ch 19 인계 6번(「흐름 안 입력 검사 오류 장면 없음」)을 이 절에서 모델 없이 결정적으로 보일 수 있는 자리입니다(선택).
- **오류 처리 함수의 매개변수 힌트 `error: ValueError`가 동작을 바꿉니다.** `ToolNode`는 처리 함수의 첫 매개변수 표시를 읽어 받을 오류 종류를 정합니다(설치판 `tool_node.py` 444~500·993~996행). 표시를 빼면 모든 오류(인자 검사 오류 포함)를 받습니다(§5-2 모델 없는 확인). 이 힌트는 장식이 아니라 **라이브러리가 읽는 값**입니다(§7-1).
- `MessagesState`는 과정 처음(Ch 13은 직접 적은 상태 형식만). 01과 같은 상태 형식을 다시 쓰면 새 이름이 줄어듭니다.
- Ch 19 인계(§4-1 1~3번)가 모두 이 절에 몰려 있습니다: 학습 목표 b1 「tool_call_id가 요청과 결과를 연결하는 방식」(Ch 19 05가 가르친 「호출 ID」) · b4 둘째 비유 「택배 송장 번호」(Ch 19 「같은 색 집게」) · b2·b4 「오류를 도구 메시지로」를 처음처럼 씀(Ch 19 06 도구 속성 `handle_tool_error`(단수, `ToolException`만)와 가르는 문장 없음) · b7 「`handle_tool_errors=True`처럼 모든 예외를 같은 방식으로」.
- b7 「쓰기 도구가 … Ch24의 내구 실행에서 멱등성을 다시 다룹니다」 — 내구 실행은 **Ch 23 04**(`04-내구-실행-모드-비교`), 멱등성은 **Ch 23 06**(`06-노드-재시작과-멱등성`)입니다. Ch 24 01은 「Ch23에서 … 외부 쓰기에는 멱등성이 필요하다는 점을 확인」이라고 적음.
- b3 「스키마를 통과한 문자열이더라도 로컬 자료에 없는 주제라면 ValueError」 — 도구는 `topic: str`뿐이라 Ch 19 02의 `Literal` 양식이 없습니다. 「주차」가 입력 검사를 통과하는 까닭(고를 수 있는 값을 정하지 않음)을 한 문장으로 잇거나, `Literal`을 쓰면 오류 종류가 인자 검사 오류로 바뀐다는 점을 알고 정할 것.
- `try` 블록 안에서 만든 `before_error`를 블록 밖 `assert`가 씀 — 예외가 안 나면 `NameError`(Ch 19 01 Before 모양과 견줘 정리).

### 03 recursion_limit과 명시적 종료 (paired)
- **모델 없이 결정적**입니다(이번 설치판에서 같은 그래프를 모델 없이 돌려 확인 — §5-3). `recursion_limit=4`는 **After가 통과하는 가장 작은 값**입니다(노드 실행 세 번 뒤 끝나는 흐름은 한도 4부터 통과, 3이면 세 번 실행 뒤 오류). Before는 한도 N이면 `tick`이 N번 실행된 뒤 오류.
- **`check_bundle_execution.py` 계약**: Part 5 묶음 검사가 **Ch 20 03을 키 없이 새 커널로 실행**합니다(29~42행, Ch 17 05·Ch 19 01과 함께, `uv sync --locked` 뒤 `notebooks/`에서, 실행 뒤 `code_sha256` 비교). **03에 모델 요청을 넣으면 이 검사가 멈춥니다.** 도구 파일을 가져오면 그 파일이 잠금 밖 패키지를 import하지 않아야 합니다. `%pip` 줄은 이미 있음(잠금에 pip).
- 설명: 「super-step」·「비상 차단기」·「실행 한도」·「명시적 종료」가 새 말. **Ch 17 03 「바퀴 한도」·Ch 19 05 `turn_limit`(바퀴 한 번 = 모델 요청 한 번)와 다른 것**이라는 문장이 없습니다(Ch 19 인계 5번). 대응: 01 대출 흐름은 모델 요청 2번(바퀴 2) = 노드 실행 3번(model·tools·model) → 한도 4부터 통과(모델 없는 흐름 모양으로 확인한 규칙 — 모델 흐름에서는 이번에 실행하지 않음).
- **설치판 기본 한도는 10007**입니다(`langgraph/_internal/_config.py` 32행, 환경 변수 `LANGGRAPH_DEFAULT_RECURSION_LIMIT`로 바뀜). 공식 Graph API 문서는 「1.0.6부터 기본 1000」이라 적어 **문서와 설치판이 다릅니다**. 본문에 기본값을 쓰려면 설치판 소스 근거로(규격 §3).
- b3 「Ch17에서 정지 조건 없는 자율성은 비용과 예측 불가능성을 **키운다**고 배웠습니다」 — 계약 §3 「→ 커질 수 있다」. b2 「잘못된 프롬프트」·「비용과 지연」. b7 「`configurable` 안에 넣지 않고 최상위 키」는 공식 문서와 맞음(`graph-api` 「standalone config key」).
- After 조건 함수가 조건 표현식 + `Literal['tick', '__end__']` 반환 힌트. Ch 13 03 모양은 여러 줄 `if` + 이름표 표(`path_map`)이고 끝은 `END` 상수. 반환 힌트를 빼도 동작은 같습니다(§5-3 확인에서 힌트 없는 조건 함수 사용). 구조 문자열의 갈래 표시는 `path_map`으로 적을 수 있음.
- paired Before는 **실제 결함**(끝 엣지가 빠진 순환)이라 빨강 규칙에 맞습니다.

### 04 if 분기와 모델 선택 비교 (experiment)
- **핵심 비교가 잰 시간에 기대 있습니다.** 제목·`objectives`·b1·b6·b8·복습이 「토큰·비용·지연·출력 변동」을 약속하고 b6가 평균 걸린 초 `1.077`·`1.462`를 결론 단락에 씁니다. 규격 §3 「재지 않은 것은 쓰지 않는다」와는 맞지만(재기는 함), §2-7 9번 끝(두 번 다른 값은 결론 금지)과 부딪힙니다 — 걸린 초·출력 토큰·답 글 종류 수는 실행마다 흔들립니다. 선례: Ch 15 05·06(주제 절 예외), **Ch 17 04(걸린 시간·토큰을 잰 예외, 결론은 요청 수·입력 토큰만)**, Ch 18 03(걸린 초 비교는 결론·그림·정리에서 뺌). §7-4 선택지.
- **코드로 세는 결정적 값이 이미 있습니다**: 실행당 모델 요청 수(fixed 1 · agent 2) → 12실행 합 6 ↔ 12, 흔적 모양 `['fixed_choose', 'tools', 'model_answer']` ↔ `['model_choose', 'tools', 'model_answer']`, agent 고르기 요청의 입력 토큰(같은 질문 + 도구 명세라 흔들리지 않을 가능성이 큼 — 확인 필요). 모델이 고른 `topic`이 `fixed_topic`과 같은지 세는 칸은 없습니다(추가하면 「같은 주제를 고른 수 3/3」 같은 셈 가능 — 모델 답에 기댐).
- **질문 글이 도구 사용을 강제합니다**(「반드시 제공된 규정 조회 도구로 확인한 뒤」). 그래서 agent 흐름에서 「도구를 부르지 않는 선택」은 나오지 않고, `tools_condition`의 끝 갈래(`'__end__'`)는 실행되지 않습니다. 모델이 따르지 않으면 `run_branch`의 `assert`가 멈춥니다. 모델 선택이 이기는 장면(키워드 규칙이 놓치는 질문 — 예: 「연체」 낱말 없이 늦게 반납하는 질문은 규칙이 `대출`로 보냄)은 없습니다. 값 바꿔 보기 후보(규칙 쪽 잘못은 코드로 정해지는 값, 모델 쪽은 「이번 실행에서는」).
- 「고정 if 분기」는 그래프의 조건부 엣지가 아니라 `choose` 노드 **안의 `if`**입니다. Ch 13 03(코드가 점수로 갈래를 고르는 조건부 엣지)과 이어 쓸지, 노드 안 `if`로 둘지 결정. `strategy` 칸 하나로 한 그래프를 두 방법에 쓰는 설계(b8 「같은 컴파일 그래프」).
- `run_branch`가 한 함수에서 실행·검사·합계·기록을 모두 함(본문 13줄) · 집계 셀 16줄·내포식 셋·`defaultdict`·`mean`. 출력 `output_variants_by_question`(두 번 실행한 답 글의 서로 다른 종류 수, `2·1·2`)은 흔들리는 값.
- `_src` b3 「Ch18에서는 … 단계·분기·병렬 실행」·「Ch20에서 처음 조립한」(자기 챕터를 3인칭) · b5 「사전으로 반환」·「벽시계 시간」·「바인딩」 · b7 「예상 API 비용은 절 전체 1달러 미만」(04만 「예상」).
- **앞 챕터 약속**: Ch 17 01·02 b7 「Ch 20 04절은 코드의 if로 고르는 흐름과 모델이 고르는 흐름을 견줍니다」 · **Ch 17 05 보호 자료** `autonomy-diagnostic-example.json` 12행 `"next_measurement": "Ch 20에서 고정 분기와 모델 분기의 호출 수·비용·결과 편차 비교"`(Ch 17 05 노트북 출력·HTML에도 찍힘, 고치지 않는 자료). **걸린 시간은 약속에 없고 「호출 수·비용·결과 편차」는 있습니다.**

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part5/ch20-tool-node/
  README.md (3줄 — 「로컬 읽기 전용 규정 자료」·「예상 비용이 절당 1달러 미만인지 검사」)
  pyproject.toml   uv.lock (88항목)
  notebooks/01~04-*.ipynb
  .ruff_cache/ · .venv/ (macOS 판 175MB — home = /Users/…/cpython-3.12-macos-aarch64-none, uv 0.11.6)
  (없음: data/ · runs/ · tests/ · 모듈 · 도구 파일 · 노트북 생성기)
```

- **자료**: `data/`가 없습니다. 네 노트북이 모두 **노트북 안 딕셔너리 `POLICIES`**(대출·운영·연체 규정 글 셋)를 다시 적어 씁니다(01·02·04 같은 셀, 03은 자료 없음). 파일 읽기는 준비 셀의 `.env` 찾기(`[Path.cwd(), *Path.cwd().parents]`에서 위로)뿐, 파일 쓰기 0건. **Ch 19 `data/orders.csv`·`order_tools.py`는 읽지 않습니다.**
- **Ch 20 파일을 코드로 읽는 곳**(`grep -rn`, `textbook`·`labs`·`qa`):

| 읽는 곳 | 무엇을 | 계약 |
|---|---|---|
| **`textbook/part5/qa/check_bundle_execution.py`** 29~42행 | `part5-practice.zip`을 풀어 **Ch 20 03 노트북을 키 없이 새 커널로 실행**, 실행 뒤 `code_sha256`이 같은지 봄 | **03은 모델 없이 돌아야 합니다.** 마지막 기록 `bundle-execution.json`(zip `72d3e3e7…`, 03 PASS) |
| `textbook/part5/_build_index.py` 25행 | (3, 5, 설명 「ToolNode와 조건부 엣지로 루프를 조립하고 고정 **분기**와 모델 선택을 비교합니다.」) · 묶음에 실습 폴더 파일(노트북 넷·`README.md`·`pyproject.toml`·`uv.lock` — zip 안 판이 디스크와 같음) | 설명 한 줄 금지어 · 도구 파일을 만들면 `textbook/part5/public-files.json`(지금 Ch 20 줄 0)·챕터 `qa/public-files.json`(`include`에 `*.py` 없음)에 더해야 묶음에 들어감 |
| `textbook/_notebook/build_index.py` 44행 · `build_bundle.py` 22행 | (`'ToolNode'`, 절 수 **4**, 「… 고정 분기와 비교합니다.」) | 실습 절을 더하면 4 ≠ 5(Ch 17·18·19 선례: 고치지 않고 전체 마감 몫) |
| `textbook/_notebook/verify.py` 105~124행 | import 금지 모듈 `openai`·`rag`·`context_lab`·`document_processing`·`experiment`·`harness`·`prompts` | 도구 파일 이름 |
| `textbook/part6/qa/shared-tests.json` | 기록: 공용 테스트를 `uv run --project labs/part5/ch20-tool-node --with pytest --with pillow …`로 돌렸음(읽는 스크립트 없음) | Ch 20 잠금을 공용 테스트 환경으로 쓴 기록 — 패키지를 빼면 같은 명령이 달라질 수 있음 |
| 옛 검사 넷(고치지 않음, 기록만) | `check_scope.py`(`EXPECTED` ch20 (3, 5) · `SECTION_COUNTS` ch20 = **4**) · `check_notebook_readiness.py`(**함수 타입힌트 필수**·노트북마다 `assert`·`len(reports) == 21`) · `check_figures.py`(SVG마다 `.excalidraw` 짝) · `finalize_evidence.py`(`language/ch20-final.json`의 `source_sha256`·`built_sha256` 해시 고정 — Ch 20 `_src`·그림·HTML을 바꾸면 무조건 어긋남) | Ch 19 마감 기록대로 넷 모두 Ch 19·20에 닿기 전(Ch 17·18 자리)에 멈춤. `check_notebook_readiness.py`는 멈추기 전에 결과 파일을 다시 써서 되돌려야 함(Ch 18·19 선례) |
| 기록만 | `textbook/part5/qa/ch20-technical-review.md`·`ch20-visual-summary.json`·`ch20-lint-findings.json`·`ch20-overflow.png`·`language/ch20-original/`·`final-manifest.json` · `textbook/part6/qa/existing-artifact-hashes.json` 136~139·433~441행 · `textbook/part7/qa/existing-artifacts-before.json` 248~251·269~272행 · `textbook/_notebook/checks/notebook-contracts-part5-ch20-tool-node.json`(verify가 다시 씀) | — |

- **Part 6 선행 목록(`textbook/part6/prerequisite-files.json`·Ch 28 목록)과 `textbook/part6/qa/final-artifact-hashes.json`에 Ch 20 파일은 없습니다**(grep 0). Part 6·7 노트북·스크립트가 Ch 20 파일을 코드로 읽는 곳도 0입니다. → **산출 파일 계약 없음, 묶음 계약은 Part 5 묶음(파일 일곱)과 03 실행 하나.**
- **옛 생성기**(부르는 스크립트 0 — 챕터 `qa/public-files.json`이 `qa/author_ch20.py`를 묶음에서 뺌):

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| `textbook/part5/ch20-tool-node/qa/author_ch20.py`(53KB, 626줄) | 노트북 넷(출력 없이) · `_src` 넷 · `figures/NN-흐름.{svg,excalidraw,caption.md}` · **`chapter.json`** · **`labs/…/pyproject.toml`(dev 그룹 없는 판으로 덮어씀)** · `README.md` · `집필점검표.md` | 실행하면 개선본과 잠금 설정을 옛 판으로 덮어씀. 이 파일 안 노트북 글은 지금 노트북과도 다름(「코드를 읽기 전에」 블록 없음, `usage_of(message)` 힌트 없음) |
| `textbook/part5/ch20-tool-node/figures/_gen_figures.py` | `NN-흐름.{svg,excalidraw,caption.md}`(`textbook/part5/_figure.py`) | 옛 그림 |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part5_enrich.py`·`part5_review_repairs.py` | 「코드를 읽기 전에」·「다른 상황에 적용하기」 블록을 끼워 넣은 옛 도구(ch20 이름이 들어 있음) | 기록만(Ch 16~19 선례대로 막지 않음) |

→ 규격 §8 1번: **01절 작업 때 앞의 둘 첫머리에 설명 주석 + `raise SystemExit(...)`**, 마감 때 `mv -n` → `qa/upgrade/before/generators/blocked/`(사본은 이미 `before/generators/`).

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `langchain-core 1.6.2`·`langgraph-prebuilt 1.1.0`·`langgraph-checkpoint 4.2.0`·`openai 3.11.0`·`pydantic 2.13.5`·`langsmith 0.12.4`·`tiktoken 0.14.0`·`httpx 0.28.1`. **`pandas`·`numpy`·`pytest` 없음.**
- **Ch 19 잠금과 견줌**: `langchain`·`langchain-core`·`langchain-openai 1.6.0`·`langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`·`openai 3.11.0`·`pip`·`ipykernel`·`nbclient` **같음**. 다른 것: **`pydantic` Ch 19 2.12.5(고정) ↔ Ch 20 2.13.5**(`pydantic-core` 2.41.5 ↔ 2.46.5), Ch 19에만 `pandas 3.0.5`·`numpy 2.5.3`·`pytest`·`tzdata`. Ch 13·17은 `langchain-openai 1.6.1`(과정 요약 「강사 확인」 그대로).

## 4. 앞뒤 챕터 이음새

### 4-1. Ch 19 인계(요약 §13 「Ch 20이 전제하면 안 되는 것」) 항목별 지금 상태

| # | Ch 19가 넘긴 것 | Ch 20 지금 자리 | 상태 |
|---|---|---|---|
| 1 | 호출 ID를 처음처럼 쓰지 않기, 비유 둘(「같은 색 집게」 ↔ 「택배 송장 번호」) | 02 `_src` 2행 b1 학습 목표 「ToolMessage의 tool_call_id가 요청과 결과를 연결하는 방식을 설명」 · 5행 b4 「택배 송장 번호가 발송 요청과 배송 결과를 연결하듯」 · 8행 b8 · 복습 1 | **그대로** — 「Ch 19 05절에서 본 호출 ID」로 잇고 비유를 하나로(비유 계열 결정 §8과 함께) |
| 2 | 도구 오류 → 도구 메시지를 처음처럼 쓰지 않기, 도구 속성 `handle_tool_error`(단수, `ToolException`만) ≠ `ToolNode(handle_tool_errors=…)`(복수) | 02 b2·b4·「코드를 읽기 전에」·b7 「`handle_tool_errors=True`처럼」 — Ch 19 06과 가르는 문장 0 | **그대로**. 이번 확인으로 더 정확한 사실이 생김(§5-2): ToolNode 기본값은 `ValueError`를 올리고 인자 검사 오류만 도구 메시지로 바꿈 → Ch 19 06 b4·b7 「`ValueError`는 설정을 켜도 올라온다」(도구 속성)와 **기본값 모양이 닮음**, `handle_tool_errors=True`면 모든 오류를 받음 |
| 3 | 01 b8 다음 절 예고에 Ch 19 06을 잇는 말 | 01 `_src` 9행 b8 「… 예외를 숨기지 않고 ToolMessage로 어떻게 전달할지」 | **그대로** |
| 4 | Ch 18 금지어 「추정 비용」·「지연」 → 예상 비용·걸린 초 | 01 b6(7행) · 02 b6(7행) · 03 b2·b8(「지연」) · 04 b1·b4·b5·b6·b8 + 노트북 md 01 2·02 1·04 7 · `chapter.json` objectives 셋째 줄 「지연」 | **그대로** + 01·02는 걸린 시간을 실제로 잼(주제 절 아님) |
| 5 | `recursion_limit` ≠ 바퀴 한도 `turn_limit` | 03 전체에 Ch 17 03·Ch 19 05 언급 0 | **그대로**. 대응 규칙을 모델 없이 확인(§5-3): 한도 N = 노드 실행 N번까지, 노드 실행 K번 뒤 끝나는 흐름은 한도 K+1부터 통과 |
| 6 | Ch 19가 하지 않은 것(`ToolNode`·그래프·`tools_condition`·`tool_choice`·시스템 메시지·서비스 오류·걸린 시간·`ToolMessage(…)` 직접 만들기·흐름 안 입력 검사 오류·한 응답의 요청 여럿을 한꺼번에 실행) | 02·04가 `AIMessage(tool_calls=[…])`를 코드로 만듦(Ch 13 04가 `AIMessage(content=…, id=…)` 직접 만들기는 가르침, `tool_calls` 칸 넷은 Ch 19 04) · 01·02·04 걸린 시간 잼 · 시스템 메시지·`tool_choice`·서비스 오류 0 · **ToolNode는 한 응답의 도구 호출 요청 여럿을 스레드 실행기로 한꺼번에 실행**(설치판 821~823행 `executor.map`) — 지금 네 절은 요청 하나씩이라 장면 없음 | 부분. 흐름 안 입력 검사 오류는 ToolNode 기본값이 도구 메시지로 바꿈(§5-2) — 02에서 보일 수 있는 자리 |
| 7 | `order_tools.py`는 Ch 19 폴더 전용 | Ch 20 폴더에 없음, Ch 20은 자기 자료 `POLICIES`·도구 `lookup_policy`를 다시 적음 | 맞음 — 가져올지는 §6 |
| 8 | 모델 답이 늘 같다고 쓰지 않기 | 01 `assert` 셋·04 `assert` 하나가 모델 답에 걸림 · 01 b8 「model 한 번 뒤에 종료될 수 있습니다」(한정 표현은 있음) | 부분 |
| 계약 | Ch 17 → Ch 20 몫: 01 b3 「구성 요소」·「자율성의 비용」 · 03 b3 「키운다」 · 04 「추정 비용」 / Ch 18 → Ch 20 몫: `_src` 01·04 「분기·병렬」 | 01 4행 b3 · 03 4행 b3 · 04 b1·b6 · 01 3행 b2·04 4행 b3 | **모두 그대로** |

- **Ch 19에서 이어받을 말**(요약 §13): 도구·도구 설명·입력 형식·도구 명세 · 입력 검사(Ch 16 01 뜻과 다름) · 도구 호출 요청 · 도구 메시지·호출 ID·여럿 담기·도구 찾기 표 · 읽기 도구·쓰기 도구·도구 오류·**오류 담기 설정(도구 속성, 단수)**·결과 상태(`status`) · 사람 확인 값 · 바퀴 한도 · 예상 비용. `ToolNode`가 내는 오류 도구 메시지의 `status`는 `error`(설치판 1006~1012행) → Ch 19 06 「결과 상태」로 바로 이어짐.
- **Ch 19 쪽 참 문장**(요약 §13): Ch 20 01 b2·b3 「`@tool`과 `bind_tools`로 … `tool_calls`를 해석해 도구 함수를 호출」·「`bind_tools`가 도구 스키마를 모델 요청에 포함」 · 02 b3 「지원 범위를 도구 docstring과 Pydantic 스키마에」 · 04 b3 「`tool_calls`를 해석」 — 참. 01 b7 「쓰기 도구에는 별도의 권한 확인」 ↔ Ch 19 06 「사람 확인 값」.

### 4-2. Ch 13 그래프 모양과 대조

| 자리 | Ch 13(완료) | Ch 20 지금 | 차이 |
|---|---|---|---|
| import | `from typing_extensions import TypedDict` · `from typing import Annotated` · `from langchain.messages import AnyMessage, HumanMessage, AIMessage` · `from langgraph.graph.message import add_messages` · `from langgraph.graph import StateGraph, START, END` | 같은 이름 + `MessagesState`(02) · `langgraph.prebuilt` `ToolNode`·`tools_condition` · `langgraph.errors` `GraphRecursionError` | 새 이름 넷 |
| 상태 형식 | `class ChatState(TypedDict)` — `messages: Annotated[list[AnyMessage], add_messages]` · **`trace: Annotated[list[str], operator.add]`**(02~08) · 칸이 바뀌면 새 이름 | 01 `AgentState`·04 `CompareState`의 메시지 칸은 **Ch 13 04와 같은 모양** · **`trace: list[str]`(규칙 없음)** · 04 `strategy: Literal[…]`·`measurements: list[dict]` · 02 라이브러리 `MessagesState` | 흔적 칸 규칙 없음·`Literal` 칸·`MessagesState` |
| 노드 함수 | 힌트 없음 `def normalize(state):` · 자기 몫만 `{"trace": ["normalize"]}` | `def call_model(state: AgentState) -> dict:` · `state['trace'] + ['model']`(Ch 13 01 판, 02가 하지 말라고 한 모양) | 힌트·흔적 이어 붙이기 |
| 조건부 엣지 | 조건 함수(여러 줄 `if`, 이름표를 내놓음) + **이름표 표 `path_map`**, 끝은 `END` 상수 · 조건 함수는 `add_node`로 등록하지 않음(그림에서도 노드 모양 금지) | 01 `add_conditional_edges('model', tools_condition)`(라이브러리 조건 함수, `path_map` 없음) · 03 조건 표현식 + `Literal['tick', '__end__']` 반환 힌트 · 04 `path_map` `{'tools': 'mark_tools', '__end__': '__end__'}`(`'__end__'` 글자) | `tools_condition` = **라이브러리가 준 조건 함수**(Ch 13 03 「조건 함수」 말로 풀 수 있음), `'__end__'` = `END`의 글자 값 |
| 루프 | **자기 자신·앞 노드로 되돌아가는 엣지는 Ch 13이 가르치지 않음**(요약 §14 「자기 자신으로 다시 가는 노드」 Ch 14 전제 금지) | 01 `tools → model` 되돌아가기 · 03 `tick → tick` 자기 자신 | **Ch 20이 처음 가르치는 모양** — 한 문장 필요 |
| 실행 | `graph.invoke(상태)` · 구조 문자열 `get_graph().draw_mermaid()` | 같음 + 설정 딕셔너리 `invoke(상태, {'recursion_limit': 4})`(03) | 두 번째 인자 처음 |
| 출력 함수 | `print_state(label, state)`·`print_messages(label, messages)`(Ch 13 04·08, 노트북 판) | `for index, message in enumerate(…)` + `getattr` 직접 | Ch 19 06 `show_messages(messages)`(종류·도구 호출 요청 이름·`status`·내용)가 같은 일을 함 |

- Ch 13 말 이어 쓰기: 상태·노드·엣지·상태 그래프·가상 시작점/끝점·컴파일·**실행 흔적**(= `trace` 칸 — 「trace」 대신)·조건부 엣지·조건 함수·이름표 표·메시지 리듀서·공통 형식 `AnyMessage`. **Ch 13 금지어 「분기」(→갈래)·「경로」·「반환」·「임계값」·「재정렬」·「병렬」.**

### 4-3. 앞 챕터가 Ch 20에 기대는 문장(확인한 것만, 모두 완료 챕터)

| 자리 | 지금 문장 | Ch 20 개선 때 |
|---|---|---|
| Ch 6 01 `_src` 44행 | 「Ch 20에서는 모델이 도구를 고르는 흐름을 만듭니다.」 | 참 |
| Ch 7 05 `_src` 45행(b4) | 「도구 실행과 종료를 그래프로 잇는 방법은 Ch 20 **01절**에서 다룹니다.」 | 01이 루프를 유지해야 참 |
| Ch 17 01·02 `_src` b7 | 「모델이 실제로 도구를 고르는 코드는 Ch 19와 Ch 20에서 만듭니다.」·「Ch 20 **04절**은 코드의 if로 고르는 흐름과 모델이 고르는 흐름을 견줍니다.」 | 04가 두 흐름 비교를 유지해야 참 |
| Ch 17 03 `_src` 21행 | 「그래프로 도구 루프를 만드는 ToolNode는 Ch 20 01절에서 다룹니다.」 | 참 |
| **Ch 17 05 보호 자료** `data/autonomy-diagnostic-example.json` 12행 · 05 노트북 출력 · 05 HTML 591·601행 | `next_measurement` 「Ch 20에서 고정 분기와 모델 분기의 **호출 수·비용·결과 편차** 비교」 · 「칸 `next_measurement`가 가리키는 Ch 20 04절은 …」 | 04가 호출 수(요청 수)·비용·결과 편차(답 글 종류)를 유지하면 참. **자료 글의 「분기」는 고치지 않는 보호 파일** |
| Ch 19 05 `_src` 8행 b2 | 「Ch 20에서는 ToolNode가 이 실행을 맡습니다.」 | 참 |
| **Ch 19 06 `_src` 8행 b2 + 링크** | 「Ch 20 02절에서는 ToolNode가 도구를 실행하며 도구 오류를 다룹니다.」 · 링크 `../ch20-tool-node/02-도구-오류와-ToolMessage.html`(생성기 `author_06.py` 613행 `L_CH20_02`) | **02 슬러그를 바꾸면 완료 챕터 링크가 깨짐** |
| Ch 19 07 `_src` 60행 b8 | 「Ch 20에서는 도구를 실행하고 다시 묻는 반복을, Ch 13의 상태 그래프로 조립합니다.」 | 참 |
| Part 5 소개 `_src/index.html` 2·7·8행 · `practice-start.md` 15행 · `labs/part5/continuity-guide.md` 9행 | 「Ch 13의 상태·노드·조건부 엣지는 Ch 20의 모델과 도구를 연결하는 루프로」·「모델이 요청한 도구의 실행 결과를 다시 모델에 전달하는 루프를 StateGraph와 ToolNode로」 · continuity-guide 「노트북의 실행 환경과 **예제 데이터는 각 절에서 다시 준비**합니다」 | 도구 파일을 만들면 continuity-guide 문장이 틀어짐(Ch 19 마감처럼 한 줄 고침 또는 Part 5 마감 몫) |
| Ch 13 · Ch 18 | Ch 20 언급 0 | — |

### 4-4. 뒤 챕터가 Ch 20에 기대는 문장(모두 대기 챕터 — 고치지 않음)

| 자리 | 지금 문장 | 판정 기준 |
|---|---|---|
| Ch 21 01 `_src` 3행 b2 | 「Ch20에서는 model 노드, tools_condition, ToolNode, tools→model 엣지를 직접 연결했습니다」 | 01 구조를 유지하면 참 |
| Ch 21 01 4행 b3 · 04 4행 b3 | 「Ch20에서 직접 연결한 StateGraph와 ToolNode를 사용합니다」·「Ch20의 직접 조립 그래프를 사용합니다」 | 참(Ch 21 노트북은 Ch 20 파일을 읽지 않음 — 자기 도구를 다시 적음) |
| **Ch 21 01·05 노트북** | `@tool lookup_policy(topic: str)`「자료실 규정을 조회합니다. topic은 대출 또는 운영입니다.」 · 05 `search_rules`도 자료실 규정 | **Ch 20과 같은 자료실 규정 소재를 이어 씀** — Ch 20이 소재를 Ch 19 주문으로 바꾸면 Ch 21과 이어지는 소재가 끊김(§6 판단 근거) |
| Ch 23 01 `_src` 4행 b3 | 「Ch20의 도구 반복도 같은 실행 안에서 메시지를 누적했습니다」 | 참 |
| Ch 26 01~04 `_src` 4행 b3 | 「Ch20에서 ToolNode와 명시적 END 조건을 … 배웠습니다」 | 03 「명시적 종료」를 유지하면 참 |
| Part 6 소개 `_src/index.html` 7행 · `labs/part6/continuity-guide.md` 7행 | 「Ch 20의 StateGraph·ToolNode 루프를 Ch 21의 create_agent와 비교」·「Ch20의 모델·ToolNode 그래프 → Ch21」 | 참 |
| Ch 22 01 `_src`(완료) | Ch 20 언급 0(옛 판 문장 「Ch20에서는 모델 노드와 ToolNode를 직접 연결했고」는 Ch 22 개선으로 없어짐 — `gates-before.json`·`language/originals/`에만 남음) | — |
| Ch 20 02 b7 → Ch 24 | 「Ch24의 내구 실행에서 멱등성을 다시 다룹니다」 | **틀림** — Ch 23 04·06(§2 02) |
| Ch 21 `_author_ch21_ch29.py`·Ch 25·26 `_generate_ch25_ch26.py` | 위 문장의 생성기(옛 판) | 기록만 |

## 5. 라이브러리 동작 — 설치판 소스와 모델 없는 확인 (2026-09-24)

설치판: `langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`(`langgraph/prebuilt/tool_node.py` 2030줄)·`langchain-core 1.6.2`. 확인 스크립트 `/tmp/ch20-prep/offline_check.py`·`offline_check2.py`(기기 `/tmp`, 모델 객체를 만들지 않음, 키 뺌). **노트북 셀이 아니라 준비 조사용 확인이며, 모델이 낀 흐름에서는 실행하지 않았습니다.**

### 5-1. `tools_condition`
- 마지막 메시지에 `tool_calls`가 하나 이상 있으면 `"tools"`, 없으면 `"__end__"`를 내놓는 **평범한 함수**(1582~1660행, 반환 힌트 `Literal["tools", "__end__"]`). 노드가 아니라 조건 함수입니다 — 그림에서 노드 모양·색으로 그리지 않음(규격 §5-3). 확인: 요청 없는 `AIMessage` → `__end__`, 요청 있는 것 → `tools`.
- 이름이 `tools`인 노드로 가므로 `ToolNode`를 `'tools'`로 등록하거나 `path_map`으로 이름을 잇습니다(04가 `{'tools': 'mark_tools', …}`로 이음).

### 5-2. `ToolNode(handle_tool_errors=…)` — 설정별 결과(같은 도구·같은 네 요청)

도구는 01~04와 같은 모양(`topic: str`, 없는 주제면 `ValueError`). 요청 넷: 없는 주제 `'주차'`(ValueError) · `topic` 자리에 정수 3(인자 검사 오류) · 인자 없음(인자 검사 오류) · 등록 안 된 도구 이름.

| 설정 | `ValueError` | 인자 검사 오류(자료형·빠진 인자) | 없는 도구 이름 |
|---|---|---|---|
| **기본값**(`_default_handle_tool_errors`, 753행) | **그대로 올라옴** | 도구 메시지 `status: error` 「Error invoking tool 'lookup_policy' with kwargs … Please fix the error and try again.」 | 도구 메시지 `error` 「Error: no_such_tool is not a valid tool, try one of [lookup_policy].」 |
| `False` | 올라옴 | **`ToolInvocationError`로 올라옴** | 도구 메시지(설정과 무관) |
| `True` | 도구 메시지 「Error: ValueError('지원하지 않는 주제: 주차')\n Please fix your mistakes.」(111행 틀, 영어) | 도구 메시지(같은 틀) | 도구 메시지 |
| 처리 함수 `def h(error: ValueError) -> str` | 도구 메시지(함수가 쓴 글) | **올라옴**(`ToolInvocationError`는 `ValueError`가 아님) | 도구 메시지 |
| 처리 함수 **힌트 없음** `def h(error)` | 도구 메시지(함수 글) | **도구 메시지(함수 글)** — 모든 오류를 받음 | 도구 메시지 |
| 튜플 `(ValueError,)` | 도구 메시지(영어 틀, 글을 못 바꿈) | 올라옴 | 도구 메시지 |

- **처리 함수의 첫 매개변수 표시가 받을 오류 종류를 정합니다**(`_infer_handled_types`, 444~500행 — `get_type_hints`로 읽고, 표시가 없으면 `(Exception,)`). `Union[ValueError, TypeError]`도 받음.
- 받은 오류로 만든 도구 메시지는 `status="error"`·`tool_call_id=call["id"]`·`name=call["name"]`(1006~1012행) → Ch 19 06 「결과 상태」·05 「호출 ID」와 같은 칸.
- 인자 검사는 `tool.invoke` 안 `ValidationError`를 `ToolInvocationError`로 감싸는 자리(955~966행). **Ch 19 07 b7 「흐름 안 입력 검사 오류는 오류 담기 설정(도구 속성)으로 받지 못해 멈춘다」는 Ch 19 흐름(`run_tool_calls`) 이야기이고, ToolNode 기본값에서는 도구 메시지가 됩니다.**
- 한 응답의 도구 호출 요청 여럿은 `get_executor_for_config` 스레드 실행기의 `executor.map`으로 한꺼번에 실행(821~823행, 비동기는 `asyncio.gather` 858행), 결과 차례는 요청 차례.
- 공식 문서: ToolNode API 참조 페이지는 기본값 이름과 자료형만 적고 동작 설명이 없습니다. LangChain Tools 문서의 도구 오류 예는 **미들웨어(`@wrap_tool_call`)**입니다(Ch 19 06 b10이 이미 가름). → 동작 근거는 설치판 소스로.

### 5-3. `recursion_limit`
- 모델 없는 그래프에서 확인:

| 그래프 | 한도 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 03 Before 모양(`tick → tick`, 끝 없음) | 1번 실행 뒤 오류 | 2번 뒤 오류 | 3번 뒤 오류 | **4번 뒤 오류** | 5번 뒤 오류 |
| 03 After 모양(세 번째에 `END`) | — | 2번 뒤 오류 | **3번 실행하고도 오류** | **통과(3번)** | — |
| 일직선 노드 K개 → END | K=1: 1 오류·2 통과 | K=2: 2 오류·3 통과 | K=3: 3 오류·4 통과 | | |

  → 이 설치판에서 **한도 N이면 노드 실행 N번까지**, **노드 실행 K번 뒤 끝나는 흐름은 한도 K+1부터 통과**. 03의 한도 4는 After가 통과하는 가장 작은 값입니다. 01 대출 흐름(model·tools·model 뒤 끝)에 이 규칙을 대면 한도 4부터 통과가 되지만 **모델 흐름에서는 확인하지 않았습니다**. 소스 자리: `pregel/_loop.py` 607행(`if self.step > self.stop`)·1701·1961행(`self.stop = self.step + recursion_limit + 1`), 오류 글 `pregel/main.py` 3005행.
- **기본 한도는 10007**(`langgraph/_internal/_config.py` 32행 `DEFAULT_RECURSION_LIMIT = int(getenv("LANGGRAPH_DEFAULT_RECURSION_LIMIT", "10007"))`, `ensure_config()` 335행 — 이번에 `ensure_config()["recursion_limit"]`이 `10007`). `langchain_core` 쪽 기본값은 25(`runnables/config.py` 171행)지만 그래프 실행은 LangGraph 값을 씀. **공식 Graph API 문서(2026-09-24 확인)는 「Starting in version 1.0.6, the default recursion limit is set to 1000 steps」** — 문서와 설치판이 다름. 기본값에 기대는 문장을 쓰면 설치판 근거로 쓰고 「문서와 다르다」를 밝힐 것. 모델이 도구를 끝없이 요청하면 기본값으로는 요청 수천 번까지 갈 수 있다는 뜻이라 **한도를 늘 적어 주는 까닭**이 됨.
- 문서: 「`recursion_limit` is a standalone `config` key and should not be passed inside the `configurable` key」(03 b7과 맞음), 「A super-step can be considered a single iteration over the graph nodes」, 「Once the limit is reached, LangGraph will raise `GraphRecursionError`」. `GRAPH_RECURSION_LIMIT` 오류 문서는 기본값을 적지 않음.
- **실제 모델로 결정적인 한도 장면**: 모델이 매번 도구를 요청하게 만들면(`bind_tools(…, tool_choice=…)` — **Ch 19가 가르치지 않은 인자**) 흐름이 끝나지 않아 요청 수가 한도로 정해집니다. 그러지 않으면 한도에 닿는지는 모델 답에 달림. 03을 모델 없이 두면 `check_bundle_execution.py` 계약이 지켜짐(§3).

## 6. §2-7 판단 근거 — 도구 파일

### 사실
1. **챕터 안 되풀이**: 01·02·04에 같은 셀 세 벌 138줄(38%) — 설치·키 셀, 모델·비용 셀(`usage_of`·`make_model`), 규정 자료 + `@tool lookup_policy`. 그래프 만들기는 절마다 다름(01 루프 · 02 ToolNode만 · 03 모델 없음 · 04 비교 그래프).
2. **옮길 수 없는 것**: 노드 함수(`call_model`·`choose`·`answer`)는 LangGraph가 `state` 하나만 넘겨 노트북 전역(`bound_model`·`choice_model`)을 읽습니다 — 인자로 받을 수 없고 함수를 만들어 내는 함수는 「함수 안의 함수」라 금지 → **노트북에 남음**. `@tool` 감싸기·도구 객체는 Ch 19 결정 2대로 노트북.
3. **옮길 수 있는 것(평범한 함수)**: 비용 셈 — 지금 `usage_of`(이 챕터 판)는 **Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`**(과정 표준) + **Ch 19 05 `sum_usage(messages)`**로 바꿀 수 있음 · 메시지 출력 — **Ch 19 06 `show_messages(messages)`**(종류·도구 호출 요청 이름·`status`·내용 — 01·02에서 지금 `enumerate`+`getattr`로 하는 일) · **Ch 19 04 `tool_call_names(response)`** · 규정 찾기 몸통(예: `find_policy(policies, topic)` — Ch 19 03 「몸통 함수」 모양, `@tool` 감싸기는 노트북).
4. **Ch 19 `order_tools.py`를 통째로는 못 가져옵니다**: 파일 맨 위 `import pandas as pd`, Ch 20 잠금에 `pandas` 없음(§3). 폴더도 다름(§2-7 관례 — 챕터마다 따로 두고 같은 본문 + `# Ch N NN절에서 배웠습니다`). 쓸 함수(`estimate_cost`·`sum_usage`·`show_messages`·`tool_call_names`·`make_tools_table`·`spec_names`·`pick_tools`)는 모두 pandas가 필요 없음. `fetch_orders`·`find_order`·`sum_orders`만 pandas에 기댐.
5. **소재**: Ch 20은 자료실 규정(`POLICIES`)을, Ch 19는 주문 CSV를, **Ch 21 01·05(대기)는 Ch 20과 같은 자료실 규정 `lookup_policy`**를 씀. Ch 22(완료)는 도서관 상담 `lookup_hours`.
6. 벡터 계산 없음 → NumPy 대상 없음. 실습 폴더 `tests/` 없음 → §2-7 7항 해당 없음. `verify.py` 금지 모듈 이름(§3).
7. 03은 도구 파일이 없어도 되고, 가져오면 `check_bundle_execution.py`가 묶음 `notebooks/`에서 실행하므로 파일이 묶음에 있어야 함.

### 선택지 (결정하지 않음 — 장단점만)

**A. 도구 파일을 만들지 않는다**
- 장점: 묶음 목록·README·continuity-guide가 그대로. 01·02·04가 독립 노트북으로 남음.
- 단점: 138줄 되풀이, 비용 셈이 과정 표준(`estimate_cost`)과 다른 판으로 남음. 규격 §2-7 3항(앞 챕터 함수는 다시 적지 않음)과 부딪힘 — 선례 Ch 2·4·6·22의 근거(「만들어도 챕터 전체가 줄지 않음」)가 Ch 20에는 약함.

**B. 필요한 함수만 옮긴 새 도구 파일**(이름 후보 **`graph_tools.py`**(챕터 내용 — 그래프) · `toolnode_tools.py`(챕터 이름) · `policy_tools.py`(자료 이름))
- 담을 후보: Ch 6 06 `estimate_cost` · Ch 19 05 `sum_usage` · Ch 19 06 `show_messages` · Ch 19 04 `tool_call_names`(`show_messages`가 안에서 부름) · 필요하면 규정 찾기 몸통. 모두 pandas 없음.
- 장점: 잠금 그대로(패키지 추가 없음). 「앞에서 배운 함수 = 도구 파일」 규칙에 맞음. Ch 19 이름·인자를 그대로 써 이어짐(메시지 읽기가 Ch 19 06과 같은 출력 모양).
- 단점: 묶음 목록 둘(`textbook/part5/public-files.json`·챕터 `qa/public-files.json`)·README·`labs/part5/continuity-guide.md` 9행 「예제 데이터는 각 절에서 다시 준비」 손질. 줄어드는 양은 비용 셀·출력 셀 정도(규정 자료·`@tool` 셀·설치 셀은 남음).

**C. Ch 19 `order_tools.py`를 통째로 복사**(`order_tools.py` 이름 그대로)
- 장점: Ch 19와 글자까지 같은 파일(「같은 코드」라고 쓸 수 있음), 소재를 주문으로 바꾸면 `find_order`까지 바로 씀.
- 단점: **`pandas` 추가**(`pyproject.toml` → `uv lock` → 잠금 재생성, 마운트 폴더라 `uv sync`는 막힘 — 가상환경에 `uv pip install`, `%pip` 줄, 묶음) · 안 쓰는 함수 여럿(`ask_questions`·`count_expected`·`fetch_orders` 등) · 소재를 주문으로 바꾸면 Ch 21 01·05 자료실 규정과 끊기고 `data/orders.csv`도 복사해야 함.

**B·C 공통으로 따라오는 것**: 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」(과정 요약 §3·Ch 19 선례) · `run_section.sh`는 이미 `notebooks/`를 `PYTHONPATH`에 더함 · 가져오는 절이 03이면 `check_bundle_execution.py`가 묶음에서 그 파일을 찾음.

## 7. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 7-1. 그래프 상태 정의와 함수의 타입힌트·클래스

**사실**: 규격 사다리 L5(스키마 클래스 `TypedDict`, 필드만, 라이브러리가 스키마를 요구할 때만) · Ch 13이 상태 형식 아홉 개를 `TypedDict` + `Annotated`로 가르침(클래스 정의는 그것뿐) · Ch 13 노드 함수 힌트 0 · Ch 19는 `@tool` 함수 매개변수 `: str`만 허용(반환 힌트 0). **LangGraph가 힌트를 실제로 읽는 자리는 셋**: 상태 형식 칸(`Annotated[…, add_messages]`의 리듀서) · `@tool` 매개변수(입력 형식) · **오류 처리 함수의 첫 매개변수(받을 오류 종류, §5-2)**. 조건 함수의 반환 힌트 `Literal[…]`은 구조 그림의 갈래 표시에만 쓰이고 `path_map`으로 대신할 수 있습니다(Ch 13 03 「이름표 표」). 노드·도움 함수의 힌트(`-> dict`·`state: AgentState`·`-> BaseChatModel`·`-> tuple[AIMessage, float]`)는 동작에 영향이 없습니다.

- **상태 형식**: (가) Ch 13 04 모양 그대로(`class …(TypedDict)`, 메시지 칸 `Annotated[list[AnyMessage], add_messages]`, 흔적 칸은 Ch 13 02처럼 `Annotated[list[str], operator.add]` + 노드는 자기 몫만) — 장점: 새 문법 0, Ch 13 약속과 같음. 단점: ToolNode는 흔적 칸을 쓰지 않으므로 흔적에 도구 실행이 안 남음(도구 실행은 도구 메시지로 읽거나 04처럼 흔적 노드를 끼움). (나) 02처럼 라이브러리 `MessagesState` — 장점: 클래스 정의 0. 단점: Ch 13이 안 가르친 이름, 흔적 칸을 더할 수 없어 흔적을 버림. (다) 04 `strategy: Literal['fixed', 'agent']` → `str`로(Ch 13 0건 `Literal` 뺌) 또는 Ch 19 02 「고를 수 있는 값」으로 풀어 둠.
- **노드·도움 함수 힌트**: (가) 모두 뺌(Ch 13·19와 같음, `BaseChatModel` import가 없어져 G4 착시도 사라짐) — 단점: 고치지 않는 옛 검사 `check_notebook_readiness.py`(함수 힌트 필수)와는 더 멀어짐(이미 Ch 17~19에서 멈춰 있음). (나) 그대로 — 새 표기(`tuple[…]`·`Any`·`Literal` 반환)마다 한 문장, 옛 검사 `check_notebook_readiness.py`만 만족.
- **오류 처리 함수 `handle_policy_error(error: ValueError)`**: (가) 매개변수 힌트만 **라이브러리가 읽는 값**으로 예외 허용(`@tool` `: str`과 같은 자리, 「이 표시를 보고 ToolNode가 이 함수로 받을 오류를 정합니다」 한 문장 + 힌트를 뺀 판을 값 바꿔 보기로 보여 줄 수 있음) — 장점: 사실 그대로·라이브러리 문서 예와 같음. 단점: 과정 첫 「힌트가 동작을 바꾸는」 장면이라 설명 부담. (나) `handle_tool_errors=(ValueError,)` 튜플 — 장점: 힌트 없음. 단점: 도구 메시지가 영어 틀 「Error: ValueError(…)\n Please fix your mistakes.」로 고정, 안내 글을 못 넣음. (다) 힌트 없는 함수 + 안에서 `type(error).__name__`을 보고 다른 오류는 `raise error`(Ch 16 06 맨 `raise error`, Ch 19 `type(x).__name__` 모양) — 장점: 힌트·새 문법 없음. 단점: 라이브러리 관례와 다르고, ToolNode가 모든 오류를 이 함수에 넘긴다는 사실을 따로 풀어야 함. (라) `True` — 02 b7이 권하지 않는 모양.
- **`@tool lookup_policy(topic: str) -> str`**: Ch 19 결정대로 `: str`만 두고 반환 힌트를 뺄지(Ch 19 01·02 b7 「반환 힌트는 입력 형식·명세에 안 들어감」과 같음).

### 7-2. 제목·`objectives`·Part 목차의 금지어

| 자리 | 말 | 과정 말 |
|---|---|---|
| 04 제목·슬러그 「if **분기**와 모델 선택 비교」 | 분기(Ch 13 금지어) | 갈래 — 선례(Ch 15 03 「프롬프트」·Ch 16 05 「폴백」·Ch 19 05 「병렬 호출」)는 **제목에만 두고 강사 확인**. 슬러그를 바꾸면 `textbook/index.html`·`part5/index.html`(빌드로 다시 만듦)만 따라 바뀌고 완료 챕터 링크는 없음(04를 링크하는 완료 파일 0 — Ch 17은 「Ch 20 04절」 번호로만) |
| 01·02·03 제목 「ToolNode와 tools_condition」·「도구 오류와 ToolMessage」·「recursion_limit과 명시적 종료」 · 챕터 제목 「ToolNode — 모델이 도구를 고른다」 | API 이름 | Ch 19 선례(「tool」·「bind_tools」 제목에만, 본문에서 한 번 풂). **02 슬러그는 Ch 19 06 링크가 걸려 바꾸면 안 됨** |
| `chapter.json` objectives 셋째 줄 「고정 if **분기**와 모델 선택 **분기**를 … **trace**·토큰·비용·**지연**을 비교」 | 분기×2 · trace · 지연 | 갈래 · 실행 흔적(Ch 13 01) · 걸린 초(재면)·요청 수 · objectives 둘째 줄 「실행 한도」는 새 말 후보 |
| `_build_index.py` 25행 · `_notebook/build_index.py` 44행 | 「고정 분기」 | 마감 때 25행만(44행은 선례대로 둠) |
| 본문 공통 | 추정 비용·지연·측정·경로·반환·전파·사전·필드·캐시 단독·로그·프롬프트·병렬·바인딩·벽시계·super-step·비상 차단기·「trace」 | 예상 비용·걸린 초·재다·흐름/차례·내놓다·(오류가) 올라오다·딕셔너리·칸·캐시 입력·기록·질문 글·함께 보내기·도구 알려 주기·걸린 시간·(풀어 쓴 말)·실행 흔적 |

### 7-3. 01·02의 걸린 시간 재기
- 01·02는 주제가 시간이 아닌데 `perf_counter`로 재고 b6 결론에 초를 씁니다. (가) 재기를 빼고 「걸린 시간은 재지 않았습니다」(Ch 13·14·16·19 흐름) · (나) 재되 결과 읽기 둘째 단락에만 「이번 실행에서는」.

### 7-4. 04의 토큰·비용·걸린 시간 비교
- (가) **주제 절 예외로 재고, 결론은 코드로 세는 값만** — 요청 수(6 ↔ 12)·흔적 모양·고르기 요청의 입력 토큰(도구 명세가 실린 몫)·예상 비용(요청 수에서 오는 차이). 걸린 초·출력 토큰·답 글 종류 수는 본문 표와 결과 읽기 둘째 단락·「확인할 점」에만 「이번 실행에서는」, 그림·정리·복습에서 뺌(Ch 17 04·Ch 18 03 선례, 규격 §2-7 9번 끝). 장점: objectives·Ch 17 약속(호출 수·비용·결과 편차) 모두 유지. 단점: 설명이 길어짐, 흔들리는 값 표를 다뤄야 함.
- (나) **걸린 시간을 빼고** 요청 수·토큰·예상 비용·답 글 종류만 — 장점: 흔들리는 값이 줄고 규격 §3 쪽에 가까움, 걸린 시간은 Ch 17 약속에 없음. 단점: 제목·objectives의 「지연」을 고쳐야 하고(마감 몫) Ch 17 이후 처음 도구 선택 비용을 초로 보일 기회를 버림.
- (다) 지금 모양(결론에 평균 초) — 규격 §2-7 9번 끝과 부딪혀 권하지 않음.
- 공통: 비용 셈을 과정 표준 `estimate_cost`로(캐시 입력 칸), 「예상 비용 = 요금표로 어림, 청구 금액 아님」, 반복 2번은 미리 정한 반복(값 고르기 아님)이라는 문장.

## 8. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약·계약·각 챕터 요약·`figures/*.prompt.md` 162개 grep): 카드·봉투·서랍·쟁반·끈·단추·관·깔때기·그릇·빵 칼·주문서 양식·바구니·이름표·꼬리표·우편함·소포·명찰·클립보드·도막·색 딱지·자물쇠·열쇠·리모컨·플러그·**나무 길·갈림길·나무 레일·작업대(Ch 13·18)**·나무판·구멍·마개(Ch 14)·사과·저울·모래시계·궤짝·선반(Ch 15)·쪽지·도장·덮개 천·두루마리·개찰구·체(Ch 16)·눈 위 발자국·바위·말뚝·울타리(Ch 17)·점토·물레·가마(Ch 18)·공항 검사·우편 가림막·전화 연결·방문자 명부·안내 데스크(Ch 22)·**식당 벽·메뉴판 카드·주문 전표·같은 색 집게·내주는 창·걸쇠 건 서랍·취소 상자(Ch 19)**. prompt grep에서 `conveyor`(Ch 2·3)·`rail`(Ch 6·13·17)·`kitchen`(Ch 1·5·6·15)·`counter`·`clip`·`tag`·`hourglass`·`marble`·`gear`(Ch 7)·`turnstile`(Ch 16)·`ticket`(Ch 16·19·22)가 이미 있습니다. **도르래·승강 상자(덤웨이터)·엘리베이터·기송관·차단기(두꺼비집)·부구(볼탭)·수차는 0건.** 지금 `_src` 비유는 01 「도서관 상담 직원」·02 「택배 송장 번호」·03 「건물의 비상 차단기와 정상 종료 버튼」·04 「같은 시험 문제」(그림 없음).

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. 자료실 도르래 승강 상자(덤웨이터)** — 창구와 서고를 잇는 작은 손잡이 도르래 상자 | 01 창구 턱의 상자에 요청 쪽지가 꽂혀 있으면 상자가 서고로 내려갔다 책을 싣고 올라옴 / 쪽지가 없으면 상자는 창구에 그대로 · 02 책 대신 빨간 빈 카드가 실려 올라온 상자(Before는 끈이 풀려 멈춘 상자) · 03 도르래 옆 딸깍 톱니 셋째 칸의 걸림쇠(명시적 종료) ↔ 끈 끝 매듭이 도르래에 걸려 멈춤(한도) · 04 정해진 칸으로만 떨어지는 경사 통로 ↔ 올리고 내리는 상자 | **자료실 규정 소재와 맞음**(Ch 21 01·05도 자료실) · 위아래 왕복이 「노드 둘 사이 되돌아가기」를 화살표 없이 보여 줌 | 끈(앞 계열)·톱니(Ch 7 gear) 소품과 조금 겹침 · 도르래가 작으면 판독이 어려움 · 사람 없이 누가 돌리는지 안 보임 |
| **B. 엘리베이터 층 버튼판** | 01 불 켜진 층 버튼(요청 있음)이면 그 층에 들렀다 돌아옴, 불이 모두 꺼지면 1층 문이 열림 · 02 들른 층의 「닫힘」 표시 카드를 싣고 돌아옴 · 03 운행 횟수 딸깍 계수기(종료 조건) ↔ 비상 정지 손잡이(한도 — 옛 비유 「비상 차단기」와 이어짐) · 04 정해진 층만 서는 급행 ↔ 버튼으로 고르는 칸 | 0건 · 「요청이 있으면 간다 / 없으면 끝」이 버튼 불빛 하나로 읽힘 · 03 두 멈춤의 차이가 뚜렷 | 버튼 숫자·글자 금지라 층 구분을 색·모양으로만 · 결과를 「싣고 돌아오는」 장면이 약함 · 화면·표시등이 과한 색 요소가 되기 쉬움(규격 §5-4 탈락 원인) |
| **C. Ch 19 「식당 주문 전표와 내주는 창」 이어 가기** | 01 전표꽂이에 전표가 걸리면 창 너머로, 요리가 나오면 다시 전표꽂이 확인, 비면 계산서 받침 · 02 요리 대신 「재료 없음」 빈 카드가 **같은 색 집게**로 돌아옴 · 03 전표꽂이 칸 넷이 다 차면 닫히는 덧문(한도) ↔ 마지막 접시 뒤 내려놓는 종(종료) · 04 정식 세트판 ↔ 손님이 고르는 메뉴판 | **Ch 20 = Ch 19 흐름을 그래프로 옮긴 챕터라 그대로 이어짐** · 02의 호출 ID 비유가 「같은 색 집게」 하나로 정리됨(Ch 19 인계 1번) | 식당 그림 7장 뒤 4~5장 더 — 새로 볼 것이 적음 · 되돌아가는 흐름을 화살표 없이 보이기 어려움 · 03 비유가 억지스러움 · kitchen 계열(Ch 1·5·6·15)과도 겹침 |
| **D. 기송관(에어 슈터) 캡슐** | 01 창구에서 캡슐을 관에 넣으면 뒷방으로 갔다 같은 캡슐이 돌아옴 · 02 서류 대신 빨간 카드가 든 캡슐 · 03 캡슐 계수 다이얼 ↔ 관의 차단 밸브 · 04 한 곳으로만 가는 관 ↔ 행선지 다이얼 | 0건 · 같은 캡슐이 돌아오는 모습이 호출 ID와 맞음 | **관(앞 계열)** 과 겹침 · 학생에게 덜 익숙할 수 있음 · 관이 얽히면 판독 어려움 |

- **이어 갈지 새로 갈지**: C는 이음새가 가장 강하지만 Ch 19에서 이미 7장을 썼고 되돌아가는 반복(이 챕터의 새 것)을 보이기 약합니다. A·B는 새 계열이지만 「요청이 있으면 다녀오고 없으면 끝」과 「두 가지 멈춤(03)」이 그림 하나로 읽힙니다. 02의 호출 ID는 새 계열로 가도 「Ch 19 05절의 같은 색 집게처럼」 한 문장으로 이을 수 있습니다(택배 송장 비유는 빼는 쪽). 사람·손·동물·화면·글자·숫자·화살표를 넣지 않는 것이 Ch 19 선례입니다.

## 9. 위험과 깨진 것

1. **01 핵심 관찰이 모델 답에 달림**(§2 01) — 대출 질문에서 도구를 한 번만 부름·인사 질문에서 안 부름에 `assert` 셋. 모델이 두 번 부르거나 인사에도 부르면 셀이 멈춤 → 규격 §2-7 10번 끝(노트북 밖 다섯 번 먼저), `assert`는 매번 같아야 하는 값(메시지 종류가 있는지·자료형·키)으로.
2. **04 결론이 흔들리는 값에 걸림**(§2 04·§7-4) — 걸린 초·출력 토큰·답 글 종류 수(`2·1·2`)는 실행마다 다름. 결론을 걸 수 있는 코드로 세는 값: 요청 수(6 ↔ 12 — agent가 도구를 한 번씩 부를 때), 흔적 모양, 고르기 요청 입력 토큰(흔들리는지 확인 필요). 질문 글이 도구 사용을 강제해 「모델이 고르지 않는 장면」은 없음 — 강제 문구를 빼면 agent 흐름이 끝 갈래로 가는 실행이 섞이고 `run_branch` `assert`가 멈춤.
3. **03 오류 장면은 모델 없이 결정적**(§5-3, 한도 4 = After가 통과하는 가장 작은 값). 실제 모델로 한도에 닿는 장면을 결정적으로 만들려면 `tool_choice`(Ch 19가 안 가르친 인자)로 매번 도구를 요청하게 해야 함. 03에 모델을 넣으면 **`check_bundle_execution.py`가 키 없는 묶음에서 멈춤**(챕터 밖 스크립트 계약).
4. **02 Before 설정이 기본값이 아님**(§2 02·§5-2) — `False`와 기본값은 `ValueError`에서 같지만 인자 검사 오류에서 다름. 「기본 실행은 예외로 중단될 수 있습니다」(`코드를 읽기 전에`)는 기본값 기준으로 다시 쓸 것. 오류 처리 함수의 힌트를 빼면 받는 범위가 넓어짐(힌트가 동작을 바꿈).
5. **`temperature=0` 없음**(G4 `temperature_missing` 3) — `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` + `bind_tools` 조합은 Ch 19 04~07이 통과한 조합(같은 판). `ToolNode`·그래프 안에서 보내는 것은 **이번에 보내지 않았습니다** — 01 첫 실행에서 확인.
6. **완료 챕터 약속**(§4-3) — Ch 7 05·Ch 17 03 「01절에서 ToolNode 루프」 · Ch 17 01·02 「04절 두 흐름 비교」 · **Ch 17 05 보호 자료 「호출 수·비용·결과 편차」** · **Ch 19 06 링크(02 슬러그)**. 어기면 완료 챕터를 고쳐야 함.
7. **첫 줄 주석 틀 문장 32셀**(G3가 못 잡음 — §0) · 결과 읽기 셀 0 · 코드 앞 설명이 소제목 한 줄.
8. **실행하지 않은 사실·틀린 사실**: 01 b3 「Ch13에서 MessagesState」 · 02 b7 「Ch24의 내구 실행」(Ch 23) · 02 `코드를 읽기 전에` 「기본 실행은 예외로 중단될 수 있습니다」(기본값은 `ValueError`만 올림 — 표현 조정) · 03 b3 「키운다고 배웠습니다」 · 01 b4 장소 이름(도서관 ↔ 교육센터 자료실).
9. **옛 생성기 `author_ch20.py`가 개선본·`pyproject.toml`(dev 그룹 없는 판)·`chapter.json`을 덮어씀**(§3) — 01 작업 첫머리에 `raise SystemExit`.
10. **Part 5 옛 검사 넷**(Ch 17~19와 같음) — 고치지 않고 기록. `finalize_evidence.py`는 `language/ch20-final.json` 해시에 Ch 20 원고를 고정해 둠(개선하면 무조건 어긋남).
11. **절 수·실습 절**: `check_scope.py` `SECTION_COUNTS` ch20 = 4 · `_notebook/build_index.py` 44행 절 수 4 → 실습 절을 붙이면 5(선례: 고치지 않음).
12. **서비스 요청 어림**: 노트북 한 번 22번(01 3 · 02 1 · 03 0 · 04 18). 새 커널 두 번 44 + 노트북 밖 다섯 번(01 대출·인사 3 × 5 = 15 · 02 답 1 × 5 = 5 · 04 고르기만 6 × 5 = 30, 전체면 90) + 05 실습 절(3~5 × (2 + 5) ≈ 35) → **약 130~190번**, 요금표 어림 0.1달러 아래(Ch 19 237번 0.073달러). 04 한 번 실행(요청 18)은 기기 셸 180초 안으로 보이지만 걸린 시간은 이번에 재지 않았습니다(옛 출력 평균 걸린 초 1.08~1.46 × 12실행).
13. **판 차이**: `pydantic` 2.13.5(Ch 20) ↔ 2.12.5(Ch 19) · `langchain-openai` 1.6.0(Ch 19·20) ↔ 1.6.1(Ch 13·17). 잠금은 바꾸지 않는 것이 선례(강사 확인). 도구 파일에 pandas 함수를 넣으면 잠금 변경이 따라옴(§6 C).
14. **디스크·환경**: 기기 루트 여유 **1.9G**(작업 전후 같음 — pip 캐시 안 씀, uv 캐시 `/tmp/uv-cache` 387MB 그대로). 가상환경은 마운트 폴더(238MB). Mermaid 도구(`/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`·`/tmp/pw`) 있음. 루트 `.env`에 `OPENAI_API_KEY` **이름** 있음(값은 보지 않음).

## 10. 01절 작업자가 먼저 결정해야 할 것

1. **도구 파일과 소재(§6)** — A(만들지 않음) / B(`estimate_cost`·`sum_usage`·`show_messages`·`tool_call_names`만 옮긴 새 파일, 이름 `graph_tools.py` 등) / C(`order_tools.py` 통째 + pandas). 소재는 자료실 규정 유지(Ch 21 01·05와 이어짐, 잠금 그대로)인지 Ch 19 주문으로 바꿀지(Ch 19와 이어짐, pandas·자료 복사). 비용 셈을 과정 표준 `estimate_cost`로 바꿀지. 결정은 `handoff.md`에 적어 02~05가 따르게.
2. **상태 형식과 힌트 범위(§7-1)** — 상태 형식은 Ch 13 04 모양(흔적 칸에 `operator.add` + 노드는 자기 몫)으로 통일할지, 02 `MessagesState`를 쓸지 · 노드·도움 함수 힌트를 모두 뺄지 · **02 오류 처리 함수의 `error: ValueError`를 「라이브러리가 읽는 표시」로 허용할지**(대안 튜플·안에서 `raise error`) · 조건 함수는 여러 줄 `if` + `path_map`(Ch 13 03)으로, 끝은 `END` 상수로 · 되돌아가는 엣지(`tools → model`·`tick → tick`)를 과정 처음으로 풀 문장.
3. **모델 셀·준비 셀과 오프라인 계약** — `nbkit.key_and_model_cells()` 과정 표준(`temperature=0`)으로 · 03은 모델 없이 둠(`check_bundle_execution.py`) · 01·02의 걸린 시간 재기를 뺄지(§7-3) · `%pip` 줄 모양(Ch 13 따옴표 모양).
4. **흔들림 확인 계획과 `assert` 대상** — 01(대출·인사 질문 노트북 밖 다섯 번: 도구 호출 요청 수·도구 이름·흔적)·04(agent 고르기 요청의 도구 이름·`topic`·입력 토큰 다섯 번) 먼저. 모델 답에 건 `assert` 넷을 무엇(메시지 종류 목록의 자료형, 키가 있는지, 코드가 만든 요청의 `tool_call_id`)으로 바꿀지. 04 결론 기준(§7-4 가/나)과 값 바꿔 보기 후보(키워드 규칙이 놓치는 질문).
5. **용어 표와 비유 계열(§8)** — Ch 13 말(실행 흔적·조건 함수·이름표 표·메시지 리듀서)과 Ch 19 말(도구 호출 요청·도구 메시지·호출 ID·결과 상태·오류 담기 설정(단수)·바퀴 한도·예상 비용)을 이어 쓰고, 새 말(예: 도구 실행 노드(`ToolNode`)·되돌아가는 엣지·오류 처리 함수·실행 한도(`recursion_limit`)·단계(super-step)·명시적 종료) 후보를 정함. 「분기」·「trace」·「지연」·「추정 비용」·「전파」 대체어. 비유 계열 A·B·C·D 중 하나(02 택배 송장 비유를 뺄지).

## 11. 챕터 마감으로 미룰 것

- **05 실습 절 신설**(규격 §7-2): 슬러그 **`05-ToolNode-실습`**(선례 `09-Middleware-실습`·`08-LangGraph-실습`·`06-Agent-개요-실습`·`07-모델과-도구-실습` — 챕터 제목의 앞말 「ToolNode」), 제목 「ToolNode 실습: …」, `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 3·5h에 더하지 않음**). 요청 3~5번, 새 문법·API 0. 주제 예 — 자료실 문의 하나에 01 루프 + 02 오류 처리 함수 + 03 실행 한도를 붙이고 값 하나만 바꿔 다시(예: 오류 처리 설정 켬/끔, 또는 지원하지 않는 주제 질문 ↔ 지원하는 주제 질문). 모델 답이 요청 수를 정하므로 흔들림 확인 대상. 따라오는 것: `chapter.json` 절 추가 · `textbook/part5/_build_index.py` 25행(설명 금지어 「분기」도) · 챕터 `qa/public-files.json`(`notebooks/*.ipynb` 모양이라 노트북은 자동, 도구 파일은 따로) · `textbook/_notebook/build_index.py` 44행(절 수 4, 선례대로 둘지) · `check_scope.py` `SECTION_COUNTS`(기록만) · 01~04 「다음 학습과 이어지는 지점」 중 04를 실습 절로.
- 옛 생성기 둘 `mv -n` → `qa/upgrade/before/generators/blocked/`.
- 옛 그림 12개(`figures/0N-흐름.{svg,excalidraw,caption.md}`) + `figures/_gen_figures.py` 삭제 승인 목록(사본 `before/figures/`).
- `chapter.json` `objectives` 셋(「분기」·「trace」·「지연」, 실습 줄 더하기)과 `textbook/part5/_build_index.py` 25행 설명을 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 넷 + 실습, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 요청 수·예상 비용, 03은 키 없이, 도구 파일을 만들면 그 단락) · `labs/part5/continuity-guide.md` 9행(도구 파일을 만들면) · `qa/research.md`·`technical-review.md`·`verification.md`·`집필점검표.md`(새 값 또는 「개선 전 판」 표시 — 학생 묶음 밖).
- `part5-practice.zip` 재생성(`python3 textbook/part5/_build_index.py`) → `check_bundle_execution.py`(Ch 20 03 PASS 확인, 03 `code_sha256`이 바뀌면 새 값으로 다시 씀) · `check_delivery.py`(`llm-practice.zip` Stale에서 멈춤 예상) · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py`는 결과 파일 되돌림).
- **뒤 챕터 인계**: Ch 21 01 b2·b3·04 b3(직접 조립 그래프) · Ch 21 01·05 노트북 `lookup_policy` 자료실 소재 · Ch 23 01 b3 · Ch 26 01~04 b3(「ToolNode와 명시적 END 조건」) · Part 6 소개 · Ch 22(완료, 언급 0) 대조. Ch 20 02 b7 「Ch24」 → Ch 23.
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 175MB)·`.ruff_cache` · `qa/upgrade/gates-wip-*.json` · `.cache/vm/venv-ch20-tool-node`(238MB) · 기기 `/tmp/ch20-prep`.

## 12. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 4 · `notebooks` 4 · `figures` 13(SVG·excalidraw·caption 각 4 + `_gen_figures.py`) · `generators` 2(`author_ch20.py`·`_gen_figures.py`) · `qa` 4(`public-files.json`·`research.md`·`technical-review.md`·`verification.md`) · `pyproject.toml`·`uv.lock`·`README.md`·`chapter.json`·`집필점검표.md`·`_build.py`·`index.html`(목차, objectives 문장 대조용) = **34개, 476KB**. 원본과 `cmp` 모두 같음(원본은 그대로). `data/`·`runs/`·`tests/`는 챕터에 없어 없음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 182, 통과 0/4) |
| `qa/upgrade/before-manifest.json` | sha256 **50개** — ① 이 챕터가 가져올 수 있는 앞 챕터 파일: Ch 19 `order_tools.py`(`fa5975b5…`) ② Ch 20에 문장·자료로 기대는 완료 챕터 파일: Ch 6 01·Ch 7 05 `_src` · Ch 17 01·02·03·05 `_src` · **Ch 17 05 보호 자료 `autonomy-diagnostic-example.json`**(`9e3ad7da…`)·05 노트북 · Ch 19 05·06·07 `_src`·06 HTML·`author_06.py`(02 링크) · Part 5 소개 `_src/index.html`·`practice-start.md`·`labs/part5/continuity-guide.md` · Ch 22 01 `_src` ③ Ch 20에 기대는 대기 챕터 파일: Ch 21 01·04 · Ch 23 01·06 · Ch 24 01 · Ch 26 01~04 `_src` · Part 6 소개 · `labs/part6/continuity-guide.md` · `_author_ch21_ch29.py` ④ 묶음·목록·기록: `part5-practice.zip`(`72d3e3e7…`) · `textbook/part5/public-files.json` · Part 6 선행 목록·`final-artifact-hashes.json`(Ch 20 없음 — 기준선) · `shared-tests.json` · `existing-artifact-hashes.json`(Part 6)·`existing-artifacts-before.json`(Part 7) ⑤ 규칙·검사: `part5/_build_index.py` · `_notebook/build_index.py`·`build_bundle.py` · `check_bundle_execution.py`·`bundle-execution.json` · 옛 검사 넷 + `language/ch20-final.json` · `verify.py`·`test_verify.py` · `_template/builder.py` |
| `$ROOT/.cache/vm/venv-ch20-tool-node` | Python 3.12.13 · 238MB |

### 가상환경 만든 방법과 결과

- `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch20-tool-node`. 잠금 목록은 `uv export --project labs/part5/ch20-tool-node --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일은 그대로 — `pyproject.toml`·`uv.lock` 수정 시각 전후 같음), 주석 줄만 빼고 환경 표시는 남김(87줄, `/tmp/ch20-prep/req-clean.txt`).
- Ch 16~19 선례대로 `uv pip install pip==26.2` → **`bin/python -m pip install --no-cache-dir -r`**(마운트 폴더에서 `uv pip install -r`이 멈추는 문제를 피하고 루트 디스크에 pip 캐시를 남기지 않음). 설치 오류 0, uv 캐시 정리 안 함.
- 결과: `pip freeze`와 잠금 대조 **판 차이 0**(설치 82 = 잠금 87 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(PyPy)·`httpx2-jsfetch`(emscripten)). `langgraph 1.2.11` · `langgraph-prebuilt 1.1.0` · `langgraph-checkpoint 4.2.0` · `langchain 1.4.0` · `langchain-core 1.6.2` · `langchain-openai 1.6.0` · `openai 3.11.0` · `pydantic 2.13.5` · `python-dotenv 1.2.3` · `ipykernel 7.3.0` · `nbclient 0.11.0` · `pip 26.2` · `ruff 0.15.6` · `tiktoken 0.14.0` · `httpx 0.28.1` · `langsmith 0.12.4` · `IPython 9.17.1` · `jupyter-client 8.10.0` · `pyzmq 27.2.0` · `nbformat 5.11.1`. `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인만: `from langgraph.prebuilt import ToolNode, tools_condition` · `from langgraph.graph import StateGraph, START, END, MessagesState` · `from langgraph.graph.message import add_messages` · `from langgraph.errors import GraphRecursionError` · `from langchain.messages import AIMessage, HumanMessage, ToolMessage, AnyMessage` · `from langchain.tools import tool` · `from langchain.chat_models import init_chat_model` · `typing_extensions.TypedDict` · `dotenv`·`ipykernel`·`nbclient`·`nbformat`·`jupyter_client`·`IPython`·`zmq`. `UV_PROJECT_ENVIRONMENT=…/venv-ch20-tool-node UV_NO_SYNC=1 uv run --project labs/part5/ch20-tool-node`로 이 가상환경을 잡는 것도 확인(`run_section.sh`가 `venv-<챕터 폴더 이름>`을 자동으로 씀).
- §5 확인은 이 가상환경에서 `env -u OPENAI_API_KEY`로 키를 뺀 채 모델 객체 없이 했습니다.

### 참고 자료 (2026-09-24 확인)
- LangGraph Graph API `https://docs.langchain.com/oss/python/langgraph/graph-api`(기본 한도 1000 문구·standalone config key·super-step 정의) · `https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT`(기본값 안 적음) · ToolNode API `https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode`(기본값 이름·자료형만) · `https://reference.langchain.com/python/langgraph.prebuilt/tool_node/tools_condition` · LangChain Tools `https://docs.langchain.com/oss/python/langchain/tools`(도구 오류 예는 미들웨어).
- 설치판 소스: `langgraph/prebuilt/tool_node.py` 111·117·339~382·383~392·394~442·444~500·749~776·821~823·858·940~1012·1582~1660행 · `langgraph/_internal/_config.py` 32·184~186·335행 · `langgraph/pregel/_loop.py` 607·1701·1961행 · `langgraph/pregel/main.py` 3005행 · `langchain_core/runnables/config.py` 171행.
