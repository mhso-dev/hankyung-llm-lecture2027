# Ch 4 실행 검증

- 환경: Python 3.12.13, uv 잠금 환경
- 노트북: 5개, 코드 셀 30개, 셀 최대 24줄, 새 커널 실행 PASS
- 모듈 테스트: `uv run python -m pytest -q` → 8 passed
- HTML 계약: `verify.py --chapter textbook/part1/ch04-data-tools` → 5 sections / 30 code cells PASS
- 도식: `_gen_figures.py`에서 같은 상자·화살표 요소 목록으로 SVG·Excalidraw 5쌍 생성. 파랑=학생이 작성한 조건·처리 흐름, 초록=도구·데이터, 노랑=측정·평가, 빨강=실패를 공통 적용
- 생성형 삽화: 순서·관계 도식이 학습 내용을 직접 설명하므로 사용하지 않음, 크레딧 0
- 정적 검사: 모듈·테스트 Ruff 통과, 노트북 import 순서·복합문 규칙 Ruff 통과, Pyright 0 errors
- 화면 검사: 1280px·390px에서 index와 5절 모두 PASS. 작은 글자·대비·잘림·본문 밖 텍스트·SVG 경계·가로 넘침·깨진 이미지·복사·Before/After 오류가 모두 0건
- 본문 분량: 최종 언어 감사 뒤 태그와 공백을 제외한 5절 합계 12,681자

Excalidraw MCP가 현재 도구 목록에 없어 미리보기는 실행하지 못했습니다. 같은 생성기의 상자·화살표를 SVG와 JSON으로 만들고 두 형식을 파싱했으며, SVG는 브라우저 화면 검사에 포함했습니다. 별도 검토 세션의 한국어 감사 결과는 `qa/language/review.md`에 기록했습니다. 판정은 corrected, S1 잔존 0, Phase 6 의미 보존 15/15·자체 검증 6/6입니다. 외부 맞춤법 전송은 상업적 대량 처리 제한에 따라 생략했습니다.

## 품질 개선 01절 (2026-09-16)

- 노트북 `01-Pandas로-표-다루기`: 코드 셀 16개(최대 10줄), 새 커널 실행 PASS(Linux aarch64, Python 3.12.13, pandas 3.0.5), 모델 호출 0번
- `verify.py --chapter textbook/part1/ch04-data-tools` → `PASS 5 sections / 41 code cells (max 20 lines)`(02~05절은 개선 전)
- 게이트 `upgrade_gates.py --section 01`: G1~G7 0(수정 전 53건, `qa/upgrade/gates-before.json`)
- 화면 검사: 이 절 HTML을 `/tmp`에 복사해 `visual.cjs` 1280·390px PASS
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield 2회 생성, 채택 job `f412811a-9852-4a29-91de-484ddc6e19f8`, 4크레딧)
- 실습 폴더 `uv run python -m pytest -q` → 10 passed(`data_tools.py`·테스트는 고치지 않음)
- 진단과 결과: `qa/upgrade/01-diagnosis.md`, 인계: `qa/upgrade/handoff.md`

## 품질 개선 02절 (2026-09-16)

- 노트북 `02-관계형-테이블과-키`: 코드 셀 16개(최대 9줄), 새 커널 실행 PASS(Linux aarch64, Python 3.12.13, pandas 3.0.5), 모델 호출 0번
- `verify.py --chapter textbook/part1/ch04-data-tools` → `PASS 5 sections / 51 code cells (max 20 lines)`(03~05절은 개선 전)
- 게이트 `upgrade_gates.py --section 02`: G1~G7 0(수정 전 34건, `qa/upgrade/gates-before.json`)
- 화면 검사: 이 절 HTML을 `/tmp`에 복사해 `visual.cjs` 1280·390px PASS
- 그림: Mermaid 4장(PNG 직접 확인). 삽화 1장은 Higgsfield 2회 생성 모두 탈락해 삽화 대기(job `0b0f8381-…`, `31286c11-…`, 4크레딧, `qa/upgrade/illustration-pending.md`)
- 실습 폴더 `uv run python -m pytest -q` → 10 passed(`data_tools.py`·테스트는 고치지 않음)
- 진단과 결과: `qa/upgrade/02-diagnosis.md`, 인계: `qa/upgrade/handoff.md`

## 품질 개선 03절 (2026-09-16)

- 노트북 `03-SQL로-조회-함수-만들기`: 코드 셀 20개(최대 15줄), 새 커널 실행 PASS(Linux aarch64, Python 3.12.13, SQLite 3.53.1), 모델 호출 0번
- `verify.py --chapter textbook/part1/ch04-data-tools` → `PASS 5 sections / 65 code cells (max 20 lines)`(04·05절은 개선 전)
- 게이트 `upgrade_gates.py --section 03`: G1~G7 0(수정 전 53건, `qa/upgrade/gates-before.json`)
- 화면 검사: 이 절 HTML과 `visual.cjs` 사본을 `/tmp`에서 실행해 1280·390px PASS
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield 2회 생성, 1차 잘림으로 보류, 2차 job `7e78bd4b-…` 채택, 4크레딧, 저장 PNG 픽셀 대조 차이 0)
- 실습 폴더 `uv run python -m pytest -q` → 10 passed(`data_tools.py`·테스트는 고치지 않음)
- 진단과 결과: `qa/upgrade/03-diagnosis.md`, 인계: `qa/upgrade/handoff.md`

## 품질 개선 04절 (2026-09-16)

- 노트북 `04-REST와-페이지네이션`: 코드 셀 13개(준비 4 + 본문 9), 새 커널 실행 PASS(Linux aarch64, Python 3.12.13, httpx 0.28.1), 모델 호출 0번, 인터넷 접속 없음(연습용 서비스는 `127.0.0.1`, 포트 0)
- `verify.py --chapter textbook/part1/ch04-data-tools` → `PASS 5 sections / 72 code cells (max 21 lines)`(21줄은 개선 전 05절)
- 게이트 `upgrade_gates.py --section 04`: G1~G7 0(수정 전 50건, `qa/upgrade/gates-before.json`)
- 화면 검사: 이 절 HTML과 `visual.cjs` 사본을 `/tmp/ch04-04-vis`에서 실행해 1280·390px PASS
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield 1회 생성, job `d55f7a01-…` 채택, 2크레딧, 저장 PNG 픽셀 대조 차이 0 재확인)
- 실습 폴더 `uv run python -m pytest -q` → 10 passed(`data_tools.py`·테스트는 고치지 않음)
- 진단과 결과: `qa/upgrade/04-diagnosis.md`, 인계: `qa/upgrade/handoff.md` `## §04 → §05`

## 품질 개선 05절 (2026-09-16)

- 노트북 `05-문서-파싱과-스크래핑`: 코드 셀 13개(준비 1 + 본문 12), 새 커널 실행 PASS(Linux aarch64, Python 3.12.13, beautifulsoup4 4.15.0, lxml 6.1.3, soupsieve 2.9.2), 모델 호출 0번, 인터넷 접속 없음(robots 판단 주소는 시험용 이름 `example.test`)
- `verify.py --chapter textbook/part1/ch04-data-tools` → `PASS 5 sections / 78 code cells (max 21 lines)`(21줄은 04절 서버 프로그램 셀)
- 게이트 `upgrade_gates.py --section 05`: G1~G7 0(수정 전 47건, `qa/upgrade/gates-before.json`)
- 화면 검사: 이 절 HTML과 `visual.cjs` 사본을 `/tmp/ch04-05-vis`에서 실행해 1280·390px PASS
- 그림: Mermaid 4장(PNG 직접 확인), 삽화 1장(Higgsfield 1회 생성, job `07413a99-…` 채택, 2크레딧, 저장 PNG 픽셀 대조 차이 0)
- Ch 5 전달 파일: 노트북이 `labs/part1/ch04-data-tools/data/article-text.json`을 다시 씀. SHA-256 `e2418544…` 실행 전후 같음. 커널 cwd가 프로젝트 맨 위 폴더(run_section.sh)일 때와 `notebooks` 폴더(`execute.py --cwd`, 배포 러너 조건)일 때 모두 PASS·출력 동일
- 실습 폴더 `uv run python -m pytest -q` → 10 passed(`data_tools.py`·테스트는 고치지 않음)
- 진단과 결과: `qa/upgrade/05-diagnosis.md`, 인계: `qa/upgrade/handoff.md` `## §05 → 실습`

## 품질 개선 06절 — 챕터 끝 실습 (2026-09-16)

- 노트북 `06-데이터-도구-실습`(experiment, 새 절): 코드 셀 18개(준비 4 + 본 경로 14), 새 커널 실행 PASS(Linux aarch64, Python 3.12.13, pandas 3.0.5, SQLite 3.53.1, httpx 0.28.1), 모델 호출 0번, 인터넷 접속 없음(04절 연습용 주문 서비스를 이 컴퓨터 안에서 켰다가 끔)
- `verify.py --chapter textbook/part1/ch04-data-tools` → `PASS 6 sections / 96 code cells (max 21 lines)`
- 게이트 `upgrade_gates.py`: 06절 G1~G7 0, 챕터 전체 6/6 PASS(`qa/upgrade/gates-wip-all.json`)
- 화면 검사 `visual.cjs`: 챕터 7페이지 × 1280·390px 14건 PASS
- 실습 폴더 `data/article-text.json`은 읽거나 쓰지 않음(수정 시각 그대로). 05절 노트북은 설명 셀만 고치고 다시 실행하지 않음


## 별도 세션 검토 1차 반영과 챕터 마감 (2026-09-16)

- 검토 보고서 `qa/upgrade/review-round1.md`: 상 0·중 6·하 18. 중 6·하 17 반영, C-3은 권고대로 미반영(공용 Mermaid 설정 건). 끝에 「반영 결과」 절
- 다시 실행: 01~06 모두 생성기(`author_NN.py`) 수정 → `run_section.sh`(새 커널 PASS). 코드 셀 96개(수 변화 없음). 출력은 새 `print` 라벨 줄(01 8·02 9·03 8·05 3)과 임시 경로·포트를 빼고 반영 전과 셀별로 같음
- 게이트 `upgrade_gates.py --label after --strict`: 6/6 PASS, G1~G7 0(`qa/upgrade/gates-after.json`). 04절 첫 실행에서 G6 `dense_paragraph` 2건(설명 셀 6문장)을 빈 줄로 단락을 나눠 0으로
- `verify.py --chapter textbook/part1/ch04-data-tools` → `PASS 6 sections / 96 code cells (max 21 lines)`
- `visual.cjs`: 목차와 6절, 7페이지 × 1280·390px, 14건 PASS. Ch 04 06절 작업의 래퍼 방식(`/tmp/pw/node_modules`의 playwright-core, puppeteer Chrome 153 headless shell 실행 파일 지정)을 `/tmp/ch04-close/vis.cjs`로 복사하고 `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`를 주어 실행. 공용 도구는 고치지 않음
- 실습 폴더 `uv run python -m pytest -q` → 10 passed(`data_tools.py`·테스트는 Ch 19가 쓰므로 고치지 않음). `README.md`·`data/README.md` 안내 문장만 고침(검토 C-4)
- Ch 5 전달 파일 `labs/part1/ch04-data-tools/data/article-text.json` SHA-256: 반영 전 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1`, 05 재실행(16:17:58에 다시 씀)·06 재실행·pytest 뒤 같음
- 06-2 재실행 동작 확인: 기기 셸에서 06 노트북 코드 셀(준비~실행 1)을 그대로 실행한 뒤 실행 1을 같은 `shop-1.db`로 다시 불러 `고객 넣기 오류:` 두 줄 → `IntegrityError: UNIQUE constraint failed: orders.order_id`, 다른 연결 쓰기 `database is locked`를 확인
- 다시 렌더한 그림: `06-2-실행1-순서`(요청 라벨 `INSERT 주문 O101~O103 · SELECT *`, viewBox 798, PNG 확인). 나머지 그림은 해시가 같아 렌더 생략
- 삽화: 새 생성 없음(크레딧 0). **삽화 1장 대기(02-5)**
- 규격 문서 추가: `QUALITY-UPGRADE.md` §2-4(여러 줄 출력은 라벨을 앞줄에 따로), §7-2(뒤 챕터 연결은 뒤 챕터 파일로 확인, 실습 폴더 동명 함수 판을 뒤 챕터가 쓰면 본문에 적음). `PLAYBOOK.md` §4 두 줄
- 리뷰 묶음 `pack.py` 6개 갱신. 챕터 요약 `qa/upgrade/chapter-summary.md`(Ch 05 작업자용)

### 확인 필요 항목 (검토 1차 반영)

- 다운로드 묶음 `textbook/downloads/part1-practice.zip`의 Ch 4는 개선 전 노트북 5개와 개선 전 README입니다. Part 목차(`textbook/part1/_build_index.py`, `index.html`)도 Ch 4 절 수 5입니다. 둘 다 전체 마감 때 다시 만듭니다.
- 강사 확인: 03절 강의·실습 범위 문장, 기준 버전 표기, 규격에 더한 두 규칙, 삽화 02-5 대기로 마감한 것.
- Windows·macOS 출력, 다른 pandas·SQLite·httpx·bs4 버전, 인터넷 서비스·사이트는 이번에 실행하지 않았습니다.
