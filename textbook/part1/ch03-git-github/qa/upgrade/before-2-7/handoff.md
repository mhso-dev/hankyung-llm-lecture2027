# Ch 03 절 사이 인계 메모

절 작업자가 다음 절 작업자에게 넘기는 메모입니다. 절을 마칠 때 맨 아래에 `## §NN → §NN+1`을 붙입니다.
「이어 쓸 이름과 값」은 다음 절이 쓸 수 있는 후보이고, 「아직 안 가르친 것」은 다음 절이 설명 없이 전제하면 안 되는 것입니다.
앞 챕터 요약: `textbook/part1/ch01-development-environment/qa/upgrade/chapter-summary.md`, `textbook/part1/ch02-python/qa/upgrade/chapter-summary.md`.

## §01 → §02

(01절은 Ch 2 마감 전에 먼저 개선했고, 2026-09-16 Ch 1·2 요약 확정 뒤 연속성 보정을 마침. 보정 내용은 `01-diagnosis.md` 「연속성 보정」)

- 새로 가르친 Git 명령: `git init -b main`(Ch 1 05절 `git init`에 첫 브랜치 이름 main을 더함), `git config user.name "…"`·`git config user.email …`(`--global` 없이 이 저장소에만, 값 없이 이름만 주면 조회 — Ch 1 05절 `-c`를 대신함), `git status --short --ignored`, `git add 파일`, `git commit -m "메시지"`와 출력 읽기(`[main (root-commit) 해시]`·`1 file changed`·`1 insertion(+), 1 deletion(-)`·`create mode`/`delete mode`), `git log --oneline`(최신 순), `git diff`(작업 폴더 ↔ 색인), `git diff --cached`(색인 ↔ HEAD), `git check-ignore -v 파일`(`.gitignore:3:*.log` = 파일:줄 번호:규칙, 종료 코드 1 = 걸린 규칙 없음), `git rm --cached 파일`(색인에서만 빼고 실제 파일은 남음), `git ls-files 파일`, `git show HEAD~1:debug.log`(지난 커밋의 파일 내용). 주의 메모에서 이름만: `git add .`, `--global`
- 새로 가르친 개념·용어(용어 표 7개): 저장소(Git이 변경을 기록하는 폴더, 기록은 `.git`), 작업 폴더(working tree), 색인(index = Ch 1 05절 「기록할 목록」, staging area), 커밋(색인에 고른 상태 + 메시지를 이력에 남긴 기록 — Ch 1 05절 뜻을 넓힘), 추적(tracking), 무시 규칙(`.gitignore`, 별표 `*`), HEAD(지금 기준인 마지막 커밋)와 `HEAD~1`. 상태 표시 두 칸(첫 칸 색인, 둘째 칸 작업 폴더): `??`·`A `·` M`·`M `·`D `·`!!`(Ch 1 05절은 앞 빈칸을 떼고 한 글자만 읽었음). 「무시 규칙은 아직 추적하지 않는 파일에만 적용」, 「추적을 멈춰도 지난 커밋 내용은 남음(기록 삭제는 05절)」. 메시지 앞머리 `chore:`·`feat:`·`fix:`는 「이 교재의 팀 관례, 필수 문법 아님」. 브랜치(branch)는 「커밋이 이어지는 줄기의 이름이고 02절에서 배움」 한 문장만 적음
- 이어 쓸 도우미(코드 그대로, 정의 셀 하나):
  ```python
  import shlex
  import subprocess


  def run_git(command: str):
      full_command = "git " + command
      arguments = shlex.split(full_command)
      result = subprocess.run(arguments, capture_output=True, encoding="utf-8")
      print("$", full_command)
      print(result.stdout + result.stderr)
      if result.returncode != 0:
          print("종료 코드:", result.returncode)
  ```
  설명 셀에서 한 것: 「뼈대는 Ch 2 08절 `run_pytest()`」, 글자 사이 `+` = 이어 붙이기, `shlex.split()` = 따옴표 메시지를 한 낱말로, `text=True` 대신 `encoding="utf-8"`(기본 규칙이 UTF-8이 아니면 한글 메시지가 깨질 수 있음, 다른 OS 실행 안 함), 반환값이 없어 `->` 생략. 출력은 `$ git 명령` 다음 줄에 결과, 0이 아닌 종료 코드만 `종료 코드: N`. `check=True`가 없어 git이 실패해도 셀은 멈추지 않음 — 02절의 push 거절 등 실패 장면에서 쓰기 좋음. 02절이 두 저장소(작성자·리뷰어)나 원격을 다루면 ① 셀마다 `os.chdir()`로 옮기거나 ② 같은 이름으로 다시 정의해 기본값 매개변수(Ch 2 04절)와 `subprocess.run(..., cwd=폴더)`(Ch 1 05절)를 더하는 방법이 사다리 안에 있음. `*args`·`X | None`·`cwd or root`는 A 트랙 미교육(G1)
- 이어 쓸 폴더·파일 이름과 값: 준비 셀 `import os`·`import tempfile` → `practice_folder = tempfile.mkdtemp(prefix="ch03-01-")` → `os.chdir(practice_folder)` → `file_names = os.listdir()` 출력 `[]`(Ch 2 08절 모양, 02절은 `ch03-02-`). 임시 폴더 자체가 저장소(`orders` 하위 폴더 없음), `git init` 뒤 `['.git']`. 작성자 `Ch3 Student`·`student@example.com`(Ch 1 05절 `Ch1 Student` 규칙. 두 사람이 필요하면 같은 규칙으로 이름을 지으면 됨). 파일 `app.py` `print("주문 2건")` → 값 바꿔 보기 `print("주문 3건")`, `.gitignore` 3줄(`.env`/`__pycache__/`/`*.log`), `.env` `APP_MODE=demo`(추적하지 않음 `!! .env`), `debug.log`(`first run` → `second run` → `third run`, 마지막에 추적 해제). 파일 쓰기는 모두 `with open(이름, "w"/"a", encoding="utf-8") as file:` + `file.write(…)`, 여러 줄은 `ignore_text = """…"""`. 커밋 5개(먼저 만든 순): `chore: 생성 파일 추적 제외` → `feat: 주문 요약 추가` → `fix: 주문 건수 수정` → `chore: 디버그 로그 기록` → `chore: 로그 파일 추적 제외`. 브랜치 main 하나. 교재 실행 Linux Git 2.34.1(2026-09-16). 커밋 해시·임시 경로는 결과 읽기에서 인용하지 않음(출력의 `[사용자 폴더]`는 실행 도구가 가린 표시라고 적음)
- 비유·그림: 삽화 01-5 택배 상자(책상 = 작업 폴더, 열린 상자 = 색인, 봉한 상자 = 커밋, 휴지 = 무시 규칙에 적은 파일). 색: 작업 폴더·색인·커밋·파일 tool 초록, 실행한 일 flow 파랑, 상태 표시·After 결과 measure 노랑, Before 결함 결과(`M debug.log`·종료 코드 1) fail 빨강, 추적하지 않는 `.env` 회색. §5-3: 잡아서 출력한 오류는 노랑, 멈춘 실패·0이 아닌 종료 코드·Before 결함은 빨강
- 02절이 이어받을 연결: 01 본문 「다음 학습」은 「02절에서는 목적이 분명한 커밋을 기능 브랜치에 쌓습니다. 그 변경을 PR 단위로 비교하고 검토합니다」. 01 노트북 끝은 「다음 절에서는 기능 브랜치에 커밋을 쌓고 PR로 변경을 검토합니다」. 기존 02 노트북의 `summarize(count)` → `주문 {count}건`은 01 `app.py`의 「주문 N건」과 이어짐. 기존 02 노트북은 개선 전 모양: 한 셀에 `git(*args, cwd=…, check=…)`와 `configure()` 두 함수, `TemporaryDirectory(prefix="git-lesson-")`, `Path`·`write_text`·`read_text().replace().replace()`, 작성자 `Git Learner`, `subprocess.check_output`, `isinstance`·`raise TypeError`, bare 원격·clone·`switch -c`·push·fetch·`merge --no-ff`·`diff --stat origin/main...HEAD`·`log --graph`. 01의 `run_git()`·준비 셀·작성자 이름으로 맞추고, `raise`·`isinstance`는 Ch 2에서 가르치지 않았으므로 다른 입력 확인으로 바꾸거나 한 문장씩 풀어야 함
- Ch 1·Ch 2에서 이어받아 01이 쓴 것: Ch 1 05절 `git init/add/commit`·`-c`·`status --short`(`??`·`A`·`M`·0줄)·`git diff`·「기록할 목록」·`.git` 폴더를 고치지 않음·수량 2→3 실험·「이름을 저장소에 적는 방법은 Ch 3」 약속, Ch 1 03절 `\n` 줄바꿈과 종료 코드, Ch 1 04절 `"""…"""`, Ch 2 03절 `in`, Ch 2 04절 함수 정의(정의 셀/호출 셀 분리, 결과 읽기 「예상대로 출력이 없습니다」), Ch 2 05절 `with open("w")`·`encoding="utf-8"`·모드 `"a"`(Ch 2에서 실행 안 한 모드라고 연결), Ch 2 07절 import 문·표준 라이브러리(그래서 `upgrade_allow=["stdlib-import"]`는 쓰지 않음 — Ch 3은 L4 위치), Ch 2 08절 `run_pytest()`·`subprocess.run(…, capture_output=True, text=True)`·종료 코드 0/0 아님·준비 셀. 학습 순서 「실행 전에 예상합니다 → 실행 → 결과 읽기」
- 아직 안 가르친 것(02절이 설명 없이 전제하면 안 됨): 브랜치 만들기·전환(`git branch`·`switch`·`checkout`), 병합(`merge`)·병합 커밋·`--no-ff`, 원격(`remote`·`clone`·`push`·`fetch`·`pull`·bare 저장소·`origin`), GitHub·PR·리뷰, `git log --graph`·`--stat`·세 점 비교 `A...B`, `git restore`·`reset`·`revert`·`reflog`·`stash`·`worktree`, `git add .`(이름만), `--global`(이름만), `.gitignore`의 `!` 부정·폴더 규칙 동작(`__pycache__/`는 적기만 함), 팀원 작업 폴더에서 `rm --cached` 파일이 지워지는 장면(실행 안 함), 기록에서 내용 지우기(05절), Windows·macOS 실행. Python 쪽: `pathlib.Path`(01에서 뺌, Ch 1에서만), 목록 `+`(01은 글자 `+`만 풂), `raise`·`isinstance`, `subprocess.check_output`, `sys.executable -c`로 코드 실행(Ch 1 03 `python -c`·Ch 2 08 `sys.executable`은 따로 배움, 둘을 합친 모양은 안 씀), 메서드 세 번 연결, `*args`·`**kwargs`(A 트랙), 타입힌트 `-> None`·`X | None`, `try/except`(01에서는 안 씀. 쓰면 Ch 2 05절처럼 그 오류 이름만 받기), `@` 줄·`BaseModel`·픽스처(A 트랙은 Ch 2 09~11절을 건너뜀)

## §02 → §03

(02절 품질 개선 2026-09-16. 결과는 `02-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 23, 모델 호출 0)

- 새로 가르친 Git 명령: `git init --bare -b main 이름.git`(bare 저장소 = 작업 폴더 없는 원격), `git clone 원격 폴더`(빈 저장소면 경고 `You appear to have cloned an empty repository`, 복제 뒤 원격 main으로 시작), `git remote -v`(`origin` + `(fetch)`/`(push)`), `git push -u origin 브랜치`(`[new branch]`, `Branch '…' set up to track`), 짝을 적은 뒤 `git push`, `git push origin main`, `git switch -c 새 브랜치`, `git switch 기존/원격에만 있는 브랜치`(원격 이름이 있으면 짝 브랜치를 새로 만듦), `git branch`(`*` = 지금 브랜치)·`-v`(가리키는 커밋 메시지)·`-vv`(대괄호 짝 `[origin/main]`, `behind 1`, `ahead 3`), `git diff --stat origin/main...HEAD`·`git diff origin/main...HEAD`(점 세 개 = 갈라진 커밋 뒤 지금 브랜치의 변경), `git fetch`(`origin/` 이름만 옮기고 내 브랜치·작업 폴더는 그대로), `git merge --no-ff origin/브랜치 -m "…"`(`Merge made by the 'ort' strategy.`), `git log --oneline --graph`, `git log --oneline -1 origin/main`
- 새로 가르친 개념·용어(용어 표 7개): 원격 저장소(remote repository)·bare 저장소·브랜치(줄기 끝 커밋을 가리키는 이름, 새 커밋은 지금 브랜치 이름만 옮김)·기능 브랜치·풀 리퀘스트(PR, GitHub 기능)·코드 리뷰·병합 커밋(부모 둘). 본문에서만: 복제(clone), 병합(merge), 짝(추적 관계를 교재에서 부른 말 — 「upstream」「원격 추적 브랜치」 용어는 쓰지 않음), GitHub Flow 여섯 단계, PR 템플릿(루트 `pull_request_template.md`, 기본 브랜치에 있어야 함), fast-forward는 이름만(실행 안 함), squash·rebase 병합은 이름만
- 이어 쓸 도우미(정의 셀 각각 하나):
  ```python
  def run_git(command: str, folder: str = "."):
      full_command = "git " + command
      arguments = shlex.split(full_command)
      result = subprocess.run(arguments, capture_output=True, encoding="utf-8", cwd=folder)
      print(folder, "$", full_command)
      print(result.stdout + result.stderr)
      if result.returncode != 0:
          print("종료 코드:", result.returncode)
  ```
  ```python
  def run_python(file_name: str, folder: str):
      arguments = [sys.executable, file_name]
      result = subprocess.run(arguments, capture_output=True, text=True, cwd=folder)
      print(folder, "$ python", file_name)
      print(result.stdout + result.stderr)
      if result.returncode != 0:
          print("종료 코드:", result.returncode)
  ```
  `run_git`은 01절 함수를 같은 이름으로 다시 정의(기본값 `"."`, 출력 `author $ git …`/`. $ git …`), `import shlex`·`import subprocess`는 정의 셀 안. `run_python`은 `import sys`와 함께 Before 첫 사용 직전에 정의, 「뼈대는 Ch 2 08절 run_pytest(), text=True는 새 Python이 기본 규칙으로 내보내므로」라고 설명. 두 함수 모두 `check=True`가 없어 git이 실패해도 셀이 멈추지 않음 → 03절 push 거절(종료 코드 1)·pull 충돌을 `종료 코드: 1` 줄로 읽게 쓸 수 있음(기존 03 노트북의 `subprocess.run(["git", "push", …])` 직접 호출·`push.stderr…splitlines()[-1]` 메서드 연결을 대신)
- 이어 쓸 폴더·파일 이름과 값: 준비 셀 `mkdtemp(prefix="ch03-02-")`+`os.chdir`+`os.listdir()` `[]`(03절은 `ch03-03-`). 원격 `team.git`, 작성자 폴더 `author`(`Ch3 Student`·`student@example.com`), 리뷰어 폴더 `reviewer`(`Ch3 Reviewer`·`reviewer@example.com`). 경로는 `"author/summary.py"`처럼 상대 경로 글. 파일 목록은 `sorted(os.listdir("reviewer"))`. 첫 커밋 `chore: 저장소와 PR 템플릿 시작`(`.gitignore` `__pycache__/`, `pull_request_template.md` 「## 변경 내용 / - (여기에 적기) / ## 확인한 입력 / - [ ] 빈 값을 넣어 실행」), `feat: 주문 요약 함수 추가`(`summary.py` 두 줄), `fix: 빈 주문 건수 입력 확인`(`number = int(count)`), `merge: 주문 요약`. 확인 파일 `check_summary.py`(커밋 안 함) 출력 `보통 값 3: 주문 3건` / `빈 값: 주문 건` → `입력 오류: invalid literal for int() with base 10: ''`. 교재 실행 Linux Git 2.34.1(2026-09-16). 해시·임시 경로는 인용하지 않음
- 기존 03 노트북과 맞출 곳: `git(*args, cwd, check)`+`configure()` 한 셀·`Path`·`write_text`·`read_text`·`alice, bob = …` 두 이름 한 줄 대입(Ch 2 03 풀어 담기라 문법은 배웠으나 한 줄 두 경로)·`subprocess.run(["git", "pull", …])` 직접 호출·`all(… for …)` 제너레이터 식·`assert len(parents.split()) == 2`·`git show --pretty=%P`. 작성자 `Git Learner` → 두 사람이면 02절처럼 `Ch3 Student`/`Ch3 Reviewer` 규칙(예: `Ch3 Alice`·`Ch3 Bob`은 새 규칙이므로 폴더 이름만 alice/bob으로 두고 이름표 규칙을 한 문장 설명). 기존 03이 쓰는 `git pull --no-rebase`는 02절에서 가르치지 않음(fetch+merge만) → 「pull = fetch 뒤 merge」를 한 문장으로 풀면 02절과 이어짐. 부모 수는 02-5 그림·`log --graph`로 보여 준 방식이 있음
- 비유·그림: 삽화 02-6 검수대와 선반(긴 선반 = main, 수레 = 기능 브랜치, 파란 상자 = 브랜치 커밋, 검수대 = PR 리뷰, 선반 끝 = 병합), 01-5 택배 상자를 이어 씀. 색: 저장소·커밋·파일 tool 초록, 실행한 일 flow 파랑, 브랜치 이름표 회색(클래스 없음), Before 결함 결과(오류 없이 나온 틀린 글) fail 빨강, 받아서 출력한 오류 measure 노랑, sequenceDiagram 메모 노랑(결과 값 대신 실행 시점만). 03절 충돌은 git이 멈춘 실패(종료 코드 1, `UU`)라 §5-3상 빨강, 해결 뒤 결과는 노랑이 자연스러움
- 02절이 03절에 넘긴 연결: 본문 「다음 학습」 = 「03절에서는 두 사람이 같은 줄을 다르게 고쳐 병합이 멈추는 경우를 봅니다. 충돌 표시를 읽고 합칠 결과를 직접 정합니다」. 노트북 끝 = 「다음 절에서는 두 브랜치가 같은 줄을 다르게 고쳐 병합이 멈추는 경우를 다룹니다」. 02절 주의 메모 「받아 온 뒤 `git branch -vv`의 behind·ahead로 짝과 비교」는 03절 push 거절 원인(원격이 앞섬)을 읽는 데 바로 씀
- Python 쪽에서 02가 쓴 것: Ch 2 01 `int()` 형 변환과 ValueError, 03 `sorted()`, 04 기본값 매개변수·같은 이름 재정의, 05 `with open("r"/"w")`·`try/except ValueError as error`, 07 `from … import`·타입힌트(값 검사 안 함), 08 `sys.executable`·`text=True`·종료 코드, 13 오류 글. Ch 1 02 상대 경로, 04 `replace()`, 05 `cwd=`
- 아직 안 가르친 것(03절이 설명 없이 전제하면 안 됨): `git pull`(fetch+merge 합친 명령)·`--no-rebase`·rebase 실행, push 거절(non-fast-forward)과 그 출력, 병합 충돌·충돌 표시 `<<<<<<<`·`=======`·`>>>>>>>`·상태 `UU`, `git merge --abort`, fast-forward 병합 실행, `git show --pretty=%P`·`rev-parse`, 브랜치 삭제(`git branch -d`, `push --delete`), 원격 main이 먼저 움직인 뒤의 점 세 개/두 개 비교 차이, `git restore`·`reset`·`revert`·`reflog`·`stash`·`worktree`, 실제 GitHub 화면(PR·리뷰 승인·브랜치 보호·병합 버튼), Windows·macOS 실행. Python 쪽: `isinstance`·`raise`(02에서 뺌), `pathlib.Path`, 제너레이터 식 `all(… for …)`, `*args`·`**kwargs`(A 트랙), 메서드 세 번 연결, `subprocess.check_output`, `sys.executable -c`, 타입힌트 `-> None`·`X | None`, `@` 줄·`BaseModel`·픽스처

## §03 → §04

(03절 품질 개선 2026-09-16. 결과는 `03-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 19, 모델 호출 0)

- 새로 가르친 Git 명령·출력: 거절된 `git push`(`! [rejected]        main -> main (fetch first)`, `hint: Updates were rejected because the remote contains work that you do`, `종료 코드: 1`), `git branch -vv`의 `[origin/main: ahead 1, behind 1]`(갈라진 이력), `git merge origin/main -m "…"`(갈라진 줄기라 `--no-ff` 없이도 병합 커밋, `Merge made by the 'ort' strategy.`), `git pull`(= 받아 오기 뒤 병합, 뒤처진 쪽에서만 실행 → `Updating a..b`·`Fast-forward`, stdout이 먼저라 `From …`·`main -> origin/main` 줄이 아래에 보임), 충돌 병합 출력(`Auto-merging message.txt`, `CONFLICT (content): Merge conflict in message.txt`, `Automatic merge failed; fix conflicts and then commit the result.`, `종료 코드: 1`), 충돌 중 `git status --short`의 `UU message.txt`(충돌 중에는 두 칸 뜻이 01절과 다름), 해결 전 `git commit` 거절(`error: Committing is not possible because you have unmerged files.`, `hint: … use 'git add/rm <file>'`, `fatal: Exiting because of an unresolved conflict.`, `종료 코드: 128`), 충돌 표시 `<<<<<<< HEAD`/`=======`/`>>>>>>> origin/main`, 해결 뒤 `git add` → `M  message.txt` → `git commit -m`(출력 `[main 해시] 메시지`만, 요약 줄 없음) → `git push`
- 새로 가르친 개념·용어(용어 표 7개): 올리기 거절(rejected push, 「거절은 파일이 아니라 커밋 줄기를 보고 정함」)·갈라진 이력(diverged history)·공통 조상(merge base, 「두 줄기가 갈라지기 전의 마지막 커밋, 병합은 이것과 두 쪽을 비교」)·풀(pull)·fast-forward 병합(02절에서 이름만 → 03에서 실행)·병합 충돌(merge conflict)·충돌 표시(conflict marker). 본문 규칙: 「한쪽만 바꾼 파일·줄은 그 변경을 가져오고, 같은 줄을 다르게 바꾸면 멈춤」, 「충돌 표시만 지우고 한쪽을 고르면 병합은 끝나도 팀 기준과 다를 수 있음 → 기준 파일과 비교해 새 줄」. 주의 메모에서 이름만(실행 안 함): `git merge --abort`, `--ours`·`--theirs`, `git push --force`(원격 커밋을 잃게 할 수 있음, git-push 문서), 갈라진 상태의 `git pull --no-rebase`(git-pull 문서 근거, 노트북은 fetch+merge로 나눠 실행)
- 이어 쓸 도우미: 02절 `run_git(command: str, folder: str = ".")`를 같은 모양으로 다시 정의(정의 셀 하나, `import shlex`·`import subprocess` 포함). 03절은 `run_python()`을 쓰지 않았음. 파일 읽기는 `with open("폴더/파일", "r", encoding="utf-8") as file:` + `변수 = file.read()` + `print(변수)`, 표시 확인은 `print("충돌 표시가 남아 있음:", "<<<<<<<" in message_text)`(Ch 2 03절 `in`) — Before/After에 같은 방법으로 두 번 실행
- 이어 쓸 폴더·파일 이름과 값: 준비 셀 `mkdtemp(prefix="ch03-03-")`(04절은 `ch03-04-`). 원격 `team.git`, `author`(`Ch3 Student`·`student@example.com`), `reviewer`(`Ch3 Reviewer`·`reviewer@example.com`) — 03절에서 리뷰어도 팀원으로 파일을 고침. 파일 `message.txt`(`배송 안내: 준비 중` → 리뷰어 `배송 안내: 14시 이전은 오늘 출고` / 작성자 `배송 안내: 내일 출고` → 해결 `배송 안내: 14시 이전 결제는 오늘 출고, 14시 이후 결제는 내일 출고`), `policy.txt`(`14시 이전 결제: 오늘 출고`/`14시 이후 결제: 내일 출고`), `contact.txt`(`문의 안내: 주문 번호와 함께 남겨 주세요`). 커밋 7개(먼저 만든 순): `docs: 배송 안내 시작` → `docs: 출고 기준 기록`(리뷰어)·`docs: 문의 안내 추가`(작성자) → `merge: 출고 기준 받기` → `docs: 당일 출고 안내`(리뷰어)·`docs: 익일 출고 안내`(작성자) → `merge: 출고 기준에 맞춰 충돌 해결`. 메시지 앞머리 `docs:`는 「문서 파일을 고친 커밋에 붙이는 이 교재의 팀 관례」로 03에서 처음 설명. 해시·임시 경로는 인용하지 않음. Linux Git 2.34.1(2026-09-16)
- 비유·그림: 삽화 03-6 한 칸의 두 카드(선반 끝 칸 하나 = 파일의 한 줄, 해 카드 = 리뷰어 줄, 달 카드 = 작성자 줄, 기준표 = `policy.txt`, 해와 달 흰 카드 = 해결한 줄, 칸에 꽂기 = 병합 커밋). 01-5 택배 상자 → 02-6 검수대와 선반 → 03-6으로 창고 선반을 이어 씀. 색: 커밋·파일 초록, 성공한 명령(병합·올리기·pull) 파랑, 짝 비교·상태 표시·확인 출력 노랑, 거절·충돌·커밋 거절(종료 코드 1·128, `UU`) 빨강. 성공한 병합 결과는 03-2·03-3 모두 파랑으로 맞춤
- 03절이 04절에 넘긴 연결: 본문 「다음 학습」 = 「04절에서는 이미 원격에 올린 잘못된 변경을 새 커밋으로 취소합니다. 로컬에서 보이지 않게 된 커밋을 기록에서 찾아 복구하는 방법도 봅니다.」 노트북 끝 = 「다음 절에서는 이미 원격에 올린 잘못된 변경을 새 커밋으로 취소하고, 보이지 않게 된 커밋을 기록에서 찾아 복구합니다.」 03절 주의 메모의 「`--force`로 덮어 올리지 않음」은 04절 「공개한 변경은 revert로 취소」의 이유로 이어 쓸 수 있음
- 기존 04 노트북과 맞출 곳: 개선 전 모양 그대로 — `git(*args, cwd, check)`+`configure()` 한 셀, `TemporaryDirectory(prefix="git-lesson-")`·`Path`·`mkdir`·`write_text`·`read_text`·`exists()`, 작성자 `Git Learner`, `git init -b main`을 `root / "recovery"`에서 실행(원격 없음), `rev-parse HEAD`로 해시를 변수에 담기(`good`·`bad`·`lost`), `git revert --no-edit 해시`, `git worktree add -b fix/urgent 경로`·`worktree list --porcelain`·`branch --show-current`, `git reset --hard HEAD~1`, `git log --format=%H`, `git reflog --format=%H%x09%gs -5`, `next(… for … if …)` 제너레이터 식(G1), `line.split("\t", 1)[0]`, `git branch 이름 해시`·`git show 브랜치:파일`·`rev-parse --short`, `assert` 네 줄. 해시를 인용하지 않는 규칙이라 `rev-parse`로 변수에 담는 대신 `HEAD`·`HEAD~1`(01절)·브랜치 이름·커밋 메시지로 가리키는 방법이 이어짐에 맞음. `next(…)`는 규격 §2-3대로 `for`+`if`+`break` 여러 줄로. 할인율 `discount=10`→`90`은 Ch 2 주문 데이터(할인율 0.1)와 이어 설명할 수 있음
- Python 쪽에서 03이 쓴 것: Ch 1 03 종료 코드·`.stdout`/`.stderr`, Ch 2 03 `in`, 04 기본값 매개변수·같은 이름 재정의, 05 `with open("r"/"w")`, 07 import·타입힌트. `try/except`·`sorted()`·`run_python()`·`sys`는 03에서 쓰지 않음
- 아직 안 가르친 것(04절이 설명 없이 전제하면 안 됨): `git revert`·`git reset`(특히 `--hard`)·`git reflog`·`git worktree`·`git restore`·`git stash`, `git rev-parse`·`git show --pretty`·`--format=%H` 같은 형식 지정, `git branch 이름 커밋`(특정 커밋에 브랜치 이름 붙이기)·`git branch --show-current`, `git show 커밋:파일`은 01절에서 `HEAD~1:debug.log`로만 씀, `git merge --abort`·`--ours/--theirs`·`push --force` 실행, rebase, 브랜치 삭제, 원격이 없는 단독 저장소에서 `git init -b main`(01절 방식)과 원격 저장소 방식 중 무엇을 쓸지, GitHub 화면. Python 쪽: `pathlib.Path`·`exists()`, `next()`·제너레이터 식, `split("\t", 1)` 같은 최대 분할 인자와 `\t`, `raise`·`isinstance`, `*args`·`**kwargs`(A 트랙), 메서드 세 번 연결, 타입힌트 `-> None`·`X | None`, `@` 줄·`BaseModel`·픽스처(A 트랙은 Ch 2 09~11절을 건너뜀)

## §04 → §05

(04절 품질 개선 2026-09-16. 결과는 `04-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 19, 모델 호출 0)

- 새로 가르친 Git 명령·출력: `git revert --no-edit HEAD`(출력 `[main 해시] Revert "fix: 할인율 90 설정"`, ` Date:` 줄, `1 file changed, 1 insertion(+), 1 deletion(-)`, 이력은 커밋 세 개로 잘못된 커밋도 남음), 취소 커밋을 올린 `git push`(거절 없음 `main -> main`)와 리뷰어 `git pull`(`Fast-forward`), `git worktree add -b 새브랜치 ../폴더`(`Preparing worktree (new branch 'fix/urgent')`, `HEAD is now at`), `git worktree list`(경로·해시·`[브랜치]`), `git branch`의 `+ 브랜치`(다른 작업 폴더가 쓰는 브랜치), 이미 쓰는 브랜치로 `worktree add ../main-copy main`(`fatal: 'main' is already checked out at`, `종료 코드: 128`), `git worktree remove ../폴더`(출력 없음, 브랜치는 남음), `git reset --hard HEAD~1`(`HEAD is now at 해시 메시지`, 종료 코드 0), `git reflog -5`(`해시 HEAD@{0}: reset: moving to HEAD~1`, `HEAD@{1}: commit: …`, `checkout: moving from main to experiment`, `revert: …`), `git branch 이름 HEAD@{1}`(출력 없음, 지금 브랜치는 그대로), `git log --oneline -1 브랜치`, `git show 브랜치:파일`, `git switch 기존 브랜치`(`Switched to branch '…'`)
- 새로 가르친 개념·용어(용어 표 6개): 공개한 커밋(원격에 올려 다른 사람이 받을 수 있게 된 커밋)·취소 커밋(revert commit)·리셋(reset, 「지금 브랜치 이름을 다른 커밋으로 옮김, `--hard`는 추적 파일도 맞춤」)·참조 기록(reflog, 「HEAD나 브랜치 이름이 가리킨 커밋이 바뀔 때마다 이 저장소가 적는 기록」 → 검토 1차에서 「HEAD가 옮겨 갈 때마다(커밋, 브랜치 전환, reset 등) 적는 기록」으로 고침. 커밋이 그대로여도 브랜치를 바꾸면 한 줄이 생김)·`HEAD@{n}`(n번 옮기기 전 HEAD)·추가 작업 폴더(worktree). 본문 규칙: 「공개한 커밋은 더해서 취소」, 「`git log`는 지금 커밋에서 부모 쪽으로 따라가므로 이름에서 떨어진 커밋은 목록에서 빠짐」, 「한 브랜치는 한 작업 폴더에서만」, 「해시를 옮겨 적지 않고 git 이름으로 가리킴」. 주의 메모에서 문서 근거로만(실행 안 함): 공개한 커밋에 `reset`·`push --force` 쓰지 않기, revert 충돌과 `--continue`, revert는 작업 폴더가 깨끗해야 함, `--hard`로 커밋 전 변경을 잃으면 참조 기록에 없음, 참조 기록은 저장소마다 따로·기본 90일(이름에서 떨어진 줄 30일) 뒤 정리될 수 있음(git-reflog 문서), `HEAD@{1}` 번호는 HEAD를 옮기면 달라짐, 고치다 만 worktree는 remove가 지우지 않음
- 이어 쓸 도우미: 03절과 같은 `run_git(command: str, folder: str = ".")` 정의 셀 하나(`import shlex`·`import subprocess` 포함). `run_python()`·`sys`·`try/except`는 04에서 쓰지 않음. 파일 쓰기 `with open("폴더/파일", "w", encoding="utf-8")`, 여러 줄은 `urgent_config = """…"""`, 읽기 `config_text = file.read()` + `print("리뷰어의 config.txt:", config_text)`, 폴더 확인 `file_names = os.listdir("author")` + `print("idea.txt가 폴더에 있는가:", "idea.txt" in file_names)`(Before/After 같은 방법), 준비 셀 폴더 목록은 `sorted(os.listdir())`
- 이어 쓸 폴더·파일 이름과 값: 준비 셀 `mkdtemp(prefix="ch03-04-")`(05절은 `ch03-05-`). 원격 `team.git`, `author`(`Ch3 Student`)·`reviewer`(`Ch3 Reviewer`). `config.txt` `discount=10`(10% = Ch 2 04절 할인율 0.1) → `discount=90` → 취소, `urgent-fix/config.txt`에 `max_discount=30`, 커밋하지 않은 `notice.txt` `공지 초안: 할인 행사 안내`, `idea.txt` `첫 주문 쿠폰 아이디어`. 커밋(먼저 만든 순): `feat: 할인율 10 설정` → `fix: 할인율 90 설정` → `Revert "fix: 할인율 90 설정"`(main, 원격) / `fix: 할인율 상한 30 추가`(`fix/urgent`, 원격에 안 올림) / `docs: 쿠폰 아이디어 기록`(`experiment`에서 reset으로 떨어짐 → `recovered-idea`). 브랜치 `main`·`fix/urgent`·`experiment`·`recovered-idea`. 교재 실행 Linux Git 2.34.1(2026-09-16). 해시·임시 경로는 인용하지 않음(`[사용자 폴더]`는 실행 도구가 가린 표시라고 04 결과 읽기에 적음)
- 비유·그림: 삽화 04-6 취소 상자와 깃발 수첩(왼쪽 팀 선반 = 원격 main, 구겨진 종이가 삐져나온 상자 = 잘못된 커밋, 되돌리기 화살표 초록 테이프 상자 = 취소 커밋, 클립보드 동료 = 이미 받은 리뷰어 / 오른쪽 책상 = 내 저장소, 노란 깃발 = experiment, 점선 깃발 윤곽 = reset 전 자리, 깃발 그림 수첩 = 참조 기록, 파란 새 깃발 = recovered-idea). 01-5 택배 상자 → 02-6 검수대와 선반 → 03-6 한 칸의 두 카드 → 04-6으로 창고 선반을 이어 씀. 색: 커밋·파일·작업 폴더 초록, 실행한 명령(reset 포함) 파랑, 확인 출력·짝 비교 노랑, 브랜치 이름·상황 회색, 거절(`종료 코드: 128`)과 Before 결함 결과(`False`)만 빨강. 잘못된 커밋 자체는 실패가 아니라 초록
- 04절이 05절에 넘긴 연결: 본문 「다음 학습」 = 「05절에서는 비밀 값이 커밋에 들어간 경우를 다룹니다. 이 절에서 본 것처럼 취소 커밋을 더해도 지난 커밋에는 값이 남습니다. 그래서 기록 자체를 정리하는 절차와 값을 바꾸는 조치를 함께 봅니다.」 노트북 끝 = 「다음 절에서는 비밀 값이 커밋에 들어간 경우를 다룹니다. 취소 커밋을 더해도 지난 커밋에는 값이 남으므로, 기록 자체를 정리하는 절차를 봅니다.」 04 복습 1번 「잘못된 커밋은 이력 가운데에 그대로」와 주의 메모 「공개한 커밋에 `push --force`를 쓰지 않음」은 05의 「이력 재작성은 해시가 바뀌고 강제 올리기가 필요해 팀 합의가 먼저」로 이어 쓸 수 있음(04는 강제 올리기를 실행하지 않았으므로 05가 처음 실행하는 자리)
- 기존 05 노트북과 맞출 곳: 개선 전 모양 그대로 — `git(*args, cwd, check)`+`configure()` 한 셀, `TemporaryDirectory(prefix="git-lesson-")`·`Path`·`write_text`·`exists()`, 작성자 `Git Learner`, 원격 `secret-remote.git`·저장소 `secret-demo`(03·04는 `team.git`·`author`), 변수 `DUMMY = "DEMO-ONLY-NOT-A-REAL-SECRET"`와 f-string `f"DEMO_API_KEY={DUMMY}\n"`, `git init --bare --initial-branch=main`(02~04는 `-b main`), `rev-parse HEAD`로 `leak_commit`에 해시 담기와 `f"{leak_commit}:.env"`(→ 01절 `git show HEAD~1:.env`처럼 해시 없이 가능), `git add -f`·`git rm .env`·`check-ignore -q`·`diff --cached -- 파일`, `subprocess.run(["git", "filter-repo", …], check=True)` 직접 호출, `clone --mirror`·`push --force --mirror`·`rev-list --objects --all`·`log -S 값 --all --format=%H`, 제너레이터 식 `any(line.endswith(" .env") for …)`(G1)·조건 표현식 `len(…) if … else 0`(G1), 셀 11이 20줄 넘음(G2), `assert` 여러 줄. `git filter-repo`는 lab `pyproject.toml`의 `git-filter-repo==2.47.0`이 설치하는 명령이라, `run_git("filter-repo …")`로 부를 때 커널의 PATH에 가상환경 bin이 있어야 git이 찾음(04에서는 확인하지 않음 — 05에서 실행으로 확인 필요)
- Python 쪽에서 04가 쓴 것: Ch 1 03 종료 코드, Ch 2 01 대입, 03 `in`·`sorted()`, 04 기본값 매개변수·같은 이름 재정의, 05 `with open("r"/"w")`, 07 import·타입힌트, Ch 1 04 `"""…"""`. f-string·`try/except`·`sys`는 04에서 쓰지 않음
- 아직 안 가르친 것(05절이 설명 없이 전제하면 안 됨): `git rm`(파일과 색인에서 함께 지우기 — 01은 `--cached`만), `git add -f`(무시 규칙 무시), `check-ignore -q`, `diff --cached -- 경로`의 `--`, `git log -S`·`--all`·`--format`, `rev-list`, `rev-parse`, `clone --mirror`·`push --mirror`, `push --force` 실행(03·04는 이름만), `git filter-repo` 전체, 해시가 바뀌는 이력 재작성, `git remote add`(02는 clone이 만든 `origin`만), `git gc`·참조 기록 만료 실행, `git reset`을 공개 브랜치에 쓰는 장면, `git restore`·`stash`, 브랜치 삭제(`branch -d`), GitHub 화면(시크릿 스캐닝·푸시 보호). 개념: 시크릿·폐기(revoke)·교체(rotate)·포크·캐시. Python 쪽: `pathlib.Path`·`exists()`, 제너레이터 식·`any()`·`all()`, 조건 표현식, `endswith()`, f-string 안 식(변수만 넣은 f-string은 Ch 2 01), `raise`·`isinstance`, `*args`·`**kwargs`(A 트랙), 메서드 세 번 연결, 타입힌트 `-> None`·`X | None`, `@` 줄·`BaseModel`·픽스처(A 트랙은 Ch 2 09~11절을 건너뜀), `os.environ`·`.env` 읽기(`python-dotenv`는 pyproject에 있으나 Ch 3 노트북에서 아직 안 씀)

## §05 → 실습

(05절 품질 개선 2026-09-16. 결과는 `05-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 17, 모델 호출 0. 05는 챕터 본문의 마지막 절이라 이 메모는 06 실습 절 작업자에게 넘깁니다)

### 05절이 새로 가르친 것

- Git 명령·출력: `git add .`(지금 폴더의 변경을 한꺼번에 색인에 — 무시 규칙에 안 걸린 `.env.local`도 올라감, `A  .env.local`), `git log --oneline --all -S 글자`(그 글자를 넣거나 뺀 커밋만, `--all` = 모든 브랜치와 원격 이름에서. 결과 없으면 명령 줄 아래가 빔), `git clone --no-local 원격 폴더`(출력 `Cloning into '…'...`만), `git remote add origin ../team.git`(출력 없음), `git push --force origin main`(` + 해시...해시 main -> main (forced update)`), `git fetch`의 `(forced update)`, 이력 도구 `git filter-repo --invert-paths --path 경로`(출력 `NOTICE: Removing 'origin' remote`, `Parsed 4 commits`, `HEAD is now at`, `New history written`, `Completely finished after N seconds` — 시간·경로는 읽지 않음). 01절 명령 재사용: `status --short --ignored`(`!! .env`·`?? .env.local`), `check-ignore -v`(`.gitignore:1:.env`, 종료 코드 1 = 걸린 규칙 없음), `diff --cached`, `rm --cached`, `show HEAD~1:파일`
- 개념·용어(용어 표 6개): 시크릿(secret)·폐기와 교체(revoke·rotate, 실행 안 함)·이력 재작성(history rewriting, 바뀐 커밋과 그 뒤 커밋의 해시가 바뀜, 앞 커밋은 그대로)·git-filter-repo(git에 없는 도구, 실습 `.venv`에 설치)·강제 올리기(force push)·글자 검색(`git log -S`). 본문 규칙: 「추적을 멈추면 커밋이 하나 늘 뿐, 지난 커밋에 값이 남음」, 「무시 규칙은 이름이 맞는 파일만 막음(별표 없는 `.env`는 `.env.local`에 안 걸림)」, 「커밋 전 비교 읽기는 사람이 읽어야 효과」, 「순서: 폐기·교체 → 새 복제본에서 재작성 → 강제 올리기 → 팀원 다시 복제」, 「옛 복제본은 원격을 고쳐도 그대로(`ahead 1, behind 2`), 받아 합친 뒤 올리면 값이 돌아올 수 있음(문서 근거, 실행 안 함)」
- 도우미(05에서 새로 만듦, 정의 셀 하나):
  ```python
  import sys


  def run_filter_repo(options: str, folder: str):
      arguments = [sys.executable, "-m", "git_filter_repo"]
      # 옵션 글을 낱말로 나눠 목록 끝에 하나씩 붙입니다
      for word in shlex.split(options):
          arguments.append(word)
      result = subprocess.run(arguments, capture_output=True, encoding="utf-8", cwd=folder)
      print(folder, "$ python -m git_filter_repo", options)
      print(result.stdout + result.stderr)
      if result.returncode != 0:
          print("종료 코드:", result.returncode)
  ```
  이유: `run_git("filter-repo …")`는 커널 PATH에 `.venv` 실행 폴더가 있어야 git이 찾음. 기기 확인(2026-09-16) — `uv run` 안(교재 실행 도구)은 찾음, 가상환경 Python 직접 실행은 `git: 'filter-repo' is not a git command`·종료 코드 1, `sys.executable -m git_filter_repo`는 둘 다 성공. `shlex`·`subprocess`는 앞 셀 `run_git()` 정의에서 import한 것을 씀. `--sensitive-data-removal`은 Git 2.34.1에서 `unknown option 'batch-command'`로 멈춤(도구 README: Git 2.36.0 이상) — 실습에서도 쓰지 않음
- 05 폴더·파일·값: 준비 셀 `mkdtemp(prefix="ch03-05-")`(실습은 `ch03-06-`). `team.git`, `author`(`Ch3 Student`), `reviewer`(05는 커밋하지 않아 config 안 함), `author-clean`(작성자 새 복제본, config 안 함), `reviewer-new`. 변수 `dummy_key = "DEMO-ONLY-NOT-A-REAL-SECRET"`, 파일 쓰기 `"DEMO_API_KEY=" + dummy_key + "\n"`. 파일 `.gitignore`(01절 세 줄 `.env`/`__pycache__/`/`*.log` → 넷째 줄 `.env.local`), `.env`, `settings.example`(`DEMO_API_KEY=replace-me`), `.env.local`, `config.txt`(`discount=10`). 커밋(먼저 만든 순): `chore: 환경 파일 추적 제외` → `docs: 설정 예시 추가` → `feat: 할인율 설정 추가`(더미 키 포함) → `chore: 로컬 설정 파일 추적 제외`. 확인 출력 모양: `print("리뷰어 폴더의 파일:", sorted(file_names))`
- 비유·그림: 삽화 05-5 자물쇠와 다시 싼 상자(창고 문 자물쇠 교체 = 폐기·교체, 열쇠 = 시크릿, 팀 선반 상자 넷 중 셋째 = 더미 키 커밋, 초록 테이프 셋째·넷째 = 새로 쓴 커밋, 수레 = 리뷰어 옛 복제본). 01-5 택배 상자 → 02-6 검수대와 선반 → 03-6 한 칸의 두 카드 → 04-6 취소 상자와 깃발 수첩 → 05-5로 창고 선반을 이어 씀. 색: 커밋·파일 초록, 실행한 명령 파랑, 확인 출력·메모 노랑, 실행하지 않은 단계 회색, Before 결함 결과(검색 두 줄)와 막지 못한 결과(`종료 코드: 1`)만 빨강

### 챕터 전체(01~05)에서 가르친 Git 명령과 개념 — 실습에서 설명 없이 쓸 수 있는 것

| 절 | Git 명령 | 개념·읽는 법 |
|---|---|---|
| 01 | `init -b main`, `config user.name/user.email`(저장소에만), `status --short [--ignored]`, `add 파일`, `commit -m`, `log --oneline`, `diff`, `diff --cached`, `check-ignore -v`, `rm --cached`, `ls-files`, `show HEAD~1:파일` | 저장소·작업 폴더·색인·커밋·추적·무시 규칙·HEAD/`HEAD~1`, 상태 두 칸(`??`·`A `·` M`·`M `·`D `·`!!`), 메시지 앞머리 `chore:`·`feat:`·`fix:`(03에서 `docs:`) |
| 02 | `init --bare -b main 이름.git`, `clone`, `remote -v`, `push -u origin 브랜치`/`push`, `switch -c`/`switch`, `branch`/`-v`/`-vv`, `diff [--stat] origin/main...HEAD`, `fetch`, `merge --no-ff origin/브랜치 -m`, `log --oneline --graph`, `log --oneline -1 이름` | 원격·bare·브랜치·기능 브랜치·PR·코드 리뷰·병합 커밋, 짝(`[origin/main: ahead/behind]`), GitHub Flow 여섯 단계 |
| 03 | 거절된 `push`(`! [rejected]`·종료 코드 1), `merge origin/main -m`, `pull`(fast-forward), 충돌 병합(`CONFLICT`·`UU`·커밋 거절 128), 해결 뒤 `add`→`commit`→`push` | 올리기 거절·갈라진 이력·공통 조상·pull·fast-forward·병합 충돌·충돌 표시 `<<<<<<<`/`=======`/`>>>>>>>` |
| 04 | `revert --no-edit HEAD`, `worktree add -b 새브랜치 ../폴더`/`list`/`remove`, `reset --hard HEAD~1`, `reflog -5`, `branch 이름 HEAD@{1}`, `show 브랜치:파일` | 공개한 커밋·취소 커밋·리셋·참조 기록·`HEAD@{n}`·추가 작업 폴더, 「공개한 커밋은 더해서 취소」, 「해시를 옮겨 적지 않고 git 이름으로」 |
| 05 | `add .`, `log --oneline --all -S 글자`, `clone --no-local`, `filter-repo --invert-paths --path`(`run_filter_repo()`), `remote add origin`, `push --force origin main` | 시크릿·폐기와 교체·이력 재작성·강제 올리기·글자 검색, 대응 순서 |

### 실습에서 이어 쓸 것

- 도우미: `run_git(command: str, folder: str = ".")`(02~05 같은 모양, `import shlex`·`import subprocess` 포함 정의 셀 하나). 필요할 때만 `run_python(file_name, folder)`(02, `import sys`)·`run_filter_repo(options, folder)`(05). 모두 `check=True`가 없어 git이 실패해도 셀이 멈추지 않고 `종료 코드: N` 줄로 읽음
- 셀 모양: 준비 셀 `import os`·`import tempfile` → `practice_folder = tempfile.mkdtemp(prefix="ch03-06-")` → `os.chdir()` → `os.listdir()` `[]`. 파일 쓰기 `with open("폴더/파일", "w"/"a", encoding="utf-8") as file:`, 여러 줄 `"""…"""`, 읽기 `file.read()`+`print("라벨:", 값)`, 폴더 확인 `file_names = os.listdir("폴더")`+`"이름" in file_names`/`sorted(file_names)`. 해시·임시 경로는 결과 읽기에서 인용하지 않고, 출력의 `[사용자 폴더]`는 실행 도구가 가린 표시라고 적음
- 이름: 원격 `team.git`, 작성자 폴더 `author`(`Ch3 Student`·`student@example.com`), 리뷰어 폴더 `reviewer`(`Ch3 Reviewer`·`reviewer@example.com`), 커밋 메시지 앞머리 `chore:`·`feat:`·`fix:`·`docs:`·`merge:`. 파일 후보: `.gitignore` 세 줄(01), `app.py` `print("주문 2건")`(01), `summary.py`·`check_summary.py`(02), `message.txt`·`policy.txt`(03), `config.txt` `discount=10`(04·05), `settings.example`·더미 키(05). Ch 2 주문 데이터(할인율 0.1 = `discount=10`)와 이어짐
- 실습 절 연결: 05 본문 「다음 학습과 이어지는 지점」은 지금 Ch 4를 가리킴(확인한 사실만: Ch 4 첫 절 Pandas 표, Ch 6 01 `.env`의 `OPENAI_API_KEY`, Ch 32 05 Compose 시크릿). 05 노트북 끝 문장은 「다음 챕터 Ch 4에서는 Pandas로 표 데이터를 다루는 것부터 시작합니다.」. 실습 절을 붙이면 둘 다 06 실습 절을 가리키게 고치고, Ch 4 연결 문장은 06 실습 절 끝으로 옮김(`author_05.py` 마지막 셀과 `_src/05` b8)
- 실습 주제 후보(규격 §7-2: 새 명령 없이 앞 절 기능 2~3개): 기능 브랜치에서 `config.txt`를 고치고(02) 올리기 전 `git diff --cached`와 `.gitignore`로 더미 키를 막는 확인(01·05)을 거쳐, 리뷰어와 같은 줄 충돌을 해결(03)하거나 잘못 올린 커밋을 취소(04)하는 흐름. 실행 1·2는 값 하나(예: 환경 파일 이름 `.env` ↔ `.env.local`, 또는 리뷰어가 고치는 줄)만 바꿈. 모델 호출은 0번(Ch 3은 API 키 불필요 — 규격의 「모델 호출 3~5번」은 모델 챕터 기준이므로 Ch 1·2 실습처럼 0번으로 두는 것을 진단에 적을 것)
- 교재 실행 환경: Linux, Python 3.12.13, Git 2.34.1, git-filter-repo 2.47.0(2026-09-16). Git 2.34.1은 git-filter-repo 요구 사항(2.36.0)보다 낮음 — `--invert-paths --path`만 확인함

### 아직 안 가르친 것(실습이 설명 없이 전제하면 안 됨)

- Git: `git restore`·`git stash`·`git rebase`(실행)·`git cherry-pick`·`git tag`, 브랜치 삭제(`branch -d`·`push --delete`), `merge --abort`·`--ours/--theirs` 실행, 갈라진 상태의 `pull`(Git 2.34.1은 설정 없으면 `fatal: Need to specify how to reconcile divergent branches`로 멈춤 — 05 준비 중 따로 확인, 노트북에는 없음), `clone --mirror`·`push --mirror`, `rev-parse`·`rev-list`·`--format=%H` 형식 지정, `git gc`·`reflog expire`, `add -f`·`check-ignore -q`, `.gitignore`의 `!` 부정·`.env*` 같은 넓힌 규칙의 실행, `git commit -a`, `git add -p`/`--interactive`, 커밋 서명, hook·pre-commit·gitleaks 같은 검사 도구, `--sensitive-data-removal`, `--global` 설정 실행
- GitHub: 실제 계정·원격 URL·PR 화면·리뷰 승인·브랜치 보호·병합 버튼·되돌리기 버튼·시크릿 스캐닝·푸시 보호·지원 요청. 네트워크 원격(https·ssh)
- 환경: Windows·macOS 실행, VS Code Git 화면, VS Code 커널의 PATH, 터미널에서 `git filter-repo` 직접 실행
- Python: `pathlib.Path`·`exists()`, 목록 `+`로 잇기, 제너레이터 식·내포식·`any()`·`all()`, 조건 표현식, `endswith()`, f-string 안 식, `raise`·`isinstance`, `*args`·`**kwargs`(A 트랙), 메서드 세 번 연결, 타입힌트 `-> None`·`X | None`, `try/except`(Ch 3에서는 02절 확인 파일 안에서만), `@` 줄·`BaseModel`·픽스처(A 트랙은 Ch 2 09~11절 건너뜀), `os.environ`·`python-dotenv`로 `.env` 읽기(pyproject에 있으나 Ch 3 노트북에서 안 씀), `subprocess.check_output`

## 실습 → 챕터 검토

(06 실습 절 2026-09-16. 결과는 `06-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 16, 모델 호출 0. 챕터 전체 게이트 6/6 PASS `gates-wip-all.json`. 이 메모는 챕터 검토 세션과 `chapter-summary.md` 작성자에게 넘깁니다)

### 06절이 한 것

- 제목 「Git 실습: 할인율 설정 PR 합치기」(slug `06-Git-실습`, experiment, 30분, 따로 과제 없음). 01·02·03·05절 명령을 부품 여섯 개로 묶고 조립 함수 `run_pull_request(run_folder, env_file_name)`로 이음. 04절(revert·reflog·worktree)과 05절 `git-filter-repo`·`--force`는 쓰지 않음(커밋 전에 막는 흐름이라 필요 없음, 본문 b3)
- 재료: `run-1`·`run-2`에 같은 팀(`team.git`, author `Ch3 Student`, reviewer `Ch3 Reviewer`). 작성자 첫 커밋 `chore: 환경 파일 추적 제외`(01절 세 줄), 리뷰어가 먼저 `.venv/`를 더한 `chore: 가상환경 폴더 추적 제외`를 main에 올림(작성자는 받아 오지 않음)
- 부품: `add_on_branch`(`switch -c feature/discount`, `config.txt` `discount=10`과 환경 파일에 더미 키, `git add .`, `git diff --cached` 출력에 더미 문자열이 있는지 반환) → `commit_without_key`(찾았으면 `.gitignore`에 이름 덧붙이기 + `rm --cached` + `add .gitignore`, 커밋 `feat: 할인율 설정 추가`) → `update_branch`(`fetch`, `merge origin/main -m "merge: main의 무시 규칙 받기"`, 종료 코드가 0이 아니면 다섯 줄 규칙으로 덮어써 add·commit, 종료 코드 반환) → `open_pull_request`(`diff --stat origin/main...HEAD` 마지막 줄 `strip()` 반환, `push -u origin feature/discount`) → `merge_pull_request`(리뷰어 `fetch`, `merge --no-ff origin/feature/discount -m "merge: 할인율 설정"`, `push`, `.gitignore` 줄 목록 반환) → `count_key_commits`(`log --oneline --all -S DEMO-ONLY-NOT-A-REAL-SECRET` 줄 수). 기록장 출력은 Ch 2 13 `print_report()`
- `run_git()`은 05절과 같은 본문에 끝줄 `return result`만 더함(Ch 2 04절 반환값). 셀 마지막 줄에 `run_git(…)`만 두면 Jupyter가 반환값을 한 번 더 보여 줄 수 있어, 06은 그런 셀을 만들지 않음(노트북에는 적지 않음)
- 실행 1 `.env`: `색인의 더미 키 | False`, `main 받기 종료 코드 | 0`(`Merge made by the 'ort' strategy.`), `PR 변경 요약 | 1 file changed, 1 insertion(+)`, 규칙 네 줄, `더미 키 커밋 수 | 0`
- 실행 2 `.env.local`: 색인 비교 `+DEMO_API_KEY=DEMO-ONLY-NOT-A-REAL-SECRET` → `rm '.env.local'` → `CONFLICT (content): Merge conflict in .gitignore`·`종료 코드: 1` → 해결, `True`·`1`·`2 files changed, 2 insertions(+)`·규칙 다섯 줄(`.venv/`, `.env.local`)·`0`. 비교 `달라진 칸 수: 5`, 같은 칸은 `더미 키 커밋 수 | 0`. 마지막 셀 `!! .env.local`·`True`
- 그림: 06-1 조립도, 06-2 실행 1 순서(sequenceDiagram), 06-3 두 실행 비교, 삽화 06-4 열쇠를 뺀 상자(01-5 택배 상자 → 02-6 검수대와 선반 → 05-5 열쇠를 이어 씀; 열린 상자 = 색인, 열쇠 = 더미 키 파일, 서랍 = 무시 규칙에 적어 작업 폴더에만 남긴 파일, 파란 상자 = 기능 브랜치 커밋, 수레 = 기능 브랜치, 돋보기 = PR 리뷰, 선반 = main). 색: 함수 파랑, 바꾸는 값 초록, 기록장·확인 노랑, 실행 1의 「일 없음」 회색. 실행 2 충돌(종료 코드 1)과 찾은 더미 키는 코드가 받아 처리·기록한 일이라 노랑(§5-3, Ch 2 13 ValueError와 같은 판단) — 03절 Before의 빨간 충돌과 다름. 빨강 없음

### 바꾼 연결

- `chapter.json` 06 추가. 빌드 index 절 목록에 06 링크(이 챕터는 `_src/index.html`이 없고 노트북 개수 문장도 없음)
- 05 본문 b8 「다음 학습」 → 06절 링크와 실습 소개. 원래의 Ch 4(Pandas)·Ch 6(`.env`의 `OPENAI_API_KEY`)·Ch 32 05(시크릿) 문장은 06 b8로 옮김. 05 노트북·`author_05.py` 끝 문장 → 「다음 06절은 이 챕터의 실습입니다. …」(mdpatch, 05 게이트 0)
- 챕터 밖 미반영(보고만): `textbook/part1/_build_index.py`·`textbook/part1/index.html`의 Ch 3 절 수·목록(Ch 1·2 실습 절도 아직 미반영), `textbook/downloads/` 묶음, 루트 `textbook/qa/upgrade-progress.md`

### 챕터 검토에서 볼 곳

- 06 한 셀 출력 길이(재료 두 셀, 실행 1·2 셀)와 30분 분량
- 06 충돌 해결 글을 함수에 미리 적은 판단(03절 「표시를 읽고 정함」과의 관계, 노트북 5번·b7)과 06-3 충돌 노랑
- 폴더 `run-1`/`run-2`를 함께 바꾼 것과 「값 하나만」 원칙(노트북 10번·b4)
- 05 b8 새 연결 문장이 05의 결론(이력 재작성 순서)과 자연스럽게 이어지는지

### chapter-summary.md에 넣을 후보

- 06 실습 주제·실행 1/2 결과(위), 새로 가르친 Git 명령 없음, `run_git()` 반환값 판(다음 챕터가 Git 도우미를 쓰면 이 판을 이어 쓸 수 있음)
- 반복 예제: `team.git`/`author`/`reviewer`, `Ch3 Student`/`Ch3 Reviewer`, `config.txt` `discount=10`(Ch 2 할인율 0.1), `.gitignore` 세 줄 → `.venv/`·`.env.local`, 더미 문자열 `DEMO-ONLY-NOT-A-REAL-SECRET`, 창고 선반 비유(01-5 → 02-6 → 03-6 → 04-6 → 05-5 → 06-4)
- 아직 안 가르친 것: handoff `## §05 → 실습`의 목록 그대로(06은 새 명령을 더하지 않음). 06이 「실행하지 않음」으로 적은 것: 충돌 표시를 사람이 읽고 고르기(06 안에서), 넓힌 규칙 `.env*`, 받아 오기 실패로 멈춘 병합, GitHub PR 화면
