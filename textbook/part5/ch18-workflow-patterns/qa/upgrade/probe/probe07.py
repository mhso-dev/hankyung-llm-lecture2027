"""Ch 18 07절(실습) 흔들림 확인(노트북 밖). 키 값은 .env에서만 읽고 출력하지 않는다.
사용: python probe07.py <요청 글 A|B> <회차 수> [check]
  한 회차 = 노트북과 같은 두 실행: 실행 1(창구 설정 그대로) → 실행 2(허용 목록에서 보안을 뺀 설정). 실행마다 기록 목록을 따로 둔다.
설정 글·조립 함수는 author_07.py 의 노트북 코드 셀 문자열(SETUP_CELLS, NARROW)을 그대로 exec 해서 만든다(노트북과 같은 글·함수).
도구 파일 workflow_tools.py 의 01~03절 함수를 그대로 가져온다(PYTHONPATH=notebooks).
'check' 를 주면 모델을 부르지 않고 설정 글만 만들어 03·06 판과 대조한다."""
import asyncio, contextlib, importlib.util, io, json, os, sys, time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/mnt/한국경제신문/.env"))
from openai import OpenAI
import workflow_tools as wt

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("author_07", HERE.parent / "author_07.py")
author = importlib.util.module_from_spec(spec); spec.loader.exec_module(author)

REQUESTS = {
    "A": "전 직원 계정에 2단계 인증을 적용한다는 공지를 올려 주세요.",
    "B": "보안 메뉴에서 2단계 인증을 등록하라는 보안 공지를 전 직원에게 보내 주세요.",
}


def build_namespace(name, client=None):
    ns = {"ask_json": wt.ask_json, "build_part_request": wt.build_part_request, "check_route": wt.check_route,
          "print_records": wt.print_records, "write_sections": wt.write_sections, "client": client}
    for cell in author.SETUP_CELLS:
        src = cell
        if cell is author.REQUEST:
            src = cell.replace(REQUESTS["A"], REQUESTS[name])
        with contextlib.redirect_stdout(io.StringIO()):
            exec(src, ns)
    assert ns["notice_request"] == REQUESTS[name]
    with contextlib.redirect_stdout(io.StringIO()):
        exec(author.NARROW, ns)
    return ns


def check():
    ns = build_namespace("A")
    # 03절 생성기의 지시 글·머리글, 06절 생성기의 분류 지시 글과 대조(모델 요청 없음)
    spec3 = importlib.util.spec_from_file_location("author_03", HERE.parent / "author_03.py")
    a3 = importlib.util.module_from_spec(spec3); spec3.loader.exec_module(a3)
    spec6 = importlib.util.spec_from_file_location("author_06", HERE.parent / "author_06.py")
    a6 = importlib.util.module_from_spec(spec6); spec6.loader.exec_module(a6)
    ns3 = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(a3.FACT, ns3); exec(a3.WRITE_TEXT, ns3)
        exec(a3.DEF_BUILD, ns3); exec(a3.PARTS, ns3)
    ns6 = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(a6.ROUTE_TEXT, ns6)
    print("공통 사실 03과 같음:", ns["notice_fact"] == ns3["notice_fact"], len(ns["notice_fact"]))
    print("부분 지시 글 03과 같음:", ns["section_instructions"] == ns3["write_instructions"])
    print("부분 요청 머리글 03과 같음:", ns["section_head"] == ns3["request_head"])
    c7 = ns["classify_instructions"]; c6 = ns6["classify_instructions"]
    print("분류 지시 글 06과 첫 문장 뒤가 같음:", c7.split(". ", 1)[1] == c6.split(". ", 1)[1])
    print("설정 칸:", list(ns["desk_setup"].keys()))
    print("그대로인 칸:", ns["same_keys"])
    print("--- 분류 요청 글"); print(ns["classify_request"])
    print("--- 적용 부분 요청 글"); print(ns["first_part_request"])


def run_round(client, ns, label):
    out = {"run": label}
    for which, setup_name in (("one", "desk_setup"), ("two", "narrow_setup")):
        records = []
        result = asyncio.run(ns["serve_notice"](client, records, ns[setup_name], ns["notice_request"], ns["notice_fact"]))
        part_order = [a.get("부분") for a in result["부분"]]
        out[which] = {"상태": result["상태"], "분류": result["분류"], "문제": result["문제"], "요청 수": len(records),
                      "부분 요청 수": len(result["부분"]), "부분 차례": part_order,
                      "records": [(r["단계"], r["입력 토큰"], r["출력 토큰"]) for r in records],
                      "글자 수": len(result["안내문"]), "안내문": result["안내문"]}
    return out


def main():
    name, times = sys.argv[1], int(sys.argv[2])
    client = OpenAI()
    ns = build_namespace(name, client)
    out = []
    for t in range(times):
        print("=== round", t + 1, "| request", name, "|", time.strftime("%H:%M:%S", time.gmtime()), "UTC")
        item = run_round(client, ns, t + 1)
        for which in ("one", "two"):
            r = item[which]
            print(which, "|", r["상태"], "|", r["분류"], "|", r["문제"], "| 요청", r["요청 수"], "| 부분", r["부분 요청 수"],
                  r["부분 차례"], "|", r["records"], "| 글자", r["글자 수"])
        out.append(item)
    Path("/tmp/ch18-07/probe-" + name + ".json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("done", time.strftime("%H:%M:%S", time.gmtime()), "UTC")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[-1] == "check":
        check()
    else:
        main()
