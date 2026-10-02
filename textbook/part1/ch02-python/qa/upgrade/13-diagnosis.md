# 13-파이썬-실습 — 챕터 끝 실습 절 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md` §7-2, `textbook/_notebook/upgrade/PLAYBOOK.md` §3, `.claude/agents/easy-upgrade-editor.md` 6.8. 기준 사례: Ch 22 `09-Middleware-실습`(`author_upgrade.py` section_09), Ch 1 `06-개발환경-실습`(`author_06.py`).
새 절이라 수정 전 원본(`qa/upgrade/before/`)은 없습니다. 생성기: `qa/upgrade/author_13.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 13`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 `qa/upgrade/handoff.md`(특히 `## §12 → 실습`), `author_03`·`04`·`05`·`06`·`07`·`12.py`, `_src/12`, `12-diagnosis.md`·`12-figures.md`, 05-5·06-5 삽화 프롬프트, 챕터 `_src/index.html`(A트랙 보충 과제 6).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 새 절 | 0 |
| G2 | 새 절 | 0 |
| G3 | 새 절 | 0 |
| G4 | 새 절 | 0 |
| G5 | 새 절 | 0 |
| G6 | 새 절 | 0 |
| G7 | 새 절 | 0 |
| 코드 셀 | 새 절 | 16 (준비 1 + 본 경로 15, 심화 셀 없음) |
| 검사한 문장 | 새 절 | 305 (노트북 설명 셀 + `_src`) |
| 모델 호출 | 새 절 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, 2026-09-16, 오류·stderr 출력 0), verify PASS(`13 sections / 190 code cells`). 챕터 전체 게이트 13/13 PASS(`gates-wip-all.json`, G1~G7 0). 빌드 HTML 1280px·390px에서 가로 넘침 없음(scrollWidth 1280·390, SVG 3·삽화 1, 남은 `{{` 토큰 없음, 챕터 index에 13절 링크). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.

**모델 호출 수 근거**: §7-2의 「모델 호출 3~5번」은 LLM 챕터 기준입니다. Ch 2는 절 01~12 모두 모델을 부르지 않고 API 키도 쓰지 않으므로(모델 호출은 Ch 6부터), 이 실습도 0번입니다. Ch 1 06 실습과 같은 판단입니다.

## 주제와 구성

- 주제: 「주문 파일로 합계 내기」. 5절 주문 파일 orders.txt·bad_orders.txt를 같은 조립 함수로 읽어, 수량을 읽을 수 없는 줄은 건너뛴 줄로 기록장에 남기고 나머지 줄로 합계를 냅니다.
- 노트북 순서(PLAYBOOK §3): 준비(임시 폴더 `[]`) → 주제 소개 → 재료(파일 두 개 `['bad_orders.txt', 'orders.txt']`, 가격표 `{'연필': 1000, '노트': 2500}`) → 부품(6절 `OrderLine`, 7절 `calculate_line_total`, 연필 3개 확인 `3000`, 5절 `read_items`, `make_order_line`, 확인 `['연필,3', '노트,2']`·`<class '__main__.OrderLine'>`) → 부품 잇기(`collect_order_lines`, `add_up_total`) → 기록 장치(`print_report`, 기록장 딕셔너리 칸 다섯 개) → 조립(`summarize_orders`, 줄마다 배운 절 주석) → 실행 1 → 실행 2 → 칸별 비교(+assert) → 정리 3줄
- 실행 1(`file_name = "orders.txt"`): `연필 금액: 3000`·`노트 금액: 5000`, 기록장 `읽은 줄 수 | 2`·`주문 수 | 2`·`건너뛴 줄 | []`·`합계 | 8000`
- 실행 2(`file_name = "bad_orders.txt"`, 값 하나만 바꿈): `건너뛴 줄: 연필,많이 / 오류 메시지: invalid literal for int() with base 10: '많이'`·`노트 금액: 5000`, 기록장 `읽은 줄 수 | 2`·`주문 수 | 1`·`건너뛴 줄 | ['연필,많이']`·`합계 | 5000`
- 비교: `같음 | 읽은 줄 수 | 2`, 달라진 칸 수 `4`(파일·주문 수·건너뛴 줄·합계), `assert report_2["읽은 줄 수"] == report_2["주문 수"] + skipped_count` 통과
- 사다리: L1~L4(§12까지 허용 범위 안). 클래스 정의 셀 하나에만 `upgrade_allow=["class_def"]`(6절과 같음). 셀 하나에 함수 하나, 정의 셀과 호출 셀 분리, 함수 본문 10줄 이하

## 앞 절에서 가져온 이름과 경로 판단

- 가져온 것: 1절 `int()`·`type()` / 2절 `for` / 3절 딕셔너리 키 읽기·키 추가·`items()`·`append()`·`+=`·튜플과 풀어 담기·`sorted()`·`!=` / 4절 정의·호출 셀 분리, 지역 변수(가격표를 매개변수 `price_table`로 넘김, 함수 안에서 바깥 이름을 읽는 모양은 4절에서 가르치지 않음) / 5절 `order_text`·`bad_order_text` 글, `with open("w")`, `read_items(file_name)` 그대로, `parse_order()`의 `split(",")`·`int()`, `except ValueError as error`, 임시 폴더 준비 셀 / 6절 `OrderLine(name, count)`(쓰지 않는 `add_count`는 뺌) / 7절 `calculate_line_total(unit_price: int, quantity: int = 1) -> int` 그대로 / Ch 1 6절 칸별 비교 모양(달라짐/같음)
- 새 이름: 함수 `make_order_line`·`collect_order_lines`·`add_up_total`·`print_report`·`summarize_orders`, 값 `unit_prices`·`report_1`·`report_2`. 새 문법·새 API 없음
- 단가 연필 1000원·노트 2500원은 챕터 index A트랙 보충 과제 6과 같은 값(상품 합계 8000원)
- 경로: 기본 경로(A: 01~08 → 12)도 따라가게 1~7절 문법과 `assert`만 씀. 9~11절(@ 줄 정의·Pydantic·픽스처·패키징)은 B 경로 전용이라 쓰지 않음. 8절 pytest는 테스트 파일 쓰기와 `subprocess` 셀이 3~4개 늘어 30분 분량을 넘겨 쓰지 않고, 셀 끝 `assert`로 대신함. 12절 async는 주문 합계와 연결이 억지스러워 쓰지 않음. 본문 b3 표에 경로 열(A·B)을 둠
- 5절과 이어지는 판단: 5절 Before(except Exception → 정상 줄 「노트,2」까지 사라짐)와 After(오류 이름만 받고 ValueError는 함수 밖으로)를 이어, 이번에는 같은 `ValueError`를 줄 하나를 바꾸는 자리에서 받아 그 줄만 기록장에 남김. 「오류를 숨기지 않는다」는 5절 결론과 어긋나지 않게 오류 메시지를 출력하고 건너뛴 줄 칸에 적음. 파일을 읽는 줄은 try 밖이라 FileNotFoundError는 받지 않음(실행하지 않음, 본문 b7)
- 첫 설계에서 칸 「읽은 줄 수」를 `len(order_lines) + len(skipped_lines)`로 계산해 비교 셀 assert가 늘 참이 되는 문제를 발견 → 파일 읽기를 조립 함수로 옮기고(`lines = read_items(file_name)`), 부품 함수는 `collect_order_lines(lines)`로 줄 목록을 받게 바꿔 `len(lines)`로 독립해 셈. 출력은 같음

## 사실 주장 확인

- 실행 출력으로 확인: 노트북 전체 출력(위). 쉼표가 없는 줄은 `split(",")` 풀어 담기에서 ValueError가 날 것이지만 실행하지 않았으므로 본문에는 「실행하지 않았습니다」로만 적음. 가격표에 없는 상품 이름은 단가를 읽는 줄이 try 밖이라 건너뛴 줄에 적히지 않는다고만 적고, 오류 이름은 가르치지 않은 것이라 쓰지 않음
- 뒤 챕터 연결: 본문 b8 「Ch 3 Git과 GitHub 협업에서 파일의 바뀐 내용을 Git으로 기록」(Ch 3 chapter.json 제목·절 이름), 「Ch 4 데이터 처리」(챕터 index 「여기에서 배운 파일과 함수는 Ch 4의 데이터 처리로 이어집니다」)만 씀

## 그림

- Mermaid 3장(PNG 직접 확인): 13-1 조립도(flowchart TB, 587px. 처음 LR로 1254px → TB), 13-2 실행 1 순서(sequenceDiagram, 855px. 메시지를 `<br>`로 줄이고 첫 메모 문구를 줄여 글자가 상자를 넘지 않게 함), 13-3 두 실행 비교(flowchart TB 두 칸, 802px)
- 삽화 1장: 13-4 주문서 두 받침(5절 잉크 얼룩 종이·받침, 7·8·10절 동전을 이어 씀. 3~12절의 좌우 Before/After 대신 Ch 1 6·Ch 22 9 실습처럼 한 장면). nano_banana_pro 16:9 2k, 1회 생성 채택, 2크레딧, job 16184074-47d0-4031-9cd1-fd53efacb1df
- 설계표 `qa/upgrade/13-figures.md`. 색: 조립한 함수 파랑, 값 초록, 기록장 노랑, 실제로 난 ValueError만 빨강

## 바꾼 다른 파일

- `chapter.json` sections 끝에 `13-파이썬-실습`(「파이썬 실습: 주문 파일로 합계 내기」, experiment) 추가
- `_src/12-async와-await.html` b8 「다음 학습과 이어지는 지점」 첫 문장 「Ch 2 본문은 이 절에서 끝납니다」 → `<a href="13-파이썬-실습.html">13절 파이썬 실습</a>에서 1~7절의 부품을 한 함수로 조립합니다`(뒤의 Ch 3·18·30 문장은 유지). 12 노트북·`author_12.py` 정리 셀 끝 「이 절이 Ch 2 본문의 마지막 절입니다」 → 「다음 13절은 이 챕터의 실습입니다. …」. `mdpatch.py`로 재실행 없이 고침, `run_section.sh … 12 --no-exec` 게이트 0건
- `_src/index.html` 「어느 순서로 학습하나요?」 첫 단락 끝에 13절 실습 한 문장 추가(절 목록은 빌더가 chapter.json으로 만듦). 같은 단락의 「12개 노트북」 다운로드 문장과 `downloads/ch02-practice.zip`은 고치지 않음(묶음 재생성은 전체 챕터 뒤 일괄, Ch 1 C-2와 같음)

## 검토에서 볼 곳

- 5절 After(ValueError를 받지 않음)와 이번 실습(ValueError를 받아 건너뜀)의 정책 차이 설명이 학생에게 모순으로 읽히지 않는지(노트북 5번·b3 마지막 단락·복습 3)
- 함수 다섯 개 + 클래스 하나(코드 셀 16개)가 30분 분량에 맞는지. 타입힌트를 7절 함수에만 두고 나머지는 5절 모양대로 없앤 판단(노트북 4번 설명)
- 13-1에서 `read_items()`와 `collect_order_lines()`를 한 파란 상자에 묶은 것, 13-3 실행 1 가운데 회색 「ValueError 없음」 상자

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept-with-fixes(중 1, 하 3, 공통 C-3·C-4 하). 모두 반영했습니다.
- 13-1(중): 노트북 오늘 볼 그림 「위에서 아래로 읽습니다」, 「두 갈래는 모두 맨 아래 기록장에 모입니다」
- 13-2: 「5절 결론은 서로 다른 문제를 같은 빈 결과로 감추지 않는다는 것이었습니다. 이번 함수도 …」(노트북 5번 새 단락, 본문 b3, 복습 3 해설)
- 13-3: 13-3 `b2`를 measure(노랑)로 렌더, 도식 읽기·alt·캡션·설계표. 이 절 그림에 빨강 없음
- 13-4: 「7절에서 본 것처럼, 타입힌트는 표시일 뿐이라 값을 검사하지 않습니다.」
- C-3: 「챕터 소개의 기본 경로(A트랙) 보충 과제 6」. C-4: 노트북 「5·7·8·12절처럼」(권고 5·7·8에 A 경로인 12절을 더한 변형), 본문 b2 「앞의 절에서는」
- 새 커널 출력은 반영 전과 같음. 코드 셀 16, 검사한 문장 311

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/13-파이썬-실습.md`
- 챕터 `gates-after.json`·`chapter-summary.md`·루트 `textbook/qa/upgrade-progress.md`는 챕터 검토 뒤(메인 세션)
- `textbook/downloads/ch02-practice.zip` 재생성, index의 「12개 노트북」 문장
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
