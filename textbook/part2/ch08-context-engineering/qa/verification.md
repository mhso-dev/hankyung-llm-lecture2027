# Ch 08 컨텍스트 엔지니어링 — 품질 개선 검증 기록

개선 전 검증 기록은 챕터 폴더의 `verification.md`·`notebook-verification.md`와 `qa/part2-verification.md`에 있습니다. 이 파일은 품질 개선(규격 `textbook/QUALITY-UPGRADE.md`) 뒤 챕터 마감 검증입니다.

## §2-7 리팩터 (2026-09-21)

- 대상: 02~07(앞 절·Ch 7 08 함수를 다시 적고 있었음). 01은 처음 가르친 절이라 그대로. 도구 파일 `labs/part2/ch08-context-engineering/notebooks/llm_tools.py`(함수 9개, 코드 57줄, SHA-256 `c4f8cd5f73aa…daa75`), 리팩터 직전 스냅숏 `qa/upgrade/before-2-7/`.
- 코드 셀 183 → 161, 코드 줄 1335 → 1186(−149, −11.2%, `count_code.py`). 도구 파일을 더해도 1243.
- 새 커널 2번(A 04:58~05:02, B 교재 출력, 2026-09-21 UTC): 요청 없는 셀·입력 토큰 수는 A·B·리팩터 전 모두 같음. 모델 답 셀만 달랐고(03·04·05·06·07), 교재 인용은 B, 결론에 닿은 A 값은 「교재 출력 바로 앞의 새 커널 실행」으로 적음. 리팩터 전과 달라진 결론 자리: 02·04 Before 출처 표시, 05 세 답 글자, 06 비용 순서, 07 실행 1 빠진 지킬 말(handoff 표). §2-7 10항 입력 수정 없음.
- 테스트: `tests/test_ch06_ch08_continuity.py` `load_function()`이 노트북의 `from llm_tools import`를 확인한 뒤 도구 파일 정의를 읽도록 고침(확인 성질 같음). 20 passed · 1 failed → **21 passed**.
- runs: `runs/context-design-continuity.json` `125fc147e81fb8b6234ff87045120a30f9fdccd6bae52fc0dc8d7c68670e58ad` → `043750eeffb6dc15f56b915da51e87dd69e51adcfd266dbdbd246abb0a66a5d2`(run_id `ch08-context-20260921T050226`, 출처 Ch 7 `434640f4…a561`), 사본 `runs/continuity/20260921T050226/`. 옛 사본·A 사본은 `qa/upgrade/before-2-7/runs/moved/`(삭제 아님). `ex0*.jsonl`·`data/memory.json` 같음. Ch 6 → 7 → 8 사슬 통과(테스트·`check_course_continuity.py` 66~76행).
- 게이트 `upgrade_gates.py --label after-2-7` 7/7 PASS(G1~G7 0, `qa/upgrade/gates-after-2-7.json`). `verify.py --chapter` `PASS 7 sections / 161 code cells (max 17 lines)`. 빌드 HTML `{{` 0건. `visual.cjs` 02~07 × 1280·390px 12건 PASS(사본 `/tmp/ch08-27/vis.cjs`). 다시 렌더한 그림 02-4·04-3·05-3·06-2·07-2·07-3(폭 683~830).
- 묶음: `part2-practice.zip` 다시 만듦(`Part 2: 23 verified sections; 37 bundled files`), 풀어서 07 새 커널 19셀 오류 0. `textbook/part2/qa/check_delivery.py` 90행에서 멈춤(20노트북·180셀 기대값, 지금 23·470 — 전체 마감).
- 서비스 요청 53번(A 24 + B 24 + 묶음 5), 약 0.05달러.

## 2026-09-17 챕터 마감 (검토 1차 A·B 반영 뒤)

환경: Cowork 기기 셸 Linux aarch64, Python 3.12.13, 가상환경 `$ROOT/.cache/vm/venv-ch08-context-engineering`(langchain 1.4.0·langchain-core 1.6.2·langchain-openai 1.6.0·openai 3.8.0·tiktoken 0.14.0), 새 커널 `nbclient==0.11.0`·`ipykernel==7.3.0`.

| 검사 | 명령 | 결과 |
|---|---|---|
| 게이트 G1~G7 | `python3 textbook/_notebook/checks/upgrade_gates.py textbook/part2/ch08-context-engineering --label after --strict` | **7/7 PASS, 모두 0**(`qa/upgrade/gates-after.json`). 수정 전 `gates-before.json` 274건(G1 4·G2 6·G3 2·G4 6·G5 80·G6 159·G7 17). 코드 셀 22·23·26·29·27·31·25 = 183, 검사 문장 409·408·412·452·465·513·465 |
| 노트북·본문 계약 | `uv run --project labs/part2/ch08-context-engineering python textbook/_notebook/verify.py --chapter textbook/part2/ch08-context-engineering`(`chapter.json` 없음 — `run_section.sh`가 건너뛰므로 따로) | `PASS 7 sections / 183 code cells (max 17 lines)` |
| 새 커널 실행 | `bash textbook/_notebook/upgrade/run_section.sh textbook/part2/ch08-context-engineering 07` | 07만 `PASS 07-컨텍스트-엔지니어링-실습.ipynb: 25 cells`(2026-09-17T13:54:27, 요청 5번). 01~06은 재실행하지 않음 — 코드·출력·`verification` 해시 반영 전후 같음(01 `b115cde5/b790d25d`, 02 `8985cc77/d3643c52`, 03 `f2edf316/08696210`, 04 `b067099b/017eafb9`, 05 `5f2ad27e/b3aac7ca`, 06 `6dd95a1f/d72096cd`), 07 `e17ebf63/e8119816` |
| 빌드 | `(cd textbook/part2/ch08-context-engineering && uv run --project … --with pillow python _build.py)` | HTML 8개, 남은 `{{` 0건(잔존 검사 `\{\{[a-z]+:`로 넓힘 — 멈춤 없음) |
| 화면 | `/tmp/ch08-close/vis/vis.cjs`(공용 `textbook/_notebook/visual.cjs`와 `require` 경로만 다른 사본) + HTML 사본 폴더, `LD_LIBRARY_PATH=/tmp/libs/…` | 7절 + 목차 × 1280·390px **16/16 passed**(작은 글자·대비·잘림·SVG 경계·가로 스크롤·깨진 이미지 0) |
| Mermaid | `render_mermaid.py`(run_section 안) | 다시 렌더 01-1·07-1·07-2·07-3(mmd 수정으로 도장 해시 변경, 도장 삭제 없음), 나머지 skip. PNG 직접 확인. viewBox 폭 01-1 599·07-1 370·07-2 787·07-3 767(≤ 868) |
| 실습 폴더 테스트 | `PYTHONDONTWRITEBYTECODE=1 … uv run --project labs/part2/ch08-context-engineering --with pytest python -m pytest -q -p no:cacheprovider --basetemp=/tmp/ch08-close/pt labs/part2/ch08-context-engineering/tests`(먼저 `tests/`가 `tmp_path`에만 쓰는 것을 확인) | **21 passed**, 실행 전후 `runs/`·`data/`·`tests/` 목록·수정 시각 같음 |
| runs 사슬 | `sha256sum`(반영 전·07 재실행 전·마감 뒤 세 번) | 모두 같음: Ch 8 `context-design-continuity.json`·사본 `continuity/20260917T121654/` `125fc147…58ad`, `ex01_budget.jsonl` `e3b6a71d…`, `ex04_failures.jsonl` `d23dbb45…`, `ex05_rot.jsonl` `6a9db927…`, `ex06_compare.jsonl` `5cb060d6…`, `data/memory.json` `0aa9fae5…`, Ch 7 `prompt-ab-continuity.json` `a8aaafb7…95e9`·`prompt-ab-v1.json` `16a4b672…4341`, Ch 6 `provider-comparison-continuity.json` `f18920c6…4f4c` |
| review-pack | `python3 textbook/_notebook/upgrade/pack.py textbook/part2/ch08-context-engineering NN`(01~07) | 7개 다시 만듦, 반영 전 묶음 `qa/upgrade/before/review-round1/review-pack/` |
| 옛 생성기 | `mv -n labs/part2/ch08-context-engineering/_make_notebooks.py qa/upgrade/before/generators/` | 옮긴 뒤 빌드·verify·테스트 결과 같음, 코드·검사 스크립트 참조 없음 |

실행하지 않은 것: `textbook/qa/check_course_continuity.py`(runs 해시가 검토 B 실행 때와 같음 — 212행 `part1-practice.zip` 신선도에서 멈추는 상태, 전체 마감 때 zip 재생성 뒤 끝까지), 다운로드 zip·Part 2 목차 재생성(전체 마감), Windows·macOS.
