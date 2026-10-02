"""Ch 22 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용: python author_upgrade.py 01   → labs/.../notebooks/01-*.ipynb 를 새로 쓴다(출력 없음).
이후 execute.py 로 실행하고 mermaid/attach_figures.py 로 그림을 첨부한다.
이전 생성기(가짜 모델 사용)는 qa/upgrade/before/ 에 보존했다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
LAB = ROOT / "labs/part6/ch22-middleware/notebooks"

INSTALL = '''# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langchain==1.4.0" "langchain-openai==1.6.0" "langgraph==1.2.11" "python-dotenv==1.2.3"
from importlib.metadata import version

print("langchain:", version("langchain"))
print("langchain-openai:", version("langchain-openai"))
print("langgraph:", version("langgraph"))'''

KEY = '''# .env 파일에서 OpenAI API 키를 읽습니다(키 값은 출력하지 않습니다)
import os
from dotenv import find_dotenv, load_dotenv

env_path = find_dotenv(usecwd=True)
load_dotenv(env_path)
has_key = os.getenv("OPENAI_API_KEY") is not None
print("OPENAI_API_KEY 설정 여부:", has_key)
assert has_key, "프로젝트 폴더의 .env 파일에 OPENAI_API_KEY를 적어 주세요."'''

MODEL = '''# 실습에 쓸 모델을 준비합니다
model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
)
print("모델 이름:", model.model_name)
print("temperature:", model.temperature)'''


def md(source: str, **metadata) -> dict:
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": source.strip("\n")}


def code(source: str, **metadata) -> dict:
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": metadata, "outputs": [], "source": source.strip("\n")}


def setup(source: str) -> dict:
    return code(source, lesson_role="setup")


def section_01() -> tuple[str, str, list[dict]]:
    cells = [
        md("""# 미들웨어와 6개 훅

**이 노트북에서 할 일**

1. 훅 여섯 개를 함수로 하나씩 만들고, 실행될 때마다 이름을 목록에 적습니다.
2. 도구가 필요한 질문으로 에이전트를 실행해 훅이 실행된 순서를 읽습니다.
3. 도구를 쓰지 말라고 적은 인사 질문으로 실행하고 훅 실행 횟수를 비교합니다.

**준비물** — `.env` 파일의 `OPENAI_API_KEY`, 데이터 파일은 없습니다. 모델 호출은 3번이고 실행 시간은 1분 이내입니다. 예상 비용은 0.01달러 미만입니다.""", html="skip"),
        md("""## 오늘 볼 그림

![훅 여섯 개가 에이전트 실행 중 놓이는 위치](attachment:01-1-훅-위치.png)

위에서 아래로 읽습니다. 파란 상자가 이번에 만들 훅입니다. 보라 상자는 모델, 초록 상자는 도구입니다.
모델이 도구를 요청하면 도구 상자를 거쳐 다시 모델 호출로 돌아갑니다.""", html="skip"),
        md("""## 1. 준비

첫 셀은 패키지를 설치하고 설치된 버전을 출력합니다. 설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""이번 절에서 쓰는 이름을 한 번에 불러옵니다. 훅을 만드는 데코레이터 여섯 개가 여기에 들어 있습니다.
함께 불러오는 `Callable`, `AgentState`, `Runtime`은 타입 힌트에 쓰는 이름입니다.
타입 힌트는 함수가 받는 값의 종류를 적어 두는 표시입니다. 이 절의 훅 함수에 붙인 타입 힌트는 실행 결과를 바꾸지 않습니다."""),
        setup('''# 에이전트·훅·모델·도구를 만드는 도구를 불러옵니다
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import AgentState, Runtime
from langchain.agents.middleware import ModelRequest, ModelResponse, ToolCallRequest
from langchain.agents.middleware import after_agent, after_model, before_agent, before_model
from langchain.agents.middleware import wrap_model_call, wrap_tool_call
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import ToolMessage'''),
        md("""API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."""),
        setup(KEY),
        md("""## 2. 모델과 도구 만들기

`init_chat_model()` 함수는 모델 이름을 받아 모델 객체를 만듭니다.
temperature 값은 답을 고를 때의 무작위 정도입니다. 0으로 두면 매번 비슷한 답을 고릅니다.
추론 설정(`reasoning_effort="none"`)은 모델이 긴 추론 없이 바로 답하게 합니다."""),
        code(MODEL),
        md("""**결과 읽기** — 모델 이름에 `gpt-5.4-mini`, temperature에 `0.0`이 보이면 준비가 끝났습니다.
temperature 값을 0으로 두어도 답 문장이 매번 똑같다고 보장하지는 않습니다.
이 노트북의 출력은 2026-09-15에 이 모델로 실행한 결과입니다."""),
        md("""에이전트가 쓸 도구를 하나 만듭니다. 도구는 모델이 필요할 때 부르는 보통의 파이썬 함수입니다.
함수 위의 `@tool` 줄은 아래 함수를 에이전트용 도구로 등록합니다.
큰따옴표 세 개로 쓴 설명문은 모델이 도구를 고를 때 읽는 안내입니다."""),
        code('''# 자료실 운영 시간을 알려 주는 도구를 만듭니다
@tool
def lookup_hours(day: str) -> str:
    """자료실 운영 시간을 조회합니다. day에는 "평일" 또는 "토요일"을 넣습니다."""
    if day == "평일":
        return "평일 09:00~20:00"
    return "토요일 10:00~17:00"


print("도구 이름:", lookup_hours.name)'''),
        md("""**결과 읽기** — 도구 이름이 `lookup_hours`로 나옵니다. 모델도 이 이름으로 도구를 부릅니다."""),
        md("""## 3. 훅 여섯 개 만들기

훅은 에이전트가 정해진 순간에 알아서 실행하는 함수입니다. 우리가 직접 부르지 않습니다.
각 훅은 실행될 때 자기 이름을 `trace` 목록에 적습니다. 먼저 빈 목록을 만듭니다."""),
        code('''# 훅이 실행된 순서를 적을 빈 목록을 만듭니다
trace = []
print("기록 개수:", len(trace))'''),
        md("""**결과 읽기** — 아직 아무 훅도 실행되지 않았으므로 기록 개수는 `0`입니다.

첫 번째 훅은 에이전트 실행이 시작될 때 한 번 실행됩니다.
`@before_agent` 줄은 아래 함수를 "시작할 때 실행할 훅"으로 등록합니다.
state 값은 지금까지의 대화 기록이고, runtime 값은 실행 환경 정보입니다. 이번에는 둘 다 쓰지 않습니다."""),
        code('''# 에이전트 실행이 시작될 때 한 번 실행되는 훅
@before_agent
def record_before_agent(state: AgentState, runtime: Runtime) -> None:
    trace.append("before_agent")'''),
        md("""출력은 없습니다. 함수를 만들기만 했고 아직 실행하지 않았기 때문입니다.

두 번째 훅은 모델을 부르기 직전마다 실행됩니다. 모델을 두 번 부르면 두 번 실행됩니다."""),
        code('''# 모델을 부르기 직전마다 실행되는 훅
@before_model
def record_before_model(state: AgentState, runtime: Runtime) -> None:
    trace.append("before_model")'''),
        md("""세 번째 훅은 모델 호출을 앞뒤로 감쌉니다. 이런 훅을 감싸기형 훅이라고 부릅니다.
`handler` 함수는 실제로 모델을 부릅니다. `handler(request)` 줄에서 모델이 실행됩니다.
그래서 이 줄 앞에 적은 기록은 모델 호출 전에, 뒤에 적은 기록은 호출 후에 남습니다."""),
        code('''# 모델 호출을 앞뒤로 감싸는 훅
@wrap_model_call
def record_wrap_model(request: ModelRequest, handler: Callable) -> ModelResponse:
    trace.append("wrap_model_call 시작")
    response = handler(request)  # 여기서 실제 모델이 실행됩니다
    trace.append("wrap_model_call 끝")
    return response'''),
        md("""네 번째 훅은 모델 응답을 받은 직후마다 실행됩니다."""),
        code('''# 모델 응답을 받은 직후마다 실행되는 훅
@after_model
def record_after_model(state: AgentState, runtime: Runtime) -> None:
    trace.append("after_model")'''),
        md("""다섯 번째 훅은 도구 호출을 앞뒤로 감쌉니다. 모양은 세 번째 훅과 같습니다.
여기서 `handler(request)`는 모델이 아니라 도구를 실행합니다."""),
        code('''# 도구 호출을 앞뒤로 감싸는 훅
@wrap_tool_call
def record_wrap_tool(request: ToolCallRequest, handler: Callable) -> ToolMessage:
    trace.append("wrap_tool_call 시작")
    result = handler(request)  # 여기서 실제 도구가 실행됩니다
    trace.append("wrap_tool_call 끝")
    return result'''),
        md("""마지막 훅은 에이전트 실행이 끝날 때 한 번 실행됩니다."""),
        code('''# 에이전트 실행이 끝날 때 한 번 실행되는 훅
@after_agent
def record_after_agent(state: AgentState, runtime: Runtime) -> None:
    trace.append("after_agent")'''),
        md("""## 4. 에이전트에 훅 등록하고 실행하기

`create_agent()` 함수의 `middleware` 인자에 훅 목록을 넘깁니다. 목록 순서는 07절에서 따로 다룹니다."""),
        code('''# 도구 1개와 훅 6개를 등록해 에이전트를 만듭니다
hooks = [
    record_before_agent,
    record_before_model,
    record_wrap_model,
    record_after_model,
    record_wrap_tool,
    record_after_agent,
]
agent = create_agent(model, tools=[lookup_hours], middleware=hooks)
print("등록한 훅 수:", len(hooks))'''),
        md("""**결과 읽기** — 등록한 훅 수가 `6`입니다.

이제 운영 시간을 묻습니다. 답하려면 도구가 필요한 질문입니다."""),
        code('''# 도구가 필요한 질문으로 에이전트를 한 번 실행합니다
question = {"messages": [{"role": "user", "content": "자료실 평일 운영 시간을 알려 주세요."}]}
result = agent.invoke(question)
last_message = result["messages"][-1]
print("최종 답:", last_message.text)'''),
        md("""**결과 읽기** — 최종 답에 `09:00~20:00`이 들어 있으면 모델이 도구 결과를 읽고 답한 것입니다.
답 문장은 실행할 때마다 조금씩 달라질 수 있습니다.

훅이 남긴 기록을 번호와 함께 출력합니다.
반복문에 쓴 `enumerate(trace, start=1)` 함수는 목록의 값마다 1부터 시작하는 번호를 붙여 줍니다."""),
        code('''# 훅이 실행된 순서를 번호와 함께 출력합니다
for number, name in enumerate(trace, start=1):
    print(number, name)'''),
        md("""**결과 읽기** — 1번은 `before_agent`, 마지막은 `after_agent`입니다.
그 사이에서 `before_model`부터 `after_model`까지 모델 호출 한 묶음이 두 번 나옵니다.
두 묶음 사이에 `wrap_tool_call 시작`과 `wrap_tool_call 끝`이 끼어 있습니다.

대화 기록에 어떤 메시지가 쌓였는지도 봅니다. 메시지 종류 중 human은 사용자, ai는 모델, tool은 도구가 만든 메시지입니다."""),
        code('''# 대화 기록에 쌓인 메시지를 종류별로 출력합니다
for message in result["messages"]:
    print(message.type, "|", message.text)'''),
        md("""**결과 읽기** — 두 번째 줄의 ai 메시지는 글자가 비어 있습니다. 이 메시지는 답 대신 도구를 요청했습니다.
그다음 tool 메시지에 `평일 09:00~20:00`이 있고, 마지막 ai 메시지가 최종 답입니다.
ai 메시지 하나가 모델 호출 한 번입니다. 이제 ai 메시지 수와 훅 기록 수를 따로 세어 비교합니다."""),
        code('''# ai 메시지 수(모델 호출 횟수)와 훅 기록 수를 따로 셉니다
ai_messages = 0
for message in result["messages"]:
    if message.type == "ai":
        ai_messages = ai_messages + 1
model_calls = trace.count("before_model")
tool_calls = trace.count("wrap_tool_call 시작")
print("ai 메시지 수(모델 호출 횟수):", ai_messages)
print("before_model 기록 수:", model_calls)
print("도구 호출 횟수:", tool_calls)'''),
        md("""**결과 읽기** — ai 메시지 수 `2`, before_model 기록 수 `2`, 도구 호출 횟수 `1`입니다.
모델을 2번 불렀고, before_model 훅도 호출마다 한 번씩 실행됐습니다.

모델 답 문장과 상관없이 늘 성립해야 하는 관계를 `assert` 줄로 확인합니다. 관계가 틀리면 오류가 납니다."""),
        code('''# 매번 같아야 하는 관계 다섯 가지를 확인합니다
assert trace[0] == "before_agent"
assert trace[-1] == "after_agent"
assert model_calls == ai_messages
assert trace.count("wrap_model_call 시작") == ai_messages
assert trace.count("after_model") == ai_messages
print("다섯 관계가 모두 맞습니다")'''),
        md("""**결과 읽기** — `다섯 관계가 모두 맞습니다`가 출력됐습니다. 모델 훅 세 개 모두 모델 호출 횟수만큼 실행됐습니다.

## 5. 질문 하나 바꿔 보기

도구를 쓰지 말라고 적은 인사 질문으로 바꿉니다. 실행 전에 예상해 봅니다.
모델이 도구를 부르지 않으면 모델 호출은 한 번이고, 도구 훅은 실행되지 않을 것입니다."""),
        code('''# 기록을 비우고, 도구를 쓰지 말라고 적은 질문으로 다시 실행합니다
trace.clear()
greeting = {"messages": [{"role": "user", "content": "도구를 쓰지 말고 한 문장으로 인사해 주세요."}]}
greeting_result = agent.invoke(greeting)
print("최종 답:", greeting_result["messages"][-1].text)
for number, name in enumerate(trace, start=1):
    print(number, name)'''),
        md("""**결과 읽기** — 기록이 `before_agent`로 시작해 `after_agent`로 끝나는 것은 앞과 같습니다.
이번에는 `wrap_tool_call 시작`이 없고 모델 호출 묶음이 한 번뿐입니다. 인사 문장은 실행할 때마다 달라질 수 있습니다."""),
        code('''# 두 질문의 호출 횟수를 비교합니다
print("인사 질문 모델 호출 횟수:", trace.count("before_model"))
print("인사 질문 도구 호출 횟수:", trace.count("wrap_tool_call 시작"))
print("운영 시간 질문 모델 호출 횟수:", model_calls)
print("운영 시간 질문 도구 호출 횟수:", tool_calls)'''),
        md("""**결과 읽기** — 인사 질문은 모델 `1`번, 도구 `0`번입니다. 운영 시간 질문은 모델 2번, 도구 1번이었습니다.
훅이 실행되는 횟수는 등록한 개수가 아니라, 에이전트가 실제로 모델과 도구를 몇 번 불렀는지에 따라 정해집니다.

## 정리

- `before_agent`와 `after_agent`는 에이전트를 한 번 실행할 때 한 번씩 실행됩니다.
- 모델 훅 세 개는 모델을 부를 때마다, `wrap_tool_call`은 도구를 부를 때마다 실행됩니다.
- 감싸기형 훅은 `handler(request)` 줄을 기준으로 호출 전과 호출 후가 나뉩니다.

다음 절에서는 이 훅 자리에 개인정보를 가리는 기능을 넣습니다."""),
    ]
    return "01-미들웨어와-6개-훅", "experiment", cells



RECORD_INPUT = """# 모델이 실제로 받은 메시지를 기록하는 훅을 만듭니다
seen_by_model = []


@wrap_model_call
def record_model_input(request: ModelRequest, handler: Callable) -> ModelResponse:
    for message in request.messages:
        seen_by_model.append(message.text)
    return handler(request)"""


def title_cells(title: str, todo: list[str], ready: str, figure: str, figure_alt: str, figure_read: str) -> list[dict]:
    steps = "\n".join(f"{number}. {item}" for number, item in enumerate(todo, start=1))
    return [
        md(f"# {title}\n\n**이 노트북에서 할 일**\n\n{steps}\n\n**준비물** — {ready}", html="skip"),
        md(f"## 오늘 볼 그림\n\n![{figure_alt}](attachment:{figure})\n\n{figure_read}", html="skip"),
        md("## 1. 준비\n\n첫 셀은 패키지를 설치하고 설치된 버전을 출력합니다. 설치에는 몇십 초가 걸릴 수 있습니다."),
        setup(INSTALL),
    ]


def key_and_model_cells() -> list[dict]:
    return [
        md("API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."),
        setup(KEY),
        md("""실습에 쓸 모델을 준비합니다. 01절과 같은 설정입니다.
temperature 값을 0으로 두어 매번 비슷한 답을 고르게 합니다."""),
        code(MODEL),
        md("**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.\n이 노트북의 출력은 2026-09-15에 이 모델로 실행한 결과입니다."),
    ]


def section_02() -> tuple[str, str, list[dict]]:
    cells = title_cells(
        "PII 마스킹 이식",
        ["Ch16 02절의 가리기 함수를 딕셔너리와 `re.compile`로 정리한 판을 실행해 봅니다.",
         "마스킹 없이 이메일이 든 질문을 보내고, 모델이 받은 글을 확인합니다(Before).",
         "이메일 마스킹 미들웨어를 등록하고 같은 질문을 보냅니다(After)."],
        "`.env` 파일의 `OPENAI_API_KEY`. 데이터 파일은 없습니다. 모델 호출은 4번이고 실행 시간은 1분 이내입니다. 예상 비용은 0.01달러 미만입니다.",
        "02-1-마스킹-위치.png", "마스킹 미들웨어가 모델 호출 앞에서 이메일을 가리는 위치",
        "위가 Before, 아래가 After입니다. After에서는 모델에 보내기 전에 마스킹 훅이 이메일을 가립니다.\n"
        "파란 상자는 질문과 거쳐 가는 단계, 빨간 상자는 원문이 간 모델 입력, 보라 상자는 가려진 모델 입력입니다.",
    )
    cells += [
        md("이번 절에서 쓰는 이름을 불러옵니다. 개인정보를 가리는 미들웨어는 `PIIMiddleware`입니다."),
        setup("""# 에이전트·미들웨어·모델을 만드는 도구를 불러옵니다
import re
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, PIIMiddleware
from langchain.agents.middleware import wrap_model_call
from langchain.chat_models import init_chat_model"""),
    ]
    cells += key_and_model_cells()
    cells += [
        md("""## 2. Ch16 마스킹 함수를 정리한 판

개인정보(PII)는 이메일이나 전화번호처럼 사람을 알아볼 수 있는 정보입니다.
Ch16 02절에서는 정규식으로 개인정보를 찾아 표식으로 바꿨습니다. 정규식은 글자의 모양을 적는 규칙입니다.
이 절은 그 가리기 함수를 딕셔너리와 `re.compile`로 정리한 판을 씁니다.

함수 `re.compile(정규식)`은 정규식 글을 미리 규칙 객체 하나로 만들어 둡니다. 그 객체의 `sub`가 맞는 부분을 바꿉니다.
전화번호·주민등록번호·카드 번호 정규식은 Ch16 02절과 같고, 이메일 정규식은 Ch16 02절과 다른 모양입니다.
먼저 찾을 모양 네 가지를 딕셔너리에 담습니다."""),
        code("""# 찾을 개인정보 모양을 이름별 정규식으로 적습니다
PII_PATTERNS = {
    "email": re.compile(r"[\\w.+-]+@[\\w-]+\\.[\\w.]+"),
    "phone": re.compile(r"01[016789]-?\\d{3,4}-?\\d{4}"),
    "rrn": re.compile(r"\\d{6}-?[1-4]\\d{6}"),
    "card": re.compile(r"\\d{4}-\\d{4}-\\d{4}-\\d{4}"),
}
print("찾을 개인정보 종류:", list(PII_PATTERNS))"""),
        md("""**결과 읽기** — 네 가지 이름 `email`, `phone`, `rrn`, `card`가 나옵니다. 이름 중 rrn은 주민등록번호, card는 카드 번호입니다.

글 하나를 받아 네 가지 모양을 차례로 표식으로 바꾸는 함수를 만듭니다.
Ch16 02절 함수와 달리 종류별 개수는 내놓지 않고 가린 글만 내놓습니다."""),
        code("""# 정규식에 맞는 부분을 <EMAIL_MASKED> 같은 표식으로 바꾸는 함수
def mask_pii(text: str) -> str:
    masked = text
    for name, pattern in PII_PATTERNS.items():
        label = "<" + name.upper() + "_MASKED>"
        masked = pattern.sub(label, masked)
    return masked"""),
        md("""출력은 없습니다. 함수를 만들기만 했습니다. 예시 글로 실행해 봅니다."""),
        code("""# 개인정보 네 가지가 든 예시 글에 함수를 적용합니다
sample = "learner@example.com 010-1234-5678 900101-1234567 1234-5678-9012-3456"
print("원문:", sample)
print("마스킹 결과:", mask_pii(sample))"""),
        md("""**결과 읽기** — 네 값이 모두 `<EMAIL_MASKED>` 같은 표식으로 바뀌었습니다.
Ch16에서는 모델을 부르기 전에 가리기 함수를 우리가 직접 호출해야 했습니다. 호출을 빠뜨리면 원문이 그대로 모델에 갑니다.

## 3. 모델이 받은 글을 기록하는 훅

이번 비교의 기준은 「모델이 실제로 무엇을 받았나」입니다. 01절의 감싸기형 훅으로 모델 입력을 기록합니다.
`request.messages`에는 이번 모델 호출에 들어가는 메시지 목록이 있습니다."""),
        code(RECORD_INPUT),
        md("""출력은 없습니다. 이 훅은 모델을 부르기 직전에 메시지 글을 `seen_by_model` 목록에 적습니다.

## 4. Before — 마스킹 없이 보내기

이메일이 든 질문을 보냅니다. 에이전트에는 기록 훅만 등록합니다.""", lesson_part="before"),
        code("""# Before: 마스킹 없이 이메일이 든 질문을 보냅니다
question = {"messages": [{"role": "user", "content": "제 이메일 learner@example.com 으로 대출 연장 안내를 보내 주세요."}]}
plain_agent = create_agent(model, tools=[], middleware=[record_model_input])
plain_result = plain_agent.invoke(question)
print("모델이 받은 글:", seen_by_model[0])""", lesson_part="before"),
        md("""**결과 읽기** — 모델이 받은 글에 이메일 `learner@example.com`이 그대로 들어 있습니다.""", lesson_part="before"),
        code("""# 모델 입력에 이메일 원문이 있었는지 참/거짓으로 확인합니다
email_sent = "learner@example.com" in seen_by_model[0]
print("모델 입력에 이메일 원문이 있나:", email_sent)
assert email_sent""", lesson_part="before"),
        md("""**결과 읽기** — `True`입니다. 개인정보가 외부 모델 서비스로 그대로 전송됐습니다.

## 5. After — 마스킹 미들웨어 등록하기

`PIIMiddleware()` 클래스로 미들웨어를 만듭니다. 첫 인자 `"email"`은 가릴 종류입니다.
인자 `strategy="mask"`는 값의 일부를 별표로 가리는 방식입니다. 인자 `apply_to_input=True`는 모델에 보내는 입력에 적용하라는 뜻입니다.

인자 `apply_to_output=True`는 모델이 만든 답에도 적용하라는 뜻입니다. 답 쪽 마스킹은 이번에 확인하지 않습니다.""", lesson_part="after"),
        code("""# After: 이메일 마스킹 미들웨어를 만듭니다
email_mask = PIIMiddleware("email", strategy="mask", apply_to_input=True, apply_to_output=True)
print("미들웨어 이름:", email_mask.name)""", lesson_part="after"),
        md("""**결과 읽기** — 미들웨어 이름에 `email`이 들어 있습니다.

기록을 비우고 같은 질문을 보냅니다. 마스킹 미들웨어의 입력 처리는 01절에서 본 before_model 자리에서 실행됩니다.
그래서 모델 호출을 감싸는 기록 훅보다 먼저 글을 바꿉니다.""", lesson_part="after"),
        code("""# 같은 질문을 마스킹 미들웨어가 있는 에이전트로 보냅니다
seen_by_model.clear()
masked_agent = create_agent(model, tools=[], middleware=[email_mask, record_model_input])
masked_result = masked_agent.invoke(question)
print("모델이 받은 글:", seen_by_model[0])""", lesson_part="after"),
        md("""**결과 읽기** — 이메일 자리가 `learner@****.com`처럼 별표로 바뀌었습니다. 모델은 가려진 글만 받았습니다.""", lesson_part="after"),
        code("""# 모델 입력과 저장된 대화 기록에 이메일 원문이 남았는지 확인합니다
email_sent = "learner@example.com" in seen_by_model[0]
stored_text = masked_result["messages"][0].text
print("모델 입력에 이메일 원문이 있나:", email_sent)
print("대화 기록에 저장된 질문:", stored_text)
assert not email_sent""", lesson_part="after"),
        md("""**결과 읽기** — 모델 입력 확인 결과가 `False`입니다. 대화 기록에 저장된 질문도 가려진 글로 바뀌었습니다.
이번에는 Ch16 방식과 달리 마스킹 함수를 직접 부르지 않았습니다. 그런데도 모델 호출 전에 적용됐습니다.

## 6. 값 하나 바꿔 보기 — 전화번호

공식 문서 기준으로 내장 종류는 email, credit_card, ip, mac_address, url입니다. 전화번호는 내장 종류에 없습니다.
이메일 마스킹만 등록한 상태에서 전화번호를 보내 봅니다.
실행 전에 예상해 봅니다. 전화번호는 등록하지 않은 종류이므로 그대로 모델에 갈 것입니다.""", lesson_part="after"),
        code("""# 전화번호가 든 질문을 이메일 마스킹 에이전트로 보냅니다
seen_by_model.clear()
phone_question = {"messages": [{"role": "user", "content": "연락처 010-1234-5678 로 문자 안내를 받을 수 있나요?"}]}
masked_agent.invoke(phone_question)
print("모델이 받은 글:", seen_by_model[0])""", lesson_part="after"),
        md("""**결과 읽기** — 전화번호 `010-1234-5678`이 그대로 보입니다. 등록한 종류만 가려집니다.

Ch16에서 쓴 전화번호 정규식을 `detector` 인자로 넘기면 전화번호용 미들웨어를 하나 더 만들 수 있습니다.
정규식 객체의 `.pattern` 속성에는 규칙이 글자로 들어 있습니다. 이 글자를 `detector` 인자에 넘깁니다.""", lesson_part="after"),
        code("""# Ch16의 전화번호 정규식으로 마스킹 미들웨어를 하나 더 만듭니다
phone_rule = PII_PATTERNS["phone"].pattern
phone_mask = PIIMiddleware(
    "phone",
    detector=phone_rule,
    strategy="mask",
    apply_to_input=True,
)
print("정규식 규칙:", phone_rule)
print("미들웨어 이름:", phone_mask.name)""", lesson_part="after"),
        md("""**결과 읽기** — 미들웨어 이름에 `phone`이 들어 있습니다.

이메일과 전화번호 마스킹 미들웨어를 함께 등록하고 같은 질문을 보냅니다.""", lesson_part="after"),
        code("""# 이메일·전화번호 마스킹을 함께 등록한 에이전트로 같은 질문을 보냅니다
seen_by_model.clear()
both_agent = create_agent(model, tools=[], middleware=[email_mask, phone_mask, record_model_input])
both_agent.invoke(phone_question)
print("모델이 받은 글:", seen_by_model[0])
assert "010-1234-5678" not in seen_by_model[0]""", lesson_part="after"),
        md("""**결과 읽기** — 이번에는 전화번호가 `****5678`로 가려졌습니다. 마지막 `assert` 줄이 오류 없이 지나갔습니다.

## 정리

- Ch16의 마스킹 함수는 우리가 부를 때만 적용됩니다. 미들웨어는 모델을 부를 때마다 자동으로 적용됩니다.
- 내장 미들웨어는 등록한 종류만 가립니다. 전화번호처럼 없는 종류는 `detector`에 정규식을 넘겨 추가합니다.
- 비교할 때는 답 문장이 아니라 「모델이 받은 글」을 기록해서 확인했습니다.""", lesson_part="after"),
    ]
    return "02-PII-마스킹-이식", "paired", cells



def section_03() -> tuple[str, str, list[dict]]:
    cells = title_cells(
        "요약 압축과 Compress",
        ["메시지 6개를 그대로 모델에 보내고 모델이 받은 메시지 수를 셉니다(Before).",
         "요약 미들웨어를 등록해 오래된 메시지를 요약 한 개로 바꿉니다(After).",
         "요약문에 중요한 조건이 남았는지 확인하고, 남길 메시지 수를 바꿔 봅니다."],
        "`.env` 파일의 `OPENAI_API_KEY`. 데이터 파일은 없습니다. 모델 호출은 5번이고 실행 시간은 1분 이내입니다. 예상 비용은 0.01달러 미만입니다.",
        "03-1-요약-전후.png", "요약 미들웨어가 오래된 메시지를 요약 한 개로 바꾸는 과정",
        "위가 요약 전, 아래가 요약 후입니다. 오래된 메시지 네 개가 요약 한 개가 되고 최근 두 개는 그대로 남습니다.",
    )
    cells += [
        md("이번 절에서 쓰는 이름을 불러옵니다. 오래된 대화를 요약하는 미들웨어는 `SummarizationMiddleware`입니다."),
        setup("""# 에이전트·미들웨어·메시지·모델을 만드는 도구를 불러옵니다
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, SummarizationMiddleware
from langchain.agents.middleware import wrap_model_call
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage"""),
    ]
    cells += key_and_model_cells()
    cells += [
        md("""## 2. 긴 대화 준비

대화가 길어지면 모델에 보내는 글이 늘어납니다. 요약 압축은 오래된 메시지를 짧은 요약 하나로 바꿔 입력을 줄이는 방법입니다.
Ch8에서 배운 Compress 전략을 미들웨어로 적용하는 것입니다. 먼저 도서관 대출 조건을 묻는 메시지 6개를 만듭니다.

메시지를 만드는 클래스 중 `HumanMessage`는 사용자 메시지, `AIMessage`는 모델 메시지입니다.
마지막 두 개는 사용자가 연달아 보낸 요청입니다. 에이전트는 마지막 사용자 요청에 답합니다."""),
        code("""# 사용자와 모델이 주고받은 메시지 6개를 만듭니다
history = [
    HumanMessage("대출은 몇 권까지 되나요?"),
    AIMessage("한 번에 5권까지 빌릴 수 있습니다. [E01 p.3]"),
    HumanMessage("대출 기간은요?"),
    AIMessage("14일이며, 예약자가 없으면 7일 연장할 수 있습니다. [E01 p.3]"),
    HumanMessage("출처도 같이 기억해 주세요."),
    HumanMessage("지금까지 말한 대출 조건을 정리해 주세요."),
]
print("대화 메시지 수:", len(history))"""),
        md("""**결과 읽기** — 대화 메시지 수는 `6`입니다. 권수 5권, 기간 14일, 연장 7일, 출처 E01 p.3가 중요한 조건입니다.

02절과 같은 기록 훅을 만듭니다. 모델이 받은 메시지를 목록에 적습니다."""),
        code(RECORD_INPUT),
        md("""출력은 없습니다.

## 3. Before — 대화 전체 보내기

요약 없이 메시지 6개를 모두 보냅니다.""", lesson_part="before"),
        code("""# Before: 요약 없이 대화 전체를 보냅니다
plain_agent = create_agent(model, tools=[], middleware=[record_model_input])
plain_agent.invoke({"messages": history})
print("모델이 받은 메시지 수:", len(seen_by_model))""", lesson_part="before"),
        md("""**결과 읽기** — 모델이 받은 메시지 수는 `6`입니다. 메시지가 100개로 늘면 100개를 모두 보내게 됩니다.

## 4. After — 요약 미들웨어 등록하기

`SummarizationMiddleware()` 클래스에 인자 세 개를 넘깁니다. 인자 `model`은 요약문을 만들 모델입니다.
인자 `trigger=("messages", 4)`는 메시지가 4개 이상이면 요약을 시작하라는 뜻입니다.
인자 `keep=("messages", 2)`는 가장 최근 메시지 2개는 요약하지 말고 그대로 두라는 뜻입니다.""", lesson_part="after"),
        code("""# After: 메시지가 4개 이상이면 최근 2개만 남기고 요약하는 미들웨어를 만듭니다
summarizer = SummarizationMiddleware(model=model, trigger=("messages", 4), keep=("messages", 2))
print("미들웨어 이름:", summarizer.name)""", lesson_part="after"),
        md("""**결과 읽기** — 미들웨어 이름 `SummarizationMiddleware`가 출력됩니다.

기록을 비우고 같은 대화를 보냅니다. 요약 미들웨어도 before_model 자리에서 실행됩니다.
그래서 모델 호출을 감싸는 기록 훅은 요약이 끝난 메시지를 봅니다.""", lesson_part="after"),
        code("""# 같은 대화를 요약 미들웨어가 있는 에이전트로 보냅니다
seen_by_model.clear()
summary_agent = create_agent(model, tools=[], middleware=[summarizer, record_model_input])
summary_result = summary_agent.invoke({"messages": history})
print("모델이 받은 메시지 수:", len(seen_by_model))""", lesson_part="after"),
        md("""**결과 읽기** — 모델이 받은 메시지 수가 `3`으로 줄었습니다. 요약 1개와 최근 메시지 2개입니다.

모델이 받은 메시지를 하나씩 출력해 봅니다.""", lesson_part="after"),
        code("""# 모델이 받은 메시지를 번호와 함께 출력합니다
for number, text in enumerate(seen_by_model, start=1):
    print(number, "|", text)""", lesson_part="after"),
        md("""**결과 읽기** — 1번은 `Here is a summary`로 시작하는 요약문입니다. 이 앞부분은 미들웨어 코드가 붙이는 고정 문구입니다.
그 뒤의 소제목과 내용은 요약 지시문에 따라 모델이 썼습니다. 그래서 실행마다 달라질 수 있습니다.
2번과 3번은 원래 대화의 마지막 두 메시지와 같습니다.""", lesson_part="after"),
        code("""# 요약문에 중요한 조건 네 가지가 남았는지 하나씩 확인합니다
summary_text = seen_by_model[0]
for condition in ["5권", "14일", "7일", "E01 p.3"]:
    print(condition, "남음:", condition in summary_text)
assert len(seen_by_model) == 3
assert summary_text.startswith("Here is a summary")""", lesson_part="after"),
        md("""**결과 읽기** — 이번 실행에서는 네 조건 모두 `True`입니다. 결과에 False가 있으면 그 조건은 요약하면서 사라진 것입니다.
`assert` 두 줄은 모델 문장과 상관없이 늘 같아야 하는 값(메시지 수와 고정 문구)만 확인합니다.

요약으로 메시지 수는 줄었습니다. 글자 수도 줄었는지, 저장된 대화 기록은 어떻게 됐는지 확인합니다.""", lesson_part="after"),
        code("""# 요약 전후의 모델 입력 글자 수와 저장된 대화 기록 수를 비교합니다
before_chars = 0
for message in history:
    before_chars = before_chars + len(message.text)
after_chars = 0
for text in seen_by_model:
    after_chars = after_chars + len(text)
print("요약 전 모델 입력 글자 수:", before_chars)
print("요약 후 모델 입력 글자 수:", after_chars)
print("저장된 대화 기록 수:", len(summary_result["messages"]))
for message in summary_result["messages"]:
    print("-", message.type, "|", message.text[:20])""", lesson_part="after"),
        md("""**결과 읽기** — 요약 전 글자 수는 `130`, 요약 후 글자 수는 `381`입니다. 짧은 대화라 요약문이 원문보다 길었습니다.
저장된 대화 기록 수는 `4`입니다. 첫 메시지는 `Here is a summary`로 시작하는 요약문입니다.
다음 두 개는 최근 메시지이고, 마지막 ai 메시지가 모델의 새 답입니다.

## 5. 값 하나 바꿔 보기 — 남길 메시지 수

`keep` 값을 2에서 4로 바꿉니다. 실행 전에 예상해 봅니다. 요약 1개와 최근 4개, 모두 5개가 될 것입니다.""", lesson_part="after"),
        code("""# 최근 메시지를 4개 남기도록 바꿔 같은 대화를 보냅니다
keep_four = SummarizationMiddleware(model=model, trigger=("messages", 4), keep=("messages", 4))
seen_by_model.clear()
keep_four_agent = create_agent(model, tools=[], middleware=[keep_four, record_model_input])
keep_four_agent.invoke({"messages": history})
print("모델이 받은 메시지 수:", len(seen_by_model))
for number, text in enumerate(seen_by_model, start=1):
    print(number, "|", text[:30])""", lesson_part="after"),
        md("""**결과 읽기** — 모델이 받은 메시지 수가 `5`입니다. 1번은 요약문이고, 2~5번은 원래 대화의 마지막 네 메시지입니다.
남길 메시지가 많을수록 입력은 덜 줄지만 원문이 더 많이 보존됩니다.

## 정리

- 요약 미들웨어는 메시지 수가 기준 이상이면 오래된 메시지를 요약 하나로 바꿉니다.
- 최근 메시지는 `keep` 값만큼 원문 그대로 남습니다.
- 요약문은 모델이 만들므로 권수·기간·출처 같은 조건이 빠질 수 있습니다. 중요한 조건은 요약에 맡기지 말고 따로 저장합니다.""", lesson_part="after"),
    ]
    return "03-요약-압축과-Compress", "paired", cells


def section_04() -> tuple[str, str, list[dict]]:
    cells = title_cells(
        "호출 한도와 재시도·폴백",
        ["시간 제한을 아주 짧게 준 모델로 재시도 미들웨어가 몇 번 다시 부르는지 셉니다.",
         "존재하지 않는 모델 이름으로 폴백 미들웨어가 예비 모델로 넘어가는지 확인합니다.",
         "호출 한도를 1번으로 두고 도구가 필요한 질문을 보내 실행이 멈추는지 확인합니다."],
        "`.env` 파일의 `OPENAI_API_KEY`. 데이터 파일은 없습니다. 모델 호출 요청은 6번이고 그중 정상 응답은 2번입니다. 실행 시간은 1분 이내이고, 예상 비용은 0.01달러 미만입니다.",
        "04-1-세-정책.png", "재시도, 폴백, 호출 한도가 각각 실패를 다루는 방식",
        "위에서부터 재시도, 폴백, 호출 한도입니다. 재시도는 같은 모델을 다시 부르고, 폴백은 다른 모델로 바꾸고, 호출 한도는 실행을 멈춥니다.",
    )
    cells += [
        md("이번 절에서 쓰는 이름을 불러옵니다. 재시도·폴백·호출 한도 미들웨어 세 개가 들어 있습니다."),
        setup("""# 에이전트·미들웨어·도구·모델을 만드는 도구를 불러옵니다
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ModelFallbackMiddleware, ModelRetryMiddleware
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.chat_models import init_chat_model
from langchain.tools import tool"""),
    ]
    cells += key_and_model_cells()
    cells += [
        md("""## 2. 시도 기록 훅 만들기

이번 절에서는 모델 호출이 실패하는 상황을 실제로 만듭니다. 시도가 몇 번 있었는지 세려면 기록 훅이 필요합니다.
이 훅은 모델을 부를 때마다 모델 이름을 `attempts` 목록에 적습니다."""),
        code("""# 모델을 부를 때마다 모델 이름을 적는 훅을 만듭니다
attempts = []


@wrap_model_call
def record_attempt(request: ModelRequest, handler: Callable) -> ModelResponse:
    attempts.append(request.model.model_name)
    return handler(request)"""),
        md("""출력은 없습니다.

## 3. 재시도 — 같은 모델을 다시 부르기

재시도(retry)는 실패한 호출을 같은 모델에 다시 보내는 방법입니다. 네트워크가 잠깐 느릴 때 쓸모가 있습니다.

실패를 일부러 만들기 위해 시간 제한(`timeout`)을 0.001초로 줍니다. 이 시간 안에는 응답이 올 수 없습니다.
인자 `max_retries=0`은 모델 객체가 스스로 다시 시도하지 않게 합니다. 재시도는 미들웨어에만 맡깁니다."""),
        code("""# 0.001초 안에 응답해야 하는 모델을 만듭니다(반드시 시간 초과가 납니다)
slow_model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
    timeout=0.001,
    max_retries=0,
)
print("시간 제한(초):", slow_model.request_timeout)"""),
        md("""**결과 읽기** — 시간 제한이 `0.001`초로 설정됐습니다.

`ModelRetryMiddleware()` 클래스의 `max_retries=2`는 처음 시도가 실패하면 두 번 더 시도하라는 뜻입니다.
인자 `initial_delay=0.5`는 첫 재시도 전에 0.5초 기다린다는 뜻입니다.
기다리는 시간은 재시도할 때마다 두 배가 되므로 두 번째 재시도 전에는 1초입니다. 대기 시간은 이번에 재지 않습니다.
인자 `jitter=False`는 기다리는 시간에 무작위 값을 더하지 않게 합니다.

먼저 등록한 미들웨어가 바깥에서 감쌉니다. 그래서 재시도는 안쪽의 기록 훅과 모델을 함께 다시 부릅니다.
재시도 미들웨어를 기록 훅보다 앞에 두어야 다시 시도할 때마다 기록 훅도 실행됩니다."""),
        code("""# 재시도 미들웨어를 등록하고 질문을 보냅니다
retry = ModelRetryMiddleware(max_retries=2, initial_delay=0.5, jitter=False)
retry_agent = create_agent(slow_model, tools=[], middleware=[retry, record_attempt])
question = {"messages": [{"role": "user", "content": "자료실 운영 시간을 알려 주세요."}]}
retry_result = retry_agent.invoke(question)
last_message = retry_result["messages"][-1]
print("시도 횟수:", len(attempts))
print("마지막 메시지:", last_message.text)"""),
        md("""**결과 읽기** — 시도 횟수는 `3`입니다. 처음 1번과 재시도 2번입니다.
세 번 모두 시간 초과였기 때문에 마지막 메시지는 답이 아니라 실패 안내입니다.
재시도는 원인이 사라지지 않으면 결과를 바꾸지 못합니다. 이번 조건은 매번 시간 초과가 나도록 만들었습니다."""),
        code("""# 재시도 횟수를 확인하고, 다음 실험을 위해 기록을 비웁니다
retry_attempts = len(attempts)
assert retry_attempts == 3
attempts.clear()
print("비운 뒤 기록 개수:", len(attempts))"""),
        md("""**결과 읽기** — 비운 뒤 기록 개수는 `0`입니다.

## 4. 폴백 — 다른 모델로 넘어가기

폴백(fallback)은 첫 모델이 실패하면 예비 모델로 바꿔 부르는 방법입니다. 모델 서비스 한 곳에 장애가 났을 때 씁니다.
실패를 만들기 위해 존재하지 않는 모델 이름을 씁니다. 예비 모델은 더 작은 `gpt-5.4-nano`입니다."""),
        code("""# 존재하지 않는 이름의 모델과, 대신 쓸 예비 모델을 만듭니다
broken_model = init_chat_model("openai:gpt-no-such-model", temperature=0, max_retries=0)
backup_model = init_chat_model("openai:gpt-5.4-nano", temperature=0, reasoning_effort="none")
print("첫 모델:", broken_model.model_name)
print("예비 모델:", backup_model.model_name)"""),
        md("""**결과 읽기** — 첫 모델 이름은 `gpt-no-such-model`, 예비 모델 이름은 `gpt-5.4-nano`입니다.

`ModelFallbackMiddleware()` 클래스에 예비 모델을 넘깁니다. 이번에도 기록 훅을 뒤에 둡니다.
마지막 메시지의 `response_metadata` 속성에는 답한 모델 이름 같은 응답 정보가 들어 있습니다."""),
        code("""# 폴백 미들웨어를 등록하고 질문을 보냅니다
fallback = ModelFallbackMiddleware(backup_model)
fallback_agent = create_agent(broken_model, tools=[], middleware=[fallback, record_attempt])
greeting = {"messages": [{"role": "user", "content": "한 문장으로 인사해 주세요."}]}
fallback_result = fallback_agent.invoke(greeting)
last_message = fallback_result["messages"][-1]
print("시도한 모델 순서:", attempts)
print("답한 모델:", last_message.response_metadata["model_name"])"""),
        md("""**결과 읽기** — 시도한 모델 순서가 `gpt-no-such-model` 다음 `gpt-5.4-nano`입니다.
답한 모델도 nano 모델입니다. 첫 모델이 실패하자 미들웨어가 요청의 모델만 바꿔 다시 불렀습니다."""),
        code("""# 폴백 순서를 확인하고, 다음 실험을 위해 기록을 비웁니다
# list()로 복사본을 만들어 두면 원본을 비워도 순서가 남습니다
fallback_order = list(attempts)
assert fallback_order == ["gpt-no-such-model", "gpt-5.4-nano"]
attempts.clear()
print("비운 뒤 기록 개수:", len(attempts))"""),
        md("""**결과 읽기** — 비운 뒤 기록 개수는 `0`입니다.

## 5. 호출 한도 — 실행 멈추기

호출 한도(call limit)는 한 번 실행하는 동안 모델을 부를 수 있는 횟수의 상한입니다.
모델이 도구를 끝없이 부르는 반복을 막을 때 씁니다. 01절의 운영 시간 도구를 다시 만듭니다."""),
        code("""# 자료실 운영 시간을 알려 주는 도구를 만듭니다
@tool
def lookup_hours(day: str) -> str:
    \"\"\"자료실 운영 시간을 조회합니다. day에는 "평일" 또는 "토요일"을 넣습니다.\"\"\"
    if day == "평일":
        return "평일 09:00~20:00"
    return "토요일 10:00~17:00"


print("도구 이름:", lookup_hours.name)"""),
        md("""**결과 읽기** — 도구 이름 `lookup_hours`가 출력됩니다.

인자 `run_limit=1`은 한 번 실행하는 동안 모델을 1번만 부르라는 뜻입니다.
도구가 필요한 질문은 모델을 최소 2번 불러야 합니다. 도구 요청에 1번, 최종 답에 1번입니다. 그래서 두 번째 호출에서 멈출 것입니다.
인자 `exit_behavior="end"`는 한도에 걸리면 오류를 내지 않고 안내 메시지로 끝내라는 뜻입니다."""),
        code("""# 모델 호출을 1번으로 제한하고 도구가 필요한 질문을 보냅니다
limit = ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")
limit_agent = create_agent(model, tools=[lookup_hours], middleware=[limit, record_attempt])
tool_question = "반드시 lookup_hours 도구로 확인한 뒤 자료실 평일 운영 시간을 알려 주세요."
limit_result = limit_agent.invoke({"messages": [{"role": "user", "content": tool_question}]})
print("모델 호출 횟수:", len(attempts))
for message in limit_result["messages"]:
    print(message.type, "|", message.text)"""),
        md("""**결과 읽기** — 모델 호출 횟수는 `1`입니다. 마지막 메시지는 `Model call limits exceeded`로 시작하는 안내입니다.
첫 호출에서 모델이 도구를 요청했고 도구도 실행됐습니다. 그러나 도구 결과를 읽을 두 번째 모델 호출은 한도에 걸려 실행되지 않았습니다."""),
        code("""# 세 실험의 결과를 한 번에 출력합니다
limit_calls = len(attempts)
print("재시도 — 시도 횟수:", retry_attempts)
print("폴백 — 시도한 모델:", fallback_order)
print("호출 한도 — 모델 호출 횟수:", limit_calls)
assert limit_calls == 1"""),
        md("""**결과 읽기** — 재시도는 `3`번 시도, 폴백은 두 모델을 차례로 시도, 호출 한도는 `1`번 호출에서 멈췄습니다.

## 정리

- 재시도는 같은 모델을 다시 부릅니다. 실패 원인이 그대로면 횟수만 늘어납니다.
- 폴백은 다른 모델로 바꿔 부릅니다. 한 모델 서비스의 장애에 대비합니다.
- 호출 한도는 정해진 횟수를 넘으면 실행을 멈춥니다. 끝없는 반복과 비용 증가를 막습니다."""),
    ]
    return "04-호출-한도와-재시도-폴백", "experiment", cells



def section_05() -> tuple[str, str, list[dict]]:
    cells = title_cells(
        "커스텀 예산 미들웨어",
        ["모델 응답에 붙은 토큰 사용량을 읽습니다.",
         "예산 검사 없이 질문 두 개를 보내 둘 다 모델이 답하는 것을 확인합니다(Before).",
         "토큰 예산 미들웨어를 직접 만들어, 예산을 다 쓰면 모델을 부르지 않게 합니다(After)."],
        "`.env` 파일의 `OPENAI_API_KEY`. 데이터 파일은 없습니다. 모델 호출은 6번이고 실행 시간은 1분 이내입니다. 예상 비용은 0.01달러 미만입니다.",
        "05-1-예산-검사.png", "예산 검사 훅이 모델 호출 전에 사용량을 비교해 호출을 막는 과정",
        "모델을 부르기 전에 쓴 토큰과 한도를 비교합니다. 한도에 닿았으면 모델을 부르지 않고 안내 메시지를 반환합니다.",
    )
    cells += [
        md("이번 절에서 쓰는 이름을 불러옵니다. 훅 두 개(`after_model`, `wrap_model_call`)로 예산 미들웨어를 만듭니다."),
        setup("""# 에이전트·훅·메시지·모델을 만드는 도구를 불러옵니다
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import AgentState, ModelRequest, ModelResponse, Runtime
from langchain.agents.middleware import after_model, wrap_model_call
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage"""),
    ]
    cells += key_and_model_cells()
    cells += [
        md("""## 2. 토큰 사용량 읽기

토큰(token)은 모델이 글을 나누어 읽는 단위입니다. 모델 서비스 비용은 보통 토큰 수로 계산합니다.
모델 응답의 `usage_metadata` 속성에 이번 호출에서 쓴 토큰 수가 들어 있습니다."""),
        code("""# 모델을 한 번 불러 사용한 토큰 수를 출력합니다
reply = model.invoke("파이썬을 한 문장으로 소개해 주세요.")
usage = reply.usage_metadata
print("입력 토큰(input_tokens):", usage["input_tokens"])
print("출력 토큰(output_tokens):", usage["output_tokens"])
print("합계(total_tokens):", usage["total_tokens"])"""),
        md("""**결과 읽기** — 합계 `total_tokens`는 입력과 출력 토큰을 더한 값입니다. 숫자는 답 길이에 따라 실행마다 조금 달라집니다.

## 3. Before — 예산 검사 없이 두 번 부르기

예산 검사가 없는 에이전트에 질문 두 개를 차례로 보냅니다.""", lesson_part="before"),
        code("""# Before: 예산 검사 없이 질문 두 개를 차례로 보냅니다
plain_agent = create_agent(model, tools=[])
first = plain_agent.invoke({"messages": [{"role": "user", "content": "파이썬을 한 문장으로 소개해 주세요."}]})
second = plain_agent.invoke({"messages": [{"role": "user", "content": "LangChain을 한 문장으로 소개해 주세요."}]})
print("첫 답:", first["messages"][-1].text)
print("둘째 답:", second["messages"][-1].text)""", lesson_part="before"),
        md("""**결과 읽기** — 두 질문 모두 모델이 답했습니다. 출력의 `첫 답:` 줄과 `둘째 답:` 줄에 모두 모델의 문장이 있습니다.
답 문장은 실행할 때마다 달라질 수 있습니다.""", lesson_part="before"),
        code("""# 두 호출에서 쓴 토큰을 더합니다
first_tokens = first["messages"][-1].usage_metadata["total_tokens"]
second_tokens = second["messages"][-1].usage_metadata["total_tokens"]
print("두 호출 토큰 합계:", first_tokens + second_tokens)
print("둘째 답을 만든 메시지 종류:", second["messages"][-1].type)""", lesson_part="before"),
        md("""**결과 읽기** — 둘째 답을 만든 메시지 종류가 `ai`입니다. 사용량이 아무리 늘어도 막는 장치가 없습니다.

## 4. After — 토큰 예산 미들웨어 만들기

예산 정보를 딕셔너리 하나에 담습니다. 키 `limit_tokens`는 한도, 키 `used_tokens`는 지금까지 쓴 양입니다.
실습에서는 차단을 바로 보기 위해 한도를 1토큰으로 둡니다. 첫 호출은 사용량 0에서 시작하므로 허용됩니다.""", lesson_part="after"),
        code("""# 토큰 예산을 담을 딕셔너리를 만듭니다
budget = {"limit_tokens": 1, "used_tokens": 0}
print("예산:", budget)""", lesson_part="after"),
        md("""**결과 읽기** — 한도 `1`, 사용량 `0`으로 시작합니다.

첫 번째 훅은 모델 응답을 받은 직후 실행됩니다. 방금 받은 메시지의 토큰 수를 사용량에 더합니다.
`state["messages"][-1]` 값은 대화 기록의 마지막 메시지, 즉 방금 받은 응답입니다.
모델을 부르지 않고 만든 응답에는 사용량(`usage_metadata`)이 없습니다. 이때는 더하지 않고 끝냅니다.""", lesson_part="after"),
        code("""# 모델 응답을 받은 직후 사용한 토큰 수를 예산에 더하는 훅
@after_model
def record_usage(state: AgentState, runtime: Runtime) -> None:
    last_message = state["messages"][-1]
    if last_message.usage_metadata is None:
        return None
    used = last_message.usage_metadata["total_tokens"]
    budget["used_tokens"] = budget["used_tokens"] + used""", lesson_part="after"),
        md("""출력은 없습니다.

두 번째 훅은 모델을 부르기 전에 실행되는 감싸기형 훅입니다. 사용량이 한도에 닿았으면 `handler(request)`를 부르지 않습니다.
대신 안내 문장을 담은 `AIMessage`를 반환합니다. 모델이 답한 것처럼 대화가 끝나지만, 실제 모델은 호출되지 않습니다.
반환 타입에 적은 `ModelResponse | AIMessage`는 모델 응답이거나 직접 만든 AIMessage라는 뜻입니다.""", lesson_part="after"),
        code("""# 모델을 부르기 전에 예산이 남았는지 검사하는 훅
@wrap_model_call
def check_budget(request: ModelRequest, handler: Callable) -> ModelResponse | AIMessage:
    if budget["used_tokens"] >= budget["limit_tokens"]:
        return AIMessage("토큰 예산을 모두 써서 모델을 부르지 않았습니다.")
    return handler(request)""", lesson_part="after"),
        md("""출력은 없습니다. 두 훅을 등록하고 Before와 같은 질문 두 개를 보냅니다.""", lesson_part="after"),
        code("""# After: 예산 미들웨어를 등록하고 같은 질문 두 개를 보냅니다
budget_agent = create_agent(model, tools=[], middleware=[check_budget, record_usage])
first = budget_agent.invoke({"messages": [{"role": "user", "content": "파이썬을 한 문장으로 소개해 주세요."}]})
second = budget_agent.invoke({"messages": [{"role": "user", "content": "LangChain을 한 문장으로 소개해 주세요."}]})
print("첫 답:", first["messages"][-1].text)
print("둘째 답:", second["messages"][-1].text)""", lesson_part="after"),
        md("""**결과 읽기** — 첫 답은 모델이 만들었고, 문장은 실행마다 달라질 수 있습니다. 둘째 답은 `토큰 예산을 모두 써서 모델을 부르지 않았습니다.`입니다.""", lesson_part="after"),
        code("""# 두 번째 질문에서 모델이 호출되지 않았는지 확인합니다
second_message = second["messages"][-1]
print("사용한 토큰:", budget["used_tokens"])
print("둘째 답에 토큰 사용량이 있나:", second_message.usage_metadata is not None)
assert second_message.text == "토큰 예산을 모두 써서 모델을 부르지 않았습니다.\"""", lesson_part="after"),
        md("""**결과 읽기** — 둘째 답에 토큰 사용량이 있는지 확인한 결과가 `False`입니다. 실제 모델 응답에는 사용량이 붙으므로, 모델이 호출되지 않았다는 뜻입니다.
사용한 토큰은 첫 호출에서 쓴 양만 들어 있습니다.

## 5. 값 하나 바꿔 보기 — 한도 늘리기

한도를 1,000토큰으로 늘리고 사용량을 0으로 바꿉니다. 실행 전에 예상해 봅니다. 두 질문 모두 답할 것입니다.""", lesson_part="after"),
        code("""# 한도를 1,000토큰으로 늘리고 같은 질문 두 개를 다시 보냅니다
budget["limit_tokens"] = 1000
budget["used_tokens"] = 0
first = budget_agent.invoke({"messages": [{"role": "user", "content": "파이썬을 한 문장으로 소개해 주세요."}]})
second = budget_agent.invoke({"messages": [{"role": "user", "content": "LangChain을 한 문장으로 소개해 주세요."}]})
print("둘째 답을 만든 메시지에 사용량이 있나:", second["messages"][-1].usage_metadata is not None)
print("사용한 토큰:", budget["used_tokens"])""", lesson_part="after"),
        md("""**결과 읽기** — 이번에는 `True`입니다. 한도가 넉넉하므로 두 번째 호출도 실제 모델이 답했습니다.

## 정리

- `after_model` 훅으로 호출마다 쓴 토큰을 더하고, `wrap_model_call` 훅으로 호출 전에 한도를 검사했습니다.
- 감싸기형 훅이 `handler(request)`를 부르지 않으면 모델이 호출되지 않습니다.
- 이 예산은 노트북 안의 딕셔너리에만 저장됩니다. 사용자별 하루 한도처럼 오래 유지할 값은 데이터베이스에 저장해야 합니다.""", lesson_part="after"),
    ]
    return "05-커스텀-예산-미들웨어", "paired", cells


def section_06() -> tuple[str, str, list[dict]]:
    cells = title_cells(
        "커스텀 감사 미들웨어",
        ["개인정보 원문 대신 지문(해시)을 남기는 함수를 만듭니다.",
         "에이전트 시작·도구 호출·종료를 기록하는 감사 훅 세 개를 만듭니다.",
         "이메일이 든 질문으로 실행하고, 기록에 원문이 남지 않았는지 확인합니다."],
        "`.env` 파일의 `OPENAI_API_KEY`. 데이터 파일은 없습니다. 모델 호출은 2번이고 실행 시간은 1분 이내입니다. 예상 비용은 0.01달러 미만입니다.",
        "06-1-감사-기록.png", "감사 훅 세 개가 실행 중 사건을 기록하는 위치",
        "에이전트 시작, 도구 호출 앞뒤, 에이전트 종료에서 사건 하나씩이 기록됩니다. 기록에는 질문 원문이 들어가지 않습니다.",
    )
    cells += [
        md("이번 절에서 쓰는 이름을 불러옵니다. 지문은 파이썬 기본 모듈 `hashlib`으로 만듭니다."),
        setup("""# 지문·기록·에이전트·훅·도구·모델을 만드는 도구를 불러옵니다
import hashlib
import json
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import AgentState, Runtime, ToolCallRequest
from langchain.agents.middleware import after_agent, before_agent, wrap_tool_call
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import ToolMessage"""),
    ]
    cells += key_and_model_cells()
    cells += [
        md("""## 2. 원문 대신 지문 남기기

감사 기록(audit log)은 나중에 「언제 어떤 실행이 있었고 어떤 도구가 쓰였나」를 확인하기 위한 사건 목록입니다.
질문 원문을 그대로 기록하면 기록 파일에 개인정보가 쌓입니다. 그래서 원문 대신 지문을 남깁니다.
지문(해시)은 글을 정해진 규칙으로 섞어 만든 짧은 문자열입니다. 같은 글은 같은 지문이 되지만, 지문만 보고 원문을 알아내기는 어렵습니다."""),
        code("""# 글을 받아 10글자짜리 지문을 만드는 함수
def fingerprint(text: str) -> str:
    data = ("lesson-salt:" + text).encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    return digest[:10]


print("지문 예시:", fingerprint("learner@example.com"))"""),
        md("""**결과 읽기** — 지문 예시로 `367129c879`처럼 영문과 숫자 10글자가 나옵니다. 이 안에 `learner@example.com`이라는 글자는 없습니다.
글 앞에 `lesson-salt:`를 붙이는 이유는, 흔한 글의 지문을 미리 만들어 둔 표로 원문을 짐작하기 어렵게 하기 위해서입니다.

## 3. 감사 훅 세 개 만들기

사건을 담을 빈 목록을 만듭니다."""),
        code("""# 감사 사건을 담을 빈 목록을 만듭니다
events = []
print("사건 수:", len(events))"""),
        md("""**결과 읽기** — 사건 수는 `0`입니다.

첫 번째 훅은 에이전트가 시작할 때 질문의 글자 수와 지문을 기록합니다. 원문은 기록하지 않습니다."""),
        code("""# 에이전트 시작 사건을 기록하는 훅
@before_agent
def audit_start(state: AgentState, runtime: Runtime) -> None:
    first_text = state["messages"][0].text
    event = {"event": "agent_start", "input_chars": len(first_text), "fingerprint": fingerprint(first_text)}
    events.append(event)"""),
        md("""출력은 없습니다.

두 번째 훅은 도구 호출을 감쌉니다. 호출 전에 시작 사건을, 성공하면 성공 사건을, 오류가 나면 오류 사건을 남깁니다.
예외 처리 문법인 `try`와 `except`는 Ch2 05절에서 배웠습니다.

오류 사건의 `type(error).__name__` 값은 오류 종류 이름(예: `ValueError`)을 글로 꺼낸 것입니다.
이 훅은 오류를 기록한 뒤 단독 `raise` 줄로 방금 잡은 오류를 그대로 다시 올려 보냅니다."""),
        code("""# 도구 호출의 시작·성공·오류를 기록하는 훅
@wrap_tool_call
def audit_tool(request: ToolCallRequest, handler: Callable) -> ToolMessage:
    tool_name = request.tool_call["name"]
    events.append({"event": "tool_start", "tool": tool_name})
    try:
        result = handler(request)
    except Exception as error:
        events.append({"event": "tool_error", "tool": tool_name, "error": type(error).__name__})
        raise
    events.append({"event": "tool_success", "tool": tool_name})
    return result"""),
        md("""출력은 없습니다.

세 번째 훅은 에이전트가 끝날 때 대화 기록의 메시지 수를 남깁니다."""),
        code("""# 에이전트 종료 사건을 기록하는 훅
@after_agent
def audit_end(state: AgentState, runtime: Runtime) -> None:
    events.append({"event": "agent_end", "messages": len(state["messages"])})"""),
        md("""출력은 없습니다.

## 4. 이메일이 든 질문으로 실행하기

01절의 운영 시간 도구를 다시 만듭니다."""),
        code("""# 자료실 운영 시간을 알려 주는 도구를 만듭니다
@tool
def lookup_hours(day: str) -> str:
    \"\"\"자료실 운영 시간을 조회합니다. day에는 "평일" 또는 "토요일"을 넣습니다.\"\"\"
    if day == "평일":
        return "평일 09:00~20:00"
    return "토요일 10:00~17:00"


print("도구 이름:", lookup_hours.name)"""),
        md("""**결과 읽기** — 도구 이름 `lookup_hours`가 출력됩니다.

감사 훅 세 개를 등록하고, 이메일이 든 질문을 보냅니다."""),
        code("""# 감사 훅을 등록하고 이메일이 든 질문으로 실행합니다
events.clear()
audit_agent = create_agent(model, tools=[lookup_hours], middleware=[audit_start, audit_tool, audit_end])
question = "learner@example.com 입니다. 자료실 평일 운영 시간을 알려 주세요."
audit_result = audit_agent.invoke({"messages": [{"role": "user", "content": question}]})
print("최종 답:", audit_result["messages"][-1].text)
for event in events:
    print(event)"""),
        md("""**결과 읽기** — 사건이 `agent_start`, `tool_start`, `tool_success`, `agent_end` 순서로 기록됐습니다.
시작 사건에는 글자 수와 지문만 있고, 종료 사건에는 메시지 수만 있습니다. 최종 답 문장은 실행마다 달라질 수 있습니다."""),
        code("""# 기록 전체를 글로 바꿔 이메일 원문이 들어 있는지 확인합니다
saved_text = json.dumps(events, ensure_ascii=False)
has_email = "learner@example.com" in saved_text
print("기록에 이메일 원문이 있나:", has_email)
print("첫 사건:", events[0]["event"], "/ 마지막 사건:", events[-1]["event"])
assert not has_email
assert events[0]["event"] == "agent_start"
assert events[-1]["event"] == "agent_end\""""),
        md("""**결과 읽기** — 기록에 이메일 원문이 있는지 확인한 결과는 `False`입니다. 첫 사건은 `agent_start`, 마지막 사건은 `agent_end`입니다.

## 5. 값 하나 바꿔 보기 — 글자 수가 같은 두 글

글자 수만 기록하면 서로 다른 질문을 구분할 수 없습니다. 글자 수가 같은 두 글의 지문을 비교합니다."""),
        code("""# 글자 수가 같은 두 글의 지문을 비교합니다
text_a = "대출 연장 문의"
text_b = "반납 기한 문의"
print("글자 수:", len(text_a), len(text_b))
print("지문:", fingerprint(text_a), fingerprint(text_b))
print("지문이 서로 다른가:", fingerprint(text_a) != fingerprint(text_b))
print("같은 글의 지문이 같은가:", fingerprint(text_a) == fingerprint("대출 연장 문의"))"""),
        md("""**결과 읽기** — 두 글의 글자 수는 같지만 지문이 서로 다르다는 결과가 `True`입니다.
같은 글을 다시 넣으면 지문도 같았습니다. 그래서 지문을 남기면 원문 없이도 「같은 질문이 반복됐는지」는 알 수 있습니다.

## 정리

- 감사 훅은 실행의 시작·도구 호출·종료에서 사건을 하나씩 기록했습니다.
- 개인정보가 들어갈 수 있는 원문 대신 글자 수와 지문을 남겼습니다.
- 도구 오류는 기록한 뒤 `raise`로 다시 올려 보내도록 만들었습니다. 오류가 난 실행은 이번에 관찰하지 않았습니다."""),
    ]
    return "06-커스텀-감사-미들웨어", "experiment", cells


def section_07() -> tuple[str, str, list[dict]]:
    cells = title_cells(
        "순서와 합성",
        ["이름표 A와 B마다 훅을 세 종류씩, 모두 여섯 개 만듭니다.",
         "A 다음 B 순서로 등록하고, 훅이 실행된 순서를 읽습니다.",
         "등록 순서를 B 다음 A로 바꿔 실행 순서가 어떻게 바뀌는지 비교합니다."],
        "`.env` 파일의 `OPENAI_API_KEY`. 데이터 파일은 없습니다. 모델 호출은 2번이고 실행 시간은 1분 이내입니다. 예상 비용은 0.01달러 미만입니다.",
        "07-1-합성-순서.png", "미들웨어 A와 B가 모델 호출을 겹겹이 감싸는 모양",
        "바깥 칸이 먼저 등록한 A, 안쪽 칸이 B입니다. 들어갈 때는 A 다음 B, 나올 때는 B 다음 A 순서입니다.",
    )
    cells += [
        md("이번 절에서 쓰는 이름을 불러옵니다. 01절과 같은 훅 데코레이터를 씁니다."),
        setup("""# 에이전트·훅·모델을 만드는 도구를 불러옵니다
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import AgentState, ModelRequest, ModelResponse, Runtime
from langchain.agents.middleware import after_model, before_model, wrap_model_call
from langchain.chat_models import init_chat_model"""),
    ]
    cells += key_and_model_cells()
    cells += [
        md("""## 2. 이름표 붙은 훅 만들기

04절에서는 재시도 미들웨어를 기록 훅보다 앞에 두어 시도 3번을 모두 기록했습니다.
이번에는 훅을 여러 개 등록했을 때의 순서 규칙을 확인합니다. 실행 순서를 적을 빈 목록부터 만듭니다."""),
        code("""# 훅이 실행된 순서를 적을 빈 목록을 만듭니다
order = []
print("기록 개수:", len(order))"""),
        md("""**결과 읽기** — 기록 개수는 `0`입니다.

이름표 A가 붙은 훅 세 개를 만듭니다. 먼저 모델을 부르기 직전에 실행되는 훅입니다.
데코레이터로 만든 훅은 하나가 미들웨어 하나입니다. 이 노트북에서는 이름표가 같은 세 개를 묶어 「미들웨어 A」라고 부릅니다."""),
        code("""# A: 모델을 부르기 직전에 실행되는 훅
@before_model
def a_before(state: AgentState, runtime: Runtime) -> None:
    order.append("A before_model")"""),
        md("""이름표 A의 두 번째 훅은 모델 호출을 감쌉니다."""),
        code("""# A: 모델 호출을 앞뒤로 감싸는 훅
@wrap_model_call
def a_wrap(request: ModelRequest, handler: Callable) -> ModelResponse:
    order.append("A wrap 시작")
    response = handler(request)
    order.append("A wrap 끝")
    return response"""),
        md("""이름표 A의 세 번째 훅은 모델 응답을 받은 직후 실행됩니다."""),
        code("""# A: 모델 응답을 받은 직후 실행되는 훅
@after_model
def a_after(state: AgentState, runtime: Runtime) -> None:
    order.append("A after_model")"""),
        md("""이름표 B가 붙은 훅 세 개도 같은 모양으로 만듭니다."""),
        code("""# B: 모델을 부르기 직전에 실행되는 훅
@before_model
def b_before(state: AgentState, runtime: Runtime) -> None:
    order.append("B before_model")"""),
        md("""이름표 B의 감싸기형 훅입니다."""),
        code("""# B: 모델 호출을 앞뒤로 감싸는 훅
@wrap_model_call
def b_wrap(request: ModelRequest, handler: Callable) -> ModelResponse:
    order.append("B wrap 시작")
    response = handler(request)
    order.append("B wrap 끝")
    return response"""),
        md("""이름표 B의 마지막 훅입니다."""),
        code("""# B: 모델 응답을 받은 직후 실행되는 훅
@after_model
def b_after(state: AgentState, runtime: Runtime) -> None:
    order.append("B after_model")"""),
        md("""출력은 없습니다.

## 3. A 다음 B 순서로 등록하기

이름표 A의 훅 세 개를 먼저, 이름표 B의 훅 세 개를 나중에 목록에 넣습니다. 도구 없이 질문 하나를 보내므로 모델은 1번 호출됩니다.
반복문에 쓴 `enumerate(order, start=1)` 함수는 기록마다 1부터 시작하는 번호를 붙여 줍니다."""),
        code("""# A 다음 B 순서로 등록하고 질문 하나를 보냅니다
a_then_b = [a_before, a_wrap, a_after, b_before, b_wrap, b_after]
agent = create_agent(model, tools=[], middleware=a_then_b)
agent.invoke({"messages": [{"role": "user", "content": "한 문장으로 인사해 주세요."}]})
for number, name in enumerate(order, start=1):
    print(number, name)"""),
        md("""**결과 읽기** — 1~2번은 `A before_model` 다음 `B before_model`입니다. 들어가는 훅은 등록 순서대로 실행됩니다.

3~6번은 `A wrap 시작`, `B wrap 시작`, `B wrap 끝`, `A wrap 끝`입니다. 미들웨어 A가 B를 감싸고, B가 모델을 감쌉니다.

7~8번은 `B after_model` 다음 `A after_model`입니다. 나오는 훅은 등록 순서의 반대로 실행됩니다.

목록에서는 A의 감싸기 훅이 B의 before_model 훅보다 앞에 있습니다. 그래도 2번이 B before_model, 3번이 A wrap 시작입니다.
종류가 다른 훅은 등록 순서와 상관없이 before → wrap → after 순서로 실행됐습니다."""),
        code("""# 실행 순서가 규칙대로인지 확인하고 기록을 비웁니다
expected = [
    "A before_model", "B before_model",
    "A wrap 시작", "B wrap 시작", "B wrap 끝", "A wrap 끝",
    "B after_model", "A after_model",
]
print("규칙과 같은가:", order == expected)
assert order == expected
order.clear()"""),
        md("""**결과 읽기** — 규칙과 같은지 확인한 결과가 `True`입니다.

## 4. 값 하나 바꿔 보기 — B 다음 A

등록 순서를 B 먼저로 바꿉니다. 실행 전에 예상해 봅니다. 들어가는 before_model 훅은 B가 먼저, 나오는 after_model 훅은 A가 먼저일 것입니다."""),
        code("""# B 다음 A 순서로 등록하고 같은 질문을 보냅니다
b_then_a = [b_before, b_wrap, b_after, a_before, a_wrap, a_after]
agent = create_agent(model, tools=[], middleware=b_then_a)
agent.invoke({"messages": [{"role": "user", "content": "한 문장으로 인사해 주세요."}]})
for number, name in enumerate(order, start=1):
    print(number, name)"""),
        md("""**결과 읽기** — 이번에는 1번이 `B before_model`이고 마지막 8번이 `B after_model`입니다. 바깥에서 감싸는 쪽도 B로 바뀌었습니다.

## 정리

- 들어가는 훅(before_model)은 등록 순서대로, 나오는 훅(after_model)은 반대 순서로 실행됩니다.
- 감싸기형 훅은 먼저 등록한 것이 바깥에서 감쌉니다.
- 종류가 다른 훅은 등록 순서와 상관없이 before → wrap → after 순서로 실행됐습니다."""),
    ]
    return "07-순서와-합성", "experiment", cells


def section_08() -> tuple[str, str, list[dict]]:
    cells = title_cells(
        "컨텍스트 분리와 Isolate",
        ["대출과 인사 두 업무가 섞인 대화 기록을 만듭니다.",
         "대화 전체를 모델에 보내고, 모델이 받은 메시지를 확인합니다(Before).",
         "현재 업무의 메시지만 골라 보내는 훅을 만들어 같은 대화를 보냅니다(After)."],
        "`.env` 파일의 `OPENAI_API_KEY`. 데이터 파일은 없습니다. 모델 호출은 3번이고 실행 시간은 1분 이내입니다. 예상 비용은 0.01달러 미만입니다.",
        "08-1-분리-전후.png", "섞인 대화에서 대출 업무 메시지만 골라 모델에 보내는 과정",
        "위는 저장된 대화 기록 다섯 개, 아래는 모델이 받은 메시지입니다. 분리 훅이 대출 메시지만 골라 보냅니다.",
    )
    cells += [
        md("이번 절에서 쓰는 이름을 불러옵니다."),
        setup("""# 에이전트·훅·메시지·모델을 만드는 도구를 불러옵니다
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage"""),
    ]
    cells += key_and_model_cells()
    cells += [
        md("""## 2. 업무가 섞인 대화 만들기

컨텍스트 분리(Isolate)는 대화 기록에서 지금 업무에 필요한 메시지만 골라 모델에 보내는 방법입니다. Ch8에서 배운 전략입니다.
메시지의 `additional_kwargs` 속성은 메시지에 추가 정보를 담아 두는 딕셔너리입니다.
여기에 업무 이름표 `topic`을 붙입니다. 이름표 중 loan은 대출, hr은 인사 업무입니다."""),
        code("""# 대출(loan)과 인사(hr) 업무가 섞인 대화 5개를 만듭니다
mixed = [
    HumanMessage("대출은 몇 권까지 되나요?", additional_kwargs={"topic": "loan"}),
    AIMessage("한 번에 5권까지 빌릴 수 있습니다.", additional_kwargs={"topic": "loan"}),
    HumanMessage("직원 급여 명세는 어디서 보나요?", additional_kwargs={"topic": "hr"}),
    AIMessage("급여 명세는 인사팀 내부 문서에 있습니다.", additional_kwargs={"topic": "hr"}),
    HumanMessage("대출 기간을 연장할 수 있나요?", additional_kwargs={"topic": "loan"}),
]
print("대화 메시지 수:", len(mixed))"""),
        md("""**결과 읽기** — 대화 메시지 수는 `5`입니다. 마지막 질문은 대출 업무입니다.

02절과 같은 기록 훅을 만듭니다."""),
        code(RECORD_INPUT),
        md("""출력은 없습니다.

## 3. Before — 대화 전체 보내기""", lesson_part="before"),
        code("""# Before: 대화 전체를 그대로 보냅니다
plain_agent = create_agent(model, tools=[], middleware=[record_model_input])
plain_agent.invoke({"messages": mixed})
for text in seen_by_model:
    print("-", text)""", lesson_part="before"),
        md("""**결과 읽기** — 모델이 받은 글 다섯 개 중에 `직원 급여 명세는 어디서 보나요?`가 있습니다. 대출 질문에 필요 없는 인사 업무 내용입니다.""", lesson_part="before"),
        code("""# 모델 입력에 인사 업무 내용이 섞였는지 확인합니다
has_salary = False
for text in seen_by_model:
    if "급여" in text:
        has_salary = True
print("모델 입력 메시지 수:", len(seen_by_model))
print("급여 내용이 섞였나:", has_salary)
assert has_salary""", lesson_part="before"),
        md("""**결과 읽기** — 모델 입력 메시지 수는 `5`, 급여 내용이 섞였는지 확인한 결과는 `True`입니다.

## 4. After — 현재 업무의 메시지만 보내기

지금 처리할 업무 이름을 변수에 담습니다.""", lesson_part="after"),
        code("""# 지금 처리할 업무 이름을 정합니다
current_topic = "loan"
print("현재 업무:", current_topic)""", lesson_part="after"),
        md("""**결과 읽기** — 현재 업무는 `loan`입니다.

분리 훅은 모델을 부르기 전에 메시지를 하나씩 보고, 이름표가 현재 업무와 같은 것만 새 목록에 담습니다.
메서드 `request.override(messages=selected)`는 요청의 메시지만 바꾼 새 요청을 만듭니다. 대화 기록에는 쓰지 않으므로 저장된 기록은 줄지 않습니다.""", lesson_part="after"),
        code("""# 현재 업무 이름표가 붙은 메시지만 골라 모델에 보내는 훅
@wrap_model_call
def isolate_topic(request: ModelRequest, handler: Callable) -> ModelResponse:
    selected = []
    for message in request.messages:
        if message.additional_kwargs.get("topic") == current_topic:
            selected.append(message)
    new_request = request.override(messages=selected)
    return handler(new_request)""", lesson_part="after"),
        md("""출력은 없습니다. 분리 훅을 기록 훅보다 앞에 두어야, 기록 훅이 고른 뒤의 메시지를 봅니다.""", lesson_part="after"),
        code("""# After: 분리 훅을 등록하고 같은 대화를 보냅니다
seen_by_model.clear()
isolated_agent = create_agent(model, tools=[], middleware=[isolate_topic, record_model_input])
isolated_result = isolated_agent.invoke({"messages": mixed})
for text in seen_by_model:
    print("-", text)""", lesson_part="after"),
        md("""**결과 읽기** — 모델이 받은 글이 대출 업무 세 개로 줄었습니다. 마지막 글은 `대출 기간을 연장할 수 있나요?`이고 급여 질문은 보이지 않습니다.""", lesson_part="after"),
        code("""# 모델이 받은 메시지 수와 저장된 대화 기록을 비교합니다
stored = isolated_result["messages"]
print("모델 입력 메시지 수:", len(seen_by_model))
print("저장된 대화 기록 수:", len(stored))
print("기록의 세 번째 메시지:", stored[2].text)
print("새 답의 topic 이름표:", stored[-1].additional_kwargs.get("topic"))
assert len(seen_by_model) == 3""", lesson_part="after"),
        md("""**결과 읽기** — 모델 입력 메시지 수는 `3`입니다. 저장된 대화 기록 수는 `6`입니다. 원래 5개에 새 답 1개가 더해졌습니다.
기록의 세 번째 메시지로 급여 질문이 그대로 남아 있습니다. 새 답의 이름표는 `None`, 즉 없습니다.

분리는 모델에 보내는 요청만 줄였고, 저장된 기록에서는 아무것도 지우지 않았습니다.

## 5. 값 하나 바꿔 보기 — 업무 이름 바꾸기

`current_topic` 값을 hr로 바꿉니다. 실행 전에 예상해 봅니다. 인사 업무 메시지 2개만 모델에 갈 것입니다.""", lesson_part="after"),
        code("""# 현재 업무를 인사(hr)로 바꿔 같은 대화를 보냅니다
current_topic = "hr"
seen_by_model.clear()
isolated_agent.invoke({"messages": mixed})
print("모델 입력 메시지 수:", len(seen_by_model))
for text in seen_by_model:
    print("-", text)""", lesson_part="after"),
        md("""**결과 읽기** — 모델 입력 메시지 수가 `2`입니다. 이번에는 대출 메시지가 빠지고 인사 업무 메시지만 남았습니다.

## 정리

- 분리 훅은 모델 요청에 들어갈 메시지만 골랐습니다. 저장된 대화 기록에서 지운 메시지는 없었습니다(5개에 새 답이 더해져 6개).
- 이름표(`topic`)를 붙여 두어야 코드로 업무를 구분할 수 있습니다.
- 모델 입력에서 빠졌다고 해서 접근이 막힌 것은 아닙니다. 급여 같은 내부 정보의 접근 권한은 별도로 관리해야 합니다.""", lesson_part="after"),
    ]
    return "08-컨텍스트-분리와-Isolate", "paired", cells


def section_09() -> tuple[str, str, list[dict]]:
    cells = title_cells(
        "Middleware 실습: 도서관 상담 에이전트",
        ["도서관 상담 에이전트가 쓸 도구 두 개와 기록 훅 네 개를 만듭니다.",
         "개인정보 가리기·호출 한도·감사 기록 미들웨어를 한 에이전트에 함께 등록해 대출 연장을 요청합니다(실행 1).",
         "호출 한도만 1로 낮춰 같은 요청을 보내고 결과를 비교합니다(실행 2)."],
        "`.env` 파일의 `OPENAI_API_KEY`. 데이터 파일은 없습니다. 모델 호출은 3번이고 실행 시간은 1분 이내입니다. 예상 비용은 0.01달러 미만입니다.",
        "09-1-조립도.png", "도서관 상담 에이전트에 붙인 미들웨어가 실행되는 자리",
        "위에서 아래로 읽습니다. 질문이 들어오면 감사 시작, 이메일 가리기, 호출 수 확인을 거쳐 모델이 호출됩니다.\n"
        "모델이 도구를 요청하면 도구 호출도 기록한 뒤 다시 모델 앞으로 돌아갑니다. 한도를 넘으면 감사 끝으로 갑니다.",
    )
    cells += [
        md("""이번 실습에서 쓰는 이름을 불러옵니다. 모두 01~08절에서 한 번씩 써 본 이름입니다.
새로 배우는 문법은 없습니다."""),
        setup("""# 에이전트·미들웨어·훅·도구·모델을 만드는 도구를 불러옵니다
import json
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import AgentState, ModelRequest, ModelResponse, Runtime, ToolCallRequest
from langchain.agents.middleware import ModelCallLimitMiddleware, PIIMiddleware
from langchain.agents.middleware import after_agent, before_agent, wrap_model_call, wrap_tool_call
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import ToolMessage"""),
    ]
    cells += key_and_model_cells()
    cells += [
        md("""## 2. 실습 주제 — 도서관 상담 에이전트

도서관 이용자의 질문에 답하는 상담 에이전트를 만듭니다. 여기에 이 챕터에서 배운 미들웨어 세 가지를 붙입니다.
02절의 이메일 가리기, 04절의 호출 한도, 06절의 감사 기록입니다.

먼저 에이전트가 쓸 도구를 만듭니다. 첫 번째 도구는 01절에서 쓴 운영 시간 도구입니다."""),
        code('''# 자료실 운영 시간을 알려 주는 도구를 만듭니다
@tool
def lookup_hours(day: str) -> str:
    """자료실 운영 시간을 조회합니다. day에는 "평일" 또는 "토요일"을 넣습니다."""
    if day == "평일":
        return "평일 09:00~20:00"
    return "토요일 10:00~17:00"


print("도구 이름:", lookup_hours.name)'''),
        md("""**결과 읽기** — 도구 이름 `lookup_hours`가 출력됩니다.

두 번째 도구는 대출 기간을 연장합니다. 실습용이므로 실제 도서관 시스템에 연결하지 않고 안내 문장만 만듭니다."""),
        code('''# 책 제목을 받아 대출 연장 안내를 돌려주는 도구를 만듭니다
@tool
def renew_loan(book_title: str) -> str:
    """빌린 책의 대출 기간을 7일 연장합니다. book_title에는 책 제목을 넣습니다."""
    return book_title + " 대출을 7일 연장했습니다."


print("도구 이름:", renew_loan.name)'''),
        md("""**결과 읽기** — 도구 이름 `renew_loan`이 출력됩니다. 모델은 질문을 보고 두 도구 중 필요한 것을 고릅니다.

## 3. 기록 훅 만들기

실행 결과를 확인하려면 기록이 필요합니다. 감사 사건을 담을 목록과, 모델이 받은 첫 메시지를 담을 목록을 만듭니다."""),
        code("""# 감사 사건과 모델 입력을 담을 빈 목록을 만듭니다
events = []
model_inputs = []
print("감사 사건 수:", len(events))
print("모델 입력 기록 수:", len(model_inputs))"""),
        md("""**결과 읽기** — 두 목록 모두 `0`개로 시작합니다.

06절처럼 에이전트가 시작할 때 사건을 남기는 훅을 만듭니다. 질문 원문 대신 글자 수만 적습니다."""),
        code("""# 에이전트가 시작할 때 질문의 글자 수를 기록하는 훅
@before_agent
def audit_start(state: AgentState, runtime: Runtime) -> None:
    first_text = state["messages"][0].text
    events.append({"event": "agent_start", "input_chars": len(first_text)})"""),
        md("""출력은 없습니다. 두 번째 감사 훅은 도구 호출을 감싸고 도구 이름을 기록합니다."""),
        code("""# 도구를 부를 때마다 도구 이름을 기록하는 훅
@wrap_tool_call
def audit_tool(request: ToolCallRequest, handler: Callable) -> ToolMessage:
    events.append({"event": "tool_call", "tool": request.tool_call["name"]})
    return handler(request)"""),
        md("""출력은 없습니다. 세 번째 감사 훅은 에이전트가 끝날 때 대화 기록의 메시지 수를 남깁니다."""),
        code("""# 에이전트가 끝날 때 메시지 수를 기록하는 훅
@after_agent
def audit_end(state: AgentState, runtime: Runtime) -> None:
    events.append({"event": "agent_end", "messages": len(state["messages"])})"""),
        md("""출력은 없습니다. 마지막 훅은 모델을 부를 때마다 모델이 받은 첫 메시지를 적습니다.
이 목록의 길이가 모델 호출 횟수이고, 첫 항목에서 이메일이 가려졌는지 볼 수 있습니다."""),
        code("""# 모델을 부를 때마다 모델이 받은 첫 메시지를 적는 훅
@wrap_model_call
def record_model_call(request: ModelRequest, handler: Callable) -> ModelResponse:
    model_inputs.append(request.messages[0].text)
    return handler(request)"""),
        md("""출력은 없습니다.

## 4. 미들웨어 모으기

02절에서 쓴 이메일 마스킹 미들웨어를 만듭니다. 모델에 보내는 입력에만 적용합니다."""),
        code("""# 이메일을 별표로 가리는 미들웨어를 만듭니다
email_mask = PIIMiddleware("email", strategy="mask", apply_to_input=True)
print("미들웨어 이름:", email_mask.name)"""),
        md("""**결과 읽기** — 미들웨어 이름에 `email`이 들어 있습니다.

04절의 호출 한도 미들웨어를 만듭니다. 대출 연장은 도구를 쓰므로 모델을 최소 두 번 부릅니다(04절).
그래서 한도를 넉넉하게 4로 둡니다.
그다음 미들웨어 여섯 개를 한 목록에 담아 에이전트를 만듭니다. 목록의 주석은 각 미들웨어를 배운 절입니다."""),
        code("""# 호출 한도 4의 미들웨어를 만들고, 미들웨어 여섯 개로 에이전트를 만듭니다
limit_four = ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")
tools = [lookup_hours, renew_loan]
middleware = [
    email_mask,  # 02절 이메일 가리기
    limit_four,  # 04절 호출 한도
    audit_start,  # 06절 감사 기록
    audit_tool,
    audit_end,
    record_model_call,  # 01·02절 모델 입력 기록
]
agent = create_agent(model, tools=tools, middleware=middleware)
print("등록한 도구 수:", len(tools))
print("등록한 미들웨어 수:", len(middleware))"""),
        md("""**결과 읽기** — 도구 `2`개와 미들웨어 `6`개를 등록했습니다.
02절에서 본 것처럼 이메일 가리기는 before_model 자리에서 실행됩니다.
그래서 07절 규칙대로 감싸기형 기록 훅은 가려진 글을 받습니다.

## 5. 실행 1 — 이메일이 든 대출 연장 요청

이용자가 이메일과 함께 대출 연장을 요청합니다. 실행 전에 예상해 봅니다.
모델은 `renew_loan` 도구를 고르고, 모델이 받은 글에서는 이메일이 가려져 있을 것입니다."""),
        code("""# 이메일이 든 대출 연장 요청을 보냅니다
request_text = "제 이메일은 learner@example.com 입니다. 『파이썬 첫걸음』 대출을 연장해 주세요."
result = agent.invoke({"messages": [{"role": "user", "content": request_text}]})
last_message = result["messages"][-1]
print("최종 답:", last_message.text)"""),
        md("""**결과 읽기** — 최종 답에 `7일 연장`이 들어 있습니다. 모델이 도구 결과를 읽고 답했습니다.
답 문장은 실행할 때마다 달라질 수 있습니다.

대화 기록을 종류별로 출력해 어떤 도구가 쓰였는지 봅니다."""),
        code("""# 대화 기록에 쌓인 메시지를 종류별로 출력합니다
for message in result["messages"]:
    print(message.type, "|", message.text)"""),
        md("""**결과 읽기** — 두 번째 줄의 ai 메시지는 글자가 비어 있습니다. 이 메시지가 도구를 요청했습니다.
도구 결과인 tool 메시지에 `대출을 7일 연장했습니다`가 있습니다. 첫 human 메시지의 이메일도 가려진 채 저장됐습니다.

이제 기록 훅이 남긴 모델 입력을 확인합니다."""),
        code("""# 모델 호출 횟수와 모델이 받은 첫 메시지를 확인합니다
print("모델 호출 횟수:", len(model_inputs))
print("모델이 받은 글:", model_inputs[0])
email_sent = "learner@example.com" in model_inputs[0]
print("모델 입력에 이메일 원문이 있나:", email_sent)
assert not email_sent"""),
        md("""**결과 읽기** — 모델 호출 횟수는 `2`입니다. 모델이 받은 글에는 `learner@****.com`이 보이고, 원문 확인 결과는 `False`입니다.
호출 2번은 한도 4 안이므로 호출 한도 미들웨어는 실행을 멈추지 않았습니다.

마지막으로 감사 기록을 확인합니다."""),
        code("""# 감사 사건을 출력하고, 기록에 이메일 원문이 없는지 확인합니다
for event in events:
    print(event)
saved_text = json.dumps(events, ensure_ascii=False)
print("감사 기록에 이메일 원문이 있나:", "learner@example.com" in saved_text)
assert events[0]["event"] == "agent_start"
assert events[-1]["event"] == "agent_end\""""),
        md("""**결과 읽기** — 사건이 `agent_start`, `tool_call`, `agent_end` 순서로 남았습니다. 도구 사건의 이름은 `renew_loan`입니다.
모델이 두 도구 중 대출 연장 도구를 골랐다는 뜻입니다. 운영 시간 도구는 이번 질문에 쓰이지 않았습니다.

감사 기록에 이메일 원문이 있는지 확인한 결과도 `False`입니다. 세 미들웨어가 한 에이전트에서 각자 제 역할을 했습니다.

## 6. 실행 2 — 호출 한도를 1로 낮추기

같은 요청을 호출 한도 1로 보냅니다. 나머지 미들웨어와 도구는 그대로입니다. 실행 전에 예상해 봅니다.
첫 호출에서 도구는 실행되지만, 도구 결과를 읽을 두 번째 모델 호출은 한도에 걸릴 것입니다."""),
        code("""# 기록을 비우고, 호출 한도만 1로 바꾼 에이전트로 같은 요청을 보냅니다
events.clear()
model_inputs.clear()
limit_one = ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")
middleware_one = [email_mask, limit_one, audit_start, audit_tool, audit_end, record_model_call]
agent_one = create_agent(model, tools=tools, middleware=middleware_one)
result_one = agent_one.invoke({"messages": [{"role": "user", "content": request_text}]})
print("최종 메시지:", result_one["messages"][-1].text)"""),
        md("""**결과 읽기** — 최종 메시지가 `Model call limits exceeded`로 시작하는 안내입니다. 04절에서 본 것과 같은 멈춤입니다."""),
        code("""# 실행 2의 대화 기록, 모델 호출 횟수, 감사 사건을 확인합니다
for message in result_one["messages"]:
    print(message.type, "|", message.text)
print("모델 호출 횟수:", len(model_inputs))
for event in events:
    print(event)
assert len(model_inputs) == 1"""),
        md("""**결과 읽기** — tool 메시지에 `대출을 7일 연장했습니다`가 있어 도구가 실행됐음을 알 수 있습니다.
모델 호출 횟수는 `1`입니다. 두 번째 호출은 기록 훅에 닿기 전에 멈췄습니다.
최종 답은 없었지만 감사 기록의 시작과 끝 사건은 그대로 남았습니다.

## 정리

- 이메일 가리기, 호출 한도, 감사 기록 미들웨어를 한 목록에 담아 한 에이전트에 함께 등록했습니다.
- 실행 1에서 모델 입력과 감사 기록 모두 이메일 원문이 없었고, 호출 2번은 한도 4 안이었습니다.
- 실행 2에서 한도 값 하나만 1로 바꾸자 도구 실행 뒤 두 번째 모델 호출에서 멈췄습니다. 감사 끝 사건은 남았습니다."""),
    ]
    return "09-Middleware-실습", "experiment", cells


SECTIONS = {"01": section_01, "02": section_02, "03": section_03, "04": section_04,
            "05": section_05, "06": section_06, "07": section_07, "08": section_08,
            "09": section_09}


def split_part_boundaries(cells: list[dict]) -> list[dict]:
    """결과 읽기와 다음 소제목이 한 셀에 있으면 lesson_part 경계에서 둘로 나눈다."""
    result = []
    previous_part = None
    for cell in cells:
        part = cell["metadata"].get("lesson_part")
        text = cell["source"]
        if cell["cell_type"] == "markdown" and part != previous_part and "\n\n## " in text:
            head, tail = text.split("\n\n## ", 1)
            head_meta = {key: value for key, value in cell["metadata"].items() if key != "lesson_part"}
            if previous_part is not None:
                head_meta["lesson_part"] = previous_part
            result.append(md(head, **head_meta))
            result.append(md("## " + tail, **cell["metadata"]))
        else:
            result.append(cell)
        if cell["cell_type"] == "code":
            previous_part = part
    return result


def write(number: str) -> Path:
    slug, lesson_format, cells = SECTIONS[number]()
    if lesson_format == "paired":
        cells = split_part_boundaries(cells)
    for index, cell in enumerate(cells):
        cell["id"] = f"s{number}-c{index:02d}"
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": lesson_format,
            "quality_upgrade": "2026-09-15",
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = LAB / f"{slug}.ipynb"
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    for number in sys.argv[1:]:
        print("wrote", write(number).name)
