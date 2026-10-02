# 09절 진단과 작업 기록 — 문서 처리 실습 (챕터 끝 실습 절)

규격 `textbook/QUALITY-UPGRADE.md` §7-2, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §3, 에이전트 절차 `.claude/agents/easy-upgrade-editor.md` 6.8.
앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1·2), `textbook/part3/ch09-rag-first-run/qa/upgrade/chapter-summary.md`, 이 챕터 `qa/upgrade/handoff.md` §01 → §02 ~ §08 → 실습, 01~08절 완료본.
기준 사례: Ch 22 `textbook/part6/ch22-middleware/_src/09-Middleware-실습.html`, Ch 9 `_src/07-RAG-실습.html`·`qa/upgrade/author_07.py`(검토 반영본).

## 1. 진단 — 새로 만든 절

**이 절은 수정 전 원본이 없습니다.** 챕터 끝 실습 절은 규격 §7-2가 새로 붙이라고 정한 절이라 게이트 「전」 수치가 없습니다.
챕터 전체 수정 전 게이트는 `gates-before.json`(8절, 합계 363)이고 01~08절 진단은 `01-diagnosis.md`~`08-diagnosis.md`에 있습니다.

작업 전에 확인한 것:

| 확인한 것 | 결과 |
|---|---|
| 08절 뒤 챕터 상태 | 개념 8절 모두 G1~G7 0, `verify.py --chapter` `PASS 8 sections / 185 code cells` |
| `runs/` 정본 | `continuity-ch10-indexing.jsonl` `58cc790c45df9bf9cfbdda21a4de267bd10a7749568f1306d9625657d5ebda45`(6줄), 사본 48개, `runs/` 전체 64개 |
| 실습 폴더 모듈 | `document_processing.py` `37ca2cc9…`·`experiment.py` `342e85b0…`, 테스트 38 passed |
| HTML 해시 | `/tmp/ch10-09/hash/disk-before.txt`(9개) |
| 기기 디스크 | 루트 여유 566MB(작업 뒤 545MB), 작업 폴더 `/tmp/ch10-09` |

## 2. 주제를 고른 근거

handoff §08 → 실습이 「이 챕터에서 아직 한 번에 이어 보지 않은 묶음」으로 남긴 것을 그대로 골랐습니다.
「형식이 다른 문서 두 개를 읽어(01·03·04) 같은 칸 기록을 붙이고(01·03) 한 방식으로 나눠(05) 한 색인에 넣어 찾기(08)」입니다.

여기에 04절이 남긴 물음을 함께 풀었습니다. handoff §04 → §05는 「이 챕터에는 출처 표시 함수가 세 개이니 05절 이후 형식이 섞인 글을 다룰 때 어느 함수를 쓸지 정하라」고 적었습니다.
실습은 세 함수를 고치지 않고 부르는 함수 `pick_mark()` 하나를 새로 만들어 답했습니다. 칸을 보는 순서는 실습 폴더 `document_processing.py` `_with_chunk_metadata()`와 같은 `page`·`section`·`row`입니다.

핵심은 네 개입니다: 형식마다 다른 읽기(01·03·04) → 형식마다 다른 기록과 출처 표시(01·03·04) → 한 방식으로 나누기(05) → 한 색인에 넣어 검색(08).
새 함수는 세 개(`pick_mark`·`run_index`·`print_hit_rows`)이고 새 API·새 문법은 0개입니다.

## 3. 실행 1·2 설계와 결과

바꾸는 값은 색인에 넣는 문서 묶음 하나입니다. 질문·검색 개수 5·목표 크기 200자·겹침 0자·끊을 자리 순서·임베딩 모델은 같게 두었습니다.

| 실행 | 색인에 넣은 것 | 문서 청크 | 1위 | 나머지 네 줄 |
|---|---|---|---|---|
| 실행 1 | PDF 한 건(E01 2쪽) | 6개 `[185, 147, 86, 164, 130, 188]` | `[E01 p.2]` 147자 점수 `0.33` | 모두 `[E01 p.2]`(86·164·130·188자) |
| 실행 2 | 세 형식(PDF·DOCX·HWPX) | 8개 | `[sample docx]` 26자 점수 `0.63` | `[E01 p.2]` 네 줄(147·86·164·130자) |

- 실행 1의 1위는 질문과 관계없는 도서관 운영 목표 글입니다. 색인에 답이 없어도 검색은 다섯 줄을 채웁니다(Ch 9 05절 「답이 없는 질문」과 이음).
- 실행 2에서 PDF 문서 청크 네 개는 차례가 그대로이고 순위만 한 칸씩 내려갔습니다. 실행 1의 다섯째 줄 188자 문서 청크는 다섯 줄 상한에 밀려 표에서 빠졌습니다.
- HWPX 문서 청크는 두 실행 모두 상위 다섯 줄에 없습니다. 몇 위였는지는 확인하지 않았습니다(다섯 줄만 받음).
- **점수 경계**: 셋째 줄 점수가 새 커널 두 실행에서 `0.31`과 `0.3`로 갈렸습니다(소수 둘째 자리 자름). 교재 출력(두 번째 실행)에는 실행 1 `0.31`·실행 2 `0.3`이 남았고, 그 사실을 b6 한 단락과 b7 항목에 적었습니다. 1위 점수 `0.33`·`0.63`은 두 실행에서 같았고 그림 라벨에는 이 두 값만 넣었습니다.

**질문을 고른 과정(규격 §3)**: 교재를 만들 때 휴관일 질문과 배송 질문을 각각 두 색인에 보내 보았습니다. 휴관일 질문은 PDF에만 답이 있어 문서를 더해도 상위 다섯 줄이 바뀌지 않았습니다. 그래서 DOCX 견본에만 있는 내용을 묻는 질문을 골랐고, 과정과 「흐름을 보여 주려고 정한 예」를 b7 첫 항목에 적었습니다.

## 4. 바꾼 것 (파일별)

- **새 파일**: `qa/upgrade/author_09.py`(생성기), `labs/part3/ch10-document-processing/notebooks/09-문서-처리-실습.ipynb`(코드 셀 30개), `_src/09-문서-처리-실습.html`(10블록), `figures/09-1-조립도.*`·`09-2-실행1-순서.*`·`09-3-두-실행-비교.*`(mmd·svg·png·caption·render.json), `figures/09-4-세-묶음과-한-상자.png/.prompt.md/.caption.md`, `qa/upgrade/09-figures.md`, 이 파일, `qa/upgrade/before/08-to-09/`(08절 `_src`·노트북·`index.html`·README 수정 전 사본).
- **`_build.py`**: `SECTIONS`에 09 제목 한 줄(주제 포함), `render_index()` 메타 「개념 8절」 → 「개념 8절 + 실습 1절」. 빌드한 HTML 10개에 `{{` 잔존 0건.
- **08절**(`mdpatch.py`, **재실행하지 않음** — 기록 계약): `_src` b8 「다음 학습」 두 단락을 09절 안내로 바꾸고 Ch 11·12 안내는 09절 b8로 옮겼습니다. 노트북 정리 끝 세 줄도 같은 뜻으로 고쳤습니다. 노트북은 마크다운 셀 하나만 달라졌고 **코드 셀과 출력은 그대로**입니다(대조 결과 코드 0건·출력 0건 변경).
- **`_src/index.html`**(목차 본문, 게이트 밖): 절 표에 09행(30분 · 실습 16h 안), 학습 범위 단락에 실습 절 문단, 05~09절이 쓰는 자료 문단, 「다음 학습」 세 단락, 마지막 단락의 개선 전 08절 설명(45자 청크·large 모델)을 지금 설계로 고쳤습니다. `[[미정: 임베딩 모델]]` 표시는 강사 확인 항목이라 그대로 두었습니다.
- **실습 폴더 `README.md`**: 기준 파일 01~09절, 06~09절 키 필요, 09절 한 단락(주제·30분·요청 4번·파일 쓰지 않음). 08절 문장의 `local_token_estimate` 설명은 개선된 기록에 그 칸이 없어 「노트북이 요청 전에 출력하는 조각 수와 비용 어림」으로 고쳤습니다.
- **`qa/verification.md`**: 표에 09절 행 + 메모 11줄. **`집필점검표.md`**: 두 표에 09절 행.
- **챕터 밖 파일 두 개**(규격 §7-2가 함께 고치라고 적은 곳): `textbook/part3/_build_index.py` `CHAPTERS`의 ch10 절 수 칸 8 → 9(강의 8h·실습 16h 그대로), `textbook/part3/qa/finalize_continuity_evidence.py` 15행 `assert len(visual) == 88` → `92`(주석 세 줄로 행 수 구성과 남은 일 적음).
- **화면 검사 결과 파일**: `textbook/_notebook/checks/ch10-document-processing/visual-results.json` 18행 → 20행(공용 `visual.cjs` 재실행 결과, 20/20 PASS).
- **챕터 안 QA 스크립트 두 개**: `qa/check_visual.cjs`의 14px 허용 목록을 공용 `visual.cjs`와 같게 맞춰(`.nb-toolbar`·`.nb-prompt`·`button`·`.copy-status`) 20/20 PASS → `qa/visual-results.json` 18행 → 20행. `qa/check_content.py`는 b1~b11 열한 블록·`<details class="instructor">`·`{{code:}}`·`{{output:}}`을 요구하는 개선 전 전제라 `qa/upgrade/before/qa-scripts/`로 `mv -n`(삭제 아님, 참조하는 코드 0곳, Ch 9 선례).

**준비 셀 `import os` 중복을 없앴습니다.** Ch 9 검토 B 05-1이 지적한 모양입니다(공용 `nbkit.KEY`가 `import os`를 다시 부름). 09절은 키 확인 셀을 생성기 안에 따로 두어 `IMPORTS`의 `import os`만 씁니다. 공용 `nbkit.py`는 고치지 않았습니다.

## 5. 건드리지 않은 것 (확인한 해시)

| 파일 | 상태 |
|---|---|
| `runs/` 전체 64개 | 작업 전후 묶음 해시 `2a73b21a073dfc9f76b606393abd85a0b94f409174cfdf8e6014737f45cdf84e` 같음 |
| `runs/continuity-ch10-indexing.jsonl` | `58cc790c45df9bf9cfbdda21a4de267bd10a7749568f1306d9625657d5ebda45`(6줄) 그대로 |
| `document_processing.py`·`experiment.py` | `37ca2cc9…`·`342e85b0…` 그대로, 노트북에서 부르지 않음 |
| `tests/`·`fixtures/` | 고치지 않음, 38 passed(작업 전후 같음) |
| Ch 11 평가셋·Ch 6~9 사슬 기록 | 읽지도 쓰지도 않음 |
| 01~07절 HTML | 해시 그대로. 08절 HTML은 다음 절 링크와 b8 문단만 달라짐(`0273e394…` → `98d3c32c…`) |

## 6. 검사 결과

- `upgrade_gates.py --label wip --section 09`: **G1~G7 모두 0, PASS**(`gates-wip-09.json`, 코드 셀 30, 검사 문장 443 → 검토 반영 뒤 451).
- 챕터 전체 `upgrade_gates.py --label wip`: **9/9 PASS, G1~G7 0**(`gates-wip.json`).
- `verify.py --chapter`: `PASS 9 sections / 215 code cells (max 14 lines)`(08절 뒤 185).
- 새 커널 실행: `execute.py` **PASS 30 cells** 두 번. 교재 출력은 두 번째 실행(`executed_at` 2026-09-18T06:57:44Z, `fresh_kernel: true`, `outputs_sha256` `0c1619ae…`, `code_sha256` `88b63098…`)입니다. 그 뒤 설명 문장만 `mdpatch.py`로 고쳤고 코드 셀과 출력은 그대로입니다.
- 공용 `visual.cjs`(`/tmp` 사본): 10페이지 × 1280·390px **20/20 PASS**.
- 실습 폴더 테스트 **38 passed**, `runs/`·모듈 해시 전후 같음.
- `build_bundle.py`의 `check_public_file()`·`validate()`·`validate_parts()`를 09 노트북에 직접 돌려 통과.
- 게이트 중간에 걸려 고친 것 네 개: `E01.pdf`를 백틱으로 인용해 G5가 셀 출력에 없는 숫자로 본 자리, 점검표 첫 열두 글자 인용 오타(`배송 안내 제주 배송에는` → `배송 안내 제주 배송에`), 71자 문장 하나, 문장을 나눈 뒤 6문장이 된 b7 항목.

## 7. 과정 단계 검사 (앞과 같은 자리에서 멈춤)

- `textbook/part3/qa/check_continuity.py` → 154행 `Stale archive: part2-practice.zip/…`(zip 신선도).
- `textbook/qa/check_course_continuity.py` → 212행 `Stale archive: part1-practice.zip/…`(zip 신선도). 기기 `python3`이 3.10이라 `tomllib`이 없어 실습 폴더 가상환경(3.12.13)으로 돌렸습니다.
- 두 검사의 해시 허용 목록은 고치지 않았습니다. 09절이 `runs/`를 건드리지 않았기 때문입니다.
- `textbook/part3/_build_index.py`는 절 수 검사(56행)를 지납니다. ch09 7 · ch10 9 · ch11 6 · ch12 12로 `_src` 개수와 같습니다. **목차 페이지와 `part3-practice.zip` 재생성은 돌리지 않았습니다**(전체 마감 몫, Ch 9 요약 §9 선례).

## 8. 남은 것

- **전체 마감**: `part3-practice.zip` 재생성(09 노트북이 아직 묶음에 없음) → `run_continuity_bundle.py` → ch09 HTML을 공용 `visual.cjs`로 다시 찍어 `checks/ch09-rag-first-run/visual-results.json`을 14행 → 16행으로 → `finalize_continuity_evidence.py`(이제 92를 기대) → 두 continuity 검사.
- **챕터 요약**(`qa/upgrade/chapter-summary.md`)과 루트 `textbook/qa/upgrade-progress.md` Ch 10 행: 오케스트레이터 몫입니다. 진행표는 아직 「절 개선 중(01 완료)」입니다.
- **2차 검토에서 볼 곳**: 09절 본문 b4 비유 단락과 삽화(카드 수를 노트북 문서 청크 수와 맞추지 않은 점), b6 점수 경계 단락, b7 질문 선택 근거, `_src/index.html`의 남은 개선 전 문장(`[[미정: 임베딩 모델]]`·「챕터 개요」 첫 단락), 08절 b8 수정 문단.
- **정리 대상(삭제하지 않고 목록만)**: `qa/content-results.json`(옮긴 `check_content.py`의 개선 전 결과), `qa/1280-*.png`·`390-*.png` 여섯 개(개선 전 화면 캡처였고 `check_visual.cjs` 재실행으로 개선본 캡처로 덮였습니다), `qa/upgrade/gates-wip-01.json`~`09.json`, 기기 `/tmp/ch10-09`, `.cache/vm/shot/ch10-09-*.png`.
- **강사 확인 대상**: 실습 절 30분을 챕터 시수(강의 8h·실습 16h)에 더하지 않고 실습 16h 안으로 둔 것(규격 §7-2), 09절 표시 제목 「09 · 문서 처리 실습: 형식이 다른 문서를 한 색인에 모아 찾기」.

## 검토 반영 (별도 세션 검토 1차, 2026-09-18 챕터 마감 세션)

검토 보고서: `review-round1-A.md`(§01~05)·`review-round1-B.md`(§06~09), 각 끝 「반영 결과」. 이 절은 **다시 실행하지 않았습니다**(설명·본문·그림만 바뀜, 규격 §3). 노트북 `code_sha256`·`outputs_sha256`·`executed_at`가 반영 전후 같습니다.

- **[중] 09-1** 그림 `09-2-실행1-순서`의 노란 메모 「저장 항목 6개」 → 「문서 청크 6개를 넣음」. 노트북은 `len(store.store)`를 출력하지 않고 `문서 청크 수: 6`만 출력하므로, 노랑(출력으로 확인한 값) 자리에 실행하지 않은 관찰이 들어가 있었습니다. 본문 도식 읽기 「첫 노란 메모는 그 직후에 확인한 저장 항목 수입니다」 → 「첫 노란 메모는 색인에 넣은 문서 청크 수입니다」. mmd 재렌더 viewBox 750.5.
- **[하] 09-2** b6 「소수 둘째 자리에서 자른 값」 → 「반올림한 값」(`print_hit_rows()`는 `round(score, 2)`).
- **[하] 09-3** 노트북 [63] 결과 읽기에 한 단락 — 「셋째 줄 86자 문서 청크의 점수만 `0.31`과 `0.3`으로 갈렸습니다. 같은 글도 요청마다 소수 아래 자리가 달라질 수 있어 순위와 출처 표시를 먼저 읽습니다.」(규격 §6)
- **[하] 09-5** 노트북 [59] 결과 읽기에 「DOCX 재료는 27자였는데 문서 청크는 26자입니다. 끝 줄바꿈이 빠졌기 때문입니다.」
- **[하] 09-6** 그림 `09-3-두-실행-비교`의 질문 라벨을 실제 글 「제주로 보내는 배송은 며칠이 더 걸리나요?」로 바꿨습니다(규격 §5-3). alt·캡션도 함께, viewBox 504.7.
- **[하] 09-7** 노트북 마지막 두 소제목에 번호를 붙였습니다 — 「## 10. 실험 결과 해석」·「## 11. 정리」(01~08절 표기와 통일).
- **[하] 09-8** b2 둘째 단락을 자료 중심으로 — 「이 실습의 자료는 01~04절에서 읽은 견본 세 개입니다. 형식이 섞인 자료를 한 색인에 모으는 흐름만 보려고 그대로 씁니다.」
- 검토 B의 09 결정 여섯 가지(주제, `pick_mark()` 신설, 점수 경계 단락, 질문 선택 근거, 요청 4번, 규격 §7-2 점검 전부)는 **수용**입니다.
- **미반영**: 삽화 `09-4-세-묶음과-한-상자`의 꼬리표 수(네모 4·타원 2·세모 1 → 6·1·1, 검토 B 09-4). 그림을 다시 만드는 일이고 **강사 확인 대상**으로 남겼습니다. 「그림 읽기」가 「카드 수는 노트북 8절 문서 청크 수와 맞춘 것이 아닙니다」로 밝혀 두었습니다.
- **이 절은 파일을 쓰지 않습니다**: `runs/` 64개 해시가 반영 전후 같습니다.
