# Ch21 실행 검증

- 실행일: 2026-09-11
- Python 3.12, langchain 1.4.0, langchain-openai 1.6.0, langgraph 1.2.11
- 실제 모델: gpt-5.4-mini, 실제 임베딩: text-embedding-3-small

## 실제 결과

- 01절: CompiledStateGraph의 Mermaid PNG 8,388바이트와 PNG 서명을 확인했습니다. 메시지는 Human→AI 도구 호출→Tool→AI 답 순서였고 입력 379·출력 47토큰, 추정 0.000496달러였습니다.
- 02절: ToolStrategy는 메시지 3개·AIMessage 1개, ProviderStrategy는 메시지 2개·AIMessage 1개였습니다. 두 결과 모두 R-14와 14일을 검증했습니다.
- 03절: `request_tag=lesson-03`은 상태에 남고 `student-7:read-only`는 도구가 context에서 읽었습니다. 최종 상태에 context 키는 없었습니다.
- 04절: 설치된 `create_agent` 서명에서 6개 핵심 인자를 확인하고 v1 최소 실행을 완료했습니다.
- 05절: 예약 질문은 3일을 답했고 자료에 없는 주차 질문은 검색어를 바꾸어 재검색한 뒤 규정이 없다고 답했습니다.
- 06절: Ch14 C01·C05·C07을 두 경로로 실행했습니다. Agent는 3/3, 고정 RAG는 2/3 supported였습니다. 원문 답·검색 ID·trace·모든 AIMessage 사용량·모델/도구 호출 수·전체 지연을 `rag-comparison.json`에 저장했습니다.

## 자동·화면 검증

- 공통 검증기: 6절, 38개 코드 셀, 최대 15줄로 통과했습니다.
- readiness: 주석 누락 0, 타입 힌트 누락 0, 일반 주석 0, 모든 노트북 assert 포함입니다.
- 화면: 1280px·390px의 7개 페이지에서 작은 글자, 대비, 잘림, 화면 밖 요소, SVG 경계, 가로 스크롤, 깨진 이미지, 복사 오류가 모두 0입니다.
- 도식: SVG·Excalidraw 6쌍을 동일 명세에서 생성했습니다.

## 해석 제한과 확인 필요 항목

세 질문의 한 차례 실행이므로 일반적인 성능 우열을 정하지 않습니다. 고정 RAG의 C01 실패는 검색된 두 문서 중 전자책 정보를 함께 답한 사례입니다. 별도 한국어 감사 3단과 독립 기술 검토는 후속 세션에서 수행합니다. Excalidraw MCP가 없어 기존 생성기를 사용했습니다.
