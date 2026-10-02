import json, os, sys
from dotenv import load_dotenv, find_dotenv
load_dotenv(os.path.expanduser("~/mnt/한국경제신문/.env"))
from openai import OpenAI
client = OpenAI()
INSTR = "고객 지원 안내문을 만드는 작성자입니다. 한국어로 쓰고, 답은 JSON 객체 하나로만 출력합니다."
LOOSE = "비밀번호 재설정 안내문을 쓰기 전에 기획을 JSON으로 적어 주세요."
FULL = ("비밀번호 재설정 안내문을 쓰기 전에 기획을 적어 주세요.\n"
        "「단계」에는 고객이 따라 할 재설정 절차를 셋 이상 적습니다.\n"
        'JSON만 출력하세요: {"제목": "글", "독자": "글", "단계": ["글", "글", "글"]}')
def ask(req):
    r = client.responses.create(model="gpt-5.4-mini", temperature=0, reasoning={"effort": "none"},
        instructions=INSTR, input=req, text={"format": {"type": "json_object"}})
    return r
mode = sys.argv[1]
if mode == "t0":
    r = ask(FULL)
    print("model:", r.model, "| temperature:", r.temperature, "| reasoning:", r.reasoning, "| status:", r.status)
    print(r.output_text); print("usage:", r.usage.input_tokens, r.usage.output_tokens)
else:
    req = LOOSE if mode == "loose" else FULL
    n = int(sys.argv[2])
    for i in range(n):
        r = ask(req)
        d = json.loads(r.output_text)
        steps = d.get("단계")
        print(i+1, "| keys:", list(d.keys()), "| 단계 수:", (len(steps) if isinstance(steps, list) else None), "| in/out:", r.usage.input_tokens, r.usage.output_tokens)
        print("   ", r.output_text.replace("\n"," ")[:400])
