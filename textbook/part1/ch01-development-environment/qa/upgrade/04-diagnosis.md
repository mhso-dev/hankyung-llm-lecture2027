# 04-첫-스크립트와-디버거 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/04-debugging.*`).
생성기: `qa/upgrade/author_04.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch01-development-environment 04`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 1 | 0 |
| G2 | 1 | 0 |
| G3 | 1 | 0 |
| G4 | 0 | 0 |
| G5 | 6 | 0 |
| G6 | 30 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 5 | 14 (준비 1 + 본 경로 13, 심화 셀 없음) |
| 검사한 문장 | 158 | 296 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Linux aarch64 기기 VM, 2026-09-16), verify PASS(5절 58셀). 빌드 HTML 1280px·390px에서 가로 넘침 없음(scrollWidth 1280/390, 로컬 puppeteer, `qa/upgrade/_shot04/`).

## 수정 전 주요 문제

- G1·G2: pdb 출력 정리를 두 줄에 걸친 리스트 내포식(`[line.removeprefix(...) for line in ... if ...]`)으로 작성, 그 셀이 15줄 초과. f-string 출력, 한 줄에 인자 다섯 개를 몰아 쓴 `subprocess.run(...)`
- G3: 준비 셀 첫 줄 주석 없음
- G5: 제목 셀·「오늘 볼 그림」 없음. 코드 셀 뒤 결과 읽기 셀이 출력 값을 인용하지 않음
- G6: 70자 초과 문장 9개(학습 목표, 확장 세 개를 한 문장에 설명, 도식 색 설명 등), 코드 이름+조사로 시작하는 문장 다수(「`pdb`는」, 「`b 4`는」, 「`strip()`은」 등), 5문장 넘는 단락
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. Excalidraw 도식 `04-debugging.svg`은 VS Code 화면(노란 현재 줄·Variables 패널)을 그렸지만 노트북은 그 화면을 실행하지 않음
- 내용: 「중단점 줄은 실행 직전에 멈춘다」를 VS Code 화면 기준으로 사실처럼 설명했지만 노트북은 4번 줄(print 줄)에 중단점을 둬서 그 성질을 보여 주지 못함. 03절이 정한 인터프리터·커널·Python Debugger 확장 설치를 다시 정의(02·03절과 중복). 「앞에서 배운 내용」이 개선 전 03절(「프로젝트 안에 .venv를 만들고 Python 3.12를 선택」) 기준

## 바꾼 것

- 노트북(paired, 학습 질문·price 3000/count 2·`+`→`*`·pdb 유지): 제목 셀(API 키 불필요, 호출 0번·비용 없음·1분 이내) → 오늘 볼 그림(04-1) → 준비(import 4개) → 임시 폴더와 파일 경로 세 개(`False`) → `hello.py`와 같은 네 줄 저장(코드 줄 수 `4`, 3번 줄 `total = price * count`) → 커널 Python으로 실행(`총액: 6000원`, 종료 코드 `0`) → 예상 출력 비교 `True` → **Before**: `replace()`로 `*`→`+`(`총액: 3002원`, 종료 코드 `0`) → 예상 비교 `False`(논리 오류) → 디버거 명령 8개 목록 → `python -m pdb`에 `input`으로 입력(종료 코드 `0`) → for·여러 줄 if로 위치 줄을 뺀 출력(`-> total = price + count`, `3000`, `2`, `*** NameError: name 'total' is not defined`, `3002`) → **After**: `+`→`*`(`총액: 6000원` `True`) → 같은 디버거 명령(3번 줄 앞 NameError, `n` 뒤 `6000`) → **값 바꿔 보기**: `count = 3`(`총액: 9000원` `True`) → cleanup `False` → 정리
- 디버거 명령을 `b 4`(print 줄)에서 `b 3`(계산 줄) + `p total` 두 번 + `n`으로 바꿈. 「멈춘 줄은 아직 실행 전」을 VS Code 화면 설명 대신 실제 pdb 출력(NameError → n 뒤 3002)으로 뒷받침
- 스크립트 출력을 숫자만 찍는 별도 형식(`print(total)`+`int()`)에서 `hello.py`와 같은 `총액: {total}원` 형식으로 통일하고, 예상도 출력 모양 `총액: 6000원`으로 비교
- 사다리: 기본 경로는 대입·print(쉼표 인자)·`==`·`in`·`not`·`and`·for·여러 줄 if·인덱싱 `[2]`·`len()`·`assert`, 준비 셀의 표준 라이브러리 import(환경 챕터 예외(`QUALITY-UPGRADE.md` §2 끝)로 표준 라이브러리 import와 그 결과 값의 메서드를 쓰고, import나 점(.)으로 부르는 메서드·속성이 있는 코드 셀에 `upgrade_allow=["stdlib-import"]`를 적음), 글·경로·실행 결과의 메서드(`write_text`·`splitlines`·`strip`·`replace`·`removeprefix`·`is_file`·`is_dir`·`cleanup`)만 사용. 내포식·f-string 출력 제거. 스크립트 글 안의 f-string은 `hello.py` 원문이라 유지하고 본문·노트북에서 뜻을 설명
- 이어짐: 01절 단가 3000·수량 2·예상 6000·「실행 전에 예상」·수량 3→9000, 01절 복습 3번(오류 없이 3002)을 「배우는 이유」의 출발점으로 씀. 02절 `workspace`·`write_text()`·`is_file()`·`cleanup()`·기준 폴더(터미널 현재 폴더), 03절 `sys.executable`·`subprocess.run(capture_output, text, check)`·`stdout`·`splitlines()`·`returncode`·`uv run`·인터프리터 `.venv`를 다시 정의하지 않고 이어 씀. 인터프리터·커널·확장 설치 설명은 뺌
- 본문 10블록 전체를 다시 씀. 요리 그릇 비유(그릇 = 줄, 빈 셋째 그릇 = 아직 없는 total, 빨간 점 = 중단점), 용어 6개 표(스크립트·확장자·논리 오류·디버거·중단점·한 줄 실행), `hello.py` 줄 표, 글 기능 5행 표, pdb 명령 ↔ VS Code 조작 표, 「VS Code에서 같은 장면 찾아보기」 6단계(이번에 실행하지 않았다고 명시), 복습 5문항(01~03절 형식)
- 그림: Mermaid 4장(04-1 멈춘 줄, 04-2 저장·실행, 04-3 기호 비교, 04-4 출력 고르기) + 삽화 1장(04-5 그릇 앞에서 멈춤, 1회 생성 채택). 기존 Excalidraw 도식은 본문에서 뺌(원본은 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 사실 주장 확인

- 실행 출력으로 확인(2026-09-16, 기기 VM, Python 3.12.13): 노트북 전체 출력. 기기 셸에서 `uv run python hello.py`(실습 폴더) → `총액: 6000원`·종료 0, 같은 명령을 `notebooks` 폴더에서 → `can't open file '…/notebooks/hello.py': [Errno 2] No such file or directory`·종료 2. pdb 원문 출력에 `Breakpoint 1 at …/price_bug.py:3`, `> …price_bug.py(3)<module>()` 줄이 있음(노트북은 이 줄을 걸러 냄)
- Python 3.12 pdb 문서: `python -m pdb`, `b(reak)`, `c(ont(inue))`, `p`, `n(ext)`, `q(uit)`
- VS Code 문서(2026-09-16 조회): 편집기 여백 클릭 또는 F9로 중단점(빨간 원), F5 Start/Continue, F10 Step Over, Shift+F5 Stop, Run and Debug 보기의 VARIABLES, 실행 단추 메뉴의 `Python Debugger: Debug Python File`, launch.json 없이 F5 → `Python File`, 디버거는 워크스페이스에서 고른 인터프리터 사용(Python 디버깅 페이지 표시 2026-02-04). **VS Code 문서에는 「중단점 줄 실행 전에 멈춘다」는 문장이 없음** → 본문은 이 성질을 pdb 결과로만 말하고, VS Code 화면은 「이번에 실행하지 않았습니다」로 적음
- 확인 필요: VS Code 편집기 탭의 저장 안 됨 표시 모양(본문에서 뺌). Windows에서 pdb 출력의 위치 줄 모양(파일 이름이 들어 있으므로 같은 필터로 걸러질 것으로 보나 실행하지 않음)

## 검토에서 볼 곳

- 04-1·본문 「디버거가 멈추는 자리」가 pdb 출력(NameError → `n` 뒤 3002)과 1:1로 맞는지, VS Code 안내 6단계가 실행하지 않은 범위로 한정됐는지
- 디버거 출력 고르기 셀(for + `if not has_location and text != ""`)이 Ch 1 학생에게 읽히는지. 04-4 그림과 결과 읽기가 이를 풀어 주는지
- 05절(아직 개선 전)의 임시 Git 저장소 `hello.py`와 이번 절의 실습 폴더 `hello.py`는 다른 파일. 이 절 「다음 학습」은 특정 파일을 전제하지 않게 적음

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 1·하 5, 공통 C-1 중·C-3 하·C-4 하). 모두 반영했습니다.
- C-1(중): 코드 셀 14개 중 12개 `upgrade_allow=["stdlib-import"]`(글자 비교만 하는 두 셀은 표시 없음)
- 04-1(중): 실습 폴더 `labs/part1/ch01-development-environment/hello.py`의 빈 4번 줄을 지워 본문 표·노트북 「네 줄」과 맞춤(`cat -n` 4줄, `uv run python hello.py` → `총액: 6000원` 기기 셸 확인). 배포 묶음 zip은 아직 옛 파일(C-2와 함께 일괄 재생성)
- 04-2(하): 04-1 그림 멈춤 2의 초록 상자를 `print(f"총액: {total}원")` 아직 실행 전으로 바꾸고 범례·캡션을 「멈춘 줄(아직 실행 전)」로 고침(pdb 출력 `-> print(f"총액: {total}원")`과 일치). 본문 「4번 줄 `print` 앞의 멈춤 2」
- 04-3(하): 결과 읽기 [29] 끝에 `Breakpoint 1 at …price_bug.py:3` 원문 줄 설명과 「기기 셸에서 따로 확인」(기기 셸 pdb 재실행으로 줄 모양 확인)
- 04-4(하): 04-4 그림 출력 예시를 `3000 같은 줄`로 바꿔 3002 빨강과 겹치지 않게 함(캡션·alt·도식 읽기 함께). 04-5(하): 준비 셀 설명 「스크립트 파일 네 개」, `price_changed.py`는 값 바꿔 보기 셀에서 정함. 04-6(하): 「이번 절에서 새로 쓰는 기능은…」
- C-3(하) 「경로 기능 `Path`」, C-4(하) 「중단점은 VS Code에서도 빨간 점으로 보입니다.」

재실행: `run_section.sh … 04`(새 커널 PASS, 코드 셀 출력은 수정 전과 글자 단위로 같음) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 84 code cells (max 14 lines)`, `visual.cjs` 7페이지 × 1280·390px 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 강사 확인(2차 검토는 보고서 「다음 조치」 4대로 중 항목과 C-4 문장만 대조하면 됨)
- 실습 묶음 `textbook/downloads/ch01-practice.zip` 재생성(C-2, 전체 챕터가 끝난 뒤 일괄)
