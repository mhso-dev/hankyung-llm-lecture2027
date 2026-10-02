"""Ch 34 01절 흔들림 확인(노트북 밖). 사용: python probe01.py <회차> <기록 파일>
노트북과 같은 글·같은 모델 설정·같은 차례(A 뒤에 Q1 → B 뒤에 Q2 → C 앞에 Q1 → D 앞에 Q2)로 요청 넷을 보냅니다.
키는 루트 .env에서만 읽고 출력하지 않습니다. 실험 번호(uuid4)는 기록하지 않습니다(글자 수만).
"""
import datetime, json, sys, uuid
from pathlib import Path
from dotenv import load_dotenv
ROOT = Path.home() / "mnt/한국경제신문"
load_dotenv(ROOT / ".env")
from langchain.chat_models import init_chat_model

round_no = int(sys.argv[1]); out = Path(sys.argv[2])
rule_sentence = "고객 문의에 답할 때는 확인한 주문 정보만 근거로 삼고, 확인하지 못한 내용은 확인하지 못했다고 적습니다. "
repeat_count = 100
policy_text = ""
for number in range(repeat_count):
    policy_text = policy_text + rule_sentence
inquiries = [
    "주문한 책이 일주일째 오지 않습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "받은 책이 찢어져 있어 돈을 되찾고 싶습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
]
experiment_mark = "실험 번호 " + uuid.uuid4().hex

def make_request(mark, first_text, second_text):
    return mark + "\n" + first_text + "\n" + second_text

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
plan = [("A", "뒤에", policy_text, inquiries[0]), ("B", "뒤에", policy_text, inquiries[1]),
        ("C", "앞에", inquiries[0], policy_text), ("D", "앞에", inquiries[1], policy_text)]
row = {"round": round_no, "start": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
       "policy_chars": len(policy_text), "mark_chars": len(experiment_mark), "requests": []}
for label, place, first, second in plan:
    text = make_request(experiment_mark, first, second)
    item = {"label": label, "place": place, "request_chars": len(text)}
    try:
        resp = model.invoke(text)
        usage = resp.usage_metadata
        raw = resp.response_metadata.get("token_usage") or {}
        item.update({
            "input": usage["input_tokens"], "output": usage["output_tokens"],
            "details": usage.get("input_token_details"), "out_details": usage.get("output_token_details"),
            "cache_read": usage["input_token_details"].get("cache_read"),
            "has_cache_creation": "cache_creation" in usage["input_token_details"],
            "raw_prompt_details": raw.get("prompt_tokens_details"),
            "model_name": resp.response_metadata.get("model_name"),
            "finish": resp.response_metadata.get("finish_reason"),
            "answer": resp.text,
        })
        cr = item["cache_read"]
        item["mult128"] = (cr % 128 == 0) if isinstance(cr, int) else None
        item["le_input"] = (cr <= item["input"]) if isinstance(cr, int) else None
    except Exception as error:  # 기록만 하고 다시 보내지 않음
        item["error"] = type(error).__name__ + ": " + str(error)[:200]
    row["requests"].append(item)
row["end"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
with out.open("a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("round", round_no, "done", [(r["label"], r.get("input"), r.get("cache_read"), r.get("error")) for r in row["requests"]])
