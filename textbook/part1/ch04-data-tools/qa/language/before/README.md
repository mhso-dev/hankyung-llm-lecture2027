# Ch 4 데이터 도구 실습

Python 3.12와 uv를 사용합니다. 외부 API 키는 필요하지 않으며, REST 실습은 노트북이나 pytest가 컴퓨터 안에서 잠시 여는 교육용 HTTP 서버에만 접속합니다.

```text
uv sync --locked
uv run python -m pytest
```

VS Code에서 이 폴더의 `.venv` 커널을 고른 뒤 각 노트북을 첫 셀부터 실행합니다. 노트북은 서로 변수를 공유하지 않습니다. `data_tools.py`의 `fetch_orders`, `find_customer_orders`, `fetch_articles`는 Ch 19에서 에이전트 도구로 감쌀 수 있는 재사용 함수입니다. 입력 자료의 뜻과 출처는 `data/README.md`에서 확인합니다.

