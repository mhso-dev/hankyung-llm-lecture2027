# Ch30 공식 문서 조사

> **개선 전 판(2026-09-11)의 기록입니다.** 품질 개선(2026-09-29) 뒤 교재가 확인한 문서와 설치판 소스 행은 각 절 본문 「참고 자료」와 `qa/upgrade/NN-diagnosis.md`, 챕터 요약 `qa/upgrade/chapter-summary.md` §16에 있습니다. 이 파일의 내용은 고치지 않았습니다.

- 확인일: 2026-09-11
- 기준: Python 3.12.13, FastAPI 0.135.0, LangChain 1.4.0, LangGraph 1.2.11

## 확인한 내용

- FastAPI 의존성은 경로 연산이 필요한 객체와 공통 검사를 선언하고 OpenAPI 스키마에도 반영합니다.
- FastAPI 0.135.0은 `fastapi.sse.EventSourceResponse`와 `ServerSentEvent`를 제공하며 POST 라우트에서도 SSE를 반환할 수 있습니다.
- SSE의 `event`, `id`, `data`, `retry` 필드를 지정할 수 있고 data 값은 JSON으로 직렬화됩니다.
- FastAPI 네이티브 SSE는 keep-alive ping, `Cache-Control: no-cache`, `X-Accel-Buffering: no`를 처리합니다.
- 브라우저 EventSource는 POST 본문과 임의 Authorization 헤더를 설정하지 못하므로 이 장은 fetch 응답 스트림을 직접 해석합니다.
- CORS에서 credentials를 허용할 때 origins, methods, headers를 와일드카드로 두지 않고 명시해야 합니다.
- FastAPI의 `.openapi()`와 `/openapi.json`은 기본 OpenAPI 3.1 문서를 제공합니다.
- LangChain `create_agent`는 LangGraph 기반 실행 객체를 만들고 `ainvoke`와 `astream`으로 실행할 수 있습니다.

## 실제 버전 확인과 보정

- LangChain 1.4.0은 LangGraph 1.2.11 이상을 요구하므로 커리큘럼의 `LangGraph 1.2` 범위 안에서 1.2.11로 고정했습니다.
- OpenAPI Generator 7.25.0은 FastAPI 0.135가 SSE 스키마에 기록하는 `itemSchema`를 아직 검증하지 못했습니다. `--skip-validate-spec`로 경고를 보존한 채 TypeScript fetch SDK를 생성했고, 생성물은 TypeScript 컴파일을 통과했습니다.
- 결정적 LangGraph는 HTTP와 SSE 계약 검증용입니다. 실제 모델 통합은 09절에서 OpenAI 모델, 도구 호출, ToolMessage, 모델 token SSE를 별도로 실행했습니다.

## 출처

- https://fastapi.tiangolo.com/tutorial/dependencies/
- https://fastapi.tiangolo.com/tutorial/server-sent-events/
- https://fastapi.tiangolo.com/reference/sse/
- https://fastapi.tiangolo.com/tutorial/cors/
- https://fastapi.tiangolo.com/tutorial/security/first-steps/
- https://fastapi.tiangolo.com/how-to/extending-openapi/
- https://docs.langchain.com/oss/python/langchain/agents
- https://docs.langchain.com/oss/python/langgraph/streaming
- https://openapi-generator.tech/docs/generators/typescript-fetch/

## 확인 필요 항목

- 실제 클라우드 프록시의 SSE 버퍼링과 유휴 timeout은 로컬 환경에서 확인하지 않았습니다.
- Excalidraw MCP는 이 세션에서 호출할 수 없어 프로젝트의 기존 생성기로 SVG와 Excalidraw JSON을 함께 만들었습니다.
