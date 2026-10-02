# 06-커스텀-감사-미들웨어 — 품질 개선 진단과 결과

작성 2026-09-15. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 7 | 0 |
| G2 | 6 | 0 |
| G3 | 6 | 0 |
| G4 | 1 | 0 |
| G5 | 6 | 0 |
| G6 | 16 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 13 |
| 검사한 문장 | 80 | 135 |

## 수정 전 주요 문제

- G1: class_def 2, varargs_def 2, list_comprehension 2, conditional_expression 1
- G2: over_15_lines 2, one_line_compound 2, one_letter_name:e 2
- G3: boilerplate_comment 6
- G4: fake_model 1
- G5: result_reading_quotes_no_output 3, title_cell_missing 1, core_figure_attachment_missing 1, result_reading_after_missing 1
- G6: long 8, english_start 8
  - 예: Ch16의 AuditLogger는 질문을 마스킹하고 소금값을 더한 해시, 이벤트 이름, 안전한 상세 정보만 JSONL에 기록했습니다
  - 예: Ch16 AuditLogger.record는 query_masked와 query_hash를 만들고 중첩된 문자열에도 mask_pii를 적용했습니다
  - 예: AuditMiddleware의 before_agent는 실행 시작, wrap_tool_call은 도구 이름과 성공·오류, after_agent는 종료를 기록합니다
- G7: mermaid_count:0, illustration_count:0, figure_design_table_missing

## 바꾼 것

- 원문 대신 글자 수와 지문(sha256 앞 10자) 기록
- 감사 훅 3개(before_agent, wrap_tool_call, after_agent)를 셀별로 분리
- 같은 글 지문 일치·글자 수 같은 두 글 지문 차이 출력
- Mermaid 3장, 삽화 1장 prompt(방문자 명부)

## 검토

- 1차 accept-with-fixes(중 3·하 6) → 2차 accept(하 1, 반영 완료)
- 리뷰 묶음: `qa/upgrade/review-pack/`

## 남은 것

- 삽화: 2026-09-15 생성·검수 통과, 본문 「비유로 시작하기」 아래에 넣음(노트북에는 넣지 않음)
- 강사 확인
