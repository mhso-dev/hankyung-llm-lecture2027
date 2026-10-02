"""Ch 30 02절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 paired).

사용:
  python3 -B author_02.py            → 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_02.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **paired 형식 유지**. 슬러그 그대로.

## 결정 1 — paired: Before = 재정의 누수(실제 결함, Ch 2 11 b8이 기댐), After = 재정의 딕셔너리 비우기

클래스·lambda·가짜 에이전트 없이, 실습 앱의 제공 함수 get_timeout을 0.0을 내놓는 이름 있는 async def zero_timeout으로
재정의한다. 첫 테스트 질문 504(재정의가 뜻한 결과 — 노랑) → 다음 테스트가 새 TestClient로 보낸 보통 질문도 504,
재정의 딕셔너리 키 수 1(Before 결함 결과 — 빨강) → After app.dependency_overrides.clear() 뒤 키 수 0·200(노랑).
값 바꿔 보기 = 재정의 딕셔너리의 값만 2.0을 내놓는 two_second_timeout으로 → 200인데 키 수 1(상태 코드로는 안 보임, 빨강 0).
노트북 밖 /tmp/ch30-02/exp/p1_scene.py 5/5 같음(준비 노트 e6_repeat.py 5/5와 같은 장면).

## 결정 2 — 예시 부분: 연습 앱 demo_app에 의존성 하나(Depends 동작)와 재정의 하나

제공 함수 get_limit(요청마다 provider_calls에 적음, 2.0) → LimitDep = Annotated[float, Depends(get_limit)](Ch 13 02 표시 Annotated
이음, FastAPI 문서의 type alias 모양 = 실습 앱 TimeoutDep 모양) → 처리 함수 show_limit(limit: LimitDep) → 요청 두 번에 기록 둘.
재정의 get_limit → get_short_limit(0.5) → 응답 0.5·기록 []·키 수 1(남은 재정의는 4절에서 실습 앱으로).
기본값 모양 x=Depends(f)는 기본값 매개변수라 쓰지 않는다.

## 결정 3 — 실습 앱 가져오기(02가 처음, handoff 「파일 위치 셀」)

파일 위치 셀은 01절 셀 글 그대로(FIND_LAB — __main__에서 author_01.py와 문자열 대조) → os.chdir(lab_path) →
from agent_service.app import app, get_agent, get_timeout(agent_service.app 속성은 FastAPI 객체라 이 모양만).
앱 파일 app.py는 고치지 않는다(이 절이 읽는 줄 29~38·63~67·75~83은 과정이 푼 모양 — Annotated·Depends·내놓는 값 힌트(Ch 2 07).
나머지 금지 문법은 06 이어 받기·07 인증·05 스트림 줄이라 그 절 몫, app.openapi() 기준값 06e5d1b9… 그대로).
설치 셀은 01 넷 + live_agent.py가 가져오는 langgraph·langchain(모델 객체는 만들지 않음).

## 결정 4 — 비동기

처리 함수·제공 함수 async def(셀당 하나, 01이 풂) + 셀 맨 위 await(Ch 28 01 이음 — 제공 함수를 직접 불러 값 보기).
asyncio.wait_for는 본문·노트북에서 첫 풀이 한 문장(앱 파일 78~80행이 씀, 노트북은 부르지 않음).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 딕셔너리 `.get`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·대입 풀기·별표 풀기·
`while`·`try`·세미콜론·`isinstance`·클래스·가짜 에이전트. 데코레이터는 요청 주소 줄 하나(@demo_app.get), 힌트는 처리 함수
매개변수 `limit: LimitDep`(챕터 예외), async def 다섯(제공 함수 넷·처리 함수 하나), 셀 맨 위 await 셋. 호출 깊이 2 이하.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part7/ch30-fastapi-serving/notebooks"
FIGS = ROOT / "textbook/part7/ch30-fastapi-serving/figures"
SLUG = "02-의존성으로-Agent-주입"
TITLE_TEXT = "의존성으로 Agent 주입"
SRC = ROOT / "textbook/part7/ch30-fastapi-serving/_src" / (SLUG + ".html")
AUTHOR01 = ROOT / "textbook/part7/ch30-fastapi-serving/qa/upgrade/author_01.py"
RUNS_SENTENCE = os.environ.get("AUTHOR02_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물넷의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 모델을 부르지 않아, 이 절의 출력은 앱과 시험용 클라이언트가 주고받은 값으로 정해집니다.")

# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["fastapi==0.135.0", "httpx==0.28.1", "pydantic==2.12.5", "starlette==1.6.0",
                          "langgraph==1.2.11", "langchain==1.4.0"])

IMPORTS = r'''# 이 절에서 쓸 이름을 가져옵니다(os·typing은 Python에 들어 있는 모듈입니다)
import os
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

print("가져온 fastapi 이름:", "Depends, FastAPI, TestClient")'''

DEMO_APP = r'''# 연습용 앱 객체와, 제공 함수가 불린 기록을 적을 빈 목록을 만듭니다
demo_app = FastAPI(title="연습 앱")
provider_calls = []
print("앱 이름:", demo_app.title)'''

DEF_LIMIT = r'''# 처리 함수에 넘길 시간 제한 초를 내놓는 제공 함수를 정의합니다
async def get_limit():
    # 불릴 때마다 목록에 이름을 적습니다(몇 번 불렸는지 보려는 줄입니다)
    provider_calls.append("get_limit")
    return 2.0'''

LIMIT_DEP = r'''# 자료형 float 옆에 「get_limit이 내놓는 값」이라는 의존성을 적어, 이름 LimitDep에 담습니다
LimitDep = Annotated[float, Depends(get_limit)]'''

DEF_SHOW = r'''# 요청 방식 GET과 요청 주소 /limit의 짝에, 시간 제한 초를 받는 처리 함수를 잇습니다
@demo_app.get("/limit")
async def show_limit(limit: LimitDep):
    return {"limit": limit}'''

CALL_TWICE = r'''# 같은 요청을 두 번 넣고, 응답과 제공 함수가 불린 기록을 봅니다
demo_client = TestClient(demo_app)
first_response = demo_client.get("/limit")
second_response = demo_client.get("/limit")
print("첫 응답:", first_response.status_code, first_response.json())
print("둘째 응답:", second_response.status_code, second_response.json())
print("제공 함수가 불린 기록:", provider_calls)'''

DEF_SHORT = r'''# 시험 때 바꿔 낄, 시간 제한 0.5초를 내놓는 함수를 정의합니다
async def get_short_limit():
    return 0.5'''

OVERRIDE_DEMO = r'''# 재정의 딕셔너리에 원래 함수를 키로, 바꿔 낄 함수를 값으로 적고 다시 요청합니다
demo_app.dependency_overrides[get_limit] = get_short_limit
provider_calls = []
override_response = demo_client.get("/limit")
print("응답:", override_response.status_code, override_response.json())
print("제공 함수가 불린 기록:", provider_calls)
print("재정의 딕셔너리의 키 수:", len(demo_app.dependency_overrides))'''

# 01절 2절 셀 글 그대로(아래 __main__에서 author_01.py와 문자열 대조)
FIND_LAB = r'''# 노트북을 연 자리에서 본 실습 폴더의 위치를 후보 셋 가운데에서 고릅니다
candidates = ["..", ".", "labs/part7/ch30-fastapi-serving"]
lab_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/agent_service/schemas.py"):
        lab_path = candidate
        break
print("실습 폴더를 찾았는가:", lab_path is not None)
assert lab_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

IMPORT_APP = r'''# 작업 폴더를 실습 폴더로 옮기고, 앱 파일에서 앱 객체와 제공 함수 둘을 가져옵니다
os.chdir(lab_path)
from agent_service.app import app, get_agent, get_timeout
print("가져온 앱 이름:", app.title)
print("재정의 딕셔너리의 키 수:", len(app.dependency_overrides))'''

READ_DEPENDS = r'''# 앱 파일을 글로 읽어, 의존성을 적은 줄과 처리 함수 chat의 정의 줄만 출력합니다
with open("agent_service/app.py", encoding="utf-8") as app_file:
    app_text = app_file.read()
print("의존성을 적은 줄과 chat의 정의 줄:")
for line in app_text.splitlines():
    if "Depends(" in line or line.startswith("async def chat("):
        print(line)'''

PROVIDER_VALUES = r'''# 제공 함수 둘을 직접 불러, 시간 제한 초와 두 번 받은 그래프를 봅니다
original_seconds = await get_timeout()
first_graph = await get_agent()
second_graph = await get_agent()
print("get_timeout이 내놓은 초:", original_seconds)
print("두 번 받은 그래프가 같은 객체인가:", first_graph is second_graph)'''

NO_TOKEN = r'''# 실습 앱에 시험용 클라이언트를 붙이고, 접근 토큰 없이 POST /v1/chat 요청을 넣습니다
client = TestClient(app)
question_body = {"question": "휴관일을 알려 주세요", "thread_id": "dep-01"}
no_token_response = client.post("/v1/chat", json=question_body)
print("상태 코드:", no_token_response.status_code)
print("응답 본문:", no_token_response.json())'''

WITH_TOKEN = r'''# 요청 머리의 칸 Authorization에 접근 토큰을 적어, 같은 요청을 다시 넣습니다
auth_headers = {"Authorization": "Bearer local-demo-token"}
ok_response = client.post("/v1/chat", json=question_body, headers=auth_headers)
print("상태 코드:", ok_response.status_code)
print("응답 본문:", ok_response.json())'''

DEF_ZERO = r'''# 시험용으로, 시간 제한 0초를 내놓는 함수를 정의합니다
async def zero_timeout():
    return 0.0'''

REGISTER = r'''# 첫 테스트: 재정의 딕셔너리에 get_timeout 대신 zero_timeout을 적습니다
app.dependency_overrides[get_timeout] = zero_timeout
zero_seconds = await zero_timeout()
print("재정의할 함수가 내놓는 초:", zero_seconds)
# 키와 값은 함수 객체라서, 속성 __name__으로 이름을 꺼냅니다
for original in app.dependency_overrides:
    replacement = app.dependency_overrides[original]
    print("재정의:", original.__name__, "→", replacement.__name__)
print("재정의 딕셔너리의 키 수:", len(app.dependency_overrides))'''

FIRST_Q = r'''# 첫 테스트의 질문을 보내고, 상태 코드와 응답 본문을 봅니다
first_body = {"question": "휴관일을 알려 주세요", "thread_id": "test-01"}
first_test = client.post("/v1/chat", json=first_body, headers=auth_headers)
print("상태 코드:", first_test.status_code)
print("응답 본문:", first_test.json())'''

NEXT_Q = r'''# 다음 테스트: 새 시험용 클라이언트를 만들어 다른 질문을 보냅니다(재정의는 지우지 않았습니다)
next_client = TestClient(app)
next_body = {"question": "대출 기간을 알려 주세요", "thread_id": "test-02"}
next_test = next_client.post("/v1/chat", json=next_body, headers=auth_headers)
print("상태 코드:", next_test.status_code)
print("응답 본문:", next_test.json())
print("재정의 딕셔너리의 키 수:", len(app.dependency_overrides))'''

CLEAR = r'''# After: 첫 테스트가 끝날 때 재정의 딕셔너리를 비웁니다
app.dependency_overrides.clear()
print("재정의 딕셔너리의 키 수:", len(app.dependency_overrides))'''

NEXT_AGAIN = r'''# 다음 테스트의 질문을 같은 클라이언트로 다시 보냅니다
after_test = next_client.post("/v1/chat", json=next_body, headers=auth_headers)
print("상태 코드:", after_test.status_code)
print("응답 본문:", after_test.json())'''

DEF_TWO = r'''# 시험용으로, 원래 제공 함수와 같은 2초를 내놓는 함수를 정의합니다
async def two_second_timeout():
    return 2.0'''

VARY = r'''# 재정의 딕셔너리의 값만 two_second_timeout으로 바꿔 적고, 다음 테스트의 질문을 보냅니다
app.dependency_overrides[get_timeout] = two_second_timeout
two_seconds = await two_second_timeout()
vary_test = next_client.post("/v1/chat", json=next_body, headers=auth_headers)
print("재정의할 함수가 내놓는 초:", two_seconds)
print("상태 코드:", vary_test.status_code)
print("재정의 딕셔너리의 키 수:", len(app.dependency_overrides))'''

CLEANUP = r'''# 노트북을 마치기 전에, 두 앱의 재정의 딕셔너리를 모두 비웁니다
app.dependency_overrides.clear()
demo_app.dependency_overrides.clear()
print("실습 앱의 키 수:", len(app.dependency_overrides))
print("연습 앱의 키 수:", len(demo_app.dependency_overrides))'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/02-figures.md)
FIG1 = "02-1-요청마다-불리는-제공-함수"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 요청 GET /limit 두 번 보냄에서 회색 상자 라이브러리가 요청마다 제공 함수를 부름으로 화살표가 갑니다. 이어서 파란 상자 제공 함수 get_limit 내놓는 값 2.0과 파란 상자 처리 함수 show_limit 매개변수 limit: LimitDep을 지나 노란 상자 응답 두 번 200 limit 2.0으로 이어집니다. 제공 함수 상자에서 노란 상자 불린 기록 get_limit 두 번으로도 화살표가 가는 그림"
FIG1_CAP = "라이브러리가 요청마다 제공 함수 get_limit을 불러, 내놓은 값 2.0을 처리 함수의 매개변수에 넣었습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 보낸 요청이고, 회색 상자는 라이브러리가 하는 일입니다.
파란 상자 둘은 노트북 2절에서 우리가 만든 제공 함수와 처리 함수입니다.
노란 상자 둘은 2절 출력의 응답과 불린 기록입니다."""

FIG2 = "02-2-재정의-딕셔너리로-바꿔-낀-함수"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 요청 GET /limit과 파란 상자 재정의 딕셔너리 키 get_limit 값 get_short_limit에서 회색 상자 라이브러리가 딕셔너리에서 바꿔 낄 함수를 찾음으로 화살표가 모입니다. 이어서 파란 상자 get_short_limit 내놓는 값 0.5와 파란 상자 처리 함수 show_limit 고치지 않음을 지나 노란 상자 200 limit 0.5, get_limit 불린 기록 없음, 딕셔너리 키 수 1로 가는 그림"
FIG2_CAP = "재정의 딕셔너리에 적은 함수가 원래 제공 함수 대신 불려, 처리 함수를 고치지 않고도 받는 값이 0.5로 바뀌었습니다."
FIG2_READ = """위에서 아래로 읽습니다.
초록 상자는 보낸 요청이고, 파란 상자 셋은 노트북 2절에서 적은 재정의와 두 함수입니다.
회색 상자는 라이브러리가 요청마다 재정의 딕셔너리를 보는 자리입니다.
노란 상자는 2절 출력이고, 원래 제공 함수 get_limit은 한 번도 불리지 않았습니다."""

FIG3 = "02-3-실습-앱-chat이-받는-의존성-셋"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 요청 POST /v1/chat 질문과 thread_id에서 라이브러리가 요청마다 부르는 제공 함수 셋이라는 칸으로 화살표가 갑니다. 칸 안에는 초록 상자 get_agent 두 번 받아도 같은 그래프, require_token 요청 머리의 접근 토큰 검사, get_timeout 내놓는 값 2.0이 위아래로 놓여 있습니다. 칸에서 초록 상자 처리 함수 chat 몸통 2.0초 안에서 그래프를 부름을 지나 노란 상자 접근 토큰 있음 200 answer thread_id로 이어지고, 칸에서 점선이 노란 상자 접근 토큰 없음 401로 가는 그림"
FIG3_CAP = "실습 앱의 처리 함수 chat은 제공 함수 셋의 값을 받았고, 접근 토큰이 없으면 401, 있으면 200으로 답했습니다."
FIG3_READ = """위에서 아래로 읽습니다.
초록 상자는 보낸 요청과 실습 앱 파일의 함수이고, 칸 안의 셋이 처리 함수 chat의 의존성입니다.
노란 상자 둘은 노트북 3절 출력의 상태 코드입니다.
점선 갈래는 접근 토큰이 없을 때 require_token이 401로 답한 자리입니다."""

FIG4 = "02-4-남은-재정의와-비운-재정의"
FIG4_ALT = "위에 파란 상자 첫 테스트가 적은 재정의 get_timeout 대신 zero_timeout 내놓는 초 0.0이 있고, 노란 상자 첫 테스트의 질문 상태 코드 504로 화살표가 갑니다. 그 아래 칸 둘이 나란히 놓여 있습니다. 왼쪽 칸 Before 재정의를 남긴 채에는 파란 상자 다음 테스트 새 시험용 클라이언트로 보냄에서 빨간 상자 다음 질문 상태 코드 504 딕셔너리 키 수 1로 이어집니다. 오른쪽 칸 After 딕셔너리를 비움에는 파란 상자 첫 테스트 끝에서 dependency_overrides.clear()에서 노란 상자 딕셔너리 키 수 0 다음 질문 상태 코드 200으로 이어지는 그림"
FIG4_CAP = "첫 테스트가 남긴 재정의 때문에 다음 테스트도 504를 받았고, 재정의 딕셔너리를 비우자 같은 질문이 200을 받았습니다."
FIG4_READ = """맨 위 파란 상자와 노란 상자는 두 판이 함께 쓰는 첫 테스트이고, 노트북에서는 한 번 실행했습니다.
왼쪽 칸이 Before, 오른쪽 칸이 After이고, 칸 안은 위에서 아래로 우리가 쓴 줄과 받은 결과입니다.
빨간 상자 하나가 Before 결함 결과이고, 노란 상자는 노트북 4절·5절 출력입니다.
첫 테스트의 504는 재정의가 뜻한 대로 쓰인 결과라 노랑입니다."""

FIG5 = "02-5-2초-재정의가-남은-다음-테스트"
FIG5_ALT = "위에서 아래로 읽는 그림입니다. 파란 상자 바꾼 값 재정의 함수 two_second_timeout 내놓는 초 2.0에서 다음 테스트의 출력이라는 칸으로 화살표가 갑니다. 칸 안에는 노란 상자 상태 코드 200 재정의가 없을 때와 같음과 노란 상자 딕셔너리 키 수 1이 위아래로 놓여 있습니다. 칸에서 점선이 회색 상자 상태 코드로는 남은 재정의가 보이지 않음으로 가는 그림"
FIG5_CAP = "원래와 같은 2초를 내놓는 재정의를 남기자, 상태 코드는 200이었지만 재정의 딕셔너리의 키는 하나 남아 있었습니다."
FIG5_READ = """위에서 아래로 읽습니다.
파란 상자는 6절에서 바꾼 값이고, 칸 안 노란 상자 둘은 같은 요청의 출력입니다.
점선 끝 회색 상자는 두 출력을 함께 읽은 사실입니다.
값 바꿔 보기 장면이라 빨강은 쓰지 않았습니다."""

ILLU = "02-6-주황-기관차를-단-두-열차"
ILLU_ALT = "흰 바탕에 곧은 선로 세 줄이 위아래로 놓여 있습니다. 맨 위의 짧은 선로에는 큰 파란 기관차 하나가 짐칸 없이 홀로 서 있고, 선로 오른쪽 끝에 멈춤 막이가 있습니다. 가운데 선로와 아래 선로에는 똑같은 열차가 하나씩 있어, 초록 짐칸 둘의 오른쪽 앞에 작은 주황 기관차 하나가 붙어 있습니다. 사람·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "주황 기관차로 바꾼 약속이 남아 두 열차가 모두 주황 기관차를 달았고, 파란 기관차는 위쪽 짧은 선로에 홀로 서 있습니다."
# 2차 job d90885eb-7e9f-4f36-8a63-0ce5e08e3c36 채택(1차 1a81d545… 탈락 — 아래 열차에 짐칸 셋·주황 기관차 둘, 기관차 모두 넷) — 저장 PNG를 열어 센 개수로 적음
ILLU_READ = "흰 바탕에 선로 세 줄이 위아래로 있습니다. 가운데와 아래 선로의 두 열차는 똑같이 초록 짐칸 둘을 달았고, 맨 앞에 작은 주황 기관차가 하나씩 붙어 있습니다. 맨 위 짧은 선로에는 큰 파란 기관차 하나가 짐칸 없이 홀로 서 있습니다. 두 열차가 첫 테스트와 다음 테스트, 짐칸이 처리 함수, 주황 기관차가 바꿔 낀 함수가 요청마다 내놓은 값입니다. 파란 기관차는 쓰이지 않은 원래 제공 함수이고, 기관차의 크기는 어떤 값과도 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 처리 함수의 매개변수에 의존성을 적어, 라이브러리가 요청마다 값을 넘겨 주게 합니다.
2. 실습 앱을 가져와, 처리 함수 `chat`이 받는 의존성 셋과 접근 토큰 검사를 봅니다.
3. 시간 제한을 재정의한 채 두면 다음 테스트도 504를 받는 것을 보고, 재정의를 비워 고칩니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.
실습 앱의 에이전트 그래프는 모델을 쓰지 않고, 정해 둔 말로 답합니다.
그래서 다시 실행해도 같은 값이 나와야 합니다.

요청은 같은 노트북 안에서 앱 객체로 바로 들어갑니다.
서버 프로그램을 따로 띄우지 않고, 네트워크와 포트를 쓰지 않습니다.
실습 폴더의 앱 파일을 가져오고 읽기만 하며, 쓰는 파일은 없습니다.

걸린 시간은 재지 않았습니다.
이 절은 앞 챕터에서 배운 함수를 쓰지 않아, 가져오는 도구 파일도 없습니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 fastapi 0.135.0, httpx 0.28.1, pydantic 2.12.5, starlette 1.6.0입니다.
패키지 langgraph 1.2.11과 langchain 1.4.0은 실습 앱 파일이 가져오는 패키지입니다.
여섯 모두 실습 폴더 잠금과 같은 판입니다.

교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~5절을 읽습니다.
의존성과 재정의를 보고, 남은 재정의가 다음 테스트를 바꾸는 자리를 Before·After로 봅니다.
6절은 넣는 값 하나를 바꿔 보는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part7/ch30-fastapi-serving`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01절에서는 앱 객체와 처리 함수를 노트북에서 만들었습니다.
이 절은 처리 함수가 쓸 값을 라이브러리가 넘겨 주게 하는 방법을 봅니다.
제목의 주입은 FastAPI 문서의 말 injection을 옮긴 말로, 그렇게 값을 넘겨 주는 일을 가리킵니다.
이 교재 본문에서는 「처리 함수에 값을 넘겨 주기」라고 부릅니다.
제목의 Agent는 실습 앱의 에이전트 그래프입니다.

첫 셀은 패키지 여섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `fastapi: 0.135.0`과 `langgraph: 1.2.11`이 보입니다.
여섯 모두 실습 폴더 잠금과 같은 판입니다.
패키지 fastapi·httpx·pydantic·starlette는 01절에서 쓴 넷입니다.
패키지 langgraph와 langchain은 3절에서 가져올 실습 앱 파일이 가져옵니다.
이 절은 모델 객체를 만들지 않습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
표시 `Annotated`는 Ch 13 02절에서 리듀서를 적을 때 쓴 이름입니다.
함수 `Depends`는 패키지 fastapi에서 가져오고, 2절에서 뜻을 풉니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `가져온 fastapi 이름: Depends, FastAPI, TestClient`가 보입니다.
이 노트북에는 API 키를 확인하는 셀이 없습니다.
모델을 부르지 않기 때문입니다.

## 2. 의존성으로 처리 함수에 값 넘기기

처리 함수가 쓸 값을 몸통에서 만들지 않고, 라이브러리가 요청마다 넘겨 주게 할 수 있습니다.
패키지 fastapi는 이런 약속을 의존성(dependency)이라고 부릅니다.
도서관에 책을 신청해 두면, 자리에 앉을 때마다 사서가 그 책을 책상에 놓아 주는 것과 같습니다.
이 절에서는 매개변수 힌트에 `Depends(get_limit)`를 적어, 함수 `get_limit`이 내놓는 값을 받습니다.
먼저 연습용 앱 객체와, 기록을 적을 빈 목록을 만듭니다."""),
        code(DEMO_APP),
        md("""**결과 읽기** — 출력 줄 `앱 이름: 연습 앱`이 보입니다.
목록 `provider_calls`에는 아래 함수가 불릴 때마다 함수 이름을 적습니다.
01절에서 몸통에 들어온 값을 목록 `body_inputs`에 적은 방법과 같습니다.

다음 셀은 처리 함수에 넘길 값을 만들어 내놓는 함수를 정의합니다.
이 챕터에서는 이런 함수를 제공 함수라고 부릅니다.
값은 시간 제한 2.0초이고, 불릴 때마다 목록에 이름을 적습니다."""),
        code(DEF_LIMIT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
정의 줄이 `async def`인 비동기 함수이고, 01절의 처리 함수처럼 라이브러리가 await로 부릅니다.

다음 셀은 처리 함수의 매개변수 힌트에 쓸 이름 `LimitDep`을 만듭니다.
표시 `Annotated`의 첫 자리는 자료형 `float`, 둘째 자리는 `Depends(get_limit)`입니다.
Ch 13 02절에서는 둘째 자리에 합칠 함수를 적었고, 여기서는 값을 줄 함수를 적습니다.
함수 `Depends`에는 `get_limit`을 부르지 않고, 괄호 없이 함수 자체를 넘깁니다."""),
        code(LIMIT_DEP),
        md("""**결과 읽기** — 이름을 만드는 셀이라 출력이 없습니다.
FastAPI 문서는 이렇게 표시를 이름에 담아, 여러 처리 함수에서 함께 쓰는 모양을 보여 줍니다.
실습 앱 파일도 같은 모양으로 적혀 있고, 3절에서 그 줄을 봅니다.

다음 셀은 GET `/limit`에 처리 함수를 잇습니다.
매개변수 `limit`의 힌트가 `LimitDep`입니다.
라이브러리는 요청이 오면 `get_limit`을 불러, 내놓은 값을 `limit`에 넣고 처리 함수를 부릅니다."""),
        code(DEF_SHOW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
처리 함수 몸통에는 `get_limit`을 부르는 줄이 없습니다.
값을 만드는 일은 제공 함수가, 제공 함수를 부르는 일은 라이브러리가 맡습니다.

다음 셀은 시험용 클라이언트로 같은 요청을 두 번 넣습니다.
실행 전에 예상해 봅니다.
요청 두 번에 제공 함수는 몇 번 불릴까요?"""),
        code(CALL_TWICE),
        md("""**결과 읽기** — 출력 줄 `첫 응답: 200 {'limit': 2.0}`과 `둘째 응답: 200 {'limit': 2.0}`이 보입니다.
기록은 `['get_limit', 'get_limit']`이고, 요청 한 번에 제공 함수가 한 번씩 불렸습니다.
처리 함수는 제공 함수가 내놓은 값을 매개변수로 받아 그대로 내놓았습니다.

이제 시험 때 제공 함수를 다른 함수로 바꿔 끼워 봅니다.
다음 셀은 바꿔 낄 함수로, 시간 제한 0.5초를 내놓는 함수를 정의합니다."""),
        code(DEF_SHORT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 함수는 목록에 아무것도 적지 않습니다.

앱 객체에는 재정의 딕셔너리 `dependency_overrides`가 있습니다.
원래 제공 함수를 키로, 바꿔 낄 함수를 값으로 적으면 라이브러리가 값 쪽 함수를 부릅니다.
이렇게 제공 함수를 바꿔 끼우는 일을 이 챕터에서는 재정의(override)라고 부릅니다.
다음 셀은 연습 앱에 재정의를 적고, 기록을 비운 뒤 같은 요청을 넣습니다."""),
        code(OVERRIDE_DEMO),
        md("""**결과 읽기** — 출력 줄 `응답: 200 {'limit': 0.5}`와 `제공 함수가 불린 기록: []`이 보입니다.
처리 함수는 그대로인데, 바꿔 낀 함수가 내놓은 값을 받았습니다.
원래 제공 함수 `get_limit`은 한 번도 불리지 않았습니다.

출력 줄 `재정의 딕셔너리의 키 수: 1`도 봅니다.
재정의는 앱 객체의 딕셔너리에 적힌 값이라, 이 셀이 끝난 뒤에도 남아 있습니다.
남은 재정의가 무엇을 일으키는지는 4절에서 실습 앱으로 봅니다.

## 3. 실습 앱 가져오기

이 챕터의 앱은 실습 폴더 맨 위의 폴더 `agent_service/`에 있습니다.
다음 셀은 01절 2절과 같은 파일 위치 셀로, 후보 셋 가운데 실습 폴더를 고릅니다."""),
        code(FIND_LAB),
        md("""**결과 읽기** — 출력 줄 `실습 폴더를 찾았는가: True`가 보입니다.
고른 후보는 연 자리마다 달라서 출력하지 않습니다.

01절은 형식 파일 하나만 실행해 읽었습니다.
앱 파일 `app.py`는 같은 폴더의 다른 파일에서 이름을 가져오므로, 그렇게 읽을 수 없습니다.
그래서 다음 셀은 작업 폴더를 실습 폴더로 옮긴 뒤, 폴더 `agent_service`에서 이름을 가져옵니다.
함수 `os.chdir`는 작업 폴더를 옮기는 함수입니다.
가져오는 이름은 앱 객체 `app`과 제공 함수 `get_agent`·`get_timeout`입니다."""),
        code(IMPORT_APP),
        md("""**결과 읽기** — 출력 줄 `가져온 앱 이름: 교육용 Agent API`와 `재정의 딕셔너리의 키 수: 0`이 보입니다.
실습 앱 파일이 만든 앱 객체이고, 아직 재정의가 하나도 없습니다.

다음 셀은 앱 파일을 글로 읽어, 의존성을 적은 줄만 출력합니다.
처리 함수 `chat`의 정의 줄도 함께 출력합니다.
문장 `with open(...)`은 Ch 2 05절에서 파일을 열 때 쓴 모양입니다."""),
        code(READ_DEPENDS),
        md("""**결과 읽기** — 라벨 줄 아래에 `TimeoutDep = Annotated[float, Depends(get_timeout)]`처럼 이름을 만드는 줄 다섯이 있습니다.
2절의 `LimitDep`과 같은 모양입니다.
마지막 줄은 처리 함수 `chat`의 정의 줄이고, 매개변수 넷을 받습니다.

매개변수 `body`는 01절의 입력 형식이고, 나머지 셋은 의존성입니다.
매개변수 `runtime`에는 `get_agent`가 내놓는 에이전트 그래프가 들어옵니다.
매개변수 `_token`에는 `require_token`이 요청 머리를 검사한 값이 들어옵니다.
매개변수 `timeout`에는 `get_timeout`이 내놓는 초가 들어옵니다.
이름 `LiveAgentDep`·`ResumeIndexDep`은 이 절에서 쓰지 않는 처리 함수의 의존성입니다.

정의 줄 끝의 `-> ChatResponse`는 Ch 2 07절에서 본 내놓는 값 힌트입니다.
응답의 모양은 01절처럼 데코레이터 줄의 `response_model`이 정합니다.
다음 셀은 제공 함수 둘을 직접 불러, 내놓는 값을 봅니다.
제공 함수도 평범한 비동기 함수라, await로 부르면 값을 받습니다.
Ch 28 01절처럼, 셀 맨 위에 await 줄을 바로 쓰는 것은 노트북 도구(IPython)의 기능입니다."""),
        code(PROVIDER_VALUES),
        md("""**결과 읽기** — 출력 줄 `get_timeout이 내놓은 초: 2.0`과 `두 번 받은 그래프가 같은 객체인가: True`가 보입니다.
앱은 에이전트 그래프를 파일을 가져올 때 한 번 만들고, 요청마다 같은 객체를 넘깁니다.
이 그래프를 닫는 줄은 없어서, 앱을 가져온 프로그램이 끝날 때까지 같은 객체가 쓰입니다.
Ch 23 03절에서 배운 객체의 수명을 이 앱에서 본 것입니다.
그래프를 만드는 데 걸린 시간은 재지 않았습니다.

이 앱의 에이전트 그래프는 모델을 쓰지 않습니다.
질문 앞에 정해 둔 말을 붙여 답하는 그래프이고, 실습 폴더 `agent_service/agent.py`에 있습니다.
모델을 부르는 에이전트는 09절에서 씁니다.

다음 셀은 실습 앱에 시험용 클라이언트를 붙여, 접근 토큰 없이 질문을 보냅니다."""),
        code(NO_TOKEN),
        md("""**결과 읽기** — 출력 줄 `상태 코드: 401`과 `응답 본문: {'detail': '인증 정보가 올바르지 않습니다'}`가 보입니다.
의존성 `require_token`이 요청 머리에서 접근 토큰을 찾지 못해 401로 답했습니다.
접근 토큰은 Ch 28 03절에서 본 말이고, 이 앱의 검사는 07절에서 자세히 봅니다.

다음 셀은 요청 머리의 칸 `Authorization`에 접근 토큰을 적어 다시 보냅니다.
요청 머리는 01절의 응답 머리처럼, 본문과 따로 가는 이름과 값의 목록입니다.
값 `Bearer local-demo-token`은 실습 앱이 받는 교재용 접근 토큰입니다."""),
        code(WITH_TOKEN),
        md("""**결과 읽기** — 출력 줄 `상태 코드: 200`이 보입니다.
응답 본문은 `{'answer': '질문을 확인했습니다: 휴관일을 알려 주세요', 'thread_id': 'dep-01'}`입니다.
세 의존성의 값을 받은 처리 함수 `chat`이 에이전트 그래프를 불러 답했습니다.
그래프를 부르는 줄은 03절에서 자세히 봅니다."""),
        md("""## 4. 재정의를 남긴 채 다음 테스트 (Before)

이제 테스트 두 개가 차례로 이 앱에 요청하는 장면을 만듭니다.
첫 테스트는 시간 제한을 0초로 재정의해, 504 응답을 확인하려는 테스트입니다.
다음 테스트는 보통 질문에 200이 오는지 보려는 테스트입니다.
Before에서는 첫 테스트가 적은 재정의를 지우지 않습니다.
다음 셀은 시간 제한 0초를 내놓는 함수를 정의합니다.""", lesson_part="before"),
        code(DEF_ZERO, lesson_part="before"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이름 있는 비동기 함수 하나이고, 늘 0.0을 내놓습니다.

다음 셀은 첫 테스트의 첫 줄로, 재정의 딕셔너리에 `get_timeout` 대신 이 함수를 적습니다.
재정의할 함수를 await로 한 번 불러, 내놓는 값도 출력합니다.""", lesson_part="before"),
        code(REGISTER, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `재정의: get_timeout → zero_timeout`과 `재정의 딕셔너리의 키 수: 1`이 보입니다.
재정의할 함수가 내놓는 초는 `0.0`입니다.
딕셔너리의 키와 값은 함수 객체라서, 속성 `__name__`으로 이름을 꺼내 출력했습니다.

앱 파일 78~80행의 몸통은 함수 `asyncio.wait_for`로 그래프 실행에 시간 제한을 겁니다.
이 함수는 코루틴을 기다리다가, 정한 초 안에 끝나지 않으면 멈추고 오류 `TimeoutError`를 일으킵니다.
몸통은 이 오류를 Ch 16 05절처럼 `except TimeoutError`로 받아, 상태 코드 504로 답합니다.
상태 코드 504는 기다리던 쪽이 정한 시간 안에 답을 받지 못했다는 뜻입니다.
다음 셀은 첫 테스트의 질문을 보냅니다.""", lesson_part="before"),
        code(FIRST_Q, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `상태 코드: 504`와 `응답 본문: {'detail': 'Agent 응답 시간이 초과되었습니다'}`가 보입니다.
재정의한 0초 시간 제한이 처리 함수에 들어가, 첫 테스트가 바란 504가 나왔습니다.
이 504는 첫 테스트가 일부러 만든 결과입니다.

첫 테스트는 여기서 끝납니다.
다음 셀은 다음 테스트로, 새 시험용 클라이언트를 만들어 다른 질문을 보냅니다.
재정의는 지우지 않았습니다.
실행 전에 예상해 봅니다.
새 클라이언트로 보낸 보통 질문은 200을 받을까요?""", lesson_part="before"),
        code(NEXT_Q, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `상태 코드: 504`와 `재정의 딕셔너리의 키 수: 1`이 보입니다.
다음 테스트는 보통 질문을 보냈는데도, 첫 테스트와 같은 504를 받았습니다.
재정의는 클라이언트가 아니라 앱 객체의 딕셔너리에 남아 있어서, 새 클라이언트로 보내도 같았습니다.
이것이 이 절의 Before 결함입니다.

Ch 2 11절의 테스트 격리가 깨진 장면입니다.
테스트 격리는 테스트마다 따로 준비한 값으로 실행해, 다른 테스트가 남긴 값이 끼어들지 않게 하는 일입니다.
다음 테스트의 결과를 그 테스트의 코드가 아니라, 앞 테스트가 남긴 재정의가 정했습니다.""", lesson_part="before"),
        md("""## 5. 재정의 딕셔너리를 비우는 테스트 (After)

After에서는 첫 테스트가 끝날 때 재정의 딕셔너리를 비웁니다.
딕셔너리의 메서드 `clear`는 딕셔너리의 키와 값을 모두 지웁니다.
FastAPI 문서도 테스트 함수 끝에서 재정의를 비우라고 적습니다.""", lesson_part="after"),
        code(CLEAR, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `재정의 딕셔너리의 키 수: 0`이 보입니다.
앱 객체에 남은 재정의가 없어졌습니다.

다음 셀은 다음 테스트의 질문을 같은 클라이언트로 다시 보냅니다.
이번에는 200을 받을까요?""", lesson_part="after"),
        code(NEXT_AGAIN, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `상태 코드: 200`이 보입니다.
응답 본문은 `{'answer': '질문을 확인했습니다: 대출 기간을 알려 주세요', 'thread_id': 'test-02'}`입니다.
재정의가 없어지자, 원래 제공 함수 `get_timeout`이 내놓는 2.0초가 다시 쓰였습니다.
다음 테스트의 결과를 다시 그 테스트의 질문이 정합니다.

## 6. 값 바꿔 보기: 재정의 함수가 내놓는 초

값 하나만 바꿔 봅니다.
바꿀 것은 재정의 딕셔너리에 값으로 적는 함수입니다.
0초 대신, 원래 제공 함수와 같은 2초를 내놓는 함수를 적습니다.
다음 셀은 그 함수를 정의합니다.""", lesson_part="after"),
        code(DEF_TWO, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 재정의를 다시 적고, 다음 테스트의 질문을 보냅니다.
이번에는 셀이 끝나도 재정의를 지우지 않습니다.
실행 전에 예상해 봅니다.
상태 코드만 보고, 재정의가 남아 있는 것을 알아챌 수 있을까요?""", lesson_part="after"),
        code(VARY, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `상태 코드: 200`과 `재정의 딕셔너리의 키 수: 1`이 보입니다.
재정의할 함수가 내놓는 초는 `2.0`으로, 원래 제공 함수와 같습니다.
그래서 응답은 재정의가 없을 때와 같은 200이었지만, 재정의는 딕셔너리에 남아 있습니다.

남은 재정의는 결과가 같을 때 상태 코드로 드러나지 않습니다.
그래서 테스트가 끝날 때 재정의 딕셔너리를 비우고, 키 수로 확인합니다.
다음 셀은 노트북을 마치기 전에 두 앱의 재정의 딕셔너리를 비웁니다.""", lesson_part="after"),
        code(CLEANUP, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `실습 앱의 키 수: 0`과 `연습 앱의 키 수: 0`이 보입니다.
두 앱 모두 재정의가 남지 않았습니다.

## 정리

1. 매개변수 힌트에 의존성을 적자, 라이브러리가 요청마다 제공 함수를 불러 값을 넘겼습니다.
2. 재정의 딕셔너리에 바꿔 낄 함수를 적자, 처리 함수는 그대로인 채 받는 값이 바뀌었습니다.
3. 첫 테스트가 남긴 재정의로 다음 테스트도 504를 받았고, 딕셔너리를 비우자 200이 왔습니다.

03절에서는 처리 함수 몸통이 에이전트 그래프를 부르는 줄을 봅니다.
비동기 그래프를 await로 기다려 부르는 방법입니다.""", lesson_part="after"),
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
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(01절 생성기와 같은 함수)."""
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
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH02_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH02_07 = "../../part1/ch02-python/07-모듈과-타입힌트.html"
L_CH02_11 = "../../part1/ch02-python/11-패키징과-테스트-격리.html"
L_CH02_12 = "../../part1/ch02-python/12-async와-await.html"
L_CH13_02 = "../../part4/ch13-langgraph-basics/02-State-갱신.html"
L_CH16_05 = "../../part4/ch16-guardrails/05-재시도-폴백과-감사-로그.html"
L_CH23_03 = "../../part6/ch23-persistence/03-스레드-재개와-대화-이어가기.html"
L_CH28_01 = "../../part6/ch28-mcp/01-MCP-구조와-capability-협상.html"
L_CH28_03 = "../../part6/ch28-mcp/03-stdio와-원격-전송-권한-경계.html"
L_01 = "01-비동기-라우팅과-스키마.html"
L_03 = "03-ainvoke-요청-응답.html"

TERM_ROWS = [
    ("의존성(dependency)", "처리 함수가 쓸 값을 라이브러리가 요청마다 만들어 넘겨 주도록 적어 둔 약속입니다. 도서관에 책을 신청해 두면, 자리에 앉을 때마다 사서가 그 책을 책상에 놓아 주는 것과 같습니다. 이 절에서는 <code>LimitDep = Annotated[float, Depends(get_limit)]</code>로 적고, 매개변수 힌트 <code>limit: LimitDep</code>에 씁니다."),
    ("제공 함수", "의존성에 적어, 처리 함수에 넘길 값을 만들어 내놓는 함수입니다. 신청한 책을 서고에서 꺼내 오는 사서의 일과 같습니다. 이 절에서는 연습 앱의 <code>get_limit</code>과 실습 앱의 <code>get_agent</code>·<code>get_timeout</code>·<code>require_token</code>입니다."),
    ("재정의(override) · 재정의 딕셔너리", "제공 함수를 다른 함수로 바꿔 끼우는 일입니다. 앱 객체의 딕셔너리 <code>dependency_overrides</code>에 원래 함수를 키로, 바꿔 낄 함수를 값으로 적습니다. 시험 날에만 다른 책을 놓아 달라고 신청서를 고쳐 두는 것과 같습니다. 이 절에서는 <code>get_timeout</code> 대신 <code>zero_timeout</code>을 적어 시간 제한을 0초로 바꿉니다."),
    ("상태 코드 504", "기다리던 쪽이 정한 시간 안에 답을 받지 못했다는 뜻의 상태 코드입니다. 택시가 약속 시간까지 오지 않아 예약이 취소된 것과 같습니다. 이 절에서는 실습 앱의 처리 함수가 시간 제한을 넘기면 이 값으로 답합니다."),
]

COMPARE_ROWS = [
    ("첫 테스트가 끝날 때", "재정의를 그대로 둠", "<code>app.dependency_overrides.clear()</code>"),
    ("첫 테스트 질문의 상태 코드", "<code>504</code>", "Before와 함께 쓰는 첫 테스트(한 번 실행)"),
    ("다음 테스트 전 재정의 딕셔너리의 키 수", "<code>1</code>", "<code>0</code>"),
    ("다음 테스트의 시험용 클라이언트", "새로 만든 <code>next_client</code>", "같음"),
    ("다음 테스트 질문의 상태 코드", "<code>504</code>", "<code>200</code>"),
    ("다음 테스트의 응답 본문", "칸 <code>detail</code> 하나", "칸 <code>answer</code>·<code>thread_id</code>"),
]

LOOK_B5 = "노트북 2절에서 <code>제공 함수가 불린 기록: ['get_limit', 'get_limit']</code>을 봅니다. 재정의를 적은 뒤 <code>응답: 200 {'limit': 0.5}</code>와 <code>제공 함수가 불린 기록: []</code>을 확인합니다. 3절에서 <code>두 번 받은 그래프가 같은 객체인가: True</code>와, 접근 토큰이 없을 때의 <code>상태 코드: 401</code>도 찾습니다."
LOOK_B6 = "Before 마지막 셀에서 <code>상태 코드: 504</code>와 <code>재정의 딕셔너리의 키 수: 1</code>을 봅니다. After에서 비운 뒤 <code>재정의 딕셔너리의 키 수: 0</code>과 <code>상태 코드: 200</code>을 확인합니다. 6절에서는 상태 코드가 200인데 키 수가 1인지 봅니다."


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    compare = table_html(["견준 것", "Before(재정의를 남김)", "After(딕셔너리를 비움)"], COMPARE_ROWS)
    return """<!--meta: 강의 1h | 실습 2.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>처리 함수의 매개변수에 의존성을 적어, 라이브러리가 요청마다 제공 함수의 값을 넘기게 할 수 있습니다.</li>
<li>재정의 딕셔너리로 제공 함수를 바꿔 끼우고, 원래 함수가 불리지 않는 것을 출력으로 확인할 수 있습니다.</li>
<li>남은 재정의가 다음 테스트를 504로 바꾸는 것을 보고, 재정의 딕셔너리를 비워 고칠 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a>의 처리 함수는 몸통에서 함수 <code>make_result</code>를 바로 불렀습니다. 실습 앱의 처리 함수는 에이전트 그래프·시간 제한 값·접근 토큰 검사처럼 여러 값을 씁니다. 이 값을 몸통에서 직접 만들면, 시험 때 다른 값으로 바꾸기 어렵습니다. 그래서 이 절은 처리 함수가 쓸 값을 라이브러리가 요청마다 넘겨 주게 합니다.</p><p>제목의 주입은 FastAPI 문서의 말 injection을 옮긴 말이고, 본문에서는 「넘겨 주기」라고 부릅니다. 제목의 Agent는 실습 앱의 에이전트 그래프입니다. 넘겨 줄 값은 시험 때 다른 함수로 바꿔 낄 수 있습니다. 그런데 바꿔 낀 것을 지우지 않으면, 다음 테스트의 결과까지 바뀝니다. 이 절의 Before가 그 장면입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 앱 객체에 요청 방식·요청 주소와 처리 함수를 잇고, 시험용 클라이언트로 요청을 넣었습니다. 처리 함수의 매개변수 힌트에 입력 형식을 적어, 빈 질문을 몸통 전에 422로 멈추게 했습니다. 이 절은 같은 매개변수 힌트 자리에 의존성을 적습니다. 실습 폴더의 앱 파일은 이 절에서 처음 가져옵니다.</p><p><a href=\"""" + L_CH13_02 + """\">Ch 13 02절</a>의 표시 <code>Annotated</code>는 자료형 옆에 함께 쓸 정보를 적어 두는 표시였습니다. 그 절에서는 둘째 자리에 합칠 함수를 적었고, 이 절에서는 값을 줄 함수를 적습니다. <a href=\"""" + L_CH02_12 + """\">Ch 2 12절</a>의 await와, <a href=\"""" + L_CH28_01 + """\">Ch 28 01절</a>에서 쓴 셀 맨 위 await 줄도 씁니다. <a href=\"""" + L_CH16_05 + """\">Ch 16 05절</a>에서 받은 오류 <code>TimeoutError</code>는 이 절 실습 앱의 504 응답 뒤에 있습니다.</p><p><a href=\"""" + L_CH02_11 + """\">Ch 2 11절</a>에서는 목록 하나를 함께 쓴 두 테스트 가운데, 둘째 테스트가 앞 테스트의 노트를 받았습니다. 테스트마다 따로 준비한 값으로 실행하는 테스트 격리가 깨진 장면이었습니다. B 트랙의 절이라, A 트랙은 이 뜻을 여기서 처음 봐도 됩니다. 그 절 끝에서 예고한 대로, 이 절은 한 테스트가 남긴 재정의가 다음 질문까지 이어지는 실패를 다룹니다.</p><p><a href=\"""" + L_CH23_03 + """\">Ch 23 03절</a>에서는 객체의 수명을 배웠습니다. 객체를 만든 때부터, 닫혀서 더 쓸 수 없게 된 때까지입니다. 이 절은 실습 앱이 에이전트 그래프를 언제 만들고, 요청마다 어떤 객체를 넘기는지 봅니다. 접근 토큰은 <a href=\"""" + L_CH28_03 + """\">Ch 28 03절</a>의 말이고, 이 절에서는 요청을 보낼 때 한 번 적습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>화물역에서는 열차를 떠나보내기 전에 맨 앞에 기관차를 붙입니다. 평소에는 늘 쓰는 파란 기관차를 붙이기로 정해져 있습니다. 시험 운행 날에는 그 약속을 작은 주황 시험용 기관차로 바꿔 둡니다. 시험이 끝나도 바꾼 약속을 되돌리지 않으면, 다음 열차도 주황 기관차를 달고 떠납니다.</p><p>짐칸이 처리 함수이고, 앞에 붙는 기관차가 제공 함수가 내놓는 값입니다. 어느 기관차를 붙일지 정한 약속이 재정의 딕셔너리입니다. 파란 기관차는 원래 제공 함수, 주황 기관차는 시험용으로 바꿔 낀 함수입니다. 짐칸은 그대로인데, 약속 하나 때문에 다음 열차까지 달라집니다.</p><p>비유와 다른 점이 있습니다. 실제 앱에서는 기관차 한 대가 열차 둘을 끄는 것이 아닙니다. 요청마다 바꿔 낀 함수가 새로 불려 값을 내놓습니다.</p>
""" + illustration_block() + """<h3>의존성과 제공 함수</h3><p>처리 함수가 쓸 값을 몸통에서 만들지 않고, 라이브러리가 요청마다 넘겨 주게 할 수 있습니다. 패키지 fastapi는 이 약속을 의존성이라고 부릅니다. 의존성은 표시 <code>Annotated</code>의 둘째 자리에 함수 <code>Depends</code>로 적습니다. 함수 <code>Depends</code>에는 값을 줄 함수를 부르지 않고 넘깁니다.</p><p>요청이 오면 라이브러리가 그 함수를 불러, 내놓은 값을 매개변수에 넣고 처리 함수를 부릅니다. 설치판 fastapi 0.135.0 <code>dependencies/utils.py</code> 675~676행이 비동기 제공 함수를 await로 부르는 자리입니다. FastAPI 문서는 표시를 이름에 담아, 여러 처리 함수에서 함께 쓰는 모양을 보여 줍니다. 실습 앱 파일의 <code>TimeoutDep</code>도 같은 모양입니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 요청 두 번에 제공 함수의 기록이 <code>['get_limit', 'get_limit']</code>이 되었습니다. 재정의를 적자 응답이 <code>{'limit': 0.5}</code>로 바뀌었고, 기록은 <code>[]</code>였습니다. 시간 제한 0초를 재정의한 실습 앱은 <code>상태 코드: 504</code>로 답했습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>재정의 딕셔너리</h3><p>앱 객체의 속성 <code>dependency_overrides</code>는 평범한 딕셔너리입니다. 원래 제공 함수를 키로, 바꿔 낄 함수를 값으로 적습니다. 라이브러리는 요청이 올 때마다 이 딕셔너리에서 제공 함수를 찾고, 있으면 값 쪽 함수를 부릅니다. 설치판 <code>dependencies/utils.py</code> 629~643행이 그 자리입니다.</p><p>이 딕셔너리는 앱 객체의 속성이라, 적은 셀이 끝나도 지우기 전까지 남습니다. 새 시험용 클라이언트를 만들어도, 같은 앱 객체에 요청하면 재정의가 그대로 쓰입니다. FastAPI 문서는 테스트 함수 처음에 재정의를 적고, 끝에서 비우라고 적습니다.</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h3>실습 앱의 의존성과 객체의 수명</h3><p>실습 앱의 처리 함수 <code>chat</code>은 의존성 셋을 받습니다. 제공 함수 <code>get_agent</code>는 에이전트 그래프를, <code>get_timeout</code>은 시간 제한 2.0초를 내놓습니다. 제공 함수 <code>require_token</code>은 요청 머리의 접근 토큰을 검사하고, 맞지 않으면 401로 답합니다. 설치판 <code>routing.py</code> 452~462행은 의존성을 먼저 풀고, 그 뒤에 처리 함수 쪽으로 갑니다. 그래서 의존성이 401로 멈추면 처리 함수 몸통은 실행되지 않습니다.</p><p>제공 함수 <code>get_agent</code>는 요청마다 불리지만, 내놓는 그래프는 늘 같은 객체였습니다. 그래프 파일 <code>agent.py</code> 46행이 파일을 가져올 때 그래프를 한 번 만들기 때문입니다. 이 그래프를 닫는 줄은 없어서, 앱을 가져온 프로그램이 끝날 때까지 같은 객체가 쓰입니다. Ch 23 03절의 말로 하면, 이 그래프의 수명은 프로그램과 같습니다.</p><p>모델을 부르는 에이전트를 만드는 <code>live_agent.py</code>는 줄 <code>@lru_cache(maxsize=1)</code>로 처음 만든 에이전트를 기억해 둡니다. 첫 요청 때 한 번 만들고, 다음 요청부터는 같은 객체를 씁니다. 이 줄은 설치판 소스로만 보았고, 노트북에서는 실행하지 않았습니다. 이 앱에는 앱의 시작과 끝에 할 일을 적는 <code>lifespan</code> 설정이 없습니다. 그래프를 만드는 데 걸린 시간은 재지 않았습니다.</p><h3>시간 제한과 상태 코드 504</h3><p>처리 함수 <code>chat</code>의 몸통은 함수 <code>asyncio.wait_for</code>로 에이전트 그래프 실행에 시간 제한을 겁니다. 이 함수는 코루틴을 기다리다가, 정한 초 안에 끝나지 않으면 멈추고 오류 <code>TimeoutError</code>를 일으킵니다. 몸통은 이 오류를 받아 상태 코드 504로 답합니다. 앱 파일 76~83행이 이 자리입니다.</p><p>시간 제한이 0초이면 그래프는 끝날 틈이 없어, 처리 함수는 504로 답합니다. 설치판 Python 3.12.13 <code>asyncio/tasks.py</code> 507~517행은 시간 제한이 0 이하이면 작업을 기다리지 않고 취소합니다. 그래서 이 절의 504는 다시 실행해도 같게 나옵니다. 노트북 밖에서도 같은 장면을 다섯 번 실행해 모두 같았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 연습 앱에 의존성을 적고, 요청 두 번에 제공 함수가 몇 번 불리는지 봅니다. 이어서 재정의를 적고 같은 요청을 넣어, 받는 값과 불린 기록을 견줍니다. 3절은 실습 앱을 가져와, 의존성을 적은 줄과 처리 함수 <code>chat</code>의 정의 줄을 읽습니다. 제공 함수 둘을 직접 부르고, 접근 토큰 없이 한 번과 적어서 한 번 질문을 보냅니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 서버 프로그램을 띄우지 않아 네트워크·포트·자식 프로세스를 쓰지 않습니다. 실습 폴더의 앱 파일을 가져오고 읽기만 하며, 쓰는 파일은 없습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2><p>아래 Before 셀은 테스트 두 개가 차례로 실습 앱에 요청하는 장면입니다. 첫 테스트는 시간 제한을 0초로 재정의해 504를 확인하고, 재정의를 지우지 않은 채 끝납니다. 다음 테스트는 새 시험용 클라이언트로 보통 질문을 보냅니다. After 셀은 첫 테스트가 끝날 때 재정의 딕셔너리를 비우고, 같은 질문을 다시 보냅니다.</p>
{{notebook:""" + SLUG + """|failure}}
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + compare + """
<p>두 판의 테스트 코드는 같았고, 다른 것은 첫 테스트 끝의 줄 하나였습니다. 다음 테스트의 상태 코드를 가른 것은 재정의 딕셔너리에 남은 키 하나입니다.</p><p>Before에서 다음 테스트는 보통 질문을 보냈는데도 504를 받았습니다. 새 시험용 클라이언트를 만들었지만, 재정의는 앱 객체에 남아 있었습니다. 다음 테스트의 코드만 읽어서는 504의 까닭을 찾을 수 없습니다. Ch 2 11절에서 둘째 테스트가 앞 테스트의 노트를 받은 것과 같은 모양입니다.</p><p>After 판은 첫 테스트가 끝날 때 재정의 딕셔너리를 비웠습니다. 키 수가 0이 되자, 같은 질문이 원래 제공 함수의 2.0초 시간 제한 안에서 200을 받았습니다. 첫 테스트의 504는 두 판이 함께 쓰는 장면이고, 재정의가 뜻한 대로 쓰인 결과입니다.</p>
<p>노트북 6절에서 재정의 함수만 2초를 내놓는 함수로 바꾸자, 상태 코드는 200이었습니다. 그래도 재정의 딕셔너리의 키 수는 1이었습니다. 남은 재정의는 결과가 같을 때 상태 코드로 드러나지 않습니다. 그래서 테스트 끝에서 딕셔너리를 비우고, 키 수로 확인합니다.</p>
""" + mermaid_block(FIG5, FIG5_ALT, FIG5_CAP, FIG5_READ) + """<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>FastAPI 문서의 예는 재정의를 비울 때 딕셔너리를 <code>{}</code>로 새로 적습니다. 이 절은 딕셔너리의 메서드 <code>clear</code>로 비웠고, 문서의 방법은 실행하지 않았습니다. 재정의 하나만 지우는 메서드 <code>pop</code>도 이 절에서는 쓰지 않았습니다.</li><li>테스트를 pytest로 쓴다면, 비우는 줄을 테스트 함수 끝이나 Ch 2 11절의 픽스처에 둡니다. 테스트가 중간에 실패하면 함수 끝의 줄까지 가지 못합니다. 이 절에서는 pytest를 실행하지 않았습니다.</li><li>폴더 <code>agent_service</code>의 첫 파일 <code>__init__.py</code>는 앱 객체를 이름 <code>app</code>으로 내보냅니다. 그래서 가져올 때는 <code>from agent_service.app import …</code> 모양을 씁니다. 줄 <code>import agent_service.app</code> 뒤의 이름 <code>agent_service.app</code>은 파일이 아니라 앱 객체를 가리킵니다. 이 사실은 노트북 밖에서 확인했습니다.</li><li>시험용 클라이언트는 <code>with</code> 없이 만들었습니다. FastAPI 문서는 <code>lifespan</code>이 있는 앱이면 <code>with TestClient(app)</code>일 때만 시작과 끝의 할 일이 돈다고 적습니다. 이 앱에는 <code>lifespan</code>이 없고, 이 절에서 실행하지도 않았습니다.</li><li>접근 토큰 <code>local-demo-token</code>은 교재용 값입니다. 앱 파일 57행은 환경 변수 <code>DEMO_API_TOKEN</code>이 있으면 그 값을 씁니다. 인증은 07절에서 자세히 봅니다.</li><li>앱 파일에는 이 절이 풀지 않은 줄도 있습니다. 나머지 처리 함수 넷과 그 의존성은 뒤 절에서 봅니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>매개변수 힌트에 의존성을 적자, 라이브러리가 요청마다 제공 함수를 불러 값을 넘겼습니다.</li><li>재정의 딕셔너리에 바꿔 낄 함수를 적자, 처리 함수는 그대로인 채 받는 값이 바뀌었습니다.</li><li>첫 테스트가 남긴 재정의로 다음 테스트도 504를 받았고, 딕셔너리를 비우자 200이 왔습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_03 + """\">03절</a>에서는 처리 함수 몸통이 에이전트 그래프를 부르는 줄을 봅니다. 비동기 그래프를 await로 기다려 부르는 방법입니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 연습 앱에 같은 요청을 두 번 넣었을 때, 제공 함수가 불린 기록은 무엇이었나요?</p><p class="quiz-a">기록은 <code>['get_limit', 'get_limit']</code>이었습니다. 라이브러리가 요청 한 번에 제공 함수를 한 번씩 불렀습니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. 연습 앱에 재정의를 적은 뒤 받은 응답과 기록은 무엇이었나요? 처리 함수를 고쳤나요?</p><p class="quiz-a">응답은 <code>{'limit': 0.5}</code>, 기록은 빈 목록이었습니다. 처리 함수는 고치지 않았고, 원래 제공 함수는 한 번도 불리지 않았습니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">3. Before에서 다음 테스트는 새 시험용 클라이언트를 만들었는데도 504를 받았습니다. 까닭은 무엇인가요?</p><p class="quiz-a">재정의는 클라이언트가 아니라 앱 객체의 딕셔너리에 남아 있었기 때문입니다. 그때 재정의 딕셔너리의 키 수는 1이었습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 동료가 「다음 테스트가 200을 받았으니 재정의는 남아 있지 않다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 6절에서 2초를 내놓는 재정의를 남기자, 상태 코드는 200인데 키 수는 1이었습니다. 남은 재정의는 키 수로 확인합니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">5. 제공 함수 <code>get_agent</code>를 두 번 불러 받은 그래프가 같은 객체였던 까닭은 무엇인가요?</p><p class="quiz-a">그래프 파일이 가져올 때 그래프를 한 번 만들고, 제공 함수는 늘 그 객체를 내놓기 때문입니다. 그래프를 닫는 줄이 없어, 프로그램이 끝날 때까지 같은 객체가 쓰입니다. 틀렸다면 노트북 3절과 본문 4블록을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://fastapi.tiangolo.com/tutorial/dependencies/">FastAPI Dependencies</a></div>확인 2026-09-29 · 새 요청이 올 때마다 제공 함수를 불러, 결과를 처리 함수의 매개변수에 넣는다고 적습니다. 함수 <code>Depends</code>에는 함수를 부르지 않고 넘기며, 표시를 이름에 담아 함께 쓸 수 있다고 적습니다.</li><li><div><a href="https://fastapi.tiangolo.com/advanced/testing-dependencies/">FastAPI Testing Dependencies with Overrides</a></div>확인 2026-09-29 · 재정의 딕셔너리의 키는 원래 제공 함수, 값은 바꿔 낄 함수라고 적습니다. 일부 테스트에서만 쓰려면 테스트 함수 처음에 적고 끝에서 비우라고 적습니다.</li><li><div><a href="https://docs.python.org/3.12/library/asyncio-task.html">Python asyncio Coroutines and Tasks</a></div>확인 2026-09-29 · 함수 <code>wait_for</code>는 시간 제한이 지나면 작업을 취소하고 오류 <code>TimeoutError</code>를 일으킨다고 적습니다.</li><li>설치판 fastapi 0.135.0 소스 <code>applications.py</code> 969~984행은 앱 객체의 속성 <code>dependency_overrides</code>를 딕셔너리로 만듭니다. 같은 자리의 설명 글은 이 딕셔너리가 시험용이라고 적습니다. <code>dependencies/utils.py</code> 629~643행은 요청마다 이 딕셔너리에서 제공 함수를 찾고, 675~676행은 비동기 제공 함수를 await로 부릅니다.</li><li>Python 3.12.13 <code>asyncio/tasks.py</code> 507~517행은 시간 제한이 0 이하일 때 작업을 취소하고 <code>TimeoutError</code>를 일으킵니다. 실습 폴더 <code>agent.py</code> 46행은 그래프를 한 번 만들고, <code>live_agent.py</code> 15~16행은 <code>@lru_cache(maxsize=1)</code>를 씁니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 3절 파일 위치 셀은 01절 셀 글 그대로(「01절 2절과 같은 파일 위치 셀」 문장의 근거)
    assert FIND_LAB in AUTHOR01.read_text(encoding="utf-8"), "FIND_LAB이 01절 셀과 다릅니다"
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "02", SLUG, "paired", cells())
        print("wrote", path)
