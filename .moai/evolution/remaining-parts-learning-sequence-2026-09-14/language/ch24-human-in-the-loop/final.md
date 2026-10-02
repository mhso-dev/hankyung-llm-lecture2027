textbook/part6/ch24-human-in-the-loop/_src/01-interrupt-승인-게이트.html

1학습 목표
interrupt와 Command(resume=)가 승인 값을 주고받는 과정을 설명할 수 있습니다.
승인 요청 전후의 부작용 순서가 파일 기록에 미치는 차이를 확인할 수 있습니다.
interrupt 앞의 외부 쓰기에 멱등성이 필요한 이유를 설명할 수 있습니다.
2이 내용을 배우는 이유
결제·배포·삭제처럼 되돌리기 어려운 동작은 모델의 판단만으로 실행하지 않고 사람이 요청 내용을 확인해야 합니다.
이 실습은 같은 거절 값을 unsafe와 safe 그래프에 전달합니다. unsafe는 transfer-local을 두 번 기록하고, safe는 파일을 만들지 않아 승인 질문의 위치가 결과를 바꾸는지를 확인합니다.
3앞에서 배운 내용
Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다. 이번 절은 실행을 시작하기 전에 사람이 요청을 검토하는 경계를 추가합니다. 체크포인터는 InMemorySaver를 사용해 승인 흐름 자체에 집중합니다.
4핵심 개념
구체적인 상황
로컬 파일 쓰기를 송금이나 배포 같은 되돌리기 어려운 작업이라고 가정합니다. 거절할 수 있는 화면을 보여 주더라도 실제 쓰기가 이미 끝난 뒤라면 승인 게이트의 목적을 달성하지 못합니다. 코드 순서가 정책 문구만큼 중요합니다.
정의
interrupt()는 노드 실행을 중단합니다. 그래프 호출 결과는 JSON으로 직렬화할 수 있는 payload를 __interrupt__에 담아 호출자에게 보여 주며, 체크포인터는 같은 thread_id에서 재개할 상태를 보관합니다.
Command(resume=value)를 같은 thread_id로 전달하면 value가 interrupt()의 반환값이 됩니다. 재개할 때 노드는 처음부터 실행되므로 interrupt 앞 코드는 다시 실행됩니다.
코드를 읽는 순서
interrupt(payload)는 노드 실행을 멈추고 payload를 호출자에게 반환합니다. 이를 사용하려면 상태를 저장할 체크포인터와 재개할 실행을 찾는 thread_id가 필요합니다. 첫 invoke의 결과에는 __interrupt__가 들어 있고, Command(resume=value)로 같은 스레드를 호출하면 그 값이 노드 안 interrupt()의 반환값이 됩니다.
재개는 interrupt 다음 줄에서 프로세스를 그대로 계속하는 방식이 아닙니다. 런타임은 노드를 처음부터 다시 실행하며 저장된 재개 값을 같은 interrupt 호출에 전달합니다. 따라서 interrupt 앞의 write_effect는 첫 실행과 재개에서 두 번 실행될 수 있습니다. 승인 게이트는 부작용보다 앞에 두어야 거절이 실제 실행을 막습니다.
도식 읽기
‘요청 상태 저장’ 뒤 ‘interrupt 승인 질문’이 나오고 사람이 승인 또는 거절을 선택합니다. ‘승인일 때만 로컬 쓰기’는 safe_node의 if 문과 대응합니다. Before는 마지막 두 상자의 순서가 뒤바뀐 비교 경로입니다.
5실행 예제
effect_path는 노트북 폴더와 프로젝트 루트 어디에서 실행해도 찾을 수 있는 로컬 파일입니다. unsafe_node는 write_effect 뒤 interrupt를 호출합니다. safe_node는 interrupt 반환값이 참일 때만 write_effect를 호출합니다. 두 그래프 모두 False로 재개해 순서만 비교합니다.
확인할 점 — 부작용 뒤에 interrupt를 둔 Before는 거절해도 기록이 남았습니다. interrupt를 먼저 둔 After는 거절 상태를 반환하고 파일을 만들지 않았습니다.
다른 상황과 적용 경계
파일 쓰기는 송금, 배포, 삭제처럼 되돌리기 어려운 동작을 대신한 관찰 가능한 예입니다. 읽기 전용 검색까지 매번 승인받으면 흐름만 느려질 수 있으므로 위험한 도구 이름이나 인자 조건에만 게이트를 두는 편이 적절합니다.
승인 화면을 보여 줬다는 사실만으로 안전하지 않습니다. 외부 동작이 승인 전에 실행됐는지, 재개 때 다시 실행되는지 코드 순서로 확인해야 합니다. safe 경로의 파일 부재는 False가 외부 쓰기 전에 검사됐다는 이번 실습의 증거입니다.
6일부러 실패해 보기
unsafe 경로는 거절 상태인데도 transfer-local이 두 줄 남았습니다. 첫 중단과 재개에서 노드 앞부분이 각각 실행됐기 때문입니다. safe 경로는 rejected를 반환하고 effect 파일이 없습니다. 승인 질문을 외부 쓰기 앞에 둔 효과를 실제 파일로 확인했습니다.
부작용 뒤에 interrupt를 둔 Before는 거절해도 기록이 남았습니다. interrupt를 먼저 둔 After는 거절 상태를 반환하고 파일을 만들지 않았습니다.
7주의할 점과 실무 메모
interrupt를 try/except로 감싸면 런타임의 중단 신호를 일반 오류로 처리할 수 있으므로 공식 규칙을 따릅니다.
payload는 JSON으로 직렬화할 수 있는 요청 ID, 요약, 위험 수준처럼 검토에 필요한 값만 담습니다.
interrupt 앞에 필요한 쓰기가 있다면 재실행돼도 같은 결과를 내도록 멱등하게 만듭니다.
8정리와 다음 절
재개한 노드는 interrupt 앞부터 다시 실행돼 unsafe 경로는 같은 파일 기록을 두 번 남겼습니다.
safe 경로는 거절 값을 먼저 확인해 파일을 만들지 않았습니다.
승인 게이트만으로는 interrupt 앞의 필요한 쓰기를 안전하게 만들 수 없으므로 멱등 처리가 필요합니다.
다음 학습과 이어지는 지점 — 다음 절에서는 Command(resume=) 값이 interrupt()의 반환값이 되는 과정을 확인합니다.
9복습 문제
1. unsafe 경로에서 같은 값이 두 줄 기록된 이유는 무엇인가요?
해설 — 중단 전 한 번 쓰고 재개 시 노드가 처음부터 실행되며 한 번 더 썼기 때문입니다.
2. safe_node에서 False를 전달하면 write_effect가 호출되지 않는 이유는 무엇인가요?
해설 — interrupt 반환값을 확인한 if not approved 분기가 먼저 rejected를 반환하기 때문입니다.
3. interrupt payload에 넣기 알맞은 값은 무엇인가요?
해설 — 요청 ID와 사람이 판단할 요약처럼 JSON 직렬화가 가능하고 검토에 필요한 값입니다.
4. 이 실습이 실제 송금을 실행하지 않는 이유는 무엇인가요?
해설 — 학습용 로컬 부작용으로 승인 순서를 안전하게 관찰하기 위해서입니다.
10참고 자료
LangGraph Persistence 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph Interrupts 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph Time Travel 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph MIT 라이선스 · 확인 2026-09-14

textbook/part6/ch24-human-in-the-loop/_src/02-Command-resume으로-실행-재개.html

1학습 목표
Command(resume=) 값이 interrupt() 반환값으로 전달되는 과정을 설명할 수 있습니다.
허용되지 않은 maybe 값에 오류를 넣어 재질문하는 흐름을 읽을 수 있습니다.
재개 때 thread_id와 interrupt 호출 순서를 유지해야 하는 이유를 설명할 수 있습니다.
2이 내용을 배우는 이유
사람의 응답은 늦게 도착하거나 허용한 형식과 다를 수 있습니다. 중단된 실행을 잃지 않고 값을 검증한 뒤 다시 요청해야 합니다.
실습에서는 maybe를 보낸 뒤 error가 추가된 두 번째 interrupt를 받고, 같은 review-2402 스레드에 approve를 전달해 decision과 종료 상태를 확인합니다.
3앞에서 배운 내용
앞 절에서 interrupt가 실행을 멈추고 Command(resume=False)가 거절 값을 반환하는 기본 흐름을 확인했습니다. 이번 절은 한 번의 승인·거절로 끝나지 않는 입력 검증을 다룹니다. 동일한 interrupt 호출 순서를 유지하는 while 반복을 사용합니다.
4핵심 개념
구체적인 상황
승인 화면이 maybe 같은 허용되지 않은 값을 보내거나 오래된 클라이언트가 예상과 다른 문자열을 보낼 수 있습니다. 잘못된 값을 승인으로 해석하거나 실행을 버리지 않고, 오류 설명을 포함한 새 중단 상태를 반환해야 합니다.
정의
Command(resume=value)는 같은 스레드의 중단된 interrupt()에 value를 전달합니다. 재개하면 노드는 처음부터 다시 실행되며 interrupt 호출 순서가 같아야 저장된 재개 값과 정확히 대응합니다.
첫 graph.invoke는 입력 상태를 받아 interrupt에서 멈춥니다. Command(resume='maybe')는 첫 interrupt의 반환값이 되지만 허용 집합에 없으므로 while이 다음 interrupt를 호출합니다. 두 번째 Command(resume='approve')는 두 번째 interrupt의 반환값이 되어 노드가 상태 갱신을 반환합니다.
코드를 읽는 순서
Command(resume="maybe")는 새 그래프 입력이 아니라 중단된 interrupt()에 전달할 값입니다. review 노드는 approve와 reject만 허용하고, 다른 문자열이면 오류 정보를 payload에 추가해 다음 interrupt를 호출합니다. 호출자는 두 번째 결과의 __interrupt__를 읽어 사용자가 다시 판단할 화면을 만들 수 있습니다.
여러 interrupt가 있는 노드는 호출 순서가 재개 값의 위치를 정합니다. 재개하면 노드가 처음부터 실행되지만 런타임은 이미 처리한 interrupt에 저장된 값을 대응시키고 다음 interrupt에서 다시 멈춥니다. 조건에 따라 호출 순서를 바꾸면 같은 값이 다른 질문의 답으로 사용될 수 있습니다.
도식 읽기
‘interrupt에서 중단’과 ‘Command(resume=값)’ 사이를 사람이 응답할 때마다 오갑니다. 노드는 처음부터 다시 실행하지만 같은 순서의 interrupt가 저장된 값을 소비합니다. ‘검증 뒤 완료 또는 재질문’ 상자가 maybe와 approve의 두 경로를 나눕니다.
5실행 예제
review 노드는 allowed를 approve와 reject로 고정합니다. 첫 출력의 payload에는 요청과 허용값만 있습니다. maybe를 전달한 두 번째 출력에는 error가 추가됩니다. 마지막 호출은 같은 review-2402 스레드에 approve를 전달하고 get_state로 next를 확인합니다.
확인할 점 — 첫 호출은 승인 질문에서 멈췄고 maybe를 전달한 두 번째 호출은 오류 설명과 함께 다시 멈췄습니다. approve를 전달하자 decision이 저장되고 next가 빈 튜플이 됐습니다.
다른 상황과 적용 경계
승인 외에도 주소 보정, 도구 인자 수정, 분류 선택처럼 사람이 유효한 값이 나올 때까지 입력하는 흐름에 적용할 수 있습니다. 자유 형식 문자열을 그대로 실행 명령으로 사용하지 말고 허용값과 스키마를 검증한 뒤 상태를 갱신합니다.
같은 thread_id는 기다리던 실행을 찾는 포인터입니다. 새 ID로 resume을 보내면 기존 interrupt에 값이 전달되지 않습니다. history count는 저장된 체크포인트 수이므로 사용자에게 질문한 횟수와 일치한다고 단정할 수 없습니다. 이번 출력은 payload의 error와 최종 next == ()를 함께 봅니다.
6실험 결과 해석
첫 prompt와 두 번째 prompt의 request와 allowed는 같습니다. 달라진 값은 error 한 항목뿐입니다. approve 뒤 final.decision은 approve이고 next가 빈 튜플이므로 실행이 완료됐습니다. history count 3은 중단을 세 번 뜻하는 값이 아니라 최신 체크포인트 기록 수입니다.
첫 호출은 승인 질문에서 멈췄고 maybe를 전달한 두 번째 호출은 오류 설명과 함께 다시 멈췄습니다. approve를 전달하자 decision이 저장되고 next가 빈 튜플이 됐습니다.
7주의할 점과 실무 메모
재개할 때 다른 thread_id를 쓰면 기다리던 interrupt를 찾지 못합니다.
노드 안의 여러 interrupt 호출 순서를 조건에 따라 바꾸지 않습니다.
승인 값과 승인자, 승인 시각의 감사 기록은 그래프 상태와 운영 정책에 맞게 별도로 보존합니다.
8정리와 다음 절
maybe는 첫 interrupt의 반환값이 됐고, 검증 실패 뒤 두 번째 interrupt가 error를 포함했습니다.
approve는 두 번째 interrupt의 반환값이 되어 decision을 저장하고 next를 빈 튜플로 만들었습니다.
history count 3은 이번 실행에서 만든 체크포인트 기록 수이며, interrupt 횟수를 직접 나타내지는 않습니다.
다음 학습과 이어지는 지점 — 다음 절에서는 완료된 기록을 열어 중간 상태에서 새 분기를 만듭니다.
9복습 문제
1. maybe를 전달한 뒤 그래프가 완료되지 않은 이유는 무엇인가요?
해설 — 허용 집합에 없는 값이라 review가 오류를 포함한 다음 interrupt를 호출했기 때문입니다.
2. Command(resume='approve')의 문자열은 어디에서 읽히나요?
해설 — 중단돼 있던 review 노드의 interrupt() 반환값으로 읽힙니다.
3. 재개 호출에 같은 thread_id가 필요한 이유는 무엇인가요?
해설 — 체크포인터가 해당 스레드의 중단 상태와 재개할 interrupt를 찾아야 하기 때문입니다.
4. interrupt 순서를 바꾸면 어떤 문제가 생기나요?
해설 — 저장된 재개 값이 의도와 다른 interrupt 호출에 대응할 수 있습니다.
10참고 자료
LangGraph Persistence 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph Interrupts 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph Time Travel 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph MIT 라이선스 · 확인 2026-09-14

textbook/part6/ch24-human-in-the-loop/_src/03-상태-기록과-다른-분기-재실행.html

1학습 목표
get_state_history()에서 분기 기준 checkpoint를 고르는 방법을 설명할 수 있습니다.
update_state()가 원본 결과를 보존한 새 분기를 만드는 과정을 확인할 수 있습니다.
time travel이 외부 시스템의 부작용을 되돌리지 않는 이유를 설명할 수 있습니다.
2이 내용을 배우는 이유
운영 중 잘못된 파라미터나 판단을 발견했을 때 전체 실행을 지우지 않고 과거 지점에서 다른 선택을 시험할 수 있어야 합니다.
이 실습은 quote 뒤 discount 전 checkpoint에서 rate만 0.2로 바꿉니다. 원본의 final_price 9000과 분기의 8000이 함께 남는지, 분기 trace에 quote가 새로 추가되지 않는지를 확인합니다.
3앞에서 배운 내용
앞 절까지는 최신 중단 상태를 같은 스레드에서 이어 갔습니다. 체크포인터에는 최신 상태뿐 아니라 단계별 StateSnapshot도 남습니다. 이번 절은 완료된 가격 계산의 과거 snapshot을 골라 할인율 하나만 바꾼 새 경로를 실행합니다.
4핵심 개념
구체적인 상황
10% 할인으로 계산을 마친 뒤 20% 할인 시나리오를 검토해야 한다고 가정합니다. 원본 결과 9000을 지우거나 START부터 모든 작업을 반복할 필요는 없습니다. quote가 끝나고 discount가 시작되기 전 상태에서 rate만 바꾸면 됩니다.
정의
get_state_history()는 스레드의 StateSnapshot을 최신순으로 반환합니다. 과거 체크포인트에 update_state()로 새 값을 쓰면 원본 기록을 보존한 새 분기 설정이 생기고 invoke(None, config)으로 그 지점 뒤를 다시 실행할 수 있습니다.
get_state_history(config)는 최신순으로 snapshot을 반환합니다. snapshot.next가 ('discount',)인 항목은 quote 결과가 저장됐고 discount가 다음인 지점입니다. update_state(snapshot.config, {'rate': 0.2})는 그 과거 상태를 부모로 하는 새 체크포인트를 만들며 원본 완료 체크포인트는 남깁니다.
코드를 읽는 순서
상태 기록에는 현재 값뿐 아니라 단계별 StateSnapshot이 남습니다. get_state_history(config)는 최신 기록부터 반환하고, 각 snapshot의 next는 그 상태에서 다음에 실행할 노드를 나타냅니다. next == ("discount",)인 기록을 고르면 quote는 끝났지만 discount는 실행되기 전인 분기 지점이 됩니다.
update_state(before_discount.config, {"rate": 0.2})는 과거 기록을 수정해 덮어쓰지 않습니다. 그 체크포인트를 부모로 하는 새 체크포인트 설정을 반환합니다. invoke(None, fork_config)는 저장된 quote 결과를 사용하고 그 뒤의 discount부터 실행합니다. 원본 완료 config를 따로 보관하면 원본과 분기 결과를 각각 다시 읽을 수 있습니다.
도식 읽기
‘get_state_history’에서 ‘과거 체크포인트 선택’으로 이동해 next가 discount인 항목을 고릅니다. ‘update_state로 값 변경’은 rate만 0.2로 바꾸고, ‘새 분기 invoke’는 discount 뒤쪽만 실행합니다. quote가 분기 trace에서 한 번만 보이는 이유입니다.
5실행 예제
quote는 trace에 이름만 추가하고 discount는 base_price와 rate로 final_price를 계산합니다. 원본 완료 뒤 original_final_config를 따로 보존합니다. 과거 before_discount.config를 update_state로 갱신하고 반환된 fork_config에 invoke(None)를 호출합니다.
확인할 점 — 원본 할인율 0.1의 최종 가격은 9000으로 유지됐고 과거 체크포인트에서 0.2로 바꾼 분기는 8000을 반환했습니다.
다른 상황과 적용 경계
프롬프트나 임계값을 바꿔 후속 단계만 다시 평가할 때 같은 방식을 사용할 수 있습니다. 다만 분기 지점 뒤의 모델 호출과 API 요청은 다시 실행되므로 저장된 결과와 새 결과의 조건을 기록해야 합니다. reducer가 있는 상태 키를 update하면 값이 대체되지 않고 누적될 수 있다는 점도 확인합니다.
그래프의 time travel은 체크포인트에서 새 실행 경로를 만드는 기능이며 외부 세계의 시간을 되돌리지 않습니다. 이미 전송한 이메일이나 결제를 취소하지 않으므로 보상 작업이나 격리가 필요합니다. 이번 trace는 quote가 재실행되지 않은 상태 경로를 보여 줄 뿐 외부 부작용 복원을 검증하지 않습니다.
6실험 결과 해석
원본 설정을 직접 읽은 final_price는 9000이고 분기는 8000입니다. fork trace에는 기존 quote와 새 discount:0.2가 있어 quote 결과가 재사용됐음을 보여 줍니다. 두 최신 config가 다르므로 새 분기가 원본 완료 체크포인트를 덮어쓰지 않았습니다.
원본 할인율 0.1의 최종 가격은 9000으로 유지됐고 과거 체크포인트에서 0.2로 바꾼 분기는 8000을 반환했습니다.
7주의할 점과 실무 메모
과거 지점 뒤의 LLM 호출, API 요청, interrupt는 다시 실행되므로 비용과 부작용을 검토합니다.
업데이트할 상태 키가 어느 노드의 출력으로 간주되는지 필요하면 as_node를 명시합니다.
time travel은 외부 시스템 시간을 되돌리지 않습니다. 이미 수행한 외부 쓰기는 별도 보상이나 격리가 필요합니다.
8정리와 다음 절
next가 discount인 checkpoint를 골라 quote 결과를 보존했습니다.
rate를 0.2로 바꾼 분기는 8000을 반환했고 원본 설정은 9000을 유지했습니다.
분기 지점 뒤의 호출과 interrupt는 다시 실행될 수 있으며 외부 시스템 상태는 별도 보상 또는 격리가 필요합니다.
다음 학습과 이어지는 지점 — Ch25에서는 저장된 실행에서 상태·메시지·사용자 정의 진행 상황을 스트리밍합니다.
9복습 문제
1. 분기 기준으로 next가 discount인 snapshot을 고른 이유는 무엇인가요?
해설 — quote 결과는 보존하고 할인 계산부터 새 rate로 다시 실행하기 위해서입니다.
2. 원본 9000과 분기 8000이 함께 남는 근거는 무엇인가요?
해설 — 원본 완료 config를 따로 읽었고 fork config가 다른 체크포인트를 가리킵니다.
3. fork trace에서 quote가 새로 추가되지 않은 이유는 무엇인가요?
해설 — 분기 지점이 quote 완료 뒤이므로 저장된 quote 결과를 재사용했기 때문입니다.
4. time travel로 외부 결제도 자동 취소되나요?
해설 — 아닙니다. 그래프 상태 분기와 외부 시스템의 보상 작업은 별도로 처리해야 합니다.
10참고 자료
LangGraph Persistence 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph Interrupts 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph Time Travel 공식 문서 · 확인 2026-09-14 · LangGraph 1.2.11
LangGraph MIT 라이선스 · 확인 2026-09-14

labs/part6/ch24-human-in-the-loop/notebooks/01-interrupt-승인-게이트.ipynb

# interrupt 승인 게이트
로컬 쓰기 전에 승인 여부를 확인해야 거절된 작업이 실행되지 않는지 확인합니다.
## 실행 환경 준비
Python 3.12 커널에 이 절에서 사용할 패키지 버전을 고정합니다.
## 승인 대상과 기록 파일 준비
되돌릴 수 없는 동작을 대신해 로컬 파일 기록을 사용합니다.
`interrupt(payload)`는 노드 실행을 멈추고 payload를 호출자에게 반환합니다. 이를 사용하려면 상태를 저장할 체크포인터와 재개할 실행을 찾는 `thread_id`가 필요합니다. 첫 `invoke`의 결과에는 `__interrupt__`가 들어 있고, `Command(resume=value)`로 같은 스레드를 호출하면 그 값이 노드 안 `interrupt()`의 반환값이 됩니다.
재개는 interrupt 다음 줄에서 프로세스를 그대로 계속하는 방식이 아닙니다. 런타임은 노드를 처음부터 다시 실행하며 저장된 재개 값을 같은 interrupt 호출에 전달합니다. 따라서 interrupt 앞의 `write_effect`는 첫 실행과 재개에서 두 번 실행될 수 있습니다. 승인 게이트는 부작용보다 앞에 두어야 거절이 실제 실행을 막습니다.
## Before: 부작용 뒤에 승인 요청
## After: 승인 뒤에만 부작용 실행
파일 쓰기는 송금, 배포, 삭제처럼 되돌리기 어려운 동작을 대신한 관찰 가능한 예입니다. 읽기 전용 검색까지 매번 승인받으면 흐름만 느려질 수 있으므로 위험한 도구 이름이나 인자 조건에만 게이트를 두는 편이 적절합니다.
승인 화면을 보여 줬다는 사실만으로 안전하지 않습니다. 외부 동작이 승인 전에 실행됐는지, 재개 때 다시 실행되는지 코드 순서로 확인해야 합니다. safe 경로의 파일 부재는 False가 외부 쓰기 전에 검사됐다는 이번 실습의 증거입니다.

labs/part6/ch24-human-in-the-loop/notebooks/02-Command-resume으로-실행-재개.ipynb

# Command(resume=)으로 실행 재개
잘못된 승인 입력을 다시 요청하고 올바른 값으로 같은 스레드를 완료하는 과정을 확인합니다.
## 실행 환경 준비
Python 3.12 커널에 이 절에서 사용할 패키지 버전을 고정합니다.
## 입력 검증 노드 준비
`interrupt()`를 반복문 안에 두고 허용할 문자열을 제한합니다.
`Command(resume="maybe")`는 새 그래프 입력이 아니라 중단된 `interrupt()`에 전달할 값입니다. `review` 노드는 `approve`와 `reject`만 허용하고, 다른 문자열이면 오류 정보를 payload에 추가해 다음 interrupt를 호출합니다. 호출자는 두 번째 결과의 `__interrupt__`를 읽어 사용자가 다시 판단할 화면을 만들 수 있습니다.
여러 interrupt가 있는 노드는 호출 순서가 재개 값의 위치를 정합니다. 재개하면 노드가 처음부터 실행되지만 런타임은 이미 처리한 interrupt에 저장된 값을 대응시키고 다음 interrupt에서 다시 멈춥니다. 조건에 따라 호출 순서를 바꾸면 같은 값이 다른 질문의 답으로 사용될 수 있습니다.
## 처음 중단하고 잘못된 값 전달
각 호출 뒤 `__interrupt__`에 담긴 질문을 확인합니다.
## 올바른 값으로 완료
같은 `thread_id`에 `Command(resume=...)`을 전달합니다.
승인 외에도 주소 보정, 도구 인자 수정, 분류 선택처럼 사람이 유효한 값이 나올 때까지 입력하는 흐름에 적용할 수 있습니다. 자유 형식 문자열을 그대로 실행 명령으로 사용하지 말고 허용값과 스키마를 검증한 뒤 상태를 갱신합니다.
같은 `thread_id`는 기다리던 실행을 찾는 포인터입니다. 새 ID로 resume을 보내면 기존 interrupt에 값이 전달되지 않습니다. `history count`는 저장된 체크포인트 수이므로 사용자에게 질문한 횟수와 일치한다고 단정할 수 없습니다. 이번 출력은 payload의 error와 최종 `next == ()`를 함께 봅니다.

labs/part6/ch24-human-in-the-loop/notebooks/03-상태-기록과-다른-분기-재실행.ipynb

# 상태 기록과 다른 분기 재실행
완료된 실행의 중간 체크포인트에서 값을 바꾸어 원본을 보존한 새 분기를 만들 수 있는지 확인합니다.
## 실행 환경 준비
Python 3.12 커널에 이 절에서 사용할 패키지 버전을 고정합니다.
## 가격 계산 그래프 준비
가격 확정 뒤 할인율을 적용하는 두 노드로 분기 지점을 만듭니다.
상태 기록에는 현재 값뿐 아니라 단계별 `StateSnapshot`이 남습니다. `get_state_history(config)`는 최신 기록부터 반환하고, 각 snapshot의 `next`는 그 상태에서 다음에 실행할 노드를 나타냅니다. `next == ("discount",)`인 기록을 고르면 quote는 끝났지만 discount는 실행되기 전인 분기 지점이 됩니다.
`update_state(before_discount.config, {"rate": 0.2})`는 과거 기록을 수정해 덮어쓰지 않습니다. 그 체크포인트를 부모로 하는 새 체크포인트 설정을 반환합니다. `invoke(None, fork_config)`는 저장된 quote 결과를 사용하고 그 뒤의 discount부터 실행합니다. 원본 완료 config를 따로 보관하면 원본과 분기 결과를 각각 다시 읽을 수 있습니다.
## 그래프 컴파일
두 노드를 순서대로 연결하고 메모리 체크포인터를 붙입니다.
## 원본 실행과 기록 조회
`next`가 `discount`인 상태를 분기 기준으로 고릅니다.
## 할인율을 바꾼 분기 실행
선택한 체크포인트의 상태를 갱신한 뒤 `None`으로 이어서 실행합니다.
프롬프트나 임계값을 바꿔 후속 단계만 다시 평가할 때 같은 방식을 사용할 수 있습니다. 다만 분기 지점 뒤의 모델 호출과 API 요청은 다시 실행되므로 저장된 결과와 새 결과의 조건을 기록해야 합니다. reducer가 있는 상태 키를 update하면 값이 대체되지 않고 누적될 수 있다는 점도 확인합니다.
그래프의 time travel은 체크포인트에서 새 실행 경로를 만드는 기능이며 외부 세계의 시간을 되돌리지 않습니다. 이미 전송한 이메일이나 결제를 취소하지 않으므로 보상 작업이나 격리가 필요합니다. 이번 trace는 quote가 재실행되지 않은 상태 경로를 보여 줄 뿐 외부 부작용 복원을 검증하지 않습니다.
