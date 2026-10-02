"""Ch 02 03절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§6).

사용: python3 author_03.py  → labs/part1/ch02-python/notebooks/03-자료구조.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 새 커널 실행 → 그림 첨부 → 빌드 → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 보존했다.
이 절은 모델을 부르지 않는다. 기본 경로 문법은 사다리 L1(대입·print·여러 줄 if·for·목록·딕셔너리·튜플·집합·인덱싱·
슬라이싱·기본 메서드·변수만 넣은 f-string)과 1·2절에서 배운 elif·while·range()·enumerate(), 이 절에서 가르치는
슬라이싱·append()·복합 대입 +=·튜플 풀어 담기·딕셔너리 키 읽기/추가·in·get()·items()·set()·sorted()·is·copy()만 쓴다.
함수 정의·try/except는 기본 경로에 쓰지 않는다(4절·5절). 튜플을 바꾸는 TypeError는 「원리 더 알아보기」 심화 셀
(lesson_level="deep-dive")에만 둔다(2절 IndexError와 같은 방식). upgrade_allow 예외는 쓰지 않는다.
이어짐: 2절 주문 세 건 [18000, 42000, 65000]·합계 125000·배송비 기준 30000/50000·enumerate의 이름 두 개,
1절 무선 키보드 2개·단가 39000(이 절은 2절처럼 원 단위 정수)·주문 금액 78000·재대입·이름표 상자 비유,
Ch 1 2절 메서드, Ch 1 3절 [0]·[-1]·is not None, Ch 1 4절 in.
형식은 paired: example(1~12, 심화 셀 포함) → before(13) → after(14).
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


def section_03() -> tuple[str, str, list[dict]]:
    cells = [
        md("""# 자료구조

**이 노트북에서 할 일**

1. 주문 금액 목록을 위치 번호와 슬라이싱으로 읽고, `append()`로 새 주문을 추가합니다.
2. 튜플·딕셔너리·집합에 주문 정보를 목적에 맞게 담고 읽습니다.
3. 대입으로 만든 백업이 원본과 함께 바뀌는 장면을 보고, `copy()`로 고칩니다.

**준비물** — API 키 불필요. 데이터 파일도 없습니다. 모델 호출은 0번이고 비용은 들지 않습니다.
실행 시간은 1분 이내입니다.

**강의와 실습 범위** — 강의 시간에는 2~7번과 13~14번 소제목을 함께 실행합니다.
8~12번(딕셔너리 키 추가, `in`과 `get()`, `items()`, 집합과 값 바꿔 보기)은 실습 시간에 이어서 실행합니다.

1·2절과 같은 실습 폴더 `labs/part1/ch02-python`의 `.venv`를 커널로 고릅니다.
이전 커널의 변수는 쓰지 않으므로 첫 셀부터 순서대로 실행합니다.""", html="skip"),
        md("""## 오늘 볼 그림

![목록 order_amounts와 튜플 order_line은 위치 번호로 읽고, 딕셔너리 order는 키로, 집합 unique_items는 포함 여부로 읽는다는 것을 네 상자로 보여 주는 그림](attachment:03-1-네-자료구조.png)

위 칸은 위치 번호로 읽는 목록과 튜플, 아래 칸은 키로 찾는 딕셔너리와 포함 여부로 찾는 집합입니다.
상자마다 첫 줄은 자료구조 이름, 둘째 줄은 변수 이름, 셋째 줄은 이 노트북에서 담는 값입니다.
마지막 줄은 값을 읽는 방법입니다. 예를 들어 목록은 위치 0에서 18000을 읽습니다.""", html="skip"),
        md("""## 1. 준비

이 절도 설치할 패키지가 없습니다. 준비 셀은 2절에서 읽은 주문 세 건의 금액을 새 커널에 저장합니다.
금액은 2절처럼 원 단위 정수로 적습니다."""),
        setup('''# 2절에서 읽은 주문 세 건의 금액을 새 커널에 다시 저장합니다
order_amounts = [18000, 42000, 65000]
order_count = len(order_amounts)
print("주문 세 건의 금액:", order_amounts)
print("주문 수:", order_count)'''),
        md("""**결과 읽기** — 주문 세 건의 금액은 `[18000, 42000, 65000]`이고, 주문 수는 `3`입니다.
2절 After에서 읽은 세 건과 같습니다."""),
        md("""## 2. 목록에서 일부 읽기

자료구조(data structure)는 여러 값을 한 이름 아래 묶어 저장하는 방법입니다. 장 볼 물건을 종이 한 장에 줄줄이 적는 것과 같습니다.
이 절에서는 목록·튜플·딕셔너리·집합 네 가지를 씁니다. 그 가운데 목록(list)은 값을 순서대로 담는 자료구조입니다.

Ch 1 3절에서 본 대로 위치 번호 `[0]`은 첫 값, `[-1]`은 마지막 값을 읽습니다.
슬라이싱(slicing)은 위치 번호 두 개로 목록의 일부를 잘라 새 목록을 만드는 일입니다.
읽는 식 `order_amounts[0:2]`는 위치 0부터 위치 2 바로 앞까지 읽습니다. 2절의 `range(1, 3)`처럼 끝 번호는 들어가지 않습니다.

실행 전에 예상합니다. 앞의 두 주문은 18000과 42000일 것입니다."""),
        code('''# 위치 번호와 슬라이싱으로 목록의 일부를 읽습니다
first_amount = order_amounts[0]
last_amount = order_amounts[-1]
# [0:2]는 위치 0부터 위치 2 바로 앞까지 읽어 새 목록을 만듭니다
first_two = order_amounts[0:2]
print("첫 주문 금액:", first_amount)
print("마지막 주문 금액:", last_amount)
print("앞의 두 주문:", first_two)'''),
        md("""**결과 읽기** — 첫 주문 금액은 `18000`, 마지막 주문 금액은 `65000`입니다. 앞의 두 주문은 `[18000, 42000]`으로 예상과 같습니다.
잘라 낸 결과도 대괄호와 함께 출력됐습니다. 슬라이싱은 목록의 일부를 새 목록으로 만듭니다."""),
        md("""## 3. append()로 새 주문 추가하기

목록은 만든 뒤에도 값을 더하거나 바꿀 수 있습니다. 이런 성질을 변경 가능(mutable)하다고 합니다.
Ch 1 2절에서 값 뒤에 점을 찍고 부르는 기능을 메서드라고 했습니다. 메서드 `append()`는 괄호 안의 값 하나를 목록 끝에 추가합니다.
이 메서드는 새 목록을 만들지 않고, 이름 `order_amounts`가 붙은 목록 자체를 바꿉니다.

이 셀은 한 번만 실행합니다. 다시 실행하면 27000이 한 번 더 들어가므로, 그럴 때는 첫 셀부터 다시 실행합니다.

실행 전에 예상합니다. 주문 수는 3에서 4로 늘 것입니다."""),
        code('''# 새로 들어온 주문 27000원을 목록 끝에 추가합니다
new_amount = 27000
order_amounts.append(new_amount)
order_count = len(order_amounts)
print("추가한 뒤 목록:", order_amounts)
print("추가한 뒤 주문 수:", order_count)'''),
        md("""**결과 읽기** — 추가한 뒤 목록은 `[18000, 42000, 65000, 27000]`이고, 주문 수는 `4`입니다.
새 값 27000은 목록 맨 끝에 들어갔습니다. 앞의 세 값과 그 순서는 그대로입니다."""),
        md("""## 4. 빈 목록에 조건에 맞는 값 모으기

2절의 배송비 규칙에서 30000원 미만 주문은 배송비가 3000원이었습니다. 이런 주문만 골라 새 목록에 모읍니다.
먼저 빈 목록 `[]`을 만들고, 반복문 `for`로 금액을 하나씩 읽습니다. 조건이 참일 때만 `append()`로 추가합니다.
여러 값 가운데 일부를 고를 때 앞으로 계속 쓰는 모양입니다.

실행 전에 예상합니다. 네 금액 가운데 18000과 27000이 모일 것입니다."""),
        code('''# 배송비가 3000원인 30000원 미만 주문만 새 목록에 모읍니다
reduced_fee_minimum = 30000
small_orders = []
for amount in order_amounts:
    # 조건이 참인 차례에만 목록 끝에 금액을 추가합니다
    if amount < reduced_fee_minimum:
        small_orders.append(amount)
small_count = len(small_orders)
print("30000원 미만 주문:", small_orders)
print("30000원 미만 주문 수:", small_count)'''),
        md("""**결과 읽기** — 30000원 미만 주문은 `[18000, 27000]`, 개수는 `2`로 예상과 같습니다.
금액 42000과 65000을 읽은 차례에는 조건이 거짓이라 `append()` 줄을 건너뛰었습니다. 모인 순서는 원래 목록의 순서와 같습니다."""),
        md("""## 5. 복합 대입 +=로 합계 늘리기

2절에서는 합계를 `checked_total = checked_total + amount`처럼 늘렸습니다. 같은 이름을 두 번 적어야 합니다.
복합 대입 `+=`는 이 줄을 줄여 씁니다. 줄 `order_sum += amount`는 `order_sum = order_sum + amount`와 같은 뜻입니다.

실행 전에 예상합니다. 2절의 합계 125000에 새 주문 27000을 더한 152000일 것입니다."""),
        code('''# 주문 네 건의 금액을 모두 더합니다
order_sum = 0
for amount in order_amounts:
    # order_sum = order_sum + amount와 같은 뜻입니다
    order_sum += amount
print("주문 수:", order_count)
print("주문 네 건의 합계:", order_sum)'''),
        md("""**결과 읽기** — 주문 수 `4`, 주문 네 건의 합계는 `152000`으로 예상과 같습니다.
2절 After에서 센 세 건의 합계 125000보다 새 주문 27000원만큼 많습니다."""),
        md("""## 6. 튜플로 순서가 정해진 값 묶기

튜플(tuple)은 순서가 있고, 만든 뒤에는 바꿀 수 없는 묶음입니다. 영수증에 이미 찍힌 한 줄처럼 자리와 개수가 고정됩니다.
대괄호 대신 소괄호 `( )`로 만들고, 읽을 때는 목록처럼 위치 번호를 씁니다.

1절의 주문 한 줄을 상품 이름, 수량, 단가 순서로 튜플에 담습니다. 단가는 2절처럼 원 단위 정수 39000으로 적습니다.
이름 세 개를 쉼표로 적고 튜플을 대입하면 값이 차례로 담깁니다. 이 모양을 풀어 담기(unpacking)라고 합니다.
2절의 `for index, amount in enumerate(order_amounts):`도 이름 두 개에 값을 풀어 담았습니다.

실행 전에 예상합니다. 수량 2에 단가 39000을 곱한 주문 금액은 78000일 것입니다."""),
        code('''# 상품 이름·수량·단가를 순서가 정해진 튜플 하나에 담습니다
order_line = ("무선 키보드", 2, 39000)
second_value = order_line[1]
print("주문 줄:", order_line)
print("둘째 값(수량):", second_value)
# 이름 세 개를 쉼표로 적으면 튜플의 값이 순서대로 담깁니다
product_name, quantity, unit_price = order_line
line_total = quantity * unit_price
print("상품 이름:", product_name)
print("주문 금액:", line_total)'''),
        md("""**결과 읽기** — 주문 줄은 `('무선 키보드', 2, 39000)`으로 소괄호와 함께 출력됐습니다. 둘째 값은 수량 `2`입니다.
풀어 담은 뒤 상품 이름은 `무선 키보드`, 주문 금액은 `78000`입니다.
1절에서는 실수 단가로 78000.0을 얻었고, 이번에는 같은 금액을 정수로 계산했습니다."""),
        md("""### 원리 더 알아보기 — 튜플의 값을 바꾸면 나오는 오류

튜플의 수량 자리에 3을 넣으면 어떻게 될까요? 튜플은 바꿀 수 없으므로 오류가 나고 셀 실행이 멈춥니다.
아래 셀은 멈추지 않고 오류 이름만 보려고 `try`와 `except`를 씁니다. 2절의 원리 더 알아보기와 같은 방법입니다.
이 문법은 5절 파일과 예외에서 배우므로 지금은 출력만 읽습니다."""),
        code('''# 원리 더 알아보기: 튜플의 수량 자리에 3을 넣어 봅니다
try:
    order_line[1] = 3
except TypeError as error:
    print("오류 이름:", type(error).__name__)
    print("오류 메시지:", error)
print("튜플 값:", order_line)''', lesson_level="deep-dive"),
        md("""**결과 읽기** — 오류 이름은 `TypeError`, 메시지는 `'tuple' object does not support item assignment`입니다.
튜플은 위치 번호로 값을 바꾸는 대입을 받지 않는다는 뜻입니다. 마지막 줄의 튜플 값은 `('무선 키보드', 2, 39000)` 그대로입니다."""),
        md("""## 7. 딕셔너리로 이름을 붙여 저장하기

딕셔너리(dictionary)는 키(key)와 값을 짝지어 저장하는 자료구조입니다. 서랍마다 붙은 이름표를 보고 물건을 꺼내는 것과 같습니다.
중괄호 `{ }` 안에 `키: 값`을 쉼표로 나눠 적습니다. 콜론 왼쪽이 키, 오른쪽이 값입니다.

튜플은 둘째 값이 수량이라는 것을 순서로만 압니다. 딕셔너리는 `"amount"` 같은 키 이름으로 값을 찾으므로 뜻이 드러납니다.
1절의 주문 한 건에 주문 번호를 붙여 딕셔너리에 담습니다.

실행 전에 예상합니다. 키 `"amount"`로 읽은 값은 78000일 것입니다."""),
        code('''# 주문 한 건의 번호·상품 이름·금액을 키와 값의 짝으로 저장합니다
order = {"order_id": "A102", "product_name": "무선 키보드", "amount": 78000}
print("주문:", order)
# 대괄호 안에 키를 적으면 그 키와 짝인 값을 읽습니다
order_id = order["order_id"]
order_amount = order["amount"]
print("주문 번호:", order_id)
print("주문 금액:", order_amount)'''),
        md("""**결과 읽기** — 주문 번호는 `A102`, 주문 금액은 `78000`으로 예상과 같습니다.
딕셔너리 전체를 출력하면 `'amount': 78000`처럼 키와 값이 콜론으로 이어져 보입니다."""),
        md("""## 8. 딕셔너리에 키 추가하기

없는 키에 값을 대입하면 딕셔너리에 새 짝이 추가됩니다. 목록처럼 딕셔너리도 만든 뒤에 바꿀 수 있습니다.
2절 규칙대로 78000원은 50000원 이상이라 배송비가 0원입니다. 키 `"shipping_fee"`에 0을 대입해 주문 정보에 더합니다.
함수 `len()`에 딕셔너리를 넣으면 키와 값의 짝이 몇 개인지 반환합니다.

실행 전에 예상합니다. 짝의 수는 3에서 4로 늘 것입니다."""),
        code('''# 없는 키 "shipping_fee"에 대입해 배송비 짝을 추가합니다
order["shipping_fee"] = 0
field_count = len(order)
print("배송비를 추가한 주문:", order)
print("키와 값의 짝 수:", field_count)'''),
        md("""**결과 읽기** — 출력 끝에 `'shipping_fee': 0`이 붙었고, 짝의 수는 `4`로 예상과 같습니다.
새 짝은 맨 뒤에 들어갔습니다. 앞의 세 짝은 그대로입니다."""),
        md("""## 9. 없을 수도 있는 키 확인하기

대괄호로 없는 키를 읽으면 `KeyError` 오류가 나고 셀이 멈춥니다. 이 장면은 이번에 실행하지 않았습니다.
키가 없을 수도 있으면 연산자 `in`으로 먼저 확인합니다. Ch 1 4절에서 쓴 연산자이고, 딕셔너리에서는 그 키가 있는지 검사합니다.
메서드 `get()`은 키가 있으면 그 값을, 없으면 괄호 둘째 자리에 적은 기본값을 반환합니다.

실행 전에 예상합니다. 이 주문에는 쿠폰 키가 없으므로 `False`와 기본값 `"없음"`이 나올 것입니다.
기본값을 적지 않으면 `get()`은 `None`을 반환합니다. 이 장면은 이번에 실행하지 않았습니다."""),
        code('''# 쿠폰 키가 있는지 in으로 확인하고, get()으로 기본값과 함께 읽습니다
has_coupon = "coupon_code" in order
coupon_code = order.get("coupon_code", "없음")
# 있는 키를 get()으로 읽으면 기본값 대신 저장된 값이 나옵니다
shipping_fee = order.get("shipping_fee", "없음")
print("쿠폰 키가 있는가:", has_coupon)
print("쿠폰 코드:", coupon_code)
print("배송비:", shipping_fee)'''),
        md("""**결과 읽기** — 쿠폰 키가 있는가는 `False`, 쿠폰 코드는 기본값 `없음`입니다. 있는 키인 배송비는 저장된 값 `0`이 나왔습니다.
기본값을 주었기 때문에 키가 없어도 셀이 멈추지 않았습니다."""),
        md("""## 10. 키와 값을 함께 읽기

반복문 `for`로 딕셔너리의 짝을 모두 읽을 때는 메서드 `items()`를 씁니다. 이 메서드는 키와 값의 짝을 차례로 내놓습니다.
반복문 머리에 이름 두 개를 쉼표로 적으면 키와 값이 풀어 담깁니다. 2절의 `enumerate()`와 같은 모양입니다.
읽은 짝의 수는 5번 소제목의 `+=`로 셉니다.

실행 전에 예상합니다. 짝 네 개를 읽고, 앞 셀에서 추가한 배송비가 마지막 줄에 나올 것입니다."""),
        code('''# items()가 내놓는 키와 값의 짝을 하나씩 읽어 출력합니다
read_count = 0
for key, value in order.items():
    print(f"{key}: {value}")
    read_count += 1
print("읽은 짝의 수:", read_count)'''),
        md("""**결과 읽기** — 첫 줄은 `order_id: A102`, 마지막 줄은 `shipping_fee: 0`입니다. 읽은 짝의 수는 `4`로 예상과 같습니다.
딕셔너리는 넣은 순서대로 짝을 내놓았습니다. 그래서 나중에 추가한 배송비가 마지막에 나왔습니다."""),
        md("""## 11. 집합으로 중복 없애기

집합(set)은 같은 값을 한 번만 담는 자료구조입니다. 출석부에 같은 이름을 두 번 적어도 한 사람으로 세는 것과 같습니다.
내장 함수 `set()`에 목록을 넣으면 중복을 뺀 새 집합을 반환합니다.
집합에는 위치 번호가 없고, 값의 순서도 정해 두지 않습니다. 그래서 화면에 보일 때는 내장 함수 `sorted()`로 정렬한 새 목록을 만듭니다.

장바구니 기록에 담긴 상품 이름은 키보드, 마우스, 키보드입니다.

실행 전에 예상합니다. 목록 길이는 3, 상품 종류 수는 2일 것입니다."""),
        code('''# 장바구니 기록의 상품 이름에서 중복을 뺀 집합을 만듭니다
product_names = ["키보드", "마우스", "키보드"]
unique_items = set(product_names)
# sorted()는 값을 정렬한 새 목록을 반환합니다(집합에 순서가 생기지는 않습니다)
sorted_items = sorted(unique_items)
has_mouse = "마우스" in unique_items
print("원래 목록:", product_names)
print("상품 목록 길이:", len(product_names))
print("상품 종류 수:", len(unique_items))
print("상품 종류(정렬):", sorted_items)
print("마우스가 있는가:", has_mouse)'''),
        md("""**결과 읽기** — 상품 목록 길이는 `3`, 상품 종류 수는 `2`로 예상과 같습니다. 정렬한 상품 종류는 `['마우스', '키보드']`입니다.
마우스가 있는가는 `True`입니다. 원래 목록은 키보드가 두 번 든 그대로라서, 집합은 새로 만들어졌습니다.

목록 길이 3은 담긴 상품 수이고, 종류 수 2는 서로 다른 상품 수입니다. 두 숫자는 서로 다른 질문에 답합니다."""),
        md("""## 12. 값 바꿔 보기 — 새 상품 하나 추가하기

변수 `new_item` 하나만 바꿔 목록 길이와 상품 종류 수를 비교합니다. 목록은 매번 처음 세 상품으로 다시 만듭니다.
먼저 목록에 없던 헤드셋을 추가합니다.

실행 전에 예상합니다. 목록 길이는 4, 종류 수는 3일 것입니다."""),
        code('''# 목록에 없던 상품 하나를 추가하고 목록 길이와 종류 수를 봅니다
new_item = "헤드셋"
product_names = ["키보드", "마우스", "키보드"]
product_names.append(new_item)
unique_items = set(product_names)
sorted_items = sorted(unique_items)
print("추가한 상품:", new_item)
print("상품 목록 길이:", len(product_names))
print("상품 종류 수:", len(unique_items))
print("상품 종류(정렬):", sorted_items)'''),
        md("""**결과 읽기** — 목록 길이 `4`, 상품 종류 수 `3`으로 예상과 같습니다. 정렬한 상품 종류는 `['마우스', '키보드', '헤드셋']`입니다."""),
        md("""이번에는 변수 `new_item`만 이미 목록에 있는 키보드로 바꿉니다. 다시 만드는 목록과 세는 방법은 그대로 둡니다.

실행 전에 예상합니다. 목록 길이는 똑같이 4이지만, 종류 수는 2에 머물 것입니다."""),
        code('''# 추가할 상품만 이미 있는 키보드로 바꾸고 같은 방법으로 봅니다
new_item = "키보드"
product_names = ["키보드", "마우스", "키보드"]
product_names.append(new_item)
unique_items = set(product_names)
sorted_items = sorted(unique_items)
print("추가한 상품:", new_item)
print("상품 목록 길이:", len(product_names))
print("상품 종류 수:", len(unique_items))
print("상품 종류(정렬):", sorted_items)'''),
        md("""**결과 읽기** — 목록 길이는 `4`, 상품 종류 수는 `2`로 예상과 같습니다. 정렬한 상품 종류는 `['마우스', '키보드']` 그대로입니다.
목록에는 키보드가 세 번 들어갔지만 집합에는 한 번만 남았습니다.
바꾼 값은 추가한 상품 하나뿐입니다. 그래서 종류 수 3과 2의 차이는 새 상품이 이미 있던 상품인지에서 나왔습니다."""),
        md("""## 13. Before — 대입으로 백업 만들기

장바구니 `cart`에 키보드와 마우스를 담았습니다. 상품을 더 담기 전에 지금 상태를 백업해 두려고 합니다.
백업(backup)은 나중에 비교하거나 되돌리려고 따로 남겨 두는 사본입니다.
1절에서 대입은 오른쪽 값에 왼쪽 이름을 붙이는 일이라고 배웠습니다. 그래서 `backup = cart`로 이름을 하나 더 붙여 백업으로 삼습니다.

연산자 `is`는 두 이름이 같은 목록 하나에 붙어 있는지 검사합니다. Ch 1 3절의 `is not None`에서 본 연산자입니다.
백업을 만든 뒤 `cart`에만 헤드셋을 추가합니다. 실행 전에 예상해 봅니다. 백업은 두 상품 그대로일까요?""", **BEFORE),
        code('''# 장바구니에 이름 backup을 하나 더 붙인 뒤, cart 쪽에만 헤드셋을 추가합니다
cart = ["키보드", "마우스"]
backup = cart
cart.append("헤드셋")
# is는 두 이름이 같은 목록 하나에 붙어 있는지 검사합니다
is_same_list = cart is backup
is_backup_kept = backup == ["키보드", "마우스"]
print("cart:", cart)
print("backup:", backup)
print("같은 목록인가:", is_same_list)
print("백업이 추가 전 그대로인가:", is_backup_kept)''', **BEFORE),
        md("""**결과 읽기** — 두 줄 모두 `['키보드', '마우스', '헤드셋']`입니다. 같은 목록인가는 `True`, 백업이 추가 전 그대로인가는 `False`입니다.

오류는 나지 않았지만 백업에도 헤드셋이 들어갔습니다. 대입 `backup = cart`는 새 목록을 만들지 않았습니다.
목록 하나에 이름 두 개가 붙었을 뿐입니다. 그래서 이름 `cart`로 추가한 헤드셋이 이름 `backup`으로 읽어도 보입니다.

1절에서 수량에 3을 다시 대입했을 때는 주문 금액이 그대로였습니다. 다시 대입은 이름을 옮겨 붙이지만, `append()`는 목록 자체를 바꿉니다.""", **BEFORE),
        md("""## 14. After — copy()로 새 목록 만들기

메서드 `copy()`는 목록에 든 값을 그대로 담은 새 목록을 만들어 반환합니다. 같은 물건을 새 상자에 한 벌 더 담는 것과 같습니다.
Before 셀과 달라진 곳은 `backup = cart.copy()` 한 줄입니다. 복사 직후에는 연산자 `==`로 내용이 같은지도 확인합니다.

실행 전에 예상합니다. 복사 직후 내용은 같지만, 같은 목록인가는 `False`일 것입니다.""", **AFTER),
        code('''# copy()로 내용이 같은 새 목록을 만든 뒤, cart 쪽에만 헤드셋을 추가합니다
cart = ["키보드", "마우스"]
backup = cart.copy()
# 복사 직후에는 두 목록의 내용이 같습니다
is_same_content = backup == cart
cart.append("헤드셋")
is_same_list = cart is backup
is_backup_kept = backup == ["키보드", "마우스"]
print("복사 직후 내용이 같은가:", is_same_content)
print("cart:", cart)
print("backup:", backup)
print("같은 목록인가:", is_same_list)
print("백업이 추가 전 그대로인가:", is_backup_kept)
# 백업이 추가 전 두 상품 그대로가 아니면 이 줄에서 멈춥니다
assert is_backup_kept''', **AFTER),
        md("""**결과 읽기** — 복사 직후 내용이 같은가는 `True`입니다. 헤드셋을 추가한 뒤 `cart: ['키보드', '마우스', '헤드셋']`, `backup: ['키보드', '마우스']`입니다.
같은 목록인가는 `False`, 백업이 추가 전 그대로인가는 `True`입니다. 검사 줄 `assert`에서도 멈추지 않았습니다.

Before 셀의 `True`·`False`가 After 셀에서 `False`·`True`로 바뀌었습니다. 연산자 `==`는 내용이 같은지, `is`는 같은 목록 하나인지 검사합니다.
이번 목록에는 글자 값만 들어 있습니다. 목록 안에 목록이 든 경우의 복사는 이번에 실행하지 않았습니다.""", **AFTER),
        md("""## 정리

- 목록은 값을 순서대로 담고 바꿀 수 있습니다. 슬라이싱 `[0:2]`로 일부를 읽고, `append()`로 끝에 추가했습니다.
- 빈 목록과 `for`·`append()`로 30000원 미만 주문 `[18000, 27000]`을 모았고, `+=`로 합계 152000을 셌습니다.
- 튜플은 바꿀 수 없는 순서 묶음, 딕셔너리는 키로 찾는 묶음, 집합은 중복 없는 묶음입니다.
- 대입 `backup = cart`는 목록 하나에 이름을 하나 더 붙입니다. 따로 남기려면 `copy()`로 새 목록을 만듭니다.

다음 절에서는 계산 순서에 이름을 붙여 다시 쓰는 함수를 배웁니다.""", html="skip", **AFTER),
    ]
    return "03-자료구조", "paired", cells


if __name__ == "__main__":
    slug, lesson_format, cells = section_03()
    write_notebook(LAB, "03", slug, lesson_format, cells)
