# 02-GitHub-Flow와-PR-리뷰 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/02-flow-review.*`).
생성기: `qa/upgrade/author_02.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch03-git-github 02`.
이어짐 기준: Ch 1·Ch 2 `chapter-summary.md`, 01절 완료본(`_src/01-*`, 노트북, `author_01.py`, `01-diagnosis.md`), `handoff.md` §01 → §02.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 2 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 8 | 0 |
| G6 | 31 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 23 (준비 1 + 본문 22) |
| 검사한 문장 | 122 | 444 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Git 2.34.1, 2026-09-16), verify PASS(챕터 5절 60셀).

## 수정 전 주요 문제

- G1: 준비 셀 하나에 `git(*args, cwd=..., check=...)`와 `configure()` 두 함수, `*args` 정의(Ch 2 09절, A 트랙 미교육), `Path | None`·`cwd or root`
- G2: `read_text().replace().replace()` 세 번 연결, 마지막 셀 20줄(수정·커밋·push·fetch·merge·push·log·실행·assert 둘)
- 배우지 않은 문법: `isinstance()`·`raise TypeError`(Ch 1·2 요약 어디에도 없음, Ch 2 요약 「아직 가르치지 않은 것」에 `raise`), `subprocess.check_output`, `sys.executable -c`, `pathlib.Path`·`write_text`·`mkdir`, `assert A and B`
- 이어짐: 작성자 `Git Learner`·`learner@example.invalid`(01절은 `Ch3 Student`), `TemporaryDirectory(prefix="git-lesson-")`(01절은 `mkdtemp(prefix="ch03-01-")`+`chdir`), 01절 `run_git()`을 쓰지 않음. 첫 설명 셀이 01절에서 이미 배운 작업 폴더·색인·커밋·HEAD를 처음 배우는 것처럼 다시 정의
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기 셀이 출력 값을 인용하지 않음, 준비 셀 뒤 설명 없음
- G6: 70자 초과 14개(용어 정의 한 문장에 정보 3~4개), 영문·코드 이름+조사 시작 16개(「`origin`은」, 「`--no-ff`는」, 「Git은」 등)
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. Excalidraw 도식 1장
- 내용: 병합 커밋의 부모 둘, `origin/main`이 fetch로만 바뀐다는 점을 출력으로 보여 주지 않음(`assert`로만 확인). PR 템플릿을 `.github/`에 두어 `mkdir` 필요

## 바꾼 것

- 학습 질문·데이터·형식 유지: paired, `summarize(count)` → `주문 {count}건`, 빈 글자 입력 결함, bare 원격 `team.git`, 기능 브랜치 `feature/order-summary`, `--no-ff` 병합, `merge: 주문 요약`
- 입력 확인을 배운 문법으로 교체: `isinstance`+`raise TypeError` → Ch 2 01절 형 변환 `number = int(count)`(빈 글자면 `ValueError`). 결함 관찰은 리뷰어의 확인 파일 `check_summary.py`(Ch 2 07절 `from summary import summarize`, 05절 `try`/`except ValueError as error`)로 Before·After에 똑같이 실행. Ch 2 05절 결론 「틀린 값을 빈 결과로 감추지 않음」과 13절 오류 글 `invalid literal for int() with base 10`에 연결
- 01절 도우미를 이어 씀: `run_git(command: str, folder: str = ".")`로 같은 이름 재정의(Ch 2 04절 기본값 매개변수, Ch 1 05절 `cwd=`), 출력 첫 줄 `author $ git …`. 파이썬 파일 실행은 Ch 2 08절 `run_pytest()` 모양의 `run_python(file_name, folder)`(`sys.executable`, `text=True`) — 정의 셀 각각 하나
- 준비 셀: 01절과 같은 `mkdtemp(prefix="ch03-02-")`+`os.chdir()`+`os.listdir()` `[]`. 파일 쓰기는 모두 `with open(…, "w"/"r", encoding="utf-8")`. 작성자 `Ch3 Student`·`student@example.com`, 리뷰어 `Ch3 Reviewer`·`reviewer@example.com`
- 노트북 흐름: 제목 → 오늘 볼 그림(02-1) → 준비 → 함수 재정의 → bare 원격 → 작성자 clone·`remote -v` → config → 첫 커밋(`.gitignore` `__pycache__/` + 루트 `pull_request_template.md`) → `push -u origin main` → `switch -c`·`branch` → feat 커밋·`branch -v` → `push -u`·`branch -vv` → `diff --stat origin/main...HEAD` → 템플릿 `replace()` 한 번으로 PR 설명 → 리뷰어 clone·config·`sorted(os.listdir())` → 값 하나 바꿔 보기(브랜치 main → 기능 브랜치, `summary.py` 나타남) → Before(`diff origin/main...HEAD`, `run_python` 정의, 확인 파일 `빈 값: 주문 건`, 리뷰 의견) → After(fix 커밋·push, reviewer fetch `behind 1`, `switch main`·`merge --no-ff`, 확인 파일 `입력 오류`, `branch -vv` `ahead 3` → push → `[origin/main]`·`log --graph`, 작성자 fetch·`log -1 origin/main`) → 정리
- `assert`로만 확인하던 `HEAD == origin/main`을 `git branch -vv` 짝 표시 전후 비교와 작성자 저장소 확인으로 바꿈(출력으로 읽음)
- 본문 10블록 전체 재작성. 용어 7개 표(원격 저장소·bare 저장소·브랜치·기능 브랜치·PR·코드 리뷰·병합 커밋), GitHub Flow 여섯 단계(공식 문서 2026-09-16 확인, 6번 브랜치 삭제는 실행 안 함), 점 세 개 비교(공식 문서 확인, main이 먼저 움직인 경우는 실행 안 함), 복습 5문항(5번이 「이 절의 질문」에 답함)
- 그림: Mermaid 5장(세 저장소, 브랜치 두 줄기, 주고받는 순서, 확인 결과 비교, 병합 이력) + 삽화 1장(검수대와 선반, 01-5 택배 상자 이어 씀). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 참고 자료: GitHub flow(여섯 단계·병합 뒤 브랜치 삭제), PR 템플릿(루트 위치 가능, 기본 브랜치에 있어야 채워짐), git-merge(`--no-ff`), git-fetch(원격 추적 브랜치만 갱신), git-diff(`A...B` = merge-base부터 B) — 2026-09-16 확인. PR 리뷰 문서는 이전 판 확인일 2026-09-09 유지

## 검토에서 볼 곳

- `run_python()`의 `text=True` 설명 「새 Python은 기본 규칙으로 내보내므로 받는 쪽도 같은 규칙」: `run_git()`의 `encoding="utf-8"`과 다른 이유. Linux에서만 실행했고 Windows(cp949) 동작은 확인 안 함
- 고친 함수가 빈 글자에 `ValueError`를 내게 한 설계: 원래 `TypeError` 검사와 달리 `"3"` 같은 숫자 글도 받음(본문에 적지 않음). 확인 파일이 `except`로 받아 출력하므로 02-4 After를 노랑(§5-3)으로 칠함
- 02-2의 브랜치 이름표 회색(클래스 없음), 02-3 메모에 결과 값을 넣지 않은 선택(02-4 빨강·노랑과 겹치지 않게)
- 삽화 02-6: 수레·검수대·선반 끝에 파란 상자가 모두 보이는 연속 장면 구도(01-5와 같은 방식)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 1, 하 3, 공통 C-2·C-3·C-4 일부). 모두 반영했습니다.
- 02-1(중): 작성자 config 셀을 4번 복제 셀에 합침(코드 셀 23 → 22, 출력 줄은 같음). 노트북 준비물 아래와 본문 b5 노트북 토큰 앞에 「강의 시간에는 6~8번과 11~12번 소제목을 설명합니다. 6~8번은 기능 브랜치·올리기·PR 범위이고, 11~12번은 리뷰와 병합입니다. 1~5번과 9~10번은 셀을 함께 실행하고, 결과 읽기는 실습 시간에 이어서 읽습니다.」 **강사 확인 대상**. 코드 번호가 옛 6번부터 하나씩 줄어 캡션 읽는 법(02-1·02-2·02-3·02-5)과 설계표를 새 번호로 고침
- 02-2: [12. After] 설명과 본문 b6 둘째 단락에 「함수 `int()`는 숫자 모양 글 `"3"`도 정수 3으로 바꾸므로, 고친 함수는 그런 글도 받습니다. 이 경우는 이번에 실행하지 않았습니다.」(노트북은 G6 dense_paragraph 때문에 별도 단락)
- 02-3: `02-1-세-저장소.mmd` 작성자 쪽 화살표 라벨 「git clone / git fetch」, 캡션 읽는 법 코드 번호 4·9·12·18·21·22. PNG에서 라벨 겹침 없음 확인
- 02-4: 02-2 캡션 「기능 브랜치를 원격에 올린 뒤의 브랜치 이름. 새 커밋으로 옮겨 간 이름은 지금 있는 기능 브랜치뿐입니다.」(본문 토큰·caption.md)
- C-2·C-3: `02-3-주고받는-순서.mmd`를 실선 요청 → 점선 응답(`summary.py 받음`, `fix 커밋 받음 (behind 1)`, `origin/main = merge: 주문 요약`)으로 바꾸고 `messageAlign: left`·한 줄 라벨. 도식 읽기 「실선 화살표는 요청한 명령, 점선 화살표는 받아 온 결과입니다.」 `visual.cjs`가 SVG 글자 13.98px로 잡아 리뷰어 화살표 라벨을 「clone, switch 기능 브랜치」로 줄여 viewBox 870 → 806(PNG 확인)
- C-4: PR 설명 셀에 `print("PR 설명 글:")` 한 줄. 결과 읽기는 줄 번호를 쓰지 않아 그대로
- 코드 셀 22, 검사한 문장 455

재실행: `run_section.sh … 02`(새 커널 PASS) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 112 code cells (max 18 lines)`, `visual.cjs` 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/02-GitHub-Flow와-PR-리뷰.md`
- 루트 `textbook/qa/upgrade-progress.md` 표는 챕터 밖 파일이라 이 작업에서 고치지 않음
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
