# Ch34 비용 · Rate Limit 엔지니어링 실습

Python 3.12와 uv를 사용합니다. 01과 03은 루트 `.env`의 `OPENAI_API_KEY`로 LangChain을 통해 실제 OpenAI 모델 API를 호출합니다. 02는 Responses API용 Batch 입력을 만들고 검증하지만 제출하지 않습니다. 04의 429는 로컬 HTTP 서버에서만 재현합니다.

```bash
uv sync
uv run --with nbclient==0.11.0 --with ipykernel==7.3.0 python ../../../textbook/_notebook/execute.py notebooks/*.ipynb --cwd notebooks
```
