# Part 1 집필 조사 근거

확인일: 2026-09-09 (KST). 이 메모는 Ch3–5의 실행 설계와 참고 자료를 위한 근거입니다. 패키지와 모델의 **실제 출력값**은 각 챕터 노트북을 빈 커널에서 실행한 뒤에만 본문에 기록합니다.

## Ch3 — Git & GitHub 협업

### 확정할 실습 범위

- `git revert <commit>`은 기존 커밋의 효과를 되돌리는 **새 커밋**을 만듭니다. 공개 브랜치에서 변경을 취소하는 예제에 맞습니다. 실습 전에 작업 트리가 깨끗해야 합니다.
- `git reflog show`는 이 로컬 저장소에서 참조 끝이 이동한 기록입니다. `HEAD@{n}`을 찾은 뒤 별도 복구 브랜치로 확인하게 합니다. reflog는 영구 백업이 아니며 기본 만료 설정이 있으므로, 원격 협업의 복구 수단으로 단정하지 않습니다.
- `git worktree add -b <branch> <path> main`은 같은 저장소에서 브랜치별 작업 폴더를 만드는 예제에 적합합니다. 연결 worktree는 끝난 뒤 `git worktree remove <path>`로 정리합니다. 현재 환경의 Git은 `2.50.1`입니다.
- GitHub Flow 절은 `main`에서 짧은 기능 브랜치를 만들고, 커밋·검토·병합하는 흐름으로 설명합니다. **로컬 bare remote는 GitHub가 아니므로 실제 PR·승인·보호 규칙을 만들 수 없습니다.** 외부에 발행하지 않는 실습에서는 bare remote에 push한 뒤 `git diff main...feature`와 `git log main..feature`로 “PR 검토에 해당하는 비교”를 수행한다고 명시합니다. GitHub의 실제 줄 단위 댓글·Approve·Request changes는 GitHub 저장소에서만 실습할 수 있습니다.

### 시크릿 사고 실습의 경계

- 실제 키·개인 토큰을 절대 쓰지 않습니다. 격리된 임시 저장소에 `DEMO_SECRET_DO_NOT_USE=...`만 커밋합니다.
- `.gitignore`는 새 파일이 Git에 추가되는 것을 막을 뿐, 이미 추적한 파일이나 커밋 이력을 지우지 않습니다.
- 이력 삭제는 `git-filter-repo`로 다룹니다. 현재 환경에는 `git filter-repo` 명령이 없습니다. upstream은 Git 2.36+와 Python 3.6+를 요구하며, 단일 스크립트를 PATH에 두거나 패키지 관리자로 설치하는 방법을 안내합니다. 이 장의 Git 2.50.1은 Git 버전 조건을 만족합니다.
- 실제 유출이라면 이력 재작성만으로 충분하지 않습니다. 제공자에서 자격 증명을 즉시 폐기·재발급하고, 협업자에게 새 이력으로 다시 복제하도록 안내해야 합니다. 수업에서는 더미 문자열이 모든 참조에서 사라졌는지 `git log -S`와 `git grep $(git rev-list --all)`류의 확인으로 관찰하되, 참조·reflog·원격 clone에 남을 수 있는 복제본까지 제거했다고 주장하지 않습니다.

### 공식 근거

- [git-revert](https://git-scm.com/docs/git-revert.html) — 기존 변경을 역으로 적용하는 새 커밋이며, 버려지는 변경과 구분합니다.
- [git-reflog](https://git-scm.com/docs/git-reflog) — 로컬 참조 변경 기록, `HEAD@{n}`, 만료 동작을 설명합니다.
- [git-worktree](https://git-scm.com/docs/git-worktree) — 복수 worktree, `add`와 `remove`를 설명합니다.
- [GitHub: About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests) — 브랜치, 검토, 검사, 병합의 PR 흐름입니다.
- [GitHub: Giving reviews](https://docs.github.com/en/pull-requests/concepts/giving-reviews) — Comment·Approve·Request changes와 줄 단위 검토를 구분합니다.
- [git-filter-repo upstream README](https://github.com/newren/git-filter-repo) 및 [설치 안내](https://github.com/newren/git-filter-repo/blob/main/INSTALL.md) — 공식 Git 배포물에는 없는 별도 이력 재작성 도구의 설치 조건입니다. 외부 upstream 자료이며 Git SCM 매뉴얼보다 보조 근거입니다.

## Ch4 — 데이터를 도구 함수로 만들기

### 재현 가능한 실습 설계

- Pandas는 작은 CSV/리스트 데이터를 `DataFrame`으로 만들고, 열 선택·필터·결측값 처리·정렬을 한 동작씩 보여 줍니다. 데이터 분석 보고서를 만드는 흐름으로 확장하지 않고, `fetch_orders()`처럼 이후 도구로 감쌀 조회 함수의 입력·반환값을 고정합니다.
- 관계형 모델은 SQLite 한 파일에서 `customers`와 `orders`를 만들고 기본 키와 외래 키를 보여 주는 최소 사례로 제한합니다. SQL 값에는 문자열 결합이나 f-string이 아니라 DB-API 자리표시자를 사용합니다. Pandas `to_sql`·`read_sql`로 DataFrame과 테이블을 왕복하되, 테이블을 매번 덮어쓰는 `replace`가 데이터 삭제임을 명시합니다.
- HTTP 페이지네이션은 **실제 HTTP 요청**으로 관찰합니다. 노트북 안에서 `ThreadingHTTPServer`를 localhost의 임의 포트에 띄우고, `httpx.Client`가 `params={"page": ...}`로 요청하여 JSON의 `items`와 `next_page`를 끝까지 읽게 합니다. 이 서버는 외부 API 모사가 아니라 로컬 HTTP 서버임을 캡션과 출력에 명시합니다. `raise_for_status()`, timeout, 응답 JSON 형식 오류를 별도 실패 사례로 다룹니다.
- HTML 파싱은 제공한 정적 HTML 문자열 또는 수업용 공개 fixture만 씁니다. Beautiful Soup 생성자에 parser 이름(`"lxml"` 또는 `"html.parser"`)을 명시합니다. 잘못된 HTML은 parser마다 다른 트리를 만들 수 있으므로, 환경에 따라 결과가 같다고 단정하지 않습니다.
- robots.txt는 크롤러 접근 범위를 기술하는 관례이며 법적 허가나 개인정보·저작권 이용 허가가 아닙니다. 예제 URL마다 robots.txt, 서비스 약관, 저작권·DB 권리, 개인정보 및 요청 빈도를 별도로 확인하게 합니다. `urllib.robotparser`는 robots.txt를 읽는 표준 라이브러리입니다. 이 교재는 법률 판단을 제공하지 않습니다.

### 현재 패키지 기준

PyPI에서 2026-09-09에 확인한 최신 릴리스는 `pandas==3.0.5`, `httpx==0.28.1`, `beautifulsoup4==4.15.0`, `lxml==6.1.3`입니다. Ch4의 `pyproject.toml`과 노트북 설치 셀은 **같은 값**으로 잠그고, 빈 커널 실행 성공 뒤에만 이 값을 정본으로 기록합니다.

### 공식 근거

- [pandas `DataFrame.to_sql`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html), [pandas `read_sql`](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html) — DataFrame과 SQL 데이터베이스의 입출력 API입니다.
- [PyPI pandas](https://pypi.org/project/pandas/), [httpx](https://pypi.org/project/httpx/), [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), [lxml](https://pypi.org/project/lxml/) — 위 고정 후보 버전의 배포 기준입니다.
- [Python `sqlite3`](https://docs.python.org/3/library/sqlite3.html) — SQLite DB-API와 값 자리표시자 사용 근거입니다.
- [HTTPX QuickStart](https://www.python-httpx.org/quickstart/) — client, query parameter, timeout, `raise_for_status()` 사용 근거입니다.
- [Python `http.server`](https://docs.python.org/3/library/http.server.html) — 로컬 `ThreadingHTTPServer` API 근거입니다.
- [Beautiful Soup 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — HTML/XML 파싱과 parser별 차이입니다.
- [Google Search Central robots.txt 안내](https://developers.google.com/search/docs/crawling-indexing/robots/intro) — robots.txt의 목적은 crawler traffic 관리이며 비공개 처리 수단이 아니라는 설명입니다.
- [Python `urllib.robotparser`](https://docs.python.org/3/library/urllib.robotparser.html) — robots.txt를 읽는 표준 라이브러리입니다.

## Ch5 — LLM 동작 원리 (첫 API 호출 전)

### 권장 모델과 실행 한계

- 토큰 수 비교에는 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`의 tokenizer를 권장합니다. 모델 카드상 50개 언어, Apache-2.0이며, 한국어와 영어 문장을 **동일 tokenizer에서** `add_special_tokens=False`로 부호화해 token 수와 글자당 token 수를 함께 출력합니다. 기준 revision은 `8d253e9c039960257027285d16027b422b85f011`입니다. special token을 빼는 이유는 문장 자체의 분할 효율을 비교하기 위해서이며, 실제 모델 입력 길이는 special token까지 포함해 다시 계산해야 합니다.
- 의미 유사도에는 같은 multilingual 모델을 `SentenceTransformer.encode()`로 실행하고 cosine similarity 행렬을 출력합니다. 한국어 원문/의미가 같은 영어 번역/주제가 다른 문장을 함께 두고, 높은 수치는 “문장이 같은 뜻”의 증거가 아니라 해당 모델·문장·거리 함수에서의 근접도라고 설명합니다.
- temperature 관찰에는 `Qwen/Qwen2.5-0.5B-Instruct` revision `7ae557604adf67be50417f59c2c2f167def9a775`를 권장합니다. 0.49B, Apache-2.0, 한국어를 포함한 다국어 지원 모델이며 safetensors는 약 988MB입니다. `apply_chat_template()`로 입력을 만들고 생성합니다. CPU/MPS에서 내려받기와 첫 실행 시간이 걸리므로, 실습은 짧은 한국어 prompt와 작은 `max_new_tokens`로 제한합니다. 작은 모델의 출력 분산은 sampling 원리를 보이는 관찰일 뿐 한국어 생성 품질이나 LLM 일반 성능의 판단 근거가 아닙니다.
- 같은 prompt를 `do_sample=True`, 고정 `top_p`, temperature `0.2`와 `1.0`에서 각각 3회 생성합니다. seed는 반복마다 달리 기록하고 `max_new_tokens`는 작게 제한합니다. `do_sample=False`인 greedy decoding에서는 temperature가 효과를 내지 않으므로, 반드시 sampling을 켭니다. 낮은 temperature가 항상 더 정확하다는 결론을 내리지 않습니다.
- Apple Silicon에서는 `torch.backends.mps.is_available()`일 때만 MPS를 쓰고, 아니면 CPU로 fallback합니다. MPS 사용 여부와 모델 내려받기 시간은 기기마다 다르므로 실제 로그에 기록합니다.

### 현재 환경 확인과 버전

- 현재 사용자 cache에는 `sentence-transformers/all-mpnet-base-v2` revision `e8c3b32edf5434bc2275fc9bab85f82640a19130`만 있습니다. 이는 영어 중심 모델이므로 한국어/영어 비교와 다국어 유사도 실습에 쓰지 않습니다. 언어별 분할 차이를 추가로 보이려면 `openai-community/gpt2` revision `607a30d783dfa663caf39e06633721c8d4cfcd7e` (MIT)와 `klue/bert-base` revision `77c8b3d707df785034b4e50f2da5d37be5f0f546` (CC-BY-SA-4.0)의 **tokenizer만** 사용할 수 있습니다. 서로 다른 tokenizer의 수치는 어휘와 알고리즘까지 함께 바뀐 비교이므로, 언어 자체의 보편적 효율 수치로 해석하지 않습니다.
- Ch2 가상환경에는 `torch`, `transformers`, `sentence-transformers`, `pandas`, `httpx`, `beautifulsoup4`, `lxml`이 없습니다. Ch5는 독립 `pyproject.toml`을 만들어야 합니다.
- PyPI 2026-09-09 조회값: `transformers==5.16.1`, `sentence-transformers==6.0.1`, `torch==2.14.0`. 이 조합은 아직 이 저장소에서 빈 커널로 실행 검증하지 않았습니다. 실제 설치·모델 다운로드·CPU/MPS 실행이 통과한 뒤 고정하며, 실패하면 호환되는 잠금 조합과 원인을 `확인 필요 항목`에 남깁니다.

### 공식 근거

- [Hugging Face Tokenizers](https://huggingface.co/docs/transformers/fast_tokenizers) — `AutoTokenizer.from_pretrained`, encode/decode, special token의 의미입니다.
- [Hugging Face Generation strategies](https://huggingface.co/docs/transformers/generation_strategies) — greedy decoding과 `do_sample=True` sampling의 차이입니다.
- [Transformers `GenerationConfig`](https://huggingface.co/docs/transformers/main_classes/text_generation) — `temperature`, `do_sample`, `max_new_tokens` 설정입니다.
- [Sentence Transformers STS](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html) — embedding과 cosine similarity 행렬 예제입니다.
- [Sentence Transformers multilingual example](https://www.sbert.net/examples/sentence_transformer/training/multilingual/README.html) — 다국어 model과 cross-lingual similarity의 적용 범위입니다.
- [multilingual MiniLM model card, pinned revision](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/tree/8d253e9c039960257027285d16027b422b85f011) — 50 languages, Apache-2.0, encode/similarity 사용법입니다.
- [Qwen2.5-0.5B-Instruct model card, pinned revision](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/tree/7ae557604adf67be50417f59c2c2f167def9a775) — 0.49B, Apache-2.0, 다국어 지원 및 chat-template→generate 사용법입니다.
- [KLUE BERT model card](https://huggingface.co/klue/bert-base/tree/77c8b3d707df785034b4e50f2da5d37be5f0f546) — 한국어 tokenizer의 출처와 CC-BY-SA-4.0 라이선스입니다.
- [PyTorch MPS backend](https://docs.pytorch.org/docs/main/backends.html) — MPS가 빌드되었는지와 사용 가능한지는 구분해야 한다는 근거입니다.
- [PyPI transformers](https://pypi.org/project/transformers/), [sentence-transformers](https://pypi.org/project/sentence-transformers/), [torch](https://pypi.org/project/torch/) — Ch5 고정 후보 버전의 배포 기준입니다.

### 길어진 입력·어텐션·환각을 설명할 때의 연구 근거

- **컨텍스트 윈도 크기와 사용 품질은 다릅니다.** Chroma의 *Context Rot* 보고서는 긴 입력에서 관련 정보 외의 문맥을 늘리면 성능이 일관되게 낮아졌고, 18개 모델에서 구조적으로 이어진 haystack이 무작위 순서보다 어려웠다고 보고합니다. 학생 실험은 “토큰 수를 늘리면 반드시 성능이 떨어진다”를 재현했다고 쓰지 않습니다. 작은 Qwen 한 모델·한 질문의 결과는 그 조건의 관찰이며, Chroma의 특정 benchmark와 모델군을 일반화하지 않습니다.
- *Lost in the Middle*은 다문서 QA와 key-value 검색에서 답이 되는 정보의 **위치만** 바꾸었을 때, 당시 여러 모델이 시작·끝보다 중간 위치에서 더 낮은 성능을 보였다고 보고합니다. 절의 도식은 입력 길이와 정보 위치를 분리해 그립니다. 이 결과는 2023년 연구 대상 모델의 경향이며, 현재 모든 long-context 모델의 보증 또는 반증은 아닙니다.
- 어텐션의 직관은 “다음 표현을 만들 때 입력 토큰 사이의 관계에 가중치를 두어 정보를 섞는 방식”까지만 설명합니다. 원 논문은 Transformer가 recurrence와 convolution 없이 attention만으로 구성된 architecture를 제안했습니다. attention 가중치 하나를 사람의 이유나 사실 검증 증거로 해석하지 않으며, 수식·구현은 이 챕터 범위 밖입니다.
- 환각은 모델이 거짓을 의도한다는 뜻이 아닙니다. OpenAI의 2025 연구는 next-word pretraining이 유창한 문장의 분포를 근사하며, 희소하거나 임의적인 사실에는 true/false 표지가 없고, 정확도만 채점하는 평가가 불확실할 때의 추측을 유리하게 만들 수 있다는 구조적 설명을 제시합니다. 이는 하나의 연구 관점입니다. 훈련 자료의 품질도 원인이 될 수 있으며, 지식 기반 대화 benchmark의 응답 자체에 환각이 많이 포함됐다고 보고한 별도 연구도 있습니다. 따라서 교재에서는 “환각의 단일 원인”이라고 단정하지 않고, 학습 자료·질문 정보·모델·sampling·평가 기준을 함께 확인할 변수로 둡니다.

### 1차 연구·원문 근거

- [Chroma Research: Context Rot](https://www.trychroma.com/research/context-rot) — 2025년 Chroma의 기술 보고서입니다. 긴 입력에서 distractor, 구조, focused/full prompt 조건을 비교합니다. 공급업체 연구이므로 independent replication이 아니라 원 연구의 조건과 결론으로만 인용합니다.
- [Liu et al., *Lost in the Middle*](https://arxiv.org/abs/2307.03172) — 2023년 long-context position 연구입니다. 관련 정보가 중간에 있을 때의 성능 저하와 평가 방법을 제시합니다.
- [Vaswani et al., *Attention Is All You Need*](https://arxiv.org/abs/1706.03762) — 2017년 Transformer 원 논문입니다. attention 기반 architecture의 역사·직관을 위한 1차 출처입니다.
- [Kalai et al., *Why Language Models Hallucinate*](https://openai.com/index/why-language-models-hallucinate/) 및 [원문 PDF](https://cdn.openai.com/pdf/d04913be-3f6f-4d2b-b283-ff432ef4aaa5/why-language-models-hallucinate.pdf) — 2025년 next-word prediction과 accuracy-only 평가의 추측 유인을 분석한 연구입니다.
- [Dziri et al., *On the Origin of Hallucinations in Conversational Models*](https://aclanthology.org/2022.naacl-main.387/) — 2022년 knowledge-grounded conversation benchmark와 훈련 자료 품질을 분석한 ACL 연구입니다.

## 작성 전 확인 필요 항목

1. Ch3 격리 실습 환경에 `git-filter-repo`를 설치하고, 설치 버전과 이력 삭제 검증 결과를 기록합니다. 현재 명령은 없습니다.
2. Ch5 multilingual 모델(약 471MB weights, Hub 전체 표시 용량은 export 포함 더 큼)과 Qwen2.5-0.5B-Instruct(약 988MB)를 실제로 내려받을 네트워크·디스크 여유를 확인합니다.
3. 본문에 넣을 token 수·cosine score·temperature별 출력은 이 메모의 예시값이 아니라 새 커널의 실제 출력으로 교체합니다.
