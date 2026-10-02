import json, os, sys
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/mnt/한국경제신문/.env"))
from openai import OpenAI
client = OpenAI()
INSTR = "고객 지원 안내문을 만드는 작성자입니다. 한국어로 쓰고, 답은 JSON 객체 하나로만 출력합니다."
LOOSE = "비밀번호 재설정 안내문을 쓰기 전에 기획을 JSON으로 적어 주세요."
FULL = ("비밀번호 재설정 안내문을 쓰기 전에 기획을 적어 주세요.\n"
        "「단계」에는 고객이 따라 할 재설정 절차를 셋 이상 적습니다.\n"
        'JSON만 출력하세요: {"제목": "글", "독자": "글", "단계": ["글", "글", "글"]}')
WRITE = ("아래 기획대로 고객에게 보낼 안내문을 네 문장으로 쓰세요.\n"
         'JSON만 출력하세요: {"안내문": "글"}')
def ask(req):
    r = client.responses.create(model="gpt-5.4-mini", temperature=0, reasoning={"effort": "none"},
        instructions=INSTR, input=req, text={"format": {"type": "json_object"}})
    return r
def check(plan):
    probs=[]
    for k in ["제목","독자","단계"]:
        if k not in plan: probs.append(k+" 칸 없음")
    if "단계" in plan and len(plan["단계"])<3: probs.append("단계 셋 미만")
    return probs
which = sys.argv[1]; n=int(sys.argv[2])
for i in range(n):
    r1 = ask(LOOSE if which=="loose" else FULL)
    plan = json.loads(r1.output_text)
    wr = WRITE + "\n\n기획:\n" + json.dumps(plan, ensure_ascii=False)
    r2 = ask(wr)
    out = json.loads(r2.output_text)
    print(i+1, "| problems:", check(plan), "| plan keys:", len(plan), "| write keys:", list(out.keys()), "| tok:", r1.usage.input_tokens, r1.usage.output_tokens, r2.usage.input_tokens, r2.usage.output_tokens)
    print("   ", str(out.get("안내문"))[:300])
