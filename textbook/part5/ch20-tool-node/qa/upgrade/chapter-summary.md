# Ch 20 ToolNode — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part5/ch20-tool-node` 01~04절(품질 개선) + **05절 챕터 끝 실습 절 신설**(`05-ToolNode-실습`), 노트북 `labs/part5/ch20-tool-node/notebooks/01~05-*.ipynb`, 도구 파일 `notebooks/graph_tools.py`.
- 기간: 2026-09-24(준비 조사 · 01~04절 개선 · 05절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 네 절 합계 **182**(01 52 · 02 39 · 03 29 · 04 62, `gates-before.json`) → 마감 뒤 **5/5 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 399·397·398·424·361 = **1,979**).
- 코드 셀 28·25·25·32·25 = **135**(`verify.py --chapter` → `PASS 5 sections / 135 code cells (max 16 lines)`). Mermaid **20장**(01·02·04 넷씩 · 03 다섯 · 05 셋), 삽화 **5장**(절마다 하나, Higgsfield `nano_banana_pro` 14크레딧, 마감 0), 복습 문제는 HTML에만.
- 모델 요청(노트북 한 번씩, 교재 출력 기준): 01 6 · 02 3 · 03 0 · 04 12 · 05 4 = **25번**(모두 `gpt-5.4-mini`, 임베딩 0). 01·04는 모델이 도구를 부르는 수에 따라 달라질 수 있음, 05의 실행 2 두 번은 노트북에서 셀 수 없어 노트북 밖 다섯 번으로 셈. 노트북마다 요금표로 어림한 예상 비용은 0.01달러 아래(청구 금액 아님). **03은 모델·API 키 없이 돕니다**(`check_bundle_execution.py`가 키 없는 학생 묶음에서 실행).
- 화면 검사 `visual.cjs`: HTML **여섯 개**(다섯 절 + `index.html`) × 1280px·390px = **12행 PASS**(`textbook/_notebook/checks/ch20-tool-node/visual-results.json`).
- **마감에서 다시 실행한 노트북은 없습니다.** 다섯 노트북 모두 `code_sha256`·`outputs_sha256`·`executed_at`이 마감 전후 같습니다(마크다운과 05 첨부 그림만 바뀜, §15).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 19 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝의 「검토 반영과 챕터 마감」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」) → 검토 `review-round1-A.md`(01~02·공통)·`review-round1-B.md`(03~05) → 흔들림 확인 `01·02·04·05-probe.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 ToolNode와 tools_condition (experiment) | `from langgraph.prebuilt import ToolNode, tools_condition` · **`StateGraph`에 모델 노드 + `ToolNode(tools)` 등록** · `add_conditional_edges("model", tools_condition, path_map)`(이름표 표 `{"tools": "tools", END: END}` — Ch 13 03 모양) · **되돌아가는 엣지 `add_edge("tools", "model")`**(과정 처음) · `.tools_by_name` · `tools_condition(상태)` 직접 부르기(손으로 만든 응답 둘 → `__end__`·`tools`, `END와 같은가: True`) · **손으로 만든 `AIMessage(content="", tool_calls=[{name, args, id, type}])`**(Ch 13 04 직접 만들기 + Ch 19 04 칸 넷) · `bind_tools(tools, parallel_tool_calls=False)` · `get_graph().draw_mermaid()` · 상태 형식 `AgentState`(메시지 칸 `add_messages` + 흔적 칸 `operator.add`) | 노드 `call_model` · **`call_id_lists`** · **`run_row`**(두 도움 함수는 05절이 도구 파일로 옮김) | 모델 노드 · 도구 실행 노드 · 도구 조건 함수 · 되돌아가는 엣지 (4) |
| 02 도구 오류와 ToolMessage (paired) | **오류 처리 인자 `ToolNode(tools, handle_tool_errors=함수)`** · **오류 처리 함수와 받을 오류 표시 `def handle_policy_error(error: ValueError)`**(02·05에서만 허용한 매개변수 표시) · 기본값 노드가 도구의 `ValueError`를 올려 그래프가 멈춤(Before) · 입력 검사 오류를 노드가 `ToolInvocationError`로 감싸고 기본값 노드는 도구 메시지로 바꿈 · `try/except ToolException as error`로 `ToolInvocationError` 받기 · 시작 엣지를 `START → "tools"`로 옮긴 실험용 그래프 | 노드 함수 없음 · `handle_policy_error` · `build_graph(tool_node)`(노트북 전역에 기대어 도구 파일로 옮기지 않음) | 오류 처리 인자 · 오류 처리 함수 · 받을 오류 표시 (3) |
| 03 recursion_limit과 명시적 종료 (paired) | **설정 딕셔너리 `graph.invoke(상태, {"recursion_limit": N})`**(맨 위 키, 과정 처음) · **`from langgraph.errors import GraphRecursionError`** · 끝점 엣지가 없는 그래프(Before)와 조건 함수가 `END`를 내놓는 그래프(After) · `builder.edges`·**`builder.branches`**(과정 처음) · 상태 형식 `TopicState`(칸 넷) · 한도 경계(노드 K번 흐름은 한도 K+1부터 통과) · **모델 없음** | 노드 `pick_topic`·`find_policy` · 조건 함수 `next_or_end` · `try_limits` | 단계 · 실행 한도 · 설정 딕셔너리 · 명시적 종료 (4) |
| 04 if 분기와 모델 선택 비교 (experiment) | **`add_conditional_edges(START, 조건 함수, path_map)`**(시작점 뒤 조건부 엣지, 과정 처음) · 글 안에 글 `in` · `is not None` · `.usage_metadata` · 도구 파일 `sum_usage`·`estimate_cost` 가져오기 · 입력 몫 예상 비용(`output_rate` 자리에 0을 담은 변수) | 규칙 함수 `keyword_topic` · 조건 함수 `pick_by_rule` · 노드 `make_rule_request`·`call_answer` · `model_responses` · `called_topics` · `compare_row` · **`sum_usage`·`estimate_cost`**(Ch 19 판을 옮김) | 규칙 갈래 그래프 · 모델 선택 그래프 · 결과 편차 (3) |
| 05 ToolNode 실습 | **새 문법·API·말 0개**(01~04 이름만, 이 절이 새로 정의한 함수 0) | — | 0 |

- 새 용어 합계 **14개**(절 meta 「새 용어」 4·3·4·3·0과 같음).
- **이 챕터 주제라서 허용한 문법**(챕터 리드 결정 3·4): 맨 `@tool` · `@tool` 매개변수 `: str` · `@tool` 함수 독스트링 · 필드만 적은 `TypedDict` 상태 형식(`Annotated[…]` 칸) · 02·05 오류 처리 함수의 `error: ValueError`. 노드·도움 함수의 타입힌트·반환 힌트 0.
- **쓰지 않은 것(다섯 절 모두 0건, AST 확인)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`:=`·`next`·`all`·`any`·`sum`·`max`·`min`·`sorted`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·별표 풀기·`isinstance`·`MessagesState`·`'__end__'` 글자·`Literal`·`perf_counter`·시스템 메시지·`tool_choice`·`ToolMessage(…)` 직접 만들기·체크포인터·`create_agent`·미들웨어. 도구 파일의 예외는 `estimate_cost`의 `.get` 둘(Ch 6 06 원본)뿐. 마감 AST 따로(05절 판 `extra_check.py`): 걸린 4건이 모두 허용 예외(02 [39]·05 [21] `error: ValueError`, 도구 파일 `.get` 둘).
- 셀 모양: 코드 셀 최대 16줄은 설치 셀(준비 셀), 준비 셀이 아닌 셀 최대 9줄, 함수 본문 최대 8줄(`call_id_lists`), 셀당 함수 하나, 첫 줄 주석 100%. **모델이 정하는 값(도구 호출 요청·답 글)에 건 `assert` 0건** — 호출 ID 짝·결과 상태·규칙 함수 값처럼 코드가 정하는 값에만.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 13 상태 그래프**: 상태 형식 `class …(TypedDict)`(04) · 메시지 칸 `Annotated[list[AnyMessage], add_messages]`(04) · 흔적 칸 `Annotated[list[str], operator.add]`(02, 노드는 자기 몫만) · 조건 함수 + 이름표 표 `path_map` + 상수 `END`(03) · `draw_mermaid` 구조 문자열(01) · 손으로 만든 `AIMessage`(04). **`MessagesState`는 쓰지 않음**(Ch 13이 가르치지 않음). 칸 구성이 다르면 새 이름(03 `TopicState`).
- **Ch 19 도구**: `@tool`·독스트링·`: str`(01) · 입력 검사·값 검사 오류(02) · `bind_tools`·도구 호출 요청(04) · 도구 메시지·호출 ID·여럿 담기·도구 찾기 표(05) · 오류 담기 설정(`handle_tool_error`, 단수)·결과 상태(06) · 바퀴 한도(Ch 17 03, `turn_limit`). 함수 `tool_call_names`(Ch 19 04)·`show_messages`(Ch 19 06)·`sum_usage`(Ch 19 05)는 Ch 19 `order_tools.py`(`fa5975b5…`) 본문을 글자 그대로 옮김.
- **Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`**(Ch 19 판)와 요금표(2026-09-17, 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러) · 「예상 비용」 = 사용량 × 요금표(청구 금액 아님).
- **Ch 17**: 루프·바퀴·정지 조건(03, 01 b3 「모델의 끝 선택」) · 결정 주체와 자율성 진단표(01·05) — **Ch 17 05 보호 자료 `autonomy-diagnostic-example.json` 12행 「호출 수·비용·결과 편차 비교」 약속을 04가 지킴**(모델 요청 수 · 입력 몫 예상 비용 · 결과 편차 표).
- **Ch 2**: 05 `try/except 오류이름 as error`(안에서 출력만) · **Ch 16 01** `raise`로 오류 내기.
- 소재: 교육센터 자료실 규정 `POLICIES` 셋(대출 「일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.」 · 운영 「평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.」 · 연체 「연체한 일수만큼 새 대출이 제한됩니다.」) + `@tool lookup_policy(topic: str)`(없는 주제어면 `raise ValueError("지원하지 않는 주제: " + topic)`). 절마다 노트북에 다시 적음.

## 3. 절별 사례·값 (새 커널 두 번과 노트북 밖 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값(결론·그림에 쓴 값) | 요청 |
|---|---|---|---|
| 01 | 대출 「자료실에서 일반 도서를 며칠 빌릴 수 있나요?」 · 인사 · 값 바꿔 보기 운영·연체 「자료실 운영 시간과 연체 규정을 함께 알려 주세요.」 | 흔적 `['model', 'model']` / `['model']` / `['model', 'model', 'model']` · 모델 요청 2·1·3 · 도구 메시지 1·0·2 · 인자 `{'topic': '대출'}` / 없음 / 운영 → 연체 · 호출 ID 짝 `True`(인사는 두 목록이 비어 `True` — 마감 A-3) · `tools_condition` → `__end__`·`tools` · 구조 문자열 상자 넷 `tools --> model`(실선) | 6 |
| 02 | 손으로 만든 요청 주차(`hand_call_park`) · 값 바꿔 보기 인자 이름이 틀린 요청(`{'주제': '대출'}`, 질문도 01 대출 질문) | Before(기본값) `받은 오류: ValueError`·멈춤·모델 요청 0 · After(오류 처리 함수) `결과 상태: error`·`호출 ID: hand_call_park`·`요청 id와 같은가: True`·흔적 `['model']` · 인자 이름 요청: 함수 판 `받은 오류: ToolInvocationError`로 멈춤 / 기본값 노드는 `error` 도구 메시지 → 모델이 `{'topic': '대출'}`로 다시 요청 → 흔적 `['model', 'model']` · **이 두 요청에서 두 설정이 받은 오류가 엇갈림**(마감 A-8 — 범위 한정) | 3 |
| 03 | 모델 없는 고르기·찾기 노드 둘, 대출 하나 / 운영·연체 둘 | Before 한도 미기입 `Recursion limit of 10007`(설치판 기본값 — 문서 1000과 다름) · 한도 10 `Recursion limit of 10` · After 흔적 `['pick', 'find', 'pick']`·노드 실행 수 3 · 경계 한도 3 오류·4 통과, 5 오류·6 통과 · 고르기 노드를 지난 수 2·3(바퀴 셈) | 0 |
| 04 | 질문 넷(대출 「… 며칠 대출할 수 있나요?」 · 인사 · 운영·연체 · 값 바꿔 보기 빌림 「… 빌릴 수 있나요?」 = 01 대출 글) × 규칙 갈래 / 모델 선택 | 흔적 `['request', 'answer']` ↔ `['model', 'model']` 등 · 모델 요청 세 질문 1·1·1 ↔ 2·1·3(합 3 ↔ 6) · 입력 토큰 72 / 164·214 · 18 / 160 · 75 / 161·217·260 · 빌림 22 / 164·214(합 165 ↔ 1176, 도구 명세 몫 142) · 입력 몫 `0.000124` ↔ `0.000882` · 규칙 함수 값 `['대출', '', '운영']` · 빌림 질문 규칙 갈래는 도구 쪽에 가지 않음 · **결론은 두 차이(답 노드에 도구를 안 알림 · 되돌아가는 엣지 없음)를 밝히고 배수는 쓰지 않음**(마감 B-4) | 12 |
| 05 | 01 대출 질문 하나 · 실행 1 한도 10 / 실행 2 한도 3(= 실행 1 노드 실행 수) | §7 | 4 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 모델 노드 | 도구를 알려 준 모델에 메시지 칸 전체를 보내고, 받은 응답을 메시지 칸에 더하는 노드(우리가 적는 함수) | `call_model`, 이름 `"model"` |
| 01 | 도구 실행 노드(ToolNode) | 마지막 응답의 도구 호출 요청을 실행하고, 결과를 도구 메시지로 메시지 칸에 더하는 노드(LangGraph가 미리 만들어 둔 노드) | `ToolNode(tools)`, 이름 `"tools"` |
| 01 | 도구 조건 함수(tools_condition) | 마지막 응답에 도구 호출 요청이 있으면 이름표 `"tools"`, 없으면 `END`를 내놓는 조건 함수(노드로 등록하지 않음) | `add_conditional_edges("model", tools_condition, path_map)` |
| 01 | 되돌아가는 엣지 | 뒤에 있는 노드에서 앞의 노드로 다시 가는 엣지 | `add_edge("tools", "model")` |
| 02 | **오류 처리 인자(handle_tool_errors, 복수)** | **도구 실행 노드를 만들 때 넘기는 인자** — 도구를 실행하다 난 오류 가운데 무엇을 받아 도구 메시지로 바꿀지 정함. 기본값 노드는 도구의 `ValueError`를 올리고 입력 검사 오류만 도구 메시지로 바꿈 | `ToolNode(tools, handle_tool_errors=handle_policy_error)` |
| Ch 19 06 | **오류 담기 설정(handle_tool_error, 단수)** — 나란히 적음 | **도구 하나에 붙는 속성** — 그 도구의 `ToolException`만 도구 메시지에 담음(`ValueError`는 켜도 올라옴). **차이: 단수 속성은 도구마다·`ToolException`만, 복수 인자는 노드에 한 번·받을 오류를 우리가 정함** | `도구.handle_tool_error = True` |
| 02 | 오류 처리 함수 | 도구 실행 노드가 넘긴 오류 하나를 받아 도구 메시지에 담을 글을 내놓는 함수 | `handle_policy_error` |
| 02 | 받을 오류 표시 | 오류 처리 함수 첫 매개변수 뒤의 `: ValueError` 같은 표시 — 설치판 노드가 이 표시를 읽어 그 종류만 함수에 넘김(**소스·노트북 밖 확인이 근거, 노트북은 「표시가 `ValueError`인 함수 판이 입력 검사 오류를 받지 않았다」까지만 보임** — 마감 A-7) | `error: ValueError` |
| 03 | 단계 | 그래프가 실행할 노드를 골라 한 번 실행하는 차례(함께 실행되는 노드는 한 단계) — super-step을 풀어 쓴 말 | — |
| 03 | 실행 한도(recursion_limit) | 그래프가 한 번 실행에서 진행할 수 있는 단계 수의 한도, 닿으면 `GraphRecursionError`. **바퀴 한도(`turn_limit`, 모델 요청 수)와 세는 것이 다름** | `{"recursion_limit": N}` |
| 03 | 설정 딕셔너리 | `invoke`의 둘째 인자로 넘기는, 실행하는 방법을 적은 딕셔너리(상태에 들어가지 않음, Ch 13 07 설정 칸과 다름) | `graph.invoke(상태, limit_config)` |
| 03 | 명시적 종료 | 흐름을 끝낼 때를 조건 함수에 적어 두고 그때 `END`로 보내는 것 | `next_or_end` → `END` |
| 04 | 규칙 갈래 그래프 | 우리 코드의 조건 함수가 질문 낱말을 보고 도구 쪽으로 갈지 정하는 그래프(요청은 요청 노드가 손으로 만들고 모델은 답만) | `rule_graph` |
| 04 | 모델 선택 그래프 | 도구를 알려 준 모델이 도구 호출 요청으로 도구를 고르는 그래프 = 01절 그래프 | `model_graph` |
| 04 | 결과 편차 | 같은 질문을 여러 번 보냈을 때 결과가 달라진 정도(달라진 회차 수·답 글 종류 수, Ch 17 05 칸의 말). 두 그래프의 결과 차이 표는 04 b6 실험 결과 표에 따로 있음(마감 B-6) | 노트북 밖 `probe04.py`, 04 b6 표 |

- **일반 말(새 말 아님)**: 메시지 칸 · 실행 흔적 칸 · 이름표 · 손으로 만든 응답/요청(가짜 모델 아님 — 조건 함수·노드에 넣어 보는 값) · 요청 id 목록 · 호출 ID 목록 · 규정 주제어 · 고르기 노드·찾기 노드(03, 「정해 둔 차례를 따르는 우리 노드」 — 마감 B-2) · 규칙 함수·요청 노드·답 노드·입력 몫·도구 명세 몫(04) · 노드 실행 수(05) · 루프·바퀴·정지 조건(Ch 17 03).
- **금지어(다섯 절 설명·주석·캡션·`.mmd` 0건 — 제목·슬러그 말고)**: 「분기」(→갈래) · 「trace」(→실행 흔적) · 「지연」(→걸린 시간) · 「추정 비용」(→예상 비용) · 「반환」(→내놓다) · 「경로」 · 「검증」 · 「전파」 · 「필드」(→칸) · 「측정」 · 「병렬」 · 「프롬프트」 · 「레코드」 · 「사전」 · 「캐시」 단독 · 「로그」 · 「스키마」(→입력 형식) · `MessagesState` · 「super-step」 · 「비상 차단기」 · 「택배 송장」 · 「변동」 · 「벽시계」 · 「최대」 · 「한 겹 더」 · 「돌려주다」류 · 「쉽게·간단히·당연히」 · 「개선 전」 · 「강사 시연」 · Ch 18·19 금지어 전부. 마감이 더한 문장도 같은 목록으로 셈 — 마감 전후 금지어 목록 같음(8줄 — 「프로그램」 안의 「로그」, 슬러그·제목의 「분기」, 옛 그림 캡션 `0N-흐름.caption.md`).
- 제목의 「ToolNode」·「tools_condition」(01)·「ToolMessage」(02)·「recursion_limit」(03)·「분기」(04)는 제목과 본문 첫 풀이에만(강사 확인).

## 5. 색 규칙 (Mermaid 20장, 빨강은 paired Before 결함만)

- **질문·첫 상태·손으로 만든 요청·설정 딕셔너리 초록(tool)** · **우리가 적은 노드·함수·부르는 줄 파랑(flow)** · **실제로 부른 모델 보라(model)**(01-2·05-2는 sequenceDiagram 모델 노드 세로선 `box Lavender` 띠, 02-3 「모델 요청 한 번」, 04·05 모델 노드·답 노드) · **출력으로 확인한 값·받아 출력한 오류 노랑(measure)** · **LangGraph가 준 것(`ToolNode`·가상 시작점/끝점·노드 안 오류 처리 차례)·공통 사실·노트북 밖 값·규칙 셈 회색** · **빨강은 paired Before 결함 결과만**(02-1 멈춤 · 02-3 Before 둘 · 02-4 기본값+주차 · 03-3 Before 셋). experiment 01·04·05는 빨강 0, 02 After·값 바꿔 보기의 `ToolInvocationError` 멈춤과 05 실행 2의 `GraphRecursionError`는 받아 출력한 오류라 노랑.
- **도구 조건 함수·조건 함수는 상자로 그리지 않고** 점선 갈래 라벨로만(구조 문자열 상자 수와 맞춤). 갈래는 점선, 되돌아가는 엣지는 실선. **05-1의 오류 처리 함수는 노드가 아니라서 양옆 세로줄 상자 `[[…]]` + 「이번 흐름에서 쓰이지 않음」**(마감 B-12).
- 원본 viewBox 폭 모두 868 이하(최대 859, 01-3). 넷 이상 한 줄이면 `flowchart TB`, 칸 비교는 subgraph 둘 + `~~~` 회색 공통 상자, 저절로 꺾이는 라벨은 `<br>`로 미리, 노드 id `call`·`end` 금지. **마감에서 다시 렌더한 `.mmd` 셋**: `02-3`(A-11) · `02-4`(A-8) · `05-1`(B-12 — 노트북 첨부 그림, 첨부 PNG 새 판) — 모두 `--force`, PNG를 다른 이름으로 복사해 직접 보고 「도식 읽기」와 맞춤.
- 비유 계열 「자료실 승강 상자」: 01 쪽지가 든 상자와 **파란 책**(= 도구 메시지, 마감 A-6에서 본문 「규정 카드」를 「규정 책」으로) · 02 **빈 회색 카드**(= 결과 상태 `error` 도구 메시지, 책장 빈칸 = 자료 없음) · 03 계수기(칸 수 = 실행 한도)와 창구 층 받침(명시적 종료) — **03 삽화는 성공 결과를 흰 카드로 그림**(강사 확인) · 04 색 점 판·놋쇠 손잡이(규칙) ↔ 흰 쪽지(모델 선택), 파란 책 · 05 받침에 선 상자(쪽지·파란 책)·계수기 등 여섯(한도 10을 줄여 그림, 켜진 셋 = 실행 1 단계 셋)·빈 카드 주머니(오류 처리 함수, 쓰이지 않음). 사람·손·화살표·글자·숫자·끈·톱니·집게(02 2차부터)는 쓰지 않았습니다.

## 6. 서비스 요청과 흔들린 값

- 노트북 한 번 요청: 머리 참고(25번). 작업 전체 서비스 요청(노트북 밖 확인 + 새 커널 두 번): 01 42 · 02 21 · 03 0 · 04 84 · 05 56 = **203번**, **마감 0번**. 요금표로 어림한 예상 비용 합 약 0.058달러(01 0.011 · 02 0.008 · 04 0.022 · 05 0.017, 청구 금액 아님). 삽화 5장 14크레딧(02·05는 1차 탈락 뒤 2차 채택).
- **흔들림 확인(노트북 밖 다섯 번, 규격 §2-7 10번 끝 — 입력·판단 규칙을 첫 요청 전 `NN-probe.md` §0에)**: 01(세 질문 × 5, 15/15 같음) · 02(After 흐름·기본값 노드 흐름, 5/5 — 다시 보낸 요청 `{'topic': '대출'}`) · 04(네 질문 × 두 그래프 × 5 = 40번, 흔적·요청 수·도구 인자·입력 토큰 40/40 같음) · 05(후보 A 주차 → 모델이 첫 요청 열 번 중 여덟 번 주제어 `운영`, 두 번 도구 없음 · B 「주제어 주차로 …」 다섯 번 모두 도구 없음 · **C 대출 5/5 → 채택**). 03은 모델이 없어 흔들림 확인 없음(새 커널 25/25 같음).
- **탐색·설계로 정한 입력(b7에 「흐름을 보여 주려고 정한 예」)**: 01 질문 셋 · 02 손으로 만든 요청 둘·질문 둘·오류 처리 함수 안내 글 · 03 주제어 목록 · 04 질문 넷·규칙 낱말 셋과 차례 · 05 문의(규칙대로 셋째 후보)·실행 2 한도(= 실행 1 노드 실행 수, 코드로 정함).
- **흔들린 값의 자리**: 모든 답 글 · 04 출력 토큰·출력 몫이 든 예상 비용 합(A 규칙 갈래 `0.000731` / B `0.000713`) · 04 빌림 질문 규칙 갈래 답 글(다섯 번 모두 다름, 한 번은 대출 기간을 규정과 다르게) · 05 출력 토큰 46/45·예상 비용 `0.000491`/`0.000486`·답 글 쉼표 하나 · 05 노트북 밖 주차 → 운영 관찰 — 결과 읽기 둘째 단락·「확인할 점」·본문 표·b7에만 「이번 실행에서는」·「교재 출력에서는」으로. **그림 라벨·캡션·정리·복습·본문 결론에서 흔들린 값에서 끌어낸 비교 0건**(마감 확인 — B-5 04 결과 편차 원인 해석 뺌, B-15 05 복습 4에서 노트북 밖 관찰 뺌, B-4 04 「약 일곱 배」 뺌).
- 새 커널 셀별 같음: 01 28/28 · 02 24/25 · 03 25/25 · 04 29/32 · 05 23/25(달라진 셀은 모두 답 글·출력 토큰·그 비용).
- **재지 않은 것**: 걸린 시간(다섯 절 모두, 준비물의 「10초·15초 안에」는 셀 실행 기록) · 청구 금액 · 서비스 오류(429·5xx·시간 제한) · 한 응답의 요청 여럿을 `ToolNode`가 한꺼번에 실행하는 장면(소스로만, 모든 절 `parallel_tool_calls=False`) · 받을 오류 표시를 뺀 함수·`True`·`False` 설정(02 — 노트북 밖 확인만) · 모델 흐름의 통과 쪽 한도(05 한도 4 — 셈만) · 오류 처리 함수가 흐름 안에서 쓰인 장면(05).

## 7. 05절 실습 절 주제와 결과

- 제목 「**ToolNode 실습: 자료실 문의 그래프에 오류 처리 함수와 실행 한도 붙이기**」, 슬러그 `05-ToolNode-실습`(선례 `07-모델과-도구-실습`·`09-Middleware-실습` 규칙 — 챕터 제목 앞말), `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~04 meta 합 강의 1 + 0.75 + 0.75 + 0.5 = **3h** · 실습 1.5 + 1.25 + 1 + 1.25 = **5h** = `chapter.json` 「총 8h · 강의 3h · 실습 5h」(`_build_index.py`도 3·5).
- 붙인 앞 절 기능 셋: **01 그래프**(셀 글자 그대로, 구조 문자열 01 6절과 같은 네 줄) + **02 오류 처리 함수**(`ToolNode(tools, handle_tool_errors=handle_policy_error)`) + **03 설정 딕셔너리·실행 한도·명시적 종료**. 뺀 것: 04 두 그래프 견주기 · 02·03 Before · 01 인사·운영·연체 질문.
- 결과(새 커널 두 번 + 노트북 밖 다섯 번 모두 같음): 실행 1 `{'recursion_limit': 10}` · 흔적 `['model', 'model']` · `success` 도구 메시지 하나 · 인자 `{'topic': '대출'}` · `'모델 요청 수': 2, '도구 메시지 수': 1, '호출 ID 짝': True` · **`노드 실행 수: 3`** · `END`로 끝남 · 사용량 `{'requests': 2, 'input_tokens': 378` / 실행 2 `{'recursion_limit': 3}` · **`받은 오류: GraphRecursionError`** · `Recursion limit of 3 reached` · 흔적·답 글·사용량 받지 못함(노트북 밖 다섯 번: 모델 노드 두 번 뒤 멈춤) / `셈으로 통과하는 가장 작은 한도: 4` · 실행 1 `False` · 실행 2 `True`.
- **오류 처리 함수는 붙여 두었지만 두 실행 모두에서 쓰이지 않았습니다**(대출은 규정에 있는 주제라 도구 오류 없음). 마감에서 이 사실을 학습 목표(「붙여 둔 오류 처리 함수가 이번 흐름에서 쓰였는지, 도구 메시지의 결과 상태로 확인」)·b2·b3 표·05-1 조립도(「이번 흐름에서 쓰이지 않음」)에 올렸습니다(검토 B-8 (가), 제목 유지 — 강사 확인). 이 함수는 도구 몸통이 낸 `ValueError`만 받도록 좁힌 02 판 그대로이고, 한도 오류·입력 검사 오류는 받지 않습니다(b4·b7·복습 4).
- 「노드 실행 수 = 모델 요청 수 + 도구 메시지 수」 셈은 요청을 하나씩만 받을 때(`parallel_tool_calls=False`)만 맞습니다(b7). **노드 실행 수와 같은 한도로는 같은 흐름도 멈추고, 통과하는 가장 작은 한도(+1)에 맞춰도 도구를 한 번 더 부르는 실행은 한도에 닿습니다**(마감 B-9).

## 8. 도구 파일 `notebooks/graph_tools.py` — 함수 표와 해시 변천

| 함수(인자) | 배운 곳 | 가져오는 절 |
|---|---|---|
| `tool_call_names(response)` | Ch 19 04 | 01·02 |
| `show_messages(messages)` — 종류, 응답이면 `| 도구 호출 요청: [...]`, 도구 메시지면 `| 결과 상태: … | 내용: …` 출력(내놓는 값 없음) | Ch 19 06 | 01·02·04·05 |
| `sum_usage(messages)` — `{"requests", "input_tokens", "output_tokens"}`, **손으로 만든 요청(사용량 `None`)을 넘기면 `TypeError`**(04는 `model_responses`로 거름) | Ch 19 05 | 04·05 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06(Ch 19 판) | 04·05 |
| `call_id_lists(messages)` — 요청 id 목록·호출 ID 목록 | **Ch 20 01**(05절이 옮김) | 05(`run_row` 안에서) |
| `run_row(question_name, result)` — 흔적·모델 요청 수(= 흔적 길이)·도구 메시지 수·호출 ID 짝 | **Ch 20 01**(05절이 옮김) | 05 |

- 함수 **여섯**, 함수마다 `# Ch N NN절에서 배웠습니다 — …`, **import 0**, 전역 이름 기대기 0, 금지 문법 0(`.get` 둘은 Ch 6 06 원본 예외), 88줄(주석·빈 줄 뺀 코드 59줄, 모듈 독스트링 포함). 노드·`@tool`·오류 처리 함수·그래프 조립 함수(`build_graph` — 노트북 전역에 기댐)는 노트북에(챕터 리드 결정 1). Ch 19 함수 넷은 `order_tools.py`와, 01 함수 둘은 01 노트북 셀과 소스 조각·AST 모두 같음(검토 A·B 확인).
- **해시 변천**: 없음 → 01 `dd2dd4f8…`(두 함수) → 02·03 그대로 → 04 `45f8d0de…`(+ `sum_usage`·`estimate_cost`) → 05 **`34161a6f5fc7f15d7d15ee6a0e5cb20d6f34eaa76b778521fb14c9f7b0c30061`**(+ `call_id_lists`·`run_row`) → **마감 그대로**.
- 가져오는 절(01·02·04·05)마다 준비 셀 결과 읽기에 고정 세 문장(「앞에서 배운 함수는 `graph_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. …」) + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」. **03은 가져오지 않음**(묶음 키 없는 실행에 영향 없음). 01 [6]은 마감에서 「이 절에서 만드는 `call_id_lists`·`run_row`도 뒤 절이 쓰도록 본문을 글자 그대로 옮겨 두었다」를 더함(A-2).
- 묶음 목록 두 곳(`textbook/part5/public-files.json` 01절 한 줄 · 챕터 `qa/public-files.json` 글롭)에 있고, 마감 zip(`faf00151…`)에 든 판이 디스크와 같음. **Ch 20 실습 폴더 전용**입니다(Ch 21 실습 폴더에 없음). Part 6 선행 목록에는 넣지 않았습니다(Ch 21~ 노트북이 쓰지 않음).

## 9. 의존성 (`pyproject.toml`·`uv.lock`, 바꾸지 않음)

- `dependencies = ["langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`. 잠금에 `langgraph-prebuilt 1.1.0`·`langgraph-checkpoint 4.2.0`·`langchain-core 1.6.2`·`openai 3.11.0`·**`pydantic 2.13.5`**(Ch 20은 pydantic을 고정하지 않아 잠금이 정함 — **Ch 19는 `pydantic==2.12.5` 고정**, 두 챕터 판이 다름)·`tiktoken 0.14.0`·`httpx 0.28.1`·`langsmith 0.12.4`·`pip 26.2`. 노트북 `%pip`은 01·02·04·05 다섯(langgraph·langchain·langchain-core·langchain-openai·python-dotenv), 03 셋(앞 셋), 모두 잠금 판.
- 교재 출력 환경 `.cache/vm/venv-ch20-tool-node`(Python 3.12.13, 잠금과 판 차이 0 — 이 기기에 해당하지 않는 다섯 빼고). 실습 폴더에 `tests/`·`data/` 없음.

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part5/ch20-tool-node/notebooks/01~05-*.ipynb` · `notebooks/graph_tools.py` | 01~05절 · **마감**(노트북 마크다운·05 첨부 그림만) | 실습 폴더(챕터 몫) — §1·§8·§15. 마감은 코드·출력 0 변경. 노트북 파일 `0f848029`→`f65156b6` · `b774711e`→`6154c8b5` · `b92f7378`→`ea1390db` · `e790caf4`→`a5818cf9` · `32252e12`→`8db65a77`. 도구 파일 마감 그대로(`34161a6f…`) |
| `labs/part5/ch20-tool-node/README.md` | 05절(05 단락) · **마감(전체)** | `f6157253…` → **`cfa7e2ca7f285e274e14c89b13c273cd03b3c692173f650abed4df21cb3fd339`**: 노트북 다섯(03 키 없이 · 01·02·04·05 API 키), `uv sync --locked` → `.venv` → `notebooks/`에서 열기(다른 폴더면 `ModuleNotFoundError`), 키는 커널 폴더에서 위로 찾은 첫 `.env`, 패키지 판, 규정 자료는 노트북 안 딕셔너리, 모델 설정(`gpt-5.4-mini`·`temperature=0`·`reasoning_effort="none"`·`bind_tools`·`parallel_tool_calls=False`), 도구 파일 단락(고정 문장 뜻 · 함수 여섯·배운 절·가져오는 절 · Ch 19 `order_tools.py`와 다름 · import 0), 절마다 하는 일, 요청 25번(절별)·예상 비용(청구 아님), 05 단락(오류 처리 함수가 쓰이지 않음 · 실행 2 요청 수). **「예상 비용이 절당 1달러 미만인지 검사합니다」 뺌**, 묶음에 없는 파일을 가리키지 않음 |
| `textbook/part5/public-files.json` | 01절 | `graph_tools.py` 한 줄(`08ee1d6c`→`77511382`, 보호 파일) |
| `textbook/part5/_build_index.py` | **마감** | ch20 설명 「ToolNode와 조건부 엣지로 루프를 조립하고 고정 **분기**와 모델 선택을 비교합니다.」 → 「모델 노드와 도구 실행 노드를 되돌아가는 엣지로 잇고 도구 오류·실행 한도·명시적 종료를 다룬 뒤, 규칙 갈래와 모델 선택을 견주고 자료실 문의 그래프에 오류 처리 함수와 실행 한도를 붙이는 실습을 합니다.」(시수 3·5 그대로, 절 수 칸 없음 — 링크 수로 5절, `246d7dcc`→`b9a443a3`, 보호 파일) |
| `textbook/part5/index.html` · `textbook/downloads/part5-practice.zip` · `textbook/part5/qa/integration-results.json` | 05절 + **마감** | `python3 textbook/part5/_build_index.py` → **`Part 5: 25 verified sections; 65 bundled files`**, zip `6d8846e3…`(05절) → **`faf00151f902de75a951dc603f1a8f8bff56c0cf97602b8bc9732fe50d75ce15`**(68항목, Ch 20 아홉 모두 디스크와 같음, `__pycache__` 0), `index.html` `262d2112`→`b38b67fa`, `integration-results.json` `576a2ca8`→`0691c2e8` |
| `labs/part5/continuity-guide.md` | **마감** | 9행 「노트북의 실행 환경과 예제 데이터는 각 절에서 다시 준비합니다」(도구 파일이 생겨 어긋남) → 「규정 자료는 노트북마다 다시 적고, 앞에서 배운 평범한 함수는 도구 파일 `notebooks/graph_tools.py`에서 가져옵니다」(`0d0237e1`→`75f65db3`, 보호 파일). 같은 줄의 Ch 21·22 문장과 7행 「반환」·9행 「검증」·11행 「측정」은 Ch 20 사실이 아니라 그대로(Part 5 마감 몫) |
| `textbook/part5/qa/bundle-execution.json` | **마감** | `check_bundle_execution.py`가 다시 씀(`1d109972`→`0ab3133f` — 새 zip `faf00151…`, Ch 17 05 · Ch 19 01 · **Ch 20 03 PASS 25 cells, `code_sha256` `877f2261aa0a…`**, 보호 파일). `bundle-execution-summary.json`은 이 스크립트가 쓰지 않는 옛 파일이라 그대로 |
| `textbook/part5/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 이 파일을 다시 써서, 실행 전 사본으로 되돌렸습니다(내용 변경 0, `b87e5028…`) |
| `textbook/part5/qa/ch20-visual-summary.json` · `textbook/part5/qa/visual-summary.json` | **마감** | ch20 행 10 → **12**(05 두 줄, 새 결과로, `dc3959b4`→`c564ea4d`), 합 `checks`·`passed` 60 → **62**(`b071ea4a`→`9afeb9bc`, 다른 챕터 파일 그대로) |
| `textbook/_notebook/checks/notebook-contracts-part5-ch20-tool-node.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(마감 뒤 `d2e6286f…` 그대로) |
| `textbook/_notebook/checks/ch20-tool-node/visual-results.json`(+ 스크린숏 넷) | **마감** | `visual.cjs` 12행(`NODE_PATH=/tmp/pw/node_modules`) |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 20 행 한 줄 · §2-9 Ch 20 항목과 §3·§4 Ch 20 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·계약 파일, 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`build_bundle.py`·`render_mermaid.py`·`attach_figures.py`), Part 5 옛 검사 스크립트와 `check_*` 스크립트, **`textbook/_notebook/build_index.py` 44행**(Ch 20 절 수 4 — Ch 17·18·19 선례대로 그대로), `textbook/part5/practice-start.md`·Part 5 소개 `_src/index.html`, 챕터 `qa/public-files.json`(글롭이라 05·도구 파일이 자동), **Ch 21 이후 파일 전부**(Ch 21·23·26 `_src`·노트북·`labs/part6/continuity-guide.md`·Part 6 선행 목록·`part6-practice.zip`), Ch 17 05 보호 자료, 보호 파일 가운데 아래 다섯 밖의 45개.
- **파일을 지운 것은 없습니다.** 옛 생성기 둘만 `mv -n`으로 옮겼습니다(§14 1번). 마감이 새로 만든 파일: `chapter-summary.md`(이 파일) · `gates-after.json` · `before/generators/blocked/` 둘(옮긴 것) · `.cache/ch20-close/`(마감 전 사본 `pre/`·확인 스크립트 `cpatch.py`·`fpatch.py`·`nbhash.py`·`genmatch.py`·`gate1.py`·`ban_check.py`·`extra_check.py`·치환 목록 `reps/`·그림 확인 사본 `view/`·옛 검사 결과 `oldcheck/`·`dx/`(`llm-practice.zip`을 뺀 전달 검사 사본과 결과)·로그).
- **보호 파일 50개(`before-manifest.json`)**: **45개 같음 · 5개 바뀜** — 모두 의도한 것: `textbook/part5/public-files.json`(01절) · `part5-practice.zip`(05절·마감) · `labs/part5/continuity-guide.md`(마감) · `textbook/part5/_build_index.py`(마감) · `textbook/part5/qa/bundle-execution.json`(마감). Ch 17 05 자료·노트북·HTML, Ch 19 파일, Ch 21~26 `_src`, Part 6 목록, `textbook/_notebook/build_index.py`·`build_bundle.py`, `check_bundle_execution.py`, 옛 검사 넷, `verify.py`·테스트는 그대로.

## 11. 기준 버전·확인 날짜

- 실습 폴더 잠금: §9. **교재 출력 환경 = 잠금 판**(langgraph 1.2.11 · langgraph-prebuilt 1.1.0 · langchain 1.4.0 · langchain-core 1.6.2 · langchain-openai 1.6.0 · pydantic 2.13.5 · python-dotenv 1.2.3).
- 교재 출력: Linux aarch64 · Python **3.12.13** · 모델 `gpt-5.4-mini`(응답 `gpt-5.4-mini-2026-03-17`, `temperature=0`·`reasoning_effort="none"`). 실행일 모두 2026-09-24(01 06:15 · 02 06:47 · 03 07:21 · 04 08:00 · 05 08:34 UTC).
- 참고 자료(2026-09-24 확인): LangGraph Graph API(조건부 엣지 이름표 딕셔너리 · `START` 뒤 조건부 엣지 「conditional entry point」 · 「1.0.6부터 기본 한도 1000」 · `recursion_limit`은 `configurable` 밖 맨 위 키) · `GRAPH_RECURSION_LIMIT` 안내(기본값 안 적음) · Workflows and agents(도구 노드 → 모델 노드 엣지) · ToolNode·tools_condition API 참조(인자 이름·기본값 이름만) · LangChain Tools(도구 오류 예는 미들웨어). 설치판 소스: `langgraph/prebuilt/tool_node.py` 339(`ToolInvocationError(ToolException)`)·383~391(기본값 함수)·444~507(`_infer_handled_types` — 받을 오류 표시)·789(`tools_by_name`)·823(요청 여럿 스레드 실행)·957~967(감싸기)·1002~1012(도구 메시지)·1657~1659(`tools_condition`)행 · `langgraph/_internal/_config.py` 32행(`DEFAULT_RECURSION_LIMIT = 10007`, 환경 변수로 바뀜) · `langgraph/pregel/_loop.py` 607·653·1701·1961행 · `pregel/main.py` 3005행(오류 글) · pydantic 2.13.5 `ValidationError.__mro__` = `ValidationError → ValueError`(마감 확인).

## 12. 강사 확인 대상

1. **제목 말**: 01 「ToolNode와 tools_condition」 · 02 「ToolMessage」 · 03 「recursion_limit」 · 04 「if **분기**와 모델 선택 비교」(「분기」는 제목·슬러그에만, 본문은 「갈래」) · 05 긴 부제. 모두 본문 첫 자리에서 풂. 슬러그는 뒤 챕터·Ch 19 링크 때문에 그대로.
2. **코드 줄 증가**(검토 A-20): 01 88 → 153 · 02 93 → 140 · 03 39 → 131 · 04 144 → 198 · 05 새 절(코드 셀 25) + 도구 파일 88줄 — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 검토는 줄이기를 권하지 않음(줄일 후보: 01 [31] 이름표 표 출력·[43]/[55] 인자 출력·01/02 [49] 마지막 응답 셀 — 재실행 필요).
3. **02 받을 오류 표시 `error: ValueError`**(과정에서 `@tool` 밖 매개변수 표시가 동작을 바꾸는 첫 자리, 02·05에서만) · **A-7 (가) 선택** — 표시가 받는 오류 종류를 정한다는 것은 설치판 소스·노트북 밖 확인이 근거(노트북은 표시가 `ValueError`인 함수 판이 입력 검사 오류를 받지 않은 것까지). (나) 8절에 표시 없는 함수 판 셀을 더하려면 02 재실행·모델 요청 1~2번·02-4 칸 추가.
4. **02 설계**: 시작 엣지를 도구 실행 노드로 옮긴 실험용 그래프(마감에서 「보통 그래프는 01 모양, 05도 01 모양」 한 문장 — A-16) · 값 바꿔 보기에서 질문도 바꿈 · `except ToolException`으로 `ToolInvocationError`를 받음 · **A-9 맺음** — 「도구 몸통이 낸 `ValueError`만 받도록 좁힌 설계 · 둘 다 받는 방법은 실행하지 않음」 문장으로(02·05 b7·05 복습 4).
5. **「오류 처리 인자」(Ch 20, 복수) ↔ 「오류 담기 설정」(Ch 19 06, 단수)** 두 말이 비슷함 — 02 b4 소제목·[38]·복습 3이 가르고, §4 용어 표에 나란히 적음.
6. **03 설계**: 모델 없이 「정해 둔 차례를 따르는 우리 노드」 둘로 01 모양 그래프(마감 B-2에서 「모델 대신」 문구만 고침 — 가짜 모델 아님) · **한도를 적지 않은 Before 셀**(10007단계를 실제로 돎, 약 0.7초, 환경 변수로 기본값을 바꾼 컴퓨터에서는 숫자가 달라짐) · **`builder.branches`**(공식 문서에 없는 속성, 구조 문자열이 없는 점선을 그리는 문제를 피하려고).
7. **04 설계**: `START` 뒤 조건부 엣지(과정 처음) · 규칙 갈래 답 노드에 도구를 알려 주지 않음 · 되돌아가는 엣지 없음(마감 B-4에서 이 두 차이를 결론에 밝히고 「약 일곱 배」 뺌 — 한 변수만 바꾼 실험으로 다시 하려면 04 재실행) · 입력 몫 예상 비용 · 질문 설계(01 글에서 낱말 하나) · 코드 셀 32(상한) · **「결과 편차」 뜻**(04가 정한 「같은 질문을 여러 번 보냈을 때 달라진 정도」 유지, 두 방법의 결과 차이 표는 b6에 따로 — 마감 B-6 한 문장) · b8에 05절 링크를 더함(01~03 b8 모양, B-7).
8. **05 오류 처리 함수를 붙여 두기만 한 설계**(검토 B-8 (가)) — 제목 「… 오류 처리 함수와 실행 한도 붙이기」 유지, 학습 목표·b2·b3 표·조립도에 「쓰이지 않았고 결과 상태로 확인」을 올림. 흐름 안 오류 장면으로 다시 설계하려면(나안) 흔들림 확인부터 재실행·그림 재작업.
9. **05 실행 2**: 요청 수 2를 노트북에서 셀 수 없음(노트북 밖 다섯 번) · 한도 = 실행 1 노드 실행 수(코드로 정함) · 통과 쪽 한도 4는 실행하지 않음 · 코드 셀 25(실습 선례 위 끝).
10. **삽화(다시 만들지 않음, Higgsfield 0)**: 01-5 오른쪽 통로가 아래층 밑으로 더 그려짐 · 02-5 윗 틈 상자가 투표함처럼 보일 수 있음·책장 빈칸 셋(마감 A-17에서 그림 읽기에 빈칸의 뜻과 「글자는 없지만 비유의 카드에는 까닭이 적혀 있다」) · **03-6 성공 결과를 흰 카드로 그림(01·04·05는 파란 책, 02는 빈 회색 카드 — 마감 A-6 연장에서 글은 01·02·04만 책으로 맞추고 03은 그림대로 둠)**·두 통로 사이 파란 기둥 · 04-5 쪽지가 앞 모서리에 걸침 · **05-4 계수기 등 여섯**(한도 10을 줄여 그림 — 마감 B-13 한 문장).
11. 01 손으로 만든 `AIMessage(tool_calls=…)`(처음 합친 모양) · 모든 절 `parallel_tool_calls=False` · 새 용어 수 변화(01 5→4 · 02 4→3 · 04 5→3).
12. **`chapter.json` 학습 목표 셋 → 다섯**(「분기」·「trace」·「지연」·「ToolMessage로 전달」을 빼고 01~04·05 실습 줄, `hours` 그대로 8h = 01~04 meta 합) · 실습 폴더 README 다시 쓴 범위.
13. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토 모두 「확인하지 못한 것」에 그림 PNG·삽화를 눈으로 못 봄을 적음. 마감은 02-3·02-4·05-1·02-5·05-4·01-5를 직접 봄).

## 13. 뒤 챕터 인계

### Ch 21 create_agent가 이어받을 것

- 말: 모델 노드·도구 실행 노드·도구 조건 함수·되돌아가는 엣지(01) · 오류 처리 인자·오류 처리 함수·받을 오류 표시(02) · 단계·실행 한도·설정 딕셔너리·명시적 종료(03) · 규칙 갈래 그래프·모델 선택 그래프·결과 편차(04) · 예상 비용(Ch 6 06 뜻).
- 사실(참): Ch 21 `_src/01-create-agent와-ReAct-루프.html` 3행 b2 「Ch20에서는 model 노드, tools_condition, ToolNode, tools→model 엣지를 직접 연결했습니다」 · 4행 b3 「Ch20에서 직접 연결한 StateGraph와 ToolNode」 · `04-0x에서-1x로-마이그레이션.html` 4행 b3 「Ch20의 직접 조립 그래프」 — 01·05 그래프로 **참**. 05 b8 「Ch 21 01절은 이 챕터에서 직접 이은 반복 구조를 함수 `create_agent` 한 줄로 얻는 법을 다룹니다」(마감 B-14 — 「네 부품」을 「반복 구조」로 좁힘).

### Ch 21이 전제하면 안 되는 것 (Ch 21 파일은 고치지 않았습니다)

1. **`create_agent`가 대신하는 부품을 Ch 20 부품과 같다고 전제하지 않기**: Ch 20은 `create_agent`·미들웨어·체크포인터·`thread_id`·`interrupt`·스트리밍·`MessagesState`·`tool_choice`·**시스템 메시지를 쓰지 않았습니다.** 그래프는 모두 직접 조립(`StateGraph` + `AgentState` — 메시지 칸 `add_messages` + 실행 흔적 칸 `operator.add`)이고, 모델 노드 `call_model`만 흔적 칸에 `"model"`을 남깁니다. 설치판 `langchain/agents/factory.py`는 `ToolNode`와 `"model"`·`"tools"` 노드를 만들지만 갈래는 자체 조건부 엣지로 적고 **`tools_condition`을 가져오지 않습니다**(검토 B-14 확인). 노드 이름·상태 칸·단계 수가 Ch 20 그래프와 같다고 적지 마세요(Ch 21이 소스·출력으로 확인할 몫).
2. **되돌아가는 엣지 실선/점선**: Ch 20 01·05 구조 문자열은 `tools --> model`(**실선**, 고정 엣지). Ch 21 01 노트북 출력의 `create_agent` 구조 문자열은 `tools -.-> model`(**점선**, 137행) — 모양 차이는 Ch 21이 풀 몫. 「같은 되풀이 구조」(상자 넷·엣지 넷)는 참.
3. **Ch 21 01 b2 「create_agent의 세 인자가 Ch20의 모델·도구·지시를 어떻게 묶고, 반환 그래프가 …」**: Ch 20은 **지시(시스템 메시지)를 한 번도 쓰지 않았고**, 「반환」은 과정 금지어(→「내놓는」) — Ch 21 작업 때 고칠 자리.
4. **자료실 소재 `lookup_policy` 규정 글 차이**: Ch 21 01 노트북(152행)의 규정은 「일반 도서는 14일 동안 5권까지 대출할 수 있습니다.」·운영 「평일 09:00~20:00 운영합니다.」(토요일 없음)·없는 주제는 딕셔너리 `KeyError` ↔ Ch 20 `POLICIES`(§2 — 「1인 5권까지 14일 동안」·토요일 10:00~17:00·없는 주제는 `raise ValueError`). 소재를 이으면 글을 맞출지 Ch 21이 정함(Ch 21 05 노트북도 같은 소재).
5. **오류 처리**: `ToolNode(tools, handle_tool_errors=handle_policy_error)`(02·05) — 받을 오류 표시 `error: ValueError`는 02·05에서만 허용. 기본값 노드는 도구의 `ValueError`를 올려 멈추고 입력 검사 오류만 도구 메시지로 바꿈(02). **05 흐름에서 오류 처리 함수가 실제로 쓰인 장면은 없습니다.** 「두 설정이 받는 오류가 반대」는 02의 두 요청 범위(도구 몸통의 `KeyError` 같은 다른 오류는 두 설정 모두 올림 — 소스). 미들웨어 오류 처리(`@wrap_tool_call`)는 Ch 22 몫.
6. **실행 한도**: 설정 딕셔너리 `invoke(상태, {"recursion_limit": N})`(03·05), 노드 K번 흐름은 한도 K+1부터 통과(03 모델 없는 그래프 · 05 모델 흐름에서는 멈추는 쪽만 실행), 한도에 닿으면 `invoke`는 결과를 내놓지 않음, 설치판 기본 한도 10007(문서 1000과 다름). **실행 한도(단계 수) ≠ 바퀴 한도(모델 요청 수)**.
7. **요청 여럿**: 모든 절 `parallel_tool_calls=False` — 한 응답의 요청 여럿을 `ToolNode`가 한꺼번에 실행하는 장면은 소스로만(01). 「모델 요청 수 = 도구 메시지 수 + 1」(01)·「노드 실행 수 = 모델 요청 수 + 도구 메시지 수」(05)는 요청을 하나씩만 받을 때만 맞습니다.
8. **도구 파일 `graph_tools.py`는 Ch 20 실습 폴더 전용**(함수 여섯, import 0). Ch 21 실습 폴더(`labs/part6/ch21-create-agent`)에는 없고, `run_row`의 「모델 요청 수 = 실행 흔적 칸 길이」는 모델 노드만 흔적을 남기는 Ch 20 그래프에서만 맞습니다.
9. **모델 답의 흔들림**: 05 대출 흐름은 밖 5/5·새 커널 2/2 같았지만 「항상」이라 쓰지 마세요. 딕셔너리에 없는 주제(주차)를 물으면 모델이 비슷한 다른 주제어(운영)로 바꿔 찾거나 도구를 부르지 않았습니다(05 노트북 밖 확인 — 오류 처리 함수는 이런 어긋난 답을 막지 못함).

### Ch 23 persistence (대기 챕터 — 고치지 않음)

- `_src/01-체크포인터와-스레드.html` 4행 b3 「Ch20의 도구 반복도 같은 실행 안에서 메시지를 누적했습니다」 — **참**(메시지 리듀서 `add_messages`, 한 번의 `invoke` 안).
- Ch 20 02 b7이 Ch 23을 가리킴: 「멈춘 실행을 다시 이어 가는 방법은 **Ch 23 04절(강제 종료 뒤)과 05절(실패한 단계)**」 · 「같은 쓰기를 한 번만 반영하는 방법은 Ch 23 06절」(마감 A-14 — Ch 23 04 = 강제 종료 뒤 같은 스레드 실제 재개, 05 = 실패 원인을 없앤 뒤 `invoke(None, config)`로 재개, 03 = 정상 종료한 두 프로세스 사이의 대화 재개라 넣지 않음). Ch 23 슬러그를 바꾸면 02 링크 둘·06 링크가 끊김.

### Ch 26 delegation (대기 챕터 — 고치지 않음)

- `_src/01~04` 4행 b3 「Ch20에서 ToolNode와 명시적 END 조건을 … 배웠습니다」 — 01(ToolNode)·03(명시적 종료)·05로 **참**.
- `04-호출-수-비용-종료-조건-비교.html` 5행: 「recursion_limit 같은 **실행 한도**는 비상 경계이며 업무 완료 조건을 대신하지 않습니다」(Ch 20 03 뜻과 맞음, 「비상 경계」는 과정 금지어 「비상 차단기」 계열) · 같은 줄 「운영에서는 ‘최대 세 번 호출’ 같은 **실행 한도**와 …」 — Ch 20 03이 「실행 한도 = 그래프 단계 수」로 가른 말을 **호출 수 상한(바퀴 한도) 뜻**으로 씀 → Ch 26 작업 때 「바퀴 한도」 또는 「호출 한도(Ch 16 04)」로 · 3·6행 「추정 비용」(→「예상 비용」, Ch 6 06 뜻) · 「최대」.

### 완료 챕터가 Ch 20을 가리키는 문장 (고치지 않음, 확인만)

- Ch 7 05 · Ch 17 01·02·03 b7 · Ch 17 05 보호 자료 12행 · Ch 19 05·06·07 b8(「Ch 20에서는 `ToolNode`가 이 실행을 맡습니다」 등) — 모두 01·04로 참, Ch 19 06 b2 → 02 슬러그 그대로라 링크 살아 있음. Ch 19 요약 §13 「Ch 20이 전제하면 안 되는 것」 1~8은 01·02·03 절 작업에서 모두 반영(02 b1 호출 ID는 Ch 19 05로 잇고 「같은 색 집게」 하나로 · 02 b3·b4 단수/복수 구분 · 01 b8 Ch 19 06 잇기 · 「추정 비용」·「지연」 0 · 03 `turn_limit` ≠ `recursion_limit` · 02 흐름 안 입력 검사 오류 장면을 기본값 노드로 보임). `textbook/qa/upgrade-final-checklist.md` §2-8 10번은 끝난 일입니다.

## 14. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-9)

1. **옛 생성기 둘은 옮겼습니다(삭제 아님, 2026-09-24 완료)**: `textbook/part5/ch20-tool-node/qa/author_ch20.py`(`59800f42…`)·`figures/_gen_figures.py`(`d5b3347f…`, 모두 01절이 `raise SystemExit`로 막은 판) → `qa/upgrade/before/generators/blocked/`(원본 사본 `before/generators/`, 옮기기 전후 해시 같음). 부르는 빌드·검사 스크립트 없음(`grep` — 챕터 `qa/public-files.json` `exclude` 글롭 한 줄과 옛 `finalize_evidence.py`가 읽는 `language/ch20-final.json` 해시 목록뿐), 옮긴 뒤 `_build.py` HTML 여섯 해시 같음. **`_build.py`는 빌드 도구**(`_template/builder.py`의 `build_chapter`)라 그대로.
2. **옛 그림 열둘 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(01~04절 각 셋, 본문 참조 0, 캡션에 「분기」·「지연」·「변동」이 남음, 사본 `qa/upgrade/before/figures/`).
3. **`gates-wip-*.json` 열 삭제 승인**(`gates-wip-01~05.json` · 첫 실행 전 판 `gates-wip-0N-0N.json` 다섯, `gates-after.json` 5/5로 갈음 — 마감 `run_section.sh --no-exec`가 `gates-wip-01~05.json`을 끝 값으로 다시 씀) · **`qa/upgrade/__pycache__/`**(`author_0N` 가져올 때 생긴 것) · **`labs/…/notebooks/__pycache__/`**(묶음에는 없음).
4. **코드 쪽 다음 재실행 몫**: 이번 마감에서 코드 셀을 고쳐야 맞는 자리는 없었습니다(모든 고침이 설명·그림·캡션). 다음에 노트북을 다시 실행할 일이 생기면: 02 8절에 표시 없는 함수 판 셀(A-7 (나)) · 04 규칙 갈래 답 노드에 도구를 알려 준 판으로 한 변수만 바꾼 비교(B-4) · 05 흐름 안 오류 장면(B-8 (나)) · 코드 줄 줄이기 후보(A-20)는 강사 결정 뒤.
5. **Part 5 옛 검사 스크립트 넷(고치지 않음, 마감에서 돌려 본 결과 — 모두 Ch 20에 닿기 전 멈춤)**: `check_scope.py` — Ch 17 `06-Agent-개요-실습.html` 「실습 30분」에서 `Missing scope`(`SECTION_COUNTS` ch20 = 4 ≠ 5도 걸림) · `check_figures.py` — Ch 17 `01-1-고른-쪽으로-가르기.svg`의 `.excalidraw` 짝 요구 · `check_notebook_readiness.py` — `assert len(reports) == 21`(Part 5 노트북 25), **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림** · `finalize_evidence.py` — Ch 18 `_src/01-게이트가-있는-프롬프트-체이닝.html` 감사 해시에서 멈춤(Ch 20 `language/ch20-final.json` 해시도 개선으로 어긋남). 결과 파일은 `notebook-readiness.json` 말고 바뀌지 않음.
6. **`llm-practice.zip`**: Part 5 `check_delivery.py`가 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`(115행)에서 멈춤(결과 파일 안 바뀜, `a4465793…`). 사본에서 그 zip만 빼고 결과 파일 없이 돌리면 **HTML 31 · 링크 579 · 누락 0 · 절 25 · 복습 100문항 오류 0 · 비밀값 0 · `part5-practice.zip` `faf00151…` 68항목(part5 노트북 25 = 절 25) 통과**. `llm-practice.zip` 안 Ch 20은 옛 판(노트북 넷·README·잠금, `graph_tools.py`·05 없음).
7. **`textbook/_notebook/build_index.py` 44행**(Ch 20 절 수 4 · 설명) — 전체 목차 마감 때 `chapter.json`·`textbook/part5/_build_index.py` 새 설명과 맞출 것(Ch 17·18·19 선례대로 이번에는 고치지 않음).
8. **`labs/part5/continuity-guide.md`**의 Ch 20 밖 문장(7행 「반환」·9행 Ch 22 「검증」·11행 「측정」) — Part 5 마감 몫.
9. **뒤 챕터 문장**(§13): Ch 21 01 b2 「지시」·「반환」, 규정 글 차이, `create_agent` 그림 점선 · Ch 26 04 「실행 한도」(호출 수 뜻)·「비상 경계」·「추정 비용」·「최대」 — 그 챕터 개선 때.
10. **`qa/research.md`·`qa/technical-review.md`**(2026-09-10)와 `qa/verification.md`·`집필점검표.md` 위쪽 옛 줄: 학생 묶음 밖 기록이라 머리에 「개선 전 판」 표시만 하고 그대로 · `qa/upgrade/review-pack/`은 마감 전 판(검토에 쓴 묶음 — 다시 만들지 않음) · `bundle-execution-summary.json`(옛 파일, 스크립트가 쓰지 않음).
11. **과정 요약·계약 파일(누적 문서 몫)**: Ch 20 용어(§4 — 「오류 처리 인자」 ↔ 「오류 담기 설정」, 「실행 한도」 ≠ 「바퀴 한도」, 「결과 편차」)와 도구 파일 `graph_tools.py` 줄은 과정 요약·`upgrade-contracts.md`에 아직 넣지 않았습니다(Part 5 마감 오케스트레이터 몫).
12. **삭제 승인 대상(캐시·임시)**: 실습 폴더 `labs/part5/ch20-tool-node/.venv`(macOS 판 175MB)·`.ruff_cache` · `notebooks/__pycache__` · `qa/upgrade/__pycache__` · `.cache/ch20-01-view`~`ch20-05-view` · `.cache/ch20-close`(마감 전 사본·확인 스크립트·그림 확인 사본·로그) · `.cache/vm/venv-ch20-tool-node`(238MB) · 기기 `/tmp/ch20-prep`·`/tmp/ch20-01`~`/tmp/ch20-05`·`/tmp/reviewA20`·`/tmp/reviewB20`.
13. **2차 검토**: 두 검토의 「확인하지 못한 것」(한국어 감사 3단, `uv sync --locked`로 만든 학생 `.venv`에서 첫 셀 확인)과 §12.

## 15. 검토 1차와 반영 (2026-09-24 마감)

- 판정: **A(01~02·공통) 중 4 · 하 16**(01 accept with fixes 중 1·하 5 · 02 중 3·하 8 · 공통 하 3), **B(03~05) 중 3 · 하 16**(03 수락 하 3 · 04 조건부 수락 중 1·하 3 · 05 조건부 수락 중 2·하 7 · 공통 하 3). 상 0.
- **[중] 7건 모두 반영**: A-1(01 셈의 까닭에 여럿 담기를 끈 조건) · A-7 (가)(02 표시 효과는 소스·노트북 밖 근거, 결과 읽기·목표·복습·b6 범위를 좁힘, 02 재실행 안 함) · A-8(02-4 공통 상자·b6·복습 4·캡션을 사실대로 — 원래 오류는 `ValueError`의 한 종류, 아닌 것은 감싼 `ToolInvocationError`, 엇갈림은 두 요청에서만, `.mmd` 다시 렌더) · A-9(02·05 b7·05 복습 4 「좁힌 설계」) · B-4(04 「바꾼 것 하나」 → 두 차이를 밝힘, 배수 뺌) · B-8 (가)(05 학습 목표·b2·b3·조립도에 「쓰이지 않음·결과 상태로 확인」) · B-9(05 딱 맞춘 한도는 같은 흐름도 멈춤).
- **[하] 32건 모두 반영**: A-2 · A-3 · A-4 · A-5 · A-6(+ 02·04 비유 「카드 → 책」, 04 결과 편차 비유) · A-10 · A-11(`.mmd`) · A-12 · A-13 · A-14(Ch 23 04·05) · A-15 · A-16 · A-17(그림 읽기·`02-figures.md`) · A-18(`chapter.json` `objectives`·`index.html` — 제목 「분기」만 남음) · A-19(README 전체) · A-20(판단만 — 강사 확인 §12 2) · B-1 · B-2(문구, 설계 유지 — 강사 확인) · B-3(묶음 실행 검사·03 진단 문장) · B-5 · B-6(가능성·「안내 화면」·결과 편차 한 문장) · B-7(04 b8 링크) · B-10 · B-11(+ 노트북 7절 앞 문장) · B-12(`.mmd`) · B-13(그림 읽기 — 다시 만들지 않음) · B-14 · B-15 · B-16 · B-17(`objectives`·`_build_index.py` 설명) · B-18(README) · B-19(뒤 챕터 몫 — §13에 기록). 검토 A 끝 「뒤 챕터가 Ch 20에 기대는 문장」 표도 §13에 옮김.
- **반영하지 않은 갈래와 까닭**: A-7 (나)·B-8 (나)(재실행·요청 증가 — 챕터 리드 결정 (가)) · A-20 코드 줄 줄이기(셀을 줄이면 재실행 — 강사 확인) · B-4의 한 변수 실험 다시 하기(04 재실행) · 삽화 다시 만들기(B-13·A-17 — 글만) · 03 한도 없는 Before 셀·`builder.branches`(설계 유지 — 강사 확인) · 뒤 챕터 파일 수정(Ch 21·23·26 — §13 기록). **코드 셀을 바꿔야 맞는 지적은 없었습니다.**
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자, **모두 그대로**): 01 `836cc6492589`/`8b2c88251b19` · 02 `04dc67fc0329`/`aad8f31985cc` · 03 `877f2261aa0a`/`d0339818f64c` · 04 `b0920807d041`/`a0bcc06b99fd` · 05 `6408399ee855`/`1daf319fbe87`. 다섯 노트북 모두 `metadata.verification`과 다시 계산한 값이 같고 `executed_at` 그대로, 셀 수 그대로(61·59·58·69·55), 바뀐 것은 마크다운과 05 첨부 PNG뿐. 노트북 파일 해시는 §10 첫 줄.
- 고친 방법: 마감 전용 `cpatch.py`(생성기·노트북 마크다운·`_src`에 같이 적용 — 코드 셀에 옛 글이 있으면 멈춤, 적용 전 대상별 횟수 확인, 모든 치환에서 코드 셀 0회) → `run_section.sh … NN --no-exec` 다섯 번 → 캡션 파일 둘(`02-4`·`05-1`)을 `_src`와 같게(캡션 25개 모두 같음 확인) → `.mmd` 셋 `--force`. 마감 뒤 생성기 `author_01~05.py`의 `cells()`·`src_html()`이 노트북·`_src`와 글자까지 같음(5/5, 코드 셀 차이 0). 마감이 더한 문장의 금지어 0(마감 전후 금지어 목록 같음), 게이트 G6 0.
- 검사: `upgrade_gates.py … --label after` **5/5 PASS, G1~G7 0** · AST 따로 4건 = 허용 예외 · `verify.py --chapter` **PASS 5 sections / 135 code cells (max 16 lines)** · 빌드 HTML 여섯 `{{` **0건** · `visual.cjs` **12행 PASS** · Part 5 `check_bundle_execution.py` **PASS**(Ch 17 05 29셀 · Ch 19 01 21셀 · **Ch 20 03 25셀**, 모두 `notebooks/`에서 `code_sha256` 같음) · Part 5 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(알려진 일 — 그 zip을 뺀 대조 통과, §14 6번) · Part 6·7 묶음(`part6-practice.zip` 95항목·`part7-practice.zip` 111항목)과 Part 6 선행 목록에 Ch 20 파일 0.
