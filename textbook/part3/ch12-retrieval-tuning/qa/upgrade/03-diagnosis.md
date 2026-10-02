# Ch 12 03절 「메타데이터 필터와 iterative scan」 품질 개선 기록

규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`, 절 사이 인계 `handoff.md`.
작업 2026-09-18. 앞 내용은 `textbook/qa/upgrade-course-summary.md`(Part 1·2), Ch 09·Ch 10·Ch 11 `qa/upgrade/chapter-summary.md`, 이 챕터 01·02절 완료본과 `handoff.md` 「§01 → §02」·「§02 → §03」을 읽고 맞췄습니다.
**이 절은 이 챕터에서 유일한 `paired` 형식입니다**(`chapter.json`). 형식을 그대로 유지했습니다.

## 1. 게이트 전후

| 게이트 | 수정 전 | 수정 뒤 |
|---|---|---|
| G1 문법 사다리 | 4 | **0** |
| G2 셀 모양 | 6 | **0** |
| G3 주석 | 7 | **0** |
| G4 실제 모델 | 0 | **0** |
| G5 노트북 설명 | 8 | **0** |
| G6 문장 | 13 | **0** |
| G7 그림 | 3 | **0** |
| 합계 | **41** | **0 (PASS)** |

- 기록 파일: 수정 전 `gates-before.json`(챕터 첫 절 작업에서 12절 전체를 한 번 기록), 수정 뒤 `gates-after-03.json`·`gates-wip-03.json`.
- 코드 셀 7개 → **51개**(준비 5), 검사 문장 73개 → **406개**.
- 새 커널 실행: `PASS 03-메타데이터-필터와-iterative-scan.ipynb: 51 cells`. 같은 코드로 두 번 실행해 `code_sha256` `56595a043b3d0d0a…`와 `outputs_sha256` `76e5c409969eeabc…`가 같았습니다. 교재 출력은 마지막 실행 **2026-09-18T16:12:36Z**입니다.
- `verify.py --chapter`: `PASS 12 sections / 180 code cells (max 25 lines)`(02절 뒤 136셀 → 180셀, `max 25`는 아직 개선 전인 12절 셀).
- `visual.cjs`: 1280px·390px 모두 PASS. 공용 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`은 **26줄을 유지**하고 03절 두 줄만 다시 찍었습니다(02절처럼 `/tmp/ch12-03/vis12.cjs` 사본에 `ONLY` 필터와 병합 저장을 넣어 실행, 공용 도구 원본은 고치지 않았습니다). 두 줄의 결과 값이 개선 전과 같아 파일 바이트는 바뀌지 않았습니다.
- 실습 폴더 테스트: 작업 전후 모두 **4 passed**(`uv run --project labs/part3/ch12-retrieval-tuning --with pytest==8.4.2 python -m pytest labs/part3/ch12-retrieval-tuning/tests -q`).

## 2. 수정 전 주요 문제

1. **문법 사다리**: 내포식 세 곳(`[("common", v) for v in common]` 계열·`[(row_id, float(distance)) for ...]`), 제너레이터 식 한 곳(`next((folder for folder in [Path.cwd(), *Path.cwd().parents] ...), None)`), 한 글자 변수 `v`, 세미콜론 세 곳, 한 줄 복합문 한 곳(`if not backup.exists(): backup.write_bytes(old)`).
2. **가르치지 않은 도구**: `numpy`(`np.random.default_rng(12)`·`np.zeros`·`rng.normal`)와 `pgvector` 파이썬 패키지의 `register_vector`, `conn.transaction()`과 `with` 두 개 묶기, f-string으로 만든 `SET LOCAL hnsw.iterative_scan={mode}`, 함수 안 `with` 두 겹, `Path`·`hashlib`·`datetime`.
3. **주석과 설명**: 코드 셀 일곱 개 모두 첫 줄 주석이 없었습니다. 제목 셀과 「오늘 볼 그림」 첨부가 없고 코드 셀 앞뒤 설명 셀도 빠져 있었습니다. 결과 읽기가 출력의 실제 값을 인용하지 않았습니다.
4. **문장**: 영문 용어에 조사를 바로 붙여 시작한 문장이 열 곳(「HNSW와」·「`hnsw.iterative_scan`을」·「`strict_order`는」·「Before는」·「After는」 등), 70자 초과 두 문장, 정의 `<dl class="term">` 때문에 한 단락 여러 문장으로 센 곳 한 곳.
5. **그림**: Mermaid 0장, 삽화 0장, 설계표 없음. 옛 Excalidraw SVG 한 장(`03-필터-반복탐색.svg`)을 `{{svg:03-필터-반복탐색}}`으로 넣고 있었습니다.
6. **결론 범위와 미실행 내용**: b4에 「PostgreSQL 17에서 relaxed 결과를 정확히 다시 정렬하려면 공식 문서의 materialized CTE와 `distance + 0` 방식을 확인합니다」가 있었으나 노트북에서 실행하지 않은 내용입니다. b7의 「Recall@50, Precision@5, nDCG@5를 같은 실험 행에 남깁니다」도 이 절에서 재지 않은 지표입니다. 「지연 시간이 늘 수 있다」는 시간을 재지 않고 적은 문장입니다.
7. **자료가 앞 절과 이어지지 않음**: 개선 전은 8차원 합성 벡터 3012행만 썼고 교육용 문서 12개를 쓰지 않아 01·02절 결과와 대조할 수 없었습니다. 표 이름만 `ch12_core_filter`로 같았습니다.

## 3. 가장 큰 결정 — 합성 자료를 numpy 없이 만들기

`handoff.md` 「§02 → §03」이 적어 둔 두 갈래 가운데 **갈래 1(규칙으로 만든 벡터)** 을 골랐습니다.

- 질문 벡터를 `copy()` 한 뒤 숫자 한 개만 반복 번호에 따라 조금 키웁니다(`vector[position] = vector[position] + shift_base + shift_step * number`). 난수를 쓰지 않아 다시 실행해도 같은 값이고 `random`·`numpy`가 모두 필요 없습니다.
- 갈래 2(`INSERT ... SELECT` + `generate_series`)는 새 SQL 낱말이 늘고 값이 난수면 재현성을 따로 맞춰야 해서 쓰지 않았습니다.
- **채움 행을 질문마다 50개씩(모두 400개) 만듭니다.** 첫 질문 하나에서만 만들면 다른 질문에서는 채움 행이 문서보다 멀어져 나중 걸러 내기가 재현되지 않았습니다(탐색 실행 `/tmp/ch12-03/probe3.py`에서 확인). 질문마다 만들면 여덟 질문 모두 초기 후보가 채움 행으로 찹니다.
- 차원 수는 **256**을 그대로 씁니다(개선 전 8차원). 교육용 문서 12개를 같은 표에 넣어 01·02절 상위 세 개와 대조할 수 있습니다.
- 행 수는 3012개 → **412개**로 줄였습니다. 후보 목록 크기 기본값 40보다 충분히 크고 `INSERT` 412번이 0.3초 안에 끝납니다.
- 채움 행 수와 바꿀 숫자의 크기는 탐색 실행 뒤 정했습니다. 그 사실과 「흐름을 보여 주려고 정한 예」를 본문 b7에 적었습니다(규격 §3).

## 4. 실행 계획과 psycopg 준비된 문장 — 이 절의 함정 하나

- **질문 여덟 개 비교를 「정확 검색」 대 「색인 경로」로 바꿨습니다.** 처음에는 「순차 스캔 경로」 대 「색인 경로」로 잡았는데, 같은 필터 SQL을 `enable_seqscan` on과 off에서 섞어 실행하면 결과가 달라졌습니다. psycopg는 같은 SQL을 다섯 번 넘게 실행하면 준비된 문장으로 바꾸고 그때 만든 계획을 다시 쓰기 때문입니다(`prepare_threshold` 기본값 5, `/tmp/ch12-03/probe4.py`에서 `EXPLAIN`은 `Index Scan`인데 실제 실행은 순차 스캔 계획이 그대로 쓰여 3줄을 냈습니다).
- 그래서 필터 검색은 **처음부터 끝까지 `enable_seqscan` off 상태에서만** 실행하고, 견줄 정답은 01절 거리 함수로 **파이썬에서** 냅니다(`rank_in_category()`). 파이썬 쪽은 데이터베이스 계획과 무관하게 늘 같습니다. 이 사실을 b7에 한 문장으로 적었습니다.
- 412행 표에서도 필터 없는 검색의 계획 줄은 `Seq Scan on ch12_core_filter`였습니다. 02절 12행 표의 결론과 이어지는 사실이라 결과 읽기와 b3에 적었습니다.
- `ANALYZE`를 쓰지 않았습니다(개선 전은 표를 만든 뒤 불렀습니다). `enable_seqscan`을 off로 두면 색인 경로를 고르므로 필요 없고 새 낱말을 하나 덜 가르칩니다.

## 5. 반복 탐색 값을 질문 여덟 개로 재지 않은 까닭 (흔들리는 값)

- 탐색 실행을 색인을 다시 만들며 **다섯 번** 돌려 보니 `strict_order`의 받아 온 줄 수가 질문마다 **0~3으로 흔들렸습니다**(예: `C05` 3 → 2, `C07` 3 → 1, `C08` 3 → 0). `relaxed_order`도 세 번째 줄의 문서가 실행에 따라 달라졌습니다. pgvector HNSW 색인은 만들 때마다 구조가 조금 달라지고, 반복 탐색은 공식 문서대로 요청한 줄 수보다 적게 낼 수 있습니다.
- 그래서 **반복 탐색은 첫 질문 하나로만 확인**하고 질문 여덟 개 표에는 넣지 않았습니다. 그 사실을 b7에 「이번에 실행하지 않았습니다」로 적었습니다.
- 교재에 싣는 값은 같은 순서로 색인을 다섯 번 다시 만들어 모두 같았던 것만 골랐습니다(`/tmp/ch12-03/p6-1.txt`~`p6-5.txt` 동일). 첫 질문의 `off` 0줄, `strict_order`·`relaxed_order` 3줄(`LIB-004` 0.43 · `LIB-001` 0.56 · `LIB-003` 0.62), 질문 여덟 개 표와 질문 평균 여섯 줄이 그 값입니다.
- 거리는 01·02절과 같이 소수 둘째 자리까지만 출력하고 그림 라벨에는 문서 ID만 넣었습니다.

## 6. 파일 쓰기 결정 — 이 절도 파일을 쓰지 않음

- 개선 전 마지막 두 셀이 `runs/core-03-iterative-scan.json`을 덮어쓰고 `runs/core-history/`에 보존본을 남겼습니다. `Path`·`hashlib`·`datetime`·세미콜론·한 줄 복합문을 쓰고 이 절 주제(필터 순서와 반복 탐색)와 무관합니다.
- 읽는 쪽은 `textbook/qa/check_course_continuity.py` 187~196행 하나이고 **바이트만** 봅니다. 그래서 쓰지 않는 쪽을 골랐습니다(Ch 9 07·Ch 10 09·Ch 11 07·Ch 12 01·02절 선례).

| 확인 항목 | 값(작업 전 = 작업 뒤) |
|---|---|
| `runs/core-03-iterative-scan.json` | `4d9be88254b631d348b3572c8216ad57b6c2bd8166f7f58a46ac596f83e9e1d1` |
| `runs/core-history/before-4d9be88254b6-core-03-iterative-scan.json` | 같은 바이트 |
| `runs/` 36개 묶음 해시 | `a9c5d35a40a8acc0ac9455eae8682bc7cacadfc66682f1087c81f739abc3c8f6` |
| `runs/core-history/` 파일 수 | 12 |
| `advanced-queries.json`·`advanced-documents.json`·`core-*.json` | 건드리지 않았습니다 |
| `pyproject.toml` · `uv.lock` | `5b10531e0675a231…` · `f13e8c6f1880e7de…` |

- 노트북은 데이터베이스 표 `ch12_core_filter`를 만들고 남겨 둡니다(02절 표 `ch12_core_hnsw`는 건드리지 않습니다). 마지막 셀은 바꾼 설정 두 개(`hnsw.iterative_scan`·`enable_seqscan`)를 기본값으로 되돌리고 연결을 닫습니다.
- `%pip` 목록은 02절과 같은 세 개(`psycopg[binary]==3.3.5`·`python-dotenv==1.2.3`·`langchain-openai==1.6.1`)이고 모두 `pyproject.toml`에 이미 고정돼 있습니다. dev 그룹 `pip==26.2`가 `uv.lock`에 있고 그 `.venv`에서 `import pip`이 `26.2`로 되는 것을 확인했습니다(`check_course_continuity.py` 43행 조건).

## 7. 바꾼 것 (블록·노트북)

- **본문 10블록을 다시 썼습니다.** 정의 `<dl>`을 용어 표로 바꾸고 용어 다섯 개를 다시 썼습니다: **메타데이터 필터** · **나중 걸러 내기(post-filtering)** · **선택도(selectivity)** · **반복 탐색(iterative scan)** · **채움 행**. meta 「새 용어 5」와 시수(강의 1h·실습 3h)는 그대로 두었습니다.
- **영문 줄임말을 쓰지 않습니다.** 02절이 정한 규칙대로 「post-filtering」을 본문 용어로 쓰지 않고 「나중 걸러 내기(post-filtering)」로 한 번만 원어를 적었습니다. 절 제목의 「iterative scan」은 `chapter.json` 제목·파일 이름이라 그대로 두고 본문에서는 「반복 탐색(iterative scan)」으로 부릅니다.
- **실행하지 않은 내용을 뺐습니다**: materialized CTE와 `distance + 0`, Recall@50·Precision@5·nDCG@5, 「지연 시간이 늘 수 있다」는 단정. 대신 「검색 시간을 재지 않았습니다」와 「반복 탐색을 켠 채로 질문 여덟 개를 재지 않았습니다」를 b7에 적었습니다.
- **볼 줄 수 한도를 출력으로 보입니다**: `SHOW hnsw.max_scan_tuples` → `20000`. 설치판 설정 목록(`pg_settings`)으로도 `hnsw.iterative_scan` 값이 `off`·`relaxed_order`·`strict_order` 세 가지이고 `hnsw.ef_search` 기본값이 40, `hnsw.scan_mem_multiplier` 기본값이 1인 것을 확인했습니다.
- **노트북 흐름**(16개 소제목): 준비 5셀 → 2 접속·값·판 번호 → 3 문서·질문 벡터 → 4 01절 거리 함수 네 개 → 5 `find_category` → 6 채움 행 규칙과 파이썬 거리 대조 → 7 표·`INSERT` 412줄·범주별 행 수·색인 → 8 검색 SQL 두 가지와 `run_search`·`print_hits`·`find_scan_line` → 9 실행 1 필터 없는 검색 → 10 `set_seqscan` off와 계획 줄 → 11 `rank_in_category`로 정확 검색 상위 세 개 → 12 Ch 11 지표 함수 네 개와 `run_filtered_search`·`set_iterative_scan`·`pick_hits`·`score_one` → 13 기록 16줄·표·질문 평균 → **14 Before(반복 탐색 off, 0줄)** → **15 After(`strict_order`, 3줄)** → 16 값 바꿔 보기(`relaxed_order`) → 정리.
- **01·02절과 같은 코드로 다시 정의한 함수 여덟 개**: `dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`·`unique_doc_ids`·`find_gold_rank`·`recall_at`·`mean_score`. 02절과 같은 코드 셋: `run_search`·`print_hits`·`set_seqscan`. `find_scan_line`은 SQL과 값을 인자로 받는 판으로 바꿨습니다(이 절은 SQL이 두 가지).
- **03절이 새로 만든 함수 여섯 개**: `find_category`(6) · `make_filler_vectors`(7) · `rank_in_category`(9) · `run_filtered_search`(6) · `set_iterative_scan`(3) · `pick_hits`(8) · `score_one`(10). 괄호 안은 주석·빈 줄을 뺀 본문 줄 수이고 모두 10줄 이하입니다(규격 §2-2 L2, 직접 셈).
- **셀 크기**: 주석·빈 줄을 뺀 코드 줄 수가 셀마다 최대 **12줄**입니다(규격 §2-4 권장 3~12줄 안).
- **기록 한 줄의 칸**: `경로`·`질문`·`받아 온 줄 수`·`정답 자리`·`자리 1`·`자리 2`·`자리 3`. 02절 기록에 **`받아 온 줄 수`** 칸을 더한 모양입니다(이 절의 주제가 받아 온 줄 수이기 때문).

## 8. 그림

- 설계표 `03-figures.md`. Mermaid 4장 + 삽화 1장.
- `03-1-후보를-고른-뒤-조건-검사`(flowchart TB, 폭 251) · `03-2-표에-넣은-두-가지-행`(flowchart TB, 폭 405) · `03-3-두-경로의-질문-평균`(xychart-beta 꺾은선 두 개, 폭 700) · `03-4-설정-하나만-바꾼-뒤`(flowchart TB 칸 두 개, 폭 558). 모두 약 868 아래입니다.
- PNG 네 장을 직접 열어 확인했습니다. `03-4`는 칸을 넘는 화살표 때문에 `strict_order` 칸이 왼쪽, `off` 칸이 오른쪽으로 렌더돼 처음 쓴 「아래 칸만」 라벨이 맞지 않았습니다. 라벨을 「`strict_order` 칸만 정확 검색 상위 세 개와 같음」으로 고치고 alt·캡션·「도식 읽기」도 위치 말 없이 칸 제목으로 가리키게 바꿨습니다.
- **빨강은 `03-4`의 Before 결함 결과 한 곳뿐입니다**(받아 온 줄 수 0, paired 절이므로 규격 §5-3). 02절은 빨강 0장이었습니다.
- `03-3`은 `plotColorPalette: '#22c55e, #f59e0b'`로 초록 선 = 정확 검색, 주황 선 = 색인 경로입니다. 색 이름을 캡션·「도식 읽기」에 적었습니다(규격 §5-3, Ch 5 C-2).
- 삽화 `03-5-끈과-빈-쟁반`: **1차 job `d1fdbff2-70a9-4f3a-ac71-f9c8476ed4f8` 채택**, 2크레딧, 생성 전 잔액 2735. 저장 PNG(1100 × 614)를 채택 job 결과에서 같은 폭으로 줄인 그림과 픽셀 대조해 차이가 없었습니다(`ImageChops.difference` 범위 `None`, 규격 §5-4). 쟁반에 쌓인 책의 권수가 또렷하지 않아 alt·캡션·「그림 읽기」에 권수를 적지 않았습니다(`03-5-끈과-빈-쟁반.prompt.md` 상태 줄).
- 옛 도식 `figures/03-필터-반복탐색.svg`·`.excalidraw`·`.caption.md`는 지우지 않고 `qa/upgrade/before/figures/`에 사본을 두었습니다.

## 9. 앞 절·앞 챕터와 이어지게 바꾼 점

- 01절 자료(문서 12개·질문 8개)·차원 수 256·거리 함수·「거리는 소수 둘째 자리까지」 규칙을 그대로 이어 썼습니다. 정확 검색 상위 세 개 `LIB-004` 0.43 · `LIB-001` 0.56 · `LIB-003` 0.62가 01·02절 값과 같은 것을 본문 b3·b5·b6에서 짚었습니다.
- 02절에서 배운 `psycopg`·자리표시자 `%s`·`set_config()`·`EXPLAIN`·`enable_seqscan`·연산자 클래스 `vector_cosine_ops`를 같은 코드·같은 뜻으로 씁니다. 02절 관찰(작은 표에서는 계획기가 차례로 읽음, 시간은 재지 않음)을 b3와 9절 결과 읽기에서 인용하고 412행 표에서도 같았다는 사실을 더했습니다.
- Ch 4 03절 `WHERE`와 「값은 자리표시자로」를 b3에서 잇고, 조건 값도 `%s`로 넘깁니다.
- Ch 11 지표 함수 네 개를 같은 인자 모양으로 씁니다(중복을 뺀 문서 ID 목록을 받고 자르기는 함수 안에서). `evaluate.py`의 같은 이름 함수와 섞지 않았습니다(Ch 11 요약 §11-2).
- Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과 나란히 놓지 않는다는 문장은 01절 b7에 있어 되풀이하지 않았습니다. 대신 b7에 「채움 행이 섞여 있어 01·02절 재현율과 이 절 색인 경로 값을 같은 뜻으로 읽지 않는다」를 적었습니다.
- 비유는 02절 「서가와 끈」을 이어받아 「같은 끈이 어디까지 이어지는가」로 좁혀 씁니다. 빈 쟁반 = 받아 온 줄 수 0은 이 절에서 새로 정한 뜻이고 `.prompt.md`에 적었습니다.
- 04절 연결 문장은 개선 전 `_src`·노트북에서 Kiwi 형태소와 BM25를 쓰는 것을 확인하고 「형태소 분석기로 낱말을 가르고 낱말이 겹치는 정도로 순위를 냅니다」까지만 적었습니다.

## 10. 작업 환경 (교재 본문은 학생 기준 그대로)

- 02절과 같습니다. Docker가 없는 작업 VM에서 conda-forge PostgreSQL **17.11** + pgvector **0.8.1**을 `.cache/vm/pgenv`(데이터 `.cache/vm/pgdata`)에 두고 교재와 같은 접속 정보로 띄웠습니다. `qa/upgrade/pre_exec.sh`를 `run_section.sh`가 절 실행 직전에 `source` 합니다.
- 교재 준비물의 기준 버전 세 갈래: **필수 최소 pgvector 0.8.0**(반복 탐색 설정이 생긴 판) · 교재 출력 PostgreSQL 17.11과 pgvector 0.8.1 · 참고 자료로 적은 공식 문서 v0.8.6. 학생 기준은 실습 폴더 `README.md`의 `pgvector/pgvector:0.8.2-pg17` 이미지이고, 「Docker 이미지에서는 확장 판이 0.8.2로 나온다」와 「판 번호가 달라도 이 절에서 쓰는 기능은 같다」를 준비물과 b7에 한 문장씩 넣었습니다(02절과 같은 두 문장, 규격 §6).
- 임베딩 요청 9번(문서 1 + 질문 8), 0.01달러 아래. 답을 쓰는 모델은 부르지 않았습니다.
- 기기 루트 디스크 여유는 작업 중 약 500MB였습니다. 임시 파일은 `/tmp/ch12-03/`에 두었습니다.

## 11. 남은 것과 강사 확인 대상

- **절 meta 시수 합이 `chapter.json`과 맞지 않습니다.** 열두 절 meta의 합은 강의 12h·**실습 22h**이고 `chapter.json`은 「총 40h · 강의 12h · 실습 28h」입니다. 실습 6h가 비어 있고 개선 전부터 그랬습니다. 규격 §7-2에 따라 **고치지 않고 강사 확인 대상으로** 둡니다(01·02절 진단과 같은 항목).
- **강사 확인 대상(이 절)**: ① 합성 자료를 「채움 행 400개 + 교육용 문서 12개」로 바꾼 것(개선 전은 8차원 3012행), ② 질문 여덟 개 비교를 「정확 검색(파이썬) 대 색인 경로」로 잡은 것, ③ 반복 탐색을 첫 질문 하나로만 확인한 것(값이 실행마다 흔들림), ④ 「나중 걸러 내기」·「채움 행」·「선택도」 세 말의 한국어 표기, ⑤ 절 제목에 영문 「iterative scan」이 남는 것.
- **다시 실행하면 함께 고칠 것**: 없습니다. 이 절은 파일을 쓰지 않고 앞 절 기록도 읽지 않습니다.
- **정리 대상(삭제하지 않고 목록만, 삭제 승인 필요)**: 옛 도식 `figures/03-필터-반복탐색.svg`·`.excalidraw`·`.caption.md`, `qa/upgrade/gates-wip-03.json`, 기기 `/tmp/ch12-03/`, `.cache/vm/shot/ch12-03-crop-tray.png`·`ch12-03-b4.png`·`ch12-03-b6.png`(삽화·화면 검수용 사본, `.cache/`는 `.gitignore` 안).
- **챕터 마감 때 볼 것**: 절 meta 실습 시수 합, `chapter.json`의 `objectives` 둘째 줄(「메타데이터 필터의 영향을 실제 SQL로 확인」은 이 절과 맞습니다), 데이터베이스 표 `ch12_core_hnsw`·`ch12_core_filter`가 남는 것, 공용 `visual-results.json` 26행 유지.

## 검토 반영 (2026-09-19, 챕터 마감)

- **03-1(중) `03-4` 좌우 차례** — `.mmd`에서 회색 상자 `same`을 두 칸 아래 가운데로 모으고(`off_out --> same`·`strict_out --> same`) 다시 렌더했습니다. PNG를 직접 열어 **왼쪽 = 반복 탐색 off(Before) · 오른쪽 = strict_order(After)**임을 확인했고 viewBox 폭은 548로 868 안입니다. alt·「도식 읽기」에 왼쪽·오른쪽을 적었습니다.
- **03-2(하) 삽화 앞뒤 → 좌우** — b4 비유·`{{img:…}}` alt·「그림 읽기」의 「앞쪽/뒤쪽」을 그림대로 **「왼쪽/오른쪽」**으로 고쳤습니다.
- **03-3(하) b8 자리 표기** — 「자리 1에서 정확 검색 `0.75`에 색인 경로 `0.375`였고 색인 경로는 세 자리가 모두 같았습니다」로 고쳤습니다.
- **02-1과 같은 문장** — 이 절 b7의 Docker 0.8.2 문장도 같은 모양으로 고쳤습니다.
- **C-7(하) 실습 시수** — 해소(01절 항목 참조).
- **결정 요청** — 합성 자료 방식·두 경로 비교 잡기·반복 탐색 첫 질문 하나·용어 세 개·절 제목 영문은 **모두 유지**했습니다.
- 노트북 재실행 없음: `code_sha256` `56595a043b3d0d0a`·`outputs_sha256` `76e5c409969eeabc`·`executed_at` 2026-09-18T16:12:36Z 전후 같음.
