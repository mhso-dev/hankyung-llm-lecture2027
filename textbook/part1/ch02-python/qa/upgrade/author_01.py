"""Ch 02 01절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§6).

사용: python3 author_01.py  → labs/part1/ch02-python/notebooks/01-변수와-자료형.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 새 커널 실행 → 그림 첨부 → 빌드 → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 보존했다.
이 절은 모델을 부르지 않는다. 문법은 사다리 L1(대입·print)과 이 절에서 가르치는
자료형·type()·int()·변수만 넣은 f-string만 쓴다. 조건문·반복문은 2절에서 배우므로 쓰지 않는다.
2026-09-16 Ch01 chapter-summary 반영: Ch 1 1절의 price 3000 × count 2 = 6000(int) 셀을 4번 소제목에 추가,
이름 규칙(Ch 1이 Ch 2로 미룸)을 2번 소제목에, Ch 1 용어(함수·인자·import·f-string 읽기)를 이어받는 문장으로 교체.
형식은 paired: example(2~7) → before(8) → after(9).
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


def section_01() -> tuple[str, str, list[dict]]:
    cells = [
        md("""# 변수와 자료형

**이 노트북에서 할 일**

1. 상품 정보 네 가지를 변수에 저장하고, 값마다 자료형을 출력합니다.
2. 수량과 단가로 주문 금액과 결제 금액을 계산하고, 수량 하나만 바꿔 비교합니다.
3. 문자열 수량 `"2"`로 계산이 틀리는 장면을 보고, 정수로 바꿔 고칩니다.

**준비물** — API 키 불필요. 데이터 파일도 없습니다. 모델 호출은 0번이고 비용은 들지 않습니다.
실행 시간은 1분 이내입니다.

실습 폴더 `labs/part1/ch02-python`에서 Ch 1 3절처럼 `uv sync --locked`로 환경을 만듭니다.
커널에서 이 폴더의 `.venv`를 고른 뒤 첫 셀부터 순서대로 실행합니다.""", html="skip"),
        md("""## 오늘 볼 그림

![값 2가 대입을 거쳐 이름 quantity에 붙고, type(quantity)로 확인하면 int가 나오는 흐름도](attachment:01-1-대입-읽는-순서.png)

위에서 아래로 읽습니다. 초록 상자는 값, 파란 상자는 우리가 적는 대입과 이름, 노란 상자는 확인 결과입니다.
대입문 `quantity = 2`는 오른쪽 값부터 읽습니다. 값 2에 이름 quantity가 붙고, 자료형을 확인하면 int가 나옵니다.""", html="skip"),
        md("""## 1. 준비

이 절은 설치할 패키지가 없습니다. 첫 셀은 Ch 1 1절의 첫 셀과 같이 Python 버전을 확인합니다.
셀을 고른 뒤 `Shift+Enter`를 누르면 그 셀이 실행되고 다음 셀로 넘어갑니다.

코드의 `import` 줄은 Ch 1에서 본 대로 Python에 들어 있는 기능 묶음을 불러오는 줄입니다. 자세한 뜻은 7절 모듈과 타입힌트에서 배웁니다."""),
        code('''# 이 노트북을 실행하는 Python 버전을 확인합니다
import platform

# python_version()은 "3.12.13" 같은 버전 문자열을 반환합니다
python_version = platform.python_version()
is_python_312 = python_version.startswith("3.12")
print("Python 버전:", python_version)
print("3.12 버전인가:", is_python_312)''', lesson_role="setup", upgrade_allow=["stdlib-import"]),
        md("""**결과 읽기** — Python 버전이 3.12로 시작하고 `True`가 보이면 준비가 된 것입니다.
버전의 마지막 숫자는 컴퓨터마다 다를 수 있습니다."""),
        md("""## 2. 값에 이름 붙이기

Ch 1 1절에서 이름 `price`에 3000을 저장했습니다. 이렇게 값을 저장한 이름을 변수(variable)라고 합니다.
선반의 상자에 이름표를 달아 두면 이름만 보고 상자를 찾는 것과 같습니다.
등호 `=`로 오른쪽 값에 왼쪽 이름을 붙여 저장하는 일은 대입(assignment)이라고 합니다.

Ch 1이 Ch 2로 미룬 이름 규칙을 여기서 정리합니다. 숫자로 시작하는 `2price`는 이름으로 쓸 수 없습니다.
빈칸도 넣을 수 없어서 두 낱말은 `unit_price`처럼 밑줄로 잇습니다.
`for`, `True`처럼 Python이 문법에 쓰려고 정해 둔 낱말(예약어)도 이름으로 쓸 수 없습니다.
대문자와 소문자는 다른 글자라서 `quantity`와 `Quantity`는 서로 다른 이름입니다.

규칙에 어긋난 이름이 든 셀은 문법 오류로 실행되지 않습니다. 이 장면은 이번에 실행하지 않았습니다.
아래 셀은 규칙에 맞는 이름으로 상품 이름, 수량, 단가, 회원 여부를 변수 네 개에 저장합니다."""),
        code('''# 주문 한 건의 상품 정보를 변수 네 개에 저장합니다
product_name = "무선 키보드"
quantity = 2
unit_price = 39000.0
is_member = True
# 저장만 하면 화면에 아무것도 나오지 않으므로 print()로 출력합니다
print("상품 이름:", product_name)
print("수량:", quantity)
print("단가:", unit_price)
print("회원 여부:", is_member)'''),
        md("""**결과 읽기** — 저장한 순서대로 네 줄이 출력됐습니다. 상품 이름은 `무선 키보드`, 수량은 `2`입니다.
단가는 `39000.0`, 회원 여부는 `True`입니다.
출력에는 따옴표가 나오지 않습니다. 따옴표는 이 값이 글자라고 Python에 알려 주는 표시입니다."""),
        md("""## 3. 자료형 확인하기

자료형(type)은 값의 종류입니다. 종류에 따라 할 수 있는 계산이 달라집니다.

Ch 1에서 이름 뒤에 괄호를 붙여 부르는 기능을 함수라고 했습니다. 함수를 부르는 일은 함수 호출이라고 합니다.
내장 함수 `type()`은 괄호 안에 건넨 인자의 자료형을 반환합니다."""),
        code('''# type() 함수로 네 변수에 담긴 값의 자료형을 확인합니다
print("product_name:", type(product_name))
print("quantity:", type(quantity))
print("unit_price:", type(unit_price))
print("is_member:", type(is_member))'''),
        md("""**결과 읽기** — 네 줄의 자료형이 모두 다릅니다. 상품 이름은 문자열 `<class 'str'>`, 수량은 정수 `<class 'int'>`입니다.
단가는 실수 `<class 'float'>`, 회원 여부는 불리언 `<class 'bool'>`입니다.
수량 2에는 소수점이 없고, 단가 39000.0에는 소수점이 있습니다. 그래서 둘의 자료형이 다릅니다."""),
        md("""## 4. 주문 금액 계산하기

계산식에는 값 대신 변수 이름을 쓸 수 있습니다. 먼저 Ch 1 1절의 합계를 같은 이름으로 다시 계산합니다.
단가 3000과 수량 2는 둘 다 소수점이 없는 정수입니다. 정수끼리 곱한 합계의 자료형을 실행 전에 예상해 봅니다."""),
        code('''# Ch 1 1절의 단가와 수량을 정수로 적어 곱합니다
price = 3000
count = 2
total = price * count
print("Ch 1의 합계:", total)
print("합계의 자료형:", type(total))'''),
        md("""**결과 읽기** — Ch 1과 같은 합계 `6000`이 나왔고, 자료형은 `<class 'int'>`입니다.
정수끼리 곱했더니 정수가 나왔습니다. 그래서 출력에도 소수점이 없습니다.

이번 상품은 단가를 소수점이 있는 39000.0으로 적었습니다. 식 `quantity * unit_price`로 수량과 단가를 곱합니다.
결과는 새 변수 `order_total`에 저장합니다. 정수와 실수를 곱하면 어떤 자료형이 나올지 예상해 봅니다."""),
        code('''# 수량과 단가를 곱해 주문 금액을 계산합니다
order_total = quantity * unit_price
print("주문 금액:", order_total)
print("주문 금액의 자료형:", type(order_total))'''),
        md("""**결과 읽기** — 주문 금액은 `78000.0`이고, 자료형은 `<class 'float'>`입니다.
정수 2와 실수 39000.0을 곱했더니 실수가 나왔습니다. 앞 셀에서 정수끼리 곱한 6000과 달리 소수점이 붙었습니다."""),
        md("""## 5. 결제 금액 계산하기

회원 할인율 10%를 소수 0.1로 저장합니다. 할인액은 주문 금액에 할인율을 곱한 값입니다.
결제 금액은 주문 금액에서 할인액을 뺀 값입니다. 뺄셈 기호는 `-`입니다.
할인액을 변수에 따로 담으면 중간 값도 출력해 확인할 수 있습니다."""),
        code('''# 회원 할인율 10%를 소수로 저장합니다
discount_rate = 0.1
# 할인액을 따로 담아 두면 중간 값을 출력해 볼 수 있습니다
discount = order_total * discount_rate
payment = order_total - discount
print("할인율:", discount_rate)
print("할인액:", discount)
print("결제 금액:", payment)'''),
        md("""**결과 읽기** — 할인율 `0.1`, 할인액 `7800.0`, 결제 금액 `70200.0`이 출력됐습니다.
주문 금액 78000.0에서 할인액 7800.0을 빼면 70200.0입니다.
이번에는 회원 여부를 따지지 않고 할인을 계산했습니다. 회원일 때만 할인하려면 조건문이 필요합니다.
Ch 1에서 여러 줄 `if`를 써 보았고, 조건문은 2절에서 자세히 배웁니다."""),
        md("""## 6. 한 문장으로 출력하기

Ch 1 4절의 `hello.py` 마지막 줄 `f"총액: {total}원"`은 읽기만 했습니다. 이번에는 이 문법을 직접 씁니다.
따옴표 앞에 `f`를 붙인 문자열을 f-string이라고 합니다.

중괄호 안에 변수 이름을 적으면 그 자리에 변수 값이 들어갑니다. 서식의 빈칸에 이름을 채워 넣는 모습과 비슷합니다.
중괄호 안에는 변수 이름만 적습니다. 계산은 앞 셀에서 끝내고 결과를 변수에 담아 둡니다."""),
        code('''# 중괄호 자리에 변수 값을 넣어 주문 요약 문장을 만듭니다
summary = f"{product_name} {quantity}개, 결제 금액 {payment}원"
print(summary)
print("요약의 자료형:", type(summary))'''),
        md("""**결과 읽기** — 출력된 문장은 `무선 키보드 2개, 결제 금액 70200.0원`입니다. 중괄호 세 곳에 변수 값이 들어갔습니다.
요약의 자료형은 `<class 'str'>`입니다. 숫자를 넣어 만들어도 f-string의 결과는 문자열입니다."""),
        md("""## 7. 수량 하나만 바꿔 보기

Ch 1 1절에서는 수량을 바꿀 때 새 이름 `new_count`에 3을 담았습니다.
이번에는 같은 이름 `quantity`에 3을 다시 대입합니다. 이미 있는 변수에 다시 대입하면 그 이름의 값이 새 값으로 바뀝니다.
앞에서 계산한 `order_total`도 저절로 바뀔까요?

실행 전에 예상을 적습니다. 주문 금액은 78000.0 그대로일 것입니다. 곱셈은 그 줄을 실행한 순간에 한 번만 일어나기 때문입니다."""),
        code('''# 수량 변수에 새 값 3을 대입합니다
quantity = 3
print("바꾼 수량:", quantity)
# 주문 금액은 수량이 2일 때 계산해 둔 값입니다
print("주문 금액:", order_total)'''),
        md("""**결과 읽기** — 바꾼 수량은 `3`이지만, 주문 금액은 `78000.0` 그대로입니다.
변수 `order_total`에는 4번 소제목의 두 번째 셀을 실행한 순간의 결과가 들어 있습니다. 수량을 바꿔도 다시 계산되지 않습니다.

새 수량으로 금액을 얻으려면 곱셈을 다시 실행합니다. 결과는 수량 2일 때와 나란히 보려고 새 이름 `new_total`에 담습니다.
실행 전에 예상합니다. 39000.0원짜리 3개이므로 117000.0이 나올 것입니다."""),
        code('''# 바꾼 수량으로 주문 금액을 다시 계산합니다
new_total = quantity * unit_price
print("수량 2일 때 주문 금액:", order_total)
print("수량 3일 때 주문 금액:", new_total)'''),
        md("""**결과 읽기** — 수량 3일 때 주문 금액은 `117000.0`으로 예상과 같습니다. 수량 2일 때 금액 `78000.0`도 남아 있습니다.
두 금액의 차이 39000.0은 단가와 같습니다. 바꾼 값이 수량 하나뿐이라서 금액이 달라진 원인을 수량이라고 말할 수 있습니다."""),
        md("""## 8. Before — 문자열 수량으로 계산하기

파일에서 읽은 값은 숫자 모양이어도 문자열입니다. 5절에서 파일을 읽어 직접 확인합니다.

이번에는 수량을 문자열 `"2"`로 받았다고 가정합니다.
상자 3개에 이 수량만큼씩 담으면 기대하는 전체 수량은 6개입니다.
아래 셀은 문자열 `"2"`에 정수 3을 곱합니다. 결과가 6이 나올지 먼저 예상해 봅니다.""", **BEFORE),
        code('''# 입력으로 받았다고 가정한 수량은 따옴표가 붙은 문자열입니다
input_quantity = "2"
box_count = 3
expected_items = 6
# 문자열 수량에 상자 수를 곱하고, 기대한 수량과 비교합니다
total_items = input_quantity * box_count
is_expected = total_items == expected_items
print("입력 수량의 자료형:", type(input_quantity))
print("전체 수량:", total_items)
print("전체 수량의 자료형:", type(total_items))
print("기대한 수량과 같은가:", is_expected)''', **BEFORE),
        md("""**결과 읽기** — 전체 수량이 6이 아니라 `222`입니다. 기대한 수량과 비교한 결과는 `False`입니다.

입력 수량의 자료형이 `<class 'str'>`이기 때문입니다. 문자열에 정수를 곱하면 글자를 그 횟수만큼 이어 붙입니다.
오류 메시지는 나오지 않았습니다. 실행이 멈추지 않아도 계산 결과는 틀릴 수 있습니다.""", **BEFORE),
        md("""## 9. After — 정수로 바꾼 뒤 계산하기

내장 함수 `int()`는 숫자 모양의 문자열을 정수로 바꿉니다. 이렇게 자료형을 바꾸는 일을 형 변환이라고 합니다.
입력 `"2"`와 상자 수 3은 Before 셀과 같습니다. 곱하기 전에 `int()`를 거치는 줄만 더합니다.""", **AFTER),
        code('''# int() 함수로 문자열 "2"를 정수 2로 바꿉니다
converted_quantity = int(input_quantity)
print("바꾸기 전 자료형:", type(input_quantity))
print("바꾼 뒤 자료형:", type(converted_quantity))
print("바꾼 수량:", converted_quantity)''', **AFTER),
        md("""**결과 읽기** — 자료형이 `<class 'str'>`에서 `<class 'int'>`로 바뀌었습니다. 바꾼 수량은 `2`입니다.
출력 화면에는 따옴표가 나오지 않아 문자열과 정수가 똑같이 2로 보입니다. 그래서 자료형을 함께 출력해 구분합니다.

이제 정수로 바꾼 수량에 상자 수를 곱합니다. 이번에는 6이 나오고 비교 결과가 `True`일 것이라고 예상합니다.""", **AFTER),
        code('''# 정수로 바꾼 수량에 상자 수를 곱하고, 기대한 수량과 비교합니다
total_items = converted_quantity * box_count
is_expected = total_items == expected_items
print("전체 수량:", total_items)
print("기대한 수량과 같은가:", is_expected)
# 전체 수량이 기대와 다르면 이 줄에서 실행을 멈춥니다
assert total_items == expected_items''', **AFTER),
        md("""**결과 읽기** — 전체 수량은 `6`이고, 기대한 수량과 비교한 결과는 `True`입니다. Ch 1에서 쓴 검사 줄 `assert`에서도 멈추지 않았습니다.

Before 셀과 달라진 곳은 `int()`로 바꾸는 한 줄입니다. 곱하기 전에 자료형을 맞추자 전체 수량이 222에서 6으로 바뀌었습니다.
숫자 모양이 아닌 문자열(예: `"두 개"`)을 `int()`에 넣는 장면은 이번에 실행하지 않았습니다. 이런 입력을 다루는 방법은 5절 파일과 예외에서 배웁니다.""", **AFTER),
        md("""## 정리

- 변수는 값에 붙인 이름이고, 등호 `=`로 값을 대입합니다. 이름은 숫자로 시작할 수 없고 빈칸 대신 밑줄로 잇습니다.
- 값마다 자료형이 있고, 함수 `type()`으로 확인합니다. 정수끼리 곱한 6000은 int, 정수와 실수를 곱한 78000.0은 float였습니다.
- 다시 대입해도 앞에서 계산한 값은 바뀌지 않습니다. 새 값으로 계산하려면 계산 줄을 다시 실행합니다.
- 숫자 모양 문자열은 함수 `int()`로 정수로 바꾼 뒤 계산합니다.

다음 절에서는 조건문으로 주문 금액에 따라 서로 다른 줄을 실행합니다.""", html="skip", **AFTER),
    ]
    return "01-변수와-자료형", "paired", cells


if __name__ == "__main__":
    slug, lesson_format, cells = section_01()
    write_notebook(LAB, "01", slug, lesson_format, cells)
