
## 10. 전체 마감 (2026-09-30~10-01)

근거는 `textbook/qa/final-close-log.md` 1~6단계입니다. 사용자 결정: **제목·슬러그 그대로**, **옛 검사 스크립트는 지금 구조에 맞게 고침**, **삭제 승인 목록은 마감 끝에 지움**(보존 대상과 다음 작업에 필요한 것은 뺌). 노트북 재실행 0, 삽화 생성 0, 모델 요청은 5단계 Part 3 연속성 묶음 한 번(코드 기준 37 — 임베딩 36·`gpt-5.4-mini` 1, 약 $0.03)뿐입니다.

**한 일**
1. 옛 생성기 18개를 막은 뒤 각 챕터 `qa/upgrade/before/generators/blocked/`로 옮김(삭제 아님), `.moai` 보조 스크립트 9개 막음, Ch 6 04~06·Ch 25 02 「스트림 청크」 표기(마크다운만).
2. 도구 파일 여섯(Ch 24·25·26·27·29·30)의 머리 설명만 고침(함수 본문·가져오는 이름·노트북 해시 같음), 생성기 대조 사슬의 고정 해시를 함께 맞춤.
3. 옛 검사 스크립트 15개를 지금 구조에 맞게 고침(목록·전후 해시는 `upgrade-contracts.md` §5).
4. 목차는 이미 스크립트 출력과 같아 `build_index.py` 설명만 고침, 묶음 여섯(ch01·ch02·llm·Part 2·6·7) 다시 만듦, Part 5·6 `check_delivery.py`의 `queries.jsonl` 금지 줄을 Part 3·4 규칙에 맞춤, Part 7 기준 파일 `existing-artifacts-final-close.json`을 한 번 만듦.
5. 묶음 실행 검사(Part 6·Part 7 `--pre-exec`·Part 3 연속성) 통과, 화면 26폴더 164쪽 328행 다시 찍음(322 PASS), `check_continuity.py`·`check_course_continuity.py`·`check_visual_reports.py`·`check_figures.py` 넷 통과.
6. Ch 12 화면을 다시 찍음(같은 6행 실패 — 아래 남은 결정), 검토 묶음 236절 다시 만듦, 누적 문서·진행표·최종 점검표 정리, 최종 게이트 236/236 확인, 삭제 목록 `textbook/qa/deletion-manifest-2026-10-01.tsv`·`.md` 작성.

**고친 검사 스크립트와 그 원칙**
- 옛 구조(절 수·노트북 수·화면 행 수 고정값, `.excalidraw` 짝, `figures/_gen_figures.py` 요구, Ch 31 macOS `.venv` 러너, 옛 `existing-artifacts-before.json`)를 가리키는 곳만 지금 구조로 바꾸고 **검사 항목과 기준은 그대로 둡니다 — 기대값을 낮추지 않습니다.** 고정 숫자는 숫자를 바꾸는 대신 실제 구조(`chapter.json` 절 목록, 폴더별 공개 HTML 쪽 × 두 너비)에서 세도록 했습니다. 예: `finalize_continuity_evidence.py`의 94(실습 쪽이 빠진 채 맞아떨어진 값) → 폴더별 합 98, 주석에 「98을 94·96 등으로 내리지 마세요」.
- **내용 때문에 멈추는 검사는 고치지 않습니다**(함수 타입힌트·`assert`·복습 문항 수 — 사람 결정). 기준이 사람 승인인 검사(Part 4 `check_language_freeze.py`·Part 5 `finalize_evidence.py`, 2026-09-10 언어 감사 해시)도 그대로입니다.
- 환경 때문에 스크립트 그대로 돌릴 수 없을 때(연결 폴더 삭제 막힘)는 스크립트를 고치지 않고 `.cache/final-close/` 안의 감싸개·사본으로 돌렸고, 사본 결과는 「사본 결과」라고 따로 적었습니다.
- 고친 파일마다 설명 맨 위에 「전체 마감 2026-10-01: …」 한 단락, 원본 사본과 전후 해시는 `.cache/final-close/<단계>/`(`log/`는 삭제 목록에서 뺌), 고친 파일 목록은 `upgrade-contracts.md` §5입니다.

**새 값**(§2-15~2-21의 옛 해시는 고치지 않음 — 지금 값은 이 줄)
- 도구 파일 머리 줄 뒤 해시: Ch 24 `approval_tools.py` `d562c9e6…` → `295bfaf6…` · Ch 25 `stream_tools.py` `3a734aeb…` → `6df804b8…` · Ch 26 `delegation_tools.py` `c3c1709a…` → `0748a8eb…` · Ch 27 `harness_tools.py` `7a40d994…` → `ed5c4240…` · Ch 29 `eval_tools.py` `d624b8f3…` → `b75636c4…` · Ch 30 `serve_tools.py` `2f66bc6b…` → `333e9a62…`. Ch 28 `connect_tools.py` `570ed3cc…` 그대로. 전체 해시는 `upgrade-contracts.md` §4.
- 묶음 zip 열 개·`bundle-execution.json` Part 6·7·Part 7 기준 파일·Part 3 연속성 결과: `upgrade-contracts.md` §5 「전체 마감」 줄.
- 게이트(2026-10-01, `check_section()` 직접 호출·파일 쓰기 없음): 32챕터 236절 PASS, G1~G7 합 0, 코드 셀 5,282, 검사 문장 88,782(Ch 6 +1 — 「스트림 청크」 설명 한 문장). 노트북 236개 `code_sha256`·`outputs_sha256`·`code_cells`가 메타데이터와 모두 같음.

**남은 사람 결정**(목록은 `upgrade-final-checklist.md` 맨 위 「전체 마감 결과」 절): 과정 전체 결정 가운데 남은 것(코드 양·잠금 정리·`openai` 판·묶음 실행 후보·「예상 비용」·규격 반영·옛 기록 해시·`.moai` 처리·삽화·2차 검토·제외 챕터 문장·계정 Batch 파일 등)과 마감 중에 새로 찾은 것 — Part 5·6 노트북 함수 타입힌트, Ch 29 01 `assert` 0, Ch 2 01~12 복습 6문항, Ch 12 화면 라벨 0.552px, 2026-09-10 언어 감사 기준 두 스크립트, `build_index.py` Ch 13 설명의 과정 금지어.
