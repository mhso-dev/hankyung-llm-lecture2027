# Ch28 MCP 기술 근거 검토

검토일: 2026-09-11 · 범위: Ch28 5절, Ch28 실습 README·노트북 마크다운, Part 6 공통 안내

## 판정

본문·실습·노트북 출력의 기술 주장은 2025-11-25 MCP 사양, FastMCP 4.0.3 실행 기록, LangChain 1.4.0 공식 MCP 문서와 대조했습니다. 본문 기술 교정과 생성 도식의 접근성 캡션 동기화를 반영했습니다.

## 공식 근거

- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) — JSON-RPC 2.0, 서버의 도구·리소스·프롬프트, 사용자 동의와 도구 안전 원칙을 정합니다.
- [Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle) — `initialize` 요청·응답 뒤 `notifications/initialized`로 정상 동작 단계에 들어가며, 협상한 capability만 사용하도록 정합니다.
- [Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) — stdio는 줄바꿈 JSON-RPC와 하위 프로세스를 사용하고, Streamable HTTP는 POST·GET MCP 엔드포인트를 사용합니다. Streamable HTTP 서버는 Origin을 검증해야 하며, 로컬에서는 127.0.0.1 바인딩과 적절한 인증을 권고합니다.
- [Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) — HTTP 인증은 선택 사항이며 지원할 때 OAuth 기반 흐름을 정합니다. stdio에는 이 HTTP 인증 흐름을 적용하지 않고 환경에서 자격 정보를 가져오도록 구분합니다.
- [LangChain MCP](https://docs.langchain.com/oss/python/langchain/mcp) — `langchain[mcp]>=1.4.0`의 beta `MCPAdapter`, `Path`의 stdio 하위 프로세스, `http(s)` URL의 Streamable HTTP 연결을 확인했습니다.
- [FastMCP Server](https://gofastmcp.com/v2/servers/server) — 도구·리소스·프롬프트를 서버 구성 요소로 등록하는 FastMCP 구조를 확인했습니다.

## 기술 교정

`03-stdio와-원격-전송-권한-경계`의 “TLS, Origin 검사, 인증 토큰, 사용자별 인가가 필요합니다”를 의무 수준에 맞게 고쳤습니다. Origin 검증은 필수로, 127.0.0.1 바인딩과 인증·인가 설계는 공개 서비스 운영의 권고·설계 항목으로 구분했습니다. HTTP OAuth 절차와 stdio 환경 자격 정보의 경계도 분명히 했습니다.

## 실행·수치 대조

- 노트북의 고정 버전은 LangChain 1.4.0, langchain-openai 1.6.0, FastMCP 4.0.3, MCP 2.2.0입니다.
- 01절은 메모리 연결에서 도구·리소스·프롬프트 각각 한 항목을 발견하고 사용했습니다.
- 03절은 제한된 환경 변수로 stdio 서버를 실제 호출했습니다. 원격 Streamable HTTP는 실행하지 않은 비교 범위입니다.
- 04절의 `MCPAdapter(Path)`·stdio, `MCPAdapter(http(s) URL)`·Streamable HTTP 설명은 현재 공식 문서와 일치합니다.
- 05절의 158·158·316 입력 토큰과 비용 추정은 노트북의 실제 출력에 있으며, 도구 정의의 개수·이름·설명·스키마가 함께 바뀌므로 MCP만의 인과로 단정하지 않는 본문 해석이 적절합니다.

## 도식 동기화

`figures/_gen_figures.py`의 03절 캡션을 교정하고 SVG·Excalidraw를 재생성했습니다. `03-흐름.caption.md`, SVG의 title, aria-label이 모두 같은 문장인지 확인했고, 재생성 뒤 `visual.cjs` PC·모바일 12건도 모두 통과했습니다.

후속 시각 감사에서 역할 색도 바로잡았습니다. 파란색은 학생 코드·클라이언트 실행, 보라색은 모델 판단, 초록색은 도구·데이터, 노란색은 측정값, 빨간색은 실패·권한 경계를 뜻합니다. 따라서 모델 판단이 없는 `prompts/list`, `BaseTool`, MCP 클라이언트는 보라색에서 적절한 역할색으로 옮겼고, 단순 읽기 결과도 측정값 색으로 표시하지 않았습니다. 본문의 도식 읽기 설명도 같은 범례로 고쳤습니다. 최종 생성기 SHA-256은 `dadf0c2baf1073c61a890fbf3334f64c2a43e6f2b4ea52a303a53a8cdb8261e3`입니다.

## 독립 실행 경로

01~04절의 서버 파일 경로는 노트북 작업 디렉터리에 의존하지 않도록 상위 폴더에서 프로젝트 루트를 찾아 계산하도록 작성자가 보정했습니다. 새 커널 실행은 01~04절에 각각 4·4·5·3 코드 셀로 통과했고, 도구 목록·호출 결과는 그대로였습니다. 학생용 README에서는 배포 묶음에 없는 내부 `textbook/_notebook/execute.py` 명령을 제거하고 `uv sync --locked`와 새 Python 3.12 커널의 순차 실행만 안내합니다.

## 버전 주의

커리큘럼의 `MCP 2026-07`은 미래 기준입니다. 2026-09-11 확인 시 공식 발행 사양은 2025-11-25였습니다. 개강 전 2026-07 발행 여부와 capability·인증 변경을 다시 확인해야 합니다.
