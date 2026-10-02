# 보호 파일 변경 기록 (before-manifest.json 190개)

## 01절 뒤 (2026-09-28)

- 다시 계산: **180개 같음 · 10개 바뀜 · 0개 없어짐** — 모두 의도한 변경.

| 파일 | 전 | 후 | 까닭 |
|---|---|---|---|
| `labs/part6/ch26-delegation/notebooks/01-Subagent-도구-위임.ipynb` | `d9e73dbbb1db…` | `f366a099709a…` | 01절 새 노트북(A2 교재 출력, `code_sha256` `499eb8665ba1…`) |
| `textbook/part6/ch26-delegation/_src/01-Subagent-도구-위임.html` | `2c3f1796b537…` | `750fdffaa03e…` | 01절 본문 다시 씀(`author_01.py`) |
| `textbook/part6/ch26-delegation/01-Subagent-도구-위임.html` | `884dfee3acc2…` | `10350358ff6f…` | `_build.py`가 다시 만든 01 HTML |
| `textbook/part6/ch26-delegation/figures/_gen_figures.py` | `af127dcaba9e…` | `2e2304468817…` | 맨 위 설명 주석 + `raise SystemExit`(챕터 리드 결정 6) |
| `textbook/part6/ch26-delegation/qa/public-files.json` | `ab0fa37ad44b…` | `2b1e35ba5adc…` | 도구 파일 `delegation_tools.py` 한 줄 |
| `textbook/part6/public-files.json` | `8140df88908b…` | `bf15d6e6049e…` | `collect_public_files.py` — 도구 파일 한 줄(58행) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch26-delegation.json` | `0db775e628b9…` | `9fa9eb6cb684…` | `verify.py --chapter`가 다시 씀 |
| `textbook/part6/_generate_ch25_ch26.py` | `0767052613d9…` | `06fa7d9993e1…` | 공용 옛 생성기 맨 위 설명 주석 + `raise SystemExit`(챕터 밖, 챕터 리드 결정 6) |
| `textbook/part6/ch26-delegation/집필점검표.md` | `01932b1f3f00…` | `2cbc3214cb84…` | 끝에 「품질 개선 (2026-09-28~)」 표와 01 행 |
| `textbook/part6/ch26-delegation/qa/verification.md` | `08ddf5f10403…` | `c3e62a667f56…` | 끝에 「품질 개선 검증 (2026-09-28~)」 표와 01 행 |

- 새로 생긴 파일(보호 목록 밖): `labs/part6/ch26-delegation/notebooks/delegation_tools.py`(`90e83bcf…`) · `figures/01-1`~`01-5`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`01-6-큰-배와-작은-보트.{png,caption.md,prompt.md}` · `qa/upgrade/author_01.py`·`01-probe.md`·`probe/`·`01-figures.md`·`01-diagnosis.md`·`handoff.md`·`gates-wip-01*.json`·`review-pack/` · 연결 폴더 `.cache/ch26-01-view/`(그림 확인 사본).
- `textbook/part6/prerequisite-files.json`은 `collect_public_files.py`가 다시 썼지만 바이트가 같음(보호 목록 안, 같음).

## 02절 뒤 (2026-09-28)

- 다시 계산: **177개 같음 · 13개 바뀜 · 0개 없어짐** — 01절 뒤 10개(그중 셋은 02가 다시 바꿈) + 02가 새로 바꾼 셋. 모두 의도한 변경.

| 파일 | 01절 뒤 | 02절 뒤 | 까닭 |
|---|---|---|---|
| `labs/part6/ch26-delegation/notebooks/02-Handoff-상태-전환.ipynb` | `bfa710193162…`(원래) | `90a08c5d55f6…` | 02절 새 노트북(A 교재 출력, `code_sha256` `2d1b15cf6e77…`, 그 뒤 설명 셀·그림 첨부만 바뀜) |
| `textbook/part6/ch26-delegation/_src/02-Handoff-상태-전환.html` | `e0ef35c9a656…`(원래) | `f7bf91ecd95c…` | 02절 본문 다시 씀(`author_02.py`) |
| `textbook/part6/ch26-delegation/02-Handoff-상태-전환.html` | `90121da772a9…`(원래) | `a28898f14875…` | `_build.py`가 다시 만든 02 HTML |
| `textbook/_notebook/checks/notebook-contracts-part6-ch26-delegation.json` | `9fa9eb6cb684…` | `c3f7c8d81d9e…` | `verify.py --chapter`가 다시 씀(챕터 밖) |
| `textbook/part6/ch26-delegation/집필점검표.md` | `2cbc3214cb84…` | `dc55f9ccc230…` | 「품질 개선」 표에 02 행 |
| `textbook/part6/ch26-delegation/qa/verification.md` | `c3e62a667f56…` | `1902b091823f…` | 「품질 개선 검증」 표에 02 행 |

- 그대로: 01 노트북·`_src`·HTML(01절 뒤 값) · 03·04 노트북·`_src`·HTML · `index.html` · `chapter.json` · 공개 목록 둘 · 공용 옛 생성기 · `figures/_gen_figures.py` · 실습 폴더 잠금·README.
- 새로 생긴 파일(보호 목록 밖): `figures/02-1`~`02-5`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`02-6-밧줄이-넘어간-예인선.{png,caption.md,prompt.md}` · `qa/upgrade/author_02.py`·`02-probe.md`·`probe/probe02.py`·`probe/probe-02-P1.jsonl`·`02-figures.md`·`02-diagnosis.md`·`gates-wip-02*.json`·`review-pack/02-Handoff-상태-전환.md` · 연결 폴더 `.cache/ch26-02-view/`(삽화 확인 사본). 도구 파일 `delegation_tools.py`는 그대로(`90e83bcf…`).

## 03절 뒤 (2026-09-28)

- 다시 계산: **174개 같음 · 16개 바뀜 · 0개 없어짐** — 02절 뒤 13개(그중 셋은 03이 다시 바꿈) + 03이 새로 바꾼 셋. 모두 의도한 변경.

| 파일 | 02절 뒤 | 03절 뒤 | 까닭 |
|---|---|---|---|
| `labs/part6/ch26-delegation/notebooks/03-Router-분류와-병렬-실행.ipynb` | `a0e27cfe31c0…`(원래) | `0071c07d09a9…` | 03절 새 노트북(A 교재 출력, `code_sha256` `940a1065dba4…`, 그 뒤 설명 한 셀·그림 첨부만 바뀜) |
| `textbook/part6/ch26-delegation/_src/03-Router-분류와-병렬-실행.html` | `1ae3ec340d28…`(원래) | `57215e265535…` | 03절 본문 다시 씀(`author_03.py`) |
| `textbook/part6/ch26-delegation/03-Router-분류와-병렬-실행.html` | `a4f4af4a9366…`(원래) | `8eb3342fbb34…` | `_build.py`가 다시 만든 03 HTML |
| `textbook/_notebook/checks/notebook-contracts-part6-ch26-delegation.json` | `c3f7c8d81d9e…` | `6eda7f5f0573…` | `verify.py --chapter`가 다시 씀(챕터 밖) |
| `textbook/part6/ch26-delegation/집필점검표.md` | `dc55f9ccc230…` | `fd258b848006…` | 「품질 개선」 표에 03 행 |
| `textbook/part6/ch26-delegation/qa/verification.md` | `1902b091823f…` | `1bf353ca556c…` | 「품질 개선 검증」 표에 03 행 |

- 그대로: 01·02 노트북·`_src`·HTML(02절 뒤 값 — 01·02 HTML은 `_build.py`가 다시 만들었지만 바이트가 같음) · 04 노트북·`_src`·HTML · `index.html` · `chapter.json` · 공개 목록 둘 · 공용 옛 생성기 · `figures/_gen_figures.py` · 실습 폴더 잠금·README.
- 새로 생긴 파일(보호 목록 밖): `figures/03-1`~`03-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`03-5-분류-부두를-떠나는-짐배.{png,caption.md,prompt.md}` · `qa/upgrade/author_03.py`·`03-probe.md`·`probe/probe03.py`·`probe/probe-03-P1.jsonl`·`03-figures.md`·`03-diagnosis.md`·`gates-wip-03*.json`·`review-pack/03-Router-분류와-병렬-실행.md` · 연결 폴더 `.cache/ch26-03-view/`(삽화 확인 사본 둘). 도구 파일 `delegation_tools.py`는 그대로(`90e83bcf…`).

## 04절 뒤 (2026-09-28)

- 다시 계산: **171개 같음 · 19개 바뀜 · 0개 없어짐** — 03절 뒤 16개(그중 셋은 04가 다시 바꿈) + 04가 새로 바꾼 셋. 모두 의도한 변경.

| 파일 | 03절 뒤 | 04절 뒤 | 까닭 |
|---|---|---|---|
| `labs/part6/ch26-delegation/notebooks/04-호출-수-비용-종료-조건-비교.ipynb` | `cb8a579c6b50…`(원래) | `fc50cd3f6a6f…` | 04절 새 노트북(A 교재 출력, `code_sha256` `bc1e02160142…`, 그 뒤 자리 표시 두 단락·그림 첨부만 바뀜) |
| `textbook/part6/ch26-delegation/_src/04-호출-수-비용-종료-조건-비교.html` | `e8c1a42bef02…`(원래) | `550f41208e86…` | 04절 본문 다시 씀(`author_04.py`) |
| `textbook/part6/ch26-delegation/04-호출-수-비용-종료-조건-비교.html` | `1a5b54e9c2de…`(원래) | `5bf0a5cc0363…` | `_build.py`가 다시 만든 04 HTML |
| `textbook/_notebook/checks/notebook-contracts-part6-ch26-delegation.json` | `6eda7f5f0573…` | `40e28c491b42…` | `verify.py --chapter`가 다시 씀(챕터 밖) |
| `textbook/part6/ch26-delegation/집필점검표.md` | `fd258b848006…` | `8fad863c883d…` | 「품질 개선」 표에 04 행 |
| `textbook/part6/ch26-delegation/qa/verification.md` | `1bf353ca556c…` | `3ec85425af12…` | 「품질 개선 검증」 표에 04 행 |

- 그대로: 01·02·03 노트북·`_src`·HTML(03절 뒤 값 — 세 HTML은 `_build.py`가 다시 만들었지만 바이트가 같음) · `index.html` · `chapter.json` · 공개 목록 둘 · 공용 옛 생성기 · `figures/_gen_figures.py` · 실습 폴더 잠금·README.
- **보호 목록 밖 변경**: 도구 파일 `labs/part6/ch26-delegation/notebooks/delegation_tools.py` `90e83bcf…` → **`91512d6a60ea46c503fab132f05d7e4357be49ce795ed0b9674663a9b94fcf8b`**(04절 판 — 머리 설명 뒤 가져오기 줄 하나 + 01 `message_kinds`·`usage_with_specialists`, 02 `writer_names`, 03 `send_to_desks`, 01절 판 사본 `/tmp/ch26-04/delegation_tools.before.py`) · `notebooks/__pycache__/delegation_tools.cpython-312.pyc`(있던 파일 — `run_section.sh` 커널이 바뀐 도구 파일을 가져오며 08:26:23Z에 다시 씀, 지우지 않음).
- 새로 생긴 파일(보호 목록 밖): `figures/04-1`~`04-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`04-5-짐이-다-찬-배와-문에-막힌-배.{png,caption.md,prompt.md}` · `qa/upgrade/author_04.py`·`04-probe.md`·`probe/probe04.py`·`probe/probe-04-P1·P2·P2b·P3·P4.jsonl`·`04-figures.md`·`04-diagnosis.md`·`gates-wip-04*.json`·`review-pack/04-호출-수-비용-종료-조건-비교.md` · 연결 폴더 `.cache/ch26-04-view/`(삽화 확인 사본 둘).

## 05절 뒤 (2026-09-28 — 챕터 끝 실습 절 신설)

- 다시 계산: **165개 같음 · 25개 바뀜 · 0개 없어짐** — 04절 뒤 19개(그중 여덟은 05가 다시 바꿈) + 05가 새로 바꾼 여섯. 모두 의도한 변경(규격 §7-2 — 절 추가·앞 절 「다음 학습」 링크·공개 목록·Part 목차·묶음).

| 파일 | 04절 뒤 | 05절 뒤 | 까닭 |
|---|---|---|---|
| `labs/part6/ch26-delegation/notebooks/04-호출-수-비용-종료-조건-비교.ipynb` | `fc50cd3f6a6f…` | `582d4a1c44ae…` | 정리 끝 문장만 05절 링크 문장으로(`mdpatch.py`) — `code_sha256` `bc1e02160142…`·`outputs_sha256` `3f6d995346c3…` 그대로, 바뀐 셀은 마크다운 63번 하나 |
| `textbook/part6/ch26-delegation/_src/04-호출-수-비용-종료-조건-비교.html` | `550f41208e86…` | `6922649f7c49…` | b8 「다음 학습과 이어지는 지점」 → 05절(`mdpatch.py` + `author_04.py --src-only`) |
| `textbook/part6/ch26-delegation/04-호출-수-비용-종료-조건-비교.html` | `5bf0a5cc0363…` | `8d23a7dfc784…` | `_build.py`(04 `--no-exec`) |
| `textbook/part6/ch26-delegation/index.html` | `747e9a20ac2e…`(원래) | `b77becfb53d7…` | `_build.py` — 05절 목록 한 줄 |
| `textbook/part6/ch26-delegation/chapter.json` | `cf1f16f482ac…`(원래) | `07a5a74e7d51…` | `sections`에 05절(`hours`·`objectives` 그대로) |
| `textbook/part6/ch26-delegation/집필점검표.md` | `8fad863c883d…` | `a47ad8befdfc…` | 「품질 개선」 표에 05 행 |
| `textbook/part6/ch26-delegation/qa/verification.md` | `3ec85425af12…` | `4ba10ec88429…` | 「품질 개선 검증」 표에 05 행 |
| `textbook/part6/ch26-delegation/qa/public-files.json` | `2b1e35ba5adc…`(01절 뒤) | `d11ec800da78…` | 05 HTML·05 노트북 두 줄 |
| `labs/part6/ch26-delegation/README.md` | `d460b0debe8b…`(원래) | `87bc2dc1c795…` | 05절 단락 하나(README 다시 쓰기는 마감 몫) |
| `textbook/part6/public-files.json` | `bf15d6e6049e…`(01절 뒤) | `0d44ef6f80b1…` | `collect_public_files.py` — 05 노트북 한 줄(`prerequisite-files.json` 바이트 같음 `4c7f5a4b…`) |
| `textbook/part6/index.html` | `64594baf8fc7…`(원래) | `d46148b89fb3…` | `_build_index.py` — Ch 26 「5절」·05 링크 |
| `textbook/downloads/part6-practice.zip` | `71683e44e8e0…`(원래) | `83c92a6ae213…` | `_build_index.py` — Ch 26 아홉 항목(05 노트북·도구 파일 05절 판 등) 디스크와 같음 |
| `textbook/part6/qa/integration-results.json` | `bfe462a5d877…`(원래) | `4d620eb700b4…` | `_build_index.py`(절 53·묶음 102) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch26-delegation.json` | `40e28c491b42…` | `28c2358b506c…` | `verify.py --chapter`가 다시 씀(챕터 밖) |

- 그대로: 01·02·03 노트북·`_src`·HTML(`_build.py`가 다시 만들었지만 바이트 같음) · 공용 옛 생성기 · `figures/_gen_figures.py` · 실습 폴더 잠금 둘 · `labs/part6/continuity-guide.md` · `textbook/downloads/llm-practice.zip`(`f2d2008a…` — `_build_index.py`가 만들지 않음) · `textbook/part6/qa/delivery-results.json`(`check_delivery.py`가 `llm-practice.zip` Stale에서 멈춰 다시 쓰지 않음).
- **보호 목록 밖 변경**: 도구 파일 `delegation_tools.py` `91512d6a…` → **`c3c1709a8f0774196a6d6549c6deb5c93d244ce16d0d758afc9932d089f073b4`**(05절 판 — 04 `answered_desks`·`is_complete` 끝에 더함, 04절 판 사본 `/tmp/ch26-05/pre/delegation_tools.py`) · `notebooks/__pycache__/delegation_tools.cpython-312.pyc`(A 커널이 09:02:41Z에 다시 씀, 지우지 않음) · `qa/upgrade/author_04.py`(b8·정리 문자열만 — `dce68118…`).
- 새로 생긴 파일(보호 목록 밖): 05 노트북(`bbd6f27d…`)·`_src/05-…`(`0187840d…`)·`05-…html`(`133d0022…`) · `figures/05-1`~`05-3`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`05-4-항아리를-내려놓은-기중기와-멈춘-기중기.{png,caption.md,prompt.md}` · `qa/upgrade/author_05.py`·`05-probe.md`·`probe/probe05.py`·`probe/probe-05-A1·A2·B2·L2·L1.jsonl`·`05-figures.md`·`05-diagnosis.md`·`gates-wip-05*.json`·`review-pack/05-위임-구조-실습.md` · 연결 폴더 `.cache/ch26-05-view/`(그림 확인 사본 여섯).

## 마감 뒤 (2026-09-28 — 검토 반영과 챕터 마감)

- 다시 계산: **149개 같음 · 39개 바뀜 · 2개 옮김(없어짐)** — 마감이 바꾼 36(05절 뒤 이미 바뀌었던 것을 다시 바꾼 것 포함) + 옮김 2 + 05절 뒤 바뀐 채 마감이 건드리지 않은 3(`qa/public-files.json`·`textbook/part6/public-files.json`·`notebook-contracts-part6-ch26-delegation.json`). 모두 의도한 변경.

| 파일 | 마감 전 | 마감 뒤 | 까닭 |
|---|---|---|---|
| `labs/part6/ch26-delegation/README.md` | `87bc2dc1c795…` | `2ad9cfedddc9…` | 전체 다시 씀(검토 A-21·B-12) |
| `labs/part6/ch26-delegation/notebooks/01-Subagent-도구-위임.ipynb` | `f366a099709a…` | `a2f574c2c775…` | 마크다운만(검토 반영) — `code_sha256`·`outputs_sha256` 그대로 |
| `labs/part6/ch26-delegation/notebooks/02-Handoff-상태-전환.ipynb` | `90a08c5d55f6…` | `b2953d7fb0cf…` | 마크다운만(검토 반영) — `code_sha256`·`outputs_sha256` 그대로 |
| `labs/part6/ch26-delegation/notebooks/03-Router-분류와-병렬-실행.ipynb` | `0071c07d09a9…` | `60f57acd19f3…` | 마크다운만(검토 반영) — `code_sha256`·`outputs_sha256` 그대로 |
| `labs/part6/ch26-delegation/notebooks/04-호출-수-비용-종료-조건-비교.ipynb` | `582d4a1c44ae…` | `b32deb8e3b2a…` | 마크다운만(검토 반영) — `code_sha256`·`outputs_sha256` 그대로 |
| `textbook/part6/ch26-delegation/_src/01-Subagent-도구-위임.html` | `750fdffaa03e…` | `724e68ff74e8…` | 검토 반영 문장(`author_NN.py --src-only`) |
| `textbook/part6/ch26-delegation/_src/02-Handoff-상태-전환.html` | `f7bf91ecd95c…` | `68bc6ee69f65…` | 검토 반영 문장(`author_NN.py --src-only`) |
| `textbook/part6/ch26-delegation/_src/03-Router-분류와-병렬-실행.html` | `57215e265535…` | `5f7f69367af9…` | 검토 반영 문장(`author_NN.py --src-only`) |
| `textbook/part6/ch26-delegation/_src/04-호출-수-비용-종료-조건-비교.html` | `6922649f7c49…` | `bd756d770397…` | 검토 반영 문장(`author_NN.py --src-only`) |
| `textbook/part6/ch26-delegation/01-Subagent-도구-위임.html` | `10350358ff6f…` | `22ef62c335ec…` | `_build.py`(`run_section.sh … --no-exec`) |
| `textbook/part6/ch26-delegation/02-Handoff-상태-전환.html` | `a28898f14875…` | `1f5d5c0f96cb…` | `_build.py`(`run_section.sh … --no-exec`) |
| `textbook/part6/ch26-delegation/03-Router-분류와-병렬-실행.html` | `8eb3342fbb34…` | `7ea432b1fa1e…` | `_build.py`(`run_section.sh … --no-exec`) |
| `textbook/part6/ch26-delegation/04-호출-수-비용-종료-조건-비교.html` | `8d23a7dfc784…` | `334763446820…` | `_build.py`(`run_section.sh … --no-exec`) |
| `textbook/part6/ch26-delegation/index.html` | `b77becfb53d7…` | `5f39ac7ff8d8…` | `_build.py` — 학습 목표 넷 |
| `textbook/part6/ch26-delegation/chapter.json` | `07a5a74e7d51…` | `8000bbc49081…` | `objectives` 셋 → 넷(검토 B-11), `hours` 그대로 |
| `textbook/part6/ch26-delegation/research.md` | `80aeb44339bd…` | `3c9bbf5f703c…` | 머리 「개선 전 판」 표시 |
| `textbook/part6/ch26-delegation/집필점검표.md` | `a47ad8befdfc…` | `e554af82f171…` | 머리 표시 + 끝 「마감」 절 |
| `textbook/part6/ch26-delegation/figures/_gen_figures.py` | `2e2304468817…` | `(옮김)` | `mv -n` → `qa/upgrade/before/generators/blocked/`(해시 같음) |
| `textbook/part6/ch26-delegation/qa/authoring-checklist.md` | `7997622e83b1…` | `5929615a8be4…` | 머리 「개선 전 판」 표시 |
| `textbook/part6/ch26-delegation/qa/ch26-technical-review.md` | `5ec35a2ca110…` | `3a13de844353…` | 머리 「개선 전 판」 표시 |
| `textbook/part6/ch26-delegation/qa/research.md` | `d1716d3a5a6d…` | `7ac37eb5661b…` | 머리 「개선 전 판」 표시 |
| `textbook/part6/ch26-delegation/qa/verification.md` | `4ba10ec88429…` | `4230d5d61150…` | 머리 표시 + 끝 「마감」 절 |
| `textbook/part6/ch25-streaming/qa/upgrade/chapter-summary.md` | `2f623bd39308…` | `7d146069f9a5…` | §13-7에 「옮김」 한 줄 덧붙임(과제 지시 — 공용 옛 생성기 이동) |
| `labs/part6/continuity-guide.md` | `629587f0d854…` | `89b7e207a29e…` | Ch 26 줄(「Ch39」·옛 말 뺌) |
| `textbook/part6/index.html` | `d46148b89fb3…` | `5c19e32c3318…` | `_build_index.py` — Ch 26 설명 한 줄 |
| `textbook/part6/_build_index.py` | `e8d784c4971a…` | `20a14e7a5cae…` | ch26 설명 한 줄 |
| `textbook/_notebook/build_index.py` | `4bca42a3c613…` | `3454389df824…` | Ch 26 설명(절 수 4 그대로) |
| `textbook/index.html` | `90d6a6b84dfa…` | `18479837018b…` | `build_index.py` — Ch 26 행 하나 |
| `textbook/downloads/part6-practice.zip` | `83c92a6ae213…` | `110579388680…` | `_build_index.py` 마지막 한 번 — Ch 26 9파일·continuity-guide 디스크와 같음 |
| `textbook/part6/qa/bundle-execution.json` | `baaaf52f223c…` | `4f1cd14a98c4…` | `check_bundle_execution.py` PASS(새 zip) |
| `textbook/part6/qa/integration-results.json` | `4d620eb700b4…` | `c352bd9fe9f3…` | `_build_index.py`(절 53·묶음 102) |
| `textbook/part6/qa/visual-results.json` | `f2b70b7bcb57…` | `f63506dc3c20…` | Ch 26 줄만 10 → 12(`screens` 126) |
| `textbook/_notebook/checks/ch26-delegation/01-Subagent-도구-위임-1280.png` | `f9102cfa70a6…` | `a8359263ff37…` | `visual.cjs` 12행 PASS(스크린숏·결과 새로) |
| `textbook/_notebook/checks/ch26-delegation/01-Subagent-도구-위임-390.png` | `d8656652f222…` | `508ed0e80081…` | `visual.cjs` 12행 PASS(스크린숏·결과 새로) |
| `textbook/_notebook/checks/ch26-delegation/index-1280.png` | `3820abb2a077…` | `b5828c73c389…` | `visual.cjs` 12행 PASS(스크린숏·결과 새로) |
| `textbook/_notebook/checks/ch26-delegation/index-390.png` | `b0780660d8d6…` | `b9ea98c169ac…` | `visual.cjs` 12행 PASS(스크린숏·결과 새로) |
| `textbook/_notebook/checks/ch26-delegation/visual-results.json` | `f1b8e56968ab…` | `fbf86de72d0b…` | `visual.cjs` 12행 PASS(스크린숏·결과 새로) |
| `textbook/part6/_generate_ch25_ch26.py` | `06fa7d9993e1…` | `(옮김)` | `mv -n` → `qa/upgrade/before/generators/blocked/`(해시 같음) |

- 보호 목록 밖 변경: `_src/05-…`(`0187840d` → `367518a4`)·`05-…html`(`133d0022` → `00644be7`) · `qa/upgrade/author_01~05.py`(생성기 문자열만 — 도구 줄·코드 셀 글 0 바뀜) · 그림 `01-2`·`02-4`·`04-3`(`.mmd`·`.svg`·`.png`·`.render.json`) · `qa/upgrade/` 기록(진단 다섯·그림 설계표 넷·`02-probe.md`·`03-probe.md`·`04-probe.md`·`handoff.md`·`gates-after.json`·`gates-wip-01~05.json`·`chapter-summary.md`·이 파일) · `textbook/qa/upgrade-progress.md`(Ch 26 행) · `textbook/qa/upgrade-final-checklist.md`.
- 그대로: 도구 파일 `delegation_tools.py`(`c3c1709a…`) · 05 노트북(`bbd6f27d…`) · 실습 폴더 잠금 둘 · `textbook/downloads/llm-practice.zip` · `textbook/part6/qa/delivery-results.json`(`check_delivery.py`가 `llm-practice.zip` Stale에서 멈춰 다시 쓰지 않음) · `notebook-readiness.json`(옛 검사가 다시 쓴 것을 실행 전 사본으로 되돌림 `b3d69e9c…`) · `lesson-scope.json`·`figure-consistency.json`.
