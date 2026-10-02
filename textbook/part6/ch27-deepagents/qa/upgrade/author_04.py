"""Ch 27 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_04.py            → 노트북 + _src 본문을 다시 쓴다(도구 파일은 쓰지 않음 — 02절 판 그대로, 노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_04.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  python3 -B author_04.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 실행용 — Ch 26 A-19 교훈)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**.
슬러그 `04-파일시스템과-중간-결과` 그대로(Part 6 목차와 03절 b8이 링크), 제목 「파일시스템과 중간 결과」 그대로.

## 결정 1 — M2: 앞 절반 모델 없음 + 뒤 절반 실제 모델 (챕터 리드 결정 1)

nbkit.key_and_model_cells("openai:gpt-5.4-mini") — temperature=0·reasoning_effort="none", 키는 루트 .env에서만(값 출력 없음).
2절은 디스크 백엔드(FilesystemBackend)를 직접 부르고(쓰기·운영체제로 보기·with open 읽기·파일 위치 규칙 둘),
3절은 손으로 만든 write_file 요청을 두 Deep Agent(기본 StateBackend ↔ FilesystemBackend)의 도구 실행 노드만 든 작은 그래프에 넣어
파일이 남는 자리(상태 칸 files ↔ 임시 폴더)를 견준다. 모두 모델을 부르지 않는 결정적 셀이다.
5절에서 디스크 백엔드 Deep Agent를 실제 모델로 한 번 실행한다(모델이 찾은 규정을 파일로 적는 장면). 가짜 채팅 모델 없음(규격 §3).

## 결정 2 — 파일 쓰기 자리 (챕터 리드 결정 3)

tempfile.mkdtemp(prefix="ch27-04-")로 만든 임시 폴더에만 쓴다(2·3절 work_folder 하나, 5절 run_folder 하나 — 실행마다 새로).
os.chdir 하지 않음(백엔드에 폴더를 직접 넘김). 실습 폴더 workspace*에 쓰지 않음. 임시 폴더 이름은 출력하지 않고 폴더 안 이름만.
노트북은 임시 폴더를 지우지 않는다(진단 삭제 승인 목록).

## 결정 3 — 안전 규칙 (가)·(나)와 요청 수 셈 (챕터 공통)

바깥 ModelCallLimitMiddleware(run_limit=10) — 03절 셀과 같은 글 + 같은 이름 general-purpose 명세(02절 셀과 같은 글, 한도 2).
상한 10 + task 부른 횟수 × 2. 요청 수 = 이번 실행이 더한 메시지만 잘라 sum_usage = 기록 훅(02절 record_tool_names와 같은 글) 요청 수.

## 결정 4 — 흔들림 먼저 확인 (qa/upgrade/04-probe.md)

노트북 밖 5번(요청 15번, §0은 첫 요청 전 13:28:11Z, 회차마다 새 임시 폴더): 구조 값(받은 도구 아홉·execute 없음, files 빈 목록,
디스크 글 == 요청 인자 글, 요청 수 == 훅 == 도구 요청 응답 + 1)·모델 판단 값(write_file 한 번 /notes/rules.md, task 0, 요청 3) 5/5 → 입력 그대로.
첫 응답의 lookup_rule 수 3 ↔ 4(운영까지)·메시지 수 8 ↔ 9·파일 글자 수는 흔들림 → 결론·그림에 넣지 않음. assert는 키 셀뿐.
흔들리는 값(메시지 수·lookup_rule 수·파일 글·토큰·비용)은 [[READ_…]] 자리 표시 → 교재 출력(A) 뒤 mdpatch.py.

## 결정 5 — 도구 파일 (챕터 리드 결정 6)

02절 판 harness_tools.py에서 함수 다섯을 가져온다(추가 0 — 도구 파일을 쓰지 않음). author_03.check_tools()(= 02절 대조 사슬 + 디스크 판이 02절 판으로 시작).
작은 그래프 함수 tools_only_graph는 이 절에서 처음 가르쳐 노트북에 둔다. 02·03절 셀과 같은 글(RULES·DEF_TOOL·HELPER_SPEC·DEF_HOOK·COST / OUTER_LIMIT)은
author_02·author_03 문자열 그대로 + 두 노트북 디스크 셀 대조.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·변수 힌트·대입 풀기·별표 풀기·
`while`·세미콜론·`isinstance`·클래스. `try`는 2절 `..` 셀 하나(Ch 2 05절 `try/except 이름 as error`, 받은 오류를 출력). 힌트는 @tool 매개변수 `: str`만(02절 셀),
데코레이터는 @tool과 @wrap_model_call(02절 셀)만. 호출 깊이 2 이하.
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
import author_03  # noqa: E402  03절 셀 글·도구 파일 대조 사슬
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch27-deepagents/notebooks"
FIGS = ROOT / "textbook/part6/ch27-deepagents/figures"
SLUG = "04-파일시스템과-중간-결과"
TITLE_TEXT = "파일시스템과 중간 결과"
SRC = ROOT / "textbook/part6/ch27-deepagents/_src" / (SLUG + ".html")
NB02 = LAB / "02-create-deep-agent와-도구.ipynb"
NB03 = LAB / "03-플래닝과-시스템-프롬프트.ipynb"
TOOLS_PATH = LAB / "harness_tools.py"
html_text = author_02.html_text
table_html = author_02.table_html
mermaid_block = author_02.mermaid_block
placeholder = author_02.placeholder


def check_tools() -> None:
    """04절은 도구 파일에 함수를 더하지 않습니다. 03절 대조 사슬(= 02절 사슬 + 디스크 판이 02절 판으로 시작)을 그대로 돌립니다."""
    author_03.check_tools()


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["deepagents==0.7.0", "langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3"])

IMPORTS = r'''# Deep Agents(01절)·백엔드와 상태 형식(이 절 처음)·미들웨어(Ch 22)·모델·메시지·도구·그래프 이름을 가져옵니다
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware.filesystem import FilesystemState, supports_execution
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_model_call
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
# 앞 챕터와 01절에서 배운 함수 다섯은 도구 파일에서 가져옵니다
from harness_tools import estimate_cost, show_messages, sum_usage, tool_call_names, tool_names

print("도구 파일에서 가져온 함수:", "estimate_cost, show_messages, sum_usage, tool_call_names, tool_names")'''

FOLDER = r'''# 파일을 쓸 빈 임시 폴더를 만듭니다(Ch 23 01절 모양 — 작업 위치는 옮기지 않음)
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고, 그 폴더의 위치를 글로 내놓습니다
work_folder = tempfile.mkdtemp(prefix="ch27-04-")
print("임시 폴더 이름에 ch27-04-가 들어 있는가:", "ch27-04-" in work_folder)
print("임시 폴더 안 이름:", os.listdir(work_folder))'''

DISK_BACKEND = r'''# 임시 폴더를 기준 폴더(root_dir)로 삼는 디스크 백엔드를 만듭니다(에이전트에는 아직 넘기지 않음)
disk_backend = FilesystemBackend(root_dir=work_folder)
print("백엔드 종류:", type(disk_backend).__name__)
print("virtual_mode 값:", disk_backend.virtual_mode)
print("명령을 실행할 수 있는가:", supports_execution(disk_backend))'''

DIRECT_WRITE = r'''# 중간 결과로 둘 규정 메모 글을 정하고, 백엔드의 메서드 write로 파일 위치 /notes/rules.md에 직접 씁니다
note_text = "# 규정 메모\n대출: 1인 5권까지 14일\n연장: 반납 예정일 전에 한 번, 7일\n연체: 연체한 일수만큼 새 대출 제한\n"
write_result = disk_backend.write("/notes/rules.md", note_text)
print("쓰기 결과 종류:", type(write_result).__name__)
print("오류:", write_result.error)
print("쓴 파일 위치:", write_result.path)'''

DISK_LIST = r'''# 운영체제 함수로 임시 폴더 안을 직접 봅니다(폴더 이름은 출력하지 않고, 폴더 안 이름만)
print("임시 폴더 안 이름:", os.listdir(work_folder))
# os.path.join은 폴더 위치와 이름을 운영체제에 맞는 구분 기호로 잇습니다
notes_folder = os.path.join(work_folder, "notes")
print("notes 폴더 안 이름:", os.listdir(notes_folder))'''

DISK_READ = r'''# 백엔드를 거치지 않고, Ch 2 05절처럼 with open으로 디스크의 파일을 직접 읽습니다
notes_file = os.path.join(notes_folder, "rules.md")
with open(notes_file, encoding="utf-8") as file:
    disk_text = file.read()
print("디스크 파일 글자 수:", len(disk_text))
print("쓴 글과 같은가:", disk_text == note_text)'''

PATH_ETC = r'''# 파일 위치 규칙 하나: 맨 앞 /는 컴퓨터의 맨 위 폴더가 아니라 기준 폴더를 뜻합니다
etc_result = disk_backend.write("/etc/rules.md", note_text)
print("쓴 파일 위치:", etc_result.path)
top_names = os.listdir(work_folder)
top_names.sort()
print("임시 폴더 안 이름:", top_names)'''

PATH_OUTSIDE = r'''# 파일 위치 규칙 둘: ..로 기준 폴더 밖을 가리키면, 쓰기 전에 오류로 막히는지 봅니다(Ch 2 05절 try/except)
try:
    disk_backend.write("../outside.md", note_text)
except ValueError as error:
    print("받은 오류:", type(error).__name__, "|", error)'''

DEF_GRAPH = r'''# Deep Agent 하나를 받아, 그 도구 실행 노드 하나만 든 작은 그래프를 만들어 내놓습니다(상태 형식은 files 칸이 있는 FilesystemState)
def tools_only_graph(agent):
    builder = StateGraph(FilesystemState)
    builder.add_node("tools", agent.nodes["tools"].bound)
    builder.add_edge(START, "tools")
    builder.add_edge("tools", END)
    return builder.compile()'''

AGENTS = r'''# 기본 백엔드와 디스크 백엔드로 Deep Agent를 하나씩 만들고, 작은 그래프를 하나씩 만듭니다(요청은 보내지 않음)
state_agent = create_deep_agent(model=model)
disk_agent = create_deep_agent(model=model, backend=disk_backend)
print("두 Deep Agent의 도구가 같은가:", tool_names(state_agent) == tool_names(disk_agent))
state_tools_graph = tools_only_graph(state_agent)
disk_tools_graph = tools_only_graph(disk_agent)
small_graph = state_tools_graph.get_graph()
print("작은 그래프의 노드:", list(small_graph.nodes))'''

HAND_REQUEST = r'''# 모델 없이, write_file 요청 하나를 담은 응답을 손으로 만듭니다(01절 6절 모양)
memo_args = {"file_path": "/drafts/memo.md", "content": note_text}
memo_call = {"name": "write_file", "args": memo_args, "id": "hand_write_1", "type": "tool_call"}
memo_request = AIMessage(content="", tool_calls=[memo_call])
print("요청한 도구:", tool_call_names(memo_request))'''

RUN_STATE = r'''# 기본 백엔드 쪽 작은 그래프에 넣고, 도구 메시지·상태 칸 files·임시 폴더 안을 봅니다
state_result = state_tools_graph.invoke({"messages": [memo_request]})
state_message = state_result["messages"][-1]
print("도구 메시지:", state_message.content, "|", state_message.status)
print("상태 칸 files의 파일 위치:", list(state_result["files"]))
top_names = os.listdir(work_folder)
top_names.sort()
print("임시 폴더 안 이름:", top_names)'''

STATE_ENTRY = r'''# 상태 칸 files에 든 파일 항목 하나의 칸 이름과 글을 봅니다(시각 칸의 값은 출력하지 않음)
memo_entry = state_result["files"]["/drafts/memo.md"]
print("파일 항목의 칸:", list(memo_entry))
print("쓴 글과 같은가:", memo_entry["content"] == note_text)'''

RUN_DISK = r'''# 값 바꿔 보기: 같은 요청을 디스크 백엔드 쪽 작은 그래프에 넣고 같은 것을 봅니다
disk_result = disk_tools_graph.invoke({"messages": [memo_request]})
disk_message = disk_result["messages"][-1]
print("도구 메시지:", disk_message.content, "|", disk_message.status)
print("상태 칸 files의 파일 위치:", list(disk_result["files"]))
top_names = os.listdir(work_folder)
top_names.sort()
print("임시 폴더 안 이름:", top_names)'''

RULES = author_02.RULES
DEF_TOOL = author_02.DEF_TOOL
OUTER_LIMIT = author_03.OUTER_LIMIT
HELPER_SPEC = author_02.HELPER_SPEC
DEF_HOOK = author_02.DEF_HOOK

RUN_FOLDER = r'''# 모델 실행에 쓸 새 임시 폴더와, 그 폴더를 기준 폴더로 삼는 디스크 백엔드를 만듭니다
run_folder = tempfile.mkdtemp(prefix="ch27-04-")
run_backend = FilesystemBackend(root_dir=run_folder)
print("새 임시 폴더 안 이름:", os.listdir(run_folder))'''

RUN_AGENT = r'''# 이 백엔드와 우리 도구·호출 한도·기록 훅·명세를 넘겨 Deep Agent를 만듭니다(요청은 아직 보내지 않음)
run_agent = create_deep_agent(
    model=model,
    tools=[lookup_rule],
    backend=run_backend,
    middleware=[outer_limit, record_tool_names],
    subagents=[helper_spec],
)
run_tools = tool_names(run_agent)
print("그래프에 등록된 도구 수:", len(run_tools))'''

RUN = r'''# 기록 목록을 새로 만들고, 규정을 찾아 파일에 적어 두라는 질문 한 줄로 한 번 실행합니다
seen_tool_lists = []
question = "교육센터 자료실의 대출, 연장, 연체 규정을 찾아, 찾은 규정 글을 /notes/rules.md 파일에 적어 두세요. 그다음 처음 온 학생에게 줄 안내문을 세 문장으로 써 주세요."
first_input = {"messages": [HumanMessage(content=question)]}
input_count = len(first_input["messages"])
run_result = run_agent.invoke(first_input)
run_messages = run_result["messages"]
print("결과 메시지 수:", len(run_messages))'''

SHOW = r'''# 결과 메시지를 차례로 봅니다(Ch 19 06절 함수 show_messages)
print("결과 메시지:")
show_messages(run_messages)'''

WRITTEN = r'''# 이번 실행이 더한 응답에서 write_file 요청의 인자를 모으고, 파일 위치를 봅니다
run_new = run_messages[input_count:]
written_args = []
for message in run_new:
    if type(message).__name__ == "AIMessage":
        for call in message.tool_calls:
            if call["name"] == "write_file":
                written_args.append(call["args"])
print("write_file 요청 수:", len(written_args))
for args in written_args:
    print("적으려 한 파일 위치:", args["file_path"])'''

WHERE = r'''# 디스크 백엔드 쪽 결과의 상태 칸 files와, 임시 폴더 안 이름을 봅니다
print("상태 칸 files의 파일 위치:", list(run_result["files"]))
run_names = os.listdir(run_folder)
run_names.sort()
print("임시 폴더 안 이름:", run_names)'''

DISK_FILE = r'''# 모델이 적은 파일 위치마다, 임시 폴더 안 실제 파일을 with open으로 읽어 요청 인자의 글과 견줍니다
for args in written_args:
    # 메서드 lstrip("/")은 파일 위치 맨 앞의 /를 떼어, 임시 폴더 안 상대 이름으로 만듭니다
    disk_path = os.path.join(run_folder, args["file_path"].lstrip("/"))
    print("임시 폴더 안에 파일이 있는가:", os.path.isfile(disk_path))
    if os.path.isfile(disk_path):
        with open(disk_path, encoding="utf-8") as file:
            run_text = file.read()
        print("요청 인자의 글과 같은가:", run_text == args["content"])'''

USAGE = r'''# 이번 실행이 더한 메시지만 Ch 19 05절 함수 sum_usage로 세고, 기록 훅이 센 요청 수·받은 도구와 견줍니다
run_usage = sum_usage(run_new)
print("응답으로 센 요청 수:", run_usage["requests"])
print("기록 훅이 센 요청 수:", len(seen_tool_lists))
print("받은 도구 수:", len(seen_tool_lists[0]))
print("execute를 받았는가:", "execute" in seen_tool_lists[0])
print("입력 토큰:", run_usage["input_tokens"], "| 출력 토큰:", run_usage["output_tokens"])'''

COST = author_02.COST


def check_same_as_prev() -> None:
    """02·03절 셀과 같은 글이라고 적는 셀이 두 노트북 디스크 셀과 글자 그대로 같은지 봅니다."""
    sources_02 = author_02.notebook_code_sources(NB02)
    for cell in [RULES, DEF_TOOL, HELPER_SPEC, DEF_HOOK, COST]:
        assert cell in sources_02, cell.splitlines()[0]
    sources_03 = author_02.notebook_code_sources(NB03)
    assert OUTER_LIMIT in sources_03, "OUTER_LIMIT가 03 노트북 셀과 다릅니다"


def check_same_as_probe() -> None:
    """노트북 셀의 규정 글·도구·명세·한도·훅·백엔드·에이전트·질문이 흔들림 확인 스크립트(probe04.py)와 같은 글인지 봅니다."""
    probe = (HERE / "probe/probe04.py").read_text(encoding="utf-8")
    pieces = []
    skip = ("#", "print(", "run_tools")
    for cell in [RULES, DEF_TOOL, HELPER_SPEC, OUTER_LIMIT, DEF_HOOK, RUN_FOLDER, RUN_AGENT]:
        for line in cell.splitlines():
            if line.startswith(skip):
                continue
            pieces.append(line)
    pieces.append('model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")')
    for piece in pieces:
        assert piece in probe, piece
    question_line = RUN.splitlines()[2]
    assert question_line.replace("question = ", "QUESTION = ") in probe


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/04-figures.md)
FIG1 = "04-1-같은-요청-두-자리"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 손으로 만든 요청 write_file 파일 위치 /drafts/memo.md에서 나란한 두 칸으로 화살표가 갑니다. 왼쪽 칸 기본 백엔드 StateBackend에는 노란 상자 상태 칸 files에 /drafts/memo.md와 노란 상자 임시 폴더 안 drafts 없음이 위아래로 있습니다. 오른쪽 칸 디스크 백엔드 FilesystemBackend에는 노란 상자 상태 칸 files 빈 목록과 노란 상자 임시 폴더 안 drafts 폴더와 파일이 생김이 있는 그림"
FIG1_CAP = "같은 write_file 요청이 기본 백엔드에서는 상태 칸 files에, 디스크 백엔드에서는 임시 폴더의 파일로 남았습니다."
FIG1_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자는 모델 없이 손으로 만든 요청이고, 노란 상자는 노트북 3절 출력입니다.
두 칸은 백엔드만 바꾼 서로 다른 설정이라 나란히 두었습니다.
두 칸 모두 도구 메시지는 같았고, 파일이 남은 자리만 달랐습니다."""

FIG2 = "04-2-파일-위치-규칙"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 파란 상자 FilesystemBackend 기준 폴더는 임시 폴더 virtual_mode True에서 초록 상자 셋으로 화살표가 갑니다. 초록 상자는 파일 위치 /notes/rules.md, /etc/rules.md, ../outside.md입니다. 각각 아래 노란 상자 임시 폴더 안 notes/rules.md, 임시 폴더 안 etc/rules.md 컴퓨터의 /etc 아님, 받은 오류 ValueError 쓰기 전에 막힘으로 이어지는 그림"
FIG2_CAP = "맨 앞 /는 기준 폴더를 뜻해 /etc/rules.md도 임시 폴더 안에 생겼고, ..가 든 파일 위치는 쓰기 전에 ValueError로 막혔습니다."
FIG2_READ = """위에서 아래로 읽습니다.
파란 상자는 우리가 만든 백엔드 객체, 초록 상자는 우리가 넘긴 파일 위치입니다.
노란 상자는 노트북 2절 출력이고, 초록 상자와 노란 상자는 위아래로 한 쌍씩 짝을 이룹니다.
오류 상자도 코드가 받아 출력한 오류라 노란색입니다."""

FIG3 = "04-3-파일을-적는-실행"
FIG3_ALT = "세로선 넷이 있는 차례 그림입니다. 왼쪽부터 우리 코드, 그래프, 임시 폴더, 연보라 띠 안의 모델 gpt-5.4-mini입니다. 우리 코드에서 질문 한 줄로 invoke 화살표가 그래프로 갑니다. 그래프에 노란 메모 기록 훅 받은 도구 아홉 execute 없음이 붙습니다. 요청 1 화살표가 모델로 가고 lookup_rule 요청 한 응답에 함께 점선이 돌아옵니다. 요청 2에는 write_file 요청 하나 점선이 돌아오고, 그래프에서 임시 폴더로 notes/rules.md를 씀 화살표가 갑니다. 요청 3에는 도구 요청 없음 답 글 점선이 돌아오고, 결과 메시지와 상태 칸 files 빈 목록 점선이 우리 코드로 돌아오는 그림"
FIG3_CAP = "이번 실행에서 모델은 규정을 한 응답에 함께 찾고 write_file을 한 번 불렀으며, 파일은 임시 폴더에만 생겼습니다."
FIG3_READ = """위에서 아래로 실행 차례대로 읽고, 세로선은 왼쪽부터 우리 코드, 그래프, 임시 폴더, 모델입니다.
연보라 띠는 실제로 부른 모델 gpt-5.4-mini의 자리이고, 노란 메모는 노트북 5·6절 출력입니다.
첫 응답에 lookup_rule 요청이 몇 개 들었는지는 실행마다 달라 그리지 않았습니다."""

FIG4 = "04-4-같은-글이-남은-두-자리"
FIG4_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 보라 상자 모델의 응답 write_file 요청 하나에서 나란한 두 칸으로 화살표가 갑니다. 왼쪽 칸 이번 실행의 메시지 목록에는 노란 상자 응답의 도구 호출 인자 content 글과 노란 상자 도구 메시지 Updated file이 있습니다. 오른쪽 칸 메시지 목록 밖에는 노란 상자 임시 폴더 안 notes/rules.md 요청 인자의 글과 같음 True와 노란 상자 상태 칸 files 빈 목록이 있습니다. 맨 아래 회색 상자 셈 요청 수는 도구를 요청한 응답 수 더하기 1이 있는 그림"
FIG4_CAP = "모델이 write_file로 적은 글은 임시 폴더의 파일에도, 이번 실행의 메시지 목록에도 남았고, 상태 칸 files는 비어 있었습니다."
FIG4_READ = """위에서 아래로 읽습니다.
보라 상자는 실제로 부른 모델의 응답이고, 노란 상자는 노트북 5·6절 출력입니다.
두 칸은 같은 글이 남은 서로 다른 자리라 나란히 두었습니다.
맨 아래 회색 상자는 두 커널과 흔들림 확인에서 모두 맞은 셈이고, 요청 수 자체는 그리지 않았습니다."""

ILLU = "04-5-온실과-헛간의-모종판"
ILLU_ALT = "흰 바탕의 그림이 좌우 두 쪽으로 나뉩니다. 왼쪽은 유리 온실 안이고, 벽에 단 나무 선반 위에 두 줄 네 칸짜리 모종판 하나가 있습니다. 칸마다 작은 새싹이 하나씩 났습니다. 오른쪽은 문이 열린 나무 헛간 안이고, 벽에 단 나무 선반 위에 같은 모양의 모종판 하나가 있습니다. 헛간 모종판의 오른쪽 끝 칸은 문틀에 조금 가려 있습니다. 사람·손·연장·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "같은 모양의 모종판이 하나는 온실 안 선반에, 하나는 온실 밖 헛간 선반에 놓여 있습니다."
ILLU_READ = "그림은 좌우 두 쪽입니다. 왼쪽 유리 온실 안 벽 선반과 오른쪽 나무 헛간 안 벽 선반에 같은 모양의 모종판이 하나씩 놓여 있습니다. 온실 안 모종판이 기본 백엔드의 상태 칸 <code>files</code>, 헛간 모종판이 디스크 백엔드의 기준 폴더에 둔 파일입니다. 헛간 쪽 모종판은 오른쪽 끝 칸이 문틀에 조금 가렸지만, 두 모종판은 같은 모양입니다. 칸 수와 새싹 수는 어떤 값과도 짝짓지 않고, 새싹이 자란 모습이 걸린 시간을 뜻하지도 않습니다."

RUNS_SENTENCE = '새 커널로 두 번 실행해 견주자, 코드 셀 서른하나의 출력이 셀마다 모두 같았습니다. 메시지 수·토큰·예상 비용이 찍힌 셀도 이번 두 번에서는 같았지만, 노트북 밖에서는 달랐던 값이라 결론에는 쓰지 않습니다.'

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 디스크에 쓰는 백엔드로 임시 폴더에 파일을 쓰고, 파일 위치 규칙을 모델 없이 봅니다.
2. 같은 파일 쓰기 요청이 두 백엔드에서 어디에 남는지, 상태 칸과 임시 폴더를 견줍니다.
3. 실제 모델이 찾은 규정을 파일에 적어 두는 실행을 한 번 보고, 요청 수를 셉니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 5절에서 Deep Agent를 한 번 실행합니다.
노트북 밖에서 같은 질문을 다섯 번 보냈을 때, 요청은 다섯 번 모두 3번이었습니다.
바깥 호출 한도 10과 서브에이전트 호출 한도 2를 주어, 요청이 끝없이 늘지 않게 막습니다.
요금표로 어림한 예상 비용은 0.01달러 아래이고, 청구 금액이 아닙니다.

파일은 실행할 때마다 새로 만드는 임시 폴더에만 씁니다.
실습 폴더에는 파일을 쓰지 않고, 노트북은 임시 폴더를 지우지 않습니다.
모델이 파일에 적는 글과 답 글은 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.
앞에서 배운 함수 다섯은 도구 파일 `harness_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 deepagents 0.7.0, langchain 1.4.0, langgraph 1.2.11입니다.
나머지 둘은 `langchain-openai` 1.6.0과 `python-dotenv` 1.2.3입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2·3절을 읽습니다.
파일이 어디에 생기는지를 모델 없이 보는 자리입니다.
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
다음 셀은 파일을 쓸 빈 임시 폴더를 Ch 23 01절처럼 만듭니다.
Ch 23과 달리 작업 위치는 옮기지 않습니다.
파일을 둘 폴더는 백엔드에 직접 넘겨 정하기 때문입니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절에서는 02절에서 정의한 백엔드를 바꿔 가며, 파일 도구가 쓴 파일이 어디에 남는지 봅니다.
중간 결과는 긴 일을 하는 도중에 만들어, 나중에 다시 쓸 값입니다.
이 절에서는 찾은 규정을 적어 둔 메모가 중간 결과입니다.

첫 셀은 패키지 다섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `deepagents: 0.7.0`과 `langgraph: 1.2.11`이 보입니다.
다섯 판 모두 실습 폴더 잠금과 같은 판입니다.
패키지 langgraph는 3절에서 작은 그래프를 직접 만들려고 설치 목록에 넣었습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
백엔드 `FilesystemBackend`와 상태 형식 `FilesystemState`는 이 절에서 처음 씁니다.
함수 `supports_execution`과 `wrap_model_call`은 02절처럼 씁니다.
마지막 가져오기 줄은 앞에서 배운 함수 다섯을 도구 파일 `harness_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, show_messages, sum_usage, tool_call_names, tool_names`가 보입니다.
다섯 함수의 뜻은 02절 1절에 적었습니다.
앞에서 배운 함수는 `harness_tools.py`에 모아 두었고, 파일을 열면 코드를 볼 수 있습니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다."""),
    ] + model_cells() + [
        setup(FOLDER),
        md("""**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch27-04-가 들어 있는가: True`가 보입니다.
라벨 `임시 폴더 안 이름:` 뒤는 빈 목록이라, 빈 폴더를 새로 만들었습니다.
폴더 위치는 컴퓨터마다 달라 출력하지 않고, 폴더 안 이름만 봅니다.
실행할 때마다 새 폴더가 생기므로, 이 노트북이 쓴 파일만 보입니다.

## 2. 디스크에 쓰는 백엔드를 직접 부르기

02절에서 백엔드는 파일 도구가 파일을 실제로 두는 자리를 정하는 부품이라고 했습니다.
기본 백엔드 `StateBackend`는 파일을 그래프 상태 안에 두고, 디스크에는 쓰지 않습니다.
이 절에서 처음 쓰는 백엔드 `FilesystemBackend`는 컴퓨터 디스크의 폴더에 실제 파일을 씁니다.

백엔드가 파일 위치의 맨 앞 `/`로 삼는 폴더를 기준 폴더라고 부르겠습니다.
아파트 안내문의 「101호」가 그 아파트 안의 101호를 뜻하는 것과 같습니다.
이 절 코드에서는 인자 `root_dir=`에 넘긴 임시 폴더가 기준 폴더입니다.
다음 셀은 이 백엔드를 만들고, 설정 두 가지를 봅니다."""),
        code(DISK_BACKEND),
        md("""**결과 읽기** — 출력 줄 `백엔드 종류: FilesystemBackend`와 `virtual_mode 값: True`가 보입니다.
설정 `virtual_mode`의 기본값 `True`는 파일 위치를 기준 폴더 아래로 묶는 설정입니다.
출력 줄 `명령을 실행할 수 있는가: False`도 보입니다.
이 백엔드도 명령을 실행하지 못해, 02절처럼 모델이 받는 목록에서 `execute`가 빠질 것입니다.

다음 셀은 중간 결과로 둘 규정 메모 글을 정하고, 백엔드에 직접 씁니다.
파일 도구 없이 백엔드만 부르는 모양입니다.
메서드 `write`는 파일 위치와 글을 받아, 결과 객체 하나를 내놓습니다."""),
        code(DIRECT_WRITE),
        md("""**결과 읽기** — 출력 줄 `쓰기 결과 종류: WriteResult`와 `오류: None`이 보입니다.
결과 객체의 칸 `error`가 `None`이면 쓰기에 성공한 것입니다.
출력 줄 `쓴 파일 위치: /notes/rules.md`는 우리가 넘긴 파일 위치 그대로입니다.
설치판 `backends/filesystem.py` 495~530행에서, 없는 폴더는 백엔드가 먼저 만듭니다.

다음 셀은 운영체제 함수로 임시 폴더 안을 직접 봅니다.
함수 `os.listdir`는 Ch 23 01절처럼 폴더 안 이름 목록을 내놓습니다.
함수 `os.path.join`은 폴더 위치와 이름을 운영체제에 맞는 구분 기호로 잇습니다."""),
        code(DISK_LIST),
        md("""**결과 읽기** — 출력 줄 `임시 폴더 안 이름: ['notes']`와 `notes 폴더 안 이름: ['rules.md']`가 보입니다.
파일 위치 `/notes/rules.md`가 기준 폴더 안 `notes/rules.md`가 되었습니다.

다음 셀은 백엔드를 거치지 않고, Ch 2 05절에서 배운 `with open`으로 그 파일을 읽습니다.
백엔드 밖에서도 읽힌다면, 디스크에 실제 파일이 있다는 뜻입니다."""),
        code(DISK_READ),
        md("""**결과 읽기** — 출력 줄 `디스크 파일 글자 수: 67`과 `쓴 글과 같은가: True`가 보입니다.
백엔드가 쓴 파일을 보통의 파일 읽기로 그대로 읽었습니다.
이 파일은 노트북을 닫아도 임시 폴더에 남습니다.

이제 파일 위치 규칙을 둘 봅니다.
Linux·macOS 컴퓨터에서 `/etc`는 맨 위 폴더 바로 아래의 설정 폴더입니다.
다음 셀은 파일 위치 `/etc/rules.md`에 써 보고, 파일이 어디에 생기는지 봅니다.
실행 전에 예상해 봅니다."""),
        code(PATH_ETC),
        md("""**결과 읽기** — 출력 줄 `쓴 파일 위치: /etc/rules.md`와 `임시 폴더 안 이름: ['etc', 'notes']`가 보입니다.
컴퓨터의 `/etc`가 아니라, 기준 폴더 안에 `etc` 폴더가 새로 생겼습니다.
설정 `virtual_mode`가 `True`이면 파일 위치의 맨 앞 `/`는 기준 폴더를 뜻합니다.
메서드 `sort`로 이름을 가나다·알파벳 차례로 맞춰, 출력 차례가 컴퓨터마다 달라지지 않게 했습니다.

파일 위치에 `..`를 넣으면 한 단계 위 폴더, 곧 기준 폴더 밖을 가리킵니다.
다음 셀은 그런 파일 위치로 써 보고, 받은 오류를 출력합니다.
Ch 2 05절처럼 `try`·`except`로 그 오류 이름만 받아, 셀은 끝까지 실행됩니다."""),
        code(PATH_OUTSIDE),
        md("""**결과 읽기** — 출력 줄 `받은 오류: ValueError | Path traversal not allowed`가 보입니다.
영어 글은 위 폴더로 거슬러 오르는 파일 위치를 허용하지 않는다는 뜻입니다.
설치판 `backends/filesystem.py` 202~206행에서, 백엔드는 파일을 쓰기 전에 이 오류를 냅니다.
그래서 기준 폴더 밖에는 아무것도 쓰지 않았습니다.

## 3. 같은 요청을 두 백엔드에 넣어 보기

이번에는 백엔드를 직접 부르지 않고, Deep Agent의 파일 도구 `write_file`을 부릅니다.
모델 없이 도구를 부르려고, 01절 6절처럼 도구 실행 노드만 든 작은 그래프를 만듭니다.
상태 형식은 01절과 달리 Deep Agents가 준 `FilesystemState`를 씁니다.
이 형식은 Ch 21 03절의 라이브러리 상태 형식 `AgentState`에 파일 칸 `files`를 더한 것입니다.
기본 백엔드는 파일을 이 칸에 쓰므로, 칸이 없는 상태 형식으로는 받을 수 없습니다.

다음 셀은 Deep Agent 하나를 받아, 그 도구 실행 노드만 든 작은 그래프를 내놓는 함수입니다.
01절 6절 셀의 흐름을 함수 하나로 묶었습니다."""),
        code(DEF_GRAPH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
속성 `agent.nodes["tools"].bound`는 01절에서 본 도구 실행 노드입니다.
도구 실행 노드는 그래프 밖에서 따로 부를 수 없어, 이렇게 작은 그래프에 넣어 부릅니다.

다음 셀은 기본 백엔드와 디스크 백엔드로 Deep Agent를 하나씩 만듭니다.
인자 `backend=`에 2절의 디스크 백엔드 객체를 그대로 넘깁니다.
두 Deep Agent의 도구 실행 노드로 작은 그래프도 하나씩 만듭니다."""),
        code(AGENTS),
        md("""**결과 읽기** — 출력 줄 `두 Deep Agent의 도구가 같은가: True`가 보입니다.
백엔드를 바꿔도 도구 이름은 그대로이고, 바뀌는 것은 파일을 두는 자리뿐입니다.
라벨 `작은 그래프의 노드:` 뒤에는 시작과 끝 사이에 `tools` 하나만 있습니다.

다음 셀은 모델 없이 `write_file` 요청 하나를 담은 응답을 손으로 만듭니다.
Ch 20 01절과 01절 6절처럼, 칸 `name`·`args`·`id`·`type`을 적은 딕셔너리를 넣습니다.
파일 위치는 2절과 다른 `/drafts/memo.md`로 정해, 새로 생기는 폴더가 보이게 했습니다."""),
        code(HAND_REQUEST),
        md("""**결과 읽기** — 출력 줄 `요청한 도구: ['write_file']`이 보입니다.
응답 하나에 도구 요청 하나를 담았습니다.

호출 ID `hand_write_1`과 글 `note_text`는 우리가 정한 값입니다.
다음 셀은 이 요청을 기본 백엔드 쪽 작은 그래프에 넣습니다.
실행 전에 예상해 봅니다.
기본 백엔드라면 파일은 상태 칸 `files`에 들어가고, 임시 폴더는 그대로일 것입니다."""),
        code(RUN_STATE),
        md("""**결과 읽기** — 출력 줄 `도구 메시지: Updated file /drafts/memo.md | success`가 보입니다.
출력 줄 `상태 칸 files의 파일 위치: ['/drafts/memo.md']`에서, 파일은 상태 칸에 들어갔습니다.
출력 줄 `임시 폴더 안 이름: ['etc', 'notes']`는 앞과 같아, `drafts` 폴더는 생기지 않았습니다.
설치판 `backends/state.py` 98~122행에서, 기본 백엔드는 디스크 대신 그래프의 `files` 칸에 씁니다.

다음 셀은 상태 칸 `files`에 든 파일 항목 하나를 봅니다."""),
        code(STATE_ENTRY),
        md("""**결과 읽기** — 출력 줄 `파일 항목의 칸: ['content', 'encoding', 'created_at', 'modified_at']`이 보입니다.
칸 `content`가 글이고, `encoding`은 글자를 적는 방식입니다.
나머지 두 칸은 만든 시각과 고친 시각이라, 실행마다 달라져 값을 출력하지 않았습니다.
출력 줄 `쓴 글과 같은가: True`로, 상태 칸에 우리 글이 그대로 들어간 것을 봅니다.

### 값 바꿔 보기: 디스크 백엔드

바꿀 값은 작은 그래프의 백엔드 하나이고, 넣는 요청은 같습니다.
실행 전에 예상해 봅니다.
디스크 백엔드라면 상태 칸 `files`는 비고, 임시 폴더에 `drafts` 폴더가 생길 것입니다."""),
        code(RUN_DISK),
        md("""**결과 읽기** — 출력 줄 `도구 메시지: Updated file /drafts/memo.md | success`는 앞 셀과 같습니다.
출력 줄 `상태 칸 files의 파일 위치: []`에서, 상태 칸은 비어 있습니다.
출력 줄 `임시 폴더 안 이름: ['drafts', 'etc', 'notes']`에서, `drafts` 폴더가 새로 생겼습니다.
같은 요청이 같은 도구 메시지를 냈지만, 파일이 남은 자리는 백엔드에 따라 달랐습니다.

## 4. 실제 모델을 부를 준비

5절에서는 02절의 자료실 규정 도구로, 모델이 찾은 규정을 파일에 적게 합니다.
다음 셀은 02절 2절의 규정 글 셀과 같은 글입니다."""),
        code(RULES),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '연장', '연체', '운영']`이 보입니다.
02절과 같은 교재용 규정이고, 실제 도서관 규정이 아닙니다.

다음 셀도 02절의 도구 셀과 같은 글입니다.
맨 위 `@tool` 줄이 아래 함수를 도구로 등록하는 것도 02절과 같습니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 `lookup_rule`은 주제어 하나로 규정 글 하나를 찾고, 없는 주제어에는 넣을 수 있는 주제어를 알려 주는 정해 둔 글을 내놓습니다.

다음 셀은 03절 셀과 같은 글의 바깥 호출 한도입니다.
규정을 찾고, 파일에 적고, 답하는 흐름이라 02절의 3보다 넉넉한 10을 그대로 씁니다."""),
        code(OUTER_LIMIT),
        md("""**결과 읽기** — 출력 줄 `바깥 호출 한도: 10`이 보입니다.
주석의 「02절 셀과 한도만 다름」은 이 셀을 처음 쓴 03절에서 적은 말입니다.

다음 셀은 02절과 같은 글의 general-purpose 명세이고, 자기 호출 한도는 2입니다.
01절에서 본 것처럼 바깥 호출 한도는 이 서브에이전트로 옮겨 가지 않아, 두 곳에 따로 줍니다."""),
        code(HELPER_SPEC),
        md("""**결과 읽기** — 출력 줄 `명세의 키: ['name', 'description', 'system_prompt', 'middleware']`가 보입니다.
한 번 실행의 모델 요청은 10에, 도구 `task`를 부른 횟수 × 2를 더한 값을 넘지 않습니다.

다음 셀은 02절과 같은 글의 기록 훅입니다.
모델 요청이 나갈 때마다, 모델이 받은 도구 이름을 기록 목록 `seen_tool_lists`에 붙입니다."""),
        code(DEF_HOOK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
기록 목록은 실행 셀에서 새로 만듭니다.
이 훅은 바깥 인자 `middleware=`에만 넣어, general-purpose의 요청은 적지 않습니다.

## 5. 모델이 중간 결과를 파일로 적는 실행

모델 실행에는 2·3절과 다른 새 임시 폴더를 씁니다.
모델이 쓴 파일만 보이게 하려는 것입니다."""),
        code(RUN_FOLDER),
        md("""**결과 읽기** — 라벨 `새 임시 폴더 안 이름:` 뒤는 빈 목록입니다.
이 폴더가 5절 디스크 백엔드의 기준 폴더입니다.

다음 셀은 이 백엔드와 4절의 부품을 넘겨 Deep Agent를 만듭니다.
02절 `rule_agent`와 같은 모양에 인자 `backend=`를 더했고, 바깥 한도는 03절의 10입니다."""),
        code(RUN_AGENT),
        md("""**결과 읽기** — 출력 줄 `그래프에 등록된 도구 수: 10`이 보입니다.
기본 도구 아홉과 우리 도구 하나이고, 02절 `rule_agent`와 같은 수입니다.

질문은 규정 셋을 찾아 파일 `/notes/rules.md`에 적어 두고, 안내문을 쓰라는 글입니다.
파일 위치를 질문이 정해 준 것은 흐름을 보여 주려고 실행 전에 정한 예입니다.
실행 전에 예상해 봅니다.
모델은 규정을 찾은 뒤 `write_file`로 메모를 적고, 도구 요청 없는 답으로 끝낼 것입니다."""),
        code(RUN),
        md("""**결과 읽기** — 라벨 `결과 메시지 수:` 뒤에 이번 실행의 메시지 수가 보입니다.
넣은 질문 하나 뒤에 모델 응답과 도구 메시지가 더해졌습니다.

이번 실행에서는 `결과 메시지 수: 8`이었습니다.
모델이 규정을 몇 개 함께 찾았는지에 따라 달라지는 값입니다.
노트북 밖 다섯 번에서는 여덟이 세 번, 아홉이 두 번이었습니다.
새 커널로 한 번 더 실행했을 때도 여덟이었습니다.

다음 셀은 결과 메시지를 Ch 19 06절 함수 `show_messages`로 봅니다."""),
        code(SHOW),
        md("""**결과 읽기** — 라벨 줄 아래 둘째 줄이 첫 응답이고, 도구 호출 요청에는 `lookup_rule`만 들어 있습니다.
그 뒤 응답 줄 `AIMessage | 도구 호출 요청: ['write_file']`이 모델이 파일을 적으려 한 자리입니다.
바로 아래 줄 `ToolMessage | 결과 상태: success | 내용: Updated file /notes/rules.md`가 도구 결과입니다.
마지막 줄은 도구 요청이 없는 답입니다.

이번 실행에서 첫 응답은 `lookup_rule`을 세 번 함께 요청했고, 주제어는 대출·연장·연체였습니다.
노트북 밖 다섯 번 가운데 두 번은 묻지 않은 운영 규정까지 네 번 요청했습니다.
몇 개를 요청하든 모두 첫 응답 한 번에 넣은 것은 다섯 번 모두 같았습니다.

다음 셀은 이번 실행이 더한 응답에서 `write_file` 요청의 인자를 모읍니다.
응답의 속성 `tool_calls`에서 이름이 `write_file`인 요청만 고릅니다."""),
        code(WRITTEN),
        md("""**결과 읽기** — 출력 줄 `write_file 요청 수: 1`과 `적으려 한 파일 위치: /notes/rules.md`가 보입니다.
모델은 질문이 정한 파일 위치에 한 번 적었습니다.
요청을 몇 번, 어느 파일 위치로 보낼지는 모델이 정하는 값입니다.
노트북 밖 다섯 번에서도 모두 같은 파일 위치에 한 번 적었습니다.

다음 셀은 결과의 상태 칸 `files`와 임시 폴더 안을 봅니다.
3절의 값 바꿔 보기에서 본 대로라면, 상태 칸은 비고 임시 폴더에 파일이 생길 것입니다."""),
        code(WHERE),
        md("""**결과 읽기** — 출력 줄 `상태 칸 files의 파일 위치: []`와 `임시 폴더 안 이름: ['notes']`가 보입니다.
디스크 백엔드라 상태 칸은 비었고, 모델이 적은 파일은 임시 폴더에 생겼습니다.
3절에서 손으로 만든 요청으로 본 자리와 같습니다.

다음 셀은 모델이 적은 파일 위치마다, 임시 폴더 안 파일을 `with open`으로 읽습니다.
메서드 `lstrip("/")`은 글 맨 앞의 `/`를 떼어 냅니다.
함수 `os.path.isfile`은 그 위치에 파일이 있으면 `True`를 내놓습니다."""),
        code(DISK_FILE),
        md("""**결과 읽기** — 출력 줄 `임시 폴더 안에 파일이 있는가: True`와 `요청 인자의 글과 같은가: True`가 보입니다.
모델이 요청 인자로 보낸 글이 디스크 파일에 그대로 적혔습니다.
같은 글은 메시지 목록 안 응답의 `write_file` 요청 인자에도 남아 있습니다.
파일로 적어 두어도 이번 실행의 메시지 목록에서 그 글이 빠지지는 않습니다.

## 6. 요청 수와 예상 비용

이 실행도 도구 `task`를 부르지 않아, 모델 요청은 모두 바깥 에이전트의 것입니다.
02절처럼 응답으로 센 요청 수와 기록 훅이 센 요청 수를 견주고, 받은 도구도 봅니다."""),
        code(USAGE),
        md("""**결과 읽기** — 라벨 `응답으로 센 요청 수:`와 `기록 훅이 센 요청 수:` 뒤의 수가 같습니다.
요청 수는 도구를 요청한 응답 수에 마지막 응답 하나를 더한 값입니다.
출력 줄 `받은 도구 수: 9`와 `execute를 받았는가: False`도 보입니다.
2절에서 예상한 대로, 디스크 백엔드에서도 모델은 `execute`를 받지 않았습니다.

이번 실행에서는 요청 3번, `입력 토큰: 6093 | 출력 토큰: 284`였습니다.
도구를 요청한 응답이 둘이라, 셈으로도 3번입니다.
노트북 밖 다섯 번과 새 커널 두 번에서 요청은 모두 3번이었습니다.
출력 토큰은 노트북 밖 다섯 번에서 실행마다 달랐습니다.

다음 셀은 02절과 같은 글의 셀로, 이번 실행의 예상 비용을 셉니다.
요금은 과정 요금표(2026-09-17)의 100만 토큰당 달러이고, 예상 비용은 청구 금액이 아닙니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 `예상 비용(달러):` 뒤에 이번 실행의 어림값이 보입니다.
토큰 수가 실행마다 달라, 이 값도 달라질 수 있습니다.
합친 사용량에는 캐시 입력 칸이 없어, 입력 토큰을 모두 입력 요금으로 셉니다.

이번 실행에서는 `예상 비용(달러): 0.005848`이었습니다.
노트북 밖 다섯 번에서는 0.005843에서 0.006201 사이였습니다.
캐시 입력을 빼지 않은 어림이라, 청구 금액은 이보다 작을 수 있습니다.

## 정리

1. 디스크 백엔드는 기준 폴더 안에 실제 파일을 쓰고, 기본 백엔드는 상태 칸 `files`에 둡니다.
2. 파일 위치의 맨 앞 `/`는 기준 폴더를 뜻하고, `..`로 밖을 가리키면 쓰기 전에 막힙니다.
3. 도구 `write_file`로 적은 글은 파일에도 남고, 요청 인자로 이번 실행의 메시지 목록에도 남습니다.

05절에서는 아주 긴 도구 결과를 파일로 옮기는 장치를 봅니다.
메시지 목록에는 짧은 안내 글만 남습니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH02_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH08_02 = "../../part2/ch08-context-engineering/02-Write와-Select.html"
L_CH13_04 = "../../part4/ch13-langgraph-basics/04-add_messages-리듀서.html"
L_CH20_01 = "../../part5/ch20-tool-node/01-ToolNode와-tools-condition.html"
L_CH21_03 = "../ch21-create-agent/03-AgentState와-context-schema.html"
L_CH23_01 = "../ch23-persistence/01-체크포인터와-스레드.html"
L_01 = "01-하네스와-일곱-기능.html"
L_02 = "02-create-deep-agent와-도구.html"
L_03 = "03-플래닝과-시스템-프롬프트.html"
L_05 = "05-컨텍스트-관리와-오프로딩.html"
L_08 = "08-통합-실행과-운영-한계.html"

RESULT_ROWS = [
    ("디스크 백엔드 설정", "<code>virtual_mode 값: True</code> · <code>명령을 실행할 수 있는가: False</code>", "구조 값"),
    ("파일 위치 규칙", "<code>임시 폴더 안 이름: ['etc', 'notes']</code> · <code>받은 오류: ValueError | Path traversal not allowed</code>", "구조 값"),
    ("같은 요청, 기본 백엔드", "<code>상태 칸 files의 파일 위치: ['/drafts/memo.md']</code> · 임시 폴더 그대로", "구조 값"),
    ("같은 요청, 디스크 백엔드", "<code>상태 칸 files의 파일 위치: []</code> · <code>임시 폴더 안 이름: ['drafts', 'etc', 'notes']</code>", "구조 값"),
    ("5절 파일이 남은 자리", "<code>상태 칸 files의 파일 위치: []</code> · <code>요청 인자의 글과 같은가: True</code> · <code>받은 도구 수: 9</code>", "구조 값"),
    ("5절 모델이 적은 파일과 요청 수", "<code>write_file 요청 수: 1</code> · <code>적으려 한 파일 위치: /notes/rules.md</code> · <code>응답으로 센 요청 수: 3</code> · <code>task</code> 0", "모델 판단 값"),
    ("5절 메시지 수·토큰·예상 비용", '교재 출력 <code>결과 메시지 수: 8</code> · <code>입력 토큰: 6093 | 출력 토큰: 284</code> · <code>예상 비용(달러): 0.005848</code>(노트북 밖에서는 메시지 9도 나옴)', "흔들리는 값"),
]

LOOK_B5 = "노트북 2절에서 <code>임시 폴더 안 이름: ['etc', 'notes']</code>와 받은 오류 <code>ValueError</code>를 확인합니다. 3절에서 두 백엔드의 <code>상태 칸 files의 파일 위치:</code> 줄을 견줍니다. 5절에서 <code>상태 칸 files의 파일 위치: []</code>와 <code>요청 인자의 글과 같은가: True</code>를 봅니다. 6절에서 두 방법으로 센 요청 수가 같은지 확인합니다."
LOOK_B6 = "노트북 3절 두 셀의 <code>상태 칸 files의 파일 위치:</code> 줄이 <code>['/drafts/memo.md']</code>와 <code>[]</code>로 다른지 봅니다. 6절 <code>응답으로 센 요청 수:</code>와 <code>기록 훅이 센 요청 수:</code>가 같은지 확인합니다. 교재 출력에서는 <code>응답으로 센 요청 수: 3</code>이었습니다."


def src_html() -> str:
    results = table_html(["확인한 것", "교재 출력", "값의 성격"], RESULT_ROWS)
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 1 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>디스크에 쓰는 백엔드와 상태 칸에 두는 백엔드에서, 파일이 남는 자리를 출력으로 짚을 수 있습니다.</li>
<li>파일 위치의 맨 앞 <code>/</code>와 <code>..</code>가 기준 폴더에서 어떻게 해석되는지 설명할 수 있습니다.</li>
<li>모델이 중간 결과를 파일로 적은 실행에서 구조 값과 흔들리는 값을 나누고, 요청 수를 셈으로 말할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>긴 일을 하는 에이전트는 찾은 자료나 정리한 메모를 나중에 다시 씁니다. 이런 값을 이 절에서는 중간 결과라고 부릅니다. Deep Agent는 중간 결과를 파일 도구로 파일에 적어 둘 수 있습니다. 그런데 그 파일이 어디에 생기는지는 백엔드에 따라 다릅니다.</p><p>이 절은 앞 절반에서 모델 없이, 같은 쓰기 요청이 두 백엔드에서 어디에 남는지 봅니다. 이 챕터에서 디스크 쓰기를 주제로 다루는 절은 이 절입니다. 뒤 절반에서는 실제 모델이 찾은 규정을 파일로 적어 두는 실행을 한 번 봅니다. 파일에 적힌 글은 실행마다 달라져서, 결론은 파일이 생긴 자리와 칸으로 씁니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH02_05 + """\">Ch 2 05절</a>에서는 <code>with open</code>으로 파일에 글을 쓰고 다시 읽었습니다. <a href=\"""" + L_CH23_01 + """\">Ch 23 01절</a>에서는 <code>tempfile.mkdtemp</code>로 빈 임시 폴더를 만들어, 실습 폴더에 파일을 남기지 않았습니다. <a href=\"""" + L_CH08_02 + """\">Ch 8 02절</a>은 나중에 쓸 정보를 이번 요청의 메시지 목록 밖에 저장해 두는 일을 적어 두기(Write)라고 불렀습니다. 그 절에서 파일에 있다고 모델이 그 내용을 아는 것은 아니라는 것도 보았습니다.</p><p><a href=\"""" + L_CH13_04 + """\">Ch 13 04절</a>에서는 상태 형식에 메시지 칸을 두었습니다. <a href=\"""" + L_CH20_01 + """\">Ch 20 01절</a>에서는 도구 요청을 담은 응답을 손으로 만들어 도구 실행 노드에 넣었습니다. <a href=\"""" + L_CH21_03 + """\">Ch 21 03절</a>에서는 라이브러리가 준 상태 형식 <code>AgentState</code>를 보았습니다.</p><p><a href=\"""" + L_01 + """\">01절</a> 6절에서는 Deep Agent의 도구 실행 노드만 든 작은 그래프로, 모델 없이 도구를 불렀습니다. <a href=\"""" + L_02 + """\">02절</a>에서는 파일 도구가 파일을 두는 자리를 정하는 부품을 백엔드라고 정의했습니다. 기본 백엔드 <code>StateBackend</code>는 디스크에 쓰지 않고, 명령을 실행하지 못해 모델이 받는 목록에서 <code>execute</code>가 빠졌습니다. <a href=\"""" + L_03 + """\">03절</a>에서는 할 일 목록이 상태 칸 <code>todos</code>에 담기는 것을 보았습니다. 그 절 출력에서 기본 결과 칸에 <code>files</code>가 있는 것도 보았습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 쓴 유리 온실 옆에, 문이 열린 작은 나무 헛간이 있다고 합시다. 옮겨 심기 전까지 모종판을 둘 곳은 두 군데입니다. 온실 안 선반에 두면 온실을 쓰는 동안 곁에 있고, 헛간 선반에 두면 온실 밖에 따로 남습니다. 어디에 둘지는 모종판이 아니라, 정해 둔 보관 방식을 따릅니다.</p><p>모종판이 중간 결과를 적은 파일이고, 온실 안 선반이 기본 백엔드의 상태 칸 <code>files</code>입니다. 헛간 선반은 디스크 백엔드의 기준 폴더입니다. 어디에 둘지 정하는 이 보관 방식이 02절에서 정의한 백엔드에 해당합니다.</p><p>비유와 다른 점이 있습니다. 모종판은 한 번에 한 곳에만 있지만, 이 절 실행에서는 모델이 적은 글이 요청 인자로 메시지 목록에도 남습니다. 또 칸 수와 모종 수는 어떤 값과도 짝짓지 않고, 모종이 자란 모습이 걸린 시간을 뜻하지도 않습니다.</p>
""" + illustration_block() + """<h3>두 백엔드와 기준 폴더</h3><p>기본 백엔드 <code>StateBackend</code>는 파일을 그래프 상태의 칸 <code>files</code>에 둡니다. 이 칸은 파일 위치를 키로, 글과 시각 칸을 담은 파일 항목을 값으로 둔 딕셔너리입니다. 디스크에 쓰는 백엔드 <code>FilesystemBackend</code>는 컴퓨터 폴더에 실제 파일을 씁니다. 두 백엔드 모두 파일 도구 이름은 같고, 파일을 두는 자리만 다릅니다.</p><p>백엔드가 파일 위치의 맨 앞 <code>/</code>로 삼는 폴더를 기준 폴더라고 부릅니다. 아파트 안내문의 「101호」가 그 아파트 안의 101호를 뜻하는 것과 같습니다. 이 절 코드에서는 인자 <code>root_dir=</code>에 넘긴 임시 폴더가 기준 폴더입니다. 같은 <code>write_file</code> 요청을 넣자 기본 백엔드는 <code>상태 칸 files의 파일 위치: ['/drafts/memo.md']</code>를 냈습니다. 디스크 백엔드는 <code>상태 칸 files의 파일 위치: []</code>를 내고, 임시 폴더에 <code>drafts</code> 폴더를 만들었습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>파일 위치 규칙</h3><p>설치판 0.7.0의 디스크 백엔드는 설정 <code>virtual_mode</code>의 기본값이 <code>True</code>입니다. 이 설정에서 파일 위치의 맨 앞 <code>/</code>는 컴퓨터의 맨 위 폴더가 아니라 기준 폴더를 뜻합니다. 그래서 <code>/etc/rules.md</code>에 써도 기준 폴더 안에 <code>etc</code> 폴더가 생겼습니다. 파일 위치에 <code>..</code>가 들면, 쓰기 전에 <code>받은 오류: ValueError | Path traversal not allowed</code>로 막혔습니다.</p><p>설치판 <code>backends/filesystem.py</code> 독스트링은 이 설정이 프로그램을 가두는 장치는 아니라고 적습니다. 파일 위치 규칙으로 기준 폴더 밖을 막을 뿐입니다. 그래서 기준 폴더에는 비밀 글이 없는 빈 임시 폴더를 줍니다.</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h3>중간 결과와 적어 두기</h3><p>Ch 8 02절의 적어 두기는 나중에 쓸 정보를 메시지 목록 밖에 두는 일이었습니다. Deep Agent에서는 파일 도구 <code>write_file</code>이 그 일을 맡습니다. 기본 백엔드는 그 파일을 그래프 상태에, 디스크 백엔드는 기준 폴더에 둡니다. 둘 다 메시지 목록 밖이라, 파일에 있다고 모델이 그 글을 보는 것은 아닙니다. 다시 보려면 <code>read_file</code> 같은 파일 도구로 읽어야 합니다.</p><p>다만 모델이 파일에 적은 글은 <code>write_file</code> 요청의 인자로 이번 실행의 메시지 목록에도 남습니다. 5절 출력에서 두 글이 같은 것을 봅니다. 그래서 파일로 적어 두는 쓸모는 이번 요청을 줄이는 데보다, 나중에 다시 읽을 수 있다는 데 있습니다. 디스크 백엔드의 파일은 실행이 끝난 뒤에도 임시 폴더에 남습니다. 긴 도구 결과를 메시지 목록에서 빼는 장치는 05절에서 다룹니다.</p><h3>실제 모델을 부를 때의 안전 설정</h3><p>02절처럼 호출 한도를 두 곳에 줍니다. 바깥 호출 한도는 03절과 같은 10이고, general-purpose 명세의 자기 호출 한도는 2입니다. 한 번 실행의 모델 요청은 10에, 도구 <code>task</code>를 부른 횟수 × 2를 더한 값을 넘지 않습니다. 모델 실행도 새 임시 폴더를 기준 폴더로 삼아, 실습 폴더에는 파일을 쓰지 않습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 디스크 백엔드를 직접 불러 임시 폴더에 쓰고, 운영체제 함수와 <code>with open</code>으로 확인합니다. 파일 위치 규칙 둘도 2절에서 봅니다. 3절은 손으로 만든 <code>write_file</code> 요청을 두 백엔드의 작은 그래프에 넣어 견줍니다. 4절은 02·03절 셀과 같은 부품을 준비하고, 5절은 디스크 백엔드 Deep Agent를 실제 모델로 한 번 실행합니다. 6절은 요청 수와 예상 비용을 셉니다.</p><p>모델 요청은 5절 실행 셀에서만 나갑니다. 노트북 밖에서 같은 질문을 다섯 번 보냈을 때, 요청은 다섯 번 모두 3번이었습니다. 요금표로 어림한 예상 비용은 0.01달러 아래이고, 청구 금액이 아닙니다. 파일은 임시 폴더 둘에만 쓰고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>같은 쓰기 요청이 기본 백엔드에서는 상태 칸 <code>files</code>에, 디스크 백엔드에서는 임시 폴더에 남았습니다. 두 백엔드의 도구 이름과 도구 메시지는 같았습니다. 파일이 남는 자리는 모델이 아니라 백엔드가 정합니다.</p><p>아래 표는 이 절이 확인한 값과 그 성격입니다. 구조 값은 코드가 정하는 값이고, 모델 판단 값은 모델이 고른 값입니다. 흔들리는 값은 실행마다 달라질 수 있어 결론에 쓰지 않습니다.</p>
""" + results + """
<p>5절 실행에서도 디스크 백엔드는 상태 칸 <code>files</code>를 비워 두었고, 모델이 적은 파일은 임시 폴더에 생겼습니다. 디스크 파일의 글은 요청 인자의 글과 같았습니다. 모델이 받은 도구는 아홉이었고, <code>execute</code>는 없었습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>흔들림 확인 다섯 번과 두 커널에서 모두, 모델은 질문이 정한 <code>/notes/rules.md</code>에 <code>write_file</code>을 한 번 불렀습니다. 우리 도구 요청은 모두 첫 응답에 함께 넣었고, 도구 <code>task</code>는 부르지 않았습니다. 요청 수는 도구를 요청한 응답 수에 1을 더한 3번이었습니다. 첫 응답의 <code>lookup_rule</code> 요청 수는 노트북 밖에서 셋 또는 넷으로 달랐습니다. 몇 개를 함께 넣든 한 응답이라, 파일을 한 번 적고 답하면 요청은 3번이 됩니다.</p>
<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>디스크 백엔드는 모델에게 기준 폴더 안 파일을 읽고 쓰게 합니다. 설치판 <code>backends/filesystem.py</code> 97~136행 경고는 비밀 글이 든 파일도 읽힐 수 있다고 적습니다. 그래서 이 절은 기준 폴더를 빈 임시 폴더로 두고, 프로젝트 폴더를 넘기지 않았습니다.</li><li>공식 백엔드 문서는 <code>virtual_mode</code>의 기본값을 <code>False</code>로 적습니다. 설치판 0.7.0 소스의 기본값은 <code>True</code>이고, 이 절 출력도 <code>True</code>였습니다. 0.7.0 릴리스 노트도 기본값이 <code>True</code>로 바뀌었다고 적습니다. 다른 판을 쓰면 이 값을 먼저 확인합니다.</li><li>백엔드를 직접 부르면 권한 규칙이 걸리지 않습니다. 설치판 <code>graph.py</code> 474~478행 독스트링이 그렇게 적습니다. 노트북 밖에서 모델 없이 보니, 쓰기를 막은 파일 위치도 직접 부른 <code>write</code>로는 써졌습니다. 권한 규칙은 파일 도구 안에서만 판정하며, 이 노트북에서는 실행하지 않았습니다. <a href=\"""" + L_08 + """\">08절</a>에서 다룹니다.</li><li>파일 도구 <code>write_file</code>에 <code>..</code>가 든 파일 위치를 넘기면, 오류를 던지지 않고 결과 상태 <code>error</code>인 도구 메시지를 냅니다. 노트북 밖에서 모델 없이 확인했고, 이 노트북에서는 실행하지 않았습니다.</li><li>메시지 칸만 있는 상태 형식으로 작은 그래프를 만들면, 기본 백엔드의 쓰기가 <code>KeyError: 'files'</code>로 멈춥니다. 노트북 밖에서 모델 없이 확인한 것이라, 3절은 <code>FilesystemState</code>를 썼습니다.</li><li>deepagents 0.7.0부터 <code>write_file</code>은 있던 파일을 통째로 바꿉니다. 노트북 밖에서 모델 없이 두 백엔드 모두 확인했습니다. 여러 실행이 같은 파일 위치에 쓰면 앞 실행의 글이 사라지므로, 이 절은 실행마다 새 임시 폴더를 씁니다.</li><li>기본 백엔드의 파일은 그 실행의 상태 안에 있습니다. 공식 백엔드 문서는 체크포인터가 있으면 같은 스레드에서 이어진다고 적습니다. 이 노트북은 체크포인터를 쓰지 않아, 그 모양은 실행하지 않았습니다.</li><li>노트북을 쓰기 전에 5절 실행을 노트북 밖에서 다섯 번 보냈습니다. 파일이 생긴 자리·받은 도구·요청 수는 다섯 번 모두 같았습니다. 첫 응답의 <code>lookup_rule</code> 요청 수와 파일에 적은 글은 실행마다 달랐습니다. 같은 요청도 실행한 때에 따라 파일을 적는 모양이 달라질 수 있어, 이 절은 그 값을 결론에 쓰지 않습니다.</li><li>질문·파일 위치 <code>/notes/rules.md</code>·바깥 한도 10은 흐름을 보여 주려고 실행 전에 정한 예이고, 결과를 보고 바꾸지 않았습니다. 질문이 파일에 적으라고 했으므로, 모델이 스스로 중간 결과를 적었다고 읽지 않습니다.</li><li>노트북이 만든 임시 폴더는 지우지 않습니다. 운영체제 임시 폴더 안에 있어, 필요 없으면 직접 지웁니다. 걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>디스크 백엔드는 기준 폴더 안에 실제 파일을 쓰고, 기본 백엔드는 상태 칸 <code>files</code>에 둡니다.</li><li>파일 위치의 맨 앞 <code>/</code>는 기준 폴더를 뜻하고, <code>..</code>로 밖을 가리키면 쓰기 전에 막힙니다.</li><li>도구 <code>write_file</code>로 적은 글은 파일에도 남고, 요청 인자로 이번 실행의 메시지 목록에도 남습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_05 + """\">05절</a>에서는 아주 긴 도구 결과를 파일로 옮기는 장치를 봅니다. 메시지 목록에는 짧은 안내 글만 남습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 같은 <code>write_file</code> 요청을 기본 백엔드와 디스크 백엔드에 넣으면, 파일은 각각 어디에 남나요?</p><p class="quiz-a">기본 백엔드는 상태 칸 <code>files</code>에, 디스크 백엔드는 기준 폴더 안 실제 파일로 둡니다. 디스크 백엔드 쪽 상태 칸 <code>files</code>는 빈 목록입니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 기준 폴더가 임시 폴더인 디스크 백엔드에 <code>/etc/rules.md</code>와 <code>../outside.md</code>를 쓰면 어떻게 되나요?</p><p class="quiz-a">앞의 것은 기준 폴더 안 <code>etc/rules.md</code>로 생깁니다. 뒤의 것은 쓰기 전에 <code>ValueError</code>로 막혀, 기준 폴더 밖에는 아무것도 생기지 않습니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 「디스크 백엔드로 파일에 적어 두었으니, 이번 실행의 메시지 목록에서 그 글은 빠졌다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 모델이 적은 글은 <code>write_file</code> 요청 인자로 메시지 목록의 응답에 남습니다. 파일은 나중에 다시 읽을 수 있게 따로 둔 것입니다. 틀렸다면 노트북 5절 마지막 셀을 다시 읽습니다.</p><p class="quiz-q">4. 모델이 첫 응답에서 <code>lookup_rule</code> 넷을 함께 요청하고, 다음 응답에서 <code>write_file</code> 하나를 요청한 뒤 답했습니다. 모델 요청은 몇 번인가요?</p><p class="quiz-a">3번입니다. 도구를 요청한 응답 둘에 마지막 답 하나를 더합니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/deepagents/backends">Deep Agents backends</a></div>확인 2026-09-28 · 기본 백엔드를 중간 결과를 적는 메모장으로 소개합니다. 그 파일은 같은 스레드 안에서 이어진다고 적습니다. 디스크 백엔드에는 보안 경고를 두고 <code>virtual_mode=True</code>를 권합니다. 기본값은 <code>False</code>로 적어, 설치판 0.7.0과 다릅니다.</li><li><div><a href="https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.0">deepagents 0.7.0 release</a></div>확인 2026-09-28 · <code>write_file</code>이 있던 파일을 통째로 바꾸고, 도구 <code>delete</code>가 생겼다고 적습니다. 디스크 백엔드의 <code>virtual_mode</code> 기본값이 <code>True</code>로 바뀌었고, 백엔드는 객체로 넘긴다고 적습니다.</li><li>설치판 deepagents 0.7.0 소스 <code>backends/filesystem.py</code> 97~136행은 보안 경고입니다. 141행이 <code>virtual_mode</code> 기본값, 202~206행이 <code>..</code>를 막는 자리, 495~530행이 쓰기입니다.</li><li>설치판 소스 <code>backends/state.py</code> 56~80행은 그래프 밖에서 부를 때의 오류입니다. 98~122행은 파일을 그래프의 <code>files</code> 칸에 쓰는 자리입니다.</li><li>설치판 소스 <code>middleware/filesystem.py</code> 801~805행은 상태 형식 <code>FilesystemState</code>입니다. 1156~1175행은 함수 <code>supports_execution</code>, 1706~1795행은 도구 <code>write_file</code>입니다. <code>graph.py</code> 474~478행은 백엔드 직접 호출에 권한이 걸리지 않는다는 독스트링입니다.</li></ul>
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
        # 04절은 도구 파일에 함수를 더하지 않아 도구 파일을 쓰지 않습니다(02절 판 그대로 — 위 check_tools가 확인)
        path = write_notebook(LAB, "04", SLUG, "experiment", cells())
        print("wrote", path)
