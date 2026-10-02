# Ch 27 DeepAgents — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part6/ch27-deepagents` 01~08절(품질 개선) + **09절 챕터 끝 실습 절 신설**(`09-DeepAgents-실습`), 노트북 `labs/part6/ch27-deepagents/notebooks/01~09-*.ipynb`, 도구 파일 `notebooks/harness_tools.py`. 뒤 챕터가 읽는 계약 파일(산출 파일)은 없습니다.
- 기간: 2026-09-28(준비 조사 · 01~08절 개선 · 09절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 여덟 절 합계 **245**(G1 23 · G2 15 · G3 12 · G4 5 · G5 46 · G6 120 · G7 24 — 01 22 · 02 42 · 03 32 · 04 33 · 05 30 · 06 32 · 07 30 · 08 24, `gates-before.json`) → 마감 뒤 **9/9 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 403·368·432·417·437·432·390·474·373 = **3,726**).
- 코드 셀 4·5·5·4·5·4·4·5 = 36 → **26·26·30·31·31·30·27·31 + 09 새 절 21 = 253**(`verify.py --chapter` → `PASS 9 sections / 253 code cells (max 13 lines)`). 코드 줄(`count_code.py`, 주석·빈 줄 뺌) 24·28·25·26·46·26·41·36 → **131·132·182·180·183·189·148·194 + 09 122 = 1,461**, 도구 파일 66줄. Mermaid **36장**(01~07 넷씩 · 08 다섯 · 09 셋), 삽화 **9장**(절마다 하나, Higgsfield — 01·02·04 재생성 1회씩, 마감 0), 복습 문제는 HTML에만.
- **모델 요청**: 01은 0(모델 객체만 만들고 부르지 않음). 02~08은 앞 절반이 모델 없는 구조(결정적)이고 뒤 절반이 실제 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`), 09는 실습 절. 노트북 한 번 **0 · 2 · 7(교재 출력, B 6) · 3 · 3 · 5(바깥 2 + 서브에이전트 3) · 3 · 4 · 4 = 31**번. 작업 전체(노트북 밖 흔들림 확인 + 새 커널 A·B — `probe/*.jsonl`과 진단으로 다시 셈, §9) **01 0 · 02 14 · 03 47 · 04 21 · 05 21 · 06 35 · 07 21 · 08 32 · 09 28 = 219번**, 마감 **0번**.
- 화면 검사 `visual.cjs`: HTML **열 개**(아홉 절 + `index.html`) × 1280px·390px = **20행 PASS**(기기 `/tmp/pw` playwright·`/tmp/pw-browsers` chromium-headless-shell — Ch 26 마감이 설치한 것 그대로).
- **마감에서 다시 실행한 노트북: 없음.** 아홉 노트북 모두 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같습니다(마크다운만 — §19).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 26 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-28)」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」)·`NN-probe.md`(노트북 밖 흔들림 확인) → 검토 `review-round1-A.md`(01~04·공통)·`review-round1-B.md`(05~09) → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 하네스와 일곱 기능 | **함수 `create_deep_agent`**(모델 객체만 넘김) ↔ `create_agent`(도구 없음) — 둘 다 `CompiledStateGraph`, 노드 `['__start__', 'model', 'tools', 'PatchToolCallsMiddleware.before_agent', '__end__']` ↔ `['__start__', 'model', '__end__']`, 실행 한도 9999 둘 · **기본 도구 아홉**(파일 도구 일곱 + `execute` = `FilesystemMiddleware`, `task` = `SubAgentMiddleware`) · 도구 찾기 표 `agent.nodes["tools"].bound.tools_by_name` · **기본 미들웨어 다섯**(파일 → 서브에이전트 → 요약 → 짝 맞추기 → Anthropic 모델용 `AnthropicPromptCachingMiddleware` — 이름·차례는 설치판 `graph.py` 816~860행으로만, 요약·Anthropic 모델용은 출력에 안 보임, 마감 A-2) · 인자 하나씩: `skills=`·`memory=`·`interrupt_on=`(노드 하나씩) · 권한 `FilesystemPermission(mode="deny")`(더한 것 없음 — 파일 도구 안 판정) · 비동기 명세(도구 다섯) · 값 바꿔 보기 `middleware=[TodoListMiddleware()]` · 바깥 `ModelCallLimitMiddleware`(노드 둘) · **general-purpose 교체**(같은 이름 서브에이전트 명세 + 자기 호출 한도 0) · 도구 실행 노드만 든 작은 그래프(`StateGraph` + `TypedDict` `ToolsOnlyState`)에 손 `task` 요청 → `Model call limits exceeded: run limit (0/0)` | **`tool_names`**·**`names_only_in`**(02가 도구 파일로 옮김) · `show_added`(노트북) | Deep Agent · 기본 미들웨어/선택 기능 · 파일 도구 · general-purpose 서브에이전트 · 할 일 목록 · 서브에이전트 명세 (6) |
| 02 create deep agent와 도구 | 인자 `tools=`(더해지기만 함 — 설치판 336행) · **백엔드**와 `StateBackend`(기본, 상태 칸 `files`) · `supports_execution` · `LocalShellBackend`(만들기만) · 모델이 받는 도구 목록(기록 훅 `@wrap_model_call` — Ch 22 02 모양, `execute`가 빠진 아홉) · **안전 규칙 (가)·(나)**(바깥 한도 3 + general-purpose 명세 한도 2) · 요청 수 두 셈(응답 목록 · 기록 훅) | 도구 `lookup_rule`·기록 훅 `record_tool_names`(노트북) · **도구 파일 첫 판**(앞 챕터 넷 + 01 둘) | 백엔드 (1) |
| 03 플래닝과 시스템 프롬프트 | `TodoListMiddleware()` → 도구 `write_todos`·노드 `TodoListMiddleware.after_model`·**상태 칸 `todos`**·**할 일 설명 글**(속성 `system_prompt`, 1370자) · `args_schema.model_json_schema()`·`$defs` · `get_output_jsonschema()`·`properties` · 인자 `system_prompt=`와 합쳐지는 차례(우리 글 + 빈 줄 + 할 일 설명 글, 요청마다) · `repr` · 할 일 목록을 켠 실행의 요청 수 셈 | 기록 훅 `record_request` · `show_todos`(노트북) | 0 |
| 04 파일시스템과 중간 결과 | `FilesystemBackend(root_dir=tempfile.mkdtemp(prefix="ch27-04-"))`(`virtual_mode` `True`) · 백엔드 직접 `write`(권한 밖) · 파일 위치 규칙(`/` = 기준 폴더, `..` → `try/except ValueError`) · 두 백엔드의 도구 실행 노드 작은 그래프(`FilesystemState`)에 같은 손 `write_file` 요청 — 상태 칸 ↔ 디스크 · 파일 항목 칸 · 실제 모델이 `write_file`로 중간 결과를 적은 실행 | `tools_only_graph`(노트북 — 05~08이 04 셀 글 그대로 다시 적음, §15 예외) | 기준 폴더 (1) |
| 05 컨텍스트 관리와 오프로딩 | **옮겨 두기** — `FilesystemMiddleware`가 도구 결과를 `/large_tool_results/<호출 ID>`로 옮기고 **안내 글**(파일 위치 + 나눠 읽으라는 설명 + 미리보기 — 열 줄을 넘으면 앞뒤 다섯 줄, 마감 B-1)만 남김 · 기준 `4 × tool_token_limit_before_evict`자(`NUM_CHARS_PER_TOKEN` 4, 기본 80000자) · 같은 이름 `FilesystemMiddleware(tool_token_limit_before_evict=10)`로 한도 바꾸기 · 요약 기준 `model.profile["max_input_tokens"]` × 0.85 = 340000토큰(요약은 실행하지 않음) | 도구 `read_visit_log` · 기록 훅 `record_sizes`(노트북) | 옮겨 두기 · 안내 글 (2) |
| 06 서브에이전트 위임 | 서브에이전트 명세 키 `tools`(rule-checker, 한도 4) · 바깥 `tools=` 없이 위임을 구조로 · 명세 하나면 기본 general-purpose가 함께 붙음 → 같은 이름 교체 · 한도 0 복사본에 손 `task` 요청 → 서브에이전트가 받은 것(시작 기록 훅 **`@before_agent`**, 딕셔너리 `.copy()` — 넘긴 글 한 줄 `HumanMessage` + 바깥 `files`) · 기록 훅을 바깥과 두 명세에 → 받은 도구로 요청을 나눠 셈 · Ch 26 셈 3 ↔ 훅 5 | `show_task_names`·`record_inputs`(노트북) | 0 |
| 07 출처 검증형 deep research | **W2**: 교재용 자료 셋을 손 요청 `write_file`로 상태 칸에 넣고, 기본 `grep`·`read_file`로 찾게 함(새 도구 0 · 서브에이전트 0 · 디스크 0) · 출처 표시 뽑기 **`find_source_marks`**(Ch 16 01 — 도구 파일에 더함) · 출처 확인 판정 **`check_citations(answer, known)`** · 인자 모으기 **`call_args`** · 판정이 보지 못하는 것(글 내용·빠진 자료) | **`check_citations`**·**`call_args`**(08이 도구 파일로 옮김) | 주어진 자료로 하는 조사 · 출처 확인 (2) |
| 08 통합 실행과 운영 한계 | 권한 규칙 `FilesystemPermission(operations=["write"], paths=["/sources/**"], mode="deny")`(도구 실행 노드만 든 그래프로 손 요청 — `success`·`error`) · 같은 이름 `FilesystemMiddleware()`면 권한이 사라짐(노트북 안) · `interrupt_on={"write_file": True}` + `InMemorySaver` → 승인 노드 `HumanInTheLoopMiddleware.after_model` · `__interrupt__`의 질문 값(`action_requests`·`review_configs`, 결정 넷) · **결정 목록** `Command(resume={"decisions": [{"type": "approve"}]})`(Ch 24 모양 글 답 `Command(resume="approve")`는 `TypeError`) · 승인 작은 그래프(거절·대신 답하기는 막지 못함 — 마감 B-4) · 운영 한계 표 | `review_graph`(노트북) | 도구 실행 경계 · 결정 목록 (2) |
| 09 DeepAgents 실습 | **새 문법·새 API·새 말 0**(01~08 노트북·도구 파일과 AST 대조) | 조립 함수 `build_memo_agent`·견주기 함수 `show_run`(노트북) | 0 |

- 새 용어 합계 **14개**(절 meta 「새 용어」 6·1·0·1·2·0·2·2·0).
- **이 챕터에서 허용한 문법**: 맨 `@tool` 줄 + 매개변수 `: str` · 데코레이터 `@wrap_model_call`(02·03·04·05·06)·`@before_agent`(06) · 칸만 적은 `TypedDict` 상태 형식(01 `ToolsOnlyState` — 04 이후 `FilesystemState` 가져옴) · `try/except 오류 이름` 두 셀(04 `ValueError`·08 `TypeError`) · 도구 파일 `estimate_cost`의 `.get` 둘(Ch 6 06 본문 그대로). 마감 AST 따로(`extra_check.py`) 금지 문법 0.
- **쓰지 않은 것**(아홉 절·도구 파일 0건): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·힌트·대입 풀기·별표 풀기·`while`·세미콜론·`isinstance`·클래스(상태 형식 밖)·`re`·`get_state_history`·`update_state`·`stream`·스킬·장기 메모리·비동기 서브에이전트 실행·웹 검색.
- 셀 모양: 준비 셀 밖 셀 10줄 이하, 함수 본문 8줄 이하, 셀당 정의 하나, 첫 줄 주석 100%, 호출 깊이 최대 2. `assert`는 키 셀에만(모델 판단·모델 글에 0).

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 6 01·06**: 하네스 정의(모델 호출을 둘러싼 실행 틀 — 01 b4가 그대로 이어 씀, 계층 지도의 DeepAgents 자리) · 모델 설정 · **`estimate_cost`와 요금표**(02~09, Ch 21 `runner_tools.py` 판 글자 그대로).
- **Ch 8 02·03**: 「파일에 있어도 컨텍스트는 아님」(04 b4) · 적어 두기·골라 넣기·나누기(05·06 b3). **Ch 9 06**: 실험 하네스와 가름(01 b4 한 문장).
- **Ch 13 01·04 · Ch 20 01·03**: 상태 형식 · 도구 실행 노드와 도구 찾기 표 `tools_by_name` · 손으로 만든 도구 요청 · 실행 한도.
- **Ch 16 01·04**: `find_source_marks`와 허용 목록(07 — Ch 16 `guardrails.py` `d4f76099…` 글자 그대로) · 호출 한도.
- **Ch 17 03 · Ch 18 04**: 정지 조건(03 할 일 목록의 상태와 가름) · 계획 모델과 작업 목록(03 b3).
- **Ch 19 01·02·04·05·06**: `@tool`·독스트링 설명 · 세 글 가운데 하나만 받는 칸(`Literal` — 03 항목의 `status` 값과 같은 모양) · `tool_call_names`·`sum_usage`·`show_messages`(도구 파일, Ch 21 판 글자 그대로).
- **Ch 21 01**: `create_agent`·`system_prompt=`·`lookup_policy`(없는 주제어 오류 — 02 `lookup_rule`은 정해 둔 글을 내놓음).
- **Ch 22 01·02·04·07**: 노드형 훅·감싸기형 훅(01) · 기록 훅(02 이후) · 호출 한도(`ModelCallLimitMiddleware`) · 먼저 등록한 미들웨어가 바깥에서 감쌈(03 기록 훅 자리).
- **Ch 23 01**: 체크포인터·스레드(08·09 `InMemorySaver`) · `mkdtemp`(04).
- **Ch 24 01**: `interrupt`·`Command(resume=답)` — 08이 결정 목록으로 이음(b3·5절, 같은 점과 다른 점).
- **Ch 26 01·04·05**: 도구 함수 안 전문 에이전트의 안쪽 목록·바깥 실행 한도가 닿지 않음(01 b3·6절) · 요청 셈(06 — Ch 27 서브에이전트는 도구를 가져 「× 1」이 아님) · 완료 조건(03·06 b3 — 06은 명세 글에 끝나는 조건을 적음) · 05 b8이 Ch 27 01을 링크.
- 소재: **교육센터 자료실**(Ch 21·26 규정 글을 이음 — 대출·연장·연체·운영 규정 넷, 07 교재용 자료 셋 `/sources/closing-notice.md`·`return-box.md`·`new-books.md`). 모두 「교재용」 표시.

## 3. 절별 과제·값 (새 커널 두 번과 노트북 밖 흔들림 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값·두 커널과 흔들림 확인 5/5가 같았던 값(결론·그림에 쓴 값) |
|---|---|---|
| 01 | 도구 없는 `create_agent` · 인자 없는 Deep Agent · 인자 하나씩 · general-purpose 교체 명세(한도 0) + 바깥 한도 3 · 손 `task` 요청(모델 없음) | 노드 셋 ↔ 다섯 · `9999` 둘 · `도구 수: 9`·`8` · `Deep Agent에만 있는 도구: ['task']` · 더해진 노드 `SkillsMiddleware.before_agent`·`MemoryMiddleware.before_agent`·`HumanInTheLoopMiddleware.after_model`·(권한 `[]`)·`TodoListMiddleware.after_model` · 비동기 도구 다섯·`write_todos` · 호출 한도 노드 둘 · `바꾼 설명이 실렸는가: True`·`기본 설명이 남았는가: False` · `run limit (0/0)`·`success` · 요청 0 · 새 커널 26/26 |
| 02 | 규정 넷 + `lookup_rule` · 바깥 한도 3 · 질문 한 줄 | `도구 수: 10`·`빠진 도구: []` · `StateBackend` `False` ↔ `LocalShellBackend` `True` · 모델이 받은 도구 아홉·그래프에만 `['execute']` · (5/5) 첫 응답 `lookup_rule` 한 번·메시지 넷·요청 2(두 셈 같음)·`task` 0 |
| 03 | 5절 할 일 목록 없이 ↔ 6절 할 일 목록 + 우리 글 93자(「먼저 write_todos로 …」) · 바깥 한도 10 | 도구 설명 3873자 · 할 일 설명 글 1370자 · 5절 시스템 글 `''`·받은 도구 아홉 ↔ 6절 1465자(우리 글 + 빈 줄 + 할 일 설명 글, 요청마다)·열 · (5/5) 6절 첫 응답 `write_todos`·응답마다 하나 이하·`task` 0·5절 요청 2 · 첫 요청 입력 토큰 1874 → 3106(서비스 값, 「이번 실행에서는」) |
| 04 | 디스크 백엔드(임시 폴더) ↔ 기본 백엔드 · 손 `write_file` · 질문이 정한 `/notes/rules.md` | `virtual_mode` `True` · `..` → `ValueError` · 손 요청 `['/drafts/memo.md']` ↔ `[]`·임시 폴더에 `drafts` · (5/5) `write_file` 한 번·디스크 글 == 요청 인자 글·요청 3 |
| 05 | 방문 기록 2,000줄(분실물 345번째) · 기본 한도 ↔ 한도 10 | 88889자 → 안내 글 1122자·`/large_tool_results/hand_log_1`·원래 글과 같음 · 기준 80000자 · 한도 10 → 41자 → 658자 · 요약 기준 340000 · (5/5) `read_visit_log` → `grep` → 답·요청 3 |
| 06 | rule-checker 명세(한도 4) + general-purpose 교체(한도 2) · 바깥 조회 도구 없음 · 한도 0 복사본 손 `task` | 받은 것 `메시지 수 1`·`HumanMessage`·`['/notes/question.md']` · `run limit (0/0)` · (5/5) `task` 한 번 rule-checker·보고 파일 `/notes/rule-check.md`가 상태 칸에·요청 5(바깥 2 + 안 3)·Ch 26 셈 3 ≠ 5 |
| 07 | 자료 셋 · 질문 「10월 셋째 주 토요일에 … 반납할 수 있나요?」 류 · 손 글 넷 | 손 `grep` → 둘 · 판정 `True`·`False`·`[]`·빠뜨린 글 `True` · (5/5) `grep` → `read_file`(휴관 안내 하나) → 답·`task` 0·요청 3 — **무인 반납함 자료를 읽지 않은 실행을 교재 출력으로 둠**(판정이 보지 못하는 예) |
| 08 | 조립(안전 규칙·보고 파일·자료 셋·권한 deny·`interrupt_on`·체크포인터) · 손 요청 둘 · 승인 작은 그래프 · 실제 흐름 | 노드 여덟·`실행 한도: 9999` · `success`·`error` ↔ 같은 이름 둘 다 `success` · `__interrupt__`·`('review',)`·결정 넷 · 결정 목록 → `success`·보고 파일 · 글 답 `TypeError` · (5/5) 멈출 때까지 `grep` → `read_file` → `write_file`·멈춘 요청 `write_file \| /reports/answer.md`·다시 멈추지 않음·`task` 0 · 요청 수 = 도구를 요청한 응답 수 + 1 |
| 09 | §10 | §10 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | Deep Agent | 함수 `create_deep_agent`가 만든 에이전트 그래프(문장 첫머리는 「이 Deep Agent는」·「함수 … 가 만든 …」) | `deep_agent` |
| 01 | 기본 미들웨어 · 선택 기능 | 인자 없이도 붙는 미들웨어(파일·서브에이전트·요약·짝 맞추기·Anthropic 모델용 **다섯** — 다섯째는 이 과정 모델에서 아무 일도 하지 않음, 마감 A-2) / 인자를 줘야 붙는 기능(스킬·메모리·사람 승인·비동기 서브에이전트) | `graph.py` 816~860행 |
| 01 | 파일 도구 | 파일을 보고 쓰는 도구 일곱(`ls`·`read_file`·`write_file`·`edit_file`·`delete`·`glob`·`grep`) — `execute`는 「명령 실행 도구」 | `FilesystemMiddleware` |
| 01 | general-purpose 서브에이전트 | 따로 막지 않으면 늘 붙는 기본 서브에이전트(호출 한도 없음) | `subagent_type="general-purpose"` |
| 01·03 | 할 일 목록 | 모델이 긴 일을 단계로 나눠 적고 상태를 고쳐 적는 목록(01 한 줄 정의 · 03 본격) | `write_todos` · 상태 칸 `todos` |
| 01·06 | 서브에이전트 명세 | 서브에이전트의 이름·설명·시스템 메시지 글·미들웨어(·`tools`)를 적은 딕셔너리 | `helper_spec` · rule-checker |
| 02 | 백엔드 | 파일 도구가 파일을 실제로 두는 자리를 정하는 부품(보관 방식) — `StateBackend`(상태 칸 `files`)·`FilesystemBackend`(디스크) | 04 b4 비유도 「보관 방식」(마감 A-12) |
| 04 | 기준 폴더 | 디스크 백엔드가 파일 위치 `/`로 보는 폴더 | `root_dir` |
| 05 | 옮겨 두기 | 긴 도구 결과를 파일로 옮기고 메시지 목록에는 안내 글만 남기는 일(「오프로딩」은 제목에만) | `tool_token_limit_before_evict` |
| 05 | **안내 글** | **옮겨 둔 뒤 도구 메시지에 남는 짧은 글**(파일 위치·나눠 읽으라는 설명·미리보기) — **챕터 안에서 이 뜻 하나만**(마감 A-14·B-7) | 도구 메시지 내용 |
| 07 | 주어진 자료로 하는 조사 · 출처 확인 | deep research를 교재 자료 셋으로 좁힌 조사 / 답의 출처 표시가 실제로 있는 자료를 가리키는지 살피는 일(「검증」은 제목에만) | `check_citations` |
| 08 | 도구 실행 경계 · 결정 목록 | 도구가 실행되기 직전의 자리(승인 노드·권한 판정) / 멈춘 요청마다 결정 하나를 담은 목록 | `{"decisions": [...]}` |
| (이어 씀) | 실행 한도 · 호출 한도 · 바퀴 한도 | 그래프 단계 수(Deep Agent 9999) · 한도를 붙인 에이전트의 invoke 한 번 모델 요청 수 · 루프 바퀴 수 — 섞지 않음 | — |
| (이어 씀) | 상태 칸 | 그래프 상태의 칸(03 `todos`·04~ `files`). 03 할 일 항목의 칸은 「항목의 `status` 값」으로 가름(마감 A-9) | — |

- **「안내 글」 한 뜻 정리(마감)**: 03의 할 일 미들웨어 글 → **「할 일 설명 글」**(`_src`·노트북 설명·그림 03-1~03-4) · 02·04의 「정해 둔 안내 글」(없는 주제어 답) → 「넣을 수 있는 주제어를 알려 주는 정해 둔 글」 · 09의 사용자 공지 → **「공지 글」**. 코드 속 말은 그대로 두고 결과 읽기에서 가름: 03 출력 라벨 `안내 글 첫 줄:`·`안내 글 글자 수:`·`할 일 안내 글로 끝나는가:`·`우리 글 + 빈 줄 + 안내 글과 같은가:`(03 셀 21·b4) · 02·04·05·06 `lookup_rule` 주석 「정해 둔 안내 글」(05 셀 35) · 09 `request_text` 머리말 「안내 글:」과 `memo_text` 속 「안내 글」(09 셀 17·b7). **다음 재실행 몫**(§18-5).
- **쓰지 않는 말**(아홉 절 설명·주석·캡션·`.mmd`·README 참 금지어 0 — 제목·슬러그·코드 백틱 말고): 챕터 리드 결정 5 목록 + 준비 노트 §9-2(「반환」·「측정」·「검증」·「경로」·「최대」·「오프로딩」·「플래닝」·「프롬프트」·「캐시」 단독·「명시」·「결정적」 등 — `ban27.py`). 마감이 더한 문장의 걸림은 거짓 양성(「체크포인터」 속 「포인터」)뿐. Anthropic 캐시 미들웨어는 본문에서 「Anthropic 모델용 미들웨어」로 부름(「캐시」 단독 금지).
- **뜻 겹침 주의(뒤 챕터)**: Ch 28 01 b3 「하위 작업」은 Ch 27 본문 말이 아님(06은 「위임」·「서브에이전트」) — §17.

## 5. 비유 가족 「온실과 모종판」 (삽화 아홉)

- 01-5 설비를 갖춘 온실(설비 넷 = 이 과정 모델에서 일하는 기본 미들웨어 넷, 빈 화분 넷 = 선택 기능 — 다섯째 Anthropic 모델용은 그림에 없음, 마감 A-2) · 02-5 도구 걸이에 더한 연장 · 03-5 봉투를 꽂은 화단(할 일 목록, 새싹 = `completed`) · 04-5 온실과 헛간의 모종판(보관 방식 = 백엔드, 마감 A-12) · 05-5 온실 밖으로 옮긴 퇴비 포대(옮겨 두기, 꼬리표 = 안내 글) · 06-5 곁 온실에 맡긴 모종(서브에이전트) · 07-5 색 리본과 어미 화초(출처 표시) · 08-6 자물쇠 문과 막아 둔 문(권한·승인) · 09-4 심기 전 모종과 바로 심은 모종(승인 켬 ↔ 끔).
- 사람·손·글자·숫자·화살표 없음. 짝짓지 않는 요소(수·크기·자란 모습·여백)는 그림 읽기에 밝힘. 삽화는 마감에서 다시 만들지 않음(Higgsfield 0).

## 6. 색 규칙 (Mermaid 36장)

- 우리가 정한 값·손으로 만든 요청·넣은 글 **초록(tool)** · 우리가 부른 함수·만든 함수·작은 그래프 **파랑(flow)** · 출력으로 확인한 값·받아 출력한 오류·한도 글 **노랑(measure)** · 설치판 소스로만 확인한 것·라이브러리가 준 것·셈 **회색(클래스 없음)** · **보라 = 그 절에서 실제로 부른 모델만**(차례 그림의 연보라 띠 02-2·03-3·04-3·05-3·06-3·07-3·08-4·09-2, 모델 응답 상자 04-4·05-4·07-1 — 01과 앞 절반 그림 보라 0) · **아홉 절 모두 experiment라 빨강 0장**.
- 원본 viewBox 폭 모두 868 이하. 라벨에 토큰·비용·답 글·보고 글 없음. 모델 판단 값 라벨은 흔들림 확인 5/5 **그리고** 새 커널 두 번 같을 때만(06-3 안쪽 도구 차례는 이 규칙에 맞지 않아 마감에서 뺌 — B-2).
- **마감에서 다시 렌더한 `.mmd` 여섯**: `01-1`(기본 미들웨어 다섯·차례는 소스 확인 — 노트북 첨부 교체) · `03-1`(상태 칸·할 일 설명 글 — 노트북 첨부 교체) · `03-2`·`03-3`·`03-4`(할 일 설명 글) · `06-3`(안쪽 도구 차례 뺌). 모두 `--force`, PNG 직접 확인.

## 7. 결정적 값과 흔들린 값

- **결정적 값**(결론·그림·정리·복습에 쓴 값): §3 표 전부. 코드가 정하는 구조 값은 새 커널 두 번 모두 같았고, 모델 판단 값은 노트북 밖 흔들림 확인 5/5(09는 조건마다 5/5 = 열 번)와 두 커널에서 같을 때만 「흔들림 확인 다섯 번과 두 커널에서 모두」로 한정해 씀. **결론 문장의 중심은 셈**: 요청 수 = 도구를 요청한 응답 수 + 1(서브에이전트를 부르지 않은 실행) · 서브에이전트 요청은 기록 훅으로만(06).
- **흔들린 값 — 결론·그림·정리·복습에 쓰지 않음**(결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만): 03 6절 요청 수 4 ↔ 5·할 일 항목 글 · 04 메시지 수 8 ↔ 9·`lookup_rule` 3 ↔ 4 · 06 넘긴 글·보고 글 · 07 `grep` 출력 모양·인용 줄 수·답 글 · 08 이어 간 뒤 요청 1 ↔ 2(노트북 밖 4/5는 보고 파일을 다시 읽음)·보고 글 · 09 메모 글 · 모든 절의 토큰·예상 비용. 마감에서 결론·그림·정리·복습에 흔들린 값에서 끌어낸 비교가 남았는지 다시 봄 — 없음(두 검토와 같음).
- **노트북 밖에서만 본 값(b7에 「노트북 밖」 표시)**: 01 문자열 모델의 Responses API·같은 이름 `FilesystemMiddleware`의 권한 손실·이름 다른 명세의 기본 general-purpose 동반 · 03 한 응답 `write_todos` 둘 이상 막기(소스) · 04 파일 도구 `..` 오류·`KeyError: 'files'` · 05 40자 그대로·41자 옮김 · 06 rule-checker 안쪽 도구 차례(콜백 기록)·전체 비용 · 08 `edit`·결정 0개 `ValueError`·호출 한도가 이어 가는 invoke에서 0부터·**작은 그래프에 거절·대신 답하기를 넣으면 쓰기가 실행됨(마감 재확인)**.
- **재지 않은 것·실행하지 않은 것**: 걸린 시간(모든 절) · 요약 실행 · 스킬·장기 메모리·비동기 서브에이전트 실행 · 웹 검색 · `LocalShellBackend` 에이전트 실행 · 결정 `edit`·`reject`·`respond`(노트북) · 권한 `mode="interrupt"` · Windows·macOS 실행.

## 8. 안전 규칙 (가)·(나)와 상한 식·남는 틈

- **사실(01 확인)**: Deep Agent 그래프의 실행 한도 9999 · general-purpose 서브에이전트가 늘 붙고 호출 한도가 없음 · 서브에이전트는 도구 `task`의 함수 안에서 실행되어 묶인 설정(9999)이 바깥 설정보다 앞섬(`subagents.py` 559~565행) · 바깥 `middleware=`의 호출 한도는 general-purpose로 옮겨 가지 않음(`graph.py` 777행) · 이름이 다른 명세만 넘기면 기본 general-purpose가 함께 붙음 · 같은 이름 명세는 기본 자리를 바꾸고 명세의 한도가 그 스택에 들어감(01 6절 `run limit (0/0)`).
- **규칙**: (가) 바깥 에이전트 `middleware=[ModelCallLimitMiddleware(run_limit=N, exit_behavior="end")]` (나) `subagents=`에 **언제나** 같은 이름 `general-purpose` 명세(자기 호출 한도 M) (다) 사용자 서브에이전트 명세(06)마다 자기 호출 한도. 모델을 부르는 02~09 모두 (가)·(나)(바깥 N = 02 3 · 03~09 10, M = 2, 06 rule-checker 4).
- **상한 식**: 한 번 실행(invoke)의 모델 요청 ≤ N + (`task`를 부른 횟수) × M. **예외 — 요약 요청은 이 식 밖**(요약 미들웨어는 감싸기형 훅 안에서 모델을 따로 불러 호출 한도가 세지 않음, 기준 340,000토큰이라 수업에서는 켜지지 않음 — 01 b4·셀 55에 마감 A-16으로 한 문장). 호출 한도는 invoke 한 번마다 세고, 승인으로 이어 가는 invoke에서 0부터(08).
- **남는 틈**: 한 응답의 `task` 요청 수는 막지 않음(`task` 설명 글이 「여럿을 함께」 권함 — 01 b7) · `ToolCallLimitMiddleware`는 과정 0건이라 쓰지 않음 · general-purpose를 끄는 하네스 프로필은 전역 등록이라 쓰지 않음 · 권한 규칙은 파일 도구 안 판정이라 우리 도구·명령 실행·백엔드 직접 호출에 걸리지 않고, 같은 이름 `FilesystemMiddleware`를 넣으면 사라짐 · 승인 작은 그래프(`review_graph`)는 거절을 막지 못함(08 b7).

## 9. 모델 요청 수와 예상 비용

| 절 | 노트북 한 번 | 흔들림 확인(노트북 밖) | 새 커널 A + B | 작업 전체 | 예상 비용 어림(작업 전체) |
|---|---|---|---|---|---|
| 01 | 0 | 0 | 0 + 0 | **0** | 0 |
| 02 | 2 | 10(5회 × 2) | 2 + 2 | **14** | 약 0.022달러 |
| 03 | 7(5절 2 + 6절 5, B는 6) | 34(두 조건 5회씩 — 2·4·2·5·2·5·2·5·2·5) | 7 + 6 | **47** | 약 0.12달러 |
| 04 | 3 | 15 | 3 + 3 | **21** | 약 0.042달러 |
| 05 | 3 | 15 | 3 + 3 | **21** | 약 0.038달러 |
| 06 | 5(바깥 2 + 안 3) | 25 | 5 + 5 | **35** | 약 0.059달러 |
| 07 | 3 | 15 | 3 + 3 | **21** | 약 0.035달러 |
| 08 | 4(노트북 밖 1/5 4 · 4/5 5) | 24(4·5·5·5·5) | 4 + 4 | **32** | 약 0.055달러 |
| 09 | 4(2 + 2) | 20(두 조건 5회씩 × 2) | 4 + 4 | **28** | 약 0.046달러 |
| 합 | 31 | 158 | 61 | **219**(마감 0) | **약 0.41달러** |

- 다시 센 방법: `probe/probe-0N-*.jsonl`의 회차마다 `requests`(06은 `hook_total`, 07은 `outer_requests`)를 더하고, A·B는 각 진단의 새 커널 기록과 노트북 출력(`기록 훅이 센 요청 수`·`요청 수`·셈 표)으로 셈 — 인계의 절별 값과 모두 같음. 탐색 스크립트(`x*.py`·`DRY`)는 가짜 키 글로 요청 0.
- 예상 비용은 과정 요금표(2026-09-17, mini 입력 0.75·출력 4.50달러/100만 토큰)로 **캐시 입력을 빼지 않고** 어림한 값이고 청구 금액이 아님(06은 서브에이전트까지 — 노트북 셀은 바깥 요청만). 절마다 1달러 안.

## 10. 09절 실습 절 주제와 결과

- 제목 「**DeepAgents 실습: 메모 파일 쓰기에 사람 승인을 켜고 끄기**」, 슬러그 `09-DeepAgents-실습`, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~08 meta 합 강의 1h × 8 = **8h** · 실습 2h × 8 = **16h** = `chapter.json` 「총 24h · 강의 8h · 실습 16h」(`_build_index.py`도 8·16).
- 자료실 안내 도우미가 사용자가 보낸 **공지 글**(07 교재용 자료 `/sources/return-box.md` 두 문장 + 머리말 「안내 글:」)을 이용자용 한 문장으로 다듬어 메모 파일 `/reports/notice.md`에 적음. 붙인 앞 절 기능 셋(두 실행 모두 흐름 안에서 쓰임): **04** 파일 도구와 상태 칸 `files` · **08** 사람 승인(`interrupt_on`·`InMemorySaver`·결정 목록) · **02·07·08** 요청 수 셈(`sum_usage`·`call_args`) + **01~03** 안전 규칙. 뺀 것: 07 자료 찾기·출처 판정(요청 4번 이상 × 2) · 08 권한 규칙(흐름에서 안 쓰임) · 06 서브에이전트 · 03 할 일 목록 · 05 옮겨 두기.
- 실행 1(`build_memo_agent({"write_file": True})`) → 실행 2(**값 하나 `{}`** — 승인 미들웨어가 붙지 않음, 설치판 `graph.py` 193~194행). 모델 요청 **4번**(2 + 2). 사람의 답은 코드가 넣은 `approve`(b7).
- 결과(새 커널 두 번 20/21 같음 — 갈린 하나는 토큰·비용 + 노트북 밖 조건마다 5번, 열 번 같음): 실행 1 노드 여덟(`HumanInTheLoopMiddleware.after_model`)·`멈췄는가: True`·`첫 invoke 뒤 메모 파일이 있는가: False`·`멈춘 도구 요청: write_file | /reports/notice.md`·`넣을 결정 수: 1`·`다시 멈췄는가: False` · 실행 2 노드 일곱·`멈췄는가: False`·`True` · 7절 `실행 1 | True | False | ['/reports/notice.md'] | 2`·`실행 2 | False | True | ['/reports/notice.md'] | 2` → **「사람 승인은 요청 수를 늘리지 않고 invoke를 둘로 나눔 · 달라진 것은 메모 파일이 생긴 때」**(흔들림 확인 열 번 + 두 커널로 한정, **다른 도구를 쓰지 말고 적은 파일을 다시 읽지 말라고 정한 시스템 메시지 글 아래에서** — 마감 B-8). `assert`는 키 셀 하나뿐.
- 코드 셀 21(실습 선례 19~28) · 코드 줄 122 · 함수 본문 8·6줄.

## 11. 도구 파일 `notebooks/harness_tools.py` — 함수 표·해시 변천·생성기 대조 사슬

| 함수(인자) | 배운 곳 | 가져오는 절 | 하는 일 |
|---|---|---|---|
| `tool_call_names(response)` | Ch 19 04 | 02~05(`show_messages` 안에서도) | 응답 하나의 도구 요청 이름 목록 |
| `show_messages(messages)` | Ch 19 06 | 02·03·04·06·07·08·09 | 메시지 목록을 한 줄씩 출력 |
| `sum_usage(messages)` | Ch 19 05 | 02~09 | 목록 안 `AIMessage`마다 요청 하나·토큰 합(사용량 `None`이면 멈춤) |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06 | 02~09 | 예상 비용(`.get` 둘 — 허용 표시) |
| `tool_names(agent)` | **Ch 27 01 노트북 3절** | 02~09 | 도구 실행 노드의 도구 이름을 알파벳 차례로 |
| `names_only_in(base, other)` | **Ch 27 01 노트북 3절** | 02·03 | 둘째 목록에만 있는 이름 |
| `find_source_marks(answer)` | Ch 16 01 | 07(`check_citations` 안에서도) | 대괄호로 묶은 출처 표시 목록 |
| `check_citations(answer, known)` | **Ch 27 07 노트북 4절** | 08 | 출처 표시마다 인용한 파일이 known 안에 있는지 |
| `call_args(messages, tool_name, arg_name)` | **Ch 27 07 노트북 5절** | 08·09 | 이름이 같은 도구 요청마다 인자 하나의 값 |

- 함수마다 `# Ch NN MM절에서 배웠습니다 — …` 주석, 가져오기 줄 0, 노트북 전역 이름 기대기 0, 금지 문법 0(허용 표시 `.get` 둘), 66줄. 앞 넷은 Ch 21 `runner_tools.py`(`f4113158…`)·Ch 26 `delegation_tools.py`와 본문·설명 주석 같음, `find_source_marks`는 Ch 16 `guardrails.py`(`d4f76099…`)와 글자 같음. 01 `show_added`·04 `tools_only_graph`·08 `review_graph`와 기록 훅들은 노트북에 둠.
- **해시 변천**: 없음 → 02 `14ee39ca…`(함수 여섯) → 03~06 그대로 → 07 `0c4ee4f9…`(+ `find_source_marks`) → 08 **`7a40d99477ca7c4371a7120e6088c3ac77ed5919300091873f214694675372ed`**(+ `check_citations`·`call_args`) → 09 그대로 → **마감 그대로**(챕터 리드 결정).
- **머리 설명**(검토 A-17·B-11): 「Ch 21 도구 파일 runner_tools.py에서 옮긴 함수」·「이 챕터 01절 노트북에서 옮긴 함수」 두 줄만 있고, 07·08이 더한 Ch 16 `guardrails.py`·07 노트북 출처는 머리에 없음(함수마다 위 주석은 바름). 해시 고정 결정으로 그대로 — README가 함수 열의 배운 절·가져오는 절을 적음. 고치면 `author_02.TOOLS_HEAD` → `author_02/07/08.TOOLS`·`strip_later_imports`·`check_tools()`·02/07/08 쓰기 가드·zip·챕터 공개 목록 해시를 함께 맞춤(노트북은 다시 실행 불필요) — **Ch 24·25·26과 함께 전체 마감 한 항목**(최종 점검표 §2-13 6번에 덧붙임).
- **생성기 대조 사슬**(마감에서 다시 확인 — 모두 통과, 생성기의 도구 줄 0 바뀜, `.cache/ch27-close/tools/chain27.py` — 쓰기 없음): `author_02.TOOLS` = `TOOLS_HEAD` + 함수 여섯(`RUNNER_SHA`·`DELEGATION_SHA` 고정 확인) · `author_07.TOOLS` = 02 판 + Ch 16 블록(`GUARDRAILS_SHA`) · `author_08.TOOLS` = 07 판 + 07 셀 둘 = **디스크 파일**. `author_02.strip_later_imports(디스크)`가 02 판으로 시작 → 02 쓰기 가드 「skip」, 07 가드 「skip」(디스크가 02·07 판이 아님), 08 「같은 판」, 03~06·09는 도구 파일을 쓰지 않음(`check_tools()` 통과). 아홉 생성기 `cells()`가 노트북과 56·56·64·66·66·64·58·66·46셀 차이 0, `src_html()` = `_src` 9/9, `check_same_as_02`/`check_same_as_prev`/`check_same_as_probe` 통과. **`--src-only` 없이 부르면 노트북 출력이 지워지므로** 설명만 고칠 때는 `--src-only`(또는 `gapply.py`) → `run_section.sh … NN --no-exec`.
- **전체 마감 2026-09-30: 머리 줄 고침, 새 해시 `ed5c424006c2b41dd40c3d4861555fbe4180b8df7de2144febd7ef4f9a3f5b2c`**(검토 A-17·B-11 · 체크리스트 §2-13 6번). 8행 「이 챕터 01절 노트북에서 옮긴 함수는 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.」 → 「Ch 16 도구 파일 guardrails.py에서 옮긴 find_source_marks는 몸통 첫 줄 주석까지 글자 그대로 옮겼습니다.」 + 「이 챕터 01절·07절 노트북에서 옮긴 함수는 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.」(머리 설명 12 → 13줄). 1행(「앞 챕터와 이 챕터에서 배운 …」 — 함수 전부를 두루 가리킴, Ch 28 판단과 같음)·나머지 줄·함수 아홉 본문은 AST·글자 같음. 생성기 안 판: 02 `14ee39ca…` → `b59e8419…` · 07 `0c4ee4f9…` → `55f5890e…` · 08 = 디스크. 고친 생성기: `author_02.TOOLS_HEAD` 한 곳뿐(`author_07`·`08`의 `TOOLS`·`strip_later_imports`·02~09 `check_tools()`·02/07/08 쓰기 가드는 이 상수를 따라감, 챕터 안 해시 고정값 없음 — 앞서 Ch 26 머리 줄 고침으로 `author_02.DELEGATION_SHA`도 새 값). **뒤 챕터 고정값**: Ch 28 `author_04.HARNESS_SHA`·Ch 29 `author_01.HARNESS_SHA`를 새 값으로(설명 한 줄씩, 두 생성기 `--src-only`를 쓰기 없이 돌려 `check_tools` 통과·`_src` 바이트 같음). 조건 넷: (가) 노트북 아홉 마크다운·출력과 `_src`·HTML·README에 머리 글·판 해시 0 · (나) 아홉 생성기를 파일 쓰기를 가로챈 채(`.cache/final-close/2-tools-head/tools/dryrun.py`) `--src-only`(01~09)와 인자 없는 모드(02~09)로 돌림 → `_src` 아홉 바이트 같음, 02·07 가드 `skip`, 08 가드는 같은 글, 09 `disk == author_08.TOOLS`, 02~09 `check_tools()` 통과, `cells()`가 노트북과 56·56·64·66·66·64·58·66·46셀 같음 · (다) 아홉 절 모두 모델 셀이 있어 사본 실행 없이 가져오는 이름(02~09 — 6·6·5·4·4·5·6·5개, 01은 가져오지 않음)이 새 파일에 있고 함수 아홉 본문 AST가 옛 파일과 같음만 확인 · (라) 이 줄·handoff·계약 §4. 노트북 `code_sha256`·`outputs_sha256` 전후 같음.

## 12. 묶음·검사 (마감)

- **묶음**: `python3 textbook/part6/_build_index.py`(README·노트북·`chapter.json`·목차 줄·continuity-guide를 모두 고친 뒤 마지막에 한 번) → **`Part 6: 54 verified sections; 104 bundled files`**, `part6-practice.zip` `23a4d586…` → **`1a20c73c8dd533cc8e706f4be8ace65ebb6626412dd3a367001a414e50b7eddd`**(107항목, **Ch 27 13파일과 `continuity-guide.md`가 모두 디스크와 같음**, `__pycache__`·`workspace*`·`.env`·`.venv` 0). 공개 목록 둘은 바이트 같음(`collect_public_files.py` → `Explicit public files: 88; prerequisites: 13`).
- **묶음 실행 검사**(Part 6 `check_bundle_execution.py` — 목록은 Ch 24 01·Ch 28 01, **Ch 27은 없음**): `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink` 환경 변수만(스크립트 수정 0, `TMPDIR`은 세션 홈 — 맥 마운트 밖) → **PASS**(Ch 24 01 `7187f7a39f3f…`·Ch 28 01 `a09d959cecc4…`). `bundle-execution.json` `4f1cd14a…` → **`4f39acac93d1d36cbf9fa7a878bc9124d55a6177c342aa553249a09ce27ab061`**(`archive_sha256` 새 zip). Ch 27은 01만 요청 0이지만 모델 객체 셀이 키 없이 멈춰 목록에 넣을 수 없음(넣으려면 01에서 모델·키 셀을 빼야 함 — 강사 확인).
- **전달 검사**(Part 6 `check_delivery.py`): 117행 `llm-practice.zip`의 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤(알려진 일, `delivery-results.json` `3cc2d143…` 안 바뀜). 그 zip을 뺀 사본(`.cache/ch27-close/dx/check_delivery_nollm.py` — 바꾼 줄 셋: 루트·zip 목록·결과 파일 자리)은 **HTML 65 · 로컬 링크 1,435 · 누락 0 · 절 54 · 코드 셀 1,136 · 복습 213문항 오류 0 · SVG 218 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` 107항목(part6 노트북 54)** 통과.
- **화면 검사** `visual.cjs`(1280px·390px): **20행 PASS**(`textbook/_notebook/checks/ch27-deepagents/visual-results.json` + 스크린숏 넷 새로). Part 6 공용 `qa/visual-results.json`은 **Ch 27 줄만** 18 → 20(09 두 줄, 새 HTML 해시), `screens` 126 → 128, 다른 챕터 줄 그대로.
- **옛 검사 스크립트(고치지 않음, 돌려서 멈춘 자리만 기록)**: Part 6 `check_scope.py` — Ch 21 07 `Missing scope`에서 멈춤(Ch 27에 닿기 전, **`SECTION_COUNTS` ch27 8 ≠ 9**도 남음) · `check_figures.py` — Ch 21 `01-1-….svg`의 `.excalidraw` 짝 · `check_notebook_readiness.py` — `assert len(reports) == 47`(Part 6 노트북 54), **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림**(`b3d69e9c…`) · `check_visual_reports.py` — `ch22-middleware` · `textbook/qa/check_course_continuity.py`(시스템 파이썬 3.10에 `tomllib`이 없어 챕터 가상환경 3.12로) — 노트북 불변 조건·잠금 대조를 지나 **212행 `llm-practice.zip` Part 1 Stale**에서 멈춤(해시 허용 목록 단계는 Ch 27에서 멈추지 않음, `course-static-results.json` 안 바뀜).

## 13. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/01~09-*.ipynb` | 01~09절 · **마감(마크다운만)** | 실습 폴더(챕터 몫) — §1. 마감: 코드·출력·`executed_at` 그대로, 파일 01 `056ea2d4`→`5bd52b6f` · 02 `f031b310`→`bfdade30` · 03 `1eed50d9`→`cbd6fc87` · 04 `4ab0023c`→`0896cbd7` · 05 `d27f1ddf`→`d8d3c324` · 06 `c9927ab1` 그대로 · 07 `9d684fab`→`2c6423e4` · 08 `ac7b0a9f`→`70decb2f` · 09 `b64bcc16`→`084d2c03`. 도구 파일 그대로 `7a40d994…` |
| `labs/part6/ch27-deepagents/README.md` | 09절(09 단락) · **마감(전체)** | `acdc9201…`(원본) → `938c3227…` → **`28c360669383c1f6be0e20894efe1d14cbd6f8fc3944908a1adfd2881fcf9dca`**: 노트북 아홉, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 설치 판(아홉 절 넷 + 02·03을 뺀 일곱 절 `langgraph`), **모델 요청 01 0 · 02 2 · 03 7(교재 출력) · 04 3 · 05 3 · 06 5 · 07 3 · 08 4(교재 출력) · 09 4**, 예상 비용(요금표 어림, 청구 금액 아님), 키는 `.env`의 `OPENAI_API_KEY`에서만(학생 묶음이면 `part6-practice/`, 값 출력 0 — 01도 모델 객체 때문에 키 필요), 파일을 쓰는 곳(04 임시 폴더뿐 · 나머지 상태 칸 `files` · 08·09 메모리 체크포인터), 도구 파일 단락(규격 §2-7 고정 문장 뜻·함수 아홉·배운 절·가져오는 절), 절마다 하는 일, 09 단락(「공지 글」). `workspace*`·07 옛 사용량·옛 도구 이름 모두 뺌, 묶음 밖 파일을 가리키지 않음, 참 금지어 0(「체크포인터」 거짓 양성 말고) |
| `textbook/part6/ch27-deepagents/chapter.json` | 09절 · **마감** | 09 절(09절) · `objectives` 셋 → **넷**(옛 「조사 단위를 위임」·「deep research」·「비용과 한계를 기록」을 뺌 — §15), `hours` 그대로(`440ca1b9` → **`cc55e8e6`**, 보호 파일) |
| `textbook/part6/ch27-deepagents/index.html` | 09절 · **마감** | `_build.py`(목표 넷, `1b5c2c68` → `98837cf8`) |
| `textbook/part6/ch27-deepagents/qa/public-files.json` | 02·09절 | 도구 파일(02)·09 노트북(09). 옛 그림 줄은 원래 없음, HTML 줄도 원래 없음 — 마감 그대로(`80e9d01b`) |
| `textbook/part6/public-files.json` | 02·09절 | `collect_public_files.py` — 마감에서 다시 돌려 **바이트 같음**(`e43894fa`), `prerequisite-files.json`(`4c7f5a4b`) 같음 |
| `textbook/part6/_build_index.py` | **마감** | ch27 설명 「파일과 서브에이전트를 사용해 중간 자료가 남는 조사 에이전트를 만듭니다.」 → 「함수 create_deep_agent가 미리 붙이는 미들웨어와 도구를 조립 결과로 확인하고, 할 일 목록·파일 도구와 백엔드·긴 도구 결과 옮겨 두기·서브에이전트 위임을 호출 한도 두 곳과 요청 수 셈으로 실행한 뒤, 주어진 자료로 답하게 해 출처를 코드로 확인하고 권한 규칙과 사람 승인을 붙이며, 메모 파일 쓰기에 사람 승인을 켜고 끄는 실습을 합니다.」(시수 8·16 그대로, → `971a81e0`, 보호 파일) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | **마감** | Ch 27 설명 「파일·서브에이전트·컨텍스트 관리를 연결해 조사 과정을 구성합니다.」 → 「미리 조립한 Deep Agent의 기본 도구와 선택 기능, 할 일 목록·파일·옮겨 두기·서브에이전트를 보고, 출처 확인·권한 규칙·사람 승인을 붙입니다.」. **절 수 8은 그대로**(과정 전체가 실습 절을 빼고 세는 약속). 스크립트를 돌리기 전 옛 스크립트 출력이 지금 `index.html`과 바이트까지 같았고, 다시 만든 뒤 바뀐 줄은 Ch 27 행 하나(`→ 907ebc44` · `18479837` → `2c14ab24`, 보호 파일) |
| `labs/part6/continuity-guide.md` | **마감** | 13행 Ch 27 칸 「Ch27 파일·위임·컨텍스트 관리를 조립한 에이전트」 → 「Ch27 미들웨어를 미리 조립한 Deep Agent의 파일 도구·할 일 목록·옮겨 두기·서브에이전트 위임, 파일·출처 확인·권한 규칙·사람 승인을 한 에이전트에 모은 흐름」(→ `cb0e8bd1`, 보호 파일, 묶음에 들어감). **8행 「Ch27의 컨텍스트 관리」(05)·12행 「Ch27의 서브에이전트 위임과 완료 조건」(06 — 명세 글에 끝나는 조건을 적음)은 참이라 그대로**. 13행 셋째 칸 「최종 프로젝트의 조사 과정 구성」은 뒤 과정 몫이라 그대로 |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | 09절 + **마감** | §12 — `index.html` `651f22ff` → `ca9b9ff9`(Ch 27 섹션 설명 한 줄만), zip → `1a20c73c`, `integration-results.json` `9501518b` → `7eacc30b` |
| `textbook/part6/qa/bundle-execution.json` | **마감** | §12(`4f1cd14a` → `4f39acac`) |
| `textbook/part6/qa/visual-results.json` · `textbook/_notebook/checks/ch27-deepagents/visual-results.json`(+ 스크린숏 넷) | **마감** | §12 — 공용 파일은 Ch 27 줄만 18 → 20·`screens` 128(`→ 23a6919e`, 보호 파일), 챕터 결과 `→ 56c8c4cb`, 스크린숏 넷(index·01 × 1280·390) 새로 찍음(보호 파일) |
| `textbook/part6/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 다시 써서 실행 전 사본으로 되돌림(내용 변경 0, `b3d69e9c…`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(마감 뒤 `b4abdcfa…` — 09절 뒤와 같음) |
| **`qa/author_ch27.py` → `qa/upgrade/before/generators/blocked/author_ch27.py`** | 01절(막음) · **마감(`mv -n`)** | `7bc6c96d3e1e0a458f0499d42aaafa900aa14bb50ea7a973f201832ea43af8e4` 같음(01절이 첫머리에 `raise SystemExit`). 부르는 빌드·검사 스크립트 0(`grep` — 기록 문서·`before-manifest.json`뿐) |
| **`figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/_gen_figures.py`** | 01절(막음) · **마감(`mv -n`)** | `98641eb53491c3b9b8770596c1f8d162639c710b58ce67d05a8b7ece1c708e48` 같음. 부르는 스크립트 0. `before/generators/`의 두 원본 사본(막기 전 `45453725…`·`45d40ea2…`)은 그대로 |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | 진행표 Ch 27 행 한 줄 · 체크리스트 §2-13 6번에 덧붙임, §2-15 Ch 27 항목, §3·§4 Ch 27 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md` · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`render_mermaid.py`·`attach_figures.py`) · Part 6 옛 검사 스크립트와 `check_*`·`collect_public_files.py` · `textbook/qa/check_course_continuity.py` · Part 6 `_src/index.html`·`practice-start.md`(Ch 27 문장 참) · `textbook/part6/qa/final-artifact-hashes.json`·`notebook-executions.json`·`ch27-technical-review.md`·`language/`(옛 기록) · 실습 폴더 `pyproject.toml`·`uv.lock` · 도구 파일(해시 고정) · 삽화 · **Ch 28 이후 파일 전부**(Part 6 목차·묶음·공개 목록·기록·`continuity-guide.md` Ch 27 줄 말고) · `llm-practice.zip`·`delivery-results.json`.
- **파일을 지운 것은 없습니다.** 옮긴 것은 옛 생성기 둘(`mv -n`, 해시 같음). 옮긴 뒤 `_build.py`·`verify.py`·게이트·묶음 검사 통과. 마감이 기기 `/tmp`에 만든 것: `/tmp/ch27-close/`(모델 없는 재확인 `x_reject.py` + 검토 B의 `common.py` 사본, 12K).
- **보호 파일 238개(`before-manifest.json`)**: `manifest-changes.md` 「마감 뒤」.

## 14. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `deepagents==0.7.0`·`langchain==1.4.0`·`langchain-openai==1.6.0`·`python-dotenv==1.2.3`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`): `langchain-core 1.6.2`·`langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`·`langgraph-checkpoint 4.2.0`. 노트북 `%pip`은 아홉 절 넷 + 02·03을 뺀 일곱 절 `langgraph==1.2.11`(잠금 판).
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch27-deepagents`(잠금 판). 실행일 모두 2026-09-28(01 11:49 · 02 12:24 · 03 13:03 · 04 13:41 · 05 14:19 · 06 14:58 · 07 15:35 · 08 16:14 · 09 16:48 UTC — 마감에서 다시 실행하지 않음). 모델 `gpt-5.4-mini`.
- 설치판 소스 행(검토 A·B와 마감이 다시 확인): deepagents 0.7.0 `graph.py` 193~194·201~235·336·349~351·474~478·627·657·664·666~674·720·728·750~814·777·816~860(855 `_main_core_names`·860 `append_prompt_caching_middleware`·883 `_apply_custom_middleware`)·912~920·922~944(937 9999) · `middleware/subagents.py` 252~256·464~468·474~512·537~539·559~565 · `middleware/filesystem.py` 801~805·1156~1175(`supports_execution` — 04 b10을 마감에서 1175로)·1706~1795·1727~1733·2688~2707·2846 · `middleware/_message_eviction.py` 25~34·37~63(50~53 열 줄 이하 모든 줄 — 마감 B-1)·119~142 · `middleware/summarization.py` 249~286·642·1324 · `backends/filesystem.py` 97~136·495~530 · `backends/state.py` 56~80·98~122 · langchain 1.4.0 `agents/middleware/todo.py` 42·119~136·131·153~164·231~256·286~336(316 `len(...) > 1` — 마감 A-8) · `agents/middleware/human_in_the_loop.py` 337~354·405·456·459~464 · `agents/middleware/model_call_limit.py` 34·168~208·236~250 · `agents/factory.py` 1953~1964(짝 도구 메시지 있는 요청을 건너뜀 — 마감 B-4).
- 참고 자료(2026-09-28 확인, 검토 WebFetch): Deep Agents overview(agent harness·네 무리·0.7 할 일 계획 opt-in) · customization(기본 미들웨어 차례, **5번 prompt caching 「always registered; no-ops on models it does not support」**, 새 미들웨어는 `PatchToolCallsMiddleware` 뒤) · subagents(general-purpose 자동·같은 이름 교체·**`mode` `"isolated"`/`"fork"` — deepagents>=0.7.13**) · backends(`virtual_mode=False` 표기 ↔ 설치판 `True`) · context-engineering(20,000토큰·앞 10줄 미리보기 ↔ 설치판 앞뒤 다섯 줄) · deep-research(Tavily 예) · human-in-the-loop(Deep Agents·LangChain — **두 문서 예 모두 `version="v2"`**) · permissions · deepagents 0.7.0 릴리스 · PR #5009(5,395 → 1,895, −65% — 셀에서 뺌). OpenAI `gpt-5.4-mini` 요금(입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰, 요금표 2026-09-17).

## 15. 강사 확인 대상

1. **제목 말**: 챕터 「DeepAgents — Harness 계층」 · 02 「create deep agent」 · 03 「플래닝」·「프롬프트」 · 05 「오프로딩」 · 07 「출처 검증형 deep research」(「검증」) · **09 긴 제목**(「DeepAgents 실습: 메모 파일 쓰기에 사람 승인을 켜고 끄기」)·슬러그. 슬러그 01은 Ch 26 05 b8이 링크해 고정, 챕터 제목은 Ch 6 01 표와 같음.
2. **`chapter.json` 학습 목표 셋 → 넷**(01 조립 · 02~06 실행과 요청 수 셈 · 07~08 출처 확인·권한·승인 · 09 실습, 「deep research」·「비용과 한계를 기록」·「조사 단위를 위임」을 뺌, `hours` 그대로) · `_build_index.py`·`build_index.py`·`continuity-guide.md` Ch 27 문구 · README 다시 쓴 범위.
3. **「기본 미들웨어 다섯」**(마감 A-2 — 챕터 리드 결정으로 정의대로 셈. 검토자는 「넷을 지키고 한 문장」을 권했음) · 삽화 01-5 설비 넷을 「이 과정 모델에서 일하는 넷」으로 읽게 한 것(다시 만들지).
4. **「안내 글」 한 뜻**(마감 A-14·B-7): 03 「할 일 설명 글」·09 「공지 글」로 가름, 코드 속 말(03 출력 라벨·`lookup_rule` 주석·09 요청 글 머리말)은 다음 재실행 몫으로 결과 읽기에서 가름.
5. **코드 양**(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」): 코드 줄 252 → 1,461(01~08 131·132·182·180·183·189·148·194 + 09 122) + 도구 파일 66 · 코드 셀 36 → 253. 03·04는 02 셀(규정 글·도구·명세·기록 훅·비용)을 셀 글 그대로 다시 적고, 03은 01·02 결과를 되풀이함(A-11 — 셀 합치기는 03 재실행, 모델 요청 7번 안팎). 01 4절 인자 다섯 셀을 줄일지.
6. **`tools_only_graph`를 05~08 노트북에 04 셀 글 그대로 다시 적은 것**(규격 §2-7 3번 ↔ 6번 충돌): **예외로 둠**(검토자 권고) — `handoff.md` 허용 문법 목록에 한 줄. 도구 파일로 옮기면 `langgraph` 가져오기가 생겨 02·03 설치 셀과 두 모델 절 재실행. 08 `review_graph`도 같은 판단.
7. **01이 06보다 먼저 서브에이전트 명세와 general-purpose 교체를 가르친 설계**(01 새 말 6·코드 셀 26 — 한 시간 강의에 무거움).
8. **03 6절 「값 바꿔 보기」가 두 값(`system_prompt=`·할 일 미들웨어)을 함께 바꾼 것**(본문·b7에 공개) · 우리 시스템 메시지 글이 `write_todos`를 먼저 쓰라고 정함.
9. **07 교재 출력이 자료와 어긋난 답(무인 반납함 자료를 읽지 않음)을 싣는 것**(5/5 + 두 커널, 입력 그대로, 「판정이 보지 못하는 것」의 예로만 — 원치 않으면 07 재실행으로 별도 값 바꿔 보기) · W2·서브에이전트 0 · 4절 손 글 둘은 흔들림 확인 뒤에 더한 예.
10. **08**: 조립 범위(할 일 목록·서브에이전트·옮겨 두기 뺌) · 사람의 답은 코드가 넣은 승인 · 새 API 결정 목록 · 승인 작은 그래프가 거절을 막지 못함을 글로만 경고(마감 B-4 — `reject` 셀을 더하려면 08 재실행).
11. **09**: 조립 범위 · **실행 1이 08 6절과 같은 모양**(찾기 단계만 없음) · 「다시 읽지 말고」 문구 · 코드가 넣은 `approve` · 값 `{}` · 복습 4(실행하지 않은 경우를 소스로 답함) · 챕터 공개 목록에 HTML 줄 없음 · **그림 설계표를 렌더 뒤에 적은 차례**(§20).
12. **삽화**: 01-5 양옆 여백 · 02-5 플러그 둘 · 06-5 창 위치 · 08-6 널빤지(글로만 맞춤 — 다시 만들지) · **작업 조회 결과의 모델 표시 `nano_banana_2`와 거래 기록 「Nano Banana Pro」가 다름**(기록만).
13. **도구 파일 머리 설명**(A-17·B-11 — 해시 고정으로 그대로, Ch 24·25·26과 함께 전체 마감).
14. **01을 Part 6 묶음 실행 검사에 넣을지**(요청 0이지만 모델 객체 셀이 키 없이 멈춤 — 넣으려면 모델·키 셀을 빼야 함).
15. 새 용어 14(6·1·0·1·2·0·2·2·0)와 정의 · 새 말 「Deep Agent」를 영어 그대로 둔 것 · 교재용 규정 글·자료 셋.
16. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: 삽화 직접 판독, Windows·macOS 실제 실행, 학생 `uv sync --locked` `.venv` 첫 셀, `check_scope.py` 등 옛 검사 넷).

## 16. Ch 28이 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 말: Deep Agent·기본 미들웨어(다섯)/선택 기능·파일 도구·general-purpose 서브에이전트·할 일 목록·서브에이전트 명세(01) · 백엔드(02) · 기준 폴더(04) · 옮겨 두기·안내 글(05) · 주어진 자료로 하는 조사·출처 확인(07) · 도구 실행 경계·결정 목록(08).
- 사실(참, 출력 근거): `create_deep_agent`는 `create_agent`에 미들웨어를 미리 골라 붙인 그래프(실행 한도 9999) · 도구와 노드를 미들웨어가 가져옴 · 모델에게 보내는 도구 목록은 등록된 도구와 다를 수 있음(`execute` 빠짐) · 서브에이전트 요청은 바깥 결과 목록에 없음 · 요청 수 = 도구를 요청한 응답 수 + 1(서브에이전트를 부르지 않은 실행).
- **Ch 28 01 b3 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다」는 뜻으로 참**(01 조립·04 파일·06 위임). 「하위 작업」은 Ch 28의 말(Ch 27 본문은 「위임」·「서브에이전트」 — Ch 28 개선 때 한 구절로 맞출지는 Ch 28 몫). Ch 27 09 b8 「Ch 28 01절에서는 도구를 같은 프로그램 밖의 서버로 옮겨 …」는 Ch 28 01 b2와 맞음.

### 전제하면 안 되는 것 (Ch 28 파일은 고치지 않았습니다)

1. **Ch 27의 Deep Agent는 모두 기본 백엔드 `StateBackend`(상태 칸 `files`)로 파일을 다뤘고, 디스크에 쓴 것은 04절의 임시 폴더뿐**입니다. 실습 폴더 `workspace*`는 옛 판의 흔적이고 새 판 노트북은 쓰지 않습니다. Ch 27이 만든 파일을 Ch 28이 읽는다고 전제하지 말 것(파일 계약 없음).
2. **사람 승인은 `interrupt_on`(→ `HumanInTheLoopMiddleware`)과 결정 목록 `Command(resume={"decisions": [...]})`만** 실행했습니다(08·09, 결정은 `approve`만). **08의 승인 작은 그래프는 거절·대신 답하기를 넣어도 쓰기를 실행**합니다(실제 에이전트는 `agents/factory.py` 1953~1964행에서 건너뜀). 사람의 답은 늘 코드가 넣은 값입니다.
3. **권한 규칙은 파일 도구 안 판정**이라 우리 도구·명령 실행·백엔드 직접 호출에는 걸리지 않고, 같은 이름 `FilesystemMiddleware`를 넣으면 사라집니다(01·05·08). **MCP 도구(Ch 28)에 Deep Agents 권한 규칙이 걸린다고 전제하지 말 것.**
4. **호출 한도는 invoke 한 번마다 세고**, 승인으로 이어 가는 invoke에서 0부터 셉니다. 요약 요청은 상한 식 밖이고, 한 응답의 `task` 요청 수는 막지 않습니다(§8).
5. **기본 미들웨어의 다섯째 `AnthropicPromptCachingMiddleware`는 이 과정 모델(OpenAI)에서 아무 일도 하지 않습니다.** 문자열 모델(`"openai:gpt-5.4-mini"`)을 넘기면 Responses API·temperature 없음으로 바뀌므로 모델 객체를 넘기세요(01 b7).
6. **웹 검색·원격 도구·비동기 서브에이전트·스킬·장기 메모리는 실행하지 않았습니다**(01은 조립만). 07 「deep research」는 상태 칸에 넣은 교재용 자료만 찾았습니다.
7. **도구 파일 `harness_tools.py`는 Ch 27 실습 폴더에만** 있습니다(`7a40d994…`, 가져오기 0, 머리 설명은 옛 두 줄). Ch 28 실습 폴더와 잠금이 다르면 파일째 가져오지 말 것.
8. **말**: 「경로」(→ 파일 위치)·「반환」·「검증」(제목 밖)·「오프로딩」·「플래닝」·「프롬프트」(제목 밖)·「재개」·「인터럽트」·「캐시」 단독은 본문 0. **「안내 글」은 05 뜻 하나**(옮겨 둔 뒤 남는 도구 메시지 글). 09 소재(자료실 안내 메모·`/reports/notice.md`)를 Ch 28이 이어 쓴다는 약속은 없습니다.

## 17. 뒤 챕터 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 27 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 28(대기) | 01 `_src` b3 | 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다」 | 뜻으로 참(01·04·06) — 「하위 작업」은 Ch 27 본문 말이 아님(06 「위임」·「서브에이전트」) | Ch 28 개선 때 「하위 작업」을 Ch 27 말(서브에이전트 위임)과 맞출지 확인 |
| Ch 28(대기) | 권한·승인을 다루는 자리 | — | Deep Agents 권한 규칙은 내장 파일 도구에만 걸림 · 승인 작은 그래프는 거절을 막지 못함 | MCP 도구 권한을 Deep Agents 권한으로 설명하지 말 것(§16-3) |
| Ch 24(완료) | 요약 §15 192행 「도구 실행 경계」 | — | 08 b3·b4로 참이 됨(모델이 고른 `write_file` 앞 승인 — `HumanInTheLoopMiddleware` 장면) | 없음 |
| Ch 26(완료) | 05 b8(01 슬러그·「미리 묶어 둔 DeepAgents」) · 요약 §13 「Ch 27 01·03·06 b3 참」 | — | 참(01 b3 「Ch 26은 위임 구조를 다뤘고」·03 b3 완료 조건·06 b3 완료 조건 — 06은 명세 글에 끝나는 조건) | 없음 |
| Ch 6(완료) | 01 계층 지도 표(「DeepAgents — 긴 작업에 필요한 기능을 갖춘 하네스 — Ch 27」) | — | 참(챕터 제목 그대로, 01 b4가 이어 씀 — Deep Agent는 도구 루프를 품지만 루프까지 미리 조립한 틀이라 하네스 자리, 마감 A-5) | 없음 |
| Part 6 | `continuity-guide.md` 8·12·13행 | (마감에서 13행 고침) | 8·12 참 | 없음 |
| Part 6 목차 | `_src/index.html`·`practice-start.md` | — | 참 | 없음 |
| 전체 마감 | `llm-practice.zip` 안 Ch 27 | 옛 판(노트북 여덟·옛 README — 도구 파일·09 없음) | `part6-practice.zip`은 새 판 13항목이 디스크와 같음 | 전체 묶음 재생성 때 Ch 27 13항목 대조 |
| Part 6·7 기록 | `textbook/part6/qa/final-artifact-hashes.json`·`notebook-executions.json`·`notebook-readiness.json`·`ch27-technical-review.md` | Ch 27 옛 해시·옛 판(09 없음) | 기록 파일(계약·검사 입력 아님) | 고치지 않음 — Part 6 마감 때 |

## 18. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-15)

1. **옛 그림 스물넷 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~8, 본문 참조 0, `08-흐름.caption.md`에 「거부」, 사본 `qa/upgrade/before/figures/`, 챕터 공개 목록 줄은 원래 없음). Part 6 옛 검사 `check_figures.py`가 `.excalidraw` 짝을 요구하는 것과 함께 정할 것.
2. **실습 폴더 `workspace`·`workspace-05`·`workspace-08` 삭제 승인**(옛 04·05·07·08이 쓴 9파일 — 새 판은 쓰지 않음, 읽는 코드 0, 사본 `before/workspace*/`, 보호 파일 목록에 있음).
3. **`gates-wip-*.json` 열아홉 삭제 승인**(`gates-wip-01-01`~`09-09`·`01`~`09`·`ch27-after09` — `gates-after.json` 9/9로 갈음, 절 번호 아홉은 마감 `run_section.sh --no-exec`가 다시 씀).
4. **캐시·임시 삭제 승인**: `qa/__pycache__/author_ch27.cpython-312.pyc`(09-10) · `qa/upgrade/__pycache__/`(`author_02`·`author_08` cpython-310 둘 — 09 작업 때) · 실습 폴더 `notebooks/__pycache__/harness_tools.cpython-312.pyc`(03 A 13:03:47 — 마감은 만들지 않음) · 실습 폴더 `labs/part6/ch27-deepagents/.venv`(macOS 판 215MB) · `.cache/vm/venv-ch27-deepagents`(292MB) · `.cache/ch27-0N-view/`(N=1~9, 약 14MB) · `.cache/ch27-close/`(마감 전 사본 `pre/`·확인 스크립트 `tools/`·치환 목록 `reps/`·옛 검사 결과 `oldcheck/`·`llm-practice.zip`을 뺀 전달 검사 사본 `dx/`·로그 `log/`·그림 확인 사본 `view/`, 약 4MB) · 기기 `/tmp/ch27-prep`·`/tmp/ch27-01`~`/tmp/ch27-09`(약 100MB)·`/tmp/ch27-close` · `/tmp/reviewA27`·`/tmp/reviewB27`(검토 재현 파일) · 기기 세션 임시 폴더 `$TMPDIR/ch27-04-*`(16개 — 04 노트북·흔들림 확인이 만든 임시 폴더, 노트북은 지우지 않음) · 공용 `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`·`/tmp/uv-cache`·`/tmp/pw`·`/tmp/pw-browsers`·`/tmp/npm-cache-ch26close`(Ch 26 마감이 설치, 마감이 그대로 씀).
5. **코드 쪽 다음 재실행 몫**(마감은 코드 셀을 한 글자도 바꾸지 않음): **03 셀 20·54 `print` 라벨**(`안내 글 첫 줄:`·`안내 글 글자 수:`·`할 일 안내 글로 끝나는가:`·`우리 글 + 빈 줄 + 안내 글과 같은가:` → 「할 일 설명 글」)과 **셀 20 첫 줄 주석**(검토 A-14) · 03 셀 16 라벨 `상태 칸에 넣을 수 있는 값:`(→ 항목의 `status` 값, A-9) · **02·04·05·06 `lookup_rule` 주석 「정해 둔 안내 글」**(→ 「정해 둔 글」, B-7 — 02·04·05·06 모델 절 재실행) · **09 코드 문자열 `request_text` 머리말 「안내 글:」·`memo_text` 속 「안내 글」**(→ 「공지 글」, B-7 — 09 흔들림 확인·새 커널 두 번) · **04 셀 42 주석 「(02절 셀과 한도만 다름)」**(03 셀 글 — A-13) · 08 셀 58 주석 「(07절 6절 셀에 첫 줄 run_new만 더함)」(주석도 바뀜 — B-9) · **03 셀 12·14 합치기**(A-11, 강사 결정) · 코드 줄 줄이기 후보(§15-5). 다시 실행하면 새 커널 두 번 대조·교재 출력 인용 다시 대조·zip 다시 만들기.
6. **도구 파일 머리 설명**: §11(Ch 24·25·26·27 한 항목 — 최종 점검표 §2-13 6번).
7. **Part 6 옛 검사 스크립트(고치지 않음)**: `check_scope.py` `SECTION_COUNTS` ch27 **8 ≠ 9**(Ch 21 07에서 먼저 멈춤) · `check_figures.py`·`check_notebook_readiness.py`(47 ≠ 54 — 결과 파일 되돌림)·`check_visual_reports.py` · `textbook/qa/check_course_continuity.py`(212행 `llm-practice.zip` Stale, 시스템 파이썬에 `tomllib` 없음) — §12.
8. **`llm-practice.zip`**: §12 · 안 Ch 27은 옛 판(§17).
9. **기록 파일의 옛 해시(계약·검사 입력 아님 — 고치지 않음)**: `textbook/part6/qa/final-artifact-hashes.json`(Ch 27 줄, 옛 생성기 옛 자리 포함) · `notebook-executions.json`·`notebook-readiness.json`(Ch 27 여덟 — 09 없음) · `ch27-technical-review.md`·`language/`(옛 감사) · **Part 6 공용 `visual-results.json`**: Ch 27 줄은 마감에서 20줄로 새로 모음, 다른 챕터 줄은 옛 HTML 해시 그대로 — Part 6 마감 때 다시 모을 것. **`textbook/_notebook/build_index.py`** 절 수(Ch 27 8 — 실습 절 뺀 수) — 전체 목차 마감 때.
10. **과정 요약(누적 문서 몫)**: Ch 27 용어(§4 — 특히 기본 미들웨어 다섯·「안내 글」 한 뜻·상태 칸 ↔ 항목의 `status` 값·출처 확인·결정 목록)와 안전 규칙·상한 식(§8), 도구 파일 `harness_tools.py`(`7a40d994…`, 함수 아홉)는 과정 요약에 아직 넣지 않음(Part 6 마감 오케스트레이터).
11. **옛 기록 파일**: `qa/research.md`·`qa/technical-review.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용 그대로 — 뒤 둘은 끝에 「마감」 절) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음) · `figures/01-5-….prompt.md`의 「설비 넷 = 기본 미들웨어 넷」(생성 기록 — 그대로).
12. **실습 폴더 잠금**: `pyproject.toml`·`uv.lock` 그대로. 바꿀 것 없음.
13. **2차 검토**: 두 검토의 「확인하지 못한 것」과 §15-16.

## 19. 검토 1차와 반영 (2026-09-28 마감)

- 판정: **A(01~04·공통) 중 6 · 하 13**, **B(05~09·마감 몫) 중 4 · 하 10**. 합 **[중] 10 · [하] 23**, [상] 0.
- **[중] 10건 모두 반영**(코드 셀·게이트를 건드리지 않고 글·그림·기록으로, 코드 속 말은 다음 재실행 몫):
  - **A-1** 01 b7 문서 값 `forked` → `"fork"`·deepagents 0.7.13 이상 요구(b10·진단 §6·인계 금지어 줄도).
  - **A-2** 「기본 미들웨어 넷」 → **다섯**(챕터 리드 결정 — 검토 권고 「넷 + 한 문장」과 다름): 01 용어 표·실제 조립 표(새 행)·「다시 세면」·비유·그림 읽기·01-1 그림(다시 렌더, 노트북 첨부 교체)·캡션·도식 읽기·셀 1·27·43·b10, 05 셀 43·b3, 02 셀 37(「짝 맞추기 미들웨어 뒤」). 코드 출력에 넷을 세는 자리는 없음.
  - **A-8** 03 「둘 넘게」 → 「둘 이상」 네 곳(셀 15·51·b6·b7).
  - **A-9** 03 그래프 칸은 「상태 칸 `todos`」, 항목은 「항목의 `status` 값」(b3·b4·b5·b6·b7·복습 1·셀 17·19·41·03-1·03-4 캡션), 출력 라벨 풀이 문장.
  - **A-14·B-7** 「안내 글」 한 뜻 — 03 「할 일 설명 글」(`_src`·노트북·그림 넷) · 02·04 「정해 둔 글」 · 09 「공지 글」 · 05 첫 사용 앞당겨 알림·`lookup_rule` 주석과 다르다는 문장 · 09 머리말 풀이(셀 17·b7). 09 meta 「새 용어 0」 참.
  - **A-15·B-12** 실습 폴더 README 전체 다시 씀(§13).
  - **B-2** 06-3 — `06-probe.md` §0 그림 라벨 규칙이 막는 값(안쪽 도구 차례)이라 라벨에서 빼고 다시 렌더, 도식 읽기·캡션·alt·`06-figures.md`(규칙은 바꾸지 않음).
  - **B-4** 08 셀 35·b7에 승인 작은 그래프 경고(거절·대신 답하기도 쓰기가 실행됨 — 마감이 노트북 밖에서 모델 없이 다시 확인).
- **[하] 23건 처리** — 20건은 권고대로 글·그림·기록을 고침: A-3(01-1 근거 갈래) · A-4(짝 맞추기 풀이·Responses API·기본 미들웨어 차례) · A-5(하네스 자리 한 문장) · A-6(02 b6) · A-7(샌드박스·하네스 프로필·04 b10 1175행) · A-10(03 b6 인자 형식) · A-12(04 보관 방식) · A-13(04 진단 다음 재실행 몫) · A-16(01 b4·셀 55 요약 예외) · A-18(03 진단 pyc) · A-19(02 probe §0 머리) · B-1(05 미리보기 셋) · B-3(07 제목 풀이) · B-5(08 b3) · B-6(08 b10 `version`) · B-8(09 b6·셀 43) · B-9(08 셀 57·09 셀 25) · B-10(§20) · B-13(확인 — 이미 완결, 고칠 것 없음) · B-14(`objectives`·continuity-guide·`check_scope.py` 기록). **코드나 도구 파일을 바꿔야 하는 3건은 권고의 「지금은 기록」 쪽대로 기록만**: **A-11**(03 셀 합치기 — 03 재실행, 강사 확인) · **A-17·B-11**(도구 파일 머리 설명 — 해시 `7a40d994…` 고정, Ch 24·25·26 선례, 전체 마감 한 항목).
- **검토의 「사람이 정해야 할 것」 처리**: A 1(기본 미들웨어 수 → 다섯) · A 2·B 2(안내 글 → 03·09 쪽을 바꾸고 코드 문자열은 둠) · A 3·B 1(`tools_only_graph` → 예외) · A 4·5·6(01 설계·코드 양·03 두 값 → 그대로, 강사 확인) · A 7·B 7(README → 마감에서 전체) · A 8(머리 설명 → 그대로) · B 3(`reject` → 글 경고만) · B 4(06-3 → 라벨에서 뺌) · B 5(07 틀린 답 → 그대로, 강사 확인) · B 6(09 복습 4·조립 → 그대로 + B-8 한 문장).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자 — 모두 같음): 01 `0ffa59d9d8de`/`36d9986576b5` · 02 `6f5358591ac9`/`7691ccfa1d3a` · 03 `2da25ac9de6d`/`f48621ade915` · 04 `b3c842d492d8`/`2b52741582d3` · 05 `aa6c1b13ebc2`/`5fd97f33cfb9` · 06 `4469ff95f584`/`1a587e750d3e` · 07 `edb511130a77`/`184016bb214b` · 08 `33c153ec1ba5`/`d88cc3b198b6` · 09 `53f6ef6bf2fd`/`b89a469ecd40`. `executed_at` 아홉 모두 같음, `metadata.verification.code_sha256`과 다시 계산한 값이 같음. 파일 해시만 바뀜(06은 파일도 그대로): §13 첫 줄.
- 고친 방법: `.cache/ch27-close/tools/gapply.py`(생성기 문자열 치환 — 치환 수가 다르면 멈춤) · `smartrep.py`(03 「안내 글」·「결과 칸」·「둘 넘게」 일괄 — 코드 셀 상수 `r'''#…`·백틱·`<code>` 안은 건드리지 않음, 바뀐 자리를 앞뒤 글과 함께 출력) → 두 도구 모두 바뀐 생성기를 실행해 **코드 셀이 노트북과 한 글자라도 다르면 멈추고**, 달라진 마크다운 셀만 노트북에 옮긴 뒤(첨부·메타데이터 그대로) `src_html()`로 `_src` → `capsync.py`(캡션 파일 = 생성기 `FIGn_CAP`) → `.mmd` 고친 여섯만 `render_mermaid.py --only … --force` → `run_section.sh … NN --no-exec` 아홉 번 → `chain27.py`(생성기 대조 사슬). 마감이 더한 문장의 참 금지어 0, 게이트 G6 0.
- 검사: `upgrade_gates.py … --label after` **9/9 PASS, G1~G7 0** · AST 따로 금지 문법 0(허용 표시 `@wrap_model_call` 다섯 셀·06 `@before_agent`, 도구 파일 `.get` 둘) · `verify.py --chapter` **PASS 9 sections / 253 code cells (max 13 lines)** · 빌드 HTML 열 `{{`·`[[` **0건** · `visual.cjs` **20행 PASS** · Part 6 `check_bundle_execution.py` **PASS** · Part 6 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(그 zip을 뺀 대조 통과) · 옛 검사 넷·과정 연속성 검사는 Ch 27 전에 멈춤(§12) · 보호 파일 238개 — `manifest-changes.md` 「마감 뒤」.

## 20. 절차 메모

- **09 그림 설계표를 렌더·삽화 뒤에 적음**(검토 B-10 — `09-figures.md` 차례 줄·09 진단 §10에 스스로 적음). 렌더 뒤 라벨·색 변경 0, 새 커널 B는 그림 전, 라벨은 `09-probe.md` §0 그림 라벨 규칙(첫 요청 전)과 맞음. Ch 24 B-14와 같은 [하] 기록 처리.
- **흔들림 확인 §0 작성 시각**: 02~09 모두 §0 시각이 첫 요청 기록보다 앞선다고 적었고(검토 B 12 대조), 02 §0 머리의 앞뒤가 부딪히던 표현만 마감에서 고침(A-19). 파일 수정 시각은 결과를 붙인 뒤 하나뿐이라 §0 작성 시각 자체는 따로 확인할 수 없음(Ch 26 A-8 교훈).
- **03 A 실행의 바이트코드**: 03 교재 출력 A가 `PYTHONDONTWRITEBYTECODE` 없이 돌아 실습 폴더에 pyc 하나를 씀(A-18) — 마감의 모든 파이썬 호출은 `PYTHONDONTWRITEBYTECODE=1`.
- 마감은 기기 셸 한 곳에서만 작업(`mcp__remote-devices__device_bash`), 셸 호출마다 `timeout 165~170`. 모델 요청 0 · 삽화 생성 0 · 파일 삭제 0.
