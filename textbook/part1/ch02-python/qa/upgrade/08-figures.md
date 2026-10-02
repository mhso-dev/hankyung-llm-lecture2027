# 08 pytest — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 08-5 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 테스트는 함수가 반환한 실제값과 미리 적어 둔 기대값을 저울 양쪽에 올려 보는 일입니다. 같으면 저울이 수평이고, 다르면 기웁니다. | 값 없음(비유). 기준 동전 = 기대값 39000, 동전 그림 종이 카드 = 실제값 '39000'(7절 삽화의 카드를 다시 씀), 진짜 동전 = int()로 바꾼 39000, 기운 저울 = Before 실패, 수평 = After 통과. 3~7절 좌우 Before/After 구도 | — |
| 08-1 | 4 핵심 개념 · pytest가 테스트를 찾아 실행하는 차례 (노트북 「오늘 볼 그림」) | Mermaid flowchart TD | 노트북 셀이 함수 run_pytest()를 부르면, 새 Python이 pytest를 실행합니다. pytest는 이름이 test_로 시작하는 파일과 함수를 찾아 부릅니다. | 4번 셀 `['price_tools.py', 'test_price_tools.py']`, 5번 셀 명령 목록, 6번 셀 `1 passed`·`종료 코드: 0` | 노트북 셀·명령·테스트 함수 flow(파랑), 테스트 파일·모듈 파일 tool(초록), 출력 measure(노랑) |
| 08-2 | 5 실행 예제 · 새 Python에서 두 번 실행한 차례 | Mermaid sequenceDiagram | 함수 run_pytest()는 부를 때마다 새 Python을 실행하므로, pytest는 다시 쓴 테스트 파일을 새로 불러옵니다. | 4번 셀 `쓴 글자 수: 152`, 6번 셀 `1 passed`·`종료 코드: 0`, 7번 셀 `..`·`2 passed`·`종료 코드: 0` | 메모 노랑(결과를 전한 뒤 시점), 참여자 기본색 |
| 08-3 | 6 일부러 실패해 보기 · 실패 설명 읽기 | Mermaid flowchart TD | 실패 설명에서 > 표시가 붙은 줄이 멈춘 줄이고, 바로 아래 E 줄에는 변수 이름 대신 실제값이 들어 있습니다. | 10번 셀 `..F`, `test_read_unit_price`, `>       assert unit_price == 39000`, `E       AssertionError: assert '39000' == 39000`, `test_unit_price.py:6`, `1 failed, 2 passed`, `종료 코드: 1` | 테스트 함수·assert 줄 flow(파랑), 멈춘 파일 tool(초록), 진행 줄 ..F·E 줄·요약 줄 fail(빨강) |
| 08-4 | 6 일부러 실패해 보기 · Before/After | Mermaid flowchart TB(Before·After 두 칸) | Before와 달라진 곳은 모듈 파일의 int() 줄 하나이고, 테스트 파일과 기대값은 그대로입니다. | 8번 셀 `쓴 글자 수: 262`, 10번 셀 `..F`·`1 failed, 2 passed`·`종료 코드: 1` / 11번 셀 `쓴 글자 수: 295`, 12번 셀 `...`·`3 passed`·`종료 코드: 0` | 모듈 파일 tool(초록), run_pytest() flow(파랑), Before 결과 fail(빨강), After 결과 measure(노랑) |

셀 번호는 코드 셀 순번입니다(준비 1·2, 모듈 파일 3, 테스트 파일 4, run_pytest 정의 5, 실행 6, 값 바꿔 보기 7, Before 모듈 8·테스트 파일 9·실행 10, After 모듈 11·실행 12, 심화 13).
색 규칙: 우리가 적은 코드(노트북 셀, 명령, 테스트 함수, assert 줄, run_pytest())는 파랑입니다. 파일(테스트 파일, 모듈 파일, 멈춘 파일 위치)은 초록입니다(1~7절 「값·파일은 초록」과 같음). 통과 출력은 노랑이고, 빨강은 실제로 실패를 알린 Before 출력(진행 줄 ..F, E 줄, 요약 줄)뿐입니다. 08-3과 08-4의 ..F는 같은 출력이라 둘 다 빨강입니다.
노트북 13번 심화 셀(매개변수화, 6 passed)은 그림을 만들지 않고 본문 「확인한 범위」 문단으로만 설명합니다.
기존 도식 `08-concept.svg`(Excalidraw)는 본문에서 뺐습니다. 원본은 `qa/upgrade/before/figures/`에 있고, `figures/`의 옛 파일은 지우지 않았습니다.
