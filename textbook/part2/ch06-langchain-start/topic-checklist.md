# Ch 6 주제 점검표

| 커리큘럼 항목 | 절 | 실행 근거 |
| --- | --- | --- |
| prompt ⊂ context ⊂ harness ⊂ loop | 01 | 네 중첩 영역 도식과 설명 |
| LangGraph 런타임 / LangChain 프레임워크 / DeepAgents 하네스 | 01 | 구현 없이 지도에 위치만 배치 |
| `init_chat_model`과 첫 호출 | 01 | OpenAI 실제 `invoke`, `AIMessage` |
| provider 전환과 메시지 구조 | 02 | 세 provider 조건부 분기, 한 제공자 실행·두 제공자 건너뜀 |
| `content_blocks` | 02, 04 | 응답과 청크의 실제 블록 관찰 |
| Pydantic 구조화 출력과 검증 실패 처리 | 03 | 실제 구조화 호출·충돌 입력 미관찰 기록·결정적 ValidationError |
| 스트리밍 | 04 | 실제 `stream`, 청크 결합과 타입 비교 |
| 재시도·폴백·타임아웃 | 05 | 제한 설정, `with_retry`, `with_fallbacks` 실행 |
| API 키와 `.env` | 모든 절 | 상위 경로 검색, 존재 여부만 확인 |
| 토큰 계측과 비용 감각 | 06 | 실제 usage·지연·공식 단가 비용 계산 |
| 같은 작업 세 provider 비교 | 02, 06 | 완전한 코드 분기. 키 부재 제공자는 건너뜀 |

`create_agent`, 도구 선택, 반복 실행 에이전트, LangGraph 그래프는 사용하지 않았습니다.
