# Ch28 MCP 실습

Python 3.12와 uv를 사용합니다. 프로젝트 루트에서 다음 명령으로 각 노트북을 새 커널에서 실행합니다.

```bash
uv run --project labs/part6/ch28-mcp \
  --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip \
  python textbook/_notebook/execute.py \
  labs/part6/ch28-mcp/notebooks/*.ipynb --cwd "$(pwd)"
```

`course_server.py`는 도구·리소스·프롬프트를 제공하는 읽기 전용 FastMCP 서버입니다. 01·02절은 API 키가 필요하지 않습니다. 03·04절은 로컬 stdio 하위 프로세스를 시작했다가 어댑터 컨텍스트가 끝날 때 종료합니다. 05절의 실제 모델 토큰 측정에만 `.env`의 `OPENAI_API_KEY`가 필요합니다. 키 값은 출력하지 않습니다.

학생 배포 파일은 이 README, `course_server.py`, `pyproject.toml`, `uv.lock`, `notebooks/*.ipynb`입니다. `.env`, `.venv`, 실패 진단 JSON은 배포하지 않습니다.
