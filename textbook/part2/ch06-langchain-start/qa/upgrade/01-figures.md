# 01 계층 지도와 첫 호출 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 01-5 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 노란 쪽지가 프롬프트, 서류철이 컨텍스트, 쟁반이 하네스, 회전 받침이 루프입니다. | 값 없음(비유). 쪽지 < 서류철 < 쟁반(도장·공책) < 둥근 회전 받침 | — |
| 01-1 | 4 핵심 개념 · 네 범위 (노트북 「오늘 볼 그림」) | Mermaid flowchart TB(칸 세 겹 + 보이지 않는 연결로 세로 배치) | 프롬프트·컨텍스트·하네스·루프는 적은 질문에서 반복 흐름까지 범위를 넓혀 읽는 지도입니다. | 구조 도식. 노트북 3절 system 문장(프롬프트), 4절 `model.invoke(messages)`, 칸 제목 LangGraph·DeepAgents, 모델 호출 상자에 LangChain | 넣은 문장 tool 초록, 실행한 코드 flow 파랑, 이 절에서 실행하지 않은 단계(입력 검사와 답 기록, 다시 요청할지 정하기) 회색 |
| 01-2 | 5 실행 예제 · 첫 호출에서 오간 것 | Mermaid sequenceDiagram(`messageAlign: left`) | 함수 `init_chat_model()`은 모델 객체만 만들고, 메서드 `invoke()`가 요청을 보냅니다. | [2절] `모델 객체 종류: ChatOpenAI`·`출력 상한(max_tokens): None`, [준비] `모델 이름: gpt-5.4-mini`, [3절] 메시지 2개, [4절] `응답 객체 종류: AIMessage`, [5절] `입력 토큰 수: 36`·`출력 토큰 수: 41`·`끝난 이유: stop` | 실선 요청·점선 응답, 메모 노랑(요청 전 메모는 만든 직후, 사용량 메모는 응답 뒤) |
| 01-3 | 5 실행 예제 · 출력 상한을 줄이면 | Mermaid flowchart TB(칸 두 개, 칸 안 LR) | 출력 상한(`max_tokens`)은 Ch 5 04절 출력 몫(`max_new_tokens`)과 같은 뜻의 값이고, 모자라면 오류 없이 답이 끊깁니다. | [2절] `None`, [5절] `출력 토큰 수: 41`·`끝난 이유: stop`, [7절] `출력 상한(max_tokens): 12`·`출력 토큰 수: 12`·`끝난 이유: length` | 설정 tool 초록, 실행한 모델 model 보라, 출력으로 확인한 값 measure 노랑(끊긴 답도 노랑, Ch 5 04-4 선례) |
| 01-4 | 6 일부러 실패해 보기 · 노트북 뒤 | Mermaid flowchart TB(Before/After 두 칸, 칸 안 LR) | 질문이 `None`이면 요청 전에 `ValidationError`가 났고, 기본값을 준 After는 `AIMessage`를 받았습니다. | [8절] `꺼낸 질문: None`·`오류 종류: ValidationError`·`2 validation errors for HumanMessage`, [9절] `꺼낸 질문: AIMessage라고만 답하세요.`·`응답 객체 종류: AIMessage`·assert 통과 | 꺼낸 질문 tool 초록, 튜플을 메시지 객체로 바꾸는 단계 flow 파랑, 실행한 모델 model 보라, Before 결함 결과 fail 빨강, After 확인 결과 measure 노랑 |

색 규칙(Part 1 선례 이어받음): 넣은 문장·설정은 초록, 실행한 코드·라이브러리 단계는 파랑, 실행한 서비스 모델은 보라, 출력으로 확인한 값은 노랑, 실행하지 않은 단계는 회색입니다. 같은 요소(`gpt-5.4-mini`)는 01-3·01-4 모두 보라입니다.
빨강은 01-4 Before의 `ValidationError` 하나입니다. 노트북은 `try/except ValidationError`로 받아 출력했지만, `invoke()`가 할 일(요청 보내기)로 보면 받지 않을 때 프로그램이 멈추는 실패라 Ch 4 05-3 선례대로 「Before 결함 결과」로 칠했습니다. 01-3의 끊긴 답은 오류가 아니라 출력으로 확인한 결과라 노랑입니다.
01-1은 처음 LR·점선 제품 연결로 그렸을 때 viewBox 폭 1230으로 868을 넘어, 칸 제목에 제품 이름을 넣고 세로 배치로 바꿨습니다(viewBox 약 361×856).
