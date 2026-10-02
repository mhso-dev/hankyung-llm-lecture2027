"""Ch 34 06절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§5-3·§6 experiment).

사용:
  python3 -B author_06.py               → 도구 파일(없거나 01·02·04·05·06 판일 때만) + 노트북 + _src 본문을 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_06.py --src-only    → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_06.py --nb-copy DIR → 새 노트북과 06 판 도구 파일 사본을 DIR에만 쓴다(사본 실행·새 커널 B용 — 실습 폴더는 건드리지 않음)
  python3 -B author_06.py --tools-copy DIR → 06 판 도구 파일 사본만 DIR에 쓴다(흔들림 확인·설계 확인용)
  python3 -B author_06.py --guard-check → 01·02·04·05 생성기의 쓰기 가드와 03 생성기 대조가 06 판을 덮어쓰지 않는지 본다
  python3 -B author_06.py --design-check → 모델 요청이 없는 코드 셀을 커널 없이 차례로 실행해, 본문에 쓴 매번 같은 값이 출력에 있는지 본다
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음. 설계는 qa/upgrade/06-design.md,
노트북 밖 흔들림 확인 5번은 qa/upgrade/probe/06-probe.md(§0을 첫 요청 전에 적음).

## 결정 1 — 붙인 앞 절 기능 셋 (handoff 「§05 → 실습 절」 2번 · 과정표 과제 「대화당 비용을 줄이고 무엇을 포기했는지」)

책 가게 문의 셋(03절 문의 글·정답 종류)에 01절 정책 글(규칙 문장 100번)을 앞에 붙여 보내는 흐름 하나:
03 모델 라우터(choose_model — 기준 길이로 nano·mini) → 05 예산 가드(대화마다 먼저 try_reserve, 비용 상한에 걸린 대화는 보내지 않음,
예약 금액 = 정한 사용량(make_usage 3200·0·20)을 모델마다 estimate_cost로) → 01 실험 번호 + make_request + 03 send_inquiry(실제 요청)
→ 01 cost_row(캐시 입력 할인을 넣은 값·할인 없이 센 값) + 05 total_cost. 셋 모두 실행 1·2 흐름에서 출력으로 보인다.
뺀 것: 02 일괄 처리(노트북 안에서 기다리지 않음 — 02 조건) · 04 다시 보내기·한꺼번에 보내는 수(실패·함께 보내기가 없어 드러나지 않음) · 05 평균·95 백분위수.

## 결정 2 — 실행 2는 기준 길이 하나만 (30 → 0, 03절 값 바꿔 보기와 같은 값)

같은 비용 상한 0.006에서 실행 1(nano·nano·mini)은 셋 모두 받고(예약 합 0.00382), 실행 2(mini 셋)는 셋째 대화가 막힘(0.00747 > 0.006).
모델 요청 5번(실행 1 3 + 실행 2 2 — 막힌 대화는 보내지 않음). 실험 번호는 실행마다 새로 만든다.
b2 「새로 볼 것」은 실행이 보인 만큼만(Ch 26 05 검토 B-7). 결론은 설계로 정한 값 + 흔들림 확인 5/5·두 커널 같은 서비스 판단 값(한정어).
흔들리는 값(토큰·캐시 입력 수·답 글·요금)은 [[이름]] 자리 → A 출력으로 mdpatch.py. 모델 출력·토큰·요금에 assert 없음. 빨강 0 · 보라는 실제로 부른 두 모델만.

## 결정 3 — 도구 파일 cost_tools.py 06 판 (규격 §2-7 · handoff 3항)

05 판(68ac446c…, 마감 전 39bb0e25…) 뒤에 노트북에만 있던 앞 절 함수 일곱을 절·셀 차례로 더한다: 01 make_request·cost_row · 03 choose_model·send_inquiry ·
05 make_usage·total_cost·try_reserve. 주석 「# Ch 34 0N절에서 배웠습니다 — Ch 34 0N절 노트북 셀의 같은 이름 함수를 옮겼습니다」 + 셀 첫 줄 설명 주석 +
def~return 글자 그대로. 원본은 노트북 verification.code_sha256으로 고정하고, 생성기 상수·AST·설명 줄과 대조한다. 가져오기 줄은 늘지 않는다.
쓰기 가드: 없거나 01·02·04·05·06 판일 때만(06 판으로 시작하는 더 긴 판은 건너뜀).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·`key=`·`reverse=`·
`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·힌트·대입 풀기(for 포함)·별표 풀기·`while`·`raise`·`try`(도구 파일 try_reserve 안 말고)·
세미콜론·`isinstance`·클래스·데코레이터·가짜 모델·비동기·파일 쓰기·`max_retries`. 호출 깊이 2 이하.
01~05 노트북에 없던 내장 이름·속성·키워드 인자·노드 종류 0(도구 파일로 옮긴 함수의 가져오기 이름만 새로 생김).
"""
from __future__ import annotations

import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import KEY, RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

CHAPTER = ROOT / "textbook/part7/ch34-cost-rate-limits"
LAB = ROOT / "labs/part7/ch34-cost-rate-limits/notebooks"
FIGS = CHAPTER / "figures"
SLUG = "06-비용과-Rate-Limit-실습"
TITLE_TEXT = "비용과 Rate Limit 실습: 문의 셋을 모델 라우터와 예산 가드로 보내고 기준 길이 바꾸기"
SRC = CHAPTER / "_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "cost_tools.py"
TOOLS05_SHA = "68ac446cfb3fcf8fb395a9e5a65db9c350d694528f952bf28ec8dc785102a4af"
NB01 = LAB / "01-프롬프트-캐시-계측.ipynb"
NB03 = LAB / "03-모델-라우팅.ipynb"
NB05 = LAB / "05-예산-가드와-p95.ipynb"
# 원본 노트북의 코드 셀 해시(execute.py code_sha256) — 마크다운만 고쳐도 바뀌지 않는 값으로 고정
NB_CODE_SHA = {
    "01": "f5a17ed5befbbcbe",
    "03": "2d7f2868d55a40d5",
    "05": "92e7ef90171e1498",
}
RUNS_SENTENCE = os.environ.get("AUTHOR06_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물여섯 가운데 스물의 출력 글이 셀마다 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 다른 여섯은 모델 응답의 토큰 수와 그 값으로 센 비용이 든 셀입니다. 둘째 실행에서는 실행 1 대화 2에 캐시 입력이 생기지 않아, 5절 둘째 셀 대화 2의 칸도 달랐습니다. 모델 배정·예약 결과·보낸 요청 수와 다섯 답의 정답 여부는 두 번 모두 같았습니다.")


def load_author(number: str):
    spec = importlib.util.spec_from_file_location("author_" + number, CHAPTER / "qa/upgrade" / ("author_" + number + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A05 = load_author("05")
A04 = A05.A04
A02 = A05.A02
A01 = A05.A01
A03 = load_author("03")
TOOLS01 = A01.TOOLS01
TOOLS02 = A02.TOOLS02
TOOLS04 = A04.TOOLS04
TOOLS05 = A05.TOOLS05

# ---------------------------------------------------------------- 도구 파일 cost_tools.py (06 판)
# (절, 원본 노트북, 함수 이름, 그 절 생성기의 셀 상수)
MOVE06 = [
    ("01", NB01, "make_request", A01.DEF_REQUEST),
    ("01", NB01, "cost_row", A01.DEF_COST),
    ("03", NB03, "choose_model", A03.DEF_CHOOSE),
    ("03", NB03, "send_inquiry", A03.DEF_SEND),
    ("05", NB05, "make_usage", A05.DEF_USAGE),
    ("05", NB05, "total_cost", A05.DEF_TOTAL),
    ("05", NB05, "try_reserve", A05.DEF_TRY),
]
MOVE_NAMES = []
for _item in MOVE06:
    MOVE_NAMES.append(_item[2])
TOOL_ORDER06 = A05.TOOL_ORDER05 + MOVE_NAMES


def note_of(section: str) -> str:
    return "Ch 34 " + section + "절에서 배웠습니다 — Ch 34 " + section + "절 노트북 셀의 같은 이름 함수를 옮겼습니다"


def nb_cell(path: Path, section: str, name: str) -> str:
    """원본 노트북(코드 셀 해시 고정)에서 def name이 든 코드 셀 글을 꺼냅니다(첫 줄 설명 주석 포함)."""
    nb = json.loads(path.read_text(encoding="utf-8"))
    sources = []
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            sources.append(cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"]))
    got = hashlib.sha256(json.dumps(sources, ensure_ascii=False).encode()).hexdigest()
    assert got.startswith(NB_CODE_SHA[section]), path.name + " 노트북 코드 셀이 고정한 판과 다릅니다"
    assert nb["metadata"]["verification"]["code_sha256"] == got, path.name + " verification.code_sha256이 코드 셀과 다릅니다"
    for source in sources:
        if ("def " + name + "(") in source:
            return source
    raise KeyError(name)


def tools06_text() -> str:
    assert hashlib.sha256(TOOLS05.encode("utf-8")).hexdigest() == TOOLS05_SHA, "05 판 해시가 다릅니다"
    text = TOOLS05
    for section, path, name, gen_cell in MOVE06:
        cell = nb_cell(path, section, name)
        assert cell == gen_cell.strip("\n"), name + " — 노트북 셀과 생성기 상수가 다릅니다"
        desc = A02.description_of(cell, name, "cell")
        text = text + "\n\n# " + note_of(section) + "\n# " + desc + "\n" + A01.def_to_return(cell, name) + "\n"
    return text


TOOLS06 = tools06_text()


def free_names(func: ast.FunctionDef) -> set:
    """함수 안에서 읽는 이름 가운데 인자·함수 안 대입 이름이 아닌 것."""
    local = set()
    for arg in func.args.args:
        local.add(arg.arg)
    for node in ast.walk(func):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            local.add(node.id)
        if isinstance(node, ast.ExceptHandler) and node.name:
            local.add(node.name)
    used = set()
    for node in ast.walk(func):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id not in local:
            used.add(node.id)
    return used


def check_tools06() -> None:
    """06 판이 05 판을 그대로 이어 쓰고, 더한 일곱이 원본 노트북 셀과 글자·AST·설명 줄 모두 같은지 봅니다."""
    A05.check_tools05()
    assert hashlib.sha256(TOOLS05.encode("utf-8")).hexdigest() == TOOLS05_SHA
    plain06 = A01.strip_later_imports(TOOLS06)
    assert TOOLS06.startswith(TOOLS05), "06 판이 05 판으로 시작하지 않습니다"
    for older in (TOOLS05, TOOLS04, TOOLS02):
        assert plain06.startswith(A01.strip_later_imports(older))
    assert plain06.startswith(TOOLS01)
    tree = ast.parse(TOOLS06)
    names = []
    imports = []
    functions = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
            functions[node.name] = node
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == TOOL_ORDER06, names
    assert imports == ["import json", "import math", "import socket", "import time"], imports
    for name in A05.TOOL_ORDER05:
        assert A01.def_to_return(TOOLS06, name) == A01.def_to_return(TOOLS05, name), name
    allowed = set(names) | {"print", "round", "len", "str", "ValueError", "math", "json", "socket", "time", "open", "sorted"}
    for section, path, name, gen_cell in MOVE06:
        cell = nb_cell(path, section, name)
        block = "# " + note_of(section) + "\n# " + A02.description_of(cell, name, "cell") + "\n" + A01.def_to_return(cell, name) + "\n"
        assert block in TOOLS06, name
        assert A01.def_to_return(TOOLS06, name) == A01.def_to_return(cell, name), name
        mine = A05.function_dumps(TOOLS06, name)
        assert mine == A05.function_dumps(cell, name) and len(mine) == 1, name + " — 셀과 AST가 다릅니다"
        extra = free_names(functions[name]) - allowed
        assert not extra, (name, extra)
    bad = (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp, ast.Lambda, ast.IfExp, ast.JoinedStr, ast.ClassDef, ast.Global)
    whiles = 0
    for node in ast.walk(tree):
        assert not isinstance(node, bad), type(node).__name__
        if isinstance(node, ast.While):
            whiles = whiles + 1
    assert whiles == 1, "while은 Ch 28 03절 wait_for_port 안의 하나뿐이어야 합니다"


def write_tools() -> None:
    """도구 파일은 없거나 01·02·04·05·06 판일 때만 06 판으로 쓴다. 06 판으로 시작하는 더 긴 판은 덮어쓰지 않는다."""
    current = ""
    if TOOLS_PATH.is_file():
        current = TOOLS_PATH.read_text(encoding="utf-8")
    if current == TOOLS06:
        print("same", TOOLS_PATH.name, hashlib.sha256(TOOLS06.encode("utf-8")).hexdigest()[:12])
        return
    if current in ("", TOOLS01, TOOLS02, TOOLS04, TOOLS05):
        TOOLS_PATH.write_text(TOOLS06, encoding="utf-8")
        print("wrote", TOOLS_PATH, hashlib.sha256(TOOLS06.encode("utf-8")).hexdigest()[:12])
        return
    plain = A01.strip_later_imports(current)
    assert plain.startswith(A01.strip_later_imports(TOOLS06)), "도구 파일이 06절 판으로 시작하지 않습니다 — 손으로 확인하세요"
    print("skip", TOOLS_PATH, "(뒤에서 함수를 더한 판 — 덮어쓰지 않음)")


def guard_check() -> None:
    """01·02·04·05 생성기의 쓰기 가드가 06 판을 건너뛰고, 03 생성기 대조가 06 판을 받아들이는지 본다(파일 해시 전후)."""
    before = hashlib.sha256(TOOLS_PATH.read_bytes()).hexdigest()
    assert before == hashlib.sha256(TOOLS06.encode("utf-8")).hexdigest(), "실습 폴더 도구 파일이 06 판이 아닙니다"
    A01.write_tools()
    A02.write_tools()
    A04.write_tools()
    A05.write_tools()
    A03.check_tools03()
    after = hashlib.sha256(TOOLS_PATH.read_bytes()).hexdigest()
    print("guard check: before", before[:12], "after", after[:12], "same", before == after)
    assert before == after


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["langchain==1.4.0", "langchain-openai==1.6.0", "python-dotenv==1.2.3"])

IMPORTS = r'''# 실험 번호를 만들 모듈 uuid와 모델 객체를 만들 함수, 도구 파일의 함수 아홉을 가져옵니다
import uuid
from langchain.chat_models import init_chat_model
# 01·03·05절과 Ch 6 06절·Ch 16 04절에서 배운 함수는 도구 파일에서 가져옵니다(이름의 알파벳 차례)
from cost_tools import choose_model, cost_row, estimate_cost, make_budget, make_request
from cost_tools import make_usage, send_inquiry, total_cost, try_reserve

print("가져온 이름:", "uuid, init_chat_model")
print("도구 파일에서 가져온 함수:", choose_model.__name__, cost_row.__name__, estimate_cost.__name__)
print("도구 파일에서 가져온 함수:", make_budget.__name__, make_request.__name__, make_usage.__name__)
print("도구 파일에서 가져온 함수:", send_inquiry.__name__, total_cost.__name__, try_reserve.__name__)'''

NANO = A03.NANO
MINI = A03.MINI
MODELS = A03.MODELS

PRICES = r'''# 두 모델의 공식 요금(100만 토큰당 달러)과 확인한 날짜를 적고, 모델 이름으로 찾게 모읍니다
pricing_date = "2026-09-30"
nano_prices = {"ordinary_input": 0.20, "cached_input": 0.02, "output": 1.25}
mini_prices = {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}
price_tables = {"gpt-5.4-nano": nano_prices, "gpt-5.4-mini": mini_prices}
print("요금 확인 날짜:", pricing_date)
print("nano 요금:", nano_prices)
print("mini 요금:", mini_prices)'''

POLICY = A01.POLICY
INQUIRIES = A03.INQUIRIES

RULE = r'''# 문의 글 뒤에 붙일 답 형식 글을 정합니다(03절과 같은 글입니다)
answer_rule = "이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요."
print("답 형식 글:", answer_rule)
print("답 형식 글의 글자 수:", len(answer_rule))'''

AMOUNTS = r'''# 요청 전에 정한 토큰 수로 사용량 딕셔너리를 만들고, 모델마다 대화 하나의 예약 금액을 셉니다
planned_input = 3200
planned_cached = 0
planned_output = 20
planned_usage = make_usage(planned_input, planned_cached, planned_output)
nano_amount = estimate_cost(planned_usage, nano_prices["ordinary_input"], nano_prices["cached_input"], nano_prices["output"])
mini_amount = estimate_cost(planned_usage, mini_prices["ordinary_input"], mini_prices["cached_input"], mini_prices["output"])
amounts = {"gpt-5.4-nano": round(nano_amount, 6), "gpt-5.4-mini": round(mini_amount, 6)}
print("정한 사용량:", planned_usage)
print("모델마다 예약 금액(달러):", amounts)'''

CAP = r'''# 두 실행에 같게 쓸 비용 상한과 호출 한도를 정합니다(대화 하나에 요청 한 번이라, 호출 한도는 대화 수로 둡니다)
cost_cap = 0.006
max_calls = len(inquiries)
print("비용 상한(달러):", cost_cap)
print("호출 한도:", max_calls)'''

DEF_ANSWER = r'''# 응답 하나의 대화 번호·응답한 모델·답·정답 종류와 같은가·토큰 수를 한 줄로 출력하고, 정답 종류와 같은지를 내놓습니다
def print_answer(number, response, expected_type):
    usage = response.usage_metadata
    cache_read = usage["input_token_details"]["cache_read"]
    matched = response.text == expected_type
    print(number, "|", response.response_metadata["model_name"], "|", response.text, "|", matched, "|", usage["input_tokens"], "|", cache_read)
    return matched'''

ROUTE1 = r'''# 실행 1: 기준 길이를 30으로 두고, 문의마다 모델 라우터가 고른 이름을 모읍니다(요청 없음)
run1_limit = 30
run1_models = []
for inquiry in inquiries:
    run1_models.append(choose_model(inquiry, run1_limit))
print("기준 길이:", run1_limit)
print("모델 배정:", run1_models)'''

RESERVE1 = r'''# 실행 1: 대화마다 고른 모델의 예약 금액을 먼저 예약해 봅니다(요청 없음)
run1_budget = make_budget(max_calls, cost_cap)
run1_results = []
for number in range(len(inquiries)):
    model_name = run1_models[number]
    run1_results.append(try_reserve(run1_budget, amounts[model_name]))
print("예약 결과:", run1_results)
print("받은 대화 수:", run1_results.count("예약됨"))
print("예약한 금액의 합(달러):", round(run1_budget["cost_usd"], 6))'''

SHAPE1 = r'''# 실행 1에서만 쓸 실험 번호를 만들고, 대화 1로 보낼 요청 글의 모양을 봅니다(번호는 글자 수만 출력합니다)
run1_mark = "실험 번호 " + uuid.uuid4().hex
first_request = make_request(run1_mark, policy_text, inquiries[0]) + " " + answer_rule
print("실험 번호의 글자 수:", len(run1_mark))
print("요청 글 1의 글자 수:", len(first_request))
print("정책 글이 시작하는 자리:", first_request.find(policy_text))'''

SEND1 = r'''# 실행 1: 예약된 대화만 실험 번호와 정책 글을 앞에 붙여, 고른 모델로 하나씩 보냅니다(모델 요청 3번)
run1_sent = []
run1_responses = []
for number in range(len(inquiries)):
    if run1_results[number] == "예약됨":
        question = make_request(run1_mark, policy_text, inquiries[number])
        run1_responses.append(send_inquiry(question, run1_models[number], models, answer_rule))
        run1_sent.append(number)
print("보낸 요청 수:", len(run1_responses))'''

ANSWERS1 = r'''# 실행 1에서 보낸 대화마다 응답을 한 줄씩 보고, 정답 종류와 같은 답을 셉니다(요청 없음)
print("대화 | 응답한 모델 | 답 | 정답 종류와 같은가 | 입력 토큰 | 캐시 입력 토큰")
run1_matched = 0
for index in range(len(run1_sent)):
    number = run1_sent[index]
    matched = print_answer(number + 1, run1_responses[index], expected_types[number])
    if matched:
        run1_matched = run1_matched + 1
print("정답 종류와 같은 답 수:", run1_matched)'''

COSTS1 = r'''# 실행 1에서 보낸 대화마다 할인을 넣은 비용과 할인 없이 센 비용을 보고, 예약 합과 비용 합을 견줍니다(요청 없음)
print("대화 | 할인을 넣은 비용 | 할인 없이 센 비용 | 두 값이 같은가")
run1_costs = []
for index in range(len(run1_sent)):
    number = run1_sent[index]
    label = "대화 " + str(number + 1)
    run1_costs.append(cost_row(label, run1_responses[index].usage_metadata, price_tables[run1_models[number]]))
print("예약한 금액의 합(달러):", round(run1_budget["cost_usd"], 6))
print("받은 대화의 대화당 비용 합(달러):", total_cost(run1_costs))'''

ROUTE2 = r'''# 실행 2: 기준 길이 하나만 0으로 바꾸고, 모델 배정을 다시 만듭니다(요청 없음)
run2_limit = 0
run2_models = []
for inquiry in inquiries:
    run2_models.append(choose_model(inquiry, run2_limit))
print("기준 길이:", run2_limit)
print("모델 배정:", run2_models)'''

RESERVE2 = r'''# 실행 2: 새 예산에 대화마다 고른 모델의 예약 금액을 먼저 예약해 봅니다(요청 없음)
run2_budget = make_budget(max_calls, cost_cap)
run2_results = []
for number in range(len(inquiries)):
    model_name = run2_models[number]
    run2_results.append(try_reserve(run2_budget, amounts[model_name]))
print("예약 결과:", run2_results)
print("받은 대화 수:", run2_results.count("예약됨"))
print("예약한 금액의 합(달러):", round(run2_budget["cost_usd"], 6))'''

SEND2 = r'''# 실행 2: 새 실험 번호를 만들고, 예약된 대화만 같은 방법으로 보냅니다(모델 요청 2번)
run2_mark = "실험 번호 " + uuid.uuid4().hex
run2_sent = []
run2_responses = []
for number in range(len(inquiries)):
    if run2_results[number] == "예약됨":
        question = make_request(run2_mark, policy_text, inquiries[number])
        run2_responses.append(send_inquiry(question, run2_models[number], models, answer_rule))
        run2_sent.append(number)
print("보낸 요청 수:", len(run2_responses))'''

ANSWERS2 = r'''# 실행 2에서 보낸 대화마다 응답을 한 줄씩 보고, 정답 종류와 같은 답을 셉니다(요청 없음)
print("대화 | 응답한 모델 | 답 | 정답 종류와 같은가 | 입력 토큰 | 캐시 입력 토큰")
run2_matched = 0
for index in range(len(run2_sent)):
    number = run2_sent[index]
    matched = print_answer(number + 1, run2_responses[index], expected_types[number])
    if matched:
        run2_matched = run2_matched + 1
print("정답 종류와 같은 답 수:", run2_matched)'''

COSTS2 = r'''# 실행 2에서 보낸 대화마다 할인을 넣은 비용과 할인 없이 센 비용을 보고, 예약 합과 비용 합을 견줍니다(요청 없음)
print("대화 | 할인을 넣은 비용 | 할인 없이 센 비용 | 두 값이 같은가")
run2_costs = []
for index in range(len(run2_sent)):
    number = run2_sent[index]
    label = "대화 " + str(number + 1)
    run2_costs.append(cost_row(label, run2_responses[index].usage_metadata, price_tables[run2_models[number]]))
print("예약한 금액의 합(달러):", round(run2_budget["cost_usd"], 6))
print("받은 대화의 대화당 비용 합(달러):", total_cost(run2_costs))'''

SUMMARY = r'''# 두 실행을 한 표로 모읍니다(요청 없음)
print("실행 | 기준 길이 | 받은 대화 | 막힌 대화 | 보낸 요청 | 정답 종류와 같은 답 | 대화당 비용 합(달러)")
run1_blocked = run1_results.count("비용 상한을 넘습니다.")
run2_blocked = run2_results.count("비용 상한을 넘습니다.")
print("실행 1 |", run1_limit, "|", run1_results.count("예약됨"), "|", run1_blocked, "|", len(run1_responses), "|", run1_matched, "|", total_cost(run1_costs))
print("실행 2 |", run2_limit, "|", run2_results.count("예약됨"), "|", run2_blocked, "|", len(run2_responses), "|", run2_matched, "|", total_cost(run2_costs))'''

SAME_CONV = r'''# 두 실행에서 모두 받은 대화마다 두 실행의 모델과 대화당 비용을 견줍니다(요청 없음)
print("대화 | 실행 1 모델 | 실행 2 모델 | 실행 1의 비용이 더 적은가")
for index in range(len(run2_sent)):
    number = run2_sent[index]
    # 메서드 index는 목록에서 그 값이 처음 나오는 자리를 0부터 세어 내놓습니다
    run1_cost = run1_costs[run1_sent.index(number)]
    print(number + 1, "|", run1_models[number], "|", run2_models[number], "|", run1_cost < run2_costs[index])'''

CODE_CELLS = [INSTALL, IMPORTS, KEY, NANO, MINI, MODELS, PRICES, POLICY, INQUIRIES, RULE, AMOUNTS, CAP, DEF_ANSWER,
              ROUTE1, RESERVE1, SHAPE1, SEND1, ANSWERS1, COSTS1,
              ROUTE2, RESERVE2, SEND2, ANSWERS2, COSTS2, SUMMARY, SAME_CONV]
# 모델 요청이 나가는 셀과, 그 응답을 읽는 셀(설계 확인에서 빼는 셀)
MODEL_CELLS = [SEND1, ANSWERS1, COSTS1, SEND2, ANSWERS2, COSTS2, SUMMARY, SAME_CONV]

# 본문·결과 읽기 첫 단락에 쓴 매번 같은 값(--design-check가 출력에 있는지 본다)
EXPECTED = [
    "모델 이름: gpt-5.4-nano", "모델 이름: gpt-5.4-mini", "temperature: 0.0",
    "고를 수 있는 모델: ['gpt-5.4-nano', 'gpt-5.4-mini']", "요금 확인 날짜: 2026-09-30",
    "nano 요금: {'ordinary_input': 0.2, 'cached_input': 0.02, 'output': 1.25}",
    "mini 요금: {'ordinary_input': 0.75, 'cached_input': 0.075, 'output': 4.5}",
    "규칙 문장의 글자 수: 60", "정책 글의 글자 수: 6000", "문의 글 수: 3", "정답 종류: ['배송', '환불', '결제']",
    "답 형식 글의 글자 수: 36",
    "정한 사용량: {'input_tokens': 3200, 'output_tokens': 20, 'input_token_details': {'cache_read': 0}}",
    "모델마다 예약 금액(달러): {'gpt-5.4-nano': 0.000665, 'gpt-5.4-mini': 0.00249}",
    "비용 상한(달러): 0.006", "호출 한도: 3",
    "기준 길이: 30", "모델 배정: ['gpt-5.4-nano', 'gpt-5.4-nano', 'gpt-5.4-mini']",
    "예약 결과: ['예약됨', '예약됨', '예약됨']", "받은 대화 수: 3", "예약한 금액의 합(달러): 0.00382",
    "실험 번호의 글자 수: 38", "요청 글 1의 글자 수: 6097", "정책 글이 시작하는 자리: 39",
    "기준 길이: 0", "모델 배정: ['gpt-5.4-mini', 'gpt-5.4-mini', 'gpt-5.4-mini']",
    "예약 결과: ['예약됨', '예약됨', '비용 상한을 넘습니다.']", "받은 대화 수: 2", "예약한 금액의 합(달러): 0.00498",
]


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/06-figures.md)
FIG1 = "06-1-세-절의-기능을-이은-조립도"
FIG1_ALT = "위에서 아래로 읽는 조립도입니다. 맨 위 초록 상자 문의 셋 20 25 36글자에서 파란 상자 choose_model 03절 모델 라우터 기준 길이와 글자 수를 견줌으로 갑니다. 이어서 파란 상자 try_reserve 05절 예산 가드 모델마다 예약 금액 비용 상한 0.006으로 갑니다. 여기서 점선 둘이 갈라져, 예약이 막힘은 왼쪽 회색 상자 막힌 대화 요청을 보내지 않음으로, 예약됨은 오른쪽 파란 상자 make_request send_inquiry 01절 실험 번호와 정책 글 6000자를 앞에로 갑니다. 그 아래 보라 상자 gpt-5.4-nano 또는 gpt-5.4-mini temperature=0 reasoning_effort none을 지나, 맨 아래 파란 상자 cost_row total_cost 캐시 입력 할인을 넣은 예상 비용에 이르는 그림"
FIG1_CAP = "문의 하나마다 모델 라우터가 모델을 고르고, 예산 가드가 예약한 뒤에만 정책 글을 앞에 붙여 요청을 보냅니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 셀에 적은 문의 셋이고, 파란 상자는 01·03·05절에서 배운 함수입니다.
점선 둘은 예산 가드의 두 갈래입니다.
왼쪽 회색 상자는 막힌 대화가 요청을 보내지 않는다는, 코드 차례로 정해지는 사실입니다.
보라 상자는 이 절에서 실제로 부른 두 모델이고, 맨 아래 상자에서 응답의 사용량으로 대화당 비용을 셉니다."""

FIG2 = "06-2-실행-1의-실제-차례"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 기준 길이 30에서 노란 상자 모델 배정 nano nano mini, 노란 상자 예약됨 셋 예약 합 0.00382 비용 상한 0.006 안으로 이어집니다. 여기서 두 갈래로 나뉘어 왼쪽 보라 상자 gpt-5.4-nano 요청 1 대화 1 요청 2 대화 2와 오른쪽 보라 상자 gpt-5.4-mini 요청 3 대화 3으로 가고, 두 상자는 노란 상자 보낸 요청 세 번 대화 1 캐시 입력 0으로 모입니다. 맨 아래 노란 상자는 받은 대화의 비용 합 예약 합보다 적음인 그림"
FIG2_CAP = "기준 길이 30에서는 문의 셋이 모두 예약되어 nano에 두 번, mini에 한 번 요청이 나갔습니다."
FIG2_READ = """위에서 아래로 읽습니다.
초록 상자는 실행 1에서 셀에 적은 기준 길이이고, 노란 상자는 노트북 3절에서 출력으로 확인한 값입니다.
보라 상자 둘은 실제로 부른 두 모델과, 그 모델로 보낸 요청의 차례입니다.
맨 아래 노란 상자는 흔들림 확인 다섯 번과 새 커널 두 번에서 모두 같았던 부등식입니다.
대화 2의 캐시 입력은 실행에 따라 달라, 그림에 넣지 않았습니다."""

FIG3 = "06-3-기준-길이만-바꾼-두-실행"
FIG3_ALT = "맨 위 회색 상자 두 실행 공통 문의 셋 정책 글 6000자 예약 금액 nano 0.000665 예약 금액 mini 0.00249 비용 상한 0.006 아래에 칸 둘이 나란히 있습니다. 왼쪽 칸 실행 1 기준 길이 30에는 초록 상자 기준 길이 30에서 노란 상자 모델 배정 nano nano mini 예약됨 셋 예약 합 0.00382, 노란 상자 받은 대화 셋 막힌 대화 없음 보낸 요청 세 번으로 이어집니다. 오른쪽 칸 실행 2 값 하나만 바꿈에는 파란 상자 기준 길이 0에서 노란 상자 모델 배정 mini mini mini 예약됨 둘 예약 합 0.00498, 노란 상자 대화 3 막힘 받은 대화 둘 보낸 요청 두 번으로 이어지는 그림"
FIG3_CAP = "기준 길이를 0으로 내리자 mini 셋의 예약이 비용 상한을 넘어, 대화 3이 막히고 요청은 두 번만 나갔습니다."
FIG3_READ = """맨 위 회색 상자는 두 실행에 공통인 값입니다.
왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 칸마다 위가 기준 길이, 아래가 노트북 3·4절의 출력입니다.
오른쪽 칸의 파란 상자가 바꾼 값입니다.
노란 상자의 값은 코드와 정한 값으로 정해져, 흔들림 확인 다섯 번과 새 커널 두 번에서 모두 같았습니다."""

ILLU = "06-4-모듈-셋을-이은-충전대"
ILLU_ALT = "흰 바탕에 긴 충전대 하나가 화면을 가로지릅니다. 충전대는 네모 모듈 셋을 한 줄로 붙이고 은색 걸쇠 둘로 이은 것입니다. 모듈은 왼쪽부터 세이지 초록, 연보라, 복숭아색입니다. 왼쪽과 가운데 모듈의 윗면 칸에는 작은 크림색 배터리가 하나씩, 오른쪽 모듈의 큰 칸에는 큰 크림색 배터리 하나가 꽂혀 있습니다. 모듈 앞면마다 큰 둥근 초록 불이 하나씩 켜져 있습니다. 사람·글자·숫자·화살표·전선은 없는 그림"
ILLU_CAP = "색이 다른 모듈 셋을 걸쇠로 이은 충전대에 작은 배터리 둘과 큰 배터리 하나가 꽂혀, 불 셋이 모두 켜져 있습니다."
ILLU_READ = "색이 다른 모듈 셋이 은색 걸쇠 둘로 이어져, 충전대 하나가 되었습니다. 왼쪽과 가운데 모듈에는 작은 배터리가 하나씩, 오른쪽 모듈에는 큰 배터리가 하나 꽂혀 있습니다. 모듈 앞면의 초록 불은 셋 모두 켜져 있습니다. 작은 배터리 둘과 큰 배터리 하나는, 실행 1의 모델 배정 nano 둘·mini 하나와 같은 나뉨입니다. 배터리의 크기는 요금 값과 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 01·03·05절에서 쓴 기능을 책 가게 문의 셋의 흐름 하나로 잇습니다.
2. 기준 길이 30으로 문의 셋을 예약하고 보내, 답과 대화당 비용을 봅니다.
3. 기준 길이 하나만 0으로 바꿔 다시 실행하고, 받은 대화와 포기한 것을 견줍니다.

**준비물** — 이 노트북은 실제 모델에 요청을 다섯 번 보냅니다.
실행 1에서 세 번, 실행 2에서 두 번입니다.
모델별로는 `gpt-5.4-nano`에 두 번, `gpt-5.4-mini`에 세 번입니다.
프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
키가 없으면 키를 확인하는 셀에서 멈추고, 모델 요청은 나가지 않습니다.

요청마다 6,000자 정책 글을 앞에 붙여 보내, 요청 하나가 약 3,200토큰입니다.
요금표(2026-09-30 확인)로 어림한 비용은 다섯 번을 합쳐 약 0.006달러입니다.
청구 금액이 아니라, 교재를 만들 때 본 사용량으로 어림한 값입니다.
실행마다 답 글과 토큰 수가 달라질 수 있습니다.
교재를 만들 때 같은 요청 다섯을 노트북 밖에서 다섯 번 더 보내 보았고, 이를 흔들림 확인이라고 부릅니다.

실습 폴더의 도구 파일 `cost_tools.py`에서 함수 아홉을 가져옵니다.
이 노트북은 파일을 쓰지 않습니다.
걸린 시간은 재지 않았습니다.

**기준 버전** — 첫 셀에서 패키지 셋을 설치합니다.
버전은 langchain 1.4.0, langchain-openai 1.6.0, python-dotenv 1.2.3입니다.
셋 모두 실습 폴더 잠금과 같은 버전입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 버전과 Windows·macOS에서는 실행하지 않았습니다.

**실습 범위** — 이 절은 이 챕터 끝의 실습 절입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
실습 시간 30분 안팎에 맞춘 분량입니다.

실습 폴더 `labs/part7/ch34-cost-rate-limits`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md(r"""## 1. 준비

이 절은 이 챕터의 실습 절입니다.
01·03·05절에서 쓴 기능을 책 가게 문의 셋의 흐름 하나로 이어 실행합니다.
새 문법과 새 라이브러리 함수는 넣지 않고, 결과를 보는 함수 하나만 이 절에서 만듭니다.

제목의 Rate Limit은 04절에서 본 요청 제한(rate limit)입니다.
이 실습은 요청 제한에 닿는 장면을 만들지 않고, 비용 쪽 기능을 한 흐름으로 잇습니다.

첫 셀은 패키지 셋을 설치하고 설치된 버전을 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md(r"""**결과 읽기** — 출력 줄 `langchain: 1.4.0`과 `langchain-openai: 1.6.0`이 보입니다.
세 패키지 모두 01·03절과 같은 버전입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `uuid`는 01절에서 실험 번호를 만들 때 쓴 모듈입니다.
앞에서 배운 함수 아홉은 도구 파일 `cost_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md(r"""**결과 읽기** — 출력 줄 `가져온 이름: uuid, init_chat_model`이 보입니다.
라벨 `도구 파일에서 가져온 함수:` 뒤에 함수 아홉이 세 줄로 나뉘어 보입니다.

함수 `make_request`·`cost_row`는 01절, `choose_model`·`send_inquiry`는 03절에서 배웠습니다.
함수 `make_usage`·`total_cost`·`try_reserve`는 05절에서 배웠습니다.
이 일곱 함수는 이 절에서 도구 파일에 옮겼고, 설명 줄과 본문은 앞 절 셀과 글자까지 같습니다.
나머지 둘 가운데 `estimate_cost`는 Ch 6 06절, `make_budget`은 Ch 16 04절에서 배웠습니다.

앞에서 배운 함수는 `cost_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

다음 셀은 `.env` 파일에서 API 키를 읽고, 키가 있는지만 출력합니다."""),
        setup(KEY),
        md(r"""**결과 읽기** — 출력 줄 `OPENAI_API_KEY 설정 여부: True`가 보입니다.
키 값은 출력하지 않고, 있는지만 봅니다.
키가 없으면 이 셀의 `assert`가 멈추고, 뒤 셀의 모델 요청도 나가지 않습니다.

다음 두 셀은 03절과 같은 두 모델을 과정 표준 설정으로 준비합니다.
먼저 작은 모델 `gpt-5.4-nano`입니다.
객체를 만들 때는 모델 요청이 나가지 않습니다."""),
        code(NANO),
        md(r"""**결과 읽기** — 모델 이름 `gpt-5.4-nano`, temperature `0.0`이 보입니다.
03절 노트북의 셀과 글자까지 같은 셀입니다.

다음 셀은 과정 표준 모델 `gpt-5.4-mini`를 같은 설정으로 준비합니다."""),
        code(MINI),
        md(r"""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + r"""에 이 두 모델로 실행한 결과입니다.
온도 값을 0으로 두어도 모델의 답이 매번 같다고 할 수는 없습니다.
인자 `reasoning_effort="none"`은 모델이 답하기 전에 따로 생각하는 단계를 쓰지 않게 합니다.

## 2. 오늘의 상황과 재료

책 가게 상담 서비스에 문의 셋이 차례로 옵니다.
문의마다 긴 정책 글을 앞에 붙여, 모델에 문의의 종류를 묻습니다.
이 절에서는 문의 하나를 대화 하나로 보고, 대화마다 요청을 한 번 보냅니다.
목표는 대화당 비용을 줄이는 것이고, 그 대신 무엇을 포기했는지도 함께 적습니다.

흐름은 네 단계입니다.
03절 모델 라우터가 보낼 모델을 고르고, 05절 예산 가드가 요청 전에 예약합니다.
예약된 대화만 01절처럼 실험 번호와 정책 글을 앞에 붙여 보냅니다.
끝으로 응답의 사용량으로 캐시 입력 할인을 넣은 예상 비용을 셉니다.

다음 셀은 03절과 같은 셀로, 모델 이름과 모델 객체를 딕셔너리에 담습니다.
모델 라우터가 고른 이름으로 모델 객체를 찾을 때 씁니다."""),
        code(MODELS),
        md(r"""**결과 읽기** — 출력 줄 `고를 수 있는 모델: ['gpt-5.4-nano', 'gpt-5.4-mini']`가 보입니다.
키는 모델 라우터가 내놓는 이름이고, 값은 1절에서 만든 모델 객체입니다.

다음 셀은 두 모델의 요금표를 적습니다.
값은 03절 셀과 같고, 확인한 날짜만 이 절에서 다시 본 날로 적었습니다."""),
        code(PRICES),
        md(r"""**결과 읽기** — 출력 줄 `요금 확인 날짜: 2026-09-30`이 보입니다.
단위는 100만 토큰당 달러이고, 세 값 모두 nano가 mini보다 작습니다.
두 모델 모두 캐시 입력 요금이 일반 입력 요금의 10분의 1입니다.

다음 셀은 01절과 같은 셀로, 요청마다 똑같이 보낼 긴 정책 글을 만듭니다.
여러 요청이 첫 글자부터 똑같이 보내는 부분을 01절에서는 공통 앞부분이라고 불렀습니다.
이 절에서는 실험 번호와 정책 글이 공통 앞부분이 됩니다."""),
        code(POLICY),
        md(r"""**결과 읽기** — 출력 줄 `정책 글의 글자 수: 6000`이 보입니다.
규칙 문장 `60`글자를 100번 이어 붙였습니다.
01절에서는 이 정책 글을 앞에 둔 둘째 요청에 캐시 입력이 생겼습니다.

다음 셀은 03절과 같은 셀로, 문의 글 셋과 정답 종류를 같은 차례로 적습니다.
문의마다 맞는 종류를 03절에서는 정답 종류라고 불렀습니다."""),
        code(INQUIRIES),
        md(r"""**결과 읽기** — 출력 줄 `정답 종류: ['배송', '환불', '결제']`가 보입니다.
세 문의 글은 차례대로 20·25·36글자입니다.
모델 라우터는 이 글자 수만 보고 모델을 고릅니다.

다음 셀은 문의 글 뒤에 붙일 답 형식 글을 정합니다.
03절과 같은 글이고, 03절 함수 `send_inquiry`가 문의 글 뒤에 공백과 함께 붙입니다."""),
        code(RULE),
        md(r"""**결과 읽기** — 출력 줄 `답 형식 글의 글자 수: 36`이 보입니다.
한 낱말로 답하게 해서, 출력 토큰이 적게 나오게 했습니다.

다음 셀은 대화 하나를 받기 전에 예약할 금액을 모델마다 셉니다.
05절에서는 대화 하나를 받기 전에 예산에 적는 예상 비용을 예약 금액이라고 불렀습니다.
요청 전에는 사용량을 모르므로, 토큰 수를 정해 05절 함수 `make_usage`로 사용량을 만듭니다.
입력 3,200토큰은 01절 교재 출력의 입력 토큰 수보다 조금 크게 정한 값입니다.
캐시 입력은 생길지 모르므로 0으로, 출력은 한 낱말 답이라 넉넉히 20토큰으로 두었습니다."""),
        code(AMOUNTS),
        md(r"""**결과 읽기** — 출력 줄 `모델마다 예약 금액(달러): {'gpt-5.4-nano': 0.000665, 'gpt-5.4-mini': 0.00249}`가 보입니다.
모델 nano의 예약 금액은 (3200 × 0.2 + 20 × 1.25) ÷ 1000000 = 0.000665달러입니다.
모델 mini의 예약 금액은 같은 토큰 수에 mini 요금을 곱해 0.00249달러입니다.
두 값은 정한 토큰 수와 요금표로만 정해져, 실행할 때마다 같습니다.

다음 셀은 두 실행에 같게 쓸 비용 상한과 호출 한도를 정합니다.
비용 상한 0.006달러는 실행 전에 이 절에서 정한 값입니다.
모델 nano 둘과 mini 하나의 예약 합은 들어가고, mini 셋의 예약 합은 넘도록 골랐습니다.
이 절은 05절처럼 대화마다 한 번 예약하고, 호출 한도는 대화 수와 같게 둡니다."""),
        code(CAP),
        md(r"""**결과 읽기** — 출력 줄 `비용 상한(달러): 0.006`과 `호출 한도: 3`이 보입니다.
호출 한도가 대화 수와 같아, 이 절에서 호출 한도에 막히는 대화는 없습니다.
막는 일은 05절처럼 비용 상한만 합니다.

Ch 16 04절은 요청마다 예약했고, 05절은 대화마다 예약했습니다.
이 절은 대화 하나에 요청 한 번이라, 예산 칸 `calls`는 받은 대화 수이자 보낸 요청 수가 됩니다.

다음 셀은 결과를 볼 함수를 정의합니다.
응답 하나의 대화 번호·응답한 모델·답·정답 종류와 같은지·토큰 수를 한 줄로 출력합니다.
캐시 입력 토큰 수는 01절에서 본 사용량 칸 `cache_read`의 값입니다.
함수는 답이 정답 종류와 같은지를 내놓아, 뒤 셀에서 같은 답의 수를 셉니다."""),
        code(DEF_ANSWER),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
응답한 모델의 이름은 03절처럼 `response_metadata`에서 꺼냅니다.
답은 연산자 `==`로 정답 종류와 글자까지 견줍니다.
이 절에서 새로 만드는 함수는 이것 하나입니다.

**가설** — 실행 1은 기준 길이를 30으로 두어, 03절 실행 1처럼 nano·nano·mini로 보냅니다.
예약 합은 0.000665 + 0.000665 + 0.00249 = 0.00382달러라, 셋을 모두 받을 것입니다.
nano 둘째 요청은 같은 번호와 정책 글 뒤에 오므로, 01절처럼 캐시 입력이 생길 것입니다.
대화 3은 그 실행에서 mini로 보내는 첫 요청이라, 캐시 입력이 없을 것입니다.

## 3. 실행 1 — 기준 길이 30

다음 셀은 기준 길이를 30으로 두고, 문의마다 모델 라우터가 고른 이름을 모읍니다.
03절에서 본 대로, 모델 라우터는 Ch 26 03절의 라우터와 달리 모델 이름만 고릅니다.
이 셀에서는 모델 요청이 나가지 않습니다."""),
        code(ROUTE1),
        md(r"""**결과 읽기** — 출력 줄 `모델 배정: ['gpt-5.4-nano', 'gpt-5.4-nano', 'gpt-5.4-mini']`이 보입니다.
03절 실행 1과 같은 모델 배정입니다.
36글자인 대화 3만 기준 길이 30보다 길어 mini로 갑니다.

다음 셀은 대화마다 고른 모델의 예약 금액을 예산에 먼저 예약해 봅니다.
05절 함수 `try_reserve`는 예약이 되면 「예약됨」을, 막히면 받은 오류의 글을 내놓습니다.
05절에서는 예약이 된 대화를 받은 대화, 예약이 막힌 대화를 막힌 대화라고 불렀습니다.
이 셀에서도 모델 요청은 나가지 않습니다."""),
        code(RESERVE1),
        md(r"""**결과 읽기** — 출력 줄 `예약 결과: ['예약됨', '예약됨', '예약됨']`과 `받은 대화 수: 3`이 보입니다.
예약한 금액의 합은 `0.00382`달러로, 비용 상한 0.006달러 안입니다.
이 절은 예약 결과를 먼저 모두 만든 뒤, 받은 대화만 보냅니다.
예산은 예약 금액으로만 바뀌어, 대화마다 예약 직후 보내도 받는 대화는 같습니다.

다음 셀은 실행 1에서만 쓸 실험 번호를 만들고, 대화 1로 보낼 요청 글의 모양을 봅니다.
실험 번호는 01절에서, 앞 실행이 남긴 앞부분과 맞지 않게 요청 글 맨 앞에 둔 무작위 글입니다.
실행 2에서는 번호를 새로 만들어, 실행 1이 남긴 앞부분과도 맞지 않게 합니다."""),
        code(SHAPE1),
        md(r"""**결과 읽기** — 출력 줄 `요청 글 1의 글자 수: 6097`과 `정책 글이 시작하는 자리: 39`가 보입니다.
실험 번호 `38`글자와 줄바꿈 하나 뒤에 정책 글이 시작합니다.
정책 글 뒤에는 줄바꿈, 문의 글, 공백, 답 형식 글이 옵니다.
01절 요청 글 1과 글자 수와 모양이 같고, 실험 번호만 다릅니다.

다음 셀은 받은 대화만 차례로 보냅니다.
함수 `make_request`가 실험 번호·정책 글·문의 글을 줄바꿈으로 잇습니다.
함수 `send_inquiry`는 그 글 뒤에 공백과 답 형식 글을 붙여, 고른 모델로 보냅니다.
이 셀에서 모델 요청이 세 번 나갑니다."""),
        code(SEND1),
        md(r"""**결과 읽기** — 출력 줄 `보낸 요청 수: 3`이 보입니다.
받은 대화 셋을 모두 보냈습니다.

목록 `run1_sent`에는 보낸 대화의 차례 번호를 0부터 세어 담았습니다.

다음 셀은 보낸 대화마다 응답을 한 줄씩 보고, 정답 종류와 같은 답을 셉니다.
각 줄의 마지막 칸이 캐시 입력 토큰 수입니다."""),
        code(ANSWERS1),
        md(r"""**결과 읽기** — 라벨 줄 아래 세 줄에서, 응답한 모델 이름이 모델 배정의 이름으로 시작합니다.
대화 1·2는 `gpt-5.4-nano-2026-03-17`, 대화 3은 `gpt-5.4-mini-2026-03-17`이 답했습니다.
대화 1은 새 실험 번호로 보낸 첫 요청이라, 캐시 입력 토큰 수가 0입니다.
흔들림 확인 다섯 번과 새 커널 두 번에서 모두, 대화 3의 캐시 입력은 0이었고 세 답은 정답 종류와 같았습니다.
대화 3은 그 실행에서 mini로 보낸 첫 요청입니다.

교재 출력에서는 답이 차례대로 `배송`, `환불`, `결제`입니다.
입력 토큰 수는 `3164`·`3168`·`3168`토큰이고, 대화 2의 캐시 입력 토큰 수는 `2816`토큰입니다.
흔들림 확인 다섯 번에서도 대화 2에는 캐시 입력이 생겼습니다.
그러나 새 커널로 한 번 더 실행했을 때는 대화 2의 캐시 입력이 0이었습니다.
같은 앞부분을 보내도, 캐시 입력이 생기는지는 실행한 때에 따라 달라질 수 있습니다.

다음 셀은 보낸 대화마다 캐시 입력 할인을 넣은 비용과 할인 없이 센 비용을 봅니다.
01절 함수 `cost_row`가 한 줄씩 출력하고, 할인을 넣은 값을 내놓습니다.
요금표는 그 대화를 받은 모델의 것을 씁니다.
끝에서 예약한 금액의 합과 받은 대화의 비용 합을 견줍니다."""),
        code(COSTS1),
        md(r"""**결과 읽기** — 라벨 줄 아래 세 줄이 대화마다의 예상 비용입니다.
대화 1·3은 캐시 입력이 없어, 두 값이 같은지를 보는 마지막 칸이 `True`입니다.
출력 줄 `예약한 금액의 합(달러): 0.00382`는 예약 셀과 같은 값입니다.
흔들림 확인 다섯 번과 새 커널 두 번에서 모두, 받은 대화의 비용 합이 예약한 금액의 합보다 적었습니다.

교재 출력에서는 대화당 비용이 `0.000638`·`0.000133`·`0.002399`달러입니다.
대화 2는 캐시 입력이 있어 할인을 넣은 값이 작고, 할인 없이 세면 `0.00064`달러입니다.
캐시 입력이 없는 실행이라면, 대화 2의 비용은 할인 없이 센 값과 같아집니다.
받은 대화의 대화당 비용 합은 `0.003169`달러입니다.
예약은 입력 3,200·출력 20토큰으로 넉넉히 잡고 캐시 입력 할인도 넣지 않아, 비용 합이 예약 합보다 작게 나왔습니다.

## 4. 실행 2 — 기준 길이 0

실행 2는 값 하나만 바꿉니다.
바꾸는 값은 기준 길이이고, 30에서 0으로 내립니다.
03절 실행 2와 같은 값이라, 모든 문의가 mini로 갑니다.
정책 글·문의 글·예약 금액·비용 상한·호출 한도는 실행 1과 같습니다.

**가설** — 예약 금액 0.00249달러를 세 번 예약하면 0.00747달러라, 비용 상한 0.006달러를 넘습니다.
그래서 두 번까지만 예약되고, 대화 3은 막힐 것입니다.
막힌 대화는 요청을 보내지 않으므로, 요청은 두 번만 나갈 것입니다.

다음 셀은 기준 길이 하나만 0으로 바꾸고, 모델 배정을 다시 만듭니다."""),
        code(ROUTE2),
        md(r"""**결과 읽기** — 출력 줄 `모델 배정: ['gpt-5.4-mini', 'gpt-5.4-mini', 'gpt-5.4-mini']`이 보입니다.
빈 글이 아닌 문의는 모두 0글자보다 길어서 mini로 갑니다.
실행 1과 견주면 대화 1·2만 nano에서 mini로 바뀌었습니다.

다음 셀은 새 예산을 만들고, 대화마다 예약 금액을 예약해 봅니다.
실행 1에서 예약한 양이 섞이지 않게, 예산은 새로 만듭니다."""),
        code(RESERVE2),
        md(r"""**결과 읽기** — 출력 줄 `예약 결과: ['예약됨', '예약됨', '비용 상한을 넘습니다.']`가 보입니다.
두 번 예약한 합 `0.00498`달러에 0.00249를 더하면 0.00747달러라, 대화 3이 막혔습니다.
같은 비용 상한인데, 실행 1은 셋을 받았고 실행 2는 둘만 받았습니다.

다음 셀은 새 실험 번호를 만들고, 받은 대화만 실행 1과 같은 방법으로 보냅니다.
막힌 대화 3은 요청을 보내지 않으므로, 이 셀에서 모델 요청은 두 번 나갑니다."""),
        code(SEND2),
        md(r"""**결과 읽기** — 출력 줄 `보낸 요청 수: 2`가 보입니다.
대화 3은 예약이 막혀, 모델에 요청이 하나도 나가지 않았습니다.
예산 가드가 요청보다 먼저 막았기 때문입니다.

다음 셀은 실행 2에서 보낸 대화마다 응답을 한 줄씩 보고, 정답 종류와 같은 답을 셉니다."""),
        code(ANSWERS2),
        md(r"""**결과 읽기** — 라벨 줄 아래 두 줄 모두 `gpt-5.4-mini-2026-03-17`이 답했습니다.
대화 1은 새 실험 번호로 보낸 실행 2의 첫 요청이라, 캐시 입력 토큰 수가 0입니다.
흔들림 확인 다섯 번과 새 커널 두 번에서 모두, 대화 2에는 캐시 입력이 생겼습니다.
두 답도 모두 정답 종류와 같았습니다.

교재 출력에서는 답이 차례대로 `배송`, `환불`입니다.
입력 토큰 수는 `3165`·`3169`토큰이고, 대화 2의 캐시 입력 토큰 수는 `2816`토큰입니다.
실험 번호의 토큰 수가 실행마다 조금 달라, 입력 토큰 수는 실행마다 달라질 수 있습니다.

다음 셀은 실행 2에서 보낸 대화마다 두 가지 비용을 보고, 예약 합과 비용 합을 견줍니다."""),
        code(COSTS2),
        md(r"""**결과 읽기** — 라벨 줄 아래 두 줄이 실행 2의 대화마다의 예상 비용입니다.
대화 1은 캐시 입력이 없어, 마지막 칸이 `True`입니다.
출력 줄 `예약한 금액의 합(달러): 0.00498`은 예약 셀과 같은 값입니다.
흔들림 확인 다섯 번과 새 커널 두 번에서 모두, 받은 대화의 비용 합이 예약한 금액의 합보다 적었습니다.

교재 출력에서는 대화당 비용이 `0.002392`·`0.000498`달러입니다.
대화 2를 할인 없이 세면 `0.002399`달러입니다.
받은 대화의 대화당 비용 합은 `0.00289`달러입니다.

## 5. 두 실행 견주기

다음 셀은 두 실행을 한 표로 모읍니다.
받은 대화·막힌 대화·보낸 요청·정답 종류와 같은 답의 수와 대화당 비용 합을 나란히 둡니다."""),
        code(SUMMARY),
        md(r"""**결과 읽기** — 라벨 줄 아래 첫 줄은 `실행 1 | 30 | 3 | 0 | 3 | 3 |`으로 시작합니다.
둘째 줄은 `실행 2 | 0 | 2 | 1 | 2 | 2 |`로 시작합니다.
바꾼 값은 기준 길이 하나였고, 받은 대화와 보낸 요청이 셋에서 둘로 줄었습니다.
두 실행 모두 받은 대화 수와 보낸 요청 수가 같습니다.

교재 출력에서는 대화당 비용 합이 실행 1 `0.003169`달러, 실행 2 `0.00289`달러입니다.
두 실행은 받은 대화의 수가 달라, 합만으로 어느 쪽이 싼지 견주지 않습니다.
같은 대화끼리의 견줌은 다음 셀에서 봅니다.

다음 셀은 두 실행에서 모두 받은 대화 1·2만 골라, 두 실행의 대화당 비용을 견줍니다.
같은 대화를 nano와 mini에 보낸 값이라, 모델에 따른 차이를 봅니다."""),
        code(SAME_CONV),
        md(r"""**결과 읽기** — 라벨 줄 아래 두 줄 모두 실행 1은 `gpt-5.4-nano`, 실행 2는 `gpt-5.4-mini`로 보냈습니다.
대화 1의 줄은 흔들림 확인 다섯 번과 새 커널 두 번에서 모두 마지막 칸이 `True`였습니다.
대화 1은 두 실행 모두 첫 요청이라 캐시 입력이 없어, 요금표만 다른 비교입니다.
같은 사용량이면 nano 요금표로 센 값이 늘 적다는 03절 결과와 맞습니다.

교재 출력에서는 대화 1이 `0.000638`달러와 `0.002392`달러이고, 대화 2의 줄도 `True`였습니다.
새 커널로 한 번 더 실행했을 때는 실행 1 대화 2에 캐시 입력이 없어, 대화 2의 줄이 False였습니다.
캐시 입력이 없는 nano 요청은 `0.00064`달러로, 캐시 입력이 있는 mini 요청 `0.000498`달러보다 비쌉니다.
모델 mini의 캐시 입력 요금 0.075달러가, nano의 일반 입력 요금 0.20달러보다 작기 때문입니다.

**결론** — 바꾼 값은 모델 라우터의 기준 길이 하나였습니다.
기준 길이 30에서는 nano 둘·mini 하나로 문의 셋을 모두 받았고, 요청이 세 번 나갔습니다.
기준 길이 0에서는 mini 셋의 예약이 비용 상한을 넘어 대화 3이 막혔고, 요청은 두 번 나갔습니다.
흔들림 확인 다섯 번과 새 커널 두 번에서 모두, 다섯 답이 정답 종류와 같았고 대화 1은 nano 쪽 비용이 적었습니다.

실행 1이 포기한 것은 대화 1·2의 mini 답이고, 실행 2가 포기한 것은 대화 3의 답입니다.
대화 2의 비용 비교는 캐시 입력이 생기는지에 따라 달라져, 결론에 넣지 않았습니다.
문의 셋만 본 결과라, 다른 문의에서도 nano의 답이 맞는다고 할 수는 없습니다.

## 정리

1. 모델 라우터가 고른 모델의 예약 금액을 요청 전에 예약하면, 비용 상한에 걸린 대화는 요청을 보내지 않습니다.
2. 같은 비용 상한에서 기준 길이 30은 문의 셋을 모두 받았고, 0은 mini 셋의 예약이 상한을 넘어 둘만 받았습니다.
3. 정책 글을 앞에 둔 요청은 캐시 입력 할인을 넣어 비용을 세고, 싼 모델의 답이 정답 종류와 같은지도 함께 적습니다.

이 절로 Ch 34와 Part 7이 끝납니다.
과정표의 다음 차례는 Part 8 Ch 35 「0단계 — 무지침」입니다.
이 교재에는 Part 8이 아직 없고, 과정표는 그 세부를 개강 전에 정한다고 적습니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
def table_html(head: list, rows: list) -> str:
    head_html = ""
    for value in head:
        head_html = head_html + "<th>" + value + "</th>"
    body = ""
    for row in rows:
        cells_html = ""
        for value in row:
            cells_html = cells_html + "<td>" + value + "</td>"
        body = body + "<tr>" + cells_html + "</tr>"
    return "<table><thead><tr>" + head_html + "</tr></thead><tbody>" + body + "</tbody></table>"


def html_text(text: str) -> str:
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(01~05 생성기와 같은 함수)."""
    parts = text.replace("\n", " ").split("`")
    out = ""
    for index in range(len(parts)):
        if index % 2 == 1:
            out = out + "<code>" + parts[index] + "</code>"
        else:
            out = out + parts[index]
    return out


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    """.mmd가 있을 때만 본문에 넣습니다(새 커널 A·B를 그림보다 먼저 돌릴 때 빌드가 멈추지 않게)."""
    if not (FIGS / (name + ".mmd")).is_file():
        return ""
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다."""
    if not (FIGS / (ILLU + ".png")).is_file() or ILLU_READ.startswith("[["):
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH16_04 = "../../part4/ch16-guardrails/04-호출-한도와-비용-상한.html"
L_CH26_03 = "../../part6/ch26-delegation/03-Router-분류와-병렬-실행.html"
L_01 = "01-프롬프트-캐시-계측.html"
L_02 = "02-Batch-API.html"
L_03 = "03-모델-라우팅.html"
L_04 = "04-백오프-큐-동시성.html"
L_05 = "05-예산-가드와-p95.html"


def link(href: str, text: str) -> str:
    return '<a href="' + href + '">' + text + "</a>"


LEARNED_ROWS = [
    (link(L_01, "01절"), "공통 앞부분·실험 번호·함수 <code>make_request</code> · 캐시 입력 할인과 함수 <code>cost_row</code>(할인을 넣은 값과 할인 없이 센 값)",
     "정책 글 셀(01절 셀과 글자까지 같음), 실행마다 새 실험 번호, 요청 글 모양, 비용 표"),
    (link(L_03, "03절"), "모델 라우터 <code>choose_model</code>·기준 길이 30과 0·모델 배정·함수 <code>send_inquiry</code>·모델마다 요금표·정답 종류",
     "두 모델 셀과 문의 셀(03절 셀과 글자까지 같음), 모델 배정, 보내기, 답 표"),
    (link(L_05, "05절"), "예산 가드(<code>make_budget</code>·<code>try_reserve</code>)·예약 금액·받은 대화·막힌 대화·함수 <code>make_usage</code>·<code>total_cost</code>",
     "모델마다 예약 금액, 대화마다 한 번 예약, 받은 대화의 비용 합"),
    (link(L_CH06_06, "Ch 6 06절"), "요금표와 함수 <code>estimate_cost</code> · 예상 비용은 청구 금액이 아님",
     "예약 금액 셈, 대화당 비용 셈(함수 <code>cost_row</code> 안)"),
    (link(L_CH16_04, "Ch 16 04절"), "호출 한도·비용 상한·예약·예산 · 함수 <code>make_budget</code>·<code>reserve</code> · 요청마다 예약",
     "예산 딕셔너리, 함수 <code>try_reserve</code> 안의 <code>reserve</code>"),
]

COMPARE_ROWS = [
    ("바꾼 값 — 기준 길이", "<code>30</code>", "<code>0</code>"),
    ("모델 배정", "nano · nano · mini", "mini · mini · mini"),
    ("예약 결과", "셋 모두 <code>예약됨</code>", "<code>예약됨</code> · <code>예약됨</code> · <code>비용 상한을 넘습니다.</code>"),
    ("예약한 금액의 합(달러)", "<code>0.00382</code>", "<code>0.00498</code>"),
    ("받은 대화 · 막힌 대화 · 보낸 요청", "<code>3</code> · <code>0</code> · <code>3</code>", "<code>2</code> · <code>1</code> · <code>2</code>"),
    ("대화 1의 캐시 입력", "0(새 실험 번호 뒤 첫 요청)", "0(새 실험 번호 뒤 첫 요청)"),
    ("대화 2의 캐시 입력", "교재 출력 <code>2816</code> · 새 커널 둘째 실행 0(흔들림 확인 다섯 번은 0보다 큼)", "0보다 큼(흔들림 확인 다섯 번과 새 커널 두 번)"),
    ("답이 정답 종류와 같은가(흔들림 확인 다섯 번과 새 커널 두 번)", "세 답 모두 같음", "두 답 모두 같음"),
    ("받은 대화의 대화당 비용 합(교재 출력, 실행마다 다를 수 있음)", "<code>0.003169</code>달러", "<code>0.00289</code>달러"),
    ("포기한 것", "대화 1·2의 mini 답", "대화 3의 답"),
]

METAPHOR = """<p>충전대 하나를 모듈 셋으로 조립한다고 해 봅니다. 모듈마다 배터리를 꽂는 칸이 하나 있고, 모듈끼리는 걸쇠로 이어져 한 줄이 됩니다. 칸의 크기는 꽂을 배터리에 맞춥니다. 가벼운 일에는 작은 배터리를, 무거운 일에는 큰 배터리를 꽂습니다.</p><p>충전대가 한 번에 쓸 수 있는 전력은 정해져 있습니다. 그래서 배터리를 꽂기 전에 그 배터리의 몫을 먼저 떼어 두고, 몫이 모자라면 꽂지 않습니다. 몫을 떼어 둔 배터리만 칸에 꽂히고, 그 모듈 앞의 불이 켜집니다.</p><p>그림은 실행 1이 끝난 모습입니다. 작은 배터리 둘과 큰 배터리 하나가 꽂혀, 불 셋이 모두 켜져 있습니다.</p><p>배터리의 크기가 모델이고, 크기를 고르는 일이 모델 라우터입니다. 떼어 두는 몫이 예약 금액이고, 정해진 전력이 비용 상한입니다. 모듈 셋을 걸쇠로 이은 것이, 세 절의 기능을 한 흐름으로 이은 것입니다.</p><p>비유와 다른 점이 있습니다. 실제 요청은 정책 글을 앞에 붙여 보내고, 같은 앞부분의 둘째 요청은 캐시 입력 할인을 받을 수 있습니다. 그림에는 이 할인이 보이지 않습니다. 그림에 없는 실행 2라면, 큰 배터리 셋 가운데 둘만 꽂히는 셈입니다.</p>"""

LOOK_B5 = "노트북 3절에서 <code>예약 결과: ['예약됨', '예약됨', '예약됨']</code>과 <code>보낸 요청 수: 3</code>을 찾습니다. 4절에서는 <code>예약 결과: ['예약됨', '예약됨', '비용 상한을 넘습니다.']</code>와 <code>보낸 요청 수: 2</code>를 봅니다. 답·토큰 수·비용은 교재 출력의 값이라, 여러분의 실행에서는 다를 수 있습니다."
LOOK_B6 = "5절 첫 셀의 두 줄에서 받은 대화 <code>3</code>과 <code>2</code>, 막힌 대화 <code>0</code>과 <code>1</code>을 견줍니다. 5절 둘째 셀에서는 대화 1의 마지막 칸 <code>True</code>를 봅니다. 대화 2의 칸과 비용 합, 토큰 수는 실행마다 달라질 수 있는 값입니다."


def src_html() -> str:
    learned = table_html(["절", "배운 것", "실습에서 쓰는 곳"], LEARNED_ROWS)
    compare = table_html(["견준 것", "실행 1 — 기준 길이 30", "실행 2 — 기준 길이 0"], COMPARE_ROWS)
    return """<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>01절 공통 앞부분, 03절 모델 라우터, 05절 예산 가드를 문의 셋의 흐름 하나로 이어 실행할 수 있습니다.</li>
<li>기준 길이 하나만 바꾼 두 실행에서, 받은 대화와 보낸 요청의 수가 어떻게 달라지는지 출력으로 설명할 수 있습니다.</li>
<li>대화당 비용을 캐시 입력 할인을 넣어 세고, 싼 모델로 줄인 비용과 포기한 것을 함께 적을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 비용을 줄이는 방법을 절마다 따로 익혔습니다. """ + link(L_01, "01절") + """은 공통 앞부분 뒤에 바뀌는 글을 두어 캐시 입력 할인을 받았습니다. """ + link(L_03, "03절") + """은 문의 글의 글자 수로 싼 모델과 비싼 모델을 골랐습니다. """ + link(L_05, "05절") + """은 요청 전에 예약해, 비용 상한을 넘는 대화를 막았습니다.</p><p>실제 서비스에서는 이 일들이 문의 하나를 처리하는 동안 함께 일어납니다. 이번 실습은 세 기능을 책 가게 문의 셋의 흐름 하나로 이어 실행합니다. 기준 길이 하나만 바꿔 한 번 더 실행하고, 두 실행을 견줍니다. 과정표의 이 챕터 과제는 대화당 비용을 줄이고, 무엇을 포기했는지 함께 적는 것입니다.</p><p>03절에서도 기준 길이를 30에서 0으로 바꿨습니다. 이 절에서 새로 볼 것은 두 가지입니다. 같은 비용 상한에서 모두 mini로 보내면 대화 하나가 막히고, 막힌 대화는 요청을 보내지 않습니다. 01절에서 본 캐시 입력이, 모델 라우터가 고른 모델마다 따로 생기는지도 봅니다.</p><p>제목의 Rate Limit은 """ + link(L_04, "04절") + """에서 본 요청 제한(rate limit)입니다. 이 실습은 요청 제한에 닿는 장면을 만들지 않고, 비용 쪽 기능을 한 흐름으로 잇습니다. 이번 절은 이 챕터의 실습입니다. 01~05절에서 쓴 이름과 Ch 2에서 배운 문법만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p><p><b>이 절의 질문</b> — 모델 라우터와 예산 가드를 함께 붙이면, 같은 비용 상한에서 받는 대화와 포기하는 것은 어떻게 달라질까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 앞 절 함수는 도구 파일 <code>cost_tools.py</code>에서 가져오고, 결과를 보는 함수 하나만 노트북에 새로 적습니다.</p>
""" + learned + """
<p>붙인 기능은 01절 공통 앞부분과 캐시 입력 할인, 03절 모델 라우터, 05절 예산 가드 셋입니다. 셋 모두 실행 1·2 흐름에서 출력으로 보입니다. 03절에서 본 대로 모델 라우터는 모델 이름만 고르는 함수입니다. """ + link(L_CH26_03, "Ch 26 03절") + """에서 요청을 분류해 전문 에이전트에게 보내던 라우터와는 다른 말입니다.</p><p>""" + link(L_02, "02절") + """의 일괄 처리(Batch API)는 결과를 24시간 안에 받는 방법이라, 노트북 흐름 안에서 기다리지 않도록 뺐습니다. 04절의 다시 보내기와 한꺼번에 보내는 수는 요청이 실패하거나 여럿을 함께 보낼 때 드러납니다. 이 절의 요청 다섯은 차례로 하나씩 보내고, 제공자의 요청 제한에 일부러 닿게 할 수 없어 뺐습니다. 05절의 평균과 95 백분위수는 대화가 셋뿐이라 뜻을 갖기 어려워 쓰지 않았습니다.</p><p>이 절은 05절처럼 대화마다 한 번 예약합니다. Ch 16 04절은 요청마다 예약했습니다. 이 절은 대화 하나가 요청 한 번이라, 두 방식의 예약 수가 같습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + METAPHOR + """
""" + illustration_block() + """<h3>실습 조립의 구성</h3><p>실습의 흐름은 대화 하나마다 네 단계입니다. 먼저 03절 함수 <code>choose_model</code>이 문의 글의 글자 수로 모델 이름을 고릅니다. 다음으로 05절 함수 <code>try_reserve</code>가 그 모델의 예약 금액을 예산에 예약해 봅니다. 예약이 되면 01절 함수 <code>make_request</code>가 실험 번호와 정책 글을 앞에 붙이고, 03절 함수 <code>send_inquiry</code>가 고른 모델로 보냅니다.</p><p>응답이 오면 01절 함수 <code>cost_row</code>가 캐시 입력 할인을 넣은 비용과 할인 없이 센 비용을 한 줄에 적습니다. 예약이 막힌 대화는 모델에 요청을 보내지 않습니다. 예산 칸은 예약 금액으로만 바뀌고, 응답의 실제 사용량으로 고치지 않습니다. 이 절에서 새로 배우는 말은 없습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 1절은 패키지·도구 파일 함수·키와 두 모델을 준비합니다. 2절은 요금표·정책 글·문의 셋·답 형식 글과, 예약 금액·비용 상한을 정합니다. 3절은 기준 길이 30으로 모델 배정·예약·보내기를 하고, 답과 비용을 봅니다. 4절은 기준 길이만 0으로 바꿔 같은 일을 하고, 5절은 두 실행을 견줍니다.</p><p>모델 요청은 모두 다섯 번으로, nano에 두 번, mini에 세 번입니다. 요금표(2026-09-30 확인)로 어림한 비용은 다섯 번을 합쳐 약 0.006달러이고, 청구 금액이 아닙니다. 파일은 쓰지 않고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>가설은 예약 금액과 비용 상한으로 세웠습니다. 기준 길이 30이면 예약 합 0.00382달러로 셋을 모두 받을 것이라고 보았습니다. 기준 길이 0이면 mini 셋의 예약 합 0.00747달러가 상한 0.006달러를 넘을 것이라고 보았습니다. 실험은 같은 문의 글·정책 글·예약 금액·비용 상한으로, 기준 길이 하나만 바꿔 두 번 했습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + compare + """
<p>기준 길이를 0으로 내리자, nano로 가던 대화 1·2가 mini로 갔습니다. 예약 금액이 0.000665달러에서 0.00249달러로 커져, 같은 비용 상한에서 대화 3의 예약이 막혔습니다. 막힌 대화 3은 모델에 요청을 보내지 않아, 보낸 요청이 셋에서 둘로 줄었습니다. 모델 배정·예약 결과·요청 수는 코드와 정한 값으로 정해져, 실행할 때마다 같습니다.</p><p>아래 다섯 가지는 흔들림 확인 다섯 번과 새 커널 두 번에서 모두 같았습니다. 다섯 답이 정답 종류와 같았고, 실행 2의 대화 2(mini 둘째 요청)에는 캐시 입력이 생겼습니다. 두 실행 모두 첫 요청인 대화 1은, nano로 보낸 실행 1의 대화당 비용이 더 적었습니다. 두 실행 모두 받은 대화의 비용 합이 예약한 금액의 합보다 적었습니다. 실행 1에서 nano 다음에 mini로 보낸 대화 3은, 같은 정책 글 뒤인데도 캐시 입력이 0이었습니다.</p><p>실행 1 대화 2(nano 둘째 요청)의 캐시 입력은 실행에 따라 달랐습니다. 그래서 대화 2의 비용 비교는 결론에 넣지 않고, 위 표와 주의할 점에만 적었습니다.</p><p>과제 모양으로 적으면, 실행 1은 대화 1을 nano로 보내 대화당 비용을 줄였습니다. 그 대신 대화 1·2의 mini 답을 포기했습니다. 이번 문의 셋에서는 nano의 답도 정답 종류와 같았습니다. 실행 2는 모든 대화를 mini로 보내, 같은 비용 상한에서 대화 3을 받지 못했습니다.</p><p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>정한 사용량(입력 3,200토큰·캐시 입력 0·출력 20토큰)과 비용 상한 0.006달러는 실행 전에 이 절에서 정한 값입니다. 입력 3,200토큰은 01절 교재 출력의 입력 토큰 수 3,166·3,170보다 조금 크게 잡았습니다. 비용 상한은 nano 둘·mini 하나의 예약 합은 들어가고, mini 셋의 예약 합은 넘도록 고른 흐름을 보여 주는 예입니다. 문의 글·정답 종류·답 형식 글은 03절, 정책 글은 01절 셀에서 가져왔습니다.</li><li>교재를 만들 때 노트북 밖에서 같은 요청 다섯을 다섯 번 보냈습니다. 다섯 번 모두 모델 배정·예약 결과·요청 수가 같았고, 다섯 답도 모두 정답 종류와 같았습니다. 두 실행의 대화 2에도 다섯 번 모두 캐시 입력이 생겼습니다. 그런데 교재 출력을 만든 뒤 새 커널로 한 번 더 실행하자, 실행 1 대화 2의 캐시 입력은 0이었습니다. 같은 요청도 실행한 때에 따라 캐시 입력과 답이 달라질 수 있습니다.</li><li>공식 안내는 같은 앞부분을 가진 기계에 요청이 닿았을 때만 캐시 입력이 생긴다고 적습니다. 조직이 다르면 나누어 쓰지 않고, 쉬는 시간이 5~10분쯤 지나면 지워질 수 있다고도 적습니다. 새 커널 둘째 실행의 대화 2는 첫 요청 바로 뒤에 보냈는데도 캐시 입력이 없었습니다. 그 까닭은 서비스 안쪽 일이라 확인하지 못했습니다. 여러분의 출력에서도 대화 2에 캐시 입력이 없을 수 있습니다.</li><li>새 커널 둘째 실행의 대화 2는 실행 1(nano, 캐시 입력 없음)이 0.00064달러였습니다. 실행 2(mini, 캐시 입력 있음)는 0.000499달러로, 실행 2 쪽이 더 쌌습니다. 캐시 입력이 있는 mini 요청이 캐시 입력이 없는 nano 요청보다 쌀 수 있기 때문입니다. 그래서 대화 2의 비용 비교는 결론에 넣지 않았습니다.</li><li>예약 금액은 캐시 입력 할인 없이 넉넉히 어림했습니다. 그래서 캐시 입력이 생긴 대화는 예약 금액보다 훨씬 적게 들었습니다. 05절과 Ch 16 04절처럼, 대화를 마친 뒤 응답의 사용량으로 예산 칸을 고치는 일은 하지 않았습니다.</li><li>예약은 앱이 세는 단위입니다. 04절처럼 오류가 나면 SDK가 요청을 다시 보낼 수 있어, 제공자가 받은 요청 수는 예약 수보다 많아질 수 있습니다. 이 절은 설치판의 다시 보내기(오류 때 2번)를 켜 둔 채 실행했고, 교재 출력에서는 다섯 요청이 모두 답을 받았습니다.</li><li>모델 라우터는 글자 수만 봅니다. 짧아도 판단이 까다로운 문의가 있어, nano로 보낸 문의의 답은 따로 확인해야 합니다. 이 절의 문의 셋에서 nano의 답이 맞았다고, 다른 문의에서도 맞는다고 할 수는 없습니다.</li><li>제공자도 프로젝트마다 월 지출 한도를 둘 수 있습니다. 공식 안내는 알림만 보내는 설정과 요청을 막는 설정이 있다고 적습니다. 이 설정은 프로젝트 설정 화면의 기능이고, 노트북에서 실행하지 않았습니다.</li><li>02절에서 문서로 본 일괄 처리의 할인 50%는 이 절 셈에 넣지 않았습니다. 이 절에서는 일괄 작업을 만들지 않았습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 버전과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>모델 라우터가 고른 모델의 예약 금액을 요청 전에 예약하면, 비용 상한에 걸린 대화는 요청을 보내지 않습니다.</li><li>같은 비용 상한에서 기준 길이 30은 문의 셋을 모두 받았고, 0은 mini 셋의 예약이 상한을 넘어 둘만 받았습니다.</li><li>정책 글을 앞에 둔 요청은 캐시 입력 할인을 넣어 비용을 세고, 싼 모델의 답이 정답 종류와 같은지도 함께 적습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 34와 Part 7이 끝납니다. 과정표의 다음 차례는 Part 8 Ch 35 「0단계 — 무지침」입니다. 이 교재에는 Part 8이 아직 없고, 과정표는 그 세부를 개강 전에 정한다고 적습니다. 이 절은 파일을 쓰지 않아, 다음 챕터로 넘기는 파일도 없습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 실행 1에서 대화 셋의 예약 금액을 모두 더하면 얼마이고, 비용 상한 안에 드나요?</p><p class="quiz-a">0.000665 + 0.000665 + 0.00249 = 0.00382달러입니다. 비용 상한 0.006달러 안이라, 셋 모두 예약되었습니다. 틀렸다면 노트북 2절의 예약 금액 셀과 3절의 예약 셀을 다시 읽습니다.</p><p class="quiz-q">2. 실행 2에서 대화 3이 막힌 까닭은 무엇이고, 막힌 뒤 모델에 요청이 나갔나요?</p><p class="quiz-a">예약 금액 0.00249달러를 세 번 예약하면 0.00747달러라, 비용 상한 0.006달러를 넘기 때문입니다. 예약이 요청보다 먼저라, 대화 3은 요청을 보내지 않았고 보낸 요청 수는 2였습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">3. 두 실행 모두 대화 1의 캐시 입력 토큰 수가 0인 까닭은 무엇인가요?</p><p class="quiz-a">실행마다 새 실험 번호를 요청 글 맨 앞에 두어, 앞 요청과 첫 글자부터 맞는 앞부분이 거의 없기 때문입니다. 01절의 첫 요청과 같은 자리입니다. 틀렸다면 노트북 3절의 실험 번호 셀을 다시 읽습니다.</p><p class="quiz-q">4. 받은 대화의 비용 합이 예약한 금액의 합보다 적었던 까닭은 무엇인가요?</p><p class="quiz-a">예약 금액은 입력 3,200토큰·캐시 입력 0·출력 20토큰으로, 할인 없이 넉넉히 어림했습니다. 흔들림 확인 다섯 번과 새 커널 두 번에서 모두, 실제 입력 토큰 수는 3,200보다 적었습니다. 흔들림 확인 다섯 번에서는 출력 토큰 수도 20보다 적었습니다. 캐시 입력이 생긴 대화는 할인까지 받아 더 적게 들었습니다. 틀렸다면 노트북 2절의 예약 금액 셀과 3절의 비용 셀을 다시 읽습니다.</p><p class="quiz-q">5. 이 실습에서 비용을 줄인 대신 포기한 것은 무엇이고, 무엇으로 확인했나요?</p><p class="quiz-a">실행 1은 대화 1·2를 nano로 보내 mini의 답을 포기했고, 그 답이 정답 종류와 같은지로 확인했습니다. 실행 2는 모든 대화를 mini로 보내, 같은 비용 상한에서 대화 3을 받지 못했습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://developers.openai.com/api/docs/models/gpt-5.4-nano">OpenAI GPT-5.4 nano</a></div>확인 2026-09-30 · 100만 토큰당 입력 0.20달러, 캐시 입력 0.02달러, 출력 1.25달러입니다. 날짜판 이름은 <code>gpt-5.4-nano-2026-03-17</code>이고, 03절에서 2026-09-29에 확인한 요금표와 같습니다.</li><li><div><a href="https://developers.openai.com/api/docs/models/gpt-5.4-mini">OpenAI GPT-5.4 mini</a></div>확인 2026-09-30 · 100만 토큰당 입력 0.75달러, 캐시 입력 0.075달러, 출력 4.50달러입니다. 날짜판 이름은 <code>gpt-5.4-mini-2026-03-17</code>이고, 01·05절의 요금표와 같습니다.</li><li><div><a href="https://developers.openai.com/api/docs/guides/prompt-caching">OpenAI Prompt caching</a></div>확인 2026-09-30 · GPT-5.6 앞 모델은 캐시 입력 토큰 수를 128의 배수로 내려 보고한다고 적습니다. 같은 앞부분을 가진 기계에 요청이 닿아야 다시 쓸 수 있고, 조직 사이에는 나누지 않는다고 적습니다. 메모리에 둔 앞부분은 보통 쉬는 시간 5~10분쯤 남는다고 적습니다.</li><li><div><a href="https://developers.openai.com/api/docs/guides/spend-limits">OpenAI Spend limits</a></div>확인 2026-09-30 · 조직과 프로젝트마다 월 지출 한도를 두는 방법을 설명합니다. 알림은 요청을 막지 않고, 막는 한도에 닿은 요청은 429를 받는다고 적습니다.</li><li>도구 파일 함수의 출처 · 확인 2026-09-30 · 함수 <code>make_request</code>·<code>cost_row</code>는 01절, <code>choose_model</code>·<code>send_inquiry</code>는 03절 노트북 셀에서 옮겼습니다. 함수 <code>make_usage</code>·<code>total_cost</code>·<code>try_reserve</code>는 05절 노트북 셀에서 옮겼습니다. 설명 줄과 본문은 셀과 글자까지 같습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


# ---------------------------------------------------------------- 설계 확인 · 대조
def design_check() -> str:
    """06 판 도구 파일을 임시 폴더에 두고, 모델 요청이 없는 코드 셀을 커널 없이 한 이름 공간에서 차례로 실행해 출력을 모읍니다.

    모델 객체는 만들지만 요청은 보내지 않습니다(가짜 키 글을 환경 변수에 둠 — 서비스 요청 0)."""
    folder = tempfile.mkdtemp(prefix="ch34-06-design-")
    Path(folder, "cost_tools.py").write_text(TOOLS06, encoding="utf-8")
    sys.path.insert(0, folder)
    os.environ["OPENAI_API_KEY"] = "design-check-no-request"
    space = {}
    buffer = io.StringIO()
    skip = [INSTALL, KEY] + MODEL_CELLS
    with contextlib.redirect_stdout(buffer):
        for text in CODE_CELLS:
            if text in skip:
                continue
            exec(compile(text, "<cell>", "exec"), space)
    sys.path.remove(folder)
    sys.modules.pop("cost_tools", None)
    out = buffer.getvalue()
    missing = []
    for phrase in EXPECTED:
        if phrase not in out:
            missing.append(phrase)
    assert not missing, missing
    return out


def check_inputs() -> None:
    """앞 절 셀을 그대로 쓴 셀이 그 절 셀과 글자까지 같고, 요청 글이 01절 요청 글과 같은 모양인지 봅니다."""
    assert POLICY == A01.POLICY and INQUIRIES == A03.INQUIRIES
    assert NANO == A03.NANO and MINI == A03.MINI and MODELS == A03.MODELS
    rule03 = A03.value_from(A03.RULE, "answer_rule")
    assert A03.value_from(RULE, "answer_rule") == rule03
    inquiries = A03.value_from(INQUIRIES, "inquiries")
    first01 = A03.value_from(A01.INQUIRIES, "inquiries")
    # send_inquiry가 붙이는 「공백 + 답 형식 글」까지 이으면, 대화 1·2의 뒤 글은 01절 문의 글 1·2와 글자까지 같다
    assert inquiries[0] + " " + rule03 == first01[0] and inquiries[1] + " " + rule03 == first01[1]
    # 요금표 셀은 03절 셀과 확인 날짜 한 줄만 다르다
    assert PRICES.replace('"2026-09-30"', '"2026-09-29"') == A03.PRICES
    code_count = 0
    for text in CODE_CELLS:
        code_count = code_count + 1
        assert ast.parse("\n".join("pass" if line.strip().startswith("%") else line for line in text.splitlines()))
    assert 20 <= code_count <= 32, code_count


def leftover_placeholders() -> list:
    found = []
    text = src_html()
    for cell in cells():
        text = text + cell["source"]
    for part in text.split("[[")[1:]:
        found.append(part.split("]]")[0])
    return found


if __name__ == "__main__":
    check_tools06()
    check_inputs()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        target.mkdir(parents=True, exist_ok=True)
        (target / "cost_tools.py").write_text(TOOLS06, encoding="utf-8")
        print("wrote", target / "cost_tools.py", hashlib.sha256(TOOLS06.encode("utf-8")).hexdigest())
        raise SystemExit(0)
    if "--design-check" in sys.argv:
        print(design_check())
        print("design check: 본문 값", len(EXPECTED), "개 모두 출력에 있음")
        raise SystemExit(0)
    if "--guard-check" in sys.argv:
        guard_check()
        raise SystemExit(0)
    left = leftover_placeholders()
    if left:
        print("자리 표시(흔들리는 값은 A 출력으로 mdpatch):", left)
    if "--nb-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--nb-copy") + 1])
        target.mkdir(parents=True, exist_ok=True)
        path = write_notebook(target, "06", SLUG, "experiment", cells())
        (target / "cost_tools.py").write_text(TOOLS06, encoding="utf-8")
        print("wrote copy", path, "and cost_tools.py (06 판 사본)")
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        write_tools()
        path = write_notebook(LAB, "06", SLUG, "experiment", cells())
        print("wrote", path)
