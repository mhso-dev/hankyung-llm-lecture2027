# 02 메시지와 제공자 전환 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 02-5 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 카드 한 벌이 메시지 목록, 우편함이 모델, 색과 모양이 제공자, 자물쇠가 준비되지 않은 키입니다. | 값 없음(비유). 같은 카드 한 벌 × 3, 같은 모양 초록 우편함 2(크고 작음), 자물쇠 걸린 회색 우편함 1 | — |
| 02-1 | 4 핵심 개념 · 메시지 객체와 역할 이름 (노트북 「오늘 볼 그림」) | Mermaid flowchart LR | 튜플과 메시지 객체는 같은 역할의 다른 표기이고, 두 호출의 입력 토큰 수는 33으로 같았습니다. | [2절] `system | 한 문장의 한국어로 답하세요.`, [3절] `SystemMessage | system | …`·`HumanMessage | human | …`, [준비] `모델 이름: gpt-5.4-mini`, [4절] `입력 토큰 수: 33` ×2·`두 호출의 입력 토큰 수가 같은가: True` | 넣은 목록 tool 초록, invoke 안 변환 단계 flow 파랑, 실행한 모델 model 보라, 출력으로 확인한 값 measure 노랑 |
| 02-2 | 5 실행 예제 · 모델 이름을 하나씩 바꾸면 | Mermaid flowchart TB(칸 세 개, 칸 안 LR) | 5절은 같은 코드로 답을 받았고, 6절은 인자 한 줄을 지워야 모델 객체가 만들어졌습니다. | [5절] `모델 객체 종류: ChatOpenAI`·`모델 이름: gpt-5.4-nano`·`출력 토큰 수: 44`, [6절] `1 validation error for ChatAnthropic`·`Input should be 'max', 'xhigh', 'high', 'medium' or 'low'`, `모델 객체 종류: ChatAnthropic`·`ANTHROPIC_API_KEY 설정 여부: False` | 넘긴 이름·인자 tool 초록, 실행한 모델 model 보라, 확인한 값 measure 노랑, 받아 출력한 `ValidationError`도 measure 노랑(검토 02-1) |
| 02-3 | 5 실행 예제 · 멈춘 자리가 다른 세 경우 | Mermaid sequenceDiagram(`messageAlign: left`) | 세 경우는 요청이 나갔는지가 달라서 기록도 다르게 합니다. | [6절] `오류 종류: ValidationError`, `ChatAnthropic`·`False`, [7절] `Error code: 404`·`model_not_found`·`오류 종류: OpenAIModelNotFoundError` | 실선 요청·점선 응답, 메모 노랑(각 경우가 끝난 뒤) |
| 02-4 | 6 실험 결과 해석 | Mermaid flowchart TB(상태별 칸 세 개, 보이지 않는 연결) | 키 없음 두 줄은 실행하지 않았다는 기록이고, 출력 토큰 수는 0이 아니라 None입니다. | [8절] 기록표 다섯 줄(39·44·None×3), [9절] `상태별 줄 수: {'실행함': 2, '요청 오류': 1, '키 없음': 2}` | 확인한 결과 measure 노랑(요청 오류 포함), 요청을 보내지 않은 설정 회색 |

색 규칙(01절 선례 이어받음): 넣은 문장·설정은 초록, 코드·라이브러리 단계는 파랑, 실행한 서비스 모델은 보라, 출력으로 확인한 값은 노랑, 실행하지 않은 설정은 회색입니다. 같은 요소(`gpt-5.4-mini`·`gpt-5.4-nano` 모델)는 보라, 확인한 모델 객체 종류(`ChatOpenAI`·`ChatAnthropic`)는 노랑으로 절 안에서 같습니다.
빨강은 0장입니다. 처음에는 02-2 가운데 칸 `ValidationError`를 빨강으로 칠했습니다(받지 않으면 멈추는 결함, 01-4 선례). 챕터 검토 02-1(2026-09-17)에서 노랑으로 바꿨습니다. 02는 experiment 형식이고 6절은 값 바꿔 보기라 Before가 아니며, 노트북이 `try/except ValidationError`로 받아 출력한 오류이기 때문입니다(규격 §5-3, 과정 요약 §8 Ch 5 `ValueError` 선례). 01-4 Before의 빨강은 그대로입니다.
7절 `OpenAIModelNotFoundError`는 코드가 받아 기록표의 상태 「요청 오류」로 적은 오류라 02-4에서 노랑입니다(규격 §5-3 「잡아서 기록한 오류」). 02-3 sequenceDiagram은 색 대신 메모(노랑)로만 표시합니다.
02-3은 처음 viewBox 폭 932로 868을 넘어(자기 호출 화살표 라벨·왼쪽 메모), 키 확인을 자기 호출 대신 「추론 설정을 빼고 만들기 → ChatAnthropic」 메시지와 메모로 바꿔 833으로 줄였습니다. 02-2·02-4는 `claude-haiku-4-` 줄바꿈이 어색해 `anthropic:<br>` 식으로 직접 줄을 나눴습니다.
