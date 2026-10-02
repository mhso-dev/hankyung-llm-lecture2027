# 프로젝트 맥락 — 한경 KDT 「LLM Agent 개발 & 바이브코딩」 교재

> 인터뷰 2026-09-07 · 민감도 `public` · 검토자 강사 본인

## 새 세션에서 먼저 읽을 파일

기존 절을 학생 수준으로 고치는 작업은 `textbook/QUALITY-UPGRADE.md`를 가장 먼저 읽습니다. 그다음 `AGENTS.md` → `textbook/AUTHORING.md` → `textbook/_template/README.md` 순서로 읽고 아래 진행표에서 대상 절을 확인합니다. 템플릿은 일반 Before/After형과 실험 해석형을 제공하며, 미완성·미실행 초안은 완성 교재로 빌드하지 않습니다. 최신 주제 검토 사례는 `textbook/_notebook/TOPIC-ALIGNMENT-REVIEW.md`입니다.

## 품질 개선 단계 (2026-09-15 인터뷰)

규격 정본은 `textbook/QUALITY-UPGRADE.md`입니다(상태: 시범 결과 반영, 강사 확인 대기). 담당 에이전트는 `easy-upgrade-editor`, 체인은 `AGENTS.md` §9의 ⑨입니다. 수정 전 지침 원문은 `.moai/evolution/quality-upgrade-before-2026-09-15/`에 있습니다.

| 렌즈 | 상태 | 내용 |
|---|---|---|
| A 정체성 | 충족 | 완성된 Part 1~7(214절·노트북 214개)을 최대한 쉬운 교재로 다시 쓰는 단계 |
| B 산출물 | 충족 | 같은 절의 HTML·노트북 개정판, 절마다 Mermaid 도식 3~5장과 Higgsfield 삽화 1~2장 |
| C 독자 | 충족(기존) | 개발을 처음 하는 학생이 기본 경로의 기준 |
| D 문체 | 충족 | `~합니다`체 유지, 문장 구조를 쉽게(한 문장 한 정보, 70자 상한) |
| E 현행 | 충족 | 도식 절당 1장(상자 5개 세로 흐름), 삽화 전체 4장, Part 6 함수 정의 117·클래스 35, Part 3 내포식 49·lambda 26, Ch 22 가짜 모델 노트북 8개·틀 주석 50곳, 노트북 설명 셀 평균 117~253자 |
| F 품질 | 충족 | 게이트 G1~G8 + 별도 세션 사람 검토 + 강사 확인 |
| G 자산 | 충족(기존) | `execute.py`·`verify.py`·`visual.cjs`·`_build.py`, 기존 `_gen_figures.py` 도식 |
| H 제약 | 충족(기존) | `public`. Higgsfield 충전 완료(2026-09-15, 3,000크레딧) — Ch 22 삽화 9장 생성에 22크레딧 사용 |

사용자가 확정한 내용:

- 기존 지침은 부분 수정합니다.
- 코드는 Part별 허용 문법 사다리를 따릅니다. Ch 2에서 배운 문법이라도 기본 경로는 입문 문법으로 고정합니다.
- 「장표」는 Higgsfield 기반 그림과 Mermaid 차트 그림입니다. 개념마다 도식을 여러 장 넣습니다.
- Higgsfield 삽화는 절마다 1~2장입니다. 크레딧이 부족한 동안에는 프롬프트·캡션 파일만 만듭니다.
- 노트북만 봐도 따라갈 수 있게 설명과 그림을 넣습니다.
- 학습 목표가 아닌 준비 코드(가짜 모델 클래스)는 없애고 실제 모델을 temperature 0으로 호출합니다.
- 시범 챕터 Ch 22 Middleware를 먼저 고치고, 확인받은 뒤 Part 1부터 전체에 적용합니다.

진행표:

| 챕터 | 상태 | 게이트(G1~G7) | 검토 | 남은 것 |
|---|---|---|---|---|
| Ch 22 Middleware (시범) | 강사 확인 대기 | 수정 전 386건 → 0건, 9/9절(09 Middleware 실습 추가) | 별도 세션 2회(09는 1회), 지적 반영 완료 | 강사 확인, Part 6 목차·실습 묶음 재생성 |

다음 작업: 강사가 Ch 22 시범 결과를 확인하면 `QUALITY-UPGRADE.md` 상태를 「확정」으로 바꾸고 Part 1 Ch 1부터 적용합니다. 시범 기록은 `textbook/part6/ch22-middleware/qa/upgrade/`(진단 8개, 게이트 전후, 리뷰 묶음)와 `qa/verification.md`에 있습니다.

셋업 때 임시 스크립트로 잰 수정 전 수치(공식 게이트 아님, 시범에서 `upgrade_gates.py`로 다시 측정): Ch 22는 코드 셀 50개에 사다리 위반 55건·한 줄 복합문 등 25건·틀 주석 50곳·가짜 모델 흔적 15곳·`temperature=0` 없는 모델 생성 2셀·결과 설명 셀 없는 코드 셀 8개·Mermaid 0장, 문장 평균 41자·70자 초과 71개. Ch 12는 사다리 위반 131건·첫 줄 주석 없는 셀 79개. Ch 2는 사다리 위반 12건으로, 문법 자체가 학습 목표인 절은 게이트에 절별 허용 목록이 필요합니다.

## Part 7 현재 학생용 산출물 (2026-09-11)

현재 교재는 Ch1–34의 214개 절입니다. Part 7 시작점은 `textbook/part7/index.html`, 실습 묶음은 `textbook/downloads/part7-practice.zip`입니다. Ch30–34의 29절·노트북 29개·코드 셀 141개·SVG/Excalidraw 29쌍·복습 114문항을 추가했습니다. 커리큘럼 v6 기준 강의 28시간·실습 60시간이며, Ch30은 32시간입니다. 실행·배포·독립 검토 근거는 `textbook/part7/qa/verification.md`입니다.

- Ch30이 만든 것: `labs/part7/ch30-fastapi-serving/agent_service/`와 노트북 9개, `client/stream.ts`. FastAPI 입력·의존성·인증·CORS, Agent `ainvoke`·`astream`, POST SSE와 재연결·오류·시간 제한을 실제 HTTP와 TypeScript 클라이언트로 확인했습니다. 마지막 절은 실제 모델이 도구를 호출합니다. 이후 프로젝트에 API 형식과 전송 검증 기준을 넘깁니다.
- Ch31이 만든 것: `labs/part7/ch31-database/app/`, `migrations/`와 노트북 5개. 비동기 PostgreSQL·트랜잭션·Alembic·풀 고갈, pgvector와 체크포인터 공존, 별도 데이터베이스 복원을 실행했습니다. Ch32와 최종 프로젝트에 저장·복구 범위를 넘깁니다.
- Ch32가 만든 것: `labs/part7/ch32-docker/Dockerfile`, `compose.yaml`, `app.py`와 노트북 5개. 실제 다단계 빌드·레이어·컨테이너 변경, 동일 실행 의존성의 이미지 크기 86.2% 감소, Compose·pgvector·liveness/readiness를 확인했습니다. Ch33에 이미지와 구동 상태 확인 기준을 넘깁니다.
- Ch33이 만든 것: `labs/part7/ch33-cicd/.github/workflows/`, `scripts/`와 노트북 5개. 실제 평가 함수의 회귀 검출, OCI 이미지 빌드, 연속 위반 경보, HTTP 200→503→200 롤백과 이력 보존을 실행했습니다. 원격 GitHub Actions·레지스트리·클라우드 배포는 미실행입니다. Part 8에 변경 검사와 되돌리기 기준을 넘깁니다.
- Ch34가 만든 것: `labs/part7/ch34-cost-rate-limits/notebooks/`와 `runs/`의 캐시·라우팅 기록. 실제 LangChain 사용량과 두 모델의 답변, Batch 입력 세 건, 로컬 429·백오프·큐·동시성, 합성 비용 자료의 p95와 예산 차단을 확인했습니다. Batch는 외부 제출하지 않았습니다. 최종 프로젝트에 비용·품질·지연 비교 기준을 넘깁니다.

다음 집필은 Part 8 Ch35 「0단계 — 무지침」입니다. 연결 안내는 `labs/part7/continuity-guide.md`를 따릅니다. 본문 정본은 `_src/`, 코드와 출력 정본은 실행된 `.ipynb`입니다. 초기 원고 생성기로 한국어 감사 완료 본문을 덮어쓰지 않습니다. 실습 묶음은 현재·상위 폴더에서 챕터를 찾는 준비 셀과 잠금 환경을 포함하며 실제 비밀값을 제외합니다.

## Part 6 학생용 산출물 (2026-09-11)

Part 6까지의 교재는 Ch1–29의 185개 절입니다. Part 6 시작점은 `textbook/part6/index.html`, 실습 묶음은 `textbook/downloads/part6-practice.zip`입니다. Ch21–29의 47절·노트북 47개·코드 셀 248개·SVG/Excalidraw 47쌍·복습 171문항을 추가했습니다. 강의 46시간·실습 82시간이며 실행·배포·독립 검토 근거는 `textbook/part6/qa/verification.md`입니다.

- Ch21이 만든 것: `labs/part6/ch21-create-agent/notebooks/`와 `data/rag-comparison.json`. `create_agent`, 구조화 출력, 상태·런타임 컨텍스트, 검색 도구와 동일 세 질문 비교를 실행했습니다. Ch29에 실제 답변·도구 궤적·사용량·지연·judge 기록을 넘깁니다.
- Ch22가 만든 것: `labs/part6/ch22-middleware/notebooks/` 8개. 6개 훅, Ch16 처리의 미들웨어 이식, 호출 한도·재시도, 커스텀 예산·감사 처리, 순서·합성·컨텍스트 분리를 실행했습니다. Ch27에 하네스 구성의 기반을 넘깁니다.
- Ch23이 만든 것: `labs/part6/ch23-persistence/notebooks/`와 `durability_worker.py`, `idempotency_worker.py`. 체크포인터·스레드·PostgresSaver, 중단 후 실제 재개, pending writes, 멱등성을 확인했습니다. Ch24와 Ch30에 저장·복구 범위를 넘깁니다.
- Ch24가 만든 것: `labs/part6/ch24-human-in-the-loop/notebooks/` 3개. `interrupt`, `Command(resume=...)`, 상태 기록과 분기를 실행했습니다. 이후 업무 승인과 서비스 재개 설계로 연결합니다.
- Ch25가 만든 것: `labs/part6/ch25-streaming/notebooks/` 3개. 일곱 stream mode, 메시지 조각과 최종 답변 비교, first_event·TTFT 근삿값·total·실제 토큰 사용량을 구분했습니다. Ch30에 응답 스트림의 관찰 기준을 넘깁니다.
- Ch26이 만든 것: `labs/part6/ch26-delegation/notebooks/` 4개. 도구로 서브에이전트 위임, `active_agent` 상태 전환, 구조화된 destinations에 따른 라우팅·병렬 실행과 종료·비용 비교를 실행했습니다. Ch27·Ch39에 위임과 정지 기준을 넘깁니다.
- Ch27이 만든 것: `labs/part6/ch27-deepagents/notebooks/` 8개. `create_deep_agent`, 플래닝 opt-in, 파일 I/O, 이번 호출의 큰 결과 파일, 부모·자식 위임과 허용·차단 경로를 확인했습니다. 제공 자료 조사와 실제 웹 검색의 범위를 구분합니다.
- Ch28이 만든 것: `labs/part6/ch28-mcp/course_server.py`와 노트북 5개. MCP의 도구·리소스·프롬프트, FastMCP 서버, stdio·MCPAdapter, 도구 정의 수와 첫 호출 토큰 비교를 실행했습니다. 공식 사양 2025-11-25와 커리큘럼 2026-07의 차이를 기록했습니다.
- Ch29가 만든 것: `labs/part6/ch29-agent-evaluation/notebooks/` 4개. 최종 답변·한 단계·궤적 평가, 네 가지 매칭 모드, 참조 궤적 judge, 실제 Ch18·Ch21 운영 기록의 공통 표시를 실행했습니다. 최종 프로젝트의 평가 설계로 연결합니다.

Part 6 다음 학습은 Part 7 Ch30입니다. 연결 안내는 `labs/part6/continuity-guide.md`를 따릅니다. 본문·노트북·도식의 최종 정본과 해시는 Part 6 검증 기록에 있습니다. 초기 초안 생성기로 감사 완료 원고를 덮어쓰지 않습니다.

## Part 5 학생용 산출물 (2026-09-10)

Part 5까지의 교재는 Ch 1–20의 138개 절입니다. Part 5 시작점은 `textbook/part5/index.html`, 실습 묶음은 `textbook/downloads/part5-practice.zip`입니다. Ch 17–20의 21절·독립 노트북 21개·코드 셀 151개·SVG/Excalidraw 21쌍·복습 86문항을 추가했습니다. 강의 18시간·실습 30시간이며 최종 실행·배포·검토 근거는 `textbook/part5/qa/verification.md`입니다.

- Ch 17이 만든 것: `labs/part5/ch17-agent-overview/notebooks/` 5개, `architecture`·`stop_reason`·`metrics`, 커밋 고정 공개 궤적 발췌와 자율성 진단표. 합성 계산과 실제 공개 기록을 구분하며 Ch 18에 코드가 정한 흐름을 먼저 선택할 판단 기준을 넘깁니다.
- Ch 18이 만든 것: `labs/part5/ch18-workflow-patterns/notebooks/` 6개. 직접 OpenAI SDK로 게이트·라우팅·병렬 섹셔닝/투표·동적 워커·생성자/평가자와 동일 과제 비교를 실행했습니다. 실제 사용량·시간·비용과 관찰하지 못한 분기를 구분합니다. Ch 21에 프레임워크 없이 작성한 비교 기준을 넘깁니다.
- Ch 19가 만든 것: `labs/part5/ch19-model-tools/notebooks/` 6개, Ch 4의 `fetch_orders` 재사용, Pydantic 인자·반환 검증, `bind_tools`·`ToolMessage` 식별자 연결, 애플리케이션이 확인된 주문 ID를 보관하는 쓰기 통제. 실제 주문 변경은 수행하지 않는 모의 예제이며 Ch 20에 도구 정의와 오류 처리 방식을 넘깁니다.
- Ch 20이 만든 것: `labs/part5/ch20-tool-node/notebooks/` 4개. `ToolNode`·`tools_condition`·`StateGraph` 순환, 오류 결과 반환, `recursion_limit`과 명시적 종료, 동일 그래프에서 고정 선택과 모델 선택 비교. Ch 21에 수동으로 구성한 도구 에이전트와 비용·지연 비교 기준을 넘깁니다.

Part 5 다음 학습은 Part 6의 Ch21입니다. 선수 파일과 실행 순서는 `labs/part5/continuity-guide.md`를 따릅니다. 최종 본문은 `_src/`, 코드는 실행된 `.ipynb`가 정본이며 `_build.py`로 HTML을 갱신합니다. 초기 초안 생성기로 감사 완료 원고를 덮어쓰지 않습니다.

## Part 4 학생용 산출물 (2026-09-10)

Part 4까지의 교재는 Ch 1–16의 117개 절입니다. Part 4 시작점은 `textbook/part4/index.html`, 실습 묶음은 `textbook/downloads/part4-practice.zip`입니다. Ch 13–16의 30절·독립 노트북 30개·코드 셀 191개·도식 30쌍·복습 105문항을 추가했습니다. 강의 27시간·실습 37시간이며 실행·배포·검토 근거는 `textbook/part4/qa/verification.md`에 모읍니다.

- Ch 13이 만든 것: `labs/part4/ch13-langgraph-basics/notebooks/` 7개와 `runs/graph-integrated-result.json`. StateGraph·State·리듀서·조건부 엣지·Send·Command를 실행하고, PDF 로드→임베딩 검색→Kiwi BM25→RRF→CrossEncoder→출처 답변 생성의 여섯 노드를 연결했습니다. Ch 12의 Q002·PDF 6건 35쪽을 실제 사용하며 실행 결과의 근거는 E01 p.3·E02 p.3입니다. Ch 14와 중간 프로젝트에 그래프의 상태·입출력 형식을 넘깁니다.
- Ch 14가 만든 것: `labs/part4/ch14-rag-patterns/notebooks/` 9개와 `runs/pattern-comparison.json`. 대화 질문 재작성, Multi-Query, 질의 분해, Step-back, HyDE, 임계값 폴백, 생성 후 근거 검사, 한 단계 요약 계층을 직접 구현했습니다. Ch 12 전반의 12문서·8질문 원리 예제를 사용하며 세 질문의 Recall@3·지연·사용량·추정 비용을 비교합니다. 축소 예제를 원 논문의 전체 CRAG·Self-RAG·RAPTOR 구현으로 간주하지 않습니다. 중간 프로젝트와 Ch 21의 비교 대상으로 코드가 선택하는 처리 흐름을 넘깁니다.
- Ch 15가 만든 것: `labs/part4/ch15-evaluation-advanced/notebooks/` 8개, `data/evaluation-cases.json`, `runs/batch-eval-input.jsonl`. Ch 12의 36개 검색 설정 기록에서 낮은 순위 사례를 찾고 별도로 실제 답변을 생성해 Correctness·Relevance·Groundedness·Retrieval relevance 평가를 학습합니다. judge 위치 편향, 고정값으로 추적 구조를 읽는 연습, 합성 비용 분포의 p50/p95/p99, 회귀 비교와 Batch 입력 형식을 다룹니다. 제시 라벨은 독립적인 사람 평가가 아니며 실제 클라우드 추적·Batch 제출은 미실행입니다. 중간 프로젝트와 Ch 29에 평가 항목·기록 형식을 넘깁니다.
- Ch 16이 만든 것: `labs/part4/ch16-guardrails/notebooks/` 6개와 재사용 모듈 `guardrails.py`, 회귀 검사 `tests/test_guardrails.py`. 입출력 검증·PII 마스킹·히스토리 제한·계획 비용 상한·재시도·폴백·감사 기록을 구현했습니다. 문서 지시문 영향은 전후 모두 미관찰이므로 완화 효과를 입증했다고 쓰지 않습니다. 의심 문서가 있으면 해당 요청 전체를 호출 전에 중단하는 경로는 확인했습니다. 중간 프로젝트와 Ch 22에 직접 만든 검증 함수를 넘깁니다.
- LangChain 1.4.0의 요구 범위에 따라 LangGraph는 1.2 계열의 1.2.11을 고정했습니다. 실행 환경·버전·새 커널 검증 해시는 각 챕터와 노트북에 기록합니다. 공개 묶음은 앞 챕터에서 필요한 데이터·로그도 포함하며 비밀값과 비공개 전체 질문셋을 제외합니다.

Part 5의 Ch 17 「Agent 개요」와 연결됩니다. 중간 프로젝트에서는 제공된 작은 실험 수치를 재사용하지 않고 자신의 50문항과 전체 처리 흐름으로 평가합니다. 연결 안내는 `labs/part4/continuity-guide.md`를 따릅니다.

## Ch1–Ch12 전체 연결 갱신 (2026-09-10)

Part 4 집필 전 연결 검토 범위는 Ch1–Ch12의 87개 절입니다. 전체 연결 기록은 `textbook/qa/chapter-continuity-review.md`와 `chapter-continuity-verification.md`입니다. 다음 집필은 현재 학생용 `_src`·노트북·배포 파일을 기준으로 이어갑니다.

- Ch1의 Python 3.12·uv·커널 준비는 각 챕터의 `uv sync --locked`와 해당 `.venv`로 이어집니다. Git은 Ch3에서 실제 사용하며 Ch3의 임시 저장소가 Ch4로 전달되지는 않습니다.
- Ch4 05는 `data/article.html`을 파싱해 `labs/part1/ch04-data-tools/data/article-text.json`을 직접 생성합니다. `parse_article_html()`의 결과를 `schema_version/source/record`로 저장하고 Ch5 01이 읽어 토큰 수를 확인합니다. Ch5의 로컬 모델 선택 원리는 Ch6 API 후보 판단에 적용하며 모델 목록 자체를 넘기지 않습니다.
- Ch6 06은 `runs/provider-comparison-continuity.json`, Ch7 08은 `runs/prompt-ab-continuity.json`, Ch8 06은 `runs/context-design-continuity.json`을 생성합니다. Ch7·8은 앞 파일의 `run_id`와 SHA-256을 확인합니다. 사용량·캐시·단가 기준일·예상 비용은 이어 쓰며 다른 질문의 수치를 직접 비교하지 않습니다. 단어 포함 수와 자동 확인은 생성 품질 평가가 아닙니다.
- Ch8의 E01-p2/p3/p5 근거는 실제 PDF의 공휴일 예외·회원 한 사람·최초 2시간 주차와 맞췄습니다. 가상 필터 시행일은 실제 문서 날짜와 구분합니다. E01-p3은 Ch9의 `doc_id=E01/page=3`과 같은 원천 위치입니다.
- Ch9 02는 실제 청크와 임베딩 인코딩의 토큰 수를 확인합니다. Ch10의 HWPX 예제는 본문 문자열만 추출하며 표·문단 유형을 보존하는 구현이 아닙니다. Ch10 새 검색 로그는 Ch11이 실제로 다시 읽어 별도 평가 파일에 저장합니다.
- Ch12 전반 01~06은 챕터·노트북 폴더 어느 곳에서도 데이터와 로그를 찾습니다. `runs/core-history/`에 기존 로그 원본과 새 실행본을 보존합니다. 후반 통합 RAG는 임베딩 256차원·`gpt-5.4-mini`이며 36건의 TF-IDF+MMR 설정 비교와 별도입니다. 08절의 여섯 지표 행은 두 모델의 20후보 점수를 재사용하며 후보 수별 시간을 각각 측정한 결과가 아닙니다.

## Ch8–Ch12의 현재 학생용 연결 (2026-09-10)

초기 구현 기록의 `rag.py`, `harness.py`, `search()`는 현재 배포 노트북의 선수 코드가 아닙니다. 아래 경로와 최신 `textbook/qa/chapter-continuity-verification.md`를 다음 집필의 연결 기준으로 사용합니다. 이전 Part3 QA는 당시 실행 기록으로 보존합니다.

- Ch8의 Select는 Ch9의 `InMemoryVectorStore.similarity_search()`로 이어집니다. Ch11은 검색을 평가하고, 생성 답변 평가는 Ch15에서 확장합니다.
- Ch9 06은 디지털 PDF 18건과 개발용 Q001의 실제 검색·답변을 `labs/part3/ch09-rag-first-run/runs/continuity-ch09-search.jsonl`에 기록합니다. Ch10 08은 작은 예제 뒤에 같은 PDF·Q001의 여섯 설정을 `labs/part3/ch10-document-processing/runs/continuity-ch10-indexing.jsonl`에 기록합니다. `source_run_id`, 실제 검색 설정, `qid`, `gold_doc_ids`, 문서·쪽·청크·순위를 전달합니다.
- Ch11 06은 이 두 로그를 직접 읽어 원본과 분리된 평가를 저장합니다. 기록된 후보 수가 50보다 작으면 Recall@50은 미측정이며, 실제 저장된 후보에 대한 Recall을 따로 기록합니다. Ch11 자체의 페이지 검색 기준선과 연결 확인용 Q001 점수를 개선율로 비교하지 않습니다. 전체 후보는 `candidate_count/candidate_doc_ids`, 보고용 상위 결과는 `returned_count/top_results`로 구분하며, 기준선 평가마다 고유 실행 ID를 남깁니다.
- Ch11의 30문항과 Ch12 `advanced-queries.json`은 질문·정답 ID·개발/시험 분할이 같습니다. 설정 비교와 오류 분석은 개발용 15문항에 한정합니다. 두 챕터 모두 정답 문서가 없거나 답할 수 없는 질문은 검색 평균에서 제외하고, 여러 정답 중 찾은 문서의 비율로 Recall을 계산합니다. Ch12 전반 12문서·8질문은 별도 원리 예제이고, 후반 PDF 부모 6건·청크 175개로 전환할 때 대응 관계와 비교 한계를 설명합니다.
- Ch12 12절의 `advanced-continuity-experiment-log.jsonl` 36건은 TF-IDF+MMR 검색 설정 비교입니다. `advanced-continuity-test-result.json`은 선택 설정의 시험 평가이며, `advanced-continuity-integrated-result.json`은 개발 질문 한 건의 별도 통합 RAG 실행입니다. 통합 답변의 생성 품질은 아직 평가하지 않았습니다. Ch13에는 처리 단계의 입출력을, Ch15에는 실제 답변·출처와 미평가 상태를 전달합니다.
- 학생 실행 순서는 `labs/part3/continuity-guide.md`를 따릅니다. 기존 교재에서 시험 질문을 보고 설정을 선택했다면 새 시험 질문이 필요합니다. Ch13·15의 학생용 구현은 위 Part 4 산출물과 연결 안내에 추가되었습니다.

## 인터뷰 요약 (8렌즈)

| 렌즈 | 상태 | 내용 |
|---|---|---|
| A 정체성 | 충족 | 커리큘럼 v6(24주 960h · 8 Part 41 Ch) 기반 교재 집필. Jupyter 테마 HTML + 같은 코드·출력을 공유하는 절별 실행 노트북 |
| B 산출물 | 충족 | 개념 단위 HTML 절(강의 1h당 A4 5쪽) · .ipynb · 도식/삽화 · 퀴즈 |
| C 독자 | 충족 | 개발 입문자부터 웹 개발·기초 머신러닝 학습 경험자까지. 학생이 설명을 읽고 셀을 따라 실행하는 자습 교재 |
| D 문체 | 충족 | 커리큘럼과 같은 `~합니다`체 |
| E 현행 | 충족 | 공통 모듈·긴 파일형 코드가 학생의 복사 실행을 어렵게 함. 짧은 노트북 셀로 전환(2026-09-08) |
| F 품질 | 충족 | 모든 코드 uv 실행 후 수록 · 커리큘럼 두 규칙 위반 = 결함 · 검토자 1인 |
| G 자산 | 충족 | 기존 Ch 8·9·10 교재의 설명·도식은 유지. 공통 노트북 테마와 20개 실행 예제를 자산으로 사용 |
| H 제약 | 충족 | `public`. 삽화 Excalidraw MCP(연결됨)·Higgsfield(OAuth 필요). OpenAI 키는 `.env`에서만 |

집필 기준: 짧은 개념 설명 → 기본 실행 → 중간 결과 관찰 → 값 하나 변경 → 결과 비교를 반복합니다. 실제 원인을 고치는 절은 Before/After, 현상을 측정하는 절은 실험 결과 해석을 사용합니다. 기본 예제는 완성 코드이며 내부 구현은 선택 심화로 둡니다. API 검증에는 프로젝트 `.env`를 사용하고 비밀값은 출력하지 않습니다.

## 미정 항목 (커리큘럼 푸터) — 확정 시 `[[미정: …]]` 일괄 치환

| 항목 | 걸리는 챕터 | 플레이스홀더 | 임시 가정 |
|---|---|---|---|
| 바이브코딩 도구(Claude Code / Codex) | Ch 35~41 | `[[미정: 코딩 에이전트]]` | 두 도구 공통 개념(AGENTS.md·Skills·Hooks·서브에이전트)으로 서술 |
| 도메인 문서 세트·질의셋 | Ch 9~12·중간 프로젝트 | **확정(2026-09-07)** | `labs/data/rag-corpus/` — 합성 PDF 21종(쉬움6·중간6·어려움6·스캔3) + 질의셋 149문항(`queries.jsonl`) + 공개 PDF 15건 목록. 교재에서 `[[미정: 도메인 문서 세트]]`는 이 경로로 치환 |
| 임베딩·리랭커 모델 | Ch 10·12 | `[[미정: 임베딩 모델]]` `[[미정: 리랭커]]` | 한국어 벤치 상위 오픈 모델 2종 비교 형식으로 서술 |
| judge 모델 | Ch 15·29 | `[[미정: judge 모델]]` | 버전 고정 원칙만 서술 |

## 기준 버전 (고정)

LangChain v1.4 · LangGraph 1.2 · DeepAgents 0.7 · MCP 2026-07 · FastAPI 0.135+ · Python 3.12 · uv. 집필 시 `education-tutor-research`로 공식 문서 재확인.

## 진행표 (절 확정 시 갱신)

| Part | Ch | 개념 절 | HTML | 노트북 | 도식 | 비고 |
|---|---|---|---|---|---|---|
| 1 | 01 | 01 과정 지도와 학습 규칙 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 01-learning-cycle.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 01 | 02 도구 설치와 터미널 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 02-paths.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 01 | 03 Python과 가상환경 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 03-environments.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 01 | 04 첫 스크립트와 디버거 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 04-debugging.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 01 | 05 Git과 Docker 준비 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 05-tool-readiness.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 01 변수와 자료형 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 01-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 02 조건문과 반복문 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 02-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 03 자료구조 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 03-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 04 함수 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 04-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 05 파일과 예외 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 05-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 06 클래스 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 06-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 07 모듈과 타입힌트 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 07-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 08 pytest | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 08-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 09 데코레이터와 컨텍스트 매니저 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 09-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 10 Pydantic | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 10-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 11 패키징과 테스트 격리 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 11-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 02 | 12 async와 await | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 12-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 03 | 01 커밋과 gitignore | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 01-commit-ignore.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 03 | 02 GitHub Flow와 PR 리뷰 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 02-flow-review.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 03 | 03 병합 충돌 해결 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 03-merge-conflict.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 03 | 04 revert reflog worktree | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 04-recovery-tools.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 03 | 05 시크릿 이력 정리와 예방 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 05-secret-response.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 04 | 01 Pandas로 표 다루기 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 01-dataframe-flow.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 04 | 02 관계형 테이블과 키 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 02-relational-keys.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 04 | 03 SQL로 조회 함수 만들기 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 03-sql-query.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 04 | 04 REST와 페이지네이션 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 04-rest-pagination.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 04 | 05 문서 파싱과 스크래핑 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 05-document-parsing.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 05 | 01 토큰화와 한국어 효율 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 01-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 05 | 02 임베딩과 의미 유사도 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 02-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 05 | 03 어텐션 직관 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 03-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 05 | 04 컨텍스트 윈도 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 04-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 05 | 05 컨텍스트 로트 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 05-concept.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 05 | 06 temperature와 샘플링 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 06-temperature-sampling.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 05 | 07 환각의 구조적 원인 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 07-hallucination-conditions.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 1 | 05 | 08 모델 선택 기준 | 개념 설명·실행·검토 완료 | 실행 완료 .ipynb | 08-model-selection.svg | 2026-09-11 · 첫 사용 설명 개정 · .moai/evolution/part1-learning-sequence-2026-09-11/verification.md |
| 2 | 06 | 01 계층 지도와 첫 호출 | 집필·검증 완료 | 실행 완료 .ipynb | 01-layer-map.svg | 2026-09-09 · 실행·화면·독립 언어 검토 완료 |
| 2 | 06 | 02 메시지와 제공자 전환 | 집필·검증 완료 | 실행 완료 .ipynb | 02-provider-switch.svg |  |
| 2 | 06 | 03 구조화 출력과 검증 | 집필·검증 완료 | 실행 완료 .ipynb | 03-structured-output.svg |  |
| 2 | 06 | 04 스트리밍과 content blocks | 집필·검증 완료 | 실행 완료 .ipynb | 04-streaming.svg |  |
| 2 | 06 | 05 타임아웃 재시도 폴백 | 집필·검증 완료 | 실행 완료 .ipynb | 05-resilience.svg |  |
| 2 | 06 | 06 토큰 비용 지연 비교 | 집필·검증 완료 | 실행 완료 .ipynb | 06-observation.svg |  |
| 2 | 07 | 01 역할별 메시지와 제약 | 집필·검증 완료 | 실행 완료 .ipynb | 01-역할별-메시지.svg | 2026-09-09 · 실행·화면·독립 언어 검토 완료 |
| 2 | 07 | 02 페르소나와 과업 제약 | 집필·검증 완료 | 실행 완료 .ipynb | 02-페르소나-과업-제약.svg |  |
| 2 | 07 | 03 Few shot 예시 선택 | 집필·검증 완료 | 실행 완료 .ipynb | 03-Few-shot-선택.svg |  |
| 2 | 07 | 04 ChatPromptTemplate과 MessagesPlaceholder | 집필·검증 완료 | 실행 완료 .ipynb | 04-메시지-템플릿.svg |  |
| 2 | 07 | 05 CoT와 ReAct의 경계 | 집필·검증 완료 | 실행 완료 .ipynb | 05-reasoning-boundary.svg |  |
| 2 | 07 | 06 Self Consistency와 표본 합의 | 집필·검증 완료 | 실행 완료 .ipynb | 06-sample-consensus.svg |  |
| 2 | 07 | 07 구조화 출력 프롬프트 진단 | 집필·검증 완료 | 실행 완료 .ipynb | 07-structured-diagnosis.svg |  |
| 2 | 07 | 08 프롬프트 버전과 AB 비교 | 집필·검증 완료 | 실행 완료 .ipynb | 08-prompt-version-log.svg |  |
| 2 | 08 | 01 컨텍스트와 토큰 예산 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 01-컨텍스트-예산.svg · 01-책상-예산.png | 2026-09-09 재실행·독립 언어 검토 완료 |
| 2 | 08 | 02 Write와 Select | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 02-저장과-선택.svg | |
| 2 | 08 | 03 Compress와 Isolate | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 03-압축과-분리.svg | |
| 2 | 08 | 04 네 가지 실패 모드 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 04-실패-진단.svg | |
| 2 | 08 | 05 Context rot 측정 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 05-길이와-위치.svg | |
| 2 | 08 | 06 단계적 공개와 설계 비교 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 06-단계적-공개.svg | |
| 3 | 09 | 01 RAG 지도 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 01-파이프라인.svg · 01-오픈북-비유.png | 2026-09-09 재실행·독립 검토, 외부 맞춤법 생략 |
| 3 | 09 | 02 로더와 스플리터 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 02-청크-경계.svg | |
| 3 | 09 | 03 임베딩·벡터스토어·top-k | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 03-벡터-검색.svg | |
| 3 | 09 | 04 생성과 출처 인용 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | — | |
| 3 | 09 | 05 첫 실패 보기 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 05-실패-경로.svg · 05-지어낸-숫자.png | |
| 3 | 09 | 06 실험 하네스 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 06-하네스-루프.svg · 06-실험-노트.png | |
| 3 | 10 | 01 문서와 메타데이터 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 01-문서-계약.svg | 2026-09-09 재실행·독립 검토, 선택 확장은 검증 기록 참조 |
| 3 | 10 | 02 PDF와 표·OCR | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 02-표-구조.svg | |
| 3 | 10 | 03 DOCX·HTML·CSV | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 03-형식별-단위.svg | |
| 3 | 10 | 04 HWP와 HWPX | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 04-hwp-hwpx.svg | |
| 3 | 10 | 05 문자·재귀·토큰 청킹 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 05-청크-경계.svg | |
| 3 | 10 | 06 구조와 시맨틱 청킹 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 06-구조-의미-청킹.svg | |
| 3 | 10 | 07 한국어 임베딩과 캐시 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 07-임베딩-캐시.svg | |
| 3 | 10 | 08 인덱싱 비교 실험 | 입문자 단계별 실습 개편·실행 검증 완료 | 실행 완료 .ipynb | 08-실험-격자.svg | |
| 3 | 11 | 01 질의셋과 정답 문서 ID | 집필·실행 검증 완료 | 실행 완료 .ipynb | 01-평가셋-구조.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 11 | 02 Recall at 50 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 02-recall-후보.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 11 | 03 Precision at 5 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 03-precision-상위.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 11 | 04 nDCG at 5 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 04-ndcg-순위.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 11 | 05 조건별 평가와 오류 분류 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 05-오류-분기.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 11 | 06 실험 로그와 자동 실행 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 06-실험-루프.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 01 벡터 거리와 정확 검색 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 01-정확-검색.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 02 pgvector와 HNSW | 집필·실행 검증 완료 | 실행 완료 .ipynb | 02-HNSW.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 03 메타데이터 필터와 iterative scan | 집필·실행 검증 완료 | 실행 완료 .ipynb | 03-필터-반복탐색.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 04 한국어 Kiwi와 BM25 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 04-Kiwi-BM25.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 05 dense와 sparse 비교 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 05-dense-sparse.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 06 RRF 하이브리드 검색 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 06-RRF.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 07 cross encoder 리랭킹 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 07-리랭킹-흐름.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 08 후보 수와 리랭커 비교 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 08-후보-모델-격자.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 09 Parent document 검색 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 09-부모-자식-검색.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 10 MMR 다양성 선택 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 10-mmr-선택.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 11 질문 재작성과 검색 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 11-질문-재작성.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 3 | 12 | 12 종합 튜닝과 실험 로그 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 12-실험-로그.svg · 12-통합-RAG.svg | 2026-09-09 · 최종 검토는 Part 3 qa 기록 참조 |
| 4 | 13 | 01 StateGraph와 노드·엣지 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-10 · Part 4 qa/verification.md |
| 4 | 13 | 02 상태 갱신 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 02-흐름.svg |  |
| 4 | 13 | 03 조건부 엣지 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 03-흐름.svg |  |
| 4 | 13 | 04 add_messages 리듀서 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 04-흐름.svg |  |
| 4 | 13 | 05 Send와 동적 팬아웃 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 05-흐름.svg |  |
| 4 | 13 | 06 Command의 갱신과 이동 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 06-흐름.svg |  |
| 4 | 13 | 07 RAG 통합과 시각화 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 07-흐름.svg |  |
| 4 | 14 | 01 대화 히스토리와 질문 재작성 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 01-대화-히스토리와-질문-재작성-flow.svg | 2026-09-10 · Part 4 qa/verification.md |
| 4 | 14 | 02 Multi Query | 집필·실행 검증 완료 | 실행 완료 .ipynb | 02-Multi-Query-flow.svg |  |
| 4 | 14 | 03 질의 분해 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 03-질의-분해-flow.svg |  |
| 4 | 14 | 04 Step back | 집필·실행 검증 완료 | 실행 완료 .ipynb | 04-Step-back-flow.svg |  |
| 4 | 14 | 05 HyDE | 집필·실행 검증 완료 | 실행 완료 .ipynb | 05-HyDE-flow.svg |  |
| 4 | 14 | 06 CRAG | 집필·실행 검증 완료 | 실행 완료 .ipynb | 06-CRAG-flow.svg |  |
| 4 | 14 | 07 Self RAG | 집필·실행 검증 완료 | 실행 완료 .ipynb | 07-Self-RAG-flow.svg |  |
| 4 | 14 | 08 RAPTOR 계층 요약 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 08-RAPTOR-계층-요약-flow.svg |  |
| 4 | 14 | 09 패턴 비교와 선택 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 09-패턴-비교와-선택-flow.svg |  |
| 4 | 15 | 01 실패 로그와 평가 대상 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 01-평가-흐름.svg | 2026-09-10 · Part 4 qa/verification.md |
| 4 | 15 | 02 4대 RAG 평가자 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 02-평가-흐름.svg |  |
| 4 | 15 | 03 judge 프롬프트와 편향 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 03-평가-흐름.svg |  |
| 4 | 15 | 04 제시 라벨과 일치율 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 04-평가-흐름.svg |  |
| 4 | 15 | 05 로컬 트레이싱과 지연 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 05-평가-흐름.svg |  |
| 4 | 15 | 06 대화당 비용 백분위수 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 06-평가-흐름.svg |  |
| 4 | 15 | 07 회귀 스위트 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 07-평가-흐름.svg |  |
| 4 | 15 | 08 Batch 평가 입력 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 08-평가-흐름.svg |  |
| 4 | 16 | 01 입출력과 출처 검증 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-10 · Part 4 qa/verification.md |
| 4 | 16 | 02 PII 마스킹 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 02-흐름.svg |  |
| 4 | 16 | 03 히스토리 트리밍과 실제 요약 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 03-흐름.svg |  |
| 4 | 16 | 04 호출 한도와 비용 상한 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 04-흐름.svg |  |
| 4 | 16 | 05 재시도·폴백과 감사 로그 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 05-흐름.svg |  |
| 4 | 16 | 06 문서 프롬프트 인젝션과 통합 | 집필·실행 검증 완료 | 실행 완료 .ipynb | 06-흐름.svg |  |
| 5 | 17 | 01 워크플로우와 에이전트 경계 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 17 | 02 워크플로우가 충분한 조건 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 17 | 03 모델 도구 루프와 정지 조건 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 17 | 04 자율성의 대가 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 17 | 05 제품 트레이스와 자율성 진단 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 05-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 18 | 01 게이트가 있는 프롬프트 체이닝 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 18 | 02 실패를 처리하는 라우팅 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 18 | 03 병렬 섹셔닝과 투표 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 18 | 04 동적 오케스트레이터와 워커 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 18 | 05 생성자 평가자와 정지 조건 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 05-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 18 | 06 같은 과제로 다섯 패턴 비교 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 06-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 19 | 01 tool과 Ch 4 함수 재사용 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-tool과-Ch4-함수-재사용-flow.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 19 | 02 Pydantic 인자와 반환 스키마 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-Pydantic-인자와-반환-스키마-flow.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 19 | 03 좋은 도구 이름과 설명 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-좋은-도구-이름과-설명-flow.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 19 | 04 설명만으로 도구 선택하기 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-설명만으로-도구-선택하기-flow.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 19 | 05 bind_tools와 병렬 호출 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 05-bind_tools와-병렬-호출-flow.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 19 | 06 오류와 읽기 쓰기 분리 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 06-오류와-읽기-쓰기-분리-flow.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 20 | 01 ToolNode와 tools_condition | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 20 | 02 도구 오류와 ToolMessage | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 20 | 03 recursion_limit과 명시적 종료 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 5 | 20 | 04 if 분기와 모델 선택 비교 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-10 · Part 5 qa/verification.md |
| 6 | 21 | 01 create agent와 ReAct 루프 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 21 | 02 구조화 출력 두 전략 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 21 | 03 AgentState와 context schema | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 21 | 04 0x에서 1x로 마이그레이션 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 21 | 05 retriever를 도구로 전환 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 05-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 21 | 06 같은 평가셋으로 RAG 비교 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 06-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 22 | 01 미들웨어와 6개 훅 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-미들웨어와-6개-훅-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 22 | 02 PII 마스킹 이식 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-PII-마스킹-이식-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 22 | 03 요약 압축과 Compress | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-요약-압축과-Compress-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 22 | 04 호출 한도와 재시도 폴백 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-호출-한도와-재시도-폴백-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 22 | 05 커스텀 예산 미들웨어 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 05-커스텀-예산-미들웨어-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 22 | 06 커스텀 감사 미들웨어 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 06-커스텀-감사-미들웨어-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 22 | 07 순서와 합성 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 07-순서와-합성-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 22 | 08 컨텍스트 분리와 Isolate | 집필·실행·검토 완료 | 실행 완료 .ipynb | 08-컨텍스트-분리와-Isolate-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 23 | 01 체크포인터와 스레드 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 23 | 02 PostgresSaver 준비와 스키마 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 23 | 03 스레드 재개와 대화 이어가기 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 23 | 04 내구 실행 모드 비교 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 23 | 05 pending writes와 장애 복구 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 05-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 23 | 06 노드 재시작과 멱등성 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 06-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 24 | 01 interrupt 승인 게이트 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 24 | 02 Command resume으로 실행 재개 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 24 | 03 상태 기록과 다른 분기 재실행 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 25 | 01 일곱 가지 stream mode | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 25 | 02 토큰과 중간 진행 스트리밍 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 25 | 03 TTFT와 total 비교 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 26 | 01 Subagent 도구 위임 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 26 | 02 Handoff 상태 전환 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 26 | 03 Router 분류와 병렬 실행 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 26 | 04 호출 수·비용·종료 조건 비교 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 27 | 01 하네스와 일곱 기능 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 27 | 02 create deep agent와 도구 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 27 | 03 플래닝과 시스템 프롬프트 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 27 | 04 파일시스템과 중간 결과 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 27 | 05 컨텍스트 관리와 오프로딩 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 05-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 27 | 06 서브에이전트 위임 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 06-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 27 | 07 출처 검증형 deep research | 집필·실행·검토 완료 | 실행 완료 .ipynb | 07-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 27 | 08 통합 실행과 운영 한계 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 08-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 28 | 01 MCP 구조와 capability 협상 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 28 | 02 FastMCP 로컬 서버 제작 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 28 | 03 stdio와 원격 전송·권한 경계 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 28 | 04 LangChain MCP 클라이언트 연동 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 28 | 05 도구 정의와 첫 호출 토큰 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 05-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 29 | 01 에이전트 평가 세 전략 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 01-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 29 | 02 궤적 매칭 네 모드 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 02-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 29 | 03 LLM judge로 궤적 평가 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 03-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| 6 | 29 | 04 운영 지표와 Ch18 궤적 비교 | 집필·실행·검토 완료 | 실행 완료 .ipynb | 04-흐름.svg | 2026-09-11 · Part 6 qa/verification.md |
| … | … | | | | | |

### 현재 학생용 산출물 — Ch 1 (2026-09-09)

- 교재: `textbook/part1/ch01-development-environment/index.html`과 5절. 강의 5h·실습 3h, 복습 20문항·해설, A/B 경로 자가진단 6과제·답안. 정본은 `_src/`와 `chapter.json`입니다.
- 실습: `labs/part1/ch01-development-environment/notebooks/` 5개·25셀, Python 3.12.13·uv 0.11.6, ipykernel 7.3.0·nbclient 0.11.0. 노트북마다 새 커널 실행, 최대 19줄. 키·모델 호출 없음.
- 이 챕터가 만든 것: `hello.py`, uv 잠금 환경, 상대 경로 읽기·가상환경 비교·pdb 값 관찰·Git 상태와 Docker 준비 확인 기록. 새 용어는 입력/출력/셀, 경로, 인터프리터/가상환경/커널, 중단점, 저장소/클라이언트/데몬 등입니다. Ch 2에 `hello.py`와 환경 선택·실행·수정·검증 방법을 넘깁니다.
- 배포: `textbook/downloads/ch01-practice.zip`(노트북 5개와 준비 파일), 전체 `llm-practice.zip`에도 Ch 1을 추가했습니다. 전체 묶음은 노트북 25개·PDF 21개·예제 5개·Ch 1 준비 파일 4개입니다.
- 도식: SVG/Excalidraw 5쌍. 생성형 삽화 크레딧 0. Excalidraw MCP 미리보기 미지원으로 SVG·JSON 검증을 사용합니다.
- 확인 범위: macOS 실제 실행, Docker 클라이언트·데몬 29.4.1 응답 확인. Windows/Linux 설치 및 VS Code 디버거 GUI는 미검증. A/B 공식 반 배치 기준은 미정입니다. 외부 맞춤법 전송은 스킬의 대량 처리 제한에 따라 생략합니다. 상세: 챕터 `집필점검표.md`, `qa/verification.md`, `qa/topic-review.md`, `qa/language/`.

### 현재 학생용 산출물 — Ch 2 (2026-09-09)

- 교재: `textbook/part1/ch02-python/index.html`과 개념 12절. 강의 12h·실습 28h, 복습 48문항·해설, A 경로 보충 6과제·기대값. 09~11절은 B 경로 확장, 12절 async/await는 공통 필수입니다.
- 정본: 챕터 `_src/`·`chapter.json`, `labs/part1/ch02-python/notebooks/` 12개. 76개 코드 셀을 새 커널·임시 작업 폴더에서 실행했으며 최대 22줄입니다. Python 3.12.13, pytest 9.1.1, Pydantic 2.13.5, uv/uv-build 0.12.11, API 키·모델 호출 없음.
- 이 챕터가 만든 것: `calculate_payment`, `add_tag`, `read_items`·`parse_order`, `Order`, `pricing.py`·`add_tax`, pytest 검사, `trace`·`managed_resource`, `LooseJob`·`StrictJob`, `report_tools` 휠, `fetch_label` 비동기 예제. 새 용어는 자료형·자료구조·함수·모듈·타입힌트·fixture·코루틴 등입니다. Ch 4에 파일 읽기·변환 함수와 검증 방식을, Ch 18·30에 입력 검증·자원 정리·비동기 대기의 기초를 넘깁니다. 임시 파일 생성 예제는 각 노트북을 실행할 때 만들어집니다.
- 배포: `textbook/downloads/ch02-practice.zip`에 12개 노트북, README, pyproject.toml, uv.lock을 포함합니다. 전체 목차와 공통 실습 묶음에도 추가합니다. 전체 묶음의 현황은 해당 manifest를 기준으로 확인합니다.
- 검증: 기술·교육 독립 검토, HTML 코드·출력·다운로드 일치, 1280/390px 화면·복사 26건, 도식 12개 라벨 경계 검사. SVG/Excalidraw 12쌍, 생성형 삽화 크레딧 0입니다.
- 확인 범위: macOS에서 실제 실행했습니다. Windows/Linux 실행은 미검증이며 외부 맞춤법 전송은 스킬의 상업적 대량 처리 제한으로 생략합니다. 로컬 언어 감사와 다른 모델의 최종 의미 검토 기록은 `qa/language/`, 상세 완료 근거는 `집필점검표.md`·`qa/verification.md`·`qa/topic-review.md`입니다.

### 현재 학생용 산출물 — Part 1 전체 (2026-09-11 개념 학습 순서 개정)

- 학생 시작점: `textbook/part1/index.html`. Ch 1–5의 35절, 강의 37h·실습 59h, 총 96h입니다. 35절 모두 첫 사용 설명과 선수 학습 연결을 개정했습니다. 2026-09-09 최초 집필 기록은 기존 qa/verification.md에 보존합니다.
- 교재와 실습: 기본 노트북 35개·199셀(최대 25줄), SVG·Excalidraw 35쌍, 복습 135문항·해설. 코드가 바뀐 노트북 21개의 새 커널 실행 기록을 확인하고 전체 35개의 코드·출력 해시를 검증했습니다. HTML 코드·실제 출력·내장 다운로드를 정본 노트북과 대조했습니다.
- Ch 3이 만든 것: 격리된 Git 저장소에서 커밋·무시 규칙·브랜치 리뷰·병합 충돌·revert·reflog·worktree·더미 시크릿 이력 정리를 확인했습니다. GitHub PR 화면의 설명과 로컬 실행 범위를 구분합니다. Ch 35 이후 변경 관리와 리뷰에서 다시 사용합니다.
- Ch 4가 만든 것: `labs/part1/ch04-data-tools/data_tools.py`의 `fetch_orders`, `find_customer_orders`, `fetch_articles`, 교육용 CSV·JSON·HTML·robots.txt와 테스트 10개입니다. Ch 19의 도구 작성에 조회 함수와 입력·반환 형식, 타임아웃·페이지네이션 검증을 넘깁니다.
- Ch 5가 만든 것: 토큰화·문장 임베딩·어텐션 비중·토큰 예산·입력 길이와 근거 위치·샘플링·환각·모델 필수 조건을 관찰한 8개 노트북입니다. GPT-2·KLUE 토큰화기, multilingual MiniLM 임베딩 모델, Qwen2.5-0.5B-Instruct의 revision을 고정했습니다. Ch 6에는 토큰과 모델 출력 해석, Ch 8에는 채팅 형식까지 포함한 예산과 실험 조건 기록을 넘깁니다.
- 배포: `textbook/downloads/part1-practice.zip`은 노트북 35개를 포함한 실습 파일 60개와 시작 안내·SHA-256 manifest를 제공합니다. 전체 `llm-practice.zip`에도 반영했습니다. 모델 가중치·가상환경·실제 키는 포함하지 않습니다.
- 검증: `.moai/evolution/part1-learning-sequence-2026-09-11/verification.md`와 연결 기록에서 HTML 42개·노트북 35개·로컬 링크 309개·화면 84건·배포 정본 해시 일치를 확인합니다. 절별 첫 사용 설명과 독립 정독, 자동 언어 경고의 수동 재판정은 같은 폴더에 기록했습니다.
- 확인 범위: macOS에서 실행·화면을 확인했습니다. 다른 운영체제와 실제 GitHub PR 게시 화면은 미검증입니다. 외부 맞춤법 서비스는 상업적 대량 처리 제한에 따라 생략하고 로컬 검수로 대체했습니다. 새 Part 1의 유료 모델 API 호출과 생성형 삽화 크레딧 사용은 모두 0입니다.

### 현재 학생용 산출물 — Part 3 전체 (2026-09-10 연결성 수정)

- 교재: `textbook/part3/index.html`에서 Ch 9의 6절, Ch 10의 8절, Ch 11의 6절, Ch 12의 12절을 순서대로 읽습니다. 강의 32h·실습 64h, 총 96h입니다. Ch 9·10을 보완하고 Ch 11·12를 작성했습니다. 아래 과거 Ch 9·10 메모보다 이 현재 산출물 설명과 절별 노트북을 우선합니다.
- 실습: `labs/part3/`의 독립 노트북 32개가 정본입니다. 연결성 수정으로 코드가 바뀐 노트북은 Python 3.12 새 커널에서 다시 실행하고, 설명만 바뀐 노트북은 코드·출력·실행 메타데이터를 보존합니다. 최신 셀 수와 실행 범위는 연결성 검증 기록을 따릅니다. 이전 집필 때 실행한 PostgreSQL·pgvector 검증은 이번 수정의 재실행 범위와 구분합니다.
- Ch 11이 만든 것: `labs/part3/ch11-evaluation/evaluate.py`, `data/evaluation-queries.jsonl`의 공개 학습용 30개 질문, 문서 중복을 제거한 Recall@5·Recall@50·Precision@5·nDCG@5, 난이도·질문 유형별 결과와 실행 기록. 정답 문서 ID, 평가 단위, 빈 정답 제외 정책을 Ch 12·15에 넘깁니다. 전체 집필용 149문항 원본은 학생 묶음에 넣지 않습니다.
- Ch 12가 만든 것: 거리·HNSW·필터의 비교, Kiwi BM25, 직접 RRF, 두 CrossEncoder, 자식 검색·부모 전달, 직접 MMR, 원문·재작성·RRF 비교입니다. `runs/advanced-continuity-experiment-log.jsonl`은 TF-IDF+MMR 개발 설정 36건, `advanced-continuity-test-result.json`은 선택 설정의 시험용 15문항 평가입니다. `advanced-continuity-integrated-result.json`은 실제 PDF 쪽 본문을 dense·BM25·RRF·리랭킹·출처 표시 생성으로 처리한 개발 질문 Q002의 별도 실행입니다. 이 처리 단계와 입출력을 Ch 13에 넘기며, 생성 답변은 Ch 15에서 평가할 대상으로 남깁니다.
- 도식·복습: SVG·Excalidraw 정본 32쌍, 기존 삽화 유지, 복습 128문항·해설입니다. 새 생성형 이미지 크레딧은 0입니다. Ch 12 정본은 `figures/_gen_figures.py`이며 모든 단계의 노드·화살표에서 SVG와 편집본을 함께 만듭니다.
- 배포: `textbook/downloads/part3-practice.zip`과 전체 `llm-practice.zip`에 현재 노트북·공용 자료·환경 파일·공개 평가 코드·질문·연결 로그와 `labs/part3/continuity-guide.md`를 포함합니다. 파일 수와 해시는 각 manifest 및 연결성 검증 기록으로 확인합니다.
- 검증: 이번 수정의 실행·화면·복사·배포 검사와 독립 기술·언어·의미 검토는 `textbook/part3/qa/chapter-continuity-verification.md`에 기록합니다. 기존 `qa/verification.md`는 이전 집필 검증의 범위와 증거를 보존합니다.
- 해석 범위: Ch 11의 작은 문서 집합에서 Recall@50=1은 포화 결과입니다. 전반 12개 문서·8개 질문과 후반 6개 PDF·30개 질문을 일반 업무 성능으로 확대하지 않습니다. 상용 파서·자신의 문서 100건은 선택 확장이며 미실행입니다. 실제 pgvector 0.8.2와 공식 조사 최신 0.8.6을 구분합니다. 외부 맞춤법 전송은 상업적 대량 처리 제한으로 생략하며, Excalidraw MCP 미리보기 대신 정본·브라우저 검사로 확인합니다. 다른 운영체제에서의 전체 재실행은 미검증입니다.

### 현재 학생용 산출물 — Part 2 전체 (2026-09-09)

- 교재: `textbook/part2/index.html`에서 Ch 6의 6절, Ch 7의 8절, Ch 8의 6절을 순서대로 읽습니다. 강의 20h·실습 36h, 총 56h입니다. Ch 6·7을 새로 작성하고 Ch 8은 현재 기준으로 보완·재실행했습니다.
- 실습: `labs/part2/`의 독립 노트북 20개·180개 코드 셀을 Python 3.12 새 커널에서 실행했습니다. 셀은 최대 21줄이며 HTML 코드·출력·다운로드와 일치합니다. OpenAI 실제 호출을 확인했습니다. Anthropic·Google 분기는 완성했지만 키가 없어 실제 호출은 미검증입니다.
- 이 챕터들이 만든 것: Ch 6은 `init_chat_model`·`invoke`·`AIMessage.text`, 구조화 출력, 스트리밍, 오류 처리, 사용량·비용 기록을 제공합니다. Ch 7은 `ChatPromptTemplate`·`MessagesPlaceholder`, 프롬프트 조건 비교, `labs/part2/ch07-prompt-engineering/runs/prompt-ab-v1.json`의 프롬프트·응답·설정 저장과 읽기를 제공합니다. Ch 8은 예산·선택·압축·분리·단계적 공개를 실험하고 Ch 9에 질문과 함께 전달할 자료를 선택하는 방법을 이어 줍니다.
- 도식·평가: SVG·Excalidraw 20쌍, 기존 Ch 8 삽화 1장, 복습 80문항과 해설입니다. 새 생성형 이미지 비용은 없습니다. Excalidraw MCP 미리보기 대신 SVG·JSON 구조와 실제 브라우저 표시를 확인했습니다.
- 배포: `textbook/downloads/part2-practice.zip`에 노트북 20개·준비 파일 9개와 시작 안내·빈 환경 파일·해시 목록을 담았습니다. 전체 묶음 `llm-practice.zip`은 현재 노트북 51개와 공용 자료를 포함합니다. 최신 파일 구성은 manifest를 기준으로 확인합니다.
- 검증: Part 2 본문·목차의 PC/모바일 화면 48건, 링크 161건, 다운로드 해시·키 비노출 확인을 마쳤습니다. 언어 감사는 다른 모델의 전문 정독과 Phase 6 대조를 마쳤으며, 외부 맞춤법은 스킬의 상업적 대량 전송 제한으로 생략했습니다. 자동 언어 게이트 WARN을 통과로 바꾸지 않고 수동 판정 근거를 남겼습니다. 상세: `textbook/part2/qa/verification.md`·`qa/language/part2-final-audit-2026-09-09.md`.

### 이전 학생용 구성 기록 — Ch 8·9·10 (2026-09-09)

- 정본: 각 챕터 `labs/.../notebooks/*.ipynb`의 기본 노트북 20개와 `textbook/.../_src/`의 대응 20절입니다. 공통 렌더러가 코드와 실제 출력을 HTML에 삽입합니다.
- Ch 8은 짧은 컨텍스트 예제를 단계별로 실행합니다. Ch 9는 제공 PDF 첫 완주 후 짧은 Document로 검색·생성·실패·설정 비교를 관찰합니다. Ch 10은 형식 관찰과 LangChain 청킹·임베딩·캐시·세 조건 검색 비교를 실행합니다.
- Ch 11 연결 시 현재 노트북의 검색 ID·출처·설정과 실제 반환값을 기준으로 삼습니다. 아래의 초기 모듈·전체 말뭉치 로그·metrics 필드는 과거 구현 기록이며 현재 기본 노트북의 산출물로 가정하지 않습니다.
- 학생 배포: `textbook/downloads/llm-practice.zip` — Ch 1 추가 후 노트북 25개, PDF 21개, 예제 5개, Ch 1 준비 파일 4개, 시작 안내, 빈 환경 파일 예시. 실제 키와 평가 답안은 포함하지 않습니다.
- 검증: 새 커널에서 20개·207셀을 실행했으며 API 예제는 실제 생성·임베딩을 사용했습니다. 상세 근거와 제한은 `textbook/_notebook/GUIDED-PRACTICE-VERIFICATION.md`에 기록합니다.

### 초기 구현 기록 — Ch 8 (2026-09-08)

- 교재: `textbook/part2/ch08-context-engineering/{index,01..06}.html` — 강의 6h·실습 10h, 개념 6절, 복습 문제 24개와 해설. Ch 9의 `_src/`·`_build.py` 구조를 적용했습니다. 빌드는 실습 파일의 코드와 저장 출력을 직접 삽입합니다.
- 코드: `labs/part2/ch08-context-engineering/context_lab.py`의 `make_budget`·`ensure_input_fits`·`save_memory`·`load_memory`·`select_documents`·`compress_facts`·`assemble_isolated_messages`·`call_model`, `examples/ex01~ex06`, 원문 응답과 사용량을 담은 `runs/*.jsonl`. uv·Python 3.12·OpenAI Responses API, gpt-5.4-mini. Ruff·잠금 검사 통과, 테스트 16개 통과.
- 도식: SVG·Excalidraw 각 6개, `figures/_gen_figures.py`가 함께 생성. 삽화 1장과 캡션, Higgsfield 실제 사용 2크레딧. 요청 모델과 완료 조회 모델의 차이는 `verification.md`에 기록했습니다.
- 다음 학습과 이어지는 지점: 사람이 선택한 E01 문서 근거를 고정 함수로 조립하는 과정을 Ch 9의 검색 기반 선택으로 연결합니다. Write·Select·Compress·Isolate, 토큰 예산, 네 실패 유형, 길이/위치 실험, 단계적 공개, 캐시를 반영한 비용 비교를 도입했습니다. LangChain·LangGraph·에이전트는 사용하지 않았습니다.
- 검증: 코드 블록 13개·실행 출력 6개 일치, 최종 API 로그 46건 완료, 응답 45건 정독, 화면 14건 통과. 길이/위치 실험 27건 모두 최소 정답+출처 기준을 통과하여 성능 저하를 관찰했다고 일반화하지 않았습니다. 상세 근거는 교재 폴더의 `verification.md`와 `checks/`에 있습니다.
- 정식 한국어 3단 감사는 별도 검토 세션에서 진행합니다. Excalidraw MCP 미리보기는 연결 도구가 없어 생략하고 생성된 SVG를 브라우저에서 검증했습니다.

### 초기 구현 기록 — Ch 9 (2026-09-07)

- 교재: `textbook/part3/ch09-rag-first-run/{index,01..06}.html` — `_src/*.html`(본문 조각) + `_build.py`(공통 골격·SVG 인라인·삽화 base64)로 생성. 수정은 `_src/`를 고치고 `python _build.py`.
- 도식: `figures/_gen_figures.py` 한 파일이 `.excalidraw`와 `.svg`를 함께 생성(색 규칙 §16). 삽화 3장(`*.png`, Higgsfield nano_banana_pro, 6크레딧) + `*.caption.md`.
- 코드: `labs/part3/ch09-rag-first-run/` — `rag.py`(`load_pdfs`·`corpus_paths`·`split_docs`·`build_index`·`search`·`format_context`·`generate`·`answer`·`Answer`), `prompts.py`(`strict`·`helpful`), `harness.py`(`load_config`·`index_key`·`get_index`·`load_queries`·`run`), `config.yaml`, `examples/ex02~ex05`, `tests/`(10 passed). 환경: uv · Python 3.12.13 · langchain 1.4.0 · langchain-openai 1.6.0 · langchain-text-splitters 1.1.2 · pypdf 6.17.0. 모델: text-embedding-3-small(`[[미정: 임베딩 모델]]`) · gpt-5.4-mini.
- 새 용어(27): RAG·색인·청크·벡터스토어·top-k·출처 인용·Document·로더·스플리터·chunk_size/overlap·separators·임베딩·코사인 유사도·질문 임베딩·dump/load·컨텍스트 조립·시스템 프롬프트·usage_metadata·환각·거부·unanswerable·확률적 실패·실험 하네스·설정 파일·run_id·설정 해시·JSONL.
- 다음 챕터에 넘기는 것: 출처 태그 형식 `[doc_id p.페이지]`(Ch 11 합의·Ch 16 검증), `metadata.doc_id/page/chunk_id`(Ch 11·12), `runs/{run_id}.jsonl`의 `gold_doc_id`+`retrieved(chunk_id 포함)`(Ch 11 Recall@k 계산 입력), `runs.jsonl`의 `metrics: {}`(Ch 11이 채움), 실패 사례 4종(검색 실패 Q003/Q008·확률적 환각 A/S 질문·부칙 누락 오답 Q070·문서 속 지시문 → Ch 11/12/15/16 첫 문장).
- 실측 사실(교재 인용): easy 6건=28쪽, 500/50 → 47청크; easy+medium+hard 18건=90쪽 → 176청크(1000/100 → 107); 498자=431토큰(cl100k); 휴관일 질문 1위=표지(0.649), 답은 2위(0.565); "책을 3일 늦게 반납" 정답 청크 #3은 6위; gpt-5.4-mini helpful 프롬프트 5회 중 2회 환각.
- 초판(2026-09-07)은 한국어 감사를 생략했습니다. 2026-09-08 보완에서 일반 슬롭 정리·로컬 맞춤법·윤문과 다른 모델의 최종 정독을 마쳤습니다. 외부 맞춤법 서비스는 상업적 대량 처리 제한으로 생략했습니다.
- 2026-09-08 보완: Ch 10의 글자 크기·모바일 도식 표시를 적용하고 목차 원본을 `_src/index.html`로 옮겼습니다. 코드·출력 30블록을 실습 파일과 연결하고 기존 출력 12개를 원본 절·순번·해시와 함께 보존했습니다. 도식 5개는 글자 크기·대비·고정 흐름의 색을 보완했고 삽화 3개는 유지했습니다. 실제 실행 범위와 최종 검사 결과는 `textbook/part3/ch09-rag-first-run/qa/verification.md`에 있습니다.

### 초기 구현 기록 — Ch 10 (2026-09-08)

- 교재: `textbook/part3/ch10-document-processing/index.html`과 8절, 강의 8h·실습 16h, 복습 32문항·해설. `_src/`가 원본이며 `_build.py`가 실습 코드·저장 출력을 직접 삽입합니다.
- 코드: `labs/part3/ch10-document-processing/document_processing.py`의 `normalize_metadata`, 형식별 `load_*`, `split_char`·`split_recursive`·`split_token`·`split_structural`·`split_semantic`, `EmbeddingCache`·`embed_with_cache`·`preflight_corpus`; `experiment.py`, `examples/ex01~ex08`, `runs/`의 설정별 상세 로그와 집계 로그.
- 새 용어: OCR, 레이아웃 추출, OLE 컨테이너, HWPX, 토큰 경계, 구조 청킹, 시맨틱 청킹, 입력 접두어, 캐시 키, 말뭉치 지문. 기존 Document·메타데이터·임베딩·유사도 개념을 확장했습니다.
- 다음 챕터에 넘기는 것: 출처·페이지·청크 식별자, 실제 청크 설정·말뭉치 지문·질의 ID를 기록한 3×2 실험 로그, Ch 11에서 채울 `metrics: {}`. 디지털 PDF 18건에서 재귀 137개·토큰 211개·구조 136개의 청크를 만들었습니다. 교육용 특징 벡터 실행이므로 실제 임베딩 모델의 품질 비교에 사용할 수 없습니다.
- 검증: 테스트 38개, Ruff·문법 검사, 본문 구성·코드·출력 대조 8/8, PC·모바일 화면 18/18 통과. SVG·Excalidraw 각 8개는 공통 생성기에서 작성했습니다. 일반 슬롭 정리·로컬 맞춤법과 윤문·다른 모델의 Phase 6 정독을 마쳤습니다. 외부 맞춤법 서비스는 상업적 대량 처리 제한으로 생략했습니다.
- 초판 당시 외부 조건: OpenAI API 키, 100건 문서 확보, OCR·상용 파서·실제 HWP/HWPX 변환 검증. 실제 API 비용은 발생하지 않았습니다. 상세 근거와 한계는 `textbook/part3/ch10-document-processing/qa/verification.md`에 있습니다.

다음 제안 챕터: **Part 8 Ch35** — Part 7에서 만든 서비스와 변경 검사·복구 기준을 AI 페어 개발 실습에 연결합니다.

## 세션 운영 (2026-09-07 결정)

- 집필 세션: Fable 5.1 · High. 한 세션 = 한 챕터. 본문·코드 실행·도식·Higgsfield 삽화까지 한 흐름으로.
- 검토 세션: Opus 5 · High. 완성 절을 읽고 ⟨감사 3단⟩ + 삽화 검수("그림만 보고 읽히는가").
- 노트북 분할: Sonnet 5 · High (Ch 12·22·23은 Opus 5).
- 예외: Ch 12·21·29는 Fable Extra high.

## 누적 노트

- 2026-09-15 품질 개선 단계 셋업 — `/project` 재진입 인터뷰로 학생 수준 코드(문법 사다리)·쉬운 문장·절당 Mermaid 3~5장과 삽화 1~2장·노트북 설명 보강·실제 모델 temperature 0을 확정했습니다. `textbook/QUALITY-UPGRADE.md`, 체인 ⑨, `easy-upgrade-editor`를 추가하고 `AGENTS.md` §9·§15·§16·§17·§19와 기존 에이전트 3종을 갱신했습니다. 교재 본문·노트북은 아직 고치지 않았습니다. 시범은 Ch 22입니다.

- 2026-09-11 Part 6 집필·통합 — 47절·248셀·도식 47쌍·복습 171문항을 추가했습니다. 116개 화면, 853개 링크, 두 ZIP 정본 대조와 압축 해제 환경의 대표 실습이 통과했습니다. 독립 기술·한국어 검토, 실제 노트북 폴더 cwd 재실행, 역할색 교정과 judge 변동 기록을 반영했습니다. 외부 맞춤법 검사는 스킬의 상업적 대량 처리 제한으로 생략하고 로컬 검토했습니다. 상세: `textbook/part6/qa/verification.md`.

- 2026-09-10 Part 5 집필·통합 — Ch 17–20의 21절·노트북 21개·151개 코드 셀·도식 21쌍·복습 86문항을 추가했습니다. 새 커널 실행, HTML 코드·출력·다운로드 대조, 화면 54건, 로컬 링크 395개, ZIP 정본 해시 대조와 압축 해제 환경의 대표 오프라인 실습을 확인했습니다. 한국어·기술 독립 검토를 반영했으며 외부 맞춤법 검사는 스킬의 상업적 대량 처리 제한으로 생략했습니다. 경미한 코드 스타일 지적과 미검증 범위는 `textbook/part5/qa/verification.md`에 명시합니다.

- 2026-09-10 Part 4 집필·통합 — Ch 13–16의 30절·노트북 30개·코드 셀 191개·SVG/Excalidraw 30쌍·복습 105문항을 추가했습니다. 새 커널 실행, 코드·출력·다운로드 대조, 화면 72건, 로컬 링크 542개, ZIP 해시 대조를 확인했습니다. 언어 검토는 네 챕터 모두 accept이며 외부 맞춤법 전송은 상업적 대량 처리 제한으로 생략했습니다. 최종 근거와 미확인 범위는 `textbook/part4/qa/verification.md`입니다.

- 2026-09-10 Ch8–Ch12 연결성 수정 — Ch9·10의 실제 PDF 검색 로그를 Ch11에 전달하고, Ch11·12의 개발/시험 분리·다중 정답 Recall·빈 정답 제외·후보와 보고 결과의 로그 필드를 맞췄습니다. Ch12의 36개 TF-IDF+MMR 설정과 개발 질문 한 건의 통합 RAG를 구분했습니다. 변경 노트북 14개 새 커널 실행, 24개 코드·출력·메타데이터 보존, 질문 결과 555개 재계산, 원본 로그 49개 보존을 확인했습니다. 최종 실행·배포·독립 검토 기록은 `textbook/part3/qa/chapter-continuity-verification.md`입니다.

- 2026-09-09 Part 1 전체 완성 — 기존 Ch 1·2를 보존하고 Ch 3–5의 18절을 추가했습니다. 전체 35절·노트북 35개·194셀·도식 35쌍·복습 135문항, 새 커널 실행·독립 기술/언어/의미 검토·화면 84건·링크 277개·ZIP 해시 대조를 확인했습니다. 시작점은 `textbook/part1/index.html`, 실습 묶음은 `textbook/downloads/part1-practice.zip`, 검증 기록은 `textbook/part1/qa/verification.md`입니다.

- 2026-09-09 Part 2 전체 완성 — Ch 6·7 신규 14절과 Ch 8 보완 6절, 독립 노트북 20개·180셀, 도식 20쌍·복습 80문항을 확인했습니다. 독립 언어 감사에서 재실행된 지연 시간의 비교 방향을 수정하고 최종 원문 해시를 확정했습니다. 학생 시작점은 `textbook/part2/index.html`, 실습 묶음은 `textbook/downloads/part2-practice.zip`입니다.

- 2026-09-08 노트북 형식 통일 — Ch 8·9·10 총 20절을 Jupyter 테마로 전환했습니다. 코드 셀 116개(최대 15줄)를 Python 3.12.13 새 커널에서 실행했고 실제 OpenAI 생성·임베딩을 확인했습니다. HTML과 노트북 코드·출력·다운로드 대조 통과, 화면·복사 48건 통과. 원본은 각 챕터 qa/notebook-before에 보존했습니다. 학생 시작 페이지는 textbook/index.html입니다.

- 2026-09-08 Ch 9 보완 — 6절과 목차에 Ch 10의 가독성·원본 연결·검증 방식을 적용했습니다. 일반화된 모델 성향·청크 크기·비용 설명을 실제 실험 범위로 좁히고, 보라색 범례를 고정 흐름과 일치시켰습니다. 기존 실행 출력은 보존했으며 최종 독립 정독 판정은 accept입니다.

- 2026-09-08 Ch 10 완성 — 8절·도식 8개·복습 32문항·실행 예제 8개를 작성했습니다. 테스트 38개와 화면 18건을 확인하고 다른 모델의 최종 정독을 마쳤습니다. 실제 임베딩 API·OCR·상용 파서 미실행과 문서 100건 미충족을 본문 및 검증 기록에 명시했습니다.

- 2026-09-08 Ch 8 집필본 완성 — Ch 9를 참고해 6절·복습 24문항·도식 6개·삽화 1장을 작성했습니다. 최종 실행 로그와 교재 숫자를 대조하고 단순 키워드 채점의 모순 통과 가능성, 기준선 출처 메타데이터, 캐시 비용 비교를 보완했습니다. 정식 한국어 3단 감사는 별도 검토 세션에 남겼습니다.

- 2026-09-08 지침 반영 — AGENTS.md §14-4(문어체 어휘 표, "함정" 금지 포함) · §14-5(_src/_build.py/_gen_figures.py 산출물 구조) · §15(샌드박스 uv 우회·비결정 출력 반복·기록 단위=처리 단위·숫자 재확인) · §16(삽화 실무·playwright 4축 실측) · §14-1(검토 반영 절차) · §9 체인 ① 갱신. 에이전트 textbook-writer·figure-maker 동기화.

- 2026-09-08 문체 검토 반영 — 사용자 지적 15건 + 같은 유형 추가 발견분을 Ch 9 `_src/` 6절에서 110곳 수정(§14-4 표). "확인할 점"·"선수 지식 되짚기"·"다음 학습과 이어지는 지점"이 고정 소제목. 다음 챕터부터는 집필 단계에서 §14-4 grep을 통과해야 한다.

- 2026-09-07 Ch 9 집필(6절·도식 5·삽화 3·코드/테스트). 샌드박스 FUSE 마운트에서 `uv sync`가 실패 → `UV_PROJECT_ENVIRONMENT=/tmp/venv-ch09`로 우회(다음 세션도 동일). langchain-community sunset 확인 → 로더는 pypdf 직접 호출로 결정. 시각 품질 4축은 playwright(chromium)로 DOM 실측.

- 2026-09-07 RAG 실습 문서 세트 생성(labs/data/rag-corpus, 가상 기관 8곳 세계관). 긴 문서 실습은 public_pdfs.md 병용.
- 2026-09-07 프로젝트 셋업. 에이전트 3(textbook-writer · lab-notebook-builder · figure-maker), 체인 8.

- 2026-09-08 LangChain 호출 통일 — Ch 6 이후 기본 실습은 생성 `init_chat_model`·`invoke`·`AIMessage.text`, 임베딩 `OpenAIEmbeddings`를 사용합니다. 직접 OpenAI SDK는 Ch 18 등 명시된 학습 목적에 한정합니다. 제공자 사용량과 로컬 토큰 추정값을 구분합니다.
- LangChain 전환 최종 검증: 기본 노트북 20개·116셀(최대 16줄), 변경 12개 새 커널 실제 API 재실행, 직접 SDK import 0건, 화면·복사 48건 통과. 검증 기록: textbook/_notebook/LANGCHAIN-VERIFICATION.md.

- 2026-09-08 Before/After 보완 — 20절의 6번 블록에 실패·수정 코드와 실제 결과 20쌍을 배치했습니다. 준비→Before→After 순서의 136셀(최대16줄)을 새 커널에서 실행했습니다. 전체 복사·노트북 다운로드는 두 블록을 모두 포함합니다. 최신 검증: textbook/_notebook/BEFORE-AFTER-VERIFICATION.md.

- 2026-09-09 학생용 구성 확정 — 20절에서 강사 노트 본문과 목차를 제거했습니다. 복습 문제 다음 참고 자료가 오는 10개 블록을 기본 집필 구조로 적용합니다.

- 2026-09-09 여러 줄 문자열 형식 통일 — 11절의 본문·프롬프트 16곳을 삼중 큰따옴표와 실제 줄바꿈으로 수정했습니다. 문자열 값 보존, 변경 노트북 11개·77셀 새 커널 실제 실행, 전체 20절·136셀 HTML 일치, 화면·복사 46건을 확인했습니다. AGENTS.md §15와 집필 에이전트 및 Ch 8 생성기에 반영했습니다.

- 2026-09-09 초보자용 주석 보강 — 20절·136개 코드 셀에 주석 350줄을 추가했습니다. 기존 코드와 문자열의 AST 동일성을 확인하고 전체를 빈 커널에서 실제 실행했습니다. 독립 검토 지적 9건을 수정한 뒤 해당 노트북을 다시 실행했습니다. 주석 포함 최대 21줄이며 Ch 8 생성기와 집필·노트북 에이전트 지침도 동기화했습니다. 상세 검증: textbook/_notebook/COMMENTS-VERIFICATION.md.

- 2026-09-09 코드 셀 상단 빈 줄처럼 보이던 공간 제거 — 공통 CSS 상단 여백을 44px에서 14px로 줄이고 복사 버튼을 코드 영역 밖으로 옮겼습니다. 전체 20절 재빌드, 136셀 내용·출력 동일, PC·모바일 화면·복사 46건 통과.

- 2026-09-09 개발 입문자용 실습 개편 — 20절을 기본 실행·중간 결과 관찰·값 하나 변경·Before/After 순서로 개편했습니다. 본문·복습·챕터 목차도 실제 노트북과 대조했습니다. 작성 지침과 에이전트 4개를 갱신하고 학생 환경 안내 및 자료 묶음을 제공합니다. 최신 검증: textbook/_notebook/GUIDED-PRACTICE-VERIFICATION.md.

- 2026-09-09 Ch8 05 도식 설명 보완 — 입력 길이·근거 위치의 의미, 칸과 점 읽는 법, 실제 두 조건의 토큰·점수 표를 추가했습니다. 코드가 실행하는 두 칸과 후속 3×3 실험의 범위를 구분합니다. 코드와 출력은 그대로 유지합니다.

- 2026-09-09 Ch8 05 재개편 — 이전 두 조건/질문 검사/배치 오류 BA 및 3×3 위치 도식은 폐기했습니다. 같은 질문·근거 중앙·길이 3개·각 3회로 입력 토큰과 정답을 측정하고 모두 3/3 정답이므로 성능 저하 미관찰로 해석합니다. 이 절은 experiment 형식(BA 없음)이며 19개 기존 절의 BA는 유지합니다.

- 2026-09-09 설명 난도 기준 — 표준 문어체를 어려운 한자어와 추상어로 해석하지 않습니다. 개발 입문자가 무엇을 확인하고 실행할지 한 번에 알 수 있게 설명합니다. 고정 제목은 「이 내용을 배우는 이유」·「앞에서 배운 내용」으로 바꾸고 학습에 필요한 용어는 뜻과 예를 먼저 제공합니다.

- 2026-09-09: Ch8~10 20절·20개 노트북 설명을 개발 입문자 기준으로 정독·수정. 공통 제목과 도식·시작 안내, 작성 지침 동기화. 코드206셀·출력 보존, 화면/복사48건 통과, 독립 의미 검토 승인. 검토 기록: textbook/_notebook/PLAIN-LANGUAGE-REVIEW.md.

- 2026-09-09: 사용자 요청 — 쉬운말 검수 뒤 전20절 주제·실제 코드·출력·Before/After의 학습 목표 일관성을 재검토하고, context rot와 같은 주제 이탈·인위적 검사 실패를 수정한다.

- 2026-09-09: 주제·코드 일관성 전수 검토 완료 — Ch8~10 20절의 목표·정의·코드·출력·Before/After·도식·복습을 대조했습니다. 인위적 검사 실패를 실제 근거 누락·충돌·청크 경계·출처·캐시 문제로 수정하고, 17절은 비교·3절은 실험 해석으로 구성했습니다. 변경15개 노트북 새 커널 실제 실행, 총207셀(최대22줄), 화면/복사48건·공통테스트22개 통과. 최종 기록: textbook/_notebook/TOPIC-ALIGNMENT-REVIEW.md.

- 2026-09-09: 교재 템플릿·새 세션 지침 완료 — textbook/_template 생성기로 비교형과 실험 해석형을 만들고 AUTHORING.md·AGENTS.md·Claude/Codex 에이전트 지침을 동기화했습니다. 실제 원인에 맞는 Before/After, 주제·코드·출력·도식 대조, 초보자용 코드와 새 커널 실행을 필수 기준으로 정했습니다. 테스트 37개 및 하위 검사 16개, 화면·복사 6건 통과. 기존 학생 산출물 43개 내용 동일. 기록: .moai/evolution/template-guidance-verification.md.

- 2026-09-09 Ch 1 작성 — 5절·노트북 5개(25셀)·도식 5쌍·복습 20문항과 A/B 자가진단 6과제를 작성했습니다. 실제 경로 오류, 두 uv 가상환경, pdb 계산값, Git/Docker 응답을 확인하고 도구 미발견 환경도 별도 실행했습니다. 학생 시작 화면·배포 묶음에 등록했습니다.

- 2026-09-11 개념 학습 중심 보강 요청 — 설명이 짧고 공식 문서 요약에 치우친 구성을 개선합니다. 사용자는 비용 설명 추가보다 다양한 상황의 예시와 개념 비교를 원합니다. AUTHORING.md와 템플릿 안내에 기본 예시·다른 상황·비교/반례·결과 해설 기준을 반영했습니다. Ch 1~34의 214절 구조 집계와 장별 보강 예시는 `.moai/evolution/depth-expansion-2026-09-11/concept-depth-review.md`에 있습니다. 이번 대표 개정은 Ch 6이며 나머지 33개 챕터는 보강 후보 단계입니다. 실행·화면·검토 완료 여부는 같은 폴더의 `verification.md`를 확인합니다.

- 2026-09-11 사용자 보정: 교재 설명 부족은 처음 나오는 개념·메서드를 이미 안다고 가정한 학습 순서의 문제입니다. 옵션·예시 개수보다 사용 전 정의·표기·입출력·호출 시점 설명과 실제 선수 학습 위치를 확인합니다. Part 1 Ch 1–5 전35절부터 개정하며 작업 근거는 `.moai/evolution/part1-learning-sequence-2026-09-11/`에 남깁니다.

- 2026-09-11 Part 1 학습 순서 개정 완료 — Ch 1–5 전35절·대응 노트북 35개에 첫 사용 정의·표기·입출력·호출 시점과 실제 선수 학습을 보완했습니다. 기본 예제 뒤에 조건 비교를 배치하고 미관찰 원인 추론을 수정했습니다. 199셀(최대25줄) 코드·출력 일치, 화면84건, 링크309개, ZIP 정본 해시 대조를 확인했습니다. 검증·독립 정독 근거는 `.moai/evolution/part1-learning-sequence-2026-09-11/verification.md`입니다.

- 2026-09-14 Part 2~7 학습 순서·개념 깊이 개정 완료 — Ch6~34의 179절·대응 노트북 179개에 첫 사용 정의·표기·입출력·호출 시점을 보완하고 다양한 비교 사례와 실제 결과 해설을 배치했습니다. 반복 문단과 실행하지 않은 동작의 설명을 교정하고 활성 생성기를 동기화했습니다. 1,161셀 코드·출력·다운로드 대조, 변경 노트북 9개/55셀 새 커널 실행, 나머지 170개 코드·출력 보존, 화면430건·링크3,152개·복습684문항·ZIP7개 정본 대조를 확인했습니다. Part1 추적파일129개 보존, 미작성 Part8 제외. 독립 기술·한국어 검토7범위 corrected이며 외부 맞춤법 검사는 스킬의 대량 처리 제한으로 생략했습니다. 최종 근거: `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/verification.md`.
