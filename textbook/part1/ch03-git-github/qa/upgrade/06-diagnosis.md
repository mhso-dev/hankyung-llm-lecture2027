# 06-Git-실습 — 챕터 끝 실습 절 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md` §7-2, `textbook/_notebook/upgrade/PLAYBOOK.md` §3, `.claude/agents/easy-upgrade-editor.md` 6.8. 기준 사례: Ch 22 `09-Middleware-실습`, Ch 1 `06-개발환경-실습`(`author_06.py`), Ch 2 `13-파이썬-실습`(`author_13.py`, 검토 반영본).
새 절이라 수정 전 원본(`qa/upgrade/before/`)은 없습니다. 생성기: `qa/upgrade/author_06.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch03-git-github 06`.
먼저 읽은 것: Ch 1·Ch 2 `qa/upgrade/chapter-summary.md`, 이 챕터 `qa/upgrade/handoff.md`(특히 `## §05 → 실습`), `author_02`~`05.py`, `_src/05`, `05-figures.md`, 05-5·02-6·01-5 삽화 프롬프트, Ch 2 `author_13.py`·`_src/13`·`13-figures.md`·`13-diagnosis.md`, Ch 1 `author_06.py`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 새 절 | 0 |
| G2 | 새 절 | 0 |
| G3 | 새 절 | 0 |
| G4 | 새 절 | 0 |
| G5 | 새 절 | 0 |
| G6 | 새 절 | 0 (첫 검사 9건: 70자 초과 3, 영문 시작 5, 6문장 단락 1 → 문장 나눔·주어 앞에 종류 이름) |
| G7 | 새 절 | 0 |
| 코드 셀 | 새 절 | 16 (준비 1 + 본 경로 15, 심화 셀 없음) |
| 검사한 문장 | 새 절 | 333 (노트북 설명 셀 + `_src`) |
| 모델 호출 | 새 절 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13·Git 2.34.1, 2026-09-16, `PASS 06-Git-실습.ipynb: 16 cells`), verify PASS(`6 sections / 113 code cells`). 챕터 전체 게이트 6/6 PASS(`gates-wip-all.json`, G1~G7 0). 빌드 HTML 1280px·390px에서 가로 넘침 없음(scrollWidth 1280·390, SVG 3·삽화 1, 남은 `{{` 토큰 0). 챕터 index 절 목록에 06 링크. `visual.cjs` 전체 검사는 실행하지 않았습니다.

**모델 호출 수 근거**: §7-2의 「모델 호출 3~5번」은 LLM 챕터 기준입니다. Ch 3은 01~05절 모두 모델을 부르지 않고 API 키도 쓰지 않으므로(모델 호출은 Ch 6부터), 이 실습도 0번입니다. Ch 1 06·Ch 2 13 실습과 같은 판단입니다.

## 주제와 구성

- 주제: 「할인율 설정 PR 합치기」. 작성자(`Ch3 Student`)가 기능 브랜치 `feature/discount`에서 `config.txt`(`discount=10`, 04·05절 값)와 더미 키를 적은 환경 파일을 만들고, 리뷰어(`Ch3 Reviewer`)가 main에 병합합니다. 그사이 리뷰어는 main 무시 규칙에 `.venv/`를 먼저 더해 둡니다.
- 고른 절(핵심 네 개): 01 커밋·gitignore·`rm --cached`, 02 브랜치·PR 흐름(`diff --stat origin/main...HEAD`, `merge --no-ff`), 03 main 받기와 충돌 해결, 05 커밋 전 `git diff --cached` 읽기·`git add .`·`.env.local`·`log -S`. 04절(revert·reflog·worktree)과 05절 `git-filter-repo`·`--force`는 쓰지 않음 — 커밋 전에 막는 흐름이라 공개 커밋 취소나 이력 재작성이 생기지 않음(본문 b3에 적음)
- 바꾸는 값: `env_file_name` 하나(`.env` → `.env.local`, 05절 값 바꿔 보기와 같은 이름). 이름 하나가 ① 색인 비교(05) ② 규칙 더하기·색인에서 빼기(01) ③ 같은 자리 규칙 줄 충돌(03) ④ PR 변경 요약(02)으로 차례로 번지게 설계. 폴더 `run-1`/`run-2`는 두 실행의 저장소를 나누는 자리이고 조건이 아니라고 본문·노트북에 적음
- 노트북 순서(PLAYBOOK §3): 준비(`[]`) → `run_git()`에 `return result` 한 줄 더하기 → 주제 → 재료(두 폴더에 같은 팀 저장소, `for` 두 셀) → 부품 5개(`add_on_branch`·`commit_without_key`·`update_branch`·`open_pull_request`·`merge_pull_request`) → 기록 장치(`count_key_commits`, Ch 2 13 `print_report`) → 조립 `run_pull_request(run_folder, env_file_name)`(줄마다 절 주석) → 실행 1 → 실행 2 → 칸별 비교(+assert) → 작성자 폴더에 남은 환경 파일 → 정리 3줄
- 실행 1(`.env`): 색인 비교 `+++ b/config.txt`만, `Merge made by the 'ort' strategy.`, 기록장 `색인의 더미 키 | False`·`main 받기 종료 코드 | 0`·`PR 변경 요약 | 1 file changed, 1 insertion(+)`·규칙 네 줄·`더미 키 커밋 수 | 0`
- 실행 2(`.env.local`): 색인 비교 `+DEMO_API_KEY=DEMO-ONLY-NOT-A-REAL-SECRET` → `rm '.env.local'` → `CONFLICT (content): Merge conflict in .gitignore`·`종료 코드: 1` → 두 규칙 남긴 글로 해결, 기록장 `True`·`1`·`2 files changed, 2 insertions(+)`·규칙 다섯 줄·`0`
- 비교: `달라진 칸 수: 5`, `같음 | 더미 키 커밋 수 | 0`, `assert` 두 줄 통과. 마지막 셀 `!! .env.local`·`True`
- 사다리: L1~L4(Ch 2 12절까지). 셀 하나에 함수 하나, 함수 본문 10줄 이하(최대 `add_on_branch` 9문장), 코드 셀 최대 12줄. 타입힌트는 02~05절처럼 매개변수 `: str`만, 반환 자료형은 적지 않음(Ch 2에서 `-> int/str`만 가르침). 바깥 변수를 함수 안에서 읽지 않도록 더미 문자열은 함수마다 글자로 적음(Ch 2 13 판단과 같음). `upgrade_allow` 없음

## 앞 절에서 가져온 이름과 연속성 판단

- 가져온 것: 도우미 `run_git(command: str, folder: str = ".")`(05절과 같은 본문 + 끝줄 `return result`, Ch 2 04절 반환값·Ch 1 03/Ch 2 08 `.returncode`·`.stdout`), 준비 셀 `mkdtemp(prefix="ch03-06-")`, `team.git`·`author`·`reviewer`·작성자/리뷰어 이름과 전자우편, 01절 `.gitignore` 세 줄·모드 `"a"`, 커밋 메시지 앞머리 `chore:`·`feat:`·`merge:`, 02절 브랜치 이름 모양 `feature/…`, 05절 커밋 메시지 `feat: 할인율 설정 추가`·더미 문자열·`.env.local`, Ch 2 13 `print_report()`·칸별 비교 셀, Ch 2 05 `read()`·`splitlines()`, Ch 1 03 `[-1]`, Ch 1 04 `strip()`
- 새 이름: 함수 `add_on_branch`·`commit_without_key`·`update_branch`·`open_pull_request`·`merge_pull_request`·`count_key_commits`·`run_pull_request`, 값 `run_folder`·`env_file_name`·`report_1`·`report_2`, 폴더 `run-1`·`run-2`, 리뷰어 커밋 `chore: 가상환경 폴더 추적 제외`·`merge: main의 무시 규칙 받기`·`merge: 할인율 설정`. 새 Git 명령·새 옵션·새 문법 없음
- 두 이름 한 형태: 02절은 `git diff --stat origin/main...HEAD`를 작성자 폴더에서, 03절은 `git merge origin/main -m`을 썼고 이번에도 같은 모양 그대로. `git init --bare -b main run-1/team.git`처럼 경로에 폴더를 붙인 인자는 02절 `init --bare -b main team.git`의 경로만 바꾼 것
- 03절과의 차이: 03절은 사람이 충돌 표시를 읽고 기준 파일에 맞춰 새 줄을 정했음. 이번에는 충돌 자리가 무시 규칙 파일뿐이고 두 규칙이 모두 필요하므로 해결 글을 함수에 미리 적었다고 노트북 5번·본문 b7에 명시, 충돌 표시를 읽는 경우는 「실행하지 않았습니다」
- 05절과의 차이: 05절 Before는 커밋·올리기 뒤에 추적을 멈춰 검색 두 줄. 이번에는 같은 수단(규칙 더하기 + `rm --cached`)을 커밋 전에 써서 검색 0줄 — 복습 3에 연결

## 사실 주장 확인

- 실행 출력으로 확인: 노트북 전체 출력(위). 프로토타입(`/tmp/p06/proto.py`, 연결 폴더 밖)과 새 커널 실행 두 번(생성 직후, mdpatch 뒤 전체 재실행)에서 기록장 값이 같음. 커밋 해시와 임시 경로는 인용하지 않음
- 「종료 코드가 0이 아니면 모두 충돌로 봄」, 넓힌 규칙 `.env*`, 받아 오기 실패, GitHub PR 화면, Windows·macOS는 실행하지 않았다고 b7에 적음
- 뒤 챕터 연결: 05 b8에 있던 확인한 사실(Ch 4 첫 절 Pandas, 이 챕터 임시 저장소는 쓰지 않음, Ch 6 `.env`의 `OPENAI_API_KEY`, Ch 32 05절 시크릿)을 06 b8로 옮김

## 그림

- Mermaid 3장(PNG 직접 확인): 06-1 조립도(flowchart TB 7노드, 원본 폭 266px. 첫 렌더에서 `rm --cached`가 어색하게 줄바꿈되어 `<br>` 위치 조정), 06-2 실행 1 순서(sequenceDiagram 참여자 셋, 760px. 둘째 메모에 넣은 `Merge made by the 'ort' strategy.`가 상자 밖으로 넘쳐 「충돌 없이 병합」으로 줄임), 06-3 두 실행 비교(flowchart TB 두 칸, 860px)
- 삽화 1장: 06-4 열쇠를 뺀 상자(01-5 택배 상자·02-6 검수대와 선반·05-5 열쇠를 이어 씀). nano_banana_pro 16:9 2k, 2회 생성(탈락 1), 4크레딧. 채택 job d86a7698-5b2e-4e70-8c8c-b903755eb1b9, 탈락 job 815c3cbe-5bbd-4398-8a55-426d3ca920c5(열쇠 두 번·가운데 상자 둘)
- 색(§5-3): 조립한 함수 파랑, 바꾸는 값 초록, 기록장·확인 출력 노랑, 실행 1의 「막을 것·충돌 없음」 회색. 실행 2의 병합 충돌(종료 코드 1)과 색인에서 찾은 더미 키는 코드가 받아 처리하고 기록한 일이라 노랑(셀은 멈추지 않음). 이 절 그림에 빨강 없음. 근거는 `06-figures.md`

## 바꾼 다른 파일

- `chapter.json` sections 끝에 `06-Git-실습`(「Git 실습: 할인율 설정 PR 합치기」, experiment) 추가
- `_src/05-시크릿-이력-정리와-예방.html` b8 「다음 학습과 이어지는 지점」 → 06절 링크와 실습 소개 네 문장(Ch 4·Ch 6·Ch 32 문장은 06 b8로 옮김). 05 노트북·`author_05.py` 정리 셀 끝 「다음 챕터 Ch 4에서는 …」 → 「다음 06절은 이 챕터의 실습입니다. …」. `mdpatch.py`로 재실행 없이 고치고 `run_section.sh … 05 --no-exec` 게이트 0건(첫 문장이 70자를 넘어 한 번 더 줄임)
- `_src/index.html`: 이 챕터에는 없음(`_build.py`가 `_src/index.html`을 쓰지 않고, 빌더가 `chapter.json`으로 절 목록을 만듦). 빌드한 `index.html` 절 목록에 06이 들어간 것을 확인. 노트북 개수를 적은 문장도 챕터 안에는 없음
- 챕터 밖(고치지 않음): `textbook/part1/_build_index.py` CHAPTERS의 Ch 3 절 수 5와 `textbook/part1/index.html` 목록(Ch 1·2 실습 절도 반영되지 않은 상태), `textbook/downloads/` 챕터 묶음

## 검토에서 볼 곳

- 한 셀 출력이 긴 곳: 재료 두 셀(폴더 두 벌)과 실행 1·2 셀(명령 약 15개씩). 결과 읽기가 볼 줄을 짚지만 30분 분량과 읽기 부담이 맞는지
- 충돌 해결 글을 함수에 미리 적은 판단(03절의 「표시를 읽고 정함」과 어긋나 보이지 않는지, 노트북 5번·b7), 실행 2 충돌을 노랑으로 둔 색 판단(06-3)
- 폴더 `run-1`/`run-2`를 함께 바꾼 것이 「값 하나만」 원칙에 어긋나 보이지 않는지(노트북 10번·b4 「두 번의 실행」)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept(중 0, 하 4, 공통 C-2·C-3). 모두 반영했습니다. 결정 Q3대로 실행 2 충돌 노랑과 `run-1`/`run-2` 폴더는 유지했습니다.
- 06-1: 06-3 도식 읽기 「실행 1의 왼쪽 두 회색 상자」·「실행 2의 왼쪽 두 노란 상자」, 캡션 「실행 2는 앞의 두 단계에서」(본문 토큰·caption.md·설계표 색 열)
- 06-2: 06-1 도식 읽기 「파란 상자는 이 절에서 만든 함수입니다. 상자 안에는 쓰는 절과, 적는 기록장 칸(「칸:」으로 시작하는 줄)을 함께 적었습니다.」 노트북 오늘 볼 그림은 이미 같은 뜻이라 그대로
- 06-3: `commit_without_key(run_folder: str, env_file_name: str, key_found: bool)`로 타입힌트를 맞추고, 설명 셀에 「매개변수 `key_found` 옆의 `bool`은 Ch 2 01절에서 배운 불리언 자료형으로, 값이 `True`나 `False`라는 표시입니다. Ch 2 07절에서 본 것처럼 타입힌트는 값을 검사하지 않습니다.」 출력은 반영 전과 같음
- 06-4: b8 「그때도 이 실습처럼 … 확인하길 권합니다.」, `chapter-summary.md` 「다음 챕터가 이어받을 것」에 Ch 6 01절 `.gitignore` 확인 문장 검토를 적음
- C-2·C-3: `06-2-실행1-순서.mmd`에 `messageAlign: left`, 자기 메시지 라벨을 한 줄(`switch -c, git add .`, `merge --no-ff`)로 줄이고 전체 명령은 도식 읽기에 적음. 도식 읽기 「가로 실선은 요청한 명령, 점선은 받아 온 결과입니다.」(PNG 확인, viewBox 819)
- 코드 셀 16, 검사한 문장 339

재실행: `run_section.sh … 06`(새 커널 PASS) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 112 code cells (max 18 lines)`, `visual.cjs` 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.
