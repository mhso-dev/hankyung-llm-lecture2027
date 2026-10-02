# 08-pytest — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/08-concept.*`).
생성기: `qa/upgrade/author_08.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 08`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01~07절 개선본(`_src`, 노트북, `author_01.py`~`author_07.py`, `07-diagnosis.md`, `07-figures.md`), `qa/upgrade/handoff.md`의 `## §07 → §08`, Ch 1 3절 노트북의 `subprocess.run` 셀.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 10 | 0 |
| G6 | 15 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 13 (준비 2 + example 5 + before 3 + after 3(심화 1)) |
| 검사한 문장 | 108 | 318 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, pytest 9.1.1, 2026-09-16, 오류 출력 0), verify PASS(12절 135셀). 수정 후 수치는 `gates-wip-08.json`. 수정 전 수치는 `gates-before.json`(덮어쓰지 않음). 빌드 HTML 가로 넘침 없음(puppeteer 1280px·390px에서 scrollWidth 1280·390). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.

## 수정 전 주요 문제

- **아직 안 배운 문법·도구(G1이 잡지 않음)**: 준비 셀 `from subprocess import run`·`from sys import executable`·`TemporaryDirectory`·`Path`, `os.environ.copy()`와 환경 변수 `PYTEST_DISABLE_PLUGIN_AUTOLOAD`, `run_pytest(folder: Path, target: str)`가 `run([...], cwd=folder, env=pytest_env, capture_output=True, text=True)`를 반환(반환 자료형 표시 없음), `(test_dir / "x.py").write_text()`의 경로 `/` 잇기, 기본 경로의 `@pytest.mark.parametrize`(L6, 9절 전), `param_test.replace(...)`로 테스트 글을 바꾸는 방식, 할인 식 `int(price * 0.9) + 100`(숫자를 식 안에 바로 씀), `%pip install`
- **이어짐 결함**: 「앞에서 배운 내용」이 「07절의 모듈과 타입힌트는 이 절의 필수 선행 지식이 아닙니다」라고 적음. 7절이 가르친 모듈 파일·from import 문과 연결이 없고, 테스트 파일이 모듈을 import 하지 않음(함수 정의를 테스트 파일 안에 둠). 7절 「다음 학습」의 「검사할 코드도 파일에 적어 두고 실행」 약속을 받지 않음. 데이터 `1200 + 800`·`discounted(10000)` 9100/9000·`(1000, 1, 1000)`이 앞 절 데이터와 무관. Ch 1 3절 `subprocess.run`·종료 코드와의 연결이 없음
- **설명**: 한 단락에 종료 코드·`run_pytest()`·`subprocess.run()`·반환 객체 속성을 모두 담음. 「테스트 케이스」「픽스처」를 정의만 하고 노트북에서 보이지 않음. 실패 출력의 `>` 줄·`E` 줄을 읽는 방법이 없음
- G5: 제목 셀·「오늘 볼 그림」 없음, 결과 읽기 셀 없음(출력을 인용한 결과 읽기 0). G6: 코드 이름·영문으로 시작하는 문장 13개(「pytest는」, 「`run_pytest(folder, target)`는」, 「Before의 `discounted()`는」 등), 70자 초과 2개. G7: Mermaid 0장, 삽화 0장, 설계표 없음

## subprocess가 이 절에 필요한지 (handoff §07 → §08의 판단 거리)

결론: **쓴다.** 다만 기존 준비를 줄이고, Ch 1 3절과 같은 모양으로만 씁니다.

- 필요한 이유: 이 노트북의 학습 목표 3(결함에서 실패 → 함수만 고쳐 같은 테스트 통과)은 **같은 커널에서 모듈 파일을 고쳐 쓴 뒤 테스트를 다시 실행**해야 보입니다. 커널 안에서 `pytest.main()`을 여러 번 부르면 Python import 캐시 때문에 고친 파일이 반영되지 않습니다. pytest 9.1.1 소스 배포본 `doc/en/how-to/usage.rst`(Calling pytest from Python code)가 이 이유로 같은 프로세스에서 여러 번 부르는 방법을 권하지 않고, 7절 본문도 「모듈은 처음 불러올 때 한 번만 실행」(Python 자습서)이라고 가르쳤습니다. 부를 때마다 새 Python을 띄우면 이 문제가 없습니다(After에서 고친 파일로 `3 passed` 관찰). 커널 안 `pytest.main()` 재호출 장면은 실행하지 않았습니다.
- 대안 검토: `pytest.main()`(위 캐시 문제, 모듈 이름을 바꾸면 「같은 테스트·구현만 고침」 구조가 깨짐), `!pytest` 셸 명령(IPython 전용 문법이고 셸의 python이 커널 Python과 다를 수 있음, 종료 코드를 변수로 받지 못함), `importlib.reload`·`sys.modules` 조작(안 배운 도구). 모두 택하지 않음
- 연결: Ch 1 3절 노트북이 `kernel_command = [sys.executable, "-c", import_code]` → `subprocess.run(kernel_command, capture_output=True, text=True)` → `.returncode`(종료 코드)를 이미 가르쳤으므로 새 도구가 아닙니다. 사다리 L4(패키지 import, 라이브러리 함수 호출)는 7절 뒤 허용이고, 7절이 import의 뜻을 가르쳤습니다
- 줄인 것: `os.environ.copy()`·플러그인 자동 로드 끄기(실습 폴더 가상환경에 pytest11 플러그인 0개를 2026-09-16 확인), `cwd=`(5·7절처럼 `os.chdir()`로 작업 폴더를 옮김), `Path`·`TemporaryDirectory`, 함수 인자 두 개. 함수는 `run_pytest() -> int` 하나(본문 4줄: 명령 목록, `subprocess.run`, `print(result.stdout)`, `return result.returncode`)
- 더한 것: `--color=no`. 실행 도구 커널 환경에서 pytest가 ANSI 색 기호를 출력에 넣어(첫 실행에서 확인) 결과 읽기 인용과 HTML이 깨졌습니다. 옵션 뜻은 노트북·본문에 한 문장으로 적음
- 알려진 제약: 새 Python은 `__pycache__` 기록을 원본 파일의 수정 시각(초)·크기로 확인하므로, 실행 도구가 1초 안에 같은 크기로 파일을 다시 쓰면 옛 기록을 읽을 수 있습니다. 다시 쓰는 파일은 글자 수가 달라지게 두었습니다(price_tools.py 130 → 262 → 295, test_price_tools.py 152 → 255). 생성기 docstring에 적음. 학생에게는 보여 주지 않음

## 바꾼 것

- 노트북(paired 유지): 제목(API 키 불필요·호출 0번·1분 이내, `uv sync --locked`로 pytest 설치) → 오늘 볼 그림(08-1) → 준비(pytest 버전 `9.1.1`, 5·7절과 같은 임시 폴더 `[]`) → 7절 타입힌트 함수 `calculate_line_total()`을 모듈 파일 price_tools.py에 저장(`130`) → 테스트 파일 test_price_tools.py(from import + `test_two_keyboards`, `152`, 파일 두 개) → `run_pytest()` 정의 → 실행(`.`, `[100%]`, `1 passed`, 종료 코드 `0`) → 값 바꿔 보기: 4절 수량 생략 테스트 `test_one_keyboard` 더하기(`..`, `2 passed`) → Before: 모듈에 `read_unit_price()`를 더하며 `int()` 빠뜨림(`262`), 테스트 파일 test_unit_price.py(기대값 정수 39000, `150`), 실행(`..F`, `E       AssertionError: assert '39000' == 39000`, `test_unit_price.py:6`, `1 failed, 2 passed`, 종료 코드 `1`) → After: `unit_price = int(unit_price_text)` 한 줄(`295`), 같은 테스트 실행(`...`, `3 passed`, 종료 코드 `0`, `assert exit_code == 0`) → 원리 더 알아보기(심화): `@pytest.mark.parametrize` 수량 1·2·3(`......`, `6 passed`) → 정리
- **학습 질문·실패 구조·형식 유지**: 질문 「결함을 고친 뒤 같은 테스트가 통과하나요?」를 「단가를 꺼내는 함수에서 `int()` 줄을 빠뜨렸을 때, 기대값 39000을 적어 둔 테스트는 실패로 알려 줄까요? 함수만 고치면 같은 테스트가 통과할까요?」로 구체화(뜻 같음). 「기대값은 두고 구현 한 줄만 고침 → failed·종료 1에서 passed·종료 0」 구조와 paired 형식을 유지. 데이터만 앞 절 것으로 바꿈: `discounted(10000)`의 +100 → 7절 Before와 같은 `int()` 빠뜨림(7절에서는 타입힌트가 못 막고 사람이 출력으로 찾았고, 이번에는 테스트가 찾음)
- **7절 연결(선행 관계 고침)**: 「07절은 필수 선행 지식이 아님」을 지우고 「이 절은 7절에 바로 이어집니다」로 바꿈. 모듈 파일을 글로 적어 `with open("w")`·`write()`로 저장(7절 order_tools.py와 같은 방법), 테스트 파일이 7절 from import 문으로 모듈을 불러옴, 7절 「모듈은 처음 불러올 때 한 번만 실행」을 새 Python 실행의 이유로 씀, 7절 값 바꿔 보기 117000을 심화 셀 기대값으로 씀
- 사다리: G1이 잡는 문법을 새로 쓰지 않아 `upgrade_allow` 없음. 매개변수화(`@` 줄, L6)는 기본 경로에서 빼 After 뒤 심화 셀(`lesson_level="deep-dive"`)로 옮기고 「`@` 줄의 뜻은 9절」이라고 적음(기본 경로의 마지막 코드 셀 뒤라 기본 경로가 심화 셀의 파일을 쓰지 않음). 테스트 함수·모듈 함수는 파일에 쓸 글 안에만 있음. 타입힌트는 7절 모양(`-> int`, `: str`)만 쓰고 `-> None`은 쓰지 않음. 「픽스처」「테스트 케이스」 용어는 뺌(픽스처는 11절 몫)
- 본문 10블록 전체를 다시 씀. 「앞에서 배운 내용」 표 6행, 용어 8개 표, 「테스트 파일과 테스트 함수」「pytest가 테스트를 찾아 실행하는 차례」「노트북에서 pytest를 새 Python으로 실행하는 이유」「결과 줄 읽기」 소제목, 「확인한 범위」(입력 한 줄만, 심화 셀은 출력만, 커널 안 pytest 재호출·터미널 실행·다른 출력 옵션 미실행), 복습 6문항(4 → 6), 참고 자료 8개. pytest 9.1.1 소스 배포본 문서로 문장 확인: 테스트 찾기 규칙(`test_*.py`·`*_test.py`, `test`로 시작하는 함수, 인자 없으면 현재 폴더), `python -m pytest`는 현재 폴더를 `sys.path`에 더함, `pytest.main()` 재호출 비권장, 종료 코드 0·1, `-q` = Decrease verbosity
- 그림: Mermaid 4장(한 번 실행의 차례, 새 Python 두 번 sequenceDiagram, 실패 설명 읽기, Before/After) + 삽화 1장(동전 저울, 1회 생성 통과, 7절 삽화의 동전 그림 종이 카드를 이어 씀). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 검토에서 볼 곳

- subprocess 판단(위 절)과 `--color=no`·파일 글자 수를 다르게 둔 이유. 학생이 VS Code에서 같은 셀을 사람 속도로 다시 실행하면 수정 시각이 달라 문제없지만, 실행 도구로 1초 안에 같은 크기 파일을 다시 쓰는 경우는 시험하지 않음
- 매개변수화를 심화 셀로 옮긴 것(기존 학습 목표 2 → 원리 더 알아보기). 9절 작업자가 「`@` 줄」 설명에서 이 셀을 되짚을지
- 삽화: 동전이 접시 안에 세워져 있음(채택). 본문은 왼쪽 접시 = 함수가 반환한 실제값, 오른쪽 접시 = 기대값으로 읽게 해 `assert unit_price == 39000`의 왼쪽·오른쪽과 방향을 맞춤

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept-with-fixes(중 1, 하 2). 모두 반영했습니다. 결정: 매개변수화 심화 유지, subprocess 유지
- 08-1(중): 노트북 2번·본문 「테스트 파일이 있는 폴더의 터미널에서 `uv run python -m pytest -q --color=no`를 입력하는 것과 같은 일입니다. 노트북은 두 파일을 임시 폴더에 두었으므로, 실습 폴더에서 그대로 입력하면 찾을 테스트가 없습니다.」(노트북 단락은 5문장 규칙으로 나눔)
- 08-2: 오늘 볼 그림 alt를 08-1 caption alt로. 08-3: 다음 학습 9절 링크
- index A트랙 과제 1·5가 이 절의 매개변수화 심화·`read_unit_price`·`run_pytest()`를 가리키도록 고침(C-2)
- 새 커널 출력은 반영 전과 같음. 코드 셀 13, 검사한 문장 322

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/08-pytest.md`
- 화면 확인용 캡처를 실수로 `qa/upgrade/_shot08/`(b4.png·b6.png)에 복사함. 삭제 금지라 남겨 둠(메인 세션이 정리)
- 챕터 전체 `gates-after.json`과 루트 `textbook/qa/upgrade-progress.md` 갱신은 챕터를 마친 뒤
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
