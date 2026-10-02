"""Ch 21 05절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe05.py <설정 S5|SP> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  S5 : Ch 14 queries.json C05 「토요일 자료실 폐관 시각은?」
  SP : 「자료실 주차 요금은 얼마인가요?」 (값 바꿔 보기 — 질문 하나)
자료·검색 함수·도구·시스템 메시지 글은 05절 노트북과 같은 코드(05-probe.md §0-2).
검색 함수는 Ch 14 도구 파일 rag_tools.py를 가져오기만 한다(바이트 코드를 쓰지 않음, 파일은 고치지 않음).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[6]
CH14 = ROOT / "labs/part4/ch14-rag-patterns"
sys.path.insert(0, str(CH14 / "notebooks"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from langchain.agents import create_agent  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402
from langchain_openai import OpenAIEmbeddings  # noqa: E402
from rag_tools import search_hits  # noqa: E402

SYSTEM_TEXT = ("교육센터 자료실 안내 도우미입니다. 자료실 이용을 묻는 질문에는 search_documents 도구로 찾은 문서 글에 근거해 답하세요. "
               "찾은 문서에 답이 없으면 검색어를 바꿔 한 번만 더 검색하고, 그래도 없으면 문서에서 찾지 못했다고 답하세요.")
PARKING = "자료실 주차 요금은 얼마인가요?"

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
EMBED = {"doc": 1, "direct": 0, "tool": 0, "recheck": 0}


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


def summarize(result):
    kinds, calls, tools_out, usages, req_ids, msg_ids = [], [], [], [], [], []
    all_calls = []
    for message in result["messages"]:
        kind = type(message).__name__
        kinds.append(kind)
        if kind == "AIMessage":
            calls.append([[c["name"], c["args"]] for c in message.tool_calls])
            for c in message.tool_calls:
                req_ids.append(c["id"])
                all_calls.append(c)
            usage = message.usage_metadata
            usages.append({"input": usage["input_tokens"], "output": usage["output_tokens"],
                           "cache_read": usage.get("input_token_details", {}).get("cache_read")})
        if kind == "ToolMessage":
            tools_out.append({"status": message.status, "ids": ids_in(message.content), "content": message.content,
                              "tool_call_id": message.tool_call_id})
            msg_ids.append(message.tool_call_id)
    EMBED["tool"] += len(tools_out)
    # 같은 검색어 다시 부르기(Ch 19 05절 모양) — 요청마다 임베딩 1번
    rechecks = []
    by_id = {t["tool_call_id"]: t for t in tools_out}
    for c in all_calls:
        again = search_documents.invoke(c)
        EMBED["recheck"] += 1
        rechecks.append(again.content == by_id[c["id"]]["content"])
    last_ai = [m for m in result["messages"] if type(m).__name__ == "AIMessage"][-1]
    return {"kinds": kinds, "calls": calls, "tool_messages": [{k: t[k] for k in ("status", "ids")} for t in tools_out],
            "id_pair": req_ids == msg_ids, "n_ai": kinds.count("AIMessage"), "n_tool": kinds.count("ToolMessage"),
            "recheck_same": rechecks, "usage": usages, "last_ai_content": last_ai.content,
            "model_name": last_ai.response_metadata.get("model_name")}


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    question = PARKING
    if mode == "S5":
        for query in queries:
            if query["qid"] == "C05":
                question = query["question"]
    direct = search_hits(embedding_model, question, doc_vectors, doc_ids, top_count)
    EMBED["direct"] += 1
    agent = create_agent(model, tools=[search_documents], system_prompt=SYSTEM_TEXT)
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "question": question, "direct": direct,
                   "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            try:
                result = agent.invoke({"messages": [HumanMessage(content=question)]})
                row.update(summarize(result))
            except Exception as error:  # 기록만 하고 다음 회차로
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            row["embed_so_far"] = dict(EMBED)
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(mode, round_no, row.get("kinds"), row.get("calls"), [t["ids"] for t in row.get("tool_messages", [])],
                  row.get("id_pair"), row.get("recheck_same"), row.get("usage"), row.get("error", ""))
    print("direct", direct, "embed", EMBED)


if __name__ == "__main__":
    main()
