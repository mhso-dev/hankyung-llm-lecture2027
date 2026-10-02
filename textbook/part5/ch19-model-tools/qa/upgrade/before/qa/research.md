# Ch19 공식 문서 조사

- 조사일: 2026-09-10
- 기준 환경: Python 3.12, LangChain 1.4.0, langchain-openai 1.6.0, Pydantic 2.12.5
- 모델: `gpt-5.4-mini`

LangChain 도구 문서는 `@tool`이 함수의 docstring을 기본 설명으로 사용하며, 문자열과 구조화된 객체를 반환할 수 있다고 설명합니다. 모델 문서는 `bind_tools()`로 도구를 제공한 뒤 응답의 `tool_calls`를 읽고, 프로그램이 도구를 실행해 결과를 다시 전달하는 흐름을 제시합니다. 각 `ToolMessage.tool_call_id`는 원래 호출의 ID와 일치해야 합니다. 여러 독립 호출을 한 응답에 요청할 수 있고 제공자에 따라 `parallel_tool_calls=False`로 제한할 수 있습니다.

Pydantic 모델은 타입 주석과 `Field` 제약을 검증하고 JSON Schema를 생성합니다. Ch19에서는 이 스키마를 모델 입력 설명과 실행 전 검증이라는 두 역할로 설명합니다.

## 출처

- https://docs.langchain.com/oss/python/langchain/tools
- https://docs.langchain.com/oss/python/langchain/models
- https://docs.langchain.com/oss/python/langchain/messages
- https://docs.pydantic.dev/latest/concepts/models/
- https://platform.openai.com/docs/guides/function-calling

## 범위

Ch19는 단일 모델 요청과 도구 객체를 다룹니다. `ToolNode`, 조건부 엣지, 자동 반복 루프, `create_agent`는 Ch20 이후 범위로 남깁니다.
