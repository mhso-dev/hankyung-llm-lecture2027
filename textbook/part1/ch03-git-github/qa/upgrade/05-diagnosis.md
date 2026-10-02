# 05-시크릿-이력-정리와-예방 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/05-secret-response.*`).
생성기: `qa/upgrade/author_05.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch03-git-github 05`.
이어짐 기준: Ch 1·Ch 2 `chapter-summary.md`, 01~04절 완료본(`_src`, 노트북, `author_01.py`~`author_04.py`, `01`~`04-diagnosis.md`), `handoff.md` §04 → §05.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 7 | 0 |
| G2 | 1 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 8 | 0 |
| G6 | 34 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 17 (준비 1 + 본문 16) |
| 검사한 문장 | 131 | 360 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Git 2.34.1, git-filter-repo 2.47.0, 2026-09-16), verify PASS(챕터 5절 97셀).

## 04절 메모 확인 — git이 `filter-repo`를 찾는가 (실제 실행)

- 기기 `/tmp`에서 같은 가상환경으로 따로 실행(2026-09-16):
  - `uv run --project labs/part1/ch03-git-github python` 안에서 `subprocess.run(["git", "filter-repo", "--version"])` → 종료 코드 0(`a40bce548d2c`). `uv run`이 PATH 앞에 `/tmp/venv-ch03-git-github/bin`을 넣기 때문. 교재 실행 도구(`execute.py`)도 `uv run` 안에서 커널을 띄우므로 여기서는 찾음.
  - 가상환경 Python을 직접 실행(활성화 없음) → `git: 'filter-repo' is not a git command. See 'git --help'.`, 종료 코드 1.
  - 같은 조건에서 `[sys.executable, "-m", "git_filter_repo", "--version"]` → 종료 코드 0.
- 결론: `run_git("filter-repo …")`는 커널 PATH에 따라 달라짐. 학생 VS Code 커널의 PATH는 확인할 수 없어(실행 안 함) 노트북은 `run_filter_repo(options, folder)`로 `sys.executable -m git_filter_repo`를 실행. 뼈대는 02절 `run_python()`, `-m`은 Ch 2 08절 `run_pytest()`, 목록 붙이기는 Ch 2 03절 `for`+`append()`(목록 `+`는 미교육이라 쓰지 않음). 근거: git-filter-repo INSTALL.md(「PATH에 두면 `python3 git-filter-repo`를 `git filter-repo`로 줄여 부를 수 있음」, Windows 메모의 긴 모양 실행).
- 추가 발견 1: GitHub 문서 절차의 `--sensitive-data-removal`은 Git 2.34.1에서 `error: unknown option 'batch-command'` + Traceback(AssertionError), 종료 코드 1로 멈춤(`git cat-file --batch-command`가 없음). git-filter-repo README 요구 사항은 Git 2.36.0 이상. 그래서 노트북은 이 옵션 없이 `--invert-paths --path .env.local`만 씀(2.34.1에서 끝까지 실행됨). 본문 주의 메모에 「교재 실행 환경에서 따로 실행하니 멈춤, 설명서는 2.36.0 이상 요구」로 적음.
- 추가 발견 2: 옵션 없는 실행은 원격 이름 origin을 지움(`NOTICE: Removing 'origin' remote`, 설명서 「Why is my origin removed?」). 그래서 `git remote add origin ../team.git` 뒤 `git push --force origin main`. `--sensitive-data-removal`을 쓰면 origin을 남기므로(소스 확인) 학생이 새 Git에서 옵션을 더하면 `remote add`가 실패할 수 있음 — 실행 안 함, 본문에 쓰지 않음.
- 같은 컴퓨터 폴더 복제는 설명서 권고대로 `git clone --no-local`(설명서 FRESH CLONE 절: 로컬 복제는 `--force`보다 `--no-local`). 작은 저장소에서는 일반 `git clone`도 안전 검사를 통과했으나(따로 확인) 설명서 권고를 따름.

## 수정 전 주요 문제

- G1: 준비 셀 하나에 `git(*args, cwd=..., check=...)`·`configure()` 두 함수와 `*args` 정의, 수정 셀의 `any(line.endswith(" .env") for …)` 제너레이터 식 3곳, `len(…) if … else 0` 조건 표현식 2곳
- G2: 수정 셀 20줄 초과
- 배우지 않은 모양: `TemporaryDirectory`·`Path`·`write_text`·`exists()`, 대문자 `DUMMY`와 f-string, `rev-parse HEAD`로 해시를 변수에 담아 `f"{leak_commit}:.env"`, `subprocess.run(["git", "filter-repo", …], check=True)` 직접 호출, `clone --mirror`·`push --force --mirror`·`rev-list --objects --all`·`log -S … --format=%H`, `git add -f`·`check-ignore -q`·`diff --cached -- 파일`, `assert` 여러 줄
- 이어짐: 작성자 `Git Learner`, 원격 `secret-remote.git`·저장소 `secret-demo`(02~04는 `team.git`·`author`), `--initial-branch=main`(02~04는 `-b main`), 첫 설명 셀이 01절의 작업 폴더·색인·커밋·HEAD·브랜치를 처음처럼 다시 정의, 리뷰어(이미 받은 사람)가 없어 「팀원 조치」가 실행으로 드러나지 않음
- 내용: 실패 장면이 `git add -f`로 무시 규칙을 일부러 우회(실제 유출 원인과 거리), 값 바꿔 보기가 제목만 있고 실제로 값을 바꾸지 않음, 「다음 학습」이 없는 Ch 38·「후반 AI 페어 개발」과 Ch 4 내용(CSV·JSON·API 함수)을 사실과 다르게 적음
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기 셀 없음. G6: 70자 초과 11곳, 코드 이름+조사 시작 13곳, 5문장 넘는 단락 등. G7: Mermaid 0장, 삽화 0장, 설계표 없음(Excalidraw 1장)

## 바꾼 것

- 학습 질문·더미 값·형식 유지: paired, `DEMO-ONLY-NOT-A-REAL-SECRET`, 「파일을 치워도 지난 커밋에 남음 → 이력 재작성 → 검사 범위」. 경로 `.env` → `.env.local`(값 바꿔 보기에서 무시 규칙이 막지 못한 이름이 Before의 유출 원인이 되도록 이음)
- 04절을 이어 씀: 준비 셀 `mkdtemp(prefix="ch03-05-")`, `run_git()` 같은 모양, `team.git`·`author`(`Ch3 Student`)·`reviewer`, 해시 대신 `HEAD~1`, `config.txt` `discount=10`(04절 값), 01절 무시 규칙 세 줄·`git rm --cached`·모드 `"a"`, 02절 `fetch`·`branch -vv`, 03절 갈라진 이력 읽기
- 예방(example): `.env` → `!! .env`·`.gitignore:1:.env`, `settings.example` `replace-me` + 커밋 전 `git diff --cached`(`+DEMO_API_KEY=replace-me`)
- 값 하나 바꿔 보기(실행): 파일 이름만 `.env.local` → `?? .env.local`, `check-ignore -v` `종료 코드: 1`
- Before: `git add .`(01절에서 이름만)로 `A  .env.local` 커밋·올리기 → 리뷰어 복제(파일 목록에 `.env.local`) → 01절 방법으로 추적 해제 → `git log --oneline --all -S 더미 키` 두 줄, `git show HEAD~1:.env.local` 값 보임
- After: 폐기·교체는 「이번에 실행하지 않았습니다」로 먼저 적음 → `run_filter_repo()` 정의 → `clone --no-local` + `--invert-paths --path .env.local`(`Parsed 4 commits`) → 새 이력 검색 빈 출력·해시 바뀜 → `remote add` + `push --force origin main`(`(forced update)`) → 리뷰어 옛 복제본 `ahead 1, behind 2`·검색 한 줄 → `reviewer-new` 다시 복제, 검색 빈 출력·`.env.local` 없음. `assert` 대신 출력으로 읽음
- 본문 10블록 전체 재작성. 용어 6개(시크릿·폐기와 교체·이력 재작성·git-filter-repo·강제 올리기·글자 검색), 복습 5문항(5번이 이 절의 질문). 실행하지 않은 것(폐기·교체, 옛 복제본에서 받아 합친 뒤 올리기, GitHub 포크·캐시·PR, `--sensitive-data-removal`, 도구가 복제본을 거부하는 경우, VS Code 커널 PATH, 커밋 전 검사 도구·푸시 보호, Windows·macOS)은 주의 메모에 문서 근거와 함께 적음
- 「다음 학습」: 06 실습 절 링크는 다음 단계 몫이라 Ch 4를 가리키는 자리를 유지하고, 확인한 사실만 남김(Ch 4 첫 절 Pandas 표 — chapter.json, Ch 6 01 `.env`의 `OPENAI_API_KEY` — `_src/01`, Ch 32 05 Compose 시크릿 — `_src/05`). 없는 Ch 38·AI 페어 개발 문장과 Ch 4 CSV·JSON·API 설명은 뺌
- 그림: Mermaid 4장(추적 해제와 다시 쓴 이력, 무시 규칙과 비교 읽기, 다시 쓴 이력 퍼뜨리기 sequenceDiagram, 대응 순서) + 삽화 1장(자물쇠와 다시 싼 상자, 04-6 팀 선반을 이어 씀). Excalidraw `05-secret-response`는 05-4로 바꾸고 본문에서 뺌(파일은 삭제하지 않음)
- 참고 자료: GitHub Docs 민감 정보 제거·푸시 보호, git-filter-repo 설명서·INSTALL.md·README 요구 사항, git-log(-S, --all)·git-push(--force)·git-clone(--no-local)·gitignore — 2026-09-16 확인

## 검토에서 볼 곳

- `run_filter_repo()`로 모듈을 직접 실행한 선택(위 「04절 메모 확인」). 출력 줄은 `$ python -m git_filter_repo …`이고, 본문은 터미널의 `git filter-repo`와 같은 옵션이라고 적음
- `--sensitive-data-removal`을 빼고 GitHub 문서 절차와 다르게 실행한 점과 그 설명(주의 메모). 교재 실행 Git 2.34.1이 도구 요구 사항(2.36.0)보다 낮음 — 챕터 전체 실행 환경 결정 대상
- 05-2의 `?? .env.local`·`종료 코드: 1`을 빨강(막지 못한 결과, 0이 아닌 종료 코드)으로 둔 것. 05-3 sequenceDiagram의 자기 메시지 `git filter-repo`와 `git clone` 글자가 세로선에 조금 겹침(04-2와 같은 정도)
- 삽화 05-5: 2회차 채택. 두 칸 사이 흰 틈이 뚜렷하지 않고, 수레 상자가 셋(내리는 상자 포함)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 1, 하 3, 공통 C-1·C-2·C-3·C-5). 모두 반영했습니다. 결정 Q2대로 `run_filter_repo()`와 `--sensitive-data-removal` 제외는 유지했습니다.
- 05-1(중) 삽화 05-5: 채택 job `7bc1a6fa-087c-472c-9273-023b5dc5beea`와 탈락 job `fd474ddb-e478-4947-95ed-8cf7d2abaeaf`의 결과를 Higgsfield `show_generation_by_ids`로 다시 받아(새 생성 없음) 1100px로 줄여 저장본과 픽셀 비교했습니다. 저장본은 탈락본과 평균 차이 0.0, 채택본과 29.3이라 **탈락본이 저장돼 있었습니다**. 채택본을 열어 선반 상자 넷, 첫째·둘째 갈색 테이프, 셋째 열린 상자의 초록 띠와 꺼내는 열쇠, 넷째 초록 테이프, 수레 위 상자에서 삐져나온 열쇠, 바닥의 옛 자물쇠 하나와 열쇠를 확인하고 폭 1100px(1100×614)로 교체했습니다. 본문 그림 읽기·alt·캡션과 검수 메모가 채택본과 맞으므로 글은 고치지 않았습니다. prompt.md 상태 줄에 기록. 추가 크레딧 0
- C-1(중, 챕터 공통): 준비물 아래 「**기준 Git 버전** — Git은 2.28 이상이 필요하고, 교재 출력은 Git 2.34.1로 만들었습니다. 이력 정리 도구 설명서는 Git 2.36.0 이상을 요구 사항으로 적어 두었으므로, 새로 설치한다면 2.36 이상을 권합니다. 이 노트북이 쓰는 옵션은 Git 2.34.1에서도 끝까지 실행됐습니다.」
- 05-2: 주의 메모 여섯째 항목 끝 「도구 소스를 보면 이 옵션은 원격 이름 origin을 지우지 않습니다. 그래서 노트북의 `git remote add` 단계가 필요 없고, 이 경우는 실행하지 않았습니다.」(검토 세션의 소스 확인이 근거)
- 05-3: 학습 목표 둘째 항목 「이력 정리 도구 `git-filter-repo`로 새 복제본의 이력에서 경로를 빼고 …」
- 05-4: 「다음 학습과 이어지는 지점」 첫 문장 앞에 「이 절에서 본 것처럼 올린 뒤에 치우려면 폐기·교체와 팀원 다시 복제까지 해야 합니다.」, 둘째 문장 「그래서 06절 Git 실습에서는 커밋 전 비교 읽기를 할인율 설정 PR 흐름에 넣어, 더미 키를 커밋하기 전에 막습니다.」
- C-2·C-3: `05-3-다시-쓴-이력-퍼뜨리기.mmd`에 점선 응답 `옛 이력 4커밋`(작성자 새 복제본)·`새 이력`(리뷰어 새 복제본)을 더하고 `messageAlign: left`로 `git filter-repo`·`git clone` 라벨 겹침을 없앰. `visual.cjs` 기준(viewBox 928 → 13.1px)을 맞추려고 `actorMargin: 30`, 작성자 메모 「.env.local을 뺀 새 이력」으로 줄여 851(PNG 확인). 도식 읽기에 「실선 화살표는 요청한 명령, 점선 화살표는 받아 온 결과입니다.」
- 코드 셀 17, 검사한 문장 366

재실행: `run_section.sh … 05`(새 커널 PASS) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 112 code cells (max 18 lines)`, `visual.cjs` 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 06 실습 절 추가 뒤 05 「다음 학습과 이어지는 지점」과 노트북 끝 문장을 실습 절로 고침(`handoff.md` §05 → 실습)
- 리뷰 묶음: `qa/upgrade/review-pack/05-시크릿-이력-정리와-예방.md`
- 루트 `textbook/qa/upgrade-progress.md` 표는 챕터 밖 파일이라 이 작업에서 고치지 않음
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
