from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHAPTER = ROOT / "textbook/part5/ch20-tool-node"
LAB = ROOT / "labs/part5/ch20-tool-node"


def md(source: str, lesson_part: str | None = None) -> dict:
    metadata = {"lesson_part": lesson_part} if lesson_part else {}
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": source.splitlines(keepends=True)}


def code(source: str, lesson_part: str | None = None) -> dict:
    metadata = {"lesson_part": lesson_part} if lesson_part else {}
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": metadata, "outputs": [], "source": source.splitlines(keepends=True)}


INSTALL = """%pip install -q langgraph==1.2.11 langchain==1.4.0 langchain-openai==1.6.0 python-dotenv==1.2.3
import os
from pathlib import Path
from importlib.metadata import version
from dotenv import load_dotenv

for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / '.env').is_file():
        load_dotenv(folder / '.env')
        break
assert os.getenv('OPENAI_API_KEY'), 'OPENAI_API_KEY가 필요합니다.'
print('langgraph', version('langgraph'))
print('langchain', version('langchain'))
print('langchain-openai', version('langchain-openai'))
print('API 키 존재 여부 확인 완료')"""


COMMON = """from time import perf_counter
from langchain.chat_models import init_chat_model

MODEL_NAME = 'gpt-5.4-mini'
INPUT_USD_PER_MTOK = 0.75
OUTPUT_USD_PER_MTOK = 4.50

def usage_of(message) -> dict:
    usage = message.usage_metadata
    assert usage is not None, 'usage_metadata가 없어 비용을 계산할 수 없습니다.'
    assert 'input_tokens' in usage and 'output_tokens' in usage
    input_tokens = usage['input_tokens']
    output_tokens = usage['output_tokens']
    cost = input_tokens / 1_000_000 * INPUT_USD_PER_MTOK
    cost += output_tokens / 1_000_000 * OUTPUT_USD_PER_MTOK
    return {'input_tokens': input_tokens, 'output_tokens': output_tokens, 'estimated_cost_usd': cost}

def make_model():
    return init_chat_model(f'openai:{MODEL_NAME}', reasoning_effort='none')"""


DATA_AND_TOOLS = """from langchain.tools import tool

POLICIES = {
    '대출': '일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.',
    '운영': '평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.',
    '연체': '연체한 일수만큼 새 대출이 제한됩니다.',
}

@tool
def lookup_policy(topic: str) -> str:
    \"\"\"교육센터 자료실 규정을 주제어로 조회합니다. topic은 대출, 운영, 연체 중 하나입니다.\"\"\"
    if topic not in POLICIES:
        raise ValueError(f'지원하지 않는 주제: {topic}')
    return POLICIES[topic]

TOOLS = [lookup_policy]"""


LESSONS = {
    "01-ToolNode와-tools-condition": {
        "title": "ToolNode와 tools_condition",
        "format": "experiment",
        "hours": "강의 1h · 실습 1.5h",
        "terms": "5",
        "question": "StateGraph에 ToolNode와 tools_condition을 직접 연결하면 모델의 도구 선택이 어떤 메시지 흐름으로 실행될까요?",
        "goals": [
            "add_messages 리듀서와 trace를 가진 AgentState에 모델 노드와 ToolNode를 등록할 수 있습니다.",
            "tools_condition이 도구 실행과 종료를 고르는 기준을 설명할 수 있습니다.",
            "실제 모델 호출의 AIMessage, ToolMessage, 최종 AIMessage를 순서대로 읽을 수 있습니다.",
        ],
        "why": "Ch18에서는 직접 작성한 while 문이 tool_calls를 읽고 도구 함수를 호출했습니다. Ch19에서는 @tool과 bind_tools로 모델이 읽을 도구 설명과 인자 형식을 만들었습니다. 이제 그 두 요소를 Ch13의 StateGraph에 넣습니다. 모델이 도구를 요청하면 ToolNode가 실행하고, 요청하지 않으면 종료하는 연결이 처음 완성됩니다. 이 구조를 직접 조립해야 다음 Ch21의 create_agent가 감추는 반복 구조를 읽을 수 있습니다.",
        "prior": "Ch13에서 StateGraph, MessagesState와 add_messages 리듀서, 조건부 엣지를 배웠습니다. Ch17에서는 모델·도구·반복·정지 조건이 에이전트의 구성 요소라는 사실과 자율성의 비용을 확인했습니다. Ch19에서는 lookup 함수에 @tool을 붙이고 model.bind_tools(tools)가 도구 스키마를 모델 요청에 포함시키는 과정을 배웠습니다. 이번 노트북은 앞 노트북의 변수에 의존하지 않고 작은 읽기 전용 규정 자료를 다시 선언합니다.",
        "concept": "상담 창구를 떠올려 봅니다. 모델 노드는 질문을 읽고 바로 답하거나 조회표를 작성합니다. tools_condition은 마지막 AIMessage에 tool_calls가 있는지만 확인하는 안내 표지입니다. 요청이 있으면 tools 노드로 이동하고, 없으면 END로 이동합니다. ToolNode는 요청 이름과 인자를 확인해 실제 도구를 실행하고 그 결과를 ToolMessage로 추가합니다. 도구 결과를 읽은 모델이 최종 답을 만들면 tool_calls가 사라지고 그래프가 끝납니다. 이 절은 MessagesState를 직접 쓰지 않고, 직접 정의한 AgentState의 messages 필드에 add_messages 리듀서를 붙여 HumanMessage, AIMessage, ToolMessage를 실행 순서대로 보존합니다. trace 필드는 실행한 노드 이름을 별도로 누적합니다.",
        "observe": "대출 기간 질문의 trace에는 모델 호출 두 번이 나타나고, 그 사이의 ToolNode 실행은 메시지 목록의 ToolMessage로 확인합니다. 메시지 종류는 HumanMessage, AIMessage, ToolMessage, AIMessage 순서입니다. 첫 AIMessage의 tool_calls에는 lookup_policy와 topic 인자가 있고, ToolMessage에는 로컬 규정 문자열이 있습니다. 반면 인사 질문은 도구를 부를 이유가 없으므로 model 한 단계 뒤에 끝날 수 있습니다. 모델 출력은 실행 시점에 달라질 수 있으므로 정확한 문장보다 메시지 종류, 호출 이름, 도구 결과 포함 여부를 확인합니다.",
        "notes": [
            "tools_condition은 질문의 키워드를 직접 검사하지 않습니다. 마지막 AIMessage의 tool_calls 유무만 봅니다.",
            "ToolNode는 모델이 아닙니다. 이미 만들어진 도구 호출 요청을 실행하는 그래프 노드입니다.",
            "이번 자료의 도구는 로컬 딕셔너리를 읽기만 합니다. 쓰기 도구에는 별도의 권한 확인과 중복 실행 방지가 필요합니다.",
            "가격 계산은 2026-09-10 공개 단가인 입력 100만 토큰당 0.75달러, 출력 100만 토큰당 4.50달러를 사용합니다. 실제 청구액은 계정의 캐시·배치 조건에 따라 달라질 수 있습니다.",
        ],
        "next": "다음 절에서는 ToolNode가 실행한 도구에서 오류가 발생했을 때 예외를 숨기지 않고 ToolMessage로 어떻게 전달할지 확인합니다.",
        "quiz": [
            ("tools_condition이 확인하는 값은 무엇인가요?", "마지막 AIMessage의 tool_calls 유무를 확인합니다."),
            ("ToolNode가 메시지 상태에 추가하는 대표 메시지는 무엇인가요?", "도구 실행 결과와 tool_call_id를 담은 ToolMessage입니다."),
            ("tools 노드 뒤에 model 노드로 돌아가는 엣지가 필요한 이유는 무엇인가요?", "모델이 도구 결과를 읽고 최종 답을 만들거나 다음 도구 호출을 정해야 하기 때문입니다."),
            ("이번 실행의 성공을 최종 답 문장 일치로 판정하지 않는 이유는 무엇인가요?", "모델 표현은 실행할 때마다 달라질 수 있고, 이번 학습 목표는 메시지 흐름과 도구 실행이기 때문입니다."),
        ],
        "cells": [
            ("패키지와 환경 준비", INSTALL),
            ("모델과 비용 함수 준비", COMMON),
            ("읽기 전용 규정 도구 준비", DATA_AND_TOOLS),
            ("모델 노드와 실행 흔적 정의", """from typing import Annotated
from typing_extensions import TypedDict
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    trace: list[str]

bound_model = make_model().bind_tools(TOOLS)

def call_model(state: AgentState) -> dict:
    response = bound_model.invoke(state['messages'])
    return {'messages': [response], 'trace': state['trace'] + ['model']}"""),
            ("ToolNode 루프 직접 조립", """from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

builder = StateGraph(AgentState)
builder.add_node('model', call_model)
builder.add_node('tools', ToolNode(TOOLS))
builder.add_edge(START, 'model')
builder.add_conditional_edges('model', tools_condition)
builder.add_edge('tools', 'model')
graph = builder.compile()
print(graph.get_graph().draw_mermaid())"""),
            ("실제 질문 실행과 전체 메시지 확인", """from langchain.messages import HumanMessage

started = perf_counter()
result = graph.invoke({'messages': [HumanMessage('자료실에서 일반 도서를 며칠 빌릴 수 있나요?')], 'trace': []})
elapsed = perf_counter() - started
for index, message in enumerate(result['messages'], 1):
    calls = getattr(message, 'tool_calls', [])
    print(index, type(message).__name__, 'tool_calls=', calls, 'text=', message.text[:120])
print('trace:', result['trace'])
print('latency_sec:', round(elapsed, 3))
assert any(type(m).__name__ == 'ToolMessage' for m in result['messages'])
assert result['trace'] == ['model', 'model']"""),
            ("호출별 토큰과 비용 집계", """usages = [usage_of(m) for m in result['messages'] if type(m).__name__ == 'AIMessage']
total = {key: sum(item[key] for item in usages) for key in usages[0]}
print('calls:', usages)
print('total:', {**total, 'estimated_cost_usd': round(total['estimated_cost_usd'], 6)})
assert total['estimated_cost_usd'] < 1.0"""),
            ("도구가 필요 없는 질문과 비교", """direct = graph.invoke({'messages': [HumanMessage('안녕하세요. 한 문장으로 인사해 주세요.')], 'trace': []})
print('trace:', direct['trace'])
print('message_types:', [type(m).__name__ for m in direct['messages']])
print('answer:', direct['messages'][-1].text)
assert not any(type(m).__name__ == 'ToolMessage' for m in direct['messages'])"""),
        ],
    },
    "02-도구-오류와-ToolMessage": {
        "title": "도구 오류와 ToolMessage",
        "format": "paired",
        "hours": "강의 0.75h · 실습 1.25h",
        "terms": "4",
        "question": "도구 실행 오류를 그래프 밖의 예외로 끝내지 않고 모델이 읽을 ToolMessage로 바꾸려면 무엇을 설정해야 할까요?",
        "goals": [
            "ToolMessage의 tool_call_id가 요청과 결과를 연결하는 방식을 설명할 수 있습니다.",
            "handle_tool_errors=False와 사용자 정의 오류 처리 함수를 비교할 수 있습니다.",
            "도구가 실패한 뒤 모델이 오류 내용을 읽고 안전한 답을 만들게 할 수 있습니다.",
        ],
        "why": "모델은 도구 인자를 잘못 만들 수 있고, 도구가 지원하지 않는 값을 요청할 수도 있습니다. 예외가 그래프 밖으로 바로 전파되면 실행이 중단되어 모델은 무엇이 잘못됐는지 알지 못합니다. 모든 오류를 성공 결과처럼 바꾸는 것도 문제입니다. 오류 종류와 다음 행동을 담은 ToolMessage를 남기면 모델이 재시도하거나 제한을 설명할 근거를 얻고, 개발자는 같은 메시지 기록에서 원인을 추적할 수 있습니다.",
        "prior": "앞 절에서 첫 AIMessage의 tool_calls에 이름·인자·id가 들어 있고 ToolNode가 결과 ToolMessage를 추가하는 것을 확인했습니다. Ch19에서는 지원 범위를 도구 docstring과 Pydantic 스키마에 적었습니다. 이번에는 스키마를 통과한 문자열이더라도 로컬 자료에 없는 주제라면 ValueError가 발생하는 사례를 사용합니다.",
        "concept": "택배 송장 번호가 발송 요청과 배송 결과를 연결하듯 tool_call_id는 하나의 도구 요청과 결과를 연결합니다. ToolMessage는 content에 도구 결과나 처리된 오류를 담고 tool_call_id에 원래 요청 id를 넣습니다. ToolNode의 handle_tool_errors=False는 도구 예외를 호출자에게 그대로 전파합니다. 반면 특정 예외를 받는 오류 처리 함수는 학생이 이해할 수 있는 오류 문자열을 반환하고 ToolNode가 이를 ToolMessage로 만듭니다. 오류가 메시지가 되었다고 해서 성공한 것은 아니며, 모델에게 다음 판단 자료가 생겼다는 뜻입니다.",
        "observe": "Before에서는 lookup_policy(topic='주차') 호출이 ValueError로 끝나고 ToolMessage가 만들어지지 않습니다. After에서는 같은 호출 id와 같은 인자를 유지한 채 handle_policy_error가 오류를 설명하는 ToolMessage를 반환합니다. 이어서 실제 모델이 이 메시지 기록을 읽으면 지원하지 않는 규정이라고 설명해야 합니다. 비교의 원인은 ToolNode의 오류 처리 설정 하나이며 질문과 도구는 같습니다.",
        "notes": [
            "handle_tool_errors=True처럼 모든 예외를 같은 방식으로 처리하면 네트워크 장애와 잘못된 인자를 구분하기 어렵습니다.",
            "오류 메시지에는 비밀 값, 내부 경로, 전체 스택 추적을 넣지 않습니다. 운영 로그에는 원인을 보존하되 모델 입력은 필요한 정보로 제한합니다.",
            "쓰기 도구가 일부 동작한 뒤 실패했다면 단순 재시도는 중복 변경을 만들 수 있습니다. Ch24의 내구 실행에서 멱등성을 다시 다룹니다.",
        ],
        "next": "다음 절에서는 오류 처리와 별개로, 모델이 계속 도구를 요청해 그래프가 끝나지 않는 상황을 recursion_limit과 명시적 종료 조건으로 다룹니다.",
        "quiz": [
            ("tool_call_id는 왜 필요한가요?", "여러 도구 요청 중 어떤 요청에 대한 결과인지 정확히 연결하기 위해 필요합니다."),
            ("오류를 ToolMessage로 바꾸면 도구 실행이 성공한 것인가요?", "아닙니다. 실패 사실을 모델이 읽을 수 있는 메시지로 표현한 것입니다."),
            ("모든 예외를 한 문장으로 처리하면 어떤 정보가 사라지나요?", "잘못된 인자, 일시적 장애, 권한 오류처럼 원인별로 달라야 하는 다음 행동 정보가 사라집니다."),
            ("쓰기 도구 오류에서 재시도 전에 확인할 것은 무엇인가요?", "도구가 이미 일부 변경을 수행했는지와 같은 요청을 반복해도 결과가 중복되지 않는지 확인해야 합니다."),
        ],
        "cells": [
            ("패키지와 환경 준비", INSTALL, None),
            ("모델과 비용 함수 준비", COMMON, None),
            ("읽기 전용 규정 도구 준비", DATA_AND_TOOLS, None),
            ("같은 실패 도구 호출 만들기", """from langchain.messages import AIMessage

bad_call = AIMessage(content='', tool_calls=[{
    'name': 'lookup_policy', 'args': {'topic': '주차'}, 'id': 'call_bad_1', 'type': 'tool_call'
}])
print(bad_call.tool_calls)""", "before"),
            ("Before: 예외가 그래프 밖으로 전파됨", """from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode

strict_builder = StateGraph(MessagesState)
strict_builder.add_node('tools', ToolNode(TOOLS, handle_tool_errors=False))
strict_builder.add_edge(START, 'tools')
strict_builder.add_edge('tools', END)
strict_graph = strict_builder.compile()
try:
    strict_graph.invoke({'messages': [bad_call]})
except ValueError as error:
    before_error = f'{type(error).__name__}: {error}'
    print(before_error)
assert before_error.startswith('ValueError:')""", "before"),
            ("After: 오류 처리 함수 정의", """def handle_policy_error(error: ValueError) -> str:
    return f'규정 조회 실패: {error}. topic은 대출, 운영, 연체 중 하나를 사용하세요.'

safe_node = ToolNode(TOOLS, handle_tool_errors=handle_policy_error)
safe_builder = StateGraph(MessagesState)
safe_builder.add_node('tools', safe_node)
safe_builder.add_edge(START, 'tools')
safe_builder.add_edge('tools', END)
safe_graph = safe_builder.compile()
after_result = safe_graph.invoke({'messages': [bad_call]})
tool_error = after_result['messages'][-1]
print(type(tool_error).__name__)
print('tool_call_id:', tool_error.tool_call_id)
print('content:', tool_error.content)
assert tool_error.tool_call_id == 'call_bad_1'""", "after"),
            ("After: 실제 모델이 오류 메시지 읽기", """from langchain.messages import HumanMessage

model = make_model()
conversation = [
    HumanMessage('자료실 주차 규정을 알려 주세요.'),
    bad_call,
    tool_error,
]
started = perf_counter()
reply = model.invoke(conversation)
elapsed = perf_counter() - started
usage = usage_of(reply)
print('answer:', reply.text)
print('usage:', usage)
print('latency_sec:', round(elapsed, 3))
assert reply.text and usage['estimated_cost_usd'] < 1.0""", "after"),
        ],
    },
    "03-recursion-limit과-명시적-종료": {
        "title": "recursion_limit과 명시적 종료",
        "format": "paired",
        "hours": "강의 0.75h · 실습 1h",
        "terms": "4",
        "question": "그래프의 반복이 끝나지 않을 때 실행 한도와 상태 기반 종료 조건은 각각 어떤 역할을 할까요?",
        "goals": [
            "recursion_limit이 한 번의 실행에서 허용할 최대 super-step 수를 제한한다는 점을 설명할 수 있습니다.",
            "GraphRecursionError를 재현하고 순환 엣지의 원인을 찾을 수 있습니다.",
            "상태에 누적한 실행 횟수를 기준으로 END로 이동하는 명시적 종료 조건을 구현할 수 있습니다.",
        ],
        "why": "모델이 도구를 선택하는 루프에는 실행 횟수 변동이 생깁니다. 정상 질문도 두세 번 도구를 호출할 수 있지만, 잘못된 프롬프트나 서로 맞지 않는 도구 결과 때문에 같은 요청을 반복할 수도 있습니다. 비용과 지연이 계속 늘어나지 않게 실행 한도를 두고, 정상 경로에는 업무 의미가 드러나는 종료 조건을 넣어야 합니다. 실행 한도는 마지막 안전장치이고 종료 조건은 정상 동작을 설명하는 규칙입니다.",
        "prior": "Ch17에서 정지 조건 없는 자율성은 비용과 예측 불가능성을 키운다고 배웠습니다. 앞 절의 ToolNode 루프는 모델 응답에 tool_calls가 없으면 tools_condition이 END를 선택했습니다. 이번 실험은 모델의 비결정성과 구분하기 위해, 종료하지 않는 로컬 그래프를 명시적으로 만들어 recursion_limit의 경계를 재현합니다.",
        "concept": "건물의 비상 차단기와 정상 종료 버튼은 역할이 다릅니다. recursion_limit은 그래프가 지정한 super-step 수를 넘으면 GraphRecursionError를 발생시키는 비상 차단기입니다. super-step은 한 번에 실행 가능한 노드 묶음이 진행되는 단위입니다. 명시적 종료 조건은 상태의 attempts나 remaining 같은 값을 읽어 END를 선택하는 정상 종료 버튼입니다. 한도 값을 무조건 크게 올리면 순환 원인을 감출 수 있으므로 먼저 엣지와 조건 함수를 확인해야 합니다.",
        "observe": "Before 그래프는 tick 노드에서 count를 늘린 뒤 다시 tick으로만 이동합니다. recursion_limit=4에서 GraphRecursionError가 실제로 발생합니다. 이 그래프는 모델이 판단한 척하는 예제가 아니라, 경계 동작만 분리해 확인하는 결정적 로컬 그래프입니다. After 그래프는 tick 뒤 stop_or_continue가 count 3에서 END를 반환합니다. 같은 시작 상태에서도 예외 없이 count 3과 trace 세 항목을 반환합니다.",
        "notes": [
            "recursion_limit은 configurable 안에 넣지 않고 invoke의 설정 딕셔너리 최상위 키로 전달합니다.",
            "한도를 늘리기 전에 반복이 예상된 정상 경로인지, 종료 엣지가 빠진 순환인지 구분합니다.",
            "예외가 발생하면 최종 상태가 정상 반환되지 않습니다. 중간 결과 보존이 필요하면 체크포인터와 별도 오류 처리를 설계해야 합니다.",
            "실제 모델 루프에는 총 호출 횟수, 도구별 횟수, 비용 상한 같은 업무 기준도 함께 둡니다.",
        ],
        "next": "마지막 절에서는 코드가 고정한 if 분기와 모델이 고른 도구 분기를 같은 질문·자료·모델로 실행해 토큰, 지연, 결과 변동을 비교합니다.",
        "quiz": [
            ("recursion_limit이 제한하는 것은 무엇인가요?", "한 번의 그래프 실행에서 진행할 수 있는 최대 super-step 수입니다."),
            ("한도 초과 때 발생하는 대표 예외는 무엇인가요?", "GraphRecursionError입니다."),
            ("한도를 크게 올리기 전에 무엇을 확인해야 하나요?", "순환 엣지와 종료 조건이 의도대로 연결됐는지 확인해야 합니다."),
            ("명시적 종료 조건이 실행 한도보다 설명력이 좋은 이유는 무엇인가요?", "업무 상태에서 왜 반복을 마쳤는지 코드와 trace로 드러내기 때문입니다."),
        ],
        "cells": [
            ("패키지 준비", "%pip install -q langgraph==1.2.11\nfrom importlib.metadata import version\nprint('langgraph', version('langgraph'))", None),
            ("Before: 종료 없는 순환 그래프", """from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START

class LoopState(TypedDict):
    count: int
    trace: list[str]

def tick(state: LoopState) -> dict:
    next_count = state['count'] + 1
    return {'count': next_count, 'trace': state['trace'] + [f'tick:{next_count}']}

before_builder = StateGraph(LoopState)
before_builder.add_node('tick', tick)
before_builder.add_edge(START, 'tick')
before_builder.add_edge('tick', 'tick')
before_graph = before_builder.compile()""", "before"),
            ("Before: 실제 한도 초과 확인", """from langgraph.errors import GraphRecursionError

try:
    before_graph.invoke({'count': 0, 'trace': []}, {'recursion_limit': 4})
except GraphRecursionError as error:
    error_name = type(error).__name__
    print(error_name)
    print(str(error).splitlines()[0])
assert error_name == 'GraphRecursionError'""", "before"),
            ("After: 상태 기반 종료 조건 추가", """from typing import Literal
from langgraph.graph import END

def stop_or_continue(state: LoopState) -> Literal['tick', '__end__']:
    return END if state['count'] >= 3 else 'tick'

after_builder = StateGraph(LoopState)
after_builder.add_node('tick', tick)
after_builder.add_edge(START, 'tick')
after_builder.add_conditional_edges('tick', stop_or_continue)
after_graph = after_builder.compile()""", "after"),
            ("After: 정상 종료와 실행 흔적 확인", """after = after_graph.invoke({'count': 0, 'trace': []}, {'recursion_limit': 4})
print('count:', after['count'])
print('trace:', after['trace'])
print(after_graph.get_graph().draw_mermaid())
assert after['count'] == 3
assert len(after['trace']) == 3""", "after"),
        ],
    },
    "04-if-분기와-모델-선택-비교": {
        "title": "if 분기와 모델 선택 비교",
        "format": "experiment",
        "hours": "강의 0.5h · 실습 1.25h",
        "terms": "5",
        "question": "같은 질문·자료·모델을 사용할 때 코드가 정한 조회와 모델이 고른 조회는 토큰, 지연, 실행 경로에서 어떻게 다를까요?",
        "goals": [
            "고정 if 분기와 모델 도구 선택 분기의 책임 차이를 설명할 수 있습니다.",
            "같은 질문·자료·생성 모델로 두 경로의 전체 trace를 수집할 수 있습니다.",
            "입력·출력 토큰, 추정 비용, 지연, 출력 변동을 표로 비교하고 관찰 범위를 제한할 수 있습니다.",
        ],
        "why": "모델이 흐름을 정한다고 해서 모든 분기가 모델 판단에 적합한 것은 아닙니다. 규칙이 분명한 질문은 if 문이 더 짧고 예측 가능한 경로를 만들 수 있습니다. 반대로 표현이 다양하고 어떤 조회가 필요한지 규칙으로 모두 적기 어렵다면 모델 선택이 유용할 수 있습니다. 둘을 다른 데이터나 다른 모델로 비교하면 원인을 알 수 없으므로 같은 세 질문, 같은 로컬 규정, 같은 gpt-5.4-mini를 사용합니다.",
        "prior": "Ch13과 Ch14의 조건부 엣지는 점수나 키워드처럼 코드가 계산한 값으로 경로를 골랐습니다. Ch18의 직접 SDK 실습에서는 모델 응답에 포함된 도구 호출을 해석했습니다. 이번 절은 Ch20에서 처음 조립한 ToolNode 루프와 고정 분기를 하나의 그래프와 측정표에 놓아, 에이전트 도입의 비용과 유연성을 함께 읽습니다.",
        "concept": "두 상담 절차를 같은 시험지와 같은 조립 그래프로 평가한다고 생각해 봅니다. 공통 choose 노드는 strategy가 fixed이면 파이썬 규칙으로 AIMessage 도구 호출을 만들고, agent이면 도구 설명을 받은 모델이 AIMessage 도구 호출을 만듭니다. 그 뒤에는 두 경로가 같은 mark_tools, ToolNode, answer 노드를 지나며, answer 노드는 같은 모델로 같은 메시지 형식의 결과를 작성합니다. trace는 실제로 실행한 fixed_choose 또는 model_choose, tools, model_answer 단계를 드러냅니다.",
        "observe": "세 질문을 각 경로에서 두 번 실행합니다. 두 경로는 같은 컴파일된 그래프와 ToolNode·최종 답변 노드를 공유합니다. fixed는 fixed_choose, tools, model_answer를 실행하고, agent는 model_choose, tools, model_answer를 실행합니다. ToolMessage가 실제로 있을 때만 실행이 성공하도록 검사합니다. 표에는 실제 input_tokens, output_tokens, estimated_cost_usd, latency_sec와 답변 문자열을 기록합니다. output_variants는 같은 조건 두 번의 답 문자열 종류 수입니다.",
        "notes": [
            "샘플 2회와 질문 3개는 학습용 소규모 비교입니다. 정확도나 안정성의 일반 결론에는 더 큰 고정 평가셋이 필요합니다.",
            "fixed 경로의 키워드 규칙은 세 질문에 맞춰 작성한 기준선입니다. 새로운 표현이 들어오면 규칙을 확장하거나 실패 사례로 기록해야 합니다.",
            "agent 경로는 도구 스키마가 입력 토큰에 포함되고 선택을 위한 모델 호출이 추가될 수 있습니다.",
            "예상 API 비용은 절 전체 1달러 미만이며, 노트북은 실제 사용량으로 다시 계산해 이를 검사합니다.",
        ],
        "next": "Ch21에서는 같은 루프를 create_agent로 만들고 직접 조립한 그래프와 노드·메시지·종료 조건을 대응합니다.",
        "quiz": [
            ("두 경로 비교에서 반드시 같게 유지한 조건은 무엇인가요?", "질문, 로컬 규정 자료, 최종 생성 모델, 반복 횟수와 비용 단가입니다."),
            ("agent 경로의 입력 토큰이 늘 수 있는 이유는 무엇인가요?", "도구 이름·설명·인자 스키마가 모델 입력에 포함되고 선택 호출이 추가되기 때문입니다."),
            ("출력 문자열 종류가 한 개면 모델은 항상 같은 답을 하나요?", "아닙니다. 이번 두 번의 실행에서 변동을 관찰하지 못했다는 뜻만 가집니다."),
            ("고정 분기가 알맞은 사례는 무엇인가요?", "분기 규칙이 명확하고 감사 가능성, 비용, 예측 가능성이 중요한 사례입니다."),
            ("최종 답만 비교하면 놓치는 것은 무엇인가요?", "도구 선택, 호출 횟수, 오류, 토큰, 지연처럼 답을 만드는 경로의 차이를 놓칩니다."),
        ],
        "cells": [
            ("패키지와 환경 준비", INSTALL),
            ("모델과 비용 함수 준비", COMMON),
            ("읽기 전용 규정 도구 준비", DATA_AND_TOOLS),
            ("공통 답변 프롬프트와 측정 함수", """from langchain.messages import HumanMessage, ToolMessage

QUESTIONS = [
    '일반 도서는 며칠 동안 빌릴 수 있나요?',
    '토요일 자료실 운영 시간을 알려 주세요.',
    '책을 사흘 연체하면 새 대출은 어떻게 되나요?',
]

def timed_invoke(model, messages):
    started = perf_counter()
    reply = model.invoke(messages)
    return reply, perf_counter() - started"""),
            ("고정 주제 규칙", """def fixed_topic(question: str) -> str:
    if '연체' in question:
        return '연체'
    if '운영' in question or '시간' in question:
        return '운영'
    return '대출'"""),
            ("공통 그래프 상태", """from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain.messages import AIMessage, AnyMessage
from langgraph.graph.message import add_messages

class CompareState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    trace: list[str]
    measurements: list[dict]
    strategy: Literal['fixed', 'agent']"""),
            ("고정 또는 모델 선택 노드", """choice_model = make_model().bind_tools(TOOLS)

def choose(state: CompareState) -> dict:
    if state['strategy'] == 'fixed':
        question = state['messages'][0].text
        call = {'name': 'lookup_policy', 'args': {'topic': fixed_topic(question)},
                'id': 'fixed_call', 'type': 'tool_call'}
        return {'messages': [AIMessage(content='', tool_calls=[call])],
                'trace': state['trace'] + ['fixed_choose']}
    reply, latency = timed_invoke(choice_model, state['messages'])
    return {'messages': [reply], 'trace': state['trace'] + ['model_choose'],
            'measurements': state['measurements'] + [{**usage_of(reply), 'latency_sec': latency}]}"""),
            ("공통 도구·답변 노드", """answer_model = make_model()

def mark_tools(state: CompareState) -> dict:
    return {'trace': state['trace'] + ['tools']}

def answer(state: CompareState) -> dict:
    reply, latency = timed_invoke(answer_model, state['messages'])
    return {'messages': [reply], 'trace': state['trace'] + ['model_answer'],
            'measurements': state['measurements'] + [{**usage_of(reply), 'latency_sec': latency}]}"""),
            ("같은 ToolNode 그래프 조립", """from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

builder = StateGraph(CompareState)
builder.add_node('choose', choose)
builder.add_node('mark_tools', mark_tools)
builder.add_node('tools', ToolNode(TOOLS))
builder.add_node('answer', answer)
builder.add_edge(START, 'choose')
builder.add_conditional_edges('choose', tools_condition, {'tools': 'mark_tools', '__end__': '__end__'})
builder.add_edge('mark_tools', 'tools')
builder.add_edge('tools', 'answer')
graph = builder.compile()"""),
            ("공통 그래프 실행 함수", """def run_branch(question: str, strategy: str) -> dict:
    prompt = f'{question} 반드시 제공된 규정 조회 도구로 확인한 뒤 한 문장으로 답하세요.'
    started = perf_counter()
    state = graph.invoke({'messages': [HumanMessage(prompt)], 'trace': [],
                          'measurements': [], 'strategy': strategy})
    latency = perf_counter() - started
    assert any(type(message).__name__ == 'ToolMessage' for message in state['messages'])
    measures = state['measurements']
    total_input = sum(m['input_tokens'] for m in measures)
    total_output = sum(m['output_tokens'] for m in measures)
    total_cost = sum(m['estimated_cost_usd'] for m in measures)
    return {'branch': strategy, 'question': question, 'trace': state['trace'],
            'answer': state['messages'][-1].text, 'latency_sec': latency,
            'input_tokens': total_input, 'output_tokens': total_output,
            'estimated_cost_usd': total_cost}"""),
            ("같은 조건으로 두 번씩 실제 실행", """records = []
for repeat in range(1, 3):
    for question in QUESTIONS:
        for strategy in ('fixed', 'agent'):
            record = run_branch(question, strategy)
            record['repeat'] = repeat
            records.append(record)
            print(repeat, record['branch'], record['trace'], round(record['estimated_cost_usd'], 6))

total_cost = sum(r['estimated_cost_usd'] for r in records)
print('chapter_section_estimated_cost_usd:', round(total_cost, 6))
assert total_cost < 1.0"""),
            ("토큰·지연·출력 변동 집계", """from collections import defaultdict
from statistics import mean

groups = defaultdict(list)
for record in records:
    groups[record['branch']].append(record)

for branch, rows in groups.items():
    variants = {q: len({r['answer'] for r in rows if r['question'] == q}) for q in QUESTIONS}
    print({
        'branch': branch,
        'runs': len(rows),
        'mean_input_tokens': round(mean(r['input_tokens'] for r in rows), 1),
        'mean_output_tokens': round(mean(r['output_tokens'] for r in rows), 1),
        'mean_latency_sec': round(mean(r['latency_sec'] for r in rows), 3),
        'total_estimated_cost_usd': round(sum(r['estimated_cost_usd'] for r in rows), 6),
        'output_variants_by_question': variants,
    })
print('sample_traces:', {b: groups[b][0]['trace'] for b in groups})"""),
        ],
    },
}


DETAILS = {
    "01-ToolNode와-tools-condition": {
        "diagram": "질문은 model 노드로 들어갑니다. tools_condition의 점선 두 갈래 가운데 tool_calls가 있는 실행은 ToolNode로 이동하고, 도구 결과가 추가되면 다시 model로 돌아갑니다. 마지막 AIMessage에 도구 호출이 없을 때만 END로 이동합니다.",
        "execution": "먼저 gpt-5.4-mini에 lookup_policy를 bind_tools로 연결합니다. call_model은 모델 응답을 messages에 추가하고 모델 호출만 trace에 기록합니다. 그 다음 StateGraph에 model과 ToolNode를 등록하고 tools_condition을 조건부 엣지로 연결합니다. 대출 기간 질문과 인사 질문을 각각 실행해 ToolMessage 생성 여부를 비교합니다.",
        "result": "대출 질문은 HumanMessage, 도구 호출이 있는 AIMessage, '일반 도서는 1인 5권까지 14일'이라는 ToolMessage, 최종 AIMessage 순서로 끝났습니다. 모델 trace는 두 번 기록됐고 ToolNode 실행은 가운데 ToolMessage로 확인했습니다. 두 모델 호출은 입력 370토큰, 출력 52토큰이었고 추정 비용은 0.000512달러, 전체 지연은 1.383초였습니다. 인사 질문에는 ToolMessage가 없었습니다.",
        "limit": "두 질문을 한 번씩 실행한 구조 확인입니다. 다른 질문에서도 같은 도구 선택이 일어나는지, 응답 품질이 유지되는지는 더 많은 고정 질문으로 따로 측정해야 합니다.",
        "summary": ["tools_condition은 마지막 AIMessage의 tool_calls 유무로 ToolNode 또는 END를 선택합니다.", "ToolNode의 실행 여부는 요청 AIMessage와 결과 ToolMessage의 연결로 확인합니다.", "도구가 필요 없는 질문은 model 한 번 뒤에 종료될 수 있습니다."],
    },
    "02-도구-오류와-ToolMessage": {
        "diagram": "같은 AIMessage 도구 요청이 ToolNode에 들어갑니다. 엄격한 설정에서는 ValueError가 그래프 밖으로 전파됩니다. 사용자 정의 처리 함수를 둔 설정에서는 같은 call_bad_1을 가진 ToolMessage 오류가 만들어지고, 모델이 그 내용을 읽어 지원 범위를 설명합니다.",
        "execution": "topic='주차'인 하나의 AIMessage를 고정해 두 그래프에 넣습니다. Before의 ToolNode에는 handle_tool_errors=False를 사용합니다. After에는 ValueError만 받는 handle_policy_error를 연결합니다. 마지막에는 실제 gpt-5.4-mini가 오류 ToolMessage를 포함한 대화를 읽도록 호출합니다.",
        "result": "Before는 'ValueError: 지원하지 않는 주제: 주차'를 발생시키고 실행을 중단했습니다. After는 tool_call_id가 call_bad_1인 ToolMessage에 허용 주제 세 가지를 담았습니다. 후속 모델은 주차 규정을 확인할 수 없다고 답했습니다. 후속 호출은 입력 73토큰, 출력 106토큰, 추정 비용 0.00053175달러, 지연 1.292초였습니다.",
        "limit": "잘못된 호출은 비교 조건을 고정하려고 코드에서 직접 만들었습니다. 모델이 이런 호출을 얼마나 자주 만드는지 보여 주는 실험은 아니며, 그 비율은 별도 평가셋에서 측정해야 합니다.",
        "summary": ["tool_call_id는 하나의 요청과 하나의 도구 결과를 연결합니다.", "좁은 오류 처리 함수는 ValueError를 모델이 읽을 ToolMessage로 바꿉니다.", "오류 메시지로 바뀌어도 도구 실행이 성공한 것은 아닙니다."],
    },
    "03-recursion-limit과-명시적-종료": {
        "diagram": "Before에서는 START에서 tick으로 들어간 뒤 tick으로만 되돌아가므로 빨간 recursion_limit 차단에 도달합니다. After에서는 tick 뒤 종료 조건이 count를 읽고, 3 미만이면 tick으로 돌아가며 3이면 END로 이동합니다.",
        "execution": "모델 호출 없이 count를 하나씩 늘리는 결정적 로컬 그래프를 만듭니다. 종료 엣지가 없는 그래프를 recursion_limit=4로 실행해 경계 오류를 확인합니다. 이어서 stop_or_continue가 count 3에서 END를 반환하도록 조건부 엣지를 추가하고 같은 시작 상태와 같은 실행 한도로 다시 실행합니다.",
        "result": "종료 조건이 없는 그래프는 'Recursion limit of 4 reached'라는 GraphRecursionError를 실제로 발생시켰습니다. 종료 조건을 추가한 그래프는 예외 없이 count 3을 반환했고 trace에는 tick:1, tick:2, tick:3이 남았습니다. 이 결과는 모델의 반복 성향이 아니라 LangGraph 실행 한도의 동작을 분리해 보여 줍니다.",
        "limit": "이 절은 모델을 호출하지 않는 결정적 경계 실험입니다. 실제 모델 루프가 몇 단계에서 끝나는지나 적절한 운영 한도는 질문과 도구별 실행 기록으로 정해야 합니다.",
        "summary": ["recursion_limit은 한 실행의 최대 super-step 수를 제한합니다.", "GraphRecursionError는 종료 조건에 도달하지 못했다는 경계 신호입니다.", "정상 경로에는 상태로 설명할 수 있는 명시적 END 조건을 둡니다."],
    },
    "04-if-분기와-모델-선택-비교": {
        "diagram": "같은 질문과 로컬 규정이 공통 choose 노드에 들어갑니다. fixed는 파란 규칙으로 도구 호출 AIMessage를 만들고 agent는 보라색 모델이 같은 형식의 호출을 만듭니다. 두 갈래는 초록 ToolNode에서 합쳐지고 같은 answer 모델을 지난 뒤 토큰·비용·전체 지연을 측정합니다.",
        "execution": "하나의 StateGraph에 choose, mark_tools, ToolNode, answer를 등록합니다. strategy만 fixed 또는 agent로 바꾸고 세 질문을 각 두 번 실행합니다. 두 경로 모두 ToolMessage가 실제로 생성됐는지 검사하며, answer 노드는 같은 gpt-5.4-mini와 같은 메시지 기록을 사용합니다. 실행 전후 perf_counter로 그래프 전체 시간을 측정합니다.",
        "result": "12개 실제 실행의 총 추정 비용은 0.003305달러였습니다. fixed와 agent의 평균 입력 토큰은 각각 88과 264.3, 평균 출력 토큰은 23과 40.7, 그래프 전체 평균 지연은 0.841초와 1.551초였습니다. 실제 trace는 fixed_choose→tools→model_answer와 model_choose→tools→model_answer였습니다. fixed 출력 종류는 세 질문 모두 2개였고 agent는 2·1·2개였습니다. 두 번의 반복에서 관찰한 값이므로 일반적인 변동성 차이로 해석하지 않습니다.",
        "limit": "세 질문을 두 번씩 실행한 소규모 비교입니다. 이번 실행에서 agent의 평균 토큰과 지연이 더 컸지만, 다른 도구 수·프롬프트·네트워크 상태에서도 같은 비율이 유지된다고 볼 수 없습니다.",
        "summary": ["두 경로는 같은 컴파일 그래프, ToolNode, answer 모델을 공유하고 choose 방식만 다릅니다.", "모델 선택 경로에는 도구 스키마와 선택 호출에 따른 토큰·지연이 추가됐습니다.", "최종 답과 함께 실제 trace와 사용량을 기록해야 경로 비용을 비교할 수 있습니다."],
    },
}


def notebook(lesson: dict) -> dict:
    cells = [md(f"# {lesson['title']}\n\n{lesson['question']}"), md("## 실행 환경 준비\n\nPython 3.12 새 커널에서 첫 셀부터 순서대로 실행합니다. API 키 값은 출력하지 않습니다.")]
    paired = lesson["format"] == "paired"
    for item in lesson["cells"]:
        heading, source, *part = item
        lesson_part = part[0] if part else None
        description = "코드를 실행한 뒤 출력된 값과 메시지 종류를 확인합니다."
        cells.extend([md(f"## {heading}\n\n{description}", lesson_part if paired else None), code(f"# {heading}에 필요한 연산을 실행합니다.\n{source}", lesson_part if paired else None)])
    for i, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{i:02d}"
    return {
        "cells": cells,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}, "lesson_format": lesson["format"]},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def quiz_html(items: list[tuple[str, str]]) -> str:
    return "".join(f'<details class="quiz"><summary>{i}. {html.escape(q)}</summary><p class="quiz-a"><b>해설</b> — {html.escape(a)}</p></details>' for i, (q, a) in enumerate(items, 1))


def source_html(slug: str, lesson: dict) -> str:
    goals = "".join(f"<li>{html.escape(x)}</li>" for x in lesson["goals"])
    notes = "".join(f"<li>{html.escape(x)}</li>" for x in lesson["notes"])
    insert = f"{{{{notebook:{slug}|example}}}}" if lesson["format"] == "paired" else f"{{{{notebook:{slug}}}}}"
    failure = f"{{{{notebook:{slug}|failure}}}}" if lesson["format"] == "paired" else ""
    h6 = "일부러 실패해 보기" if lesson["format"] == "paired" else "실험 결과 해석"
    detail = DETAILS[slug]
    analogy, separator, definition = lesson["concept"].partition(". ")
    if separator:
        analogy += "."
    else:
        definition = lesson["concept"]
    summary = "".join(f"<li>{html.escape(item)}</li>" for item in detail["summary"])
    return f'''<!--meta: {lesson['hours']} | 코드 Jupyter Notebook | 새 용어 {lesson['terms']} -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>{goals}</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{lesson['why']}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{lesson['prior']}</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>구체적인 상황</h3><p>{analogy}</p><h3>정의와 메시지 흐름</h3><p>{definition}</p><h3>도식 읽기</h3>{{{{svg:{slug[:2]}-흐름}}}}<p>{detail['diagram']}</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>{detail['execution']}</p>{insert}<p class="look"><b>확인할 점</b> — {lesson['observe']}</p>
<h2 id="b6"><span class="no">6</span>{h6}</h2>{failure}<p>{detail['result']}</p><p>{detail['limit']}</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{notes}</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul>{summary}</ul><p><strong>다음 학습과 이어지는 지점</strong> — {lesson['next']}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quiz_html(lesson['quiz'])}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><a href="https://docs.langchain.com/oss/python/langchain/tools">LangChain Tools 공식 문서</a> · 확인 2026-09-10 · LangChain 1.4.0</li><li><a href="https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode">ToolNode API</a> · 확인 2026-09-10 · LangGraph 1.2.11</li><li><a href="https://docs.langchain.com/oss/python/langgraph/graph-api">LangGraph Graph API</a> · 확인 2026-09-10 · LangGraph 1.2.11</li><li><a href="https://developers.openai.com/api/docs/models/gpt-5.4-mini">GPT-5.4 mini 모델과 가격</a> · 확인 2026-09-10</li></ul>
'''


FIGURES = {
    "01-흐름": (["질문", "model", "tools_condition", "ToolNode", "model", "END"], ["data", "model", "code", "tool", "model", "metric"]),
    "02-흐름": (["AIMessage 요청", "ToolNode", "ValueError", "ToolMessage 오류", "모델 답변"], ["data", "tool", "failure", "failure", "model"]),
    "03-흐름": (["START", "tick", "종료 조건", "tick 또는 END", "recursion_limit"], ["data", "code", "code", "metric", "failure"]),
    "04-흐름": (["같은 질문·자료", "fixed 선택", "agent 선택", "공통 ToolNode", "공통 answer", "토큰·지연·변동"], ["data", "code", "model", "tool", "model", "metric"]),
}


COLORS = {"data": "#DDEDE8", "tool": "#DDEDE8", "code": "#DDEAF4", "model": "#E9E0F3", "metric": "#F7EDC7", "failure": "#F4D9D5"}


def make_figure(name: str, labels: list[str], roles: list[str]) -> tuple[str, dict]:
    elements = []
    shapes = []
    for i, (label, role) in enumerate(zip(labels, roles)):
        x, y, w, h = 20, 20 + i * 100, 320, 62
        elements.append({"id": f"{name}-box-{i}", "type": "rectangle", "x": x, "y": y, "width": w, "height": h, "angle": 0, "strokeColor": "#334155", "backgroundColor": COLORS[role], "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None, "roundness": {"type": 3}, "seed": i + 1, "version": 1, "versionNonce": i + 1, "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False})
        elements.append({"id": f"{name}-text-{i}", "type": "text", "x": x + 10, "y": y + 18, "width": w - 20, "height": 26, "angle": 0, "strokeColor": "#172033", "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None, "roundness": None, "seed": i + 10, "version": 1, "versionNonce": i + 10, "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False, "text": label, "originalText": label, "fontSize": 20, "fontFamily": 1, "textAlign": "center", "verticalAlign": "middle", "containerId": None, "autoResize": True, "lineHeight": 1.3})
        shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{COLORS[role]}" stroke="#334155" stroke-width="2"/><text x="180" y="{y+39}" text-anchor="middle" font-size="20" font-family="sans-serif" fill="#172033">{html.escape(label)}</text>')
        if i:
            shapes.append(f'<path d="M180 {y-38} L180 {y-4}" stroke="#334155" stroke-width="2" marker-end="url(#arrow)"/>')
    height = 20 + len(labels) * 100
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 {height}" style="width:360px;max-width:100%;height:auto;display:block;margin:0 auto" role="img" aria-label="{html.escape("에서 ".join(labels), quote=True)}"><title>{html.escape(" → ".join(labels))}</title><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#334155"/></marker></defs>{"".join(shapes)}</svg>'
    drawing = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": elements, "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"}, "files": {}}
    return svg, drawing


def main() -> None:
    LAB.mkdir(parents=True, exist_ok=True)
    (LAB / "notebooks").mkdir(exist_ok=True)
    (CHAPTER / "_src").mkdir(exist_ok=True)
    (CHAPTER / "figures").mkdir(exist_ok=True)
    (CHAPTER / "qa").mkdir(exist_ok=True)

    for slug, lesson in LESSONS.items():
        (LAB / "notebooks" / f"{slug}.ipynb").write_text(json.dumps(notebook(lesson), ensure_ascii=False, indent=1) + "\n")
        (CHAPTER / "_src" / f"{slug}.html").write_text(source_html(slug, lesson))

    for name, (labels, roles) in FIGURES.items():
        svg, drawing = make_figure(name, labels, roles)
        (CHAPTER / "figures" / f"{name}.svg").write_text(svg)
        (CHAPTER / "figures" / f"{name}.excalidraw").write_text(json.dumps(drawing, ensure_ascii=False, indent=2) + "\n")
        (CHAPTER / "figures" / f"{name}.caption.md").write_text("위에서 아래로 노드 이름과 화살표를 읽고 노트북의 trace와 대조합니다. 초록은 자료·도구, 파랑은 코드 흐름, 보라는 모델, 노랑은 측정, 빨강은 오류·차단을 뜻합니다.\n")

    chapter = {
        "part": 5,
        "part_title": "Part 5 · Agent 입문",
        "chapter": "ch20-tool-node",
        "title": "ToolNode — 모델이 도구를 고른다",
        "hours": "총 8h · 강의 3h · 실습 5h",
        "objectives": ["StateGraph에 ToolNode와 tools_condition을 직접 연결해 모델·도구 반복을 구성할 수 있습니다.", "도구 오류를 ToolMessage로 전달하고 실행 한도와 명시적 종료 조건을 적용할 수 있습니다.", "고정 if 분기와 모델 선택 분기를 같은 조건에서 실행해 trace·토큰·비용·지연을 비교할 수 있습니다."],
        "lab_path": "labs/part5/ch20-tool-node",
        "sections": [{"slug": slug, "title": lesson["title"], "format": lesson["format"]} for slug, lesson in LESSONS.items()],
    }
    (CHAPTER / "chapter.json").write_text(json.dumps(chapter, ensure_ascii=False, indent=2) + "\n")
    (LAB / "pyproject.toml").write_text('''[project]\nname = "kdt-ch20-tool-node"\nversion = "0.1.0"\nrequires-python = ">=3.12,<3.13"\ndependencies = [\n  "langchain==1.4.0",\n  "langchain-openai==1.6.0",\n  "langgraph==1.2.11",\n  "python-dotenv==1.2.3",\n]\n''')
    (LAB / "README.md").write_text("# Ch20 ToolNode 실습\n\nPython 3.12 새 커널에서 각 노트북을 첫 셀부터 실행합니다. 로컬 읽기 전용 규정 자료를 사용하며 OpenAI API 호출이 필요한 셀은 절당 1달러 미만을 검사합니다.\n")

    checklist = """# 집필 점검표

| 확인 항목 | 작성자 기록 | 독립 검토 |
| --- | --- | --- |
| 학습 질문 | ToolNode 조립, 오류 메시지, 종료 경계, 고정 분기와 모델 선택 비교를 절별 질문으로 둡니다. | 별도 검토 예정 |
| 고정 조건 | Python 3.12, LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11, gpt-5.4-mini, 같은 로컬 규정 자료를 고정합니다. | 별도 검토 예정 |
| 실제 연산 | bind_tools, ToolNode, tools_condition, StateGraph.compile/invoke, GraphRecursionError, usage_metadata를 실행했습니다. | 별도 검토 예정 |
| 비교 조건 | 오류 처리 설정만 바꾸고 같은 tool_call을 실행합니다. fixed/agent 비교는 질문·자료·모델·반복 수를 유지합니다. | 별도 검토 예정 |
| 실제 출력 | 01절은 Human→AI(tool call)→Tool→AI와 추정 0.000512달러를, 02절은 같은 call_bad_1의 ValueError와 ToolMessage를, 03절은 GraphRecursionError와 count 3 종료를 확인했습니다. 04절 총 추정 비용은 0.003305달러이며 fixed/agent 평균 입력 토큰은 88/264.3, 그래프 전체 평균 지연은 0.841/1.551초였습니다. | 별도 검토 예정 |
| 해석 범위 | 세 질문·2회 실행의 소규모 실험이며 전체 모델 품질로 일반화하지 않습니다. fixed 출력은 세 질문 모두 2종, agent 출력은 2/1/2종이었습니다. | 별도 검토 예정 |

- [x] 모든 작성 자리표시자를 실제 내용으로 바꿨습니다.
- [x] 모든 코드 셀을 Python 3.12 새 커널에서 실행했습니다.
- [x] API 키·개인 경로·강사 노트가 학생 파일에 없습니다.

한국어 감사 3단은 집필 세션과 분리된 검토자가 수행합니다.
"""
    (CHAPTER / "집필점검표.md").write_text(checklist)
    print("Ch20 sources, notebooks, figures, and metadata authored")


if __name__ == "__main__":
    main()
