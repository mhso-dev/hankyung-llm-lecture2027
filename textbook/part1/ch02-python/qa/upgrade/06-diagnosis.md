# 06-클래스 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/06-concept.*`).
생성기: `qa/upgrade/author_06.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 06`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01~05절 개선본(`_src/01-*`~`_src/05-*`, 노트북, `author_01.py`~`author_05.py`, `05-diagnosis.md`, `05-figures.md`), `qa/upgrade/handoff.md`의 `## §05 → §06`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 3 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 23 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 11 (준비 1 + example 5 + before 3(심화 1) + after 2) |
| 검사한 문장 | 112 | 327 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12, 2026-09-16, 오류 출력 0), verify PASS(12절 124셀). 수정 후 수치는 `gates-wip-06.json`. 수정 전 수치는 `gates-before.json`(덮어쓰지 않음). 빌드 HTML 가로 넘침 없음(puppeteer 1280px·390px에서 scrollWidth 1280·390). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.

## 수정 전 주요 문제

- **G1**: 클래스 정의 세 셀(`Order`·`SharedOrder`·`IsolatedOrder`)이 `class_def`. 클래스가 학습 목표인 절인데 예외 표시가 없음. 정의 셀과 호출 셀을 나누지 않음(클래스 정의 뒤 바로 인스턴스·호출)
- **이어짐 결함**: 「앞에서 배운 내용」이 「03절 목록, 04절 함수, 05절 튜플」 한 단락(5문장 넘음). 5절 주문 목록 `[('연필', 3), ('노트', 2)]`, 5절 `file.closed`(속성), 4절 기본값 빈 목록 Before(같은 구조의 실수), 3절 `is`·튜플 TypeError, 1절 `type()`의 `<class 'int'>`와 연결 없음. 「05절에서 파일의 주문 한 줄을 튜플로 바꾸었다면」처럼 가정형으로만 언급
- **설명 순서**: 첫 코드 셀에 클래스 정의·`__init__`·`self`·메서드·인스턴스·호출이 한꺼번에 나옴. 예제에서 이미 정답(`self.items = []`)을 보여 준 뒤 Before에서 같은 질문을 다시 물음
- **Before/After**: Before 클래스에 `__init__`·메서드가 없어 예제 `Order`와 모양이 다르고, After와 달라진 한 줄이 드러나지 않음. 목록에 메서드가 아니라 `bad_first.items.append()`로 직접 추가. Before 셀에 `assert bad_second.items == ["노트"]`로 틀린 결과를 단언
- G5: 제목 셀·「오늘 볼 그림」 없음. 결과 읽기 셀이 없고 설명 셀이 출력 값을 인용하지 않음(4곳), After 셀 뒤 설명 없음
- G6: 코드 이름+조사로 시작하는 문장 20개(「`self`는」, 「`is`는」, 「`class Order:`는」 등), 70자 초과 2개, 5문장 넘는 단락 1개
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 도식 `06-concept.svg`는 인스턴스 두 개와 지우개 추가를 한 그림에 그렸고 본문과 셀 번호가 맞지 않음
- 「속성(attribute)」 정의에서 클래스 속성 공유를 「기본적으로 모든 인스턴스가 함께 참조」라고만 쓰고, 인스턴스에 없으면 클래스에서 찾는다는 차례를 보이지 않음

## 바꾼 것

- 노트북(paired 유지): 제목(API 키 불필요·호출 0번·1분 이내) → 오늘 볼 그림(06-1) → 준비(5절 주문 목록 `orders` 다시 저장) → 튜플 번호 읽기(`연필`·`3`) → `OrderLine` 정의(출력 없음) → 인스턴스 두 개(`pencil 수량: 3`·`note 수량: 2`·`<class '__main__.OrderLine'>`) → 메서드 `pencil.add_count(2)`(5·2) → 값 바꿔 보기 `note.add_count(2)`(5·4) → Before `OrderBefore` 정의·호출(노트 추가 뒤 준호 `['노트']`, 둘 다 `['노트', '연필']`, True)·심화 `__dict__`(`{'customer': '민지'}`, 클래스 items `['노트', '연필']`) → After `Order` 정의·호출(`[]`, `['노트']`·`['연필']`, False, assert) → 정리
- **학습 질문·데이터·형식 유지**: 질문 「인스턴스마다 목록을 따로 가지려면 어디에 만드나요?」를 쉬운 말로 「주문마다 상품 목록을 따로 가지게 하려면, 빈 목록을 클래스의 어디에서 만들어야 할까요?」로 바꿈(뜻 같음). 민지·준호 두 주문, 노트 추가, 클래스 본문 `items = []` → `__init__` 안 `self.items = []` 유지. 기존 예제의 준호 연필은 Before/After의 둘째 추가로 옮김(4절 신규·배송 두 호출과 같은 모양). 기존 예제의 「지우개 추가」는 빼고, 수량을 바꾸는 `add_count()`로 인스턴스 상태 분리를 보임
- **예제와 Before/After 분리**: 4절(예제 `quantity=1` → Before `tags=[]`)과 5절(예제 `except FileNotFoundError` → Before `except Exception`)처럼, 예제는 목록 없는 `OrderLine`(이름·수량)으로 클래스·인스턴스·`self`·메서드를 가르치고, 목록 속성의 자리는 Before/After에서 처음 다룸. Before와 After 클래스는 빈 목록 줄의 자리만 다름(`OrderBefore` → `Order`, 4·5절 `_before` 이름 규칙)
- 사다리: 클래스를 정의하는 세 셀에만 `upgrade_allow=["class_def"]`. 이 절에서 가르치는 `class`·`__init__`·`self`·속성·메서드·클래스 속성만 새로 씀. 메서드는 클래스당 둘 이하·본문 1~2줄, 정의 셀과 호출 셀을 모두 나눔. import·파일·try/except·타입힌트·f-string 없음(`print(라벨, 값)`만). `__dict__`는 심화 셀에만(4절 `__defaults__`와 같음). 5절의 `os`·`tempfile` 준비 셀은 파일을 만들지 않으므로 쓰지 않음
- 앞 절과의 연결: 5절 주문 목록·`parse_order()` 튜플 순서 → 준비·2번 소제목, 5절 수량 3 → 5를 파일 다시 쓰기로 바꾼 셀 → `add_count(2)`로 5, 5절 `file.closed` → 속성, 3절 튜플 TypeError(심화) → 「튜플은 바꿀 수 없음」, 3절 `is`·`append()` → Before/After 검사와 `add()`, 4절 정의/호출 분리·return 없는 함수 → 메서드, 4절 기본값 목록 Before → 이 절 Before와 나란히 설명(본문·결과 읽기·복습 6), 1절 `type()`의 `<class 'int'>` → `<class '__main__.OrderLine'>`(`__main__`의 뜻은 7절로 미룸), 1절·5절 준비 셀의 import → 7절 예고. 삽화도 3~5절의 좌우 Before/After 구도를 이어 씀
- 본문 10블록 전체를 다시 씀. 용어 8개 표, 「앞에서 배운 내용」 표 7행, 「확인한 범위」(딕셔너리 클래스 속성·바꾸지 않는 클래스 속성·없는 속성 오류·상속 미실행), 복습 6문항(4 → 6), 참고 자료 5개(Python 3.12 자습서 9.3.1·9.3.2·9.3.4·9.3.5·9.4를 내려받아 문장 확인: `__init__` 자동 호출, 메서드 첫 인자로 인스턴스 전달, 클래스 변수는 모든 인스턴스가 공유, 같은 이름은 인스턴스를 먼저 찾음)
- 그림: Mermaid 4장(클래스와 인스턴스, 속성 찾는 차례, self에 들어가는 인스턴스, Before/After) + 삽화 1장(주문서 바구니, 1회 생성 통과). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 검토에서 볼 곳

- 클래스 정의 셀에 메서드가 둘(`__init__` + `add_count()`/`add()`). 규격 L2 「셀 하나에 함수 하나」를 클래스 안 메서드에도 적용할지. 클래스를 두 번 다시 정의하는 방법(먼저 `__init__`만)은 앞 인스턴스에 메서드가 없는 혼란이 커서 택하지 않음
- 「인스턴스에 없는 이름은 클래스에서 찾는다」는 자습서 9.4와 심화 셀 `__dict__` 출력으로 뒷받침했지만, 준호 주문 인스턴스의 `__dict__`는 출력하지 않음(본문은 「초기화 메서드가 customer만 저장하므로」라고 코드 근거로 적음)
- 예제의 기존 「지우개 추가」 장면을 `add_count()`로 바꿔 예제가 목록을 쓰지 않음. 원래 예제의 의도(인스턴스별 상태 분리)는 수량 3·2 → 5·2 → 5·4로 보였지만, 목록 상태 분리는 After 한 곳에서만 확인
- 7절 기존 본문의 「다음 절에서는 `Order`처럼 커진 정의를 별도 `.py` 파일에」 연결은 7절 작업자가 확인(`handoff.md`)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-A.md`

- 판정 accept(하 2, 공통 C-5 하). 모두 반영했습니다.
- Q2 결정: 클래스 정의 셀의 메서드 2개 허용. 규격 §2-4에 「클래스 정의 셀은 메서드 2개 이하, 메서드 본문 3줄 이하면 한 셀에 둔다」, PLAYBOOK §4 한 줄
- 06-1: 비유 둘째 단락 앞 「이번에는 상품 한 줄이 아니라 고객 한 명의 주문서 양식을 생각합니다.」
- 06-2: 심화 셀에 `junho_attributes = junho_order.__dict__` 출력 `{'customer': '준호'}`를 더하고, 결과 읽기·06-2 도식 읽기를 출력 근거로 고침
- C-5: 06-3 캡션 「점 왼쪽이 pencil이면 pencil만 5, note이면 note만 4가 됩니다.」
- 출력 차이는 심화 셀 한 줄. 코드 셀 11, 검사한 문장 329

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/06-클래스.md`
- 챕터 전체 `gates-after.json`과 루트 `textbook/qa/upgrade-progress.md` 갱신은 챕터를 마친 뒤
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
