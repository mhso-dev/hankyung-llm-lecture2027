# 12절 품질 개선 진단 (종합 튜닝과 실험 로그)

대상: `_src/12-종합-튜닝과-실험-로그.html` · `labs/part3/ch12-retrieval-tuning/notebooks/12-종합-튜닝과-실험-로그.ipynb`
형식 **experiment** 유지 · 작업 2026-09-18 · 생성기 `qa/upgrade/author_12.py`
수정 전 사본: `qa/upgrade/before/_src/12-*.html` · `before/notebooks/12-*.ipynb` · `before/figures/12-*`

## 1. 게이트 전후

| 게이트 | 전(`gates-before.json`) | 후(`gates-after-12.json`) |
|---|---|---|
| G1 문법 사다리 | 43 | **0** |
| G2 셀 모양 | 11 | **0** |
| G3 주석 | 12 | **0** |
| G4 실제 모델 | 0 | **0** |
| G5 노트북 설명 | 12 | **0** |
| G6 문장 | 13 | **0** |
| G7 그림 | 3 | **0** |
| 합계 | **94** | **0 (PASS)** |

- 코드 셀 12개 → **54개**, 검사 문장 105 → **424**.
- 새 커널 실행 PASS(`2026-09-18T23:20:56Z`, `code_sha256` `9fc0c448…`·`outputs_sha256` `ef7db1a0…`).
- `verify.py --chapter` `PASS 12 sections / 428 code cells (max 20 lines)`.
- `visual.cjs` 1280·390 PASS(공용 `visual-results.json` **26행 유지**, 12절 두 줄만 다시 찍음).
- 실습 폴더 테스트 `4 passed`(작업 전후 같음, `tests/test_continuity.py`의 12절 블록은 이 절에서 고침 — §8).

## 2. 수정 전 주요 문제

1. **가르친 적 없는 도구로 만든 절이었습니다.** 셀 12개에 내포식·제너레이터 식·조건 표현식·`lambda`가 43곳이었고 `TfidfVectorizer(analyzer="char_wb")`·`cosine_similarity`·`np.argsort`로 검색을 만들었습니다. Part 1~3에서 `sklearn`과 `numpy`를 가르친 적이 없습니다.
2. **앞 절과 이어지지 않았습니다.** 36벌의 손잡이가 「문자 분석기 2종 · n-gram 범위 3종 · 보고 순위 2종 · λ 3종」이었습니다. 이 챕터가 05~11절에서 가르친 가중치·후보 수·관련성 비중은 하나도 손잡이가 아니었습니다.
3. **셀 12개가 모두 첫 줄 주석 없이 15줄을 넘었습니다.** 제목 셀·핵심 그림 셀·결과 읽기 셀도 없었습니다.
4. **본문이 그림 없이 옛 `{{svg:}}` 토큰 두 개만 썼습니다.** Mermaid 0장·삽화 0장·설계표 없음.
5. **본문 숫자가 노트북 출력과 달랐습니다.** b5·b6이 「시험 nDCG@5 0.9508」을 인용했지만 그 값은 지금 노트북 어디에도 없습니다.
6. **리랭커를 쓴 통합 실행과 TF-IDF 36벌이 한 절에 섞여 있었습니다.** 「고른 설정」과 「실제로 돈 설정」이 달랐습니다.

## 3. 산출 파일 계약 (읽는 쪽을 실제 파일에서 확인)

이 절은 이 챕터에서 **유일하게 파일을 쓰는 절**입니다. 읽는 쪽 다섯 곳을 열어 키·모양을 확인했습니다.

| 읽는 쪽 | 보는 것 |
|---|---|
| `labs/part3/ch12-retrieval-tuning/tests/test_continuity.py` 61~129행 | 36줄·`selected_run_id`·`settings` 일치·사본 세 개 일치·`smoke["settings"]["dimensions"] == 256`·`["chat"] == "gpt-5.4-mini"`·`chunk_id`가 `{doc_id}-P{page:02d}-`로 시작 |
| `textbook/part3/qa/check_continuity.py` 81~137행 | 위와 같은 것 + 네 칸(`recall_at_5`·`recall_at_50`·`precision_at_5`·`ndcg_at_5`)을 **다시 계산해 대조**(`abs_tol=1e-10`) + 갈래 세 개(`easy`·`medium`·`hard`) 평균 대조 + 통합 기록의 출처 표시가 검색한 쪽 안인지 |
| `textbook/qa/check_course_continuity.py` 115~180행 | 위와 같음 |
| `textbook/part4/ch13-langgraph-basics/qa/author_ch13.py` 259·272행 | 통합 기록의 `question`·`retrieved[].doc_id` |
| `textbook/part4/ch15-evaluation-advanced/_author.py` 210·211행 | 기록 36줄의 `response` 칸 유무, 시험 기록의 `ndcg_at_5 < 1`인 줄 |

지킨 것: 줄 수 36 · 칸 이름 여섯 개 · `candidate_unit` `chunk` · `report_unit` `unique-parent-document` · `metrics_policy` `chunk-candidate-unique-parent-macro-v1` · `query_count` 15 · `excluded_query_count` 0 · `settings.chat` `gpt-5.4-mini` · `settings.dimensions` 256 · 지표는 **반올림하지 않고** 저장.
더한 것: 08~11절이 쓰던 두 칸 `recall_at_3`·`chunk_precision_at_5`(검사 스크립트는 네 칸만 보므로 더해도 통과).

**바뀐 값(키는 그대로)** — 다시 실행했으므로 해시가 바뀌었습니다.

| 파일 | SHA-256 앞 20 | 줄·칸 |
|---|---|---|
| `runs/advanced-continuity-experiment-log.jsonl` | `9b447a417c3ed9ec5478` | 36줄 · 한 줄 17칸 |
| `runs/advanced-continuity-test-result.json` | `f9b16717d910d8612742` | 칸 18개(`selected_run_id` 포함) |
| `runs/advanced-continuity-integrated-result.json` | `ce76d3d8e3139d1691a0` | 칸 11개 |

사본은 `runs/continuity/20260918T232052/`입니다. 실행마다 사본 폴더가 하나 늘어 이 절 작업에서 **네 개가 늘었습니다**(`20260918T231546`·`231622`·`231828`·`232052`). `runs` 파일 수 36 → 48, `runs/continuity` 2.7MB. 삭제는 막혀 있어 그대로 두었고, `public-files.json`에는 맨 위 파일 세 개만 있어 학생 묶음은 커지지 않습니다. `check_continuity.py`는 사본 가운데 **하나라도** 지금 파일과 같으면 통과합니다.

**뒤 챕터에 남는 차이(Ch 13 마감 때 고칠 것)**: 통합 실행 값이 달라졌습니다. `settings.reranker`가 `"BAAI/bge-reranker-v2-m3"` → `null`, `settings.context_selection`이 `"matched-page-text"` → `"matched-chunk-text"`, `retrieved`가 `E01 p.3`·`E02 p.3` 두 건 → `E01 p.3` 문서 청크 세 건입니다. `textbook/part4/ch13-langgraph-basics/_src/07-RAG-통합과-시각화.html` b3의 「검색된 E01·E02 쪽」 문장이 이제 맞지 않습니다. Ch 13 코드는 `question`과 `retrieved`를 읽어 출력만 하므로 멈추지는 않습니다.

`data/advanced-documents.json`(`832d89c2…`)·`data/advanced-queries.json`(`dcf7f288…`)·`pyproject.toml`(`5b10531e…`)·`uv.lock`(`f13e8c6f…`)은 한 글자도 고치지 않았습니다. Ch 9·10·11 기록과 Ch 6~8 사슬은 읽기만 했습니다.

## 4. 손잡이 두 개를 고른 까닭

- **가중치(06절)와 관련성 비중(10절)** 두 개를 골랐습니다. 이 챕터가 실제로 가르친 손잡이이고, 둘 다 값 하나만 바꿔도 앞 절 함수를 그대로 쓸 수 있습니다.
- **순위 상수를 손잡이로 두지 않았습니다.** 손잡이로 만들려면 06절 `fuse_scores()`가 상수를 인자로 받게 고쳐야 해서 「같은 코드로 다시 쓴다」가 깨집니다.
- **후보 수를 손잡이로 두지 않았습니다.** 08절이 이미 후보 수 2·4·8을 견주어 끝냈습니다. 대신 `candidate_k`를 설정 칸에 8로 적어 기록에는 남깁니다.
- **리랭커를 넣지 않았습니다.** 36벌 × 15문항 = 540번 리랭킹이 필요하고, 통합 실행에만 넣으면 「고른 설정」과 「실제로 돈 설정」이 달라집니다. 08절이 「이 조건에서는 어느 리랭커가 낫다고 말할 수 없다」로 끝난 것도 함께 셈에 넣었습니다.

## 5. 무엇으로 고를지 (탐색 실행 뒤 정함)

탐색 실행(`/tmp/ch12-12/probe4.py`, 2026-09-18)에서 계약 네 칸(`recall_at_5`·`recall_at_50`·`precision_at_5`·`ndcg_at_5`)이 서른여섯 줄에서 거의 갈리지 않았습니다. 교재 실행에서도 재현율 세 칸은 `[1.0]`, 부모 문서 정밀도는 `[0.2]` 한 가지뿐이었습니다.

그래서 **문서 청크 정밀도 자리 5**(08절 판)를 고르는 칸으로 두었습니다. 노트북 7절이 **먼저 출력으로 「어느 칸이 갈리는가」를 보이고** 고릅니다(규격 §3, 기준을 먼저 보이는 순서).

관찰한 어긋남: 관련성 비중을 1.0에서 0.0으로 내리면 문서 청크 정밀도 평균은 내려가고 nDCG 자리 5 평균은 `0.9795` → `0.9944`로 올라갑니다. 네 번 실행에서 nDCG 칸은 글자까지 같았습니다. 까닭은 재지 않았고 본문에 「이번에 확인하지 않았습니다」로 적었습니다.

## 6. 개발 15 / 시험 15 — Ch 11 약속을 지킨 순서

1. 노트북 3절에서 개발 열다섯만 벡터로 바꿉니다(임베딩 15번).
2. 6절에서 서른여섯 벌을 개발로 재고 기록 파일을 씁니다.
3. 7절에서 기록을 읽고, 8절에서 설정 한 벌을 고릅니다.
4. **9절에서 시험 열다섯을 처음 엽니다**(임베딩 15번). 고른 설정 한 벌만 한 번 적용합니다.
5. 시험 값을 본 뒤 설정을 다시 고르는 셀은 없습니다. 본문 b4·b7과 노트북 9절 머리글에 그 순서를 적었습니다.

## 7. 코드 셀 수 (54개)

규격 목표(25~35)보다 많습니다. 내역은 준비 6 + 지문·값 4 + 재료 3 + **앞 절 함수 다시 만들기 16** + 지표·기록 함수 8 + 설정·실행 4 + 결과 읽기 4 + 시험 2 + 통합 실행 5 + 기록 2입니다.

- 앞 절 함수 **스물네 개**를 09절 방식대로 준비 셀 열여섯 개에 묶었습니다(`lesson_role="setup"` + `upgrade_allow=["multiple_defs_in_cell"]`). 셀당 3~14줄이라 더 묶으면 15줄 상한을 넘습니다.
- 스물네 개가 필요한 까닭은 계약 칸 이름 때문입니다. `ndcg_at_5`·`precision_at_5`를 기록에 남기려면 Ch 11 04절 함수 네 개(`rank_weight`·`dcg_at`·`ideal_dcg`·`ndcg_at`)와 03절 `precision_at`을 07~11절에서 쓰지 않았어도 다시 만들어야 합니다.
- 함수 본문은 모두 10줄 이하이고, 주석·빈 줄을 뺀 코드 줄 수는 셀마다 3~15줄입니다.
- 03절이 51개, 02절이 39개였으므로 이 챕터에서 처음 있는 일은 아닙니다. 더 줄이려면 절을 둘로 나눠야 해서 그대로 두고 여기에 적습니다(강사 확인 대상).

## 8. 실습 폴더 테스트 `tests/test_continuity.py` (08·10절 선례대로 고침)

수정 전 161~188행은 12절 노트북에서 이름 네 개를 찾아 불렀습니다. 그 계약이 `TfidfVectorizer`와 넘파이 배열을 전제로 해서 사다리에 맞춘 12절과 맞지 않았습니다. 08·10절이 한 것처럼 **이름 공간으로 불러오는 방식**(`load_notebook_namespace()`)으로 바꾸고 넣는 값을 파이썬 목록으로 고쳤습니다.

| 이름 | 전 | 후 |
|---|---|---|
| `eligible_items(subset)` | 같음 | 같음 |
| `metrics(...)` | `(doc_ids, gold, all_ids)` → 값 4개, 앞 둘이 `(0.5, 0.5)` | `(candidate_doc_ids, top_doc_ids, gold, picked_chunk_ids)` → 값 6개, **둘째·셋째가 `(0.5, 0.5)`** |
| `mmr(...)` | 넘파이 배열 입력 | 10절과 같이 파이썬 목록 입력, 고른 자리 번호 목록 반환 |
| `evaluate_config(config, items)` | 이름 공간 `{eligible_items, TfidfVectorizer, chunks, mmr, metrics}`, `config`에 `analyzer`·`ngram`·`lambda` | 이름 공간에 `TfidfVectorizer` 없음, `config`는 `weights`·`relevance_weight`·`rank_constant`·`candidate_k`·`candidate_unit`·`report_k`·`report_unit`, 질문별 순위는 `lists_by_qid`·`vector_by_qid`로 넣음 |

`ValueError("평가 가능한 문항 …")`과 `top_results`의 `rank` 1부터는 그대로 둡니다. 08·10절 블록(노트북 이름 공간·문서 청크 ID 모양)은 손대지 않았습니다. 전후 모두 **4 passed**입니다.

## 9. 실행값 (2026-09-18 마지막 새 커널 23:20:56Z)

- `부모 문서 수: 6` · `문서 청크 수: 175` · `질문 수: 30` · `개발 질문 수: 15` · `시험 질문 수: 15` · `문서 청크 하나의 평균 검색 낱말 수: 44.01`(07~11절과 같음).
- `만들 설정 수: 36` · `기록 한 줄의 칸 수: 17` · `고정으로 넣을 칸 수: 10`.
- 서른여섯 줄의 서로 다른 값: `recall_at_3`·`recall_at_5`·`recall_at_50` 모두 `[1.0]`, `precision_at_5` `[0.2]`, `ndcg_at_5` `[0.9667, 0.9754, 1.0]`, `chunk_precision_at_5` 열네 가지.
- 고른 설정: `가중치 [0.0, 1.0]` · `관련성 비중 1.0` · 그 줄 `문서 청크 정밀도 자리 5: 0.88` · `nDCG 자리 5: 1.0`.
- 시험 한 번: `ndcg_at_5 0.9754` · `chunk_precision_at_5 0.8533` · 재현율 세 칸 `1.0` · `precision_at_5 0.2`.
- 통합 실행: `Q002` · 보고 자리 다섯 개가 모두 `E01` · 넣을 자리 3 · `첫 출처 표시: [E01 p.3]` · `넣을 글의 길이: 490` · `보낸 글의 길이: 588` · 답 「도서는 한 번에 **7권까지** 빌릴 수 있고, **14일 동안** 대출할 수 있습니다. [E01 p.3]」.
- 요청: **임베딩 31번**(문서 청크 1 + 개발 15 + 시험 15), **답을 쓰는 모델 1번**, 리랭커 0번. 합쳐 미화 0.01달러 아래. 노트북 전체 10.5초(패키지가 이미 깔린 작업 환경 기준, 노트북 준비물의 「2분 안팎」은 설치까지 넣은 학생 기준).

### 실행마다 흔들리는 값 (09~11절 인계 확인)

같은 코드로 **새 커널 네 번**(`/tmp/ch12-12/runA·runB·runC.ipynb`와 교재 출력) 실행했습니다. `code_sha256`은 네 번 모두 `9fc0c448…`이고 다른 셀은 **두 개**뿐입니다.

- 7절 첫 표의 `chunk_precision_at_5` 값 목록(열네 가지 가운데 한두 값이 갈림, 예 `0.8667` ↔ `0.88`).
- 7절 손잡이별 평균 표의 **문서 청크 정밀도 칸**(예 가중치 `[1.0, 0.0]`이 `0.6711` ↔ `0.68`).
- **nDCG 칸은 네 번 모두 글자까지 같았습니다.** 고른 설정도 네 번 모두 `[0.0, 1.0]`·`1.0`이었고 시험 값 `0.9754`·`0.8533`도 같았습니다. 답 문장도 네 번 모두 같았습니다.
- 그래서 그림 라벨·정리 세 줄·복습 해설에는 네 번 모두 같았던 값만 넣었고, 흔들린 값은 본문 표와 b7에만 적었습니다(10·11절과 같은 규칙).

## 10. 그림

설계표는 `qa/upgrade/12-figures.md`입니다. Mermaid 4장 + 삽화 1장.

- `12-1-설정-서른여섯-벌과-두-번의-실행`(flowchart TB, 본문 b4 + 노트북 「오늘 볼 그림」 첨부)
- `12-2-기록-한-줄에-담는-것`(flowchart LR, b4)
- `12-3-설정-하나가-질문-하나를-재는-차례`(flowchart TB, b5)
- `12-4-개발에서-고르고-시험에서-한-번`(flowchart TB, 칸 두 개, b6) — 처음 렌더에서 subgraph 제목이 길어 화살표가 제목을 지나가 제목을 줄이고 `render_mermaid.py --force`로 다시 렌더했습니다.
- 삽화 `12-5-연습-자물쇠와-봉한-상자` — job `88933c13-2cf4-4361-94e5-872e2e40e354`, **1차 채택**(재생성 없음), 2크레딧. 원본 2752×1536 sha256 `a639d9e6…`, 저장본 1100×614. 저장 PNG를 채택 job 결과와 같은 폭으로 줄여 픽셀 대조했고 `ImageChops.difference().getbbox()`가 `None`이었습니다.
- 옛 `{{svg:12-실험-로그}}`·`{{svg:12-통합-RAG}}` 두 토큰을 뺐습니다. 원본 `.excalidraw`·`.svg`·`.caption.md` 여섯 파일은 `figures/`에 그대로 있고 `qa/upgrade/before/figures/`에도 복사돼 있습니다.

## 11. 본문에서 고친 것

- meta의 「코드 Jupyter Notebook」을 07~11절처럼 노트북 경로로 고쳤습니다. 시수는 **강의 1h · 실습 1h 그대로**(09절에서 맞춘 절 합을 지킴).
- b3이 「앞 절의 변수나 실행 상태는 필요하지 않습니다」로 끝나 앞 절을 가리키지 않았습니다. 06·08·09·10·11절과 Ch 11 02~04절을 이름으로 이었습니다.
- 용어 표를 새로 만들고 네 개(손잡이 · 설정 한 벌 · 입력 지문 · 실험 기록 한 줄)를 세 문장 규칙으로 풀었습니다. meta 「새 용어 4」 유지.
- b6을 표 네 개로 다시 썼습니다. 지표 칸별 값, 가중치 여섯 줄, 관련성 비중 여섯 줄, 개발·시험 여섯 줄입니다.
- 「다음 학습과 이어지는 지점」은 Ch 13·Ch 15를 가리키게 두었습니다(실습 절을 붙이는 다음 단계에서 고칩니다). 두 챕터가 실제로 읽는 파일과 칸을 열어 보고 문장을 썼습니다.
- 마지막 재실행 뒤에 설명만 고친 것은 `mdpatch.py`로 처리했습니다: 노트북 `넣을 글의 길이: 451` → `490`(G5 지적), 「함수 스물두 개」 → 「스물네 개」, 「시험에서는 한 질문이 2위였습니다」를 nDCG 값에서 나온 셈이라고 풀어 쓴 두 문장, 「오늘 볼 그림」 alt의 맨 아래 두 상자 설명.

## 12. 작업 환경

- 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part3/ch12-retrieval-tuning 12`(마지막은 `--no-exec`).
- 실습 폴더 가상환경에 `pytest`가 없어 테스트는 `UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch12-retrieval-tuning UV_NO_SYNC=1 uv run --project labs/part3/ch12-retrieval-tuning --with pytest==9.1.0 python -m pytest …`로 돌렸습니다. 이 세 변수를 주지 않으면 uv가 루트 디스크에 torch·CUDA를 새로 받다가 `No space left on device`로 멈춥니다.
- `visual.cjs`는 `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`와 `ONLY=12- node /tmp/ch12-12/vis12.cjs …`로 돌렸습니다.
- 루트 디스크 여유 2.1G. 리랭커 모델(`.cache/vm/hf`)은 이 절에서 건드리지 않았습니다.
- `textbook/part3/qa/check_delivery.py` 종료 코드 0. `textbook/part3/qa/check_continuity.py`는 01~11절과 같은 **154행 `Stale archive: part2-practice.zip`**에서 멈춥니다(그 앞의 ch12 계약 검사는 모두 통과). `textbook/qa/check_course_continuity.py`도 같은 까닭으로 **212행 `part1-practice.zip`**에서 멈춥니다.

## 13. 강사 확인 대상

1. **코드 셀 54개**(§7). 규격 목표 25~35보다 많습니다. 줄이려면 앞 절 함수 다시 만들기 열여섯 셀을 별도 파일 import로 바꾸거나 절을 둘로 나눠야 합니다.
2. **실습 폴더 테스트를 고쳤습니다**(§8). 12절 블록의 넣는 값과 기대 값이 바뀌었습니다.
3. **Ch 13 07절 b3 문장이 낡았습니다**(§3). 통합 기록의 `retrieved`가 이제 `E01` 한 부모입니다. Ch 13 개선 때 함께 고쳐야 합니다.
4. **`runs/continuity` 사본 폴더가 네 개 늘었습니다**(§3). 삭제 권한이 없어 그대로 두었습니다.

## 검토 반영 (2026-09-19, 챕터 마감)

- **12-1(하) 「기록 칸 이름 여섯 개는 검사 스크립트가 다시 계산해 대조합니다」** — 실제보다 넓은 문장이라 「기록 칸 여섯 개 가운데 **네 개**는 검사 스크립트가 다시 계산해 대조합니다. 그 네 개는 `recall_at_5`·`recall_at_50`·`precision_at_5`·`ndcg_at_5`입니다.」로 고쳤습니다. 이 절이 **고르는 칸으로 쓴 `chunk_precision_at_5`는 다시 계산되지 않는 칸**입니다(`check_continuity.py` 90행·`check_course_continuity.py` 124행).
- **12-2(하) 코드 셀 54개·앞 절 함수 24개 재정의** — 검토 권고대로 **절을 나누지 않고 그대로** 두었습니다. 나누면 「개발에서 고르고 시험에서 한 번」이 두 절로 끊기고 기록 파일을 쓰는 절이 둘이 됩니다. (a) meta 시수, (b) 노트북 5절 머리말 보강을 **강사 확인 대상**으로 올렸습니다.
- **C-6(하) `review-pack/12-….md`** — 13절이 `mdpatch.py`로 b8과 노트북 정리를 고친 뒤 다시 만들지 않아 옛 판이었습니다. 마감에서 `pack.py`로 **13개 절 모두** 다시 만들었습니다.
- **결정 요청** — 손잡이 36벌(가중치 6 × 관련성 비중 6)·리랭커 미사용·계약 칸 때문에 함수 24개 재정의·코드 셀 54개는 **모두 유지**했습니다.
- 노트북 재실행 없음: `code_sha256` `9fc0c4485d9e2ca7`·`outputs_sha256` `ef7db1a0485caa94`·`executed_at` 2026-09-18T23:20:56Z 전후 같음. 12절 기록 세 파일도 바이트 그대로입니다(`9b447a41…`·`f9b16717…`·`ce76d3d8…`).

## §2-7 리팩터 (2026-09-21, 작업자 B)

- 준비 셀 16개(함수 24개, 164줄)를 import 세 줄(12개)로 바꿈. Ch 11 04절 함수는 Ch 11 도구 파일 판(`rank_weight(rank)`·`ideal_dcg(gold_count, cutoff)`) — 값이 같아 시험 기록 내용이 바이트까지 같게 나옴. b7 「순위 상수 … `fuse_scores()`의 모양을 바꿔야」 → 「06절에서 정한 60을 모든 설정에 그대로 썼습니다」. 코드 셀 54 → 38, 코드 줄 532 → 372.
- 새 커널 두 번: 7절 두 표와 고른 줄 정밀도 `0.8667` ↔ `0.88`만 다름. 교재 출력(두 번째)에 맞춰 b6 손잡이 표 여덟 칸·「열다섯 가지」, b7 「두 번」을 고침. 고른 설정·시험 지표·통합 기록 같음. 산출 파일 해시 `9b447a41…`·`f9b16717…`·`ce76d3d8…` → `f16aa358…`·`7b9b9db7…`·`7b142cd5…`(사본 `20260921T082024/`).
- 세부는 `handoff.md` 「§2-7 리팩터 B — 07~13절과 챕터 마감」.
