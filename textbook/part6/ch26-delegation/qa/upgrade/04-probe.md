# 04절 흔들림 확인 (노트북 밖, 2026-09-28)

규격 §2-7 10번 끝 · 챕터 리드 결정(R1 — 「노트북 실행 전 노트북 밖 5번」). 04절은 같은 문의 하나를 세 구조(서브에이전트·핸드오프·라우터)에 보내고, 호출 한도 1을 붙인 서브에이전트를 한 번 더 실행합니다. 모델 없는 핑퐁 그래프(실행 한도 4)는 요청 0이라 흔들림 확인에서 뺍니다. 키는 루트 `.env`에서만 읽고 출력하지 않습니다. 스크립트 `qa/upgrade/probe/probe04.py`, 기록 `qa/upgrade/probe/probe-04-P1.jsonl`~`P4.jsonl`(기기 `/tmp/ch26-04/probe/`의 사본).

## 0. 실행 전에 적은 입력과 판단 규칙 (2026-09-28T08:00Z, 첫 요청 전에 적음)

공통(노트북과 같은 코드로 씀):

- 모델 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` 객체 하나를 모든 에이전트·분류 모델이 함께 씀(과정 표준 셀).
- 분야 이름 셋 `desk_names = ["loan_desk", "interlibrary_desk", "facility_desk"]` · 규정 글 셋(대출 01절 네 문장 · 상호대차 02절 세 문장 · 시설 03절 한 문장, 글자 그대로) · **전문 에이전트 셋 `desk_agents`는 03절 5절 셀과 같은 코드**(도구 없음, `name=` 분야 이름, `answer_rule` = 「 문의 가운데 아래 교재용 규정에 해당하는 부분에만 한 문장의 한국어로 답하세요.」). 세 구조가 **이 에이전트 셋을 함께 씀**(R1 — 같은 전문 에이전트).
- 담당 설명 글 `desk_guide` = 「 loan_desk는 대출·반납·연장·연체, interlibrary_desk는 다른 도서관 책을 빌려 오는 상호대차를 맡습니다. facility_desk는 자료실 운영 시간과 시설을 맡습니다.」(03절 분류 시스템 메시지 글의 가운데 두 문장 그대로) — 세 구조의 첫 에이전트(중앙 에이전트·안내 담당·분류 모델)가 모두 이 글을 씀.
- 문의 글 `question_text` = 「빌린 책을 연장하려면 어떻게 하나요? 토요일 운영 시간도 알려 주세요.」(03절 문의 그대로 — 03 흔들림 확인에서 분류가 두 분야 5/5). 실행 한도 `limit_config = {"recursion_limit": 10}`(01~03과 같은 값).
- **P1 서브에이전트**: 도구 하나 `@tool ask_desk_agent(desk: str, question: str)`(공식 Subagents 문서의 「single dispatch tool」 모양 — 문서 예 `task(agent_name, description)`이 `SUBAGENTS[agent_name]`을 찾아 `invoke`, 2026-09-28 확인. 01절은 담당마다 도구 하나). 본문 = `agent = desk_agents[desk]` · 넘긴 글 한 줄로 시작한 새 목록 `invoke` · 기록 목록 `specialist_runs.append(안쪽 메시지)` · 마지막 답 글 `.text`(01절 도구와 같은 모양). 독스트링 「문의 가운데 한 분야 부분을 그 분야 담당(loan_desk·interlibrary_desk·facility_desk)에게 맡기고, 담당의 답 글을 받습니다.」. 중앙 에이전트 `supervisor = create_agent(model, tools=[ask_desk_agent], system_prompt=central_text)`, `central_text` = 「도서관 자료실 문의 창구의 안내 도우미입니다. 규정을 묻는 부분은 직접 답하지 말고 ask_desk_agent 도구로 담당에게 맡기세요.」 + `desk_guide` + 「 담당이 준 답을 바탕으로 두 문장의 한국어로 답하세요.」(01절 중앙 글의 뼈대). 요청 수 = `usage_with_specialists(결과[1:], specialist_runs)`(01절 함수).
- **P2 핸드오프**: 상태 형식 `TeamState`(02절 5절과 같은 칸 `messages`·`active_agent`) · 넘기기 도구 `@tool transfer_to_desk(desk: str, runtime: ToolRuntime)`(02절 `transfer_to_interlibrary` 모양에 분야 이름 인자) — `Command(goto=desk, update={"active_agent": desk, "messages": [마지막 응답, ToolMessage(desk + " 담당에게 넘겼습니다.", tool_call_id=…)]}, graph=Command.PARENT)`, 독스트링 「문의를 맡을 담당 한 명(loan_desk·interlibrary_desk·facility_desk)에게 대화를 넘깁니다.」 · 안내 담당 `front_agent = create_agent(model, tools=[transfer_to_desk], system_prompt=front_text, name="front_desk")`, `front_text` = 「도서관 자료실 문의 창구의 안내 담당입니다. 문의에 직접 답하지 말고, 맡을 담당 한 명을 골라 transfer_to_desk 도구로 넘기세요.」 + `desk_guide`(「한 명」은 공식 Handoffs 문서가 「no parallel tool calls」를 전제하기 때문 — 노트북 밖 모델 없는 확인 `e2_parent2.py`에서 한 응답에 넘기기 요청 둘이면 첫 요청만 적용되고 둘째 도구 메시지가 빠짐) · 바깥 그래프 `add_node("front_desk", front_agent, destinations=(세 분야))` + 분야마다 `add_node(분야, desk_agents[분야])`·`add_edge(분야, END)` + `add_edge(START, "front_desk")` · `compile()`(체크포인터 없음 — 한 차례만). 요청 수 = `sum_usage(결과[1:])`.
- **P3 라우터**: 03절 5~6절 셀과 같은 코드(`DeskChoice` · `classify_text` = 03절 글과 같은 글(가운데 두 문장을 `desk_guide`로 이음) · `ModelRouteState` · `classify_by_model` · `send_to_desks` · `ask_desk` · `join_answers` · 그래프). 요청 수 = `sum_usage(응답 칸)`.
- **P4 호출 한도**: P1과 같은 도구·시스템 메시지 글에 `middleware=[ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")]`(Ch 22 04절 이름 그대로). 설치판 `langchain/agents/middleware/model_call_limit.py` 168~208행은 모델 요청 **전** 훅에서 이번 실행 요청 수가 한도 이상이면 `AIMessage("Model call limits exceeded: …")`를 넣고 끝으로 건너뜀, 236~250행은 요청 **뒤** 훅에서 수를 늘림 → 첫 요청은 나가고, 도구 요청이 있으면 도구(담당)는 실행되고, 둘째 요청 전에 끝남(Ch 22 04 출력과 같은 모양 — 노트북 밖에서 서비스 모델로는 아직 안 봄).
- 결과를 보고 규정 글·시스템 메시지 글·문의 글·도구 글·실행 한도를 바꾸지 않습니다.

회차마다 기록: 시각 · (P1·P4) 이번 실행이 더한 바깥 메시지 종류 · 응답마다 도구 요청 수와 인자 `desk` · 넘긴 글 · 전문 에이전트를 부른 횟수 · 담당 답이 모인 분야(`answered_desks` — 분야 이름 차례) · 요청 수(중앙 + 전문) · 마지막 응답의 사용량이 `None`인지·도구 요청 수·(P4) 글 · (P2) 넘기기 요청 수·인자·응답을 쓴 에이전트·담당 칸·도구 메시지 짝 · (P3) 고른 분야(모델이 쓴 차례)·답 칸 줄 수·`parsing_error` · 입력·출력 토큰 · 예상 비용(요금표 2026-09-17, 청구 금액 아님) · 마지막 답 글과 글자 수 · 완료 조건(`is_complete(모인 분야, ["loan_desk", "facility_desk"], 마지막 답 있음)`) · 경고(`warnings`) · 오류.

판단 규칙(결론에 쓸 수 있는 관찰):

- **구조 값 — 코드가 정하는 값이라 5번 모두 같아야 하고, 결론·그림에 씀**: P1 요청 수 == (도구를 요청한 중앙 응답 수 + 1) + 부른 횟수 · 안쪽 목록마다 두 줄 · 도구 메시지 수 == 도구 요청 수 · P2 넘기기 요청이 하나면 요청 수 == 2(넘긴 담당 1 + 받은 담당 1)·응답을 쓴 에이전트 `['front_desk', 받은 담당]`·담당 칸 == 받은 담당·도구 메시지 짝 `True` · P3 요청 수 == 1 + 고른 분야 수·답 칸 줄 수 == 고른 분야 수·`parsing_error` None · P4 첫 응답에 도구 요청이 있으면 마지막 응답 글 「Model call limits exceeded: run limit (1/1)」·사용량 `None`·중앙 응답 중 사용량 있는 것 1 · 완료 조건: P2(한 담당만 답함)·P4는 `False`, P1·P3은 두 분야가 모이고 마지막 답이 있으면 `True`. 하나라도 다르면 결론에서 빼고 진단에 적은 뒤 보고.
- **모델 판단 값 — 5번 모두 같을 때만 결론에 「흔들림 확인 다섯 번과 두 커널에서 모두 …」로 한정해 씀**: P1 중앙 에이전트가 두 분야(`loan_desk`·`facility_desk`)에 맡김과 맡긴 모양(한 응답에 둘이면 요청 2 + 2 = 4, 응답 둘에 하나씩이면 3 + 2 = 5) · P2 안내 담당이 넘기기 요청 하나로 넘김과 받은 담당 이름 · P3 두 분야를 고름(요청 3) · P4 첫 응답의 도구 요청(두 분야) → 담당 두 번 실행. 결론 문장의 중심은 셈(세 구조의 요청 수 공식)과 완료 조건에 두고, 이번 값은 「이번 실행에서는」으로 이어 씀. `assert`는 걸지 않음.
- **5번 가운데 하나라도 다르면**: 입력을 고치지 않고 노트북 결과를 사실대로 두고, 원래 관찰일 때의 값을 「…이면 …이 됩니다」 꼴 셈 한 문장으로 덧붙이고 b7에 「같은 요청도 실행한 때에 따라 맡기는 모양·넘기는 담당·고르는 분야가 달라질 수 있다」. 원하는 값이 나올 때까지 다시 돌리지 않음.
- **흔들리는 값 — 결론·그림·정리·복습에 쓰지 않음**(결과 읽기 둘째 단락·b6 표 「교재 출력」·「확인할 점」·b7에만 「이번 실행에서는」): 답 글·넘긴 글·글자 수 · 도구 요청·고른 분야의 **차례** · 입력/출력 토큰 · 예상 비용. **세 구조의 토큰·비용으로 순위를 매기지 않음**(규격 §2-7 9번 끝).
- **그림 라벨 규칙**(뒤에서 넓히지 않음): 구조 그림에는 노드·도구·에이전트 이름·셈(「중앙 = 도구를 요청한 응답 수 + 1, 전문 = 부른 횟수」·「넘긴 담당 1 + 받은 담당 1」·「분류 1 + 고른 분야 수」)·핑퐁 오류 이름과 한도 4·호출 한도 문구·완료 조건 `True`/`False`(구조 값일 때)만. 이번 실행의 요청 수(4·2·3 등)와 맡긴 분야·받은 담당은 모델 판단 값이 위 규칙으로 5/5 **그리고** 노트북 새 커널 두 번에서 같을 때만 「이번 실행」 한정어와 함께. 토큰·비용·답 글은 라벨·캡션·alt에 넣지 않음.
- 요청 어림: 회차당 P1 4~5 · P2 2 · P3 3 · P4 3 = 약 12~13 × 5 = 약 **60~65번**(예상 비용 약 0.05달러 아래 — 청구 금액 아님). 더 보내지 않습니다. 오류가 나면 기록만 하고 다시 보내지 않습니다. 셸 한 호출 180초라 P1~P4를 호출마다 나눠 `timeout 165`로 부름.

### 0-2. P2 첫 판 결과와 설계 바꿈 (2026-09-28T08:06Z에 적음 — P2b 첫 요청 뒤, 마감 고침)

> **마감 고침(2026-09-28, 검토 B-10)**: 처음에는 머리에 「P2b 첫 요청 전에 적음」이라 적었습니다. 그러나 기록 `probe/probe-04-P2b.jsonl`의 첫 요청은 08:05:53Z이고 `probe/probe04.py`는 08:05:34Z에 고쳐져, 이 절의 시각 08:06Z보다 앞섭니다. **이 §0-2는 P2b 첫 요청 뒤에 적었습니다.** 다섯 번 결과(넘기기 요청 둘·서비스 400)가 모두 같아 결론은 바뀌지 않습니다.
>
> **마감 고침(검토 B-3)**: 아래 첫 항목의 까닭(`prebuilt/tool_node.py` 895~920행의 합치기, 모델 없는 확인 `e2_parent2.py`)은 노트북이 지나는 자리가 아닙니다. `e2_parent2.py`는 도구 실행 노드 하나에 요청 둘을 한꺼번에 넣은 모양이라 늘 첫째만 적용됩니다. `create_agent`는 도구 요청마다 도구 실행 노드를 따로 부르고(langchain 1.4.0 `agents/factory.py` 1964행 `Send("tools", [tool_call])`), 넘기기 도구 둘이 저마다 `ParentCommand`를 올려 보냅니다(langgraph 1.2.11 `graph/state.py` 1762행). `ParentCommand`는 `GraphBubbleUp`이라 다른 작업을 멈추지 않고, 두 작업이 끝난 뒤 `pregel/_runner.py` `_panic_or_proceed`(650~690행)가 끝난 작업 모음(집합)에서 꺼낸 하나를 올려 보냅니다. 그래서 도구 요청 차례가 같아도 적용된 담당이 대출 셋·시설 둘로 갈렸습니다(「첫째만 적용된다」고 전제하지 말 것). 마감에서 검토자의 모델 없는 `create_agent` 모양 확인 `/tmp/reviewB26/t3.py`(요청 0)를 다시 돌려, 여섯 번씩 지연 없음 대출 4·시설 2 · 대출 쪽 0.2초 지연 대출 4·시설 2 · 시설 쪽 지연 대출 5·시설 1로 먼저 끝난 쪽이 정해 주지 않음을 확인했습니다(검토 때는 4·2 · 1·5 · 3·3). `prebuilt/tool_node.py`는 langgraph-prebuilt 1.1.0 소속입니다(langgraph 1.2.11 아님).

- **P2 첫 판(§0 코드, 체크포인터 없음) 5번 모두 서비스 오류**(08:02:04Z~08:02:13Z, 기록 `probe-04-P2.jsonl`): `OpenAIInvalidRequestError: Error code: 400 - … "An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'. The following tool_call_ids did not have response messages: call_…"`. 안내 담당이 **한 응답에 넘기기 요청을 둘** 낸 것으로 보임(시스템 메시지 글의 「한 명」에도) → 설치판 도구 실행 노드는 부모 그래프로 가는 `Command` 여럿을 `goto`가 `Send` 목록일 때만 합치고(`prebuilt/tool_node.py` 895~920행), 노트북 밖 모델 없는 확인 `e2_parent2.py`에서 **첫 넘기기만 적용되고 둘째 도구 메시지가 빠짐** → 받은 담당의 모델 요청에 짝 없는 도구 요청이 실려 서비스가 400으로 거절. 공식 Handoffs 문서의 두 문장(「assumes only the handoff tool was called (no parallel tool calls)」·「without it, the conversation history becomes malformed」)과 같은 장면. 이 첫 판은 오류가 기록을 지워 도구 요청 수·받은 담당을 적지 못했음(다시 보내지 않음).
- **판단**: 입력(문의 글·시스템 메시지 글·도구 글·실행 한도)은 바꾸지 않습니다(§0 규칙 — 결과를 고르려고 바꾸지 않음). 오류는 노트북이 받아 출력하는 **실제 조건의 실패 장면**(규격 §3)으로 두고, 그 전 기록을 보이려고 **바깥 그래프에만 체크포인터(`InMemorySaver`, Ch 23 01절)를 붙이고 `get_state`로 멈추기 전 체크포인트를 읽는 코드를 더함**(모델 요청 수는 같음). 받는 오류는 `langchain_core.exceptions.ModelInvalidRequestError`(제공자가 요청을 잘못된 요청으로 거절할 때의 공통 오류 — 올라온 것은 그 OpenAI용 하위 오류 `OpenAIInvalidRequestError`). 오류가 안 나면 셀은 「오류 없이 끝났습니다」를 출력하고 같은 기록을 읽음.
- **P2b 판단 규칙**(§0 규칙을 이 모양으로): 구조 값 — 오류가 나면 체크포인트의 메시지 종류 `['AIMessage', 'ToolMessage']`·다음 노드 `(받은 담당,)`·도구 메시지 하나·첫 요청과 짝 `True`·요청 1(안내 담당)·완료 조건 `False` / 모델 판단 값 — 넘기기 요청 수(2)와 첫 요청의 분야 이름(담당 칸) / 흔들리는 값 — 토큰·비용. 그림 라벨 규칙은 §0 그대로(넘기기 요청 수·받은 담당은 5/5와 두 커널 같을 때만 「이번 실행」 한정어와 함께). 요청 어림: 회차당 안내 담당 1(+ 거절된 요청 1) × 5.

## 1. 흔들림 확인 결과 (기록 `probe/probe-04-P1·P2·P2b·P3·P4.jsonl`)

### P1 — 서브에이전트 (08:01:27Z~08:01:47Z)

| 회차 | 바깥 새 메시지 | 응답마다 도구 요청(인자 desk) | 부른 횟수 | 모인 분야 | 요청 | 마지막 응답 | 완료 조건 | 입력·출력 토큰 | 예상 비용(달러) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | AI·Tool·Tool·AI | [[loan_desk, facility_desk], []] | 2 | loan_desk·facility_desk | 4 | 모델 응답·도구 요청 0 | True | 977 · 202 | 0.001642 |
| 2 | 〃 | 〃 | 2 | 〃 | 4 | 〃 | True | 951 · 183 | 0.001537 |
| 3~5 | 〃 | 〃 | 2 | 〃 | 4 | 〃 | True | 962 · 193 | 0.00159 |

- 구조 값 5/5: 요청 == (도구를 요청한 중앙 응답 1 + 1) + 부른 횟수 2 · 안쪽 목록마다 두 줄 · 도구 메시지 2 == 도구 요청 2. 모델 판단 값 5/5: **한 응답에서 두 분야에 맡김 → 요청 4**. 흔들린 값: 넘긴 글(「…연장 방법과 필요한 조건이 있으면 알려 주세요.」·「빌린 책을 연장하려면 어떻게 하나요?」·「…안내해 주세요.」 셋), 최종 답 글, 토큰 951~977 · 183~202, 비용. 경고·오류 0.

### P2 — 핸드오프 첫 판(§0 코드, 체크포인터 없음) (08:02:04Z~08:02:13Z)

- 5/5 `OpenAIInvalidRequestError`(400, 「An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'. The following tool_call_ids did not have response messages: …」) — 오류가 기록을 지워 도구 요청 수·받은 담당은 기록 못 함. 안내 담당 요청 5번(응답 받음, 토큰은 기록 없음 — P2b와 같은 코드라 약 0.000446달러 × 5로 어림) + 거절된 요청 5번. → §0-2 판단.

### P2b — 핸드오프 노트북 판(체크포인터 + 오류 받기 + `get_state`) (08:05:53Z~08:05:58Z)

| 회차 | 받은 오류 | 저장된 메시지 | 넘기기 요청(인자 desk) | 도구 메시지 | 담당 칸 · 다음 노드 | 요청 | 완료 조건 | 입력·출력 토큰 |
|---|---|---|---|---|---|---|---|---|
| 1 | OpenAIInvalidRequestError · 400 | AI·Tool | 2 (loan_desk, facility_desk) | 「facility_desk 담당에게 넘겼습니다.」 | facility_desk · (facility_desk,) | 1 | False | 265 · 55 |
| 2 | 〃 | 〃 | 〃 | 「loan_desk 담당에게 넘겼습니다.」 | loan_desk · (loan_desk,) | 1 | False | 265 · 55 |
| 3 | 〃 | 〃 | 〃 | 〃 loan_desk | loan_desk | 1 | False | 265 · 55 |
| 4 | 〃 | 〃 | 〃 | 〃 facility_desk | facility_desk | 1 | False | 265 · 55 |
| 5 | 〃 | 〃 | 〃 | 〃 loan_desk | loan_desk | 1 | False | 265 · 55 |

- 구조 값 5/5: 오류 이름·상태 코드 400·첫 문장 같음 · 저장된 메시지 `['AIMessage', 'ToolMessage']` · 도구 메시지 하나가 적용된 넘기기 요청과 짝(첫 요청과 짝 `True`는 loan_desk가 적용된 2·3·5회, facility_desk가 적용된 1·4회는 둘째 요청과 짝) · 다음 노드 하나 · 요청 1 · 완료 조건 `False`. 모델 판단 값 5/5: **한 응답에 넘기기 요청 둘**(모델이 쓴 차례 loan_desk → facility_desk). **흔들린 값: 적용된 넘기기(담당 칸) loan_desk 3 · facility_desk 2** — 모델이 아니라 도구 실행 노드의 함께 실행 차례로 보임(두 도구 요청이 함께 실행되고 먼저 끝난 부모행 `Command`가 올라감 — 소스 추적은 하지 않음, 노트북 밖 모델 없는 확인 `e2_parent2.py`는 세 번 모두 첫째였음). 둘째 단락·b7에만.

### P3 — 라우터 (08:04:24Z~08:04:33Z)

- 5/5: 고른 분야 `['loan_desk', 'facility_desk']` · 답 칸 두 줄 · 요청 3 == 1 + 2 · `parsing_error` None · 완료 조건 `True`. 흔들린 값: 출력 토큰(이번 다섯 번은 86으로 같았지만 03절 확인에서 86~89) · 답 글.

### P4 — 호출 한도 1 (08:04:42Z~08:04:50Z)

- 5/5: 바깥 새 메시지 `['AIMessage', 'ToolMessage', 'ToolMessage', 'AIMessage']` · 첫 응답 도구 요청 둘(loan_desk·facility_desk) → 부른 횟수 2 · 마지막 응답 글 「Model call limits exceeded: run limit (1/1)」 · 사용량 `None` · 요청 3(중앙 1 + 전문 2 — 호출 한도는 한도를 붙인 중앙 에이전트 요청만 셈) · 완료 조건 `False`. 흔들린 값: 토큰 514~519 · 132~143, 넘긴 글.

### 판단

- 구조 값·모델 판단 값 모두 「5번 모두 같음」 → **입력 그대로**(핸드오프 오류 장면 포함 — §0-2). 결론 중심은 세 구조의 셈과 완료 조건, 이번 값은 「이번 실행」·「흔들림 확인 다섯 번과 두 커널에서 모두」로 한정. 담당 칸은 흔들린 값.
- 요청(응답을 받은 것): P1 20 · P2 5 · P2b 5 · P3 15 · P4 15 = **60번** + 서비스가 거절한 요청 10번. 예상 비용 합 약 0.0189달러(기록한 네 판) + P2 첫 판 약 0.0022달러 ≈ **약 0.021달러**(요금표 2026-09-17, 청구 금액 아님).
- 모델 없는 확인(노트북 밖, 요청 0, 기기 `/tmp/ch26-04/exp/`): `e1_bounce.py`(핑퐁 그래프 — 한도 2·3·4·5·10 모두 `GraphRecursionError`, 한도 N이면 노드 N번 실행 뒤 오류 · 오류 글) · `e2_parent2.py`(손으로 만든 응답에 넘기기 요청 하나·둘·없는 이름 — 하나면 정상, 둘이면 첫째만 적용·둘째 도구 메시지 없음, 없는 이름은 담당 칸만 바뀌고 조용히 끝남). 가짜 채팅 모델 없음.

## 2. 노트북 새 커널 두 번 (교재 출력 A · 사본 B)

- A `run_section.sh`(2026-09-28T08:26:33Z 실행, `code_sha256` `bc1e02160142…` · `outputs_sha256` `3f6d995346c3…`) · B 사본 `/tmp/ch26-04/B/`(08:26:52Z~08:27:02Z, 그림 라벨 확정 전) 모두 PASS 30셀. 셀별 출력 대조 **29/30 같음** — 갈린 셀은 6절 요청 수 표(code25) 하나: 서브에이전트 A 989·228·0.001768 ↔ B 963·195·0.0016, 라우터 A 468·87·0.000742 ↔ B 468·95·0.000779(요청 수 칸 4·1·3과 핸드오프 줄은 같음).
- 모델 판단 값은 두 커널 모두 흔들림 확인과 같음: 3절 한 응답에 두 담당 · 요청 4 · 4절 넘기기 요청 2 · 요청 1 · 오류 400 · 5절 두 분야 · 요청 3 · 7절 한도 글 · 8절 `True`·`False`·`True`·`False`. 4절 담당 칸은 두 커널 모두 `loan_desk`였지만 흔들림 확인에서 갈렸으므로 둘째 단락·b7에만.
- 요청: A 11 + B 11 = 22(+ 거절된 요청 2). 예상 비용 A 약 0.0040 · B 약 0.0038달러(7절 호출 한도 실행은 토큰을 출력하지 않아 P4 평균으로 어림).
