# Ch27 실행 검증

- 실행일: 2026-09-11
- Python: 3.12.13
- 패키지: DeepAgents 0.7.0, LangChain 1.4.0, langchain-openai 1.6.0
- 모델: gpt-5.4-mini, 07절 실제 OpenAI API 호출

## 실제 결과

- 공통 실행기에서 8개 노트북, 36개 코드 셀이 모두 새 커널 실행을 통과했습니다. 가장 긴 코드 셀은 18줄입니다.
- 01절은 설치된 생성 함수에서 7개 기능에 연결된 미들웨어 이름을 확인했습니다.
- 02절은 `create_deep_agent`의 주요 인자와 생성한 그래프의 노드를 확인했습니다.
- 03절은 기본 생성 소스에 TodoListMiddleware가 없고 opt-in 객체를 만들 수 있음을 확인했습니다. 65%는 릴리스 PR의 5,395→1,895 첫 턴 비교로 표시했습니다.
- 04절은 `workspace/research/source-a.md`를 실제로 쓰고 다시 읽었습니다.
- 07절은 실제 모델이 `source-reviewer`에 검증을 위임하고 `workspace/research/final.md`를 저장했습니다. 파일에는 `Verified claims`, `Scope limits`, `Source ids`가 모두 있습니다.
- 07절 부모의 마지막 응답 `usage_metadata`는 입력 2,379·출력 34·합계 2,413토큰입니다. 이 값은 서브에이전트 호출 전체 사용량을 합산한 값이 아니므로 전체 비용으로 표시하지 않습니다.

## 정적·빌드 검증

- `_build.py`가 index와 8개 완성 HTML을 생성했습니다.
- `verify.py --chapter`가 `PASS 8 sections / 36 code cells (max 19 lines)`를 반환했습니다.
- 도식 생성기가 8개의 SVG와 Excalidraw 원본, 캡션을 생성했습니다.
- 각 절의 본문 텍스트는 2,539~2,717자이며 강의 1시간당 약 2,500자 기준을 충족합니다.

## 확인 필요 항목

- Playwright 화면 검사는 1280px와 390px에서 8개 절 모두 본문 크기·대비·잘림·본문 밖 요소·SVG 경계·가로 넘침·이미지·복사·실패 블록 검사를 통과했습니다.

## 최종 실행 해시

| 절 | 코드 SHA-256 | 출력 SHA-256 |
| --- | --- | --- |
| 01 | `5452a8d5efa21915ae619133a8accf71ac4cb3f4e46a3363dd3f1c2be9e4ca55` | `c244b5634556190843f06c6516a27a1690d31443045f3aad277e53b48eb75307` |
| 02 | `f302f7a3c451dafc2e562c48e5baa5c8930f8fa89798210e41895f608aaaf54c` | `ba154aab80936548f11f1c8a1227a726713412208750b82f3c3c3f783c9b8c84` |
| 03 | `7b6c4edf3a6b8cd6d4ccf673f6f3bb25a3862dc0d168370d56cf4da095e5edaa` | `e848899d74fc37087d31fa41b2f1b0f64829db6b6c2ce48dedd1d84d41ee356d` |
| 04 | `b3d0938d2cb8deca6d0a6d679968c785155b4c0ff7a1c66af96f4befcf61ec5b` | `010f5ccd27fc3cb772fe5855c08fb39530c2a635fe79b91aba08f0babe293b7a` |
| 05 | `96cab476f5ca2c55be8fcfd80ddaf0d8bbb98ec3cf33efb285df01625abcb385` | `6b53e2045b5872e24942b77cd2172ac53c9a72a930f0c1da11bb729d9175e2ca` |
| 06 | `02000e813991e7fc6236dffced710e96713a0dc464880a28e8a7eb31da4c971d` | `99841edc51a30ae1d67be41abac2e2871816f7ae068f1b2a826521021ea5664f` |
| 07 | `5e0e2b7aefaa27b7edba16c2eb5a70b6fd24053ac1d5865d3df97cc1a537dd95` | `aa4ec6cefc4d4b47fff1a0aa818f7eb307c53b29789845011e5f646597d8564a` |
| 08 | `18dd64177cdd924695dfe03d5a6c6bd3561d72dfdbd680638c96020d33e2fe5f` | `d9ec427e83f0d27a3e7d21b00ff18ffcda5aada90adceebcfa47114cb4bb3e19` |
- 독립 한국어 감사 3단은 후속 검토 세션에서 수행합니다.
