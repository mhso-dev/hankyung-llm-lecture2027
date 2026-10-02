# 04-호출-한도와-재시도-폴백 — 품질 개선 진단과 결과

작성 2026-09-15. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 6 | 0 |
| G2 | 3 | 0 |
| G3 | 7 | 0 |
| G4 | 1 | 0 |
| G5 | 7 | 0 |
| G6 | 21 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 14 |
| 검사한 문장 | 84 | 163 |

## 수정 전 주요 문제

- G1: varargs_def 3, class_def 2, conditional_expression 1
- G2: one_line_compound 2, over_15_lines 1
- G3: boilerplate_comment 7
- G4: fake_model 1
- G5: result_reading_quotes_no_output 4, title_cell_missing 1, core_figure_attachment_missing 1, result_reading_after_missing 1
- G6: english_start 12, long 8, dense_paragraph 1
  - 예: Ch16의 CallBudget과 retry_with_fallback은 호출자가 매번 reserve와 재시도 함수를 직접 사용했습니다
  - 예: 이 절에서는 같은 역할을 ModelCallLimitMiddleware, ModelRetryMiddleware, ModelFallbackMiddleware의 설정과 실행 trace로 확인합니다
  - 예: ModelCallLimitMiddleware의 run_limit는 현재 invoke, thread_limit는 같은 스레드에 누적된 호출을 제한합니다
- G7: mermaid_count:0, illustration_count:0, figure_design_table_missing

## 바꾼 것

- 실패를 실제 조건으로 재현: timeout 0.001초(재시도 3번), 없는 모델 이름(폴백), run_limit 1(호출 한도)
- 시도 기록 훅으로 세 실험을 같은 방식으로 셈
- 대기 시간 0.5초·1초는 설정값이며 재지 않았다고 명시
- Mermaid 4장, 삽화 1장 prompt(전화 연결)

## 검토

- 1차 accept-with-fixes(중 5·하 5) → 2차 accept(새 문제 없음)
- 리뷰 묶음: `qa/upgrade/review-pack/`

## 남은 것

- 삽화: 2026-09-15 생성·검수 통과, 본문 「비유로 시작하기」 아래에 넣음(노트북에는 넣지 않음)
- 강사 확인
