# 보호 파일 해시 변경 기록 (`before-manifest.json` 73개 기준)

## 01절 끝 (2026-09-25)

73개 가운데 **69개 같음 · 4개 바뀜**. 바뀐 넷은 모두 의도한 것입니다.

| 파일 | 전 | 후 | 까닭 |
|---|---|---|---|
| `textbook/part6/_author_ch21_ch29.py` | `1d3d1dc9…` | `650f6506936f8c3660f6973d542d2b5d730c87354861ca704605a8c41167027a` | 공용 옛 생성기(Ch 21·Ch 29). 머리 주석 세 줄 + `write_chapter()` 첫머리에 `if chapter == 21:` 건너뛰기 세 줄(챕터 리드 결정 9). 사본 `/tmp/ch21-01/gentest/`에서 옛 판·새 판을 돌려 **Ch 29 쪽 산출(chapter.json·노트북 넷·`_src` 넷)이 바이트까지 같고 Ch 21 쪽은 하나도 쓰지 않음**을 확인 |
| `textbook/part6/public-files.json` | `50531719…` | `c6c7137f21a845c30293006e4cce56dcc5cd00f4869d723f09de702a99ee0bb4` | 도구 파일 `labs/part6/ch21-create-agent/notebooks/runner_tools.py` 한 줄(06 노트북 줄 뒤, 이름 차례). 그 줄을 빼고 같은 형식으로 다시 쓰면 옛 해시와 같음 |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | `72b1792e…` | `2c7c8fa8830add06d6478a3cbd829665554cb50bbfed4b15751524c66c043293` | 같은 한 줄(경로 배열). 그 줄을 빼면 옛 해시와 같음 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `17a5d369…` | `1e0c83f3c116…` | `verify.py --chapter`가 실행마다 다시 씀(Ch 20 선례와 같은 기록 파일) |

- Ch 22 01·02 `_src`·01 HTML·01 노트북, Ch 29 04 노트북·`_src`, Ch 20 파일, `rag-comparison.json`, `part6-practice.zip`·`llm-practice.zip`, 실습 폴더 `pyproject.toml`·`uv.lock`, 검사·빌드 스크립트는 그대로입니다.
- 목록 밖에서 이 절이 만든·바꾼 파일은 `01-diagnosis.md` §10에 있습니다.

## 02절 끝 (2026-09-25)

73개 가운데 **69개 같음 · 4개 바뀜** — 01절 끝과 같은 넷이고, 02절이 새로 바꾼 보호 파일은 **기록 파일 하나**뿐입니다.

| 파일 | 01절 끝 | 02절 끝 | 까닭 |
|---|---|---|---|
| `textbook/part6/_author_ch21_ch29.py` | `650f6506…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/public-files.json` | `c6c7137f…` | 같음 | 01이 바꾼 뒤 그대로(도구 파일 줄은 01이 이미 올림) |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | `2c7c8fa8…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `1e0c83f3…` | `4fa11281cbc3b50d58967e701726626d619b2c223138828f9eaca352820d1903` | `verify.py --chapter`가 실행마다 다시 씀(기록 파일) |

- 목록 밖이지만 뒤 절·묶음이 읽는 파일: 도구 파일 `labs/part6/ch21-create-agent/notebooks/runner_tools.py` `eb408639…` → `ab31d0c1ef7b4b89a63a8fcf843d21f3ee7feff311afe7ecbb86d6c007f32621`(`agent_row` 더함 — `handoff.md` 해시 변천). `part6-practice.zip` 안 판은 옛 판(묶음 재생성은 마감 몫).
- Ch 22·Ch 26·Ch 29·Ch 30 파일, Ch 20 파일, `rag-comparison.json`, `part6-practice.zip`·`llm-practice.zip`, 실습 폴더 `pyproject.toml`·`uv.lock`, 검사·빌드 스크립트는 그대로입니다.

## 03절 끝 (2026-09-25)

73개 가운데 **69개 같음 · 4개 바뀜** — 01·02절 끝과 같은 넷이고, 03절이 새로 바꾼 보호 파일은 **기록 파일 하나**뿐입니다.

| 파일 | 02절 끝 | 03절 끝 | 까닭 |
|---|---|---|---|
| `textbook/part6/_author_ch21_ch29.py` | `650f6506…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/public-files.json` | `c6c7137f…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | `2c7c8fa8…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `4fa11281…` | `4d673fe9a4f2758db57a496037602bc9fb5f5dc4614a44818d98cffe3a390ec0` | `verify.py --chapter`가 실행마다 다시 씀(기록 파일) |

- 목록 밖이지만 뒤 절·묶음이 읽는 파일: 도구 파일 `labs/part6/ch21-create-agent/notebooks/runner_tools.py` `ab31d0c1…` → `6ce7a8d29a2f96a9aa48d61ace68811932920f0d69fa3b758962809c39770471`(`print_branches` 더함 — `handoff.md` 해시 변천). `part6-practice.zip` 안 판은 옛 판(묶음 재생성은 마감 몫).
- Ch 22·Ch 29·Ch 30 파일, Ch 20 파일, `rag-comparison.json`, `part6-practice.zip`·`llm-practice.zip`, 실습 폴더 `pyproject.toml`·`uv.lock`, 검사·빌드 스크립트는 그대로입니다.

## 04절 끝 (2026-09-25)

73개 가운데 **69개 같음 · 4개 바뀜** — 01~03절 끝과 같은 넷이고, 04절이 새로 바꾼 보호 파일은 **기록 파일 하나**뿐입니다.

| 파일 | 03절 끝 | 04절 끝 | 까닭 |
|---|---|---|---|
| `textbook/part6/_author_ch21_ch29.py` | `650f6506…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/public-files.json` | `c6c7137f…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | `2c7c8fa8…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `4d673fe9…` | `8bd0846580a08d41de2306854a850c99844442161160df986b10da030552a677` | `verify.py --chapter`가 실행마다 다시 씀(기록 파일) |

- 목록 밖이지만 뒤 절·묶음이 읽는 파일: 도구 파일 `labs/part6/ch21-create-agent/notebooks/runner_tools.py`는 **바꾸지 않음**(`6ce7a8d2…` 그대로). `chapter.json`은 04 제목 글자 하나만 바뀜(`f163836b…` — 보호 목록 밖, 챕터 파일). `textbook/part6/index.html`(보호 목록 안)은 다시 만들지 않아 **같음**(옛 제목 글자 그대로 — 마감 때 `_build_index.py`).
- Ch 14·Ch 22·Ch 29·Ch 30 파일, Ch 20 파일, `rag-comparison.json`, `part6-practice.zip`·`llm-practice.zip`, 실습 폴더 `pyproject.toml`·`uv.lock`, 검사·빌드 스크립트는 그대로입니다.

## 05절 끝 (2026-09-25)

73개 가운데 **69개 같음 · 4개 바뀜** — 01~04절 끝과 같은 넷이고, 05절이 새로 바꾼 보호 파일은 **기록 파일 하나**뿐입니다.

| 파일 | 04절 끝 | 05절 끝 | 까닭 |
|---|---|---|---|
| `textbook/part6/_author_ch21_ch29.py` | `650f6506…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/public-files.json` | `c6c7137f…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | `2c7c8fa8…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `8bd08465…` | `cb9db81faf515372d429a65aba09fbfa459e0416e7343a64d9a29c4404dbd427` | `verify.py --chapter`가 실행마다 다시 씀(기록 파일) |

- **Ch 14 보호 파일 셋은 같음**: `documents.json` `d54899d9…` · `queries.json` `abdbb041…` · `rag_tools.py` `868a653e…`(노트북은 읽기만, 노트북 밖 확인은 `rag_tools.py`를 `sys.dont_write_bytecode`로 가져오기만 — Ch 14 `notebooks/__pycache__/` 시각도 그대로 2026-09-21).
- 목록 밖이지만 뒤 절·묶음이 읽는 파일: 도구 파일 `labs/part6/ch21-create-agent/notebooks/runner_tools.py` `6ce7a8d2…` → `8538fedb9943a783183958eb0ef3de619a73762c4735b3576c80681efd911eda`(검색 함수 다섯 + `import numpy as np` — `handoff.md` 해시 변천). `part6-practice.zip` 안 판은 옛 판(묶음 재생성은 마감 몫). `rag-comparison.json`(`122cfce2…`)은 05가 쓰지 않아 같음(06이 다시 씀).
- Ch 22·Ch 29·Ch 30 파일, Ch 20 파일, `part6-practice.zip`·`llm-practice.zip`, 실습 폴더 `pyproject.toml`·`uv.lock`, 검사·빌드 스크립트는 그대로입니다.

## 06절 끝 (2026-09-25)

73개 가운데 **68개 같음 · 5개 바뀜** — 01~05절 끝과 같은 넷에 더해, 06절이 **계약 파일 하나를 의도해서 다시 씀**(기록 파일도 다시 씀).

| 파일 | 05절 끝 | 06절 끝 | 까닭 |
|---|---|---|---|
| `textbook/part6/_author_ch21_ch29.py` | `650f6506…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/public-files.json` | `c6c7137f…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | `2c7c8fa8…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `cb9db81f…` | `a5d1415d5e2629c733848d79b0382f7a0b8874b4607bdac7302818ffa6004b08` | `verify.py --chapter`가 실행마다 다시 씀(기록 파일) |
| **`labs/part6/ch21-create-agent/data/rag-comparison.json`** | `122cfce2…`(옛 판, 사본 `before/data/`) | **`25cfe5df3cfd729c130bce4af26c716cfcc3bcd4b4ff6e4a9d0a725816b02f51`** | **의도한 변경** — 06 노트북 A 실행이 새 판으로 씀(줄 셋·Ch 29 04가 읽는 칸 그대로, `fixed_latency_s` 뺌). Ch 29 04 읽기 코드·`assert` 셋 흉내 검사 PASS, 인용값 519.7·1.880·2.094·541 → 688·1.731·2.003·699(Ch 29 몫, `06-diagnosis.md` §6). B 실행은 `/tmp/ch21-06/Broot` 아래에 써 이 파일을 건드리지 않음 |

- **Ch 14·Ch 15 보호 파일은 같음**: `documents.json` `d54899d9…` · `queries.json` `abdbb041…` · Ch 14 `rag_tools.py` `868a653e…` · Ch 15 `rag_tools.py` `6c59d0f2…`(노트북은 읽기만, 노트북 밖 확인은 둘 다 `sys.dont_write_bytecode`로 가져오기만 — Ch 14·15 `__pycache__/` 시각 그대로). Part 6 선행 목록 둘(`textbook/part6/prerequisite-files.json`·Ch 29 `qa/prerequisite-files.json`)은 경로만 적어 그대로.
- 목록 밖이지만 뒤 절·묶음이 읽는 파일: 도구 파일 `labs/part6/ch21-create-agent/notebooks/runner_tools.py` `8538fedb…` → `f4113158c0ccaee1205f0eabe315ef153e14c4dc6bcfd70ae8a9378edda96bdf`(`import json` + 함수 셋 — `handoff.md` 해시 변천). `part6-practice.zip` 안 판은 옛 판(마감 몫).
- Ch 22·Ch 29·Ch 30 파일, Ch 20 파일, `part6-practice.zip`·`llm-practice.zip`, 실습 폴더 `pyproject.toml`·`uv.lock`·README, 검사·빌드 스크립트는 그대로입니다.

## 07절 끝 (2026-09-25, 챕터 끝 실습 절 새로 만듦)

73개 가운데 **65개 같음 · 8개 바뀜** — 06절 끝까지의 다섯에 더해, 07절이 **지시대로 `python3 textbook/part6/_build_index.py`를 한 번 돌려** Part 6 목차·묶음·통합 기록 셋이 바뀜(기록 파일도 다시 씀).

| 파일 | 06절 끝 | 07절 끝 | 까닭 |
|---|---|---|---|
| `textbook/part6/_author_ch21_ch29.py` | `650f6506…` | 같음 | 01이 바꾼 뒤 그대로 |
| `textbook/part6/public-files.json` | `c6c7137f…` | 같음 | 01이 바꾼 뒤 그대로(07 줄은 **더하지 않음** — 마감 몫) |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | `2c7c8fa8…` | 같음 | 01이 바꾼 뒤 그대로(명시 목록 — 07 노트북·HTML 줄은 마감 몫) |
| `labs/part6/ch21-create-agent/data/rag-comparison.json` | `25cfe5df…` | **같음** | 07은 읽지도 쓰지도 않음 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `a5d1415d…` | `71f81c16bb74e53e1b4eaf68588378c4e30c66383b2ea150888029e695d6dfe7` | `verify.py --chapter`가 실행마다 다시 씀(기록 파일) |
| **`textbook/part6/index.html`** | `a606f921…` | `32fbf36e8ab0467c755413bda060d5ddc0bbfa2c81474e541f8c899a2d854011` | `_build_index.py` — Ch 21 「7절」·07 링크·04 새 제목 글자 |
| **`textbook/downloads/part6-practice.zip`** | `0543ea63…` | `278766340335be21d8bf93a5b1fe5a98736428d7e5b6b8ab856e3c23638fe17b` | `_build_index.py` — 07 노트북·06 새 노트북·도구 파일 `f4113158…`·계약 파일 `25cfe5df…`·README 새 판이 들어감(`Part 6: 49 verified sections; 94 bundled files`) |
| **`textbook/part6/qa/integration-results.json`** | `8be394e0…` | `119d32c666124fde03c9d16c33e7f46d32f2e05ffb592b76afa0b52477eaba47` | `_build_index.py`가 함께 씀 |

- `llm-practice.zip`(`check_delivery.py`가 Part 1 항목에서 Stale로 멈춤 — 알려진 일)·`textbook/index.html`·`build_index.py`·`_build_index.py`·검사 스크립트·Ch 14·15·20·22·29·30 파일은 그대로입니다.
- 목록 밖이지만 뒤 절·묶음이 읽는 파일: 도구 파일 `runner_tools.py` `f4113158…` **그대로** · 06 노트북 `768d4f9e…` **그대로**(`code_sha256` `ca14949bb0f9…`·`outputs_sha256` `1ded374d9f64…`) · `chapter.json` `f163836b…` → `67d7c5e2…`(07절 추가, `hours`·`objectives` 그대로 — 보호 목록 밖).

## 챕터 마감 끝 (2026-09-25, 검토 반영·마감 담당)

73개 가운데 **60개 같음 · 13개 바뀜** — 07절 끝의 여덟(그 가운데 목록·묶음·목차·통합 기록·기록 파일은 마감에서 다시 바뀜)에 더해, 마감이 **다섯을 새로 바꿈**. 모두 의도한 것입니다.

| 파일 | 07절 끝 | 마감 끝 | 까닭 |
|---|---|---|---|
| `textbook/part6/_author_ch21_ch29.py` | `650f6506…` | 같음 | 01이 바꾼 뒤 그대로(옮기지 않음 — Ch 29가 씀) |
| `labs/part6/ch21-create-agent/data/rag-comparison.json` | `25cfe5df…` | **같음** | 06은 다시 실행하지 않음(Ch 29 04 계약, 흉내 검사 PASS) |
| `textbook/part6/public-files.json` | `c6c7137f…` | `cf2fb079d315f08e…` | 검토 A-14 — 챕터 목록 둘에 줄을 더한 뒤 `collect_public_files.py`로 다시 모음: `labs/part6/ch21-create-agent/notebooks/07-create-agent-실습.ipynb`·**`labs/part6/ch22-middleware/notebooks/09-Middleware-실습.ipynb`** 두 줄만 늘어남(선행 목록 `prerequisite-files.json`은 바이트까지 같음) |
| `textbook/part6/ch21-create-agent/qa/public-files.json` | `2c7c8fa8…` | `cf882fbd42617ff7…` | 07 HTML·07 노트북 두 줄 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `71f81c16…` | `b8a4f9123f90c398…` | `verify.py --chapter`(기록 파일) |
| `textbook/part6/index.html` | `32fbf36e…` | `c465e7b42c27ab6a…` | `_build_index.py` — 01·03 제목 밑줄, Ch 21 설명 새 줄 |
| `textbook/downloads/part6-practice.zip` | `27876634…` | `3755de3d15b36c8d…` | `_build_index.py` — 01~07 노트북 새 판·README 새 판·Ch 22 01 노트북 새 판(97항목, 디스크와 모두 같음) |
| `textbook/part6/qa/integration-results.json` | `119d32c6…` | `e539f6d25a1252f1…` | `_build_index.py`가 함께 씀 |
| **`textbook/part6/_build_index.py`** | `882eda82…` | `9e130bd434e4187f…` | Ch 21 설명 줄만(시수 6·10 그대로) |
| **`textbook/part6/qa/bundle-execution.json`** | `d6e1ba96…` | `2a3bed108e11ed8e…` | `check_bundle_execution.py`(Ch 24 01·Ch 28 01 PASS, 새 zip 해시) — 환경 변수만 줌 |
| **`textbook/part6/qa/visual-results.json`** | `402e57e0…` | `eec79f55672db8c1…` | Ch 21 줄만 새 `visual.cjs` 결과로(14 → 16줄, `screens` 116 → 118). 다른 챕터 줄 그대로 |
| **`textbook/part6/ch22-middleware/01-미들웨어와-6개-훅.html`** | `801711e9…` | `413b07b00c7e…` | 검토 A-10(챕터 리드 결정) — Ch 22 01 노트북 설명 셀 한 문장을 훅 함수로 한정, Ch 22 `_build.py`로 다시 빌드(다른 Ch 22 HTML·`_src/01` 바이트까지 같음) |
| **`labs/part6/ch22-middleware/notebooks/01-미들웨어와-6개-훅.ipynb`** | `885379d3…` | `fc953e9cc56c…` | 같은 문장(마크다운만 — `code_sha256` `138108940422…`·`outputs_sha256` `50baad1054f4…`·`executed_at` 그대로) |

- 그대로인 보호 파일 60개: 실습 폴더 `pyproject.toml`·`uv.lock`, Ch 14·15·17·19·20 파일, Ch 22 `_src/01`·`_src/02`, Ch 27·29·30 파일, Part 6 선행 목록 둘, `llm-practice.zip`, `textbook/index.html`, `build_index.py`·`build_bundle.py`·`verify.py`·`builder.py`, 옛 검사 스크립트(`notebook-readiness.json`은 옛 검사가 먼저 써서 실행 전 사본으로 되돌림), `final-artifact-hashes.json`·`existing-artifact-hashes.json` 등.
- 목록 밖 챕터 밖 수정(보호 목록에 없음): `textbook/part6/ch22-middleware/qa/upgrade/author_upgrade.py`(같은 문장) · `textbook/part6/ch22-middleware/qa/public-files.json`(09 HTML·노트북 두 줄) · `textbook/_notebook/checks/ch21-create-agent/visual-results.json`(+ 스크린숏) · `textbook/qa/upgrade-progress.md`(Ch 21 행) · `textbook/qa/upgrade-final-checklist.md`(Ch 21 몫) — 요약 `chapter-summary.md` §10.
