# 03-병합-충돌-해결 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/03-merge-conflict.*`).
생성기: `qa/upgrade/author_03.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch03-git-github 03`.
이어짐 기준: Ch 1·Ch 2 `chapter-summary.md`, 01·02절 완료본(`_src`, 노트북, `author_01.py`·`author_02.py`, `01-diagnosis.md`·`02-diagnosis.md`), `handoff.md` §02 → §03.

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
| 검사한 문장 | 106 | 362 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Git 2.34.1, 2026-09-16), verify PASS(챕터 5절 73셀).

## 수정 전 주요 문제

- G1: 준비 셀 하나에 `git(*args, cwd=..., check=...)`와 `configure()` 두 함수, `*args` 정의(A 트랙 미교육), `Path | None`·`cwd or root`, 마지막 셀 `all(marker not in saved for marker in (...))` 제너레이터 식
- 배우지 않은 문법·모양: `pathlib.Path`·`write_text`·`read_text`, `alice, bob = root / "alice", root / "bob"` 한 줄 두 경로, `subprocess.run(["git", "push", ...])` 직접 호출과 `push.stderr.strip().splitlines()[-1]` 연결, `git show --pretty=%P`·`rev-parse`, `assert` 여섯 줄(부모 수·HEAD 일치를 출력 없이 assert로만 확인)
- 이어짐: 작성자 `Git Learner`·`learner@example.invalid`(01·02절은 `Ch3 Student`/`Ch3 Reviewer`), `TemporaryDirectory(prefix="git-lesson-")`(02절은 `mkdtemp(prefix="ch03-02-")`+`chdir`), 02절 `run_git()`을 쓰지 않음. 첫 설명 셀이 01절에서 배운 작업 폴더·색인·커밋·HEAD·브랜치를 처음처럼 다시 정의. 02절에서 가르치지 않은 `git pull --no-rebase`를 설명 없이 사용
- 내용: 거절 이유 끝줄이 `hint: See the 'Note about fast-forwards'…`라 거절 원인을 보여 주지 못함. 「서로 다른 파일이면 자동 병합」을 본문에서 주장만 하고 실행하지 않음(복습 1번 해설도 실행 근거 없음). 3번 셀 결과가 `준비 완료` 한 줄
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기 셀 없음
- G6: 70자 초과 문장(한 문장에 fetch·merge·--no-rebase 정의를 함께), 영문·코드 이름+조사 시작(「`git add`하면」, 「Git은」 등)
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. Excalidraw 도식 1장

## 바꾼 것

- 학습 질문·데이터·형식 유지: paired, `policy.txt` 두 줄(`14시 이전 결제: 오늘 출고`/`14시 이후 결제: 내일 출고`), `message.txt` 한 줄을 두 사람이 `14시 이전은 오늘 출고`/`내일 출고`로 다르게 고침, 해결 문장 `배송 안내: 14시 이전 결제는 오늘 출고, 14시 이후 결제는 내일 출고`, 커밋 메시지 `docs: 당일 출고 안내`·`docs: 익일 출고 안내`·`merge: 출고 정책에 맞춰 충돌 해결`(→ `출고 기준에 맞춰`)
- 02절을 이어 씀: 준비 셀 `mkdtemp(prefix="ch03-03-")`+`chdir`+`listdir`, `run_git(command, folder=".")` 같은 모양 재정의, 원격 `team.git`, 작성자 `author`(`Ch3 Student`)·리뷰어 `reviewer`(`Ch3 Reviewer`) — Alice/Bob 대신 02절의 두 사람이 이번에는 팀원으로 파일을 고침. `git fetch` → `git branch -vv`(`ahead 1, behind 1`) → `git merge origin/main -m` 순서는 02절 명령만으로 구성
- 값 하나 바꿔 보기를 실행으로 추가: 1차 「서로 다른 파일」(리뷰어 `policy.txt`, 작성자 `contact.txt`) → 거절(`! [rejected]`·`(fetch first)`·`종료 코드: 1`) → 받아 오기 → 자동 병합(`Merge made by the 'ort' strategy.`) → 올리기 → 리뷰어 `git pull`(`Fast-forward`). 2차는 고치는 자리만 `message.txt` 같은 줄로 바꿈. 두 번 모두 병합 전 짝 비교가 같다는 점을 결과 읽기에 적음
- `git pull`은 뒤처진 리뷰어가 받는 자리(fast-forward)에서만 실행하고 「받아 오기 뒤 병합」 한 문장으로 풂. 갈라진 상태의 `git pull --no-rebase`는 주의 메모에서 git 문서 근거로만 적고 「노트북은 fetch와 merge를 나눠 실행」으로 표시
- Before: 병합 `CONFLICT (content)`·`종료 코드: 1` → `status --short` `UU message.txt` + 해결 전 커밋 시도 `Committing is not possible because you have unmerged files.`·`종료 코드: 128`(git이 `git add`로 해결 표시하라는 안내를 보여 줌) → 파일 읽기(`<<<<<<< HEAD`·`=======`·`>>>>>>> origin/main`)와 `충돌 표시가 남아 있음: True`
- After: `policy.txt` 읽기와 새 줄 쓰기·`git add`·`M  message.txt` → `git commit` + `log --oneline --graph`(두 번의 병합 모양) → `git push` + `branch -vv` `[origin/main]` → 리뷰어 `git pull` + 같은 방법 확인 `False`. `assert` 대신 출력으로 읽음(부모 둘은 이력 그림으로)
- 본문 10블록 전체 재작성. 용어 7개 표(올리기 거절·갈라진 이력·공통 조상·풀·fast-forward 병합·병합 충돌·충돌 표시), 「거절은 커밋 줄기를 보고 정합니다」, 「공통 조상과 같은 줄」, 복습 5문항(5번이 「이 절의 질문」에 답함, 4번은 실행하지 않은 경우라고 해설에 적음)
- 그림: Mermaid 5장(갈라진 두 줄기, 거절에서 병합까지, 다른 파일과 같은 줄, 멈춘 병합 마치기, 두 번의 병합 이력) + 삽화 1장(한 칸의 두 카드, 02-6 선반을 이어 씀). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/03-merge-conflict.*`는 삭제하지 않음)
- 참고 자료: git-merge(충돌 표시·해결·fast-forward), git-status(`UU` = unmerged, both modified), git-pull(fetch 뒤 병합, 갈라지면 기본 설정에서 실패), git-push(fast-forward가 아닌 올리기 거절, `--force`는 원격 커밋을 잃게 할 수 있음) — 2026-09-16 확인. GitHub 문서 두 개는 이전 확인일 2026-09-09 유지

## 검토에서 볼 곳

- 리뷰어(`Ch3 Reviewer`)가 파일을 고치는 설정: 02절의 두 사람을 그대로 이어 쓰려고 고른 것. 「팀원으로서 파일을 직접 고칩니다」 한 문장으로만 설명함
- 1차 병합 결과(성공)를 03-2·03-3에서 파랑(성공한 명령)으로, 짝 비교·상태·확인 출력은 노랑, 거절·충돌·커밋 거절(종료 코드 1·128)은 빨강으로 칠함(§5-3)
- 실행 예제 결과 읽기의 「`result.stdout`을 먼저, `result.stderr`를 나중에 출력해서 순서가 바뀌어 보입니다」(Ch 1 03절 `.stdout`·`.stderr`에 기댐)
- 삽화 03-6: 2차 채택본은 두 사람이 칸을 가리키지 않고 곤란한 얼굴로 마주 봄(물음표 기호 두 개). 기준판이 받침 달린 판이라 화면처럼 보일 여지. 1차 탈락 사유는 `.prompt.md`

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept(중 0, 하 4, 공통 C-4). 모두 반영했습니다(03-4는 다시 만들지 않는 쪽).
- 03-1: 본문 03-2 도식 읽기 「병합 커밋을 새로 만들지 않고 이름만 앞으로 옮기는 `Fast-forward`」, 노트북 8번 「병합 커밋을 새로 만들지 않고 main 이름만 앞으로 옮깁니다」
- 03-2: 주의 메모 「충돌 중 `git checkout --ours 파일`·`--theirs 파일`은 파일 전체를 한쪽 내용으로 고릅니다. 충돌하지 않은 다른 쪽 변경까지 사라질 수 있어 이번에는 쓰지 않았습니다.」
- 03-3: 주의 메모 「교재 환경의 Git 2.34.1에서 갈라진 상태로 설정 없이 `git pull`을 따로 실행해 봤습니다. 그러자 `Need to specify how to reconcile divergent branches`로 멈췄습니다. 노트북에서는 실행하지 않았고, 이때는 `git fetch`와 `git merge`를 나눠 실행합니다.」(검토 세션의 기기 셸 확인을 근거로 씀)
- 03-4: 삽화 03-6은 다시 만들지 않고(크레딧 0), 그림 읽기와 캡션 읽는 법을 「받침에 세워 둔 기준판」으로 고침. prompt.md에 다시 만들 때의 문구를 적음
- C-4: `print("작성자의 message.txt:")`, `print("출고 기준 policy.txt:")`, `print("리뷰어의 message.txt:")` 라벨 줄. 출력 첫 줄만 늘고 결과 읽기는 줄 번호를 쓰지 않아 그대로
- 코드 셀 19, 검사한 문장 363

재실행: `run_section.sh … 03`(새 커널 PASS) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 112 code cells (max 18 lines)`, `visual.cjs` 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/03-병합-충돌-해결.md`
- 루트 `textbook/qa/upgrade-progress.md` 표는 챕터 밖 파일이라 이 작업에서 고치지 않음
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
