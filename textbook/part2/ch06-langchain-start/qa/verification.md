# Ch 6 verification — 품질 개선본

개선 전(2026-09-09) 검증은 챕터 루트 `verification.md`에 있습니다. 이 파일은 품질 개선(규격 `textbook/QUALITY-UPGRADE.md`) 뒤 기록입니다.

## 품질 개선 01~07과 챕터 마감 (2026-09-16~17)

- 새 커널 실행 PASS: 노트북 7개, 코드 셀 130개(15·18·19·19·19·21·19), Linux aarch64, Python 3.12.13, langchain 1.4.0·langchain-core 1.6.2·langchain-openai 1.6.0·openai 3.10.0·tenacity 9.1.4·langchain-anthropic 1.7.1·langchain-google-genai 4.4.0·pydantic 2.13.5·python-dotenv 1.2.3. 실행일 01 2026-09-16, 02~07 2026-09-17. 절별 실행 기록은 `qa/upgrade/NN-diagnosis.md`.
- 서비스 요청(노트북 기준): 01 4번, 02 4번(답 3), 03 6번, 04 4번, 05 시도 13번(답 2·404 2·시간 초과 9), 06 9번, 07 답 4번 + 시간 초과 시도 2번. OpenAI `gpt-5.4-mini`·`gpt-5.4-nano`만, Anthropic·Google 요청 0번. 요금은 2026-09-17 OpenAI 모델 페이지 기준.
- 검토 1차 반영(마감 세션, 2026-09-17): 설명·그림·기록만 고쳐 노트북을 다시 실행하지 않음. 코드 셀·출력은 반영 전 review-pack과 `diff`해 같음. `labs/part2/ch06-langchain-start/runs/provider-comparison-continuity.json` SHA-256 `f18920c63088bded645bc4712b8ee16436e46d394499bfeaa4cc081f76ef4f4c` 유지.
- `verify.py --chapter` `PASS 7 sections / 130 code cells (max 16 lines)`. 품질 게이트 `upgrade_gates.py --label after --strict` 7/7 PASS, G1~G7 0(`qa/upgrade/gates-after.json`, 수정 전 `gates-before.json` 273건).
- `visual.cjs` 7절 + 챕터 목차 × 1280·390px 16건 PASS(작은 글자·대비·잘림·SVG 경계·가로 넘침·깨진 이미지·복사 오류 0). 공용 도구를 고치지 않고 `/tmp/ch06-close/vis/vis.cjs` 사본으로 실행.
- 뒤 챕터 연결 검사(알려진 실패, 해소 순서는 `qa/upgrade/chapter-summary.md` §9): Ch 8 `tests/test_ch06_ch08_continuity.py` 3 passed·2 failed(`test_log_paths_are_portable…`, `test_continuity_logs_form_a_hash_verified_chain`), `textbook/qa/check_course_continuity.py` 73행 `source_record.sha256` 불일치에서 멈춤. 옛 생성기·옛 실행 사본을 `qa/upgrade/before/`로 옮기기 전후 결과 같음.
- 강사 확인 전. 다운로드 묶음 `textbook/downloads/part2-practice.zip`과 Part 2 목차는 전체 마감 때 다시 만듭니다.
