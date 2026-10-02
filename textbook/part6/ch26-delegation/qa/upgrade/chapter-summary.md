# Ch 26 위임 구조 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part6/ch26-delegation` 01~04절(품질 개선) + **05절 챕터 끝 실습 절 신설**(`05-위임-구조-실습`), 노트북 `labs/part6/ch26-delegation/notebooks/01~05-*.ipynb`, 도구 파일 `notebooks/delegation_tools.py`. 뒤 챕터가 읽는 계약 파일(산출 파일)은 없습니다.
- 기간: 2026-09-28(준비 조사 · 01~04절 개선 · 05절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 네 절 합계 **128**(G1 8 · G2 4 · G4 3 · G5 24 · G6 77 · G7 12 — 01 28 · 02 31 · 03 31 · 04 38, `gates-before.json`) → 마감 뒤 **5/5 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 393·463·390·477·321 = **2,044**).
- 코드 셀 28·31·25·30·21 = **135**(`verify.py --chapter` → `PASS 5 sections / 135 code cells (max 19 lines)` — 19줄은 준비 셀). 코드 줄(`count_code.py`, 주석·빈 줄 뺌) 42·37·37·109 → **145·199·170·223 + 05 새 절 127 = 864**, 도구 파일 70줄. Mermaid **21장**(01 다섯 · 02 다섯 · 03 넷 · 04 넷 · 05 셋), 삽화 **5장**(절마다 하나, Higgsfield — 03만 재생성 1회, 마감 0), 복습 문제는 HTML에만.
- **모델 요청**: 다섯 절 모두 실제 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`). 02·03은 앞 절반(02 2~5절 · 03 2~4절)이 모델 없는 구조라 그 구간은 요청 0·키 없이 돎. 노트북 한 번 **6 · 3 · 3 · 11(+ 서비스가 거절하는 요청 1) · 5**번. 작업 전체(노트북 밖 흔들림 확인 + 새 커널 A·B, 기록 `probe/*.jsonl`과 진단으로 다시 셈) **01 54 · 02 21 · 03 21 · 04 82(+ 거절 12) · 05 95 = 273번(+ 거절 12)**, 마감 **0번**. 예상 비용 합 약 **0.095달러**(요금표 2026-09-17로 어림, 청구 금액 아님 — 01 약 0.019 · 02 약 0.0077 · 03 약 0.0052 · 04 약 0.029 · 05 약 0.034).
- 화면 검사 `visual.cjs`: HTML **여섯 개**(다섯 절 + `index.html`) × 1280px·390px = **12행 PASS**(기기 `/tmp/pw`에 playwright 1.63.0, `/tmp/pw-browsers`에 chromium-headless-shell — §10).
- **마감에서 다시 실행한 노트북: 없음.** 다섯 노트북 모두 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같습니다(마크다운만 — §17).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 25 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-28)」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」)·`NN-probe.md`(노트북 밖 흔들림 확인) → 검토 `review-round1-A.md`(01~02·공통)·`review-round1-B.md`(03~05) → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 Subagent 도구 위임 (experiment) | **에이전트를 도구로 감싸기** — `@tool` 함수 안에서 도구 없는 전문 에이전트(`create_agent`)를 넘긴 글 한 줄로 시작한 새 목록으로 `invoke`, 마지막 답 글(`.text`)을 내놓음 · 도구 함수가 안쪽 결과 메시지를 노트북 기록 목록 `specialist_runs`에 붙임 · **안쪽 목록 ↔ 바깥 목록**을 나란히 출력(두 목록 시스템 메시지 0, 이어지는 자리는 넘긴 글 하나와 답 글 하나 — `True` 둘) · `supervisor.config["recursion_limit"]`(9999) → `invoke(입력, {"recursion_limit": 10})` · 이번 실행이 더한 바깥 메시지만 자르기 `목록[n:]` · 앞 차례 기록 두 줄을 손으로 붙인 실행(바깥만 늘고 안쪽 그대로) | **`message_kinds`**·**`usage_with_specialists`**(이 절이 처음 가르침 — 04가 도구 파일로 옮김) · 도구 `ask_loan_desk`(노트북) | 서브에이전트 · 중앙 에이전트 · 전문 에이전트 · 바깥 목록/안쪽 목록 (4) |
| 02 Handoff 상태 전환 (experiment) | 앞 절반(모델 없음): **`Command(goto=…, update={"active_agent": …})`**로 담당 넘기기 · `add_node(…, destinations=…)`(Ch 13 06) · `START` 뒤 조건 함수 `pick_desk`(Ch 20 04)가 저장된 담당 칸으로 첫 노드를 고름 · `compile(checkpointer=InMemorySaver())`·스레드·`get_state(…).values`·`.next`(Ch 23 01) · 없는 노드 이름 `goto` → 경고만(`pregel/_algo.py` 311~313행, 표준 `logging`) · **하위 그래프**(`add_node`에 컴파일한 그래프) · 손으로 만든 도구 요청 응답(Ch 20 01)으로 도구 메시지 짝 검사(지금 그래프 `ValueError` ↔ **`graph=Command.PARENT`**는 검사 없음) · 뒤 절반(실제 모델): 넘기기 도구 `transfer_to_interlibrary(runtime: ToolRuntime)` — **`runtime.state["messages"][-1]`·`runtime.tool_call_id`**로 요청 응답과 `ToolMessage`를 함께 담아 `Command(…, graph=Command.PARENT)` · `create_agent(…, name=…)`(응답의 칸 `name`) · 에이전트 그래프를 바로 노드로 넣은 바깥 그래프(구조 문자열 `draw_mermaid()`가 2절과 같음 `True`) | **`writer_names`**(04가 옮김) · 노드 `loan_desk`·`interlibrary_desk`·`pick_desk`·도구 둘(노트북) | 핸드오프 · 담당 칸 · 하위 그래프 · 넘기기 도구 (4) |
| 03 Router 분류와 병렬 실행 (experiment) | 앞 절반(모델 없음): 조건 함수가 **`Send` 목록**을 내놓아 고른 분야 노드만 실행(Ch 13 05 팬아웃 되짚기) · 답 칸 `Annotated[list[dict], operator.add]` 이어 붙이기(분야 이름을 함께 담아 차례에 기대지 않음) · `get_state_history`의 `metadata["step"]`·`next`로 두 분야 노드가 **같은 단계 2**에서 실행된 것을 봄 · 빈 분류(`Send` 0개 → 종합 노드 안 돌고 조용히 끝남, 경고도 없음) · 뒤 절반(실제 모델): 양식 클래스 `DeskChoice(BaseModel)` 칸 `list[Literal[…]] = Field(…)`(Ch 21 02) · `with_structured_output(…, include_raw=True)`(Ch 6 03) · 분야 노드가 도구 없는 전문 에이전트 셋 `desk_agents`를 부름 · 코드 종합 노드 | **`send_to_desks`**(04가 옮김) · 노드 `classify_by_words`·`desk_reply`·`join_answers`·`classify_by_model`·`ask_desk`(노트북) | 라우터 · 분류 노드 · 분야 노드 · 종합 노드 (4) |
| 04 호출 수·비용·종료 조건 비교 (experiment) | 같은 문의·같은 전문 에이전트(R1)로 세 구조 한 번씩 · 서브에이전트는 분야 이름을 받는 도구 하나 `ask_desk_agent(desk, question)`(공식 single dispatch tool) · 핸드오프 안내 담당 `front_desk` + 넘기기 도구 `transfer_to_desk(desk, runtime)` → **실제 서비스 400**을 `try/except ModelInvalidRequestError`로 받아 `error.status_code`·`error.body["message"]` 출력, 바깥 그래프 체크포인터로 멈추기 전 기록 읽기 · **`ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")`**(Ch 22 04 — 한도를 붙인 에이전트 요청만 셈, 한도 글 응답 사용량 `None`) · 모델 없는 핑퐁 그래프 + `{"recursion_limit": 4}` → `GraphRecursionError` · **완료 조건 함수** · `typing_extensions` 한 줄 가져오기 | **`answered_desks`**·**`is_complete`**(05가 옮김) · `bounce`·도구 둘(노트북) | 완료 조건 (1) |
| 05 위임 구조 실습 | **새 문법·새 API·새 말 0**(01~04 노트북·도구 파일과 AST 대조) · 새 가져오기는 도구 파일로 옮긴 04 함수 둘 | 조립 함수 `handle_inquiry`·기록 장치 `count_run_usage`·`summarize_run`(노트북) | 0 |

- 새 용어 합계 **13개**(절 meta 「새 용어」 4·4·4·1·0).
- **이 챕터 주제라서 허용한 문법**: 맨 `@tool` 줄 + 매개변수 `: str`·`runtime: ToolRuntime`(대괄호 없음 — 02 셀 51에 Ch 21 03 `ToolRuntime[MemberContext]`와의 차이 한 문장) · 칸만 적은 `TypedDict` 상태 형식(칸 구성이 바뀌면 새 이름 — `DeskState`·`TeamState`·`RouteState`·`ModelRouteState`) · `BaseModel` 양식 클래스(03·04) · `try/except 오류 이름` 세 셀(02 `ValueError` · 04 `ModelInvalidRequestError`·`GraphRecursionError`) · 도구 파일 `estimate_cost`의 `.get` 둘(Ch 6 06 본문 그대로). 마감 AST 따로(`extra_check.py`) 금지 문법 0(허용 표시 넷뿐).
- **쓰지 않은 것**(다섯 절·도구 파일 모두 0건): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`set`·노트북 `.get`·`+=`·`while`·기본값 매개변수·반환 힌트·대입 풀기·별표 풀기·세미콜론·`isinstance`·`join`·식 안 요금 숫자·**`stream`·`astream`·비동기 서브에이전트·`parallel_tool_calls`·미들웨어 핸드오프 모양·`langgraph-supervisor`**.
- 셀 모양: 준비 셀 밖 셀 10줄 이하, 함수 본문 8줄 이하, 셀당 정의 하나, 첫 줄 주석 100%, 호출 깊이 최대 2. `assert`는 키 셀에만(모델 판단·모델 글·완료 조건에 0).

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 6 01·03·06**: 모델 설정(`init_chat_model`·`temperature=0`·`reasoning_effort="none"`) · `with_structured_output(…, include_raw=True)`(03) · **`estimate_cost`와 요금표**(01·04·05, Ch 21 `runner_tools.py` 판 글자 그대로).
- **Ch 8 03**: 나누기(Isolate) = 01의 안쪽 목록 모양(01 b3 한 문장) · **Ch 22 08** 컨텍스트 분리는 같은 생각(되풀이하지 않음).
- **Ch 13 04·05·06**: `add_messages`(02 `TeamState`) · `Send`·팬아웃·이어 붙이기 규칙(03) · `Command(update=, goto=)`·`destinations`(02). **`Command` 세 쓰임 가르기 한 문장**(Ch 13 06 `goto` · Ch 24 01 `resume` · Ch 26 02 `graph=Command.PARENT`)은 02 b4·노트북 셀 53.
- **Ch 16 04·Ch 22 04**: 호출 한도(`ModelCallLimitMiddleware` 이름 그대로) · **Ch 17 03**: 정지 조건 넷(04 b4 표 — 완료 조건과 가름) · **Ch 20 01·03·04**: 손으로 만든 도구 요청 응답 + `ToolNode`(02 5절) · 실행 한도 `recursion_limit` · `START` 뒤 조건부 엣지(02).
- **Ch 18 02·03·04**: 라우팅(03 — 「라우터는 라우팅을 하는 쪽」) · 함께 보내기(03 제목 「병렬 실행」의 풀이) · 작업 나눠 맡기기(01 b3 가르기 문장 — 코드가 정함 ↔ 중앙 에이전트의 모델이 정함).
- **Ch 19 01·04·05·06**: `@tool`·독스트링 도구 설명 · `tool_call_names`·도구 요청 칸 넷 · **`sum_usage`**(목록 안 `AIMessage`를 모두 요청 하나로 셈 — 손으로 적은·한도 글 응답은 사용량 `None`이라 멈춤)·호출 ID 짝 · `show_messages`.
- **Ch 21 01·02·03**: `create_agent`·에이전트 그래프 노드 · `Literal` 양식 칸 · `ToolRuntime`(02가 새 속성 `state`·`tool_call_id`를 읽음). 01 규정 글의 대출·연체 문장은 Ch 21 01 `POLICIES` 그대로, 03 시설 규정의 시각은 Ch 21 01 「운영」.
- **Ch 23 01**: `InMemorySaver`·스레드·`get_state`·`get_state_history`·체크포인트 단계 번호(02·03·04) · Ch 23 02·03 다른 체크포인터는 02 b7에 이름만.
- **Ch 24 01·04**: `Command(resume=…)`(가르기 문장의 한 쓰임) · 대출 연장 7일(01 규정 글 연장 문장).
- **Ch 25 04**: 01·05 문의 글 「빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?」 · Ch 26 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」류 문장은 참(Ch 26은 스트리밍 0건).
- 소재: **도서관 자료실 문의 창구**(Ch 20~25를 이음) — 전문 담당 셋 `loan_desk`(대출 규정)·`interlibrary_desk`(상호대차)·`facility_desk`(시설), 규정 글 셋은 모두 「교재용」 표시(01 연장 두 문장 · 02 상호대차 세 문장 · 03 시설 한 문장을 이 챕터가 정함 — 각 b7).

## 3. 절별 과제·값 (새 커널 두 번과 노트북 밖 흔들림 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값·두 커널과 흔들림 확인 5/5가 같았던 값(결론·그림에 쓴 값) |
|---|---|---|
| 01 | 중앙 에이전트 `supervisor`(도구 `ask_loan_desk` 하나) + 도구 없는 대출 규정 담당, 문의 한 줄(4·5절) → 앞 차례 기록 두 줄 + 문의(6절, 값 바꿔 보기) | 기본 실행 한도 `9999`·준 한도 `10` · 중앙 노드 `['__start__', 'model', 'tools', '__end__']` · 한 번 맡김(밖 10/10) · 바깥 `['HumanMessage', 'AIMessage', 'ToolMessage', 'AIMessage']` 4줄 · 안쪽 `['HumanMessage', 'AIMessage']` 2줄 · 시스템 메시지 `0 0` · 두 `True` · 바깥만 센 요청 `2`·안쪽 `1`·합 `3`(중앙 2 + 전문 1) · 6절 바깥 6줄·안쪽 2줄·`False`·요청 3 |
| 02 | 앞 절반: 두 담당 노드 + `pick_desk` + 체크포인터, 같은 스레드 두 글 → 새 스레드(값 바꿔 보기) · 이름 오타 · 도구 메시지 없는 넘기기 두 도구 / 뒤 절반: 두 담당 에이전트 + 넘기기 도구, 같은 스레드 두 차례 | 구조 문자열 화살표 다섯 · 첫 차례 흔적 `['loan_desk', 'interlibrary_desk']`·저장 담당 칸 `interlibrary_desk`·다음 노드 `()` · 둘째 차례 `['interlibrary_desk']` · 새 스레드 `['loan_desk']` · 오타: 경고 한 줄·답 칸 빈 글 `True`·담당 칸만 `interlibrary_desk` · `ValueError` ↔ PARENT 목록 `Human·AI(요청)·AI`(요청 응답을 바깥 입력에 손으로 넣은 장면) · 7절 구조 문자열 같음 `True` · 응답을 쓴 담당 `['loan_desk', 'interlibrary_desk']` · 짝 `True` · 요청 `2`/`1`(밖 5/5 첫 차례에 넘김) |
| 03 | 앞 절반: 글자 규칙 분류 + `Send` + 이어 붙이기, 두 분야 문의 → 빈 분류 문의(값 바꿔 보기) / 뒤 절반: 분류 모델 + 전문 에이전트 셋 | `분야 칸: ['loan_desk', 'facility_desk']` · 체크포인트 `1 \| ('loan_desk', 'facility_desk')`·`2 \| ('join_answers',)`·`3 \| ()` · 빈 분류 `분야 칸: []`·답 칸 0·종합 빈 글·단계 1에서 끝남 · 모델 분류 두 분야(밖 5/5)·답 칸 2줄·`모델 요청 수: 3`(분류 1 + 고른 분야 수) |
| 04 | 03 두 분야 문의 「빌린 책을 연장하려면 어떻게 하나요? 토요일 운영 시간도 알려 주세요.」를 세 구조에 · 모델 없는 핑퐁 · 호출 한도 1 · 완료 조건(필요한 분야 `['loan_desk', 'facility_desk']`, 실행 전에 정함) | 요청 수 `4`(중앙 2 + 전문 2, 한 응답에 두 담당 — 밖 5/5) · 핸드오프 저장 `['AIMessage', 'ToolMessage']`·넘기기 요청 `2`(밖 기록 다섯 번 5/5)·요청 `1`·`OpenAIInvalidRequestError`·`400`(밖 10/10) · 라우터 `3` · 핑퐁 `GraphRecursionError`(한도 4) · 호출 한도 1 바깥 `['AIMessage', 'ToolMessage', 'ToolMessage', 'AIMessage']`·부른 횟수 2·`Model call limits exceeded: run limit (1/1)`·사용량 `None` · 완료 조건 `True`·`False`·`True`·`False` |
| 05 | §7 | §7 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 서브에이전트(subagent) | 중앙 에이전트가 도구로 감싸 불러 쓰며, 일 하나를 맡기는 전문 에이전트(공식 문서 subagent 뜻) | 도구 `ask_loan_desk` 안의 `loan_desk` |
| 01 | 중앙 에이전트 | 문의한 사람과 대화하며, 맡길지 고르고 받은 답으로 최종 답을 쓰는 에이전트 | 코드 이름 `supervisor`(본문은 「중앙 에이전트」만) |
| 01 | 전문 에이전트 | 한 분야만 맡아 답하는 에이전트(「담당」으로 줄여 씀) | 01 `loan_desk` · 03~05 `desk_agents` 셋 |
| 01 | 바깥 목록 · 안쪽 목록 | 중앙 에이전트의 메시지 목록 / 전문 에이전트가 한 번 불려 받고 쓴 메시지 목록 | `first_result["messages"]` / `specialist_runs[0]` |
| 02 | 핸드오프(handoff) | 다음 차례에 문의한 사람과 대화할 담당 자체를 바꾸는 일 — 답을 받아 오지 않음 | `Command(goto=…, update={"active_agent": …})` · 넘기기 도구 |
| 02 | 담당 칸 | 다음 차례에 대화할 담당 이름을 적어 두는 상태 칸(「제어권」 대신) | `active_agent`, `pick_desk`가 읽음 |
| 02 | 하위 그래프 | 다른 그래프의 노드로 들어간 컴파일한 그래프(Ch 25 01이 이름만 든 말을 02가 처음 정의) | `add_node`에 넘긴 작은 그래프·에이전트 그래프 |
| 02 | 넘기기 도구 | 모델이 불러 담당을 넘기는 도구 | `transfer_to_interlibrary`·04 `transfer_to_desk` |
| 03 | 라우터(router) | **요청을 분류해, 맞는 전문 에이전트에게 보내는 쪽 — 고른 담당이 여럿이면 함께 보냄**(마감 B-1로 한 담당도 덮게 고침) · Ch 18 02 라우팅을 하는 쪽 | 분류 노드 + `send_to_desks`의 `Send` 목록 |
| 03 | 분류 노드 · 분야 노드 · 종합 노드 | 답할 분야 이름 목록을 적는 노드 / 분야 하나를 맡아 답을 내는 노드 / 분야 이름 차례로 답을 엮는 노드 | `classify`·`loan_desk` 등·`join_answers` |
| 04 | 완료 조건(completion condition) | 필요한 결과가 다 모였는지 보는 기준 — 정지 조건(멈추는 까닭)과 가름 | `is_complete(collected, needed, has_final)` |
| (이어 씀) | 실행 한도 · 호출 한도 · 바퀴 한도 | 그래프 단계 수 상한(Ch 20 03) · **한도를 붙인 에이전트가 한 번 실행에서 보낼 수 있는 모델 요청 수의 상한**(Ch 16 04·Ch 22 04 — 마감 B-6로 「한도를 붙인 에이전트가」를 더함) · 루프 바퀴 수 상한(Ch 17 03) | 셋을 섞지 않음 |

- **쓰지 않는 말**(다섯 절 설명·주석·캡션·`.mmd`·README 참 금지어 0건 — 제목·슬러그·코드 백틱 말고): 챕터 리드 결정 4의 「반환」·「스키마」·「필드」·「런타임」·「검증」·「측정」·「계측」·「추정」·「지연」·「경로」·「영속」·「재시작」·「최대」·「비상 경계」·「동적」·「문맥」·「맥락」·「제어권」·「이벤트」·「조각」·한정어 없는 「청크」·「분기」·「병렬」(본문) + Ch 25 목록 전부(`ban26.py` — 「로그」 포함: 02 셀 28 A-14는 「파이썬 표준 모듈 `logging`으로 남긴 경고」로 씀). 제목의 영어 「Subagent」·「Handoff」·「Router」·「병렬 실행」·「종료 조건」은 제목에만(본문 첫 자리 풀이, 강사 확인). 마감 전후 금지어 대조 — 마감이 더한 문장의 새 걸림은 거짓 양성(「체크포인터」 안 「포인터」·「프로그램」 안 「로그」·자리 확인용 「핸드오프」·「라우터」)뿐.
- **「라우터」 뜻 겹침(뒤 챕터)**: Ch 34 03은 쓸 모델을 고르는 쪽을 「모델 라우터」와 맨말 「라우터」로 모두 부름 — Ch 26 03의 「라우터」(전문 에이전트에게 보내는 쪽)와 다른 뜻. Ch 34 개선 때 한 문장으로 가를 것(§15).
- **비유 계열 「항구의 예인선과 바지선」**: 01-6 닻 내린 큰 화물선(중앙 에이전트, 제자리)과 상자 하나만 싣고 돌아오는 작은 보트(전문 에이전트·마지막 답 글), 부두에 남은 상자 셋(담당만 가진 규정 글) · 02-6 바지선(대화)을 끄는 밧줄이 오른쪽 예인선에 걸림(담당 칸) · 03-5 돌 부두(분류 노드)에서 자루 실은 배 둘만 떠남(고른 분야 노드)·건너편 빈 부두(종합 노드) · 04-5 칸이 다 찬 짐배(완료 조건)와 닫힌 문에 막힌 짐배(한도) · 05-4 항아리를 내려놓은 기중기와 멈춘 기중기(최종 답까지 쓴 실행 1 · 한도 하나 모자란 실행 2). **비유와 다른 점**(각 절 b4): 중앙 에이전트는 상자를 받은 뒤 요청을 한 번 더 보냄(01) · 도구로 넘길 때는 요청과 답을 메시지로 직접 담음(02 — 마감 A-7로 「요청만 담고 답을 빠뜨리면」) · 걸린 시간을 재지 않음·답은 분야 이름을 담아야 함(03) · 한도에 닿은 실행은 그 자리에서 끝남(04·05). 사람·손·글자·숫자·화살표 없음. 짝짓지 않는 요소는 그림 읽기에 밝힘(01-6 상자 수 셋·**큰 배 갑판의 붉은 짐**(마감 A-5) · 02-6 배 색·상자 수 · 03-5 빈 배 수·자루 무늬·**빈 배를 묶은 줄**(마감 B-2) · 04-5 칸·통 수 · 05-4 기중기·수레 둘).

## 5. 색 규칙 (Mermaid 21장)

- **넣은 글·규정 글·손으로 적은 기록·바꾼 값 초록(tool)** · **우리 도구 함수·함수·노드 파랑(flow)** · **출력으로 확인한 값·받아 출력한 오류 노랑(measure)** · **`create_agent`가 만든 에이전트 그래프·라이브러리가 준 것·두 실행 공통 값·소스로만 확인한 동작 회색(클래스 없음)** · **보라 = 그 절에서 실제로 부른 모델만**(01-1 모델 상자·01-2 연보라 띠 · 02-5 연보라 띠 · 03-4 · 04-2·04-3 · 05-2 — 02·03 앞 절반 그림 보라 0).
- **다섯 절 모두 experiment라 빨강 0장**(02 `ValueError`·경고, 04 서비스 400·`GraphRecursionError`는 받아 출력한 오류라 노랑).
- 원본 viewBox 폭 모두 868 이하(최대 02-5 830). 라벨에 토큰·비용·답 글 없음. 모델 판단 값 라벨은 흔들림 확인 5/5 **그리고** 새 커널 두 번 같을 때 「이번 실행」·「한 번 맡긴 실행」 한정어와 함께.
- **마감에서 다시 렌더한 `.mmd`: `01-2`·`02-4`·`04-3`**(`--force`, PNG 직접 확인, 셋 다 노트북 첨부 아님 — 첨부는 절마다 「오늘 볼 그림」 한 장: 01-1·02-1·03-1·04-1·05-1). 01-2 「요청 2 두 문장 답」 → 「요청 2 도구 요청 없음」(폭 724 그대로) · 02-4 「AIMessage 받은 쪽 응답」 → 「받은 쪽이 손으로 적은 답」(폭 671 그대로) · 04-3 회색 상자 「도구 실행 노드 … 둘 가운데 하나만」 → 「넘기기 도구 둘이 저마다 바깥 그래프로 가는 Command를 냄 / 그 가운데 하나만 바깥 그래프에 적용」(폭 319). 삽화는 다시 만들지 않음.

## 6. 결정적 값과 흔들린 값

- **결정적 값**(결론·그림·정리·복습에 쓴 값): §3 표 전부 + §7. 코드가 정하는 구조 값은 새 커널 두 번 모두 같았고, 모델 판단 값(맡긴 횟수·모양·넘긴 여부·넘기기 요청 수·고른 분야)은 노트북 밖 흔들림 확인 5/5(04 핸드오프 오류는 10/10)와 두 커널에서 같을 때만 「흔들림 확인 다섯 번과 두 커널에서 모두」로 한정해 씀. **결론 문장의 중심은 셈**: 서브에이전트 중앙 = 도구를 요청한 응답 수 + 1(**도구 요청 없는 모델 응답으로 끝난 실행에서** — 마감 A-1) · 전문 = 부른 횟수 × 전문 안 요청 수(도구 없으면 1) / 핸드오프 넘긴 차례 = 넘긴 담당 1 + 받은 담당 1 · 다음 차례 = 받은 담당 1 / 라우터 = 분류 1 + 고른 분야 수 / 호출 한도로 끝난 실행은 마지막 1이 없음(04 7절·05 실행 2).
- **흔들린 값 — 결론·그림·정리·복습에 쓰지 않음**(결과 읽기 둘째 단락·b6 표 「교재 출력」·「확인할 점」·b7에만 「이번 실행에서는」·「교재 출력에서는」): 답 글·넘긴 글·글자 수 · 토큰(01 685·104 / 757·101 · 02 471·80 / 259·45 · 03 468·87 · 04 989·228 / 265·55 / 468·87 · 05 796·112 / 426·71 — 05는 밖에서 112·102) · 예상 비용 · **04 핸드오프 담당 칸**(밖 다섯 번 대출 셋·시설 둘 — §8 B-3) · 도구 요청·고른 분야의 **차례**.
- **노트북 밖에서만 본 값(b7에 「노트북 밖」 표시)**: 01 손으로 적은 응답에서 `sum_usage`가 멈춤(P2 `TypeError`) · 01 실행 한도가 도구 안 담당 실행에 닿지 않음(마감 A-2, 모델 없는 작은 그래프) · 02 하위 그래프 안에서 더한 메시지가 바깥에 저절로 들어가지 않음(`x6_propagate.py`) · 03 같은 분야 이름 둘이면 그 노드가 두 번 실행 · 04 핑퐁 한도 2·3·4·5·10 모두 오류 · 04 넘기기 둘 가운데 적용되는 쪽이 한쪽으로 고정되지 않음(모델 없는 `create_agent` 모양 — 마감 재확인) · 05 분류 모델 앞문 흐름(맡을 분야가 없는 문의 A2·B2가 열 번 모두 시설 담당으로 분류 — b7 한 문장과 주의 항목).
- **재지 않은 것·실행하지 않은 것**: 걸린 시간(모든 절) · 01 기록을 담당에게 넘기는 방법·비동기 서브에이전트·한 차례 여러 서브에이전트 · 02 미들웨어 핸드오프·받는 쪽 넘기기 도구·대출 문의로 되돌아가기·도구 메시지 빠진 기록으로 서비스 부르기 · 03 모델 종합·같은 분야 둘(노트북) · 04 한 번에 하나로 묶는 설정·차례로 넘기기·담당 에이전트 호출 한도·없는 분야 이름 `KeyError` · 05 셈보다 큰 한도·두 분야 문의에 한도 2 · 스트리밍(0건) · Windows·macOS 실행.

## 7. 05절 실습 절 주제와 결과

- 제목 「**위임 구조 실습: 요청 수 셈으로 호출 한도를 정하고 완료 조건으로 확인하기**」, 슬러그 `05-위임-구조-실습`, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~04 meta 합 강의 1+1+1+1 = **4h** · 실습 1+1+1+1 = **4h** = `chapter.json` 「총 8h · 강의 4h · 실습 4h」(`_build_index.py`도 4·4).
- 자료실 문의 창구의 중앙 에이전트에 요금 사고를 막는 호출 한도를 붙이되, 한도 값을 01절 셈으로 정하고(`tool_responses = 1` → `first_limit = tool_responses + 1` = 2), 일이 끝났는지는 04절 완료 조건으로 확인. 문의 = 01절 문의 · 필요한 분야 `['loan_desk']`(문의 글을 보고 실행 전에 정함).
- 붙인 앞 절 기능 셋(두 실행 모두 흐름 안에서 쓰임): **01** 서브에이전트 모양(04 도구 `ask_desk_agent` 하나)·요청 수 셈(`usage_with_specialists`·`message_kinds`) · **04** 호출 한도(조립 함수 `handle_inquiry(limit, question)`) · **04** 완료 조건(`answered_desks`·`is_complete` — 기록 장치 `summarize_run`). 뺀 것: 02 핸드오프(04 4절 400) · 03 분류 모델 앞문(맡을 분야가 없는 문의도 시설 담당으로 분류되어 빈 목록 갈래를 보일 수 없고, 요청이 3~5번을 넘음) · 03 `Send` 그래프 · 04 핑퐁·체크포인터.
- 실행 1(호출 한도 2) → 실행 2(**호출 한도 하나만 1** — 04절 7절과 같은 값, 마감 B-7로 b2 「새로 볼 것」을 「셈으로 정한 한도 2면 완료 조건 `True`, 하나 모자라면 `False` — 셈과 한도와 완료 조건이 한 흐름에서 이어지는지」로 좁힘). 모델 요청 **5번**(3 + 2).
- 결과(새 커널 두 번 21/21 같음 + 밖 L2·L1 열 번 같음): 실행 1 `['AIMessage', 'ToolMessage', 'AIMessage']`·부른 횟수 1·`도구 인자의 분야 이름: loan_desk`·`담당 답이 모인 분야: ['loan_desk']`·도구 요청 없는 모델 응답 `True`·`모델 요청 수(중앙 + 전문): 3`·`완료 조건: True` · 실행 2 같은 바깥 메시지·`Model call limits exceeded: run limit (1/1)`·사용량 `None`·요청 `2`·`완료 조건: False` · 8절 표 `실행 1 | 2 | ['loan_desk'] | True | 3 | True`·`실행 2 | 1 | ['loan_desk'] | False | 2 | False`. `assert`는 키 셀 하나뿐.
- 코드 셀 21(실습 선례 19~28) · 코드 줄 127 · 함수 본문 최대 6줄.

## 8. 도구 파일 `notebooks/delegation_tools.py` — 함수 표·해시 변천·생성기 대조 사슬

| 함수(인자) | 배운 곳 | 가져오는 절 | 하는 일 |
|---|---|---|---|
| `tool_call_names(response)` | Ch 19 04 | 01(`show_messages` 안) | 응답 하나의 도구 요청 이름 목록 |
| `show_messages(messages)` | Ch 19 06 | 01·02 | 메시지 목록을 한 줄씩 출력 |
| `sum_usage(messages)` | Ch 19 05 | 01~04 | 목록 안 `AIMessage`마다 요청 하나·토큰 합(사용량 `None`이면 멈춤) |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06 | 01·04·05 | 예상 비용(`.get` 둘 — 허용 표시) |
| `message_kinds(messages)` | **Ch 26 01 노트북 4절** | 04·05 | 메시지 종류 이름 목록 |
| `usage_with_specialists(new_messages, inner_runs)` | **Ch 26 01 노트북 5절** | 04·05 | 이번 실행이 더한 바깥 메시지 + 안쪽 목록 여럿의 요청 수·토큰 합 |
| `writer_names(messages)` | **Ch 26 02 노트북 7절** | 04 | 응답마다 칸 `name`(쓴 에이전트) |
| `send_to_desks(state)` | **Ch 26 03 노트북 2절** | 04 | 분야 칸 이름마다 `Send` |
| `answered_desks(inner_runs, names)` | **Ch 26 04 노트북 3절** | 05 | 안쪽 목록 마지막 응답의 `name`을 분야 이름 차례로 |
| `is_complete(collected, needed, has_final)` | **Ch 26 04 노트북 8절** | 05 | 완료 조건 |

- 함수 열, 함수마다 `# Ch NN MM절에서 배웠습니다 — …` 주석, 가져오기는 `from langgraph.types import Send` 하나(머리 설명 바로 뒤 — `send_to_desks`가 씀). 노트북 전역 이름 기대기 0, 금지 문법 0(허용 표시 `.get` 둘). 노드·도구·에이전트(노트북 전역 `model`·`desk_agents`를 읽음)는 도구 파일에 두지 않음(04·05가 03·04 셀과 글자 같게 다시 적음 — 생성기 대조).
- **해시 변천**: 없음 → 01 `90e83bcf7029…`(함수 넷) → 02·03 그대로 → 04 `91512d6a60ea…`(+ 01 둘·02 하나·03 하나 + `Send` 줄) → 05 **`c3c1709a8f0774196a6d6549c6deb5c93d244ce16d0d758afc9932d089f073b4`**(+ 04 둘, 70줄) → **마감 그대로**(챕터 리드 결정 — Ch 24 A-13·Ch 25 A-14 선례).
- **머리 설명 첫 줄 「앞 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다」**(검토 A-18·B-9): 지금 판에는 이 챕터 01~04절 함수 여섯도 있어 모자란 말. 해시 고정 결정으로 그대로 두고, 마감에서 다시 쓴 README가 함수 열의 배운 절·가져오는 절·`Send`를 적음. 고치면 `author_01.TOOLS_HEAD`부터 `strip_later_imports(…).startswith(TOOLS)` 판정·01~05 쓰기 가드·`author_05.TOOLS_05`·zip·공개 목록 해시를 함께 맞춤 — **Ch 24·25와 함께 전체 마감 한 항목**(최종 점검표 §2-13 6번에 Ch 26을 덧붙임).
- **생성기 대조 사슬**(마감에서 다시 확인 — 모두 통과, 생성기의 도구 줄 0 바뀜): `author_01.TOOLS` = `TOOLS_HEAD` + 함수 넷(`RUNNER_SHA` 고정 확인) · `author_04.TOOLS_04` = 01 판 + 01·02·03 함수 넷 + 가져오기 줄 · `author_05.TOOLS_05` = `author_04.TOOLS_04` + 04 함수 둘 = **디스크 파일**. `author_01.strip_later_imports(디스크)`가 01 판으로 시작 → 01 쓰기 가드 「skip」, 04 가드 「skip」, 05 「same」, 02·03은 도구 파일을 쓰지 않음(`check_tools()` 통과). 다섯 생성기 `cells()`가 노트북과 60·66·54·64·46셀 차이 0, `src_html()` = `_src` 5/5(`.cache/ch26-close/tools/chain05.py`·`genmatch.py` — 쓰기 없음). **`--src-only` 없이 부르면 노트북 출력이 지워지므로**(각 생성기 머리 설명) 설명만 고칠 때는 `--src-only` → `run_section.sh … NN --no-exec`.
- `author_01.py --tools-copy`는 디스크 판이 아니라 01절 판 `TOOLS`를 사본 폴더에 씀(검토 A-19) — 01을 다시 실행할 때 사본 B가 다른 도구 파일로 도는 문제, 생성기 코드라 마감은 고치지 않음(다음 재실행 몫).
- **전체 마감 2026-09-30: 머리 줄 고침, 새 해시 `0748a8eb7fa0e0886521a616d373f87d3453a4d405e70f38782e9001bf2d4de4`**(검토 A-18·B-9 · 체크리스트 §2-13 6번). 1행 「앞 챕터에서 배운 평범한 함수를」 → 「앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를」만 바꿈(나머지 머리 줄 — 「Ch 21 도구 파일 runner_tools.py에서 옮긴 함수는 …」 등 — 과 `Send` 가져오기·함수 열 본문은 AST·글자 같음). 생성기 안 판: 01 `90e83bcf…` → `5ea57020…` · 04 `91512d6a…` → `b35fbdfd…` · 05 = 디스크. 고친 생성기: `author_01.TOOLS_HEAD` 한 곳뿐(`strip_later_imports`·`TOOLS_04`·`TOOLS_05`·01~05 `check_tools`·쓰기 가드는 이 상수를 따라감, 챕터 안 해시 고정값 없음 — 앞서 Ch 25 머리 줄 고침으로 `author_01.STREAM_SHA`도 새 값). **뒤 챕터 고정값**: Ch 27 `author_02.DELEGATION_SHA`를 새 값으로(설명 한 줄) — Ch 27 02·Ch 29 03 생성기 `--src-only`를 쓰기 없이 돌려 `_src` 바이트 같음(Ch 29 03은 함수 글만 대조). 조건 넷: (가) 노트북 다섯 마크다운·출력과 `_src`·HTML·README에 머리 글·판 해시 0 · (나) 다섯 생성기를 파일 쓰기를 가로챈 채(`.cache/final-close/2-tools-head/tools/dryrun.py`) `--src-only`와 인자 없는 모드로 돌림 → `_src` 다섯 바이트 같음, 01·04 가드 `skip`, 05 `same`, `check_tools` 다섯 통과, `cells()`가 노트북과 60·66·54·64·46셀 같음 · (다) 다섯 절 모두 모델 셀이 있어 사본 실행 없이 가져오는 이름(4·2·1·6·5개)이 새 파일에 있고 함수 열 본문 AST가 옛 파일과 같음만 확인 · (라) 이 줄·handoff·계약 §4. 노트북 `code_sha256`·`outputs_sha256` 전후 같음.

## 9. 묶음 실행 검사 (Part 6 `check_bundle_execution.py`)

- 검사 목록은 Ch 24 01·Ch 28 01뿐이고 **Ch 26은 없습니다**(스크립트는 고치지 않음). Ch 26은 다섯 절 모두 키가 필요해(02·03 앞 절반만 키 없이 돎) 노트북 전체로는 대상이 아닙니다. 02·03 앞 절반을 넣을지는 전체 마감 후보(강사 확인).
- **마감 결과**: `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink` 환경 변수만(스크립트 수정 0, `TMPDIR`은 세션 홈 — 맥 마운트 밖) → **PASS**(Ch 24 01 `code_sha256` `7187f7a39f3f…` 28셀 · Ch 28 01 `a09d959cecc4…` 4셀, 10초). `bundle-execution.json` `baaaf52f…`(Ch 25 마감 때 zip `71683e44…` 기록) → **`4f1cd14a98c42d88bbe4b58f03dd16fc7337b4332002ac4110d2731a634abf81`**(`archive_sha256` `110579388680…`).

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part6/ch26-delegation/notebooks/01~05-*.ipynb`·`delegation_tools.py` | 01~05절 · **마감(마크다운만)** | 실습 폴더(챕터 몫) — §1·§8. 마감: 코드·출력 그대로, 파일 `f366a099`→`a2f574c2` · `90a08c5d`→`b2953d7f` · `0071c07d`→`60f57acd` · `582d4a1c`→`b32deb8e` · 05 `bbd6f27d` 그대로. 도구 파일 그대로 `c3c1709a…` |
| `labs/part6/ch26-delegation/README.md` | 05절(05 단락) · **마감(전체)** | `d460b0de…`(원본) → `87bc2dc1…` → **`2ad9cfedddc984a21e596d5244d55178bfa1fd4077c60f163564c1ad06978e33`**: 노트북 다섯, `uv sync --locked` → `.venv` → `notebooks/`에서 열기(다른 폴더면 `ModuleNotFoundError`), 설치 판(다섯 절 langchain 1.4.0·langchain-openai 1.6.0·langgraph 1.2.11·python-dotenv 1.2.3, 03·04 pydantic 2.13.5), **모델 요청 01 6 · 02 3(2~5절 0, 키 없이 돎) · 03 3(2~4절 0) · 04 11(4절 핸드오프 칸은 서비스가 거절한 요청의 오류를 받아 출력, 거절 1은 넣지 않음) · 05 5**, 예상 비용(요금표 2026-09-17 어림, 청구 금액 아님), 키는 `.env`의 `OPENAI_API_KEY`에서만(학생 묶음이면 `part6-practice/`의 `.env`, 값 출력 0), 도구 파일 단락(규격 §2-7 고정 문장 뜻·함수 열·배운 절·가져오는 절·`Send`), 절마다 하는 일, 05 단락. 묶음 밖 파일을 가리키지 않음, 참 금지어 0(「프로그램」·「체크포인터」·「핸드오프」 거짓 양성 말고) |
| `textbook/part6/ch26-delegation/chapter.json` | 05절 · **마감** | 05 절(05절) · `objectives` 셋 → **넷**(옛 「맥락 소유자」·「계측」·「추정 비용」·비용으로 구조를 고른다는 목표를 뺌 — §17), `hours` 그대로(`cf1f16f4` → `07a5a74e` → `8000bbc4`, 보호 파일) |
| `textbook/part6/ch26-delegation/qa/public-files.json` | 01·05절 | 도구 파일(01)·05 HTML·노트북 두 줄(05). 옛 그림 줄은 원래 없음 — 마감 그대로(`d11ec800`) |
| `textbook/part6/public-files.json` | 01·05절 | `collect_public_files.py`(도구 파일·05 노트북 줄, `0d44ef6f`) — 마감에서 다시 돌려 **바이트 같음**(`Explicit public files: 86; prerequisites: 13`), `prerequisite-files.json`(`4c7f5a4b`) 같음 |
| `textbook/part6/_build_index.py` | **마감** | ch26 설명 「세 가지 위임 구조를 구현하고 호출 수·비용·종료 조건을 비교합니다.」 → 「전문 에이전트를 도구로 부르는 서브에이전트, 다음 차례의 담당을 넘기는 핸드오프, 문의를 분류해 고른 담당에게 보내는 라우터를 만들고, 같은 문의로 세 구조의 모델 요청 수를 셈으로 견주며 한도로 멈춘 실행과 일이 끝난 실행을 완료 조건으로 가른 뒤, 요청 수 셈으로 호출 한도를 정하고 완료 조건으로 확인하는 실습을 합니다.」(시수 4·4 그대로, → `20a14e7a`, 보호 파일) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | **마감** | Ch 26 설명 「Subagent·Handoff·Router를 구현하고 같은 과제의 호출 수·비용을 비교합니다.」 → 「서브에이전트·핸드오프·라우터를 만들고, 구조가 정하는 모델 요청 수와 완료 조건을 확인합니다.」. **절 수 4는 그대로**(과정 전체가 실습 절을 빼고 세는 약속). 스크립트를 돌리기 전 옛 스크립트 출력이 지금 `index.html`과 바이트까지 같았고, 다시 만든 뒤 바뀐 줄은 Ch 26 행 하나(`→ 3454389d` · `90d6a6b8` → `18479837`, 보호 파일) |
| `labs/part6/continuity-guide.md` | **마감** | Ch 26 줄 「Ch18의 패턴과 Ch21의 에이전트 \| Ch26 도구로 위임·활성 담당 변경·라우팅 \| Ch27의 서브에이전트, Ch39의 정지 조건」 → 「Ch18의 라우팅과 함께 보내기, Ch13의 `Command`·`Send`, Ch21의 에이전트 \| Ch26 전문 에이전트를 도구로 부르는 서브에이전트, 담당을 넘기는 핸드오프, 분류해 보내는 라우터, 요청 수 셈과 완료 조건 \| Ch27의 서브에이전트 위임과 완료 조건」(없는 「Ch39」·옛 「활성 담당」·「라우팅」 뺌, → `89b7e207`, 보호 파일, 묶음에 들어감) |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | 05절 + **마감** | `python3 textbook/part6/_build_index.py`(README·노트북·`chapter.json`·목차 줄·continuity-guide를 모두 고친 뒤 **마지막에 한 번**) → **`Part 6: 53 verified sections; 102 bundled files`**, zip `83c92a6a…` → **`110579388680522757742b878be4ff5e7bf7c5e577c8705d69e2d76a821d5833`**(105항목, **Ch 26 9파일과 `continuity-guide.md`가 모두 디스크와 같음**, `__pycache__`·`.env` 0), `index.html` `d46148b8` → `5c19e32c`(Ch 26 섹션 설명 한 줄만), `integration-results.json` `4d620eb7` → `c352bd9f` |
| `textbook/part6/qa/bundle-execution.json` | **마감** | §9(`baaaf52f` → `4f1cd14a`) |
| `textbook/part6/qa/visual-results.json` · `textbook/_notebook/checks/ch26-delegation/visual-results.json`(+ 스크린숏 넷) | **마감** | `visual.cjs` 12행 PASS. 공용 파일은 **Ch 26 줄만** 10 → 12(05 두 줄, 새 HTML 해시), `screens` 124 → 126, 다른 챕터 줄 114개 그대로(`f2b70b7b` → `f63506dc`, 보호 파일). 챕터 결과 `f1b8e569` → `fbf86de7`, 스크린숏 넷(index·01 × 1280·390) 새로 찍음(보호 파일) |
| `textbook/part6/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 다시 써서 실행 전 사본으로 되돌림(내용 변경 0, `b3d69e9c…`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch26-delegation.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(마감 뒤 `28c2358b…` — 05절 뒤와 같음) |
| **`textbook/part6/_generate_ch25_ch26.py`(공용 옛 생성기) → `qa/upgrade/before/generators/blocked/_generate_ch25_ch26.py`** | 01절(막음) · **마감(`mv -n`)** | `06fa7d9993e1bada0b9fa4f6af0ced561dc263e48969559b6ca667e14f3cce6f` 같음(Ch 25 쪽 건너뛰기 + 01절이 첫머리에 `raise SystemExit`). 부르는 빌드·검사 스크립트 0(`grep` — `final-artifact-hashes.json`·`before-manifest.json` 기록뿐) |
| **`figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/_gen_figures.py`** | 01절(막음) · **마감(`mv -n`)** | `2e23044688175691ab6b411375cbc13c842b9732536c53d64c88e72d60530e90` 같음. 부르는 스크립트 0. `before/generators/`의 두 원본 사본(막기 전)은 그대로 |
| `textbook/part6/ch25-streaming/qa/upgrade/chapter-summary.md` · `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 25 요약 §13-7에 「옮김」 한 줄(덧붙이기만) · 진행표 Ch 26 행 한 줄 · 체크리스트 §2-13 1·6번에 덧붙임, §2-14 Ch 26 항목, §3·§4 Ch 26 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md` · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`render_mermaid.py`·`attach_figures.py`) · Part 6 옛 검사 스크립트와 `check_*`·`collect_public_files.py` · Part 6 `_src/index.html`·`practice-start.md`(Ch 26 문장 참) · `textbook/part6/qa/final-artifact-hashes.json`·`notebook-executions.json`·`prose-repetition-initial.json`·`language/ch26-*`·`ch25-ch26-original-prose.sha256` · `textbook/part7/qa/existing-artifacts-before.json`(Ch 26 옛 해시 — 기록 파일) · 실습 폴더 `pyproject.toml`·`uv.lock` · 도구 파일(해시 고정) · **Ch 27 이후 파일 전부**(Part 6 목차·묶음·공개 목록·기록·`continuity-guide.md` Ch 26 줄 말고) · `llm-practice.zip`·`delivery-results.json`.
- **파일을 지운 것은 없습니다.** 옮긴 것은 옛 생성기 둘(`mv -n`, 해시 같음). 옮긴 뒤 `_build.py`·`verify.py`·게이트·묶음 검사 통과. 마감이 기기 `/tmp`에 설치한 것: `/tmp/pw`(playwright 1.63.0, 19MB) · `/tmp/pw-browsers`(chromium-headless-shell 1243·ffmpeg 1011, 269MB) · `/tmp/npm-cache-ch26close`(38MB) — 지우지 않음(삭제 승인 목록).
- **보호 파일 190개(`before-manifest.json`)**: **149개 같음 · 39개 바뀜 · 2개 옮김(없어짐)** — 모두 의도한 것. 마감이 바꾼 것 36(01~05절이 바꾼 뒤 마감이 다시 바꾼 것 포함 — Ch 25 요약 한 줄 덧붙임도 보호 파일) + 옮김 2 + 01~05절이 바꾼 뒤 마감이 건드리지 않은 3(챕터·Part 공개 목록 · notebook-contracts). 목록은 `manifest-changes.md` 「마감 뒤」.

## 11. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`python-dotenv==1.2.3`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`): `langchain-core 1.6.2`·`langgraph-checkpoint 4.2.0`·**`langgraph-prebuilt 1.1.0`**·`pydantic 2.13.5`. 노트북 `%pip`은 다섯 절 넷 + 03·04 `pydantic==2.13.5`(잠금 판).
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch26-delegation`(잠금 판). 실행일 모두 2026-09-28(01 06:21 · 02 06:55 · 03 07:31 · 04 08:26 · 05 09:02 UTC — 마감에서 다시 실행하지 않음). 모델 `gpt-5.4-mini`.
- 설치판 소스 행(검토 A·B와 마감이 다시 확인): langchain 1.4.0 `agents/factory.py` 1829~1831(`recursion_limit` 9999)·1857(`with_config`)·1455~1456(`name`)·**1964(도구 요청마다 `Send("tools", [tool_call])`)** · `agents/middleware/model_call_limit.py` 168~208·236~250 · langgraph 1.2.11 `types.py` 704(`Send`)·799~848(`Command`)·806(`PARENT`) · **`graph/state.py` 1762(`raise ParentCommand`)** · `pregel/_algo.py` 253~256·311~313 · `pregel/_runner.py` 135~138·**616~634(`_should_stop_others` — `GraphBubbleUp`은 다른 작업을 멈추지 않음)·650~690(`_panic_or_proceed` — 끝난 작업 집합에서 하나를 올려 보냄)** · **langgraph-prebuilt 1.1.0** `prebuilt/tool_node.py` 821~824·895~920·1559~1563(01·02·04가 「langgraph 1.2.11」로 적었던 것을 마감에서 바로잡음).
- 참고 자료(2026-09-28 확인): LangChain Subagents(stateless·기록은 중앙·과제 글만/기록 넘기기·한 차례 여럿·Tool per agent vs single dispatch tool) · Handoffs(「single agent with middleware for most」·「assumes only the handoff tool was called (no parallel tool calls)」·「without it, the conversation history becomes malformed」·「you must include both」) · Router(「Zero or more」·한 담당 `Command`/여러 담당 `Send`) · multi-agent 개요(요청 수 표 4·3·3·3 등, 「Subagents adds one extra call」) · langgraph-supervisor README(도구로 직접 만들기 권고, 최신 0.0.31 — 잠금 밖) · OpenAI `gpt-5.4-mini` 요금(입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰, 요금표 2026-09-17).

## 12. 강사 확인 대상

1. **제목 말**: 챕터 「위임 구조 — Subagents · Handoffs · Router」 · 01 「Subagent」 · 02 「Handoff」·「전환」 · 03 「Router」·「병렬 실행」 · 04 「종료 조건」(본문에서 정지 조건·완료 조건으로 풂) · **05 긴 제목**(「위임 구조 실습: 요청 수 셈으로 호출 한도를 정하고 완료 조건으로 확인하기」)·슬러그. 슬러그 01은 Ch 25 04 b8이 링크해 고정.
2. **`chapter.json` 학습 목표 셋 → 넷**(절 무리 한 줄씩 + 05 실습 줄, 비용으로 구조를 고른다는 목표를 뺌, `hours` 그대로) · `_build_index.py`·`build_index.py`·`continuity-guide.md` Ch 26 문구 · README 다시 쓴 범위.
3. **코드 줄 증가**(주석·빈 줄 뺌): 01 42→145(셀 4→28) · **02 37→199(6→31, 검토 A-9 — 5절 셀 여덟은 줄이지 않음 권고)** · 03 37→170(4→25) · 04 109→223(9→30) · 05 새 절 127(21) + 도구 파일 70 — 챕터 225 → 864. 줄이면 그 절 새 커널 두 번(모델 요청·흔들린 값 인용·해시 사슬).
4. **04 설계**: 서브에이전트를 01의 「담당마다 도구」 대신 분야 이름을 받는 도구 하나(공식 single dispatch tool)로 바꾼 것 · **핸드오프 칸을 실제 서비스 400 오류 장면으로 둔 것**(마감 B-3·B-4로 근거와 한정어를 고침 — 한 번에 하나로 묶는 설정은 새 API라 실행하지 않음) · 「어느 구조가 싸다」 결론 없음 · `typing_extensions` 한 줄.
5. **05 실행 2가 04 7절과 같은 호출 한도 1**(마감 B-7 — b2를 「셈으로 정한 한도 2면 `True`, 하나 모자라면 `False`」로 좁힘, 설계는 그대로) · 인계 (가) 분류 모델 앞문 대신 (나) · **b7 넷째 항목**(분류가 고른 분야를 필요한 분야로 쓸 때의 주의 — 노트북 밖 확인 결과, 마감 B-8로 셋째 항목은 한 문장) · 흔들림 확인 85요청.
6. **삽화**: 01-6 위쪽 빈 하늘·갑판 붉은 짐(글만 — A-5) · 02-6 맞닿은 예인선·밧줄 매듭 · 03-5 배 넷·묶는 줄·자루 무늬(글만 — B-2, 재생성 한도 1회를 이미 씀) · 05-4 거울처럼 마주 본 기중기 둘. 다시 만들지. **05 삽화 기록의 모델 표시**: 작업 조회 결과의 `nano_banana_2`와 거래 기록의 「Nano Banana Pro」가 다름 — 기록만(01~05 prompt 기록 표시는 서로 같음).
7. **02 설계**: 뒤 절반을 공식 권고 「한 에이전트 + 미들웨어」 대신 「여러 에이전트 하위 그래프」로 · 받는 쪽에 넘기기 도구 없음(한 방향 넘기기 — 마감 A-12로 b7에 영향 한 문장) · 5절 받는 쪽 노드가 손으로 적은 응답(보통 함수 — 마감 A-15로 라벨·b6에 표시).
8. **새 용어 13**(4·4·4·1·0)과 정의 · **라우터 정의 폭**(마감 B-1로 한 담당도 덮게) · 코드 이름 `supervisor` · 01 도구 함수가 노트북 전역 기록 목록 `specialist_runs`에 붙이는 설계.
9. **교재용 규정 글**(01 연장 두 문장 · 02 상호대차 세 문장 · 03 시설 한 문장) · 03~05 전문 에이전트 「한 문장」(01·02는 「두 문장」).
10. **도구 파일 머리 설명**(A-18·B-9 — 해시 고정으로 그대로, README가 함수 열을 설명). Ch 24·25와 함께 고칠지.
11. **B-3 표현**: 검토 B는 「먼저 올라간 하나만 적용」을 권했지만, 설치판 소스와 모델 없는 재확인에서 「먼저 끝난 쪽」이 정하지 않아 본문은 「그 가운데 하나만 골라 바깥으로」·「어느 쪽이 남는지는 실행마다 달라」로 적음(§17).
12. **코드 쪽 다음 재실행 몫**(마감은 코드 셀을 한 글자도 바꾸지 않음): 04 셀 40·42·44·48 주석의 「2절」·「뒤 절반」(03 판 글 — 셀 39에 한 문장) · 02 셀 37 `error_text[:66]`(A-16 (가)) · 02 코드 줄 줄이기(A-9) · `author_01.py --tools-copy`(A-19).
13. 02·03 앞 절반(모델 없음)을 Part 6 묶음 실행 검사에 넣을지(§9).
14. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: 삽화 직접 판독, Windows·macOS 실제 실행, 학생 `uv sync --locked` `.venv` 첫 셀, 서비스가 답 없는 도구 요청을 400으로 막는지(02 — 실행하지 않음)).

## 13. Ch 27이 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 말: 서브에이전트·중앙 에이전트·전문 에이전트·바깥 목록/안쪽 목록(01) · 핸드오프·담당 칸·하위 그래프·넘기기 도구(02) · 라우터·분류 노드·분야 노드·종합 노드(03) · 완료 조건(04 — 정지 조건과 가름).
- 사실(참, 출력 근거): 도구 함수 안에서 부른 전문 에이전트는 넘긴 글 한 줄로 시작한 새 목록으로 일하고, 바깥 목록에는 마지막 답 글만 도구 메시지로 들어감 · 바깥 목록만 세면 전문 에이전트 요청이 빠짐(안쪽 목록을 함께 셈) · 핸드오프 담당 칸은 체크포인터로 다음 차례에 이어짐 · 라우터 두 분야 노드는 같은 단계에서 실행 · 호출 한도로 멈춘 실행은 오류 없이 끝나도 완료 조건 `False`.
- **Ch 27 01 b3 「Ch 26은 위임 구조를 다뤘습니다」·03 b3 「Ch 26에서 위임 완료 조건을 문장으로 적었습니다」·06 b3 「Ch 26에서 서브에이전트의 완료 조건을 적었습니다」는 참**(완료 조건 문장의 자리 = 04 b4 소제목 「서브에이전트의 완료 조건」 두 문장 + 노트북 8절, 핸드오프·라우터 완료 조건 문장도 같은 자리 · 05 b8이 Ch 27 01을 링크).

### 전제하면 안 되는 것 (Ch 27 파일은 고치지 않았습니다)

1. **서브에이전트 안쪽 실행에는 바깥 실행 한도가 닿지 않습니다**(마감 A-2). 01 중앙 에이전트의 `{"recursion_limit": 10}`은 도구 함수 안에서 설정 없이 부른 전문 에이전트 실행에 닿지 않습니다 — `create_agent`가 그래프에 9999를 붙여 둠(`agents/factory.py` 1829~1831·1857행). 02처럼 에이전트를 **하위 그래프 노드로** 넣으면 바깥 한도가 안쪽에도 걸립니다. 모두 노트북 밖 모델 없는 작은 그래프로 확인(`/tmp/reviewA26/limit2.py`·`limit.py`). **도구를 가진 서브에이전트(DeepAgents `task` 등)는 안쪽 실행에 한도를 따로** 줘야 요금 사고를 막습니다. 호출 한도(`ModelCallLimitMiddleware`)도 한도를 붙인 에이전트의 요청만 셉니다(04 7절·05).
2. **Ch 26의 전문 에이전트는 모두 도구가 없습니다**(01 담당 하나·03~05 `desk_agents` 셋). 전문 에이전트가 도구를 부르는 모양, 기록(바깥 목록)을 담당에게 넘기는 모양, 비동기 서브에이전트, 한 차례에 서로 다른 서브에이전트를 차례로 여러 번 부르는 모양은 실행하지 않았습니다. **요청 수 셈**(중앙 = 도구를 요청한 응답 수 + 1)은 도구 없는 담당·도구 요청 없는 모델 응답으로 끝난 실행의 값이고, 호출 한도로 끝나면 마지막 1이 없습니다.
3. **핸드오프는 한 응답에 넘기기 요청이 둘이면 서비스 400으로 멈춘 채로** 남았습니다(04 4절 — 이번 넘기기 도구 모양 + 안내 담당의 모델 판단). `create_agent`는 도구 요청마다 따로 실행하고(`factory.py` 1964행), 두 넘기기가 저마다 `ParentCommand`를 올려 보낸 뒤 **그 가운데 하나만 적용되며 어느 쪽인지는 실행마다 다릅니다**(밖 다섯 번 대출 셋·시설 둘 — **「첫째만 적용된다」고 전제하지 말 것**). 한 번에 하나로 묶는 설정·차례로 넘기기는 실행하지 않았습니다. 02 핸드오프는 받는 쪽에 넘기기 도구가 없는 한 방향 넘기기입니다.
4. **Ch 26은 스트리밍을 0건 했습니다**(`stream`·`astream`·`subgraphs=True` 없음). 서브에이전트·핸드오프의 스트림 청크가 섞이는 모양은 실행하지 않았습니다.
5. **완료 조건**은 04 함수 `is_complete(collected, needed, has_final)`입니다 — 필요한 분야는 04·05 모두 **문의 글을 보고 손으로 정한 값**이고, 「완료 조건 = 답이 맞았는가」가 아닙니다. 분류 모델이 고른 분야를 필요한 분야로 쓰면 답하지 못한 문의도 완료 조건을 채울 수 있습니다(05 b7 — 노트북 밖 확인).
6. **도구 파일 `delegation_tools.py`는 Ch 26 실습 폴더에만** 있습니다(`c3c1709a…`, 머리 설명 첫 줄은 앞 챕터 함수만 말함). Ch 27 실습 폴더와 잠금이 다르면 파일째 가져오지 말 것.
7. **말**: 「문맥」·「맥락」·「제어권」·「병렬」(본문)·「추정」·「측정」·「지연」·「반환」·「조각」·「이벤트」·「로그」는 제목·슬러그 밖 0. 소재(자료실 문의 창구)를 Ch 27이 이어 쓴다는 약속은 없습니다. 공용 옛 생성기 `_generate_ch25_ch26.py`는 옮겼습니다(§10).

## 14. 챕터 끝 인계 요약 (Ch 27 작업자용 한 줄)

Ch 27 01·03·06 b3는 참이지만, **Ch 26의 서브에이전트는 도구 없는 담당을 도구 함수 안에서 부른 모양뿐이고 그 안쪽 실행에는 바깥 실행 한도가 닿지 않으며(create_agent 9999), 핸드오프는 한 응답 넘기기 둘에서 400으로 멈춘 채이고 스트리밍은 0건입니다** — DeepAgents 서브에이전트에는 안쪽 한도를 따로 주고, 「첫 넘기기만 적용」을 전제하지 마세요.

## 15. 뒤 챕터(Ch 27·34)·전체 마감 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 26 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 27(대기) | 01 `_src` b3 | 「Ch 26은 위임 구조를 다뤘습니다」 | 참(01~05, 05 b8이 Ch 27 01 링크 — 하네스 기능을 앞당겨 풀지 않음) | 없음 |
| Ch 27(대기) | 03 `_src` b3 | 「Ch 26에서 위임 완료 조건을 문장으로 적었습니다」 | 참(04 b4 「서브에이전트의 완료 조건」·핸드오프·라우터 문장 + 노트북 8절) | 없음 — 필요한 분야는 손으로 정한 값(§13-5) |
| Ch 27(대기) | 06 `_src` b3 | 「Ch 26에서 서브에이전트의 완료 조건을 적었습니다」 | 참(같은 자리) | 없음 — 안쪽 실행 한도(§13-1)·도구 없는 담당(§13-2)을 전제하지 말 것 |
| **Ch 34(대기)** | **03 `_src`(`03-모델-라우팅.html`)** | 「모델 라우터는 요청을 관찰해 사용할 모델을 선택하는 함수입니다」 + 맨말 「라우터는 요청 길이 … 로 모델을 고릅니다」·「라우터가 요청 난이도를 잘못 판단했을 때」 | Ch 26 03 「라우터」 = 요청을 분류해 맞는 전문 에이전트에게 보내는 쪽 — **다른 뜻** | **Ch 34 개선 때 한 문장으로 가를 것**(예: 「Ch 26 03의 라우터는 전문 에이전트를 고르고, 이 절의 모델 라우터는 쓸 모델을 고릅니다」) |
| Part 6 | `labs/part6/continuity-guide.md` 12행 | (마감에서 고침) | Ch 26 줄 참, 「Ch39」 뺌 | 없음 |
| Part 6 목차 | `_src/index.html` 「Ch 26–28은 다른 에이전트·파일·외부 도구를 연결하는 범위를 넓힙니다」 · `practice-start.md` 「Ch 26의 위임」 | — | 참 | 없음 |
| Ch 25(완료) | 04 b8(01 슬러그·「전문 에이전트를 도구로 감싸 일을 맡기는 위임 구조」) | — | 참 | 없음 |
| Ch 8(완료) | 03 b4·b8·목차 | 「서브에이전트가 따로 받은 컨텍스트로 일하는 모양」 | 참(01 4·6절) | 없음 |
| 전체 마감 | `llm-practice.zip` 안 Ch 26 | 옛 판(노트북 넷·옛 README — 도구 파일·05 없음) | `part6-practice.zip`은 새 판 9항목이 디스크와 같음 | 전체 묶음 재생성 때 Ch 26 9항목 대조 |
| Part 7 | `textbook/part7/qa/existing-artifacts-before.json` | Ch 26 `_src` 옛 해시 셋 | 기록 파일(계약·검사 입력 아님) | 고치지 않음 — Part 7 작업 때 판단 |

## 16. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-14)

1. **옛 그림 열둘 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~4, 12개 — 본문 참조 0, 캡션에 「경로」·「병렬」, 사본 `qa/upgrade/before/figures/`, `final-artifact-hashes.json`·`qa/ch26-code-output-preservation.sha256`이 해시를 적은 기록 파일, 챕터 공개 목록 줄은 원래 없음). Part 6 옛 검사 `check_figures.py`가 `.excalidraw` 짝을 요구하는 것과 함께 정할 것.
2. **`gates-wip-*.json` 열하나 삭제 승인**(`gates-wip-01-01`·`01`·`02-02`·`02`·`03-03`·`03`·`04-04`·`04`·`05-05`·`05`·`ch26-after05` — `gates-after.json` 5/5로 갈음, 절 번호 다섯은 마감 `run_section.sh --no-exec`가 다시 씀).
3. **캐시·임시 삭제 승인**: 실습 폴더 `labs/part6/ch26-delegation/notebooks/__pycache__/delegation_tools.cpython-312.pyc`(05 A 커널 09:02:41Z — 마감은 만들지 않음) · 실습 폴더 `labs/part6/ch26-delegation/.venv`(macOS 판 174MB) · `.cache/vm/venv-ch26-delegation`(238MB) · `.cache/ch26-0N-view/`(N=1~5) · `.cache/ch26-close/`(마감 전 사본 `pre/`·확인 스크립트 `tools/`·치환 목록 `reps/`·옛 검사 결과 `oldcheck/`·`llm-practice.zip`을 뺀 전달 검사 사본 `dx/`·로그 `log/`·노트북 글 추출 `dump/`) · 기기 `/tmp/ch26-prep`·`/tmp/ch26-01`~`/tmp/ch26-05` · `/tmp/reviewA26`·`/tmp/reviewB26`(검토 재현 파일) · `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`(Mermaid 도구, 공용) · `/tmp/uv-cache`(공용) · **마감이 설치한 `visual.cjs` 도구 `/tmp/pw`·`/tmp/pw-browsers`·`/tmp/npm-cache-ch26close`** · 기기 `/tmp/ch26close-index-old.html`(옛 목차 스크립트 출력 대조용).
4. **01~05절 작업 알림**: 01 작업자가 Mermaid 설치 안내(`textbook/_notebook/mermaid/README.md` 13행 `rm -rf /tmp/npm-cache`)대로 기기 `/tmp/npm-cache`를 설치 직후 지움(01 진단 §11에 보고 — 기기 `/tmp`의 캐시, 연결 폴더 파일 아님). 챕터 리드가 적은 「명령에 들어간 `rm -rf`(지워진 것 없음)」는 기록 파일에서 따로 찾지 못함 — 지워진 연결 폴더 파일은 0.
5. **코드 쪽 다음 재실행 몫**: 04 셀 40·42·44·48 주석(「2절」·「뒤 절반」 — `author_04`가 `author_03` 셀 글을 그대로 씀, 04 판 주석으로 가를 것) · 02 셀 37 `[:66]`(이름 있는 변수로) · 02 코드 줄 줄이기(A-9, 강사 결정) · `author_01.py --tools-copy`를 디스크 판 복사로(A-19). 다시 실행하면 새 커널 두 번 대조·교재 출력 인용 다시 대조·zip 다시 만들기.
6. **도구 파일 머리 설명 — Ch 24·25·26 한 항목**(§8).
7. **Part 6 옛 검사 스크립트 넷(고치지 않음, 마감에서 돌린 결과)** — 모두 Ch 26에 닿기 전에 멈춤: `check_scope.py` Ch 21 07 `Missing scope`(Ch 26 05 「실습 30분」도 같은 모양, `SECTION_COUNTS` ch26 **4 ≠ 5**) · `check_figures.py` Ch 21 `01-1-….svg`의 `.excalidraw` 짝(Ch 26 새 SVG 스물하나도 짝 없음) · `check_notebook_readiness.py` `assert len(reports) == 47`(Part 6 노트북 53), **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림**(`b3d69e9c…`) · `check_visual_reports.py` `ch22-middleware`에서 멈춤(`visual-results.json` 안 바뀜). 결과 파일 `lesson-scope.json`·`figure-consistency.json`·`visual-results.json`은 안 바뀜.
8. **`llm-practice.zip`**: Part 6 `check_delivery.py`가 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`(117행)에서 멈춤(결과 파일 `delivery-results.json` `3cc2d143…` 안 바뀜). 사본(`.cache/ch26-close/dx/check_delivery_nollm.py`)에서 그 zip만 빼면 HTML 64 · 링크 1,305 · 누락 0 · 절 53 · 코드 셀 919 · 복습 201문항 오류 0 · SVG 182 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` `11057938…` 105항목(part6 노트북 53) 통과.
9. **Part 6·Part 7 기록 파일의 옛 해시**(계약·검사 입력 아님 — 고치지 않음): `textbook/part6/qa/final-artifact-hashes.json`(Ch 26 줄 30, 옛 생성기 옛 자리 포함) · `notebook-executions.json`·`notebook-readiness.json`(Ch 26 넷 — 05 없음) · `prose-repetition-initial.json` · `language/ch26-final.*`·`ch25-ch26-original-prose.sha256`·`language/ch26-original/` · `textbook/part7/qa/existing-artifacts-before.json`(Ch 26 `_src` 옛 해시). **Part 6 공용 `visual-results.json`**: Ch 26 줄은 마감에서 12줄로 새로 모음(`screens` 126), 다른 챕터 줄은 옛 HTML 해시 그대로 — Part 6 마감 때 다시 모을 것.
10. **`textbook/_notebook/build_index.py`** 절 수(Ch 26 4 — 실습 절 뺀 수, 과정 전체 약속) — 전체 목차 마감 때.
11. **과정 요약(누적 문서 몫)**: Ch 26 용어(§4 — 서브에이전트 = 도구로 감싸 부르는 전문 에이전트 · 핸드오프 = 다음 차례의 담당 바꾸기 · 라우터 = 분류해 보내는 쪽(Ch 34 「모델 라우터」와 다름) · 완료 조건 ≠ 정지 조건 · 호출 한도 = 한도를 붙인 에이전트 요청만)와 도구 파일 `delegation_tools.py`(`c3c1709a…`, 함수 열)는 과정 요약에 아직 넣지 않음(Part 6 마감 오케스트레이터).
12. **옛 기록 파일**: `qa/research.md`·`research.md`(Ch 25 조사가 섞임)·`qa/ch26-technical-review.md`·`qa/authoring-checklist.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용 그대로 — 뒤 둘은 끝에 「마감」 절) · `qa/ch26-code-output-preservation.sha256`(옛 판 해시) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음).
13. **실습 폴더 잠금**: `pyproject.toml`·`uv.lock` 그대로. 바꿀 것 없음.
14. **2차 검토**: 두 검토의 「확인하지 못한 것」(한국어 감사 3단, 삽화 직접 판독, Windows·macOS 실제 실행, 학생 `.venv` 첫 셀)과 §12.

## 17. 검토 1차와 반영 (2026-09-28 마감)

- 판정: **A(01~02·공통) 중 5 · 하 16**(01 중 1·하 5 · 02 중 3·하 7 · 공통 중 1·하 4), **B(03~05·마감 몫) 중 4 · 하 8**(03 하 2 · 04 중 2·하 2 · 05 중 1·하 1 · 도구 파일 하 1 · 기록·마감 몫 중 1·하 2). 합 **[중] 9 · [하] 24**, [상] 0. (챕터 리드 지시의 「A-8·04 §0-2 기록 정직성 [중]」은 A-8 [중] + B-10 [하]의 한 부분.)
- **[중] 9건 모두 처리 — 8건은 글·그림·기록으로 반영, A-9는 검토 권고(「강사 결정 전에는 그대로」)대로 그대로 두고 강사 확인**: A-1(01 b4 셈 한정어 + 호출 한도로 끝난 실행 한 문장 · 복습 4 · 05 b4·복습 1 「최종 답까지 쓰는 실행에서」) · A-7(02 b4 인과 「하위 그래프 안 요청 응답은 바깥에 저절로 들어가지 않음」 · 5절 결과 읽기·b6에 조건 「요청 응답을 바깥 입력에 손으로 넣은 경우」 · 비유 다른 점·복습 3 — 5절 셀 여덟은 줄이지 않음) · A-8(`02-probe.md` §0 「첫 요청 뒤에 적음」 + 진단 §4) · A-17(01 b7·b10·02 b10·04 전부 — `prebuilt/tool_node.py`는 langgraph-prebuilt 1.1.0) · B-3(04 b7·b10·그림 04-3을 `factory.py` 1964행·`graph/state.py` 1762행·`pregel/_runner.py` 650~690행으로, 3:2의 까닭 한 문장 — **표현은 검토 권고와 다름**: 「먼저 올라간 하나」 → 「그 가운데 하나만 골라」, 설치판 `_should_stop_others`·`_panic_or_proceed`와 모델 없는 재확인(대출 쪽을 늦춰도 대출 4·시설 2)이 근거) · B-4(04 정리·b8·b6·노트북 4절 끝 — 이번 도구 모양 + 모델 판단으로 한정, 「오류가 없었더라도 모인 분야가 하나라 `False`」 셈 문장, 02 7절 이음 문장) · B-7(05 b2 「새로 볼 것」을 실행이 보인 만큼 — 04 7절과 같은 한도 1을 밝힘) · B-11(`objectives` 넷 — 금지어·비용 선택 목표 뺌, 05 줄, `hours` 그대로, 절 meta 합 4·4 맞음). **코드를 바꿔야 해 그대로 둔 [중] 1건: A-9**(02 코드 37 → 199줄·코드 셀 31 — 줄이면 02 노트북 전체 새 커널 두 번(7절 모델 셀 포함), 코드 셀을 바꾸지 않는다는 결정·검토 권고대로 그대로, 강사 확인 대상).
- **[하] 24건 가운데 22건 반영**(코드 쪽은 검토 권고대로 설명 셀 한 문장 + 다음 재실행 몫): A-2(01 b7 새 항목·노트북 셀 23 — Ch 27 인계) · A-3(01-2 라벨·alt, 다시 렌더) · A-4(01 복습 2·3) · A-5(01-6 그림 읽기, PNG 직접 확인) · A-6(01 진단 145줄·그림 차례) · A-10(02 셀 53) · A-11(02 진단 §5 바로잡음·b7·b10) · A-12(02 b7) · A-13(02 셀 24·26) · A-14(02 셀 28 — 「로그」 대신 `logging`) · A-15(02-4 라벨·alt·도식 읽기·b6, 다시 렌더) · A-16 (나)(02 셀 51) · A-20(02 b5·준비물) · A-21·B-12(README 전체) · B-1(03 라우터 정의·셀 6) · B-2(03-5 그림 읽기, PNG 직접 확인) · B-5(04 셀 39에 주석 가리킴 한 문장) · B-6(04 호출 한도 정의·b6 표·셀 53) · B-8(05 b7 셋째 항목 한 문장·진단 인용 §3으로) · B-10(03 probe 절 번호·03 figures 표·03 진단 Ch 34 줄·04 probe §0-2 시각 — 05 진단 §9 「B는 도구 파일 사본 포함」은 기기에서 다시 보니 맞아 고치지 않음) · A-19(`author_01.py --tools-copy` — 검토 권고 「다음 재실행 때」대로 생성기 코드는 그대로 두고 최종 점검표에 기록). **반영하지 않은 [하] 2건과 까닭**: **A-18·B-9**(같은 항목 — 도구 파일 머리 설명, 해시 `c3c1709a…` 고정 결정 — 01~05 생성기 사슬·zip이 이 판에 기댐, Ch 24 A-13·Ch 25 A-14 선례, README가 함수 열을 설명, 전체 마감 한 항목). **코드 쪽이 남은 것**(검토 권고대로 다음 재실행 몫, §16-5): A-16 (가)(`[:66]` — 코드 셀이라 그대로, 결과 읽기에 바로잡을 틀린 말은 없어 문장을 더하지 않음) · B-5 주석 넷(코드 셀 그대로, 셀 39 한 문장) · A-19.
- **검토의 「사람이 정해야 할 것」 처리**: A 1(A-9 코드 부피)·5(제목·새 용어·코드 셀 수·삽화) · B 1(05 실행 2 — (가)안: 설계 그대로, b2만)·2(05 b7 — 셋째는 한 문장, 넷째는 둠)·3(04 핸드오프 오류 장면 — 둠)·4(03-5 — 글만)·5(라우터 정의 — 한 담당도 덮게)·6(05 제목) → 그대로 두거나 권고대로 고치고 강사 확인(§12). A 2(A-7 범위) → 문장만(셀 더하지 않음). A 3(A-8) → 「첫 요청 뒤에 적음」으로 사실대로. A 4(A-18) → 그대로. A 6(옛 `check_figures.py`) → 예상 실패로 기록(§16-7).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자 — 모두 같음): 01 `499eb8665ba1`/`32606c9c4976` · 02 `2d1b15cf6e77`/`01ffd42285ea` · 03 `940a1065dba4`/`2f8e5fd8cd0b` · 04 `bc1e02160142`/`3f6d995346c3` · 05 `52feb1f894ef`/`5e0677ed5b5b`. `executed_at` 다섯 모두 같음, `metadata.verification`과 다시 계산한 값이 같음. 파일 해시만 바뀜(01~04 마크다운, 05는 파일도 그대로): §10 첫 줄.
- 고친 방법: `.cache/ch26-close/tools/gpatch.py`(생성기 문자열과 노트북 마크다운을 함께 — 노트북 코드 셀에 옛 글이 있거나 생성기에서 한 번이 아니면 멈춤, 새 마크다운은 줄 목록으로 저장, `reps/0N.json`) → `author_NN.py --src-only` → `genmatch.py`(60·66·54·64·46셀 · `_src` 5/5 같음) → `gcheck.py`(게이트를 파일 쓰기 없이) → `.mmd` 고친 셋만 `render_mermaid.py --only … --force` → `run_section.sh … NN --no-exec` 다섯 번. 마감이 더한 문장의 참 금지어 0, 게이트 G6 0.
- 검사: `upgrade_gates.py … --label after` **5/5 PASS, G1~G7 0** · AST 따로 금지 문법 0(허용 표시 02 셀 52·04 셀 28 `ToolRuntime`, 도구 파일 `.get` 둘) · `verify.py --chapter` **PASS 5 sections / 135 code cells (max 19 lines)** · 빌드 HTML 여섯 `{{`·`[[` **0건** · `visual.cjs` **12행 PASS** · Part 6 `check_bundle_execution.py` **PASS**(Ch 24 01·Ch 28 01) · Part 6 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(그 zip을 뺀 대조 통과, §16-8) · 옛 검사 넷 Ch 26 전에 멈춤(§16-7) · 보호 파일 190개 149 같음 · 39 의도한 변경 · 2 옮김.
