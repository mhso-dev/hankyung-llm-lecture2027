"""Ch 18 05절 흔들림 확인(노트북 밖). 키 값은 .env에서만 읽고 출력하지 않는다.
사용: python probe05.py loop <과제 이름 A|B1|B2> <횟수>
  한 회차 = 쓰고 평가하기 반복 한 흐름(바퀴 한도 3): 바퀴마다 쓰기 요청 1 → 평가 요청 1 → 코드 검사 → 정지 판정.
도구 파일 workflow_tools.py(01절 판)의 ask_json을 그대로 가져온다(PYTHONPATH=notebooks).
지시 글·머리글·공통 사실·검사 함수는 노트북 05절에 쓸 설계 판(05-probe.md §0)과 같게 둔다."""
import json, os, sys
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/mnt/한국경제신문/.env"))
from openai import OpenAI
from workflow_tools import ask_json

client = OpenAI()

FACT = ("2026년 10월 15일부터 전 직원 계정에 2단계 인증을 적용합니다. "
        "비밀번호만으로는 계정을 지키기 어렵기 때문입니다. "
        "등록은 사내 포털의 보안 메뉴에서 인증 앱을 연결하면 됩니다. "
        "문의는 help@company.test로 받습니다.")
TASKS = {
    "A": ("전 직원에게 보낼 2단계 인증 안내문을 120~180자로 쓰세요. 적용 날짜, 대상, 등록 방법, 문의처 주소를 담습니다.", 120, 180),
    "B1": ("전 직원에게 보낼 2단계 인증 안내문을 80~100자로 쓰세요. 적용 날짜, 대상, 등록 방법, 문의처 주소를 담습니다.", 80, 100),
    "B2": ("전 직원에게 보낼 2단계 인증 안내문을 150~170자로 쓰세요. 적용 날짜, 대상, 등록 방법, 문의처 주소를 담습니다.", 150, 170),
}
WRITE_INSTR = ("사내 안내문을 쓰는 작성자입니다. "
               "과제의 요구를 지키고, 공통 사실에 없는 날짜·연락처·절차는 지어내지 않습니다. "
               "앞 초안과 고칠 점이 주어지면 고칠 점을 반영해 안내문을 새로 씁니다. "
               '답은 JSON 객체 하나로만 출력합니다: {"안내문": "글"}')
WRITE_HEAD = "아래 과제에 맞는 안내문을 JSON으로 쓰세요.\n"
JUDGE_INSTR = ("사내 안내문 초안을 채점하는 평가 모델입니다. "
               "과제의 요구를 모두 지켰는지 보고 0~100 사이 정수로 점수를 매깁니다. "
               "고칠 점은 한 문장으로 적고, 고칠 것이 없으면 없음이라고 적습니다. "
               '답은 JSON 객체 하나로만 출력합니다: {"점수": 정수, "고칠 점": "한 문장"}')
JUDGE_HEAD = "아래 과제와 공통 사실로 초안을 평가해 JSON으로 답하세요.\n"
MUST = ["10월 15일", "전 직원", "보안 메뉴", "help@company.test"]
THRESHOLD = 85
TURN_LIMIT = 3


def check_draft(draft, min_length, max_length, must_words):
    problems = []
    if len(draft) < min_length:
        problems.append("글자 수가 " + str(min_length) + "자보다 적음")
    if len(draft) > max_length:
        problems.append("글자 수가 " + str(max_length) + "자보다 많음")
    for word in must_words:
        if word not in draft:
            problems.append(word + " 없음")
    return problems


def decide_stop(rounds, threshold, turn_limit):
    last = rounds[-1]
    if last["점수"] >= threshold and len(last["문제"]) == 0:
        return "기준 통과"
    if len(rounds) >= turn_limit:
        return "바퀴 한도"
    return "계속"


def build_notes(rounds):
    if len(rounds) == 0:
        return ""
    last = rounds[-1]
    notes = "\n앞 초안: " + last["초안"] + "\n앞 초안 글자 수: " + str(last["글자 수"])
    notes = notes + "\n평가 모델의 고칠 점: " + last["고칠 점"]
    for problem in last["문제"]:
        notes = notes + "\n코드 검사의 문제: " + problem
    return notes


def write_and_judge(client, records, setup, base_text, rounds):
    write_request = setup["쓰기 머리글"] + base_text + build_notes(rounds)
    written = ask_json(client, records, "쓰기", setup["쓰기 지시 글"], write_request)
    draft = written["안내문"]
    judge_request = setup["평가 머리글"] + base_text + "\n초안: " + draft
    judged = ask_json(client, records, "평가", setup["평가 지시 글"], judge_request)
    row = {"초안": draft, "글자 수": len(draft), "점수": judged["점수"], "고칠 점": judged["고칠 점"]}
    row["문제"] = check_draft(draft, setup["최소 글자 수"], setup["최대 글자 수"], setup["필수 말"])
    return row


def finish_loop(rounds, reason):
    status = "멈춤"
    if reason == "기준 통과":
        status = "완료"
    return {"상태": status, "멈춘 까닭": reason, "바퀴": rounds, "안내문": rounds[-1]["초안"]}


def run_write_judge_loop(client, records, setup, task_text, fact):
    base_text = "과제: " + task_text + "\n공통 사실: " + fact
    rounds = []
    for turn in range(setup["바퀴 한도"]):
        rounds.append(write_and_judge(client, records, setup, base_text, rounds))
        reason = decide_stop(rounds, setup["기준값"], setup["바퀴 한도"])
        if reason != "계속":
            break
    return finish_loop(rounds, reason)


def main():
    mode, name, times = sys.argv[1], sys.argv[2], int(sys.argv[3])
    task_text, lo, hi = TASKS[name]
    setup = {"쓰기 지시 글": WRITE_INSTR, "쓰기 머리글": WRITE_HEAD, "평가 지시 글": JUDGE_INSTR,
             "평가 머리글": JUDGE_HEAD, "최소 글자 수": lo, "최대 글자 수": hi, "필수 말": MUST,
             "기준값": THRESHOLD, "바퀴 한도": TURN_LIMIT}
    tot_in = tot_out = 0
    for t in range(times):
        records = []
        result = run_write_judge_loop(client, records, setup, task_text, FACT)
        for row in records:
            tot_in += row["입력 토큰"]; tot_out += row["출력 토큰"]
        print("=== run", t + 1, "| task", name, "| 상태", result["상태"], "| 멈춘 까닭", result["멈춘 까닭"],
              "| 바퀴 수", len(result["바퀴"]), "| 요청 수", len(records))
        for i, r in enumerate(result["바퀴"]):
            print("  바퀴", i + 1, "| 글자 수", r["글자 수"], "| 점수", r["점수"], type(r["점수"]).__name__,
                  "| 문제", r["문제"], "| 고칠 점", r["고칠 점"])
            print("     초안:", r["초안"])
        print("  records:", [(row["단계"], row["입력 토큰"], row["출력 토큰"]) for row in records])
    print("TOTAL tokens in", tot_in, "out", tot_out)


main()
