# 챕터 리드 메모 (마감 때 처리할 것)

## 절 사이 이음새
- **[중] 01절 b8 마지막 문장 대 02절 입력**: 01절은 「02절에서는 질문 하나를 여러 개로 늘려 검색합니다. 이 절이 만든 독립 질문이 그 절의 입력이 됩니다」로 끝나는데, 02절은 01절 독립 질문 대신 자료 질문 `C01`을 썼습니다(01절 질문은 한 번 검색으로도 정답이 첫 자리라 늘린 효과가 안 보임 — 02절 탐색 실행). **마감 때 01절 b8과 노트북 정리 문장을 02절 실제 입력에 맞게 고칠 것**(01절 노트북은 다시 실행하지 말고 `mdpatch.py`로 글만).

## 마감 때 옮기거나 지울 것 (삭제 승인 대상)
- `qa/upgrade/gates-wip-01-01.json` — 01절이 남긴 중복 보고 파일(정본은 `gates-wip-01.json`).
- 옛 그림 `figures/NN-*-flow.{svg,excalidraw,caption.md}` — 본문에서 더는 참조하지 않음(`before/figures/`에 사본 있음).
- 옛 생성기 셋 `_make_sources.py`·`figures/_gen_figures.py`·`labs/part4/ch14-rag-patterns/_make_notebooks.py` — 01절이 `raise SystemExit`으로 막아 둠. 규격 §8대로 `qa/upgrade/before/generators/`로 `mv -n`.

## 실습 폴더
- `labs/part4/ch14-rag-patterns/README.md`가 아직 `gpt-4.1-mini`·비용 문장·「임계값」을 담고 있음 → **마감 때 한 번에** 고칠 것.

## 작업 범위 (사용자 지시 2026-09-19)
- **「14장 까지만 작업해」** — Ch 14 마감까지 하고 멈춥니다. Ch 15 이후는 이번에 손대지 않습니다.
- Ch 15 01절이 Ch 12 기록 때문에 깨져 있는 건(`_author.py` 212행)은 `textbook/qa/upgrade-final-checklist.md`에 그대로 남겨 둡니다.

## 09절이 의도적으로 바꾼 산출 파일
- `labs/part4/ch14-rag-patterns/runs/pattern-comparison.json` — `8b1fd13cd844fcf9…` → `94d10997803eabdc…`(4540 → 4454바이트). 칸을 다시 짜고 `usd`·`ms`·토큰 칸을 뺐습니다. 코드로 읽는 쪽 0건, 묶음 목록 둘에 경로가 이미 있어 고칠 것 없음.
- 나머지 보호 파일 19개는 그대로입니다.

## 챕터 마감에서 손봐야 할 챕터 밖 자리 (09절 보고)
- `textbook/part4/ch14-rag-patterns/chapter.json` `objectives` — 「임계값」·「노드」·「토큰·실행 시간 비교」가 남아 있음(새 교재와 어긋남).
- `textbook/part4/_build_index.py` 21~22행 ch14 설명 — 「지연·사용량을 비교」가 남아 있음(걸린 시간을 재지 않음).
- `labs/part4/ch14-rag-patterns/README.md` — `gpt-4.1-mini`·비용 문장·「임계값」.
- `labs/part4/ch14-rag-patterns/pyproject.toml` — `numpy`(아홉 절 모두 import 0건이 되었는지 마감에서 확인).
