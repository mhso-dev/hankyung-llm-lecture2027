# 07 모듈과 타입힌트 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 07-5 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 저금통 투입구 옆에 동전 그림 스티커를 붙여 두면, 넣는 사람은 동전을 넣으면 된다는 것을 압니다. 그러나 스티커가 다른 물건을 막지는 않습니다. | 값 없음(비유). 동전 그림 스티커 = 타입힌트 `unit_price: int`, 동전 그림 종이 카드 = 문자열 '39000', 진짜 동전 = 정수 39000, 왼쪽 = Before, 오른쪽 = After. 3~6절 삽화의 좌우 Before/After 구도를 이어 씀 | — |
| 07-1 | 4 핵심 개념 · 모듈과 import 문 (노트북 「오늘 볼 그림」) | Mermaid flowchart TD | 줄 `import order_tools`는 파일 order_tools.py를 찾아 불러옵니다. 처음 불러올 때 파일의 줄이 위에서부터 실행되어, 모듈 안에 클래스 OrderLine이 만들어집니다. | 2번 셀 `쓴 글자 수: 179`·`['order_tools.py']`, 3번 셀 `pencil 수량: 5`·`<class 'order_tools.OrderLine'>` | 코드 셀·import 문·호출 flow(파랑), 파일과 모듈 tool(초록), 출력 measure(노랑) |
| 07-2 | 4 핵심 개념 · 모듈 이름과 __main__ | Mermaid flowchart TB(6절·7절 두 칸) | 자료형에서 점 앞은 클래스를 정의한 모듈의 이름입니다. | 4번 셀 `이 노트북의 이름: __main__`·`order_tools의 이름: order_tools`, 3번 셀 `<class 'order_tools.OrderLine'>`, 6절 노트북 4번 셀 `<class '__main__.OrderLine'>`(이번에 실행하지 않음) | 정의 셀 flow(파랑), 모듈 파일과 이름 tool(초록), 이 절 출력 measure(노랑), 6절 출력은 클래스 없음(회색) |
| 07-3 | 5 실행 예제 · import 문의 두 가지 모양 | Mermaid flowchart TB(3번·5번 두 칸) | 두 셀은 import 문의 모양만 다르고, 그래서 클래스를 부를 때 적는 이름이 다릅니다. | 3번 셀 `pencil 수량: 5`, 5번 셀 `note 수량: 4`·`<class 'order_tools.OrderLine'>` | import 문과 호출 flow(파랑), 노트북에 생긴 이름 tool(초록), 출력 measure(노랑) |
| 07-4 | 6 일부러 실패해 보기 | Mermaid flowchart TB(Before·After 두 칸) | Before 셀은 문자열 단가를 타입힌트가 int인 매개변수에 그대로 넣었고, 오류 없이 실행됐습니다. After 셀은 함수에 넣기 전에 `int()`로 단가를 정수로 바꿨습니다. | 9번 셀 `주문 줄 금액: 3900039000`·`<class 'str'>`·`False` / 11번 셀 `주문 줄 금액: 78000`·`<class 'int'>`·`True`(10번 심화 셀 타입힌트 기록은 본문 문장) | 함수에 넣는 단가 tool(초록), 함수 호출 flow(파랑), Before 결과 fail(빨강), After 결과 measure(노랑) |

셀 번호는 코드 셀 순번입니다(준비 1, 모듈 파일 쓰기 2, import 3, 모듈 이름 4, from import 5, 타입힌트 정의 6, 호출 7, 값 바꿔 보기 8, Before 9·심화 10, After 11).
색 규칙: 우리가 적은 코드(코드 셀·import 문·정의 셀·호출)는 파랑입니다. 파일·모듈·이름·단가처럼 저장된 값은 초록입니다(1~6절 「값은 초록」과 같음). 07-1의 파일 order_tools.py와 07-2의 모듈 파일은 같은 요소라 둘 다 초록입니다. 출력은 노랑이고, 빨강은 실제로 틀린 Before 결과뿐입니다. 이번 노트북에서 실행하지 않은 6절 출력은 회색입니다.
노트북 6~8번 셀(타입힌트 정의·호출·값 바꿔 보기)은 그림을 따로 만들지 않고 본문 「타입힌트」 문단으로 설명합니다.
기존 도식 `07-concept.svg`(Excalidraw)는 본문에서 뺐습니다. 원본은 `qa/upgrade/before/figures/`에 있고, `figures/`의 옛 파일은 지우지 않았습니다.
