# Ch 31 DB & 상태 영속화 실습

이 폴더는 에이전트 서비스가 쓰는 자료와 실행 상태를 PostgreSQL 데이터베이스에 남기는 방법을 배우는 실습 폴더입니다. 제목의 DB는 데이터베이스이고, 상태 영속화는 Ch 23에서 배운 상태 저장과 같은 뜻입니다. 노트북 여섯 개(`notebooks/01~06-*.ipynb`)는 Python 3.12 새 커널에서 절마다 따로 실행할 수 있고, 앞 절 노트북의 변수는 쓰지 않습니다.

여섯 노트북은 모두 모델을 부르지 않습니다. 그래서 API 키가 필요 없고, 노트북은 `.env` 파일을 읽지 않습니다. 대신 아래 PostgreSQL 서버가 켜져 있어야 합니다.

## 데이터베이스 준비

여섯 절은 Docker 컨테이너 `kdt-ch31-postgres` 하나를 함께 씁니다. 컨테이너가 없으면 터미널에서 아래 명령으로 먼저 만듭니다. 01절 노트북 맨 위 준비물의 명령과 같습니다.

```bash
docker run --name kdt-ch31-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ch31_lab \
  -p 127.0.0.1:55431:5432 \
  -d pgvector/pgvector:0.8.1-pg17
```

- 비밀번호 `postgres`는 이 실습에서만 쓰는 연습용 값입니다. 다른 서버에는 쓰지 않습니다.
- 줄 `-p 127.0.0.1:55431:5432`는 이 컴퓨터 안에서만 서버에 붙을 수 있게 묶는 설정입니다. 주소를 빼면 Docker는 이 컴퓨터 밖에서도 붙을 수 있게 엽니다.
- 컨테이너가 꺼져 있으면 `docker start kdt-ch31-postgres`로 다시 켭니다. 실습을 마치면 `docker stop kdt-ch31-postgres`로 끄고, 데이터까지 지우려면 `docker rm -f kdt-ch31-postgres`를 씁니다.

노트북은 설정 셀에 적은 연습용 접속 글로 서버에 붙습니다. 01·02·04절은 비동기 드라이버 asyncpg를 씁니다. 03·05·06절은 동기 드라이버 psycopg를 써서, 접속 글의 앞부분만 다릅니다. 서버를 다른 주소나 계정으로 켰다면 노트북 설정 셀의 글만 고칩니다.

```text
postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab   01·02·04절
postgresql+psycopg://postgres:postgres@127.0.0.1:55431/ch31_lab   03·06절
postgresql://postgres:postgres@127.0.0.1:55431/ch31_lab           05절, 06절 체크포인터
```

교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다. pgvector 확장은 0.8.1입니다. 그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다. Docker 이미지 `pgvector/pgvector:0.8.1-pg17`은 pgvector 0.8.1과 PostgreSQL 17을 담습니다. 다만 서버 버전의 끝자리는 교재 출력과 다를 수 있습니다. Docker 컨테이너와 Windows·macOS에서는 교재 출력을 만들지 않았습니다.

## 준비

실습 폴더(`labs/part7/ch31-database`, 학생 묶음이면 `part7-practice/labs/part7/ch31-database`)에서 `uv sync --locked`를 실행하고, 이 폴더의 `.venv` 커널을 고릅니다. 그다음 `notebooks/` 폴더의 노트북을 열어 첫 셀부터 차례로 실행합니다.

노트북의 첫 코드 셀은 그 절에서 쓰는 패키지를 설치하고 버전 번호를 출력합니다. 모두 실습 폴더 잠금(`uv.lock`)과 같은 버전입니다.

- 01·02·04절: `sqlalchemy[asyncio]` 2.0.43, `asyncpg` 0.30.0
- 03절: `sqlalchemy` 2.0.43, `psycopg[binary]` 3.3.3, `alembic` 1.16.5
- 05절: `psycopg[binary]` 3.3.3, `langgraph` 1.2.11, `langgraph-checkpoint-postgres` 3.0.5
- 06절: `sqlalchemy` 2.0.43, `psycopg[binary]` 3.3.3, `langgraph` 1.2.11, `langgraph-checkpoint-postgres` 3.0.5

## 노트북 여섯 개와 모델 요청

| 절 | 노트북 | 하는 일 | 이름 공간 | 모델 요청 |
|---|---|---|---|---|
| 01 | `01-SQLAlchemy-비동기-PostgreSQL.ipynb` | 비동기 엔진과 연결 풀을 만들고, 조회 셋을 차례로 기다릴 때와 `gather()`로 함께 기다릴 때를 견줍니다 | `ch31_async` | 0번 |
| 02 | `02-트랜잭션과-원자성.ipynb` | 두 계좌 이체를 블록 둘로 따로 확정할 때와 한 묶음 작업으로 확정할 때를, CHECK 제약 위반으로 견줍니다 | `ch31_tx` | 0번 |
| 03 | `03-Alembic-적용과-롤백.ipynb` | Alembic으로 판을 올리고 내리며, 줄이 든 표에 기본값 없는 NOT NULL 칸을 더하는 판이 막히는 것을 봅니다 | `ch31_migration` | 0번 |
| 04 | `04-커넥션-풀-고갈과-대응.ipynb` | 풀 크기 1인 엔진에서 닫지 않은 연결 때문에 다음 요청이 연결을 받지 못하는 것과, 반납해 고치는 것을 봅니다 | 만들지 않음 | 0번 |
| 05 | `05-pgvector-체크포인터-공존과-백업.ipynb` | 한 이름 공간에 pgvector 문서 표·HNSW 색인과 체크포인터 표를 두고, `pg_dump`로 백업해 `pg_restore`로 복원합니다 | `ch31_shared`, 복원 데이터베이스 `ch31_restore` | 0번 |
| 06 | `06-DB와-상태-영속화-실습.ipynb` | 챕터 끝 실습 절입니다(아래) | `ch31_practice` | 0번 |

노트북은 제 이름 공간을 처음에 지우고 다시 만들며, 끝에서 지웁니다. 그래서 노트북을 처음부터 다시 실행해도 같은 출력이 나옵니다. 05절이 만든 확장 `vector`는 데이터베이스 `ch31_lab`에 남습니다.

노트북은 작업 폴더에 파일을 쓰지 않습니다. 03절은 `alembic.ini`와 `migrations/`를 운영체제 임시 폴더에 복사하고, 그 사본에만 새 판 파일을 씁니다. 05절은 덤프 파일 하나를 운영체제 임시 폴더에 씁니다. 03절의 파일 위치 셀은 `notebooks/` 폴더, 실습 폴더 맨 위, 프로젝트 맨 위 세 자리에서 실습 폴더를 찾습니다. 나머지 절은 실습 폴더의 파일을 읽지 않습니다.

## 05절의 백업 명령

05절은 PostgreSQL의 명령 `pg_dump`와 `pg_restore`를 부릅니다. 이 컴퓨터에 `pg_dump`가 있으면 그것을 쓰고, 없으면 컨테이너 `kdt-ch31-postgres` 안의 명령을 `docker exec -i`로 부릅니다. 교재 출력은 서버와 같은 17.11 버전의 명령을 이 컴퓨터에서 불러 만들었고, 컨테이너 쪽 갈래는 실행하지 않았습니다.

PostgreSQL 문서는 `pg_dump`가 제 주 버전(앞자리)보다 새 서버에서는 백업을 받지 않는다고 적습니다. 더 높은 주 버전이 만든 파일을 낮은 주 버전 서버에 넣는 것도 장담하지 않습니다. 그래서 이 컴퓨터의 `pg_dump` 앞자리가 17이 아니면 컨테이너 안의 명령을 씁니다. 05절 노트북 5절의 첫 셀에서 `pg_dump_found = shutil.which("pg_dump")` 다음 줄에 `pg_dump_found = None`을 더하면 됩니다.

백업 셀은 명령이 실패해도 멈추지 않습니다. 출력 줄 `pg_dump 종료 코드:`가 0인지 꼭 확인합니다.

## 실습 폴더의 파일

- `alembic.ini`·`migrations/` — Alembic 설정과 판 파일 폴더입니다. 첫 판 `migrations/versions/20260911_01_create_tickets.py`는 이름 공간 `ch31_migration`에 표 `tickets`를 만듭니다. 파일 `migrations/env.py`는 환경 변수 `CH31_SYNC_URL`에서 접속 글을 읽고, 없으면 `localhost:55431`로 붙습니다. 03절 노트북은 이 폴더의 사본으로 판을 올리고 내리며, 실습 폴더의 파일은 고치지 않습니다.
- `app/` — ORM 모델 클래스(`app/models.py`)와 `AsyncSession`(`app/db.py`)으로 표 `tickets`의 질문을 읽는 짧은 예제입니다. 노트북은 이 패키지를 쓰지 않습니다. 파일 `app/db.py`는 환경 변수 `CH31_DATABASE_URL`에서 접속 글을 읽고, 없으면 `localhost:55431`로 붙습니다.

노트북 밖에서 이 둘을 실행하려면, 실습 폴더 맨 위에서 아래 명령을 차례로 실행합니다. 모듈 `app`은 실습 폴더 맨 위에서만 찾을 수 있어, 프로젝트 맨 위에서 `python -m app.service`를 실행하면 `ModuleNotFoundError`로 멈춥니다.

```bash
export CH31_SYNC_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:55431/ch31_lab
export CH31_DATABASE_URL=postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab
uv run alembic upgrade head      # 첫 판을 올려 표 tickets를 만듭니다
uv run python -m app.service     # 표의 질문 목록을 출력합니다(빈 표라 [])
uv run alembic downgrade base    # 판을 내려 표 tickets를 지웁니다
```

교재를 만들 때 Linux에서 같은 차례로 실행해, `[]`가 출력되는 것을 확인했습니다. 환경 변수를 정하지 않으면 두 파일의 기본 글 `localhost`로 붙습니다. 컨테이너를 `127.0.0.1`에만 묶었으므로, 위처럼 `127.0.0.1`을 적는 편이 안전합니다. 03절 노트북은 시작할 때 이름 공간 `ch31_migration`을 지우고 다시 만들어, 위 명령을 먼저 실행해도 03절 출력은 달라지지 않습니다.

## 06절 실습 — 상담 예약 그래프에서 처음 상담 시간 하나만 바꾸기

노트북 `notebooks/06-DB와-상태-영속화-실습.ipynb`는 챕터 끝 실습 절입니다. 30분 안팎의 분량이고, 따로 내는 과제와 새 문법은 없습니다. 02절 한 묶음 작업, 04절 작은 연결 풀과 반납, 05절 체크포인터를 상담 예약 그래프 하나로 잇습니다.

실행 1은 처음 상담 시간 50분으로 문의 셋을 보내고, 실행 2는 처음 상담 시간 하나만 30분으로 바꿔 두 실행을 견줍니다. 모델을 부르지 않아 모델 요청은 0번입니다. 앞에서 배운 함수를 모은 도구 파일은 이 챕터에 없고, 노트북이 쓰는 파일도 없습니다.
