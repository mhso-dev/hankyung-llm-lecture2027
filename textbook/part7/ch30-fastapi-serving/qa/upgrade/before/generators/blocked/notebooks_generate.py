from __future__ import annotations
# 2026-09-29 Ch 30 01절 품질 개선: 이 파일은 Ch 30 노트북 아홉을 출력 없는 옛 셀로 다시 쓰는 옛 생성기입니다.
# 개선본 노트북은 절마다 textbook/part7/ch30-fastapi-serving/qa/upgrade/author_NN.py가 씁니다. 이 파일을 실행하면 개선본을 옛 셀로 덮어쓰므로, 아래 줄에서 실행을 막습니다.
# 내용은 고치지 않았습니다(이 설명 세 줄과 아래 한 줄만 더함). 옮기기(mv -n)는 챕터 마감 몫입니다.
raise SystemExit('옛 Ch 30 노트북 생성기(notebooks/_generate.py)입니다. 실행하면 개선본 노트북을 옛 셀로 덮어씁니다. 개선본은 qa/upgrade/author_NN.py를 쓰세요.')

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def md(text: str, lesson_part: str | None = None) -> dict:
    metadata = {} if lesson_part is None else {"lesson_part": lesson_part}
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": text.splitlines(keepends=True)}


def code(text: str, lesson_part: str | None = None) -> dict:
    metadata = {} if lesson_part is None else {"lesson_part": lesson_part}
    return {
        "cell_type": "code", "execution_count": None, "id": "", "metadata": metadata,
        "outputs": [], "source": text.splitlines(keepends=True),
    }


COMMON = [
    md("## 실행 환경 준비\n\n현재 폴더나 상위 폴더에서 `labs/part7/ch30-fastapi-serving`을 찾아 작업 폴더로 사용합니다. 비밀 키를 출력하지 않습니다."),
    code("import os\nfrom pathlib import Path\nstart = Path.cwd().resolve()\nlab = next((p for p in (start, *start.parents)\n    if (p / 'agent_service').is_dir()), None)\nassert lab is not None, 'agent_service가 있는 Ch30 실습 폴더에서 실행하세요.'\nos.chdir(lab)\nprint('실습 폴더:', Path.cwd().name)"),
]


LESSONS: dict[str, tuple[str, str, list[dict]]] = {
    "01-비동기-라우팅과-스키마": (
        "비동기 라우팅과 Pydantic 스키마", "paired", [
            md("# 비동기 라우팅과 Pydantic 스키마\n\n요청 본문을 타입으로 선언하면 정상 입력과 잘못된 입력이 어떻게 나뉘는지 확인합니다."),
            *COMMON,
            md("## 기본 실행\n\n작은 FastAPI 앱에 `async def` 라우트와 Pydantic 요청 모델을 연결합니다."),
            code("from fastapi import FastAPI\nfrom fastapi.testclient import TestClient\nfrom pydantic import BaseModel, Field\n\nclass Question(BaseModel):\n    text: str = Field(min_length=1, max_length=20)\n\nmini = FastAPI()\n@mini.post('/ask')\nasync def ask(body: Question):\n    return {'length': len(body.text)}\n\nclient = TestClient(mini)"),
            md("## 정상 요청 관찰\n\nJSON 본문이 `Question` 객체로 변환된 뒤 길이가 반환됩니다."),
            code("ok = client.post('/ask', json={'text': '안녕하세요'})\nprint(ok.status_code, ok.json())\nassert ok.json() == {'length': 5}"),
            md("## 실패 재현\n\n빈 문자열은 응용 코드에 도달하기 전에 스키마 검증에서 거부됩니다.", "before"),
            code("bad = client.post('/ask', json={'text': ''})\nprint(bad.status_code, bad.json()['detail'][0]['type'])\nassert bad.status_code == 422", "before"),
            md("## 수정\n\n같은 요청에서 내용을 한 글자 이상 채우면 검증을 통과합니다.", "after"),
            code("fixed = client.post('/ask', json={'text': '확인'})\nprint(fixed.status_code, fixed.json())\nassert fixed.status_code == 200", "after"),
        ],
    ),
    "02-의존성으로-Agent-주입": (
        "의존성으로 Agent 주입", "paired", [
            md("# 의존성으로 Agent 주입\n\n`Depends`가 라우트와 Agent 생성 책임을 어떻게 분리하는지 확인합니다."), *COMMON,
            md("## 기본 실행\n\n운영 객체 대신 테스트 객체를 의존성 재정의 표에 넣습니다."),
            code("from fastapi.testclient import TestClient\nfrom agent_service.app import app, get_agent\n\nclass StubAgent:\n    async def ainvoke(self, state):\n        return {'answer': '대체 응답'}\n\napp.dependency_overrides[get_agent] = lambda: StubAgent()\nclient = TestClient(app)\nheaders = {'Authorization': 'Bearer local-demo-token'}"),
            md("## 대체 결과 관찰\n\n라우트 코드는 그대로인데 응답을 만드는 객체만 바뀝니다."),
            code("response = client.post('/v1/chat', headers=headers,\n    json={'question': '질문', 'thread_id': 'dep-1'})\nprint(response.json())\nassert response.json()['answer'] == '대체 응답'"),
            md("## 실패 재현\n\n재정의를 해제하지 않으면 다음 실험도 대체 객체를 사용합니다.", "before"),
            code("still_stub = client.post('/v1/chat', headers=headers,\n    json={'question': '다음 질문', 'thread_id': 'dep-2'})\nprint(still_stub.json()['answer'])\nassert still_stub.json()['answer'] == '대체 응답'", "before"),
            md("## 수정\n\n재정의 표를 비운 뒤 실제 LangGraph 객체가 다시 호출됩니다.", "after"),
            code("app.dependency_overrides.clear()\nreal = client.post('/v1/chat', headers=headers,\n    json={'question': '다음 질문', 'thread_id': 'dep-2'})\nprint(real.json()['answer'])\nassert real.json()['answer'].startswith('질문을 확인했습니다')", "after"),
        ],
    ),
    "03-ainvoke-요청-응답": (
        "ainvoke 요청 응답", "paired", [
            md("# ainvoke 요청 응답\n\nFastAPI 라우트 아래에서 호출되는 실제 LangGraph `ainvoke` 결과를 확인합니다."), *COMMON,
            md("## 기본 실행\n\n컴파일된 그래프에 메시지 상태를 비동기로 전달합니다."),
            code("from agent_service.agent import agent\nstate = {'messages': ['운영 시간을 알려 주세요']}\nresult = await agent.ainvoke(state)\nprint(result['answer'])\nassert '운영 시간을 알려 주세요' in result['answer']"),
            md("## 반환 상태 관찰\n\n최종 상태에는 입력 메시지와 노드가 만든 답이 함께 남습니다."),
            code("print(sorted(result))\nprint(result['messages'])\nassert sorted(result) == ['answer', 'messages']"),
            md("## 실패 재현\n\n서비스 규칙이 오류 문구를 만나면 호출 자체가 예외로 끝납니다.", "before"),
            code("try:\n    await agent.ainvoke({'messages': ['오류를 발생']})\nexcept RuntimeError as exc:\n    print(type(exc).__name__, str(exc))\n    failed = True\nassert failed", "before"),
            md("## 수정\n\nHTTP 스트림 계층에서는 이 예외를 `error` 이벤트로 바꿉니다. 여기서는 정상 질문으로 호출을 마칩니다.", "after"),
            code("fixed = await agent.ainvoke({'messages': ['정상 질문']})\nprint(fixed['answer'])\nassert fixed['answer'].endswith('정상 질문')", "after"),
        ],
    ),
    "04-astream과-응답-스트림": (
        "astream과 응답 스트림", "experiment", [
            md("# astream과 응답 스트림\n\n실제 LangGraph `astream`이 한 번의 최종 응답을 여러 사용자 정의 조각으로 전달하는지 관찰합니다."), *COMMON,
            md("## 스트림 수집\n\n`stream_mode='custom'`은 노드가 기록한 토큰 조각을 받습니다."),
            code("from agent_service.agent import agent\nchunks = []\nasync for chunk in agent.astream(\n    {'messages': ['세 단어 질문']}, stream_mode='custom'\n):\n    chunks.append(chunk['token'])\nprint(chunks)\nassert len(chunks) >= 4"),
            md("## 중간 결과 관찰\n\n마지막 조각을 기다리지 않아도 첫 조각을 먼저 처리할 수 있습니다."),
            code("first = chunks[0]\njoined = ''.join(chunks).strip()\nprint('첫 조각:', first)\nprint('전체:', joined)\nassert joined == '질문을 확인했습니다: 세 단어 질문'"),
            md("## 반복 실험과 결과 해석\n\n질문의 단어 수만 바꾸고 생성된 조각 수를 비교합니다."),
            code("counts = {}\nfor question in ['짧음', '두 단어', '세 개의 단어']:\n    count = 0\n    async for _ in agent.astream({'messages': [question]}, stream_mode='custom'):\n        count += 1\n    counts[question] = count\nprint(counts)\nassert counts['짧음'] < counts['세 개의 단어']"),
        ],
    ),
    "05-POST-SSE-이벤트-설계": (
        "POST SSE 이벤트 설계", "experiment", [
            md("# POST SSE 이벤트 설계\n\nPOST 본문으로 질문을 보내고 네이티브 SSE의 `event`, `id`, `data` 필드를 확인합니다."), *COMMON,
            md("## 기본 실행\n\nTestClient가 실제 ASGI 스트림을 끝까지 읽어 전송 형식을 보여 줍니다."),
            code("from fastapi.testclient import TestClient\nfrom agent_service.app import app\nclient = TestClient(app)\nheaders = {'Authorization': 'Bearer local-demo-token'}\nresponse = client.post('/v1/chat/stream', headers=headers,\n    json={'question': 'SSE 확인', 'thread_id': 'sse-1'})\nprint(response.status_code, response.headers['content-type'])\nassert response.status_code == 200"),
            md("## 이벤트 필드 관찰\n\n토큰 이벤트는 재연결 위치에 쓸 `id`를 갖고 완료 이벤트는 별도 타입입니다."),
            code("import re\nblocks = [b for b in re.split(r'\\r?\\n\\r?\\n', response.text) if b]\nprint(blocks[0])\nprint(blocks[-1])\nassert blocks[0].splitlines()[0] == 'event: token'\nassert 'id: sse-1:0' in blocks[0]\nassert blocks[-1].splitlines()[0] == 'event: done'"),
            md("## 반복 실험과 결과 해석\n\n문장 길이만 바꾸면 토큰 이벤트 수는 달라지지만 완료 이벤트는 한 번입니다."),
            code("for text in ['한', '두 단어']:\n    res = client.post('/v1/chat/stream', headers=headers,\n        json={'question': text, 'thread_id': 'count'})\n    token_count = res.text.count('event: token')\n    done_count = res.text.count('event: done')\n    print(text, token_count, done_count)\n    assert done_count == 1"),
        ],
    ),
    "06-fetch-재연결과-오류-이벤트": (
        "fetch 재연결과 오류 이벤트", "paired", [
            md("# fetch 재연결과 오류 이벤트\n\nPOST SSE에서 클라이언트가 마지막 이벤트 ID를 보관해 다시 보내고, 스트림 도중 오류를 이벤트로 받는 과정을 확인합니다."), *COMMON,
            md("## 기본 실행\n\n첫 요청의 `id`를 읽어 다음 요청의 `Last-Event-ID` 헤더로 보냅니다."),
            code("import re\nfrom fastapi.testclient import TestClient\nfrom agent_service.app import app\nclient = TestClient(app)\nauth = {'Authorization': 'Bearer local-demo-token'}\nbody = {'question': '재연결 확인 질문', 'thread_id': 'resume-1'}\nfirst = client.post('/v1/chat/stream', headers=auth, json=body)\nids = re.findall(r'id: ([^\\n]+)', first.text)\nprint(ids[:2])\nassert ids[0] == 'resume-1:0'"),
            md("## 재연결 위치 관찰\n\n두 번째 요청은 마지막으로 처리한 ID 다음 토큰부터 전달합니다."),
            code("resume_headers = {**auth, 'Last-Event-ID': ids[0]}\nresumed = client.post('/v1/chat/stream', headers=resume_headers, json=body)\nresumed_ids = re.findall(r'id: ([^\\n]+)', resumed.text)\nprint(resumed_ids[0])\nassert resumed_ids[0] == 'resume-1:1'"),
            md("## 실패 재현\n\n스트림이 이미 200으로 시작한 뒤 Agent가 실패합니다.", "before"),
            code("failed = client.post('/v1/chat/stream', headers=auth,\n    json={'question': '오류', 'thread_id': 'error-1'})\nprint(failed.status_code)\nprint(failed.text.strip())\nassert failed.status_code == 200", "before"),
            md("## 수정\n\n클라이언트는 HTTP 상태만 보지 않고 `event: error`와 오류 코드를 확인합니다.", "after"),
            code("has_error = 'event: error' in failed.text\nhas_code = 'stream_failed' in failed.text\nprint(has_error, has_code)\nassert has_error and has_code", "after"),
        ],
    ),
    "07-인증-CORS-타임아웃": (
        "인증 CORS 타임아웃", "paired", [
            md("# 인증 CORS 타임아웃\n\nBearer 인증, 브라우저 출처 허용, 응답 시간 상한을 각각 확인합니다."), *COMMON,
            md("## 기본 실행\n\n허용한 출처의 사전 요청과 올바른 인증 헤더를 보냅니다."),
            code("import asyncio\nfrom fastapi.testclient import TestClient\nfrom agent_service.app import app, get_agent, get_timeout\nclient = TestClient(app)\npreflight = client.options('/v1/chat', headers={\n    'Origin': 'http://localhost:5173',\n    'Access-Control-Request-Method': 'POST',\n    'Access-Control-Request-Headers': 'Authorization,Content-Type',\n})\nprint(preflight.status_code, preflight.headers['access-control-allow-origin'])\nassert preflight.status_code == 200"),
            md("## 인증 실패 관찰\n\n토큰이 없으면 Agent 호출 전에 401이 반환됩니다."),
            code("missing = client.post('/v1/chat',\n    json={'question': '질문', 'thread_id': 'auth-1'})\nprint(missing.status_code, missing.json())\nassert missing.status_code == 401"),
            md("## 시간 초과 관찰\n\n지연 Agent와 짧은 시간 상한을 주입해 단일 응답과 스트림의 차이를 확인합니다."),
            code("class SlowAgent:\n    async def ainvoke(self, state):\n        await asyncio.sleep(0.05)\n        return {'answer': '늦은 답'}\n    async def astream(self, state, stream_mode):\n        await asyncio.sleep(0.05)\n        yield {'token': '늦은 답'}\n\napp.dependency_overrides[get_agent] = lambda: SlowAgent()\napp.dependency_overrides[get_timeout] = lambda: 0.01\nheaders = {'Authorization': 'Bearer local-demo-token'}"),
            code("single_timeout = client.post('/v1/chat', headers=headers,\n    json={'question': '질문', 'thread_id': 'slow-1'})\nstream_timeout = client.post('/v1/chat/stream', headers=headers,\n    json={'question': '질문', 'thread_id': 'slow-2'})\nprint(single_timeout.status_code, 'event: error' in stream_timeout.text)\nassert single_timeout.status_code == 504\nassert stream_timeout.status_code == 200\nassert 'event: error' in stream_timeout.text\napp.dependency_overrides.clear()"),
            md("## 실패 재현\n\n허용 목록에 없는 출처는 CORS 허용 헤더를 받지 못합니다.", "before"),
            code("blocked = client.options('/v1/chat', headers={\n    'Origin': 'https://unknown.example',\n    'Access-Control-Request-Method': 'POST',\n})\nprint(blocked.status_code, blocked.headers.get('access-control-allow-origin'))\nassert 'access-control-allow-origin' not in blocked.headers", "before"),
            md("## 수정\n\n정확한 출처와 인증 헤더를 함께 보내면 요청이 성공합니다. 운영에서는 환경별 허용 목록을 관리합니다.", "after"),
            code("ok = client.post('/v1/chat',\n    headers={'Authorization': 'Bearer local-demo-token'},\n    json={'question': '질문', 'thread_id': 'auth-1'})\nprint(ok.status_code, ok.json()['answer'])\nassert ok.status_code == 200", "after"),
        ],
    ),
    "08-OpenAPI와-TS-SDK": (
        "OpenAPI와 TS SDK", "experiment", [
            md("# OpenAPI와 TS SDK\n\nPydantic과 FastAPI 선언이 OpenAPI 스키마가 되고 TypeScript 클라이언트 생성 입력이 되는 과정을 확인합니다."), *COMMON,
            md("## 스키마 생성\n\n서버 프로세스를 시작하지 않아도 앱 객체에서 같은 OpenAPI 문서를 얻을 수 있습니다."),
            code("import json\nfrom agent_service.app import app\nschema = app.openapi()\npath = Path('openapi.json')\npath.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding='utf-8')\nprint(schema['openapi'], len(schema['paths']))\nassert '/v1/chat' in schema['paths']"),
            md("## 타입과 보안 정보 관찰\n\n요청 스키마의 필수 필드와 응답 타입이 계약 문서에 포함됩니다."),
            code("chat = schema['paths']['/v1/chat']['post']\nrequest_ref = chat['requestBody']['content']['application/json']['schema']['$ref']\nresponse_ref = chat['responses']['200']['content']['application/json']['schema']['$ref']\nprint(request_ref, response_ref)\nassert request_ref.endswith('/ChatRequest')\nassert response_ref.endswith('/ChatResponse')"),
            md("## 반복 실험과 결과 해석\n\n같은 앱에서 두 번 생성한 스키마를 정렬해 직렬화하면 같은 결과가 나옵니다."),
            code("first = json.dumps(app.openapi(), sort_keys=True)\nsecond = json.dumps(app.openapi(), sort_keys=True)\nprint('동일:', first == second, '문자 수:', len(first))\nassert first == second\nprint('SDK 생성 입력:', path.resolve())"),
        ],
    ),
    "09-실제-Agent-HTTP-통합": (
        "실제 Agent HTTP 통합", "experiment", [
            md("# 실제 Agent HTTP 통합\n\nOpenAI 모델과 조회 도구가 있는 LangChain `create_agent`를 FastAPI에서 실제 호출합니다."), *COMMON,
            md("## 키 존재 확인\n\n상위 폴더의 `.env`를 읽고 키 값은 출력하지 않습니다."),
            code("import os\nfrom dotenv import find_dotenv, load_dotenv\nload_dotenv(find_dotenv(usecwd=True))\nhas_key = bool(os.getenv('OPENAI_API_KEY'))\nprint('OPENAI_API_KEY 설정:', has_key)\nassert has_key"),
            md("## 실제 ainvoke HTTP 요청\n\nAgent는 운영 시간을 도구로 확인한 뒤 한 문장으로 답합니다."),
            code("from fastapi.testclient import TestClient\nfrom agent_service.app import app\nclient = TestClient(app)\nheaders = {'Authorization': 'Bearer local-demo-token'}\nbody = {'question': '한빛도서관 월요일 운영 시간은?', 'thread_id': 'live-1'}\nresponse = client.post('/v1/chat/live', headers=headers, json=body)\nprint(response.status_code, response.json()['answer'])\nassert response.status_code == 200\nassert '18:00' in response.json()['answer']"),
            md("## 도구 호출 궤적 확인\n\n같은 실제 Agent의 메시지에서 도구 이름, 입력, 도구 출력을 확인합니다."),
            code("from langchain_core.messages import ToolMessage\nfrom agent_service.live_agent import build_live_agent\nlive_agent = build_live_agent()\ntrace = await live_agent.ainvoke({'messages': [\n    {'role': 'user', 'content': body['question']}\n]})\ntool_call = next(call for message in trace['messages']\n    for call in getattr(message, 'tool_calls', [])\n    if call['name'] == 'lookup_library_hours')\ntool_result = next(message for message in trace['messages']\n    if isinstance(message, ToolMessage))\nprint(tool_call['name'], tool_call['args'], tool_result.content)\nassert tool_call['args']['day'] == '월요일'\nassert tool_result.content == '09:00~18:00'"),
            md("## 실제 astream HTTP 요청\n\n같은 Agent의 모델 메시지 청크를 SSE token 이벤트로 받습니다."),
            code("import json, re\nstream = client.post('/v1/chat/live/stream', headers=headers, json=body)\nblocks = [b for b in re.split(r'\\r?\\n\\r?\\n', stream.text) if b]\ntokens = []\nfor block in blocks:\n    if block.startswith('event: token'):\n        data_line = next(line for line in block.splitlines() if line.startswith('data: '))\n        tokens.append(json.loads(data_line[6:])['token'])\nlive_answer = ''.join(tokens)\nprint(stream.status_code, live_answer)\nassert stream.status_code == 200\nassert blocks[-1].startswith('event: done')\nassert '18:00' in live_answer"),
            md("## 실험 결과 해석\n\n결정적 그래프와 실제 모델 Agent의 출력 성질을 구분합니다."),
            code("token_events = stream.text.count('event: token')\nprint('실제 모델 token 이벤트:', token_events)\nprint('결정적 그래프가 아닌 create_agent 호출: True')\nassert token_events > 0"),
        ],
    ),
}


for slug, (title, lesson_format, cells) in LESSONS.items():
    for index, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{index:02d}"
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": lesson_format,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (HERE / f"{slug}.ipynb").write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print("wrote", title)
