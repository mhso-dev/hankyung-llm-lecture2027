# Ch30 FastAPI로 Agent 서빙

Python 3.12와 uv를 사용합니다. 01~08절의 결정적 LangGraph는 API 키 없이 전송 계약을 반복 검사합니다. 09절은 `.env`의 `OPENAI_API_KEY`를 읽어 LangChain 1.4 `create_agent`의 실제 모델·도구 `ainvoke`와 `astream`을 HTTP로 호출합니다. 교육용 토큰 기본값은 `local-demo-token`이며 운영 비밀값으로 사용하면 안 됩니다.

```bash
uv sync
uv run fastapi dev agent_service/app.py
uv run pytest
```

`POST /v1/chat/stream`은 네이티브 SSE를 사용합니다. 브라우저 `EventSource`는 POST 본문과 인증 헤더를 다루지 못하므로 `client/stream.ts`는 `fetch()` 응답 본문을 직접 읽고, 재연결할 때 마지막 `id`를 `Last-Event-ID` 헤더로 다시 보냅니다.

OpenAPI 문서는 `http://127.0.0.1:8000/docs`, 스키마는 `/openapi.json`에서 확인합니다. TypeScript SDK 생성 예시는 다음과 같습니다.

```bash
npx @openapitools/openapi-generator-cli generate --skip-validate-spec \
  -i http://127.0.0.1:8000/openapi.json \
  -g typescript-fetch \
  -o generated-sdk
```

OpenAPI Generator 7.25.0은 FastAPI 0.135의 SSE `itemSchema` 확장을 아직 검증하지 못하므로 경고를 기록하고 생성은 계속합니다. 생성 뒤에는 다음 명령으로 생성 SDK와 직접 작성한 스트림 클라이언트를 함께 검사합니다.

```bash
npx --package typescript@latest tsc --noEmit --target ES2022 \
  --moduleResolution bundler --module ESNext --allowImportingTsExtensions \
  client/generated/index.ts client/stream.ts client/test_stream.ts
npx tsx client/test_stream.ts
```
