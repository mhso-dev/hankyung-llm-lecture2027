# Ch 01 오리엔테이션 · 개발환경 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-16(품질 개선 + 실습 절 + 검토 1차 반영 뒤). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6.
절: 01 과정 지도와 학습 규칙 · 02 도구 설치와 터미널(paired) · 03 Python과 가상환경 · 04 첫 스크립트와 디버거(paired) · 05 Git과 Docker 준비 · 06 개발환경 실습. 모델 호출 0번, API 키 불필요.

## 1. 새로 가르친 문법·API·용어

### 문법 (사다리 L1 + 환경 챕터 예외)

| 절 | 문법 | 설명 수준 |
|---|---|---|
| 01 | 대입 `=`, 곱셈 `*`·뺄셈 `-`, 비교 `==`와 `True`/`False`, `print(라벨, 값)`(쉼표 인자), 목록 `[ ]`, 여러 줄 `for`, 번호 늘리기 `number = number + 1`, `len()`, 검사 줄 `assert` | 「이름」에 값을 저장한다는 수준. 「이름과 값의 규칙은 Ch 2에서」라고 적음 |
| 01 | `import`(뜻만), 함수·반환값·문자열의 한 문장 정의 | 「`import`는 Python에 들어 있는 기능 묶음을 불러오는 줄입니다. 자세한 뜻은 Ch 2에서 배웁니다」 |
| 02 | 메서드(점 뒤 이름과 괄호), 인자(괄호 안에 건네는 값), 변수(값을 저장한 이름) | 한 문장 정의만 |
| 03 | `!=`, `is not None`과 `None`, 여러 줄 `if/else`, 인덱스 `[0]`·`[-1]` | 목록 번호는 0부터(04에서 다시) |
| 03 | 모듈(`import` 뒤에 적는 기능 묶음 한 단위)과 패키지(따로 설치하는 기능 묶음)의 구분 | 용어 표 |
| 04 | 여러 줄 글 `"""…"""`, 연산자 `in`·`not`·`and`, 여러 줄 `if` | f-string은 `hello.py` 글 안의 `f"총액: {total}원"`을 읽기만 함(노트북 출력에는 쓰지 않음) |
| 05 | 연산자 `or` | — |
| 02(심화 셀만) | `try/except FileNotFoundError`, `type(error).__name__` | `lesson_level="deep-dive"`, 「이 문법은 Ch 2에서 배우므로 출력만 읽습니다」 |

환경 챕터 예외: 표준 라이브러리 import(`platform`·`tempfile`·`pathlib.Path`·`sys`·`shutil`·`subprocess`)와 그 결과 값의 메서드를 씀. 해당 셀 메타데이터 `upgrade_allow=["stdlib-import"]`.

### API (절에서 처음 쓴 곳)

- 02 `tempfile.TemporaryDirectory()`·`.name`·`cleanup()`, `Path()`와 `/` 잇기, `is_dir()`·`is_file()`·`mkdir()`·`write_text(…, encoding="utf-8")`·`read_text()`·`relative_to()`
- 01·03 `platform.python_version()`·`startswith()`, 03 `sys.prefix`·`sys.base_prefix`·`sys.platform`·`sys.executable`, `shutil.which()`, `subprocess.run(목록, check=True, capture_output=True, text=True)`·`.stdout`·`.stderr`·`.returncode`(종료 코드), `splitlines()`
- 04 `strip()`·`replace()`·`removeprefix()`, `subprocess.run(…, input=글)`, `python -m pdb`와 명령 `b 3`·`c`·`p 이름`·`n`·`q`
- 05 `subprocess.run(…, cwd=폴더)`, `git --version`·`git init`·`git status --short`(`??`·`A`·`M`·0줄)·`git add`·`git -c user.name=… -c user.email=… commit --quiet -m`·`git diff`(기록할 목록과 파일 비교), `docker --version`·`docker version --format {{.Server.Version}}`
- 터미널: `pwd`/`Get-Location`, `ls`/`Get-ChildItem`, `cd`, `uv --version`, `uv sync --locked`, `uv run python --version`, `uv run python hello.py`, `uv venv --python 3.12 --no-project`, `python -c`
- VS Code: File → Open Folder, Terminal → New Terminal, 확장(Python·Jupyter·Python Debugger), `Python: Select Interpreter`, Select Kernel. F5·F10·Shift+F5와 VARIABLES는 안내만 하고 실행하지 않음

### 용어 (용어 표에 넣은 것)

프로그램·셀·입력·출력·검증·목록·반복문(01) / 편집기·터미널·셸·현재 작업 폴더·경로·절대 경로·상대 경로(02) / 인터프리터·모듈·패키지·표준 라이브러리·가상환경·의존성·잠금 파일·커널(03) / 스크립트·확장자·논리 오류·디버거·중단점·한 줄 실행(04) / Git·저장소·커밋·GitHub·Docker·클라이언트·데몬(05). 본문 정의만: 함수·반환값·문자열(01), 메서드·인자·변수(02), 종료 코드(03).

## 2. 반복해 쓴 예제 데이터·비유·이름

- **단가 3000 × 수량 2 = 6000**(01 셀 → 04 `hello.py` → 05 Git 기록 → 06 점검). 수량 3 → 9000(01·04), 틀린 예상 5000(01), 덧셈으로 잘못 쓴 3002(01 복습 → 04 Before). 이름 `price`·`count`·`total`·`prediction`·`new_count`
- **`hello.py` 네 줄**: `price = 3000` / `count = 2` / `total = price * count` / `print(f"총액: {total}원")`, 예상 출력 `"총액: 6000원"`. 실습 폴더의 실제 파일도 네 줄로 맞춤(검토 1차)
- **임시 폴더 `workspace`**(`tempfile.TemporaryDirectory()`, 끝에 `cleanup()`), **연습 폴더 `practice/data/message.txt`** 글 `"안녕, 터미널!"`, `base_folder`·`relative_path`(02·06)
- **폴더 이름 규칙**: 「실습 폴더」 = 교재가 준비한 `labs/part1/ch01-development-environment`(`.venv`·`hello.py`·`notebooks`). 「연습 폴더」 = 학생이 만든 빈 폴더 `course-ch01`(02)이나 노트북이 만든 `practice`(06)
- 03 `env_a`·`env_b`, `ipykernel`(커널 0 / env_a 1, `ModuleNotFoundError`), `import json` 0. 04 `price_bug.py`·`price_fixed.py`·`price_changed.py`. 05 `user.name=Ch1 Student`·`user.email=student@example.com`, `git_path`·`status_command`, 여섯 가지 준비 상태(Python 3.12·uv 응답·가상환경·Git 응답·Docker 클라이언트·Docker 서버)
- **학습 순서**: 예상 적기 → 실행 → 출력 확인 → 비교 → 값 하나만 바꿔 다시(01에서 정하고 모든 절이 「실행 전에 예상합니다」로 따름). 「실행하지 않은 것」을 따로 적는 습관
- **비유와 삽화**: 메모와 영수증(01) · 두 방 책상 서랍의 편지(02, 방 = 기준 폴더) · 한 줄 사물함(03, 칸 = 환경 폴더) · 조리대 그릇과 멈춤(04, 빈 셋째 그릇 = 아직 없는 total) · 리모컨과 빠진 플러그(05, 리모컨 = 클라이언트) · 두 방과 가방 속 필통(06, 02 비유를 이어 씀)
- 그림 색: flow 파랑, tool(값·파일) 초록, measure 노랑, fail 빨강(실제 실패만), 실행하지 않은 분기 회색

## 3. 06 실습 절 주제와 결과

- 주제 「새 연습 폴더 점검하기」: 1~5절의 확인 여섯 가지(Python 3.12·가상환경·`data/message.txt`·`python hello.py`·`git status --short` 0줄·docker 찾기)를 점검표 `check_names`로 모으고, 작업 폴더 `base_folder` 하나만 바꿔 두 번 점검
- 실행 1(practice): True 5칸, Docker만 `명령을 찾지 못함` False
- 실행 2(한 칸 위 임시 폴더): True 2칸, 달라진 칸 3(파일 False, hello.py 종료 코드 2 `can't open file`, git 종료 코드 128 `not a git repository`). Python·가상환경·Docker 칸은 같음
- 교재 실행 환경: Linux aarch64 기기 VM, Python 3.12.13, uv 0.12.3, git 2.34.1, docker 없음(2026-09-16)

## 4. 다음 챕터(Ch 2 파이썬)가 이어받을 것

- 실행 환경: 챕터마다 실습 폴더에서 `uv sync --locked` → 인터프리터·커널에서 `.venv` → 첫 셀부터 `Shift+Enter`. 06의 점검표 순서로 먼저 확인해 볼 수 있다고만 적음(Ch 2에 점검 단계를 강제하지 않음)
- Ch 1이 「Ch 2에서 배웁니다」로 미룬 약속: 이름과 값의 규칙(01), `import`의 자세한 뜻(01, 규격상 Ch 2 07절), `try/except`(02 심화), 함수·반환값·문자열·변수·인자·메서드·모듈은 한 문장 정의만 했으니 Ch 2가 제대로 정의함
- 「앞에서 배운 내용」에 쓸 수 있는 것: 예상 → 실행 → 비교 순서, `==`·`assert`, 목록과 `for`, `print(라벨, 값)`, 종료 코드 0/0 아님, 논리 오류와 pdb로 멈춰 값 보기, 상대 경로와 기준 폴더
- 예제 이어 쓰기 후보: 단가 3000·수량 2(`price`·`count`·`total`), `hello.py`, 예상 출력 `총액: 6000원`
- 05 A/B 트랙 자가진단: B 트랙은 「Ch 2의 확장 과제를 함께 합니다」, A 트랙은 「Ch 2의 변수, 조건문, 함수를 차례로」. Ch 2에 확장 과제가 없으면 05 문장을 고쳐야 함. 공식 배치 기준은 `[[미정]]`(HTML 주석)
- Ch 3(Git): 05에서 `git init/add/commit`(`-c`로 이름 한 번만), `status --short`, `diff`까지만 함. 저장소에 이름 적기(`git config`)·`.gitignore`·브랜치·GitHub는 Ch 3 몫이라고 적음

## 5. 아직 가르치지 않은 것 (Ch 2 앞부분이 전제하면 안 되는 것)

- 문법: 함수 정의 `def`와 `return`, `elif`, `while`·`break`·`continue`, `range()`·`enumerate()`, 목록 `append()`·슬라이싱, 딕셔너리·튜플·집합, 자료형 이름(`int`·`str`·`float`·`bool`)과 형 변환, `input()`, f-string으로 출력 만들기(읽기만 함), `with open(...)`, 예외 처리 작성, 클래스, 내포식·조건 표현식, 타입힌트, 모듈을 직접 만들기
- 도구: `pip install`/`uv add`로 패키지 추가, `.env`와 API 키, 모델 호출(Ch 6), `git config`·`.gitignore`·브랜치·원격 저장소·GitHub, Docker 이미지·컨테이너
- 실행하지 않은 화면: VS Code 디버거 GUI(F5·F10), 인터프리터·커널 선택 화면, OS별 설치 화면, Windows 경로·오류 출력, Docker가 설치된 컴퓨터의 출력
