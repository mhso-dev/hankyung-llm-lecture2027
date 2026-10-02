# 보호 파일 변경 기록 (`before-manifest.json` 217개 대조)

준비 담당이 만든 `qa/upgrade/before-manifest.json`(217개, `4aa29f63…`)의 sha256과 절 작업 뒤 디스크를 대조한 기록입니다. 없어진 파일은 0개입니다.

## 01절 뒤 (2026-09-29)

바뀐 파일 **10개**(모두 01절 작업의 예정된 결과, 나머지 207개 같음, 없어진 것 0):

| 파일 | 전 → 후(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch29-agent-evaluation/_src/01-에이전트-평가-세-전략.html` | `8bf41a94` → `228234ba` | 01절 본문 다시 씀(`author_01.py`) |
| `textbook/part6/ch29-agent-evaluation/01-에이전트-평가-세-전략.html` | `6fb8d298` → `9fc60c2f` | `_build.py` 빌드(02~04·`index.html`은 해시 그대로) |
| `labs/part6/ch29-agent-evaluation/notebooks/01-에이전트-평가-세-전략.ipynb` | `d95e84d2` → `debd4640` | 01절 노트북 다시 씀 + 새 커널 실행(A) + 그림 첨부 + 「오늘 볼 그림」 alt 한 곳 마크다운만 옮김(`code_sha256` `6ed13ca33e52…` → **`b7a67c68540b3d0f7c890a582aaaa30ad7c5e28398435919f37bf12567c11537`**, 코드 셀 5 → 23 — Ch 29는 묶음 실행 검사 목록 밖) |
| `textbook/part6/ch29-agent-evaluation/qa/public-files.json` | `7c28818f` → `57815fa5` | 도구 파일 줄 `labs/part6/ch29-agent-evaluation/notebooks/eval_tools.py` 하나 더함(규격 §2-7 6번) |
| `textbook/part6/public-files.json` | `498845c7` → `e0052b91` | `textbook/part6/qa/collect_public_files.py`로 다시 모음 — 도구 파일 한 줄만 늘어남(`Explicit public files: 92` → `93`, `prerequisites: 13` 그대로, `prerequisite-files.json` `4c7f5a4b…` 바이트 같음). **`part6-practice.zip`은 다시 만들지 않음(마감 몫)** |
| `textbook/part6/_author_ch21_ch29.py`(공용 옛 생성기) | `650f6506` → `391be055` | 옛 생성기 막기 — Ch 21 설명 주석 뒤에 설명 주석 셋 + `raise SystemExit(...)`, Ch 21 건너뛰기 조건(`write_chapter`)은 그대로. 원본 사본 `qa/upgrade/before/generators/_author_ch21_ch29.py`(`650f6506…`)와 `diff` — 더한 줄 넷뿐 |
| `textbook/part6/ch29-agent-evaluation/figures/_gen_figures.py` | `65b435f8` → `3577112d` | 옛 도식 생성기 막기(설명 주석 셋 + `raise SystemExit`), 원본 사본 `before/generators/_gen_figures.py`와 `diff` — 더한 줄 넷뿐 |
| `textbook/part6/ch29-agent-evaluation/집필점검표.md` | `1e914c7c` → `1c58bcaf` | 「품질 개선」 표(01 행) 덧붙임 — 위 옛 기록은 그대로 |
| `textbook/part6/ch29-agent-evaluation/qa/verification.md` | `52d03d42` → `0f5e4c98` | 「품질 개선 검증」 표(01 행) 덧붙임 — 위 옛 기록은 그대로 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` | `f2c0141a` → `6201b897` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **바뀌지 않은 것(확인)**: 계약 두 파일 — Ch 21 `data/rag-comparison.json`(`25cfe5df…`)·Ch 18 06 노트북(`5ba7f5a0…`) · Ch 18 `workflow_tools.py` · Ch 21 `runner_tools.py`(`f4113158…` — 도구 파일 원본, 읽기만) · Ch 27 `harness_tools.py`(`7a40d994…`)·Ch 28 `connect_tools.py`(`570ed3cc…`) — 대조만 · `chapter.json`·`index.html`·`_build.py` · 02~04 `_src`·HTML·노트북 · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · `part6-practice.zip`(`5002dce3…`)·`llm-practice.zip` · Ch 28 06·Ch 17 04·Ch 21 06 원고 · `.moai/…/part6b_enrich.py`(`8528cb33…`)·`part6b_review_fixes.py`(`a0299166…`) — 실행·수정 안 함.
- 새로 생긴 파일(목록 밖): `labs/part6/ch29-agent-evaluation/notebooks/eval_tools.py`(`dab0888f…`, 도구 파일 첫 판) · `qa/upgrade/author_01.py`·`01-figures.md`·`01-diagnosis.md`·`handoff.md`·`manifest-changes.md`·`gates-wip-01-01.json`·`gates-wip-01.json`·`review-pack/01-…md` · `figures/01-1~01-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/01-5-오르골-종이띠.{png,prompt.md,caption.md}` · 사용자 디스크 `.cache/ch29-01-view/illu-1-1100.png`(삽화 확인 사본).
- 노트북 실행은 모두 `PYTHONDONTWRITEBYTECODE=1`로 해서 실습 폴더 `notebooks/__pycache__`가 생기지 않았습니다(확인). `.failure.json`도 생기지 않았습니다.

## 02절 뒤 (2026-09-29)

`before-manifest.json` 217개 대조: 바뀐 파일 **13개**(01절 뒤 10개 + 02절 새 3개), 나머지 204개 같음, 없어진 것 0. 01절 뒤 10개 가운데 7개는 01 기록 해시 그대로, 셋은 02절 작업으로 다시 바뀜.

| 파일 | 01절 뒤 → 02절 뒤(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch29-agent-evaluation/_src/02-궤적-매칭-네-모드.html` | `f24afc79`(목록 값) → `65d77f15` | 02절 본문 다시 씀(`author_02.py`) |
| `textbook/part6/ch29-agent-evaluation/02-궤적-매칭-네-모드.html` | `9aa592e5`(목록 값) → `62822dcf` | `_build.py` 빌드(01·03·04·`index.html`은 해시 그대로 — 01 HTML `9fc60c2f`는 01 기록 값) |
| `labs/part6/ch29-agent-evaluation/notebooks/02-궤적-매칭-네-모드.ipynb` | `a1bd4160`(목록 값) → `abdd6dc3` | 02절 노트북 다시 씀 + 새 커널 실행(A) + 그림 첨부 + 「오늘 볼 그림」 alt 한 곳 마크다운만 옮김(`code_sha256` `c2807667e2b7…` → **`8e80cc8d5a270839969513d3c83a343fd83e9ab4587208299c3a23aa6067682a`**, 코드 셀 5 → 27 — Ch 29는 묶음 실행 검사 목록 밖) |
| `textbook/part6/ch29-agent-evaluation/집필점검표.md` | `1c58bcaf` → `3798990a` | 「품질 개선」 표에 02 행 덧붙임(위 기록·01 행 그대로) |
| `textbook/part6/ch29-agent-evaluation/qa/verification.md` | `0f5e4c98` → `f527e61b` | 「품질 개선 검증」 표에 02 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` | `6201b897` → `b1cb3a55` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **01 기록 해시 그대로(7)**: 01 `_src`(`228234ba`)·01 HTML(`9fc60c2f`)·01 노트북(`debd4640` — 다시 실행하지 않음)·챕터 `qa/public-files.json`(`57815fa5`)·Part `public-files.json`(`e0052b91`)·공용 옛 생성기(`391be055`)·`figures/_gen_figures.py`(`3577112d`).
- **목록 밖(01이 만든 새 파일)**: 도구 파일 `labs/part6/ch29-agent-evaluation/notebooks/eval_tools.py` `dab0888f…`(01판) → **`4a3d81431a29d0a62d33e13766f0c57652a85fd5a4e87de6e7df9bfc9a1e58bf`**(02판 — 01 셀 셋 + 가져오기 줄 `langchain.messages`, 대조 사슬 `author_02.check_tools`). 공개 목록 줄은 01이 이미 올림(바꾸지 않음).
- **바뀌지 않은 것(확인)**: 계약 두 파일 — Ch 21 `data/rag-comparison.json`(`25cfe5df…`)·Ch 18 06 노트북(`5ba7f5a0…`) · `chapter.json`·`index.html`·`_build.py` · 03·04 `_src`·HTML·노트북 · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · `part6-practice.zip`(`5002dce3…`)·`llm-practice.zip` · Ch 17 04·Ch 19·Ch 21 06·Ch 28 06 원고 · `.moai/…/part6b_enrich.py`·`part6b_review_fixes.py`(실행·수정 안 함).
- 새로 생긴 파일(목록 밖): `qa/upgrade/author_02.py`·`02-figures.md`·`02-diagnosis.md`·`gates-wip-02-02.json`·`gates-wip-02.json`·`review-pack/02-궤적-매칭-네-모드.md` · `figures/02-1~02-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/02-5-기준-띠에-대-보기.{png,prompt.md,caption.md}` · 사용자 디스크 `.cache/ch29-02-view/illu-1-1100.png`(삽화 확인 사본). `handoff.md`·이 파일은 덧붙임.
- 노트북 실행은 모두 `PYTHONDONTWRITEBYTECODE=1`로 해서 실습 폴더 `notebooks/__pycache__`·챕터 `qa/upgrade/__pycache__`가 생기지 않았습니다(확인). `.failure.json`도 생기지 않았습니다.

## 03절 뒤 (2026-09-29)

`before-manifest.json` 217개 대조: 바뀐 파일 **16개**(02절 뒤 13개 + 03절 새 3개), 나머지 201개 같음, 없어진 것 0. 02절 뒤 13개 가운데 10개는 02 기록 해시 그대로, 셋은 03절 작업으로 다시 바뀜.

| 파일 | 02절 뒤 → 03절 뒤(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch29-agent-evaluation/_src/03-LLM-judge로-궤적-평가.html` | `c1ffadca`(목록 값) → `1732be10` | 03절 본문 다시 씀(`author_03.py`) |
| `textbook/part6/ch29-agent-evaluation/03-LLM-judge로-궤적-평가.html` | `16b17a74`(목록 값) → `d5a0ac5f` | `_build.py` 빌드(01 `9fc60c2f`·02 `62822dcf`·04·`index.html`은 해시 그대로) |
| `labs/part6/ch29-agent-evaluation/notebooks/03-LLM-judge로-궤적-평가.ipynb` | `72324f31`(목록 값) → `41e79afe` | 03절 노트북 다시 씀 + 새 커널 실행(A, 모델 요청 5) + 그림 첨부 + 마크다운만 옮김(`code_sha256` `0bc0530051bb…` → **`c38454ecf35a06fde9d4ea3655c4a1149fa589c4ac33631359b6787a551d3593`**, 코드 셀 5 → 28 — Ch 29는 묶음 실행 검사 목록 밖) |
| `textbook/part6/ch29-agent-evaluation/집필점검표.md` | `3798990a` → `65e468e4` | 「품질 개선」 표에 03 행 덧붙임(위 기록·01·02 행 그대로) |
| `textbook/part6/ch29-agent-evaluation/qa/verification.md` | `f527e61b` → `e3214f53` | 「품질 개선 검증」 표에 03 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` | `b1cb3a55` → `7fbda8ee` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **02 기록 해시 그대로(10)**: 01·02 `_src`(`228234ba`·`65d77f15`)·01·02 HTML(`9fc60c2f`·`62822dcf`)·01·02 노트북(`debd4640`·`abdd6dc3` — 다시 실행하지 않음, 사본에서 03판 도구 파일로 23/23·27/27 같음)·챕터 `qa/public-files.json`(`57815fa5`)·Part `public-files.json`(`e0052b91`)·공용 옛 생성기(`391be055`)·`figures/_gen_figures.py`(`3577112d`).
- **목록 밖(01이 만든 새 파일)**: 도구 파일 `labs/part6/ch29-agent-evaluation/notebooks/eval_tools.py` `4a3d8143…`(02판) → **`617a82bc44fcba03823a30aa551fd519deb4cac368b499160259f933453cf0bf`**(03판 — 02 셀 `four_modes` + Ch 21 `sum_usage`·`estimate_cost`, 가져오기 줄 그대로, 대조 사슬 `author_03.check_tools`). 공개 목록 줄은 01이 이미 올림(바꾸지 않음).
- **바뀌지 않은 것(확인)**: 계약 두 파일 — Ch 21 `data/rag-comparison.json`(`25cfe5df…`)·Ch 18 06 노트북(`5ba7f5a0…`) · Ch 21 `runner_tools.py`(`f4113158…` — 원본, 읽기만)·Ch 26 `delegation_tools.py`·Ch 27 `harness_tools.py`(`7a40d994…`)·Ch 28 `connect_tools.py`(`570ed3cc…`) — 대조만 · `chapter.json`·`index.html`·`_build.py` · 04 `_src`·HTML·노트북 · 실습 폴더 `README.md`·`pyproject.toml`·`uv.lock` · `part6-practice.zip`(`5002dce3…`)·`llm-practice.zip` · Ch 15·19·20·21·22·27·28 원고 · `.moai/…/part6b_enrich.py`·`part6b_review_fixes.py`(실행·수정 안 함).
- 새로 생긴 파일(목록 밖): `qa/upgrade/author_03.py`(`db5aa8fb…`)·`03-probe.md`·`probe/probe03.py`(`591041d9…`)·`probe/probe-03-A.jsonl`(`5b1a6b73…`)·`03-figures.md`·`03-diagnosis.md`·`gates-wip-03-03.json`·`gates-wip-03.json`·`review-pack/03-LLM-judge로-궤적-평가.md` · `figures/03-1~03-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/03-5-겹쳐-보기와-울려-보기.{png,prompt.md,caption.md}` · 사용자 디스크 `.cache/ch29-03-view/illu-1-1100.png`(삽화 확인 사본). `handoff.md`·이 파일은 덧붙임.
- 노트북 실행은 모두 `PYTHONDONTWRITEBYTECODE=1`로 해서 실습 폴더 `notebooks/__pycache__`·챕터 `qa/upgrade/__pycache__`가 생기지 않았습니다(확인). `.failure.json`도 생기지 않았습니다.

## 04절 뒤 (2026-09-29)

`before-manifest.json` 217개 대조: 바뀐 파일 **19개**(03절 뒤 16개 + 04절 새 3개), 나머지 198개 같음, 없어진 것 0. 03절 뒤 16개 가운데 13개는 03 기록 해시 그대로, 셋은 04절 작업으로 다시 바뀜.

| 파일 | 03절 뒤 → 04절 뒤(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch29-agent-evaluation/_src/04-운영-지표와-Ch18-궤적-비교.html` | `ec34bf6e`(목록 값) → `fd2bf9c9` | 04절 본문 다시 씀(`author_04.py`) |
| `textbook/part6/ch29-agent-evaluation/04-운영-지표와-Ch18-궤적-비교.html` | `f39bbffe`(목록 값) → `1305131f` | `_build.py` 빌드(01 `9fc60c2f`·02 `62822dcf`·03 `d5a0ac5f`·`index.html` `934283ad`는 해시 그대로) |
| `labs/part6/ch29-agent-evaluation/notebooks/04-운영-지표와-Ch18-궤적-비교.ipynb` | `b8c1b9d2`(목록 값) → `3c1c41fd` | 04절 노트북 다시 씀 + 새 커널 실행(A, 모델 요청 0) + 그림 첨부(`code_sha256` `0c6de54fd899…` → **`43163e6ac114234793831530166a668892bea76d7d77c5f3e168861b02054457`**, 코드 셀 9 → 25 — Ch 33 `regression-baseline.json`의 출처 해시 `71fa56ef…`와는 이미 달랐음, 확인 코드 없음) |
| `textbook/part6/ch29-agent-evaluation/집필점검표.md` | `65e468e4` → `8fcf2bdd` | 「품질 개선」 표에 04 행 덧붙임(01~03 행 그대로) |
| `textbook/part6/ch29-agent-evaluation/qa/verification.md` | `e3214f53` → `34de337d` | 「품질 개선 검증」 표에 04 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` | `7fbda8ee` → `49dc8ded` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **03 기록 해시 그대로(13)**: 01~03 `_src`(`228234ba`·`65d77f15`·`1732be10`)·01~03 HTML(`9fc60c2f`·`62822dcf`·`d5a0ac5f`)·01~03 노트북(`debd4640`·`abdd6dc3`·`41e79afe` — 다시 실행하지 않음, 01·02는 사본에서 04판 도구 파일로 23/23·27/27 같음)·챕터 `qa/public-files.json`(`57815fa5`)·Part `public-files.json`(`e0052b91`)·공용 옛 생성기(`391be055`)·`figures/_gen_figures.py`(`3577112d`).
- **계약 파일 둘 그대로(목록 값과 같음)**: Ch 21 `labs/part6/ch21-create-agent/data/rag-comparison.json` **`25cfe5df…`** · Ch 18 `labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb` **`5ba7f5a0…`** — 읽기만(생성기 `check_contracts()`가 매 실행 확인). 원본 대조만 한 파일도 그대로: Ch 15 `06-대화당-비용-백분위수.ipynb`(`b688b514`)·Ch 15 `rag_tools.py`(`6c59d0f2`)·Ch 21 `runner_tools.py`(`f4113158`)·Ch 26~28 도구 파일.
- **목록 밖(01이 만든 새 파일)**: 도구 파일 `labs/part6/ch29-agent-evaluation/notebooks/eval_tools.py` `617a82bc…`(03판) → **`223881ecd08b583b6625f5249122745fbdfec5feb222cf2feda50294f3d1e262`**(04판 — Ch 15 06 노트북 셀 `average`·`nearest_rank` + 가져오기 줄 `import math`, 대조 사슬 `author_04.check_tools`). 공개 목록 줄은 01이 이미 올림(바꾸지 않음).
- **바뀌지 않은 것(확인)**: `chapter.json`(`d84d0a07`)·`index.html`·`_build.py` · 실습 폴더 `README.md`(`e252d099`)·`pyproject.toml`(`5a3ca31c`)·`uv.lock`(`de2416a1`) · `part6-practice.zip`(`5002dce3…`)·`llm-practice.zip` · Ch 18·21·30·33 원고 · `.moai/…/part6b_enrich.py`·`part6b_review_fixes.py`(실행·수정 안 함).
- 새로 생긴 파일(목록 밖): `qa/upgrade/author_04.py`(`370829e4…`)·`04-figures.md`·`04-diagnosis.md`·`gates-wip-04-04.json`·`gates-wip-04.json`·`review-pack/04-운영-지표와-Ch18-궤적-비교.md` · `figures/04-1~04-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/04-5-받침대에-걸린-종이띠.{png,prompt.md,caption.md}` · 사용자 디스크 `.cache/ch29-04-view/illu-1-1100.png`(삽화 확인 사본). `handoff.md`·이 파일은 덧붙임.
- 노트북 실행은 모두 `PYTHONDONTWRITEBYTECODE=1`로 해서 실습 폴더 `notebooks/__pycache__`·챕터 `qa/upgrade/__pycache__`가 생기지 않았습니다(확인). `.failure.json`도 생기지 않았습니다.

## 05절 뒤 (2026-09-29)

`before-manifest.json` 217개 대조: 바뀐 파일 **25개**(04절 뒤 19개 + 05절 새 6개), 나머지 192개 같음, 없어진 것 0. 04절 뒤 19개 가운데 11개는 04 기록 해시 그대로, 여덟은 05절 작업으로 다시 바뀜.

| 파일 | 04절 뒤 → 05절 뒤(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch29-agent-evaluation/chapter.json` | `d84d0a07`(목록 값) → `4e565b61` | **새로 바뀜** — `sections`에 05절(`experiment`) 한 줄, `hours`·`objectives` 그대로 |
| `textbook/part6/ch29-agent-evaluation/index.html` | `934283ad`(목록 값) → `2821043d` | **새로 바뀜** — `_build.py`가 05절 줄을 더함 |
| `textbook/part6/ch29-agent-evaluation/_src/04-운영-지표와-Ch18-궤적-비교.html` | `fd2bf9c9` → `e120a5d4` | b8 「다음 학습과 이어지는 지점」 → 05(`mdpatch.py` + `author_04.py --src-only`, 나머지 글 같음) |
| `textbook/part6/ch29-agent-evaluation/04-운영-지표와-Ch18-궤적-비교.html` | `1305131f` → `6f5f2a80` | `_build.py`(b8 05 링크) |
| `labs/part6/ch29-agent-evaluation/notebooks/04-운영-지표와-Ch18-궤적-비교.ipynb` | `3c1c41fd` → `95dfbec8` | 정리 끝 마크다운 셀 52 하나만(`mdpatch.py`) — **`code_sha256` `43163e6ac114…`·`outputs_sha256` `cccaacaa28da…`·`executed_at` 03:03:14Z 그대로**(다시 실행 안 함) |
| `textbook/part6/ch29-agent-evaluation/집필점검표.md` | `8fcf2bdd` → `e7bc38dc` | 「품질 개선」 표에 05 행 덧붙임 |
| `textbook/part6/ch29-agent-evaluation/qa/verification.md` | `34de337d` → `7f08c234` | 「품질 개선 검증」 표에 05 행 덧붙임 |
| `textbook/part6/ch29-agent-evaluation/qa/public-files.json` | `57815fa5` → `4913e24d` | 05 HTML·05 노트북 두 줄 |
| `textbook/part6/public-files.json` | `e0052b91` → `47429ce7` | `collect_public_files.py`(93 → 94 — 05 노트북) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` | `49dc8ded` → `c1ea214f` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀(5절) |
| `labs/part6/ch29-agent-evaluation/README.md` | `e252d099`(목록 값) → `8be9903b` | **새로 바뀜** — 맨 아래 05절 한 단락만 |
| `textbook/part6/index.html` | `4e3d5941`(목록 값) → `a8c95c20` | **새로 바뀜** — `_build_index.py`(Ch 29 「5절」·05 링크) |
| `textbook/downloads/part6-practice.zip` | `5002dce3`(목록 값) → `f5d87d66` | **새로 바뀜** — `_build_index.py`(Ch 29 01~05 새 판·도구 파일 05판, 113항목, `__pycache__` 0) |
| `textbook/part6/qa/integration-results.json` | `7a46d6c8`(목록 값) → `0526eb39` | **새로 바뀜** — `_build_index.py`(`Part 6: 56 verified sections; 110 bundled files`) |

- **04 기록 해시 그대로(11)**: 01~03 `_src`(`228234ba`·`65d77f15`·`1732be10`)·01~03 HTML(`9fc60c2f`·`62822dcf`·`d5a0ac5f`)·01~03 노트북(`debd4640`·`abdd6dc3`·`41e79afe` — 다시 실행하지 않음, 01·02는 사본에서 05판 도구 파일로 23/23·27/27 같음)·공용 옛 생성기(`391be055`)·`figures/_gen_figures.py`(`3577112d`).
- **계약 파일 둘 그대로(목록 값과 같음)**: Ch 21 `data/rag-comparison.json` **`25cfe5df…`** · Ch 18 06 노트북 **`5ba7f5a0…`** — 05는 읽지도 않음(`author_04.check_contracts()`로 해시만 확인).
- **목록 밖(01이 만든 새 파일)**: 도구 파일 `labs/part6/ch29-agent-evaluation/notebooks/eval_tools.py` `223881ec…`(04판) → **`d624b8f360c993e5f93d779dbf58f3ad41e60f6bd47dda2c3aecd9c5da6f0af9`**(05판 — 04 노트북 셀 `show_row` 글자 그대로, 가져오기 줄 그대로, 대조 사슬 `author_05.check_tools`). `author_04.py` `370829e4` → `e0bc07da`(`L_05` 한 줄·b8·노트북 끝 문장 — `mdpatch.py`).
- **바뀌지 않은 것(확인)**: `pyproject.toml`(`5a3ca31c`)·`uv.lock`(`de2416a1`) · `prerequisite-files.json`(`4c7f5a4b`) · `llm-practice.zip`·`bundle-execution.json`·`delivery-results.json`(`3cc2d143`) · `textbook/index.html` · Ch 18·21·28·30·33 원고 · `.moai/…/part6b_enrich.py`·`part6b_review_fixes.py`(실행·수정 안 함).
- 새로 생긴 파일(목록 밖): 노트북 `05-Agent-평가-실습.ipynb`(`053ab017…`) · `_src/05-Agent-평가-실습.html`(`7b93c106…`)·빌드 `05-Agent-평가-실습.html`(`c6eaca34…`) · `qa/upgrade/author_05.py`(`4f516b75…`)·`05-probe.md`·`probe/probe05.py`(`978d1685…`)·`probe/probe-05-R.jsonl`(`7a5012f4…`)·`05-figures.md`·`05-diagnosis.md`·`gates-wip-05-05.json`·`gates-wip-05.json`·`gates-wip-ch29-after05.json`·`review-pack/05-Agent-평가-실습.md`(04 묶음도 다시 만듦) · `figures/05-1~05-3-*.{mmd,svg,png,caption.md,render.json}` · `figures/05-4-끝이-다른-두-띠.{png,prompt.md,caption.md}` · 사용자 디스크 `.cache/ch29-05-view/`(그림 확인 사본 셋). `handoff.md`·이 파일은 덧붙임.
- 노트북 실행·생성기는 모두 `PYTHONDONTWRITEBYTECODE=1`(+ `python3 -B`) — 실습 폴더 `notebooks/__pycache__`·챕터 `qa/upgrade/__pycache__` 없음, 이 작업 뒤 새 `.pyc` 0. `.failure.json` 없음.

## 마감 뒤 (2026-09-29)

`before-manifest.json` 217개 대조: **같음 177 · 바뀜 38 · 옮김 2**(`.cache/ch29-close/tools/manifest_check29.py`). 05절 뒤 25개에 마감이 더한 것은 Ch 21 06 셋·Ch 21 요약·Part 6 목차 스크립트·`bundle-execution.json`·`visual-results.json`·`continuity-guide.md`·전체 목차 둘·`.moai` 둘·옛 기록 둘·최종 점검표와 옮긴 생성기 둘입니다. 가운데 열은 마감 전 사본(`.cache/ch29-close/log/pre-hashes.txt`, 04:30) 값입니다.

| 파일 | 목록 값 → 마감 전 → 마감 뒤(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch29-agent-evaluation/chapter.json` | `d84d0a07` → `4e565b61` → `174ae411` | `objectives` 둘 → 다섯(A-12·B-13), `hours` 그대로 |
| `textbook/part6/ch29-agent-evaluation/index.html` | `934283ad` → `2821043d` → `1b9b3fb0` | `_build.py` — 목표 다섯 |
| `textbook/part6/ch29-agent-evaluation/01-에이전트-평가-세-전략.html` | `6fb8d298` → `9fc60c2f` → `aab5840d` | `_build.py` — 01 `_src` 고침 |
| `textbook/part6/ch29-agent-evaluation/02-궤적-매칭-네-모드.html` | `9aa592e5` → `62822dcf` → `83f80421` | `_build.py` — 02 `_src` 고침·재실행 출력 |
| `textbook/part6/ch29-agent-evaluation/03-LLM-judge로-궤적-평가.html` | `16b17a74` → `d5a0ac5f` → `9eaf630e` | `_build.py` — 03 `_src`·캡션 고침 |
| `textbook/part6/ch29-agent-evaluation/04-운영-지표와-Ch18-궤적-비교.html` | `f39bbffe` → `6f5f2a80` → `00494da5` | `_build.py` — 04 `_src` 고침·재실행 출력·04-3 다시 렌더 |
| `textbook/part6/ch29-agent-evaluation/_src/01-에이전트-평가-세-전략.html` | `8bf41a94` → `228234ba` → `0ff9e39f` | A-1·A-2·A-5 — `gapply29.py`(`src_html()`) |
| `textbook/part6/ch29-agent-evaluation/_src/02-궤적-매칭-네-모드.html` | `f24afc79` → `65d77f15` → `bc8ca1a2` | A-1·A-3·A-4·A-5·A-6·A-9 — `gapply29.py` |
| `textbook/part6/ch29-agent-evaluation/_src/03-LLM-judge로-궤적-평가.html` | `c1ffadca` → `1732be10` → `94a0d55c` | A-3·B-1·B-2·B-4·B-8 — `gapply29.py` |
| `textbook/part6/ch29-agent-evaluation/_src/04-운영-지표와-Ch18-궤적-비교.html` | `ec34bf6e` → `e120a5d4` → `1ba3b8c2` | B-5·B-6·B-7 — `gapply29.py` |
| `textbook/part6/ch29-agent-evaluation/집필점검표.md` | `1e914c7c` → `e7bc38dc` → `20c414d1` | 머리 「개선 전 판」 표시 + 끝 「마감 (2026-09-29)」 |
| `textbook/part6/ch29-agent-evaluation/figures/_gen_figures.py` | `65b435f8` → `3577112d` → **옮김** | **옮김** → `qa/upgrade/before/generators/blocked/_gen_figures.py`(`mv -n`, `3577112d…` 같음) |
| `textbook/part6/ch29-agent-evaluation/qa/public-files.json` | `7c28818f` → `4913e24d` → `4913e24d` | 마감에서 바꾸지 않음(05절 값 — 옛 그림 줄 원래 없음) |
| `textbook/part6/ch29-agent-evaluation/qa/research.md` | `9415074c` → `9415074c` → `7ea74452` | 머리 「개선 전 판」 표시 |
| `textbook/part6/ch29-agent-evaluation/qa/technical-notes.md` | `163d4879` → `163d4879` → `b67e8ec8` | 머리 「개선 전 판」 표시 |
| `textbook/part6/ch29-agent-evaluation/qa/verification.md` | `52d03d42` → `7f08c234` → `51abe017` | 머리 「개선 전 판」 표시 + 끝 「마감 (2026-09-29)」 |
| `labs/part6/ch29-agent-evaluation/README.md` | `e252d099` → `8be9903b` → `b108b2d3` | 전체 다시 씀(A-11·B-13) |
| `labs/part6/ch29-agent-evaluation/notebooks/01-에이전트-평가-세-전략.ipynb` | `d95e84d2` → `debd4640` → `a693de5c` | 마크다운 셀 0·6·18만(코드·출력·`executed_at` 같음) |
| `labs/part6/ch29-agent-evaluation/notebooks/02-궤적-매칭-네-모드.ipynb` | `a1bd4160` → `abdd6dc3` → `934cc954` | **다시 실행**(A-7 코드 셀 여섯 + 마크다운) — 코드 `238911432b50…`·출력 `274931b425d1…` |
| `labs/part6/ch29-agent-evaluation/notebooks/03-LLM-judge로-궤적-평가.ipynb` | `72324f31` → `41e79afe` → `36378027` | 마크다운 셀 6·27·29·51·59만(코드·출력·`executed_at` 같음) |
| `labs/part6/ch29-agent-evaluation/notebooks/04-운영-지표와-Ch18-궤적-비교.ipynb` | `b8c1b9d2` → `95dfbec8` → `76c112f6` | **다시 실행**(B-6 (나) 셀 [11] 출력 한 줄 뺌 + 마크다운) — 코드 `4ed26b54f6ff…`·출력 `492d4e24d7f3…` |
| `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` | `f2c0141a` → `c1ea214f` → `662d2a2f` | `verify.py --chapter`가 다시 씀(05절 뒤 `c1ea214f`) |
| `textbook/part6/ch21-create-agent/_src/06-같은-평가셋으로-RAG-비교.html` | `556759ee` → `556759ee` → `f2cb4ac5` | b10 셀 번호 문장(A-15·B-14) — `src_html()` = `_src` 전후 참 |
| `textbook/part6/ch21-create-agent/06-같은-평가셋으로-RAG-비교.html` | `f1c735dc` → `f1c735dc` → `73df1a27` | Ch 21 `_build.py`(다른 HTML 일곱은 해시 같음·수정 시각만 바뀜) |
| `textbook/part6/ch21-create-agent/qa/upgrade/author_06.py` | `137ddee4` → `137ddee4` → `c19c22f3` | b10 문장(생성기 쪽) — Ch 21 06 노트북·계약 파일 그대로 |
| `textbook/part6/ch21-create-agent/qa/upgrade/chapter-summary.md` | `0cb6fe08` → `0cb6fe08` → `214d2747` | 옛 생성기 항목(231행) 아래 「옮김」 한 줄 덧붙임 |
| `textbook/part6/public-files.json` | `498845c7` → `47429ce7` → `47429ce7` | 마감에서 바꾸지 않음(05절 값 — `collect_public_files.py` 결과 바이트 같음) |
| `textbook/part6/_build_index.py` | `2020202a` → `2020202a` → `66943bb4` | ch29 설명 줄 |
| `textbook/part6/index.html` | `4e3d5941` → `a8c95c20` → `d909e971` | `_build_index.py` — Ch 29 설명 한 줄 |
| `textbook/part6/qa/bundle-execution.json` | `fc4e1b78` → `fc4e1b78` → `f858a5ca` | `check_bundle_execution.py` PASS(새 zip 기준, Ch 24 01·Ch 28 01 값 그대로) |
| `textbook/part6/qa/integration-results.json` | `7a46d6c8` → `0526eb39` → `67c362bd` | `_build_index.py`(`Part 6: 56 verified sections; 110 bundled files`) |
| `textbook/part6/qa/visual-results.json` | `24d74549` → `24d74549` → `d8c16739` | Ch 29 줄 10 → 12 · Ch 21 06 두 줄 새 해시 · `screens` 132 |
| `labs/part6/continuity-guide.md` | `f549f3ad` → `f549f3ad` → `15b2dd3c` | Ch 29 줄(뒤 칸 Ch33 평가 회귀 검사) |
| `textbook/_notebook/build_index.py` | `cde0dc13` → `cde0dc13` → `b21bb749` | Ch 29 설명(절 수 4 그대로) |
| `textbook/index.html` | `64bfbb36` → `64bfbb36` → `fc7fdde3` | `build_index.py` — Ch 29 설명만 |
| `textbook/downloads/part6-practice.zip` | `5002dce3` → `f5d87d66` → `6d746be1` | `_build_index.py` 마지막 한 번 — `6d746be1ac649c10…`(113항목) |
| `textbook/part6/_author_ch21_ch29.py` | `650f6506` → `391be055` → **옮김** | **옮김** → `textbook/part6/ch29-agent-evaluation/qa/upgrade/before/generators/blocked/_author_ch21_ch29.py`(`mv -n`, `391be055…` 같음) |
| `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py` | `8528cb33` → `8528cb33` → `11ffa9fa` | 막음(A-13) — 주석 세 줄 + `raise SystemExit` 한 줄 |
| `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_review_fixes.py` | `a0299166` → `a0299166` → `fea9f8c7` | 막음(A-13) — 주석 세 줄 + `raise SystemExit` 한 줄 |
| `textbook/qa/upgrade-final-checklist.md` | `34cb850f` → `34cb850f` → `23a625b3` | §2-10 2번 「옮김」 · §2-13 6번 Ch 29 줄 · §2-17 새 절 · §3·§4 Ch 29 줄(덧붙이기만) |

- **계약 파일 둘 그대로(목록 값과 같음)**: Ch 21 `data/rag-comparison.json` **`25cfe5df…`** · Ch 18 06 노트북 **`5ba7f5a0…`**. Ch 21 06 노트북 `8a6f9da7…`(코드 `ca14949bb0f9…`·출력 `1ded374d9f64…`·`executed_at` 2026-09-25T05:11:56Z) 그대로 — 실행하지 않음.
- **목록 밖**: 05 노트북 `053ab017` → `18313379`(마크다운 셀 6·23·29만 — 코드 `7dba1d37a0bd…`·출력 `2793f969c4ac…`·`executed_at` 같음) · 05 `_src`·HTML · `author_01~05.py`(마감 반영 — 생성기 코드 셀 = 노트북 코드 셀, `src_html()` = `_src`) · 도구 파일 `eval_tools.py` **`d624b8f3…` 그대로** · `figures/03-2·03-3·03-4·04-3` 캡션 파일(생성기 `FIGn_CAP`과 맞춤)·`04-3-*.mmd`·`.svg`·`.png`·`.render.json`(다시 렌더) · `02-figures.md`(02-3 줄) · `01~05-diagnosis.md`(끝 「마감 반영」) · `handoff.md`(끝 「검토 반영과 챕터 마감」) · `chapter-summary.md`(새로) · `gates-after.json`·`gates-wip-01~05.json`(마감 `run_section.sh`) · `textbook/_notebook/checks/ch29-agent-evaluation/visual-results.json`과 스크린숏 넷 · `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json`(`verify.py --chapter` Ch 21) · `textbook/qa/upgrade-progress.md` Ch 29 행 · `qa/upgrade/before/generators/blocked/`(옮긴 두 파일).
- **바뀌지 않은 것(확인)**: `pyproject.toml`·`uv.lock` · `prerequisite-files.json` · `llm-practice.zip`·`delivery-results.json`(`3cc2d143`) · `textbook/part6/qa/notebook-readiness.json`(옛 검사가 다시 쓴 것을 실행 전 사본으로 되돌림 — `b3d69e9c…`) · `textbook/qa/upgrade-contracts.md`·`upgrade-course-summary.md` · Ch 18·28·30·33 원고.
- 파일 삭제 0. 모든 파이썬 실행 `PYTHONDONTWRITEBYTECODE=1` — 실습 폴더 `notebooks/__pycache__`·챕터 `qa/upgrade/__pycache__` 없음.
