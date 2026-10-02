# 11 패키징과 테스트 격리 — 그림 설계표

| 번호 | 위치 | 종류 | 설명 대상 문장 | 보여 줄 실제 값 | 색 |
|---|---|---|---|---|---|
| 11-6 | 4 핵심 개념 · 비유로 시작하기 | Higgsfield 삽화 | 앞 손님이 쓰던 바구니를 그대로 받으면, 내가 담지 않은 공책이 이미 들어 있습니다. 더미에서 새 바구니를 꺼내면 내가 담은 연필 하나만 들어 있습니다. | 값 없음(비유). 바구니 = 목록 items, 공책 = '노트', 연필 = '연필', 왼쪽 = 13번 셀 Before `['노트', '연필']`, 빈 바구니 더미 = 픽스처 함수 items(), 오른쪽 = 16·17번 셀 After `2 passed`. 3~10절 좌우 Before/After 구도, 6절 바구니·공책·연필을 이어 씀 | — |
| 11-1 | 4 핵심 개념 · 빌드와 휠 (노트북 「오늘 볼 그림」) | Mermaid flowchart TD | 명령 uv build --wheel이 폴더 dist에 휠 파일을 만들었습니다. 명령 uv pip install이 휠을 환경 install_env에 설치합니다. | 3번 셀 `쓴 글자 수: 295`, 4번 셀 pyproject.toml(name price-tools, version 0.1.0), 5번 셀 `Successfully built dist/price_tools-0.1.0-py3-none-any.whl`·`종료 코드: 0`, 8번 셀 `price-tools 0.1.0`, 9번 셀 `출력: 78000` | 파일·휠·환경 폴더 tool(초록), 명령 flow(파랑), 출력 measure(노랑) |
| 11-2 | 5 실행 예제 · 설치한 환경의 Python에서만 불러와짐 | Mermaid flowchart TD(두 갈래) | 값 바꿔 보기는 이름 python_path의 값만 sys.executable로 바꿨습니다. 휠을 설치하지 않은 커널의 Python은 종료 코드 1로 끝났습니다. | 7번 셀 `install_env/bin/python`, 8번 셀 `price-tools 0.1.0`, 9번 셀 `출력: 78000`·`종료 코드: 0`, 10번 셀 `종료 코드: 1`·`ModuleNotFoundError: No module named 'price_tools'` | 코드 글 flow(파랑), 두 Python tool(초록), 78000 measure(노랑), ModuleNotFoundError fail(빨강, 실제로 불러오기에 실패한 출력) |
| 11-3 | 6 일부러 실패해 보기 · Before | Mermaid flowchart TD | 앞 테스트가 담은 노트가 같은 목록에 남아 있었습니다. 같은 테스트가 혼자면 통과하고, 다른 테스트 뒤면 실패했습니다. | 12번 셀 test_items.py(`items = []`), 13번 셀 `.F`·`E       AssertionError: assert ['노트', '연필'] == ['연필']`·`1 failed, 1 passed`·`종료 코드: 1`, 14번 셀 `1 passed`·`종료 코드: 0` | 파일의 목록 tool(초록), 테스트 함수 flow(파랑), 통과 출력 measure(노랑), 실패 출력 fail(빨강) |
| 11-4 | 6 일부러 실패해 보기 · After의 픽스처 차례 | Mermaid sequenceDiagram | 옵션 --setup-show를 더해 다시 실행하면, 픽스처를 준비하고 치운 줄이 함께 나옵니다. | 17번 셀 `SETUP    F items`·`TEARDOWN F items` 각 두 번, `test_items.py::test_add_note (fixtures used: items) .`, `2 passed` | 참여자 기본색, 메모 노랑(테스트가 끝나 점을 전한 뒤 시점의 TEARDOWN) |
| 11-5 | 6 일부러 실패해 보기 · Before/After | Mermaid flowchart TB(Before·After 두 칸) | After 셀은 목록 줄을 픽스처 함수로 바꾸고, 두 테스트 함수의 괄호에 items를 적었습니다. 상품을 담는 줄과 기대값은 그대로입니다. | 13번 셀 `.F`·`1 failed, 1 passed`·`종료 코드: 1` / 15번 셀 `쓴 글자 수: 217`, 16번 셀 `..`·`2 passed`·`종료 코드: 0`, 17번 셀 SETUP 두 번 | 목록 tool(초록), run_pytest() flow(파랑), Before 결과 fail(빨강), After 결과 measure(노랑) |

셀 번호는 코드 셀 순번입니다(준비 1·2, 패키지 폴더 3, pyproject.toml 4, 빌드 5, 휠 안 6, 새 가상환경 7, 설치 8, 새 환경 Python 9, 값 바꿔 보기 커널 Python 10, Before run_pytest 정의 11·테스트 파일 12·실행 13·혼자 실행 14, After 테스트 파일 15·실행 16·--setup-show 17, 심화 18·19).
색 규칙: 파일·휠·환경 폴더·목록(값)은 초록, 우리가 실행한 명령·코드 글·테스트 함수·run_pytest()는 파랑, 출력은 노랑입니다(1~10절과 같음). 빨강은 실제로 실패한 출력뿐입니다. 11-2의 ModuleNotFoundError(종료 코드 1)와 11-3·11-5의 Before `.F`(종료 코드 1)입니다.
노트북 6번 셀(휠 안의 파일 이름 여섯 개)은 그림 없이 본문 「빌드와 휠」 문단으로 설명합니다. 18·19번 심화 셀(monkeypatch, 4 passed)도 그림을 만들지 않고 본문 「확인한 범위」 문단으로만 설명합니다.
기존 도식 `11-concept.svg`(Excalidraw)는 본문에서 뺐습니다. 원본은 `qa/upgrade/before/figures/`에 있고, `figures/`의 옛 파일은 지우지 않았습니다.
