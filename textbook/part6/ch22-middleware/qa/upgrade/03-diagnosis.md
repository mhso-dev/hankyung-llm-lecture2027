# 03-요약-압축과-Compress — 품질 개선 진단과 결과

작성 2026-09-15. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 9 | 0 |
| G2 | 6 | 0 |
| G3 | 7 | 0 |
| G4 | 2 | 0 |
| G5 | 8 | 0 |
| G6 | 12 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 13 |
| 검사한 문장 | 80 | 156 |

## 수정 전 주요 문제

- G1: class_def 3, generator_expression 3, varargs_def 2, conditional_expression 1
- G2: one_line_compound 2, semicolon 2, over_15_lines 1, one_letter_name:m 1
- G3: boilerplate_comment 7
- G4: fake_model 1, temperature_missing 1
- G5: result_reading_quotes_no_output 5, title_cell_missing 1, core_figure_attachment_missing 1, result_reading_after_missing 1
- G6: english_start 7, long 5
  - 예: Ch16 summarize_history는 system 메시지와 최근 대화를 남기고, 오래된 대화를 summarizer 함수에 넘긴 뒤 참고용 요약 메시지로 바꿨습니다
  - 예: 여섯 메시지를 Before 에이전트에 그대로 전달한 뒤, trigger=4·keep=2 조건의 SummarizationMiddleware를 붙입니다
  - 예: 결정적 요약문으로 메시지 구성 변화를 재현하고, 별도 실제 모델 호출로 권수·기간·연장 조건·출처를 보존한 요약문과 사용량을 확인합니다
- G7: mermaid_count:0, illustration_count:0, figure_design_table_missing

## 바꾼 것

- 실제 요약 모델 호출로 trigger 4·keep 2 실행, 입력 6개 → 3개
- 요약 전후 글자 수(130 → 381)와 저장 기록 구성 출력 셀 추가
- trigger 경계를 「이상이면」으로 정정(소스 확인)
- Mermaid 3장, 삽화 1장 prompt(메모 정리)

## 검토

- 1차 accept-with-fixes(상 2·중 4·하 5) → 2차 accept-with-fixes(중 1·하 2, 반영 완료)
- 리뷰 묶음: `qa/upgrade/review-pack/`

## 남은 것

- 삽화: 2026-09-15 생성·검수 통과, 본문 「비유로 시작하기」 아래에 넣음(노트북에는 넣지 않음)
- 강사 확인
