# Ch26 공식 문서 조사

- 확인일: 2026-09-11
- 기준: LangChain 1.4.0, LangGraph 1.2.11, `gpt-5.4-mini`
- Subagents 문서는 중앙 에이전트가 전문 에이전트를 도구로 호출하고 사용자 문맥을 소유한다고 설명합니다.
- Handoffs 문서는 `active_agent` 또는 `current_step` 상태 변경으로 다음 동작을 전환한다고 설명합니다.
- Router 문서는 단일 경로에 `Command`, 병렬 fan-out에 `Send`를 안내합니다.
- `langgraph-supervisor-py`는 대부분의 새 사용 사례에서 도구를 통한 직접 구현을 권고합니다. `langgraph-swarm-py`에는 같은 전면 권고 문구가 확인되지 않았습니다.
- GPT-5.4 mini 공식 가격은 2026-09-11 확인 기준 100만 토큰당 일반 입력 0.75달러, 캐시 입력 0.075달러, 출력 4.50달러입니다.

## 출처

- https://docs.langchain.com/oss/python/langchain/multi-agent/subagents
- https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs
- https://docs.langchain.com/oss/python/langchain/multi-agent/router
- https://github.com/langchain-ai/langgraph-supervisor-py
- https://github.com/langchain-ai/langgraph-swarm-py
- https://developers.openai.com/api/docs/models/gpt-5.4-mini
