# Ch 2 최종 검증 기록

확인일: 2026-09-09. 대상은 「파이썬 프로그래밍」 40시간(강의 12시간·실습 28시간), 개념 12절·챕터 목차·기본 노트북 12개입니다.

## 실행과 산출물

Python 3.12.13, pytest 9.1.1, Pydantic 2.13.5, uv/uv-build 0.12.11, ipykernel 7.3.0, nbclient 0.11.0으로 검증했습니다. 실행 환경은 macOS arm64입니다. 학생 환경은 `labs/part1/ch02-python/pyproject.toml`과 `uv.lock`에 고정했습니다.

공통 `execute.py`로 노트북마다 저장 출력을 지우고 새 커널을 시작했습니다. 작업 위치도 노트북마다 새 임시 폴더로 지정했습니다. 최종 결과는 12개 노트북·76개 코드 셀 통과이며 셀 최대 길이는 22줄입니다. 10절에서 발견한 셀 연결 줄바꿈 오류를 수정한 뒤 10~12절을 다시 실행했습니다. 재실행 후 학생 파일에는 실패 기록 파일이 남아 있지 않으며 최종 실행 출력만 포함합니다.

실패 예제의 예외와 pytest 종료 코드 1은 의도한 관찰값입니다. 예외를 예상하는 셀은 예외 유형과 결과를 검사합니다. 08절은 같은 테스트를 유지한 채 할인 계산의 결함만 고쳐 실패에서 통과로 바뀌었습니다. 11절은 실제 휠을 빌드하고 격리 venv에 설치하여 새 Python 프로세스로 import했습니다. 공유 목록 비교는 1 failed/1 passed에서 fixture 적용 후 2 passed로 바뀌었고, 별도의 monkeypatch 대체·복원 검사 2건도 통과했습니다.

12절은 실제 네트워크 없이 모의 I/O를 사용합니다. 최종 저장 출력의 순차·동시 대기는 0.082초·0.042초입니다. Before는 `block-start, block-end, heartbeat`, After는 `wait-start, heartbeat, wait-end`를 관찰했습니다. After는 모든 사건의 완료를 검사하고 시간 임계값이나 특정 스케줄 순서를 합격 조건으로 강제하지 않습니다. 이 한 번의 결과로 일반적인 속도 향상을 주장하지 않습니다.

## HTML과 화면

`_src/` 본문과 노트북을 `_build.py`로 결합했습니다. 공통 `verify.py --chapter textbook/part1/ch02-python` 검사는 HTML의 코드, 실제 출력, 내장 다운로드 노트북을 정본과 대조합니다. 추가 `qa/audit.py`는 절별 고정 10개 구성, 본문 최소 2,500자, 복습 4문항·해설, 한국어 코드 주석, 함수 반환 타입힌트, 도식·로컬 링크를 검사합니다. 전체 복습은 48문항이며 A 경로 보충 과제 6개는 목차에 있습니다.

Playwright로 13개 페이지를 폭 1280px와 390px에서 열고 글자 크기, 대비, 잘림, 콘텐츠 경계, 가로 넘침, 이미지, 코드 복사, 실패/수정 표시를 확인했습니다. 총 26건이 통과했습니다. 도식 12개는 개별 SVG 텍스트의 상자 경계도 검사하여 잘린 라벨이 없음을 확인했습니다. 실제 데스크톱·모바일 화면도 확인했습니다.

증거: `textbook/_notebook/checks/ch02-python/visual-results.json`, `qa/visual/diagram-boxes.json`, `qa/delivery-audit.json`. 최종 전달 시점의 파일 해시는 `qa/release-manifest.json`에 기록합니다.

## 검토와 배포

작성자와 분리된 기술·교육 검토 결과는 `qa/topic-review.md`, 절별 통제 조건·실제 셀·출력은 `집필점검표.md`에 있습니다. 독립 언어 검토는 일반 슬롭 정리, 로컬 맞춤법 확인, 산문 윤문과 Phase 6 의미 검토를 수행했습니다. 다른 모델인 리더도 12절 전체와 목차의 보충 과제·기대값을 읽고 실제 출력과 대조했습니다. 문장 변경은 코드와 출력에서 분리했습니다. 세부 판단과 구조 게이트는 `qa/language/`에 보존합니다.

공통 교재 도구 회귀 검사는 37개 테스트와 16개 하위 검사를 통과했습니다. 화면 도구 테스트에 필요한 Pillow는 검증 전용 uv 환경에만 추가했으며 학생 의존성을 바꾸지 않았습니다. 이 폴더는 Git 저장소가 아니므로 Git diff 검증을 완료했다고 주장하지 않습니다.

`ch02-practice.zip`은 명시한 학생 파일 15개(노트북 12개, README, pyproject.toml, uv.lock), 시작 안내 사본, SHA-256 manifest로 구성됩니다. ZIP 무결성과 모든 원본 해시를 확인했습니다. 전체 목차와 `llm-practice.zip`에도 Ch 2를 추가하며 다른 챕터를 보존했습니다. 전체 묶음 파일 수는 동시 작업으로 바뀔 수 있으므로 해당 ZIP의 manifest를 기준으로 확인합니다. 실제 키나 개인 환경 파일은 포함하지 않습니다.

## 확인 필요 항목

- Windows와 Linux에서는 직접 실행하지 않았습니다. 특히 11절의 휠 설치와 새 프로세스 import는 macOS 실행 증거입니다.
- 외부 맞춤법 단계는 생략했습니다. 적용한 [korean-spell-check SKILL.md](/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-spell-check/SKILL.md:35)는 “사용 금지: … 상업적 대량 처리”를 명시합니다. 공개 교재 전체의 대량 전송에 해당하여 외부 서비스로 보내지 않고 로컬 교정·윤문으로 검토했습니다.
- Excalidraw MCP 미리보기 도구가 이 세션에 없어 생성된 SVG·Excalidraw JSON과 브라우저 화면을 검증했습니다. 도식 12개는 같은 생성기에서 두 형식을 만들었습니다. 생성형 삽화는 사용하지 않았으며 Higgsfield 크레딧 사용량은 0입니다.
- 공식 Python 3.12 문서의 패치 버전과 로컬 3.12.13, Pydantic 문서의 버전별 경로 차이는 `qa/research.md`에 기록했습니다. 수록 API는 위 고정 버전으로 실제 실행했습니다.

## 품질 개선 01절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 01 변수와 자료형을 다시 썼습니다. 생성기 `qa/upgrade/author_01.py`, 진단 `qa/upgrade/01-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, 코드 셀 11개, 모델 호출 0번). `verify.py --chapter` PASS. 게이트 G1~G7 0건(`qa/upgrade/gates-wip-01.json`).
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job ae745864-8153-46eb-b96e-c9b23224aa0e). 수정 전 파일은 `qa/upgrade/before/`.
- 화면 검사(`visual.cjs`)는 이번에 다시 실행하지 않았습니다.

## 품질 개선 02절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 02 조건문과 반복문을 다시 썼습니다. 생성기 `qa/upgrade/author_02.py`, 진단 `qa/upgrade/02-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, 코드 셀 13개 중 심화 1개, 모델 호출 0번). `verify.py --chapter` PASS(12절 89셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-02.json`).
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job 1c7c0c75-65e9-4757-ab58-8cf14ff7aa9d). 수정 전 파일은 `qa/upgrade/before/`.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.

## 품질 개선 04절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 04 함수를 다시 썼습니다. 생성기 `qa/upgrade/author_04.py`, 진단 `qa/upgrade/04-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, 코드 셀 15개 중 심화 1개, 모델 호출 0번). `verify.py --chapter` PASS(12절 108셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-04.json`).
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job 2aed0c60-ac79-4320-a08a-fabf6b4afd17). 수정 전 파일은 `qa/upgrade/before/`.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.

## 품질 개선 06절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 06 클래스를 다시 썼습니다. 생성기 `qa/upgrade/author_06.py`, 진단 `qa/upgrade/06-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12, 코드 셀 11개 중 심화 1개, 모델 호출 0번). `verify.py --chapter` PASS(12절 124셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-06.json`).
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job f1c6889f-fedb-467f-bf50-b9f8f9c5c1af). 수정 전 파일은 `qa/upgrade/before/`.

## 품질 개선 07절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 07 모듈과 타입힌트를 다시 썼습니다. 생성기 `qa/upgrade/author_07.py`, 진단 `qa/upgrade/07-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, 코드 셀 11개 중 심화 1개, 모델 호출 0번). `verify.py --chapter` PASS(12절 129셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-07.json`).
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job 18aef5d7-06c5-4633-94c2-ef9cba71c543). 수정 전 파일은 `qa/upgrade/before/`.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.
- 임시 폴더의 모듈 파일을 import 할 수 있는 근거: 실행 커널의 `sys.path`에 `''`(현재 작업 폴더)가 들어 있음을 별도 시험 노트북으로 확인했습니다(2026-09-16).

## 품질 개선 08절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 08 pytest를 다시 썼습니다. 생성기 `qa/upgrade/author_08.py`, 진단 `qa/upgrade/08-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, pytest 9.1.1, 코드 셀 13개 중 심화 1개, 모델 호출 0번). `verify.py --chapter` PASS(12절 135셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-08.json`).
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job bc358c9c-634f-4430-a7db-1afc73f4e3d0). 수정 전 파일은 `qa/upgrade/before/`.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.
- pytest를 새 Python(`subprocess.run([sys.executable, "-m", "pytest", "-q", "--color=no"])`)에서 실행하는 근거: pytest 9.1.1 문서 `how-to/usage.rst`의 `pytest.main()` 재호출 비권장 문장. 실습 폴더 가상환경의 pytest11 플러그인 0개 확인(2026-09-16).

## 품질 개선 09절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 09 데코레이터와 컨텍스트 매니저를 다시 썼습니다. 생성기 `qa/upgrade/author_09.py`, 진단 `qa/upgrade/09-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, 코드 셀 17개 중 심화 1개, 모델 호출 0번). `verify.py --chapter` PASS(12절 146셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-09.json`).
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job ebfd4db6-924d-41c2-92cb-ce9b762e4b84). 수정 전 파일은 `qa/upgrade/before/`.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390, SVG 4·삽화 1, 남은 `{{` 토큰 없음). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.
- 동작 근거: `functools.WRAPPER_ASSIGNMENTS`(설치한 Python 3.12.13에서 출력), `contextlib._GeneratorContextManager.__exit__`의 `gen.throw()`(소스 확인), pytest 9.1.1 `_pytest/mark/structures.py` `MarkDecorator.__call__`(표시를 붙이고 같은 함수 반환).

## 품질 개선 10절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 10 Pydantic을 다시 썼습니다. 생성기 `qa/upgrade/author_10.py`, 진단 `qa/upgrade/10-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, Pydantic 2.13.5, 코드 셀 14개 중 심화 1개, 언어 모델 호출 0번). `verify.py --chapter` PASS(12절 154셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-10.json`).
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job 9b6e7a33-6abb-49d7-8a04-2ed826aa1cdb). 수정 전 파일은 `qa/upgrade/before/`.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390, SVG 4·삽화 1, 남은 `{{` 토큰 없음). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.
- 동작 근거: 설치한 Pydantic 2.13.5의 `BaseModel.__init__(self, /, **data)` 소스, Pydantic 문서 Strict Mode·Models·Migration Guide(2026-09-16 확인, 문서 주소가 pydantic.dev/docs/validation으로 옮겨 감).

## 품질 개선 11절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 11 패키징과 테스트 격리를 다시 썼습니다. 생성기 `qa/upgrade/author_11.py`, 진단 `qa/upgrade/11-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, uv 0.12.11, pytest 9.1.1, 코드 셀 19개 중 심화 2개, 모델 호출 0번). `verify.py --chapter` PASS(12절 164셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-11.json`).
- 그림: Mermaid 5장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job 2af1bd3c-1fa4-4465-b1d4-d6c5301011b9). 수정 전 파일은 `qa/upgrade/before/`.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390, SVG 5·삽화 1, 남은 `{{` 토큰 없음). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.
- 동작 근거: pytest 9.1.1 소스(`fixtures.py` 기본 범위 function, `setuponly.py` SETUP/TEARDOWN 줄, `monkeypatch.py` 되돌림 설명, `main.py` `_in_venv`), uv 문서 build backend, Packaging 규격 Binary distribution format(2026-09-16 확인). 실행 도구 커널에서 uv 출력에 색 기호가 들어가 빌드 명령에 `--color never`를 더했습니다.

## 품질 개선 12절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 12 async와 await를 다시 썼습니다. 생성기 `qa/upgrade/author_12.py`, 진단 `qa/upgrade/12-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, 코드 셀 16개 중 심화 1개, 모델 호출 0번). `verify.py --chapter` PASS(12절 174셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-12.json`).
- 그림: Mermaid 5장(PNG 직접 확인, 챕터 첫 gantt 포함), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job b0084744-36d2-4291-8924-7faacbec8980). 수정 전 파일은 `qa/upgrade/before/`.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390, SVG 5·삽화 1, 남은 `{{` 토큰 없음). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.
- 동작 근거: Python 3.12.13 설치본 asyncio 소스(`threads.py` to_thread, `tasks.py` gather 결과 순서와 시작 순서 설명, `base_events.py` 기본 실행기 스레드 이름, `runners.py` run), Python 문서 코루틴과 태스크·asyncio-dev, IPython autoawait(2026-09-16 확인).


## 챕터 끝 실습 13절 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md` §7-2로 13 파이썬 실습(주문 파일로 합계 내기, experiment)을 새로 만들었습니다. 생성기 `qa/upgrade/author_13.py`, 진단 `qa/upgrade/13-diagnosis.md`.
- 새 커널 실행 PASS(Python 3.12.13, 코드 셀 16개, 심화 셀 없음, 모델 호출 0번). `verify.py --chapter` PASS(13절 190셀). 게이트 G1~G7 0건(`qa/upgrade/gates-wip-13.json`, 챕터 전체 `gates-wip-all.json` 13/13).
- 그림: Mermaid 3장(PNG 직접 확인), 삽화 1장(Higgsfield nano_banana_pro 2크레딧, job 16184074-47d0-4031-9cd1-fd53efacb1df). 새 절이라 수정 전 파일은 없습니다.
- 빌드 HTML의 가로 넘침은 puppeteer로 1280px·390px에서 확인했습니다(scrollWidth 1280·390, SVG 3·삽화 1, 남은 `{{` 토큰 없음). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.
- 함께 고친 곳: `chapter.json` 13절 추가, 12절 본문·노트북의 다음 학습 문장(13절 링크), `_src/index.html` 학습 순서 단락 한 문장.

## 별도 세션 검토 1차 반영과 챕터 마감 (2026-09-16)

- 검토 보고서: `qa/upgrade/review-round1-A.md`(§01~07, 상 0·중 7·하 22), `qa/upgrade/review-round1-B.md`(§08~13, 상 0·중 4·하 22). 반영 중 10/11·하 44/44. 미반영은 A C-3 다운로드 zip 재생성 하나(전체 마감 때 일괄). 항목별 반영은 두 보고서 끝 「반영 결과」, 절별 기록은 `qa/upgrade/NN-diagnosis.md` 「검토」 절에 있습니다.
- 재실행: 01·03~13 `run_section.sh` 새 커널 PASS, 02는 `--no-exec`(노트북 변경 없음). 코드 셀 출력은 반영 전과 글자 단위로 같고, 05 준비 셀 작업 폴더 경로 한 줄(실행마다 다름, `[사용자 폴더]`로 가림)과 06 심화 셀 `준호 주문 인스턴스의 속성: {'customer': '준호'}` 한 줄만 늘었습니다.
- `upgrade_gates.py --label after --strict`: 13/13절 G1~G7 0건(`qa/upgrade/gates-after.json`). 수정 전(`gates-before.json`, 12절) G1 9·G2 5·G5 95·G6 268·G7 36, 합계 413건.
- `verify.py --chapter`: `PASS 13 sections / 190 code cells (max 21 lines)`.
- `visual.cjs`: 목차와 13절, 14페이지 × 1280·390px, 28건 PASS(가로 넘침·잘림·깨진 이미지·복사 오류 0). 기기 VM에 Playwright가 없어 `/tmp`에 playwright-core 1.63.0을 설치하고, 이미 있던 puppeteer Chrome 153 headless shell을 실행 파일로 지정해 돌렸습니다. 처음 실행에서 05-4·07-3·12-3·12-4의 SVG 글자가 본문 축소 뒤 14px 미만(11.4~13.6px)이라 실패했고, 라벨 줄바꿈·눈금 글자 15px로 다시 렌더해 통과했습니다.
- 다시 렌더한 그림(PNG 직접 확인): 02-2(선언 순서로 break 라벨 교차 해소), 03-1·03-3(라벨), 05-3(오류 노랑), 05-4·07-3·12-4(폭 축소), 10-1·10-3(넣은 값 초록), 12-3(눈금 글자), 13-3(받아 기록한 오류 노랑).
- 규격 문서 추가: `QUALITY-UPGRADE.md` §2-3 Ch 2 01~06절 준비 셀 표준 라이브러리 import 예외, §2-2 「A 트랙과 L5·L6」(Part 2 이후 `@` 줄·`BaseModel` 첫 사용 시 세 문장과 Ch 2 09·10절 링크), §2-4 클래스 정의 셀(메서드 2개·본문 3줄 이하면 한 셀), §5-3 오류 상자 색(잡아서 기록한 오류 노랑, 프로그램을 멈춘 실패 빨강). `PLAYBOOK.md` §4 한 줄.
- 함께 고친 곳: `_src/index.html`(경로 이름 한 문장, 「13개 노트북」, A트랙 소개 단락 두 문장, 과제 1·3·5), 실습 폴더 `README.md` 13절 한 문장, `qa/upgrade/handoff.md` 두 곳, 설계표 05·10·13.
- 챕터 요약: `qa/upgrade/chapter-summary.md`(Ch 03 작업자용).

### 확인 필요 항목 (검토 1차 반영)

- 다운로드 묶음 `textbook/downloads/ch02-practice.zip`은 개선 전 12개 노트북입니다. 전체 마감 때 다시 만듭니다.
- 강사 확인: 03·05절 강의·실습 범위 문장, 규격에 더한 네 규칙, index A트랙 과제 1·3·5, 05절 작업 폴더 경로 출력.
- Windows 출력, VS Code에서 모듈 파일 만들기, 터미널 pytest 실행은 이번에 실행하지 않았습니다.
