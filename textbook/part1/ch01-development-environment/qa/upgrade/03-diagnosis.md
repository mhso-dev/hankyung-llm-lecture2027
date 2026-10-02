# 03-Python과-가상환경 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/03-environments.*`).
생성기: `qa/upgrade/author_03.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch01-development-environment 03`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 1 | 0 |
| G2 | 0 | 0 |
| G3 | 3 | 0 |
| G4 | 0 | 0 |
| G5 | 6 | 0 |
| G6 | 38 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 4 | 14 (준비 1 + 본 경로 13, 심화 셀 없음) |
| 검사한 문장 | 160 | 282 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Linux aarch64 기기 VM, uv 0.12.3, 2026-09-16 01:55 UTC), verify PASS(5절 49셀). 빌드 HTML 1280px·390px에서 가로 넘침 없음(scrollWidth 1280/390, 로컬 puppeteer, `qa/upgrade/_shot03/`).

## 수정 전 주요 문제

- G1: 운영체제 분기를 조건 표현식 `Path(...) if os.name == "nt" else Path(...)`로 작성
- G2 밖 가독성: `lines_a[0] == lines_b[0] == "True"` 연쇄 비교, 한 줄 90자 넘는 `subprocess.run(...)`, 세미콜론으로 이은 `-c` 코드 문자열, f-string 출력
- G3: 코드 셀 3개 첫 줄 주석 없음
- G5: 제목 셀·「오늘 볼 그림」 없음. 결과 읽기 셀 없음(설명 셀이 코드 앞에만 있음)
- G6: 코드 이름+조사로 시작하는 문장 29개(「`subprocess.run`의」, 「`check=True`는」, 「uv로」 등), 70자 초과 9개, 5문장 넘는 단락 1개. 실행 예제 설명 단락 5개가 `import`·`shutil.which`·`subprocess.run`·`sys.prefix`·`assert`를 한 번에 풀어 씀
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 Excalidraw 도식 `03-environments.svg`의 「초록 환경 A·B, 노란 확인 단계」 설명이 셀 출력 값과 1:1로 이어지지 않음
- 내용: 「가상환경이 패키지 설치 위치를 나눈다」고 설명했지만 실제로 확인한 것은 폴더 위치뿐. 앞 절(01 예상→비교, 02 임시 폴더·relative_to)과 이어지는 장치 없음

## 바꾼 것

- 노트북(experiment, 학습 질문·env_a/env_b·uv venv·sys.prefix 비교 유지): 제목 셀(준비물 「API 키 불필요」, 호출 0번·비용 없음·1분 이내, uv 필요, Python 3.12가 없으면 내려받을 수 있음) → 오늘 볼 그림(03-2) → 준비(import 6개) → 커널 Python 버전 `3.12.13`·가상환경 여부 `True` → uv 찾기 `True` → 02절 방식 임시 폴더(만들기 전 `False`) → env_a 만들기(폴더·pyvenv.cfg `True`) → env_b(예상 → `True`) → 여러 줄 if/else로 `env_a/bin/python` 경로 → env_a Python이 알려 준 폴더 `env_a`·가상환경 `True` → env_b(예상 → `env_b`) → 두 환경 비교(폴더 다름 `True`, 기반 같음 `True`) → **실험**: `import ipykernel`을 커널 Python(`0`)과 env_a Python(`1`)에서 실행 → 오류 마지막 줄 `ModuleNotFoundError: No module named 'ipykernel'` → **값 바꿔 보기**: `import json`을 env_a에서 `0` → cleanup `False` → 정리
- 새 실험 추가 이유: 기존 본문의 「패키지 설치 위치를 나눈다」를 실제 출력으로 뒷받침. 네트워크 없이 재현되는 조건(프로젝트 의존성 `ipykernel`은 커널 환경에만 있고, `uv venv`로 만든 환경은 비어 있음)만 씀
- 사다리: 기본 경로는 대입·print(쉼표 인자)·`==`/`!=`·`is not None`·여러 줄 if/else·인덱싱(`[0]`, `[-1]`)·`assert`와 준비 셀의 표준 라이브러리 import(환경 챕터 예외(`QUALITY-UPGRADE.md` §2 끝)로 표준 라이브러리 import와 그 결과 값의 메서드를 쓰고, import나 점(.)으로 부르는 메서드·속성이 있는 코드 셀에 `upgrade_allow=["stdlib-import"]`를 적음), 경로 값·실행 결과의 메서드와 속성만 사용. f-string·조건 표현식·연쇄 비교 제거. 명령 목록은 변수에 담은 뒤 `subprocess.run()`에 넣음
- 이어짐: 01절의 `platform.python_version()`·`.startswith("3.12")`·「실행 전에 예상」·「값 하나만 바꿔 원인 말하기」, 02절의 `tempfile.TemporaryDirectory()`·`workspace`·`is_dir()`/`is_file()`·`relative_to()`·`cleanup()`·「경로를 이어 붙이기만 해서는 폴더가 생기지 않음」·`course-ch01` 구분을 그대로 이어 씀
- 본문 10블록 전체를 다시 씀. 사물함 비유(줄 = 기반 Python, 칸 = 환경 폴더, 붓 = 패키지, 빈 칸 = 새 env_a), 용어 7개 표(프로젝트 → 표준 라이브러리로 교체), 실습 폴더 세 가지 표, 함수·값 5행 표, 「이 절의 질문」, 실행하지 않은 범위 명시, 복습 5문항(01·02절 형식)
- 그림: Mermaid 4장(03-1 준비 순서, 03-2 두 환경, 03-3 값 흐름, 03-4 불러오기 비교) + 삽화 1장(03-5 사물함, 1회 생성 채택). 기존 Excalidraw 도식은 본문에서 뺌(원본은 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 사실 주장 확인

- 실행 출력으로 확인(2026-09-16, 기기 VM): `uv sync --locked --project labs/part1/ch01-development-environment` 종료 0(「Checked 38 packages」), `uv run python --version` → `Python 3.12.13`, `.venv`의 `pyvenv.cfg`에 `home =` 절대 경로가 적힘, uv venv 폴더에 `pyvenv.cfg`·`bin/python` 생성, 새 환경 site-packages에 `ipykernel` 없음
- uv 0.12.3 `--help`로 확인: `uv sync --locked` = 「Assert that the uv.lock will remain unchanged」, `uv venv --no-project` = 「Avoid discovering a project or workspace」, `--seed`를 주지 않으면 pip 등을 넣지 않음
- Python 3.12 공식 문서(2026-09-16 조회): `sys.prefix != sys.base_prefix`로 가상환경 판별, Windows는 `Scripts`·POSIX는 `bin`, `pyvenv.cfg`의 `home` 키, 가상환경은 옮기거나 복사하지 않고 새로 만듦, 활성화는 필수가 아님, `sys.platform`은 Windows에서 `'win32'`, `returncode`는 「보통」 0이 성공, `check=True`는 0이 아니면 예외, args 목록에 경로 값 허용
- `qa/research.md`(2026-09-09) 범위: `uv run`이 활성화 없이 프로젝트 환경에서 실행, VS Code `Python: Select Interpreter`·`Select Kernel`, 인터프리터와 노트북 커널이 다를 수 있음, `.venv`는 재생성 가능한 결과물
- 확인 필요: 명령 팔레트 단축키(`Ctrl+Shift+P`/`Cmd+Shift+P`)는 기존 본문에서 유지했고 research.md에 출처가 없음. Windows에서 `uv venv`가 `Scripts/python.exe`를 만들고 `cleanup()`이 오류 없이 지우는지는 실행하지 않음(본문에 미확인으로 적음). 학생 컴퓨터에 Python 3.12가 여러 개 있을 때 두 환경의 기반 Python이 같은지는 이번 한 환경에서만 봄(본문은 「이번 실행에서」로 한정, assert는 폴더가 다른지에만 씀)

## 검토에서 볼 곳

- 새 실험(`import ipykernel` 커널 0 / env_a 1)이 학습 질문 「두 환경이 나뉘는지 확인」과 이어지는지, 기존 「패키지 충돌은 실행하지 않았다」 경계가 유지되는지
- 03-4의 빨강은 실제 실패(env_a의 ModuleNotFoundError) 한 곳. 03-1 「아니요」 분기는 실행하지 않아 회색
- 04절(아직 개선 전) 「앞에서 배운 내용」의 「3절에서는 프로젝트 안에 .venv를 만들고 Python 3.12를 선택」과 이 절의 준비 순서가 맞는지. 04절이 인터프리터·커널을 다시 정의하므로 04절 개선 때 이 절 용어를 이어받게 할 것

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 1·하 3, 공통 C-1 중·C-3 하·C-4 하). 모두 반영했습니다.
- C-1(중): 코드 셀 14개 중 13개 `upgrade_allow=["stdlib-import"]`(두 환경 비교 셀은 점 호출이 없어 표시 없음)
- 03-1(중): 준비 설명에 「코드에서 `import` 뒤에 적어 불러오는 Python 기능 묶음 한 단위를 모듈(module)이라고 합니다.」, 용어 표에 모듈 행(새 용어 8), [34] 「패키지를 설치하면 그 안의 모듈을 불러올 수 있습니다. 새로 만든 env_a에는 `ipykernel` 패키지를 설치하지 않아 같은 이름의 모듈을 찾지 못했습니다.」
- C-3(하): 「모듈 `tempfile`과 경로 기능 `Path`는…」
- 03-2(하): `shutil.which()` 기준을 「이 노트북의 Python이 찾을 수 있는」으로 고치고, 설치 전에 열어 둔 VS Code에서 못 찾을 수 있다는 안내와 「이번에 실행하지 않았습니다」를 한 단락으로 추가(Python 문서: path 생략 시 프로세스의 PATH)
- 03-3(하): 03-1 도식 읽기에 회색 상자 설명과 「이 분기는 이번에 실행하지 않았습니다」. 03-4(하·C-4): 「인터프리터와 커널을 고르는 VS Code 화면은…」

재실행: `run_section.sh … 03`(새 커널 PASS, 뒤이어 [34] 한 문장을 `mdpatch.py`+`--no-exec`로 고침, 코드 셀 출력은 수정 전과 글자 단위로 같음) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 84 code cells (max 14 lines)`, `visual.cjs` 7페이지 × 1280·390px 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 강사 확인(2차 검토는 보고서 「다음 조치」 4대로 중 항목과 C-4 문장만 대조하면 됨)
- 실습 묶음 `textbook/downloads/ch01-practice.zip` 재생성(C-2, 전체 챕터가 끝난 뒤 일괄)
