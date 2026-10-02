# 03-임베딩과-벡터스토어 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 03, `figures/03-벡터-검색.svg`·`.excalidraw`). 챕터 전체 수정 전 게이트는 01절 작업 전에 남긴 `gates-before.json`(03절 G1 2·G2 0·G3 0·G4 0·G5 10·G6 19·G7 3 = 34).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 10 | 0 |
| G6 | 19 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 8 | 21(준비 3) |
| 검사한 문장 | 118 | 426 |

G8: `run_section.sh` 새 커널 PASS 두 번(같은 코드 `code_sha256` `09781533…90b1b3`). 1차 16:05:53 `outputs_sha256` `ab16b912…2866`, 2차 16:06:35 `8c3cd4d31ba7a480e17c6175749cc5f2d645556c31aebda63720117752be22e2`(교재 출력). 두 실행의 구조(요청 수, 순위와 출처, 저장 항목 키, 벡터 길이, 토큰 합계, Before `['7권']`·After `[]`)는 같았고, 서비스 임베딩 값이라 점수 소수 넷째 자리만 달랐음: 1차 표지 `0.5832`·k=8 4위 `0.3544`·7위 `0.322`·8위 `0.1541` → 2차 `0.5833`·`0.3553`·`0.3225`·`0.1542`. 결과 읽기·본문·캡션·그림 라벨은 2차 출력으로 `mdpatch.py`(재실행 없음)로 맞춤. 1차 값은 교재에 싣지 않음(규격 §4). `chapter.json`이 없어 `verify.py --chapter textbook/part3/ch09-rag-first-run`을 따로 실행 → `PASS 6 sections / 92 code cells (max 25 lines)`. 빌드 HTML `{{` 0건(7개 모두), `figure.mmd` 4·`figure.illustration` 1. `visual.cjs` 1280px·390px PASS(`/tmp/ch09-01/vis/vis.cjs` 사본 + `/tmp/ch09-03/html/`). 다른 절 HTML 해시: 03만 바뀜(01·02·04·05·06·index 작업 전과 같음, `SECTIONS` 제목 안 바꿈). 실습 폴더 테스트 작업 전 `10 passed` = 작업 뒤 `10 passed`. `runs/` 27개 파일 SHA-256 작업 전후 같음(읽기·쓰기 0). Ch 6·7·8 runs 사슬 파일도 읽지 않음.

## 수정 전 주요 문제

- G1: [14]·[16] 내포식 `[document.metadata["doc_id"] for document in …]`
- G5: 제목 셀·핵심 그림 없음, 결과 읽기가 출력 값을 인용하지 않음(7건), After 코드 뒤 설명 없음
- G6: 70자 초과 9(참고 자료 3 포함), 영문+조사 시작 8(「`similarity_search_with_score()`는」「k는」「`InMemoryVectorStore`의」 등), 5문장 넘는 단락 2
- G7: Mermaid 0(옛 Excalidraw `03-벡터-검색.svg` 하나), 삽화 0, 설계표 없음
- 사다리 밖 문법(게이트가 세지 않은 것): `{"D01", "D03"}.issubset(…)`(메서드 처음), try `except AssertionError`·`else`·`raise AssertionError`, `hits_k1[0][0]` 두 겹 인덱싱, `type(…).__name__`, `print` 인자에 영어 라벨(`doc_id:`·`score:`·`content:`)
- 이어짐: (1) 01·02절이 E01 5쪽·문서 청크 8개·`[E01 p.N]`으로 이어 왔는데 03만 합성 문장 D01~D03(도서관·해솔식당·별빛회사)이라 01 k=2·k=1 표지 결과, 02 `load_pdf_pages()`와 끊김. (2) 임베딩 객체 이름 `embedding`(01은 `embedding_model`). (3) 01 `from_documents()`와 03 `InMemoryVectorStore(embedding=…)`+`add_documents()`의 관계 설명 없음. (4) Ch 5 02절 `cosine_similarity()`를 「같은 계산을 적용」이라고만 적고 확인하지 않음. (5) 「청크」 단독 표기(규격 §4 결정 전), 「질문 임베딩(query embedding)」「저장 ID」 등 용어 6개가 01과 겹침. (6) b4 비유 「지도 위의 핀」이 01-5·02-5 카드·상자 비유와 이어지지 않음. (7) b7 「[[미정: 임베딩 모델]]」, 확인일 2026-09-07·08, 이번에 실행하지 않은 Ch 12 pgvector·Ch 14 폴백 설명. (8) meta 「코드 03-임베딩과-벡터스토어.ipynb」, 개선 전 모델 셀에 `reasoning_effort` 없음(03은 모델을 부르지 않아 해당 없음)

## 바꾼 것

- **형식·학습 질문 유지**: paired. 빈 벡터스토어 + `add_documents()` 저장 ID, `similarity_search_with_score()` (Document, 점수) 튜플, k 바꾸기, 두 근거가 필요한 질문의 k=1 Before → k를 늘린 After.
- **데이터 결정(D01~D03 → E01 문서 청크)**: 합성 문장 대신 01·02절과 같은 E01 5쪽·500/50 문서 청크 8개로 바꿈. 근거: 01 b7이 「표지와 2쪽 문서 청크의 코사인 유사도 차이는 0.01보다 작았다」고 탐색 값을 예고했고, 03이 같은 질문·같은 색인에서 그 점수를 출력으로 보여 줄 수 있음(`0.5833`·`0.5748`). 01 k=1 표지 결과를 k=8 전체 순위로 이어 볼 수 있음. 02 `load_pdf_pages()`·`count_tokens()`(`cl100k_base`)를 같은 코드로 이어 쓰고 넣을 토큰 수 합계 2885(02 4절 여덟 값의 합)로 색인 비용 어림(02 인계 「03에서 임베딩 토큰·비용을 숫자로」). Before/After 질문은 Ch 8 02 기록 두 개(E01 p.2 휴관·E01 p.3 대출 7권)를 합친 글, 검사는 Ch 8 03·07 지킬 말·`find_missing_words()`(02와 같은 코드).
- **임베딩 이름 결정**: 객체 `embedding_model`(01과 같음), 모델 이름 글 `embedding_model_name`(02와 같음). 개선 전 03 `embedding`은 쓰지 않음. 01은 코드·설명 모두 바꿀 필요 없음(01 코드가 이미 `embedding_model`). 04~06 개선 전 노트북은 `embedding`을 씀 → handoff §03 → §04에 기록.
- **Ch 5 02절 함수 이어 쓰기**: `dot_product()`·`vector_length()`·`cosine_similarity()`를 Ch 5 02 노트북 [15]·[20]·[22] 셀과 주석까지 같은 코드로(셀 하나에 함수 하나), `import math`. 벡터스토어 점수와 직접 계산 값을 `round(…, 4)`로 나란히 출력(두 실행 모두 같음). 튜플 나눠 담기 `for hit, score in …`는 Ch 5 02 [36] `for first_sentence, second_sentence in sentence_pairs` 모양으로 잇고, `round()`는 Ch 2 04.
- **새 API는 처음 자리에서 풀기**: `InMemoryVectorStore(embedding=…)`(빈 벡터스토어), `add_documents()`(한 요청, 저장 ID 목록 반환), 속성 `store`(01은 개수만 → 저장 ID를 키로 삼는 딕셔너리, 항목 키 `id`·`vector`·`text`·`metadata`), `similarity_search_with_score()`(튜플 목록, `<class 'tuple'>` 출력), 검색 결과 Document 속성 `id`, `embedding_model.model`. 새 함수 `make_source_mark(chunk)`(01 f-string 세 줄을 함수로, 본문 4줄).
- **설치판 소스로 확인해 본문에 쓴 것**: langchain-core 1.6.2 `InMemoryVectorStore.__init__`(`self.store = {}`), `add_documents`(`embed_documents(texts)` 한 번, `doc.id` 없으면 `uuid.uuid4()`, 항목 네 키), `similarity_search_with_score` = `embed_query(query)` + `_similarity_search_with_score_by_vector`(numpy `_cosine_similarity`, `argsort()[::-1][:k]`, `Document(id=…)` 반환), simsimd 없으면 numpy(실습 가상환경에 simsimd 없음, numpy 2.5.3), `from_documents` → `from_texts` → `cls(embedding=…)` + `add_texts` → `add_documents`, `dump()`·`load()` 있음(실행 안 함). langchain-openai 1.6.0 `embed_query` = `embed_documents([text])[0]`, `_get_len_safe_embeddings`가 `chunk_size` 1000·토큰 한도 안에서 한 번 `client.create`(문서 청크 8개 = 요청 1번). OpenAI Embeddings 안내(2026-09-17 WebFetch): 기본 1536, `dimensions`, 「normalized to length 1」(본문 b7에 「이번에 확인하지 않음」으로). 모델 안내: 100만 토큰당 0.02달러(2026-09-17 WebFetch, 01과 같은 값).
- **탐색 뒤 정한 값(규격 §3, 노트북 After 설명 한 문장 + 본문 b7에 공개)**: `/tmp/ch09-03/probe1.py`·`probe2.py`(임베딩 요청 13번: 넣기 2, 질문 임베딩 2, 문서 청크 다시 임베딩 1, k=8 검색 8). 질문 7개(휴관일, 휴관+권수, 휴관+주차, 권수+주차, 요일+며칠, 휴관+연장, 휴관+권수+며칠)를 k=8로 검색. 휴관+권수 질문은 1위 2쪽(`월요일`)·2위 표지·3위 3쪽(`7권`) → k=1 `['7권']` 빠짐, k=3에서 처음 모두 들어옴 → 이 질문과 k=3을 흐름을 보여 주는 예로 고름. 휴관+연장 질문은 1위 표지(k=1이면 두 말 모두 빠짐, 01 표지 결과와 겹쳐 고르지 않음), 권수+주차 질문은 `7권` 문서 청크가 5위(b7에 한 문장). 같은 질문 벡터를 두 번 받으면 값이 같았고(최대 차 0.0), 2쪽 첫 문서 청크를 따로 다시 임베딩하면 최대 차 0.000458 → 점수를 `assert`하지 않고 b7 「실행마다 소수 넷째 자리가 달라질 수 있음」, After `assert`는 결과 개수 `len(after_hits) == 3`만.
- **요청 수**: 서비스 요청 6번(모두 `text-embedding-3-small`: 넣기 1, k=2 점수 검색 1, `embed_query` 1, k=8 1, Before k=1 1, After k=3 1), 답 모델 0번(개선 전 03도 0번). 비용 어림: 넣기 2885토큰 + 질문 5번 → 100만 토큰당 0.02달러로 약 0.00006달러, 준비물은 「0.001달러 미만」. 새 커널 두 번 + 탐색 13번 = 임베딩 요청 25번.
- **키 셀 처리(02와 맞춤)**: 02는 키·모델 없음, 03은 임베딩 때문에 키만 필요 → `nbkit.KEY` 준비 셀 하나(01 설명 문장 「01절과 같은 셀로」), 모델 셀은 두지 않음(`key_and_model_cells()` 안 씀). 실행일 문장 「이 노트북의 출력은 2026-09-17에 이 임베딩 모델로 실행한 결과입니다」는 임베딩 객체 셀 결과 읽기에 한 번(규격 §3). 준비물 구조(데이터·요청 수·비용·요금 확인일·강의와 실습 범위·기준 버전·Linux만 실행)는 01·02와 같음.
- **기본 경로**: 설치(버전 7줄) → import(`math`·`os`·`PdfReader`·`Document`·스플리터·`tiktoken`·`OpenAIEmbeddings`·`InMemoryVectorStore`) → 키 → 2절 경로 / `load_pdf_pages` 정의 / 500·50 문서 청크 → 3절 임베딩 객체·규칙 / `count_tokens` 정의 / 토큰 합계·비용 어림 / 빈 벡터스토어·`add_documents` / 저장 항목 열기 → 4절 `make_source_mark` 정의 / k=2 점수 검색 → 5절 `dot_product` / `vector_length` / `cosine_similarity` / 질문 벡터·직접 계산 비교 → 6절 k=8 순위 → Before `find_missing_words` 정의 / 두 가지 질문 k=1 → After k=3·`assert` → 정리
- **쓰지 않은 것**: 내포식·`issubset`·try·`raise`·조건 표현식·`lambda`·`+=`·`join`·`Path`·`enumerate`·`zip`·`sum`·`max`·`@`·`BaseModel`·타입힌트·반복문 안 요청(요청은 반복문 밖, 반복문은 받은 결과만 출력)·서비스 값 `assert`·f-string 안 계산(출처 표시 f-string은 변수만). 새로 쓴 모양: 튜플 목록을 `for a, b in` 두 이름으로(Ch 5 02 모양), 딕셔너리 `keys()` 출력, 목록 원소 자료형 `type(scored_hits[0])`, 반복문 안 순위 카운터 `rank = rank + 1`(01 `page_number` 모양), 아주 작은 수 `round(…, 7)`와 `e-05` 표기 한 문장.
- **함수 본문 줄 수 직접 셈**(규격 §2-2 L2): `load_pdf_pages` 9, `count_tokens` 2, `make_source_mark` 4, `dot_product` 4, `vector_length` 2, `cosine_similarity` 3, `find_missing_words` 5. 주석 제외 셀당 코드 줄 3~13(13 = 01·02와 같은 경로 셀).
- **용어**: 한정어 없는 「청크」 0건(노트북·본문·그림·캡션·alt). 새 용어 3개(저장 항목, 저장 ID, 검색 점수) = meta 「새 용어 3」. 01 용어(벡터스토어·임베딩·top-k 검색·문서 청크)와 Ch 5 코사인 유사도·Ch 8 지킬 말은 「같은 뜻」 한 문장으로 이음. 「조각」 0건. 개선 전 「질문 임베딩(query embedding)」은 용어 표에 두지 않고 그림 라벨 「질문 임베딩」으로만.
- **meta 시수**: 「강의 1h | 실습 2h」 유지(01~06 합 강의 6h·실습 10h = `render_index()` 16h). 코드 표기 「Jupyter Notebook」(01·02와 같음).
- **그림**: Mermaid 4장(03-1 넣기와 점수 검색·03-2 코사인 유사도 계산·03-3 k8 점수 xychart·03-4 Before-After, PNG 직접 확인, viewBox 848·466·700·797) + 삽화 03-5 메모지와 막대 카드 1장(2회 생성, 1차 job `dd269c29-…` 탈락, 2차 job `3b5bed77-5d5c-463a-ae1d-08819a1d1b44` 채택, 4크레딧, 잔액 2826 → 2822). 옛 `03-벡터-검색.svg/.excalidraw`는 지우지 않고 본문에서 쓰지 않음(정리 대상).
- **본문**: 10블록 모두 다시 씀. b2 01 순서만 본 결과·02 토큰 수·담긴 모양과 점수, b3 표(Ch 2 04·Ch 5 02·Ch 8 01·Ch 8 03·07·Ch 9 01·02) + 이름 결정 한 문장, b4 비유·삽화·그림 읽기·도식 03-1·용어 표, b5 토큰 수·저장 항목·점수와 코사인 유사도(03-2)·k=8(03-3), b6 Before/After 해석(03-4, 빨강 1상자, 공통 값 회색 상자, 개수 2는 실행 안 함, Ch 8 01 입력 가용분), b7 탐색 뒤 정한 값·점수 변동·절대 기준 없음(Ch 11)·길이 1 벡터(확인 안 함)·`dimensions`·`ids`·`dump`/`load`·simsimd·같은 모델(Ch 10 07)·요금·기준 버전, b8 04절 연결, b9 복습 5문제, b10 참고 자료 3건(확인 2026-09-17). 제작 이력 문장 없음(규격 §4).

## 검토

- 스스로 확인: 결과 읽기·본문·캡션·그림 라벨의 숫자와 인용을 두 번째 새 커널 출력과 대조(G5·G7 0). 1차와 달라진 네 값은 `mdpatch.py` 치환 뒤 `grep`으로 0.5832·0.1541·0.3544 잔존 0 확인(탐색·1차 값 인용 없음). 조사 「0.5833과」로 고침. 그림 방향 말(03-1·03-4 「위 칸·아래 칸, 칸마다 왼쪽에서 오른쪽」, 03-2 「위에서 아래로」, 03-3 가로축·세로축), 색 이름(xychart 주황 막대)을 PNG와 대조. 03-4 결과 상자에 두 조건 공통 값(같은 질문, 1위 `[E01 p.2] | 498 | 0.6257`)을 넣지 않음(규격 §5-3). 03-1 보라 = 실행한 임베딩 모델(01-2와 같은 색). 빨강은 03-4 Before 한 상자.
- 문장 확인(게이트 밖): 「4쪽 문서 청크에 「휴관」이 없다」는 탐색 스크립트 낱말 검사로 확인. 「2쪽 첫 문서 청크에 이용 시간 글이 있다」는 02 출력(끝 두 줄 표 머리)으로 확인. 「개수 2로는 3쪽 문서 청크가 들어오지 않는다」는 k=3 출력 순서와 1.6.2 `argsort()[::-1][:k]`로 추론한 것이라 「그 검색은 이번에 실행하지 않았습니다」를 붙임.
- 삽화 검수(저장 파일 기준, `figures/03-5-메모지와-막대-카드.prompt.md`): 메모지와 올라온 두 카드가 같은 산 모양, 앞줄 카드는 모양이 모두 다름, 초록 스티커가 모든 카드에. 약점(메모지 막대 6개·카드 5개, 앞줄 두 겹, 상자가 책상 위)은 그림 읽기에 적음. 저장 PNG ↔ 채택 job 결과 픽셀 차이 0.
- 별도 세션 검토: 아직(메인 세션 차례)

## 남은 것

- 뒤 절 작업자에게: `qa/upgrade/handoff.md` §03 → §04
- 정리 대상(삭제 승인 필요, 목록만): `figures/03-벡터-검색.svg`·`.excalidraw`(옛 도식), `qa/upgrade/gates-wip-03.json`, 기기 `/tmp/ch09-03`(probe·삽화 원본·html 사본·해시)
- 챕터 마감 때: `_src/index.html` 03 행(「짧은 Document 세 건, 실제 임베딩, InMemoryVectorStore, k 변경」·「벡터 검색 도식」)과 새 용어 줄(「질문 임베딩」·「청크」)을 절 본문과 대조(규격 §7-2). 개선 전 QA `qa/check_content.py` 20·30행(`ex03_preserved.txt`·`ex03_failure_preserved.txt`)·`qa/test_notebook_migration.py` 9행은 개선 전 노트북 기준(실행하지 않음). `runs/examples/ex03_*_preserved.txt`는 개선 전 D01~D03 예제 출력(읽지도 바꾸지도 않음)
- 강사 확인 후보: 두 가지 질문·k=3(탐색 뒤 정한 예), 새 함수 `make_source_mark()`를 04 이후에서 이어 쓸지

## 검토 반영 (2026-09-17, 챕터 마감 세션)

별도 세션 검토 1차 A(§01~04)·B(§05~07)를 받아 반영했습니다. 보고서와 반영 내역 전체는 `review-round1-A.md`·`review-round1-B.md` 끝 「반영 결과」, 챕터 차원 정리는 `chapter-summary.md`입니다. **이 절 노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 반영 뒤 게이트 `--label after --strict` 7/7 PASS(G1~G7 0), `verify.py --chapter` `PASS 7 sections / 175 code cells`, `visual.cjs` 16건 PASS, 실습 폴더 테스트 10 passed, 빌드 HTML `{{` 0건.

- **판정 accept**(상 0·중 0·하 1). 03-1 반영: `figures/03-2-코사인-유사도-계산.mmd` 결과 상자 라벨을 출력 줄과 같은 순서 「벡터스토어 점수 | 직접 계산」으로, `figures/03-1-넣기와-점수-검색.mmd` 보라 상자를 「임베딩 모델<br>질문 1개<br>숫자 1536개」로 바꿨습니다. 캡션·alt·도식 읽기·설계표 색 열도 같이 고쳤고, mmd를 고쳐 자동으로 다시 렌더한 뒤 PNG를 직접 확인했습니다(viewBox 852.7·466.3, 렌더 도장은 지우지 않음).
- 결정 요청 네 가지(합성 문서 D01~D03 제거 / 임베딩 이름 두 개 / 직접 계산과 점수 일치를 `assert`로 검사하지 않음 / 「개수 2로는 3쪽이 안 들어온다」 추론)는 권고대로 **모두 유지**했습니다(A Q3). 「개수 2」 추론은 `similarity_search_with_score`가 전체 순위를 매긴 뒤 앞 k개를 자른다는 설치판 소스로 뒷받침됩니다.
- C-5 반영으로 b5와 노트북 준비물에 「2절은 01·02절과 같은 코드라 강의에서 빠르게 확인합니다.」를 더했습니다(**강사 확인 대상**).
