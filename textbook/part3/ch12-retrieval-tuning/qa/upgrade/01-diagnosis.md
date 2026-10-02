# Ch 12 01절 「벡터 거리와 정확 검색」 품질 개선 기록

작업 2026-09-18. 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`.
앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1·2), 같은 Part 앞 챕터 `textbook/part3/ch09-rag-first-run/qa/upgrade/chapter-summary.md`·`textbook/part3/ch10-document-processing/qa/upgrade/chapter-summary.md`·`textbook/part3/ch11-evaluation/qa/upgrade/chapter-summary.md`.
**이 챕터 첫 절**이라 수정 전 게이트를 챕터 전체로 먼저 남겼습니다(`gates-before.json`, 덮어쓰지 않음).

## 1. 게이트 전후

| 게이트 | 수정 전(01절) | 수정 후(01절) |
|---|---|---|
| G1 문법 사다리 | 9 | 0 |
| G2 셀 모양 | 7 | 0 |
| G3 주석 | 6 | 0 |
| G4 실제 모델 | 0 | 0 |
| G5 노트북 설명 | 9 | 0 |
| G6 문장 | 8 | 0 |
| G7 그림 | 3 | 0 |
| 합계 | **42** | **0 (PASS)** |

- 챕터 전체 수정 전 합계(`gates-before.json`, 12절): G1 131 · G2 66 · G3 79 · G4 0 · G5 108 · G6 137 · G7 36 = **557**, 통과 절 0/12.
- 코드 셀 7 → **31**(준비 셀 5 포함), 검사 문장 82 → **291**, 주석·빈 줄 뺀 셀 최대 줄 수 **11**(규격 §2-4 권장 3~12 안), 함수 본문은 모두 **10줄 이하**(직접 셈: 4·2·3·2·5·7·7·5·6·6·4·10줄, 가장 긴 것은 `score_one` 10줄).
- G8: 새 커널 실행 PASS(`fresh_kernel: true`, Python 3.12.13). **같은 코드로 새 커널 두 번 실행해 `code_sha256` `727b3bdf75a8c253…`·`outputs_sha256` `ef039ce7b877e036…`가 같았습니다.** 교재 출력은 마지막 실행(`executed_at` 2026-09-18T14:19:30Z). `verify.py --chapter` **PASS 12 sections / 105 code cells (max 25 lines)**(`max 25`는 아직 개선 전인 12절 셀), `visual.cjs` 1280px·390px **2건 PASS**(small·contrast·clipped·svgBounds·horizontal 모두 0), 빌드 HTML 13개에 `{{` 잔존 **0건**.
- 서비스 요청 **임베딩 9번**(문서 1 + 질문 8, `text-embedding-3-small`). 보낸 글은 문서 712자 + 질문 155자로 900자 아래이고 예상 비용은 0.01달러 아래입니다. 답을 쓰는 모델은 이 절에서 부르지 않았습니다.

## 2. 수정 전 주요 문제

- **G1 9건**: 내포식 7곳·제너레이터 식 2곳. `[f"{doc['title']} {doc['text']}" for doc in docs]`, `[embedder.embed_query(q["question"]) for q in queries]`, `[(docs[i]["doc_id"], round(float(scores[i]), 4)) for i in order]`, 경로 찾기 `next((folder for folder in [Path.cwd(), *Path.cwd().parents] if ...), None)`가 그 자리입니다.
- **G2 7건**: 15줄 초과 셀 1개(준비 셀 18줄), 두 겹 함수 호출 2곳(`round(float(...), 4)`), 한 글자 변수 `q`, 한 글자 인자 `k`, 세미콜론과 한 줄 복합문 각 1곳(`runs = chapter_dir / "runs"; history = runs / "core-history"`, `if not backup.exists(): backup.write_bytes(old)`).
- **G3 6건**: 코드 셀 여섯 개에 첫 줄 주석이 없었습니다.
- **G5 9건**: 제목 셀과 「오늘 볼 그림」 첨부가 없었고, 코드 셀 네 개의 뒤 설명 셀이 출력 값을 인용하지 않았으며, 준비 셀 앞과 마지막 셀 뒤에는 설명 셀이 아예 없었습니다.
- **G6 8건**: 70자 초과 5문장, 영문 용어로 시작해 조사가 바로 붙는 문장 2개(「`text-embedding-3-small`을 …」·「C02의 정답 …」), `<dl class="term">` 정의 다섯 개가 한 단락으로 세어져 단락 5문장 초과 1건.
- **G7 3건**: Mermaid 0장(옛 Excalidraw SVG 1장만), 삽화 0장, 설계표 없음.
- **그 밖에 고친 것**: `numpy`를 기본 경로에서 씀(`np.array`·`np.argsort`·`np.linalg.norm`·`@` 행렬 곱). numpy는 Part 1~3에서 가르친 적이 없습니다(Ch 11 요약 §12). 한 셀에서 거리 계산·정렬·자르기를 한꺼번에 했고, 함수 `exact_rank(query_vector, metric="cosine", k=3)`이 `if`로 두 자를 갈라 본문 9줄이었습니다.

## 3. 데이터 결정 — core 벌을 그대로 씀

이 챕터 `labs/part3/ch12-retrieval-tuning/data/`에는 두 벌이 있습니다.

| 파일 | 내용 | 쓰는 절 |
|---|---|---|
| `core-documents.json` | 교육용 문서 12개(`doc_id`·`category`·`title`·`text`, `LIB-001`~`ACC-004`, 글자 수 합 712) | 01·02·04·05·06 |
| `core-queries.json` | 질문 8개(`qid`·`question`·`gold_doc_id`·`kind`, `C01`~`C08`, 글자 수 합 155) | 01·02·04·05·06 |
| `advanced-documents.json` | 부모 문서 6건(`E01`·`E02`·`H01`·`H02`·`M01`·`M02`)과 문서 청크 175개(`chunk_id` `E01-P01-C01` 모양) | 07~12 |
| `advanced-queries.json` | 질문 30개 | 07~12 |

- **`advanced-queries.json`은 Ch 11 평가셋과 파싱 결과가 완전히 같습니다**(30줄, 칸 7개 `qid`·`tier`·`question`·`type`·`gold_doc_ids`·`answerable`·`split`, 개발 15 · 시험 15). `textbook/part3/qa/check_continuity.py` 44~46행·`textbook/qa/check_course_continuity.py` 78~80행·실습 폴더 `tests/test_continuity.py`가 두 파일이 같은지 검사합니다 → **한 글자도 고치지 않습니다.**
- **01절은 core 벌을 씁니다.** 까닭 세 가지.
  1. 02절이 같은 문서 12개 벡터를 pgvector `CREATE TABLE ch12_core_hnsw (… embedding vector(256))`에 넣고 정확 검색과 HNSW 결과를 대조합니다. 01절만 자료를 바꾸면 01 → 02 대조가 끊어지고 01~06절 여섯 절을 함께 바꿔야 합니다.
  2. 이 절의 학습 대상은 지표 값이 아니라 거리 계산과 정렬 방향입니다. 문서 12개는 「모두 재었다」를 손으로 셀 수 있습니다.
  3. Ch 11 요약 §2·§11-3이 「후보 단위·중복 제거 순서·자르는 자리·질문 묶음이 같을 때만 값을 견주라」고 했습니다. core 벌은 말뭉치와 질문이 달라 Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과 나란히 놓지 않는다는 문장을 b7에 적었습니다.
- **개발 15문항 / 시험 15문항 약속**(Ch 11 요약 §11-1): 이 절은 평가셋을 읽지 않아 시험 분할을 보지 않습니다. 평가셋을 처음 쓰는 절은 07절이고, 그 약속은 그때 지킨다고 b7에 적었습니다.
- Ch 11 함수 네 개를 인자 모양 그대로 이어 쓰려고 `gold_doc_id`(글 하나)를 `[query["gold_doc_id"]]`로 감싸 목록으로 넘깁니다. 두 칸 이름이 다른 사실을 노트북 2절 결과 읽기에 적었습니다.

## 4. 차원 수 결정 — 256을 그대로 둠

- 개선 전 01 노트북은 `OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)`이었고 **그대로 두었습니다.**
- 이 챕터가 256으로 이어집니다: 02절 `vector(256)` 표, 05·06·12절 노트북도 `dimensions=256`입니다.
- **계약**: `textbook/qa/check_course_continuity.py` 219행과 실습 폴더 `tests/test_continuity.py`가 12절 기록 `advanced-continuity-integrated-result.json`의 `settings.dimensions == 256`을 검사합니다.
- Ch 10 07절 결정(색인에 넣을 벡터는 기본 설정 = 숫자 1536개, 256은 비교용)과 값이 다릅니다. 그래서 b7에 「Ch 10 08절 색인은 인자 없이 1536이었으므로 두 색인의 점수를 나란히 놓지 않습니다」를 적었습니다.

## 5. 파일 쓰기 결정 — 이 절은 파일을 쓰지 않음

- 개선 전 마지막 셀은 `runs/core-01-exact.json`을 덮어쓰고 `runs/core-history/`에 보존본을 남겼습니다. `Path`·`hashlib`·`datetime`·세미콜론·한 줄 복합문을 쓰고 이 절 주제와 무관합니다.
- **읽는 쪽을 모두 확인했습니다.** 이 파일의 키를 읽는 코드는 없습니다. `textbook/qa/check_course_continuity.py` 187~196행만 바이트를 봅니다: 정본이 `before-manifest.json` 해시와 다르면 `runs/core-history/before-*-core-01-exact.json`에 원본 바이트가 남아 있어야 합니다.
- 그래서 **파일을 쓰지 않는 쪽을 골랐습니다**(Ch 9 07·Ch 10 09·Ch 11 07 선례). `runs/core-01-exact.json`은 2026-09-09 바이트 `f8e81361e9c79fa5…c758` 그대로이고 `before-f8e81361e9c7-core-01-exact.json`과 바이트가 같습니다. 검사의 「바뀌지 않은 기록」 갈래로 지나갑니다.
- `runs/` 36개 파일 묶음 해시는 작업 전후 `a9c5d35a40a8acc0ac9455eae8682bc7cacadfc66682f1087c81f739abc3c8f6`로 같고, 오늘 바뀐 파일이 없습니다(`find … -newermt` 0건).
- **02절 작업자 주의**: 02~06절 개선에서 `runs/core-0N-*.json`을 다시 쓰려면 `core-history/before-*-` 보존본이 원본 바이트를 가진 채로 남아 있어야 합니다. 쓰지 않는 쪽이 가장 안전합니다.

## 6. 바꾼 것

- **노트북**(`qa/upgrade/author_01.py`가 씀, 코드 셀 31개, experiment 형식 유지)
  - 준비 다섯 셀: 설치(`langchain-openai==1.6.1`·`python-dotenv==1.2.3`) → import(`json`·`math`·`OpenAIEmbeddings`) → 키 확인(`nbkit.KEY`) → 후보 경로 `for`+`break` → 문서·질문 읽기.
  - **numpy를 없앴습니다.** 점곱·벡터 길이·코사인 유사도를 **Ch 9 03절 함수 세 개와 같은 코드**로 정의하고(`dot_product`·`vector_length`·`cosine_similarity`), `cosine_distance`·`l2_distance`를 새로 만들었습니다.
  - **코사인 거리를 새로 가르칩니다**(유사도를 가장 큰 값 1에서 뺀 값). 02절 pgvector `<=>` 연산자가 내는 값과 같아 01 → 02 연결이 됩니다.
  - 정확 검색을 두 함수로 나눴습니다: `measure_all(question_vector, distance_name)`(문서 12개 모두와 재기)과 `rank_by_distance(id_list, distance_list)`(`sorted(목록)`으로 작은 거리부터). `np.argsort` 대신 튜플 목록을 `sorted`로 정렬합니다(Ch 10 01절에서 배운 `sorted(목록)`).
  - **Ch 11 함수 네 개를 같은 코드로 이어 씁니다**: `unique_doc_ids`(01절)·`find_gold_rank`(01절)·`recall_at`(02절)·`mean_score`(02절). 후보 한 개가 문서 한 개라 중복 제거가 목록을 바꾸지 않는 것을 출력으로 보이고, Ch 11에서는 후보가 쪽이라 목록이 줄었다는 문장을 붙였습니다.
  - 실행 1(코사인 거리) → 실행 2(자만 L2 거리)로 값 하나만 바꿉니다. 그다음 질문 여덟 개 × 두 자 = 기록 16줄을 담아 표와 질문 평균을 냅니다. **반복문 안에서는 담기만 하고 끝난 뒤 한꺼번에 출력합니다**(Part 2 §3 규칙).
  - **거리는 소수 둘째 자리까지만 출력합니다.** 탐색 실행 두 번에서 같은 글을 보내도 임베딩 값이 조금 달라져 소수 셋째 자리가 흔들렸습니다(§8).
  - 파일을 쓰는 마지막 두 셀을 없앴습니다(§5).
- **본문**(`_src/01-벡터-거리와-정확-검색.html`, 10블록 모두 다시 씀)
  - b3에 Ch 5 02절·Ch 9 03절·Ch 10 07절·Ch 11을 잇는 두 단락을 적었습니다.
  - b4: 비유 단락 + 삽화 + 「그림 읽기」, 용어 표 다섯 개(**L2 거리·코사인 거리·정확 검색·근사 검색·단위 길이 벡터**), 도식 두 장. 정의를 `<dl class="term">`에서 **용어 표**로 바꿨습니다(Ch 11 handoff의 G6 단락 주의).
  - b6에 xychart 한 장과 「이 값은 두 자 가운데 어느 쪽이 나은지 가르지 못합니다」를 적었습니다.
  - b7 일곱 항목: 정렬 방향, 모델·차원 수가 다른 벡터, **256 고정 근거와 Ch 10 1536과 나란히 놓지 않기**, **거리 값이 흔들려 라벨에 넣지 않은 것**, **Ch 11 15문항 값과 나란히 놓지 않기**, **개발·시험 분할 약속은 07절부터**, 자리 12까지 넓히면 재현율 1.0이 되는 천장.
  - b10 참고 자료를 `<li><div><a>원제목</a></div>설명 · 확인일</li>`로 나눴습니다(Ch 5 03-6 선례).
- **그림**: 설계표 `qa/upgrade/01-figures.md` → Mermaid 4장 + 삽화 1장. 옛 도식 `figures/01-정확-검색.svg`·`.excalidraw`·`.caption.md`는 지우지 않고 `qa/upgrade/before/figures/`에 사본을 두었습니다.
- **옛 생성기 두 개에 실행을 막는 줄을 넣었습니다**(규격 §8, PLAYBOOK §2-1, 삭제 아님): `figures/_gen_figures.py`와 `qa/advanced_author.py`. 둘 다 첫머리에 설명 주석과 `raise SystemExit(...)`을 두었고 실제로 실행해 멈추는 것을 확인했습니다(종료 코드 1). 챕터 마감 때 `qa/upgrade/before/generators/`로 옮깁니다. 두 파일은 `before-manifest.json`에 등록돼 있지만 두 검사 스크립트가 해시를 보는 항목은 `labs/**/runs/**`뿐입니다(두 스크립트를 실제로 돌려 확인).

## 7. 검사와 대조

- 게이트 `--label after --section 01 --strict` **PASS**(`gates-after-01.json`).
- `verify.py --chapter` `PASS 12 sections / 105 code cells (max 25 lines)`. 빌드한 HTML 13개에 `{{` 잔존 0건이고 **다시 빌드해도 13개 해시가 같습니다**(빌드가 되풀이해도 같은 결과).
- **빌드가 12절 HTML을 모두 다시 썼습니다.** 2026-09-09 `before-manifest.json` 해시와 달라졌는데, `full-course-before.tar.gz` 사본과 비교하면 차이는 **2026-09-14에 고친 `_src`·노트북 내용**(「두 검색기가 같은 입력을 보는 방식」 절, 경로 찾기 셀, 실행 결과 보존 셀)이고 이번 작업에서 만든 변경이 아닙니다. 02~12절 `_src`와 노트북은 이번에 고치지 않았습니다.
- 실습 폴더 테스트 `uv run --project labs/part3/ch12-retrieval-tuning --with pytest==8.4.2 python -m pytest labs/part3/ch12-retrieval-tuning/tests -q` → **4 passed**. 이 테스트는 08·10·12절 노트북과 `data/`·`runs/`만 읽고 01절 노트북은 보지 않으므로 작업 전후 결과가 같습니다.
- `textbook/part3/qa/check_continuity.py` → 154행 `Stale archive: part2-practice.zip/…`에서 멈춥니다. `textbook/qa/check_course_continuity.py` → 212행 `Stale archive: part1-practice.zip/…`에서 멈춥니다. **두 자리 모두 Ch 11 마감과 같은 자리이고 전체 마감 몫입니다.** 그 앞의 기록 계약 블록(ch09·ch10 기록, ch12 실험 36건, 평가셋 동일성, `%pip`·`uv.lock` 대조, core 별칭·보존본 대조)은 모두 지나갑니다.
- `textbook/part3/qa/check_delivery.py` → **끝까지 통과**(Ch 11 마감과 같음).
- **학생 묶음**: 01절이 읽는 두 파일은 `textbook/part3/public-files.json` 4·5행에 이미 있고 `part3-practice.zip`(91개 항목)에도 들어 있습니다. **허용 목록을 고치지 않았습니다.** 묶음을 `/tmp`에 풀어 **세 자리**(묶음 맨 위·실습 폴더 맨 위·`notebooks`)에서 경로 셀과 자료 읽기 셀을 돌려 모두 `문서 수: 12`·`질문 수: 8`을 확인했습니다.
- **`%pip` 셀과 잠금**(규격 §7-2, Ch 11 검토 C-1): 설치 목록 `langchain-openai==1.6.1`·`python-dotenv==1.2.3`이 `labs/part3/ch12-retrieval-tuning/uv.lock`에 그 버전으로 있고 dev 그룹에 `pip==26.2`·`ipykernel==7.3.0`이 이미 있습니다. `pyproject.toml`·`uv.lock`을 고치지 않았습니다. `check_course_continuity.py` 43행이 지나갑니다.
- **챕터 밖에 바뀐 파일은 세 개뿐입니다**: 진행표 `textbook/qa/upgrade-progress.md`(기록, PLAYBOOK §7)와 검사 스크립트가 늘 다시 쓰는 결과 파일 두 개 — `textbook/part3/qa/delivery-results.json`(`check_delivery.py` 실행 결과)·`textbook/_notebook/checks/notebook-contracts-part3-ch12-retrieval-tuning.json`(`verify.py --chapter`가 쓰는 계약 파일). 묶음 허용 목록·`public-files.json`·`build_bundle.py`·`_build_index.py`·`finalize_continuity_evidence.py`·공용 도구는 고치지 않았습니다.
- **그림 대조**: Mermaid PNG 4장을 직접 열어 상자 색과 붙은 자리를 확인했습니다. `01-2`는 칸을 넘는 화살표 때문에 칸 안 `direction`이 무시되어 **두 칸이 위아래가 아니라 나란히** 그려졌습니다 → alt와 「도식 읽기」의 방향 말을 「왼쪽 칸·오른쪽 칸」으로 고쳤습니다(PLAYBOOK §4). `01-4` 막대가 두 자에서 같은 값이라 한 계열로만 그렸고 그 사실을 「도식 읽기」에 적었습니다. viewBox 폭은 373·547·458·700으로 모두 868 아래입니다.
- **삽화**: 2차 job 채택, 저장 PNG(1100 × 614)를 채택 job 결과에서 같은 폭으로 줄인 그림과 픽셀 대조해 차이가 없고(`ImageChops.difference` 범위 `None`) 1차 탈락본과는 다름을 확인했습니다(규격 §5-4). 상태·job id·크레딧은 `figures/01-5-쪽지와-열두-권.prompt.md`.

## 8. 탐색 실행과 흔들리는 값

- 탐색 실행은 `/tmp/ch12-01/probe.py`를 두 번 돌렸습니다(2026-09-18). 문서 12개·질문 8개·벡터 숫자 256개·문서 벡터 길이 열두 개 모두 소수 둘째 자리에서 `1.0`.
- **흔들린 값**: 첫 질문과 `LIB-001`의 코사인 거리가 `0.5582`와 `0.5583`, L2 거리가 `1.0564`와 `1.0566`, 둘째 질문과 `LIB-003`의 코사인 거리가 `0.5581`과 `0.5599`였습니다. 같은 글을 보내도 임베딩 값이 조금 달라집니다.
- **흔들리지 않은 값**: 두 자의 가까운 순서, 정답 자리(`C01` 2·`C02` 7·나머지 1), 질문 평균 재현율(자리 1 `0.75`·자리 2 `0.875`·자리 3 `0.875`).
- 그래서 거리는 소수 둘째 자리까지만 출력하고 **그림 라벨에는 거리 값을 넣지 않았습니다**(Ch 11 요약 §3과 같은 처리). 본문 b7에도 적었습니다.
- 노트북 본문 실행에서는 **같은 코드로 새 커널 두 번 실행해 `outputs_sha256`이 같았습니다.** 소수 둘째 자리까지 자르면 같은 값이 나옵니다.

## 9. 강사 확인 대상

- **core 벌을 쓰기로 한 결정**(§3). 01~06절이 교육용 문서 12개를 쓰고 07~12절이 평가셋 30문항을 씁니다. Ch 11 값과 견주는 자리는 07절 이후입니다.
- **차원 수 256**(§4). Ch 10 07절의 「색인은 기본 1536」 결정과 값이 다르고, 12절 기록 계약이 256을 요구합니다.
- **파일을 쓰지 않기로 한 결정**(§5). 개선 전 01절이 남긴 `runs/core-01-exact.json`은 2026-09-09 바이트로 남습니다.
- **절 meta 시수 합이 챕터 시수와 맞지 않습니다**(규격 §7-2). 12절 meta 실습 시수 합은 2+3+3+3+2+3+1+1+1+1+1+1 = **22h**인데 `chapter.json`은 「총 40h · 강의 12h · 실습 28h」입니다(강의는 1h × 12 = 12h로 맞습니다). **개선 전부터 6h 어긋나 있었고 01절만 고쳐서는 맞출 수 없어 그대로 두었습니다.** 챕터 마감 때 절별 실습 시수를 다시 나누거나 `chapter.json`을 고쳐야 합니다.
- **자르는 자리 1·2·3**: 문서가 12개라 Ch 11의 자리 5·50을 쓸 수 없어 정한 값입니다. 자리 12까지 넓히면 재현율이 1.0이 되는 천장을 b7에 적었습니다.
- **강의와 실습 범위 문장**: 노트북 준비물의 「강의 시간에는 2~5절과 8·9절을 읽습니다」와 「6·7절 정의 셀은 Ch 9 03절에서 쓴 코드라 실행만 하고 넘어갑니다」는 작업자가 정한 배분입니다.
- **임베딩 요청 9번**: 질문을 하나씩 보내 여덟 번입니다. 한 번에 보내면 요청이 두 번으로 줄지만 질문 임베딩과 문서 임베딩을 갈라 보여 주는 설명이 사라집니다.

## 10. 남은 것

- 02절: pgvector 실행 방법과 인계는 `qa/upgrade/handoff.md` `## §01 → §02`.
- **다시 실행하면 함께 고칠 것**(지금은 재실행 금지 아님, 다만 값 대조가 필요): 없음. 코드 주석·설명에 틀린 곳을 찾지 못했습니다.
- **삽화를 다시 만들 때**: 뒤쪽 아홉 권이 조금 작게 그려져 「아홉 권」을 세기 어렵습니다. 다시 만들면 책 크기를 고르게 해 열두 권을 셀 수 있게 하세요.
- **정리 대상**(삭제하지 않고 목록만, 삭제 승인 필요): 옛 도식 `figures/01-정확-검색.svg`·`.excalidraw`·`.caption.md`, `figures/_gen_figures.py`·`qa/advanced_author.py`(마감 때 `qa/upgrade/before/generators/`로), `qa/upgrade/gates-wip-01.json`, `.cache/vm/shot/ch12-01/`(검수용 화면 캡처 여섯 장), 기기 `/tmp/ch12-01`·`/tmp/ch12-vis`, 챕터·실습 폴더 `__pycache__`·`.pytest_cache`, `.cache/vm/venv-ch12-retrieval-tuning`(전체 마감 때).

## 검토 반영 (2026-09-19, 챕터 마감)

- **01-1(중) 노트북 절 번호** — b6 「노트북 12절에서」 → 「노트북 5절 「두 가지 자 만들기」에서」. 두 자의 관계를 내는 셀은 노트북 5절입니다.
- **01-2(하) 「네 칸」** — 「정답 자리와 자르는 자리 세 개, 네 칸이 모두 같았습니다」로 풀었습니다.
- **C-7(하) 실습 시수 6h 어긋남** — **해소**입니다. 07·08·09절이 실습 1h → 3h로 올려 절 meta 합이 강의 12h·실습 28h가 되었고 `chapter.json`과 정확히 맞습니다. 강사 확인 목록에는 「07·08·09절 배분이 맞는지」만 남깁니다.
- **결정 요청 네 항목**(core 벌 · `dimensions=256` · 파일 미기록 · 자르는 자리 1·2·3) — 검토 권고대로 **모두 유지**했습니다.
- 노트북 재실행 없음: `code_sha256` `727b3bdf75a8c253`·`outputs_sha256` `ef039ce7b877e036`·`executed_at` 2026-09-18T14:19:30Z가 반영 전후 같고, 다시 계산한 값도 같습니다.

## §2-7 챕터 마감 (2026-09-21, 작업자 B)

- 준비물 「강의와 실습 범위」의 절 번호를 소절 번호에 맞춤 — 「2~5절과 8·9절」 → 「2~5절과 7·8절」, 「10~12절은 함께 실행」 → 「6절과 9~12절은 함께 실행」(A 인계 8번, 리팩터 전부터 있던 어긋남). 마크다운 한 셀만 고치고 다시 실행하지 않음.
