# Ch22 공식 문서 조사

조사일은 2026-09-11입니다. 실행 환경은 LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11, Python 3.12로 고정했습니다. 세 패키지의 배포 메타데이터에서 MIT 라이선스를 확인했습니다.

## 훅과 실행 순서

LangChain 1.4.0의 공식 커스텀 미들웨어 문서는 노드형 훅 네 개와 감싸기형 훅 두 개를 제공합니다.

| 훅 | 실행 범위 | 이 챕터의 확인 방법 |
| --- | --- | --- |
| `before_agent` | 에이전트 실행 전 한 번 | 01절 trace의 첫 이벤트 |
| `before_model` | 각 모델 호출 전 | 도구 전후 모델 호출에서 두 번 |
| `wrap_model_call` | 각 모델 호출을 감쌈 | handler 전후 trace |
| `wrap_tool_call` | 각 도구 호출을 감쌈 | `lookup_hours` 전후 trace |
| `after_model` | 각 모델 응답 뒤 | 도구 전후 모델 응답에서 두 번 |
| `after_agent` | 정상 에이전트 종료 뒤 한 번 | 01절 trace의 마지막 이벤트 |

커리큘럼의 “모델 호출 전후, 도구 호출 전후, 에러, 종료”는 학습 흐름을 여섯 지점으로 설명한 문구입니다. 설치된 Python API에는 `on_error`라는 독립 훅이 없습니다. 모델 오류는 `wrap_model_call`, 도구 오류는 `wrap_tool_call`에서 handler 예외로 처리합니다. 종료는 `after_agent` 또는 `jump_to="end"`로 다룹니다. 본문은 존재하지 않는 독립 오류 훅을 만들지 않고 공식 여섯 훅 이름을 기준으로 설명합니다.

여러 미들웨어를 넣으면 `before_*`는 목록 순서, `after_*`는 역순으로 실행됩니다. `wrap_*`는 첫 미들웨어가 가장 바깥쪽인 중첩 호출을 만듭니다. 07절은 A·B·C의 18개 trace를 정확히 비교합니다.

## 내장 미들웨어와 Ch16 차이

Ch16 원본 `labs/part4/ch16-guardrails/guardrails.py`의 SHA-256은 `d48a5869fad27e7969f0db362d372e658263745939f8ce8708afafc65dd504f5`입니다.

- Ch16 `mask_pii`는 이메일·전화번호·주민등록번호·카드 네 정규식을 순서대로 적용하고 `<TYPE_MASKED>`로 완전 치환하며 유형별 개수를 반환합니다. `PIIMiddleware("email", strategy="mask")`는 한 인스턴스에서 이메일 한 유형을 처리하고 기본 마스킹은 일부 문자를 남깁니다. 02절은 네 유형의 동일 가상 입력으로 Ch16 결과를 먼저 검사한 뒤 내장 이메일 처리 범위를 따로 관찰합니다.
- Ch16 `summarize_history`는 호출자가 요약 함수를 직접 넘기고 system 메시지와 최근 대화를 조립합니다. `SummarizationMiddleware`는 `before_model`에서 `trigger`와 `keep`을 검사합니다. 03절은 결정적 모델로 훅 동작을 검사하고 실제 GPT-5.4 mini 호출로 권수·기간·연장 조건·출처를 포함한 요약문을 별도 생성합니다.
- Ch16 `CallBudget`은 호출 수와 예상비용을 함께 예약합니다. `ModelCallLimitMiddleware`는 run/thread 호출 수를 제한하지만 프로젝트 가격표에 따른 비용 상한은 계산하지 않습니다. 04절은 실제 두 번째 모델 호출 차단을 관찰하고 05절에서 비용 예약을 커스텀 미들웨어로 옮깁니다.
- Ch16 `retry_with_fallback`은 `TimeoutError` 재시도와 폴백 함수를 한 함수에 넣습니다. LangChain은 `ModelRetryMiddleware`와 `ModelFallbackMiddleware`로 두 정책을 분리합니다.

## Compress와 Isolate

`SummarizationMiddleware`는 오래된 메시지를 줄이는 Compress 구현에 해당합니다. Isolate는 단일 공식 미들웨어 이름이 아니라 컨텍스트를 업무별로 나누는 전략입니다. 08절은 `wrap_model_call`에서 `request.override(messages=selected)`를 사용해 현재 모델 요청만 줄입니다. 원래 상태 삭제나 저장소 권한 분리를 제공하지 않으므로 보안 격리로 설명하지 않습니다.

## 공식 자료

- https://docs.langchain.com/oss/python/langchain/middleware/custom — 커스텀 훅·상태 갱신·실행 순서, 확인 2026-09-11, LangChain 1.4.0
- https://docs.langchain.com/oss/python/langchain/middleware/built-in — PII·요약·호출 한도·재시도·폴백, 확인 2026-09-11, LangChain 1.4.0
- https://docs.langchain.com/oss/python/langchain/context-engineering — 모델·도구·생명주기 컨텍스트, 확인 2026-09-11
- https://reference.langchain.com/python/langchain/agents/middleware — 설치 API와 생성자 시그니처, 확인 2026-09-11, LangChain 1.4.0
- https://reference.langchain.com/python/langchain/agents/middleware/types/AgentMiddleware/wrap_model_call — handler 재호출·요청 수정, 확인 2026-09-11
- https://reference.langchain.com/python/langchain/agents/middleware/types/AgentMiddleware/wrap_tool_call — 도구 실행 감싸기·예외 전파, 확인 2026-09-11
- https://developers.openai.com/api/docs/models/gpt-5.4-mini — 실습 모델과 공개 단가, 확인 2026-09-11

