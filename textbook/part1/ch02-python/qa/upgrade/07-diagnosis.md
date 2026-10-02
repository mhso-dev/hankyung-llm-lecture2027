# 07-모듈과-타입힌트 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/07-concept.*`).
생성기: `qa/upgrade/author_07.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 07`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01~06절 개선본(`_src`, 노트북, `author_01.py`~`author_06.py`, `06-diagnosis.md`, `06-figures.md`), `qa/upgrade/handoff.md`의 `## §06 → §07`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 8 | 0 |
| G6 | 17 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 11 (준비 1 + example 7 + before 2(심화 1) + after 1) |
| 검사한 문장 | 104 | 331 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, 2026-09-16, 오류 출력 0), verify PASS(12절 129셀). 수정 후 수치는 `gates-wip-07.json`. 수정 전 수치는 `gates-before.json`(덮어쓰지 않음). 빌드 HTML 가로 넘침 없음(puppeteer 1280px·390px에서 scrollWidth 1280·390). `visual.cjs` 전체 검사는 다시 실행하지 않았습니다.

## 수정 전 주요 문제

- **아직 안 배운 문법(G1이 잡지 않음)**: 준비 셀에 `from subprocess import run`·`from sys import executable`·`TemporaryDirectory`·`Path`, 모듈 실행을 `run([executable, "run_price.py"], cwd=..., capture_output=True, text=True, check=True)`로 하위 프로세스에서 확인(한 줄에 인자 5개). `label_price()` 본문의 형식 지정 f-string `f"{price:,}원"`(1~6절에서 안 배움). `(module_dir / "pricing.py").write_text(...)`의 경로 `/` 잇기. import의 뜻을 설명하기 전에 준비 셀이 import 네 줄을 씀
- **이어짐 결함**: 「앞에서 배운 내용」이 「04절 함수, 05절 `Path.write_text()`」(개선된 5절은 `with open`·`write()`), 「06절의 클래스는 필수 선행 지식이 아닙니다」. 6절이 약속한 `__main__` 설명과 1·5절 준비 셀 import의 뜻을 풀지 않음. 1절 Before(`"2"` × 3 = 222)와 같은 구조의 실패인데 연결 없음. 데이터(`add_tax(10000, 0.1)`·`label_price(12000)`·`double_total("1200")`)가 앞 절 데이터와 무관
- **설명**: 한 단락에 import 검색 위치·최상위 문장 실행·네임스페이스·`import`와 `from` 비교를 모두 담음(70자 초과 3). 「네임스페이스」「런타임 검증」「정적 타입 검사」를 정의만 하고 노트북에서 보이지 않음. 실패 셀에 `assert wrong == "12001200"`로 틀린 결과를 단언
- G5: 제목 셀·「오늘 볼 그림」 없음, 결과 읽기 셀 없음(코드 셀 뒤 설명 없음 6곳). 값 바꿔 보기가 12,000 → 25,000 표시 형식 비교라 학습 질문과 무관
- G6: 코드 이름+조사로 시작하는 문장 12개(「`from pricing import add_tax`는」, 「Before의 `double_total()`은」, 「Python은」 등), 70자 초과 3개
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 도식 `07-concept.svg`는 모듈 흐름과 타입힌트 비교를 한 그림에 넣음

## 바꾼 것

- 노트북(paired 유지): 제목(API 키 불필요·호출 0번·1분 이내) → 오늘 볼 그림(07-1) → 준비(5절과 같은 `os`·`tempfile` 임시 폴더, `[]`) → 6절 `OrderLine` 정의를 글로 적어 `order_tools.py`에 저장(`179`, `['order_tools.py']`) → `import order_tools`와 `order_tools.OrderLine("연필", 3)`(`5`, `<class 'order_tools.OrderLine'>`) → 모듈 이름(`__main__`·`order_tools`·`os`, `<class 'module'>`) → `from order_tools import OrderLine`(note `4`, 같은 자료형) → 4절 함수에 타입힌트(`calculate_line_total(unit_price: int, quantity: int = 1) -> int`) 정의·호출(`78000`, `<class 'int'>`) → 값 바꿔 보기 수량 3(`117000`) → Before 쉼표로 나눈 단가 글자 그대로(`3900039000`, `<class 'str'>`, `False`)·심화 `__annotations__` → After `int()` 뒤 넣기(`78000`, `True`, assert) → 정리
- **학습 질문·실패 구조·형식 유지**: 질문 「타입힌트는 문자열 입력을 거부하나요?」를 「정의 줄에 `unit_price: int`라고 적어 두면, 문자열 단가를 넣을 때 Python이 막아 줄까요?」로 쉽게 바꿈(뜻 같음). 「타입힌트 int 함수에 숫자 모양 문자열 → 곱셈이 글자를 이어 붙임 → `int()`로 바꾼 뒤 넣음」 구조와 「모듈 파일을 만들어 import」 흐름을 유지. 데이터만 앞 절 것으로 바꿈: `"1200"`·`double_total` → 5절식 줄 「무선 키보드,39000」과 4절 `calculate_line_total`(39000·2 → 78000), `pricing.py`·`run_price.py` 하위 프로세스 → 6절 `OrderLine`을 담은 `order_tools.py`를 노트북 커널에서 직접 import
- **6절 약속 이행**: `<class '__main__.OrderLine'>`의 `__main__`을 「직접 실행하는 코드(이 노트북)의 모듈 이름」으로 풀고, 같은 클래스를 모듈 파일로 옮기면 `<class 'order_tools.OrderLine'>`이 되는 것을 출력으로 보임(07-2 그림). 1·5절 준비 셀 import는 「표준 라이브러리 모듈 os를 불러오는 import 문, `os.chdir()` = 모듈 이름.함수」로 3번 소제목·복습 4에서 풂
- 사다리: L4가 처음 허용되는 절. 이 절에서 가르치는 import 문·from import 문·`__name__`·타입힌트만 새로 씀. G1이 이 문법을 잡지 않으므로 `upgrade_allow`는 쓰지 않음(클래스는 모듈 파일에 쓸 문자열 안에만 있어 `class_def`도 해당 없음). 모듈 파일 안 클래스는 6절 정의 셀과 같은 모양(`__init__` + `add_count()`)을 유지하고 새 규칙을 만들지 않음. 형식 지정 f-string·`subprocess`·`pathlib`·`Path.write_text()` 없음. `__annotations__`는 심화 셀에만(4절 `__defaults__`, 6절 `__dict__`와 같음)
- 앞 절과의 연결: Ch 1 1·3절 import·모듈·표준 라이브러리 용어 → 3번 소제목의 정의, Ch 1 2절 `from pathlib import Path` → from import 문, 1절 Before 222와 `int()` → Before/After, 1절 수량 3 → 117000.0 → 값 바꿔 보기 117000(int), 4절 `calculate_line_total` → 타입힌트를 적은 같은 함수, 5절 쓰기 모드·`write()`·`split(",")`·`parse_order()`의 `int()` → 모듈 파일 쓰기와 Before, 6절 `OrderLine`·pencil 3 → 5·note 2 → 4 → 모듈 파일의 클래스, 6절 `__main__` → 모듈 이름. 삽화도 3~6절의 좌우 Before/After 구도를 이어 씀
- 본문 10블록 전체를 다시 씀. 용어 7개 표, 「앞에서 배운 내용」 표 7행, 「확인한 범위」(정수로 바꿀 수 없는 글자·정적 타입 검사기·python 명령으로 실행한 파일의 `__main__`·모듈 수정 뒤 다시 불러오기 미실행), 복습 6문항(4 → 6), 참고 자료 5개(Python 3.12 자습서 6.1·6.1.1·6.1.2·4.9.8과 typing 문서를 내려받아 문장 확인: 모듈 = 정의를 담은 파일·`__name__`, 최상위 문장은 처음 import 때만 실행, 모듈을 고치면 인터프리터를 다시 시작, 스크립트로 실행하면 `__name__`이 `"__main__"`, 어노테이션은 `__annotations__`에 저장되고 함수의 다른 부분에 영향 없음, 실행기는 타입힌트를 강제하지 않음)
- 그림: Mermaid 4장(모듈 불러오기, 모듈 이름, import 두 방법, Before/After) + 삽화 1장(저금통 스티커, 1회 생성 통과). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 실행 근거 확인: 실행 도구 커널의 `sys.path`에 `''`가 있어 `os.chdir()` 뒤 임시 폴더의 모듈 파일을 import 할 수 있음을 별도 시험 노트북(`/tmp`)으로 확인. 본문 「노트북에서는 현재 작업 폴더도 이 목록에 들어 있습니다」의 근거

## 검토에서 볼 곳

- 모듈 파일을 `"""…"""` 문자열로 적어 `write()`로 저장하는 방식(5절 연결). 코드가 문자열이라 문법 색이 없고, 학생이 VS Code에서 `order_tools.py`를 직접 만드는 방법은 안내하지 않음. Jupyter 매직 `%%writefile`은 새 도구라 택하지 않음
- 이 절은 모듈(클래스)과 타입힌트(함수)를 다른 예제로 다룸. 타입힌트를 적은 함수는 모듈 파일이 아니라 노트북 셀에서 정의함(같은 모듈 파일을 다시 쓰면 같은 커널에서 새로 읽지 않는 문제를 피하려고). 본문은 「모듈로 나눈 정의는 정의를 열어 보지 않고 부르므로 타입힌트가 필요」로 잇기만 함
- 「노트북 셀에서 정의한 이름은 모두 `__main__`에 속합니다」는 이 노트북 출력(`__name__` = `__main__`)과 6절 자료형 출력에 근거. python 명령으로 파일을 실행한 경우는 자습서 6.1.1 인용이고 실행하지 않음. `if __name__ == "__main__":` 관용구는 다루지 않음
- 삽화의 스티커가 투입구 바로 아래가 아니라 몸통 가운데에 있음(검수에서 채택)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-A.md`

- 판정 accept-with-fixes(중 1, 하 3, 공통 C-4·C-6 하). 모두 반영했습니다.
- 07-1(중, 사실 오류): 주의할 점 「모듈 파일에는 random.py처럼 … 작업 폴더의 파일이 표준 라이브러리 모듈을 가려, 그 모듈을 쓰는 다른 import까지 실패할 수 있습니다. 이 장면은 노트북에서 실행하지 않았습니다.」
- 07-2: Ch 1 3절 모듈 정의와 잇는 문장(노트북 2번·용어 표·본문). 07-3: 「저금통 몸통에」. 07-4: 노트북 2번 결과 읽기에 VS Code로 만드는 길(실행하지 않음)
- C-4: 확인한 범위·다음 학습 「확장 경로(B)의 10절 Pydantic」. C-6: handoff §07→§08 셋째 문장 보충, 위 게이트 표 검사한 문장 330 → 331(`gates-wip-07.json`). 반영 뒤 335
- 검토 밖: `visual.cjs`가 07-3 SVG 글자 11.4px를 잡아 라벨 줄바꿈으로 폭 1066 → 861(PNG 확인)
- 새 커널 출력은 반영 전과 같음. 코드 셀 11

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/07-모듈과-타입힌트.md`
- 8절 기존 본문의 「07절의 모듈과 타입힌트는 이 절의 필수 선행 지식이 아닙니다」와 `Path`·`subprocess` 준비는 8절 작업자가 판단(`handoff.md`)
- 챕터 전체 `gates-after.json`과 루트 `textbook/qa/upgrade-progress.md` 갱신은 챕터를 마친 뒤
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
