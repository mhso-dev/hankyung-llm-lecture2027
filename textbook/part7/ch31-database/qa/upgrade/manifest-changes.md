# 보호 파일 변경 기록 (`before-manifest.json` 209개 대조)

## 01절 뒤 (2026-09-29)

- 대조: 209개 가운데 **같음 201 · 바뀜 8 · 없어짐 0**. 바뀐 것은 모두 01절 작업의 의도한 변경입니다.

| 파일 | 전 sha256 | 후 sha256 | 까닭 |
|---|---|---|---|
| `textbook/part7/ch31-database/01-SQLAlchemy-비동기-PostgreSQL.html` | `b39c35d034a9…` | `ba896f000f30…` | `_build.py`가 개선본 `_src`·노트북으로 다시 만든 절 HTML |
| `textbook/part7/ch31-database/집필점검표.md` | `aaba39f3529f…` | `1a3c4353ccff…` | 끝에 「품질 개선」 절과 01 행을 더함 |
| `textbook/part7/ch31-database/_src/01-SQLAlchemy-비동기-PostgreSQL.html` | `9de4f15a940f…` | `54b6e6369297…` | 개선본 본문(`author_01.py`) |
| `textbook/part7/ch31-database/figures/_gen_figures.py` | `dc2d8216a715…` | `34448715a376…` | 옛 그림 생성기 맨 위 막기(설명 주석 셋 + `raise SystemExit`) |
| `textbook/part7/ch31-database/qa/author_ch31.py` | `1755fcec2eb2…` | `79bf670cf5f3…` | 옛 생성기 맨 위 막기(설명 주석 셋 + `raise SystemExit`) |
| `textbook/part7/ch31-database/qa/verification.md` | `788e3ab561a6…` | `522b7bf1a1f8…` | 끝에 「품질 개선 01절」 절을 더함 |
| `labs/part7/ch31-database/notebooks/01-SQLAlchemy-비동기-PostgreSQL.ipynb` | `b6f89db6337c…` | `0b743f06d456…` | 개선본 노트북(새 커널 A 출력, `code_sha256` `addb4391…`) |
| `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` | `d04297070a95…` | `ec9e7cd623d9…` | `verify.py --chapter`가 다시 쓴 챕터 계약 파일(01 줄) |

- 새로 만든 파일(목록 밖): `qa/upgrade/pre_exec.sh`·`author_01.py`·`01-figures.md`·`01-diagnosis.md`·`handoff.md`·`gates-wip-01-01.json`·`gates-wip-01.json`·`review-pack/01-…md`·`figures/01-1`~`01-5`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`·`.prompt.md`). 옛 그림 `figures/01-흐름.*`은 그대로.

## 02절 뒤 (2026-09-29)

- 대조: 209개 가운데 **같음 198 · 바뀜 11 · 없어짐 0**. 01이 바꾼 8개 가운데 5개는 01 기록 값 그대로(01 절 HTML·`_src`·노트북 01·옛 생성기 둘). 02 작업으로 바뀐 것은 아래 여섯이고 모두 의도한 변경입니다.

| 파일 | 01 뒤(없으면 원래) sha256 | 02 뒤 sha256 | 까닭 |
|---|---|---|---|
| `textbook/part7/ch31-database/02-트랜잭션과-원자성.html` | `d68fc2e08a17…`(원래) | `bfde8e44f7a4…` | `_build.py`가 개선본 `_src`·노트북으로 다시 만든 절 HTML |
| `textbook/part7/ch31-database/_src/02-트랜잭션과-원자성.html` | `7db86936165d…`(원래) | `97d95f85f8fc…` | 개선본 본문(`author_02.py`) |
| `labs/part7/ch31-database/notebooks/02-트랜잭션과-원자성.ipynb` | `d08a39ca7386…`(원래) | `b427398a8a07…` | 개선본 노트북(새 커널 A 출력 + 02-1 PNG 첨부, `code_sha256` `39d29f86…`) |
| `textbook/part7/ch31-database/집필점검표.md` | `1a3c4353ccff…` | `ac6eaf65ef3d…` | 「품질 개선」 표 끝에 02 행을 더함 |
| `textbook/part7/ch31-database/qa/verification.md` | `522b7bf1a1f8…` | `6842bf822694…` | 끝에 「품질 개선 02절」 절을 더함 |
| `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` | `ec9e7cd623d9…` | `b07392b30fea…` | `verify.py --chapter`가 다시 쓴 챕터 계약 파일(02 줄) |

- 새로 만든 파일(목록 밖): `qa/upgrade/author_02.py`·`02-figures.md`·`02-diagnosis.md`·`gates-wip-02-02.json`·`gates-wip-02.json`·`review-pack/02-…md`·`figures/02-1`~`02-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`figures/02-5-…`(`.png`·`.prompt.md`·`.caption.md`). `handoff.md`·`manifest-changes.md`(목록 밖)에 02 절을 더함. 옛 그림 `figures/02-흐름.*`은 그대로. 실습 폴더 `app/`·`migrations/`·`alembic.ini`·`README.md`·`pyproject.toml`·`uv.lock`은 같음(목록 안 — 대조 같음).

## 03절 뒤 (2026-09-29)

- 대조: 209개 가운데 **같음 195 · 바뀜 14 · 없어짐 0**. 01·02가 바꾼 것 가운데 01·02 절 HTML·`_src`·노트북 01·02·옛 생성기 둘은 01·02 기록 값 그대로. 03 작업으로 바뀐 것은 아래 여섯이고 모두 의도한 변경입니다.

| 파일 | 02 뒤(없으면 원래) sha256 | 03 뒤 sha256 | 까닭 |
|---|---|---|---|
| `textbook/part7/ch31-database/03-Alembic-적용과-롤백.html` | `8939000517cf…`(원래) | `7d303aea3af2…` | `_build.py`가 개선본 `_src`·노트북으로 다시 만든 절 HTML |
| `textbook/part7/ch31-database/_src/03-Alembic-적용과-롤백.html` | `85f969e51570…`(원래) | `9610c772a90c…` | 개선본 본문(`author_03.py`) |
| `labs/part7/ch31-database/notebooks/03-Alembic-적용과-롤백.ipynb` | `d52e8aa566d3…`(원래) | `28595499c4fb…` | 개선본 노트북(새 커널 A 출력 + 03-1 PNG 첨부 + `mdpatch.py` 설명 셋, `code_sha256` `f97cba07…`) |
| `textbook/part7/ch31-database/집필점검표.md` | `ac6eaf65ef3d…` | `2d2ce2805912…` | 「품질 개선」 표 끝에 03 행을 더함 |
| `textbook/part7/ch31-database/qa/verification.md` | `6842bf822694…` | `a9ebb50ba687…` | 끝에 「품질 개선 03절」 절을 더함 |
| `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` | `b07392b30fea…` | `730a5e361553…` | `verify.py --chapter`가 다시 쓴 챕터 계약 파일(03 줄) |

- 새로 만든 파일(목록 밖): `qa/upgrade/author_03.py`·`03-figures.md`·`03-diagnosis.md`·`gates-wip-03-03.json`·`gates-wip-03.json`·`review-pack/03-…md`·`figures/03-1`~`03-5`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`figures/03-6-…`(`.png`·`.prompt.md`·`.caption.md`). `handoff.md`·`manifest-changes.md`(목록 밖)에 03 절을 더함. 옛 그림 `figures/03-흐름.*`은 그대로. **실습 폴더 `app/`·`migrations/`·`alembic.ini`·`README.md`·`pyproject.toml`·`uv.lock`·맥 pyc 17개는 sha256 전후 같음**(목록 안 — 대조 같음, 작업 전 `/tmp/ch31-03/lab-before.sha`와도 같음).

## 04절 뒤 (2026-09-29)

- 대조: 209개 가운데 **같음 192 · 바뀜 17 · 없어짐 0**. 01·02·03이 바꾼 것 가운데 01~03 절 HTML·`_src`·노트북 01~03·옛 생성기 둘은 01~03 기록 값 그대로. 04 작업으로 바뀐 것은 아래 여섯이고 모두 의도한 변경입니다(재개 작업 — 앞 04 작업자는 보호 파일을 고치지 않고 멈춤).

| 파일 | 03 뒤(없으면 원래) sha256 | 04 뒤 sha256 | 까닭 |
|---|---|---|---|
| `textbook/part7/ch31-database/04-커넥션-풀-고갈과-대응.html` | `d499941d2fa6…`(원래) | `69d1f347e5bc…` | `_build.py`가 개선본 `_src`·노트북으로 다시 만든 절 HTML |
| `textbook/part7/ch31-database/_src/04-커넥션-풀-고갈과-대응.html` | `d58cc3e73894…`(원래) | `b1533f7db6f9…` | 개선본 본문(`author_04.py`) |
| `labs/part7/ch31-database/notebooks/04-커넥션-풀-고갈과-대응.ipynb` | `74256be64a65…`(원래) | `3d9bf01c3a76…` | 개선본 노트북(새 커널 A 출력 + 04-1 PNG 첨부, `code_sha256` `d919bdcd…`) |
| `textbook/part7/ch31-database/집필점검표.md` | `2d2ce2805912…` | `aab506f6903f…` | 「품질 개선」 표 끝에 04 행을 더함 |
| `textbook/part7/ch31-database/qa/verification.md` | `a9ebb50ba687…` | `e6b3726baedf…` | 끝에 「품질 개선 04절」 절을 더함 |
| `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` | `730a5e361553…` | `f907abbc5762…` | `verify.py --chapter`가 다시 쓴 챕터 계약 파일(04 줄) |

- 새로 만든 파일(목록 밖): `qa/upgrade/author_04.py`·`04-figures.md`·`04-diagnosis.md`·`gates-wip-04-04.json`·`gates-wip-04.json`·`review-pack/04-…md`·`figures/04-1`~`04-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`figures/04-5-…`(`.png`·`.prompt.md`·`.caption.md`). `handoff.md`·`manifest-changes.md`(목록 밖)에 04 절을 더함. 옛 그림 `figures/04-흐름.*`은 그대로. **실습 폴더 `app/`·`migrations/`·`alembic.ini`·`README.md`·`pyproject.toml`·`uv.lock`·맥 pyc 17개는 sha256 전후 같음**(목록 안 — 대조 같음, 03의 `/tmp/ch31-03/lab-before.sha`와도 17/17 같음). 훅 `pre_exec.sh`는 `8a9529f1…` 그대로.

## 05절 뒤 (2026-09-29)

- 대조: 209개 가운데 **같음 189 · 바뀜 20 · 없어짐 0**. 01~04가 바꾼 것 가운데 01~04 절 HTML·`_src`·노트북 01~04·옛 생성기 둘은 01~04 기록 값 그대로. 05 작업으로 바뀐 것은 아래 여섯이고 모두 의도한 변경입니다.

| 파일 | 04 뒤(없으면 원래) sha256 | 05 뒤 sha256 | 까닭 |
|---|---|---|---|
| `textbook/part7/ch31-database/05-pgvector-체크포인터-공존과-백업.html` | `7c20a8061521…`(원래) | `057b0e2fed7f…` | `_build.py`가 개선본 `_src`·노트북으로 다시 만든 절 HTML |
| `textbook/part7/ch31-database/_src/05-pgvector-체크포인터-공존과-백업.html` | `efae0d4ce8e4…`(원래) | `8e2423a7c2d8…` | 개선본 본문(`author_05.py`) |
| `labs/part7/ch31-database/notebooks/05-pgvector-체크포인터-공존과-백업.ipynb` | `5549cfa7f9f2…`(원래) | `bc3a68a1348f…` | 개선본 노트북(새 커널 A 출력 + 05-1 PNG 첨부 + `mdpatch.py` 설명 넷, `code_sha256` `62695363…`) |
| `textbook/part7/ch31-database/집필점검표.md` | `aab506f6903f…` | `e542a3b6af18…` | 「품질 개선」 표 끝에 05 행을 더함 |
| `textbook/part7/ch31-database/qa/verification.md` | `e6b3726baedf…` | `8cd5a312e6c8…` | 끝에 「품질 개선 05절」 절을 더함 |
| `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` | `f907abbc5762…` | `f73ca7c2d861…` | `verify.py --chapter`가 다시 쓴 챕터 계약 파일(05 줄) |

- **목록 밖 파일 고침 — 훅 `qa/upgrade/pre_exec.sh`**(01이 만든 다섯 절 공통 파일): `8a9529f101ef38bdbf57ae31118c70fd53736df65ca884038fe1096aae009b9e` → **`dd564645cc2a7a625ede2d7040c31dfa387ae7155fee82c5ef1355c4a6d846d6`** — `CH31_PGURL` 정의 뒤에 설명 주석 셋과 pgenv `bin`을 PATH **끝**에 더하는 한 줄(`case … esac`, 두 번 불러도 한 번만). 챕터 리드 결정(「PATH 앞에 더하는 한 줄을 넣어도 됨」)을 따르되 끝에 둔 까닭은 `05-diagnosis.md` 「백업 명령 자리」. 01~04 노트북에 `PATH` 출력 0 · 01~04는 다시 실행하지 않음.
- 새로 만든 파일(목록 밖): `qa/upgrade/author_05.py`·`05-figures.md`·`05-diagnosis.md`·`gates-wip-05-05.json`·`gates-wip-05.json`·`review-pack/05-…md`·`figures/05-1`~`05-4`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`figures/05-5-…`(`.png`·`.prompt.md`·`.caption.md`) · 연결 폴더 `.cache/ch31-05/`(확인 스크립트 셋·`edit.py` 사본)·`.cache/ch31-05-view/`(확인용 PNG 아홉). `handoff.md`·`manifest-changes.md`(목록 밖)에 05 절을 더함(handoff: 머리 줄·용어 표 여섯 줄·「§05 → 실습 절」). 옛 그림 `figures/05-흐름.*`은 그대로. **실습 폴더 `app/`·`migrations/`·`alembic.ini`·`README.md`·`pyproject.toml`·`uv.lock`·맥 pyc 17개는 sha256 전후 같음**(목록 안 — 대조 같음, 03의 `/tmp/ch31-03/lab-before.sha`와도 17/17 같음).

## 06절 뒤 (2026-09-29)

- 대조: 209개 가운데 **같음 181 · 바뀜 28 · 없어짐 0**. 01~05가 바꾼 20개 가운데 14개(01~04 절 HTML·`_src`·노트북 01~04·옛 생성기 둘 등)는 05 뒤 기록 값 그대로. 06 작업으로 바뀐 것은 아래 열넷(05 뒤 값에서 다시 바뀐 여섯 + 처음 바뀐 여덟)이고 모두 의도한 변경입니다.

| 파일 | 05 뒤(없으면 원래) sha256 | 06 뒤 sha256 | 까닭 |
|---|---|---|---|
| `textbook/part7/ch31-database/chapter.json` | `2f4ce4ae0446…`(원래) | `755495028d64…` | `sections`에 06절 한 줄(`experiment`) — `hours`·`objectives` 그대로, 들여쓰기 2(원래 모양) |
| `textbook/part7/ch31-database/index.html` | `815dcc962b74…`(원래) | `d9cc74a27558…` | `_build.py`가 06절 줄을 더함(「절 6개」) |
| `textbook/part7/ch31-database/05-pgvector-체크포인터-공존과-백업.html` | `057b0e2fed7f…` | `da333b5306f9…` | 꼬리말 다음 절 링크(06) + b8 06 링크·문장(05 `--no-exec`) |
| `textbook/part7/ch31-database/_src/05-pgvector-체크포인터-공존과-백업.html` | `8e2423a7c2d8…` | `604080c9ffc0…` | b8 06 링크·문장(`mdpatch.py` → `author_05.py --src-only` 바이트 같음) |
| `labs/part7/ch31-database/notebooks/05-pgvector-체크포인터-공존과-백업.ipynb` | `bc3a68a1348f…` | `09471344dfd9…` | 정리 셀 끝 06 문장(`mdpatch.py`) — **`code_sha256` `62695363…`·`outputs_sha256` `8bac96cd…`·`executed_at` 19:32:40Z 그대로** |
| `textbook/part7/ch31-database/집필점검표.md` | `e542a3b6af18…` | `a5df89a2a189…` | 「품질 개선」 표 끝에 06 행 |
| `textbook/part7/ch31-database/qa/verification.md` | `8cd5a312e6c8…` | `b2781c082ed4…` | 끝에 「품질 개선 06절」 절 |
| `textbook/part7/ch31-database/qa/public-files.json` | `dd039b3ace59…`(원래) | `51fc1808efd3…` | 06 HTML·06 노트북 두 줄(이 챕터 목록 모양 — 절 HTML도 적음) |
| `labs/part7/ch31-database/README.md` | `a54f0fd5f937…`(원래) | `bd99e26b2d00…` | 맨 아래 06절 한 단락만(다시 쓰기는 마감) |
| `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` | `f73ca7c2d861…` | `089e8b84e2ae…` | `verify.py --chapter`가 다시 쓴 챕터 계약 파일(06 줄) |
| `textbook/part7/public-files.json` | `12565fee9013…`(원래) | `d822ee88744f…` | `collect_public_files.py` — 06 노트북 한 줄(112줄) |
| `textbook/part7/index.html` | `f5e86b4ae753…`(원래) | `bfea1c9a89e1…` | `_build_index.py` — Ch 31 「6절」·Part 「31절」 |
| `textbook/downloads/part7-practice.zip` | `007f13875f11…`(원래) | `b5dac376866d…` | `_build_index.py` 두 번(첫 `f3637bd8…`) — 06 노트북·README 새 판, **중간 판(최종은 마감)** |
| `textbook/part7/qa/integration-results.json` | `70f89984c053…`(원래) | `e231a76cc68a…` | `_build_index.py`(`sections` 31·`code_cells` 448·`bundle_sha256` 새 zip) |

- 새로 만든 파일(목록 밖): `_src/06-DB와-상태-영속화-실습.html`·`06-DB와-상태-영속화-실습.html` · `labs/part7/ch31-database/notebooks/06-DB와-상태-영속화-실습.ipynb` · `figures/06-1`~`06-3`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`)·`figures/06-4-…`(`.png`·`.prompt.md`·`.caption.md`) · `qa/upgrade/author_06.py`·`06-design.md`·`06-figures.md`·`06-diagnosis.md`·`gates-wip-06-06.json`·`gates-wip-06.json`·`gates-wip-ch31-after06.json`·`review-pack/06-…md`(05 묶음도 다시) · 연결 폴더 `.cache/ch31-06/`·`.cache/ch31-06-view/`. 목록 밖 고침: `qa/upgrade/author_05.py`(`42cd35c9…` → `5e83dfb1…`, b8·정리 문장 둘)·`gates-wip-05.json`(05 `--no-exec`)·`handoff.md`·이 파일. 훅 `pre_exec.sh` `dd564645…` 그대로. **실습 폴더 `app/`·`migrations/`·`alembic.ini`·`pyproject.toml`·`uv.lock`·맥 pyc 16개 sha256 전후 같음**(`/tmp/ch31-03/lab-before.sha` 17개 가운데 README만 다름).

## 마감 뒤 (2026-09-29)

- 대조(`.cache/ch31-close/tools/manifest_check31.py`): 209개 가운데 **같음 169 · 바뀜 38 · 옮김 2**(06절 뒤 181 · 28 · 0). 바뀜 가운데 **36개가 마감에서 바뀜**(아래 표 — 06절 뒤 값에서 다시 바뀐 것 포함), 둘(챕터 `qa/public-files.json` `51fc1808…`·`textbook/part7/public-files.json` `d822ee88…`)은 06절 뒤 값 그대로(마감에서 다시 모아 바이트 같음). 모두 의도한 변경.
- **옮김(없어짐) 둘** — 옛 생성기 `mv -n`(해시 같음): `textbook/part7/ch31-database/qa/author_ch31.py`(`79bf670c…`) · `textbook/part7/ch31-database/figures/_gen_figures.py`(`34448715…`) → `qa/upgrade/before/generators/blocked/`.

| 파일 | 마감 전(06절 뒤) sha256 | 마감 뒤 sha256 | 까닭 |
|---|---|---|---|
| `textbook/part7/ch31-database/01-SQLAlchemy-비동기-PostgreSQL.html` | `ba896f000f30…` | `4abedad7365f…` | 01 재실행 뒤 빌드(A-1·A-2·A-3·A-4·A-5·A-15·A-16) |
| `textbook/part7/ch31-database/02-트랜잭션과-원자성.html` | `bfde8e44f7a4…` | `fbf1f379be03…` | 02 `--no-exec` 빌드(A-6·A-7·A-15) |
| `textbook/part7/ch31-database/03-Alembic-적용과-롤백.html` | `7d303aea3af2…` | `c27e230b824f…` | 03 `--no-exec` 빌드(A-5·A-8~A-13, 03-2·03-3 다시 렌더) |
| `textbook/part7/ch31-database/04-커넥션-풀-고갈과-대응.html` | `69d1f347e5bc…` | `d68870c0574d…` | 04 `--no-exec` 빌드(B-1·B-2) |
| `textbook/part7/ch31-database/05-pgvector-체크포인터-공존과-백업.html` | `da333b5306f9…` | `a7620466937d…` | 05 `--no-exec` 빌드(B-3·B-4·「보장」→「장담」) |
| `textbook/part7/ch31-database/chapter.json` | `755495028d64…` | `6837a4e9a145…` | `objectives` 셋 → 여섯(`hours`·`sections` 그대로) |
| `textbook/part7/ch31-database/index.html` | `d9cc74a27558…` | `62a18699ef35…` | `_build.py` — 새 `objectives` |
| `textbook/part7/ch31-database/집필점검표.md` | `a5df89a2a189…` | `c5dfe15d9c5b…` | 머리 「개선 전 판」 표시 + 끝 「마감」 절 |
| `textbook/part7/ch31-database/_src/01-SQLAlchemy-비동기-PostgreSQL.html` | `54b6e6369297…` | `be197fe15c28…` | 생성기 `src_html()`로 다시 씀(검토 반영 글 — 요약 §21) |
| `textbook/part7/ch31-database/_src/02-트랜잭션과-원자성.html` | `97d95f85f8fc…` | `bf2f059bd0be…` | 생성기 `src_html()`로 다시 씀(검토 반영 글 — 요약 §21) |
| `textbook/part7/ch31-database/_src/03-Alembic-적용과-롤백.html` | `9610c772a90c…` | `983add36cb6f…` | 생성기 `src_html()`로 다시 씀(검토 반영 글 — 요약 §21) |
| `textbook/part7/ch31-database/_src/04-커넥션-풀-고갈과-대응.html` | `b1533f7db6f9…` | `bc10ffaafec3…` | 생성기 `src_html()`로 다시 씀(검토 반영 글 — 요약 §21) |
| `textbook/part7/ch31-database/_src/05-pgvector-체크포인터-공존과-백업.html` | `604080c9ffc0…` | `c09f2f4d3b73…` | 생성기 `src_html()`로 다시 씀(검토 반영 글 — 요약 §21) |
| `textbook/part7/ch31-database/qa/research.md` | `f65ecfda9897…` | `fdfe45cd3cac…` | 머리 「개선 전 판」 표시(내용 그대로) |
| `textbook/part7/ch31-database/qa/verification.md` | `b2781c082ed4…` | `f2b49ca1340f…` | 머리 「개선 전 판」 표시 + 끝 「마감」 절 |
| `labs/part7/ch31-database/README.md` | `bd99e26b2d00…` | `e6eba05a3b7c…` | 전체 다시 씀(요약 §15) |
| `labs/part7/ch31-database/notebooks/01-SQLAlchemy-비동기-PostgreSQL.ipynb` | `0b743f06d456…` | `325b22d7c4b7…` | **01 다시 실행**(`code_sha256` `1566ad03…`·`outputs_sha256` `f8a551e4…`) |
| `labs/part7/ch31-database/notebooks/02-트랜잭션과-원자성.ipynb` | `b427398a8a07…` | `9e0114824cf4…` | 마크다운만(코드·출력 해시 같음) |
| `labs/part7/ch31-database/notebooks/03-Alembic-적용과-롤백.ipynb` | `28595499c4fb…` | `8870859a14df…` | 마크다운만(코드·출력 해시 같음) |
| `labs/part7/ch31-database/notebooks/04-커넥션-풀-고갈과-대응.ipynb` | `3d9bf01c3a76…` | `d2f2ce27cef8…` | 마크다운만(코드·출력 해시 같음) |
| `labs/part7/ch31-database/notebooks/05-pgvector-체크포인터-공존과-백업.ipynb` | `09471344dfd9…` | `073717772d54…` | 마크다운만(코드·출력 해시 같음 `62695363…`/`8bac96cd…`) |
| `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` | `089e8b84e2ae…` | `a386e8229f44…` | `verify.py --chapter`가 다시 씀(01 새 해시) |
| `textbook/_notebook/checks/ch31-database/01-SQLAlchemy-비동기-PostgreSQL-1280.png` | `86c336ee7b6e…` | `5820bf7d4aca…` | 화면 검사 스크린숏 새로(`visual.cjs`) |
| `textbook/_notebook/checks/ch31-database/01-SQLAlchemy-비동기-PostgreSQL-390.png` | `696ff144182f…` | `7932abebb66b…` | 화면 검사 스크린숏 새로(`visual.cjs`) |
| `textbook/_notebook/checks/ch31-database/index-1280.png` | `05dbe60b8bb3…` | `6c2dcc1ae5f5…` | 화면 검사 스크린숏 새로(`visual.cjs`) |
| `textbook/_notebook/checks/ch31-database/index-390.png` | `e8337045784c…` | `d70b1db99667…` | 화면 검사 스크린숏 새로(`visual.cjs`) |
| `textbook/_notebook/checks/ch31-database/visual-results.json` | `9d60cedfcac6…` | `964cfbb21917…` | `visual.cjs` 14행 PASS |
| `textbook/part7/_build_index.py` | `43525ed44d83…` | `750baec3dcb6…` | 20행 ch31 설명 |
| `textbook/part7/index.html` | `bfea1c9a89e1…` | `9c5663296c41…` | `_build_index.py` — Ch 31 설명 한 줄 |
| `labs/part7/continuity-guide.md` | `17b0723988db…` | `b9aa0766e770…` | 9행 Ch 31 줄 |
| `textbook/_notebook/build_index.py` | `db6ad12f8c77…` | `8457fd7d121c…` | 66~67행 Ch 31 설명(절 수 5 그대로) |
| `textbook/index.html` | `80aad0d4a39f…` | `2159e001114d…` | `build_index.py` — Ch 31 설명 하나 |
| `textbook/downloads/part7-practice.zip` | `b5dac376866d…` | `6711c32aaad9…` | `_build_index.py` 마지막 한 번 — 최종 판 |
| `textbook/part7/qa/integration-results.json` | `e231a76cc68a…` | `89f684f253c6…` | `bundle_sha256`만 |
| `textbook/part7/qa/visual-results.json` | `b73d3e840271…` | `85ca91f8fbf1…` | Ch 31 줄만 12 → 14 |
| `textbook/qa/upgrade-final-checklist.md` | `7f54471778bb…` | `34a83379880d…` | §2-19 Ch 31 항목·§3·§4 Ch 31 줄·§2-18 11번 아래 한 줄 |

- **목록 밖 파일 고침**: 훅 `qa/upgrade/pre_exec.sh` `dd564645…` → **`3a838c9204b9b8d8be487e2f0460bd3bd3f394fe891161efa2b88c54cb35a435`**(주석 두 줄 「다섯 절」 → 「여섯 절」, 주석 밖 줄 같음 — `diff`) · 생성기 여섯(`author_01` `3d310dcd`→`dbd4a456` · `02` `db71734c`→`da0decd2` · `03` `c7946dcf`→`c5335e39` · `04` `f5a282a8`→`380cd50c` · `05` `5e83dfb1`→`e3d80adf` · `06` `fa0bfd3c`→`1f40ad8c`) · `_src` 06·06 HTML · 노트북 06(마크다운만) · `figures/` 03-2·03-3·06-3(`.mmd`·`.svg`·`.png`·`.render.json`)·캡션 넷(01-1·03-3·05-2·06-3) · 설계표 `03-figures.md`·`06-figures.md` · `01-diagnosis.md`·`05-diagnosis.md`(사용자가 금지한 표현 바꿈) · `handoff.md` · `upgrade-progress.md` Ch 31 행.
- 새로 만든 파일: `qa/upgrade/chapter-summary.md` · `qa/upgrade/gates-after.json` · `qa/upgrade/before/generators/blocked/`(옮긴 둘).
