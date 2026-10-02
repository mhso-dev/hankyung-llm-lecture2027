"""Ch 21 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_04.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_04.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**(chapter.json).

## 결정 1 — 0.x 판은 실행하지 않고, 1.x에 남은 옛 함수로 그래프 모양만 견준다 (챕터 리드 결정)

실습 폴더 잠금(uv.lock)에 langgraph 0.x가 없다. 설치판 langgraph-prebuilt 1.1.0에 사용 중단 경고와 함께 남은
`create_react_agent`로 모델 없이 그래프를 만들어, 새 함수 `create_agent`와 노드·엣지·조건 함수·상태 칸·입력 칸을 견준다.
그래프를 만들기만 하고 invoke하지 않으므로 **모델 요청 0번**(새 API 실행은 01~03이 이미 보임) — 흔들림 확인 대상 없음.
모델 객체는 키가 있어야 만들어지므로(가짜 키 없이 만들면 OpenAIError — probe/check04_graph_shapes.py) 키·모델 셀은 둔다.

## 결정 2 — 경고는 목록에 모아 필요한 값만 출력한다

옛 함수의 사용 중단 경고를 그대로 두면 셀 출력(stderr)에 실행한 컴퓨터의 임시 파일 위치가 찍힌다
(노트북 밖 확인 — probe/check04_warning_stderr.py). 새 커널 두 번의 출력이 같도록 `warnings.catch_warnings(record=True)`로 모은다.
`with`는 Ch 2 05절에서 파일을 열 때 쓴 문법이다.

## 결정 3 — 대응표는 출력으로 확인한 줄만 (챕터 리드 결정)

인자 이름은 `inspect.signature(...).parameters`로 모은 목록에서 **견줄 이름 여덟만** 있는지 출력한다(긴 서명 출력은 뺌).
옛 대응표 셋째 줄 「response_format 별도 후처리」는 사실과 달라, 「옛 함수는 루프 뒤 노드 generate_structured_response를 더함」으로 고친다.
넷째 줄 「Pydantic 사용자 상태 → TypedDict」는 공식 옮기기 안내에만 있고 노트북에서 실행하지 않아 대응표에서 뺐다(b7에 한 줄).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·세미콜론·
`isinstance`·별표 풀기·`try`·`@dataclass`·`draw_mermaid_png`·`stream`·`perf_counter`·`invoke`(모델 요청 0).
"""
from __future__ import annotations

import ast
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import KEY, RUN_DATE, code, install_source, md, model_source, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch21-create-agent/notebooks"
FIGS = ROOT / "textbook/part6/ch21-create-agent/figures"
UPGRADE = ROOT / "textbook/part6/ch21-create-agent/qa/upgrade"
SLUG = "04-0x에서-1x로-마이그레이션"
TITLE_TEXT = "0.x에서 1.x로 마이그레이션"
SRC = ROOT / "textbook/part6/ch21-create-agent/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR04_RUNSEC", "5초 안에")

INSTALL = install_source([
    "langchain==1.4.0", "langchain-core==1.6.2", "langchain-openai==1.6.0", "langgraph==1.2.11",
    "langgraph-prebuilt==1.1.0", "numpy==2.5.3", "pydantic==2.13.5", "python-dotenv==1.2.3",
])

IMPORTS = r'''# 두 함수와, 인자 목록을 읽을 모듈·경고를 모을 모듈, 01·02절에서 쓴 이름을 가져옵니다
import inspect
import warnings
from typing import Literal

from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

# 앞에서 배운 함수는 도구 파일에서 가져옵니다
from runner_tools import print_branches

print("이 절에서 새로 가져온 이름:", "inspect", "warnings", "create_react_agent")'''

MODEL = model_source("openai:gpt-5.4-mini")

# 01절 셀과 글자까지 같은 두 셀, 02절 셀과 글자까지 같은 한 셀(check_same_as_before()가 대조)
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

DEF_FORM = r'''# 답을 담을 양식 클래스를 적습니다(칸 둘: 주제어와 한 문장 답)
class PolicyAnswer(BaseModel):
    # 주제어 칸에는 괄호 안 세 값 가운데 하나만 적을 수 있습니다(Ch 19 02절 Literal)
    topic: Literal["대출", "운영", "연체"] = Field(description="답의 근거가 된 규정의 주제어")
    answer: str = Field(description="찾은 규정 글에 근거한 한 문장 답")'''

PARAMS = r'''# 두 함수가 받는 인자 이름을 목록으로 모읍니다(inspect.signature는 함수의 인자 목록을 담은 객체를 내놓음)
old_signature = inspect.signature(create_react_agent)
old_params = list(old_signature.parameters)
new_signature = inspect.signature(create_agent)
new_params = list(new_signature.parameters)
# 목록의 앞 두 자리는 이름 없이 차례로 넘기는 인자입니다
print("옛 함수의 처음 두 인자:", old_params[0:2])
print("새 함수의 처음 두 인자:", new_params[0:2])'''

PARAM_CHECK = r'''# 이 절에서 견줄 인자 이름마다, 두 함수가 그 인자를 받는지 봅니다
check_names = [
    "prompt", "system_prompt", "pre_model_hook", "post_model_hook",
    "middleware", "response_format", "state_schema", "context_schema",
]
for name in check_names:
    print(name, "| 옛 함수:", name in old_params, "| 새 함수:", name in new_params)'''

OLD_BUILD = r'''# 옛 함수로 01절과 같은 에이전트 그래프를 만들고, 그동안 나온 경고를 목록에 모읍니다(요청은 보내지 않음)
system_text = "교육센터 자료실 안내 도우미입니다. 자료실 규정을 묻는 질문에는 lookup_policy 도구로 찾은 규정 글에 근거해 답하세요."
with warnings.catch_warnings(record=True) as old_warnings:
    # 이 블록 안에서는 같은 경고도 빠짐없이 목록에 모읍니다
    warnings.simplefilter("always")
    # 옛 함수는 시스템 메시지 글을 인자 prompt로 받습니다
    old_agent = create_react_agent(model, tools=[lookup_policy], prompt=system_text)
print("만든 것의 종류:", type(old_agent).__name__)
print("받은 경고 수:", len(old_warnings))'''

WARN = r'''# 모은 경고의 종류와 글을 봅니다(경고 하나에 종류 category와 글 message가 들어 있음)
first_warning = old_warnings[0]
print("경고 종류:", first_warning.category.__name__)
print("사용 중단 경고의 한 종류인가:", issubclass(first_warning.category, DeprecationWarning))
print("경고 글:")
print(first_warning.message)'''

NEW_BUILD = r'''# 새 함수로 같은 에이전트 그래프를 만들고, 여기서도 경고를 모읍니다(요청은 보내지 않음)
with warnings.catch_warnings(record=True) as new_warnings:
    warnings.simplefilter("always")
    # 새 함수는 같은 시스템 메시지 글을 인자 system_prompt로 받습니다
    new_agent = create_agent(model, tools=[lookup_policy], system_prompt=system_text)
print("만든 것의 종류:", type(new_agent).__name__)
print("받은 경고 수:", len(new_warnings))'''

NODES = r'''# 두 그래프의 설계 객체에서 등록된 노드를 봅니다(01절 5절 builder.nodes)
old_nodes = list(old_agent.builder.nodes)
new_nodes = list(new_agent.builder.nodes)
print("옛 그래프의 노드:", old_nodes)
print("새 그래프의 노드:", new_nodes)'''

DEF_ARROWS = r'''# 에이전트 그래프 하나의 구조 문자열에서 화살표가 든 줄만 골라 출력합니다(내놓는 값 없음)
def print_arrow_lines(graph_agent):
    structure_text = graph_agent.get_graph().draw_mermaid()
    for line in structure_text.splitlines():
        # 실선 화살표나 점선 화살표가 든 줄이 엣지이고, 나머지는 상자와 꾸밈 줄입니다
        if "-->" in line or "-.->" in line:
            print(line.strip())'''

ARROWS = r'''# 두 그래프의 화살표 줄을 차례로 봅니다
print("옛 그래프의 화살표 줄:")
print_arrow_lines(old_agent)
print("새 그래프의 화살표 줄:")
print_arrow_lines(new_agent)'''

EDGES = r'''# 고정 엣지로 적힌 수와 조건 함수를 봅니다(조건 함수는 02절 함수 print_branches — 도구 파일)
print("옛 그래프의 고정 엣지 수:", len(old_agent.builder.edges))
print_branches(old_agent)
print("새 그래프의 고정 엣지 수:", len(new_agent.builder.edges))
print_branches(new_agent)'''

CHANNELS = r'''# 두 그래프의 상태 칸과, 그래프가 실행하면서 스스로 채우는 값(속성 managed)을 봅니다
print("옛 그래프의 상태 칸:", list(old_agent.builder.channels))
print("옛 그래프가 채우는 값:", list(old_agent.builder.managed))
print("새 그래프의 상태 칸:", list(new_agent.builder.channels))
print("새 그래프가 채우는 값:", list(new_agent.builder.managed))'''

INPUTS = r'''# 두 그래프가 입력으로 받는 칸을, 입력 형식의 JSON 모양 설명에서 봅니다
old_input = old_agent.get_input_jsonschema()
old_input_names = list(old_input["properties"].keys())
print("옛 그래프의 입력 칸:", old_input_names)
new_input = new_agent.get_input_jsonschema()
new_input_names = list(new_input["properties"].keys())
print("새 그래프의 입력 칸:", new_input_names)'''

OLD_FORM = r'''# 바꿀 값: 옛 함수에 3절 양식 클래스를 인자 response_format으로 더 넘깁니다(나머지 인자는 5절과 같음)
with warnings.catch_warnings(record=True) as form_warnings:
    warnings.simplefilter("always")
    old_form_agent = create_react_agent(
        model,
        tools=[lookup_policy],
        prompt=system_text,
        response_format=PolicyAnswer,
    )
print("받은 경고 수:", len(form_warnings))'''

NEW_FORM = r'''# 새 함수에도 같은 양식 클래스를 넘깁니다(02절 11절 값 바꿔 보기와 인자가 같은 줄)
new_form_agent = create_agent(
    model,
    tools=[lookup_policy],
    system_prompt=system_text,
    response_format=PolicyAnswer,
)
print("만든 것의 종류:", type(new_form_agent).__name__)'''

FORM_NODES = r'''# 양식을 넘긴 두 그래프의 노드와 고정 엣지 수를 봅니다
old_form_nodes = list(old_form_agent.builder.nodes)
new_form_nodes = list(new_form_agent.builder.nodes)
print("옛 그래프의 노드:", old_form_nodes, "| 고정 엣지 수:", len(old_form_agent.builder.edges))
print("새 그래프의 노드:", new_form_nodes, "| 고정 엣지 수:", len(new_form_agent.builder.edges))
# 노드 목록은 함수가 정하는 값이라, 실행마다 같아야 합니다
assert "generate_structured_response" in old_form_nodes, "옛 그래프에는 양식 노드가 더해져야 합니다"
assert "generate_structured_response" not in new_form_nodes, "새 그래프에는 양식 노드가 없어야 합니다"'''

FORM_ARROWS = r'''# 양식을 넘긴 두 그래프의 화살표 줄을 봅니다
print("옛 그래프의 화살표 줄:")
print_arrow_lines(old_form_agent)
print("새 그래프의 화살표 줄:")
print_arrow_lines(new_form_agent)'''

FORM_BRANCHES = r'''# 양식을 넘긴 두 그래프의 조건 함수와 갈 수 있는 곳을 봅니다
print("옛 그래프:")
print_branches(old_form_agent)
print("새 그래프:")
print_branches(new_form_agent)'''

FORM_CHANNELS = r'''# 양식을 넘긴 두 그래프의 상태 칸과 입력 칸을 봅니다
print("옛 그래프의 상태 칸:", list(old_form_agent.builder.channels))
print("새 그래프의 상태 칸:", list(new_form_agent.builder.channels))
old_form_input = old_form_agent.get_input_jsonschema()
new_form_input = new_form_agent.get_input_jsonschema()
old_form_input_names = list(old_form_input["properties"].keys())
new_form_input_names = list(new_form_input["properties"].keys())
print("옛 그래프의 입력 칸:", old_form_input_names)
print("새 그래프의 입력 칸:", new_form_input_names)'''


def string_constants(path: Path) -> dict:
    """생성기 파일에서 글 상수(이름 = r'''…''')를 모읍니다."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            found[node.targets[0].id] = node.value.value
    return found


def system_line(source: str) -> str:
    for line in source.splitlines():
        if line.startswith("system_text = "):
            return line
    return ""


def check_same_as_before() -> None:
    """01·02절 생성기의 같은 셀·함수와 대조합니다(「글자까지 같은 코드」는 이 대조가 근거)."""
    ch01 = string_constants(UPGRADE / "author_01.py")
    ch02 = string_constants(UPGRADE / "author_02.py")
    for name in ["POLICY_DATA", "DEF_TOOL"]:
        assert globals()[name] == ch01[name], name + " 셀이 01절과 다릅니다"
    assert DEF_FORM == ch02["DEF_FORM"], "DEF_FORM 셀이 02절과 다릅니다"
    # 시스템 메시지 글은 01절 4절 글과 한 줄 통째로 같습니다
    assert system_line(OLD_BUILD) == system_line(ch01["AGENT"]), "시스템 메시지 글이 01절과 다릅니다"
    tools_tree = ast.parse((LAB / "runner_tools.py").read_text(encoding="utf-8"))
    moved = {}
    for node in tools_tree.body:
        if isinstance(node, ast.FunctionDef):
            moved[node.name] = ast.dump(node)
    assert moved["print_branches"] == ast.dump(ast.parse(ch02["DEF_BRANCHES"]).body[0]), "print_branches가 02절과 다릅니다"


FIG1 = "04-1-두-함수가-만든-그래프"
FIG1_ALT = os.environ.get("AUTHOR04_FIG1_ALT", "위아래 칸 둘이 있는 그림으로 위 칸 옛 함수 create_react_agent 인자 prompt에는 회색 상자 agent와 tools와 끝점 __end__가 있고 agent에서 tools와 __end__로 should_continue 점선이, tools에서 agent로 고정 엣지 실선이 갑니다. 노란 상자에는 받은 경고 하나 고정 엣지 둘 시작점 엣지 포함이 적혀 있습니다. 아래 칸 새 함수 create_agent 인자 system_prompt에는 회색 상자 model과 tools와 __end__가 있고 model에서 tools와 __end__로 model_to_tools 점선이, tools에서 model로 tools_to_model 점선이 갑니다. 노란 상자에는 받은 경고 없음 고정 엣지 하나 시작점 엣지가 적혀 있는 그림")
FIG1_CAP = "같은 모델·도구·시스템 메시지 글로 만들어도, 옛 그래프는 되돌아가는 엣지가 실선이고 새 그래프는 점선입니다."
FIG1_READ = """위 칸이 옛 함수, 아래 칸이 새 함수가 만든 그래프입니다.
회색 상자는 라이브러리가 만든 노드이고, 노란 상자는 노트북 5·6절에서 출력한 값입니다.
가상 시작점은 두 그래프 모두 첫 노드로 가는 실선 하나라 그리지 않았습니다.
두 칸의 차이는 모델 노드 이름과, tools에서 돌아오는 화살표의 모양입니다."""

FIG2 = "04-2-인자-이름이-바뀐-자리"
FIG2_ALT = os.environ.get("AUTHOR04_FIG2_ALT", "맨 위 초록 상자 같은 시스템 메시지 글 system_text에서 칸 둘로 화살표가 갑니다. 왼쪽 칸 옛 함수 create_react_agent에는 파란 상자 prompt=system_text와 노란 상자 견준 여덟 가운데 옛 함수에만 있는 인자 prompt pre_model_hook post_model_hook이 있습니다. 오른쪽 칸 새 함수 create_agent에는 파란 상자 system_prompt=system_text와 노란 상자 견준 여덟 가운데 새 함수에만 있는 인자 system_prompt middleware가 있습니다. 맨 아래 회색 상자에는 견준 여덟 가운데 두 함수 모두 받는 인자 response_format state_schema context_schema가 적힌 그림")
FIG2_CAP = "같은 시스템 메시지 글을 옛 함수는 인자 prompt로, 새 함수는 system_prompt로 받습니다."
FIG2_READ = """맨 위 초록 상자는 두 함수에 똑같이 넘긴 값입니다.
파란 상자는 노트북 5절에서 우리가 적은 인자이고, 노란 상자는 노트북 4절에서 견준 이름 여덟 가운데 한쪽에만 있던 것입니다.
맨 아래 회색 상자는 두 칸 출력에서 모두 True였던 인자입니다.
노란 상자끼리는 이름이 다른 자리이고, 짝을 지은 것은 공식 옮기기 안내입니다."""

FIG3 = "04-3-상태-칸과-입력-칸"
FIG3_ALT = os.environ.get("AUTHOR04_FIG3_ALT", "위아래 칸 둘이 있는 그림으로 위 칸 옛 그래프 old_agent에는 노란 상자 상태 칸 messages, 노란 상자 그래프가 채우는 값 remaining_steps, 노란 상자 입력 칸 messages remaining_steps가 위에서 아래로 놓이고, 회색 상자 소스 확인 남은 단계가 둘보다 적은데 도구 요청이 오면 멈추는 글을 남김이 붙어 있습니다. 아래 칸 새 그래프 new_agent에는 노란 상자 상태 칸 messages jump_to structured_response, 노란 상자 그래프가 채우는 값 없음, 노란 상자 입력 칸 messages가 놓인 그림")
FIG3_CAP = "옛 그래프만 그래프가 스스로 채우는 값 remaining_steps를 가지고, 그 이름이 입력 칸에도 보입니다."
FIG3_READ = """위 칸이 옛 그래프, 아래 칸이 새 그래프입니다.
노란 상자는 노트북 7절 출력이고, 한 칸 안의 상자끼리는 화살표로 잇지 않았습니다.
위 칸 회색 상자는 설치판 소스로만 본 동작이고, 노트북에서 실행하지 않았습니다.
두 칸 모두 맨 아래 상자가 입력 칸입니다."""

FIG4 = "04-4-양식을-넘긴-두-그래프"
FIG4_ALT = os.environ.get("AUTHOR04_FIG4_ALT", "위아래 칸 둘이 있는 그림으로 위 칸 옛 함수 양식 PolicyAnswer를 넘김에는 회색 상자 agent tools generate_structured_response 끝점 __end__가 있습니다. agent에서 tools와 generate_structured_response로 should_continue 점선이 가고, tools에서 agent로 실선, generate_structured_response에서 __end__로 실선이 갑니다. 그 옆 회색 상자 소스 확인 루프가 끝난 뒤 모델에게 한 번 더 요청 이번에 실행 안 함이 붙어 있습니다. 아래 칸 새 함수 같은 양식을 넘김에는 회색 상자 model tools __end__가 있고, model에서 tools와 __end__와 model 자신으로, tools에서 model과 __end__로 점선이 가는 그림")
FIG4_CAP = "양식을 넘기면 옛 그래프에는 끝나기 전에 거치는 노드가 더해지고, 새 그래프는 노드가 그대로이고 갈래만 늘어납니다."
FIG4_READ = """위 칸이 옛 그래프, 아래 칸이 새 그래프이고, 두 칸 모두 8절 값 바꿔 보기의 출력입니다.
회색 상자는 라이브러리가 만든 노드이고, 가상 시작점은 그리지 않았습니다.
위 칸 오른쪽 회색 상자만 설치판 소스로 본 동작이라, 화살표로 잇지 않았습니다.
아래 칸 모델 노드의 자기 자신으로 가는 점선은 라벨을 빼고 그렸습니다."""

ILLU = "04-5-같은-빨래를-하는-옛-세탁기와-새-세탁기"
ILLU_ALT = os.environ.get("AUTHOR04_ILLU_ALT", "옅은 베이지 벽과 회색 바닥이 보이는 방을 그린 그림입니다. 왼쪽에 연녹색 위 뚜껑형 세탁기 한 대가 서 있고, 그 오른쪽 옆에 짧은 관 하나로 이어진 작은 회색 상자 하나가 붙어 있습니다. 오른쪽에는 흰 앞문형 세탁기 한 대가 떨어져 서 있고, 윗면 오른쪽에 둥근 버튼 하나, 앞면에 둥근 유리문 하나가 있으며 옆에 붙은 것은 없습니다. 두 세탁기 앞 바닥에는 똑같이 개어진 연노랑 수건이 한 장씩 놓인 그림")
ILLU_CAP = os.environ.get("AUTHOR04_ILLU_CAP", "두 세탁기는 같은 수건을 빨지만, 옛 세탁기에만 빨래가 끝난 뒤 한 번 더 거치는 칸이 옆에 붙어 있습니다.")
ILLU_READ = os.environ.get("AUTHOR04_ILLU_READ", "왼쪽 연녹색 세탁기는 위 뚜껑형이고, 오른쪽 옆에 짧은 관 하나로 이어진 작은 회색 상자 하나가 붙어 있습니다. 오른쪽 흰 세탁기에는 윗면 오른쪽 둥근 버튼 하나와 앞면 둥근 유리문 하나가 있고, 옆에 붙은 것이 없습니다. 두 기계 앞에는 똑같이 개어진 연노랑 수건이 한 장씩 놓여 있습니다. 옛 기계에만 붙은 회색 상자가, 양식을 넘겼을 때 옛 그래프에만 더해지는 노드 <code>generate_structured_response</code>입니다. 흰 세탁기 윗면 왼쪽의 가로로 긴 칸 모양과 연녹색 세탁기 윗면의 작은 단추는 코드의 무엇과도 짝짓지 않습니다.")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 옛 판의 에이전트 함수 `create_react_agent`와 지금 판 `create_agent`가 받는 인자 이름을 견줍니다.
2. 같은 모델·도구·시스템 메시지 글로 두 함수가 만든 그래프의 노드·엣지·칸을 견줍니다.
3. 양식 클래스를 더 넘겨, 옛 함수의 그래프에만 더해지는 노드를 봅니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
키는 모델 객체를 만들 때 읽습니다.
이 노트북은 그래프를 만들기만 하고 실행하지 않아, 모델 요청을 한 번도 보내지 않습니다.
그래서 요금표로 어림한 예상 비용도 0달러입니다.
도구도 실행하지 않고, 자료 파일을 읽거나 새로 쓰지 않습니다.

앞에서 배운 함수 하나는 도구 파일 `runner_tools.py`에서 가져옵니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.
설치 셀에 걸리는 시간은 네트워크에 따라 달라집니다.

**0.x 판에 대해** — 0.x는 판 번호 앞자리가 0인 옛 판들이고, 1.x는 앞자리가 1인 지금 판들입니다.
실습 폴더의 잠금 파일(`uv.lock`)에는 0.x 판이 없어, 이 노트북은 0.x 판을 실행하지 않습니다.
대신 지금 판에 경고와 함께 남아 있는 옛 함수로 그래프 모양만 견줍니다.
옛 함수는 langgraph를 설치할 때 함께 들어오는 langgraph-prebuilt 1.1.0에 들어 있습니다.

**기준 버전** — 첫 셀에서 패키지 여덟을 설치합니다.
판은 langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0입니다.
langgraph 1.2.11과 langgraph-prebuilt 1.1.0도 함께 설치합니다.
numpy 2.5.3, pydantic 2.13.5, python-dotenv 1.2.3도 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~5절을 읽습니다.
두 함수가 받는 인자와, 옛 함수를 부를 때 나오는 경고를 보는 자리입니다.
6~8절은 두 그래프의 노드·엣지·칸을 견주고 값 하나를 바꿔 보는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch21-create-agent`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01~03절에서는 함수 `create_agent`로 에이전트 그래프를 만들었습니다.
이 함수가 나오기 전 판에서는 LangGraph의 함수 `create_react_agent`로 같은 일을 했습니다.
제목의 마이그레이션(migration)은 옛 판에서 쓴 코드를 새 판에서 돌도록 고쳐 쓰는 일입니다.
이 절은 두 함수로 같은 그래프를 만들어, 옮길 때 무엇을 고쳐야 하는지 출력으로 봅니다.

첫 셀은 패키지 여덟 개를 설치하고 설치된 판 번호를 출력합니다.
도구 파일이 NumPy를 쓰므로, 01절처럼 numpy도 함께 설치합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`·`langchain-core: 1.6.2`·`langchain-openai: 1.6.0`이 보입니다.
출력 줄 `langgraph: 1.2.11`·`langgraph-prebuilt: 1.1.0`도 잠금과 같은 판입니다.
출력 줄 `numpy: 2.5.3`·`pydantic: 2.13.5`·`python-dotenv: 1.2.3`도 같습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `inspect`와 `warnings`는 Python에 들어 있는 기능 묶음입니다.
모듈 `inspect`로 함수가 받는 인자 이름을 읽고, `warnings`로 경고를 모읍니다.
함수 `create_react_agent`는 모듈 `langgraph.prebuilt`에서 가져오는 옛 함수입니다.
양식 클래스를 적을 이름 `BaseModel`·`Field`·`Literal`은 02절과 같습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 절에서 새로 가져온 이름: inspect warnings create_react_agent`가 보입니다.
옛 함수를 가져오는 줄에서는 경고가 나오지 않았습니다.

앞에서 배운 함수는 `runner_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

함수 `print_branches`는 02절 6절에서 처음 적고, 03절부터 도구 파일에서 가져오는 함수입니다.
이 절에서는 도구 파일에서 이 함수 하나만 가져옵니다.

## 2. 키와 모델 준비

모델 객체는 01절과 같은 `gpt-5.4-mini`를 과정의 같은 설정으로 만듭니다.
이 절은 모델 객체를 두 함수에 넘겨 그래프를 만들기만 하고, 모델에게 요청을 보내지 않습니다.
그래도 모델 객체를 만들 때 키가 있어야 해서 키 셀을 둡니다.

API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."""),
        setup(KEY),
        md("""실습에 쓸 모델 객체를 준비합니다.
설정은 01절과 같지만, 이 절에서는 요청을 보내지 않아 답 글이 나오지 않습니다."""),
        code(MODEL),
        md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 실행한 결과이고, 이 모델에게 보낸 요청은 없습니다.

## 3. 규정 자료, 도구, 양식 클래스

두 함수에 같은 재료를 넘기려고, 01절의 규정 딕셔너리와 도구를 다시 만듭니다.
다음 셀은 01절 3절 셀과 글자까지 같은 코드입니다."""),
        code(POLICY_DATA),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '운영', '연체']`로 키 셋을 확인합니다.
이 절에서는 도구를 실행하지 않지만, 01절과 같은 도구를 만들려고 이 딕셔너리를 둡니다.

다음 셀도 01절 3절의 도구 셀과 글자까지 같은 코드입니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 이름은 `lookup_policy`이고, 5절에서 두 함수에 이 도구 하나를 똑같이 넘깁니다.

다음 셀은 02절 4절의 양식 클래스 셀과 글자까지 같은 코드입니다.
8절 값 바꿔 보기에서 두 함수에 이 양식 클래스를 넘깁니다."""),
        code(DEF_FORM),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
양식 클래스 `PolicyAnswer`의 칸은 `topic`과 `answer` 둘입니다.

## 4. 두 함수가 받는 인자 이름

옛 판 코드를 옮길 때 먼저 보이는 차이는 인자 이름입니다.
함수 `inspect.signature`는 함수 하나를 받아, 그 함수가 받는 인자 목록을 담은 객체를 내놓습니다.
그 객체의 속성 `parameters`를 목록으로 바꾸면 인자 이름만 남습니다.
다음 셀은 두 함수의 인자 이름을 목록으로 모으고, 앞 두 자리를 봅니다."""),
        code(PARAMS),
        md("""**결과 읽기** — 출력 줄 `옛 함수의 처음 두 인자: ['model', 'tools']`와 `새 함수의 처음 두 인자: ['model', 'tools']`입니다.
두 함수 모두 모델과 도구 목록을 앞 두 자리로 받습니다.
그래서 모델 객체와 도구 목록을 넘기는 부분은 옮길 때 그대로 둘 수 있습니다.

다음 셀은 이 절에서 견줄 인자 이름 여덟을 두 목록에서 찾아봅니다.
연산자 `in`은 값이 목록에 있으면 `True`, 없으면 `False`를 냅니다."""),
        code(PARAM_CHECK),
        md("""**결과 읽기** — 줄 `prompt | 옛 함수: True | 새 함수: False`와 `system_prompt | 옛 함수: False | 새 함수: True`가 짝입니다.
옛 함수는 시스템 메시지 글을 인자 `prompt`로 받았고, 새 함수는 `system_prompt`로 받습니다.
옛 함수의 `pre_model_hook`·`post_model_hook`은 새 함수에 없고, 새 함수에는 `middleware`가 있습니다.
나머지 셋 `response_format`·`state_schema`·`context_schema`는 두 함수 모두 받습니다.

이 출력이 보여 주는 것은 두 함수에 어느 인자 이름이 있는가까지입니다.
LangChain 공식 옮기기 안내는 인자 `prompt`를 `system_prompt`로 바꾸라고 적습니다.
모델 앞뒤 훅은 미들웨어로 옮기라고 적는데, 미들웨어는 Ch 22에서 배웁니다.

## 5. 옛 함수로 그래프 만들기

다음 셀은 옛 함수로 01절과 같은 에이전트 그래프를 만듭니다.
모델 객체와 도구는 같고, 01절 시스템 메시지 글은 인자 `prompt`로 넘깁니다.
옛 함수는 부를 때마다 경고를 하나 냅니다.

노트북 밖에서 확인해 보면, 이 경고는 셀 출력에 실행한 컴퓨터의 임시 파일 위치와 함께 찍혔습니다.
그래서 경고를 목록에 모았다가 필요한 값만 출력합니다.
블록 `with`는 Ch 2 05절에서 파일을 열 때 썼습니다.
여기서는 `warnings.catch_warnings(record=True)`로, 블록 안에서 나온 경고를 목록에 모읍니다."""),
        code(OLD_BUILD),
        md("""**결과 읽기** — 출력 줄 `만든 것의 종류: CompiledStateGraph`로, 01절과 같은 종류의 그래프입니다.
출력 줄 `받은 경고 수: 1`로, 옛 함수를 한 번 부르자 경고 하나가 목록에 모였습니다.
이 셀에서도 모델 요청은 나가지 않습니다.

다음 셀은 모은 경고의 종류와 글을 봅니다.
함수 `issubclass`는 앞의 클래스가 뒤의 클래스를 물려받았는지를 참·거짓으로 알려 줍니다.
클래스 `DeprecationWarning`은 곧 없앨 기능을 쓸 때 Python이 내는 경고의 종류입니다."""),
        code(WARN),
        md("""**결과 읽기** — 출력 줄 `경고 종류: LangGraphDeprecatedSinceV10`입니다.
출력 줄 `사용 중단 경고의 한 종류인가: True`로, 사용 중단 경고를 물려받은 종류입니다.
라벨 줄 `경고 글:` 아래 앞부분 `create_react_agent has been moved to`는 함수가 다른 자리로 옮겨졌다는 뜻입니다.
이어서 모듈 `langchain.agents`에서 `create_agent`를 가져오라고 알립니다.

끝 문장 `Deprecated in LangGraph V1.0 to be removed in V2.0.`은 LangGraph 1.0부터 쓰지 말라고 알린(사용 중단을 예고한) 기능이라는 뜻입니다.
경고 글에 따르면 2.0 판에서 없어질 예정입니다.
설치판 소스(`chat_agent_executor.py` 274~277행)로 보면, 함수 위에 붙은 표시가 부를 때마다 이 경고를 냅니다.

다음 셀은 새 함수로 같은 그래프를 만들고, 여기서도 경고를 모읍니다.
새 함수는 같은 시스템 메시지 글을 인자 `system_prompt`로 받습니다.
01절 4절 셀과 인자가 같은 줄이고, 만든 그래프의 이름만 `new_agent`로 바꿨습니다."""),
        code(NEW_BUILD),
        md("""**결과 읽기** — 출력 줄 `만든 것의 종류: CompiledStateGraph`로, 옛 함수와 같은 종류입니다.
출력 줄 `받은 경고 수: 0`으로, 새 함수는 경고를 내지 않았습니다.

## 6. 노드와 엣지 견주기

두 그래프는 같은 모델·도구·시스템 메시지 글로 만들었습니다.
다음 셀은 01절 5절처럼 설계 객체의 속성 `nodes`로 등록된 노드를 봅니다."""),
        code(NODES),
        md("""**결과 읽기** — 출력 줄 `옛 그래프의 노드: ['agent', 'tools']`와 `새 그래프의 노드: ['model', 'tools']`입니다.
도구 실행 노드의 이름은 `tools`로 같고, 모델 노드의 이름이 `agent`에서 `model`로 바뀌었습니다.
공식 옮기기 안내는 스트리밍으로 받는 노드 이름도 `agent`에서 `model`로 바뀌었다고 적습니다.
스트리밍은 Ch 25에서 배우고, 이번에 실행하지 않았습니다.

다음 셀은 구조 문자열에서 화살표가 든 줄만 골라 출력하는 함수를 적습니다.
01절 5절에서는 구조 문자열 전체를 출력했는데, 이번에는 그래프 넷을 견주므로 엣지 줄만 봅니다.
메서드 `splitlines`는 글을 줄마다 나눈 목록을, `strip`은 앞뒤 빈칸을 뺀 글을 내놓습니다."""),
        code(DEF_ARROWS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
구조 문자열에서 실선 화살표는 `-->`, 점선 화살표는 `-.->`로 적힙니다.

다음 셀은 이 함수로 두 그래프의 화살표 줄을 봅니다."""),
        code(ARROWS),
        md("""**결과 읽기** — 라벨 줄 `옛 그래프의 화살표 줄:` 아래 네 줄과 `새 그래프의 화살표 줄:` 아래 네 줄입니다.
되돌아가는 엣지가 옛 그래프는 실선 `tools --> agent;`, 새 그래프는 점선 `tools -.-> model;`입니다.
나머지 세 줄은 노드 이름만 다르고 화살표 모양이 같습니다.

옛 그래프의 네 줄에서 `agent`를 `model`로 바꿔 읽으면, Ch 20 01절 구조 문자열의 화살표 줄과 같습니다.
01절에서 본 것처럼 새 그래프의 되돌아가는 엣지는 조건부 엣지라 점선입니다.

다음 셀은 고정 엣지로 적힌 수와 조건 함수를 봅니다.
조건 함수는 02절 함수 `print_branches`로 봅니다."""),
        code(EDGES),
        md("""**결과 읽기** — 출력 줄 `옛 그래프의 고정 엣지 수: 2`와 `새 그래프의 고정 엣지 수: 1`입니다.
옛 그래프의 조건 함수 줄은 `agent | 조건 함수: should_continue | 갈 수 있는 곳: ['tools', '__end__']` 하나입니다.
새 그래프는 01절과 같이 `tools_to_model`과 `model_to_tools` 두 줄입니다.
옛 그래프에서 되돌아가는 엣지는 조건 함수 없이 고정 엣지로 적혀, 실선으로 그려졌습니다.

설치판 소스(`chat_agent_executor.py` 990행)에도 도구 실행 노드에서 모델 노드로 가는 고정 엣지를 적는 줄이 있습니다.
옛 그래프의 고정 엣지 둘은 가상 시작점에서 오는 엣지와 이 되돌아가는 엣지입니다.

## 7. 상태 칸과 입력 칸 견주기

다음 셀은 두 그래프의 상태 칸을 봅니다.
속성 `managed`에는 그래프가 실행하면서 스스로 채우는 값의 이름이 들어 있습니다."""),
        code(CHANNELS),
        md("""**결과 읽기** — 출력 줄 `옛 그래프의 상태 칸: ['messages']`와 `옛 그래프가 채우는 값: ['remaining_steps']`입니다.
출력 줄 `새 그래프의 상태 칸: ['messages', 'jump_to', 'structured_response']`는 01절 5절과 같습니다.
새 그래프가 채우는 값은 빈 목록 `[]`입니다.
옛 그래프의 상태 칸은 메시지 칸 하나이고, 새 그래프에는 03절에서 본 라이브러리 상태 형식의 칸 셋이 있습니다.

설치판 소스(`chat_agent_executor.py` 57~62행)로 보면, 옛 상태 형식에 `remaining_steps`가 적혀 있습니다.
이 값은 Ch 20 03절의 실행 한도까지 남은 단계 수이고, 그래프가 단계마다 채웁니다.
같은 소스 620~633행을 보면, 옛 모델 노드가 이 값을 읽습니다.
남은 단계가 둘보다 적은데 도구 호출 요청이 오면, 도구로 가지 않고 멈추는 글을 남깁니다.
이 동작은 이번에 실행하지 않았습니다.

다음 셀은 두 그래프가 입력으로 받는 칸을 봅니다.
메서드 `get_input_jsonschema`는 그래프의 입력 형식을 JSON 모양 설명으로 내놓습니다.
02절 4절 `model_json_schema`처럼, 칸 이름은 키 `properties` 아래에 있습니다."""),
        code(INPUTS),
        md("""**결과 읽기** — 출력 줄 `옛 그래프의 입력 칸: ['messages', 'remaining_steps']`입니다.
출력 줄 `새 그래프의 입력 칸: ['messages']`로, 새 그래프는 메시지 칸만 입력으로 받습니다.
옛 그래프에서는 상태 칸 목록에 없던 `remaining_steps`가 입력 칸에는 나타났습니다.
01절에서 본 것처럼 새 그래프의 `jump_to`는 비공개 칸이고, `structured_response`는 결과를 담는 칸입니다.

## 8. 값 바꿔 보기 · 양식 클래스를 더 넘기기

바꿀 값은 두 함수의 인자 `response_format` 하나입니다.
3절의 양식 클래스 `PolicyAnswer`를 두 함수에 똑같이 넘기고, 나머지 인자는 5절과 같습니다.
실행 전에 예상해 봅니다.
새 그래프는 02절 11절처럼 노드는 그대로이고 갈 수 있는 곳만 늘 것입니다.
옛 그래프가 어떻게 바뀌는지는 노드 목록부터 봅니다."""),
        code(OLD_FORM),
        md("""**결과 읽기** — 출력 줄 `받은 경고 수: 1`로, 옛 함수를 다시 부르자 경고가 또 하나 모였습니다.
이 경고의 글은 다시 출력하지 않았습니다.

다음 셀은 새 함수에 같은 양식 클래스를 넘깁니다.
02절 11절 값 바꿔 보기와 인자가 같은 줄입니다."""),
        code(NEW_FORM),
        md("""**결과 읽기** — 출력 줄 `만든 것의 종류: CompiledStateGraph`입니다.
02절에서 본 것처럼, 양식 클래스를 그대로 넘기면 요청할 때 두 전략 가운데 하나를 고릅니다.

다음 셀은 양식을 넘긴 두 그래프의 노드와 고정 엣지 수를 봅니다.
셀 끝 `assert`는 함수가 정하는 노드 목록에만 겁니다."""),
        code(FORM_NODES),
        md("""**결과 읽기** — 출력 줄 `옛 그래프의 노드: ['agent', 'tools', 'generate_structured_response'] | 고정 엣지 수: 2`입니다.
옛 그래프에는 노드 `generate_structured_response`가 하나 더해졌고, 고정 엣지 수는 6절과 같습니다.
출력 줄 `새 그래프의 노드: ['model', 'tools'] | 고정 엣지 수: 1`로, 새 그래프는 6절과 같습니다.

다음 셀은 두 그래프의 화살표 줄을 봅니다."""),
        code(FORM_ARROWS),
        md("""**결과 읽기** — 라벨 줄 `옛 그래프의 화살표 줄:` 아래 다섯 줄에서 끝으로 가는 자리가 바뀌었습니다.
줄 `agent -.-> generate_structured_response;`가 생기고, 모델 노드에서 끝으로 바로 가는 줄은 없어졌습니다.
줄 `generate_structured_response --> __end__;`는 실선이지만, 고정 엣지 수는 늘지 않았습니다.
설치판 소스(`chat_agent_executor.py` 900~915행)에는 이 노드에서 나가는 엣지를 적는 줄이 없습니다.
나가는 엣지가 없어 이 노드에서 흐름이 끝나는 자리를 실선으로 그린 것으로 보입니다.

라벨 줄 `새 그래프의 화살표 줄:` 아래 여섯 줄에는 `tools -.-> __end__;`와 `model -.-> model;`이 더해졌습니다.
두 줄 모두 점선이고, 새로 생긴 노드는 없습니다.

다음 셀은 두 그래프의 조건 함수와 갈 수 있는 곳을 봅니다."""),
        code(FORM_BRANCHES),
        md("""**결과 읽기** — 라벨 줄 `옛 그래프:` 아래 줄은 `agent | 조건 함수: should_continue | 갈 수 있는 곳: ['tools', 'generate_structured_response']`입니다.
옛 조건 함수는 도구 호출 요청이 없으면 끝이 아니라 더해진 노드로 보냅니다.
설치판 소스(`chat_agent_executor.py` 744~767행)로 보면, 이 노드는 메시지 칸을 모델에게 한 번 더 보내 양식 값을 받습니다.
루프가 끝난 뒤 모델 요청이 한 번 더 나가는 셈이지만, 이번에는 실행하지 않아 요청 수를 세지 않았습니다.

라벨 줄 `새 그래프:` 아래 두 줄은 02절 11절 출력과 같습니다.
새 함수는 02절에서 본 두 전략으로 양식을 루프 안에서 다루므로, 노드를 더하지 않고 갈래만 늘었습니다.
공식 옮기기 안내도 양식 값을 루프 안에서 만들어 비용과 걸린 시간을 줄인다고 적습니다.
이 절에서는 요청 수와 걸린 시간을 재지 않았습니다.

다음 셀은 양식을 넘긴 두 그래프의 상태 칸과 입력 칸을 봅니다."""),
        code(FORM_CHANNELS),
        md("""**결과 읽기** — 출력 줄 `옛 그래프의 상태 칸: ['messages', 'structured_response']`로, 양식 값을 담을 칸이 더해졌습니다.
출력 줄 `새 그래프의 상태 칸: ['messages', 'jump_to', 'structured_response']`는 7절과 같습니다.
출력 줄 `옛 그래프의 입력 칸: ['messages', 'remaining_steps', 'structured_response']`입니다.
출력 줄 `새 그래프의 입력 칸: ['messages']`는 7절과 같습니다.

## 9. 옛 코드에서 바꾸는 자리

앞의 출력으로 확인한 자리만 모았습니다.

- 가져오는 줄 — `from langgraph.prebuilt import create_react_agent`를 `from langchain.agents import create_agent`로 바꿉니다. 근거는 5절 경고 글입니다.
- 시스템 메시지 글 — 인자 `prompt`를 `system_prompt`로 바꿉니다. 근거는 4절 인자 줄과 5절 두 셀이고, 두 인자를 짝지은 것은 공식 옮기기 안내입니다.
- 모델 앞뒤 훅 — 인자 `pre_model_hook`·`post_model_hook`은 새 함수에 없고, `middleware`가 있습니다. 옮기는 법은 Ch 22에서 배웁니다.
- 양식 — 인자 이름 `response_format`은 그대로입니다. 옛 함수만 노드 `generate_structured_response`를 더했습니다. 근거는 8절입니다.
- 노드 이름 — 모델 노드 `agent`가 `model`로 바뀝니다. 근거는 6절입니다.
- 되돌아가는 엣지 — 고정 엣지(실선)가 조건부 엣지(점선)로 바뀝니다. 근거는 6절입니다.
- 입력 칸 — 이름 `remaining_steps`는 옛 그래프에만 있고, 새 그래프의 입력 칸은 `messages` 하나입니다. 근거는 7절입니다.

## 정리

1. 옛 함수 `create_react_agent`는 지금 판에도 남아 있지만, 부를 때마다 사용 중단 경고를 냈습니다.
2. 같은 재료로 만든 두 그래프는 모델 노드 이름, 되돌아가는 엣지의 모양, 입력 칸 `remaining_steps`가 달랐습니다.
3. 양식 클래스를 넘기자 옛 그래프에만 노드 `generate_structured_response`가 더해졌고, 새 그래프는 노드가 그대로였습니다.

05절에서는 문서를 찾는 검색을 도구로 바꿔 에이전트 그래프에 넣습니다."""),
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


L_CH02_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH13_01 = "../../part4/ch13-langgraph-basics/01-StateGraph와-노드-엣지.html"
L_CH16_03 = "../../part4/ch16-guardrails/03-히스토리-트리밍과-요약.html"
L_CH20_01 = "../../part5/ch20-tool-node/01-ToolNode와-tools-condition.html"
L_CH20_03 = "../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html"
L_CH22_01 = "../ch22-middleware/01-미들웨어와-6개-훅.html"
L_01 = "01-create-agent와-ReAct-루프.html"
L_02 = "02-구조화-출력-두-전략.html"
L_03 = "03-AgentState와-context-schema.html"
L_05 = "05-retriever를-도구로-전환.html"

SHAPE_ROWS = [
    ("옛 함수 · 양식 없음(6·7절)", "<code>agent</code>·<code>tools</code>", "2", "<code>should_continue</code> → <code>__end__</code>",
     "<code>messages</code>", "<code>messages</code>·<code>remaining_steps</code>"),
    ("새 함수 · 양식 없음(6·7절)", "<code>model</code>·<code>tools</code>", "1", "<code>model_to_tools</code> → <code>__end__</code>",
     "<code>messages</code>·<code>jump_to</code>·<code>structured_response</code>", "<code>messages</code>"),
    ("옛 함수 · 양식 넘김(8절)", "<code>agent</code>·<code>tools</code>·<code>generate_structured_response</code>", "2",
     "<code>should_continue</code> → <code>generate_structured_response</code> → <code>__end__</code>",
     "<code>messages</code>·<code>structured_response</code>", "<code>messages</code>·<code>remaining_steps</code>·<code>structured_response</code>"),
    ("새 함수 · 양식 넘김(8절)", "<code>model</code>·<code>tools</code>", "1",
     "<code>model_to_tools</code> → <code>__end__</code> · <code>tools_to_model</code> → <code>__end__</code>",
     "<code>messages</code>·<code>jump_to</code>·<code>structured_response</code>", "<code>messages</code>"),
]

MAP_ROWS = [
    ("가져오는 줄", "<code>from langgraph.prebuilt import create_react_agent</code>", "<code>from langchain.agents import create_agent</code>", "5절 경고 글"),
    ("시스템 메시지 글", "인자 <code>prompt</code>", "인자 <code>system_prompt</code>", "4절 인자 줄 · 5절 두 셀(짝은 공식 옮기기 안내)"),
    ("모델 앞뒤 훅", "인자 <code>pre_model_hook</code>·<code>post_model_hook</code>", "없음 · 인자 <code>middleware</code>가 있음(Ch 22)", "4절 인자 줄"),
    ("양식", "<code>response_format</code> · 루프 뒤 노드 <code>generate_structured_response</code>를 더함", "<code>response_format</code> · 노드를 더하지 않음(02절 두 전략)", "8절 노드·갈 곳"),
    ("모델 노드 이름", "<code>agent</code>", "<code>model</code>", "6절 노드"),
    ("되돌아가는 엣지", "고정 엣지(실선)", "조건부 엣지(점선)", "6절 화살표 줄·고정 엣지 수"),
    ("입력 칸", "<code>messages</code>·<code>remaining_steps</code>", "<code>messages</code>", "7절 입력 칸"),
]


def table_html(head: list, rows: list) -> str:
    head_html = ""
    for value in head:
        head_html = head_html + "<th>" + value + "</th>"
    body = ""
    for row in rows:
        cells_html = ""
        for value in row:
            cells_html = cells_html + "<td>" + value + "</td>"
        body = body + "<tr>" + cells_html + "</tr>"
    return "<table><thead><tr>" + head_html + "</tr></thead><tbody>" + body + "</tbody></table>"


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def src_html() -> str:
    shape_table = table_html(["그래프", "노드", "고정 엣지 수", "끝으로 가는 갈래", "상태 칸", "입력 칸"], SHAPE_ROWS)
    map_table = table_html(["자리", "옛 함수 코드", "새 함수 코드", "노트북 근거"], MAP_ROWS)
    return """<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>옛 함수 <code>create_react_agent</code>와 새 함수 <code>create_agent</code>가 받는 인자 이름의 차이를 출력으로 확인할 수 있습니다.</li>
<li>같은 모델·도구·시스템 메시지 글로 두 함수가 만든 그래프의 노드·엣지·칸을 견줄 수 있습니다.</li>
<li>양식 클래스를 넘겼을 때 옛 그래프에만 더해지는 노드를 찾고, 옛 코드에서 바꿀 자리를 적을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a>부터 <a href=\"""" + L_03 + """\">03절</a>까지는 함수 <code>create_agent</code>로 에이전트 그래프를 만들었습니다. 이 함수가 나오기 전 판에서는 LangGraph의 함수 <code>create_react_agent</code>로 같은 일을 했습니다. 예전 판 문서와 예제 코드에는 이 함수로 쓴 코드가 있습니다.</p><p>제목의 마이그레이션(migration)은 옛 판에서 쓴 코드를 새 판에서 돌도록 고쳐 쓰는 일입니다. 함수 이름만 바꾸면 끝나는지, 다른 자리도 고쳐야 하는지 알아야 옮길 수 있습니다. 이 절은 두 함수로 같은 그래프를 만들어, 이름과 모양이 어디서 다른지 출력으로 셉니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 설계 객체 <code>agent.builder</code>로 노드·엣지·상태 칸을 보았습니다. 구조 문자열에서 되돌아가는 엣지 <code>tools -.-> model</code>이 점선이라는 것도 보았습니다. <a href=\"""" + L_02 + """\">02절</a>에서는 양식 클래스 <code>PolicyAnswer</code>를 인자 <code>response_format</code>으로 넘겼고, 조건 함수를 보는 함수 <code>print_branches</code>를 적었습니다.</p><p><a href=\"""" + L_03 + """\">03절</a>에서는 라이브러리 상태 형식 <code>AgentState</code>의 칸 셋을 보았습니다. <a href=\"""" + L_CH20_01 + """\">Ch 20 01절</a>에서는 모델 노드와 도구 실행 노드를 손으로 이었고, 되돌아가는 엣지가 실선이었습니다. <a href=\"""" + L_CH20_03 + """\">Ch 20 03절</a>에서는 그래프가 지날 수 있는 단계 수인 실행 한도를 보았습니다.</p><p>시스템 메시지 글은 <a href=\"""" + L_CH16_03 + """\">Ch 16 03절</a>에서 모델이 따를 규칙을 담은 메시지로 보았습니다. 구조 문자열은 <a href=\"""" + L_CH13_01 + """\">Ch 13 01절</a>에서 처음 보았습니다. 이 절의 블록 <code>with</code>는 <a href=\"""" + L_CH02_05 + """\">Ch 2 05절</a>에서 파일을 열 때 쓴 문법입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절에서는 에이전트 그래프를 버튼 하나로 도는 세탁기에 견주었습니다. 이번에는 옛 세탁기와 새 세탁기를 나란히 둡니다. 두 기계는 같은 수건을 빨지만, 옛 기계에는 빨래가 끝난 뒤 한 번 더 거치는 작은 칸이 옆에 붙어 있습니다. 새 기계는 그 일을 몸통 안에서 마칩니다.</p><p>옛 기계가 옛 함수 <code>create_react_agent</code>가 만든 그래프이고, 새 기계가 <code>create_agent</code>가 만든 그래프입니다. 옆에 붙은 칸은 양식을 넘겼을 때 옛 그래프에만 더해지는 노드 <code>generate_structured_response</code>입니다. 같은 수건은 두 함수에 똑같이 넘긴 모델·도구·시스템 메시지 글입니다.</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>옮기기(마이그레이션, migration)</td><td>옛 판에서 쓴 코드를 새 판에서 돌도록 고쳐 쓰는 일입니다. 쓰던 빨래 순서를 새 세탁기의 버튼 자리에 맞춰 다시 익히는 일과 같습니다. 이 절에서는 옛 함수 줄을 새 함수 줄로 바꾸고, 달라진 이름을 찾는 일입니다.</td></tr><tr><td>옛 함수(create_react_agent)</td><td>LangGraph 0.x 판에서 에이전트 그래프를 만들던 함수입니다. 지금 판에도 남아 있지만, 부를 때마다 경고를 냅니다. 비유에서 옆에 칸이 붙은 옛 세탁기와 같습니다.</td></tr><tr><td>사용 중단 경고(DeprecationWarning)</td><td>곧 없앨 기능을 쓸 때 Python이 내는 경고의 종류입니다. 가게에서 곧 팔지 않을 물건에 붙이는 「단종 예정」 안내처럼, 지금은 쓸 수 있지만 곧 없앤다는 표시입니다. 코드는 그대로 실행되고, 경고 글이 새로 쓸 이름을 알려 줍니다. 이 절에서는 옛 함수를 부를 때마다 하나씩 나왔습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 옮기기는 노트북 5절에서 옛 함수 줄 <code>create_react_agent(model, tools=[lookup_policy], prompt=system_text)</code>를 적고, 새 함수 줄로 바꿔 적는 모습입니다. 새 함수 줄은 <code>create_agent(model, tools=[lookup_policy], system_prompt=system_text)</code>입니다. 사용 중단 경고는 5절 출력 <code>경고 종류: LangGraphDeprecatedSinceV10</code>으로 보입니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
<h3>인자 이름이 바뀐 자리</h3><p>두 함수 모두 앞 두 자리로 모델과 도구 목록을 받습니다. 시스템 메시지 글을 받는 인자는 옛 함수가 <code>prompt</code>, 새 함수가 <code>system_prompt</code>입니다. 옛 함수의 모델 앞뒤 훅 인자 둘은 새 함수에 없고, 새 함수에는 인자 <code>middleware</code>가 있습니다.</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
<h3>다른 상황에 적용</h3><p>인터넷에서 찾은 예제에 <code>create_react_agent(model, tools, prompt=...)</code>가 있다면, 이 절의 순서로 옮깁니다. 가져오는 줄과 함수 이름을 바꾸고, 인자 <code>prompt</code>를 <code>system_prompt</code>로 바꿉니다. 결과에서 노드 이름 <code>agent</code>를 찾는 코드가 있다면 <code>model</code>로 고칩니다. 이 순서로 다른 예제를 옮겨 보지는 않았습니다.</p>
<h3>비교와 경계</h3><p>이 절은 0.x 판을 실행하지 않았습니다. 실습 폴더 잠금 파일에 0.x 판이 없기 때문입니다. 지금 판 langgraph-prebuilt 1.1.0에 남은 옛 함수로 그래프 모양만 보았습니다. 0.x 판에서도 모양이 같았는지는 확인하지 않았습니다.</p><p>두 함수 모두 그래프를 만들기만 하고 실행하지 않았습니다. 그래서 두 그래프가 같은 질문에 같은 답을 내는지, 모델 요청 수가 얼마인지는 이 절에서 보지 않았습니다. 새 함수의 실행은 01~03절에서 보았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 01절과 같은 규정 딕셔너리와 도구, 02절과 같은 양식 클래스를 만듭니다. 두 함수의 인자 이름을 견주고, 옛 함수와 새 함수로 같은 재료의 그래프를 하나씩 만듭니다. 두 그래프의 노드·화살표 줄·조건 함수·상태 칸·입력 칸을 차례로 출력합니다. 값 바꿔 보기로 양식 클래스를 더 넘겨 다시 봅니다.</p><p>모델 객체는 01절과 같은 <code>gpt-5.4-mini</code>를 temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 만듭니다. 그래프를 실행하지 않아 모델 요청은 0번이고, 요금표로 어림한 예상 비용도 0달러입니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — 노트북 4절에서 인자 <code>prompt</code>와 <code>system_prompt</code>가 한 함수에만 있는지 봅니다. 5절에서 옛 함수만 경고 하나를 내는지, 6절에서 노드 이름과 되돌아가는 엣지의 모양을 봅니다. 7절에서 <code>remaining_steps</code>가 옛 그래프의 입력 칸에만 있는지 확인합니다.</p>
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>값 바꿔 보기에서 바꾼 것은 두 함수의 인자 <code>response_format</code> 하나입니다. 모델 객체·도구·시스템 메시지 글은 그대로였습니다. 아래 표는 노트북 6~8절 출력을 그래프마다 한 줄로 모은 것입니다.</p>
""" + shape_table + """
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG4_READ) + """</p>
<p>양식을 넘기자 옛 그래프에만 노드 <code>generate_structured_response</code>가 더해졌습니다. 옛 조건 함수는 도구 호출 요청이 없으면 끝 대신 이 노드로 보냈습니다. 설치판 소스로 보면 이 노드는 모델에게 요청을 한 번 더 보내 양식 값을 받지만, 이번에는 실행하지 않았습니다.</p><p>새 그래프는 노드가 그대로였고, 갈 수 있는 곳만 늘었습니다. <a href=\"""" + L_02 + """\">02절</a>에서 본 두 전략이 양식을 루프 안에서 다루기 때문입니다. 공식 옮기기 안내는 이 차이로 비용과 걸린 시간이 준다고 적지만, 이 절은 요청 수와 걸린 시간을 재지 않았습니다.</p><p>아래 표는 옛 코드를 새 함수로 옮길 때 바꾸는 자리입니다. 노트북 출력으로 확인한 자리만 적었습니다.</p>
""" + map_table + """
<p>모델 요청을 보내지 않아, 노트북 출력은 새 커널로 두 번 실행해도 글자까지 같아야 합니다. """ + os.environ.get("AUTHOR04_RUNS_SENTENCE", "새 커널로 두 번 실행했을 때 모든 셀의 출력이 같았습니다.") + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>0.x 판은 실행하지 않았습니다. 실습 폴더 잠금 파일에 0.x 판이 없어, 지금 판에 남은 옛 함수로 그래프 모양만 견줬습니다.</li><li>두 함수로 만든 그래프는 어느 것도 실행하지 않았고, 모델 요청은 0번입니다. 모델 객체는 키가 있어야 만들어져서 키 셀을 두었습니다.</li><li>옛 그래프의 노드 <code>generate_structured_response</code>가 모델에게 한 번 더 요청하는 것은 설치판 소스(<code>chat_agent_executor.py</code> 744~767행)로만 확인했습니다.</li><li>옛 모델 노드가 <code>remaining_steps</code>를 읽어 멈추는 글을 남기는 동작도 소스(620~633·684~692행)로만 확인했습니다.</li><li>경고를 모으지 않으면 셀 출력에 경고 글이 임시 파일 위치와 함께 찍혔습니다. 이것은 노트북 밖에서 모델 없이 확인했습니다.</li><li>공식 옮기기 안내에는 새 함수의 상태 형식이 <code>TypedDict</code>만 받는다는 내용도 있습니다. 옛 함수의 Pydantic 상태 형식은 이 절에서 실행하지 않아 대응표에 넣지 않았습니다.</li><li>공식 옮기기 안내는 스트리밍 노드 이름이 <code>agent</code>에서 <code>model</code>로 바뀐 것과, 도구 목록에 <code>ToolNode</code>를 넘기지 못하는 것도 적습니다. 두 가지 모두 이번에 실행하지 않았습니다.</li><li>모델 앞뒤 훅을 미들웨어로 옮기는 법은 <a href=\"""" + L_CH22_01 + """\">Ch 22</a>에서 배웁니다. 이 절은 인자 이름이 있는지만 보았습니다.</li><li>화살표 줄은 구조 문자열에서 화살표가 든 줄만 골라 출력했습니다. 끝점으로 가는 실선 하나는 고정 엣지로 세어지지 않았습니다.</li><li>함수 <code>print_branches</code>는 02절 노트북의 본문을 글자 그대로 도구 파일로 옮긴 것입니다. 함수 <code>print_arrow_lines</code>는 이 절 노트북에서 처음 적었습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>옛 함수 <code>create_react_agent</code>는 지금 판에도 남아 있지만, 부를 때마다 사용 중단 경고를 냈습니다.</li><li>같은 재료로 만든 두 그래프는 모델 노드 이름, 되돌아가는 엣지의 모양, 입력 칸 <code>remaining_steps</code>가 달랐습니다.</li><li>양식 클래스를 넘기자 옛 그래프에만 노드 <code>generate_structured_response</code>가 더해졌고, 새 그래프는 노드가 그대로였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_05 + """\">05절</a>에서는 문서를 찾는 검색을 도구로 바꿔 에이전트 그래프에 넣습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 옛 함수로 쓴 코드의 인자 <code>prompt=system_text</code>는 새 함수에서 어떻게 적나요?</p><p class="quiz-a">인자 <code>system_prompt=system_text</code>로 적습니다. 노트북 4절에서 <code>prompt</code>는 옛 함수에만, <code>system_prompt</code>는 새 함수에만 있었습니다. 틀렸다면 노트북 4절과 5절을 다시 읽습니다.</p><p class="quiz-q">2. 같은 재료로 만든 두 그래프에서 도구 실행 노드에서 모델 노드로 돌아오는 엣지는 어떻게 달랐나요?</p><p class="quiz-a">옛 그래프는 고정 엣지라 실선이었고, 새 그래프는 조건부 엣지라 점선이었습니다. 옛 그래프의 고정 엣지 수는 2, 새 그래프는 1이었습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 입력 칸 <code>remaining_steps</code>는 어느 그래프에 있었고, 무엇을 담는 값인가요?</p><p class="quiz-a">옛 그래프에만 있었습니다. 실행 한도까지 남은 단계 수를 그래프가 채우는 값이고, 이 값으로 멈추는 동작은 소스로만 보았습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">4. 양식 클래스를 넘기자 두 그래프는 어떻게 달라졌나요?</p><p class="quiz-a">옛 그래프에는 노드 <code>generate_structured_response</code>가 더해졌고, 옛 조건 함수는 끝 대신 그 노드로 보냈습니다. 새 그래프는 노드가 그대로이고 갈 수 있는 곳만 늘었습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/migrate/langchain-v1">LangChain v1 migration guide</a></div>확인 2026-09-25 · 가져오는 자리, 인자 <code>system_prompt</code>, 훅과 미들웨어, 루프 안 양식 값을 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/migrate/langgraph-v1">LangGraph v1 migration guide</a></div>확인 2026-09-25 · 옛 함수 <code>create_react_agent</code>의 사용 중단을 적습니다.</li><li>langgraph-prebuilt 1.1.0 소스 <code>langgraph/prebuilt/chat_agent_executor.py</code> 274~277행 — 옛 함수의 사용 중단 표시입니다.</li><li>같은 소스 57~62행은 옛 상태 형식과 <code>remaining_steps</code>입니다.</li><li>같은 소스 620~633행과 684~692행은 남은 단계로 멈추는 자리입니다.</li><li>같은 소스 744~767행은 노드 <code>generate_structured_response</code>입니다.</li><li>같은 소스 831~841행은 조건 함수 <code>should_continue</code>, 990행은 되돌아가는 고정 엣지입니다.</li><li>langgraph 1.2.11 소스 <code>langgraph/warnings.py</code> 13·58행 — 경고 종류가 사용 중단 경고를 물려받는 자리입니다.</li><li>같은 판 <code>langgraph/managed/is_last_step.py</code> 18~21행은 남은 단계 수를 채우는 자리입니다.</li><li>langchain 1.4.0 소스 <code>langchain/agents/factory.py</code> 1687~1705행 — 새 그래프의 조건부 엣지 둘을 적는 자리입니다.</li><li>01절에서 설계 객체를, 02절에서 양식 클래스와 함수 <code>print_branches</code>를, 03절에서 상태 칸 셋을 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_same_as_before()
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "04", SLUG, "experiment", cells())
        print("wrote", path)
