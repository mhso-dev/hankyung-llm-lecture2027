# Ch20 공식 문서 조사

- LangChain 1.4.0 / langchain-openai 1.6.0 / LangGraph 1.2.11을 실행 환경에 고정했습니다.
- `ToolNode`는 도구 호출을 실행하고 딕셔너리 상태 입력에 `ToolMessage` 목록을 반환합니다. `handle_tool_errors`는 예외 유형 또는 오류 처리 함수로 범위를 정할 수 있습니다.
- `tools_condition`은 마지막 AI 메시지의 `tool_calls`가 있으면 `tools`, 없으면 `END`로 분기합니다.
- `recursion_limit`은 `invoke` 설정 딕셔너리의 독립 키이며 한도를 넘기면 `GraphRecursionError`가 발생합니다.
- GPT-5.4 mini 공개 단가는 입력 100만 토큰당 0.75달러, 출력 100만 토큰당 4.50달러입니다. 모든 API 사용 절은 실제 `usage_metadata`로 비용을 계산하고 절당 1달러 미만을 검사합니다.

## 확인한 공식 자료

- https://docs.langchain.com/oss/python/langchain/tools — 2026-09-10
- https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode — 2026-09-10
- https://docs.langchain.com/oss/python/langgraph/graph-api — 2026-09-10
- https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT — 2026-09-10
- https://developers.openai.com/api/docs/models/gpt-5.4-mini — 2026-09-10
