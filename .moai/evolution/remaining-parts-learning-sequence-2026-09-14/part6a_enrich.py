from __future__ import annotations
raise SystemExit("옛 Part 6 보조 스크립트(part6a_enrich.py)입니다. 실행하면 Ch 21~24 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


LESSONS = {
    "ch21-create-agent/01-create-agent와-ReAct-루프": {
        "heading": "도구와 에이전트 만들기",
        "core": """`@tool`은 평범한 Python 함수를 모델이 선택할 수 있는 도구 명세로 바꿉니다. 함수 이름은 도구 이름이 되고, 매개변수의 타입 힌트는 입력 형식이 되며, 독스트링은 모델이 언제 이 도구를 골라야 하는지 판단하는 설명이 됩니다. `lookup_policy(topic: str) -> str`에서 모델은 `topic` 문자열을 만들고, 실행기는 함수를 호출하며, 반환 문자열은 `ToolMessage`로 대화 상태에 추가됩니다.

`create_agent(model, tools, system_prompt=...)`는 이 명세와 모델을 엮어 `CompiledStateGraph`를 반환합니다. 이 객체를 만드는 순간에는 질문을 처리하지 않습니다. `invoke({"messages": ...})`를 호출해야 루프가 시작되고, 모델이 도구 호출을 만들지 않을 때 끝납니다. 따라서 `print(type(agent).__name__)`은 그래프의 종류를, `result["messages"]`는 한 요청이 실제로 지나간 기록을 보여 줍니다.""",
        "application": """같은 구조를 주문 조회에 적용하면 `lookup_policy` 대신 `lookup_order(order_id)`를 등록할 수 있습니다. 달라지는 것은 도구의 입력과 반환 자료이고, 모델→도구→관찰→모델이라는 루프는 같습니다. 반대로 항상 한 번만 실행할 계산이라면 모델이 다음 행동을 고를 이유가 없으므로 일반 함수나 고정 그래프가 더 분명합니다.

그래프 그림은 가능한 경로의 지도이고 메시지 목록은 이번 요청의 이동 기록입니다. 그림에 ToolNode가 있다고 해서 모든 요청이 도구를 사용한 것은 아닙니다. 이번 출력에서는 `AIMessage.tool_calls`와 그 호출 ID에 대응하는 `ToolMessage`가 모두 있어 실제 도구 사용을 확인할 수 있습니다.""",
    },
    "ch21-create-agent/02-구조화-출력-두-전략": {
        "heading": "출력 스키마와 두 에이전트",
        "core": """출력 스키마는 모델이 채워야 할 필드의 이름과 타입을 미리 정한 형식입니다. `PolicyAnswer(BaseModel)`은 `topic`, `answer`, `source`가 모두 문자열이어야 한다고 선언합니다. `Field(description=...)`의 설명은 사람만 읽는 주석이 아니라 모델에게 각 필드의 의미를 알려 주는 스키마 정보입니다. 에이전트 실행 뒤에는 자연어 메시지를 다시 자르는 대신 `result["structured_response"]`에서 검증된 `PolicyAnswer` 객체를 꺼냅니다.

`response_format=ToolStrategy(PolicyAnswer)`는 스키마를 가상의 도구 호출로 표현하고 LangChain이 결과를 검증하게 합니다. `ProviderStrategy(PolicyAnswer)`는 제공자 API의 구조화 출력 기능에 같은 스키마를 전달합니다. 둘 다 같은 객체를 반환하지만 강제하는 위치가 다릅니다. 스키마 클래스만 직접 넘기면 모델 프로필을 기준으로 전략을 고를 수 있지만, 이 실습은 차이를 관찰하려고 두 전략을 명시합니다.""",
        "application": """구조화 출력은 자연어 답을 표나 데이터베이스 행으로 넘길 때 유용합니다. 예를 들어 상담 분류라면 `category`, `urgency`, `reason`을 필드로 두고, `urgency`를 제한된 값으로 정의해 후속 분기 코드가 예상하지 못한 문자열을 받지 않게 할 수 있습니다. 사람에게 보여 줄 긴 설명만 필요하다면 별도 스키마가 오히려 수정 비용을 늘릴 수 있습니다.

메시지 수는 모델 호출 수와 같지 않습니다. ToolStrategy는 구조화 결과를 나타내는 도구 메시지를 남길 수 있으므로 전체 메시지가 더 많아도 모델을 한 번만 호출했을 수 있습니다. 이번 셀은 `AIMessage` 수와 전체 메시지 수를 따로 세어 이 경계를 확인합니다.""",
    },
    "ch21-create-agent/03-AgentState와-context-schema": {
        "heading": "상태와 실행 컨텍스트 정의",
        "core": """상태(state)는 그래프 단계 사이에 남고 체크포인터가 저장할 수 있는 실행 데이터입니다. `SupportState(AgentState)`의 `request_tag`는 입력 상태에 들어가고 최종 결과에도 남습니다. 실행 컨텍스트(context)는 한 번의 호출 동안 노드와 도구가 참고하지만 상태 채널로 자동 저장되지 않는 의존 정보입니다. `UserContext`를 데이터 클래스로 선언한 이유는 `user_id`와 `access_level`이라는 입력 형식을 호출 전에 고정하기 위해서입니다.

`ToolRuntime[UserContext]`는 모델이 채우는 도구 인자가 아닙니다. LangChain 실행기가 `current_access`를 호출할 때 런타임 객체를 주입하고, 함수는 `runtime.context`에서 호출자가 건넨 컨텍스트를 읽습니다. `agent.invoke(state, context=UserContext(...))`에서 첫 번째 인자는 누적 상태이고 `context=`는 실행 의존 정보입니다. 두 값을 분리하면 모델에게 권한 값을 도구 인자로 생성하게 하지 않아도 됩니다.""",
        "application": """쇼핑 상담에서는 장바구니 항목과 대화 메시지를 상태에 두고, 데이터베이스 연결이나 현재 사용자의 권한 객체를 컨텍스트에 둘 수 있습니다. 같은 권한을 다음 날 다시 써야 한다면 컨텍스트만으로는 충분하지 않으며 별도 저장소에서 다시 읽거나 상태에 필요한 식별자를 남겨야 합니다.

이번 출력에서 `request_tag`가 남고 `context` 키가 없는 사실은 자동 저장 여부만 보여 줍니다. 도구가 컨텍스트 값을 답 문자열에 포함했기 때문에 `read-only`는 메시지에는 나타납니다. 이것을 컨텍스트 객체 전체가 상태에 저장됐다는 뜻으로 해석하면 안 됩니다.""",
    },
    "ch21-create-agent/04-0x에서-1x로-마이그레이션": {
        "heading": "현재 API 서명 확인",
        "core": """마이그레이션은 이름을 일괄 치환하는 작업보다 호출 경계의 변화를 확인하는 작업입니다. `inspect.signature(create_agent)`는 현재 설치된 함수가 받는 매개변수 이름과 기본값을 문자열로 보여 줍니다. 셀의 `for name in [...]` 검사는 이 교재가 사용하는 여섯 인자가 실제 1.4.0 API에 존재하는지 확인하며, 예전 API가 어떻게 동작했는지를 실행하는 검사는 아닙니다.

대응표에서 import 위치, 인자 이름, 반환 상태를 따로 보는 이유가 있습니다. `prompt`를 `system_prompt`로 바꿔도 사용자 상태 형식이나 구조화 결과를 읽는 위치가 예전 코드에 남아 있으면 실행은 일부만 고쳐집니다. 최소 실행은 새 import→그래프 생성→`invoke`→마지막 메시지 읽기까지 한 경로를 통과시켜 호출부가 서로 맞는지 확인합니다.""",
        "application": """실제 서비스에서는 먼저 기존 호출의 관찰 테스트를 고정한 뒤 한 경계씩 바꿉니다. 도구 호출 횟수, 메시지 종류, 구조화 결과 필드처럼 사용자에게 보이는 동작을 기록하면 단순히 import가 성공했다는 사실보다 회귀를 빨리 찾을 수 있습니다.

이 절의 표는 대표적인 이동 지점을 설명하며 모든 0.x API의 호환 목록은 아닙니다. 설치된 1.4.0의 서명에 인자가 있다는 사실도 특정 모델 제공자가 모든 조합을 지원한다는 보장은 아닙니다. 구조화 출력과 도구를 함께 쓸 때의 제공자 지원 범위는 02절의 조건을 다시 확인해야 합니다.""",
    },
    "ch21-create-agent/05-retriever를-도구로-전환": {
        "heading": "로컬 문서와 검색 도구",
        "core": """리트리버(retriever)는 질문을 받아 관련 문서를 반환하는 검색 인터페이스입니다. 이것을 도구로 등록하면 검색 시점과 검색어를 모델이 선택합니다. `search_rules(query: str) -> str`에서 `query`는 모델이 만든 검색 문자열이고, 함수는 `DOCS`를 읽어 관련 문장을 줄바꿈 문자열로 반환합니다. `SEARCH_LOG.append(query)`는 검색 품질을 높이는 기능이 아니라 이번 실행에서 모델이 어떤 검색어를 선택했는지 관찰하는 기록입니다.

고정 RAG는 애플리케이션 코드가 매 질문마다 정해진 검색을 먼저 실행합니다. Agentic RAG는 모델이 검색할지, 어떤 말로 검색할지, 결과가 없을 때 다시 검색할지를 정합니다. `create_agent(..., [search_rules])`는 이 선택권을 제공하지만 검색 결과의 정확성까지 보장하지 않습니다. 도구의 설명과 반환 형식이 모호하면 모델이 적절한 검색어를 만들어도 근거를 잘못 읽을 수 있습니다.""",
        "application": """상품 지원 시스템에서는 주문 번호가 있는 질문만 주문 도구를 호출하고 일반 안내는 검색 없이 답하게 할 수 있습니다. 반면 모든 질문이 같은 사내 문서 한 묶음에서 답을 찾아야 한다면 고정 검색이 실행 횟수와 재현성을 관리하기 쉽습니다. 모델 선택이 필요한 경우와 애플리케이션 규칙으로 충분한 경우를 구분합니다.

검색 로그가 두 줄이면 재검색했다는 사실은 알 수 있지만 두 번째 검색어가 더 좋았다는 결론은 문서와 답을 함께 읽어야 합니다. 결과 없음 답변도 성공한 거부인지 검색어 실패인지 구분해야 하므로, 이 셀은 검색어와 최종 답을 함께 출력합니다.""",
    },
    "ch21-create-agent/06-같은-평가셋으로-RAG-비교": {
        "heading": "Ch14 문서와 평가셋 읽기",
        "core": """공정한 비교에서는 두 경로가 같은 문서, 질문, 정답 기준, 검색 함수를 사용해야 합니다. `cases`는 Ch14 평가 질문 중 세 건을 고정하고, `document_vectors`는 두 경로가 공유하는 임베딩 색인입니다. `retrieve(query, top_k=2)`는 질문 벡터와 모든 문서 벡터의 코사인 유사도를 계산해 상위 두 문서와 점수를 반환합니다. 여기서 반환되는 점수는 답의 정확도가 아니라 질문과 문서 벡터의 가까움을 나타냅니다.

고정 경로는 애플리케이션이 `retrieve`를 호출한 뒤 원문을 모델 프롬프트에 넣습니다. 에이전트 경로는 같은 `retrieve`를 감싼 `search_documents`를 모델이 선택합니다. `usage_total`은 한 실행의 모든 `AIMessage.usage_metadata`를 합쳐 모델 호출 수와 토큰을 세며, `search_events`는 도구 호출 횟수와 검색어를 별도로 남깁니다. 서로 다른 측정값을 같은 비용 또는 품질 지표로 합치지 않습니다.""",
        "application": """질문이 항상 문서 검색을 요구하면 고정 RAG가 적은 분기와 일정한 호출 수를 제공합니다. 계산기·데이터베이스·검색 등 여러 도구 중 하나를 골라야 하거나 검색 결과를 보고 질의를 다시 작성해야 하면 에이전트 경로의 선택 능력이 의미가 있습니다. 같은 정답률이 나와도 실행 과정과 지연은 다를 수 있습니다.

세 질문 결과는 이 데이터와 이번 실행 조건의 관찰입니다. 전체 Agentic RAG가 항상 더 정확하거나 느리다고 일반화할 수 없습니다. 정확도, 검색 성공, 모델 호출 수, 입력 토큰, 지연을 각각 읽고, Ch29 평가에서는 저장한 원문 기록을 다시 사용합니다.""",
    },
    "ch22-middleware/01-미들웨어와-6개-훅": {
        "heading": "도구와 여섯 훅 trace 준비",
        "core": """미들웨어는 `create_agent`가 만든 루프의 약속된 시점에 실행되는 로직입니다. 개발자가 훅 함수를 직접 호출하지 않아도 런타임이 `before_agent`, `before_model`, `after_model`, `after_agent`를 노드처럼 실행합니다. `wrap_model_call`과 `wrap_tool_call`은 대상 호출과 `handler`를 함께 받아 호출 전후를 감쌉니다. 랩 훅에서 `handler`를 호출하지 않으면 실제 모델 또는 도구도 실행되지 않으므로 단순한 전후 알림과 제어 로직을 구분해야 합니다.

`SixHookTrace`는 상태를 바꾸지 않고 `TRACE`에 이름만 남기는 관찰용 클래스입니다. 첫 모델 응답이 도구 호출을 만들기 때문에 `before_model`과 모델 랩은 두 번 실행되고, 도구 랩은 한 번 실행됩니다. 반면 `before_agent`와 `after_agent`는 한 번의 `invoke` 경계에서 각각 한 번 나타납니다. 훅의 횟수는 등록 개수가 아니라 실제 루프 반복과 도구 선택에 따라 달라집니다.""",
        "application": """모델 입력에 사용자 등급을 추가하는 일은 `before_model`, 일시 오류를 재시도하는 일은 `wrap_model_call`, 도구 인자를 검사하는 일은 `wrap_tool_call`이 자연스럽습니다. 같은 검사를 모든 노드에 복사하면 변경 위치가 늘어나므로 반복되는 횡단 관심사를 미들웨어로 모읍니다.

모든 로직을 미들웨어로 옮길 필요는 없습니다. 주문 금액 계산처럼 업무 자체를 나타내는 단계는 그래프 노드나 도구에 두는 편이 흐름을 읽기 쉽습니다. 이 실습의 TRACE 순서는 한 번의 도구 호출 경로에서 관찰한 값이며, 도구가 없거나 병렬 호출이 있으면 횟수와 순서가 달라질 수 있습니다.""",
    },
    "ch22-middleware/02-PII-마스킹-이식": {
        "heading": "Ch16 원본 마스킹 함수 재현",
        "core": """개인 식별 정보(PII)는 이메일, 전화번호처럼 개인을 알아볼 수 있게 하는 데이터입니다. `mask_pii(text)`는 문자열 하나를 받아 정규식과 일치한 부분을 표식으로 바꾸고, 유형별 발견 개수를 함께 반환합니다. 이 함수만 정의해 두면 아무 요청에도 자동 적용되지 않습니다. 호출 지점을 빠뜨린 Before가 그대로 노출되는 이유입니다.

`PIIMiddleware`는 같은 검사를 에이전트 경계에 등록합니다. 입력 검사는 모델에 전달하기 전에 사용자 메시지를 바꾸고, 출력 검사는 모델 응답을 호출자에게 반환하기 전에 바꿉니다. `strategy="mask"`는 일부를 가리는 처리 방식이며, 감지기가 찾지 못한 형식이나 이미지 속 정보까지 보호한다는 뜻은 아닙니다. 입력과 출력 두 방향은 서로 대신할 수 없습니다.""",
        "application": """고객 상담에서는 사용자가 보낸 주민등록번호가 모델로 들어가기 전 마스킹되어야 하고, 모델이 도구 결과에서 읽은 이메일도 최종 응답에서 다시 검사해야 합니다. 로그 저장 경로가 미들웨어 바깥에 있다면 로그에는 원문이 먼저 남을 수 있으므로 데이터가 지나가는 모든 경계를 따로 검토합니다.

마스킹은 값을 숨기면서 요청을 계속 처리하고, 차단은 요청을 중단합니다. 계좌 이체처럼 민감값 없이 업무를 수행할 수 없는 경우에는 무조건 마스킹보다 승인된 별도 경로가 필요할 수 있습니다. 이번 결과는 네 가지 예시 문자열과 지정한 감지 범위에서만 확인한 것입니다.""",
    },
    "ch22-middleware/03-요약-압축과-Compress": {
        "heading": "긴 대화 준비",
        "core": """요약 압축은 오래된 메시지의 핵심을 짧은 메시지로 바꾸어 다음 모델 입력을 줄이는 처리입니다. `SummarizationMiddleware`는 트리거 조건을 넘으면 요약 모델을 호출하고, 최근 메시지 일부와 생성한 요약을 다음 요청에 전달합니다. 체크포인터의 과거 기록 전체를 삭제하는 기능과는 다릅니다. 무엇을 저장했는지와 이번 모델에 무엇을 보냈는지를 구분합니다.

실습의 `CaptureAll`과 `CaptureCompressed`는 모델이 실제로 받은 메시지를 `seen_before`, `seen_after`에 복사하는 관찰 장치입니다. 요약문의 길이만 줄었다고 성공으로 판단하지 않고, 대출 권수·기간·연장 조건·출처가 남았는지 문자열을 읽습니다. 압축은 손실을 허용하는 변환이므로 업무에 필요한 사실을 먼저 정해야 합니다.""",
        "application": """친근한 말투나 반복된 인사는 요약해도 영향이 작지만, 승인 여부·계약 숫자·출처 식별자는 빠지면 후속 답이 달라질 수 있습니다. 이런 값은 상태의 별도 필드에 구조화해 보존하고 대화 요약에는 맥락만 맡기는 설계가 안전합니다.

메시지 수 감소와 토큰 수 감소는 관련되지만 같은 값은 아닙니다. 긴 한 메시지가 짧은 여러 메시지보다 토큰이 많을 수 있습니다. 이번 실습은 전달 메시지와 보존 문자열을 확인하며, 실제 모델별 토큰 절감률이나 요약 정확도 전체를 보장하지 않습니다.""",
    },
    "ch22-middleware/04-호출-한도와-재시도-폴백": {
        "heading": "재시도 모델 준비",
        "core": """재시도, 폴백, 호출 한도는 모두 실패에 대응하지만 해결하는 문제가 다릅니다. `ModelRetryMiddleware`는 같은 요청을 같은 모델에 다시 보내 일시 오류가 사라지는지 확인합니다. `max_retries=2`는 최초 시도 외에 허용할 재시도 수이며, `retry_on=(TimeoutError,)`는 어떤 오류만 반복할지 제한합니다. 코드 버그나 잘못된 입력까지 반복하면 같은 실패만 늘어납니다.

`ModelFallbackMiddleware`는 주 모델 호출이 실패했을 때 다른 모델로 넘깁니다. `ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")`는 한 `invoke` 안에서 허용할 모델 호출을 제한하고, 루프가 두 번째 호출을 요구해도 종료 응답을 만듭니다. 재시도 횟수, 모델 교체 횟수, 루프 호출 한도는 서로 다른 카운터입니다.""",
        "application": """검색 API의 순간적인 타임아웃에는 재시도가 맞고, 특정 제공자 장애에는 폴백이 맞습니다. 모델이 도구를 계속 호출하는 논리적 루프에는 호출 한도가 필요합니다. 세 정책을 함께 쓸 때는 안쪽 재시도가 모두 끝난 뒤 폴백할지, 전체 한도가 재시도까지 셀지 실행 순서를 명시해야 합니다.

이번 결정적 모델은 오류와 응답 순서를 미리 정해 정책 분기를 재현합니다. 실제 네트워크의 지연 분포나 제공자 장애 복구를 측정한 결과는 아닙니다. `calls==2`, 보조 모델 응답, 한도 메시지는 각각 별도의 정책이 작동했다는 증거로 읽습니다.""",
    },
    "ch22-middleware/05-커스텀-예산-미들웨어": {
        "heading": "After: 예산 미들웨어 작성",
        "core": """예산 미들웨어는 모델 호출 직전에 예상 사용량을 예약하고 상한을 넘는 호출을 시작하지 않게 하는 제어 장치입니다. `BudgetMiddleware(max_cost_usd, estimated_cost_per_call)`은 누적 예약값 `reserved`를 보관합니다. `wrap_model_call`은 다음 예약값을 계산한 뒤 허용되면 `handler(request)`를 한 번 호출하고, 넘으면 `BudgetExceeded`를 발생시킵니다. 반환값은 모델 응답이며 예산 숫자가 아닙니다.

여기서 `estimated_cost_per_call`은 실제 사용량에서 계산한 청구 금액이 아니라 실습용 예약 단위입니다. 호출 전에 정확한 출력 길이를 알 수 없기 때문에 보수적인 예상치나 토큰 상한으로 입장을 결정할 수 있습니다. 호출 뒤 실제 사용량을 정산하는 방식과 호출 전 차단은 목적과 오차가 다릅니다.""",
        "application": """사용자별 일일 한도라면 `reserved`를 미들웨어 객체의 메모리에만 두지 않고 사용자 ID와 날짜를 키로 하는 공유 저장소에 기록해야 합니다. 여러 프로세스가 동시에 요청을 받으면 읽기와 예약을 하나의 원자적 연산으로 처리해야 두 요청이 같은 남은 예산을 함께 사용하는 일을 막을 수 있습니다.

호출 한도는 횟수를 제한하고 예산 한도는 서로 다른 모델·입력 길이를 공통 단위로 비교하려는 정책입니다. 이번 셀의 두 번째 차단은 0.004+0.004가 0.006을 넘는 계산을 검증할 뿐, 실제 모델 비용을 측정하거나 제공자의 청구를 대체하지 않습니다.""",
    },
    "ch22-middleware/06-커스텀-감사-미들웨어": {
        "heading": "감사 미들웨어 작성",
        "core": """감사 기록은 나중에 누가 어떤 실행을 했고 어느 단계가 호출됐는지 재구성하기 위한 변경 불가능한 사건 목록입니다. `AuditMiddleware`는 에이전트·모델·도구 경계에서 이벤트를 `EVENTS`에 추가합니다. 각 항목의 `event`는 시점을, 해시는 원문을 저장하지 않고 같은 값인지 비교할 식별값을 나타냅니다. 해시만으로 원문을 복원하지는 못하지만 짧거나 예측 가능한 비밀은 대입 공격에 취약하므로 비밀 저장 수단으로 사용하면 안 됩니다.

직렬화 셀은 이벤트를 JSON으로 바꿔 필드와 순서를 검사합니다. `sort_keys=True`는 같은 딕셔너리를 일정한 문자열로 만드는 데 도움을 주며 시간 순서를 자동 보장하지 않습니다. 모델 호출과 도구 호출의 시작·완료를 구분해야 실패가 어느 경계에서 발생했는지 알 수 있습니다.""",
        "application": """운영 환경에서는 메모리 리스트 대신 접근 제어된 로그 저장소에 요청 ID, 실행 ID, 도구 이름, 성공 여부를 기록합니다. 입력 전문을 그대로 남기면 PII나 비밀값이 감사 로그에 복제될 수 있으므로 허용 필드 목록과 보존 기간을 먼저 정합니다.

관측성 로그는 성능과 오류를 분석하는 자료이고 감사 로그는 책임 있는 변경 이력을 증명하는 자료입니다. 같은 시스템에 저장할 수 있어도 접근 권한과 보존 규칙이 다릅니다. 이번 `assert`는 예상 이벤트 종류와 비밀 문자열 부재를 확인하지만 로그의 위변조 방지나 장기 보존을 검증하지 않습니다.""",
    },
    "ch22-middleware/07-순서와-합성": {
        "heading": "태그 미들웨어 정의",
        "core": """여러 미들웨어를 등록하면 목록 순서가 실행 경계를 만듭니다. `before_agent`와 `before_model` 같은 진입 훅은 A→B→C 순서로 실행됩니다. 랩 훅은 A가 B를 감싸고 B가 C를 감싸는 중첩 구조이므로 호출 전에는 A→B→C, 반환 후에는 C→B→A가 됩니다. `after_model`과 `after_agent`도 바깥으로 나오며 역순으로 실행됩니다.

`Tagged(name)`은 각 훅에서 태그와 시점을 `ORDER`에 남깁니다. `handler(request)` 앞뒤에 서로 다른 문자열을 기록하면 한 랩의 진입과 이탈을 구분할 수 있습니다. 예상 목록과 실제 목록의 완전 일치 검사는 훅이 모두 한 번 실행됐다는 사실뿐 아니라 중첩 순서까지 확인합니다.""",
        "application": """입력 마스킹 뒤 감사 해시를 만들면 감사 기록에는 마스킹된 값이 남습니다. 반대로 감사 뒤 마스킹하면 원문 해시가 남을 수 있습니다. 재시도 랩과 사용량 기록 랩의 순서도 재시도마다 사용량을 셀지 전체 요청 한 번으로 셀지를 바꿉니다. 목록 순서는 코드 스타일이 아니라 정책 의미입니다.

서로 독립적인 읽기 전용 기록은 순서 영향이 작지만, 요청이나 상태를 수정하는 미들웨어는 교환해도 같은 결과가 나오는지 확인해야 합니다. 이 실습은 모델 호출 한 번인 경로를 사용하므로 도구 루프와 재시도가 섞인 전체 순서를 자동으로 증명하지 않습니다.""",
    },
    "ch22-middleware/08-컨텍스트-분리와-Isolate": {
        "heading": "업무가 섞인 메시지 준비",
        "core": """컨텍스트 분리는 한 대화 기록에서 현재 작업에 필요한 메시지만 모델 입력으로 선택하는 처리입니다. `mixed`에는 대출과 급여 두 업무의 메시지가 함께 있고, `CapturingModel.seen`은 모델이 실제로 받은 텍스트를 보관합니다. Before는 다섯 메시지를 모두 전달하므로 현재 질문과 무관한 급여 정보도 모델 입력에 포함됩니다.

`IsolateMiddleware("loan")`은 모델 호출 직전 요청의 메시지를 업무 표식으로 걸러 새 요청을 전달합니다. 원래 그래프 상태를 영구 삭제하는 것과는 다르며, 이번 모델 호출의 가시 범위를 줄입니다. 필터가 필요한 근거까지 제거하면 답변 품질이 낮아질 수 있으므로 업무 ID를 붙이는 시점과 기본 포함 규칙을 명확히 해야 합니다.""",
        "application": """하나의 고객이 주문과 환불을 동시에 문의하면 업무별 분리가 오히려 연결 정보를 끊을 수 있습니다. 이런 경우 공통 고객 정보는 별도 컨텍스트로 제공하고, 업무별 대화만 선택하는 두 층 구조가 필요합니다. 단순 키워드 필터보다 생성 시점에 명시적 `task_id`를 붙이는 편이 경계를 확인하기 쉽습니다.

격리는 접근 통제와 같지 않습니다. 모델 입력에서 급여 문장을 뺐더라도 원본 상태나 로그를 읽을 권한이 그대로라면 보안 경계가 완성되지 않습니다. 이번 출력은 모델이 받은 다섯 문장이 세 문장으로 줄고 급여 문자열이 사라진 사실만 보여 줍니다.""",
    },
    "ch23-persistence/01-체크포인터와-스레드": {
        "heading": "그래프와 체크포인터 준비",
        "core": """체크포인터(checkpointer)는 그래프의 단계별 상태 스냅샷을 저장하고, 스레드(thread)는 관련 체크포인트를 묶는 식별자입니다. `builder.compile(checkpointer=memory)`에서 저장 기능을 그래프에 연결하지만 이때 상태가 생기지는 않습니다. `invoke(..., {"configurable": {"thread_id": ...}})`가 실행될 때 해당 스레드에 체크포인트가 기록됩니다.

`InMemorySaver`는 현재 Python 프로세스의 메모리에만 저장합니다. `get_state(config)`는 선택한 스레드의 최신 `StateSnapshot`을, `get_state_history(config)`는 단계별 기록을 최신순으로 반환합니다. 상태의 `events`가 누적되는 방식은 상태 스키마와 노드가 반환하는 값에 달려 있으며, 체크포인터가 모든 리스트를 자동으로 합치는 것은 아닙니다.""",
        "application": """같은 고객의 이어지는 대화에는 같은 `thread_id`를 사용하고, 독립된 상담이나 테스트에는 새 ID를 사용합니다. 사용자 ID를 그대로 스레드 ID로 쓰면 동시에 열린 두 상담이 섞일 수 있으므로 대화 단위를 구분하는 식별자가 필요합니다.

체크포인터는 그래프 상태를 저장하고 Store는 여러 스레드가 공유할 사용자 선호 같은 데이터를 저장합니다. 이번 `customer-a`와 `customer-b` 비교는 스레드 격리를 보여 주며, 프로세스 종료 뒤 복구는 증명하지 않습니다. 그 경계는 파일 또는 데이터베이스 기반 저장기를 사용하는 다음 절에서 다룹니다.""",
    },
    "ch23-persistence/02-PostgresSaver-준비와-스키마": {
        "heading": "접속과 그래프 준비",
        "core": """`PostgresSaver`는 체크포인트와 pending write를 PostgreSQL 표에 저장하는 구현입니다. 데이터베이스 URI는 연결 위치를, `search_path`는 이 실습이 사용할 스키마를 정합니다. `PostgresSaver(conn)`은 이미 열린 연결을 사용하며, `setup()`은 필요한 표와 마이그레이션을 준비합니다. 저장기를 만든 것과 저장 구조를 준비한 것은 서로 다른 단계입니다.

Before는 새 스키마에서 `setup()` 없이 그래프를 실행해 실제 데이터베이스 오류를 확인합니다. After는 같은 연결에서 `setup()`을 먼저 호출한 뒤 체크포인터를 붙여 실행합니다. `checkpoints`는 상태 스냅샷을, `checkpoint_writes`는 단계 안의 쓰기를 저장하는 핵심 표입니다. 표가 존재한다는 사실과 운영 권한·백업·성능이 준비됐다는 사실은 구분해야 합니다.""",
        "application": """개발자의 로컬 실험은 SQLite로 충분할 수 있지만 여러 서버가 같은 실행을 재개해야 하면 공유 데이터베이스가 필요합니다. 운영에서는 애플리케이션 시작 때마다 무제한으로 스키마 권한을 주기보다 배포 마이그레이션과 실행 계정의 권한을 분리합니다.

연결 문자열에는 비밀번호가 포함될 수 있으므로 로그나 노트북 출력에 원문을 남기지 않습니다. 이 실습은 로컬 PostgreSQL의 별도 스키마에서 표 생성과 값 12 저장을 확인합니다. 장애 조치, 연결 풀, 동시 실행 성능은 별도 운영 검증이 필요합니다.""",
    },
    "ch23-persistence/03-스레드-재개와-대화-이어가기": {
        "heading": "파일 체크포인터 준비",
        "core": """`SqliteSaver`는 체크포인트를 SQLite 파일에 저장하므로 Python 그래프 객체를 새로 만들어도 같은 파일과 `thread_id`를 사용하면 상태를 읽을 수 있습니다. `sqlite3.connect(..., check_same_thread=False)`는 파일 연결을 만들고, `SqliteSaver(conn)`은 그 연결을 체크포인터 인터페이스로 감쌉니다. 연결의 생명주기와 그래프 객체의 생명주기를 구분합니다.

상태의 `turns`에는 `Annotated[list[str], operator.add]` 리듀서가 붙어 있습니다. 노드가 새 턴 목록을 반환하면 기존 목록을 덮어쓰지 않고 이어 붙입니다. 두 번째 프로그램 객체에서 `invoke({"turns": ["질문 2"]}, 같은 config)`를 호출하면 저장된 이전 턴을 먼저 불러온 뒤 새 입력과 노드 출력을 합칩니다.""",
        "application": """웹 서버가 재시작된 뒤 사용자가 같은 상담을 이어 가는 상황에 이 패턴을 적용할 수 있습니다. 새 상담을 시작하려면 SQLite 파일을 지우는 대신 새 `thread_id`를 사용해야 기존 기록과 새 기록의 경계가 분명합니다.

리듀서가 없으면 같은 키의 새 값은 이전 값을 대체할 수 있습니다. 반대로 모든 데이터를 무조건 누적하면 메시지와 중복 상태가 계속 커집니다. 이번 출력의 네 턴은 파일 지속성과 리스트 리듀서가 함께 만든 결과이며, SQLite가 자동으로 대화 의미를 관리한 것은 아닙니다.""",
    },
    "ch23-persistence/04-내구-실행-모드-비교": {
        "heading": "실험 함수 준비",
        "core": """내구 실행 모드는 완료된 단계의 체크포인트를 저장 호출과 어느 시점에 맞출지 정합니다. `sync`는 다음 단계로 진행하기 전에 저장 완료를 기다리고, `async`는 저장을 진행하면서 다음 작업을 이어 가며, `exit`는 실행이 끝날 때 상태를 기록합니다. 저장 시점이 다르면 갑작스러운 프로세스 종료 직전에 디스크에 남은 범위가 달라질 수 있습니다.

`kill_and_resume(mode)`는 같은 그래프와 입력을 자식 프로세스에서 실행하고, 두 번째 노드 진입을 알리는 ready 파일이 생기면 프로세스를 종료합니다. `read_saved`는 SQLite에서 최신 `channel_values`를 읽고, 같은 모드 이름을 `thread_id`로 사용해 새 프로세스로 재개합니다. ready 파일은 체크포인트 저장 완료 신호가 아니라 노드 진입 신호입니다.""",
        "application": """결제 승인처럼 한 단계 손실도 허용하기 어려운 흐름은 저장 완료를 기다리는 모드가 필요할 수 있습니다. 대량 배치처럼 처리량이 우선이고 다시 계산할 수 있는 흐름은 비동기 저장의 지연 이점을 검토할 수 있습니다. 선택에는 저장소 지연과 재실행 비용을 함께 봐야 합니다.

특히 `async` 결과는 종료와 백그라운드 저장의 경합에 따라 달라질 수 있습니다. 이번 한 번의 관찰을 항상 같은 보장으로 읽으면 안 됩니다. 세 모드가 모두 재개 후 완료됐다는 결과와 종료 직전 저장 범위의 차이를 따로 해석합니다.""",
    },
    "ch23-persistence/05-pending-writes와-장애-복구": {
        "heading": "병렬 그래프 준비",
        "core": """LangGraph의 한 superstep에서는 여러 노드가 병렬로 실행될 수 있습니다. `good`과 `flaky`는 START에서 동시에 갈라지는 같은 단계의 노드입니다. `results`에는 리스트를 합치는 리듀서를 붙여 두 노드의 성공 결과가 하나의 상태 채널에 모이게 합니다. `flaky`가 오류를 내더라도 `good`이 이미 반환한 쓰기는 pending write로 체크포인터에 남을 수 있습니다.

첫 실행 뒤 `snapshot.tasks`에는 각 작업의 결과나 오류가 기록됩니다. `graph.invoke(None, config)`는 새 입력을 넣지 않고 실패한 단계에서 재개합니다. 저장된 `good`의 결과를 재사용하고 실패한 `flaky`만 다시 실행하므로 호출 로그에서 good은 한 번, flaky는 두 번 나타납니다.""",
        "application": """문서 세 개를 병렬 분석하다 하나만 실패한 경우 성공한 두 분석을 다시 호출하지 않는 데 같은 원리를 사용할 수 있습니다. 다만 노드가 체크포인터 밖의 파일이나 외부 API에 먼저 쓴 결과까지 pending write가 관리하지는 않습니다. 외부 부작용에는 다음 절의 멱등성 설계가 필요합니다.

superstep 전체가 데이터베이스 트랜잭션처럼 모두 취소된다고 설명하면 이번 출력과 맞지 않습니다. 성공한 노드의 상태 쓰기는 보존되고 실패한 작업만 다시 실행될 수 있습니다. 실제 실행 순서는 병렬 스케줄링에 따라 달라질 수 있으므로 로그의 순서보다 호출 횟수와 최종 결과를 봅니다.""",
    },
    "ch23-persistence/06-노드-재시작과-멱등성": {
        "heading": "실제 중단과 재개 함수",
        "core": """멱등성(idempotency)은 같은 연산 요청을 여러 번 받아도 외부 결과가 한 번 처리한 것과 같게 유지되는 성질입니다. 체크포인터는 노드 시작과 완료 사이에 프로세스가 종료되면 그 노드를 다시 실행할 수 있습니다. 파일 쓰기는 이미 끝났지만 노드 완료 체크포인트가 없으면 재개 시 같은 주문 번호를 다시 쓸 수 있습니다.

`interrupt_then_resume(strategy)`는 자식 프로세스가 외부 쓰기를 마친 직후 종료 신호 파일을 만들게 하고, 부모가 그 프로세스를 강제로 종료한 뒤 같은 SQLite와 전략으로 재개합니다. `operation_id="order-2306"`은 논리적 작업을 식별합니다. idempotent 전략은 이미 처리한 ID인지 검사해 두 번째 쓰기를 건너뜁니다.""",
        "application": """결제나 이메일 API가 멱등 키를 지원하면 호출자가 작업 ID를 보내고 서버가 이전 결과를 재사용하게 할 수 있습니다. 로컬에서 먼저 조회한 뒤 쓰는 방식은 두 프로세스가 동시에 통과할 수 있으므로 운영 저장소에서는 고유 제약이나 원자적 삽입을 사용해야 합니다.

재시도는 실패한 호출을 다시 시도하는 정책이고 멱등성은 반복 호출이 중복 효과를 만들지 않게 하는 성질입니다. 재시도 횟수를 1로 줄여도 종료 시점의 불확실성은 남습니다. 이번 로그 한 줄은 실습 worker의 중복 차단을 확인하며 외부 서비스 전체의 멱등성을 보장하지 않습니다.""",
    },
    "ch24-human-in-the-loop/01-interrupt-승인-게이트": {
        "heading": "승인 대상과 기록 파일 준비",
        "core": """`interrupt(payload)`는 노드 실행을 멈추고 payload를 호출자에게 반환합니다. 이를 사용하려면 상태를 저장할 체크포인터와 재개할 실행을 찾는 `thread_id`가 필요합니다. 첫 `invoke`의 결과에는 `__interrupt__`가 들어 있고, `Command(resume=value)`로 같은 스레드를 호출하면 그 값이 노드 안 `interrupt()`의 반환값이 됩니다.

재개는 interrupt 다음 줄에서 프로세스를 그대로 계속하는 방식이 아닙니다. 런타임은 노드를 처음부터 다시 실행하며 저장된 재개 값을 같은 interrupt 호출에 전달합니다. 따라서 interrupt 앞의 `write_effect`는 첫 실행과 재개에서 두 번 실행될 수 있습니다. 승인 게이트는 부작용보다 앞에 두어야 거절이 실제 실행을 막습니다.""",
        "application": """파일 쓰기는 송금, 배포, 삭제처럼 되돌리기 어려운 동작을 대신한 관찰 가능한 예입니다. 읽기 전용 검색까지 매번 승인받으면 흐름만 느려질 수 있으므로 위험한 도구 이름이나 인자 조건에만 게이트를 두는 편이 적절합니다.

승인 화면을 보여 줬다는 사실만으로 안전하지 않습니다. 외부 동작이 승인 전에 실행됐는지, 재개 때 다시 실행되는지 코드 순서로 확인해야 합니다. safe 경로의 파일 부재는 False가 외부 쓰기 전에 검사됐다는 이번 실습의 증거입니다.""",
    },
    "ch24-human-in-the-loop/02-Command-resume으로-실행-재개": {
        "heading": "입력 검증 노드 준비",
        "core": """`Command(resume="maybe")`는 새 그래프 입력이 아니라 중단된 `interrupt()`에 전달할 값입니다. `review` 노드는 `approve`와 `reject`만 허용하고, 다른 문자열이면 오류 정보를 payload에 추가해 다음 interrupt를 호출합니다. 호출자는 두 번째 결과의 `__interrupt__`를 읽어 사용자가 다시 판단할 화면을 만들 수 있습니다.

여러 interrupt가 있는 노드는 호출 순서가 재개 값의 위치를 정합니다. 재개하면 노드가 처음부터 실행되지만 런타임은 이미 처리한 interrupt에 저장된 값을 대응시키고 다음 interrupt에서 다시 멈춥니다. 조건에 따라 호출 순서를 바꾸면 같은 값이 다른 질문의 답으로 사용될 수 있습니다.""",
        "application": """승인 외에도 주소 보정, 도구 인자 수정, 분류 선택처럼 사람이 유효한 값이 나올 때까지 입력하는 흐름에 적용할 수 있습니다. 자유 형식 문자열을 그대로 실행 명령으로 사용하지 말고 허용값과 스키마를 검증한 뒤 상태를 갱신합니다.

같은 `thread_id`는 기다리던 실행을 찾는 포인터입니다. 새 ID로 resume을 보내면 기존 interrupt에 값이 전달되지 않습니다. `history count`는 저장된 체크포인트 수이므로 사용자에게 질문한 횟수와 일치한다고 단정할 수 없습니다. 이번 출력은 payload의 error와 최종 `next == ()`를 함께 봅니다.""",
    },
    "ch24-human-in-the-loop/03-상태-기록과-다른-분기-재실행": {
        "heading": "가격 계산 그래프 준비",
        "core": """상태 기록에는 현재 값뿐 아니라 단계별 `StateSnapshot`이 남습니다. `get_state_history(config)`는 최신 기록부터 반환하고, 각 snapshot의 `next`는 그 상태에서 다음에 실행할 노드를 나타냅니다. `next == ("discount",)`인 기록을 고르면 quote는 끝났지만 discount는 실행되기 전인 분기 지점이 됩니다.

`update_state(before_discount.config, {"rate": 0.2})`는 과거 기록을 수정해 덮어쓰지 않습니다. 그 체크포인트를 부모로 하는 새 체크포인트 설정을 반환합니다. `invoke(None, fork_config)`는 저장된 quote 결과를 사용하고 그 뒤의 discount부터 실행합니다. 원본 완료 config를 따로 보관하면 원본과 분기 결과를 각각 다시 읽을 수 있습니다.""",
        "application": """프롬프트나 임계값을 바꿔 후속 단계만 다시 평가할 때 같은 방식을 사용할 수 있습니다. 다만 분기 지점 뒤의 모델 호출과 API 요청은 다시 실행되므로 저장된 결과와 새 결과의 조건을 기록해야 합니다. reducer가 있는 상태 키를 update하면 값이 대체되지 않고 누적될 수 있다는 점도 확인합니다.

그래프의 time travel은 체크포인트에서 새 실행 경로를 만드는 기능이며 외부 세계의 시간을 되돌리지 않습니다. 이미 전송한 이메일이나 결제를 취소하지 않으므로 보상 작업이나 격리가 필요합니다. 이번 trace는 quote가 재실행되지 않은 상태 경로를 보여 줄 뿐 외부 부작용 복원을 검증하지 않습니다.""",
    },
}


def md_to_html(text: str) -> str:
    parts = []
    for paragraph in text.strip().split("\n\n"):
        escaped = html.escape(paragraph)
        escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
        parts.append(f"<p>{escaped}</p>")
    return "".join(parts)


def update_source(chapter: str, stem: str, data: dict[str, str]) -> None:
    path = ROOT / "textbook/part6" / chapter / "_src" / f"{stem}.html"
    source = path.read_text(encoding="utf-8")
    core_html = "<h3>코드를 읽는 순서</h3>" + md_to_html(data["core"])
    application_html = "<h3>다른 상황과 적용 경계</h3>" + md_to_html(data["application"])
    core_start = source.find("<h3>코드를 읽는 순서</h3>")
    if core_start >= 0:
        core_end = source.find("<h3>도식 읽기</h3>", core_start)
        if core_end < 0:
            raise RuntimeError(f"diagram heading missing: {path}")
        source = source[:core_start] + source[core_end:]
    application_start = source.find("<h3>다른 상황과 적용 경계</h3>")
    if application_start >= 0:
        token = f"{{{{notebook:{stem}"
        candidates = [
            position for position in (
                source.find(token, application_start),
                source.find('<h2 id="b6">', application_start),
            ) if position >= 0
        ]
        if not candidates:
            raise RuntimeError(f"application boundary missing: {path}")
        application_end = min(candidates)
        source = source[:application_start] + source[application_end:]
    source = source.replace("<h3>도식 읽기</h3>", core_html + "<h3>도식 읽기</h3>", 1)
    token = f"{{{{notebook:{stem}"
    if source.find(token) < 0:
        raise RuntimeError(f"notebook token missing: {path}")
    boundary = source.find('<h2 id="b6">')
    if boundary < 0:
        raise RuntimeError(f"section 6 heading missing: {path}")
    source = source[:boundary] + application_html + source[boundary:]
    source = source.replace("확인 2026-09-11", "확인 2026-09-14")
    source = source.replace("거절 값을 돌려주는 기본 흐름", "거절 값을 반환하는 기본 흐름")
    path.write_text(source, encoding="utf-8")


def update_notebook(chapter: str, stem: str, data: dict[str, str]) -> None:
    path = ROOT / "labs/part6" / chapter / "notebooks" / f"{stem}.ipynb"
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for markdown in (cell for cell in notebook["cells"] if cell["cell_type"] == "markdown"):
        current = "".join(markdown.get("source", []))
        current = current.replace("중단된 `interrupt()`에 돌려줄 값", "중단된 `interrupt()`에 전달할 값")
        current = current.replace(data["core"].strip(), "").replace(data["application"].strip(), "")
        current = re.sub(r"\n{3,}", "\n\n", current).rstrip() + "\n"
        markdown["source"] = current.splitlines(keepends=True)
    target = next(
        cell for cell in notebook["cells"]
        if cell["cell_type"] == "markdown" and data["heading"] in "".join(cell["source"])
    )
    target_text = "".join(target["source"]).rstrip() + "\n\n" + data["core"].strip() + "\n"
    target["source"] = target_text.splitlines(keepends=True)

    last_code_index = max(i for i, cell in enumerate(notebook["cells"]) if cell["cell_type"] == "code")
    preceding = max(i for i in range(last_code_index) if notebook["cells"][i]["cell_type"] == "markdown")
    cell = notebook["cells"][preceding]
    text = "".join(cell["source"]).rstrip() + "\n\n" + data["application"].strip() + "\n"
    cell["source"] = text.splitlines(keepends=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> None:
    for key, data in LESSONS.items():
        chapter, stem = key.split("/", 1)
        update_source(chapter, stem, data)
        update_notebook(chapter, stem, data)
        print(key)

    source_path = ROOT / "textbook/part6/ch21-create-agent/_src/06-같은-평가셋으로-RAG-비교.html"
    source = source_path.read_text(encoding="utf-8")
    extra = (
        '<p>Ch6에서 배운 <code>model.with_structured_output(Grade, method="json_schema", strict=True)</code>는 '
        '<code>Grade</code> 형식을 적용한 새 호출 객체를 준비하며, 이 줄만으로 모델을 호출하지 않습니다. '
        '뒤의 <code>grader.invoke(...)</code>가 원문과 답을 실제로 보내고 <code>Grade</code> 객체를 반환합니다. '
        '<code>supported: bool</code>은 참·거짓 형식을 검증하지만 판정 자체가 옳다는 보장은 아니므로 '
        '<code>explanation</code>과 원문을 함께 읽습니다. Ch21 02의 '
        '<code>create_agent(..., response_format=...)</code>이 에이전트 최종 상태의 '
        '<code>structured_response</code>를 만드는 방식과 달리, 여기서는 모델 호출의 직접 반환값이 '
        '<code>Grade</code>입니다.</p>'
    )
    if extra not in source:
        source = source.replace('<h3>다른 상황과 적용 경계</h3>', extra + '<h3>다른 상황과 적용 경계</h3>', 1)
        source_path.write_text(source, encoding="utf-8")

    notebook_path = ROOT / "labs/part6/ch21-create-agent/notebooks/06-같은-평가셋으로-RAG-비교.ipynb"
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    extra_md = (
        'Ch6에서 배운 `model.with_structured_output(Grade, method="json_schema", strict=True)`는 `Grade` 형식을 '
        '적용한 새 호출 객체를 준비하며, 이 줄만으로 모델을 호출하지 않습니다. 뒤의 `grader.invoke(...)`가 '
        '원문과 답을 실제로 보내고 `Grade` 객체를 반환합니다. `supported: bool`은 참·거짓 형식을 검증하지만 '
        '판정 자체가 옳다는 보장은 아니므로 `explanation`과 원문을 함께 읽습니다. Ch21 02의 '
        '`create_agent(..., response_format=...)`이 에이전트 최종 상태의 `structured_response`를 만드는 방식과 '
        '달리, 여기서는 모델 호출의 직접 반환값이 `Grade`입니다.'
    )
    for cell in (item for item in notebook["cells"] if item["cell_type"] == "markdown"):
        current = "".join(cell.get("source", [])).replace(extra_md, "")
        current = re.sub(r"\n{3,}", "\n\n", current).rstrip() + "\n"
        cell["source"] = current.splitlines(keepends=True)
    target = next(
        cell for cell in notebook["cells"]
        if cell["cell_type"] == "markdown" and "원문 기준 LLM 평가" in "".join(cell["source"])
    )
    target["source"] = ("".join(target["source"]).rstrip() + "\n\n" + extra_md + "\n").splitlines(keepends=True)
    notebook_path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
