# Ch31 공식 문서 조사

- 조사일: 2026-09-11
- 학습자 수준: 개발 입문자부터 기초 웹 개발 경험자
- 실습 환경: PostgreSQL 17.8, pgvector 0.8.1, Python 3.12.13

## SQLAlchemy 비동기와 풀

SQLAlchemy 2.0 공식 비동기 문서는 `async_sessionmaker`가 고정 설정의 `AsyncSession` 팩터리를 만들며, 비동기 문맥 관리자가 세션을 닫는 흐름을 설명합니다. 세션 기본 문서는 `AsyncSession`이 변경 가능한 한 논리 트랜잭션을 나타내므로 여러 동시 작업이 하나를 공유하지 않아야 한다고 명시합니다. 연결 풀 문서는 비동기 엔진이 `AsyncAdaptedQueuePool`을 사용하고 `pool_size`, `max_overflow`, `timeout`으로 제한과 대기를 설정한다고 설명합니다.

- https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- https://docs.sqlalchemy.org/en/20/orm/session_basics.html
- https://docs.sqlalchemy.org/en/20/core/pooling.html

## 트랜잭션과 PostgreSQL

PostgreSQL 공식 문서는 기본 READ COMMITTED에서 각 문장이 시작되기 전에 커밋된 행을 본다고 설명합니다. REPEATABLE READ와 SERIALIZABLE은 더 넓은 스냅샷 일관성을 제공하지만, SERIALIZABLE 충돌은 `serialization_failure`로 한 트랜잭션을 롤백할 수 있습니다. 교재는 격리 수준 전체 실험 대신 원자성의 최소 실패와 롤백을 실행합니다.

- https://www.postgresql.org/docs/current/sql-set-transaction.html
- https://docs.sqlalchemy.org/en/20/core/connections.html

## Alembic

Alembic 공식 튜토리얼은 리비전 계보, `upgrade`, `downgrade`와 버전 표를 설명합니다. 자동 생성 문서는 모델과 데이터베이스의 차이를 후보 마이그레이션으로 만들며 결과를 직접 검토해야 한다고 안내합니다. 실습은 수동 리비전 한 개로 표 생성, 제거, 재생성을 확인합니다.

- https://alembic.sqlalchemy.org/en/latest/tutorial.html
- https://alembic.sqlalchemy.org/en/latest/autogenerate.html

## pgvector와 백업

pgvector 공식 저장소는 HNSW가 근사 최근접 이웃 인덱스이며 거리 함수마다 맞는 연산자 클래스를 사용해야 한다고 설명합니다. 코사인 거리는 `vector_cosine_ops`를 사용합니다. PostgreSQL `pg_dump` 문서는 데이터베이스를 SQL 또는 아카이브로 추출하는 논리 백업 도구의 옵션과 복원 흐름을 설명합니다.

- https://github.com/pgvector/pgvector
- https://www.postgresql.org/docs/current/app-pgdump.html
- https://github.com/langchain-ai/langgraph/tree/main/libs/checkpoint-postgres

## 버전 판단

프로젝트 기준에 맞춰 LangGraph 1.2.11을 고정했습니다. pgvector 서버 확장은 독립 컨테이너 이미지의 0.8.1을 실제 사용했고 Python 어댑터는 0.4.1을 고정했습니다. 커리큘럼 기준보다 최신 PostgreSQL 공식 문서가 18을 가리키는 항목은 본문에서 실습 서버 17.8과 구분했습니다.

