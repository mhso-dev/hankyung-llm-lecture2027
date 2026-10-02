# Ch18 공식 문서 조사와 실행 전 비용 계획

- 조사일: 2026-09-10
- 기준 모델: `gpt-5.4-mini`
- SDK: `openai==2.29.0`
- API: Responses API

## 공식 근거

OpenAI Python SDK의 공식 저장소는 `OpenAI`와 `AsyncOpenAI`가 같은 인터페이스를 제공하며, 텍스트 생성의 기본 API로 Responses API를 안내합니다. 응답의 `output_text`를 읽고, 비동기 호출에서는 `await client.responses.create(...)`를 사용합니다. Responses API 응답에는 입력·출력·전체 토큰 사용량이 포함됩니다.

`gpt-5.4-mini` 공식 모델 페이지는 Responses API, 구조화 출력과 비동기 SDK 호출을 지원한다고 명시합니다. 2026-09-10 확인 가격은 입력 100만 토큰당 0.75달러, 캐시 입력 0.075달러, 출력 100만 토큰당 4.50달러입니다. 이 장은 텍스트 입력만 사용하며 캐시 할인은 비용 상한 계산에 반영하지 않습니다.

## 실행 전 비용 상한

비용 상한은 할인 없는 입력·출력 단가로 보수적으로 계산합니다. 실행 뒤 표시하는 값도 응답의 `usage.input_tokens`와 `usage.output_tokens`에 이 단가를 곱한 추정치입니다. 캐시 할인, 세금, 청구 조정은 반영하지 않으므로 제공자 청구서의 실제 결제 금액을 뜻하지 않습니다. 각 절은 1달러 미만이어야 하며, 아래 계획은 이를 크게 밑돕니다.

| 절 | 최대 API 호출 | 호출당 최대 출력 토큰 | 계획상 입력 토큰 상한 | 계획상 출력 토큰 상한 | 보수적 예상 비용 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 01 체이닝 | 3 | 260 | 6,000 | 780 | $0.0081 |
| 02 라우팅 | 4 | 220 | 8,000 | 880 | $0.0100 |
| 03 병렬 | 8 | 220 | 16,000 | 1,760 | $0.0199 |
| 04 오케스트레이터-워커 | 6 | 700 | 15,000 | 2,600 | $0.0229 |
| 05 생성자-평가자 | 6 | 260 | 18,000 | 1,560 | $0.0205 |
| 06 다섯 패턴 비교 | 18 | 500 | 45,000 | 6,000 | $0.0608 |

실행 중에는 호출 수와 `max_output_tokens` 상한을 코드에서 고정합니다. 06절 비교는 같은 과제·모델·채점 기준을 사용합니다. 라우팅이 허용 범주를 반환하지 않으면 `no_answer` 상태로 기록할 수 있지만, 엄격한 `answer` 또는 `score` 형식이 깨지면 해당 실행을 명시적으로 실패시킵니다. 임의의 문자열이나 0점으로 바꾸어 계속하지 않습니다. 최고 점수가 같으면 동점을 그대로 유지합니다.

## 출처

- [OpenAI Python SDK 공식 저장소](https://github.com/openai/openai-python) · 확인 2026-09-10 · `OpenAI`, `AsyncOpenAI`, Responses API, `.env` 권장
- [OpenAI Python SDK LICENSE](https://github.com/openai/openai-python/blob/main/LICENSE) · 확인 2026-09-10 · Apache-2.0
- [GPT-5.4 Mini 모델](https://developers.openai.com/api/docs/models/gpt-5.4-mini) · 확인 2026-09-10 · 가격, 컨텍스트, Responses API와 구조화 출력 지원
- [OpenAI API 빠른 시작](https://platform.openai.com/docs/quickstart/make-your-first-api-request) · 확인 2026-09-10 · Responses API와 `output_text`

## 확인 필요 항목

가격과 모델 별칭은 서비스 변경 대상입니다. 수강생이 실습을 다시 실행하는 날 공식 모델 페이지를 확인해야 합니다.
