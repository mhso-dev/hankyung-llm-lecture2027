"""Ch 18 워크플로우 5패턴 — 이 챕터 앞 절에서 배운 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from workflow_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""
import asyncio
import json
import re


# Ch 18 01절에서 배웠습니다 — 요청 한 번의 기록 한 줄(단계 이름·입력 토큰·출력 토큰)을 기록 목록 끝에 더합니다
def add_record(records, step_name, usage):
    row = {"단계": step_name}
    row["입력 토큰"] = usage.input_tokens
    row["출력 토큰"] = usage.output_tokens
    records.append(row)


# Ch 18 01절에서 배웠습니다 — 기록 목록을 줄마다 번호·단계·입력 토큰·출력 토큰 차례로 출력합니다
def print_records(records):
    print("번호 | 단계 | 입력 토큰 | 출력 토큰")
    for i in range(len(records)):
        row = records[i]
        print(i + 1, "|", row["단계"], "|", row["입력 토큰"], "|", row["출력 토큰"])


# Ch 18 01절에서 배웠습니다 — 요청을 한 번 보내 기록 한 줄을 남기고, 받은 JSON 글을 딕셔너리로 읽어 내놓습니다(모델 요청 1번)
def ask_json(client, records, step_name, instructions_text, request_text):
    response = client.responses.create(
        # 모델 이름과 설정: temperature 0, 추론 none(01절 직접 요청과 같음)
        model="gpt-5.4-mini", temperature=0, reasoning={"effort": "none"},
        # 지시 글과 요청 글, 그리고 답을 JSON 글로만 받는 형식
        instructions=instructions_text, input=request_text,
        text={"format": {"type": "json_object"}},
    )
    add_record(records, step_name, response.usage)
    return json.loads(response.output_text)


# Ch 18 01절에서 배웠습니다 — 게이트: 기획이 다음 단계에 쓸 모양인지 코드로 검사해 문제를 글 목록으로 내놓습니다(문제가 없으면 빈 목록)
def check_plan(plan, required_keys, min_count):
    problems = []
    for key in required_keys:
        if key not in plan:
            problems.append(key + " 칸 없음")
    # 칸 「절차」가 있으면 목록인지, 목록이면 정한 수 이상인지 봅니다(or는 앞이 참이면 뒤를 보지 않음)
    if "절차" in plan and (type(plan["절차"]) != list or len(plan["절차"]) < min_count):
        problems.append("절차가 " + str(min_count) + "개 이상인 목록이 아님")
    return problems


# Ch 18 01절에서 배웠습니다 — 작성 머리글 뒤에 기획 딕셔너리를 JSON 글로 바꿔 붙여 둘째 단계 요청 글을 만듭니다
def build_write_request(write_head, plan):
    plan_text = json.dumps(plan, ensure_ascii=False)
    return write_head + "\n\n기획:\n" + plan_text


# Ch 18 01절에서 배웠습니다 — 게이트가 있는 두 단계: 기획을 검사해 문제가 있으면 작성 요청을 보내지 않고 멈춥니다(모델 요청 1~2번)
def run_gated_chain(client, records, setup, plan_request):
    plan = ask_json(client, records, "기획", setup["지시 글"], plan_request)
    problems = check_plan(plan, setup["필수 칸"], setup["최소 절차 수"])
    # 문제가 하나라도 있으면 둘째 요청을 보내기 전에 멈춥니다
    if len(problems) > 0:
        return {"상태": "멈춤", "기획": plan, "문제": problems, "안내문": ""}
    write_request = build_write_request(setup["작성 머리글"], plan)
    written = ask_json(client, records, "작성", setup["지시 글"], write_request)
    return {"상태": "완료", "기획": plan, "문제": problems, "안내문": written["안내문"]}


# Ch 18 02절에서 배웠습니다 — 분류를 검사해 갈래로 보내면 안 되는 까닭을 글 목록으로 내놓습니다(문제가 없으면 빈 목록)
def check_route(decision, allowed_kinds, threshold):
    problems = []
    # 모델이 쓴 종류가 허용 목록에 없으면 문제입니다
    if decision["종류"] not in allowed_kinds:
        problems.append("허용 목록에 없는 종류")
    # 모델이 스스로 적은 신뢰도가 기준값보다 낮아도 문제입니다
    if decision["신뢰도"] < threshold:
        problems.append("신뢰도가 기준값보다 낮음")
    return problems


# Ch 18 02절에서 배웠습니다 — 라우팅: 분류를 검사해 문제가 있으면 되묻기 갈래로, 없으면 그 종류의 갈래로 답합니다(모델 요청 1~2번)
def route_question(client, records, setup, question):
    request_text = setup["요청 머리글"] + question
    decision = ask_json(client, records, "분류", setup["분류 지시 글"], request_text)
    problems = check_route(decision, setup["허용 목록"], setup["기준값"])
    # 문제가 하나라도 있으면 갈래 표를 찾기 전에 되묻기 갈래로 끝냅니다(답 요청 없음)
    if len(problems) > 0:
        return {"상태": "되묻기", "분류": decision, "문제": problems, "답": setup["되묻기 글"]}
    branch_instructions = setup["갈래 표"][decision["종류"]]
    written = ask_json(client, records, "답", branch_instructions, request_text)
    return {"상태": "완료", "분류": decision, "문제": problems, "답": written["답"]}


# Ch 18 03절에서 배웠습니다 — 요청 머리글과 공통 사실 뒤에, 쓸 부분의 이름과 담을 내용을 붙여 요청 글 하나를 만듭니다
def build_part_request(request_head, fact, part):
    part_lines = "\n쓸 부분: " + part["이름"] + "\n담을 내용: " + part["담을 내용"]
    return request_head + fact + part_lines


# Ch 18 03절에서 배웠습니다 — 요청 딕셔너리 목록을 함께 보내고, 받은 답을 넣은 차례대로 목록 하나로 내놓습니다(모델 요청 = 요청 수)
async def ask_all_together(client, records, requests):
    waitings = []
    for request in requests:
        # 요청마다 ask_json을 다른 스레드에서 부르는 코루틴을 만듭니다(기록 줄은 응답이 도착한 차례로 쌓임)
        waiting = asyncio.to_thread(ask_json, client, records, request["단계"], request["지시 글"], request["요청 글"])
        waitings.append(waiting)
    # 별표 *는 목록 waitings의 항목을 하나씩 풀어 gather() 괄호에 차례로 넣습니다
    answers = await asyncio.gather(*waitings)
    return answers


# Ch 18 03절에서 배웠습니다 — 받은 답 목록에서 칸 「글」을 차례로 꺼내, 한 줄씩 이어 안내문 하나로 만듭니다
def join_parts(answers):
    notice = ""
    for answer in answers:
        notice = notice + answer["글"] + "\n"
    return notice


# Ch 18 03절에서 배웠습니다 — 나눠 쓰기: 지시 글은 하나, 요청 글은 부분마다 다르게 만들어 함께 보내고 받은 글을 잇습니다(모델 요청 = 부분 수)
async def write_sections(client, records, setup, fact):
    requests = []
    for part in setup["부분"]:
        request_text = build_part_request(setup["요청 머리글"], fact, part)
        requests.append({"단계": part["이름"], "지시 글": setup["지시 글"], "요청 글": request_text})
    answers = await ask_all_together(client, records, requests)
    notice = join_parts(answers)
    return {"상태": "완료", "부분": answers, "안내문": notice}


# Ch 18 03절에서 배웠습니다 — 받은 답마다 칸 「표」를 읽어 A·B·그 밖으로 나눠 셉니다
def count_votes(answers):
    counts = {"A": 0, "B": 0, "그 밖": 0}
    for answer in answers:
        vote = answer["표"]
        # A도 B도 아닌 표(고르지 않음 등)는 그 밖으로 셉니다
        if vote != "A" and vote != "B":
            vote = "그 밖"
        counts[vote] = counts[vote] + 1
    return counts


# Ch 18 03절에서 배웠습니다 — 셈에서 A나 B가 필요한 표 수 이상을 받았으면 그 이름을, 둘 다 모자라면 「정하지 못함」을 내놓습니다
def decide_vote(counts, needed_votes):
    if counts["A"] >= needed_votes:
        return "A"
    if counts["B"] >= needed_votes:
        return "B"
    return "정하지 못함"


# Ch 18 03절에서 배웠습니다 — 투표: 요청 글은 하나, 지시 글은 평가자마다 다르게 두고 함께 보내 표를 세어 결과를 정합니다(모델 요청 = 평가자 수)
async def run_vote(client, records, setup, request_text):
    requests = []
    for judge in setup["평가자"]:
        requests.append({"단계": judge["이름"], "지시 글": judge["지시 글"], "요청 글": request_text})
    answers = await ask_all_together(client, records, requests)
    counts = count_votes(answers)
    result = decide_vote(counts, setup["필요한 표 수"])
    return {"상태": "완료", "답": answers, "셈": counts, "결과": result}


# Ch 18 04절에서 배웠습니다 — 계획의 작업 가운데 칸 「이름」과 「맡을 일」이 모두 있는 것만, 정한 수까지 골라 내놓습니다
def pick_tasks(plan, max_tasks):
    tasks = []
    for task in plan["작업"]:
        # 작업 요청을 만들 때 두 칸을 모두 쓰므로, 하나라도 없으면 뺍니다
        if "이름" in task and "맡을 일" in task:
            tasks.append(task)
    # 정한 수보다 많으면 앞에서부터 그 수만큼만 씁니다
    return tasks[:max_tasks]


# Ch 18 04절에서 배웠습니다 — 작업마다 요청 딕셔너리(단계·지시 글·요청 글)를 만들어 요청 목록 하나로 내놓습니다
def build_task_requests(instructions_text, task_head, fact, tasks):
    requests = []
    for task in tasks:
        # 요청 글 = 요청 머리글 + 공통 사실 + 맡을 작업의 이름과 맡을 일
        task_lines = "\n맡을 작업: " + task["이름"] + "\n맡을 일: " + task["맡을 일"]
        request_text = task_head + fact + task_lines
        requests.append({"단계": task["이름"], "지시 글": instructions_text, "요청 글": request_text})
    return requests


# Ch 18 04절에서 배웠습니다 — 종합 요청 글을 만듭니다: 머리글과 공통 사실 뒤에, 받은 작업 답의 글을 차례로 이어 붙입니다
def build_summary_request(summary_head, fact, answers):
    # 03절 함수 join_parts는 답마다 칸 「글」을 꺼내 넣은 차례로 한 줄씩 잇습니다
    answers_text = join_parts(answers)
    return summary_head + fact + "\n작업 답:\n" + answers_text


# Ch 18 04절에서 배웠습니다 — 검사할 글에서 정규식에 맞는 값 가운데, 공통 사실에서는 찾을 수 없는 것만 목록으로 내놓습니다
def find_new_contacts(text, fact, patterns):
    new_items = []
    for pattern in patterns:
        # 같은 정규식으로 공통 사실에서 찾은 목록에 없으면 공통 사실 밖의 값입니다
        fact_items = re.findall(pattern, fact)
        for item in re.findall(pattern, text):
            if item not in fact_items:
                new_items.append(item)
    return new_items


# Ch 18 04절에서 배웠습니다 — 계획 요청을 한 번 보내고, 받은 계획을 거른 작업 목록을 내놓습니다(모델 요청 1번)
def plan_tasks(client, records, setup, task_text, fact):
    plan_request = setup["계획 머리글"] + task_text + "\n공통 사실: " + fact
    plan = ask_json(client, records, "계획", setup["계획 지시 글"], plan_request)
    return pick_tasks(plan, setup["최대 작업 수"])


# Ch 18 04절에서 배웠습니다 — 작업 나눠 맡기기 흐름: 계획 → 작업 요청들을 함께 → 종합의 차례를 코드가 정합니다(모델 요청 = 1 + 작업 수 + 1)
async def run_orchestrator(client, records, setup, task_text, fact):
    tasks = plan_tasks(client, records, setup, task_text, fact)
    # 작업이 최소 작업 수보다 적으면 작업 요청을 보내기 전에 멈춥니다
    if len(tasks) < setup["최소 작업 수"]:
        return {"상태": "멈춤", "작업": tasks, "답": [], "안내문": ""}
    requests = build_task_requests(setup["작업 지시 글"], setup["작업 머리글"], fact, tasks)
    answers = await ask_all_together(client, records, requests)
    summary_request = build_summary_request(setup["종합 머리글"], fact, answers)
    summary = ask_json(client, records, "종합", setup["종합 지시 글"], summary_request)
    return {"상태": "완료", "작업": tasks, "답": answers, "안내문": summary["안내문"]}


# Ch 18 05절에서 배웠습니다 — 초안의 글자 수가 범위를 벗어났는지 검사해, 문제를 글 목록으로 내놓습니다(문제가 없으면 빈 목록)
def check_length(draft, min_length, max_length):
    problems = []
    # 함수 len()은 띄어쓰기와 문장 부호까지 한 글자로 셉니다. 어느 쪽으로 벗어났는지 적습니다
    if len(draft) < min_length:
        problems.append("글자 수가 " + str(min_length) + "자보다 적음")
    if len(draft) > max_length:
        problems.append("글자 수가 " + str(max_length) + "자보다 많음")
    return problems


# Ch 18 05절에서 배웠습니다 — 글자 수 검사에 이어, 꼭 담을 말이 초안에 있는지 검사합니다(문제가 없으면 빈 목록)
def check_draft(draft, min_length, max_length, must_words):
    problems = check_length(draft, min_length, max_length)
    # 꼭 담을 말이 초안에 글자 그대로 없으면 그 말마다 문제로 적습니다
    for word in must_words:
        if word not in draft:
            problems.append(word + " 없음")
    return problems


# Ch 18 05절에서 배웠습니다 — 바퀴 줄 목록의 마지막 줄을 보고 「기준 통과」·「바퀴 한도」·「계속」 가운데 하나를 내놓습니다
def decide_stop(rounds, threshold, turn_limit):
    last = rounds[-1]
    # 평가 점수가 기준값 이상이고, 코드 검사 문제도 없어야 통과입니다
    if last["점수"] >= threshold and len(last["문제"]) == 0:
        return "기준 통과"
    # 통과하지 못했어도 바퀴를 한도만큼 돌았으면 멈춥니다
    if len(rounds) >= turn_limit:
        return "바퀴 한도"
    return "계속"


# Ch 18 05절에서 배웠습니다 — 마지막 바퀴 줄로 다음 쓰기 요청 글 끝에 붙일 글(앞 초안·글자 수·고칠 점·코드 검사 문제)을 만듭니다
def build_notes(rounds):
    # 첫 바퀴에는 앞 바퀴가 없으므로 아무것도 붙이지 않습니다
    if len(rounds) == 0:
        return ""
    last = rounds[-1]
    notes = "\n앞 초안: " + last["초안"] + "\n앞 초안 글자 수: " + str(last["글자 수"])
    notes = notes + "\n평가 모델의 고칠 점: " + last["고칠 점"]
    for problem in last["문제"]:
        notes = notes + "\n코드 검사의 문제: " + problem
    return notes


# Ch 18 05절에서 배웠습니다 — 한 바퀴: 쓰기 요청과 평가 요청을 한 번씩 보내고 초안을 코드로 검사해, 바퀴 줄 하나를 내놓습니다(모델 요청 2번)
def write_and_judge(client, records, setup, base_text, rounds):
    write_request = setup["쓰기 머리글"] + base_text + build_notes(rounds)
    written = ask_json(client, records, "쓰기", setup["쓰기 지시 글"], write_request)
    draft = written["안내문"]
    judge_request = setup["평가 머리글"] + base_text + "\n초안: " + draft
    judged = ask_json(client, records, "평가", setup["평가 지시 글"], judge_request)
    row = {"초안": draft, "글자 수": len(draft), "점수": judged["점수"], "고칠 점": judged["고칠 점"]}
    row["문제"] = check_draft(draft, setup["최소 글자 수"], setup["최대 글자 수"], setup["필수 말"])
    return row


# Ch 18 05절에서 배웠습니다 — 멈춘 까닭으로 흐름 결과를 만듭니다: 기준을 통과했을 때만 상태 「완료」, 바퀴 한도면 「멈춤」
def finish_loop(rounds, reason):
    status = "멈춤"
    if reason == "기준 통과":
        status = "완료"
    return {"상태": status, "멈춘 까닭": reason, "바퀴": rounds, "안내문": rounds[-1]["초안"]}


# Ch 18 05절에서 배웠습니다 — 쓰고 평가하기 반복 흐름: 바퀴마다 쓰기·평가·코드 검사를 하고, 멈출지는 코드가 고릅니다(모델 요청 = 바퀴 수 × 2)
def run_write_judge_loop(client, records, setup, task_text, fact):
    base_text = "과제: " + task_text + "\n공통 사실: " + fact
    rounds = []
    for turn in range(setup["바퀴 한도"]):
        rounds.append(write_and_judge(client, records, setup, base_text, rounds))
        reason = decide_stop(rounds, setup["기준값"], setup["바퀴 한도"])
        # 판정이 「계속」이 아니면 남은 바퀴를 돌지 않고 끝냅니다
        if reason != "계속":
            break
    return finish_loop(rounds, reason)


# Ch 18 06절에서 배웠습니다 — 기록 목록의 줄마다 입력 토큰과 출력 토큰을 더해, 흐름 하나의 토큰 수를 내놓습니다
def total_tokens(records):
    total = 0
    for row in records:
        total = total + row["입력 토큰"] + row["출력 토큰"]
    return total


# Ch 18 06절에서 배웠습니다 — 안내문을 05절 코드 검사로 보고, 항목 가운데 문제가 없는 항목 수를 내놓습니다
def grade_notice(notice, grade_setup):
    problems = check_draft(notice, grade_setup["최소 글자 수"], grade_setup["최대 글자 수"], grade_setup["필수 말"])
    # 글자 수 검사는 문제를 많아야 하나 내므로, 항목 수는 글자 수 1 + 꼭 담을 말 수입니다
    item_count = 1 + len(grade_setup["필수 말"])
    return item_count - len(problems)


# Ch 18 06절에서 배웠습니다 — 흐름 하나의 기록 목록·걸린 초·상태·안내문으로 비교 표 한 줄(칸 여섯)을 딕셔너리로 만듭니다
def make_row(pattern, records, elapsed, state, notice, grade_setup):
    row = {"패턴": pattern, "요청 수": len(records), "토큰 수": total_tokens(records)}
    row["걸린 초"] = round(elapsed, 3)
    row["품질"] = grade_notice(notice, grade_setup)
    # 흐름이 끝까지 간 「완료」만 ok로 적고, 멈춤·되묻기는 그 상태를 그대로 적습니다
    row["상태"] = state
    if state == "완료":
        row["상태"] = "ok"
    return row
