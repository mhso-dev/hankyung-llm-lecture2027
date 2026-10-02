# Ch 7 — 프롬프트 엔지니어링 실습

`notebooks/`의 8개 노트북은 각각 빈 Python 3.12 커널에서 독립 실행합니다. 모든 실습은 같은 고객 문의와 같은 평가 항목을 사용하며, 프롬프트 조건만 바꾸어 원문 응답·토큰·지연 시간·평가 결과를 비교합니다.

모델은 LangChain `init_chat_model("openai:gpt-5.4-mini")`로 초기화합니다. 응답은 `AIMessage.text`, 사용량은 `AIMessage.usage_metadata`에서 읽습니다. `.env`에서는 `OPENAI_API_KEY`의 존재만 확인하며 키 값은 출력하거나 노트북에 저장하지 않습니다.

모델 출력은 실행마다 달라질 수 있습니다. 실습은 실패를 만들기 위해 질문이나 평가 기준을 바꾸지 않으며, 관찰되지 않은 실패는 관찰했다고 기록하지 않습니다.

챕터 폴더를 VS Code에서 열고 `uv sync --locked`를 실행한 뒤 이 폴더의 `.venv`를 노트북 커널로 선택합니다. 노트북은 새 커널에서 각각 실행할 수 있지만, `08-프롬프트-버전과-AB-비교.ipynb`은 Ch 6의 `runs/provider-comparison-continuity.json`을 읽어 공통 필드와 지문을 확인합니다. 배포본에는 검증한 정본이 함께 들어 있습니다.

`runs/prompt-ab-continuity.json`은 현재 학생 노트북의 정본입니다. `runs/continuity/<실행 시각>/`은 재실행 전 결과를 보존합니다. `runs/prompt-ab-v1.json`은 이전 구현의 증거로 남겨 두었으며 현재 노트북이 덮어쓰지 않습니다.
