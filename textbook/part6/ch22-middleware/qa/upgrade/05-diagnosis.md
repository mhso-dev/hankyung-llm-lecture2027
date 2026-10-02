# 05-커스텀-예산-미들웨어 — 품질 개선 진단과 결과

작성 2026-09-15. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 6 | 0 |
| G2 | 6 | 0 |
| G3 | 6 | 0 |
| G4 | 1 | 0 |
| G5 | 5 | 0 |
| G6 | 20 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 13 |
| 검사한 문장 | 77 | 140 |

## 수정 전 주요 문제

- G1: class_def 3, varargs_def 2, conditional_expression 1
- G2: one_line_compound 3, semicolon 2, over_15_lines 1
- G3: boilerplate_comment 6
- G4: fake_model 1
- G5: result_reading_quotes_no_output 2, title_cell_missing 1, core_figure_attachment_missing 1, result_reading_after_missing 1
- G6: long 13, english_start 7
  - 예: 내장 ModelCallLimitMiddleware는 호출 횟수를 제한하지만 프로젝트가 사용하는 가격표와 예상 토큰으로 비용 상한을 계산하지는 않습니다
  - 예: 에이전트마다 같은 reserve 호출을 넣는 대신 커스텀 미들웨어 하나로 모델 호출 경계를 감싸면 정책 코드를 재사용하고 독립적으로 검사할 수 있습니다
  - 예: Ch16 CallBudget은 max_calls, max_cost_usd, calls, cost_usd를 보관하고 reserve에서 다음 호출이 한도를 넘는지 검사했습니다
- G7: mermaid_count:0, illustration_count:0, figure_design_table_missing

## 바꾼 것

- 예산 단위를 달러 가정값에서 실제 usage_metadata 토큰으로 변경
- after_model 기록 훅 + wrap_model_call 검사 훅(AIMessage 반환)으로 구성
- 한도 1 → 1000 값 바꿔 보기
- Mermaid 3장, 삽화 1장 prompt(교통카드 개찰구)

## 검토

- 1차 accept-with-fixes(중 3·하 4) → 2차 accept(하 1, 반영 완료)
- 리뷰 묶음: `qa/upgrade/review-pack/`

## 남은 것

- 삽화: 2026-09-15 생성·검수 통과, 본문 「비유로 시작하기」 아래에 넣음(노트북에는 넣지 않음)
- 강사 확인
