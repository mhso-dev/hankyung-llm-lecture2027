"""Ch 18 03절 흔들림·스레드 확인(노트북 밖). 키 값은 .env에서만 읽고 출력하지 않는다.
사용: python probe03.py threads <동시 수> <회차>   — 클라이언트 하나를 여러 스레드가 함께 쓰는지
      python probe03.py section <횟수>             — 하나씩 세 번 vs 함께 세 번: 받은 차례·기록 도착 차례·걸린 초
      python probe03.py vote <횟수> [판]            — 평가자 셋 투표 원표
ask_json은 도구 파일 workflow_tools.py(01절 판)를 그대로 가져온다(PYTHONPATH=notebooks)."""
import asyncio, json, os, sys, threading, time
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/mnt/한국경제신문/.env"))
from openai import OpenAI
from workflow_tools import ask_json

client = OpenAI()

FACT = ("2026년 10월 15일부터 전 직원 계정에 2단계 인증을 적용합니다. "
        "비밀번호만으로는 계정을 지키기 어렵기 때문입니다. "
        "등록은 사내 포털의 보안 메뉴에서 인증 앱을 연결하면 됩니다. "
        "문의는 help@company.test로 받습니다.")
WRITE = ("사내 안내문의 한 부분을 쓰는 작성자입니다. "
         "공통 사실 가운데 쓸 부분에 맞는 것만 골라 한국어 두 문장으로 씁니다. "
         "공통 사실에 없는 날짜·연락처·절차는 지어내지 않습니다. "
         '답은 JSON 객체 하나로만 출력합니다: {"부분": "쓸 부분 이름 그대로", "글": "글"}')
HEAD = "아래 공통 사실로 안내문의 한 부분을 JSON으로 쓰세요.\n공통 사실: "
PARTS = [("목적", "적용 날짜와 까닭"), ("절차", "직원이 할 일"), ("문의", "물어볼 곳")]

def part_request(name, content):
    return HEAD + FACT + "\n쓸 부분: " + name + "\n담을 내용: " + content

CAND_A = ("2026년 10월 15일부터 전 직원 계정에 2단계 인증을 적용합니다. "
          "비밀번호만으로는 계정을 지키기 어렵기 때문입니다. "
          "그 전에 사내 포털의 보안 메뉴에서 인증 앱을 연결해 주세요. "
          "궁금한 점은 help@company.test로 보내 주세요.")
CAND_B = "10월 15일부터 2단계 인증이 켜집니다. 사내 포털 보안 메뉴에서 인증 앱을 지금 연결하세요."
VOTE_TAIL = '더 나은 글 하나를 A 또는 B로 고릅니다. 답은 JSON 객체 하나로만 출력합니다: {"표": "A 또는 B"}'
JUDGES = [
    ("인사 담당", "인사 담당자 입장에서 사내 안내문 두 편을 견주는 평가자입니다. 전 직원이 알아야 할 사실(날짜·대상·문의처)이 빠짐없이 들어간 글을 더 낫다고 봅니다. " + VOTE_TAIL),
    ("보안 담당", "보안 담당자 입장에서 사내 안내문 두 편을 견주는 평가자입니다. 직원이 해야 할 행동과 기한이 분명한 글을 더 낫다고 봅니다. " + VOTE_TAIL),
    ("신입 직원", "신입 직원 입장에서 사내 안내문 두 편을 견주는 평가자입니다. 처음 읽는 사람이 빨리 이해할 수 있는 짧은 글을 더 낫다고 봅니다. " + VOTE_TAIL),
]
VOTE_HEAD = "아래 두 안내문 가운데 더 나은 글 하나를 골라 JSON으로 답하세요.\n"

def vote_request(a, b):
    return VOTE_HEAD + "A: " + a + "\nB: " + b

async def gather_list(jobs):
    return await asyncio.gather(*jobs)

def mode_threads(n, rounds):
    instr = '받은 번호를 그대로 적습니다. 답은 JSON 객체 하나로만 출력합니다: {"번호": 수}'
    def one(k, bag):
        r = client.responses.create(model="gpt-5.4-mini", temperature=0, reasoning={"effort": "none"},
            instructions=instr, input="JSON으로 답하세요. 받은 번호: " + str(k), text={"format": {"type": "json_object"}})
        bag.append((k, threading.current_thread().name, r.id, json.loads(r.output_text).get("번호"), r.usage.input_tokens, r.status))
        return k
    for rd in range(rounds):
        bag = []
        t0 = time.perf_counter()
        out = asyncio.run(gather_list([asyncio.to_thread(one, k, bag) for k in range(1, n + 1)]))
        wall = time.perf_counter() - t0
        ok_order = out == list(range(1, n + 1))
        match = all(k == num for k, _, _, num, _, _ in bag)
        ids = len(set(x[2] for x in bag))
        threads = sorted(set(x[1] for x in bag))
        arrival = [x[0] for x in bag]
        print("round", rd + 1, "| n", n, "| done", len(bag), "| status", sorted(set(x[5] for x in bag)),
              "| gather order == input", ok_order, "| echo matches", match, "| unique ids", ids,
              "| threads", len(threads), threads[:3], "| arrival", arrival, "| wall", round(wall, 3))

def mode_section(times):
    for t in range(times):
        # 하나씩
        seq_records = []
        t0 = time.perf_counter()
        seq = [ask_json(client, seq_records, name, WRITE, part_request(name, c)) for name, c in PARTS]
        seq_s = time.perf_counter() - t0
        # 함께(기록 목록 하나를 함께 씀 → 도착 차례)
        shared = []
        jobs = [asyncio.to_thread(ask_json, client, shared, name, WRITE, part_request(name, c)) for name, c in PARTS]
        t1 = time.perf_counter()
        tog = asyncio.run(gather_list(jobs))
        tog_s = time.perf_counter() - t1
        print(t + 1, "| seq parts", [x.get("부분") for x in seq], "| together parts", [x.get("부분") for x in tog],
              "| record arrival", [r["단계"] for r in shared],
              "| in tok seq", [r["입력 토큰"] for r in seq_records], "| in tok tog", [r["입력 토큰"] for r in shared],
              "| out tok tog", [r["출력 토큰"] for r in shared],
              "| seq s", round(seq_s, 3), "| together s", round(tog_s, 3), "| together shorter", tog_s < seq_s,
              "| keys", sorted(set(k for x in tog for k in x.keys())))
        if t == 0:
            for x in tog:
                print("    ", json.dumps(x, ensure_ascii=False))

def mode_vote(times):
    req = vote_request(CAND_A, CAND_B)
    for t in range(times):
        recs = []
        jobs = [asyncio.to_thread(ask_json, client, recs, name, instr, req) for name, instr in JUDGES]
        votes = asyncio.run(gather_list(jobs))
        print(t + 1, "| votes", [v.get("표") for v in votes], "| raw", json.dumps(votes, ensure_ascii=False),
              "| in tok", [(r["단계"], r["입력 토큰"], r["출력 토큰"]) for r in recs])

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "threads":
        mode_threads(int(sys.argv[2]), int(sys.argv[3]))
    elif m == "section":
        mode_section(int(sys.argv[2]))
    elif m == "vote":
        mode_vote(int(sys.argv[2]))
