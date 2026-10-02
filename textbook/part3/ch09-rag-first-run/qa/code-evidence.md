# Ch 9 코드·출력 연결 검증

교재 6개 절과 목차의 30개 `<pre>` 블록은 `_src/`에 코드나 출력 사본을 두지 않습니다. `{{code:파일#심볼}}`은 빌드할 때 `labs/part3/ch09-rag-first-run/`의 실제 파일에서 가져오고, `{{output:파일}}`은 `runs/examples/`의 출력 증거를 가져옵니다.

2026-09-08 보완 전 `uv run --python 3.12 pytest -q` 결과는 `10 passed in 7.47s`였습니다. API 키가 설정된 환경이어서 검색 테스트 하나가 `text-embedding-3-small` 색인·질의 임베딩을 호출했습니다. 생성 모델 호출은 없었습니다. 미화 0.001달러 미만이라는 값은 청구 실측이 아니라 입력 규모와 고정 단가에 따른 추정입니다.

`examples/ex02_load_split.py`는 API를 사용하지 않고 다시 실행했습니다. 출력은 기존 교재와 같으며 `runs/examples/ex02.txt`에 저장했습니다. 나머지 `_preserved.txt` 파일은 `qa/before/`의 기존 출력 블록과 글자 단위로 대조합니다. API 출력은 다시 실행하지 않았습니다.

검증 명령:

```bash
/Users/mhso/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 textbook/part3/ch09-rag-first-run/_build.py
/Users/mhso/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 textbook/part3/ch09-rag-first-run/qa/check_content.py
uv run --project labs/part3/ch09-rag-first-run pytest -q textbook/part3/ch09-rag-first-run/qa/test_code_evidence.py
uv run --project labs/part3/ch09-rag-first-run pytest -q labs/part3/ch09-rag-first-run/tests
```

출력의 실행 시점과 재현 여부는 `labs/part3/ch09-rag-first-run/runs/examples/MANIFEST.md`에 기록했습니다.

최종 결과(2026-09-08): 원본 연결 30블록, 과거 출력 스냅샷 12블록, 출력 manifest SHA-256 12파일이 모두 일치했습니다. 새 연결 회귀 3개와 기존 실습 회귀 10개를 함께 실행해 `13 passed`를 확인했고, Ruff·`compileall`·셸 구문 검사도 통과했습니다.
