# Ch 10 조사 노트 — 문서 처리·청킹·임베딩

조사일: **2026-09-08**. 이 문서는 교재 집필을 위한 사실 확인 노트입니다. 문서 파서와 임베딩 모델의 최종 선택은 `labs/`에서 같은 말뭉치·같은 질의셋으로 측정한 뒤에만 확정합니다.

## 1. 로더와 문서 유형

### PDF

- `pypdf` 6.18.0 공식 문서는 `PdfReader`와 `page.extract_text()`를 제공하며, `extraction_mode="layout"`도 제공합니다. 다만 일반 PDF의 콘텐츠 스트림은 문단·표·머리말이라는 **의미 계층을 보장하지 않으므로**, 절대 좌표로 놓인 글자를 어떤 행·열로 볼지 확정할 수 없습니다. 표는 특히 글자가 절대 위치에 놓일 수 있어 열과 행을 안정적으로 복원하기 어렵습니다. 태그가 있는 PDF가 존재해도, 로더는 대상 파일에서 실제로 구조가 보존되는지 확인해야 합니다. [pypdf: Extract Text from a PDF](https://pypdf.readthedocs.io/en/stable/user/extract-text.html)
- 스캔 PDF에서 `pypdf`는 이미 존재하는 OCR 텍스트층은 읽을 수 있지만 OCR 엔진은 아니며 이미지 안의 글자를 추출하지 않습니다. 공식 문서는 스캔 문서라면 Tesseract 같은 OCR을 고려하되, 디지털 PDF를 항상 OCR로 렌더링하지 말라고 안내합니다. 디지털 PDF의 글꼴·인코딩 정보가 OCR보다 문자 구별에 유리할 수 있기 때문입니다. 같은 문서는 압축 해제된 300 MB 콘텐츠 스트림에 10 GB 메모리가 든 사례도 명시합니다. [pypdf: Extract Text from a PDF](https://pypdf.readthedocs.io/en/stable/user/extract-text.html)
- PyMuPDF는 `Page.find_tables()`로 표 후보와 셀 경계를 찾습니다. 검출 전략(`lines`, `lines_strict`, `text`)과 허용오차를 조정할 수 있으므로, 표가 깨진 사례는 결과만 비교하지 말고 전략과 문서의 선·텍스트 배치를 함께 기록합니다. [PyMuPDF: `Page.find_tables()`](https://pymupdf.readthedocs.io/en/latest/page.html#Page.find_tables)
- `pdfplumber`는 문자·사각형·선 정보를 다루며 표 추출과 시각 디버깅을 제공합니다. `find_tables()`·`extract_tables()`는 선 또는 단어 정렬에서 셀 경계를 추정해 `표 → 행 → 셀` 구조를 반환합니다. 공식 README는 기계 생성 PDF에서 가장 잘 작동한다고 밝힙니다. **MIT 라이선스**라서 AGPL을 수용할 수 없는 배포 경로의 두 번째 실제 표 파서 후보로 적합하지만, 스캔 PDF OCR이나 모든 표의 정확성을 보장하지는 않습니다. [pdfplumber upstream README](https://github.com/jsvine/pdfplumber/blob/stable/README.md), [MIT license](https://github.com/jsvine/pdfplumber/blob/stable/LICENSE.txt)
- PyMuPDF의 통합 OCR은 별도 설치한 Tesseract-OCR에 기반합니다. OCR 결과를 한 번 만들면 통상 추출·검색 API로 읽을 수 있지만, OCR이 필요한 페이지만 처리해야 합니다. [PyMuPDF: OCR](https://pymupdf.readthedocs.io/en/latest/recipes-ocr.html)
- **배포 주의:** PyMuPDF/MuPDF는 AGPL 또는 상용 라이선스 이중 체계입니다. 패키지를 교육용 예제로 실행하는 것과 이를 포함한 제품을 배포하는 것은 별도로 검토해야 합니다. [PyMuPDF: License and Copyright](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright)

**교재 코드 사실:** 텍스트 중심 디지털 PDF의 기준선은 `pypdf`로 두고, 스캔 3종은 추출 문자열 길이·한글 비율·사람 검토를 먼저 기록합니다. 표는 `pypdf` 텍스트 결과와 `pdfplumber` 표 후보를 같은 페이지 단위로 비교하고, PyMuPDF는 라이선스 조건을 충족하는 별도 실험으로 둡니다. 표가 문장과 섞여 의미를 잃으면 단순 텍스트 추출의 실패로 명시합니다.

### DOCX·HTML·CSV

- `python-docx`의 `Document`는 문단과 표를 별도 객체로 다루며 `document.tables`, 각 표의 `rows`·`columns`·`cell()` API로 셀을 순회할 수 있습니다. 따라서 단락 텍스트와 표를 같은 문자열로 무분별하게 이어 붙이지 말고, 출처·문서 순번·표 번호를 메타데이터로 보존합니다. [python-docx: Quickstart](https://python-docx.readthedocs.io/en/latest/user/quickstart.html)
- Beautiful Soup는 파싱 트리 탐색 도구이며 내장 `html.parser`, `lxml`, `html5lib` 등을 선택할 수 있습니다. 공식 문서는 잘못된 HTML에서는 파서마다 서로 다른 트리를 만들 수 있다고 밝힙니다. `lxml`은 빠르다고 권하지만, 교재에서는 결과가 파서에 의존한다는 실패 사례도 포함합니다. [Beautiful Soup: Installing a parser](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)
- Python 표준 `csv` 모듈은 CSV의 엄밀히 단일한 표준이 없어 생산자별 구분자·인용 차이가 생길 수 있다고 설명합니다. 파일은 `newline=''`로 열고, 인코딩을 명시합니다. `Sniffer.has_header()`는 거짓 양성과 거짓 음성을 낼 수 있는 거친 휴리스틱이므로 헤더를 자동 확정하지 않습니다. [Python 3.14 `csv`](https://docs.python.org/3/library/csv.html)

**교재 코드 사실:** CSV는 `DictReader`를 쓰되, `encoding`·`dialect`·헤더 유무를 입력 계약으로 드러냅니다. HTML은 본문 선택자와 제거할 `script`·`style` 기준을 코드에 적고, HTML 전체를 텍스트화하는 예제는 자료 구조를 잃는 실패 사례로 둡니다.

### HWP·HWPX

- 한컴의 공식 FAQ는 HWPX를 OWPML 기반, 국가표준 KS X 6101에 등록된 XML 기반 개방형 파일 포맷이라고 설명합니다. [한컴: HWPX FAQ](https://www.hancom.co.kr/support/faqCenter/faq/detail/2784)
- 한컴 개발자 문서는 HWP를 한글 네이티브 형식, HWPX를 한글 표준 형식으로 구분하고, 둘 다 열기 API의 형식 값으로 지원합니다. [Hancom Developer: `HwpCtrl.Open`](https://developer.hancom.com/en-us/webhwp/devguide/hwpctrl/methods/open)
- 한컴의 2026-07-31 기술 블로그는 HWPX가 OWPML Open XML을 ZIP 컨테이너에 묶은 구조여서 텍스트 접근이 기존 HWP 이진 레코드 해석보다 쉽다고 설명합니다. 그러나 HWP는 구조·레코드 흐름을 정확히 해석해야 하며, HWPX도 본문·설정·메타데이터가 여러 XML에 나뉘어 표와 단락 계층을 단순 텍스트 추출만으로 원래대로 복원하지 못할 수 있습니다. 이는 **공식 공급자 설명이지만 제품 문서가 아닌 기술 블로그**라는 한계를 붙여 인용합니다. [Hancom Blog: HWP·HWPX data extraction](https://blog.hancom.com/en/hwp-hwpx-data-extraction-format-library/)

**교재 코드 사실:** HWP를 파이썬 범용 로더로 "지원한다"고 단정하지 않습니다. 실습에서는 HWPX의 ZIP+XML 구조를 관찰하고, HWP는 HWPX 변환 또는 한컴이 제공하는 도구·SDK라는 처리 경계를 제시합니다. 실제 HWP/HWPX 샘플별 성공 여부는 실행 결과로만 적습니다.

## 2. 상용 문서 파서 비교의 정확한 범위

| 서비스 | 공식 문서로 확인한 기능 | 교재에서 반드시 함께 보일 제한 |
|---|---|---|
| Upstage Document Parse | Console 예제는 `document-digitization` 엔드포인트, `ocr="force"`, 표 base64 출력 옵션을 보입니다. 제품 가격 페이지는 Parse only를 **페이지당 $0.01**로 표기합니다. | 가격과 API 경로는 변경될 수 있으므로 확인일을 붙입니다. 실제 한국어 표·스캔 품질은 동일 PDF의 로컬 기준선과 비교해 측정합니다. [Console example](https://console.upstage.ai/api-keys?api=document-parsing), [API pricing](https://www.upstage.ai/pricing/api) |
| LlamaParse / LlamaCloud | 공식 API는 파일 ID 또는 URL을 비동기로 파싱하며, `fast`(규칙 기반)·`cost_effective`·`agentic`·`agentic_plus` 티어와 OCR·표·차트 옵션, 언어 지정, Markdown/Text 확장을 제공합니다. | API의 `latest`는 움직입니다. 2026-09-08 문서는 `fast=2026-06-15`, 나머지 3개 티어=`2026-08-19`를 현재값으로 제시하므로, 재현 실습은 `latest` 대신 날짜 버전을 기록합니다. [LlamaIndex API: Parse File](https://developers.api.llamaindex.ai/api/python/resources/parsing/methods/create/) |

두 서비스는 비교 대상으로만 소개합니다. "어느 쪽이 더 정확하다"는 일반 결론이나 한국어 정확도 수치는 공식 문서로 확인하지 못했으므로 쓰지 않습니다. 수강생 문서를 외부 API로 보내는 예제는 자격증명·비용·전송 정책을 분리해 표시합니다.

## 3. 청킹: 검증된 설명과 실습 설계

- **문자 수 청킹:** 가장 단순한 기준선입니다. 빠르고 재현 가능하지만, 문자 수는 모델 토큰 수나 문서 의미 단위와 같지 않습니다.
- **재귀 문자 청킹:** LangChain 공식 문서는 일반 텍스트의 권장 시작점으로 소개합니다. 기본 구분자 `\n\n`, `\n`, 공백, 빈 문자열을 큰 단위부터 시도해 문단·문장·단어를 가능한 오래 함께 둡니다. `chunk_size`는 `length_function` 기준 최대 크기, `chunk_overlap`은 분할 경계의 정보 손실을 줄이는 목표 중첩입니다. [LangChain: Recursive splitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)
- **토큰 청킹:** 임베딩 API와 생성 모델의 입력 한도에 직접 맞추려면 실제 토크나이저로 크기를 재야 합니다. 문자 수를 토큰 수로 환산해 단정하지 않습니다. OpenAI 임베딩 가이드는 두 `text-embedding-3` 모델의 최대 입력이 8,192 토큰이라고 명시합니다. [OpenAI: embeddings guide](https://developers.openai.com/api/docs/guides/embeddings)
- **구조 기반 청킹:** HTML 제목, DOCX의 문단·표, HWPX의 XML 단위처럼 로더가 보존한 경계를 먼저 사용합니다. 구조가 없는 PDF는 이 방식을 보장할 수 없으므로, 파서 출력에서 헤더·표·페이지 경계가 실제로 살아 있는지 먼저 확인합니다.
- **시맨틱 청킹:** 인접 문장·단락의 임베딩 유사도를 계산해 주제 변화 지점에서 나누는 방식입니다. 추가 임베딩 계산과 임계값 선택이 필요하므로 재귀 청킹보다 자동으로 낫다고 쓰지 않습니다. Ch 9 하네스의 같은 질의·정답 문서·동일 임베딩 모델로 Recall@k와 실패 질의를 비교해야 합니다. 공개된 현재 LangChain 계획 이슈는 `SemanticChunker`를 `langchain-experimental`에 둔다고 명시하므로, 교재 코드의 안정 API로 전제하지 않습니다. [LangChain issue #4722](https://github.com/langchain-ai/docs/issues/4722)

**한국어:** LangChain 공식 안내의 무공백 언어 예외는 중국어·일본어·태국어용입니다. 한국어에는 보통 공백이 있으므로 그 설정을 그대로 적용한다는 근거는 없습니다. 다만 `.`·줄바꿈만 기준으로 쪼개면 `합니다.` 같은 문장 종결과 제목·목록의 구조가 섞일 수 있으므로, 한국어 실습에서는 문단·제목·표 경계를 먼저 보존하고 수치만 하네스로 조정합니다.

## 4. 임베딩 후보·비용·캐시

- OpenAI 공식 문서는 `text-embedding-3-small` 기본 차원 1,536, `text-embedding-3-large` 기본 차원 3,072이며 `dimensions`으로 축소 가능하다고 명시합니다. 두 모델은 최대 8,192 입력 토큰입니다. API 모델 페이지의 2026-09-08 확인 단가는 각각 **$0.02 / 100만 토큰**, **$0.13 / 100만 토큰**입니다. [OpenAI: embeddings guide](https://developers.openai.com/api/docs/guides/embeddings), [small model](https://developers.openai.com/api/docs/models/text-embedding-3-small/), [large model](https://developers.openai.com/api/docs/models/text-embedding-3-large/)
- OpenAI 가이드는 v3의 MTEB 점수와 달러당 대략적 영문 텍스트 페이지 수를 제공하지만, 그것은 한국어 말뭉치의 검색 품질 보증이 아닙니다. `text-embedding-3-large`가 비영어 작업에도 가장 성능이 좋다는 공급자 설명은 후보 선정 근거가 될 수 있어도, Ch 10의 한국어 우열 결론은 자체 질의셋 평가로 정합니다. [OpenAI: large model](https://developers.openai.com/api/docs/models/text-embedding-3-large/)
- 오픈 후보는 **다국어 검색용 모델 카드가 있고 로컬 실행 가능한 모델**만 비교합니다. 다음 두 모델은 후보일 뿐, 정본으로 확정하지 않습니다.
  - `intfloat/multilingual-e5-large`: MIT, 1,024차원, XLM-RoBERTa 기반 100개 언어 지원을 표방합니다. 검색에는 문서에 `passage: `, 질의에 `query: ` 접두사를 붙여야 하며, 모델 카드는 접두사 생략 시 성능 저하를 경고합니다. 긴 입력은 최대 512 토큰에서 잘립니다. 실험 고정 리비전은 `3d7cfbdacd47fdda877c5cd8a79fbcc4f2a574f3`(모델 허브 API에서 2026-09-08 확인)입니다. [pinned model card](https://huggingface.co/intfloat/multilingual-e5-large/blob/3d7cfbdacd47fdda877c5cd8a79fbcc4f2a574f3/README.md)
  - `BAAI/bge-m3`: MIT, 1,024차원, 100개 이상 언어와 최대 8,192 토큰을 명시합니다. 단일 dense 벡터뿐 아니라 sparse·multi-vector 검색 기능도 제공하지만, Ch 10의 2모델 비교는 dense 임베딩만 같은 조건으로 사용합니다. 실험 고정 리비전은 `5617a9f61b028005a4858fdac845db406aefb181`(모델 허브 API에서 2026-09-08 확인)입니다. [pinned model card](https://huggingface.co/BAAI/bge-m3/blob/5617a9f61b028005a4858fdac845db406aefb181/README.md)
  - 비교 기준은 한국어 `queries.jsonl`의 Recall@k, 인덱싱 시간, 디스크 크기, 청크당 임베딩 비용/속도입니다. 각 실행에는 리비전 SHA, 모델 카드의 입력 접두사, 차원, 최대 길이, 라이선스를 함께 적습니다.
- MTEB는 모델·과제·언어별 평가 결과를 모으는 벤치마크이며, 현재 공식 문서는 캐시 임베딩 예시를 별도로 제공합니다. 리더보드의 종합 순위만 가져오지 말고 **Korean retrieval 과제와 우리 말뭉치**를 분리해 봅니다. [MTEB overview](https://docs.mteb.org/overview/), [MTEB multilingual v2 leaderboard](https://leaderboard.mteb.org/benchmark/MTEB(Multilingual,%20v2))
- **벡터 캐시**의 키에는 최소한 `정규화된 청크 텍스트 해시`, `임베딩 제공자·모델·리비전·차원`, 해당 모델의 입력 접두사를 넣습니다. 이 값이 같으면 파서나 스플리터를 바꾸어도 같은 텍스트의 벡터는 재사용할 수 있습니다. **인덱스 매니페스트**에는 별도로 `문서 원문 해시`, `정규화·파서 버전`, `청킹 전략과 설정`, 청크와 벡터 캐시 키의 대응을 기록합니다. 매니페스트가 바뀌면 인덱스는 다시 구성하되, 추가·변경된 청크만 임베딩하고 불변 청크의 벡터는 캐시에서 읽습니다. 모델·리비전·차원·입력 접두사가 달라지면 같은 텍스트도 재임베딩합니다.
- Sentence Transformers 공식 예제도 문서에는 `encode_document`, 질의에는 `encode_query`를 사용해 같은 벡터 공간에서 코사인 유사도를 계산하는 비대칭 검색 흐름을 보여 줍니다. 오픈 모델이 해당 API의 프롬프트·입력 규칙을 요구한다면 반드시 모델 카드의 규칙도 따릅니다. [Sentence Transformers: Semantic Search](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)

## 5. 집필·실습용 결정 규칙

1. 로더 결과에는 `source_path`, `source_type`, `page` 또는 `section`, `parser`, `parser_version`, `has_table`, `ocr_used`를 붙입니다.
2. 같은 PDF를 `pypdf`, PyMuPDF, 상용 파서 중 사용할 수 있는 것으로 처리하고, 원문 페이지와 추출 결과를 나란히 보고 표·순서·누락을 사람 검토합니다.
3. Ch 9의 고정 질의셋으로 **3 청킹 × 2 임베딩**을 실험합니다. 청킹 하나의 승자를 선언하기 전에 Recall@k와 대표 실패 3건 이상을 제시합니다.
4. 모델·차원·청크 설정 변경은 인덱스 전체 재생성 사유입니다. 비용 표에는 실제 입력 토큰 합계와 확인일을 기록하고, API 가격은 수치가 아닌 공식 가격 URL도 함께 둡니다.

## 6. 버전·근거 한계

- pypdf의 위 문서는 6.18.0, LangChain의 `RecursiveCharacterTextSplitter` 참조 페이지는 1.1.2를 표시했습니다. 프로젝트의 기준선 LangChain v1.4와 패키지 버전 표기가 일치하지 않을 수 있으므로, 수록 코드의 `langchain-text-splitters` 버전은 Ch 10 `pyproject.toml`에 고정하고 `uv run` 결과로 검증합니다.
- Upstage·LlamaParse의 가격·티어·API는 상용 서비스라 변경될 수 있습니다. 본문에는 조사일을 붙이고, 실행 직전에 공식 페이지를 다시 확인합니다.
- "2026년에 청크가 커진다"는 일반 경향은 이 조사에서 공식·재현 가능한 근거로 확인하지 못했습니다. 교재에는 일반 법칙으로 쓰지 않고, 말뭉치와 평가값에 따라 정한다는 원칙만 둡니다.
