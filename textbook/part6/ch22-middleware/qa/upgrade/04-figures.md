# 04 호출 한도와 재시도·폴백 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 04-1 | 4 핵심 개념 · 노트북 첫 그림 | Mermaid flowchart(세 줄) | 세 정책은 실패 뒤에 하는 일이 다릅니다. | 구조 도식 | model, fail, flow, measure |
| 04-2 | 5 실행 예제 뒤 · 재시도 | Mermaid sequenceDiagram | 재시도는 원인이 그대로면 결과를 바꾸지 못합니다. | In[5] 시간 제한 `0.001`, In[6] 시도 횟수 `3`, initial_delay 0.5 | — |
| 04-3 | 6 실험 결과 해석 · 폴백 | Mermaid flowchart | 첫 모델이 실패하자 예비 모델로 바꿨습니다. | In[9] `gpt-no-such-model` → `gpt-5.4-nano` | flow, model, fail |
| 04-4 | 6 실험 결과 해석 · 호출 한도 | Mermaid flowchart | 두 번째 모델 호출이 한도에 걸렸습니다. | In[13] 메시지 네 개, `평일 09:00~20:00`, `Model call limits exceeded` | flow, model, tool, fail |
| 04-5 | 4 핵심 개념 · 비유 | Higgsfield 삽화(대기) | 전화가 안 될 때의 세 가지 대처 | 값 없음 | — |
