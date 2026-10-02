# Ch22 독립 기술 검토

- 검토일: 2026-09-11
- 대상: 8개 `_src` 절, 8개 노트북의 코드·저장 출력, `chapter.json`, 그림 캡션, 실습 README와 노트북 Markdown
- 기준: LangChain 1.4.0, LangGraph 1.2.11, Python 3.12

## 판정

수정 후 통과합니다. 여섯 훅의 이름과 경계, PII·요약·호출 한도·재시도·폴백의 역할은 공식 문서 및 실제 노트북 출력과 일치합니다. `Isolate`는 공식 내장 미들웨어 명칭이 아니라 이 교재에서 정의한 요청 범위 선택 전략으로 제한해 설명하고 있어, 접근 통제나 상태 삭제를 한다는 주장도 없습니다.

## 수정

- 모든 절에 복제돼 있던 실행 안내를 각 노트북의 실제 비교로 바꿨습니다. 예를 들어 03절은 6개 메시지가 3개가 되는 관찰, 04절은 재시도 2회·폴백·run limit 1회의 독립 관찰을 가리킵니다.
- 01절의 실제 API 연결 확인과 결정적 검사 모델의 역할을 분리해, 후자가 모델 품질·비용 측정이라는 오해를 막았습니다.
- 도식에서 실제 미들웨어 실행인 `before_agent`, `after_agent`, PII 처리, 재시도, before·after 순서, topic 선택을 파랑으로 고쳤습니다. 노랑은 호출 한도·비용 예약·감사 이벤트처럼 측정·평가에만 남겼습니다.

## 근거

- [LangChain custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom) — `before_agent`, `before_model`, `wrap_model_call`, `wrap_tool_call`, `after_model`, `after_agent`와 합성 순서.
- [LangChain prebuilt middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in) — PII, 요약, 모델 호출 한도, 재시도, 폴백의 설정 범위.
- [Middleware API reference](https://reference.langchain.com/python/langchain/agents/middleware) — 1.4 계열 API 표면.

## 실행 대조

01절 trace는 agent 훅 각 1회, 모델 관련 훅 각 2회, 도구 감싸기 훅 1회입니다. 03절은 입력 6개가 요약문과 최근 2개를 포함한 3개가 됐고 `14일`, `E01 p.3`을 남겼습니다. 04절은 재시도 모델 2회, 보조 모델 폴백, run limit 1의 종료 메시지를 출력했습니다. 08절은 loan 3개만 모델 요청에 전달하고 상태의 5개 메시지는 유지했습니다.

## 남은 한계

결정적 모델로 실행 경계를 검사한 절은 실제 공급자 지연·장애율·모델 품질을 측정하지 않습니다. 실제 모델을 호출한 01·03절의 문장·토큰·예상 비용은 실행 시점에 달라질 수 있습니다.
