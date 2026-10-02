"""Ch 34 03절 흔들림 확인(노트북 밖). 사용: python probe03.py <회차> <기록 파일>
노트북과 같은 문의 글 셋·답 형식 글·모델 라우터(choose_model)·보내는 함수(send_inquiry)·모델 설정으로,
실행 1(기준 길이 30) 요청 셋 → 실행 2(기준 길이 0) 요청 셋을 차례대로 보냅니다(요청 6번).
키는 루트 .env에서만 읽고 출력하지 않습니다. 오류가 나면 기록만 하고 다시 보내지 않습니다.
"""
import datetime, json, sys
from pathlib import Path
from dotenv import load_dotenv
ROOT = Path.home() / "mnt/한국경제신문"
load_dotenv(ROOT / ".env")
from langchain.chat_models import init_chat_model
from cost_tools import estimate_cost

round_no = int(sys.argv[1]); out = Path(sys.argv[2])
nano_model = init_chat_model("openai:gpt-5.4-nano", temperature=0, reasoning_effort="none")
mini_model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
inquiries = [
    "주문한 책이 일주일째 오지 않습니다.",
    "받은 책이 찢어져 있어 돈을 되찾고 싶습니다.",
    "결제 창에서 카드 번호를 넣었는데 다음 단계로 넘어가지 않습니다.",
]
expected_types = ["배송", "환불", "결제"]
answer_rule = "이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요."

def choose_model(inquiry, length_limit):
    model_name = "gpt-5.4-nano"
    if len(inquiry) > length_limit:
        model_name = "gpt-5.4-mini"
    return model_name

models = {"gpt-5.4-nano": nano_model, "gpt-5.4-mini": mini_model}
nano_prices = {"ordinary_input": 0.20, "cached_input": 0.02, "output": 1.25}
mini_prices = {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}
price_tables = {"gpt-5.4-nano": nano_prices, "gpt-5.4-mini": mini_prices}

def send_inquiry(inquiry, model_name, models, answer_rule):
    chosen_model = models[model_name]
    request_text = inquiry + " " + answer_rule
    response = chosen_model.invoke(request_text)
    return response

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

row = {"round": round_no, "start": now(), "runs": {}}
usages = {}
for run, limit in (("run1", 30), ("run2", 0)):
    names = [choose_model(q, limit) for q in inquiries]
    items = []
    total = 0.0
    for number, inquiry in enumerate(inquiries):
        item = {"number": number + 1, "chosen": names[number], "inquiry_chars": len(inquiry),
                "request_chars": len(inquiry + " " + answer_rule), "sent_at": now()}
        try:
            resp = send_inquiry(inquiry, names[number], models, answer_rule)
            usage = resp.usage_metadata
            prices = price_tables[names[number]]
            cost = estimate_cost(usage, prices["ordinary_input"], prices["cached_input"], prices["output"])
            item.update({
                "answered": resp.response_metadata.get("model_name"),
                "contains": names[number] in (resp.response_metadata.get("model_name") or ""),
                "answer": resp.text, "match": resp.text == expected_types[number],
                "input": usage["input_tokens"], "output": usage["output_tokens"],
                "details": usage.get("input_token_details"), "out_details": usage.get("output_token_details"),
                "finish": resp.response_metadata.get("finish_reason"),
                "cost": cost, "cost_1000": round(cost * 1000, 6),
            })
            total += cost * 1000
            usages[(run, number)] = usage
        except Exception as error:
            item["error"] = type(error).__name__ + ": " + str(error)[:300]
        items.append(item)
    row["runs"][run] = {"limit": limit, "names": names, "nano_count": names.count("gpt-5.4-nano"),
                        "mini_count": names.count("gpt-5.4-mini"), "items": items, "total_1000": round(total, 6)}
r1 = row["runs"]["run1"]; r2 = row["runs"]["run2"]
cmp = {"run1_lt_run2": r1["total_1000"] < r2["total_1000"],
       "model_changed": [a != b for a, b in zip(r1["names"], r2["names"])],
       "same_answer": [x.get("answer") == y.get("answer") for x, y in zip(r1["items"], r2["items"])],
       "same_input": [x.get("input") == y.get("input") for x, y in zip(r1["items"], r2["items"])]}
if ("run1", 0) in usages:
    u = usages[("run1", 0)]
    nc = estimate_cost(u, nano_prices["ordinary_input"], nano_prices["cached_input"], nano_prices["output"])
    mc = estimate_cost(u, mini_prices["ordinary_input"], mini_prices["cached_input"], mini_prices["output"])
    cmp.update({"same_usage_nano_1000": round(nc * 1000, 6), "same_usage_mini_1000": round(mc * 1000, 6), "nano_lt_mini": nc < mc})
row["compare"] = cmp
row["end"] = now()
with out.open("a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("round", round_no, "done", r1["names"], r2["names"],
      [(i.get("answer"), i.get("input"), i.get("output"), i.get("error", "")[:60]) for i in r1["items"] + r2["items"]])
