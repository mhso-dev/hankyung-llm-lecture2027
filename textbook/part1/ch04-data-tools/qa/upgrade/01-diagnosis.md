# 01-Pandas로-표-다루기 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/01-dataframe-flow.*`, `_gen_figures.py`).
생성기: `qa/upgrade/author_01.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch04-data-tools 01`.
챕터 첫 절이라 먼저 `upgrade_gates.py --label before`를 실행했습니다(`gates-before.json`, 5절 합계 237건).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 6 | 0 |
| G6 | 42 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 16 (준비 1 + 본문 15) |
| 검사한 문장 | 130 | 339 (검토 반영 뒤, `gates-after.json`) |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, pandas 3.0.5, 2026-09-16), verify PASS(챕터 5절 41셀), `visual.cjs` 1280·390px PASS(이 절 HTML을 `/tmp`에 복사해 실행), 실습 폴더 pytest 10 passed(`data_tools.py`는 고치지 않음).

## 수정 전 주요 문제

- G1: `assert [row["order_id"] for row in paid] == …` 목록 내포식 2곳
- 사다리 밖 문법(게이트가 세지 않은 것): `from pathlib import Path`·`TemporaryDirectory`(Ch 3 요약 「가르치지 않음」), 타입힌트 `str | Path`·`str | None = None`·`-> list[dict]`, 홀로 놓인 `*`(키워드 전용 인자), 한 셀에 마스크 확인과 함수 정의와 호출을 함께 둠, `orders.dtypes.astype(str).to_dict()` 연결 호출, `pd.DataFrame([...]).to_csv(...)` 한 문장
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기 셀이 없거나 출력 값을 인용하지 않음(설명 셀이 코드 앞에만 있음)
- G6: 영문·코드 이름+조사로 시작하는 문장 38개(「`pd.read_csv(경로)`는」, 「Series는」, 「DataFrame은」 등), 70자 초과 4개
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 Excalidraw 도식 1장(본문이 「초록 상자는 원본 주문 세 행」처럼 설명)
- 내용: 본문 「`Ch 2의 05절에서는 Path로 파일 경로를 만들고`」는 Ch 2 개선본과 다름(05절은 `with open()`, `Path`는 Ch 1에서만 씀). 「`to_numeric`은 변환할 수 없는 값이 있으면 예외를 발생시킵니다」는 노트북에서 실행하지 않은 동작. Before가 `astype({"amount": "string"})`로 일부러 망가뜨려 원인이 인위적

## 바꾼 것

- 노트북: 제목(할 일 3, API 키 불필요·호출 0번·1분 이내, **기준 pandas 버전** 3.0.5·Python 3.11 이상·pandas 2 이하 실행 안 함) → 오늘 볼 그림(01-1) → 준비(`mkdtemp(prefix="ch04-01-")`+`chdir`+`listdir` `[]`) → `import pandas as pd`(별명 `as` 한 문장, `pandas 버전: 3.0.5`) → `with open("orders.csv", "w")`로 CSV 글 저장(`['orders.csv']`) → `pd.read_csv()`와 인덱스 → `shape` `(3, 3)`·`dtypes`(`int64`·`str`, 마지막 줄 `dtype: object` 설명) → 열 꺼내기(시리즈) → `== "paid"` 마스크 → `orders.loc[paid_mask]`(인덱스 0·2 유지, 원래 표 3행) → `orders.loc[paid_mask, "amount"]`·`sum()` `59000` → `fetch_orders(file_name: str, status: str) -> list` 정의 셀 → 호출 셀(for+append로 `['O101', 'O103']`, assert) → 값 바꿔 보기 `"pending"`(`주문 수: 1`) → Before(`dtype=str`, 표는 같아 보이나 세 열 `str`, 합계 `320001800027000`·`<class 'str'>`) → After(`pd.to_numeric()` 뒤 `int64`·`77000`·assert, 「미정」이 섞인 목록을 `try/except ValueError`로 받아 `Unable to parse string "미정" at position 1`) → 정리
- 기존 학습 질문(상태와 금액을 안전하게 조회)·데이터(O101 paid 32000, O102 pending 18000, O103 paid 27000, 합계 77000·paid 59000)·paired 형식 유지. 02~05절과 `data/orders.csv`·`data_tools.py`가 같은 주문 번호·금액을 쓰므로 바꾸지 않음
- 가르치지 않은 문법 처리(Ch 3 요약 §4·§5): `Path`·`TemporaryDirectory`·목록 내포식·`str | …`·`*`·`list[dict]`는 기본 경로에서 제거. `import pandas as pd`는 이 절 학습 목표라 「키워드 `as`는 불러온 모듈에 짧은 별명을 붙입니다」로 풂. `-> list`는 「Ch 2 07절 `-> int`와 같은 타입힌트 모양」 한 문장. `__version__`은 Ch 2 07절 `__name__`에 연결. `raise`·f-string 안 식·`@`·`BaseModel`·`*args` 없음(A 트랙 제약 유지)
- Before 원인을 「주문 번호를 글자로 지키려고 모든 열을 글자로 읽음(`dtype=str`)」으로 바꿔 Ch 2 05절 「파일에서 읽은 줄은 글자」와 연결. 「변환할 수 없는 값은 오류」는 After 마지막 셀에서 실제로 실행(Ch 2 05·13절 「연필,많이」 ValueError와 연결)
- 본문 10블록 전체를 다시 씀. 「이 절의 질문」, 용어 7개 표, 비유(창을 낸 덮개), 「앞에서 배운 내용」 4단락(Ch 2 03·04·05·07, Ch 3 준비 셀), 주의 메모에 실행하지 않은 것(글자로 둘 열만 정하기, 금액에 글자가 섞인 파일, 없는 파일·상태, 다른 OS·pandas 2)과 Ch 3 01절 `git status --short` 확인 습관 연결. 복습 5문항
- 그림: Mermaid 4장(주문 표 읽기, 조건으로 행 고르기, 조회 함수, 글자 합계 Before/After) + 삽화 1장(창을 낸 덮개). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 라이브러리 동작 확인: `pd.to_numeric` 기본값 `errors='raise'`, `DataFrame.to_dict(orient=…)`를 설치본(pandas 3.0.5) 시그니처·설명으로 대조

## 그림 확인

- PNG 네 장을 직접 열어 확인. 01-1은 처음 LR 배치가 viewBox 폭 970이라 TB로 바꿈(744). 01-2는 LR 폭 1526이라 TB로 바꿈(236×666). 01-2 첫 판의 화살표 라벨 `#quot;`가 `&quot;` 글자로 보여 「paid와 같은가」로 고침. 01-4 첫 판은 「미정」 목록이 `pd.to_numeric()` 표 칸에서 갈라지는 것처럼 그려져, 실제 노트북(따로 만든 목록)과 맞게 둘째 줄로 분리
- 삽화 01-5: 1차 job `755be28c-…` 탈락(덮개가 밀려 주황 줄이 보이고 동전이 덮개 위에 놓임). 프롬프트를 세 구역으로 고쳐 2차 job `f412811a-9852-4a29-91de-484ddc6e19f8` 채택. 4크레딧(잔액 2920에서). 저장 PNG(1100px)를 채택 job 결과와 같은 폭으로 대조해 픽셀 차이 0

## 검토에서 볼 곳

- Before를 `dtype=str`(모든 열 글자)로 만든 설정이 학생에게 자연스러운지. 대안은 금액 칸에 글자가 섞인 파일이지만 After에서 값 정리가 더 필요해 목록 실험으로 나눔
- `print(orders.dtypes)`의 마지막 줄 `dtype: object`를 「목록 자체에 붙은 표시라 지금은 읽지 않음」으로 넘긴 설명
- 삽화 01-5의 동전 개수는 프롬프트(4·2·3)와 다름. 금액 크기가 아니라 「고른 줄의 동전을 합친다」만 읽으면 되어 채택

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 1, 하 1, 공통 C-1·C-2). 모두 반영했습니다.
- 01-1(중): 노트북 「오늘 볼 그림」을 01-1(`flowchart TB`)에 맞춰 「위에서 아래로 읽습니다. 초록 상자는 파일과 표의 열처럼 값이 담긴 자리이고, 화살표 옆 글자는 실행한 코드나 한 일입니다.」「가운데 칸의 회색 상자는 pandas가 붙인 행 번호(인덱스)입니다. 맨 아래 상자가 상태 열 하나를 꺼낸 시리즈입니다.」로 고침
- 01-2(Q1 권고: `dtype=str` 유지): 노트북 9번 설명과 본문 b6 첫 단락에 「앞자리 0이 있는 번호(예: `01234`)는 숫자로 읽히면 0이 사라지기 때문입니다. 이번 파일에는 그런 번호가 없어 실행하지 않았습니다.」
- C-1: 본문 b7에 실습 폴더 `data_tools.py`의 `fetch_orders(csv_path, *, status=None)` 항목(키워드 인자 `status=`, 별표 `*` 한 문장, 「Ch 19 01절이 도구로 다시 쓰는 것은 이 실습 폴더 판입니다」). `data_tools.py`는 고치지 않음
- C-2: 표·시리즈 출력 앞 라벨 줄 8개(`주문 표:`, `열마다의 자료형:` 2곳, `상태 열:`, `paid와 같은가:`, `결제 완료 주문 표:`, `결제 완료 금액:`, `글자로 읽은 표:`). 4번 결과 읽기 첫 문장을 「라벨 줄 아래 첫 줄은 열 이름 …」으로
- 코드 셀 16(변화 없음), 검사한 문장 339

재실행: 생성기 `author_01.py` 수정 → `run_section.sh … 01`(새 커널 PASS). 코드 셀 출력은 새 라벨 줄·임시 경로·포트를 빼고 반영 전과 같습니다. 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0, `qa/upgrade/gates-after.json`), `verify.py --chapter` `PASS 6 sections / 96 code cells (max 21 lines)`, `visual.cjs` 14건 PASS, 실습 폴더 pytest 10 passed. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(`review-round1.md` 끝 「반영 결과」의 볼 곳)가 남음
- 리뷰 묶음: `qa/upgrade/review-pack/01-Pandas로-표-다루기.md`
- 정리 대상(삭제하지 않고 목록만): `figures/01-dataframe-flow.excalidraw`·`.svg`(옛 도식, 본문에서 뺌)
- 작업 환경 메모: 기기 VM 루트 디스크가 가득 차(3.9MB) uv 실행이 실패해, 이 작업에서 방금 만든 uv 캐시 항목 5개(pandas·numpy·lxml·bs4·soupsieve, 113MB)를 `$HOME/ch04-01-hold/uv-archive-v0/`로 옮겼습니다(삭제 없음, 가상환경은 복사본이라 영향 없음). 루트 여유 약 115MB
