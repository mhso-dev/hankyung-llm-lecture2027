# Ch26 공식 문서 조사

> **개선 전 판(2026-09-11)** — 이 조사는 품질 개선 전 판이고, 마감(2026-09-28)에서 내용은 고치지 않고 이 표시만 더했습니다. 「사용자 문맥을 소유」·「병렬 fan-out」 같은 옛 말이 남아 있고, 개선 뒤 교재가 확인한 문서 사실(Handoffs의 「no parallel tool calls」 전제·「you must include both」, multi-agent 개요의 요청 수 표, Subagents의 single dispatch tool 등)과 날짜(2026-09-28)는 각 절 `_src` b10과 `qa/upgrade/NN-diagnosis.md`·`chapter-summary.md` §11에 있습니다.

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
