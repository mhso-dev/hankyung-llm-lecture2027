# Ch32 공식 문서 조사

- Dockerfile 명령과 레이어: RUN, COPY, WORKDIR, CMD 의미와 명령별 레이어 생성 원리를 확인했습니다. https://docs.docker.com/build/concepts/dockerfile/
- 멀티스테이지 빌드: 여러 FROM, 이름 있는 stage, COPY --from과 target 빌드를 확인했습니다. https://docs.docker.com/build/building/multi-stage/
- 빌드 캐시: COPY 입력이나 RUN 명령이 바뀌면 해당 레이어와 뒤 레이어의 캐시가 무효화되는 규칙을 확인했습니다. https://docs.docker.com/build/cache/
- Docker 빌드 권장 사항: 작은 기반 이미지, .dockerignore, 멀티스테이지, 불필요한 패키지 제외를 확인했습니다. https://docs.docker.com/build/building/best-practices/
- uv Docker 통합: 고정 uv 이미지에서 바이너리 복사, uv sync --locked, .venv 제외, 의존성과 프로젝트 설치 분리 지침을 확인했습니다. https://docs.astral.sh/uv/guides/integration/docker/
- Compose 시작 순서: depends_on의 service_healthy 조건과 pg_isready 예제를 확인했습니다. https://docs.docker.com/compose/how-tos/startup-order/
- Compose 시크릿: 서비스별 허용과 /run/secrets/<name> 파일 mount를 확인했습니다. https://docs.docker.com/compose/how-tos/use-secrets/
- Compose 로그: --tail, --since, --follow 옵션의 의미를 확인했습니다. https://docs.docker.com/reference/cli/docker/compose/logs/
- pgvector: 공식 이미지 태그와 0.8.6-pg17-bookworm 지원을 확인했습니다. https://github.com/pgvector/pgvector

확인일은 2026-09-11입니다. 실습은 Docker Engine 29.4.1, Docker Desktop 4.71.0, Compose 5.1.3, uv 0.12.13, FastAPI 0.135.1, PostgreSQL 17.11, pgvector 0.8.6에서 검증했습니다.
