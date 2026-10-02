# 02절 흔들림 확인 (노트북 밖, 2026-09-25)

규격 §2-7 10번 끝 · 챕터 리드 결정(인계 「§01 → §02」 5항). 노트북을 쓰기 **전에** 세 모드를 함께 받는 실행과 값 바꿔 보기 후보(모드 `messages`를 뺀 실행)를 노트북 밖에서 **5번씩** 봅니다. 키는 루트 `.env`에서만 읽고 출력하지 않습니다. 스크립트 `qa/upgrade/probe/probe02.py`, 기록 `qa/upgrade/probe/probe-02-{M3,M2}.jsonl`(기기 `/tmp/ch25-02/probe/`의 사본).

## 0. 실행 전에 적은 입력과 판단 규칙 (2026-09-25T17:58Z, 첫 요청 전에 적음)

공통(노트북과 같은 코드로 씀):

- 모델 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` 객체(규격 §3, 과정 표준 셀).
- 상태 형식 `AnswerState`(칸 `question`·`answer`, 규칙 없음 — 01 `DraftState`와 칸이 달라 새 이름).
- 지시 글 `system_text` = 「배송 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요.」
- 노드 `write_answer` 하나: `writer = get_stream_writer()` → `writer({"stage": "before_model", "progress": 30})` → `model.invoke([("system", system_text), ("user", state["question"])])` → `writer({"stage": "after_model", "progress": 100})` → `{"answer": response.text}`. 그래프 `START → write_answer → END`, 체크포인터 없음(설정 `None`).
- 입력 하나(01절 소재 「배송 문의」를 이음): `{"question": "주문한 책이 아직 오지 않았어요. 언제 받을 수 있나요?", "answer": ""}`. 결과를 보고 질문·지시 글·진행 값을 바꾸지 않습니다.
- **M3**(노트북 본 실행): `stream_mode=["messages", "updates", "custom"]` 한 실행, 사건을 목록에 모음(01 `collect_events`와 같은 모양).
- **M2**(값 바꿔 보기 후보): `stream_mode=["updates", "custom"]`. 이 실행에만 평범한 콜백(스트리밍 콜백이 아닌 `BaseCallbackHandler`)을 설정 `{"callbacks": [...]}`로 붙여 `on_llm_new_token` 횟수를 셈 — 설치판 `_should_stream`(langchain-core `chat_models.py` 549행)이 스트리밍 요청을 보내지 않으면 0이어야 함. 이 콜백은 노트북에 넣지 않습니다.

회차마다 기록(M3): 시각 · 사건 수 · 모드별 수 · 같은 모드가 이어진 것을 한 번으로 줄인 모드 차례 · custom 값 차례 · custom·updates가 나온 자리 · updates 키(노드 이름)와 그 안 칸 이름 · messages 사건마다 자료 모양(튜플 길이)·청크 자료형·`metadata` 자료형 · 첫 청크 `metadata`의 키 목록(정렬)과 모든 청크에서 키 목록이 같은지 · `langgraph_node`·`langgraph_step`·`langgraph_triggers`·`langgraph_path`·`ls_provider`·`ls_model_name`·`ls_model_type`·`ls_temperature` 값(청크 전체에서 모은 서로 다른 값) · 청크 수 · 글자가 든 청크 수 · 글자가 없는 청크의 자리(청크 차례, 1부터)와 그 청크의 끝난 이유 칸·사용량 여부·`chunk_position` · 사용량이 든 청크 수 · 청크 `id` 서로 다른 값 수 · 이어 붙인 글 == updates의 답 글 · 답 글과 글자 수 · 청크를 `+`로 합친 객체의 사용량(입력·출력)·끝난 이유·모델 이름.
회차마다 기록(M2): 사건 수 · 모드별 수 · 줄인 모드 차례 · custom 값 · `on_llm_new_token` 횟수 · 답 글자 수.

판단 규칙(결론에 쓸 수 있는 관찰):

- **결정적 후보 — 5번 모두 같아야 결론·그림에 씀**: M3 줄인 모드 차례 `['custom', 'messages', 'custom', 'updates']` · updates 1 · custom 2(값 30 → 100) · custom 첫 자리 1 · updates가 맨 끝 자리 · 모든 청크의 `langgraph_node`가 `write_answer` 하나 · 청크 자료형이 모두 `AIMessageChunk` · 이어 붙인 글 == 답 글 `True`(같은 실행 안에서 코드가 판정) · M2 줄인 모드 차례 `['custom', 'updates']`·messages 0.
- **5번 모두 같으면 결과 읽기 첫 단락에 둘 수 있으나 결론·그림에는 넣지 않는 값**: `metadata` 키 목록 · `langgraph_step` · `ls_*` 값 · 글자가 없는 청크 수와 자리 모양(첫 청크 + 끝 셋 같은 모양) · 사용량이 든 청크 수 · 입력 토큰 — 라이브러리·서비스 쪽 모양이라 노트북 새 커널 두 번에서도 같을 때만 첫 단락에, 그 밖은 둘째 단락.
- **흔들리는 값 — 결론·그림·정리·복습에 쓰지 않음**(결과 읽기 둘째 단락·표·「확인할 점」에 「이번 실행에서는」·「교재 출력에서는」): 청크 수·글자가 든 청크 수·custom 둘째 자리·updates 자리·사건 수·답 글·글자 수·출력 토큰(옛 기록 71·73·88로 이미 흔들림).
- 결정적 후보 가운데 하나라도 다르면: **입력을 그대로 두고** 그 값은 둘째 단락·b7로 내리며, 노트북 결과가 다르면 사실대로 두고 원래 값일 때를 「…이면 …이 됩니다」 꼴로 한 문장. 원하는 값이 나올 때까지 다시 돌리지 않습니다.
- M2의 `on_llm_new_token` 횟수가 5번 모두 0이면 b7에 「모드 `messages`를 고르지 않은 실행에서는 노드 안 `invoke`가 스트리밍 요청을 보내지 않았다」를 설치판 소스(549~585행·1969행)와 이 확인으로 적고, 「노트북에서는 요청 종류를 확인하지 않았습니다」를 붙임. 하나라도 0이 아니면 그 문장을 쓰지 않고 03 인계에 적음.
- 요청 수: M3 5 + M2 5 = **10번**(각 요청 1번). 더 보내지 않습니다.

## 1. 흔들림 확인 결과 (`probe02.py M3 5` · `M2 5`, 기록 `probe/probe-02-{M3,M2}.jsonl`)

### M3 — 세 모드 한 실행 (17:58:06Z~17:58:12Z)

| 회차 | 사건 수 | messages | 글자가 든 청크 | custom 자리 | updates 자리 | 입력·출력 토큰 | 답 글자 수 |
|---|---|---|---|---|---|---|---|
| 1 | 44 | 41 | 37 | [1, 43] | [44] | 47 · 41 | 68 |
| 2 | 44 | 41 | 37 | [1, 43] | [44] | 47 · 41 | 68 |
| 3 | 53 | 50 | 46 | [1, 52] | [53] | 47 · 50 | 86 |
| 4 | 37 | 34 | 30 | [1, 36] | [37] | 47 · 34 | 56 |
| 5 | 44 | 41 | 37 | [1, 43] | [44] | 47 · 41 | 68 |

- **결정적 후보 5/5 같음**: 줄인 모드 차례 `['custom', 'messages', 'custom', 'updates']` · updates 1 · custom 2(값 `{'stage': 'before_model', 'progress': 30}` → `{'stage': 'after_model', 'progress': 100}`) · custom 첫 자리 1 · updates가 맨 끝 자리 · updates 키 `['write_answer']`·그 안 칸 `['answer']` · messages 자료 모양 `(AIMessageChunk, dict)` 둘짜리 튜플 · 모든 청크의 `langgraph_node` = `write_answer` 하나 · 이어 붙인 글 == 답 글 `True`.
- **첫 단락 후보 5/5 같음**: `metadata` 키 열둘(정렬 `checkpoint_ns`·`langgraph_checkpoint_ns`·`langgraph_node`·`langgraph_path`·`langgraph_step`·`langgraph_triggers`·`lc_versions`·`ls_integration`·`ls_model_name`·`ls_model_type`·`ls_provider`·`ls_temperature`), 모든 청크에서 키 목록 같음 · `langgraph_step` 1 · `langgraph_triggers` `('branch:to:write_answer',)` · `langgraph_path` `('__pregel_pull', 'write_answer')` · `ls_provider` `openai` · `ls_model_name` `gpt-5.4-mini` · `ls_model_type` `chat` · `ls_temperature` 0.0 · `checkpoint_ns`는 `write_answer:` 뒤에 실행마다 다른 작업 아이디(출력하지 않음) · 글자가 없는 청크 넷 — **첫 청크**(끝난 이유 없음·사용량 없음) + **끝 셋**(끝에서 셋째 끝난 이유 `stop` · 끝에서 둘째 사용량 있음 · 마지막 `chunk_position` `last` — Ch 6 04와 같은 모양) · 사용량 청크 1 · 청크 `id` 한 가지 · 입력 토큰 47 · 합친 객체 `AIMessageChunk`·끝난 이유 `stop`·모델 `gpt-5.4-mini-2026-03-17`.
- **흔들린 값**: messages 사건 수 41·41·50·34·41(옛 기록 71·73·88과 함께 — 질문이 달라 범위는 견주지 않음) · 글자가 든 청크 37·37·46·30·37 · 사건 수 · custom 둘째 자리 · updates 자리 · 출력 토큰 · 답 글(다섯 가운데 셋이 같은 글, 한 번은 줄바꿈이 든 두 줄 글) · 글자 수 68·68·86·56·68.
- 참고(결론에 쓰지 않음): 다섯 번 모두 messages 사건 수와 출력 토큰 수가 같았습니다(41·41 등). Ch 6 04 교재 출력은 청크 18·출력 토큰 17로 달랐고, 이 절도 같은 실행 안에서 글자가 든 청크 수(37)와 출력 토큰 수(41)가 다릅니다. 「청크 수 = 토큰 수」로 읽지 않게 본문은 Ch 6 04 문장만 잇습니다.

### M2 — 모드 messages를 뺀 실행 (17:58:20Z~17:58:24Z)

- 5/5: 사건 3 · 줄인 차례 `['custom', 'updates']` · custom 2(30 → 100) · updates 1 · messages 0 · **평범한 콜백의 `on_llm_new_token` 횟수 0**. 답 글자 수 56·69·70·56·83(흔들림).
- 콜백 방법 확인(서비스 요청 없이, 조사 전용 가짜 모델 — 교재에 넣지 않음, `/tmp/ch25-02/probe/counter_check.py`): 같은 평범한 콜백을 붙이면 세 모드 실행에서 모델 시작 1·`on_llm_new_token` 9, 두 모드 실행에서 모델 시작 1·`on_llm_new_token` 0 → 콜백이 노드 안 모델 실행까지 붙고, messages를 고를 때만 스트리밍 경로로 간다는 뜻.

### 판단

- 결정적 후보는 모두 판단 규칙의 「5번 모두 같음」 → **입력 그대로**, 차례·updates 1·custom 2·`langgraph_node`·이어 붙인 글 == 답 글을 결론·그림에 씀.
- messages 사건 수·글자가 든 청크 수·출력 토큰·답 글은 결과 읽기 둘째 단락·b6 표·「확인할 점」에만 「이번 실행에서는」·「교재 출력에서는」.
- M2 → b7에 「모드 `messages`를 고르지 않은 실행에서는 노드 안 `invoke`가 스트리밍 요청을 보내지 않았다」(설치판 소스 + 노트북 밖 확인, 노트북에서는 요청 종류를 확인하지 않음). 03 인계에 그대로.
- 요청 **10번**(M3 5 · M2 5), 오류 0. 요금표(2026-09-17, 100만 토큰당 mini 입력 0.75·출력 4.50달러)로 어림하면 요청당 약 0.0002~0.0003달러.

## 마감 주 (2026-09-25, 검토 A-5·A-6)

- 위 §0이 「결과 읽기 첫 단락에 둘 수 있으나 결론·그림에는 넣지 않는 값」으로 정한 `metadata` 키 목록(열둘)·`langgraph_step`(1)이 그림 02-3 라벨과 b6 해석 단락에 들어가 있었습니다. 마감에서 §0 규칙대로 라벨과 b6에서 빼고(라벨은 「첫 스트림 청크의 langgraph_node write_answer」), 두 값은 노트북 6절 결과 읽기에만 남겼습니다(`02-diagnosis.md`·`02-figures.md` 끝 「마감 반영」).
