"""Ch 02 08절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§6).

사용: python3 author_08.py  → labs/part1/ch02-python/notebooks/08-pytest.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 새 커널 실행 → 그림 첨부 → 빌드 → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 보존했다.
이 절은 모델을 부르지 않는다. 사다리 위치는 L4(§07) 뒤, L6(§09 데코레이터) 앞이다.
이 절에서 가르치는 것: 테스트·테스트 함수(test_ 이름 규칙), pytest 실행과 결과 읽기(점 . / F, N passed·N failed,
실패 설명의 > 줄과 E 줄, 종료 코드 0·1). G1이 잡는 문법을 새로 쓰지 않으므로 upgrade_allow 는 쓰지 않는다.
매개변수화(@pytest.mark.parametrize)는 L6 문법(@ 줄)이라 기본 경로에 두지 않고, After 뒤 「원리 더 알아보기」
심화 셀(lesson_level=deep-dive)에서 출력만 읽는다. 심화 셀은 기본 경로의 마지막 코드 셀(assert) 뒤에 있어
기본 경로가 심화 셀의 파일·변수를 쓰지 않는다.

subprocess 판단(07-diagnosis·handoff §07 → §08의 질문): 이 노트북은 같은 커널에서 price_tools.py를 두 번 고쳐 쓰고
테스트를 다시 실행한다. 커널 안에서 pytest.main()을 여러 번 부르면 import 캐시 때문에 고친 파일이 반영되지 않는다
(pytest 9.1.1 doc/en/how-to/usage.rst 「Calling pytest from Python code」, 7절 「모듈은 처음 불러올 때 한 번만 실행」).
그래서 부를 때마다 새 Python을 띄우는 subprocess.run([sys.executable, "-m", "pytest", "-q", "--color=no"])를 쓴다.
--color=no: 실행 도구 커널 환경에서 pytest가 ANSI 색 기호를 출력에 넣어(2026-09-16 첫 실행) 출력 글과 HTML이 깨지므로 끈다.
Ch 1 3절이 같은 모양(subprocess.run(목록, capture_output=True, text=True), sys.executable, returncode)을 가르쳤다.
기존 노트북의 os.environ.copy()·PYTEST_DISABLE_PLUGIN_AUTOLOAD·cwd=·Path·TemporaryDirectory·함수 인자 두 개는 뺐다
(실습 폴더 가상환경에 pytest11 플러그인이 0개임을 2026-09-16 확인, 작업 폴더는 5·7절처럼 os.chdir()로 옮김).
주의: 새 Python은 __pycache__의 기록 파일을 원본 파일의 수정 시각(초)과 크기로 확인한다. 실행 도구는 셀을 1초 안에
이어 실행할 수 있으므로, 같은 파일을 다시 쓸 때는 글자 수가 달라지게 둔다(price_tools.py 130 → 262 → 295,
test_price_tools.py 152 → 255). 기록 파일(__pycache__)은 학생에게 보여 주지 않는다.

이어짐: 7절 order_tools.py 쓰기(글을 with open "w"·write()로 저장)와 from import 문, 7절 타입힌트 함수
calculate_line_total(unit_price: int, quantity: int = 1) -> int(39000·2 → 78000), 4절 수량 생략 → 39000,
7절 Before/After(주문 줄 「무선 키보드,39000」, split(",")으로 나눈 단가 글자, int() 빠뜨림 → 넣음)와 같은 결함을
이번에는 테스트가 찾음, 7절 값 바꿔 보기 수량 3 → 117000(심화 셀), Ch 1 1절 assert·3절 subprocess/sys.executable/종료 코드.
기존 8절의 학습 질문(결함을 고친 뒤 같은 테스트가 통과하나요?)·실패 구조(기대값은 두고 구현 한 줄만 고침,
1 failed·종료 1 → passed·종료 0)·paired 형식을 유지한다. 데이터 discounted(10000) 9100/9000·1200+800은
앞 절 데이터로 바꿨다. 형식은 paired: example(1~6) → before(7) → after(8, 심화 셀 포함).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import code, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part1/ch02-python/notebooks"
BEFORE = {"lesson_part": "before"}
AFTER = {"lesson_part": "after"}


def section_08() -> tuple[str, str, list[dict]]:
    cells = [
        md("""# pytest

**이 노트북에서 할 일**

1. 7절 함수 `calculate_line_total()`을 모듈 파일에 저장하고, 기대값을 적은 테스트 파일을 만듭니다.
2. 새 Python에서 pytest를 실행해, 통과 표시와 요약 줄, 종료 코드를 읽습니다.
3. 7절과 같은 `int()` 빠뜨림 결함을 테스트로 찾고, 함수만 고쳐 같은 테스트를 통과시킵니다.

**준비물** — API 키 불필요. 모델 호출은 0번이고 비용은 들지 않습니다. 실행 시간은 1분 이내입니다.

테스트 도구 pytest 9.1.1은 실습 폴더에서 `uv sync --locked`를 실행할 때 함께 설치됩니다.
1~7절과 같은 실습 폴더 `labs/part1/ch02-python`의 `.venv`를 커널로 고르고, 첫 셀부터 순서대로 실행합니다.""", html="skip"),
        md("""## 오늘 볼 그림

![노트북 셀이 run_pytest()를 부르면 새 Python이 python -m pytest -q --color=no를 실행하고, 현재 작업 폴더에서 test_price_tools.py를 찾아 price_tools.py를 불러온 뒤 test_two_keyboards를 불러 assert line_total == 78000을 확인하고, 점 하나와 1 passed, 종료 코드 0이 출력되는 흐름도](attachment:08-1-테스트-실행-흐름.png)

위에서 아래로 읽습니다. 파란 상자는 우리가 적은 코드, 초록 상자는 파일, 노란 상자는 출력입니다.

노트북 셀은 테스트를 직접 부르지 않습니다. 새 Python에서 실행한 pytest가 test_로 시작하는 파일과 함수를 찾아 부르고, 결과만 노트북에 전합니다.""", html="skip"),
        md("""## 1. 준비

테스트 도구 pytest는 실습 폴더의 pyproject.toml에 9.1.1 버전으로 적혀 있습니다.
첫 준비 셀은 커널에서 pytest를 불러와 버전을 출력합니다.

오류 `ModuleNotFoundError`가 나오면, Ch 1 3절처럼 커널이 실습 폴더의 `.venv`인지 확인합니다."""),
        setup('''# 실습 폴더 가상환경에 설치된 pytest를 불러와 버전을 확인합니다
import pytest

# __version__은 패키지에 적어 둔 버전 글자입니다
print("pytest 버전:", pytest.__version__)'''),
        md("""**결과 읽기** — pytest 버전은 `9.1.1`로, pyproject.toml에 적은 버전과 같습니다."""),
        md("""이 노트북은 모듈 파일과 테스트 파일을 만듭니다. 5절·7절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.

첫 두 줄은 7절에서 배운 import 문으로, 표준 라이브러리 모듈 os와 tempfile을 불러옵니다."""),
        setup('''# 파일을 둘 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고 그 경로를 반환합니다
practice_folder = tempfile.mkdtemp(prefix="ch02-08-")
# chdir()는 터미널의 cd처럼 현재 작업 폴더를 옮깁니다
os.chdir(practice_folder)
file_names = os.listdir()
print("현재 작업 폴더의 파일:", file_names)'''),
        md("""**결과 읽기** — 현재 작업 폴더의 파일은 `[]`로, 빈 폴더에서 시작합니다.
폴더의 경로는 컴퓨터마다 달라서 출력하지 않았습니다."""),
        md("""## 2. 검사할 함수를 모듈 파일에 저장하기

테스트(test)는 함수가 기대한 값을 반환하는지 확인하는 코드입니다.
먼저 검사받을 함수를 파일에 둡니다. 7절 order_tools.py처럼 정의를 글로 적어 모듈 파일 price_tools.py에 저장합니다.

함수는 7절에서 타입힌트를 적은 `calculate_line_total()`입니다. 7절 노트북에서 단가 39000, 수량 2를 넣어 78000을 얻었습니다.

실행 전에 예상합니다. 현재 작업 폴더에 파일 price_tools.py 하나가 보일 것입니다."""),
        code('''# 7절 함수 calculate_line_total()의 정의를 글로 적어 모듈 파일 price_tools.py에 저장합니다
module_text = """def calculate_line_total(unit_price: int, quantity: int = 1) -> int:
    line_total = unit_price * quantity
    return line_total
"""
with open("price_tools.py", "w", encoding="utf-8") as file:
    written_count = file.write(module_text)
file_names = os.listdir()
print("쓴 글자 수:", written_count)
print("현재 작업 폴더의 파일:", file_names)'''),
        md("""**결과 읽기** — 쓴 글자 수는 `130`이고, 현재 작업 폴더의 파일은 `['price_tools.py']`로 예상과 같습니다.
7절 order_tools.py와 같은 방법으로 저장한 모듈 파일입니다."""),
        md("""## 3. 기대값을 적은 테스트 파일 만들기

테스트 함수(test function)는 검사할 함수를 부르고, 반환값이 기대값과 같은지 `assert`로 확인하는 함수입니다.
검사 줄 `assert`는 Ch 1 1절에서 처음 썼고, 1~7절 After 셀 끝에서도 썼습니다. 뒤의 비교가 참이면 지나가고, 거짓이면 그 줄에서 멈춥니다.

테스트 도구 pytest는 이름이 `test_`로 시작하는 파일을 찾습니다. 그 파일 안에서 이름이 `test_`로 시작하는 함수를 찾아 부릅니다.
그래서 파일 이름은 test_price_tools.py, 함수 이름은 test_two_keyboards로 짓습니다.

테스트 파일의 첫 줄은 7절에서 배운 from import 문입니다. 모듈 price_tools에서 함수 이름만 가져옵니다.
이 셀도 글을 저장만 하고, 테스트는 아직 실행하지 않습니다.

실행 전에 예상합니다. 현재 작업 폴더의 파일은 두 개가 될 것입니다."""),
        code('''# 단가 39000, 수량 2의 기대값 78000을 적은 테스트 파일을 저장합니다
test_text = """from price_tools import calculate_line_total


def test_two_keyboards():
    line_total = calculate_line_total(39000, 2)
    assert line_total == 78000
"""
with open("test_price_tools.py", "w", encoding="utf-8") as file:
    written_count = file.write(test_text)
# listdir()는 순서를 정하지 않고 반환하므로 sorted()로 이름 순서로 정렬합니다
file_names = sorted(os.listdir())
print("쓴 글자 수:", written_count)
print("현재 작업 폴더의 파일:", file_names)'''),
        md("""**결과 읽기** — 쓴 글자 수는 `152`이고, 현재 작업 폴더의 파일은 `['price_tools.py', 'test_price_tools.py']`로 예상과 같습니다.
테스트 파일도 모듈 파일처럼 글자로 된 .py 파일입니다."""),
        md("""## 4. 새 Python에서 pytest를 실행하는 함수 만들기

테스트 파일은 노트북 셀이 아니라 pytest가 불러와 실행합니다. 이 노트북은 뒤에서 price_tools.py를 고쳐 쓰고 테스트를 다시 실행합니다.

7절 주의할 점에 적은 것처럼, 모듈은 한 커널에서 처음 불러올 때 한 번만 실행됩니다.
그래서 커널 안에서 pytest를 여러 번 부르면 고친 파일이 반영되지 않을 수 있습니다. pytest 문서도 이 방법을 권하지 않습니다.
이 노트북은 pytest를 부를 때마다 새 Python을 하나 실행합니다. Ch 1 3절에서 `subprocess.run()`으로 Python을 따로 실행한 방법과 같습니다.

함수 `run_pytest()`가 실행하는 목록은 `[sys.executable, "-m", "pytest", "-q", "--color=no"]`입니다.
값 `sys.executable`은 지금 커널의 Python 파일 경로입니다. 옵션 `-m pytest`는 모듈 pytest를 실행하라는 뜻입니다.
옵션 `-q`는 출력을 짧게 줄이고, 옵션 `--color=no`는 출력 글에 색을 나타내는 기호를 넣지 않습니다.

테스트 파일이 있는 폴더의 터미널에서 `uv run python -m pytest -q --color=no`를 입력하는 것과 같은 일입니다.
노트북은 두 파일을 임시 폴더에 두었으므로, 실습 폴더에서 그대로 입력하면 찾을 테스트가 없습니다. 터미널에서는 이번에 실행하지 않았습니다.

파일 이름을 적지 않았으므로, pytest는 현재 작업 폴더에서 테스트 파일을 찾습니다.
함수는 pytest가 화면에 쓴 글(`stdout`)을 출력하고, 종료 코드(`returncode`)를 반환합니다.

실행 전에 예상합니다. 정의 셀이라 출력은 없을 것입니다."""),
        code('''# 현재 작업 폴더의 테스트를 새 Python에서 pytest로 실행하고, 종료 코드를 반환합니다
import subprocess
import sys


def run_pytest() -> int:
    # 터미널에서 python -m pytest -q --color=no를 입력하는 것과 같은 명령 목록입니다
    command = [sys.executable, "-m", "pytest", "-q", "--color=no"]
    # Ch 1 3절처럼 capture_output=True, text=True로 출력을 글로 받아 둡니다
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    return result.returncode'''),
        md("""**결과 읽기** — 예상대로 출력이 없습니다. 함수 `run_pytest()`는 부를 때마다 새 Python에서 pytest를 실행합니다."""),
        md("""## 5. 테스트 실행하고 결과 읽기

함수 `run_pytest()`를 불러 테스트를 실행합니다. 테스트 도구 pytest는 test_price_tools.py를 찾아 불러옵니다. 이어서 그 파일 안의 함수 test_two_keyboards를 부릅니다.
테스트 파일의 from import 줄은 같은 폴더의 price_tools.py를 불러옵니다.

실행 전에 예상합니다. 반환값 78000이 기대값 78000과 같으므로 테스트는 통과하고, 종료 코드는 0일 것입니다."""),
        code('''# 테스트 파일 하나, 테스트 함수 하나를 pytest로 실행합니다
exit_code = run_pytest()
print("종료 코드:", exit_code)'''),
        md("""**결과 읽기** — 첫 줄의 점 `.` 하나는 테스트 함수 하나가 통과했다는 표시입니다. 줄 끝 `[100%]`는 찾은 테스트를 모두 실행했다는 진행 표시입니다. 요약 줄은 `1 passed`이고, 종료 코드는 `0`입니다.

요약 줄 끝의 시간은 실행할 때마다 달라질 수 있습니다.
pytest 문서는 종료 코드 0을 「테스트를 모두 찾았고 모두 통과함」으로 설명합니다."""),
        md("""## 6. 값 바꿔 보기 — 테스트 함수 하나 더하기

테스트 파일에 테스트 함수를 하나 더합니다. 4절에서 수량을 적지 않고 부르면 기본값 1이 들어가 39000이 나왔습니다.
이 기대값을 새 테스트 함수 test_one_keyboard에 적습니다. 앞의 테스트 함수와 모듈 파일은 그대로 둡니다.

실행 전에 예상합니다. 통과 표시 점이 두 개가 되고, 요약 줄은 2 passed일 것입니다."""),
        code('''# 앞 테스트는 그대로 두고, 수량을 적지 않은 테스트 함수를 더해 테스트 파일을 다시 씁니다
two_tests_text = """from price_tools import calculate_line_total


def test_two_keyboards():
    line_total = calculate_line_total(39000, 2)
    assert line_total == 78000


def test_one_keyboard():
    line_total = calculate_line_total(39000)
    assert line_total == 39000
"""
with open("test_price_tools.py", "w", encoding="utf-8") as file:
    file.write(two_tests_text)
exit_code = run_pytest()
print("종료 코드:", exit_code)'''),
        md("""**결과 읽기** — 점이 `..` 두 개로 늘었고, 요약 줄은 `2 passed`, 종료 코드는 `0`으로 예상과 같습니다.

테스트 파일에 기대값 두 개가 남았습니다. 다음에 모듈 파일을 고친 뒤에도 같은 명령 한 번으로 두 기대값을 함께 확인합니다."""),
        md("""## 7. Before — 단가를 꺼내는 함수에서 int()를 빠뜨림

7절 Before에서는 주문 줄 「무선 키보드,39000」을 쉼표로 나눈 단가 글자를 그대로 함수에 넣었습니다.
이번에는 단가를 꺼내는 일을 함수 `read_unit_price()`로 만들어 모듈 파일에 더합니다. 그런데 7절 Before처럼 `int()`로 바꾸는 줄을 빠뜨렸습니다.

아래 셀은 두 함수를 담은 글로 price_tools.py를 다시 씁니다. 함수 calculate_line_total은 앞과 같습니다.
새 함수의 반환값 표시는 `-> int`이지만, 7절에서 본 것처럼 타입힌트는 값을 검사하지 않습니다.""", **BEFORE),
        code('''# 단가를 꺼내는 함수 read_unit_price()를 더해 모듈 파일을 다시 씁니다(int() 줄이 빠짐)
module_text = """def calculate_line_total(unit_price: int, quantity: int = 1) -> int:
    line_total = unit_price * quantity
    return line_total


def read_unit_price(price_line: str) -> int:
    product_name, unit_price_text = price_line.split(",")
    return unit_price_text
"""
with open("price_tools.py", "w", encoding="utf-8") as file:
    written_count = file.write(module_text)
print("쓴 글자 수:", written_count)''', **BEFORE),
        md("""**결과 읽기** — 쓴 글자 수는 `262`입니다. 함수 하나만 담았던 앞의 글보다 함수 read_unit_price만큼 늘었습니다.""", **BEFORE),
        md("""새 함수의 기대값을 적은 테스트 파일 test_unit_price.py를 따로 만듭니다.
주문 줄 「무선 키보드,39000」을 넣으면 정수 39000이 나와야 하므로, 기대값을 정수 39000으로 적습니다.
이 셀도 글을 저장만 합니다.""", **BEFORE),
        code('''# 주문 줄에서 꺼낸 단가의 기대값 39000(정수)을 적은 테스트 파일을 저장합니다
unit_test_text = """from price_tools import read_unit_price


def test_read_unit_price():
    unit_price = read_unit_price("무선 키보드,39000")
    assert unit_price == 39000
"""
with open("test_unit_price.py", "w", encoding="utf-8") as file:
    written_count = file.write(unit_test_text)
print("쓴 글자 수:", written_count)''', **BEFORE),
        md("""**결과 읽기** — 쓴 글자 수는 `150`입니다. 이제 테스트 파일은 두 개, 테스트 함수는 모두 세 개입니다.""", **BEFORE),
        md("""파일 이름을 적지 않았으므로, pytest는 테스트 파일 두 개를 모두 찾아 실행합니다.

실행 전에 예상해 봅니다. 7절에서 타입힌트는 문자열 단가를 막지 않았습니다. 이번에는 테스트가 이 결함을 알려 줄까요?""", **BEFORE),
        code('''# 테스트 파일 두 개, 테스트 함수 세 개를 pytest로 실행합니다
exit_code = run_pytest()
print("종료 코드:", exit_code)''', **BEFORE),
        md("""**결과 읽기** — 첫 줄은 `..F`이고, 요약 줄은 `1 failed, 2 passed`, 종료 코드는 `1`입니다.
점 두 개는 test_price_tools.py의 두 테스트가 통과했다는 표시입니다. 글자 F는 실패(failed)한 테스트 하나입니다.

실패 설명에서 `>` 표시가 붙은 줄이 멈춘 줄 `assert unit_price == 39000`입니다.
바로 아래 `E` 줄 `AssertionError: assert '39000' == 39000`에는 변수 이름 대신 실제값이 들어 있습니다.
왼쪽 '39000'은 함수가 반환한 문자열, 오른쪽 39000은 테스트에 적은 정수입니다.

그 아래 `test_unit_price.py:6`은 테스트 파일의 6번째 줄에서 멈췄다는 뜻입니다.
7절에서는 틀린 금액을 출력해 보고 결함을 찾았습니다. 이번에는 기대값을 적어 둔 테스트가 실패로 알렸습니다.""", **BEFORE),
        md("""## 8. After — int()로 바꾸는 줄 하나 더하기

Before 셀과 달라진 곳은 함수 `read_unit_price()` 안에 `int()` 줄 하나를 더한 것입니다. 테스트 파일 두 개와 기대값 39000은 그대로 둡니다.
테스트를 통과시키려고 기대값을 문자열 '39000'으로 바꾸면, 결함을 고친 것이 아니라 틀린 결과를 맞다고 적은 것입니다.

아래 셀은 고친 글로 price_tools.py를 다시 씁니다. 실행 전에 예상합니다. 줄 하나가 늘었으므로 쓴 글자 수는 Before보다 클 것입니다.""", **AFTER),
        code('''# read_unit_price()가 단가 글자를 int()로 바꿔 반환하도록 모듈 파일을 고쳐 씁니다
module_text = """def calculate_line_total(unit_price: int, quantity: int = 1) -> int:
    line_total = unit_price * quantity
    return line_total


def read_unit_price(price_line: str) -> int:
    product_name, unit_price_text = price_line.split(",")
    unit_price = int(unit_price_text)
    return unit_price
"""
with open("price_tools.py", "w", encoding="utf-8") as file:
    written_count = file.write(module_text)
print("쓴 글자 수:", written_count)''', **AFTER),
        md("""**결과 읽기** — 쓴 글자 수는 `295`로, Before의 262보다 큽니다. 모듈 파일만 고쳤고 테스트 파일은 쓰지 않았습니다.""", **AFTER),
        md("""Before 셀과 같은 함수 `run_pytest()`로 같은 테스트 파일 두 개를 다시 실행합니다.
함수는 부를 때마다 새 Python을 실행하므로, pytest는 고친 price_tools.py를 새로 불러옵니다.

실행 전에 예상합니다. 세 테스트가 모두 통과해 점 세 개와 3 passed, 종료 코드 0이 나올 것입니다.""", **AFTER),
        code('''# 테스트 파일은 그대로 두고, 고친 모듈 파일로 같은 테스트를 다시 실행합니다
exit_code = run_pytest()
print("종료 코드:", exit_code)
# 테스트가 하나라도 실패해 종료 코드가 0이 아니면 이 줄에서 멈춥니다
assert exit_code == 0''', **AFTER),
        md("""**결과 읽기** — 첫 줄은 `...`, 요약 줄은 `3 passed`, 종료 코드는 `0`입니다. 검사 줄 `assert`에서도 멈추지 않았습니다.

Before 셀의 ..F와 비교하면 F 자리가 점으로 바뀌었습니다. 달라진 곳은 모듈 파일의 `int()` 줄 하나이고, 테스트 파일과 기대값은 그대로입니다.

이번에 확인한 입력은 「무선 키보드,39000」 한 줄입니다. 쉼표가 없는 줄이나 「삼만구천」처럼 정수로 바꿀 수 없는 단가는 테스트하지 않았습니다.""", **AFTER),
        md("""### 원리 더 알아보기 — 매개변수화

입력만 다른 테스트를 함수 하나로 적는 pytest 기능을 매개변수화(parametrization)라고 합니다. 이 셀은 수량 1·2·3을 한 함수로 검사합니다.
테스트 함수 위에 `@pytest.mark.parametrize` 줄을 적습니다. 이 줄은 아래 테스트 함수를 입력 묶음마다 한 번씩 실행하도록 등록합니다.

기호 `@`로 시작하는 줄의 뜻은 9절 데코레이터에서 배우므로, 지금은 출력만 읽습니다.
이 셀은 테스트 파일을 하나 더 만들어, 앞의 세 테스트와 함께 실행합니다.""", **AFTER),
        code('''# 원리 더 알아보기: 수량 1·2·3의 입력 묶음 세 개를 테스트 함수 하나에 넣어 실행합니다
quantity_test_text = """import pytest
from price_tools import calculate_line_total


@pytest.mark.parametrize("quantity, expected", [(1, 39000), (2, 78000), (3, 117000)])
def test_quantities(quantity, expected):
    line_total = calculate_line_total(39000, quantity)
    assert line_total == expected
"""
with open("test_quantities.py", "w", encoding="utf-8") as file:
    file.write(quantity_test_text)
deep_exit_code = run_pytest()
print("종료 코드:", deep_exit_code)''', lesson_level="deep-dive", **AFTER),
        md("""**결과 읽기** — 점이 `......` 여섯 개이고, 요약 줄은 `6 passed`입니다.
앞의 세 테스트에, 테스트 함수 test_quantities가 입력 묶음 세 개로 세 번 실행되어 더해졌습니다.
수량 3의 기대값 117000은 7절 값 바꿔 보기에서 얻은 금액입니다.""", **AFTER),
        md("""## 정리

- 테스트 함수는 검사할 함수를 부르고 `assert`로 기대값과 비교합니다. 테스트 도구 pytest는 이름이 test_로 시작하는 파일과 함수를 찾아 부릅니다.
- 결과는 점(통과)과 F(실패), 요약 줄의 passed·failed 수, 종료 코드 0·1로 읽습니다.
- `int()` 줄을 빠뜨린 함수에서 테스트가 ..F로 실패했고, 기대값은 두고 함수만 고치자 3 passed가 되었습니다.

확장 경로(B)는 9절 데코레이터와 컨텍스트 매니저로, 기본 경로(A)는 12절 async와 await로 이어집니다.""", html="skip", **AFTER),
    ]
    return "08-pytest", "paired", cells


if __name__ == "__main__":
    slug, lesson_format, cells = section_08()
    write_notebook(LAB, "08", slug, lesson_format, cells)
