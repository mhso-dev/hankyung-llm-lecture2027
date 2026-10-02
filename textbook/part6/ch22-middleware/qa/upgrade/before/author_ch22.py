from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHAPTER = ROOT / "textbook/part6/ch22-middleware"
LAB = ROOT / "labs/part6/ch22-middleware"


def md(source: str, lesson_part: str | None = None) -> dict:
    metadata = {"lesson_part": lesson_part} if lesson_part else {}
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": source.splitlines(keepends=True)}


def code(source: str, lesson_part: str | None = None) -> dict:
    metadata = {"lesson_part": lesson_part} if lesson_part else {}
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": metadata, "outputs": [], "source": source.splitlines(keepends=True)}


INSTALL = '''%pip install -q "langchain==1.4.0" "langchain-openai==1.6.0" "langgraph==1.2.11" "python-dotenv==1.2.3"
from importlib.metadata import version
print("langchain", version("langchain"))
print("langchain-openai", version("langchain-openai"))
print("langgraph", version("langgraph"))'''


FAKE = '''# 정해 둔 응답으로 미들웨어 실행 순서를 재현합니다.
from typing import Any
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain.tools import tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
class ScriptedModel(BaseChatModel):
    replies: list[AIMessage]
    index: int = 0
    @property
    def _llm_type(self) -> str: return "scripted-model"
    def _generate(self, messages: Any, stop: Any = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
        reply = self.replies[min(self.index, len(self.replies) - 1)]
        self.index += 1
        return ChatResult(generations=[ChatGeneration(message=reply)])
    def bind_tools(self, tools: Any, *, tool_choice: Any = None, **kwargs: Any) -> "ScriptedModel":
        return self
@tool
def lookup_hours(day: str) -> str:
    """자료실 운영 시간을 요일로 조회합니다."""
    return "평일 09:00~20:00" if day == "평일" else "토요일 10:00~17:00"'''


LESSONS = {
"01-미들웨어와-6개-훅": {
"title":"미들웨어와 6개 훅","format":"experiment","hours":"강의 1h · 실습 2h","terms":"6",
"question":"미들웨어의 여섯 훅은 에이전트 실행의 어느 지점에서 어떤 순서로 호출될까요?",
"goals":["여섯 훅을 에이전트 전체·모델·도구 범위로 구분할 수 있습니다.","노드형 훅과 감싸기형 훅의 반환 방식 차이를 설명할 수 있습니다.","실제 도구 호출 trace에서 각 훅의 실행 위치를 확인할 수 있습니다."],
"why":"Ch20에서는 모델 노드와 ToolNode를 직접 연결했고 Ch21에서는 create_agent가 같은 반복을 컴파일된 그래프로 만든다는 사실을 확인했습니다. 운영 요구가 추가될 때마다 모델 노드와 도구 함수 본문을 수정하면 핵심 업무 코드와 횡단 기능이 섞입니다. 미들웨어는 반복 구조의 정해진 지점에 검증, 기록, 재시도를 연결합니다. 이 절에서는 먼저 훅의 정확한 이름과 실행 범위를 확인합니다.",
"prior":"Ch16의 guardrails.py는 모델 호출 전후에 validate_query, mask_pii, CallBudget, retry_with_fallback을 직접 호출했습니다. Ch20에서는 도구 요청과 ToolMessage 사이를 ToolNode가 맡았습니다. 이번 절은 그 사이 지점을 create_agent의 middleware 인자로 노출합니다.",
"concept":"공항 보안 절차를 떠올려 봅니다. 탑승 수속 전체의 시작과 끝, 탑승구 진입 전후, 수하물 검사 전후는 서로 다른 검사 지점입니다. 미들웨어도 에이전트 전체에는 before_agent와 after_agent, 각 모델 호출에는 before_model·wrap_model_call·after_model, 각 도구 호출에는 wrap_tool_call을 제공합니다. 노드형 훅은 정해진 지점에서 한 번 실행되고 상태 갱신 딕셔너리를 반환할 수 있습니다. 감싸기형 훅은 handler를 호출하기 전후를 모두 제어하며 재시도하거나 요청을 바꾸거나 호출을 생략할 수도 있습니다.",
"observe":"학습용 모델은 첫 응답에서 lookup_hours 도구를 한 번 요청하고 두 번째 응답에서 종료합니다. 출력 trace에는 before_agent가 한 번, 모델 관련 세 훅이 두 번, wrap_tool_call이 한 번, after_agent가 한 번 나타납니다. 여섯 훅이라는 말은 여섯 개의 독립 오류 이벤트를 뜻하지 않습니다. 오류는 wrap_model_call 또는 wrap_tool_call에서 예외로 관찰하고 종료는 after_agent에서 관찰합니다.",
"notes":["공식 LangChain 1.4.0의 여섯 훅은 before_agent, before_model, wrap_model_call, wrap_tool_call, after_model, after_agent입니다.","노드형 훅에서 상태를 바꾸려면 딕셔너리를 반환합니다. 감싸기형 훅은 handler의 반환값을 보존하거나 문서가 허용한 형식으로 바꿉니다.","첫 기능 셀에서 실제 OpenAI API 연결을 확인한 뒤, 훅의 정확한 순서는 정해 둔 응답을 쓰는 검사 모델로 재현합니다. 키 값은 출력하지 않습니다."],
"next":"다음 절에서는 Ch16의 정규식 기반 mask_pii를 LangChain의 PIIMiddleware로 옮기고 입력과 출력 적용 범위를 비교합니다.",
"quiz":[("에이전트 실행당 한 번 호출되는 훅 두 개는 무엇인가요?","before_agent와 after_agent입니다."),("handler를 여러 번 호출해 재시도를 구현할 수 있는 모델 훅은 무엇인가요?","wrap_model_call입니다."),("도구 오류를 관찰하기에 알맞은 훅은 무엇인가요?","wrap_tool_call에서 handler 호출 예외를 처리합니다."),("after_model은 왜 한 실행에서 여러 번 호출될 수 있나요?","도구를 사용한 에이전트는 모델을 여러 차례 호출하기 때문입니다.")],
"cells":[("패키지 버전 확인",INSTALL),("훅 확인용 결정적 모델 준비",FAKE),("도구와 여섯 훅 trace 준비",'''from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain.tools import tool

TRACE = []
@tool
def lookup_hours(day: str) -> str:
    """자료실 운영 시간을 요일로 조회합니다."""
    return "평일 09:00~20:00" if day == "평일" else "토요일 10:00~17:00"

class SixHookTrace(AgentMiddleware):
    def before_agent(self, state: Any, runtime: Any) -> None: TRACE.append("before_agent")
    def before_model(self, state: Any, runtime: Any) -> None: TRACE.append("before_model")
    def wrap_model_call(self, request: Any, handler: Any) -> Any:
        TRACE.append("wrap_model:before"); result = handler(request); TRACE.append("wrap_model:after"); return result
    def wrap_tool_call(self, request: Any, handler: Any) -> Any:
        TRACE.append("wrap_tool:before"); result = handler(request); TRACE.append("wrap_tool:after"); return result
    def after_model(self, state: Any, runtime: Any) -> None: TRACE.append("after_model")
    def after_agent(self, state: Any, runtime: Any) -> None: TRACE.append("after_agent")'''),("도구 1회인 에이전트 실행",'''scripted = ScriptedModel(replies=[
    AIMessage(content="", tool_calls=[{"name":"lookup_hours","args":{"day":"평일"},"id":"call_1","type":"tool_call"}]),
    AIMessage(content="평일 운영 시간은 09:00~20:00입니다."),
])
agent = create_agent(scripted, tools=[lookup_hours], middleware=[SixHookTrace()])
result = agent.invoke({"messages":[{"role":"user","content":"평일 운영 시간은?"}]})
print("trace:", TRACE)
print("answer:", result["messages"][-1].text)
assert TRACE.count("before_model") == 2 and TRACE.count("wrap_tool:before") == 1'''),("훅 호출 횟수 집계",'''from collections import Counter
counts = Counter(item.split(":")[0] for item in TRACE)
print(dict(counts))
assert TRACE[0] == "before_agent" and TRACE[-1] == "after_agent"'''),("실제 API 연결과 비용 확인",'''import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / ".env").is_file(): load_dotenv(folder / ".env"); break
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY가 필요합니다."
live = init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none")
reply = live.invoke("LangChain 에이전트 미들웨어를 한국어 한 문장으로 정의하세요.")
usage = reply.usage_metadata or {}
cost = usage.get("input_tokens",0)/1_000_000*0.75 + usage.get("output_tokens",0)/1_000_000*4.50
print("answer:", reply.text)
print("usage:", usage)
print("estimated_cost_usd:", round(cost,6))
assert cost < 1.0''')]
},
"02-PII-마스킹-이식": {
"title":"PII 마스킹 이식","format":"paired","hours":"강의 1h · 실습 2h","terms":"5",
"question":"Ch16의 PII 마스킹을 PIIMiddleware로 옮기면 적용 지점과 코드가 어떻게 달라질까요?",
"goals":["PII와 마스킹 전략을 설명할 수 있습니다.","apply_to_input과 apply_to_output의 적용 범위를 구분할 수 있습니다.","Ch16 정규식 함수와 내장 미들웨어의 책임 차이를 비교할 수 있습니다."],
"why":"개인 식별 정보(PII)는 질문, 모델 답변, 도구 결과 어디에서든 나타날 수 있습니다. Ch16에서는 guarded_generate 안에서 입력과 문서를 직접 mask_pii에 전달했습니다. 에이전트에서는 모델과 도구가 반복되므로 같은 호출을 여러 위치에 빠뜨리지 않고 적용해야 합니다. PIIMiddleware는 이 반복 지점을 설정으로 모읍니다.",
"prior":"Ch16 guardrails.py의 mask_pii는 email, phone, rrn, card 정규식을 순서대로 적용하고 종류별 개수를 반환했습니다. 테스트는 가상 이메일과 전화번호가 가려지고 출처 태그는 유지되는지 확인했습니다. 여기서는 같은 가상 이메일을 사용해 직접 함수와 미들웨어 결과를 비교합니다.",
"concept":"문서 발송 전에 담당자가 특정 칸을 검게 가리는 절차를 생각해 봅니다. 어떤 문서를 가릴지와 어떤 정보 유형을 찾을지를 따로 정해야 합니다. PIIMiddleware의 pii_type은 찾을 유형, strategy는 block·redact·mask·hash 중 처리 방법입니다. apply_to_input은 사용자가 보낸 메시지, apply_to_output은 모델 답변, apply_to_tool_results는 도구 결과에 적용합니다. 한 인스턴스는 한 유형을 맡으므로 이메일과 신용카드를 함께 다루려면 각각 추가합니다.",
"observe":"Before의 Ch16 축소 함수는 호출자가 mask_pii를 호출하지 않으면 원문 이메일이 그대로 모델에 전달됩니다. After의 PIIMiddleware는 create_agent의 실행 흐름 안에서 사용자 이메일과 모델이 만든 이메일을 모두 부분 마스킹합니다. 기본 내장 email 검출기의 mask 결과는 도메인을 일부 남길 수 있으므로 완전 삭제가 필요한 정책이라면 redact 또는 block을 선택해야 합니다.",
"notes":["PIIMiddleware는 비밀 관리 시스템이 아닙니다. 이미 외부 로그에 기록된 값은 되돌려 지우지 못하므로 가장 이른 입력 경계에 둡니다.","정규식 검출에는 오탐과 누락이 있습니다. 주민등록번호처럼 한국 고유 유형은 detector 함수를 직접 제공하고 별도 테스트를 작성합니다.","출력 마스킹은 안전한 응답을 보장하지 않습니다. 허용되지 않은 정보 조회 자체는 권한 검사로 차단해야 합니다."],
"next":"다음 절에서는 길어진 메시지를 줄이는 Ch16의 summarize_history와 SummarizationMiddleware를 비교해 Compress의 보존 범위를 확인합니다.",
"quiz":[("apply_to_tool_results는 무엇을 제어하나요?","도구가 반환한 ToolMessage 내용에도 PII 처리를 적용할지 정합니다."),("email과 credit_card를 함께 처리하려면 어떻게 하나요?","유형별 PIIMiddleware 인스턴스를 middleware 목록에 추가합니다."),("mask와 block의 차이는 무엇인가요?","mask는 일치한 값을 일부 가리고 실행을 계속하며 block은 검출 시 실행을 중단합니다."),("한국 주민등록번호 검출에서 추가할 것은 무엇인가요?","프로젝트 정책에 맞는 사용자 정의 detector와 오탐·누락 회귀 테스트입니다.")],
"cells":[("패키지 버전 확인",INSTALL),("결정적 모델 준비",FAKE),("Ch16 원본 마스킹 함수 재현",'''import re
PII_PATTERNS = {
 "email": re.compile(r"(?<![\\w.])[\\w.+-]+@[\\w.-]+\\.[A-Za-z]{2,}(?![\\w.])"),
 "phone": re.compile(r"(?<!\\d)01[016789][ -]?\\d{3,4}[ -]?\\d{4}(?!\\d)"),
 "rrn": re.compile(r"(?<!\\d)\\d{6}[ -]?[1-4]\\d{6}(?!\\d)"),
 "card": re.compile(r"(?<!\\d)(?:\\d[ -]?){15}\\d(?!\\d)"),
}
def mask_pii(text: str) -> tuple[str, dict[str, int]]:
    masked, counts = text, {}
    for name, pattern in PII_PATTERNS.items():
        masked, count = pattern.subn(f"<{name.upper()}_MASKED>", masked)
        counts[name] = count
    return masked, counts
sample = "learner@example.com 010-1234-5678 900101-1234567 1234-5678-9012-3456"
direct_masked, direct_counts = mask_pii(sample)
print(direct_masked); print(direct_counts)
assert direct_counts == {"email":1,"phone":1,"rrn":1,"card":1}'''),("Before: 호출을 빠뜨린 경로",'''before_model = ScriptedModel(replies=[AIMessage(content="확인: learner@example.com")])
before_agent = create_agent(before_model, tools=[])
before = before_agent.invoke({"messages":[{"role":"user","content":sample}]})
print([message.text for message in before["messages"]])
assert "learner@example.com" in before["messages"][0].text''',"before"),("After: 입력과 출력 미들웨어 적용",'''from langchain.agents.middleware import PIIMiddleware
after_model = ScriptedModel(replies=[AIMessage(content="확인: learner@example.com")])
after_agent = create_agent(after_model, tools=[], middleware=[
    PIIMiddleware("email", strategy="mask", apply_to_input=True, apply_to_output=True)
])
after = after_agent.invoke({"messages":[{"role":"user","content":"회신: learner@example.com 입니다."}]})
texts = [message.text for message in after["messages"]]
print(texts)
assert all("learner@example.com" not in text for text in texts)''',"after"),("적용 범위 비교",'''print("Ch16 직접 치환:", direct_masked)
print("Ch16 종류별 개수:", direct_counts)
print("미들웨어 입력:", after["messages"][0].text)
print("미들웨어 출력:", after["messages"][-1].text)
print("차이: 내장 email 한 유형만 부분 마스킹하며 Ch16의 네 유형·치환 문자열·개수 반환은 자동 보존하지 않습니다.")
print("estimated_cost_usd: 0.0 (결정적 로컬 모델)")''',"after")]
},
"03-요약-압축과-Compress": {
"title":"요약 압축과 Compress","format":"paired","hours":"강의 1h · 실습 2h","terms":"6",
"question":"자동 요약 압축은 언제 실행되며 최근 메시지와 중요 조건을 어떻게 보존해야 할까요?",
"goals":["trigger와 keep 조건을 설명할 수 있습니다.","Ch16 수동 요약 호출과 SummarizationMiddleware의 실행 지점을 비교할 수 있습니다.","압축 결과에서 조건·예외·출처가 남았는지 확인할 수 있습니다."],
"why":"대화가 길어지면 모든 메시지를 모델에 전달하는 비용이 커지고 모델이 현재 질문에 필요한 사실을 찾기 어려워집니다. Ch8의 Compress는 필요한 정보를 남기고 반복을 줄이는 전략이었습니다. Ch16에서는 summarize_history를 직접 호출했습니다. 미들웨어는 모델 호출 직전에 임계값을 검사하고 오래된 메시지를 요약해 이 전략을 반복 루프에 연결합니다.",
"prior":"Ch8에서는 압축할 때 결정·조건·예외·출처를 보존해야 한다고 배웠습니다. Ch16 summarize_history는 system 메시지와 최근 대화를 남기고, 오래된 대화를 summarizer 함수에 넘긴 뒤 참고용 요약 메시지로 바꿨습니다. 이번 절은 같은 메시지 수 조건을 미들웨어 설정으로 표현합니다.",
"concept":"회의록을 다음 회의용 한 장 요약으로 바꾸는 상황을 생각해 봅니다. trigger는 언제 요약을 시작할지, keep은 최근 기록을 얼마나 원문으로 남길지 정합니다. SummarizationMiddleware는 before_model 훅에서 메시지 수나 토큰 수를 검사합니다. 요약 모델은 압축문을 만들고 주 모델은 압축된 문맥으로 답합니다. 압축은 원문을 완전히 보존하지 않으므로 결정, 예외, 날짜, 출처처럼 반드시 남겨야 할 필드를 프롬프트와 검증에 넣어야 합니다.",
"observe":"Before에서는 여섯 메시지가 그대로 주 모델에 전달됩니다. After에서는 trigger=(messages,4), keep=(messages,2)를 적용해 오래된 대화를 요약 메시지로 바꾸고 최근 두 메시지를 유지합니다. 학습용 요약 모델이 만든 문자열에서 14일, 예약 없음, E01 p.3을 검사합니다. 이 검사는 설정이 실행됐음을 보여 주지만 실제 생성 모델의 모든 요약이 정확하다는 뜻은 아닙니다.",
"notes":["메시지 개수 임계값은 문자 수나 실제 토큰 수와 다릅니다. 운영에서는 모델 프로필이 확인되면 토큰 또는 fraction 조건을 검토합니다.","요약 호출도 비용과 지연을 추가합니다. 너무 낮은 임계값은 매번 요약을 실행할 수 있습니다.","압축본에는 원문 식별자를 남겨 중요한 판단 전에 원문을 다시 확인할 수 있게 합니다."],
"next":"다음 절에서는 모델 호출 횟수 제한과 재시도·폴백을 내장 미들웨어로 조합합니다.",
"quiz":[("trigger와 keep의 역할은 각각 무엇인가요?","trigger는 압축 시작 조건, keep은 압축하지 않고 남길 최근 범위를 정합니다."),("메시지 수 임계값의 한계는 무엇인가요?","메시지마다 길이가 달라 실제 토큰 사용량을 정확히 나타내지 못합니다."),("압축 결과에서 출처 식별자를 보존하는 이유는 무엇인가요?","중요한 판단 때 압축 주장과 원문을 다시 대조하기 위해서입니다."),("요약 미들웨어가 비용을 항상 줄인다고 단정할 수 없는 이유는 무엇인가요?","별도 요약 모델 호출 비용이 들고 임계값과 대화 길이에 따라 절감량이 달라집니다.")],
"cells":[("패키지 버전 확인",INSTALL),("결정적 모델 준비",FAKE),("긴 대화 준비",'''from langchain_core.messages import HumanMessage, AIMessage
history = [
 HumanMessage("대출은 몇 권인가요?"), AIMessage("5권입니다 [E01 p.3]"),
 HumanMessage("기간은요?"), AIMessage("14일이며 예약이 없으면 7일 연장됩니다 [E01 p.3]"),
 HumanMessage("출처를 기억해 주세요."), HumanMessage("지금까지 조건을 정리해 주세요."),
]
print("원본 메시지 수:", len(history))'''),("Before: 원문 전체 전달",'''seen_before=[]
class CaptureAll(AgentMiddleware):
    def wrap_model_call(self, request: Any, handler: Any) -> Any:
        seen_before.extend(message.text for message in request.messages)
        return handler(request)
before_agent=create_agent(ScriptedModel(replies=[AIMessage("답")]),tools=[],middleware=[CaptureAll()])
before_agent.invoke({"messages":history})
print("모델 입력 메시지 수:",len(seen_before))
assert len(seen_before)==6''',"before"),("After: 자동 요약 적용",'''from langchain.agents.middleware import SummarizationMiddleware
summary_model=ScriptedModel(replies=[AIMessage("대출은 5권·14일, 예약이 없으면 7일 연장 [E01 p.3]")])
seen_after=[]
class CaptureCompressed(AgentMiddleware):
    def wrap_model_call(self, request: Any, handler: Any) -> Any:
        seen_after.extend(message.text for message in request.messages)
        return handler(request)
after_agent=create_agent(
 ScriptedModel(replies=[AIMessage("압축된 조건을 확인했습니다.")]), tools=[],
 middleware=[SummarizationMiddleware(model=summary_model,trigger=("messages",4),keep=("messages",2)),CaptureCompressed()])
after_agent.invoke({"messages":history})
print("모델 입력:",seen_after)
joined=" ".join(seen_after)
assert "14일" in joined and "E01 p.3" in joined''',"after"),("실제 모델로 압축문 생성",'''import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / ".env").is_file(): load_dotenv(folder / ".env"); break
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY가 필요합니다."
live = init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none")
prompt = "다음 기록을 한 문장으로 요약하되 권수, 기간, 연장 조건, 출처를 모두 보존하세요: " + " ".join(m.text for m in history[:4])
live_summary = live.invoke(prompt)
usage = live_summary.usage_metadata or {}
cost = usage.get("input_tokens",0)/1_000_000*0.75 + usage.get("output_tokens",0)/1_000_000*4.50
print("summary:", live_summary.text)
print("usage:", usage); print("estimated_cost_usd:", round(cost,6))
assert cost < 1.0 and live_summary.text.strip()''',"after"),("압축 전후 비교",'''print("before_count:",len(seen_before))
print("after_count:",len(seen_after))
print("estimated_cost_usd: 0.0 (결정적 로컬 모델)")''',"after")]
},
"04-호출-한도와-재시도-폴백": {
"title":"호출 한도와 재시도·폴백","format":"experiment","hours":"강의 1h · 실습 2h","terms":"7",
"question":"호출 한도, 재시도, 폴백은 서로 다른 실패 조건을 어떻게 나누어 처리할까요?",
"goals":["run_limit와 thread_limit을 구분할 수 있습니다.","재시도 대상 예외와 지수 백오프를 설정할 수 있습니다.","폴백 모델이 실행되는 조건과 비용 경계를 설명할 수 있습니다."],
"why":"Ch16의 CallBudget과 retry_with_fallback은 호출자가 매번 reserve와 재시도 함수를 직접 사용했습니다. create_agent 반복에서는 모델이 도구를 여러 번 요청할 수 있으므로 실행 전체에서 호출 수를 세어야 합니다. 일시적 오류에는 재시도가 도움이 되지만 잘못된 입력이나 권한 오류를 반복하면 비용만 늘어납니다. 한도·재시도·폴백을 서로 다른 정책으로 분리해야 합니다.",
"prior":"Ch16 CallBudget.reserve는 호출 직전에 예상 비용과 호출 수를 검사했습니다. retry_with_fallback은 TimeoutError만 정해진 횟수만 재시도하고 마지막에 폴백 함수를 호출했습니다. 이 절에서는 같은 역할을 ModelCallLimitMiddleware, ModelRetryMiddleware, ModelFallbackMiddleware의 설정과 실행 trace로 확인합니다.",
"concept":"고객센터 전화를 생각해 봅니다. 한도는 한 통화에서 상담원 연결을 몇 번까지 시도할지 막습니다. 재시도는 연결이 일시적으로 끊겼을 때 같은 상담원에게 다시 거는 규칙입니다. 폴백은 주 상담망이 계속 실패할 때 보조 상담망으로 바꾸는 규칙입니다. ModelCallLimitMiddleware의 run_limit는 현재 invoke, thread_limit는 같은 스레드에 누적된 호출을 제한합니다. ModelRetryMiddleware는 retry_on, 지연, 최대 횟수를 정합니다. ModelFallbackMiddleware는 첫 모델과 후속 모델 순서를 정합니다.",
"observe":"결정적 오류 모델로 세 정책을 따로 실행합니다. 재시도 실험에서는 첫 TimeoutError 뒤 두 번째 호출이 성공해 호출 수 2가 됩니다. 폴백 실험에서는 주 모델이 실패하고 보조 모델의 답을 받습니다. 호출 한도 실험에서는 도구를 요청한 뒤 두 번째 모델 호출 전에 제한이 적용됩니다. 이 결과는 정책 경로를 확인하며 실제 공급자 장애율이나 지연 분포를 측정한 값은 아닙니다.",
"notes":["retry_on에는 일시적 오류만 포함합니다. 인증 실패, 잘못된 스키마, 정책 차단은 반복해도 해결되지 않습니다.","재시도는 모델 호출 횟수와 비용을 늘립니다. 호출 한도는 재시도 횟수까지 포함해 설계합니다.","폴백 모델은 기능, 도구 호출 형식, 개인정보 처리 지역, 가격을 따로 검토해야 합니다."],
"next":"다음 절에서는 내장 호출 수 제한이 다루지 않는 예상비용 상한을 커스텀 미들웨어로 작성합니다.",
"quiz":[("run_limit와 thread_limit의 차이는 무엇인가요?","run_limit는 한 invoke 안의 호출 수, thread_limit는 같은 스레드에 누적된 호출 수를 제한합니다."),("모든 예외를 재시도하면 안 되는 이유는 무엇인가요?","영구 오류는 반복해도 해결되지 않고 비용과 지연만 늘어납니다."),("폴백 전에 확인할 호환성은 무엇인가요?","도구 호출·구조화 출력 지원, 정책, 데이터 처리, 가격을 확인합니다."),("재시도와 호출 한도를 함께 설계해야 하는 이유는 무엇인가요?","재시도도 모델 호출 수와 비용에 포함되기 때문입니다.")],
"cells":[("패키지 버전 확인",INSTALL),("결정적 모델 준비",FAKE),("재시도 모델 준비",'''from langchain.agents.middleware import ModelRetryMiddleware, ModelFallbackMiddleware, ModelCallLimitMiddleware
class FlakyModel(ScriptedModel):
    failures: int = 1
    calls: int = 0
    def _generate(self, messages: Any, stop: Any = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
        self.calls += 1
        if self.calls <= self.failures: raise TimeoutError("temporary")
        return super()._generate(messages,stop,run_manager,**kwargs)
flaky=FlakyModel(replies=[AIMessage("재시도 성공")],failures=1)'''),("재시도 실험",'''retry_agent=create_agent(flaky,tools=[],middleware=[ModelRetryMiddleware(max_retries=2,retry_on=(TimeoutError,),initial_delay=0,jitter=False)])
retry_result=retry_agent.invoke({"messages":[{"role":"user","content":"상태 확인"}]})
print("calls:",flaky.calls,"answer:",retry_result["messages"][-1].text)
assert flaky.calls==2'''),("폴백 실험",'''primary=FlakyModel(replies=[AIMessage("주 모델")],failures=5)
backup=ScriptedModel(replies=[AIMessage("보조 모델 응답")])
fallback_agent=create_agent(primary,tools=[],middleware=[ModelFallbackMiddleware(backup)])
fallback_result=fallback_agent.invoke({"messages":[{"role":"user","content":"상태 확인"}]})
print("answer:",fallback_result["messages"][-1].text)
print("primary_calls:",primary.calls,"backup_calls:",backup.index)
assert fallback_result["messages"][-1].text=="보조 모델 응답"
assert primary.calls==1 and backup.index==1'''),("호출 한도 실제 차단",'''limit=ModelCallLimitMiddleware(run_limit=1,exit_behavior="end")
limited_model=ScriptedModel(replies=[
 AIMessage("",tool_calls=[{"name":"lookup_hours","args":{"day":"평일"},"id":"limit_1","type":"tool_call"}]),
 AIMessage("두 번째 모델 응답")])
limit_agent=create_agent(limited_model,tools=[lookup_hours],middleware=[limit])
limit_result=limit_agent.invoke({"messages":[{"role":"user","content":"평일 운영 시간은?"}]})
print("model_calls:",limited_model.index)
print("last_message:",limit_result["messages"][-1].text)
assert limited_model.index==1 and "limit" in limit_result["messages"][-1].text.lower()'''),("정책별 결과 표",'''rows={"retry_calls":flaky.calls,"fallback_primary_calls":primary.calls,"limit":limit.run_limit,"limited_model_calls":limited_model.index,"estimated_cost_usd":0.0}
print(rows)
assert rows["estimated_cost_usd"] < 1.0''')]
},
"05-커스텀-예산-미들웨어": {
"title":"커스텀 예산 미들웨어","format":"paired","hours":"강의 1h · 실습 2h","terms":"6",
"question":"모델 호출 수뿐 아니라 예상비용 상한을 호출 직전에 어떻게 검사할까요?",
"goals":["커스텀 AgentMiddleware 클래스를 작성할 수 있습니다.","wrap_model_call에서 handler 호출 전 예산을 예약할 수 있습니다.","Ch16 CallBudget과 미들웨어 구현의 코드 위치 차이를 비교할 수 있습니다."],
"why":"내장 ModelCallLimitMiddleware는 호출 횟수를 제한하지만 프로젝트가 사용하는 가격표와 예상 토큰으로 비용 상한을 계산하지는 않습니다. Ch16의 CallBudget은 이 정책을 직접 구현했습니다. 에이전트마다 같은 reserve 호출을 넣는 대신 커스텀 미들웨어 하나로 모델 호출 경계를 감싸면 정책 코드를 재사용하고 독립적으로 검사할 수 있습니다.",
"prior":"Ch16 CallBudget은 max_calls, max_cost_usd, calls, cost_usd를 보관하고 reserve에서 다음 호출이 한도를 넘는지 검사했습니다. 이번 구현은 그 계산을 wrap_model_call 앞에 옮깁니다. 가격과 토큰 예상치는 수업용 고정값이며 실제 청구액과 구분합니다.",
"concept":"교통카드 선불 한도를 생각해 봅니다. 버스를 탄 뒤 잔액을 검사하면 이미 비용이 발생했습니다. 호출 전 예약은 다음 호출의 예상비용을 먼저 더해 상한을 넘으면 handler를 호출하지 않습니다. BudgetMiddleware는 estimated_cost_per_call과 max_cost_usd를 받아 같은 미들웨어 인스턴스가 처리한 요청의 예약 비용을 누적합니다. 이 예제는 한 인스턴스에 두 번의 invoke를 순차적으로 전달하며, 운영에서는 예산 범위에 맞게 상태나 외부 저장소의 키를 분리해야 합니다.",
"observe":"Before에서는 두 번의 모델 호출이 모두 실행됩니다. After에서는 첫 호출이 0.004달러를 예약하고 성공하지만 두 번째 호출은 0.008달러가 0.006달러 상한을 넘으므로 handler 실행 전에 BudgetExceeded가 발생합니다. 모델의 calls 값이 1인 것으로 차단 시점이 호출 전임을 확인합니다.",
"notes":["예상비용은 실제 토큰 사용량과 다를 수 있습니다. 응답 후 usage_metadata를 기록해 예상값과 차이를 측정합니다.","미들웨어 인스턴스 필드에 사용자별 값을 두면 동시 요청이 섞일 수 있습니다. 실제 서비스에서는 state, runtime context 또는 원자적 저장소를 사용합니다.","비용 상한 오류 메시지에 계정 잔액이나 내부 가격표 전체를 노출하지 않습니다."],
"next":"다음 절에서는 입력과 도구 호출을 비밀값 없이 추적하는 두 번째 커스텀 미들웨어를 만듭니다.",
"quiz":[("비용을 handler 호출 전에 예약하는 이유는 무엇인가요?","상한을 넘는 호출 자체를 실행하지 않기 위해서입니다."),("호출당 예상비용의 한계는 무엇인가요?","실제 입력·출력 토큰과 캐시 조건에 따라 청구액이 달라질 수 있습니다."),("공유 인스턴스 필드가 운영에서 위험한 이유는 무엇인가요?","여러 요청의 카운터가 섞여 사용자별 한도가 잘못 적용될 수 있습니다."),("내장 호출 한도와 커스텀 예산 미들웨어를 함께 쓸 수 있나요?","가능하며 호출 수와 프로젝트별 비용 정책을 각각 검사할 수 있습니다.")],
"cells":[("패키지 버전 확인",INSTALL),("결정적 모델 준비",FAKE),("Before: 비용 검사 없는 두 호출",'''plain=ScriptedModel(replies=[AIMessage("첫 응답"),AIMessage("둘째 응답")])
plain.invoke("첫 호출"); plain.invoke("둘째 호출")
print("calls:",plain.index)
assert plain.index==2''',"before"),("After: 예산 미들웨어 작성",'''class BudgetExceeded(RuntimeError): pass
class BudgetMiddleware(AgentMiddleware):
    def __init__(self, max_cost_usd: float, estimated_cost_per_call: float) -> None:
        self.max_cost_usd=max_cost_usd; self.estimated=estimated_cost_per_call; self.reserved=0.0
    def wrap_model_call(self, request: Any, handler: Any) -> Any:
        next_cost=self.reserved+self.estimated
        if next_cost > self.max_cost_usd: raise BudgetExceeded("이 미들웨어 인스턴스의 누적 예상비용 상한을 초과합니다.")
        self.reserved=next_cost
        return handler(request)''',"after"),("첫 호출 허용과 두 번째 차단",'''budget=BudgetMiddleware(max_cost_usd=0.006,estimated_cost_per_call=0.004)
guarded=ScriptedModel(replies=[AIMessage("첫 응답"),AIMessage("둘째 응답")])
agent=create_agent(guarded,tools=[],middleware=[budget])
first=agent.invoke({"messages":[{"role":"user","content":"첫 호출"}]})
try:
    agent.invoke({"messages":[{"role":"user","content":"둘째 호출"}]})
except BudgetExceeded as error:
    print(type(error).__name__,str(error))
print("model_calls:",guarded.index,"reserved:",budget.reserved)
assert guarded.index==1 and budget.reserved==0.004''',"after"),("비용 기록",'''print({"max_cost_usd":budget.max_cost_usd,"reserved_cost_usd":budget.reserved,"actual_api_cost_usd":0.0})
assert budget.reserved < 1.0''',"after")]
},
"06-커스텀-감사-미들웨어": {
"title":"커스텀 감사 미들웨어","format":"experiment","hours":"강의 1h · 실습 2h","terms":"6",
"question":"에이전트 전체와 도구 호출을 개인정보 없이 어떤 이벤트로 기록할까요?",
"goals":["감사 로그와 디버그 로그의 목적을 구분할 수 있습니다.","에이전트 시작·도구 감싸기·종료 훅으로 이벤트를 기록할 수 있습니다.","원문 대신 해시와 유형만 남기는 최소 기록 원칙을 적용할 수 있습니다."],
"why":"Ch16의 AuditLogger는 질문을 마스킹하고 소금값을 더한 해시, 이벤트 이름, 안전한 상세 정보만 JSONL에 기록했습니다. 에이전트에서는 한 요청 안에 여러 모델·도구 호출이 있으므로 시작, 도구, 종료를 같은 실행 식별자로 연결해야 합니다. 감사 미들웨어는 업무 함수에서 기록 코드를 분리합니다.",
"prior":"Ch16 AuditLogger.record는 query_masked와 query_hash를 만들고 중첩된 문자열에도 mask_pii를 적용했습니다. 이번 절에서는 원문 질문 자체를 저장하지 않고 메시지 유형과 길이, 도구 이름, 성공 여부만 메모리 이벤트로 남깁니다. 실제 파일 저장은 운영 저장 정책과 접근 권한이 필요하므로 실습 범위에서 제외합니다.",
"concept":"건물 출입 기록은 사람이 들고 있던 문서 내용을 복사하지 않고 출입 시각, 출입구, 승인 여부를 남깁니다. 감사 로그도 목적에 필요한 최소 정보만 기록해야 합니다. AuditMiddleware의 before_agent는 실행 시작, wrap_tool_call은 도구 이름과 성공·오류, after_agent는 종료를 기록합니다. 입력 지문은 고정 소금값과 실제 메시지 텍스트를 함께 해시한 학습용 예시이며 실제 운영에서는 키 관리와 보존 기간 정책이 필요합니다.",
"observe":"운영 시간 질문 한 건을 실행하면 agent_start, tool_start, tool_success, agent_end 순서의 네 이벤트가 남습니다. 이벤트에는 learner@example.com 원문이 없고 입력 길이와 짧은 지문만 있습니다. 도구 결과 본문도 기록하지 않습니다. 이 실험은 누락 없는 전체 감사 체계를 증명하지 않으며 선택한 훅에서 정한 네 이벤트만 확인합니다.",
"notes":["감사 로그에 전체 프롬프트와 도구 결과를 기본 저장하면 개인정보와 영업 정보가 복제될 수 있습니다.","해시는 익명화와 같지 않습니다. 입력 후보가 좁으면 대입 공격으로 원문을 추정할 수 있으므로 접근 통제와 소금 관리가 필요합니다.","after_agent는 정상 종료 경로입니다. 처리되지 않은 예외를 별도로 기록하려면 wrap 훅에서 오류 이벤트를 남기고 다시 raise합니다."],
"next":"다음 절에서는 여러 미들웨어를 한 목록에 넣었을 때 before, after, wrap의 순서를 실제 trace로 확인합니다.",
"quiz":[("감사 로그에 전체 질문을 기본 저장하지 않는 이유는 무엇인가요?","개인정보와 민감한 업무 내용이 로그 저장소에 복제될 수 있기 때문입니다."),("after_agent만으로 모든 오류 종료를 기록할 수 있나요?","아닙니다. 처리되지 않은 예외는 wrap 훅에서 기록하고 다시 전파하는 경로가 필요합니다."),("도구 감사 이벤트에 최소로 필요한 항목 예시는 무엇인가요?","실행 식별자, 도구 이름, 시작·성공·오류 유형, 시각 등입니다."),("해시가 곧 익명화가 아닌 이유는 무엇인가요?","후보가 좁거나 소금이 노출되면 원문을 추정할 수 있기 때문입니다.")],
"cells":[("패키지 버전 확인",INSTALL),("결정적 모델 준비",FAKE),("감사 미들웨어 작성",'''import hashlib
import json
EVENTS=[]
def fingerprint(text: str) -> str:
    return hashlib.sha256(b"lesson-salt:"+text.encode("utf-8")).hexdigest()[:10]
class AuditMiddleware(AgentMiddleware):
    def before_agent(self, state: Any, runtime: Any) -> None:
        text=state["messages"][0].text
        digest=fingerprint(text)
        EVENTS.append({"event":"agent_start","input_chars":len(text),
                       "fingerprint":digest})
    def wrap_tool_call(self, request: Any, handler: Any) -> Any:
        EVENTS.append({"event":"tool_start","tool":request.tool.name})
        try:
            result=handler(request)
        except Exception as error:
            EVENTS.append({"event":"tool_error","tool":request.tool.name,
                           "type":type(error).__name__}); raise
        EVENTS.append({"event":"tool_success","tool":request.tool.name})
        return result
    def after_agent(self, state: Any, runtime: Any) -> None:
        EVENTS.append({"event":"agent_end","messages":len(state["messages"])})'''),("도구를 사용하는 실행",'''scripted=ScriptedModel(replies=[
 AIMessage("",tool_calls=[{"name":"lookup_hours",
  "args":{"day":"평일"},"id":"audit_1","type":"tool_call"}]),
 AIMessage("09:00~20:00")])
audit_agent=create_agent(scripted,tools=[lookup_hours],middleware=[AuditMiddleware()])
audit_agent.invoke({"messages":[{"role":"user","content":"learner@example.com 운영 시간 문의"}]})
for event in EVENTS: print(event)'''),("비밀값 부재 검사",'''serialized=json.dumps(
 EVENTS,ensure_ascii=False)
print("event_order:",[e["event"] for e in EVENTS])
print("same_length_fingerprints:",fingerprint("AA"),fingerprint("BB"))
assert "learner@example.com" not in serialized
assert len("AA") == len("BB") and fingerprint("AA") != fingerprint("BB")
assert [e["event"] for e in EVENTS]==[
 "agent_start","tool_start","tool_success","agent_end"]'''),("기록 범위 해석",'''print({"events":len(EVENTS),"raw_input_saved":False,
       "tool_result_saved":False,"estimated_cost_usd":0.0})''')]
},
"07-순서와-합성": {
"title":"순서와 합성","format":"experiment","hours":"강의 1h · 실습 2h","terms":"5",
"question":"여러 미들웨어의 before·after·wrap 훅은 어떤 순서로 합성될까요?",
"goals":["before 훅의 순방향 실행을 확인할 수 있습니다.","after 훅의 역방향 실행을 확인할 수 있습니다.","wrap 훅의 중첩 순서를 함수 호출 구조로 설명할 수 있습니다."],
"why":"PII 처리, 예산, 재시도, 감사를 한 에이전트에 함께 넣으면 목록 순서가 실제 동작을 바꿉니다. 예산을 예약한 뒤 재시도하면 각 시도를 비용으로 셀지, 재시도 전체를 한 호출로 셀지에 따라 결과가 다릅니다. 출력 감사가 마스킹보다 바깥에 있으면 마스킹 전 값을 기록할 수도 있습니다. 따라서 합성 순서를 trace로 확인해야 합니다.",
"prior":"앞 절까지 PIIMiddleware, 내장 안정화 미들웨어, 두 커스텀 미들웨어를 각각 실행했습니다. 이번에는 기능을 추가하지 않고 A, B, C 세 미들웨어가 같은 훅에서 남기는 문자열만 관찰합니다. 모델은 한 번만 답하는 결정적 모델로 고정합니다.",
"concept":"겹쳐 입은 옷을 생각해 봅니다. 안으로 들어갈 때는 겉옷 A, 중간 옷 B, 안쪽 옷 C 순서로 통과합니다. 밖으로 나올 때는 C, B, A 순서입니다. LangChain의 before 훅은 목록의 앞에서 뒤로 실행됩니다. after 훅은 뒤에서 앞으로 실행됩니다. wrap 훅은 첫 항목이 가장 바깥쪽이 되어 A before, B before, C before, 모델, C after, B after, A after 순서가 됩니다.",
"observe":"middleware=[A,B,C]로 한 번 실행한 trace를 세 구간으로 나눕니다. before_agent와 before_model은 A·B·C, wrap_model_call 진입은 A·B·C이고 반환은 C·B·A, after_model과 after_agent는 C·B·A입니다. 이 순서는 공식 문서의 실행 순서와 일치합니다. 도구 훅도 같은 중첩 원칙을 따르지만 이 셀은 모델 한 번의 최소 예제로 제한합니다.",
"notes":["목록 순서를 문서화하고 trace 회귀 테스트로 고정합니다. 라이브러리 업그레이드 뒤에도 다시 실행합니다.","마스킹 전후의 어느 값이 감사 로그에 들어가는지 실제 요청과 반환 위치로 확인합니다.","재시도 미들웨어의 안쪽과 바깥쪽에 예산 미들웨어를 둘 때 시도 횟수 계산이 달라질 수 있습니다."],
"next":"마지막 절에서는 wrap_model_call로 업무별 메시지만 선택해 Ch8의 Isolate를 에이전트 구현으로 연결합니다.",
"quiz":[("before 훅의 실행 순서는 무엇인가요?","middleware 목록의 첫 항목에서 마지막 항목 순서입니다."),("after 훅이 역순인 이유를 함수 중첩으로 설명해 보세요.","안쪽 처리가 먼저 반환되고 바깥쪽 처리가 나중에 반환되기 때문입니다."),("첫 미들웨어의 wrap 훅은 어느 위치인가요?","다른 wrap 훅과 실제 호출을 감싸는 가장 바깥쪽입니다."),("순서 테스트가 필요한 실무 사례는 무엇인가요?","PII 마스킹 전 원문이 감사 로그에 남지 않는지 확인하는 사례입니다.")],
"cells":[("패키지 버전 확인",INSTALL),("결정적 모델 준비",FAKE),("태그 미들웨어 정의",'''ORDER=[]
class Tagged(AgentMiddleware):
    def __init__(self, tag: str) -> None: self.tag=tag
    @property
    def name(self) -> str: return f"Tagged-{self.tag}"
    def before_agent(self, state: Any, runtime: Any) -> None: ORDER.append(f"before_agent:{self.tag}")
    def before_model(self, state: Any, runtime: Any) -> None: ORDER.append(f"before_model:{self.tag}")
    def wrap_model_call(self, request: Any, handler: Any) -> Any:
        ORDER.append(f"wrap_in:{self.tag}"); result=handler(request); ORDER.append(f"wrap_out:{self.tag}"); return result
    def after_model(self, state: Any, runtime: Any) -> None: ORDER.append(f"after_model:{self.tag}")
    def after_agent(self, state: Any, runtime: Any) -> None: ORDER.append(f"after_agent:{self.tag}")'''),("A B C 순서로 실행",'''ordered=create_agent(ScriptedModel(replies=[AIMessage("완료")]),tools=[],middleware=[Tagged("A"),Tagged("B"),Tagged("C")])
ordered.invoke({"messages":[{"role":"user","content":"순서 확인"}]})
for item in ORDER: print(item)'''),("구간별 순서 검사",'''expected=[
"before_agent:A","before_agent:B","before_agent:C","before_model:A","before_model:B","before_model:C",
"wrap_in:A","wrap_in:B","wrap_in:C","wrap_out:C","wrap_out:B","wrap_out:A",
"after_model:C","after_model:B","after_model:A","after_agent:C","after_agent:B","after_agent:A"]
assert ORDER==expected
print("order_match:",ORDER==expected)'''),("합성 표 출력",'''print({"before":"A→B→C","wrap":"A(B(C(model)))","after":"C→B→A","estimated_cost_usd":0.0})''')]
},
"08-컨텍스트-분리와-Isolate": {
"title":"컨텍스트 분리와 Isolate","format":"paired","hours":"강의 1h · 실습 2h","terms":"6",
"question":"같은 상태에 섞인 여러 업무 메시지에서 현재 업무에 필요한 내용만 모델 요청으로 분리하려면 어떻게 할까요?",
"goals":["Ch8의 Isolate를 업무별 모델 입력 분리로 설명할 수 있습니다.","wrap_model_call에서 request.override(messages=...)를 사용할 수 있습니다.","텍스트 태그와 실제 별도 모델 요청의 차이를 검증할 수 있습니다."],
"why":"Ch8에서는 대출 문의와 휴관 문의의 자료를 별도 메시지 목록으로 구성했습니다. create_agent 상태에는 여러 업무의 대화가 누적될 수 있고, 전체 상태를 그대로 모델에 전달하면 관련 없는 자료가 입력을 차지합니다. 미들웨어는 영구 상태를 삭제하지 않고 이번 모델 호출에 보낼 메시지만 선택할 수 있습니다. 이것이 Ch8의 Isolate를 실행 구조로 연결하는 방법입니다.",
"prior":"Ch8 context_lab.py의 assemble_isolated_messages는 업무별 자료를 별도 필드로 조립했고 텍스트 태그는 보안 격리가 아니라고 설명했습니다. 이번 절도 같은 경계를 지킵니다. request.override로 메시지를 줄이는 것은 모델 입력 분리이며 저장소 권한이나 프로세스 격리를 제공하지 않습니다.",
"concept":"두 사건의 서류를 한 책상에 올려놓되 담당자에게는 현재 사건 서류철만 건네는 상황을 생각해 봅니다. 상태에는 감사와 추적을 위해 전체 메시지가 남아 있을 수 있습니다. IsolateMiddleware는 각 메시지의 additional_kwargs에 있는 topic을 읽어 현재 topic과 같은 메시지만 새 요청에 넣습니다. request.override는 원래 요청 객체를 바꾸지 않고 선택된 messages를 가진 새 요청을 만듭니다. handler는 그 새 요청만 모델에 전달합니다.",
"observe":"Before에서는 대출 세 메시지와 인사 두 메시지가 모두 모델에 전달되어 입력 수가 5입니다. After에서는 topic=loan 미들웨어가 대출 메시지 세 개만 선택합니다. capture 모델이 실제로 받은 메시지 수와 내용에서 HR 급여 문자열이 없음을 검사합니다. 상태에서 원문이 삭제된 것이 아니므로 보안 권한 분리라고 표현하지 않습니다.",
"notes":["메시지 메타데이터는 신뢰할 수 있는 애플리케이션 코드가 붙여야 합니다. 사용자가 topic 값을 임의로 바꿀 수 있으면 접근 통제가 되지 않습니다.","민감한 자료는 선택 전에도 권한이 없는 프로세스나 상태에 넣지 않습니다. 저장소·도구·런타임 권한을 별도로 검사합니다.","Isolate와 Compress를 함께 쓰면 먼저 업무 범위를 선택한 뒤 그 범위 안에서 압축하는 순서를 검토합니다."],
"next":"Ch23에서는 체크포인터와 스레드에 상태를 저장하고 프로세스 중단 뒤 이어서 실행합니다. 이 절의 업무별 상태 범위가 지속성 설계의 입력이 됩니다.",
"quiz":[("request.override의 역할은 무엇인가요?","원본 요청을 직접 바꾸지 않고 일부 필드를 바꾼 새 요청을 만듭니다."),("메시지 태그만으로 보안 격리가 되지 않는 이유는 무엇인가요?","같은 호출이나 상태에 들어간 자료는 모델이나 프로세스가 접근할 수 있기 때문입니다."),("Compress와 Isolate를 함께 적용할 때 한 가지 합리적인 순서는 무엇인가요?","현재 업무의 자료를 먼저 선택하고 그 범위 안에서 오래된 내용을 압축합니다."),("topic 메타데이터를 누가 붙여야 하나요?","권한과 업무 범위를 확인한 애플리케이션 코드가 붙여야 합니다.")],
"cells":[("패키지 버전 확인",INSTALL),("메시지 수집 모델 준비",'''from typing import Any
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration,ChatResult
class CapturingModel(BaseChatModel):
    seen:list[str]=[]
    @property
    def _llm_type(self) -> str: return "capture"
    def _generate(self, messages: Any, stop: Any = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
        self.seen=[m.text for m in messages]
        return ChatResult(generations=[ChatGeneration(message=AIMessage("확인 완료"))])
    def bind_tools(self, tools: Any, *, tool_choice: Any = None, **kwargs: Any) -> "CapturingModel": return self'''),("업무가 섞인 메시지 준비",'''from langchain_core.messages import HumanMessage,AIMessage
mixed=[
 HumanMessage("대출은 5권",additional_kwargs={"topic":"loan"}),AIMessage("기간은 14일",additional_kwargs={"topic":"loan"}),
 HumanMessage("급여 자료는 내부 문서",additional_kwargs={"topic":"hr"}),AIMessage("인사팀 확인",additional_kwargs={"topic":"hr"}),
 HumanMessage("대출 연장은?",additional_kwargs={"topic":"loan"})]
print("state_messages:",len(mixed))'''),("Before: 전체 메시지 전달",'''before_model=CapturingModel()
create_agent(before_model,tools=[]).invoke({"messages":mixed})
print("model_messages:",before_model.seen)
assert len(before_model.seen)==5 and any("급여" in text for text in before_model.seen)''',"before"),("After: 업무별 요청 분리",'''class IsolateMiddleware(AgentMiddleware):
    def __init__(self, topic: str) -> None: self.topic=topic
    def wrap_model_call(self, request: Any, handler: Any) -> Any:
        selected=[m for m in request.messages if m.additional_kwargs.get("topic")==self.topic]
        return handler(request.override(messages=selected))
after_model=CapturingModel()
create_agent(after_model,tools=[],middleware=[IsolateMiddleware("loan")]).invoke({"messages":mixed})
print("model_messages:",after_model.seen)
assert len(after_model.seen)==3 and all("급여" not in text for text in after_model.seen)''',"after"),("상태와 요청 범위 비교",'''print({"stored_messages":len(mixed),"selected_messages":len(after_model.seen),"security_boundary":False,"estimated_cost_usd":0.0})''',"after")]
}}

DIAGRAM_READINGS = {
    "01-미들웨어와-6개-훅": "왼쪽의 파란 입력 상태에서 실행을 시작해 노란 before_agent를 한 번 통과합니다. 보라색 모델 호출 상자의 앞뒤에는 before_model·wrap_model_call·after_model이 놓입니다. 모델이 도구를 요청하면 초록색 lookup_hours 앞뒤를 wrap_tool_call이 감싸고 다시 모델 상자로 돌아갑니다. 마지막 노란 after_agent 뒤에서 실행이 끝납니다.",
    "02-PII-마스킹-이식": "파란 원문 입력에는 네 종류의 가상 PII가 있습니다. 노란 Ch16 mask_pii 상자는 네 유형을 완전 치환하고 개수를 반환합니다. 다른 경로의 노란 PIIMiddleware(email) 상자는 이메일 한 유형만 모델 호출 전후에 부분 마스킹합니다. 두 화살표가 같은 보라색 모델 경계에 닿지만 보존하는 정책은 같지 않습니다.",
    "03-요약-압축과-Compress": "파란 원본 여섯 메시지가 노란 trigger 검사로 들어갑니다. 임계값 미만이면 그대로 보라색 주 모델로 이동합니다. 임계값 이상이면 오래된 메시지가 보라색 요약 모델을 거쳐 파란 요약문과 최근 두 메시지로 바뀐 뒤 주 모델에 전달됩니다. E01 p.3은 압축 뒤에도 확인할 보존 항목입니다.",
    "04-호출-한도와-재시도-폴백": "파란 모델 요청은 먼저 노란 호출 한도를 확인합니다. 일시적 TimeoutError는 빨간 실패 상자에서 재시도 경로로 돌아가고, 정한 횟수 뒤에도 실패하면 보라색 보조 모델로 이동합니다. 성공 화살표와 차단 화살표를 구분하면 한도·재시도·폴백이 서로 다른 조건을 처리한다는 점을 읽을 수 있습니다.",
    "05-커스텀-예산-미들웨어": "파란 요청이 노란 예상비용 예약 상자에 들어갑니다. 예약 합계가 0.006달러 이하이면 보라색 handler와 모델 호출로 이어집니다. 두 번째 요청처럼 0.008달러가 되면 빨간 BudgetExceeded로 이동하고 모델 호출 화살표는 생기지 않습니다. 차단 전후의 guarded.index가 호출 시점을 확인하는 값입니다.",
    "06-커스텀-감사-미들웨어": "파란 사용자 입력에서 노란 agent_start 이벤트를 만들되 원문 대신 길이와 지문만 남깁니다. 초록색 lookup_hours 전후에는 tool_start와 tool_success가 놓이고, 마지막 노란 agent_end는 메시지 수만 기록합니다. 도구 결과 본문과 이메일 원문은 어느 이벤트 상자에도 들어가지 않습니다.",
    "07-순서와-합성": "파란 middleware 목록 A·B·C가 노란 before 구간에서는 왼쪽부터 A→B→C로 실행됩니다. 보라색 모델을 감싸는 wrap 구간은 A(B(C(model))) 형태입니다. 반환과 after 구간은 C→B→A로 반대 방향입니다. 노트북의 ORDER 18개 항목이 각 화살표의 순서를 검증합니다.",
    "08-컨텍스트-분리와-Isolate": "파란 상태에는 loan 세 메시지와 hr 두 메시지가 함께 있습니다. 노란 IsolateMiddleware가 topic=loan인 세 메시지만 선택해 새 파란 요청을 만들고 보라색 모델에 전달합니다. hr 메시지로 향하는 빨간 차단 표시는 모델 입력에서 제외됐다는 뜻이며 원래 상태나 저장소에서 삭제됐다는 뜻은 아닙니다.",
}

SUMMARIES = {
    "01-미들웨어와-6개-훅": ["훅은 에이전트 전체·모델·도구의 실행 경계에 미들웨어 로직을 연결합니다.", "도구를 한 번 쓴 실행에서 모델 훅은 두 번, 도구 훅은 한 번 실행되는 trace를 확인했습니다.", "결정적 검사 모델은 훅 경계를 확인하며 실제 모델 품질을 측정하지 않습니다."],
    "02-PII-마스킹-이식": ["PIIMiddleware는 설정한 메시지 경계에서 정한 개인 식별 정보 유형을 탐지하고 처리합니다.", "입력과 출력에 email 마스킹을 적용해 호출자가 직접 함수를 부르지 않아도 경계가 유지됨을 확인했습니다.", "마스킹은 접근 권한을 대신하지 않으며 한국 고유 식별자에는 별도 탐지기와 테스트가 필요합니다."],
    "03-요약-압축과-Compress": ["SummarizationMiddleware는 trigger에 도달하면 오래된 메시지를 요약하고 keep 범위는 원문으로 남깁니다.", "여섯 메시지가 요약문과 최근 두 메시지로 바뀌며 날짜·예외·출처가 남았는지 확인했습니다.", "결정적 요약문의 검사 통과는 실제 생성 모델의 정확성을 보장하지 않습니다."],
    "04-호출-한도와-재시도-폴백": ["재시도는 같은 모델의 일시 오류를, 폴백은 다른 모델로의 전환을, 호출 한도는 반복 횟수를 다룹니다.", "최초 모델은 한 번 실패하고 보조 모델이 응답하며, 도구 루프는 두 번째 모델 호출 전에 종료됨을 확인했습니다.", "재시도 대상 오류와 미들웨어 순서를 정하지 않으면 영구 오류를 반복하거나 호출 한도를 예상과 다르게 소비할 수 있습니다."],
    "05-커스텀-예산-미들웨어": ["BudgetMiddleware는 handler 호출 전에 예상비용을 예약하고 인스턴스의 누적 상한을 넘는 요청을 차단합니다.", "같은 인스턴스에 두 invoke를 전달해 첫 요청만 모델에 도달하고 두 번째 요청은 호출 전에 차단됨을 확인했습니다.", "운영에서는 예산 범위와 동시성에 맞게 누적값을 state, runtime context 또는 원자적 저장소에 분리합니다."],
    "06-커스텀-감사-미들웨어": ["AuditMiddleware는 에이전트 시작·도구 성공 또는 오류·정상 종료를 선택한 훅에서 사건으로 기록합니다.", "서로 길이가 같은 두 입력도 서로 다른 지문을 만들고, 예제 이벤트에 이메일 원문과 도구 결과가 없음을 확인했습니다.", "짧은 해시와 메모리 목록은 익명화·위변조 방지·영구 보존을 제공하지 않으며 운영에서 키 관리와 접근 통제가 필요합니다."],
    "07-순서와-합성": ["여러 미들웨어의 before 훅은 등록 순서로, after 훅과 wrap 반환 구간은 역순으로 실행됩니다.", "A·B·C의 18개 trace를 예상 목록과 비교해 진입과 반환의 중첩 순서를 확인했습니다.", "요청이나 상태를 바꾸는 미들웨어는 순서가 정책 결과를 바꾸므로 trace 회귀 검사로 고정합니다."],
    "08-컨텍스트-분리와-Isolate": ["IsolateMiddleware는 저장 상태를 지우지 않고 현재 모델 호출에 전달할 메시지만 request.override로 선택합니다.", "loan 메시지 세 개만 모델에 도달하고 hr 급여 문자열은 제외됨을 수집 모델의 입력으로 확인했습니다.", "topic 태그는 모델 입력 범위를 줄이지만 저장소·도구·런타임의 접근 권한을 대신하지 않습니다."],
}


def source_for(item: dict) -> str:
    goals = "".join(f"<li>{goal}</li>" for goal in item["goals"])
    notes = "".join(f"<li>{note}</li>" for note in item["notes"])
    quiz = "".join(f'<p class="quiz-q">{index}. {question}</p><p class="quiz-a"><b>해설</b> — {answer}</p>' for index,(question,answer) in enumerate(item["quiz"],1))
    refs = '''<li><a href="https://docs.langchain.com/oss/python/langchain/middleware/custom">LangChain Custom middleware</a> · 확인 2026-09-11 · LangChain 1.4.0</li><li><a href="https://docs.langchain.com/oss/python/langchain/middleware/built-in">LangChain Prebuilt middleware</a> · 확인 2026-09-11 · LangChain 1.4.0</li><li><a href="https://reference.langchain.com/python/langchain/agents/middleware">LangChain middleware API reference</a> · 확인 2026-09-11 · LangChain 1.4.0</li>'''
    failure_title = "실험 결과 해석" if item["format"] == "experiment" else "일부러 실패해 보기"
    notebook = f'{{{{notebook:{item["slug"]}}}}}' if item["format"] == "experiment" else f'{{{{notebook:{item["slug"]}|example}}}}'
    failure = f'<p>{item["observe"]}</p>' if item["format"] == "experiment" else f'<p>{item["observe"]}</p>{{{{notebook:{item["slug"]}|failure}}}}'
    return f'''<!--meta: {item["hours"]} | 코드 Jupyter Notebook | 새 용어 {item["terms"]}개 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>{goals}</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{item["why"]}</p><p><strong>이 절의 질문</strong> — {item["question"]}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{item["prior"]}</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>{item["concept"]}</p><h3>도식 읽기</h3><p>{DIAGRAM_READINGS[item["slug"]]}</p>{{{{svg:{item["slug"]}-흐름}}}}
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 Python 3.12 새 커널에서 독립 실행합니다. 설치 버전을 먼저 출력한 뒤 한 조건만 바꾸어 실제 객체와 trace를 비교합니다. 결정적 학습용 모델을 사용한 절은 API 비용이 0달러이며, 01절의 실제 API 호출은 usage_metadata로 예상비용 1달러 미만을 검사합니다.</p>{notebook}<p class="look"><b>확인할 점</b> — 출력의 호출 횟수, 메시지 수, 이벤트 순서를 설명과 대조합니다.</p>
<h2 id="b6"><span class="no">6</span>{failure_title}</h2>{failure}
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{notes}</ul><p>실습의 결정적 모델은 미들웨어 실행 경계를 재현하기 위한 검사 도구입니다. 실제 모델 품질, 공급자 장애율, 운영 비용을 대신 측정하지 않습니다. 적용 전에는 사용 중인 모델과 계정의 실제 사용량을 다시 확인합니다.</p>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul>{''.join(f'<li>{line}</li>' for line in SUMMARIES[item["slug"]])}</ul><p><strong>다음 학습과 이어지는 지점</strong> — {item["next"]}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz"><summary>문제와 해설</summary>{quiz}</details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul>{refs}</ul>
'''


def build_notebook(item: dict) -> dict:
    cells = [md(f'# {item["title"]}\n\n{item["question"]}'), md(f'## 실행 환경 준비\n\n실습 파일은 `labs/part6/ch22-middleware/notebooks/{item["slug"]}.ipynb`입니다. Python 3.12 새 커널에서 위에서부터 실행합니다.')]
    for title, source, *part in item["cells"]:
        lesson_part = part[0] if part else None
        purpose = f"# 이 셀은 {title} 작업을 수행하고 확인할 값을 출력합니다.\n"
        helper_note = "\n\n이 모델은 정해 둔 응답으로 훅 경계를 관찰하는 결정적 검사 장치입니다. BaseChatModel 상속 구현 자체는 이 절의 학습 대상이 아닙니다." if source == FAKE else ""
        cells.append(md(f"## {title}{helper_note}", lesson_part)); cells.append(code(purpose + source, lesson_part))
    for index, cell in enumerate(cells, 1): cell["id"] = f"cell-{index:02d}"
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.12"},"lesson_format":item["format"]},"nbformat":4,"nbformat_minor":5}


def main() -> None:
    config = json.loads((CHAPTER / "chapter.json").read_text(encoding="utf-8"))
    config.update({"part_title":"Part 6 · Agent 개발","title":"Middleware","hours":"총 24h · 강의 8h · 실습 16h","objectives":["에이전트 생명주기의 여섯 훅을 설명하고 내장·커스텀 미들웨어를 적용할 수 있습니다.","Ch16의 PII·요약·호출 한도·재시도 가드레일을 미들웨어로 이식하고 코드 위치를 비교할 수 있습니다.","여러 미들웨어의 실행 순서를 검증하고 Compress·Isolate를 모델 요청 경계에 구현할 수 있습니다."]})
    (CHAPTER / "chapter.json").write_text(json.dumps(config,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for section in config["sections"]:
        item = LESSONS[section["slug"]]; item["slug"] = section["slug"]
        if item["slug"] == "01-미들웨어와-6개-훅":
            cells = item["cells"]
            item["cells"] = [cells[0], cells[-1], cells[1], *cells[2:-1]]
        (CHAPTER / "_src" / f'{item["slug"]}.html').write_text(source_for(item),encoding="utf-8")
        (LAB / "notebooks" / f'{item["slug"]}.ipynb').write_text(json.dumps(build_notebook(item),ensure_ascii=False,indent=1)+"\n",encoding="utf-8")


if __name__ == "__main__": main()
