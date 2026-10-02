# 보호 파일 변경 기록 (`before-manifest.json` 238개)

## 01절 뒤 (2026-09-28)

`before-manifest.json`(238개, `0484871c…`)을 다시 계산했습니다: **230개 같음 · 8개 바뀜 · 0개 없어짐** — 모두 의도한 변경입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/01-하네스와-일곱-기능.ipynb` | `ff1694dc5271` → `056ea2d4347e` | 01절 개선(새 노트북 26 코드 셀, 새 커널 실행, 그림 첨부, 설명 한 문장 `mdpatch.py`) |
| `textbook/part6/ch27-deepagents/_src/01-하네스와-일곱-기능.html` | `112e1a80586d` → `527e28ac3ccf` | 01절 본문 10블록 다시 씀 |
| `textbook/part6/ch27-deepagents/01-하네스와-일곱-기능.html` | `a8fd18066143` → `973b8dd2b514` | `_build.py` 빌드(`run_section.sh`) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | `6c0eec7e8ea7` → `05608f8910b9` | 끝에 「품질 개선」 표·01절 행 덧붙임(위 기록은 그대로) |
| `textbook/part6/ch27-deepagents/qa/verification.md` | `c59949985cb6` → `7d409b3768bd` | 끝에 「품질 개선 검증」 표·01절 행 덧붙임(위 기록은 그대로) |
| `textbook/part6/ch27-deepagents/qa/author_ch27.py` | `45453725f256` → `7bc6c96d3e1e` | 옛 생성기 막음(주석 셋 + `raise SystemExit`) — 마감에 `mv -n` |
| `textbook/part6/ch27-deepagents/figures/_gen_figures.py` | `45d40ea2f4e0` → `98641eb53491` | 옛 그림 생성기 막음(주석 셋 + `raise SystemExit`) — 마감에 `mv -n` |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | `8775ce031573` → `4308e6499904` | `verify.py --chapter`가 다시 씀(공용 도구 동작 — 손으로 고치지 않음) |

- 챕터 `index.html`·`chapter.json`·`_build.py`·02~08 `_src`·노트북·실습 폴더 README·잠금·`workspace*`·앞 챕터 파일·Part 6 목록·zip·기록 파일은 모두 같습니다.
- 새로 만든 파일(목록 밖): `qa/upgrade/author_01.py`·`01-figures.md`·`01-diagnosis.md`·`handoff.md`·`manifest-changes.md`·`gates-wip-01.json`·`gates-wip-01-01.json`·`review-pack/01-하네스와-일곱-기능.md` · `figures/01-1~01-4.{mmd,svg,png,caption.md,render.json}` · `figures/01-5-설비를-갖춘-온실.{png,prompt.md,caption.md}` · `.cache/ch27-01-view/`(그림 확인 사본).

## 02절 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **225개 같음 · 13개 바뀜 · 0개 없어짐** — 01절 뒤 8개(01 노트북·01 `_src`·01 HTML·옛 생성기 둘은 01 판 그대로, 아래 표시 셋은 02가 다시 바꿈) + 02절이 새로 바꾼 5개. 모두 의도한 변경입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/02-create-deep-agent와-도구.ipynb` | `22ab1526e430` → `f031b31008d6` | 02절 개선(새 노트북 26 코드 셀, 새 커널 실행 A, 흔들리는 값 둘째 단락 채움, 그림 첨부) |
| `textbook/part6/ch27-deepagents/_src/02-create-deep-agent와-도구.html` | `cd8d6f17fddd` → `5b670ce844a1` | 02절 본문 10블록 다시 씀 |
| `textbook/part6/ch27-deepagents/02-create-deep-agent와-도구.html` | `fc67f38f85f7` → `cad8f9afd7d4` | `_build.py` 빌드(`run_section.sh --no-exec`) |
| `textbook/part6/ch27-deepagents/qa/public-files.json` | `d13305337fd3` → `47aa0ac881a8` | 도구 파일 `notebooks/harness_tools.py` 한 줄 |
| `textbook/part6/public-files.json` | `0d44ef6f80b1` → `205d50ff5b4c` | `collect_public_files.py`가 위 한 줄을 모음(87개, `prerequisite-files.json` `4c7f5a4b` 그대로) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | (01 뒤 `05608f8910b9`) → `d0a4401412f7` | 「품질 개선」 표에 02절 행 덧붙임 |
| `textbook/part6/ch27-deepagents/qa/verification.md` | (01 뒤 `7d409b3768bd`) → `f5b4269ada30` | 「품질 개선 검증」 표에 02절 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | (01 뒤 `4308e6499904`) → `aba581b5708c` | `verify.py --chapter`가 다시 씀(공용 도구 동작 — 손으로 고치지 않음) |

- 챕터 `index.html`·`chapter.json`·`_build.py`·03~08 `_src`·노트북·실습 폴더 README·잠금·`workspace*`·앞 챕터 파일·zip·기록 파일은 모두 같습니다.
- 새로 만든 파일(목록 밖): **`labs/part6/ch27-deepagents/notebooks/harness_tools.py`**(`14ee39ca…`, 묶음 목록 두 곳에 올림 — zip은 마감) · `qa/upgrade/author_02.py`·`02-probe.md`·`02-figures.md`·`02-diagnosis.md`·`gates-wip-02.json`·`gates-wip-02-02.json`·`probe/probe02.py`·`probe/probe-02-P1.jsonl`·`review-pack/02-create-deep-agent와-도구.md` · `figures/02-1~02-4.{mmd,svg,png,caption.md,render.json}` · `figures/02-5-도구-걸이에-더한-연장.{png,prompt.md,caption.md}` · `.cache/ch27-02-view/`(그림 확인 사본).

## 03절 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **222개 같음 · 16개 바뀜 · 0개 없어짐** — 02절 뒤 13개(01·02 노트북·`_src`·HTML·옛 생성기 둘·공개 목록 둘은 앞 절 판 그대로, 아래 표시 셋은 03이 다시 바꿈) + 03절이 새로 바꾼 3개. 모두 의도한 변경입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/03-플래닝과-시스템-프롬프트.ipynb` | `17de24d510a1` → `1eed50d9a80f` | 03절 개선(새 노트북 30 코드 셀, 새 커널 실행 A, 흔들리는 값 둘째 단락 채움·그림 설명 두 문장 `mdpatch.py`, 그림 첨부) |
| `textbook/part6/ch27-deepagents/_src/03-플래닝과-시스템-프롬프트.html` | `00a21a31f6d3` → `2af1c7f2b3d2` | 03절 본문 10블록 다시 씀 |
| `textbook/part6/ch27-deepagents/03-플래닝과-시스템-프롬프트.html` | `58beaab207d8` → `c99cec3a9137` | `_build.py` 빌드(`run_section.sh --no-exec`) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | (02 뒤 `d0a4401412f7`) → `f96b347259f0` | 「품질 개선」 표에 03절 행 덧붙임 |
| `textbook/part6/ch27-deepagents/qa/verification.md` | (02 뒤 `f5b4269ada30`) → `b6d02c42a61c` | 「품질 개선 검증」 표에 03절 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | (02 뒤 `aba581b5708c`) → `727dc9988971` | `verify.py --chapter`가 다시 씀(공용 도구 동작 — 손으로 고치지 않음) |

- 도구 파일 `harness_tools.py`(목록 밖, 02 판 `14ee39ca…`)·챕터 `qa/public-files.json`(`47aa0ac8`)·`textbook/part6/public-files.json`(`205d50ff`)은 02절 뒤 그대로 — 03은 묶음 목록을 바꾸지 않음. 챕터 `index.html`·`chapter.json`·`_build.py`·04~08 `_src`·노트북·실습 폴더 README·잠금·`workspace*`·앞 챕터 파일·zip·기록 파일은 모두 같습니다.
- 새로 만든 파일(목록 밖): `qa/upgrade/author_03.py`·`03-probe.md`·`03-figures.md`·`03-diagnosis.md`·`gates-wip-03.json`·`gates-wip-03-03.json`·`probe/probe03.py`·`probe/probe-03-P.jsonl`·`review-pack/03-플래닝과-시스템-프롬프트.md` · `figures/03-1~03-4.{mmd,svg,png,caption.md,render.json}` · `figures/03-5-봉투를-꽂은-화단.{png,prompt.md,caption.md}` · `.cache/ch27-03-view/`(그림 확인 사본). `handoff.md`(목록 밖)에 「§03 → §04」와 03 완료 줄을 덧붙임.

## 04절 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **219개 같음 · 19개 바뀜 · 0개 없어짐** — 03절 뒤 16개(01~03 노트북·`_src`·HTML·옛 생성기 둘·공개 목록 둘은 앞 절 판 그대로, 아래 표시 셋은 04가 다시 바꿈) + 04절이 새로 바꾼 3개. 모두 의도한 변경입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/04-파일시스템과-중간-결과.ipynb` | `cf642b1f240c` → `4ab0023cde77` | 04절 개선(새 노트북 31 코드 셀, 새 커널 실행 A, 흔들리는 값 둘째 단락 채움·결과 읽기 한 문장 옮김 `mdpatch.py`, 그림 첨부) |
| `textbook/part6/ch27-deepagents/_src/04-파일시스템과-중간-결과.html` | `325279691e79` → `94b81208ad45` | 04절 본문 10블록 다시 씀 |
| `textbook/part6/ch27-deepagents/04-파일시스템과-중간-결과.html` | `04f83d6b8bfc` → `33bfbb651b2b` | `_build.py` 빌드(`run_section.sh --no-exec`) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | (03 뒤 `f96b347259f0`) → `0656205ccb45` | 「품질 개선」 표에 04절 행 덧붙임 |
| `textbook/part6/ch27-deepagents/qa/verification.md` | (03 뒤 `b6d02c42a61c`) → `c14a3b3891fd` | 「품질 개선 검증」 표에 04절 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | (03 뒤 `727dc9988971`) → `e6e271ece19c` | `verify.py --chapter`가 다시 씀(공용 도구 동작 — 손으로 고치지 않음) |

- **실습 폴더 `workspace`·`workspace-05`·`workspace-08`의 목록 안 파일은 모두 같음**(04는 임시 폴더에만 씀 — 옛 04가 쓰던 `workspace/research/source-a.md` 포함). 도구 파일 `harness_tools.py`(목록 밖, 02 판 `14ee39ca…`)·챕터 `qa/public-files.json`(`47aa0ac8`)·`textbook/part6/public-files.json`(`205d50ff`)은 그대로 — 04는 묶음 목록을 바꾸지 않음. 챕터 `index.html`·`chapter.json`·`_build.py`·05~08 `_src`·노트북·실습 폴더 README·잠금·앞 챕터 파일·zip·기록 파일은 모두 같습니다.
- 새로 만든 파일(목록 밖): `qa/upgrade/author_04.py`·`04-probe.md`·`04-figures.md`·`04-diagnosis.md`·`gates-wip-04.json`·`gates-wip-04-04.json`·`probe/probe04.py`·`probe/probe-04-P.jsonl`·`review-pack/04-파일시스템과-중간-결과.md` · `figures/04-1~04-4.{mmd,svg,png,caption.md,render.json}` · `figures/04-5-온실과-헛간의-모종판.{png,prompt.md,caption.md}` · `.cache/ch27-04-view/`(그림 확인 사본). `handoff.md`(목록 밖)에 「§04 → §05」와 04 완료 줄을 덧붙임. 연결 폴더 밖: 기기 세션 임시 폴더 `$TMPDIR/ch27-04-*` 11개·`ch27-04x-*` 5개, `/tmp/ch27-04/`.

## 05절 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **216개 같음 · 22개 바뀜 · 0개 없어짐** — 04절 뒤 19개(01~04 노트북·`_src`·HTML·옛 생성기 둘·공개 목록 둘은 앞 절 판 그대로, 아래 표시 셋은 05가 다시 바꿈) + 05절이 새로 바꾼 3개. 모두 의도한 변경입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/05-컨텍스트-관리와-오프로딩.ipynb` | `3e3f95dd5878` → `d27f1ddf7498` | 05절 개선(새 노트북 31 코드 셀, 새 커널 실행 A, 흔들리는 값 둘째 단락 채움·결과 읽기 두 문장 고침 `mdpatch.py`, 그림 첨부) |
| `textbook/part6/ch27-deepagents/_src/05-컨텍스트-관리와-오프로딩.html` | `3df443306242` → `050afaa59b89` | 05절 본문 10블록 다시 씀 |
| `textbook/part6/ch27-deepagents/05-컨텍스트-관리와-오프로딩.html` | `6624803769fd` → `f5ec27c3b0ec` | `_build.py` 빌드(`run_section.sh --no-exec`) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | (04 뒤 `0656205ccb45`) → `48b9345ed647` | 「품질 개선」 표에 05절 행 덧붙임 |
| `textbook/part6/ch27-deepagents/qa/verification.md` | (04 뒤 `c14a3b3891fd`) → `da93d5976954` | 「품질 개선 검증」 표에 05절 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | (04 뒤 `e6e271ece19c`) → `28a50ddc0a19` | `verify.py --chapter`가 다시 씀(공용 도구 동작 — 손으로 고치지 않음) |

- **실습 폴더 `workspace`·`workspace-05`·`workspace-08`의 목록 안 파일은 모두 같음**(05는 디스크에 쓰지 않음 — 옛 05가 쌓던 `workspace-05/large_tool_results/call_…` 여섯 개도 그대로, `find -newer 05-probe.md` 0건). 도구 파일 `harness_tools.py`(목록 밖, 02 판 `14ee39ca…`)·챕터 `qa/public-files.json`(`47aa0ac8`)·`textbook/part6/public-files.json`(`205d50ff`)은 그대로 — 05는 묶음 목록을 바꾸지 않음. 챕터 `index.html`·`chapter.json`·`_build.py`·06~08 `_src`·노트북·실습 폴더 README·잠금·앞 챕터 파일·zip·기록 파일은 모두 같습니다.
- 새로 만든 파일(목록 밖): `qa/upgrade/author_05.py`·`05-probe.md`·`05-figures.md`·`05-diagnosis.md`·`gates-wip-05.json`·`gates-wip-05-05.json`·`probe/probe05.py`·`probe/probe-05-P.jsonl`·`review-pack/05-컨텍스트-관리와-오프로딩.md` · `figures/05-1~05-4.{mmd,svg,png,caption.md,render.json}` · `figures/05-5-온실-밖으로-옮긴-퇴비-포대.{png,prompt.md,caption.md}` · `.cache/ch27-05-view/`(그림 확인 사본). `handoff.md`(목록 밖)에 「§05 → §06」과 05 완료 줄을 덧붙임. 연결 폴더 밖: 기기 `/tmp/ch27-05/`.

## 06절 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **213개 같음 · 25개 바뀜 · 0개 없어짐** — 05절 뒤 22개(01~05 노트북·`_src`·HTML·옛 생성기 둘·공개 목록 둘은 앞 절 판 그대로, 아래 표시 셋은 06이 다시 바꿈) + 06절이 새로 바꾼 3개. 모두 의도한 변경입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/06-서브에이전트-위임.ipynb` | `c05bd813c200` → `c9927ab1eb6e` | 06절 개선(새 노트북 30 코드 셀, 새 커널 실행 A, 흔들리는 값 둘째 단락 채움·설명 고침 `mdpatch.py`, 그림 첨부) |
| `textbook/part6/ch27-deepagents/_src/06-서브에이전트-위임.html` | `6ef81bf80781` → `6d62a12a69d6` | 06절 본문 10블록 다시 씀 |
| `textbook/part6/ch27-deepagents/06-서브에이전트-위임.html` | `869912633f0c` → `00d733e0377d` | `_build.py` 빌드(`run_section.sh --no-exec`) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | (05 뒤 `48b9345ed647`) → `44b3451396f1` | 「품질 개선」 표에 06절 행 덧붙임 |
| `textbook/part6/ch27-deepagents/qa/verification.md` | (05 뒤 `da93d5976954`) → `948d37225e6b` | 「품질 개선 검증」 표에 06절 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | (05 뒤 `28a50ddc0a19`) → `e5240bd05786` | `verify.py --chapter`가 다시 씀(공용 도구 동작 — 손으로 고치지 않음) |

- **실습 폴더 `workspace`·`workspace-05`·`workspace-08`의 목록 안 파일은 모두 같음**(06은 디스크에 쓰지 않음). 도구 파일 `harness_tools.py`(목록 밖, 02 판 `14ee39ca…`)·챕터 `qa/public-files.json`(`47aa0ac8`)·`textbook/part6/public-files.json`(`205d50ff`)은 그대로 — 06은 묶음 목록을 바꾸지 않음. 챕터 `index.html`·`chapter.json`·`_build.py`·07·08 `_src`·노트북·실습 폴더 README·잠금·앞 챕터 파일·zip·기록 파일은 모두 같습니다.
- 새로 만든 파일(목록 밖): `qa/upgrade/author_06.py`·`06-probe.md`·`06-figures.md`·`06-diagnosis.md`·`gates-wip-06.json`·`gates-wip-06-06.json`·`probe/probe06.py`·`probe/probe-06-P.jsonl`·`review-pack/06-서브에이전트-위임.md` · `figures/06-1~06-4.{mmd,svg,png,caption.md,render.json}` · `figures/06-5-곁-온실에-맡긴-모종.{png,prompt.md,caption.md}` · `.cache/ch27-06-view/`(그림 확인 사본). `handoff.md`(목록 밖)에 「§06 → §07」과 06 완료 줄을 덧붙임. 연결 폴더 밖: 기기 `/tmp/ch27-06/`.

## 07절 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **210개 같음 · 28개 바뀜 · 0개 없어짐** — 06절 뒤 25개(01~06 노트북·`_src`·HTML·옛 생성기 둘·공개 목록 둘은 앞 절 판 그대로, 아래 표시 셋은 07이 다시 바꿈) + 07절이 새로 바꾼 3개. 모두 의도한 변경입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/07-출처-검증형-deep-research.ipynb` | `992d162c1b45` → `9d684fab0eae` | 07절 개선(새 노트북 27 코드 셀, 새 커널 실행 A, 흔들리는 값 둘째 단락 채움 `mdpatch.py`, 그림 첨부) |
| `textbook/part6/ch27-deepagents/_src/07-출처-검증형-deep-research.html` | `7f3782622790` → `a414a0fac047` | 07절 본문 10블록 다시 씀 |
| `textbook/part6/ch27-deepagents/07-출처-검증형-deep-research.html` | `04674a830128` → `34892906e1e2` | `_build.py` 빌드(`run_section.sh --no-exec`) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | (06 뒤 `44b3451396f1`) → `626ebc60883e` | 「품질 개선」 표에 07절 행 덧붙임 |
| `textbook/part6/ch27-deepagents/qa/verification.md` | (06 뒤 `948d37225e6b`) → `63eb802396c9` | 「품질 개선 검증」 표에 07절 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | (06 뒤 `e5240bd05786`) → `b5ef5c76b56f` | `verify.py --chapter`가 다시 씀(공용 도구 동작 — 손으로 고치지 않음) |

- **도구 파일 `harness_tools.py`(목록 밖)를 07절 판으로 바꿈**: 02 판 `14ee39ca…` → **07 판 `0c4ee4f985c0fdafd093f95065644a81a7b160731d95531b7884663173a1e439`**(뒤에 Ch 16 01 `find_source_marks` 블록만 더함 — 앞머리는 02 판 글자 그대로, `author_07.check_tools()` 대조). 01~06 노트북은 가져오는 이름이 그대로라 다시 실행하지 않음(`verify.py --chapter` PASS). 두 공개 목록(`qa/public-files.json` `47aa0ac8` · `textbook/part6/public-files.json` `205d50ff`)은 그대로(도구 파일이 이미 들어 있음) — zip은 마감 때 다시 만들 것.
- **실습 폴더 `workspace`·`workspace-05`·`workspace-08`의 목록 안 파일은 모두 같음**(07은 디스크에 쓰지 않음 — 옛 07이 쓰던 `workspace/research/final.md`도 그대로, `find -newer 07-probe.md` 0건). 챕터 `index.html`·`chapter.json`·`_build.py`·08 `_src`·노트북·실습 폴더 README·잠금·앞 챕터 파일(Ch 16 `guardrails.py`는 읽기만, `d4f76099…` 그대로)·zip·기록 파일은 모두 같습니다.
- 새로 만든 파일(목록 밖): `qa/upgrade/author_07.py`·`07-probe.md`·`07-figures.md`·`07-diagnosis.md`·`gates-wip-07.json`·`gates-wip-07-07.json`·`probe/probe07.py`·`probe/probe-07-P.jsonl`·`review-pack/07-출처-검증형-deep-research.md` · `figures/07-1~07-4.{mmd,svg,png,caption.md,render.json}` · `figures/07-5-색-리본과-어미-화초.{png,prompt.md,caption.md}` · `.cache/ch27-07-view/`(그림 확인 사본). `handoff.md`(목록 밖)에 「§07 → §08」과 07 완료 줄을 덧붙임. 연결 폴더 밖: 기기 `/tmp/ch27-07/`.

## 08절 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **207개 같음 · 31개 바뀜 · 0개 없어짐** — 07절 뒤 28개(01~07 노트북·`_src`·HTML·옛 생성기 둘·공개 목록 둘은 앞 절 판 그대로, 아래 표시 셋은 08이 다시 바꿈) + 08절이 새로 바꾼 3개. 모두 의도한 변경입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/08-통합-실행과-운영-한계.ipynb` | `543fd1cc356f` → `fba43561498f` | 08절 개선(새 노트북 31 코드 셀, 새 커널 실행 A, 흔들리는 값 둘째 단락 채움 `mdpatch.py`, 그림 첨부) |
| `textbook/part6/ch27-deepagents/_src/08-통합-실행과-운영-한계.html` | `4516cbe92e3d` → `b4e1ea7f76b8` | 08절 본문 10블록 다시 씀 |
| `textbook/part6/ch27-deepagents/08-통합-실행과-운영-한계.html` | `114b433609f9` → `958abceba669` | `_build.py` 빌드(`run_section.sh --no-exec`) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | (07 뒤 `626ebc60883e`) → `0c3f6269ade2` | 「품질 개선」 표에 08절 행 덧붙임 |
| `textbook/part6/ch27-deepagents/qa/verification.md` | (07 뒤 `63eb802396c9`) → `d72c453a849a` | 「품질 개선 검증」 표에 08절 행 덧붙임 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | (07 뒤 `b5ef5c76b56f`) → `01f1da5a01bf` | `verify.py --chapter`가 다시 씀(공용 도구 동작 — 손으로 고치지 않음) |

- **도구 파일 `harness_tools.py`(목록 밖)를 08절 판으로 바꿈**: 07 판 `0c4ee4f9…` → **08 판 `7a40d99477ca7c4371a7120e6088c3ac77ed5919300091873f214694675372ed`**(뒤에 07절 노트북 셀 `check_citations`·`call_args` 블록만 더함 — 앞머리는 07 판 글자 그대로, `author_08.check_tools()` 대조). 01~07 노트북은 가져오는 이름이 그대로라 다시 실행하지 않음(`verify.py --chapter` PASS). 두 공개 목록(`qa/public-files.json` `47aa0ac8` · `textbook/part6/public-files.json` `205d50ff`)은 그대로(도구 파일이 이미 들어 있음) — zip은 마감 때 다시 만들 것.
- **실습 폴더 `workspace`·`workspace-05`·`workspace-08`의 목록 안 파일은 모두 같음**(08은 디스크에 쓰지 않음 — 옛 08이 쓰던 `workspace-08/run/report.md`도 그대로, `find -newer 08-probe.md` 0건). 챕터 `index.html`·`chapter.json`·`_build.py`·실습 폴더 README·잠금·앞 챕터 파일(Ch 24·Ch 28 `_src`는 읽기만)·zip·기록 파일은 모두 같습니다.
- 새로 만든 파일(목록 밖): `qa/upgrade/author_08.py`·`08-probe.md`·`08-figures.md`·`08-diagnosis.md`·`gates-wip-08.json`·`gates-wip-08-08.json`·`probe/probe08.py`·`probe/probe-08-P.jsonl`·`review-pack/08-통합-실행과-운영-한계.md` · `figures/08-1~08-5.{mmd,svg,png,caption.md,render.json}` · `figures/08-6-자물쇠-문과-막아-둔-문.{png,prompt.md,caption.md}` · `.cache/ch27-08-view/`(그림 확인 사본). `handoff.md`(목록 밖)에 08 완료 줄·「07절 값 추가」·「§08 → 실습(09)」·「08절 값」을 덧붙임. 연결 폴더 밖: 기기 `/tmp/ch27-08/`.

## 09절 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **201개 같음 · 37개 바뀜 · 0개 없어짐** — 08절 뒤 31개(아래 표시 여덟은 09가 다시 바꿈) + 09절이 새로 바꾼 6개. 모두 의도한 변경입니다. 01~07 노트북·`_src`·HTML(01~07 HTML은 각 절 진단의 빌드 해시와 같음 — 다시 빌드해도 바이트 같음)·옛 생성기 둘은 앞 절 판 그대로입니다.

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| `labs/part6/ch27-deepagents/notebooks/08-통합-실행과-운영-한계.ipynb` | (08 뒤 `fba43561498f`) → `ac7b0a9f8f33` | 정리 셀 끝 두 줄을 09로(`mdpatch.py` — 마크다운 셀 하나, 그림 다시 첨부). **`code_sha256` `33c153ec1ba5…`·`outputs_sha256` `d88cc3b198b6…`·`executed_at` 16:14:42Z 그대로**(다시 실행하지 않음, 셀별 출력 31/31 같음) |
| `textbook/part6/ch27-deepagents/_src/08-통합-실행과-운영-한계.html` | (08 뒤 `b4e1ea7f76b8`) → `3cf66f382148` | b8 「다음 학습과 이어지는 지점」을 09로(`author_08.py` b8 줄 → `--src-only`) |
| `textbook/part6/ch27-deepagents/08-통합-실행과-운영-한계.html` | (08 뒤 `958abceba669`) → `3f2595981a49` | 빌드(b8 · 다음 절 링크 「챕터 끝」 → 09) |
| `textbook/part6/ch27-deepagents/집필점검표.md` | (08 뒤 `0c3f6269ade2`) → `57d3684d319a` | 「품질 개선」 표에 09절 행 |
| `textbook/part6/ch27-deepagents/qa/verification.md` | (08 뒤 `d72c453a849a`) → `c1bdc74b5060` | 「품질 개선 검증」 표에 09절 행 |
| `textbook/part6/ch27-deepagents/qa/public-files.json` | (02 뒤 `47aa0ac881a8`) → `80e9d01bdac5` | 09 노트북 한 줄(08 노트북 줄 뒤). 이 챕터 목록에는 원래 HTML 줄이 없어 HTML은 넣지 않음 |
| `textbook/part6/public-files.json` | (02 뒤 `205d50ff5b4c`) → `e43894fa22f1` | `collect_public_files.py` → 09 노트북 한 줄(`Explicit public files: 88; prerequisites: 13`, `prerequisite-files.json` 바이트 같음) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json` | (08 뒤 `01f1da5a01bf`) → `b4abdcfab490` | `verify.py --chapter`가 다시 씀(09 줄 — 공용 도구 동작) |
| `labs/part6/ch27-deepagents/README.md` | `acdc92015a64` → `938c32274678` | **새로 바꿈** — 맨 아래 09절 한 단락만(옛 첫 단락·`workspace*` 설명·07 옛 사용량은 마감 몫) |
| `textbook/part6/ch27-deepagents/chapter.json` | `dcb80fff84a2` → `440ca1b90678` | **새로 바꿈** — `sections`에 09 추가. `hours`·`objectives` 그대로 |
| `textbook/part6/ch27-deepagents/index.html` | `4d1905bece8f` → `1b5c2c684c66` | **새로 바꿈** — 빌드(절 9개) |
| `textbook/part6/index.html` | `5c19e32c3318` → `651f22ffd427` | **새로 바꿈** — `_build_index.py`(Ch 27 「9절」·09 링크, `Ch 21–29 · 54절`) |
| `textbook/downloads/part6-practice.zip` | `110579388680` → `23a4d586b49f` | **새로 바꿈** — `_build_index.py`(`Part 6: 54 verified sections; 104 bundled files`). zip 안 Ch 27 13항목이 디스크와 같음, `__pycache__`·`workspace*`·`.env` 0 |
| `textbook/part6/qa/integration-results.json` | `c352bd9fe9f3` → `9501518b7d6a` | **새로 바꿈** — `_build_index.py`가 다시 씀 |

- 도구 파일 `harness_tools.py`(목록 밖)는 **08 판 `7a40d994…` 그대로**(09는 쓰지 않음 — `author_09.check_tools()`가 디스크 == 08 판 확인). 실습 폴더 `workspace*` 목록 안 파일 모두 같음(09는 디스크에 쓰지 않음). `pyproject.toml`·`uv.lock`·`_build.py`·`textbook/index.html`·`llm-practice.zip`·`delivery-results.json`·앞 챕터 파일·뒤 챕터 파일(Ch 28 `_src`는 읽기만)은 모두 같습니다.
- 새로 만든 파일(목록 밖): 노트북 `09-DeepAgents-실습.ipynb` · `_src/09-DeepAgents-실습.html` · 빌드 `09-DeepAgents-실습.html` · `qa/upgrade/author_09.py`·`09-probe.md`·`09-figures.md`·`09-diagnosis.md`·`gates-wip-09.json`·`gates-wip-09-09.json`·`gates-wip-ch27-after09.json`·`probe/probe09.py`·`probe/probe-09-A.jsonl`·`probe/probe-09-B.jsonl`·`review-pack/09-DeepAgents-실습.md` · `figures/09-1~09-3.{mmd,svg,png,caption.md,render.json}` · `figures/09-4-심기-전-모종과-바로-심은-모종.{png,prompt.md,caption.md}` · `.cache/ch27-09-view/view1.png`(그림 확인 사본). 목록 밖을 고친 파일: `qa/upgrade/author_08.py`(b8 줄 · 정리 끝 두 줄 — `cfe161ae` → `68833ee1`) · `review-pack/08-통합-실행과-운영-한계.md`(다시 묶음) · `handoff.md`(09 완료 줄·「실습 → 챕터 검토」). 연결 폴더 밖: 기기 `/tmp/ch27-09/`.

## 마감 뒤 (2026-09-28)

`before-manifest.json`(238개)을 다시 계산했습니다: **188개 같음 · 48개 바뀜 · 2개 옮김(없어짐)** — 모두 의도한 변경입니다. 09절 뒤 37개 가운데 마감이 다시 바꾼 31개 + 옮긴 2개 + 09절 뒤 그대로인 4개(06 노트북 `c9927ab1`·챕터 공개 목록 `80e9d01b`·Part 6 공개 목록 `e43894fa`·notebook-contracts `b4abdcfa`) + **마감이 새로 바꾼 13개**. 노트북 코드·출력·`executed_at`은 아홉 모두 그대로입니다(마크다운만).

| 파일 | 전 → 후(sha256 앞 12자) | 까닭 |
|---|---|---|
| 노트북 01·02·03·04·05·07·08 | (09 뒤) `056ea2d4`·`f031b310`·`1eed50d9`·`4ab0023c`·`d27f1ddf`·`9d684fab`·`ac7b0a9f` → `5bd52b6f`·`bfdade30`·`cbd6fc87`·`0896cbd7`·`d8d3c324`·`2c6423e4`·`70decb2f` | 검토 반영 마크다운 셀만(01·03은 첨부 그림 01-1·03-1도 새 PNG). **`code_sha256`·`outputs_sha256`·`executed_at` 그대로**. 06 노트북은 바뀐 셀 없음(06-3은 첨부가 아님). 09 노트북(목록 밖) `b64bcc16` → `084d2c03` |
| `_src/01~08-*.html` | (09 뒤) → `9974664f`·`077fdc74`·`0ff91075`·`00c5cef8`·`bf38841d`·`81c9468b`·`289e17ba`·`724496a7` | 생성기 `src_html()`(검토 반영 — 요약 §19). 09 `_src`(목록 밖) `63adf10d` → `36210cc4` |
| 빌드 HTML 01~08 · 챕터 `index.html` | (09 뒤) → `52378ee6`·`1013ac28`·`510526e4`·`01f1cc38`·`35015546`·`66bba86c`·`d7236f9b`·`55577df2` · `index.html` `1b5c2c68` → `98837cf8` | `run_section.sh … --no-exec`·`_build.py`(목표 넷). 09 HTML(목록 밖) → `7958dde3` |
| `labs/part6/ch27-deepagents/README.md` | `938c3227` → `28c36066` | 전체 다시 씀(검토 A-15·B-12 — 요약 §13) |
| `textbook/part6/ch27-deepagents/chapter.json` | `440ca1b9` → `cc55e8e6` | `objectives` 셋 → 넷, `hours` 그대로 |
| `집필점검표.md` · `qa/verification.md` | `57d3684d` → `563d29ea` · `c1bdc74b` → `5b454f2e` | 머리 「개선 전 판」 표시 + 끝 「마감」 절 |
| `qa/research.md` · `qa/technical-review.md` | → `94d6cbc0` · `65530f89` | **새로 바꿈** — 머리 「개선 전 판」 표시만(내용 그대로) |
| `labs/part6/continuity-guide.md` | → `cb0e8bd1` | **새로 바꿈** — 13행 Ch 27 칸(8·12행 그대로) |
| `textbook/part6/_build_index.py` | → `971a81e0` | **새로 바꿈** — ch27 설명 줄(시수 8·16 그대로) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | → `907ebc44` · `18479837` → `2c14ab24` | **새로 바꿈** — Ch 27 설명(절 수 8 그대로), 목차는 Ch 27 행 한 줄만 바뀜(옛 스크립트 출력 = 옛 `index.html` 바이트 같음 확인) |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | `651f22ff` → `ca9b9ff9` · `23a4d586` → `1a20c73c` · `9501518b` → `7eacc30b` | `_build_index.py` 한 번(`Part 6: 54 verified sections; 104 bundled files`) — 목차는 Ch 27 설명 한 줄만, zip 안 Ch 27 13항목·continuity-guide 디스크와 같음 |
| `textbook/part6/qa/bundle-execution.json` | `4f1cd14a` → `4f39acac` | **새로 바꿈** — `check_bundle_execution.py` PASS(새 zip 해시) |
| `textbook/part6/qa/visual-results.json` | → `23a6919e` | **새로 바꿈** — Ch 27 줄만 18 → 20, `screens` 126 → 128 |
| `textbook/_notebook/checks/ch27-deepagents/visual-results.json` + 스크린숏 넷 | → `56c8c4cb` · `index-1280` `cf655b48` · `index-390` `53c04e9e` · `01-…-1280` `0c1aae4d` · `01-…-390` `91f4b092` | **새로 바꿈** — `visual.cjs` 20행 PASS |
| `qa/author_ch27.py` · `figures/_gen_figures.py` | `7bc6c96d` · `98641eb5` → **옮김** | `mv -n` → `qa/upgrade/before/generators/blocked/`(해시 같음, 부르는 스크립트 0) |

- 되돌린 것: `textbook/part6/qa/notebook-readiness.json`(옛 `check_notebook_readiness.py`가 멈추기 전에 씀 → 실행 전 사본으로, `b3d69e9c` 같음).
- 목록 밖으로 바꾼 것: 도구 파일은 **그대로** `7a40d994…` · 생성기 `author_01~09.py`(문자열만 — 도구 파일 줄·코드 셀 상수 그대로) · 그림 `01-1`·`03-1`·`03-2`·`03-3`·`03-4`·`06-3`(`.mmd`·`.svg`·`.png`·`.render.json`)과 캡션 `01-1`·`03-1`·`03-2`·`03-4`·`06-3` · 진단 아홉 끝 「마감 반영」 · `01`·`03`·`06-figures.md` · `02-probe.md` §0 머리 · `handoff.md`(금지어 줄·허용 문법 예외 한 줄·끝 「검토 반영과 챕터 마감」) · `chapter-summary.md`(새) · `gates-after.json`(새) · `gates-wip-01`~`09.json`(`run_section.sh --no-exec`가 다시 씀) · `textbook/qa/upgrade-progress.md`(Ch 27 행) · `textbook/qa/upgrade-final-checklist.md`(§2-13 6번·§2-15·§3·§4).
- 실습 폴더 `workspace*` 목록 안 파일 9개 모두 같음(삭제 승인 목록 — 지우지 않음). `pyproject.toml`·`uv.lock` 같음.
