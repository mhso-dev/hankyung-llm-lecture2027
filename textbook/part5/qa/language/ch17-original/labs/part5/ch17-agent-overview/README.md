# Ch 17 Agent 개요 실습

다섯 노트북은 Python 3.12 새 커널에서 각각 독립 실행됩니다. 외부 API를 호출하거나 자율 도구 에이전트를 구현하지 않습니다. 교육용 고정 사례로 워크플로우와 에이전트의 경계, 워크플로우 적합 조건, 정지 조건, 비용·지연·경로 지표를 분석합니다.

마지막 노트북은 공식 저장소가 공개한 SWE-agent와 mini-SWE-agent 실제 실행 궤적 두 건의 추출본 `data/public-trace-extracts.json`을 읽습니다. 추출본에는 원본 커밋, 원문 URL, SHA-256, MIT 라이선스, 사건 순서를 기록했습니다. 이 컴퓨터에서 두 제품을 다시 실행한 로그는 아닙니다. `data/product-trace-evidence.json`의 Codex·Claude Code·Deep Research 항목은 공식 문서가 공개한 사건 유형과 제한 인터페이스만 정리한 보조 자료입니다.

`data/autonomy-diagnostic-example.json`은 중간 프로젝트 규정 RAG의 작성 예시입니다. `data/autonomy-diagnostic-sheet.csv`는 프로젝트마다 복사해 사용할 빈 진단표입니다. 예시 결론은 ‘워크플로우 유지’이며, Ch 20에서 고정 분기와 모델 분기를 실제로 비교한 뒤 갱신합니다.

```bash
uv run --project labs/part5/ch17-agent-overview \
  --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip \
  python textbook/_notebook/execute.py \
  labs/part5/ch17-agent-overview/notebooks/*.ipynb
```
