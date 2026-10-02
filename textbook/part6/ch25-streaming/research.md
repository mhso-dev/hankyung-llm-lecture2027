# 공식 문서 조사 기록

> **개선 전 판(2026-09-11)** — 공용 옛 생성기(`textbook/part6/_generate_ch25_ch26.py`) 시절 Ch 25·26 조사를 함께 적은 기록이라 Ch 26 문서(Subagents·Handoffs·Router) 조사가 섞여 있습니다. 마감(2026-09-25)에서 내용은 고치지 않고 이 표시만 더했습니다. Ch 25 쪽 지금 기록은 `qa/upgrade/chapter-lead-notes.md`·각 절 `qa/upgrade/NN-diagnosis.md`·`qa/upgrade/chapter-summary.md`이고, 요금(0.75·0.075·4.50달러)은 03절이 2026-09-17 요금표로 다시 적었습니다.

- 확인일: 2026-09-11
- 기준 버전: Python 3.12, LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11
- 공식 문서의 StreamMode는 values, updates, messages, custom, checkpoints, tasks, debug의 7개입니다.
- streaming 문서는 단일 모드의 기본 v1 출력, 복수 모드의 `(mode, data)` 출력, 최신 v2의 `type/ns/data` 통일 형식을 구분합니다. 이 교재 코드는 기준 버전의 기본 v1 형식을 사용합니다.
- Subagents 공식 문서는 중앙 에이전트가 전문 에이전트를 도구로 호출하고 사용자 문맥을 소유한다고 설명합니다.
- Handoffs 공식 문서는 `active_agent` 또는 `current_step` 같은 상태 변경을 핵심으로 설명합니다.
- Router 공식 문서는 단일 경로에 Command, 병렬 fan-out에 Send를 안내합니다.
- `langgraph-supervisor-py` 저장소는 대부분의 사용 사례에서 supervisor 패턴을 도구로 직접 구현할 것을 권고합니다. `langgraph-swarm-py` 저장소에는 동일한 전면 권고 문구가 확인되지 않아 두 라이브러리를 함께 폐기 대상으로 서술하지 않습니다.
- GPT-5.4 mini 공식 가격은 2026-09-11 확인 기준 100만 토큰당 일반 입력 0.75달러, 캐시 입력 0.075달러, 출력 4.50달러입니다. 실습은 usage_metadata의 cache_read를 일반 입력에서 분리합니다.

## 출처

- https://docs.langchain.com/oss/python/langgraph/streaming
- https://reference.langchain.com/python/langgraph/types/StreamMode
- https://docs.langchain.com/oss/python/langchain/multi-agent/subagents
- https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs
- https://docs.langchain.com/oss/python/langchain/multi-agent/router
- https://github.com/langchain-ai/langgraph-supervisor-py
- https://github.com/langchain-ai/langgraph-swarm-py
- https://developers.openai.com/api/docs/models/gpt-5.4-mini
