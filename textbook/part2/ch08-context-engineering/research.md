# Ch 8 컨텍스트 엔지니어링 기초 — 조사 노트

확인일: 2026-09-08  
대상: 초보자용 Ch 8 HTML 교재의 근거 자료. 이 노트는 구현 지시서가 아니며, Ch 8에서는 에이전트·LangChain·LangGraph를 사용하지 않고 고정된 파이썬 함수로 입력 컨텍스트만 조정한다.

## Ch 9와의 연결

Ch 9의 첫 절은 Ch 8의 **Select**를 “지금 필요한 것만 골라 넣기”로 정의하고, RAG를 그 선택을 검색으로 자동화한 방식으로 설명한다. 그러므로 Ch 8에서는 사람이 직접 문자열·문서 조각을 고르는 작은 예제를 먼저 보여 준다. 검색, 임베딩, 벡터스토어, 에이전트 판단은 Ch 9 이후의 범위다.

## 핵심 개념

컨텍스트 엔지니어링은 한 번의 프롬프트 문장을 다듬는 일에 그치지 않는다. 매 모델 호출 때 시스템 지시, 사용자 요청, 대화 이력, 도구 결과, 외부 문서 가운데 **목표 달성에 필요한 고신호 토큰의 작은 집합**을 고르고 유지하는 일이다. Anthropic은 컨텍스트를 추론 시 모델에 들어가는 토큰 전체로 정의하며, 프롬프트 밖에서 들어오는 도구·외부 데이터·메시지 이력까지 관리 대상으로 든다.

교재의 최소 규칙은 다음 한 문장으로 충분하다. **컨텍스트 창이 크더라도, 이번 질문에 필요한 근거만 넣고 나머지는 밖에 둡니다.**

## 네 가지 전략의 출처와 안전한 설명

`Write → Select → Compress → Isolate`는 국제 표준이나 모델 API의 공식 분류가 아니다. LangChain 팀이 2025-07-02 블로그에서 여러 에이전트와 논문 사례를 묶어 제시한 실무용 네 범주다. 따라서 본문에서는 “컨텍스트를 다루는 네 가지 전략” 또는 “LangChain 팀이 정리한 네 범주”라고 쓰고, 보편적·완결된 표준이라고 단정하지 않는다.

| 전략 | 이 교재에서의 뜻 | Ch 8 범위에서의 표현 |
|---|---|---|
| Write | 현재 창 밖에 나중에 쓸 정보를 기록한다. | 결정·문서 조각을 파이썬 변수나 파일에 보관합니다. 모든 기록을 매번 모델에 넣지는 않습니다. |
| Select | 이번 질문에 관련 있는 기록만 창으로 가져온다. | 질문 키워드에 맞는 1~2개 문단을 사람이 고릅니다. Ch 9에서 검색이 이 선택을 자동화합니다. |
| Compress | 긴 이력에서 필요한 사실을 남기고 줄인다. | 원문 전체 대신 결정, 수치, 출처를 담은 짧은 요약을 만듭니다. 요약이 원문을 완전히 보존하지는 않으므로 확인이 필요합니다. |
| Isolate | 서로 다른 작업의 컨텍스트를 분리한다. | 이 장에서는 ‘고객 문의’와 ‘코드 리뷰’처럼 서로 다른 자료 묶음을 섞지 않는 것으로만 설명합니다. 하위 에이전트 분리는 Ch 20 이후에 다룹니다. |

LangChain의 정의는 Write를 창 밖 저장, Select를 창 안으로 가져오기, Compress를 과업에 필요한 토큰만 남기기, Isolate를 컨텍스트 분할로 설명한다. Anthropic의 공식 글은 같은 이름의 네 범주를 쓰지는 않지만, JIT(just-in-time) 로딩, 압축, 구조화 메모, 하위 작업 분리를 각각 뒷받침한다.

## 네 가지 실패 양상의 출처와 주의점

`Poisoning`, `Distraction`, `Confusion`, `Clash`도 표준화된 진단 체계가 아니다. LangChain 글이 Drew Breunig의 해설을 인용해 소개한 실무적 명명이다. 교재에서는 진단을 돕는 이름으로만 쓰고, 과학적으로 상호 배타적인 네 원인이라고 가르치지 않는다.

| 이름 | 짧은 정의 | 고정 함수 실습으로 보일 수 있는 사례 |
|---|---|---|
| Context Poisoning | 이전 모델의 틀린 주장이나 환각이 다음 호출의 사실처럼 남는다. | `notes`에 잘못 저장한 휴관일을 다시 프롬프트에 넣어 답이 반복해서 틀립니다. |
| Context Distraction | 너무 긴 컨텍스트가 모델의 주의와 학습된 과업 수행을 압도한다. | 질문과 무관한 긴 회의록을 추가하면 핵심 문장이 묻힐 수 있습니다. |
| Context Confusion | 불필요한 정보가 응답에 영향을 준다. | 같은 기관이 아닌 다른 기관의 안내문을 함께 넣으면 그 정보가 답에 섞일 수 있습니다. |
| Context Clash | 컨텍스트 안의 두 정보가 서로 모순된다. | ‘월요일 휴관’과 ‘화요일 휴관’이라는 서로 다른 버전의 규정을 출처·시점 없이 함께 넣습니다. |

각 실패 양상은 실제 제품의 모든 오답을 설명하지 않는다. 검색 오류, 불충분한 지시, 모델의 지식 한계, 최신성 문제도 별도로 점검해야 한다.

## Context rot를 어떻게 해석할 것인가

Chroma의 2025 기술 보고서는 GPT-4.1, Claude 4, Gemini 2.5, Qwen3 등을 포함한 18개 모델에서 입력이 길어질수록 단순한 과제의 성능도 불균일하게 낮아진다고 보고했다. 의미적 바늘 찾기, 방해 문서, 대화형 QA, 단어 반복처럼 과제를 통제해 **입력 길이의 영향**을 보려 했다. Anthropic도 이를 근거로 토큰 수가 늘면 정확한 회상이 감소하는 현상을 context rot이라 부르며, 컨텍스트를 한정된 자원으로 다룰 것을 권한다.

수업에서 다음처럼 해석한다.

* “컨텍스트 창에 들어간 모든 내용을 모델이 같은 정확도로 활용한다”는 가정은 안전하지 않습니다.
* 이는 고정된 ‘몇 토큰부터 반드시 성능이 떨어진다’는 임계값이 아닙니다. 모델, 과제, 정보의 위치·유사성·방해 문서, 출력 길이에 따라 달라집니다.
* Chroma 보고서는 동료 심사 논문이 아니라 Chroma의 기술 보고서다. 원문은 일반화된 제품 성능 보증이 아니라 긴 입력을 평가할 때 확인할 위험 신호로 사용합니다.
* 대응은 창을 억지로 채우지 않고, 필요한 근거를 선택하고, 오래된 도구 출력은 줄이며, 중요한 결정은 창 밖의 구조화된 기록에 보관하는 것입니다.

## Progressive disclosure 근거

점진적 공개(progressive disclosure)는 처음부터 전체 자료를 넣지 않고, 현재 판단에 필요한 얕은 정보에서 시작해 필요할 때 다음 수준의 자료를 여는 방식이다. Anthropic의 Agent Skills 글은 스킬 이름·설명, `SKILL.md` 본문, 연결 파일을 단계별로 여는 구조를 실제 예로 든다. 별도의 Anthropic 컨텍스트 엔지니어링 글도 파일 경로·저장 질의·웹 링크 같은 가벼운 식별자를 유지하고, 도구로 필요한 데이터를 실행 시점에 불러오는 JIT 접근을 권한다.

Ch 8의 비에이전트 예제에서는 이를 단순한 함수 순서로 보인다.

1. 문서 목록에서는 제목과 식별자만 봅니다.
2. 질문과 맞는 식별자 하나를 고릅니다.
3. 그 문서 본문만 프롬프트에 넣습니다.

이 방식은 더 적은 토큰을 보장하는 만능 해법은 아니다. Anthropic은 탐색이 미리 계산한 검색보다 느릴 수 있고, 적절한 도구와 탐색 지침이 없으면 오히려 컨텍스트를 낭비할 수 있다고 명시한다.

## OpenAI API·비용: 코드 담당 전달 사항

기준 모델은 `gpt-5.4-mini`이며, 별칭 대신 재현성이 필요하면 현재 문서에 기재된 스냅샷 `gpt-5.4-mini-2026-03-17`을 사용할 수 있다. 다만 프로젝트 커리큘럼의 기준 모델 표기와 교재 내 실행 모델 표기를 일치시켜야 한다.

| 항목 | 2026-09-08 확인값 및 수업에서의 의미 |
|---|---|
| 컨텍스트 창 | 400,000 토큰. 한도는 ‘권장 입력량’이나 긴 입력의 균일한 품질 보증이 아닙니다. |
| 최대 출력 | 128,000 토큰. `max_output_tokens`의 실제 상한은 모델 한도보다 클 수 없습니다. |
| 표준 텍스트 가격 | 입력 100만 토큰당 USD 0.75, 캐시된 입력 USD 0.075, 출력 USD 4.50. 지역 처리 엔드포인트는 10% 가산입니다. |
| API | `POST /v1/responses`를 지원합니다. `max_output_tokens`는 보이는 출력과 reasoning token을 합친 생성 토큰의 상한입니다. |
| 사용량 기록 | 응답의 `usage.input_tokens`, `usage.output_tokens`, `usage.total_tokens`를 기록합니다. `input_tokens_details.cached_tokens`와 `output_tokens_details.reasoning_tokens`는 세부 분석용입니다. |
| 불완전 응답 | `incomplete_details.reason`가 `max_output_tokens`이면 출력 상한에 닿았다는 뜻입니다. 이때 답을 완결된 것으로 채점하거나 요약하지 않습니다. |

Ch 8의 비용 계산은 `usage`의 실제 토큰 수를 사용한다. 예를 들어 입력 1,000토큰과 출력 300토큰이면 도구 요금을 제외한 표준 텍스트 비용은 약 USD 0.00210이다. 계산식은 `(input_tokens × 0.75 + output_tokens × 4.50) / 1_000_000`이며, 캐시 입력은 실제 청구 세부 항목에 맞춰 별도로 계산한다. 이 숫자는 검색·파일 검색·웹 검색처럼 별도 도구 비용이 붙는 호출의 총비용이 아니다.

## 공식 문서·원 출처

* Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025-09-29 — 컨텍스트 정의, 최소 고신호 토큰 원칙, context rot, JIT 검색, compaction·메모·분리의 근거.
* Anthropic, [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), 2025-10-16 — 스킬 메타데이터→본문→연결 파일의 점진적 공개 사례.
* OpenAI, [GPT-5.4 Mini model](https://developers.openai.com/api/docs/models/gpt-5.4-mini), 2026-09-08 확인 — 모델 ID·스냅샷, 400k 창, 128k 최대 출력, 토큰 가격, 지원 엔드포인트.
* OpenAI, [Create a model response API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create), 2026-09-08 확인 — `max_output_tokens`, `usage`, `incomplete_details`, `previous_response_id`의 의미.

## 보조 출처: 분류와 실험

* LangChain Team, [Context Engineering](https://www.langchain.com/blog/context-engineering-for-agents), 2025-07-02 — Write/Select/Compress/Isolate 네 범주와 네 실패 양상을 소개한 벤더 유지 블로그. 표준 문서가 아니므로 분류의 출처를 본문에서 밝힙니다.
* Hong, Troynikov, Huber, [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://www.trychroma.com/research/context-rot), Chroma Technical Report, 2025-07-14 — 18개 모델의 통제 실험. 동료 심사 문헌이 아님을 함께 표기합니다.

## 집필 시 피할 표현

* “큰 컨텍스트 창이면 모든 정보를 정확히 기억합니다.”
* “네 실패 양상은 국제 표준입니다.”
* “요약은 원문을 보존하므로 안전합니다.”
* “컨텍스트 rot는 정확히 N토큰에서 시작합니다.”
* “점진적 공개는 언제나 더 빠르고 더 싸다.”

