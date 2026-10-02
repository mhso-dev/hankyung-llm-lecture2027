# 02 GitHub Flow와 PR 리뷰 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 02-6 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 저장소에서는 긴 선반이 main 브랜치, 수레가 기능 브랜치입니다. 검수대의 확인이 PR 리뷰이고, 선반에 올리는 일이 병합입니다. | 값 없음(비유). 파란 상자 두 개 = feat·fix 커밋 | — |
| 02-1 | 4 핵심 개념 · 세 저장소가 주고받는 길 (노트북 「오늘 볼 그림」) | Mermaid flowchart TB | 두 사람은 서로 직접 주고받지 않고, 늘 원격 저장소를 거칩니다. | 코드 3 `team.git`, 코드 4 `git clone`·`Ch3 Student`, 코드 9 push `feature/order-summary`, 코드 12 `Ch3 Reviewer`, 코드 18·22 `git fetch`, 코드 21 `git push origin main` | 저장소 tool(초록) |
| 02-2 | 5 실행 예제 · 기능 브랜치만 앞으로 옮겨 갑니다 | Mermaid flowchart TB(칸 + 이름표) | 새 커밋을 만들면 지금 있는 브랜치의 이름만 그 커밋으로 옮겨 갑니다. | 코드 8 `git branch -v` 두 줄, 코드 9 `[origin/feature/order-summary]`·`[origin/main]` | 커밋 tool(초록), 브랜치 이름 회색(클래스 없음) |
| 02-4 | 6 일부러 실패해 보기 · Before/After 결과 | Mermaid flowchart TB(Before/After 두 칸) | 기능 브랜치에서 실행한 확인 파일은 오류 없이 `빈 값: 주문 건`을 출력했습니다. | 코드 16 `보통 값 3: 주문 3건`·`빈 값: 주문 건`, 코드 17 `number = int(count)`, 코드 20 `입력 오류: invalid literal for int() with base 10: ''` | 함수 파일 tool(초록), 실행한 확인 flow(파랑), Before 결함 결과 fail(빨강), 받아서 출력한 오류 measure(노랑) |
| 02-3 | 6 일부러 실패해 보기 · 리뷰에서 병합까지 실제 순서 | Mermaid sequenceDiagram | 리뷰어는 병합 결과를 확인한 뒤에 main을 올렸습니다. | 코드 9·12·13 push·clone·switch, 코드 17 push, 코드 18 `behind 1`, 코드 19 `merge --no-ff`, 코드 21 `ahead 3`, 코드 22 `merge: 주문 요약` | 참여자 회색, 메모 노랑(확인 파일 실행 시점). 실선 = 요청한 명령, 점선 = 받아 온 결과(검토 1차 C-2), 라벨 왼쪽 정렬(C-3) |
| 02-5 | 8 정리 · 요약 도식 | Mermaid flowchart BT | 리뷰어는 `git fetch` 뒤 main에 병합하고, 확인한 다음 원격까지 올립니다. | 코드 21 `git log --oneline --graph` 네 커밋 메시지, `[origin/main]` | 커밋 tool(초록), 브랜치 이름 회색 |

색 규칙: 01절과 같이 저장소·커밋·파일은 모든 그림에서 초록, 우리가 실행한 일은 파랑입니다. 브랜치 이름(가리키는 이름표)은 클래스 없이 회색입니다. 빨강은 02-4 Before 결과(오류 없이 나온 틀린 글 = Before 결함)에만 씁니다. After의 입력 오류는 확인 파일이 `except`로 받아 출력한 오류라서 노랑입니다(규격 §5-3). 02-3의 메모는 sequenceDiagram 규칙대로 노랑이며 결과 값 대신 실행 시점만 적어 02-4의 빨강·노랑과 겹치지 않게 했습니다.
코드 번호는 노트북 코드 셀 순번(준비 셀 = 1)입니다. 검토 1차(2026-09-16)에서 작성자 config 셀을 복제 셀에 합쳐, 옛 코드 6부터 번호가 하나씩 줄었습니다.
