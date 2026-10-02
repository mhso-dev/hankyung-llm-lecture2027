# Ch 1 실행 검증 기록

- 실행일: 2026-09-09
- 검증 환경: macOS, Python 3.12.13, uv 0.11.6
- 고정 도구: ipykernel 7.3.0, nbclient 0.11.0
- 실행기: `textbook/_notebook/execute.py`
- 커널: 노트북별 새 Python 3.12 커널, `allow_errors=False`

## 준비 명령 검증

```bash
uv lock --project labs/part1/ch01-development-environment
uv sync --locked --project labs/part1/ch01-development-environment
uv run --project labs/part1/ch01-development-environment python --version
uv run --project labs/part1/ch01-development-environment python labs/part1/ch01-development-environment/hello.py
```

실제 출력은 `Python 3.12.13`과 `총액: 6000원`이었습니다. 또한 따로 만든 임시 폴더에서 `uv venv --python 3.12`와 `uv run --python 3.12 hello.py`를 실행했으며, 같은 총액을 확인했습니다. 임시 폴더 경로는 기록에 남기지 않았습니다.

## 노트북 실행 결과

| 노트북 | 코드 셀 | 실제 관찰 결과 |
| --- | ---: | --- |
| 01 과정 지도와 학습 규칙 | 4 | 예상 6,000원, 실행 6,000원, 개수 3개로 변경 후 9,000원 |
| 02 도구 설치와 터미널 | 5 | `data/message.txt` 정상 읽기, 잘못된 기준에서 `FileNotFoundError`, 기준 수정 후 성공 |
| 03 Python과 가상환경 | 4 | Python 3.12 확인, 두 `sys.prefix`가 다름, 두 실행 모두 가상환경 내부 |
| 04 첫 스크립트와 디버거 | 5 | 정상 6,000원, Before 3,002원, pdb에서 `price=3000`, `count=2`, `total=3002`, After 6,000원 |
| 05 Git과 Docker 준비 | 7 | Git 저장소 초기 상태는 비어 있음, 파일 생성 후 `?? hello.py`, Docker 클라이언트와 데몬 응답 각각 확인 |

전체 명령은 다음 결과로 끝났습니다.

```text
PASS 01-과정-지도와-학습-규칙.ipynb: 4 cells
PASS 02-도구-설치와-터미널.ipynb: 5 cells
PASS 03-Python과-가상환경.ipynb: 4 cells
PASS 04-첫-스크립트와-디버거.ipynb: 5 cells
PASS 05-Git과-Docker-준비.ipynb: 7 cells
```

## 정적 검사

코드 셀의 최대 길이는 순서대로 6, 9, 15, 19, 18줄입니다. 모두 25줄 이하입니다. 노트북과 `hello.py`에서 미완성 표시, `NotImplementedError`, 개인 절대 경로, API 키 이름을 검색했으며 발견하지 못했습니다.

## 확인 필요 항목

Docker 결과는 검증 호스트의 관찰값입니다. 이 호스트에서는 클라이언트와 데몬이 모두 29.4.1로 응답했습니다. 학습자의 컴퓨터에서는 05번 노트북을 실행해 클라이언트 설치와 데몬 연결을 각각 확인해야 합니다. Docker 앱 설치, 데몬 시작, 컨테이너 실행은 이 검증의 범위에 포함하지 않았습니다.

VS Code와 다른 운영체제의 그래픽 디버거 화면은 검증하지 않았습니다. 04번의 표준 라이브러리 `pdb`를 통한 중단점과 변수 출력은 실제 실행했습니다.
