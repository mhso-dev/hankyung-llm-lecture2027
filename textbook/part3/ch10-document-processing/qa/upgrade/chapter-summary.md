# Ch 10 문서 처리 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-18(품질 개선 8절 + 실습 절 09 + 별도 세션 검토 1차 A·B 반영 뒤). **Part 3 두 번째 챕터**입니다. 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6. 앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1·2), 바로 앞 챕터 `part3/ch09-rag-first-run/qa/upgrade/chapter-summary.md`. 절 사이 인계 원문: `qa/upgrade/handoff.md`(절마다 「새로 가르친 것」「이어 쓸 이름과 값」「출력 라벨」「아직 안 가르친 것」 전체 목록). 검토: `qa/upgrade/review-round1-A.md`(§01~05)·`review-round1-B.md`(§06~09), 각 끝에 「반영 결과」. 절별 반영 상세는 각 `qa/upgrade/NN-diagnosis.md` 「검토 반영」 절.

**Ch 11 작업자는 과정 요약(Part 1·2) + Ch 09 요약 + 이 파일만 읽고 시작할 수 있게 썼습니다.** 세부 값·라벨이 필요하면 handoff를 찾아봅니다.

절: 01 문서와 메타데이터 · 02 PDF와 표·OCR · 03 DOCX·HTML·CSV 로더 · 04 HWP와 HWPX · 05 문자·재귀·토큰 청킹 · 06 구조와 시맨틱 청킹 · 07 한국어 임베딩과 캐시 · 08 인덱싱 비교 실험 · 09 문서 처리 실습: 형식이 다른 문서를 한 색인에 모아 찾기. 형식 01~07 paired, 08·09 experiment. **답을 쓰는 모델은 이 챕터에서 한 번도 부르지 않았습니다.** 임베딩만 `text-embedding-3-small` 하나. 코드 셀 215개(18·18·23·24·24·26·23·29·30), 게이트 **9/9**(G1~G7 0, 수정 전 8절 합계 363 = G1 22·G2 9·G3 16·G4 0·G5 86·G6 206·G7 24), 검사 문장 306·328·405·442·418·458·430·491·451, Mermaid 35장(4×8 + 3)·삽화 9장(대기 없음), 모든 노트북 새 커널 실행 PASS(실행일 모두 2026-09-18 — **검토 반영에서 다시 실행한 절은 없음**). 서비스 요청 01~05 **0번** · 06 2 · 07 6 · 08 13 · 09 4번(절마다 0.01달러 미만).

이 챕터는 `chapter.json`이 없고 자체 `_build.py`를 씁니다. `run_section.sh`가 verify를 건너뛰므로 **`verify.py --chapter`를 따로 실행합니다**(`PASS 9 sections / 215 code cells (max 14 lines)`). 빌드 뒤 HTML 10개에 `{{` 잔존이 0건인지도 따로 봅니다.

## 1. 새로 가르친 개념·기법·함수·용어 (노트북에서 실행한 것만)

| 절 | 새 API·값 | 직접 만든 함수(노트북 셀, 실습 폴더 모듈 아님) | 용어 표 |
|---|---|---|---|
| 01 | `os.listdir()`·`sorted(목록)`, `from pathlib import Path`·`Path(글).name`·`stem`·`suffix`, `type(객체).__name__`, `extract_text(extraction_mode="layout")`, `딕셔너리.keys()` | `load_pdf_pages(pdf_path, doc_id)`(Ch 9 코드), `make_source_record(file_path, page, parser)`, `make_source_mark(chunk)`(Ch 9 코드) | 출처 기록(다섯 칸), 파서(parser), 파일 형식, 출처 계보, 문서 청크(Ch 9 뜻 그대로) |
| 02 | `pdfplumber.open()`·`extract_text(layout=True)`·`extract_tables()` | `make_cell_text()`, `make_row_text()`, `count_page_lengths()`, `find_ocr_candidates()` | 글자 층, 표 읽기(table extraction), 글자 인식(OCR), OCR 후보 쪽, 값이 없는 칸 |
| 03 | `from docx import Document as DocxDocument`·`paragraphs`·`style.name`·`tables`, `BeautifulSoup`·`find_all()`·`get_text(" ", strip=True)`, `csv.DictReader`·`newline=""`·`encoding="utf-8-sig"` | `read_row_values()`, `pick_tag_texts()`, `make_unit_record()`, `make_unit_mark()` | 꾸밈 이름(style), 태그, **자리 칸**(CSV `row`, 2부터), 네 칸 기록(쪽 없는 형식) |
| 04 | `open(..., "rb")`·`read(8)`·`hex()`, `zipfile.is_zipfile`·`ZipFile`·`namelist()`·`read()`, `xml.etree.ElementTree.fromstring`·`root.iter()`, `try/except zipfile.BadZipFile as error` | `read_head_hex()`, `make_local_name()`, `read_body_text()`, `make_section_mark()`, `recognize_file_kind()`, `read_hwpx_body()` | 형식 표시(file signature), 압축 묶음, 본문 XML, 자리 칸 `section`(1부터), HWP 후보 |
| 05 | `CharacterTextSplitter(separator=, chunk_size=, chunk_overlap=)`·`split_text()`, `RecursiveCharacterTextSplitter(separators=, keep_separator="end")`·`split_documents()`, `tiktoken.get_encoding()`, `RecursiveCharacterTextSplitter.from_tiktoken_encoder()` | `make_length_list()`, `count_tokens()`(Ch 9 코드), `make_token_list()`, `find_missing_words()`(Ch 8 코드), `find_chunks_with_words()`, `find_over_limit()` | 문자 방식·재귀 방식·토큰 방식, **조각 수 한도**, 입력 가용분(Ch 8 뜻), 조각 세기 |
| 06 | `MarkdownHeaderTextSplitter(headers_to_split_on=)`·`split_text()`·`chunk.metadata["heading"]`, `SemanticChunker(embedding_model, breakpoint_threshold_amount=)`·`split_documents()`, 딕셔너리 `copy()` | `mark_heading_line()`, `make_markdown_text()`, `make_text_list()`, `make_heading_record()` | 구조 방식·시맨틱 방식, 제목 표시, **제목 칸 `heading`**, 끊는 기준값(백분위수) |
| 07 | `OpenAIEmbeddings(model=)`·`embed_documents()`·`dimensions=256`·속성 `model`·`dimensions`, `tempfile.mkdtemp()`, `LocalFileStore`, `CacheBackedEmbeddings.from_bytes_store(namespace=, key_encoder="sha256")` | `make_size_list()` | 차원 수(dimensions), **벡터 캐시**, 가르는 이름(namespace), 저장 이름표(가르는 이름 28자 + sha256 64자 = 92자) |
| 08 | `InMemoryVectorStore(embedding=)`·`add_documents()`·`similarity_search_with_score(질문, k=)`(Ch 9 03절 모양을 이 챕터에서 처음), `with open(..., encoding="utf-8")`, `str(숫자).zfill(4)`, `time.strftime("%Y%m%dT%H%M%S")`, `os.makedirs(..., exist_ok=True)`, `hashlib.sha256(바이트).hexdigest()`(Ch 7 08 코드), `json.dumps(..., ensure_ascii=False)`·`json.loads()`, `글.splitlines()` | `name_chunks()`, `run_setting()`, `make_doc_id_list()`, `print_result_rows()`, `make_retrieved_list()`, `make_record()` | 실험 격자, 같게 유지할 조건, 기록 줄 수(logged candidates), 결과를 확인한 자료 범위 |
| 09 | 새 API 0개 | 같은 코드 8개(`load_pdf_pages`·`make_source_record`·`make_source_mark`·`make_unit_record`·`make_unit_mark`·`make_local_name`·`read_body_text`·`make_section_mark`) + 새 3개 `pick_mark()`·`run_index()`(조립)·`print_hit_rows()` | 새 용어 0개 |

- **Python 쪽(215셀)**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`raise`·`+=`·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`next`·`isinstance`·`join`·`set`·`sorted(key=)`·f-string 안 계산·타입힌트·`@`·`BaseModel`·`Path.cwd()`·`parents`·`glob`·`deepcopy`·모델 답·임베딩 값 `assert`가 **0건**(검토 A·B AST). 호출한 내장 이름은 `len`·`print`·`type`·`range`·`round`·`str`·`open`·`sorted`(01절만). `try`는 04절 Before 한 곳, `with`는 02·03·04·08·09절 파일·라이브러리 객체 자리뿐이고 모두 처음 쓰는 자리에 설명이 있습니다. 함수 본문은 모두 10줄 이하(규격 §2-2)이고 주석·빈 줄 뺀 셀 최대 줄 수는 10~13줄입니다.
- **결론 태도(Ch 11도 지킬 것)**: 한 번 본 결과는 「이번 실행에서는」, 실행하지 않은 동작은 「이번에 실행하지 않았습니다」, 설치판 소스로만 확인한 동작은 출력 근거와 갈라 적기(07절 캐시), 두 조건 공통 값은 맨 아래 회색 상자로, 점수는 실행마다 소수 아래 자리가 달라져 라벨·결론에 넣지 않기(08절은 **1·2위까지만** 결론), 탐색 뒤 정한 값은 b7에 과정과 「흐름을 보여 주려고 정한 예」.

## 2. 반복해 쓴 데이터·함수·이름·비유

- **경로**: `candidates = [".", "../../..", "../../../.."]` + `for`·`break`(01~09절 같은 코드), `root_path`(교재 출력 `.`), `corpus_path`(= `root_path + "/labs/data/rag-corpus"`), `manifest_path`, `pdf_path`(= `corpus_path + "/pdf/easy/E01.pdf"`), `fixtures_path`.
- **데이터**: `labs/data/rag-corpus/pdf/easy/E01.pdf`(미르시립도서관 이용 안내, 5쪽 — 쪽 글자 수 `45·905·925·871·270`, 2쪽 26줄). **2쪽 905자가 01·02·05·06·07절의 나눌 글**입니다. 08절만 디지털 PDF 18건 93쪽(총 62,512자, 쪽 평균 672.2자). **`pdf/hard/H05.pdf`는 스캔본 폴더가 아닌데 세 쪽 모두 0자**라 글을 얻은 문서는 **17건**입니다(01 b2·08절 「글이 있는 문서 수: 17」). 견본은 `fixtures/`의 `sample.docx`·`sample.html`·`sample.csv`·`legacy-signature.hwp`·`minimal-marker.hwpx` 다섯 개.
- **나누기 값**: `separator_order = ["\n\n", ". ", "\n", " ", ""]`. 05절 목표 200자 — 문자 방식 6개 `[156, 156, 184, 172, 152, 80]`, 재귀 방식 6개 `[185, 147, 86, 164, 130, 188]`, 토큰 방식 목표 100조각 13개. 06절 구조 방식 3개 `[223, 470, 182]`·시맨틱 방식 기준값 95에서 2개 `[233, 671]`. 08절 목표 400자 여섯 설정 `[212, 232, 228, 245, 220, 235]`. 09절 재귀 200자로 PDF 6개 / 세 형식 8개.
- **임베딩·검색**: `embedding_model_name = "text-embedding-3-small"`, `embedding_model`(차원 수 인자 없음 = 숫자 1536개), `search_count = 5`, `chunk_target = 400`, `overlap_values = [0, 100]`. 조각 세기는 `encoding`(규칙 `cl100k_base`)과 `count_tokens(text)`. 2쪽 글 조각 수 869, 말뭉치 전체 59,238. 요금 `embedding_rate = 0.02`·`tokens_per_million = 1000000`.
- **질문·지킬 말**: 08·09절이 읽는 평가셋 Q001 「미르시립도서관의 정기 휴관일은 언제인가요?」·정답 문서 ID `['E01']`(평가셋 파일과 **글자까지 같아야 함**). 05·06절 `closure_words = ["정기 휴관일", "화요일에도 휴관"]`(Ch 9 05절 정답 출처와 같은 휴관 안내에서 고름). 09절 질문은 「제주로 보내는 배송은 며칠이 더 걸리나요?」.
- **출력 라벨(대표)**: 「Document 수:」「2쪽 본문 글자 수:」「출처 기록:」「메타데이터 칸 수:」「출처 표시:」「찾은 표의 수:」「첫 표의 행 수:」「머리글 행:」「기준값(글자 수):」「문단 꾸밈 이름:」「칸 이름:」「앞 여덟 바이트:」「압축 묶음인가:」「본문 XML 수:」「문서 청크 수:」「문서 청크별 문자 수:」「문서 청크별 조각 수:」「조각 수 한도:」「한도를 넘은 문서 청크 번호:」「표시를 붙인 뒤 글자 수:」「끊는 기준값:」「벡터의 숫자 개수:」「저장 파일 수:」「설정별 문서 청크 수:」「상위 다섯 줄의 문서 이름:」「기록 줄 수:」「첫 줄의 검색 항목 수:」(절마다 전체 목록은 handoff).
- **비유와 삽화**: 01-5 서류와 봉투(봉투 = 출처 기록) → 02-5 칸막이 상자(칸 = 표의 칸) → 03-5 공책·이름표 상자·장부 + 같은 봉투 세 개 → 04-5 잠긴 상자와 주머니 + 봉투 한 개와 빈 꼬리표(= 자리 칸) → 05-5 세 줄로 자른 띠(도막) → 06-5 문패와 무늬 → 07-5 서랍과 표찰 → 08-5 상자 세 개와 기록 용지 → 09-4 세 묶음과 한 상자. **Ch 9 계열(카드 상자 = 색인, 흰 카드 = 문서 청크, 노란 쪽지 = 질문)을 09-4가 그대로 씁니다.**
- **쓰지 않은 말**: 한정어 없는 **「청크」**(반드시 「문서 청크」), **「청킹」**(본문 0건 — 절 제목·파일 이름에만 남음, §12), **「조각」을 도막 뜻으로**(「조각」은 Ch 5 토큰 전용. 스플리터가 끊어 낸 단위는 「스플리터가 끊어 낸 단위」, 비유는 「도막」), 「열」(→ **칸**), 「오버랩」(→ 겹침), 「임계값」·「중단점」(→ **끊는 기준값**), 「텍스트 레이어」(→ **글자 층**. 08절이 말뭉치 목록을 인용할 때만 원문 그대로 쓰고 바로 뒤에 02절 말을 붙임), 「행 사전」(→ 딕셔너리), 「캐시」 단독(→ **벡터 캐시**), 「색인 이름표」는 Ch 9 뜻 전용(08절은 이름을 만들지 않고 `config` 칸에 설정을 그대로 적음).

## 3. 기록 칸 계약 (형식마다 다른 자리 칸 — Ch 11·12가 이어 읽음)

| 형식 | 기록 칸 | 출처 표시 함수 | 표시 보기 |
|---|---|---|---|
| PDF(쪽 있음) | 다섯 칸 `doc_id`·`source`·`file_type`·`parser`·**`page`** | `make_source_mark()`(01·02·05·06·09) | `[E01 p.2]` |
| DOCX·HTML(쪽 없음) | 네 칸(`page` **없음**) | `make_unit_mark()`(03·04·09) | `[sample docx]` |
| CSV | 네 칸 + 자리 칸 **`row`**(첫 줄이 칸 이름 줄이라 **2부터**) | `make_unit_mark()` | `[sample csv row.2]` |
| HWPX | 네 칸 + 자리 칸 **`section`**(**1부터**, `parser`는 `zip-xml`) | `make_section_mark()`(04·09) | `[minimal-marker hwpx section.1]` |
| 제목으로 나눈 문서 청크 | 위 칸 + **`heading`**(04절 자리 칸 `section`과 뜻이 달라 이름을 가름) | 쪽이 있으면 `make_source_mark()` | `[E01 p.2]` |

- **함수를 고치지 않고 새 이름으로 더하는 방식**을 이 챕터가 세 번 썼습니다(`make_unit_mark` → `make_section_mark` → `pick_mark`). 앞 절 출력이 바뀌지 않는 것을 출력으로 확인했습니다.
- 09절 `pick_mark()`가 **`page` → `section` → `row`** 순서로 보고 표시를 고릅니다. 실습 폴더 모듈 `_with_chunk_metadata()`도 같은 순서입니다(소스 204행). 「제목을 `section`에 담으면 안 되는 까닭」은 06 b4·b7에 있습니다.

## 4. runs 산출 파일 계약 (Ch 11이 읽음 — 꼭 먼저 읽을 것)

**08절만 쓰는 파일 두 갈래**: 정본 `labs/part3/ch10-document-processing/runs/continuity-ch10-indexing.jsonl`(여섯 줄)과 같은 바이트 사본 `runs/continuity/20260918T061902-ch10-01.jsonl` ~ `-06.jsonl`. 사본 폴더는 48개(2026-09-09 24개 + 2026-09-18 24개), **앞 사본은 지우지 않습니다**(`check_course_continuity.py` 184행이 옛 정본의 줄마다 그 이름을 찾습니다). `runs/` 전체는 64개입니다.

| 항목 | 값 |
|---|---|
| 정본 SHA-256 | **`58cc790c45df9bf9cfbdda21a4de267bd10a7749568f1306d9625657d5ebda45`**(옛 정본 `9e59586a…`) → **§2-7 리팩터로 `0984e1679db1d16afbb37b3b98e4846a0b6629a0a486a917e9d4a0aaa7e69188`**(2026-09-21, `source_run_id` `20260921T062600-ch10-01`~`-06`, 계약·순위·`chunk_id`·지표 같음, §16). `runs/` 64개 묶음 해시 `2a73b21a073dfc9f76b606393abd85a0b94f409174cfdf8e6014737f45cdf84e` |
| 줄 수 | **6**(설정 여섯 개). `finalize_continuity_evidence.py` 51행 `assert len(source_ids) == 7`(ch09 1 + ch10 6) |
| 최상위 키 **7개** | `qid`·`question`·`gold_doc_ids`·`source_chapter`(`ch10`)·`source_run_id`·`config`·`retrieved`. **Ch 9와 달리 `answer` 칸이 없습니다**(이 챕터는 답을 쓰지 않음) |
| `config` 키 **6개** | `chunk_method`(`char`·`recursive`·`token`)·`split_config`·`embedding`·**`dimensions`(1536)**·`k`(**5**)·`inputs`. `inputs`는 `corpus_scope`(`"디지털 PDF 18건"`)·`corpus_manifest_sha256`(`27541f41…`)·`evaluation_dataset_sha256`(`9544b332…`). `dimensions`가 256에서 1536으로 바뀐 까닭은 07절이 「색인에 넣을 벡터는 기본 설정으로」라고 정했기 때문이고, **이 칸을 읽는 쪽은 없습니다**(`check_course_continuity.py` 219행은 Ch 12 기록을 봅니다) |
| `retrieved` 항목 키 **5개** | `doc_id`·`chunk_id`·`page`·`rank`·`score`. 항목은 실행마다 5개, `rank` 1부터 빈틈없이, `page` 1 이상. `score`는 `evaluate.py` 178행이 필수로 봅니다 |
| `chunk_id` 모양 | **`ch10:char:0000`**(`"ch10:" + method + str(number).zfill(4)`, **네 자리 채움**). Ch 9는 `ch09:6f9f83db90:0`입니다. 읽는 쪽 세 곳 모두 **빈 값인지만** 보므로 깨지지 않지만, 두 챕터 기록을 나란히 보는 **Ch 11 06절 화면에서는 모양이 섞여 보입니다**(검토 B R-2 — Ch 11 작업자가 판단) |
| 라벨 | `question`·`gold_doc_ids`는 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl` Q001과 글자까지 같아야 하고, 08 노트북이 그 파일에서 읽어 옵니다. **라벨을 `config` 안에 넣지 않습니다** |
| 지표 제약 | `finalize_continuity_evidence.py` 54~58행이 ch10 실행마다 `recall_at_5 == 1`·`precision_at_5 == .2`·`ndcg_at_5 == 1`·`recall_at_logged_candidates == 1`·`recall_at_50 is None`을 봅니다. `evaluate.py`의 `dedupe_docs()` 때문에 **정답 문서 E01이 겹침 없는 상위 목록의 첫 자리**여야 하고 상위 5건에 정답 문서가 하나만 있어야 합니다. 여섯 실행 모두 확인했습니다 |

**읽는 쪽 목록**(여섯 곳, 08절 작업과 검토 B가 모두 열어 확인): `labs/part3/ch11-evaluation/evaluate.py` 176~200·205~250행 · `textbook/part3/qa/check_continuity.py` 58~78·140~155행 · `textbook/qa/check_course_continuity.py` 94~112·172~198행 · `textbook/part3/qa/run_continuity_bundle.py` 45~54행 · `textbook/part3/qa/finalize_continuity_evidence.py` 15·37·44~58행 · Ch 11 06 노트북(줄 수만).

**고치지 않는 파일과 해시**: `document_processing.py` `37ca2cc9cf18…`, `experiment.py` `342e85b048…`, `tests/`·`fixtures/`(수정 시각 2026-09-08), Ch 11 평가셋 `9544b332…`, `labs/data/rag-corpus/` 전체, Ch 9 기록 `294713765a…`, Ch 6·7·8 비용 사슬(`f18920c6…`·`a8aaafb7…`·`125fc147…`). **검토 반영 전후 모두 같습니다.**

**이 파일을 다시 쓸 때**: (a) 위 읽는 쪽을 먼저 확인하고, (b) 08 본문·그림의 인용 값(문서 청크 수 여섯 개·1·2위·조각 390970·`0.0078194`달러)을 새 출력으로 모두 맞추고, (c) 앞 사본은 지우지 말고 그대로 두고, (d) 위 표와 진행표를 새로 적습니다. **08 재실행은 기본적으로 금지**입니다(Ch 11 입력이 바뀌고 3~5위 순서가 실행마다 달라집니다).

## 5. 09 실습 절 주제와 결과

- 「09 · 문서 처리 실습: 형식이 다른 문서를 한 색인에 모아 찾기」(30분, 따로 과제 없음, 강사와 함께 실행). 파일·slug `09-문서-처리-실습`, 형식 experiment, meta 「실습 30분 · 새 용어 0」. 새 API·새 문법 **0개**.
- 조립: 형식별 읽기(01·03·04) → 형식별 기록(01·03·04) → 표시 함수 고르기 `pick_mark()` → 재귀 방식 200자(05) → 색인·검색(08) → 점검표 `print_hit_rows()`. 조립 함수는 `run_index(index_documents, index_splitter)` 하나입니다. 바꾸는 값 하나 = **색인에 넣는 문서 묶음**.
- 결과(2026-09-18 06:57): 실행 1(PDF 한 건, 문서 청크 6개) 상위 다섯 줄 모두 `[E01 p.2]`·1위 147자 점수 `0.33`. 실행 2(세 형식, 문서 청크 8개) 1위 `[sample docx]` 26자 점수 `0.63`, PDF 문서 청크 네 개가 한 칸씩 내려감. **HWPX 문서 청크는 두 실행 모두 상위 다섯 줄에 없음**(몇 위였는지는 확인하지 않음 — 다섯 줄만 받음).
- 결론: 「색인에 넣는 문서 묶음을 바꾸면 같은 질문의 1위가 다른 형식 문서로 바뀔 수 있다」, 「출처 표시가 있으면 1위가 어느 파일에서 왔는지 바로 읽는다」까지. 어느 묶음이 좋은지는 정하지 않습니다(질문 하나·색인 두 벌·색인마다 한 번 검색).
- **시수**: 09 실습 30분은 `render_index()`의 「24h · 강의 8h · 실습 16h」에 더하지 않고 실습 16h 안(규격 §7-2). 01~08 meta 합(강의 8h·실습 16h)은 그대로. `_src/index.html` 절 표 09행은 「30분(실습 16h 안)」.
- 09은 **파일을 쓰지 않습니다**(`runs/` 64개 해시·모듈 두 개 해시가 전후 같음).

## 6. 다음 챕터가 이어받을 것

- **Ch 11 평가 기초**(6절, 아직 개선 전): `labs/part3/ch11-evaluation/evaluate.py`가 **Ch 9 06절 기록 한 줄과 Ch 10 08절 기록 여섯 줄을 함께 읽습니다**(§4의 필수 키·k 제약). Ch 9는 k=2라 @5 지표가 `None`이고 Ch 10은 k=5라 `recall_at_5 1.0`·`precision_at_5 0.2`·`ndcg_at_5 1.0`이 나옵니다. **이 차이가 Ch 11 06절이 가르칠 자리입니다.**
  - **꼭 고쳐야 할 어긋남(검토 B C-3)**: `textbook/part3/ch11-evaluation/_src/01-질의셋과-정답-문서-ID.html` b3이 「Ch 10의 08절 연결 실습은 공개 디지털 PDF 18건에 **세 청킹 방법과 두 임베딩 모델**을 적용하고」라고 적었습니다. 개선된 08절은 **임베딩 모델 하나** + 나누기 방식 세 가지 × 겹침 두 값입니다. Ch 11 개선 때 이 문장을 고치세요. 같은 챕터 06절 b3·b5의 「Ch 10의 후보 5개로는 @5 지표를 계산할 수 있지만 Recall@50은 측정하지 않습니다」는 맞습니다.
  - 이 챕터는 **지표를 계산하지 않았습니다.** 「정답 문서가 몇 번째에 있었는지만 눈으로 읽었다」까지입니다. **쪽 단위 정답 출처(Ch 9 05)와 문서 단위 정답 문서 ID(Ch 9 06)의 차이**를 08 b5·노트북 [48]이 「1위가 E01 1쪽 표지 글인데도 정답 문서」라는 결과로 이었습니다 — Ch 11이 이 구분을 이어받습니다.
  - `chunk_id` 모양이 두 챕터에서 다릅니다(§4). Ch 11 06절이 두 기록을 나란히 보이면 그 사실을 한 문장으로 적으세요.
  - 용어: 문서 청크·색인·벡터스토어·검색 점수·정답 문서 ID·기록 줄 수·실행 기록 한 줄을 Ch 9·Ch 10 뜻 그대로. 「청킹」·한정어 없는 「청크」·「오버랩」·「임계값」·「텍스트 레이어」·「열」은 쓰지 않습니다.
- **Ch 12 검색 품질과 튜닝**(12절, 아직 개선 전): 이 챕터가 만든 문서 청크·색인 설정을 전제로 검색·병합·재정렬을 다룹니다. Ch 12 `advanced-continuity-integrated-result.json`의 `settings.dimensions == 256` 검사(`check_course_continuity.py` 219행)는 **Ch 12 자기 기록**이라 ch10의 1536과 무관합니다. **Ch 9 01·03절의 「점수 = 코사인 유사도」는 `InMemoryVectorStore` 기준**이라 다른 벡터스토어로 옮기면 그대로 이어 쓰지 마세요(Ch 9 요약 §5, 08 b4 마지막 단락이 같은 주의를 적었습니다).
- Ch 10이 「이번에 실행하지 않았다」고 적은 것: 글자 인식(OCR) 실행, 두 단 레이아웃과 읽기 순서, 선 없는 표·병합 셀, 본문 XML이 여러 개인 HWPX, 상용 파서, 표 읽기 결과를 문서 청크로 쓰기, 다른 임베딩 모델 비교, 차원 수를 준 색인, 여러 질문 평균.

## 7. 아직 가르치지 않은 것 (Ch 11이 설명 없이 전제하면 안 되는 것)

Ch 9 요약 §6 전체에 더해, Ch 10에서도 하지 않은 것:

- **검색·색인**: 다른 임베딩 모델, 차원 수를 준 색인, 점수 기준값·거르기·MMR, 색인 파일 저장과 다시 불러오기, `as_retriever()`, `similarity_search_with_score_by_vector`, `ids` 직접 지정, 문서·질문 앞머리 글, 질문 쪽 벡터 저장, 여러 질문을 한 번에 돌려 평균 내기, 같은 조건 반복 요청, 검색 지표 계산, 다른 벡터스토어.
- **생성**: 답을 쓰는 모델 호출(`init_chat_model` 0건 — **이 챕터에 `langchain` 메인 패키지가 없어 import 여부를 확인하지 않았습니다**), 근거를 넣은 메시지 목록, 출처 인용 검사, 답 정확성 판정.
- **문서**: OCR 실행, 읽기 순서, 선 없는 표·병합 셀, 본문 XML 여러 개, 암호가 걸린 문서, HWP 전용 도구, 상용 파서, 시맨틱 방식 기준값 0.
- **Python**: §1 「쓰지 않은 Python」 목록 전부, 실습 폴더 모듈 `import`, `set` 메서드, `deepcopy`, 딕셔너리 `|`, `**딕셔너리` 풀어 넘기기.

## 8. 실습 묶음·절 수 스크립트 상태

- **허용 목록을 고치지 않았습니다.** 01~09절이 읽는 입력은 `labs/data/rag-corpus/pdf/*/*.pdf`·`manifest.json`, `fixtures/` 다섯 개, `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`이고 모두 `textbook/_notebook/build_bundle.py`(`data`·`FIXTURES`)와 `textbook/part3/public-files.json`에 이미 있습니다. 절마다 `part3-practice.zip`을 풀어 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 경로 셀을 돌려 확인했습니다.
- **`part3-practice.zip`(83개 항목)에는 06~08 노트북이 개선 전 판이고 09 노트북이 아직 없습니다.** Ch 9가 더한 `labs/data/rag-corpus/queries.jsonl`도 아직 없습니다 → 전체 마감 때 재생성(§9).
- `textbook/part3/_build_index.py` `CHAPTERS`의 ch10 절 수 칸을 **8 → 9**로 올렸고(강의 8h·실습 16h는 그대로), 챕터 밖 수정으로 ch10 설명 문장도 고쳤습니다(§10).
- `textbook/part3/qa/finalize_continuity_evidence.py` 15행 `assert len(visual)`을 **88 → 92**로 고쳤고, **2026-09-18 Ch 11 마감에서 94로 다시 올렸습니다**(ch11이 실습 절 07로 14 → 16행, 공용 `visual.cjs` 재실행 16/16 PASS). 목표 합은 ch08 14 + ch09 16 + ch10 20 + ch11 16 + ch12 26 + part3 2 = **94**이고 **2026-09-18 기준 실제 합은 92**입니다(ch09만 아직 14) — ch09 HTML을 공용 `visual.cjs`로 다시 찍으면 94가 됩니다. **92나 90으로 내리지 마세요**(ch10 20행·ch11 16행을 버립니다). Ch 9 요약 §9 4단계에도 같은 경고를 적었습니다.

## 9. 전체 마감 순서 (이 순서를 지켜야 검증이 끝까지 갑니다 — Ch 9 요약 §9와 합친 판)

1. `textbook/downloads/part3-practice.zip`·`llm-practice.zip`(필요하면 `part4-practice.zip`) 재생성 — Ch 9 §7 허용 목록 수정과 Ch 10 09절 노트북이 들어가야 합니다.
2. `textbook/part3/qa/run_continuity_bundle.py`를 **`--reuse-upstream` 없이** 실행(옛 `temporary_extraction` 폴더가 없어 재사용 경로는 쓸 수 없습니다). 이 스크립트가 묶음에서 **Ch 9 06 · Ch 10 08 · Ch 11 06 노트북을 실제로 돌립니다.**
3. 공용 `visual.cjs`로 **ch09 HTML 8개를 다시 찍어 `textbook/_notebook/checks/ch09-rag-first-run/visual-results.json`을 14행 → 16행**으로 갱신(Ch 9 챕터 폴더의 `qa/visual-results.json`도 같이). ch10은 이미 20행·20/20 PASS, ch11도 Ch 11 마감에서 16행·16/16 PASS로 갱신했습니다.
4. `textbook/part3/qa/finalize_continuity_evidence.py` 실행 — 15행은 **이미 94**입니다(Ch 11 마감에서 92 → 94, 고치지 마세요). 37행 `assert not any(execution_input(name) for name in changed)`은 2번을 먼저 끝내야 통과합니다. **2026-09-19 Ch 12 마감 갱신**: ch12가 실습 절 13을 붙여 26 → **28행**이 되었습니다. 그래서 지금 실제 합은 **94**(ch09 14 + ch08 14 + ch10 20 + ch11 16 + ch12 28 + part3 2)이고, 이 94는 **ch09의 -2와 ch12의 +2가 상쇄된 값**입니다. 기대값은 **94 그대로** 두었습니다. ch09 8쪽을 다시 찍어 16행이 되면 합이 **96**이 되므로, 그때 15행을 96으로 올리고 실행하세요.
5. `textbook/part3/qa/check_continuity.py`·`textbook/qa/check_course_continuity.py`를 끝까지 실행. **2026-09-18 기준 각각 154행·212행 zip 신선도에서 멈춥니다**(`part2-practice.zip`·`part1-practice.zip`). 기록 계약 블록은 모두 지나갑니다. `check_course_continuity.py`는 `tomllib`이 필요해 Python 3.11 이상으로 돌립니다(`uv run --project labs/part3/ch10-document-processing python …`).
6. Part 3 목차 `textbook/part3/_build_index.py` 재생성(ch09 7절·ch10 9절 표시), `textbook/qa/upgrade-progress.md`와 과정 요약 Part 3 절은 Part 3 마지막 챕터(Ch 12) 뒤.

## 10. 챕터 밖 수정

- **`labs/part3/continuity-guide.md` 10행**(학생 묶음 포함, 검토 B C-2): 08절에 없어진 「작은 원문의 여섯 조합을 관찰한 뒤」 단계를 빼고 「같은 18개 PDF와 Q001에 나누기 방식 세 가지와 겹침 두 값을 곱한 설정 여섯 개를 적용해 검색 결과를 … 저장합니다」로 고쳤습니다.
- **`textbook/part3/ch09-rag-first-run/qa/upgrade/chapter-summary.md` §9 4단계**(검토 B R-1): 「`assert len(visual) == 88`을 90으로」가 Ch 10이 고친 92와 어긋나 마감 작업자가 되돌릴 위험이 있었습니다. 「Ch 10 마감에서 이미 92로 고쳤고 90으로 내리지 말라」로 바꿨습니다.
- (같은 라운드에서 고친 학생 묶음·공용 파일) **`labs/part3/ch10-document-processing/README.md`**(검토 B C-4): 「청킹」·한정어 없는 「청크」와 `embed_query()` 설명(이 챕터 노트북에 0건)을 지금 설계로. **`textbook/part3/_build_index.py`** ch10 설명 문장(검토 B C-8): 「문서 형식과 청크 경계 … 청킹과 임베딩 설정을 비교」 → 「문서 형식과 나누는 자리를 확인합니다. 같은 자료에서 나누기 설정을 바꿔 색인과 검색 결과를 견줍니다.」 **`textbook/_notebook/checks/ch10-document-processing/visual-results.json`**(20행, 20/20 PASS로 갱신).
- 09절 작업에서 고친 챕터 밖 파일 두 개(`_build_index.py` 절 수 8 → 9, `finalize_continuity_evidence.py` 88 → 92)는 검토 B가 **둘 다 맞는 값**으로 판정했습니다.

## 11. 그림 색 판단 선례

- 넣은 자료·파일·문서 청크·질문·기록·**색인** **초록(tool)**, 정의한 함수·코드 단계·사람이 정한 설정(끊을 자리 순서·목표 크기·끊는 기준값·검색 개수) **파랑(flow)**, 출력으로 확인한 값·검사 결과 **노랑(measure)**, 실행한 임베딩 모델 **보라(model)**, 두 조건 공통 값·한 칸에만 해당하는 설명·뒤 챕터가 읽는 칸 **회색(클래스 없음)**. **빨강은 paired Before 결함 결과 한 상자씩**(01-4·02-4·03-4·04-4·05-4·06-4·07-4), experiment 08·09는 0장. `xychart-beta` 막대는 **주황**(02-3·05-3·08-3), 선은 **초록**(05-3).
  - **색인을 초록으로 둡니다**(Ch 9 요약 §10과 같음). 08-2 첫 판은 색인 상자를 보라로 두었는데 검토 B 08-3이 지적해 초록으로 바꾸고 임베딩 요청을 화살표 라벨로 옮겼습니다.
- 원인 과장 막기: 두 조건 공통 값은 맨 아래 회색 상자로. **한 칸에만 해당하는 설명을 공통으로 적지 않습니다**(06-2 회색 상자를 「표시가 맞은 위 칸에서는 …」으로 고친 선례, 검토 B 06-1). 노랑 메모에는 **출력으로 확인한 값만** 넣습니다(09-2 「저장 항목 6개」 → 「문서 청크 6개를 넣음」, 검토 B 09-1). 소스로만 확인한 동작은 메모에 「소스 확인:」을 붙입니다(07-3, 검토 B 07-3).
- 모양: subgraph = 「칸」, 칸 안 세로 쌓기는 `direction TB` + `a ~~~ b`, sequenceDiagram은 실선 요청·점선 응답 + `messageAlign: left`, 메모는 그 기록이 남는 시점에. **viewBox 폭 868 이하**(이번 35장 최대 846). 주의 두 가지(08절 작업 기록): **칸을 넘어가는 화살표가 있으면 칸 안 `direction`이 무시됩니다**(화살표를 칸끼리 이으세요), `xychart-beta`의 마지막 가로축 라벨이 테두리를 넘어 `svgBounds`에 걸립니다(라벨을 줄이고 단위는 캡션으로). 화살표 라벨이 폭을 늘리면 `<br>`로 줄입니다(08-2 재렌더에서 871.7 → 823.0). **렌더 도장 `*.render.json`은 지우지 않습니다**(mmd를 고치면 자동 재렌더, 같은 mmd는 `render_mermaid.py --force`).

## 12. 강사 확인 대상

- **챕터 제목·절 제목의 「청킹」**(반영하지 않음, 검토 A C-6·Q7): `_build.py` `CHAPTER = "Ch 10 · 문서 처리: 로더·청킹·임베딩"`, `SECTIONS`의 「05 · 문자·재귀·토큰 청킹」·「06 · 구조와 시맨틱 청킹」. 본문·노트북에서는 0건으로 만들었는데 페이지 머리글·목차·이전/다음 링크에 남아 있습니다. 권고: 챕터 「Ch 10 · 문서 처리: 읽기·나누기·임베딩」, 05 「05 · 문자·재귀·토큰 나누기」, 06 「06 · 구조와 시맨틱 나누기」. slug·파일 이름·묶음 목록·`chunk_id` 계약은 건드리지 않습니다(표시 문자열만 바뀝니다). 바꾸면 이웃 절 HTML의 이전/다음 링크 한 줄과 `_src/index.html` 절 표가 함께 바뀝니다.
- **07 제목의 「한국어」**(반영하지 않음, 검토 B 07-1): 한국어 관련 내용(MTEB·`multilingual-e5-large`·`bge-m3`·입력 접두사)이 b7 두 항목과 참고 자료 한 줄로 줄어 제목과 범위가 벌어졌습니다. 권고 제목은 「07 · 임베딩과 벡터 캐시」. 대신 b2에 「한국어 문서에 맞는 모델을 고르는 일은 지표를 잰 뒤 Ch 11에서 판단합니다」를 더했습니다.
- **08절 임베딩 모델 하나와 바꾸는 조건**(검토 B 수용(강사 확인)): 개선 전 두 모델 비교를 빼고 나누기 방식 세 가지 × 겹침 두 값으로 바꿨습니다. 모델 비교를 되살리려면 세 문장 설명과 요청 12번이 더 듭니다(08-diagnosis §8). 이번 실행에서 겹침이 1·2위를 바꾸지 않았다는 사실은 b6이 「겹침이 쓸모없다는 뜻은 아닙니다」로 한정했습니다.
- **05절 근거 예산 450조각**(검토 A Q5): 한도 150을 끌어내는 계산이 Ch 8 01절 입력 가용분 **440**과 다릅니다. 이번에는 「Ch 8 가용분 440과 다른 값이고 나누는 방법만 같다」는 문장을 더해 재실행 없이 닫았습니다. 예산을 Ch 8 값과 맞추면 한도가 100 안팎으로 내려가 Before/After 결과와 05-1·05-3·05-4 라벨을 모두 다시 맞춰야 합니다(**05절 재실행 필요**).
- **09 삽화 카드 수**(반영하지 않음, 검토 B 09-4): `09-4-세-묶음과-한-상자`의 꼬리표가 네모 4·타원 2·세모 1인데 실제 문서 청크는 PDF 6·DOCX 1·HWPX 1입니다. 「타원이 둘」이 DOCX 문서 청크가 둘인 것처럼 보이므로 다시 만들 때 6·1·1로. 지금은 「그림 읽기」가 「카드 수는 노트북 8절 문서 청크 수와 맞춘 것이 아닙니다」로 밝힙니다.
- **04절 분량**(검토 A C-8): 검사 문장 442로 01~05 가운데 가장 무거운데 강의 1h·실습 2h가 02절(328)과 같습니다. 03~09절도 400문장 안팎·코드 셀 23~30개를 강의 1h에 모두 읽기는 어렵습니다.
- **09 실습 절 30분**을 챕터 시수(강의 8h·실습 16h)에 더하지 않고 실습 16h 안으로 둔 것(규격 §7-2, Ch 1·3·4·5·9·22 선례).
- 검토 권고대로 **유지한 설계**(A Q1~Q5·B 결정 요청 판정 전부): 01 다섯 칸 계약·강의·실습 범위 문장, 02 표 읽기 구성·기준값 20자 사후 결정 공개, 03 쪽 없는 형식의 네 칸·`make_unit_mark()` 신설·Before/After 교체, 04 자리 칸 `section`·`make_section_mark()` 신설·한컴 링크 정리, 05 조각 수 한도 150·지킬 말 선정 기준·재귀 방식 결론 범위, 06 제목 칸 `heading`·`dimensions=256` 제거·`warnings.filterwarnings` 제거, 07 paired 유지·256 대 1536 비교·용어 네 개·08에 256차원 벡터를 이어 쓰지 않음, 08 목표 크기 400·3~5위를 결론에서 뺌, 09 주제·`pick_mark()` 신설·점수 경계 단락·질문 선택 근거·요청 4번. **권한 한 문장**: 이 유지 결정은 검토 두 보고서의 권고를 그대로 따른 것이고, 강사가 뒤집을 수 있는 항목은 위 목록에만 있습니다.

## 13. 기준 버전·요금 확인 날짜

- 실습 폴더 `labs/part3/ch10-document-processing/pyproject.toml`·`uv.lock`: pypdf **6.18.0**(Ch 9는 6.17.0), pdfplumber **0.11.10**, python-docx **1.2.0**, beautifulsoup4 **4.15.0**, langchain-core **1.6.2**, langchain-text-splitters **1.1.2**, langchain-experimental **0.4.2**, langchain-openai **1.6.0**, langchain-classic **1.0.8**, openai, tiktoken **0.14.0**, pytest 8.4.2, ruff 0.16.6. **`langchain` 메인 패키지가 없습니다.** 새 커널 `nbclient==0.11.0`·`ipykernel==7.3.0`, Linux aarch64 Python 3.12.13. 절마다 준비물에 기준 버전 + 「다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다」.
- 요금: 임베딩 `text-embedding-3-small` 100만 토큰당 0.02달러(OpenAI 모델 안내 2026-09-17 확인). 답을 쓰는 모델은 부르지 않았습니다.
- 소스 확인(설치판): `CharacterTextSplitter` 기본 구분자 `"\n\n"`·`keep_separator` 기본 `False`, `RecursiveCharacterTextSplitter` `keep_separator` 기본 `True`·기본 순서 `["\n\n","\n"," ",""]`·`_merge_splits`의 목표 초과 경고, `MarkdownHeaderTextSplitter` `strip_headers=True`, `SemanticChunker` `sentence_split_regex=r"(?<=[.?!])\s+"`·`buffer_size=1`·`if x > breakpoint_distance_threshold`, `OpenAIEmbeddings` `dimensions=None`·`chunk_size=1000`, `CacheBackedEmbeddings`의 `_make_default_key_encoder`(가르는 이름 + sha256 64자)·`query_embedding_cache=False`, pypdf 6.18.0의 `extraction_mode="layout"`.
- 실습 폴더 모듈은 노트북과 **이름이 비슷하고 모양이 다릅니다**: `split_char()`는 구분자를 쓰지 않고 문자 수로 그대로 자르고, `split_recursive()`·`split_token()`의 끊을 자리 순서는 `["\n\n", "\n", "다. ", ". ", " ", ""]`(한국어 종결 어미 표시가 하나 더), `_with_chunk_metadata()`의 `chunk_id`는 `E01:page2:recursive:0` 모양(08절은 `ch10:recursive:0000`), `experiment.py`는 임베딩 모델 두 개와 구조 방식을 쓰고 `runs/examples/`에 적습니다. **본문 b7에 이 차이를 적어 두었고 노트북은 모듈을 부르지 않습니다.**

## 14. 규격·절차서에 더한 줄

- `QUALITY-UPGRADE.md` §5-3: 「비교 그림에서 한 조건에만 해당하는 설명을 두 조건 공통 상자로 적지 않습니다」와 「노랑(measure) 상자·메모에는 출력으로 확인한 값만 넣고, 설치판 소스로만 확인한 동작은 「소스 확인」을 붙이거나 회색으로 둡니다」.
- `PLAYBOOK.md` §4: 같은 두 줄을 실행 절차 관점으로(재렌더 뒤 PNG를 열어 회색 상자가 어느 칸에 붙었는지 보기, 그림 라벨의 값이 노트북 출력에 실제로 있는지 `grep`으로 대조하기).

## 15. 남은 것

- **전체 마감**: §9 순서. `textbook/qa/upgrade-progress.md` Ch 10 행은 「완료(강사 확인 대기)」로 갱신했습니다.
- **다시 실행하면 함께 고칠 코드(지금은 재실행 금지)**: 02 노트북 [14](표 머리글 줄 찾기, 주석 뺀 13줄 — 규격 권장 3~12줄 초과, 검토 A C-8)를 두 셀로 나누기, 06·07·08 준비 셀 [2]·[3]의 `import os` 중복(09절만 한 번, 검토 B C-9), 08 노트북 [26] `make_record()`가 다음 셀 [27]에서 만드는 `corpus_scope`를 읽는 정의 순서(설명 한 줄로 막아 두었습니다, 검토 B 08-2).
- **삽화를 다시 만들 때 고칠 것**: 07-5는 손이 든 카드를 아래 칸 입구 안쪽으로 내리기(검토 B 07-4), 09-4는 꼬리표를 네모 6·타원 1·세모 1로(§12), 01-5는 봉투 앞면 빈 줄을 다섯 줄로(다섯 칸과 맞추기), 05-5는 도막 수를 여섯·여섯·열셋으로.
- **빌더**: `_build.py`에서 (a) 한 칸 `{{mermaid:이름}}`이 멈추지 않고 alt·캡션이 빈 `<figure class="mmd">`를 내는 자리를 `ValueError`로 막기(사용처 0곳, 검토 A C-5), (b) 표 감싸기를 img·mermaid 치환 뒤로 옮겨 `_template/builder.py`와 순서 맞추기(현재 결과는 같음). 모듈 설명에 두 항목을 적어 두었습니다.
- 2차 검토(두 보고서 끝 「2차 검토 때 볼 곳」과 「반영 결과」), 강사 확인(§12).
- **정리 대상**(삭제하지 않고 목록만, 삭제 승인 필요): 옛 도식 `figures/0[1-8]-*.svg`·`.excalidraw`·`.caption.md` 개선 전 판(`01-문서-계약`·`02-표-구조`·`03-형식별-단위`·`04-hwp-hwpx`·`05-청크-경계`·`06-구조-의미-청킹`·`07-임베딩-캐시`·`08-실험-격자`)과 `figures/_gen_figures.py`, `qa/upgrade/gates-wip-01.json`~`09.json`·`gates-wip.json`, `qa/upgrade/before/review-round1/`, `qa/content-results.json`(옮긴 `check_content.py`의 개선 전 결과), `qa/1280-*.png`·`390-*.png` 여섯 개, `qa/langchain-before/`·`qa/notebook-before/` 계열 개선 전 자료, 챕터·실습 폴더 `__pycache__`·`.pytest_cache`·`.ruff_cache`, `.cache/vm/venv-ch10-document-processing`(전체 마감 때), 기기 `/tmp/ch10-01`~`/tmp/ch10-09`·`/tmp/ch10-rvA`·`/tmp/ch10-rvB`·`/tmp/ch10-close`.

## 16. §2-7 리팩터 (2026-09-21)

- 앞 절·Ch 8·Ch 9 함수 14개를 `labs/part3/ch10-document-processing/notebooks/rag_tools.py`(코드 97줄)로 모으고 01~09절 준비 셀에서 한 줄로 가져옵니다: Ch 8 01 `count_tokens(encoding, text)`(규칙 객체를 첫 인자로 — 05절이 알림)·03 `find_missing_words`, Ch 9 02 `load_pdf_pages`·03 `make_source_mark`, 01 `make_source_record`, 02 `make_cell_text`·`make_row_text`, 03 `make_unit_record`·`make_unit_mark`, 04 `make_local_name`·`read_body_text`·`make_section_mark`, 05 `make_length_list`·`find_chunks_with_words`. 01도 Ch 9 함수 두 개를 가져옵니다(처음 가르친 `make_source_record`만 남김). NumPy는 쓰지 않았습니다(벡터 계산 0곳).
- 코드 셀 215 → **185**, 코드 줄 1574 → **1361**(−213, −13.5%; 도구 파일 포함 1458). 절 번호 그대로. 게이트 9/9·verify `PASS 9 sections / 185 code cells (max 14 lines)`·visual 18건·tests 38 passed.
- 01~09 새 커널 두 번: B 출력이 리팩터 전과 글자까지 같음(새 출력 두 줄 `조각 세는 규칙 이름: cl100k_base`만 더함). 인용·그림 수치 수정 없음. 01-3 파란 상자 라벨만 「Ch 9 03절 함수(도구 파일)」로 다시 렌더. §2-7 10항 입력 수정 없음.
- **08을 다시 실행해 Ch 11 입력이 바뀌었습니다**(§4 「08 재실행은 기본적으로 금지」의 예외 — §2-7 규격): `runs/continuity-ch10-indexing.jsonl` `58cc790c…` → `0984e167…`, 사본 `runs/continuity/20260921T062600-ch10-0N.jsonl`(A 실행 사본은 `qa/upgrade/before-2-7/runs/moved/`), `runs/` 64 → 70개. Ch 11 01~05는 읽는 값이 같고, 06 출력의 실행 이름 열두 줄만 다음 재실행 때 바뀝니다(재실행 안 함).
- 학생 묶음: `part3-practice.zip` 94항목(`040e53ea…45bc5`), `check_delivery.py` 통과. 세부는 `handoff.md` 「§2-7 리팩터 (2026-09-21)」.

