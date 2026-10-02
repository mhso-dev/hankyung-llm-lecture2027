import warnings
from dataclasses import dataclass
from typing_extensions import TypedDict
from pydantic import BaseModel
from langchain.agents import AgentState, create_agent
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import ToolRuntime, tool
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

class LibraryState(AgentState):
    ticket_no: str

class CtxTD(TypedDict):
    member_id: str
    overdue_days: int

@dataclass
class CtxDC:
    member_id: str
    overdue_days: int

class CtxBM(BaseModel):
    member_id: str
    overdue_days: int

class ScriptModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self

def make_tool(hint, reader):
    if hint is None:
        @tool
        def check_my_loan(runtime: ToolRuntime):
            """확인합니다."""
            return reader(runtime.context)
    else:
        @tool
        def check_my_loan(runtime: ToolRuntime[hint]):
            """확인합니다."""
            return reader(runtime.context)
    return check_my_loan

def td_read(c): return "M=" + c["member_id"]
def obj_read(c): return "M=" + c.member_id

def run(label, ctx_cls, ctx_val, generic, reader):
    t = make_tool(ctx_cls if generic else None, reader)
    script = iter([AIMessage(content="", tool_calls=[{"name": "check_my_loan", "args": {}, "id": "c1", "type": "tool_call"}]), AIMessage(content="끝")])
    agent = create_agent(ScriptModel(messages=script), tools=[t], system_prompt="x", state_schema=LibraryState, context_schema=ctx_cls)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        r = agent.invoke({"messages": [HumanMessage(content="q")], "ticket_no": "Q"}, context=ctx_val)
    print(label, "| warnings:", len(caught), "| tool:", r["messages"][2].content, "| args:", t.args)

run("TD plain", CtxTD, {"member_id": "M-0317", "overdue_days": 0}, False, td_read)
run("TD generic", CtxTD, {"member_id": "M-0317", "overdue_days": 0}, True, td_read)
run("DC plain", CtxDC, CtxDC(member_id="M-0317", overdue_days=0), False, obj_read)
run("DC generic", CtxDC, CtxDC(member_id="M-0317", overdue_days=0), True, obj_read)
run("BM plain", CtxBM, CtxBM(member_id="M-0317", overdue_days=0), False, obj_read)
run("BM generic", CtxBM, CtxBM(member_id="M-0317", overdue_days=0), True, obj_read)
