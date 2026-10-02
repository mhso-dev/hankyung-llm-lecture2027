# 03절 흔들림 확인 (노트북 밖, 2026-09-25)

규격 §2-7 10번 끝 · 챕터 리드 결정 8 · 인계 「§02 → §03」 4·6·7. 노트북을 쓰기 **전에**, 모델이 컨텍스트를 읽는 도구를 부르는지(부르지 않으면 도구 메시지가 없어 컨텍스트가 도구에 들어가는 장면이 사라짐)를 노트북 밖에서 **5번씩** 봅니다. 키는 루트 `.env`에서만 읽고 출력하지 않습니다.

## 0. 실행 전에 적은 입력과 판단 규칙 (2026-09-25T03:13Z, 첫 요청 전에 적음)

### 0-1. 모델 없이 먼저 본 것 (요청 0, 가짜 키 글자·키 뺌 — `/tmp/ch21-03/inject_check.py`·`inject_flow.py`·`warn_variants.py`)

- `AgentState is langchain.agents.middleware.AgentState` → `True`(Ch 22가 가져오는 자리와 같은 클래스).
- 도구 `check_my_loan(runtime: ToolRuntime)`의 입력 형식 `{}` · `convert_to_openai_tool` 명세 `parameters` = `{'properties': {}, 'type': 'object'}`(매개변수 `runtime`이 명세에 없음).
- 에이전트 그래프: 상태 형식 없이 `['messages', 'jump_to', 'structured_response']` ↔ `state_schema=LibraryState` `['messages', 'jump_to', 'structured_response', 'ticket_no']` · 노드 `['model', 'tools']`·조건 함수와 갈 곳은 01절과 같음(`tools_to_model` → `['model']` · `model_to_tools` → `['tools', '__end__']`) · 구조 문자열 01절과 같음.
- **주입 확인 ①**(준비 노트 §5-3 모양): `create_agent`가 만든 `ToolNode`(`agent.builder.nodes["tools"].runnable`)를 `StateGraph(LibraryState, context_schema=MemberContext)`에 넣고 손으로 만든 도구 호출 요청 + `context={"member_id": "M-0317", "overdue_days": 0}` → 도구 메시지 `이용자 M-0317: 연체가 없어 새 대출을 할 수 있습니다.`(`success`), 결과 키 `['messages', 'ticket_no']`. `overdue_days` 3이면 `이용자 M-0317: 연체 3일. 연체한 일수만큼 새 대출이 제한됩니다.`
- **주입 확인 ②**(`create_agent` 흐름 전체): 노트북 밖 확인용 대본 모델(`GenericFakeChatModel`에 `bind_tools`만 더한 것 — 첫 응답에 `check_my_loan {}` 요청, 둘째 응답 글)을 `create_agent(…, state_schema=LibraryState, context_schema=MemberContext)`에 넣어 `invoke(상태, context=딕셔너리)` → 도구 메시지에 컨텍스트 값이 들어감(0일·3일 모두), 결과 키 `['messages', 'ticket_no']`, `ticket_no` 입력 값 그대로. 컨텍스트를 빼고 부르면 도구 안에서 `TypeError: 'NoneType' object is not subscriptable`(도구 오류 — 노트북에서 실행하지 않음).
- **경고**: 표시를 `ToolRuntime`만 적으면 컨텍스트 모양(`TypedDict`·데이터 클래스·`BaseModel`) 셋 모두 흐름 한 번에 Pydantic 직렬화 `UserWarning` **2건**(`field_name='context'` · `Expected none`), `ToolRuntime[컨텍스트 형식]`으로 적으면 셋 모두 **0건**. 도구 메시지·입력 형식은 두 적기에서 같음. → 노트북은 `runtime: ToolRuntime[MemberContext]`로 적음(까닭은 진단 §3·강사 확인 대상, 공식 문서 Tools 예도 컨텍스트를 읽는 도구는 `ToolRuntime[UserContext]`).

### 0-2. 흔들림 확인 입력(노트북과 같은 코드, 결과를 보고 바꾸지 않음)

- 모델 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` 객체(01·02와 같음).
- 자료 `POLICIES` 셋 — 01절 셀과 같은 글(도구가 연체 규정 글을 읽음).
- 상태 형식 `class LibraryState(AgentState): ticket_no: str` · 컨텍스트 형식 `class MemberContext(TypedDict): member_id: str · overdue_days: int`.
- 도구(설계로 정함):
  ```python
  @tool
  def check_my_loan(runtime: ToolRuntime[MemberContext]):
      """자료실 이용자 본인이 지금 새 책을 빌릴 수 있는지 확인합니다."""
      member = runtime.context["member_id"]
      days = runtime.context["overdue_days"]
      if days == 0:
          return "이용자 " + member + ": 연체가 없어 새 대출을 할 수 있습니다."
      return "이용자 " + member + ": 연체 " + str(days) + "일. " + POLICIES["연체"]
  ```
- 시스템 메시지 글(01 글과 같은 틀, 도구만 바꿈): 「교육센터 자료실 안내 도우미입니다. 이용자가 지금 새 책을 빌릴 수 있는지 물으면 check_my_loan 도구로 확인한 결과에 근거해 답하세요.」 — 01절 도구 `lookup_policy`는 에이전트에 넣지 않음(도구를 부를지를 한 가지로 보기 위해).
- 에이전트: `create_agent(model, tools=[check_my_loan], system_prompt=system_text, state_schema=LibraryState, context_schema=MemberContext)`.
- 질문 하나: 「제가 지금 새 책을 빌릴 수 있나요?」 · 입력 상태 `{"messages": [HumanMessage(content=질문)], "ticket_no": "Q-017"}`.
- 설정 둘(바꾼 값은 컨텍스트의 `overdue_days` 하나):
  - **R0** `context={"member_id": "M-0317", "overdue_days": 0}`(노트북 7절)
  - **R3** `context={"member_id": "M-0317", "overdue_days": 3}`(노트북 8절 값 바꿔 보기)

회차마다 기록: 결과 딕셔너리 키 · `ticket_no` 값 · 메시지 종류 차례 · 응답마다 도구 호출 요청 이름과 인자 · 도구 메시지 결과 상태·내용 · 요청 id 목록 == 호출 ID 목록 · 응답 수 · 마지막 응답 글 · 응답마다 사용량(입력·출력·캐시 입력) · 모델 이름 · 경고 수 · 오류.

### 0-3. 판단 규칙

- **예상 모양(R0·R3 같음)**: 키 `['messages', 'ticket_no']` · `ticket_no` `Q-017` · 종류 `HumanMessage, AIMessage, ToolMessage, AIMessage` · 첫 응답 요청 `check_my_loan {}` 하나 · 도구 메시지 `success`, 내용 R0 `이용자 M-0317: 연체가 없어 새 대출을 할 수 있습니다.` / R3 `이용자 M-0317: 연체 3일. 연체한 일수만큼 새 대출이 제한됩니다.` · 짝 `True` · 응답 2 · 경고 0.
- 두 설정에서 **5번 모두 같은 모양**이면 그 모양(메시지 종류·수·도구 요청 이름·응답 수)을 결론·그림에 씀.
- 하나라도 다르면(도구를 부르지 않음, 인자를 채움, 요청이 둘, 도구를 두 번 부름): **입력을 그대로 두고**, 결론은 코드로 정해지는 값(결과 키·`ticket_no` 값·상태 칸 목록·도구 명세·도구 메시지가 있을 때 그 내용)에만 두고, 메시지 모양은 결과 읽기 둘째 단락·b7에 다른 회차 수와 함께 적음. 노트북 결과가 다르면 사실대로 두고 원래 모양일 때의 수를 셈 한 문장으로 덧붙임.
- 입력 토큰(응답마다)이 5번 모두 같으면 결과 읽기 첫 단락 가까이에 둘 수 있음. 출력 토큰·마지막 응답 글·예상 비용은 둘째 단락에만.
- 입력 후보는 위 하나뿐이고, 두 설정의 차이는 컨텍스트 값 하나입니다. 결과를 보고 질문·시스템 메시지 글·도구 글·컨텍스트 값을 바꾸지 않습니다.

## 1. 흔들림 확인 결과 (`probe03.py R0 5` · `R3 5`, 기록 `probe/probe-{R0,R3}.jsonl` — 기기 `/tmp/ch21-03/`의 사본)

| 설정 | 시각(UTC) | 결과 키 | `ticket_no` | 메시지 종류 | 응답마다 도구 호출 요청 | 도구 메시지 | 호출 ID 짝 | 경고 | 입력 토큰(응답마다) | 출력 토큰(응답마다) |
|---|---|---|---|---|---|---|---|---|---|---|
| R0 연체 0일 | 03:14:13~21 | `['messages', 'ticket_no']` 5/5 | `Q-017` 5/5 | Human·AI·Tool·AI **5/5** | `check_my_loan {}` → 0건 **5/5** | `success` 「이용자 M-0317: 연체가 없어 새 대출을 할 수 있습니다.」 5/5 | `True` 5/5 | 0 | 189 · 237 **5/5** | 15 · 24/29/23/24/24 |
| R3 연체 3일 | 03:14:30~36 | 같음 5/5 | `Q-017` 5/5 | Human·AI·Tool·AI **5/5** | `check_my_loan {}` → 0건 **5/5** | `success` 「이용자 M-0317: 연체 3일. 연체한 일수만큼 새 대출이 제한됩니다.」 5/5 | `True` 5/5 | 0 | 189 · 245 **5/5** | 15 · 64/64/61/64/61 |

- 모델 `response_metadata["model_name"]` 10/10 `gpt-5.4-mini-2026-03-17`, 캐시 입력 20/20 0, 오류 0. 요청 **20번**(R0 10 · R3 10).
- 마지막 응답 글(기록만, 결론에 쓰지 않음): R0 「네, 가능합니다. 현재 연체가 없어 …」 넷·「네, 지금 새 책을 빌릴 수 있습니다. …」 하나 — **글자까지 같지 않음**. R3 다섯 모두 「지금은 새 책을 빌릴 수 없습니다. 확인 결과, 연체 3일이라서 …」로 시작하고 끝 문장(「3일 후에/후에 … 가능해집니다/가능합니다」)이 조금씩 다름. 끝 문장의 「3일 후」는 모델이 규정 글에서 끌어낸 말이라 교재 결론에 쓰지 않음.
- **판단**: 두 설정 모두 판단 규칙의 「5번 모두 같음」 → 입력을 그대로 쓰고, 메시지 모양(넷)·도구 요청 이름과 빈 인자·응답 수(2)·도구 메시지 내용을 결론·그림에 씀. 입력 토큰(R0 426 · R3 434)은 5/5 같아 첫 단락 가까이에 둘 수 있음. 출력 토큰·마지막 응답 글·예상 비용은 둘째 단락에만.
- 두 설정의 둘째 요청 입력 토큰 차이 8(237 ↔ 245)은 도구 메시지 글이 달라서 생긴 것으로 보이지만, 토큰 몫을 나눠 세지는 않았습니다.
- 도구 표시를 `ToolRuntime[MemberContext]`로 적어 경고는 10/10 0건(§0-1의 모델 없는 확인과 같음).
- 모델 없는 확인 스크립트(§0-1)는 `probe/check03_inject_check.py`·`check03_inject_flow.py`·`check03_warn_variants.py`에 사본을 두었습니다(원본은 기기 `/tmp/ch21-03/`). `probe/check03_old_api_peek.py`는 04절 인계용 모델 없는 확인입니다(`handoff.md` 「§03 → §04」).
