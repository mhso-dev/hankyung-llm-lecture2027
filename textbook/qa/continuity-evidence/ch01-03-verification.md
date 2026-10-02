# Ch 1~3 챕터 연결성 수정 후 검증

## 수정 결과

2026-09-10에 Ch 1→Ch 2→Ch 3→Ch 4 경계의 수정 후 본문과 학생용 노트북을 다시 대조했다. 노트북 셀 번호는 markdown과 code를 모두 포함한 1부터 시작하는 전체 셀 번호다.

| 수정 파일 | 최종 연결 관계 | 검증 근거 |
|---|---|---|
| `textbook/part1/ch01-development-environment/_src/05-Git과-Docker-준비.html`:110 | Ch 2는 Ch 1의 Python 3.12·uv 환경을 쓴다. Git 상태와 커밋은 Ch 3의 임시 저장소에서 처음 실습한다. | Ch 2 README 3~13행의 `uv sync --locked`·Python 3.12 커널, Ch 3 노트북 01 셀 3~12의 `repo`·`git()`과 일치한다. |
| `textbook/part1/ch02-python/_src/12-async와-await.html`:9 | Ch 3은 Ch 2의 파일·외부 명령 실행을 Git에 적용하고, Ch 4는 동기 데이터 처리를 먼저 배운다. async는 Ch 18·30에서 재사용한다. | Ch 3 노트북 01~05의 `subprocess.run()`, Ch 4 노트북 01~05의 동기 코드를 직접 확인했다. |
| `textbook/part1/ch03-git-github/_src/02-GitHub-Flow와-PR-리뷰.html`:5 | 02절은 01절의 커밋 원칙을 적용하지만 산출물은 직접 읽지 않는다. 새 커널에서 별도 임시 저장소를 만든다. | Ch 3 노트북 02 셀 3 `workspace`, 셀 4 `remote`·`author`, 셀 6 `feature/order-summary`과 일치한다. |
| `textbook/part1/ch03-git-github/_src/05-시크릿-이력-정리와-예방.html`:9 | Ch 4는 Ch 3의 임시 저장소를 입력으로 쓰지 않고 별도 프로젝트·제공 데이터로 시작한다. Git의 시크릿 예방과 diff 확인 습관을 후속 프로젝트에 적용한다. | Ch 4 `_src/01-Pandas로-표-다루기.html`:4의 독립 실행 설명과 노트북 01 셀 3~13의 자체 입력·`fetch_orders()` 구현과 일치한다. |
| `labs/part1/ch03-git-github/README.md`:10 | 버전 확인 명령이 `git-filter-repo` CLI의 소스 커밋 해시가 아닌 설치된 Python 패키지 버전을 출력한다. | `uv run python -c "from importlib.metadata import version; print(version('git-filter-repo'))"` → `2.47.0`. `pyproject.toml`과 `uv.lock`의 고정 버전과 일치한다. |

수정한 `_src` 4개를 `_build.py`로 빌드했다. 생성 HTML에도 같은 설명이 반영되었고 기존의 잘못된 문구 `이번에는 그 커밋을`과 `Ch 4에서는 안전하게 공유한 저장소 위에서`는 소유 범위의 `_src`·생성 HTML에 남지 않았다.

## 실행·배포 검증

### 챕터 빌드

```text
for chapter in textbook/part1/ch01-development-environment textbook/part1/ch02-python textbook/part1/ch03-git-github; do
  (cd "$chapter" && uv run --with pillow==12.1.1 --with nbformat==5.10.4 python _build.py)
done
```

결과: Ch 1 5개, Ch 2 12개, Ch 3 5개 절과 각 `index.html`을 오류 없이 재생성했다.

### HTML·노트북 일치 검증

```text
uv run --with nbformat==5.10.4 python textbook/_notebook/verify.py --chapter textbook/part1/ch01-development-environment
PASS 5 sections / 25 code cells (max 19 lines)

uv run --with nbformat==5.10.4 python textbook/_notebook/verify.py --chapter textbook/part1/ch02-python
PASS 12 sections / 76 code cells (max 22 lines)

uv run --with nbformat==5.10.4 python textbook/_notebook/verify.py --chapter textbook/part1/ch03-git-github
PASS 5 sections / 30 code cells (max 22 lines)
```

### 학생용 환경 시작 경로

세 실습 폴더에서 각각 `uv sync --locked`와 `uv run python --version`을 실행했다. 모두 의존성 해석과 잠금 파일 검사를 통과했고 `Python 3.12.13`을 출력했다. README의 대표 명령은 다음 결과를 냈다.

```text
Ch 1: uv run python hello.py              -> 총액: 6000원
Ch 2: uv run python -m pytest --version   -> pytest 9.1.1
Ch 3: uv run python -c "...version('git-filter-repo')..." -> 2.47.0
system: git --version                     -> git version 2.50.1 (Apple Git-155)
```

### 새 커널 연결 실행

저장소 원본 출력을 덮어쓰지 않도록 Ch 2 07절과 Ch 3 01절 노트북을 임시 복사했다. 각 챕터의 `.venv/bin/python`을 절대 경로로 지정하고 `textbook/_notebook/execute.py`로 새 커널 실행했다.

```text
PASS ch02-07.ipynb: 6 cells
PASS ch03-01.ipynb: 6 cells
ch02-07.ipynb code_cells 6 errors 0 execution_counts [1, 2, 3, 4, 5, 6]
ch03-01.ipynb code_cells 6 errors 0 execution_counts [1, 2, 3, 4, 5, 6]
```

첫 시도에서 상대 `--kernel-python` 경로를 지정해 커널 시작 전 `FileNotFoundError`가 발생했다. 같은 검증을 절대 경로로 다시 실행해 위 결과로 통과했다. 노트북 코드의 실패가 아니라 검증기에 넘긴 커널 경로의 표기 문제였다.

### 수정 전 노트북·실행 출력 보존

`before-manifest.json`의 SHA-256 값과 Ch 1~3 실습 디렉터리의 현재 파일의 SHA-256을 비교했다. 노트북 22개와 코드·데이터·잠금 파일은 일치했고, 실제 오류를 수정한 Ch 3 README 1개만 달라졌다.

```text
scoped notebooks 22 unchanged 22
expected lab mismatches 1: labs/part1/ch03-git-github/README.md
missing 0
```

노트북 파일 전체가 바이트 단위로 일치하므로 코드, markdown, 실행 출력, 실행 번호, 커널·검증 메타데이터가 모두 보존되었다. 소유 범위에서 수정 전과 달라진 파일은 `_src` 4개, 대응하는 생성 HTML 4개, Ch 3 README 1개다.

## 자체 의미 검토와 남은 제한

- 수정한 문장의 챕터 번호·함수명·실행 관계를 노트북과 다시 대조했다. 새로 산출물을 전달한다는 주장을 추가하지 않았고, 독립 실행과 개념 적용을 구분했다.
- Ch 4는 소유 범위 밖이므로 수정하지 않았다. 현재 Ch 4 01절은 이전 커널과 프로젝트 모듈을 사용하지 않는다고 이미 명시하므로, Ch 3의 후속 설명만 바로잡으면 두 쪽이 일치한다.
- 코드와 도식은 변경하지 않아 새 API 호출과 도식 재생성은 하지 않았다.
- 이 기록은 작성자 자체 검토까지를 담는다. 프로젝트 전체의 작성자와 분리된 한국어·최종 의미 감사는 총괄 검증 단계에서 수행해야 한다.
