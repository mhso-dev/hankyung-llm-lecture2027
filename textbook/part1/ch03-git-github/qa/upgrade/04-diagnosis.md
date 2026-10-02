# 04-revert-reflog-worktree — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/04-recovery-tools.*`).
생성기: `qa/upgrade/author_04.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch03-git-github 04`.
이어짐 기준: Ch 1·Ch 2 `chapter-summary.md`, 01~03절 완료본(`_src`, 노트북, `author_01.py`~`author_03.py`, `01`~`03-diagnosis.md`), `handoff.md` §03 → §04.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 3 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 9 | 0 |
| G6 | 29 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 19 (준비 1 + 본문 18) |
| 검사한 문장 | 119 | 371 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Git 2.34.1, 2026-09-16), verify PASS(챕터 5절 86셀).

## 수정 전 주요 문제

- G1: 준비 셀 하나에 `git(*args, cwd=..., check=...)`와 `configure()` 두 함수, `*args` 정의(A 트랙 미교육), `Path | None`·`cwd or root`, 복구 셀의 `next(line.split("\t", 1)[0] for line in ... if ...)` 제너레이터 식
- 배우지 않은 문법·모양: `TemporaryDirectory`·`pathlib.Path`·`mkdir`·`write_text`·`read_text`·`exists()`, `rev-parse HEAD`로 해시를 변수(`good`·`bad`·`lost`)에 담기(`good`은 쓰지도 않음), `--format=%H`·`%H%x09%gs` 형식 지정, `split("\t", 1)` 최대 분할 인자, `branch --show-current`·`worktree list --porcelain`, `assert` 네 줄(`candidate == lost`처럼 미리 담아 둔 해시와 비교)
- 이어짐: 작성자 `Git Learner`·`learner@example.invalid`, 원격 없는 단독 저장소 `recovery`(학습 목표는 「공개 변경 취소」인데 공개된 적이 없음), 첫 설명 셀이 01절에서 배운 작업 폴더·색인·커밋·HEAD·브랜치를 처음처럼 다시 정의, 03절 `run_git()`·`team.git`·`author`/`reviewer`를 쓰지 않음
- 내용: worktree 셀이 커밋만 하고 「기본 폴더 작업을 둔 채」라는 이유를 출력으로 보여 주지 않음. 임시 경로와 전체 해시를 그대로 출력(`worktree list --porcelain`). 복습 3번(reflog 만료)을 실행·문서 근거 없이 단정. 값 바꿔 보기 없음
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기 셀 없음
- G6: 70자 초과(한 문장에 revert·reflog·worktree 선택 기준을 함께), 영문·코드 이름+조사 시작(「`worktree`로」, 「reflog는」, 「Git은」 등 22곳), 금지어 「되돌립니다」 2곳, 5문장 넘는 단락 2곳
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. Excalidraw 도식 1장

## 바꾼 것

- 학습 질문·데이터·형식 유지: paired, `config.txt` `discount=10` → `discount=90` → `git revert`로 `discount=10`, 커밋 `feat: 할인율 10 설정`·`fix: 할인율 90 설정`, `idea.txt` 커밋 → `git reset --hard HEAD~1` → `git reflog` → 브랜치 `recovered-idea`, worktree `fix/urgent`. 아이디어 파일 내용은 `recover me` → `첫 주문 쿠폰 아이디어`, 커밋 메시지 `experiment: 복구할 아이디어` → `docs: 쿠폰 아이디어 기록`(03절 `docs:` 관례), 긴급 파일 `hotfix.txt` `urgent=true` → `config.txt`에 `max_discount=30`(할인율 사고와 이어지는 급한 수정)
- 03절을 이어 씀: 준비 셀 `mkdtemp(prefix="ch03-04-")`+`chdir`+`listdir`, `run_git(command, folder=".")` 같은 모양 재정의, 원격 `team.git`, 작성자 `author`(`Ch3 Student`)·리뷰어 `reviewer`(`Ch3 Reviewer`). 잘못된 커밋을 올리고 리뷰어가 `git pull`로 받아 `discount=90`을 읽게 해 「공개한 커밋」을 실제로 만듦 → revert → 거절 없는 `git push`와 리뷰어 `Fast-forward`로 `discount=10`
- 해시 없이 가리키기(handoff 권고): `rev-parse` 대신 `HEAD`·`HEAD~1`(01절)·브랜치 이름, 복구는 `next(...)`를 `for`+`break`로 푸는 대신 git의 참조 기록 이름 `HEAD@{1}`을 그대로 사용(`git branch recovered-idea HEAD@{1}`). 해시·임시 경로는 결과 읽기에서 인용하지 않음
- worktree 이유를 출력으로: 기본 폴더에 커밋하지 않은 `notice.txt`를 둔 채 `worktree add -b fix/urgent ../urgent-fix` → 새 폴더에서 커밋 → 새 폴더 `git branch` `* fix/urgent`·`+ main`, 기본 폴더 `?? notice.txt`·`+ fix/urgent`·`discount=10` 한 줄. `git worktree remove`로 정리하고 `fix/urgent` 브랜치가 남는 것까지 실행
- 값 하나 바꿔 보기를 실행으로 추가: worktree에 꺼낼 브랜치를 새 브랜치 `fix/urgent` → 기본 폴더가 쓰는 `main`으로 바꿈 → `fatal: 'main' is already checked out at`·`종료 코드: 128`, 목록 그대로 두 줄
- Before: `switch -c experiment` + 커밋 → `reset --hard HEAD~1` → `log --oneline`에 아이디어 커밋 없음·`idea.txt가 폴더에 있는가: False`. After: `reflog -5`(`HEAD@{1}: commit: docs: 쿠폰 아이디어 기록`) → `branch recovered-idea HEAD@{1}` + `log --oneline -1`(02절) + `show 브랜치:파일`(01절) → `switch recovered-idea` + 같은 확인 `True`. `assert` 대신 출력으로 읽음
- 본문 10블록 전체 재작성. 용어 6개 표(공개한 커밋·취소 커밋·리셋·참조 기록·`HEAD@{n}`·추가 작업 폴더), 「공개한 커밋은 더해서 취소합니다」, 「이름을 옮긴 커밋은 참조 기록에서 찾습니다」, 복습 5문항(5번이 「이 절의 질문」에 답함, 2번에 「빼고 올리는 경우는 실행하지 않았습니다」). 실행하지 않은 동작(공개한 커밋 reset·`--force`, revert 충돌·`--continue`, `--hard`로 커밋 전 변경 잃기, reflog 기한, 고치다 만 폴더의 `worktree remove`, GitHub 되돌리기 버튼)은 주의 메모에 「이번에 실행하지 않았습니다」 또는 git 문서 근거로만 적음
- 그림: Mermaid 5장(더하기와 옮기기, 공개한 커밋 취소 sequenceDiagram, 두 작업 폴더, 사라진 커밋 되살리기, 상황별 도구) + 삽화 1장(취소 상자와 깃발 수첩, 02-6·03-6 창고 선반을 이어 씀). 기존 Excalidraw 도식은 04-5로 바꾸고 본문에서 뺌(원본 `before/figures/`, `figures/04-recovery-tools.*`는 삭제하지 않음)
- 참고 자료: git-revert(작업 폴더가 깨끗해야 함·`--no-edit`·`--continue`), git-reset(`--hard`), git-reflog(로컬 저장소 기록·`HEAD@{2}` 뜻·기본 90일/30일 정리), git-worktree(이미 쓰는 브랜치 거절·clean만 remove), git-branch(`*`·`+` 표시, 시작 커밋 지정) — 2026-09-16 확인

## 검토에서 볼 곳

- 복구에 `HEAD@{1}`을 그대로 쓴 선택: handoff는 `for`+`break` 파싱을 제안했으나, 사람이 메시지로 줄을 확인하고 git 이름으로 가리키는 편이 입문 사다리·해시 비인용 규칙에 맞다고 판단함. 주의 메모에 「번호는 HEAD를 옮기면 달라짐, 쓰기 직전에 다시 확인」을 적음
- 04-1의 브랜치 이름 회색·점선 연결(02절 규칙)과 잘못된 커밋 `fix: 할인율 90 설정`을 빨강이 아닌 초록으로 둔 것(실패가 아닌 이력 속 커밋), reset 명령은 파랑·Before 결과 `False`만 빨강(04-4)
- 04-2 sequenceDiagram에서 작성자 자기 메시지 글자 `git revert --no-edit HEAD`가 세로선에 조금 겹침(읽기에는 지장 없음)
- 삽화 04-6: 오른쪽 상자 셋의 높이가 계단처럼 다름. worktree는 삽화에 넣지 않고 Mermaid 04-3으로만 보여 줌

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 1, 하 2, 공통 C-2·C-3·C-5). 모두 반영했습니다. 결정 Q1대로 `HEAD@{1}` 복구와 잘못된 커밋 초록은 유지했습니다.
- 04-1(중): 참조 기록 정의를 「HEAD가 옮겨 갈 때마다」로 통일. 용어 표 「HEAD가 옮겨 갈 때마다(커밋, 브랜치 전환, reset 등) 이 저장소가 적어 두는 기록」, b4 「저장소는 HEAD가 옮겨 갈 때마다 참조 기록에 한 줄씩 적습니다. 커밋이 그대로여도 브랜치를 바꾸면 한 줄이 생깁니다.」, 노트북 10번 설명·코드 주석 「HEAD가 옮겨 간 기록」, 결과 읽기 끝 「셋째 줄 `checkout`은 커밋은 그대로이고 브랜치만 바꾼 기록입니다.」 같은 뜻으로 주의 메모 「참조 기록은 HEAD가 옮겨 간 기록이라 커밋하지 않은 변경은 여기서 찾을 수 없습니다」와 handoff §03→§04 정의에도 표시
- 04-2: 노트북 할 일 3과 10번 소제목의 「이동 기록」 → 「참조 기록」
- 04-3: 주의 메모 「git 문서는 취소 커밋을 만들기 전에 작업 폴더를 깨끗하게 두라고 안내합니다. 교재 환경에서 따로 해 보니, 취소할 파일을 고쳐 둔 경우에는 `revert failed`로 멈췄습니다. 노트북은 취소를 먼저 마치고 공지 초안을 만들었습니다.」(검토 세션의 기기 셸 확인이 근거)
- C-2·C-3: `04-2-공개한-커밋-취소.mmd`에 `messageAlign: left`(자기 메시지 `git revert --no-edit HEAD`가 세로선과 겹치지 않음, PNG 확인), 도식 읽기에 「실선 화살표는 요청한 명령, 점선 화살표는 받아 온 결과입니다.」
- C-5: 게이트 표 검사한 문장 370 → 371(당시 `gates-wip-all.json`)
- 검토 밖: `visual.cjs`가 04-4 SVG 글자 13.74px(viewBox 885)를 잡아 `git branch recovered-idea HEAD@{1}` 라벨을 세 줄로 나눠 806으로 줄임(글자는 같음, PNG 확인)
- 코드 셀 19, 검사한 문장 375

재실행: `run_section.sh … 04`(새 커널 PASS) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 112 code cells (max 18 lines)`, `visual.cjs` 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/04-revert-reflog-worktree.md`
- 루트 `textbook/qa/upgrade-progress.md` 표는 챕터 밖 파일이라 이 작업에서 고치지 않음
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
