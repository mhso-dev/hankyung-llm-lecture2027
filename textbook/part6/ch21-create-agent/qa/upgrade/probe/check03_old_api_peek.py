"""04절 인계용 모델 없는 확인(요청 0): 1.x에 남은 create_react_agent 그래프 모양만 본다."""
import warnings
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from pydantic import BaseModel
@tool
def lookup_policy(topic: str):
    """규정."""
    return topic
class PolicyAnswer(BaseModel):
    topic: str
model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", api_key="sk-not-a-real-key")
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    from langgraph.prebuilt import create_react_agent
    old = create_react_agent(model, tools=[lookup_policy])
    old_fmt = create_react_agent(model, tools=[lookup_policy], response_format=PolicyAnswer)
for w in caught:
    print("warn:", w.category.__name__, [c.__name__ for c in w.category.__mro__][:4], str(w.message)[:160])
new = create_agent(model, tools=[lookup_policy])
new_fmt = create_agent(model, tools=[lookup_policy], response_format=PolicyAnswer)
for name, g in [("old", old), ("old_fmt", old_fmt), ("new", new), ("new_fmt", new_fmt)]:
    print("==", name, type(g).__name__, "nodes:", list(g.builder.nodes), "channels:", list(g.builder.channels))
    print(g.get_graph().draw_mermaid().split("graph TD;")[1].split("classDef")[0].replace("\n", " ").replace("\t", ""))
    try:
        print("input keys:", list(g.get_input_jsonschema()["properties"].keys()))
    except Exception as e:
        print("input schema err", e)
