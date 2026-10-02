# 02-PII-마스킹-이식 — 품질 개선 진단과 결과

작성 2026-09-15. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 7 | 0 |
| G2 | 4 | 0 |
| G3 | 6 | 0 |
| G4 | 1 | 0 |
| G5 | 7 | 0 |
| G6 | 25 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 16 |
| 검사한 문장 | 82 | 160 |

## 수정 전 주요 문제

- G1: varargs_def 2, list_comprehension 2, class_def 1, conditional_expression 1, generator_expression 1
- G2: over_15_lines 2, one_line_compound 1, semicolon 1
- G3: boilerplate_comment 6
- G4: fake_model 1
- G5: result_reading_quotes_no_output 4, title_cell_missing 1, core_figure_attachment_missing 1, result_reading_after_missing 1
- G6: english_start 16, long 9
  - 예: Ch16 guardrails.py의 mask_pii는 email, phone, rrn, card 정규식을 순서대로 적용하고 종류별 개수를 반환했습니다
  - 예: PIIMiddleware의 pii_type은 찾을 유형, strategy는 block·redact·mask·hash 중 처리 방법입니다
  - 예: apply_to_input은 사용자가 보낸 메시지, apply_to_output은 모델 답변, apply_to_tool_results는 도구 결과에 적용합니다
- G7: mermaid_count:0, illustration_count:0, figure_design_table_missing

## 바꾼 것

- Ch16 마스킹 함수 재실행 → Before(기록 훅만) → After(PIIMiddleware email) 구성
- 모델이 받은 글을 기록하는 감싸기형 훅으로 비교 기준을 고정
- 전화번호는 detector 인자로 두 번째 미들웨어를 만들어 확인
- Mermaid 3장, 삽화 1장 prompt(우편 가림막)

## 검토

- 1차 accept-with-fixes(상 1·중 4·하 4) → 2차 accept(하 2, 반영 완료)
- 리뷰 묶음: `qa/upgrade/review-pack/`

## 남은 것

- 삽화: 2026-09-15 생성·검수 통과, 본문 「비유로 시작하기」 아래에 넣음(노트북에는 넣지 않음)
- 강사 확인
