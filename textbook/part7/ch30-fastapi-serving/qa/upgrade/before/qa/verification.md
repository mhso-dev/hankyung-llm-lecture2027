# Ch30 실행 검증

- 실행일: 2026-09-11
- 환경: Python 3.12.13, FastAPI 0.135.0, LangChain 1.4.0, LangGraph 1.2.11, OpenAPI Generator 7.25.0, Node 25.9.0

## 실제 결과

- 01절: 정상 본문은 200, 빈 문자열은 Pydantic 최소 길이 제약으로 422였습니다.
- 02절: 의존성 대체 중에는 `대체 응답`, 해제 뒤에는 실제 LangGraph 답을 받았습니다.
- 03절: 실제 `ainvoke` 결과에 messages와 answer가 있었고 교육용 오류 조건은 RuntimeError를 냈습니다.
- 04절: 실제 `astream(stream_mode="custom")` 조각을 결합해 최종 문장을 복원했습니다.
- 05절: POST SSE의 첫 이벤트는 token과 `sse-1:0`, 마지막 이벤트는 done이었습니다.
- 06절: `resume-1:0`을 Last-Event-ID로 보낸 뒤 첫 재개 ID는 `resume-1:1`이었습니다. 스트림 오류는 HTTP 200 안의 error 이벤트로 받았습니다.
- 07절: 인증 누락 401, 미허용 출처의 CORS 헤더 누락, 지연 Agent의 단일 응답 504와 스트림 error 이벤트를 확인했습니다.
- 08절: OpenAPI의 `/v1/chat` 요청과 응답이 ChatRequest와 ChatResponse를 참조했습니다.
- 09절: 실제 OpenAI Agent가 `lookup_library_hours`를 `day=월요일`로 호출했고 ToolMessage는 `09:00~18:00`이었습니다. JSON과 모델 token SSE를 결합한 답 모두 18:00을 포함했습니다.

## 자동 검증

- `execute.py`: 9개 노트북, 코드 셀 45개, 최대 14줄 통과.
- `verify.py --chapter`: 9개 절, 코드 셀 45개 통과.
- `pytest -q`: 6 passed. Starlette TestClient 내부의 anyio 별칭 DeprecationWarning 1건이 있습니다.
- OpenAPI Generator 7.25.0: SSE `itemSchema` 검증 경고 뒤 TypeScript fetch SDK 생성 완료.
- TypeScript `tsc --noEmit`: 생성 SDK, `stream.ts`, `test_stream.ts` 통과.
- 실제 TS fetch 클라이언트: normal 이벤트 token 5회 뒤 done, 첫 ID `web-01:0`, 재개 첫 ID `web-01:1`, 오류 요청 error 이벤트 확인.
- 화면: 1280px·390px의 10개 페이지에서 작은 글자, 대비, 잘림, 화면 밖 요소, SVG 경계, 가로 스크롤, 깨진 이미지, 복사 오류가 모두 0입니다.
- 도식: SVG·Excalidraw 9쌍을 동일 명세에서 생성했습니다.

## 해석 제한과 확인 필요 항목

OpenAPI Generator는 FastAPI 네이티브 SSE의 `itemSchema`를 아직 표준 속성으로 인정하지 않아 `--skip-validate-spec`가 필요했습니다. 생성된 일반 JSON SDK는 컴파일했으며 SSE 재연결은 직접 작성한 fetch 클라이언트로 실행했습니다. 실제 클라우드 프록시, 장시간 연결, 공급자 장애, 여러 인스턴스 사이 이벤트 재생은 확인하지 않았습니다. 한국어 최종 감사는 별도 모델이 완료했으며 Part 7 통합 검증 기록에서 판정을 확인할 수 있습니다. 실제 API 호출 비용은 1달러 미만으로 예상하며 키 값은 출력하지 않았습니다.

## 최종 경로 재검증

준비 셀은 현재·상위 폴더에서 `agent_service`가 있는 챕터를 찾고 작업 폴더를 설정합니다. 노트북 폴더에서 9개 모두 실제 새 커널로 다시 실행했으며 API 호출을 포함합니다. 최종 ZIP의 01절도 추출된 노트북 폴더에서 실행했습니다. 감사 완료 본문은 유지했습니다.
