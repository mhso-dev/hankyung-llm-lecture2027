# 전체 마감 체크리스트 (upgrade-final-checklist)

**무엇이 들어 있나**: 전체 마감 순서 10단계(번호·명령·기대값), 뒤 챕터 인계 두 건과 「뒤 챕터에서 확인」 목록, 강사 확인 대기 항목 전부, 미결 모순, 삭제 승인 대상(보존할 것 포함).
**누가 읽나**: **전체 마감 담당만**. 절 작업의 판단 기준은 `upgrade-course-summary.md`, 산출 파일·데이터 계약은 `upgrade-contracts.md`.

2026-09-19에 `upgrade-course-summary.md`의 Part별 §10에서 옮겼습니다(내용 그대로). 근거는 각 챕터 `qa/upgrade/chapter-summary.md`와 `textbook/qa/upgrade-progress.md`.

## 1. 전체 마감 순서 (Ch12 §16이 최신 판 — Ch9 §9·Ch10 §9·Ch11 §15에 이어 붙인 것)

0. 끝났습니다: `part3-practice.zip` 재생성(**92항목**, `Part 3: 36 verified sections`), ch12 화면 검사 28행, `check_delivery.py` 통과(노트북 36).
1. `textbook/downloads/` 묶음 재생성 — **`part1-practice.zip`·`part2-practice.zip`**(지금 두 검사가 여기서 멈춤), **`llm-practice.zip`**(ch12 노트북 12개가 2026-09-14 판이고 13절 없음), 필요하면 `part4-practice.zip`. 함께: `ch01-practice.zip`, `ch02-practice.zip`(13절 없음), `part1-practice.zip`(Ch3~5 개선 전), `part2-practice.zip`.
2. `part3/qa/run_continuity_bundle.py`를 **`--reuse-upstream` 없이** 실행(옛 `temporary_extraction` 폴더가 없음). 묶음에서 **Ch9 06 · Ch10 08 · Ch11 06** 노트북을 실제로 돌립니다.
3. 공용 `visual.cjs`로 **ch09 HTML 8쪽을 다시 찍어 14 → 16행**(`_notebook/checks/ch09-rag-first-run/visual-results.json`과 챕터 폴더 `qa/visual-results.json`). ch10 20 · ch11 16 · **ch12 28**은 이미 맞음.
4. `finalize_continuity_evidence.py` **15행을 `94` → `96`으로 올린 뒤** 실행. 지금 94는 **ch09의 −2와 ch12의 +2가 상쇄된 값**이라 3단계를 끝내야 96(ch08 14 + ch09 16 + ch10 20 + ch11 16 + ch12 28 + part3 2). 37행은 2단계를 먼저 끝내야 통과.
5. `check_continuity.py`·`qa/check_course_continuity.py`를 끝까지 실행(각각 **154행 part2 zip**·**212행 part1 zip**에서 멈춤, 1단계를 끝내면 지나감).
6. `part3/_build_index.py`를 마지막에 한 번 더 돌려 **Part 3 목차**와 `part3-practice.zip`을 맞춤(`CHAPTERS` 절 수 칸 ch09 **7**·ch10 **9**·ch11 **7**·ch12 **13**, 강의 시수는 따로). 함께: `textbook/part1/_build_index.py`·`index.html`(Ch3~5 절 수가 실습 절 전 값), Part 2 목차 재생성, 옛 경로가 남은 과거 목록 재생성(Ch7·8 요약 §12).
7. 옛 생성기·옛 그림 정리(삭제 아님, `qa/upgrade/before/generators/`로 `mv -n`): Ch11 `_make_notebooks.py`, Ch12 `figures/_gen_figures.py`·`qa/advanced_author.py`, 각 챕터 옛 SVG·excalidraw·`gates-wip*.json`. Ch3 labs 생성기도 남아 있음.
8. 삭제 승인(§4 목록).
9. **잠금 정리**(Ch12 A C-5): Ch12 잠금의 `pgvector`·`pypdf`를 뺄지 `tests/`와 함께 정함(빼면 `uv.lock`과 묶음 두 개 재생성).
10. `textbook/qa/upgrade-progress.md`와 Part 3 절 마무리, 2차 검토(각 `review-round1*.md` 끝 「2차 검토 때 볼 곳」).

**Part 1·2에서 넘어온 항목**(위 단계에 함께 처리)
- 삽화 대기: Ch4 02-5(`figures/02-5-쪽지와-카드-상자.prompt.md`, `qa/upgrade/illustration-pending.md`).
- 삽화 대조: 규격 §5-4가 Ch3에서 생겨 Ch1·2 채택본 대조 기록이 없음 → 점검.
- 재실행하게 되면 함께 고칠 코드: `cache_read` → `.get()`(Ch6 06·07, Ch8 05·06), Ch7 08 R-1, Ch8 06 R-2 등(각 요약 §12).

## 2. 뒤 챕터 인계 두 건

- **Ch15 01절 — 지금 깨져 있습니다(반드시)**. `part4/ch15-evaluation-advanced/_author.py` **212행** `assert len(rows) == 36 and len(low) == 2` 실패. 211행이 Ch12 시험 기록에서 `ndcg_at_5 < 1`인 줄을 뽑는데 12절 재실행으로 **2 → 1**(`Q090`, 첫 문서 `H02`, 정답 `['H01']`, `recall_at_5` `1.0`, `ndcg_at_5` `0.6309`). 함께 고칠 것 — (1) 212행 기대값 `2` → **`1`**, (2) 배포본 노트북 `labs/part4/ch15-evaluation-advanced/notebooks/01-실패-로그와-평가-대상.ipynb` 셀 7의 저장 출력 **두 줄 → 한 줄**(셀 9에 그 `assert`), (3) `data/evaluation-cases.json`의 **`Q006` 선정 근거**. 지금 멈추는 공용 검사는 없지만 `part4-practice.zip`·`llm-practice.zip`에 12절 기록이 함께 들어가 **학생이 한 묶음에서 실행하면 막힙니다**. Ch15가 「대기」라 Ch12에서 안 고침. (여기까지 **§2-7 리팩터 전** 설명, 시험 기록 `f9b16717…` 기준.)
  - **§2-7 리팩터 뒤 새 값(2026-09-21, Ch12 12절을 새 커널로 두 번 다시 실행)**: 새 시험 기록 `labs/part3/ch12-retrieval-tuning/runs/advanced-continuity-test-result.json`(`7b9b9db75a3986f6…`, `run_id` `advanced-continuity-20260921T082024-test-01`)에서도 `ndcg_at_5 < 1`인 줄은 **1개** — `Q090`(난이도 `hard`), `top_results` 문서 차례 `H02`·`H01`·`H01`·`M02`·`H01`(첫 문서 `H02`), 정답 `['H01']`, `recall_at_5` `1.0`, `ndcg_at_5` `0.6309297535714575`. 두 실행(첫 실행 사본 `ch12-…/qa/upgrade/before-2-7/runs/moved/20260921T081609/`)이 모두 같고, 시험 기록은 `run_id`·`selected_run_id`·`run_date` 말고 내용이 리팩터 전과 같습니다. 그래서 **212행 기대값 `2` → `1`·노트북 셀 7 저장 출력 두 줄 → 한 줄·`Q006` 선정 근거 세 가지 할 일은 그대로**입니다(Ch15는 이번 범위 밖이라 고치지 않음). Ch15가 36줄 `response` 칸 유무를 보는 210행도 새 실험 기록(`f16aa358…`, 36줄, `response` 칸 0)에서 그대로 맞습니다.
- **Ch13 07절 — 낡은 문장(코드는 안 멈춤) → 2026-09-19 처리 끝**(Ch13 07절 작업에서 b3과 `qa/author_ch13.py` 261~265행을 실제 값으로 고쳤고, 노트북 셀 15 출력과 글자까지 같습니다. 아래는 원래 내용). `part4/ch13-langgraph-basics/qa/author_ch13.py` **251행** `prior`와 `_src/07-RAG-통합과-시각화.html` **b3**의 「검색된 E01·E02 쪽」 → 지금 통합 기록의 `retrieved`는 **`E01-P03-C02`·`E01-P03-C01`·`E01-P03-C06` 세 건(모두 `E01`·3쪽)**이고 「쪽」이 아니라 **문서 청크 본문**을 넣음(`context_selection` `matched-chunk-text`, `reranker` `null`). 질문 `Q002`와 답이 있다는 사실은 맞음.

**뒤 챕터에서 확인**(앞 Part가 남긴 것)
- Part 1: Ch6 01(`.env` 무시 규칙 확인 한 문장, 「선택표」), Ch6 03·Ch19 01·02(규격 §2-2), Ch18 03(`gather(*jobs)`), Ch19 01(`fetch_orders` 판), Ch9 01(청크), Ch32 05(시크릿 ↔ Ch3 05). Ch5 연결 문장은 개선 전 Ch6·9·11·15·22 파일 기준 → 그 챕터가 바뀌면 Ch5 03·06~09 해당 블록 재확인. Ch4 06 「다음 학습」은 Ch5 01 출력이 바뀌면 확인.
- Part 2: Ch9 01 `_src` 38·42행 「조각」·05 b3 실패 모드 이름, Ch7 04 b6, Ch13 루프 삽화, Ch26 「나누기」.

## 2-2. Ch13 마감에서 생긴 항목 (2026-09-19)

1. **`labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json` 삭제 승인**(sha256 `c704a2eb…`, 2026-09-10). **개선 전 07절이 남긴 기록**이고 지금 교재와 값이 반대입니다(`reranker`가 `BAAI/bge-reranker-v2-m3`, `duration_ms` `13186.79`, `retrieved`에 `E02-P03-C01` ↔ 본문은 「리랭커를 부르지 않습니다」·「걸린 시간은 재지 않았습니다」). **코드로 읽는 쪽 0건**(`grep -rn "graph-integrated-result" --exclude-dir=.venv textbook labs`)이라 지워도 깨지는 검사가 없습니다. Ch13 세션에서는 **지우지 않았습니다.** 지우기로 하면 순서대로:
   1. 파일 삭제(승인 필요).
   2. `textbook/part4/public-files.json` **12행** `"labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json",` 제거.
   3. `textbook/part4/ch13-langgraph-basics/qa/public-files.json` `include`의 **10행** 같은 경로 제거(이 파일은 노트북 줄만 글로브이고 이 줄은 **명시 항목**입니다).
   4. `python3 textbook/part4/_build_index.py`(Part 4 목차 + `textbook/downloads/part4-practice.zip` 재생성, 지금 91항목 → 90항목) 뒤 `python3 textbook/part4/qa/check_delivery.py`.
   - 지우지 않기로 하면 Ch13 요약 §9의 「개선 전 기록이라 지금 교재와 값이 다름」을 그대로 두고 진행표에도 남깁니다.
2. **Ch13 실습 폴더 잠금의 쓰지 않는 패키지 넷**: `labs/part4/ch13-langgraph-basics/pyproject.toml`·`uv.lock`의 `numpy 2.5.3`·`pypdf 6.18.0`·`scikit-learn 1.9.0`·`sentence-transformers 6.0.1`(여덟 노트북에 import 0건). 빼면 학생 `uv sync --locked` 설치량이 크게 줄지만 `uv.lock`과 묶음 둘을 다시 만들어야 합니다(Ch12 §9 잠금 정리와 함께).
3. **삭제 승인 대상 추가**: `.cache/vm/venv-ch13-firstattempt-unused`(첫 시도 가상환경, 마운트 폴더라 내림 설치·삭제가 막혀 남음) · `labs/part4/ch13-langgraph-basics/.venv`(깨진 채 남아 `uv run --project`가 `.lock` 삭제에서 멈춤) · `.cache/vm/venv-ch13-langgraph-basics` · `/tmp/ch13-*`·`/tmp/ch13rv`·`/tmp/ch13rev`·`/tmp/ch13close` · `textbook/part4/ch13-langgraph-basics/qa/upgrade/gates-wip-*.json`.
4. **옛 파일 정리**(삭제 아님, `mv -n`으로 `textbook/part4/ch13-langgraph-basics/qa/upgrade/before/generators/`): `qa/author_ch13.py`·`figures/_gen_figures.py`(둘 다 첫머리 `raise SystemExit`으로 막아 둠). 옛 도식 `figures/NN-흐름.{caption.md,excalidraw,svg}` **스물한 개**는 본문이 참조하지 않습니다.
5. **`openai` 판 차이는 기록만 했습니다**(재실행 없음): 작업 환경 `3.16.2` ↔ 학생 잠금 `3.11.0`. `upgrade-contracts.md` §8과 Ch13 요약 §11에 한 줄씩 있습니다.

## 2-3. Ch14 마감에서 생긴 항목 (2026-09-20)

1. **옛 도식 27개 삭제 승인**: `textbook/part4/ch14-rag-patterns/figures/NN-*-flow.{svg,excalidraw,caption.md}`(01~09절 각 3개). 본문에서 참조하지 않고(`{{` 잔존 0건) 사본이 `qa/upgrade/before/figures/`에 있습니다. Ch14 세션에서는 **지우지 않았습니다.**
2. **`textbook/part4/ch14-rag-patterns/qa/upgrade/gates-wip-01-01.json` 삭제 승인**: 01절이 남긴 중복 보고 파일(정본은 `gates-wip-01.json`). 절별 `gates-wip-NN.json`·`gates-wip.json`도 `gates-after.json`으로 갈음됩니다.
3. **Ch14 실습 폴더 잠금의 `numpy 2.5.3`**: `labs/part4/ch14-rag-patterns/pyproject.toml`·`uv.lock`. **열 노트북 모두 import 0건**을 마감에서 확인했습니다. 빼면 `uv lock` → `uv sync --locked` → `part4-practice.zip`·`llm-practice.zip` 재생성이 함께 필요해 Ch14 세션에서는 빼지 않았습니다(Ch12 §9·Ch13 §2-2 2번의 잠금 정리와 함께 처리).
4. **옛 생성기 셋은 옮겼습니다(삭제 아님, 2026-09-20 완료)**: `textbook/part4/ch14-rag-patterns/_make_sources.py` · `figures/_gen_figures.py` · `labs/part4/ch14-rag-patterns/_make_notebooks.py` → `textbook/part4/ch14-rag-patterns/qa/upgrade/before/generators/`. `_build.py`·`run_section.sh`·게이트·`verify.py`·`_build_index.py`·`check_delivery.py`·`build_bundle.py` 어디도 부르지 않는 것을 `grep`으로 확인했고, 옮긴 뒤 `_build_index.py`를 다시 돌려 묶음 항목 수가 그대로였습니다(89).
5. **묶음 재생성**: `part4-practice.zip`은 마감에서 다시 만들었고(`Part 4: 32 verified sections; 89 bundled files`) `check_delivery.py`를 **끝까지 통과**합니다(zip 92항목·manifest 89항목, 해시 어긋남 0·Stale 0). **`llm-practice.zip`은 2026-09-14 판이라 낡은 항목이 139개**이고 `check_delivery.py`가 **111행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`**에서 멈춥니다. `check_course_continuity.py`도 212행 `Stale archive: part1-practice.zip/…`에서 멈춥니다(§1 전체 마감 순서에서 함께 처리).
6. **삭제 승인 대상 추가**: `.cache/vm/venv-ch14-rag-patterns` · `.cache/ch14close`(마감 해시 대조 기록) · `labs/part4/ch14-rag-patterns/__pycache__` · `textbook/part4/ch14-rag-patterns/__pycache__`·`qa/upgrade/__pycache__`.
7. **규격에 더한 두 줄**(`textbook/QUALITY-UPGRADE.md`와 `textbook/_notebook/upgrade/PLAYBOOK.md` 같은 내용): §4 「같은 코드로 다시 정의합니다」는 주석까지 같다는 뜻이 아니다(Ch14 A-3) · §7-2 서비스 요청이 3~5번을 넘으면 까닭을 진단에 적고 강사 확인 대상에 올린다(Ch14 10절 열 번).
8. **Ch15 이후는 손대지 않았습니다**(사용자 지시 「14장 까지만 작업해」, 2026-09-19). 위 §2의 **Ch15 01절 깨짐**은 그대로 남아 있습니다.

## 3. 강사 확인 대기 (챕터별, 진행표 모두 「완료(강사 확인 대기)」)

- **Ch1** A/B 배치 기준 `[[미정]]`.
- **Ch2** 03·05 강의 범위, 규격 네 규칙, 보충 과제 1·3·5.
- **Ch3** 02 강의 범위, Git 기준 버전, `HEAD@{1}` 복구, 삽화 05-5 교체.
- **Ch4** 03 강의 범위, Q1~Q6, 삽화 02-5 대기 마감.
- **Ch5** 03 강의 범위·심화 셀, 16h 유지, 컨텍스트 로트 정의, 08 기준 값 문장.
- **Ch6~8**(각 요약 §11) 세 챕터 범위 문장·규격 세 줄씩·Q 권고 설계 · Ch6 runs 한국어 키 · Ch7 05~08 meta 시수 변경, R-1 · Ch8 06 실습 1h, 07 결론, R-2.
- **Ch9**(§11) 절 제목 01·04, 07 표시 제목 축약, 강의·실습 범위 문장, meta 시수(강의 6h·실습 10h), 07 요청 6번, **정답키 공개 정책**(`queries.jsonl`을 학생 묶음에 넣고 세 delivery 검사 금지 목록을 바꿈 → **사용자 결정 2026-09-18: 현재 상태 유지**).
- **Ch10**(§12) 챕터·05·06 제목의 「청킹」(본문 0건), 07 제목의 「한국어」, 08절 임베딩 모델 하나, **05절 근거 예산 450조각·한도 150이 Ch8 입력 가용분 440과 다름**, 09 삽화 카드 수, 04절 분량, 09 실습 30분.
- **Ch11**(§16) 분량·시수 배분(05·06절이 가장 무거운데 실습 1h), 01절에서 검색기·b4 표를 뺀 것, 30문항 기준선을 임베딩으로 고른 것, 본문 값이 바뀐 자리(03 `0.200`→`0.173`, 04 `0.893`→`0.751`), 오류 이름 한국어 셋, 06절이 `runs/`에 파일 셋을 쓰는 것, 07 실습 설계, 삽화 06-5 빨강 딱지.
- **Ch13**(§12) `chapter.json` 목표 다섯 줄(「분기」·「재정렬」을 고치고 08절 줄 추가), `runs/graph-integrated-result.json` 삭제 승인, 01~06절 모델 요청 0번·API 키 셀 없음, `Literal`을 뺀 결정, 07·08절 코드 셀 32개, 01~06절 참고 확인일 2026-09-10 유지, 잠금의 쓰지 않는 패키지 넷, `textbook/part4/_build_index.py` ch13 설명 한 줄 수정.
- **Ch12**(§12) 07·08·09절 실습 1h → 3h, 12절 코드 셀 54개·함수 24개 재정의, 08절 33·03절 51개, 기록된 함수 예외 둘, 13절 질문 수 2 대 3, 08절 두 번째 리랭커, 잠금의 쓰지 않는 패키지, 본문 값이 바뀐 자리, 06절 참고 확인일 2026-09-09.
- **Ch14**(§11) `chapter.json` 학습 목표 여섯 줄(「임계값」·「노드」·「토큰·실행 시간」을 고치고 10절 줄 추가, `hours`는 그대로), 10절 서비스 요청 **열 번**(답 모델 5 + 임베딩 5 — 규격 §7-2 「3~5번」을 넘는 기록된 예외), 01절 이름의 「히스토리」, 01~05절 준비 셀에서 빠진 Ch12 설명 주석 셋을 언제 되살릴지, 그림 `alt` 200자 기준(앞 챕터 전체에 걸림), 실습 폴더 잠금의 `numpy`, 삽화 열 장의 관계 판독(특히 `04-5`·`05-5`·`10-4`), 한국어 감사 3단.

## 4. 삭제 승인 대상 (보존할 것 명시)

- **Part 1**: 옛 도식·`_gen_figures.py`·`gates-wip-*.json`, `textbook/_notebook/checks/--chapter/`, `/tmp/venv-ch04-data-tools`·`/tmp/ch04-*`·`/tmp/ch05-*`, `.cache/vm` 전체(목록은 각 챕터 요약 「남은 것」).
- **Part 2**: 각 요약 §12 목록, `.cache/vm/venv-ch06~08`.
- **Part 3**: Ch12 `.venv`(빈 폴더), `runs/continuity/` 12절 사본 넷 중 **셋**(`20260918T231546`·`231622`·`231828`), `.cache/vm/venv-ch09~12`·`hf`(6.0GB)·`pgenv`·`pgdata`, `/tmp/ch09-*`~`/tmp/ch12-*`, 챕터 `__pycache__`·`.pytest_cache`·`.ruff_cache`.
- **Part 4**: Ch13 §2-2 3번 목록, Ch14 옛 도식 27개·`qa/upgrade/gates-wip-*.json`(`gates-wip-01-01.json` 포함)·`.cache/vm/venv-ch14-rag-patterns`·`.cache/ch14close`·챕터 `__pycache__`.
- **보존**: 정본과 같은 **`20260918T232052`**(검사가 요구 — §2-7 리팩터 뒤로는 지금 정본과 같은 사본이 **`20260921T082024`**이고 `20260918T232052`는 옛 정본 사본, 둘 다 보존), **Ch9·Ch10의 옛 사본**(`check_course_continuity.py` 184행이 옛 정본의 줄마다 이름을 찾음), 렌더 도장 `*.render.json`, 옛 생성기(삭제가 아니라 `qa/upgrade/before/generators/`로 이동).
- 2026-09-19 분할 작업 중 실수로 만든 `textbook/qa/_to_delete/_trim_tmp.py`(임시 스크립트, 지워도 됨).

## 5. 미결 (요약 사이 어긋남, 원문은 안 고침)

**Part 1**
1. Ch1 05 「Ch 2의 확장 과제를 함께 합니다」 — Ch2에는 「확장 과제」가 없고 「확장 경로(B)」·「A트랙 보충 실습」만 있음.

**Part 2**
1. 「청크」: Ch6 04 = 스트리밍 답의 일부 ↔ Part1 §5·Ch8 §4 = Ch9 문서 덩어리(청크). → **결정(규격 §4)**: 「스트림 청크」(Ch6 04) / 「문서 청크」(Ch9~), 한정어 없는 「청크」 금지, Ch9 첫 자리에서 구분 한 문장. Ch6 04 본문 표기는 전체 마감 때 「스트림 청크」로 맞춤.
2. Ch8 요약 §5가 try·`BaseModel`·타입힌트를 미교육으로 적음 ↔ Part1 §1(Ch2 05·07)·Ch6 요약 §6, try는 Ch6·7이 씀.
3. Ch8 요약 §1 「새 API」에 Ch6이 가르친 `usage_metadata`·`json.dumps`·`cache_read` 등이 있음.
4. subgraph 이름: Ch7 01~03·Ch8 「칸」 ↔ Ch7 04~09 「큰 상자」, 「칸」은 Ch6 「칸(필드)」와도 겹침.
5. 「쟁반」: Ch6 01-5 = 하네스인데 Ch8 「쓰지 않은 말」은 Ch4·5 뜻만 적음.
6. PLAYBOOK §0·Part1 §9 가상환경 `/tmp/venv-…` ↔ Part 2 실제 `.cache/vm`.

**Part 3**
1. `finalize_continuity_evidence.py` 15행: Ch10 §9 4단계·Ch11 §15 4단계 첫 문장은 「이미 **94**(고치지 마세요)」인데 Ch12 §16 4단계는 「**94 → 96**으로 올린 뒤 실행」. 두 요약 끝의 2026-09-19 갱신 문단이 96을 말하므로 **Ch12 판이 맞음.** Ch10 §8은 아직 「실제 합 **92**」(ch12 26 → 28 뒤 94), Ch9 §9 4단계 한 문단에 94의 구성이 두 가지(ch09 16 + ch12 26 / ch09 14 + ch12 28).
2. ch09 화면 결과 파일 경로: Ch9 §9 3단계는 챕터 폴더 `qa/visual-results.json`만, Ch10 §9 3단계는 공용 `_notebook/checks/ch09-…/visual-results.json`을 먼저 적음. finalize가 세는 쪽이 어느 파일인지 Ch9 요약만으로는 알 수 없음.
3. Ch10 §6이 「꼭 고쳐야 할 어긋남」으로 넘긴 Ch11 01절 b3(「Ch10 08절 … 세 청킹 방법과 **두 임베딩 모델**」)의 처리 기록이 Ch11 요약(§14·§16) 어디에도 없음.
4. 미교육 목록과 「0건」 목록이 섞임: Ch10 01절이 가르친 `Path`의 `.name`·`.stem`·`.suffix`와 `sorted(목록)`을 Ch11 §12·Ch12 §14가 「아직 가르치지 않은 것」에 넣었고, Ch12 §14의 **f-string·기본값 매개변수**는 Part 1 §1(Ch2)에서 가르친 것.
5. 「후보 목록」과 「색인」이 두 뜻: 후보 목록 = 중복 뺀 문서 목록(Ch11 02) ↔ **「후보 목록 크기」** = HNSW `ef_search`(Ch12 02); 색인 = 벡터스토어에 넣어 만든 것(Ch9 01) ↔ **데이터베이스 색인**(Ch12 02). 어느 요약도 갈라 두지 않음(Ch12 §9는 「인덱스」만 금지어).
6. 「흰 카드」: Ch9 01-5·Ch10 09-4 = 문서 청크, Ch11 02~04절 = 후보 한 줄, 05절부터 = 질문 한 장. Ch11 §9는 카드 상자·봉투·서랍만 「뜻이 정해져 있어 쓰지 않았다」고 적음.
7. 「입력 가용분」 값이 셋: Ch8 01 **440** ↔ Ch10 05 근거 예산 450조각·한도 150 ↔ Ch12 09 **3400**. Ch10은 Ch8과 다름을 본문에 적었고(§12) Ch12는 Ch8·Ch10과의 차이를 적지 않음.
8. Ch12 기록 세 파일 이름에 `continuity`가 들어 있는데, Ch11 §5의 이름 규칙(`continuity`가 들어가면 `run_continuity_bundle.py` 79~83행이 증거 폴더로 옮김)과 `finalize_continuity_evidence.py` 51행 `len(source_ids) == 7`(ch09 1 + ch10 6)에 어떻게 맞물리는지, Ch12 §4의 「읽는 쪽 다섯 곳」에 그 두 스크립트가 없어 확인되지 않음.
9. 가상환경 경로: Part 1 §9·PLAYBOOK §0의 `/tmp/venv-…` ↔ 실제 `.cache/vm`(Part 2 미결 6)에 더해, Part 3에서는 **uv 캐시만 `/tmp/uv-cache`**로 두는 예외가 생김.
