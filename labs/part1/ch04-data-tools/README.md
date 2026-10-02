# Ch 4 데이터 도구 실습

Python 3.12와 uv를 사용합니다. 외부 API 키는 필요하지 않으며 REST 실습은 노트북이나 pytest가 컴퓨터에서 잠시 실행하는 교육용 HTTP 서버에만 접속합니다. 압축을 풀고 `labs/part1/ch04-data-tools` 폴더에서 터미널을 연 뒤 다음 명령을 실행합니다.

```text
uv sync --locked
uv run python -m pytest
```

VS Code에서 이 폴더의 `.venv` 커널을 고른 뒤 각 노트북을 첫 셀부터 실행합니다. 노트북은 서로 변수를 공유하지 않습니다. `data_tools.py`의 `fetch_orders`는 Ch 19 01절에서 도구의 실행 함수로 다시 씁니다. `data/article-text.json`은 05 노트북이 `data/article.html`을 파싱해 씁니다. pytest는 이 파일이 `parse_article_html()` 결과와 같은지 확인하고, Ch 5 01절은 이 파일을 읽습니다. 입력 자료의 뜻과 출처는 `data/README.md`에서 확인합니다.
