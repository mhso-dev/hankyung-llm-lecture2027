# Ch 12 02절 「pgvector와 HNSW」 품질 개선 기록

규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`, 절 사이 인계 `handoff.md`.
작업 2026-09-18. 앞 내용은 `textbook/qa/upgrade-course-summary.md`(Part 1·2), Ch 09·Ch 10·Ch 11 `qa/upgrade/chapter-summary.md`, 이 챕터 01절 완료본과 `handoff.md` 「§01 → §02」를 읽고 맞췄습니다.

## 1. 게이트 전후

| 게이트 | 수정 전 | 수정 뒤 |
|---|---|---|
| G1 문법 사다리 | 6 | **0** |
| G2 셀 모양 | 6 | **0** |
| G3 주석 | 7 | **0** |
| G4 실제 모델 | 0 | **0** |
| G5 노트북 설명 | 12 | **0** |
| G6 문장 | 13 | **0** |
| G7 그림 | 3 | **0** |
| 합계 | **47** | **0 (PASS)** |

- 기록 파일: 수정 전 `gates-before.json`(챕터 첫 절 작업에서 12절 전체를 한 번 기록), 수정 뒤 `gates-after-02.json`·`gates-wip-02.json`.
- 코드 셀 8개 → **39개**(준비 5), 검사 문장 82개 → **350개**.
- 새 커널 실행: `PASS 02-pgvector와-HNSW.ipynb: 39 cells`. 같은 코드로 두 번 실행해 `code_sha256` `17978388a9a5efec…`와 `outputs_sha256` `9947bfc44d4a1803…`가 같았고 셀별 출력 글자도 모두 같았습니다. 교재 출력은 마지막 실행 **2026-09-18T15:19:32Z**입니다.
- `verify.py --chapter`: `PASS 12 sections / 136 code cells (max 25 lines)`(01절 뒤 105셀 → 136셀, `max 25`는 아직 개선 전인 12절 셀).
- `visual.cjs`: 1280px·390px 모두 PASS. 공용 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`은 26줄을 유지하고 02절 두 줄만 새 결과로 바꿨습니다(`/tmp` 사본에 `ONLY` 필터와 병합 저장을 넣어 실행, 공용 도구 원본은 고치지 않았습니다).
- 실습 폴더 테스트: 작업 전후 모두 **4 passed**.

## 2. 수정 전 주요 문제

1. **문법 사다리**: 내포식 세 곳(`[f"{d['title']} {d['text']}" for d in docs]`·`[(d["doc_id"], d["category"], v) for d, v in zip(docs, vectors)]`·`[row[0] for row in result]`), 제너레이터 식 한 곳(`next((folder for folder in ... ), None)`), 조건 표현식 두 곳(`"off" if use_index else "on"`), 한 글자 변수 `d`·`v`, 세미콜론과 한 줄 복합문(마지막 기록 셀), 15줄 넘는 셀 하나.
2. **가르치지 않은 도구**: `numpy`(`np.array(..., dtype=np.float32)`)와 `pgvector` 파이썬 패키지의 `register_vector`. `numpy`는 Part 1~3 기본 경로에서 가르친 적이 없습니다. f-string 안 계산(`{int(ef_search)}`)과 `%` 문자열 서식으로 SQL을 만든 자리도 있었습니다.
3. **주석과 설명**: 코드 셀 일곱 개에 첫 줄 주석이 없었습니다. 제목 셀과 「오늘 볼 그림」 첨부가 없고, 코드 셀 앞뒤 설명 셀도 빠져 있었습니다. 결과 읽기가 출력의 실제 값을 인용하지 않았습니다.
4. **문장**: 영문 용어에 조사를 바로 붙여 시작한 문장이 아홉 곳(「pgvector의」·「`ef_search`는」·「HNSW는」·「vector는」 등), 70자 초과 세 문장, 한 단락 여섯 문장이 한 곳 있었습니다. 정의를 `<dl class="term">`으로 써서 G6가 한 단락 여러 문장으로 셌습니다.
5. **그림**: Mermaid 0장, 삽화 0장, 설계표 없음. 옛 Excalidraw SVG 한 장(`02-HNSW.svg`)을 `{{svg:02-HNSW}}`로 넣고 있었습니다.
6. **결론 범위**: 「공식 최신 v0.8.6의 2,000/4,000차원 설명과 실습 컨테이너의 0.8.2에서 관찰한 결과가 일치한 사례」처럼 실행하지 않은 판까지 묶어 적은 문장이 있었습니다. 「Recall@50·nDCG@5를 함께 비교합니다」는 이 절에서 재지 않은 지표입니다.
7. **인덱스 선택 설명 없음**: 개선 전 노트북은 `enable_seqscan`·`enable_indexscan`을 강제로 바꿔 두 경로를 만들었을 뿐이고, 계획기가 무엇을 골랐는지는 보여 주지 않았습니다. 본문은 「`EXPLAIN`으로 실행 계획도 확인합니다」라고 적었지만 노트북에 `EXPLAIN`이 없었습니다.

## 3. 데이터·차원 수 결정 — 01절을 그대로 이어 씀

- `core-documents.json`(12개)·`core-queries.json`(8개)을 그대로 씁니다. 01절 정확 검색 순위와 대조하려면 같은 문서·같은 질문·같은 차원 수여야 합니다(`01-diagnosis.md` §3).
- `dimensions=256`을 유지했습니다. `check_course_continuity.py` 219행과 실습 폴더 `tests/test_continuity.py`가 12절 기록의 `settings.dimensions == 256`을 봅니다.
- Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과 나란히 놓지 않는다는 문장은 01절 b7에 있으므로 되풀이하지 않고, b7에 「이 절의 자료는 01절과 같은 교육용 자료」로만 적었습니다.
- Ch 10 08절 색인(숫자 1536개)과의 비교 금지 문장도 01절 b7에 있어 되풀이하지 않았습니다.

## 4. 파일 쓰기 결정 — 이 절도 파일을 쓰지 않음

- 개선 전 마지막 두 셀이 `runs/core-02-hnsw.json`을 덮어쓰고 `runs/core-history/`에 보존본을 남겼습니다. `Path`·`hashlib`·`datetime`·세미콜론·한 줄 복합문을 쓰고 이 절 주제(거리 연산자·색인·실행 계획)와 무관합니다.
- 읽는 쪽은 `textbook/qa/check_course_continuity.py` 187~196행 하나이고 **바이트만** 봅니다. 정본이 `before-manifest.json` 해시와 다르면 `runs/core-history/before-*-core-02-hnsw.json`에 원본 바이트가 남아 있어야 합니다.
- 그래서 파일을 쓰지 않는 쪽을 골랐습니다(Ch 9 07·Ch 10 09·Ch 11 07·Ch 12 01절 선례). 작업 전후 확인값은 그대로입니다.

| 확인 항목 | 값(작업 전 = 작업 뒤) |
|---|---|
| `runs/core-02-hnsw.json` | `e007a959899ec0ea866ca7d03597fec13bbd3c84bf677c9048251658f1519175` |
| `runs/` 36개 묶음 해시 | `a9c5d35a40a8acc0ac9455eae8682bc7cacadfc66682f1087c81f739abc3c8f6` |
| `runs/core-history/` 파일 수 | 12 |
| `advanced-queries.json`·`advanced-documents.json` | 건드리지 않았습니다 |

- 노트북은 데이터베이스 표 `ch12_core_hnsw`를 만들고 남겨 둡니다. 차원 한도를 보려고 만든 `ch12_dim_vector`·`ch12_dim_halfvec`은 마지막 셀에서 지웁니다. 실습 폴더 `pyproject.toml`·`uv.lock`은 고치지 않았습니다.

## 5. 작업 환경 — Docker 없이 pgvector 띄우기

- 교재 본문과 노트북은 **학생 기준(Docker 데이터베이스)** 을 그대로 씁니다. 실습 폴더 `README.md`의 `pgvector/pgvector:0.8.2-pg17` 이미지와 접속 글 `postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab`입니다.
- 작업 VM에는 Docker가 없어 conda-forge PostgreSQL + pgvector를 `$ROOT/.cache/vm/pgenv`(데이터 `.cache/vm/pgdata`, 로그 `/tmp/pg-ch12.log`)에 두고 같은 접속 글로 띄웠습니다. 준비 스크립트는 `qa/upgrade/pre_exec.sh`이고 `run_section.sh` 24행이 절 실행 직전에 `source` 합니다. 기기 셸은 호출이 끝나면 서버도 꺼지므로 노트북 실행은 `run_section.sh` 한 호출 안에서 끝냈습니다.
- **판 번호 차이**: 작업 VM은 **PostgreSQL 17.11 · pgvector 0.8.1**입니다(`SELECT current_setting('server_version')`·`SELECT extversion …`로 확인). 개선 전 노트북 출력의 `실제 pgvector 확장 버전: 0.8.2`는 macOS Docker 값이었고, 새 출력은 `0.8.1`입니다. 본문·노트북의 인용을 모두 새 출력으로 고쳤고, 준비물과 b7 주의 메모에 「Docker 이미지에서는 확장 판이 0.8.2로 나온다」와 「판 번호가 달라도 이 절에서 쓰는 기능은 같다」를 한 문장씩 적었습니다(규격 §6).
- 기준 버전은 준비물에 세 갈래로 적었습니다: 필수 최소 pgvector **0.7.0**(자료형 `halfvec`이 생긴 판), 교재 출력 **PostgreSQL 17.11 · pgvector 0.8.1**, 참고 자료로 적은 공식 문서 **v0.8.6**.
- 디스크: 작업 중 기기 루트 여유가 약 500MB였습니다(9.6G 공유). 새로 설치한 것은 없고 `$ROOT/.cache/vm/venv-ch12-retrieval-tuning`을 그대로 썼습니다. 임시 파일은 `/tmp/ch12-02/`에 두었습니다.

## 6. 바꾼 것

- **노트북을 다시 씀**(`qa/upgrade/author_02.py`, experiment 형식 유지). 준비 5셀(설치 → import → 키 확인 → 후보 경로 → 자료 읽기) 뒤에 13개 소제목으로 나눴습니다.
- **numpy·pgvector 파이썬 패키지를 빼고** 벡터를 `str(목록)`으로 바꿔 `INSERT`와 `<=>`에 값으로 넘깁니다. pgvector가 읽는 글 모양(`[0.1,0.2]`)과 같아 그대로 동작합니다. 설치 목록은 psycopg·python-dotenv·langchain-openai 세 개입니다.
- **`Decimal`을 없앰**: 개선 전 `round((embedding <=> %s)::numeric, 4)`는 `Decimal('0.4324')`를 출력했습니다. SQL은 거리를 그대로 받고 파이썬 `round(값, 2)`로 출력해 01절과 모양을 맞췄습니다(handoff 결정 항목).
- **`SET` 대신 `set_config()`**: `SET` 문장에는 자리표시자를 쓸 수 없어 개선 전은 `%` 서식과 f-string으로 SQL을 만들었습니다. Ch 4 03절이 가르친 「값은 자리표시자로 넘긴다」를 지키려고 `SELECT set_config('이름', %s, false)`로 바꿨습니다. 표 이름과 자료형 이름은 값이 아니라 문장의 일부라 넘길 수 없다는 사실을 주석과 결과 읽기에 적었습니다.
- **「언제 색인을 타는가」를 실행으로 보임**: `find_scan_line()`이 `EXPLAIN` 출력에서 읽기 방법이 적힌 줄만 골라 옵니다. 실행 1(색인 없음)·실행 2(색인 있음)·실행 3(`enable_seqscan`만 off) 세 번을 같은 SQL로 돌려 계획 줄이 `Seq Scan` → `Seq Scan` → `Index Scan`으로 바뀌는 것을 보였습니다. **색인을 만든 뒤에도 계획기가 순차 스캔을 골랐다**가 이 절의 결론입니다.
- **01절 함수 여덟 개를 같은 코드로 이어 씀**: `dot_product`·`vector_length`·`cosine_similarity`(Ch 9 03절)·`cosine_distance`(01절)·`unique_doc_ids`·`find_gold_rank`(Ch 11 01절)·`recall_at`·`mean_score`(Ch 11 02절). 파이썬으로 낸 코사인 거리 `0.56`과 pgvector `<=>`가 낸 `0.56`을 대조하고, 질문 여덟 개를 두 경로로 재어 정답 자리와 질문 평균 재현율이 01절과 같음을 보였습니다.
- **미교육 문법을 처음 쓰는 자리에서 풂**: `psycopg`(Ch 4 03절 `sqlite3`와 이어 씀), 자리표시자 `%s`(Ch 4 03절 `?`와의 차이), SQL `LIMIT`·`count(*)`·`CREATE EXTENSION`·`CREATE INDEX … USING hnsw`·`EXPLAIN`·`set_config`·`SHOW`, `try/except psycopg.Error as error`와 `error.diag.message_primary`.
- **본문 10블록을 다시 씀**: 정의 `<dl>`을 용어 표로 바꾸고 용어 여덟 개(pgvector·HNSW·거리 연산자 `<=>`·연산자 클래스·실행 계획·순차 스캔·`ef_search`·`halfvec`)를 다시 썼습니다. meta 「새 용어 6」 → 「새 용어 8」로 고쳤고 **시수(강의 1h·실습 3h)는 그대로 두었습니다.**
- **그림**: 설계표 `02-figures.md` → Mermaid 4장 + 삽화 1장. 옛 `{{svg:02-HNSW}}`를 `{{mermaid:}}`로 바꿨고 옛 SVG·Excalidraw는 지우지 않고 `qa/upgrade/before/figures/`에 사본을 두었습니다.
- **빼거나 고친 결론**: 「공식 v0.8.6 설명과 0.8.2 관찰이 일치한 사례」는 실행한 판(0.8.1)의 관찰로 한정했습니다. 「Recall@50·nDCG@5를 함께 비교합니다」는 이 절에서 재지 않은 지표라 「재현율과 걸린 시간을 함께 재는 일은 이번에 실행하지 않았습니다」로 바꿨습니다. 검색 시간을 재지 않았다는 사실을 b6·b7·복습 4번에 적었습니다.

## 7. 검사와 대조

- 게이트 G1~G7 **0건**(`gates-after-02.json`), 새 커널 PASS, `verify.py --chapter` PASS, `visual.cjs` 1280·390 PASS, 실습 폴더 테스트 4 passed.
- 빌드 결과 `02-pgvector와-HNSW.html`에 `{{` 잔존 0건, `<figure class="mmd">` 4개, `<figure class="illustration">` 1개.
- Mermaid PNG 네 장을 직접 열어 칸 배치와 색을 확인했습니다. `02-1`과 `02-4`는 두 칸이 **왼쪽·오른쪽**으로 렌더되어 「도식 읽기」의 방향 말과 맞습니다.
- 그림 라벨의 숫자를 노트북 출력과 대조했습니다(`256`·`12`·`004`·`001`·`003`·`2001`·`2000`은 출력에, `01`은 본문에). 거리 값과 실행 계획의 비용·행 수 어림은 라벨에 넣지 않았습니다(`02-figures.md`).
- 삽화는 저장 PNG를 채택 job 결과와 픽셀 대조했습니다(`ImageChops.difference` 범위 `None`), 1차 탈락본과는 다름을 확인했습니다(규격 §5-4).
- 산출 파일: 이 절은 파일을 쓰지 않습니다(§4 표).
- **검사 스크립트를 실제로 돌렸습니다**(멈추는 자리가 01절과 같음, 전체 마감 몫): `textbook/part3/qa/check_delivery.py` 끝까지 통과 · `textbook/part3/qa/check_continuity.py` 154행 `Stale archive: part2-practice.zip/…` · `textbook/qa/check_course_continuity.py` 212행 `Stale archive: part1-practice.zip/…`. 뒤 스크립트는 **43행(`%pip` 셀마다 `uv.lock`의 `pip == '26.2'`와 설치 목록 판 대조)과 187~196행(`runs/` 바이트 대조)을 모두 지나** 212행에서 멈춥니다. `%pip` 목록을 세 개로 줄였고 `uv.lock`에 `psycopg 3.3.5`·`python-dotenv 1.2.3`·`langchain-openai 1.6.1`·`pip 26.2`·`ipykernel 7.3.0`이 모두 있어 실습 폴더 `pyproject.toml`·`uv.lock`을 고치지 않았습니다.

## 8. 탐색 실행과 흔들리지 않은 값

- 탐색 실행은 `/tmp/ch12-02/probe1.py`~`probe4.py`(2026-09-18)입니다. `register_vector` 없이 파이썬 목록과 글 가운데 무엇이 `INSERT`·`<=>`에 통하는지, `EXPLAIN` 계획이 색인 뒤에 어떻게 나오는지, 질문 여덟 개의 두 경로 결과가 같은지를 먼저 확인했습니다.
- `enable_seqscan`을 바꾼 것과 `ef_search` 값 4·40은 **탐색 실행 뒤 정한 값이 아니라 개선 전 노트북이 쓰던 값**을 그대로 이어 쓴 것입니다. 개선 전은 두 값을 강제로 바꿔 두 경로를 만들었고, 이 절은 계획기 기본 계획을 먼저 보인 뒤 같은 설정을 씁니다.
- 두 번의 새 커널 실행에서 `outputs_sha256`이 같았습니다. 거리 값은 01절 규칙대로 소수 둘째 자리까지만 출력해 흔들리는 자리를 잘라 냈습니다.
- 실행 계획 줄의 괄호 안 값(`cost=0.00..19.75 rows=650`, `cost=0.00..2.18 rows=12`, `cost=12.09..20.27 rows=12`)은 두 실행에서 같았지만 표의 통계와 실행 환경에 달린 값이라 그림 라벨에 넣지 않았고, 결과 읽기에서도 「실행 환경에 따라 달라집니다」로 적었습니다.

## 9. 강사 확인 대상

- **절 meta 시수 합이 `chapter.json`과 맞지 않습니다.** 열두 절 meta의 합은 강의 12h·**실습 22h**이고 `chapter.json`은 「총 40h · 강의 12h · 실습 28h」입니다. 실습 6h가 비어 있습니다. 개선 전부터 그랬고 이 절에서 고치지 않았습니다(규격 §7-2는 절 meta 합을 챕터 시수와 같게 두라고 합니다). 03절 이후 절을 고칠 때 배분을 함께 정해야 합니다.
- **02절 meta를 「강의 1h · 실습 3h」로 그대로 둔 것**: 코드 셀이 8개에서 39개로 늘었습니다. 강의 시간에는 2~4절과 7~9절만 읽고 나머지는 실습으로 돌리도록 준비물의 「강의와 실습 범위」에 적었습니다.
- **`ef_search` 4와 40만 본 것**: 개선 전 값을 이어 썼습니다. 값을 더 넓히거나 큰 말뭉치로 재는 일은 이 절 범위 밖으로 두었습니다.
- **`halfvec` 2001차원 실험을 남긴 것**: 이 챕터가 숫자 256개를 쓰는 까닭을 실행으로 보이려고 유지했습니다. 자료형 `halfvec`은 이 절에서 검색에 쓰지 않습니다.
- **삽화 `02-5`가 프롬프트와 다른 점**: 그림의 책이 열세 권이고 「앞으로 나온 정도」의 차이가 보이지 않습니다. 본문 비유·alt·캡션·「그림 읽기」에서 책 수를 빼고 읽히는 두 관계만 설명했습니다(`figures/02-5-서가와-끈.prompt.md` 상태 줄).
- **작업 VM 판 번호(0.8.1)로 교재 출력을 만든 것**: 학생 Docker 이미지는 0.8.2입니다. 준비물과 b7에 한 문장씩 적었습니다.

## 10. 남은 것

- **정리 대상**(삭제하지 않고 목록만, 삭제 승인 필요): 옛 도식 `figures/02-HNSW.svg`·`.excalidraw`·`.caption.md`(사본은 `qa/upgrade/before/figures/`), `qa/upgrade/gates-wip-02.json`, 기기 `/tmp/ch12-02/`, `.cache/vm/shot/ch12-02-*.png`.
- 03절이 이어받을 것은 `handoff.md` 「§02 → §03」에 적었습니다.
- 챕터 마감에서 볼 것: 절 meta 시수 합(§9), `textbook/part3/_build_index.py`의 ch12 절 수 칸(실습 절을 붙일 때), `textbook/downloads/part3-practice.zip` 재생성.

## 검토 반영 (2026-09-19, 챕터 마감)

- **02-1(중) Docker 판 번호** — b7을 「실습 폴더 안내는 `pgvector/pgvector:0.8.2-pg17` 이미지를 씁니다. 그 이미지에서는 확장 판이 0.8.2입니다. **이번 교재 출력은 그 환경에서 만들지 않았습니다.**」로 갈라 적고, **필수 최소 판 0.7.0**을 b7에도 넣었습니다(준비물과 갈래 셋이 같아짐).
- **02-2(하) SQL 예시** — `ORDER BY embedding <=> %s LIMIT 3` → `LIMIT %s`로 고치고 「받아 올 줄 수도 값으로 넘깁니다」를 붙였습니다(b3의 「값은 자리표시자로」와 맞음).
- **02-3(하) 다음 절 말** — b8·노트북 정리를 03절이 정한 「받아 올 줄 수보다 적어질 수 있습니다」로 맞췄습니다.
- **C-6(하) 캡션 파일** — `02-2.caption.md`를 「표의 벡터 칸에 넣고」로, `02-4.caption.md`를 「vector 칸에는 2001차원 …」으로 본문 캡션과 같게 했습니다.
- **C-7(하) 실습 시수** — 해소(01절 항목 참조).
- **결정 요청** — 판 번호 문장만 02-1대로 고치고 나머지(02절 meta 1h·3h, `ef_search` 4·40, `halfvec` 2001, 삽화 `02-5`, 작업 VM 0.8.1로 교재 출력)는 **유지**했습니다.
- 노트북 재실행 없음: `code_sha256` `17978388a9a5efec`·`outputs_sha256` `9947bfc44d4a1803`·`executed_at` 2026-09-18T15:19:32Z 전후 같음.

## §2-7 챕터 마감 (2026-09-21, 작업자 B)

- 준비물 「강의와 실습 범위」의 절 번호를 소절 번호에 맞춤 — 「2~4절과 7~9절」 → 「2~4절과 9~11절」, 「10~13절은 함께 실행」 → 「7·8절과 12~14절은 함께 실행」(A 인계 8번, 리팩터 전부터 있던 어긋남). 마크다운 한 셀만 고치고 다시 실행하지 않음.
