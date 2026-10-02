# 보호 파일 변경 기록 (`before-manifest.json` 226개 대조)

준비 담당이 만든 `qa/upgrade/before-manifest.json`(226개, `e5259ab8…`)의 sha256과 절 작업 뒤 디스크를 대조한 기록입니다. 없어진 파일은 0개입니다.

## 01절 뒤 (2026-09-28)

바뀐 파일 **6개**(모두 01절 작업의 예정된 결과, 나머지 220개 같음):

| 파일 | 전 → 후(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch28-mcp/_src/01-MCP-구조와-capability-협상.html` | `f6b7f696` → `2f7404e7` | 01절 본문 다시 씀(`author_01.py`) |
| `textbook/part6/ch28-mcp/01-MCP-구조와-capability-협상.html` | `2a8b009b` → `55434f0f` | `_build.py` 빌드 |
| `labs/part6/ch28-mcp/notebooks/01-MCP-구조와-capability-협상.ipynb` | `0e891d39` → `049d4608` | 01절 노트북 다시 씀 + 새 커널 실행 + 그림 첨부(`code_sha256` `a09d959cecc4…` → `2407c4c57138…` — **묶음 실행 검사 계약 값이 바뀜, 마감에서 zip·검사 다시**) |
| `textbook/part6/ch28-mcp/qa/author_ch28.py` | `6806d465` → `41a3af28` | 옛 생성기 막기(설명 주석 셋 + `raise SystemExit`, 원본 사본 `qa/upgrade/before/generators/author_ch28.py` 해시 같음) |
| `textbook/part6/ch28-mcp/figures/_gen_figures.py` | `dadf0c2b` → `5bb85474` | 옛 도식 생성기 막기(같은 모양, 원본 사본 `before/generators/_gen_figures.py`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json` | `70eba133` → `6e8b8224` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **바뀌지 않은 것(확인)**: `labs/part6/ch28-mcp/course_server.py`(`d7f7e8b9…`) · 실습 폴더 `__pycache__/course_server.cpython-312.pyc`(09-10 15:52 그대로 — 새 판 01은 `runpy.run_path`로 읽어 pyc를 쓰지 않음) · `chapter.json`·`index.html`·`_build.py` · 02~05 `_src`·HTML·노트북 · 공개 목록 둘 · `part6-practice.zip`(`1a20c73c…`) · `bundle-execution.json`(`4f39acac…`) · Ch 27 09 `_src`·HTML·노트북·`author_09.py` · 과정 문서·공용 도구 전부.
- 새로 생긴 파일(목록 밖): `qa/upgrade/author_01.py`·`01-figures.md`·`01-diagnosis.md`·`handoff.md`·`manifest-changes.md`·`gates-wip-01-01.json`·`gates-wip-01.json`·`review-pack/01-…md` · `figures/01-1~01-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/01-5-도킹-고리-셋과-우주선-둘.{png,caption.md,prompt.md}` · 사용자 디스크 `.cache/ch28-01-view/`(그림 확인 사본 다섯).

## 02절 뒤 (2026-09-28)

바뀐 파일 **11개**(01절 뒤 6개 + 이번 5개, 나머지 215개 같음, 없어진 것 0). 01 뒤 6개의 해시는 01 기록 값 그대로입니다(02가 다시 빌드한 01 HTML도 `55434f0f` 그대로).

| 파일 | 전 → 후(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch28-mcp/_src/02-FastMCP-로컬-서버-제작.html` | `634fe88f` → `7cf24dd8` | 02절 본문 다시 씀(`author_02.py`, 뒤에 `mdpatch.py` 두 번) |
| `textbook/part6/ch28-mcp/02-FastMCP-로컬-서버-제작.html` | `c2a30758` → `54e85c46` | `_build.py` 빌드 |
| `labs/part6/ch28-mcp/notebooks/02-FastMCP-로컬-서버-제작.ipynb` | `142dc81d` → `19d05788` | 02절 노트북 다시 씀 + 새 커널 실행 + 그림 첨부 + 설명 `mdpatch`(`code_sha256` `55bbba9402b5…` → `687062053d18…`, 코드 셀 4 → 24 — 02는 묶음 실행 검사 대상이 아님) |
| `textbook/part6/ch28-mcp/집필점검표.md` | `bc7a790b` → `00200162` | 「품질 개선」 표에 01 행(01절이 더함 — 01 기록에는 빠져 있음)·02 행 |
| `textbook/part6/ch28-mcp/qa/verification.md` | `37f3aa6c` → `ea7c0bbc` | 「품질 개선 검증」 표에 01 행(01절)·02 행 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json` | `6e8b8224`(01 뒤) → `395a6c6b` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **바뀌지 않은 것(확인)**: `labs/part6/ch28-mcp/course_server.py`(`d7f7e8b9…`) · 실습 폴더 `__pycache__/course_server.cpython-312.pyc`(09-10 15:52 그대로) · 01 `_src`·HTML·노트북(01 뒤 값 그대로, 01 `code_sha256` `2407c4c57138…`) · `chapter.json`·`index.html`·`_build.py` · 03~05 `_src`·HTML·노트북 · 공개 목록 둘 · `part6-practice.zip`(`1a20c73c…`) · `bundle-execution.json`(`4f39acac…`) · 도구 파일(없음) · Ch 19·27 파일 · 과정 문서·공용 도구 전부.
- 새로 생긴 파일(목록 밖): `qa/upgrade/author_02.py`(`1c89a565…`)·`02-figures.md`·`02-diagnosis.md`·`gates-wip-02-02.json`·`gates-wip-02.json`·`review-pack/02-FastMCP-로컬-서버-제작.md` · `figures/02-1~02-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/02-5-테두리-없는-해치와-네모-테두리-해치.{png,caption.md,prompt.md}` · 사용자 디스크 `.cache/ch28-02-view/`(그림 확인 사본 여섯). `handoff.md`(「02절 완료」 한 줄·「§02 → §03」)·이 파일은 덧붙임.


## 03절 뒤 (2026-09-28)

바뀐 파일 **16개**(02절 뒤 11개 + 이번 5개, 나머지 210개 같음, 없어진 것 0). 01·02의 `_src`·HTML·노트북 해시는 02 기록 값 그대로입니다(03이 다시 빌드한 01·02 HTML도 `55434f0f`·`54e85c46` 그대로).

| 파일 | 전 → 후(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch28-mcp/_src/03-stdio와-원격-전송-권한-경계.html` | `e98e8fda` → `e4034c7b` | 03절 본문 다시 씀(`author_03.py`) |
| `textbook/part6/ch28-mcp/03-stdio와-원격-전송-권한-경계.html` | `97ba8fbb` → `02326cae` | `_build.py` 빌드 |
| `labs/part6/ch28-mcp/notebooks/03-stdio와-원격-전송-권한-경계.ipynb` | `5f4b7827` → `3ea536db` | 03절 노트북 다시 씀 + 새 커널 실행 + 그림 첨부 + 「오늘 볼 그림」 설명 `mdpatch`(`code_sha256` `2165ed1b94ce…` → `04c437f720bc…`, 코드 셀 5 → 25 — 03은 묶음 실행 검사 대상이 아님) |
| `textbook/part6/ch28-mcp/qa/public-files.json` | `e4a7455c` → `1d6d2416` | 새 파일 세 줄(`env_server.py`·`auth_server.py`·`notebooks/connect_tools.py`) |
| `textbook/part6/public-files.json` | `e43894fa` → `7b66b4f9` | `collect_public_files.py`가 다시 모음(차이는 위 세 줄뿐) |
| `textbook/part6/ch28-mcp/집필점검표.md` | `00200162`(02 뒤) → `b19301a8` | 「품질 개선」 표에 03 행 |
| `textbook/part6/ch28-mcp/qa/verification.md` | `ea7c0bbc`(02 뒤) → `136f3635` | 「품질 개선 검증」 표에 03 행 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json` | `395a6c6b`(02 뒤) → `a90b1fde` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **바뀌지 않은 것(확인)**: `labs/part6/ch28-mcp/course_server.py`(`d7f7e8b9…`) · 실습 폴더 `__pycache__/course_server.cpython-312.pyc`(09-10 15:52 그대로) · 01 노트북(`code_sha256` `2407c4c57138…`)·02 노트북(`687062053d18…`) · `chapter.json`·`index.html`·`_build.py` · 04·05 `_src`·HTML·노트북 · `textbook/part6/prerequisite-files.json`(다시 모았지만 바이트 같음) · `part6-practice.zip`(`1a20c73c…`)·`bundle-execution.json`(`4f39acac…`) · README·잠금 · Ch 19·23·27 파일 · 과정 문서·공용 도구 전부.
- 새로 생긴 파일(목록 밖): 실습 폴더 `env_server.py`(`8b4c40bc…`)·`auth_server.py`(`8f41e542…`)·`notebooks/connect_tools.py`(`9139c4f8…`)·`notebooks/__pycache__/connect_tools.cpython-312.pyc`(커널 가져오기) · `qa/upgrade/author_03.py`(`91b4a00b…`)·`03-figures.md`·`03-diagnosis.md`·`gates-wip-03-03.json`·`gates-wip-03.json`·`review-pack/03-stdio와-원격-전송-권한-경계.md` · `figures/03-1~03-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/03-5-짧은-통로와-긴-통로.{png,caption.md,prompt.md}` · 사용자 디스크 `.cache/ch28-03-view/`(그림 확인 사본 하나). `handoff.md`(「03절 완료」 한 줄·「§03 → §04」)·이 파일은 덧붙임.


## 04절 뒤 (2026-09-28)

바뀐 파일 **19개**(03절 뒤 16개 + 이번 3개, 나머지 207개 같음, 없어진 것 0). 01~03의 `_src`·HTML·노트북 해시는 03 기록 값 그대로입니다(04가 다시 빌드한 01·02·03 HTML도 `55434f0f`·`54e85c46`·`02326cae` 그대로).

| 파일 | 전 → 후(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch28-mcp/_src/04-LangChain-MCP-클라이언트-연동.html` | `863111c6` → `4174ea74` | 04절 본문 다시 씀(`author_04.py`) |
| `textbook/part6/ch28-mcp/04-LangChain-MCP-클라이언트-연동.html` | `d5735b9f` → `1a481e22` | `_build.py` 빌드 |
| `labs/part6/ch28-mcp/notebooks/04-LangChain-MCP-클라이언트-연동.ipynb` | `58f6c302` → `13b49a27` | 04절 노트북 다시 씀 + 새 커널 실행 + 자리 표시 `mdpatch` + 그림 첨부(`code_sha256` `aa628c23c529…` → `7bd03afa0ca1…`, 코드 셀 3 → 25 — 04는 묶음 실행 검사 대상이 아님) |
| `textbook/part6/ch28-mcp/집필점검표.md` | `b19301a8`(03 뒤) → `dd5314d7` | 「품질 개선」 표에 04 행 |
| `textbook/part6/ch28-mcp/qa/verification.md` | `136f3635`(03 뒤) → `2fa48b12` | 「품질 개선 검증」 표에 04 행 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json` | `a90b1fde`(03 뒤) → `613684f2` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **바뀌지 않은 것(확인)**: `labs/part6/ch28-mcp/course_server.py`(`d7f7e8b9…`) · 실습 폴더 `__pycache__/course_server.cpython-312.pyc`(09-10 15:52 그대로) · 01·02·03 노트북(`code_sha256` `2407c4c57138…`·`687062053d18…`·`04c437f720bc…`) · `chapter.json`·`index.html`·`_build.py` · 05 `_src`·HTML·노트북 · 공개 목록 둘(03 뒤 값 그대로 — 04 새 공개 파일 없음) · `part6-practice.zip`(`1a20c73c…`)·`bundle-execution.json`(`4f39acac…`) · README·잠금 · Ch 19~27 파일(`runner_tools.py` `f4113158…`·`harness_tools.py` `7a40d994…` 읽기만) · 과정 문서·공용 도구 전부.
- **목록 밖에서 바뀐 것**: `labs/part6/ch28-mcp/notebooks/connect_tools.py` `9139c4f8…`(03 판) → `cc066bd7…`(04 판 — 함수 넷·`import sys` 더함, 03 글 그대로 담음) · `notebooks/__pycache__/connect_tools.cpython-312.pyc`(커널 가져오기가 21:25에 다시 씀) · `env_server.py`·`auth_server.py` 그대로.
- 새로 생긴 파일(목록 밖): `qa/upgrade/author_04.py`(`51958a06…`)·`04-figures.md`·`04-diagnosis.md`·`04-probe.md`·`probe/probe04.py`(`f5417f95…`)·`probe/probe-04-P.jsonl`(`f8d0aac7…`)·`gates-wip-04-04.json`·`gates-wip-04.json`·`review-pack/04-LangChain-MCP-클라이언트-연동.md` · `figures/04-1~04-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/04-5-이음-부품으로-이은-모듈.{png,caption.md,prompt.md}` · 사용자 디스크 `.cache/ch28-04-view/`(그림 확인 사본 둘). `handoff.md`(「04절 완료」 한 줄·「§04 → §05」)·이 파일은 덧붙임.


## 05절 뒤 (2026-09-28)

바뀐 파일 **22개**(04절 뒤 19개 + 이번 3개, 나머지 204개 같음, 없어진 것 0). 01~04의 `_src`·HTML·노트북 해시는 04 기록 값 그대로입니다(05가 다시 빌드한 01~04 HTML도 `55434f0f`·`54e85c46`·`02326cae`·`1a481e22` 그대로).

| 파일 | 전 → 후(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch28-mcp/_src/05-도구-정의와-첫-호출-토큰.html` | `8ab2e073` → `5dd681ea` | 05절 본문 다시 씀(`author_05.py`) |
| `textbook/part6/ch28-mcp/05-도구-정의와-첫-호출-토큰.html` | `4392e27b` → `ddc0fae3` | `_build.py` 빌드 |
| `labs/part6/ch28-mcp/notebooks/05-도구-정의와-첫-호출-토큰.ipynb` | `8f489c06` → `c7a489bb` | 05절 노트북 다시 씀 + 새 커널 실행 + 자리 표시 `mdpatch` + 그림 첨부(`code_sha256` `497b3ecd342c…` → `b99a57642e5d…`, 코드 셀 6 → 28 — 05는 묶음 실행 검사 대상이 아님) |
| `textbook/part6/ch28-mcp/집필점검표.md` | `dd5314d7`(04 뒤) → `405c9c92` | 「품질 개선」 표에 05 행 |
| `textbook/part6/ch28-mcp/qa/verification.md` | `2fa48b12`(04 뒤) → `67cc33f4` | 「품질 개선 검증」 표에 05 행 |
| `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json` | `613684f2`(04 뒤) → `8ddfae9a` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀 |

- **바뀌지 않은 것(확인)**: `labs/part6/ch28-mcp/course_server.py`(`d7f7e8b9…`) · 실습 폴더 `__pycache__/course_server.cpython-312.pyc`(09-10 15:52 그대로 — `runpy.run_path`는 pyc를 쓰지 않음) · 01·02·03·04 노트북(`code_sha256` `2407c4c57138…`·`687062053d18…`·`04c437f720bc…`·`7bd03afa0ca1…`) · `chapter.json`·`index.html`·`_build.py` · 공개 목록 둘(04 뒤 값 그대로 — 05 새 공개 파일 없음) · `part6-practice.zip`(`1a20c73c…`)·`bundle-execution.json`(`4f39acac…`) · README·잠금 · Ch 19~27 파일(Ch 19 03 노트북 `f0d83063…` 읽기만) · 과정 문서·공용 도구 전부.
- **목록 밖에서 바뀐 것**: `labs/part6/ch28-mcp/notebooks/connect_tools.py` `cc066bd7…`(04 판) → **`570ed3cc…`(05 판 — `spec_length`·가져오기 두 줄 더함, 04 글 그대로 담음)** · `notebooks/__pycache__/connect_tools.cpython-312.pyc`(커널 가져오기가 22:08에 다시 씀) · `env_server.py`·`auth_server.py` 그대로.
- 새로 생긴 파일(목록 밖): `qa/upgrade/author_05.py`(`df4d186d…`)·`05-figures.md`·`05-diagnosis.md`·`05-probe.md`·`probe/probe05.py`(`8ab1193a…`)·`probe/probe-05-P.jsonl`(`1d29a28f…`)·`gates-wip-05-05.json`·`gates-wip-05.json`·`review-pack/05-도구-정의와-첫-호출-토큰.md` · `figures/05-1~05-4-*.{mmd,svg,png,caption.md,render.json}` · `figures/05-5-모듈-수만큼-쌓이는-설명서.{png,caption.md,prompt.md}` · 사용자 디스크 `.cache/ch28-05-view/`(그림 확인 사본 다섯). `handoff.md`(「05절 완료」 한 줄·「§05 → 실습(06)」)·이 파일은 덧붙임.

## 06절 뒤 (2026-09-28)

바뀐 파일 **28개**(05절 뒤 22개 + 이번 6개, 나머지 198개 같음, 없어진 것 0). 01~04의 `_src`·HTML·노트북 해시는 05 기록 값 그대로입니다(06이 다시 빌드한 01~04 HTML도 `55434f0f`·`54e85c46`·`02326cae`·`1a481e22` 그대로).

| 파일 | 전 → 후(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch28-mcp/chapter.json` | `062fd0dc` → `f4b0bbc6` | **새로 바뀜** — `sections`에 06절(`06-MCP-실습`, experiment) 추가, `hours`·`objectives` 그대로 |
| `textbook/part6/ch28-mcp/index.html` | `fdf7b95d` → `a3b20d23` | **새로 바뀜** — `_build.py`가 06절 목록 줄을 더함 |
| `labs/part6/ch28-mcp/README.md` | `5b72cb94` → `9cd50583` | **새로 바뀜** — 맨 아래 06절 한 단락(옛 본문은 마감 몫) |
| `textbook/part6/index.html` | `ca9b9ff9` → `a4964c57` | **새로 바뀜** — `_build_index.py`(Ch 28 「6절」·06 링크, `Ch 21–29 · 55절`) |
| `textbook/downloads/part6-practice.zip` | `1a20c73c` → `1a4059ab` | **새로 바뀜** — `_build_index.py`(Ch 28 13항목 디스크와 같음, **zip 안 01이 새 판 `2407c4c57138…`** — `bundle-execution.json` `4f39acac…`는 옛 zip 기준, 묶음 실행 검사는 마감 몫) |
| `textbook/part6/qa/integration-results.json` | `7eacc30b` → `8cc9b160` | **새로 바뀜** — `_build_index.py`(55절·108파일) |
| `textbook/part6/ch28-mcp/_src/05-도구-정의와-첫-호출-토큰.html` | `5dd681ea`(05 뒤) → `cab679ba` | b8 「다음 학습과 이어지는 지점」을 06으로(`author_05.py --src-only`) |
| `textbook/part6/ch28-mcp/05-도구-정의와-첫-호출-토큰.html` | `ddc0fae3`(05 뒤) → `7f4fa4ec` | 빌드(다음 절 링크 · b8) |
| `labs/part6/ch28-mcp/notebooks/05-도구-정의와-첫-호출-토큰.ipynb` | `c7a489bb`(05 뒤) → `9b4b0138` | 정리 끝 문장 `mdpatch.py`(마크다운 셀 59만 — **`code_sha256` `b99a57642e5d…`·`outputs_sha256` `a080eff183cf…`·`executed_at` 22:08:27Z 그대로**) |
| `textbook/part6/ch28-mcp/집필점검표.md` | `405c9c92`(05 뒤) → `b9eae81f` | 「품질 개선」 표에 06 행 |
| `textbook/part6/ch28-mcp/qa/verification.md` | `67cc33f4`(05 뒤) → `ee6fb4cb` | 「품질 개선 검증」 표에 06 행 |
| `textbook/part6/ch28-mcp/qa/public-files.json` | `1d6d2416`(03 뒤) → `68b20d31` | 06 HTML·06 노트북 두 줄 |
| `textbook/part6/public-files.json` | `7b66b4f9`(03 뒤) → `498845c7` | `collect_public_files.py` — 06 노트북 한 줄(`Explicit public files: 92; prerequisites: 13`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json` | `8ddfae9a`(05 뒤) → `4a0e20c6` | `run_section.sh` 안 `verify.py --chapter`가 다시 씀(06절 더함) |

- **바뀌지 않은 것(확인)**: 서버 파일 셋(`course_server.py` `d7f7e8b9…`) · 도구 파일 `connect_tools.py` 05 판 `570ed3cc…`(목록 밖) · `notebooks/__pycache__/connect_tools.cpython-312.pyc`(22:08 그대로 — 06 커널은 다시 쓰지 않음)·실습 폴더 `__pycache__/course_server.cpython-312.pyc`(09-10) · 01·02·03·04 노트북(`code_sha256` 그대로) · `_build.py` · `prerequisite-files.json` · `pyproject.toml`·`uv.lock` · `bundle-execution.json`(`4f39acac…` — 이제 옛 값)·`delivery-results.json`(`3cc2d143…`)·`llm-practice.zip` · `textbook/index.html` · Ch 19~27·29 파일 · 과정 문서·공용 도구 전부.
- 새로 생긴 파일(목록 밖): 노트북 `06-MCP-실습.ipynb`(`4ad6dfbd…`, `code_sha256` `b36b5fc9b595…`) · `_src/06-MCP-실습.html`(`9e735b71…`) · `06-MCP-실습.html`(`505e9e50…`) · `qa/upgrade/author_06.py`(`89312a3a…`)·`06-probe.md`·`06-figures.md`·`06-diagnosis.md`·`probe/probe06.py`(`68961241…`)·`probe/probe-06-P.jsonl`(`402354d6…`)·`gates-wip-06-06.json`·`gates-wip-06.json`·`gates-wip-ch28-after06.json`·`review-pack/06-MCP-실습.md` · `figures/06-1~06-3-*.{mmd,svg,png,caption.md,render.json}` · `figures/06-4-받침대에-꽂은-통-하나와-셋.{png,caption.md,prompt.md}` · 사용자 디스크 `.cache/ch28-06-view/illu-1-1100.png`. `handoff.md`(「06절 완료」 한 줄·「실습 → 챕터 검토」)·`author_05.py`(`df4d186d` → `9f24c15a`, 05 문장 둘)·`review-pack/05-…md`(다시 만듦)·이 파일은 덧붙임·고침.

## 마감 뒤 (2026-09-28 — 검토 1차 반영·챕터 마감)

`python3 .cache/ch28-close/tools/manifest_check.py` → **226개 가운데 183 같음 · 41 바뀜 · 2 옮김(없어짐)** — 모두 의도한 것. 아래 「마감 전」은 06절 뒤(마감 시작 때) 해시입니다.

| 파일 | 마감 전 → 후(앞 8자) | 까닭 |
|---|---|---|
| `textbook/part6/ch28-mcp/chapter.json` | `f4b0bbc6` → `e2eaf6c8` | `objectives` 넷 → 다섯(`hours` 그대로) |
| `textbook/part6/ch28-mcp/index.html` | `a3b20d23` → `5e7123eb` | `_build.py`(목표 다섯) |
| `textbook/part6/ch28-mcp/_src/01~05-*.html` | `2f7404e7`·`7cf24dd8`·`e4034c7b`·`4174ea74`·`cab679ba` → `13d7aa5c`·`d48b0863`·`20904b1e`·`7fcc3830`·`9d60e4d6` | 검토 반영 글(01 A-1·A-2 · 02 A-5 · 03 A-9~A-14 · 04 B-1·B-2·B-11 · 05 B-4·B-6) — 생성기 `src_html()` |
| `textbook/part6/ch28-mcp/01~05-*.html` | `55434f0f`·`54e85c46`·`02326cae`·`1a481e22`·`7f4fa4ec` → `f565477a`·`268c6375`·`b4358dae`·`d1e094ca`·`38f81af7` | 빌드(글·03 새 출력·03-3·03-4 그림) |
| `labs/part6/ch28-mcp/notebooks/01·02·04·05-*.ipynb` | `049d4608`·`19d05788`·`13b49a27`·`9b4b0138` → `ee6068c3`·`46231dee`·`78cbb550`·`d4db557b` | 마크다운 셀만(**`code_sha256`·`outputs_sha256`·`executed_at` 그대로**) |
| `labs/part6/ch28-mcp/notebooks/03-*.ipynb` | `3ea536db` → `c1f22daa` | **다시 실행**(`code_sha256` `04c437f720bc…` → `0935bc12bf4e…`, 셀 55 → 57) |
| `labs/part6/ch28-mcp/README.md` | `9cd50583` → `2de0808f` | 전체 다시 씀 |
| `labs/part6/ch28-mcp/course_server.py` | `d7f7e8b9` → `5dc77333` | 문법만(f-string 둘·제너레이터 식 하나) — 값 같음(`srvcmp.py` 18항목) |
| `textbook/part6/ch28-mcp/qa/public-files.json` | `68b20d31` → `e0533bb7` | 옛 SVG 다섯 줄 뺌 |
| `textbook/part6/ch28-mcp/qa/research.md` | `0bf952e8` → `a0325b2a` | 머리에 「개선 전 판」 표시 |
| `textbook/part6/ch28-mcp/qa/verification.md` · `집필점검표.md` | `ee6fb4cb`·`b9eae81f` → `4e2b3902`·`743d17ad` | 머리 표시 + 끝 「마감」 절 |
| `textbook/part6/_build_index.py` | `971a81e0` → `2020202a` | ch28 설명 줄(시수 5·11 그대로) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | `907ebc44` · `2c14ab24` → `cde0dc13` · `64bfbb36` | Ch 28 설명(절 수 5 그대로) — 목차는 Ch 28 설명만 바뀜(옛 스크립트 출력 = 옛 `index.html` 바이트 같음 확인) |
| `labs/part6/continuity-guide.md` | `cb0e8bd1` → `f549f3ad` | 14행 Ch 28 줄(「Ch37」·「측정」 뺌) |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | `a4964c57` · `1a4059ab` · `8cc9b160` → `4e3d5941` · `5002dce3` · `7a46d6c8` | `_build_index.py` 한 번(`Part 6: 55 verified sections; 108 bundled files`) — 목차는 Ch 28 설명 한 줄만 |
| `textbook/part6/qa/bundle-execution.json` | `4f39acac` → `fc4e1b78` | `check_bundle_execution.py` PASS(새 zip, **Ch 28 01 `2407c4c57138…`**) |
| `textbook/part6/qa/visual-results.json` | `23a6919e` → `24d74549` | Ch 28 줄만 12 → 14, `screens` 128 → 130 |
| `textbook/_notebook/checks/ch28-mcp/visual-results.json` + 스크린숏 넷 | → `831667dd` · `01-…-1280` `32d4484f` · `01-…-390` `65e2d92b` · `index-1280` `7b122ac5` · `index-390` `30cd500f` | `visual.cjs` 14행 PASS |
| `textbook/_notebook/checks/notebook-contracts-part6-ch28-mcp.json` | `4a0e20c6` → `1613295a` | `verify.py --chapter`(03 셀 26) |
| `textbook/qa/upgrade-contracts.md` · `upgrade-final-checklist.md` | → `288e1d48` · `34cb850f` | 계약 §5 「Ch28 마감 뒤」 · 체크리스트 §2-16·§3·§4·§2-13 6번 한 줄 |
| `qa/author_ch28.py` · `figures/_gen_figures.py` | `41a3af28` · `5bb85474`(01절이 막은 판) → **옮김** | `mv -n` → `qa/upgrade/before/generators/blocked/`(해시 같음, 부르는 스크립트 0) |

- 06절 뒤에 바뀐 뒤 마감이 바이트를 바꾸지 않은 것: `textbook/part6/public-files.json`(`498845c7` — `collect_public_files.py`를 다시 돌려 같음).
- 되돌린 것: `textbook/part6/qa/notebook-readiness.json`(옛 `check_notebook_readiness.py`가 멈추기 전에 씀 → 실행 전 사본으로, `b3d69e9c` 같음).
- 목록 밖으로 바꾼 것: 노트북 `06-MCP-실습.ipynb`(`4ad6dfbd` → `bad09ea5`, 마크다운·06-1 첨부만) · `_src/06`·`06-*.html`(`9e735b71`→`421120cf` · `505e9e50`→`f79ad77b`) · 생성기 `author_01~06.py`(`71b1f594`→`89091dba` · `1c89a565`→`dd600bb6` · `91b4a00b`→`1c1f2280` · `51958a06`→`f0a0c7c7` · `9f24c15a`→`b5c8b139` · `89312a3a`→`dddb8191` — 문자열만, 도구 파일 줄 그대로) · 그림 `03-3`·`03-4`·`06-1`·`06-3`(`.mmd`·`.svg`·`.png`·`.render.json`, 캡션 그대로) · 진단 여섯·`01`·`03`·`06-figures.md`·`handoff.md`·`chapter-summary.md`(새로)·`gates-after.json`(새로)·`gates-wip-0N.json`(`--no-exec`가 다시 씀) · `textbook/qa/upgrade-progress.md` Ch 28 행.
- **바뀌지 않은 것(확인)**: 도구 파일 `connect_tools.py` 05 판 `570ed3cc…` · 서버 파일 둘 `env_server.py` `8b4c40bc…`·`auth_server.py` `8f41e542…` · `pyproject.toml`·`uv.lock` · 실습 폴더 pyc 둘(22:08·09-10 그대로 — 마감은 만들지 않음) · `delivery-results.json` `3cc2d143…` · `textbook/qa/*.json` · 삽화.
