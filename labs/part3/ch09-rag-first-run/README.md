# Ch 9 RAG 첫 완주와 실험 기록

기본 학습 경로는 `notebooks/`의 01~07절입니다. 01·02절은 제공 PDF(E01) 다섯 쪽을 읽어 문서 청크 8개로 나눕니다. 03~05절은 같은 E01 문서 청크 8개로 검색·생성·실패를 관찰합니다. 06절은 실습 폴더 `config.yaml`을 읽어 디지털 PDF 18건과 Ch11의 개발 질문 Q001로 실제 검색·답변 로그를 만듭니다. 문서가 하나인 절의 결과와 18건 색인의 결과를 직접 비교하지 않습니다. 07절은 챕터 실습으로, 문서 청크 크기를 500자와 300자로 바꿔 같은 질문의 검색·답·검사를 점검표 한 줄로 비교하며 파일은 쓰지 않습니다.

02~07절 노트북은 앞 절과 Ch 8에서 배운 함수를 `notebooks/rag_tools.py`에서 가져오므로, 이 파일을 노트북과 같은 폴더에 그대로 둡니다.

압축 해제한 전체 폴더를 유지하고 VS Code에서 `labs/part3/ch09-rag-first-run` 폴더를 엽니다. 이 챕터 폴더의 터미널에서 다음 명령을 실행합니다.

```bash
uv sync --locked
uv run python --version
```

노트북 커널로 이 챕터의 `.venv`를 선택합니다. 각 절은 새 Python 3.12 커널에서 첫 셀부터 순서대로 실행합니다. 02절은 PDF 읽기·문서 청크 나누기·토큰 세기를 로컬에서 실행합니다. 나머지 절은 임베딩 또는 답변 생성 API를 사용하므로 압축 해제한 최상위 폴더의 `.env`에 `OPENAI_API_KEY`를 준비합니다. 키를 출력하지 않으며 API 사용량에 따른 비용이 발생합니다.

06절의 현재 검색 결과는 `runs/continuity-ch09-search.jsonl`, 실행별 원본은 `runs/continuity/`에 저장합니다. Ch10 08절은 같은 PDF와 Q001에 문서 청크 나누기·임베딩 설정을 적용하고, Ch11 06절은 두 챕터의 실제 검색 로그를 읽어 평가합니다. 06절은 이 폴더의 `config.yaml`, `labs/data/rag-corpus/queries.jsonl`, `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`을 읽습니다. 공용 PDF와 질문은 노트북 폴더 밖의 `labs/data/rag-corpus`와 `labs/part3/ch11-evaluation/data`에 있으므로 노트북만 옮기지 않습니다. 전체 실행 순서와 식별자 대응은 최상위 폴더의 `labs/part3/continuity-guide.md`에서 확인합니다.
