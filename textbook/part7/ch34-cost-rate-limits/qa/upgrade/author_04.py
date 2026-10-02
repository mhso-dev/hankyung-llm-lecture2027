"""Ch 34 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 paired).

사용:
  python3 -B author_04.py              → 도구 파일(없거나 01·02·04 판일 때만)·연습용 서버 파일(없거나 같을 때만) + 노트북 + _src 본문을 쓴다
  python3 -B author_04.py --src-only   → _src 본문만 다시 쓴다(노트북·도구 파일·서버 파일은 그대로)
  python3 -B author_04.py --nb-copy DIR → 새 노트북을 DIR에만 쓴다(새 커널 B 사본 실행용 — 실습 폴더는 건드리지 않음)
  python3 -B author_04.py --guard-check → 01·02 생성기의 도구 파일 쓰기 가드와 03 생성기 대조가 04 판을 덮어쓰지 않는지 본다
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **paired 형식 유지**. 슬러그 `04-백오프-큐-동시성` 그대로.

## 결정 1 — paired: Before = 겹친 다시 보내기(모델 객체 안 SDK 기본 2 + with_retry 3 → 서버 요청 9), After = 한 곳에만(max_retries=0 + 같은 with_retry → 3)

늘 429만 보내는 127.0.0.1 연습용 서버(notebooks/always_429_server.py — 함수 하나 wsgiref, 클래스·데코레이터 없음)를 자식 프로세스로
띄우고(stdout·stderr 버림), 모델 객체는 과정 표준 설정 + base_url(연습용 서버) + 가짜 키. 서비스 요청 0, 키 셀 없음.
서버는 주소 끝이 /chat/completions인 요청만 세고, /reset은 0으로 맞추고, /count는 세지 않고 알려 줌 — 셀마다 0으로 맞추고 시작해
앞 셀이 뒤 셀의 수를 바꾸지 않는다(옛 판 결함 고침). 노트북 밖 확인(/tmp/ch34-04, qa/upgrade/probe/04-shape.md) 5/5 같음:
기본 3 · max_retries=0 1 · Before 9 · After 3 · 오류 이름 OpenAIRateLimitError. 빨강은 Before 결과(9)만, 받은 오류는 노랑, 보라 0.

## 결정 2 — 값 바꿔 보기(After 쪽): 한꺼번에 보내는 수

02 문의 글 다섯을 RunnableLambda(ask_and_count).batch — 설정 없이 한꺼번에 처리 중이던 수의 가장 큰 값 5 ↔ max_concurrency 2 → 2,
서버 요청 15 그대로(동기 batch, async/await 없음). wsgiref는 한 번에 한 요청만 처리하므로 수는 클라이언트 쪽 함수가 셈.
문의마다 with_retry의 기다림(1·2초 + 무작위)이 있어 겹침이 생긴다. 걸린 초는 출력하지 않는다(흔들림 — 결론·라벨·assert 금지).

## 결정 3 — 도구 파일 cost_tools.py 04 판 (규격 §2-7 · handoff 도구 파일 대조 사슬)

02 판(78d4d697…, 마감 전 72429dfa…) 머리 설명 뒤 가져오기 줄에 `import socket`·`import time`을 더하고, 02 판 함수 뒤에 Ch 28 03절 노트북 셀의
wait_for_port를 def~return 글자 그대로(설명 줄도 셀 첫 줄 주석 그대로) 더한다. 대조: strip_later_imports 뒤 02 판으로 시작 · 글자·AST ·
Ch 28 03 노트북 해시 고정. 쓰기 가드: 없거나 01·02·04 판일 때만 쓰고, 04 판으로 시작하는 더 긴 판은 건너뜀.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`min`·`enumerate`·`zip`·`getattr`·`key=`·`reverse=`·
`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·힌트·대입 풀기·별표 풀기·`while`(노트북)·`raise`·세미콜론·`isinstance`·클래스·데코레이터·
가짜 모델·정해 둔 답을 주는 서버·비동기·파일 쓰기·InMemoryRateLimiter. `try`는 오류 이름 하나만 받는 함수 둘. 호출 깊이 2 이하.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

CHAPTER = ROOT / "textbook/part7/ch34-cost-rate-limits"
LAB = ROOT / "labs/part7/ch34-cost-rate-limits/notebooks"
FIGS = CHAPTER / "figures"
SLUG = "04-백오프-큐-동시성"
TITLE_TEXT = "백오프 큐 동시성"
SRC = CHAPTER / "_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "cost_tools.py"
SERVER_NAME = "always_429_server.py"
SERVER_PATH = LAB / SERVER_NAME
CH28_03_NB = ROOT / "labs/part6/ch28-mcp/notebooks/03-stdio와-원격-전송-권한-경계.ipynb"
CH28_03_SHA = "c1f22daac6fd95726de79f9c8563e0908f017fdf892d0ed57c44e3b80f35893d"
TOOLS02_SHA = "78d4d6974d148d1283f833115e0e6acf7b742d6898803f81e0ce6e795da0dfa1"
RUNS_SENTENCE = os.environ.get("AUTHOR04_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물넷의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 연습용 서버가 늘 같은 응답을 보내, 요청 수와 한꺼번에 처리된 수가 두 번 모두 같았습니다.")


def load_author02():
    spec = importlib.util.spec_from_file_location("author_02", CHAPTER / "qa/upgrade/author_02.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A02 = load_author02()
A01 = A02.A01
TOOLS01 = A01.TOOLS01
TOOLS02 = A02.TOOLS02
TOOLS_HEAD = A01.TOOLS_HEAD

# ---------------------------------------------------------------- 도구 파일 cost_tools.py (04 판)
CH28_NOTE = "Ch 28 03절에서 배웠습니다 — Ch 28 03절 노트북 셀의 같은 이름 함수를 옮겼습니다"
TOOL_ORDER04 = A02.TOOL_ORDER02 + ["wait_for_port"]
IMPORTS02 = "\nimport json\n"
IMPORTS04 = "\nimport json\nimport socket\nimport time\n"


def ch28_cell_source(name: str) -> str:
    """Ch 28 03절 노트북에서 def name이 든 코드 셀 글을 꺼냅니다(첫 줄 설명 주석 포함)."""
    raw = CH28_03_NB.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CH28_03_SHA, "Ch 28 03절 노트북이 마감 판과 다릅니다"
    nb = json.loads(raw)
    for cell in nb["cells"]:
        source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
        if cell["cell_type"] == "code" and ("def " + name + "(") in source:
            return source
    raise KeyError(name)


def tools04_text() -> str:
    assert TOOLS02.startswith(TOOLS_HEAD + IMPORTS02), "02 판 머리가 예상과 다릅니다"
    original = ch28_cell_source("wait_for_port")
    desc = A02.description_of(original, "wait_for_port", "cell")
    body = TOOLS02[len(TOOLS_HEAD + IMPORTS02):]
    text = TOOLS_HEAD + IMPORTS04 + body
    return text + "\n\n# " + CH28_NOTE + "\n# " + desc + "\n" + A01.def_to_return(original, "wait_for_port") + "\n"


TOOLS04 = tools04_text()


def check_tools04() -> None:
    """04 판이 02 판을 그대로 이어 쓰고(가져오기 줄 뺀 뒤), 더한 wait_for_port가 Ch 28 03절 셀과 글자·AST 모두 같은지 봅니다."""
    A02.check_tools02()
    assert hashlib.sha256(TOOLS02.encode("utf-8")).hexdigest() == TOOLS02_SHA, "02 판 해시가 다릅니다"
    assert A01.strip_later_imports(TOOLS04).startswith(A01.strip_later_imports(TOOLS02)), "04 판이 02 판으로 시작하지 않습니다"
    assert A01.strip_later_imports(TOOLS04).startswith(TOOLS01), "04 판이 01 판으로 시작하지 않습니다"
    tree = ast.parse(TOOLS04)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == TOOL_ORDER04, names
    assert imports == ["import json", "import socket", "import time"], imports
    original = ch28_cell_source("wait_for_port")
    assert A01.def_to_return(TOOLS04, "wait_for_port") == A01.def_to_return(original, "wait_for_port")
    mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "wait_for_port"]
    theirs = [ast.dump(n) for n in ast.parse(original).body if isinstance(n, ast.FunctionDef) and n.name == "wait_for_port"]
    assert mine == theirs and len(mine) == 1
    # 셀 첫 줄 주석이 도구 파일 설명 줄과 같다
    assert ("# " + A02.description_of(original, "wait_for_port", "cell") + "\ndef wait_for_port(") in TOOLS04
    # 02 판 함수 다섯은 02 판과 def~return 글자가 같다
    for name in A02.TOOL_ORDER02:
        assert A01.def_to_return(TOOLS04, name) == A01.def_to_return(TOOLS02, name), name
    bad = (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp, ast.Lambda, ast.IfExp, ast.JoinedStr, ast.ClassDef, ast.Global)
    for node in ast.walk(tree):
        assert not isinstance(node, bad), type(node).__name__
    # while은 Ch 28 03절 wait_for_port 안의 하나뿐
    whiles = [n for n in ast.walk(tree) if isinstance(n, ast.While)]
    assert len(whiles) == 1


def write_tools() -> None:
    """도구 파일은 없거나 01·02·04 판일 때만 04 판으로 쓴다. 04 판으로 시작하는 더 긴 판(뒤 절)은 덮어쓰지 않는다."""
    current = ""
    if TOOLS_PATH.is_file():
        current = TOOLS_PATH.read_text(encoding="utf-8")
    if current == TOOLS04:
        print("same", TOOLS_PATH.name, hashlib.sha256(TOOLS04.encode("utf-8")).hexdigest()[:12])
        return
    if current in ("", TOOLS01, TOOLS02):
        TOOLS_PATH.write_text(TOOLS04, encoding="utf-8")
        print("wrote", TOOLS_PATH, hashlib.sha256(TOOLS04.encode("utf-8")).hexdigest()[:12])
        return
    plain = A01.strip_later_imports(current)
    assert plain.startswith(A01.strip_later_imports(TOOLS04)), "도구 파일이 04절 판으로 시작하지 않습니다 — 손으로 확인하세요"
    print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")


def guard_check() -> None:
    """01·02 생성기의 쓰기 가드가 04 판을 건너뛰고, 03 생성기 대조가 04 판을 받아들이는지 본다(파일이 바뀌지 않았는지 해시로)."""
    before = hashlib.sha256(TOOLS_PATH.read_bytes()).hexdigest()
    A01.write_tools()
    A02.write_tools()
    spec = importlib.util.spec_from_file_location("author_03", CHAPTER / "qa/upgrade/author_03.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.check_tools03()
    after = hashlib.sha256(TOOLS_PATH.read_bytes()).hexdigest()
    print("guard check: before", before[:12], "after", after[:12], "same", before == after)
    assert before == after


# ---------------------------------------------------------------- 연습용 서버 파일 (학생이 여는 파일 — 금지 문법 0)
SERVER = r'''"""Ch 34 04절 연습용 서버 — 어떤 요청이 와도 상태 코드 429(요청 제한)만 보냅니다.

실제 제공자의 요청 제한을 흉내 내는 연습용 서버입니다. 모델의 답은 한 번도 보내지 않습니다.
주소 끝이 /chat/completions인 요청(모델에 보내는 요청)만 세어, 응답 머리 practice-count에 센 수를 적습니다.
주소 끝이 /reset인 요청을 받으면 센 수를 0으로 맞춥니다. 주소 끝이 /count인 요청은 세지 않고, 센 수만 알려 줍니다.
노트북 04절이 이 파일을 자식 프로세스로 띄우고, 마지막 셀에서 끕니다.
"""
import sys
from wsgiref.simple_server import make_server

# 모든 응답에 보낼 오류 글입니다(OpenAI 오류 글과 같은 모양의 JSON입니다)
error_text = '{"error": {"message": "연습용 서버는 늘 429를 보냅니다.", "code": "practice_429"}}'
error_body = error_text.encode("utf-8")
json_type = ("content-type", "application/json")

# 모델에 보내는 요청을 받을 때마다 그 주소를 한 줄씩 모읍니다(목록의 길이가 센 수입니다)
request_log = []


# 요청 하나를 받아 수를 세고, 센 수를 머리에 적어 상태 코드 429와 오류 글을 보냅니다(wsgiref가 요청마다 부릅니다)
def app(environ, start_response):
    path = environ["PATH_INFO"]
    if path.endswith("/reset"):
        request_log.clear()
    if path.endswith("/chat/completions"):
        request_log.append(path)
    headers = [json_type, ("practice-count", str(len(request_log)))]
    start_response("429 Too Many Requests", headers)
    return [error_body]


if __name__ == "__main__":
    # 파일을 직접 실행할 때만: 명령 줄의 첫 인자를 포트 번호로 읽어, 이 컴퓨터 안의 주소에서만 요청을 받습니다
    port = int(sys.argv[1])
    server = make_server("127.0.0.1", port, app)
    server.serve_forever()
'''


def check_server() -> None:
    """학생이 여는 서버 파일에도 금지 문법이 없는지(Ch 28 A-17), 함수 하나·본문 8줄 이하인지 봅니다."""
    tree = ast.parse(SERVER)
    bad = (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp, ast.Lambda, ast.IfExp, ast.JoinedStr, ast.ClassDef,
           ast.Global, ast.While, ast.Try, ast.AsyncFunctionDef, ast.Starred, ast.AugAssign)
    defs = []
    for node in ast.walk(tree):
        assert not isinstance(node, bad), type(node).__name__
        if isinstance(node, ast.FunctionDef):
            assert not node.decorator_list and not node.args.defaults and not node.returns
            defs.append(node)
    assert len(defs) == 1 and defs[0].name == "app"
    body_lines = [l for l in ast.get_source_segment(SERVER, defs[0]).splitlines()[1:] if l.strip() and not l.strip().startswith("#")]
    assert len(body_lines) <= 8, len(body_lines)
    assert "127.0.0.1" in SERVER and "200" not in SERVER


def write_server() -> None:
    """서버 파일은 없거나 이 판과 같을 때만 쓴다(손으로 고친 판이면 멈춤)."""
    if SERVER_PATH.is_file():
        current = SERVER_PATH.read_text(encoding="utf-8")
        assert current == SERVER, "서버 파일이 이 생성기 판과 다릅니다 — 손으로 확인하세요"
        print("same", SERVER_PATH.name, hashlib.sha256(SERVER.encode("utf-8")).hexdigest()[:12])
        return
    SERVER_PATH.write_text(SERVER, encoding="utf-8")
    print("wrote", SERVER_PATH, hashlib.sha256(SERVER.encode("utf-8")).hexdigest()[:12])


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["langchain==1.4.0", "langchain-core==1.6.2", "langchain-openai==1.6.0", "openai==3.13.0", "httpx==0.28.1"])

IMPORTS = r'''# 이 절에서 쓸 이름을 가져옵니다(os·subprocess·sys는 Python에 들어 있는 모듈입니다)
import os
import subprocess
import sys
import httpx
from langchain.chat_models import init_chat_model
from langchain_core.exceptions import ModelRateLimitError
from langchain_core.runnables import RunnableLambda
# Ch 28 03절에서 배운 함수는 도구 파일에서 가져옵니다
from cost_tools import wait_for_port

print("가져온 모듈:", "os, subprocess, sys, httpx")
print("도구 파일에서 가져온 함수:", wait_for_port.__name__)'''

FIND_LAB = r'''# 노트북을 연 자리에서 본 실습 폴더의 위치를 후보 셋 가운데에서 고릅니다
candidates = ["..", ".", "labs/part7/ch34-cost-rate-limits"]
lab_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/notebooks/always_429_server.py"):
        lab_path = candidate
        break
print("실습 폴더를 찾았는가:", lab_path is not None)
assert lab_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

PLAN = r'''# 서버 파일 위치·포트·주소·명령을 정하고, 띄우기 전에 그 포트가 비어 있는지 봅니다
server_file = lab_path + "/notebooks/always_429_server.py"
practice_port = 58034
base_url = "http://127.0.0.1:" + str(practice_port) + "/v1"
command = [sys.executable, server_file, str(practice_port)]
check_limit = 1
port_in_use = wait_for_port(practice_port, check_limit)
print("띄우기 전에 이 포트에서 듣는 프로그램이 있는가:", port_in_use)
assert not port_in_use, "다른 프로그램이 이 포트를 쓰고 있습니다. 셀의 포트 번호를 바꿔 이 셀부터 다시 실행합니다."'''

START = r'''# 연습용 서버 파일을 자식 프로세스로 띄우고, 포트가 열렸는지와 띄운 서버가 살아 있는지 봅니다(서버가 남기는 줄은 버림)
server_process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
port_limit = 20
server_ready = wait_for_port(practice_port, port_limit)
# 메서드 poll은 프로그램이 아직 돌고 있으면 None을 내놓습니다
server_alive = server_process.poll() is None
print("서버가 준비되었는가:", server_ready)
print("띄운 서버가 살아 있는가:", server_alive)
assert server_ready, "기한 안에 서버가 포트를 열지 않았습니다. 커널을 다시 시작해 앞 셀부터 실행합니다."
assert server_alive, "띄운 서버가 끝났습니다. 앞 셀로 이 포트를 다른 프로그램이 쓰는지 다시 봅니다."'''

CHECK = r'''# 연습용 서버에 센 수를 0으로 맞추는 요청을 보내고, 받은 상태 코드·머리 값·오류 글을 봅니다
reset_response = httpx.post(base_url + "/reset")
print("상태 코드:", reset_response.status_code)
print("머리 practice-count:", reset_response.headers["practice-count"])
print("오류 글:", reset_response.json()["error"]["message"])'''

DEF_READ = r'''# 연습용 서버에 센 수를 묻고, 응답 머리 practice-count의 값을 정수로 내놓습니다
def read_count(url):
    response = httpx.get(url + "/count")
    return int(response.headers["practice-count"])'''

DEF_SEND = r'''# 호출 객체에 문의 글 하나를 보내고, 요청 제한 오류를 받으면 오류 이름과 상태 코드를 출력합니다
def send_once(runnable, text):
    try:
        runnable.invoke(text)
    except ModelRateLimitError as error:
        print("받은 오류:", type(error).__name__)
        print("상태 코드:", error.status_code)'''

QUESTION = r'''# 01절의 첫 문의 글을 보낼 글로 정하고, 모델 객체에 넣을 가짜 키를 정합니다
question = "주문한 책이 일주일째 오지 않습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요."
practice_key = "not-a-real-key"
print("보낼 문의 글:", question)
print("가짜 키:", practice_key)'''

MODEL_DEFAULT = r'''# 연습용 서버 주소와 가짜 키로, 과정 표준 설정의 모델 객체를 만듭니다(요청은 나가지 않습니다)
default_model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
    base_url=base_url,
    api_key=practice_key,
)
print("모델 객체 max_retries:", default_model.max_retries)
print("openai 클라이언트 max_retries:", default_model.root_client.max_retries)'''

SEND_DEFAULT = r'''# 서버가 센 수를 0으로 맞춘 뒤 모델 객체를 한 번 부르고, 서버가 받은 요청 수를 봅니다
httpx.post(base_url + "/reset")
send_once(default_model, question)
default_count = read_count(base_url)
print("서버가 받은 요청 수:", default_count)'''

MODEL_ZERO = r'''# 같은 설정에 max_retries=0만 더해, 모델 객체 안에서 다시 보내지 않는 모델 객체를 만듭니다(요청은 나가지 않습니다)
zero_model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
    base_url=base_url,
    api_key=practice_key,
    max_retries=0,
)
print("모델 객체 max_retries:", zero_model.max_retries)
print("openai 클라이언트 max_retries:", zero_model.root_client.max_retries)'''

SEND_ZERO = r'''# 서버가 센 수를 0으로 맞춘 뒤 이 모델 객체를 한 번 부르고, 서버가 받은 요청 수를 봅니다
httpx.post(base_url + "/reset")
send_once(zero_model, question)
zero_count = read_count(base_url)
print("서버가 받은 요청 수:", zero_count)'''

BEFORE_BUILD = r'''# Before: 안에서 다시 보내는 default_model에, 요청 제한 오류일 때 모두 3번까지 부르는 with_retry를 붙입니다(요청 없음)
retry_attempts = 3
before_runnable = default_model.with_retry(
    retry_if_exception_type=(ModelRateLimitError,),
    stop_after_attempt=retry_attempts,
)
print("호출 객체 종류:", type(before_runnable).__name__)'''

BEFORE_SEND = r'''# Before: 서버가 센 수를 0으로 맞춘 뒤 이 호출 객체를 한 번 부르고, 서버가 받은 요청 수를 봅니다
httpx.post(base_url + "/reset")
send_once(before_runnable, question)
before_count = read_count(base_url)
print("서버가 받은 요청 수:", before_count)'''

BEFORE_MATH = r'''# 3절에서 센 모델 객체 한 번의 요청 수에 시도 횟수를 곱해, Before의 요청 수와 견줍니다
multiplied = default_count * retry_attempts
print("모델 객체 한 번의 요청 수 × 시도 수:", multiplied)
print("Before의 요청 수와 같은가:", multiplied == before_count)'''

AFTER_BUILD = r'''# After: 안에서 다시 보내지 않는 zero_model에 같은 with_retry를 붙입니다(요청 없음)
after_runnable = zero_model.with_retry(
    retry_if_exception_type=(ModelRateLimitError,),
    stop_after_attempt=retry_attempts,
)
print("호출 객체 종류:", type(after_runnable).__name__)'''

AFTER_SEND = r'''# After: 서버가 센 수를 0으로 맞춘 뒤 이 호출 객체를 한 번 부르고, 서버가 받은 요청 수를 봅니다
httpx.post(base_url + "/reset")
send_once(after_runnable, question)
after_count = read_count(base_url)
print("서버가 받은 요청 수:", after_count)'''

AFTER_COMPARE = r'''# After의 요청 수를 모델 객체 한 번의 요청 수 × 시도 수와 견주고, Before가 After의 몇 배인지 봅니다
after_multiplied = zero_count * retry_attempts
print("모델 객체 한 번의 요청 수 × 시도 수:", after_multiplied)
print("After의 요청 수와 같은가:", after_multiplied == after_count)
print("Before 요청 수 ÷ After 요청 수:", before_count // after_count)'''

DEF_ASK = r'''# 문의 글 하나를 After의 호출 객체로 보내면서, 시작할 때 처리 중인 문의 수를 적고 받은 오류 이름을 모읍니다
def ask_and_count(text):
    active.append(text)
    peaks.append(len(active))
    try:
        after_runnable.invoke(text)
    except ModelRateLimitError as error:
        received.append(type(error).__name__)
    active.remove(text)'''

INQUIRIES = r'''# 02절의 문의 글 다섯을 목록에 담고, 함수 ask_and_count를 호출 객체로 감쌉니다(요청 없음)
inquiries = [
    "주문한 책이 일주일째 오지 않습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "결제 창에서 카드 번호를 넣었는데 다음 단계로 넘어가지 않습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "받은 책이 찢어져 있어 돈을 되찾고 싶습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "주문한 책을 받을 주소를 회사로 바꾸고 싶습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "결제 수단을 카드에서 계좌 이체로 바꿀 수 있나요? 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
]
counting_runnable = RunnableLambda(ask_and_count)
print("문의 글 수:", len(inquiries))
print("호출 객체 종류:", type(counting_runnable).__name__)'''

BATCH_NONE = r'''# 설정 없이 문의 다섯을 한꺼번에 보내고, 한꺼번에 처리 중이던 문의 수의 가장 큰 값과 서버가 받은 요청 수를 봅니다
httpx.post(base_url + "/reset")
active = []
peaks = []
received = []
counting_runnable.batch(inquiries)
print("받은 오류 수:", len(received))
print("한꺼번에 처리 중이던 문의 수의 가장 큰 값:", max(peaks))
print("서버가 받은 요청 수:", read_count(base_url))'''

BATCH_TWO = r'''# 값 바꿔 보기: 설정 max_concurrency만 2로 두고 같은 문의 다섯을 보냅니다
httpx.post(base_url + "/reset")
active = []
peaks = []
received = []
counting_runnable.batch(inquiries, config={"max_concurrency": 2})
print("받은 오류 수:", len(received))
print("한꺼번에 처리 중이던 문의 수의 가장 큰 값:", max(peaks))
print("서버가 받은 요청 수:", read_count(base_url))'''

STOP = r'''# 연습용 서버에 끝내라는 신호를 보내고, 끝날 때까지 기다려 종료 코드와 포트가 닫혔는지 봅니다
server_process.terminate()
stop_limit = 10
return_code = server_process.wait(timeout=stop_limit)
print("종료 코드:", return_code)
print("포트가 아직 열려 있는가:", wait_for_port(practice_port, check_limit))'''

CODE_CELLS = [IMPORTS, FIND_LAB, PLAN, START, CHECK, DEF_READ, DEF_SEND, QUESTION, MODEL_DEFAULT, SEND_DEFAULT, MODEL_ZERO,
              SEND_ZERO, BEFORE_BUILD, BEFORE_SEND, BEFORE_MATH, AFTER_BUILD, AFTER_SEND, AFTER_COMPARE, DEF_ASK, INQUIRIES,
              BATCH_NONE, BATCH_TWO, STOP]


def list_from(code_text: str, name: str) -> list:
    """코드 셀 글에서 `name = [...]` 목록 값을 꺼냅니다(앞 절 문의 글과 대조할 때)."""
    for node in ast.parse(code_text).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name:
            return ast.literal_eval(node.value)
    raise KeyError(name)


def check_inputs() -> None:
    """문의 글 다섯은 02절 문의 글과, 보낼 문의 글은 01절 첫 문의 글과 글자까지 같은지 봅니다."""
    assert list_from(INQUIRIES, "inquiries") == list_from(A02.INQUIRIES, "inquiries")
    first01 = list_from(A01.INQUIRIES, "inquiries")[0]
    for node in ast.parse(QUESTION).body:
        if isinstance(node, ast.Assign) and node.targets[0].id == "question":
            assert ast.literal_eval(node.value) == first01


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/04-figures.md)
FIG1 = "04-1-다시-보내기가-놓이는-두-곳"
FIG1_ALT = "위에서 아래로 한 줄로 읽는 흐름도입니다. 파란 상자 우리 코드 with_retry 시도 세 번까지에서 부를 때마다라는 화살표가 회색 상자 모델 객체 안 openai 클라이언트 429면 두 번 더 보냄으로 가고, 이어서 초록 상자 늘 429를 보내는 연습용 서버 127.0.0.1을 지나 노란 상자 서버가 받은 요청 수 응답 머리 practice-count로 이어지는 그림"
FIG1_CAP = "다시 보내는 곳은 우리가 붙인 with_retry와 모델 객체 안의 openai 클라이언트, 두 곳입니다."
FIG1_READ = """위에서 아래로 읽습니다.
파란 상자는 우리가 붙이는 다시 보내기 규칙이고, 회색 상자는 라이브러리 안에서 다시 보내는 곳입니다.
초록 상자는 이 절이 띄우는 연습용 서버이고, 노란 상자는 서버가 알려 준 수를 노트북이 출력한 값입니다.
두 곳이 한 줄로 이어져 있어, 위 상자가 한 번 부를 때마다 아래 상자가 요청을 여러 번 보낼 수 있습니다."""

FIG2 = "04-2-모델-객체-한-번의-요청-수"
FIG2_ALT = "맨 위 회색 상자 두 칸 공통 늘 429를 보내는 연습용 서버 같은 문의 글을 한 번 부름 아래에 칸 둘이 나란히 있습니다. 왼쪽 칸 max_retries를 적지 않음에는 초록 상자 default_model openai 클라이언트 max_retries 2에서 노란 상자 OpenAIRateLimitError 429 서버가 받은 요청 세 번으로 이어집니다. 오른쪽 칸 max_retries=0에는 초록 상자 zero_model openai 클라이언트 max_retries 0에서 노란 상자 OpenAIRateLimitError 429 서버가 받은 요청 한 번으로 이어지는 그림"
FIG2_CAP = "모델 객체를 한 번 불렀을 때 서버가 받은 요청은, 값을 적지 않으면 셋이고 0을 적으면 하나였습니다."
FIG2_READ = """맨 위 회색 상자는 두 칸에 공통인 조건입니다.
왼쪽 칸이 인자 max_retries를 적지 않은 모델 객체, 오른쪽 칸이 0을 적은 모델 객체입니다.
칸마다 위 초록 상자는 3절 셀에서 만든 모델 객체이고, 그 셀이 출력한 클라이언트 값을 함께 적었습니다.
아래 노란 상자는 받은 오류와 서버가 받은 요청 수입니다."""

FIG3 = "04-3-Before에서-요청-아홉이-나오는-차례"
FIG3_ALT = "위에서 아래로 한 줄로 읽는 흐름도입니다. 파란 상자 before_runnable with_retry 시도 세 번까지에서 회색 상자 시도 1 default_model이 요청 세 번, 회색 상자 시도 2 default_model이 요청 세 번, 회색 상자 시도 3 default_model이 요청 세 번을 차례로 지나, 빨간 상자 서버가 받은 요청 아홉 번과 노란 상자 받은 오류는 OpenAIRateLimitError 하나로 갈라지는 그림"
FIG3_CAP = "with_retry가 세 번 부를 때마다 모델 객체가 요청을 셋씩 보내, 한 번 부른 호출 객체가 서버에 요청 아홉을 보냈습니다."
FIG3_READ = """위에서 아래로 읽습니다.
파란 상자는 노트북 4절에서 만든 호출 객체이고, 빨간 상자는 4절에서 출력한 Before의 결함 결과인 서버 요청 수입니다.
노란 상자는 셀이 받아 출력한 오류로, 요청은 아홉 번 갔지만 오류는 하나만 왔습니다.
가운데 회색 상자 셋은 시도마다 요청 셋이 갔다는 것을, 3절의 수와 시도 횟수로 셈한 차례입니다.
노트북은 시도마다 따로 세지 않았고, 모두 합친 수만 세었습니다."""

FIG4 = "04-4-두-곳과-한-곳의-다시-보내기"
FIG4_ALT = "맨 위 회색 상자 두 칸 공통 같은 연습용 서버 같은 문의 글 with_retry 시도 세 번까지 아래에 칸 둘이 있습니다. 왼쪽 칸 Before 두 곳에 겹침에는 초록 상자 default_model 안에서 두 번 더 보냄에서 빨간 상자 서버가 받은 요청 아홉 번 3 곱하기 3으로 이어집니다. 오른쪽 칸 After 한 곳에만에는 초록 상자 zero_model max_retries 0에서 노란 상자 서버가 받은 요청 세 번 1 곱하기 3으로 이어지는 그림"
FIG4_CAP = "같은 with_retry를 붙여도, 안에서 다시 보내는 모델 객체면 요청 아홉 번이고 다시 보내지 않는 모델 객체면 세 번이었습니다."
FIG4_READ = """맨 위 회색 상자는 두 칸이 함께 쓴 조건입니다.
왼쪽 칸이 Before, 오른쪽 칸이 After이고, 칸마다 위가 안쪽 모델 객체, 아래가 노트북 4·5절의 출력입니다.
빨간 상자는 Before의 결함 결과이고, 노란 상자는 After에서 받은 오류와 함께 출력한 수입니다."""

FIG5 = "04-5-한꺼번에-보내는-수만-바꾼-두-실행"
FIG5_ALT = "맨 위 회색 상자 두 칸 공통 02절 문의 글 다섯 After 호출 객체 문의마다 요청 세 번 아래에 칸 둘이 나란히 있습니다. 왼쪽 칸 설정 없음에는 초록 상자 batch 설정 없음에서 노란 상자 한꺼번에 처리 중이던 문의 다섯 서버가 받은 요청 열다섯 번으로 이어집니다. 오른쪽 칸 값 바꿔 보기에는 파란 상자 max_concurrency 2에서 노란 상자 한꺼번에 처리 중이던 문의 둘 서버가 받은 요청 열다섯 번으로 이어지고, 그 아래 회색 상자 기다린 문의는 일꾼 모음의 대기열에 설치판 소스로 확인이 있는 그림"
FIG5_CAP = "설정 max_concurrency를 2로 두자, 서버가 받은 요청 열다섯 번은 그대로이고 한꺼번에 처리되던 문의만 다섯에서 둘로 줄었습니다."
FIG5_READ = """맨 위 회색 상자는 두 칸에 공통인 조건입니다.
왼쪽 칸이 설정 없이 보낸 노트북 6절 첫 셀, 오른쪽 칸이 값 하나만 바꾼 둘째 셀이고, 파란 상자가 바꾼 값입니다.
노란 상자는 두 셀의 출력이고, 오른쪽 맨 아래 회색 상자는 설치판 소스로만 확인한 사실입니다."""

ILLU = "04-6-꽂는-자리-둘과-줄-선-배터리"
ILLU_ALT = "흰 바탕에 크림색 충전기 하나가 왼쪽에 있고, 위쪽 칸 둘에 산호색 배터리가 하나씩 꽂혀 있습니다. 배터리 윗부분에는 은색 단자 뚜껑이 있고, 충전기 앞면에는 큰 동그란 표시등 둘이 파랗게 켜져 있습니다. 충전기 오른쪽에는 같은 산호색 배터리 셋이 한 줄로 서 있고, 배터리마다 아래쪽의 작은 표시등이 꺼져 있습니다. 사람·손·글자·숫자·화살표·전선은 없는 그림"
ILLU_CAP = "꽂는 자리 둘에는 배터리가 꽂혀 파란 불이 켜졌고, 나머지 셋은 옆에 줄을 서서 기다립니다."
# 2차 job c3c6d588-5c49-40a2-83a5-bbd45fdd7723 채택(재생성 1 — 1차 a58166e5…는 충전기가 빵 굽는 기계처럼 보여 탈락) — 저장 PNG를 열어 센 개수로 적음(꽂힌 둘·파란 불 둘 / 줄 선 셋·꺼진 불 셋)
ILLU_READ = "충전기의 꽂는 자리는 둘이고, 두 자리 모두 배터리가 꽂혀 앞면의 파란 불 둘이 켜져 있습니다. 옆에는 배터리 셋이 한 줄로 서 있고, 셋 모두 작은 불이 꺼져 있습니다. 배터리는 모두 다섯이지만, 한꺼번에 채우는 것은 둘뿐입니다. 꽂는 자리 둘이 설정 <code>max_concurrency</code> 2이고, 줄 선 셋이 대기열에서 차례를 기다리는 문의입니다. 그림의 배터리 다섯은 노트북 6절의 문의 다섯과 짝지은 비유이고, 기다리는 시간은 그리지 않았습니다."

METAPHOR = """<p>배터리를 꽂는 자리가 둘뿐인 충전기가 있습니다. 배터리 다섯 개를 채우려면 두 개를 먼저 꽂고, 나머지 셋은 옆에 줄을 세워 둡니다. 꽂힌 배터리가 다 차서 빠지면, 줄 맨 앞의 배터리가 그 자리에 들어갑니다. 꽂는 자리를 늘리지 않는 한, 채우는 중인 배터리는 둘을 넘지 않습니다.</p><p>꽂는 자리 수가 한꺼번에 보내는 수이고, 옆에 선 줄이 대기열입니다. 배터리 하나가 요청을 보내야 하는 문의 하나입니다. 자리를 둘로 정해도 채울 배터리는 다섯 그대로입니다. 설정 <code>max_concurrency</code>도 요청 수를 줄이지 않고, 한꺼번에 보내는 수만 정합니다.</p><p>비유와 다른 점도 있습니다. 충전기는 배터리를 거절하지 않지만, 이 절의 연습용 서버는 모든 요청을 429로 거절합니다. 그래서 문의마다 다시 보내기가 일어나고, 문의 하나가 끝나기까지 기다리는 시간이 생깁니다.</p>"""

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 늘 429를 보내는 연습용 서버를 띄우고, 모델 객체를 한 번 부를 때 서버에 가는 요청 수를 셉니다.
2. 다시 보내기를 두 곳에 겹친 코드(Before)와 한 곳에만 둔 코드(After)의 요청 수를 견줍니다.
3. 문의 다섯을 한꺼번에 보낼 때, 값 `max_concurrency` 하나만 바꿔 한꺼번에 처리되는 수를 봅니다.

**준비물** — 이 노트북은 OpenAI 서비스에 요청을 보내지 않고, API 키도 읽지 않습니다.
모델 객체는 가짜 키로 만들고, 요청은 이 컴퓨터 안의 연습용 서버로만 보냅니다.
연습용 서버는 실습 폴더 `notebooks/`의 파일 `always_429_server.py`입니다.
이 서버는 어떤 요청에도 상태 코드 429만 보내고, 모델의 답은 보내지 않습니다.
제공자의 요청 제한을 흉내 낸 서버라, 이 절의 429는 제공자가 보낸 것이 아닙니다.

노트북이 이 서버를 자식 프로세스로 띄우고, 마지막 셀에서 끕니다.
서비스에 보내는 요청이 없어 요금은 들지 않습니다.
다시 보내기 전에 기다리는 셀이 있어, 몇 셀은 곧바로 끝나지 않습니다.
걸린 시간은 재지 않았고, 이 노트북은 파일을 쓰지 않습니다.
실습 폴더의 도구 파일 `cost_tools.py`에서 함수 하나를 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
셋은 langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0입니다.
나머지 둘은 openai 3.13.0과 httpx 0.28.1입니다.
다섯 모두 실습 폴더 잠금과 같은 버전입니다.

교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 버전과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2절의 연습용 서버와 3절의 요청 수를 함께 봅니다.
4절 Before와 5절 After, 6절 값 바꿔 보기는 실습 시간에 실행합니다.

실습 폴더 `labs/part7/ch34-cost-rate-limits`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md(r"""## 1. 준비

제목의 백오프는 다시 보내기 전에 기다리는 시간을 두 배씩 늘리는 방법입니다.
큐는 차례를 기다리는 대기열이고, 동시성은 한꺼번에 보내는 요청의 수입니다.
이 절은 세 말을 제목에만 두고, 본문에서는 풀어 쓴 말을 씁니다.

요청 제한(rate limit)은 제공자가 정한 분당 요청 수와 토큰 수의 상한입니다.
Ch 6 05절에서 배운 말이고, 상한을 넘은 요청은 상태 코드 429를 받습니다.
요청이 실패했을 때 같은 요청을 다시 보내는 일은 다시 보내기(재시도)라고 부릅니다.
Ch 6 05절의 「다시 시도」와 같은 뜻입니다.

첫 셀은 패키지 다섯을 설치하고 설치된 버전을 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md(r"""**결과 읽기** — 출력 줄 `openai: 3.13.0`과 `httpx: 0.28.1`이 보입니다.
패키지 openai는 LangChain 모델 객체가 요청을 보낼 때 쓰는 OpenAI 클라이언트입니다.
패키지 httpx는 Ch 28 03절에서 쓴 HTTP 요청 도구로, 연습용 서버에 센 수를 물을 때 씁니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
Ch 28 03절에서 배운 함수 `wait_for_port`는 도구 파일 `cost_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md(r"""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: wait_for_port`가 보입니다.
이 함수는 Ch 28 03절 셀의 함수를 주석과 본문 글자 그대로 옮긴 것으로, 이 절에서 도구 파일에 더했습니다.
이름 `ModelRateLimitError`는 LangChain이 요청 제한 오류에 붙인 공통 이름입니다.
Ch 6 05절의 `ModelTimeoutError`와 같은 곳에 있습니다.

앞에서 배운 함수는 `cost_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

이 절은 모델 서비스에 요청을 보내지 않아, 키를 읽는 셀을 두지 않았습니다.

## 2. 늘 429를 보내는 연습용 서버

실제 요청 제한은 조직과 프로젝트마다 정해지고, 교재 실습의 요청 몇 번으로는 닿지 않습니다.
그래서 이 절은 연습용 서버를 이 컴퓨터 안에 띄웁니다.
연습용 서버는 어떤 요청이 와도 상태 코드 429만 보내는 작은 서버입니다.
소방 훈련의 연습용 경보처럼, 진짜 불은 없어도 대응은 실제로 해 봅니다.
Ch 16 05절의 실패 흉내처럼 제공자의 요청 제한을 흉내 내고, 모델의 답은 보내지 않습니다.

서버는 받은 요청 가운데 모델에 보내는 요청만 셉니다.
센 수는 응답 머리 `practice-count`에 적어 보냅니다.
머리는 HTTP 응답에서 본문 앞에 붙는 이름과 값 줄입니다.
주소 끝이 `/reset`인 요청을 받으면, 서버는 센 수를 0으로 맞춥니다.

다음 셀은 실습 폴더의 위치를 찾습니다.
연습용 서버 파일이 실습 폴더 `notebooks/`에 있기 때문입니다."""),
        code(FIND_LAB),
        md(r"""**결과 읽기** — 출력 줄 `실습 폴더를 찾았는가: True`가 보입니다.
첫 후보 `..`는 `notebooks/` 폴더에서 열었을 때 맞는 자리입니다.
둘째 `.`는 실습 폴더 맨 위, 셋째는 프로젝트 맨 위에서 열었을 때 맞습니다.
고른 후보는 연 자리마다 달라서 출력하지 않습니다.

다음 셀은 서버를 띄울 포트와 주소, 명령을 정합니다.
포트는 한 컴퓨터 안에서 프로그램마다 나눠 쓰는 번호입니다.
띄우기 전에 Ch 28 03절처럼, 그 포트에서 이미 듣는 프로그램이 있는지 봅니다.
함수 `wait_for_port`는 정한 초 동안 포트에 연결해 보고, 열려 있으면 `True`를 내놓습니다."""),
        code(PLAN),
        md(r"""**결과 읽기** — 출력 줄 `띄우기 전에 이 포트에서 듣는 프로그램이 있는가: False`가 보입니다.
포트가 비어 있어, 셀 끝의 `assert`를 지났습니다.
포트 번호와 주소는 출력하지 않았습니다.

주소 `base_url` 끝의 `/v1`은 OpenAI 요청 주소의 앞부분과 같은 모양입니다.
모델 객체는 이 주소 뒤에 `/chat/completions`를 붙여 요청을 보냅니다.

다음 셀은 서버 파일을 자식 프로세스로 띄웁니다.
함수 `subprocess.Popen`은 Ch 28 03절처럼 프로그램을 켜 두고, 끝나기를 기다리지 않습니다.
서버가 요청마다 표준 오류로 남기는 한 줄은 버립니다.
포트가 열린 뒤에는 메서드 `poll`로, 띄운 서버가 아직 돌고 있는지 봅니다."""),
        code(START),
        md(r"""**결과 읽기** — 출력 줄 `서버가 준비되었는가: True`와 `띄운 서버가 살아 있는가: True`가 보입니다.
연습용 서버가 자식 프로세스로 떠서 포트를 열었고, 지금도 돌고 있습니다.
이 서버는 7절의 마지막 셀에서 끕니다.

이 셀만 두 번 실행하면, 앞에서 띄운 서버가 포트를 쥔 채 남습니다.
그때는 마지막 셀로 서버를 끈 뒤 앞 셀부터 실행하고, 끄지 못했으면 커널을 다시 시작합니다.

다음 셀은 연습용 서버에 센 수를 0으로 맞추는 요청을 보냅니다.
Ch 28 03절처럼 httpx로 요청을 보내고, 받은 응답을 그대로 봅니다.
함수 `httpx.post`는 상태 코드가 429여도 오류를 내지 않고 응답을 내놓습니다."""),
        code(CHECK),
        md(r"""**결과 읽기** — 출력 줄 `상태 코드: 429`와 `머리 practice-count: 0`이 보입니다.
센 수를 0으로 맞추는 요청에도 서버는 429를 보냈습니다.
오류 글 `연습용 서버는 늘 429를 보냅니다.`는 서버 파일에 적어 둔 글입니다.
이 글은 OpenAI 오류 글과 같은 모양의 JSON으로 옵니다.

## 3. 모델 객체 한 번이 보내는 요청 수

Ch 6 05절은 인자 `max_retries`를 적지 않으면 openai 클라이언트의 값 2가 쓰인다는 것을 출력으로 봤습니다.
그러나 모델 객체 안에서 다시 보낸 요청의 수는 세지 못했습니다.
이 절은 연습용 서버가 받은 요청 수로 그 수를 셉니다.

다음 셀은 연습용 서버가 센 수를 묻는 함수를 정의합니다.
주소 끝이 `/count`인 요청은 서버가 세지 않고, 센 수만 머리에 적어 보냅니다."""),
        code(DEF_READ),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `httpx.get`은 주소에 GET 요청을 보내고 응답을 내놓습니다.
속성 `headers`는 응답 머리를 딕셔너리처럼 담습니다.
머리 값은 글이라, 함수 `int`로 정수로 바꿉니다.

다음 셀은 호출 객체에 문의 글 하나를 보내는 함수를 정의합니다.
Ch 6 05절처럼 오류 이름 하나만 받아, 셀이 끝까지 실행되게 합니다.
받는 오류는 요청 제한 오류 `ModelRateLimitError` 하나입니다."""),
        code(DEF_SEND),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
연습용 서버는 답을 보내지 않아, 이 함수는 늘 오류를 받습니다.
속성 `status_code`는 오류가 난 응답의 상태 코드입니다.
다른 오류는 받지 않아, 실제 프로그램이라면 거기서 멈춥니다.

다음 셀은 보낼 문의 글과, 모델 객체에 넣을 가짜 키를 정합니다.
문의 글은 01절의 첫 문의 글입니다."""),
        code(QUESTION),
        md(r"""**결과 읽기** — 출력 줄 `가짜 키: not-a-real-key`가 보입니다.
교재에서 지어낸 글이라 실제 키가 아니고, 이 절은 이 키로 OpenAI 서비스에 보내지 않습니다.
요청은 모두 연습용 서버로만 가고, 연습용 서버는 키를 보지 않습니다.

다음 셀은 연습용 서버 주소와 가짜 키로 모델 객체를 만듭니다.
설정은 과정 표준 그대로이고, 인자 `base_url`로 요청을 보낼 곳만 바꿉니다.
Ch 6 05절처럼 인자 `max_retries`는 적지 않고, 두 자리의 값을 봅니다.
객체를 만들 때는 요청이 나가지 않습니다."""),
        code(MODEL_DEFAULT),
        md(r"""**결과 읽기** — 출력 줄 `모델 객체 max_retries: None`과 `openai 클라이언트 max_retries: 2`가 보입니다.
모델 객체에 값을 적지 않아, 요청을 보내는 openai 클라이언트의 기본값 2가 쓰입니다.
Ch 6 05절과 같은 출력입니다.
이 노트북의 출력은 """ + RUN_DATE + r"""에 실행한 결과입니다.

설치판 openai 3.13.0의 파일 `_constants.py` 8행이 이 기본값 `DEFAULT_MAX_RETRIES = 2`입니다.
설치판 langchain-openai 1.6.0은 값을 적지 않으면 클라이언트에 넘기지 않습니다.

다음 셀은 서버가 센 수를 0으로 맞춘 뒤, 이 모델 객체를 한 번 부릅니다.
실행 전에 예상해 봅니다.
서버는 요청을 몇 번 받을까요?"""),
        code(SEND_DEFAULT),
        md(r"""**결과 읽기** — 출력 줄 `서버가 받은 요청 수: 3`이 보입니다.
모델 객체를 한 번 불렀지만, 서버에는 요청이 세 번 갔습니다.
첫 요청이 429를 받자, openai 클라이언트가 같은 요청을 두 번 더 보냈습니다.
받은 오류는 `OpenAIRateLimitError`로, `ModelRateLimitError`의 한 종류입니다.

설치판 소스로 보면, 클라이언트는 기다리는 시간을 두 배씩 늘리는 방법(지수 백오프)으로 기다립니다.
처음 0.5초에서 시작해 8초까지 늘리고, 그 값에 0.75~1 사이의 무작위 값을 곱합니다.
서버가 머리 `Retry-After`로 120초 이하를 적어 보내면 그만큼 기다립니다.
연습용 서버는 이 머리를 보내지 않았고, 기다린 시간은 재지 않았습니다.

다음 셀은 모델 객체 안에서 다시 보내지 않게, 인자 `max_retries=0`을 적은 모델 객체를 만듭니다."""),
        code(MODEL_ZERO),
        md(r"""**결과 읽기** — 출력 줄 `모델 객체 max_retries: 0`과 `openai 클라이언트 max_retries: 0`이 보입니다.
모델 객체에 적은 0이 openai 클라이언트까지 넘어갔습니다.
나머지 설정은 앞 모델 객체와 같습니다.

다음 셀은 같은 방법으로 이 모델 객체를 한 번 부르고, 서버가 받은 요청 수를 봅니다."""),
        code(SEND_ZERO),
        md(r"""**결과 읽기** — 출력 줄 `서버가 받은 요청 수: 1`이 보입니다.
모델 객체 안에서 다시 보내지 않아, 첫 요청 한 번만 서버에 갔습니다.
받은 오류와 상태 코드는 앞 셀과 같습니다.
셀마다 센 수를 0으로 맞추고 시작해, 앞 셀의 요청이 이 셀의 수에 섞이지 않습니다.

## 4. 다시 보내기를 두 곳에 겹치기 (Before)

Ch 6 05절의 메서드 `with_retry`는 호출 객체에 다시 보내기 규칙을 붙입니다.
인자 `stop_after_attempt`에는 첫 요청을 포함한 전체 시도 횟수를 적습니다.
모델 객체 안의 다시 보내기를 그대로 둔 채 이 메서드를 붙이면, 다시 보내기가 두 곳에 겹칩니다.
이 절에서는 이것을 겹친 다시 보내기라고 부릅니다.

반송된 편지를 집배원이 다시 나르고, 보낸 사람도 다시 부치는 것과 같습니다.
이 절 코드에서는 openai 클라이언트의 다시 보내기와 메서드 `with_retry`가 겹칩니다.
다음 셀은 3절의 `default_model`에, 요청 제한 오류일 때 모두 3번까지 부르는 `with_retry`를 붙입니다.""", lesson_part="before"),
        code(BEFORE_BUILD, lesson_part="before"),
        md(r"""**결과 읽기** — 출력 줄 `호출 객체 종류: RunnableRetry`가 보입니다.
Ch 6 05절처럼 다시 보내기 규칙을 붙인 호출 객체입니다.
객체를 만들 때는 요청이 나가지 않습니다.

다음 셀은 이 호출 객체를 한 번 부르고, 서버가 받은 요청 수를 봅니다.
실행 전에 예상해 봅니다.
3절의 모델 객체는 한 번 부를 때 요청 셋을 보냈고, 이 호출 객체는 그 모델 객체를 3번까지 부릅니다.
메서드 `with_retry`도 시도 사이에 기다려, 이 셀은 곧바로 끝나지 않습니다.""", lesson_part="before"),
        code(BEFORE_SEND, lesson_part="before"),
        md(r"""**결과 읽기** — 출력 줄 `서버가 받은 요청 수: 9`가 보입니다.
호출 객체를 한 번 불렀을 뿐인데, 요청 제한에 걸린 서버에 요청이 아홉 번 갔습니다.
메서드 `with_retry`가 모델 객체를 세 번 불렀고, 모델 객체는 부를 때마다 요청을 셋씩 보냈습니다.
마지막에 받은 오류는 `OpenAIRateLimitError` 하나라, 오류만 보면 요청이 몇 번 갔는지 모릅니다.
공식 안내는 실패한 요청도 분당 한도에 들어간다고 적습니다.

다음 셀은 3절에서 센 수에 시도 횟수를 곱해, 이 수와 견줍니다.""", lesson_part="before"),
        code(BEFORE_MATH, lesson_part="before"),
        md(r"""**결과 읽기** — 출력 줄 `모델 객체 한 번의 요청 수 × 시도 수: 9`와 `Before의 요청 수와 같은가: True`가 보입니다.
두 곳의 횟수가 더해지지 않고 곱해졌습니다.
Ch 6 05절은 이 수를 3 × 3 = 9로 셈만 했고, 이 절은 서버에서 실제로 셌습니다.
Ch 22 04절이 적은 「시도 횟수가 곱해질 수 있습니다」도 이 모양입니다.

## 5. 다시 보내기를 한 곳에만 두기 (After)

고치는 방법은 다시 보내기를 한 곳에만 두는 것입니다.
Ch 6 05절 노트북 7절도, 안에서 다시 보내지 않는 모델 객체를 `with_retry` 안에서 불렀습니다.
다음 셀은 3절의 `zero_model`에 같은 `with_retry`를 붙입니다.""", lesson_part="after"),
        code(AFTER_BUILD, lesson_part="after"),
        md(r"""**결과 읽기** — 출력 줄 `호출 객체 종류: RunnableRetry`가 보입니다.
시도 횟수 `retry_attempts`는 Before와 같은 값입니다.
바꾼 것은 안쪽 모델 객체 하나입니다.

다음 셀은 이 호출 객체를 한 번 부르고, 서버가 받은 요청 수를 봅니다.""", lesson_part="after"),
        code(AFTER_SEND, lesson_part="after"),
        md(r"""**결과 읽기** — 출력 줄 `서버가 받은 요청 수: 3`이 보입니다.
메서드 `with_retry`가 모델 객체를 세 번 불렀고, 모델 객체는 부를 때마다 요청을 하나씩 보냈습니다.
같은 문의 글과 같은 시도 횟수로, Before의 9가 3으로 줄었습니다.
받은 오류는 Before와 같은 `OpenAIRateLimitError`입니다.

다음 셀은 After의 수도 곱셈으로 견줍니다.""", lesson_part="after"),
        code(AFTER_COMPARE, lesson_part="after"),
        md(r"""**결과 읽기** — 출력 줄 `After의 요청 수와 같은가: True`와 `Before 요청 수 ÷ After 요청 수: 3`이 보입니다.
After도 모델 객체 한 번의 요청 수에 시도 횟수를 곱한 값이었고, 안쪽이 1이라 곱이 3입니다.
Before 쪽은 After 쪽의 세 배를 보냈습니다.
연산자 `//`는 나눈 몫을 정수로 냅니다.

## 6. 값 바꿔 보기 — 한꺼번에 보내는 수

문의가 여럿이면 하나씩 보내지 않고 한꺼번에 보내기도 합니다.
한꺼번에 보내는 수는 동시에 처리 중인 요청의 수입니다.
계산대 두 곳에 손님이 줄을 서면, 계산 중인 손님은 둘뿐인 것과 같습니다.
차례를 기다리는 나머지 손님의 줄은 대기열이라고 부릅니다.
이 절 코드에서는 메서드 `batch`의 설정 `max_concurrency`가 한꺼번에 보내는 수의 상한입니다.

메서드 `batch`는 02절 4블록 마지막 단락에서 본 메서드입니다.
요청 여러 개를 곧바로 함께 보내며, 일괄 처리(Batch API)와 다릅니다.
다음 셀은 문의 글 하나를 After의 호출 객체로 보내며, 처리 중인 문의 수를 적는 함수를 정의합니다.""", lesson_part="after"),
        code(DEF_ASK, lesson_part="after"),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수는 시작할 때 목록 `active`에 문의 글을 넣고, 그때의 목록 길이를 `peaks`에 적습니다.
끝날 때는 메서드 `remove`로 그 문의 글을 목록에서 뺍니다.
Ch 6 05절의 함수 `ask_current_model`처럼, 셀 바깥에서 만든 목록과 호출 객체를 함수 안에서 씁니다.

다음 셀은 02절의 문의 글 다섯을 담고, 이 함수를 호출 객체로 감쌉니다.
Ch 6 05절처럼 `RunnableLambda`로 감싸면 메서드 `batch`를 쓸 수 있습니다.""", lesson_part="after"),
        code(INQUIRIES, lesson_part="after"),
        md(r"""**결과 읽기** — 출력 줄 `문의 글 수: 5`와 `호출 객체 종류: RunnableLambda`가 보입니다.
문의 글 다섯은 02절 일괄 처리에 맡긴 문의 글과 글자까지 같습니다.

다음 셀은 설정 없이 문의 다섯을 한꺼번에 보냅니다.
문의마다 After의 호출 객체가 요청 셋을 보내니, 서버가 받는 요청은 15번일 것입니다.
실행 전에 예상해 봅니다.
한꺼번에 처리 중이던 문의 수의 가장 큰 값은 얼마일까요?""", lesson_part="after"),
        code(BATCH_NONE, lesson_part="after"),
        md(r"""**결과 읽기** — 출력 줄 `한꺼번에 처리 중이던 문의 수의 가장 큰 값: 5`와 `서버가 받은 요청 수: 15`가 보입니다.
설정이 없자 문의 다섯이 모두 한꺼번에 처리되었습니다.
출력 줄 `받은 오류 수: 5`로, 문의마다 요청 제한 오류를 하나씩 받았습니다.
함수 `max`는 목록에서 가장 큰 값을 내놓습니다.

설치판 소스로 보면, 설정이 없을 때 메서드 `batch`는 Python이 정한 수만큼 일꾼을 둡니다.
그 수는 CPU 수에 4를 더한 값이고, 32까지입니다.
컴퓨터에 CPU가 하나여도 다섯이라, 문의 다섯은 한꺼번에 처리됩니다.
문의가 많으면 그만큼 많은 요청이 한꺼번에 서버로 갑니다.

**값 바꿔 보기** — 바꿀 값은 설정 `max_concurrency` 하나이고, 없음에서 2로 바꿉니다.
실행 전에 예상해 봅니다.
한꺼번에 처리 중이던 수는 2를 넘지 않고, 서버가 받는 요청 수는 그대로일 것입니다.
나머지 문의는 차례를 기다려서, 이 셀은 곧바로 끝나지 않습니다.""", lesson_part="after"),
        code(BATCH_TWO, lesson_part="after"),
        md(r"""**결과 읽기** — 출력 줄 `한꺼번에 처리 중이던 문의 수의 가장 큰 값: 2`와 `서버가 받은 요청 수: 15`가 보입니다.
예상대로 한꺼번에 처리된 문의는 둘을 넘지 않았고, 요청 수는 앞 셀과 같았습니다.
출력 줄 `받은 오류 수: 5`로 다섯 모두 처리되었으니, 셋은 앞 문의가 끝나기를 기다렸다가 처리되었습니다.
설정 `max_concurrency`는 요청 수를 줄이지 않고, 한꺼번에 보내는 수만 줄입니다.

설치판 소스로 보면, 차례를 기다리는 문의는 Python 일꾼 모음 안의 대기열에 담깁니다.
노트북은 대기열을 직접 보지 않았고, 한꺼번에 처리 중이던 수로만 확인했습니다.

## 7. 연습용 서버 끄기

마지막 셀은 연습용 서버를 끕니다.
메서드 `terminate`는 프로그램에 끝내라는 신호를 보냅니다.
메서드 `wait`는 프로그램이 끝날 때까지 기다려 종료 코드를 내놓습니다.
Ch 28 03절의 마지막 셀과 같은 모양입니다.""", lesson_part="after"),
        code(STOP, lesson_part="after"),
        md(r"""**결과 읽기** — 출력 줄 `종료 코드: -15`와 `포트가 아직 열려 있는가: False`가 보입니다.
음수 종료 코드는 신호를 받아 끝났다는 표시이고, 15는 끝내라는 신호의 번호입니다.
서버가 연 포트도 닫혀, 이 절에서 띄운 서버는 남지 않았습니다.

**결론** — 같은 연습용 서버와 같은 문의 글, 같은 시도 횟수 3에서 안쪽 모델 객체만 달랐습니다.
다시 보내기를 두 곳에 겹친 Before는 한 번 부를 때 요청 9번을, 한 곳에만 둔 After는 3번을 보냈습니다.
겹친 다시 보내기는 요청 수를 곱으로 늘려, 요청 제한에 걸린 서버에 더 많은 요청을 보냅니다.
값 바꿔 보기에서 설정 `max_concurrency`를 2로 두자, 요청 수 15는 그대로이고 한꺼번에 처리되는 문의만 둘로 줄었습니다.

## 정리

1. 인자 `max_retries`를 적지 않은 모델 객체는 한 번 부를 때 서버에 요청 3번을 보냈습니다.
2. 모델 객체 안의 다시 보내기에 `with_retry`를 겹치자 요청이 9번으로 곱해졌고, 한 곳에만 두자 3번이었습니다.
3. 설정 `max_concurrency`는 요청 수를 그대로 두고, 한꺼번에 처리되는 수만 정한 값 아래로 막았습니다.

05절에서는 요청을 보내기 전에 비용 상한으로 막는 예산 가드와 95 백분위수를 다룹니다.""", lesson_part="after"),
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
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(01·02 생성기와 같은 함수)."""
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


L_CH06_05 = "../../part2/ch06-langchain-start/05-타임아웃-재시도-폴백.html"
L_CH16_04 = "../../part4/ch16-guardrails/04-호출-한도와-비용-상한.html"
L_CH16_05 = "../../part4/ch16-guardrails/05-재시도-폴백과-감사-로그.html"
L_CH22_04 = "../../part6/ch22-middleware/04-호출-한도와-재시도-폴백.html"
L_CH28_03 = "../../part6/ch28-mcp/03-stdio와-원격-전송-권한-경계.html"
L_CH30_01 = "../ch30-fastapi-serving/01-비동기-라우팅과-스키마.html"
L_02 = "02-Batch-API.html"
L_03 = "03-모델-라우팅.html"
L_05 = "05-예산-가드와-p95.html"


def link(href: str, text: str) -> str:
    return '<a href="' + href + '">' + text + "</a>"


PREV_ROWS = [
    (link(L_CH06_05, "Ch 6 05절"), "인자 <code>max_retries</code>를 적지 않으면 openai 클라이언트 값 2가 쓰임 · 메서드 <code>with_retry</code>와 <code>stop_after_attempt=3</code> · 두 곳을 함께 두면 9번까지라는 셈 · 요청 제한(429)은 실행하지 않음", "3절에서 서버가 받은 요청 수로 셈 · 4절에서 9를 실제로 셈"),
    (link(L_CH22_04, "Ch 22 04절"), "<code>ModelRetryMiddleware</code>와 모델 객체의 <code>max_retries</code>를 함께 쓰면 시도 횟수가 곱해질 수 있음(실행 안 함)", "4절에서 곱해지는 것을 출력으로 봄"),
    (link(L_CH16_04, "Ch 16 04절"), "호출 한도 — 우리 코드가 정한, 한 대화에서 모델을 부를 수 있는 횟수", "요청 제한은 제공자가 정한 상한이라 다른 말"),
    (link(L_CH16_05, "Ch 16 05절"), "정해 둔 횟수만큼 오류를 내는 실패 흉내", "연습용 서버의 429도 흉내"),
    (link(L_CH28_03, "Ch 28 03절"), "서버 파일을 자식 프로세스로 띄우기 · <code>wait_for_port</code> · <code>poll</code> · <code>terminate</code>·<code>wait</code>", "2절·7절 — <code>wait_for_port</code>는 도구 파일에서 가져옴"),
    (link(L_02, "02절"), "LangChain 메서드 <code>batch</code>는 곧바로 함께 보내며 일괄 처리(Batch API)와 다름", "6절 값 바꿔 보기 · 문의 글 다섯"),
    (link(L_03, "03절"), "모델마다 요청 수를 셈", "이 절은 서버가 받은 요청 수를 셈"),
]

TERM_ROWS = [
    ("연습용 서버", "어떤 요청에도 상태 코드 429만 보내는, 이 컴퓨터 안의 작은 서버입니다. 제공자의 요청 제한을 흉내 냅니다.", "<code>always_429_server.py</code> — 센 수를 머리 <code>practice-count</code>에 적음"),
    ("겹친 다시 보내기", "다시 보내기를 두 곳에 두어, 요청 수가 곱해지는 것입니다.", "4절 Before — 서버가 받은 요청 수 <code>9</code>"),
    ("기다리는 시간을 두 배씩 늘리기(지수 백오프)", "실패할 때마다 다시 보내기 전 기다리는 시간을 두 배씩 늘리는 방법입니다.", "openai 클라이언트 0.5초부터 · <code>with_retry</code> 1초부터(설치판 소스)"),
    ("한꺼번에 보내는 수", "동시에 처리 중인 요청의 수입니다.", "설정 <code>max_concurrency</code> — 설정 없이 <code>5</code>, 2로 두면 <code>2</code>"),
    ("대기열", "차례를 기다리는 요청의 줄입니다.", "설정 2에서 앞 문의가 끝나기를 기다린 문의 셋"),
]

COMPARE_ROWS = [
    ("안쪽 모델 객체", "<code>default_model</code> — openai 클라이언트 <code>max_retries: 2</code>", "<code>zero_model</code> — openai 클라이언트 <code>max_retries: 0</code>"),
    ("with_retry 시도 횟수", "3", "3"),
    ("받은 오류", "<code>OpenAIRateLimitError</code>", "<code>OpenAIRateLimitError</code>"),
    ("서버가 받은 요청 수", "<code>9</code>", "<code>3</code>"),
    ("모델 객체 한 번의 요청 수 × 시도 수와 같은가", "<code>True</code>(3 × 3)", "<code>True</code>(1 × 3)"),
]

VARY_ROWS = [
    ("받은 오류 수", "<code>5</code>", "<code>5</code>"),
    ("한꺼번에 처리 중이던 문의 수의 가장 큰 값", "<code>5</code>", "<code>2</code>"),
    ("서버가 받은 요청 수", "<code>15</code>", "<code>15</code>"),
]

LOOK_B5 = "3절에서 <code>openai 클라이언트 max_retries: 2</code>와 <code>서버가 받은 요청 수: 3</code>을 찾습니다. 인자 <code>max_retries=0</code>을 적은 모델 객체는 <code>서버가 받은 요청 수: 1</code>입니다. 두 셀 모두 받은 오류는 <code>OpenAIRateLimitError</code>, 상태 코드는 <code>429</code>입니다."
LOOK_B6 = "Before 셀의 <code>서버가 받은 요청 수: 9</code>와 After 셀의 <code>서버가 받은 요청 수: 3</code>을 견줍니다. 값 바꿔 보기의 두 셀은 <code>서버가 받은 요청 수: 15</code>가 같고, 한꺼번에 처리 중이던 수만 <code>5</code>와 <code>2</code>로 다릅니다. 마지막 셀의 <code>포트가 아직 열려 있는가: False</code>로 서버가 꺼졌는지도 봅니다."


def src_html() -> str:
    prev = table_html(["앞 절", "배운 것", "이 절에서 이어지는 곳"], PREV_ROWS)
    terms = table_html(["말", "뜻", "이 절에서 보이는 모습"], TERM_ROWS)
    compare = table_html(["견준 것", "Before — 두 곳에 겹침", "After — 한 곳에만"], COMPARE_ROWS)
    vary = table_html(["값 바꿔 보기", "설정 없음", "<code>max_concurrency</code> 2"], VARY_ROWS)
    return """<!--meta: 강의 0.6h | 실습 1h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 5 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>연습용 서버가 받은 요청 수로, 모델 객체 안에서 다시 보낸 요청을 셀 수 있습니다.</li>
<li>다시 보내기를 두 곳에 겹치면 요청 수가 곱해진다는 것을 출력으로 설명하고, 한 곳에만 두도록 고칠 수 있습니다.</li>
<li>설정 <code>max_concurrency</code>로 한꺼번에 보내는 수를 정하고, 요청 수와 가려 말할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>모델 제공자는 조직과 프로젝트마다 분당 요청 수와 토큰 수의 상한을 둡니다. 이 상한이 요청 제한이고, 넘은 요청은 상태 코드 429로 거절됩니다. 공식 안내는 실패한 요청도 분당 한도에 들어가, 계속 다시 보내도 풀리지 않는다고 적습니다. 그런데 다시 보내는 코드가 두 곳에 있으면, 한 번 부를 때 보내는 요청이 곱으로 늘어납니다.</p><p>제목의 백오프는 다시 보내기 전에 기다리는 시간을 두 배씩 늘리는 방법입니다. 큐는 차례를 기다리는 대기열이고, 동시성은 한꺼번에 보내는 요청의 수입니다. 이 절은 세 말을 제목에만 두고, 본문에서는 풀어 쓴 말을 씁니다. 요청 제한은 """ + link(L_CH06_05, "Ch 6 05절") + """에서 배운 말이고, 이 절은 그 429를 연습용 서버에서 받아 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>""" + link(L_CH06_05, "Ch 6 05절") + """은 모델 객체 안의 다시 보내기와 메서드 <code>with_retry</code>를 함께 두면 시도 수가 곱해진다고 셈했습니다. 그러나 모델 객체 안에서 다시 보낸 요청은 세지 못했고, 요청 제한(429)은 실행하지 않았습니다. """ + link(L_CH22_04, "Ch 22 04절") + """도 <code>ModelRetryMiddleware</code>와 모델 객체의 설정을 함께 쓰면 시도 횟수가 곱해질 수 있다고만 적었습니다. 이 절은 연습용 서버가 받은 요청 수로 그 곱을 처음 셉니다.</p>""" + prev + """<p>""" + link(L_CH16_04, "Ch 16 04절") + """의 호출 한도는 우리 코드가 정한 상한이고, 요청 제한은 제공자가 정한 상한입니다. """ + link(L_CH30_01, "Ch 30") + """에서는 FastAPI 처리 함수를 비동기로 써서, 요청을 받는 서버 쪽을 만들었습니다. 이 절은 모델에 요청을 보내는 쪽에서 요청 수를 세고, 비동기 문법은 쓰지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + METAPHOR + """
""" + illustration_block() + """<h3>요청 제한과 연습용 서버</h3><p>요청 제한(rate limit)은 제공자가 정한 분당 요청 수와 토큰 수의 상한입니다. 식당이 한 시간에 받는 손님 수를 정해 두는 것과 같습니다. 공식 안내는 이 상한이 조직과 프로젝트마다 정해지고, 모델마다 다르다고 적습니다. 교재 실습의 요청 몇 번으로는 이 상한에 닿지 않아, 실제 429를 매번 같게 받기 어렵습니다.</p><p>그래서 이 절은 연습용 서버를 띄웁니다. 연습용 서버는 어떤 요청에도 상태 코드 429만 보내는, 이 컴퓨터 안의 작은 서버입니다. 소방 훈련의 연습용 경보처럼, 진짜 불은 없어도 대응은 실제로 해 봅니다. """ + link(L_CH16_05, "Ch 16 05절") + """의 실패 흉내처럼 제공자의 요청 제한을 흉내 내고, 모델의 답은 보내지 않습니다.</p><p>이 절 코드에서는 실습 폴더 <code>notebooks/</code>의 파일 <code>always_429_server.py</code>가 연습용 서버입니다. 파일 안의 함수 <code>app</code> 하나가 요청을 받고, 표준 라이브러리 wsgiref가 요청마다 이 함수를 부릅니다. 서버는 모델에 보내는 요청만 세어, 센 수를 응답 머리 <code>practice-count</code>에 적습니다. 머리는 HTTP 응답에서 본문 앞에 붙는 이름과 값 줄입니다.</p>
<h3>다시 보내기가 놓이는 두 곳</h3><p>다시 보내기(재시도)는 요청이 실패했을 때 같은 요청을 다시 보내는 일입니다. 통화 중인 전화를 조금 있다가 다시 거는 것과 같습니다. 이 절 코드에서는 두 곳이 다시 보냅니다. 하나는 모델 객체 안의 openai 클라이언트이고, 다른 하나는 우리가 붙이는 메서드 <code>with_retry</code>입니다.</p><p>두 곳을 한 줄에 겹치면 요청 수가 곱해지고, 이 절에서는 이것을 겹친 다시 보내기라고 부릅니다. 반송된 편지를 집배원이 다시 나르고, 보낸 사람도 다시 부치는 것과 같습니다. 노트북 4절의 <code>before_runnable</code>이 겹친 다시 보내기입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>기다리는 시간을 두 배씩 늘리기</h3><p>다시 보내기 전에는 조금 기다리고, 실패할 때마다 기다리는 시간을 두 배씩 늘립니다. 이 방법을 기다리는 시간을 두 배씩 늘리기(지수 백오프)라고 부릅니다. 통화 중인 전화를 1분, 2분, 4분 뒤에 다시 거는 것과 같습니다. 여러 곳이 같은 순간에 다시 보내지 않게, 기다리는 시간에 작은 무작위 값을 섞습니다.</p><p>설치판 openai 3.13.0 클라이언트는 0.5초에서 시작해 두 배씩 늘리고, 0.75~1 사이의 무작위 값을 곱합니다. 서버가 머리 <code>Retry-After</code>로 120초 이하를 적어 보내면 그만큼 기다리고, 120초를 넘으면 다시 보내지 않습니다. 메서드 <code>with_retry</code>는 1초에서 시작해 두 배씩 늘리고, 0~1초의 무작위 값을 더합니다. 이 규칙은 설치판 소스로 확인했습니다. 연습용 서버는 <code>Retry-After</code>를 보내지 않아 그 갈래는 노트북에서 실행하지 않았고, 기다린 시간도 재지 않았습니다.</p>
<h3>한꺼번에 보내는 수와 대기열</h3><p>한꺼번에 보내는 수는 동시에 처리 중인 요청의 수입니다. 계산대 두 곳에 손님이 줄을 서면, 계산 중인 손님은 둘뿐인 것과 같습니다. 차례를 기다리는 줄은 대기열이라고 부릅니다. 이 절 코드에서는 메서드 <code>batch</code>의 설정 <code>max_concurrency</code>가 한꺼번에 보내는 수의 상한입니다.</p><p>메서드 <code>batch</code>는 """ + link(L_02, "02절") + """ 4블록 마지막 단락에서 본 메서드로, 요청 여러 개를 곧바로 함께 보냅니다. 파일로 맡기는 일괄 처리(Batch API)와 다르고, 할인도 붙지 않습니다. 설치판 소스로 보면, 설정이 없을 때는 Python이 정한 수만큼 함께 처리하고 설정을 두면 그 수를 넘지 않습니다. 나머지 요청은 대기열에서 차례를 기다립니다.</p>
<h3>이 절에서 쓰는 말</h3>""" + terms + """
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 연습용 서버 파일을 자식 프로세스로 띄우고, 센 수를 0으로 맞추는 요청으로 429를 받아 봅니다. 3절은 과정 표준 설정의 모델 객체를 연습용 서버 주소와 가짜 키로 만듭니다. 인자 <code>max_retries</code>를 적지 않은 모델 객체와 0을 적은 모델 객체를 한 번씩 부르고, 서버가 받은 요청 수를 셉니다. 셀마다 센 수를 0으로 맞추고 시작해, 앞 셀의 요청이 뒤 셀의 수에 섞이지 않습니다.</p><p>노트북은 OpenAI 서비스에 요청을 보내지 않고, API 키도 읽지 않습니다. 파일을 쓰지 않고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2><p>아래 Before 셀은 3절의 <code>default_model</code>에 <code>with_retry</code>를 붙여 한 번 부릅니다. After 셀은 3절의 <code>zero_model</code>에 같은 <code>with_retry</code>를 붙여 한 번 부릅니다. 두 쪽은 같은 연습용 서버와 같은 문의 글, 같은 시도 횟수 3을 쓰고, 안쪽 모델 객체만 다릅니다.</p>
{{notebook:""" + SLUG + """|failure}}
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>Before 쪽은 호출 객체를 한 번 불렀는데, 서버에 요청이 아홉 번 갔습니다. 메서드 <code>with_retry</code>가 세 번 부를 때마다, 모델 객체가 요청을 셋씩 보냈기 때문입니다. 마지막에 받은 오류는 하나뿐이라, 오류만 보면 요청이 몇 번 갔는지 알 수 없습니다. 요청 제한에 걸린 때 요청을 세 배로 보내면, 공식 안내대로 그 요청도 분당 한도에 들어갑니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + compare + """
<p>After 쪽은 안쪽 모델 객체를 <code>max_retries=0</code>으로 바꿔, 다시 보내기를 <code>with_retry</code> 한 곳에만 두었습니다. 같은 시도 횟수 3으로 서버가 받은 요청이 3이 되었습니다. 두 쪽 모두 요청 수는 모델 객체 한 번의 요청 수에 시도 횟수를 곱한 값과 같았습니다.</p><p>값 바꿔 보기는 After의 호출 객체로 문의 다섯을 한꺼번에 보내, 설정 <code>max_concurrency</code> 하나만 바꿨습니다. 설정이 없으면 다섯이 모두 한꺼번에 처리되었고, 2로 두면 둘을 넘지 않았습니다. 서버가 받은 요청 수는 두 번 모두 15로, 한꺼번에 보내는 수는 요청 수를 줄이지 않았습니다.</p>
""" + mermaid_block(FIG5, FIG5_ALT, FIG5_CAP, FIG5_READ) + vary + """
<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절의 429는 연습용 서버가 보낸 흉내이고, 제공자가 보낸 429가 아닙니다. 제공자의 실제 요청 제한은 이번에 받지 않았습니다. 공식 안내는 제한이 조직과 프로젝트마다 정해지고, 모델마다 다르다고 적습니다.</li><li>LangChain 모델 안내는 모델이 기본으로 여섯 번까지 다시 보낸다고 적습니다. 그러나 이 절의 설치판에서는 인자 <code>max_retries</code>를 적지 않으면 openai 클라이언트의 값 2가 쓰였습니다. 서버가 받은 요청은 3이었습니다. 교재는 설치판에서 실행한 출력을 따릅니다. 판이 바뀌면 기본값이 달라질 수 있어, 모델 객체와 클라이언트의 값을 출력해 확인합니다.</li><li>한 곳에만 두는 방법은 둘입니다. After처럼 모델 객체 쪽을 0으로 두고 <code>with_retry</code>를 쓰면, 다시 보낼 오류의 종류를 우리 코드가 고릅니다. 반대로 <code>with_retry</code>를 빼고 모델 객체의 다시 보내기만 두어도, 3절처럼 요청은 3입니다.</li><li>설치판 소스로 보면, 모델 객체 쪽을 0으로 두면 서버가 적어 준 <code>Retry-After</code>를 따르는 일도 함께 빠집니다. 그때는 <code>with_retry</code>의 기다리는 시간 규칙만 남습니다. 이 차이는 노트북에서 실행하지 않았습니다.</li><li>시도 횟수 3과 문의 다섯, 설정 값 2는 흐름을 보여 주려고 정한 예입니다. 알맞은 한꺼번에 보내는 수는 계정의 요청 제한과 모델, 요청 크기에 따라 다릅니다.</li><li>설정 <code>max_concurrency</code>가 없으면, 메서드 <code>batch</code>는 CPU 수에 4를 더한 수(32까지)만큼 함께 처리합니다. 문의가 많으면 그만큼 요청이 한꺼번에 몰리니, 요청 제한에 맞춰 설정을 둡니다.</li><li>걸린 시간은 재지 않았습니다. 기다리는 시간에 무작위 값이 섞여, 같은 셀도 실행할 때마다 걸린 시간이 달라질 수 있습니다.</li><li>노트북은 포트 58034에 서버를 띄웁니다. 다른 프로그램이 그 포트를 쓰면 2절 셀이 멈추니, 셀의 포트 번호를 바꿔 다시 실행합니다. 서버를 끄지 못했으면 커널을 다시 시작합니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 버전과 Windows·macOS에서는 실행하지 않았고, 종료 코드는 운영체제에 따라 다를 수 있습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>인자 <code>max_retries</code>를 적지 않은 모델 객체는 한 번 부를 때 서버에 요청 3번을 보냈습니다.</li><li>모델 객체 안의 다시 보내기에 <code>with_retry</code>를 겹치자 요청이 9번으로 곱해졌고, 한 곳에만 두자 3번이었습니다.</li><li>설정 <code>max_concurrency</code>는 요청 수를 그대로 두고, 한꺼번에 처리되는 수만 정한 값 아래로 막았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — """ + link(L_05, "05절") + """에서는 요청을 보내기 전에 비용 상한으로 막는 예산 가드와 95 백분위수를 다룹니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 인자 <code>max_retries</code>를 적지 않은 모델 객체를 한 번 부르자, 연습용 서버는 요청을 몇 번 받았고 그 까닭은 무엇인가요?</p><p class="quiz-a">세 번 받았습니다. 첫 요청이 429를 받자, openai 클라이언트가 기본값 2대로 같은 요청을 두 번 더 보냈습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 그 모델 객체에 <code>stop_after_attempt=3</code>인 <code>with_retry</code>를 붙이면, 한 번 부를 때 요청은 몇 번 가나요?</p><p class="quiz-a">아홉 번입니다. 메서드 <code>with_retry</code>가 모델 객체를 세 번 부르고, 모델 객체는 부를 때마다 요청을 셋씩 보내 3 × 3 = 9입니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">3. 요청을 아홉 번 보내도 받은 오류가 하나뿐이었습니다. 요청 수를 어떻게 알 수 있었나요?</p><p class="quiz-a">연습용 서버가 받은 요청을 세어 응답 머리에 적었고, 노트북이 그 수를 물어 출력했습니다. 오류만 보면 몇 번 보냈는지 알 수 없습니다. 틀렸다면 노트북 2·3절을 다시 읽습니다.</p><p class="quiz-q">4. 설정 <code>max_concurrency</code>를 2로 두면 서버가 받는 요청 수가 줄어드나요?</p><p class="quiz-a">줄지 않습니다. 노트북에서 요청 수는 설정이 없을 때와 같은 15였고, 한꺼번에 처리 중이던 수만 5에서 2로 줄었습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">5. 동료가 「429가 오면 계속 다시 보내면 언젠가 통한다」고 말합니다. 이 절과 공식 안내로 보면 어떤가요?</p><p class="quiz-a">공식 안내는 실패한 요청도 분당 한도에 들어가, 계속 다시 보내도 풀리지 않는다고 적습니다. 다시 보내는 횟수를 정하고, 한 곳에만 두고, 기다리는 시간을 두 배씩 늘려야 합니다. 틀렸다면 본문 4블록과 7블록을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://developers.openai.com/api/docs/guides/rate-limits">OpenAI Rate limits</a></div>확인 2026-09-30 · 요청 제한이 조직과 프로젝트마다 정해지고 모델마다 다르다고 적습니다. 실패한 요청도 분당 한도에 들어간다는 문장과, 머리 <code>Retry-After</code>가 이 안내에 있습니다. 공식 SDK가 429와 503을 스스로 다시 보내고, 기다리는 시간을 늘리며 무작위 값을 섞으라고 권합니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langchain/models">LangChain Models</a></div>확인 2026-09-30 · 모델이 기본으로 여섯 번까지 다시 보낸다고 적습니다. 이 절의 설치판 출력은 클라이언트 값 2와 요청 3이었습니다. 메서드 <code>batch</code>와 설정 <code>max_concurrency</code>로 함께 부르는 수를 정하는 방법도 이 안내에 있습니다.</li><li><div>설치판 소스 openai 3.13.0</div>확인 2026-09-30 · 파일 <code>_constants.py</code> 8행이 <code>DEFAULT_MAX_RETRIES = 2</code>, 11~13행이 기다리는 시간의 처음 값·상한·서버 대기 상한입니다. 파일 <code>_base_client.py</code> 763행은 머리 <code>retry-after-ms</code>를 먼저 봅니다. 801행은 서버가 준 대기를 따르고, 808·811행은 두 배씩 늘리며 무작위 값을 곱합니다. 815행 이하가 다시 보낼지 정하고, 847행이 429에 다시 보냅니다.</li><li><div>설치판 소스 langchain-openai 1.6.0</div>확인 2026-09-30 · 파일 <code>chat_models/base.py</code> 838행은 <code>max_retries</code>의 기본값 None입니다. 1371~1372행은 값이 있을 때만 클라이언트에 넘깁니다. 같은 파일 594행이 오류 <code>OpenAIRateLimitError</code>입니다.</li><li><div>설치판 소스 langchain-core 1.6.2 · tenacity 9.1.4</div>확인 2026-09-30 · langchain-core 파일 <code>runnables/base.py</code> 2101~2107행이 <code>with_retry</code>의 기본값입니다. 같은 파일 978행이 <code>batch</code>의 일꾼 모음입니다. 파일 <code>runnables/config.py</code> 672~673행이 설정 <code>max_concurrency</code>를 일꾼 수로 넘깁니다. tenacity 파일 <code>wait.py</code> 256~259행이 처음 1초·두 배·무작위 1초입니다.</li><li><div>Python 3.12.13 표준 라이브러리</div>확인 2026-09-30 · 파일 <code>concurrent/futures/thread.py</code> 146행이 일꾼 수의 기본값으로, CPU 수에 4를 더한 수(32까지)입니다. 154행이 기다리는 일을 담는 대기열입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


def leftover_placeholders() -> list:
    names = []
    for name, value in globals().items():
        if isinstance(value, str) and value.startswith("[[") and name.isupper():
            names.append(name)
    return names


if __name__ == "__main__":
    check_tools04()
    check_server()
    check_inputs()
    left = leftover_placeholders()
    if left:
        print("자리 표시(그림을 본 뒤 채움):", left)
    if "--guard-check" in sys.argv:
        guard_check()
        raise SystemExit(0)
    if "--nb-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--nb-copy") + 1])
        target.mkdir(parents=True, exist_ok=True)
        path = write_notebook(target, "04", SLUG, "paired", cells())
        print("wrote copy", path)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        write_tools()
        write_server()
        path = write_notebook(LAB, "04", SLUG, "paired", cells())
        print("wrote", path)
