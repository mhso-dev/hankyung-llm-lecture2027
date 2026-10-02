# Ch 10 문서 처리 실습

Python 3.12와 uv를 사용합니다. 압축 해제한 전체 폴더는 유지하고, VS Code에서 `labs/part3/ch10-document-processing` 폴더를 엽니다. 이 챕터 폴더의 터미널에서 다음 명령을 실행합니다.

```bash
uv sync --locked
uv run python --version
```

노트북 커널로 이 챕터의 `.venv`를 선택합니다. 학생 실습의 기준 파일은 `notebooks/`의 01~08절 Jupyter Notebook입니다. 각 절을 새 커널에서 준비 셀부터 순서대로 실행합니다. 01~05절은 제공 자료로 문서 형식과 청킹을 확인합니다. 06~08절은 프로젝트 최상위 `.env`의 `OPENAI_API_KEY`가 필요하며 실제 임베딩 API 사용량에 따른 비용이 발생합니다. 키를 출력하지 않습니다.

06·08절은 설정을 바꾸며 결과를 관찰합니다. 청크 수나 점수의 변화만으로 품질이 좋아졌다고 결론 내리지 않습니다. 06절의 시맨틱 청킹과 07절의 캐시는 `langchain-openai==1.6.0`의 `OpenAIEmbeddings`를 사용하며 문서는 `embed_documents()`, 질문은 `embed_query()`로 변환합니다.

04절의 HWPX는 본문 문자열 추출과 HWP 미지원 분기를 확인하는 최소 표식입니다. 실제 HWPX의 표·문단 구조 보존이나 일반 업무 문서 호환성을 검증한 자료는 아닙니다. 디지털 PDF 18건은 공용 `labs/data/rag-corpus`에 있으며 노트북만 따로 옮기면 읽을 수 없습니다. 자신의 문서 100건이나 외부 상용 파서는 선택 확장으로, 배포 기본 실습에 포함되지 않습니다.

08절은 작은 예제의 여섯 조합 뒤에 같은 조건을 공용 PDF와 Ch11 개발 질문 Q001에 적용합니다. 실제 검색 결과는 `runs/continuity-ch10-indexing.jsonl`, 실행별 원본은 `runs/continuity/`에 보존합니다. JSONL의 `local_token_estimate`는 `tiktoken`으로 센 입력 규모 추정치이며 공급자가 반환한 실제 사용량이 아닙니다. 다음 Ch11 06절은 이 파일과 Ch9 검색 로그를 직접 읽어 검색 지표를 계산합니다. 압축 해제한 최상위 폴더의 `labs/part3/continuity-guide.md`에서 전달 순서와 비교 범위를 확인합니다.
