# Ch18 워크플로우 5패턴 실습

Python 3.12와 OpenAI Python SDK만으로 다섯 워크플로우 패턴을 구현합니다. 각 노트북은 새 커널에서 독립적으로 실행되며 프로젝트 루트의 `.env`에서 `OPENAI_API_KEY`를 읽습니다. 키 값은 출력하지 않습니다.

실습 모델은 `gpt-5.4-mini`입니다. 호출마다 `max_output_tokens`와 호출 수를 제한하며, 실행 전에 `textbook/part5/ch18-workflow-patterns/qa/research.md`의 비용 상한을 확인합니다. API 가격과 모델 동작은 바뀔 수 있으므로 다시 실행할 때 공식 모델 페이지를 확인합니다.
