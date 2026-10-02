# 삭제 목록 (2026-10-01)

전체 마감 6단계가 만든 삭제 목록의 요약입니다. 지우는 일은 마감 담당이 `deletion-manifest-2026-10-01.tsv`(같은 폴더) 한 줄씩 합니다. 이 목록을 만들면서 지운 것은 없습니다. 기준 시각 2026-10-01(기기 셸 UTC), 사용자 결정 「삭제 승인 목록은 마감 끝에 지움(보존 대상과 다음 작업에 필요한 것은 뺌)」.

## 읽는 법

- TSV 칸: `구분`(`connected` = 연결 폴더 `$ROOT` = `~/mnt/한국경제신문`, `device` = 작업 기기) · `경로`(연결 폴더는 `$ROOT` 기준 상대 경로, 기기는 절대 경로) · `종류`(파일/폴더) · `크기(바이트)` · `까닭`(맨 앞 `[분류]`).
- 기기 경로의 `/sessions/rcw-01fa62dwjghtyrmrgyqrfwx5/tmp`는 이 세션의 `$TMPDIR`, `/sessions/rcw-01fa62dwjghtyrmrgyqrfwx5`는 세션 홈(`~`)입니다. 다른 세션에서 지우면 경로가 다를 수 있으니 `$TMPDIR`·`$HOME`으로 바꿔 읽으세요.
- 크기: 파일은 바이트. 연결 폴더의 작은 폴더(파이썬 캐시·개별 항목)는 안의 파일 크기 합, `.cache`·실습 `.venv`·기기 폴더는 `du -sb`(겉보기 크기, 한 폴더 안의 하드링크는 한 번만 셈). 서로 하드링크를 나눈 폴더가 있으면 실제로 비는 자리는 합보다 작을 수 있습니다.
- **통째로 지우면 안 되는 상위 폴더**: `.cache/vm`(안의 `pgenv`를 남김) · `.cache/final-close`와 각 단계 폴더(안의 `log/`·`tools/`를 남김) · 챕터 `figures/`·`qa/upgrade/`(옛 그림·`gates-wip*` 파일만 줄마다) · `labs/part7/ch34-cost-rate-limits/runs/`(파일 셋만 — 폴더는 비게 됨). TSV에 적힌 경로만 지우세요.
- 연결 폴더는 지우기가 막혀 있습니다(지울 때 권한 요청이 필요). 기기 쪽은 바로 지워집니다.

## 종류별 개수·크기

| 구분 | 분류 | 줄 | 크기(바이트) | 내용 |
|---|---|---|---|---|
| 연결 폴더 | 옛 그림 | 527파일 | 5,827,302 | 31챕터(Ch 22 뺌) 그림 폴더에서 지금 `_src`가 `{{mermaid:}}`·`{{img:}}`로 부르지 않는 파일 — `.svg` 196·`.excalidraw` 196·`.caption.md` 129·개선 전 삽화 `.png` 4(Ch 8 1·Ch 9 3)·`verification.md` 2(Ch 9·10 옛 도식 검증 기록) |
| 연결 폴더 | 게이트 작업 기록 | 362파일 | 408,527 | 챕터 `qa/upgrade/gates-wip*`·`gates-closecheck*`·`gates-pre*` JSON(`gates-before.json`·`gates-after.json`·`gates-after-2-7.json`은 넣지 않음) |
| 연결 폴더 | 파이썬 캐시 | 120폴더 | 8,699,380 | `__pycache__` 99·`.ruff_cache` 13·`.pytest_cache` 8 — 챕터·실습·Part·공용(`textbook/_notebook`·`textbook/qa`·`textbook/_template` 등) 폴더, `.venv` 밖, Ch 32·33과 보존 폴더 밖 |
| 연결 폴더 | 개별 항목 | 15(파일 6·폴더 9) | 1,688,598 | Ch 34 옛 `runs/` 셋 · 루트 `batch-input.jsonl` · Ch 27 `workspace`·`workspace-05`·`workspace-08` · `textbook/qa/_to_delete/`(폴더째, `_trim_tmp.py` 하나) · Ch 16 `depth-notes.json` · Ch 34 `probe/02-batch.md.tmp` · Ch 12 `runs/continuity/` 사본 셋(`20260918T231546`·`231622`·`231828`) · 빈 폴더 `textbook/_notebook/checks/--chapter`·`checks/ch34-cost-optimization` |
| 연결 폴더 | 실습 `.venv` | 18폴더 | 2,362,926,825 | 점검표 ※ 18개(Ch 12·13·16~21·23~31·34). Ch 31 `.venv`는 Part 7 묶음 실행 러너를 3단계에서 `uv run --project <풀린 묶음 챕터>`로 고쳐 더는 쓰지 않음(5단계 `--pre-exec` 통과) |
| 연결 폴더 | `.cache` | 199폴더 | 29,151,565,181 | 챕터 작업 폴더 145(`chNN-*-view`·`chNN-close` 등 401,544,477) · `.cache/vm/` 아래 35(가상환경 27·`bundle-check`·`hf`·`mamba`·`pg`·`pgdata`·`pgembed-try`·`pgtool`·`shot`, 28,568,693,826) · `.cache/final-close/` 단계 사본·작업 폴더 19(181,326,878) |
| **연결 폴더 합** | | **1,241** | **31,531,115,813**(29.37 GiB) | |
| 기기 | `/tmp` | 28(파일 1·폴더 27) | 2,404,154,334 | 작업 폴더(`ch31-02`~`06`·`ch31-close`·`ch31-pg`·`ch34-01`~`06`·`ch34-close`·`ch34-prep`·`reviewA31`·`reviewB31`·`reviewA34`·`reviewB34`·`cumdocs31`·`cumdocs34`·`finalcheck`·`fc1-builds.txt`) · 도구(`uv-cache` 816,133,410·`pptr-cache` 691,777,369·`mmd` 400,520,724·`npm-cache` 250,374,747·`npm-cache-ch31close` 39,417,498) |
| 기기 | `$TMPDIR` | 75폴더 | 106,701,800 | 노트북 실행 임시 폴더(`ch23-04-*`·`ch24-0N-*`·`ch27-04-*`·`ch27-04x-*`·`ch31-03-*`·`ch31-05-*`·`ch31-close-b3`·`ch34-02-*`·`ch34-06-design-*`·`reviewA27-*`) · `fc3-ch33`·`fc3-ch34`(3단계) · `fc5-part6`(5단계) |
| 기기 | 세션 홈 | 1폴더 | 70,971,692 | `~/ch16work` |
| **기기 합** | | **104** | **2,581,827,826**(2.40 GiB) | |
| **전체** | | **1,345** | **34,112,943,639**(31.77 GiB) | |

챕터별 옛 그림 수: Ch 1 10 · Ch 2 24 · Ch 3 10 · Ch 4 10 · Ch 5 16 · Ch 6 12 · Ch 7 16 · Ch 8 14 · Ch 9 17 · Ch 10 25 · Ch 11 12 · Ch 12 39 · Ch 13 21 · Ch 14 27 · Ch 15 24 · Ch 16 18 · Ch 17 15 · Ch 18 18 · Ch 19 18 · Ch 20 12 · Ch 21 18 · Ch 22 0(24 뺌) · Ch 23 18 · Ch 24 9 · Ch 25 9 · Ch 26 12 · Ch 27 24 · Ch 28 15 · Ch 29 12 · Ch 30 27 · Ch 31 15 · Ch 34 10. 옛 그림에 딸린 `*.render.json`은 0개였습니다(있었으면 보존).

## 부르는 곳 확인

- **옛 그림**: 파일 이름(그림은 확장자를 뗀 이름도)을 `_src` 252개·빌드 HTML 288개·`*.caption.md` 1,353개·공개 목록(`public-files.json`·`prerequisite-files.json`) 49개·zip 10개의 항목 이름에서 찾고, 찾은 곳이 **같은 챕터**이거나 그 챕터 그림 경로를 적었을 때만 「부르는 곳」으로 셈 → 527개 모두 0. (Ch 33 `_src`가 제 폴더의 `01-흐름.svg` 등을 부르는 것은 이름만 같은 다른 파일이라 걸리지 않음.) 대기 삽화 Ch 4 02-5 `prompt.md`·`caption.md`는 넣지 않았습니다.
- **폴더·개별 항목·캐시·`.venv`**: 공개 목록 49개와 zip 10개에 그 경로나 그 아래 경로가 없음. Ch 12 사본 셋·Ch 27 `workspace*`·Ch 16 `depth-notes.json`·`02-batch.md.tmp`를 부르는 스크립트(`.py`·`.sh`·`.cjs`) 0.
- **기록에만 남는 경로**(읽는 스크립트 0 — 지운 뒤 기록과 디스크가 달라질 뿐 검사는 멈추지 않음): `textbook/qa/continuity-evidence/figures-preserved.json`(옛 그림 174) · `textbook/part6/qa/final-artifact-hashes.json`(133) · `textbook/part7/qa/final-artifact-hashes.json`(Ch 34 옛 `runs/` 셋 등) · `textbook/part7/ch34-cost-rate-limits/qa/delivery-inventory.json`(옛 `runs/` 셋·루트 `batch-input.jsonl`) · Part 4 `qa/language/snapshots/*.manifest.json`·Part 5 `qa/language/*.json`(2026-09-10 감사 기록). Part 5 `final-manifest.json`(42)은 `finalize_evidence.py`가 **쓰는** 결과이고 이 스크립트는 언어 감사 기준에서 이미 멈춤(사람 결정 ⑤). 과정 결정 14번(옛 기록 해시)과 함께 정할 일입니다.
- 노트북 저장 출력 안의 경로 글(예: Ch 12 `.venv` 경고 글이 `notebook-before-invariants.json`에 들어 있음)은 부르는 곳이 아님.

## 넣지 않은 것과 까닭

**보존 대상**(최종 점검표 §4)
- 챕터 `qa/upgrade/before/`·`before-2-7/` 등 사본 폴더(옮긴 생성기 포함 — 그 안의 `__pycache__` 1개·`gates-wip-*` 5개도 손대지 않음) · `qa/upgrade/probe/`(안의 `__pycache__` 2개 포함, `02-batch.md.tmp` 하나만 넣음) · `review-pack/`(6단계에서 다시 만든 판).
- Ch 12 `runs/continuity/20260918T232052`·`20260921T082024`(검사가 요구하는 정본 사본), 그 밖의 `20260910T*` 넷 · Ch 9·10 옛 사본 · `*.render.json` · 계약 노트북·자료 파일(Ch 18 06·Ch 21 06 `data/rag-comparison.json` 등) · Ch 23·31 `qa/upgrade/pre_exec.sh`.
- `.cache/vm/pgenv`(168,043,511 B) — Ch 23·31 `pre_exec.sh`가 `.cache/vm/pgenv/bin`만 씀(밖을 가리키는 링크 0이라 `mamba`를 지워도 됨).
- `.cache/final-close/*/log/`·`*/tools/`(11폴더 약 5.2 MB) — `final-close-log.md`가 근거로 가리키는 전후 해시 표, 다시 쓸 사본(Part 1 복습 문항 줄만 건너뛴 `check_delivery` 사본, 묶음 검사 감싸개 등). 같은 단계의 `before/`·작업 폴더는 넣음(전후 해시는 `log/`와 마감 기록에 있음).
- `textbook/downloads/` zip 10개 · 루트 `.env` · `.moai` 전체 · 제외 챕터 Ch 32·33 파일(캐시·`.venv` 포함) · 이번 단계가 만든 문서(이 파일·TSV·누적 문서 넷·`final-close-log.md`). `.git`은 없음.
- 사용자 것으로 보이는 실습 폴더 `.venv` 16개(Ch 1~11·14·15·22·32·33 — 점검표 ※ 18개 밖). Ch 7 요약 §12 등 몇 챕터 요약이 정리 대상으로 적었으나 지시대로 넣지 않음(사람 확인).

**다음 작업에 필요해 보류**(Ch 12 화면 라벨 결정 뒤 지울 것)
- 기기 `$TMPDIR/fc5-part3`(50,107,058 B) — `finalize_continuity_evidence.py`가 읽는 `temporary_extraction`(다시 만들려면 Part 3 연속성 묶음을 다시 돌려 모델 요청).
- 기기 `/tmp/pw`(18,722,087)·`/tmp/pw-browsers`(280,926,484)·`/tmp/libs`(52,607) — `visual.cjs` 실행(`NODE_PATH=/tmp/pw/node_modules PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`). Mermaid 도구(`/tmp/mmd`·`pptr-cache`)는 그림을 고치기로 할 때만 필요하고 다시 설치할 수 있어 목록에 넣음.

**부르는 곳이 있어 뺌**
- Ch 22 옛 그림 24개(86,309 B) — 옛 SVG 8개가 챕터 `textbook/part6/ch22-middleware/qa/public-files.json` 12~19행에 있음(Part 6 `collect_public_files.py`가 읽는 목록). 짝 `.excalidraw` 8·`.caption.md` 8도 함께 남김 — `.svg`만 남고 `.excalidraw`가 없으면 Part 6 `check_figures.py`가 「Missing editable source」로 멈춤. 지우려면 Ch 23·24·28 선례처럼 목록 줄을 먼저 빼고 Part 목록·zip이 바이트 같은지 확인(사람 결정 ⑧).
- Ch 13 `labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json`(1,078 B) — Part 4 `public-files.json`·챕터 `qa/public-files.json`에 명시 항목, `part4-practice.zip`·`llm-practice.zip`에 들어 있음. 점검표 §2-2 1번 절차(목록 두 줄 → Part 4 목차·zip·`llm-practice.zip` → 전달 검사) 뒤에 지울 것(사람 결정 ⑨).

**이번 작업물이 아니거나 지시 범위 밖**
- 기기 시스템·도구가 관리하는 것: `/tmp/hsperfdata_root`·`/tmp/systemd-private-*` · `$TMPDIR/data-gym-cache`(5,299,144, tiktoken)·`node-compile-cache`(1,409,448)·`generator-cli-*` · `$TMPDIR`의 `srt-mux-*.sock`·`uv-*.lock`(쓰는 중일 수 있음).
- 세션 홈의 다른 파일(2026-09-20~21의 `before-contracts.md`·`before-course-summary.md`·`before2-course-summary.md`·`ch13_patch.py`·`ch13_trim*.py`·`ch14_patch.py`·`ch14_trim*.py`·`contracts_edit.py`·`cs_edit.py`·`docs_edit.py`·`prog_edit.py`, 합 130,214 B · `~/scratch27` 7,485 B) — 지시 목록에 없음, 사람 확인.
- 연결 폴더 루트 `.pytest_cache`·`.ruff_cache` — 챕터·실습·Part·공용 폴더 밖, 사람 확인.

## 지운 뒤 알아 둘 것

- Ch 12 `pre_exec.sh`는 `.cache/vm/pgdata`를 `initdb` 없이 켭니다(보존 목록에 없음). `pgdata`를 지운 뒤 Ch 12 01~03을 다시 실행하려면 클러스터를 새로 만들어야 합니다. Ch 23·31 훅은 데이터 폴더가 없으면 스스로 `initdb`(Ch 31 `/tmp/ch31-pg`도 마찬가지).
- `.cache/vm/venv-*`·`hf`·`bundle-check`를 지우면 다음 재실행·묶음 검사가 가상환경과 캐시를 새로 받습니다(네트워크·시간). `check_course_continuity.py`는 Python 3.11 이상이 필요한데 지금 쓰던 `.cache/vm/venv-ch06-langchain-start`도 지워지므로 uv가 둔 `~/.local/share/uv/python/cpython-3.12-linux-aarch64-gnu/bin/python3.12`(표준 라이브러리만으로 `render`·`verify`·`tomllib` 가져오기 확인)를 씁니다.
- 기기 루트(`/`=`/tmp`)는 지금 여유 약 0.7 GB(93%)입니다. `/tmp` 줄을 지우면 약 2.4 GB가 비고, `$TMPDIR`·세션 홈(`/sessions`)은 약 0.18 GB, 연결 폴더는 약 29.4 GiB가 빕니다.

## 지운 뒤 다시 돌릴 검사

```bash
ROOT=$HOME/mnt/한국경제신문; cd $ROOT; export PYTHONDONTWRITEBYTECODE=1
# 1) 그림 검사 넷 — 옛 짝이 빠져 쌍 수가 줄어야 정상(지금 163·119·260·119 → 지운 뒤 133·98·221·100, Part 6에는 Ch 22 옛 짝 8 포함)
for p in 4 5 6 7; do python3 textbook/part$p/qa/check_figures.py || echo "FAIL part$p"; done
# 2) HTML ↔ 노트북 대조(계약 JSON을 다시 씀 — 바이트가 같아야 함), 챕터마다
for c in textbook/part*/ch*/; do case $c in *ch32-*|*ch33-*) continue;; esac; python3 textbook/_notebook/verify.py --chapter ${c%/} || echo "FAIL $c"; done
# 3) 연속성 둘
python3 textbook/part3/qa/check_continuity.py
$HOME/.local/share/uv/python/cpython-3.12-linux-aarch64-gnu/bin/python3.12 textbook/qa/check_course_continuity.py
# 4) 전달 검사(공개 목록 경로가 모두 남았는지) — Part 1은 Ch 2 복습 문항(사람 결정 ③)에서 멈추는 것이 지금 상태
for p in 2 3 4 5 6 7; do python3 textbook/part$p/qa/check_delivery.py || echo "FAIL part$p"; done
python3 textbook/qa/check_course_delivery.py; python3 textbook/part7/qa/check_secrets.py
python3 textbook/part1/qa/check_delivery.py --revised-existing
```
- 게이트도 한 번: 전체 점검 방식대로 `textbook/_notebook/checks/upgrade_gates.py`의 `check_section()`만 불러 236절 G1~G7 합 0(`main()`은 `gates-*.json`을 쓰므로 부르지 않음).
- `check_figures.py` 넷과 전달·연속성 검사는 결과 파일(`figure-consistency.json`·`delivery-results.json`·`*-static-results.json` 등)을 다시 씁니다 — 그림 검사 결과 파일은 쌍 수가 줄어 바뀌는 것이 정상, 나머지는 바이트가 같아야 합니다.
