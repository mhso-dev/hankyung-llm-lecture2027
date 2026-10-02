# 01절 진단 — 하네스와 일곱 기능 (2026-09-28)

- 생성기 `qa/upgrade/author_01.py`(`1cdb29de…`) · 노트북 `labs/part6/ch27-deepagents/notebooks/01-하네스와-일곱-기능.ipynb`(`056ea2d4…`, `code_sha256` `0ffa59d9d8de…`) · `_src/01-하네스와-일곱-기능.html`(`527e28ac…`) · 빌드 HTML(`973b8dd2…`) · 그림 `figures/01-1~01-5`.
- 형식 **experiment** 유지, 슬러그 `01-하네스와-일곱-기능` 고정(Ch 26 05 b8 링크), 제목 「하네스와 일곱 기능」 그대로(강사 확인).
- **모델 요청 0번**(챕터 리드 결정 1 M2의 01 몫 — 모델 객체만 만들고 부르지 않음). 흔들림 확인(`01-probe.md`)은 모델 판단 값이 없어 두지 않았습니다.

## 1. 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 뒤(`gates-wip-01-01.json`) |
|---|---|---|
| 코드 셀 | 4 | **26**(준비 셋 + 모델 셀 하나 + 본문 스물둘) |
| 검사 문장 | 71 | **391** |
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 0 · 2 · 1 · 0 · 5 · 11 · 3 = **22** | **0 · 0 · 0 · 0 · 0 · 0 · 0 (PASS)** |
| 코드 줄(`count_code.py`, 주석·빈 줄 뺌) | 24 | 131 |

- 첫 실행 전 `upgrade_gates.py … --label wip-01 --section 01`: G1 0 · G2 0 · G3 0 · G4 0 · G5 0 · G6 19(70자 넘는 문장 — 대부분 괄호 뒤 「).」로 두 문장이 한 문장으로 세진 것) · G7 18(그림 전). G6은 실행 전에 고쳐 0.
- AST 따로(`/tmp/ch27-01/tools/extra_check.py` — Ch 26 판 + 도구 파일 이름 `harness_tools.py` 허용 줄만 더함): **0건**. 호출 깊이(`depth.py`) **최대 2**. 준비 셀 밖 셀 최대 8줄(6절 `task` 실행 셀), 함수 본문 최대 5줄, 셀당 정의 하나.
- 금지어(`/tmp/ch27-01/tools/ban27.py` = ban26 + 준비 노트 §9-2 말): 노트북 설명·주석·`_src`·`.mmd`·캡션에서 **걸림 1건 — 「Harness」(b2 첫 풀이 자리, 의도)**. 「경로」·「반환」·「측정」·「검증」·「문맥」·「프롬프트」·「캐시」·「오프로딩」·「한 겹 더」 0건(`AnthropicPromptCachingMiddleware`·`system_prompt` 같은 코드 이름은 백틱 안).
- `verify.py --chapter`: `PASS 8 sections / 58 code cells (max 17 lines)`(17줄은 02~08 옛 노트북). 빌드 HTML `{{`·`[[` 0건.

## 2. 수정 전 주요 문제 (옛 판 — 학생 본문에는 쓰지 않음)

1. **검사 방법 결함**: `inspect.getsource(create_deep_agent)` 문자열에서 미들웨어 이름 일곱을 `in`으로 찾아 `True` 일곱·`all(...)`. 소스에는 독스트링·주석이 들어 있어, 설치판에서 조립하지 않는 `TodoListMiddleware`도 `True`로 나옴(준비 노트 §2 01) → 「조립 경로가 있다」도 보이지 못함. 옛 b5 「True는 해당 조립 경로가 소스에 존재한다는 뜻」은 틀린 해석.
2. 「일곱 기능」 분류가 조립과 맞지 않음: 기본 넷(파일·서브에이전트·요약·짝 맞추기)과 선택(스킬·메모리·사람 승인·비동기 서브에이전트)을 한 줄로 셈, 「파일 권한」은 미들웨어가 아니라 파일 도구 안 판정인데 `HumanInTheLoopMiddleware`와 한 항목, 기본으로 붙는 `PatchToolCallsMiddleware`는 빠짐.
3. 모델·키 셀 없음(`dotenv`만), 하네스를 Ch 6 01 정의와 다르게 「모델 호출 주위에 … 조립해 긴 작업을 실행하는 틀」로 새로 정의, Ch 9 06 「실험 하네스」와 가르지 않음.
4. 문법: 한 줄 복합문 `for …: print(…)` · 딕셔너리 13줄 셀 · `sum(features.values())`(호출 두 겹)·`all`·`inspect` · 첫 줄 주석 없는 준비 셀.
5. 금지어: 경로 6/3/2 · 측정 2 · 검증 2/0/1 · 런타임 1(복습 3) · 표면 1/1 · 「기본 활성」 등.
6. 결과 읽기 셀 0 · 제목 셀·핵심 그림 첨부 없음 · Mermaid 0 · 삽화 0 · 옛 SVG 토큰 `{{svg:01-흐름}}` · b10 참고 자료가 여덟 절 같은 여섯(확인 2026-09-11) · b1 둘째·셋째 목표와 b8 셋째 항목이 여덟 절 같은 틀 문장.
7. 요금 사고 구조(실행 한도 9999·general-purpose 서브에이전트 자동·부모 한도가 서브에이전트에 닿지 않음)를 다루지 않음.

## 3. 바꾼 것

- **노트북(26 코드 셀, 여섯 절)**: 1절 준비(설치 다섯 — deepagents 0.7.0·langchain 1.4.0·langchain-openai 1.6.0·langgraph 1.2.11·python-dotenv 1.2.3, 잠금 판 · 가져오기 · 키 · 모델 셀) → **2절** `create_agent(model, tools=[])` ↔ `create_deep_agent(model=model)`의 종류·노드 · 두 그래프의 실행 한도 → **3절** 함수 `tool_names(agent)`(속성 `nodes["tools"].bound.tools_by_name` — Ch 20 01 `tools_by_name` 이음) · Deep Agent 도구 아홉 · `create_agent` + `FilesystemMiddleware()` 하나(Ch 22 이음 — 도구 여덟·노드 넷) · 함수 `names_only_in` · Deep Agent에만 있는 `['task']`·`['PatchToolCallsMiddleware.before_agent']` · 도구 `task`의 인자와 설명 글의 `general-purpose` → **4절** 함수 `show_added` · 인자 하나씩(`skills=`·`memory=`·`interrupt_on=`·`permissions=`·비동기 서브에이전트 명세) → **5절 값 바꿔 보기** `middleware=[TodoListMiddleware()]`(예상 → 노드 하나·도구 하나) → **6절** 바깥 `ModelCallLimitMiddleware(run_limit=3)` 노드 둘 · 같은 이름 `general-purpose` 명세(자기 호출 한도 0) · 설명 글 바뀜 `True`/기본 설명 `False` · 상태 형식 `ToolsOnlyState`(Ch 13 04) · 도구 실행 노드만 든 작은 그래프(Ch 26 02 모양) · 손으로 만든 `task` 요청(Ch 20 01 모양) → `Model call limits exceeded: run limit (0/0)`·`success` → 정리 셋.
- **본문 10블록** 블록 단위로 다시 씀: b2 「왜」(미리 조립한 틀 · 챕터 제목 Harness 첫 풀이) · b3 Ch 6 01·Ch 21 01·Ch 22 01/04·Ch 20 01/03·Ch 26 01/05 · b4 비유(온실) + 삽화 + 하네스 정의(Ch 6 01 그대로 이어 씀·쟁반과의 관계·Ch 9 06과 가름) + 용어 표 여섯 + 01-1 + 일곱 기능 대응 표 + 요금 사고 단락 · b5 + 01-2 · b6 조립 결과 표 + 01-3 + 01-4 + 두 커널 문장 · b7 열 항목 · b8 · b9 네 문제 · b10 절 자료(확인 2026-09-28).
- **새 용어 6**(meta): Deep Agent · 기본 미들웨어/선택 기능 · 파일 도구 · general-purpose 서브에이전트 · 할 일 목록 · 서브에이전트 명세. 이어 쓴 말: 하네스(Ch 6 01) · 노드형 훅/감싸기형 훅(Ch 22 01) · 도구 찾기 표(Ch 20 01) · 실행 한도·호출 한도(Ch 20 03·Ch 22 04) · 서브에이전트·전문 에이전트(Ch 26 01).
- 옛 판의 `assert`(판 번호·`all(features.values())`) 뺌 — `assert`는 키 셀 하나뿐.

## 4. 실행과 값 (모델 요청 0 — 모두 결정적 값)

- 교재 출력 **A**: `run_section.sh` 2026-09-28T11:49:19Z · `PASS … 26 cells` · `code_sha256` `0ffa59d9d8de38e8…`. 사본 **B**(그림 전): 11:49:48Z, 같은 `code_sha256`. **셀별 출력 대조 26/26 같음**(`cmpout.py`, 셀 출력 글 연결 해시 `c5d6b14a0e82d71d` 셋 — A·B·마크다운 고친 뒤 디스크 노트북). `outputs_sha256`(A `36d99865…` · B `650b51dd…`)은 실행 메타데이터가 섞여 달라 셀 글로 대조(과정 요약 §9).
- **요청 0 확인**: 같은 코드 셀 스물둘을 가짜 키 글(`sk-not-a-real-key`)로 노트북 밖에서 모두 실행해도 오류 없이 같은 출력(`/tmp/ch27-01/dryrun.py`) — 모델을 한 번이라도 불렀다면 인증 오류로 멈췄을 조건. 6절 `task` 실행은 서브에이전트 명세의 `ModelCallLimitMiddleware(run_limit=0)`의 `before_model`이 모델 앞에서 끝냄(`model_call_limit.py` 168~208행).
- 결정적 값(본문·그림·정리에 쓴 값): `CompiledStateGraph`(두 함수) · `create_agent의 노드: ['__start__', 'model', '__end__']` · `create_deep_agent의 노드: ['__start__', 'model', 'tools', 'PatchToolCallsMiddleware.before_agent', '__end__']` · 실행 한도 `9999`·`9999` · `도구 수: 9`(`delete`·`edit_file`·`execute`·`glob`·`grep`·`ls`·`read_file`·`task`·`write_file`) · `create_agent` + `FilesystemMiddleware` `도구 수: 8`·노드 넷 · 차이 `['task']`·`['PatchToolCallsMiddleware.before_agent']` · `task` 인자 `['description', 'subagent_type']`·설명 글 `general-purpose` `True` · 더해진 노드/도구: skills `SkillsMiddleware.before_agent`/— · memory `MemoryMiddleware.before_agent`/— · interrupt_on `HumanInTheLoopMiddleware.after_model`/— · permissions deny —/— · 비동기 —/도구 다섯(`cancel_async_task`·`check_async_task`·`list_async_tasks`·`start_async_task`·`update_async_task`) · TodoList `TodoListMiddleware.after_model`/`write_todos` · 바깥 호출 한도 `ModelCallLimitMiddleware.before_model`·`.after_model`/— · 명세 키 넷 · `바꾼 설명이 실렸는가: True`·`기본 설명이 남았는가: False` · `등록한 노드: ['tools']` · `ToolMessage`·`Model call limits exceeded: run limit (0/0)`·`success`.
- 흔들린 값 없음. 걸린 시간은 재지 않음. 파일 쓰기 0(StateBackend·임시 폴더도 쓰지 않음).

## 5. 요금 사고 방지 — 모델 없이 확인한 결과 (챕터 리드 결정 2)

노트북 밖(`/tmp/ch27-01/x3_safety.py`, 가짜 키 글·요청 0 — 서브에이전트 모듈의 `create_agent`를 감싸 만든 그래프의 미들웨어 이름과 묶인 설정을 봄):

| 확인 | 결과 |
|---|---|
| A 기본 Deep Agent의 general-purpose 스택 | `FilesystemMiddleware`·`SummarizationMiddleware`·`PatchToolCallsMiddleware`·`AnthropicPromptCachingMiddleware`, 묶인 `recursion_limit` **9999**, 호출 한도 없음 |
| B 부모 `middleware=[ModelCallLimitMiddleware(run_limit=3)]` | 부모 그래프에 노드 둘이 더해짐 · **general-purpose 스택은 A와 같음**(옮겨 가지 않음 — `graph.py` 777행 `_gp_inheritable`은 기본 자리 이름과 같은 것만) |
| C 같은 이름 `general-purpose` 명세 + 명세 `middleware`에 한도 | 스택에 `ModelCallLimitMiddleware`가 들어감(기본 GP 대신) · `task` 설명 글의 서브에이전트는 우리 설명 하나 |
| D 이름이 다른 명세만(`reviewer`) | 기본 general-purpose(한도 없음)가 **함께 붙음** + `reviewer`(한도 있음) |
| E C 판의 도구 실행 노드만 든 그래프 + 손 `task` 요청, 부모 설정 `{"recursion_limit": 3}` | `ToolMessage 'Model call limits exceeded: run limit (0/0)' success` — 요청 0으로 서브에이전트 안 한도가 걸림(노트북 6절에 같은 모양으로 넣음) |
| (준비 노트 e3 재실행) 묶인 한도가 있는 서브에이전트 그래프 | 부모 한도 5를 무시하고 20단계 끝까지(`subagents.py` 559~565행 — 묶인 설정이 부딪히는 키에서 이김) · 묶이지 않은 그래프는 `GraphRecursionError` |

→ **챕터 공통 안전 규칙(02~09)**: ① 바깥 에이전트 `middleware=[ModelCallLimitMiddleware(run_limit=N, exit_behavior="end")]` ② `subagents=`에 **언제나** 같은 이름 `general-purpose` 명세를 넣고 그 `middleware`에 `ModelCallLimitMiddleware(run_limit=M, exit_behavior="end")` ③ 사용자 서브에이전트 명세마다 자기 호출 한도. 상한 = N + (`task` 부른 횟수) × M(요약이 켜지면 그 요청 더함 — 340,000토큰 기준이라 수업에서는 켜지지 않음). **남는 틈**: 한 응답의 `task` 요청 수는 막지 않음(설명 글이 「여럿을 함께」 권함) — `ToolCallLimitMiddleware(tool_name="task", …)`가 langchain 1.4.0에 있지만 과정에서 가르치지 않아 쓰지 않음(쓰면 그 절이 새 API로 풂). general-purpose를 아예 끄는 방법(`HarnessProfile`의 `GeneralPurposeSubagentProfile(enabled=False)` + `register_harness_profile`)은 전역 등록이라 쓰지 않음.

## 6. 고친 틀린 사실·과장

- 옛 b4·b5·b6 「`in source`가 True면 생성 경로에 관련 코드가 존재」·「일곱 항목이 모두 True, 합계 7」 → 소스 문자열은 조립 여부를 보이지 못함(조립하지 않는 `TodoListMiddleware`도 True) → **조립 결과(노드·도구 이름)를 출력으로 견주는 방법**으로 바꿈.
- 옛 b4 「일곱 기능을 … 분류합니다」·그림 설명 「7개 기능은 모두 항상 활성화된다는 뜻이 아닙니다. skills·memory·permissions·async subagents는 인자를 전달할 때 추가」 → 부분 참이지만 **권한(deny)은 미들웨어를 붙이지 않고 파일 도구 안에서 판정**, 「사람 승인」은 `interrupt_on=`(또는 권한 `mode="interrupt"`)일 때 `HumanInTheLoopMiddleware`, 기본에는 일곱에 없는 `PatchToolCallsMiddleware`가 있음 → 대응 표로 다시 셈(기본 셋 + 선택 넷, 일곱 밖 짝 맞추기·할 일 목록).
- 옛 b4 하네스 정의(새 정의) → Ch 6 01 정의를 그대로 이어 씀 + Ch 9 06 실험 하네스와 가름.
- 옛 b2 「설치된 패키지의 조립 코드를 읽어 그 틀이 실제로 무엇을 더하는지 확인」 → 코드를 읽는 대신 만든 그래프를 출력으로 봄.
- 옛 b10 「gpt-5.4-mini 모델과 가격」·「MIT 라이선스」 등 여덟 절 공통 자료 → 이 절 자료(개요·customization·subagents·0.7.0 릴리스·설치판 소스 행).
- (문서와 설치판의 차이, b7·b10에 밝힘) 공식 서브에이전트 문서의 명세 키 `mode`(`"isolated"`·`"fork"` — 마감에서 `forked` 오기를 고침, 검토 A-1)는 설치판 0.7.0에 없음. 문서는 이 기능이 deepagents 0.7.13 이상에서 된다고 적음.

## 7. 도구 파일 — 만들지 않음

- 이 절은 앞 챕터 함수(Ch 19 `tool_call_names`·`show_messages`·`sum_usage`, Ch 6 06 `estimate_cost`)를 **하나도 쓰지 않아** 챕터 리드 결정 6대로 `harness_tools.py`를 만들지 않았습니다(묶음 목록·zip 변경 0).
- 이 절이 처음 가르친 함수 셋(`tool_names(agent)` · `names_only_in(base, other)` · `show_added(base_nodes, base_tools, agent)`)은 노트북에 둠. 뒤 절이 다시 쓰면 그 절이 도구 파일로 옮김(인계 12항 8번).

## 8. 옛 생성기

- `qa/author_ch27.py`: 첫머리 설명 주석 셋 + `from __future__ import annotations` 바로 뒤 `raise SystemExit("옛 Ch 27 원고·노트북 생성기입니다. …")`(`from __future__`가 파일 첫 문장이어야 해 그 뒤에 둠) · `45453725…` → `7bc6c96d3e1e0a458f0499d42aaafa900aa14bb50ea7a973f201832ea43af8e4`. 사본 `/tmp/ch27-01/gen-before/`와 diff 네 줄(주석 셋·막는 줄 하나). `PYTHONDONTWRITEBYTECODE=1 python3`로 실행 → 종료 코드 1·그 글.
- `figures/_gen_figures.py`: 첫머리 설명 주석 셋 + `raise SystemExit(...)` · `45d40ea2…` → `98641eb53491c3b9b8770596c1f8d162639c710b58ce67d05a8b7ece1c708e48`(diff 네 줄, 실행 → 종료 코드 1).
- 옮기기(`mv -n` → `qa/upgrade/before/generators/blocked/`)는 마감 몫. `qa/__pycache__/author_ch27.cpython-312.pyc`는 그대로(삭제 승인 목록).

## 9. 그림

- Mermaid **4장**: 01-1(폭 333) · 01-2(313) · 01-3(395) · 01-4(667) — 모두 868 이하, PNG 직접 열어 확인. 첫 렌더에서 01-1·01-3의 긴 미들웨어 이름이 단어 가운데서 끊겨 `<br>`로 나누고 `rankSpacing` 28(01-1·01-3)·`wrappingWidth` 300(01-3), 01-4는 상자 차례를 바꿔 폭 827 → 667. 보라 0 · 빨강 0. 노트북 첨부는 01-1 하나(「오늘 볼 그림」 — `attached 1`).
- 삽화 **1장** `01-5-설비를-갖춘-온실`: 1차 job `810070a2-5fb6-4596-bc33-5bb934f29f0b` 탈락(화분 셋) → **2차 job `9644de40-2d44-4d0d-bf20-9223e47357cc` 채택**(재생성 1회, 한도 안). 거래 11:53:23.394368Z·11:54:30.718231Z 「Nano Banana Pro −2」 둘 = **4크레딧**(잔액 2345 → 2341, 바로 앞 거래 09:53:58Z는 다른 세션). 작업 조회 모델 표시 `nano_banana_2`(요청 `nano_banana_pro` — Ch 25·26과 같은 표시 차이). 저장 1100 × 614 `455326a6…`, 다시 받은 원본을 같은 폭으로 줄여 픽셀 대조 bbox `None`·최대 차이 0. 세부는 `figures/01-5-설비를-갖춘-온실.prompt.md`.
- 옛 그림 `01-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0 — 삭제 승인 목록).

## 10. 완료·대기 챕터 문장 (확인)

- **Ch 26 05 b8(완료)** 「Ch 27 01절에서는 긴 작업에 자주 쓰는 기능을 미리 묶어 둔 DeepAgents를 봅니다」 + 링크 `../ch27-deepagents/01-하네스와-일곱-기능.html` → **참**(슬러그 그대로 · 01이 기본 미들웨어 넷·도구 아홉을 출력으로 보임).
- **Ch 6 01 표(완료)** 「DeepAgents — 긴 작업에 필요한 기능을 갖춘 하네스 — Ch 27 DeepAgents — Harness 계층」 → **참**(챕터 제목 그대로, 하네스 정의를 Ch 6 01 그대로 이어 씀).
- Ch 21·23·24 요약의 「Ch 27 01 b3 참」 기록: 새 b3는 Ch 23 체크포인터·Ch 24 사람 승인 문장을 빼고 Ch 6·20·21·22·26을 가리킴(깨지는 문장 없음 — 기록 파일은 고치지 않음). Ch 26 요약 §13 「Ch 27 01 b3 『Ch 26은 위임 구조를 다뤘습니다』 참」 → 새 b3에도 그 문장이 있음(참).
- Ch 28 01 b3(대기) 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다」 → 01까지로는 참(파일·서브에이전트 미들웨어를 미리 조립). 「하위 작업」 말은 Ch 28 몫.

## 11. 강사 확인 대상

1. 제목 「하네스와 일곱 기능」 유지 — 본문은 「일곱 기능 = 이 교재가 부르는 이름, 조립으로 세면 기본 셋 + 선택 넷(+ 일곱 밖 짝 맞추기·할 일 목록)」으로 사실대로. 챕터 제목의 「Harness」도 제목에만(b2 첫 풀이).
2. 코드 셀 4 → 26, 코드 줄 24 → 131(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와의 균형 — 결정 4의 비교·안전 규칙 확인을 모두 출력으로 보이느라 늘어남). 4절 인자 다섯 셀은 표 하나로 줄일 수도 있음.
3. 01이 서브에이전트 명세·호출 한도 교체(6절)를 먼저 보임 — 06(서브에이전트 위임)보다 앞서 「서브에이전트 명세」를 새 용어로 정의.
4. 6절 호출 한도 0은 확인용으로 정한 값(b7에 「흐름을 보여 주려고 정한 예」).
5. 삽화 양옆 흰 여백이 넓음(재생성 한도를 씀 — 글로만).
6. 새 용어 6 · 새 말 「Deep Agent」(create_deep_agent가 만든 그래프)를 영어 그대로 둔 것.

## 12. 챕터 밖 수정·보호 파일·남은 것

- **챕터 밖 수정 0**(공용 도구·과정 문서·앞 챕터 파일 고치지 않음). `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json`은 `verify.py --chapter`가 다시 씀(`8775ce03…` → `4308e649…`).
- 보호 파일(`before-manifest.json` 238개): `manifest-changes.md` 참고.
- 지워야 하지만 지우지 않은 것(삭제 승인 목록): 기기 `/tmp/ch27-01/`(작업 폴더 — 탐색 스크립트 `x1~x5`·`dryrun.py`·`tools/`·사본 `A/`·`B/`·`gen-before/`·삽화 원본 `illu/`·임시 폴더 `ch27-01-x5-*` 둘) · `.cache/ch27-01-view/`(그림 확인 사본 넷 — 이 절이 만듦. **작업 중 `illu-1-orig.png` 사본에 `rm -f`를 한 번 잘못 불렀으나 연결 폴더 삭제가 막혀 지워지지 않았음**) · `qa/upgrade/gates-wip-01.json`·`gates-wip-01-01.json` · 옛 그림 `figures/01-흐름.*` · `qa/__pycache__/` · 실습 폴더 `workspace*`(이 절은 건드리지 않음).
- 기기 루트 디스크 여유 **2.3G(작업 전후 같음)**.

## 마감 반영 (2026-09-28)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 글·그림·기록으로 반영했습니다. **노트북은 다시 실행하지 않았고** 코드 셀은 한 글자도 바꾸지 않았습니다(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 고친 방법: 생성기 문자열 치환(`.cache/ch27-close/tools/gapply.py`·`smartrep.py` — 바뀐 생성기의 `cells()` 코드 셀이 노트북과 다르면 멈춤) → 달라진 마크다운 셀만 노트북에 옮김 → `src_html()`로 `_src` → `run_section.sh … NN --no-exec`. 전체 기록은 `chapter-summary.md`.

- **A-2 [중]** 「기본 미들웨어 넷」 → 정의대로 **다섯**(`AnthropicPromptCachingMiddleware`가 늘 붙음 — 이 과정 모델에서는 아무 일도 하지 않음, 설치판 `graph.py` 860행): 용어 표 행(짝 맞추기 풀이 A-4 포함) · 「일곱 기능과 실제 조립」 표에 「(일곱 밖) Anthropic 모델용 미들웨어」 행 · 「다시 세면」 단락 · 「공식 개요 문서는 같은 기능을」 → 「기능을」 · 비유 둘째 단락·「비유와 다른 점」(그림의 설비 넷 = 이 과정 모델에서 일하는 넷, 다섯째는 그림에 없음)·그림 읽기 · 01-1 그림·alt·캡션·도식 읽기(A-3 근거 갈래) · 노트북 셀 1(오늘 볼 그림, 첨부 교체)·27·43(「짝 맞추기 미들웨어 뒤, Anthropic 모델용 미들웨어 앞」 — `graph.py` 855·883행) · b10 customization 문서 「늘 붙고 맞지 않는 모델에서는 아무 일도 하지 않는다」. 코드 출력에는 넷을 세는 자리가 없음.
- **A-1 [중]** b7 문서 값 `forked` → `"fork"`, 「문서는 이 기능이 deepagents 0.7.13 이상에서 된다」 · b10 서브에이전트 문서 설명에 같은 구절 · 이 진단 §6·`handoff.md` 금지어 줄의 같은 값.
- A-4 b7 「대화 요청과 다른 OpenAI의 요청 방식(Responses API)」 · b10 「기본 스택」 → 「기본 미들웨어 차례」 · A-5 b4 쟁반 단락 뒤 하네스 자리 한 문장 · A-16 b4 둘째 단락과 노트북 셀 55에 「요약 미들웨어가 켜지면 그 요약 요청은 이 합 밖이고, 켜지는 기준은 05절에서 봅니다」.
- 마크다운 셀 1·27·43·55. 노트북 파일 `056ea2d4` → `5bd52b6f`(첨부 01-1 PNG 교체 포함) · `_src` `527e28ac` → `9974664f` · HTML → `52378ee6` · `author_01.py` `1cdb29de` → `01cfc823`. 게이트 0.
