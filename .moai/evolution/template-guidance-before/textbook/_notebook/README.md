# 교재 노트북 공통 도구

학생용 시작 페이지는 `textbook/index.html`입니다. 각 절의 실행 예제에서 코드를 복사하거나 실행 완료 노트북을 내려받습니다.

집필자는 `labs/part*/ch*/notebooks/*.ipynb`에 셀을 작성합니다. 노트북 생성기를 사용할 때도 검증 후 저장된 노트북의 source가 HTML에 그대로 들어갑니다. 수정 전 원본은 각 챕터의 `qa/notebook-before/`에 있습니다.

## 검증과 빌드

프로젝트 루트에서 해당 챕터의 잠금 환경을 사용합니다. 아래 `LAB`은 대상 챕터 폴더이며 실제 경로로 바꿉니다.

```bash
uv run --project LAB --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 python textbook/_notebook/execute.py LAB/notebooks/*.ipynb
```

그다음 해당 챕터의 `_build.py`를 실행합니다. 빌드에는 Pillow가 필요합니다. `execute.py`는 셀마다 나온 실제 출력을 저장하고, `render.py`는 미실행·오류·코드 및 출력 변경·Python 버전 불일치를 검사합니다. 실패 진단은 비밀값을 가린 `.failure.json`에 남습니다.

`verify.py`는 20개 노트북을 기준으로 HTML 셀·내려받기 파일·원본의 일치와 기본 셀 조건을 검사합니다. 새 챕터를 추가하면 기대 개수도 갱신합니다. `visual.cjs`는 챕터 경로를 받아 PC·모바일 가독성과 복사 결과를 확인합니다. 결과는 `checks/`에 저장됩니다.

## 수정 위치

- 본문·도식 배치: 챕터 `_src/`
- 실행 셀·결과: 챕터 `labs/.../notebooks/`
- 공통 화면: `theme.css`
- 셀 표시·실행 검증 연결: `render.py`
- 코드 복사: `copy.js`
- 학생 시작 페이지: `build_index.py`

기본 노트북의 생성 호출은 `init_chat_model`·`invoke`·`AIMessage.text`, 임베딩은 `OpenAIEmbeddings`로 통일합니다. `verify.py`는 기본 실습에서 직접 `openai` SDK를 import하면 실패합니다. Ch 18처럼 직접 SDK 학습이 명시된 챕터를 추가할 때는 해당 교육 경계를 검증기에 명시합니다.

기존 파일형 모듈과 과거 실험 로그는 강사용 확장 자료로 보존합니다. 새 노트북의 축소 실험 결과를 과거 전체 문서 실험 결과와 섞지 않습니다. OCR·상용 파서·실제 업무 HWP/HWPX 변환 등 별도 도구가 필요한 검증은 각 절의 확인 필요 항목을 따릅니다.

## 실패 코드와 수정 코드 배치

기본 예제 셀 다음에 Before·After 셀을 순서대로 작성합니다. Before의 코드와 설명 셀은 `metadata.lesson_part="before"`, After는 `"after"`로 표시합니다. 각 단계는 코드와 실제 출력을 포함하고, After는 같은 실패 원인을 수정한 뒤 검증합니다.

본문 5번 블록에는 `{{notebook:절|example}}`, 6번 블록에는 `{{notebook:절|failure}}`를 한 번씩 둡니다. PC에서는 두 열, 모바일에서는 위아래로 표시하며, 전체 코드 복사는 두 블록의 셀을 실행 순서대로 포함합니다. 코드·출력·내려받기 파일 대조와 6번 블록의 실제 배치는 `verify.py`에서 확인합니다.

## 학생용 구성

학생용 교재는 복습 문제 다음에 참고 자료가 오는 10개 블록으로 구성합니다. 강사 노트는 본문이나 목차에 넣지 않으며, `verify.py`가 이를 확인합니다.

## 초보자용 주석

모든 코드 셀에서 주요 변수·인자·반환값과 처리 이유를 설명합니다. 낯선 문법은 해당 예제에서 만드는 값을 풀어 쓰고, Before/After에는 실패·해결 원인을 명시합니다. 주석을 추가할 때도 문자열 값·실행문·셀 순서를 유지하고 노트북을 다시 실행한 뒤 HTML을 빌드합니다. [주석 검증 기록](COMMENTS-VERIFICATION.md)을 참고합니다.
