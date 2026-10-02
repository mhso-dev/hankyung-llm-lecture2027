# 03 Python과 가상환경 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 03-5 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 칸은 따로지만 벽과 바닥은 함께 씁니다. | 값 없음(비유). 사물함 줄 = 기반 Python, 칸 = 환경 폴더, 붓 = 설치한 패키지, 빈 칸 = 새 env_a | — |
| 03-2 | 4 핵심 개념 · 가상환경이 나누는 것 (노트북 「오늘 볼 그림」) | Mermaid flowchart TD | 두 환경은 같은 기반 Python을 함께 쓰지만, 환경 폴더는 따로 있습니다. | 노트북 [환경마다 들어 있는 Python] 셀 `env_a/bin/python`·`env_b/bin/python`, [환경 폴더 묻기] 셀 `env_a`·`env_b`, [두 환경 비교] 셀 `환경 폴더가 서로 다른가: True`·`기반 Python 폴더가 같은가: True`, [가상환경 만들기] 셀 `pyvenv.cfg 파일이 있는가: True` | 폴더·실행 파일 tool(초록), 비교 measure(노랑) |
| 03-1 | 5 실행 예제 · 노트북을 열기 전에 | Mermaid flowchart TD | 터미널에서 `uv sync --locked`를 실행해 프로젝트 환경을 준비합니다. | 기기 셸 실행(2026-09-16, uv 0.12.3) `uv sync --locked` 종료 0, `uv run python --version` → `Python 3.12.13`. 노트북 [Python 확인] 셀 `가상환경 안에서 실행 중인가: True` | 행동 flow(파랑), 확인 measure(노랑), 실행하지 않은 「아니요」 분기 회색 |
| 03-3 | 5 실행 예제 · 노트북 뒤 | Mermaid flowchart TD | env_a의 Python을 직접 실행해 환경 폴더와 기반 Python 폴더를 출력하게 합니다. | 노트북 [환경 폴더 묻기] 셀 `env_a Python이 알려 준 환경 폴더: env_a`, `env_a는 가상환경인가: True`, 경로 `env_a/bin/python` | 이름에 저장된 값 tool(초록), 비교 measure(노랑) |
| 03-4 | 6 실험 결과 해석 | Mermaid flowchart TB(세 칸 비교) | 패키지는 설치한 환경에서만 불러올 수 있습니다. | [실험] 셀 `커널 Python 종료 코드: 0`, `env_a Python 종료 코드: 1`, [오류 마지막 줄] 셀 `ModuleNotFoundError: No module named 'ipykernel'`, [값 바꿔 보기] 셀 `env_a Python 종료 코드: 0` | 실행한 코드 tool(초록), 성공 결과 measure(노랑), 실제 실패한 env_a의 ipykernel 불러오기 fail(빨강) |

색 규칙: 폴더·실행 파일·이름에 저장된 값·실행한 코드 글자는 네 그림 모두 초록입니다(01·02절과 같음). 학생이 터미널과 VS Code에서 하는 행동은 파랑입니다. 비교와 확인 결과는 노랑이고, 실제로 실패한 env_a의 `import ipykernel` 결과 한 곳만 빨강입니다. 03-1의 「아니요」 분기는 이번에 실행하지 않은 절차라 빨강 대신 회색으로 둡니다(01-1·02-2와 같은 방식).
