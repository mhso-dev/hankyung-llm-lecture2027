"""Ch 21 01절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_01.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_01.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR01_NB_ONLY=1 python3 author_01.py → 노트북만 다시 쓴다
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**(chapter.json).

## 결정 1 — 모델 객체와 create_agent (챕터 리드 결정 1·2·5)

과정 표준 모델 셀(`nbkit.key_and_model_cells`, temperature=0·reasoning_effort="none")로 만든 모델 **객체**를
`create_agent(model, tools=[…], system_prompt=…)`에 넘긴다(Ch 22 모양). 모델 이름 글자만 넘기는 모양은 쓰지 않는다.
`draw_mermaid_png()`(mermaid.ink 바깥 요청)는 빼고 `draw_mermaid()` 구조 문자열만. 걸린 시간은 재지 않는다.
`system_prompt`는 Ch 16 말 「시스템 메시지(글)」로 부른다.

## 결정 2 — 소재는 Ch 20 01 그대로 (챕터 리드 결정 3)

`POLICY_DATA` 셀은 Ch 20 01 `author_01.py`의 같은 이름 상수와 문자열까지 같다(아래 `check_same_as_ch20()`가 확인).
`DEF_TOOL`은 코드 줄이 같고, 셀 안 주석 한 줄만 「02절」→「Ch 20 02절」로 적었다(이 챕터 02절은 구조화 출력이라 오해 방지).
`LOAN_ARGS`·`LOAN_IDS`·`LOAN_ANSWER`·`TWO_ARGS`도 Ch 20 01 셀과 문자열까지 같다.

## 결정 3 — 도구 파일 runner_tools.py (챕터 리드 결정 6)

`labs/part6/ch21-create-agent/notebooks/runner_tools.py`를 이 절이 만든다. Ch 20 `graph_tools.py`에서 이 절이 쓰는
`tool_call_names`(Ch 19 04, show_messages 안에서)·`show_messages`(Ch 19 06)·`sum_usage`(Ch 19 05)·`estimate_cost`(Ch 6 06)·
`call_id_lists`(Ch 20 01)를 본문 글자 그대로(AST 대조) 옮겼다. `run_row`는 결과의 `trace` 칸을 읽어 옮기지 않았다.

## 결정 4 — 흔들림 먼저 확인 (챕터 리드 결정 8, qa/upgrade/01-probe.md)

노트북 밖에서 L(대출)·G(인사)·T(운영·연체) 세 질문을 5번씩(25요청) 보냈다. 메시지 종류·도구 이름·인자·한 응답의 요청 수·
호출 ID 짝이 15/15 같아 입력을 그대로 쓴다. 모델 답에 건 assert는 없고, assert는 호출 ID 짝에만 건다.

## 모델 요청

노트북 한 번 **5번**(6절 2 · 7절 1 · 8절 2, 모델이 도구를 부르는 수에 따름). 읽는 파일·쓰는 파일 0.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·세미콜론·
`isinstance`·별표 풀기·`try`·`@dataclass`·클래스 정의·`draw_mermaid_png`·`stream`·`perf_counter`·`recursion_limit`.
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch21-create-agent/notebooks"
FIGS = ROOT / "textbook/part6/ch21-create-agent/figures"
SLUG = "01-create-agent와-ReAct-루프"
SRC = ROOT / "textbook/part6/ch21-create-agent/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR01_RUNSEC", "10초 안에")

INSTALL = install_source([
    "langchain==1.4.0", "langchain-core==1.6.2", "langchain-openai==1.6.0", "langgraph==1.2.11", "numpy==2.5.3",
    "python-dotenv==1.2.3",
])

IMPORTS = r'''# 에이전트를 만드는 함수 create_agent와, Ch 19에서 쓴 모델·메시지·도구 이름을 가져옵니다
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool

# 앞 챕터에서 배운 함수 넷은 도구 파일에서 가져옵니다
from runner_tools import call_id_lists, estimate_cost, show_messages, sum_usage

print("이 절에서 새로 가져온 이름:", "create_agent")'''

POLICY_DATA = r'''# 교육센터 자료실 규정 셋을, 주제어를 키로 한 딕셔너리에 담습니다(도구가 읽기만 하는 자료)
POLICIES = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
}
topics = list(POLICIES.keys())
print("규정 주제어:", topics)'''

DEF_TOOL = r'''# 주제어 하나로 규정 글 하나를 찾는 도구를 만듭니다(맨 @tool 줄 — Ch 19 01절)
@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다."""
    # 딕셔너리에 없는 주제어면 오류를 냅니다(이 오류를 그래프 안에서 다루는 법은 Ch 20 02절에서 보았습니다)
    if topic not in POLICIES:
        raise ValueError("지원하지 않는 주제: " + topic)
    return POLICIES[topic]'''

AGENT = r'''# 모델 객체·도구 목록·시스템 메시지 글을 넘겨 에이전트 그래프를 만듭니다(요청은 아직 보내지 않음)
system_text = "교육센터 자료실 안내 도우미입니다. 자료실 규정을 묻는 질문에는 lookup_policy 도구로 찾은 규정 글에 근거해 답하세요."
agent = create_agent(model, tools=[lookup_policy], system_prompt=system_text)
print("만든 것의 종류:", type(agent).__name__)'''

STRUCTURE = r'''# 에이전트 그래프가 스스로 그린 구조 문자열을 받아 옵니다(Ch 13 01절 draw_mermaid)
structure_text = agent.get_graph().draw_mermaid()
print("그래프가 그린 구조:")
print(structure_text)'''

NODES = r'''# 설계 객체에서 등록된 노드, 엣지 수, 상태 칸, 노드 tools의 종류를 봅니다
agent_builder = agent.builder
print("등록된 노드:", list(agent_builder.nodes))
print("고정 엣지로 적힌 수:", len(agent_builder.edges))
print("조건부 엣지를 적은 노드 수:", len(agent_builder.branches))
print("상태 칸:", list(agent_builder.channels))
# 노드마다 속성 runnable에 실제로 실행할 것이 들어 있습니다
tools_node = agent_builder.nodes["tools"].runnable
print("노드 tools의 종류:", type(tools_node).__name__)'''

BRANCHES = r'''# 조건부 엣지마다 조건 함수의 이름과 갈 수 있는 곳을 봅니다
for source in agent_builder.branches:
    specs = agent_builder.branches[source]
    for name in specs:
        # 속성 ends는 이름표와 갈 곳을 이은 딕셔너리라, 값만 모으면 갈 수 있는 곳입니다
        ends = list(specs[name].ends.values())
        print(source, "| 조건 함수:", name, "| 갈 수 있는 곳:", ends)'''

LOAN_RUN = r'''# 규정을 찾아야 답할 수 있는 질문으로 에이전트 그래프를 실행합니다(모델 노드를 지날 때마다 모델 요청 1번)
loan_question = "자료실에서 일반 도서를 며칠 빌릴 수 있나요?"
loan_state = {"messages": [HumanMessage(content=loan_question)]}
loan_result = agent.invoke(loan_state)
result_keys = list(loan_result.keys())
print("결과 딕셔너리의 키:", result_keys)
print("메시지 칸의 메시지 수:", len(loan_result["messages"]))'''

LOAN_SHOW = r'''# 메시지 칸을 차례로 출력합니다(Ch 19 06절 함수 show_messages)
print("메시지 칸:")
show_messages(loan_result["messages"])'''

KINDS = r'''# 메시지 칸의 종류 이름을 모아, 시스템 메시지가 들어 있는지 셉니다
kinds = []
for message in loan_result["messages"]:
    kinds.append(type(message).__name__)
print("메시지 종류:", kinds)
print("시스템 메시지 수:", kinds.count("SystemMessage"))'''

LOAN_ARGS = r'''# 둘째 메시지(첫 응답)에 담긴 도구 호출 요청의 이름과 인자를 봅니다
first_response = loan_result["messages"][1]
for call in first_response.tool_calls:
    print("도구 이름:", call["name"], "| 인자:", call["args"])'''

LOAN_IDS = r'''# 대출 질문 흐름에서 요청 id 목록과 호출 ID 목록이 같은 차례로 짝이 맞는지 봅니다
loan_ids = call_id_lists(loan_result["messages"])
print("요청 id 수:", len(loan_ids["요청 id"]))
print("호출 ID 수:", len(loan_ids["호출 ID"]))
print("짝이 맞는가:", loan_ids["요청 id"] == loan_ids["호출 ID"])
# 도구 실행 노드가 옮겨 적는 값이라 매번 같아야 합니다
assert loan_ids["요청 id"] == loan_ids["호출 ID"], "도구 메시지마다 같은 차례의 요청 id가 옮겨져야 합니다"'''

LOAN_ANSWER = r'''# 메시지 칸의 마지막 응답을 봅니다(도구 호출 요청 수와 답 글)
last_message = loan_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(last_message.tool_calls))
print("답 글:")
print(last_message.content)'''

GREET_RUN = r'''# 규정을 찾을 까닭이 없는 인사 질문으로 같은 에이전트 그래프를 실행합니다(모델 요청 1번 예상)
greet_question = "안녕하세요. 한 문장으로 인사해 주세요."
greet_state = {"messages": [HumanMessage(content=greet_question)]}
greet_result = agent.invoke(greet_state)
print("메시지 칸:")
show_messages(greet_result["messages"])
print("답 글:", greet_result["messages"][-1].content)'''

TWO_RUN = r'''# 바꿀 값: 질문 하나만, 규정 두 가지가 필요한 질문으로 바꿔 같은 에이전트 그래프를 실행합니다
two_question = "자료실 운영 시간과 연체 규정을 함께 알려 주세요."
two_state = {"messages": [HumanMessage(content=two_question)]}
two_result = agent.invoke(two_state)
print("메시지 칸:")
show_messages(two_result["messages"])'''

TWO_ARGS = r'''# 응답마다 도구 호출 요청 수와 인자를 차례로 보고, 호출 ID 짝을 셉니다
for message in two_result["messages"]:
    if type(message).__name__ == "AIMessage":
        print("응답 | 도구 호출 요청 수:", len(message.tool_calls))
        for call in message.tool_calls:
            print("  인자:", call["args"])
two_ids = call_id_lists(two_result["messages"])
print("호출 ID 짝이 맞는가:", two_ids["요청 id"] == two_ids["호출 ID"])'''

USAGE = r'''# 대출 질문 흐름의 응답 둘에서 요청 수와 입력·출력 토큰을 더합니다(Ch 19 05절 함수 sum_usage)
loan_usage = sum_usage(loan_result["messages"])
print("대출 질문 사용량:", loan_usage)'''

COST = r'''# 2026-09-17 요금표(100만 토큰당 달러)로 대출 질문 흐름의 예상 비용을 셉니다(Ch 6 06절 함수 estimate_cost)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
loan_cost = estimate_cost(loan_usage, input_rate, cached_input_rate, output_rate)
rounded_cost = round(loan_cost, 6)
print("대출 질문 예상 비용(달러):", rounded_cost)'''

DEF_ROW = r'''# 실행 결과 하나를 기록 한 줄로 만듭니다(모델 요청 수 = 응답 메시지 수)
def agent_row(question_name, result):
    ids = call_id_lists(result["messages"])
    usage = sum_usage(result["messages"])
    row = {"질문": question_name}
    row["모델 요청 수"] = usage["requests"]
    row["도구 메시지 수"] = len(ids["호출 ID"])
    row["호출 ID 짝"] = ids["요청 id"] == ids["호출 ID"]
    return row'''

TABLE = r'''# 세 질문의 기록을 모아 라벨 줄 아래에 한 줄씩 출력합니다
agent_rows = []
agent_rows.append(agent_row("대출 질문", loan_result))
agent_rows.append(agent_row("인사 질문", greet_result))
agent_rows.append(agent_row("운영·연체 질문", two_result))
print("질문 | 모델 요청 수 | 도구 메시지 수 | 호출 ID 짝")
for row in agent_rows:
    print(row["질문"], "|", row["모델 요청 수"], "|", row["도구 메시지 수"], "|", row["호출 ID 짝"])'''


def check_same_as_ch20() -> None:
    """Ch 20 01 생성기의 같은 이름 셀과 문자열로 대조합니다(「글자까지 같다」는 이 대조가 근거)."""
    path = ROOT / "textbook/part5/ch20-tool-node/qa/upgrade/author_01.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    ch20 = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            ch20[node.targets[0].id] = node.value.value
    for name in ["POLICY_DATA", "LOAN_ARGS", "LOAN_IDS", "LOAN_ANSWER", "TWO_ARGS"]:
        assert globals()[name] == ch20[name], name + " 셀이 Ch 20 01과 다릅니다"
    # 도구 셀은 주석을 뺀 코드 줄만 같게 둡니다(주석 한 줄만 「Ch 20 02절」로 고침)
    mine = [line for line in DEF_TOOL.splitlines() if not line.strip().startswith("#")]
    theirs = [line for line in ch20["DEF_TOOL"].splitlines() if not line.strip().startswith("#")]
    assert mine == theirs, "도구 셀의 코드 줄이 Ch 20 01과 다릅니다"


FIG1 = "01-1-한-줄이-만든-에이전트-그래프"
FIG1_ALT = "위에서 아래로 읽는 그림으로 맨 위 초록 상자 모델 객체 도구 목록 시스템 메시지 글에서 회색 상자 create_agent 한 줄로 화살표가 가고, 거기서 에이전트 그래프 agent CompiledStateGraph 칸으로 화살표가 갑니다. 칸 안에서는 회색 가상 시작점 START에서 회색 상자 모델 노드 model create_agent가 만듦으로 실선이 가고, 모델 노드에서 점선 두 갈래가 나갑니다. 한 갈래는 model_to_tools 요청 있음 라벨을 달고 회색 상자 도구 실행 노드 tools ToolNode로, 다른 갈래는 model_to_tools 요청 없음 라벨을 달고 회색 가상 끝점 END로 갑니다. 도구 실행 노드에서 모델 노드로 tools_to_model 되돌아가는 엣지라는 점선이 올라가는 그림"
FIG1_CAP = "값 셋을 넘긴 create_agent 한 줄이 상자 넷의 에이전트 그래프를 내놓고, 그 안의 갈래는 모두 점선입니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 우리가 넘긴 값 셋이고, 그 아래 회색 상자는 라이브러리가 준 함수 create_agent를 부르는 줄입니다.
칸 안의 회색 상자와 가상 시작점·끝점은 create_agent가 만든 것이고, 노트북 5절 구조 문자열의 상자 넷과 같습니다.
모델 노드에서 나가는 두 갈래와 도구 실행 노드에서 돌아오는 엣지는 모두 조건부 엣지라 점선입니다.
점선 라벨의 이름은 노트북 5절에서 출력한 조건 함수 이름입니다."""

FIG2 = "01-2-손으로-이은-그래프와-견주기"
FIG2_ALT = "위아래 칸 둘이 있는 그림으로 위 칸 Ch 20 01절 손으로 이은 그래프에는 파란 상자 모델 노드 함수 call_model에서 tools_condition 라벨의 점선 두 갈래가 회색 상자 도구 실행 노드 ToolNode와 회색 END로 가고, 도구 실행 노드에서 모델 노드로 고정 엣지 실선이 돌아옵니다. 아래 칸 이 절 create_agent가 만든 그래프에는 회색 상자 모델 노드 create_agent가 만듦에서 model_to_tools 라벨의 점선 두 갈래가 회색 상자 도구 실행 노드 ToolNode와 회색 END로 가고, 도구 실행 노드에서 모델 노드로 tools_to_model 점선이 돌아오는 그림"
FIG2_CAP = "노드 이름과 도구 실행 노드는 같고, 갈래를 고르는 조건 함수와 되돌아가는 엣지의 모양이 다릅니다."
FIG2_READ = """위 칸이 Ch 20 01절 그래프, 아래 칸이 이 절의 에이전트 그래프입니다.
두 칸에서 같은 자리의 상자가 같은 일을 맡습니다.
파란 상자는 Ch 20에서 우리가 적은 모델 노드이고, 회색은 라이브러리가 만든 것입니다.
위 칸의 되돌아가는 엣지는 실선이고, 아래 칸은 조건 함수가 붙은 점선입니다.
가상 시작점은 두 칸이 같아 그리지 않았습니다."""

FIG3 = "01-3-대출-질문의-실제-차례"
FIG3_ALT = "세로선 셋이 있는 차례 그림으로 왼쪽부터 노트북 코드 agent.invoke, 연보라 띠 안의 모델 노드 model gpt-5.4-mini, 도구 실행 노드 tools입니다. 노트북 코드가 모델 노드에 질문 하나를 보내고, 노란 메모 소스 확인 요청마다 시스템 메시지를 앞에 붙임과 요청 1 도구 호출 요청 lookup_policy 주제어 대출이 붙습니다. 모델 노드에서 도구 실행 노드로 model_to_tools 요청 하나 화살표가 가고, 노란 메모 도구 메시지 success 1인 5권까지 14일이 붙습니다. 도구 실행 노드에서 모델 노드로 tools_to_model 되돌아가는 엣지가 오고, 노란 메모 요청 2 도구 호출 요청 0건 뒤에 모델 노드에서 노트북 코드로 model_to_tools END 점선이 가며, 마지막 노란 메모에 메시지 넷, 키 messages 하나, 시스템 메시지 0, 호출 ID 짝 True가 적힌 그림"
FIG3_CAP = "대출 질문에서 에이전트 그래프는 모델 노드, 도구 실행 노드, 모델 노드 차례로 지나고 두 번째 응답에서 끝났습니다."
FIG3_READ = "위에서 아래로 읽고, 세로선은 왼쪽부터 노트북 코드, 모델 노드, 도구 실행 노드입니다. 연보라 띠는 실제로 부른 모델 `gpt-5.4-mini`가 있는 자리입니다. 「소스 확인」이 붙은 첫 메모만 설치판 소스로 본 동작이고, 나머지 노란 메모는 노트북 6절 출력입니다. 요청 1의 응답에 도구 호출 요청이 있어 도구 실행 노드로 갔고, 요청 2의 응답에는 요청이 없어 끝났습니다."

FIG4 = "01-4-세-질문의-응답과-도구-메시지"
FIG4_ALT = "위쪽에 칸 셋이 나란히 있는 그림으로 왼쪽 칸 대출 질문에는 초록 상자 자료실에서 일반 도서를 며칠 빌릴 수 있나요에서 노란 상자 응답 둘 모델 요청 두 번 도구 메시지 하나 대출로 화살표가 갑니다. 가운데 칸 인사 질문에는 초록 상자 안녕하세요 한 문장으로 인사해 주세요에서 노란 상자 응답 하나 모델 요청 한 번 도구 메시지 없음 도구 실행 안 됨으로 갑니다. 오른쪽 칸 바꾼 값 운영·연체 질문에는 초록 상자 자료실 운영 시간과 연체 규정을 함께 알려 주세요에서 노란 상자 첫 응답에 요청 둘, 모델 요청 두 번, 도구 메시지 둘, 운영 연체로 갑니다. 맨 아래 회색 상자에는 위 두 줄에 세 질문 공통 호출 ID 짝 True, 아래 세 줄에 Ch 20 01절 교재 출력 운영·연체 질문 모델 요청 세 번이 적힌 그림"
FIG4_CAP = "같은 에이전트 그래프에 질문만 바꾸자 모델 요청은 두 번·한 번·두 번, 도구 메시지는 하나·없음·둘이었습니다."
FIG4_READ = "위쪽 칸 셋은 왼쪽부터 대출·인사·운영과 연체 질문입니다. 초록 상자가 질문이고, 노란 상자가 노트북 10절과 7·8절 출력입니다. 오른쪽 칸이 값 바꿔 보기로 바꾼 질문입니다. 맨 아래 회색 상자의 위 두 줄은 세 칸 출력에서 모두 확인한 공통점이고, 아래 세 줄은 Ch 20 01절 교재 출력입니다. 칸끼리는 화살표로 잇지 않았습니다."

ILLU = "01-5-코스-버튼-하나인-세탁기"
ILLU_ALT = os.environ.get("AUTHOR01_ILLU_ALT", "흰 바탕 그림으로 벽과 바닥이 보이는 방입니다. 왼쪽 바닥에 파란 둥근 대야, 나무 빨래판, 회색 헹굼 통 세 가지가 사이를 두고 떨어져 놓여 있습니다. 오른쪽에는 흰 앞문형 세탁기 한 대가 크게 놓여 있고, 윗면에 둥근 버튼 하나, 앞면에 둥근 유리창 하나가 있습니다. 유리창 안에서 빨강·노랑·초록·파랑 빨래가 한데 엉켜 돌고 있는 그림")
ILLU_CAP = "따로 놓인 손빨래 도구 셋과 달리, 세탁기 한 대는 버튼 하나를 누르면 안에서 빨래가 되풀이해 돕니다."
ILLU_READ = os.environ.get("AUTHOR01_ILLU_READ", "왼쪽 바닥에는 파란 대야, 나무 빨래판, 회색 헹굼 통 세 가지가 사이를 두고 떨어져 있습니다. 오른쪽에는 둥근 버튼 하나와 둥근 유리창 하나가 달린 세탁기 한 대가 있습니다. 유리창 안에서는 여러 색 빨래가 한데 돌고 있습니다. 떨어진 도구 셋은 Ch 20에서 손으로 이은 부품이고, 세탁기는 에이전트 그래프입니다. 유리창은 안에서 도는 반복을 보여 주는 구조 문자열과 메시지 칸입니다.")

TITLE = """# create_agent와 ReAct 루프

**이 노트북에서 할 일**

1. Ch 20에서 손으로 이은 모델과 도구의 반복 그래프를 함수 `create_agent` 한 줄로 만듭니다.
2. 만든 그래프의 노드·엣지·조건 함수 이름을 출력해, Ch 20 그래프와 같은 점과 다른 점을 찾습니다.
3. 세 질문을 보내 메시지 칸의 응답 수·도구 메시지 수와 호출 ID 짝을 셉니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 교재 출력에서 모델 요청은 모두 5번입니다.
6절에서 2번, 7절에서 1번, 8절에서 2번을 보냈습니다.
모델이 도구를 몇 번 부르느냐에 따라 요청 수가 달라질 수 있습니다.
요금표로 어림한 예상 비용은 모두 합쳐 0.01달러 아래이고, 청구 금액이 아닙니다.

도구는 노트북 안 규정 딕셔너리를 읽기만 하고, 읽는 파일과 새로 쓰는 파일은 없습니다.
앞 챕터에서 배운 함수 넷은 도구 파일 `runner_tools.py`에서 가져옵니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.
모델 응답을 기다리는 시간은 네트워크와 실행 때에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0입니다.
langgraph 1.2.11, numpy 2.5.3, python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~6절을 읽습니다.
자료와 도구를 만들고, 에이전트 그래프를 만들어 모양을 보고, 첫 질문을 보내는 자리입니다.
7~10절은 질문을 바꿔 보내고 Ch 20 그래프와 견주는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch21-create-agent`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""

MAP_LIST = """- 도구를 모델에게 알려 주는 `bind_tools`는 `create_agent`가 안에서 부르고, 여럿 담기 값은 넣지 않습니다.
- 메시지 칸과 실행 흔적 칸을 둔 상태 형식은, 칸 `messages`·`jump_to`·`structured_response`인 상태로 바뀝니다.
- 우리가 적은 모델 노드 `call_model`은, `create_agent`가 만든 이름 `model`인 노드가 맡습니다.
- 도구 실행 노드 `ToolNode(tools)`는 이름도 종류도 같은 노드 `tools`가 맡습니다.
- 도구 조건 함수 `tools_condition`은 조건 함수 `model_to_tools`가 맡습니다.
- 실선이던 되돌아가는 엣지 `add_edge("tools", "model")`는 조건 함수 `tools_to_model`의 점선이 맡습니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

Ch 20 01절에서는 모델 노드·도구 실행 노드·도구 조건 함수·되돌아가는 엣지를 하나씩 이어 그래프를 만들었습니다.
이 절에서는 같은 반복을 함수 `create_agent` 한 줄로 만듭니다.
제목의 ReAct는 Ch 7 05절에서 본 말로, 생각과 행동을 번갈아 하는 방식입니다.
모델이 다음 행동을 고르고, 코드가 도구를 실행하고, 그 결과를 다시 모델에게 보여 주는 반복입니다.

첫 셀은 패키지 여섯 개를 설치하고 설치된 판 번호를 출력합니다.
뒤에서 가져오는 도구 파일이 NumPy를 쓰므로, numpy도 함께 설치합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`·`langchain-core: 1.6.2`·`langchain-openai: 1.6.0`이 보입니다.
출력 줄 `langgraph: 1.2.11`·`numpy: 2.5.3`·`python-dotenv: 1.2.3`도 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모델·메시지·도구 이름은 Ch 19와 Ch 20에서 쓴 이름입니다.
새 이름은 모듈 `langchain.agents`에서 가져오는 함수 `create_agent` 하나입니다.
Ch 20에서 쓴 그래프 이름(`StateGraph`·`ToolNode`·`tools_condition`)은 가져오지 않습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 절에서 새로 가져온 이름: create_agent`가 보입니다.
모듈 `langchain.agents`는 에이전트를 만드는 도구를 모아 둔 곳입니다.

앞에서 배운 함수는 `runner_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

이 파일은 Ch 20 도구 파일 `graph_tools.py`와 다른 파일입니다.
이 절이 쓰는 함수는 Ch 20 파일에서 본문을 글자 그대로 옮긴 것입니다.
같은 파일에는 뒤 절이 쓰는 함수도 함께 들어 있습니다.
파일 맨 위에서 NumPy를 가져오므로, 첫 셀에서 `numpy`도 설치했습니다.

함수 `show_messages`는 Ch 19 06절, `sum_usage`는 Ch 19 05절에서 배웠습니다.
함수 `estimate_cost`는 Ch 6 06절, `call_id_lists`는 Ch 20 01절에서 배웠습니다.

함수 `show_messages`가 안에서 쓰는 Ch 19 04절 함수 `tool_call_names`도 함께 옮겼습니다.
Ch 20 01절 함수 `run_row`는 옮기지 않았고, 까닭은 10절에서 봅니다.

## 2. 키와 모델 준비

모델은 Ch 20과 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다.
이 절은 이렇게 만든 모델 객체를 `create_agent`에 넘깁니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도, 모델이 도구 호출 요청을 보낼지가 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. 규정 자료와 도구

이 챕터는 Ch 20에 이어 교육센터 자료실 규정을 소재로 씁니다.
다음 셀은 Ch 20 01절 셀과 글자까지 같은 코드입니다.
주제어를 키, 규정 글을 값으로 둔 딕셔너리를 만듭니다."""),
        code(POLICY_DATA),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '운영', '연체']`로 키 셋을 확인합니다.
도구는 이 딕셔너리를 읽기만 하므로, Ch 19 06절 말로 읽기 도구입니다.

다음 셀도 Ch 20 01절의 도구 셀과 코드 줄이 같습니다.
셀 안 주석 한 줄만 이 챕터에 맞게 「Ch 20 02절」로 적었습니다.
맨 `@tool` 줄과 독스트링, 매개변수의 `: str` 표시는 Ch 19 01절에서 배운 모양입니다.
딕셔너리에 없는 주제어면 Ch 16 01절처럼 `raise`로 오류를 냅니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
독스트링은 도구 설명이 되어 모델 요청에 실립니다.
설명에 주제어 셋을 적어, 모델이 인자에 무엇을 넣을지 알게 했습니다.

## 4. create_agent 한 줄

Ch 20 01절에서는 도구를 모델에게 알려 주고, 상태 형식과 모델 노드를 적었습니다.
그다음 노드 둘을 등록하고 엣지 셋을 이어 컴파일했습니다.
함수 `create_agent`는 이 일을 한 번에 맡아, 컴파일한 그래프를 내놓습니다.
이 절에서는 이 그래프를 에이전트 그래프라고 부릅니다.

넘기는 값은 셋입니다.
첫째 자리에 모델 객체, 인자 `tools`에 도구 목록을 넣습니다.
인자 `system_prompt`에는 시스템 메시지 글을 넣습니다.
시스템 메시지는 Ch 16 03절에서 본, 모델이 따를 규칙을 담은 메시지입니다.
Ch 20의 그래프는 시스템 메시지를 쓰지 않았습니다."""),
        code(AGENT),
        md("""**결과 읽기** — 출력 줄 `만든 것의 종류: CompiledStateGraph`입니다.
Ch 20 01절에서 `builder.compile()`이 내놓은 것과 같은 종류입니다.
이 줄에서는 모델 요청이 나가지 않고, 질문을 넣어 실행할 때 나갑니다.

설치한 langchain 1.4.0 소스로 보면, 이 함수는 안에서 메서드 `bind_tools`로 도구를 모델에게 알려 줍니다.
소스(`factory.py` 995~996행)를 보면, 모델 이름 글자만 넘길 때는 기본 설정으로 모델을 새로 만듭니다.
그래서 이 절은 temperature 0으로 만든 모델 객체를 넘겼습니다.

## 5. 에이전트 그래프의 모양

다음 셀은 Ch 20 01절처럼 그래프가 스스로 그린 구조 문자열을 받아 옵니다.
Ch 20 01절 구조 문자열과 무엇이 같고 무엇이 다른지 봅니다."""),
        code(STRUCTURE),
        md("""**결과 읽기** — 라벨 줄 `그래프가 그린 구조:` 아래에서 상자 줄 넷과 화살표 줄 넷을 봅니다.
상자는 `__start__`·`model`·`tools`·`__end__` 넷으로, Ch 20 01절 구조 문자열과 같습니다.
줄 `model -.-> __end__`와 `model -.-> tools`는 조건부 엣지의 두 갈래라 점선입니다.
되돌아가는 엣지 줄 `tools -.-> model`도 점선입니다.
Ch 20 01절 출력에서는 이 줄이 실선 `tools --> model`이었습니다.

구조 문자열의 점선은 조건부 엣지라는 표시입니다.
되돌아가는 엣지가 왜 조건부 엣지인지는 다음 두 셀에서 봅니다.

컴파일한 그래프는 속성 `builder`에 설계 객체를 담아 둡니다.
설계 객체의 속성 `nodes`·`edges`는 Ch 20 01절에서, `branches`는 Ch 20 03절에서 보았습니다.
속성 `channels`에는 상태 칸 이름이 들어 있습니다."""),
        code(NODES),
        md("""**결과 읽기** — 출력 줄 `등록된 노드: ['model', 'tools']`로, 노드 이름은 Ch 20 01절과 같습니다.
출력 줄 `고정 엣지로 적힌 수: 1`은 시작 엣지 하나이고, Ch 20 01절은 되돌아가는 엣지까지 둘이었습니다.
출력 줄 `조건부 엣지를 적은 노드 수: 2`로, 모델 노드와 도구 실행 노드 모두에 조건부 엣지가 있습니다.
출력 줄 `상태 칸: ['messages', 'jump_to', 'structured_response']`는 Ch 20 01절 상태와 다릅니다.
출력 줄 `노드 tools의 종류: ToolNode`로, 도구 실행 노드는 Ch 20과 같은 종류입니다.

Ch 20 01절 상태 형식의 칸은 메시지 칸 `messages`와 실행 흔적 칸 `trace` 둘이었습니다.
에이전트 그래프에는 실행 흔적 칸이 없어, 흔적 칸 길이로 모델 요청을 셀 수 없습니다.
설치판 소스로 보면 칸 `jump_to`는 라이브러리가 그래프 안에서만 쓰는 칸입니다.
칸 `structured_response`는 02절 구조화 출력에서 봅니다.

속성 `branches`는 조건부 엣지를 적은 노드마다, 조건 함수 이름을 키로 한 딕셔너리를 담습니다.
그 딕셔너리 값의 속성 `ends`는 이름표와 갈 곳을 이은 딕셔너리로, Ch 13 03절 이름표 표와 같은 모양입니다.
다음 셀은 조건 함수 이름과 갈 수 있는 곳을 출력합니다."""),
        code(BRANCHES),
        md("""**결과 읽기** — 출력 줄 `tools | 조건 함수: tools_to_model | 갈 수 있는 곳: ['model']`이 먼저 나옵니다.
출력 줄 `model | 조건 함수: model_to_tools | 갈 수 있는 곳: ['tools', '__end__']`이 다음입니다.
모델 노드 뒤 조건 함수의 이름은 `model_to_tools`이고, Ch 20의 도구 조건 함수 `tools_condition`이 아닙니다.
도구 실행 노드 뒤에도 조건 함수 `tools_to_model`이 붙어, 되돌아가는 엣지가 점선으로 그려졌습니다.
이 조건 함수가 갈 수 있는 곳은 `model` 하나라, 이 에이전트 그래프에서는 늘 모델 노드로 돌아갑니다.

설치한 langchain 1.4.0 소스(`factory.py` 28행)도 `ToolNode`만 가져오고 `tools_condition`은 가져오지 않습니다.
소스로 보면 조건 함수 `model_to_tools`는 마지막 응답에 도구 호출 요청이 없으면 끝으로 보냅니다.
요청이 있으면 요청마다 도구 실행 노드를 따로 부릅니다(소스 1923~1975행).

소스(2004~2037행)를 보면 조건 함수 `tools_to_model`이 끝으로 가는 경우는 둘뿐입니다.
도구를 부르자마자 끝내는 설정의 도구와, 02절에서 보는 구조화 출력용 도구가 있을 때입니다.
이 두 경우는 이번에 실행하지 않았습니다.

## 6. 도구가 필요한 질문

첫 질문은 Ch 20 01절 7절과 같은 대출 질문입니다.
입력 상태에는 메시지 칸에 질문 하나만 넣습니다.
실행 흔적 칸이 없으므로, Ch 20처럼 빈 흔적 목록을 넣지 않습니다.

실행 전에 예상해 봅니다.
모델이 대출 규정을 찾는 요청을 보내면, 모델 노드 → 도구 실행 노드 → 모델 노드 차례로 지날 것입니다."""),
        code(LOAN_RUN),
        md("""**결과 읽기** — 출력 줄 `결과 딕셔너리의 키: ['messages']`로, 결과에는 메시지 칸 하나만 나왔습니다.
출력 줄 `메시지 칸의 메시지 수: 4`입니다.
질문 하나에 메시지 셋이 더해졌습니다.

설치판 소스로 보면 칸 `jump_to`는 결과에서 빠지게 적혀 있습니다.
구조화 출력을 쓰지 않아, 칸 `structured_response`에는 값이 생기지 않았습니다.

다음 셀은 Ch 19 06절 함수 `show_messages`로 메시지 칸을 차례로 출력합니다."""),
        code(LOAN_SHOW),
        md("""**결과 읽기** — 라벨 줄 `메시지 칸:` 아래 네 줄이 메시지 칸의 차례입니다.
질문 다음 줄은 `AIMessage | 도구 호출 요청: ['lookup_policy']`입니다.
셋째 줄 도구 메시지는 결과 상태가 `success`이고, 내용은 대출 규정 글입니다.
넷째 줄 `AIMessage | 도구 호출 요청: []`는 요청이 없는 응답이라, 조건 함수가 끝으로 보냈습니다.
모델을 부르고, 모델이 요청한 도구를 실행하고, 다시 모델을 부른 흐름입니다.

Ch 20 01절 7절 메시지 네 줄과 종류·차례가 같습니다.

4절에서 넘긴 시스템 메시지가 메시지 칸에 들어갔는지 봅니다.
Ch 16 03절에서는 시스템 메시지가 대화 기록의 첫 메시지였습니다.
다음 셀은 메시지 칸의 종류 이름을 모아 셉니다."""),
        code(KINDS),
        md("""**결과 읽기** — 출력 줄 `메시지 종류: ['HumanMessage', 'AIMessage', 'ToolMessage', 'AIMessage']`입니다.
출력 줄 `시스템 메시지 수: 0`으로, 시스템 메시지는 메시지 칸에 남지 않았습니다.

설치판 소스(`factory.py` 1451~1452행)로 보면, 모델 노드는 요청마다 시스템 메시지를 메시지 앞에 붙여 보냅니다.
요청에 실린 모습은 이번 출력으로는 보이지 않습니다.

다음 셀은 첫 응답에 담긴 도구 호출 요청의 이름과 인자를 봅니다."""),
        code(LOAN_ARGS),
        md("""**결과 읽기** — 출력 줄 `도구 이름: lookup_policy | 인자: {'topic': '대출'}`입니다.
모델이 질문을 읽고 주제어 `대출`을 골라 인자에 넣었습니다.
도구를 부를지와 인자는 모델이 정했고, 도구를 실행한 것은 도구 실행 노드입니다.

다음 셀은 도구 파일 함수 `call_id_lists`로 요청 id 목록과 호출 ID 목록을 모아, 짝이 맞는지 봅니다.
이 목록은 도구 실행 노드가 옮겨 적는 값이라, 모델이 요청을 몇 건 보내든 짝이 맞아야 합니다.
그래서 셀 끝에서 `assert`로 확인합니다."""),
        code(LOAN_IDS),
        md("""**결과 읽기** — 출력 줄 `요청 id 수: 1`과 `호출 ID 수: 1`입니다.
출력 줄 `짝이 맞는가: True`로, 도구 실행 노드가 요청 `id`를 도구 메시지에 옮겨 적었습니다.
칸 `id`의 값은 요청마다 새로 붙어 실행마다 다르므로, 여기에 옮겨 적지 않습니다.

다음 셀은 메시지 칸의 마지막 응답을 봅니다."""),
        code(LOAN_ANSWER),
        md("""**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
라벨 줄 `답 글:` 아래가 모델이 도구 메시지를 읽고 쓴 최종 답입니다.

답 글의 문장은 실행마다 달라질 수 있어, 결론에 쓰지 않습니다.
이번 실행에서는 답 글에 도구 메시지의 `1인 5권까지`와 `14일`이 들어 있었습니다.
답 글의 별표 두 개(`**`)는 모델이 굵은 글씨를 표시하려고 붙인 기호입니다.

## 7. 도구가 필요 없는 질문

둘째 질문은 Ch 20 01절 8절과 같은 인사입니다.
같은 에이전트 그래프에 질문만 바꿔 넣습니다.
실행 전에 예상해 봅니다.
모델이 도구 호출 요청 없이 바로 답하면, 모델 노드를 한 번만 지나고 끝날 것입니다."""),
        code(GREET_RUN),
        md("""**결과 읽기** — 라벨 줄 `메시지 칸:` 아래는 `HumanMessage`와 `AIMessage | 도구 호출 요청: []` 두 줄입니다.
첫 응답에 요청이 없어, 조건 함수 `model_to_tools`가 바로 끝으로 보냈습니다.
도구 실행 노드는 한 번도 실행되지 않았고, 모델 요청은 1번입니다.

답 글은 실행마다 달라질 수 있습니다.
이번 실행에서는 `안녕하세요, 무엇을 도와드릴까요?`였습니다.
노트북 밖에서 이 질문을 다섯 번 보냈을 때도 다섯 번 모두 도구 호출 요청이 없었습니다.

## 8. 값 바꿔 보기 · 규정 두 가지를 묻는 질문

바꿀 값은 질문 하나입니다.
운영 시간과 연체 규정을 함께 묻는, Ch 20 01절 9절과 같은 질문으로 바꿉니다.
Ch 20에서는 `bind_tools(tools, parallel_tool_calls=False)`로 한 응답에 요청을 하나까지만 받았습니다.
함수 `create_agent`에는 이 값을 넣는 인자가 없습니다.
설치판 소스(`factory.py` 1431~1436행)도 이 값 없이 도구를 알려 줍니다.

langchain-openai 1.6.0 소스 설명으로는, 이 값을 보내지 않으면 여럿 담기가 켜진 채로 요청됩니다.
실행 전에 예상해 봅니다.
한 응답에 요청 둘이 함께 오면, 모델 요청은 Ch 20의 3번보다 적은 2번일 것입니다."""),
        code(TWO_RUN),
        md("""**결과 읽기** — 라벨 줄 `메시지 칸:` 아래 다섯 줄입니다.
둘째 줄은 `AIMessage | 도구 호출 요청: ['lookup_policy', 'lookup_policy']`로, 한 응답에 요청 둘이 들었습니다.
그 뒤에 도구 메시지 둘이 이어지고, 둘 다 결과 상태가 `success`입니다.
마지막 줄 `AIMessage | 도구 호출 요청: []`가 최종 답입니다.

다음 셀은 응답마다 도구 호출 요청 수와 인자를 보고, 호출 ID 짝을 셉니다.
Ch 20 01절 9절과 같은 코드입니다."""),
        code(TWO_ARGS),
        md("""**결과 읽기** — 첫 응답은 `응답 | 도구 호출 요청 수: 2`이고, 인자는 `{'topic': '운영'}`과 `{'topic': '연체'}`입니다.
둘째 응답은 `응답 | 도구 호출 요청 수: 0`이라 최종 답입니다.
출력 줄 `호출 ID 짝이 맞는가: True`로, 두 도구 메시지 모두 짝이 맞았습니다.

Ch 20 01절 9절에서는 요청이 응답마다 한 건씩 와서 모델 요청이 3번이었습니다.
여기서는 한 응답에 두 건이 함께 와서 모델 요청이 2번입니다.
설치판 소스로 보면 조건 함수 `model_to_tools`는 Ch 13 05절의 `Send`로 요청마다 도구 실행 노드를 따로 부릅니다.
두 도구 실행이 한 단계 안에서 함께 도는지는 이번에 세지 않았습니다.

## 9. 사용량과 예상 비용

다음 셀은 Ch 19 05절 함수 `sum_usage`로 대출 질문 흐름의 요청 수와 토큰을 더합니다.
함수가 세는 요청 수는 메시지 칸의 응답(`AIMessage`) 수입니다.
모델 노드가 한 번 돌 때마다 응답이 하나 붙으므로, 이 수가 곧 모델 요청 수입니다."""),
        code(USAGE),
        md("""**결과 읽기** — 라벨 `대출 질문 사용량:` 뒤 딕셔너리에서 `'requests': 2`는 응답 둘, 곧 모델 요청 2번입니다.
입력 토큰은 `'input_tokens': 456`으로, 두 요청의 입력을 더한 값입니다.
설치판 소스로 보면 요청마다 시스템 메시지와 도구 명세가 함께 실립니다.

출력 토큰은 실행마다 달라질 수 있습니다.
이번 실행에서는 `'output_tokens': 44`였습니다.

다음 셀은 Ch 6 06절 함수 `estimate_cost`로 이 사용량의 예상 비용을 셉니다.
요금은 2026-09-17 요금표의 100만 토큰당 달러입니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 `대출 질문 예상 비용(달러):` 뒤 값이 요금표로 어림한 예상 비용이고, 청구 금액이 아닙니다.
사용량에 캐시 입력 칸이 없어, 입력 토큰은 모두 입력 요금으로 셌습니다.

출력 토큰이 실행마다 달라질 수 있어, 이 값도 달라질 수 있습니다.
이번 실행에서는 `0.00054`달러였습니다.

## 10. Ch 20 그래프와 견주기

Ch 20 01절 함수 `run_row`는 실행 흔적 칸의 길이로 모델 요청 수를 셌습니다.
에이전트 그래프의 결과에는 흔적 칸이 없어, 그 함수를 그대로 쓸 수 없습니다.
다음 셀은 응답 수로 모델 요청 수를 세는 함수를 새로 만듭니다."""),
        code(DEF_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `agent_row`는 칸 넷을 담은 딕셔너리를 내놓습니다.
칸은 질문·모델 요청 수·도구 메시지 수·호출 ID 짝입니다.
모델 요청 수는 함수 `sum_usage`가 센 응답 수입니다.

다음 셀은 세 질문의 기록을 모아 한 줄씩 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 세 줄입니다.
대출 질문은 `대출 질문 | 2 | 1 | True`입니다.
인사 질문은 `인사 질문 | 1 | 0 | True`입니다.
바꾼 질문은 `운영·연체 질문 | 2 | 2 | True`입니다.

Ch 20 01절 10절 표에서 모델 요청은 2·1·3번, 도구 메시지는 1·0·2개였습니다.
대출·인사 질문은 같고, 운영·연체 질문만 모델 요청이 하나 적습니다.
한 응답에 요청 둘이 함께 왔기 때문입니다.
그래서 「모델 요청 수 = 도구 메시지 수 + 1」은 요청을 하나씩 받을 때만 맞는 셈입니다.
세 질문 모두 호출 ID 짝은 맞았습니다.

Ch 20 01절에서 손으로 이은 부품이 에이전트 그래프에서 맡는 곳은 아래와 같습니다.

""" + MAP_LIST + """

## 정리

1. 함수 `create_agent` 한 줄로 만든 에이전트 그래프에도 노드 `model`·`tools`와 상자 넷이 있었습니다.
2. 갈래는 조건 함수 `model_to_tools`·`tools_to_model`이 맡아, 되돌아가는 엣지도 점선이었습니다.
3. 대출·인사·운영과 연체 질문의 모델 요청은 2·1·2번, 도구 메시지는 1·0·2개였습니다.

02절에서는 `create_agent`가 답을 정해 둔 양식으로 내놓게 하는 구조화 출력 두 가지를 봅니다."""),
    ]


def html_text(text: str) -> str:
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다."""
    parts = text.replace("\n", " ").split("`")
    out = ""
    for index in range(len(parts)):
        if index % 2 == 1:
            out = out + "<code>" + parts[index] + "</code>"
        else:
            out = out + parts[index]
    return out


L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH07_05 = "../../part2/ch07-prompt-engineering/05-CoT와-ReAct의-경계.html"
L_CH13_01 = "../../part4/ch13-langgraph-basics/01-StateGraph와-노드-엣지.html"
L_CH13_03 = "../../part4/ch13-langgraph-basics/03-조건부-엣지.html"
L_CH13_05 = "../../part4/ch13-langgraph-basics/05-Send-동적-팬아웃.html"
L_CH16_03 = "../../part4/ch16-guardrails/03-히스토리-트리밍과-요약.html"
L_CH17_03 = "../../part5/ch17-agent-overview/03-모델-도구-루프와-정지-조건.html"
L_CH19_01 = "../../part5/ch19-model-tools/01-tool과-Ch4-함수-재사용.html"
L_CH19_04 = "../../part5/ch19-model-tools/04-설명만으로-도구-선택하기.html"
L_CH19_05 = "../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH20_01 = "../../part5/ch20-tool-node/01-ToolNode와-tools-condition.html"
L_CH20_02 = "../../part5/ch20-tool-node/02-도구-오류와-ToolMessage.html"
L_CH20_03 = "../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html"
L_CH22_01 = "../ch22-middleware/01-미들웨어와-6개-훅.html"
L_02 = "02-구조화-출력-두-전략.html"

COMPARE_ROWS = [
    ("도구 알려 주기", "<code>bind_tools(tools, parallel_tool_calls=False)</code>", "안에서 <code>bind_tools</code>, 여럿 담기 값 없음(소스)"),
    ("상태 칸", "<code>messages</code>·<code>trace</code>", "<code>messages</code>·<code>jump_to</code>·<code>structured_response</code>, 결과 키는 <code>messages</code>"),
    ("모델 노드", "우리가 적은 <code>call_model</code>, 이름 <code>model</code>", "<code>create_agent</code>가 만든 노드, 이름 <code>model</code>"),
    ("도구 실행 노드", "<code>ToolNode(tools)</code>, 이름 <code>tools</code>", "<code>ToolNode</code>, 이름 <code>tools</code>"),
    ("모델 뒤 갈래", "도구 조건 함수 <code>tools_condition</code>", "조건 함수 <code>model_to_tools</code>"),
    ("되돌아가는 엣지", "고정 엣지, 구조 문자열 실선", "조건 함수 <code>tools_to_model</code>, 점선"),
    ("시스템 메시지", "쓰지 않음", "<code>system_prompt</code>, 메시지 칸에는 남지 않음"),
]


def compare_table_html() -> str:
    body = ""
    for part, left, right in COMPARE_ROWS:
        body = body + "<tr><td>" + part + "</td><td>" + left + "</td><td>" + right + "</td></tr>"
    return ("<table><thead><tr><th>부품</th><th>Ch 20 01절(손으로 이음)</th><th>이 절(<code>create_agent</code>)</th></tr></thead><tbody>"
            + body + "</tbody></table>")


def illustration_block() -> str:
    """삽화 PNG가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file():
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def src_html() -> str:
    return """<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>함수 <code>create_agent</code>에 모델 객체·도구 목록·시스템 메시지 글을 넘겨 에이전트 그래프를 만들 수 있습니다.</li>
<li>에이전트 그래프의 노드·엣지·조건 함수 이름을 출력해, Ch 20 그래프와 같은 점과 다른 점을 말할 수 있습니다.</li>
<li>메시지 칸의 응답 수·도구 메시지 수·호출 ID 짝으로 반복이 몇 번 돌았는지 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_CH20_01 + """\">Ch 20 01절</a>에서는 모델 노드·도구 실행 노드·도구 조건 함수·되돌아가는 엣지를 하나씩 이어 그래프를 만들었습니다. 모델이 도구 호출 요청을 보내면 도구를 실행하러 가고, 보내지 않으면 끝나는 그래프였습니다. 이 모양은 도구를 쓰는 에이전트마다 되풀이됩니다.</p><p>라이브러리 LangChain은 이 반복을 함수 <code>create_agent</code> 한 줄로 만들어 줍니다. 그러나 한 줄로 만든 그래프도 안에서는 노드와 엣지가 돕니다. 답이 이상하거나 흐름이 멈추면, 어느 노드를 몇 번 지났는지 읽어야 까닭을 찾을 수 있습니다.</p><p>이 절은 한 줄로 만든 그래프를 Ch 20의 그래프와 나란히 놓고 읽습니다. 같은 질문 셋을 보내, 메시지 칸에 남은 흐름이 Ch 20과 어디서 같고 어디서 다른지 셉니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH07_05 + """\">Ch 7 05절</a>에서는 생각과 행동을 번갈아 하는 방식을 ReAct라고 불렀습니다. 코드가 도구를 실행한 결과를 다음 요청에 넣는 것을 관찰이라고 했고, 그 절에서는 이 반복을 실행하지 않았습니다. <a href=\"""" + L_CH17_03 + """\">Ch 17 03절</a>에서는 이런 반복을 루프, 한 번 도는 것을 바퀴라고 불렀습니다. 모델이 도구 호출 요청 없이 답하면 멈추는 것은 정지 조건 가운데 「모델의 끝 선택」이었습니다.</p><p><a href=\"""" + L_CH13_01 + """\">Ch 13 01절</a>에서는 상태 그래프를 컴파일하고 구조 문자열을 받아 보았습니다. <a href=\"""" + L_CH13_03 + """\">03절</a>에서는 조건 함수와 이름표 표로 조건부 엣지를 적었고, <a href=\"""" + L_CH13_05 + """\">05절</a>에서는 조건 함수가 목록으로 내놓는 <code>Send</code>를 보았습니다. <a href=\"""" + L_CH16_03 + """\">Ch 16 03절</a>에서는 모델이 따를 규칙을 담은 시스템 메시지를 대화 기록 맨 앞에 두었습니다.</p><p><a href=\"""" + L_CH19_01 + """\">Ch 19 01절</a>에서는 <code>@tool</code>로 도구를 만들었습니다. <a href=\"""" + L_CH19_04 + """\">04절</a>에서는 도구 호출 요청을, <a href=\"""" + L_CH19_05 + """\">05절</a>에서는 도구 메시지와 호출 ID를 보았습니다. Ch 19에서는 인자 <code>parallel_tool_calls</code>로 한 응답에 요청을 여럿 담을지(여럿 담기)도 정했습니다. <a href=\"""" + L_CH20_01 + """\">Ch 20 01절</a>에서는 이 모든 것을 상태 그래프에 손으로 이었고, <a href=\"""" + L_CH20_03 + """\">03절</a>에서는 설계 객체의 속성 <code>branches</code>를 보았습니다. 이 절은 Ch 20 도구 파일의 함수를 새 도구 파일 <code>runner_tools.py</code>로 옮겨 씁니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>빨래를 손으로 하는 모습을 떠올려 봅니다. 대야에 물을 받고, 빨래판에 문지르고, 헹굼 통에서 헹굽니다. 덜 깨끗하면 이 차례를 다시 되풀이합니다. 도구는 따로따로 놓여 있고, 한 도구에서 다음 도구로 잇는 일은 사람이 합니다.</p><p>세탁기는 같은 일을 기계 한 대로 합니다. 코스 버튼 하나를 누르면 물 받기·돌리기·헹구기를 기계가 알아서 되풀이합니다. 앞의 동그란 창으로는 안에서 빨래가 도는 모습이 보입니다.</p><p>손빨래 도구는 Ch 20 01절에서 손으로 이은 노드와 엣지입니다. 세탁기는 함수 <code>create_agent</code>가 만든 에이전트 그래프이고, 코스 버튼을 누르는 일은 <code>invoke</code>로 질문을 보내는 일입니다. 동그란 창은 구조 문자열과 메시지 칸입니다. 창으로 안을 보듯, 이 둘로 그래프 안에서 무엇이 몇 번 돌았는지 읽습니다.</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>에이전트를 만드는 함수(create_agent)</td><td>모델·도구 목록·시스템 메시지 글을 받아, 모델과 도구를 오가는 그래프를 만들어 컴파일까지 해 주는 LangChain 함수입니다. 비유의 세탁기를 만드는 공장과 같습니다.</td></tr><tr><td>에이전트 그래프</td><td>함수 <code>create_agent</code>가 내놓는 컴파일한 그래프입니다. 모델 노드와 도구 실행 노드가 들어 있습니다. 비유의 세탁기 한 대와 같습니다.</td></tr><tr><td>ReAct 루프</td><td>모델이 다음 행동을 고르고, 코드가 도구를 실행하고, 그 결과를 다시 모델에게 보여 주는 반복입니다. Ch 7 05절에서 이름만 본 방식을 실제로 도는 모습입니다. 비유에서 기계가 알아서 되풀이하는 코스와 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 에이전트를 만드는 함수는 노트북 4절의 <code>create_agent(model, tools=[lookup_policy], system_prompt=system_text)</code> 한 줄입니다. 그 결과인 <code>agent</code>가 에이전트 그래프이고, 종류는 <code>CompiledStateGraph</code>입니다. ReAct 루프는 노트북 6절 대출 질문에서 모델 노드 → 도구 실행 노드 → 모델 노드로 이어진 흐름입니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
<h3>Ch 20 그래프와 견주기</h3><p>한 줄로 만든 그래프가 Ch 20 01절 그래프의 부품을 어떻게 맡는지 표로 적었습니다. 왼쪽이 Ch 20 01절 코드이고, 오른쪽이 이 절 노트북 5절 출력과 설치판 소스로 본 것입니다.</p>
""" + compare_table_html() + """
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
<h3>다른 상황에 적용</h3><p>Ch 19의 주문 도구를 넣는다면 인자 <code>tools</code>의 목록만 바꾸면 됩니다. 도구를 모델에게 알리고 노드를 새로 만드는 일은 <code>create_agent</code>가 맡습니다. 시스템 메시지 글도 주문 안내에 맞게 바꿉니다. 이 조합은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>한 줄로 만든 그래프는 짧지만, Ch 20 그래프와 모든 것이 같지는 않습니다. 실행 흔적 칸이 없고, 되돌아가는 엣지도 조건부 엣지입니다. 여럿 담기를 끄는 인자도 없어, 한 응답에 요청이 여럿 올 수 있습니다. 모델 요청 앞뒤에 처리를 더하는 방법은 <a href=\"""" + L_CH22_01 + """\">Ch 22</a>에서 봅니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 Ch 20 01절과 같은 규정 딕셔너리와 도구를 만듭니다. 함수 <code>create_agent</code>로 에이전트 그래프를 만들고, 구조 문자열과 설계 객체로 모양을 봅니다. 대출 질문과 인사 질문을 보내고, 값 바꿔 보기로 운영과 연체를 함께 묻는 질문을 보냅니다. 마지막으로 사용량과 예상 비용을 세고, 세 질문을 Ch 20 결과와 견줍니다.</p><p>모델은 <code>gpt-5.4-mini</code>이고, temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다. 교재 출력에서 모델 요청은 모두 5번입니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — 노트북 5절 출력에서 노드 이름, 고정 엣지 수 <code>1</code>, 조건 함수 이름 둘을 봅니다. 노트북 6절 메시지 네 줄로 모델 → 도구 → 모델 흐름을 보고, <code>시스템 메시지 수: 0</code>을 확인합니다. 노트북 10절 표에서 세 질문의 모델 요청 수와 도구 메시지 수를 Ch 20과 견줍니다. 답 글과 출력 토큰은 실행마다 달라질 수 있어 결론에 쓰지 않았습니다.</p>
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>실험에서 바꾼 것은 질문 하나이고, 에이전트 그래프·도구·모델 설정은 그대로였습니다. 아래 표의 오른쪽 두 칸은 Ch 20 01절 교재 출력입니다.</p>
<table><thead><tr><th>질문</th><th>응답 수(모델 요청)</th><th>도구 메시지 수</th><th>첫 응답의 요청 수</th><th>호출 ID 짝</th><th>Ch 20 모델 요청</th><th>Ch 20 도구 메시지</th></tr></thead><tbody><tr><td>대출</td><td>2</td><td>1</td><td>1</td><td>True</td><td>2</td><td>1</td></tr><tr><td>인사</td><td>1</td><td>0</td><td>0</td><td>True</td><td>1</td><td>0</td></tr><tr><td>운영·연체(바꾼 값)</td><td>2</td><td>2</td><td>2</td><td>True</td><td>3</td><td>2</td></tr></tbody></table>
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG4_READ) + """</p>
<p>대출·인사 질문의 수는 Ch 20과 같았습니다. 운영·연체 질문만 모델 요청이 하나 적었고, 첫 응답에 요청 둘이 함께 들어 있었습니다. Ch 20은 여럿 담기를 꺼서 한 응답에 요청이 하나까지만 올 수 있었습니다. 에이전트 그래프는 그 값을 넣지 않아, 모델이 한 응답에 두 요청을 담았습니다.</p><p>두 그래프는 시스템 메시지도 달라, 이 표는 한 가지만 바꾼 비교가 아닙니다. 그래서 모델 요청 수는 도구 메시지 수로 짐작하지 않고, 응답 수로 셉니다. 「모델 요청 수 = 도구 메시지 수 + 1」은 요청을 하나씩 받을 때만 맞습니다.</p><p>새 커널로 두 번 실행했을 때 표의 값은 두 번 모두 같았습니다. 노트북 밖에서 세 질문을 다섯 번씩 보냈을 때도 같았습니다. 답 글과 출력 토큰은 이 표에 넣지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>노트북을 실행하기 전에 노트북 밖에서 세 질문을 다섯 번씩 보냈습니다. 메시지 종류와 차례, 도구 이름과 인자, 한 응답의 요청 수가 다섯 번 모두 같았습니다. 같은 요청도 실행한 때에 따라 모델이 도구를 부를지와 한 응답의 요청 수가 달라질 수 있습니다.</li><li>질문 셋과 시스템 메시지 글은 흐름을 보여 주려고 정한 예입니다. 질문은 Ch 20 01절과 같은 글이고, 시스템 메시지 글은 노트북 밖 확인 전에 정했습니다.</li><li>도구를 부를지와 인자, 한 응답의 요청 수에는 <code>assert</code>를 걸지 않았습니다. 모델이 정하는 값이기 때문입니다. 셀의 <code>assert</code>는 도구 실행 노드가 옮겨 적는 호출 ID 짝에만 걸었습니다.</li><li>노드 이름·조건 함수 이름·갈 곳·상태 칸은 출력으로 보았습니다. 조건 함수가 하는 일과, 시스템 메시지를 요청 앞에 붙이는 동작은 설치한 langchain 1.4.0 소스로만 확인했습니다.</li><li>한 응답에 온 요청 둘을 도구 실행 노드가 한 단계 안에서 함께 실행하는지는 세지 않았습니다. 그래서 단계 수가 Ch 20과 어떻게 다른지도 이번에 보지 않았습니다. 실행 한도(<a href=\"""" + L_CH20_03 + """\">Ch 20 03절</a>)는 주지 않고 설치판 기본값으로 실행했습니다.</li><li>딕셔너리에 없는 주제어면 도구가 <code>ValueError</code>를 냅니다. 설치판 소스(<code>factory.py</code> 1089행)로 보면, 에이전트 그래프의 도구 실행 노드는 오류 처리 인자를 기본값으로 둡니다. <a href=\"""" + L_CH20_02 + """\">Ch 20 02절</a> 기본값 노드처럼 오류가 올라와 멈출 것으로 보이지만, 이번에 실행하지 않았습니다.</li><li>그래프를 그림 파일로 그리는 메서드 <code>draw_mermaid_png</code>도 있습니다. langchain-core 1.6.2 소스로 보면, 이 메서드는 기본값이 바깥 서비스에 그림을 요청합니다. 이 절은 글자로 된 구조 문자열만 썼습니다.</li><li>걸린 시간은 재지 않았습니다. 모델 요청 수는 응답 수로 셌습니다.</li><li>이 절이 가져오는 함수 넷과 그 안에서 쓰는 <code>tool_call_names</code>는 Ch 20 <code>graph_tools.py</code>의 본문을 글자 그대로 옮긴 것입니다. 같은 도구 파일 <code>runner_tools.py</code>에는 뒤 절이 쓰는 함수도 들어 있습니다. 함수 <code>estimate_cost</code>는 <a href=\"""" + L_CH06_06 + """\">Ch 6 06절</a>에서 배웠습니다.</li><li>예상 비용은 2026-09-17 요금표로 어림하면 노트북 한 번에 0.01달러 아래이고, 청구 금액이 아닙니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>함수 <code>create_agent</code> 한 줄로 만든 에이전트 그래프에도 노드 <code>model</code>·<code>tools</code>와 상자 넷이 있었습니다.</li><li>갈래는 조건 함수 <code>model_to_tools</code>·<code>tools_to_model</code>이 맡아, 되돌아가는 엣지도 점선이었습니다.</li><li>대출·인사·운영과 연체 질문의 모델 요청은 2·1·2번, 도구 메시지는 1·0·2개였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_02 + """\">02절</a>에서는 <code>create_agent</code>가 답을 정해 둔 양식으로 내놓게 하는 구조화 출력 두 가지를 봅니다. 이 절에서 본 상태 칸 <code>structured_response</code>가 그 결과를 담는 자리입니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 에이전트 그래프에서 모델 노드 뒤의 갈래를 고르는 조건 함수의 이름은 무엇이고, Ch 20 01절과 무엇이 다른가요?</p><p class="quiz-a">이름은 <code>model_to_tools</code>입니다. Ch 20 01절에서는 도구 조건 함수 <code>tools_condition</code>을 우리가 조건부 엣지에 넣었습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">2. 구조 문자열에서 되돌아가는 엣지가 점선으로 나온 까닭은 무엇인가요?</p><p class="quiz-a">도구 실행 노드 뒤에도 조건 함수 <code>tools_to_model</code>이 붙은 조건부 엣지이기 때문입니다. 이 에이전트 그래프에서 갈 곳은 <code>model</code> 하나라, 늘 모델 노드로 돌아갑니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">3. 대출 질문 결과의 메시지 칸에 시스템 메시지가 있었나요?</p><p class="quiz-a">없었습니다. 출력 줄 <code>시스템 메시지 수: 0</code>입니다. 설치판 소스로 보면 모델 노드가 요청마다 앞에 붙여 보내고, 메시지 칸에는 남기지 않습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">4. 운영·연체 질문에서 모델 요청이 Ch 20보다 하나 적었던 까닭은 무엇인가요?</p><p class="quiz-a">첫 응답에 도구 호출 요청 둘이 함께 들어 있었기 때문입니다. 함수 <code>create_agent</code>에는 여럿 담기를 끄는 인자가 없어, Ch 20처럼 요청을 하나씩 받지 않았습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/agents">LangChain Agents</a></div>확인 2026-09-25 · 에이전트를 「도구를 반복해 부르는 모델」로 설명합니다. 모델 이름 글자나 모델 객체를 넘길 수 있다고 적습니다.</li><li>langchain 1.4.0 소스 <code>langchain/agents/factory.py</code> 995~996행 — 글자로 넘긴 모델을 기본 설정으로 만듭니다.</li><li>같은 소스 1089행 — 도구 실행 노드를 만듭니다. 1431~1436행은 <code>bind_tools</code>, 1451~1452행은 시스템 메시지를 붙이는 자리입니다.</li><li>같은 소스 1672~1735행 — 조건부 엣지 둘을 적습니다. 1923~1975행은 <code>model_to_tools</code>, 2004~2037행은 <code>tools_to_model</code>입니다.</li><li>langchain 1.4.0 소스 <code>langchain/agents/middleware/types.py</code> 349~355행 — 상태 칸 셋입니다.</li><li>langchain-openai 1.6.0 소스 <code>chat_models/base.py</code> 2427~2428행 — 여럿 담기 값은 줄 때만 요청에 넣습니다.</li><li>langchain-core 1.6.2 소스 <code>runnables/graph.py</code> 639행·<code>graph_mermaid.py</code> 422~423행 — 그림 파일은 기본값이 바깥 서비스입니다.</li><li>Ch 7 05절에서 ReAct와 관찰을, Ch 16 03절에서 시스템 메시지를 보았습니다.</li><li>Ch 19 04·05절에서 도구 호출 요청과 도구 메시지를 보았습니다.</li><li>Ch 20 01·03절에서 도구 실행 노드, 도구 조건 함수, 설계 객체를 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_same_as_ch20()
    if os.environ.get("AUTHOR01_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "01", SLUG, "experiment", cells())
        print("wrote", path)
