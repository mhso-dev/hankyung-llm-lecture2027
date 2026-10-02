# Ch21 공식 문서 조사

> **개선 전 판(2026-09-11) 기록입니다.** 품질 개선(2026-09-25) 뒤의 설치판 소스·공식 문서 확인은 `upgrade/chapter-lead-notes.md` §5와 절별 `upgrade/NN-diagnosis.md`, 챕터 요약 `upgrade/chapter-summary.md` §11에 있습니다. 아래 내용(예: `draw_mermaid_png()`, 옛 예제)은 지금 교재와 다를 수 있습니다.

- 확인일: 2026-09-11
- 기준: Python 3.12, langchain 1.4.0, langchain-openai 1.6.0, langgraph 1.2.11

## 확인한 내용

- `create_agent(model, tools, system_prompt, ...)`는 `CompiledStateGraph`를 반환합니다. 설치된 API 서명과 실제 반환형으로 확인했습니다.
- 구조화 출력은 `ToolStrategy`, `ProviderStrategy`, 스키마 직접 전달을 지원하며 결과를 `structured_response`에 저장합니다.
- 이번 실행에서 두 전략 모두 AI 모델 응답은 한 번이었습니다. ToolStrategy는 전체 메시지 3개, ProviderStrategy는 2개였습니다. “추가 모델 호출 없음”을 “추가 메시지 없음”으로 확대하지 않았습니다.
- 사용자 상태는 `AgentState`를 확장한 TypedDict를 `state_schema`로 전달합니다. 실행별 의존 정보는 `context_schema`로 선언하고 `invoke(..., context=...)`에서 제공합니다.
- v1은 `langgraph.prebuilt.create_react_agent` 대신 `langchain.agents.create_agent`를 사용하며 정적 `prompt`는 `system_prompt`에 대응합니다.

## 출처

- https://docs.langchain.com/oss/python/langchain/agents
- https://docs.langchain.com/oss/python/langchain/structured-output
- https://docs.langchain.com/oss/python/migrate/langchain-v1
- https://reference.langchain.com/python/langchain/agents/

## 확인 필요 항목

- 모델 단가와 프로필은 바뀔 수 있습니다. 비용은 실행 시점 공개 단가를 적용한 추정치입니다.
- Excalidraw MCP는 이 세션에 없었습니다. 기존 `_figure.py`로 같은 명세에서 SVG와 Excalidraw JSON을 생성했습니다.
