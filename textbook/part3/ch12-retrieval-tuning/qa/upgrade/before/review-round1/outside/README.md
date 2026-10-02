# Ch 12 검색 품질 실습

Python 3.12와 uv를 사용합니다. 노트북은 각각 빈 커널에서 독립 실행되며, 01~02절, 05~06절, 11~12절은 프로젝트 루트 `.env`의 `OPENAI_API_KEY`가 필요합니다. 키 값은 노트북 출력에 표시하지 않습니다.

압축을 푼 폴더에서 다음 명령으로 잠금 파일과 같은 환경을 먼저 준비합니다.

```bash
uv sync --locked --project labs/part3/ch12-retrieval-tuning
```

VS Code에서 `labs/part3/ch12-retrieval-tuning` 폴더를 열고 노트북 커널로 이 폴더의 `.venv`를 선택합니다. 같은 Python 3.12라도 다른 챕터의 환경을 선택하면 필요한 패키지가 다를 수 있습니다.

pgvector 실습은 `pgvector/pgvector:0.8.2-pg17` 이미지로 만든 `hankyung-part3-pgvector` 컨테이너를 사용합니다. 호스트의 `127.0.0.1:55432`에만 포트를 공개하고, 전용 `rag_lab` 데이터베이스의 `ch12_core_*` 테이블만 변경합니다. 연결 문자열은 `postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab`입니다. 이 암호는 로컬 수업 전용이며 다른 환경에서 사용하지 않습니다.

```bash
docker run --name hankyung-part3-pgvector \
  -e POSTGRES_USER=student \
  -e POSTGRES_PASSWORD=local-practice-only \
  -e POSTGRES_DB=rag_lab \
  -p 127.0.0.1:55432:5432 \
  -d pgvector/pgvector:0.8.2-pg17
```

실습 후 `docker stop hankyung-part3-pgvector`로 중지합니다. 같은 데이터를 다시 사용할 때는 `docker start hankyung-part3-pgvector`로 시작합니다.

07~08절과 12절은 로컬 CrossEncoder 모델을 사용합니다. 첫 실행에서는 모델 파일을 내려받으므로 인터넷 연결과 저장 공간이 필요합니다. 다운로드 시간과 추론 시간은 구분해서 읽습니다. 11절의 질문 재작성과 12절의 통합 예제는 실제 모델 API를 호출하므로 사용량에 따른 비용이 발생합니다.

전반은 검색 원리를 분리해 관찰하는 교육용 문서 12개와 질문 8개를 사용합니다. 07절부터는 제공 PDF 6건에서 만든 `data/advanced-documents.json`과 Ch11 `evaluation-queries.jsonl` 30문항의 독립 실행용 복제본 `data/advanced-queries.json`을 사용합니다. Ch12 12절은 두 질문 파일의 내용이 같은지 실행 중 확인합니다. 부모 `doc_id`는 `gold_doc_ids`와 비교하고, 자식 `parent_id`는 그 부모를 가리키며 `page`·`chunk_id`는 출처 위치를 담습니다. 전반과 후반은 문서·질문·지표가 달라 수치를 직접 비교하지 않습니다. 압축을 푼 전체 폴더를 유지해야 12절이 `labs/data/rag-corpus/pdf`의 PDF를 직접 읽을 수 있습니다.

`runs/advanced-continuity-experiment-log.jsonl`에는 TF-IDF와 MMR의 개발 설정 36건, `runs/advanced-continuity-test-result.json`에는 선택한 설정의 시험 평가 1건을 기록합니다. 각 실행은 Ch11의 지표 정책과 연결할 수 있도록 질문별 순위·지표와 분할별 집계를 남깁니다. `runs/advanced-continuity-integrated-result.json`은 dense·Kiwi BM25·RRF·CrossEncoder·쪽 본문 선택·답변 생성을 연결한 별도의 개발 질문 1건 스모크 실행입니다. 이 1건은 TF-IDF+MMR 설정 36건의 후속 시험이 아니며, 검색 지표나 생성 답변 품질을 평가하지 않습니다. 생성 평가는 Ch15에서 수행합니다. 개발 질문 15개와 시험 질문 15개를 구분하며, 작은 학습용 자료의 결과를 실제 업무 전체의 품질로 해석하지 않습니다. 기존 `advanced-*` 로그는 수정 전 증거로 보존합니다.

13절은 이 챕터의 실습입니다. 05·06절 순위 합치기와 08절 보고 자리·지표, 12절 답 쓰기를 한 줄기로 잇고 06절 가중치 한 자리만 바꿔 두 번 실행합니다. 개발 질문 두 개만 쓰고 임베딩 3번과 답변 모델 2번을 호출하며, pgvector·CrossEncoder·MMR은 사용하지 않습니다. `runs/`의 기록 파일을 읽지도 쓰지도 않고 결과를 화면에만 출력합니다.

12절 통합 RAG는 앞 임베딩 실습과 같은 `text-embedding-3-small`의 256차원, Ch6·Ch9와 같은 답변 모델 `gpt-5.4-mini`를 사용하며 실제 차원을 로그에 기록합니다. 11절의 `gpt-4.1-mini`는 질문 재작성 과제를 위한 별도 모델입니다. 재작성과 답변 생성은 과제가 다르므로 모델 간 품질 비교로 해석하지 않습니다.
