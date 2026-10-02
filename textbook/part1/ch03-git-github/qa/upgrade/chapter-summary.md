# Ch 03 Git & GitHub 협업 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-16(품질 개선 5절 + 실습 절 06 + 별도 세션 검토 1차 반영 뒤). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6. 앞 챕터 요약: `textbook/part1/ch01-development-environment/qa/upgrade/chapter-summary.md`, `textbook/part1/ch02-python/qa/upgrade/chapter-summary.md`. 절 사이 인계 원문: `qa/upgrade/handoff.md`.
절: 01 커밋과 gitignore · 02 GitHub Flow와 PR 리뷰 · 03 병합 충돌 해결 · 04 revert reflog worktree · 05 시크릿 이력 정리와 예방 · 06 Git 실습(experiment). 01~05는 paired. 모델 호출 0번, API 키 불필요. 코드 셀 112개(19·22·19·19·17·16), 게이트 6/6(G1~G7 0, 수정 전 233건). 모든 저장소는 노트북이 만든 임시 폴더 안에 있고, GitHub 계정·네트워크는 쓰지 않았습니다.

## 1. 새로 가르친 명령·개념·용어

### 절별 Git 명령과 개념

| 절 | Git 명령(노트북에서 실행) | 개념·읽는 법 |
|---|---|---|
| 01 | `init -b main`, `config user.name/user.email`(`--global` 없이 저장소에만), `status --short [--ignored]`, `add 파일`, `commit -m`, `log --oneline`, `diff`(작업 폴더 ↔ 색인), `diff --cached`(색인 ↔ HEAD), `check-ignore -v`(`.gitignore:3:*.log`, 종료 코드 1 = 걸린 규칙 없음), `rm --cached`, `ls-files`, `show HEAD~1:파일` | 저장소·작업 폴더·색인·커밋(색인에 고른 상태 + 메시지)·추적·무시 규칙·HEAD/`HEAD~1`. 상태 두 칸(첫 칸 색인, 둘째 칸 작업 폴더): `??`·`A `·` M`·`M `·`D `·`!!`. 「무시 규칙은 아직 추적하지 않는 파일에만」, 「추적을 멈춰도 지난 커밋 내용은 남음」. 메시지 앞머리 `chore:`·`feat:`·`fix:`(03에서 `docs:`, 02~에서 `merge:`)는 교재의 팀 관례 |
| 02 | `init --bare -b main team.git`, `clone`, `remote -v`, `push -u origin 브랜치`/`push`/`push origin main`, `switch -c`/`switch`(원격에만 있는 이름이면 짝 브랜치를 만듦), `branch`/`-v`/`-vv`(`[origin/main: ahead 3]`, `behind 1`), `diff --stat origin/main...HEAD`/`diff origin/main...HEAD`, `fetch`(`origin/` 이름만 옮김), `merge --no-ff origin/브랜치 -m`, `log --oneline --graph`, `log --oneline -1 이름` | 원격 저장소·bare 저장소·브랜치(줄기 끝 커밋을 가리키는 이름)·기능 브랜치·풀 리퀘스트(PR, GitHub 기능)·코드 리뷰·병합 커밋(부모 둘). 짝(추적 관계를 교재에서 부른 말, upstream 용어는 쓰지 않음), GitHub Flow 여섯 단계, PR 템플릿(루트 `pull_request_template.md`) |
| 03 | 거절된 `push`(`! [rejected] … (fetch first)`, 종료 코드 1), `merge origin/main -m`(갈라진 줄기라 `--no-ff` 없이도 병합 커밋), `pull`(뒤처진 쪽에서만, `Fast-forward`), 충돌 병합(`CONFLICT (content)`, 종료 코드 1), 충돌 중 `status --short`의 `UU`, 해결 전 `commit` 거절(종료 코드 128), 해결 뒤 `add` → `commit` → `push` | 올리기 거절(커밋 줄기를 보고 정함)·갈라진 이력·공통 조상·풀·fast-forward 병합(병합 커밋을 새로 만들지 않고 이름만 앞으로)·병합 충돌·충돌 표시 `<<<<<<<`/`=======`/`>>>>>>>`. 「기준 파일과 비교해 새 줄로 해결」 |
| 04 | `revert --no-edit HEAD`, 취소 커밋 `push`와 리뷰어 `pull`, `worktree add -b 새브랜치 ../폴더`/`list`/`remove`, 이미 쓰는 브랜치 `worktree add`(128), `reset --hard HEAD~1`, `reflog -5`, `branch 이름 HEAD@{1}`, `show 브랜치:파일`, `switch 기존 브랜치` | 공개한 커밋·취소 커밋·리셋·참조 기록(**HEAD가 옮겨 갈 때마다 적는 기록**, 커밋이 그대로여도 브랜치를 바꾸면 한 줄)·`HEAD@{n}`·추가 작업 폴더. 「공개한 커밋은 더해서 취소」, 「해시를 옮겨 적지 않고 git 이름으로 가리킴」, 「한 브랜치는 한 작업 폴더에서만」 |
| 05 | `add .`, `log --oneline --all -S 글자`, `clone --no-local`, `git-filter-repo --invert-paths --path 경로`(도우미 `run_filter_repo()`로 `python -m git_filter_repo` 실행), `remote add origin`, `push --force origin main`(`(forced update)`) | 시크릿·폐기와 교체(실행 안 함)·이력 재작성(바뀐 커밋과 그 뒤 해시가 바뀜)·git-filter-repo(실습 `.venv`에 설치)·강제 올리기·글자 검색. 대응 순서 「폐기·교체 → 새 복제본에서 재작성 → 강제 올리기 → 팀원 다시 복제」, 「무시 규칙은 이름이 맞는 파일만 막음(`.env`는 `.env.local`에 안 걸림)」 |
| 06 | 새 명령 없음. 01·02·03·05절 명령을 부품 함수 여섯 개로 조립 | 실습 절(§3) |

### Python 쪽에서 Ch 3이 새로 쓴 모양 (모두 Ch 1·2 사다리 안)

- 모듈 `shlex`(`shlex.split()` = 따옴표 메시지를 한 낱말로), 글자 `+` 이어 붙이기, `subprocess.run(…, capture_output=True, encoding="utf-8", cwd=폴더)`, 모드 `"a"`(01에서 한 문장으로 풂), 상대 경로 `..`(04), 반환값 `return result`와 `.stdout.splitlines()[-1].strip()`(06), 타입힌트 `: bool`(06, Ch 2 01절 불리언 연결)
- `raise`·`isinstance`·`pathlib.Path`·`check_output`·제너레이터 식·조건 표현식·`*args`·데코레이터·`BaseModel`·반환 타입힌트 `-> None`은 기본 경로 코드 셀 112개에서 0건(검토 AST 확인)

### 용어 표에 넣은 것

저장소·작업 폴더·색인·커밋·추적·무시 규칙·HEAD(01) / 원격 저장소·bare 저장소·브랜치·기능 브랜치·풀 리퀘스트·코드 리뷰·병합 커밋(02) / 올리기 거절·갈라진 이력·공통 조상·풀·fast-forward 병합·병합 충돌·충돌 표시(03) / 공개한 커밋·취소 커밋·리셋·참조 기록·`HEAD@{n}`·추가 작업 폴더(04) / 시크릿·폐기와 교체·이력 재작성·git-filter-repo·강제 올리기·글자 검색(05).

## 2. 반복해 쓴 도우미·데이터·비유·이름

- **도우미 `run_git()`**: 01은 `run_git(command: str)`(현재 폴더), 02~05는 `run_git(command: str, folder: str = ".")`(같은 이름 재정의, 출력 첫 줄 `author $ git …`, 0이 아닌 종료 코드만 `종료 코드: N`, `check=True` 없음 → git이 실패해도 셀은 멈추지 않음). 06은 끝에 `return result`만 더한 판. `run_python(file_name, folder)`(02, `sys.executable`, `text=True`), `run_filter_repo(options, folder)`(05). 뼈대는 모두 Ch 2 08절 `run_pytest()`
- **셀 모양**: 준비 셀 `import os`·`import tempfile` → `practice_folder = tempfile.mkdtemp(prefix="ch03-NN-")` → `os.chdir()` → `os.listdir()` `[]`. 파일 쓰기 `with open("폴더/파일", "w"/"a", encoding="utf-8") as file:`, 여러 줄 `"""…"""`, 읽기 `file.read()` 뒤 라벨 줄 `print("작성자의 message.txt:")` + `print(값)`, 폴더 확인 `"이름" in os.listdir("폴더")`·`sorted(…)`. 해시·임시 경로는 결과 읽기에서 인용하지 않고, 출력의 `[사용자 폴더]`는 실행 도구가 가린 표시라고 적음
- **이름**: 원격 `team.git`, 작성자 폴더 `author`(`Ch3 Student`·`student@example.com`), 리뷰어 폴더 `reviewer`(`Ch3 Reviewer`·`reviewer@example.com`), 05의 `author-clean`·`reviewer-new`, 06의 `run-1`·`run-2`. 브랜치 `main`·`feature/order-summary`(02)·`fix/urgent`·`experiment`·`recovered-idea`(04)·`feature/discount`(06)
- **데이터**: `app.py` `print("주문 2건")` → 3건(01), `.gitignore` 세 줄 `.env`/`__pycache__/`/`*.log`(01, 05·06이 이어 씀) → `.venv/`·`.env.local`(06), `summary.py` `summarize(count)` → `number = int(count)`(02), `message.txt`·`policy.txt`(14시 기준 출고)·`contact.txt`(03), `config.txt` `discount=10`(Ch 2 할인율 0.1과 연결) → `discount=90` → 취소(04) → 05·06, `idea.txt` `첫 주문 쿠폰 아이디어`(04), 더미 문자열 `DEMO-ONLY-NOT-A-REAL-SECRET`과 `DEMO_API_KEY=…`(05·06), `settings.example` `DEMO_API_KEY=replace-me`(05)
- **비유(창고 선반 이어 쓰기)**: 01-5 택배 상자(책상 = 작업 폴더, 열린 상자 = 색인, 봉한 상자 = 커밋) → 02-6 검수대와 선반(선반 = main, 수레 = 기능 브랜치, 검수대 = PR 리뷰) → 03-6 한 칸의 두 카드(칸 = 파일의 한 줄, 받침에 세운 기준판 = `policy.txt`) → 04-6 취소 상자와 깃발 수첩(깃발 = 브랜치 이름, 수첩 = 참조 기록) → 05-5 자물쇠와 다시 싼 상자(열쇠 = 시크릿, 자물쇠 교체 = 폐기·교체, 초록 테이프 = 해시가 바뀐 커밋, 수레 = 옛 복제본) → 06-4 열쇠를 뺀 상자(서랍 = 무시 규칙에 적어 작업 폴더에만 남긴 파일)
- **그림 색 규칙**: 저장소·커밋·파일·작업 폴더 초록, 실행한 명령·함수 파랑, 상태 표시·짝 비교·확인 출력·메모 노랑, 브랜치 이름·실행하지 않은 단계 회색. 잘못된 커밋 자체는 성공한 커밋이라 초록(04·05). **git 명령이 0이 아닌 종료 코드를 내도, 코드가 반환값으로 받아 처리하고 셀이 끝까지 가면 노랑(06-3). 사람이 멈춘 명령을 마주한 장면과 Before 결함 결과는 빨강(01-4·03-1~4·05-2)**
- **sequenceDiagram 규칙(검토 1차에서 정함)**: 받아 오기는 실선 요청 → 점선 응답. 라벨이 세로선과 겹치면 첫 줄 `%%{init: {"sequence": {"messageAlign": "left"}}}%%` + 한 줄 라벨(`<br>` 금지). 본문 SVG는 viewBox 약 868 이하여야 `visual.cjs` 14px를 통과(02-3·04-2·05-3·06-2 참고)

## 3. 06 실습 절 주제와 결과

- 「Git 실습: 할인율 설정 PR 합치기」(experiment, 30분, 모델 호출 0번, 따로 과제 없음). 조립 함수 `run_pull_request(run_folder, env_file_name)`가 부품 `add_on_branch` → `commit_without_key` → `update_branch` → `open_pull_request` → `merge_pull_request` → `count_key_commits`를 부르고 기록장(칸 여섯 개)을 Ch 2 13절 `print_report()` 모양으로 출력. 리뷰어가 먼저 `.venv/` 규칙을 main에 올려 둔 같은 팀 저장소 두 벌(`run-1`·`run-2`)
- 실행 1 `.env`: `색인의 더미 키 | False`, `main 받기 종료 코드 | 0`(`Merge made by the 'ort' strategy.`), `PR 변경 요약 | 1 file changed, 1 insertion(+)`, 규칙 네 줄, `더미 키 커밋 수 | 0`
- 실행 2 `.env.local`(값 하나만 바꿈): 색인 비교에 `+DEMO_API_KEY=DEMO-ONLY-NOT-A-REAL-SECRET` → 규칙에 이름을 더하고 `rm '.env.local'` → `CONFLICT (content): Merge conflict in .gitignore`·종료 코드 1을 함수가 받아 두 규칙을 남겨 해결 → `True`·`1`·`2 files changed, 2 insertions(+)`·규칙 다섯 줄·`0`. `달라진 칸 수: 5`, 같은 칸은 더미 키 커밋 수 0. 마지막 셀 `!! .env.local`·`True`
- 결론 범위: 「이름이 다른 환경 파일 한 가지로 관찰한 것」으로 한정. 04절 revert·reflog와 05절 이력 재작성은 실습에서 쓰지 않음(커밋 전에 막는 흐름)

## 4. 다음 챕터(Ch 04 데이터 도구: Pandas·관계형 테이블·SQL·REST·문서 파싱)가 이어받을 것

- 「앞에서 배운 내용」에 쓸 수 있는 것: Ch 1·2 요약의 문법 전부 + 이 챕터의 준비 셀 모양(`tempfile.mkdtemp(prefix=…)`+`os.chdir()`+`os.listdir()`), `with open(…, encoding="utf-8")`의 모드 `"w"`/`"r"`/`"a"`, `subprocess.run`과 종료 코드 읽기, 「출력의 어느 줄을 읽는가」 결과 읽기 방식, 커밋·`.gitignore`·`git diff --cached`로 올리기 전에 확인하는 습관
- Ch 4 노트북(개선 전, 2026-09-16 확인)이 쓰는 것 중 **Ch 1~3에서 가르치지 않은 것**: `import pandas as pd`(별명 import — Ch 2 요약 §5 미교육), `from pathlib import Path`·`TemporaryDirectory`(Ch 3은 `mkdtemp` 문자열 경로만 씀), `raise`(01·02·03), 목록 내포식(03), `BaseHTTPRequestHandler` 상속과 `threading`(04), f-string 안 식(04). 규격 §2-3대로 바꾸거나 처음 쓰는 자리에서 한 문장씩 풉니다
- 임시 폴더 준비 셀은 Ch 3처럼 `mkdtemp(prefix="ch04-NN-")`로 맞추면 Ch 2 08절·Ch 3과 이어집니다. 데이터 파일을 저장소에 둘지 설명할 일이 생기면 01절 무시 규칙과 05절 「비밀 값은 커밋하지 않음」을 한 문장으로 연결할 수 있습니다
- Ch 6 01절(`part2/ch06-langchain-start/_src/01`)은 `.env`의 `OPENAI_API_KEY`만 적고 `.gitignore`·커밋 전 확인은 적지 않았습니다. Ch 6 작업 때 「환경 파일이 무시 규칙에 걸리는지 `git status --short --ignored`로 확인」 한 문장을 이어 넣을지 검토합니다(검토 1차 06-4). Ch 32 05절(Compose 시크릿)도 05절 대응 순서와 연결할 수 있습니다
- 실행 도구 명령을 노트북에서 부를 때는 `sys.executable -m 모듈`로 부르면 커널 PATH에 좌우되지 않습니다(05 `run_filter_repo()` 근거: 가상환경 Python 직접 실행에서 `git: 'filter-repo' is not a git command`)
- 외부 도구 버전이 출력에 영향을 주면 준비물에 기준 버전을 적습니다(규격 §6에 추가한 규칙)

## 5. 아직 가르치지 않은 것 (다음 챕터가 전제하면 안 되는 것)

- Git: `restore`·`stash`·`rebase`(실행)·`cherry-pick`·`tag`, 브랜치 삭제(`branch -d`·`push --delete`), `merge --abort`·`checkout --ours/--theirs` 실행, 갈라진 상태의 `pull`(Git 2.34.1은 설정 없으면 `Need to specify how to reconcile divergent branches`로 멈춤 — 문장으로만), `clone --mirror`·`push --mirror`, `rev-parse`·`rev-list`·`--format` 형식 지정, `gc`·`reflog expire`, `add -f`·`check-ignore -q`, `.gitignore`의 `!` 부정·`.env*` 넓힌 규칙, `commit -a`·`add -p`, 커밋 서명, hook·pre-commit·gitleaks, `--sensitive-data-removal`, `--global` 설정 실행, 브랜치별 참조 기록 `브랜치@{n}`
- GitHub: 실제 계정·원격 URL(https·ssh)·PR 화면·리뷰 승인·브랜치 보호·병합 버튼·되돌리기 버튼·시크릿 스캐닝·푸시 보호. 실행한 PR은 모두 임시 폴더 bare 원격에서 흉내 낸 것
- 환경: Windows·macOS 실행, VS Code Git 화면, VS Code 커널의 PATH, 터미널에서 `git filter-repo` 직접 실행
- Python: `pathlib.Path`·`exists()`, `TemporaryDirectory`, 목록 `+`로 잇기, 내포식·제너레이터 식·`any()`·`all()`, 조건 표현식, `endswith()`, f-string 안 식, `raise`·`isinstance`, `import 모듈 as 별명`, `try/except`(Ch 3에서는 02절 확인 파일 안에서만), `os.environ`·`python-dotenv`로 `.env` 읽기(pyproject에 있으나 노트북에서 안 씀), `subprocess.check_output`

## 6. Ch 2에서 넘어온 A·B 트랙 제약 (그대로 유지)

- A 트랙(기본 경로)은 Ch 2 09~11절(데코레이터 `@` 줄·컨텍스트 매니저 원리, Pydantic `BaseModel`·`Field`·`ValidationError`, 패키징·픽스처)을 건너뜁니다. Ch 3은 이 문법을 한 번도 쓰지 않았으므로 **A 학생 기준 전제는 Ch 2 요약 §5와 같습니다**
- 규격 §2-2: Part 2 이후 절이 `@` 줄이나 `BaseModel`을 처음 쓰면 세 문장으로 뜻을 풀고 Ch 2 09·10절을 링크합니다. `*args`·`**kwargs`·`*목록` 풀어 넘기기도 A 트랙 미교육
- 타입힌트는 기본 경로에서 `매개변수: int/str/float/bool = 기본값`과 `-> int/str`까지만 씀(Ch 3이 `: bool`을 한 번 더함)

## 7. 기준 Git 버전

- 필수 **2.28 이상**(`git init -b main`), 교재 출력 **Linux Git 2.34.1**(2026-09-16, Python 3.12.13, git-filter-repo 2.47.0), 05절 도구 설명서 요구 **2.36.0 이상**(새로 설치하면 2.36 이상 권장). 01·05 노트북 준비물과 실습 폴더 `README.md`에 적음
- 05절 `--invert-paths --path`는 2.34.1에서 끝까지 실행됨(도구 소스상 2.36 기능 경로를 쓰지 않음). `--sensitive-data-removal`은 2.34.1에서 `unknown option 'batch-command'`로 멈춰 노트북에 넣지 않음. 이 옵션을 기본 경로에 넣으려면 2.36 이상 환경에서 05절만 다시 실행해 origin 처리(지우지 않음 → `remote add` 단계 불필요)를 확인한 뒤 넣음
- 새 Git에서는 안내 문구(hint 줄 등)가 조금 다를 수 있다고 각 절 주의 메모에 적음. Windows·macOS 설치본 버전과 출력은 확인하지 않음

## 8. 강사 확인 대상

- 02절 강의·실습 범위: 강의 6~8번(기능 브랜치·올리기·PR 범위)과 11~12번(리뷰와 병합), 1~5번과 9~10번은 셀을 함께 실행하고 결과 읽기는 실습 시간에(검토 Q4). 02는 새 Git 명령이 챕터에서 가장 많음(코드 셀 22, 검사 문장 455)
- 기준 Git 버전 표기(01·05 준비물, README)와 05절 `--sensitive-data-removal` 제외 판단
- 04절 복구를 `HEAD@{1}`로 가리키는 방식(쓰기 직전 번호 재확인 주의 메모)과 참조 기록 정의 「HEAD가 옮겨 갈 때마다」
- 06 실습의 충돌 해결 글을 함수에 미리 적은 설계와 노랑 표시, 폴더 `run-1`/`run-2`
- 규격에 더한 세 규칙(§6 외부 도구 기준 버전, §5-3 sequenceDiagram 받아 오기·왼쪽 정렬, §5-4 삽화 저장본 대조)
- 교체한 삽화 05-5(채택 job 결과)와 그대로 둔 삽화 03-6(받침 기준판)

## 9. 남은 것

- 다운로드 묶음: `textbook/downloads/part1-practice.zip` 안 Ch 3은 개선 전 노트북 5개(06 없음), `ch03-practice.zip`은 없음. 전체 마감 때 일괄 재생성
- Part 목차: `textbook/part1/_build_index.py`(Ch 3 절 수 5)와 `textbook/part1/index.html`. 전체 마감 때 재생성
- 정리 대상(삭제하지 않고 목록만): `figures/01-commit-ignore.excalidraw`·`.svg`, `figures/02-flow-review.*`, `figures/03-merge-conflict.*`, `figures/04-recovery-tools.*`, `figures/05-secret-response.*`(옛 도식, 본문에서 뺌), `figures/_gen_figures.py`·`figures/__pycache__/`(옛 도식 생성기), `qa/figures-01-05.json`(옛 도식 기록), `qa/final-visual.log`(개선 전 visual 기록), `qa/upgrade/gates-wip-*.json`(절 작업 중간 기록), 챕터 루트 `__pycache__/`, `textbook/_notebook/checks/--chapter/`(챕터 밖, Ch 2 요약에도 있음)
- `집필점검표.md` 아래 체크 목록은 개선 전(2026-09-09) 기록이라 검토 1차 반영 때 현재 기준 문장을 덧붙임
- 2차 검토(`review-round1.md` 끝 「반영 결과」의 볼 곳), 강사 확인

- **§2-7 리팩터(2026-09-21)**: 도구 파일 `labs/part1/ch03-git-github/notebooks/git_tools.py`(`run_git(command, folder=".")` 02절 판 · `print_report(report)` Ch 2 13절)를 만들어 03·04·05는 `run_git`, 06은 `print_report`를 준비 셀에서 `os.chdir()` 전에 가져옴(06의 반환 판 `run_git`은 노트북에 둠). 코드 셀 112 → 108, 코드 줄 553 → 526(도구 파일 포함 539), 출력·인용 변화 없음, 게이트 6/6·verify·visual 8/8 PASS. 세부 `qa/upgrade/handoff.md` 「§2-7 확인」.
