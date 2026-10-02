from __future__ import annotations
# 2026-09-25 Ch 21 품질 개선: 이 파일은 Ch 21과 Ch 29를 함께 쓰는 옛 생성기입니다.
# Ch 21 개선본(chapter.json·노트북·_src)은 textbook/part6/ch21-create-agent/qa/upgrade/author_NN.py가 씁니다.
# 그래서 write_chapter()는 Ch 21 쪽을 건너뛰고, Ch 29 쪽 동작은 그대로 둡니다.

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = "2026-09-11"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "id": "", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": {}, "outputs": [], "source": text.splitlines(keepends=True)}


INSTALL21 = '''%pip install -q langchain==1.4.0 langchain-openai==1.6.0 langgraph==1.2.11 python-dotenv==1.2.3 pillow
import os
from pathlib import Path
from importlib.metadata import version
from dotenv import load_dotenv
for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / ".env").is_file():
        load_dotenv(folder / ".env")
        break
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY가 필요합니다."
print("langchain", version("langchain"))
print("langgraph", version("langgraph"))
print("API 키 존재 여부 확인 완료")'''

INSTALL29 = '''%pip install -q agentevals==0.0.9 langchain==1.4.0 langchain-openai==1.6.0 langgraph==1.2.11 python-dotenv==1.2.3
import os
from pathlib import Path
from importlib.metadata import version
from dotenv import load_dotenv
for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / ".env").is_file():
        load_dotenv(folder / ".env")
        break
print("agentevals", version("agentevals"))
print("langchain", version("langchain"))'''


CELL_COMMENTS = {
    "환경 준비": "공개하지 않은 API 키는 존재 여부만 확인하고 고정한 패키지 버전을 출력합니다.",
    "도구와 에이전트 만들기": "tools 목록은 모델이 선택할 lookup_policy를 제공하고 system_prompt는 근거 사용을 제한합니다.",
    "컴파일 그래프 PNG 확인": "CompiledStateGraph의 Mermaid 구조를 PNG 바이트로 렌더링하고 파일 서명을 검사합니다.",
    "실제 ReAct 실행": "messages를 순서대로 읽어 AIMessage의 호출 id와 뒤따르는 ToolMessage 결과를 연결합니다.",
    "사용량과 비용 상한": "최종 답만 보지 않고 모든 AIMessage의 usage_metadata를 합산해 실행 전체 비용을 추정합니다.",
    "출력 스키마와 두 에이전트": "같은 PolicyAnswer 스키마를 ToolStrategy와 ProviderStrategy에 각각 연결합니다.",
    "두 전략 실제 실행": "같은 입력으로 두 전략을 호출하고 structured_response의 세 필드를 검증합니다.",
    "메인 루프 메시지 확인": "AIMessage 수와 전체 메시지 수를 나란히 출력해 추가 모델 호출과 추가 메시지를 구분합니다.",
    "상태와 실행 컨텍스트 정의": "request_tag는 AgentState에, 사용자 권한은 ToolRuntime이 읽는 context에 둡니다.",
    "컨텍스트를 전달해 실행": "invoke의 상태 입력과 context 인자를 분리해 current_access 도구를 실행합니다.",
    "상태와 컨텍스트 구분": "최종 상태 키를 검사해 context가 AgentState에 자동 저장되지 않음을 확인합니다.",
    "현재 API 서명 확인": "설치된 langchain 1.4.0의 create_agent 서명에서 마이그레이션 대상 인자를 확인합니다.",
    "이전과 현재 호출 대조": "0.x 호출 지점과 v1 대응 지점을 한 행씩 출력해 변경 범위를 분리합니다.",
    "v1 최소 실행": "바꾼 import와 system_prompt를 사용한 최소 에이전트가 실제 응답하는지 검사합니다.",
    "로컬 문서와 검색 도구": "읽기 전용 규정과 검색 로그를 선언해 모델의 검색어와 재검색 횟수를 남깁니다.",
    "Agentic RAG 실행": "예약 질문에서 모델이 search_rules를 선택하고 3일 근거를 답에 사용하는지 확인합니다.",
    "검색 결과가 없는 질문": "주차 규정이 없는 질문으로 검색어 변경과 근거 없음 응답을 관찰합니다.",
    "Ch14 문서와 평가셋 읽기": "Ch14 원본 documents와 queries에서 비교할 C01·C05·C07을 그대로 선택합니다.",
    "공통 임베딩 색인 만들기": "열두 문서의 임베딩을 단위 벡터로 정규화해 두 RAG 경로가 공유할 색인을 만듭니다.",
    "공통 검색 함수 정의": "질문 벡터와 문서 벡터의 코사인 유사도로 상위 두 원문과 점수를 반환합니다.",
    "고정 RAG와 Agentic RAG 준비": "같은 모델과 색인을 쓰되 고정 경로는 직접 검색하고 Agent 경로는 search_documents 도구를 선택합니다.",
    "호출별 사용량 집계 함수": "한 실행에 포함된 모든 AIMessage의 입력·출력 토큰과 모델 호출 수를 합산합니다.",
    "같은 평가셋으로 두 경로 실행": "각 질문의 원문, 모델 답, 검색 trace, 전체 지연을 두 경로에서 빠짐없이 보존합니다.",
    "원문 답변과 실행 지표 출력": "원문 답변과 문서 id, 모델·도구 호출 수, 토큰, 지연을 질문별 한 행으로 출력합니다.",
    "원문 기준 LLM 평가": "gold_doc_id의 원문과 각 답을 구조화 judge가 함께 읽어 사실 지지 여부와 이유를 반환합니다.",
    "정확도·토큰·지연 집계": "세 질문의 supported 비율과 두 경로의 전체 토큰·평균 지연을 집계합니다.",
    "Ch29가 읽을 실제 비교 기록 저장": "Ch29가 같은 실행을 재현할 수 있도록 비밀값 없는 답·trace·사용량을 JSON으로 저장합니다.",
    "세 종류의 평가 입력 만들기": "같은 메시지 궤적에서 최종 답, 첫 도구 선택, 전체 호출 순서를 각각 추출합니다.",
    "최종 답만 맞는 나쁜 경로 비교": "답은 유지하고 검색만 반복해 Final Response 평가가 놓치는 호출 증가를 만듭니다.",
    "기준 궤적 준비": "search_rules 다음 check_source가 이어지는 기준 메시지 궤적을 만듭니다.",
    "strict와 unordered 실행": "두 도구 순서를 뒤집어 strict와 unordered의 순서 처리 차이를 확인합니다.",
    "subset과 superset 실행": "기준보다 짧은 궤적과 추가 호출 궤적으로 포함 관계의 방향을 검증합니다.",
    "평가할 궤적": "judge와 결정적 평가가 같은 실제·기준 메시지를 읽도록 입력을 고정합니다.",
    "실제 LLM judge 실행": "TRAJECTORY_ACCURACY_PROMPT로 전체 단계의 논리와 효율을 실제 모델이 판정합니다.",
    "결정적 검사와 함께 보기": "같은 궤적의 strict 점수와 judge 설명을 나란히 출력해 구조와 의미 평가를 구분합니다.",
    "프로젝트 루트 찾기": "현재 폴더부터 상위로 탐색해 개인 절대 경로 없이 Ch18·Ch21 산출물을 찾습니다.",
    "Ch18 실제 워크플로우 출력 읽기": "실행 완료된 Ch18 비교 노트북에서 다섯 패턴의 저장 출력 행을 읽습니다.",
    "Ch18 출력 공통 필드로 변환": "Ch18의 calls·tokens·latency·quality를 공통 운영 열로 변환합니다.",
    "Ch21 실제 Agentic RAG 기록 읽기": "Ch21이 실제 실행 후 저장한 세 질문의 답·trace·usage JSON을 읽습니다.",
    "Agent 궤적을 공통 필드로 변환": "모든 AIMessage 토큰과 tool_calls를 Ch18과 같은 열 이름으로 변환합니다.",
    "실제 두 기록 비교": "서로 다른 표본임을 유지하면서 각 기록 안의 평균 품질·호출·토큰·지연을 계산합니다.",
    "실제 Agent 기록의 p95 계산": "Ch21 세 실행의 실제 지연과 토큰을 nearest-rank p95로 계산합니다.",
}


def notebook(title: str, cells: list[tuple[str, str]]) -> dict:
    out = [md(f"# {title}\n\n이 노트북은 Python 3.12 새 커널에서 독립 실행합니다.")]
    for heading, source in cells:
        comment = CELL_COMMENTS[heading]
        if source.startswith("%pip install"):
            install, rest = source.split("\n", 1)
            out.extend([md("## 패키지 설치"), code(f"# 노트북이 사용하는 패키지 버전을 새 커널 환경에 설치합니다.\n{install}"), md(f"## {heading}"), code(f"# {comment}\n{rest}")])
        else:
            out.extend([md(f"## {heading}"), code(f"# {comment}\n{source}")])
    for i, cell in enumerate(out, 1):
        cell["id"] = f"cell-{i:02d}"
    return {"cells": out, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}, "lesson_format": "experiment"}, "nbformat": 4, "nbformat_minor": 5}


NB21 = {
"01-create-agent와-ReAct-루프": notebook("create_agent와 ReAct 루프", [
 ("환경 준비", INSTALL21),
 ("도구와 에이전트 만들기", '''from langchain.agents import create_agent
from langchain.tools import tool
@tool
def lookup_policy(topic: str) -> str:
    """자료실 규정을 조회합니다. topic은 대출 또는 운영입니다."""
    return {"대출": "일반 도서는 14일 동안 5권까지 대출할 수 있습니다.", "운영": "평일 09:00~20:00 운영합니다."}[topic]
agent = create_agent("openai:gpt-5.4-mini", [lookup_policy], system_prompt="규정 도구를 사용해 근거가 있는 답만 하세요.")
print(type(agent).__name__)
print(agent.get_graph().draw_mermaid())'''),
 ("컴파일 그래프 PNG 확인", '''from IPython.display import Image, display
png = agent.get_graph().draw_mermaid_png()
print("png_bytes:", len(png), "signature:", png[:8])
display(Image(png))
assert png[:8] == b"\\x89PNG\\r\\n\\x1a\\n"'''),
 ("실제 ReAct 실행", '''result = agent.invoke({"messages": [{"role": "user", "content": "일반 도서를 며칠 빌릴 수 있나요?"}]})
for i, message in enumerate(result["messages"], 1):
    print(i, type(message).__name__, "calls=", getattr(message, "tool_calls", []), "text=", message.text[:100])
assert any(type(m).__name__ == "ToolMessage" for m in result["messages"])
assert "14" in result["messages"][-1].text'''),
 ("사용량과 비용 상한", '''INPUT_USD_PER_MTOK, OUTPUT_USD_PER_MTOK = 0.75, 4.50
usage = [m.usage_metadata for m in result["messages"] if getattr(m, "usage_metadata", None)]
tokens_in = sum(x["input_tokens"] for x in usage)
tokens_out = sum(x["output_tokens"] for x in usage)
cost = tokens_in/1_000_000*INPUT_USD_PER_MTOK + tokens_out/1_000_000*OUTPUT_USD_PER_MTOK
print({"input_tokens": tokens_in, "output_tokens": tokens_out, "estimated_cost_usd": round(cost, 6)})
assert cost < 1''')]),
"02-구조화-출력-두-전략": notebook("ToolStrategy와 ProviderStrategy", [
 ("환경 준비", INSTALL21),
 ("출력 스키마와 두 에이전트", '''from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
class PolicyAnswer(BaseModel):
    topic: str = Field(description="규정 주제")
    answer: str = Field(description="근거에 맞는 답")
    source: str = Field(description="자료 식별자")
tool_agent = create_agent("openai:gpt-5.4-mini", [], response_format=ToolStrategy(PolicyAnswer))
provider_agent = create_agent("openai:gpt-5.4-mini", [], response_format=ProviderStrategy(PolicyAnswer))
prompt = "자료 R-14에 따르면 일반 도서 대출 기간은 14일입니다. 구조화해 주세요."'''),
 ("두 전략 실제 실행", '''rows = {}
for name, current in [("tool", tool_agent), ("provider", provider_agent)]:
    result = current.invoke({"messages": [{"role": "user", "content": prompt}]})
    parsed = result["structured_response"]
    rows[name] = {"parsed": parsed.model_dump(), "messages": len(result["messages"]), "ai_messages": sum(type(m).__name__ == "AIMessage" for m in result["messages"])}
    print(name, rows[name])
    assert "R-14" in parsed.source and "14" in parsed.answer'''),
 ("메인 루프 메시지 확인", '''print(rows)
print("구조화 결과 키:", "structured_response")
assert rows["tool"]["ai_messages"] >= 1 and rows["provider"]["ai_messages"] >= 1''')]),
"03-AgentState와-context-schema": notebook("AgentState와 context_schema", [
 ("환경 준비", INSTALL21),
 ("상태와 실행 컨텍스트 정의", '''from dataclasses import dataclass
from langchain.agents import AgentState, create_agent
from langchain.tools import tool, ToolRuntime
class SupportState(AgentState):
    request_tag: str
@dataclass
class UserContext:
    user_id: str
    access_level: str
@tool
def current_access(runtime: ToolRuntime[UserContext]) -> str:
    """현재 사용자의 접근 수준을 확인합니다."""
    return f"{runtime.context.user_id}:{runtime.context.access_level}"'''),
 ("컨텍스트를 전달해 실행", '''agent = create_agent("openai:gpt-5.4-mini", [current_access], system_prompt="접근 수준 질문에는 도구를 반드시 사용하세요.", state_schema=SupportState, context_schema=UserContext)
result = agent.invoke({"messages": [{"role":"user","content":"제 접근 수준을 확인해 주세요."}], "request_tag":"lesson-03"}, context=UserContext("student-7", "read-only"))
print("state keys:", sorted(result.keys()))
print("request_tag:", result["request_tag"])
print("answer:", result["messages"][-1].text)
assert result["request_tag"] == "lesson-03" and "read-only" in result["messages"][-1].text'''),
 ("상태와 컨텍스트 구분", '''print("AgentState는 그래프 실행 결과에 남음:", result["request_tag"])
print("context는 도구 실행 중 읽고 결과 상태의 키로 자동 저장되지 않음:", "context" in result)
assert "context" not in result''')]),
"04-0x에서-1x로-마이그레이션": notebook("0.x에서 1.x로 마이그레이션", [
 ("환경 준비", INSTALL21),
 ("현재 API 서명 확인", '''import inspect
from langchain.agents import create_agent
signature = str(inspect.signature(create_agent))
print(signature)
for name in ["model", "tools", "system_prompt", "response_format", "state_schema", "context_schema"]:
    assert name in signature'''),
 ("이전과 현재 호출 대조", '''migration = [
 ("create_react_agent", "create_agent", "langgraph.prebuilt에서 langchain.agents로 이동"),
 ("prompt", "system_prompt", "정적 시스템 지시 인자 이름 변경"),
 ("response_format 별도 후처리", "response_format", "에이전트 루프 상태의 structured_response로 반환"),
 ("Pydantic 사용자 상태", "TypedDict 기반 AgentState", "사용자 상태 형식 변경"),
]
for old, new, note in migration: print(f"{old:28} -> {new:28} | {note}")'''),
 ("v1 최소 실행", '''agent = create_agent("openai:gpt-5.4-mini", [], system_prompt="한 문장으로 답하세요.")
result = agent.invoke({"messages": [{"role":"user", "content":"마이그레이션에서 먼저 고정할 것은 무엇인가요?"}]})
print(result["messages"][-1].text)
assert result["messages"][-1].text''')]),
"05-retriever를-도구로-전환": notebook("retriever를 도구로 전환", [
 ("환경 준비", INSTALL21),
 ("로컬 문서와 검색 도구", '''from langchain.agents import create_agent
from langchain.tools import tool
DOCS = {"대출":"일반 도서는 14일 동안 5권까지 대출할 수 있습니다.", "예약":"예약 도서는 도착 알림 뒤 3일 안에 찾아야 합니다.", "운영":"평일 09:00~20:00 운영합니다."}
SEARCH_LOG=[]
@tool
def search_rules(query: str) -> str:
    """자료실 규정에서 질문과 관련된 문장을 검색합니다."""
    SEARCH_LOG.append(query)
    hits=[f"{k}: {v}" for k,v in DOCS.items() if k in query or any(w in query for w in v.split())]
    return "\\n".join(hits) if hits else "검색 결과 없음"'''),
 ("Agentic RAG 실행", '''agent=create_agent("openai:gpt-5.4-mini", [search_rules], system_prompt="규정 질문은 search_rules로 검색하세요. 결과가 없으면 다른 검색어로 한 번 재검색하고, 근거 없는 답은 만들지 마세요.")
SEARCH_LOG.clear()
result=agent.invoke({"messages":[{"role":"user","content":"예약한 도서는 며칠 안에 찾아야 하나요?"}]})
print("searches:", SEARCH_LOG)
print("answer:", result["messages"][-1].text)
print("message types:", [type(m).__name__ for m in result["messages"]])
assert SEARCH_LOG and "3" in result["messages"][-1].text'''),
 ("검색 결과가 없는 질문", '''SEARCH_LOG.clear()
missing=agent.invoke({"messages":[{"role":"user","content":"주차 요금 규정을 알려 주세요."}]})
print("searches:", SEARCH_LOG)
print("answer:", missing["messages"][-1].text)
assert SEARCH_LOG''')]),
"06-같은-평가셋으로-RAG-비교": notebook("고정 RAG와 Agentic RAG 비교", [
 ("환경 준비", INSTALL21 + "\n%pip install -q numpy"),
 ("Ch14 문서와 평가셋 읽기", '''import json
from pathlib import Path
data_dir = Path("labs/part4/ch14-rag-patterns/data")
documents = json.loads((data_dir / "documents.json").read_text(encoding="utf-8"))
queries = json.loads((data_dir / "queries.json").read_text(encoding="utf-8"))
cases = [queries[index] for index in [0, 4, 6]]
print("원천:", data_dir)
print("문서 수:", len(documents), "평가 질문:", [case["qid"] for case in cases])
assert len(documents) == 12 and len(cases) == 3'''),
 ("공통 임베딩 색인 만들기", '''import numpy as np
from langchain_openai import OpenAIEmbeddings
embedder = OpenAIEmbeddings(model="text-embedding-3-small")
document_vectors = np.array(embedder.embed_documents([item["text"] for item in documents]))
document_vectors /= np.linalg.norm(document_vectors, axis=1, keepdims=True)
print("색인 모양:", document_vectors.shape)
assert document_vectors.shape[0] == len(documents)'''),
 ("공통 검색 함수 정의", '''def retrieve(query: str, top_k: int = 2) -> list[dict]:
    """질문 임베딩과 가까운 원문을 top_k개 반환합니다."""
    query_vector = np.array(embedder.embed_query(query))
    query_vector /= np.linalg.norm(query_vector)
    scores = document_vectors @ query_vector
    indices = np.argsort(scores)[::-1][:top_k]
    return [{**documents[index], "score": round(float(scores[index]), 4)} for index in indices]

sample_hits = retrieve(cases[0]["question"])
print([(item["doc_id"], item["score"]) for item in sample_hits])
assert cases[0]["gold_doc_id"] in [item["doc_id"] for item in sample_hits]'''),
 ("고정 RAG와 Agentic RAG 준비", '''from time import perf_counter
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
model = init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none")
search_events: list[dict] = []
@tool
def search_documents(query: str) -> str:
    """Ch14 교육센터 문서에서 질문과 가까운 원문 두 건을 검색합니다."""
    hits = retrieve(query)
    search_events.append({"query": query, "doc_ids": [item["doc_id"] for item in hits]})
    return "\\n".join(f"[{item['doc_id']}] {item['text']}" for item in hits)
agent = create_agent(model, [search_documents], system_prompt="규정 질문에는 search_documents를 사용하세요. 검색 원문에 없는 내용은 만들지 마세요.")
print("비교 경로 준비 완료")'''),
 ("호출별 사용량 집계 함수", '''def usage_total(messages: list) -> dict[str, int]:
    """모든 AIMessage의 입력·출력 토큰을 합산합니다."""
    usages = [message.usage_metadata for message in messages if getattr(message, "usage_metadata", None)]
    return {"input_tokens": sum(item["input_tokens"] for item in usages), "output_tokens": sum(item["output_tokens"] for item in usages), "model_calls": len(usages)}

assert usage_total([]) == {"input_tokens": 0, "output_tokens": 0, "model_calls": 0}'''),
 ("같은 평가셋으로 두 경로 실행", '''records: list[dict] = []
for case in cases:
    hits = retrieve(case["question"])
    context = "\\n".join(f"[{item['doc_id']}] {item['text']}" for item in hits)
    started = perf_counter()
    fixed = model.invoke(f"다음 원문만 사용해 답하세요.\\n{context}\\n질문: {case['question']}")
    fixed_latency = perf_counter() - started
    search_events.clear()
    started = perf_counter()
    agent_result = agent.invoke({"messages": [{"role": "user", "content": case["question"]}]})
    agent_latency = perf_counter() - started
    records.append({"case": case, "fixed_hits": hits, "fixed": fixed, "fixed_latency": fixed_latency, "agent_result": agent_result, "agent_latency": agent_latency, "search_events": list(search_events)})
print("실행 행:", len(records))
assert len(records) == 3'''),
 ("원문 답변과 실행 지표 출력", '''for record in records:
    fixed_usage = usage_total([record["fixed"]])
    agent_messages = record["agent_result"]["messages"]
    agent_usage = usage_total(agent_messages)
    tool_calls = sum(len(getattr(message, "tool_calls", [])) for message in agent_messages)
    print({"qid": record["case"]["qid"], "fixed_answer": record["fixed"].text, "agent_answer": agent_messages[-1].text, "fixed_doc_ids": [item["doc_id"] for item in record["fixed_hits"]], "agent_trace": record["search_events"], "fixed_usage": fixed_usage, "agent_usage": agent_usage, "tool_calls": tool_calls, "fixed_latency_s": round(record["fixed_latency"], 3), "agent_latency_s": round(record["agent_latency"], 3)})
assert all(record["agent_result"]["messages"][-1].text for record in records)'''),
 ("원문 기준 LLM 평가", '''from pydantic import BaseModel
class Grade(BaseModel):
    supported: bool
    explanation: str
grader = model.with_structured_output(Grade, method="json_schema", strict=True)
for record in records:
    gold = next(item for item in documents if item["doc_id"] == record["case"]["gold_doc_id"])
    record["fixed_grade"] = grader.invoke(f"원문과 답의 사실이 맞는지 판정하세요. 원문: {gold['text']} 답: {record['fixed'].text}")
    answer = record["agent_result"]["messages"][-1].text
    record["agent_grade"] = grader.invoke(f"원문과 답의 사실이 맞는지 판정하세요. 원문: {gold['text']} 답: {answer}")
    print(record["case"]["qid"], "fixed:", record["fixed_grade"].model_dump(), "agent:", record["agent_grade"].model_dump())
assert all(isinstance(record["fixed_grade"].supported, bool) and isinstance(record["agent_grade"].supported, bool) for record in records)'''),
 ("정확도·토큰·지연 집계", '''from statistics import mean
summary = {"fixed_accuracy": mean(record["fixed_grade"].supported for record in records), "agent_accuracy": mean(record["agent_grade"].supported for record in records), "fixed_mean_s": round(mean(record["fixed_latency"] for record in records), 3), "agent_mean_s": round(mean(record["agent_latency"] for record in records), 3), "fixed_tokens": sum(usage_total([record["fixed"]])["input_tokens"] + usage_total([record["fixed"]])["output_tokens"] for record in records), "agent_tokens": sum(usage_total(record["agent_result"]["messages"])["input_tokens"] + usage_total(record["agent_result"]["messages"])["output_tokens"] for record in records)}
print(summary)
assert summary["fixed_accuracy"] >= 0 and summary["agent_accuracy"] >= 0'''),
 ("Ch29가 읽을 실제 비교 기록 저장", '''public_rows = []
for record in records:
    agent_messages = record["agent_result"]["messages"]
    public_rows.append({"qid": record["case"]["qid"], "gold_doc_id": record["case"]["gold_doc_id"], "fixed_answer": record["fixed"].text, "agent_answer": agent_messages[-1].text, "fixed_doc_ids": [item["doc_id"] for item in record["fixed_hits"]], "agent_trace": record["search_events"], "fixed_usage": usage_total([record["fixed"]]), "agent_usage": usage_total(agent_messages), "tool_calls": sum(len(getattr(message, "tool_calls", [])) for message in agent_messages), "fixed_latency_s": round(record["fixed_latency"], 3), "agent_latency_s": round(record["agent_latency"], 3), "fixed_supported": record["fixed_grade"].supported, "agent_supported": record["agent_grade"].supported})
output_path = Path("labs/part6/ch21-create-agent/data/rag-comparison.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(public_rows, ensure_ascii=False, indent=2), encoding="utf-8")
print("saved:", output_path, "rows:", len(public_rows))
assert output_path.is_file() and len(public_rows) == 3''')]),
}


TRACE_SETUP = '''from langchain.messages import HumanMessage, AIMessage, ToolMessage
def trace(*tools: str) -> list:
    messages=[HumanMessage("규정을 확인해 주세요.")]
    for i,name in enumerate(tools,1):
        messages += [AIMessage("", tool_calls=[{"name":name,"args":{"topic":"대출"},"id":f"c{i}","type":"tool_call"}]), ToolMessage("확인", tool_call_id=f"c{i}")]
    messages.append(AIMessage("일반 도서는 14일입니다."))
    return messages
reference=trace("search_rules", "check_source")'''

NB29 = {
"01-에이전트-평가-세-전략": notebook("에이전트 평가 세 전략", [
 ("환경 준비", INSTALL29), ("기준 궤적 준비", TRACE_SETUP),
 ("세 종류의 평가 입력 만들기", '''actual=trace("search_rules", "check_source")
final_response = "14일" in actual[-1].text
single_step = actual[1].tool_calls[0]["name"] == "search_rules"
trajectory = [call["name"] for m in actual for call in getattr(m,"tool_calls",[])]
print({"final_response":final_response,"single_step":single_step,"trajectory":trajectory})'''),
 ("최종 답만 맞는 나쁜 경로 비교", '''wasteful=trace("search_rules","search_rules","search_rules","check_source")
print("final pass:", "14일" in wasteful[-1].text)
print("reference calls:", 2, "wasteful calls:", sum(len(getattr(m,"tool_calls",[])) for m in wasteful))
assert "14일" in wasteful[-1].text and len(wasteful)>len(reference)''')]),
"02-궤적-매칭-네-모드": notebook("궤적 매칭 네 모드", [
 ("환경 준비", INSTALL29), ("기준 궤적 준비", TRACE_SETUP + '\nprint([c["name"] for m in reference for c in getattr(m,"tool_calls",[])])'),
 ("strict와 unordered 실행", '''from agentevals.trajectory.match import create_trajectory_match_evaluator
reversed_trace=trace("check_source","search_rules")
strict_score=create_trajectory_match_evaluator(trajectory_match_mode="strict")(outputs=reversed_trace,reference_outputs=reference)
unordered_score=create_trajectory_match_evaluator(trajectory_match_mode="unordered")(outputs=reversed_trace,reference_outputs=reference)
print("strict", strict_score)
print("unordered", unordered_score)
assert strict_score["score"] is False and unordered_score["score"] is True'''),
 ("subset과 superset 실행", '''short=trace("search_rules")
extra=trace("search_rules","check_source","audit_log")
for label,actual in [("short",short),("extra",extra)]:
    print(label)
    for mode in ["subset","superset"]:
        print(mode, create_trajectory_match_evaluator(trajectory_match_mode=mode)(outputs=actual,reference_outputs=reference)["score"])
short_subset=create_trajectory_match_evaluator(trajectory_match_mode="subset")(outputs=short,reference_outputs=reference)
extra_superset=create_trajectory_match_evaluator(trajectory_match_mode="superset")(outputs=extra,reference_outputs=reference)
print("subset은 실제 호출이 기준 호출 범위 안에 있는지, superset은 실제 호출이 기준의 필수 호출을 모두 포함하는지 봅니다.")
assert short_subset["score"] is True and extra_superset["score"] is True''')]),
"03-LLM-judge로-궤적-평가": notebook("LLM judge로 궤적 평가", [
 ("환경 준비", INSTALL29 + '\nassert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY가 필요합니다."'), ("평가할 궤적", TRACE_SETUP + '\nactual=trace("search_rules","check_source")'),
 ("실제 LLM judge 실행", '''from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
evaluator=create_trajectory_llm_as_judge(model="openai:gpt-5.4-mini",prompt=TRAJECTORY_ACCURACY_PROMPT)
evaluation=evaluator(outputs=actual,reference_outputs=reference)
print(evaluation)
assert evaluation["score"] in [True, False]'''),
 ("결정적 검사와 함께 보기", '''from agentevals.trajectory.match import create_trajectory_match_evaluator
deterministic=create_trajectory_match_evaluator(trajectory_match_mode="strict")(outputs=actual,reference_outputs=reference)
print("strict:", deterministic)
print("judge:", evaluation)
assert deterministic["score"] is True''')]),
"04-운영-지표와-Ch18-궤적-비교": notebook("운영 지표와 Ch18 궤적 비교", [
 ("환경 준비", INSTALL29),
 ("프로젝트 루트 찾기", '''import json
from pathlib import Path
def find_project_root(start: Path) -> Path:
    """필요한 textbook과 labs 폴더가 함께 있는 상위 경로를 찾습니다."""
    for folder in [start, *start.parents]:
        if (folder / "textbook").is_dir() and (folder / "labs").is_dir():
            return folder
    raise FileNotFoundError("프로젝트 루트를 찾지 못했습니다.")
root = find_project_root(Path.cwd())
print("project root:", root.name)
assert (root / "커리큘럼_v6.html").is_file()'''),
 ("Ch18 실제 워크플로우 출력 읽기", '''ch18_path = root / "labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb"
ch18_nb = json.loads(ch18_path.read_text(encoding="utf-8"))
printed = "\\n".join("".join(out.get("text", [])) for cell in ch18_nb["cells"] for out in cell.get("outputs", []) if out.get("output_type") == "stream")
table_lines = [line for line in printed.splitlines() if " | " in line and not line.startswith("pattern")]
print("Ch18 실제 표 행:", len(table_lines))
print("\\n".join(table_lines[-5:]))
assert len(table_lines) >= 5'''),
 ("Ch18 출력 공통 필드로 변환", '''workflow_rows: list[dict] = []
for line in table_lines[-5:]:
    pattern, calls, tokens, latency, quality, status = [part.strip() for part in line.split("|")]
    workflow_rows.append({"system": f"Ch18:{pattern}", "final_score": int(quality) / 5, "model_calls": int(calls), "tool_calls": 0, "tokens": int(tokens), "latency_s": float(latency), "trace_source": "Ch18 notebook output", "status": status})
print(workflow_rows)
assert all(row["status"] == "ok" for row in workflow_rows)'''),
 ("Ch21 실제 Agentic RAG 기록 읽기", '''agent_path = root / "labs/part6/ch21-create-agent/data/rag-comparison.json"
agent_records = json.loads(agent_path.read_text(encoding="utf-8"))
print("Ch21 실제 행:", len(agent_records), "qid:", [row["qid"] for row in agent_records])
assert len(agent_records) == 3'''),
 ("Agent 궤적을 공통 필드로 변환", '''agent_rows: list[dict] = []
for record in agent_records:
    usage = record["agent_usage"]
    agent_rows.append({"system": f"Ch21:{record['qid']}", "final_score": float(record["agent_supported"]), "model_calls": usage["model_calls"], "tool_calls": record["tool_calls"], "tokens": usage["input_tokens"] + usage["output_tokens"], "latency_s": record["agent_latency_s"], "trace_source": record["agent_trace"]})
print(agent_rows)
assert all(row["tool_calls"] >= 1 for row in agent_rows)'''),
 ("실제 두 기록 비교", '''from statistics import mean
for label, rows in [("Ch18 workflow", workflow_rows), ("Ch21 agent", agent_rows)]:
    summary = {"system": label, "runs": len(rows), "final_score_mean": round(mean(row["final_score"] for row in rows), 3), "model_calls_mean": round(mean(row["model_calls"] for row in rows), 3), "tool_calls_mean": round(mean(row["tool_calls"] for row in rows), 3), "tokens_mean": round(mean(row["tokens"] for row in rows), 1), "latency_mean_s": round(mean(row["latency_s"] for row in rows), 3)}
    print(summary)
assert workflow_rows and agent_rows'''),
 ("실제 Agent 기록의 p95 계산", '''import math
def nearest_rank_p95(values: list[float]) -> float:
    """표본을 정렬하고 ceil(0.95*n)번째 값을 반환합니다."""
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]
agent_latency_p95 = nearest_rank_p95([row["latency_s"] for row in agent_rows])
agent_tokens_p95 = nearest_rank_p95([float(row["tokens"]) for row in agent_rows])
print({"actual_agent_runs": len(agent_rows), "latency_p95_s": agent_latency_p95, "tokens_p95": agent_tokens_p95})
assert agent_latency_p95 >= max(row["latency_s"] for row in agent_rows)
print("세 건의 작은 표본이므로 운영 기준을 정하려면 더 많은 실제 대화가 필요합니다.")''')]),
}


LESSON_META = {
"01-create-agent와-ReAct-루프": ("create_agent와 ReAct 루프", "create_agent의 세 인자가 Ch20의 모델·도구·지시를 어떻게 묶고, 반환 그래프가 어떤 루프를 실행하는가?", "Ch20에서 직접 연결한 StateGraph와 ToolNode", "02-구조화-출력-두-전략"),
"02-구조화-출력-두-전략": ("구조화 출력 두 전략", "ToolStrategy와 ProviderStrategy는 어디에서 스키마를 강제하고 결과를 어떤 키로 반환하는가?", "앞 절의 create_agent 호출", "03-AgentState와-context-schema"),
"03-AgentState와-context-schema": ("AgentState와 context_schema", "실행 중 누적되는 상태와 호출 때 주입하는 컨텍스트를 어떻게 구분하는가?", "MessagesState와 TypedDict 상태", "04-0x에서-1x로-마이그레이션"),
"04-0x에서-1x로-마이그레이션": ("0.x에서 1.x로 마이그레이션", "이전 create_react_agent 코드를 v1 create_agent로 옮길 때 무엇을 바꾸어야 하는가?", "Ch20의 직접 조립 그래프", "05-retriever를-도구로-전환"),
"05-retriever를-도구로-전환": ("retriever를 도구로 전환", "항상 한 번 검색하던 RAG에서 모델이 검색과 재검색 여부를 선택하게 하려면 무엇이 필요한가?", "Part4의 검색 파이프라인과 Ch19의 @tool", "06-같은-평가셋으로-RAG-비교"),
"06-같은-평가셋으로-RAG-비교": ("같은 평가셋으로 RAG 비교", "고정 RAG와 Agentic RAG를 같은 질문으로 비교하면 정확도·지연·실패 양상이 어떻게 달라지는가?", "앞 절의 검색 도구", "Ch22 Middleware"),
"01-에이전트-평가-세-전략": ("에이전트 평가 세 전략", "Final Response·Single step·Trajectory는 각각 어떤 실패를 발견하는가?", "Ch11 평가셋과 Ch21 에이전트", "02-궤적-매칭-네-모드"),
"02-궤적-매칭-네-모드": ("궤적 매칭 네 모드", "정답 경로가 여러 개일 때 strict·unordered·subset·superset 중 무엇을 선택해야 하는가?", "앞 절의 메시지 궤적", "03-LLM-judge로-궤적-평가"),
"03-LLM-judge로-궤적-평가": ("LLM judge로 궤적 평가", "정확 일치로 잡기 어려운 합리적 경로를 LLM judge가 어떻게 평가하는가?", "결정적 궤적 매칭", "04-운영-지표와-Ch18-궤적-비교"),
"04-운영-지표와-Ch18-궤적-비교": ("운영 지표와 Ch18 궤적 비교", "개발 평가를 운영의 스텝·도구 호출·비용 p95와 어떻게 연결하는가?", "Ch18의 실제 워크플로우 비교 출력", "Ch30 최종 프로젝트 평가 설계"),
}

DETAILS = {
"01-create-agent와-ReAct-루프": {
"why":"Ch20에서는 model 노드, tools_condition, ToolNode, tools→model 엣지를 직접 연결했습니다. create_agent를 사용하면 호출 한 줄로 같은 반복 구조를 얻지만, 문제가 생겼을 때 어느 단계에서 멈췄는지 읽으려면 내부 그래프를 알아야 합니다.",
"concept":"ReAct는 모델이 상황을 읽고 다음 행동을 정한 뒤 도구 결과를 다시 관찰하는 반복 방식입니다. create_agent의 model은 판단과 답변을 생성하고, tools는 모델이 선택할 수 있는 동작을 제공하며, system_prompt는 근거 사용과 종료 기준을 지시합니다. 반환값은 CompiledStateGraph이므로 invoke, stream, get_graph 같은 LangGraph 인터페이스를 그대로 사용합니다.",
"diagram":"사용자 질문→model→도구 선택→ToolNode→model 또는 END 순서로 읽습니다. 마지막 model이 tool_calls를 만들면 초록 ToolNode로 이동하고, 만들지 않으면 END로 이동합니다.",
"result":"실제 실행은 HumanMessage, 도구 호출이 든 AIMessage, 규정 원문 ToolMessage, 최종 AIMessage의 4개 메시지를 남겼습니다. lookup_policy의 topic은 대출이었고 답에는 14일이 포함됐습니다. get_graph().draw_mermaid_png()는 PNG 서명과 8,388바이트를 반환했습니다. 두 모델 호출의 합은 입력 379토큰, 출력 47토큰, 추정 0.000496달러였습니다.",
"limit":"그래프 PNG는 구조를 보여 주지만 특정 질문에서 실제로 지난 엣지는 보여 주지 않습니다. 실제 경로는 메시지와 stream 기록으로 함께 확인해야 합니다.",
"quiz":[("create_agent의 세 필수 학습 요소는 무엇인가요?","model, tools, system_prompt입니다."),("도구 결과는 어떤 메시지로 모델에 전달되나요?","ToolMessage로 전달됩니다."),("반환 그래프를 확인한 메서드는 무엇인가요?","get_graph()와 draw_mermaid_png()입니다.")],},
"02-구조화-출력-두-전략": {
"why":"자연어 답을 정규식으로 잘라 쓰면 필드가 빠지거나 형태가 바뀔 때 오류가 늦게 드러납니다. 에이전트 루프 안에서 스키마를 검증하면 후속 코드가 topic, answer, source 필드를 확정된 형식으로 받을 수 있습니다.",
"concept":"ToolStrategy는 구조화 결과를 도구 호출 형식으로 만들고 LangChain이 스키마를 검증합니다. ProviderStrategy는 모델 제공자의 네이티브 구조화 출력 기능을 사용합니다. 두 방식 모두 최종 상태의 structured_response에 Pydantic 객체를 저장합니다. 스키마 유형을 직접 넘기면 모델 프로필에 따라 전략을 자동 선택할 수도 있습니다.",
"diagram":"출력 스키마에서 두 갈래로 나뉜 뒤 structured_response에서 합쳐집니다. 초록 ToolStrategy는 도구 메시지를 거치고, 보라색 ProviderStrategy는 제공자 응답 형식을 사용합니다.",
"result":"같은 R-14 문장을 두 전략에 입력했습니다. ToolStrategy는 전체 메시지 3개, AIMessage 1개였고 ProviderStrategy는 전체 2개, AIMessage 1개였습니다. 두 결과 모두 대출 기간 14일과 출처 R-14를 검증했습니다. 추가 모델 호출이 없다는 말은 확인됐지만 ToolStrategy의 추가 메시지까지 없다는 뜻은 아닙니다.",
"limit":"ProviderStrategy의 사용 가능 여부는 모델 프로필과 제공자 기능에 달려 있습니다. 도구와 구조화 출력을 동시에 쓸 때는 모델이 두 기능을 함께 지원하는지도 확인해야 합니다.",
"quiz":[("검증된 객체는 어느 상태 키에 있나요?","structured_response입니다."),("ProviderStrategy는 어디에서 스키마를 강제하나요?","모델 제공자의 네이티브 기능에서 강제합니다."),("이번 실행에서 두 전략의 AIMessage 수는 몇 개인가요?","각각 1개입니다.")],},
"03-AgentState와-context-schema": {
"why":"사용자 식별자나 권한을 대화 메시지에 매번 붙이면 모델이 필요 없는 내부 값까지 읽습니다. 실행 상태와 호출 컨텍스트를 나누면 기록할 값과 도구에만 주입할 값을 구분할 수 있습니다.",
"concept":"AgentState는 messages와 structured_response를 포함하는 TypedDict 기반 상태입니다. 사용자 필드를 추가한 SupportState는 request_tag를 실행 결과까지 유지합니다. context_schema는 실행 중 도구와 미들웨어가 읽을 컨텍스트의 형식을 선언합니다. ToolRuntime[UserContext]를 받은 도구는 runtime.context로 user_id와 access_level을 읽습니다.",
"diagram":"invoke 입력에서 AgentState와 context가 갈라집니다. request_tag는 최종 상태까지 이어지고, UserContext는 current_access 도구가 읽은 뒤 도구 결과 문자열에만 반영됩니다.",
"result":"request_tag=lesson-03은 최종 상태 키에 남았습니다. context로 전달한 student-7과 read-only는 도구 답에 나타났지만 결과 상태에 context 키가 자동으로 생기지 않았습니다. 이 차이를 두 assert로 확인했습니다.",
"limit":"context를 상태에 자동 보존하지 않는다고 해서 로그에도 남지 않는다는 뜻은 아닙니다. 추적 시스템과 도구 로그에 민감 정보가 기록되는지 별도로 점검해야 합니다.",
"quiz":[("request_tag는 왜 AgentState에 두나요?","실행 중 누적하고 최종 결과에서도 확인할 값이기 때문입니다."),("access_level은 어디에서 읽나요?","도구의 ToolRuntime.context에서 읽습니다."),("사용자 상태 스키마는 어떤 형식을 사용하나요?","TypedDict 기반 AgentState를 확장합니다.")],},
"04-0x에서-1x로-마이그레이션": {
"why":"이름만 바꾸면 마이그레이션이 끝난다고 생각하기 쉽지만 반환 상태와 사용자 상태 형식도 달라졌습니다. 먼저 입력·출력 경계를 고정해야 기존 호출자의 동작을 보존할 수 있습니다.",
"concept":"v1의 create_agent는 langchain.agents에서 가져옵니다. 이전 langgraph.prebuilt.create_react_agent의 prompt는 정적 지시에서 system_prompt로 대응합니다. 구조화 결과는 별도 후처리보다 response_format과 structured_response를 사용합니다. 사용자 상태는 Pydantic 모델 대신 TypedDict 기반 AgentState를 사용합니다.",
"diagram":"0.x API 목록을 현재 inspect.signature 결과와 대조하고 v1 최소 실행으로 이어집니다. 각 화살표는 이름 치환이 아니라 호출 경계의 대응을 뜻합니다.",
"result":"설치된 1.4.0 서명에서 model, tools, system_prompt, response_format, state_schema, context_schema를 모두 확인했습니다. create_react_agent→create_agent, prompt→system_prompt 등 네 행을 출력하고 v1 에이전트의 실제 답을 받았습니다.",
"limit":"동적 프롬프트와 상태 변경은 단순 인자 치환으로 옮길 수 없습니다. v1에서는 미들웨어가 권장되는 경우가 있으므로 Ch22에서 훅 단위로 다시 확인합니다.",
"quiz":[("create_agent의 새 import 경로는 무엇인가요?","langchain.agents입니다."),("정적 prompt에 대응하는 v1 인자는 무엇인가요?","system_prompt입니다."),("마이그레이션 전에 고정할 것은 무엇인가요?","입력·출력 상태와 도구 부작용 같은 경계입니다.")],},
"05-retriever를-도구로-전환": {
"why":"고정 RAG는 모든 질문에 같은 검색 단계를 실행합니다. retriever를 도구로 노출하면 모델이 검색 필요 여부와 검색어를 정할 수 있고, 결과가 없을 때 한 번 더 찾아볼 수 있습니다.",
"concept":"Agentic RAG는 검색 증강 생성의 검색 단계를 에이전트 도구로 제공합니다. search_rules는 읽기 전용 규정 자료를 조회하고 검색어를 SEARCH_LOG에 남깁니다. system_prompt는 규정 질문에서 검색하고 결과가 없으면 다른 검색어로 한 번 재검색하며 근거를 만들지 말라고 제한합니다.",
"diagram":"질문 뒤 모델이 검색 여부를 고르고 search_rules 결과를 관찰합니다. 근거가 부족하면 재검색 화살표를 따르고, 충분하면 근거 답을 작성합니다.",
"result":"예약 도서 질문은 검색 도구를 호출했고 최종 답에 보관 기간 3일이 포함됐습니다. 주차 요금 질문은 주차 규정이 없음을 설명했으며 SEARCH_LOG에는 첫 검색과 다른 표현의 재검색이 남았습니다. 이 경로는 키워드 if문이 아니라 실제 모델의 tool_calls로 결정됐습니다.",
"limit":"재검색을 허용하면 recall이 좋아질 가능성이 있지만 호출 수와 지연도 늘 수 있습니다. 반복 상한과 근거 없음 응답을 함께 두어야 합니다.",
"quiz":[("retriever를 도구로 만들면 누가 검색 여부를 정하나요?","모델이 tool_calls로 정합니다."),("재검색을 무한히 허용하면 어떤 문제가 생기나요?","호출 수·지연·비용이 계속 늘 수 있습니다."),("근거가 없을 때의 안전한 답은 무엇인가요?","자료에서 확인하지 못했다고 범위를 밝히는 답입니다.")],},
"06-같은-평가셋으로-RAG-비교": {
"why":"Agentic RAG의 코드가 더 복잡하다는 사실만으로 품질 향상을 말할 수 없습니다. Ch14의 같은 문서와 질문을 두 경로에 넣고 답·검색 문서·토큰·지연을 함께 비교해야 합니다.",
"concept":"고정 RAG는 질문 임베딩으로 상위 두 문서를 검색한 뒤 모델을 한 번 호출합니다. Agentic RAG는 같은 색인을 search_documents 도구로 제공하고 모델이 검색어를 작성합니다. 평가 표본은 Ch14 documents.json 12건과 queries.json의 C01·C05·C07입니다. Grade 스키마의 judge가 사람이 지정한 gold_doc_id 원문과 답을 함께 읽어 supported를 판정합니다.",
"diagram":"같은 평가셋에서 고정 RAG와 Agentic RAG가 갈라지고 정확도·토큰·지연 열에서 합쳐집니다. 두 갈래는 문서, 임베딩 모델, 생성 모델, judge 기준을 공유합니다.",
"result":"Agent 경로는 세 질문 모두 supported=True였고 고정 RAG는 2/3이었습니다. C01 고정 답은 전자책 7일을 함께 제시해 gold 원문만으로 답을 지지할 수 없다는 판정을 받았고 Agent 답은 일반 도서 14일에 집중했습니다. Agent는 각 질문에서 모델 2회·도구 1회를 사용했고 토큰은 520·491·544, 지연은 2.037·1.631·1.986초였습니다. 고정 RAG는 모델 1회이며 토큰은 113·118·122였습니다. 이 세 문항에서는 Agent 답의 지지율이 높았지만 호출 수와 전체 토큰이 늘었습니다.",
"limit":"세 문항 모두 첫 검색에 정답 문서가 포함돼 재검색 이점을 시험하지 못했습니다. judge도 모델이므로 사람 검토와 더 큰 평가셋이 필요합니다.",
"quiz":[("두 경로에서 같게 둔 것은 무엇인가요?","Ch14 문서·질문, 임베딩 색인, 생성 모델, 판정 기준입니다."),("Agent 경로의 질문당 모델 호출 수는 몇 회였나요?","도구 선택과 최종 답으로 2회였습니다."),("이번 결과에서 Agent가 항상 낫다고 말할 수 있나요?","아닙니다. 정확도는 동률이고 호출과 지연은 늘었습니다.")],},
"01-에이전트-평가-세-전략": {
"why":"최종 답이 14일로 맞아도 search_rules를 세 번 반복하면 운영 비용과 장애 가능성이 커집니다. 답과 내부 행동을 서로 다른 평가 단위로 보아야 이런 실패를 찾을 수 있습니다.",
"concept":"Final Response는 전체 실행을 블랙박스로 보고 마지막 답을 채점합니다. Single step은 특정 시점의 도구 선택이나 인자를 검사합니다. Trajectory는 시작부터 끝까지의 AIMessage와 ToolMessage 순서를 평가합니다. 세 전략은 서로 대체하지 않으며 발견하려는 실패에 따라 함께 사용합니다.",
"diagram":"하나의 에이전트 실행에서 세 측정 상자가 나옵니다. Final Response는 마지막 문장, Single step은 첫 tool_calls, Trajectory는 모든 호출 순서를 읽습니다.",
"result":"정상 궤적은 search_rules→check_source였고 final_response와 single_step이 모두 True였습니다. 낭비 궤적은 같은 14일 답을 반환해 최종 응답 평가는 통과했지만 도구 호출이 기준 2회에서 4회로 늘었습니다.",
"limit":"Single step 통과는 다음 단계가 옳다는 보장이 아니며 Trajectory 통과는 최종 문장의 사실 정확성을 보장하지 않습니다.",
"quiz":[("최종 답 평가가 놓친 실패는 무엇인가요?","같은 검색의 반복과 불필요한 도구 호출입니다."),("첫 도구 선택만 검사하는 전략은 무엇인가요?","Single step입니다."),("전체 도구 순서를 보는 전략은 무엇인가요?","Trajectory입니다.")],},
"02-궤적-매칭-네-모드": {
"why":"올바른 경로가 여러 개인 문제에 strict를 적용하면 순서만 다른 정상 실행을 탈락시킵니다. 반대로 필수 순서가 있는 승인 절차에 unordered를 쓰면 위험한 순서도 통과합니다.",
"concept":"strict는 메시지 구조와 도구 호출 순서가 기준과 같아야 합니다. unordered는 같은 호출을 순서와 무관하게 요구합니다. subset은 실제 호출이 기준 호출 범위 안에 있는지 보고 누락을 허용합니다. superset은 기준의 필수 호출을 실제 호출이 모두 포함하는지 보고 추가 호출을 허용합니다.",
"diagram":"기준 궤적이 네 검사 상자로 들어갑니다. strict와 unordered는 동등성의 두 방식이고 subset과 superset은 포함 방향이 서로 반대입니다.",
"result":"search_rules와 check_source의 순서를 뒤집자 strict=False, unordered=True였습니다. search_rules만 호출한 짧은 궤적은 subset=True·superset=False였고 audit_log를 추가한 궤적은 subset=False·superset=True였습니다. 따라서 subset 점수를 효율 자체로 부르지 않습니다.",
"limit":"기본 매칭은 도구 이름과 인자까지 비교합니다. 특정 인자를 무시하면 검사 범위가 좁아지므로 이유를 평가 정의에 기록해야 합니다.",
"quiz":[("순서만 다른 궤적을 허용하는 모드는 무엇인가요?","unordered입니다."),("필수 호출을 모두 포함했는지 보는 모드는 무엇인가요?","superset입니다."),("subset만으로 효율을 보장할 수 없는 이유는 무엇인가요?","필요한 호출을 빠뜨린 짧은 궤적도 통과할 수 있기 때문입니다.")],},
"03-LLM-judge로-궤적-평가": {
"why":"도구 이름이 정확히 같아도 질문과 도구 인자의 의미가 어긋날 수 있습니다. 의미와 효율을 함께 읽으려면 루브릭을 받은 judge가 전체 메시지를 평가하는 방법이 필요합니다.",
"concept":"LLM-as-judge는 다른 언어 모델이 평가 루브릭과 실제 궤적을 읽고 점수와 설명을 반환하는 방식입니다. agentevals의 TRAJECTORY_ACCURACY_PROMPT는 단계의 논리, 진행, 상대적 효율, 기준 궤적과의 의미 동등성을 묻습니다. 결정적 매칭과 함께 쓰면 구조 차이와 의미 차이를 구분할 수 있습니다.",
"diagram":"실제 궤적과 평가 루브릭이 LLM judge에 함께 들어가고 trajectory_accuracy 점수와 comment가 나옵니다.",
"result":"실제 궤적과 기준 궤적이 같아 strict는 True였습니다. 그러나 judge는 사용자의 모호한 ‘규정을 확인해 주세요’에서 대출 주제를 임의로 선택했고 도구 결과가 14일 답을 충분히 뒷받침하지 못한다고 설명하며 False를 반환했습니다. 같은 구조도 의미 검토에서는 실패할 수 있음을 확인했습니다.",
"limit":"judge 평가는 모델과 프롬프트에 따라 달라지고 별도 토큰·지연·비용이 듭니다. 권한이나 필수 순서는 결정적 검사로 남겨야 합니다.",
"quiz":[("이번 궤적의 strict 점수는 무엇이었나요?","True였습니다."),("judge가 False로 본 핵심 이유는 무엇인가요?","질문에서 대출 주제를 뒷받침할 근거가 없었기 때문입니다."),("judge만으로 권한 순서를 검사하면 안 되는 이유는 무엇인가요?","결과가 비결정적이고 필수 규칙을 놓칠 수 있기 때문입니다.")],},
"04-운영-지표와-Ch18-궤적-비교": {
"why":"개발 단계의 통과율만 보면 호출 증가와 꼬리 지연을 놓칩니다. Ch18 워크플로우와 Ch21 에이전트의 실제 기록을 같은 열로 바꾸면 최종 품질과 실행 비용을 함께 볼 수 있습니다.",
"concept":"운영 지표는 실제 대화에서 계속 모으는 측정값입니다. 이 절의 공통 열은 final_score, model_calls, tool_calls, tokens, latency_s입니다. p95는 측정값을 작은 값부터 정렬했을 때 95% 지점의 nearest-rank 값으로, 평균에 숨는 느린 실행을 보는 데 사용합니다.",
"diagram":"Ch18 노트북 출력과 Ch21 rag-comparison.json이 공통 열 변환 코드를 거쳐 스텝·도구·토큰·지연 상자로 모입니다.",
"result":"Ch18 다섯 패턴은 평균 final_score 0.88, 모델 2.8회, 610.2토큰, 4.145초였습니다. Ch21 세 Agentic RAG 행은 평균 final_score 1.0, 모델 2회, 도구 1회, 518.3토큰, 1.885초였습니다. Agent 세 건의 p95는 지연 2.037초, 토큰 544였습니다. 서로 다른 과제와 표본 수이므로 이 숫자로 시스템 우열을 정하지 않습니다.",
"limit":"Ch18 quality/5와 Ch21 supported는 판정 척도가 다릅니다. 공통 열 변환은 운영 화면을 맞추는 작업이며 직접 성능 대결이 아닙니다. p95도 세 건으로 안정적인 운영 기준을 만들 수 없습니다.",
"quiz":[("p95를 보는 이유는 무엇인가요?","평균에 가려지는 느린 실행과 높은 비용을 보기 위해서입니다."),("Ch18과 Ch21의 final_score를 바로 비교할 수 없는 이유는 무엇인가요?","평가 과제와 척도가 다르기 때문입니다."),("이번 Agent 기록의 지연 p95는 얼마였나요?","2.037초였습니다.")],},
}

LESSON_HOURS = {
    "01-create-agent와-ReAct-루프": "강의 1h | 실습 1.5h",
    "02-구조화-출력-두-전략": "강의 1h | 실습 1.5h",
    "03-AgentState와-context-schema": "강의 1h | 실습 1.5h",
    "04-0x에서-1x로-마이그레이션": "강의 1h | 실습 1.5h",
    "05-retriever를-도구로-전환": "강의 1h | 실습 2h",
    "06-같은-평가셋으로-RAG-비교": "강의 1h | 실습 2h",
    "01-에이전트-평가-세-전략": "강의 0.75h | 실습 1.25h",
    "02-궤적-매칭-네-모드": "강의 0.75h | 실습 1.25h",
    "03-LLM-judge로-궤적-평가": "강의 0.75h | 실습 1.25h",
    "04-운영-지표와-Ch18-궤적-비교": "강의 0.75h | 실습 1.25h",
}


def source(slug: str, chapter: int) -> str:
    title, question, prior, nxt = LESSON_META[slug]
    item = DETAILS[slug]
    fig = slug.split("-",1)[0] + "-흐름"
    refs = ("https://docs.langchain.com/oss/python/langchain/agents", "https://docs.langchain.com/oss/python/langchain/structured-output") if chapter == 21 else ("https://docs.langchain.com/oss/python/langchain/test/evals", "https://docs.langchain.com/langsmith/trajectory-evals")
    quiz = "".join(f'<details class="quiz"><summary>{index}. {prompt}</summary><p class="quiz-a"><b>해설</b> — {answer}</p></details>' for index, (prompt, answer) in enumerate(item["quiz"], 1))
    return f'''<!--meta: {LESSON_HOURS[slug]} | 코드 Jupyter Notebook | 새 용어 5 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>{title}의 핵심 요소를 실제 코드에서 찾을 수 있습니다.</li><li>노트북 출력으로 실행 경로와 결과를 설명할 수 있습니다.</li><li>한계와 적용 조건을 구분해 평가할 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{question}</p><p>{item['why']}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{prior}를 사용합니다. 필요한 자료와 객체는 노트북에서 다시 선언하므로 앞 노트북의 메모리 상태는 필요하지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>정의와 구체 예</h3><p>{item['concept']}</p><h3>도식 읽기</h3>{{{{svg:{fig}}}}}<p>{item['diagram']}</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>준비 셀에서 Python 3.12와 고정 패키지를 확인한 뒤, 데이터·함수·객체 생성·invoke·관찰을 짧은 셀로 나누어 실행합니다. 각 코드 셀의 첫 주석은 그 셀에서 확인할 행동을 설명합니다.</p>{{{{notebook:{slug}}}}}<p class="look"><b>확인할 점</b> — {item['result']}</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>{item['result']}</p><p>{item['limit']}</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>{item['limit']}</li><li>실제 모델 호출 비용은 절당 1달러 미만으로 예상하며, API 키 값은 출력하지 않습니다.</li><li>재실행하면 모델 문장과 지연이 달라질 수 있으므로 저장된 원문 출력과 조건을 함께 읽습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>{item['concept']}</li><li>{item['result']}</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — {nxt}에서 이 결과를 다시 사용합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quiz}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><a href="{refs[0]}">LangChain 공식 문서</a> · 확인 {DATE} · langchain 1.4.0</li><li><a href="{refs[1]}">LangChain 공식 세부 문서</a> · 확인 {DATE}</li></ul>'''


def write_chapter(chapter: int, slug: str, notebooks: dict[str, dict], hours: str) -> None:
    if chapter == 21:  # Ch 21 개선본을 옛 판으로 덮어쓰지 않도록 건너뜀(2026-09-25)
        print("skip ch21: textbook/part6/ch21-create-agent/qa/upgrade/author_NN.py가 Ch 21 파일을 씁니다")
        return
    text_dir = ROOT / f"textbook/part6/{slug}"
    lab_dir = ROOT / f"labs/part6/{slug}"
    config = json.loads((text_dir / "chapter.json").read_text())
    config.update({"part_title":"Part 6 · Agent 개발", "hours":hours, "objectives":["에이전트의 실행 구조를 코드와 궤적으로 설명합니다.", "같은 평가셋과 명시적 기준으로 동작을 비교합니다."]})
    for section in config["sections"]:
        section["format"] = "experiment"
    (text_dir / "chapter.json").write_text(json.dumps(config, ensure_ascii=False, indent=2)+"\n")
    for name, nb in notebooks.items():
        if not os.getenv("SOURCES_ONLY"):
            (lab_dir / "notebooks" / f"{name}.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1)+"\n")
        (text_dir / "_src" / f"{name}.html").write_text(source(name, chapter))


write_chapter(21, "ch21-create-agent", NB21, "총 16h · 강의 6h · 실습 10h")
write_chapter(29, "ch29-agent-evaluation", NB29, "총 8h · 강의 3h · 실습 5h")
print("authored", len(NB21) + len(NB29), "lessons")
