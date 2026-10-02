# 04 revert, reflog, worktree — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 04-6 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 팀 선반의 잘못 포장한 상자는 그대로 두고 되돌리기 화살표를 그린 상자를 더합니다. 내 책상에서는 수첩의 깃발 기록을 보고 끝 상자에 새 깃발을 꽂습니다. | 값 없음(비유). 화살표 상자 = 취소 커밋, 깃발 = 브랜치 이름, 수첩 = 참조 기록, 파란 새 깃발 = `recovered-idea` | — |
| 04-1 | 4 핵심 개념 · 이름을 옮긴 커밋은 참조 기록에서 찾습니다 (노트북 「오늘 볼 그림」) | Mermaid flowchart LR(두 칸, 칸 안 BT) | 취소 커밋은 커밋을 더하고, reset은 이름을 옮깁니다. | 코드 8 `git log --oneline` 세 커밋·`discount=10`/`discount=90`, 코드 15 `docs: 쿠폰 아이디어 기록`, 코드 16 `HEAD is now at` 뒤 커밋 | 커밋 tool(초록), 브랜치 이름 회색 |
| 04-2 | 5 실행 예제 · 공개한 커밋을 취소한 순서 | Mermaid sequenceDiagram | 작성자는 이력을 고치지 않고 커밋을 하나 더해 올렸습니다. | 코드 6 `main -> main`, 코드 7 `Fast-forward`·`리뷰어의 config.txt: discount=90`, 코드 8 `git revert --no-edit HEAD`·세 커밋, 코드 9 `main -> main`·`Fast-forward`·`discount=10` | 메모 노랑(확인한 값) |
| 04-3 | 5 실행 예제 · 두 작업 폴더와 거절된 세 번째 폴더 | Mermaid flowchart TB | 두 폴더는 커밋과 브랜치 기록을 함께 쓰지만 작업 파일은 따로 가집니다. | 코드 10 `[main]`·`[fix/urgent]`, 코드 11 `fix: 할인율 상한 30 추가`, 코드 12 `?? notice.txt`·`* main`·`discount=10`, 코드 13 `already checked out`·`종료 코드: 128` | 저장소·폴더 tool(초록), 거절 fail(빨강) |
| 04-4 | 6 일부러 실패해 보기 · 감춰진 커밋을 되살린 순서 | Mermaid flowchart TB(Before/After 두 칸) | 사이에 한 일은 참조 기록을 읽고 이름을 하나 붙인 것뿐입니다. | 코드 16 `git log --oneline`·`False`, 코드 17 `HEAD@{1}: commit: docs: 쿠폰 아이디어 기록`, 코드 18 `git branch recovered-idea HEAD@{1}`, 코드 19 `True` | 실행한 명령 flow(파랑), 출력 measure(노랑), Before 결함 결과 fail(빨강) |
| 04-5 | 8 정리 · 요약 도식 | Mermaid flowchart LR(세 줄) | 세 명령은 순서대로 실행하는 절차가 아니라, 상황에 따라 고르는 도구입니다. | 코드 8 `git revert HEAD`, 코드 10 `git worktree add`, 코드 17·18 `git reflog`·`HEAD@{1}` | 상황 회색, 명령 flow(파랑) |

색 규칙: 01~03절과 같이 커밋·파일·작업 폴더는 초록, 우리가 실행한 명령은 파랑, 확인한 출력은 노랑입니다. 브랜치 이름은 02절처럼 회색입니다.
빨강은 git이 거절한 실패(코드 13 `종료 코드: 128`)와 Before 결함 결과(코드 16 `idea.txt가 폴더에 있는가: False`)에만 씁니다(규격 §5-3). reset 명령 자체는 종료 코드 줄 없이 성공했으므로 파랑입니다.
잘못된 커밋 `fix: 할인율 90 설정`은 실패가 아니라 이력에 남는 커밋이라 초록으로 둡니다.
코드 번호는 노트북 코드 셀 순번(준비 셀 = 1)입니다.
