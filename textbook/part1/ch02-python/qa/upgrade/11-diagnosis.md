# 11-패키징과-테스트-격리 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/11-concept.*`).
생성기: `qa/upgrade/author_11.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 11`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01~10절 개선본(`_src`, `author_08.py`·`author_10.py`, `09-diagnosis.md`·`10-diagnosis.md`, `10-figures.md`, 06-5 삽화 프롬프트), `qa/upgrade/handoff.md`(특히 `## §10 → §11`), `upgrade_gates.py`, Ch 1 03 노트북(uv venv·ModuleNotFoundError 셀), 뒤 챕터 확인용 Ch 30 02·Ch 33 01 `_src`와 Ch 33 01 노트북.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 1 | 0 |
| G2 | 4 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 12 | 0 |
| G6 | 22 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 9 | 19 (준비 2 + example 8 + before 4 + after 5(심화 2)) |
| 검사한 문장 | 114 | 423 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, uv 0.12.11, pytest 9.1.1, 2026-09-16, 오류 출력·색 기호 0), verify PASS(12절 164셀). 수정 후 수치는 `gates-wip-11.json`, 수정 전은 `gates-before.json`(덮어쓰지 않음). 빌드 HTML 가로 넘침 없음(puppeteer 1280px·390px에서 scrollWidth 1280·390, SVG 5·삽화 1, 남은 `{{` 토큰 없음).

## 수정 전 주요 문제

- **G1·G2**: 조건 표현식 `"Scripts/python.exe" if os.name == "nt" else "bin/python"`, 15줄 넘는 셀 4개(빌드·설치·import를 한 셀에, 테스트 파일 쓰기와 실행을 한 셀에)
- **G1이 잡지 않은 사다리 문제**: `next((root / "dist").glob("*.whl"))`(제너레이터 첫 항목), `%pip install`, `pathlib.Path`·`TemporaryDirectory`(Ch 2에서 안 씀), 테스트 파일 안 `items: list[str]`·`-> None`(아직 안 배운 타입힌트), monkeypatch 테스트 안의 함수 안의 함수 `fake_status`, 준비 셀에 import 네 줄을 몰아 둠, `stdout.strip().splitlines()[-1]`
- **이어짐 결함**: 데이터 `report_tools.make_title("  agent log  ")`·alpha/beta·`status_service`가 1~10절 주문 데이터와 무관. 「10절의 Pydantic은 필수 선행 지식이 아닙니다」는 맞지만, 8절 `run_pytest()`·결과 줄 읽기, 6절 `items = []` 공유, Ch 1 3절 `uv venv`·`ModuleNotFoundError`를 받지 않음. 「Ch 18에서 API 클라이언트를 모듈로 관리」는 Ch 18 본문에서 확인되지 않음(Ch 18 `_src`에 pytest·패키지 없음)
- **Before/After 구조**: 실패 설명(E 줄)을 출력하지 않고 요약 줄 한 줄만 봄. 「혼자 실행하면 통과」가 없어 격리 문제가 순서 문제라는 점이 출력으로 드러나지 않음. monkeypatch 예제는 Before/After와 별개인데 기본 경로에 있음
- G5: 제목 셀·「오늘 볼 그림」 없음, 결과 읽기 셀 없음. G6: 코드·영문 이름으로 시작하는 문장 14개(「`pyproject.toml`에」「pytest의」「monkeypatch는」 등), 70자 초과 6개, 5문장 넘는 단락 2개. G7: Excalidraw 도식 1장뿐, Mermaid 0장, 삽화 0장, 설계표 없음

## §10이 넘긴 판단 거리

- **Before 고르기(메인 지시: `int()` 빠뜨림 네 번째 반복 금지)**: 이 절 학습 질문(공유 상태 → 테스트 실패)에 맞는 기존 실패 구조를 유지. 데이터는 6절 Before의 클래스 본문 `items = []`와 두 주문 `['노트', '연필']`을 그대로 이어 테스트 파일 맨 위 `items = []`에 노트·연필을 담는 두 테스트로 바꿈. E 줄 `assert ['노트', '연필'] == ['연필']`이 6절 출력과 같은 목록
- **L6 `@pytest.fixture`**: 테스트 파일 글 안에만 있지만 노트북 11번 설명과 본문 「테스트 격리와 픽스처」에 「이 줄은 아래 함수 items를 픽스처로 등록합니다. 9절 `@` 줄과 같은 규칙」을 적음. `upgrade_allow` 없음
- **8절 테스트 파일 쓰기·`__pycache__` 글자 수 주의**: `run_pytest()`는 8절 본문 그대로 다시 정의. 같은 이름 test_items.py를 159 → 217글자로 다시 씀
- **기존 11절 데이터(휠 빌드·격리 venv·monkeypatch)**: 휠은 8절 After price_tools.py(295글자)를 `src/price_tools/__init__.py`로 옮겨 만듦. 새 환경은 Ch 1 3절 모양(`uv venv`, pyvenv.cfg, `sys.platform == "win32"` 분기, `python -c` 코드 글). monkeypatch는 심화 셀로 옮기고 함수 안의 함수를 파일 맨 위 함수로 바꿈
- **타입힌트**: 기본 경로 함수 `run_pytest() -> int`만 정의. 테스트 파일 글의 테스트 함수·픽스처에는 8절처럼 적지 않음(`list[str]`·`-> None`은 아직 안 배움)
- **뒤 챕터 연결 문장**: 「Ch 18 API 클라이언트를 모듈로」는 뺌. Ch 30 2절(`_src` b6 「첫 테스트 뒤 재정의를 남겨 다음 질문도 대체 응답」)과 Ch 33 1절(`_src` 「pytest·Ruff·wheel 빌드」, 종료 코드 판정)은 본문에서 확인한 내용만 적음

## 바꾼 것

- 노트북(paired 유지): 제목 → 오늘 볼 그림(11-1) → 준비(`uv 0.12.11`, 임시 폴더 `[]`) → 패키지 폴더(`295`, `['__init__.py']`) → pyproject.toml(`125`, `['pyproject.toml', 'src']`) → `uv build --wheel --color never`(`Successfully built dist/price_tools-0.1.0-py3-none-any.whl`, 0, `['.gitignore', …whl]`) → zipfile로 휠 안 이름 6개 → `uv venv install_env`(0, `install_env/bin/python`, pyvenv.cfg True) → `uv pip install`·`uv pip list`(`price-tools 0.1.0`) → 새 환경 Python `-c`(`78000`, 0) → 값 바꿔 보기: python_path를 `sys.executable`로(`ModuleNotFoundError: No module named 'price_tools'`, 1) → Before: `run_pytest()` 정의 → test_items.py 맨 위 `items = []`(159) → 실행(`.F`, E 줄, `test_items.py:11`, `1 failed, 1 passed`, 1) → `test_items.py::test_add_pencil`만(`1 passed`, 0) → After: 픽스처 판(217) → 실행(`..`, `2 passed`, 0, assert) → `--setup-show`(`SETUP    F items` 두 번) → 원리 더 알아보기(심화): order_status.py(131)와 monkeypatch 테스트(`4 passed`) → 정리
- **학습 목표 조정**: 「빌드 시스템 선언과 휠」→ 패키지 폴더·pyproject.toml 두 구역·휠 안의 파일, 「격리된 위치에 설치하고 새 프로세스에서 가져오기」→ 설치한 환경의 Python에서만 불러와짐(커널 Python 대조), 「fixture와 monkeypatch로 목록·환경 변수 분리」→ 픽스처로 테스트마다 새 목록(monkeypatch는 심화, 환경 변수 `setenv`는 실행하지 않음)
- 본문 10블록 전체를 다시 씀. 「앞에서 배운 내용」 표 6행(Ch 1 3절·4/6절·5/7절·7/8절·8절·9절), 용어 8개 표(패키지·배포 이름과 import 이름·빌드·빌드 백엔드·휠·테스트 격리·픽스처·monkeypatch), 소제목 「패키지 폴더와 설정 파일」「빌드와 휠」「테스트 격리와 픽스처」「설치한 환경의 Python에서만 불러와짐」「새 가상환경에 설치한 이유」「확인한 범위」, 복습 6문항(4 → 6), 참고 자료 7개. 다음 학습: A·B 모두 12절, Ch 30 2절, Ch 33 1절
- 그림: Mermaid 5장(휠 만들고 설치, 두 Python 비교, 공유 목록 차례, 픽스처 준비 차례 sequenceDiagram, Before/After) + 삽화 1장(바구니 더미, 1회 생성 통과, 6절 바구니·공책·연필과 3~10절 좌우 Before/After 구도를 이어 씀). 11-1·11-3은 첫 렌더에서 `__init__.py`·`test_add_pencil`이 글자 중간에서 줄바꿈되어 `<br>` 위치를 고쳐 다시 렌더. 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 동작 근거: pytest 9.1.1 소스 `_pytest/fixtures.py`(`scope="function"` 기본값), `_pytest/setuponly.py`(SETUP/TEARDOWN 줄, 범위 첫 글자 대문자), `_pytest/monkeypatch.py`(「All modifications will be undone after the requesting test function or fixture has finished」), `_pytest/main.py` `_in_venv`(pyvenv.cfg). uv 문서 build backend(「src/<package_name>/__init__.py」, 이름 정규화, uv에 든 빌드 백엔드, 순수 Python만). Packaging 규격 Binary distribution format(ZIP 형식, METADATA·WHEEL·RECORD, py3-none-any)
- 실행 환경 주의: 실행 도구 커널에서 uv가 색 기호를 출력에 넣어(첫 실행) 빌드 명령에 `--color never`를 더함(8절 pytest `--color=no`와 같은 이유)

## 검토에서 볼 곳

- 새 내용 양: 패키지 폴더·pyproject.toml·빌드·휠·zipfile·uv venv/pip install/list·픽스처·`::`·`--setup-show`, 심화 monkeypatch. 코드 셀 19개로 챕터에서 가장 긴 노트북(9절 17개). 새 문법은 없고 명령·도구가 많음
- 11-2의 `ModuleNotFoundError`를 빨강으로 둠(실제로 불러오기에 실패한 출력). 값 바꿔 보기 결과라 노랑이 맞는지 검토 필요
- 「현재 작업 폴더에서 price_tools는 src 안에 있어 바로 보이지 않으므로 설치한 패키지를 불러온 것」은 커널 Python 대조(값 바꿔 보기)로 뒷받침. `sys.path` 자체는 출력하지 않음
- 삽화: 빈 바구니 더미가 「포갠」 모양보다 위로 쌓은 모양(맨 위 바구니 속이 비어 보여 채택). 공책 표지에 글자 없는 네모 라벨

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept-with-fixes(하 3). 모두 반영했습니다. 결정: 11-2 빨강 유지(프로그램을 멈춘 실패, 규격 §5-3)
- 11-1: 도식 읽기에 「빨간색은 이 Python이 불러오기에 실패해 종료 코드 1로 끝났다는 뜻입니다. 휠을 설치한 곳을 확인하려고 일부러 만든 결과입니다.」
- 11-2: 휠 이름 표시 「none은 Python 확장 규약(ABI)…, any는 운영체제와 컴퓨터 종류…」
- 11-3: 노트북 3번 `src/패키지 이름/__init__.py`, 「뒤에서 설정 파일에 적을 패키지 이름 price-tools의 하이픈을 밑줄로 바꾼 price_tools」
- 새 커널 출력은 반영 전과 같음. 코드 셀 19, 검사한 문장 428

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/11-패키징과-테스트-격리.md`
- 챕터 전체 `gates-after.json`과 루트 `textbook/qa/upgrade-progress.md` 갱신은 챕터를 마친 뒤
- Windows(`Scripts\python.exe` 경로)는 실행하지 않음
- 챕터 index(`_src/index.html`)의 A트랙 보충 과제 5는 개선 전 07·08절 데이터를 가리킴(이 절 범위 밖, handoff에 이미 남김)
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
