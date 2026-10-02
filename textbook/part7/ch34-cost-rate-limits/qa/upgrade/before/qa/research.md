# Ch34 공식 자료 조사

- 확인일: 2026-09-11
- OpenAI Prompt caching: 1,024토큰 이상의 프롬프트에서 자동 캐싱이 적용되며 `usage`의 캐시 토큰으로 적중을 확인합니다. <https://developers.openai.com/api/docs/guides/prompt-caching>
- OpenAI Batch API: JSONL 입력, 고유한 `custom_id`, 현재 `24h` 완료 창, 표준 동기 API 대비 50% 할인을 확인했습니다. <https://developers.openai.com/api/docs/guides/batch>
- OpenAI Rate limits: 요청·토큰 제한, 지수 백오프와 무작위 지터 권고를 확인했습니다. <https://developers.openai.com/api/docs/guides/rate-limits>
- GPT-5.4 mini: 표준 입력 0.75달러, 캐시 입력 0.075달러, 출력 4.50달러/100만 토큰을 확인했습니다. <https://developers.openai.com/api/docs/models/gpt-5.4-mini>
- GPT-5.4 nano: 표준 입력 0.20달러, 캐시 입력 0.020달러, 출력 1.25달러/100만 토큰을 확인했습니다. <https://developers.openai.com/api/docs/models/gpt-5.4-nano>

## 적용 범위

단가는 실제 API 사용량에 적용했습니다. 캐시 절의 `cache_creation`은 LangChain `usage_metadata`가 값을 제공하지 않아 `null`로 보존했습니다. 이는 생성량 0을 뜻하지 않습니다. Batch 입력은 로컬 구조 검증까지 마쳤고 외부 제출은 수행하지 않았습니다.
