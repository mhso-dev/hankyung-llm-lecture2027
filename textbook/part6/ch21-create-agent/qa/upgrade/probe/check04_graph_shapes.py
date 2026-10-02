"""04절 모델 없는 확인(요청 0): 1.x에 남은 옛 함수 create_react_agent와 새 함수 create_agent의 그래프 모양을 가짜 키 글자로 견준다.
사용: env -u OPENAI_API_KEY $ROOT/.cache/vm/venv-ch21-create-agent/bin/python check04_graph_shapes.py $ROOT/labs/part6/ch21-create-agent/notebooks
(2026-09-25 실행 — PYTHONHASHSEED 1·2·3·4·5·99에서 출력 md5 같음. 키 없이 모델 객체를 만들면 OpenAIError.)"""
import inspect, warnings, sys
sys.path.insert(0, sys.argv[1])
from typing import Literal
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from runner_tools import print_branches
POLICIES = {"대출": "a", "운영": "b", "연체": "c"}
@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다."""
    if topic not in POLICIES:
        raise ValueError("x")
    return POLICIES[topic]
class PolicyAnswer(BaseModel):
    topic: Literal["대출", "운영", "연체"] = Field(description="답의 근거가 된 규정의 주제어")
    answer: str = Field(description="찾은 규정 글에 근거한 한 문장 답")
try:
    m0 = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
    print("model without key: OK", type(m0).__name__)
except Exception as e:
    print("model without key: ERR", type(e).__name__, str(e)[:120])
model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", api_key="sk-not-a-real-key")
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    from langgraph.prebuilt import create_react_agent
print("warnings at import:", len(caught))
print("old params:", list(inspect.signature(create_react_agent).parameters))
print("new params:", list(inspect.signature(create_agent).parameters))
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    old = create_react_agent(model, tools=[lookup_policy])
    old_fmt = create_react_agent(model, tools=[lookup_policy], response_format=PolicyAnswer)
print("warnings at calls:", len(caught))
for w in caught:
    print("warn:", w.category.__name__, [c.__name__ for c in w.category.__mro__], "|", str(w.message), "|", w.filename, w.lineno)
new = create_agent(model, tools=[lookup_policy])
new_fmt = create_agent(model, tools=[lookup_policy], response_format=PolicyAnswer)
for name, g in [("old", old), ("old_fmt", old_fmt), ("new", new), ("new_fmt", new_fmt)]:
    b = g.builder
    print("==", name, type(g).__name__)
    print(" nodes:", list(b.nodes), "| edges:", sorted(b.edges), "| branches:", list(b.branches))
    print(" channels:", list(b.channels), "| managed:", list(getattr(b, "managed", {}).keys()))
    print(" input:", list(g.get_input_jsonschema()["properties"].keys()), "| output:", list(g.get_output_jsonschema()["properties"].keys()))
    print_branches(g)
    print(g.get_graph().draw_mermaid())
