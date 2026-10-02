# Ch28 공식 문서 조사

- 조사일: 2026-09-11
- 학습자 수준: 개발 입문~초급
- 실행 기준: Python 3.12.13, LangChain 1.4.0, langchain-openai 1.6.0, FastMCP 4.0.3, MCP Python SDK 2.2.0

## 확인한 내용

MCP 공식 스펙에서 도구는 모델이 호출할 수 있는 기능, 리소스는 URI로 읽는 자료, 프롬프트는 사용자가 명시적으로 선택하는 재사용 메시지 틀로 정의됩니다. 초기화 단계에서 프로토콜 버전과 capability를 교환한 뒤 정상 동작 단계로 이동합니다. stdio는 클라이언트가 로컬 하위 프로세스를 시작하고, Streamable HTTP는 하나의 MCP 엔드포인트에서 HTTP 요청을 처리합니다. HTTP 인증 스펙은 stdio에 적용하지 않습니다.

커리큘럼의 기준 문자열은 `MCP 2026-07`입니다. 2026-09-11 현재 공식 사양 사이트에서 확인할 수 있는 최신 발행판은 `2025-11-25`입니다. 미래 기준을 구현된 것처럼 쓰지 않고 이번 교재와 실행 검증은 2025-11-25 사양 및 설치된 Python 구현을 기준으로 삼았습니다. 개강 전에 2026-07 발행판 존재 여부와 변경 내용을 다시 확인해야 합니다.

FastMCP 4.0.3에서 `@mcp.tool`, `@mcp.resource`, `@mcp.prompt`와 메모리·stdio 연결을 실행했습니다. PyPI 배포판의 라이선스 표현은 Apache-2.0입니다. MCP Python SDK 2.2.0의 프로젝트 메타데이터는 MIT 라이선스입니다. MCP 명세 저장소는 MIT에서 Apache-2.0으로 전환 중이며 문서 기여는 CC-BY-4.0이라고 밝힙니다. LangChain 저장소는 MIT 라이선스입니다. 교재 코드는 공식 예제를 복제하지 않고 교육센터 자료실 도메인으로 다시 작성했습니다.

LangChain 1.4.0 공식 문서는 `from langchain.mcp import MCPAdapter`를 현재 경로로 안내하며 이 네임스페이스가 beta라고 명시합니다. 이전의 `langchain-mcp-adapters` 패키지와 `MultiServerMCPClient` 예시는 마이그레이션 대상입니다. 따라서 커리큘럼의 `langchain.mcp` 경로는 현재 1.4.0에서 틀리지 않았고, 실제 수업 코드는 구체 클래스 `MCPAdapter`를 사용해야 합니다.

## 출처

- MCP Specification 2025-11-25: https://modelcontextprotocol.io/specification/2025-11-25
- MCP tools: https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- MCP resources: https://modelcontextprotocol.io/specification/2025-11-25/server/resources
- MCP prompts: https://modelcontextprotocol.io/specification/2025-11-25/server/prompts
- MCP transports: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- MCP authorization: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
- FastMCP server: https://gofastmcp.com/v2/servers/server
- FastMCP 4.0.3 PyPI: https://pypi.org/project/fastmcp/4.0.3/
- LangChain MCP: https://docs.langchain.com/oss/python/langchain/mcp
- MCP Python SDK project metadata: https://github.com/modelcontextprotocol/python-sdk/blob/main/pyproject.toml
- MCP 명세 저장소 라이선스: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/LICENSE
- LangChain 저장소: https://github.com/langchain-ai/langchain

## 확인 필요 항목

- 개강 전 `MCP 2026-07` 공식 발행판의 존재와 변경된 capability·인증 요구사항을 다시 확인합니다.
- `langchain.mcp`는 1.4.0에서 beta이므로 개강 고정 환경에서 import와 대상 형식을 다시 실행합니다.
