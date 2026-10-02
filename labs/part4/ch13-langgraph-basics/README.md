# Ch13 LangGraph 기초 실습

각 노트북은 Python 3.12 새 커널에서 첫 셀부터 독립 실행합니다. 노트북의 설치 셀과 `pyproject.toml`은 LangGraph 1.2.11, LangChain 1.4.0을 고정합니다. LangChain 1.4.0이 LangGraph 1.2.11 이상을 요구하므로 함께 설치되는 최신 1.2 계열을 사용합니다.

01절부터 06절까지는 모델을 부르지 않습니다. 모델을 부르는 절은 07절과 08절입니다.

07절은 `labs/part3/ch12-retrieval-tuning/data/advanced-documents.json`과 `runs/advanced-continuity-integrated-result.json`을 읽습니다. 두 파일 모두 읽기만 하고 고치지 않습니다. 통합 기록에서는 질문과 정답 부모 문서 ID만 가져오고 저장된 답은 쓰지 않습니다. Ch 12 문서 청크 175개를 그대로 쓰며 PDF를 다시 읽지 않습니다. 임베딩 `text-embedding-3-small`(`dimensions=256`)과 Kiwi BM25 검색, 순위 합치기, `gpt-5.4-mini` 답 쓰기를 노드 다섯으로 나눠 실제로 실행합니다. 리랭커는 부르지 않습니다. 서비스 요청은 다섯 번(임베딩 3 + 답 모델 2)이고 예상 비용은 미화 0.01달러 아래입니다. 실행 전 프로젝트 루트 `.env`에 `OPENAI_API_KEY`가 있어야 합니다. 키 값은 출력하지 않습니다.

08절은 이 챕터의 실습입니다. 07절과 같은 Ch 12 문서 파일 하나만 읽고 새로 쓰는 파일은 없습니다. 01절 노드 `normalize`와 07절 검색 부품, 06절 `Command` 이동, 04절 메시지 칸을 노드 다섯짜리 그래프 하나에 함께 붙입니다. 검색이 낸 낱말 겹침 점수를 설정 칸의 기준값과 견줘 답을 쓸지 되물을지 노드가 정합니다. 기준값을 `5.0`과 `9.0`으로 두어 두 번 실행합니다. 서비스 요청은 네 번(임베딩 3 + 답 모델 1)이고 예상 비용은 미화 0.01달러 아래입니다.

```bash
uv run --project labs/part4/ch13-langgraph-basics \
  --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip \
  python textbook/_notebook/execute.py \
  labs/part4/ch13-langgraph-basics/notebooks/*.ipynb --cwd "$(pwd)"
```
