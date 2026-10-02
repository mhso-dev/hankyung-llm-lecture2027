# Ch 7 verification — 품질 개선본

개선 전(2026-09-09) 검증 기록은 챕터 `집필점검표.md` 위쪽 표와 체크 목록에 있습니다. 이 파일은 품질 개선(규격 `textbook/QUALITY-UPGRADE.md`) 뒤 기록입니다.

## 품질 개선 01~09와 챕터 마감 (2026-09-17)

- 새 커널 실행 PASS: 노트북 9개, 코드 셀 200개(19·19·22·24·18·22·24·27·25), Linux aarch64, Python 3.12.13, langchain 1.4.0·langchain-core 1.6.2·langchain-openai 1.6.0·openai 3.10.0·pydantic 2.13.5·python-dotenv 1.2.3, 실행 도구 nbclient 0.11.0·ipykernel 7.3.0. 실행일 모두 2026-09-17. 절별 실행 기록은 `qa/upgrade/NN-diagnosis.md`.
- 서비스 요청(노트북 기준): 01 4번, 02 3번, 03 4번, 04 4번, 05 3번, 06 6번, 07 4번, 08 6번, 09 4번. OpenAI `gpt-5.4-mini`만(temperature 0, reasoning_effort none). 비용 문장은 Ch 6 06절에서 2026-09-17에 확인한 mini 요금 기준.
- 검토 1차 반영(마감 세션): 설명·그림 라벨·기록만 고쳐 노트북을 다시 실행하지 않음. 코드 셀·출력·`verification` 메타데이터 해시를 반영 전후 비교해 9개 모두 같음(08 `14593bfd5ee03ad2`, `executed_at` `2026-09-17T07:07:04`). review-pack 9개를 다시 만들어 반영 전 묶음과 `diff`, 바뀐 줄은 설명·meta·그림 라벨·caption뿐.
- runs 파일 SHA-256(반영 전후 같음): `labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json`·`runs/continuity/20260917T070701/prompt-ab-continuity.json` `a8aaafb775e710438a1bd9e5d79340d3032f61be30c4dbb2e8aa4dd7b82095e9`, `runs/prompt-ab-v1.json` `16a4b67210853c925e75ced02cc88fa704957aa196a2572a05f8fce49fbf4341`, `labs/part2/ch06-langchain-start/runs/provider-comparison-continuity.json` `f18920c63088bded645bc4712b8ee16436e46d394499bfeaa4cc081f76ef4f4c`.
- `verify.py --chapter` `PASS 9 sections / 200 code cells (max 15 lines)`. 품질 게이트 `upgrade_gates.py --label after --strict` 9/9 PASS, G1~G7 0(`qa/upgrade/gates-after.json`, 수정 전 `gates-before.json` 272건).
- `visual.cjs` 9절 + 챕터 목차 × 1280·390px 20건 PASS(작은 글자·대비·잘림·SVG 경계·가로 넘침·깨진 이미지·복사 오류 0). 공용 도구를 고치지 않고 `/tmp/ch07-close/vis/vis.cjs` 사본으로 실행.
- 뒤 챕터 연결 검사(알려진 실패, 해소 순서는 `qa/upgrade/chapter-summary.md` §9): Ch 8 `tests/test_ch06_ch08_continuity.py` 3 passed·2 failed(`test_log_paths_are_portable…`, `test_continuity_logs_form_a_hash_verified_chain` 103행 ch08 출처), `textbook/qa/check_course_continuity.py` 73행 ch08 `source_record.sha256` 불일치에서 멈춤(ch07 네 조건은 통과). 옛 생성기·`_src/index-body.html`을 `qa/upgrade/before/`로 옮기기 전후 결과 같음.
- 강사 확인 전. 다운로드 묶음 `textbook/downloads/part2-practice.zip`과 Part 2 목차는 전체 마감 때 다시 만듭니다.

## §2-7 리팩터 (2026-09-21)

- 대상: 01~09 전부(모든 절이 `timed_invoke`·`make_prompt_record`를 다시 적고 있었음). 도구 파일 `labs/part2/ch07-prompt-engineering/notebooks/llm_tools.py`(함수 6개, 코드 52줄, SHA-256 `0b82eb0f22e9…29e8`), 리팩터 직전 스냅숏 `qa/upgrade/before-2-7/`.
- 새 커널 실행: 절마다 `run_section.sh` 두 번(A 03:46~03:48, B 03:48~03:49 UTC), 코드 셀을 소스로 짝지어 출력 대조 → 모델을 부른 셀(답·출력 토큰·걸린 초)만 다르고 입력 토큰 수·요청 없는 셀은 같음. 리팩터 전 노트북과도 같은 결과. 교재 인용은 B 값, 달랐던 A 값은 「앞선 새 커널 실행」으로 적음. 실행일 모두 2026-09-21, 코드 셀 179개(18·17·20·22·16·20·22·25·19).
- 서비스 요청: A 38 + B 38 + 묶음 확인 4 = 80번, `gpt-5.4-mini`만(temperature 0, reasoning_effort none), 약 0.05달러 미만.
- runs 파일 SHA-256: `runs/prompt-ab-continuity.json` `a8aaafb775e710438a1bd9e5d79340d3032f61be30c4dbb2e8aa4dd7b82095e9` → `434640f485d47bd936685b286f654d78249fb8a41e0a64e54b48cc64fb30a561`(run_id `ch07-prompt-ab-20260921T034935`), 같은 바이트 사본 `runs/continuity/20260921T034935/`. 옛 사본과 A 실행 사본은 `qa/upgrade/before-2-7/runs/moved/`로 옮김(삭제 아님). `prompt-ab-v1.json` `16a4b672…4341`, Ch 6 `f18920c6…4f4c` 같음.
- 게이트 `upgrade_gates.py --label after-2-7` 9/9 PASS(G1~G7 0, `qa/upgrade/gates-after-2-7.json`). `verify.py --chapter` `PASS 9 sections / 179 code cells (max 15 lines)`. 빌드 HTML `{{` 1건(04 출력의 LangChain `KeyError` 메시지 속 `{{history}}`, 리팩터 전에도 있음). `visual.cjs` 9절 + 목차 × 1280·390px 20건 PASS(사본 `/tmp/ch07-27/vis.cjs`).
- 다시 렌더한 그림: 절 번호·인용 값이 바뀐 mmd 18장(05-3은 구조 변경, 09-1은 라벨 「버전의 허용 이름」). 모두 폭 868px 미만.
- 뒤 챕터 연결: `check_course_continuity.py` ch07 네 조건 통과, ch08 출처 지문·run_id 불일치. Ch 8 `tests/test_ch06_ch08_continuity.py` 20 passed · 1 failed(`test_continuity_logs_form_a_hash_verified_chain` 127행, 리팩터 전 21 passed) — Ch 8 06 새 커널 실행 뒤 풀림. Ch 8 노트북은 다시 실행하지 않음.
- 묶음: `part2-practice.zip` 다시 만듦(23절·36파일, `llm_tools.py` 포함, SHA-256 `d159d74e…3436`, 04 질문 바꿈 뒤 `d2bd54ef…d58e`). 풀어서 `notebooks` 폴더를 작업 폴더로 09 새 커널 실행 → 19셀 오류 0. `textbook/part2/qa/check_delivery.py`는 90행(20노트북·180셀 기대값)에서 멈춤 — 전체 마감 몫.

- **04 다음 질문 바꿈(§2-7 10항)**: 옛 질문으로는 기록 있음 답의 A-1042가 두 실행에서 갈려, 기록이 있어야 답할 수 있는 질문과 셋째 기록 메시지(고객 대답)로 바꿈. 새 커널 두 번 모두 기록 없음 False·기록 있음 True·최근 메시지 하나 False(모델 답 `assert` 없음). 04 `outputs_sha256` `577f45be`, 요청 8번. 게이트 9/9·verify PASS·`{{` 1건(오류 메시지 속)·visual 04·05 두 폭 PASS. runs `434640f4…a561` 그대로.
