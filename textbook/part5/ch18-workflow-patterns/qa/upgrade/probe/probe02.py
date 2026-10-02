"""Ch 18 02절 흔들림 확인(노트북 밖). 키 값은 .env에서만 읽고 출력하지 않는다.
사용: python probe02.py <single|mixed|vague|pair> <횟수> [지시글 판]"""
import json, os, sys
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/mnt/한국경제신문/.env"))
from openai import OpenAI
client = OpenAI()
CLASSIFY = ("고객 문의를 종류 하나로 가르는 분류 담당입니다. "
            "종류는 결제, 계정, 기술 가운데 하나로 적습니다. "
            "하나로 정할 수 없으면 종류를 모름으로 적습니다. "
            "신뢰도에는 그 종류가 맞다고 보는 정도를 0과 1 사이 수로 적습니다. "
            '답은 JSON 객체 하나로만 출력합니다: {"종류": "글", "신뢰도": 수}')
TAIL = ' 한국어 두 문장으로 답하고, 답은 JSON 객체 하나로만 출력합니다: {"답": "글"}'
HEADS = {"결제": "결제 문의를 맡은 상담원입니다." + TAIL,
         "계정": "계정 문의를 맡은 상담원입니다." + TAIL,
         "기술": "기술 문의를 맡은 상담원입니다." + TAIL}
Q = {"single": "카드에서 같은 요금이 두 번 결제됐어요.",
     "mixed": "로그인도 안 되고 카드 청구도 이상해요.",
     "vague": "앱에서 결제 버튼을 누르면 화면이 멈춰요.",
     "outside": "주문한 물건이 아직 안 왔어요."}
# 첫 시도(요청 글에 JSON이라는 말이 없음)는 서비스가 400으로 막았다 → 요청 머리글에 JSON을 적는다
HEAD = "아래 고객 문의에 JSON으로 답하세요.\n문의: "
def ask(instr, req):
    r = client.responses.create(model="gpt-5.4-mini", temperature=0, reasoning={"effort": "none"},
        instructions=instr, input=req, text={"format": {"type": "json_object"}})
    return r
which = sys.argv[1]; n = int(sys.argv[2])
for i in range(n):
    key = which
    if which == "pair":
        key = "single"
    if which == "outpair":
        key = "outside"
    r1 = ask(CLASSIFY, HEAD + Q[key])
    d = json.loads(r1.output_text)
    line = [i + 1, "|", key, "|", r1.output_text, "|", "keys", list(d.keys()), "| type conf", type(d.get("신뢰도")).__name__, "| tok", r1.usage.input_tokens, r1.usage.output_tokens, "| model", r1.model, r1.temperature, r1.reasoning.effort]
    print(*line)
    if which == "pair" or which == "outpair":
        kind = d["종류"]
        r2 = ask(HEADS[kind], HEAD + Q[key])
        out = json.loads(r2.output_text)
        print("    answer keys", list(out.keys()), "| tok", r2.usage.input_tokens, r2.usage.output_tokens, "|", str(out.get("답"))[:200])
