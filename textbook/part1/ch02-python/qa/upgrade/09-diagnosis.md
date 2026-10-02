# 09-데코레이터와-컨텍스트-매니저 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/09-concept.*`).
생성기: `qa/upgrade/author_09.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 09`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01~08절 개선본(`_src`, 노트북, `author_08.py`, `08-diagnosis.md`, `08-figures.md`), `qa/upgrade/handoff.md`(특히 `## §08 → §09`), `upgrade_gates.py`(L6 위치 확인).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 4 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 8 | 0 |
| G6 | 28 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 17 (준비 1 + example 12 + before 1 + after 3(심화 1)) |
| 검사한 문장 | 97 | 407 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, 2026-09-16, 오류 출력 0), verify PASS(12절 146셀). 수정 후 수치는 `gates-wip-09.json`, 수정 전은 `gates-before.json`(덮어쓰지 않음). 빌드 HTML 가로 넘침 없음(puppeteer 1280px·390px에서 scrollWidth 1280·390).

## 수정 전 주요 문제

- **G1**: 한 셀에 데코레이터 정의·장식한 함수 정의·호출을 함께 둠(함수 둘, `nested_def`·`varargs_def`), Before에 준비용 클래스 `DemoResource`(`class_def`, 메서드 두 개에 `-> None`)
- **아직 안 배운 문법(G1이 잡지 않음)**: `inspect.signature()`, 독스트링, `raise RuntimeError(...)`, `type(error).__name__`(handoff: 기본 경로에서 안 씀), f-string 출력(`f"호출 시작: {function.__name__}"`), `managed = None`과 `assert managed is not None and managed.closed is True`, 반환 표시 `-> None`(handoff: 아직 안 씀), 한 셀에 import 세 줄로 `inspect`·`contextmanager`·`wraps`를 미리 불러옴
- **이어짐 결함**: 「07절의 타입힌트는 B 경로에서 배웠지만, 데코레이터 예제의 보조 타입 표기는 제거」 — 개선된 7절은 타입힌트를 기본 경로에서 가르쳤고 8절도 `-> int`를 씀. 그런데 기존 예제는 `normalize_title(title: str) -> str`에 타입힌트를 그대로 둬 문장과 코드도 어긋남. 데이터 「월간 보고서」 제목·`DemoResource` 모의 자원이 1~8절 주문 데이터와 무관. 5절 「with 원리는 9절」 약속과 8절 심화 셀의 `@pytest.mark.parametrize`를 받지 않음
- **Before/After 구조**: Before는 관리자 없이 `try` 안에서 `raise` 뒤에 `close()`를 둔 코드, After는 `@contextmanager`와 `try/finally`를 한꺼번에 도입 → 두 셀 사이에 바뀐 것이 여러 개(관리자 도입 + finally)
- G5: 제목 셀·「오늘 볼 그림」 없음, 결과 읽기 셀 없음. G6: 코드 이름으로 시작하는 문장 20여 개(「`trace`의」「`*args`는」「`wraps`는」 등), 70자 초과 4개, 6문장 넘는 단락 2개. G7: Mermaid 0장, 삽화 0장, 설계표 없음

## §08이 넘긴 판단 거리

- **「07절 타입힌트는 B 경로」 문장**: 지우고 「7절에서 타입힌트를 기본 경로로 배웠으므로, 이 절도 장식할 함수와 관리자의 매개변수에 타입힌트를 적습니다」로 바꿈. 장식할 함수는 7·8절과 같은 `calculate_line_total(unit_price: int, quantity: int = 1) -> int`, 관리자는 `open_order_file(file_name: str)`. 함수를 받는 매개변수 `function`과 wrapper의 `*args`·`**kwargs`, 관리자의 반환 자료형에는 적지 않고, 「함수를 가리키는 자료형 이름은 아직 배우지 않았다」고 한 문장으로 적음(`Callable`·`Iterator`는 쓰지 않음)
- **`@` 줄과 8절 심화 셀 연결**: 노트북 4번 설명 셀과 본문 「@ 줄로 장식하기」에 「8절 원리 더 알아보기의 `@pytest.mark.parametrize(...)` 줄도 같은 `@` 줄」 문장을 둠. pytest 9.1.1 `_pytest/mark/structures.py`의 `MarkDecorator.__call__`이 함수에 표시를 붙이고 같은 함수를 반환함을 소스로 확인해, 본문에 「함수를 감싸지 않고 입력 묶음 표시만 붙인 같은 함수를 반환」으로 적음
- **사다리**: `upgrade_allow=["nested_def", "varargs_def"]`는 데코레이터 정의 셀 두 개(print_call, wraps 판)에만. `@print_call`·`@wraps(function)`·`@contextmanager` 사용은 L6이며 절에서 처음 쓰는 자리에 「이 줄은 아래 함수를 ○○」 설명을 둠. L5(스키마 클래스)·L7(async) 없음. 클래스 정의가 없도록 `DemoResource`를 5절 실제 파일로 바꿈(가짜 자원이 아닌 실제 파일 객체의 `closed`)
- **5절 약속**: 「with 블록의 원리는 9절」을 관리자 셀(준비 → yield에서 멈춤 → 블록 → 이어서 정리)과 심화 셀(`__enter__`·`__exit__`)로 받음

## 바꾼 것

- 노트북(paired 유지): 제목 → 오늘 볼 그림(09-1) → 준비(임시 폴더 `[]`) → 7절 함수 정의 → 이름에 담기(`calculate_line_total`, `78000`) → 데코레이터 print_call 정의 → 직접 넣기(`받은 인자: (39000, 2) {}`, `금액: 78000`, `새 함수의 이름: wrapper`) → `@print_call` 정의 → 부르기(같은 네 줄, `wrapper`) → 값 바꿔 보기: `quantity=3`(`(39000,) {'quantity': 3}`, `117000`) → `@wraps(function)` 판 정의 → line_function 넣기(`calculate_line_total`) → 5절 주문 파일 두 개(`['bad_orders.txt', 'orders.txt']`, `True`) → `@contextmanager` 관리자 정의(yield 아래 close) → 관리자 사용(열었습니다·읽은 줄·안 `False`·닫았습니다·밖 `True`) → Before: 같은 관리자로 bad_orders.txt, `int('많이')`(열었습니다·`invalid literal for int() with base 10: '많이'`·`False`) → After: yield를 try, 닫는 두 줄을 finally로 옮겨 다시 정의 → 같은 셀(열었습니다·닫았습니다·같은 오류 메시지·`True`, `assert order_file.closed`) → 원리 더 알아보기(심화): `hasattr`로 open() 파일·관리자의 `__enter__`·`__exit__`(True 네 줄, with 없이 부르면 열었습니다가 안 나옴) → 정리
- **학습 질문·실패 구조·형식 유지**: 질문 「예외가 발생해도 자원을 정리하려면?」을 주문 파일 상황으로 구체화. 「같은 오류를 유지하고 close 위치만 관리자의 finally로」 구조와 paired 형식을 유지하되, Before도 같은 관리자를 쓰게 해 Before/After 차이를 관리자 정의의 try·finally 하나로 줄임(기존은 관리자 도입과 finally가 함께 바뀜)
- **학습 목표 조정**: 「`functools.wraps`로 이름·설명·서명 유지」 → 이름만 관찰(`inspect.signature`·독스트링 제거, 본문에 「문서는 설명 글도 복사한다고 적지만 이 절에서는 이름만 확인」). `*args`·`**kwargs`는 받은 인자를 출력해 튜플·딕셔너리로 보이게 함(3절 연결)
- 본문 10블록 전체를 다시 씀. 「앞에서 배운 내용」 표 7행, 용어 8개 표, 「함수를 값처럼 이름에 담기」「데코레이터와 감싸는 함수」「@ 줄로 장식하기」「컨텍스트 매니저와 yield」「오류가 나도 실행되는 finally 블록」「키워드 인자가 들어간 자리」「wraps로 원래 함수의 이름 지키기」「관리자가 실행되는 차례」「확인한 범위」 소제목, 복습 6문항(4 → 6), 참고 자료 7개. 다음 학습: B는 10절 Pydantic, A는 12절, Ch 19 `@tool`(Ch 19 01절 본문 「`@tool`은 바로 아래 파이썬 함수를 LangChain의 도구 객체로 감쌉니다」 확인). 기존 본문의 Ch 18·Ch 30 연결 문장은 확인하지 않아 뺌
- 그림: Mermaid 4장(데코레이터 호출 차례, wraps 이름 비교, with 블록 차례 sequenceDiagram, Before/After) + 삽화 1장(문 닫힘 장치, 1회 생성 통과, 3~8절 좌우 Before/After 구도). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 검토에서 볼 곳

- 새 문법 양: 함수 안의 함수·`*args`/`**kwargs`·`@`·`wraps`·`contextmanager`·`yield`·`finally`를 한 절에 둠(기존 절 범위와 같음). 코드 셀 17개로 가장 긴 노트북. `yield`는 「값을 건네고 멈추는 줄」로만 설명하고 제너레이터 용어는 쓰지 않음
- 본문 「새 함수 wrapper는 print_call이 받은 원래 함수 function을 기억해 둡니다」(클로저라는 말은 쓰지 않음)와 Before 설명 「오류가 yield 자리에서 다시 일어남」(contextlib 문서·`__exit__`의 `gen.throw()` 소스 근거)
- 삽화: 왼쪽 문이 「활짝」보다 반쯤 열림(열린 것은 분명해 채택). 문 닫힘 장치는 문 위 회색 팔

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept-with-fixes(하 4). 모두 반영했습니다.
- 09-1: 삽화 그림 읽기·alt(_src·caption.md)·캡션 읽는 법을 「열린 상자와 바닥에 쏟아진 종이」로
- 09-2: 노트북 6번·본문에 「괄호가 붙은 `@wraps(function)` 줄은 … 이름을 복사한 같은 wrapper를 반환합니다.」
- 09-3: 노트북 3번 「이 장면은 이번에 실행하지 않았습니다.」 09-4: 주의할 점 「return 줄이 없는 wrapper로 장식하는 장면은 이번에 실행하지 않았습니다.」
- 새 커널 출력은 반영 전과 같음. 코드 셀 17, 검사한 문장 413

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/09-데코레이터와-컨텍스트-매니저.md`
- 챕터 전체 `gates-after.json`과 루트 `textbook/qa/upgrade-progress.md` 갱신은 챕터를 마친 뒤
- 챕터 index의 A트랙 보충 과제 5(07절 `add_tax`, 08절 `discounted`)는 개선 전 데이터를 가리킴(이 절 범위 밖, 챕터 마무리 때 확인)
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
