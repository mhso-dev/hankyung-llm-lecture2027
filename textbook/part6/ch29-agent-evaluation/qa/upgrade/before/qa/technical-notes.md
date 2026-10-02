# 구현 보완 기록

- 합성 지연 목록을 제거하고 Ch18의 실행 완료 노트북 출력과 Ch21의 실제 RAG 비교 JSON을 읽도록 교체했습니다.
- 두 기록을 final_score, model_calls, tool_calls, tokens, latency_s로 변환했습니다.
- `subset(효율)` 표현을 API 의미에 맞춰 허용 범위 검사로 바로잡고 효율은 호출·토큰·지연으로 따로 측정했습니다.
- 모든 agentevals 모드를 실제 실행하고 LLM judge 결과의 설명 원문을 노트북에 보존했습니다.
