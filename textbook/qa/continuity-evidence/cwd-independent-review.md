# 학생용 노트북 87개 cwd 독립성 감사

## 범위와 방법

2026-09-10의 현재 `labs/part*/ch*/notebooks/*.ipynb` 87개를 직접 읽었다. 기존 QA의 PASS는 근거로 쓰지 않았다. JSON의 모든 code cell에서 `Path(...)`, `open(...)`, `read_*`, `write_*`, `labs/`, `data/`, `runs/`, `cwd=`, `Path.cwd()`, `find_dotenv(usecwd=True)`, 외부 명령 문자열을 검색했다. 검색 결과는 첫 준비 셀이 경로 기준을 어떻게 만드는지 뒤의 사용 셀과 함께 대조했다.

노트북 셀은 markdown과 code를 모두 포함한 1부터 시작하는 전체 셀 번호다. 학생이 README에 따라 챕터 폴더를 열었을 때의 cwd와 Jupyter가 노트북 파일의 `notebooks` 폴더를 cwd로 사용하는 경우를 모두 확인했다. 배포 최상위 폴더를 cwd로 쓰라고 명시한 명령은 그 안내와 함께 판정했다.

## 최종 판정

| 분류 | 노트북 수 | 판정 |
|---|---:|---|
| code cell에 `labs/` 경로가 있는 노트북 | 31 | 모두 배포 최상위를 먼저 찾거나, 찾은 최상위와 상대 경로를 결합한다. 챕터 cwd와 `notebooks` cwd에서 같은 입력·로그 경로를 가리킨다. |
| code cell에 `labs/` 경로가 없는 노트북 | 56 | 셀 안의 값만 쓰거나 `TemporaryDirectory`·`gettempdir()` 아래에 파일을 만든다. `find_dotenv(usecwd=True)`만 쓰는 API 예제는 현재 cwd에서 상위 폴더로 `.env`를 찾는다. |
| 합계 | 87 | **최종 현재 파일에서 미해결 cwd 결함을 발견하지 못했다.** |

감사 첫 스캔에서는 Ch 12 01~06이 `Path("labs/part3/ch12-retrieval-tuning/data")`와 `Path("labs/part3/ch12-retrieval-tuning/runs")`를 cwd에 바로 붙이는 결함을 확인했다. 챕터 cwd에서는 `.../ch12-retrieval-tuning/labs/part3/...`를, `notebooks` cwd에서는 `.../notebooks/labs/part3/...`를 찾아 입력을 읽지 못했다. 이 문제는 이미 수정 담당이 확정된 항목이었다. 공유 작업공간에 수정이 반영된 뒤 87개를 처음부터 다시 스캔했으며, Ch 12 01~06도 아래와 같이 통과했다.

## 최종 경로별 근거

### 임시 폴더 기준

- Ch 1 02 셀 3은 `TemporaryDirectory()`로 `workspace`와 `project`를 만든다. 셀 5의 `Path("data/message.txt")`는 상대 경로 표기를 보여 주는 값이며 실제 파일은 `project / "data" / "message.txt"`에 쓴다.
- Ch 1 03 셀 5의 `env_a`·`env_b`는 임시 폴더 아래에 있다. 셀 7의 `Path("bin/python")`과 `Path("Scripts/python.exe")`는 각 가상환경 경로에 결합된다.
- Ch 1 04~05, Ch 2 05·07·08·11, Ch 3 01~05, Ch 4 01·03, Ch 8 02의 파일·저장소·캐시는 `TemporaryDirectory()`나 `gettempdir()` 아래에서 생성된다. 외부 명령에도 해당 임시 폴더를 `cwd=`로 지정한다.

### 배포 최상위 탐색 기준

다음 준비 셀은 `Path.cwd()`와 모든 상위 폴더를 순서대로 확인하고 `labs/...` 표지가 있는 배포 최상위를 찾는다. 아래 표의 모든 표지를 챕터 cwd와 `notebooks` cwd에서 각각 탐색했으며 두 경우 모두 실제 배포 최상위를 반환했다.

| 구간 | 준비 셀과 표지 | 챕터 cwd | `notebooks` cwd |
|---|---|---:|---:|
| Ch 4 05 → Ch 5 01 | Ch 4 05 셀 3, Ch 5 01 셀 5: `labs/part1/ch04-data-tools/data/article-text.json` | PASS | PASS |
| Ch 6 06 → Ch 7 08 | Ch 6 06 셀 16, Ch 7 08 셀 11: `labs/part2/ch06-langchain-start` | PASS | PASS |
| Ch 7 08 → Ch 8 06 | Ch 7 08 셀 19, Ch 8 06 셀 9: `labs/part2/ch07-prompt-engineering` | PASS | PASS |
| Ch 9 | 01·02 셀 4, 06 셀 4: `labs/data/rag-corpus` | PASS | PASS |
| Ch 10 | 01·02·03·04 셀 4, 08 셀 15: 공용 corpus 또는 Ch 10 폴더 | PASS | PASS |
| Ch 11 | 01~06 셀 3: `labs/data/rag-corpus/manifest.json` | PASS | PASS |
| Ch 12 01~06 | 각 노트북 셀 4: `labs/part3/ch12-retrieval-tuning/data` | PASS | PASS |
| Ch 12 07~12 | 각 노트북 셀 3: `labs/part3/ch12-retrieval-tuning` | PASS | PASS |

Ch 12 01~06은 최종 상태에서 다음과 같이 입력과 로그 기준을 함께 고정한다.

| 노트북 | 최상위·챕터 경로 준비 | 로그 경로 |
|---|---|---|
| 01 | 셀 4 `course_root`, `chapter_dir`, `data_dir` | 셀 14 `runs = chapter_dir / "runs"` |
| 02 | 셀 4 `course_root`, `chapter_dir`, `data_dir` | 셀 15 `runs = chapter_dir / "runs"` |
| 03 | 셀 4 `course_root`, `chapter_dir` | 셀 14 `runs = chapter_dir / "runs"` |
| 04 | 셀 4 `course_root`, `chapter_dir`, `data_dir` | 셀 14 `runs = chapter_dir / "runs"` |
| 05 | 셀 4 `course_root`, `chapter_dir`, `data_dir` | 셀 16 `runs = chapter_dir / "runs"` |
| 06 | 셀 4 `course_root`, `chapter_dir`, `data_dir` | 셀 16 `runs = chapter_dir / "runs"` |

최종 정규식 검사에서 `Path("labs/...`) 형태는 Ch 7 08 셀 11의 `ch06_relative`와 Ch 8 06 셀 9의 `ch07_relative` 두 곳만 남았다. 두 변수는 단독으로 읽지 않고 각각 `course_root / ch06_relative`, `course_root / ch07_relative`로 결합하므로 cwd에 의존하지 않는다.

`find_dotenv(usecwd=True)`를 사용하는 Ch 6~10·12의 API 노트북은 현재 cwd에서 상위로 `.env`를 찾는다. 챕터 cwd와 `notebooks` cwd 모두 배포 최상위 `.env`에 도달한다.

### 명령 문자열의 cwd

- Ch 9 06 셀 18은 `uv run --project labs/part3/ch09-rag-first-run ... labs/part3/.../06-실험-하네스.ipynb`를 출력한다. 직전 markdown 셀 17이 이 명령을 압축 해제한 `part3-practice` 최상위 폴더에서 실행하라고 명시하므로 정상이다.
- Ch 11 06 셀 11의 `subprocess.run(command, cwd=root, ...)`은 `evaluate.py`와 `runs`를 Ch 11 폴더에서 절대 경로로 만든 뒤 배포 최상위를 cwd로 지정한다.
- Ch 12 README의 `uv sync --locked --project labs/part3/ch12-retrieval-tuning`은 “압축을 푼 폴더에서” 실행하라는 문장 바로 아래에 있어 명령과 cwd 안내가 일치한다.

## 재검증 결과와 제한

```text
student notebooks: 87
notebooks containing code-cell `labs/`: 31
remaining notebooks: 56
unanchored Path("labs/...") after final rescan: 0
chapter/notebooks cwd root-resolution probes: PASS 16/16
```

Ch 6 06, Ch 7 08, Ch 8 06은 현재 준비 셀의 정적 경로 탐색이 두 cwd를 모두 통과했다. 실제 연속 실행은 해당 수정 담당의 실행 증거와 합쳐야 한다. 이 감사는 경로 독립성에 한정한 읽기 전용 검토이며 API·PostgreSQL·Docker·로컬 CrossEncoder의 성공 여부는 각 챕터 실행 검증 기록에서 다룬다.
