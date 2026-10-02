# Ch 6 LangChain 시작 실습

Python 3.12와 `uv`를 사용합니다. 프로젝트 루트의 `.env`에서 API 키를 읽으며 키 값은 출력하지 않습니다. 여섯 노트북은 각각 새 커널에서 독립 실행할 수 있습니다. Anthropic과 Google 키가 없으면 관련 비교 행은 `skipped`로 기록됩니다.

챕터 폴더를 VS Code에서 열고 다음 명령으로 잠금 환경을 준비합니다.

```bash
uv sync --locked
```

그런 다음 이 폴더의 `.venv`를 노트북 커널로 선택합니다. 첫 실제 API 호출은 `01-계층-지도와-첫-호출.ipynb`의 `invoke()` 셀에서 일어납니다. `06-토큰-비용-지연-비교.ipynb`은 실행할 때마다 `runs/provider-comparison-continuity.json`을 새 기록으로 덮어씁니다(실행 시각별 사본은 만들지 않습니다). Ch 7의 08절 노트북이 이 파일을 읽습니다.
