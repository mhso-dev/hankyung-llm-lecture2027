# 01-미들웨어와-6개-훅 — 품질 개선 진단과 결과

작성 2026-09-15. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 7 | 0 |
| G2 | 11 | 0 |
| G3 | 6 | 0 |
| G4 | 2 | 0 |
| G5 | 5 | 0 |
| G6 | 17 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 20 |
| 검사한 문장 | 81 | 204 |

## 수정 전 주요 문제

- G1: class_def 2, varargs_def 2, conditional_expression 2, generator_expression 1
- G2: one_line_compound 6, semicolon 3, over_15_lines 2
- G3: boilerplate_comment 6
- G4: temperature_missing 1, fake_model 1
- G5: result_reading_quotes_no_output 2, title_cell_missing 1, core_figure_attachment_missing 1, result_reading_after_missing 1
- G6: long 12, english_start 5
  - 예: Ch20에서는 모델 노드와 ToolNode를 직접 연결했고 Ch21에서는 create_agent가 같은 반복을 컴파일된 그래프로 만든다는 사실을 확인했습니다
  - 예: Ch16의 guardrails.py는 모델 호출 전후에 validate_query, mask_pii, CallBudget, retry_with_fallback을 직접 호출했습니다
  - 예: 미들웨어도 에이전트 전체에는 before_agent와 after_agent, 각 모델 호출에는 before_model·wrap_model_call·after_model, 각 도구 호출에는 wrap_tool_call을 제공합니다
- G7: mermaid_count:0, illustration_count:0, figure_design_table_missing

## 바꾼 것

- 가짜 모델(ScriptedModel) 클래스를 없애고 gpt-5.4-mini를 temperature 0으로 호출
- 훅 6개를 셀 하나에 하나씩 데코레이터 함수로 분리
- ai 메시지 수와 훅 기록 수를 따로 세어 assert로 대조
- Mermaid 4장(훅 위치, 실제 실행 순서, 질문별 횟수, 훅 세 범위), 삽화 1장 prompt(공항 검사 지점)

## 검토

- 1차 accept-with-fixes(중 4·하 5) → 2차 accept-with-fixes(중 1·하 1, 반영 완료)
- 리뷰 묶음: `qa/upgrade/review-pack/`

## 남은 것

- 삽화: 2026-09-15 생성·검수 통과, 본문 「비유로 시작하기」 아래에 넣음(노트북에는 넣지 않음)
- 강사 확인
