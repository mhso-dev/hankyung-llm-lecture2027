# 보호 파일 변경 기록 (`before-manifest.json` 147개 대조)

준비 담당이 적은 `qa/upgrade/before-manifest.json`(sha256 147개, `d5114134…`)과 절 작업 뒤 디스크를 대조한 기록입니다. 절마다 아래에 이어 적습니다. 새로 만든 파일(`qa/upgrade/*`·`figures/01-*`)은 목록 밖이라 여기 없습니다.

## 01절 뒤 (2026-09-25)

- **147개 가운데 139개 같음 · 8개 바뀜 · 없어진 것 0** — 바뀐 8개는 모두 01절이 의도해서 고친 파일입니다.

| 파일 | 전 → 후 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch25-streaming/notebooks/01-일곱-가지-stream-mode.ipynb` | `c7b772653cf1` → `723a4a14824f` | 01 노트북 개선본(새 커널 A2 실행 + 그림 첨부, `code_sha256` `650e86fce1fa…`) |
| `textbook/part6/_generate_ch25_ch26.py` | `545db83cf499` → `0767052613d9` | 챕터 밖 — 공용 옛 생성기 Ch 25 쪽 건너뛰기(결정 6, Ch 26 쪽 결과 파일 15개 해시 같음 — 사본 대조) |
| `textbook/part6/ch25-streaming/figures/_gen_figures.py` | `45d88f5ec4dd` → `cb02fe4e59df` | 옛 그림 생성기 맨 위 `raise SystemExit`(결정 6) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch25-streaming.json` | `e4366f11f0c6` → `22d280f95bf0` | 챕터 밖 — `verify.py --chapter`가 다시 씀 |
| `textbook/part6/ch25-streaming/01-일곱-가지-stream-mode.html` | `c9deeef5eecb` → `38730b75a061` | `_build.py` 다시 빌드(01 본문·그림) |
| `textbook/part6/ch25-streaming/_src/01-일곱-가지-stream-mode.html` | `6807d5178f07` → `bcefa4ac5e67` | 01 본문 개선본(`author_01.py`) |
| `textbook/part6/ch25-streaming/qa/verification.md` | `cb27f94a8718` → `17090cbf6794` | 「품질 개선 검증」 표와 01 행 덧붙임(위 옛 기록은 그대로) |
| `textbook/part6/ch25-streaming/집필점검표.md` | `805e89c08bfe` → `eabf8a8a7a23` | 「품질 개선」 표와 01 행 덧붙임(위 옛 표는 그대로) |

- 같음을 확인한 것 가운데 눈여겨볼 것: Ch 25 02·03 노트북·`_src`·HTML · 챕터 `index.html`·`chapter.json`·`_build.py` · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · 챕터·Part 6 공개 목록·선행 목록 · zip 셋 · `_build_index.py`·`build_index.py`·`build_bundle.py` · 목록에 든 Ch 24 파일(04 `_src`·HTML·`author_04.py`·요약·인계 — 01 슬러그 링크 그대로) · Ch 23·21 파일 · Ch 26·30 대기 챕터 파일 · 공용 검사·빌드 도구(`run_section.sh`·`nbkit.py`·`upgrade_gates.py`·`verify.py`·`execute.py`).
- 대조 결과 사본 `/tmp/ch25-01/manifest-now.txt`(첫 대조 — 점검표·검증 행 전).

## 02절 뒤 (2026-09-25)

- **147개 가운데 134개 같음 · 13개 바뀜 · 없어진 것 0** — 01절 뒤 바뀐 8개(그중 `qa/verification.md`·`집필점검표.md`·`notebook-contracts…json`은 02가 다시 바꿈) + 02절이 새로 바꾼 5개. 모두 의도한 변경입니다.

| 파일 | 01절 뒤 → 02절 뒤 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch25-streaming/notebooks/02-토큰과-중간-진행-스트리밍.ipynb` | `f4f7441539a5`(원본) → `74e56120e2ee` | 02 노트북 개선본(새 커널 A 18:14:46 실행 + 그림 첨부 + `mdpatch` 설명 셀, `code_sha256` `68b434d3f859…`) |
| `textbook/part6/ch25-streaming/_src/02-토큰과-중간-진행-스트리밍.html` | `443d633b2278`(원본) → `728cc7b3d3d2` | 02 본문 개선본(`author_02.py` + `mdpatch`) |
| `textbook/part6/ch25-streaming/02-토큰과-중간-진행-스트리밍.html` | `42648a01a9a7`(원본) → `269fd1e545e4` | `_build.py` 다시 빌드(02 본문·그림) |
| `textbook/part6/ch25-streaming/qa/public-files.json` | `d728ac4fbf17`(원본) → `bbfdade37e95` | 도구 파일 `notebooks/stream_tools.py` 한 줄 |
| `textbook/part6/public-files.json` | `7c9cb35e3374`(원본) → `b12a39212fbc` | 챕터 밖 — `collect_public_files.py`로 다시 모음(한 줄 늘어남, `prerequisite-files.json` 바이트 같음) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch25-streaming.json` | `22d280f95bf0` → `bb84d87808b3` | 챕터 밖 — `verify.py --chapter`가 다시 씀 |
| `textbook/part6/ch25-streaming/qa/verification.md` | `17090cbf6794` → `62d52e5b65b9` | 「품질 개선 검증」 표에 02 행 |
| `textbook/part6/ch25-streaming/집필점검표.md` | `eabf8a8a7a23` → `ea6743a7e5c4` | 「품질 개선」 표에 02 행 |

- 01절 뒤 값 그대로: 01 노트북 `723a4a14824f` · 01 `_src` `bcefa4ac5e67` · 01 HTML `38730b75a061` · `_generate_ch25_ch26.py` `0767052613d9` · `figures/_gen_figures.py` `cb02fe4e59df`.
- 같음을 확인한 것 가운데 눈여겨볼 것: 03 노트북·`_src`·HTML · 챕터 `index.html`·`chapter.json`·`_build.py` · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · Part 6 `prerequisite-files.json` · zip 셋(다시 만들지 않음 — 마감 몫) · Ch 21 `runner_tools.py` · Ch 24·23 파일 · Ch 26·30 대기 챕터 파일 · 공용 검사·빌드 도구.
- 목록 밖 새 파일: `labs/part6/ch25-streaming/notebooks/stream_tools.py`(`dfea09bc3644…`) · `figures/02-*`(Mermaid 넷 × `.mmd`·`.svg`·`.png`·`.caption.md`·`.render.json`, 삽화 `.png`·`.prompt.md`·`.caption.md`) · `qa/upgrade/author_02.py`·`02-probe.md`·`02-figures.md`·`02-diagnosis.md`·`probe/`·`review-pack/02-…md`·`gates-wip-02*.json`.

## 03절 뒤 (2026-09-25)

- **147개 가운데 131개 같음 · 16개 바뀜 · 없어진 것 0** — 02절 뒤 바뀐 13개(그중 `qa/verification.md`·`집필점검표.md`·`notebook-contracts…json`은 03이 다시 바꿈) + 03절이 새로 바꾼 3개. 모두 의도한 변경입니다.

| 파일 | 02절 뒤 → 03절 뒤 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch25-streaming/notebooks/03-TTFT와-total-비교.ipynb` | `4bef74ac8b58`(원본) → `bf1462828c47` | 03 노트북 개선본(새 커널 A 18:45:21 실행 + 그림 첨부 + `mdpatch` 설명 셀, `code_sha256` `ffe254e0d3c2…`) |
| `textbook/part6/ch25-streaming/_src/03-TTFT와-total-비교.html` | `a83ffd860264`(원본) → `3ca2fa1c33c4` | 03 본문 개선본(`author_03.py` + `mdpatch`) |
| `textbook/part6/ch25-streaming/03-TTFT와-total-비교.html` | `d671e2db1958`(원본) → `546ba9167927` | `_build.py` 다시 빌드(03 본문·그림) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch25-streaming.json` | `bb84d87808b3` → `18829e11726f` | 챕터 밖 — `verify.py --chapter`가 다시 씀 |
| `textbook/part6/ch25-streaming/qa/verification.md` | `62d52e5b65b9` → `1863c4088499` | 「품질 개선 검증」 표에 03 행 |
| `textbook/part6/ch25-streaming/집필점검표.md` | `ea6743a7e5c4` → `ca35598cd26e` | 「품질 개선」 표에 03 행 |

- 02절 뒤 값 그대로: 01·02 노트북(`723a4a14824f`·`74e56120e2ee`) · 01·02 `_src`(`bcefa4ac5e67`·`728cc7b3d3d2`) · 01·02 HTML(`38730b75a061`·`269fd1e545e4`) · 공개 목록 둘(`bbfdade37e95`·`b12a39212fbc` — 도구 파일 줄은 02가 올림) · `_generate_ch25_ch26.py` `0767052613d9` · `figures/_gen_figures.py` `cb02fe4e59df`.
- 같음을 확인한 것 가운데 눈여겨볼 것: 챕터 `index.html`·`chapter.json`·`_build.py` · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · Part 6 `prerequisite-files.json` · zip 셋(다시 만들지 않음 — 마감 몫) · **Ch 21 `runner_tools.py`(`f4113158…` — `estimate_cost`를 읽기만 함)** · Ch 6 06·Ch 15 05·Ch 17 04·Ch 18 03 노트북·`_src` · Ch 24·23 파일 · Ch 26·30 대기 챕터 파일 · 공용 검사·빌드 도구.
- 목록 밖 파일: **도구 파일 `labs/part6/ch25-streaming/notebooks/stream_tools.py` `dfea09bc3644…`(02 판) → `a468d87878fc…`(03 판, 함수 둘 덧붙임)** · 새 파일 `figures/03-*`(Mermaid 넷 × `.mmd`·`.svg`·`.png`·`.caption.md`·`.render.json`, 삽화 `.png`·`.prompt.md`·`.caption.md`) · `qa/upgrade/author_03.py`·`03-probe.md`·`03-figures.md`·`03-diagnosis.md`·`probe/probe03.py`·`probe/probe-03-{T3,R3}.jsonl`·`review-pack/03-…md`·`gates-wip-03*.json` · `handoff.md`(03 완료 줄 + 「§03 → 실습(04)」).
- 대조 결과 사본 `/tmp/ch25-03/manifest-now.txt`.

## 04절 뒤 (2026-09-25)

- **147개 가운데 125개 같음 · 22개 바뀜 · 없어진 것 0** = 03절 뒤 바뀐 16개(그중 7개는 04가 값을 다시 바꿈) + **04절이 지시대로 새로 바꾼 6개**(`chapter.json`·실습 폴더 `README.md`·챕터 `index.html`·`part6/index.html`·`part6-practice.zip`·`integration-results.json`). 모두 의도한 변경입니다.

| 파일 | 03절 뒤 → 04절 뒤 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `textbook/part6/ch25-streaming/chapter.json` | `28171e3214bf`(원본) → `da13aa03f20c` | 04절 추가(`hours`·`objectives` 그대로 — objectives는 마감 몫) |
| `labs/part6/ch25-streaming/README.md` | `ef0bf41d9545`(원본) → `bd86ef71819f` | 맨 아래 04절 한 단락만(다시 쓰기는 마감 몫) |
| `textbook/part6/ch25-streaming/index.html` | `6c94f5ec01c4`(원본) → `725777d6b40c` | `_build.py` — 04절 목차 줄 |
| `textbook/part6/ch25-streaming/03-TTFT와-total-비교.html` | `546ba9167927` → `466b95df011d` | `_build.py` — 다음 절 이동 줄 + b8 04 링크 |
| `textbook/part6/ch25-streaming/_src/03-TTFT와-total-비교.html` | `3ca2fa1c33c4` → `91d9f2cfb649` | b8 「04절 실습」에 링크만(`author_03.py --src-only`, 링크를 빼면 앞 해시와 같음) |
| `textbook/part6/ch25-streaming/qa/public-files.json` | `bbfdade37e95` → `0b890e75317c` | 04 HTML·04 노트북 두 줄 |
| `textbook/part6/public-files.json` | `b12a39212fbc` → `8140df88908b` | 챕터 밖 — `collect_public_files.py`(04 노트북 한 줄, `prerequisite-files.json` 바이트 같음) |
| `textbook/part6/index.html` | `a183814b4655`(원본) → `778b240be0d6` | 챕터 밖 — `_build_index.py`(Ch 25 「4절」·04 링크) |
| `textbook/downloads/part6-practice.zip` | `edd8c3be1179`(원본) → `acf14b060f58` | 챕터 밖 — `_build_index.py`(Ch 25 항목 8개 디스크와 같음) |
| `textbook/part6/qa/integration-results.json` | `a9661d7ce9af`(원본) → `8b9ecb322c8b` | 챕터 밖 — `_build_index.py`(`52 verified sections; 100 bundled files`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch25-streaming.json` | `18829e11726f` → `feefa318eca4` | 챕터 밖 — `verify.py --chapter`가 다시 씀 |
| `textbook/part6/ch25-streaming/qa/verification.md` | `1863c4088499` → `5bd9830c2628` | 「품질 개선 검증」 표에 04 행 |
| `textbook/part6/ch25-streaming/집필점검표.md` | `ca35598cd26e` → `dabd2209d5ad` | 「품질 개선」 표에 04 행 |

- 03절 뒤 값 그대로: 01·02·03 노트북(`723a4a14824f`·`74e56120e2ee`·**`bf1462828c47`** — 03은 다시 실행하지 않음) · 01·02 `_src`·HTML · `_generate_ch25_ch26.py` `0767052613d9` · `figures/_gen_figures.py` `cb02fe4e59df`.
- 같음을 확인한 것 가운데 눈여겨볼 것: `_build.py`·실습 폴더 `pyproject.toml`·`uv.lock` · Part 6 `prerequisite-files.json` · `llm-practice.zip`·`part7-practice.zip` · `delivery-results.json`(목록 밖, `3cc2d143…` 그대로) · Ch 21 `runner_tools.py` · Ch 24·23 파일 · Ch 26·30 대기 챕터 파일 · `_build_index.py`·`build_index.py`·`build_bundle.py` · 공용 검사·빌드 도구.
- 목록 밖 파일: **도구 파일 `stream_tools.py` `a468d87878fc…`(03 판) → `3a734aeb8724…`(04 판 — `import time` + 03절 함수 셋)** · `qa/upgrade/author_02.py` `1f1fe37be326` → `76afb50a0eb7`·`author_03.py` `9ac6183ce92f` → `747df9a376ba`(가드·메시지·03 b8 링크) · 새 파일 `labs/…/04-Streaming-실습.ipynb`(`d00014642d82…`)·`_src/04-Streaming-실습.html`·`04-Streaming-실습.html`·`figures/04-*`(Mermaid 셋 × 다섯 + 삽화 셋)·`qa/upgrade/author_04.py`·`04-probe.md`·`04-figures.md`·`04-diagnosis.md`·`probe/probe04.py`·`probe/probe-04-{N1,N2}.jsonl`·`review-pack/04-…md`(03 묶음 다시 만듦)·`gates-wip-04*.json`·`gates-wip-ch25-after04.json` · `handoff.md`(04 완료 줄 + 「실습 → 챕터 검토」).
- 대조 결과 사본 `/tmp/ch25-04/manifest-now.txt`.

## 마감 뒤 (2026-09-25, 검토 1차 반영)

- **147개 가운데 114개 같음 · 32개 바뀜 · 1개 옮김(없어짐)** — 모두 의도한 것입니다. 마감이 바꾼 것 **28**(아래 표) + 옮김 **1**(`figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/`, `mv -n`, 해시 `cb02fe4e59df` 같음) + 01~04절이 바꾼 뒤 마감이 건드리지 않은 **4**(`textbook/part6/_generate_ch25_ch26.py` `0767052613d9` · Part 6 `public-files.json` `8140df88908b`(`collect_public_files.py`를 다시 돌려 바이트 같음) · 챕터 `qa/public-files.json` `0b890e75317c`(옛 그림 줄이 원래 없어 그대로) · notebook-contracts `feefa318eca4`(`verify.py --chapter`가 다시 써도 같음)).
- 마감 전 사본은 `.cache/ch25-close/pre/`(챕터·실습 폴더·챕터 밖 파일), 대조 결과는 `.cache/ch25-close/log/manifest-now.txt`.

| 파일 | 04절 뒤 → 마감 뒤 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch25-streaming/README.md` | `bd86ef71819f` → `d29f86b3b970` | 전체 다시 씀(검토 A-13·B-10) |
| `labs/…/notebooks/01-일곱-가지-stream-mode.ipynb` | `723a4a14824f` → `be881fc5fb56` | 마크다운·그림 01-1 첨부만(코드·출력 해시 그대로, A-1·A-2) |
| `labs/…/notebooks/02-토큰과-중간-진행-스트리밍.ipynb` | `74e56120e2ee` → `e4068dbd5194` | 마크다운만(A-3·A-4·A-9·A-12) |
| `labs/…/notebooks/03-TTFT와-total-비교.ipynb` | `bf1462828c47` → `933c4202a6e7` | 마크다운만(B-1·B-2) |
| `labs/part6/continuity-guide.md` | `149a572a8f5f` → `629587f0d854` | 챕터 밖 — Ch 25 줄만(「Ch2의 비동기 실행」·「이벤트」·「지연」 뺌, A-16) |
| `textbook/downloads/part6-practice.zip` | `acf14b060f58` → `71683e44e8e0` | 챕터 밖 — `_build_index.py`(Ch 25 8항목·continuity-guide 디스크와 같음) |
| `textbook/part6/qa/integration-results.json` | `8b9ecb322c8b` → `bfe462a5d877` | 챕터 밖 — `_build_index.py`(`52 verified sections; 100 bundled files`) |
| `textbook/part6/index.html` | `778b240be0d6` → `64594baf8fc7` | 챕터 밖 — `_build_index.py`(Ch 25 설명 줄) |
| `textbook/part6/_build_index.py` | `5ffb7dde372c` → `e8d784c4971a` | 챕터 밖 — ch25 설명 줄만(시수 3·5 그대로) |
| `textbook/_notebook/build_index.py` | `53db811e5716` → `4bca42a3c613` | 챕터 밖 — Ch 25 설명만(절 수 3은 과정 전체가 실습 절을 빼고 세는 약속이라 그대로) |
| `textbook/index.html` | `1aea11034a8d` → `90d6a6b84dfa` | 챕터 밖 — `build_index.py` 한 번(바뀐 줄은 Ch 25 행 하나 — 대조 확인) |
| `textbook/part6/qa/bundle-execution.json` | `a72edd8a79a6` → `baaaf52f223c` | 챕터 밖 — 새 zip으로 묶음 실행 검사 PASS |
| `textbook/part6/qa/visual-results.json` | `dd444465a790` → `f2b70b7bcb57` | 챕터 밖 — Ch 25 줄만 8 → 10(`screens` 122 → 124) |
| `textbook/_notebook/checks/ch25-streaming/visual-results.json` | → `9d38d2e399d5` | `visual.cjs` 10행(스크린숏 넷 함께) |
| `textbook/part6/ch25-streaming/chapter.json` | `da13aa03f20c` → `7735f7707aea` | `objectives` 셋 → 넷(B-11, `hours` 그대로) |
| `textbook/part6/ch25-streaming/index.html` | `725777d6b40c` → `2ead7364a28a` | `_build.py`(학습 목표 넷) |
| 01·02·03 HTML | `38730b75a061`·`269fd1e545e4`·`466b95df011d` → `edfe7a857f49`·`8be21eafceed`·`780ae5012ba3` | `run_section.sh … --no-exec`·`_build.py` |
| 01·02·03 `_src` | `bcefa4ac5e67`·`728cc7b3d3d2`·`91d9f2cfb649` → `dcdca70c6714`·`74435a9022ba`·`cb5ab336239d` | 생성기 `--src-only`(검토 반영) |
| `qa/research.md`·`research.md`·`qa/ch25-technical-review.md`·`qa/authoring-checklist.md` | `d042f4f40ee7`·`80aeb44339bd`·`f08c1e4c3f7d`·`805e89c08bfe` → `ca7bb715ae1c`·`dc7c11020f80`·`500152ff234c`·`69061c53dbc1` | 머리에 「개선 전 판」 표시(내용 그대로) |
| `qa/verification.md`·`집필점검표.md` | `5bd9830c2628`·`dabd2209d5ad` → 마감 판 | 머리 「개선 전 판」 표시 + 끝 「마감」 절(이 기록 뒤에도 한 번 더 고칠 수 있어 해시는 적지 않음) |

- 목록 밖(마감이 바꾼 것): 04 `_src`·HTML(`5e1a529d4670…`) · `figures/01-1`·`02-3`·`03-3`의 `.mmd`·`.svg`·`.png`·`.render.json` · 캡션 `01-1`·`02-2`·`03-3`·`04-4` · `02-5`·`04-4` `.prompt.md`(끝에 마감 줄) · 생성기 `author_01~04.py`(문자열만) · `gates-after.json` · `gates-wip-01~04.json`(마감 `run_section.sh --no-exec`가 다시 씀) · `NN-diagnosis.md`·`NN-figures.md`·`handoff.md`·`chapter-summary.md` · `textbook/qa/upgrade-progress.md`(Ch 25 행)·`upgrade-final-checklist.md`(§2-13 등).
- 보존: 도구 파일 `stream_tools.py` `3a734aeb8724…`·04 노트북 `d00014642d82…`·`pyproject.toml`·`uv.lock`·공용 옛 생성기 `_generate_ch25_ch26.py`는 그대로. `llm-practice.zip`·`part7-practice.zip`·`delivery-results.json`(`3cc2d143…`)·`notebook-readiness.json`(옛 검사가 먼저 써서 되돌림, `b3d69e9c…`)도 그대로.
