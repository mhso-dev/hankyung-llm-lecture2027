from __future__ import annotations
# 2026-09-29 Ch 29 챕터 마감(검토 A-13): 이 파일은 Ch 25~29의 노트북 마크다운과 _src 주의 메모를 옛 글로 고치는 보조 스크립트입니다.
# 모듈 맨 위에서 곧바로 실행되고, Ch 25~29 개선본(각 챕터 qa/upgrade/author_NN.py가 씀)을 옛 글로 덮어쓰므로, 아래 줄에서 실행을 막습니다.
# 내용은 고치지 않았습니다(이 설명 세 줄과 아래 한 줄만 더함). 옮기거나 지울지는 사용자·강사가 정합니다.
raise SystemExit("옛 Part 6 보조 스크립트(part6b_review_fixes.py)입니다. 실행하면 Ch 25~29 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def write_notebook(path: Path, additions: dict[int, str], move_core_to: int | None = None) -> None:
    nb = json.loads(path.read_text())
    if move_core_to is not None:
        source = "".join(nb["cells"][3]["source"])
        marker = "\n\n### 코드 읽기와 비교 경계"
        if marker in source:
            intro, core = source.split(marker, 1)
            nb["cells"][3]["source"] = intro.rstrip() + "\n"
            target = "".join(nb["cells"][move_core_to]["source"]).rstrip()
            nb["cells"][move_core_to]["source"] = target + marker + core
    for index, text in additions.items():
        source = "".join(nb["cells"][index]["source"]).rstrip()
        if text not in source:
            nb["cells"][index]["source"] = source + "\n\n" + text + "\n"
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")


NB_ROOT = ROOT / "labs/part6"

# 기존 설명은 첫 환경 셀이 아니라 핵심 API가 처음 나오는 셀 앞에 둔다.
for filename, additions in {
    "01-일곱-가지-stream-mode.ipynb": {5: "`stream_mode` 목록을 넘기면 반복자의 각 항목은 `(mode, data)` 쌍이 됩니다. 모드 이름으로 먼저 분기한 뒤에 data의 구조를 읽어야 합니다.", 7: "두 모드를 함께 구독해도 그래프가 두 번 실행되는 것은 아닙니다. 한 실행에서 서로 다른 관찰 형태가 반환됩니다."},
    "02-토큰과-중간-진행-스트리밍.ipynb": {5: "`messages` 모드는 메시지 조각과 메타데이터를 반환합니다. 화면에는 내용이 있는 조각만 붙이고, 노드 이름과 시점은 메타데이터로 따로 보존합니다.", 7: "`custom`은 코드가 명시적으로 보낸 진행 사건이고, `updates`는 노드가 반환한 상태 변경분입니다. 둘을 같은 진행률로 표시하려면 계산 규칙을 추가해야 합니다."},
    "03-TTFT와-total-비교.ipynb": {5: "각 함수 호출은 독립된 그래프 실행입니다. 따라서 세 수치의 차이에는 모드 외에도 네트워크와 모델 상태가 함께 들어갑니다.", 9: "TTFT는 사용자가 첫 반응을 보는 시점을, total은 모든 사건을 소비한 시점을 근사합니다. 두 지표는 서로 다른 사용자 경험을 답합니다."},
}.items():
    write_notebook(NB_ROOT / "ch25-streaming/notebooks" / filename, additions)

for filename, additions in {
    "01-Subagent-도구-위임.ipynb": {5: "이 셀에서 중앙 에이전트는 교재용 고정 규정을 검토하는 전문 도구를 호출한 뒤 고객용 문장을 작성합니다. 출력의 환불 조건은 실습 규정 문자열 밖으로 확장되지 않아야 합니다.", 7: "문자 수 비교는 전달 범위만 확인합니다. 전문 답변의 정확성은 고정 규정과 답변을 항목별로 대조해 따로 검증해야 합니다."},
    "02-Handoff-상태-전환.ipynb": {5: "`dispatch()`는 현재 메시지와 저장된 담당자를 함께 읽고 새 `active_agent`만 반환합니다. `respond()`는 이 갱신된 상태를 받아 답변을 만듭니다.", 9: "첫 호출과 둘째 호출이 같은 `thread_id`를 써야 체크포인터가 이전 담당자를 찾을 수 있습니다. 다른 ID를 쓰면 독립된 대화로 처리됩니다."},
    "03-Router-분류와-병렬-실행.ipynb": {5: "구조화 분류 결과의 각 이름은 독립적인 작업만 병렬로 실행합니다. 한 결과가 다음 작업의 입력이라면 이 구조를 순차 그래프로 바꾸어야 합니다.", 7: "`results`의 키 집합과 `route.destinations`를 비교하면 선택된 분야가 모두 실행됐는지 확인할 수 있습니다. 이 검사는 분류 자체가 올바른지는 판정하지 않습니다."},
    "04-호출-수-비용-종료-조건-비교.ipynb": {7: "Subagent의 종료 값은 전문 도구가 반환한 업무 결과입니다. `records`의 호출 수나 토큰 수와 서로 다른 층의 값입니다.", 13: "Router의 분류 1회와 선택된 전문 작업 호출을 구분해 기록합니다. 집계표를 읽을 때는 호출 수가 어떤 역할에서 발생했는지까지 보아야 합니다."},
}.items():
    write_notebook(NB_ROOT / "ch26-delegation/notebooks" / filename, additions)

ch27_notes = {
    "01-하네스와-일곱-기능.ipynb": {7: "모든 값이 `True`라는 결과는 설치된 소스에 조립 경로가 있다는 뜻입니다. 각 기능이 실제 요청에서 선택되는지는 뒤 절의 실행 결과로 확인합니다."},
    "02-create-deep-agent와-도구.ipynb": {7: "`invoke()`가 반환한 메시지 목록에서 AI의 `tool_calls`, `course_lookup` ToolMessage, 마지막 AIMessage를 순서대로 찾습니다. 이 순서가 도구가 실제로 실행된 근거입니다."},
    "03-플래닝과-시스템-프롬프트.ipynb": {7: "`todos` 상태의 `completed`는 모델이 해당 항목을 완료로 기록했다는 뜻입니다. 버전 확인 결과나 설명 산출물을 실제로 검증했다는 증거가 아니므로, 산출물을 따로 검사해야 합니다.", 9: "감소율은 현재 실행의 사용량이 아니라 릴리스 PR에 적힌 5,395와 1,895를 재계산한 값입니다. 예제의 todo 상태와 서로 다른 근거입니다."},
    "04-파일시스템과-중간-결과.ipynb": {7: "쓰기 반환값만으로 내용 보존을 결론내리지 않습니다. 같은 가상 경로를 다시 읽은 본문과 목록을 함께 검사합니다."},
    "05-컨텍스트-관리와-오프로딩.ipynb": {7: "ToolMessage의 길이와 안내 문구를 출력해 원문 전체가 대화에 남지 않았는지 확인합니다. 마지막 AI 답변의 내용은 이 셀의 검사 대상이 아닙니다.", 9: "실제 파일 존재와 파일의 원문 길이를 확인해야 오프로딩을 검증할 수 있습니다. 미리보기 문장만으로는 저장 성공을 알 수 없습니다."},
    "06-서브에이전트-위임.ipynb": {7: "부모에서 보이는 `task` 호출과 반환 보고를 검사합니다. 자식 문맥의 `source_lookup` 세부 호출은 부모 메시지에 노출되지 않으므로 별도 관측이 필요합니다."},
    "07-출처-검증형-deep-research.ipynb": {7: "결과 파일에서 주장과 출처 ID, 조사 범위 한계를 함께 확인합니다. 제공된 두 자료 밖의 웹 문서를 찾았다고 해석하면 안 됩니다."},
    "08-통합-실행과-운영-한계.ipynb": {7: "허용 경로와 차단 경로를 한 요청에 넣어 성공과 거부를 함께 관찰합니다. 단순히 최종 답변을 읽지 말고 도구 메시지를 확인해야 합니다.", 9: "종료 조건은 허용된 보고서의 내용과 차단 도구의 `permission denied` 결과를 모두 확인합니다. 모델의 완료 문장만으로는 충분하지 않습니다."},
}
for filename, additions in ch27_notes.items():
    write_notebook(NB_ROOT / "ch27-deepagents/notebooks" / filename, additions, move_core_to=5)

ch28_notes = {
    "01-MCP-구조와-capability-협상.ipynb": {6: "`async def` 는 코루틴 함수를 정의하며, 함수를 호출한 것만으로는 본문이 실행되지 않습니다. `await discover()`가 코루틴을 실행하고 결과를 기다립니다. `async with Client(mcp)`는 연결을 열고 블록을 벗어날 때 연결을 정리합니다.", 8: "목록 조회는 정의를 반환하고, `call_tool`\xB7`read_resource`\xB7`get_prompt`는 각 구성 요소를 실제로 사용합니다. 이 셀에서 실행 결과, URI 본문, 메시지 틀을 서로 다른 반환값으로 읽습니다."},
    "02-FastMCP-로컬-서버-제작.ipynb": {6: "앞 절의 비동기 호출을 다시 사용합니다. `async def` 본문은 `await`할 때 실행되고, `async with Client(...)`는 등록 목록을 읽는 동안만 연결을 유지합니다.", 8: "완성 서버의 목록은 도구\xB7리소스\xB7프롬프트가 각각 하나씩 등록됐는지 확인합니다. 서버 파일이 존재하는 것과 클라이언트가 구성 요소를 발견하는 것을 따로 검사합니다."},
    "03-stdio와-원격-전송-권한-경계.ipynb": {6: "수정 후에는 전체 `os.environ`을 복사하지 않고 서버 실행에 필요한 키만 새 사전에 넣습니다. 출력은 전달된 키 이름을 비교하며 비밀 값은 보여 주지 않습니다.", 8: "`StdioServerParameters`의 `command`, `args`, `env`는 하위 프로세스를 시작하는 입력입니다. 도구 반환값이 예상 규정과 같은지까지 확인해야 전송 설정과 서버 실행을 함께 검증할 수 있습니다."},
    "04-LangChain-MCP-클라이언트-연동.ipynb": {6: "직접 작성한 LangChain 도구와 MCP에서 변환한 도구에 같은 입력 사전을 넘긴 뒤 반환 메시지를 비교합니다. 호출 형태가 같아도 MCP 도구는 어댑터와 전송 계층을 거칩니다."},
    "05-도구-정의와-첫-호출-토큰.ipynb": {8: "`schema_chars`는 도구 정의를 JSON으로 직렬화한 문자 수입니다. 모델이 보고한 토큰 수와 동일한 단위가 아니므로 증가 방향을 설명하는 보조 측정값으로만 사용합니다.", 10: "세 조건은 같은 질문을 보내지만 도구 정의의 수와 내용이 함께 달라집니다. 따라서 입력 토큰 차이를 MCP 연결 하나의 효과로 해석하지 않습니다."},
}
for filename, additions in ch28_notes.items():
    write_notebook(NB_ROOT / "ch28-mcp/notebooks" / filename, additions)

ch29_notes = {
    "01-에이전트-평가-세-전략.ipynb": {7: "세 평가 함수에 같은 고정 궤적을 넘긴 뒤 각각 마지막 답, 첫 도구 호출, 전체 호출 순서를 읽는지 비교합니다.", 9: "나쁜 경로는 최종 답을 같게 유지한 채 도구 호출만 늘립니다. 이 비교로 최종 응답 평가가 내부 낭비를 놓칠 수 있음을 확인합니다."},
    "02-궤적-매칭-네-모드.ipynb": {7: "`strict`는 순서까지 같아야 하고 `unordered`는 같은 호출이 있으면 순서를 무시합니다. 두 결과를 같이 보면 요구 사항이 순서에 의존하는지 판단할 수 있습니다.", 9: "`subset`은 실제 호출이 기준 범위 안인지, `superset`은 실제 호출이 기준의 필수 호출을 모두 포함하는지 묻습니다. 허용 누락과 허용 추가의 방향이 반대입니다."},
    "03-LLM-judge로-궤적-평가.ipynb": {7: "이 셀에서만 judge 모델을 실제로 호출합니다. 반환 사전의 `score`와 `comment`를 함께 저장해 판정과 근거를 같이 검토합니다.", 9: "권한, 금지 도구, 필수 순서처럼 코드로 정확히 표현할 수 있는 규칙은 결정적 검사로 남깁니다. judge는 의미 판단이 필요한 범위를 보완합니다."},
    "04-운영-지표와-Ch18-궤적-비교.ipynb": {7: "Ch18 JSON의 필드와 개수를 먼저 확인합니다. 파일이 존재해도 예상한 스키마와 다르면 공통 열 변환을 중단해야 합니다.", 11: "Ch21 기록의 `agent_supported`는 Ch18의 `quality/5`와 의미가 다릅니다. 같은 `final_score`로 변환해도 원래 판정 척도를 `trace_source`와 함께 보존합니다.", 17: "표본이 세 건이므로 nearest-rank p95는 정렬한 값의 최댓값입니다. 이 값은 계산 방법을 보여 주지만 안정적인 운영 기준을 만들 정도의 표본은 아닙니다."},
}
for filename, additions in ch29_notes.items():
    write_notebook(NB_ROOT / "ch29-agent-evaluation/notebooks" / filename, additions, move_core_to=5)


def replace(path: Path, old: str, new: str) -> None:
    source = path.read_text()
    if old not in source:
        raise AssertionError(f"missing text in {path}: {old[:80]}")
    path.write_text(source.replace(old, new))


# Ch26-01: 모델이 참조할 수 있는 교재용 고정 환불 규정을 명시한다.
p = NB_ROOT / "ch26-delegation/notebooks/01-Subagent-도구-위임.ipynb"
nb = json.loads(p.read_text())
nb["cells"][4]["source"] = '''# 교재용 고정 규정을 가진 전문 에이전트를 도구로 감쌍니다.
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

TRAINING_POLICY = """[교재용 환불 규정]
예정 배송일보다 3일 이상 지연되고 미배송 상태면 고객이 환불 검토를 요청할 수 있다.
담당자는 주문 번호와 현재 배송 상태를 확인한 뒤 환불 가능 여부를 안내한다."""
model = init_chat_model(f"openai:{MODEL}", reasoning_effort="none")
calls: list[str] = []
specialist = create_agent(model, tools=[], system_prompt="제공된 교재용 규정만 근거로 두 문장 이내로 답하세요.")

@tool
def policy_specialist(question: str) -> str:
    """교재용 환불 규정에서 근거를 확인합니다."""
    calls.append("policy_specialist")
    content = f"{TRAINING_POLICY}\\n\\n[고객 질문]\\n{question}"
    result = specialist.invoke({"messages": [{"role": "user", "content": content}]})
    return result["messages"][-1].text

supervisor = create_agent(model, tools=[policy_specialist], system_prompt="환불 요청은 policy_specialist를 한 번 호출하고, 도구가 제공한 규정 범위 안에서만 답하세요.")
'''
p.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")

# Ch26-02: 외부 모델을 쓰지 않는 로컬 StateGraph 실습에서 키와 모델 설정을 제거한다.
p = NB_ROOT / "ch26-delegation/notebooks/02-Handoff-상태-전환.ipynb"
nb = json.loads(p.read_text())
nb["cells"][1]["source"] = "## 실행 환경 준비\n\n이 노트북은 로컬 StateGraph와 메모리 체크포인터만 사용합니다. 모델 API 키는 필요하지 않습니다.\n"
nb["cells"][2]["source"] = '''# 로컬 그래프 실행에 필요한 패키지만 설치합니다.
%pip install -q langgraph==1.2.11
from importlib.metadata import version

print({"langgraph": version("langgraph"), "execution": "local graph only"})
'''
p.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")

# Source accuracy corrections.
src26 = ROOT / "textbook/part6/ch26-delegation/_src"
replace(src26 / "01-Subagent-도구-위임.html", "환불 전문가는 내부 기록 전체가 아니라 환불 판단에 필요한 고객 질문만 받아도 됩니다.", "환불 전문가는 교재용 고정 환불 규정과 판단에 필요한 고객 질문만 받습니다.")
replace(src26 / "01-Subagent-도구-위임.html", "policy_specialist를 @tool로 정의하고 내부에서 모델을 호출합니다.", "policy_specialist를 @tool로 정의하고 내부에서 교재용 고정 규정과 고객 질문을 함께 넘겨 모델을 호출합니다.")
replace(src26 / "02-Handoff-상태-전환.html", '<p>설치 셀은 Python 3.12 환경에 LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11을 고정합니다. 예상 API 비용은 1달러 미만이며 키 값은 출력하지 않습니다.</p>', '<p>설치 셀은 Python 3.12 환경에 LangGraph 1.2.11만 고정합니다. 모든 노드는 로컬 Python 함수이며 모델 API 키를 사용하지 않습니다.</p>')
replace(src26 / "02-Handoff-상태-전환.html", '<p>이 실험은 한 질문과 한 실행 환경의 결과입니다. 모델 응답 내용과 지연 시간은 실행할 때마다 달라질 수 있습니다. 구조의 품질을 비교하려면 여러 질문, 반복 실행, 오류율, 사용자 수정 횟수를 추가로 측정해야 합니다.</p>', '<p>이 결과는 같은 <code>thread_id</code>의 메모리에서 담당자 상태가 유지된 것을 보여 줍니다. 프로세스를 다시 시작했을 때의 영속성이나 실제 주문 존재 여부는 검증하지 않습니다.</p>')

src27 = ROOT / "textbook/part6/ch27-deepagents/_src"
notes = {
    "01-하네스와-일곱-기능.html": "<ul><li>소스 문자열 검색은 조립 경로의 존재만 보여 줍니다. 실제 도구 선택과 산출물은 기능별 실행으로 확인합니다.</li><li>이 장은 설치된 <code>deepagents==0.7.0</code> 소스와 릴리스 노트를 기준으로 읽습니다.</li></ul>",
    "02-create-deep-agent와-도구.html": "<ul><li><code>create_deep_agent</code>가 반환한 그래프는 <code>invoke</code>할 때 모델과 도구를 실행합니다.</li><li>도구 선택 여부는 최종 문장만으로 판단하지 말고 <code>tool_calls</code>와 <code>ToolMessage</code>를 함께 검사합니다.</li></ul>",
    "03-플래닝과-시스템-프롬프트.html": "<ul><li><code>completed</code>는 모델이 todo를 완료 상태로 기록한 값입니다. 버전 정보나 설명 산출물의 정확성은 따로 검증합니다.</li><li>65%는 릴리스 PR의 제한된 첫 턴 수치를 재계산한 값이며 이 노트북의 실측 사용량이 아닙니다.</li></ul>",
    "04-파일시스템과-중간-결과.html": "<ul><li>사용자 입력을 경로로 바로 사용하지 않고 허용된 실습 루트 아래로 제한합니다.</li><li>쓰기 반환값과 재읽기 본문을 함께 검사해 실제 저장을 확인합니다.</li></ul>",
    "05-컨텍스트-관리와-오프로딩.html": "<ul><li>ToolMessage의 미리보기는 원문 파일의 대체물이 아닙니다. 후속 판단에 원문이 필요하면 파일을 다시 읽어야 합니다.</li><li>실행별 오프로딩 파일의 보존 기간과 삭제 시점을 정합니다.</li></ul>",
    "06-서브에이전트-위임.html": "<ul><li>부모의 <code>task</code> 반환은 자식 작업의 요약입니다. 자식의 세부 도구 궤적과 산출물 검증은 별도 관측으로 남깁니다.</li><li>위임 지시에는 사용할 자료, 출처 표기, 완료 조건을 함께 적습니다.</li></ul>",
    "07-출처-검증형-deep-research.html": "<ul><li>이 실습의 <code>source_lookup</code>은 제공된 두 자료만 읽습니다. 웹 전체를 조사했다는 결론을 내릴 수 없습니다.</li><li>부모 마지막 응답의 usage는 서브에이전트 전체 사용량이 아닙니다.</li></ul>",
    "08-통합-실행과-운영-한계.html": "<ul><li>권한 판정은 도구 실행 직전에 적용합니다. 모델이 차단 경로를 요청해도 실제 파일은 만들어지지 않아야 합니다.</li><li>허용된 파일 본문, 거부 ToolMessage, 차단 파일의 부재를 함께 검사합니다.</li></ul>",
}
for filename, ul in notes.items():
    p = src27 / filename
    source = p.read_text()
    b7 = source.index('<h2 id="b7">')
    b8 = source.index('<h2 id="b8">')
    source = source[:b7] + '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2>' + ul + '\n' + source[b8:]
    p.write_text(source)

replace(src27 / "03-플래닝과-시스템-프롬프트.html", "이 상태는 계획 도구가 실제로 추가됐음을 보여 줍니다.", "이 상태는 계획 도구가 추가되고 모델이 두 항목을 완료로 기록했음을 보여 줍니다. 버전 확인과 결과 설명이 실제로 검증됐다는 증거는 아닙니다.")
replace(src27 / "03-플래닝과-시스템-프롬프트.html", "모델은 write_todos를 두 번 호출했고 두 항목을 모두 completed로 기록했습니다.", "모델은 write_todos를 두 번 호출했고 두 항목을 모두 completed로 기록했습니다. completed는 모델이 남긴 계획 상태이며 업무 결과 검증은 아닙니다.")
replace(src27 / "05-컨텍스트-관리와-오프로딩.html", "최종 모델은 미리보기의 첫 문장을 요약했습니다. ", "")
replace(src27 / "07-출처-검증형-deep-research.html", "입력 2,367·출력 6토큰", "입력 2,379·출력 34·합계 2,413토큰")
replace(src27 / "07-출처-검증형-deep-research.html", "<li>실제 실행은 final.</li>", "<li>실제 실행은 <code>/research/final.md</code>에 주장, 출처 ID, 조사 범위 한계를 저장했습니다.</li>")
replace(src27 / "08-통합-실행과-운영-한계.html", "<li>/run/report.</li>", "<li><code>/run/report.md</code>의 완료 내용과 <code>/blocked.txt</code> 쓰기 거부를 함께 확인했습니다.</li>")

src29 = ROOT / "textbook/part6/ch29-agent-evaluation/_src"
replacements29 = {
    "01-에이전트-평가-세-전략.html": "<ul><li>이 절의 궤적은 코드로 만든 고정 예시입니다. 실제 모델 선택률이나 지연 시간을 보여 주지 않습니다.</li><li>최종 답, 한 단계, 전체 궤적 평가가 읽는 메시지 범위를 평가 정의에 남깁니다.</li></ul>",
    "02-궤적-매칭-네-모드.html": "<ul><li>이 절은 로컬 평가 함수와 고정 메시지 목록만 사용합니다. 모델 API 호출은 없습니다.</li><li>인자 무시 옵션을 쓰면 검사 범위가 좁아지므로 무시하는 필드와 이유를 평가 정의에 기록합니다.</li></ul>",
    "04-운영-지표와-Ch18-궤적-비교.html": "<ul><li>이 절은 Ch18과 Ch21의 저장 파일을 읽으며 모델을 다시 호출하지 않습니다. 원본 파일의 기록 시점과 필드 단위를 함께 확인합니다.</li><li>표본 세 건의 p95는 nearest-rank 방법에서 최댓값이 됩니다. 이 수치만으로 운영 기준을 정하지 않습니다.</li></ul>",
}
for filename, ul in replacements29.items():
    p = src29 / filename
    source = p.read_text()
    b7 = source.index('<h2 id="b7">')
    b8 = source.index('<h2 id="b8">')
    p.write_text(source[:b7] + '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2>' + ul + '\n' + source[b8:])

print("Part6b review corrections applied")
