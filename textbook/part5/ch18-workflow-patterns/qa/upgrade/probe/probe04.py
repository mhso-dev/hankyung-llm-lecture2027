"""Ch 18 04절 흔들림 확인(노트북 밖). 키 값은 .env에서만 읽고 출력하지 않는다.
사용: python probe04.py flow <과제 이름 A|B1|B2> <횟수>
  한 회차 = 계획 요청 1 → 작업 목록 거르기 → 작업 요청 여럿을 함께(ask_all_together) → 종합 요청 1 → 종합 답 검사(정규식 둘).
도구 파일 workflow_tools.py(01·03절 판)의 ask_json·ask_all_together·join_parts를 그대로 가져온다(PYTHONPATH=notebooks).
지시 글·머리글·공통 사실은 노트북 04절과 글자까지 같게 둔다(노트북 쓰기 전 설계 판)."""
import asyncio, json, os, re, sys
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/mnt/한국경제신문/.env"))
from openai import OpenAI
from workflow_tools import ask_all_together, ask_json, join_parts

client = OpenAI()

FACT = ("2026년 10월 15일부터 전 직원 계정에 2단계 인증을 적용합니다. "
        "비밀번호만으로는 계정을 지키기 어렵기 때문입니다. "
        "등록은 사내 포털의 보안 메뉴에서 인증 앱을 연결하면 됩니다. "
        "문의는 help@company.test로 받습니다.")
TASKS = {
    "A": "전 직원에게 2단계 인증 적용을 알리는 사내 안내문을 쓰세요. 적용 까닭과 등록 방법, 문의처를 담습니다.",
    "B1": "2단계 인증 등록 방법만 짧게 알리는 안내문을 쓰세요.",
    "B2": "신입 직원이 처음 읽을 2단계 인증 안내문을 쓰세요. 적용 날짜, 까닭, 등록 방법, 문의처를 따로따로 담습니다.",
}
PLAN_INSTR = ("사내 안내문 과제를 작업으로 나누는 계획 모델입니다. "
              "과제와 공통 사실을 읽고, 서로의 글을 기다리지 않고 따로 쓸 수 있는 작업으로 나눕니다. "
              "작업은 2개 이상 4개 이하로 정합니다. "
              '답은 JSON 객체 하나로만 출력합니다: {"작업": [{"이름": "짧은 작업 이름", "맡을 일": "한 문장"}]}')
PLAN_HEAD = "아래 과제를 작업으로 나눠 JSON으로 답하세요.\n과제: "
TASK_INSTR = ("사내 안내문의 작업 하나를 맡아 쓰는 작성자입니다. "
              "공통 사실 가운데 맡은 일에 맞는 것만 골라 한국어 두 문장으로 씁니다. "
              "공통 사실에 없는 날짜·연락처·절차는 지어내지 않습니다. "
              '답은 JSON 객체 하나로만 출력합니다: {"작업": "맡을 작업 이름 그대로", "글": "글"}')
TASK_HEAD = "아래 공통 사실로 맡은 작업의 글을 JSON으로 쓰세요.\n공통 사실: "
SUM_INSTR = ("작업 답들을 엮어 사내 안내문 하나로 만드는 편집자입니다. "
             "겹치는 내용은 한 번만 남기고, 한국어 한 단락으로 씁니다. "
             "공통 사실에 없는 날짜·연락처·번호는 쓰지 않습니다. "
             '답은 JSON 객체 하나로만 출력합니다: {"안내문": "글"}')
SUM_HEAD = "아래 공통 사실과 작업 답을 엮어 안내문 하나를 JSON으로 쓰세요.\n공통 사실: "
ADDRESS = r"[a-z]+@[a-z]+\.[a-z]+"
NUMBER = r"\d+"

def build_plan_request(plan_head, task_text, fact):
    return plan_head + task_text + "\n공통 사실: " + fact

def pick_tasks(plan, max_tasks):
    tasks = []
    for task in plan["작업"]:
        if "이름" in task and "맡을 일" in task:
            tasks.append(task)
    return tasks[:max_tasks]

def build_task_request(task_head, fact, task):
    task_lines = "\n맡을 작업: " + task["이름"] + "\n맡을 일: " + task["맡을 일"]
    return task_head + fact + task_lines

def build_task_requests(instructions_text, task_head, fact, tasks):
    requests = []
    for task in tasks:
        request_text = build_task_request(task_head, fact, task)
        requests.append({"단계": task["이름"], "지시 글": instructions_text, "요청 글": request_text})
    return requests

def build_summary_request(summary_head, fact, answers):
    return summary_head + fact + "\n작업 답:\n" + join_parts(answers)

def find_new_contacts(notice, fact, patterns):
    new_items = []
    for pattern in patterns:
        fact_items = re.findall(pattern, fact)
        for item in re.findall(pattern, notice):
            if item not in fact_items:
                new_items.append(item)
    return new_items

async def one_flow(task_text):
    records = []
    plan = ask_json(client, records, "계획", PLAN_INSTR, build_plan_request(PLAN_HEAD, task_text, FACT))
    raw_count = len(plan["작업"]) if isinstance(plan.get("작업"), list) else -1
    tasks = pick_tasks(plan, 4)
    if len(tasks) < 2:
        return {"plan": plan, "raw": raw_count, "tasks": tasks, "stop": True, "records": records}
    reqs = build_task_requests(TASK_INSTR, TASK_HEAD, FACT, tasks)
    answers = await ask_all_together(client, records, reqs)
    sreq = build_summary_request(SUM_HEAD, FACT, answers)
    summary = ask_json(client, records, "종합", SUM_INSTR, sreq)
    return {"plan": plan, "raw": raw_count, "tasks": tasks, "answers": answers, "notice": summary["안내문"],
            "records": records, "stop": False}

def main():
    mode, name, times = sys.argv[1], sys.argv[2], int(sys.argv[3])
    task_text = TASKS[name]
    tot_in = tot_out = 0
    for t in range(times):
        r = asyncio.run(one_flow(task_text))
        recs = r["records"]
        for row in recs:
            tot_in += row["입력 토큰"]; tot_out += row["출력 토큰"]
        names = [x["이름"] for x in r["tasks"]]
        print("=== run", t + 1, "| task", name, "| plan keys", list(r["plan"].keys()), "| raw count", r["raw"],
              "| picked", len(r["tasks"]), "| stop", r["stop"])
        for x in r["tasks"]:
            print("   task:", x["이름"], "|", x["맡을 일"])
        if r["stop"]:
            continue
        ans_names = [a.get("작업") for a in r["answers"]]
        print("   answer 작업 == names:", ans_names == names, ans_names)
        print("   answer keys:", [sorted(a.keys()) for a in r["answers"]])
        print("   records:", [(row["단계"], row["입력 토큰"], row["출력 토큰"]) for row in recs])
        print("   requests:", len(recs), "== 1+n+1:", len(recs) == 1 + len(r["tasks"]) + 1)
        print("   worker new contacts:", [find_new_contacts(a["글"], FACT, [ADDRESS, NUMBER]) for a in r["answers"]])
        print("   notice:", r["notice"])
        print("   notice new contacts:", find_new_contacts(r["notice"], FACT, [ADDRESS, NUMBER]))
        print("   notice has help@company.test:", "help@company.test" in r["notice"], "| len", len(r["notice"]))
    print("TOTAL tokens in", tot_in, "out", tot_out)

main()
