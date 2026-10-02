"""Ch 27 06절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_06.py            → 노트북 + _src 본문을 다시 쓴다(도구 파일은 쓰지 않음 — 02절 판 그대로, 노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_06.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  python3 -B author_06.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 실행용 — Ch 26 A-19 교훈)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**.
슬러그 `06-서브에이전트-위임` 그대로(Part 6 목차와 05절 b8이 링크), 제목 「서브에이전트 위임」 그대로.

## 결정 1 — M2: 앞 절반 모델 없음 + 뒤 절반 실제 모델 (챕터 리드 결정 1)

nbkit.key_and_model_cells("openai:gpt-5.4-mini") — temperature=0·reasoning_effort="none", 키는 루트 .env에서만(값 출력 없음).
2절: 규정 도구 lookup_rule(02절 셀과 같은 글)을 서브에이전트 명세 rule-checker에만 넣고, 바깥 에이전트에는 tools=를 주지 않는다
(도구 아홉·lookup_rule 없음 — 위임이 조립으로 정해짐). 명세 하나만 넘기면 task 설명 글에 기본 general-purpose 줄과
기본 설명이 남는다(01절 안전 규칙 ⑤를 출력으로). 3절: 04절 tools_only_graph에 한도 0 복사본 명세로 task를 손 요청해,
서브에이전트가 시작할 때 받은 것(메시지 1·넘긴 글·바깥 files의 파일 위치 — @before_agent 시작 기록 훅)과
바깥으로 온 도구 메시지(Model call limits exceeded: run limit (0/0))를 모델 없이 본다(요청 0, 01절 6절 선례).
5·6절에서 실제 모델로 한 번 맡기고(바깥 2 + rule-checker 3 — 흔들림 확인 5/5), 기록 훅으로 바깥·안쪽 요청을 가르고,
Ch 26 01절 셈(바깥 + 부른 횟수 × 1)이 맞지 않음을 출력으로 본다. 가짜 채팅 모델 없음(규격 §3).

## 결정 2 — 파일 쓰기 자리 (챕터 리드 결정 3)

디스크에 쓰지 않는다. 메모 파일(3절 손 요청)·보고 파일(5절 서브에이전트)은 기본 백엔드(StateBackend)의 상태 칸 files에만 생긴다.

## 결정 3 — 안전 규칙 (가)·(나)·(다)와 요청 수 셈 (챕터 공통)

(가) 바깥 ModelCallLimitMiddleware(run_limit=10) — 03절 셀과 같은 글 · (나) 같은 이름 general-purpose 명세(02절 명세 글 + 기록 훅 한 줄,
한도 2) · (다) rule-checker 자기 한도 4. 상한 10 + rule-checker 부른 횟수 × 4 + general-purpose 부른 횟수 × 2.
한 응답 안 task 요청 수는 막지 못한다(남는 틈 — 한 문장). 기록 훅 record_tool_names(02절 셀과 같은 글)를 바깥과 두 명세에 모두 넣고,
task를 받은 요청 = 바깥, lookup_rule을 받은 요청 = rule-checker로 가른다(서브에이전트 스택에는 task가 없음 — 설치판 graph.py 666~674행).

## 결정 4 — 흔들림 먼저 확인 (qa/upgrade/06-probe.md)

노트북 밖 5번(요청 25번, §0은 첫 요청 전 14:46:44Z → 첫 호출 14:46:55Z): 구조 값과 모델 판단 값
(task 한 번 rule-checker → lookup_rule → write_file → 보고, general-purpose 0, 바깥 2 + 안 3 = 5, Ch 26 셈 3) 5/5 → 입력 그대로.
흔들리는 값(task 넘긴 글·보고 글·답 글·토큰·비용)은 [[READ_…]] 자리 표시 → 교재 출력(A)·B 대조 뒤 FILLS + mdpatch.py. assert는 키 셀뿐.

## 결정 5 — 도구 파일 (챕터 리드 결정 6)과 tools_only_graph

02절 판 harness_tools.py에서 함수 넷(estimate_cost·show_messages·sum_usage·tool_names)을 가져온다(추가 0 — 도구 파일을 쓰지 않음).
author_05.check_tools()(= 04 → 03 → 02 사슬). Ch 26 함수(usage_with_specialists 등)는 쓰지 않는다(Deep Agents는 안쪽 목록을 내놓지 않음).
tools_only_graph는 04절 셀 글 그대로 노트북에 다시 적는다(05와 같은 판단 — check_same_as_prev가 04 노트북 디스크 셀과 글자 대조).
02·03절 셀과 같은 글(RULES·DEF_TOOL·DEF_HOOK / OUTER_LIMIT)도 author_02·author_03 문자열 그대로 + 노트북 디스크 셀 대조.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·변수 힌트·대입 풀기·별표 풀기·
`while`·`try`·세미콜론·`isinstance`·클래스·`re`. 힌트는 @tool 매개변수 `: str`(02절 셀)만, 데코레이터는 @tool·@wrap_model_call(02절 셀)·
@before_agent(Ch 22 01절 훅)만. 호출 깊이 2 이하.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(HERE))
import author_02  # noqa: E402  02절 셀 글·본문 도우미
import author_03  # noqa: E402  03절 셀 글
import author_04  # noqa: E402  04절 셀 글
import author_05  # noqa: E402  도구 파일 대조 사슬(05 → 04 → 03 → 02)
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch27-deepagents/notebooks"
FIGS = ROOT / "textbook/part6/ch27-deepagents/figures"
SLUG = "06-서브에이전트-위임"
TITLE_TEXT = "서브에이전트 위임"
SRC = ROOT / "textbook/part6/ch27-deepagents/_src" / (SLUG + ".html")
NB02 = LAB / "02-create-deep-agent와-도구.ipynb"
NB03 = LAB / "03-플래닝과-시스템-프롬프트.ipynb"
NB04 = LAB / "04-파일시스템과-중간-결과.ipynb"
TOOLS_PATH = LAB / "harness_tools.py"
html_text = author_02.html_text
table_html = author_02.table_html
mermaid_block = author_02.mermaid_block
# 교재 출력(A)·새 커널 두 번째(B) 대조 뒤 채운 흔들리는 값의 글(mdpatch.py로 노트북·_src에도 같은 글)
FILLS = {
    "RUN": "이번 실행에서는 `결과 메시지 수: 4`였습니다.\n질문 하나, `task` 요청 응답, 도구 메시지, 마지막 답입니다.\n노트북 밖 다섯 번과 새 커널 두 번에서도 모두 넷이었습니다.",
    "SHOW": "이번 실행에서 바깥 모델은 첫 응답에서 `task`를 한 번 요청했고, 도구 메시지를 받은 뒤 답했습니다.\n노트북 밖 다섯 번과 새 커널 두 번에서 모두 이 차례였습니다.\n보고 글은 서브에이전트가 쓴 글이라 실행마다 달라지고, 새 커널 두 번에서도 글이 달랐습니다.\n바깥 모델이 `task`에 넘긴 글도 노트북 밖 다섯 번에서 모두 달랐습니다.",
    "ASKED": "이번 실행에서는 `task로 맡긴 서브에이전트: ['rule-checker']`였습니다.\n노트북 밖 다섯 번과 새 커널 두 번에서 모두 rule-checker에게 한 번 맡겼습니다.\ngeneral-purpose에게 맡긴 적은 없었습니다.\n어디에 몇 번 맡길지는 모델이 정하는 값이라, 실행마다 달라질 수 있습니다.",
    "OUTER_TOOLS": "이번 실행에서는 `바깥 목록의 도구 메시지 이름: ['task']`였고, `write_file` 도구 메시지도 없었습니다.\n바깥 모델이 부른 도구는 `task` 하나였다는 뜻입니다.\n노트북 밖 다섯 번과 새 커널 두 번에서도 같았습니다.",
    "FILES": "이번 실행에서는 `상태 칸 files의 파일 위치: ['/notes/rule-check.md']`였습니다.\n바깥 목록에는 `write_file` 도구 메시지가 없었으니, 이 파일은 서브에이전트가 적은 것입니다.\n서브에이전트가 쓴 파일이 바깥 결과의 상태 칸에 더해졌습니다.\n노트북 밖 다섯 번과 새 커널 두 번에서도 이 파일이 있었고, 글은 연장 규정 글과 같았습니다.\n파일에 무엇을 적을지는 모델이 정하므로, 글은 실행마다 달라질 수 있습니다.",
    "SPLIT": "이번 실행에서는 `기록 훅이 센 요청 수: 5`였습니다.\n그 가운데 `task를 받은 요청(바깥): 2`, `lookup_rule을 받은 요청(rule-checker): 3`이었습니다.\n기본 자리를 바꾼 general-purpose의 요청은 없어, 두 수를 더하면 합과 같습니다.\n노트북 밖 다섯 번과 새 커널 두 번에서도 같은 수였습니다.",
    "USAGE": "이번 실행에서는 바깥 요청 2번, `입력 토큰: 3957 | 출력 토큰: 172`였습니다.\n새 커널 두 번째는 입력 3965·출력 180으로, 토큰은 실행마다 조금씩 달랐습니다.\n바깥 요청 수는 도구를 요청한 바깥 응답 하나에 1을 더한 값입니다.",
    "CH26": "이번 실행에서는 `Ch 26 셈으로 센 요청 수: 3`, `기록 훅이 센 요청 수: 5`였습니다.\n서브에이전트를 한 번 불렀지만, 그 안에서 요청이 세 번 나갔기 때문입니다.\n노트북 밖 기록에서 rule-checker는 규정 도구, `write_file`, 보고의 차례로 응답했습니다.\n그래서 셈은 바깥 2에 1 × 3을 더한 5이고, 흔들림 확인 다섯 번과 두 커널에서 같았습니다.",
    "COST": "이번 실행에서는 `바깥 요청의 예상 비용(달러): 0.003742`였습니다.\n노트북 밖 다섯 번에서 서브에이전트 요청까지 센 값은 0.0083에서 0.0086달러 사이였습니다.\n바깥 요청만의 값은 그 절반쯤이었습니다.\n두 값 모두 입력 토큰을 모두 입력 요금으로 센 어림입니다.",
    "ROW_JUDGE": "<code>task로 맡긴 서브에이전트: ['rule-checker']</code> · <code>기록 훅이 센 요청 수: 5</code>(바깥 2 · rule-checker 3) · <code>Ch 26 셈으로 센 요청 수: 3</code> · 보고 파일 <code>/notes/rule-check.md</code>",
    "ROW_SHAKY": "교재 출력 <code>입력 토큰: 3957 | 출력 토큰: 172</code> · <code>바깥 요청의 예상 비용(달러): 0.003742</code> · 보고 글(새 커널 두 번째는 입력 토큰 3965·출력 토큰 180, 보고 글도 다름)",
    "B6_JUDGE": "흔들림 확인 다섯 번과 두 커널에서 모두, 바깥 에이전트는 첫 응답에서 rule-checker에게 한 번 맡겼습니다. 노트북 밖 기록에서 rule-checker는 규정 도구, <code>write_file</code>, 보고의 차례로 요청 세 번을 보냈습니다. 그래서 요청은 바깥 2번과 rule-checker 3번을 더한 5번이었고, Ch 26 셈 3과 달랐습니다. 서브에이전트가 적은 보고 파일도 바깥 결과의 상태 칸 <code>files</code>에 있었습니다. 맡기는 모양과 안쪽 요청 수는 모델이 정하는 값이라, 이 절은 셈의 모양을 결론의 중심에 둡니다.",
    "LOOK_B6": "노트북 6절에서 <code>task를 받은 요청(바깥):</code>과 <code>lookup_rule을 받은 요청(rule-checker):</code> 뒤의 수를 더해 봅니다. 그 합을 <code>기록 훅이 센 요청 수:</code>와 견줍니다. 5절에서 <code>write_file 도구 메시지가 있는가: False</code>인데 보고 파일이 상태 칸에 있는지 확인합니다. 교재 출력에서는 <code>Ch 26 셈으로 센 요청 수: 3</code>이었습니다.",
    "B7_MANY": "도구 <code>task</code>의 설명 글은 서로 무관한 일이면 여럿을 한 응답에 함께 부르라고 권합니다. 그러면 상한은 부른 수만큼 커지고, 한 응답의 <code>task</code> 요청 수를 막는 장치는 없습니다. 이번 실행에서는 한 응답에 하나였습니다.",
    "B7_COST": "노트북 밖 흔들림 확인에서는 기록만 하는 콜백으로 서브에이전트 응답의 토큰까지 셌습니다. 그 전체 예상 비용은 0.0083에서 0.0086달러 사이로, 바깥 요청만의 값보다 두 배쯤 컸습니다. 서브에이전트를 쓰는 에이전트의 비용은 바깥 목록만으로 다 셀 수 없습니다.",
    "B7_PROBE": "노트북을 쓰기 전에 5절 실행을 노트북 밖에서 다섯 번 보냈습니다. 맡긴 곳·안쪽 도구 차례·요청 수·보고 파일은 다섯 번 모두 같았고, 넘긴 글·보고 글·토큰은 달랐습니다. 같은 요청도 실행한 때에 따라 맡기는 모양이 달라질 수 있습니다. 그래서 이 절은 맡긴 횟수를 결론의 중심에 두지 않습니다.",
    "RUNS_SENTENCE": "새 커널로 두 번 실행해 견주자, 코드 셀 서른 가운데 스물일곱의 출력이 같았습니다. 달랐던 세 셀은 보고 글이 찍힌 5절 셀과, 토큰·예상 비용이 찍힌 6절 두 셀입니다. 이 값은 결론에 쓰지 않습니다.",
}


def placeholder(name: str) -> str:
    """교재 출력(A)·B 대조 뒤 채운 글을 내놓습니다(채우기 전에는 [[READ_…]] 자리 표시 — author_02.placeholder)."""
    if name in FILLS:
        return FILLS[name]
    return author_02.placeholder(name)


def check_tools() -> None:
    """06절은 도구 파일에 함수를 더하지 않습니다. 05절 대조 사슬(= 04 → 03 → 02 사슬 + 디스크 판이 02절 판으로 시작)을 그대로 돌립니다."""
    author_05.check_tools()


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["deepagents==0.7.0", "langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3"])

IMPORTS = r'''# Deep Agents(01절)·상태 형식(04절)·미들웨어와 훅(Ch 22)·모델·메시지·도구·그래프 이름을 가져옵니다
from deepagents import create_deep_agent
from deepagents.middleware.filesystem import FilesystemState
from langchain.agents.middleware import ModelCallLimitMiddleware, before_agent, wrap_model_call
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
# 앞 챕터와 01절에서 배운 함수 넷은 도구 파일에서 가져옵니다
from harness_tools import estimate_cost, show_messages, sum_usage, tool_names

print("도구 파일에서 가져온 함수:", "estimate_cost, show_messages, sum_usage, tool_names")'''

RULES = author_02.RULES
DEF_TOOL = author_02.DEF_TOOL
DEF_HOOK = author_02.DEF_HOOK

CHECKER_SPEC = r'''# 규정 확인을 맡을 서브에이전트 명세를 키마다 한 줄로 적습니다(자기 호출 한도 4와 기록 훅을 넣음)
checker_limit = ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")
rule_checker = {
    "name": "rule-checker",
    "description": "교육센터 자료실 규정을 찾아 확인하는 담당입니다. 규정 도구 lookup_rule은 이 담당만 가졌습니다.",
    "system_prompt": "맡은 일에 맞는 규정을 lookup_rule로 찾으세요. 찾은 규정 글을 write_file로 /notes/rule-check.md에 적으세요. 그다음 찾은 내용을 두 문장의 한국어로 보고하세요.",
    "tools": [lookup_rule],
    "middleware": [checker_limit, record_tool_names],
}
print("명세의 키:", list(rule_checker))
print("자기 호출 한도:", checker_limit.run_limit)'''

PLAIN_PARENT = r'''# 조회 도구 없이, 규정 확인 명세 하나만 넘겨 바깥 에이전트를 만듭니다(요청은 보내지 않음)
plain_parent = create_deep_agent(model=model, subagents=[rule_checker])
plain_tools = tool_names(plain_parent)
print("바깥 에이전트의 도구 수:", len(plain_tools))
print("바깥 에이전트에 lookup_rule이 있는가:", "lookup_rule" in plain_tools)'''

DEF_SHOW_TASK = r'''# task 설명 글에 서브에이전트 이름마다 「- 이름:」 줄이 있는지와, 기본 general-purpose 설명이 남았는지 출력합니다
def show_task_names(agent, names):
    task_text = agent.nodes["tools"].bound.tools_by_name["task"].description
    for name in names:
        print(name, "줄이 있는가:", "- " + name + ":" in task_text)
    print("기본 general-purpose 설명이 남았는가:", "General-purpose agent" in task_text)'''

SHOW_PLAIN = r'''# 명세 하나만 넘긴 바깥 에이전트의 task 설명 글을 봅니다
subagent_names = ["general-purpose", "rule-checker"]
show_task_names(plain_parent, subagent_names)'''

HELPER_SPEC = r'''# 02절 general-purpose 명세에 기록 훅 하나만 더해, 기본 자리를 바꿀 명세를 만듭니다(자기 호출 한도 2)
helper_limit = ModelCallLimitMiddleware(run_limit=2, exit_behavior="end")
helper_spec = {
    "name": "general-purpose",
    "description": "교재용 도우미입니다. 맡긴 일을 짧게 처리합니다.",
    "system_prompt": "맡긴 일을 두 문장의 한국어로 처리하세요.",
    "middleware": [helper_limit, record_tool_names],
}
print("명세의 키:", list(helper_spec))
print("자기 호출 한도:", helper_limit.run_limit)'''

DEF_GRAPH = author_04.DEF_GRAPH

DEF_RECORD_INPUTS = r'''# 서브에이전트 실행이 시작될 때 한 번, 받은 메시지와 파일 위치를 기록 목록에 붙이는 훅입니다(Ch 22 01절 before_agent)
@before_agent
def record_inputs(state, runtime):
    first_message = state["messages"][0]
    record = {
        "메시지 수": len(state["messages"]),
        "첫 메시지 종류": type(first_message).__name__,
        "첫 메시지 글": first_message.text,
        "파일 위치": list(state["files"]),
    }
    seen_inputs.append(record)'''

ZERO_SPEC = r'''# 규정 확인 명세를 복사해, 미들웨어만 시작 기록 훅과 호출 한도 0으로 바꿉니다(모델을 부르기 전에 멈추게)
zero_limit = ModelCallLimitMiddleware(run_limit=0, exit_behavior="end")
zero_checker = rule_checker.copy()
zero_checker["middleware"] = [record_inputs, zero_limit]
print("같은 이름인가:", zero_checker["name"] == rule_checker["name"])
print("원래 명세의 미들웨어 수:", len(rule_checker["middleware"]))'''

ZERO_GRAPH = r'''# 복사본과 general-purpose 명세로 바깥 에이전트를 만들고, 도구 실행 노드만 든 작은 그래프를 만듭니다(요청은 보내지 않음)
zero_parent = create_deep_agent(model=model, subagents=[zero_checker, helper_spec])
zero_graph = tools_only_graph(zero_parent)
zero_nodes = zero_graph.get_graph().nodes
print("작은 그래프의 노드:", list(zero_nodes))'''

HAND_WRITE = r'''# 모델 없이, 메모 파일 하나를 쓰는 write_file 요청을 손으로 만들어 작은 그래프에 넣습니다(04절 3절 모양)
memo_args = {"file_path": "/notes/question.md", "content": "문의: 빌린 책의 반납 날짜를 늘리는 방법"}
memo_call = {"name": "write_file", "args": memo_args, "id": "hand_write_1", "type": "tool_call"}
memo_request = AIMessage(content="", tool_calls=[memo_call])
memo_result = zero_graph.invoke({"messages": [memo_request]})
print("도구 메시지:", memo_result["messages"][-1].content)
print("상태 칸 files의 파일 위치:", list(memo_result["files"]))'''

HAND_TASK = r'''# 모델 없이, rule-checker에게 맡기는 task 요청을 손으로 만들어, 메모 파일이 든 상태와 함께 넣습니다
task_args = {"description": "대출 연장 규정을 확인해 주세요.", "subagent_type": "rule-checker"}
task_call = {"name": "task", "args": task_args, "id": "hand_task_1", "type": "tool_call"}
task_request = AIMessage(content="", tool_calls=[task_call])
seen_inputs = []
zero_input = {"messages": [task_request], "files": memo_result["files"]}
zero_result = zero_graph.invoke(zero_input)
print("서브에이전트가 시작할 때 받은 것:", seen_inputs)'''

SHOW_ZERO = r'''# 바깥으로 온 도구 메시지와, 실행 뒤 상태 칸 files를 봅니다
zero_message = zero_result["messages"][-1]
print("도구 메시지 종류:", type(zero_message).__name__, "| 도구 이름:", zero_message.name)
print("도구 메시지 내용:", zero_message.content)
print("결과 메시지 수:", len(zero_result["messages"]))
print("상태 칸 files의 파일 위치:", list(zero_result["files"]))'''

OUTER_LIMIT = author_03.OUTER_LIMIT

RUN_PARENT = r'''# 조회 도구 없이, 호출 한도·기록 훅·두 명세·우리 시스템 메시지 글을 넘겨 바깥 에이전트를 만듭니다(요청은 아직 보내지 않음)
parent_text = "자료실 규정은 직접 찾지 말고, task 도구로 rule-checker에게 맡기세요. 받은 보고를 바탕으로 두 문장의 한국어로 답하세요."
run_parent = create_deep_agent(
    model=model,
    system_prompt=parent_text,
    middleware=[outer_limit, record_tool_names],
    subagents=[rule_checker, helper_spec],
)
print("바깥 에이전트에 lookup_rule이 있는가:", "lookup_rule" in tool_names(run_parent))
show_task_names(run_parent, subagent_names)'''

RUN = r'''# 기록 목록을 새로 만들고, 02절과 같은 질문 한 줄로 한 번 실행합니다
seen_tool_lists = []
question = "교육센터 자료실에서 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요? 두 문장으로 답해 주세요."
first_input = {"messages": [HumanMessage(content=question)]}
input_count = len(first_input["messages"])
run_result = run_parent.invoke(first_input)
run_messages = run_result["messages"]
print("결과 메시지 수:", len(run_messages))'''

SHOW = r'''# 바깥 목록(결과 메시지)을 차례로 봅니다(Ch 19 06절 함수 show_messages)
print("바깥 목록:")
show_messages(run_messages)'''

ASKED = r'''# 이번 실행이 더한 응답에서 task 요청을 골라, 맡긴 서브에이전트 이름을 모읍니다
run_new = run_messages[input_count:]
asked_types = []
for message in run_new:
    if type(message).__name__ == "AIMessage":
        for call in message.tool_calls:
            if call["name"] == "task":
                asked_types.append(call["args"]["subagent_type"])
print("task로 맡긴 서브에이전트:", asked_types)'''

OUTER_TOOLS = r'''# 바깥 목록의 도구 메시지 이름을 모아, 서브에이전트가 부른 도구의 메시지가 있는지 봅니다
outer_tool_names = []
for message in run_new:
    if type(message).__name__ == "ToolMessage":
        outer_tool_names.append(message.name)
print("바깥 목록의 도구 메시지 이름:", outer_tool_names)
print("lookup_rule 도구 메시지가 있는가:", "lookup_rule" in outer_tool_names)
print("write_file 도구 메시지가 있는가:", "write_file" in outer_tool_names)'''

FILES = r'''# 실행 뒤 상태 칸 files를 보고, 보고 파일이 있으면 그 글을 봅니다
note_path = "/notes/rule-check.md"
print("상태 칸 files의 파일 위치:", list(run_result["files"]))
if note_path in run_result["files"]:
    print("보고 파일의 글:")
    print(run_result["files"][note_path]["content"])'''

SPLIT = r'''# 기록 훅이 적은 요청을, task를 받은 요청(바깥)과 lookup_rule을 받은 요청(rule-checker)으로 나눠 셉니다
outer_count = 0
checker_count = 0
for names in seen_tool_lists:
    if "task" in names:
        outer_count = outer_count + 1
    if "lookup_rule" in names:
        checker_count = checker_count + 1
print("기록 훅이 센 요청 수:", len(seen_tool_lists))
print("task를 받은 요청(바깥):", outer_count)
print("lookup_rule을 받은 요청(rule-checker):", checker_count)'''

USAGE = r'''# 바깥 목록에서 이번 실행이 더한 메시지만 Ch 19 05절 함수 sum_usage로 세고, 기록 훅이 센 바깥 요청 수와 견줍니다
run_usage = sum_usage(run_new)
print("바깥 목록으로 센 요청 수:", run_usage["requests"])
print("기록 훅이 센 바깥 요청 수:", outer_count)
print("입력 토큰:", run_usage["input_tokens"], "| 출력 토큰:", run_usage["output_tokens"])'''

CH26 = r'''# Ch 26 01절 셈(바깥 요청 수 + 부른 횟수 × 1)을 이번 실행에 대 보고, 기록 훅이 센 요청 수와 견줍니다
ch26_inner_requests = 1
ch26_count = run_usage["requests"] + len(asked_types) * ch26_inner_requests
print("Ch 26 셈으로 센 요청 수:", ch26_count)
print("기록 훅이 센 요청 수:", len(seen_tool_lists))
print("두 수가 같은가:", ch26_count == len(seen_tool_lists))
print("바깥 요청 수 + rule-checker 요청 수:", outer_count + checker_count)'''

COST = r'''# 2026-09-17 요금표(100만 토큰당 달러)로 바깥 요청의 예상 비용을 셉니다(Ch 6 06절 함수 estimate_cost — 서브에이전트 요청은 빠짐)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
outer_cost = estimate_cost(run_usage, input_rate, cached_input_rate, output_rate)
rounded_cost = round(outer_cost, 6)
print("바깥 요청의 예상 비용(달러):", rounded_cost)'''


def check_same_as_prev() -> None:
    """02·03·04절 셀과 같은 글이라고 적는 셀이 세 노트북 디스크 셀과 글자 그대로 같은지 봅니다."""
    sources_02 = author_02.notebook_code_sources(NB02)
    for cell in [RULES, DEF_TOOL, DEF_HOOK]:
        assert cell in sources_02, cell.splitlines()[0]
    sources_03 = author_02.notebook_code_sources(NB03)
    assert OUTER_LIMIT in sources_03, "OUTER_LIMIT가 03 노트북 셀과 다릅니다"
    sources_04 = author_02.notebook_code_sources(NB04)
    assert DEF_GRAPH in sources_04, "DEF_GRAPH가 04 노트북 셀과 다릅니다"
    # HELPER_SPEC은 02절 명세 글에 기록 훅 한 줄만 더한 판입니다(02절 셀과 그 줄만 다름)
    changed = author_02.HELPER_SPEC.replace('"middleware": [helper_limit],', '"middleware": [helper_limit, record_tool_names],')
    # 마지막 줄(자기 호출 한도 출력)은 06절이 더한 줄입니다
    assert HELPER_SPEC.splitlines()[1:-1] == changed.splitlines()[1:], "HELPER_SPEC이 02절 명세와 기록 훅 줄 밖에서 다릅니다"


def check_same_as_probe() -> None:
    """노트북 셀의 규정 글·도구·훅·명세·한도·바깥 에이전트·질문이 흔들림 확인 스크립트(probe06.py)와 같은 글인지 봅니다."""
    probe = (HERE / "probe/probe06.py").read_text(encoding="utf-8")
    pieces = []
    skip = ("#", "print(", "show_task_names")
    for cell in [RULES, DEF_TOOL, DEF_HOOK, CHECKER_SPEC, HELPER_SPEC, OUTER_LIMIT, RUN_PARENT]:
        for line in cell.splitlines():
            if line.startswith(skip):
                continue
            pieces.append(line)
    pieces.append('model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")')
    for piece in pieces:
        assert piece in probe, piece
    question_line = RUN.splitlines()[2]
    assert question_line.replace("question = ", "QUESTION = ") in probe


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/06-figures.md)
FIG1 = "06-1-맡겨야만-닿는-조립"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위에 나란한 두 칸이 있습니다. 왼쪽 칸 rule-checker 명세에는 초록 상자 도구 lookup_rule과 초록 상자 자기 호출 한도 4 기록 훅이, 오른쪽 칸 general-purpose 명세에는 초록 상자 도구를 적지 않음 바깥 도구를 물려받음과 초록 상자 자기 호출 한도 2 기록 훅이 있습니다. 두 칸에서 파란 상자 create_deep_agent 인자 tools 없음 명세 둘로 화살표가 가고, 거기서 노란 상자 둘로 갈라집니다. 하나는 바깥 에이전트 도구 아홉 lookup_rule이 있는가 False, 다른 하나는 task 설명 글 두 이름 줄 True 기본 general-purpose 설명 False인 그림"
FIG1_CAP = "조회 도구를 명세에만 주자 바깥 에이전트의 도구는 기본 아홉 그대로였고, task 설명 글에는 우리 명세 둘만 남았습니다."
FIG1_READ = """위에서 아래로 읽습니다.
맨 위 두 칸은 우리가 적은 명세이고, 서로 다른 서브에이전트라 나란히 두었습니다.
파란 상자는 우리가 부른 함수이고, 노란 상자 둘은 노트북 2·4절 출력입니다.
규정 도구는 rule-checker 명세에만 있어, 바깥 에이전트는 task로 맡겨야만 규정에 닿습니다."""

FIG2 = "06-2-모델-없이-task-불러-보기"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 손 요청 write_file /notes/question.md에서 노란 상자 상태 칸 files /notes/question.md로, 다시 초록 상자 손 요청 task rule-checker 복사본에게 넘긴 글 한 줄로 화살표가 갑니다. 그 아래 서브에이전트 rule-checker 복사본 칸 안에는 노란 상자 시작 기록 훅 메시지 수 1 HumanMessage 파일 위치 /notes/question.md에서 노란 상자 호출 한도 0 모델 요청 0으로 화살표가 갑니다. 칸에서 맨 아래 노란 상자 바깥 목록의 도구 메시지 task Model call limits exceeded run limit 0/0으로 화살표가 가는 그림"
FIG2_CAP = "모델 없이 task를 부르자 서브에이전트는 넘긴 글 한 줄과 바깥의 메모 파일을 받고 시작했고, 한도 0에서 한도 글만 남겼습니다."
FIG2_READ = """위에서 아래로 읽습니다.
초록 상자는 모델 없이 손으로 만든 요청이고, 노란 상자는 모두 노트북 3절 출력입니다.
칸 안은 서브에이전트 안에서 일어난 일이고, 시작 기록 훅이 받은 것을 적었습니다.
모델 요청이 한 번도 나가지 않아, 이 그림에는 모델 상자가 없습니다."""

FIG3 = "06-3-맡겨-본-실행의-차례"
FIG3_ALT = "세로선 넷이 있는 차례 그림입니다. 왼쪽부터 우리 코드, 바깥 에이전트, rule-checker, 연보라 띠 안의 모델 gpt-5.4-mini입니다. 우리 코드에서 질문 한 줄로 invoke 화살표가 바깥 에이전트로 갑니다. 요청 1 task를 받음 화살표가 모델로 가고 task 요청 rule-checker 점선이 돌아옵니다. 바깥 에이전트에서 rule-checker로 넘긴 글 한 줄과 files 화살표가 갑니다. 요청 2~4라는 되풀이 틀 안에서 lookup_rule을 받은 요청 화살표가 모델로 가고 응답 점선이 돌아옵니다. rule-checker에서 바깥 에이전트로 도구 메시지 하나와 files 점선이 가고, 노란 메모 상태 칸 files에 보고 파일이 있음이 붙습니다. 요청 5 뒤 도구 요청 없음 답 글이 돌아온 뒤 바깥 목록 넷 기록 훅 다섯 점선이 우리 코드로 돌아오는 그림"
FIG3_CAP = "이번 실행에서 바깥 에이전트는 rule-checker에게 한 번 맡겼고, rule-checker가 요청 셋을 보낸 뒤 상태 칸에 보고 파일이 남았습니다."
FIG3_READ = """세로선은 왼쪽부터 우리 코드, 바깥 에이전트, rule-checker, 모델이고, 위에서 아래로 읽습니다.
연보라 띠는 실제로 부른 모델 gpt-5.4-mini의 자리이고, 두 에이전트가 같은 모델 객체를 씁니다.
노란 메모는 노트북 5절 출력으로 확인한 보고 파일이고, 되풀이 틀은 기록 훅이 센 rule-checker 안의 요청 셋입니다.
맡긴 횟수와 요청 수는 흔들림 확인 다섯 번과 두 커널에서 같았을 때만 그렸습니다.
서브에이전트가 요청한 도구의 차례는 노트북 밖 기록 다섯 번에서만 보아, 그리지 않았습니다."""

FIG4 = "06-4-요청-수-두-가지-셈"
FIG4_ALT = "위에서 아래로 읽는 흐름도입니다. 나란한 두 칸이 있습니다. 왼쪽 칸 Ch 26 셈에는 노란 상자 바깥 목록으로 센 요청 수 2 더하기 task 부른 횟수 1 곱하기 1과 노란 상자 Ch 26 셈으로 센 요청 수 3 두 수가 같은가 False가 위아래로 있습니다. 오른쪽 칸 기록 훅으로 센 요청에는 노란 상자 task를 받은 요청 2 바깥, 노란 상자 lookup_rule을 받은 요청 3 rule-checker, 노란 상자 기록 훅이 센 요청 수 5가 위아래로 있습니다. 왼쪽 칸 아래에 회색 상자 셈 바깥은 도구를 요청한 응답 수 더하기 1 서브에이전트는 부른 횟수 곱하기 안 요청 수가 있는 그림"
FIG4_CAP = "이번 실행에서 Ch 26 셈은 3이었고 기록 훅은 5를 셌습니다. 도구를 가진 rule-checker가 한 번 불려 요청을 세 번 보냈기 때문입니다."
FIG4_READ = """나란한 두 칸은 같은 실행을 두 방법으로 센 것이라 나란히 두었고, 칸 안은 위에서 아래로 읽습니다.
노란 상자는 모두 노트북 6절 출력이고, 회색 상자는 두 커널과 흔들림 확인에서 모두 맞은 셈입니다.
Ch 26 셈은 바깥 목록만 보고, 서브에이전트 한 번을 요청 한 번으로 셉니다.
기록 훅은 서브에이전트 안의 요청까지 적어, 두 수가 달랐습니다."""

ILLU = "06-5-곁-온실에-맡긴-모종"
ILLU_ALT = "흰 바탕의 그림입니다. 왼쪽에는 지붕이 높은 큰 유리 온실이 있고, 그 오른쪽 벽에 지붕이 낮은 작은 곁 온실이 붙어 있습니다. 곁 온실 흙바닥에는 떡잎이 난 작은 유리병 셋이 나란히 놓여 있습니다. 큰 온실 가운데에는 흰 꽃이 핀 키 큰 화초가 든 유리병 하나가 서 있고, 그 옆 안쪽 벽에 작은 창 하나가 열려 있습니다. 큰 온실 왼쪽 흙바닥은 비어 있습니다. 사람·손·연장·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "작은 곁 온실에는 새싹 병 셋이 남고, 큰 온실에는 다 자란 화초 한 병만 와 있습니다."
ILLU_READ = "그림은 왼쪽의 큰 유리 온실과, 그 오른쪽 벽에 붙은 작은 곁 온실로 나뉩니다. 곁 온실 흙바닥에는 떡잎이 난 작은 유리병 셋이 나란히 놓여 있습니다. 큰 온실에는 꽃이 핀 다 자란 화초가 든 유리병 하나만 있고, 왼쪽 흙바닥은 비어 있습니다. 큰 온실이 바깥 에이전트, 곁 온실이 서브에이전트, 화초 한 병이 바깥 목록에 들어온 마지막 보고 글입니다. 큰 온실 안쪽 벽의 열린 작은 창과 병의 수·크기는 어떤 값과도 짝짓지 않습니다."

RUNS_SENTENCE = placeholder("RUNS_SENTENCE")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 규정 도구를 서브에이전트 명세에만 주어, 바깥 에이전트가 `task`로만 규정에 닿게 조립합니다.
2. 모델 없이 `task`를 손으로 불러, 서브에이전트가 무엇을 받고 무엇을 내놓는지 봅니다.
3. 실제 모델로 한 번 맡겨 보고, 서브에이전트의 요청까지 세어 Ch 26 셈과 견줍니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 5절에서 바깥 에이전트를 한 번 실행합니다.
노트북 밖에서 같은 질문을 다섯 번 보냈을 때, 요청은 다섯 번 모두 5번이었습니다.
바깥 에이전트 2번과 서브에이전트 3번을 더한 수입니다.

호출 한도는 바깥 10, 규정 확인 서브에이전트 4, general-purpose 2로 세 곳에 줍니다.
요금표로 어림한 예상 비용은 서브에이전트 요청까지 더해도 0.01달러 아래이고, 청구 금액이 아닙니다.
파일은 상태 칸 `files`에만 두고, 디스크에는 쓰지 않습니다.
모델의 답 글은 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.

앞에서 배운 함수 넷은 도구 파일 `harness_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 deepagents 0.7.0, langchain 1.4.0, langgraph 1.2.11입니다.
나머지 둘은 `langchain-openai` 1.6.0과 `python-dotenv` 1.2.3입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2·3절을 읽습니다.
모델 없이 위임의 조립과 서브에이전트가 받는 것을 보는 자리입니다.
4~6절은 실제 모델로 한 번 실행하는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch27-deepagents`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·요청은 5절에서만)를 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
모델 요청은 5절 실행 셀에서만 나갑니다.

2·3절은 이 객체로 Deep Agent를 만들기만 하고, 모델을 부르지 않습니다.
이 절은 파일을 디스크에 쓰지 않고, 상태 칸 `files`만 씁니다.

## 2. 규정 도구를 서브에이전트에게만 주기

맡길 일은 02절처럼 자료실 규정을 찾는 일입니다.
다음 셀은 02절 2절의 규정 글 셀과 같은 글입니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절에서는 Deep Agent가 일을 서브에이전트에게 맡기는 모양을 봅니다.
01절에서 본 것처럼, 바깥 에이전트는 도구 `task`로 서브에이전트를 부릅니다.
이번에는 규정 도구를 서브에이전트에게만 주어, 맡기지 않으면 규정에 닿지 못하게 조립합니다.

첫 셀은 패키지 다섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `deepagents: 0.7.0`과 `langgraph: 1.2.11`이 보입니다.
다섯 판 모두 실습 폴더 잠금과 같은 판입니다.
패키지 langgraph는 3절에서 04절의 작은 그래프를 다시 만들려고 설치 목록에 넣었습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
훅 데코레이터 `before_agent`는 Ch 22 01절에서 배웠고, 이 챕터에서는 이 절에서 처음 씁니다.
마지막 가져오기 줄은 앞에서 배운 함수 넷을 도구 파일 `harness_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, show_messages, sum_usage, tool_names`가 보입니다.
네 함수의 뜻은 02절 1절에 적었습니다.
앞에서 배운 함수는 `harness_tools.py`에 모아 두었고, 파일을 열면 코드를 볼 수 있습니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다."""),
    ] + model_cells() + [
        code(RULES),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '연장', '연체', '운영']`이 보입니다.
02절과 같은 교재용 규정이고, 실제 도서관 규정이 아닙니다.

다음 셀도 02절의 도구 셀과 같은 글입니다.
맨 위 `@tool` 줄이 아래 함수를 도구로 등록하는 것도 02절과 같습니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 `lookup_rule`은 주제어 하나로 규정 글 하나를 찾습니다.
이 절에서는 이 도구를 서브에이전트 명세에만 넣고, 바깥 에이전트에는 주지 않습니다.

5절에서는 서브에이전트의 요청까지 세어 봅니다.
그래서 명세를 만들기 전에, 요청마다 모델이 받은 도구 이름을 적는 기록 훅을 먼저 만듭니다.
다음 셀은 02절 5절의 기록 훅 셀과 같은 글입니다."""),
        code(DEF_HOOK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 훅은 요청마다 모델이 받은 도구 이름 목록을 `seen_tool_lists`에 붙입니다.
이 훅을 바깥 에이전트와 서브에이전트에 모두 넣으면, 받은 도구로 누구의 요청인지 가를 수 있습니다.

다음 셀은 규정 확인을 맡을 서브에이전트 명세입니다.
01절에서 명세는 서브에이전트의 이름·설명·시스템 메시지 글·미들웨어를 적은 딕셔너리라고 했습니다.
이번에는 키 `tools`도 적어, 이 서브에이전트만 쓸 도구를 줍니다.
키마다 한 줄로 적었습니다."""),
        code(CHECKER_SPEC),
        md("""**결과 읽기** — 출력 줄 `명세의 키: ['name', 'description', 'system_prompt', 'tools', 'middleware']`가 보입니다.
키 `name`은 `task`로 부를 이름이고, `description`은 바깥 모델이 읽고 고를 설명입니다.
키 `system_prompt`는 서브에이전트의 시스템 메시지 글이고, 무엇을 남기면 끝나는지 적었습니다.
키 `tools`의 도구는 이 서브에이전트만 받고, `middleware`에는 호출 한도와 기록 훅을 넣었습니다.
출력 줄 `자기 호출 한도: 4`는 찾기·적기·보고 세 요청에 하나를 더한 값입니다.

설치판 `graph.py` 728행에서, 키 `tools`가 없으면 바깥 에이전트의 도구를 물려받습니다.
적으면 그 목록이 물려받을 도구를 대신합니다.

다음 셀은 이 명세 하나만 넘겨 바깥 에이전트를 만듭니다.
인자 `tools=`는 넘기지 않아, 바깥 에이전트에는 규정 도구가 없습니다."""),
        code(PLAIN_PARENT),
        md("""**결과 읽기** — 출력 줄 `바깥 에이전트의 도구 수: 9`와 `바깥 에이전트에 lookup_rule이 있는가: False`가 보입니다.
01절에서 본 기본 도구 아홉 그대로이고, 규정 도구는 없습니다.
바깥 에이전트가 규정을 보려면 `task`로 맡기는 길밖에 없습니다.
맡길지 말지가 모델의 선택만이 아니라, 조립으로도 정해진 셈입니다.

도구 `task`의 설명 글에는 맡길 수 있는 서브에이전트가 「- 이름: 설명」 줄로 적힙니다.
설치판 `middleware/subagents.py` 464~468행이 그 글을 만듭니다.
다음 셀은 이름 목록을 받아, 이름마다 그 줄이 있는지 출력하는 함수입니다.
기본 general-purpose의 설명 글이 남았는지도 함께 출력합니다."""),
        code(DEF_SHOW_TASK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
기본 general-purpose의 설명 글은 「General-purpose agent」로 시작해서, 그 글이 있는지로 봅니다.

다음 셀은 명세 하나만 넘긴 바깥 에이전트로 이 함수를 부릅니다.
실행 전에 예상해 봅니다.
넘긴 명세는 rule-checker 하나이니, 이름 줄도 하나일까요?"""),
        code(SHOW_PLAIN),
        md("""**결과 읽기** — 출력 줄 `general-purpose 줄이 있는가: True`와 `rule-checker 줄이 있는가: True`가 보입니다.
출력 줄 `기본 general-purpose 설명이 남았는가: True`도 보입니다.
명세는 rule-checker 하나만 넘겼는데, 기본 general-purpose 서브에이전트도 함께 붙었습니다.
01절에서 본 것처럼, 이 기본 서브에이전트에는 호출 한도가 없습니다.

그래서 01절처럼 같은 이름 general-purpose 명세도 함께 넘깁니다.
다음 셀은 02절 명세 글에 기록 훅 하나만 더한 명세입니다.
기본 서브에이전트에는 바깥 미들웨어가 옮겨 가지 않아, 기록 훅도 명세에 따로 넣어야 요청이 적힙니다."""),
        code(HELPER_SPEC),
        md("""**결과 읽기** — 출력 줄 `명세의 키: ['name', 'description', 'system_prompt', 'middleware']`와 `자기 호출 한도: 2`가 보입니다.
키 `tools`가 없어, 이 서브에이전트는 바깥 에이전트의 도구를 물려받습니다.
바깥 에이전트에 넘긴 도구가 없으니, 설치판 소스대로라면 받는 도구는 파일 도구뿐입니다.
이 명세를 함께 넘긴 조립은 4절에서 봅니다.

## 3. 모델 없이 task를 불러 보기

서브에이전트가 무엇을 받고 시작하는지 모델 없이 보려고, 04절의 작은 그래프 함수를 다시 씁니다.
다음 셀은 04절 3절 셀과 같은 글입니다."""),
        code(DEF_GRAPH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
작은 그래프의 상태 형식에는 칸 `files`가 있어, 입력에 파일을 함께 넣을 수 있습니다.

다음 셀은 서브에이전트가 시작할 때 받은 것을 적는 훅입니다.
맨 위 `@before_agent` 줄은 아래 함수를, 에이전트 실행이 시작될 때 한 번 도는 훅으로 등록합니다.
Ch 22 01절에서 본 노드형 훅이고, 인자 `state`로 그때의 상태를 받습니다.
기록 한 줄은 한국어 키 딕셔너리로 적습니다."""),
        code(DEF_RECORD_INPUTS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
받은 메시지 수, 첫 메시지의 종류와 글, 상태 칸 `files`의 파일 위치를 적습니다.

모델 없이 보려면, 서브에이전트가 모델을 부르기 전에 멈춰야 합니다.
01절 6절처럼 호출 한도 0을 쓰면, 모델 요청 없이 한도 글만 남기고 끝납니다.
다음 셀은 규정 확인 명세를 복사해, 미들웨어만 이 훅과 한도 0으로 바꿉니다.
메서드 `copy`는 Ch 18 05절처럼 딕셔너리를 한 벌 더 만듭니다."""),
        code(ZERO_SPEC),
        md("""**결과 읽기** — 출력 줄 `같은 이름인가: True`와 `원래 명세의 미들웨어 수: 2`가 보입니다.
복사본의 키를 바꿔도 원래 명세는 그대로입니다.
시작 기록 훅은 모델 앞에서 한도를 따지기 전, 실행 첫머리에 한 번 돕니다.

다음 셀은 복사본과 general-purpose 명세로 바깥 에이전트를 만듭니다.
그리고 도구 실행 노드만 든 작은 그래프를 만듭니다."""),
        code(ZERO_GRAPH),
        md("""**결과 읽기** — 출력 줄 `작은 그래프의 노드: ['__start__', 'tools', '__end__']`가 보입니다.
도구 실행 노드에는 도구 `task`도 들어 있어, 손으로 만든 `task` 요청을 넣을 수 있습니다.

먼저 04절 3절처럼 손 요청으로 메모 파일 하나를 상태 칸 `files`에 적습니다.
바깥 상태에 있는 파일이 서브에이전트에게도 보이는지 보려는 것입니다."""),
        code(HAND_WRITE),
        md("""**결과 읽기** — 출력 줄 `도구 메시지: Updated file /notes/question.md`가 보입니다.
출력 줄 `상태 칸 files의 파일 위치: ['/notes/question.md']`에서, 메모 파일이 상태 칸에 생겼습니다.

다음 셀은 rule-checker에게 맡기는 `task` 요청을 손으로 만듭니다.
인자는 01절에서 본 둘로, 넘길 글 `description`과 서브에이전트 이름 `subagent_type`입니다.
앞 셀 결과의 `files`를 입력에 함께 넣어, 바깥 상태에 메모 파일이 있는 채로 부릅니다.
실행 전에 예상해 봅니다.
서브에이전트는 넘긴 글 한 줄로 시작하고, 모델을 부르기 전에 멈출 것입니다."""),
        code(HAND_TASK),
        md("""**결과 읽기** — 라벨 `서브에이전트가 시작할 때 받은 것:` 뒤에 기록 한 줄이 보입니다.
메시지 수는 1이고, 첫 메시지는 `HumanMessage`이며 글은 넘긴 글 그대로입니다.
파일 위치에는 `/notes/question.md`가 있습니다.
서브에이전트는 바깥 메시지 목록 없이, 넘긴 글 한 줄과 바깥 상태 칸 `files`로 시작했습니다.
Ch 26 01절의 안쪽 목록처럼 새 목록으로 시작하지만, 파일은 함께 봅니다.

설치판 `middleware/subagents.py` 537~539행에서, 바깥 상태의 칸 가운데 `messages`·`todos` 등을 빼고 넘깁니다.
다음 셀은 바깥으로 온 도구 메시지와, 실행 뒤 상태 칸 `files`를 봅니다."""),
        code(SHOW_ZERO),
        md("""**결과 읽기** — 출력 줄 `도구 메시지 내용: Model call limits exceeded: run limit (0/0)`이 보입니다.
서브에이전트는 모델을 한 번도 부르지 않고 한도 글만 남긴 채 끝났습니다.
도구 `task`는 서브에이전트의 마지막 글 하나를 도구 메시지에 담아 바깥 목록에 넣습니다.
출력 줄 `결과 메시지 수: 2`는 손 요청 하나와 그 도구 메시지 하나입니다.
메모 파일은 실행 뒤에도 상태 칸에 그대로 있고, 이 셀까지 모델 요청은 0번입니다.

서브에이전트가 새로 쓴 파일이 바깥 상태 칸에 더해지는지는, 모델이 있어야 보입니다.
설치판 `middleware/subagents.py` 474~512행은 서브에이전트 결과의 칸을 바깥 상태의 갱신으로 넘깁니다.
5절 실행에서 그 모양을 봅니다.

## 4. 실제 모델을 부를 준비

5절에서는 이 조립에 실제 모델을 붙여 한 번 맡겨 봅니다.
다음 셀은 03절 셀과 같은 글의 바깥 호출 한도입니다."""),
        code(OUTER_LIMIT),
        md("""**결과 읽기** — 출력 줄 `바깥 호출 한도: 10`이 보입니다.
주석의 「02절 셀과 한도만 다름」은 이 셀을 처음 쓴 03절에서 적은 말입니다.

이제 호출 한도가 세 곳에 있습니다.
바깥 10, rule-checker 4, general-purpose 2입니다.
도구 `task`는 부를 때마다 서브에이전트를 새로 실행해서, 명세의 한도도 한 번 부를 때마다 새로 셉니다.
그래서 한 번 실행의 요청 수는 10에 두 값을 더한 수를 넘지 않습니다.
두 값은 rule-checker를 부른 횟수 × 4와 general-purpose를 부른 횟수 × 2입니다.

다만 한 응답에 `task` 요청을 몇 개 담을지는 막지 못해, 그 수만큼 상한이 커집니다.
다음 셀은 바깥 에이전트를 만듭니다.
인자 `tools=`는 이번에도 넘기지 않고, 두 명세를 함께 넘깁니다.
우리 시스템 메시지 글에는 규정을 직접 찾지 말고 rule-checker에게 맡기라고 적었습니다."""),
        code(RUN_PARENT),
        md("""**결과 읽기** — 출력 줄 `바깥 에이전트에 lookup_rule이 있는가: False`가 보입니다.
출력 줄 `기본 general-purpose 설명이 남았는가: False`에서, 같은 이름 명세가 기본 자리를 바꿨습니다.
두 이름 줄은 모두 `True`라, 이 바깥 에이전트가 맡길 수 있는 곳은 우리 명세 둘뿐입니다.
두 명세 모두 호출 한도가 있고, 기록 훅은 바깥과 두 명세에 모두 들어 있습니다.

## 5. 실제 모델로 맡겨 보기

질문은 02절과 같은 글입니다.
실행 전에 예상해 봅니다.
바깥 에이전트는 `task`로 rule-checker에게 맡길 것입니다.
그러면 rule-checker는 규정을 찾아 파일에 적은 뒤 보고할 것입니다."""),
        code(RUN),
        md("""**결과 읽기** — 라벨 `결과 메시지 수:` 뒤에 바깥 목록의 메시지 수가 보입니다.
넣은 질문 하나 뒤에, 바깥 모델의 응답과 도구 메시지가 더해졌습니다.

""" + placeholder("RUN") + """

다음 셀은 Ch 19 06절 함수 `show_messages`로 바깥 목록을 차례로 봅니다."""),
        code(SHOW),
        md("""**결과 읽기** — 라벨 줄 아래가 바깥 목록의 메시지 차례입니다.
`ToolMessage` 줄의 내용은 서브에이전트가 마지막에 쓴 보고 글입니다.
바깥 목록에는 서브에이전트의 응답도, 서브에이전트가 부른 도구의 메시지도 없습니다.
마지막 `AIMessage` 줄은 도구 요청이 없는 응답이고, 바깥 모델이 쓴 답입니다.

""" + placeholder("SHOW") + """

다음 셀은 이번 실행이 더한 응답에서 `task` 요청을 골라, 맡긴 서브에이전트 이름을 모읍니다."""),
        code(ASKED),
        md("""**결과 읽기** — 라벨 `task로 맡긴 서브에이전트:` 뒤에 이름 목록이 보입니다.
모델이 도구 `task`를 부르며 인자 `subagent_type`에 적은 이름입니다.

""" + placeholder("ASKED") + """

다음 셀은 바깥 목록의 도구 메시지 이름을 모읍니다.
서브에이전트가 부른 도구의 메시지가 바깥 목록에 있는지 봅니다."""),
        code(OUTER_TOOLS),
        md("""**결과 읽기** — 출력 줄 `lookup_rule 도구 메시지가 있는가: False`가 보입니다.
바깥 에이전트에는 규정 도구가 없어, 이 값은 조립으로 정해집니다.
서브에이전트가 부른 도구의 결과는 서브에이전트 안에만 남고, 바깥 목록에는 오지 않습니다.

""" + placeholder("OUTER_TOOLS") + """

다음 셀은 실행 뒤 상태 칸 `files`를 봅니다."""),
        code(FILES),
        md("""**결과 읽기** — 라벨 `상태 칸 files의 파일 위치:` 뒤에 파일 위치 목록이 보입니다.
보고 파일이 있으면, 라벨 `보고 파일의 글:` 아래에 그 글이 보입니다.

""" + placeholder("FILES") + """

## 6. 요청 수 세기와 예상 비용

바깥 목록만 세면 서브에이전트의 요청이 빠집니다.
다음 셀은 기록 훅 목록을 받은 도구로 나눠 셉니다.
도구 `task`를 받은 요청은 바깥 요청이고, `lookup_rule`을 받은 요청은 rule-checker의 요청입니다."""),
        code(SPLIT),
        md("""**결과 읽기** — 라벨 `기록 훅이 센 요청 수:` 뒤가 이번 실행의 모델 요청을 모두 센 수입니다.
서브에이전트에는 도구 `task`가 없어, 두 도구를 함께 받은 요청은 생기지 않습니다.
설치판 `graph.py` 666~674행에서 서브에이전트의 기본 미들웨어에는 서브에이전트 미들웨어가 없습니다.

""" + placeholder("SPLIT") + """

다음 셀은 바깥 목록에서 센 요청 수를 기록 훅이 센 바깥 요청 수와 견줍니다."""),
        code(USAGE),
        md("""**결과 읽기** — 라벨 `바깥 목록으로 센 요청 수:`와 `기록 훅이 센 바깥 요청 수:` 뒤의 수가 같습니다.
바깥 목록의 응답은 모두 바깥 에이전트의 요청입니다.
입력·출력 토큰도 바깥 요청만의 합입니다.

""" + placeholder("USAGE") + """

다음 셀은 Ch 26 01절의 셈을 이번 실행에 대 봅니다.
그 셈은 바깥 요청 수에 서브에이전트를 부른 횟수 × 1을 더했습니다."""),
        code(CH26),
        md("""**결과 읽기** — 라벨 `Ch 26 셈으로 센 요청 수:` 뒤와 `기록 훅이 센 요청 수:` 뒤를 견줍니다.
Ch 26 01절의 전문 에이전트는 도구가 없어, 한 번 부르면 모델 요청이 한 번이었습니다.
이 절의 서브에이전트는 도구를 가져, 한 번 부를 때 요청이 여러 번 나갈 수 있습니다.
셈은 바깥 요청 수에, 부른 횟수 × 그 실행 안 요청 수를 더하는 모양이 됩니다.

""" + placeholder("CH26") + """

다음 셀은 02절과 같은 요금표로 예상 비용을 셉니다.
바깥 목록의 응답만으로 세므로, 라벨에 「바깥 요청의」를 붙였습니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 `바깥 요청의 예상 비용(달러):` 뒤에 어림값이 보입니다.
바깥 목록의 응답만으로 셈해서, 서브에이전트 요청의 토큰은 들어 있지 않습니다.
이 노트북의 기록 훅은 도구 이름만 적어, 서브에이전트 요청의 토큰은 세지 않았습니다.
예상 비용은 청구 금액이 아닙니다.

""" + placeholder("COST") + """

## 정리

1. 규정 도구를 서브에이전트 명세에만 주면, 바깥 에이전트는 `task`로 맡겨야만 규정에 닿습니다.
2. 서브에이전트는 넘긴 글 한 줄과 바깥 상태 칸 `files`로 시작하고, 바깥 목록에는 마지막 보고 글 하나만 옵니다.
3. 바깥 목록만 세면 서브에이전트 요청이 빠지고, 도구를 가진 서브에이전트는 한 번에 요청을 여러 번 보낼 수 있습니다.

07절에서는 교재용 자료를 상태 칸 `files`에 넣고, 모델이 파일 도구로 찾아 쓴 조사를 봅니다.
모델이 든 출처 파일이 실제로 있는지는 코드로 확인합니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH08_03 = "../../part2/ch08-context-engineering/03-Compress와-Isolate.html"
L_CH18_05 = "../../part5/ch18-workflow-patterns/05-생성자-평가자와-정지-조건.html"
L_CH22_01 = "../ch22-middleware/01-미들웨어와-6개-훅.html"
L_CH22_08 = "../ch22-middleware/08-컨텍스트-분리와-Isolate.html"
L_CH26_01 = "../ch26-delegation/01-Subagent-도구-위임.html"
L_CH26_04 = "../ch26-delegation/04-호출-수-비용-종료-조건-비교.html"
L_01 = "01-하네스와-일곱-기능.html"
L_02 = "02-create-deep-agent와-도구.html"
L_03 = "03-플래닝과-시스템-프롬프트.html"
L_04 = "04-파일시스템과-중간-결과.html"
L_05 = "05-컨텍스트-관리와-오프로딩.html"
L_07 = "07-출처-검증형-deep-research.html"

SPEC_ROWS = [
    ("<code>name</code>", "<code>\"rule-checker\"</code>", "도구 <code>task</code>의 인자 <code>subagent_type</code>에 적는 이름"),
    ("<code>description</code>", "규정을 찾아 확인하는 담당이라는 설명", "바깥 모델이 <code>task</code> 설명 글에서 읽고 맡길 곳을 고르는 글"),
    ("<code>system_prompt</code>", "찾기·적기·보고의 차례와 보고 파일 위치", "서브에이전트의 시스템 메시지 글. 무엇을 남기면 끝나는지 적음"),
    ("<code>tools</code>", "<code>[lookup_rule]</code>", "이 서브에이전트만 받는 도구. 적지 않으면 바깥 도구를 물려받음"),
    ("<code>middleware</code>", "호출 한도 4 · 기록 훅", "이 서브에이전트의 요청에만 걸리는 미들웨어"),
]

RESULT_ROWS = [
    ("조회 도구 없는 바깥 에이전트", "<code>바깥 에이전트의 도구 수: 9</code> · <code>바깥 에이전트에 lookup_rule이 있는가: False</code>", "구조 값"),
    ("명세 하나만 넘긴 <code>task</code> 설명 글", "<code>general-purpose 줄이 있는가: True</code> · <code>기본 general-purpose 설명이 남았는가: True</code>", "구조 값"),
    ("한도 0 복사본에 손으로 맡김", "받은 메시지 수 1 · 파일 위치 <code>/notes/question.md</code> · <code>도구 메시지 내용: Model call limits exceeded: run limit (0/0)</code>", "구조 값"),
    ("두 명세를 넘긴 바깥 에이전트", "<code>기본 general-purpose 설명이 남았는가: False</code>", "구조 값"),
    ("5절 바깥 목록", "<code>lookup_rule 도구 메시지가 있는가: False</code> · 바깥 목록으로 센 요청 수와 기록 훅이 센 바깥 요청 수가 같음", "구조 값"),
    ("5절 맡긴 곳과 요청 수", placeholder("ROW_JUDGE"), "모델 판단 값"),
    ("5절 글·토큰·예상 비용", placeholder("ROW_SHAKY"), "흔들리는 값"),
]

LOOK_B5 = "노트북 2절에서 <code>바깥 에이전트에 lookup_rule이 있는가: False</code>와 <code>기본 general-purpose 설명이 남았는가: True</code>를 확인합니다. 3절에서 <code>도구 메시지 내용: Model call limits exceeded: run limit (0/0)</code>을 봅니다. 4절에서 기본 설명이 남았는지를 다시 보고, 6절에서 두 방법으로 센 바깥 요청 수가 같은지 확인합니다."


def src_html() -> str:
    specs = table_html(["키", "이 절에서 넣은 값", "뜻"], SPEC_ROWS)
    results = table_html(["확인한 것", "교재 출력", "값의 성격"], RESULT_ROWS)
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>규정 도구를 서브에이전트 명세에만 주어, 바깥 에이전트가 <code>task</code>로만 규정에 닿는 조립을 만들 수 있습니다.</li>
<li>서브에이전트가 시작할 때 받는 것과 바깥으로 내놓는 것을 출력으로 짚을 수 있습니다.</li>
<li>서브에이전트 요청까지 세는 방법과, 호출 한도를 세 곳에 주는 까닭을 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>05절까지의 실제 모델 실행에서는 바깥 에이전트가 도구를 모두 직접 불렀습니다. 도구 결과는 바깥 메시지 목록에 쌓이고, 다음 요청마다 함께 실립니다. 일의 한 부분을 서브에이전트에게 맡기면, 바깥 목록에는 그 서브에이전트의 마지막 보고 글만 남습니다.</p><p>이 절은 자료실 규정을 찾는 일을 서브에이전트에게 맡깁니다. 앞 절반은 모델 없이, 맡기는 조립과 서브에이전트가 받는 것을 봅니다. 뒤 절반은 실제 모델로 한 번 맡기고, 서브에이전트의 요청까지 셉니다. 그 셈이 Ch 26과 왜 다른지도 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH26_01 + """\">Ch 26 01절</a>에서는 도구 함수 안에서 전문 에이전트를 부르는 서브에이전트를 만들었습니다. 전문 에이전트는 넘긴 글 한 줄로 시작한 안쪽 목록에서 일했고, 바깥 목록에는 마지막 답 글만 들어갔습니다. 그 전문 에이전트는 도구가 없어서, 요청 수는 바깥 요청 수에 부른 횟수 × 1을 더한 값이었습니다. <a href=\"""" + L_CH26_04 + """\">Ch 26</a>에서 서브에이전트의 완료 조건을 적었습니다. 이 절은 명세의 시스템 메시지 글에, 무엇을 남기면 일이 끝나는지 적습니다.</p><p><a href=\"""" + L_CH08_03 + """\">Ch 8 03절</a>에서는 일을 나눠 따로 받은 컨텍스트로 처리하는 일을 나누기(Isolate)라고 불렀습니다. <a href=\"""" + L_CH22_08 + """\">Ch 22 08절</a>의 컨텍스트 분리도 같은 생각이었습니다. <a href=\"""" + L_CH22_01 + """\">Ch 22 01절</a>에서는 에이전트 실행이 시작될 때 한 번 도는 훅 <code>before_agent</code>를 보았습니다. <a href=\"""" + L_CH18_05 + """\">Ch 18 05절</a>에서는 딕셔너리 메서드 <code>copy</code>로 설정을 복사해 한 칸만 바꿨습니다.</p><p><a href=\"""" + L_01 + """\">01절</a>에서는 general-purpose 서브에이전트가 늘 붙고, 거기에는 호출 한도가 없다는 것을 보았습니다. 같은 이름 명세로 그 자리를 바꾸고, 한도 0으로 <code>task</code>를 손 요청하는 모양도 보았습니다. <a href=\"""" + L_02 + """\">02절</a>의 규정 도구와 기록 훅, <a href=\"""" + L_03 + """\">03절</a>의 바깥 호출 한도를 이 절이 그대로 씁니다. <a href=\"""" + L_04 + """\">04절</a>에서는 기본 백엔드가 파일을 상태 칸 <code>files</code>에 두는 것을 보았습니다. <a href=\"""" + L_05 + """\">05절</a>은 서브에이전트가 이 칸을 함께 쓰는 모양을 이 절로 넘겼습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 쓴 큰 유리 온실 오른쪽에, 벽을 맞댄 작은 곁 온실 한 채가 있다고 합시다. 큰 온실은 모종을 키우는 일을 곁 온실에 맡깁니다. 곁 온실 흙바닥에는 새싹이 든 작은 유리병 여럿이 놓여, 일은 거기서 벌어집니다. 큰 온실로 건너온 것은 다 자란 화초가 든 유리병 하나뿐이고, 나머지 흙바닥은 비어 있습니다.</p><p>큰 온실이 바깥 에이전트이고, 곁 온실이 서브에이전트입니다. 곁 온실 안의 새싹 병들은 서브에이전트 안에서 오간 요청과 도구 결과이고, 큰 온실에는 들어오지 않습니다. 큰 온실의 다 자란 화초 한 병은 바깥 목록에 들어오는 마지막 보고 글입니다.</p><p>비유와 다른 점이 있습니다. 곁 온실은 부를 때마다 새로 비운 채로 시작하지만, 상태 칸 <code>files</code>는 두 쪽이 함께 봅니다. 또 「다 자람」은 걸린 시간을 뜻하지 않고, 병의 수는 어떤 값과도 짝짓지 않습니다.</p>
""" + illustration_block() + """<h3>명세로 맡길 곳 만들기</h3><p>서브에이전트는 명세로 만듭니다. 01절에서 명세는 이름·설명·시스템 메시지 글·미들웨어를 적은 딕셔너리라고 했습니다. 이 절은 키 <code>tools</code>를 더해, 규정 도구를 rule-checker 명세에만 넣었습니다. 아래 표는 이 절 명세의 키 다섯입니다.</p>
""" + specs + """
<p>바깥 에이전트에는 인자 <code>tools=</code>를 주지 않았습니다. 그래서 바깥 에이전트의 도구는 <code>바깥 에이전트의 도구 수: 9</code>로 기본 아홉 그대로이고, 규정 도구가 없습니다. 바깥 에이전트가 규정을 보려면 <code>task</code>로 맡겨야 합니다. 맡길지는 모델이 고르지만, 규정에 닿는 길은 조립이 하나로 정했습니다.</p><p>명세를 rule-checker 하나만 넘기면, 도구 <code>task</code>의 설명 글에 기본 general-purpose 줄도 함께 남았습니다. 01절에서 본 것처럼, 그 기본 서브에이전트에는 호출 한도가 없습니다. 그래서 같은 이름 general-purpose 명세를 함께 넘겨 기본 자리를 바꿨습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>서브에이전트가 받는 것과 내놓는 것</h3><p>도구 <code>task</code>는 부를 때마다 서브에이전트를 새로 실행합니다. 모델 없이 보려고, 한도 0인 복사본 명세에 <code>task</code>를 손 요청했습니다. 시작 기록 훅이 적은 것은 메시지 하나(넘긴 글)와 바깥 상태의 메모 파일 위치였습니다. 서브에이전트는 바깥 메시지 목록을 받지 않지만, 상태 칸 <code>files</code>는 함께 봅니다.</p><p>서브에이전트가 끝나면 <code>task</code>는 마지막 글 하나를 도구 메시지에 담아 바깥 목록에 넣습니다. 한도 0에서는 그 글이 한도 글 <code>Model call limits exceeded: run limit (0/0)</code>이었습니다. 서브에이전트 결과의 칸 <code>files</code>는 바깥 상태의 갱신으로 넘어갑니다. 설치판 <code>middleware/subagents.py</code> 474~512행이 그 자리이고, 모양은 5절 실행에서 봅니다.</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h3>호출 한도는 세 곳에</h3><p>01절 안전 규칙대로 호출 한도를 세 곳에 줍니다. 바깥 에이전트 10, rule-checker 4, general-purpose 2입니다. 명세의 한도는 그 서브에이전트의 요청에만 걸리고, <code>task</code>를 부를 때마다 새로 셉니다. 그래서 한 번 실행의 요청 수는 10에, 부른 횟수마다 그 명세의 한도를 더한 값을 넘지 않습니다.</p><p>남는 틈도 있습니다. 한 응답에 <code>task</code> 요청을 몇 개 담을지는 막는 장치가 없어, 그 수만큼 상한이 커집니다. 도구 <code>task</code>의 설명 글은 서로 무관한 일이면 여럿을 한 응답에 함께 부르라고 권합니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 규정 도구와 두 명세를 만들고, 조회 도구 없는 바깥 에이전트를 조립합니다. 3절은 모델 없이 <code>task</code>를 손 요청해, 서브에이전트가 받는 것과 내놓는 것을 봅니다. 4·5절은 실제 모델로 한 번 맡기고, 6절은 기록 훅으로 요청을 나눠 셉니다.</p><p>모델 요청은 5절 실행 셀에서만 나갑니다. 노트북 밖에서 같은 질문을 다섯 번 보냈을 때, 요청은 다섯 번 모두 5번이었습니다. 요금표로 어림한 예상 비용은 서브에이전트 요청까지 더해도 0.01달러 아래이고, 청구 금액이 아닙니다. 디스크에는 파일을 쓰지 않고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>앞 절반의 값은 모두 코드가 정하는 구조 값입니다. 바깥 에이전트에는 규정 도구가 없고, 명세 하나만 넘기면 기본 general-purpose가 함께 붙었습니다. 한도 0으로 부른 서브에이전트는 넘긴 글 한 줄과 바깥의 메모 파일로 시작했고, 모델 요청 없이 한도 글만 내놓았습니다.</p><p>아래 표는 이 절이 확인한 값과 그 성격입니다. 구조 값은 코드가 정하는 값이고, 모델 판단 값은 모델이 고른 값입니다. 흔들리는 값은 실행마다 달라질 수 있어 결론에 쓰지 않습니다.</p>
""" + results + """
<p>5절 실행에서도 바깥 목록에는 서브에이전트의 응답과 도구 메시지가 없었습니다. 바깥 목록으로 센 요청 수는 기록 훅이 센 바깥 요청 수와 같았고, 서브에이전트 요청은 기록 훅만 셌습니다. 그래서 요청 수를 바깥 목록만으로 세면 모자랍니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>""" + placeholder("B6_JUDGE") + """</p>
<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + placeholder("LOOK_B6") + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>공식 서브에이전트 문서는 명세 키 <code>mode</code>와, 부모 대화를 물려받는 <code>"fork"</code> 방식을 적습니다. 설치판 0.7.0 명세에는 이 키가 없고, <code>task</code>는 늘 넘긴 글 한 줄로 시작합니다. 다른 판을 쓰면 명세 키를 먼저 확인합니다.</li><li>설치판 <code>middleware/subagents.py</code> 556~567행에서, 서브에이전트는 자기 그래프에 묶인 설정으로 실행됩니다. 바깥 실행 한도(<code>recursion_limit</code>)는 서브에이전트 안에 닿지 않아, 요청 수는 명세마다 준 호출 한도로 막습니다. 이 노트북에서는 실행하지 않았습니다.</li><li>""" + placeholder("B7_MANY") + """</li><li>general-purpose 명세에는 <code>tools</code>를 적지 않았고, 바깥 에이전트에도 넘긴 도구가 없습니다. 설치판 <code>graph.py</code> 728행대로라면 이 서브에이전트가 받는 도구는 파일 도구뿐입니다. 이 노트북에서는 general-purpose를 부르지 않았습니다.</li><li>명세에 <code>permissions</code>·<code>interrupt_on</code>을 적지 않으면 바깥 설정을 물려받습니다. 설치판 <code>graph.py</code> 664·720행이 그 자리이고, 공식 문서는 스킬은 물려받지 않는다고 적습니다. 이 노트북에서는 실행하지 않았습니다.</li><li>6절 예상 비용은 바깥 목록의 응답만으로 셈한 값입니다. """ + placeholder("B7_COST") + """</li><li>""" + placeholder("B7_PROBE") + """</li><li>두 시스템 메시지 글, 보고 파일 위치, 한도 4, 메모 파일은 흐름을 보여 주려고 실행 전에 정한 예입니다. 바깥 글에는 rule-checker에게 맡기라고, rule-checker 글에는 찾기·적기·보고의 차례를 적었습니다. 결과를 보고 바꾸지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>규정 도구를 서브에이전트 명세에만 주면, 바깥 에이전트는 <code>task</code>로 맡겨야만 규정에 닿습니다.</li><li>서브에이전트는 넘긴 글 한 줄과 바깥 상태 칸 <code>files</code>로 시작하고, 바깥 목록에는 마지막 보고 글 하나만 옵니다.</li><li>바깥 목록만 세면 서브에이전트 요청이 빠지고, 도구를 가진 서브에이전트는 한 번에 요청을 여러 번 보낼 수 있습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_07 + """\">07절</a>에서는 교재용 자료를 상태 칸 <code>files</code>에 넣고, 모델이 파일 도구로 찾아 쓴 조사를 봅니다. 모델이 든 출처 파일이 실제로 있는지는 코드로 확인합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 바깥 에이전트에는 <code>tools=</code>를 주지 않고, rule-checker 명세에만 <code>lookup_rule</code>을 넣었습니다. 바깥 에이전트가 규정을 보려면 무엇이 필요한가요?</p><p class="quiz-a">도구 <code>task</code>로 rule-checker에게 맡겨야 합니다. 바깥 에이전트의 도구는 기본 아홉뿐이고 규정 도구가 없습니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. 명세를 rule-checker 하나만 넘겼는데 <code>task</code> 설명 글에 general-purpose 줄이 있었습니다. 같은 이름 명세를 함께 넘기는 까닭은 무엇인가요?</p><p class="quiz-a">기본 general-purpose 서브에이전트가 늘 붙고, 거기에는 호출 한도가 없기 때문입니다. 같은 이름 명세로 그 자리를 바꾸면 자기 호출 한도와 기록 훅을 넣을 수 있습니다. 틀렸다면 노트북 2절과 4절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 「서브에이전트를 한 번 불렀으니 요청 수는 바깥 요청 수에 1을 더하면 된다」고 셉니다. 이 절 조립에서도 맞나요?</p><p class="quiz-a">맞지 않을 수 있습니다. 도구를 가진 서브에이전트는 한 번 불려도, 도구를 요청한 응답 수에 1을 더한 만큼 요청을 보냅니다. 셈은 바깥 요청 수에 부른 횟수 × 그 실행 안 요청 수를 더하고, 안쪽 요청은 기록 훅으로 셉니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">4. 한도 0인 복사본 명세로 <code>task</code>를 손 요청했습니다. 서브에이전트가 시작할 때 받은 것 두 가지와, 바깥으로 온 것은 무엇인가요?</p><p class="quiz-a">넘긴 글 한 줄로 된 메시지 하나와, 바깥 상태 칸 <code>files</code>의 메모 파일을 받았습니다. 바깥으로는 마지막 글인 한도 글 하나를 담은 도구 메시지가 왔습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/deepagents/subagents">Subagents in Deep Agents</a></div>확인 2026-09-28 · 명세에 도구를 적지 않으면 바깥 도구를 물려받고, 적으면 그 목록이 대신한다고 적습니다. 권한과 <code>interrupt_on</code>은 물려받고 스킬은 물려받지 않는다고 적습니다. 바깥 에이전트는 마지막 결과만 받는다고 적습니다. 기본 general-purpose 서브에이전트는 저절로 붙고, 같은 이름 명세로 바꾼다고 적습니다. 명세 키 <code>mode</code>는 설치판 0.7.0에 없습니다.</li><li>설치판 deepagents 0.7.0 소스 <code>middleware/subagents.py</code> 252~256행은 서브에이전트에 넘기지 않는 칸입니다. 464~468행이 <code>task</code> 설명 글의 「- 이름: 설명」 줄, 474~512행이 도구 메시지와 칸 갱신입니다. 537~539행이 넘긴 글 한 줄로 시작하는 자리, 556~567행이 서브에이전트를 실행하는 자리입니다.</li><li>설치판 소스 <code>graph.py</code> 657행은 명세에 모델이 없을 때 바깥 모델을 쓰는 자리입니다. 664·720·728행이 권한·<code>interrupt_on</code>·도구를 물려받는 자리입니다. 666~674행은 서브에이전트의 기본 미들웨어입니다. 777행은 기본 general-purpose가 바깥 미들웨어를 물려받는 조건입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_tools()
    check_same_as_prev()
    check_same_as_probe()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "harness_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 06절은 도구 파일에 함수를 더하지 않아 도구 파일을 쓰지 않습니다(02절 판 그대로 — 위 check_tools가 확인)
        path = write_notebook(LAB, "06", SLUG, "experiment", cells())
        print("wrote", path)
