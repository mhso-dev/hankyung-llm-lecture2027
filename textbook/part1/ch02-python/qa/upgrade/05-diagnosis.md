# 05-파일과-예외 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/05-concept.*`).
생성기: `qa/upgrade/author_05.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 05`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01~04절 개선본(`_src/01-*`~`_src/04-*`, 노트북, `author_01.py`~`author_04.py`, `04-diagnosis.md`, `04-figures.md`), 메인 세션의 4절 작업자 메모.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 8 | 0 |
| G6 | 24 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 17 (준비 1 + example 10 + before 3 + after 3) |
| 검사한 문장 | 117 | 374 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12, 2026-09-16, 오류 출력 0), verify PASS(12절 119셀). 수정 후 수치는 `gates-wip-05.json`. 수정 전 수치는 `gates-before.json`(덮어쓰지 않음). 빌드 HTML 가로 넘침 없음(puppeteer 1280px·390px에서 scrollWidth 1280·390). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.

## 수정 전 주요 문제

- **사다리 위반(게이트가 못 잡음)**: 기본 경로에서 `from pathlib import Path`·`TemporaryDirectory`(L4, 7절 이후), `Path` 객체의 `/`·`write_text()`·`read_text()`. 정의 셀과 호출 셀을 나누지 않음(`def` 뒤 바로 호출). 가르치지 않은 `raise AssertionError`, `try/except/else`, `type(error).__name__`을 씀. 키워드 인자 `encoding=`을 설명 없이 사용. 초보자에게 어려운 모양으로 try 블록 안의 `return`(`read_items_or_empty`)
- **이어짐 결함**: 「앞에서 배운 내용」이 「03절 목록과 튜플, 04절 함수」 한 단락. 1절이 5절로 미룬 「숫자 모양이 아닌 문자열」, 2·3절 심화 셀이 5절로 미룬 `try/except`, 4절의 정의/호출 분리·기본값 매개변수와 연결 없음. 「with open(...)」은 주의할 점에 말로만 나오고 코드에서 쓰지 않음
- **Before/After 구조**: Before가 틀린 결과가 아니라 「오류가 난다」를 try/except로 관찰하는 셀이라, After와 달라진 한 줄이 드러나지 않음. 1~4절의 「실행이 멈추지 않아도 결과는 틀릴 수 있다」 흐름과 어긋남
- G5: 제목 셀·「오늘 볼 그림」 없음. 결과 읽기가 출력 값을 인용하지 않음(5곳), After 셀 뒤 설명 없음
- G6: 코드 이름+조사로 시작하는 문장 22개(「`parse_order()`는」, 「`try`는」 등), 70자 초과 2개
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 도식 `05-concept.svg`는 정상 파일과 누락 파일을 한 그림에 겹쳐 그림

## 바꾼 것

- 노트북(paired 유지): 제목(API 키 불필요·호출 0번·1분 이내) → 오늘 볼 그림(05-1) → 준비(빈 임시 폴더로 작업 위치 이동, 파일 목록 `[]`) → 파일 쓰기(쓴 글자 수 10) → 읽기(10, `closed` True) → `read_items()` 정의·호출(`['연필,3', '노트,2']`) → `parse_order()` 정의·반복(`[('연필', 3), ('노트', 2)]`) → 값 바꿔 보기(수량 3 → 5, 줄 수 2) → 없는 파일 `FileNotFoundError` → 「연필,많이」 `ValueError` → Before(`bad_orders.txt` 만들기, `except Exception` 정의, 두 파일 `[]`·`[]`·True) → After(`except FileNotFoundError` 정의, missing `[]`·orders.txt 연필 5, bad_orders.txt는 함수 밖 ValueError) → 정리
- **학습 질문·데이터·형식 유지**: 질문 「없는 파일을 선택적으로 처리하려면 무엇을 잡나요?」를 쉬운 말로 「없는 파일만 빈 목록으로 처리하고 다른 오류는 드러내려면, except 줄에 무엇을 적어야 할까요?」로 바꿈(뜻 같음). 데이터 연필,3 / 노트,2, 수량 3 → 5, `missing.txt`, 「연필,많이」의 ValueError, 함수 이름 `read_items()`·`parse_order()` 유지. 기존 After의 「파일 없음만 빈 목록, ValueError는 드러남」을 Before/After의 차이로 옮김: Before `except Exception`(두 문제가 같은 빈 목록) → After `except FileNotFoundError`(except 줄 한 줄만 바뀜). `read_items_or_empty()`는 두 번 반환하는 모양이라 `load_orders_before()`/`load_orders()`로 바꿈
- 사다리: L3이 처음 허용되는 절. 이 절에서 가르치는 `open()`·모드 `"w"`/`"r"`·키워드 인자·`with ... as`·`write()`·`read()`·`closed`·`splitlines()`·`split()`·`try/except 예외이름`·`as error`만 새로 씀. 예외 이름 없는 `except:`는 코드에 쓰지 않고 본문에서 「쓰지 않는다」고만 적음. 셀 하나에 함수 하나, 본문 최대 9줄, 정의 셀 4곳과 호출 셀을 모두 나눔. 타입힌트·`raise`·`else`·`finally`·`//`·형식 지정 f-string 없음, f-string 자체를 쓰지 않음(`print(라벨, 값)`만). `upgrade_allow` 예외 없음
- **준비 셀의 표준 라이브러리 import**: 1절 준비 셀(`import platform`)과 같은 방식으로 준비 셀(`lesson_role=setup`)에만 `os`·`tempfile`을 씀. `mkdtemp()`로 빈 폴더를 만들고 `os.chdir()`로 옮김. 이유: 실행 도구 `execute.py`의 커널 작업 폴더가 프로젝트 루트라, 파일 이름만 쓰면 루트에 orders.txt가 남음(삭제 금지). 학생 컴퓨터의 실습 폴더에도 파일을 남기지 않음. 경로는 출력하지 않음. 뒤 셀은 모두 파일 이름만 씀
- 앞 절과의 연결: 1절 Before 222(문자열 수량)와 「숫자 모양이 아닌 문자열은 5절」 약속 → 5·8번 소제목, 2절 IndexError·3절 TypeError 심화 셀의 「문법은 5절」 → 7번 소제목, 3절 튜플·풀어 담기·빈 목록+append → `parse_order()`와 주문 목록, 4절 `quantity=1` → 키워드 인자 설명, 4절 정의/호출 분리 → 모든 함수, Ch 1 2절 `cd`·현재 작업 폴더 → 준비 셀, Ch 1 4절 여러 줄 글 → `order_text`. 삽화도 3절 03-5·4절 04-5의 좌우 Before/After 구도를 이어 씀
- 4절 작업자 메모의 이름·값(`calculate_payment` 70200, `payments`, `add_tag`)은 이 절 코드에 쓰지 않음. 파일 한 줄 나누기 연습에 맞춰 기존 5절 데이터(연필·노트)를 유지하고, 그 이유를 「앞에서 배운 내용」 끝에 적음. `calculate_line_total(unit_price, quantity=1)`은 키워드 인자 설명과 복습 3번에서 이름으로만 이어 씀
- 본문 10블록 전체를 다시 씀. 용어 10개 표, 「앞에서 배운 내용」 표 7행, 「확인한 범위」(인코딩이 다른 파일·인코딩 생략·모드 "a"·큰 파일·멈추는 셀·KeyError 미실행), 복습 6문항(4 → 6), 참고 자료 5개
- 그림: Mermaid 4장(파일 쓰고 읽기, 줄을 주문으로, try/except 차례, Before/After) + 삽화 1장(봉투 받침, 1회 생성 통과). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 검토에서 볼 곳

- 준비 셀의 `os.chdir()`: 학생이 VS Code 탐색기에서 orders.txt를 찾을 수 없음(주의할 점에 적음). 1절 준비 셀의 `import platform` 선례를 따랐지만, 규격상 import는 7절(L4)이라 준비 셀 예외로 받아들일지 확인 필요
- Before가 기존(「없는 파일 오류를 관찰」)에서 「except Exception이 두 문제를 감춤」으로 바뀜. 학습 질문은 같지만 Before 장면이 달라졌으므로 원래 의도와 맞는지
- After 17셀은 함수 밖으로 나온 ValueError를 관찰하려고 호출한 셀에서 `except ValueError`를 씀. 「좁게 받기」를 가르치며 호출 셀에서 다시 받는 모양이 헷갈리지 않는지(본문과 결과 읽기에서 「셀이 멈추지 않도록」이라고 이유를 적음)
- 한 절에 새 문법이 많음(파일 열기·모드·키워드 인자·with·try/except·as·오류 이름 셋). 코드 셀 17개(정의 셀 4개)로 나눴지만 강의 1h 분량에 맞는지

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-A.md`

- 판정 accept-with-fixes(중 2, 하 2, 공통 C-1 중·C-4 하·Q3). 모두 반영했습니다(05-2는 결정대로 변형).
- 05-1(중): 노트북 2번·본문 「정의 줄의 `quantity=1`은 기본값을 정하는 자리이고, 호출 괄호 안의 `encoding="utf-8"`은 값을 이름으로 넣는 자리입니다」, 복습 3 질문·해설, handoff §05→§06
- 05-2(중, 변형): 준비 셀이 `print("작업 폴더:", practice_folder)`로 경로를 출력(실행 도구 `execute.py`가 사용자 폴더를 `[사용자 폴더]`로 가림, 결과 읽기에 설명). 결과 읽기 「실행할 때마다 새 임시 폴더를 만들고 앞 폴더는 지우지 않습니다」, 2번 설명 「앞에서 쓴 파일은 준비 셀이 출력한 앞 폴더에 남아 있습니다」, 주의할 점 항목 추가. 「파일은 커널을 다시 시작해도 남는다」와 모순되지 않음
- 05-3: After 호출 셀 설명·본문 「실제 프로그램에서는 이 오류를 받지 않고 멈추게 두어 파일을 고칩니다. 노트북은 끝까지 실행하려고 이 셀에서만 받았습니다.」
- 05-4: 05-3의 FileNotFoundError를 measure(노랑)로 바꿔 렌더, 도식 읽기·캡션·설계표. 챕터 색 규칙(규격 §5-3 「잡아서 기록한 오류는 노랑, 프로그램을 멈춘 실패는 빨강」)
- C-1: 준비 셀 `upgrade_allow=["stdlib-import"]`, 「코드의 `import` 줄은」. C-4: 다음 학습 「확장 경로(B)의 9절」
- Q3: 노트북 준비물 아래·본문 b5 「강의 시간에는 2~5번과 7~10번 소제목을 설명합니다. 6번(값 바꿔 보기)의 비교는 실습 시간에 읽습니다. 강의에서도 6번의 코드 셀 두 개는 실행해 둡니다(10번 After가 6번 파일을 읽음)」. **강사 확인 대상**
- 검토 밖: `visual.cjs`가 05-4 SVG 글자 13.5px를 잡아 라벨 줄바꿈으로 폭 898 → 846(PNG 확인)
- C-6: 위 게이트 표의 검사한 문장을 369 → 374(`gates-wip-05.json`)로 고침. 반영 뒤 401
- 출력 차이는 준비 셀의 작업 폴더 줄 하나. 코드 셀 17

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/05-파일과-예외.md`
- 6절 기존 본문·집필점검표는 「두 주문과 첫 주문의 노트 추가, 클래스 목록 → 인스턴스 목록」. 이 절의 연필·노트 주문 튜플과 4절 기본값 목록 공유(`tags=[]`)가 6절 클래스 속성 공유와 이어짐. 인계 내용은 `qa/upgrade/handoff.md`의 `## §05 → §06`
- 챕터 전체 `gates-after.json`과 루트 `textbook/qa/upgrade-progress.md` 갱신은 챕터를 마친 뒤
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
