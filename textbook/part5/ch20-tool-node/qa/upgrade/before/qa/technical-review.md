# Ch20 기술 검토

## 범위와 경계

- `create_agent`와 `create_react_agent`를 사용하지 않고 `StateGraph`, `ToolNode`, `tools_condition`을 직접 조립했습니다.
- Ch13의 `MessagesState`·리듀서·조건부 엣지, Ch17의 정지 조건과 자율성 비용, Ch19의 `bind_tools`를 연결했습니다.
- Ch18에서 모델 기반 선택을 일부 경험했다는 전제를 유지하고, Ch20은 조립된 ToolNode 반복을 처음 완성하는 장으로 설명했습니다.
- 로컬 읽기 전용 규정 딕셔너리를 사용해 미완성인 Ch19 파일에 의존하지 않습니다.

## 코드와 주장 대응

- 01절: 실제 `AIMessage.tool_calls` → `ToolMessage` → 최종 `AIMessage`를 출력합니다.
- 02절: 같은 `call_bad_1`에서 `handle_tool_errors=False`의 예외와 사용자 정의 처리 함수의 `ToolMessage`를 비교합니다.
- 03절: 결정적 비종료 로컬 그래프에서 `GraphRecursionError`를 재현하고 상태 기반 `END` 분기로 수정합니다. 이 그래프를 실제 모델 판단으로 표현하지 않습니다.
- 04절: 같은 세 질문·자료·gpt-5.4-mini·반복 2회 조건에서 fixed와 agent의 전체 trace, 토큰, 비용, 지연, 출력 변동을 기록합니다.

## 남은 독립 검토

- 한국어 감사 3단과 별도 검토자 판정은 부모 작업에서 수행합니다.
