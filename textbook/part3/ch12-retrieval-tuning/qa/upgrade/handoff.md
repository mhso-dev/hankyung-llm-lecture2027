# Ch 12 검색 품질과 튜닝 — 절 사이 인계

절 작업자가 다음 절 작업자에게 넘기는 기록입니다. 앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1·Part 2 절), 같은 Part 앞 챕터 요약 `textbook/part3/ch09-rag-first-run/qa/upgrade/chapter-summary.md`·`textbook/part3/ch10-document-processing/qa/upgrade/chapter-summary.md`·`textbook/part3/ch11-evaluation/qa/upgrade/chapter-summary.md`(§11 Ch 12 인계 여섯 가지). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`.

## §01 → §02

(01절 품질 개선 2026-09-18. 결과는 `01-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 42 = G1 9·G2 7·G3 6·G4 0·G5 9·G6 8·G7 3), 코드 셀 31(준비 5), 검사 문장 291, **임베딩 요청 9번**(문서 1 + 질문 8, 0.01달러 아래), 답을 쓰는 모델 0번. 같은 코드로 새 커널 두 번 실행해 `code_sha256` `727b3bdf75a8c253…`·`outputs_sha256` `ef039ce7b877e036…`가 같았고 교재 출력은 마지막 실행 2026-09-18T14:19:30Z. 챕터 첫 절이라 `gates-before.json`은 12절 전체 수정 전 기록(G1 131·G2 66·G3 79·G4 0·G5 108·G6 137·G7 36 = 557, 통과 0/12). Mermaid 4장·삽화 1장(2차 job `54736b6b-6faa-421c-b501-5faa652175b2` 채택, 1차 `5dc38f62-…` 탈락, 4크레딧, 생성 뒤 잔액 2764.5))

### 빌드 도구 — 고칠 것이 없습니다 (먼저 읽을 것)

- 이 챕터는 **`chapter.json`이 있고** `_build.py`가 공용 `textbook/_template/builder.py`의 `build_chapter()`를 그대로 부릅니다. Ch 8~10처럼 `_build.py`에 치환을 더할 일이 없습니다.
- 그 빌더가 이미 지원하는 토큰(`_src`에 이대로 씁니다)
  - `{{notebook:slug}}`(experiment) 또는 `{{notebook:slug|example}}`·`{{notebook:slug|failure}}`(paired). **`chapter.json`에서 03절만 `paired`이고 나머지 열한 절은 `experiment`입니다.** 노트북 메타데이터 `lesson_format`이 `chapter.json`과 다르면 빌드가 멈춥니다.
  - `{{mermaid:이름|alt|캡션}}` — `figures/이름.svg`를 `<figure class="mmd">`로 넣고 캡션을 붙입니다. `_src`에서 `<figure>`로 감싸지 않습니다. alt·캡션에 `|`·`}` 금지.
  - `{{img:이름|alt|캡션}}` — 삽화 PNG를 폭 1100px JPEG `<figure class="illustration">`로. 바로 아래에 「그림 읽기」 단락.
  - 옛 `{{svg:이름}}`도 그대로 동작합니다. **02~12 개선 전 `_src`는 아직 `{{svg:0N-…}}`을 씁니다** → 개선할 때 `{{mermaid:}}`로 바꾸고 옛 SVG·Excalidraw는 지우지 않습니다(`qa/upgrade/before/figures/`에 사본).
- **verify는 `run_section.sh`가 함께 돕니다**(`chapter.json`이 있어서). 01 뒤 기준 `PASS 12 sections / 105 code cells (max 25 lines)`. `max 25`는 아직 개선 전인 12절 셀이라 절을 고칠수록 내려갑니다.
- **빌드는 12절 HTML을 모두 다시 씁니다.** 01절 작업에서 13개 파일이 새로 쓰였고 2026-09-09 `before-manifest.json` 해시와 달라졌습니다. 차이는 2026-09-14에 고친 `_src`·노트북 내용이고(빌드가 그때 안 돌았음) 이번 작업이 만든 것이 아닙니다. 두 검사 스크립트가 해시를 보는 항목은 `labs/**/runs/**`뿐이라 걸리지 않습니다(01절에서 두 스크립트를 실제로 돌려 확인).
- `visual.cjs`는 `playwright` 패키지를 부르므로 `/tmp` 사본으로 돌립니다. 01에서 쓴 방법: `require('playwright')` → `require('/tmp/pw/node_modules/playwright-core')`, `chromium.launch({headless:true})` → `executablePath:'/tmp/pptr-cache/chrome/linux_arm-153.0.8010.36/chrome-linux-arm64/chrome'`·`args:['--no-sandbox']`, `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`. 01절 1280px·390px **2건 PASS**.
- **목차 페이지**: 빌드한 `index.html`은 `chapter.json`의 `title`·`hours`·`objectives`·`sections`에서 만들어집니다. `_src/index.html`은 이 챕터에 없습니다.

### 02절 pgvector 실행 방법 (작업 환경)

- 작업 VM에 Docker가 없어 conda-forge PostgreSQL + pgvector를 사용자 디스크에 두었습니다. 준비 스크립트는 **`qa/upgrade/pre_exec.sh`**이고 `run_section.sh`가 절 실행 직전에 `source` 합니다(`run_section.sh` 24행). 따로 부를 일은 없습니다.
- 서버 자리: 실행 파일 `.cache/vm/pgenv/bin/`, 데이터 `.cache/vm/pgdata`, 로그 `/tmp/pg-ch12.log`. 접속 정보는 **교재와 같은** `postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab`입니다.
- **기기 셸은 호출이 끝나면 서버도 꺼집니다.** 그래서 한 번의 `device_bash` 호출 안에서 서버를 켜고 노트북을 실행해야 합니다. `run_section.sh`를 한 호출로 돌리면 그렇게 됩니다. 직접 확인할 때는 `. textbook/part3/ch12-retrieval-tuning/qa/upgrade/pre_exec.sh` 뒤에 같은 호출에서 `psql`을 씁니다.
- **버전 차이(2026-09-18 확인)**: 작업 VM은 **PostgreSQL 17.11 · pgvector 0.8.1**입니다. 개선 전 02절 노트북 출력은 `실제 pgvector 확장 버전: 0.8.2`(macOS Docker)입니다. **02절을 다시 실행하면 이 값이 `0.8.1`로 바뀌므로 본문·그림 라벨의 인용을 새 출력으로 고쳐야 합니다.** 교재 본문의 학생 기준은 Docker 그대로 쓰고, 작업 환경 차이는 `02-diagnosis.md`에 적으세요(AGENT-BRIEF·PLAYBOOK §0).
- 실습 폴더 잠금에 `pgvector==0.4.2`·`psycopg[binary]==3.3.5`가 이미 있습니다(개선 전 02 노트북 `%pip` 목록과 같음).
- 개선 전 02절이 확인한 것: 인덱스 없이 `ORDER BY embedding <=> query LIMIT 3`(정확 검색)과 HNSW 인덱스 경로가 **같은 상위 3개**를 냈고, `hnsw.ef_search`를 4와 40으로 바꿔도 순위가 같았으며, `vector(2001)`은 HNSW 색인을 만들 수 없고(`column cannot have more than 2000 dimensions for hnsw index`) `halfvec(2001)`은 만들 수 있었습니다.

### 데이터 — 두 벌이 있고 01~06절은 core 벌입니다

| 파일 | 내용 | 쓰는 절 |
|---|---|---|
| `data/core-documents.json` | 교육용 문서 12개(`doc_id`·`category`·`title`·`text`, `LIB-001`~`ACC-004`, 글자 수 합 712) | 01·02·04·05·06 |
| `data/core-queries.json` | 질문 8개(`qid`·`question`·**`gold_doc_id`**(글 하나)·`kind`, `C01`~`C08`, 글자 수 합 155) | 01·02·04·05·06 |
| `data/advanced-documents.json` | 부모 문서 6건(`E01`·`E02`·`H01`·`H02`·`M01`·`M02`)과 문서 청크 175개(`chunk_id`·`parent_id`·`page`·`title`·`text`) | 07~12 |
| `data/advanced-queries.json` | 질문 30개 | 07~12 |

- **`advanced-queries.json`은 Ch 11 평가셋 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`과 파싱 결과가 완전히 같습니다**(30줄, 칸 7개, 개발 15 · 시험 15). `textbook/part3/qa/check_continuity.py` 44~46행·`textbook/qa/check_course_continuity.py` 78~80행·실습 폴더 `tests/test_continuity.py`가 검사합니다 → **한 글자도 고치지 마세요.**
- `advanced-documents.json`도 계약 파일입니다: `chunk_id`가 `부모ID-P쪽번호-C번호` 모양이어야 하고(`tests/test_continuity.py` 정규식), 12절 기록의 모든 `top_results` 항목이 이 파일의 `chunk_id`·`parent_id`·`page`와 맞아야 합니다(`check_course_continuity.py` 140~146행).
- **01절은 core 벌을 그대로 썼습니다.** 까닭은 `01-diagnosis.md` §3(02절 대조가 같은 12개 벡터를 전제 / 문서 12개라 「모두 재었다」를 셀 수 있음 / Ch 11 값과 나란히 놓지 않는다는 규칙). 02~06절도 core 벌을 이어 쓰면 01절 값과 견줄 수 있습니다.
- **Ch 11 값과 나란히 놓지 않습니다.** Ch 11 개발 15문항 자리 5 값은 `0.867`·`0.173`·`0.751`이고 말뭉치·질문 묶음·자르는 자리가 모두 다릅니다. 01 b7에 그 문장이 있으니 되풀이하지 말고 07절부터 평가셋을 쓸 때 이어 쓰세요.
- **개발 15문항 / 시험 15문항 약속**(Ch 11 요약 §11-1): 01~06절은 평가셋을 읽지 않아 시험 분할을 보지 않습니다. 평가셋을 처음 쓰는 절(07절)에서 「개발 15문항으로 고르고 시험 15문항은 마지막 한 번」을 인용하세요.

### 차원 수 — 이 챕터는 256으로 고정합니다

- 01절 `OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)`. 02절 `vector(256)` 표, 05·06·12절도 256입니다.
- **계약**: `check_course_continuity.py` 219행과 `tests/test_continuity.py`가 12절 기록의 `settings.dimensions == 256`을 봅니다.
- Ch 10 07절은 「색인에 넣을 벡터는 기본 설정(숫자 1536개)」로 정했습니다. 값이 달라 **두 색인의 점수를 나란히 놓지 않는다**는 문장을 01 b7에 적었습니다. 02~12절에서 되풀이하지 마세요.

### 용어 (01에서 정한 것, 02~12도 같게)

- **Ch 9·Ch 10·Ch 11 뜻 그대로 이어 씁니다**: 문서 청크(한정어 없는 「청크」 금지), 색인, 벡터스토어, 검색 점수, 고유 문서, 후보 목록, 자르는 자리, 재현율, 질문 평균, 정답 문서 ID, 겹침, 실행 설정, 실행 기록 한 줄. **「조각」은 Ch 5 토큰 뜻 전용**입니다.
- **01이 새로 정한 말 다섯 개**(본문 b4 용어 표): **L2 거리(L2 distance)**, **코사인 거리(cosine distance)**, **정확 검색(exact search)**, **근사 검색(approximate search)**, **단위 길이 벡터(unit length vector)**.
- **「자」**는 거리 재는 방법을 가리키는 말로 씁니다(코사인 자·L2 자). 노트북 기록 칸 이름도 `자`입니다.
- **「기준선」**은 Ch 11 §2 뜻(견줄 출발점이 되는 한 벌의 설정)을 그대로 씁니다. 01절의 기준선은 정확 검색 순위입니다.
- **Ch 9 요약 §5 주의를 01절이 이어받았습니다**: 「점수 = 코사인 유사도」는 `InMemoryVectorStore` 기준입니다. 01절은 점수 대신 **거리**를 쓰고 「작을수록 가깝다」로 방향을 맞췄습니다. 02절 pgvector `<=>`도 거리입니다.
- 정의를 `<dl class="term">`으로 쓰면 `</dd>`가 단락을 나누지 않아 G6가 한 단락 여러 문장으로 셉니다(개선 전 01절이 그 때문에 걸렸습니다). **용어 표(`<table>`)로 쓰세요**(표는 G6 대상 밖).
- 쓰지 않은 말: 「청킹」, 한정어 없는 「청크」, 「오버랩」, 「임계값」, 「열」(→ 칸), 「유클리드 거리」(→ **L2 거리** 하나로), 「정규화」(→ 단위 길이 벡터), 「exact NN」·「ANN」 같은 줄임 영문.

### 01에서 새로 가르친 것

- **API·동작(노트북에서 실행한 것만)**: `OpenAIEmbeddings(model=, dimensions=)`·속성 `model`·`dimensions`(Ch 10 07절과 같은 모양), `embed_documents(목록)`(요청 1번), `embed_query(글)`(질문마다 1번), `math.sqrt()`(Ch 9 03절), `sorted(목록)`으로 튜플 목록 정렬(Ch 10 01절에서 배운 `sorted(목록)`), `round(값, 2)`.
- **Python 모양**: 후보 경로 `for`+`break`(Ch 10 01·Ch 11 01절과 같은 코드), 글 `+`로 경로 만들기, `with open(...)` 두 번, 튜플을 목록에 담아 `sorted`로 정렬하고 `pair[1]`로 꺼내기, 딕셔너리를 만든 뒤 키를 나중에 더하기, `"자리 " + str(cutoff)`로 키 이름 만들기, 목록 슬라이싱 `[:cutoff]`. **쓰지 않은 것**: `numpy`·`lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`Path`·`Counter`·`re`·f-string 안 계산·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`·`sorted`뿐입니다.
- **직접 만든 함수 열두 개**(노트북 셀, 실습 폴더 모듈 아님). 괄호 안은 본문 줄 수.
  - **Ch 9 03절과 같은 코드**: `dot_product(first, second)`(4) · `vector_length(vector)`(2) · `cosine_similarity(first, second)`(3)
  - **Ch 11과 같은 코드**: `unique_doc_ids(hit_list)`(5, Ch 11 01) · `find_gold_rank(doc_ids, gold_doc_ids)`(6, Ch 11 01) · `recall_at(doc_ids, gold_doc_ids, cutoff)`(6, Ch 11 02) · `mean_score(score_list)`(4, Ch 11 02)
  - **01절이 새로 만든 것**: `cosine_distance(first, second)`(2) · `l2_distance(first, second)`(5) · `measure_all(question_vector, distance_name)`(7) · `rank_by_distance(id_list, distance_list)`(7) · `score_one(query_index, distance_name)`(10)
  - **02~12절이 이어 쓰면 좋은 것**: `rank_by_distance()`는 `{"doc_id": …, "거리": …}` 목록을 내고 그 목록을 `unique_doc_ids()`에 그대로 넘길 수 있습니다. Ch 11 지표 함수는 **중복을 뺀 문서 ID 목록**을 받고 자르기는 함수 안에서 합니다(Ch 11 요약 §11-2, `evaluate.py`의 같은 이름 함수와 인자 모양이 다르니 섞지 마세요).
- **이어 쓸 이름과 값**: `candidates = [".", "../../..", "../../../.."]`·`root_path`(교재 출력 `.`)·`data_path`, `docs`(12)·`queries`(8)·`first_doc`·`first_query`, `embedding_model_name`·`vector_dimensions`(256)·`embedding_model`, `similarity_top`(1)·`doubling_factor`(2)·`cutoff_values`(`[1, 2, 3]`)·`cutoff_three`(3), `doc_texts`·`doc_ids`·`doc_vectors`·`query_vectors`·`doc_lengths`, `first_question_vector`·`first_doc_vector`·`first_cosine`·`first_l2`, `cosine_distances`·`cosine_ranked`·`l2_distances`·`l2_ranked`·`cosine_doc_ids`·`l2_doc_ids`, `first_gold_doc_ids`·`score_rows`(16줄, 칸 `자`·`질문`·`정답 자리`·`자리 1`·`자리 2`·`자리 3`).
- **출력 라벨(전부)**: 「langchain-openai:」「python-dotenv:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「문서 수:」「질문 수:」「문서의 칸 이름:」「첫 문서:」「질문의 칸 이름:」「첫 질문:」「첫 질문의 정답 문서 ID:」「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「코사인 유사도의 가장 큰 값:」「자르는 자리 세 가지:」「문서 벡터 수:」「첫 문서 벡터의 숫자 개수:」「문서 ID 목록:」(라벨 줄 따로)「질문 벡터 수:」「첫 질문 벡터의 숫자 개수:」「문서 벡터 길이(소수 둘째 자리):」(라벨 줄 따로)「코사인 거리:」「L2 거리:」「L2 거리를 두 번 곱한 값:」「코사인 거리를 두 배로 한 값:」「재어 본 문서 수:」「순위 | 문서 ID | 코사인 거리」(라벨 줄 따로)「순위 | 문서 ID | L2 거리」(라벨 줄 따로)「코사인 순위 항목 수: … 중복을 뺀 문서 수:」「L2 순위 항목 수: … 중복을 뺀 문서 수:」「코사인 앞 세 개:」「L2 앞 세 개:」「정답 문서 ID:」「코사인 정답 자리:」「L2 정답 자리:」「코사인 자리 3 재현율:」「L2 자리 3 재현율:」「담은 기록 줄 수:」「자 | 질문 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율」(라벨 줄 따로)「자 | 자르는 자리 | 질문 평균 재현율」(라벨 줄 따로)
- **실행값(2026-09-18 마지막 새 커널, 앞 실행과 같음)**: `문서 수: 12`·`질문 수: 8`, 문서 칸 네 개·질문 칸 네 개, `첫 문서: LIB-001 | library | 도서 대출 기간`·`첫 질문: C01 | 책을 빌릴 수 있는 기간은 며칠인가요?`·`첫 질문의 정답 문서 ID: LIB-001`, `벡터의 숫자 개수 설정: 256`, `문서 벡터 수: 12`·`첫 문서 벡터의 숫자 개수: 256`·`질문 벡터 수: 8`, 문서 벡터 길이 열두 개 모두 `1.0`, `코사인 거리: 0.56`·`L2 거리: 1.06`·두 관계 값 모두 `1.12`, 실행 1 `1 | LIB-004 | 0.43`·`2 | LIB-001 | 0.56`·`3 | LIB-003 | 0.62`, 실행 2 `1 | LIB-004 | 0.93`·`2 | LIB-001 | 1.06`·`3 | LIB-003 | 1.11`, `코사인 순위 항목 수: 12 중복을 뺀 문서 수: 12`(L2도 같음), 앞 세 개 두 자 모두 `['LIB-004', 'LIB-001', 'LIB-003']`, 정답 자리 두 자 모두 `2`·자리 3 재현율 두 자 모두 `1.0`, `담은 기록 줄 수: 16`, 표 열여섯 줄(`C01` 자리 2 · **`C02` 자리 7·자리 3 재현율 `0.0`** · 나머지 자리 1), 질문 평균 여섯 줄(두 자 모두 자리 1 `0.75`·자리 2 `0.875`·자리 3 `0.875`).
- **흔들리는 값**: 거리 값의 소수 셋째 자리 아래입니다. 탐색 실행 두 번에서 `0.5582` → `0.5583`, `1.0564` → `1.0566`, `0.5581` → `0.5599`로 달라졌습니다. 그래서 **거리는 소수 둘째 자리까지만 출력하고 그림 라벨에 넣지 않았습니다.** 순서·정답 자리·질문 평균은 흔들리지 않았습니다. 02~12절도 같게 하세요.
- **결론 태도(Ch 9 §1·Ch 10 §1·Ch 11 §3과 같음)**: 한 번 본 결과는 「이번 실행에서는」, 실행하지 않은 동작은 「이번에 실행하지 않았습니다」(01절은 길이가 1이 아닌 벡터), 어느 자가 나은지 판정하지 않음, 문서 12개·질문 8개·한 번 실행으로 결론 범위를 한정.

### 파일 쓰기 규칙 (02~06절이 먼저 읽을 것)

- **01절은 파일을 쓰지 않습니다.** `runs/core-01-exact.json`은 2026-09-09 바이트 `f8e81361e9c79fa5…c758` 그대로입니다. `runs/` 36개 묶음 해시 `a9c5d35a40a8acc0…`도 작업 전후 같습니다.
- 개선 전 01·02·03·05·06 노트북 마지막 셀은 `runs/core-0N-*.json`을 덮어쓰고 `runs/core-history/`에 보존본을 남겼습니다. 그 코드는 `Path`·`hashlib`·`datetime`·세미콜론·한 줄 복합문을 써서 사다리를 넘습니다.
- **읽는 쪽은 한 곳뿐입니다**: `textbook/qa/check_course_continuity.py` 187~196행이 바이트만 봅니다. 정본이 `before-manifest.json` 해시와 다르면 `runs/core-history/before-*-<파일 이름>`에 **원본 바이트가 남아 있어야** 합니다. 지금 여섯 파일 모두 `before-*` 보존본이 있고 바이트가 같습니다.
- 그래서 **파일을 쓰지 않는 쪽이 가장 안전합니다**(Ch 9 07·Ch 10 09·Ch 11 07 선례). 꼭 써야 하면 (a) `before-*` 보존본을 지우지 말고, (b) 이름에 `continuity`를 넣지 말고(`run_continuity_bundle.py` 79~83행이 증거 폴더로 옮깁니다), (c) 바뀐 해시를 진단·요약에 적으세요.
- 12절이 쓰는 `runs/advanced-continuity-*` 세 파일은 **계약이 가장 촘촘합니다**(실험 36건·`settings.candidate_unit == "chunk"`·`report_unit == "unique-parent-document"`·`metrics_policy == "chunk-candidate-unique-parent-macro-v1"`·질문 15개·`slices` 세 갈래·지표 재계산 대조, `check_course_continuity.py` 113~166행과 `tests/test_continuity.py`). 12절 작업 전에 그 두 파일을 먼저 읽으세요.
- Ch 9·Ch 10·Ch 11 기록과 Ch 6~8 비용 사슬은 **읽기만** 합니다. 01절은 읽지도 않았습니다.

### 검사 스크립트가 멈추는 자리 (01절 기준, 전체 마감 몫)

- `textbook/part3/qa/check_continuity.py` → 154행 `Stale archive: part2-practice.zip/…`
- `textbook/qa/check_course_continuity.py` → 212행 `Stale archive: part1-practice.zip/…`(`tomllib`이 필요해 Python 3.11 이상으로 돌립니다: `uv run --project labs/part3/ch12-retrieval-tuning python …`)
- `textbook/part3/qa/check_delivery.py` → **끝까지 통과**
- 실습 폴더 테스트 → `uv run --project labs/part3/ch12-retrieval-tuning --with pytest==8.4.2 python -m pytest labs/part3/ch12-retrieval-tuning/tests -q` → **4 passed**(dev 그룹에 `pytest`가 없어 `--with`로 넣습니다). 이 테스트는 **08·10·12절 노트북의 함수를 `ast`로 찾아 실제로 실행합니다** → `eligible_items`·`evaluate`·`mmr`·`metrics`·`evaluate_config`의 이름·인자·반환을 지키거나 테스트를 함께 고치세요.

### 02절이 이어받을 연결과 확인할 것

- 01 b8·노트북 정리 끝: 「02절에서는 같은 문서 12개 벡터를 pgvector 표에 넣고 HNSW 색인으로 검색합니다. 이 절의 정확 검색 순위가 그 결과를 견줄 기준선입니다.」
- **개선 전 02 노트북**은 01절과 같은 준비 셀을 다시 쓰고 `psycopg`·`register_vector`로 붙어 12개 벡터를 넣고 HNSW 인덱스를 만듭니다. 정확 검색과 HNSW 결과, `ef_search` 4와 40, `vector`/`halfvec` 2001차원 색인을 확인하고 `runs/core-02-hnsw.json`을 씁니다.
- **개선 전 02 노트북이 쓰는 것 가운데 01·Part 1~2에서 안 가르친 것**: `numpy`(`np.array(..., dtype=np.float32)`), 내포식 세 곳, 함수 안 함수·`with conn.transaction(), conn.cursor()` 두 개 묶기, `%` 문자열 서식, f-string 안 계산(`{int(ef_search)}`), `try/except psycopg.Error as error`·`error.diag.message_primary`, 세미콜론·한 줄 복합문, SQL 문자열 만들기. `psycopg`·`register_vector`·`CREATE EXTENSION`·`CREATE INDEX … USING hnsw`·`SET LOCAL`은 **이 챕터에서 처음 나오는 이름**이라 처음 쓰는 자리에서 뜻을 풀어야 합니다(규격 §4 세 문장).
- **`Decimal`**: 개선 전 02절은 `round((embedding <=> %s)::numeric, 4)`를 써서 출력이 `Decimal('0.4324')`로 나옵니다. 01절은 거리를 소수 둘째 자리 `float`로 출력합니다. 두 출력 모양이 다르니 02절에서 어느 쪽으로 맞출지 정하고 본문에 적으세요.
- **01절 값과 견줄 수 있는 자리**: 개선 전 02절 정확 검색 출력 `[('LIB-004', 0.4324), ('LIB-001', 0.5582), ('LIB-003', 0.6211)]`는 01절 코사인 거리 `0.43`·`0.56`·`0.62`와 같은 값입니다(같은 12개 문서·같은 질문 `C01`·같은 256차원·같은 코사인 거리). **01절이 Python으로 계산한 값과 pgvector `<=>`가 낸 값이 같다**는 문장을 02절 본문에 쓸 수 있습니다. 소수 셋째 자리 아래는 실행마다 흔들리므로 둘째 자리까지만 인용하세요.
- **아직 안 가르친 것(02가 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 전체에 더해 01절에서도 하지 않은 것 — 근사 검색 실행, 색인 자료 구조, 데이터베이스 연결·SQL, 점수 기준값·거르기, MMR, 재정렬, BM25·형태소 분석, 질문 재작성, 여러 질문 평균을 지표 셋으로 내기(01절은 재현율 하나만), 정밀도·nDCG 계산(Ch 11에서 배웠지만 01절은 쓰지 않음), 길이가 1이 아닌 벡터, 차원 수를 바꿔 비교하기, 문서 청크로 나누기(01절 문서는 나누지 않은 한 건씩), 답을 쓰는 모델 호출(이 챕터에서는 11·12절).

## §02 → §03

(02절 품질 개선 2026-09-18. 결과는 `02-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 47 = G1 6·G2 6·G3 7·G4 0·G5 12·G6 13·G7 3), 코드 셀 39(준비 5), 검사 문장 350, **임베딩 요청 9번**(문서 1 + 질문 8, 0.01달러 아래), 답을 쓰는 모델 0번. 같은 코드로 새 커널 두 번 실행해 `code_sha256` `17978388a9a5efec…`·`outputs_sha256` `9947bfc44d4a1803…`가 같고 셀별 출력 글자도 모두 같았으며 교재 출력은 마지막 실행 2026-09-18T15:19:32Z. `verify.py --chapter` `PASS 12 sections / 136 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(2차 job `da509d1b-71a8-443d-b281-ed4ba2cb0999` 채택, 1차 `ea23bfff-…` 탈락, 4크레딧, 생성 뒤 잔액 2754.5))

### pgvector 실행 방법 — §01 → §02 항목이 그대로 적용됩니다

- 준비 스크립트 `qa/upgrade/pre_exec.sh`를 `run_section.sh`가 절 실행 직전에 `source` 합니다. 따로 부를 일은 없습니다. **기기 셸은 호출이 끝나면 서버도 꺼지므로 노트북 실행은 `run_section.sh` 한 호출 안에서 끝내야 합니다.**
- 작업 VM 판은 **PostgreSQL 17.11 · pgvector 0.8.1**입니다. 02절이 이 값을 출력에 인용했고(`PostgreSQL 판: 17.11`·`pgvector 확장 판: 0.8.1`) 준비물·b7에 「Docker 이미지에서는 확장 판이 0.8.2로 나온다」와 「판 번호가 달라도 이 절에서 쓰는 기능은 같다」를 한 문장씩 넣었습니다. **03절도 판 번호를 출력하면 같은 두 문장을 넣으세요**(규격 §6).
- 기준 버전 세 갈래(02절 준비물): 필수 최소 pgvector **0.7.0**(자료형 `halfvec`이 생긴 판), 교재 출력 **PostgreSQL 17.11 · pgvector 0.8.1**, 참고 자료로 적은 공식 문서 **v0.8.6**. 학생 기준은 실습 폴더 `README.md`의 `pgvector/pgvector:0.8.2-pg17` 이미지입니다.
- 02절이 남긴 데이터베이스 표: **`ch12_core_hnsw`**(문서 12개, `vector(256)`, HNSW 색인 `ch12_core_hnsw_idx`). 차원 한도용 `ch12_dim_vector`·`ch12_dim_halfvec`은 마지막 셀에서 지웁니다. 03절은 개선 전에도 자기 표(`ch12_core_filter`)를 따로 만들므로 02절 표를 읽지 않습니다. **02절 본문·노트북에도 「03절이 같은 표를 다시 쓴다」는 문장을 넣지 않았습니다**(PLAYBOOK §4, 확인한 것만 씀).

### 02절이 새로 가르친 것

- **psycopg(Ch 4 03절 sqlite3와 이어 씀)**: `psycopg.connect(접속 글, autocommit=True)` · `conn.cursor()` · `cur.execute(sql)` · `cur.execute(sql, 값 튜플)` · `cur.fetchone()` · `cur.fetchall()` · `conn.close()` · `conn.closed`. 자리표시자가 `?`에서 **`%s`**로 바뀌는 점을 본문 b3와 노트북 4절에 적었습니다.
- **SQL**: `CREATE EXTENSION IF NOT EXISTS vector` · `DROP TABLE IF EXISTS` · `CREATE TABLE … (doc_id text PRIMARY KEY, category text, embedding vector(256))` · `INSERT INTO … VALUES (%s, %s, %s)` · `SELECT count(*)` · 거리 연산자 **`<=>`** · `ORDER BY … LIMIT %s` · `CREATE INDEX … USING hnsw (embedding vector_cosine_ops)` · **`EXPLAIN`** · `SELECT set_config('이름', %s, false)` · `SHOW 이름` · `SELECT current_setting('server_version')` · `SELECT extversion FROM pg_extension WHERE extname = 'vector'`.
  - `LIMIT`·`count(*)`는 과정 요약 §2에서 미교육이라 처음 쓰는 자리에서 한 문장으로 풀었습니다.
  - **`SET` 문장에는 자리표시자를 쓸 수 없어 `set_config()`를 씁니다.** Ch 4 03절의 「값은 자리표시자로 넘긴다」를 깨지 않으려고 정한 규칙이고 03절도 이어 쓰세요(`hnsw.iterative_scan`·`hnsw.ef_search`·`enable_seqscan` 모두 `set_config`로 바꿀 수 있습니다).
  - **표 이름·자료형 이름은 값이 아니라 문장의 일부**라 자리표시자로 넘길 수 없다는 사실을 주석과 결과 읽기에 적었습니다. 그 목록은 우리가 직접 적은 것이고 사용자 입력이 아닙니다.
- **벡터를 글로 넘김**: `str(벡터 목록)`이 pgvector의 글 모양(`[0.1,0.2]`)과 같아 `INSERT`와 `<=>` 양쪽에 값으로 넘어갑니다. **numpy와 `pgvector` 파이썬 패키지(`register_vector`)를 쓰지 않습니다.** 설치 목록은 `psycopg[binary]==3.3.5`·`python-dotenv==1.2.3`·`langchain-openai==1.6.1` 세 개입니다(실습 폴더 잠금은 고치지 않았습니다).
- **`try/except psycopg.Error as error`**와 속성 **`error.diag.message_primary`**(오류 한 줄). Ch 4 03절 `sqlite3.IntegrityError`와 같은 「점 이은 오류 이름」 모양입니다.
- **Python 모양**: `row[0]`·`row[1]`로 튜플 칸 꺼내기, 글 `+`로 SQL 만들기, `"Scan" in row[0]`로 줄 고르기, `글.strip()`, 목록에 딕셔너리 담아 표로 출력.

### 이어 쓸 이름과 값 (02절)

- 접속과 표: `database_url`(출력하지 않음) · `table_name`(`ch12_core_hnsw`) · `index_name`(`ch12_core_hnsw_idx`) · `conn` · `cur` · `create_sql` · `insert_sql` · `index_sql` · `search_sql`.
- 값: `vector_dimensions`(256) · `similarity_top`(1) · `top_three`(3) · `top_all`(12) · `cutoff_values`(`[1, 2, 3]`) · `ef_values`(`[4, 40]`) · `dimension_count`(2001).
- 자료와 벡터(01절과 같은 이름): `candidates` · `root_path` · `data_path` · `docs`(12) · `queries`(8) · `doc_texts` · `doc_ids` · `doc_vectors` · `query_vectors` · `first_question_vector` · `first_doc_vector` · `embedding_model_name` · `embedding_model`.
- 02절이 새로 만든 함수 일곱 개(괄호 안은 본문 줄 수): `run_search(question_vector, top_count)`(6, `{"doc_id": …, "거리": …}` 목록) · `print_hits(hit_list)`(4) · `find_scan_line(question_vector)`(5, `EXPLAIN`에서 읽기 방법 줄) · `set_seqscan(setting_value)`(3, 바뀐 값을 반환) · `try_hnsw_index(type_name, dimension_count)`(4) · `score_one(query_index, path_name)`(8).
- 01절과 같은 코드로 다시 정의한 함수 여덟 개: `dot_product` · `vector_length` · `cosine_similarity` · `cosine_distance` · `unique_doc_ids` · `find_gold_rank` · `recall_at` · `mean_score`. **`run_search()`가 내는 목록을 `unique_doc_ids()`에 그대로 넘길 수 있습니다**(01절 `rank_by_distance()`와 같은 모양).
- 결과 이름: `no_index_hits` · `with_index_hits` · `index_path_hits` · `ef_rows` · `dimension_rows` · `score_rows`(16줄, 칸 `경로`·`질문`·`정답 자리`·`자리 1`·`자리 2`·`자리 3`). 경로 이름은 **`"순차 스캔"`·`"색인"`** 두 글입니다.
- **쓰지 않은 것**: `numpy`·`register_vector`·`executemany`·`conn.transaction()`·`Decimal`·`::numeric`·`%` 문자열 서식·f-string 안 계산·`lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`Path`·`hashlib`·`datetime`·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`뿐입니다.

### 출력 라벨 (02절 전부)

「psycopg:」「python-dotenv:」「langchain-openai:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「문서 수:」「질문 수:」「표 이름:」「색인 이름:」「벡터의 숫자 개수:」「받아 올 문서 수 두 가지:」「자르는 자리 세 가지:」「PostgreSQL 판:」「pgvector 확장 판:」「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 벡터 수:」「첫 문서 벡터의 숫자 개수:」「표 만들기 SQL:」(라벨 줄 따로)「표에 들어간 행 수:」「질문 벡터 수:」「첫 질문:」「첫 질문의 정답 문서 ID:」「첫 문서 ID:」「파이썬으로 낸 코사인 거리:」「검색 SQL:」(라벨 줄 따로)「이 표의 색인:」「실행 계획의 읽기 방법 줄:」(라벨 줄 따로)「순위 | 문서 ID | 코사인 거리」(라벨 줄 따로)「색인 만들기 SQL:」(라벨 줄 따로)「enable_seqscan 설정:」「ef_search | 상위 3개 문서 ID」(라벨 줄 따로)「자료형 | 차원 수 | 색인 결과」(라벨 줄 따로)「담은 기록 줄 수:」「경로 | 질문 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율」(라벨 줄 따로)「경로 | 자르는 자리 | 질문 평균 재현율」(라벨 줄 따로)「연결 닫힘:」

### 실행값 (2026-09-18 마지막 새 커널, 두 실행이 같음)

- `PostgreSQL 판: 17.11` · `pgvector 확장 판: 0.8.1` · `표에 들어간 행 수: 12` · `첫 문서 벡터의 숫자 개수: 256`.
- `파이썬으로 낸 코사인 거리: 0.56`(첫 질문 `C01` × 첫 문서 `LIB-001`).
- 검색 SQL `SELECT doc_id, embedding <=> %s FROM ch12_core_hnsw ORDER BY embedding <=> %s LIMIT %s`.
- 세 실행의 상위 3개가 모두 `1 | LIB-004 | 0.43` · `2 | LIB-001 | 0.56` · `3 | LIB-003 | 0.62`. **01절 코사인 거리와 같은 값입니다.**
- 실행 계획 줄: 실행 1 `->  Seq Scan on ch12_core_hnsw  (cost=0.00..19.75 rows=650 width=48)` · 실행 2 `->  Seq Scan on ch12_core_hnsw  (cost=0.00..2.18 rows=12 width=48)` · 실행 3 `->  Index Scan using ch12_core_hnsw_idx on ch12_core_hnsw  (cost=12.09..20.27 rows=12 width=48)`. **색인을 만든 뒤에도 계획 줄이 순차 스캔이었습니다**(표가 12행이라 계획기가 그쪽 비용을 더 작게 어림). 줄 앞의 `->` 표시와 괄호 안 비용·행 수 어림은 「실행 환경에 따라 달라집니다」로 적고 그림 라벨에 넣지 않았습니다.
- `ef_search` `4`와 `40` 모두 `['LIB-004', 'LIB-001', 'LIB-003']`. **반복이 끝난 뒤 설정 값은 기본값과 같은 40입니다**(뒤 셀이 그 값을 씁니다).
- `vector | 2001 | column cannot have more than 2000 dimensions for hnsw index` · `halfvec | 2001 | 색인을 만들었습니다`.
- 질문 8개 × 경로 2개 = `담은 기록 줄 수: 16`. 정답 자리는 `C01` 2 · `C02` 7 · 나머지 1이고 **두 경로가 질문마다 네 칸이 같았습니다.** 질문 평균 재현율은 두 경로 모두 자리 1 `0.75` · 자리 2 `0.875` · 자리 3 `0.875`로 **01절 값과 같습니다.**
- `연결 닫힘: True`.

### 용어 (02절이 더한 여덟 개, 03~12도 같게)

- **pgvector** · **HNSW** · **거리 연산자 `<=>`** · **연산자 클래스(operator class)** · **실행 계획(execution plan)**(정하는 부분은 **계획기**) · **순차 스캔(sequential scan)** · **`ef_search`** · **`halfvec`**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 8」입니다.
- 01절 말 다섯 개(L2 거리·코사인 거리·정확 검색·근사 검색·단위 길이 벡터)와 Ch 9~11 말(문서 청크·색인·벡터스토어·검색 점수·후보 목록·자르는 자리·재현율·질문 평균·정답 문서 ID·고유 문서·기준선)을 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**이고 한정어 없는 「청크」는 쓰지 않습니다.
- **「색인」은 Ch 9 뜻(벡터를 넣어 둔 검색 자료)과 이 절의 데이터베이스 색인이 겹칩니다.** 02절은 데이터베이스 쪽을 늘 「HNSW 색인」 또는 「색인 경로」로 부르고 칸 이름·연산자 클래스를 함께 적었습니다. 03절도 같게 부르세요.
- **「경로」**는 표를 읽는 방법 두 가지를 가리키는 말로 씁니다(순차 스캔 경로·색인 경로). 노트북 기록 칸 이름도 `경로`입니다.
- **「포트」**를 씁니다(실습 폴더 `README.md`와 같은 말). 「문가름 번호」 같은 낯선 말은 쓰지 않습니다.
- 쓰지 않은 말: 「인덱스」(→ 색인), 「시퀀셜 스캔」·「인덱스 스캔」(→ 순차 스캔·색인 경로, 계획 줄의 영문 `Seq Scan`·`Index Scan`은 출력이라 그대로 인용), 「쿼리」(→ 질의 또는 SQL 문장), 「컬럼」·「열」(→ 칸), 「튜닝」(→ 설정 바꾸기), 「레이턴시」(→ 걸린 시간), 「post-filtering」 같은 줄임 영문.

### 파일 쓰기 규칙 — 02절도 파일을 쓰지 않습니다

- `runs/core-02-hnsw.json`은 2026-09-18 현재 바이트 `e007a959899ec0ea866ca7d03597fec13bbd3c84bf677c9048251658f1519175` 그대로이고 `runs/core-history/before-e007a959899e-core-02-hnsw.json`과 같습니다. `runs/` 36개 묶음 해시 `a9c5d35a40a8acc0…`도 작업 전후 같고 `core-history/`는 12개입니다.
- **03절 결정 사항**: 개선 전 03 노트북 마지막 두 셀이 `runs/core-03-iterative-scan.json`을 덮어씁니다(정본 바이트 `4d9be88254b6…`가 `before-4d9be88254b6-core-03-iterative-scan.json`과 같음). 읽는 쪽은 `check_course_continuity.py` 187~196행 하나이고 바이트만 봅니다. **01·02절 선례대로 쓰지 않는 쪽을 먼저 검토하세요.**
- `advanced-queries.json`·`advanced-documents.json`은 한 글자도 고치지 않습니다(`check_continuity.py` 44~46행·`check_course_continuity.py` 78~80행·실습 폴더 `tests/test_continuity.py`).
- 실습 폴더 테스트는 작업 전후 **4 passed**입니다(`uv run --project labs/part3/ch12-retrieval-tuning --with pytest==8.4.2 python -m pytest labs/part3/ch12-retrieval-tuning/tests -q`).
- 공용 화면 검사 결과 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`은 **26행을 유지**해야 합니다(`finalize_continuity_evidence.py` 15행). 02절은 `/tmp` 사본에 `ONLY` 필터와 병합 저장을 넣어 02절 두 줄만 바꿨습니다(패치 사본은 `/tmp/ch12-02/vis12.cjs`, 공용 원본은 고치지 않았습니다).

### 03절이 이어받을 연결과 확인할 것

- 02 b8·노트북 정리 끝: 「03절에서는 범주 칸이 있는 표를 새로 만들고 메타데이터 필터를 함께 걸어 검색합니다. 필터를 걸면 받아 오는 줄 수가 `LIMIT`으로 정한 수보다 적어질 수 있습니다.」
- **03절은 이 챕터에서 유일한 `paired` 형식입니다**(`chapter.json`). 본문 토큰은 `{{notebook:03-…|example}}`과 `{{notebook:03-…|failure}}`이고, 노트북 셀 메타데이터 `lesson_part`는 `example`·`before`·`after`입니다. 결과 읽기가 다음 소제목과 한 셀에 있으면 `nbkit.write_notebook()`이 자동으로 나눕니다(규격 §6).
- **개선 전 03 노트북이 하는 일**: 8차원 합성 벡터를 표 `ch12_core_filter`에 넣습니다(`common` 3000행 + `rare` 12행, `numpy` 난수 `default_rng(12)`). HNSW 색인과 `ANALYZE` 뒤 `enable_seqscan=off`·`hnsw.ef_search=5`로 `WHERE category='rare' … LIMIT 5`를 돌립니다. Before(`hnsw.iterative_scan=off`)는 **반환 개수 0**, After(`strict_order`)는 **5개**(`[(3010, 0.0101), (3009, 0.0178), (3001, 0.036), (3008, 0.0473), (3005, 0.0539)]`)입니다. 외부 API를 부르지 않습니다.
- **가장 큰 결정: 합성 자료를 numpy 없이 만들 방법.** 02절이 numpy를 없앴으므로 03절도 같게 가야 합니다. 검토할 두 갈래를 적어 둡니다.
  1. **규칙으로 만든 벡터**: 난수 대신 반복 번호로 값을 정하는 여러 줄 `for`(예: 한 칸만 번호에 따라 조금씩 다르게)로 `common`·`rare`를 만듭니다. 재현성이 확실하고 `random`·`numpy`를 모두 안 씁니다. 행 수는 계획기가 색인을 고를 만큼 크게 두어야 합니다.
  2. **SQL로 만든 행**: `INSERT … SELECT`와 `generate_series`로 데이터베이스가 행을 만들게 합니다. 파이썬은 짧아지지만 새 SQL 낱말이 늘고 값이 난수면 재현성을 따로 맞춰야 합니다.
  - 어느 쪽이든 **02절이 가르친 것을 그대로 쓸 수 있습니다**: `str(벡터)`로 값 넘기기, `set_config('enable_seqscan', …)`, `set_config('hnsw.ef_search', …)`, `find_scan_line()`으로 계획 줄 보기, `run_search()`·`print_hits()` 모양.
  - **02절 결론과 이어집니다**: 12행 표에서는 계획기가 순차 스캔을 골랐습니다. 03절이 색인 경로를 보이려면 행을 늘리거나 `enable_seqscan`을 off로 두어야 하고, **그 까닭을 02절을 가리켜 한 문장으로 적으면 됩니다.**
- **`Decimal`**: 개선 전 03절도 `round((embedding <=> %s)::numeric, 4)` 뒤에 `float(...)`로 바꿉니다. 02절은 SQL이 거리를 그대로 내고 파이썬 `round(값, 2)`로 출력합니다. **02절 모양으로 맞추세요.**
- **`ANALYZE`**: 개선 전 03절은 표를 만든 뒤 `ANALYZE`를 부릅니다. 02절은 부르지 않았고, 색인을 만들면서 행 수 어림이 `650`에서 `12`로 바뀌는 것만 출력으로 보았습니다. 03절이 `ANALYZE`를 쓰면 처음 쓰는 자리에서 뜻을 한 문장으로 풀어야 합니다.
- **`hnsw.iterative_scan`**: 03절이 처음 쓰는 이름입니다. `off`·`strict_order`·`relaxed_order` 세 값 가운데 개선 전은 앞 두 개만 실행했습니다. 실행하지 않은 값의 동작은 「이번에 실행하지 않았습니다」로 적으세요. pgvector 0.8.1 기준으로 설치판 문서를 확인하고, 본문에 「소스 확인:」 갈래를 갈라 적습니다(규격 §5-3, Ch 10 검토 선례).
- **오류·실패 색**: 03절은 paired이므로 **Before 결함 결과는 빨강**입니다(반환 개수 0). 02절은 paired가 아니라 빨강 0장이고 받아 출력한 오류를 노랑으로 두었습니다(규격 §5-3).
- **아직 안 가르친 것(03이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01절 목록에 더해, 02절에서도 하지 않은 것 — 검색 시간 재기, 색인을 만드는 데 걸린 시간, 큰 말뭉치에서 재현율 재기, `ef_search`를 4·40 밖으로 넓히기, `halfvec`으로 실제 검색하기, `m`·`ef_construction` 같은 색인 만들기 설정, `ANALYZE`와 표 통계, `hnsw.iterative_scan`, 메타데이터 칸으로 걸러 내기, 여러 색인 견주기, `numpy`, 트랜잭션 묶기(`conn.transaction()`), `executemany`, 점수 기준값·거르기, BM25·형태소 분석, 재정렬, MMR, 질문 재작성, 답을 쓰는 모델 호출(11·12절).

## §03 → §04

(03절 품질 개선 2026-09-18. 결과는 `03-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 41 = G1 4·G2 6·G3 7·G4 0·G5 8·G6 13·G7 3), 코드 셀 51(준비 5), 검사 문장 406, **임베딩 요청 9번**(문서 1 + 질문 8, 0.01달러 아래), 답을 쓰는 모델 0번. 같은 코드로 새 커널 두 번 실행해 `code_sha256` `56595a043b3d0d0a…`·`outputs_sha256` `76e5c409969eeabc…`가 같고 교재 출력은 마지막 실행 2026-09-18T16:12:36Z. `verify.py --chapter` `PASS 12 sections / 180 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(1차 job `d1fdbff2-70a9-4f3a-ac71-f9c8476ed4f8` 채택, 2크레딧, 생성 전 잔액 2735))

### 04절은 pgvector를 쓰지 않습니다 — 먼저 읽을 것

- 개선 전 04 노트북은 `kiwipiepy`·`rank_bm25`만 쓰고 데이터베이스에 붙지 않습니다. **`pre_exec.sh`가 켜 주는 서버는 필요 없지만** `run_section.sh`가 늘 source 하므로 그대로 두면 됩니다. 서버가 켜져 있어도 04절 출력에는 영향이 없습니다.
- 01~03절이 만든 데이터베이스 표 **`ch12_core_hnsw`(02절)와 `ch12_core_filter`(03절)는 지우지 않고 남겨 두었습니다.** 04절은 두 표를 읽지 않습니다.
- 03절에서 바꾼 설정 두 개(`hnsw.iterative_scan`·`enable_seqscan`)는 마지막 셀에서 기본값(`off`·`on`)으로 되돌립니다. 설정은 연결 단위라 04절과 무관합니다.

### 03절이 새로 가르친 것

- **SQL**: `WHERE category = %s`를 거리 정렬과 한 문장에 함께 쓰기(Ch 4 03절 `WHERE` + 02절 `ORDER BY ... LIMIT`). 조건 값도 자리표시자로 넘깁니다. 범주별 행 수는 `SELECT count(*) ... WHERE category = %s`를 네 번 불러 셌습니다(**`GROUP BY`를 쓰지 않았습니다** — 과정 요약 §2에서 미교육이라 낱말을 하나 덜 늘렸습니다).
- **설정**: `hnsw.iterative_scan`(`off`·`strict_order`·`relaxed_order`), 관찰용으로 `SHOW hnsw.max_scan_tuples`(`20000`)·`SHOW hnsw.ef_search`(`40`). 02절이 정한 `set_config()` 규칙을 그대로 씁니다.
- **Python 모양**: `목록.copy()`(Ch 2 03절), 기호 `%`(나눈 뒤 남는 값 — 이 챕터에서 처음, 설명 한 문장을 넣었습니다), 튜플 목록 `sorted()`로 범주 안 순위 만들기(01절 모양), 두 겹 `for`로 목록 모으기(Ch 5 모양).
- **쓰지 않은 것**: `numpy`·`register_vector`·`conn.transaction()`·`executemany`·`ANALYZE`·`GROUP BY`·`Decimal`·`::numeric`·`%` 문자열 서식·f-string 안 계산·`lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`Path`·`hashlib`·`datetime`·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`·`sorted`뿐입니다. `try`도 쓰지 않았습니다(02절은 차원 한도 실험에서 썼습니다).

### 이어 쓸 이름과 값 (03절)

- 접속과 표: `database_url`(출력하지 않음) · `table_name`(`ch12_core_filter`) · `index_name`(`ch12_core_filter_idx`) · `conn` · `cur` · `create_sql` · `insert_sql` · `index_sql` · `search_sql`(필터 없음) · `filter_sql`(범주 조건).
- 값: `vector_dimensions`(256) · `similarity_top`(1) · `top_three`(3) · `cutoff_values`(`[1, 2, 3]`) · `filler_per_query`(50) · `shift_base`(0.02) · `shift_step`(0.0001) · `filler_category`(`"other"`) · `category_names`(`["library", "facility", "account", "other"]`) · `path_names`(**`["정확 검색", "색인 경로"]`**).
- 자료와 벡터(01·02절과 같은 이름): `candidates` · `root_path` · `data_path` · `docs`(12) · `queries`(8) · `doc_texts` · `doc_ids` · `doc_vectors` · `query_vectors` · `first_question_vector` · `first_doc_vector` · `embedding_model_name` · `embedding_model`.
- 03절이 새로 만든 이름: `first_gold_doc_id` · `first_category`(`"library"`) · `filler_vectors`(400) · `made_vectors` · `filler_id`(`OTH-1`~`OTH-400`) · `filler_distance` · `doc_distance` · `first_vector_text` · `no_filter_hits` · `exact_hits` · `before_hits` · `after_hits` · `relaxed_hits` · `score_rows`(16줄).
- 01·02절과 같은 코드로 다시 정의한 함수 여덟 개: `dot_product` · `vector_length` · `cosine_similarity` · `cosine_distance` · `unique_doc_ids` · `find_gold_rank` · `recall_at` · `mean_score`. 02절과 같은 코드 셋: `run_search` · `print_hits` · `set_seqscan`.
- 03절이 새로 만든 함수 일곱 개(괄호 안은 본문 줄 수): `find_category(doc_id)`(6) · `make_filler_vectors(base_vector, count)`(7) · `rank_in_category(question_vector, category_name, top_count)`(9, 파이썬 정확 검색) · `run_filtered_search(question_vector, category_name, top_count)`(6) · `set_iterative_scan(setting_value)`(3) · `pick_hits(query_index, path_name)`(8) · `score_one(query_index, path_name)`(10). `find_scan_line`은 02절 판을 **SQL과 값 튜플을 받는 모양**으로 바꿨습니다(7).
- **기록 한 줄의 칸 일곱 개**: `경로`·`질문`·**`받아 온 줄 수`**·`정답 자리`·`자리 1`·`자리 2`·`자리 3`. 02절 기록에 `받아 온 줄 수`를 더한 모양입니다.

### 출력 라벨 (03절 전부)

「psycopg:」「python-dotenv:」「langchain-openai:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「문서 수:」「질문 수:」「표 이름:」「색인 이름:」「벡터의 숫자 개수:」「받아 올 줄 수:」「자르는 자리 세 가지:」「질문마다 만드는 채움 행 수:」「채움 행의 숫자를 바꿀 기준과 간격:」「범주 이름 네 가지:」「견줄 경로 두 가지:」「PostgreSQL 판:」「pgvector 확장 판:」「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 벡터 수:」「첫 문서 벡터의 숫자 개수:」「질문 벡터 수:」「첫 질문:」「첫 질문의 정답 문서 ID:」「그 문서의 범주:」「채움 벡터 수:」「첫 채움 벡터의 숫자 개수:」「첫 채움 벡터의 코사인 거리:」「첫 문서 ID:」「첫 문서의 코사인 거리:」「표 만들기 SQL:」(라벨 줄 따로)「표에 들어간 행 수:」「범주 | 행 수」(라벨 줄 따로)「색인 만들기 SQL:」(라벨 줄 따로)「필터 없는 검색 SQL:」(라벨 줄 따로)「범주 조건을 붙인 검색 SQL:」(라벨 줄 따로)「실행 계획의 읽기 방법 줄:」(라벨 줄 따로)「받아 온 줄 수:」「순위 | 문서 ID | 코사인 거리」(라벨 줄 따로)「enable_seqscan 설정:」「후보 목록 크기:」「반복 탐색이 볼 줄 수 한도:」「걸 범주:」「반복 탐색 설정:」「담은 기록 줄 수:」「경로 | 질문 | 받아 온 줄 수 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율」(라벨 줄 따로)「경로 | 자르는 자리 | 질문 평균 재현율」(라벨 줄 따로)「연결 닫힘:」

### 실행값 (2026-09-18 마지막 새 커널, 두 실행이 같음)

- `PostgreSQL 판: 17.11` · `pgvector 확장 판: 0.8.1` · `표에 들어간 행 수: 412` · 범주별 `library | 4` · `facility | 4` · `account | 4` · `other | 400`.
- `첫 질문의 정답 문서 ID: LIB-001` · `그 문서의 범주: library` · `채움 벡터 수: 400`.
- `첫 채움 벡터의 코사인 거리: 0.0` · `첫 문서의 코사인 거리: 0.56`(첫 문서 `LIB-001`, 01·02절과 같은 값).
- 실행 1(필터 없음) 계획 줄 `->  Seq Scan on ch12_core_filter  (cost=0.00..65.18 rows=412 width=48)`, 상위 3개 `1 | OTH-1 | 0.0` · `2 | OTH-2 | 0.0` · `3 | OTH-3 | 0.0`. **412행 표에서도 계획기가 차례로 읽는 쪽을 골랐습니다**(02절 12행 표와 같은 결론).
- `enable_seqscan 설정: off` 뒤 `후보 목록 크기: 40` · `반복 탐색이 볼 줄 수 한도: 20000` · 계획 줄 `->  Index Scan using ch12_core_filter_idx on ch12_core_filter  (cost=246.02..524.25 rows=2 width=48)`. 괄호 안 비용·행 수 어림은 「실행 환경에 따라 달라집니다」로 적고 그림 라벨에 넣지 않았습니다.
- 정확 검색(파이썬, 범주 `library`) 상위 3개 `1 | LIB-004 | 0.43` · `2 | LIB-001 | 0.56` · `3 | LIB-003 | 0.62`. **01·02절 상위 세 개와 같은 값입니다.**
- 질문 8개 × 경로 2개 = `담은 기록 줄 수: 16`. 정확 검색은 여덟 질문 모두 `받아 온 줄 수` 3이고 정답 자리는 `C01` 2 · `C02` 0 · 나머지 1. 색인 경로는 `C05`·`C06`·`C08`만 1줄(그 한 줄이 정답 문서)이고 나머지 다섯 질문은 0줄입니다. **여덟 질문 가운데 받아 올 줄 수 3을 채운 질문이 없습니다.**
- 질문 평균 재현율: 정확 검색 자리 1 `0.75` · 자리 2 `0.875` · 자리 3 `0.875`(01·02절 값과 같음), 색인 경로 세 자리 모두 `0.375`.
- Before(반복 탐색 `off`, 첫 질문 × `library`) `받아 온 줄 수: 0`. After(`strict_order`) `받아 온 줄 수: 3`과 정확 검색과 같은 세 줄. 값 바꿔 보기(`relaxed_order`)도 같은 세 줄·같은 순서.
- `연결 닫힘: True`.

### 흔들리는 값 — 04절도 같은 규칙으로

- **반복 탐색을 켠 채로 질문 여덟 개를 재면 값이 흔들립니다.** 색인을 다시 만들며 다섯 번 재 보니 `strict_order`의 받아 온 줄 수가 질문마다 0~3으로 달라졌습니다(`C05` 3 → 2, `C07` 3 → 1, `C08` 3 → 0). pgvector HNSW 색인은 만들 때마다 구조가 조금 달라집니다. 그래서 **교재에는 첫 질문 하나만 싣고** 나머지는 「이번에 실행하지 않았습니다」로 적었습니다. 04절 이후 반복 탐색을 다시 쓰면 같은 판단을 하세요.
- 거리는 01·02절과 같이 **소수 둘째 자리까지만** 출력하고 그림 라벨에는 문서 ID만 넣습니다.
- **psycopg 준비된 문장 함정**: 같은 SQL을 다섯 번 넘게 실행하면 psycopg가 그 문장을 준비해 두고 계획을 다시 씁니다(`prepare_threshold` 기본값 5). `enable_seqscan`을 켠 상태와 끈 상태에서 같은 SQL을 섞어 실행하면 `EXPLAIN`과 실제 실행 결과가 어긋납니다. 03절은 필터 검색을 off 상태에서만 실행하고 견줄 정답은 파이썬에서 냈습니다. 데이터베이스를 다시 쓰는 절(없을 것으로 보이지만)은 이 함정을 먼저 보세요.

### 용어 (03절이 더한 다섯 개, 04~12도 같게)

- **메타데이터 필터(metadata filter)** · **나중 걸러 내기(post-filtering)** · **선택도(selectivity)** · **반복 탐색(iterative scan)** · **채움 행**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 5」입니다.
- **「나중 걸러 내기」**로 부르고 영문 「post-filtering」은 용어 표 괄호에 한 번만 적었습니다(02절 「쓰지 않은 말」 규칙). 절 제목의 「iterative scan」은 `chapter.json` 제목·파일 이름이라 그대로 두고 본문은 「반복 탐색」으로 부릅니다.
- **「경로」**는 02절 뜻(표를 읽는 방법)을 잇되 03절 기록의 두 값은 **`정확 검색`·`색인 경로`**입니다(02절은 `순차 스캔`·`색인`). 「정확 검색」은 01절이 정한 말이고 03절에서는 파이썬 계산을 가리킵니다.
- **「채움 행」**은 이 절에서만 쓰는 연습용 행입니다. 04절 이후에서 다른 뜻으로 쓰지 마세요.
- 01·02절 말 열세 개(L2 거리·코사인 거리·정확 검색·근사 검색·단위 길이 벡터·pgvector·HNSW·거리 연산자 `<=>`·연산자 클래스·실행 계획·순차 스캔·`ef_search`·`halfvec`)와 Ch 9~11 말을 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**이고 한정어 없는 「청크」는 쓰지 않습니다.
- 쓰지 않은 말: 「인덱스」(→ 색인), 「post-filtering」 단독, 「쿼리」(→ 질의 또는 SQL 문장), 「컬럼」·「열」(→ 칸), 「반환 개수」(→ 받아 온 줄 수), 「LIMIT보다 적게」 같은 영문 시작 표현(→ 「받아 올 줄 수보다 적게」), 「지연 시간」(→ 걸린 시간), 「임계값」.

### 파일 쓰기 규칙 — 03절도 파일을 쓰지 않습니다

- `runs/core-03-iterative-scan.json`은 작업 전후 `4d9be88254b631d348b3572c8216ad57b6c2bd8166f7f58a46ac596f83e9e1d1` 그대로이고 `runs/core-history/before-4d9be88254b6-core-03-iterative-scan.json`과 바이트가 같습니다. `runs/` 36개 묶음 해시 `a9c5d35a40a8acc0…`도 작업 전후 같고 `core-history/`는 12개입니다.
- **04절 결정 사항**: 개선 전 04 노트북 마지막 셀이 `runs/core-04-bm25.json`을 덮어씁니다(`Path`·`hashlib`·`datetime`·세미콜론·한 줄 복합문). 읽는 쪽은 `check_course_continuity.py` 187~196행 하나이고 바이트만 봅니다. **01·02·03절 선례대로 쓰지 않는 쪽을 먼저 검토하세요.**
- `advanced-queries.json`·`advanced-documents.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않습니다.
- 실습 폴더 테스트는 작업 전후 **4 passed**입니다. `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…`도 그대로입니다(04절 `%pip` 목록 `kiwipiepy==0.23.2`·`rank-bm25==0.2.2`는 이미 잠금에 있습니다 — 확인만 하세요).
- 공용 화면 검사 결과 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`은 **26행을 유지**해야 합니다(`finalize_continuity_evidence.py` 15행). 02·03절은 `/tmp` 사본(`/tmp/ch12-03/vis12.cjs`)에 `ONLY` 필터와 병합 저장을 넣어 해당 절 두 줄만 갱신했고 공용 원본은 고치지 않았습니다. 사본의 출력 경로는 `process.env.HOME` 기준으로 바꿔 두었습니다.

### 04절이 이어받을 연결과 확인할 것

- 03 b8·노트북 정리 끝: 「04절에서는 벡터 거리가 아니라 한국어 낱말로 문서를 찾습니다. 형태소 분석기로 낱말을 가르고 낱말이 겹치는 정도로 순위를 냅니다.」
- **개선 전 04 노트북이 쓰는 것 가운데 01~03절·Part 1~2에서 안 가르친 것**: 내포식 네 곳(`[kiwi_terms(f"{d['title']} {d['text']}") for d in docs]` 등), 제너레이터 식 한 곳(`next((folder for folder in [Path.cwd(), *Path.cwd().parents] ...))`), `lambda`(`key=lambda i: scores[i]`), `sorted(..., key=, reverse=)`, 기본값 매개변수 `k=3`, f-string 안 계산, 한 글자 변수 `d`·`i`, `sum(...)`으로 참 개수 세기, `float(...)`, 튜플 풀어 담기 `for doc_id, _ in ...`, 상수 대문자 이름 `KEEP`, `str.startswith(튜플)`, `Path.read_text()`, 세미콜론·한 줄 복합문, `hashlib`·`datetime`. **`Kiwi`·`kiwi.tokenize`·`token.form`·`token.tag`·`BM25Okapi`·`get_scores`는 이 챕터에서 처음 나오는 이름**이라 처음 쓰는 자리에서 뜻을 풀어야 합니다(규격 §4 세 문장).
- **정렬**: 01·03절은 튜플 목록을 `sorted(목록)`으로 정렬하고 `pair[1]`로 꺼냈습니다. 04절은 점수가 **클수록** 좋으므로 방향이 반대입니다. `key=`·`reverse=`를 쓰지 않고 「점수에 음수를 붙여 `sorted`」나 「점수 목록에서 가장 큰 값을 찾는 여러 줄 `for`」 가운데 하나를 골라 본문에 밝히세요.
- **01·03절 지표 함수를 이어 쓸 수 있습니다**: `unique_doc_ids()`는 `{"doc_id": …, "거리": …}` 목록을 받습니다. BM25는 거리가 아니라 점수라 **칸 이름을 `거리`로 쓰면 안 됩니다**. 칸 이름을 `점수`로 두고 `unique_doc_ids()`가 보는 키는 `doc_id`뿐이라는 점을 확인하세요. Ch 11 지표 함수 세 개는 **중복을 뺀 문서 ID 목록**을 받고 자르기는 함수 안에서 합니다(Ch 11 요약 §11-2).
- **Ch 9 요약 §5 주의**: 「점수 = 코사인 유사도」는 `InMemoryVectorStore` 기준입니다. 01~03절은 **거리**(작을수록 가까움)를 썼고 04절 BM25는 **점수**(클수록 관련 있음)입니다. 방향이 반대라는 문장을 04절 b3이나 b4에 한 줄 넣고, 01~03절 거리 값과 BM25 점수를 나란히 놓지 마세요.
- **개선 전 04절 본문에 실행하지 않은 주장이 있습니다**: 「PostgreSQL `ts_rank`는 전문 검색 순위 함수이지만 BM25 구현과 같다고 설명하지 않습니다」는 남길 수 있지만 `ts_rank`를 실행하지는 않았습니다. 「Kiwi+BM25는 교육용 질문 8개 모두에서 정답 문서를 top-3에 포함했습니다」의 `8/8`은 다시 실행해 값을 확인하세요(형태소 분석기 판이 같아도 값이 바뀌면 본문·그림을 새 출력으로 고칩니다).
- **Ch 5 「조각」과 갈라 적기**: 04절 b3이 이미 「Ch 5의 모델 입력 토큰과 이번 절의 BM25 검색 토큰은 용도와 분할 규칙이 다릅니다」를 적고 있습니다. 규격 §4의 용어 약속대로 **「조각」은 Ch 5 토큰 뜻 전용**이므로 Kiwi 결과는 「형태소」 또는 「검색 낱말」로 부르고 「조각」이라고 쓰지 마세요.
- **아직 안 가르친 것(04가 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01·02절 목록에 더해, 03절에서도 하지 않은 것 — 검색 시간 재기, 반복 탐색을 여러 질문에서 재기, `relaxed_order`와 `strict_order`를 큰 자료에서 견주기, 조건 칸 색인·부분 색인·표 나누기, `GROUP BY`·`ANALYZE`·표 통계, 여러 조건을 `AND`로 묶기, 정밀도·nDCG 계산(Ch 11에서 배웠지만 01~03절은 재현율만), 점수 기준값·거르기, BM25·형태소 분석, 재정렬, MMR, 질문 재작성, 답을 쓰는 모델 호출(11·12절).

## §04 → §05

(04절 품질 개선 2026-09-18. 결과는 `04-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 53 = G1 11·G2 8·G3 7·G4 0·G5 9·G6 15·G7 3), 코드 셀 28(준비 4), 검사 문장 303, **서비스 요청 0번**(임베딩도 답을 쓰는 모델도 부르지 않음). 같은 코드로 새 커널 두 번 실행해 `code_sha256` `a5606d20db53e44a…`·`outputs_sha256` `ad046983eeb8b318…`가 같고 셀별 출력 글자도 모두 같았으며 교재 출력은 마지막 실행 2026-09-18T16:53:34Z. `verify.py --chapter` `PASS 12 sections / 201 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(1차 job `f2ab200e-0e4a-4b9d-9376-d632369e55d3` 채택, 2크레딧, 생성 전 잔액 2733))

### 작업 환경이 바뀌었습니다 — 05절이 먼저 읽을 것

- **기기 VM이 다시 만들어져 `/tmp`가 비어 있었습니다.** `/tmp/mmd`(mermaid-cli 11.17.0)·`/tmp/pptr-cache`·`/tmp/pw`(playwright-core 1.56.1)를 다시 설치했습니다. `libxdamage1`은 apt 목록을 열 수 없어(`Permission denied`) `.deb`를 직접 받았습니다: `cd /tmp/libs && curl -sSL -o libxdamage1.deb http://ports.ubuntu.com/ubuntu-ports/pool/main/libx/libxdamage/libxdamage1_1.1.5-2build2_arm64.deb && dpkg-deb -x libxdamage1.deb root`.
- **uv가 `0.12.13`으로 올라가 `uv run`이 멈춥니다.** 기존 가상환경 `.cache/vm/venv-ch12-retrieval-tuning`의 `nvidia/cusparselt` 파일을 지우려 하는데 마운트 폴더의 삭제가 막혀 있어 `Operation not permitted`로 끝납니다(`--inexact`도 같음). 삭제 권한을 요청하지 않고 **`UV_NO_SYNC=1`**로 동기화를 건너뛰었습니다. 그 환경에는 이 챕터 잠금의 패키지가 이미 들어 있습니다.
- `--with`로 만드는 덧붙임 환경은 `UV_CACHE_DIR` 안 임시 폴더를 지우므로 **캐시만 `/tmp/uv-cache`**로 두었습니다. 사용자 디스크의 `.cache/vm/uv`는 옮기지도 지우지도 않았습니다(AGENT-BRIEF).
- `run_section.sh`가 `UV_CACHE_DIR="$VM/uv"`를 강제로 export 하므로 **사본을 만들어 썼습니다**(`/tmp/ch12-04/run_section.sh`: `set -e` 뒤에 `export UV_NO_SYNC=1`을 넣고 19행에서 `UV_CACHE_DIR` 지정만 뺌). **공용 도구 원본은 고치지 않았습니다.** uv 판이 그대로면 05절도 같은 사본이 필요합니다.
- `visual.cjs`도 `/tmp` 사본(`/tmp/ch12-04/vis12.cjs`)으로 돌렸습니다: `require('/tmp/pw/node_modules/playwright-core')`, `executablePath:'/tmp/pptr-cache/chrome/linux_arm-153.0.8010.36/chrome-linux-arm64/chrome'`·`args:['--no-sandbox']`, 출력 폴더를 `process.env.HOME` 기준으로, `ONLY` 필터와 병합 저장(02·03절과 같은 방법).
- **`uv run --project`를 부를 때 `UV_PROJECT_ENVIRONMENT`를 꼭 함께 주세요.** 04절 작업 첫머리에 그 변수 없이 한 번 불러 실습 폴더에 빈 기본 가상환경 `labs/part3/ch12-retrieval-tuning/.venv`가 만들어졌습니다(`site-packages`에 `_virtualenv.pth` 둘뿐, `.gitignore` 3행에 들어 있어 묶음·검사 대상은 아님). 정리 목록에 적어 두었습니다.

### 04절은 데이터베이스와 모델을 쓰지 않습니다

- 04절 노트북은 `kiwipiepy`·`rank_bm25`만 씁니다. `pre_exec.sh`가 켜 주는 pgvector 서버는 필요 없지만 `run_section.sh`가 늘 source 하므로 그대로 두었습니다(04절 출력에 영향 없음).
- 01~03절이 만든 표 `ch12_core_hnsw`·`ch12_core_filter`는 지우지 않고 남아 있습니다. 04절은 두 표를 읽지 않습니다.
- **API 키 셀을 두지 않았습니다.** 준비 셀은 설치 → import → 경로 찾기 → 자료 불러오기 네 개이고 `import os`는 import 셀에 있습니다. **05절은 임베딩을 다시 쓰므로 01~03절처럼 `nbkit.KEY` 셀을 되살려야 합니다.**

### 04절이 새로 가르친 것

- **kiwipiepy**: `Kiwi()` · `kiwi.tokenize(글)`(형태소 목록) · `token.form` · `token.tag`. 품사 표시 이름은 `keep_tags` 목록에 적고 `token.tag in keep_tags`로 고릅니다. **`str.startswith(튜플)`을 쓰지 않았습니다**(가르친 적 없는 모양이고 앞글자만 보면 대명사·보조 용언·서술격 조사까지 남습니다).
- **rank_bm25**: `BM25Okapi(낱말 목록의 목록)` · `get_scores(질문 낱말 목록)` · 속성 `corpus_size` · `avgdl`. 설치판 기본값 `k1 1.5`·`b 0.75`·`epsilon 0.25`는 소스로만 확인하고 교재에 싣지 않았습니다(식을 가르치지 않음).
- **정렬 방향 뒤집기**: 점수는 클수록 관련 있으므로 `(0 - 점수, 문서 ID)` 튜플을 담아 `sorted(목록)` 하고 꺼낼 때 다시 음수를 붙입니다. **`key=`·`reverse=`·`lambda`를 쓰지 않았습니다.**
- **Python 모양**: `글.split()`(Ch 8에서 배운 이름), 딕셔너리에 값으로 객체를 담아 `bm25_models[이름]`으로 고르기, 두 갈래를 `if`로 가르는 함수(`terms_by_policy`).
- **쓰지 않은 것**: `numpy`·`float()`·`sorted(key=)`·`reverse=`·기본값 매개변수·`str.startswith`·`sum`·`zip`·`enumerate`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`Path`·`hashlib`·`datetime`·`lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·f-string 안 계산·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`·`sorted`뿐입니다.

### 이어 쓸 이름과 값 (04절)

- 값: `keep_tags`(아홉 개 `["NNG", "NNP", "NNB", "NR", "VV", "VA", "MAG", "SN", "SL"]`) · `top_three`(3) · `cutoff_values`(`[1, 2, 3]`) · `policy_names`(**`["공백 분리", "Kiwi 형태소"]`**).
- 자료(01~03절과 같은 이름): `candidates` · `root_path` · `data_path` · `docs`(12) · `queries`(8) · `doc_texts` · `doc_ids`.
- 04절이 새로 만든 이름: `kiwi` · `sample_text`(`"예약자가 없으면 일반 도서를 연장할 수 있습니다."`) · `space_words` · `sample_tokens` · `sample_terms` · `kiwi_corpus` · `space_corpus` · `space_bm25` · `kiwi_bm25` · `bm25_models` · `keyword_query`(`queries[2]` = `C03`) · `keyword_terms` · `kiwi_hits` · `space_hits` · `score_rows`(16줄).
- 04절이 새로 만든 함수 여섯 개(괄호 안은 본문 줄 수): `kiwi_terms(text)`(3) · `count_docs_with(term)`(5) · `terms_by_policy(policy_name, text)`(3) · `rank_by_bm25(policy_name, question, top_count)`(7) · `print_scores(hit_list)`(2) · `score_one(query_index, policy_name)`(9).
- Ch 11·01~03절과 같은 코드로 다시 정의한 함수 네 개: `unique_doc_ids` · `find_gold_rank` · `recall_at` · `mean_score`. **`rank_by_bm25()`가 내는 목록(`{"doc_id": …, "점수": …}`)을 `unique_doc_ids()`에 그대로 넘길 수 있습니다**(보는 키가 `doc_id` 하나).
- **기록 한 줄의 칸 일곱 개**: `정책`·`질문`·**`1위 점수`**·`정답 자리`·`자리 1`·`자리 2`·`자리 3`. 03절의 `받아 온 줄 수` 자리에 `1위 점수`를 둔 모양입니다.
- **칸 이름 `점수`를 씁니다.** `거리`는 01~03절 이름이고 방향이 반대입니다. 출력 함수도 02·03절 `print_hits()`(칸 `거리`)와 가른 **`print_scores()`**(칸 `점수`)입니다. **05절이 두 검색을 한 표에 담으면 칸 이름을 `거리`와 `점수`로 갈라 두세요.**

### 출력 라벨 (04절 전부)

「kiwipiepy:」「rank-bm25:」「불러온 이름:」「고른 경로:」「문서 수:」「질문 수:」「남길 품사 표시:」「받아 올 줄 수:」「자르는 자리 세 가지:」「견줄 정책 두 가지:」「공백 분리로 만든 검색 낱말 수:」「공백 분리로 만든 검색 낱말:」「형태소 수:」「형태소 | 품사 표시」(라벨 줄 따로)「Kiwi 형태소로 만든 검색 낱말 수:」「Kiwi 형태소로 만든 검색 낱말:」「이어 붙인 글 수:」「첫 문서 ID:」「첫 문서 글:」「Kiwi 형태소 목록 수:」「공백 분리 목록 수:」「문서 ID | Kiwi 형태소 | 공백 분리」(라벨 줄 따로)「만든 모델 수:」「Kiwi 모델이 본 문서 수:」「문서 하나의 평균 검색 낱말 수:」「고른 질문:」「그 질문의 정답 문서 ID:」「질문의 검색 낱말:」「낱말 | 그 낱말이 있는 문서 수」(라벨 줄 따로)「쓴 정책:」「순위 | 문서 ID | BM25 점수」(라벨 줄 따로)「이 정책이 본 질문 낱말:」「담은 기록 줄 수:」「정책 | 질문 | 1위 점수 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율」(라벨 줄 따로)「정책 | 자르는 자리 | 질문 평균 재현율」(라벨 줄 따로)

### 실행값 (2026-09-18 마지막 새 커널, 두 실행이 같음)

- `kiwipiepy: 0.23.2` · `rank-bm25: 0.2.2` · `문서 수: 12` · `질문 수: 8`.
- 예로 쓴 문장: `공백 분리로 만든 검색 낱말 수: 7` · `형태소 수: 15` · `Kiwi 형태소로 만든 검색 낱말: ['예약', '없', '일반', '도서', '연장', '수', '있']`(개선 전 출력과 같음).
- 형태소 열다섯 줄 가운데 `예약 | NNG` · `자 | XSN` · `가 | JKS`가 앞 세 줄이고 `하 | XSV` · `ᆯ | ETM`이 열째·열한째 줄입니다. **낱말 `예약자`는 형태소로 남지 않습니다**(개선 전 본문이 「명사 `예약자`」로 적어 고쳤습니다).
- 문서별 검색 낱말 수 열두 줄: `LIB-001 | 17 | 17` · `LIB-002 | 12 | 14` · `LIB-003 | 14 | 15` · `LIB-004 | 15 | 14` · `FAC-001 | 21 | 17` · `FAC-002 | 16 | 14` · `FAC-003 | 16 | 14` · `FAC-004 | 14 | 13` · `ACC-001 | 14 | 13` · `ACC-002 | 16 | 15` · `ACC-003 | 15 | 15` · `ACC-004 | 14 | 15`. `문서 하나의 평균 검색 낱말 수: 15.33`.
- `C03` 낱말별 문서 수: `ISBN | 1` · `없 | 2` · `책 | 2` · `신청 | 2`.
- 실행 1(Kiwi 형태소, `C03`): `1 | LIB-003 | 6.34` · `2 | ACC-003 | 1.45` · `3 | LIB-004 | 1.45`. **둘째·셋째는 점수가 같아 문서 ID 차례로 정해진 자리입니다.**
- 값 바꿔 보기(공백 분리, `C03`): `이 정책이 본 질문 낱말: ['ISBN으로', '없는', '책을', '신청하려면?']`, 세 줄 모두 `0.0`(`ACC-001`·`ACC-002`·`ACC-003`).
- 기록 열여섯 줄(정답 자리는 상위 3개 안에서만 셉니다): 공백 분리 `C01` 2 · `C02` 0 · `C03` 0 · `C04` 1 · `C05` 0 · `C06` 1 · `C07` 1 · `C08` 3, Kiwi 형태소는 `C01` 3과 나머지 1. 1위 점수는 공백 분리 `2.58`·`0.0`·`0.0`·`1.9`·`0.0`·`3.02`·`2.5`·`0.0`, Kiwi 형태소 `3.37`·`2.26`·`6.34`·`8.18`·`3.41`·`2.99`·`8.73`·`4.99`.
- 질문 평균 재현율: 공백 분리 자리 1 `0.375` · 자리 2 `0.5` · 자리 3 `0.625`, Kiwi 형태소 자리 1 `0.875` · 자리 2 `0.875` · 자리 3 `1.0`.

### 05절이 01·04절 값과 견줄 수 있는 자리 (중요)

- **01절 코사인 거리와 04절 Kiwi 형태소는 같은 문서 12개·같은 질문 8개·같은 자르는 자리·같은 후보 단위(문서 한 건)를 씁니다.** 그래서 **질문 평균 재현율 세 값을 그대로 견줄 수 있습니다**: 01절 코사인 `0.75`·`0.875`·`0.875` 대 04절 Kiwi `0.875`·`0.875`·`1.0`.
- 자리 3에서 갈리는 질문은 **`C02`**(「책을 늦게 반납하면 돈을 내나요?」, 정답 `LIB-002`)입니다. 01절 코사인에서 `C02`의 정답 자리는 **7**이고 04절 Kiwi에서는 **1**입니다. 개선 전 05절이 적은 「dense 7/8 · sparse 8/8」과 「성공 여부가 다른 질문: `['C02']`」가 새 출력에서도 그대로입니다.
- **`정답 자리` 칸의 뜻은 다릅니다.** 01절은 문서 12개를 모두 재어 자리가 최대 12이고, 03·04절은 상위 3개만 담아 자리가 0~3입니다. **재현율 세 값은 같은 뜻이고 `정답 자리`만 범위가 다르니 한 표에 섞을 때 칸 이름을 가르세요.**
- `C01`에서는 두 검색의 상위 3개가 **같은 문서 세 건이고 순서만 다릅니다**: 01절 코사인 `LIB-004`·`LIB-001`·`LIB-003`, 04절 Kiwi `LIB-004`·`LIB-003`·`LIB-001`. 개선 전 05절 출력과 같습니다.
- `C03`에서는 둘째 자리만 다릅니다: 개선 전 05절 dense `LIB-003`·`ACC-002`·`LIB-004`, 04절 Kiwi `LIB-003`·`ACC-003`·`LIB-004`. **04절 둘째·셋째는 점수가 같은 자리라 순서를 결과로 읽지 마세요.**
- **Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과는 나란히 놓지 않습니다**(01절 b7에 이미 있는 문장이라 되풀이하지 않았습니다).

### 흔들리는 값 — 04절에는 없습니다

- Kiwi 형태소 분석과 BM25 점수는 같은 입력에 같은 값을 냅니다. 두 실행의 셀별 출력 글자가 모두 같았습니다. 그래서 **점수 값을 그림 라벨에 넣었습니다**(`6.34`·`0.0`·질문 평균 여섯 값). 01~03절 거리는 소수 셋째 자리가 흔들려 라벨에서 뺐습니다 — **05절이 두 값을 한 그림에 담으면 거리는 라벨에서 빼고 점수만 넣으세요.**
- **점수가 모두 같은 자리를 결과로 읽지 않습니다.** 공백 분리 여덟 줄 가운데 네 줄(`C02`·`C03`·`C05`·`C08`)의 1위 점수가 `0.0`이고, 그때 순서는 BM25가 아니라 이 절 코드의 정렬 규칙(문서 ID 차례)이 정합니다. `C08`의 정답 자리 3이 그 자리입니다(b4·b6·b7과 노트북 9·10·12절에 적음). 05절도 점수 `0.0`이 나오면 같은 문장을 쓰세요.
- 공백 분리 쪽은 낱말 정책을 보이기 위한 견줄 대상입니다. **05절에서 견줄 것은 「벡터 거리 검색 대 낱말 겹침 검색」이므로 공백 분리 쪽을 다시 싣지 않아도 됩니다.**

### 용어 (04절이 더한 일곱 개, 05~12도 같게)

- **형태소(morpheme)** · **형태소 분석기(morphological analyzer)** · **품사 표시(part-of-speech tag)** · **검색 낱말** · **낱말 정책** · **BM25** · **낱말 겹침 검색(sparse retrieval)**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 6 → **7**」로 고쳤습니다.
- **본문에서 「토큰」을 쓰지 않았습니다.** 「조각」은 Ch 5 토큰 뜻 전용이므로(규격 §4) Kiwi 결과는 **형태소**, BM25에 넣는 항목은 **검색 낱말**, 만드는 방법은 **낱말 정책**으로 부릅니다. 개선 전 b1·b3·b7의 「토큰 정책」·「검색 토큰」을 모두 바꿨습니다.
- **「점수」는 클수록 관련 있는 값**입니다(BM25). **「거리」는 01~03절 뜻 그대로 작을수록 가까운 값**입니다. 한 줄에 나란히 놓지 않습니다.
- **「정책」**은 검색 낱말을 만드는 방법을 가리킵니다. 02·03절 **「경로」**(표를 읽는 방법)와 다른 말이니 섞지 마세요.
- 01~03절 말 열여덟 개(L2 거리·코사인 거리·정확 검색·근사 검색·단위 길이 벡터·pgvector·HNSW·거리 연산자 `<=>`·연산자 클래스·실행 계획·순차 스캔·`ef_search`·`halfvec`·메타데이터 필터·나중 걸러 내기·선택도·반복 탐색·채움 행)와 Ch 9~11 말을 그대로 씁니다.
- 쓰지 않은 말: 「토큰」·「토큰화」(→ 낱말 정책·검색 낱말 만들기), 「조각」(Ch 5 전용), 한정어 없는 「청크」, 「희귀도」·「역문서빈도」(→ 「그 낱말이 있는 문서 수」), 「말뭉치」 단독(→ 문서 12개 또는 검색 낱말 목록), 「sparse」 단독(→ 낱말 겹침 검색), 「top-3」(→ 상위 3개), 「Recall@3」(→ 자리 3 재현율), 「임계값」.

### 파일 쓰기 규칙 — 04절도 파일을 쓰지 않습니다

- `runs/core-04-bm25.json`은 작업 전후 `e5405673f7efcd5188ad1586ac18fdcb68fcc10fb6e6999097692a4b62d97f00` 그대로이고 `runs/core-history/before-e5405673f7ef-core-04-bm25.json`과 바이트가 같습니다. `runs/` 36개 묶음 해시 `a9c5d35a40a8acc0…`도 작업 전후 같고 `core-history/`는 12개입니다.
- **05절 결정 사항**: 개선 전 05 노트북 마지막 두 셀이 `runs/core-05-dense-sparse.json`을 덮어씁니다(`Path`·`hashlib`·`datetime`·세미콜론·한 줄 복합문). 읽는 쪽은 `check_course_continuity.py` 187~196행 하나이고 바이트만 봅니다. **01~04절 선례대로 쓰지 않는 쪽을 먼저 검토하세요.**
- `advanced-queries.json`·`advanced-documents.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않습니다.
- 실습 폴더 테스트는 작업 전후 **4 passed**입니다. `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…`도 그대로입니다. 04절 `%pip` 목록 두 개(`kiwipiepy==0.23.2`·`rank-bm25==0.2.2`)는 잠금 112·120행에 있고 dev `pip==26.2`도 128·1142행에 있습니다(그 `.venv`에서 `import pip`이 `26.2`).
- 공용 화면 검사 결과 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`은 **26행을 유지**해야 합니다(`finalize_continuity_evidence.py` 15행). 04절은 `/tmp/ch12-04/vis12.cjs` 사본으로 04절 두 줄만 다시 찍었고 결과 값이 같아 파일 바이트가 `49352bfcd3f7e511…`로 그대로입니다.

### 05절이 이어받을 연결과 확인할 것

- 04 b8·노트북 정리 끝: 「05절에서는 같은 질문 여덟 개에서 벡터 거리 검색과 낱말 겹침 검색의 결과를 나란히 놓습니다. 두 검색이 서로 다른 문서를 고르는 자리를 찾습니다.」
- **개선 전 05 노트북이 하는 일**: 01절과 같은 임베딩(`dimensions=256`)으로 dense 순위를, 04절과 같은 Kiwi+BM25로 sparse 순위를 내고 질문 8개의 Recall@3을 견줍니다. `queries[0]`(`C01`)과 `queries[2]`(`C03`) 두 질문을 자세히 보고, 마지막에 `runs/core-05-dense-sparse.json`을 씁니다.
- **개선 전 05 노트북이 쓰는 것 가운데 01~04절에서 안 가르친 것**: `numpy`(`np.array`·`np.argsort`·`np.linalg.norm`·`@`), 내포식 네 곳, `lambda`·`key=`·`reverse=`, 기본값 매개변수 `k=3`, `zip(queries, query_vectors)`, `sum(...)`으로 참 개수 세기, f-string, 세미콜론 두 곳(`kiwi = Kiwi(); keep = (...)`), 한 줄에 문장 두 개(`dense = dense_rank(vector); sparse = sparse_rank(...)`), `str.startswith(튜플)`, `Path`·`hashlib`·`datetime`.
  - **dense 쪽은 01절 함수 네 개로 바꿀 수 있습니다**(`dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`). 01절 `rank_by_distance()`와 04절 `rank_by_bm25()`가 같은 모양의 목록을 내므로 `unique_doc_ids()`에 둘 다 넘길 수 있습니다.
  - **sparse 쪽은 04절 코드를 그대로 가져오면 됩니다**(`kiwi_terms`·`rank_by_bm25`·`print_scores`). 다만 `rank_by_bm25()`는 `bm25_models` 딕셔너리를 보므로 05절에서 정책이 하나뿐이면 모델 하나를 받는 모양으로 줄일지 정하세요.
- **임베딩 요청**: 01~03절과 같은 아홉 번(문서 1 + 질문 8)이면 됩니다. 04절은 0번이었으니 05절 준비물의 호출 수·비용을 다시 적으세요. **`nbkit.KEY` 셀을 되살려야 합니다.**
- **두 검색의 칸 이름**: dense는 `거리`, sparse는 `점수`입니다. 한 표에 담으면 칸을 갈라 두고 「거리는 작을수록 가깝고 점수는 클수록 관련 있다」를 한 문장으로 적으세요(04절 b3·b7과 같은 문장).
- **개선 전 05절 본문에 실행하지 않은 주장이 있는지 확인하세요.** 04절에서는 `ts_rank` 문장을 「확인하지 않았습니다」로 바꿨습니다.
- **아직 안 가르친 것(05가 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01·02·03절 목록에 더해, 04절에서도 하지 않은 것 — 품사 표시를 바꿔 견주기, 사용자 사전·복합명사 나누기 설정, 불용어 목록, BM25 설정 `k1`·`b` 바꾸기, 다른 BM25 판(`BM25Plus`·`BM25L`), 두 점수를 하나로 합치기(RRF는 06절), 점수를 0에서 1로 맞추기, 검색에 걸린 시간 재기, 데이터베이스 전문 검색 함수 실행, 큰 말뭉치에서 재현율 재기, 정밀도·nDCG 계산(Ch 11에서 배웠지만 01~04절은 재현율만), 재정렬, MMR, 질문 재작성, 답을 쓰는 모델 호출(11·12절).

## §05 → §06

(05절 품질 개선 2026-09-18. 결과는 `05-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 58 = G1 11·G2 10·G3 9·G4 0·G5 13·G6 12·G7 3), 코드 셀 30(준비 5), 검사 문장 307, **임베딩 요청 9번**(문서 1 + 질문 8, 0.01달러 아래), 답을 쓰는 모델 0번. 새 커널 다섯 번 실행에 `code_sha256` `9210ae09d7acd4c7…`와 셀별 출력 글자 해시 `21d15271d6bfd98d…`가 모두 같고 교재 출력은 마지막 실행 2026-09-18T17:48:05Z. `verify.py --chapter` `PASS 12 sections / 222 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(1차 job `7955a20b-3f68-4724-bc17-cd222e49ab78` 채택, 2크레딧, 생성 뒤 잔액 2729))

### 작업 환경 — `run_section.sh` 사본이 아직 필요합니다 (먼저 읽을 것)

- 원본 `run_section.sh`는 `.cache/vm` 환경에서 **`UV_NO_SYNC=1`을 이미 줍니다**(17행). 04절이 사본을 만든 두 까닭 가운데 uv sync 실패는 해소되었습니다.
- 그런데 원본은 `UV_CACHE_DIR="$VM/uv"`도 함께 export 합니다. `--with`로 만드는 덧붙임 환경이 그 캐시 폴더 안 임시 폴더를 지우려다 마운트 폴더의 삭제 금지에 걸립니다: `failed to remove directory .cache/vm/uv/builds-v0/.tmpXXXX/…: Operation not permitted`. **그래서 05절도 `UV_CACHE_DIR` 지정만 뺀 `/tmp` 사본으로 돌렸습니다**(`/tmp/ch12-05/run_section.sh`, 원본에서 한 줄만 고침). 공용 도구 원본은 고치지 않았습니다. uv 판이 `0.12.13`인 동안 06절도 같은 사본이 필요합니다.
- `uv run --project`를 직접 부를 때도 `UV_CACHE_DIR=/tmp/uv-cache`와 `UV_PROJECT_ENVIRONMENT="$ROOT/.cache/vm/venv-ch12-retrieval-tuning"`·`UV_NO_SYNC=1`을 함께 주세요. 실습 폴더에 빈 `.venv`가 생기는 사고를 막습니다(04절 기록).
- `visual.cjs`는 04절과 같은 `/tmp` 사본(`/tmp/ch12-05/vis12.cjs`, `ONLY` 필터와 병합 저장)으로 돌렸습니다. `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/pw`·`/tmp/libs`는 04절이 다시 설치한 그대로 남아 있습니다. 루트 디스크 여유는 3.6G였습니다.
- 05절은 pgvector 서버를 쓰지 않습니다(`pre_exec.sh`가 켜도 출력에 영향 없음). 01~03절 표 `ch12_core_hnsw`·`ch12_core_filter`는 남아 있고 05절은 읽지 않았습니다.
- **`outputs_sha256`을 그대로 믿지 마세요.** 다섯 번 실행 가운데 3회만 `eb4a2360c72bd631…`이 나왔고 나머지는 `5c061480b0a48b63…`였습니다. 차이는 `%pip` 셀의 출력이 스트림 두 조각으로 나뉜 것이고 **출력 글자는 같습니다**. 셀별 출력 글자를 이어 붙여 해시하면 같습니다(`/tmp/ch12-05/celltext.py`). 06절도 셀별 출력 글자로 대조하세요.

### 05절이 새로 가르친 것

- **새 API는 없습니다.** 01절 함수 네 개(`dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`)와 04절 `kiwi_terms`·`BM25Okapi`·`get_scores`, Ch 11 지표 함수 네 개를 같은 코드로 다시 정의했습니다.
- **같은 조건에서 두 방법을 견주는 방법**: 문서·질문·후보 단위·자르는 자리·지표 함수 다섯 가지를 같게 두고, 값 칸 이름만 `거리`와 `점수`로 갈라 둡니다(b4 「같게 두어야 하는 다섯 가지」).
- **정답 자리 범위를 맞추는 방법**: 두 방법 모두 `top_all = 12`로 문서를 끝까지 재어 자리를 1~12로 셉니다. 03·04절 표(상위 3개만 담아 0~3)와 범위가 다르다는 문장을 b3·b7에 적었습니다.
- **Python 모양**: 값 칸 이름을 인자로 받는 출력 함수(`print_ranked(hit_list, value_name)`, `row[value_name]`), 순위 목록을 인자로 받는 채점 함수(`score_one(query_index, method_name, hit_list)`), 두 방법을 가르는 `if`를 기록 반복문 안에 한 번만 두기.
- **쓰지 않은 것**: `numpy`·`lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`index`·`Path`·`hashlib`·`datetime`·f-string·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`·`sorted`뿐입니다.

### 이어 쓸 이름과 값 (05절)

- 값: `similarity_top`(1) · `top_three`(3) · **`top_all`(12)** · `cutoff_values`(`[1, 2, 3]`) · `keep_tags`(아홉 개) · **`method_names`(`["벡터 거리", "낱말 겹침"]`)**.
- 자료(01~04절과 같은 이름): `candidates` · `root_path` · `data_path` · `docs`(12) · `queries`(8) · `doc_texts` · `doc_ids` · `embedding_model_name` · `vector_dimensions`(256) · `embedding_model` · `doc_vectors` · `query_vectors` · `kiwi` · `kiwi_corpus` · **`bm25_model`**(04절 `bm25_models` 딕셔너리를 모델 하나로 줄인 이름).
- 05절이 새로 만든 이름: `first_query`·`first_terms`·`first_distance_hits`·`first_score_hits` · `second_query`·`second_terms`·`second_distance_hits`·`second_score_hits` · `second_gold_terms`·`shared_terms` · `score_rows`(16줄) · `places`(질문 하나의 두 자리).
- 05절이 새로 만든 함수 다섯 개(괄호 안은 본문 줄 수): `rank_by_distance(question_vector, top_count)`(8, `{"doc_id": …, "거리": …}` 목록) · `rank_by_bm25(question, top_count)`(9, `{"doc_id": …, "점수": …}` 목록) · `print_ranked(hit_list, value_name)`(4) · `score_one(query_index, method_name, hit_list)`(8) · 그리고 `kiwi_terms(text)`(5, 04절과 같은 코드).
- **기록 한 줄의 칸 일곱 개**: `방법`·`질문`·**`갈래`**(질문 파일 `kind`)·`정답 자리`·`자리 1`·`자리 2`·`자리 3`. 04절의 `1위 점수` 자리에 값 칸을 두지 않았습니다(거리와 점수를 한 칸에 섞지 않으려고).
- **`unique_doc_ids()`가 두 함수의 목록을 모두 받습니다**(보는 키가 `doc_id` 하나). 06절이 RRF에 넣을 **순위대로 된 문서 ID 목록**은 `unique_doc_ids(rank_by_distance(벡터, 후보 수))`로 바로 얻을 수 있습니다.

### 출력 라벨 (05절 전부)

「langchain-openai:」「python-dotenv:」「kiwipiepy:」「rank-bm25:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「문서 수:」「질문 수:」「코사인 유사도의 가장 큰 값:」「나란히 볼 상위 문서 수:」「자리를 셀 때 재는 문서 수:」「자르는 자리 세 가지:」「남길 품사 표시:」「견줄 방법 두 가지:」「이어 붙인 글 수:」「첫 문서 글:」「문서 ID 목록:」(라벨 줄 따로)「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 벡터 수:」「질문 벡터 수:」「검색 낱말 목록 수:」「BM25 모델이 본 문서 수:」「문서 하나의 평균 검색 낱말 수:」「고른 질문:」「그 질문의 정답 문서 ID:」「질문의 갈래:」「질문의 검색 낱말:」「순위 | 문서 ID | 거리」(라벨 줄 따로)「순위 | 문서 ID | 점수」(라벨 줄 따로)「정답 문서의 검색 낱말:」「질문과 정답 문서에 함께 있는 낱말:」「함께 있는 낱말 | 그 낱말이 있는 문서 수」(라벨 줄 따로)「담은 기록 줄 수:」「방법 | 질문 | 갈래 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율」(라벨 줄 따로)「방법 | 자르는 자리 | 질문 평균 재현율」(라벨 줄 따로)「질문 | 벡터 거리 자리 | 낱말 겹침 자리」(라벨 줄 따로)

### 실행값 (2026-09-18 마지막 새 커널, 다섯 실행이 같음)

- `문서 수: 12` · `질문 수: 8` · `벡터의 숫자 개수 설정: 256` · `문서 벡터 수: 12` · `질문 벡터 수: 8` · `검색 낱말 목록 수: 12` · `문서 하나의 평균 검색 낱말 수: 15.33`(04절과 같음).
- 실행 1(`C01`, 갈래 `semantic`, 정답 `LIB-001`): 벡터 거리 `1 | LIB-004 | 0.43`·`2 | LIB-001 | 0.56`·`3 | LIB-003 | 0.62`(01·02·03절과 같은 값), 낱말 겹침 `1 | LIB-004 | 3.37`·`2 | LIB-003 | 2.59`·`3 | LIB-001 | 2.01`. **상위 3개가 같은 문서 세 건이고 순서만 다릅니다.**
- 값 바꿔 보기(`C02`, 갈래 `semantic`, 정답 `LIB-002`): 벡터 거리 `1 | LIB-003 | 0.56`·`2 | LIB-004 | 0.58`·`3 | LIB-001 | 0.65`(정답 문서 없음), 낱말 겹침 `1 | LIB-002 | 2.26`·`2 | LIB-003 | 2.11`·`3 | LIB-004 | 1.45`.
- `질문의 검색 낱말: ['책', '늦', '반납', '돈', '내']` · `질문과 정답 문서에 함께 있는 낱말: ['반납']` · `반납 | 1`.
- 기록 열여섯 줄. 정답 자리는 벡터 거리 `C01` 2 · `C02` 7 · 나머지 1(**01절 표와 같음**), 낱말 겹침 `C01` 3 · 나머지 1(**04절 표와 같음**). 갈래는 `C03`·`C04`·`C07`이 `keyword`이고 나머지 다섯이 `semantic`입니다.
- 질문 평균 재현율: 벡터 거리 `0.75`·`0.875`·`0.875`, 낱말 겹침 `0.875`·`0.875`·`1.0`. **자리 2에서 두 값이 같습니다.**
- 정답 자리가 다른 질문 두 줄: `C01 | 2 | 3` · `C02 | 7 | 1`. **두 방법이 서로 이기는 질문이 하나씩 있습니다.**

### 흔들리는 값과 결론 한정 — 06절도 같은 규칙으로

- 거리는 소수 셋째 자리 아래가 실행마다 흔들립니다(01절). **소수 둘째 자리까지만 출력하고 그림 라벨에 넣지 않습니다.** BM25 점수는 다섯 실행에서 같았지만 `05-2`는 두 칸을 나란히 두므로 점수도 라벨에서 뺐습니다. 한쪽 칸에만 값이 있으면 방향이 반대인 두 값을 견주는 것처럼 보입니다.
- **어느 방법이 나은지 판정하지 않았습니다.** 평균은 낱말 겹침이 높지만 `C01`에서는 벡터 거리 쪽 자리가 앞입니다. 04절의 「형태소가 늘 앞선다고 쓰지 않음」과 같은 태도입니다.
- **갈래로 방법을 고르지 않습니다.** 갈린 두 질문의 갈래가 모두 `semantic`이고 갈래별 질문 수가 5와 3이라 갈래 평균은 내지 않았습니다.
- 벡터 거리 쪽이 `C02` 정답 문서를 일곱째 자리에 둔 까닭은 「이번에 확인하지 않았습니다」로 적었습니다(모델 안을 볼 수 없음).
- Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과 나란히 놓지 않습니다(01절 b7에 이미 있는 문장이라 되풀이하지 않음).

### 용어 (05절이 더한 네 개, 06~12도 같게)

- **벡터 거리 검색(dense retrieval)** · **말 바꾼 질문(semantic variation)** · **낱말 일치(lexical match)** · **점수 방향**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 4」 그대로입니다.
- **두 방법의 이름을 정했습니다**: 01~03절 방법은 **「벡터 거리 검색」**, 04절 방법은 **「낱말 겹침 검색」**(04절이 정한 말)입니다. 기록 칸의 값은 짧게 `벡터 거리`·`낱말 겹침`입니다. 영문 `dense`·`sparse`는 용어 표 괄호에 한 번만 적었고 본문에서 단독으로 쓰지 않았습니다. 절 제목 「dense와 sparse 비교」는 `chapter.json` 제목·파일 이름이라 그대로 두었습니다(03절 「iterative scan」과 같은 처리).
- **「갈래」**는 질문 파일 `kind` 칸을 가리키는 말로 씁니다(값 `semantic`·`keyword`는 출력이라 그대로 인용). 02·03절 「경로」, 04절 「정책」과 다른 말입니다.
- **「방법」**은 이 절에서 견주는 두 검색을 가리킵니다. 기록 칸 이름도 `방법`입니다.
- 01~04절 말 스물다섯 개와 Ch 9~11 말을 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**이고 본문에 「토큰」·한정어 없는 「청크」를 쓰지 않았습니다.
- 쓰지 않은 말: 「dense」·「sparse」 단독, 「의미 변형」·「어휘 일치」(→ 말 바꾼 질문·낱말 일치), 「Recall@3」(→ 자리 3 재현율), 「top-3」·「top-k」(→ 상위 3개·자르는 자리), 「P@5」·「nDCG@5」(→ 정밀도·nDCG, 이 절은 재지 않음), 「검색기」(→ 검색 방법), 「원점수」(→ 값 또는 점수), 「척도」(→ 값의 크기), 「임계값」.

### 파일 쓰기 규칙 — 05절도 파일을 쓰지 않습니다

- `runs/core-05-dense-sparse.json`은 작업 전후 `ee06e48ac32d706c9078b4dd2d4ef4937e8198f7a132cca3a523ce490f3e4669` 그대로이고 `runs/core-history/before-ee06e48ac32d-core-05-dense-sparse.json`과 바이트가 같습니다. `runs/`는 36개 파일, `core-history/`는 12개 그대로입니다.
- **01~04절 진단이 적은 `runs/` 묶음 해시 `a9c5d35a40a8acc0…`는 파일 경로가 든 방식으로 낸 값이라 세션마다 마운트 경로가 달라져 재현되지 않습니다.** 05절은 **파일 내용만 이어 붙인 해시 `d3d6478c0790e11e045c518edd1356e20c29ce0d33156722221fc5947e4a107a`**와 개별 파일 해시로 대조했습니다. 개별 해시는 01~04절 기록과 모두 같습니다(`core-01` `f8e81361e9c79fa5…` · `core-02` `e007a959899ec0ea…` · `core-03` `4d9be88254b631d3…` · `core-04` `e5405673f7efcd51…` · `core-05` `ee06e48ac32d706c…` · `core-06` `4e3fa11084a4a09e…`).
- **06절 결정 사항**: 개선 전 06 노트북 마지막 두 셀이 `runs/core-06-rrf.json`을 덮어씁니다. 정본 바이트 `4e3fa11084a4a09e5839c43c82786269f5a0a4e0b0aab0df490f0b044c511369`가 `before-4e3fa11084a4-core-06-rrf.json`과 같습니다. 읽는 쪽은 `check_course_continuity.py` 187~196행 하나이고 바이트만 봅니다. **01~05절 선례대로 쓰지 않는 쪽을 먼저 검토하세요.**
- `advanced-queries.json`·`advanced-documents.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않습니다.
- 실습 폴더 테스트는 작업 전후 **4 passed**입니다. `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…`도 그대로입니다. 05절 `%pip` 목록 네 개(`langchain-openai==1.6.1`·`python-dotenv==1.2.3`·`kiwipiepy==0.23.2`·`rank-bm25==0.2.2`)는 모두 잠금 112~120행에 있고 dev `pip==26.2`도 그대로입니다(확인만 했습니다).
- 공용 화면 검사 결과 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`은 **26행을 유지**해야 합니다(`finalize_continuity_evidence.py` 15행). 05절은 `/tmp/ch12-05/vis12.cjs` 사본으로 05절 두 줄만 다시 찍었고 값이 같아 파일 바이트가 `49352bfcd3f7e511…`로 그대로입니다.
- 검사 스크립트가 멈추는 자리는 01절 기준과 같습니다: `textbook/part3/qa/check_continuity.py` 154행 `part2-practice.zip`, `textbook/qa/check_course_continuity.py` 212행 `part1-practice.zip`, `textbook/part3/qa/check_delivery.py`는 끝까지 통과.

### 06절이 이어받을 연결과 확인할 것

- 05 b8·노트북 정리 끝: 「06절에서는 두 순위를 하나로 합칩니다. 점수를 더하지 않고 자리 번호만 써서 합치는 방법을 씁니다.」 06절 `_src` b2와 노트북 `rrf()`를 열어 `weight / (rank_constant + rank)`로 자리 번호만 쓰는 것을 확인하고 쓴 문장입니다.
- **개선 전 06 노트북이 하는 일**: 05절과 같은 준비 셀을 다시 쓰고 `dense_rank(벡터, 6)`·`sparse_rank(질문, 6)`으로 후보 여섯 개를 받아 `rrf([dense, sparse])`로 상위 3개를 냅니다. 이어서 문서마다 두 순위와 RRF 점수를 출력하고, sparse 가중치만 `1.0` → `1.5`로 바꿔 결과를 견줍니다. 마지막에 질문 8개의 Recall@3을 세고 `runs/core-06-rrf.json`을 씁니다.
- **개선 전 06 노트북의 출력(참고용, 다시 실행하면 확인할 값)**: `dense: ['LIB-003', 'ACC-002', 'LIB-004', 'ACC-004', 'ACC-003', 'LIB-001']` · `sparse: ['LIB-003', 'ACC-003', 'LIB-004', 'ACC-002', 'LIB-001', 'LIB-002']` · `RRF: ['LIB-003', 'ACC-002', 'LIB-004']`(질문 `C03`), 문서별 줄 `LIB-003 dense 순위 1 sparse 순위 1 RRF 점수 0.03279`, 가중치 바꿔 보기 `sparse 1.5: ['LIB-003', 'LIB-004', 'ACC-003']`, 마지막 `dense Recall@3: 7 / 8` · `sparse Recall@3: 8 / 8` · **`rrf Recall@3: 7 / 8`**.
- **가장 큰 주의: 합치면 좋아진다고 쓰지 마세요.** 개선 전 출력에서 RRF는 낱말 겹침보다 낮았습니다(7/8 대 8/8). 05절 값으로는 낱말 겹침 자리 3 재현율이 `1.0`이라 RRF가 그보다 높아질 수 없습니다. 다시 실행해 나온 값을 그대로 쓰고 「이번 실행에서는」으로 한정하세요.
- **개선 전 06 노트북이 쓰는 것 가운데 01~05절에서 안 가르친 것**: `numpy`, 내포식 네 곳, 제너레이터 식 한 곳, `sorted(scores, key=scores.get, reverse=True)`, 기본값 매개변수 세 개(`weights=None`·`rank_constant=60`·`k=3`), `weights or [1.0] * len(rankings)`, `enumerate(ranking, start=1)`, `zip(rankings, weights)`, 조건 표현식(`… if doc_id in dense else None`), `목록.index(값)`, `sum(...)`으로 참 개수 세기, f-string, 세미콜론 두 곳, 한 줄에 문장 두 개, `Path`·`hashlib`·`datetime`.
  - **정렬**: 04·05절이 쓴 「점수에 음수를 붙여 `sorted(목록)`」 모양을 그대로 쓸 수 있습니다(`key=`·`reverse=`를 쓰지 않음).
  - **딕셔너리 누적**: `scores.get(키, 0.0) + 값`은 Ch 2 03절과 Part 2에서 배운 모양이라 그대로 쓸 수 있습니다.
  - **순위 번호**: `enumerate` 대신 `for position in range(len(목록))` + `position + 1`을 쓰면 01·05절 `find_gold_rank()`와 같은 모양이 됩니다.
  - **숫자를 식 안에 바로 쓰지 않기**(규격 §2-3): `rank_constant = 60`처럼 이름을 먼저 만드세요. 규격 §4에 이 절을 예로 든 수식 설명 순서가 있습니다: 「순위가 높을수록 큰 점수를 줍니다. 식은 `weight / (60 + 순위)`입니다. 1위 문서는 `1 / (60 + 1)`로 약 0.0164점을 받습니다.」 그 세 문장 순서(말 → 식 → 숫자 대입)를 본문에 쓰세요.
  - **가중치 문장**(규격 §4 예시): 「단어 검색(sparse)의 가중치를 높여도 BM25 점수는 그대로입니다. 결합 점수에서 단어 검색 순위가 차지하는 몫만 커집니다.」를 이 챕터 말(낱말 겹침 검색)로 바꿔 쓰세요.
- **05절 함수를 그대로 이어 쓸 수 있습니다**: `rank_by_distance(벡터, 후보 수)`·`rank_by_bm25(질문, 후보 수)`가 순위 목록을 내고 `unique_doc_ids()`가 그것을 **순위대로 된 문서 ID 목록**으로 바꿉니다. RRF에 넣을 재료가 바로 그 목록입니다. 지표 함수 네 개와 `score_one()`의 모양(`방법` 칸에 `RRF`를 더한 세 값)도 이어 쓸 수 있습니다.
- **후보 수와 자르는 자리를 분명히 두세요.** 개선 전 06은 후보 여섯 개를 받아 상위 3개로 줄였습니다. 05절은 `top_all = 12`로 재어 정답 자리를 1~12로 셌습니다. **06절에서 후보를 여섯 개로 자르면 RRF 쪽 정답 자리 범위가 다시 달라집니다.** 05절처럼 세 방법을 모두 같은 범위로 재거나, 범위가 다른 까닭을 본문에 적으세요.
- **06절은 core 벌(문서 12개·질문 8개)의 마지막 절입니다.** 07절부터 `advanced-documents.json`(부모 6건·문서 청크 175개)과 `advanced-queries.json`(질문 30개, Ch 11 평가셋과 같은 파일)을 씁니다. 07절을 만들 때 Ch 11 요약 §11-1의 약속(**개발 15문항으로 고르고 시험 15문항은 마지막 한 번**)을 처음 쓰는 자리에서 인용하세요.
- **아직 안 가르친 것(06이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01~04절 목록에 더해, 05절에서도 하지 않은 것 — 두 순위를 합치기(06절 몫), 점수를 0에서 1로 맞추기, 가중치 고르기, 정밀도·nDCG 계산(Ch 11에서 배웠지만 01~05절은 재현율만), 점수 기준값·거르기, 검색에 걸린 시간 재기, 큰 말뭉치에서 재현율 재기, 데이터베이스 전문 검색 함수, 품사 표시·BM25 설정(`k1`·`b`) 바꿔 보기, 다른 BM25 판, 다른 임베딩 모델·차원 수, 문서 청크로 나누기, 재정렬(07·08절), MMR(10절), 질문 재작성(11절), 답을 쓰는 모델 호출(11·12절).

## §06 → §07

(06절 품질 개선 2026-09-18. 결과는 `06-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 66 = G1 12·G2 11·G3 9·G4 0·G5 13·G6 18·G7 3), 코드 셀 31(준비 5), 검사 문장 331, **임베딩 요청 9번**(문서 1 + 질문 8, 0.01달러 아래), 답을 쓰는 모델 0번. 새 커널 두 번 실행에 `code_sha256` `28482c02e3d93ff6`·셀별 출력 글자 해시 `7422bdabeab7e81e…`·`outputs_sha256` `c6fd288f4c365103`가 모두 같고 교재 출력은 마지막 실행 2026-09-18T18:19:58Z. `verify.py --chapter` `PASS 12 sections / 244 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(2차 job `87fe07ed-5750-4f5f-8d16-c6dc0761dd4b` 채택, 1차 `3e4c1f98-…` 탈락, 4크레딧, 생성 전 잔액 2729))

### 작업 환경 — `run_section.sh` 사본이 더는 필요 없습니다 (먼저 읽을 것)

- **원본 `run_section.sh`를 그대로 썼고 두 번 다 끝까지 돌았습니다.** 원본 14행이 `UV_CACHE_DIR=/tmp/uv-cache`를 주고 `.cache/vm` 분기(17~23행)가 그 값을 덮어쓰지 않도록 고쳐져 있습니다. 04·05절이 만든 `/tmp/ch12-0N/run_section.sh` 사본은 07절에서 필요하지 않습니다.
- `visual.cjs`만 `/tmp` 사본이 필요합니다(`/tmp/ch12-06/vis12.cjs`, 05절 사본을 그대로 복사). `ONLY` 필터와 병합 저장이 들어 있어 `ONLY=07- node /tmp/ch12-06/vis12.cjs textbook/part3/ch12-retrieval-tuning`으로 해당 절 두 줄만 갱신합니다.
- `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/pw`·`/tmp/libs`·`/tmp/uv-cache`는 04절이 다시 설치한 그대로 남아 있습니다. 루트 디스크 여유는 3.5G였습니다.
- 06절은 pgvector 서버를 쓰지 않습니다(`pre_exec.sh`가 켜도 출력에 영향 없음). 01~03절 표 `ch12_core_hnsw`·`ch12_core_filter`는 남아 있고 06절은 읽지 않았습니다.
- **`outputs_sha256`은 이번에도 그대로 믿지 마세요.** 06절은 두 번 다 같았지만 05절에서 `%pip` 셀 출력이 스트림 조각으로 나뉘어 달라진 적이 있습니다. 셀별 출력 글자로 대조하세요(`/tmp/ch12-06/celltext.py`, 05절 판과 같은 방법).
- 삽화는 클라우드 컨테이너에서 결과 URL을 `curl`로 받아 눈으로 보고, 저장은 기기 셸에서 `curl` + `uv run --with pillow`로 폭 1100px로 줄여 `figures/`에 바로 썼습니다(AGENT-BRIEF 대체 경로, 클라우드 `outputs` 쓰기를 쓰지 않음).

### 06절이 새로 가르친 것

- **새 라이브러리는 없습니다.** 01절 함수 네 개(`dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`), 05절 함수 두 개(`rank_by_distance`·`rank_by_bm25`), 04·05절 `kiwi_terms`·`BM25Okapi`, Ch 11 지표 함수 네 개를 같은 코드로 다시 정의했습니다.
- **자리 번호로 합치기**: `가중치 / (순위 상수 + 자리)`로 문서마다 몫을 내고 방법마다 더합니다. 순위 상수 `60`, 가중치 `[1.0, 1.0]`과 `[1.0, 1.5]`.
- **Python 모양**: 딕셔너리 누적 `scores.get(doc_id, 0.0) + share`(Ch 2 03절 모양), 목록의 목록을 인자로 받기(`ranking_list`·`weight_list`를 `range(len(...))`로 짝지음), 딕셔너리를 `for doc_id in scores`로 돌며 튜플 목록 만들기, `find_gold_rank(목록, [문서 ID])`로 문서 하나의 자리 찾기.
- **쓰지 않은 것**: `numpy`·`lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`목록.index`·`Path`·`hashlib`·`datetime`·f-string·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`·`sorted`뿐입니다.

### 이어 쓸 이름과 값 (06절)

- 값: `similarity_top`(1) · `top_three`(3) · `top_all`(12) · `cutoff_values`(`[1, 2, 3]`) · `keep_tags`(아홉 개) · **`method_names`(`["벡터 거리", "낱말 겹침", "순위 합치기"]`)** · **`rank_constant`(60)** · **`base_weight`(1.0)** · **`raised_weight`(1.5)** · **`equal_weights`(`[1.0, 1.0]`)** · **`sparse_up_weights`(`[1.0, 1.5]`)**.
- 자료(01~05절과 같은 이름): `candidates` · `root_path` · `data_path` · `docs`(12) · `queries`(8) · `doc_texts` · `doc_ids` · `embedding_model_name` · `vector_dimensions`(256) · `embedding_model` · `doc_vectors` · `query_vectors` · `kiwi` · `kiwi_corpus` · `bm25_model`.
- 06절이 새로 만든 이름: **`distance_id_lists`·`score_id_lists`**(질문마다 순위 문서 ID 목록 여덟 쌍) · `first_query` · `first_ranking_list` · `first_scores`·`first_fused_ids` · `second_scores`·`second_fused_ids` · `score_rows`(24줄) · `equal_ids`·`raised_ids`·`equal_place`·`raised_place`.
- 06절이 새로 만든 함수 두 개(괄호 안은 본문 줄 수): **`fuse_scores(ranking_list, weight_list)`**(9, 문서 ID → 합친 점수 딕셔너리) · **`fuse_rank(ranking_list, weight_list)`**(8, 합친 점수가 큰 순서의 문서 ID 목록).
- **`score_one()`의 인자 모양이 05절과 다릅니다**: 05절은 순위 목록(딕셔너리 목록)을 받아 함수 안에서 `unique_doc_ids()`를 불렀고, 06절은 **문서 ID 목록(`found_ids`)을 바로 받습니다**. 합친 순위가 이미 ID 목록이라 세 방법의 인자 모양을 맞췄습니다.
- 기록 한 줄의 칸 일곱 개는 05절과 같습니다: `방법`·`질문`·`갈래`·`정답 자리`·`자리 1`·`자리 2`·`자리 3`. `방법` 값만 셋입니다.

### 출력 라벨 (06절 전부)

「langchain-openai:」「python-dotenv:」「kiwipiepy:」「rank-bm25:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「문서 수:」「질문 수:」「코사인 유사도의 가장 큰 값:」「나란히 볼 상위 문서 수:」「자리를 셀 때 재는 문서 수:」「자르는 자리 세 가지:」「남길 품사 표시:」「견줄 방법 세 가지:」「순위 상수:」「같은 가중치:」「낱말 겹침 쪽만 올린 가중치:」「자리 | 기본 가중치가 주는 몫」(라벨 줄 따로)「이어 붙인 글 수:」「첫 문서 글:」「문서 ID 목록:」(라벨 줄 따로)「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 벡터 수:」「질문 벡터 수:」「검색 낱말 목록 수:」「BM25 모델이 본 문서 수:」「문서 하나의 평균 검색 낱말 수:」「만든 순위 목록 쌍 수:」「목록 하나의 문서 수:」「첫 질문의 벡터 거리 순위 앞 세 개:」「첫 질문의 낱말 겹침 순위 앞 세 개:」「고른 질문:」「그 질문의 정답 문서 ID:」「순위 | 문서 ID | 벡터 거리 자리 | 낱말 겹침 자리 | 합친 점수」(라벨 줄 따로)「쓴 가중치:」「담은 기록 줄 수:」「방법 | 질문 | 갈래 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율」(라벨 줄 따로)「방법 | 자르는 자리 | 질문 평균 재현율」(라벨 줄 따로)「질문 | 같은 가중치 자리 | 낱말 겹침 1.5 자리」(라벨 줄 따로)

### 실행값 (2026-09-18 마지막 새 커널, 두 실행이 같음)

- `문서 수: 12` · `질문 수: 8` · `벡터의 숫자 개수 설정: 256` · `검색 낱말 목록 수: 12` · `문서 하나의 평균 검색 낱말 수: 15.33`(04·05절과 같음).
- 자리별 몫 세 줄: `1 | 0.0164` · `2 | 0.0161` · `3 | 0.0159`.
- `만든 순위 목록 쌍 수: 8` · `목록 하나의 문서 수: 12` · 첫 질문 앞 세 개 `['LIB-004', 'LIB-001', 'LIB-003']`과 `['LIB-004', 'LIB-003', 'LIB-001']`(05절 실행 1과 같음).
- 실행 1(`C01`, 같은 가중치): `1 | LIB-004 | 1 | 1 | 0.03279` · `2 | LIB-001 | 2 | 3 | 0.032` · `3 | LIB-003 | 3 | 2 | 0.032`. **둘째와 셋째의 합친 점수가 같습니다**(자리 번호 2와 3이 서로 바뀐 짝).
- 값 바꿔 보기(`쓴 가중치: [1.0, 1.5]`): `1 | LIB-004 | 1 | 1 | 0.04098` · `2 | LIB-003 | 3 | 2 | 0.04007` · `3 | LIB-001 | 2 | 3 | 0.03994`. 정답 문서가 자리 2에서 3으로 내려갔습니다.
- 기록 스물네 줄. 정답 자리는 벡터 거리 `C01` 2·`C02` 7·나머지 1(**01·05절과 같음**), 낱말 겹침 `C01` 3·나머지 1(**04·05절과 같음**), 순위 합치기 `C01` 2·`C02` 3·나머지 1.
- 질문 평균 재현율 아홉 줄: 벡터 거리 `0.75`·`0.875`·`0.875`, 낱말 겹침 `0.875`·`0.875`·`1.0`, 순위 합치기 `0.75`·`0.875`·`1.0`. **세 방법이 자리 2에서 모두 `0.875`입니다.**
- 가중치 비교 여덟 줄: `C01 | 2 | 3` 하나만 다르고 `C02 | 3 | 3`, 나머지 여섯 질문은 `1 | 1`.

### 흔들리는 값과 결론 한정 — 07절도 같은 규칙으로

- **「합치면 좋아진다」로 쓰지 않았습니다.** 합친 값이 두 방법보다 높은 자리는 세 자리 가운데 없었습니다. 자리 1은 벡터 거리와 같고 자리 3은 낱말 겹침과 같습니다. 개선 전 06절이 적은 `rrf 7/8`(낱말 겹침 8/8보다 낮음)과 방향이 같은 결과입니다.
- **가중치를 올려도 좋아지지 않았습니다.** 정답 자리가 앞으로 온 질문은 없고 `C01`만 뒤로 갔습니다.
- **점수가 같은 자리는 성과로 읽지 않습니다.** 실행 1의 자리 2와 3은 문서 ID 차례가 정한 자리입니다(04절 공백 분리 `0.0` 줄과 같은 태도).
- 거리 값은 이 절에서 출력하지 않았습니다. 합친 점수는 자리 번호로만 계산하므로 순위가 흔들리지 않는 한 값이 흔들리지 않습니다(두 실행에서 같았음).
- **한쪽 목록에만 있는 문서 장면이 없습니다.** 두 순위 목록에 문서 열두 건이 모두 들어 있기 때문입니다. b7에 적었습니다.
- 순위 상수는 60 한 벌만 실행했습니다. 후보를 앞에서 잘라 넣는 방법, 걸린 시간, 정밀도·nDCG는 이번에 실행하지 않았습니다.
- Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과 나란히 놓지 않습니다(01절 b7에 이미 있는 문장이라 되풀이하지 않음).

### 용어 (06절이 더한 다섯 개, 07~12도 같게)

- **순위 합치기(Reciprocal Rank Fusion, RRF)** · **합친 점수(fused score)** · **순위 상수(rank constant)** · **가중치(weight)** · **하이브리드 검색(hybrid search)**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 5」 그대로입니다.
- **영문 `RRF`는 용어 표 괄호에만 적었고 본문은 「순위 합치기」로 부릅니다.** 절 제목 「RRF 하이브리드 검색」은 `chapter.json` 제목·파일 이름이라 그대로 두었습니다(03절 「iterative scan」·05절 「dense와 sparse」와 같은 처리).
- **「몫」**은 한 방법이 한 문서에 주는 값을 가리킵니다. 「합친 점수」는 그 몫을 모두 더한 값입니다. 04·05절 「점수」(BM25)와 다른 말이니 섞지 마세요.
- **「가중치」**는 몫에 곱하는 수입니다. 02·03절 「경로」, 04절 「정책」, 05절 「방법」·「갈래」와 다른 말입니다.
- 01~05절 말 스물아홉 개와 Ch 9~11 말을 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**이고 본문에 「토큰」·한정어 없는 「청크」를 쓰지 않았습니다.
- 쓰지 않은 말: 「RRF」 단독, 「융합」·「상호 순위 융합」(→ 순위 합치기), 「후보 창」(이번 절에서 쓰지 않음), 「원점수」(→ 값 또는 점수), 「정규화」(→ 값의 크기를 맞추기), 「Recall@3」(→ 자리 3 재현율), 「top-3」·「top-k」(→ 상위 3개·자르는 자리), 「임계값」, 「검색기」(→ 검색 방법).

### 파일 쓰기 규칙 — 06절도 파일을 쓰지 않습니다

- `runs/core-06-rrf.json`은 작업 전후 `4e3fa11084a4a09e5839c43c82786269f5a0a4e0b0aab0df490f0b044c511369` 그대로이고 `runs/core-history/before-4e3fa11084a4-core-06-rrf.json`과 바이트가 같습니다. `runs/`는 파일 36개, `core-history/`는 12개 그대로이고 **내용만 이어 붙인 해시는 `d3d6478c0790e11e045c518edd1356e20c29ce0d33156722221fc5947e4a107a`**로 05절 기록과 같습니다.
- `advanced-queries.json`·`advanced-documents.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않았습니다.
- 실습 폴더 테스트는 작업 전후 **4 passed**입니다. `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…`도 그대로입니다. 06절 `%pip` 목록 네 개는 05절과 같고 모두 잠금에 있으며 dev `pip==26.2`도 그대로입니다(확인만 했습니다).
- 공용 화면 검사 결과 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`은 **26행을 유지**해야 합니다(`finalize_continuity_evidence.py` 15행). 06절은 `/tmp/ch12-06/vis12.cjs` 사본으로 06절 두 줄만 다시 찍었고 값이 같아 파일 바이트가 `49352bfcd3f7e511…`로 그대로입니다.
- 검사 스크립트가 멈추는 자리는 01절 기준과 같습니다: `textbook/part3/qa/check_continuity.py` 154행 `part2-practice.zip`, `textbook/qa/check_course_continuity.py` 212행 `part1-practice.zip`, `textbook/part3/qa/check_delivery.py`는 끝까지 통과.

### 07절이 이어받을 연결과 확인할 것

- 06 b8·노트북 정리 끝: 「07절에서는 후보 목록을 고정해 두고 질문과 후보 본문을 함께 읽어 순서를 다시 정합니다. 그 절부터 쓰는 문서와 질문 묶음이 바뀝니다.」 07절 `_src` b3·b4와 노트북 셀 4·6을 열어 확인하고 쓴 문장입니다.
- **07절부터 자료가 바뀝니다.** `advanced-documents.json`(부모 6건·문서 청크 175개)과 `advanced-queries.json`(질문 30개, Ch 11 평가셋과 같은 계약 파일)을 씁니다. **Ch 11 요약 §11-1의 약속(개발 15문항으로 고르고 시험 15문항은 마지막 한 번)을 07절 처음 쓰는 자리에서 인용하세요.** 01~06절 core 벌 값(자리 3 재현율 등)과 07절 이후 값을 나란히 놓지 마세요(문서·질문·후보 단위가 모두 다름).
- **개선 전 07 노트북이 하는 일**(셀 9개, 코드 4개): 문자 단위 TF-IDF(`TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))`)로 청크 175개를 벡터로 만들고 `Q001`의 상위 8개를 후보로 뽑습니다. `CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=256, device="cpu")`의 `predict(쌍 목록)`으로 로짓을 받아 다시 정렬하고, 후보를 2개로 줄여도 정답 부모 `E01`이 들어 있음을 보입니다.
- **개선 전 07 노트북의 출력(참고용, 다시 실행하면 확인할 값)**: `부모 문서 6건 · 자식 청크 175개 · 평가 질문 30개`, 후보 여덟 줄 `1 E01-P01-C01 0.421` · `2 E01-P02-C01 0.236` · `3 E02-P05-C01 0.194` · `4 E01-P02-C04 0.172` · `5 E01-P05-C01 0.098` · `6 E01-P02-C02 0.093` · `7 E01-P03-C06 0.055` · `8 E02-P05-C02 0.048`, 그리고 `후보 부모 ID: ['E01']` · `정답 문서 포함: True` · `리랭커 입력 쌍 수: 2`. 리랭킹 뒤 다섯 줄은 모델을 내려받아야 다시 볼 수 있습니다.
- **모델 내려받기 준비**: `BAAI/bge-reranker-v2-m3`는 `.cache/vm/hf`에 **없습니다**(지금 있는 것은 Qwen2.5-0.5B·SmolLM2-135M·klue/bert-base·gpt2·paraphrase-multilingual-MiniLM-L12-v2, 합계 1.7G). 내려받기는 `HF_HOME=$ROOT/.cache/vm/hf`를 주고 `timeout 165`로 나눠 반복하세요(`run_section.sh`가 `.cache/vm/venv-ch12-…`를 보고 자동으로 `HF_HOME`을 줍니다). 실습 폴더 잠금에 `sentence-transformers==6.0.1`·`scikit-learn==1.9.0`·`numpy==2.5.3`이 이미 있고 가상환경에 `torch 2.14.0`도 들어 있습니다.
- **개선 전 07 노트북이 쓰는 것 가운데 01~06절에서 안 가르친 것**: `numpy`(`np.argsort`), `sklearn`(`TfidfVectorizer`·`cosine_similarity`), 제너레이터 식 두 곳(`next(path for path in ...)`·`next(item for item in queries ...)`), 내포식 두 곳, 집합 내포식(`{chunks[idx]["parent_id"] for idx in small_idx}`)과 `set` 연산 `&`, `enumerate(..., 1)`, f-string 안 형식 지정(`f"{score:.3f}"`), `Path`·`Path.read_text`, `assert query["split"] == "dev"`, 딕셔너리 만들기 `{item["doc_id"]: item for item in ...}`, 한 줄에 두 이름 대입(`chunks, parents = ...`). **`CrossEncoder`·`predict`·`max_length`·`device`는 이 챕터에서 처음 나오는 이름**이라 처음 쓰는 자리에서 뜻을 풀어야 합니다(규격 §4 세 문장).
  - **후보 만들기**: TF-IDF를 그대로 쓰면 새 라이브러리와 새 개념이 한 번에 늘어납니다. **01~06절이 이미 가르친 방법(임베딩 코사인 거리, Kiwi+BM25, 순위 합치기)으로 후보를 만드는 쪽을 먼저 검토하세요.** 06절 `fuse_rank()`가 낸 목록을 07절 후보로 쓰면 「합친 순위를 다시 정렬한다」로 05 → 06 → 07이 한 줄로 이어집니다. 청크 175개를 임베딩하면 요청이 늘어나므로 비용을 먼저 어림하세요(`text-embedding-3-small` 기준 0.01달러 안팎).
  - **정렬**: 04·05·06절이 쓴 「점수에 음수를 붙여 `sorted(목록)`」 모양을 그대로 쓸 수 있습니다(`key=`·`reverse=` 없이).
  - **자리 찾기**: `find_gold_rank(목록, [찾는 ID])`로 문서 하나의 자리를 낼 수 있습니다(06절에서 쓴 모양).
  - **집합 대신**: `set`은 아직 가르치지 않았습니다. `unique_doc_ids()`로 중복을 빼고 `in`으로 확인하세요.
- **후보 단위와 지표**: 07절부터 후보 하나가 **문서 청크**이고 정답은 **부모 문서 ID**입니다(`gold_doc_ids`, 목록). 01~06절은 후보 = 문서 한 건·정답 한 개였습니다. Ch 11 지표 함수는 **중복을 뺀 문서 ID 목록**을 받으므로 청크 목록을 부모 ID 목록으로 바꾼 뒤 넘겨야 합니다(Ch 9 요약 §5·Ch 11 요약 §11-2).
- **파일 쓰기**: 개선 전 07 노트북은 `runs/`에 쓰지 않습니다. 01~06절 선례대로 쓰지 않는 쪽을 유지하세요. 12절이 쓰는 `runs/advanced-continuity-*` 세 파일은 계약이 가장 촘촘하니 12절 작업 전에 `check_course_continuity.py` 113~166행과 `tests/test_continuity.py`를 먼저 읽으세요.
- **실습 폴더 테스트 주의**: `tests/`는 **08·10·12절 노트북**의 `eligible_items`·`evaluate`·`mmr`·`metrics`·`evaluate_config` 이름·인자·반환을 `ast`로 찾아 실제로 실행합니다. 그 세 절을 다시 쓸 때 테스트를 함께 확인하세요(07절은 대상이 아닙니다).
- **아직 안 가르친 것(07이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01~05절 목록에 더해, 06절에서도 하지 않은 것 — 순위 상수 다른 값, 후보를 앞에서 잘라 합치기, 한쪽 목록에만 있는 문서 다루기, 점수를 0에서 1로 맞추기, 가중치를 여러 값으로 찾기, 검색에 걸린 시간 재기, 정밀도·nDCG 계산(Ch 11에서 배웠지만 01~06절은 재현율만), 점수 기준값·거르기, 큰 말뭉치에서 재현율 재기, 문서 청크로 나누기, 부모 문서로 되돌리기(09절), 재정렬(07·08절), MMR(10절), 질문 재작성(11절), 답을 쓰는 모델 호출(11·12절).

## §07 → §08

(07절 품질 개선 2026-09-18. 결과는 `07-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 33 = G1 6·G2 0·G3 4·G4 0·G5 6·G6 14·G7 3), 코드 셀 37(준비 5), 검사 문장 380, **임베딩 요청 16번**(문서 청크 1 + 개발 질문 15, 0.01달러 아래)·**리랭커 호출 17번**(쌍 130개), 답을 쓰는 모델 0번. 새 커널 두 번 실행에 `code_sha256` `2f584b093c3b017a…`와 셀별 출력 글자 해시 `4d2fd5f078cf1fbb`가 같고 교재 출력은 마지막 실행 2026-09-18T19:11:39Z. `verify.py --chapter` `PASS 12 sections / 277 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(2차 job `1e88e31e-1643-49d6-b7fb-6a2da7b3121e` 채택, 1차 `d5f1e9ba-…` 탈락, 4크레딧, 생성 전 잔액 2725))

### 작업 환경 — 08절이 먼저 읽을 것

- **리랭커 모델은 이제 `.cache/vm/hf`에 있습니다.** `BAAI/bge-reranker-v2-m3`, revision **`953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`**, 내려받은 크기 **2.2GB**(`onnx/*`·`*.bin` 제외), 걸린 시간 64초. `hf` 폴더는 1.7GB → **3.9GB**가 되었습니다. 사용자 디스크 여유는 약 19G입니다.
- **08절이 쓰는 두 번째 리랭커 `Dongjin-kr/ko-reranker`는 아직 없습니다.** 같은 방법으로 받으세요: `HF_HOME=$ROOT/.cache/vm/hf`, `snapshot_download(repo, ignore_patterns=["onnx/*", "*.bin", "*.h5", "*.ot", "*.msgpack", "imgs/*"], max_workers=4)`, `timeout 165`로 나눠 반복. 그 모델은 klue/roberta 계열이라 v2-m3보다 작습니다(받아 보고 크기를 진단에 적으세요).
- **메모리와 시간(v2-m3, 메모리 3.8GB VM)**: 모델 만들기 3.3초, 여덟 쌍 2.9초, 열다섯 질문 × 여덟 쌍 38초, **최대 RSS 약 3.1GB**. 노트북 전체가 63초였습니다. **모델 두 개를 한 노트북에서 동시에 살려 두면 메모리가 모자랄 수 있습니다** — 08절은 한 모델을 다 쓴 뒤 다음 모델을 만드세요(개선 전 08 노트북은 딕셔너리에 두 모델을 함께 담습니다).
- **가상환경의 `transformers`가 깨져 있어 고쳤습니다.** 2,638개 파일 가운데 2,383개가 없어 `import transformers`가 `ModuleNotFoundError`로 멈췄습니다. 마운트 폴더는 삭제가 막혀 `--reinstall`을 쓸 수 없어 PyPI 휠 `transformers-5.16.1-py3-none-any.whl`을 받아 `site-packages`에 **덮어쓰기만** 했습니다(삭제 없음, 잠금이 정한 판과 같은 5.16.1). 08절은 그대로 쓰면 됩니다.
- **기기 셸 180초 제한 때문에 실행을 나눴습니다.** `run_section.sh` 한 호출로 돌리면 리랭커 실행이 들어가 아슬아슬합니다. 07절은 (1) 생성기 + `execute.py`(63초), (2) `run_section.sh … 07 --no-exec`(11초) 두 호출로 나눴습니다. 08절은 모델이 둘이라 더 오래 걸리니 같은 방법을 쓰세요. 실행 명령은 `UV_CACHE_DIR=/tmp/uv-cache UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch12-retrieval-tuning HF_HOME=$ROOT/.cache/vm/hf UV_NO_SYNC=1 uv run --project labs/part3/ch12-retrieval-tuning --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 python textbook/_notebook/execute.py <노트북>`입니다.
- `visual.cjs`만 `/tmp` 사본이 필요합니다(`/tmp/ch12-07/vis12.cjs`, 06절 사본 복사). `ONLY=08- node /tmp/ch12-07/vis12.cjs textbook/part3/ch12-retrieval-tuning`으로 해당 절 두 줄만 갱신합니다.
- `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/pw`·`/tmp/libs`·`/tmp/uv-cache`는 그대로 남아 있습니다. 루트 디스크 여유 3.5G.
- 07절은 pgvector 서버를 쓰지 않습니다(`pre_exec.sh`가 켜도 출력에 영향 없음).

### 07절이 새로 가르친 것

- **sentence-transformers**: `CrossEncoder(이름, revision=, max_length=, device="cpu")` · `predict(쌍 목록, show_progress_bar=False)` · 속성 `max_seq_length`. 쌍은 `(질문, 후보 본문)` 튜플입니다.
- **넘파이 배열을 파이썬 목록으로**: `predict()`가 주는 값에 `.tolist()`를 씁니다(Ch 5 01·05절 텐서 `.tolist()`와 같은 모양). **numpy를 import 하지 않았고 sklearn도 쓰지 않았습니다.**
- **환경 변수 쓰기**: `os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"`(진행 막대를 끄지 않으면 셀 출력에 `Loading weights: …it/s` 두 줄이 남아 실행마다 달라집니다). `warnings.filterwarnings("ignore", message="IProgress not found")`는 Ch 5 02절과 같은 줄입니다.
- **부모 문서 ID로 바꾸기**: `parent_ids_of(found_chunk_ids)`가 중복을 뺀 부모 문서 ID 목록을 냅니다. Ch 11 지표 함수는 그 목록을 받습니다.
- **쓰지 않은 것**: `numpy` import·`sklearn`·`lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`목록.index`·`float()`·`Path`·`hashlib`·`datetime`·f-string·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`·`sorted`뿐입니다.

### 이어 쓸 이름과 값 (07절)

- 값: `similarity_top`(1) · `cutoff_values`(`[1, 2, 3]`) · `keep_tags`(아홉 개) · **`method_names`(`["1차 후보", "리랭킹"]`)** · **`candidate_count`(8)** · **`small_candidate_count`(2)** · `rank_constant`(60) · `base_weight`(1.0) · `equal_weights`(`[1.0, 1.0]`) · **`all_chunk_count`(175)**.
- 자료: `candidates` · `root_path` · `data_path` · `documents` · `queries`(30) · `parents`(6) · `chunks`(175) · **`dev_queries`(15)** · **`test_queries`(15, 읽기만 하고 쓰지 않음)** · `chunk_texts` · `chunk_ids` · **`parent_by_chunk`** · **`text_by_chunk`** · `embedding_model_name` · `vector_dimensions`(256) · `embedding_model` · `chunk_vectors` · `query_vectors` · `kiwi` · `kiwi_corpus` · `bm25_model`.
- 리랭커: **`reranker_name`**(`"BAAI/bge-reranker-v2-m3"`) · **`reranker_revision`**(`"953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e"`) · **`reranker_max_length`**(256) · `reranker`.
- 후보: **`fused_lists`**(질문마다 문서 청크 175개 전체 차례) · **`candidate_lists`**(앞 여덟 개) · `example_index`(1) · `example_query` · `example_candidates` · `example_ranked` · `example_ranked_ids` · `small_candidates` · `small_ranked` · `best_chunk_id`.
- 07절이 새로 만든 함수 다섯 개(괄호 안은 본문 줄 수): **`unique_chunk_ids(hit_list)`**(5, 06절 `unique_doc_ids`와 같은 모양·보는 키만 `chunk_id`) · **`parent_ids_of(found_chunk_ids)`**(6) · **`make_pairs(question, found_chunk_ids)`**(5) · **`rerank(question, found_chunk_ids)`**(10, `{"chunk_id": …, "리랭킹 점수": …}` 목록) · **`score_one(query_index, method_name, found_chunk_ids)`**(8).
- 01~06절과 같은 코드로 다시 정의한 함수 열 개: `dot_product` · `vector_length` · `cosine_similarity` · `cosine_distance` · `kiwi_terms` · `rank_by_distance`(칸 `거리`) · `rank_by_bm25`(칸 `점수`) · `fuse_scores` · `fuse_rank` · `find_gold_rank` · `recall_at` · `mean_score`. **순위 목록의 키가 `doc_id`에서 `chunk_id`로 바뀐 것만 다릅니다.**
- **기록 한 줄의 칸 여덟 개**: `방법`·`질문`·**`난이도`**(질문 파일 `tier`)·**`1위 문서 청크`**·`정답 자리`·`자리 1`·`자리 2`·`자리 3`. 05·06절 `갈래`(`kind`) 자리에 `난이도`를 두었습니다(advanced 질문 파일에는 `kind` 칸이 없고 `tier`·`type`이 있습니다).

### 출력 라벨 (07절 전부)

「langchain-openai:」「python-dotenv:」「kiwipiepy:」「rank-bm25:」「sentence-transformers:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「부모 문서 수:」「문서 청크 수:」「질문 수:」「개발 질문 수:」「시험 질문 수:」「첫 개발 질문:」「그 질문의 정답 부모 문서 ID:」「코사인 유사도의 가장 큰 값:」「자르는 자리 세 가지:」「남길 품사 표시:」「견줄 두 단계:」「후보 수:」「줄여 볼 후보 수:」「순위 상수:」「같은 가중치:」「이어 붙인 글 수:」「첫 문서 청크 ID:」「첫 문서 청크 글:」「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 청크 벡터 수:」「질문 벡터 수:」「검색 낱말 목록 수:」「BM25 모델이 본 문서 청크 수:」「문서 청크 하나의 평균 검색 낱말 수:」「만든 후보 목록 수:」「후보 목록 하나의 문서 청크 수:」「리랭커 이름:」「리랭커 판 번호 앞 열두 글자:」「한 쌍에서 읽는 최대 조각 수:」「고른 질문:」「1차 자리 | 문서 청크 ID | 부모 문서 ID」(라벨 줄 따로)「후보의 부모 문서 차례:」「후보 밖 문서 청크 수:」「리랭킹 자리 | 문서 청크 ID | 1차 자리 | 리랭킹 점수」(라벨 줄 따로)「리랭킹 뒤 부모 문서 차례:」「리랭킹 전후 문서 청크가 같은 묶음인가:」「쓴 후보 수:」「리랭킹 자리 | 문서 청크 ID | 리랭킹 점수」(라벨 줄 따로)「후보 여덟 개의 리랭킹 1위:」「그 문서 청크가 후보 둘에 있는가:」「그 문서 청크의 1차 자리:」「담은 기록 줄 수:」「방법 | 질문 | 난이도 | 1위 문서 청크 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율」(라벨 줄 따로)「방법 | 자르는 자리 | 질문 평균 재현율」(라벨 줄 따로)「질문 | 1차 1위 문서 청크 | 리랭킹 1위 문서 청크」(라벨 줄 따로)「1위 문서 청크가 바뀐 질문 수:」

### 실행값 (2026-09-18 마지막 새 커널, 두 실행이 같음)

- `부모 문서 수: 6` · `문서 청크 수: 175` · `질문 수: 30` · `개발 질문 수: 15` · `시험 질문 수: 15`.
- `첫 개발 질문: Q001 | 미르시립도서관의 정기 휴관일은 언제인가요?` · `그 질문의 정답 부모 문서 ID: ['E01']`.
- `문서 청크 벡터 수: 175` · `질문 벡터 수: 15` · `문서 청크 하나의 평균 검색 낱말 수: 44.01`(01~06절 15.33과 나란히 놓지 않음).
- `리랭커 판 번호 앞 열두 글자: 953dc6f6f85a` · `한 쌍에서 읽는 최대 조각 수: 256`. 이 셀 출력 맨 위에 HF 토큰 없이 받았다는 영문 알림 한 줄이 남습니다(결과 읽기에 그 뜻을 적었습니다).
- 실행 1 `고른 질문: Q002 | 도서는 한 번에 몇 권까지, 며칠 동안 빌릴 수 있나요?`. 1차 후보 여덟 줄은 `1 | E01-P03-C02` · `2 | E01-P04-C06` · `3 | E01-P03-C01` · `4 | E01-P03-C08` · `5 | E01-P03-C04` · `6 | E01-P03-C06` · `7 | E02-P02-C05` · `8 | E02-P03-C02`입니다. `후보의 부모 문서 차례: ['E01', 'E02']` · `후보 밖 문서 청크 수: 167`.
- 리랭킹 뒤 여덟 줄: `1 | E01-P03-C01 | 3 | 0.2246` · `2 | E01-P03-C02 | 1 | 0.003` · `3 | E01-P03-C08 | 4 | 0.0003` · `4 | E01-P04-C06 | 2 | 0.0003` · `5 | E01-P03-C04 | 5 | 0.0003` · `6 | E01-P03-C06 | 6 | 0.0002` · `7 | E02-P03-C02 | 8 | 0.0001` · `8 | E02-P02-C05 | 7 | 0.0`. `리랭킹 전후 문서 청크가 같은 묶음인가: True`.
- 값 바꿔 보기(후보 둘): `1 | E01-P03-C02 | 0.003` · `2 | E01-P04-C06 | 0.0003` · `후보 여덟 개의 리랭킹 1위: E01-P03-C01` · `그 문서 청크가 후보 둘에 있는가: False` · `그 문서 청크의 1차 자리: 3`.
- 기록 **서른 줄**: 정답 자리가 서른 줄 모두 `1`, 자리 1·자리 3 재현율도 모두 `1.0`. 질문 평균 여섯 줄 모두 `1.0`.
- **1위 문서 청크가 바뀐 질문 3개**: `Q002 | E01-P03-C02 | E01-P03-C01` · `Q039 | M01-P05-C05 | M01-P03-C01` · `Q087 | H01-P07-C02 | H01-P07-C03`. 세 질문 모두 앞뒤 청크의 부모 문서가 같아 재현율에는 나타나지 않습니다.

### 가장 큰 주의 — 지표가 천장에 닿았습니다 (08절이 먼저 볼 것)

- **개발 15문항에서 1차 후보가 이미 정답 부모를 자리 1에 두었습니다.** 그래서 자리 1·2·3 재현율이 두 단계 모두 `1.0`이고 리랭킹 효과를 재현율로 가를 수 없습니다. 07절 본문은 「이 자료에서 리랭킹이 재현율을 올리지 못했다」까지만 적었습니다(Ch 11 요약 §3 「천장」·06절 「합치면 좋아진다고 쓰지 않음」과 같은 태도).
- **개선 전 08 노트북도 같은 자리입니다**: 후보 5·10·20 × 리랭커 두 개 여섯 행이 모두 `recall=1.000 nDCG=1.000`. 08절 본문도 「차이를 관찰하지 못했다」로 적혀 있습니다. **여섯 행이 모두 같은 값인 표를 그대로 두면 08절이 견줄 것이 없습니다.** 검토할 갈래를 적어 둡니다.
  1. **보고 단위를 문서 청크로 두기**: 부모 문서가 6건뿐이라 부모 단위 재현율은 천장에 닿습니다. 정답 부모의 **문서 청크가 앞자리에 몇 개 들어왔는지**(정밀도 모양)나 **정답 부모의 첫 청크 자리**를 재면 두 리랭커가 갈립니다(07절 실행 1에서 자리 3 → 1로 바뀜).
  2. **후보 수를 더 줄이기**: 07절이 후보 둘에서 결과가 갈리는 것을 보였습니다. 08절이 후보 2·4·8을 견주면 후보 범위 효과가 보일 수 있습니다(5·10·20은 모두 천장).
  3. 어느 갈래든 **값이 모두 같으면 「고를 근거가 없다」로 적는 태도**를 유지하세요(개선 전 08 b7 첫 줄과 같은 결론).
- **Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과 나란히 놓지 않습니다**(01 b7에 이미 있는 문장이라 07절에서 되풀이하지 않았습니다). 01~06절 core 벌 값과도 나란히 놓지 않습니다.

### 용어 (07절이 더한 다섯 개, 08~12도 같게)

- **1차 검색(first-stage retrieval)** · **리랭킹(reranking)** · **교차 인코더(cross-encoder)** · **리랭킹 점수(reranking score)** · **부모 문서(parent document)**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 4 → **5**」입니다.
- **「리랭킹 점수」는 0과 1 사이 값입니다.** 개선 전 07·08절이 쓴 **「로짓」은 쓰지 않습니다**(설치판 `get_default_activation_fn()`이 값 하나인 리랭커에 `nn.Sigmoid()`를 줍니다). 크기를 확률로 읽지 않고 같은 질문 안의 차례만 봅니다. 다른 질문의 점수끼리 견주지 않습니다.
- **「부모 문서」**는 문서 청크가 나온 원래 문서입니다. 09절 「Parent document 검색」이 그 문서를 통째로 넘기는 방법을 다루므로 같은 말을 이어 쓰세요.
- **「1차 검색」과 「리랭킹」은 단계 이름**입니다. 기록 칸의 값은 `1차 후보`·`리랭킹`입니다. 02·03절 「경로」, 04절 「정책」, 05절 「방법」·「갈래」, 06절 「가중치」와 다른 말입니다.
- **「난이도」**는 질문 파일 `tier` 칸을 가리킵니다(값 `easy`·`medium`·`hard`는 출력이라 그대로 인용). Ch 11 요약 §9와 같은 말입니다.
- 01~06절 말 서른네 개와 Ch 9~11 말을 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**(`한 쌍에서 읽는 최대 조각 수`)이고 한정어 없는 「청크」는 쓰지 않았습니다.
- 쓰지 않은 말: 「로짓」, 「크로스 인코더」(→ 교차 인코더), 「재정렬기」·「리랭커 모델」 단독(→ 리랭커), 「후보 집합」(→ 후보 목록), 「top-k」·「top-8」(→ 후보 수·상위 여덟 개), 「Recall@3」(→ 자리 3 재현율), 「임계값」, 「포화」(→ 천장에 닿음), 「TF-IDF」(이 절에서 쓰지 않음).

### 파일 쓰기 규칙 — 07절도 파일을 쓰지 않습니다

- `runs/`는 파일 10개·`core-history/` 12개 그대로이고 **내용만 이어 붙인 해시 `d3d6478c0790e11e045c518edd1356e20c29ce0d33156722221fc5947e4a107a`**로 05·06절 기록과 같습니다. 개별 해시도 모두 같습니다.
- `advanced-documents.json`·`advanced-queries.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않았습니다.
- 실습 폴더 테스트는 작업 전후 **4 passed**입니다. `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…`도 그대로입니다.
- **`%pip` 목록이 다섯 개로 늘었습니다**(05·06절 네 개 + `sentence-transformers==6.0.1`). 잠금 101·122행에 있고 dev `pip==26.2`도 107·128행에 그대로라 학생 `.venv`에서 첫 셀이 멈추지 않습니다(규격 §7-2). 잠금 파일은 고치지 않았습니다.
- 공용 화면 검사 결과 `visual-results.json`은 **26행 유지**이고 값이 같아 파일 바이트가 `49352bfcd3f7e511…`로 그대로입니다.
- 검사 스크립트가 멈추는 자리는 01절 기준과 같습니다(이번 절에서 다시 돌리지 않았습니다).

### 08절이 이어받을 연결과 확인할 것

- 07 b8·노트북 정리 끝: 「08절에서는 같은 개발 질문에서 후보 수와 리랭커를 여러 벌로 바꿔 가며 견줍니다.」 08절 `_src` b2와 노트북 셀 2·5를 열어 후보 5·10·20과 리랭커 두 가지를 확인하고 쓴 문장입니다.
- **07절 코드를 그대로 이어 쓸 수 있습니다**: 후보 만들기(`rank_by_distance`·`rank_by_bm25`·`fuse_rank`)와 `parent_ids_of`·`make_pairs`·`rerank`·`score_one`. `rerank()`에 리랭커를 인자로 받게 고치면 모델 두 개를 견줄 수 있습니다.
- **실습 폴더 테스트 주의(중요)**: `labs/part3/ch12-retrieval-tuning/tests/test_continuity.py`가 **08절 노트북의 `eligible_items`와 `evaluate`를 `ast`로 찾아 실제로 실행합니다**(10·12절은 `mmr`·`metrics`·`evaluate_config`). 08절을 다시 쓸 때 두 함수의 이름·인자·반환을 지키거나 테스트를 함께 고치세요. 개선 전 판은 `eligible_items(subset)`가 내포식 한 줄이고 `evaluate(scored, candidate_k)`가 `np.argsort`·집합 연산·`next(...)`를 씁니다 — 사다리를 넘으므로 **테스트가 요구하는 이름·인자·반환만 지키고 몸통을 여러 줄로 다시 쓰는 쪽**을 먼저 검토하세요.
- **개선 전 08 노트북이 쓰는 것 가운데 01~07절에서 안 가르친 것**: `numpy`(`np.argsort`·`np.log2`·`np.mean`), `sklearn`(`TfidfVectorizer`·`cosine_similarity`), `perf_counter`, 딕셔너리 내포식으로 모델 두 개 만들기, 집합 연산 `&`, `dict.fromkeys`, `next(... for ...)`, `raise ValueError`, f-string 형식 지정(`f"{row[0]:24s}"`), 한 줄에 두 이름 대입.
- **모델을 하나씩 만들고 지우기**: 메모리 3.8GB에서 v2-m3 하나에 최대 RSS 3.1GB였습니다. 두 모델을 딕셔너리에 함께 담으면 위험합니다. 이름 하나에 모델을 다시 대입하는 방법(같은 이름 재사용)을 검토하세요.
- **아직 안 가르친 것(08이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01~06절 목록에 더해, 07절에서도 하지 않은 것 — 리랭킹에 걸린 시간 재기, 리랭커 두 개 이상 견주기, 후보 수 여러 벌 견주기, 정밀도·nDCG 계산(Ch 11에서 배웠지만 01~07절은 재현율만), `max_length`를 바꿔 견주기, 점수 기준값·거르기, 문서 청크 단위 지표, 부모 문서를 통째로 넘기기(09절), MMR(10절), 질문 재작성(11절), 답을 쓰는 모델 호출(11·12절), 시험 15문항 보기(12절).

## §08 → §09

(08절 품질 개선 2026-09-18. 결과는 `08-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 39 = G1 12·G2 1·G3 5·G4 0·G5 8·G6 10·G7 3), 코드 셀 33(준비 5, 07절 37에서 넷 줄임), 검사 문장 341, **임베딩 요청 16번**(문서 청크 1 + 개발 질문 15, 0.01달러 아래)·**리랭커 호출 30번**(모델 둘 × 질문 15, 쌍 240개), 답을 쓰는 모델 0번. 새 커널 두 번 실행에 `code_sha256` `0f6b07865700548e`와 셀별 출력 글자 해시 `c15269cc11ba8b00`이 같고 교재 출력은 마지막 실행 2026-09-18T20:01:09Z. 노트북 전체 105초. `verify.py --chapter` `PASS 12 sections / 305 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(1차 job `4025250c-8d60-47cd-acb7-a53520dffb52` 채택, 재생성 없음, 2크레딧, 생성 전 잔액 2721))

### 작업 환경 — 09절이 먼저 읽을 것

- **리랭커 모델 두 개가 모두 `.cache/vm/hf`에 있습니다.** `BAAI/bge-reranker-v2-m3`(revision `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`, 2.2GB)와 **`Dongjin-kr/ko-reranker`(revision `8c2ab1a833734491fd3158164dd2b7d8b28e071c`, 2.2GB)**입니다. `hf` 폴더는 3.8GB → **6.0GB**가 되었고 사용자 디스크 여유는 약 18G입니다. 09절은 리랭커를 쓰지 않으므로 새로 받을 것이 없습니다.
- **메모리**: 리랭커 하나를 살려 두면 최대 RSS 약 2.5GB, 두 개를 차례로 쓰면 2.76GB였습니다(메모리 3.8GB VM). 이름에 `None`을 넣어 앞 모델을 내려놓은 뒤 다음 모델을 만드는 모양이 돌아갑니다.
- **기기 셸 180초 제한 때문에 두 호출로 나눴습니다.** (1) 생성기 + `execute.py`(105초), (2) `run_section.sh … 08 --no-exec`(11초). 09절은 리랭커가 없어 한 호출로 될 수도 있지만, 임베딩 16번 + 순수 파이썬 코사인 계산에 40초쯤 듭니다.
- **주의(실수 기록)**: 빌드를 `run_section.sh` 없이 `uv run --project … --with pillow`로 직접 부르면 `UV_PROJECT_ENVIRONMENT`·`UV_NO_SYNC`가 빠져 uv가 torch 계열을 새로 내려받습니다. 루트 디스크(9.6G)가 차서 멈췄고 `/tmp/uv-cache/.tmp*`를 지워 되돌렸습니다. **빌드·검사는 반드시 `run_section.sh`로 부르세요.** 그때 만들어진 `labs/part3/ch12-retrieval-tuning/.venv`(72KB, 패키지 없음)는 마운트 폴더 삭제 제한으로 남아 있습니다. `.gitignore` 3행 `labs/**/.venv/`에 들어 있고 `check_delivery.py`는 통과합니다. 챕터 마감 때 지울 대상입니다.
- `visual.cjs`만 `/tmp` 사본이 필요합니다(`/tmp/ch12-08/vis12.cjs`, 07절 사본 복사). `ONLY=09- node /tmp/ch12-08/vis12.cjs textbook/part3/ch12-retrieval-tuning`으로 해당 절 두 줄만 갱신합니다.
- `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/pw`·`/tmp/libs`·`/tmp/uv-cache`는 그대로입니다. 루트 디스크 여유 2.2G(07절 3.5G에서 줄었습니다 — `/tmp/uv-cache`가 1.6G).
- 08절은 pgvector 서버를 쓰지 않습니다.

### 08절이 새로 가르친 것

- **문서 청크 정밀도**: `chunk_precision_at(found_chunk_ids, gold_doc_ids, cutoff)`. 앞자리 문서 청크 가운데 부모가 정답인 것을 세고 **자르는 자리(보고 자리)로 나눕니다**. Ch 11 03절 정밀도의 「나누는 수가 고정」을 문서 청크 단위로 옮긴 것입니다.
- **보고 자리**: 검색 결과에서 다음 단계로 넘길 문서 청크 수. 이 절은 5로 고정하고 값 바꿔 보기에서만 3으로 바꿨습니다.
- **한 번에 한 가지만 바꾸기**: 방법 세 가지 × 후보 수 세 가지의 아홉 줄 격자.
- **모델을 하나씩 만들고 내려놓기**: `reranker = None` 뒤 `reranker = CrossEncoder(...)`.
- **1차 차례를 점수로 바꾸기**: `place_scores`(`[0, -1, -2, …]`)를 넣으면 리랭킹과 같은 함수로 1차 후보를 잴 수 있습니다.
- **쓰지 않은 것**: `numpy` import·`sklearn`·`lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`(단 `evaluate`의 `raise ValueError`는 실습 폴더 테스트가 요구해 한 곳에 있음)·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`목록.index`·`Path`·`hashlib`·`datetime`·f-string·타입힌트·`@`·`BaseModel`·한 줄에 두 이름 대입. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`sorted`·`dict`가 아니라 `len`·`print`·`open`·`range`·`round`·`sorted`뿐입니다.

### 이어 쓸 이름과 값 (08절)

- 값: `similarity_top`(1) · `keep_tags`(아홉 개) · `rank_constant`(60) · `equal_weights`(`[1.0, 1.0]`) · **`candidate_count`(8)** · **`candidate_counts`(`[2, 4, 8]`)** · **`recall_place`(3)** · **`report_place`(5, 값 바꿔 보기에서 3)** · **`method_names`(`["1차 후보", "리랭커 A", "리랭커 B"]`)**.
- 리랭커: **`reranker_names`**(`["BAAI/bge-reranker-v2-m3", "Dongjin-kr/ko-reranker"]`) · **`first_revision`**·**`second_revision`** · `reranker_revisions` · `reranker_max_length`(256) · `reranker`.
- 자료(07절과 같은 이름): `candidates` · `root_path` · `data_path` · `documents` · `queries`(30) · `parents`(6) · `chunks`(175) · `dev_queries`(15) · `chunk_texts` · `chunk_ids` · `parent_by_chunk` · `text_by_chunk` · `all_chunk_count`(175) · `embedding_model_name` · `vector_dimensions`(256) · `chunk_vectors` · `query_vectors` · `kiwi` · `kiwi_corpus` · `bm25_model`.
- 08절이 새로 만든 이름: **`dev_all`** · **`candidate_sets`**(질문 ID → 후보 문서 청크 ID 여덟 개) · **`first_scored`**·**`place_scores`** · **`scored_by_method`**(방법 이름 → 질문 ID → 점수 목록) · `row_values`.
- 08절이 새로 만든 함수 여섯 개(괄호 안은 본문 줄 수): **`eligible_items(subset)`**(10, 답할 수 있고 정답 ID가 있는 질문만·중복 정답 ID 제거) · **`score_candidates(question, found_chunk_ids)`**(5, 07절 `make_pairs`+`rerank`를 합친 판, 점수 목록만 반환) · **`order_by_score(question_id, scored, candidate_k)`**(9) · **`chunk_precision_at(found_chunk_ids, gold_doc_ids, cutoff)`**(6) · **`evaluate(scored, candidate_k)`**(11, 두 지표의 질문 평균 튜플) · (그 밖에 01~07절 함수 열 개를 같은 코드로 다시 정의).
- **07절과 달라진 두 가지**: 후보를 목록의 목록(`candidate_lists`)이 아니라 **질문 ID를 키로 하는 딕셔너리(`candidate_sets`)**로 담습니다(실습 폴더 테스트가 그 이름을 씁니다). 07절 `make_pairs`·`rerank`는 `score_candidates`·`order_by_score` 둘로 갈렸습니다.

### 출력 라벨 (08절 전부)

「langchain-openai:」「python-dotenv:」「kiwipiepy:」「rank-bm25:」「sentence-transformers:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「부모 문서 수:」「문서 청크 수:」「질문 수:」「개발 질문 수:」「시험 질문 수:」「첫 개발 질문:」「그 질문의 정답 부모 문서 ID:」「남길 품사 표시:」「순위 상수:」「같은 가중치:」「견줄 후보 수 세 가지:」「부모 문서 재현율을 재는 자리:」「보고 자리:」「견줄 방법 세 가지:」「이어 붙인 글 수:」「첫 문서 청크 ID:」「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 청크 벡터 수:」「질문 벡터 수:」「검색 낱말 목록 수:」「BM25 모델이 본 문서 청크 수:」「문서 청크 하나의 평균 검색 낱말 수:」「만든 후보 목록 수:」「후보 목록 하나의 문서 청크 수:」「점수를 낸 방법 수:」「리랭커 A:」「리랭커 B:」「한 쌍에서 읽는 최대 조각 수:」「방법 | 후보 수 | 부모 문서 재현율 자리 3 | 문서 청크 정밀도 자리 5」(라벨 줄 따로)「질문 | 난이도 | 1차 후보 | 리랭커 A | 리랭커 B」(라벨 줄 따로)「방법 | 후보 수 | 부모 문서 재현율 자리 3 | 문서 청크 정밀도 자리 3」(라벨 줄 따로)

### 실행값 (2026-09-18 마지막 새 커널, 두 실행이 같음)

- `부모 문서 수: 6` · `문서 청크 수: 175` · `질문 수: 30` · `개발 질문 수: 15` · `시험 질문 수: 15` · `문서 청크 하나의 평균 검색 낱말 수: 44.01`(07절과 같음).
- `만든 후보 목록 수: 15` · `후보 목록 하나의 문서 청크 수: 8` · `점수를 낸 방법 수: 3` · `한 쌍에서 읽는 최대 조각 수: 256`.
- **아홉 줄(보고 자리 5)**: 부모 문서 재현율 자리 3은 **아홉 줄 모두 `1.0`**. 문서 청크 정밀도는 1차 후보 `0.4`·`0.693`·`0.84`, 리랭커 A `0.4`·`0.693`·`0.893`, 리랭커 B `0.4`·`0.693`·`0.867`.
- **질문별 표(후보 8)**: 값이 갈린 네 줄은 `Q002 | easy | 1.0 | 1.0 | 0.8`·`Q003 | easy | 0.6 | 0.8 | 0.6`·`Q005 | easy | 0.4 | 0.6 | 0.6`·`Q038 | medium | 0.6 | 1.0 | 1.0`. 나머지 열한 줄은 세 방법이 같습니다.
- **값 바꿔 보기(보고 자리 3)**: 후보 8의 세 줄이 모두 `0.933`, 후보 4는 1차 후보·리랭커 A `0.933`과 리랭커 B `0.911`, 후보 2는 세 줄 모두 `0.667`.
- 리랭커 준비 셀 출력 맨 위에 HF 토큰 없이 받았다는 영문 알림 한 줄이 남습니다(07절과 같음).

### 천장을 다룬 방식과 결론 한정 — 09절도 같은 규칙으로

- **부모 문서 재현율은 아홉 줄 모두 `1.0`이라 설정을 가르지 못했습니다.** 표에서 빼지 않고 「이 조건에서는 가를 수 없다」를 본문 b6·b7과 복습 1번에 적었습니다.
- **천장을 푼 방법은 「보고 단위 바꾸기 + 후보 수 크게 줄이기」였습니다.** 탐색에서 자르는 자리 낮추기와 nDCG는 값이 그대로여서 버렸습니다(`08-diagnosis.md` §3 표). 09절도 부모 6건 안에서 재현율을 재면 천장에 닿습니다. **부모 수·중복 제거 뒤 남은 부모 수·부모 글자 수처럼 천장이 없는 값**을 먼저 보세요.
- **어느 리랭커가 낫다고 쓰지 않았습니다.** 후보 8의 차이 `0.893` vs `0.867`은 열다섯 질문 가운데 두 질문에서 나왔습니다.
- **걸린 시간을 재지 않았습니다.** 개선 전 08절 표의 시간 칸은 후보 수별 시간이 아니어서 본문이 단서를 네 번 되풀이했습니다. 흔들리는 값이라 아예 뺐습니다.
- **가상 수계산 표를 뺐습니다.** 실제 출력이 아닌 값을 교재 표로 싣지 않습니다(규격 §3).
- Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과 01~06절 core 벌 값은 이 절에서도 나란히 놓지 않았습니다.

### 용어 (08절이 더한 세 개, 09~12도 같게)

- **후보 수(candidate count)** · **보고 자리(report place)** · **문서 청크 정밀도(chunk precision)**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 4 → **3**」입니다.
- **「보고 자리」**는 검색 결과에서 다음 단계로 넘길 문서 청크 수입니다. 05·06절 「자르는 자리」(지표를 재는 자리)와 뜻이 겹치지 않게 말을 갈랐습니다. 재현율은 「자리 3」, 정밀도는 「보고 자리 5」로 부릅니다.
- **「문서 청크 정밀도」**는 Ch 11 「정밀도」와 나누는 수가 같고 세는 단위만 다릅니다. 「정밀도」 단독으로 쓰지 않았습니다.
- **「리랭커 A」·「리랭커 B」**는 표와 그림의 칸 이름입니다. 모델 이름은 준비 셀 출력과 b10 참고 자료에 적었습니다. 모델 이름으로 우열을 말하지 않으려고 칸 이름을 A·B로 두었습니다.
- 01~07절 말 서른아홉 개와 Ch 9~11 말을 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**이고 한정어 없는 「청크」는 쓰지 않았습니다.
- 쓰지 않은 말: 「가상 수계산」, 「포화」(→ 천장에 닿음), 「격자」(→ 아홉 줄), 「top-k」·「Recall@3」·「nDCG@5」(→ 자리 3 재현율·문서 청크 정밀도 자리 5), 「로짓」, 「임계값」, 「TF-IDF」.

### 파일 쓰기 규칙 — 08절도 파일을 쓰지 않습니다

- `runs/`는 파일 **36개** 그대로이고 내용만 이어 붙인 해시가 **`a17a42dd4d6af8957d213b6b61c7be431906f3f90c1e3deea1bb238a004c5c51`**로 작업 전과 같습니다.
- `advanced-documents.json`·`advanced-queries.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않았습니다.
- `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…` 그대로입니다. `%pip` 목록 다섯 개는 07절과 같고 모두 잠금에 있으며 dev `pip==26.2`도 그대로입니다.
- 공용 화면 검사 결과 `visual-results.json`은 **26행 유지**이고 바이트가 `49352bfcd3f7e511…`로 그대로입니다.
- `textbook/part3/qa/check_delivery.py`는 끝까지 통과(종료 코드 0), `textbook/part3/qa/check_continuity.py`는 01절 기준과 같은 154행 `part2-practice.zip`에서 멈춥니다.

### 실습 폴더 테스트를 고쳤습니다 (09절이 꼭 볼 것)

- `labs/part3/ch12-retrieval-tuning/tests/test_continuity.py`는 **작업 전후 모두 4 passed**입니다. 다음 세 곳을 고쳤습니다.
  1. **`code_cell_trees()`를 더해 `%pip` 셀을 건너뜁니다.** 07절부터 노트북 첫 셀에 `%pip`이 있어 `ast.parse`가 SyntaxError를 냅니다. 이 한 줄이 없으면 테스트가 통째로 실패합니다. 09~12절 노트북에도 `%pip` 셀이 생기므로 그대로 두세요.
  2. **`load_notebook_namespace()`를 더했습니다.** 노트북의 함수 정의를 한 이름 공간에 모아 서로 부를 수 있게 합니다. 사다리에 맞춰 나눈 함수는 서로를 부르므로 함수 하나만 따로 컴파일하는 옛 방식으로는 돌아가지 않습니다.
  3. 08절 확인 블록의 넣는 값을 문서 청크 ID 모양으로 바꿨습니다(`parent_by_chunk`·`candidate_sets`·`recall_place`·`report_place`). 중복 정답 ID를 한 번만 세는지 보는 확인 한 줄을 더했습니다.
- **10·12절 확인 블록은 손대지 않았습니다.** `load_notebook_function("10-MMR-다양성-선택.ipynb", "mmr")`·`("12-…", "eligible_items"/"metrics"/"mmr"/"evaluate_config")`가 그대로입니다. 10·12절을 다시 쓸 때 그 이름·인자·반환을 지키거나 `load_notebook_namespace()`로 바꾸세요. 12절 `evaluate_config`는 namespace로 `eligible_items`·`TfidfVectorizer`·`chunks`·`mmr`·`metrics`를 받습니다.
- 09절과 11절은 테스트 대상이 아닙니다.

### 09절이 이어받을 연결과 확인할 것

- 08 b8·노트북 정리 끝: 「09절에서는 작은 문서 청크로 찾은 뒤 부모 문서를 통째로 넘기는 방법을 봅니다.」 09절 `_src` b2·b4와 노트북 셀 4·6·8을 열어 확인하고 쓴 문장입니다.
- **07·08절 코드를 그대로 이어 쓸 수 있습니다**: 후보 만들기(`rank_by_distance`·`rank_by_bm25`·`unique_chunk_ids`·`fuse_scores`·`fuse_rank`)와 `parent_ids_of`·`recall_at`·`chunk_precision_at`·`eligible_items`. 09절의 「자식 청크 순위에서 부모 ID를 뽑고 중복을 뺀다」는 **`parent_ids_of()`가 이미 하는 일**입니다(07절부터 같은 코드). 새 함수를 만들지 말고 그 함수를 쓰세요.
- **개선 전 09 노트북이 하는 일**(셀 9개, 코드 4개): 문자 단위 TF-IDF로 `Q001`의 자식 청크를 재고 1위 자식의 부모 원문을 출력합니다. 이어서 `parent_document_search(question, child_k=8, parent_k=3)`으로 `child_k`를 3·8·20으로 바꿔 부모 ID 목록을 견줍니다.
- **개선 전 09 노트북의 출력(참고용)**: `부모 문서 6건 · 자식 청크 175개 · 평가 질문 30개`, 자식 1위와 부모 글자 수(2천 자 넘음), `child_k` 3·8·20에서 고유 부모 2·2·3개. **TF-IDF로 잰 값이라 07·08절 1차 검색으로 바꾸면 값이 달라집니다.** 다시 재세요.
- **개선 전 09 노트북이 쓰는 것 가운데 01~08절에서 안 가르친 것**: `numpy`(`np.argmax`·`np.argsort`), `sklearn`(`TfidfVectorizer`·`cosine_similarity`), 제너레이터 식 `next(...)` 두 곳, `set`과 `seen.add`, 기본값 매개변수(`child_k=8, parent_k=3`), 한 줄에 두 이름 대입(`result, seen = [], set()`), `Path`·`read_text`, f-string, `assert question["split"] == "dev"`. **`parent_k`(부모를 몇 건까지 넘길지)는 이 챕터에서 처음 나오는 설정**이라 처음 쓰는 자리에서 뜻을 풀어야 합니다.
- **09절이 견줄 값**: `child_k`(자식 후보 수)는 08절 `candidate_counts`와 같은 자리의 설정입니다. 이름을 맞출지(`candidate_counts`) 09절 말로 둘지 정하고 진단에 적으세요. 부모 문서가 6건뿐이라 **부모 문서 재현율은 또 천장에 닿습니다**. 부모 수·부모 글자 수·중복이 빠진 자리처럼 천장이 없는 값을 함께 내세요.
- **본문 b3 고칠 곳**: 개선 전 09 b3는 「앞 절의 변수나 실행 상태는 필요하지 않습니다」로 끝나고 07·08절을 가리키지 않습니다. 07절 리랭킹·08절 보고 자리와 이어 쓰세요. b2 둘째 문단의 「Ch11에서 만든 질문…」도 07·08절과 같은 문장으로 맞추세요.
- **`{{svg:09-부모-자식-검색}}`**: 09 b4에 옛 excalidraw 토큰이 남아 있습니다. Mermaid 3~5장으로 바꾸고 옛 파일은 `qa/upgrade/before/figures/`에 보존하세요(01~08절과 같은 처리).
- **절 meta 시수**: 08절을 실습 1h → 3h로 올려 절 합이 강의 12h(= 챕터 12h)·실습 **26h**입니다. `chapter.json` 실습 28h와 **2h** 차이가 남습니다. 09~12절에서 2h를 채우면 맞습니다(예: 두 절을 1h → 2h). 강사 확인 대상으로 챕터 요약에 남기세요.
- **아직 안 가르친 것(09가 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01~07절 목록에 더해, 08절에서도 하지 않은 것 — 걸린 시간 재기, nDCG 계산(Ch 11에서 배웠지만 01~08절은 재현율과 정밀도만), 후보 수 8보다 크게 두기, `max_length` 바꿔 견주기, 점수 기준값·거르기, 부모 문서를 통째로 넘기기(09절), 부모 몇 건까지 넘길지 정하기(09절), MMR(10절), 질문 재작성(11절), 답을 쓰는 모델 호출(11·12절), 시험 15문항 보기(12절).

## §09 → §10

(09절 품질 개선 2026-09-18. 결과는 `09-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 25 = G1 5·G2 0·G3 4·G4 0·G5 6·G6 7·G7 3), 코드 셀 **32**(준비 21, 07·08절 37·33에서 줄임), 검사 문장 306, **임베딩 요청 16번**(문서 청크 1 + 개발 질문 15, 0.01달러 아래), 리랭커 0번·답을 쓰는 모델 0번. 새 커널 세 번 실행에 `code_sha256` `493506d5c3591bf9`가 같고 교재 출력은 마지막 실행 2026-09-18T20:52:05Z. 노트북 전체 6~8초. `verify.py --chapter` `PASS 12 sections / 333 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(1차 job `422d3a4c-ce17-4d93-91ad-49f1f0d9257e` 채택, 재생성 없음, 2크레딧, 생성 전 잔액 2719))

### 작업 환경 — 10절이 먼저 읽을 것

- **09절은 리랭커와 pgvector를 쓰지 않아 가볍습니다.** 노트북 실행 6~8초, `run_section.sh … 09 --no-exec` 11초입니다. 10절도 MMR만 쓰면 한 호출로 끝납니다.
- 리랭커 모델 두 개는 `.cache/vm/hf`(6.0GB)에 그대로 있습니다. 09절은 건드리지 않았습니다.
- **`visual.cjs`를 돌릴 때 `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`를 주세요.** 없으면 chrome이 `libXdamage.so.1`을 못 찾아 종료 코드 127로 조용히 실패하고 `visual-results.json`이 갱신되지 않습니다(09절에서 한 번 겪음). 명령은 `ONLY=10- node /tmp/ch12-09/vis12.cjs textbook/part3/ch12-retrieval-tuning`입니다(`/tmp/ch12-09/vis12.cjs`는 08절 사본).
- `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/pw`·`/tmp/libs`·`/tmp/uv-cache`는 그대로입니다. 루트 디스크 여유 2.2G.
- 08절이 남긴 `labs/part3/ch12-retrieval-tuning/.venv`(빈 폴더)는 그대로 두었습니다(챕터 마감 때 삭제 대상).

### 09절이 새로 가르친 것

- **부모 문서 넘기기**: 후보 문서 청크 → `parent_ids_of()`(07절, 중복 제거 포함) → **`parent_texts_of(found_chunk_ids, parent_limit)`**(6줄, 새 함수 하나)로 넘길 글 목록을 만듭니다.
- **넘길 부모 수(`parent_limit`)**: 부모 문서를 몇 건까지 넘길지 정한 수. 08절 「보고 자리」를 부모 단위로 옮긴 설정입니다.
- **길이를 조각 수로 재기(Ch 8 01절 자를 그대로)**: `tiktoken.encoding_for_model("gpt-5.4-mini")`(규칙 `o200k_base`) · `count_tokens(text)`(Ch 8 01절과 같은 코드) · **`total_tokens(text_list)`** · 수업 예산 `total_budget`·출력 예약분 `output_reserve`·여유분 `safety_margin`·입력 가용분 `available`. 단위 이름은 이 챕터 말인 **「조각」**이고 Ch 8 「토큰」과 같은 단위임을 b4에 한 문장으로 이었습니다.
- **`summarize(text_lists)`**: 넘길 글 목록 열다섯 벌을 받아 (글 수 평균, 조각 수 평균, 입력 가용분에 든 질문 수)를 냅니다.
- **쓰지 않은 것**: `numpy` import·`sklearn`·`lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`목록.index`·`Path`·`hashlib`·`datetime`·f-string·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`sorted`뿐입니다.

### 이어 쓸 이름과 값 (09절)

- 값: `similarity_top`(1) · `keep_tags`(아홉 개) · `rank_constant`(60) · `equal_weights`(`[1.0, 1.0]`) · `candidate_count`(8) · `candidate_counts`(`[2, 4, 8]`) · `recall_place`(3) · `report_place`(5) · **`parent_limit`(2, 값 바꿔 보기에서 1)** · **`total_budget`(4000)**·**`output_reserve`(500)**·**`safety_margin`(100)**·**`available`(3400)**.
- 자료(07·08절과 같은 이름): `candidates` · `root_path` · `data_path` · `documents` · `queries`(30) · `parents`(6) · `chunks`(175) · `dev_all` · `dev_queries`(15) · `chunk_texts` · `chunk_ids` · `parent_by_chunk` · `text_by_chunk` · `all_chunk_count`(175) · `embedding_model_name` · `vector_dimensions`(256) · `chunk_vectors` · `query_vectors` · `kiwi` · `kiwi_corpus` · `bm25_model` · `candidate_sets`(질문 ID → 후보 여덟 개).
- 09절이 새로 만든 이름: **`parent_text_by_id`**(부모 ID → 제목 + 본문) · **`encoding`** · **`chunk_lists`**·**`parent_lists`**·**`small_lists`**(질문마다 넘길 글 목록) · `chunk_row`·`parent_row`·`small_row` · `example_index`(1)·`example_id`(`Q002`)·`example_found`·`example_parents`·`example_texts`·`example_tokens`.
- 09절이 새로 만든 함수 네 개(괄호 안은 본문 줄 수): **`count_tokens(text)`**(2, Ch 8 01절 코드) · **`total_tokens(text_list)`**(4) · **`parent_texts_of(found_chunk_ids, parent_limit)`**(5) · **`summarize(text_lists)`**(10). 그 밖에 01~08절 함수 열두 개를 같은 코드로 다시 정의했습니다.
- **준비 셀 묶음(10절이 이어 쓰면 편한 방법)**: 앞 절 함수 열두 개를 **준비 셀 여덟 개**에 나눠 담았습니다(`code(SRC, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"])`, 생성기 `prep()` 도우미). G1 `multiple_defs_in_cell`과 G5 앞뒤 설명 셀 검사를 함께 피해 코드 셀이 32개로 줄었습니다. 노트북 5절 머리말에 묶은 까닭을 한 문장 적었습니다.

### 출력 라벨 (09절 전부)

「langchain-openai:」「python-dotenv:」「kiwipiepy:」「rank-bm25:」「tiktoken:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「부모 문서 수:」「문서 청크 수:」「질문 수:」「개발 질문 수:」「시험 질문 수:」「첫 개발 질문:」「그 질문의 정답 부모 문서 ID:」「남길 품사 표시:」「순위 상수:」「같은 가중치:」「후보 수:」「견줄 후보 수 세 가지:」「보고 자리:」「넘길 부모 수:」「이어 붙인 글 수:」「첫 문서 청크 ID:」「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 청크 벡터 수:」「질문 벡터 수:」「검색 낱말 목록 수:」「BM25 모델이 본 문서 청크 수:」「문서 청크 하나의 평균 검색 낱말 수:」「만든 후보 목록 수:」「후보 목록 하나의 문서 청크 수:」「토큰화 규칙 이름:」「수업 예산:」「출력 예약분:」「여유분:」「입력 가용분:」「부모 문서 ID | 글자 수 | 조각 수」(라벨 줄 따로)「고른 질문:」「후보의 부모 문서 차례:」「후보 수 | 부모 문서 차례」(라벨 줄 따로)「넘길 부모 두 건의 조각 수 합:」「입력 가용분에 드는가:」「만든 글 목록 벌 수:」「넘기는 단위 | 글 수 평균 | 조각 수 평균 | 입력 가용분에 든 질문 수」(라벨 줄 따로)「부모 문서 재현율 자리 3:」「문서 청크 정밀도 자리 5:」「넘긴 부모 목록의 재현율:」

### 실행값 (2026-09-18 마지막 새 커널)

- `부모 문서 수: 6` · `문서 청크 수: 175` · `개발 질문 수: 15` · `문서 청크 하나의 평균 검색 낱말 수: 44.01`(07·08절과 같음) · `만든 후보 목록 수: 15`.
- **부모 문서 여섯 건(글자 수 | 조각 수)**: `E01 | 3034 | 1913` · `E02 | 2747 | 1799` · `H01 | 4964 | 3172` · `H02 | 4400 | 2940` · `M01 | 3917 | 2421` · `M02 | 4938 | 3283`.
- 예산: `토큰화 규칙 이름: o200k_base` · `수업 예산: 4000` · `출력 예약분: 500` · `여유분: 100` · `입력 가용분: 3400`.
- 실행 1(`Q002`, 07절과 같은 질문·같은 후보 여덟 개): `후보의 부모 문서 차례: ['E01', 'E02']` · `넘길 부모 두 건의 조각 수 합: 3712` · `입력 가용분에 드는가: False`. 후보 수별 부모 차례 `2 | ['E01']` · `4 | ['E01']` · `8 | ['E01', 'E02']`.
- **두 줄 표(후보 8, 넘길 부모 수 2)**: `문서 청크 | 5.0 | 596 | 15` · `부모 문서 | 1.6 | 4206 | 6`.
- 지표: `부모 문서 재현율 자리 3: 1.0` · `문서 청크 정밀도 자리 5: 0.853` · `넘긴 부모 목록의 재현율: 1.0`.
- 값 바꿔 보기(넘길 부모 수 1): `부모 문서 | 1.0 | 2502 | 15` · `넘긴 부모 목록의 재현율: 1.0`.

### 실행마다 흔들리는 값 두 개 — 10~12절이 꼭 볼 것

- 같은 코드로 새 커널에서 **세 번** 실행했고 셀 수·출력 줄·라벨은 모두 같았습니다. 그런데 **문서 청크 다섯 개의 조각 수 평균이 600 ↔ 596**, **문서 청크 정밀도 자리 5가 0.84 ↔ 0.853**으로 갈렸습니다.
- 원인은 임베딩 값이 호출마다 미세하게 달라 한 질문(`Q038`)의 앞자리 문서 청크가 바뀌기 때문입니다. **부모 쪽 값(고유 부모 수·부모 조각 수·입력 가용분에 든 질문 수)과 두 재현율은 세 번 모두 같았습니다.**
- 규격 §3대로 다시 돌려 고르지 않고 마지막 실행을 교재 출력으로 두었습니다. b7에 「같은 글을 보내도 임베딩 값이 호출마다 아주 조금 달라질 수 있습니다」와 08절 표 `0.84`와의 차이를 적었습니다.
- **10~12절도 1차 후보의 앞자리를 인용할 때 이 흔들림을 셈에 넣으세요.** 문서 청크 단위 값은 재실행하면 소수 셋째 자리가 바뀔 수 있고, 부모 단위 값은 이 자료에서 안정적이었습니다.

### 천장을 다룬 방식과 결론 한정 — 10절도 같은 규칙으로

- **부모 문서 재현율 자리 3과 넘긴 부모 목록의 재현율이 모두 `1.0`입니다.** 넘길 부모 수를 1로 줄여도 그대로라 표·그림에 값만 싣고 「이 조건에서는 가를 수 없다」를 b6·b7·복습 3번에 적었습니다.
- **가른 값은 길이 쪽입니다**: 고유 부모 수(후보 2·4·8에서 1.0·1.47·2.07, 본문에는 `Q002` 예만 실음) · 조각 수 평균 · 입력 가용분에 든 질문 수. 10절도 부모 6건 안에서 재현율을 재면 또 천장에 닿습니다.
- **답 품질을 재지 않았습니다.** 답을 쓰는 모델을 부르지 않았으므로 「부모를 넘기면 답이 좋아진다」는 쓰지 않았습니다(b6 마지막 단락·복습 4번).
- **걸린 시간을 재지 않았습니다**(07·08절과 같음).
- Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과 01~06절 core 벌 값은 이 절에서도 나란히 놓지 않았습니다.

### 용어 (09절이 더한 세 개, 10~12도 같게)

- **부모 문서 넘기기(parent document retrieval)** · **넘길 부모 수(parent limit)** · **입력 가용분(input budget)**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 4 → **3**」입니다.
- **「입력 가용분」은 Ch 8 01절과 같은 뜻**입니다(수업 예산 − 출력 예약분 − 여유분). 「출력 예약분」·「여유분」·「수업 예산」도 그 절 이름 그대로입니다.
- **「조각」은 Ch 5 토큰 뜻 전용**이고 이 절에서 길이 단위로 씁니다. Ch 8이 「토큰」이라 부른 것과 같은 단위임을 b4에 한 문장으로 이었습니다. 한정어 없는 「청크」는 쓰지 않았습니다.
- **「자식 청크」를 쓰지 않았습니다.** 개선 전 09절이 쓰던 말인데 챕터 용어 표에 없어 「문서 청크」와 「부모 문서」 두 말로만 적었습니다.
- 01~08절 말 마흔두 개와 Ch 9~11 말을 그대로 씁니다.
- 쓰지 않은 말: 「자식 청크」, 「원문」(→ 부모 문서), 「문맥」, 「반환」(→ 넘기기), 「top-k」·「child_k」·「parent_k`」, 「임계값」, 「포화」(→ 천장에 닿음), 「TF-IDF」.

### 파일 쓰기 규칙 — 09절도 파일을 쓰지 않습니다

- `runs/`는 파일 **36개**·`core-history/` 12개 그대로이고 **내용만 이어 붙인 해시 `d3d6478c0790e11e045c518edd1356e20c29ce0d33156722221fc5947e4a107a`**로 05·06·07절 기록과 같습니다. (08절이 적은 `a17a42dd…`는 세 가지 계산법으로 재현하지 못했습니다. `find … | sort | xargs cat | sha256sum`를 쓰세요.)
- `advanced-documents.json`·`advanced-queries.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않았습니다.
- `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…` 그대로입니다. **`%pip` 목록 다섯 개에서 `sentence-transformers==6.0.1` 자리에 `tiktoken==0.14.0`을 넣었습니다.** 그 항목은 `langchain-openai`를 따라 잠금 1617행에 0.14.0으로 이미 있고 dev `pip==26.2`도 그대로라 학생 `.venv`에서 첫 셀이 멈추지 않습니다. **`pyproject.toml`에 `tiktoken`을 직접 적지는 않았습니다**(잠금을 고치지 않으려고). 10절이 tiktoken을 쓰면 같은 판단을 이어 쓰세요.
- 공용 화면 검사 결과 `visual-results.json`은 **26행 유지**이고 바이트가 `49352bfcd3f7e511…`로 그대로입니다.
- `textbook/part3/qa/check_delivery.py`는 끝까지 통과(종료 코드 0), `textbook/part3/qa/check_continuity.py`는 01~08절과 같은 154행 `part2-practice.zip`에서 멈춥니다.

### 실습 폴더 테스트 — 10절은 대상입니다 (꼭 읽을 것)

- `labs/part3/ch12-retrieval-tuning/tests/test_continuity.py`는 09절 작업 전후 모두 **4 passed**입니다. 09절은 테스트 대상이 아니라 파일을 고치지 않았습니다.
- **166~168행이 10절 노트북의 `mmr`을 `ast`로 찾아 실제로 실행합니다**: `mmr(np.array([[1.0, 0.0]]), np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]]), k=3)`을 부르고 고른 자리 세 개가 서로 달라야 통과합니다. **넘파이 배열을 인자로 줍니다.**
- 10절을 사다리에 맞춰 numpy 없이 다시 쓰면 이 호출이 깨집니다. 08절이 한 것처럼 **테스트가 요구하는 이름·인자·반환만 지키고 몸통을 다시 쓰거나**, 08절이 넣은 `load_notebook_namespace()`로 바꾸고 테스트의 넣는 값을 파이썬 목록으로 고치세요(고치면 `09-diagnosis.md` §8 모양으로 진단에 적기).
- 12절 확인 블록(`eligible_items`·`metrics`·`mmr`·`evaluate_config`)은 그대로입니다.

### 10절이 이어받을 연결과 확인할 것

- 09 b8·노트북 정리 끝: 「10절에서는 넘길 목록에서 서로 닮은 문서 청크를 줄이는 MMR을 봅니다.」 10절 `_src` b2·b4와 노트북 셀 1·4·6을 열어 확인하고 쓴 문장입니다.
- **07~09절 코드를 그대로 이어 쓸 수 있습니다**: 후보 만들기(`rank_by_distance`·`rank_by_bm25`·`unique_chunk_ids`·`fuse_scores`·`fuse_rank`)·`parent_ids_of`·`recall_at`·`chunk_precision_at`·`eligible_items`·`count_tokens`·`total_tokens`·`parent_texts_of`·`summarize`. **MMR은 이미 만든 `cosine_similarity()`로 잴 수 있습니다**(01절 함수, 벡터 두 개를 받음). 후보 벡터는 `chunk_vectors`에서 `chunk_ids.index()` 없이 후보를 만들 때 함께 담아 두는 쪽이 사다리에 맞습니다.
- **개선 전 10 노트북이 하는 일**(셀 9개, 코드 4개): 문자 단위 TF-IDF 행렬에서 `mmr(query_vector, candidate_matrix, k=5, lambda_mult=0.5)`을 돌려 λ 1.0·0.5·0.2에서 고른 자리와 고유 부모 수를 보고, λ=0.2에서 관련성 점수를 함께 출력합니다.
- **개선 전 10 노트북이 쓰는 것 가운데 01~09절에서 안 가르친 것**: `numpy`(`np.argmax`), `sklearn`(`TfidfVectorizer`·`cosine_similarity` 행렬 판), `max(remaining, key=lambda i: ...)`, 기본값 매개변수 `k=5, lambda_mult=0.5`, 한 줄에 두 이름 대입(`selected, remaining = [], list(...)`), `while`과 `remaining.remove()`, `.max(axis=1)`, `set`, f-string 형식 지정(`f"{value:.1f}"`), 제너레이터 식 `next(...)`, `Path`·`read_text`.
- **10절이 견줄 값**: λ(`lambda_mult`)은 이 챕터에서 처음 나오는 설정입니다. **부모 6건 안에서 재현율을 재면 또 천장**이므로, 09절처럼 **천장이 없는 값**(고른 문서 청크의 고유 부모 수, 넘길 글의 조각 수, 08절 문서 청크 정밀도 자리 5)을 함께 내세요. 09절이 만든 `summarize()`와 예산 값을 그대로 쓰면 「다양성을 올리면 넘길 글이 어떻게 달라지는가」를 같은 자로 잴 수 있습니다.
- **본문에서 확인할 곳**: 개선 전 10 b3도 앞 절을 가리키지 않습니다. 07·08·09절과 이어 쓰고, b4의 옛 토큰(있으면)을 Mermaid 3~5장으로 바꾸세요. 옛 도식은 `qa/upgrade/before/figures/`에 복사해 두세요.
- **절 meta 시수**: 09절을 실습 1h → 3h로 올려 절 합이 **강의 12h·실습 28h**가 되어 `chapter.json`(총 40h · 강의 12h · 실습 28h)과 **맞았습니다**. 10~12절은 지금 1h씩이고, 올리려면 다른 절을 내려야 합니다(강사 확인 대상으로 챕터 요약에 남길 것).
- **아직 안 가르친 것(10이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01~08절 목록에 더해, 09절에서도 하지 않은 것 — 걸린 시간 재기, nDCG, 답을 쓰는 모델 호출(11·12절), 실제 요청 사용량 확인, 부모 글에서 질문과 무관한 대목의 몫 재기, 넘길 부모 수 3 이상, MMR(10절), 질문 재작성(11절), 시험 15문항 보기(12절).

## §10 → §11

(10절 품질 개선 2026-09-18. 결과는 `10-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 31 = G1 6·G2 2·G3 4·G4 0·G5 5·G6 11·G7 3), 코드 셀 **31**(준비 5 + 앞 절 함수 9), 검사 문장 309, **임베딩 요청 16번**(문서 청크 1 + 개발 질문 15, 0.01달러 아래), 리랭커 0번·답을 쓰는 모델 0번. 새 커널 두 번 실행에 `code_sha256` `3fc1bf38…`·셀별 출력 글자 해시 `77772b52…`·`outputs_sha256` `0637b5f7…`가 모두 같고 교재 출력은 마지막 실행 2026-09-18T21:32:22Z. 노트북 전체 20초 안팎. `verify.py --chapter` `PASS 12 sections / 360 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(1차 job `865a8de9-0ebe-4b26-8f96-6aa1f0bbd37d` 채택, 재생성 없음, 2크레딧, 생성 전 잔액 2717))

### 작업 환경 — 11절이 먼저 읽을 것

- **10절도 가볍습니다.** 노트북 실행 20초, `run_section.sh … 10 --no-exec` 15초입니다. 11절은 답을 쓰는 모델을 부르므로(개선 전 `gpt-4.1-mini` 1번) 그만큼 더 걸립니다.
- **`visual.cjs`에 `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`를 꼭 주세요**(09절 인계와 같음). 명령은 `ONLY=11- node /tmp/ch12-10/vis12.cjs textbook/part3/ch12-retrieval-tuning`입니다(`/tmp/ch12-10/vis12.cjs`는 09절 사본).
- `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/pw`·`/tmp/libs`·`/tmp/uv-cache`는 그대로입니다. 루트 디스크 여유 2.2G. 리랭커 모델 두 개(`.cache/vm/hf` 6.0GB)는 10절도 건드리지 않았습니다.
- 탐색 스크립트는 `/tmp/ch12-10/probe1.py`~`probe3.py`, 실행 사본은 `/tmp/ch12-10/run1.ipynb`·`run2.ipynb`, 출력 글자 해시 도구는 `/tmp/ch12-10/celltext.py`입니다.

### 10절이 새로 가르친 것

- **MMR(최대 주변 관련성)**: 후보 하나의 점수 = 질문과의 유사도 × 관련성 비중 − 이미 고른 것과 가장 닮은 정도 × 나머지 비중. 점수가 가장 큰 후보를 하나씩 고릅니다.
- **함수 다섯 개로 나눴습니다**(괄호 안은 본문 줄 수): `similarity_to_chosen(candidate_vectors, chosen, index)`(5) · `mmr_score(question_vector, candidate_vectors, chosen, index, relevance_weight)`(4) · `best_candidate(question_vector, candidate_vectors, chosen, relevance_weight)`(9) · **`mmr(question_vector, candidate_vectors, pick_count, relevance_weight)`**(7) · `mmr_pick(question_vector, found_chunk_ids, place, relevance_weight)`(8).
- **닮은 정도는 01절 `cosine_similarity()`로 잽니다**(새 자를 만들지 않음). 나머지 비중은 01절 `similarity_top`(1)에서 관련성 비중을 뺀 값입니다.
- **고유 부모 수**: 고른 문서 청크의 부모를 중복 없이 센 수. 07절 `parent_ids_of()` 목록의 길이입니다.
- **쓰지 않은 것**: `numpy` import·`sklearn`·`tiktoken`·`lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`목록.index`·`목록.remove`·`Path`·f-string·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`sorted`뿐입니다.

### 이어 쓸 이름과 값 (10절)

- 값: `similarity_top`(1) · `keep_tags`(아홉 개) · `rank_constant`(60) · `equal_weights`(`[1.0, 1.0]`) · `candidate_count`(8) · `recall_place`(3) · **`report_place`(5, 값 바꿔 보기에서 3)** · **`relevance_weights`(`[1.0, 0.5, 0.2]`)**.
- 자료(07~09절과 같은 이름): `candidates` · `root_path` · `data_path` · `documents` · `queries`(30) · `parents`(6) · `chunks`(175) · `dev_all` · `dev_queries`(15) · `chunk_texts` · `chunk_ids` · `parent_by_chunk` · `all_chunk_count`(175) · `embedding_model_name` · `vector_dimensions`(256) · `chunk_vectors` · `query_vectors` · `kiwi` · `kiwi_corpus` · `bm25_model` · `candidate_sets`(질문 ID → 후보 여덟 개).
- 10절이 새로 만든 이름: **`vector_by_chunk`**(문서 청크 ID → 벡터) · **`vector_by_query`**(질문 ID → 벡터) · `example_index`(10)·`example_id`(`Q085`)·`example_found`·`example_gold`·`example_picked`·`example_parents`·`example_precision` · `small_picked`·`small_parents`·`small_precision` · `mmr_row`(비중 하나의 질문 평균 세 값).
- **09절 이름 가운데 쓰지 않은 것**: `text_by_chunk`·`parent_text_by_id`·`encoding`·`count_tokens`·`total_tokens`·`parent_texts_of`·`summarize`·`parent_limit`·예산 네 값. 10절은 길이를 재지 않습니다.
- **준비 셀 묶음**(09절 방식 그대로): 앞 절 함수 **열세 개를 준비 셀 아홉 개**에 담았습니다(`code(SRC, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"])`, 생성기 `prep()` 도우미). 노트북 5절 머리말에 묶은 까닭을 한 문장 적었습니다.

### 출력 라벨 (10절 전부)

「langchain-openai:」「python-dotenv:」「kiwipiepy:」「rank-bm25:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「부모 문서 수:」「문서 청크 수:」「질문 수:」「개발 질문 수:」「시험 질문 수:」「첫 개발 질문:」「그 질문의 정답 부모 문서 ID:」「코사인 유사도의 가장 큰 값:」「남길 품사 표시:」「순위 상수:」「같은 가중치:」「후보 수:」「부모 문서 재현율을 재는 자리:」「보고 자리:」「견줄 관련성 비중 세 가지:」「이어 붙인 글 수:」「첫 문서 청크 ID:」「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 청크 벡터 수:」「질문 벡터 수:」「검색 낱말 목록 수:」「BM25 모델이 본 문서 청크 수:」「문서 청크 하나의 평균 검색 낱말 수:」「만든 후보 목록 수:」「후보 목록 하나의 문서 청크 수:」「고른 질문:」「후보의 부모 문서 차례:」「1차 자리 | 문서 청크 ID | 부모 문서 ID」(라벨 줄 따로)「관련성 비중 | 고른 문서 청크 ID」(라벨 줄 따로, 비중마다 세 줄)「  고유 부모 수:」「  문서 청크 정밀도 자리 5:」「관련성 비중 | 고유 부모 수 평균 | 문서 청크 정밀도 자리 5 | 부모 문서 재현율 자리 3」(라벨 줄 따로)「관련성 비중 | 고른 문서 청크 ID | 고유 부모 수 | 문서 청크 정밀도 자리 3」(라벨 줄 따로)「관련성 비중 | 고유 부모 수 평균 | 문서 청크 정밀도 자리 3 | 부모 문서 재현율 자리 3」(라벨 줄 따로)

### 실행값 (2026-09-18 마지막 새 커널)

- `부모 문서 수: 6` · `문서 청크 수: 175` · `개발 질문 수: 15` · `문서 청크 하나의 평균 검색 낱말 수: 44.01`(07~09절과 같음) · `만든 후보 목록 수: 15`.
- 실행 1(`Q085` = 개발 열한째 질문, 정답 부모 `['H01']`): `후보의 부모 문서 차례: ['H01', 'H02', 'M02']`, 후보 여덟 줄 가운데 **여섯 줄이 `H01`**(`H01-P03-C02`·`H01-P03-C03`·`H01-P04-C05`·`H01-P02-C02`·`H01-P02-C06`·`H01-P03-C04`·`H02-P02-C06`·`M02-P06-C01`).
- 비중별 한 질문: `1.0`은 고유 부모 수 `1`·정밀도 `1.0`, `0.5`와 `0.2`는 고유 부모 수 `3`·정밀도 `0.6`.
- **열다섯 질문 평균(보고 자리 5)**: `1.0 | 1.73 | 0.81 | 1.0` · `0.5 | 2.07 | 0.75 | 1.0` · `0.2 | 2.07 | 0.73 | 1.0`.
- 값 바꿔 보기(보고 자리 3) 한 질문: `1.0`은 부모 수 `1`·정밀도 `1.0`, `0.5`와 `0.2`는 부모 수 `3`·정밀도 `0.33`.
- 값 바꿔 보기 평균: `1.0 | 1.33 | 0.89 | 1.0` · `0.5 | 1.93 | 0.69 | 1.0` · `0.2 | 1.93 | 0.67 | 1.0`.

### 흔들리는 값 — 11·12절도 셈에 넣을 것

- 교재 출력을 만든 두 실행은 셀별 출력 글자까지 같았습니다. 그런데 앞선 탐색 실행 네 번 가운데 한 번은 **고유 부모 수 평균 `1.80`·`2.13`, 정밀도 `0.76`**이 나왔습니다(09절이 적은 임베딩 미세 차이).
- 그래서 **열다섯 질문 평균값은 그림 라벨에 넣지 않았습니다.** 그림 네 장의 숫자는 질문 `Q085` 하나의 값(`1`·`3`·`1.0`·`0.6`·`0.33`)과 구조 숫자(`15`·`175`)뿐이고 네 번 실행에서 모두 같았습니다.
- 11·12절도 **질문 평균을 그림 라벨에 넣을 때는 두 번 이상 실행해 같은지 보고**, 인용은 소수 둘째 자리까지만 하세요.

### 천장을 다룬 방식과 결론 한정 — 11절도 같은 규칙으로

- **부모 문서 재현율 자리 3이 여섯 줄 모두 `1.0`**입니다(비중 세 가지 × 보고 자리 두 가지). 표에 값 그대로 싣고 「이 조건에서는 가를 수 없다」를 b6·b7·복습 3번에 적었습니다.
- **가른 값은 고유 부모 수 평균(다양성)과 문서 청크 정밀도(관련성) 두 가지**이고, 두 값이 서로 반대로 움직이는 맞바꿈을 결론으로 삼았습니다.
- **다양성도 후보 범위를 넘지 못합니다.** 비중을 0.5에서 0.2로 더 낮춰도 고유 부모 수 평균이 `2.07` 그대로였습니다. 07절 「후보 밖은 복구하지 못한다」와 같은 한계입니다.
- **답 품질을 재지 않았습니다.** 답을 쓰는 모델을 부르지 않았으므로 「흩으면 답이 좋아진다」는 쓰지 않았습니다.
- 걸린 시간·조각 수·후보 수 여러 벌·비중 0.2 아래는 실행하지 않았습니다. Ch 11 개발 15문항 값과 01~06절 core 벌 값은 이 절에서도 나란히 놓지 않았습니다.

### 용어 (10절이 더한 세 개, 11~12도 같게)

- **최대 주변 관련성(maximal marginal relevance)** · **관련성 비중(relevance weight)** · **고유 부모 수(unique parent count)**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 4 → **3**」입니다.
- **「관련성 비중」이 λ입니다.** 개선 전 본문이 쓰던 「λ」는 본문에서 쓰지 않고 한국어 말로 적었습니다. 코드 이름도 `lambda_mult`가 아니라 **`relevance_weight`**이고, 라이브러리 이름과 다르다는 것은 b10 참고 자료(LangChain 문서)로 남겼습니다.
- **「닮은 정도」**는 이미 고른 문서 청크와의 코사인 유사도입니다. Ch 9~11의 「겹침」과 다른 말이라 「겹침」을 쓰지 않았습니다.
- 01~09절 말 마흔다섯 개와 Ch 9~11 말을 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**이고 10절은 길이를 재지 않아 쓰지 않았습니다. 한정어 없는 「청크」도 쓰지 않았습니다.
- 쓰지 않은 말: 「λ」(본문), 「다양성 점수」, 「중복 제거」(→ 중복 빼기), 「유사도 행렬」, 「임계값」, 「포화」(→ 천장에 닿음), 「TF-IDF」.

### 파일 쓰기 규칙 — 10절도 파일을 쓰지 않습니다

- `runs/`는 파일 **36개**·`core-history/` 12개 그대로이고 이어 붙인 해시 `d3d6478c0790e11e045c518edd1356e20c29ce0d33156722221fc5947e4a107a`로 05·06·07·09절 기록과 같습니다.
- `advanced-documents.json`·`advanced-queries.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않았습니다.
- `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…` 그대로입니다. **`%pip` 목록은 네 개**(`langchain-openai`·`python-dotenv`·`kiwipiepy`·`rank-bm25`)로 09절에서 `tiktoken`을 뺐고, 네 개 모두 잠금 112~120행에 같은 판으로 있으며 dev `pip==26.2`도 그대로입니다.
- 공용 화면 검사 결과 `visual-results.json`은 **26행 유지**이고 바이트가 `49352bfcd3f7e511…`로 그대로입니다.
- `textbook/part3/qa/check_delivery.py`는 끝까지 통과(종료 코드 0), `textbook/part3/qa/check_continuity.py`는 01~09절과 같은 154행 `part2-practice.zip`에서 멈춥니다.

### 실습 폴더 테스트 — 10절 확인 블록을 고쳤습니다 (11절은 대상이 아님)

- `labs/part3/ch12-retrieval-tuning/tests/test_continuity.py`는 작업 전후 모두 **4 passed**입니다.
- 10절 블록을 `load_notebook_function(... "mmr")` + 넘파이 배열에서 **`load_notebook_namespace("10-…", {"similarity_top": 1, "math": math})` + 파이썬 목록**으로 바꿨습니다. 호출은 `space_10["mmr"]([1.0, 0.0], [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]], pick_count=3, relevance_weight=0.5)`이고 반환 약속(고른 자리 번호 세 개, 서로 다름)은 그대로입니다.
- 파일 맨 위에 `import math` 한 줄을 더했습니다. 08절이 넣은 `code_cell_trees()`(`%pip` 건너뛰기)와 `load_notebook_namespace()`는 그대로 씁니다.
- **12절 확인 블록(`eligible_items`·`metrics`·`mmr`·`evaluate_config`)은 손대지 않았습니다.** 12절 작업자는 그 네 이름의 계약을 먼저 읽으세요. 12절 `mmr`은 10절 것과 **다른 함수**이고 지금은 넘파이 배열을 받습니다.
- 11절은 테스트 대상이 아닙니다.

### 11절이 이어받을 연결과 확인할 것

- 10 b8·노트북 정리 끝: 「11절에서는 대화에서 빠진 대상을 채운 질문으로 다시 검색합니다.」 11절 `_src` b2·b4·b5와 노트북 셀 4·6·8을 열어 확인하고 쓴 문장입니다.
- **07~10절 코드를 그대로 이어 쓸 수 있습니다**: 후보 만들기(`rank_by_distance`·`rank_by_bm25`·`unique_chunk_ids`·`fuse_scores`·`fuse_rank`)·`parent_ids_of`·`recall_at`·`chunk_precision_at`·`eligible_items`·`vector_by_chunk`·`vector_by_query`. 질문 하나를 바꿔 다시 검색하는 절이라 **`embed_query()`를 한 번 더 부르는 자리**가 생깁니다(임베딩 요청 수를 준비물에 다시 세세요).
- **개선 전 11 노트북이 하는 일**(셀 11개, 코드 5개): 문자 단위 TF-IDF로 원문 질문 「그곳의 정기 휴관일은 언제예요?」와 재작성문을 각각 검색해 부모 ID 다섯 개를 견주고, 두 순위를 RRF로 합치고, 이미 기관명이 있는 `Q001`은 재작성 없이 검색합니다. 재작성 모델은 `init_chat_model("openai:gpt-4.1-mini", temperature=0)`이고 호출 1번입니다.
- **개선 전 11 노트북 출력**: `재작성 결과: 미르시립도서관 정기 휴관일은 언제인가요?` · `원문 : ['E01', 'E02', 'M02', 'E02', 'E02']` · `재작성문 : ['E01', 'E01', 'E02', 'E01', 'E01']` · `RRF 결합 : ['E01', 'E02', 'E02', 'M02', 'E01']` · `Q001` 검색 `['E01', 'E01', 'E02', 'E01', 'E01']`. **TF-IDF로 잰 값이라 07~10절 1차 검색으로 바꾸면 값이 달라집니다.**
- **개선 전 11 노트북이 쓰는 것 가운데 01~10절에서 안 가르친 것**: `numpy`(`np.argsort`), `sklearn`(`TfidfVectorizer`·`cosine_similarity` 행렬 판), 제너레이터 식 `next(...)` 두 곳, 기본값 매개변수 `k=5`·`k=10`, `enumerate(ranking, 1)`, `sorted(..., key=..., reverse=True)`, f-string, `Path`·`read_text`, `__import__("os")`, `assert "미르시립도서관" in standalone`(모델 문장 속 낱말을 `assert`로 확인 — 규격 §3 금지), 부모 ID를 **중복 그대로** 다섯 개 출력하기(01~10절은 `parent_ids_of()`로 중복을 뺍니다).
- **모델 이름**: 개선 전 11절만 `gpt-4.1-mini`를 씁니다(본문 b4에 「Ch 6·Ch 9 답변 생성용 `gpt-5.4-mini`와 과제가 다르다」는 문단이 있음). 이 챕터 다른 절은 모델을 부르지 않고 12절이 `gpt-5.4-mini`를 씁니다(`runs/advanced-continuity-integrated-result.json`의 `settings.chat`이 `gpt-5.4-mini`이고 테스트가 그 값을 봅니다). **어느 모델로 갈지 정해 진단에 적고, 12절 계약 파일의 값과 어긋나지 않게 두세요.**
- **11절이 견줄 값**: 재작성은 「검색이 좋아졌다」를 보이기 어렵습니다(개선 전에도 세 결과 모두 `E01`이 앞자리). 부모 6건 안에서 재현율을 재면 또 천장이니 **문서 청크 정밀도 자리 5·고유 부모 수·정답 부모의 첫 자리**처럼 천장이 없는 값을 함께 내고, 값이 같으면 「가를 수 없다」로 적으세요(07~10절과 같은 태도).
- **본문에서 확인할 곳**: 11 b3도 「앞 절의 변수나 실행 상태는 필요하지 않습니다」로 끝나 07~10절을 가리키지 않습니다. b4에 옛 `{{svg:11-질문-재작성}}` 토큰이 있으니 Mermaid 3~5장으로 바꾸고 옛 파일은 `qa/upgrade/before/figures/`에 복사하세요.
- **절 meta 시수**: 10절은 강의 1h·실습 1h 그대로 두었습니다. 09절에서 절 합(강의 12h·실습 28h)이 `chapter.json`과 맞았으니 **11·12절도 바꾸지 마세요**(바꿔야 하면 다른 절을 내리고 근거를 진단에 적을 것).
- **아직 안 가르친 것(11이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01~09절 목록에 더해, 10절에서도 하지 않은 것 — 걸린 시간 재기, nDCG, 조각 수 재기(09절에서만), 답을 쓰는 모델 호출(11·12절), 대화 기록을 프롬프트에 넣기, 모델 출력 글을 다시 검색에 넣기, 질문을 여러 벌로 늘리기, 시험 15문항 보기(12절).

## §11 → §12

(11절 품질 개선 2026-09-18. 결과는 `11-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 28 = G1 6·G2 4·G3 5·G4 0·G5 7·G6 3·G7 3), 코드 셀 **31**(준비 6 + 앞 절 함수 9), 검사 문장 316, **답을 쓰는 모델 10번**(재작성 5 + 값 바꿔 보기 5, 이 챕터에서 처음)·**임베딩 21번**(문서 청크 1 + 질문 20, 합쳐 0.01달러 아래), 리랭커 0번. 새 커널 두 번 실행에 `code_sha256`이 같고 셀별 출력 글자는 마지막 표 한 줄만 달랐습니다. 교재 출력은 마지막 실행 2026-09-18T22:10:49Z(`code_sha256` `78621cd7…`·`outputs_sha256` `d4c743ad…`). 노트북 전체 15초. `verify.py --chapter` `PASS 12 sections / 386 code cells (max 25 lines)`. Mermaid 4장·삽화 1장(1차 job `66e61172-8120-41c9-9604-43d85bd16eba` 채택, 재생성 없음, 2크레딧))

### 작업 환경 — 12절이 먼저 읽을 것

- **11절도 가볍습니다.** 노트북 실행 15초, `run_section.sh … 11 --no-exec` 15초입니다. 12절은 시험 15문항까지 보므로 요청 수가 늘어납니다.
- **`visual.cjs`에 `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`를 꼭 주세요**(09절 인계와 같음). 명령은 `ONLY=12- node /tmp/ch12-11/vis12.cjs textbook/part3/ch12-retrieval-tuning`입니다(`/tmp/ch12-11/vis12.cjs`는 10절 사본).
- **실습 폴더 가상환경에 `pytest`가 없습니다.** 테스트는 `uv run --project labs/part3/ch12-retrieval-tuning --with pytest==9.1.0 python -m pytest labs/part3/ch12-retrieval-tuning/tests/test_continuity.py -q`로 돌리세요. `pyproject.toml`·`uv.lock`은 고치지 마세요.
- `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/pw`·`/tmp/libs`·`/tmp/uv-cache`는 그대로입니다. 루트 디스크 여유 2.2G. 리랭커 모델 두 개(`.cache/vm/hf` 6.0GB)는 11절도 건드리지 않았습니다. **12절은 계약 파일의 `settings.reranker`가 `BAAI/bge-reranker-v2-m3`이라 그 모델을 다시 쓸 수 있습니다**(이미 받아 둔 판 `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`).
- 탐색 스크립트는 `/tmp/ch12-11/probe1.py`~`probe3.py`, 실행 사본은 `/tmp/ch12-11/runA.ipynb`·`runB.ipynb`, 출력 글자 해시 도구는 `/tmp/ch12-11/celltext.py`입니다.

### 11절이 새로 가르친 것

- **질문 재작성**: `rewrite_question(history_text, question)`(6줄). 프롬프트 네 줄을 글 `+`로 이어 만들고 `model.invoke(prompt)` 뒤 `answer.text.strip()`을 냅니다.
- **모델 준비**: 규격 §3 그대로 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`이고 `nbkit.key_and_model_cells("openai:gpt-5.4-mini", note)`로 넣었습니다. 설정 `reasoning_effort="none"`의 뜻을 한 문장으로 풀었습니다.
- **질문 하나를 후보로 바꾸는 겉면 두 개**: `ranking_lists(question)`(4줄, `embed_query` → 두 순위 목록)·`candidates_of(ranking_list, weight_list)`(2줄, `fuse_rank` 뒤 앞자리 자르기). 07~10절은 개발 질문 열다섯 개를 한 번에 벡터로 바꿨지만 이 절은 질문마다 따로 부릅니다.
- **`measure(found_chunk_ids, gold_doc_ids)`**(5줄): 보고 자리 5에서 (고유 부모 수, 문서 청크 정밀도, 부모 문서 재현율) 세 값. 소수 둘째 자리로 반올림합니다.
- **`branch_row(name)`**(10줄): 갈래 하나로 대화 다섯 개를 재어 세 값의 질문 평균.
- **순위 목록 네 개 합치기**: `fuse_rank(short_lists + rewritten_lists, four_weights)`. `four_weights = [1.0, 1.0, 1.0, 1.0]`을 값 셀에서 먼저 만듭니다.
- **쓰지 않은 것**: `numpy` import·`sklearn`·`tiktoken`·리랭커·`lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`목록.index`·`Path`·f-string·타입힌트·`@`·`BaseModel`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`sorted`·`type`이 아니라 `len`·`print`·`open`·`range`·`round`·`sorted`뿐입니다.

### 이어 쓸 이름과 값 (11절)

- 값: `similarity_top`(1) · `keep_tags`(아홉 개) · `rank_constant`(60) · `equal_weights`(`[1.0, 1.0]`) · **`four_weights`(`[1.0, 1.0, 1.0, 1.0]`)** · `candidate_count`(8) · `recall_place`(3) · `report_place`(5, 이 절은 바꾸지 않음).
- 자료(07~10절과 같은 이름): `candidates` · `root_path` · `data_path` · `documents` · `queries`(30) · `parents`(6) · `chunks`(175) · `dev_all` · `dev_queries`(15) · `chunk_texts` · `chunk_ids` · `parent_by_chunk` · `all_chunk_count`(175) · `embedding_model_name` · `vector_dimensions`(256) · `chunk_vectors` · `kiwi` · `kiwi_corpus` · `bm25_model`.
- 11절이 새로 만든 이름: **`model`**(답을 쓰는 모델) · **`conversation_rows`**(다섯 줄, 한 줄은 `(질문 ID, 대화 기록, 대상 빠진 후속 질문)`) · **`question_by_id`**·**`gold_by_id`** · **`rewritten_by_id`**·**`empty_rewritten_by_id`** · **`empty_history`**(`"없음"`) · **`branch_names`**(네 개 → 다섯 개) · **`found_by_branch`**(갈래 이름 → 질문 ID → 후보 목록) · `example_id`(`Q001`)·`example_gold`·`example_found`·`example_row` · `full_lists`·`short_lists`·`rewritten_lists`·`empty_lists` · `average_row`.
- 11절이 새로 만든 함수 다섯 개: **`rewrite_question`**(6) · **`ranking_lists`**(4) · **`candidates_of`**(2) · **`measure`**(5) · **`branch_row`**(10). 그 밖에 01~10절 함수 열네 개를 같은 코드로 다시 정의했습니다.
- **준비 셀 묶음**(09·10절 방식 그대로): 앞 절 함수 **열네 개를 준비 셀 아홉 개**에 담았습니다(`code(SRC, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"])`, 생성기 `prep()` 도우미). `eligible_items`도 그 묶음에 넣었습니다.
- **10절 이름 가운데 쓰지 않은 것**: `vector_by_chunk`·`vector_by_query`·`relevance_weights`·MMR 함수 다섯 개·`query_vectors`. 11절은 질문마다 `embed_query`를 그때그때 부릅니다.

### 출력 라벨 (11절 전부)

「langchain:」「langchain-openai:」「python-dotenv:」「kiwipiepy:」「rank-bm25:」「불러온 이름:」「OPENAI_API_KEY 설정 여부:」「모델 이름:」「temperature:」「고른 경로:」「부모 문서 수:」「문서 청크 수:」「질문 수:」「코사인 유사도의 가장 큰 값:」「남길 품사 표시 수:」「순위 상수:」「같은 가중치:」「네 순위 목록에 줄 가중치:」「후보 수:」「부모 문서 재현율을 재는 자리:」「보고 자리:」「이어 붙인 글 수:」「첫 문서 청크 ID:」「임베딩 모델 이름:」「벡터의 숫자 개수 설정:」「문서 청크 벡터 수:」「개발 질문 수:」「시험 질문 수:」「첫 개발 질문:」「그 질문의 정답 부모 문서 ID:」「검색 낱말 목록 수:」「BM25 모델이 본 문서 청크 수:」「문서 청크 하나의 평균 검색 낱말 수:」「대화 수:」「첫 대화 기록:」「질문 ID | 정답 부모 | 대상 있는 질문 | 대상 빠진 질문」(라벨 줄 따로)「만든 재작성문 수:」「질문 ID | 재작성문」(라벨 줄 따로)「견줄 갈래:」「갈래 하나의 후보 목록 수:」「후보 목록 하나의 문서 청크 수:」「고른 대화의 질문 ID:」「갈래 | 보고 자리 다섯 개의 부모 문서 차례 | 고유 부모 수 | 문서 청크 정밀도 자리 5」(라벨 줄 따로)「갈래 | 고유 부모 수 평균 | 문서 청크 정밀도 자리 5 | 부모 문서 재현율 자리 3」(라벨 줄 따로, 두 번 나옴)「질문 ID | 대화 기록 없이 만든 재작성문」(라벨 줄 따로)「견줄 갈래 수:」

### 실행값 (2026-09-18 마지막 새 커널)

- `부모 문서 수: 6` · `문서 청크 수: 175` · `개발 질문 수: 15` · `문서 청크 하나의 평균 검색 낱말 수: 44.01`(07~10절과 같음) · `대화 수: 5`.
- 대화 다섯 개: `Q001`(E01, 미르시립도서관) · `Q005`(E01, 미르시립도서관 열람실) · `Q041`(M01, 도우미봇 R2) · `Q085`(H01, 누리테크) · `Q087`(H01, NT-LD-16).
- 재작성문: `Q001`·`Q005`·`Q041`은 대상이 채워졌고 `Q085`·`Q087`은 채워지지 않았습니다.
- 실행 1(`Q001`, 정답 부모 `['E01']`): `대상 있는 질문 | ['E01'] | 1 | 1.0` · `대상 빠진 질문 | ['E01', 'E02'] | 2 | 0.8` · `재작성문 | ['E01'] | 1 | 1.0` · `합친 순위 | ['E01'] | 1 | 1.0`.
- **다섯 대화 평균(보고 자리 5)**: `대상 있는 질문 | 1.4 | 0.88 | 1.0` · `대상 빠진 질문 | 2.2 | 0.72 | 1.0` · `재작성문 | 1.4 | 0.88 | 1.0` · `합친 순위 | 1.6 | 0.88 | 1.0` · `기록 없이 재작성문 | 2.2 | 0.76 | 1.0`.

### 흔들리는 값 — 12절도 셈에 넣을 것

- 두 실행에서 다른 곳은 **마지막 표 한 줄**뿐입니다. `기록 없이 재작성문`의 문서 청크 정밀도가 `0.72` ↔ `0.76`으로 갈렸습니다. **재작성문 다섯 문장은 두 실행에서 글자까지 같았으므로** 까닭은 09절이 적은 임베딩 미세 차이입니다.
- 다만 앞선 탐색 실행에서는 `Q041`·`Q085`의 재작성 문장이 조금 달라진 적이 있습니다. **모델 문장은 temperature 0에서도 같다고 보장할 수 없습니다.**
- 그래서 **그림 라벨과 정리 세 줄에는 세 번 실행에서 모두 같았던 값만** 넣었습니다. 12절도 시험 15문항 값을 그림에 넣으려면 두 번 이상 실행해 같은지 보고, 인용은 소수 둘째 자리까지만 하세요.

### 천장을 다룬 방식과 결론 한정 — 12절도 같은 규칙으로

- **부모 문서 재현율 자리 3이 다섯 갈래 모두 `1.0`**이고 **정답 부모의 첫 자리도 탐색 스무 줄이 모두 `1`**이었습니다. 값 그대로 싣고 「이 조건에서는 가를 수 없다」를 b6·b7·복습 3번에 적었습니다.
- **가른 값은 고유 부모 수 평균(흩어진 정도)과 문서 청크 정밀도 자리 5(관련성)** 두 가지입니다. 10절과 같은 이름·같은 함수인데 **읽는 방향이 반대**입니다(10절은 고유 부모 수가 크면 다양성, 11절은 후보가 흩어짐). 그 차이를 b4와 노트북 5절에 한 문장으로 적었습니다.
- **재작성이 늘 좋아진다고 쓰지 않았습니다.** `Q087`은 대상이 채워지지 않았고 `Q005`는 대상을 빼도 정밀도가 올랐습니다.
- **답 품질을 재지 않았습니다.** 답을 쓰는 모델을 검색 앞 단계에만 썼습니다.
- 걸린 시간·토큰 사용량·여러 차례 오간 대화·대상이 둘 이상인 대화는 실행하지 않았습니다. Ch 11 개발 15문항 값과 01~06절 core 벌 값은 이 절에서도 나란히 놓지 않았습니다.

### 용어 (11절이 더한 세 개)

- **질문 재작성(query rewriting)** · **독립 질문(standalone question)** · **대화 기록(conversation history)**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 4 → **3**」입니다.
- **「대상 있는 질문」·「대상 빠진 질문」·「재작성문」·「합친 순위」·「기록 없이 재작성문」**은 표와 그림의 갈래 이름입니다. 12절이 설정 이름을 붙일 때 같은 말을 쓰면 두 절 표를 나란히 읽을 수 있습니다.
- 01~10절 말 마흔여덟 개와 Ch 9~11 말을 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**이고 11절은 길이를 재지 않아 쓰지 않았습니다. 한정어 없는 「청크」도 쓰지 않았습니다.
- 쓰지 않은 말: 「원문 질문」(→ 대상 있는 질문), 「맥락」(→ 대화 기록), 「쿼리」, 「프롬프트 엔지니어링」, 「임계값」, 「포화」(→ 천장에 닿음), 「TF-IDF」, 「RRF」(→ 순위 합치기·합친 순위), **「토큰」**(04·10절과 같음 — b7의 「토큰 사용량」을 「보낸 글의 길이」로 고쳤습니다).

### 파일 쓰기 규칙 — 11절도 파일을 쓰지 않습니다

- `runs/`는 파일 **36개**·`core-history/` 12개 그대로이고 이어 붙인 해시 `d3d6478c0790e11e045c518edd1356e20c29ce0d33156722221fc5947e4a107a`로 05·06·07·09·10절 기록과 같습니다.
- `advanced-documents.json`·`advanced-queries.json`·`core-documents.json`·`core-queries.json`은 한 글자도 고치지 않았습니다.
- `pyproject.toml` `5b10531e0675a231…`·`uv.lock` `f13e8c6f1880e7de…` 그대로입니다. **`%pip` 목록은 다섯 개**(`langchain==1.4.0`·`langchain-openai==1.6.1`·`python-dotenv==1.2.3`·`kiwipiepy==0.23.2`·`rank-bm25==0.2.2`)로 10절 네 개에 `langchain`을 더했고, 다섯 개 모두 `pyproject.toml`에 이미 고정돼 있어 **잠금을 고치지 않았습니다**. dev `pip==26.2`도 그대로입니다.
- 공용 화면 검사 결과 `visual-results.json`은 **26행 유지**이고 바이트가 `49352bfcd3f7e511…`로 그대로입니다.
- `textbook/part3/qa/check_delivery.py`는 끝까지 통과(종료 코드 0), `textbook/part3/qa/check_continuity.py`는 01~10절과 같은 154행 `part2-practice.zip`에서 멈춥니다.

### 실습 폴더 테스트 — 12절은 대상입니다 (꼭 읽을 것)

- `labs/part3/ch12-retrieval-tuning/tests/test_continuity.py`는 11절 작업 전후 모두 **4 passed**입니다. 11절은 테스트 대상이 아니라 파일을 고치지 않았습니다.
- **161~188행이 12절 노트북에서 이름 네 개를 `ast`로 찾아 실제로 부릅니다.** 계약은 다음과 같습니다.
  1. `eligible_items(subset)` — `[item["qid"] for item in eligible_12(mixed)] == ["Q-MULTI"]`. 08~11절 판과 같은 동작입니다.
  2. `metrics(doc_ids, gold_doc_ids, all_ids)` — 값 네 개를 돌려주고 앞 둘이 `(0.5, 0.5)`. **08~11절 `recall_at`과 다른 함수이니 이름을 지우지 마세요.**
  3. `mmr(...)` — `load_notebook_function`으로 따로 컴파일되고 `evaluate_config`에 이름으로 넘어갑니다. **10절 `mmr`과 다른 함수**이고 지금은 넘파이 배열을 받습니다.
  4. `evaluate_config(config, items)` — `{"eligible_items", "TfidfVectorizer", "chunks", "mmr", "metrics"}`를 이름 공간으로 받고 `config`는 `{"analyzer", "ngram", "report_k", "lambda"}`. 문항이 없으면 `ValueError("평가 가능한 문항 …")`.
- 12절을 사다리에 맞춰 `TfidfVectorizer` 없이 다시 쓰면 이 네 호출이 깨집니다. **08·10절이 한 것처럼 테스트가 요구하는 이름·인자·반환만 지키고 몸통을 다시 쓰거나**, `load_notebook_namespace()`로 바꾸고 테스트의 넣는 값을 고치세요(고치면 `10-diagnosis.md` §8 모양으로 진단에 적기).

### 12절이 이어받을 연결과 확인할 것

- 11 b8·노트북 정리 끝: 「12절에서는 이 챕터에서 고른 설정을 모아 시험 질문에 한 번 실행하고 기록을 남깁니다.」 12절 `_src` b1·b2와 노트북을 열어 확인하고 쓴 문장입니다.
- **07~11절 코드를 그대로 이어 쓸 수 있습니다**: 후보 만들기(`rank_by_distance`·`rank_by_bm25`·`unique_chunk_ids`·`fuse_scores`·`fuse_rank`)·`parent_ids_of`·`recall_at`·`chunk_precision_at`·`eligible_items`·`ranking_lists`·`candidates_of`·`measure`. 답을 쓰는 모델은 11절과 같은 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`입니다.
- **모델 이름 계약**: `runs/advanced-continuity-integrated-result.json`의 `settings`는 `{"input": "PDF page text", "dense": "text-embedding-3-small", "sparse": "Kiwi+BM25", "fusion": "RRF(k=60)", "reranker": "BAAI/bge-reranker-v2-m3", "context_selection": "matched-page-text", "chat": "gpt-5.4-mini", "dimensions": 256}`입니다. 11절이 `gpt-5.4-mini`로 맞췄으므로 **이 챕터에서 답을 쓰는 모델 이름은 한 가지뿐**입니다.
- **개선 전 12 노트북이 하는 일**: 문자 단위 TF-IDF + MMR 설정 36벌을 개발 15문항에서 견주고, 고른 설정 한 벌을 시험 15문항에 한 번 실행해 `runs/advanced-*`에 기록합니다. `check_continuity.py` 85행이 `len(experiments) == 36`을 봅니다.
- **12절이 견줄 값**: 부모 6건 안에서 재현율을 재면 또 천장입니다(07~11절 모두 `1.0`). **문서 청크 정밀도 자리 5·고유 부모 수·넘길 글의 조각 수**처럼 천장이 없는 값을 함께 내세요. 시험 15문항을 처음 여는 절이므로 Ch 11 「개발로 고르고 시험은 한 번」 약속을 b3에 인용하세요.
- **본문에서 확인할 곳**: 12 b3도 「앞 절의 변수나 실행 상태는 필요하지 않습니다」로 끝나 07~11절을 가리키지 않습니다. b1~b10을 07~11절과 이어 쓰고, 옛 토큰이 있으면 Mermaid 3~5장으로 바꾸고 옛 파일은 `qa/upgrade/before/figures/`에 복사하세요. meta의 「코드 Jupyter Notebook」도 07~11절처럼 노트북 경로로 고치세요.
- **절 meta 시수**: 11절은 강의 1h·실습 1h 그대로입니다. 09절에서 절 합(강의 12h·실습 28h)이 `chapter.json`과 맞았으니 **12절도 바꾸지 마세요**.
- **챕터 마감 몫**: 12절이 끝나면 실습 절(13절)·챕터 요약·`_build_index.py` 절 수·`check_course_continuity.py` 허용 목록·`part2-practice.zip` 신선도·`labs/part3/ch12-retrieval-tuning/.venv`(08절이 남긴 빈 폴더) 정리가 남습니다. `qa/verification.md` 표의 09절 줄은 11절 작업에서 채웠습니다.
- **아직 안 가르친 것(12가 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01~10절 목록에 더해, 11절에서도 하지 않은 것 — 걸린 시간 재기, 토큰 사용량 확인, nDCG, 찾은 글로 답 쓰기, 답 문장 판정, 여러 차례 오간 대화, 대상이 둘 이상인 대화, 질문을 여러 벌로 늘리기, 파일에 기록 남기기(12절), 시험 15문항 보기(12절).

## §12 → 실습

(12절 품질 개선 2026-09-18. 결과는 `12-diagnosis.md`, 게이트 G1~G7 **0**(수정 전 94 = G1 43·G2 11·G3 12·G4 0·G5 12·G6 13·G7 3), 코드 셀 **54**(준비 6 + 앞 절 함수 16 + 나머지 32), 검사 문장 424, **임베딩 31번**(문서 청크 1 + 개발 15 + 시험 15)·**답을 쓰는 모델 1번**·리랭커 0번, 합쳐 미화 0.01달러 아래. 새 커널 **네 번** 실행에 `code_sha256` `9fc0c448…`이 같고 다른 셀은 7절 두 표의 문서 청크 정밀도 칸뿐. 교재 출력은 마지막 실행 2026-09-18T23:20:56Z(`outputs_sha256` `ef7db1a0…`). 노트북 전체 10.5초. `verify.py --chapter` `PASS 12 sections / 428 code cells (max 20 lines)`. Mermaid 4장·삽화 1장(1차 job `88933c13-2cf4-4361-94e5-872e2e40e354` 채택, 재생성 없음, 2크레딧))

### 이 챕터가 열두 절에서 가르친 것

| 절 | 새로 가르친 것 | 실습에서 바로 쓸 수 있는 이름 |
|---|---|---|
| 01 | 벡터 거리와 정확 검색, 코사인 거리 | `dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`·`l2_distance`·`rank_by_distance` |
| 02 | pgvector `vector(256)`·HNSW·`EXPLAIN`·`set_config()` | `run_search`·`print_hits`·`find_scan_line`·`set_seqscan`(Docker 필요) |
| 03 | 메타데이터 필터·나중 걸러 내기·반복 탐색 | `make_filler_vectors`·`rank_in_category`·`set_iterative_scan`(Docker 필요) |
| 04 | Kiwi 형태소·품사 표시 아홉 개·BM25 | `kiwi_terms`·`rank_by_bm25`·`print_scores`·`keep_tags` |
| 05 | 벡터 거리와 낱말 겹침 견주기·점수 방향 | `print_ranked`·`score_one` |
| 06 | 순위 합치기(RRF)·순위 상수 60·가중치 | **`fuse_scores`·`fuse_rank`**·`rank_constant`·`equal_weights` |
| 07 | 1차 검색과 리랭킹·교차 인코더·부모 문서 | `unique_chunk_ids`·**`parent_ids_of`**·`make_pairs`·`rerank` |
| 08 | 후보 수·보고 자리 5·문서 청크 정밀도·천장 다루기 | **`eligible_items`**·`score_candidates`·`order_by_score`·**`chunk_precision_at`**·`evaluate` |
| 09 | 부모 문서 넘기기·넘길 부모 수·입력 가용분 | `parent_texts_of`·`count_tokens`·`total_tokens`·`summarize` |
| 10 | MMR·관련성 비중·고유 부모 수 | **`similarity_to_chosen`·`mmr_score`·`best_candidate`·`mmr`·`mmr_pick`** |
| 11 | 질문 재작성·독립 질문·대화 기록 | **`rewrite_question`**·`ranking_lists`·`candidates_of`·`measure`·`branch_row` |
| 12 | 손잡이·설정 한 벌·입력 지문·실험 기록 한 줄 | **`file_fingerprint`·`write_text`·`question_lists`·`candidates_of`·`metrics`·`top_results_of`·`metric_summary`·`result_row`·`slice_summary`·`evaluate_item`·`evaluate_config`·`knob_mean`·`print_knob_rows`·`log_row`** |

### 실습 절이 이어 쓸 함수·데이터·설정

- **자료(07~12절과 같은 이름)**: `candidates = [".", "../../..", "../../../.."]` + `for`/`break` · `root_path` · `data_path` · `documents` · `parents`(6) · `chunks`(175) · `queries`(30) · `dev_all` · `dev_queries`(15) · `chunk_texts` · `chunk_ids` · `all_chunk_count`(175) · `parent_by_chunk` · **`page_by_chunk`·`text_by_chunk`**(12절이 더함) · `chunk_vectors` · `vector_by_chunk` · `kiwi` · `kiwi_corpus` · `bm25_model` · `model`.
- **값**: `similarity_top`(1) · `keep_tags`(아홉 개) · `rank_constant`(60) · `candidate_count`(8) · `recall_place`(3) · `report_place`(5) · `equal_weights`(`[1.0, 1.0]`). 12절이 고른 설정은 **가중치 `[0.0, 1.0]`·관련성 비중 `1.0`**입니다.
- **후보 만들기 한 줄**: `fuse_rank(ranking_lists, weight_list)`의 앞 `candidate_count`개. 07~12절이 모두 같은 방법을 씁니다. 순위 목록 두 개는 `rank_by_distance(question_vector, all_chunk_count)`와 `rank_by_bm25(question, all_chunk_count)`를 `unique_chunk_ids()`로 문서 청크 ID 목록으로 바꾼 것입니다.
- **고르기**: `mmr_pick(question_vector, found_chunk_ids, report_place, relevance_weight)`(10·12절).
- **재기**: `recall_at`(Ch 11 02) · `chunk_precision_at`(08) · `parent_ids_of`(07). 보고 단위는 **재현율 자리 3 · 문서 청크 정밀도 자리 5**입니다.
- **답 쓰기**: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` + `model.invoke(prompt)` + `answer.text.strip()`(11·12절). 출처 표시는 Ch 8 모양 `[문서ID p.쪽]`이고 12절이 `text_by_chunk`와 `page_by_chunk`로 넣을 글을 만듭니다.
- **쓰지 않는 것**: `numpy`·`sklearn`·`lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·f-string·타입힌트·세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`set`·`next`·`목록.index`·`+=`. 12절이 새로 쓴 것은 `hashlib`·`time`·`os.makedirs`·`raise ValueError`·`딕셔너리.copy()`·`str.zfill()`뿐이고 모두 그 자리에서 뜻을 풀었습니다.

### 요청 수·비용·메모리 제약

- 12절 한 절이 임베딩 31번·답 모델 1번입니다. **실습 절은 규격 §7-2대로 모델 호출 3~5번**이므로 답을 쓰는 모델을 3~5번 부르고 임베딩은 문서 청크 1번 + 질문 몇 번으로 맞추세요.
- 문서 청크 175개 임베딩 한 번이 약 2초입니다. 개발 질문 열다섯 개를 모두 부르면 다시 약 3초입니다. 30분 실습에는 **질문 두세 개**면 넉넉합니다.
- **리랭커를 쓰려면 메모리 3.8GB 안에서 하나씩 올렸다 내립니다**(07·08절, `reranker = None` 뒤 다음 모델, 최대 RSS 2.76GB). 판 번호 `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`를 고정하고 `max_length=256`·`device="cpu"`로 씁니다. 모델은 `.cache/vm/hf`에 이미 받아 두었습니다(6.0GB).
- **01~03절 pgvector는 Docker가 필요합니다.** 실습 절에 넣으면 준비물이 커집니다. 04~12절 재료만으로 구성하기를 권합니다.

### 실습 절이 건드리면 안 되는 파일과 기록 계약

- **`labs/part3/ch12-retrieval-tuning/runs/advanced-continuity-*` 세 파일을 다시 쓰지 마세요.** 12절이 쓴 마지막 실행이 교재 출력입니다. 실습 절이 같은 이름으로 쓰면 36줄 계약·`selected_run_id`·사본 대조가 모두 깨집니다. 05~11절처럼 **실습 절은 파일을 쓰지 않는 쪽**을 권합니다(Ch 5 C-3 선례). 꼭 써야 하면 다른 이름(`runs/practice-*.json`)으로 쓰고 `public-files.json`에 넣을지 함께 정하세요.
- 읽는 쪽 다섯 곳: 실습 폴더 `tests/test_continuity.py` 61~129행 · `textbook/part3/qa/check_continuity.py` 81~137행 · `textbook/qa/check_course_continuity.py` 115~180행 · `textbook/part4/ch13-langgraph-basics/qa/author_ch13.py` · `textbook/part4/ch15-evaluation-advanced/_author.py`.
- 지금 값: 기록 36줄 `9b447a41…` · 시험 기록 `f9b16717…` · 통합 기록 `ce76d3d8…` · 사본 `runs/continuity/20260918T232052/`. `runs` 파일 48개(12절 실행 네 번으로 사본 폴더가 네 개 늘었고 삭제 권한이 없어 그대로 둠), `core-history/` 12개.
- `data/advanced-documents.json` `832d89c2…` · `data/advanced-queries.json` `dcf7f288…` · `pyproject.toml` `5b10531e…` · `uv.lock` `f13e8c6f…`는 한 글자도 고치지 않았습니다. Ch 9·10·11 기록과 Ch 6~8 사슬도 읽기만 했습니다.
- 공용 화면 검사 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`은 **26행**입니다. 실습 절을 붙이면 28행이 됩니다.

### 테스트와 검사 상태

- 실습 폴더 테스트 `4 passed`입니다. 명령은 `UV_CACHE_DIR=/tmp/uv-cache UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch12-retrieval-tuning UV_NO_SYNC=1 uv run --project labs/part3/ch12-retrieval-tuning --with pytest==9.1.0 python -m pytest labs/part3/ch12-retrieval-tuning/tests/test_continuity.py -q`입니다. **세 환경 변수를 빼면** uv가 루트 디스크에 torch·CUDA를 새로 받다가 `No space left on device`로 멈춥니다.
- `tests/test_continuity.py`의 12절 블록은 12절 작업에서 `load_notebook_namespace()` 방식으로 고쳤습니다(`12-diagnosis.md` §8). 08·10절 블록(노트북 이름 공간·문서 청크 ID 모양)은 그대로입니다. 실습 절이 이 파일에 걸리는 이름을 바꾸면 함께 고치세요.
- `textbook/part3/qa/check_delivery.py` 종료 코드 0. `textbook/part3/qa/check_continuity.py`는 **154행 `Stale archive: part2-practice.zip`**, `textbook/qa/check_course_continuity.py`는 **212행 `part1-practice.zip`**에서 멈춥니다(01~11절과 같은 자리, 그 앞의 ch12 계약 검사는 모두 통과).

### 실습 절(13절)을 붙일 때 함께 고칠 것

1. **12절 b8 「다음 학습과 이어지는 지점」과 노트북 정리 마지막 줄**을 실습 절로 고칩니다. 지금은 Ch 13·Ch 15를 가리키고 있고 노트북 정리 끝 문장은 「다음 실습 절에서는 이 챕터에서 만든 함수들을 한 상황에 모아 함께 실행합니다.」입니다.
2. `chapter.json`에 `{"slug": "13-검색-품질-실습", "title": "…", "format": "experiment"}`를 더합니다. **절 시수 30분은 챕터 시수(총 40h · 강의 12h · 실습 28h)에 더하지 않습니다**(09절에서 맞춘 절 합 유지).
3. **`chapter.json`의 `objectives` 다섯째와 `textbook/part3/_build_index.py` 88행이 낡았습니다.** 둘 다 「TF-IDF와 MMR을 조합한 36건」이라고 적혀 있는데 12절 서른여섯 벌은 이제 **가중치 여섯 가지 × 관련성 비중 여섯 가지**입니다. 챕터 목차 페이지 대조 규칙(규격 §7-2)대로 챕터 마감 때 고치세요.
4. `textbook/part3/_build_index.py` 27행의 절 수 `12` → `13`, 81행 「Ch 9–12 · 32절」 → 33절을 고치고 실제로 돌려 보세요(규격 §7-2, Ch 9 검토 B C-2).
5. `textbook/qa/check_course_continuity.py`의 해시 허용 목록과 `textbook/part3/public-files.json`을 확인하고, 학생 묶음을 풀어 실습 절 첫 셀이 도는지 봅니다. `%pip` 목록을 바꾸면 `pyproject.toml` dev의 `pip==26.2`와 `uv.lock`도 함께 확인합니다(규격 §7-2, Ch 11 검토 C-1).
6. `labs/part3/ch12-retrieval-tuning/.venv`(08절이 남긴 빈 폴더) 정리도 챕터 마감 몫으로 남아 있습니다.
7. **Ch 13 07절 b3의 「검색된 E01·E02 쪽」 문장이 낡았습니다.** 12절 통합 기록의 `retrieved`가 이제 `E01` 문서 청크 세 건이고 `settings.reranker`는 `null`, `settings.context_selection`은 `matched-chunk-text`입니다. Ch 13 개선 때 함께 고쳐야 합니다(코드는 멈추지 않습니다).

### 결론 한정과 태도 — 실습 절도 같은 규칙으로

- **천장에 닿은 지표로 설정을 가르지 않습니다.** 부모 문서 재현율 자리 3은 07~12절에서 늘 `1.0`이었고 12절에서는 부모 문서 정밀도도 서른여섯 줄 모두 `0.2`였습니다. 값 그대로 싣고 「이 조건에서는 가를 수 없다」로 적습니다.
- **어느 설정·리랭커·갈래가 낫다고 일반화하지 않습니다.** 12절 결론은 「이 말뭉치·이 질문 묶음·한 번의 실행」으로 한정했습니다.
- **모델 답에 `assert`를 걸지 않습니다.** 개수·자료형·키 유무만 확인합니다.
- **흔들리는 값은 그림 라벨·정리·복습에서 뺍니다.** 12절에서 흔들린 것은 문서 청크 정밀도 평균(소수 셋째 자리)입니다. 인용은 소수 둘째 자리까지 하되 노트북 출력에 있는 글자 그대로 백틱에 넣으세요(G5).
- **실행해 보지 않은 것은 「이번에 실행하지 않았습니다」로 적습니다.**

### 용어 (12절이 더한 네 개)

- **손잡이(knob)** · **설정 한 벌(configuration)** · **입력 지문(fingerprint)** · **실험 기록 한 줄(experiment log row)**. 본문 b4 용어 표에 있습니다. meta는 「새 용어 **4**」입니다.
- 01~11절 말 쉰한 개를 그대로 씁니다. **「조각」은 Ch 5 토큰 뜻 전용**이고 문서 덩어리는 늘 **「문서 청크」**입니다. 한정어 없는 「청크」는 쓰지 않습니다.
- 12절이 쓴 표·그림의 갈래 이름: 「개발 15문항」·「시험 15문항」·「고른 설정 한 벌」·「기록 한 줄」·「손잡이별 평균」. 실습 절이 같은 말을 쓰면 두 절 표를 나란히 읽을 수 있습니다.
- 쓰지 않은 말: 「하이퍼파라미터」(→ 손잡이), 「그리드 서치」(→ 손잡이를 곱해 만든 설정), 「오버피팅」(→ 고를 때 본 질문으로 재면 값이 실제보다 높게 나옴), 「베이스라인」, 「튜닝」(제목에만), 「포화」(→ 천장에 닿음), 「쿼리」, 「토큰」, 「RRF」(→ 순위 합치기).

### 아직 안 가르친 것 (실습 절이 설명 없이 전제하면 안 됨)

Ch 9 요약 §6 + Ch 10 요약 §7 + Ch 11 요약 §12 + 01~11절 목록에 더해, 12절에서도 하지 않은 것입니다.

- 걸린 시간 재기, 보낸 글의 길이와 요청 사용량 확인, 비용 계산.
- 두 지표가 어긋난 까닭 밝히기, 통계적으로 차이를 판정하기, 설정을 여러 번 재어 평균 내기.
- 리랭커를 넣은 설정 묶음, 후보 수를 손잡이로 두기, 순위 상수 바꾸기.
- 찾은 글로 쓴 답이 맞는지 판정하기(Ch 15), 근거성·출처 표기 평가(Ch 15).
- 여러 차례 오간 대화, 대상이 둘 이상인 대화, 질문 묶음을 새로 만들기.
- 검색을 서비스로 띄우기, 색인을 다시 만들기, 자료가 바뀔 때 기록을 잇기.

## 실습 → 챕터 검토

(13절 「검색 품질 실습: 가중치 하나를 바꿔 답까지 보기」 신설 2026-09-19. 결과는 `13-diagnosis.md`, 게이트 G1~G7 **0**(새 절이라 수정 전 없음), 코드 셀 **31**(준비 6 + 앞 절 함수 8 + 나머지 17), 검사 문장 341, **임베딩 3번**(문서 청크 1 + 질문 2)·**답을 쓰는 모델 2번**(실행마다 한 번)·리랭커 0번, 합쳐 미화 0.01달러 아래. 새 커널 **두 번** 실행에 `code_sha256` `7b61e25bf8ef8e9b`·`outputs_sha256` `504b38119a748386`와 셀별 출력 글자가 모두 같았고 **모델 답 문장 두 개까지 같았습니다**. 교재 출력은 마지막 실행 2026-09-19. `verify.py --chapter` `PASS 13 sections / 459 code cells (max 20 lines)`. 챕터 `gates-after.json` **13/13 PASS**. Mermaid 3장·삽화 1장(2차 job `4292baa0-747b-4279-87db-f2fa4fba2e46` 채택, 1차 `eb37a634-…` 탈락, 4크레딧, 생성 전 잔액 2711))

### 13절이 고른 것과 뺀 것

- **주제**: 05절 순위 둘 → 06절 가중치로 합치기 → 08절 보고 자리와 두 지표 → 12절 답 쓰기를 한 줄기로 잇고 **06절 가중치 한 자리만** 바꿉니다. 실행 1 `[1.0, 1.0]`(06절 기본), 실행 2 `[1.0, 0.0]`(뜻 검색만).
- **뺀 것**: 01~03절 pgvector(Docker 필요) · 07·08절 리랭커(메모리 3.8GB·30분 수업) · 10절 MMR(함수 다섯 개를 더 다시 정의하면 셀이 36개를 넘음). 그래서 보고 자리는 **합친 순위의 앞 다섯 자리**이고 12절이 고른 설정(MMR 관련성 비중 1.0)과 다릅니다.
- **새 API·새 문법 0개**. 01~12절 함수 열세 개를 같은 코드로 준비 셀 여덟 개에 묶고(09·12절 방식), 새로 만든 함수는 `print_rows`·`column_mean`·`context_of`·`score_row`·`run_weights` 다섯 개입니다.
- **질문 두 개**(개발 묶음 앞 두 문항 `Q001`·`Q002`)로 줄여 요청을 다섯 번 안에 두었습니다. 시험 15문항은 이 절도 열지 않습니다.

### 실행값 (2026-09-19 마지막 새 커널, 두 번 실행이 같음)

- `부모 문서 수: 6`·`문서 청크 수: 175`·`질문 수: 30`, `문서 청크 하나의 평균 검색 낱말 수: 44.01`(07~12절과 같음).
- `개발 질문 수: 15 | 이번에 쓸 질문 수: 2`·`고른 질문 ID: ['Q001', 'Q002']`·`거리 순위 1위 문서 청크: E01-P02-C04`(낱말 순위도 같음).
- 실행 1: `Q001 | ['E01'] | 1.0 | 1.0`·`Q002 | ['E01'] | 1.0 | 1.0`, 평균 두 칸 모두 `1.0`, `넣은 글의 길이: 432`.
- 실행 2: `Q001 | ['E01'] | 1.0 | 1.0`·`Q002 | ['E01', 'E02'] | 1.0 | 0.4`, 정밀도 평균 `0.7`, `넣은 글의 길이: 302`.
- 비교 표 두 줄: `실행 1 | [1.0, 1.0] | 1.0 | 1.0`·`실행 2 | [1.0, 0.0] | 1.0 | 0.7`.
- 답 두 개: 실행 1은 권수와 기간을 적었고 실행 2는 자료에서 찾지 못했다고 답했습니다. **두 답 모두 한 번만 본 결과로 적었고 그림 라벨에 넣지 않았습니다.**

### 건드리지 않은 것 (작업 전후 해시 같음)

`runs/advanced-continuity-experiment-log.jsonl` `9b447a41…` · `advanced-continuity-test-result.json` `f9b16717…` · `advanced-continuity-integrated-result.json` `ce76d3d8…` · `core-history/` 12개 · `data/advanced-documents.json` `832d89c2…` · `data/advanced-queries.json` `dcf7f288…` · `pyproject.toml` `5b10531e…` · `uv.lock` `f13e8c6f…`. 실습 폴더 테스트 **4 passed**(전후 같음, `tests/test_continuity.py`를 고치지 않음). Ch 9·10·11 기록과 Ch 6~8 사슬은 열지 않았습니다.

### 챕터 밖에서 고친 것 (검토자가 확인할 것)

1. `textbook/part3/_build_index.py` **27행** ch12 절 수 `12` → `13`. 돌려서 `Part 3: 36 verified sections; 89 bundled files` 확인.
2. `textbook/part3/qa/check_delivery.py` **112~113행** `notebooks == 35` → `36`, `quizzes >= 35 * 3` → `36 * 3`. 고치기 전 `Expected 35 Part 3 notebooks; found 36`으로 멈췄습니다. 고친 뒤 종료 코드 0.
3. `labs/part3/ch12-retrieval-tuning/README.md`에 13절 한 단락 추가.
4. 12절 b8과 12절 노트북 정리 마지막 줄을 13절로 고쳤습니다(`mdpatch.py`, **12절은 다시 실행하지 않음**). 뒤 챕터(Ch 13·Ch 15) 안내는 13절 b8로 옮겼습니다.
5. `chapter.json`에 13절 추가. **절 시수 30분은 챕터 시수(총 40h · 강의 12h · 실습 28h)에 더하지 않았습니다.**
6. 공용 화면 검사 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json`이 26행 → **28행**(13절 두 줄, 모두 PASS).

### 챕터 마감에 남은 것

1. **`chapter.json`의 `objectives` 다섯째**와 **`textbook/part3/_build_index.py` 88행**의 「TF-IDF와 MMR을 조합한 36건」. 12절 서른여섯 벌은 이제 가중치 여섯 가지 × 관련성 비중 여섯 가지입니다(12절 인계 3번 그대로 남음).
2. **`_build_index.py` 81행 「Ch 9–12 · 32절」**. 디스크의 Part 3 절은 이제 36개(7+9+7+13)입니다. 브리프대로 이번 작업에서는 27행만 고쳤습니다. Part 전체 숫자를 한 번에 맞추세요.
3. **실습 폴더 README 마지막 단락의 「11절의 `gpt-4.1-mini`」**. 11절 개선에서 `gpt-5.4-mini`로 바뀌었습니다. 같은 README 위쪽의 「TF-IDF와 MMR의 개발 설정 36건」·「CrossEncoder … 스모크 실행」도 12절 개선 결과와 어긋납니다.
4. **Ch 13 07절 b3의 「검색된 E01·E02 쪽」 문장**(12절 인계 7번 그대로 남음).
5. `labs/part3/ch12-retrieval-tuning/.venv`(08절이 남긴 빈 폴더)와 `runs/continuity/` 사본 폴더 다섯 개. 삭제 권한이 없어 그대로 두었습니다.
6. 검사 스크립트가 멈추는 자리는 01~12절과 같습니다: `part3/qa/check_continuity.py` 154행 `part2-practice.zip`, `qa/check_course_continuity.py` 212행 `part1-practice.zip`(둘 다 zip 신선도). `part3/qa/check_delivery.py`는 종료 코드 0입니다.

### 검토자가 먼저 볼 세 곳

1. `_src/13-검색-품질-실습.html` b6 표 두 개와 `{{mermaid:13-3-두-실행-비교}}` — 천장에 닿은 재현율과 갈리는 정밀도를 나누어 읽었는지.
2. 노트북 8·9절 두 답과 b7 「답 두 개는 한 번씩만 본 결과입니다」 — 한 번 본 모델 답을 일반화하지 않았는지.
3. `13-diagnosis.md` §6 「챕터 밖 수정」과 위 「챕터 마감에 남은 것」 — 공용 스크립트 수정과 남은 낡은 문장.

## §2-7 리팩터 A — 01~06절 (2026-09-21)

규격 `textbook/QUALITY-UPGRADE.md` §2-7을 Ch 12 **01~06절(core 벌 문서 12건·질문 8건)**에 적용했습니다(작업자 A). 07~13절은 작업자 B 몫이라 손대지 않았습니다(07~13 노트북·`_src`·빌드 HTML 바이트 그대로). 앞 절·앞 챕터에서 배운 함수는 새 도구 파일 `labs/part3/ch12-retrieval-tuning/notebooks/rag_tools.py`에서 한 줄로 가져오고, 벡터 계산은 NumPy로 바꿨습니다. 그림·결과 읽기·설명·정직성 규칙과 절마다의 학습 내용은 그대로이고, 삽화는 새로 만들지 않았으며 Mermaid도 다시 렌더하지 않았습니다(라벨 변경 없음, 렌더 도장 `skip`).

**리팩터 직전 스냅숏(B도 씀)**: `qa/upgrade/before-2-7/` — `_src/`(13개)·`notebooks/`(13개, 출력 포함)·`html/`(빌드 HTML 13개 + `index.html`)·`tests/`(`test_continuity.py`)·`generators/`(`author_01~13.py`)·`figures/`(mmd·캡션 전부)·`lab/`(README·pyproject)·`part3/public-files.json`·`runs-sha256-before/after.txt`(48개)·`data-sha256-before/after.txt`(4개). 모두 `cp -n`. B는 07~13 원본을 여기서 보고, 이 폴더에 덮어쓰지 마세요.

### 조사 (AST, 노트북 여섯 개)

- 함수 정의 전 → 후: 01 12 → 5, 02 14 → 6, 03 19 → 7, 04 10 → 6, 05 13 → 2, 06 14 → 3. **지운 정의 53개**(01 7 · 02 8 · 03 12 · 04 4 · 05 11 · 06 11).
- 리팩터 전 생성기 = 리팩터 전 노트북(셀 글자 같음, `/tmp/ch12-27A/gensync.py`로 확인). 리팩터 뒤에도 01~06 생성기 = 노트북.
- Ch 11 함수 네 개(`unique_doc_ids`·`find_gold_rank`·`recall_at`·`mean_score`)와 02절 `print_hits`는 여섯 노트북 모든 판이 도구 파일 판과 `ast.unparse` 글자가 같습니다(Ch 11 도구 파일 판과도 같음).
- 거리 함수 네 개(`dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`)는 리팩터 전 Ch 9 03절 **반복문 판**이었습니다. Ch 9는 §2-7 리팩터에서 반복문 판을 없애고 03절 한 셀만 NumPy로 적었습니다. 그래서 도구 파일의 `cosine_similarity`는 **Ch 5 02절 NumPy 식**(`np.array`·`@`·`np.linalg.norm`)으로 적고 `# Ch 5 02절에서 배웠습니다`를 달았습니다. `dot_product`·`vector_length`는 `@`·`np.linalg.norm`이 대신해 도구 파일에 넣지 않았습니다.

### 도구 파일 `rag_tools.py` (함수 16개, 코드 107줄, SHA-256 `5154df418d102c996bd80cc8365c9005d190c898034116e836de0b1ff01d4431`)

맨 위 독스트링에 **「01~06절 함수」 / 「07~13절 함수」 두 구역**을 적었고, 파일 끝에 `# 07~13절 함수 (07~13절 노트북을 고칠 때 이 아래에 이어 붙입니다)` 구분 주석을 두었습니다. `import numpy as np` 하나만 불러옵니다(psycopg·Kiwi·BM25는 객체를 인자로 받으므로 불러오지 않음).

| 함수(인자) | 배운 절 | 01~06에서 가져가는 절 | 배운 판과 다른 점 |
|---|---|---|---|
| `cosine_similarity(first, second)` | Ch 5 02 | 01(`cosine_distance` 안) | Ch 5 02절 NumPy 식. 리팩터 전 Ch 12 노트북은 Ch 9 03절 반복문 판 |
| `cosine_distance(first, second)` | 01 | 02·03(05·06은 `rank_by_distance` 안) | 01절 판은 바깥 `similarity_top`을 읽음 → 같은 값 1을 함수 안에서 정함(둘째 줄 주석) |
| `rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)` | 01 | 03(`rank_in_category` 안)·05·06 | **01절 판은 `(id_list, distance_list)`로 차례만 매김**, 05·06절 판은 `(question_vector, top_count)`로 바깥 `doc_ids`·`doc_vectors`를 읽음 → 두 목록을 인자로. 거리 목록 → `np.argsort` → 앞 `top_count`개. 칸 `doc_id`·`거리`(소수 둘째 자리) |
| `unique_doc_ids(hit_list)`·`find_gold_rank(doc_ids, gold_doc_ids)` | Ch 11 01 | 01~06 | 없음 |
| `recall_at(doc_ids, gold_doc_ids, cutoff)`·`mean_score(score_list)` | Ch 11 02 | 01~06 | 없음 |
| `run_search(cur, search_sql, question_vector, top_count)` | 02 | 03 | 바깥 `cur`·`search_sql` → 앞 두 인자 |
| `print_hits(hit_list)` | 02 | 03 | 없음 |
| `find_scan_line(cur, sql_text, value_tuple)` | 02 | 03 | 02절 판은 바깥 `cur`·`search_sql`을 읽고 질문 벡터 하나를 받음. 03절 판(SQL·값을 받음) 본문에 `cur`만 더함 |
| `set_seqscan(cur, setting_value)` | 02 | 03 | 바깥 `cur` → 첫 인자 |
| `kiwi_terms(kiwi, text, keep_tags)` | 04 | 05·06 | 바깥 `kiwi`·`keep_tags` → 첫째·셋째 인자 |
| `count_docs_with(corpus, term)` | 04 | 05(리팩터 전 05는 같은 세기를 셀 안에 다시 적었음) | 바깥 `kiwi_corpus` → 첫 인자 |
| `rank_by_bm25(bm25_model, question_terms, doc_ids, top_count)` | 04 | 05·06 | **04절 판 `(policy_name, question, top_count)`·05·06절 판 `(question, top_count)`는 함수 안에서 낱말을 만듦 → 이 판은 질문의 검색 낱말 목록을 받음**(호출 전 `kiwi_terms()`). 점수에 음수를 붙인 튜플 `sorted` 그대로 → **점수가 같으면 문서 ID 차례**(04절 `C08`·공백 분리 `0.0` 줄이 여기에 기댐) |
| `fuse_scores(ranking_list, weight_list, rank_constant)` | 06 | (없음 — 07~13 몫) | 바깥 `rank_constant` → 셋째 인자. `weight` 변수를 식 안에 넣어 본문 7줄(06절 판 9줄). 06절 판과 200가지 무작위 입력에서 결과 같음 확인 |
| `fuse_rank(ranking_list, weight_list, rank_constant)` | 06 | (없음 — 07~13 몫) | 같은 까닭으로 셋째 인자. 합친 점수가 같으면 문서 ID 차례(06절 `C01` 동점 `0.032`) |

- 함수마다 `# NN절에서 배웠습니다 — …`(앞 챕터는 `# Ch 5 02절`·`# Ch 11 01절`), 인자·본문이 바뀐 함수는 둘째 줄 주석. 금지 문법 0건(게이트 `g1_ladder`·`g2_shape`를 파일에 돌리면 셀 규칙 `multiple_defs_in_cell`·`over_15_lines`만). 함수 본문 최대 8줄(`rank_by_bm25`·`fuse_scores`).
- **넣지 않은 것(그 절만 씀)**: 01 `l2_distance`·`measure_all`·`rank_by_distance(id_list, distance_list)`·`score_one`, 02 `try_hnsw_index`, 03 `find_category`·`make_filler_vectors`·`rank_in_category`·`run_filtered_search`·`set_iterative_scan`·`pick_hits`, 04 `terms_by_policy`·`print_scores`, 05 `print_ranked`(06~13이 쓰지 않음), 절마다 `score_one`.
- **합치지 않은 동명 함수**: 처음 가르친 절의 노트북 판은 그대로 둡니다 — 01 `cosine_distance`(바깥 `similarity_top`)·`rank_by_distance(id_list, distance_list)`, 02 `run_search`·`find_scan_line(question_vector)`·`set_seqscan`(바깥 `cur`), 04 `kiwi_terms`·`count_docs_with`·`rank_by_bm25`(바깥 이름), 06 `fuse_scores`·`fuse_rank`(바깥 `rank_constant`). 도구 파일 판과 인자가 달라 처음 가져오는 절에서 한 문장씩 알렸습니다(아래).

### NumPy — 01절에서 새로 푼 이름과 설명 문장

- 속성 `shape`: 「속성 `shape`에는 표의 행 수와 칸 수가 들어 있습니다.」(출력 `문서 벡터 표의 모양: (12, 256)`)
- 인자 `axis=1`: 「인자 `axis=1`을 주면 표의 행마다 따로 길이를 잽니다.」(`np.linalg.norm(doc_matrix, axis=1)` → 길이 열두 개 `1.0`)
- 배열 빼기: 「NumPy 배열끼리 빼면 같은 자리 숫자끼리 뺀 배열이 나옵니다.」「그 배열의 길이를 `np.linalg.norm()`으로 재면 L2 거리가 됩니다.」(`l2_distance` 본문 2줄)
- `np.argsort`: 「함수 `np.argsort(목록)`는 값을 직접 정렬하지 않고 작은 값부터 그 자리 번호를 차례로 줍니다.」(`rank_by_distance` 본문 3줄)
- Ch 5 이름(`np.array`·`@`·`np.linalg.norm`·`np.round`·`tolist`)은 다시 풀지 않고 「Ch 5 02절에서 NumPy 함수 `np.linalg.norm()`으로 벡터 하나의 길이를 쟀습니다」「Ch 5 02절에서 배운 이 계산을 NumPy로 적은 함수 `cosine_similarity()`」로 가리켰습니다. 반복문 판 거리 계산은 01절에도 두지 않았습니다(규격 §2-7 2항).
- 02~06 노트북은 NumPy를 직접 쓰지 않습니다(도구 파일 안). 도구 파일이 NumPy를 불러오므로 **01~06 설치 셀 모두에 `numpy==2.5.3`**(실습 폴더 `pyproject.toml`·`uv.lock`과 같은 판)을 더했습니다.

### 가져오기 셀과 설명

- 기존 import 준비 셀 끝에 `# …를 도구 파일에서 가져옵니다` + `from rag_tools import …`(알파벳 순, 두 줄): 01 `cosine_similarity, find_gold_rank, mean_score` + `recall_at, unique_doc_ids` / 02 `cosine_distance, find_gold_rank, mean_score` + `recall_at, unique_doc_ids` / 03 `cosine_distance, find_gold_rank, find_scan_line, mean_score, print_hits` + `rank_by_distance, recall_at, run_search, set_seqscan, unique_doc_ids` / 04 `find_gold_rank, mean_score, recall_at, unique_doc_ids` / 05 `count_docs_with, find_gold_rank, kiwi_terms, mean_score` + `rank_by_bm25, rank_by_distance, recall_at, unique_doc_ids` / 06 `find_gold_rank, kiwi_terms, mean_score, rank_by_bm25` + `rank_by_distance, recall_at, unique_doc_ids`. 01은 `import numpy as np`도 더함.
- 쓰지 않게 된 이름을 뺐습니다(AST로 확인, 가져왔는데 안 쓰는 이름 0): `math`(01·02·03·05·06), `similarity_top`(02·03·05·06 값 셀 — 01은 자기 `cosine_distance`가 써서 그대로). 준비 셀 첫 주석의 「제곱근 계산」을 뺐고 `print("불러온 이름:", …)` 목록도 맞췄습니다.
- 준비 설명 셀: 고정 세 문장 「앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.」 + 「이 노트북은 NN절 `f()`…를 가져옵니다.」(01~06 모두). 설치 결과 읽기에 `numpy: 2.5.3` 줄 설명 한 문장.
- **인자 모양 문장(처음 가져오는 자리)**: 03 8절(`run_search()`·`find_scan_line()` — 커서와 SQL, 계획 줄 함수는 넘길 값도)·10절(`set_seqscan()` — 커서를 첫 인자)·11절(`rank_by_distance()` — 01절 판과 다름 세 문장) / 05 3절(`kiwi_terms()`)·4절(`rank_by_distance()` 인자 네 가지)·5절(`rank_by_bm25()` — 04절 판과 다름)·7절(`count_docs_with()`) / 06 「인자 모양은 05절에서 쓴 것과 같습니다」.
- **소절이 통째로 빈 곳 세 개는 코드 셀 없는 설명 소절로 남겨 절 번호를 지켰습니다**: 02 「## 5. 01절 거리 함수 이어 쓰기」, 03 「## 4. 01절 거리 함수 이어 쓰기」, 05 「## 4. 벡터 거리로 순위 만들기」. 정의 셀만 빠지고 다른 셀이 남은 소절: 01 4·5·6·9·10절, 02 7·14절, 03 8·10·11·12절, 04 11절, 05 3·5·7·8절, 06 3·4·6·8절(설명 단락으로 합침).
- 「같은 코드로 다시 정의합니다」 류 문장: 01~06 생성기·노트북·`_src`에서 **0건**. 남긴 「같은 코드」는 경로 찾기 셀 한 줄씩(Ch 9~11과 같게)과 생성기 독스트링의 옛 탐색 기록입니다.
- 03 `rank_in_category`는 범주에 든 문서의 벡터·ID만 골라 도구 파일 `rank_by_distance`에 넘기도록 줄였습니다(본문 9 → 7줄, 학습 내용 「01절 정확 검색을 범주 하나에만」 그대로). 06 `find_gold_rank()`를 문서 하나의 자리를 찾는 데도 쓴다는 설명은 4절(정의 셀 자리)에서 6절 머리로 옮겼고 `_src` b5 「노트북 4절에서」 → 「노트북 6절에서」.
- 준비물 셀: 01 할 일 2 「NumPy로 벡터 길이를 재고 코사인 거리와 L2 거리, 두 가지 자를 만듭니다」, 강의 범위의 「6·7절 정의 셀은 Ch 9 03절에서 쓴 코드라」 → 「Ch 5·Ch 11에서 배운 함수는 도구 파일에서 가져오므로 다시 적지 않습니다」, 02 「5·6절 정의 셀은 01절에서 쓴 코드라」 → 「5절은 도구 파일에서 가져온 01절 함수를 소개하고 6절은 실행만」, 05 「순위 함수 두 개를 정의하는 자리」 → 「가져온 순위 함수 두 개의 인자를 확인하는 자리」, 기준 버전에 numpy 2.5.3(01~06).
- `_src`: 01 b3(Ch 9 03절 반복문 함수 세 개 설명 → Ch 5 02절 NumPy·Ch 9 03절 확인·`cosine_similarity()` 가져오기, 도구 파일 단락), 02~06 b3 도구 파일 단락, 05 b5, 06 b5. b4 이후·그림·복습은 그대로.
- 실습 폴더 README 한 문장(「01~06절 노트북은 앞 절과 앞 챕터에서 배운 함수를 `notebooks/rag_tools.py`에서 가져오므로, 이 파일을 노트북과 같은 폴더에 그대로 둡니다」) — B가 07~13을 끝내면 「01~13절」로 고치세요.

### 절별 전 → 후 (코드 줄은 주석·빈 줄 제외, `textbook/_notebook/upgrade/count_code.py`)

| 절 | 코드 셀 | 코드 줄 | 바뀐 것 |
|---|---|---|---|
| 01 | 31 → 24 | 197 → 156 (−41) | 정의 7개 삭제, 길이·L2·순위를 NumPy로 |
| 02 | 39 → 31 | 240 → 201 (−39) | 정의 8개 삭제(5절 설명 소절) |
| 03 | 51 → 39 | 303 → 238 (−65) | 정의 12개 삭제(4절 설명 소절), `rank_in_category` 줄임 |
| 04 | 28 → 24 | 170 → 147 (−23) | Ch 11 정의 4개 삭제 |
| 05 | 30 → 19 | 223 → 155 (−68) | 정의 11개 삭제(4절 설명 소절), 낱말 세기 셀 한 줄로 |
| 06 | 31 → 20 | 245 → 181 (−64) | 정의 11개 삭제 |
| 01~06 합계 | **210 → 157 (−53)** | **1378 → 1078 (−300, −21.8%)** | 도구 파일 107줄을 더해도 1185(−193, −14.0%). 도구 파일 107줄 가운데 `fuse_scores`·`fuse_rank` 17줄은 07~13 몫 |

늘어난 셀: 06 4절 순위 목록 셀 12 → 13줄(질문 낱말 한 줄), 05 9절 기록 셀 9 → 10줄. `verify.py --chapter` 셀 최대 20줄은 리팩터 전부터 있던 11절 셀입니다.

전·후 코드 한 토막(01 6절, 거리 순위):

```python
# 전 — 튜플에 담아 sorted
def rank_by_distance(id_list, distance_list):
    pairs = []
    for i in range(len(id_list)):
        pairs.append((distance_list[i], id_list[i]))
    ranked = []
    for pair in sorted(pairs):
        ranked.append({"doc_id": pair[1], "거리": round(pair[0], 2)})
    return ranked

# 후 — np.argsort로 자리 번호를 받아 바로 꺼냄
def rank_by_distance(id_list, distance_list):
    ranked = []
    for position in np.argsort(distance_list):
        ranked.append({"doc_id": id_list[position], "거리": round(distance_list[position], 2)})
    return ranked
```

(05절은 정의 셀 다섯 개 — 거리 함수 네 개 20줄 + 05절 판 `rank_by_distance` 8줄 — 가 준비 셀 한 줄과 호출 `rank_by_distance(query_vectors[0], doc_vectors, doc_ids, top_three)`로 바뀌었습니다.)

### 다시 실행과 대조

- 01~06을 `run_section.sh`로 새 커널 2회: A(`/tmp/ch12-27A/A/`, `executed_at` 2026-09-21T07:31~07:39Z)·B(교재 출력, `executed_at` 2026-09-21T07:40:04~33Z). A 뒤에 고친 것은 마크다운 문장(01 기준 버전 한 줄·02 결과 읽기 두 곳)뿐이고 코드 셀 글자는 A·B가 같습니다. 값을 고르려고 더 실행하지 않았습니다. 대조 스크립트 `/tmp/ch12-27A/outs.py`(셀 첫 주석 줄로 짝지음).
- **A·B 차이: 01~06 모두 없음**(셀 출력 글자 같음).
- **리팩터 전(2026-09-18 출력)과 대조: 값이 담긴 출력은 여섯 절 모두 글자까지 같습니다.** 다른 줄은 설치 셀의 `numpy: 2.5.3` 한 줄(01~06), 준비 셀 `불러온 이름:` 목록(`math` 빠짐, 01은 `numpy`), 01 새 줄 `문서 벡터 표의 모양: (12, 256)`, 05·06 값 셀에서 빠진 `코사인 유사도의 가장 큰 값: 1`뿐입니다. 그래서 **결과 읽기·그림 라벨·복습의 인용 값은 고칠 곳이 없었습니다**(설치·준비 셀 결과 읽기만 새 줄에 맞춤).
- 흔들리기 쉬운 값 확인: 01 거리 `0.43`·`0.56`·`0.62` / `0.93`·`1.06`·`1.11`·관계 값 `1.12`(둘째 자리까지), 02 `EXPLAIN` 세 계획 줄·`ef_search` 두 줄, 03 반복 탐색 `off` **0줄** → `strict_order`·`relaxed_order` **3줄**·색인 경로 질문 평균 `0.375`, 05 `C01 | 2 | 3`·`C02 | 7 | 1`, 06 `C01` 동점 `0.032`(`LIB-001` 2위)·가중치 1.5에서 `C01 | 2 | 3` — 모두 두 실행·리팩터 전과 같습니다.
- **§2-7 10항 판단 — 입력을 고친 절 없음**(핵심 관찰이 하나도 뒤집히지 않음). 답 모델을 쓰지 않는 여섯 절이고 임베딩 결과의 소수 셋째 자리 흔들림은 둘째 자리 반올림 아래였습니다.
- 날짜: 생성기 `RUN_DATE`(nbkit) 2026-09-21 → 01~06 「이 노트북의 출력은 2026-09-21에」. `_src` 01~06에는 실행 날짜 문장이 없고 참고 자료 확인일(2026-09-18)은 그대로.
- `code_sha256`/`outputs_sha256`(전 → 후): 01 `727b3bdf`/`ef039ce7` → `9ba38397`/`1cd487f8`, 02 `17978388`/`9947bfc4` → `8697501f`/`0d50288c`, 03 `56595a04`/`76e5c409` → `6ac446c6`/`43e4dcea`, 04 `a5606d20`/`ad046983` → `c071a07a`/`48264f65`, 05 `9210ae09`/`5c061480` → `39a16474`/`8c7e0c90`, 06 `28482c02`/`91e5c8c0` → `4d92c784`/`f513eb87`. 이 해시를 코드로 읽는 곳은 없고, 옛 값은 `집필점검표.md`·`qa/verification.md`·`NN-diagnosis.md`·이 handoff 앞 절(당시 기록)에만 있습니다.

### 산출 파일 — 01~06은 파일을 쓰지 않습니다

- 다시 실행해도 `runs/`·`data/`에 쓴 파일 없음: `runs/` 48개 해시 목록 전 = 후(묶음 `46c130da0a738062291d396c18ef57111af1a45394959a64640e0ae94131abec`), `data/` 4개 전 = 후(묶음 `bc4fa5c08fa9bef7d45051889b936df96f1b85e663fff9edc52af852e5dee9f5`). `runs/core-01~06-*.json`(옛 기록)·12절 계약 파일 세 개 바이트 그대로.
- 실습 폴더에 새로 생긴 것: `notebooks/rag_tools.py`와 커널이 가져오며 만든 `notebooks/__pycache__/rag_tools.cpython-312.pyc`(삭제 권한 없음 — 묶음 목록은 파일을 하나씩 적어서 들어가지 않고 챕터 `qa/public-files.json` `exclude`에도 `**/__pycache__/**`).
- pgvector 표 `ch12_core_hnsw`·`ch12_core_filter`는 02·03이 지우고 다시 만드는 표라 `.cache/vm/pgdata`에서만 바뀜(교재·실습 폴더 밖).

### 검사

- `upgrade_gates.py --label wip-2-7-A` **13/13 PASS, G1~G7 0**(`qa/upgrade/gates-wip-2-7-A.json`). 01~06 절마다 `run_section.sh` 게이트도 0.
- `verify.py --chapter` `PASS 13 sections / 406 code cells (max 20 lines)`(459 → 406).
- 빌드 HTML 14개 `{{` 0건. **07~13·`index.html`은 리팩터 전 빌드와 바이트가 같음**(`before-2-7/html/` 대조).
- `visual.cjs`(Ch 11 사본 `/tmp/ch12-27A/vis/vis.cjs`, chrome-headless-shell) 01~06 × 1280·390px — **파일마다 새로 연 창에서 12/12 PASS**(`qa/upgrade/visual-after-2-7.json`). 참고: 여섯 파일을 한 창에서 차례로 열면 03·04·05의 xychart 글자 `자리 3`이 svgBounds로 걸립니다. 같은 스크립트로 **리팩터 전 HTML(03~05)**을 돌려도 둘째 파일부터 같은 자리에서 걸려 이번 변경과 무관한 도구 쪽 현상입니다(창마다 열어 재면 그 글자가 SVG 오른쪽 끝에서 0.28px 넘침 — 허용 0.5px 안). 공용 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json` 28행은 **그대로 둠**.
- 생성기 ↔ 노트북 대조 01~06 셀 글자 같음. review-pack 01~06 다시 만듦(`pack.py`).
- 실습 폴더 테스트 `tests/test_continuity.py` **4 passed**(`--with pytest==9.1.0`, `venv-ch12-retrieval-tuning`) — 08·10·12 노트북만 읽어 이번 작업과 무관, 테스트는 고치지 않음.
- 서비스 요청: 임베딩 `text-embedding-3-small` 9번 × (01·02·03·05·06) × 2회 = **90번**, 04는 0번, 답 모델 0번, 리랭커 0번. 보낸 글이 한 번에 900자 아래라 예상 비용 0.001달러 미만.

### 공용·챕터 밖 변경

- `textbook/part3/public-files.json`: `labs/part3/ch12-retrieval-tuning/notebooks/rag_tools.py` 한 줄(`advanced-queries.json` 줄 뒤).
- `textbook/_notebook/checks/notebook-contracts-part3-ch12-retrieval-tuning.json`: `run_section.sh` 안의 `verify.py`가 실행마다 다시 씀(자동, 손으로 고치지 않음).
- 그 밖의 공용 도구·검사 스크립트·Part 3 목차·`part3-practice.zip`·다른 챕터: 변경 없음. **학생 묶음은 B가 챕터 마감에서 `_build_index.py`로 한 번 다시 만듭니다**(지금 zip에는 새 01~06 노트북·도구 파일이 없음).
- 챕터 안: `qa/public-files.json`(새, Ch 11 모양), 실습 폴더 README 한 문장, 생성기 01~06, `_src` 01~06, 노트북 01~06, 도구 파일, `qa/upgrade/visual-after-2-7.json`·`gates-wip-2-7-A.json`, `gates-wip-01~06.json`(run_section이 덮어씀), review-pack 01~06.

### B에게 넘길 것

1. **도구 파일 구조**: `rag_tools.py` 독스트링의 두 구역 설명을 지키고, 07~13절 함수는 파일 끝 `# 07~13절 함수` 구분 주석 아래에 이어 붙이세요. 01~06 구역 함수의 인자 모양은 위 표 그대로이고 01~06 노트북이 그 모양으로 부르므로 **바꾸면 01~06을 다시 실행해야 합니다**.
2. **07~13절이 그대로 가져갈 수 있는 것**: `cosine_similarity`(10·12 MMR의 `similarity_to_chosen` 등 — NumPy 판, 스칼라 반환), `cosine_distance`, `kiwi_terms(kiwi, text, keep_tags)`, `fuse_scores`·`fuse_rank(ranking_list, weight_list, rank_constant)`(안의 변수 이름이 `doc_id`여도 문서 청크 ID 목록에 그대로 동작), `recall_at`·`mean_score`·`find_gold_rank`(07). `dot_product`·`vector_length`는 도구 파일에 없습니다 — 07~13도 `cosine_similarity` 안에서만 쓰니 함께 지우면 됩니다.
3. **advanced 벌용 동명 판 주의**: 07~13절 `rank_by_distance(question_vector, top_count)`·`rank_by_bm25(question, top_count)`는 바깥 `chunk_ids`·`chunk_vectors`·`bm25_model`을 읽고 **칸 이름이 `chunk_id`**입니다(`unique_chunk_ids()`가 `hit["chunk_id"]`를 읽음). 도구 파일 01~06 판은 **칸 `doc_id`**라 그대로 쓰면 07~13 결과가 깨집니다. 07~13 구역에 문서 청크용 판을 따로 두거나(예: 칸 이름을 가른 다른 이름), 호출 쪽을 정하세요. `parent_ids_of`·`unique_chunk_ids`·`chunk_precision_at`·`eligible_items` 등 07절 이후 함수는 아직 도구 파일에 없습니다.
4. **NumPy로 바꾸면 달라질 수 있는 출력**: (a) `np.float64`를 목록·딕셔너리째 `print`하면 `np.float64(0.28)`로 찍힘(01~06은 값을 하나씩 찍어 영향 없음), (b) 같은 벡터끼리 코사인 거리는 `-0.0`으로 찍힐 수 있음(도구 파일 판으로 확인), (c) `np.argsort` 기본값은 같은 값의 차례를 보장하지 않음 — 거리(실수)는 동점이 사실상 없어 `rank_by_distance`만 `argsort`로 두었고, **BM25·합친 점수처럼 동점이 나는 정렬은 튜플 `sorted`(동점이면 ID 차례)를 그대로 두었습니다**. 07절 리랭킹 점수 동률(`round(…, 4)`)도 같은 주의.
5. **테스트 고칠 곳**: `tests/test_continuity.py`의 `load_notebook_function()`·`load_notebook_namespace()`(22~55행)는 이름 공간에 **sklearn `cosine_similarity`와 `np`를 미리 넣습니다**. 10·12 노트북에서 `cosine_similarity` 정의를 지우고 도구 파일에서 가져오면 테스트는 sklearn 판(행렬 API)을 쓰게 되어 깨집니다. §2-7 7항대로 도구 파일(`notebooks/rag_tools.py`)의 함수 정의도 이름 공간에 먼저 읽도록 고치세요(확인하는 성질은 그대로). 185행 10절 블록은 `{"similarity_top": 1, "math": math}`를 넣습니다.
6. **스냅숏**: `qa/upgrade/before-2-7/`(위). 07~13 리팩터 전 `_src`·노트북·생성기·빌드 HTML·테스트가 모두 있습니다. `cp -n`으로만 더하세요.
7. **챕터 마감 때 고칠 줄(A는 고치지 않음)**: `qa/upgrade/chapter-summary.md` 6행(코드 셀 `31·39·51·28·30·31` → `24·31·39·24·19·20`, 합계), 29행(01 행 `math.sqrt`·`dot_product`·`vector_length`·`cosine_similarity` → NumPy·도구 파일), 44행(「쓰지 않은 이름」의 `numpy`·`np` — 01이 `np.array`·`np.linalg.norm(axis=1)`·`np.argsort`·`np.round`·`shape`·`tolist`를 씀), 50행(「거리 네 개는 … 글자까지 같은 코드」 → 도구 파일), 54행(「새 절을 쓸 때 이 함수들을 같은 코드로 다시 정의하세요」), 193행(「아직 가르치지 않은 것: `numpy`」); `집필점검표.md` 44~49행(01~06 셀 수·해시)·67행(코드 셀 합계); `qa/verification.md` 11~16행; `textbook/qa/upgrade-contracts.md` §4 93행(「거리 네 개는 Ch12 01~13절이 글자까지 같음」)·§3 81행 Ch14 줄(「거리 넷과 `rank_by_distance`(Ch12 01·**05절 판**)」 — Ch 12 도구 파일 판은 인자 네 개)·§4·§5에 Ch 12 줄 추가. `refactor-2-7-progress.md` Ch 12 행은 B가 A 행을 합쳐 마감.
8. **리팩터 전부터 있던 어긋남(고치지 않음)**: 01·02 준비물 「강의와 실습 범위」의 절 번호가 소절 번호와 조금 어긋납니다(01 「2~5절과 8·9절 … 실행 1과 실행 2」 — 실행 1·2는 7·8절, 02 「7~9절 … 실행 1과 색인 만들기, 실행 2」 — 실제 9·10·11절). A는 정의 셀 문장만 고쳤습니다. 마감 때 한 번에 보세요.
9. 학생 묶음을 다시 만든 뒤 묶음을 풀어 `notebooks/`를 작업 폴더로 01(또는 05)을 새 커널로 돌려 `from rag_tools import …`가 PYTHONPATH 없이 되는지 확인하세요(`run_section.sh`는 PYTHONPATH를 넣어 주므로 교재 실행만으로는 확인되지 않음).

## §2-7 리팩터 B — 07~13절과 챕터 마감 (2026-09-21)

규격 `textbook/QUALITY-UPGRADE.md` §2-7을 Ch 12 **07~13절(advanced 벌 — 부모 문서 6건·문서 청크 175개·질문 30개)**에 적용하고 챕터를 마감했습니다(작업자 B). 01~06절 노트북·생성기·`_src`는 손대지 않았고 다시 실행하지 않았습니다. 도구 파일의 01~06절 구역도 함수 본문·인자 그대로이고, 맨 위에 `import math` 한 줄(Ch 11 `rank_weight`용)과 독스트링 둘째 구역 설명만 바뀌었습니다. 그림·결과 읽기·설명·정직성 규칙과 절마다의 학습 내용은 그대로이고 삽화는 새로 만들지 않았습니다. 스냅숏은 A의 `qa/upgrade/before-2-7/`을 그대로 썼고(`cp -n`만), 12절 산출 파일 해시 목록 `before-2-7/runs-sha256-after.txt`(A가 남긴 48개)가 작업 직전 상태와 같음을 확인했습니다.

### 도구 파일 07~13절 구역 (함수 17개 추가 → 모두 33개, 코드 줄 107 → 220, SHA-256 `db3fe94f13df80eed02ecac1ec3c74141c0e6bee1114d1f252735d530523dfb0`)

| 함수(인자) | 배운 절 | 가져가는 절 | 배운 판과 다른 점 |
|---|---|---|---|
| `rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, top_count)` | 01(05·06 인자 모양) | 07~13 | **advanced 벌 동명 판 처리**: 리팩터 전 07~13절 `rank_by_distance(question_vector, top_count)`는 바깥 `chunk_ids`·`chunk_vectors`를 읽고 칸이 `chunk_id`였음. 01~06 구역 `rank_by_distance`(칸 `doc_id`)를 그대로 부르고 칸 이름만 `chunk_id`로 옮기는 판을 **이름을 달리해** 07~13 구역에 둠(01~06 구역 인자 그대로 → 01~06 재실행 없음). 거리 계산은 NumPy(`cosine_similarity`)·`np.argsort` |
| `rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, top_count)` | 04 | 07~13 | 같은 방식으로 04절 `rank_by_bm25`를 부름. 점수가 같으면 ID 차례(튜플 `sorted`) 그대로. 질문 낱말은 호출 전 `kiwi_terms(kiwi, text, keep_tags)` |
| `unique_chunk_ids(hit_list)` | Ch 11 01(`unique_doc_ids` 모양, 07절 문서 청크 판) | 07~13 | 없음(07절 판과 본문 같음) |
| `parent_ids_of(found_chunk_ids, parent_by_chunk)` | 07 | 08~13 | 07절 판은 바깥 `parent_by_chunk` → 둘째 인자. **07 노트북은 자기 판 유지** |
| `eligible_items(subset)` | 08 | 09~12 | 없음. **08 노트북은 자기 판 유지** |
| `chunk_precision_at(found_chunk_ids, gold_doc_ids, cutoff, parent_by_chunk)` | 08 | 09~13 | 08절 판은 바깥 `parent_by_chunk` → 넷째 인자. **08 노트북은 자기 판 유지** |
| `count_tokens(encoding, text)` | Ch 8 01 | 09 | Ch 8·9·10 도구 파일 판과 같은 인자·본문. 리팩터 전 09절 판은 `count_tokens(text)`로 바깥 `encoding`을 읽음 |
| `similarity_to_chosen`·`mmr_score`·`best_candidate`·`mmr`·`mmr_pick(question_vector, found_chunk_ids, place, relevance_weight, vector_by_chunk)` | 10 | 12 | `mmr_score`는 10절 판이 읽던 `similarity_top`(1)을 함수 안에서 정함, `mmr_pick`은 바깥 `vector_by_chunk` → 다섯째 인자. 닮은 정도는 도구 파일 `cosine_similarity`(NumPy). **10 노트북은 다섯 개 모두 자기 판 유지**(10절 노트북 판도 가져온 NumPy `cosine_similarity`를 부름) |
| `precision_at`(Ch 11 03)·`rank_weight(rank)`·`dcg_at`·`ideal_dcg(gold_count, cutoff)`·`ndcg_at`(Ch 11 04) | Ch 11 03·04 | 12(`precision_at`·`ndcg_at`) | **Ch 11 도구 파일 판과 본문 같음**(주석만 「Ch 11 NN절」). 리팩터 전 12절 판은 `rank_weight(position)`(0부터)·`ideal_dcg(gold_doc_ids, cutoff)`·합 `0.0` 시작이었으나 `log2`에 들어가는 정수가 같아 값이 같음(12절 시험 기록이 run_id 말고 바이트까지 같게 나옴) |

- 함수마다 `# NN절에서 배웠습니다 — …`, 인자가 바뀐 함수는 둘째 줄 주석. 금지 문법 0건(게이트 `g1_ladder`·`g2_shape`를 파일에 돌리면 셀 규칙 `multiple_defs_in_cell`·`over_15_lines`만). **함수 본문 최대 10줄 = `eligible_items`(08절 판 그대로), 9줄 `best_candidate`(10절 판 그대로)** — 이번 지시의 「8줄 이하」를 넘지만 가르친 판과 글자를 맞추려고 줄이지 않았습니다(규격 L2 상한 10줄 안).
- **넣지 않은 것(그 절만 씀)**: 07 `make_pairs`·`rerank`·`score_one`, 08 `score_candidates`·`order_by_score`·`evaluate`, 09 `total_tokens`·`parent_texts_of`·`summarize`, 10 `mmr_row`, 11 `ranking_lists`·`candidates_of`·`measure`·`rewrite_question`·`branch_row`, 12 `file_fingerprint`·`write_text`·`question_lists`·`candidates_of`·`metrics` 등 13개, 13 다섯 개. 12 `question_lists(question_vector, question)`는 11 `ranking_lists(question)`(함수 안에서 임베딩)와 모양이 달라 합치지 않았습니다.

### 생성기·노트북·`_src`

- 준비 셀(import 셀 끝)에 `# …를 도구 파일에서 가져옵니다` + `from rag_tools import …`(알파벳 순, 두세 줄): 07 8개 · 08 7개 · 09 10개 · 10 10개(`cosine_similarity` 포함) · 11 9개 · 12 12개 · 13 8개. 쓰지 않게 된 `import math`를 07~13에서, `similarity_top`을 07·08·09·11·12·13 값 셀에서 뺐습니다(10은 `mmr_score`가 써서 남김). 준비 설명 셀에 고정 세 문장 + 「이 노트북은 … 가져옵니다」, 설치 결과 읽기에 `numpy: 2.5.3` 한 문장, 설치 셀에 `numpy==2.5.3`(07~13).
- `kiwi = Kiwi()`는 없어진 `kiwi_terms` 정의 셀 대신 BM25 셀 첫 줄로 옮겼습니다(05·06절 A 방식).
- **소절 번호를 지킨 설명 소절**(코드 셀 없음): 07 「## 5. 1차 검색 함수의 인자 확인하기」 · 08 같은 제목 5절 · 09 「## 5. 앞 절 함수의 인자 확인하기」 · 10 5절 · 11 4절 · 12 4절 · 13 4절. 「강의와 실습 범위」의 절 번호는 그대로 맞습니다.
- 09 조각 수 셀은 `total_tokens`만 남아 준비 셀이 아닌 보통 정의 셀이 됐습니다(09절이 처음 가르침). 09·10·11·13 생성기의 `prep()` 도우미를 뺐고 12는 `FILE_HELPERS`가 써서 남겼습니다.
- 「같은 코드로 다시 정의합니다」 류 문장: 07~13 생성기 셀·노트북·`_src`에서 **0건**. 남은 「같은 코드」는 경로 셀 설명, 12 `CHUNK_TEXTS`·13 `CHUNK_MAPS` 첫 줄 주석, 12 `file_fingerprint` 설명(Ch 11 01절 인라인 코드) — 다시 정의 문장이 아닙니다.
- 늘어난 셀(질문 낱말 한 줄): 07 후보 셀 12 → 13줄 · 09 10 → 11 · 10 12 → 13 · 11 `SEARCH_FUNCS` 14 → 15(verify 최대 20 → **21줄**, 주석·빈 줄 포함) · 12 `SEARCH_FUNCS` 7 → 8 · 13 `PREPARE_Q` 12 → 13, 설치 셀은 `numpy` 한 줄씩. 08 후보 셀은 `fuse_rank(…)[:candidate_count]`로 한 줄을 합쳐 15줄 그대로. 셀 최대 코드 줄은 08·11·12의 15줄(규격 §2-4 상한).
- `_src` 07~12 b3에 도구 파일 단락, 08 b3 「07절과 같은 코드로 만듭니다」 → 「같은 방법으로」, 09 b3 `count_tokens()` 문장, 10 b3 「01절 … 함수」 → Ch 5 02절 NumPy `cosine_similarity()`, 11 b3 「같은 코드로 다시 씁니다」 → 도구 파일, 12 b7 「순위 상수를 손잡이로 두면 06절 `fuse_scores()`의 모양을 바꿔야」 → 「06절에서 정한 60을 모든 설정에 그대로 썼습니다」(도구 파일 판은 순위 상수를 인자로 받아 옛 까닭이 없어짐), 13 함수 표 「가져온 곳」 → 「도구 파일」·b5 두 문장·출력 날짜 2026-09-19 → 2026-09-21.

### 절별 전 → 후 (코드 줄은 주석·빈 줄 제외, `count_code.py`)

| 절 | 코드 셀 | 코드 줄 | 지운 정의 |
|---|---|---|---|
| 07 | 37 → 24 | 307 → 224 (−83) | 13(거리 넷·순위 둘·`kiwi_terms`·`unique_chunk_ids`·`find_gold_rank`·합치기 둘·Ch 11 둘) |
| 08 | 33 → 21 | 281 → 203 (−78) | 12 |
| 09 | 32 → 23 | 303 → 206 (−97) | 13(`count_tokens` 포함) |
| 10 | 31 → 22 | 292 → 199 (−93) | 13 |
| 11 | 31 → 22 | 293 → 199 (−94) | 14 |
| 12 | 54 → 38 | 532 → 372 (−160) | 24(준비 셀 16개 164줄 → import 세 줄) |
| 13 | 31 → 23 | 272 → 188 (−84) | 13 |
| 07~13 합계 | **249 → 173 (−76)** | **2280 → 1591 (−689, −30.2%)** | 102 |
| 01~13 챕터 합계 | **459 → 330 (−129)** | **3658 → 2669 (−989, −27.0%)** | 도구 파일 220줄을 더해도 2889(−769, −21.0%) |

### 다시 실행과 대조

- 07~13을 새 커널 2회: A(`executed_at` 08:12~08:16Z, 07 73초·08 109초)·B(교재 출력, 08:17~08:20Z, 07 61초·08 105초). 07·08은 실행(`execute.py`, `timeout 170`)과 `run_section.sh … --no-exec`를 나눠 불렀습니다. A·B 사이 코드 셀 글자는 같고, 결과 읽기 글을 고친 뒤에는 마크다운만 생성기에서 노트북으로 옮겼습니다(`/tmp/ch12-27B/mdsync.py` — 코드 셀 글자가 같을 때만 마크다운 셀 글을 옮김). 값을 고르려고 더 실행하지 않았습니다. 대조 스크립트 `/tmp/ch12-27B/outs.py`(셀 첫 주석 줄로 짝지음, /tmp라 곧 사라짐).
- **A ↔ B 차이**: 07·08·10 없음. 09 `부모 문서 | 1.6 | 4213 | 6` ↔ `4206`. 11 `기록 없이 재작성문`의 `Q085` 문장(표 값은 같음). 12 7절 두 표(문서 청크 정밀도 서로 다른 값 열네 ↔ 열다섯 가지, 손잡이별 평균 여러 줄)와 `그 줄의 문서 청크 정밀도 자리 5: 0.8667` ↔ `0.88`(고른 설정·시험 표·통합 실행은 같음). 13 두 답의 표현(실행 1 권수·기간 답, 실행 2 「자료에 없다」는 같음).
- **리팩터 전(2026-09-18·19 출력)과 대조(B)**: 07·08 값 출력 **모두 같음**(리랭킹 점수·`3·4·5위` 동점 모양·08 정밀도 표·질문별 표 포함). 09 `문서 청크 | 5.0 | 596 | 15` → `600`(A·B 같음)·`문서 청크 정밀도 자리 5: 0.853` → `0.84`(A·B 같음)·`4206`은 B가 같고 A는 `4213`. 10 `0.5 | 2.07 | 0.75 | 1.0` → `0.76`(A·B 같음). 11 값 같음(B의 `Q085` 문장도 리팩터 전과 같음). 12 7절 두 표 값만 다름. 13 실행 2 답 표현만 다름. 다른 줄은 설치 셀 `numpy: 2.5.3`·준비 셀 이름 목록(`math` 빠짐)·빠진 `코사인 유사도의 가장 큰 값` 줄(07·11·12).
- **고친 인용**: 09 노트북 결과 읽기 `600`·`0.84`와 흔들림 한 문장, 정리 2번 「4206이 되었습니다」 → 「4200을 넘었습니다」, `_src` b5 `600`·b6 「조각 600개였고 … 4200개를 넘었습니다」·「4200 남짓에서 2502로」·b7 흔들림 항목(`4213`·`0.853`을 적고 라벨·정리는 약 4200)·b8, 그림 `09-1`·`09-4` 라벨 「조각 수 4206」 → 「조각 수 약 4200」·`09-3` 막대 `[596, 2502, 4206]` → `[600, 2502, 4206]`(세 장 다시 렌더)·`09-1` 캡션·alt 두 곳, 노트북 「오늘 볼 그림」 alt(옛 `596` 한 곳도 뺌). 10 노트북 결과 읽기 두 곳과 `_src` b6 표·본문·복습 1문항 `0.75` → `0.76`. 12 `_src` b6 손잡이 표 여덟 칸·「열네 가지」 → 「열다섯 가지」, b7 「새 커널 네 번」·「네 번 모두」 → 「두 번」(이번 두 실행에서 라벨·정리 값이 같았고 고른 설정도 같았음, `0.8667` 문장은 그대로 맞음). 13 `_src` 날짜.
- **§2-7 10항 — 입력을 고친 절 없음.** 핵심 관찰이 두 실행 모두 그대로입니다: 07 리랭킹 1위 `E01-P03-C01`(1차 자리 3)·후보 둘에 없음 `False`·1위가 바뀐 질문 `Q002`·`Q039`·`Q087`, 08 부모 재현율 아홉 줄 `1.0`·정밀도 `0.4` → `0.84`/`0.893`/`0.867`·보고 자리 3에서 `0.933`, 09 부모 두 건이 일곱 배 가까이 길고 가용분에 든 질문 6 → 15, 10 비중을 낮추면 부모 수 ↑ 정밀도 ↓, 11 대상 빠짐 `2.2`·`0.72` → 재작성 `1.4`·`0.88`, 12 고른 설정 `[0.0, 1.0]`·`1.0`·시험 `ndcg_at_5` `0.9754`, 13 실행 2 `Q002` 정밀도 `0.4`·답이 권수·기간을 찾지 못함.

### 12절 산출 파일 — 전후 해시와 값

| 파일 | 전 | 후 |
|---|---|---|
| `runs/advanced-continuity-experiment-log.jsonl` | `9b447a417c3ed9ec54788f26f9f4392870c9b9d49768fc02459dac1b12dd20e3` | `f16aa3587b2bdb113333e9ecccb8d28ea4bd76c1ee0d31f9a392db4fbe498506` |
| `runs/advanced-continuity-test-result.json` | `f9b16717d910d8612742979ae25ceb3870e03c4a098373984f064dc6527a565c` | `7b9b9db75a3986f616aeb5c1c35cdb11261adb37066b3327d5dc212d9df78094` |
| `runs/advanced-continuity-integrated-result.json` | `ce76d3d8e3139d1691a0ee84d9f67d38c5170b273d08572447ac9dbc2feb2651` | `7b142cd570aa8a4faace07ca1d7c236849124d2858b5e78d198f716bb47bf81e` |

- 사본 `runs/continuity/20260921T082024/`(run_id 머리 `advanced-continuity-20260921T082024`). 첫 실행(A) 사본 `runs/continuity/20260921T081609/`는 `qa/upgrade/before-2-7/runs/moved/20260921T081609/`로 `mv -n`(삭제 아님, 해시 `37d5fbf2…`·`b7d68754…`·`87c87176…`). 옛 사본 8개(`20260910T*`·`20260918T*`, `20260918T232052/` 포함)는 바이트 그대로. `runs/` 파일 48 → **51개**, 해시 목록 묶음 `46c130da0a738062…` → `7f93a0bb09d6cfa9…`(`before-2-7/runs-sha256-after-B.txt`). `data/` 4개 그대로. `core-0N`·`advanced-*`(옛) 그대로.
- **고른 설정 같음**: 가중치 `[0.0, 1.0]`·관련성 비중 `1.0`(`selected_run_id` `…-dev-31`). **시험 기록은 `run_id`·`selected_run_id`·`run_date` 말고 바이트 단위 내용이 같음**(지표 `recall_at_3/5/50` `1.0`·`precision_at_5` `0.2`·`ndcg_at_5` `0.9754`·`chunk_precision_at_5` `0.8533`, 질문별 결과 15줄 같음). **통합 기록은 `run_id` 말고 같음**: `qid` `Q002`·`retrieved` `E01-P03-C02`(p.3, 1)·`E01-P03-C01`(2)·`E01-P03-C06`(3)·`response` 「도서는 한 번에 **7권까지** 빌릴 수 있고, **14일 동안** 대출할 수 있습니다. [E01 p.3]」·`settings`(`chat` `gpt-5.4-mini`·`dimensions` 256·`reranker` `null`) 같음. 개발 기록 36줄 가운데 19줄의 질문별 결과, 10줄의 `metrics`·`slices`가 달라졌습니다(문서 청크 정밀도 쪽, 임베딩 흔들림). 키·칸 이름·줄 수 같음.
- **읽는 쪽**: 실습 폴더 테스트 4 passed · `check_continuity.py`·`check_course_continuity.py` 사본 Ch 12 블록 통과 · **Ch 13 07절**이 읽는 `qid`·`question`·`gold_doc_ids`·`retrieved[].chunk_id`·`settings.reranker`·`settings.context_selection`이 모두 같아 **Ch 13 07·08 노트북 출력·본문 인용은 바뀌지 않습니다**(08절은 문서 파일만 읽음, 다시 실행하지 않음). 다만 Ch 13 문서(`qa/upgrade/chapter-summary.md`·`review-round1.md`)가 옛 해시를 인용합니다. **Ch 15 01절**: 새 시험 기록에서도 `ndcg_at_5 < 1`인 줄은 **1개**(`Q090`, 첫 문서 `H02`, 정답 `['H01']`, `recall_at_5` `1.0`, `ndcg_at_5` `0.6309`) — Ch 15 `_author.py` 212행(기대 2)이 깨진 상태 그대로, Ch 15 파일은 고치지 않음(`upgrade-final-checklist.md` §2 갱신).

### 검사

- `upgrade_gates.py --label after-2-7` **13/13 PASS, G1~G7 0**(`qa/upgrade/gates-after-2-7.json`). 중간에 12절 4절 첫 단락이 여섯 문장이라 G6 1건 → 단락을 나눠 0.
- `verify.py --chapter` `PASS 13 sections / 330 code cells (max 21 lines)`. 빌드 HTML 14개 `{{` 0건, `index.html`은 리팩터 전과 바이트 같음.
- `visual.cjs`(A 사본 `/tmp/ch12-27A/vis/vis.cjs`, 파일마다 새 창) 07~13 × 1280·390 **14/14 PASS** → `qa/upgrade/visual-after-2-7.json`에 A의 12행과 합쳐 **26행**. 공용 `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json` 28행은 그대로.
- 생성기 ↔ 노트북 셀 글자 07~13 같음(`mdsync.py --check` 0). 실습 폴더 테스트 **4 passed**(`tests/test_continuity.py`를 고친 뒤, 실행 전·후 모두).
- Mermaid CLI가 `/tmp/mmd`에서 사라져 README 절차대로 다시 설치하고 `09-1`·`09-3`·`09-4`만 다시 렌더(나머지 `skip`).
- 학생 묶음: `_build_index.py`로 `part3-practice.zip` 재생성 `e7f18258…` → **`c6dea7c1722e7f7b7cffb4dd2799aa6e083dc93927de1858c27782d077aac5a5`**(93파일·96항목, 07~13 노트북·도구 파일·새 12절 기록 세 개 포함). `check_delivery.py` **끝까지 통과**. 묶음을 `/tmp`에 풀어 `notebooks/`를 작업 폴더로 **10절을 새 커널로 실행(PYTHONPATH 없음) → PASS**, 셀 출력이 교재 B와 같고 `고른 경로:` 줄만 `../../../..`. `check_continuity.py`·`check_course_continuity.py`(결과 파일 쓰기를 막은 사본)는 Ch 12 블록·원본 기록 보존 검사를 지나 `llm-practice.zip` Stale에서 멈춤(전체 마감 몫).
- 서비스 요청: 임베딩 (16·16·16·16·21·31·3) × 2회 = 238번 + 묶음 확인 16번 = **254번**, 답을 쓰는 모델 (11절 10·12절 1·13절 2) × 2회 = **26번**, 로컬 리랭커 (17·30) × 2회 = 94번. 예상 비용 0.02달러 아래(문서 청크 175개가 한 번에 약 2만 조각).

### 챕터 안 변경

도구 파일(07~13 구역·`import math`·독스트링), 생성기 07~13, 노트북 07~13, `_src` 07~13, 빌드 HTML 01~13(07~13 내용 변경), `figures/09-1`·`09-3`·`09-4`(`.mmd`·`.svg`·`.png`·`.render.json`)·`09-1.caption.md`, 실습 폴더 `tests/test_continuity.py`(`tool_namespace()` — `load_notebook_function`·`load_notebook_namespace`가 도구 파일을 먼저 읽음, sklearn `cosine_similarity`·`TfidfVectorizer` import와 주입 제거, 주석 두 줄; 확인하는 성질 그대로), 실습 폴더 README 「01~06절」 → 「01~13절」, 12절 `runs/` 세 파일과 새 사본 폴더, `qa/public-files.json` note, `qa/upgrade/`(`gates-after-2-7.json`·`gates-wip-07~13.json`·`visual-after-2-7.json`·`before-2-7/runs/moved/`·`before-2-7/runs-sha256-after-B.txt`·`09-figures.md`·`10-figures.md` 메모·07~13 진단 메모), 챕터 요약·집필점검표·`qa/verification.md`.

### A가 남긴 「마감 때 고칠 줄」 처리

- `chapter-summary.md` 6·29·44·50·54·193행(과 그 주변 07·09·12 행, §4 해시 표, §8 흔들림 표, §15 판, §16 8번), `집필점검표.md` 검사 결과 13행·마감 게이트 행, `qa/verification.md` 13행, `upgrade-contracts.md` §3 81행(Ch14 줄)·§4 93행과 Ch12 줄 추가·§5 Ch12 줄 추가 — 모두 옛 문장·해시를 지우지 않고 「§2-7 리팩터로 바뀜 전 → 후」를 덧붙였습니다. 챕터 요약 끝에 §18(§2-7 요약)을 더했습니다.
- A 인계 8번(01·02 준비물 「강의와 실습 범위」 절 번호 어긋남, 리팩터 전부터): 01 「2~5절과 8·9절」 → **「2~5절과 7·8절」**·「10~12절은 함께 실행」 → **「6절과 9~12절은 함께 실행」**, 02 「2~4절과 7~9절」 → **「2~4절과 9~11절」**·「10~13절은 함께 실행」 → **「7·8절과 12~14절은 함께 실행」**. 생성기와 노트북 첫 마크다운 셀만 고치고(`mdsync.py`, 코드·출력 그대로, 다시 실행하지 않음) `run_section.sh … --no-exec`로 다시 빌드, 두 절 게이트 0·visual 4/4 PASS. 그래서 학생 묶음을 한 번 더 만들어 최종 해시가 `c6dea7c1…`입니다.

### Ch 13 작업자에게 넘길 것

1. **Ch 12 통합 기록 값은 그대로**입니다(`qid` `Q002`·`retrieved` `E01-P03-C02`·`E01-P03-C01`·`E01-P03-C06`·`reranker` `null`·`context_selection` `matched-chunk-text`·답 글자 같음). 바뀐 것은 해시·`run_id`(`advanced-continuity-20260921T082024-integrated-01`)뿐이라 Ch 13 07·08 노트북 출력과 본문은 다시 맞출 곳이 없습니다. Ch 13 `qa/upgrade/chapter-summary.md`·`review-round1.md`의 옛 해시(`ce76d3d8…`·`9b447a41…`·사본 `20260918T232052/`)만 「§2-7로 바뀜」으로 적으세요(옛 사본 폴더는 지우지 않았으므로 그 경로도 여전히 있음).
2. Ch 12 도구 파일에서 Ch 13이 가져갈 만한 함수: `parent_ids_of(found_chunk_ids, parent_by_chunk)`·`chunk_precision_at(…, parent_by_chunk)`·`rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, top_count)`·`rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, top_count)`·`unique_chunk_ids`·`kiwi_terms(kiwi, text, keep_tags)`·`fuse_rank(ranking_list, weight_list, rank_constant)`·`mmr_pick(…, vector_by_chunk)`. **Ch 13은 실습 폴더가 달라 Ch 12 `rag_tools.py`를 바로 가져올 수 없습니다** — Ch 13 도구 파일에 같은 본문으로 옮기고 「Ch 12 NN절에서 배웠습니다」 주석을 다세요(동명 `rank_by_distance`는 칸 `doc_id` 판이니 문서 청크에는 `rank_chunks_*` 판).
3. 12절 시험 기록의 `ndcg_at_5 < 1`은 여전히 `Q090` 한 줄입니다(Ch 15 01절 212행 기대 2와 어긋난 상태 그대로).
