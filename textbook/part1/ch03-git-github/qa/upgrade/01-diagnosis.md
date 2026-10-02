# 01-커밋과-gitignore — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/01-commit-ignore.*`, `_gen_figures.py`).
생성기: `qa/upgrade/author_01.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch03-git-github 01`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 9 | 0 |
| G6 | 32 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 19 (준비 1 + 본문 18) |
| 검사한 문장 | 117 | 345 (연속성 보정 전 296) |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Git 2.34.1, 2026-09-16), verify PASS(챕터 5절 43셀).

## 수정 전 주요 문제

- G1: 준비 셀 하나에 `git(*args, cwd=..., check=...)`와 `configure()` 함수 두 개, `*args` 정의, `cwd or root` 식
- 코드 모양: 한 셀에 add·commit·status·log를 몰아 실행(셀 5·7·9는 명령 8~10개), 긴 인자 줄바꿈, `assert A and not B`
- G5: 제목 셀·오늘 볼 그림 없음, 코드 셀 뒤 결과 읽기 셀이 출력 값을 인용하지 않음
- G6: 영문·코드 이름+조사로 시작하는 문장 26개(「`git diff`는」, 「`.gitignore`는」, 「Git의」 등), 70자 초과 4개, 5문장 넘는 단락 2개
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 Excalidraw 도식 1장
- 내용: 본문의 「add 뒤 다시 고치면 색인에는 2건이 남는다」, `git diff --cached` 설명은 노트북에서 실행하지 않은 동작. `status`의 두 칸 의미를 설명하지 않음

## 바꾼 것

- git 실행 방식 통일: 모든 git 명령을 `run_git("명령")` 함수 하나로 실행(`shlex.split` + `subprocess.run`). 출력은 터미널처럼 `$ git 명령` 다음 줄에 결과, 0이 아닌 종료 코드만 표시. `!git`은 `verify.py`가 코드 셀을 `ast.parse`하므로(`%` 줄만 제외) 쓰지 않음
- 노트북: 제목(API 키 불필요·호출 0번·1분 이내) → 오늘 볼 그림 → 준비(import) → 함수 → 버전 → 임시 저장소 → 로컬 작성자 설정 → 파일 세 개와 `status --short --ignored` → `.gitignore` 첫 커밋 → `app.py` 두 번째 커밋·log → 값 바꿔 보기(2건→3건: ` M`/`git diff` → `M `/빈 `git diff`/`git diff --cached` → fix 커밋) → Before(`debug.log` 커밋 → `*.log` 추가 → ` M debug.log`, `check-ignore` 종료 코드 1) → After(`rm --cached` → 커밋 → 빈 `ls-files`·`.gitignore:3:*.log`·빈 status → `git show HEAD~1:debug.log`로 지난 커밋 내용 `first run` 확인) → 정리
- 기존 학습 질문·데이터(orders, 주문 2→3건, `.env` `APP_MODE=demo`, `debug.log`)와 paired 형식 유지. 커밋 해시·임시 경로는 결과 읽기에서 인용하지 않음
- 본문 10블록 전체를 다시 씀. 용어 7개 표, 상태 표시 표(노트북에 나온 줄), 「이 절의 질문」, 복습 5문항. 「팀원 작업 폴더에서 지워질 수 있음」과 다른 운영체제는 「이번에 실행하지 않았습니다」로 적음
- 그림: Mermaid 4장(세 자리, 목적별 커밋, diff 두 비교, 추적 해제 Before/After) + 삽화 1장(택배 상자). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 참고 자료: git-check-ignore(추적 파일은 제외 규칙 대상 아님, 종료 코드 0/1), git-status 짧은 형식(X=색인, Y=작업 폴더)을 2026-09-16 공식 문서로 확인

## 연속성 보정 (2026-09-16, Ch 1·Ch 2 chapter-summary 확정 뒤)

01절은 Ch 2 마감 전에 먼저 개선했으므로, 두 챕터 요약과 Ch 1 05절·Ch 2 05·07·08절 생성기를 대조해 다시 고쳤습니다. 게이트는 보정 뒤에도 G1~G7 0, 새 커널 PASS, verify PASS(5절 43셀)입니다. 코드 셀 수(19)와 그림 5장은 그대로입니다.

| 대조 항목 | 보정 전 | 보정 뒤 |
|---|---|---|
| 준비 셀 모양 | import 5줄만(`os`·`shlex`·`subprocess`·`tempfile`·`pathlib.Path`), 저장소 폴더는 3절에서 `mkdtemp(prefix="git-lesson-")`+`Path(...) / "orders"`+`mkdir()` | Ch 2 08절과 같은 준비 셀: `import os`·`tempfile` → `mkdtemp(prefix="ch03-01-")` → `os.chdir()` → `os.listdir()` 출력 `[]`. 임시 폴더 자체를 저장소로 씀(`orders` 하위 폴더 없음), `git init` 뒤 `['.git']` 출력 |
| 배우지 않은 문법 | `pathlib.Path`(Ch 2 요약 「Ch 1에서만 씀」)·`write_text()`·`Path.cwd().name`·`exists()`, 타입힌트 `-> None`(Ch 2 기본 경로는 `-> int/str`만), 목록 이어 붙이기 `["git"] + arguments` | `Path` 전부 제거. 반환 표시 `->` 생략(Ch 2 09절 선례)과 이유 한 문장. 명령은 글 `"git " + command`로 만든 뒤 `shlex.split()`. 글자 사이 `+`는 설명 셀에서 한 문장으로 풂 |
| 파일 쓰기 | `Path(...).write_text()`와 Before의 `with open(..., "a") as ignore_file` 두 방식 섞임 | 모두 Ch 2 05절 `with open(..., "w"/"a", encoding="utf-8") as file:` + `write()`. 두 줄 `.gitignore`는 `"""…"""`(Ch 1 04절), 한 줄 글의 `\n`은 Ch 1 03절 줄바꿈이라고 적음. 모드 `"a"`는 「Ch 2 05절에서 실행하지 않은 모드」로 연결 |
| `subprocess.run` 설명 | 「Ch 2 08절에서 쓴 `subprocess.run()`」 한 문장, 인자 `encoding="utf-8"`의 이유 없음 | 「뼈대는 Ch 2 08절 `run_pytest()`와 같음」 + 달라진 세 곳(`"git "` 붙이기, `shlex.split()`, `text=True` 대신 `encoding="utf-8"`). `text=True`는 기본 규칙으로 읽어 한글이 깨질 수 있다는 이유, 다른 운영체제는 실행 안 함 |
| Ch 1 05절과 겹치는 설명 | `??`·`A`·`M`·`git diff`·커밋을 처음 배우는 것처럼 정의. 작성자 `Git Learner`·`learner@example.invalid` | 「Ch 1 05절의 기록할 목록 = 색인」, 「처음 보는 파일 = `??`」, 「앞 빈칸을 떼어 내 한 글자만 읽었고 이번에는 두 칸」, 커밋 뜻을 색인 기준으로 넓힘, `git init`에 `-b main`을 더함, `-c` → `git config`(Ch 1 05절이 「Ch 3에서 배움」으로 미룬 약속), 주문 2→3건을 `hello.py` 수량 2→3 실험과 연결, `git add` 뒤 빈 `git diff`는 Ch 1 05절에서 기기 셸로만 본 장면이라고 적음. 작성자 `Ch3 Student`·`student@example.com`(Ch 1 05절 `Ch1 Student` 규칙) |
| 규격 변경분 | — | §2-2 A 트랙: `@`·`BaseModel`·픽스처 없음(해당 없음). §2-3 import: Ch 3은 Ch 2 07절 뒤라 L4로 허용되므로 `upgrade_allow=["stdlib-import"]`를 쓰지 않고 「Ch 2 07절에서 배운 import 문」으로 설명(환경 챕터 예외 문장 「자세한 뜻은 Ch 2에서」는 Ch 3에서 사실과 달라 쓰지 않음). §2-4 클래스 셀 없음. §5-3 오류 색: 01-4 Before 결과(`M debug.log`·종료 코드 1) 빨강은 Before 결함 결과, After 노랑 — 그대로 맞음 |
| 본문 `_src` | 「앞에서 배운 내용」이 Ch 1 05절을 「Git 설치 확인」으로만 요약 | 「앞에서 배운 내용」 4단락 재작성(Ch 1 05 init/add/commit·`-c`·상태 표시·diff, Ch 2 05 `with open`, Ch 2 08 `run_pytest()`·준비 셀). 용어 표 저장소·색인·커밋, 상태 표 앞 설명, 실행 예제의 `orders` 문장과 `run_git()` 설명 |

그림(Mermaid 4장·삽화 1장)의 라벨은 커밋 메시지·상태 줄·요약 줄만 담아 보정의 영향을 받지 않았습니다. 재실행 출력에서 인용 값(`1 file changed`, `1 insertion(+), 1 deletion(-)`, `2 files changed`, `.gitignore:3:*.log`, `first run`, `True`)이 같음을 확인했습니다. 삽화의 택배 상자는 Ch 2 02절 「택배 상자 분류대」(조건문)와 물건이 겹치지만 챕터가 다르고 역할(책상·열린 상자·봉한 상자)이 달라 유지했습니다.

## 검토에서 볼 곳

- 삽화: 프롬프트와 달리 책상에도 같은 책이 남음. `git add` 뒤에도 파일이 작업 폴더에 남는 동작과 맞아 채택하고 「그림 읽기」에 그렇게 적음
- 상태 표 「첫 칸은 색인의 변화」는 공식 문서의 X(색인 대 HEAD)를 줄여 쓴 표현
- 교재 출력은 Linux Git 2.34.1. 이전 판은 macOS Git 2.50.1로 적혀 있었음. Windows에서 `shlex.split`·UTF-8 커밋 메시지는 실행하지 않음
- 연속성 보정: `run_git()` 설명 셀의 `text=True`와 `encoding="utf-8"` 비교 문장, 준비 셀이 저장소 폴더를 겸하는 구성(`orders` 하위 폴더를 뺀 것), 작성자 `Ch3 Student`

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 0, 하 3, 공통 C-1 중을 이 절 준비물에 반영). 모두 반영했습니다.
- C-1(중, 챕터 공통): 노트북 준비물 아래 「**기준 Git 버전** — Git은 2.28 이상이 필요합니다. 교재 출력은 Git 2.34.1로 만들었고, 새 버전에서는 안내 문구가 조금 다를 수 있습니다.」
- 01-1: 준비 설명 「코드의 import 두 줄은 Ch 2 07절에서 배운 import 문입니다. 표준 라이브러리 모듈 os와 tempfile을 불러옵니다.」(한 문장은 G6 70자를 넘어 둘로 나눔)
- 01-2: 복습 5 질문을 「추적을 멈춘 로그 파일의 내용이 … 그 파일에 비밀 값이 들어 있었다면 어떨까요?」로, 해설 끝을 「비밀 값이 든 파일도 같아서, 기록에서 지우는 절차는 05절에서 따로 확인합니다.」로
- 01-3: `01-2-목적별-커밋.mmd`의 노란 상자를 「상태 표시 !! .env / 파일은 작업 폴더에만 있음」으로, 도식 읽기 「오른쪽 노란 상자는 환경 설정 파일의 상태 표시 `!! .env`이고, 이 파일은 작업 폴더에만 있습니다.」(PNG 확인, 01-1과 같이 파일 회색·상태 표시 노랑)
- 코드 셀 19, 검사한 문장 349. 출력은 반영 전과 같음(해시·임시 경로 제외 비교)

재실행: `run_section.sh … 01`(새 커널 PASS) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 112 code cells (max 18 lines)`, `visual.cjs` 7페이지 × 1280·390px 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/01-커밋과-gitignore.md`
- 루트 `textbook/qa/upgrade-progress.md` 표는 챕터 밖 파일이라 이 작업에서 고치지 않음
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
