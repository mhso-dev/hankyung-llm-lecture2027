"""Ch 27 05절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_05.py            → 노트북 + _src 본문을 다시 쓴다(도구 파일은 쓰지 않음 — 02절 판 그대로, 노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_05.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  python3 -B author_05.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 실행용 — Ch 26 A-19 교훈)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**.
슬러그 `05-컨텍스트-관리와-오프로딩` 그대로(Part 6 목차와 04절 b8이 링크), 제목 「컨텍스트 관리와 오프로딩」 그대로
(「오프로딩」은 제목에만 — 본문 첫 자리에서 「옮겨 두기(offloading)」로 풂, 강사 확인).

## 결정 1 — M2: 앞 절반 모델 없음 + 뒤 절반 실제 모델 (챕터 리드 결정 1)

nbkit.key_and_model_cells("openai:gpt-5.4-mini") — temperature=0·reasoning_effort="none", 키는 루트 .env에서만(값 출력 없음).
2~4절은 손으로 만든 도구 요청(호출 ID를 우리가 정함)을 도구 실행 노드만 든 작은 그래프(04절 tools_only_graph)에 넣어,
기본 한도(20000 → 기준 80000자)에서 방문 기록 88889자는 /large_tool_results/hand_log_1로 옮겨지고(안내 글 1122자)
규정 33·41자는 그대로인 것, 같은 이름 FilesystemMiddleware(tool_token_limit_before_evict=10 → 기준 40자)에서
운영 규정 41자가 안내 글 658자로 오히려 길어지는 것, 요약 기준 int(400000 × 0.85) = 340000토큰을 모델 없이 본다.
6절에서 기본 한도 그대로의 Deep Agent를 실제 모델로 한 번 실행한다(옮겨 둔 방문 기록에서 분실물 줄을 다시 찾는 장면).
요약은 기준에 닿지 않아 켜지지 않고, 켜 보이지도 않는다(「실행하지 않았습니다」). 가짜 채팅 모델 없음(규격 §3).

## 결정 2 — 파일 쓰기 자리 (챕터 리드 결정 3)

디스크에 쓰지 않는다. 옮겨 둔 결과는 기본 백엔드(StateBackend)의 상태 칸 files에만 생긴다(04절 임시 폴더 셀 없음).
옛 판의 실습 폴더 workspace-05/는 그대로 둔다(마감 삭제 승인 목록).

## 결정 3 — 안전 규칙 (가)·(나)와 요청 수 셈 (챕터 공통)

바깥 ModelCallLimitMiddleware(run_limit=10) — 03절 셀과 같은 글 + 같은 이름 general-purpose 명세(02절 셀과 같은 글, 한도 2).
상한 10 + task 부른 횟수 × 2. 요청 수 = 이번 실행이 더한 메시지만 잘라 sum_usage = 기록 훅(새 이름 record_sizes) 요청 수.

## 결정 4 — 흔들림 먼저 확인 (qa/upgrade/05-probe.md)

노트북 밖 5번(요청 15번, §0은 첫 요청 전 14:07Z): 구조 값(안내 글·옮겨 둔 파일 하나·글 같음·요청마다 글자 수 합 < 방문 기록)과
모델 판단 값(read_visit_log → grep → 답, task 0, 요청 3) 5/5 → 입력 그대로. 입력 토큰·출력 토큰·캐시 입력·비용은 흔들림.
흔들리는 값(메시지 수·훅 글자 수·토큰·비용)은 [[READ_…]] 자리 표시 → 교재 출력(A) 뒤 mdpatch.py. assert는 키 셀뿐.

## 결정 5 — 도구 파일 (챕터 리드 결정 6)과 tools_only_graph

02절 판 harness_tools.py에서 함수 넷을 가져온다(추가 0 — 도구 파일을 쓰지 않음). author_04.check_tools()(= 03 → 02 사슬).
tools_only_graph는 도구 파일로 옮기지 않고 04절 셀 글 그대로 노트북에 다시 적는다(check_same_as_prev로 04 노트북 디스크 셀과 글자 대조).
옮기면 도구 파일이 StateGraph·START·END·FilesystemState를 가져와야 하고(지금 도구 파일은 가져오기 0),
규격 §2-7 6번에 따라 그 도구 파일을 가져오는 02·03 노트북 설치 셀에도 langgraph를 넣어야 한다(완료된 모델 절 — 다시 실행하면 출력이 바뀜).
02·03절 셀과 같은 글(RULES·DEF_TOOL·HELPER_SPEC·COST / OUTER_LIMIT)도 author_02·author_03 문자열 그대로 + 두 노트북 디스크 셀 대조.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·변수 힌트·대입 풀기·별표 풀기·
`while`·`try`·세미콜론·`isinstance`·클래스·`re`. 힌트는 @tool 매개변수 `: str`(02절 셀)만, 데코레이터는 @tool과 @wrap_model_call만. 호출 깊이 2 이하.
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
import author_04  # noqa: E402  04절 셀 글·도구 파일 대조 사슬
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch27-deepagents/notebooks"
FIGS = ROOT / "textbook/part6/ch27-deepagents/figures"
SLUG = "05-컨텍스트-관리와-오프로딩"
TITLE_TEXT = "컨텍스트 관리와 오프로딩"
SRC = ROOT / "textbook/part6/ch27-deepagents/_src" / (SLUG + ".html")
NB02 = LAB / "02-create-deep-agent와-도구.ipynb"
NB03 = LAB / "03-플래닝과-시스템-프롬프트.ipynb"
NB04 = LAB / "04-파일시스템과-중간-결과.ipynb"
TOOLS_PATH = LAB / "harness_tools.py"
html_text = author_02.html_text
table_html = author_02.table_html
mermaid_block = author_02.mermaid_block
# 교재 출력(A, 14:19:35Z)·새 커널 두 번째(B, 14:20:01Z) 대조 뒤 채운 흔들리는 값의 글(mdpatch.py로 노트북·_src에도 같은 글)
FILLS = {
    "RUN": "이번 실행에서는 `결과 메시지 수: 6`이었습니다.\n모델이 파일 도구를 몇 번 부르는지에 따라 달라지는 값입니다.\n노트북 밖 다섯 번과 새 커널 두 번에서는 모두 여섯이었습니다.",
    "SHOW": "이번 실행에서 모델은 둘째 응답에서 `grep`을 한 번 요청했고, 그 결과를 받은 뒤 답했습니다.\n노트북 밖 다섯 번과 새 커널 두 번에서 모두 방문 기록 도구, `grep`, 답의 차례였습니다.\n어느 파일 도구를 어떤 인자로 부를지는 모델이 정하는 값이라, 실행마다 달라질 수 있습니다.\n안내 글에는 호출 ID가 두 번 들어가, 이번 `글자 수: 1160`은 3절의 1122와 호출 ID 길이만큼 다릅니다.\n마지막 답 글도 모델이 쓴 글이라 실행마다 달라질 수 있습니다.",
    "SIZES": "이번 실행에서는 `요청마다 받은 메시지 글자 수: [76, 1236, 1334]`였습니다.\n첫 요청은 질문 한 줄이고, 둘째 요청부터 안내 글과 파일 도구 결과가 더해졌습니다.\n노트북 밖 다섯 번과 새 커널 두 번에서도 같은 목록이었습니다.\n다만 호출 ID 길이와 파일 도구 결과에 따라 달라질 수 있는 값입니다.",
    "USAGE": "이번 실행에서는 요청 3번, `입력 토큰: 6702 | 출력 토큰: 86`이었습니다.\n6절 출력에서 도구 요청이 든 응답 줄이 둘이라, 셈으로도 3번입니다.\n노트북 밖 다섯 번과 새 커널 두 번에서 요청은 모두 3번이었습니다.\n입력·출력 토큰은 새 커널 두 번과 노트북 밖 다섯 번에서 조금씩 달랐습니다.",
    "COST": "이번 실행에서는 `예상 비용(달러): 0.005413`이었습니다.\n노트북 밖 다섯 번에서는 0.005396에서 0.005413 사이였습니다.\n캐시 입력을 빼지 않은 어림이라, 청구 금액은 이보다 작을 수 있습니다.",
    "ROW_SHAKY": "교재 출력 <code>입력 토큰: 6702 | 출력 토큰: 86</code> · <code>예상 비용(달러): 0.005413</code> · 안내 글 <code>글자 수: 1160</code> · <code>요청마다 받은 메시지 글자 수: [76, 1236, 1334]</code>(새 커널 두 번째는 입력 토큰 6696·출력 토큰 85)",
    "LOOK_B6": "노트북 3절 <code>도구 메시지 글자 수: 1122</code>와 4절 <code>호출 ID: hand_rule_2 | 글자 수: 658</code>을 견줍니다. 6절 <code>모두 방문 기록보다 작은가: True</code>를 확인합니다. 7절 <code>응답으로 센 요청 수:</code>와 <code>기록 훅이 센 요청 수:</code>가 같은지 봅니다. 교재 출력에서는 <code>응답으로 센 요청 수: 3</code>이었습니다.",
    "B6_JUDGE": "흔들림 확인 다섯 번과 두 커널에서 모두, 모델은 방문 기록 도구를 한 번 부른 뒤 <code>grep</code>을 한 번 부르고 답했습니다. 노트북 밖 기록에서 상태 칸 <code>files</code>의 파일은 옮겨 둔 방문 기록 하나뿐이어서, <code>grep</code>이 찾은 곳도 그 파일이었습니다. 도구 <code>task</code>는 부르지 않았고, 요청 수는 도구를 요청한 응답 수에 1을 더한 3번이었습니다. 안내 글 미리보기에는 345번째 줄이 없어, 파일 도구로 다시 찾지 않았다면 그 줄을 볼 수 없었습니다. 어느 파일 도구로 찾을지는 모델이 정하는 값이라, 이 절은 그 이름을 결론의 중심에 두지 않습니다.",
    "B7_PROBE": "노트북을 쓰기 전에 6절 실행을 노트북 밖에서 다섯 번 보냈습니다. 도구 차례·요청 수·옮겨 둔 자리는 다섯 번 모두 같았고, 입력 토큰은 조금씩 달랐습니다. 같은 요청도 실행한 때에 따라 옮겨 둔 파일을 다시 찾는 모양이 달라질 수 있습니다. 그래서 이 절은 도구 이름을 결론의 중심에 두지 않습니다.",
    "RUNS_SENTENCE": "새 커널로 두 번 실행해 견주자, 코드 셀 서른하나 가운데 스물아홉의 출력이 같았습니다. 달랐던 두 셀은 입력·출력 토큰과 예상 비용이 찍힌 7절 셀이고, 이 값은 결론에 쓰지 않습니다.",
}


def placeholder(name: str) -> str:
    """교재 출력(A)·B 대조 뒤 채운 글을 내놓습니다(첫 판은 [[READ_…]] 자리 표시 — author_02.placeholder)."""
    return FILLS[name]


def check_tools() -> None:
    """05절은 도구 파일에 함수를 더하지 않습니다. 04절 대조 사슬(= 03 → 02 사슬 + 디스크 판이 02절 판으로 시작)을 그대로 돌립니다."""
    author_04.check_tools()


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["deepagents==0.7.0", "langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3"])

IMPORTS = r'''# Deep Agents(01절)·파일 미들웨어와 상태 형식(04절)·미들웨어(Ch 22)·모델·메시지·도구·그래프 이름을 가져옵니다
from deepagents import create_deep_agent
from deepagents.middleware.filesystem import FilesystemMiddleware, FilesystemState, NUM_CHARS_PER_TOKEN
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_model_call
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
# 앞 챕터와 01절에서 배운 함수 넷은 도구 파일에서 가져옵니다
from harness_tools import estimate_cost, sum_usage, tool_call_names, tool_names

print("도구 파일에서 가져온 함수:", "estimate_cost, sum_usage, tool_call_names, tool_names")'''

RULES = author_02.RULES
DEF_TOOL = author_02.DEF_TOOL

LOG_VALUES = r'''# 방문 기록 도구가 쓸 값을 정합니다(교재용 기록 — 줄 수, 분실물 기록을 둘 자리, 그 줄의 글)
log_line_count = 2000
lost_number = 345
lost_line = "방문 기록 " + str(lost_number) + ": 분실물 신고 — 파란 우산 1개를 안내 데스크에 맡김"
print("기록 줄 수:", log_line_count)
print("분실물 줄:", lost_line)'''

DEF_LOG_TOOL = r'''# 방문 기록 전체를 한 글로 내놓는 도구를 만듭니다(맨 @tool 줄 — 02절 lookup_rule과 같은 모양)
@tool
def read_visit_log():
    """교육센터 자료실의 오늘 방문 기록 전체를 한 번에 내놓습니다."""
    visit_lines = []
    for number in range(1, log_line_count + 1):
        line = "방문 기록 " + str(number) + ": 열람실에서 신문과 잡지, 새로 들어온 책 목록을 읽고 나감"
        # 정해 둔 자리 한 줄만 분실물 기록으로 바꿉니다
        if number == lost_number:
            line = lost_line
        visit_lines.append(line)
    return "\n".join(visit_lines)'''

TOOL_TRY = r'''# 모델 없이 도구만 실행해, 결과 글의 줄 수·글자 수와 분실물 줄이 들어 있는지 봅니다(Ch 19 05절 도구.invoke)
visit_log_text = read_visit_log.invoke({})
visit_log_lines = visit_log_text.splitlines()
print("결과 줄 수:", len(visit_log_lines))
print("결과 글자 수:", len(visit_log_text))
print("분실물 줄이 들어 있는가:", lost_line in visit_log_text)
print("첫 줄:", visit_log_lines[0])'''

DEF_GRAPH = author_04.DEF_GRAPH

BASE_AGENT = r'''# 한도를 바꾸지 않은 Deep Agent에 두 도구를 넘기고, 도구 실행 노드만 든 작은 그래프를 만듭니다(요청은 보내지 않음)
base_agent = create_deep_agent(model=model, tools=[lookup_rule, read_visit_log])
base_tools = tool_names(base_agent)
print("그래프에 등록된 도구 수:", len(base_tools))
base_tools_graph = tools_only_graph(base_agent)'''

HAND_RULES = r'''# 모델 없이, lookup_rule 요청 둘을 담은 응답을 손으로 만듭니다(04절 3절 모양)
loan_call = {"name": "lookup_rule", "args": {"topic": "대출"}, "id": "hand_rule_1", "type": "tool_call"}
hours_call = {"name": "lookup_rule", "args": {"topic": "운영"}, "id": "hand_rule_2", "type": "tool_call"}
rule_request = AIMessage(content="", tool_calls=[loan_call, hours_call])
print("요청한 도구:", tool_call_names(rule_request))'''

RUN_RULES_BASE = r'''# 기본 한도의 작은 그래프에 넣고, 도구 메시지마다 글과 글자 수, 상태 칸 files를 봅니다
rule_result = base_tools_graph.invoke({"messages": [rule_request]})
for message in rule_result["messages"][1:]:
    print("도구 메시지:", message.content, "| 글자 수:", len(message.content))
print("상태 칸 files의 파일 위치:", list(rule_result["files"]))'''

HAND_LOG = r'''# 모델 없이, 방문 기록 도구 요청 하나를 담은 응답을 손으로 만듭니다(호출 ID도 우리가 정함)
log_call = {"name": "read_visit_log", "args": {}, "id": "hand_log_1", "type": "tool_call"}
log_request = AIMessage(content="", tool_calls=[log_call])
print("요청한 도구:", tool_call_names(log_request))'''

RUN_LOG_BASE = r'''# 같은 작은 그래프에 넣고, 원래 결과와 도구 메시지의 글자 수, 상태 칸 files를 봅니다
log_result = base_tools_graph.invoke({"messages": [log_request]})
log_message = log_result["messages"][-1]
print("원래 결과 글자 수:", len(visit_log_text))
print("도구 메시지 글자 수:", len(log_message.content))
print("상태 칸 files의 파일 위치:", list(log_result["files"]))'''

NOTICE = r'''# 도구 메시지에 남은 짧은 글을 그대로 봅니다(여러 줄이라 라벨 줄을 따로 출력)
print("도구 메시지:")
print(log_message.content)'''

SAVED = r'''# 상태 칸 files에 옮겨 둔 파일의 글이 원래 결과와 같은지 봅니다
saved_entry = log_result["files"]["/large_tool_results/hand_log_1"]
print("옮겨 둔 글자 수:", len(saved_entry["content"]))
print("원래 결과와 같은가:", saved_entry["content"] == visit_log_text)'''

THRESHOLD = r'''# 옮기는 기준을 기본 한도로 셉니다(기본 한도 20000은 설치판 소스의 기본값, 4는 라이브러리 상수)
default_limit = 20000
default_threshold = NUM_CHARS_PER_TOKEN * default_limit
print("기본 한도(토큰):", default_limit)
print("한 토큰으로 어림하는 글자 수:", NUM_CHARS_PER_TOKEN)
print("기본 기준(글자):", default_threshold)
print("운영 규정이 기준을 넘는가:", len(library_rules["운영"]) > default_threshold)
print("방문 기록이 기준을 넘는가:", len(visit_log_text) > default_threshold)'''

SMALL_AGENT = r'''# 값 바꿔 보기: 한도 10인 FilesystemMiddleware를 middleware=에 넣어, 같은 이름의 기본 자리를 바꿉니다(요청은 보내지 않음)
small_token_limit = 10
small_limit = FilesystemMiddleware(tool_token_limit_before_evict=small_token_limit)
small_agent = create_deep_agent(model=model, tools=[lookup_rule, read_visit_log], middleware=[small_limit])
print("작은 한도(토큰):", small_token_limit)
print("작은 기준(글자):", NUM_CHARS_PER_TOKEN * small_token_limit)
print("도구 이름이 같은가:", tool_names(small_agent) == base_tools)
small_tools_graph = tools_only_graph(small_agent)'''

RUN_RULES_SMALL = r'''# 같은 규정 요청 둘을 한도 10의 작은 그래프에 넣고, 도구 메시지마다 호출 ID·글자 수와 상태 칸 files를 봅니다
small_result = small_tools_graph.invoke({"messages": [rule_request]})
for message in small_result["messages"][1:]:
    print("호출 ID:", message.tool_call_id, "| 글자 수:", len(message.content))
print("상태 칸 files의 파일 위치:", list(small_result["files"]))'''

SUMMARY_THRESHOLD = r'''# 요약이 켜지는 기준을 모델 객체의 정보(profile)로 셉니다(요약은 실행하지 않음 — 모델 요청 없음)
max_input_tokens = model.profile["max_input_tokens"]
summary_fraction = 0.85
summary_threshold = int(max_input_tokens * summary_fraction)
print("모델이 받을 수 있는 입력 토큰:", max_input_tokens)
print("요약이 켜지는 기준(토큰):", summary_threshold)'''

OUTER_LIMIT = author_03.OUTER_LIMIT
HELPER_SPEC = author_02.HELPER_SPEC

DEF_HOOK = r'''# 모델 요청이 나갈 때마다, 그 요청에 실린 메시지 글의 글자 수 합을 기록 목록에 붙이는 훅입니다(Ch 22 02절 기록 훅 모양)
@wrap_model_call
def record_sizes(request, handler):
    total = 0
    for message in request.messages:
        total = total + len(message.text)
    seen_sizes.append(total)
    # 기록만 하고, 요청은 그대로 모델에게 보냅니다
    return handler(request)'''

RUN_AGENT = r'''# 기본 한도 그대로의 Deep Agent에 방문 기록 도구·호출 한도·기록 훅·명세를 넘깁니다(요청은 아직 보내지 않음)
run_agent = create_deep_agent(
    model=model,
    tools=[read_visit_log],
    middleware=[outer_limit, record_sizes],
    subagents=[helper_spec],
)
run_tools = tool_names(run_agent)
print("그래프에 등록된 도구 수:", len(run_tools))'''

RUN = r'''# 기록 목록을 새로 만들고, 방문 기록에서 분실물 기록을 찾아 달라는 질문 한 줄로 한 번 실행합니다
seen_sizes = []
question = "교육센터 자료실의 오늘 방문 기록을 불러와서, 분실물 신고가 적힌 기록을 찾아 주세요. 무엇을 어디에 맡겼는지 한 문장으로 답해 주세요."
first_input = {"messages": [HumanMessage(content=question)]}
input_count = len(first_input["messages"])
run_result = run_agent.invoke(first_input)
run_messages = run_result["messages"]
print("결과 메시지 수:", len(run_messages))'''

SHOW_NEW = r'''# 이번 실행이 더한 메시지마다 종류와 도구 이름을 보고, 도구 메시지는 글자 수와 안내 글인지만 봅니다(호출 ID는 출력하지 않음)
run_new = run_messages[input_count:]
print("이번 실행이 더한 메시지:")
for message in run_new:
    kind = type(message).__name__
    if kind == "AIMessage":
        print(kind, "| 도구 호출 요청:", tool_call_names(message))
    if kind == "ToolMessage":
        is_notice = message.content.startswith("Tool result too large")
        print(kind, "|", message.name, "| 글자 수:", len(message.content), "| 안내 글인가:", is_notice)
print("마지막 답:", run_messages[-1].text)'''

OFFLOADED = r'''# 상태 칸 files에서 /large_tool_results/ 아래 파일을 세고, 그 글이 방문 기록 전체와 같은지 봅니다(파일 이름은 출력하지 않음)
offloaded = []
for file_path in run_result["files"]:
    if file_path.startswith("/large_tool_results/"):
        offloaded.append(file_path)
print("옮겨 둔 파일 수:", len(offloaded))
for file_path in offloaded:
    print("방문 기록 전체와 같은가:", run_result["files"][file_path]["content"] == visit_log_text)'''

SIZES = r'''# 기록 훅이 적은 요청마다의 글자 수 합을 보고, 모두 방문 기록 글자 수보다 작은지 봅니다
print("요청마다 받은 메시지 글자 수:", seen_sizes)
all_smaller = True
for size in seen_sizes:
    if size >= len(visit_log_text):
        all_smaller = False
print("모두 방문 기록보다 작은가:", all_smaller)'''

USAGE = r'''# 이번 실행이 더한 메시지만 Ch 19 05절 함수 sum_usage로 세고, 기록 훅이 센 요청 수와 견줍니다
run_usage = sum_usage(run_new)
print("응답으로 센 요청 수:", run_usage["requests"])
print("기록 훅이 센 요청 수:", len(seen_sizes))
print("입력 토큰:", run_usage["input_tokens"], "| 출력 토큰:", run_usage["output_tokens"])'''

COST = author_02.COST


def check_same_as_prev() -> None:
    """02·03·04절 셀과 같은 글이라고 적는 셀이 세 노트북 디스크 셀과 글자 그대로 같은지 봅니다."""
    sources_02 = author_02.notebook_code_sources(NB02)
    for cell in [RULES, DEF_TOOL, HELPER_SPEC, COST]:
        assert cell in sources_02, cell.splitlines()[0]
    sources_03 = author_02.notebook_code_sources(NB03)
    assert OUTER_LIMIT in sources_03, "OUTER_LIMIT가 03 노트북 셀과 다릅니다"
    sources_04 = author_02.notebook_code_sources(NB04)
    assert DEF_GRAPH in sources_04, "DEF_GRAPH가 04 노트북 셀과 다릅니다"


def check_same_as_probe() -> None:
    """노트북 셀의 방문 기록·도구·명세·한도·훅·에이전트·질문이 흔들림 확인 스크립트(probe05.py)와 같은 글인지 봅니다."""
    probe = (HERE / "probe/probe05.py").read_text(encoding="utf-8")
    pieces = []
    skip = ("#", "print(", "run_tools")
    for cell in [LOG_VALUES, DEF_LOG_TOOL, HELPER_SPEC, OUTER_LIMIT, DEF_HOOK, RUN_AGENT]:
        for line in cell.splitlines():
            if line.startswith(skip):
                continue
            pieces.append(line)
    pieces.append('model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")')
    for piece in pieces:
        assert piece in probe, piece
    question_line = RUN.splitlines()[2]
    assert question_line.replace("question = ", "QUESTION = ") in probe


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/05-figures.md)
FIG1 = "05-1-긴-결과를-옮겨-두기"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 손으로 만든 요청 read_visit_log 호출 ID hand_log_1에서 노란 상자 도구 결과 88889자 기준 80000자를 넘음으로, 다시 회색 상자 FilesystemMiddleware 기준보다 크면 옮김으로 화살표가 갑니다. 거기서 나란한 두 칸으로 화살표가 갈라집니다. 왼쪽 칸 메시지 목록에는 노란 상자 도구 메시지 안내 글 1122자가 있습니다. 오른쪽 칸 상태 칸 files에는 노란 상자 /large_tool_results/hand_log_1 88889자 원래 결과와 같음 True가 있는 그림"
FIG1_CAP = "기준 80000자를 넘은 방문 기록은 상태 칸 files로 옮겨지고, 메시지 목록의 도구 메시지는 1122자 안내 글이 되었습니다."
FIG1_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자는 모델 없이 손으로 만든 요청이고, 노란 상자는 노트북 2·3절 출력입니다.
회색 상자는 설치판 소스로 확인한 판정 자리이고, 두 칸은 결과가 나뉘어 남은 서로 다른 자리라 나란히 두었습니다.
원래 결과는 상태 칸에 그대로 있고, 메시지 목록에는 짧은 안내 글만 남았습니다."""

FIG2 = "05-2-한도와-기준"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 손으로 만든 요청 둘 대출 33자 운영 41자 규정에서 나란한 두 칸으로 화살표가 갑니다. 왼쪽 칸 기본 한도 20000 기준 80000자에는 노란 상자 대출 33자 운영 41자 둘 다 그대로와 노란 상자 상태 칸 files 빈 목록이 위아래로 있습니다. 오른쪽 칸 한도 10 기준 40자에는 노란 상자 대출 33자 그대로, 노란 상자 운영 41자 안내 글 658자로, 노란 상자 상태 칸 files /large_tool_results/hand_rule_2가 위아래로 있는 그림"
FIG2_CAP = "같은 규정 요청도 한도 10(기준 40자)에서는 운영 규정 41자가 옮겨졌고, 그 안내 글은 658자로 원래보다 길었습니다."
FIG2_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자는 3·4절에 넣은 같은 손 요청이고, 두 칸은 한도만 다른 설정이라 나란히 두었습니다.
노란 상자는 모두 노트북 3·4절 출력입니다.
기준 40자를 한 글자 넘은 운영 규정만 옮겨졌고, 기준보다 짧은 대출 규정은 두 칸 모두에서 그대로였습니다."""

FIG3 = "05-3-옮겨-둔-결과를-다시-찾는-실행"
FIG3_ALT = "세로선 넷이 있는 차례 그림입니다. 왼쪽부터 우리 코드, 그래프, 상태 칸 files, 연보라 띠 안의 모델 gpt-5.4-mini입니다. 우리 코드에서 질문 한 줄로 invoke 화살표가 그래프로 갑니다. 요청 1 화살표가 모델로 가고 read_visit_log 요청 점선이 돌아옵니다. 그래프에서 상태 칸 files로 방문 기록 전체를 옮겨 둠 화살표가 가고, 그래프에 노란 메모 도구 메시지는 안내 글 안내 글인가 True가 붙습니다. 요청 2 안내 글을 받음 화살표가 모델로 가고 grep 요청 점선이 돌아옵니다. 그래프에서 상태 칸 files로 grep이 옮겨 둔 파일을 찾음 화살표가 갑니다. 요청 3에는 도구 요청 없음 답 글 점선이 돌아오고, 결과 메시지와 옮겨 둔 파일 수 1 점선이 우리 코드로 돌아오는 그림"
FIG3_CAP = "이번 실행에서 모델은 방문 기록 도구를 부른 뒤 안내 글만 받았고, grep으로 옮겨 둔 파일을 찾아 답했습니다."
FIG3_READ = """위에서 아래로 실행 차례대로 읽고, 세로선은 왼쪽부터 우리 코드, 그래프, 상태 칸 files, 모델입니다.
연보라 띠는 실제로 부른 모델 gpt-5.4-mini의 자리이고, 노란 메모는 노트북 6절 출력입니다.
도구 grep을 고른 것은 모델의 판단이라, 흔들림 확인 다섯 번과 두 커널에서 같았을 때만 그렸습니다.
도구 grep이 무엇을 찾아 내놓았는지와 글자 수는 실행마다 달라질 수 있어 그리지 않았습니다."""

FIG4 = "05-4-요청에-실린-것과-남은-것"
FIG4_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 보라 상자 모델의 응답 read_visit_log 요청에서 나란한 두 칸으로 화살표가 갑니다. 왼쪽 칸 모델 요청에 실린 것에는 노란 상자 도구 메시지 안내 글인가 True와 노란 상자 요청마다 받은 글자 수 합 모두 방문 기록보다 작은가 True가 있습니다. 오른쪽 칸 상태 칸 files에는 노란 상자 /large_tool_results/ 아래 옮겨 둔 파일 수 1과 노란 상자 방문 기록 전체와 같은가 True가 있습니다. 맨 아래 회색 상자 셈 요청 수는 도구를 요청한 응답 수 더하기 1이 있는 그림"
FIG4_CAP = "방문 기록 전체는 상태 칸 files에만 남았고, 모델 요청에는 어느 요청에도 실리지 않았습니다."
FIG4_READ = """위에서 아래로 읽습니다.
보라 상자는 실제로 부른 모델의 응답이고, 노란 상자는 노트북 6절 출력입니다.
두 칸은 같은 결과가 남은 서로 다른 자리라 나란히 두었습니다.
맨 아래 회색 상자는 두 커널과 흔들림 확인에서 모두 맞은 셈이고, 요청 수 자체는 그리지 않았습니다."""

ILLU = "05-5-온실-밖으로-옮긴-퇴비-포대"
ILLU_ALT = "흰 바탕의 그림입니다. 왼쪽에는 유리 온실이 있고, 안쪽 왼편 흙에는 잎이 넓은 초록 풀이 몇 포기 자라며 앞쪽 바닥은 비어 있습니다. 온실 안 앞쪽 가는 쇠기둥에는 빨간 끈에 매단 빈 빨간 꼬리표 하나가 걸려 있습니다. 오른쪽 온실 바로 밖에는 초록 천 차양 아래 아주 큰 삼베 퇴비 포대 하나가 서 있고, 묶은 포대 목에 같은 모양의 빨간 꼬리표가 달려 있습니다. 사람·손·연장·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "큰 퇴비 포대는 온실 밖 차양 아래로 옮겨 두고, 온실 안에는 같은 빨간 꼬리표 하나만 걸어 두었습니다."
ILLU_READ = "그림은 왼쪽 유리 온실과 오른쪽 온실 밖 차양 아래로 나뉩니다. 온실 안 쇠기둥에는 빈 빨간 꼬리표 하나가 걸려 있고, 차양 아래 큰 퇴비 포대에도 같은 빨간 꼬리표가 달려 있습니다. 포대가 긴 도구 결과, 차양 아래가 상태 칸 <code>files</code>, 온실 안 꼬리표가 메시지 목록에 남은 안내 글입니다. 온실 앞 바닥이 비어 있는 것은 긴 결과가 메시지 목록에서 빠진 모습입니다. 꼬리표와 포대의 크기, 풀 포기 수는 어떤 값과도 짝짓지 않습니다."

RUNS_SENTENCE = placeholder("RUNS_SENTENCE")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 아주 긴 도구 결과가 파일로 옮겨지고 짧은 안내 글만 남는 것을 모델 없이 봅니다.
2. 옮기는 기준을 셈으로 확인하고, 한도를 바꾸면 무엇이 달라지는지 봅니다.
3. 실제 모델이 옮겨 둔 파일에서 필요한 줄을 다시 찾는 실행을 한 번 보고, 요청 수를 셉니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 6절에서 Deep Agent를 한 번 실행합니다.
노트북 밖에서 같은 질문을 다섯 번 보냈을 때, 요청은 다섯 번 모두 3번이었습니다.
바깥 호출 한도 10과 서브에이전트 호출 한도 2를 주어, 요청이 끝없이 늘지 않게 막습니다.
요금표로 어림한 예상 비용은 0.01달러 아래이고, 청구 금액이 아닙니다.

옮겨 둔 결과는 상태 칸 `files`에만 두고, 디스크에는 파일을 쓰지 않습니다.
요약은 기준에 닿지 않아 일어나지 않고, 요약 요청도 나가지 않습니다.
모델의 답 글은 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.
앞에서 배운 함수 넷은 도구 파일 `harness_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 deepagents 0.7.0, langchain 1.4.0, langgraph 1.2.11입니다.
나머지 둘은 `langchain-openai` 1.6.0과 `python-dotenv` 1.2.3입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽습니다.
모델 없이 옮겨 두기의 기준과 모양을 보는 자리입니다.
5~7절은 실제 모델로 한 번 실행하는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch27-deepagents`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·요청은 6절에서만)를 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
모델 요청은 6절 실행 셀에서만 나갑니다.

2~4절은 이 객체로 Deep Agent를 만들기만 하고, 모델을 부르지 않습니다.
이 절은 파일을 디스크에 쓰지 않아, 04절의 임시 폴더 셀이 없습니다.
옮겨 둔 결과는 기본 백엔드의 상태 칸 `files`에만 생깁니다.

## 2. 긴 결과를 내놓는 도구

도구 결과가 짧으면 옮길 까닭이 없어서, 짧은 결과와 긴 결과를 함께 준비합니다.
짧은 결과는 02절의 규정 도구를 그대로 씁니다.
다음 셀은 02절 2절의 규정 글 셀과 같은 글입니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절에서는 아주 긴 도구 결과를 파일로 옮겨 두는 장치를 봅니다.
옮겨 두기(offloading)는 긴 도구 결과를 파일로 옮기고, 메시지 목록에는 짧은 글만 남기는 일입니다.
옮긴 뒤 남는 이 짧은 글을 아래 3절에서 안내 글이라고 부릅니다.
큰 짐은 창고에 넣고, 방에는 어디에 두었는지 적은 쪽지만 붙여 두는 것과 비슷합니다.
이 절 코드에서는 `FilesystemMiddleware`가 이 일을 맡고, 인자 `tool_token_limit_before_evict`가 기준을 정합니다.

첫 셀은 패키지 다섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `deepagents: 0.7.0`과 `langgraph: 1.2.11`이 보입니다.
다섯 판 모두 실습 폴더 잠금과 같은 판입니다.
패키지 langgraph는 3절에서 작은 그래프를 직접 만들려고 설치 목록에 넣었습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상수 `NUM_CHARS_PER_TOKEN`은 이 절에서 처음 씁니다.
미들웨어 `FilesystemMiddleware`는 01절에서 인자 없이 만들어 보았고, 이 절에서는 인자를 주어 만듭니다.
마지막 가져오기 줄은 앞에서 배운 함수 넷을 도구 파일 `harness_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, sum_usage, tool_call_names, tool_names`가 보입니다.
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
규정 글은 모두 한 줄짜리 짧은 글이라, 짧은 결과의 예로 씁니다.

긴 결과로는 자료실의 하루 방문 기록을 씁니다.
다음 셀은 기록의 줄 수와, 분실물 신고를 적을 자리와 그 줄의 글을 정합니다.
모두 교재용으로 정한 값입니다."""),
        code(LOG_VALUES),
        md("""**결과 읽기** — 출력 줄 `기록 줄 수: 2000`이 보입니다.
라벨 `분실물 줄:` 뒤가 345번째 줄에 넣을 글입니다.
나머지 줄은 모두 같은 모양의 방문 기록입니다.

다음 셀은 방문 기록 전체를 한 글로 내놓는 도구를 만듭니다.
인자가 없는 도구라, 모델은 빈 인자로 부릅니다.
메서드 `join`은 Ch 16 03절처럼 글 목록을 사이 글로 이어 한 글로 만듭니다.
여기서는 사이 글이 줄바꿈 `"\\n"`이라, 2,000줄짜리 글 하나가 됩니다."""),
        code(DEF_LOG_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 설명에는 결과가 길다는 말을 적지 않았습니다.
모델은 도구를 부르기 전에는 결과의 길이를 모릅니다.

다음 셀은 모델 없이 이 도구만 실행해, 결과 글의 크기를 봅니다.
Ch 19 05절처럼 도구의 `invoke`에 인자 딕셔너리를 넘기고, 인자가 없어 빈 딕셔너리를 넘깁니다.
메서드 `splitlines`는 Ch 2 05절처럼 글을 줄마다 나눈 목록을 내놓습니다."""),
        code(TOOL_TRY),
        md("""**결과 읽기** — 출력 줄 `결과 줄 수: 2000`과 `결과 글자 수: 88889`가 보입니다.
출력 줄 `분실물 줄이 들어 있는가: True`로, 가운데쯤 한 줄만 분실물 기록인 것을 봅니다.
라벨 `첫 줄:` 뒤는 나머지 줄과 같은 모양의 기록입니다.

## 3. 기본 한도에서 옮겨 두기 보기

모델 없이 도구를 부르려고, 04절의 작은 그래프 함수를 다시 씁니다.
다음 셀은 04절 3절 셀과 같은 글입니다.
Deep Agent 하나를 받아, 도구 실행 노드만 든 작은 그래프를 내놓습니다."""),
        code(DEF_GRAPH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 실행 노드에는 `FilesystemMiddleware`의 감싸기형 훅 `wrap_tool_call`이 함께 붙어 있습니다.
그래서 이 작은 그래프로 도구를 불러도, 옮겨 두기가 그대로 일합니다.

다음 셀은 두 도구만 넘겨 Deep Agent를 만들고, 작은 그래프도 만듭니다.
한도를 바꾸는 인자가 없어, 옮기는 한도는 기본값 그대로입니다."""),
        code(BASE_AGENT),
        md("""**결과 읽기** — 출력 줄 `그래프에 등록된 도구 수: 11`이 보입니다.
기본 도구 아홉에 우리 도구 둘을 더한 수입니다.

다음 셀은 모델 없이 `lookup_rule` 요청 둘을 담은 응답을 손으로 만듭니다.
04절 3절처럼 칸 `name`·`args`·`id`·`type`을 적은 딕셔너리를 넣습니다.
주제어는 대출과 운영이고, 두 규정 글의 길이는 4절에서 다시 씁니다."""),
        code(HAND_RULES),
        md("""**결과 읽기** — 출력 줄 `요청한 도구: ['lookup_rule', 'lookup_rule']`이 보입니다.
응답 하나에 도구 요청 둘을 담았습니다.

호출 ID `hand_rule_1`과 `hand_rule_2`는 우리가 정한 값입니다.
다음 셀은 이 요청을 작은 그래프에 넣고, 도구 메시지마다 글과 글자 수를 봅니다.
자르기 `[1:]`로 결과 메시지 목록의 맨 앞 손 요청은 빼고 봅니다.
실행 전에 예상해 봅니다.
짧은 결과라면 도구 메시지에 규정 글이 그대로 남을 것입니다."""),
        code(RUN_RULES_BASE),
        md("""**결과 읽기** — 두 도구 메시지에 규정 글이 그대로 남았고, 줄 끝이 `글자 수: 33`과 `글자 수: 41`입니다.
출력 줄 `상태 칸 files의 파일 위치: []`에서, 옮겨 둔 파일은 없습니다.
결과 메시지 목록의 맨 앞 손 요청은 빼고, 도구 메시지만 보았습니다.

다음 셀은 방문 기록 도구 요청 하나를 담은 응답을 손으로 만듭니다.
호출 ID는 `hand_log_1`로 정해, 옮겨 둔 파일 이름도 미리 정해지게 했습니다."""),
        code(HAND_LOG),
        md("""**결과 읽기** — 출력 줄 `요청한 도구: ['read_visit_log']`가 보입니다.

다음 셀은 이 요청을 같은 작은 그래프에 넣습니다.
실행 전에 예상해 봅니다.
방문 기록은 규정 글보다 훨씬 길어, 도구 메시지가 원래 결과와 달라질 것입니다."""),
        code(RUN_LOG_BASE),
        md("""**결과 읽기** — 출력 줄 `원래 결과 글자 수: 88889`와 `도구 메시지 글자 수: 1122`가 보입니다.
출력 줄 `상태 칸 files의 파일 위치: ['/large_tool_results/hand_log_1']`에서, 파일 하나가 생겼습니다.
파일 이름은 우리가 정한 호출 ID 그대로입니다.
도구가 내놓은 글이 메시지 목록에 들어가기 전에 파일로 옮겨지고, 짧은 글로 바뀌었습니다.

다음 셀은 도구 메시지에 남은 짧은 글을 그대로 봅니다.
여러 줄이라 라벨 줄을 따로 출력합니다."""),
        code(NOTICE),
        md("""**결과 읽기** — 라벨 줄 아래 첫 줄은 결과가 너무 커서 파일에 두었다는 말과 파일 위치입니다.
그다음 두 단락은 `read_file`로 조금씩 나눠 읽으라는 안내입니다.
맨 아래는 결과의 앞 다섯 줄과 뒤 다섯 줄이고, 가운데 줄 `... [1990 lines truncated] ...`는 뺀 줄 수입니다.
이 절에서는 이 짧은 글 전체를 안내 글이라고 부르겠습니다.

345번째 분실물 줄은 안내 글에 없습니다.
모델이 분실물을 찾으려면, 옮겨 둔 파일을 파일 도구로 다시 봐야 합니다.
설치판 `middleware/_message_eviction.py` 37~63행에서, 미리보기는 결과가 열 줄을 넘으면 앞뒤 다섯 줄입니다.
50~53행에서, 결과가 열 줄 이하이면 모든 줄을 붙입니다.

도구 `lookup_rule`의 주석에 있는 「정해 둔 안내 글」은 이 안내 글과 다릅니다.
없는 주제어에 도구가 내놓는, 정해 둔 글을 가리킵니다."""),
        code(SAVED),
        md("""**결과 읽기** — 출력 줄 `옮겨 둔 글자 수: 88889`와 `원래 결과와 같은가: True`가 보입니다.
원래 결과는 한 글자도 줄지 않고 상태 칸 `files`에 그대로 있습니다.
옮겨 두기는 요약처럼 글을 다시 쓰지 않고, 메시지 목록의 글만 안내 글로 바꿉니다.

그러면 어떤 결과를 옮길까요?
설치판 `middleware/filesystem.py` 2846행은 결과 글자 수가 「4 × 한도」 이하이면 그대로 둡니다.
그보다 크면 옮깁니다.
다음 셀은 이 기준을 기본 한도로 셉니다."""),
        code(THRESHOLD),
        md("""**결과 읽기** — 출력 줄 `기본 한도(토큰): 20000`과 `기본 기준(글자): 80000`이 보입니다.
운영 규정은 기준을 넘지 않고, 방문 기록은 넘습니다.
그래서 앞 셀들에서 규정 글은 그대로 남고, 방문 기록만 옮겨졌습니다.

인자 이름에는 토큰이 들어 있지만, 실제 판정은 글자 수로 합니다.
설치판 주석은 한 토큰을 네 글자로 어림한다고 적습니다.
이 절은 결과 글의 토큰 수를 세지 않았습니다.

## 4. 한도를 바꿔 보기와 요약 기준

### 값 바꿔 보기: 같은 이름 미들웨어로 한도 낮추기

한도를 바꾸려면 `FilesystemMiddleware`를 새로 만들어 인자 `middleware=`에 넣습니다.
설치판 `graph.py` 201~235행에서, 기본 미들웨어와 이름이 같은 것은 그 자리를 바꿉니다.
바꿀 값은 한도 하나이고, 기준이 40자가 되게 10으로 둡니다.
실행 전에 예상해 봅니다.
33자인 대출 규정은 그대로, 41자인 운영 규정은 옮겨질 것입니다."""),
        code(SMALL_AGENT),
        md("""**결과 읽기** — 출력 줄 `작은 기준(글자): 40`과 `도구 이름이 같은가: True`가 보입니다.
미들웨어를 하나 더 붙인 것이 아니라 기본 자리를 바꿔서, 도구 이름이 그대로입니다.

다음 셀은 3절의 규정 요청 둘을 이 작은 그래프에 그대로 넣습니다.
도구 메시지마다 호출 ID와 글자 수, 상태 칸 `files`를 봅니다."""),
        code(RUN_RULES_SMALL),
        md("""**결과 읽기** — 출력 줄 `호출 ID: hand_rule_1 | 글자 수: 33`에서, 대출 규정은 그대로 남았습니다.
출력 줄 `호출 ID: hand_rule_2 | 글자 수: 658`에서, 운영 규정은 안내 글로 바뀌었습니다.
출력 줄 `상태 칸 files의 파일 위치: ['/large_tool_results/hand_rule_2']`도 보입니다.
41자 결과가 기준을 한 글자 넘어 옮겨졌고, 안내 글은 원래 글보다 훨씬 깁니다.

안내 글에는 늘 같은 설명 단락과 파일 위치, 앞뒤 미리보기가 붙습니다.
그래서 옮겨 두기는 결과가 충분히 클 때만 메시지 목록을 줄입니다.
이 셀의 한도 10은 옮겨지는 모양을 짧은 글로 보여 주려고 정한 값입니다.

### 요약은 켜지지 않습니다

01절에서 본 기본 미들웨어 다섯에는 요약 미들웨어도 있습니다.
요약은 긴 대화의 앞부분을, 모델이 쓴 요약 글로 바꿔 요청에 싣는 장치입니다.
설치판 `middleware/summarization.py` 249~286행에서, 모델 정보에 입력 한도가 있으면 그 85%를 기준으로 씁니다.
모델 객체의 속성 `profile`은 입력 한도 같은 모델 정보를 담은 딕셔너리입니다.
다음 셀은 모델 요청 없이 이 기준을 셉니다."""),
        code(SUMMARY_THRESHOLD),
        md("""**결과 읽기** — 출력 줄 `모델이 받을 수 있는 입력 토큰: 400000`과 `요약이 켜지는 기준(토큰): 340000`이 보입니다.
요약은 요청에 실린 메시지의 토큰 수가 기준 이상일 때 시작합니다.
이 절의 요청은 그보다 훨씬 작아, 이 노트북에서 요약은 일어나지 않습니다.
요약 글을 쓰는 모델 요청도 나가지 않습니다.
요약을 켜 보려면 같은 이름 요약 미들웨어에 작은 기준을 주어야 하고, 이 노트북에서는 실행하지 않았습니다.

## 5. 실제 모델을 부를 준비

6절에서는 기본 한도 그대로의 Deep Agent에 방문 기록 도구를 주고, 분실물 기록을 찾게 합니다.
다음 셀은 03절 셀과 같은 글의 바깥 호출 한도입니다."""),
        code(OUTER_LIMIT),
        md("""**결과 읽기** — 출력 줄 `바깥 호출 한도: 10`이 보입니다.
주석의 「02절 셀과 한도만 다름」은 이 셀을 처음 쓴 03절에서 적은 말입니다.
방문 기록을 부르고, 옮겨 둔 파일을 찾고, 답하는 흐름이라 10이면 넉넉합니다.

다음 셀은 02절과 같은 글의 general-purpose 명세이고, 자기 호출 한도는 2입니다.
01절에서 본 것처럼 바깥 호출 한도는 이 서브에이전트로 옮겨 가지 않아, 두 곳에 따로 줍니다."""),
        code(HELPER_SPEC),
        md("""**결과 읽기** — 출력 줄 `명세의 키: ['name', 'description', 'system_prompt', 'middleware']`가 보입니다.
한 번 실행의 모델 요청은 10에, 도구 `task`를 부른 횟수 × 2를 더한 값을 넘지 않습니다.

다음 셀은 이 절에서 새로 만드는 기록 훅입니다.
모델 요청이 나갈 때마다, 요청에 실린 메시지 글의 글자 수를 모두 더해 기록 목록 `seen_sizes`에 붙입니다.
02절 기록 훅과 모양은 같고, 적는 값만 다릅니다.
속성 `text`는 메시지의 글이고, 도구 요청만 든 응답은 빈 글입니다."""),
        code(DEF_HOOK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
시스템 메시지 글과 도구 요청 인자는 세지 않습니다.
방문 기록 전체가 어느 요청에 실린다면, 그 요청의 합은 방문 기록 글자 수보다 커집니다.
이 훅도 바깥 인자 `middleware=`에만 넣어, general-purpose의 요청은 적지 않습니다.

## 6. 옮겨 둔 결과를 모델이 다시 찾는 실행

다음 셀은 방문 기록 도구와 5절의 부품을 넘겨 Deep Agent를 만듭니다.
한도를 바꾸는 미들웨어는 넣지 않아, 옮기는 기준은 기본 80,000자입니다."""),
        code(RUN_AGENT),
        md("""**결과 읽기** — 출력 줄 `그래프에 등록된 도구 수: 10`이 보입니다.
기본 도구 아홉과 방문 기록 도구 하나입니다.

질문은 방문 기록을 불러 분실물 신고 기록을 찾고, 한 문장으로 답하라는 글입니다.
어떤 파일 도구를 쓰라고는 적지 않았습니다.
실행 전에 예상해 봅니다.
방문 기록은 옮겨지고, 모델은 안내 글만 보고 파일에서 분실물 줄을 찾아야 할 것입니다."""),
        code(RUN),
        md("""**결과 읽기** — 라벨 `결과 메시지 수:` 뒤에 이번 실행의 메시지 수가 보입니다.
넣은 질문 하나 뒤에 모델 응답과 도구 메시지가 더해졌습니다.

""" + placeholder("RUN") + """

다음 셀은 이번 실행이 더한 메시지를 차례로 봅니다.
도구 메시지 글에는 서비스가 정한 호출 ID가 들어 있어, 글 대신 도구 이름과 글자 수만 출력합니다."""),
        code(SHOW_NEW),
        md("""**결과 읽기** — 라벨 줄 아래 첫 줄 `AIMessage | 도구 호출 요청: ['read_visit_log']`가 첫 응답입니다.
바로 아래 `read_visit_log` 도구 메시지 줄은 `안내 글인가: True`입니다.
모델이 받은 것은 방문 기록 전체가 아니라, 3절에서 본 모양의 안내 글입니다.
라벨 `마지막 답:` 앞 줄은 도구 요청이 없는 응답이고, 그 글이 마지막 답입니다.

""" + placeholder("SHOW") + """

다음 셀은 결과의 상태 칸 `files`에서 옮겨 둔 파일을 봅니다."""),
        code(OFFLOADED),
        md("""**결과 읽기** — 출력 줄 `옮겨 둔 파일 수: 1`과 `방문 기록 전체와 같은가: True`가 보입니다.
3절처럼, 옮겨 둔 파일은 상태 칸 `files`의 `/large_tool_results/` 아래에 생겼습니다.
파일 이름은 서비스가 정한 호출 ID라 실행마다 달라, 출력하지 않았습니다.
기본 백엔드라 디스크에는 아무 파일도 쓰지 않았습니다.

다음 셀은 기록 훅이 적은 값을 봅니다.
요청마다 모델이 받은 메시지 글자 수 합이, 방문 기록 글자 수보다 모두 작은지 확인합니다."""),
        code(SIZES),
        md("""**결과 읽기** — 출력 줄 `모두 방문 기록보다 작은가: True`가 보입니다.
방문 기록 전체는 어느 요청에도 실리지 않았습니다.
모델은 안내 글과, 파일 도구로 찾은 결과만 받았습니다.

""" + placeholder("SIZES") + """

## 7. 요청 수와 예상 비용

이번 실행에서는 도구 `task`를 부르지 않아, 모델 요청은 모두 바깥 에이전트의 것입니다.
02절처럼 응답으로 센 요청 수와 기록 훅이 센 요청 수를 견줍니다."""),
        code(USAGE),
        md("""**결과 읽기** — 라벨 `응답으로 센 요청 수:`와 `기록 훅이 센 요청 수:` 뒤의 수가 같습니다.
요청 수는 도구를 요청한 응답 수에 마지막 응답 하나를 더한 값입니다.

""" + placeholder("USAGE") + """

다음 셀은 02절과 같은 글의 셀로, 이번 실행의 예상 비용을 셉니다.
요금은 과정 요금표(2026-09-17)의 100만 토큰당 달러이고, 예상 비용은 청구 금액이 아닙니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 `예상 비용(달러):` 뒤에 이번 실행의 어림값이 보입니다.
토큰 수가 실행마다 달라, 이 값도 달라질 수 있습니다.
합친 사용량에는 캐시 입력 칸이 없어, 입력 토큰을 모두 입력 요금으로 셉니다.

""" + placeholder("COST") + """

## 정리

1. 도구 결과가 「4 × 한도」자를 넘으면, 원래 결과는 상태 칸 `files`로 옮겨지고 도구 메시지에는 안내 글만 남습니다.
2. 같은 이름 미들웨어로 한도를 바꾸면 기본 자리가 바뀌고, 작은 결과는 안내 글이 원래보다 길어질 수 있습니다.
3. 모델은 안내 글만 받으므로, 미리보기에 없는 줄은 파일 도구로 다시 찾아야 합니다.

06절에서는 일을 서브에이전트에게 맡기는 장면을 봅니다.
서브에이전트가 상태 칸 `files`를 함께 쓰는 모양도 봅니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH08_02 = "../../part2/ch08-context-engineering/02-Write와-Select.html"
L_CH08_03 = "../../part2/ch08-context-engineering/03-Compress와-Isolate.html"
L_CH16_03 = "../../part4/ch16-guardrails/03-히스토리-트리밍과-요약.html"
L_CH19_05 = "../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH20_01 = "../../part5/ch20-tool-node/01-ToolNode와-tools-condition.html"
L_CH22_03 = "../ch22-middleware/03-요약-압축과-Compress.html"
L_01 = "01-하네스와-일곱-기능.html"
L_02 = "02-create-deep-agent와-도구.html"
L_04 = "04-파일시스템과-중간-결과.html"
L_06 = "06-서브에이전트-위임.html"
L_08 = "08-통합-실행과-운영-한계.html"

RESULT_ROWS = [
    ("기본 한도의 기준", "<code>기본 한도(토큰): 20000</code> · <code>기본 기준(글자): 80000</code>", "구조 값"),
    ("짧은 결과, 기본 한도", "규정 두 도구 메시지 <code>글자 수: 33</code>·<code>글자 수: 41</code> · <code>상태 칸 files의 파일 위치: []</code>", "구조 값"),
    ("긴 결과, 기본 한도", "<code>원래 결과 글자 수: 88889</code> · <code>도구 메시지 글자 수: 1122</code> · <code>원래 결과와 같은가: True</code>", "구조 값"),
    ("한도 10으로 바꿔 보기", "<code>도구 이름이 같은가: True</code> · <code>호출 ID: hand_rule_2 | 글자 수: 658</code>", "구조 값"),
    ("요약 기준", "<code>요약이 켜지는 기준(토큰): 340000</code> · 요약은 실행하지 않음", "구조 값"),
    ("6절 옮겨 둔 자리", "<code>안내 글인가: True</code> · <code>옮겨 둔 파일 수: 1</code> · <code>모두 방문 기록보다 작은가: True</code>", "구조 값"),
    ("6절 모델이 다시 찾은 도구와 요청 수", "<code>grep</code> 한 번 · <code>응답으로 센 요청 수: 3</code> · <code>task</code> 0", "모델 판단 값"),
    ("6절 글자 수·토큰·예상 비용", placeholder("ROW_SHAKY"), "흔들리는 값"),
]

LOOK_B5 = "노트북 3절에서 <code>도구 메시지 글자 수: 1122</code>와 <code>상태 칸 files의 파일 위치: ['/large_tool_results/hand_log_1']</code>을 확인합니다. 4절에서 <code>호출 ID: hand_rule_2 | 글자 수: 658</code>을 봅니다. 6절에서 <code>안내 글인가: True</code>와 <code>모두 방문 기록보다 작은가: True</code>를 봅니다. 7절에서 두 방법으로 센 요청 수가 같은지 확인합니다."


def src_html() -> str:
    results = table_html(["확인한 것", "교재 출력", "값의 성격"], RESULT_ROWS)
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>긴 도구 결과가 옮겨지는 기준을 「4 × 한도」자로 셈하고, 옮긴 뒤 남는 것을 출력으로 짚을 수 있습니다.</li>
<li>같은 이름 미들웨어로 한도를 바꿀 때 달라지는 것과, 함께 사라지는 것을 말할 수 있습니다.</li>
<li>옮겨 둔 결과를 모델이 다시 보려면 무엇이 필요한지, 요약과 어떻게 다른지 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>도구가 아주 긴 결과를 내놓으면, 그 글은 도구 메시지로 메시지 목록에 들어갑니다. 그러면 다음 모델 요청마다 그 긴 글이 함께 실립니다. 04절에서 파일로 적은 글도 요청 인자로 메시지 목록에 남았습니다.</p><p>이 절은 긴 도구 결과를 파일로 옮기고, 메시지 목록에는 짧은 글만 남기는 장치를 봅니다. 남는 짧은 글은 「핵심 개념」에서 안내 글이라는 이름으로 풉니다. 이 일을 이 교재에서는 옮겨 두기(offloading)라고 부릅니다. 앞 절반은 모델 없이, 옮기는 기준과 옮긴 뒤의 모양을 봅니다. 뒤 절반은 실제 모델이 옮겨 둔 파일에서 필요한 줄을 다시 찾는 실행을 한 번 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH08_02 + """\">Ch 8 02절</a>에서는 나중에 쓸 정보를 메시지 목록 밖에 두는 일을 적어 두기(Write)라고 불렀습니다. 질문에 필요한 것만 다시 넣는 일은 골라 넣기(Select)였습니다. <a href=\"""" + L_CH08_03 + """\">03절</a>의 줄이기(Compress)는 원래 글을 줄이되 지킬 말은 남기는 일이었습니다. <a href=\"""" + L_CH16_03 + """\">Ch 16 03절</a>은 대화 기록을 자르는 방법과 모델로 요약하는 방법을 견줬습니다. 이 교재에서 「요약」은 모델이 줄인 글에만 씁니다.</p><p><a href=\"""" + L_CH22_03 + """\">Ch 22 03절</a>에서는 요약 미들웨어가 기준 이상에서 요약을 시작하는 것을 보았습니다. 그 절은 짧은 대화에서는 요약 글이 원래 대화보다 길 수 있다는 것도 보였습니다. <a href=\"""" + L_CH19_05 + """\">Ch 19 05절</a>에서는 도구의 <code>invoke</code>로 모델 없이 도구만 실행했습니다. <a href=\"""" + L_CH20_01 + """\">Ch 20 01절</a>에서는 손으로 만든 도구 요청을 도구 실행 노드에 넣었습니다.</p><p><a href=\"""" + L_01 + """\">01절</a>에서는 기본 미들웨어 다섯에 파일 미들웨어와 요약 미들웨어가 있다는 것을 설치판 소스로 보았습니다. 요약 미들웨어는 감싸기형 훅만 가져, 그래프에 노드로 보이지 않았습니다. <a href=\"""" + L_02 + """\">02절</a>의 규정 도구 <code>lookup_rule</code>을 이 절도 짧은 결과의 예로 씁니다. <a href=\"""" + L_04 + """\">04절</a>에서는 기본 백엔드가 파일을 상태 칸 <code>files</code>에 두는 것을 보았고, 작은 그래프 함수 <code>tools_only_graph</code>를 만들었습니다. 그 절은 긴 결과를 메시지 목록에서 빼는 장치를 이 절로 넘겼습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 쓴 유리 온실 안에, 큰 퇴비 포대 하나가 들어왔다고 합시다. 포대를 그대로 두면 온실 안 자리를 크게 차지합니다. 그래서 포대는 온실 밖 차양 아래로 옮기고, 온실 안에는 포대와 같은 색 꼬리표 하나만 걸어 둡니다. 꼬리표를 보면 포대가 밖에 있다는 것을 알고, 퇴비가 필요하면 밖에 나가 조금만 덜어 옵니다.</p><p>퇴비 포대가 긴 도구 결과이고, 온실 밖 차양 아래가 상태 칸 <code>files</code>입니다. 온실 안 꼬리표는 메시지 목록에 남는 안내 글입니다. 퇴비를 조금 덜어 오는 일은 모델이 파일 도구로 필요한 줄만 다시 찾는 일입니다.</p><p>비유와 다른 점이 있습니다. 꼬리표는 늘 작지만, 옮겨 두기의 안내 글은 설명 단락이 붙어 짧은 결과보다 길어질 수 있습니다. 또 포대와 꼬리표의 크기는 어떤 값과도 짝짓지 않습니다.</p>
""" + illustration_block() + """<h3>옮겨 두기</h3><p>옮겨 두기(offloading)는 긴 도구 결과를 파일로 옮기고, 메시지 목록에는 짧은 안내 글만 남기는 일입니다. 큰 짐은 창고에 넣고, 방에는 어디에 두었는지 적은 쪽지만 붙여 두는 것과 비슷합니다. 이 절 코드에서는 <code>FilesystemMiddleware</code>가 도구 실행을 감싸 이 일을 합니다.</p><p>기본 한도에서 방문 기록 결과는 <code>원래 결과 글자 수: 88889</code>였고, 도구 메시지는 <code>도구 메시지 글자 수: 1122</code>로 바뀌었습니다. 원래 결과는 상태 칸 <code>files</code>의 <code>/large_tool_results/hand_log_1</code>에 한 글자도 줄지 않고 남았습니다. 안내 글은 파일 위치와 <code>read_file</code>로 나눠 읽으라는 설명, 결과의 미리보기로 이루어집니다. 미리보기는 결과가 열 줄을 넘으면 앞뒤 다섯 줄이고, 열 줄 이하이면 모든 줄입니다. 이 절은 이 짧은 글을 안내 글이라고 부릅니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>옮기는 기준과 한도</h3><p>옮길지는 결과의 글자 수로 정합니다. 설치판 소스는 결과 글자 수가 「4 × 한도」 이하이면 그대로 두고, 그보다 크면 옮깁니다. 기본 한도는 20000이라 기준은 <code>기본 기준(글자): 80000</code>이고, 규정 글 33·41자는 그대로 남았습니다. 인자 이름은 토큰 한도이지만, 판정은 한 토큰을 네 글자로 어림한 글자 수로 합니다.</p><p>한도를 바꾸려면 <code>FilesystemMiddleware</code>를 새로 만들어 <code>middleware=</code>에 넣습니다. 이름이 같은 기본 미들웨어의 자리를 바꾸므로, 도구 이름은 그대로였습니다. 한도 10(기준 40자)에서 대출 규정 33자는 그대로, 운영 규정 41자는 안내 글 658자로 바뀌었습니다. 안내 글에는 늘 같은 설명 단락이 붙어, 옮겨 두기는 결과가 충분히 클 때만 메시지 목록을 줄입니다.</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<p>같은 이름으로 바꾼 미들웨어는 기본 미들웨어가 받던 인자를 물려받지 않습니다. 그래서 권한 규칙을 준 Deep Agent에서 한도를 바꾸면, 권한 규칙의 쓰기 막기도 함께 사라집니다. 01절이 노트북 밖에서 모델 없이 확인한 사실이고, 이 노트북에서는 실행하지 않았습니다. 권한은 <a href=\"""" + L_08 + """\">08절</a>에서 다룹니다.</p><h3>옮겨 두기와 요약</h3><p>옮겨 두기는 글을 다시 쓰지 않습니다. 원래 결과는 파일에 그대로 두고, 메시지 목록의 글만 안내 글로 바꿉니다. Ch 8 02절 말로는 적어 두기이고, 모델이 파일 도구로 필요한 줄만 다시 가져오는 일은 골라 넣기입니다. 메시지 목록을 짧게 한다는 목적은 Ch 8 03절 줄이기와 같지만, 지킬 말을 골라 남기지는 않습니다.</p><p>요약은 긴 대화의 앞부분을, 모델이 쓴 요약 글로 바꿔 요청에 싣는 장치입니다. 요약 글을 쓰려면 모델 요청이 한 번 더 나갑니다. 이 모델의 입력 한도는 400000토큰이라, 요약은 그 85%인 <code>요약이 켜지는 기준(토큰): 340000</code> 이상에서 시작합니다. 이 절의 요청은 그보다 훨씬 작아 요약은 일어나지 않았고, 요약을 켜 보는 실행도 하지 않았습니다.</p><h3>실제 모델을 부를 때의 안전 설정</h3><p>02절처럼 호출 한도를 두 곳에 줍니다. 바깥 호출 한도는 03절과 같은 10이고, general-purpose 명세의 자기 호출 한도는 2입니다. 한 번 실행의 모델 요청은 10에, 도구 <code>task</code>를 부른 횟수 × 2를 더한 값을 넘지 않습니다. 옮겨 둔 결과는 상태 칸에만 생기고, 디스크에는 쓰지 않습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 짧은 결과를 내는 규정 도구와 2,000줄 방문 기록 도구를 준비합니다. 3절은 손으로 만든 요청을 기본 한도의 작은 그래프에 넣어, 옮겨 두기와 기준을 봅니다. 4절은 한도를 10으로 바꿔 보고, 요약이 켜지는 기준을 셉니다. 5·6절은 기본 한도 그대로의 Deep Agent를 실제 모델로 한 번 실행하고, 7절은 요청 수와 예상 비용을 셉니다.</p><p>모델 요청은 6절 실행 셀에서만 나갑니다. 노트북 밖에서 같은 질문을 다섯 번 보냈을 때, 요청은 다섯 번 모두 3번이었습니다. 요금표로 어림한 예상 비용은 0.01달러 아래이고, 청구 금액이 아닙니다. 디스크에는 파일을 쓰지 않고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>기본 한도에서 88889자 방문 기록은 옮겨지고, 33·41자 규정 글은 그대로 남았습니다. 옮긴 뒤 도구 메시지는 안내 글이 되었고, 원래 결과는 상태 칸 <code>files</code>에 그대로 있었습니다. 옮길지는 모델이 아니라 결과 글자 수와 한도가 정합니다.</p><p>아래 표는 이 절이 확인한 값과 그 성격입니다. 구조 값은 코드가 정하는 값이고, 모델 판단 값은 모델이 고른 값입니다. 흔들리는 값은 실행마다 달라질 수 있어 결론에 쓰지 않습니다.</p>
""" + results + """
<p>6절 실행에서도 방문 기록은 <code>/large_tool_results/</code> 아래로 옮겨졌고, 도구 메시지는 안내 글이었습니다. 기록 훅으로 보니, 요청마다 모델이 받은 메시지 글자 수 합은 모두 방문 기록보다 작았습니다. 방문 기록 전체는 어느 요청에도 실리지 않았습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>""" + placeholder("B6_JUDGE") + """</p>
<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + placeholder("LOOK_B6") + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>파일 도구 일곱의 결과는 옮기지 않습니다. 설치판 <code>middleware/filesystem.py</code> 1199~1207행 목록에 <code>read_file</code>·<code>grep</code> 등이 있습니다. 대신 <code>read_file</code>은 1558~1561행에서, 읽은 글이 「4 × 한도」자 이상이면 스스로 잘라 내놓습니다. 이 노트북에서는 그 자르기를 실행하지 않았습니다.</li><li>글자 수가 기준과 꼭 같은 결과는 그대로 둡니다. 노트북 밖에서 모델 없이, 한도 10에서 40자 결과는 그대로이고 41자 결과는 옮겨지는 것을 보았습니다. 노트북에서는 운영 규정 41자로 기준을 넘는 쪽만 봅니다.</li><li>같은 이름 <code>FilesystemMiddleware</code>에 <code>backend=</code>를 주지 않으면, 설치판 1392행에서 기본 <code>StateBackend</code>를 씁니다. 에이전트에 다른 백엔드를 주었다면 새 미들웨어에도 같은 백엔드를 넘겨야 합니다. 이 노트북은 기본 백엔드만 써서, 그 차이는 실행하지 않았습니다.</li><li>사람 메시지도 설치판 1338행의 한도 50000(기준 200,000자)을 넘으면 파일로 옮기는 장치가 있습니다. 이 노트북에서는 실행하지 않았습니다.</li><li>공식 context engineering 문서는 안내 글에 결과의 첫 10줄을 미리보기로 붙인다고 적습니다. 설치판 0.7.0은 앞 다섯 줄과 뒤 다섯 줄을 붙이고, 이 절 출력도 그랬습니다. 다른 판을 쓰면 안내 글 모양을 먼저 확인합니다.</li><li>옮겨 둔 결과는 기본 백엔드에서는 그 실행의 상태 안에만 있습니다. 설치판 소스에서 옮겨 두기는 그 에이전트의 백엔드에 씁니다. 04절의 디스크 백엔드를 주면 기준 폴더 아래에 파일이 생기는 셈이지만, 이 노트북에서는 실행하지 않았습니다.</li><li>요약은 요청에 실린 메시지의 토큰 수가 기준 이상이면 시작합니다. 설치판 langchain <code>agents/middleware/summarization.py</code> 639~653행이 그 판정입니다. Deep Agents 요약은 밀려난 대화를 <code>/conversation_history/</code> 아래 파일로 적어 둔다고 독스트링이 적습니다. 이 노트북에서는 요약을 실행하지 않았습니다.</li><li>""" + placeholder("B7_PROBE") + """</li><li>방문 기록 2,000줄·분실물 자리 345·질문·한도 10은 흐름을 보여 주려고 실행 전에 정한 예입니다. 결과를 보고 바꾸지 않았습니다. 질문은 어떤 파일 도구를 쓰라고 정해 주지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>도구 결과가 「4 × 한도」자를 넘으면, 원래 결과는 상태 칸 <code>files</code>로 옮겨지고 도구 메시지에는 안내 글만 남습니다.</li><li>같은 이름 미들웨어로 한도를 바꾸면 기본 자리가 바뀌고, 작은 결과는 안내 글이 원래보다 길어질 수 있습니다.</li><li>모델은 안내 글만 받으므로, 미리보기에 없는 줄은 파일 도구로 다시 찾아야 합니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_06 + """\">06절</a>에서는 일을 서브에이전트에게 맡기는 장면을 봅니다. 서브에이전트가 상태 칸 <code>files</code>를 함께 쓰는 모양도 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 기본 한도에서 90,000자 도구 결과와 40자 도구 결과는 각각 어떻게 되나요?</p><p class="quiz-a">기본 기준은 80,000자입니다. 90,000자 결과는 상태 칸 <code>files</code>로 옮겨지고, 도구 메시지에는 안내 글만 남습니다. 40자 결과는 그대로 남습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 동료가 「한도 200이면 200글자를 넘을 때 옮긴다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 한도는 토큰 이름이고, 판정은 네 배인 800자를 넘는지로 합니다. 틀렸다면 노트북 3절 기준 셀을 다시 읽습니다.</p><p class="quiz-q">3. 한도를 10으로 낮추자 41자 결과의 도구 메시지가 658자가 되었습니다. 왜 길어졌나요?</p><p class="quiz-a">안내 글에는 늘 같은 설명 단락과 파일 위치, 미리보기가 붙기 때문입니다. 옮겨 두기는 결과가 충분히 클 때만 메시지 목록을 줄입니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 옮겨 둔 방문 기록의 345번째 줄 내용으로 답하려면, 모델에게 무엇이 필요한가요?</p><p class="quiz-a">안내 글에는 앞뒤 다섯 줄만 있어, 345번째 줄은 없습니다. 모델이 <code>grep</code>이나 <code>read_file</code> 같은 파일 도구로 옮겨 둔 파일을 다시 봐야 합니다. 틀렸다면 노트북 3절 안내 글 셀과 6절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/deepagents/context-engineering">Context engineering in Deep Agents</a></div>확인 2026-09-28 · 도구 결과가 20,000토큰을 넘으면 백엔드에 옮기고 파일 위치와 미리보기로 바꾼다고 적습니다. 미리보기는 첫 10줄로 적어, 설치판 0.7.0의 앞뒤 다섯 줄과 다릅니다. 요약은 입력 한도의 85%에서 시작해 10%를 남긴다고 적습니다.</li><li>설치판 deepagents 0.7.0 소스 <code>middleware/filesystem.py</code> 640행은 한 토큰을 네 글자로 어림하는 상수입니다. 1337~1338행이 두 한도의 기본값, 1199~1207행이 옮기지 않는 파일 도구 목록입니다. 2846행이 「4 × 한도」 이하이면 그대로 두는 판정, 3136~3160행이 도구 실행을 감싸는 훅입니다.</li><li>설치판 소스 <code>middleware/_message_eviction.py</code> 25~34행은 안내 글의 틀입니다. 37~63행은 미리보기이고, 열 줄이 넘으면 앞뒤 다섯 줄, 아니면 모든 줄을 붙입니다. 119~142행은 <code>/large_tool_results/</code> 아래에 쓰고 안내 글로 바꾸는 자리입니다.</li><li>설치판 소스 <code>graph.py</code> 201~235행은 같은 이름 미들웨어가 기본 자리를 바꾸는 자리입니다. 820~826행은 기본 <code>FilesystemMiddleware</code>를 만드는 자리입니다.</li><li>설치판 소스 <code>middleware/summarization.py</code> 249~286행은 입력 한도의 85%·10% 기본값입니다. 1609~1642행 독스트링은 밀려난 대화를 파일로 적고 상태의 메시지는 지우지 않는다고 적습니다. 판정은 langchain 1.4.0 <code>agents/middleware/summarization.py</code> 639~653행입니다.</li></ul>
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
        # 05절은 도구 파일에 함수를 더하지 않아 도구 파일을 쓰지 않습니다(02절 판 그대로 — 위 check_tools가 확인)
        path = write_notebook(LAB, "05", SLUG, "experiment", cells())
        print("wrote", path)
