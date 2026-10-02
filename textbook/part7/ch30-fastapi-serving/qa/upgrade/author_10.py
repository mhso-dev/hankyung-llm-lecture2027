"""Ch 30 10절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§5-3·§6 experiment).

사용:
  python3 -B author_10.py              → 노트북 + _src 본문 + 도구 파일(10 판)을 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_10.py --src-only   → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_10.py --tools-copy DIR → DIR에 지금 도구 파일을 복사한다(사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음.
설계와 노트북 밖 확인 5번은 qa/upgrade/10-design.md.

## 결정 1 — 붙인 앞 절 기능 셋 (handoff 「§09 → 실습 절」 2번 흐름 후보)

도서관 웹 화면(허용 출처 http://localhost:5173 — 앱 21행) 하나가 질문 「반납 기한을 알려 주세요」(스레드 web-1)를
요청 주소 /v1/chat/stream에 보내는 한 요청 흐름:
07 사전 요청과 허용 출처 응답 머리(header_or_none) → 05 SSE 응답 + 07 접근 토큰(첫 요청) → 앞 사건 둘에서 끊김(06 2절과 같은 자리)
→ 07 사전 요청(요청 머리 이름에 Last-Event-ID를 더함) → 06 이어 받기(last_event_id·요청 머리 Last-Event-ID) → 06 판정(ended_with_done)·04 join_tokens.
세 기능(05·06·07)이 실행 1 흐름에서 모두 쓰인다. 기록 장치 record_step·print_log(단계마다 [이름, 상태 코드, 허용 출처]).
뺀 것과 까닭은 b3 한 단락·10-design.md §3: 01 422 · 02·06 시간 제한 재정의 · 03 ainvoke·/v1/chat · 04 astream 직접 ·
07 HTTPBearer 새 앱 · 08 응답 문서 · 09 실제 모델.

## 결정 2 — 실행 2는 접근 토큰 하나만 (Bearer local-demo-token → Bearer wrong-token, 07절 노트북 2절 값)

07이 틀린 접근 토큰에 401을 이미 보였으므로 b2 「새로 볼 것」은 실행이 보인 만큼만(Ch 26 05 검토 B-7):
사전 요청은 두 실행 모두 200 · 401 응답에도 허용 출처 응답 머리 · 흐름이 첫 요청에서 멈춰 이어 받기를 보내지 않고 판정 False.

## 결정 3 — 모델 요청 0 (챕터 결정 M0 · 09 인계 7번 권고 · Ch 23 07·Ch 24 04 선례)

결론은 상태 코드·허용 출처·사건 이름·사건 번호·판정 값(매번 같은 값 — 노트북 밖 5/5). 키 셀 없음.
앱 기록기 logger.exception을 지나는 길이 없어(401은 제공 함수가 올림) 06절의 기록기 수준 셀은 두지 않는다(노트북 밖 표준 오류 0).

## 결정 4 — 도구 파일 serve_tools.py 10 판 (규격 §2-7 · 챕터 공통 9)

09 판(author_09.TOOLS09) 끝에 06절 노트북 함수 last_event_id(author_06.DEF_LAST)와 07절 노트북 함수 header_or_none(author_07.DEF_HEADER)을
셀 글 그대로 덧붙인다(주석 첫 줄 「# Ch 30 NN절에서 배웠습니다 — NN절 노트북의 같은 이름 함수를 옮겼습니다」). 가져오기 줄은 더하지 않는다.
대조(check_tools10): 09 사슬 통과 · 10 판이 09 판으로 시작 · 셀 글이 06·07 노트북 코드 셀과 문자열로 같음 · AST 같음 · 함수 차례.
쓰기 가드: 09 판이거나 10 판일 때만 쓰고, 10 판으로 시작하는 더 긴 판은 건너뜀.
04·06·09 생성기의 쓰기 가드와 07·08 __main__ 확인이 10 판을 건너뛰거나 통과하는지는 check_older_guards()가 같은 조건으로 확인한다.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·`sorted`·노트북 딕셔너리 `.get`·`.items`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·
대입 풀기(for 포함)·별표 풀기·`while`·`try`·`raise`·세미콜론·`isinstance`·클래스·데코레이터·셀 맨 위 await·`async`·`asyncio`·
재정의·가짜 에이전트·가짜 모델·자식 프로세스·포트·`node`·파일 쓰기. 호출 깊이 2 이하. 01~09 노트북에 없던 내장 이름·속성·키워드 인자 0.
"""
from __future__ import annotations

import ast
import hashlib
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402
import author_04  # noqa: E402
import author_06  # noqa: E402
import author_07  # noqa: E402
import author_09  # noqa: E402

LAB = ROOT / "labs/part7/ch30-fastapi-serving/notebooks"
FIGS = ROOT / "textbook/part7/ch30-fastapi-serving/figures"
SLUG = "10-FastAPI-서빙-실습"
TITLE_TEXT = "FastAPI 서빙 실습: 끊긴 SSE 응답을 이어 받는 흐름에서 접근 토큰 하나만 바꾸기"
SRC = ROOT / "textbook/part7/ch30-fastapi-serving/_src" / (SLUG + ".html")
AUTHOR01 = ROOT / "textbook/part7/ch30-fastapi-serving/qa/upgrade/author_01.py"
TOOLS_PATH = LAB / "serve_tools.py"
RUNS_SENTENCE = "새 커널로 두 번 실행해 견주자, 코드 셀 21개의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 노트북 밖에서 같은 흐름을 다섯 번 실행했을 때도 값이 모두 같았습니다."

# ---------------------------------------------------------------- 도구 파일 serve_tools.py (10 판)
NOTE06 = author_09.NOTE06
NOTE07 = "Ch 30 07절에서 배웠습니다 — 07절 노트북의 같은 이름 함수를 옮겼습니다"
MOVED10 = [
    (author_06, "DEF_LAST", "last_event_id", NOTE06),
    (author_07, "DEF_HEADER", "header_or_none", NOTE07),
]
TOOL_ORDER10 = author_09.TOOL_ORDER09 + ["last_event_id", "header_or_none"]


def tools10_text() -> str:
    text = author_09.TOOLS09
    for module, const, name, note in MOVED10:
        text = text + "\n\n# " + note + "\n" + getattr(module, const) + "\n"
    return text


TOOLS10 = tools10_text()


def check_tools10() -> None:
    """10 판이 09 판으로 시작하고, 덧붙인 함수 둘이 06·07절 노트북 셀과 글자·AST 모두 같은지 봅니다."""
    author_09.check_tools09()
    assert TOOLS10.startswith(author_09.TOOLS09) and TOOLS10 != author_09.TOOLS09, "10 판이 09 판으로 시작하지 않습니다"
    plain = author_04.strip_later_imports(TOOLS10)
    assert plain.startswith(author_06.TOOLS06) and plain.startswith(author_04.TOOLS)
    tree = ast.parse(TOOLS10)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(node.name)
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        if isinstance(node, ast.ImportFrom):
            raise AssertionError("10 판 도구 파일은 from 가져오기를 쓰지 않습니다")
    assert names == TOOL_ORDER10, names
    assert imports == ["json"], imports
    for module, const, name, note in MOVED10:
        source = getattr(module, const)
        assert source in author_06.notebook_code_cells(module.SLUG), name + " 셀 글이 그 절 노트북과 다릅니다"
        assert ("# " + note + "\n" + source + "\n") in TOOLS10
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
        assert mine == theirs and len(mine) == 1, name
    assert TOOLS10.count("# Ch 30 ") == 10


def check_older_guards() -> None:
    """04·06·09 생성기의 쓰기 가드와 07·08 생성기 __main__ 확인을, 같은 조건으로 10 판에 대 봅니다(그 생성기는 실행하지 않음)."""
    plain = author_04.strip_later_imports(TOOLS10)
    # 04: strip 뒤 04 판으로 시작하고 04 판과 다르면 건너뜀
    assert plain.startswith(author_04.TOOLS) and TOOLS10 != author_04.TOOLS
    # 06: 04·06 판과 다르고 strip 뒤 06 판으로 시작하면 건너뜀
    assert TOOLS10 not in (author_04.TOOLS, author_06.TOOLS06) and plain.startswith(author_06.TOOLS06)
    # 09: 06·09 판과 다르고 09 판으로 시작하면 건너뜀
    assert TOOLS10 not in (author_06.TOOLS06, author_09.TOOLS09) and TOOLS10.startswith(author_09.TOOLS09)
    # 07·08 __main__: strip 뒤 06 판으로 시작하면 통과
    assert plain.startswith(author_06.TOOLS06)


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["fastapi==0.135.0", "httpx==0.28.1", "pydantic==2.12.5", "starlette==1.6.0",
                          "langgraph==1.2.11", "langchain==1.4.0"])

IMPORTS = r'''# 이 절에서 쓸 이름을 가져옵니다(os는 Python에 들어 있는 모듈입니다)
import os
from fastapi.testclient import TestClient
# 04·06·07절에서 배운 함수 일곱은 도구 파일에서 가져옵니다
from serve_tools import ended_with_done, event_names, header_or_none, join_tokens, last_event_id, read_events, token_values

print("가져온 이름:", "TestClient")
print("도구 파일에서 가져온 함수:", "ended_with_done, event_names, header_or_none, join_tokens, last_event_id, read_events, token_values")'''

# 01절 2절 셀 글 그대로(아래 __main__에서 author_01.py와 문자열 대조)
FIND_LAB = author_06.FIND_LAB

IMPORT_APP = r'''# 작업 폴더를 실습 폴더로 옮기고, 앱 파일에서 앱 객체를 가져옵니다
os.chdir(lab_path)
from agent_service.app import app
print("가져온 앱 객체의 종류:", type(app).__name__)
print("재정의 딕셔너리의 키 수:", len(app.dependency_overrides))'''

SOURCE_HEAD = r'''# 앱 파일을 글로 읽어, SSE 처리 함수 chat_stream의 머리 99~105행을 출력합니다
first_line = 99
last_line = 105
with open("agent_service/app.py", encoding="utf-8") as app_file:
    app_lines = app_file.read().splitlines()
print("줄 번호 | 줄")
for index in range(first_line - 1, last_line):
    print(index + 1, "|", app_lines[index])'''

MATERIALS = r'''# 두 실행이 함께 쓸 재료를 만듭니다 — 모두 실행 전에 정한 값입니다
client = TestClient(app)
page_origin = "http://localhost:5173"
question_body = {"question": "반납 기한을 알려 주세요", "thread_id": "web-1"}
good_token = "Bearer local-demo-token"
print("화면의 출처(앱 21행의 허용 출처):", page_origin)
print("질문 본문(스레드 이름 web-1은 이 절에서 정함):", question_body)
print("실행 1의 접근 토큰(앱 57행의 교재용 값):", good_token)'''

DEF_PREFLIGHT = r'''# 허용 출처 화면이 보낼 사전 요청을 요청 주소 /v1/chat/stream에 보내고, 응답을 내놓습니다
def send_preflight(header_names):
    # 요청 머리 이름은 실제 요청에 실을 머리를 쉼표로 이어 적은 글입니다(07절과 같은 모양)
    preflight_headers = {"Origin": page_origin, "Access-Control-Request-Method": "POST",
                         "Access-Control-Request-Headers": header_names}
    return client.options("/v1/chat/stream", headers=preflight_headers)'''

DEF_SEND = r'''# 출처와 접근 토큰을 요청 머리에 실어 질문을 보내고, 응답을 내놓습니다
def send_question(token, resume_id):
    request_headers = {"Origin": page_origin, "Authorization": token}
    # 이어 받을 사건 번호가 있으면 06절처럼 요청 머리 Last-Event-ID도 싣습니다
    if resume_id is not None:
        request_headers = {"Origin": page_origin, "Authorization": token, "Last-Event-ID": resume_id}
    return client.post("/v1/chat/stream", json=question_body, headers=request_headers)'''

DEF_EVENTS = r'''# 응답의 상태 코드가 200이면 본문을 칸 딕셔너리 목록으로 읽고, 아니면 빈 목록을 내놓습니다
def events_of(response):
    # 401 같은 오류 응답의 본문은 SSE 사건이 아니라 JSON 글이라 읽지 않습니다
    if response.status_code == 200:
        return read_events(response.text)
    return []'''

BASELINE = r'''# 부품을 한 번 시험합니다 — 끊기지 않은 요청을 보내, 뒤에서 견줄 기준 응답을 만듭니다
full_response = send_question(good_token, None)
full_events = events_of(full_response)
full_text = join_tokens(token_values(full_events))
print("상태 코드:", full_response.status_code)
print("허용 출처:", header_or_none(full_response, "access-control-allow-origin"))
print("사건 이름:", event_names(full_events))
print("이어 붙인 글:", full_text)'''

DEF_RECORD = r'''# 단계 이름과 응답을 받아, 상태 코드와 허용 출처 응답 머리를 기록 목록에 한 줄로 더합니다
def record_step(log_rows, step_name, response):
    allowed = header_or_none(response, "access-control-allow-origin")
    log_rows.append([step_name, response.status_code, allowed])'''

DEF_PRINT_LOG = r'''# 기록 목록을 「단계 | 상태 코드 | 허용 출처」 표 모양으로 한 줄씩 출력합니다
def print_log(log_rows):
    print("단계 | 상태 코드 | 허용 출처")
    for row in log_rows:
        print(row[0], "|", row[1], "|", row[2])'''

DEF_START = r'''# 흐름의 앞 절반 — 사전 요청(07절)을 보낸 뒤, 접근 토큰을 실은 첫 요청(05절)을 보내고 그 응답을 내놓습니다
def start_flow(token, log_rows):
    preflight = send_preflight("Authorization, Content-Type")
    record_step(log_rows, "사전 요청", preflight)
    first_response = send_question(token, None)
    record_step(log_rows, "첫 요청", first_response)
    return first_response'''

DEF_RESUME = r'''# 흐름의 뒤 절반 — 받은 마지막 사건 번호가 있으면 사전 요청을 한 번 더 보내고 이어 받습니다(06절)
def resume_flow(token, received, log_rows):
    resume_id = last_event_id(received)
    # 받은 사건 번호가 없으면 이어 받을 자리가 없어, 받은 목록을 그대로 내놓습니다
    if resume_id is None:
        return received
    preflight = send_preflight("Authorization, Content-Type, Last-Event-ID")
    record_step(log_rows, "사전 요청(이어 받기)", preflight)
    resumed_response = send_question(token, resume_id)
    record_step(log_rows, "이어 받기", resumed_response)
    return received + events_of(resumed_response)'''

RUN1 = r'''# 실행 1 — 교재용 접근 토큰으로 흐름을 끝까지 실행하고, 단계 기록을 표로 출력합니다
run1_log = []
run1_first = start_flow(good_token, run1_log)
# 첫 요청에서 앞 사건 둘까지 받고 연결이 끊겼다고 봅니다(06절 2절과 같은 자리)
run1_received = events_of(run1_first)[0:2]
run1_events = resume_flow(good_token, run1_received, run1_log)
print_log(run1_log)'''

RUN1_IDS = r'''# 실행 1에서 끊기기 전에 받은 사건과, 이어 받은 뒤 이은 사건을 봅니다
print("끊기기 전에 받은 사건 이름:", event_names(run1_received))
print("끊기기 전에 받은 마지막 사건 번호:", last_event_id(run1_received))
# 이은 목록의 자리 2(셋째 사건)가 이어 받은 첫 사건입니다
print("이어 받은 첫 사건 번호:", run1_events[2]["id"])
print("이은 사건 이름:", event_names(run1_events))'''

RUN1_JUDGE = r'''# 실행 1을 판정합니다 — 마지막 사건이 done인가(06절)와, 이어 붙인 글이 기준 응답의 글과 같은가
run1_text = join_tokens(token_values(run1_events))
print("마지막 사건이 done인가:", ended_with_done(run1_events))
print("이어 붙인 글:", run1_text)
print("기준 응답의 글과 같은가:", run1_text == full_text)'''

RUN2 = r'''# 실행 2 — 값 하나만 바꿉니다: 접근 토큰을 07절에서 쓴 틀린 값으로 두고 같은 흐름을 실행합니다
wrong_token = "Bearer wrong-token"
run2_log = []
run2_first = start_flow(wrong_token, run2_log)
run2_received = events_of(run2_first)[0:2]
run2_events = resume_flow(wrong_token, run2_received, run2_log)
print("실행 2의 접근 토큰(07절 2절의 틀린 값):", wrong_token)
print_log(run2_log)'''

RUN2_BODY = r'''# 실행 2의 첫 요청 응답 본문과, 끊기기 전에 받은 사건을 봅니다
print("첫 요청의 응답 본문:", run2_first.json())
print("끊기기 전에 받은 사건 수:", len(run2_received))
print("끊기기 전에 받은 마지막 사건 번호:", last_event_id(run2_received))'''

RUN2_JUDGE = r'''# 실행 2를 실행 1과 같은 방법으로 판정합니다
run2_text = join_tokens(token_values(run2_events))
print("이은 사건 수:", len(run2_events))
print("마지막 사건이 done인가:", ended_with_done(run2_events))
print("이어 붙인 글의 글자 수:", len(run2_text))
print("기준 응답의 글과 같은가:", run2_text == full_text)'''

COMPARE = r'''# 두 실행의 단계 기록과 판정을 한 표로 모읍니다
print("견준 것 | 실행 1 | 실행 2")
print("사전 요청의 상태 코드 |", run1_log[0][1], "|", run2_log[0][1])
print("첫 요청의 상태 코드 |", run1_first.status_code, "|", run2_first.status_code)
print("첫 요청의 허용 출처 |", run1_log[1][2], "|", run2_log[1][2])
print("기록한 단계 수 |", len(run1_log), "|", len(run2_log))
print("마지막 사건이 done인가 |", ended_with_done(run1_events), "|", ended_with_done(run2_events))
print("기준 응답의 글과 같은가 |", run1_text == full_text, "|", run2_text == full_text)'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/10-figures.md — 렌더 전에 적음)
FIG1 = "10-1-세-절-기능을-이은-요청-흐름"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 재료에는 출처 http://localhost:5173, 질문 반납 기한, 스레드 web-1, 실행마다 접근 토큰 하나가 적혀 있습니다. 그 아래 파란 상자 넷이 실선으로 차례로 이어집니다. start_flow 사전 요청 07절 첫 요청 05절 단계마다 기록 한 줄, 앞 사건 둘만 받고 끊김 06절 노트북 2절과 같은 자리, resume_flow 번호가 있을 때만 사전 요청 07절 이어 받기 06절 단계마다 기록 한 줄, 판정 ended_with_done 06절 join_tokens 04절입니다. start_flow와 resume_flow에서 오른쪽 회색 상자 CORS 층 앱 19~26행 사전 요청에 바로 답함으로 점선이 가고, 회색 상자에서 초록 상자 실습 앱 chat_stream 제공 함수 require_token get_resume_index로 점선이 가는 그림"
FIG1_CAP = "05절 SSE 응답, 06절 이어 받기, 07절 사전 요청과 접근 토큰을 함수 둘로 이어, 한 질문의 요청 흐름을 만들었습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 우리가 보낸 재료와 실습 앱 파일의 처리 함수입니다.
파란 상자는 이 절 노트북에서 만든 함수와 흐름의 자리이고, 상자 안의 절 번호는 그 기능을 배운 절입니다.
실선은 흐름의 차례이고, 점선은 실습 앱으로 보내는 요청입니다.
회색 상자인 CORS 층은 사전 요청에 바로 답하고, 그 밖의 요청만 실습 앱으로 넘깁니다."""

FIG2 = "10-2-실행-1의-단계-차례"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 노란 상자 사전 요청 200 허용 출처 http://localhost:5173에서 노란 상자 첫 요청 200으로 이어지고, 파란 상자 앞 사건 둘만 받음 마지막 사건 번호 web-1:1을 지납니다. 이어서 노란 상자 사전 요청 이어 받기 200, 노란 상자 이어 받기 Last-Event-ID web-1:1 200 첫 번호 web-1:2를 지나, 맨 아래 노란 상자 이은 사건 일곱 done True 기준 응답의 글과 같음 True에 닿는 그림"
FIG2_CAP = "실행 1은 사전 요청부터 이어 받기까지 네 단계 모두 200이었고, 이은 사건 일곱의 글이 기준 응답과 같았습니다."
FIG2_READ = """위에서 아래로 읽습니다.
노란 상자는 노트북 6절의 출력이고, 파란 상자는 우리 흐름이 앞 사건 둘만 받은 것으로 본 자리입니다.
첫 요청과 이어 받기는 처리 함수 `chat_stream`이 답했고, 두 사전 요청은 CORS 층이 앱으로 넘기지 않고 답했습니다.
두 번째 사전 요청은 브라우저가 담아 둔 답이 없는 경우를 흉내 내어 보낸 것입니다.
맨 아래 노란 상자는 6절의 판정 출력입니다."""

FIG3 = "10-3-접근-토큰만-바꾼-두-실행"
FIG3_ALT = "맨 위 회색 상자에는 두 실행 같음, 출처·질문·끊기는 자리, 사전 요청 200, 첫 요청의 허용 출처 http://localhost:5173이 적혀 있고, 그 아래에 칸 둘이 나란히 있습니다. 왼쪽 칸 실행 1에는 초록 상자 접근 토큰 Bearer local-demo-token에서 노란 상자 첫 요청 200 기록 네 단계 done True 기준 글과 같음 True로 이어집니다. 오른쪽 칸 실행 2 값 하나만 바꿈에는 파란 상자 접근 토큰 Bearer wrong-token에서 노란 상자 첫 요청 401 기록 두 단계 이어 받기 보내지 않음 done False로 이어지는 그림"
FIG3_CAP = "접근 토큰 하나만 틀리게 바꾸자 첫 요청이 401로 끝나, 흐름이 이어 받기로 가지 않았습니다."
FIG3_READ = """맨 위 회색 상자는 두 실행의 출력에서 모두 확인한 값입니다.
왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2입니다.
칸마다 위 상자는 보낸 접근 토큰이고, 실행 2 칸의 것은 바꾼 값이라 파랑입니다.
아래 노란 상자는 노트북 6·7절의 출력입니다.
두 칸끼리는 화살표로 잇지 않았습니다."""

ILLU = "10-4-세-가지-칸을-이은-열차"
ILLU_ALT = "흰 바탕에 오른쪽 아래에서 왼쪽 위로 비스듬히 곧게 뻗은 선로 하나가 있고, 그 위에 화물 열차 하나가 한 줄로 이어져 있습니다. 오른쪽 아래 맨 앞에 검은 기관차 하나가 있고, 그 뒤로 연보라색 닫힌 칸 둘, 흰 둥근 통 칸 둘, 산호색 덮개 칸 둘이 차례로 붙어 있습니다. 칸 사이에 빈틈은 없고, 짐·사람·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "검은 기관차 뒤에 서로 다른 세 종류의 칸이 둘씩 이어져, 열차 하나가 되었습니다."
# 1차 job 97fb9b4b-… 탈락(칸 차례가 섞이고 산호색 칸 둘이 떨어져 그려짐) → 2차 job a5351a85-82f9-4b7f-b64d-41f72c9aab31 채택
# 저장 PNG를 열어 센 개수로 적음(검은 기관차 하나·연보라 닫힌 칸 둘·흰 통 칸 둘·산호색 덮개 칸 둘)
ILLU_READ = "검은 기관차 뒤로 연보라색 닫힌 칸 둘, 흰 둥근 통 칸 둘, 산호색 덮개 칸 둘이 이어져 있습니다. 세 종류의 칸은 따로 배운 05·06·07절의 기능이고, 이어진 열차 하나가 이 절의 요청 흐름입니다. 기관차 바로 뒤 연보라색 칸은 흐름이 먼저 보내는 07절의 사전 요청과 접근 토큰입니다. 흰 통 칸은 05절의 SSE 응답이고, 맨 뒤 산호색 칸은 06절의 이어 받기입니다. 칸의 색과 모양은 절을 가르려고 고른 것이고, 칸이 둘씩인 것은 값과 짝짓지 않습니다."

METAPHOR = """<p>01~09절에서는 화물 열차의 칸을 한 가지씩 따로 살펴보았습니다. 05절은 번호판을 단 칸이 차례로 들어오는 모습이었고, 06절은 끊긴 뒤 번호부터 다시 받는 모습이었습니다. 07절은 허락을 적은 꼬리표와 번호판 차량의 모습이었습니다. 이번에는 따로 본 칸을 한 열차로 이어, 한 번에 달려 봅니다.</p><p>열차 하나가 질문 하나의 요청 흐름입니다. 칸의 종류는 흐름에 붙인 05·06·07절의 기능입니다. 기관차 뒤로 칸이 붙은 차례가 흐름의 차례이고, 칸을 잇는 연결 고리가 함수 <code>start_flow</code>와 <code>resume_flow</code>입니다.</p><p>비유와 다른 점이 있습니다. 실제 흐름에서는 접근 토큰이 틀리면 앞 단계에서 멈추지만, 그림의 열차는 늘 칸이 다 이어져 있습니다.</p>"""

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 05~07절에서 배운 사전 요청·SSE 응답·이어 받기를 한 요청 흐름으로 잇습니다.
2. 교재용 접근 토큰으로 흐름을 끝까지 실행하고, 이어 붙인 글을 끊기지 않은 응답과 견줍니다.
3. 접근 토큰 하나만 틀린 값으로 바꿔 같은 흐름을 실행하고, 두 실행의 단계 기록을 견줍니다.

**준비물** — 이 노트북은 모델을 부르지 않아 API 키가 필요 없습니다.
모델 요청은 0번이고, 비용도 들지 않습니다.
요청은 시험용 클라이언트로 같은 노트북 안에서 보냅니다.
서버 프로그램을 띄우지 않고, 포트를 쓰지 않습니다.
실습 폴더의 파일은 가져오고 읽기만 하며, 쓰는 파일은 없습니다.

첫 셀의 설치에는 몇십 초가 걸릴 수 있습니다.
걸린 시간은 재지 않았습니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 fastapi 0.135.0, httpx 0.28.1, pydantic 2.12.5, starlette 1.6.0입니다.
실습 앱 파일은 패키지 langgraph 1.2.11과 langchain 1.4.0을 가져옵니다.
여섯 모두 실습 폴더 잠금과 같은 판입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.

다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**실습 방법** — 따로 내는 과제는 없고, 강사와 함께 첫 셀부터 순서대로 실행합니다.
실습 폴더 `labs/part7/ch30-fastapi-serving`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md(r"""## 1. 준비

이 절은 이 챕터의 실습입니다.
01~09절에서 쓴 라이브러리 이름과 문법만 쓰고, 흐름을 잇는 함수만 이 절에서 새로 만듭니다.
제목의 서빙은 만든 에이전트를 웹 앱에 올려, 요청에 답하게 하는 일입니다.
첫 셀은 07·08절과 같은 패키지 여섯을 설치하고, 설치된 판 번호를 출력합니다."""),
        setup(INSTALL),
        md(r"""**결과 읽기** — 출력 줄 `fastapi: 0.135.0`부터 `langchain: 1.4.0`까지 여섯 줄이 보입니다.
07·08절과 같은 패키지를 같은 판으로 설치했습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
04·06·07절에서 배운 함수 일곱은 도구 파일 `serve_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md(r"""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수:` 뒤에 함수 일곱이 보입니다.
함수 `join_tokens`는 04절, `header_or_none`은 07절에서 배웠고, 나머지 다섯은 06절에서 배웠습니다.
06절 함수 `last_event_id`와 07절 함수 `header_or_none`은 이 절부터 도구 파일에 있습니다.
두 함수는 그 절 노트북의 셀을 주석과 본문 그대로 옮겼습니다.

앞에서 배운 함수는 `serve_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

다음 셀은 01절 2절과 같은 파일 위치 셀로, 후보 셋 가운데 실습 폴더를 고릅니다."""),
        code(FIND_LAB),
        md(r"""**결과 읽기** — 출력 줄 `실습 폴더를 찾았는가: True`가 보입니다.
고른 후보는 연 자리마다 달라서 출력하지 않습니다.
실습 폴더 맨 위에서 연 커널은 이 안내를 보기 전에, 앞 셀의 도구 파일 가져오기에서 먼저 멈춥니다.

다음 셀은 작업 폴더를 실습 폴더로 옮긴 뒤, 앱 파일에서 앱 객체 `app`을 가져옵니다.
02절에서 본 재정의 딕셔너리의 키 수도 함께 출력합니다."""),
        code(IMPORT_APP),
        md(r"""**결과 읽기** — 출력 줄 `재정의 딕셔너리의 키 수: 0`이 보입니다.
바꿔 낀 제공 함수가 하나도 없어, 실습 앱의 제공 함수가 그대로 불립니다.
이 절은 재정의를 쓰지 않습니다.

## 2. 오늘의 상황과 재료

도서관 웹 화면 하나가 실습 앱에 질문을 보내고, 답을 SSE 사건으로 받습니다.
화면의 출처는 `http://localhost:5173`이고, 앱이 허용 출처로 적은 값입니다.
화면은 SSE 사건 둘을 받은 뒤 연결이 끊겨, 받은 마지막 사건 번호로 이어 받습니다.
다음 셀은 이 흐름이 요청을 보낼 처리 함수 `chat_stream`의 머리 99~105행을 출력합니다."""),
        code(SOURCE_HEAD),
        md(r"""**결과 읽기** — 라벨 줄 아래 99~105행이 처리 함수 `chat_stream`의 머리입니다.
103행의 `_token: AuthDep`은 02·07절에서 본 제공 함수 `require_token`으로 접근 토큰을 검사합니다.
105행의 `start: ResumeIndexDep`은 06절의 제공 함수로, 요청 머리 `Last-Event-ID`에서 이어 받을 자리를 읽습니다.
102행과 104행은 02절에서 본 그래프와 시간 제한의 제공 함수입니다.
라이브러리는 이 제공 함수들을 처리 함수 몸통보다 먼저 부릅니다.

07절에서 본 것처럼, 앱 19~26행의 CORS 층은 이보다도 앞에서 요청을 봅니다.
사전 요청이면 CORS 층이 앱으로 넘기지 않고 바로 답합니다.

다음 셀은 두 실행이 함께 쓸 재료를 만듭니다.
모두 실행 전에 정한 값이고, 출력 라벨에 어디서 온 값인지 적었습니다."""),
        code(MATERIALS),
        md(r"""**결과 읽기** — 출력 줄 `화면의 출처(앱 21행의 허용 출처): http://localhost:5173`이 보입니다.
질문 「반납 기한을 알려 주세요」는 03~07절과 같은 질문입니다.
스레드 이름 `web-1`은 이 절에서 정한 이름이고, 사건 번호의 앞머리가 됩니다.
접근 토큰은 02·07절에서 쓴 교재용 값이고, 실행 2에서만 바꿉니다.

## 3. 흐름의 부품

흐름은 요청 두 가지를 보냅니다.
하나는 07절의 사전 요청이고, 다른 하나는 접근 토큰을 실은 질문 요청입니다.
다음 셀은 사전 요청을 보내는 함수를 정의합니다."""),
        code(DEF_PREFLIGHT),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
인자 `header_names`에는 실제 요청에 실을 요청 머리 이름을 쉼표로 이어 적은 글을 넣습니다.
함수는 2절에서 만든 `client`와 `page_origin`을 그대로 씁니다.

다음 셀은 출처와 접근 토큰을 요청 머리에 실어 질문을 보내는 함수를 정의합니다.
이어 받을 사건 번호가 있으면, 06절처럼 요청 머리 `Last-Event-ID`도 싣습니다."""),
        code(DEF_SEND),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
인자 `resume_id`가 `None`이면 요청 머리가 둘이고, 사건 번호가 있으면 셋입니다.
질문 본문은 늘 2절의 `question_body`입니다.

다음 셀은 응답을 칸 딕셔너리 목록으로 읽는 함수를 정의합니다.
오류 응답의 본문은 SSE 사건이 아니라 JSON 글이라, 상태 코드가 200일 때만 읽습니다."""),
        code(DEF_EVENTS),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `read_events`는 06절에서 배운 함수로, 본문 글을 SSE 사건마다 칸 딕셔너리로 바꿉니다.
상태 코드가 200이 아니면 빈 목록을 내놓습니다.

다음 셀은 부품을 한 번 시험합니다.
끊기지 않은 요청을 보내, 뒤에서 견줄 기준 응답을 만듭니다."""),
        code(BASELINE),
        md(r"""**결과 읽기** — 출력 줄 `허용 출처: http://localhost:5173`이 보입니다.
SSE 응답에도 CORS 층이 허용 출처 응답 머리를 붙였습니다.
사건 이름은 token 여섯 뒤에 `done`으로, 05·06절과 같은 차례입니다.
출력 줄 `이어 붙인 글:`의 글이 뒤에서 견줄 기준 응답의 글입니다.

## 4. 단계 기록

흐름이 단계마다 무엇을 받았는지 보려면 기록이 필요합니다.
다음 셀은 단계 이름과 응답을 받아, 기록 목록에 한 줄을 더하는 함수를 정의합니다.
한 줄에는 상태 코드와 허용 출처를 적습니다."""),
        code(DEF_RECORD),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
기록 한 줄은 단계 이름, 상태 코드, 허용 출처를 담은 목록입니다.
허용 출처는 07절 함수 `header_or_none`으로 읽어, 응답 머리가 없으면 `None`이 됩니다.

다음 셀은 기록 목록을 표 모양으로 출력하는 함수를 정의합니다."""),
        code(DEF_PRINT_LOG),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
라벨 줄 다음에, 기록 한 줄이 출력 한 줄이 됩니다.

## 5. 조립

부품을 흐름의 차례대로 잇습니다.
흐름이 길어 함수 둘로 나눴습니다.
다음 셀은 흐름의 앞 절반으로, 사전 요청과 첫 요청을 보냅니다."""),
        code(DEF_START),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
사전 요청의 요청 머리 이름은 07절과 같은 `Authorization, Content-Type`입니다.
첫 요청은 이어 받을 번호가 없어 `None`을 넘깁니다.
두 요청 모두 기록 목록에 한 줄씩 남기고, 첫 요청의 응답을 내놓습니다.

다음 셀은 흐름의 뒤 절반을 정의합니다.
받은 사건에 번호가 있으면, 요청 머리 이름에 `Last-Event-ID`를 더한 사전 요청을 한 번 더 보냅니다.
그다음 그 번호로 이어 받고, 받은 사건과 이어 받은 사건을 이은 목록을 내놓습니다."""),
        code(DEF_RESUME),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
받은 사건이 하나도 없으면 함수 `last_event_id`가 `None`을 내놓아, 이어 받기 단계를 보내지 않습니다.

이어 받기 요청은 요청 머리 `Last-Event-ID`를 더 싣습니다.
07절 출력처럼, 첫 사전 요청의 답에도 허용 요청 머리 `Last-Event-ID`가 이미 들어 있습니다.
브라우저는 그 답을 담아 두면, 정한 시간 안에는 사전 요청을 다시 보내지 않을 수 있습니다.
이 흐름은 담아 둔 답이 없는 경우를 흉내 내어, 그 이름을 적은 사전 요청을 한 번 더 보냅니다.

## 6. 실행 1 — 교재용 접근 토큰

실행 1은 2절의 재료 그대로 흐름을 끝까지 실행합니다.
첫 요청에서 앞 사건 둘만 받고 끊겼다고 보며, 06절 노트북 2절과 같은 자리입니다.
실행 전에 예상해 봅니다.
기록 목록에는 몇 단계가 남고, 모두 200일까요?"""),
        code(RUN1),
        md(r"""**결과 읽기** — 라벨 줄 아래 네 줄이 실행 1의 단계 기록입니다.
사전 요청, 첫 요청, 이어 받기 앞의 사전 요청, 이어 받기가 차례대로 모두 `200`입니다.
네 응답 모두 허용 출처가 `http://localhost:5173`으로, 화면의 출처와 같습니다.
07절의 규칙으로는 화면이 네 응답을 모두 읽을 수 있습니다.

다음 셀은 끊기기 전에 받은 사건과, 이어 받은 뒤 이은 사건을 봅니다."""),
        code(RUN1_IDS),
        md(r"""**결과 읽기** — 출력 줄 `끊기기 전에 받은 마지막 사건 번호: web-1:1`이 보입니다.
이어 받은 첫 사건 번호는 `web-1:2`로, 받은 번호의 바로 다음 자리입니다.
이은 사건 이름은 token 여섯 뒤에 `done`으로, 기준 응답과 같은 차례입니다.

다음 셀은 06절의 방법으로 실행 1을 판정합니다.
마지막 사건이 `done`인지 보고, 이어 붙인 글을 기준 응답의 글과 견줍니다."""),
        code(RUN1_JUDGE),
        md(r"""**결과 읽기** — 출력 줄 `마지막 사건이 done인가: True`와 `기준 응답의 글과 같은가: True`가 보입니다.
끊긴 뒤 이어 받아도, 같은 낱말이 겹치거나 빠지지 않았습니다.

## 7. 실행 2 — 접근 토큰 하나만 바꿈

실행 2는 값 하나만 바꿔, 접근 토큰을 07절 노트북 2절의 틀린 값 `Bearer wrong-token`으로 둡니다.
출처·질문·끊기는 자리·사전 요청의 머리 이름은 실행 1과 같습니다.
07절에서도 틀린 접근 토큰에는 401이 왔습니다.
새로 볼 것은 흐름의 어느 단계에서 무엇이 달라지는지입니다.

실행 전에 예상해 봅니다.
사전 요청의 상태 코드와 기록 목록의 줄 수는 어떻게 될까요?"""),
        code(RUN2),
        md(r"""**결과 읽기** — 라벨 줄 아래 두 줄이 실행 2의 단계 기록입니다.
사전 요청은 실행 1과 같이 `200`이고, 첫 요청은 `401`입니다.
401 응답에도 허용 출처 `http://localhost:5173`이 붙어 있습니다.
기록이 두 줄뿐이라, 이어 받기 앞의 사전 요청과 이어 받기는 보내지 않았습니다.

흐름이 보낸 사전 요청에는 요청 머리 `Authorization`이 없습니다.
07절의 사전 요청처럼 출처, 요청 방식, 요청 머리 이름만 실었습니다.
그래서 CORS 층은 접근 토큰과 상관없이 사전 요청에 답했습니다.
접근 토큰 검사는 그 뒤의 첫 요청에서, 처리 함수 앞의 제공 함수가 했습니다.

다음 셀은 첫 요청의 응답 본문과, 끊기기 전에 받은 사건을 봅니다."""),
        code(RUN2_BODY),
        md(r"""**결과 읽기** — 출력 줄 `첫 요청의 응답 본문: {'detail': '인증 정보가 올바르지 않습니다'}`가 보입니다.
07절의 401과 같은 본문이고, SSE 사건이 아니라 JSON 글입니다.
그래서 함수 `events_of`가 빈 목록을 내놓아, 받은 사건 수가 `0`입니다.
받은 마지막 사건 번호가 `None`이라, 뒤 절반은 이어 받기를 보내지 않았습니다.

다음 셀은 실행 2를 실행 1과 같은 방법으로 판정합니다."""),
        code(RUN2_JUDGE),
        md(r"""**결과 읽기** — 출력 줄 `마지막 사건이 done인가: False`와 `기준 응답의 글과 같은가: False`가 보입니다.
이은 사건이 하나도 없고, 06절에서 정한 대로 빈 목록은 끝까지 받지 못한 것으로 셉니다.
이어 붙인 글의 글자 수도 `0`입니다.

## 8. 두 실행 견주기

다음 셀은 두 실행의 단계 기록과 판정을 한 표로 모읍니다."""),
        code(COMPARE),
        md(r"""**결과 읽기** — 라벨 줄 아래 여섯 줄이 두 실행을 견줍니다.
줄 `사전 요청의 상태 코드 | 200 | 200`은 두 실행이 같습니다.
줄 `첫 요청의 허용 출처 | http://localhost:5173 | http://localhost:5173`도 같습니다.
줄 `첫 요청의 상태 코드 | 200 | 401`부터 달라져, 기록한 단계 수가 `4`에서 `2`로 줄었습니다.

**결론** — 바꾼 값은 요청 머리 `Authorization`의 접근 토큰 하나였습니다.
사전 요청은 접근 토큰을 싣지 않아, 두 실행 모두 200이었습니다.
접근 토큰이 틀리면 첫 요청이 401로 끝나고, 흐름은 이어 받기로 가지 않았습니다.
401 응답에도 허용 출처 응답 머리가 붙어, 07절의 규칙으로는 화면이 이 오류 응답도 읽을 수 있습니다.
이 값들은 모델 없이 매번 같은 값이고, 걸린 시간은 재지 않았습니다.

## 정리

1. 사전 요청·SSE 응답·이어 받기를 한 흐름으로 이어, 끊긴 뒤에도 기준 응답과 같은 글을 받았습니다.
2. 흐름의 사전 요청은 접근 토큰과 상관없이 200이었고, 허용 출처 응답 머리는 401 응답에도 붙었습니다.
3. 접근 토큰 하나만 틀리면 흐름은 첫 요청의 401에서 멈췄고, 06절의 판정은 `False`였습니다.

이 절로 Ch 30이 끝납니다.
Ch 31에서는 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다.
Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장합니다.
이 챕터의 실습 앱에 붙이는 일은 다루지 않습니다.
보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
table_html = author_06.table_html
html_text = author_06.html_text


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    """.mmd가 있을 때만 본문에 넣습니다(새 커널 A·B를 그림보다 먼저 돌릴 때 빌드가 멈추지 않게)."""
    if not (FIGS / (name + ".mmd")).is_file():
        return ""
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_01 = "01-비동기-라우팅과-스키마.html"
L_02 = "02-의존성으로-Agent-주입.html"
L_03 = "03-ainvoke-요청-응답.html"
L_04 = "04-astream과-응답-스트림.html"
L_05 = "05-POST-SSE-이벤트-설계.html"
L_06 = "06-fetch-재연결과-오류-이벤트.html"
L_07 = "07-인증-CORS-타임아웃.html"
L_08 = "08-OpenAPI와-TS-SDK.html"
L_09 = "09-실제-Agent-HTTP-통합.html"
L_CH31_01 = "../../part7/ch31-database/01-SQLAlchemy-비동기-PostgreSQL.html"


def link(href: str, label: str) -> str:
    return '<a href="' + href + '">' + label + "</a>"


LEARNED_ROWS = [
    (link(L_01, "01절"), "시험용 클라이언트 <code>TestClient(app)</code>, 입력 형식 <code>ChatRequest</code>의 칸 <code>question</code>·<code>thread_id</code>", "재료의 시험용 클라이언트와 질문 본문"),
    (link(L_02, "02절"), "의존성과 제공 함수, 재정의 딕셔너리 <code>dependency_overrides</code>", "처리 함수 머리 99~105행 읽기, 재정의 딕셔너리의 키 수 0 확인"),
    (link(L_04, "04절"), "진행 값의 칸 <code>token</code>을 이어 붙이는 함수 <code>join_tokens</code>(도구 파일)", "이어 붙인 글"),
    (link(L_05, "05절"), "요청 주소 <code>/v1/chat/stream</code>의 SSE 응답, SSE 사건의 칸 <code>event</code>·<code>id</code>·<code>data</code>", "첫 요청과 이어 받기 요청의 응답"),
    (link(L_06, "06절"), "요청 머리 <code>Last-Event-ID</code>로 이어 받기, 함수 <code>last_event_id</code>·<code>read_events</code>·<code>event_names</code>·<code>token_values</code>·<code>ended_with_done</code>(도구 파일)", "끊긴 뒤 이어 받기와 두 실행의 판정"),
    (link(L_07, "07절"), "접근 토큰 검사와 401, CORS 사전 요청과 허용 출처 응답 머리, 함수 <code>header_or_none</code>(도구 파일)", "사전 요청 단계, 단계 기록의 허용 출처, 실행 2의 틀린 접근 토큰"),
]

NAME_ROWS = [
    ("<code>send_preflight(header_names)</code>", "허용 출처 화면의 사전 요청을 <code>/v1/chat/stream</code>에 보냅니다", "이 절에서 만듦(07절 사전 요청 모양)"),
    ("<code>send_question(token, resume_id)</code>", "출처와 접근 토큰, 번호가 있으면 <code>Last-Event-ID</code>까지 실어 질문을 보냅니다", "이 절에서 만듦(05·06·07절 요청 모양)"),
    ("<code>events_of(response)</code>", "상태 코드가 200이면 칸 딕셔너리 목록, 아니면 빈 목록을 내놓습니다", "이 절에서 만듦(06절 <code>read_events</code>를 부름)"),
    ("<code>record_step</code>·<code>print_log</code>", "단계 기록에 한 줄 더하기, 기록을 표 모양으로 출력하기", "이 절에서 만듦"),
    ("<code>start_flow</code>·<code>resume_flow</code>", "흐름의 앞 절반(사전 요청·첫 요청)과 뒤 절반(사전 요청·이어 받기)", "이 절에서 만듦"),
    ("<code>last_event_id</code>·<code>read_events</code>·<code>event_names</code>·<code>token_values</code>·<code>ended_with_done</code>", "받은 마지막 사건 번호, 칸 딕셔너리 목록, 사건 이름, 칸 <code>data</code>를 읽은 값, 끝 판정", "도구 파일(06절)"),
    ("<code>header_or_none</code>", "응답 머리 한 칸의 값, 없으면 <code>None</code>", "도구 파일(07절)"),
    ("<code>join_tokens</code>", "칸 <code>token</code>의 글을 차례대로 이어 붙이기", "도구 파일(04절)"),
]

COMPARE_ROWS = [
    ("바꾼 값 — 접근 토큰", "<code>Bearer local-demo-token</code>", "<code>Bearer wrong-token</code>"),
    ("사전 요청의 상태 코드", "<code>200</code>", "<code>200</code>"),
    ("첫 요청의 상태 코드", "<code>200</code>", "<code>401</code>"),
    ("첫 요청의 허용 출처", "<code>http://localhost:5173</code>", "<code>http://localhost:5173</code>"),
    ("기록한 단계 수", "<code>4</code>", "<code>2</code> — 이어 받기 앞의 사전 요청과 이어 받기를 보내지 않음"),
    ("마지막 사건이 done인가", "<code>True</code>", "<code>False</code>"),
    ("기준 응답의 글과 같은가", "<code>True</code>", "<code>False</code>"),
]

LOOK_B5 = "노트북 3절에서 <code>허용 출처: http://localhost:5173</code>과 token 여섯 뒤 <code>done</code>인 사건 이름을 찾습니다. 6절에서는 단계 기록 네 줄의 <code>200</code>과, <code>끊기기 전에 받은 마지막 사건 번호: web-1:1</code>·<code>이어 받은 첫 사건 번호: web-1:2</code>를 봅니다. 마지막으로 <code>기준 응답의 글과 같은가: True</code>를 확인합니다."
LOOK_B6 = "7절의 단계 기록 두 줄에서 <code>첫 요청 | 401 | http://localhost:5173</code>을 찾습니다. 8절 표의 줄 <code>기록한 단계 수 | 4 | 2</code>와 <code>마지막 사건이 done인가 | True | False</code>도 확인합니다. 바꾼 값은 접근 토큰 하나뿐이라, 두 칸의 차이는 모두 그 값에서 나왔습니다."


def src_html() -> str:
    learned = table_html(["절", "배운 것", "실습에서 쓰는 곳"], LEARNED_ROWS)
    names = table_html(["이름", "하는 일", "가져온 곳"], NAME_ROWS)
    compare = table_html(["견준 것", "실행 1", "실행 2"], COMPARE_ROWS)
    return """<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>05~07절에서 배운 사전 요청·SSE 응답·이어 받기를 한 요청 흐름으로 이어, 끊긴 SSE 응답을 이어 받을 수 있습니다.</li>
<li>단계마다 상태 코드와 허용 출처를 기록하고, 이어 붙인 글을 끊기지 않은 응답의 글과 견줄 수 있습니다.</li>
<li>접근 토큰 하나만 바꾼 실행에서, 흐름이 어느 단계에서 멈추는지 단계 기록으로 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 웹 앱이 답을 보내는 방법을 절마다 따로 익혔습니다. """ + link(L_05, "05절") + """은 답을 SSE 사건으로 보냈고, """ + link(L_06, "06절") + """은 끊긴 뒤 사건 번호로 이어 받았습니다. """ + link(L_07, "07절") + """은 접근 토큰을 검사하고, 다른 출처의 화면에 응답 머리로 허락을 알렸습니다. 실제 웹 화면에서는 이 일들이 질문 하나 안에서 차례로 일어납니다.</p><p>이번 실습은 세 기능을 도서관 웹 화면의 질문 하나에 모아 실행합니다. 화면은 SSE 사건 둘을 받고 끊긴 뒤, 받은 마지막 사건 번호로 이어 받습니다. 접근 토큰 하나만 바꿔 한 번 더 실행하고, 두 실행의 단계 기록을 견줍니다. 07절에서도 틀린 접근 토큰에는 401이 왔습니다. 새로 볼 것은 그 401이 흐름의 어느 단계에서 나오고, 사전 요청과 허용 출처 응답 머리가 어떻게 되는지입니다.</p><p>제목의 서빙은 만든 에이전트를 웹 앱에 올려, 요청에 답하게 하는 일입니다. 이번 절은 이 챕터의 실습입니다. 01~09절에서 쓴 이름과 Ch 2에서 배운 문법만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p><p>이 절의 질문 — 사전 요청, SSE 응답, 이어 받기를 한 흐름으로 이으면 끊긴 답을 온전히 받을 수 있을까요? 접근 토큰 하나를 바꾸면 흐름의 어디까지 달라질까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 앞 절 함수는 도구 파일 <code>serve_tools.py</code>에서 가져오고, 흐름을 잇는 함수는 노트북에 적습니다.</p>""" + learned + """
<p>붙인 기능은 05절 SSE 응답, 06절 이어 받기, 07절 사전 요청과 접근 토큰 셋이고, 모두 실행 1 흐름에서 일합니다. 01절의 422와 03절의 JSON 요청 주소는 SSE 응답을 받는 흐름 하나에 모으려고 뺐습니다. 02·06절의 시간 제한 재정의는 06절에서 이미 견줘 뺐고, 07절 <code>HTTPBearer</code> 새 앱은 실습 앱을 고치지 않으려고 뺐습니다. 04절 <code>astream</code>은 앱이 안에서 부르고, 08절 응답 문서는 요청 흐름에 들지 않아 뺐습니다. """ + link(L_09, "09절") + """의 실제 모델은 결론을 매번 같은 값으로 내려고 부르지 않았습니다.</p><p>이 챕터의 실습은 모델을 부르지 않습니다. 01~08절도 모델을 쓰지 않는 그래프로 결과를 갈랐고, 이번 흐름의 결론도 상태 코드와 사건 번호처럼 매번 같은 값입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + METAPHOR + """
""" + illustration_block() + """<h3>실습 조립의 구성</h3>""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + names + """
<p>함수 <code>send_preflight</code>와 <code>send_question</code>은 노트북 2절에서 만든 시험용 클라이언트와 출처, 질문 본문을 그대로 씁니다. 두 실행에서 달라지는 값은 인자 <code>token</code> 하나뿐입니다. 흐름을 잇는 함수 둘은 기록 목록을 인자로 받아, 단계마다 한 줄씩 남깁니다.</p>
<h3>흐름이 지나는 실습 앱의 자리</h3><p>요청 주소 <code>/v1/chat/stream</code>에 온 요청은 먼저 앱 19~26행의 CORS 층을 지납니다. 사전 요청이면 CORS 층이 앱으로 넘기지 않고 바로 답합니다. 사전 요청이 아니면 CORS 층은 요청을 앱으로 넘기고, 앱이 보낸 응답에 허용 출처 응답 머리를 붙입니다.</p><p>앱으로 넘어간 요청은 처리 함수 <code>chat_stream</code>의 제공 함수들을 먼저 지납니다. 제공 함수 <code>require_token</code>이 접근 토큰을 검사하고, 틀리면 401로 답합니다. 제공 함수 <code>get_resume_index</code>는 요청 머리 <code>Last-Event-ID</code>에서 이어 받을 자리를 읽습니다. 두 검사를 지나야 처리 함수 몸통이 SSE 사건을 보냅니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 1절은 준비이고, 2절은 처리 함수의 머리와 재료를 봅니다. 3~5절은 흐름의 부품과 단계 기록, 조립을 정의합니다. 6절은 교재용 접근 토큰으로 흐름을 실행하고, 끊긴 뒤 이어 받은 글을 기준 응답과 견줍니다.</p><p>모델 요청은 0번이라 API 키가 필요 없습니다. 서버 프로그램 없이 시험용 클라이언트로 요청하고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 요청 머리 <code>Authorization</code>에 실은 접근 토큰 하나만 달랐습니다. 출처, 질문, 끊기는 자리, 사전 요청의 머리 이름은 같았습니다. 결과는 아래 표와 같았습니다.</p>""" + compare + """
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>사전 요청은 두 실행 모두 200이었습니다. 흐름이 보낸 사전 요청에는 접근 토큰이 없고, CORS 층이 앱으로 넘기지 않고 답하기 때문입니다. 그래서 접근 토큰이 틀렸다는 것은 사전 요청 단계에서는 드러나지 않았습니다.</p><p>달라진 것은 첫 요청부터입니다. 실행 2의 첫 요청은 제공 함수 <code>require_token</code>에서 401로 끝났고, 본문은 SSE 사건이 아니라 JSON 글이었습니다. 받은 사건이 없어 받은 마지막 사건 번호도 없었고, 흐름은 이어 받기 앞의 사전 요청과 이어 받기를 보내지 않았습니다. 06절의 판정은 빈 목록을 끝까지 받지 못한 것으로 세어 <code>False</code>였습니다.</p><p>401 응답에도 허용 출처 응답 머리 <code>http://localhost:5173</code>이 붙었습니다. CORS 층은 앱이 보낸 응답이면 상태 코드와 상관없이 이 머리를 붙입니다. 07절의 규칙으로는 화면의 스크립트가 이 401을 읽을 수 있어, 접근 토큰이 틀렸다는 것을 화면에 알릴 수 있습니다. 브라우저에서 이 동작을 실행하지는 않았습니다.</p>
<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>손으로 적은 값은 모두 실행 전에 정했습니다. 출처 <code>http://localhost:5173</code>은 앱 21행의 허용 출처이고, 질문은 03~07절과 같습니다. 스레드 이름 <code>web-1</code>은 이 절에서 정했습니다. 교재용 접근 토큰은 앱 57행의 값이고, 틀린 접근 토큰은 07절 노트북 2절에서 쓴 값입니다.</li><li>끊기는 자리 둘은 06절 노트북 2절과 같은 자리입니다. 연결을 실제로 끊지 않고, 첫 응답에서 앞 사건 둘만 받은 것으로 보았습니다. 사전 요청의 머리 이름 글은 07절과 같은 글에, 이어 받기 때 <code>Last-Event-ID</code>를 더했습니다.</li><li>시험용 클라이언트는 CORS 규칙을 따지지 않고, 응답 머리만 보여 줍니다. 화면이 응답을 읽을 수 있는지는 07절에서 본 규칙으로 말한 것이고, 브라우저에서는 실행하지 않았습니다. </li><li>첫 사전 요청의 답에도 허용 요청 머리 <code>Last-Event-ID</code>와 담아 둘 시간 600초가 이미 붙어 옵니다. 설치판 starlette <code>cors.py</code> 26행의 기본값 600을 56행이 응답 머리 <code>access-control-max-age</code>로 적습니다. MDN 문서는 브라우저가 그 시간 안에는 같은 사전 요청을 다시 보내지 않을 수 있다고 적습니다. 이 흐름의 두 번째 사전 요청은 담아 둔 답이 없는 경우를 흉내 낸 것이고, 브라우저에서 확인하지는 않았습니다.</li><li>시험용 클라이언트는 응답이 끝난 뒤 본문을 한꺼번에 줍니다. 그래서 사건이 도착한 때는 이 절 결과로 말할 수 없고, 걸린 시간도 재지 않았습니다.</li><li>06절에서 본 것처럼, 이어 받기 요청마다 앱은 그래프를 처음부터 다시 실행하고 앞 자리를 건너뜁니다. 이 절의 그래프에는 바깥에 쓰는 일이 없어, 다시 실행해도 같은 사건이 나왔습니다.</li><li>401에서 이어 받기로 가지 않은 것은 이 절의 흐름 코드가 정한 것입니다. 받은 사건이 없으면 함수 <code>last_event_id</code>가 <code>None</code>을 내놓고, 함수 <code>resume_flow</code>가 그 자리에서 멈춥니다. 401을 받은 화면이 접근 토큰을 새로 얻는 방법은 이 절에서 다루지 않았습니다.</li><li>실습 앱의 401 응답에 인증 방식을 알리는 응답 머리가 없다는 것은 07절에서 보았습니다. 이 절도 실습 앱 파일을 고치지 않았고, 실습 폴더에 쓰는 파일도 없습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>사전 요청·SSE 응답·이어 받기를 한 흐름으로 이어, 끊긴 뒤에도 기준 응답과 같은 글을 받았습니다.</li><li>흐름의 사전 요청은 접근 토큰과 상관없이 200이었고, 허용 출처 응답 머리는 401 응답에도 붙었습니다.</li><li>접근 토큰 하나만 틀리면 흐름은 첫 요청의 401에서 멈췄고, 06절의 판정은 <code>False</code>였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 30이 끝납니다. """ + link(L_CH31_01, "Ch 31") + """은 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다. Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장합니다. 이 챕터의 실습 앱에 붙이는 일은 다루지 않습니다. 보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 실행 2에서 접근 토큰이 틀렸는데도 사전 요청이 200이었던 까닭은 무엇인가요?</p><p class="quiz-a">흐름이 보낸 사전 요청에는 요청 머리 <code>Authorization</code>이 없습니다. 또 CORS 층은 사전 요청을 앱으로 넘기지 않고 바로 답하므로, 접근 토큰을 검사하는 제공 함수까지 가지 않습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">2. 실행 1에서 이어 받은 첫 사건 번호는 무엇이었고, 왜 그 번호였나요?</p><p class="quiz-a">번호는 <code>web-1:2</code>였습니다. 끊기기 전에 받은 마지막 번호 <code>web-1:1</code>을 요청 머리 <code>Last-Event-ID</code>로 보내자, 앱이 그다음 자리부터 보냈습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 함수 <code>resume_flow</code>는 이어 받기 전에 사전 요청을 한 번 더 보냅니다. 실제 브라우저도 늘 이렇게 다시 보낼까요?</p><p class="quiz-a">늘 그렇지는 않습니다. 첫 사전 요청의 답에도 허용 요청 머리 <code>Last-Event-ID</code>가 이미 들어 있습니다. 브라우저는 그 답을 정한 시간 동안 담아 두면, 그동안 다시 묻지 않을 수 있습니다. 이 흐름은 담아 둔 답이 없는 경우를 흉내 내어 한 번 더 보냈고, 200을 받았습니다. 틀렸다면 노트북 5절과 6절을 다시 읽습니다.</p><p class="quiz-q">4. 동료가 「401이 났으니 허용 출처 응답 머리도 없을 것」이라고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 실행 2의 401 응답에도 허용 출처 <code>http://localhost:5173</code>이 붙었습니다. CORS 층은 앱이 보낸 응답이면 상태 코드와 상관없이 이 머리를 붙입니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">5. 실행 2의 판정 <code>ended_with_done</code>이 <code>False</code>였던 까닭은 무엇인가요?</p><p class="quiz-a">401 응답은 SSE 사건이 아니어서 받은 사건이 하나도 없었고, 이어 받기도 보내지 않았습니다. 06절에서 정한 대로, 이 함수는 빈 목록을 끝까지 받지 못한 것으로 셉니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>""" + link(L_07, "07절") + """ 참고 자료에 CORS와 사전 요청의 문서가 있습니다. SSE 이어 받기와 요청 머리 <code>Last-Event-ID</code>의 문서는 """ + link(L_06, "06절") + """ 참고 자료에 있습니다.</li><li>설치판 starlette 1.6.0 소스 <code>middleware/cors.py</code> 91~94행은 사전 요청이면 앱으로 넘기지 않고 바로 답합니다. 152~154행은 그 밖의 요청을 앱으로 넘깁니다. 156~174행은 응답을 보내기 시작할 때 허용 출처 응답 머리를 붙이고, 상태 코드는 보지 않습니다. 26행은 담아 둘 시간의 기본값 600초이고, 56행이 그 값을 응답 머리 <code>Access-Control-Max-Age</code>로 적습니다.</li><li><div><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Max-Age">MDN Access-Control-Max-Age</a></div>확인 2026-09-29 · 허용 요청 방식과 허용 요청 머리의 정보를 담아 둘 수 있는 시간을 알린다고 적습니다.</li><li>실습 폴더 <code>agent_service/app.py</code> 19~26행은 CORS 설정이고, 24행 <code>allow_headers</code>에 <code>Last-Event-ID</code>가 있습니다. 41~53행은 제공 함수 <code>get_resume_index</code>, 56~60행은 <code>require_token</code>입니다. 99~124행은 처리 함수 <code>chat_stream</code>입니다.</li><li>도구 파일 <code>notebooks/serve_tools.py</code>의 함수 <code>last_event_id</code>는 06절 노트북에서, <code>header_or_none</code>은 07절 노트북에서 옮겼습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


def write_tools() -> None:
    """도구 파일은 09 판이거나 이 판일 때만 쓴다. 이 판으로 시작하는 더 긴 판(뒤에서 함수를 더함)은 덮어쓰지 않는다."""
    current = ""
    if TOOLS_PATH.is_file():
        current = TOOLS_PATH.read_text(encoding="utf-8")
    assert current == "" or current.startswith(author_09.TOOLS09), "도구 파일이 09 판으로 시작하지 않습니다"
    if current == "" or current == author_09.TOOLS09 or current == TOOLS10:
        TOOLS_PATH.write_text(TOOLS10, encoding="utf-8")
        print("wrote", TOOLS_PATH, hashlib.sha256(TOOLS10.encode("utf-8")).hexdigest()[:12])
    elif current.startswith(TOOLS10):
        print("skip", TOOLS_PATH, "(뒤에서 함수를 더한 판 — 덮어쓰지 않음)")
    else:
        raise SystemExit("도구 파일이 09 판도 10 판도 아닌 모양입니다 — 손으로 확인하세요")


if __name__ == "__main__":
    # 1절 파일 위치 셀은 01절 셀 글 그대로(「01절 2절과 같은 파일 위치 셀」 문장의 근거)
    assert FIND_LAB in AUTHOR01.read_text(encoding="utf-8"), "FIND_LAB이 01절 셀과 다릅니다"
    check_tools10()
    check_older_guards()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "serve_tools.py").write_text(TOOLS10, encoding="utf-8")
        print("wrote tools copy (10 판) in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        write_tools()
        path = write_notebook(LAB, "10", SLUG, "experiment", cells())
        print("wrote", path)
