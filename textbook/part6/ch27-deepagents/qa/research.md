# Ch27 공식 문서 조사

> **개선 전 판(2026-09-11)** — 이 조사는 품질 개선 전 판이고, 챕터 마감(2026-09-28)에서 내용은 고치지 않고 이 표시만 더했습니다. 「기본 조립 넷」(지금 교재는 `AnthropicPromptCachingMiddleware`까지 **기본 미들웨어 다섯**)·「opt-in」·「시스템 프롬프트」·「표면」 같은 옛 말이 남아 있습니다. 개선 뒤 교재가 확인한 문서 사실(서브에이전트 문서의 `mode` 값 `"isolated"`·`"fork"`와 deepagents 0.7.13 이상 요구, customization 문서의 「always registered」 캐시 미들웨어, 사람 승인 문서 예의 `version="v2"` 등)과 확인일(2026-09-28)은 각 절 `_src` b10과 `qa/upgrade/NN-diagnosis.md`·`chapter-summary.md` §11에 있습니다.

- 기준 환경은 Python 3.12, `deepagents==0.7.0`, `langchain==1.4.0`, `langchain-openai==1.6.0`입니다.
- 설치된 0.7.0의 `create_deep_agent`는 Filesystem, SubAgent, Summarization, PatchToolCalls 미들웨어를 기본 조립하고, skills·memory·permissions/HITL·async subagents를 선택적으로 조립합니다.
- 0.7.0에서 `TodoListMiddleware`와 `write_todos`는 기본값에서 제거되어 opt-in입니다. `middleware=[TodoListMiddleware()]`로 복원합니다.
- 작성된 기본 시스템 프롬프트는 비어 있으며 도구 스키마와 겹치던 사용 설명도 줄었습니다.
- “입력 토큰 65% 감소”는 PR #5009에서 `gpt-5.5`의 기본 에이전트 `hello` 첫 턴을 비교한 5,395→1,895 토큰입니다. 0.6.12에서 0.7 개발 브랜치까지의 전체 기본 표면 변화가 포함되며 모든 모델·업무의 총 토큰 절감률이 아닙니다.
- 릴리스 시점의 최신 공식 문서에는 0.7 이후 기능도 포함될 수 있어 설치 패키지 소스와 0.7.0 릴리스 노트를 우선 대조했습니다.

## 확인한 공식 자료

- https://docs.langchain.com/oss/python/deepagents/overview — 2026-09-11
- https://docs.langchain.com/oss/python/deepagents/backends — 2026-09-11
- https://docs.langchain.com/oss/python/deepagents/subagents — 2026-09-11
- https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.0 — 2026-09-11
- https://github.com/langchain-ai/deepagents/pull/4859 — 2026-09-11
- https://github.com/langchain-ai/deepagents/pull/5009 — 2026-09-11
- https://developers.openai.com/api/docs/models/gpt-5.4-mini — 입력 100만 토큰당 0.75달러, 출력 100만 토큰당 4.50달러, 2026-09-11
- https://github.com/langchain-ai/deepagents/blob/main/LICENSE — MIT 라이선스, 2026-09-11

## 확인 필요 항목

- 공식 문서가 0.7.0 이후 인터페이스를 설명하는 부분은 향후 기준 버전 갱신 때 다시 대조해야 합니다.
- OpenAI 모델 가격은 발행 직전 최신 공식 가격표로 다시 확인해야 합니다. 본문은 절당 1달러 미만 목표와 실제 사용량 기록 방법을 설명합니다.
