# Ch 8 — 컨텍스트 엔지니어링 실습

학생 실습의 기준 파일은 `notebooks/`에 있는 절별 Jupyter Notebook 7개(07은 챕터 끝 실습)입니다. 각 노트북은 빈 커널에서 시작하며, 개념 설명 다음의 짧은 코드 셀을 위에서부터 실행합니다. 예제 데이터는 셀 안에 포함되어 있어 별도 프로젝트 모듈을 가져오지 않습니다.

노트북의 첫 코드 셀은 필요한 패키지 버전을 설치합니다. 다음 셀은 현재 작업 폴더에서 상위 폴더로 올라가며 `.env`를 찾고 `OPENAI_API_KEY`의 존재만 확인합니다. 키 값은 출력하거나 노트북에 저장하지 않습니다. 모델은 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`로 만들고, 02절부터는 출력 예약분을 `max_tokens`로 줍니다. 메시지 목록은 `invoke()`에 전달합니다.

| 절 | 노트북 |
|---|---|
| 01 | `notebooks/01-컨텍스트와-토큰-예산.ipynb` |
| 02 | `notebooks/02-Write와-Select.ipynb` |
| 03 | `notebooks/03-Compress와-Isolate.ipynb` |
| 04 | `notebooks/04-네-가지-실패-모드.ipynb` |
| 05 | `notebooks/05-Context-rot-측정.ipynb` |
| 06 | `notebooks/06-단계적-공개와-설계-비교.ipynb` |
| 07 | `notebooks/07-컨텍스트-엔지니어링-실습.ipynb`(챕터 끝 실습, 파일을 쓰지 않음) |

노트북을 새 Python 3.12 커널에서 연 뒤 첫 셀부터 순서대로 실행합니다. 프로젝트 루트의 `.env`에 `OPENAI_API_KEY`가 필요하며, 노트북은 키의 존재 여부만 확인하고 값을 출력하지 않습니다. API 응답의 표현은 실행할 때마다 달라질 수 있으므로 출력 원문과 자동 확인 결과를 함께 읽습니다.

챕터 폴더를 VS Code에서 열고 `uv sync --locked`를 실행한 뒤 이 폴더의 `.venv`를 노트북 커널로 선택합니다.

`runs/context-design-continuity.json`은 06 노트북이 쓴 세 설계 비교 기록 파일입니다. `runs/continuity/<실행 시각>/`에는 06 노트북을 실행할 때마다 기록 파일과 같은 내용의 사본을 새 폴더로 남깁니다. 지금은 교재 출력을 만든 실행의 사본 하나(`20260917T121654`)가 있습니다. `runs/ex01_budget.jsonl`, `ex04_failures.jsonl`, `ex05_rot.jsonl`, `ex06_compare.jsonl`은 예전 프로젝트 모듈을 실행한 증거이며 현재 학생 노트북의 출력으로 사용하지 않습니다.

06 노트북은 이 챕터의 `notebooks` 폴더, 실습 폴더 맨 위, 프로젝트 맨 위 가운데 한 곳에서 엽니다. 경로를 고를 때 `runs`와 `notebooks` 폴더가 있는지만 보므로, 다른 챕터의 실습 폴더에서 열면 그 챕터 폴더를 골라 그 챕터의 `runs`에 기록 파일을 씁니다. 06 노트북은 Ch 7 08 노트북이 만든 `labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json`을 읽고, 그 파일의 지문을 출처로 적습니다.
