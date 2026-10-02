# 08-컨텍스트-분리와-Isolate — 품질 개선 진단과 결과

작성 2026-09-15. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 8 | 0 |
| G2 | 5 | 0 |
| G3 | 6 | 0 |
| G4 | 1 | 0 |
| G5 | 7 | 0 |
| G6 | 20 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 13 |
| 검사한 문장 | 78 | 132 |

## 수정 전 주요 문제

- G1: class_def 2, varargs_def 2, list_comprehension 2, generator_expression 2
- G2: one_line_compound 3, one_letter_name:m 2
- G3: boilerplate_comment 6
- G4: fake_model 1
- G5: result_reading_quotes_no_output 4, title_cell_missing 1, core_figure_attachment_missing 1, result_reading_after_missing 1
- G6: english_start 12, long 8
  - 예: create_agent 상태에는 여러 업무의 대화가 누적될 수 있고, 전체 상태를 그대로 모델에 전달하면 관련 없는 자료가 입력을 차지합니다
  - 예: Ch8 context_lab.py의 assemble_isolated_messages는 업무별 자료를 별도 필드로 조립했고 텍스트 태그는 보안 격리가 아니라고 설명했습니다
  - 예: IsolateMiddleware는 각 메시지의 additional_kwargs에 있는 topic을 읽어 현재 topic과 같은 메시지만 새 요청에 넣습니다
- G7: mermaid_count:0, illustration_count:0, figure_design_table_missing

## 바꾼 것

- topic 이름표로 loan 3개·hr 2개 분리, 요청만 바꾸고 기록은 지우지 않음을 출력으로 확인
- 새 답에 이름표가 없다는 출력(None)을 주의점으로 연결
- current_topic을 hr로 바꿔 입력 2개 확인
- Mermaid 3장, 삽화 1장 prompt(서류함)

## 검토

- 1차 accept-with-fixes(중 3·하 4) → 2차 accept(하 1, 반영 완료)
- 리뷰 묶음: `qa/upgrade/review-pack/`

## 남은 것

- 삽화: 2026-09-15 생성·검수 통과, 본문 「비유로 시작하기」 아래에 넣음(노트북에는 넣지 않음)
- 강사 확인
