# Part 7 개념 학습 순서 개정 기록

담당 범위: Ch30~34의 교재 원본 29절과 대응 노트북 29개  
개정일: 2026-09-14  
코드 변경: 없음. 노트북의 기존 코드 셀·출력·실행 번호·상위 메타데이터를 보존하고 마크다운 셀만 추가했습니다.

## 적용 기준

각 준비 코드 바로 앞에는 작업 폴더 탐색, 패키지 설치, 환경 변수, `subprocess.run` 보조 함수가 무엇을 준비하고 반환하는지 설명했습니다. 핵심 API 설명은 실제 대상 코드 바로 앞으로 옮겼고, 비교·관찰 범위는 해당 결과를 만드는 뒤쪽 코드 바로 앞으로 나눴습니다. 같은 개념을 HTML 핵심 개념에도 통합했습니다. 절마다 다른 상황과 가까운 개념의 경계를 다뤘으며, 비용 설명은 Ch34의 원래 학습 목표 범위에서만 유지했습니다.

## 독립 검토 P7-01~09 반영

- P7-01: 29개 노트북의 앞부분에 몰려 있던 설명을 준비·핵심 실행·경계 해석으로 분할했습니다. 새 설명 셀 93개는 모두 설명 대상 코드 바로 앞에 있습니다.
- P7-02: Ch30-02 노트북에 실제 `AgentDep = Annotated[object, Depends(get_agent)]` 선언과 `runtime: AgentDep` 라우트 매개변수를 인용하고, 아래 코드는 제공자 재정의임을 연결했습니다.
- P7-03: Ch30-07의 OPTIONS 사전 요청 200은 CORSMiddleware 단계, 실제 POST 401은 인증 의존성 단계임을 HTML과 노트북에서 분리했습니다.
- P7-04: Ch32-01에서 `RUN`·`COPY`·`ADD`의 파일 시스템 레이어와 `CMD`·`HEALTHCHECK`의 0B 메타데이터 기록을 구분했습니다.
- P7-05: Ch32-05는 HTTP 상태와 Compose health 표시까지만 관찰하며, 재시작·트래픽 제외는 오케스트레이터의 별도 정책이 필요하다고 한정했습니다.
- P7-06: Ch33 다섯 절의 공항 수하물 비유, 공통 선수 문단, 도식 안내, 출력 확인 문장을 제거했습니다. 생산선 검사, 승인 견본 비교, 진열 이름과 로컬 물품 번호, 연속 발열, 이전 조리법 복구의 서로 다른 사례로 다시 썼습니다.
- P7-07: Ch33-03의 로컬 이미지 ID, 레지스트리 manifest digest, 다중 플랫폼 매니페스트의 적용 범위를 구분했습니다. 교육용 JSON의 `digest` 필드가 실제로는 로컬 이미지 ID를 담는다고 명시했습니다.
- P7-08: Ch31 다섯 절의 목표·실행 설명·확인 문장을 실제 출력에 맞게 모두 다시 썼습니다. 그래프 스레드 재개처럼 실행하지 않은 범위도 분리했습니다.
- P7-09: Ch30-09의 근거 없는 1달러 미만 문장을 삭제하고, 실제 호출 횟수와 사용량을 기록하되 임의 비용을 추정하지 않는 주의로 바꿨습니다.

| 절 | 첫 사용과 코드 읽기 보정 | 다른 상황·비교·해석 |
| --- | --- | --- |
| Ch30-01 | `BaseModel`, `Field`, 경로 장식자, `TestClient.post`의 입력과 실행 시점 | 422 입력 오류와 500 실행 오류, 본문·쿼리·헤더 검증 위치 |
| Ch30-02 | `Depends`와 `dependency_overrides`가 제공자를 해결·교체하는 과정 | 공유 객체와 요청별 자원, 대체 객체 검사와 실제 Agent 품질 검사 |
| Ch30-03 | `await agent.ainvoke(state)`의 상태 입력·최종 사전 반환·화면 출력 | 단일 응답과 스트리밍, 내부 예외 로그와 공개 오류 응답 |
| Ch30-04 | `astream`이 비동기 반복자를 반환하고 `async for`가 조각을 소비하는 과정 | 모델 생성 스트림과 파일 스트림, 첫 조각·전체 시간·취소 경계 |
| Ch30-05 | SSE의 `event`·`id`·`data`와 빈 줄 사건 경계 | token·done·도구 사건 분리, 재연결 ID와 업무 ID 구분 |
| Ch30-06 | `Last-Event-ID`로 이어받을 위치를 전달하고 다음 사건을 읽는 과정 | 재계산 재개와 영구 재생 구분, HTTP 200 안의 오류 사건 |
| Ch30-07 | 인증·CORS·timeout의 서로 다른 입력과 결과 | 브라우저 CORS와 서버 인증, 계층별 timeout과 취소 전달 |
| Ch30-08 | `app.openapi()`의 `paths`·`$ref`와 SDK 생성 입력 | 현재 프로세스 결정성 검사와 배포 간 하위 호환성 검사 |
| Ch30-09 | 실제 HTTP 요청, 도구 호출 궤적, `ToolMessage`, SSE JSON 조립 | 답 문자열·도구 인수·도구 결과·완료 사건을 독립 관찰 |
| Ch31-01 | `create_async_engine`, `async_sessionmaker`, `execute`, `scalar_one` | 동시 작업별 세션 분리와 `pg_sleep` 시간 관찰의 한계 |
| Ch31-02 | `engine.begin()` 블록의 정상 커밋·예외 롤백 | 원자성과 잔액 규칙·중복 처리·격리 수준의 차이 |
| Ch31-03 | Alembic `upgrade`·`downgrade`, `check=True`, `to_regclass` | 코드 롤백과 스키마 롤백, 확장-이행-축소 경계 |
| Ch31-04 | `pool_size`, `max_overflow`, `pool_timeout`, 연결 반환 | 인스턴스 수와 총 연결 수, 느린 쿼리와 풀 고갈 구분 |
| Ch31-05 | pgvector 데이터·HNSW 인덱스·체크포인터 표의 역할 | 인덱스 존재와 실행 계획 사용, 백업 포함과 복원 성공 구분 |
| Ch32-01 | Dockerfile 레이어, 이미지, 컨테이너, `build`와 `run` | 컨테이너 쓰기 층과 영속 볼륨, 이미지 재빌드 경계 |
| Ch32-02 | 여러 `FROM`, `AS builder`, `COPY --from`의 처리 | 빌드 도구 제거와 디버깅, 단계 간 플랫폼 호환성 |
| Ch32-03 | 캐시 적중 조건과 하위 레이어 무효화 | 캐시 적중 수와 이미지 크기, `--no-cache`와 `--pull` |
| Ch32-04 | Compose 서비스 이름·네트워크·의존·healthcheck | 시작 순서와 업무 준비 상태, `down`과 `--volumes` |
| Ch32-05 | 환경변수와 파일 마운트 secret의 입력 방식 | liveness와 readiness, 재시작·트래픽 제외·로그 비밀값 |
| Ch33-01 | CI가 명령의 종료 코드를 읽는 과정 | 테스트·린트·빌드의 책임, 검증 산출물과 배포 산출물 일치 |
| Ch33-02 | 기준선·현재 결과와 회귀 검사 종료 코드 | 승인된 비교점 갱신, 평균과 중요 사례별 하한 |
| Ch33-03 | 이동 가능한 태그와 내용 식별 다이제스트 | 내용 고정과 제작자 신뢰·취약점 검사·배포 승인 |
| Ch33-04 | 오류율과 p95를 계산해 복합 경보를 만드는 과정 | 임계값 지속 시간·최소 요청 수·복구 조건 |
| Ch33-05 | 이전 다이제스트 활성화와 복구 검증 | 코드 롤백과 데이터·외부 부작용 복구의 차이 |
| Ch34-01 | 공통 접두어, `usage_metadata`, 캐시 읽기 토큰 | 의미 유사성과 토큰 접두어 일치, 캐시 적중과 답 품질 |
| Ch34-02 | JSONL 한 줄 한 객체와 `custom_id` 연결 | 즉시 요청과 비동기 Batch, 부분 실패 재처리 |
| Ch34-03 | 비교 실행 뒤 `route`가 모델 이름을 반환하는 과정 | 길이 휴리스틱의 한계, 위험·도구·폴백 신호 |
| Ch34-04 | `Queue`, `Semaphore`, `task_done`, 429 재시도 | 재시도 가능한 오류와 영구 오류, 전체 시간·횟수 한도 |
| Ch34-05 | 대화별 집계, 최근접 순위 p95, 사전 예산 가드 | 사후 분포와 사전 차단의 시점, 예상 최대값의 보정 |

## 참고 자료와 버전 대조

참고 노트북은 다음 두 개를 정독했습니다.

- `/Users/mhso/working/lecture/llm/langchain-llm/02_langchain-basics/04_Memory/09-Memory-using-SQLite.ipynb`: 비유 뒤 정의, 인메모리와 영구 저장 비교, 세션별 다른 상황 전개를 확인했습니다.
- `/Users/mhso/working/lecture/llm/langchain-llm/02_langchain-basics/06_RAG/6-3_Embeddings/01-OpenAI-and-Cache-Embeddings.ipynb`: 메서드별 입력·사용 시점, 비교 표, 캐시 경계 설명 방식을 확인했습니다. 비용 수치나 강의 지시는 가져오지 않았습니다.

기술 주장은 기존 절의 공식 문서 링크와 2026-09-14에 다시 확인한 공식 자료를 대조했습니다.

- FastAPI: https://fastapi.tiangolo.com/tutorial/dependencies/ · https://fastapi.tiangolo.com/advanced/custom-response/ · https://fastapi.tiangolo.com/tutorial/cors/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html · https://docs.sqlalchemy.org/en/20/core/pooling.html · https://docs.sqlalchemy.org/en/20/orm/session_basics.html
- Docker: https://docs.docker.com/build/building/multi-stage/ · https://docs.docker.com/build/cache/optimize/ · https://docs.docker.com/compose/how-tos/use-secrets/
- GitHub Actions: https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments
- OpenAI Batch: https://platform.openai.com/docs/api-reference/batch/object?api-mode=responses

고정된 실습 패키지와 코드는 업그레이드하지 않았습니다. SQLAlchemy 공식 최신 문서가 2.0 계열임을 확인했고, 교재의 고정 2.0.43 코드는 그대로 유지했습니다. OpenAI Batch 제출은 기존 실습과 마찬가지로 실행하지 않았습니다.

## 검증

- 원본 스냅샷 대조: HTML `_src` 29/29 변경, 노트북 마크다운 29/29 변경.
- 코드·출력 보존: 29개 노트북의 코드 소스, 실행 번호, 코드 셀 메타데이터, 출력 JSON이 개정 전 스냅샷과 모두 같습니다.
- 설명 위치: 준비·핵심·경계 설명 셀 93개가 모두 설명 대상 코드 셀 바로 앞에 있는지 구조 검사했습니다.
- Ch30 빌드·공통 검증: 9절, 코드 셀 45개, 최대 14줄 PASS.
- Ch31 빌드·공통 검증: 5절, 코드 셀 27개, 최대 25줄 PASS.
- Ch32 빌드·공통 검증: 5절, 코드 셀 23개, 최대 13줄 PASS.
- Ch33 빌드·공통 검증: 5절, 코드 셀 20개, 최대 12줄 PASS.
- Ch34 빌드·공통 검증: 5절, 코드 셀 26개, 최대 19줄 PASS.
- 기존 테스트: Ch30 6개 PASS, Ch33 5개 PASS.
- 첫 테스트 실행은 저장소 루트에서 pytest 수집 범위가 넓어져 다른 파트의 선택 의존성 오류로 실패했습니다. 각 장 실습 폴더를 작업 경로로 지정해 대상 테스트만 다시 실행했고 모두 통과했습니다.
- 코드 셀은 변경하지 않았으므로 외부 모델 호출·Docker·PostgreSQL을 다시 실행하지 않았습니다. 기존 실행 기록을 수작업으로 바꾸지 않았습니다.

## 생성기 판정

Ch30의 두 `_generate.py`는 실행하면 실행 메타데이터와 현재 정독한 원본을 덮는 초기 전체 생성기입니다. `_build.py`는 이 생성기를 호출하지 않으며 `_src`와 실행 노트북을 직접 읽습니다. Ch33의 `_make_chapter.py`는 독립 검토 전 공통 문단과 오해 가능한 다이제스트 설명을 다시 쓰는 상태였으므로 안전 중지점으로 바꾸었습니다. 현재 Ch33 HTML은 `_src`와 실행 노트북을 정본으로 `_build.py`로만 재생성합니다. Ch31·32·34에는 현재 노트북·본문을 함께 다시 만드는 활성 생성기가 없습니다.

## 재검토 수정 후 검증

- 2026-09-14에 P7-01~09 수정 후 Ch30~34를 모두 다시 빌드했고, 공통 노트북 검증이 각각 9절/45셀, 5절/27셀, 5절/23셀, 5절/20셀, 5절/26셀로 통과했습니다.
- Ch30 대상 테스트 6개와 Ch33 대상 테스트 5개가 통과했습니다. Ch30의 Starlette `TestClient` 의존성 경고 1건은 테스트 실패가 아니며 실습에 고정된 현재 버전의 경고입니다.
- 초기 스냅샷과 다시 대조한 결과 29개 노트북의 코드 소스, 실행 번호, 코드 메타데이터, 출력 JSON이 모두 같았습니다.
- P7-02·03·04·05·07·09의 핵심 문구를 원본과 노트북에서 확인했고, P7-06·08의 복제 문구와 근거 없는 비용 추정은 Part 7 공개 파일 검색에서 나타나지 않았습니다.

## 남은 검토

독립 기술·한국어 정독은 root 담당 검토 단계에 남아 있습니다. 외부 맞춤법 서비스는 이 작성 단계에서 호출하지 않았습니다.
