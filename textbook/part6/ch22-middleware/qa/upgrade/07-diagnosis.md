# 07-순서와-합성 — 품질 개선 진단과 결과

작성 2026-09-15. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 5 | 0 |
| G2 | 10 | 0 |
| G3 | 6 | 0 |
| G4 | 1 | 0 |
| G5 | 6 | 0 |
| G6 | 14 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 14 |
| 검사한 문장 | 82 | 125 |

## 수정 전 주요 문제

- G1: class_def 2, varargs_def 2, conditional_expression 1
- G2: one_line_compound 8, over_15_lines 1, semicolon 1
- G3: boilerplate_comment 6
- G4: fake_model 1
- G5: result_reading_quotes_no_output 3, title_cell_missing 1, core_figure_attachment_missing 1, result_reading_after_missing 1
- G6: english_start 8, long 5, dense_paragraph 1
  - 예: wrap 훅은 첫 항목이 가장 바깥쪽이 되어 A before, B before, C before, 모델, C after, B after, A after 순서가 됩니다
  - 예: 서로 독립적인 읽기 전용 기록은 순서 영향이 작지만, 요청이나 상태를 수정하는 미들웨어는 교환해도 같은 결과가 나오는지 확인해야 합니다
  - 예: before_agent와 before_model은 A·B·C, wrap_model_call 진입은 A·B·C이고 반환은 C·B·A, after_model과 after_agent는 C·B·A입니다
- G7: mermaid_count:0, illustration_count:0, figure_design_table_missing

## 바꾼 것

- A·B·C 3개 18줄 → A·B 2개 8줄로 줄여 규칙을 읽기 쉽게 함
- 종류가 다른 훅은 before → wrap → after 순서라는 관찰 추가
- PII 순서 주장을 04절 재시도·기록 훅 예로 교체
- Mermaid 3장, 삽화 1장 prompt(두 겹 봉투)

## 검토

- 1차 accept-with-fixes(상 2·중 4·하 2) → 2차 accept(하 4, 반영 완료)
- 리뷰 묶음: `qa/upgrade/review-pack/`

## 남은 것

- 삽화: 2026-09-15 생성·검수 통과, 본문 「비유로 시작하기」 아래에 넣음(노트북에는 넣지 않음)
- 강사 확인
