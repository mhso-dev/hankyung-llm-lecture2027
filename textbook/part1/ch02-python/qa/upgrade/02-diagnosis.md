# 02-조건문과-반복문 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/02-concept.*`).
생성기: `qa/upgrade/author_02.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 02`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01절 개선본(`_src/01-*`, 노트북, `author_01.py`, `01-diagnosis.md`).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 31 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 13 (준비 1 + example 9 + before 1 + 심화 1 + after 1) |
| 검사한 문장 | 108 | 265 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, 2026-09-16), verify PASS(12절 89셀). 수정 후 수치는 `gates-wip-02.json`. 수정 전 수치는 `gates-before.json`(덮어쓰지 않음).

## 수정 전 주요 문제

- **사다리 위반(게이트가 못 잡음)**: Before 셀이 기본 경로에서 `try/except IndexError as error`와 `type(error).__name__`을 씀(L3, 5절 이후). `append()`(3절 자료구조)와 복합 대입 `+=`를 설명 없이 사용. G1은 절 위치별 단계를 검사하지 않아 0건으로 통과
- 이어짐: 「대괄호로 묶인 여러 값은 다음 절에서 배울 목록」이라고 적음. Ch 1 1절에서 이미 목록·`for`를 썼고 3절에서 `if/else`를 썼는데 연결이 없음. 1절이 약속한 「회원일 때만 할인」 조건문이 없음. 1절 금액(float 78000.0)과 이 절 금액(int 18000)의 차이 설명 없음
- G5: 제목 셀·「오늘 볼 그림」 없음. 결과 읽기 셀이 없고 설명 셀이 출력 값을 인용하지 않음(4곳), 마지막 셀 뒤 설명 없음
- G6: 코드 이름+조사로 시작하는 문장 27개(「`elif`는」, 「`break`는」, 「`range(4)`는」 등), 70자 초과 1개, 5문장 넘는 단락 2개. 한 단락에 비교 연산자·콜론·`elif`·`else`를 한꺼번에 설명
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 도식 `02-concept.svg`는 18000원 판정과 while 목록을 한 그림에 겹쳐 그림
- 한 셀에 여러 문법: while 셀 하나에 `len`·인덱싱·`+=`·`continue`·`break`·`append`를 모두 넣음

## 바꾼 것

- 노트북(paired 유지): 제목(API 키 불필요·호출 0번·1분 이내) → 오늘 볼 그림(02-1) → 준비(1절 값 78000.0·0.1·True + 주문 세 건 목록) → 회원일 때만 할인(True → 70200.0) → 회원 여부만 False(78000.0) → `if/elif/else`로 42000원 배송비 2000 → `for` 안의 조건문, 경계값 49999·50000 → `range(3)`·`range(1, 3)` → `while`로 위치 0~2 읽기(끝난 뒤 번호 3) → `continue`·`break`(읽은 값 18000·-1·42000·0, 처리 2개, 번호 4) → 값 바꿔 보기 기준 50000 → 40000(1건 → 2건) → Before → 심화 → After → 정리
- **학습 질문 변경**: 「목록 끝을 넘겨 읽는 오류를 어떻게 수정하나요?」 → 「위치 번호로 주문 목록을 읽을 때 첫 주문을 빠뜨리지 않으려면 무엇을 바꾸나요?」. 이유: `IndexError`를 멈추지 않고 보려면 `try/except`가 필요한데 2절 기본 경로에서 쓸 수 없고, 잡지 않은 오류는 `render.py`가 거부함. 데이터(주문 세 건)·형식(paired)·교체 방향(range 위치 계산 → `enumerate`)은 유지. Before는 Ch 1 1절에서 번호를 1부터 붙인 습관으로 `range(1, order_count)`를 써서 18000원을 조용히 빠뜨림(2건·107000·False), After는 반복문 머리만 `enumerate(order_amounts)`로 바꿔 3건·125000·True + `assert`
- 원래 질문의 `IndexError`는 Before 아래 「원리 더 알아보기」 심화 셀(`lesson_level="deep-dive"`, Ch 1 02절과 같은 방식)에서 `range(1, order_count + 1)`로 1회 실행해 `IndexError`·`list index out of range`를 보여 줌. 기본 경로 셀은 심화 셀 변수를 쓰지 않음
- 사다리: 기본 경로는 L1과 이 절에서 가르치는 `elif`·`>=`·`<`·`while`·`continue`·`break`·`range()`·`enumerate()`만 사용. 함수 정의·`try/except`·형식 지정 f-string·`append()`·`+=`·조건 표현식 없음. 개수 세기는 Ch 1의 `number = number + 1` 모양. `upgrade_allow` 예외는 필요 없었음
- 작업자 메모 반영: ① 「다음 절에서 배울 목록」 → 「Ch 1 1절처럼 대괄호로 만든 목록」, 앞에서 배운 내용 표에 Ch 1 1·3·4절 행 ② `elif`·`while`·`break`·`continue`·`range`·`enumerate`를 각각 소제목·용어 표에서 직접 가르침 ③ 1절 약속 「회원일 때만 할인」을 노트북 2번 소제목과 본문 첫 조건문으로 지킴(1절과 같은 7800.0·70200.0 확인, False로 바꾸면 78000.0) ④ 준비 설명·본문 「앞에서 배운 내용」에 「1절 금액은 단가 39000.0이 실수라 실수, 이 절은 1절 주의할 점대로 원 단위 정수」 한 문장
- 본문 10블록 전체를 다시 씀. 용어 11개 표, 「확인한 범위」(`range(order_count)` 고치기·빈 목록·조건 순서 바꾸기는 실행하지 않음), 복습 6문항
- 그림: Mermaid 4장(조건 검사 순서, while 갈림길, 읽은 차례, Before/After) + 삽화 1장(상자 분류대). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 검토에서 볼 곳

- 학습 질문을 바꾼 것이 챕터 의도와 맞는지(위 「학습 질문 변경」). 집필점검표 02행도 새 질문으로 고침
- 실행하지 않은 주장 세 곳: 「번호 증가를 `continue` 뒤에 두면 반복이 끝나지 않음」, 「조건 순서를 바꾸면 65000원도 2000원」, 「`range(order_count)`로 고쳐도 0부터」. 모두 「이번에 실행하지 않았습니다」로 적음. 「커널 중지(Interrupt)」 안내는 화면 확인 없이 적음
- 02-3 그림에서 continue·break 차례(-1, 0)를 값인데도 파랑으로 둔 색 선택(설계표 색 규칙에 이유 기록)
- 삽화: 줄에 남은 상자 세 개가 크기순으로 놓임. 관계(한 상자 → 한 칸) 판독에는 영향 없어 채택

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-A.md`

- 판정 accept(하 3, 공통 C-5 하). 모두 반영했습니다. 노트북 코드·설명은 바뀌지 않아 `--no-exec`로 렌더·첨부·빌드만 했습니다.
- 02-1: 표 첫 칸 「1절」(2곳). 02-2: 비유 「칸에 가까운 줄 맨 앞의 상자부터」, 그림 읽기·02-5 캡션 읽는 법 「줄 맨 앞(오른쪽 끝)」
- 02-3: 02-2 mmd 선언 순서를 바꿔 두 번 렌더. 첫 순서는 「거짓」 라벨이 다른 선에 겹쳐 버리고, 최종본(S참R·S거짓E·R→N·continue·N거짓Z·Z거짓P·break·다음 차례)은 선 교차가 없음을 PNG로 확인. 배치가 바뀌어 도식 읽기·캡션 읽는 법을 「오른쪽 파란 상자」, 「왼쪽 아래 「처리한 금액 출력」」으로 고침
- C-5: 캡션 「예약어 continue는 … 예약어 break는 …」(caption.md·_src 토큰)
- 검사한 문장 265

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/02-조건문과-반복문.md`
- 3절 기존 본문은 「반복문이 읽은 여러 값을」로 시작해 이어짐은 맞음. 3절 개선 때 이 절이 `append()`·`+=`를 가르치지 않았다는 점을 반영해야 함
- 챕터 전체 `gates-after.json`과 루트 `textbook/qa/upgrade-progress.md` 갱신은 챕터를 마친 뒤
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
