# 보호 파일 변경 기록 (`before-manifest.json` 123개 대조)

## 01절 끝 (2026-09-25)

- 대조: `before-manifest.json`의 123개를 지금 파일과 sha256로 견줌 → **118개 같음 · 5개 바뀜 · 없어진 파일 0**. 바뀐 다섯은 모두 의도한 것입니다.

| 파일 | 전 | 후 | 까닭 |
|---|---|---|---|
| `labs/part6/ch23-persistence/notebooks/01-체크포인터와-스레드.ipynb` | `3e3ac6c1a083…` | `7189b35fdcfc8379ae95b3e226cd07edab0492be4bb8bb38ae8d5b116efa1170` | 01절 개선본(`author_01.py` → 새 커널 실행, `code_sha256` `9d71f6f9…`·`outputs_sha256` `4315f7f9…`) |
| `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py` | `8635d292463d…` | `44c9d593fcd061760fc2255453c20d3ccbe21a347ff5c0325e49ad91e12edcfb` | 공용 옛 생성기의 Ch 23 쪽만 막음(챕터 리드 결정 7 — Ch 24 쪽 산출 같음, `01-diagnosis.md` §8) |
| `textbook/part6/ch23-persistence/figures/_gen_figures.py` | `e77d489f86e5…` | `6d95031c3aafa0486e01e473e8c90361d62a008511ee9a287d525ec4623371ae` | 맨 위 `raise SystemExit(…)`(규격 §8 1번) |
| `textbook/part6/ch23-persistence/qa/verification.md` | `10e499e62276…` | `9f53652be5f7f77725048ed369da53221256723618a8800e619126db993cf139` | 끝에 「품질 개선 검증」 절과 01 행을 덧붙임(위 옛 기록은 그대로) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | `764c2e1712c0…` | `d1354d58702ec7781ccda66a167d9eee6128de90b7121c25501641d8e5d450ae` | `verify.py --chapter`가 다시 씀(01 노트북 계약 줄) |

- 바뀌지 않은 것(확인): 실습 폴더 `pyproject.toml`·`uv.lock`·`README.md`·worker 둘 · 02~06 노트북 · 챕터 `chapter.json`·`_build.py`·`qa/public-files.json` · Part 6 목록·묶음(`part6-practice.zip`) · Ch 20 02·03·Ch 21 03·07·Ch 22 09 파일 · 대기 챕터(Ch 24~31) 파일 · 공용 도구·검사 스크립트.
- 목록 밖이지만 다시 쓴 것: 챕터 HTML 일곱(`_build.py` — 02~06·`index.html`은 `_src`·노트북이 그대로라 내용 변화 없음, 두 번 빌드 해시 같음, `index.html`은 `before/index.html`과 바이트까지 같음).

## 02절 끝 (2026-09-25)

- 대조: `before-manifest.json`의 123개를 지금 파일과 sha256로 견줌 → **117개 같음 · 6개 바뀜 · 없어진 파일 0**. 01절 끝의 다섯에 02 노트북 하나가 더해졌고, 01절 끝과 값이 다른 것은 셋입니다.

| 파일 | 전(01절 끝) | 후 | 까닭 |
|---|---|---|---|
| `labs/part6/ch23-persistence/notebooks/02-PostgresSaver-준비와-스키마.ipynb` | `17b9af076be1…`(원본) | `c3b15aefd6354a44dc4f0ea0cd2f9eda80fd3ba7d1457a5b0bc423552227df18` | 02절 개선본(`author_02.py` → 새 커널 실행, `code_sha256` `5b4fa7cf…`·`outputs_sha256` `abb4f3d7…`, 뒤이어 마크다운만 `mdpatch.py`·`attach_figures.py`) |
| `textbook/part6/ch23-persistence/qa/verification.md` | `9f53652be5f7…` | `7baf9718ab94e6e76d143ade2ae93fa19d1102c032598f1c4e96d3d44c24c4a0` | 「품질 개선 검증」 표에 02 행을 덧붙임(위 옛 기록·01 행 그대로) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | `d1354d58702e…` | `e9166d3e3e5c302b721d9e70d08f5646be1ffeb105913a8470c9715efab9c3e0` | `verify.py --chapter`가 다시 씀(02 노트북 계약 줄) |
| (01절 끝과 같음) 01 노트북 `7189b35f…` · `qa/author_ch23_ch24.py` `44c9d593…` · `figures/_gen_figures.py` `6d95031c…` | — | — | 02절에서 건드리지 않음 |

- 바뀌지 않은 것(확인): **Ch 12 `qa/upgrade/pre_exec.sh`·Ch 12 02 노트북**(본으로 읽기만) · Ch 31 05 `_src`·노트북·README · 실습 폴더 `pyproject.toml`·`uv.lock`·`README.md`·worker 둘 · 01·03~06 노트북 · 챕터 `chapter.json`·`_build.py`·`qa/public-files.json` · Part 6 목록·묶음(`part6-practice.zip`) · Ch 20 02·03·Ch 21 03·07·Ch 22 09 파일 · 대기 챕터(Ch 24~31) 파일 · 공용 도구·검사 스크립트. Ch 12 데이터 폴더 `.cache/vm/pgdata`는 목록 밖이지만 읽지도 켜지도 않았습니다.
- 목록 밖 새 파일: `qa/upgrade/pre_exec.sh`(`8f078591…`) · `qa/upgrade/author_02.py` · `qa/upgrade/02-figures.md`·`02-diagnosis.md` · `figures/02-1`~`02-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`02-5`(`.png`·`.prompt.md`·`.caption.md`) · `gates-wip-02-02.json`·`gates-wip-02.json` · `review-pack/02-…md`. 목록 밖이지만 다시 쓴 것: `_src/02-…html` · 챕터 HTML 일곱(`_build.py` — 01 HTML은 01절 끝 해시 `d2581c772adc…` 그대로, `index.html`은 `before/index.html`과 바이트까지 같음) · `집필점검표.md`(02 행) · `handoff.md`(`§02 → §03`).

## 03절 끝 (2026-09-25)

- 대조: `before-manifest.json`의 123개를 지금 파일과 sha256로 견줌 → **116개 같음 · 7개 바뀜 · 없어진 파일 0**. 02절 끝의 여섯에 03 노트북 하나가 더해졌고, 02절 끝과 값이 다른 것은 셋입니다.

| 파일 | 전(02절 끝) | 후 | 까닭 |
|---|---|---|---|
| `labs/part6/ch23-persistence/notebooks/03-스레드-재개와-대화-이어가기.ipynb` | `7a23d7591046…`(원본) | `ab7333da9124dcc9882ae2817e37c391630ec29a09174bc154a5420969f4609d` | 03절 개선본(`author_03.py` → 새 커널 실행, `code_sha256` `fe89a30a…`·`outputs_sha256` `952dc366…`, 뒤이어 마크다운만 `mdpatch.py`·`attach_figures.py`) |
| `textbook/part6/ch23-persistence/qa/verification.md` | `7baf9718ab94…` | `a67a714db1864d2d1558487e4af92e1d60c6f8bc9d42bfc273a6d7b7bea2602f` | 「품질 개선 검증」 표에 03 행을 덧붙임(위 옛 기록·01·02 행 그대로) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | `e9166d3e3e5c…` | `9e32f5d04e701f210ccee02eabd97ec263fe537f5950a1867634d32f59f1de0b` | `verify.py --chapter`가 다시 씀(03 노트북 계약 줄) |
| (02절 끝과 같음) 01 노트북 `7189b35f…` · 02 노트북 `c3b15aef…` · `qa/author_ch23_ch24.py` `44c9d593…` · `figures/_gen_figures.py` `6d95031c…` | — | — | 03절에서 건드리지 않음 |

- 바뀌지 않은 것(확인): 실습 폴더 `pyproject.toml`(`a000ee0f…`)·`uv.lock`(`013c4b44…`)·`README.md`·worker 둘 · 04~06 노트북 · 챕터 `chapter.json`·`_build.py`·`qa/public-files.json` · Part 6 목록(`textbook/part6/public-files.json`)·묶음(`part6-practice.zip` `3755de3d…`) · Ch 4 03·Ch 12 02 노트북·Ch 12 `pre_exec.sh` · Ch 20 02·03·Ch 21 03·07·**Ch 22 09 파일** · 대기 챕터(Ch 24~31) 파일 · 공용 도구·검사 스크립트. **`notebooks/checkpoint_tools.py`는 만들지 않음**(묶음 목록 변경 0).
- 목록 밖 새 파일: `qa/upgrade/author_03.py`(`08789d91…`) · `qa/upgrade/03-figures.md`·`03-diagnosis.md` · `figures/03-1`~`03-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`03-5`(`.png` `1a382674…`·`.prompt.md`·`.caption.md`) · `gates-wip-03-03.json`·`gates-wip-03.json` · `review-pack/03-…md`. 목록 밖이지만 다시 쓴 것: `_src/03-…html`(`59216563…`) · 챕터 HTML 일곱(`_build.py` — 03 HTML `7e2c3dc1…`, 01·02 HTML은 `_src`·노트북 그대로라 내용 변화 없음) · `집필점검표.md`(03 행) · `handoff.md`(`§03 → §04`) · `qa/upgrade/__pycache__/`(`author_03` 캐시).

## 04절 끝 (2026-09-25)

- 대조: `before-manifest.json`의 123개를 지금 파일과 sha256로 견줌 → **114개 같음 · 9개 바뀜 · 없어진 파일 0**. 03절 끝의 일곱에 04 노트북·**worker `durability_worker.py`** 둘이 더해졌고, 03절 끝과 값이 다른 것은 넷입니다.

| 파일 | 전(03절 끝) | 후 | 까닭 |
|---|---|---|---|
| `labs/part6/ch23-persistence/notebooks/04-내구-실행-모드-비교.ipynb` | `b76842eab3ca…`(원본) | `be38374b8616e3ce8765ff38345ca2aff29264284e8c7e69695e16c5b2a3bc22` | 04절 개선본(`author_04.py` → 새 커널 실행, `code_sha256` `ff4e48c4…`·`outputs_sha256` `845cda33…`, 뒤이어 마크다운만 `mdpatch.py`·오늘 볼 그림 셀 채우기·`attach_figures.py`) |
| `labs/part6/ch23-persistence/durability_worker.py` | `ce6fb8c56770…`(원본) | `c60467bdd82d40792148b2afad0471a98a8219ac6de48f10b104578be14491de` | 04절이 쓰는 worker 스크립트를 다시 씀(인자 다섯·임시 폴더 안 파일 이름·저장 여부로 가르는 다시 실행 단계·금지 문법 0·한국어 주석 — 인계 §03 → §04 3항 「04가 정함」). 자리·이름 그대로라 묶음 목록 변경 0. 생성기 `author_04.py`의 `WORKER` 글이 씀 |
| `textbook/part6/ch23-persistence/qa/verification.md` | `a67a714db186…` | `ff0c9937fe7afe863710abeb485777143d543e08ea54bab5a90d71a55b853d9b` | 「품질 개선 검증」 표에 04 행을 덧붙임(위 옛 기록·01~03 행 그대로) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | `9e32f5d04e70…` | `6a540493572b789bb927d8772d24427ab8868b009e00a336d89820d066880f31` | `verify.py --chapter`가 다시 씀(04 노트북 계약 줄) |
| (03절 끝과 같음) 01 노트북 `7189b35f…` · 02 노트북 `c3b15aef…` · 03 노트북 `ab7333da…` · `qa/author_ch23_ch24.py` `44c9d593…` · `figures/_gen_figures.py` `6d95031c…` | — | — | 04절에서 건드리지 않음 |

- 바뀌지 않은 것(확인): 실습 폴더 `pyproject.toml`(`a000ee0f…`)·`uv.lock`(`013c4b44…`)·`README.md`(`2c9516e0…`)·**`idempotency_worker.py`(`f668aa02…`, 06 몫)** · 05·06 노트북 · 챕터 `chapter.json`·`_build.py`·`qa/public-files.json`(`42208604…`) · Part 6 목록(`textbook/part6/public-files.json` `cf2fb079…`)·묶음(`part6-practice.zip` `3755de3d…` — **안의 worker·04 노트북은 옛 판, 마감에서 짝으로 다시 묶을 것**) · Ch 20 02·03(**b7 링크 슬러그 그대로**)·Ch 21 03·07·Ch 22 09 파일 · 대기 챕터(Ch 24~31) 파일 · 공용 도구·검사 스크립트. **`notebooks/checkpoint_tools.py`는 만들지 않음**(04가 강제 종료 함수를 처음 가르친 절 — 06·07 몫).
- 목록 밖 새 파일: `qa/upgrade/author_04.py`(`11e5dba8…`) · `qa/upgrade/04-probe.md`·`04-figures.md`·`04-diagnosis.md` · `figures/04-1`~`04-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`04-5`(`.png` `29a24868…`·`.prompt.md`·`.caption.md`) · `gates-wip-04-04.json`·`gates-wip-04.json`·`gates-wip.json`(챕터 전체 검사 한 번) · `review-pack/04-…md`. 목록 밖이지만 다시 쓴 것: `_src/04-…html`(`ab869ad4…`) · 챕터 HTML 일곱(`_build.py` — 04 HTML `7c175686…`, 01 `d2581c77…`·03 `7e2c3dc1…` 앞 절 기록과 같음, `index.html`은 `before/index.html`과 바이트까지 같음) · `집필점검표.md`(04 행) · `handoff.md`(`§04 → §05`) · `qa/upgrade/__pycache__/`(`author_04` 캐시).

## 05절 끝 (2026-09-25)

- 대조: `before-manifest.json`의 123개를 지금 파일과 sha256로 견줌 → **113개 같음 · 10개 바뀜 · 없어진 파일 0**. 04절 끝의 아홉에 05 노트북이 더해졌고, 04절 끝과 값이 다른 것은 셋입니다.

| 파일 | 전(04절 끝) | 후 | 까닭 |
|---|---|---|---|
| `labs/part6/ch23-persistence/notebooks/05-pending-writes와-장애-복구.ipynb` | `8ee4cd8ce654…`(원본) | `d544089a5e04f9e2796fe8eb9f7ed737081fe823d5c357dcc8c7cdd5480c9859` | 05절 개선본(`author_05.py` → 새 커널 실행, `code_sha256` `06cd28c6…`·`outputs_sha256` `b39f9ee7…`, 뒤이어 마크다운 첨부만 `attach_figures.py`) |
| `textbook/part6/ch23-persistence/qa/verification.md` | `ff0c9937fe7a…` | `40ada7bb39204d7303caeb6c8ce32041ec89d6c6288403e832054a3f06d66cc4` | 「품질 개선 검증」 표에 05 행을 덧붙임(위 옛 기록·01~04 행 그대로) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | `6a540493572b…` | `82a2f536fcdb0d8feabfc397095e6aff4863e7130d858943ec345dd3a88eff14` | `verify.py --chapter`가 다시 씀(05 노트북 계약 줄) |
| (04절 끝과 같음) 01 노트북 `7189b35f…` · 02 `c3b15aef…` · 03 `ab7333da…` · 04 `be38374b…` · worker `durability_worker.py` `c60467bd…` · `qa/author_ch23_ch24.py` `44c9d593…` · `figures/_gen_figures.py` `6d95031c…` | — | — | 05절에서 건드리지 않음 |

- 바뀌지 않은 것(확인): 실습 폴더 `pyproject.toml`·`uv.lock`·`README.md`(`2c9516e0…`)·**`idempotency_worker.py`(`f668aa02…`, 06 몫)** · 06 노트북 · 챕터 `chapter.json`·`_build.py`·`qa/public-files.json`(`42208604…`) · Part 6 목록(`textbook/part6/public-files.json` `cf2fb079…`)·묶음(`part6-practice.zip` `3755de3d…` — 안의 04·05 노트북·worker는 옛 판, 마감 몫) · Ch 20 02·03(b7 링크 슬러그 그대로)·Ch 21·22 파일 · 대기 챕터(Ch 24~31) 파일 · 공용 도구·검사 스크립트. **`notebooks/checkpoint_tools.py`는 만들지 않음**(05는 04 함수를 쓰지 않음 — 06이 처음 가져오며 만듦).
- 목록 밖 새 파일: `qa/upgrade/author_05.py`(`ca8264b9…`) · `qa/upgrade/05-probe.md`·`05-figures.md`·`05-diagnosis.md` · `figures/05-1`~`05-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`05-5`(`.png` `31b6177e…`·`.prompt.md`·`.caption.md`) · `gates-wip-05-05.json`·`gates-wip-05.json` · `review-pack/05-…md` · `qa/upgrade/__pycache__/author_05.cpython-310.pyc`. 목록 밖이지만 다시 쓴 것: `_src/05-…html`(`174bd518…`) · 챕터 HTML 일곱(`_build.py` — 05 HTML `df15083f…`, 01 `d2581c77…`·03 `7e2c3dc1…`·04 `7c175686…` 앞 절 기록과 같음, `index.html`은 `before/index.html`과 바이트까지 같음) · `집필점검표.md`(05 행) · `handoff.md`(`§05 → §06`).

## 06절 끝 (2026-09-25)

- 대조: `before-manifest.json`의 123개를 지금 파일과 sha256로 견줌 → **109개 같음 · 14개 바뀜 · 없어진 파일 0**. 05절 끝의 열에 06 노트북·**worker `idempotency_worker.py`**·**묶음 목록 둘**이 더해졌고, 05절 끝과 값이 다른 것은 여섯입니다.

| 파일 | 전(05절 끝) | 후 | 까닭 |
|---|---|---|---|
| `labs/part6/ch23-persistence/notebooks/06-노드-재시작과-멱등성.ipynb` | `767959df72d2…`(원본) | `869b6ae460f46030f89b2285a915483b0afe85f96153c5f3747eaad2b2bd434f` | 06절 개선본(`author_06.py` → 새 커널 실행, `code_sha256` `52c92b7d…`·`outputs_sha256` `8cf67c49…`, 뒤이어 마크다운 첨부만 `attach_figures.py`) |
| `labs/part6/ch23-persistence/idempotency_worker.py` | `f668aa02563d…`(원본) | `b0201de72d4534a7238d0bd5b2ad8b4d85e2ca0eeb6f307ac7d6897207430b72` | 06절이 쓰는 worker 스크립트를 다시 씀(04 worker와 같은 인자 다섯·`first-run`/`resume`·노드 `receive_order` → `charge`·저장 시점 `sync`·임시 폴더 안 파일 이름·금지 문법 0·한국어 주석 — 인계 §05 → §06 7항 「06 몫」). 자리·이름 그대로. 생성기 `author_06.py`의 `WORKER` 글이 씀(노트북 밖 확인 사본과 해시 같음) |
| `textbook/part6/public-files.json` | `cf2fb079d315…` | `9beba9726fec6067526c5607d0138038568975e15c970ff37385d01bfc48246b` | 새 도구 파일 `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py` 한 줄을 06 노트북 줄 다음에 더함(이름 차례 — `collect_public_files.py`의 `sorted` 결과와 같은 자리, 79줄) |
| `textbook/part6/ch23-persistence/qa/public-files.json` | `42208604e49e…` | `8aa1f73d014e5eb67002e10ae6aa0ce7aecc69e4903b3d66d1ffc15d3092406a` | 같은 도구 파일 한 줄을 끝에 더함(25줄) |
| `textbook/part6/ch23-persistence/qa/verification.md` | `40ada7bb3920…` | `6587bb446ee923fa8eb4dad10cde8d4aa9560f5977519100bdacf274f793cbc5` | 「품질 개선 검증」 표에 06 행을 덧붙임(위 옛 기록·01~05 행 그대로) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | `82a2f536fcdb…` | `5cf089356d7de04679ff56ed637c107702bc7239596141bb2876179d9153f64d` | `verify.py --chapter`가 다시 씀(06 노트북 계약 줄) |
| (05절 끝과 같음) 01~05 노트북 · worker `durability_worker.py` `c60467bd…` · `qa/author_ch23_ch24.py` `44c9d593…` · `figures/_gen_figures.py` `6d95031c…` | — | — | 06절에서 건드리지 않음(04 노트북은 함수를 셀에 둔 채 그대로 — 다시 실행 안 함) |

- 바뀌지 않은 것(확인): 실습 폴더 `pyproject.toml`·`uv.lock`·`README.md`(`2c9516e0…`) · 챕터 `chapter.json`·`_build.py` · 묶음 `part6-practice.zip`(`3755de3d…` — **안의 04·05·06 노트북·worker 둘은 옛 판이고 도구 파일이 없음, 마감에서 다시 묶을 것**) · Ch 20 02·03(b7 링크 슬러그 그대로)·Ch 21·22 파일 · 대기 챕터(Ch 24~31) 파일 · 공용 도구·검사 스크립트.
- 목록 밖 새 파일: **`labs/part6/ch23-persistence/notebooks/checkpoint_tools.py`(`71280dd9fdd748bb9ae98388990a7ed0d33d07e3fb1246abfba95c64c4437c29`, 도구 파일 — 묶음 목록 둘에 올림)** · `qa/upgrade/author_06.py` · `qa/upgrade/06-probe.md`·`06-figures.md`·`06-diagnosis.md` · `figures/06-1`~`06-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`06-5`(`.png` `47b1001a…`·`.prompt.md`·`.caption.md`) · `gates-wip-06-06.json`·`gates-wip-06.json` · `review-pack/06-…md`. 목록 밖이지만 다시 쓴 것: `_src/06-…html` · 챕터 HTML 일곱(`_build.py` — 06 HTML `2b2a9a45…`, 01 `d2581c77…`·02 `03bde627…`·03 `7e2c3dc1…`·04 `7c175686…`·05 `df15083f…` 앞 절 기록과 같음, `index.html`은 `before/index.html`과 바이트까지 같음) · `집필점검표.md`(06 행) · `handoff.md`(`§06 → 실습(07)`). 실습 폴더 `notebooks/__pycache__/`는 만들지 않음(실행 때 `PYTHONDONTWRITEBYTECODE=1`).

## 07절 끝 (2026-09-25)

- 대조: `before-manifest.json`의 123개를 지금 파일과 sha256로 견줌(`/tmp/ch23-07/manifest_check.py`) → **104개 같음 · 19개 바뀜 · 없어진 파일 0**. 06절 끝의 열넷에 다섯이 더해졌고, 06절 끝과 값이 다른 것은 아홉입니다.

| 파일 | 전(06절 끝) | 후 | 까닭 |
|---|---|---|---|
| `textbook/part6/ch23-persistence/chapter.json` | `d45772ccf3e4…`(원본) | `36267fb51acb8679bc5e0e3848f60687087c813242a02a8d74e246caa39eea39` | 07절(`07-Persistence-실습`, `experiment`) 추가 — `hours`·`objectives` 그대로 |
| `labs/part6/ch23-persistence/README.md` | `2c9516e0…`(원본) | `a876fed0efab5db6f4ef162f061f505483aff6d2a639224e3db52c525dd3a6fa` | 맨 아래 07절 한 단락만(README 다시 쓰기는 마감 몫) |
| `textbook/part6/ch23-persistence/qa/public-files.json` | `8aa1f73d014e…` | `d16b71f330f8198d820b9300285e6d2eba5ae72850083b43d3532f723b76928a` | 07 HTML·07 노트북 두 줄(06 줄 다음, Ch 21 마감 선례) |
| `textbook/part6/public-files.json` | `9beba9726fec…` | `8ed6852b524ff3c31686bbf62828020ab03e49fee0413215fcb48ff0832b8aef` | `collect_public_files.py`로 다시 모음 — 07 노트북 한 줄만(80줄). `prerequisite-files.json`은 바이트까지 같음 |
| `textbook/part6/ch23-persistence/qa/verification.md` | `6587bb446ee9…` | `398ec8fadeedadd8277eb723d50c62b97812efc60d5b06fbebfa6ed9db5339b4` | 「품질 개선 검증」 표에 07 행 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | `5cf089356d7d…` | `8d2cedf1b8e2f7da2752b6c2bc309fe8c1edc9bb06017255899011fdfe17efe2` | `verify.py --chapter`가 다시 씀(07 노트북 계약 줄) |
| `textbook/part6/index.html` | `c465e7b42c27…` | `ec2588c0fded345bacfa3d49a243e9d7c6672b528a6e98ccc03adb1c229037fd` | `python3 textbook/part6/_build_index.py` — Ch 23 「7절」·07 링크 |
| `textbook/downloads/part6-practice.zip` | `3755de3d15b3…` | `43b1923fa3e306e9d8adc0e787f5a45ffffddec3a803e57a9f847deefeefcc6b` | 같은 스크립트 — Ch 23 항목 13개(01~07 노트북·worker 둘·도구 파일·README·잠금 둘)가 모두 디스크와 같아짐 |
| `textbook/part6/qa/integration-results.json` | `e539f6d25a12…` | `2ff2be9f8cd615166569bc95bf04bcd3a395ef4c533eb8761e5d96169e89b719` | 같은 스크립트(`Part 6: 50 verified sections; 96 bundled files`) |
| (06절 끝과 같음) 01~06 노트북(06 `869b6ae4…`) · worker 둘(`c60467bd…`·`b0201de7…`) · `qa/author_ch23_ch24.py` `44c9d593…` · `figures/_gen_figures.py` `6d95031c…` | — | — | 07절에서 건드리지 않음 |

- 바뀌지 않은 것(확인): 실습 폴더 `pyproject.toml`·`uv.lock` · 도구 파일 `notebooks/checkpoint_tools.py`(`71280dd9…`, 목록 밖) · 챕터 `_build.py` · `textbook/index.html`(`1aea1103…`) · `textbook/part6/prerequisite-files.json`(`4c7f5a4b…`, 목록 밖) · `delivery-results.json`(`3cc2d143…` — `check_delivery.py`가 쓰기 전에 멈춤) · Ch 20 02·03(b7 링크 슬러그 그대로)·Ch 21·22 파일 · 대기 챕터(Ch 24~31) 파일 · 공용 도구·검사 스크립트.
- 목록 밖 새 파일: 노트북 `07-Persistence-실습.ipynb`(`0fe06118afcf…`) · `_src/07-…html`(`d0c586bd8191…`) · 빌드 `07-…html`(`164f1f6ad01c…`) · `figures/07-1`~`07-3`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`07-4-리본으로-이은-사진과-기보`(`.png` `68179ede…`·`.prompt.md`·`.caption.md`) · `qa/upgrade/author_07.py`(`21e1e5e9…`)·`07-figures.md`·`07-diagnosis.md`·`gates-wip-07.json`·`gates-wip-07-07.json`·`gates-wip-ch23-after07.json`·`review-pack/07-…md` · `qa/upgrade/__pycache__/author_07.cpython-310.pyc`. 목록 밖이지만 다시 쓴 것: `qa/upgrade/author_06.py`(`912c8dc7…` → `f620b444…`, b8 07 링크 한 곳) · `_src/06-…html`(`302faf19…` → `00092072…`) · 06 HTML(`2b2a9a45…` → `818b6b40…`) · 챕터 `index.html`(`45f0847c…` → `822f099e…`) · 01~05 HTML(내용 변화 없음 — 앞 절 기록 해시와 같음) · `집필점검표.md`(07 행) · `handoff.md`(「실습 → 챕터 검토」). 실습 폴더 `notebooks/__pycache__/`는 만들지 않음.
