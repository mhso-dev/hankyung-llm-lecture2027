"""03절 모델 없는 확인: TypedDict 컨텍스트 + AgentState 확장 + ToolRuntime 주입 (요청 0, 가짜 키 글자)."""
import warnings
warnings.simplefilter("always")
from typing_extensions import TypedDict
from langchain.agents import AgentState, create_agent
from langchain.agents import middleware
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import ToolRuntime, tool
from langchain_core.utils.function_calling import convert_to_openai_tool
from langgraph.graph import StateGraph, START, END

POLICIES = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
}

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

print("same class:", AgentState is middleware.AgentState)
print("args:", check_my_loan.args)
spec = convert_to_openai_tool(check_my_loan)
print("spec:", spec)
model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", api_key="sk-not-a-real-key")
system_text = "x"
plain = create_agent(model, tools=[check_my_loan], system_prompt=system_text)
agent = create_agent(model, tools=[check_my_loan], system_prompt=system_text, state_schema=LibraryState, context_schema=MemberContext)
print("plain channels:", list(plain.builder.channels))
print("agent channels:", list(agent.builder.channels))
print("context_schema:", agent.builder.context_schema)
for source in agent.builder.branches:
    for name in agent.builder.branches[source]:
        print(source, name, list(agent.builder.branches[source][name].ends.values()))
print("nodes:", list(agent.builder.nodes))
print(agent.get_graph().draw_mermaid())
# 1) create_agent가 만든 ToolNode를 작은 그래프에 넣어 손으로 만든 요청으로 실행
tool_node = agent.builder.nodes["tools"].runnable
print("tool node type:", type(tool_node).__name__)
small = StateGraph(LibraryState, context_schema=MemberContext)
small.add_node("tools", tool_node)
small.add_edge(START, "tools")
small.add_edge("tools", END)
small_graph = small.compile()
call = {"name": "check_my_loan", "args": {}, "id": "call_hand_1", "type": "tool_call"}
state_in = {"messages": [HumanMessage(content="q"), AIMessage(content="", tool_calls=[call])], "ticket_no": "Q-1"}
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    out = small_graph.invoke(state_in, context={"member_id": "M-0317", "overdue_days": 0})
    print("small warnings:", len(caught), [str(w.category.__name__) + ":" + str(w.message)[:120] for w in caught])
print("small keys:", list(out.keys()), out["ticket_no"])
print("small tool msg:", out["messages"][-1].content, out["messages"][-1].status)
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    out = small_graph.invoke(state_in, context={"member_id": "M-0317", "overdue_days": 3})
    print("small warnings:", len(caught))
print("small tool msg 3:", out["messages"][-1].content)
