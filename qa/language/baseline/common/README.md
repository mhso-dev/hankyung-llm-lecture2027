# Ch32 Docker 실습

이 폴더는 Ch30 결과에 의존하지 않는 최소 FastAPI 서비스입니다. `Dockerfile.baseline`과 `Dockerfile`을 각각 빌드해 크기와 레이어를 비교한 뒤 `docker compose up --build --wait`로 app, PostgreSQL, pgvector 스택을 실행합니다.

`secrets/db_password.txt.example`은 공개 실습용 값입니다. 운영 환경에서는 버전 관리 밖에 실제 시크릿 파일을 만들고 Compose의 `secrets.file` 경로를 바꿉니다.

```bash
docker build -f Dockerfile.baseline -t ch32-baseline:local .
docker build -f Dockerfile -t ch32-optimized:local .
docker compose -p ch32-course-stack up --build --wait
curl http://127.0.0.1:18332/ready
curl http://127.0.0.1:18332/vector-count
docker compose -p ch32-course-stack down --volumes
```
