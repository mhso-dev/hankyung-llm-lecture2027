# 보호 파일 변경 기록 (`before-manifest.json` 131개 대조)

준비 담당이 적은 `qa/upgrade/before-manifest.json`(sha256 131개, `ab149cd5…`)과 절 작업 뒤 디스크를 대조한 기록입니다. 절마다 아래에 이어 적습니다. 새로 만든 파일(`approval_tools.py`·`qa/upgrade/*`·`figures/01-*`)은 목록 밖이라 여기 없습니다.

## 01절 뒤 (2026-09-25)

- **131개 가운데 121개 같음 · 10개 바뀜 · 없어진 것 0** — 바뀐 10개는 모두 01절이 의도해서 고친 파일입니다.

| 파일 | 전 → 후 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch24-human-in-the-loop/notebooks/01-interrupt-승인-게이트.ipynb` | `74e0176d098f` → `9f25361bad4a` | 01 노트북 개선본(새 커널 A 실행 + 설명만 `mdpatch.py`, `code_sha256` `7187f7a39f3f…`) |
| `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py` | `44c9d593fcd0` → `3fc72dedb865` | 챕터 밖 — 공용 옛 생성기 첫머리 `raise SystemExit`(결정 7, Ch 23 쪽 영향 없음) |
| `textbook/part6/ch24-human-in-the-loop/figures/_gen_figures.py` | `ced25fb25d22` → `2a015c6ada60` | 옛 그림 생성기 맨 위 `raise SystemExit`(결정 7) |
| `textbook/part6/public-files.json` | `8ed6852b524f` → `a77415947a7e` | 챕터 밖 — `collect_public_files.py`로 다시 모음(도구 파일 한 줄) |
| `textbook/part6/ch24-human-in-the-loop/qa/public-files.json` | `52d2b01c3db5` → `c629078f134d` | 도구 파일 `approval_tools.py` 한 줄 더함(13 → 14줄) |
| `textbook/part6/ch24-human-in-the-loop/qa/verification.md` | `2452eb908c03` → `be8cc9d417a2` | 「품질 개선 검증」 표와 01 행 덧붙임(위 옛 기록은 그대로) |
| `textbook/part6/ch24-human-in-the-loop/집필점검표.md` | `1b1e3e622007` → `7883cb04e71e` | 「품질 개선」 표와 01 행 덧붙임(위 옛 표는 그대로) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json` | `de513cff466f` → `6e540bbc3a4d` | 챕터 밖 — `verify.py --chapter`가 다시 씀 |
| `textbook/part6/ch24-human-in-the-loop/01-interrupt-승인-게이트.html` | `2931d3bb05d9` → `09f46b30fd0c` | `_build.py` 다시 빌드(01 본문·그림) |
| `textbook/part6/ch24-human-in-the-loop/_src/01-interrupt-승인-게이트.html` | `de0701d758e9` → `5960408bb949` | 01 본문 개선본(`author_01.py`) |

- 같음을 확인한 것 가운데 눈여겨볼 것: Ch 24 `02·03` 노트북·`_src`·HTML · 챕터 `index.html`·`chapter.json`·`_build.py` · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · Part 6 `prerequisite-files.json`·zip 셋·`bundle-execution.json`·`_build_index.py`·`check_bundle_execution.py` · 목록에 든 Ch 23 파일(공용 옛 생성기 말고) · Ch 25·27·28·30 대기 챕터 파일 · 공용 검사·빌드 도구.
- 대조 스크립트 출력 사본 `/tmp/ch24-01/manifest-now.txt`.

## 02절 뒤 (2026-09-25)

- **131개 가운데 118개 같음 · 13개 바뀜 · 없어진 것 0** — 01절 뒤 10개에 02절이 바꾼 셋이 더해졌고, 01절 뒤 목록 가운데 둘은 02절이 다시 바꿨습니다. 모두 의도한 변경입니다.

| 파일 | 01절 뒤 → 02절 뒤 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch24-human-in-the-loop/notebooks/02-Command-resume으로-실행-재개.ipynb` | `b787cf038e71`(원본 그대로) → `5391d97bb170` | 02 노트북 개선본(새 커널 A 실행 + 그림 첨부, `code_sha256` `ead91c80882f…`) |
| `textbook/part6/ch24-human-in-the-loop/_src/02-Command-resume으로-실행-재개.html` | `d181c103e244`(원본 그대로) → `156ccab74aa2` | 02 본문 개선본(`author_02.py`) |
| `textbook/part6/ch24-human-in-the-loop/02-Command-resume으로-실행-재개.html` | `c523aeec8e60`(원본 그대로) → `8f502dfb2938` | `_build.py` 다시 빌드(02 본문·그림) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json` | `6e540bbc3a4d` → `a9436d1fd742` | 챕터 밖 — `verify.py --chapter`가 다시 씀 |
| `textbook/part6/ch24-human-in-the-loop/qa/verification.md` | `be8cc9d417a2` → `ee484008438e` | 「품질 개선 검증」 표에 02 행 덧붙임 |
| `textbook/part6/ch24-human-in-the-loop/집필점검표.md` | `7883cb04e71e` → `4c89ff1e10a0` | 「품질 개선」 표에 02 행 덧붙임 |

- 01절 뒤 값 그대로인 것: 01 노트북 `9f25361bad4a` · 01 `_src` `5960408bb949` · 01 HTML `09f46b30fd0c`(다시 빌드했지만 바이트 같음) · 공용 옛 생성기 `3fc72dedb865` · `figures/_gen_figures.py` `2a015c6ada60` · Part·챕터 공개 목록 `a77415947a7e`·`c629078f134d`.
- 같음을 확인한 것 가운데 눈여겨볼 것: Ch 24 `03` 노트북·`_src`·HTML · 챕터 `index.html`·`chapter.json`·`_build.py` · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · 도구 파일(목록 밖, `b40aab98ae6d…` 그대로) · Part 6 `prerequisite-files.json`·zip 셋·`bundle-execution.json`·`_build_index.py`·`check_bundle_execution.py` · Ch 23·25·27·28·30 파일 · 공용 검사·빌드 도구.
- 목록 밖 새 파일(02): `qa/upgrade/author_02.py`·`02-figures.md`·`02-diagnosis.md`·`gates-wip-02-02.json`·`gates-wip-02.json`·`review-pack/02-…md` · `figures/02-1~02-5`(`.mmd`·`.svg`·`.png`·`.caption.md`·`.render.json`)·`02-6`(`.png`·`.prompt.md`·`.caption.md`). 대조 스크립트 출력 사본 `/tmp/ch24-02/manifest-now.txt`.

## 03절 뒤 (2026-09-25)

- **131개 가운데 115개 같음 · 16개 바뀜 · 없어진 것 0** — 02절 뒤 13개에 03절이 바꾼 셋(03 노트북·`_src`·HTML)이 더해졌고, 02절 뒤 목록 가운데 셋(`verification.md`·`집필점검표.md`·notebook-contracts)은 03절이 다시 바꿨습니다. 모두 의도한 변경입니다.

| 파일 | 02절 뒤 → 03절 뒤 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch24-human-in-the-loop/notebooks/03-상태-기록과-다른-분기-재실행.ipynb` | `fcf438dcb404`(원본 그대로) → `e7649d5a0cbd` | 03 노트북 개선본(새 커널 A 실행 + 그림 첨부 + 정리 끝 설명 `mdpatch.py`, `code_sha256` `12b29f1517d5…`) |
| `textbook/part6/ch24-human-in-the-loop/_src/03-상태-기록과-다른-분기-재실행.html` | `c6f27b8eeb46`(원본 그대로) → `a6eabd0dcb84` | 03 본문 개선본(`author_03.py`) |
| `textbook/part6/ch24-human-in-the-loop/03-상태-기록과-다른-분기-재실행.html` | `8207f38e9aa1`(원본 그대로) → `d1d9e365663f` | `_build.py` 다시 빌드(03 본문·그림) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json` | `a9436d1fd742` → `cfbce0b9e1b3` | 챕터 밖 — `verify.py --chapter`가 다시 씀 |
| `textbook/part6/ch24-human-in-the-loop/qa/verification.md` | `ee484008438e` → `fb173b278415` | 「품질 개선 검증」 표에 03 행 덧붙임 |
| `textbook/part6/ch24-human-in-the-loop/집필점검표.md` | `4c89ff1e10a0` → `23f65da85c92` | 「품질 개선」 표에 03 행 덧붙임 |

- 02절 뒤 값 그대로인 것: 01·02 노트북 `9f25361bad4a`·`5391d97bb170` · 01·02 `_src` `5960408bb949`·`156ccab74aa2` · 01·02 HTML `09f46b30fd0c`·`8f502dfb2938`(다시 빌드했지만 바이트 같음) · 공용 옛 생성기 `3fc72dedb865` · `figures/_gen_figures.py` `2a015c6ada60` · Part·챕터 공개 목록 `a77415947a7e`·`c629078f134d`(경로 배열 — 도구 파일 줄은 01이 이미 넣음).
- 같음을 확인한 것 가운데 눈여겨볼 것: 챕터 `index.html`·`chapter.json`·`_build.py` · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · Part 6 `prerequisite-files.json`·zip 셋·`bundle-execution.json`·`_build_index.py`·`check_bundle_execution.py` · Ch 23·25·27·28·30 파일 · 공용 검사·빌드 도구.
- **목록 밖이지만 바뀐 것**: 도구 파일 `labs/part6/ch24-human-in-the-loop/notebooks/approval_tools.py` `b40aab98ae6d…` → **`d562c9e67c56…`**(03이 `print_history`·`find_before`를 덧붙임 — 01 함수 셋 글자 그대로). zip 안 판은 옛 판(도구 파일 없음 — 마감 몫).
- 목록 밖 새 파일(03): `qa/upgrade/author_03.py`·`03-figures.md`·`03-diagnosis.md`·`gates-wip-03-03.json`·`gates-wip-03.json`·`review-pack/03-…md` · `figures/03-1~03-4`(`.mmd`·`.svg`·`.png`·`.caption.md`·`.render.json`)·`03-5`(`.png`·`.prompt.md`·`.caption.md`). `handoff.md`에 「§03 → 실습(04)」. 대조 스크립트 출력 사본 `/tmp/ch24-03/manifest-now.txt`.

## 04절 뒤 (2026-09-25, 실습 절 새로 만듦)

- **131개 가운데 109개 같음 · 22개 바뀜 · 없어진 것 0** — 03절 뒤 16개에 04절이 새로 바꾼 여섯이 더해졌고, 03절 뒤 목록 가운데 일곱은 04절이 다시 바꿨습니다. 모두 과제가 시킨 변경입니다.

| 파일 | 03절 뒤 → 04절 뒤 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `textbook/part6/ch24-human-in-the-loop/chapter.json` | `64fad507e973`(원본 그대로) → `1ee64948471d` | `sections`에 04절 추가(`hours`·`objectives` 그대로) |
| `labs/part6/ch24-human-in-the-loop/README.md` | `525aa21ac755`(원본 그대로) → `7c557ad26f23` | 맨 아래 04절 한 단락(다시 쓰기는 마감 몫) |
| `textbook/part6/ch24-human-in-the-loop/index.html` | `d0dc258b711e`(원본 그대로) → `bd3554a12c2f` | `_build.py`가 04 줄을 넣어 다시 씀 |
| `textbook/part6/index.html` | `cfd0cd817524`(원본 그대로) → `afe83bc7dede` | 챕터 밖 — `_build_index.py` 한 번(Ch 24 「4절」·04 링크) |
| `textbook/downloads/part6-practice.zip` | `aa82b386b154`(원본 그대로) → `61119a820068` | 챕터 밖 — 같은 스크립트(Ch 24 항목 8개가 디스크와 같아짐) |
| `textbook/part6/qa/integration-results.json` | `624a596eb10d`(원본 그대로) → `fa46898a97f4` | 챕터 밖 — 같은 스크립트(`sections: 51`·`bundle_files: 98`) |
| `textbook/part6/public-files.json` | `a77415947a7e` → `7c9cb35e3374` | 챕터 밖 — `collect_public_files.py`(04 노트북 한 줄) |
| `textbook/part6/ch24-human-in-the-loop/qa/public-files.json` | `c629078f134d` → `c72eba466843` | 04 HTML·노트북 두 줄 |
| `textbook/part6/ch24-human-in-the-loop/_src/03-상태-기록과-다른-분기-재실행.html` | `a6eabd0dcb84` → `aa00400d83e3` | b8 「04절」에 링크(`author_03.py --src-only`) |
| `textbook/part6/ch24-human-in-the-loop/03-상태-기록과-다른-분기-재실행.html` | `d1d9e365663f` → `421d2df7e1f0` | 다시 빌드(다음 절 이동 줄 + b8 링크) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json` | `cfbce0b9e1b3` → `1a241f44e4a4` | 챕터 밖 — `verify.py --chapter`가 다시 씀 |
| `textbook/part6/ch24-human-in-the-loop/qa/verification.md` | `fb173b278415` → `d4cefae849a1` | 「품질 개선 검증」 표에 04 행 |
| `textbook/part6/ch24-human-in-the-loop/집필점검표.md` | `23f65da85c92` → `a0b1c726e78f` | 「품질 개선」 표에 04 행 |

- 03절 뒤 값 그대로인 것: 01·02·03 노트북 `9f25361bad4a`·`5391d97bb170`·`e7649d5a0cbd`(03 `code_sha256`·`outputs_sha256` 그대로) · 01·02 `_src`·HTML(다시 빌드했지만 바이트 같음) · 공용 옛 생성기 `3fc72dedb865` · `figures/_gen_figures.py` `2a015c6ada60` · 실습 폴더 `pyproject.toml`·`uv.lock` · Part 6 `prerequisite-files.json`·`_build_index.py`·`bundle-execution.json`·`delivery-results.json`(`check_delivery.py`가 117행에서 멈춰 쓰지 않음)·`llm-practice.zip`·`part7-practice.zip` · `textbook/index.html` · Ch 23·25·27·28·30 파일 · 공용 검사·빌드 도구.
- **목록 밖이지만 바뀐 것**: `qa/upgrade/author_03.py` `6ec79811b413` → `d2c014669b12`(b8 링크 한 곳) · `qa/upgrade/gates-wip-03.json`(03 `--no-exec`가 다시 씀, 값 0). 도구 파일 `approval_tools.py`는 **그대로**(`d562c9e67c56…`).
- 목록 밖 새 파일(04): `qa/upgrade/author_04.py`·`04-figures.md`·`04-diagnosis.md`·`gates-wip-04-04.json`·`gates-wip-04.json`·`gates-wip-ch24-after04.json`·`review-pack/04-…md` · `_src/04-…html`·빌드 `04-…html`·노트북 `04-…ipynb` · `figures/04-1~04-3`(`.mmd`·`.svg`·`.png`·`.caption.md`·`.render.json`)·`04-4`(`.png`·`.prompt.md`·`.caption.md`). `handoff.md`에 「실습 → 챕터 검토」. 대조 스크립트 출력 사본 `/tmp/ch24-04/manifest-now.txt`.

## 마감 뒤 (2026-09-25, 검토 반영과 챕터 마감)

- **131개 가운데 102개 같음 · 27개 바뀜 · 2개 옮김(없어짐)** — 모두 과제가 시킨 변경입니다(`.cache/ch24-close/tools/manifest_check.py`). 04절 뒤 바뀐 22개(01절이 막은 옛 생성기 둘 포함) 가운데 20개를 마감이 다시 바꾸거나 옮겼고(마감 전 사본 `.cache/ch24-close/pre/`와 견줌 — 내용 18 · 옮김 2), 마감이 새로 바꾼 것이 일곱(`continuity-guide.md`·`research.md`·`bundle-execution.json`·Part 6 `visual-results.json`·챕터 `visual-results.json`·`_build_index.py`·Ch 23 `chapter-summary.md`)입니다. 04절 뒤 값 그대로인 바뀐 파일은 둘(Part 6 `public-files.json` `7c9cb35e3374` — `collect_public_files.py`를 다시 돌려도 바이트 같음 · notebook-contracts `1a241f44e4a4` — `verify.py`가 같은 글로 다시 씀).

| 파일 | 마감 전 → 마감 뒤 (sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch24-human-in-the-loop/README.md` | `7c557ad26f23` → `706f760bf507` | 전체 다시 씀(검토 A-11·B-15) |
| 노트북 01·02·03 | `9f25361bad4a`·`5391d97bb170`·`e7649d5a0cbd` → `a7476f9b1939`·`ba886affdc8c`·`9b5508ddc851` | 마크다운만(코드·출력·`executed_at` 그대로) |
| `labs/part6/continuity-guide.md` | `2bc2cadc9465` → `149a572a8f5f` | Ch 24 줄 가운데 칸 |
| `textbook/downloads/part6-practice.zip` | `61119a820068` → `edd8c3be1179` | `_build_index.py`(마지막 한 번) |
| 챕터 `qa/public-files.json` | `c72eba466843` → `6efdb7328104` | 옛 SVG 세 줄 뺌 |
| 챕터 `qa/research.md` · `qa/verification.md` · `집필점검표.md` | `931d3d2953fd`·`d4cefae849a1`·`a0b1c726e78f` → 바뀜 | 「개선 전 판」 표시 · 마감 절 |
| `textbook/part6/qa/bundle-execution.json` | `f53987e87c1c` → `a72edd8a79a6` | `check_bundle_execution.py`(Ch 24 01 새 `code_sha256`) |
| `textbook/part6/qa/integration-results.json` | `fa46898a97f4` → `a9661d7ce9af` | `_build_index.py` |
| `textbook/part6/qa/visual-results.json` | `367e23e38891` → `dd444465a790` | Ch 24 줄만 8 → 10(`screens` 120 → 122) |
| `textbook/_notebook/checks/ch24-human-in-the-loop/visual-results.json` | `0faea55cd02f` → `d08c55cac953` | `visual.cjs` 10행 PASS |
| `textbook/part6/index.html` · 챕터 `index.html` | `afe83bc7dede`·`bd3554a12c2f` → `a183814b4655`·`316526ca4da3` | 목차 설명 줄 · `objectives` |
| 01·02·03 `_src` · 01·02·03 HTML | `5960408bb949`·`156ccab74aa2`·`aa00400d83e3` / `09f46b30fd0c`·`8f502dfb2938`·`421d2df7e1f0` → `d6e23d6b125f`·`5cd91c9750a0`·`21e32cafb22c` / `c697272fae9a`·`f556f9c10988`·`6df786ec2705` | 검토 반영 글(`--src-only` → `--no-exec`) |
| `textbook/part6/_build_index.py` | `036fbdd244e3` → `5ffb7dde372c` | ch24 설명 한 줄 |
| `chapter.json` | `1ee64948471d` → `40a6a389df76` | `objectives` 넷 |
| `textbook/part6/ch23-persistence/qa/upgrade/chapter-summary.md` | 원본 그대로 → `4c2a10fd3ec6` | 챕터 밖 — §16 1번에 공용 옛 생성기 이동 한 줄(과제 지시) |
| **옮김** `figures/_gen_figures.py` | `2a015c6ada60` → `qa/upgrade/before/generators/blocked/_gen_figures.py`(같은 해시) | 규격 §8 |
| **옮김** `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py` | `3fc72dedb865` → `ch23-persistence/qa/upgrade/before/generators/blocked/author_ch23_ch24.py`(같은 해시) | 공용 옛 생성기 — Ch 23·24 모두 마감 |

- **목록 밖이지만 바뀐 것**: 생성기 `author_01~04.py`(`0eb074b18134`·`e3699a921d1b`·`d2c014669b12`·`20930d1a57b7` → `87373befbd5b`·`fab9a528410e`·`7f3006cdfa3f`·`dbfbffb38b3d`) · 노트북 04(`089ed8d9e413` → `c78b1a2d45e3`, 마크다운만) · `_src/04`·HTML 04 · 그림 `03-3`·`04-2`·`04-3`(`.mmd`·`.svg`·`.png`·`.render.json`) · 캡션 파일 `02-3`·`03-4`·`03-5` · `01-5`·`03-5` `.prompt.md` · 진단 넷·설계표 넷 끝 「마감 반영」 · `gates-wip-01~04.json`(`--no-exec`가 다시 씀, 값 0) · `handoff.md`. 새 파일: `chapter-summary.md`·`gates-after.json`. 도구 파일 `approval_tools.py`는 **그대로**(`d562c9e67c56…`).

