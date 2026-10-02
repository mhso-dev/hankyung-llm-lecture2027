# 02-도구-설치와-터미널 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/02-paths.*`).
생성기: `qa/upgrade/author_02.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch01-development-environment 02`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 1 | 0 |
| G4 | 0 | 0 |
| G5 | 5 | 0 |
| G6 | 26 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 5 | 12 (준비 1 + example 5 + before 2(심화 1 포함) + after 4) |
| 검사한 문장 | 155 | 263 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, 2026-09-16 01:36 UTC), verify PASS(5절 39셀). 빌드 HTML 1280px·390px에서 가로 넘침 없음(scrollWidth 1280/390, 로컬 puppeteer 확인, `qa/upgrade/_shot02/`).

## 수정 전 주요 문제

- G3: 첫 코드 셀(`from pathlib import Path`) 첫 줄 주석 없음
- G5: 제목 셀·「오늘 볼 그림」 첨부 없음. 결과 읽기 셀이 없거나 출력 값을 인용하지 않음(셀 6·8·10)
- G6: 코드 이름+조사로 시작하는 문장 22개(「`TemporaryDirectory`는」, 「`write_text`는」, 「uv는」 등), 70자 초과 2개, 5문장 넘는 단락 1개
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 도식 `02-paths.svg`(Excalidraw)의 「빨간 실패 경로」 설명과 노트북 흐름(정상 읽기 → Before → After)이 1:1로 맞지 않음
- 문법: 셀마다 f-string, `type(error).__name__`, `try/except/else`+`raise AssertionError`를 기본 경로에서 사용(Ch 1 사다리 L1 밖). 첫 준비 셀에서 `TemporaryDirectory`·`Path`·`/`·`mkdir`·`is_dir`를 한 번에 설명
- 본문: 5절 설명 단락이 속성·메서드·객체·인자를 한 번에 설명(단락당 정보 과다). 「옆방의 책」 비유가 코드 요소와 대응되지 않음

## 바꾼 것

- 노트북(paired): 제목 셀(준비물 「API 키 불필요」, 호출 0번·비용 없음·1분 이내, 설치 명령은 실행하지 않음) → 오늘 볼 그림(02-1) → 준비(import) → 임시 폴더 → practice 폴더(만들기 전 `False`/만든 뒤 `True`) → data/message.txt 저장 → `relative_to()`로 두 기준에서 본 경로(`data/message.txt` vs `practice/data/message.txt`) → practice 기준 읽기 → Before(기준 임시 폴더, `False`/`False`) → 원리 더 알아보기 심화 셀(실제 `FileNotFoundError`) → After(기준만 practice, `True`/`True`) → 내용 비교 `True` → 값 바꿔 보기(기준 그대로, 경로 `practice/data/message.txt` → `True`, After와 같은 위치 `True`) → `cleanup()` 후 `False` → 정리
- 사다리: 기본 경로는 대입·print(쉼표 인자)·`==` 비교·`assert`와 준비 셀의 표준 라이브러리 import(환경 챕터 예외(`QUALITY-UPGRADE.md` §2 끝)로 표준 라이브러리 import와 그 결과 값의 메서드를 쓰고, import나 점(.)으로 부르는 메서드·속성이 있는 코드 셀에 `upgrade_allow=["stdlib-import"]`를 적음), 경로 값의 메서드(`mkdir`, `is_dir`, `is_file`, `write_text`, `read_text`, `relative_to`, `cleanup`)만 사용. f-string 제거. `try/except`는 `lesson_level="deep-dive"` 셀 한 곳으로 옮기고 뒤 셀은 그 변수를 쓰지 않음
- 실패 장면은 실제 조건(기준 폴더를 한 칸 위로)으로 재현. Before 판정은 `is_file()` 결과, 오류 이름은 심화 셀의 실제 출력으로 확인
- 본문 10블록 전체를 다시 씀. 서랍·편지 비유와 대응(방=기준 폴더, 맨 위 서랍=상대 경로, 편지=파일), 용어 7개 표, 메서드 5행 표, 「이 절의 질문」, 실행하지 않은 범위(설치 화면·VS Code 메뉴·터미널 입력·Windows 출력 모양) 명시, 복습 5문항(01절 형식)
- 그림: Mermaid 4장(02-1 폴더와 기준, 02-2 설치 확인 순서, 02-3 읽기 흐름, 02-4 기준 비교) + 삽화 1장(02-5 서랍과 편지, 2회 생성 중 2차 채택). 기존 Excalidraw 도식은 본문에서 뺌(원본은 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 사실 주장 확인

- 설치 안내 링크·「Standalone installer」·Python/Jupyter/Python Debugger 확장·새 터미널 필요 이유: 기존 본문과 `qa/research.md`(2026-09-09 공식 문서 조사) 범위 안에서만 다시 씀. 새 설치 명령·버전은 추가하지 않음
- `pwd`/`Get-Location`, `ls`/`Get-ChildItem`, `cd`, File → Open Folder, Terminal → New Terminal: 기존 본문 내용 유지. 교재 실행 검증에 포함하지 않았다고 본문에 적음
- pathlib `relative_to`, tempfile `TemporaryDirectory.cleanup()`: 노트북 실행 출력과 Python 3.12 공식 문서(2026-09-16 조회)로 확인
- 확인 필요: VS Code 터미널 패널의 셸 이름 표시 위치(본문은 「터미널 패널에 보이는 셸 이름」으로만 적음), Windows에서 `relative_to()` 출력이 역슬래시로 보이는지(본문은 「보일 수 있습니다」로 적고 실행하지 않았다고 명시)

## 검토에서 볼 곳

- 02-2 도식의 「명령을 찾지 못함」 분기는 실행하지 않은 절차라 빨강 대신 회색(01-1 거짓 분기와 같은 방식)
- 삽화 인물 시선이 서랍보다 정면을 향함. 메모(서랍 스케치)·빈 서랍·왼쪽 방의 편지로 관계는 읽혀 채택
- 03절 「앞에서 배운 내용」(VS Code·uv 설치, 폴더 열기, 현재 위치 확인)과 05절 「명령이 발견되는지와 실행이 성공했는지 구분」과의 연결은 본문 설치 확인 단락·02-2 도식으로 유지

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 2·하 5, 공통 C-1 중·C-4 하). 모두 반영했습니다.
- C-1(중): 코드 셀 12개 모두 `upgrade_allow=["stdlib-import"]`. 준비 설명의 import 문장은 「1절에서 본 불러오기 줄(`import`)로…」로 1절과 잇기
- 02-1(중): 학습 목표·용어 표의 「실습 폴더」 → 「연습 폴더」(`course-ch01`), 「다음 학습」은 「교재가 준비한 실습 폴더를 내려받아…」, 노트북 정리의 다음 절 문장과 [8] 「연습 프로젝트 폴더」
- 02-2(중): [9]에 「괄호 안에 넣어 메서드에 건네는 값을 인자라고 합니다.」, [15]에 「1절의 `price`처럼 값을 저장한 이름을 변수라고 합니다.」
- 02-3(하) 셸 이름에 bash(「대부분의 Linux는 bash」), 02-4(하) 입력 표시에 `%`, 02-5(하·C-4) 「설치 조건이 더 많은 Docker Desktop은…」, 02-6(하) 「코드 `tempfile.TemporaryDirectory()`를 부르면 새 임시 폴더가 만들어집니다.」(클래스라 「함수」를 뺌, 기기 셸 Python 3.10.12에서 `inspect.isclass(tempfile.TemporaryDirectory)` True 확인), 02-7(하) 주의 5번째 항목을 노트북의 `base_folder` 이유로 고침

재실행: `run_section.sh … 02`(새 커널 PASS, 코드 셀 출력은 수정 전과 글자 단위로 같음) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 84 code cells (max 14 lines)`, `visual.cjs` 7페이지 × 1280·390px 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 강사 확인(2차 검토는 보고서 「다음 조치」 4대로 중 항목과 C-4 문장만 대조하면 됨)
- 실습 묶음 `textbook/downloads/ch01-practice.zip` 재생성(C-2, 전체 챕터가 끝난 뒤 일괄)
