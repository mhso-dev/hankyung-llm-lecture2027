# Ch29 공식 문서 조사

> **개선 전 판(2026-09-11)** — 이 조사는 품질 개선 전 판이고, 챕터 마감(2026-09-29)에서 내용은 고치지 않고 이 표시만 더했습니다. 「LLM judge」·「결정적」·「매칭」 같은 옛 말과 옛 판 기준 서술이 남아 있을 수 있습니다. 지금 교재가 확인한 문서 사실과 확인일(2026-09-29)은 각 절 `_src` b10과 `qa/upgrade/NN-diagnosis.md`·`chapter-summary.md` §14에 있습니다.

- 확인일: 2026-09-11
- 기준: Python 3.12, agentevals 0.0.9, langchain 1.4.0

## 확인한 내용

- 공식 문서는 Agent 평가를 Final Response, Single step, Trajectory로 나눕니다. 세 평가는 함께 사용할 수 있습니다.
- `strict`는 같은 메시지 구조와 도구 호출 순서를, `unordered`는 같은 도구 호출을 순서와 무관하게 검사합니다.
- `subset`은 실제 호출이 기준 호출 범위를 넘지 않는지 검사합니다. 필요한 호출을 빠뜨린 궤적도 통과할 수 있습니다.
- `superset`은 실제 호출이 기준의 필수 호출을 모두 포함하는지 검사합니다. 추가 호출은 허용합니다.
- 설치된 agentevals 0.0.9에서 짧은 궤적은 subset 통과·superset 실패, 추가 호출 궤적은 subset 실패·superset 통과였습니다.
- LLM judge는 기준 궤적 없이도 사용할 수 있고 기준 궤적을 함께 제공할 수도 있습니다.

## 커리큘럼 표현 보정

커리큘럼의 `subset(효율)`은 API 의미를 충분히 설명하지 않습니다. subset은 실제 호출이 기준 호출의 부분집합인지 판정할 뿐 필요한 동작의 누락을 잡지 못합니다. 본문에서는 허용 범위 검사로 설명하고 효율은 스텝 수·호출 수·비용으로 따로 측정했습니다. `superset(필수 동작)`은 필수 호출을 포함하는지 확인하지만 추가 호출을 허용한다는 조건을 함께 적었습니다.

## 출처

- https://docs.langchain.com/oss/python/langchain/test/evals
- https://docs.langchain.com/langsmith/evaluation-approaches
- https://docs.langchain.com/langsmith/trajectory-evals
- https://github.com/langchain-ai/agentevals

## 확인 필요 항목

- 2026-09-11 PyPI에서 설치 가능한 agentevals는 0.0.9였습니다. 이후 GitHub 변경은 기준 버전에 포함하지 않았습니다.
- Excalidraw MCP는 이 세션에 없었습니다. 기존 `_figure.py`로 SVG와 Excalidraw JSON을 생성했습니다.
