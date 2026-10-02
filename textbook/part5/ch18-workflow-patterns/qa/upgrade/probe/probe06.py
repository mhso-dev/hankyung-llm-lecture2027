"""Ch 18 06절 흔들림 확인(노트북 밖). 키 값은 .env에서만 읽고 출력하지 않는다.
사용: python probe06.py <과제 이름 A|B> <회차 수> [check]
  한 회차 = 06 과제 글로 다섯 흐름(01 run_gated_chain · 02 route_question · 03 write_sections · 04 run_orchestrator ·
  05 run_write_judge_loop)을 한 번씩, 흐름마다 기록 목록을 따로 두고 앞뒤 time.perf_counter()로 걸린 초를 잰다.
설정 글은 author_06.py 의 노트북 코드 셀 문자열(SETUP_CELLS)을 그대로 exec 해서 만든다(노트북과 같은 글).
도구 파일 workflow_tools.py 의 01~05절 함수를 그대로 가져온다(PYTHONPATH=notebooks).
'check' 를 주면 모델을 부르지 않고 설정 글만 만들어 04·05 판과 대조한다."""
import asyncio, importlib.util, json, os, sys, time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/mnt/한국경제신문/.env"))
from openai import OpenAI
import workflow_tools as wt

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("author_06", HERE.parent / "author_06.py")
author = importlib.util.module_from_spec(spec); spec.loader.exec_module(author)

TASKS = {
    "A": ("전 직원에게 보낼 2단계 인증 안내문을 120~180자로 쓰세요. 적용 날짜, 대상, 등록 방법, 문의처 주소를 담습니다.", 120, 180),
    "B": ("전 직원에게 보낼 2단계 인증 안내문을 100~200자로 쓰세요. 적용 날짜, 대상, 등록 방법, 문의처 주소를 담습니다.", 100, 200),
}


def build_namespace(name):
    ns = {"check_draft": wt.check_draft, "time": time}
    task_text, lo, hi = TASKS[name]
    for cell in author.SETUP_CELLS:
        src = cell
        if cell is author.TASK:
            src = cell.replace("120~180자로", task_text.split("안내문을 ")[1].split("로 쓰세요")[0] + "로")
            src = src.replace('{"최소 글자 수": 120, "최대 글자 수": 180}', '{"최소 글자 수": ' + str(lo) + ', "최대 글자 수": ' + str(hi) + '}')
        if cell is author.HAND:
            continue
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            exec(src, ns)
    assert ns["task_text"] == task_text, (ns["task_text"], task_text)
    return ns


def check():
    ns = build_namespace("A")
    exec(author.HAND, ns)
    # probe04.py 는 import 하면 main()을 바로 부르므로, 두 파일의 상수 대입만 AST로 읽어 값을 셈한다(모델 요청 없음)
    import ast, types
    def constants(path):
        tree = ast.parse(path.read_text())
        values = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                try:
                    values[node.targets[0].id] = ast.literal_eval(node.value)
                except ValueError:
                    pass
        return types.SimpleNamespace(**values)
    probe04 = constants(HERE / "probe04.py")
    probe05 = constants(HERE / "probe05.py")
    print("04 계획 지시 글 같음:", ns["plan_instructions"] == probe04.PLAN_INSTR)
    print("04 작업 지시 글 같음:", ns["task_instructions"] == probe04.TASK_INSTR)
    print("04 종합 지시 글 같음:", ns["summary_instructions"] == probe04.SUM_INSTR)
    print("04 계획·작업 머리글 같음:", ns["orchestrator_setup"]["계획 머리글"] == probe04.PLAN_HEAD, ns["orchestrator_setup"]["작업 머리글"] == probe04.TASK_HEAD)
    print("05 쓰기 지시 글 같음:", ns["write_instructions"] == probe05.WRITE_INSTR)
    print("05 평가 지시 글 같음:", ns["judge_instructions"] == probe05.JUDGE_INSTR)
    print("05 머리글 같음:", ns["loop_setup"]["쓰기 머리글"] == probe05.WRITE_HEAD, ns["loop_setup"]["평가 머리글"] == probe05.JUDGE_HEAD)
    print("05 필수 말 같음:", ns["grade_setup"]["필수 말"] == probe05.MUST)
    print("공통 사실 같음:", ns["notice_fact"] == probe05.FACT, len(ns["notice_fact"]))
    for key in ["plan_request", "chain_head"]:
        print("---", key); print(ns[key])
    print("--- 분류 요청 글"); print(ns["route_setup"]["요청 머리글"] + ns["base_text"])
    print("--- 부분 요청 글(적용)"); print(wt.build_part_request(ns["sections_setup"]["요청 머리글"], ns["notice_fact"], ns["parts"][0]))
    print("--- 종합 머리글"); print(ns["summary_head"])


def run_one(client, ns, label, kind):
    records = []
    start = time.perf_counter()
    if kind == "chaining":
        result = wt.run_gated_chain(client, records, ns["chain_setup"], ns["plan_request"])
        notice = result["안내문"]
    elif kind == "routing":
        result = wt.route_question(client, records, ns["route_setup"], ns["base_text"])
        notice = result["답"]
    elif kind == "parallel":
        result = asyncio.run(wt.write_sections(client, records, ns["sections_setup"], ns["notice_fact"]))
        notice = result["안내문"]
    elif kind == "orchestrator_worker":
        result = asyncio.run(wt.run_orchestrator(client, records, ns["orchestrator_setup"], ns["task_text"], ns["notice_fact"]))
        notice = result["안내문"]
    else:
        result = wt.run_write_judge_loop(client, records, ns["loop_setup"], ns["task_text"], ns["notice_fact"])
        notice = result["안내문"]
    elapsed = time.perf_counter() - start
    row = ns["make_row"](kind, records, elapsed, result["상태"], notice, ns["grade_setup"])
    gs = ns["grade_setup"]
    problems = wt.check_draft(notice, gs["최소 글자 수"], gs["최대 글자 수"], gs["필수 말"])
    extra = {}
    if kind == "chaining":
        extra = {"문제": result["문제"], "절차 수": len(result["기획"].get("절차", [])) if isinstance(result["기획"].get("절차"), list) else None}
    if kind == "routing":
        extra = {"분류": result["분류"]}
    if kind == "orchestrator_worker":
        extra = {"작업": [t["이름"] for t in result["작업"]]}
    if kind == "generator_evaluator":
        extra = {"멈춘 까닭": result["멈춘 까닭"], "바퀴": [(r["글자 수"], r["점수"], r["문제"]) for r in result["바퀴"]]}
    return {"run": label, "kind": kind, "상태": result["상태"], "row": row, "글자 수": len(notice), "문제": problems,
            "records": [(r["단계"], r["입력 토큰"], r["출력 토큰"]) for r in records], "extra": extra, "안내문": notice}


def main():
    name, times = sys.argv[1], int(sys.argv[2])
    ns = build_namespace(name)
    client = OpenAI()
    out = []
    kinds = ["chaining", "routing", "parallel", "orchestrator_worker", "generator_evaluator"]
    for t in range(times):
        print("=== run", t + 1, "| task", name, "|", time.strftime("%H:%M:%S", time.gmtime()), "UTC")
        for kind in kinds:
            item = run_one(client, ns, t + 1, kind)
            out.append(item)
            r = item["row"]
            print("  ", kind, "상태", item["상태"], "calls", r["요청 수"], "tokens", r["토큰 수"], "sec", r["걸린 초"],
                  "quality", r["품질"], "len", item["글자 수"], "문제", item["문제"], item["extra"])
    dest = Path("/tmp/ch18-06/probe-" + name + ".json")
    old = []
    if dest.exists():
        old = json.loads(dest.read_text())
    dest.write_text(json.dumps(old + out, ensure_ascii=False, indent=1))
    n_ok = sum(1 for i in out if i["상태"] == "완료")
    print("완료", n_ok, "/", len(out), "| requests", sum(i["row"]["요청 수"] for i in out),
          "| in", sum(x[1] for i in out for x in i["records"]), "| out", sum(x[2] for i in out for x in i["records"]))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check()
    else:
        main()
