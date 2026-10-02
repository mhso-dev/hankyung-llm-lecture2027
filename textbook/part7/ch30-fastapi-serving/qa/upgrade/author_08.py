"""Ch 30 08절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 experiment).

사용:
  python3 -B author_08.py            → 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_08.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**. 슬러그 그대로.

## 결정 1 — 응답 문서를 읽고, 파일은 쓰지 않는다 (handoff §07 → §08 1~3)

app.openapi() → 맨 위 칸 넷·OpenAPI 3.1.0·요청 주소 다섯·/v1/chat의 $ref·operationId·매개변수 authorization ·
components의 ChatRequest(= ChatRequest.model_json_schema(), Ch 19 02 방법) · SSE 요청 주소의 itemSchema ·
두 번째 부르기는 같은 객체(openapi_schema) · /openapi.json을 시험용 클라이언트로 받아도 같은 딕셔너리.
실습 폴더 openapi.json은 다시 쓰지 않고, json.dumps(…, ensure_ascii=False, indent=2) 글과 파일 글을 견주기만 한다
(True — 옛 판은 파일을 다시 썼음. 바이트가 같아 해시 06e5d1b9…도 그대로).

## 결정 2 — 생성 SDK는 파이썬으로 파일을 읽어 줄만 찾는다 (handoff §07 → §08 4)

openapitools.json(생성기 7.25.0) · DefaultApi.ts 머리 주석 · 함수 다섯의 내놓는 값(JSON 셋 / Promise<void> 둘) ·
VoidApiResponse·JSONApiResponse 줄 · 요청 인자 선언 넷의 authorization?: · models/ChatRequest.ts의 칸과 JSON 칸 이름 바꾸기 ·
글자 수 조건 줄 없음. .openapi-generator/는 학생 묶음에 없어 읽지 않는다. node·npx는 부르지 않는다
(생성·tsc는 노트북 밖 — 진단에 기록).

## 결정 3 — 실험: 인자 dependencies에 적은 것 하나만 바꿈 (handoff §07 → §08 5)

같은 처리 함수 health를 같은 요청 주소 GET /v1/ping으로 새 앱 객체 둘에 add_api_route —
실행 1 dependencies=[Depends(require_token)](실습 앱 방식) · 실행 2 dependencies=[Depends(bearer)](bearer = HTTPBearer()).
결론(매번 같은 값): securitySchemes False/True · security 칸 False/True · parameters 칸 True/False · 응답 코드 200·422 / 200 ·
상태 코드는 같음(401/401, 200/200). 옛 b6 「두 직렬화 결과가 같았다」는 성질 확인이라 2절 한 셀(같은 객체)로 낮춤.

## 도구 파일은 건드리지 않음

이 절은 앞 절 함수를 쓰지 않아 serve_tools.py를 가져오지 않는다(06 판 그대로인지 __main__에서 확인만).
이 절이 처음 쓰는 print_lines_with는 노트북에 둔다.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·`sorted`·노트북 딕셔너리 `.get`·`.items`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·
대입 풀기(for 포함)·별표 풀기·`while`·`try`·`raise`·세미콜론·`isinstance`·클래스·데코레이터·가짜 에이전트·`asyncio`·
셀 맨 위 await·자식 프로세스·포트·`node`·`npx`·파일 쓰기. 챕터 예외 없음(요청 주소 데코레이터 줄·async def도 0). 호출 깊이 2 이하.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402
import author_06  # noqa: E402

LAB = ROOT / "labs/part7/ch30-fastapi-serving/notebooks"
FIGS = ROOT / "textbook/part7/ch30-fastapi-serving/figures"
SLUG = "08-OpenAPI와-TS-SDK"
TITLE_TEXT = "OpenAPI와 TS SDK"
SRC = ROOT / "textbook/part7/ch30-fastapi-serving/_src" / (SLUG + ".html")
AUTHOR01 = ROOT / "textbook/part7/ch30-fastapi-serving/qa/upgrade/author_01.py"
TOOLS_PATH = LAB / "serve_tools.py"
RUNS_SENTENCE = os.environ.get("AUTHOR08_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 노트북 밖에서도 같은 장면을 파이썬 파일로 다섯 번 실행해, 출력이 모두 같았습니다. 모델을 부르지 않아, 응답 문서의 칸은 앱과 설치판 라이브러리의 코드가 정합니다.")

# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["fastapi==0.135.0", "httpx==0.28.1", "pydantic==2.12.5", "starlette==1.6.0",
                          "langgraph==1.2.11", "langchain==1.4.0"])

IMPORTS = r'''# 이 절에서 쓸 이름을 가져옵니다(os와 json은 Python에 들어 있는 모듈입니다)
import os
import json
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient

print("가져온 이름:", "json, Depends, FastAPI, HTTPBearer, TestClient")'''

# 01절 2절 셀 글 그대로(아래 __main__에서 author_01.py와 문자열 대조)
FIND_LAB = author_06.FIND_LAB

IMPORT_APP = r'''# 작업 폴더를 실습 폴더로 옮기고, 앱 객체·처리 함수·제공 함수·양식 클래스를 가져옵니다
os.chdir(lab_path)
from agent_service.app import app, health, require_token
from agent_service.schemas import ChatRequest
print("가져온 앱 객체의 종류:", type(app).__name__)
print("가져온 함수:", health.__name__, require_token.__name__)
print("응답 문서를 담아 둘 속성 openapi_schema:", app.openapi_schema)'''

DOC_TOP = r'''# 앱 객체의 메서드 openapi를 불러 응답 문서를 만들고, 맨 위 칸을 봅니다
openapi_doc = app.openapi()
print("받은 값의 종류:", type(openapi_doc).__name__)
print("맨 위 칸:", list(openapi_doc))
print("OpenAPI 판:", openapi_doc["openapi"])
print("칸 info:", openapi_doc["info"])'''

PATHS = r'''# 칸 paths에 적힌 요청 주소와, 요청 주소마다 받는 요청 방식을 한 줄씩 출력합니다
print("요청 주소 수:", len(openapi_doc["paths"]))
print("요청 주소 | 요청 방식")
for address in openapi_doc["paths"]:
    print(address, "|", list(openapi_doc["paths"][address]))'''

CHAT_OP = r'''# 요청 주소 /v1/chat의 POST 칸에서, 이름표와 요청 본문·응답의 형식이 적힌 자리를 꺼냅니다
chat_operation = openapi_doc["paths"]["/v1/chat"]["post"]
print("POST /v1/chat의 칸:", list(chat_operation))
print("operationId:", chat_operation["operationId"])
print("요청 본문 형식:", chat_operation["requestBody"]["content"]["application/json"]["schema"])
print("응답 코드:", list(chat_operation["responses"]))
print("200 응답 형식:", chat_operation["responses"]["200"]["content"]["application/json"]["schema"])
print("매개변수 이름과 자리:", chat_operation["parameters"][0]["name"], chat_operation["parameters"][0]["in"])'''

FORMATS = r'''# 칸 components에 모은 형식 이름과, 입력 형식 ChatRequest에 적힌 칸 조건을 봅니다
format_table = openapi_doc["components"]["schemas"]
print("형식 이름:", list(format_table))
print("ChatRequest의 꼭 채울 칸:", format_table["ChatRequest"]["required"])
print("칸 question:", format_table["ChatRequest"]["properties"]["question"])
print("칸 thread_id의 pattern:", format_table["ChatRequest"]["properties"]["thread_id"]["pattern"])
print("model_json_schema()로 만든 딕셔너리와 같은가:", ChatRequest.model_json_schema() == format_table["ChatRequest"])'''

STREAM_CONTENT = r'''# 요청 주소 /v1/chat과 /v1/chat/stream의 200 응답에서, 본문 종류와 그 아래 키를 견줍니다
chat_content = chat_operation["responses"]["200"]["content"]
stream_operation = openapi_doc["paths"]["/v1/chat/stream"]["post"]
stream_content = stream_operation["responses"]["200"]["content"]
print("/v1/chat:", list(chat_content), list(chat_content["application/json"]))
print("/v1/chat/stream:", list(stream_content), list(stream_content["text/event-stream"]))'''

CACHE = r'''# 메서드 openapi를 한 번 더 불러, 처음 받은 딕셔너리와 같은 객체인지 봅니다
second_doc = app.openapi()
print("두 번째로 받은 값이 같은 객체인가:", second_doc is openapi_doc)
print("속성 openapi_schema가 같은 객체인가:", app.openapi_schema is openapi_doc)'''

HTTP_DOC = r'''# 시험용 클라이언트로 요청 주소 /openapi.json에 GET을 보내, 받은 문서가 같은지 봅니다
client = TestClient(app)
doc_response = client.get("/openapi.json")
print("상태 코드:", doc_response.status_code)
print("본문 종류:", doc_response.headers["content-type"])
print("메서드 openapi가 내놓은 딕셔너리와 같은가:", doc_response.json() == openapi_doc)'''

FILE_COMPARE = r'''# 응답 문서를 openapi.json과 같은 설정의 JSON 글로 바꾸고, 파일 글과 견줍니다(파일은 읽기만 합니다)
openapi_text = json.dumps(openapi_doc, ensure_ascii=False, indent=2)
with open("openapi.json", encoding="utf-8") as doc_file:
    file_text = doc_file.read()
print("새로 만든 글의 글자 수:", len(openapi_text))
print("파일 글의 글자 수:", len(file_text))
print("두 글이 같은가:", openapi_text == file_text)
print("ensure_ascii를 뺀 글과 같은가:", json.dumps(openapi_doc, indent=2) == file_text)
print("파일 첫 세 줄:", file_text.splitlines()[:3])'''

DEF_LINES = r'''# 글 줄 목록에서 word가 든 줄을 찾아, 줄 번호와 앞뒤 공백을 뺀 줄을 한 줄씩 출력합니다
def print_lines_with(text_lines, word):
    print("줄 번호 | 줄")
    for index in range(len(text_lines)):
        if word in text_lines[index]:
            print(index + 1, "|", text_lines[index].strip())'''

SDK_HEAD = r'''# openapitools.json에서 생성기 판을 읽고, 생성 SDK 파일 DefaultApi.ts의 머리 주석에서 줄 셋을 찾습니다
with open("openapitools.json", encoding="utf-8") as tools_file:
    generator_config = json.load(tools_file)
print("생성기 판:", generator_config["generator-cli"]["version"])
with open("client/generated/apis/DefaultApi.ts", encoding="utf-8") as ts_file:
    ts_lines = ts_file.read().splitlines()
print_lines_with(ts_lines, "The version of the OpenAPI document")
print_lines_with(ts_lines, "auto generated")
print_lines_with(ts_lines, "Do not edit")'''

SDK_FUNCS = r'''# DefaultApi.ts에서 요청 주소마다 만든 함수의 이름과, 내놓는 값의 형식을 찾습니다
print("줄 번호 | 함수 이름 | 내놓는 값")
for index in range(len(ts_lines)):
    line = ts_lines[index]
    if line.startswith("    async ") and "Raw(" not in line and "RequestOpts(" not in line:
        signature = line.strip().rstrip(" {")
        name = signature.split("(")[0]
        returned = signature.split("): ")[-1]
        print(index + 1, "|", name, "|", returned)'''

SDK_WRAP = r'''# DefaultApi.ts에서 받은 응답을 감싸는 줄을 찾습니다 — 본문을 읽지 않는 쪽과 JSON으로 읽는 쪽
print_lines_with(ts_lines, "VoidApiResponse(response")
print_lines_with(ts_lines, "JSONApiResponse(response")'''

SDK_AUTH = r'''# 요청 인자의 칸을 적은 TS 선언과, 그 안의 칸 authorization이 적힌 줄을 찾습니다
print_lines_with(ts_lines, "export interface")
print_lines_with(ts_lines, "authorization?:")'''

SDK_MODEL = r'''# models/ChatRequest.ts에서 칸 이름의 줄, JSON 칸 이름으로 옮기는 줄, 글자 수 조건의 줄을 찾습니다
with open("client/generated/models/ChatRequest.ts", encoding="utf-8") as model_file:
    model_lines = model_file.read().splitlines()
print_lines_with(model_lines, ": string;")
print_lines_with(model_lines, "json['thread_id']")
print_lines_with(model_lines, "value['threadId']")
print_lines_with(model_lines, "Length")'''

RUN1 = r'''# 실행 1: 실습 앱의 제공 함수 require_token을 의존성으로 적어, 처리 함수 health를 새 앱 객체에 잇습니다
header_app = FastAPI()
header_app.add_api_route("/v1/ping", health, methods=["GET"], dependencies=[Depends(require_token)])
header_doc = header_app.openapi()
header_operation = header_doc["paths"]["/v1/ping"]["get"]
print("보안 방식 칸이 있는가:", "securitySchemes" in header_doc["components"])
print("요청 주소에 적힌 칸:", list(header_operation))
print("매개변수 이름과 자리:", header_operation["parameters"][0]["name"], header_operation["parameters"][0]["in"])
print("응답 코드:", list(header_operation["responses"]))'''

RUN2 = r'''# 실행 2: 값 하나만 바꿔, 의존성에 보안 객체를 적고 같은 처리 함수를 같은 요청 주소에 잇습니다
bearer = HTTPBearer()
bearer_app = FastAPI()
bearer_app.add_api_route("/v1/ping", health, methods=["GET"], dependencies=[Depends(bearer)])
bearer_doc = bearer_app.openapi()
bearer_operation = bearer_doc["paths"]["/v1/ping"]["get"]
print("보안 방식 칸이 있는가:", "securitySchemes" in bearer_doc["components"])
print("요청 주소에 적힌 칸:", list(bearer_operation))
print("보안 방식:", bearer_doc["components"]["securitySchemes"])
print("요청 주소의 security 칸:", bearer_operation["security"])
print("응답 코드:", list(bearer_operation["responses"]))'''

RUN_REQUESTS = r'''# 두 앱 객체에 머리 없는 요청과 교재용 접근 토큰을 실은 요청을 보내, 상태 코드를 봅니다
auth_headers = {"Authorization": "Bearer local-demo-token"}
header_client = TestClient(header_app)
bearer_client = TestClient(bearer_app)
header_plain = header_client.get("/v1/ping")
header_token = header_client.get("/v1/ping", headers=auth_headers)
bearer_plain = bearer_client.get("/v1/ping")
bearer_token = bearer_client.get("/v1/ping", headers=auth_headers)
print("실행 1:", header_plain.status_code, header_plain.json(), header_token.status_code)
print("실행 2:", bearer_plain.status_code, bearer_plain.json(), bearer_token.status_code)'''

RESULT_TABLE = r'''# 두 실행의 의존성·응답 문서의 칸·상태 코드를 한 표로 모읍니다
print("견준 것 | 실행 1 | 실행 2")
print("의존성에 적은 것 | require_token | HTTPBearer()")
print("보안 방식 칸 |", "securitySchemes" in header_doc["components"], "|", "securitySchemes" in bearer_doc["components"])
print("security 칸 |", "security" in header_operation, "|", "security" in bearer_operation)
print("parameters 칸 |", "parameters" in header_operation, "|", "parameters" in bearer_operation)
print("응답 코드 |", list(header_operation["responses"]), "|", list(bearer_operation["responses"]))
print("머리 없는 요청 |", header_plain.status_code, "|", bearer_plain.status_code)
print("교재용 접근 토큰 |", header_token.status_code, "|", bearer_token.status_code)'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/08-figures.md)
FIG1 = "08-1-앱-객체에서-생성-SDK까지"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 실습 앱 객체 app 처리 함수 다섯에서, 회색 상자 FastAPI가 처리 함수와 양식 클래스를 훑어 적음을 지나 노란 상자 응답 문서 딕셔너리 OpenAPI 3.1.0 요청 주소 다섯으로 갑니다. 이어서 노란 상자 실습 폴더 openapi.json 새로 만든 글과 같음 True, 회색 상자 생성기 7.25.0 typescript-fetch 노트북 밖 README 명령을 지나 초록 상자 생성 SDK client/generated 요청 주소마다 함수 하나에 닿는 그림"
FIG1_CAP = "앱 객체가 만든 응답 문서는 실습 폴더의 openapi.json과 같았고, 생성 SDK는 그 문서로 노트북 밖에서 만든 코드입니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 실습 폴더의 앱과 파일이고, 노란 상자 둘은 노트북 2절과 3절의 출력입니다.
회색 상자 둘은 라이브러리와 생성기가 하는 일이고, 생성기는 이 노트북에서 실행하지 않았습니다."""

FIG2 = "08-2-요청-주소-v1-chat의-칸"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 POST /v1/chat operationId chat_v1_chat_post에서 노란 상자 넷으로 갈라집니다. 넷은 요청 본문 형식 ChatRequest를 가리킴, 200 응답 형식 ChatResponse를 가리킴, 422 응답 입력 형식 검사, 매개변수 authorization 자리 header입니다. 요청 본문 형식 상자 아래에는 노란 상자 components의 ChatRequest 꼭 채울 칸 둘 question 1자 이상 500자 이하가 있는 그림"
FIG2_CAP = "요청 주소 /v1/chat의 칸은 요청 본문과 200 응답의 형식을 components 쪽 자리로 가리켰고, 가리킨 ChatRequest에 글자 수 조건이 적혀 있었습니다."
FIG2_READ = """위에서 아래로 읽습니다.
초록 상자는 실습 앱의 요청 주소 하나이고, 노란 상자는 모두 노트북 2절의 출력입니다.
요청 본문 형식 상자는 형식을 다시 적지 않고, 맨 아래 상자의 자리를 가리킵니다."""

FIG3 = "08-3-요청-주소와-생성-함수"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 노란 상자 JSON 요청 주소 셋 본문 종류 아래 schema와 노란 상자 SSE 요청 주소 둘 본문 종류 아래 itemSchema가 회색 상자 생성기 typescript-fetch 노트북 밖으로 모입니다. 생성기에서 노란 상자 함수 셋 ChatResponse나 HealthResponse를 내놓는 Promise와, 노란 상자 함수 둘 void를 내놓는 Promise 응답 본문을 읽지 않음으로 갈라집니다. 함수 둘 상자에서 점선이 초록 상자 SSE 사건은 손으로 쓴 client/stream.ts가 fetch로 읽음으로 이어지는 그림"
FIG3_CAP = "JSON 요청 주소 셋의 함수는 응답 형식을 내놓았고, SSE 요청 주소 둘의 함수는 void를 내놓아 SSE 사건은 손으로 쓴 TS 파일이 읽습니다."
FIG3_READ = """위에서 아래로 읽습니다.
위 노란 상자 둘은 노트북 2절, 아래 노란 상자 둘은 4절의 출력이고, 회색 상자 생성기는 노트북에서 실행하지 않았습니다.
점선은 생성 SDK 대신 다른 파일이 맡는 갈래이고, 초록 상자는 06절에서 글로 읽은 실습 폴더 파일입니다."""

FIG4 = "08-4-의존성-하나만-바꾼-두-응답-문서"
FIG4_ALT = "맨 위 파란 상자 같은 처리 함수 health GET /v1/ping 새 앱 객체 아래에 칸 둘이 나란히 있습니다. 왼쪽 칸 실행 1 제공 함수에는 초록 상자 dependencies에 require_token에서 노란 상자 보안 방식 칸 False 매개변수 authorization 응답 코드 200과 422로 이어집니다. 오른쪽 칸 실행 2 보안 객체에는 파란 상자 dependencies에 HTTPBearer 객체에서 노란 상자 보안 방식 칸 True security 칸 HTTPBearer 응답 코드 200으로 이어집니다. 두 칸은 맨 아래 회색 상자 두 실행 모두 머리 없음 401 교재용 접근 토큰 200으로 모이는 그림"
FIG4_CAP = "의존성 하나만 보안 객체로 바꾸자, 상태 코드는 같았는데 응답 문서에 보안 방식 칸과 security 칸이 생겼습니다."
FIG4_READ = """맨 위 파란 상자는 두 실행이 함께 쓴 처리 함수와 요청 주소입니다.
왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 칸마다 위가 의존성, 아래가 노트북 5절의 출력입니다.
맨 아래 회색 상자는 두 실행에서 같았던 상태 코드입니다."""

ILLU = "08-5-모형을-보고-만든-화물-칸"
ILLU_ALT = "흰 바탕에 앞쪽 나무 탁자 위 작은 모형 열차 칸 다섯이 한 줄로 놓여 있습니다. 왼쪽 셋은 올리브색 칸이고, 오른쪽 둘은 흰색과 회색 빗금 줄무늬 칸입니다. 탁자 뒤 비스듬한 선로에는 실제 화물 칸 다섯이 같은 차례로 서 있습니다. 왼쪽 셋은 벽과 지붕이 있는 올리브색 칸이고, 오른쪽 둘은 바닥과 바퀴만 있는 빈 칸입니다. 기관차·사람·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "모형에서 한 가지 색인 칸 셋은 벽과 지붕이 있는 실제 칸이 되었고, 줄무늬 칸 둘은 바닥만 있는 빈 칸이 되었습니다."
# 1차 job ee589176-cd27-4481-8d0e-a5ddede7df50 채택(재생성 0) — 저장 PNG를 열어 센 개수로 적음(모형 칸 다섯·실제 칸 다섯)
ILLU_READ = "앞쪽 나무 탁자 위 모형 칸 다섯은 왼쪽 셋이 올리브색, 오른쪽 둘이 흰색과 회색의 빗금 줄무늬입니다. 뒤쪽 선로의 실제 화물 칸 다섯도 같은 차례로 서 있습니다. 왼쪽 셋은 벽과 지붕이 있는 올리브색 칸이고, 오른쪽 둘은 바닥과 바퀴만 있는 빈 칸입니다. 모형이 응답 문서이고, 실제 칸 다섯이 생성 SDK의 함수 다섯입니다. 줄무늬 칸 둘이 <code>itemSchema</code>로 적은 SSE 요청 주소이고, 빈 칸 둘이 <code>Promise&lt;void&gt;</code>를 내놓는 함수입니다."

METAPHOR = """<p>차량 공장은 새 화물 열차를 만들기 전에, 탁자 위에 작은 축소 모형부터 받습니다. 모형에는 칸 다섯이 차례대로 놓여 있고, 칸마다 색이 칠해져 있습니다. 공장은 모형만 보고 실제 칸을 만들고, 한 가지 색으로 칠한 칸은 벽과 지붕까지 갖춘 칸으로 만듭니다. 줄무늬만 그린 칸은 공장이 모르는 표시라서, 바닥만 있는 빈 칸으로 둡니다.</p><p>축소 모형이 응답 문서이고, 모형의 칸 하나가 요청 주소 하나입니다. 공장은 생성기이고, 공장이 만든 실제 칸이 생성 SDK의 함수입니다. 줄무늬 칸은 응답 형식을 키 <code>itemSchema</code>로 적은 SSE 요청 주소입니다. 바닥만 있는 칸은 <code>Promise&lt;void&gt;</code>를 내놓는 함수입니다.</p><p>비유와 다른 점이 있습니다. 응답 문서는 사람이 만들지 않고, 앱 객체가 처리 함수와 양식 클래스에서 만듭니다. 생성기가 줄무늬를 모른다는 것은 노트북 밖에서 생성기를 실행했을 때 나온 경고로만 확인했습니다. 이 노트북에서는 생성기를 실행하지 않았습니다.</p>"""

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 앱 객체가 만든 응답 문서에서 요청 주소와 입력 형식·응답 형식을 찾습니다.
2. 응답 문서로 만든 TS 코드(생성 SDK)에서 요청 주소마다 만든 함수를 읽습니다.
3. 인증을 적는 자리 하나만 바꾸면 응답 문서가 어떻게 바뀌는지 실험합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.
실습 앱의 에이전트 그래프도 이 절에서는 부르지 않습니다.
그래서 다시 실행해도 같은 값이 나와야 합니다.

요청은 시험용 클라이언트로 같은 노트북 안에서 보냅니다.
서버 프로그램을 띄우지 않고, 네트워크와 포트를 쓰지 않습니다.
실습 폴더의 파일을 가져오고 읽기만 하며, 쓰는 파일은 없습니다.
TS 코드를 만드는 생성기와 TS 검사 도구는 노트북에서 실행하지 않습니다.

걸린 시간은 재지 않았습니다.
앞 절에서 배운 함수는 이 절에서 쓰지 않아, 도구 파일도 가져오지 않습니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 fastapi 0.135.0, httpx 0.28.1, pydantic 2.12.5, starlette 1.6.0입니다.
패키지 langgraph 1.2.11과 langchain 1.4.0은 실습 앱 파일이 가져오는 패키지입니다.
여섯 모두 실습 폴더 잠금과 같은 판입니다.

교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽고, 5절 실험의 가설을 함께 세웁니다.
5절의 두 실행은 실습 시간에 실행합니다.

실습 폴더 `labs/part7/ch30-fastapi-serving`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md(r"""## 1. 준비

07절에서는 보안 도구 클래스 `HTTPBearer`를 쓴 새 앱의 응답 문서에만 보안 방식 칸이 있는 것을 봤습니다.
이 절은 앱 객체가 만드는 응답 문서를 처음부터 읽습니다.
제목의 OpenAPI는 요청 주소와 입력 형식·응답 형식을 JSON으로 적는 규격의 이름입니다.
제목의 TS는 TypeScript의 줄임말로, JavaScript에 자료의 형식을 적을 수 있게 한 언어입니다.
제목의 SDK는 Software Development Kit의 줄임말로, 서비스를 부르는 코드를 묶어 둔 것입니다.

이 절에서는 OpenAPI 규격으로 적은 문서를 응답 문서, 그 문서로 만든 TS 코드 묶음을 생성 SDK라고 부릅니다.
두 말은 2절과 4절에서 자세히 풉니다.
첫 셀은 패키지 여섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md(r"""**결과 읽기** — 출력 줄 `fastapi: 0.135.0`과 `starlette: 1.6.0`이 보입니다.
여섯 모두 실습 폴더 잠금과 같은 판이고, 07절과 같은 목록입니다.
응답 문서를 만드는 코드는 패키지 fastapi에 들어 있습니다.
이 절은 모델 객체를 만들지 않아, API 키를 확인하는 셀도 없습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 json은 딕셔너리를 JSON 글로 바꾸고, 파일의 JSON 글을 읽을 때 씁니다.
클래스 `HTTPBearer`는 07절에서 본 보안 도구 클래스로, 5절 실험에서 씁니다."""),
        setup(IMPORTS),
        md(r"""**결과 읽기** — 출력 줄 `가져온 이름: json, Depends, FastAPI, HTTPBearer, TestClient`가 보입니다.
이 절은 앞 절에서 배운 함수를 쓰지 않아, 도구 파일 `serve_tools.py`를 가져오지 않습니다.

다음 셀은 01절 2절과 같은 파일 위치 셀로, 후보 셋 가운데 실습 폴더를 고릅니다."""),
        code(FIND_LAB),
        md(r"""**결과 읽기** — 출력 줄 `실습 폴더를 찾았는가: True`가 보입니다.
고른 후보는 연 자리마다 달라서 출력하지 않습니다.

다음 셀은 작업 폴더를 실습 폴더로 옮긴 뒤 이름을 가져옵니다.
앱 파일에서 앱 객체 `app`과 처리 함수 `health`, 제공 함수 `require_token`을 가져옵니다.
양식 클래스 `ChatRequest`는 01절에서 본 입력 형식의 클래스입니다.
앱 객체의 속성 `openapi_schema`도 함께 출력합니다."""),
        code(IMPORT_APP),
        md(r"""**결과 읽기** — 출력 줄 `가져온 앱 객체의 종류: FastAPI`와 `가져온 함수: health require_token`이 보입니다.
속성 `openapi_schema`는 아직 `None`입니다.
앱 객체는 응답 문서를 처음 부탁받을 때 만들어, 이 속성에 담아 둡니다.
그런지는 2절에서 확인합니다.

## 2. 앱 객체가 만드는 응답 문서

응답 문서(OpenAPI 문서)는 앱 객체가 요청 주소마다 받는 요청과 내놓는 응답의 모양을 적은 JSON 문서입니다.
만들 열차를 작게 줄인 모형이, 칸의 차례와 칸마다 실을 짐의 모양을 보여 주는 것과 같습니다.
이 앱에서는 앱 객체의 메서드 `openapi`가 이 문서를 딕셔너리로 내놓습니다.
문서의 모양은 OpenAPI 규격이 정하고, 맨 위 칸 `openapi`에 그 규격의 판이 적힙니다.

다음 셀은 메서드 `openapi`를 불러 응답 문서를 만들고, 맨 위 칸을 봅니다."""),
        code(DOC_TOP),
        md(r"""**결과 읽기** — 출력 줄 `OpenAPI 판: 3.1.0`이 보입니다.
맨 위 칸은 넷이고, 칸 `info`에는 앱 파일 17행에 적은 제목과 판 `1.0.0`이 들어 있습니다.
판 `1.0.0`은 이 앱에 붙인 판이고, 패키지 fastapi의 판과는 다른 값입니다.
칸 `paths`는 요청 주소마다 받는 요청과 응답을 적고, 칸 `components`는 여러 곳에서 쓰는 형식을 모아 둡니다.

다음 셀은 칸 `paths`에 적힌 요청 주소와 요청 방식을 한 줄씩 출력합니다."""),
        code(PATHS),
        md(r"""**결과 읽기** — 출력 줄 `요청 주소 수: 5`와, 라벨 줄 아래 다섯 줄이 보입니다.
앱 파일에서 요청 주소 데코레이터 줄로 이은 처리 함수 다섯이 모두 적혔습니다.
요청 주소 `/openapi.json`은 이 목록에 없습니다.
설치판 fastapi `applications.py` 1117행이 문서를 내주는 요청 주소를 문서에서 빼기 때문입니다.

다음 셀은 01절부터 써 온 요청 주소 `/v1/chat`의 칸을 꺼냅니다.
요청 본문과 응답의 형식이 어떻게 적혔는지 봅니다."""),
        code(CHAT_OP),
        md(r"""**결과 읽기** — 출력 줄 `응답 코드: ['200', '422']`와 `operationId: chat_v1_chat_post`가 보입니다.
요청 본문 형식과 200 응답 형식에는 형식 대신 키 `$ref` 하나가 있습니다.
키 `$ref`는 같은 문서의 다른 자리를 가리키는 표시입니다.
값 `#/components/schemas/ChatRequest`는 맨 위 칸 `components`에서 `schemas`, `ChatRequest` 차례로 들어간 자리입니다.
응답 코드 422는 01절에서 본 입력 형식 검사의 응답입니다.

칸 `operationId`는 요청 주소마다 붙는 이름입니다.
설치판 fastapi `utils.py` 95~100행이 처리 함수 이름과 요청 주소, 요청 방식을 이어 만듭니다.
매개변수 `authorization`은 07절에서 본 것처럼, 요청 머리에서 읽는 값입니다.

다음 셀은 칸 `components`에 모은 형식 이름과, 입력 형식 `ChatRequest`의 칸 조건을 봅니다.
마지막 줄은 Ch 19 02절에서 쓴 메서드 `model_json_schema`로 만든 딕셔너리와 견줍니다."""),
        code(FORMATS),
        md(r"""**결과 읽기** — 출력 줄 `칸 question:`에 `'maxLength': 500`과 `'minLength': 1`이 보입니다.
실습 파일 `schemas.py`의 양식 클래스에 `Field`로 적은 글자 수 조건이 그대로 적혔습니다.
꼭 채울 칸은 `question`과 `thread_id` 둘이고, 칸 `thread_id`에는 글 모양 조건 `pattern`이 있습니다.
마지막 줄은 `True`로, Ch 19 02절 방법으로 만든 딕셔너리와 같았습니다.

형식 이름 다섯 가운데 `HTTPValidationError`와 `ValidationError`는 422 응답을 적으려고 라이브러리가 더한 형식입니다.
앱 파일에는 이 두 이름의 클래스가 없습니다.

다음 셀은 JSON 글로 답하는 `/v1/chat`과, SSE 사건으로 답하는 `/v1/chat/stream`의 200 응답을 견줍니다.
본문 종류와, 그 아래에 적힌 키를 봅니다."""),
        code(STREAM_CONTENT),
        md(r"""**결과 읽기** — 출력 줄 `/v1/chat/stream: ['text/event-stream'] ['itemSchema']`가 보입니다.
요청 주소 `/v1/chat`은 본문 종류 `application/json` 아래에 키 `schema`로 응답 형식을 적었습니다.
SSE 사건으로 답하는 요청 주소는 키 `itemSchema`로, SSE 사건 하나의 형식을 적었습니다.
05절의 작은 앱에서 본 것처럼, 이 키 아래에 칸 `data`·`event`·`id`·`retry`가 적힙니다.
이 차이가 4절의 생성 SDK에서 다시 나옵니다.

다음 셀은 메서드 `openapi`를 한 번 더 불러, 처음 받은 딕셔너리와 같은 객체인지 봅니다."""),
        code(CACHE),
        md(r"""**결과 읽기** — 두 줄 모두 `True`입니다.
연산자 `is`는 두 이름이 같은 객체를 가리키는지 봅니다.
앱 객체는 처음 만든 문서를 속성 `openapi_schema`에 담아 두고, 다음부터는 그 객체를 그대로 내놓습니다.
설치판 fastapi `applications.py` 1083~1084행이 문서가 없을 때만 새로 만듭니다.

그래서 문서를 만든 뒤에 이은 요청 주소는 문서에 나오지 않습니다.
이 노트북에서는 실행하지 않았고, 노트북 밖에서 한 번 확인했습니다.

다음 셀은 요청 주소 `/openapi.json`으로 같은 문서를 받아 봅니다.
시험용 클라이언트로 GET을 보냅니다."""),
        code(HTTP_DOC),
        md(r"""**결과 읽기** — 출력 줄 `상태 코드: 200`과 `본문 종류: application/json`이 보입니다.
받은 문서를 읽은 딕셔너리는 메서드 `openapi`가 내놓은 딕셔너리와 같았습니다.
실습 폴더 README는 서버를 띄운 뒤 주소 `/docs`와 `/openapi.json`에서 이 문서를 보라고 적습니다.
이 절에서는 서버를 띄우지 않아, 그 화면은 열지 않았습니다.

## 3. 응답 문서와 openapi.json

실습 폴더 맨 위에는 파일 `openapi.json`이 있습니다.
응답 문서를 JSON 글로 적은 파일이고, 4절의 생성 SDK는 이 문서를 생성기에 넣어 만든 코드입니다.
다음 셀은 응답 문서를 이 파일과 같은 설정의 JSON 글로 바꿔, 파일 글과 견줍니다.
인자 `ensure_ascii=False`는 한글을 그대로 적게 하고, 인자 `indent`는 칸마다 줄을 바꿔 들여 쓰게 합니다.
파일은 읽기만 하고 다시 쓰지 않습니다."""),
        code(FILE_COMPARE),
        md(r"""**결과 읽기** — 출력 줄 `두 글이 같은가: True`가 보입니다.
두 글의 글자 수도 `9987`로 같습니다.
인자 `ensure_ascii`를 뺀 글은 한글이 유니코드 번호로 적혀, 파일 글과 같지 않았습니다.
파일 첫 줄은 중괄호이고, 둘째 줄에 규격의 판이 적혀 있습니다.

지금 앱으로 만든 글과 파일 글이 같으므로, 이 노트북은 파일을 다시 쓰지 않습니다.
파일로 쓸 때는 이 글을 `with open(…, "w", encoding="utf-8")`로 연 파일에 적습니다.
앱 파일의 요청 주소나 양식 클래스를 바꾸면 이 글이 달라집니다.
그때는 파일과 생성 SDK를 함께 다시 만듭니다.

## 4. 생성 SDK 읽기

생성 SDK는 응답 문서를 생성기에 넣어 만든, 앱을 부르는 코드 묶음입니다.
차량 공장이 축소 모형만 보고 실제 화물 칸을 만드는 것과 같습니다.
이 실습 폴더에서는 `client/generated/` 폴더의 파일 열여덟(TS 파일 열하나와 설명 문서 일곱)이 생성 SDK입니다.
생성기는 OpenAPI Generator의 `typescript-fetch`로, 06절에서 본 함수 `fetch`로 요청을 보내는 코드를 만듭니다.
생성기는 Java 프로그램이라서, README 명령으로 노트북 밖에서 실행합니다.

다음 셀은 이 절에서 쓸 함수를 정의합니다.
글 줄 목록에서 낱말이 든 줄을 찾아, 줄 번호와 함께 출력합니다."""),
        code(DEF_LINES),
        md(r"""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `strip`은 줄 앞뒤의 공백을 뺀 글을 내놓습니다.
줄 번호는 0부터 세는 자리에 1을 더해, 파일을 열었을 때의 줄 번호와 맞춥니다.

다음 셀은 파일 `openapitools.json`에서 생성기 판을 읽습니다.
그다음 생성 SDK 파일 `DefaultApi.ts`의 머리 주석에서 줄 셋을 찾습니다.
함수 `json.load`는 연 파일의 JSON 글을 읽어 파이썬 값으로 바꿉니다."""),
        code(SDK_HEAD),
        md(r"""**결과 읽기** — 출력 줄 `생성기 판: 7.25.0`이 보입니다.
7행에는 응답 문서의 칸 `info`에 있던 판 `1.0.0`이 적혔습니다.
10행과 12행은 이 파일을 생성기가 만들었으니, 손으로 고치지 말라는 주석입니다.
고칠 일이 있으면 앱 파일을 고치고, 응답 문서와 생성 SDK를 다시 만듭니다.

다음 셀은 같은 파일에서 요청 주소마다 만든 함수를 찾습니다.
네 칸 들여 쓴 `async`로 시작하고, 이름에 `Raw(`와 `RequestOpts(`가 없는 줄이 앱을 부를 때 쓰는 함수입니다.
메서드 `rstrip`은 줄 끝의 공백과 `{`를 빼고, 메서드 `split`은 주어진 글에서 나눕니다."""),
        code(SDK_FUNCS),
        md(r"""**결과 읽기** — 라벨 줄 아래 다섯 줄이, 요청 주소 다섯에 하나씩 만든 함수입니다.
JSON 글로 답하는 요청 주소 셋의 함수는 `Promise<ChatResponse>`나 `Promise<HealthResponse>`를 내놓습니다.
SSE 사건으로 답하는 요청 주소 둘의 함수는 140행과 278행에서 `Promise<void>`를 내놓습니다.
형식 `Promise`는 TS에서 await로 기다려 값을 받는 객체이고, `void`는 줄 값이 없다는 표시입니다.

함수 이름은 2절의 칸 `operationId`를 TS 이름 모양으로 바꾼 것입니다.
예를 들어 `chat_v1_chat_post`가 190행의 `chatV1ChatPost`가 되었습니다.
이름 앞의 `async`는 TS에서도 비동기 함수라는 표시입니다.

다음 셀은 이 함수들이 받은 응답을 어떻게 감싸는지 찾습니다."""),
        code(SDK_WRAP),
        md(r"""**결과 읽기** — 첫 라벨 줄 아래 134행과 272행이 받은 응답을 `VoidApiResponse`로 감쌉니다.
둘째 라벨 줄 아래 세 줄은 `JSONApiResponse`로 감싸고, 본문 JSON을 `ChatResponse` 같은 형식으로 바꿉니다.
SSE 사건으로 답하는 요청 주소 둘의 함수는 응답 본문을 읽어 값으로 주지 않는다는 뜻입니다.
2절에서 본 것처럼, 두 요청 주소는 응답 형식을 키 `schema`가 아니라 `itemSchema`로 적었습니다.

노트북 밖에서 생성기를 실행해 보니, 생성기는 키 `itemSchema`를 뜻밖의 칸이라고 경고했습니다.
SSE 사건은 06절에서 글로 읽은 TS 파일 `client/stream.ts`가 함수 `fetch`로 읽습니다.
생성 SDK와 손으로 쓴 이 파일이 요청 주소를 나눠 맡습니다.

다음 셀은 요청 인자의 칸을 적은 TS 선언과, 그 안의 칸 `authorization`을 찾습니다."""),
        code(SDK_AUTH),
        md(r"""**결과 읽기** — 첫 라벨 줄 아래 네 줄은 요청 인자의 칸을 적은 TS 선언 `interface`입니다.
둘째 라벨 줄 아래 45·60·71·82행에서, 네 선언 모두 칸 `authorization?: string | null`을 가집니다.
칸 이름 뒤의 `?`는 넣지 않아도 되는 칸이라는 표시입니다.
실습 앱이 접근 토큰을 요청 머리 매개변수로 받아서, 생성 SDK도 요청마다 인자로 받습니다.
요청 주소 `/health`는 접근 토큰을 받지 않아, 요청 인자 선언이 없습니다.

다음 셀은 생성 SDK의 `models/ChatRequest.ts`에서 줄 넷을 찾습니다.
칸 이름의 줄, JSON 칸 이름으로 옮기는 두 줄, 글자 수 조건의 줄입니다."""),
        code(SDK_MODEL),
        md(r"""**결과 읽기** — 첫 라벨 줄 아래 25행과 29행이 입력 형식 `ChatRequest`의 두 칸입니다.
응답 문서의 칸 이름 `thread_id`가 TS 쪽에서는 `threadId`로 바뀌었습니다.
52행은 받은 JSON의 `thread_id`를 `threadId`로 옮기고, 68행은 보낼 때 다시 `thread_id`로 적습니다.
마지막 라벨 줄 아래에는 아무 줄도 없습니다.

생성기 문서는 칸 이름을 바꾸는 설정의 기본값이 낙타 등 모양 이름(camelCase)이라고 적습니다.
TS 형식에는 칸 이름과 글이라는 형식만 있고, 글자 수 조건은 없습니다.
그 조건은 서버의 입력 형식 검사가 맡아, 어기면 422로 답합니다.

## 5. 실험: 인증을 적는 자리 바꾸기

07절에서는 `HTTPBearer`를 쓴 새 앱의 응답 문서에만 보안 방식 칸이 있었습니다.
그런데 07절의 두 앱은 처리 함수와 요청 주소, 요청 방식도 서로 달랐습니다.
보안 방식 칸이 인증을 적는 방법 때문에 생겼는지 보려면, 다른 것은 같게 두고 그 하나만 바꿔야 합니다.
이 실험은 새 앱 객체 둘에 같은 처리 함수 `health`를 같은 요청 주소로 잇습니다.
바꿀 값은 의존성으로 적는 것 하나입니다.

인자 `dependencies`는 처리 함수의 매개변수로 받지 않을 의존성을 적는 자리입니다.
FastAPI 문서는 여기에 적은 의존성도 보통 의존성처럼 실행되고, 오류로 멈출 수 있다고 적습니다.
메서드 `add_api_route`는 05절에서 본, 처리 함수를 요청 방식과 요청 주소에 잇는 메서드입니다.

**가설** — 07절의 결과대로라면, 실행 2에만 보안 방식 칸 `securitySchemes`가 생길 것입니다.
실행 1은 실습 앱처럼, 매개변수 `authorization`이 요청 머리 자리로 적힐 것입니다.
머리 없는 요청은 두 실행 모두 401을 받을 것입니다.

**실행 1** — 다음 셀은 실습 앱의 제공 함수 `require_token`을 의존성으로 적습니다.
실행 전에 예상해 봅니다.
응답 코드 목록에 422가 있을까요?"""),
        code(RUN1),
        md(r"""**결과 읽기** — 출력 줄 `보안 방식 칸이 있는가: False`와 `응답 코드: ['200', '422']`가 보입니다.
제공 함수의 매개변수 `authorization`이 요청 주소의 매개변수로 적혔습니다.
매개변수가 있으니, 그 값이 맞지 않을 때의 422 응답도 함께 적혔습니다.
설치판 fastapi `openapi/utils.py` 457~470행이 매개변수나 요청 본문이 있을 때만 422를 적습니다.

**실행 2** — 다음 셀은 값 하나만 바꿔, 의존성에 보안 객체를 적습니다.
보안 객체 `bearer`는 07절처럼 `HTTPBearer()`로 만듭니다.
요청 주소와 요청 방식, 처리 함수는 실행 1과 같습니다.
실행 전에 예상해 봅니다.
요청 주소에 적힌 칸은 어떻게 바뀔까요?"""),
        code(RUN2),
        md(r"""**결과 읽기** — 출력 줄 `보안 방식 칸이 있는가: True`와 `응답 코드: ['200']`이 보입니다.
칸 `components`에 보안 방식 `HTTPBearer`가 생겼고, 요청 주소에는 칸 `security`가 생겼습니다.
칸 `parameters`는 없어졌고, 매개변수가 없으니 422도 적히지 않았습니다.
설치판 `openapi/utils.py` 289~296행이 보안 객체를 찾아 칸 `security`를 적습니다.
같은 파일 573~575행은 찾은 보안 방식을 칸 `components`에 모읍니다.

다음 셀은 두 앱 객체에 요청을 보내, 상태 코드도 견줍니다.
머리 없는 요청과, 교재용 접근 토큰을 실은 요청입니다."""),
        code(RUN_REQUESTS),
        md(r"""**결과 읽기** — 두 줄 모두 머리 없는 요청은 `401`, 교재용 접근 토큰을 실은 요청은 `200`입니다.
상태 코드는 같았고, 401 응답 본문의 글만 달랐습니다.
07절에서 본 것처럼 실행 2의 보안 객체는 접근 토큰 글을 견주지 않습니다.
이 셀에서는 틀린 글을 보내지 않아, 그 차이는 보지 않았습니다.

다음 셀은 두 실행을 한 표로 모읍니다."""),
        code(RESULT_TABLE),
        md(r"""**결과 읽기** — 라벨 줄 아래 일곱 줄이 두 실행을 견줍니다.
줄 `보안 방식 칸 | False | True`와 `security 칸 | False | True`가 보입니다.
줄 `parameters 칸 | True | False`에서, 매개변수 칸은 실행 1에만 있습니다.
상태 코드 두 줄은 `머리 없는 요청 | 401 | 401`과 `교재용 접근 토큰 | 200 | 200`으로 같습니다.

**결론** — 바꾼 값은 인자 `dependencies`에 적은 것 하나였습니다.
두 요청의 상태 코드는 같았지만, 응답 문서는 달랐습니다.
보안 객체를 적은 실행 2에만 보안 방식 칸과 칸 `security`가 생겼습니다.
실습 앱은 실행 1 모양이라, 4절의 생성 SDK도 접근 토큰을 요청마다 인자로 받았습니다.
이 노트북은 걸린 시간을 재지 않았고, 응답 문서의 칸과 상태 코드만 확인했습니다.

## 정리

1. 메서드 `openapi`가 내놓은 응답 문서는 실습 폴더 `openapi.json`과 글이 같았습니다.
2. 생성 SDK에서 SSE 사건으로 답하는 요청 주소 둘의 함수는 `Promise<void>`를 내놓았습니다.
3. 의존성 하나만 보안 객체로 바꾸자, 상태 코드는 같은데 응답 문서에 보안 방식 칸이 생겼습니다.

09절에서는 실제로 모델을 부르는 에이전트를 요청 주소 `/v1/chat/live`로 부릅니다."""),
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


L_CH19_02 = "../../part5/ch19-model-tools/02-Pydantic-인자와-반환-스키마.html"
L_01 = "01-비동기-라우팅과-스키마.html"
L_05 = "05-POST-SSE-이벤트-설계.html"
L_06 = "06-fetch-재연결과-오류-이벤트.html"
L_07 = "07-인증-CORS-타임아웃.html"
L_09 = "09-실제-Agent-HTTP-통합.html"

TERM_ROWS = [
    ("응답 문서(OpenAPI 문서)", "앱 객체가 요청 주소마다 받는 요청과 내놓는 응답의 모양을, OpenAPI 규격에 맞춰 적은 JSON 문서입니다. 만들 열차를 작게 줄인 모형이, 칸의 차례와 칸마다 실을 짐의 모양을 보여 주는 것과 같습니다. 이 절에서는 메서드 <code>app.openapi()</code>가 이 문서를 딕셔너리로 내놓고, 실습 폴더의 <code>openapi.json</code>이 같은 문서를 JSON 글로 적은 파일입니다."),
    ("생성 SDK", "응답 문서를 생성기에 넣어 만든, 앱을 부르는 코드 묶음입니다. 차량 공장이 축소 모형만 보고 실제 화물 칸을 만드는 것과 같습니다. 이 절에서는 생성기 <code>typescript-fetch</code> 7.25.0이 만든 <code>client/generated/</code>의 파일 열여덟(TS 파일 열하나와 설명 문서 일곱)이 생성 SDK입니다."),
]

COMPARE_ROWS = [
    ("바꾼 값 — 인자 <code>dependencies</code>", "<code>[Depends(require_token)]</code>", "<code>[Depends(bearer)]</code> — <code>bearer = HTTPBearer()</code>"),
    ("보안 방식 칸 <code>securitySchemes</code>", "<code>False</code>", "<code>True</code> — <code>{'HTTPBearer': {'type': 'http', 'scheme': 'bearer'}}</code>"),
    ("요청 주소의 칸 <code>security</code>", "<code>False</code>", "<code>True</code> — <code>[{'HTTPBearer': []}]</code>"),
    ("요청 주소의 칸 <code>parameters</code>", "<code>True</code> — <code>authorization</code>·<code>header</code>", "<code>False</code>"),
    ("응답 코드", "<code>['200', '422']</code>", "<code>['200']</code>"),
    ("머리 없는 요청", "<code>401</code>", "<code>401</code>"),
    ("교재용 접근 토큰을 실은 요청", "<code>200</code>", "<code>200</code>"),
]

LOOK_B5 = "노트북 2절에서 <code>OpenAPI 판: 3.1.0</code>과 <code>요청 주소 수: 5</code>를 찾습니다. 3절에서는 <code>두 글이 같은가: True</code>를 봅니다. 4절에서는 <code>생성기 판: 7.25.0</code>과, 140행·278행의 <code>Promise&lt;void&gt;</code>를 확인합니다."
LOOK_B6 = "5절 실행 1의 <code>보안 방식 칸이 있는가: False</code>와, 실행 2의 <code>보안 방식 칸이 있는가: True</code>를 찾습니다. 결과 표의 줄 <code>security 칸 | False | True</code>와 <code>머리 없는 요청 | 401 | 401</code>도 확인합니다."


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    compare = table_html(["견준 것", "실행 1(제공 함수)", "실행 2(보안 객체)"], COMPARE_ROWS)
    return """<!--meta: 강의 0.75h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>앱 객체의 메서드 <code>openapi</code>가 만든 응답 문서에서, 요청 주소와 입력 형식·응답 형식이 적힌 칸을 찾을 수 있습니다.</li>
<li>생성 SDK에서 요청 주소마다 만든 함수를 읽고, SSE 쪽 함수의 한계를 설명할 수 있습니다.</li>
<li>의존성 하나만 바꾼 실험으로, 응답 문서에 보안 방식 칸이 생기는 조건을 출력으로 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>웹 화면을 만드는 사람은 파이썬 앱 파일을 읽지 않고도 이 앱을 불러야 합니다. 어떤 요청 주소가 있고, 요청 본문에 어떤 칸을 채우며, 어떤 응답이 오는지 알아야 합니다. 이것을 사람이 손으로 옮겨 적으면, 앱을 고칠 때마다 두 글이 어긋나기 쉽습니다. 그래서 앱 객체가 코드에서 직접 만든 문서 하나를 두고, 앱을 부르는 코드도 그 문서로 만듭니다.</p><p>제목의 OpenAPI는 요청 주소와 입력 형식·응답 형식을 JSON으로 적는 규격의 이름입니다. 이 절에서는 그 규격으로 적은 문서를 응답 문서라고 부릅니다. 제목의 TS는 TypeScript의 줄임말로, JavaScript에 자료의 형식을 적을 수 있게 한 언어입니다. 제목의 SDK는 Software Development Kit의 줄임말로, 서비스를 부르는 코드를 묶어 둔 것입니다. 이 절에서는 응답 문서로 만든 TS 코드 묶음을 생성 SDK라고 부릅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 처리 함수 매개변수 힌트에 적은 양식 클래스가 요청 본문의 입력 형식이 되었습니다. 맞지 않는 요청은 처리 함수 전에 422를 받았습니다. 데코레이터 줄의 <code>response_model</code>에 적은 양식 클래스는 응답 형식이 되어, 내보낼 칸만 골랐습니다. 이 절은 그 두 형식이 응답 문서에 어떻게 적히는지 봅니다.</p><p><a href=\"""" + L_CH19_02 + """\">Ch 19 02절</a>에서는 양식 클래스를 메서드 <code>model_json_schema()</code>로 딕셔너리로 바꿔, 칸마다 적힌 규칙을 봤습니다. 이 절의 응답 문서에 적힌 입력 형식도, 같은 방법으로 만든 딕셔너리와 같았습니다.</p><p><a href=\"""" + L_05 + """\">05절</a>에서는 인자 <code>response_class</code>로 SSE를 보내면, 응답 문서의 본문 종류가 <code>text/event-stream</code>이 되는 것을 봤습니다. <a href=\"""" + L_06 + """\">06절</a>에서는 TS 파일 <code>client/stream.ts</code>가 함수 <code>fetch</code>로 SSE 사건을 읽는 모양을 글로 읽었습니다. <a href=\"""" + L_07 + """\">07절</a>에서는 보안 도구 클래스 <code>HTTPBearer</code>를 쓴 새 앱의 응답 문서에만 보안 방식 칸이 있었습니다. 실습 앱은 접근 토큰을 요청 머리 매개변수 <code>authorization</code>으로 받아, 보안 방식 칸이 없었습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + METAPHOR + """
""" + illustration_block() + """<h3>응답 문서의 모양</h3><p>앱 객체의 메서드 <code>openapi</code>는 앱에 이은 처리 함수를 모두 훑어, 응답 문서를 딕셔너리로 만듭니다. 맨 위 칸은 넷입니다. 칸 <code>openapi</code>에는 규격의 판 <code>3.1.0</code>이, 칸 <code>info</code>에는 앱의 제목과 판이 적힙니다. 칸 <code>paths</code>는 요청 주소마다 요청 방식과 요청 본문, 응답을 적습니다. 칸 <code>components</code>는 여러 곳에서 쓰는 형식을 모아 둡니다.</p><p>요청 주소 쪽에는 형식을 다시 적지 않고, 키 <code>$ref</code>로 칸 <code>components</code>의 자리를 가리킵니다. 요청 주소마다 붙는 이름 <code>operationId</code>는 처리 함수 이름과 요청 주소, 요청 방식을 이어 만듭니다. 앱 객체는 처음 만든 문서를 속성 <code>openapi_schema</code>에 담아 두고, 다음부터는 같은 객체를 내놓습니다. 요청 주소 <code>/openapi.json</code>으로 받는 문서도 이 딕셔너리를 JSON 글로 바꾼 것입니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 응답 문서는 <code>app.openapi()</code>가 내놓은 딕셔너리였고, 실습 폴더의 <code>openapi.json</code>과 글이 같았습니다. 생성 SDK의 <code>DefaultApi.ts</code>에는 요청 주소마다 함수가 하나씩 있었습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>생성 SDK를 만드는 곳</h3><p>생성 SDK는 노트북 밖에서 README 명령으로 만듭니다. 명령 <code>npx @openapitools/openapi-generator-cli generate</code>가 응답 문서를 읽고, 생성기 <code>typescript-fetch</code>로 TS 파일을 씁니다. 생성기는 Java 프로그램이라서, JDK 11 이상이 필요합니다. 생성기 판은 실습 폴더의 파일 <code>openapitools.json</code>이 <code>7.25.0</code>으로 정합니다.</p><p>생성기는 JSON 글로 답하는 요청 주소마다 응답 형식이 있는 함수를 만들었습니다. SSE 사건으로 답하는 요청 주소는 응답 형식을 키 <code>itemSchema</code>로 적고, 생성 SDK의 그 함수는 응답 본문을 값으로 주지 않습니다. 노트북 밖에서 생성기를 실행해 보니, 생성기는 키 <code>itemSchema</code>를 뜻밖의 칸이라고 경고했습니다. 그래서 SSE 사건은 <a href=\"""" + L_06 + """\">06절</a>의 손으로 쓴 <code>client/stream.ts</code>가 읽습니다.</p><p>이 노트북에서는 생성기와 TS 검사 도구를 실행하지 않았습니다. 만들어 둔 생성 SDK 파일을 파이썬으로 열어, 필요한 줄을 찾아 읽기만 했습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 메서드 <code>openapi</code>로 응답 문서를 만들고, 요청 주소와 형식이 적힌 칸을 차례로 꺼냅니다. 3절은 그 문서를 JSON 글로 바꿔, 실습 폴더의 <code>openapi.json</code>과 견줍니다. 4절은 생성 SDK 파일을 열어, 요청 주소마다 만든 함수와 요청 인자, 칸 이름을 찾습니다.</p><p>5절은 의존성 하나만 바꾼 두 실행으로 실험합니다. 모델 요청은 0번이고, API 키 없이 실행합니다. 서버 프로그램을 띄우지 않아 네트워크와 포트, 자식 프로세스를 쓰지 않습니다. 실습 폴더의 파일은 읽기만 하며, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>가설은 07절의 결과에서 세웠습니다. 07절의 두 앱은 인증을 적는 방법뿐 아니라, 처리 함수와 요청 주소도 달랐습니다. 이 실험은 같은 처리 함수 <code>health</code>를 같은 요청 주소 <code>GET /v1/ping</code>으로 새 앱 객체 둘에 이었습니다. 바꾼 것은 인자 <code>dependencies</code>에 적은 것 하나입니다. 실행 1은 실습 앱의 제공 함수 <code>require_token</code>이고, 실행 2는 보안 객체 <code>HTTPBearer()</code>입니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + compare + """
<p>두 실행은 머리 없는 요청에 401을, 교재용 접근 토큰을 실은 요청에 200을 보냈습니다. 두 요청에서 상태 코드는 같았지만, 응답 문서는 달랐습니다. 실행 2에만 칸 <code>components</code>의 보안 방식과 요청 주소의 칸 <code>security</code>가 생겼습니다. 실행 1은 접근 토큰을 매개변수 <code>authorization</code>으로 적었고, 그래서 422 응답도 함께 적혔습니다.</p><p>문서를 읽는 쪽에서 보면 이 차이가 큽니다. 실행 1의 문서에는 넣을 수 있는 요청 머리 하나가 적혀 있을 뿐, 그 값이 인증에 쓰인다는 표시는 없습니다. 실행 2의 문서는 이 요청 주소가 Bearer 방식의 인증을 쓴다고 적습니다. 실습 앱은 실행 1 모양이라, 생성 SDK도 접근 토큰을 요청마다 인자 <code>authorization</code>으로 받았습니다.</p><p>노트북 밖에서 두 실행의 응답 문서를 생성기에 한 번씩 넣어 보았습니다. 실행 1의 문서로 만든 함수는 인자 <code>authorization</code>을 받았습니다. 실행 2의 문서로 만든 함수에는 그 인자가 없고, 설정 칸 <code>accessToken</code>의 값으로 요청 머리 <code>Authorization</code>을 채웠습니다. 이 노트북에서는 실행하지 않았고, 생성기 7.25.0에서 한 번 본 결과입니다.</p>
<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>실습 폴더의 <code>openapi.json</code>은 지금 앱으로 만든 글과 같아서, 이 노트북은 파일을 다시 쓰지 않았습니다. 앱 파일의 요청 주소나 양식 클래스를 바꾸면 응답 문서가 바뀝니다. 그때는 파일과 생성 SDK를 함께 다시 만들고, README의 TS 검사 명령도 다시 실행합니다.</li><li>앱 객체는 처음 만든 응답 문서를 속성 <code>openapi_schema</code>에 담아 둡니다. 설치판 fastapi <code>applications.py</code> 1083~1084행이 문서가 없을 때만 새로 만듭니다. 그래서 문서를 만든 뒤에 이은 요청 주소는 문서에 나오지 않습니다. 이 노트북에서는 실행하지 않았고, 노트북 밖에서 한 번 확인했습니다.</li><li>노트북 밖에서 README 명령으로 생성기를 실행하자, 요청 주소 둘의 <code>itemSchema</code>가 뜻밖의 칸이라는 경고가 나왔습니다. 명령의 <code>--skip-validate-spec</code>이 문서 검사를 건너뛰게 해, 생성은 끝까지 갔습니다. 빈 폴더에 처음 만들면 목록 파일 <code>.openapi-generator/FILES</code>에 한 줄이 더 있었습니다. 같은 폴더에 한 번 더 만들자, 실습 폴더의 생성 SDK와 파일이 모두 글자까지 같았습니다.</li><li>실습 폴더 README의 TS 검사 명령은 판을 적은 <code>npx --package typescript@7.0.2 tsc …</code>입니다. 노트북 밖에서 2026-09-29에 최신 판을 받아 실행하자 판이 7.0.2였고, 오류 없이 끝났습니다. 다른 판에서는 실행하지 않았습니다.</li><li>생성 SDK는 가져오는 줄에 파일 확장자를 적지 않습니다. 그래서 Node.js v22.23.2가 TS 파일을 바로 읽는 방식으로는 돌지 않았습니다. 노트북 밖에서 불러 보니 오류 <code>ERR_MODULE_NOT_FOUND</code>가 났습니다. 실습 폴더 README의 시험 명령은 생성 SDK가 아니라, 직접 적은 시험 파일 <code>client/test_stream.ts</code>를 이 방식으로 실행합니다. 06절에서 노트북 밖에 실행해 통과했고, 이 절에서는 실행하지 않았습니다.</li><li>생성 SDK 파일의 머리 주석은 손으로 고치지 말라고 적습니다. 생성기를 다시 실행하면 파일을 새로 쓰기 때문입니다. 고칠 일이 있으면 앱 파일을 고친 뒤 다시 만듭니다.</li><li>생성 SDK의 TS 형식에는 칸 이름과 글이라는 형식만 있고, 글자 수와 <code>pattern</code> 조건은 없습니다. 그 조건은 서버의 입력 형식 검사가 맡아, 어기면 422로 답합니다.</li><li>실행 2의 보안 객체는 <a href=\"""" + L_07 + """\">07절</a>에서 본 것처럼 접근 토큰 글을 견주지 않습니다. 응답 문서에 보안 방식 칸이 생겨도, 글을 견주는 줄은 우리 코드가 따로 적어야 합니다. 이 절은 실습 앱의 인증을 바꾸지 않았고, 응답 문서와 생성 SDK도 그대로 두었습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>메서드 <code>openapi</code>가 내놓은 응답 문서는 실습 폴더 <code>openapi.json</code>과 글이 같았습니다.</li><li>생성 SDK에서 SSE 사건으로 답하는 요청 주소 둘의 함수는 <code>Promise&lt;void&gt;</code>를 내놓았습니다.</li><li>의존성 하나만 보안 객체로 바꾸자, 상태 코드는 같은데 응답 문서에 보안 방식 칸이 생겼습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_09 + """\">09절</a>에서는 실제로 모델을 부르는 에이전트를 요청 주소 <code>/v1/chat/live</code>로 부릅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 응답 문서에서 요청 주소 목록은 어느 칸에 있고, 이 앱에는 몇 개였나요?</p><p class="quiz-a">칸 <code>paths</code>에 있고, 다섯 개였습니다. 문서를 내주는 요청 주소 <code>/openapi.json</code>은 목록에 없습니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. 요청 본문 형식에 적힌 키 <code>$ref</code>는 무엇을 뜻하나요?</p><p class="quiz-a">같은 문서의 다른 자리를 가리키는 표시입니다. 값 <code>#/components/schemas/ChatRequest</code>는 칸 <code>components</code> 안의 형식 <code>ChatRequest</code>를 가리킵니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 「생성 SDK의 함수 <code>chatStreamV1ChatStreamPost</code>로 SSE 사건을 받으면 된다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 그 함수는 <code>Promise&lt;void&gt;</code>를 내놓고, 받은 응답을 <code>VoidApiResponse</code>로 감싸 본문을 읽지 않습니다. SSE 사건은 06절의 <code>client/stream.ts</code>가 읽습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 앱 파일의 양식 클래스를 고쳤다면, <code>openapi.json</code>과 생성 SDK는 어떻게 하나요?</p><p class="quiz-a">응답 문서가 바뀌므로 파일을 다시 쓰고, 생성기로 생성 SDK를 다시 만듭니다. 생성 SDK 파일을 손으로 고치지 않습니다. 틀렸다면 노트북 3절과 4절을 다시 읽습니다.</p><p class="quiz-q">5. 5절 실험에서 바꾼 값은 무엇이고, 응답 문서에 무엇이 생겼나요?</p><p class="quiz-a">인자 <code>dependencies</code>에 적은 것을 제공 함수 <code>require_token</code>에서 보안 객체로 바꿨습니다. 실행 2에만 보안 방식 칸과 칸 <code>security</code>가 생겼고, 상태 코드는 두 실행이 같았습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://fastapi.tiangolo.com/tutorial/first-steps/">FastAPI First Steps</a></div>확인 2026-09-29 · OpenAPI는 API의 요청 주소와 매개변수, 주고받는 자료를 적는 규격이라고 적습니다. 라이브러리 FastAPI가 이 문서를 만들어 <code>/openapi.json</code>으로 내준다고 적습니다. 클라이언트 코드를 만드는 데 쓸 수 있다고도 적습니다.</li><li><div><a href="https://fastapi.tiangolo.com/advanced/generate-clients/">FastAPI Generating SDKs</a></div>확인 2026-09-29 · <code>operationId</code>는 함수 이름과 요청 주소, 요청 방식으로 만든다고 적습니다. 도구로 OpenAPI Generator를 들고, 앱을 바꾸면 다시 만들라고 적습니다.</li><li><div><a href="https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/">FastAPI Dependencies in path operation decorators</a></div>확인 2026-09-29 · 인자 <code>dependencies</code>는 <code>Depends()</code>의 목록이라고 적습니다. 값은 쓰지 않지만 보통 의존성처럼 실행되고, 오류로 멈출 수 있다고 적습니다.</li><li><div><a href="https://openapi-generator.tech/docs/generators/typescript-fetch/">OpenAPI Generator typescript-fetch</a></div>확인 2026-09-29 · Fetch API로 부르는 TS 코드를 만든다고 적습니다. 보안 방식 BearerToken을 지원하고, 칸 이름을 바꾸는 설정의 기본값은 camelCase라고 적습니다.</li><li><div><a href="https://github.com/OpenAPITools/openapi-generator-cli">OpenAPI Generator CLI</a></div>확인 2026-09-29 · JDK 11이 가장 낮게 지원하는 판이라고 적습니다. 생성기 판을 <code>openapitools.json</code>에 적어 둔다고 적습니다.</li><li>설치판 fastapi 0.135.0 소스 <code>applications.py</code> 1069행이 메서드 <code>openapi</code>입니다. 1083~1084행은 문서가 없을 때만 만들고, 1117행은 <code>/openapi.json</code>을 문서에서 뺍니다.</li><li>같은 판 <code>openapi/utils.py</code> 289~296행은 보안 객체를 찾아 칸 <code>security</code>를 적습니다. 457~470행은 매개변수나 요청 본문이 있을 때만 422를 적고, 573~575행은 보안 방식을 칸 <code>components</code>에 모읍니다. <code>utils.py</code> 95~100행은 <code>operationId</code>를 만듭니다.</li><li>실습 폴더에서는 <code>openapi.json</code>과 <code>openapitools.json</code>을 읽었습니다. 생성 SDK 파일 <code>DefaultApi.ts</code>는 머리 주석 7·10·12행과 요청 인자 37~82행을 읽었습니다. 같은 파일의 함수와 응답을 감싸는 줄은 134·140·184·190·221·227·272·278·322·328행입니다. 파일 <code>models/ChatRequest.ts</code>는 25·29·52·68행을 읽었습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 1절 파일 위치 셀은 01절 셀 글 그대로(「01절 2절과 같은 파일 위치 셀」 문장의 근거)
    assert FIND_LAB in AUTHOR01.read_text(encoding="utf-8"), "FIND_LAB이 01절 셀과 다릅니다"
    # 도구 파일은 가져오지도 쓰지도 않는다 — 06 판(author_06.TOOLS06) 그대로인지만 확인
    # (09절 판부터) 도구 파일은 06 판 뒤에 가져오기 줄 import json과 06절 함수 넷을 더한 판 — 가져오기 줄을 빼고 06 판으로 시작하는지 본다
    author_06.check_tools06()
    assert author_06.author_04.strip_later_imports(TOOLS_PATH.read_text(encoding="utf-8")).startswith(author_06.TOOLS06), "도구 파일이 06 판으로 시작하지 않습니다 — 손으로 확인하세요"
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "08", SLUG, "experiment", cells())
        print("wrote", path)
