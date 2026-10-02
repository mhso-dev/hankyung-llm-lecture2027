# Ch 9 RAG 첫 완주와 실험 기록

기본 학습 경로는 `notebooks/`의 01~06절입니다. 01·02절은 제공 PDF를 읽고, 03~05절은 검색·생성·실패의 원리를 관찰하는 짧은 문서를 셀 안에서 준비합니다. 06절은 작은 설정 비교 뒤에 디지털 PDF 18건과 Ch11의 개발 질문 Q001로 실제 검색·답변 로그를 만듭니다. 문서와 질문이 다른 작은 예제의 점수를 PDF 기준선과 직접 비교하지 않습니다.

압축 해제한 전체 폴더를 유지하고 VS Code에서 `labs/part3/ch09-rag-first-run` 폴더를 엽니다. 이 챕터 폴더의 터미널에서 다음 명령을 실행합니다.

```bash
uv sync --locked
uv run python --version
```

노트북 커널로 이 챕터의 `.venv`를 선택합니다. 각 절은 새 Python 3.12 커널에서 첫 셀부터 순서대로 실행합니다. 02절은 PDF 로딩·청킹·토큰 관찰을 로컬에서 실행합니다. 나머지 절은 임베딩 또는 답변 생성 API를 사용하므로 압축 해제한 최상위 폴더의 `.env`에 `OPENAI_API_KEY`를 준비합니다. 키를 출력하지 않으며 API 사용량에 따른 비용이 발생합니다.

06절의 현재 검색 결과는 `runs/continuity-ch09-search.jsonl`, 실행별 원본은 `runs/continuity/`에 저장합니다. Ch10 08절은 같은 PDF와 Q001에 청킹·임베딩 설정을 적용하고, Ch11 06절은 두 챕터의 실제 검색 로그를 읽어 평가합니다. 공용 PDF와 질문은 노트북 폴더 밖의 `labs/data/rag-corpus`와 `labs/part3/ch11-evaluation/data`에 있으므로 노트북만 옮기지 않습니다. 전체 실행 순서와 식별자 대응은 최상위 폴더의 `labs/part3/continuity-guide.md`에서 확인합니다.
