# Ch 10 문서 처리 실습

Python 3.12와 uv를 사용합니다. 예제는 `ex01`부터 `ex08`까지 순서대로 실행합니다.

```bash
uv sync
uv run python examples/ex01_metadata.py
uv run python examples/ex02_pdf_tables.py
uv run python examples/ex03_other_loaders.py
uv run python examples/ex04_hwpx.py
uv run python examples/ex05_chunking.py
uv run python examples/ex06_semantic.py
uv run python examples/ex07_embedding_cache.py
uv run python examples/ex08_experiment.py
```

`ex08`의 기본 실행은 API 호출 없이 교육용 특징 해시 벡터를 사용합니다. 이 벡터는 파이프라인과 캐시를 검증할 뿐 모델 품질을 나타내지 않습니다. 실제 OpenAI 후보 비교는 먼저 출력되는 비용 예상치와 단가 가정을 확인한 뒤 `--backend openai`로 실행합니다. 프로젝트 루트 `.env`의 `OPENAI_API_KEY`만 읽으며 키를 출력하지 않습니다. 두 후보는 공식 오픈 모델 선정 전의 임시 비교 대상입니다.

교재의 06~08절 노트북은 `langchain-openai==1.6.0`의 `OpenAIEmbeddings`를 사용합니다. 문서는 `embed_documents()`, 질문은 `embed_query()`로 변환합니다. JSONL의 `local_token_estimate`는 `tiktoken`으로 센 입력 규모 추정치이며 공급자가 반환한 실제 사용량이 아닙니다.

현재 저장소에는 디지털 PDF 18건이 있습니다. 100건 실습은 파일 내용을 해시하여 중복을 제외한 문서가 100건인지 사전 점검합니다. 같은 파일을 복제해서 100건으로 세지 않습니다.

검증 명령은 다음과 같습니다.

```bash
uv run ruff check .
uv run pytest
uv run python -m compileall document_processing.py experiment.py examples tests
```
