# Ch23 Persistence와 Durable Execution 실습

Python 3.12 새 커널에서 노트북을 첫 셀부터 실행합니다. 02절은 로컬 PostgreSQL의 `ch23_lab` 스키마를 사용합니다. 나머지 절은 로컬 SQLite 또는 메모리 체크포인터를 사용합니다. 04절과 06절은 제공된 자식 프로세스를 실제로 종료하고 저장된 상태와 로컬 부작용 파일을 확인합니다.

02절을 실행하기 전에 프로젝트 루트의 터미널에서 다음 컨테이너를 시작합니다.

```bash
docker run --name kdt-ch23-postgres -e POSTGRES_PASSWORD=postgres -p 55432:5432 -d postgres:17
```

`docker exec kdt-ch23-postgres pg_isready -U postgres`가 `accepting connections`를 출력하면 노트북을 실행합니다. 실습을 마친 뒤에는 다음 명령으로 컨테이너를 중지하고 제거합니다.

```bash
docker rm -f kdt-ch23-postgres
```
