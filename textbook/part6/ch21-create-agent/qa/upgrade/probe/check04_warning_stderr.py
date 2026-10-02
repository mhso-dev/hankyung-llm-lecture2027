"""04절 노트북 밖 확인(요청 0): 경고를 모으지 않고 옛 함수를 부르면 셀 출력(stderr)에 임시 파일 위치가 함께 찍히는지 nbclient로 본다.
(2026-09-25 실행 — stderr 두 번, 각각 ipykernel 임시 파일 위치 + LangGraphDeprecatedSinceV10 경고 글.)"""
import nbformat, sys
from nbclient import NotebookClient
nb = nbformat.v4.new_notebook()
src1 = '''from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
@tool
def lookup_policy(topic: str):
    """규정."""
    return topic
model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", api_key="sk-not-a-real-key")'''
src2 = '''old_agent = create_react_agent(model, tools=[lookup_policy])
print("made")'''
nb.cells = [nbformat.v4.new_code_cell(src1), nbformat.v4.new_code_cell(src2), nbformat.v4.new_code_cell(src2)]
NotebookClient(nb, timeout=120, kernel_name="python3").execute()
for c in nb.cells[1:]:
    for o in c.outputs:
        print(o.get("name"), repr(o.get("text"))[:400])
