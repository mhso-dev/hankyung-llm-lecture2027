# Ch31 DB & 상태 영속화 실습

다섯 노트북은 PostgreSQL 17과 pgvector 0.8.1이 있는 독립 실습 데이터베이스를 사용합니다. 다른 데이터베이스를 수정하지 않도록 각 절은 `ch31_async`, `ch31_tx`, `ch31_migration`, `ch31_shared` 전용 스키마만 다시 만듭니다.

프로젝트 루트에서 실습 컨테이너를 시작합니다.

```bash
docker run --name kdt-ch31-postgres \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=ch31_lab \
  -p 55431:5432 -d pgvector/pgvector:0.8.1-pg17
docker exec kdt-ch31-postgres pg_isready -U postgres
```

기본 접속 주소는 로컬 실습 전용입니다. 다른 주소를 쓸 때만 `.env`의 `CH31_DATABASE_URL`에 `postgresql+asyncpg://...` 형식으로 지정합니다. 노트북과 서비스 코드는 비밀 값을 출력하지 않습니다.

```bash
uv sync --project labs/part7/ch31-database
uv run --project labs/part7/ch31-database python -m app.service
```

`app/`은 비동기 엔진, 모델, 트랜잭션 서비스의 최소 예제입니다. `migrations/`는 `ch31_migration.tickets` 표를 적용하고 롤백합니다. 노트북을 모두 마친 뒤 실습 컨테이너는 `docker rm -f kdt-ch31-postgres`로 제거할 수 있습니다.

