# 09 데코레이터와 컨텍스트 매니저 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 09-5 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 파일을 여는 일은 문을 여는 일이고, 수량 글자를 정수로 바꾸다 난 오류는 떨어뜨린 상자입니다. finally 블록은 문 닫힘 장치입니다. | 값 없음(비유). 쓰러진 상자 = 14·16번 셀의 같은 ValueError, 열린 문 = 14번 셀 `파일이 닫혔나요? False`, 닫힘 장치와 닫힌 문 = 16번 셀 finally·`True`. 3~8절 좌우 Before/After 구도 | — |
| 09-1 | 4 핵심 개념 · @ 줄로 장식하기 (노트북 「오늘 볼 그림」) | Mermaid flowchart TD | 함수 정의 바로 위에 @print_call을 적으면, 정의가 끝나자마자 원래 함수가 print_call에 들어갑니다. 반환된 새 함수는 같은 이름에 저장됩니다. | 6번 셀 `@print_call` 정의, 7번 셀 `호출 시작: calculate_line_total`·`받은 인자: (39000, 2) {}`·`호출 끝`·`금액: 78000`·`함수의 이름: wrapper` | @ 줄·부르는 줄·원래 함수 실행 flow(파랑), 이름에 저장된 wrapper tool(초록, 1~8절 「값·파일은 초록」), 출력 measure(노랑) |
| 09-2 | 5 실행 예제 · wraps로 원래 함수의 이름 지키기 | Mermaid flowchart TB(두 칸) | 모듈 functools의 wraps는 원래 함수의 이름 같은 정보를 새 함수에 복사하는 데코레이터입니다. | 5번 셀 `새 함수의 이름: wrapper` / 10번 셀 `새 함수의 이름: calculate_line_total` | 데코레이터를 부른 줄 flow(파랑), 새 함수 wrapper tool(초록), 이름 출력 measure(노랑). 두 출력 모두 실패가 아니라 빨강 없음 |
| 09-3 | 5 실행 예제 · 관리자가 실행되는 차례 | Mermaid sequenceDiagram | yield 줄은 값을 with 블록에 건네고, 블록이 끝날 때까지 그 자리에서 멈춥니다. 블록이 끝나면 멈춘 자리 다음 줄부터 이어서 실행합니다. | 13번 셀 `파일을 열었습니다: orders.txt`·`읽은 줄: ['연필,3', '노트,2']`·`블록 안에서 닫혔나요? False`·`파일을 닫았습니다: orders.txt`·`블록 밖에서 닫혔나요? True` | 메모 노랑(출력이 나온 시점: 열기 직후, 읽은 뒤, 닫은 뒤), 참여자 기본색 |
| 09-4 | 6 일부러 실패해 보기 · Before/After | Mermaid flowchart TB(Before·After 두 칸) | Before와 달라진 곳은 관리자 함수 한 곳입니다. yield 줄을 try 블록에 넣고, 닫는 두 줄을 finally 블록으로 옮깁니다. | 12번 셀(yield 아래 close) → 14번 셀 `오류 메시지: invalid literal for int() with base 10: '많이'`·`파일이 닫혔나요? False` / 15번 셀(try·finally) → 16번 셀 `파일을 닫았습니다: bad_orders.txt`·같은 오류 메시지·`파일이 닫혔나요? True` | 관리자·블록의 줄 flow(파랑), Before 결과 fail(빨강), After 결과 measure(노랑) |

셀 번호는 코드 셀 순번입니다(준비 1, 함수 정의 2, 이름에 담기 3, print_call 정의 4, 직접 넣기 5, @ 정의 6, 부르기 7, 값 바꿔 보기 8, wraps 정의 9, wraps 확인 10, 주문 파일 11, 관리자 정의 12, 관리자 사용 13, Before 14, After 관리자 정의 15, After 실행 16, 심화 17).
색 규칙: 우리가 적은 코드(@ 줄, 부르는 줄, 관리자, with 블록의 줄)는 파랑, 이름에 저장된 값(새 함수 wrapper)은 초록, 출력은 노랑입니다. 빨강은 실제로 파일이 닫히지 않은 Before 결과(09-4)뿐입니다. 두 칸에 같은 ValueError는 오류가 난 줄이 우리가 적은 블록의 줄이라 파랑으로 두고, 결과(닫힘 여부)로 실패를 구분합니다.
노트북 8번 값 바꿔 보기(`(39000,) {'quantity': 3}`, 117000)와 17번 심화 셀(`__enter__`·`__exit__` True 네 줄)은 그림을 만들지 않고 본문 「키워드 인자가 들어간 자리」「확인한 범위」 문단으로만 설명합니다.
기존 도식 `09-concept.svg`(Excalidraw)는 본문에서 뺐습니다. 원본은 `qa/upgrade/before/figures/`에 있고, `figures/`의 옛 파일은 지우지 않았습니다.
