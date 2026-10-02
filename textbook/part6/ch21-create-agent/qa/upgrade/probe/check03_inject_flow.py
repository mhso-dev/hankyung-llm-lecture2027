"""03절 모델 없는 확인 2: create_agent 흐름 전체를 대본 모델(노트북 밖 확인용)로 실행해 컨텍스트가 도구에 들어가는지 본다. 요청 0."""
import warnings
from typing_extensions import TypedDict
from langchain.agents import AgentState, create_agent
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import ToolRuntime, tool
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

POLICIES = {"연체": "연체한 일수만큼 새 대출이 제한됩니다."}

class LibraryState(AgentState):
    ticket_no: str

class MemberContext(TypedDict):
    member_id: str
    overdue_days: int

@tool
def check_my_loan(runtime: ToolRuntime):
    """자료실 이용자 본인이 지금 새 책을 빌릴 수 있는지 확인합니다."""
    member = runtime.context["member_id"]
    days = runtime.context["overdue_days"]
    if days == 0:
        return "이용자 " + member + ": 연체가 없어 새 대출을 할 수 있습니다."
    return "이용자 " + member + ": 연체 " + str(days) + "일. " + POLICIES["연체"]

class ScriptModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self

def run(days):
    script = iter([
        AIMessage(content="", tool_calls=[{"name": "check_my_loan", "args": {}, "id": "call_s1", "type": "tool_call"}]),
        AIMessage(content="끝"),
    ])
    model = ScriptModel(messages=script)
    agent = create_agent(model, tools=[check_my_loan], system_prompt="x", state_schema=LibraryState, context_schema=MemberContext)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = agent.invoke({"messages": [HumanMessage(content="q")], "ticket_no": "Q-0925-01"},
                              context={"member_id": "M-0317", "overdue_days": days})
    print("warnings:", len(caught))
    for w in caught:
        print("  ", w.category.__name__, str(w.message)[:400].replace("\n", " / "), w.filename, w.lineno)
    print("keys:", list(result.keys()), result.get("ticket_no"))
    for m in result["messages"]:
        print("  ", type(m).__name__, getattr(m, "tool_calls", None), getattr(m, "status", None), m.content)

run(0)
run(3)
# 컨텍스트를 빼면?
script = iter([AIMessage(content="", tool_calls=[{"name": "check_my_loan", "args": {}, "id": "c", "type": "tool_call"}]), AIMessage(content="끝")])
agent = create_agent(ScriptModel(messages=script), tools=[check_my_loan], system_prompt="x", state_schema=LibraryState, context_schema=MemberContext)
try:
    r = agent.invoke({"messages": [HumanMessage(content="q")], "ticket_no": "Q"})
    print("no context:", [ (type(m).__name__, getattr(m,'status',None), m.content[:120]) for m in r["messages"]])
except Exception as e:
    print("no context error:", type(e).__name__, str(e)[:300])
