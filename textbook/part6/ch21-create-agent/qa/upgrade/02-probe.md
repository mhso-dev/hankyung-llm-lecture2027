# 02절 흔들림 확인 (노트북 밖, 2026-09-25)

규격 §2-7 10번 끝 · 챕터 리드 결정 8 · 인계 「§01 → §02」 4·6·7. 노트북을 쓰기 **전에** 두 전략(ToolStrategy·ProviderStrategy)과 값 바꿔 보기 후보(양식 클래스를 그대로 넘김)를 노트북 밖에서 **5번씩** 봅니다. 키는 루트 `.env`에서만 읽고 출력하지 않습니다.

## 0. 실행 전에 적은 입력과 판단 규칙 (2026-09-25T02:37Z, 첫 요청 전에 적음)

공통(노트북과 같은 코드):

- 모델 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` 객체(01과 같음).
- 자료 `POLICIES` 셋과 도구 `@tool lookup_policy(topic: str)` — **01 노트북 셀과 같은 코드**(Ch 20 01과 코드 줄이 같음).
- 시스템 메시지 글 — **01 판 그대로**: 「교육센터 자료실 안내 도우미입니다. 자료실 규정을 묻는 질문에는 lookup_policy 도구로 찾은 규정 글에 근거해 답하세요.」(결과를 보고 바꾸지 않음).
- 양식 클래스(설계로 정함, 결과를 보고 바꾸지 않음):
  ```python
  class PolicyAnswer(BaseModel):
      topic: Literal["대출", "운영", "연체"] = Field(description="답의 근거가 된 규정의 주제어")
      answer: str = Field(description="찾은 규정 글에 근거한 한 문장 답")
  ```
  칸 둘. 옛 판의 `source`(지어낸 자료 번호 `R-14`)는 뺐습니다 — 근거는 도구 메시지가 보여 주고, 모델이 지어낸 번호를 칸으로 받지 않기 위해서입니다. `topic`은 `Literal`이라 코드가 「정해 둔 셋 안인가」를 판정할 수 있습니다.
- 에이전트 셋:
  - **TS** `create_agent(model, tools=[lookup_policy], system_prompt=system_text, response_format=ToolStrategy(PolicyAnswer))`
  - **PS** 같은 줄에 `response_format=ProviderStrategy(PolicyAnswer)`
  - **AS(값 바꿔 보기 후보)** 같은 줄에 `response_format=PolicyAnswer`(양식 클래스를 그대로)
- 입력 하나(01 L과 같은 글): 「자료실에서 일반 도서를 며칠 빌릴 수 있나요?」 · 입력 상태 `{"messages": [HumanMessage(content=질문)]}`.

설치판에서 미리 본 것(모델 요청 없이, 가짜 키 글자로 그래프만 만듦 — `/tmp/ch21-02/shape_check.py`): TS·AS 그래프는 `tools | tools_to_model | ['model', '__end__']` · PS는 `['model']` · 셋 모두 `model | model_to_tools | ['tools', '__end__', 'model']` · 모델 프로필 `structured_output: True`.

회차마다 기록: 결과 딕셔너리 키 · 메시지 종류 차례 · 응답마다 도구 호출 요청 이름과 인자 · 도구 메시지 이름·결과 상태·내용 · 요청 id 목록 == 호출 ID 목록 · 응답 수 · `structured_response` 자료형 이름 · `model_dump()` 키와 값 · `topic`이 정해 둔 셋 안인가 · 마지막 응답의 도구 호출 요청 수·내용 글 길이 · 응답마다 사용량(입력·출력·캐시 입력) · 오류.

판단 규칙(결론에 쓸 수 있는 관찰):

- **TS 예상 모양**: 종류 `HumanMessage, AIMessage, ToolMessage, AIMessage, ToolMessage` · 첫 응답 요청 `lookup_policy {'topic': '대출'}` · 둘째 응답 요청 `PolicyAnswer` 하나 · 마지막 도구 메시지 이름 `PolicyAnswer`, 내용이 `Returning structured response:`로 시작 · 키 `['messages', 'structured_response']` · 자료형 `PolicyAnswer` · 짝 `True`.
- **PS 예상 모양**: 종류 `HumanMessage, AIMessage, ToolMessage, AIMessage` · 첫 응답 `lookup_policy {'topic': '대출'}` · 마지막 응답 요청 0건(내용 글이 양식 JSON) · 키·자료형·짝 같음.
- **AS**: PS와 같은 모양이면 「양식 클래스를 그대로 넘기면 이 모델에서는 ProviderStrategy 쪽 모양」으로 씀(근거는 소스 1357~1367행 + 프로필 값 + 메시지 모양).
- 각 입력에서 **5번 모두 같은 모양**이면 그 모양(메시지 종류·수·도구 요청 이름·응답 수)을 결론·그림에 씀.
- 하나라도 다르면(예: 한 응답에 `lookup_policy`와 `PolicyAnswer`를 함께 요청, 도구를 부르지 않고 바로 양식, 양식 검사 실패로 다시 요청): **입력과 양식을 그대로 두고**, 결론은 코드로 정해지는 값(결과 키·`structured_response` 자료형·양식 칸 이름·`topic`이 셋 안인가·호출 ID 짝)에만 두고, 메시지 모양은 결과 읽기 둘째 단락·b7에 다른 회차 수와 함께 적음. 노트북 결과가 다르면 사실대로 두고 원래 모양일 때의 수를 셈 한 문장으로 덧붙임.
- 입력 토큰(응답마다)이 5번 모두 같으면 결과 읽기 첫 단락 가까이에 둘 수 있음(01과 같은 규칙). 출력 토큰·양식 칸 값(`topic` 값·`answer` 글)·예상 비용은 모델 글에 따라 달라지므로 둘째 단락에만.
- 입력 후보는 위 하나뿐이고, 에이전트 셋의 차이는 `response_format` 값 하나입니다. 결과를 보고 질문·시스템 메시지 글·양식 칸 설명을 바꾸지 않습니다.

## 1. 흔들림 확인 결과 (`probe02.py TS 5` · `PS 5` · `AS 5`, 기록 `probe/probe-{TS,PS,AS}.jsonl` — 기기 `/tmp/ch21-02/`의 사본)

| 설정 | 시각(UTC) | 결과 키 | 메시지 종류 | 응답마다 도구 호출 요청 | 도구 메시지 | 호출 ID 짝 | `structured_response` | 마지막 응답 | 입력 토큰(응답마다) | 출력 토큰(응답마다) |
|---|---|---|---|---|---|---|---|---|---|---|
| TS 도구 전략 | 02:37:57~02:38:05 | `['messages', 'structured_response']` 5/5 | Human·AI·Tool·AI·Tool **5/5** | `lookup_policy {'topic': '대출'}` → `PolicyAnswer {topic, answer}` **5/5** | 2개 — `lookup_policy` `success` 규정 글 · `PolicyAnswer` `success` 「Returning structured response: topic='대출' answer='…'」 5/5 | `True` 5/5 | `PolicyAnswer` · 칸 `topic`·`answer` · 주제어 셋 안 `True` 5/5 | 마지막 메시지는 도구 메시지, 둘째 응답 내용 글 `''`(길이 0) 5/5 | 261 · 311 **5/5** | 18 · 42 **5/5** |
| PS 제공자 전략 | 02:38:13~02:38:21 | 같음 5/5 | Human·AI·Tool·AI **5/5** | `lookup_policy {'topic': '대출'}` → 0건 **5/5** | 1개 · `success` 5/5 | `True` 5/5 | 같음 5/5 | 마지막 응답 요청 0건, 내용 글 `{"topic":"대출","answer":"…"}` 5/5 | 359 · 409 **5/5** | 18 · 37 **5/5** |
| AS 양식 클래스 그대로 | 02:38:24~02:38:30 | 같음 5/5 | Human·AI·Tool·AI **5/5**(PS와 같음) | PS와 같음 **5/5** | 1개 · `success` 5/5 | `True` 5/5 | 같음 5/5 | PS와 같음 5/5 | 359 · 409 **5/5** | 18 · 37 **5/5** |

- 모델 `response_metadata["model_name"]` 15/15 `gpt-5.4-mini-2026-03-17`, 캐시 입력 30/30 0, 오류 0, 양식 검사 실패로 다시 요청한 회차 0. 요청 **30번**(TS 10 · PS 10 · AS 10).
- 양식 칸 값(기록만, 결론에 쓰지 않음): 15/15 `topic` `대출` · `answer` 「일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.」(도구 메시지 규정 글과 글자까지 같음).
- **판단**: 세 설정 모두 판단 규칙의 「5번 모두 같음」 → 입력·양식을 그대로 쓰고, 메시지 모양(5 ↔ 4)·도구 요청 이름·응답 수·입력 토큰(TS 572 · PS 768)을 결론·그림에 씀. 양식 칸 값·출력 토큰·예상 비용은 5/5 같았지만 모델 글에 따르는 값이라 결과 읽기 둘째 단락(「이번 실행에서는」)에만 둠.
- 한 응답에 `lookup_policy`와 `PolicyAnswer`를 함께 요청한 회차는 **0** → 조건 함수 `tools_to_model`이 끝으로 가는 장면(소스 2028~2030행)은 이번에도 나오지 않았습니다(노트북 b7에 「실행하지 않았습니다」).
- 참고(결론에 쓰지 않음): 01절 같은 질문(양식 없음)의 입력 토큰은 203 · 253이었습니다. 양식을 붙이면 TS는 응답마다 58, PS는 156 늘었지만, 어느 몫이 몇 토큰인지(도구 명세 하나 · `response_format` 칸 · `strict=True`)는 나눠 세지 않았습니다.
- 노트북 새 커널 두 번(A·B)도 위 값과 같았습니다(`02-diagnosis.md` §4).
