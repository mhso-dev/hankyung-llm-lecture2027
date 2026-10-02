# Ch 8 노트북 전환 및 검증 기록

## 정리 계획

1. 기존 `_src/` 원본을 `qa/notebook-before/`에 보관합니다.
2. 실행 예제의 긴 모듈 코드와 과거 출력은 절별 독립 노트북으로 교체합니다.
3. 각 노트북은 개념 설명 뒤에 15줄 안팎의 짧은 코드 셀을 배치하고, 빈 커널에서 순서대로 실행합니다.
4. API 예제는 LangChain `init_chat_model("openai:gpt-5.4-mini")`와 `invoke()`를 사용하며 `.env`의 키 값은 출력하지 않습니다.
5. 기존 회귀 테스트, 노트북 전체 실행, 셀 길이와 금지 패턴 검사를 통과한 뒤 HTML을 다시 빌드합니다.

## LangChain 전환 계획

1. 현재 실행 완료 노트북과 `_src/`를 `qa/langchain-before/`에 보관합니다.
2. Ch 9와 같은 `langchain==1.4.0`, `langchain-openai==1.6.0` 조합으로 의존성을 고정합니다.
3. 여섯 노트북의 모델 호출을 `init_chat_model()`과 메시지 튜플 목록, `invoke()`로 바꿉니다.
4. 답은 `AIMessage.text`, 토큰은 `AIMessage.usage_metadata`에서 읽고 사용량이 없으면 실행을 실패 처리합니다.
5. 기존 실험·실패·측정 조건을 유지한 채 새 커널에서 실제 모델을 한 번씩 재검증합니다.

## 변경 전 기준선

- 실행일: 2026-09-08
- 명령: `uv run pytest -q`
- 결과: `16 passed in 0.56s`
- `.env` 파일: 있음
- `OPENAI_API_KEY`: 있음(값은 출력하지 않음)
- LangChain 전환 직전 회귀 테스트: `16 passed in 0.61s`

## 변경 후 검증

- 실행일: 2026-09-08
- 실행 환경: Python 3.12, 빈 Jupyter 커널, 프로젝트 루트를 작업 폴더로 지정
- 실행 명령: `uv -q run --project labs/part2/ch08-context-engineering --with nbclient --with ipykernel --with pip --with python-dotenv python textbook/_notebook/execute.py labs/part2/ch08-context-engineering/notebooks/*.ipynb`
- 결과: 6개 노트북 모두 `passed`
- API 호출: 11회. 01~03절과 06절은 각 1회, 04절은 다섯 입력 조건으로 5회, 05절은 길이 비교를 위해 2회 실행
- 모델 초기화: `init_chat_model("openai:gpt-5.4-mini")`
- 호출과 응답: 메시지 튜플 목록을 `invoke()`에 전달하고 `AIMessage.text`에서 답을 읽음
- 사용량: `AIMessage.usage_metadata`가 `None`이면 실행을 중단하며, 제공된 `input_tokens`, `output_tokens`, `total_tokens` 가운데 실습에 필요한 입력·출력 값을 기록
- 의존성: `langchain==1.4.0`, `langchain-openai==1.6.0`; `uv lock --check` 통과
- 코드 셀: 38개, 셀 하나의 최대 길이 13줄
- 실패 실습: 6개 셀 모두 예상한 `ValueError`를 포착했고, 오류가 발생하지 않으면 `AssertionError`로 검증이 실패하도록 구성
- 자격 증명 검사: 공용 실행기가 환경 변수와 `.env`의 API 키를 실행 결과에서 검사했으며 저장된 키는 0건
- 회귀 테스트: `uv run pytest -q` 결과 `16 passed in 0.49s`
- 정적 검사: `uv run ruff check _make_notebooks.py` 결과 `All checks passed!`

| 노트북 | 코드 셀 | 실제 API 결과에서 확인한 항목 | 검증 상태 |
|---|---:|---|---|
| 01 컨텍스트와 토큰 예산 | 6 | 월요일과 `[E01 p.2]`, 입력·출력 토큰 | 통과 |
| 02 Write와 Select | 7 | 7권과 90분, 각 문서 식별자 | 통과 |
| 03 Compress와 Isolate | 6 | 사실·조건·예외·출처 | 통과 |
| 04 네 가지 실패 모드 | 6 | 기준·Poisoning·Distraction·Confusion·Clash의 실제 응답 비교 | 통과 |
| 05 Context rot 측정 | 6 | 짧은 입력 65토큰, 긴 입력 1,145토큰, 두 답의 월요일과 출처 | 통과 |
| 06 단계적 공개와 설계 비교 | 7 | 선택한 대출 규정의 권수·기간·연장 조건·출처 | 통과 |

LangChain 전환 후 04절 실행에서 clean은 월요일, poisoning은 월요일·화요일과 추가 확인 표현, distraction은 월요일, confusion은 월요일·화요일과 추가 확인 표현, clash는 월요일·수요일과 추가 확인 표현을 출력했습니다. 자동 문자열 표는 관찰 위치를 찾는 데만 사용하고, 완결된 정답 여부는 응답 원문을 읽어 판단해야 합니다.

03절의 압축 결과는 `fact`, `condition`, `exception`, `source` 순서로 출력되었습니다. 필드 순서는 집합 순회에 맡기지 않고 코드의 튜플에 고정했습니다.

실행 결과는 각 `.ipynb`에 저장했습니다. 공용 실행기는 코드와 출력의 SHA-256, 실행 시각, 새 커널 사용 여부를 노트북 메타데이터에 기록합니다. API 응답은 비결정적이므로 재실행하면 출력 해시와 토큰 수가 달라질 수 있습니다.

## 검수 메모

새로 작성한 본문과 노트북 설명을 AI 슬롭 검수 기준으로 확인했습니다. AI식 도입부, 의미 없는 전환어 반복, 수사적인 `A가 아니라 B` 구조, 대시 대비 헤드라인은 발견되지 않았습니다. 실행 예제의 설명은 기존 교재의 `~합니다`체와 기술 용어를 유지했습니다.

## 제한 사항

- 05절의 두 호출은 실행 방법을 익히는 최소 예제입니다. 두 결과만으로 긴 입력의 일반적인 품질 저하를 결론 내릴 수 없습니다.
- 노트북은 현재 작업 폴더의 상위 경로에서 `.env`를 찾습니다. 프로젝트 밖의 폴더에서 열었다면 `.env`가 있는 프로젝트 폴더를 작업 폴더로 지정해야 합니다.
- HTML 빌드와 브라우저 4축 실측은 챕터 통합 단계에서 수행합니다.
