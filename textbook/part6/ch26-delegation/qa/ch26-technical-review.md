# Ch26 독립 기술 검토

> **개선 전 판(2026-09-11)** — 개선 전 노트북 넷·원고에 대한 옛 기술 검토이고, 마감(2026-09-28)에서 내용은 고치지 않고 이 표시만 더했습니다. 지금 판의 검토는 `qa/upgrade/review-round1-A.md`(01~02·공통)·`review-round1-B.md`(03~05)와 반영 기록 `qa/upgrade/chapter-summary.md` §17입니다.

- 검토일: 2026-09-11
- 범위: 네 개 노트북의 코드·저장 출력, `_src/` 원고, 도식 캡션, 공식 문서 조사 기록
- 기준: Python 3.12.13, LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11, `gpt-5.4-mini`

## 판정

수정 후 통과입니다. 노트북 코드와 저장 출력은 수정하지 않았습니다. 실제 출력의 제어 흐름, 호출 수, 토큰·비용 계산, 종료 조건이 원고에 맞습니다.

## 확인한 근거

- 01은 `create_agent`의 메시지 `tool_calls`와 도구 함수의 `calls`에 모두 `policy_specialist` 한 번이 남습니다. 원고에서 존재하지 않는 `main_agent` 호출 기록 언급을 제거했습니다. Subagent는 중앙 에이전트가 도구로 호출하고 결과를 중앙 에이전트로 돌려주는 패턴이라는 공식 설명과도 일치합니다. <https://docs.langchain.com/oss/python/langchain/multi-agent/subagents>
- 02는 같은 `thread_id`의 체크포인터 상태에서 `active_agent`가 `refund_agent`로 유지되고, 주문 번호 `A-102`와 담당자 상태를 함께 검사해 실습의 완료를 판정합니다. 실제 서비스의 다중 에이전트 handoff는 `active_agent` 갱신과 종료 분기를 함께 둔다는 공식 예와 방향이 같습니다. <https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs>
- 03은 구조화 출력의 `destinations`를 직접 읽어 `policy`, `shipping`만 실행합니다. `ThreadPoolExecutor`는 선택한 두 작업을 병렬로 실행하지만, 결과 출력 순서는 입력 순서로 정렬됩니다. 공식 Router 문서도 단일 경로에는 `Command`, 병렬 fan-out에는 `Send`를 구분합니다. <https://docs.langchain.com/oss/python/langchain/multi-agent/router>
- 04는 `create_agent`의 도구 선택, `active_agent`를 읽는 조건부 edge, 구조화 `destinations`라는 세 실제 분기 근거를 사용합니다. `sub_done`, `handoff_done`, `router_done`은 각각 실제 반환값·상태에서 계산하고 마지막 셀에서 모두 검사합니다. 고정 trace나 고정 분류 결과로 비교를 흉내 내지 않습니다.
- 비용 계산은 `input_tokens - cache_read`에 일반 입력 단가, `cache_read`에 캐시 입력 단가, `output_tokens`에 출력 단가를 적용합니다. 저장 출력의 캐시 입력은 세 구조 모두 0개이므로, 이번 비용에는 캐시 할인액이 포함되지 않습니다. GPT-5.4 Mini의 확인일 기준 공식 단가는 100만 토큰당 일반 입력 0.75달러, 캐시 입력 0.075달러, 출력 4.50달러입니다. <https://developers.openai.com/api/docs/models/gpt-5.4-mini>

## 원고 교정

- 01 실행 예제의 `main_agent` 기록 주장을 실제 `calls`·`tool_calls` 관찰으로 교정했습니다.
- 04 실행 예제의 존재하지 않는 `policy_tool.invoke`와 요청 핵심어 분기 주장을, `create_agent` 도구 선택·도구 내부 `measured_call`·구조화 `destinations` 읽기로 교정했습니다.
- 04 결과 해석에 실제 캐시 입력이 0개였음을 명시했습니다.

## 보존 해시

- 노트북 SHA-256: `01 c7e4c146…`, `02 501a0e9c…`, `03 2e6293f7…`, `04 d33cb32c…`
- SVG·Excalidraw·도식 생성기 SHA-256: 언어 감사 전후 동일. 전체 목록은 `ch26-code-output-preservation.sha256`에 보관했습니다.

## 확인 필요 항목

- 비용·호출 수는 한 요청의 실측입니다. 운영값에는 질문 집합, 반복 측정, 실패율, 사용자 수정 횟수와 캐시 적중률이 필요합니다.
- 02의 완료 조건은 학습용 주문 번호와 담당자 상태입니다. 서비스에서는 주문 조회 성공, 정책 적합성, 사용자 확인을 추가해야 합니다.
