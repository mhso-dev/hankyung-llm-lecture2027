# Ch26 검증 기록

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11
- 새 커널 실행: 4개 노트북, 코드 셀 23개 모두 성공
- 정적 검증: 4개 절, 코드 셀 최대 23줄, 설치 셀·한국어 목적 주석·함수 타입 힌트·assert 확인
- 실제 API: Subagent 도구, Handoff 상태 전환, Router 분류와 병렬 실행, 세 구조 비교 실행
- 구조 비교: create_agent가 `policy_tool` 선택, Handoff 조건부 엣지가 `shipping→refund→done` 선택, Router 구조화 출력이 `policy`와 `shipping` 선택
- 비용: 2026-09-11 GPT-5.4 mini 공식 일반 입력 0.75달러·캐시 입력 0.075달러·출력 4.50달러/100만 토큰을 적용하고 `cache_read`를 분리
- 빌드: index와 4개 절 HTML 생성 성공
- 화면: 1280px와 390px에서 5개 페이지 모두 글자 크기·대비·잘림·가로 넘침·SVG 경계·복사·다운로드 검사 통과
- 비밀값: 키 값 출력 없음, `.env` 공개 목록 제외
- 언어 검토: 후속 독립 검토 예정

## 확인 필요 항목

- 한 질문의 호출 수와 비용은 구조 이해를 위한 실행 결과이며 운영 평균을 나타내지 않습니다.
- `langgraph-supervisor` 직접 구현 권고를 `langgraph-swarm` 전체의 폐기 권고로 확대하지 않았습니다.
