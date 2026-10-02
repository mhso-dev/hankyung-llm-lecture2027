# Ch 9 보완 검증 기록

확인일: 2026-09-08. 대상: 개념 6절과 목차, 기존 도식 5개와 삽화 3개, 실습 원본 연결 및 산문 검토. 강의 6h·실습 10h의 학습 범위를 유지합니다.

## 변경 범위

본문·표·설명 글자를 16px 이상으로 맞추고, 도식은 글자 크기를 유지한 채 내부 영역에서 가로로 이동하도록 했습니다. 목차 원본은 `_src/index.html`로 옮겼습니다. 코드·출력은 실습 원본 및 보존 기록을 빌드할 때 삽입합니다. 원본 백업은 `before/`, 작업 계획은 `improvement-plan.md`에 있습니다.

## 검증

- 기존 실습 테스트: 보완 전 10 passed. 임베딩 API를 사용하는 검색 테스트 1개가 포함되며 생성 모델은 호출하지 않았습니다.
- 로더·청킹 예제: API 없이 재실행한 결과가 기존 교재 출력과 일치했습니다.
- 빌드 회귀 테스트: 3개 통과. 다중 함수 순서, HTML 이스케이프, 누락된 자료의 빌드 실패, 데코레이터 보존을 확인했습니다.
- 최종 화면 검사: 1280px·390px, 14/14 통과. 본문 16px·코드/캡션 14px 이상, 본문 대비 4.5:1 이상(큰 글자 3:1), 숨김 잘림·문서 가로 넘침·본문 영역 밖 텍스트 0건입니다. `visual-results.json` 참조.
- 원본 연결: 코드·출력 30블록, 기존 출력 12블록, manifest 해시 12개 일치. `code-evidence.md` 및 `check_content.py` 참조.
- 학습 구성·분량·질문 수·내부 링크: 7/7 통과. `structure-results.json` 참조.
- 보완 후 최종 테스트: 15 passed, 1 deselected. 앞서 통과한 임베딩 API 검색 테스트는 재호출을 피하기 위해 마지막 실행에서 제외했습니다. 기존 9개 로컬 테스트와 추가한 원본 연결 3개·빌드 추출 3개를 검사했습니다.
- Ruff·Python 문법·셸 구문·화면 검사 코드 구문 통과. 별도 정적 타입 검사는 실행하지 않았습니다.
- 도식: 5/5 통과. 글자 14px 이상, 최소 대비 4.61:1, 상자 4~7개, SVG·Excalidraw 일치, 잘림·의도하지 않은 겹침 없음. `../figures/verification.md` 참조.
- 한국어 검토: 정량 게이트 WARN(문자 변경률 3.00%, 내부 인용 플래그 포함), 독립 Phase 6 정독 accept. `language/README.md`와 `final-reading.md` 참조.

## 실행 기록의 해석

보존된 API 출력은 기존 교재의 2026-09-07~08 실행 사례입니다. 이번 보완에서 생성 API를 다시 실행한 결과로 표시하지 않습니다. 비용은 당시 요금 설정과 토큰 수에 따른 추정값이며 실제 청구액이 아닙니다. 새로 실행한 검색 테스트의 임베딩 비용도 별도 청구 내역을 확인하지 않았습니다.

## 확인 필요 항목

외부 맞춤법 서비스는 `korean-spell-check` 스킬의 상업적 대량 처리 금지에 따라 사용하지 않습니다. 로컬 맞춤법·윤문과 원문 대조를 수행하며, 외부 서비스를 포함한 3단 체인 전체 통과로 표시하지 않습니다.

## 재검증 명령

프로젝트 루트에서 실행합니다. HTML 빌드는 Pillow가 포함된 앱의 Python 환경을 사용합니다.

```bash
/Users/mhso/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 textbook/part3/ch09-rag-first-run/_build.py
uv run --project labs/part3/ch09-rag-first-run python textbook/part3/ch09-rag-first-run/qa/check_content.py
uv run --project labs/part3/ch09-rag-first-run python textbook/part3/ch09-rag-first-run/qa/check_structure.py
uv run --project labs/part3/ch09-rag-first-run pytest -q labs/part3/ch09-rag-first-run/tests textbook/part3/ch09-rag-first-run/qa/test_build.py textbook/part3/ch09-rag-first-run/qa/test_code_evidence.py -k 'not test_search_returns_k_hits_sorted_by_score'
/Users/mhso/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node textbook/part3/ch09-rag-first-run/qa/check_visual.cjs
```

최종 원고 해시는 `final-source-sha256.json`에 저장했습니다. 수정은 `_src/`에서 하고 다시 빌드합니다.

---

## §2-7 리팩터 (2026-09-21)

- 대상: 02~07(앞 절·Ch 8 함수를 다시 적고 있었고, 03절은 Ch 5 02절 코사인 유사도를 반복문으로 다시 계산). 01은 처음 가르친 절이라 그대로. 도구 파일 `labs/part3/ch09-rag-first-run/notebooks/rag_tools.py`(함수 8개, 코드 58줄, SHA-256 `4a85b7202b700165c3ba4d66b3fcb69920c06a233fdf63bc52f819df6df7c684`), 리팩터 직전 스냅숏 `qa/upgrade/before-2-7/`.
- 코드 셀 175 → 145, 코드 줄 1298 → 1081(−217, −16.7%, `count_code.py`). 도구 파일을 더해도 1139.
- 새 커널 2번(A·B, 2026-09-21 05:36~05:53 UTC): 02·05·07은 A·B 글자까지 같음. 03·06은 임베딩 점수 넷째 자리, 04·06은 모델 답의 표시 모양만 다름(검사 출력 같음). 교재 인용은 B, 결론에 닿은 A 값은 「이 페이지 출력 바로 앞의 새 커널 실행」으로 본문에 적음. 실행 뒤 설명은 `mdsync`·`mdpatch.py`로 넣고 다시 실행하지 않음. 리팩터 전과 달라진 결론 자리: 03 점수, 04 Before 표시, 05 Before 새 말 「화요일」, 07 실행 2 출처 표시 기록 수 0(handoff 표). §2-7 10항 입력 수정 없음.
- 테스트: `tests/test_harness.py`·`test_rag.py`는 노트북을 읽지 않음 → 고치지 않음, 10 passed → **10 passed**. Ch 11 `tests/` 8 passed.
- runs: `runs/continuity-ch09-search.jsonl` `294713765a115b567e162aaf37a25467577841965c1075b86553adc4080666d5` → `e0323e897794f569175ca69113b28b460cce8481435690d32651c8494406b40e`(`source_run_id` `20260921T055009-ch09`, 사본 `runs/continuity/20260921T055009-ch09.jsonl`). 옛 사본 9개 그대로, A 실행 사본은 `qa/upgrade/before-2-7/runs/moved/`(삭제 아님). 나머지 runs 파일 같음(`runs-sha256-before/after.txt`). 계약(키 8·`config` 7·k=2·`chunk_id`·순위·쪽·답 글자) 같고 `score` 두 값만 다름. `check_continuity.py`·`check_course_continuity.py`의 ch09 블록 통과(`/tmp` 사본, 결과 파일 쓰기 막음), `evaluate.py`로 ch09 지표 같음 확인.
- 게이트 `upgrade_gates.py --label after-2-7` 7/7 PASS(G1~G7 0, `qa/upgrade/gates-after-2-7.json`). `verify.py --chapter` `PASS 7 sections / 145 code cells (max 16 lines)`. 빌드 HTML `{{` 0건(01·index 바이트 같음). `visual.cjs` 02~07 × 1280·390px 12건 PASS(사본 `/tmp/ch09-27/vis.cjs`). 다시 렌더한 그림 03-1·03-2·03-3·03-4·04-4·05-4·07-3(폭 466~852).
- 묶음: `part3-practice.zip` 다시 만듦(`Part 3: 36 verified sections; 90 bundled files`, `df60a02b…7666`), 풀어서 03 새 커널 15셀 오류 0. `textbook/part3/qa/check_delivery.py` 통과(`delivery-results.json` 다시 씀).
- 서비스 요청 72번(A 33 + B 33 + 묶음 6 — 임베딩 52·mini 20), 약 0.02달러.

## 품질 개선(체인 ⑨) + 실습 절 07 + 검토 1차 반영 — 2026-09-17

위 절들은 2026-09-08 개선 전 기준 검증 기록입니다. 아래는 품질 개선 뒤의 검증 기록입니다. 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`. 상세는 `qa/upgrade/NN-diagnosis.md`·`chapter-summary.md`·`review-round1-A.md`·`review-round1-B.md`.

### 대상과 범위

절 7개(01~06 품질 개선, 07 챕터 끝 실습 절 신설), 목차 본문 `_src/index.html`, 실습 폴더 `README.md`·`config.yaml`(주석 한 줄), Mermaid 27장·삽화 7장, 자체 `_build.py`(`{{mermaid:}}`·세 칸 `{{img:}}` 추가, 잔존 검사 `\{\{[a-z]+:`). 강의 6h·실습 10h는 유지하고 실습 절 30분은 그 안으로 봅니다.

### 검증 결과 (검토 1차 반영 뒤)

- 게이트: `python3 textbook/_notebook/checks/upgrade_gates.py textbook/part3/ch09-rag-first-run --label after --strict` → **7/7 PASS, G1~G7 0건**(`qa/upgrade/gates-after.json`). 수정 전 `gates-before.json`은 6절 합계 268건(G1 12·G2 6·G3 10·G4 2·G5 72·G6 151·G7 15).
- 노트북: 일곱 개 모두 새 커널 실행 PASS(2026-09-17). 코드 셀 175개(21·19·21·25·30·32·27), 검사 문장 440·415·428·435·529·642·452. `uv run … python textbook/_notebook/verify.py --chapter textbook/part3/ch09-rag-first-run` → **`PASS 7 sections / 175 code cells (max 16 lines)`**(`chapter.json`이 없어 `run_section.sh`가 건너뛰므로 따로 실행).
- 빌드: `python _build.py` 뒤 HTML 8개에 남은 `{{` **0건**.
- 화면 검사: `textbook/_notebook/visual.cjs` 사본(`/tmp/ch09-close/vis/vis.cjs`, 공용 도구는 고치지 않음)으로 HTML 8개 × 1280·390px → **16/16 PASS**(작은 글자·대비·잘림·본문 밖 텍스트·가로 넘침·깨진 이미지·복사 단추·SVG 글자 넘침 0건). 챕터 `qa/visual-results.json`(개선 전 14행)은 전체 마감 때 16행으로 갱신합니다.
- 그림: Mermaid 27장 모두 `.render.json` 도장이 현재 mmd + `classes.mmd` + `config.json` 해시와 같고 PNG를 직접 확인했습니다. viewBox 폭은 모두 868 이하(최대 856). 삽화 7장은 저장 PNG를 채택 job 결과와 픽셀 대조했습니다.
- 실습 폴더 테스트: `uv run --project labs/part3/ch09-rag-first-run python -m pytest labs/part3/ch09-rag-first-run/tests -q` → **10 passed**(임베딩 요청 2번 포함). 실행 전후 `runs/` 29개 해시 같음.
- 개선 전 QA 스크립트: `qa/check_content.py` PASS(코드·출력 참조 0블록, 보존 출력 12블록, manifest 해시 12개 — `SECTIONS`에 07절 추가). `qa/test_build.py`·`qa/test_code_evidence.py` **6 passed**. `qa/test_notebook_migration.py`(2건 실패)와 `qa/check_structure.py`(01~07 전부 실패)는 개선 전 구조(`{{svg:}}` 5개·b1~b11·`<details class="instructor">`)를 요구해 고칠 수 없어 `qa/upgrade/before/qa-scripts/`로 옮겼습니다(삭제 아님, 참조 코드 0곳).
- 산출 파일: 06절이 `runs/continuity-ch09-search.jsonl`(SHA-256 `294713765a115b567e162aaf37a25467577841965c1075b86553adc4080666d5`)과 사본 하나를 새로 썼습니다. 계약(최상위 키 8개·`retrieved` 항목 키 5개·k=2 전제)은 그대로이고 `config` 안에 `corpus` 한 키가 늘었습니다. `harness.py`·`prompts.py`·`rag.py`·Ch 11 평가셋·Ch 6·7·8 사슬 파일은 해시가 바뀌지 않았고, `config.yaml`만 주석 한 줄로 `1e425071…`이 되었습니다.
- 과정 단계 검사: `textbook/qa/check_course_continuity.py`(182·184행 허용 목록에 ch09 기록 추가) → 원본 로그 보존 블록 통과, **212행 zip 신선도에서 멈춤**(`part1-practice.zip`, 전체 마감 몫).

### 이 기록의 해석

노트북 출력은 2026-09-17에 실제 OpenAI 모델(`gpt-5.4-mini`, `text-embedding-3-small`)로 한 번 실행한 결과입니다. 검토 반영에서는 어느 절도 다시 실행하지 않았습니다. 답 문장·출력 토큰 수·검색 점수는 실행마다 달라질 수 있어 결론에 쓰지 않았습니다. 비용은 모델 안내 요금과 토큰 수로 어림한 값이고 실제 청구액이 아닙니다.

### 재검증 명령

```bash
python3 textbook/_notebook/checks/upgrade_gates.py textbook/part3/ch09-rag-first-run --label after --strict
uv run --project labs/part3/ch09-rag-first-run python textbook/_notebook/verify.py --chapter textbook/part3/ch09-rag-first-run
(cd textbook/part3/ch09-rag-first-run && uv run --project ../../../labs/part3/ch09-rag-first-run --with pillow python _build.py)
uv run --project labs/part3/ch09-rag-first-run python -m pytest labs/part3/ch09-rag-first-run/tests -q
uv run --project labs/part3/ch09-rag-first-run python textbook/part3/ch09-rag-first-run/qa/check_content.py
```
