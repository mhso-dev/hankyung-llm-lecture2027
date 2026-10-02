# Ch 21 create_agent — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part6/ch21-create-agent` 01~06절(품질 개선) + **07절 챕터 끝 실습 절 신설**(`07-create-agent-실습`), 노트북 `labs/part6/ch21-create-agent/notebooks/01~07-*.ipynb`, 도구 파일 `notebooks/runner_tools.py`, 계약 파일 `data/rag-comparison.json`(Ch 29 04가 읽음).
- 기간: 2026-09-25(준비 조사 · 01~06절 개선 · 07절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 여섯 절 합계 **251**(G1 37 · G2 11 · G4 1 · G5 44 · G6 140 · G7 18 — 01 46 · 02 39 · 03 41 · 04 31 · 05 31 · 06 63, `gates-before.json`) → 마감 뒤 **7/7 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 396·389·355·355·379·411·347 = **2,632**).
- 코드 셀 23·28·24·24·26·31·24 = **180**(`verify.py --chapter` → `PASS 7 sections / 180 code cells (max 16 lines)` — 16줄은 05·06 가져오기 준비 셀). Mermaid **27장**(01~06 넷씩 · 07 셋), 삽화 **7장**(절마다 하나, Higgsfield 14크레딧, 마감 0), 복습 문제는 HTML에만.
- 모델 요청(노트북 한 번씩, 교재 출력 기준): 01 5 · 02 6 · 03 4 · 04 0 · 05 5(+임베딩 6) · 06 15(+임베딩 7) · 07 4 = **모델 39번 + 임베딩 13번**(모두 `gpt-5.4-mini`·`text-embedding-3-small`). 모델이 도구·검색 도구를 부르는 수에 따라 달라질 수 있음. 노트북마다 요금표 어림 예상 비용 0.01달러 아래(청구 금액 아님). **04는 모델 요청 0이지만 모델 객체를 만들 때 키가 필요**(`check_bundle_execution.py` 대상 아님 — Part 6 묶음 실행 검사는 Ch 24·28만).
- 화면 검사 `visual.cjs`: HTML **여덟 개**(일곱 절 + `index.html`) × 1280px·390px = **16행 PASS**.
- **마감에서 다시 실행한 노트북: 01·02·03·04**(설치 셀에 `numpy==2.5.3` — §15). 05·06·07은 `code_sha256`·`outputs_sha256`·`executed_at` 전후 같음(마크다운과 05 첨부 그림만). **06은 Ch 29 04 계약 때문에 다시 실행하지 않는 노트북**입니다.
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 20 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-25)」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」) → 검토 `review-round1-A.md`(01~03·공통)·`review-round1-B.md`(04~07) → 흔들림 확인 `01·02·03·05·06·07-probe.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 create_agent와 ReAct 루프 (experiment) | **`from langchain.agents import create_agent`** · `create_agent(model, tools=[lookup_policy], system_prompt=system_text)` → `CompiledStateGraph`(모델 **객체**를 넘김 — 글자면 기본 설정으로 새로 만듦, `factory.py` 995~996행) · `agent.invoke({"messages": [HumanMessage(…)]})` · `agent.get_graph().draw_mermaid()` · **설계 객체 `agent.builder`**·`.nodes`·`.edges`·`.branches`·**`.channels`**·**`.nodes["tools"].runnable`**·**`.branches[노드][조건 함수].ends`** · 결과 키 `['messages']`·상태 칸 `['messages', 'jump_to', 'structured_response']` · 조건 함수 `model_to_tools`·`tools_to_model`(점선, `tools_condition` 안 씀) · 여럿 담기 인자 없음 → 한 응답 요청 둘 | **`agent_row`**(02가 도구 파일로 옮김) | 에이전트를 만드는 함수(create_agent) · 에이전트 그래프 · ReAct 루프 (3) |
| 02 구조화 출력 두 전략 | **`response_format=`** · **`ToolStrategy(PolicyAnswer)`**·**`ProviderStrategy(PolicyAnswer)`**·양식 클래스 그대로(`from langchain.agents.structured_output import …`) · 결과 칸 **`structured_response`**(양식 객체, `model_dump`) · 양식 클래스 `PolicyAnswer(BaseModel)`(칸 `topic: Literal[…]`·`answer`, `Field(description=)` — Ch 19 02 범위) · `model_json_schema()["properties"][…]["enum"]` · 모델 객체 속성 **`profile`**(「기능 표」) · 도구 전략 그래프의 갈 곳 `tools_to_model` `['model', '__end__']`·`model_to_tools` `[…, 'model']` | **`print_branches`**(03이 도구 파일로 옮김) | 도구 전략(ToolStrategy) · 제공자 전략(ProviderStrategy) · 양식 도구 (3) |
| 03 AgentState와 context_schema | **`from langchain.agents import AgentState`**(`langchain.agents.middleware`와 같은 클래스 — 출력 `True`) · **상태 형식 확장 `class LibraryState(AgentState): ticket_no: str`** → `state_schema=` · **실행 정보 형식 `class MemberContext(TypedDict)`** → **`context_schema=`** · **`invoke(…, context={…})`** · 도구 매개변수 **`runtime: ToolRuntime[MemberContext]`**(`from langchain.tools import ToolRuntime`) · `runtime.context["member_id"]` · 도구 명세에서 `runtime`이 빠짐(`args` `{}`, `convert_to_openai_tool`로 명세 출력) | 도구 `check_my_loan`(노트북) | 라이브러리 상태 형식(AgentState) · 실행 정보(context) · 실행 객체 표시(ToolRuntime) (3) |
| 04 0.x에서 1.x로 마이그레이션 | **옛 함수 `from langgraph.prebuilt import create_react_agent`**(langgraph-prebuilt 1.1.0에 사용 중단 경고와 함께 남음, **만들기만 — 모델 요청 0**) · `prompt=` ↔ `system_prompt=` · `inspect.signature(…).parameters` · `with warnings.catch_warnings(record=True) as …:`·`warnings.simplefilter("always")`·`issubclass(…, DeprecationWarning)` · `graph.get_input_jsonschema()["properties"]` · `builder.managed`(`remaining_steps`) · 옛 그래프 `response_format` → 노드 `generate_structured_response`(소스로만 모델 요청 한 번 더) | `print_arrow_lines`(노트북) | 옮기기(마이그레이션) · 옛 함수(create_react_agent) · 사용 중단 경고(DeprecationWarning) (3) |
| 05 retriever를 도구로 전환 | Ch 14 자료 읽기(자리 찾기 셀 `candidates` + `for`·`break`) · `OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)`·`embed_documents` · **`@tool search_documents(query: str)`**(몸통 `search_hits` + 「[문서 ID] 글」 세 줄) · `convert_to_openai_tool` 명세(03에서 처음) · 도구 호출 요청의 인자 `query` = 검색어 · 같은 요청을 `도구.invoke(요청)`으로 다시 부르기 · 다시 검색은 시스템 메시지 글의 규칙(코드 제한 아님) | **`cosine_similarity`·`cosine_distance`·`rank_by_distance`·`print_ranked`·`search_hits`**(Ch 14 도구 파일에서 옮김 — NumPy) | 검색 함수(retriever) · 검색 도구 · 검색어(query) (3) |
| 06 같은 평가셋으로 RAG 비교 | 고정 흐름 `search_documents.invoke({"query": 질문})` + `model.invoke(요청 글)` ↔ 에이전트 흐름 · Ch 11 정답 문서 자리 · **Ch 15 02 근거 충실도 판정**(판정 머리글 그대로, `rag-judge-v1.0.0`) · **`time.perf_counter()`**(계약 칸 `agent_latency_s` 하나만 — 챕터 유일한 걸린 시간 재기) · **`with open(…, "w", encoding="utf-8")` + `json.dumps(…, ensure_ascii=False, indent=2)`**(계약 파일 쓰기)·`json.loads` 다시 읽기 · `sum_usage`의 `requests` → 계약 키 `model_calls` | **`find_gold_rank`·`build_judge_prompt`·`judge_once`**(Ch 15 도구 파일에서 옮김) · `doc_ids_in`·`search_trace`(노트북) | 고정 흐름 · 에이전트 흐름 · 비교 기록 (3) |
| 07 create_agent 실습 | **새 API 0**(01~06 이름 + Ch 2 문법 — 8절 `and` 하나가 01~06에 없던 Ch 2 문법, 마감 B-13) | 0(양식 클래스 `LoanAnswer`만 새로 적음 — 02와 같은 모양) | 0 |

- 새 용어 합계 **18개**(절 meta 「새 용어」 3·3·3·3·3·3·0).
- **이 챕터 주제라서 허용한 문법**(챕터 리드 결정 7): 맨 `@tool`·매개변수 `: str`·독스트링 · 칸만 적은 `BaseModel`+`Field`+`Literal`(02·04·07 양식 클래스) · **`AgentState` 상속 칸 클래스**(03, 셀 하나 `upgrade_allow=["class_def"]`) · 칸만 적은 `TypedDict`(03·07 실행 정보) · **`ToolRuntime[MemberContext]` 대괄호**(03·07 — 챕터 리드 결정의 예외, 강사 확인) · 04만 `inspect`·`warnings`·`issubclass` · 06만 `time.perf_counter()`·파일 쓰기. 노드·도움 함수 힌트·반환 힌트 0.
- **쓰지 않은 것(일곱 절 모두 0건, AST 확인)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`:=`·`next`·`all`·`any`·`sum`·`max`·`min`·`sorted`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·별표 풀기·`isinstance`·`try`·`@dataclass`·`MessagesState`·`draw_mermaid_png`·`stream`·`recursion_limit`·미들웨어·체크포인터·`Path`·`statistics`·`with_structured_output`·`as_retriever`. 마감 AST 따로(`extra_check.py` 06절 판) 11건 = 모두 허용 예외(도구 파일 `.get` 둘은 Ch 6 06 원본).
- 셀 모양: 코드 셀 최대 16줄은 05·06 가져오기 준비 셀, 준비 셀이 아닌 셀 최대 10줄, 함수 본문 최대 8줄(06 `search_trace`), 셀당 함수 하나, 첫 줄 주석 100%. **모델이 정하는 값(도구를 부를지·검색어·답 글·양식 칸 값)에 건 `assert` 0** — 호출 ID 짝·메시지 종류·키·양식 값 종류·줄 수·계약 도구 호출 수(≥ 1)에만.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 20 01**(과정 요약 §2-12): 자료실 규정 `POLICIES` 셋(대출 「일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.」·운영 「평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.」·연체 「연체한 일수만큼 새 대출이 제한됩니다.」)과 `@tool lookup_policy(topic: str)`(없는 주제면 `raise ValueError`) — 01 셀이 Ch 20 01과 **문자열까지 같음**, 도구 셀은 코드 줄 같고 주석 한 줄만 「Ch 20 02절」(01 생성기 `check_same_as_ch20()`). 대출·인사·운영과 연체 질문 셋 · Ch 20 도구 파일 `graph_tools.py` 함수 다섯(`tool_call_names`·`show_messages`·`sum_usage`·`estimate_cost`·`call_id_lists`)을 **본문 글자 그대로** `runner_tools.py`로(Ch 20 `run_row`는 흔적 칸을 읽어 옮기지 않음) · Ch 20 01 교재 출력(모델 요청 2·1·3, 도구 메시지 1·0·2, 구조 문자열 `tools --> model` 실선)과 견줌.
- **Ch 13**(상태 그래프): 노드·엣지·조건부 엣지·조건 함수·이름표 표·구조 문자열(01) · 설계 객체 `builder.nodes`·`.edges`·`.branches`(Ch 20 03) · `Send`(05, 소스로만) · 칸만 적은 `TypedDict` 상태 형식(03 실행 정보 모양) · `list[AnyMessage]` 대괄호 뜻(03 `ToolRuntime[…]` 풀이).
- **Ch 6 03·Ch 19 02**: 양식 클래스(`BaseModel`·`Field`·`Literal`)·`model_dump`·구조화 출력(02). **Ch 6 06** `estimate_cost`·요금표(2026-09-17, 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러), 「예상 비용」 = 청구 금액 아님.
- **Ch 16 03** 시스템 메시지(글) → `system_prompt`(01, 메시지 칸에 남지 않음 — 소스 1451~1452행) · **Ch 7 05** ReAct(생각·행동·관찰) · **Ch 17 03** 루프·바퀴·모델의 끝 선택.
- **Ch 19**: 도구 호출 요청(04)·도구 메시지·호출 ID·여럿 담기(05)·결과 상태·읽기 도구(06) · `convert_to_openai_tool` 명세(05).
- **Ch 5 02·Ch 12 01·05·Ch 14 06**(05): 코사인 유사도·거리·거리 순위·`search_hits`(Ch 14 도구 파일 판 — 인자로 받음, NumPy) · Ch 14 자료 `labs/part4/ch14-rag-patterns/data/documents.json`(12건, `d54899d9…`)·`queries.json`(8건, `abdbb041…`) · Ch 10 07 `dimensions=256` · Ch 14 06 다시 검색 상한(코드) ↔ 이 챕터 시스템 메시지 글 「한 번만 더」(모델 선택). **Ch 14 `FAC-003` 「평일 오전 9시~오후 9시」 ↔ 01~04 `POLICIES` 「09:00~20:00」 차이를 05 b3·b7에 밝힘.**
- **Ch 11 01**(06): 정답 문서 ID·`find_gold_rank` · **Ch 15 01·02**(06): 검색 쪽/답 쪽, 평가 모델·근거 충실도 판정 머리글·`build_judge_prompt`·`judge_once`(Ch 15 도구 파일 판) · **Ch 15 05** `time.perf_counter()` · **Ch 18 06** 같은 조건 비교·계약 칸 걸린 초 선례.

## 3. 절별 사례·값 (새 커널 두 번(01~03은 마감 새 실행과 앞 교재 출력)과 노트북 밖 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값(결론·그림에 쓴 값) | 요청 |
|---|---|---|---|
| 01 | 대출 「자료실에서 일반 도서를 며칠 빌릴 수 있나요?」 · 인사 · 값 바꿔 보기 운영·연체 「자료실 운영 시간과 연체 규정을 함께 알려 주세요.」(Ch 20 01과 같은 글) | `만든 것의 종류: CompiledStateGraph` · 상자 넷·갈래 모두 점선(`tools -.-> model`) · `등록된 노드: ['model', 'tools']`·`고정 엣지로 적힌 수: 1`·`조건부 엣지를 적은 노드 수: 2`·상태 칸 셋·`ToolNode` · `tools_to_model` → `['model']`·`model_to_tools` → `['tools', '__end__']` · 결과 키 `['messages']`·메시지 넷·`시스템 메시지 수: 0`·`{'topic': '대출'}`·짝 `True` · 운영·연체 첫 응답 요청 둘 · 표 `2 | 1`·`1 | 0`·`2 | 2`(Ch 20은 3번) · 입력 토큰 `456` | 5 |
| 02 | 01 대출 질문 × `ToolStrategy` / `ProviderStrategy` / 값 바꿔 보기 양식 클래스 그대로 | 결과 키 `['messages', 'structured_response']` · 메시지 `5` ↔ `4`·도구 메시지 `2` ↔ `1`·모델 요청 2·2 · `AIMessage | 도구 호출 요청: ['PolicyAnswer']`·내용 글 길이 0 ↔ 마지막 응답 요청 0건(내용 글 JSON) · `structured_response의 종류: PolicyAnswer` · `tools_to_model` 갈 곳 `['model', '__end__']` ↔ `['model']` · 입력 토큰 `572` ↔ `768` · `기능 표의 structured_output: True` → 양식 클래스 그대로 = 그래프는 도구 전략 모양, 메시지 칸은 제공자 전략 모양 | 6 |
| 03 | 「제가 지금 새 책을 빌릴 수 있나요?」 · 상태 `ticket_no` `Q-017` · 실행 정보 `{"member_id": "M-0317", "overdue_days": 0}` · 값 바꿔 보기 연체 3일 | `두 자리의 AgentState가 같은 클래스인가: True` · 명세 `check_my_loan | … [] | … []` · 상태 칸 넷(`ticket_no` 더함) · 결과 키 `['messages', 'ticket_no']`·`Q-017` · `check_my_loan | 인자: {}` · 도구 메시지 `이용자 M-0317: 연체가 없어 새 대출을 할 수 있습니다.` ↔ `… 연체 3일. 연체한 일수만큼 새 대출이 제한됩니다.` · `member_id | 결과 딕셔너리에 있는가: False` · 표 `2 | 1 | True` 둘 · 입력 토큰 `426`·`434` | 4 |
| 04 | 01 모델 객체·`lookup_policy`·시스템 메시지 글 + 02 양식 클래스로 옛·새 그래프 넷(만들기만) | 인자 여덟 `True/False`(`prompt`·`pre_model_hook`·`post_model_hook` 옛 함수만 · `system_prompt`·`middleware` 새 함수만) · `받은 경고 수: 1` ↔ `0`·`LangGraphDeprecatedSinceV10`·`사용 중단 경고의 한 종류인가: True` · 노드 `['agent', 'tools']` ↔ `['model', 'tools']` · `tools --> agent;` ↔ `tools -.-> model;` · 고정 엣지 2 ↔ 1 · 채우는 값 `['remaining_steps']` ↔ `[]` · 입력 칸 `['messages', 'remaining_steps']` ↔ `['messages']` · 양식을 넘기면 옛 노드 `+ generate_structured_response` | 0 |
| 05 | Ch 14 `C05` 「토요일 자료실 폐관 시각은?」 · 값 바꿔 보기 문서에 없는 주차 질문 「자료실 주차 요금은 얼마인가요?」 | `명세의 인자: ['query']` · 질문 글 그대로 `1 | FAC-003 | 0.6` · `C05` 메시지 4·검색 한 번·도구 메시지 `['FAC-003', 'LIB-002', 'ACC-004']` · 같은 검색어 다시 부르기 `True` · 주차 메시지 6·응답마다 요청 1·1·0(다시 검색 한 번) · `C05 질문 | 2 | 1 | True`·`주차 질문 | 3 | 2 | True` · 임베딩 요청 6 · 입력 토큰 `638`·`1189` | 5 + 임베딩 6 |
| 06 | Ch 14 `C01`·`C05`·`C07`(옛 판 질문 그대로) × 고정 흐름 / 에이전트 흐름, 같은 검색 도구·`top_count = 3` | 모델 요청 질문마다 1 ↔ 2 · 도구 메시지 0 ↔ 1 · 고정 입력 `178`·`186`·`185` / 에이전트 `632`·`638`(`C01`·`C05`) · 정답 문서 자리 `C01` 2 ↔ 1, `C05`·`C07` 1·1 · 판정 여섯 `1`(가를 수 없음) · `담은 줄 수: 3` · 요청 셈 `3 | 6 | 6`·임베딩 `1 | 3 | 3` | 15 + 임베딩 7 |
| 07 | §7 | §7 | 4 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 에이전트를 만드는 함수(create_agent) | 모델·도구 목록·시스템 메시지 글을 받아 모델과 도구를 오가는 그래프를 만들어 컴파일까지 해 주는 LangChain 함수 | `create_agent(model, tools=[…], system_prompt=…)` |
| 01 | 에이전트 그래프 | `create_agent`가 내놓는 컴파일한 그래프(모델 노드와 도구 실행 노드가 들어 있음) | `agent`, 종류 `CompiledStateGraph` |
| 01 | ReAct 루프 | 모델이 다음 행동을 고르고, 코드가 도구를 실행하고, 그 결과를 다시 모델에게 보여 주는 반복(Ch 7 05에서 이름만 본 방식) | 모델 노드 → 도구 실행 노드 → 모델 노드 |
| 02 | 도구 전략(ToolStrategy) | 양식을 도구 하나로 모델에게 알리고, 모델이 그 도구를 부르면 요청의 인자를 양식 값으로 받는 방식 | `response_format=ToolStrategy(PolicyAnswer)` |
| 02 | 제공자 전략(ProviderStrategy) | 모델 제공자의 구조화 출력 기능으로 요청에 양식을 실어 응답 글을 양식 모양으로 받는 방식. **OpenAI 계열이면 함께 싣는 도구 명세에 `strict=True`, 양식 쪽은 기본 `strict` 없음(`false`)**(마감 A-3) | `ProviderStrategy(PolicyAnswer)` |
| 02 | 양식 도구 | 도구 전략이 양식 클래스로 만들어 모델에게 알리는 도구(이름 = 양식 클래스 이름) | 도구 호출 요청 `['PolicyAnswer']` |
| 03 | 라이브러리 상태 형식(AgentState) | `create_agent` 그래프의 상태 형식(칸 `messages`·`jump_to`·`structured_response`), 물려받아 칸을 더함 — **Ch 20 01 우리 상태 형식 `AgentState`·Ch 30 서비스 코드의 `AgentState`와 다른 것** | `class LibraryState(AgentState)` |
| 03 | 실행 정보(context) | `invoke(…, context=…)`로 상태 밖에 따로 넘기는 값. 칸은 실행 정보 형식(`context_schema`)에 적고 결과 딕셔너리에 남지 않음 — **Ch 8 01 「컨텍스트」(모델이 받은 글 전체)와 다른 값** | `context_schema=MemberContext`·`context={…}` |
| 03 | 실행 객체 표시(ToolRuntime) | 도구 매개변수 뒤 `: ToolRuntime[…]` — 라이브러리가 실행 정보를 담은 객체를 넣어 주고 도구 명세에 실리지 않음 | `runtime: ToolRuntime[MemberContext]` |
| 04 | 옮기기(마이그레이션, migration) | 옛 판에서 쓴 코드를 새 판에서 돌도록 고쳐 쓰는 일(마감 B-4 — 풀이를 이 말로 맞춤) · **Ch 23 02·Ch 31 03의 DB 「마이그레이션」과 다른 뜻** | 옛 함수 줄 → 새 함수 줄 |
| 04 | 옛 함수(create_react_agent) | LangGraph 0.x 판에서 에이전트 그래프를 만들던 함수, 지금 판(langgraph-prebuilt 1.1.0)에 사용 중단 경고와 함께 남음 | `create_react_agent(model, tools=[…], prompt=…)` |
| 04 | 사용 중단 경고(DeprecationWarning) | 곧 없앨 기능을 쓸 때 Python이 내는 경고의 종류(「단종 예정」 안내 — 마감 B-4) | `LangGraphDeprecatedSinceV10` |
| 05 | 검색 함수(retriever) | 질문 글을 받아 가까운 문서를 거리 차례로 찾아 내놓는 함수(「검색기」는 과정 금지어) | `search_hits` |
| 05 | 검색 도구 | 검색 함수를 `@tool`로 감싼 도구(모델이 요청할 때만 실행) | `search_documents` |
| 05 | 검색어(query) | 모델이 검색 도구의 인자 `query`에 적은 글 | `call["args"]["query"]` |
| 06 | 고정 흐름 | 질문마다 코드가 먼저 검색하고 찾은 문서 글을 붙여 모델에 한 번 묻는 흐름 | `search_documents.invoke({"query": …})` + `model.invoke(…)` |
| 06 | 에이전트 흐름 | 검색 도구를 부를지와 검색어를 모델이 고르는 흐름 | `agent.invoke(agent_state)` |
| 06 | 비교 기록 | 질문 하나마다 두 흐름의 답·문서 ID·사용량·판정을 한 줄로 담아 파일로 쓴 것(기록 한 줄 = 질문 하나) | `records` · `data/rag-comparison.json` |

- **일반 말(새 말 아님)**: 메시지 칸·결과 딕셔너리의 키·응답 수·상태 칸·조건 함수 이름·갈 수 있는 곳·요청 id 목록·호출 ID 목록·설계 객체(01) · 기능 표(속성 `profile`)·양식 값이 온 자리·양식 칸·JSON 모양 설명(02) · 문의 번호·이용자 번호·연체 일수·실행 객체(매개변수 `runtime`에 들어오는 객체)(03) · 그래프가 채우는 값·화살표 줄·입력 칸·인자 이름·경고 글(04) · 문서 ID 줄·임베딩 요청·자를 개수·다시 검색(05) · 평가 질문 셋·답 머리글·검색 기록·정답 문서 자리·토큰 합·걸린 초(06).
- **금지어(일곱 절 설명·주석·캡션·`.mmd`·README 0건 — 제목·슬러그·코드 백틱 말고)**: 「지시」(→시스템 메시지 글·규칙)·「반환」(→내놓다)·「추정」(→예상)·「지연」(→걸린 시간)·「분기」(→갈래)·「경로」·「trace」·「스키마」(원어 「schema」 한 번씩만)·「필드」(→칸)·「검증」(→검사)·「프롬프트」·「프로필」(→기능 표)·「주입」(→넣어 주다)·「런타임」·「컨텍스트」(Ch 8 뜻만)·「검색기」·「리트리버」·「쿼리」(→검색어)·「정확도」·「정답률」(Ch 15 태도 문장만)·「judge」 단독·「gold」(코드 이름만)·「latency」·「Agentic」·「사전」·「캐시」 단독·「최대」·「돌려주다」류·규격 §4 금지 말·「쉽게·간단히·당연히」·「개선 전」·「강사 시연」·`MessagesState`. 마감 전후 금지어 목록(`.cache/ch21-close/log/ban-*.txt`) 같음(35줄 — 슬러그·제목 말·코드 이름·원제목).
- 제목 말 「create_agent」·「ReAct」(01)·「AgentState」·「context_schema」(03)·「마이그레이션」(04)·「retriever」(05)·「평가셋」·「RAG」(06)은 제목과 본문 첫 풀이에만(강사 확인).

## 5. 색 규칙 (Mermaid 27장, experiment 일곱 절이라 빨강 0)

- **질문·자료·넘긴 값·실행 정보·같은 조건 초록(tool)** · **우리가 적은 함수·도구·양식 클래스·실행 정보 형식·인자 줄 파랑(flow)** · **실제로 부른 모델 보라(model)**(sequenceDiagram은 `box Lavender` 띠 — 01-3·02-3·03-3·05-3·06-3·07-2, 보라 상자는 05-1 임베딩 모델·05-2 모델이 고르는 자리·06-1 모델 요청·06-2 평가 모델, 04는 0) · **출력으로 확인한 값·sequenceDiagram 메모 노랑(measure)**(소스로만 본 동작은 메모 앞 「소스 확인 ·」) · **라이브러리가 준 것(`create_agent` 함수·에이전트 그래프·모델 노드·`ToolNode`·가상 시작점/끝점·양식 도구·옛 함수 노드)·공통 사실·다른 챕터 교재 출력 회색**.
- **마감 결정(챕터 리드, 검토 A-13·B-12)**: **`create_agent`는 라이브러리가 준 함수라 회색** — 01-1·05-1을 파랑에서 회색으로 고쳐 07-1과 맞춤. 04-2의 `prompt=`·`system_prompt=` 인자 상자는 우리가 적은 줄이라 파랑 그대로.
- 조건 함수(`model_to_tools`·`tools_to_model`·`should_continue`)는 상자로 그리지 않고 점선 갈래 라벨로만(구조 문자열 상자 수와 맞춤). 에이전트 그래프의 갈래는 되돌아가는 엣지까지 모두 점선, Ch 20·옛 함수 그래프의 되돌아가는 엣지만 실선. 나란한 칸은 subgraph 둘 + `~~~` 회색 공통 상자(공통 상자에는 모든 칸 출력에서 확인한 값만). 원본 viewBox 폭 모두 868 이하(최대 865, 07-2).
- **마감에서 다시 렌더한 `.mmd` 다섯**: `01-1`(색) · `02-1`(A-6 라벨) · `04-2`(B-2 한정어) · `05-1`(색) · `06-4`(B-6 맨 위 상자) — 모두 다시 렌더(01-1·02-1·04-2는 `run_section.sh`가 바뀐 도장을 보고, 05-1·06-4는 `--force`), 노트북 첨부가 있는 01-1·02-1·05-1은 첨부 PNG 새 판. PNG를 다른 이름으로 복사해 직접 보고 「도식 읽기」와 맞춤(`.cache/ch21-close/view/`). `06-1`은 캡션만(`.caption.md`와 `_src` 같게).
- **비유 계열 「세탁기(코스 버튼과 동그란 창)」**: 01 따로 놓인 손빨래 도구 셋(대야·빨래판·헹굼 통) ↔ 흰 앞문형 세탁기 한 대(둥근 버튼·유리창 = `invoke`·구조 문자열과 메시지 칸) · 02 똑같은 세탁기 두 대 — 앞에 따로 세운 **개는 판**(도구 전략) ↔ 몸체 아래 틈(제공자 전략), 하늘색 셔츠 두 벌(오른쪽 셔츠가 개어지지 않고 늘어짐 — 강사 확인) · 03 윗면 틈에 꽂은 **주황 카드**(실행 정보, 결과에 안 남음) ↔ 셔츠 깃 **이름표**(상태 칸, 결과에 남음), 회갈색 벽 · 04 연녹색 위 뚜껑형 옛 세탁기 + 관으로 이은 회색 상자 ↔ 흰 앞문형 새 세탁기, 연노랑 수건 둘 · 05 윗면에 거꾸로 꽂힌 연녹색 세제 통·빈 계량컵(모델이 부를 때만 검색) · 06 똑같은 세탁기 두 대·분홍 스웨터 더미 둘(셋씩)·가운데 돋보기(같은 빨랫감·같은 기준) · 07 세탁기 한 대 옆 고리의 **열쇠**(실행 정보)·선반의 갠 빨래(양식 값) — 07 b4는 마감에서 03 카드·02 개는 판과 잇는 문장을 더함(B-15). 사람·손·화살표·글자·숫자·눈금 다이얼 없음.

## 6. 서비스 요청과 흔들린 값

- 노트북 한 번 요청: 머리 참고. 작업 전체 서비스 요청(노트북 밖 확인 + 새 커널): 01 35 · 02 42 · 03 28 · 04 0 · 05 모델 35·임베딩 46 · 06 모델 105·임베딩 46 · 07 28 = **모델 273번·임베딩 92번**, **마감 모델 15번**(01 5 · 02 6 · 03 4 · 04 0, 임베딩 0). 요금표 어림 예상 비용 합 약 0.10달러(01 0.012 · 02 0.016 · 03 0.0083 · 05 0.013 · 06 0.036 · 07 0.015) + 마감 약 0.005달러(청구 금액 아님). 삽화 7장 14크레딧(모두 1차 채택), 마감 Higgsfield 호출 0.
- **흔들림 확인(노트북 밖 다섯 번, 규격 §2-7 10번 끝 — 입력·판단 규칙을 첫 요청 전 `NN-probe.md` §0에)**: 01 L·G·T 각 5/5(15/15) · 02 TS·PS·AS 각 5/5 · 03 R0·R3 각 5/5 · 05 S5·SP 각 5/5(주차 다시 검색 두 번 5/5) · 06 세 질문 × 두 흐름 × 5 — **에이전트 검색 한 번 15/15**, 판정 30/30 = 1, `C07` 검색어 세 가지·입력 토큰 638~640 · 07 R1·R2 각 5/5(양식 칸 = 규칙 값 10/10). 04는 모델 요청 0(새 커널 두 번 24/24). 결론에 쓴 모양(메시지 종류·수·도구 이름과 인자·응답 수·입력 토큰·문서 ID·정답 자리)은 다섯 번과 새 커널 두 번에서 같음.
- **탐색으로 고른 입력: 없음**. 모든 질문·시스템 메시지 글·양식·실행 정보 값·문의 글은 노트북 밖 확인 전에 정했고(01~03·05·07은 이 챕터에서, 06은 옛 판 질문 그대로), b7에 「흐름을 보여 주려고 정한 예」.
- **흔들린 값의 자리**(결과 읽기 둘째 단락·「확인할 점」·본문 표의 「교재 출력」 표시·b7에만, 「이번 실행에서는」): 모든 답 글·양식 칸의 답 글·판정 까닭 · 출력 토큰과 그 예상 비용 · 03 출력 토큰(**마감 새 실행 `39`·`76`**, 앞 판 `45`·`79`/`44`)·비용(**`0.000495`·`0.000668`**) · 05·06 검색어(06 `C07`) · 06 걸린 초·토큰 합 · 06 `C07` 에이전트 입력 토큰(`638`/`639`) · 07 출력 토큰 `104`·`117`. **그림 라벨·캡션·정리·복습·본문 결론에서 흔들린 값에서 끌어낸 비교 0건**(마감 확인 — 06 b6의 입력 토큰 「세 배를 넘었습니다」는 두 번 같았던 값이고, 마감 B-6에서 원인을 검색 호출 쪽 하나로 읽지 않게 요청 모양 차이를 함께 적음).
- 새 커널 셀별 같음: 01 23/23 · 02 28/28 · 03 20/24 · 04 24/24 · 05 26/26 · 06 26/31 · 07 24/24(개선 때). **마감 새 실행 ↔ 앞 교재 출력**: 01 22/23 · 02 27/28 · 03 19/24 · 04 23/24(다른 셀은 모두 설치 셀 `numpy` 한 줄 + 03의 흔들리는 값 넷), 04 마감 새 커널 두 번 24/24.
- **재지 않은 것**: 걸린 시간(06 계약 칸 하나 말고 — 준비물의 「N초 안에」는 셀 실행 기록) · 청구 금액 · 서비스 오류 · 한 응답의 요청 둘을 한 단계에서 함께 실행하는지·단계 수(소스로만) · 도구 오류(`ValueError`) 장면 · 양식 검사 실패 재요청 · 한 응답에 규정 요청과 양식 도구 요청이 함께 오는 장면 · 옛 함수 `invoke`·0.x 판 · 에이전트가 검색하지 않는 장면·세 번 검색 · 임베딩 요금.

## 7. 07절 실습 절 주제와 결과

- 제목 「**create_agent 실습: 대출 문의 에이전트에 양식과 실행 정보 붙이기**」, 슬러그 `07-create-agent-실습`(선례 `05-ToolNode-실습`·`09-Middleware-실습`), `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~06 meta 합 강의 1×6 = **6h** · 실습 1.5×4 + 2 + 2 = **10h** = `chapter.json` 「총 16h · 강의 6h · 실습 10h」(`_build_index.py`도 6·10).
- 문의 「제가 지금 새 책을 빌릴 수 있는지 확인해 주세요. 일반 도서 대출 규정도 함께 알려 주세요.」(두 도구가 모두 있어야 답하게 — 실행 전에 정함) · 실행 1 실행 정보 `{"member_id": "M-0317", "overdue_days": 0}` → 실행 2 **`overdue_days` 하나만 3**(03 7·8절 값 그대로 — 「새로 볼 것」 = 바뀐 도구 메시지가 모델이 채우는 양식 칸까지 이어지는지).
- 붙인 앞 절 기능 셋(모두 흐름 안에서 쓰임): **01** `create_agent` + `POLICIES`·`lookup_policy`(셀 글자 그대로) · **02** 양식 클래스 `LoanAnswer`(칸 `can_borrow: Literal["가능", "불가"]`·`answer`) + `ToolStrategy` · **03** `context_schema=MemberContext` + `check_my_loan(runtime: ToolRuntime[MemberContext])`(셀 글자 그대로) + `invoke(…, context=…)`. 시스템 메시지 글 = 01 글 + 03 글 둘째 문장. 뺀 것: 02 제공자 전략 · 03 상태 칸 · 04 옛 함수 · 05 검색(임베딩) · 06 평가·**계약 파일(읽지도 쓰지도 않음)**.
- 결과(새 커널 두 번 24/24 + 노트북 밖 10/10 같음): 재료 `꼭 채울 칸: ['can_borrow', 'answer']` · 노드 `['model', 'tools']` · 갈 곳 02 도구 전략 그래프와 같음 · 두 실행 모두 결과 키 `['messages', 'structured_response']`·메시지 6·첫 응답 `['check_my_loan', 'lookup_policy']` → 둘째 응답 `['LoanAnswer']` · `실행 1 · 연체 0일 | 2 | 3 | True`·`실행 2 · 연체 3일 | 2 | 3 | True` · `check_my_loan | 두 실행의 글이 같은가: False`·`lookup_policy | … True` · **양식 칸 `가능` → `불가`**(도구 몸통과 같은 규칙으로 코드가 정한 값과 `같은가: True` 둘 — `assert` 없음) · 입력 토큰 `776`·`784` · 모델 요청 합 4.
- 마감 반영: 준비물·b2 「Ch 2에서 배운 문법」(B-13) · 복습 3을 새 관찰 쪽으로(B-14) · 비유 이음 문장(B-15) · 1절 NumPy 문장. 다시 실행하지 않음.

## 8. 도구 파일 `notebooks/runner_tools.py` — 함수 표와 해시 변천

| 함수(인자) | 배운 곳 | 가져오는 절 |
|---|---|---|
| `tool_call_names(response)` | Ch 19 04 | (`show_messages` 안) |
| `show_messages(messages)` — 종류, 응답이면 `| 도구 호출 요청: […]`, 도구 메시지면 `| 결과 상태: … | 내용: …`(`SystemMessage`는 안 찍음, 내놓는 값 없음) | Ch 19 06 | 01·02·03·05·06·07 |
| `sum_usage(messages)` — `{"requests", "input_tokens", "output_tokens"}`(응답 수 = 모델 요청 수, 캐시 입력 칸 없음) | Ch 19 05 | 01·02·03·05·06·07 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06 | 01·02·03·05·06·07 |
| `call_id_lists(messages)` — `{"요청 id": […], "호출 ID": […]}` | Ch 20 01 | 01·(`agent_row` 안) |
| `agent_row(question_name, result)` — `{"질문","모델 요청 수","도구 메시지 수","호출 ID 짝"}` | Ch 21 01 | 02·03·05·06·07 |
| `print_branches(graph_agent)` — 조건부 엣지마다 `노드 | 조건 함수: … | 갈 수 있는 곳: […]` | Ch 21 02 | 03·04·05·07 |
| `cosine_similarity(first, second)` | Ch 5 02 | (`cosine_distance` 안) |
| `cosine_distance(first, second)`·`rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)` | Ch 12 01 | (`search_hits` 안) |
| `print_ranked(hit_list, value_name)` | Ch 12 05 | 05 |
| `search_hits(embedding_model, question, doc_vectors, doc_ids, top_count)` — 부를 때마다 임베딩 요청 1번 | Ch 14 06 | 05·06 |
| `find_gold_rank(doc_ids, gold_doc_ids)` — 없으면 0 | Ch 11 01 | 06 |
| `build_judge_prompt(judge_head, pair, case)`·`judge_once(judge_model, prompt_text)` — JSON 글 → `json.loads` | Ch 15 02 | 06 |

- 함수 **열다섯**, 함수마다 `# Ch N MM절에서 배웠습니다 — …`, import `json`·`numpy as np`, 전역 이름 기대기 0, 금지 문법 0(`.get` 둘은 Ch 6 06 원본 예외), 188줄. 모든 함수가 옮겨 온 원본(Ch 20 `graph_tools.py`·Ch 14/15 `rag_tools.py`·01/02 노트북)과 def~끝 **글자와 AST가 같음**(검토 A·B 확인). `@tool`·도구·그래프 조립은 노트북에.
- **옮기며 줄이거나 다시 쓴 주석**(규격 §4, 마감 A-15 — 코드 그대로): `cosine_distance`는 Ch 14 판 둘째 주석 줄(「Ch 12 01절 판은 바깥 이름 similarity_top을 읽었고 …」)을 옮기지 않음 · `search_hits`는 Ch 14 주석 두 줄을 「Ch 14 06절에서 배웠습니다 — …」 + 뜻 + 「Ch 14 06절 노트북 판은 바깥 이름을 읽었고, 이 판은 … 인자로 받습니다」로 다시 씀. 나머지 함수의 주석 머리는 「Ch N MM절에서 배웠습니다 — (어느 도구 파일)의 같은 이름 함수를 옮겼습니다」 + 원래 뜻 줄.
- **해시 변천**: 없음 → 01 `eb408639…`(Ch 20 함수 다섯, import 0) → 02 `ab31d0c1…`(+ `agent_row`) → 03·04 `6ce7a8d2…`(+ `print_branches`) → 05 `8538fedb…`(+ `import numpy as np`·Ch 14 함수 다섯) → 06 **`f4113158c0ccaee1205f0eabe315ef153e14c4dc6bcfd70ae8a9378edda96bdf`**(+ `import json`·Ch 15 함수 셋) → 07·**마감 그대로**.
- **NumPy와 설치 셀(마감 A-12·B-1)**: 파일 맨 위 `import numpy as np` 때문에 **일곱 절 모두 설치 셀에 `"numpy==2.5.3"`**(잠금 판 — 01~04는 마감에서 더하고 다시 실행). 실습 폴더 `.venv`(`uv sync --locked`)에는 원래 있어 그대로 돌았지만, 설치 셀만으로 만든 환경에서는 가져오기 셀이 멈췄음(검토 A-12 확인).
- 가져오는 절마다 준비 셀 결과 읽기에 고정 세 문장(「앞에서 배운 함수는 `runner_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.」) + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」. 01은 마감에서 「이 절이 쓰는 함수는 … · 같은 파일에는 뒤 절이 쓰는 함수도 · 파일 맨 위에서 NumPy를 가져오므로 `numpy`도 설치」로 범위를 좁힘(A-1).
- 묶음 목록 두 곳(`textbook/part6/public-files.json`·챕터 `qa/public-files.json`)에 있고 마감 zip(`3755de3d…`)에 든 판이 디스크와 같음. **Ch 21 실습 폴더 전용**(Ch 20 `graph_tools.py`와 다른 파일). Part 6 선행 목록에는 없음(뒤 챕터 노트북이 쓰지 않음).

## 9. 06 ↔ Ch 29 04 계약과 새 인용값

- 파일 `labs/part6/ch21-create-agent/data/rag-comparison.json` — **`25cfe5df3cfd729c130bce4af26c716cfcc3bcd4b4ff6e4a9d0a725816b02f51`**(06 A가 씀, 개선 전 `122cfce2…`) · 줄 3(`C01`·`C05`·`C07`) · 칸 12. Ch 29 04 노트북 cell 12~18이 읽는 키: `qid` · `agent_usage`{`input_tokens`·`output_tokens`·**`model_calls`**(← `sum_usage`의 `requests`)} · `agent_supported`(bool, `float()`) · **`tool_calls`**(int = 도구 메시지 수, 줄마다 ≥ 1) · `agent_latency_s`(float — 에이전트 `invoke` 앞뒤 `perf_counter`) · `agent_trace`(목록 `{"query", "doc_ids"}`). `assert` 셋: `len == 3` · `tool_calls >= 1` · p95 ≥ 최댓값. Ch 29가 읽지 않는 칸: `gold_doc_id`·`fixed_*`·`agent_answer`·`summary`(개선 때 `fixed_latency_s`를 뺌 — 읽는 곳은 옛 생성기 `_author_ch21_ch29.py`(Ch 21 쪽 막힘)·옛 `집필점검표.md`뿐).
- **흉내 검사(마감 끝 다시)**: `.cache/ch21-close/ch29_04_sim.py`(06 작업자의 `/tmp/ch21-06/ch29_04_sim.py` 사본 — cell 12·14·16(Ch21 부분)·18의 읽기 코드와 `assert` 그대로) → **PASS** · `{'final_score_mean': 1.0, 'model_calls_mean': 2, 'tool_calls_mean': 1, 'tokens_mean': 688, 'latency_mean_s': 1.731}` · `{'latency_p95_s': 2.003, 'tokens_p95': 699.0}`.
- **Ch 29 04 새 인용값(Ch 29 파일은 고치지 않음 — Ch 29 작업 때)**:

| 자리 | 지금 글(옛 값) | 지금 계약 파일로 셈한 값 | 흔들림 |
|---|---|---|---|
| `textbook/part6/ch29-agent-evaluation/_src/04-운영-지표와-Ch18-궤적-비교.html` **6·7·9행**(같은 문장 세 곳) 「Ch21 세 Agentic RAG 행은 평균 final_score 1.0, 모델 2회, 도구 1회, **519.7토큰, 1.880초**」 | 1.0 · 2 · 1 · 519.7 · 1.880 | 1.0 · 2 · 1 · **688** · **1.731** | 토큰은 출력 토큰만큼(B 사본 689.3), **걸린 초는 흔들리는 값** |
| 같은 세 행 「Agent 세 건의 p95는 지연 **2.094초**, 토큰 **541**」 | 2.094 · 541 | **2.003** · **699** | 걸린 초는 흔들리는 값(B 사본 토큰 p95 702) |
| 같은 파일 **10행** 복습 3 해설 「**2.094초**였습니다」 | 2.094 | **2.003** | 흔들리는 값 |
| `labs/part6/ch29-agent-evaluation/notebooks/04-운영-지표와-Ch18-궤적-비교.ipynb` 저장 출력 cell 14·16·18 | 옛 파일로 계산한 값 | 다시 실행하면 새 값(모델 요청 없음) | — |

- 결정적인 값: 줄 3 · 모델 2 · 도구 1 · `final_score` 1.0. **걸린 초 둘을 Ch 29 본문에 숫자로 둘지부터 Ch 29 담당이 정할 것**(규격 §2-7 9번 — 흔들린 값은 결론·복습에 쓰지 않음). 「Agentic RAG」·「지연」은 과정 금지어(Ch 29 몫).
- **06은 다시 실행하지 말 것**(Ch 18 06 선례). 다시 실행하면 계약 파일 해시·위 값이 또 바뀌고, 모델이 한 질문에서 검색을 건너뛰면 06 10절 셀이 파일을 쓰기 전에 멈춤(마감 B-9 — 노트북·b7에 안내).
- **과정 계약 문서**: `textbook/qa/upgrade-contracts.md`에 「Ch21 06 출력 계약(Ch29 04)」 줄이 아직 없음(검토 B-11) — Part 6 마감 오케스트레이터가 Ch 18 06 줄(98행)과 같은 모양으로(파일 경로·해시 `25cfe5df…`·`assert` 셋·흉내 검사 PASS·위 옛/새 값·「06 다시 실행 금지」).

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part6/ch21-create-agent/notebooks/01~07-*.ipynb` · `notebooks/runner_tools.py` · `data/rag-comparison.json` | 01~07절 · **마감** | 실습 폴더(챕터 몫) — §1·§8·§9·§15. 마감: 01~04 다시 실행(설치 셀 `numpy`), 05~07 마크다운(05는 첨부 PNG도)만. 노트북 파일 `f5e6c60b`→`a520bc6e` · `920244fc`→`0acd3667` · `890665f1`→`9a5ee92f` · `cbba4573`→`8656c3f0` · `4c2eac65`→`6598d4f0` · `768d4f9e`→`8a6f9da7` · `746b3a46`→`a1ac0fcf`. 도구 파일·계약 파일 마감 그대로 |
| `labs/part6/ch21-create-agent/README.md` | 07절(07 단락) · **마감(전체)** | `c9adbb9d…` → **`fc6e44ba4750a212…`**: 노트북 일곱(모두 API 키 — 04는 요청 0이지만 키 필요), `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 키는 커널 폴더에서 위로 찾은 첫 `.env`, 패키지 판(일곱 절 모두 `numpy`), 모델 설정(`gpt-5.4-mini`·`temperature=0`·`reasoning_effort="none"`·임베딩 256), 도구 파일 단락(고정 문장 뜻 · 함수 열다섯·배운 절·가져오는 절 · `json`·NumPy · 앞 챕터 도구 파일과 다른 이 챕터만의 파일), 절마다 하는 일, 읽고 쓰는 파일(05·06 Ch 14 자료 읽기만 · **06이 쓰는 `data/rag-comparison.json` = Ch 29 04가 읽는 파일 — 다시 실행하면 덮어씀·검색을 건너뛰면 셀이 멈춤**), 모델 39번·임베딩 13번(절별)·예상 비용(청구 아님, 임베딩 요금 뺌), 07 단락. **「절당 예상 비용은 1달러 미만」·「Ch14」 띄어쓰기 옛 문장 뺌**, 묶음에 없는 파일 경로를 가리키지 않음 |
| `textbook/part6/public-files.json` | 01절 · **마감** | 01절 도구 파일 줄 · 마감 A-14: 챕터 목록 둘에 줄을 더한 뒤 `python3 textbook/part6/qa/collect_public_files.py`로 다시 모음 → **Ch 21 07 노트북·Ch 22 09 노트북 두 줄**만 늘어남(`c6c7137f`→`cf2fb079`, 보호 파일). 함께 쓰는 `prerequisite-files.json`은 바이트까지 같음 |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | 01절 · **마감** | 07 HTML·07 노트북 두 줄(`2c7c8fa8`→`cf882fbd`, 보호 파일) |
| `textbook/part6/ch22-middleware/qa/public-files.json` | **마감** | **Ch 22 09 HTML·09 노트북 두 줄**(명시 목록에 빠져 있었음 — 챕터 리드 결정 「함께」, `e4f3959f…`, 보호 목록 밖) |
| **`labs/part6/ch22-middleware/notebooks/01-미들웨어와-6개-훅.ipynb`** · `textbook/part6/ch22-middleware/qa/upgrade/author_upgrade.py` · 빌드 `textbook/part6/ch22-middleware/01-미들웨어와-6개-훅.html` | **마감** | 검토 A-10(챕터 리드 결정): 설명 셀 「타입 힌트는 … 표시입니다. 실행 결과는 바꾸지 않습니다.」 → 「… 표시입니다. **이 절의 훅 함수에 붙인 타입 힌트는** 실행 결과를 바꾸지 않습니다.」 — `mdpatch.py`(생성기 문자열 같게, `_src/01`에는 없는 문장이라 그대로), Ch 22 `_build.py`로 다시 빌드(다른 Ch 22 HTML 아홉·`_src` 바이트까지 같음 — 고치기 전 빌드로 재현성 먼저 확인). 노트북 `885379d3`→`fc953e9c`(**`code_sha256` `138108940422…`·`outputs_sha256` `50baad1054f4…`·`executed_at` 2026-09-15 그대로**), HTML `801711e9`→`413b07b0`(보호 파일 둘). Ch 22 `verify.py --chapter` **`PASS 9 sections / 135 code cells (max 14 lines)`**(계약 기록 파일 해시 그대로) · 01 게이트 `check_section()` 직접 호출 G1~G7 **0**. 근거: 설치판 `middleware/types.py`에 `get_type_hints`·`signature` 0 |
| `textbook/part6/_build_index.py` | **마감** | ch21 설명 「create_agent로 도구 에이전트를 만들고 같은 평가셋에서 고정 RAG와 비교합니다.」 → 「함수 create_agent 한 줄로 에이전트 그래프를 만들어 Ch 20 그래프와 견주고, 구조화 출력 두 전략·실행 정보·옛 함수 옮기기·검색 도구를 다룬 뒤, 같은 평가 질문으로 고정 흐름과 에이전트 흐름을 견주고 대출 문의 에이전트에 양식과 실행 정보를 붙이는 실습을 합니다.」(시수 6·10 그대로, `882eda82`→`9e130bd4`, 보호 파일) |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | 07절 + **마감** | `python3 textbook/part6/_build_index.py`(README·노트북·목록을 모두 고친 뒤 마지막 한 번) → **`Part 6: 49 verified sections; 94 bundled files`**, zip `27876634…`(07절) → **`3755de3d15b36c8d249fa6d4bfa18aeacf057c6f4e5038547e669cedc82e48ed`**(97항목, Ch 21 열둘·Ch 14 자료 둘·Ch 22 01 노트북 모두 디스크와 같음, `__pycache__` 0), `index.html` → `c465e7b4…`(01·03 제목 밑줄·새 설명), `integration-results.json` → `e539f6d2…` |
| `textbook/part6/qa/bundle-execution.json` | **마감** | Part 6 `check_bundle_execution.py`가 다시 씀(`d6e1ba96`→`2a3bed10` — 새 zip, **Ch 24 01 4셀·Ch 28 01 4셀 PASS**, Ch 21은 실행 대상 아님). `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache`·`UV_LINK_MODE=symlink` 환경 변수만(스크립트 수정 0) |
| `textbook/part6/qa/visual-results.json` · `textbook/_notebook/checks/ch21-create-agent/visual-results.json`(+ 스크린숏) | **마감** | `visual.cjs` 16행 PASS(`NODE_PATH=/tmp/pw/node_modules`·`LD_LIBRARY_PATH=/tmp/libs/…`). 공용 파일은 **Ch 21 줄만** 14 → 16(새 HTML 해시), `screens` 116 → 118, 다른 챕터 줄 그대로(`402e57e0`→`eec79f55`, 보호 파일) |
| `textbook/part6/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 다시 써서 실행 전 사본으로 되돌림(내용 변경 0, `b3d69e9c…`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(마감 뒤 `b8a4f9123f90…`) |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 21 행 한 줄 · §2-10 Ch 21 항목과 §3·§4 Ch 21 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md`(B-11 — Part 마감 몫) · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`build_bundle.py`·`render_mermaid.py`·`attach_figures.py`·`builder.py`) · Part 6 옛 검사 스크립트와 `check_*`·`collect_public_files.py` · **`textbook/_notebook/build_index.py` 46행**(Ch 21 절 수 6 — Ch 17~20 선례대로 그대로) · **공용 옛 생성기 `textbook/part6/_author_ch21_ch29.py`**(Ch 29가 아직 씀 — 01절이 넣은 Ch 21 멈춤 줄 그대로, 옮기지 않음) · `textbook/part6/qa/final-artifact-hashes.json`(Ch 21 줄 43개가 옛 판 — 만드는 스크립트가 없어 기록만) · `existing-artifact-hashes.json`(Ch 21 줄 0) · 실습 폴더 `pyproject.toml`·`uv.lock`(보호 파일 — B-16 `pillow`는 그대로, §16) · `labs/part6/continuity-guide.md`(Ch 21 문장은 참 — 확인만) · Ch 22 01 밖의 Ch 22 파일(`_src`·02~09) · **Ch 23 이후 파일 전부**(Ch 29 04 `_src`·노트북·Ch 29 01 b3·Ch 30 01·03 포함) · 보호 파일 가운데 아래 열셋 밖의 60개.
- **파일을 지운 것은 없습니다.** 옛 생성기 `figures/_gen_figures.py` 하나만 `mv -n`으로 옮겼습니다(§16 1번). 마감이 새로 만든 파일: `chapter-summary.md`(이 파일) · `gates-after.json` · `before/generators/blocked/_gen_figures.py`(옮긴 것) · 기기 `/tmp/ch21-close/`(04 B 사본) · `.cache/ch21-close/`(마감 전 사본 `pre/`·확인 스크립트 `cpatch.py`·`fpatch.py`·`nbhash.py`·`genmatch.py`·`gate1.py`·`cmpout.py`·`ban_check.py`·`extra_check.py`·`ch29_04_sim.py`·`strict_check.py`·`warn_repro.py`·`noctx.py`·`append_*.py`·치환 목록 `reps/`·그림 확인 사본 `view/`·옛 검사 결과 `oldcheck/`·`dx/`(`llm-practice.zip`을 뺀 전달 검사 사본과 결과)·로그 `log/`).
- **보호 파일 73개(`before-manifest.json`)**: **60개 같음 · 13개 바뀜** — 모두 의도한 것(`manifest-changes.md` 「챕터 마감 끝」): 01~06절이 바꾼 다섯(`_author_ch21_ch29.py`·Part 목록·챕터 목록·계약 파일·계약 기록) + 07절 셋(목차·zip·통합 기록 — 마감에서 다시 씀) + 마감 다섯(`_build_index.py`·`bundle-execution.json`·`visual-results.json`·Ch 22 01 노트북·Ch 22 01 HTML).

## 11. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`numpy>=2.0`·`python-dotenv==1.2.3`·`pillow>=11.0`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`): `langchain-core 1.6.2`·`langgraph-prebuilt 1.1.0`·`numpy 2.5.3`·`pydantic 2.13.5`·`pillow 12.3.0`·`pip 26.2`. 노트북 `%pip`은 모두 잠금 판(01·03·05·06 여섯 · 02·07 + `pydantic` 일곱 · 04 + `langgraph-prebuilt`·`pydantic` 여덟).
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch21-create-agent`(잠금 판) · 모델 `gpt-5.4-mini`(응답 `gpt-5.4-mini-2026-03-17`, `temperature=0`·`reasoning_effort="none"`) · 임베딩 `text-embedding-3-small`(`dimensions=256`). 실행일 모두 2026-09-25(01 06:41 · 02 06:41 · 03 06:42 · 04 06:40 — 마감 새 실행, 05 04:32 · 06 05:11 · 07 05:48 UTC).
- 설치판 소스 행(검토 A·B가 다시 확인): `langchain/agents/factory.py` 28 · 174~194(모델 이름 목록, 186행 `gpt-5.4-mini`) · 583~596(기능 표) · 995~996 · 1024~1036 · 1089 · 1255~1276 · 1357~1367 · 1391~1404(`strict=True`는 도구 쪽) · 1423 · 1431~1436 · 1451~1452 · 1923~1975 · 2004~2037 · `structured_output.py` 284~308 · `middleware/types.py` 349~355 · `tool_node.py` 802~817 · `langchain_core/tools/base.py` 331~340 · `langgraph/prebuilt/chat_agent_executor.py` 57~62·274~277·620~633·744~767 · `langchain_openai/…/base.py` 2427~2428·2433~2436·2482~2494.
- 참고 자료(2026-09-25 확인): LangChain Agents · Structured output(ProviderStrategy `strict` 기본 `None`) · Models(`profile`) · Tools(`ToolRuntime[UserContext]`, 「runtime parameter is hidden from the model」) · Retrieval · v1 migration guide.

## 12. 강사 확인 대상

1. **제목 말**: 01 「create_agent와 ReAct 루프」·03 「AgentState와 context_schema」(마감에서 밑줄을 살림 — 07·챕터 제목과 한 표기)·04 「0.x에서 1.x로 마이그레이션」(본문은 「옮기기」, Ch 23·31 DB 뜻과 다름)·05 「retriever를 도구로 전환」(「검색 함수」로 풂 — LangChain retriever는 객체(`as_retriever()`)라 「검색 부분」 정도로 둘지)·06 「같은 평가셋으로 RAG 비교」·07 긴 부제. 슬러그는 링크·묶음 때문에 그대로.
2. **`ToolRuntime[MemberContext]` 대괄호**(03·07 — 챕터 리드 결정의 예외): 대괄호가 없으면 Pydantic 경고 2건(모델 없이 재현, 공식 문서 모양과 같음).
3. **칸만 적은 라이브러리 클래스 상속 `LibraryState(AgentState)`**(03, `upgrade_allow=["class_def"]` — 게이트 `SCHEMA_BASES`에 `AgentState`를 더할지는 전 챕터 재검사가 듦).
4. **공식 문서에 없는 속성**(`builder`·`channels`·`nodes[…].runnable`·`branches[…][…].ends`·`managed`)을 결정적 비교의 근거로 씀 — 판을 잠가 지금은 돌지만 판을 올리면 먼저 깨질 자리.
5. **06 평가 모델 = 답 모델**(같은 `gpt-5.4-mini` 객체 — Ch 15 02와 같음, b7 한 줄) · 06 판정 설계(근거 충실도 — 준 문서 기준, 정답 문서의 답이라는 뜻 아님) · `fixed_latency_s` 뺌 · 06 삽화 비유 바꿈.
6. **07 실행 2가 03 8절과 같은 값(연체 0 → 3)** — 「새로 볼 것」을 양식 칸까지로 둠(복습 3도 그 관찰로 바꿈 — B-14) · 07 양식 클래스 `LoanAnswer`·문의 글을 새로 정함.
7. **코드 줄 증가**(01 39→124 · 02 33→157 · 03 35→129 · 04 30→142 · 05 35→166 · 06 107→246 · 07 새 절 + 도구 파일 188줄) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 02·03의 사용량·예상 비용 셀 둘은 결론에 닿지 않음(빼면 다시 실행).
8. **01~04 설치 셀 `numpy` — 마감에서 더하고 다시 실행**(챕터 리드 결정). 01~03 흔들린 값은 03의 둘째 단락 넷만 바뀜.
9. **04 모델 요청 0인 절에 키 셀·모델 셀**(모델 객체를 만들 때 키가 필요) · 04 `inspect`·`warnings`·`issubclass` 과정 처음.
10. **삽화(다시 만들지 않음, Higgsfield 0)**: 02-5 오른쪽 셔츠가 틈에서 늘어져 나와 「개어진 채」와 어긋남(그림 읽기는 보이는 대로) · 03-5 회갈색 벽 · 07-4 열쇠(03 카드와 다른 소품 — 마감에서 이음 문장).
11. **Ch 22 01 문장 고침**(A-10 — 완료 챕터의 설명 셀 한 문장, 코드·출력 그대로) · **Ch 22 09 공개 목록 줄**(Ch 22 챕터 목록에 더함).
12. **`chapter.json` 학습 목표 둘 → 일곱**(Ch 29와 같던 두 줄 — 「궤적」 등 — 을 절마다 한 줄 + 07 실습 줄로, `hours` 그대로 16h = 01~06 meta 합) · 실습 폴더 README 다시 쓴 범위.
13. **실습 폴더 `pyproject.toml`의 `pillow>=11.0`**(노트북 import 0) — 보호 파일·잠금 재생성이 들어 그대로 둠(§16).
14. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토 모두 그림 PNG·삽화를 눈으로 보지 못함. 마감은 01-1·02-1·04-2·05-1·06-4를 직접 봄).

## 13. Ch 22(완료)·Ch 23이 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 말: 에이전트를 만드는 함수·에이전트 그래프·ReAct 루프(01) · 도구 전략·제공자 전략·양식 도구(02) · 라이브러리 상태 형식·실행 정보·실행 객체 표시(03) · 옮기기·옛 함수·사용 중단 경고(04) · 검색 함수·검색 도구·검색어(05) · 고정 흐름·에이전트 흐름·비교 기록(06).
- 사실(참, 출력 근거): Ch 22 01 `_src` b3 「Ch21에서는 create_agent() 함수로 에이전트를 만들었습니다」·b4 「Ch21 01절 … 모델을 부르고, 모델이 요청하면 도구를 실행하고, 다시 모델을 부릅니다」 — 01 6절·07로 **참**. **Ch 22 노트북이 쓰는 `from langchain.agents.middleware import AgentState`는 03이 보인 라이브러리 상태 형식과 같은 클래스**(03 출력 `True`). Ch 22 01 노트북 「타입 힌트는 … 실행 결과를 바꾸지 않습니다」는 마감에서 **훅 함수에 한정**(03의 `ToolRuntime` 표시·Ch 20 02 받을 오류 표시는 동작을 바꿈).

### 전제하면 안 되는 것 (Ch 22·23 파일은 Ch 22 01 한 문장 말고 고치지 않았습니다)

1. **Ch 21은 미들웨어·체크포인터·`thread_id`·`interrupt`·스트리밍·`model_settings`·호출 한도를 쓰지 않았습니다.** 다시 검색 「한 번만 더」(05·06)는 시스템 메시지 글의 규칙이지 코드 제한이 아닙니다(코드로 막는 법은 Ch 22 04 몫). 여럿 담기(한 응답에 요청 둘)는 끄지 않았고 끄는 법은 Ch 22 몫.
2. **상태를 넓히는 길**: 03은 `state_schema=`(라이브러리 상태 형식 물려받기)만 보였습니다. 미들웨어 `state_schema`(공식 문서가 권하는 길)는 Ch 22 몫. 03은 `runtime.state`를 실행하지 않았고, 노드·미들웨어용 `Runtime`(Ch 22 훅 매개변수)은 가르치지 않았습니다(`ToolRuntime`만).
3. **결과 상태는 실행 한 번 안에서만 보았습니다** — 저장해 다음 실행에 이어 쓰는 것(체크포인터)은 Ch 23 몫. Ch 23 `_src`·노트북은 Ch 21·`create_agent`를 가리키지 않습니다(`grep` 0건). Ch 21이 뒤 챕터에 넘기는 산출 파일은 06 계약 파일 하나(Ch 29 04만 읽음).
4. **실행하지 않은 것을 전제하지 말 것**: 도구 오류(`ValueError`)를 에이전트 그래프에서 받는 장면(소스로는 기본 오류 처리 인자 — 올라와 멈출 것으로 보임) · 양식 검사 실패 재요청(`handle_errors`) · 한 응답에 규정 요청과 양식 도구 요청이 함께 오는 장면(양식 값이 도구 결과보다 먼저 채워지고 끝남 — 소스 1953~1968·2028~2030행) · 실행 정보 없이 부르기(모델 없는 확인에서 `TypeError`) · 한 응답의 요청 둘을 한 단계에서 함께 실행하는지·단계 수 · 옛 함수 `invoke` · 에이전트가 검색하지 않는 장면.
5. **모델이 채운 값은 「항상」이 아님**: 07 양식 칸 `can_borrow`가 규칙 값과 같았던 것(두 실행·밖 열 번), 06 검색 한 번(15/15), 05 주차 다시 검색 두 번(5/5)은 이번 입력·모델에서 본 것입니다.
6. **`ProviderStrategy`의 `strict`**: OpenAI 계열이면 **함께 싣는 도구 명세**에 `strict=True`가 붙고, 양식(`response_format`) 쪽은 `ProviderStrategy(…, strict=True)`를 줄 때만 `strict`가 켜집니다(02는 주지 않음 — 마감 A-3). 양식 클래스를 그대로 넘기면 기능 표(`profile`)가 참이거나 모델 이름이 정해 둔 목록에 있을 때 제공자 전략(`gpt-5.4-mini`는 둘 다 — A-4).
7. **이름 `AgentState` 셋**: Ch 20 01 우리 상태 형식 · 라이브러리 상태 형식(03, Ch 22와 같은 클래스) · Ch 30 `agent_service/agent.py`의 우리 상태 형식. 뒤 챕터가 이 이름을 쓰면 어느 것인지 적을 것.
8. **「컨텍스트」는 Ch 8 01 뜻(모델이 받은 글 전체)** — `context=` 값은 「실행 정보」. Ch 22 08 「컨텍스트 분리와 Isolate」의 「컨텍스트」는 Ch 22 뜻(확인만).

## 14. 챕터 끝 인계 요약 (Ch 22·23 작업자용 한 줄)

Ch 22(완료)는 Ch 21 01의 `create_agent`·모델 → 도구 → 모델 차례와 03의 라이브러리 `AgentState`에 기대며 모두 참입니다. Ch 23은 Ch 21에 기대지 않습니다.

## 15. 뒤 챕터(Ch 22·27·29·30) 인계 (그 챕터 파일은 고치지 않음 — Ch 22 01 한 문장만 고침)

| 챕터 | 자리 | 지금 글 | Ch 21 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 22(완료) | 01 노트북 설명 셀(셀 4) | 「타입 힌트는 … 표시입니다. 실행 결과는 바꾸지 않습니다.」 | 03 `ToolRuntime` 표시·Ch 20 02 받을 오류 표시는 동작을 바꿈 | **마감에서 고침**(「이 절의 훅 함수에 붙인 타입 힌트는 …」) — §10 |
| Ch 22(완료) | 챕터 `qa/public-files.json` | 09 HTML·노트북 줄 없음 | — | **마감에서 두 줄 더함**(Part 목록도 `collect_public_files.py`로) |
| Ch 22(완료) | 01 `_src` b3·b4 | 「Ch21에서는 create_agent() 함수로 …」·「Ch21 01절 … 다시 모델을 부릅니다」 | 01·07로 참 | 없음 |
| Ch 27 | 01·02 `_src` b3 | 「Ch 21의 create_agent는 모델과 도구의 반복을 만들었습니다」·「Ch 21에서 create_agent에 도구를 전달했습니다」 | 참 | 없음 |
| Ch 29 | 04 `_src` 6·7·9행 · 10행 · 노트북 cell 14·16·18 | §9 표(519.7·1.880·2.094·541) | 계약 파일 새 값 688·1.731·2.003·699(걸린 초는 흔들림) | Ch 29 작업 때 고침 — 걸린 초를 숫자로 둘지부터. 「Agentic RAG」·「지연」 금지어 |
| Ch 29 | 01 `_src` b3(4행) | 「Ch11 평가셋과 Ch21 에이전트를 사용합니다」 | Ch 21 06은 Ch 14 평가 질문(`queries.json`, Ch 11 01 정답 문서 ID 칸 `gold_doc_id`)으로 비교 기록 파일을 씀 — 「Ch11 평가셋」은 느슨함 | Ch 29 작업 때 Ch 29 01이 실제로 읽는 자료를 확인해 고칠지(대기 챕터 — 고치지 않음) |
| Ch 29 | 04 전체 | Ch 21 06 계약 파일을 읽음 | `assert` 셋 PASS, 06 다시 실행 금지 | 계약 유지 · `upgrade-contracts.md` 줄은 Part 마감 |
| Ch 30 | 01 `_src` b3(4행)·`_generate.py` 11행 | 「Ch21에서 Agent **실행 객체**를 만들었습니다」 | Ch 21 03은 「실행 객체」를 **도구 매개변수 `runtime`에 들어오는 객체**로 정함 — Ch 30 01은 에이전트 그래프 뜻 | Ch 30 작업 때 「Ch21에서 에이전트 그래프(`create_agent`의 결과)를 만들었습니다」로(검토 A-11) |
| Ch 30 | 03 `_src` b3 | 「Ch21에서 Agent의 입력과 결과가 상태 사전임을 확인했습니다」 | 뜻은 참(03 입력 상태·결과 키) | 「사전」은 과정 금지어 — Ch 30 몫 |
| Ch 30 | 09 `_src` b3 | 「init_chat_model과 create_agent」 | 참 | 없음 |
| Ch 30 | `agent_service/agent.py` 11행 | `class AgentState(TypedDict)` | 세 번째 같은 이름(§13-7) | 기록만 |

## 16. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-10)

1. **옛 생성기**: `figures/_gen_figures.py`(`77686b7d…`, 01절이 `raise SystemExit`로 막은 판)를 **`qa/upgrade/before/generators/blocked/`로 `mv -n`**(삭제 아님, 해시 같음, 원본 사본 `before/generators/`). 부르는 빌드·검사 스크립트 없음(`grep` — 옛 `final-artifact-hashes.json` 해시 목록과 Ch 23·29 옛 생성기가 자기 챕터에 쓰는 줄뿐), 옮긴 뒤 `_build.py` HTML 여덟 해시 같음. **공용 `textbook/part6/_author_ch21_ch29.py`는 옮기지 않음**(Ch 29가 씀 — Ch 29 작업 뒤 이동, 01절이 넣은 Ch 21 멈춤 줄 그대로).
   - **옮김(Ch 29 마감 2026-09-29)**: `textbook/part6/ch29-agent-evaluation/qa/upgrade/before/generators/blocked/_author_ch21_ch29.py`(`mv -n`, `391be055548853cc…` 같음 — Ch 29 01절이 Ch 29 쪽도 막은 판), 부르는 빌드·검사 스크립트 0(`grep`).
2. **옛 그림 열여덟 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(01~06절 각 셋, 본문 참조 0, 사본 `qa/upgrade/before/figures/`) — 옛 검사 `check_figures.py`가 `.excalidraw` 짝을 요구하는 것과 함께 정할 것.
3. **`gates-wip-*.json` 열일곱 삭제 승인**(`gates-wip-01~07.json`·첫 실행 전 판 `gates-wip-0N-0N.json` 일곱·`gates-wip-ch21-after05~07.json` 셋 — `gates-after.json` 7/7로 갈음, 마감 `run_section.sh`가 `gates-wip-01~07.json`을 끝 값으로 다시 씀) · **`qa/upgrade/__pycache__/`**(생성기 대조 때 생김) · **`labs/…/notebooks/__pycache__/`**(묶음에는 없음).
4. **Ch 29 04 인용값 고치기**(§9 — Ch 29 작업 때) · **`upgrade-contracts.md` Ch 21 06 줄**(Part 6 마감 오케스트레이터).
5. **Part 6 옛 검사 스크립트 넷(고치지 않음, 마감에서 돌린 결과)**: `check_scope.py` — Ch 21 `_src/07-create-agent-실습.html` 「실습 30분」에서 `Missing scope` · `check_figures.py` — `01-1-한-줄이-만든-에이전트-그래프.svg`의 `.excalidraw` 짝 요구 · `check_notebook_readiness.py` — `assert len(reports) == 47`(Part 6 노트북 49), **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림** · `check_visual_reports.py` — Ch 21은 지나가고 `ch22-middleware`(09 줄 없음)에서 멈춤(`assert len(records) == 116`도 Ch 21 여덟 쪽이면 118).
6. **`llm-practice.zip`**: Part 6 `check_delivery.py`가 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`(117행)에서 멈춤(결과 파일 안 바뀜). 사본에서 그 zip만 빼면 HTML 60 · 링크 995 · 누락 0 · 절 49 · 복습 185문항 오류 0 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` 97항목(part6 노트북 49 = 절 49) 통과. `llm-practice.zip` 안 Ch 21은 옛 판 — 전체 묶음 재생성 때.
7. **`textbook/_notebook/build_index.py` 46행**(Ch 21 절 수 6 · 설명) — 전체 목차 마감 때(선례대로 이번에는 고치지 않음). **`textbook/part6/qa/final-artifact-hashes.json`**(Ch 21 줄 43개가 옛 판 — 만드는 스크립트 없음) — 전체 마감 때 다시 모을지.
8. **실습 폴더 `pyproject.toml`**: `pillow>=11.0`(노트북 import 0 — 빌드 도구는 `--with pillow`로 따로 받음)·`numpy>=2.0` 범위 표기(잠금은 2.5.3) — 보호 파일이고 `uv lock`으로 잠금을 다시 만들어야 해서 그대로(검토 B-16 부분 미반영). Part 6 마감 때 다른 챕터와 함께.
9. **Part 6 공용 `visual-results.json`의 Ch 22 01 줄**: Ch 22 01 HTML이 A-10으로 바뀌어 그 줄의 해시가 옛 값 — Ch 22 `visual.cjs`는 이번에 돌리지 않음(한 문장 설명 고침, 레이아웃 영향 없음으로 봄). Ch 22 09 줄도 없음(116 기준) — Part 6 마감 때 Ch 22까지 `visual.cjs`를 다시 돌려 모을 것.
10. **과정 요약·계약 파일(누적 문서 몫)**: Ch 21 용어(§4 — 「실행 정보」 ≠ Ch 8 「컨텍스트」, 「라이브러리 상태 형식」 ≠ Ch 20·30 `AgentState`, 「옮기기」 ≠ DB 마이그레이션)와 도구 파일 `runner_tools.py`·계약 파일 줄은 과정 요약·`upgrade-contracts.md`에 아직 넣지 않음(Part 6 마감 오케스트레이터).
11. **`qa/research.md`·`qa/technical-notes.md`**(2026-09-11)와 `qa/verification.md`·`집필점검표.md` 위쪽 옛 줄: 머리에 「개선 전 판」 표시만 하고 그대로(학생 묶음 밖) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음) · `textbook/part6/qa/language/baseline/ch21-create-agent/`·`language/ch21-ch29-final.json`(옛 감사 기록).
12. **삭제 승인 대상(캐시·임시)**: 실습 폴더 `labs/part6/ch21-create-agent/.venv`(macOS 판)·`.ruff_cache`(있으면) · `notebooks/__pycache__` · `qa/upgrade/__pycache__` · `.cache/ch21-01-view`~`ch21-07-view` · `.cache/ch21-close`(마감 전 사본·확인 스크립트·그림 확인 사본·로그) · `.cache/vm/venv-ch21-create-agent` · 기기 `/tmp/ch21-prep`·`/tmp/ch21-01`~`/tmp/ch21-07`·`/tmp/ch21-close`·`/tmp/nbout.py`·`/tmp/reviewA21`·`/tmp/reviewB21`.
13. **2차 검토**: 두 검토의 「확인하지 못한 것」(한국어 감사 3단, 그림 PNG·삽화 판독, `uv sync --locked`로 만든 학생 `.venv`에서 첫 셀 확인)과 §12.

## 17. 검토 1차와 반영 (2026-09-25 마감)

- 판정: **A(01~03·공통) 중 3 · 하 12**(01 하 2 · 02 중 2·하 4 · 03 하 3 · 공통 중 1·하 3), **B(04~07·공통) 중 3 · 하 14**(04 중 1·하 3 · 05 하 1 · 06 중 2·하 4 · 07 하 4 · 공통 하 2). 상 0.
- **[중] 6건 모두 반영**: A-3(02 `strict` — 도구 명세에 붙고 양식 쪽은 `false`, 모델 없는 요청 글 확인) · A-4(02 전략 고르기 — 기능 표 → 모델 이름 목록 → 도구 전략) · **A-12·B-1(01~04 설치 셀 `numpy==2.5.3` + 다시 실행, 05 1절 문장)** · B-6(06 「바꾼 것은 하나」 → 세 차이를 밝힘, b6·06-4 다시 렌더·06-1 캡션·복습 1·노트북 6절) · B-7(06 「이 챕터는」).
- **[하] 26건 반영**: A-1(01 도구 파일 설명 범위) · A-2(제목 밑줄 — `chapter.json`, 노트북 제목은 이미 밑줄) · A-5(02 표 셋째 줄) · A-6(02-1 라벨) · A-7(02 `tools_to_model` 범위) · A-8(02 기능 표 풀이) · A-9(03 「두 건」·「모델을 부르지 않고」 + 재현 기록) · A-10(**Ch 22 01 한 문장 고침** — 챕터 리드 결정) · A-11(Ch 30 01 — §15 기록) · A-13(색 — **01-1·05-1을 회색으로**, 챕터 리드 결정) · A-14(공개 목록 두 곳 07 줄 + Ch 22 09 줄 · README 전체) · A-15(05 진단·§8에 주석 기록) · B-2(04-2 「견준 여덟 가운데」) · B-3(04 대응표 근거) · B-4(04 용어 셋) · B-5(05 두 번째 검색 문장) · B-8(06 결론 자리) · B-9(06 `assert` 안내) · B-10(06 자리 찾기 문장) · B-11(계약 문서 — §9·체크리스트에 기록, Part 마감 몫) · B-12(07-1 색 — 01-1·05-1을 07-1에 맞춤) · B-13(07 「Ch 2에서 배운 문법」) · B-14(07 복습 3) · B-15(07 비유 이음) · B-16(README 전체·zip — **`pillow` 부분만 미반영**) · B-17(`objectives` 일곱 줄·01/03 제목).
- **반영하지 않은 갈래와 까닭**: **B-16의 `pyproject.toml` `pillow>=11.0` 빼기** — 실습 폴더 `pyproject.toml`·`uv.lock`이 보호 파일이고 `uv lock`으로 잠금을 다시 만들어야 해 이 마감 범위(노트북·글·목록)를 넘음, 게이트와 무관(§16 8번) · A-13의 검토 권고 방향(07-1을 파랑으로)은 챕터 리드 결정(회색)으로 반대쪽을 맞춤 · 뒤 챕터 파일 수정(Ch 29·30 — §15 기록) · 삽화 다시 만들기(02-5 등 — 글만) · 06 다시 실행(계약) · B-6 (나) 「고정 흐름도 시스템 메시지로 보내 다시 실행」 · 02·03 사용량 셀 줄이기(검토 A 「사람이 정해야 할 것」 6 — 강사 확인).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자): 01 `becd09fa7fbb`/`89e69f57f1cd` → **`80151070e4d7`/`f7670f571346`** · 02 `cc31fb4586c9`/`4c4b79dfa046` → **`5a3351792f90`/`afecf4e50d24`** · 03 `0f23718b4749`/`8854500f33cc` → **`fdda5d72aa86`/`ef1392a510bb`** · 04 `55f6505b424a`/`39d8c0c2598a` → **`a83c7aaaa72d`/`4a8d08c4283c`** · 05 `d3898188b127`/`19cc75e8dabc` 그대로 · 06 `ca14949bb0f9`/`1ded374d9f64` 그대로 · 07 `bf48d2353026`/`7f670216e996` 그대로. 일곱 노트북 모두 `metadata.verification`과 다시 계산한 값이 같음, 셀 수 그대로(51·61·53·51·57·68·53).
- **다시 실행한 넷의 바뀐 셀**: 01·02·04 설치 셀(`numpy: 2.5.3` 한 줄)만 · 03 설치 셀 + 흔들리는 값 넷(7·8절 답 글, 출력 토큰 `39`·`76`, 비용 `0.000495`·`0.000668`) → 둘째 단락 두 곳만 고침(생성기 기본값 같게). 결과 읽기 첫 단락·결론·그림·정리·복습 고침 0.
- 고친 방법: 01~04는 생성기(`author_0N.py`) 문자열을 먼저 고친 뒤 `run_section.sh … 0N`(새 커널) — 첫 실행 뒤 02 게이트 G5 1(모델 이름을 백틱으로 인용)·G6 1(긴 판 줄)·G6 1(여섯 문장 단락)은 마크다운만 고쳐 `--no-exec` · 05~07은 마감 전용 `cpatch.py`(생성기·노트북 마크다운·`_src`에 같이 적용 — 코드 셀에 옛 글이 있으면 멈춤, 적용 전 대상별 횟수 확인, 모든 치환에서 코드 셀 0회) → `run_section.sh … 0N --no-exec` · `.mmd` 다섯 다시 렌더 · 캡션 파일 하나(`06-1`). 마감 뒤 생성기 `author_01~07.py`의 `cells()`·`src_html()`이 노트북·`_src`와 글자까지 같음(7/7, 코드 셀 차이 0). 마감이 더한 문장의 금지어 0(마감 전후 금지어 목록 같음), 게이트 G6 0.
- 검사: `upgrade_gates.py … --label after` **7/7 PASS, G1~G7 0** · AST 따로 11건 = 허용 예외 · `verify.py --chapter` **PASS 7 sections / 180 code cells (max 16 lines)** · 빌드 HTML 여덟 `{{` **0건** · `visual.cjs` **16행 PASS** · Part 6 `check_bundle_execution.py` **PASS**(Ch 24 01·Ch 28 01) · Part 6 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(그 zip을 뺀 대조 통과, §16 6번) · Ch 29 04 흉내 검사 **PASS**(계약 파일 `25cfe5df…` 그대로) · 보호 파일 73개 60 같음 · 13 의도한 변경.
