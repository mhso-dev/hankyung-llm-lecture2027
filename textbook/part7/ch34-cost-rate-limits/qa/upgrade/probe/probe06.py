"""Ch 34 06절 흔들림 확인(노트북 밖). 사용: python probe06.py <회차> <기록 파일>
생성기 author_06.py의 코드 셀(설치 셀 뺌)을 노트북과 같은 차례로 한 프로세스에서 실행합니다.
실행 1(기준 길이 30) 요청 셋 → 실행 2(기준 길이 0) 요청 둘 = 요청 다섯. 키는 루트 .env에서 키 셀이 읽고, 값은 출력·기록하지 않습니다.
오류가 나면 기록만 하고 다시 보내지 않습니다(SDK 기본 다시 보내기는 노트북과 같게 켜 둠).
"""
import contextlib, datetime, importlib.util, io, json, os, sys, traceback
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path.home() / "mnt/한국경제신문"
round_no = int(sys.argv[1]); out = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("author_06", ROOT / "textbook/part7/ch34-cost-rate-limits/qa/upgrade/author_06.py")
gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
sys.path.insert(0, "/tmp/ch34-06/probe/tools")
os.chdir(ROOT)
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
row = {"round": round_no, "start": now(), "cells": [], "error": None}
space = {}
names = {id(v): k for k, v in vars(gen).items() if isinstance(v, str) and v in gen.CODE_CELLS}
for text in gen.CODE_CELLS:
    if text == gen.INSTALL:
        continue
    label = names.get(id(text), "?")
    buf = io.StringIO()
    started = now()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(text, "<cell>", "exec"), space)
    except Exception as error:
        row["error"] = {"cell": label, "type": type(error).__name__, "message": str(error)[:300]}
        row["cells"].append({"cell": label, "started": started, "out": buf.getvalue()})
        break
    row["cells"].append({"cell": label, "started": started, "out": buf.getvalue()})
def resp_info(run, prices_key):
    items = []
    responses = space.get(run + "_responses", [])
    sent = space.get(run + "_sent", [])
    models = space.get(run + "_models", [])
    for index in range(len(responses)):
        resp = responses[index]; number = sent[index]
        usage = resp.usage_metadata
        details = usage.get("input_token_details", {})
        prices = space["price_tables"][models[number]]
        with_d = gen_estimate(usage, prices, False); without_d = gen_estimate(usage, prices, True)
        answered = resp.response_metadata.get("model_name")
        items.append({"conv": number + 1, "chosen": models[number], "answered": answered,
                      "answered_starts": (answered or "").startswith(models[number]),
                      "answer": resp.text, "match": resp.text == space["expected_types"][number],
                      "input": usage["input_tokens"], "output": usage["output_tokens"],
                      "cache_read": details.get("cache_read"), "detail_keys": sorted(details),
                      "cache_mult128": (details.get("cache_read") or 0) % 128 == 0,
                      "finish": resp.response_metadata.get("finish_reason"),
                      "cost": round(with_d, 6), "cost_nodisc": round(without_d, 6),
                      "cost_lt_1e4": with_d < 0.0001,
                      "amount": space["amounts"][models[number]], "cost_lt_amount": with_d < space["amounts"][models[number]]})
    return items
def gen_estimate(usage, prices, nodisc):
    import cost_tools
    cached = prices["ordinary_input"] if nodisc else prices["cached_input"]
    return cost_tools.estimate_cost(usage, prices["ordinary_input"], cached, prices["output"])
if row["error"] is None or space.get("run1_responses"):
    for run in ("run1", "run2"):
        if run + "_models" in space:
            b = space.get(run + "_budget", {})
            row[run] = {"models": space[run + "_models"], "results": space.get(run + "_results"),
                        "reserved": round(b.get("cost_usd", 0), 6), "calls": b.get("calls"),
                        "sent": space.get(run + "_sent"), "requests": len(space.get(run + "_responses", [])),
                        "items": resp_info(run, None),
                        "total": round(sum(space.get(run + "_costs", [])), 6) if space.get(run + "_costs") else None,
                        "matched": space.get(run + "_matched")}
    if space.get("run2_costs") and space.get("run1_costs"):
        cmpv = []
        for index in range(len(space["run2_sent"])):
            number = space["run2_sent"][index]
            c1 = space["run1_costs"][space["run1_sent"].index(number)]
            cmpv.append({"conv": number + 1, "run1_lt_run2": c1 < space["run2_costs"][index]})
        row["same_conv"] = cmpv
        row["reserved_gt_total"] = [space["run1_budget"]["cost_usd"] > sum(space["run1_costs"]), space["run2_budget"]["cost_usd"] > sum(space["run2_costs"])]
row["end"] = now()
with out.open("a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
short = {k: row.get(k) for k in ("round", "error")}
for run in ("run1", "run2"):
    if run in row:
        short[run] = [(i["conv"], i["answered"], i["answer"], i["input"], i["cache_read"], i["output"], i["cost"]) for i in row[run]["items"]]
print(json.dumps(short, ensure_ascii=False))
