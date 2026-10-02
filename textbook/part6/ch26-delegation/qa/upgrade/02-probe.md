# 02절 흔들림 확인 (노트북 밖, 2026-09-28)

규격 §2-7 10번 끝 · 챕터 리드 결정(「노트북 실행 전 노트북 밖 5번」). 02절은 앞 절반(2~5절)이 모델 없는 구조라 흔들림이 없고, **뒤 절반(6~7절)의 실제 모델 판단만** 노트북 밖에서 5번 봅니다. 키는 루트 `.env`에서만 읽고 출력하지 않습니다. 스크립트 `qa/upgrade/probe/probe02.py`, 기록 `qa/upgrade/probe/probe-02-P1.jsonl`(기기 `/tmp/ch26-02/probe/`의 사본).

## 0. 입력과 판단 규칙 (2026-09-28T06:45Z에 적음 — 첫 요청 뒤, 마감 고침)

> **마감 고침(2026-09-28, 검토 A-8)**: 처음에는 머리에 「첫 요청 전에 적음」이라 적었습니다. 그러나 기록 `probe/probe-02-P1.jsonl`의 첫 요청은 06:42:52Z이고 스크립트 `probe/probe02.py`는 06:42:45Z에 쓰여, 이 절의 시각 06:45Z보다 앞섭니다. **이 §0은 첫 요청 뒤에 적었습니다.** 다섯 번 결과가 모두 같아 판단 규칙이 갈래를 가를 일이 없었고, 결론은 바뀌지 않습니다. 값을 고르려는 재실행은 하지 않았습니다.

공통(노트북 6~7절과 같은 코드로 씀):

- 모델 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` 객체 하나를 두 에이전트가 함께 씀(과정 표준 셀).
- 바깥 상태 형식 `TeamState(TypedDict)` — 칸 `messages: Annotated[list[AnyMessage], add_messages]`(Ch 13 04절 모양) · `active_agent: str`(담당 칸). `NotRequired`·`AgentState` 확장은 쓰지 않고, 첫 입력에 빈 글 `""`을 넣음.
- 조건 함수 `pick_desk(state)` — 담당 칸이 `"interlibrary_desk"`이면 그 노드, 아니면 `"loan_desk"`(앞 절반과 같은 함수).
- 상호대차 규정 글(**교재용, 이 절이 실행 전에 정함** — 실제 도서관 규정이 아님): `interlibrary_rules` = 「[교재용 상호대차 규정] 다른 도서관의 책은 자료실 창구에서 상호대차로 신청합니다. 신청한 책은 보통 3~5일 뒤에 도착합니다. 책이 도착하면 문자로 알리고, 7일 안에 찾아가야 합니다.」
- 상호대차 담당 `interlibrary_agent = create_agent(model, tools=[], system_prompt=interlibrary_text, name="interlibrary_desk")`, `interlibrary_text` = 「도서관 자료실의 상호대차 담당입니다. 아래 교재용 규정만 근거로 두 문장의 한국어로 답하세요.」 + 줄바꿈 + `interlibrary_rules`.
- 넘기기 도구 `@tool transfer_to_interlibrary(runtime: ToolRuntime)`(독스트링 「다른 도서관의 책을 빌려 오는 상호대차 문의를 상호대차 담당에게 넘깁니다.」): `last_message = runtime.state["messages"][-1]` · `transfer_message = ToolMessage(content="상호대차 담당에게 넘겼습니다.", tool_call_id=runtime.tool_call_id)` · `Command(goto="interlibrary_desk", update={"active_agent": "interlibrary_desk", "messages": [last_message, transfer_message]}, graph=Command.PARENT)`(공식 Handoffs 문서의 여러 에이전트 하위 그래프 모양 — 문서의 `next(… reversed …)`는 과정 금지 문법이라 `[-1]`로 씀).
- 대출 규정 담당 `loan_agent = create_agent(model, tools=[transfer_to_interlibrary], system_prompt=loan_text, name="loan_desk")`, `loan_text` = 「도서관 자료실의 대출 규정 담당입니다. 아래 교재용 규정만 근거로 두 문장의 한국어로 답하세요. 다른 도서관의 책을 빌려 오는 상호대차 문의는 직접 답하지 말고 transfer_to_interlibrary 도구로 넘기세요.」 + 줄바꿈 + `loan_rules`(01절 규정 글 네 문장 그대로).
- 바깥 그래프 `StateGraph(TeamState)` — `add_node("loan_desk", loan_agent, destinations=("interlibrary_desk", END))` · `add_node("interlibrary_desk", interlibrary_agent)` · `add_conditional_edges(START, pick_desk, ["loan_desk", "interlibrary_desk"])` · `add_edge("interlibrary_desk", END)` · `compile(checkpointer=InMemorySaver())`(앞 절반 그래프와 같은 호출).
- 설정 `{"configurable": {"thread_id": "team-N"}, "recursion_limit": 10}`(회차마다 새 스레드, 실행 한도 10 — 요금 사고 방지).
- **P1**(노트북 7절 본 실행): 첫 차례 `{"messages": [HumanMessage(content="다른 도서관에 있는 책도 빌려 볼 수 있나요?")], "active_agent": ""}` → 같은 스레드 둘째 차례 `{"messages": [HumanMessage(content="신청하면 며칠 뒤에 받을 수 있나요?")]}`(두 글은 앞 절반과 같음).
- 결과를 보고 규정 글·시스템 메시지 글·문의 글·도구 글·실행 한도를 바꾸지 않습니다.

회차마다 기록: 시각 · 첫 차례 메시지 수와 종류 차례 · 응답마다 도구 요청 이름 목록 · 응답마다 `name`(쓴 담당) · 도구 메시지 내용과 호출 ID 짝(`==` 결과만, ID 값은 적지 않음) · 첫 차례 뒤 담당 칸 · `get_state` 다음 노드 · 첫 차례 요청 수(`sum_usage(메시지[1:])`) · 둘째 차례 뒤 담당 칸 · 둘째 차례에 더해진 메시지 종류와 쓴 담당 · 둘째 차례 요청 수(`메시지[첫 차례 수 + 1:]`) · 입력·출력 토큰 · 예상 비용(요금표 2026-09-17) · 두 답 글과 글자 수 · 경고(`warnings`로 모음) · 오류.

판단 규칙(결론에 쓸 수 있는 관찰):

- **구조 값 — 코드가 정하는 값이라 5번 모두 같아야 하고, 결론·그림에 씀**: 넘기면 도구 메시지 내용 「상호대차 담당에게 넘겼습니다.」·호출 ID 짝 `True` · 첫 차례 응답 수 == `sum_usage` 요청 수 · 둘째 차례에 더해진 메시지가 사람 글 하나 + 응답 하나 · 두 차례 모두 `get_state` 다음 노드 `()`. 하나라도 다르면 결론에서 빼고 진단에 적은 뒤 보고.
- **모델 판단 값 — 5번 모두 같을 때만 결론에 「흔들림 확인 다섯 번과 두 커널에서 모두 …」로 한정해 씀**: 첫 차례 대출 규정 담당의 응답에 넘기기 도구 요청 **1**개 → 첫 차례 종류 `['HumanMessage', 'AIMessage', 'ToolMessage', 'AIMessage']`, 쓴 담당 `['loan_desk', 'interlibrary_desk']`, 담당 칸 `interlibrary_desk`, 요청 **2**(첫 담당 1 + 받은 담당 1) · 둘째 차례 쓴 담당 `['interlibrary_desk']`, 요청 **1**. 결론 문장의 중심은 셈(「넘긴 차례 = 첫 담당 1 + 받은 담당 1, 다음 차례 = 받은 담당 1」)과 체크포인터·조건 함수 구조에 두고, 2·1은 「이번 실행에서는 넘겨」로 이어 씀. `assert`는 걸지 않음.
- **5번 가운데 하나라도 다르면**(넘기지 않음, 한 응답에 도구 요청 둘): 입력을 고치지 않고 노트북 결과를 사실대로 두고, 원래 관찰일 때의 값을 「넘기면 …이 됩니다」 꼴 셈 한 문장으로 덧붙이고 b7에 「같은 요청도 실행한 때에 따라 넘기는지가 달라질 수 있다」. 원하는 값이 나올 때까지 다시 돌리지 않음.
- **흔들리는 값 — 결론·그림·정리·복습에 쓰지 않음**(결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만 「이번 실행에서는」): 두 답 글·글자 수·입력/출력 토큰·예상 비용.
- **그림 라벨 규칙**(뒤에서 넓히지 않음): 앞 절반 그림(02-1~02-4)은 모델 없는 결정적 값(담당 칸·실행 흔적·경고 여부·오류 이름·메시지 종류)만. 뒤 절반 그림(02-5)의 라벨에는 구조 값(노드 이름·도구 이름·`Command.PARENT`·도구 메시지 글·셈 「첫 담당 1 + 받은 담당 1」)만 두고, 쓴 담당 목록·요청 2·1은 모델 판단 값이 위 규칙으로 5/5 **그리고** 노트북 새 커널 두 번에서 같을 때만 「넘긴 실행」 한정어와 함께. 답 글·토큰·비용은 라벨·캡션·alt에 넣지 않음.
- 요청 수: 회차당 첫 차례 2 + 둘째 차례 1 = 3(넘길 때) × 5 = 약 **15번**. 더 보내지 않습니다. 오류가 나면 기록만 하고 다시 보내지 않습니다.

## 1. 흔들림 확인 결과 (`probe02.py P1 5`, 기록 `probe/probe-02-P1.jsonl`)

### P1 — 같은 스레드 두 차례 (06:42:52Z~06:43:05Z)

| 회차 | 첫 차례 종류 | 응답마다 도구 요청 | 쓴 담당(첫 차례) | 담당 칸 | 요청 | 입력·출력 토큰 | 둘째 차례 쓴 담당 | 요청 | 입력·출력 토큰 | 예상 비용 합(달러) | 답 글자 수 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H·AI·Tool·AI | [[넘기기], []] | loan_desk·interlibrary_desk | interlibrary_desk | 2 | 471 · 80 | interlibrary_desk | 1 | 259 · 44 | 0.001105 | 98 · 62 |
| 2 | 〃 | 〃 | 〃 | 〃 | 2 | 471 · 80 | 〃 | 1 | 259 · 43 | 0.001101 | 98 · 61 |
| 3 | 〃 | 〃 | 〃 | 〃 | 2 | 471 · 79 | 〃 | 1 | 258 · 44 | 0.001100 | 97 · 62 |
| 4 | 〃 | 〃 | 〃 | 〃 | 2 | 471 · 80 | 〃 | 1 | 259 · 44 | 0.001105 | 98 · 62 |
| 5 | 〃 | 〃 | 〃 | 〃 | 2 | 471 · 80 | 〃 | 1 | 259 · 44 | 0.001105 | 98 · 62 |

- **구조 값 5/5 같음**: 도구 메시지 내용 `['상호대차 담당에게 넘겼습니다.']` · 호출 ID 짝 `True` · 첫 차례 응답 수 2 == `sum_usage` 요청 수 2 · 둘째 차례에 더해진 메시지 `['HumanMessage', 'AIMessage']` · 두 차례 모두 다음 노드 `[]`(= `()`).
- **모델 판단 값 5/5 같음**: 첫 차례 대출 규정 담당의 응답에 넘기기 도구 요청 1개(`[['transfer_to_interlibrary'], []]` — 한 응답에 요청 둘은 0번) · 첫 차례 종류 `['HumanMessage', 'AIMessage', 'ToolMessage', 'AIMessage']` · 쓴 담당 `['loan_desk', 'interlibrary_desk']` · 담당 칸 `interlibrary_desk` · 요청 2 · 둘째 차례 쓴 담당 `['interlibrary_desk']` · 담당 칸 `interlibrary_desk` · 요청 1.
- **흔들린 값**: 첫 차례 출력 토큰 79~80 · 둘째 차례 입력 토큰 258~259·출력 토큰 43~44 · 예상 비용 합 0.001100~0.001105달러 · 두 답 글(첫 차례 97~98자, 다섯 가운데 「신청하실 수」·「신청할 수」와 「3~5일 뒤」·「3~5일 뒤에」가 갈림 · 둘째 차례 61~62자, 쉼표 하나가 갈림). 첫 차례 입력 토큰 471은 다섯 번 같았지만 서비스 쪽 값이라 결론에 쓰지 않음.
- **경고 0건**(`warnings`로 모음 — 맨 `ToolRuntime` 표시로도 Pydantic 경고가 나오지 않음, Ch 21 03 b4의 경고는 `context_schema`가 있는 실행이었음) · 오류 0건.

### 판단

- 구조 값·모델 판단 값 모두 판단 규칙의 「5번 모두 같음」 → **입력 그대로**. 결론은 셈 「넘긴 차례 = 첫 담당 1 + 받은 담당 1, 다음 차례 = 받은 담당 1」과 체크포인터·조건 함수 구조(2절 그래프와 같은 구조 문자열)에 두고, 쓴 담당 목록·요청 2·1은 「이번 실행에서는 넘겨」로 이어 씀(노트북 두 커널에서도 같을 때만 그림 02-5 라벨에 「넘긴 실행」 한정어와 함께).
- 요청: 15번(회차 5 × 3), 서비스 오류 0. 예상 비용 합 약 0.00552달러(요금표 2026-09-17로 어림 — 청구 금액 아님). 노트북 한 번은 요청 3번·약 0.0011달러 → 준비물 「0.002달러 아래」.
- 모델 없는 확인(노트북 밖, 요청 0): `/tmp/ch26-02/exp/x6_propagate.py` — 하위 그래프 안에서 만든 도구 요청 응답은 넘기기로 떠날 때 바깥 메시지 칸에 저절로 들어가지 않음(도구 메시지만 담으면 바깥 기록 `Human·Tool·AI`, 둘 다 담으면 `Human·AI·Tool·AI`). 탐색 단계에서 구조만 보려고 `x3_team.py`·`x5_struct.py`에 라이브러리 가짜 채팅 모델(`FakeMessagesListChatModel`)을 썼음 — 교재·노트북·흔들림 확인에는 없음, 결론 근거로 쓰지 않음(구조 문자열 같음은 노트북 6절 출력 `2절 그래프와 구조 문자열이 같은가: True`로 다시 확인, 넘기지 않으면 끝나는 장면은 본문에 「노트북에서 실행하지 않았습니다」로만 씀).

## 2. 노트북 새 커널 두 번 (교재 출력 A · 사본 B)

- A `run_section.sh`(2026-09-28T06:55:51Z, `code_sha256` `2d1b15cf6e77…`) · B 사본 `/tmp/ch26-02/B/`(06:56:15Z, 그림 라벨 확인 전) 모두 PASS 31셀. 셀별 출력 대조 **29/31 같음** — 갈린 둘은 7절 셀 30(출력 토큰 80 ↔ 81, 답 글 「3~5일 뒤」 ↔ 「3~5일 뒤에」)·셀 31(입력·출력 토큰 259·45 ↔ 260·44, 답 글 「알려드리며」 ↔ 「알려드리고,」).
- 모델 판단 값은 두 커널 모두 흔들림 확인과 같음: 담당 칸 `interlibrary_desk` · 첫 차례 메시지 목록(도구 요청 `transfer_to_interlibrary`·도구 메시지) · 쓴 담당 `['loan_desk', 'interlibrary_desk']` · 짝 `True` · 요청 2 · 둘째 차례 쓴 담당 `['interlibrary_desk']` · 더해진 메시지 2 · 요청 1 → 그림 02-5 라벨에 「넘긴 실행」 한정어와 함께 씀(§0 규칙 안).
- 4절 경고 글(stderr) `Task loan_desk with path ('__pregel_pull', 'loan_desk') wrote to unknown channel branch:to:interlibrary_dsk, ignoring it.`은 A·B 같음 → 결과 읽기 둘째 단락에 끝부분만 인용.
- 요청: A 3 + B 3 = 6. 흔들림 확인 15와 합쳐 **이 절 서비스 요청 21번**, 예상 비용 합 약 0.0077달러(청구 금액 아님).
