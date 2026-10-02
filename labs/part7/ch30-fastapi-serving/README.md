# Ch 30 FastAPI로 Agent 서빙 실습

이 폴더는 에이전트를 웹 앱으로 내보내는 방법을 배우는 실습 폴더입니다. 노트북 열 개(`notebooks/01~10-*.ipynb`)는 Python 3.12 새 커널에서 절마다 따로 실행할 수 있고, 앞 절 노트북의 변수는 쓰지 않습니다. 노트북은 서버 프로그램을 띄우지 않고, 같은 노트북 안의 시험용 클라이언트(`TestClient`)로 앱에 요청을 보냅니다. 노트북은 실습 폴더의 파일을 가져오고 읽기만 하며, 쓰는 파일은 없습니다.

## 준비

실습 폴더(`labs/part7/ch30-fastapi-serving`)에서 `uv sync --locked`를 실행하고, 이 폴더의 `.venv` 커널을 고릅니다. 그다음 `notebooks/` 폴더의 노트북을 열어 첫 셀부터 차례로 실행합니다. VS Code와 Jupyter는 노트북이 있는 폴더에서 커널을 시작합니다.

노트북의 파일 위치 셀은 `notebooks/` 폴더, 실습 폴더 맨 위, 프로젝트 맨 위 세 자리에서 실습 폴더를 찾아 앱 패키지 `agent_service/`를 가져옵니다. 다만 04·06·07·09·10절은 파일 위치 셀보다 앞에서 도구 파일 `notebooks/serve_tools.py`를 가져옵니다. 이 다섯 절은 커널이 `notebooks/` 폴더에서 시작해야 하고, 다른 자리에서 시작하면 도구 파일을 가져오는 셀이 `ModuleNotFoundError`로 멈춥니다.

노트북의 첫 코드 셀은 그 절에서 쓰는 패키지를 설치하고 판 번호를 출력합니다. 모두 실습 폴더 잠금(`uv.lock`)과 같은 판입니다.

- 01절은 `fastapi` 0.135.0, `httpx` 0.28.1, `pydantic` 2.12.5, `starlette` 1.6.0 넷을 설치합니다.
- 02~08절과 10절은 그 넷에 실습 앱 파일이 가져오는 `langgraph` 1.2.11과 `langchain` 1.4.0을 더합니다.
- 09절은 여섯에 모델을 부르는 `langchain-openai` 1.6.0과 키를 읽는 `python-dotenv` 1.2.1을 더합니다.

## 노트북 열 개와 모델 요청

| 절 | 노트북 | 하는 일 | 모델 요청 |
|---|---|---|---|
| 01 | `01-비동기-라우팅과-스키마.ipynb` | 입력 형식과 응답 형식을 적은 처리 함수와 적지 않은 처리 함수에 빈 질문을 보내 견줍니다 | 0번 |
| 02 | `02-의존성으로-Agent-주입.ipynb` | 의존성과 제공 함수를 보고, 재정의가 다음 질문까지 남는 실패와 `clear()`로 비우는 모습을 봅니다 | 0번 |
| 03 | `03-ainvoke-요청-응답.ipynb` | 비동기 노드 그래프를 동기 `invoke`로 부른 오류와, `await`로 기다리는 `ainvoke`를 봅니다 | 0번 |
| 04 | `04-astream과-응답-스트림.ipynb` | `astream`과 `async for`로 스트림 사건을 받아 이어 붙이고, 모드 목록 하나만 바꿔 봅니다 | 0번 |
| 05 | `05-POST-SSE-이벤트-설계.ipynb` | 요청 주소 `/v1/chat/stream`의 SSE 사건을 칸으로 나눠 읽고, `response_class`를 뺀 응답과 견줍니다 | 0번 |
| 06 | `06-fetch-재연결과-오류-이벤트.ipynb` | 요청 머리 `Last-Event-ID`로 이어 받고, 오류 사건과 마지막 사건을 본 판정을 봅니다 | 0번 |
| 07 | `07-인증-CORS-타임아웃.ipynb` | 사전 요청과 허용 출처, 접근 토큰 검사의 401, 시간 제한 0초의 504를 봅니다 | 0번 |
| 08 | `08-OpenAPI와-TS-SDK.ipynb` | 앱 객체가 만든 응답 문서를 `openapi.json`과 견주고, 생성 SDK의 함수를 읽습니다 | 0번 |
| 09 | `09-실제-Agent-HTTP-통합.ipynb` | 실제 모델과 도구를 쓰는 에이전트를 `/v1/chat/live`와 `/v1/chat/live/stream`으로 부릅니다 | 6번 |
| 10 | `10-FastAPI-서빙-실습.ipynb` | 챕터 끝 실습 절입니다(아래) | 0번 |

01~08절과 10절은 모델을 부르지 않아 API 키 없이 실행합니다. 이 절들의 실습 앱은 모델을 쓰지 않는 그래프로, 질문 앞에 정해 둔 말을 붙여 답합니다. 그래서 상태 코드와 사건 번호 같은 값이 실행할 때마다 같습니다.

09절만 과정 표준 모델(`gpt-5.4-mini`, temperature 0, `reasoning_effort="none"`)에 요청을 보내므로 키가 있어야 합니다. 에이전트를 세 번 실행하고, 에이전트가 도구를 한 번씩 부르면 실행마다 요청이 두 번 나가 모두 여섯 번입니다. 과정 요금표(2026-09-17)로 어림한 예상 비용은 0.002달러보다 적습니다. 예상 비용은 요금표로 셈한 값이고, 청구 금액이 아닙니다. 모델이 쓰는 답 글은 실행마다 달라질 수 있습니다.

API 키는 `.env` 파일의 `OPENAI_API_KEY`에서만 읽습니다. 09절 노트북은 커널이 시작한 폴더에서 위로 올라가며 처음 찾은 `.env` 파일을 읽습니다. 그래서 키는 프로젝트 맨 위(학생 묶음이면 `part7-practice/`)의 `.env`에 적어 둡니다. 노트북은 키가 있는지만 확인하고, 키 값은 출력하거나 파일에 저장하지 않습니다. 키가 없으면 키를 확인하는 셀에서 멈추고, 모델 요청은 나가지 않습니다.

## 실습 폴더의 파일

- `agent_service/` — 노트북이 가져오는 앱 패키지입니다. `app.py`는 앱 객체와 처리 함수가 있는 파일이고, 요청 주소 다섯(`GET /health`, `POST /v1/chat`, `POST /v1/chat/stream`, `POST /v1/chat/live`, `POST /v1/chat/live/stream`)을 받습니다. `schemas.py`는 입력 형식과 응답 형식의 양식 클래스, `agent.py`는 모델을 쓰지 않는 그래프입니다. `live_agent.py`는 09절이 쓰는 실제 모델 에이전트와 도구 하나입니다.
- `tests/test_app.py` — 앱을 시험하는 파일입니다. 실습 폴더에서 `uv run pytest -q`로 실행하고, 교재를 만들 때 여섯 시험이 모두 통과했습니다.
- `openapi.json` — 앱 객체가 만든 응답 문서(OpenAPI 문서)입니다. 08절에서 `app.openapi()`로 새로 만든 글과 이 파일의 글이 같은지 견줍니다.
- `client/stream.ts`·`client/test_stream.ts` — 함수 `fetch`로 SSE 응답을 읽고 이어 받는 TypeScript 코드와 그 시험 파일입니다. 06절에서 글로 읽습니다.
- `client/generated/` — 응답 문서로 만든 생성 SDK입니다. TS 파일 열하나와 설명 문서 일곱이 있고, 08절에서 읽습니다.

교재용 접근 토큰 `local-demo-token`은 환경 변수 `DEMO_API_TOKEN`이 없을 때 앱이 쓰는 교재용 값입니다. 실제 서비스의 비밀 값으로 쓰지 않습니다. 요청 머리 `Authorization`에 `Bearer local-demo-token`을 실어 보냅니다.

## 노트북 밖에서 서버를 띄우고 TS 시험하기

노트북은 서버를 띄우지 않습니다. 브라우저나 TypeScript 코드로 앱을 부르려면, 실습 폴더에서 아래 명령으로 서버를 이 컴퓨터 안(`127.0.0.1`)에만 띄웁니다.

```bash
uv run uvicorn agent_service.app:app --host 127.0.0.1 --port 8000
```

응답 문서 화면은 `http://127.0.0.1:8000/docs`에서 볼 수 있습니다. 서버는 창에서 Ctrl+C로 끝냅니다. 요청 주소 `/v1/chat/live`와 `/v1/chat/live/stream`을 서버로 부르는 일은 교재에서 실행하지 않았습니다.

서버를 띄운 채로 다른 창의 실습 폴더에서 TS 시험 파일을 실행합니다. Node.js 22가 TS 파일을 바로 읽는 기능을 써서, npm으로 설치할 것은 없습니다.

```bash
node client/test_stream.ts
```

교재를 만들 때 Node.js 22.23.2로 이 명령을 실행해 통과했습니다. 시험 파일은 질문에 「오류」가 들어 있으면 그래프가 일부러 예외를 일으키는 경우도 확인합니다. 그래서 서버 창에 오류 기록이 한 번 나오는 것은 정상입니다.

## 생성 SDK를 다시 만들고 TS 코드 검사하기

생성 SDK는 노트북 밖에서 OpenAPI Generator로 만듭니다. 생성기는 Java 프로그램이라 Java 11 이상이 있어야 하고, 교재를 만들 때는 OpenJDK 11.0.32.1을 썼습니다. 아래 첫 명령은 `openapi.json`을 읽어 `client/generated/`에 생성 SDK를 다시 쓰고, 둘째 명령은 방금 만든 그 폴더의 코드와 직접 적은 스트림 코드를 함께 검사합니다.

```bash
npx @openapitools/openapi-generator-cli generate --skip-validate-spec \
  -i openapi.json \
  -g typescript-fetch \
  -o client/generated
npx --package typescript@7.0.2 tsc --noEmit --target ES2022 \
  --moduleResolution bundler --module ESNext --allowImportingTsExtensions \
  client/generated/index.ts client/stream.ts client/test_stream.ts
```

- 생성기 판은 `openapitools.json`이 7.25.0으로 고정합니다. 이 판을 감싸 부르는 npm 패키지 `@openapitools/openapi-generator-cli`의 판은 고정하지 않았고, 교재를 만들 때는 2.41.0이었습니다.
- 생성기는 SSE 요청 주소 둘의 `itemSchema`가 뜻밖의 칸이라는 경고를 두 줄 적고, `--skip-validate-spec` 덕분에 끝까지 만듭니다. 교재를 만들 때 같은 폴더에 다시 만들자, 지금 `client/generated/`의 파일과 글자까지 같았습니다.
- 생성기는 목록 파일이 든 폴더 `client/generated/.openapi-generator/`도 씁니다. 이 폴더는 학생 묶음에 넣지 않았습니다.
- TS 검사는 `typescript` 판 7.0.2를 적어 둡니다. 교재를 만들 때(2026-09-29) 최신 판을 받아 실행하자 판이 7.0.2였고, 오류 없이 끝났습니다. 다른 판에서는 실행하지 않았습니다.
- 생성 SDK는 가져오는 줄에 파일 확장자를 적지 않아, Node.js가 `client/generated/index.ts`를 바로 읽지는 못합니다. 위 `tsc` 검사로 코드 모양만 봅니다.

## 도구 파일 `notebooks/serve_tools.py`

앞에서 배운 함수는 `serve_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일이고, 04·06·07·09·10절 노트북이 `from serve_tools import …` 한 줄로 가져옵니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

함수 열두 개마다 어느 절에서 배웠는지 바로 위 주석에 적었습니다. 함수를 처음 가르치는 절은 노트북 안에 함수를 적고 설명하며, 다음 절부터 이 파일에서 가져옵니다. 함수는 노트북에서 만든 이름을 바로 읽지 않고, 필요한 값을 모두 인자로 받습니다. 이 파일은 표준 라이브러리 `json`만 가져오므로, 따로 설치할 패키지는 없습니다.

- `positions_of` — Ch 25 01절에서 배웠습니다. 사건 목록에서 한 모드의 사건이 몇 번째에 나왔는지 모읍니다. 04절이 가져옵니다.
- `mode_order` — Ch 25 02절에서 배웠습니다. 사건 목록에서 모드가 바뀐 차례를 모읍니다. 04절이 가져옵니다.
- `zero_timeout` — 이 챕터 02절에서 배웠습니다. 시험용으로 시간 제한 0초를 내놓는 비동기 함수입니다. 06·07절이 가져옵니다.
- `join_tokens` — 이 챕터 04절에서 배웠습니다. 진행 값 목록에서 칸 `token`의 글을 차례대로 이어 붙입니다. 06·09·10절이 가져옵니다.
- `split_sse` — 이 챕터 05절에서 배웠습니다. 본문 글을 빈 줄로 나눠 SSE 사건 글의 목록을 만듭니다. 06절이 가져옵니다.
- `parse_sse` — 이 챕터 05절에서 배웠습니다. SSE 사건 글 하나를 칸 이름과 값의 딕셔너리로 바꿉니다. 06절이 가져옵니다.
- `read_events` — 이 챕터 06절에서 배웠습니다. 응답 본문 글을 SSE 사건마다 칸 딕셔너리로 바꾼 목록을 만듭니다. 09·10절이 가져옵니다.
- `event_names` — 이 챕터 06절에서 배웠습니다. 사건마다 칸 `event`의 사건 이름을 모읍니다. 09·10절이 가져옵니다.
- `token_values` — 이 챕터 06절에서 배웠습니다. `token` 사건만 골라 칸 `data`의 JSON 글을 읽은 값을 모읍니다. 09·10절이 가져옵니다.
- `ended_with_done` — 이 챕터 06절에서 배웠습니다. 마지막 사건의 이름이 `done`인지 봅니다. 09·10절이 가져옵니다.
- `last_event_id` — 이 챕터 06절에서 배웠습니다. 칸 `id`가 있는 마지막 사건의 번호를 내놓고, 없으면 `None`을 내놓습니다. 10절이 가져옵니다.
- `header_or_none` — 이 챕터 07절에서 배웠습니다. 응답 머리에서 이름이 같은 칸의 값을 내놓고, 없으면 `None`을 내놓습니다. 10절이 가져옵니다.

앞 챕터 도구 파일(Ch 25 `stream_tools.py`)은 이 실습 폴더와 잠금이 달라, 파일째 가져오지 않고 이 챕터 노트북이 쓰는 함수 둘만 옮겼습니다.

## 10절 실습 — 끊긴 SSE 응답을 이어 받는 흐름에서 접근 토큰 하나만 바꾸기

노트북 `notebooks/10-FastAPI-서빙-실습.ipynb`는 챕터 끝 실습 절입니다. 30분 안팎의 분량이고, 따로 내는 과제와 새 문법은 없습니다. 05~07절에서 배운 사전 요청·SSE 응답·이어 받기를 도서관 웹 화면의 질문 하나에 한 요청 흐름으로 잇습니다.

실행 1은 교재용 접근 토큰으로 흐름을 끝까지 실행하고, 실행 2는 접근 토큰 하나만 틀리게 바꿔 두 실행의 단계 기록을 견줍니다. 모델을 부르지 않아 API 키가 필요 없고, 모델 요청은 0번입니다. 도구 파일에서 함수 일곱(`ended_with_done`·`event_names`·`header_or_none`·`join_tokens`·`last_event_id`·`read_events`·`token_values`)을 가져옵니다. 쓰는 파일은 없습니다.

## 교재 출력 환경

교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다. 노트북은 걸린 시간을 재지 않았고, 파일을 쓰지 않습니다.
