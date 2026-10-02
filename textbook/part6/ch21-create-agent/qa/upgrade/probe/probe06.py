"""Ch 21 06절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe06.py <회차 시작 번호> <회차 수> <기록 파일(JSONL, 이어 쓰기)> [질문 ID 쉼표 목록]
  기본 질문: C01,C05,C07 (06-probe.md §0-2)
자료·검색 도구·시스템 메시지 글은 05절 노트북과 같은 코드, 고정 흐름·판정은 06-probe.md §0-2.
검색 함수는 Ch 14 도구 파일, 판정 함수는 Ch 15 도구 파일(rag_tools.py 둘)을 가져오기만 한다(바이트 코드를 쓰지 않음).
"""
import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[6]
CH14 = ROOT / "labs/part4/ch14-rag-patterns"
CH15 = ROOT / "labs/part4/ch15-evaluation-advanced"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rag14 = load("rag14", CH14 / "notebooks/rag_tools.py")
rag15 = load("rag15", CH15 / "notebooks/rag_tools.py")
search_hits = rag14.search_hits
find_gold_rank = rag14.find_gold_rank
build_judge_prompt = rag15.build_judge_prompt
judge_once = rag15.judge_once

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from langchain.agents import create_agent  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402
from langchain_openai import OpenAIEmbeddings  # noqa: E402

SYSTEM_TEXT = ("교육센터 자료실 안내 도우미입니다. 자료실 이용을 묻는 질문에는 search_documents 도구로 찾은 문서 글에 근거해 답하세요. "
               "찾은 문서에 답이 없으면 검색어를 바꿔 한 번만 더 검색하고, 그래도 없으면 문서에서 찾지 못했다고 답하세요.")
ANSWER_HEAD = ("교육센터 자료실 안내 도우미입니다. 자료실 이용을 묻는 질문에는 아래 자료의 문서 글에 근거해 답하세요. "
               "자료에 답이 없으면 문서에서 찾지 못했다고 답하세요.\n\n")
JUDGE_VERSION = "rag-judge-v1.0.0"
JUDGE_HEAD = "답이 근거 문서로 뒷받침되면 1, 아니면 0을 판정하세요." + "\n" + 'JSON만 출력하세요: {"score": 0 또는 1, "reason": "한 문장"}.'
JUDGE_PAIR = {"답": "response", "근거 문서": "context"}

docs = json.loads((CH14 / "data/documents.json").read_text(encoding="utf-8"))
queries = json.loads((CH14 / "data/queries.json").read_text(encoding="utf-8"))
doc_texts, doc_ids, text_by_doc = [], [], {}
for doc in docs:
    doc_text = doc["title"] + " " + doc["text"]
    doc_texts.append(doc_text)
    doc_ids.append(doc["doc_id"])
    text_by_doc[doc["doc_id"]] = doc_text
top_count = 3
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)
doc_vectors = embedding_model.embed_documents(doc_texts)  # 임베딩 요청 1번
COUNT = {"embed_doc": 1, "embed_search": 0, "model_answer": 0, "model_agent": 0, "model_judge": 0}


@tool
def search_documents(query: str):
    """교육센터 자료실 안내 문서 열두 건에서 검색어와 가까운 문서 세 건을 찾습니다. query에는 찾을 내용을 짧은 검색어로 넣습니다."""
    hit_list = search_hits(embedding_model, query, doc_vectors, doc_ids, top_count)
    found_text = ""
    for hit in hit_list:
        doc_id = hit["doc_id"]
        found_text = found_text + "[" + doc_id + "] " + text_by_doc[doc_id] + "\n"
    return found_text


model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")


def ids_in(text):
    found = []
    for line in text.split("\n"):
        if line.startswith("["):
            found.append(line.split("]")[0][1:])
    return found


def usage_of(message):
    usage = message.usage_metadata
    return {"input": usage["input_tokens"], "output": usage["output_tokens"],
            "cache_read": usage.get("input_token_details", {}).get("cache_read")}


def run_fixed(case):
    found_text = search_documents.invoke({"query": case["question"]})
    COUNT["embed_search"] += 1
    prompt_text = ANSWER_HEAD + "질문: " + case["question"] + "\n\n자료:\n" + found_text
    reply = model.invoke(prompt_text)
    COUNT["model_answer"] += 1
    found = ids_in(found_text)
    return {"doc_ids": found, "gold_rank": find_gold_rank(found, [case["gold_doc_id"]]), "usage": usage_of(reply),
            "answer": reply.text, "context": found_text, "prompt_chars": len(prompt_text)}


def run_agent(agent, case):
    started = time.perf_counter()
    result = agent.invoke({"messages": [HumanMessage(content=case["question"])]})
    seconds = round(time.perf_counter() - started, 3)
    kinds, calls, usages, req_ids, msg_ids, tool_ids, context = [], [], [], [], [], [], ""
    for message in result["messages"]:
        kind = type(message).__name__
        kinds.append(kind)
        if kind == "AIMessage":
            calls.append([[c["name"], c["args"]] for c in message.tool_calls])
            for c in message.tool_calls:
                req_ids.append(c["id"])
            usages.append(usage_of(message))
        if kind == "ToolMessage":
            tool_ids.append(ids_in(message.content))
            msg_ids.append(message.tool_call_id)
            context = context + message.content
    COUNT["embed_search"] += len(tool_ids)
    COUNT["model_agent"] += kinds.count("AIMessage")
    flat = []
    for ids in tool_ids:
        flat = flat + ids
    last_ai = result["messages"][-1]
    return {"kinds": kinds, "calls": calls, "tool_doc_ids": tool_ids, "id_pair": req_ids == msg_ids,
            "model_calls": kinds.count("AIMessage"), "tool_calls": kinds.count("ToolMessage"), "usage": usages,
            "input_total": sum(u["input"] for u in usages), "output_total": sum(u["output"] for u in usages),
            "gold_rank": find_gold_rank(flat, [case["gold_doc_id"]]), "answer": last_ai.text, "context": context,
            "seconds": seconds, "model_name": last_ai.response_metadata.get("model_name")}


def judge(case_row):
    prompt_text = build_judge_prompt(JUDGE_HEAD, JUDGE_PAIR, case_row)
    COUNT["model_judge"] += 1
    try:
        verdict = judge_once(model, prompt_text)
    except Exception as error:  # 기록만
        return {"error": type(error).__name__ + ": " + str(error)[:200]}
    return {"score": verdict.get("score"), "reason": verdict.get("reason")}


def main():
    start, rounds, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    picked = ["C01", "C05", "C07"]
    if len(sys.argv) > 4:
        picked = sys.argv[4].split(",")
    cases = [q for q in queries if q["qid"] in picked]
    agent = create_agent(model, tools=[search_documents], system_prompt=SYSTEM_TEXT)
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(start, start + rounds):
            for case in cases:
                row = {"round": round_no, "qid": case["qid"], "gold": case["gold_doc_id"],
                       "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
                try:
                    row["fixed"] = run_fixed(case)
                    row["agent"] = run_agent(agent, case)
                    row["judge_fixed"] = judge({"response": row["fixed"]["answer"], "context": row["fixed"]["context"]})
                    row["judge_agent"] = judge({"response": row["agent"]["answer"], "context": row["agent"]["context"]})
                except Exception as error:  # 기록만 하고 다음으로
                    row["error"] = type(error).__name__ + ": " + str(error)[:300]
                row["count_so_far"] = dict(COUNT)
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                handle.flush()
                agent_part = row.get("agent", {})
                fixed_part = row.get("fixed", {})
                print(round_no, case["qid"], "| F", fixed_part.get("doc_ids"), fixed_part.get("gold_rank"),
                      fixed_part.get("usage"), "| A", agent_part.get("kinds"), agent_part.get("calls"),
                      agent_part.get("tool_doc_ids"), agent_part.get("gold_rank"), agent_part.get("input_total"),
                      agent_part.get("output_total"), agent_part.get("id_pair"),
                      "| J", row.get("judge_fixed", {}).get("score"), row.get("judge_agent", {}).get("score"),
                      row.get("error", ""))
    print("count", COUNT)


if __name__ == "__main__":
    main()
