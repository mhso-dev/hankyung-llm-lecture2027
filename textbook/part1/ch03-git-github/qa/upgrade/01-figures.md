# 01 커밋과 gitignore — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 01-5 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 책상이 작업 폴더, 열린 상자가 색인, 봉한 상자가 커밋입니다. | 값 없음(비유). 책 = 고른 파일, 휴지 = 무시 규칙에 적은 파일 | — |
| 01-1 | 4 핵심 개념 · 세 자리와 두 명령 (노트북 「오늘 볼 그림」) | Mermaid flowchart LR | 작업 폴더에서 고친 파일을 `git add` 명령으로 색인에 올립니다. | 노트북 [파일 세 개] 셀 `!! .env`, [두 번째 커밋] 셀 `feat: 주문 요약 추가`, `APP_MODE=demo`, 주문 2건 | 자리 tool(초록), 무시 표시 measure(노랑), .env 회색 |
| 01-2 | 5 실행 예제 · 목적별로 나눈 커밋 | Mermaid flowchart LR(이력 칸 + 작업 폴더 칸) | 목적이 다른 변경을 커밋 두 개로 나누면 메시지만 읽어도 무엇을 바꿨는지 알 수 있습니다. | 커밋 출력 `1 file changed`(1·2), `1 insertion(+), 1 deletion(-)`(3), 메시지 세 개, 상태 `!! .env` | 커밋 tool(초록), .env 표시 measure(노랑) |
| 01-3 | 5 실행 예제 · 두 비교가 보는 자리 | Mermaid flowchart TB(두 칸) | 명령 `git diff`는 작업 폴더와 색인을, `git diff --cached`는 색인과 마지막 커밋을 비교합니다. | [값 바꿔 보기] 셀 ` M app.py`, `-print("주문 2건")`/`+print("주문 3건")`; 다음 셀 `M  app.py`, 빈 `git diff`, `git diff --cached` 같은 줄 | 세 자리 tool(초록) |
| 01-4 | 6 일부러 실패해 보기 | Mermaid flowchart TB(Before/After 두 칸) | 무시 규칙은 아직 추적하지 않는 파일에만 적용됩니다. | Before `M debug.log`, `종료 코드: 1`; After `2 files changed`, 빈 상태 목록, `.gitignore:3:*.log` | 실행한 일 flow(파랑), 커밋·파일 tool(초록), Before 결과 fail(빨강), After 결과 measure(노랑) |

색 규칙: 작업 폴더·색인·커밋과 커밋에 들어간 파일은 모든 그림에서 초록입니다. 명령 출력으로 확인한 상태 표시(`!! .env`, After 결과)는 노랑입니다. 빨강은 01-4 Before 결과(규칙이 걸리지 않아 `M debug.log`가 남음)에만 씁니다. 01-1의 .env는 추적하지 않는 파일이라 클래스 없이 회색입니다.
