# 02 PII 마스킹 이식 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 02-1 | 4 핵심 개념 · 노트북 첫 그림 | Mermaid flowchart(비교) | 미들웨어는 정해진 자리에 한 번만 끼워 넣습니다. | In[9] `learner@example.com`, In[13] `learner@****.com` | flow, model, fail |
| 02-2 | 4 핵심 개념 · 두 방식 | Mermaid flowchart(비교) | 마스킹 함수는 부를 때만, 미들웨어는 호출마다 적용됩니다. | 구조 도식 | flow, model, fail |
| 02-3 | 6 Before/After 뒤 해석 | Mermaid flowchart(세 줄 비교) | 내장 미들웨어는 등록한 종류만 가립니다. | In[15] `010-1234-5678` 그대로, In[16] `****5678` | flow, model, fail |
| 02-4 | 4 핵심 개념 · 비유 | Higgsfield 삽화(대기) | 발송 전에 가림 스티커를 붙입니다. | 값 없음 | — |
