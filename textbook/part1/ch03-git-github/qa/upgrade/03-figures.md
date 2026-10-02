# 03 병합 충돌 해결 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 03-6 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 선반 끝 이름표 칸은 하나인데, 두 사람이 서로 다른 카드를 들고 왔습니다. 한 사람이 기준표를 보고 두 조건을 모두 담은 새 카드를 만들어 칸에 꽂습니다. | 값 없음(비유). 해 카드 = 리뷰어 줄, 달 카드 = 작성자 줄, 기준표 = `policy.txt` 두 줄 | — |
| 03-1 | 4 핵심 개념 · 공통 조상과 같은 줄 (노트북 「오늘 볼 그림」) | Mermaid flowchart BT | 두 쪽이 같은 줄을 서로 다르게 바꾸면 어느 쪽을 고를지 정하지 못합니다. | 코드 9 `merge: 출고 기준 받기`, 코드 11 `배송 안내: 14시 이전은 오늘 출고`, 코드 12 `docs: 익일 출고 안내`, 코드 13 `CONFLICT`, 코드 14 `UU message.txt` | 커밋 tool(초록), 멈춘 병합 fail(빨강) |
| 03-2 | 5 실행 예제 · 거절에서 병합까지 | Mermaid flowchart TB | 올리기가 거절되면 받아 와서 갈라진 모양을 보고, 병합한 뒤 다시 올립니다. | 코드 7 `! [rejected]`·`(fetch first)`·`종료 코드: 1`, 코드 8 `ahead 1, behind 1`, 코드 9 `Merge made by the 'ort' strategy.`·`main -> main`, 코드 10 `Fast-forward` | 거절 fail(빨강), 짝 비교 표시 measure(노랑), 성공한 명령 flow(파랑) |
| 03-3 | 6 일부러 실패해 보기 · 값 하나 바꿔 보기 비교 | Mermaid flowchart TB(1차/2차 두 칸) | 달라진 것은 두 커밋이 고친 자리이고, 그 차이는 병합할 때 드러납니다. | 코드 6·7 `policy.txt`·`contact.txt`, 코드 9 `Merge made by the 'ort' strategy.`, 코드 11·12 두 줄, 코드 13 `CONFLICT`·`종료 코드: 1` | 커밋이 고친 자리 tool(초록), 성공한 병합 flow(파랑), 멈춘 병합 fail(빨강) |
| 03-4 | 6 일부러 실패해 보기 · After 순서 | Mermaid flowchart TB | 멈춘 병합은 사람이 `git commit`으로 마칩니다. | 코드 14 `UU message.txt`·`종료 코드: 128`, 코드 16 `M  message.txt`, 코드 17 `merge: 출고 기준에 맞춰 충돌 해결`, 코드 19 `충돌 표시가 남아 있음: False` | 멈춘 상태·거절 fail(빨강), 우리가 한 일 flow(파랑), 상태·확인 결과 measure(노랑), 병합 커밋 tool(초록) |
| 03-5 | 8 정리 · 요약 도식 | Mermaid flowchart BT | 멈춘 병합은 팀 기준으로 남길 줄을 정해 파일을 고친 뒤 `git add`와 `git commit`으로 마치고 원격에 올립니다. | 코드 17 `git log --oneline --graph` 일곱 커밋 메시지, 코드 18 `[origin/main]` | 커밋 tool(초록) |

색 규칙: 01·02절과 같이 커밋·파일은 초록, 우리가 실행해 성공한 일은 파랑입니다. 짝 비교 표시(`ahead 1, behind 1`)와 상태 표시(`M  message.txt`), 확인 출력(`충돌 표시가 남아 있음: False`)은 노랑입니다.
빨강은 git이 멈추거나 거절한 실패(종료 코드 1·128, `UU` 상태)에만 씁니다(규격 §5-3). 성공한 병합 `Merge made by the 'ort' strategy.`는 03-2·03-3 모두 파랑으로 맞췄습니다.
코드 번호는 노트북 코드 셀 순번(준비 셀 = 1)입니다.
