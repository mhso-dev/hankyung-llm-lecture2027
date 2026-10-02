from __future__ import annotations

import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEPTH = runpy.run_path(str(Path(__file__).with_name("part7_apply_depth.py")))["LESSONS"]


PREP = {
    "ch30": "이 준비 셀은 `Path.cwd().resolve()`로 현재 폴더를 절대 경로로 읽고, 현재 폴더와 부모 폴더에서 `agent_service`가 있는 첫 위치를 `next(..., None)`로 찾습니다. 찾지 못하면 `assert`가 실행을 중단합니다. 찾은 뒤 `os.chdir(lab)`이 이후 import와 파일 접근의 기준 폴더를 바꾸고, 마지막 출력은 실제 선택된 폴더 이름을 확인합니다.",
    "ch31-install": "앞의 `%pip install` 셀은 이 노트북을 실행하는 현재 커널에 Ch31에서 고정한 SQLAlchemy·PostgreSQL·pgvector·LangGraph 패키지를 설치합니다. 설치 명령의 출력은 숨기지만, 다음 셀의 import가 성공하려면 이 단계가 먼저 끝나야 합니다.",
    "ch31-env": "두 번째 준비 셀은 `CH31_DATABASE_URL`을 읽고 없으면 로컬 실습용 주소를 사용합니다. 같은 데이터베이스를 비동기 SQLAlchemy, psycopg, PostgreSQL 명령에서 사용할 수 있도록 드라이버 표기만 바꾼 세 URL을 만듭니다. 화면에는 데이터베이스 이름과 비밀값을 숨겼다는 사실만 출력합니다.",
    "ch32": "이 준비 셀은 현재 폴더와 부모 폴더에서 `Dockerfile.baseline`이 있는 Ch32 실습 폴더를 찾습니다. `run(*args, check=True)`은 모든 Docker 명령을 그 폴더에서 실행하고 표준 출력·오류와 종료 코드를 `CompletedProcess`로 반환합니다. 실패 자체를 관찰하는 셀만 `check=False`를 전달하며, 마지막에는 Docker Engine이 응답하는지 확인합니다.",
    "ch33": "첫 셀의 `Path` 탐색은 어느 상위 폴더에서 열어도 Ch33의 `pyproject.toml`을 기준으로 실습 폴더를 찾습니다. 뒤의 `subprocess.run(..., cwd=lab, capture_output=True)`은 명령을 별도 프로세스로 실행하고 화면 문구와 종료 코드를 함께 반환합니다. 이 보조 코드는 CI를 흉내 내는 공통 실행 경계이며, 각 절의 판정은 다음 셀에서 해당 명령의 실제 반환값을 읽어 결정합니다.",
    "ch34": "준비 셀은 현재 폴더와 부모 폴더에서 `ch34-cost-rate-limits` 실습 폴더를 찾고, 발견한 `.env`가 있으면 현재 프로세스에 불러옵니다. 키 값은 출력하지 않으며 준비 결과로 폴더와 환경 파일의 존재 여부만 확인합니다. 이후 파일 기록은 찾은 `chapter_root` 아래 `runs` 폴더를 사용합니다.",
    "ch34-local": "준비 셀은 비동기 큐, 난수 지터, 로컬 HTTP 서버, 시간 측정에 필요한 표준 라이브러리만 불러옵니다. 외부 제공자 API는 호출하지 않습니다. 다음 셀에서 운영체제가 배정한 로컬 포트에 교육용 429 서버를 시작하며, 절이 끝나면 서버를 종료합니다.",
}


TARGETS = {
    "ch30": (1, -1),
    "ch31": (2, -1),
    "ch32": (1, -1),
    "ch33": (1, -1),
    "ch34-cost-rate-limits/01-프롬프트-캐시-계측": (2, 3),
    "ch34-cost-rate-limits/02-Batch-API": (1, 3),
    "ch34-cost-rate-limits/03-모델-라우팅": (2, 5),
    "ch34-cost-rate-limits/04-백오프-큐-동시성": (2, 4),
    "ch34-cost-rate-limits/05-예산-가드와-p95": (1, 3),
}


def md(cell_id: str, heading: str, body: str, lesson_part: str | None = None) -> dict:
    metadata = {} if lesson_part is None else {"lesson_part": lesson_part}
    return {
        "BELONGS_TO": "part7-review-fix",
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": metadata,
        "source": [f"### {heading}\n", "\n", body],
    }


for path in sorted((ROOT / "labs/part7").glob("ch*/notebooks/[0-9][0-9]-*.ipynb")):
    chapter = path.parents[1].name
    lesson = path.stem
    key = f"{chapter}/{lesson}"
    first, second = DEPTH[key]
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = [
        cell for cell in notebook["cells"]
        if not cell.get("id", "").startswith(("depth-", "prep-", "concept-"))
    ]
    code_count = sum(cell["cell_type"] == "code" for cell in cells)
    if chapter.startswith("ch30"):
        prep_points = {0: PREP["ch30"]}
        first_at, second_at = TARGETS["ch30"]
    elif chapter.startswith("ch31"):
        prep_points = {0: PREP["ch31-install"], 1: PREP["ch31-env"]}
        first_at, second_at = TARGETS["ch31"]
        if lesson.startswith("05-"):
            prep_points[2] = ("세 번째 준비 셀은 Docker 컨테이너 이름과 PostgreSQL 명령을 실행할 "
                              "`subprocess.run` 보조 함수를 준비합니다. 명령의 표준 출력과 오류를 문자열로 "
                              "반환하며, 실패하면 다음 단계로 넘어가지 않습니다. 실제 벡터 표 생성은 그다음 셀에서 시작합니다.")
            first_at = 3
    elif chapter.startswith("ch32"):
        prep_points = {0: PREP["ch32"]}
        first_at, second_at = TARGETS["ch32"]
    elif chapter.startswith("ch33"):
        prep_points = {0: PREP["ch33"]}
        first_at, second_at = TARGETS["ch33"]
    else:
        prep_points = {0: PREP["ch34-local"] if lesson.startswith("04-") else PREP["ch34"]}
        first_at, second_at = TARGETS[key]
    if second_at < 0:
        second_at = code_count - 1

    rebuilt = []
    code_index = 0
    suffix = f"{chapter[2:4]}-{lesson[:2]}"
    for cell in cells:
        if cell["cell_type"] == "code":
            lesson_part = cell.get("metadata", {}).get("lesson_part")
            if code_index in prep_points:
                rebuilt.append(md(f"prep-{suffix}-{code_index}", "이 준비 셀이 하는 일", prep_points[code_index], lesson_part))
            if code_index == first_at:
                body = first
                if key == "ch30-fastapi-serving/02-의존성으로-Agent-주입":
                    body += ("\n\n완성된 `agent_service/app.py`에는 "
                             "`AgentDep = Annotated[object, Depends(get_agent)]`가 있고, "
                             "라우트는 `async def chat(body: ChatRequest, runtime: AgentDep, ...)`처럼 "
                             "이 타입을 매개변수에 선언합니다. 아래 셀은 이 선언을 새로 만드는 코드가 아니라 "
                             "그 선언이 가리키는 `get_agent` 제공자만 테스트 객체로 바꿉니다.")
                rebuilt.append(md(f"concept-{suffix}-a", "바로 다음 코드를 읽는 방법", body, lesson_part))
            if code_index == second_at:
                rebuilt.append(md(f"concept-{suffix}-b", "이 단계에서 구분할 범위", second, lesson_part))
            code_index += 1
        rebuilt.append(cell)
    notebook["cells"] = rebuilt
    for cell in notebook["cells"]:
        cell.pop("BELONGS_TO", None)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise RuntimeError(f"replacement target missing: {path}: {old[:80]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


book = ROOT / "textbook/part7"

replace(
    book / "ch30-fastapi-serving/_src/07-인증-CORS-타임아웃.html",
    "인증은 요청한 주체를 확인하고, CORS는 브라우저가 다른 출처의 응답을 읽어도 되는지 결정하며, timeout은 기다릴 최대 시간을 제한합니다. 세 기능은 모두 요청 경계에 있지만 서로 대신하지 않습니다. OPTIONS 사전 요청은 실제 POST 전에 허용 출처와 헤더를 확인하고, Authorization이 없으면 401을 반환합니다. <code>get_timeout</code>을 0.01초로 대체한 테스트는 느린 Agent가 단일 응답에서는 504, 스트림에서는 오류 사건으로 바뀌는 차이를 보여 줍니다.",
    "인증은 요청한 주체를 확인하고, CORS는 브라우저가 다른 출처의 응답을 읽어도 되는지 결정하며, timeout은 기다릴 최대 시간을 제한합니다. 세 기능은 모두 요청 경계에 있지만 서로 대신하지 않습니다. 먼저 CORSMiddleware가 OPTIONS 사전 요청의 출처와 요청 헤더를 검사해 허용된 경우 200을 반환합니다. 이어지는 실제 POST에서 애플리케이션의 인증 의존성이 Authorization 헤더를 검사하며, 헤더가 없으면 401을 반환합니다. <code>get_timeout</code>을 0.01초로 대체한 테스트는 느린 Agent가 단일 응답에서는 504, 스트림에서는 오류 사건으로 바뀌는 차이를 보여 줍니다.",
)
replace(
    book / "ch32-docker/_src/01-이미지와-레이어.html",
    "Dockerfile의 각 명령은 빌드 결과의 파일 시스템 변화를 층으로 쌓습니다. 이미지는 이 읽기 전용 층과 실행 설정을 담은 템플릿이고, 컨테이너는 이미지 위에 쓰기 가능한 층을 더한 실행 인스턴스입니다. <code>docker build</code>는 이미지를 만들고 <code>docker run</code>은 그 이미지에서 프로세스를 시작합니다. <code>docker history</code>의 항목은 명령과 크기를 보여 주지만 보안 검사를 대신하지 않습니다.",
    "Dockerfile의 명령은 모두 이미지 기록에 남지만 역할은 다릅니다. <code>RUN</code>, <code>COPY</code>, <code>ADD</code>처럼 파일을 바꾸는 명령은 파일 시스템 레이어를 만들고, <code>CMD</code>와 <code>HEALTHCHECK</code>는 실행 기본값과 상태 검사 같은 이미지 메타데이터를 기록해 0B로 보일 수 있습니다. 이미지는 읽기 전용 레이어와 실행 설정을 담은 템플릿이고, 컨테이너는 그 위에 쓰기 가능한 층을 더한 실행 인스턴스입니다. <code>docker build</code>는 이미지를 만들고 <code>docker run</code>은 그 이미지에서 프로세스를 시작합니다.",
)
replace(
    book / "ch32-docker/_src/05-환경변수-시크릿-헬스체크-로그.html",
    "liveness는 프로세스가 응답할 수 있는지, readiness는 현재 실제 트래픽을 받을 준비가 됐는지 확인합니다. 데이터베이스 주소를 틀린 컨테이너가 <code>/health</code> 200과 <code>/ready</code> 503을 함께 반환하는 이유입니다. 자동 재시작은 liveness에, 트래픽 제외는 readiness에 연결하고 로그에는 요청 식별자를 남기되 비밀값을 출력하지 않습니다.",
    "liveness는 프로세스가 응답할 수 있는지, readiness는 현재 실제 트래픽을 받을 준비가 됐는지 확인합니다. 데이터베이스 주소를 틀린 컨테이너가 <code>/health</code> 200과 <code>/ready</code> 503을 함께 반환하는 이유입니다. 이번 실습은 두 HTTP 상태와 Compose가 표시한 health 상태까지만 확인합니다. 자동 재시작과 트래픽 제외는 배포 오케스트레이터가 이 신호에 별도 정책을 연결할 때 동작하며, healthcheck 자체가 두 행동을 보장하지 않습니다. 로그에는 요청 식별자를 남기되 비밀값을 출력하지 않습니다.",
)
replace(
    book / "ch30-fastapi-serving/_src/09-실제-Agent-HTTP-통합.html",
    "<li>실제 API 호출에는 비용이 발생합니다. 이 절의 소규모 호출 예상 비용은 1달러 미만이며 키 값은 출력하지 않습니다.</li>",
    "<li>실제 API 호출 횟수와 사용량 메타데이터를 실행 기록에 남기며 키 값은 출력하지 않습니다. 이 절은 응답과 도구 궤적 확인이 목적이므로 비용을 임의로 추정하지 않습니다.</li>",
)


CH31 = {
    "01-SQLAlchemy-비동기-PostgreSQL": (
        ["비동기 Engine과 세션 팩터리의 역할을 설명할 수 있습니다.", "동시 작업마다 별도 AsyncSession을 만들어 조회할 수 있습니다.", "순차 실행과 동시 실행의 대기 시간 차이를 실제 출력으로 해석할 수 있습니다."],
        "노트북은 전용 스키마와 세 행을 만든 뒤 세션 하나의 조회 결과를 확인합니다. 이어 각 작업이 자기 세션을 열도록 구성하고, 0.15초 대기 조회 세 건을 순차 실행과 동시 실행으로 비교합니다.",
        "세 조회 결과가 같은지, 순차 시간과 동시 시간이 각각 얼마인지 확인합니다. 시간 차이는 독립된 대기와 세 개 연결이라는 실험 조건에서만 해석합니다.",
    ),
    "02-트랜잭션과-원자성": (
        ["커밋과 롤백이 결정되는 트랜잭션 블록의 경계를 설명할 수 있습니다.", "출금과 입금을 서로 다른 트랜잭션에 둔 실패 결과를 재현할 수 있습니다.", "두 변경을 한 트랜잭션에 묶어 모두 취소되는 결과를 확인할 수 있습니다."],
        "노트북은 잔액 합계 1000에서 시작합니다. Before는 출금을 먼저 확정한 뒤 장애를 내어 총액 900을 관찰하고, After는 출금과 입금을 같은 `engine.begin()` 블록에 두어 예외 때 두 변경이 모두 취소되는지 확인합니다.",
        "Before의 두 잔액과 총액 900, After의 두 잔액과 총액 1000을 비교합니다. 출력된 RuntimeError는 장애 위치를 표시하고, 실제 롤백 결과는 이후 SELECT로 확인합니다.",
    ),
    "03-Alembic-적용과-롤백": (
        ["Alembic 리비전 파일이 스키마 변경 순서를 기록하는 방법을 설명할 수 있습니다.", "`upgrade head`와 `downgrade base`로 표의 생성과 제거를 실행할 수 있습니다.", "카탈로그 조회로 적용·제거·재적용 상태를 확인할 수 있습니다."],
        "노트북은 Alembic 설정 폴더를 찾고 명령 실행 함수를 준비합니다. 빈 스키마에 `upgrade head`를 적용해 tickets 표를 확인하고, `downgrade base`로 제거한 뒤 다시 최신 리비전을 적용합니다.",
        "마이그레이션 폴더 이름, 적용 뒤 표 이름, 다운그레이드 뒤 `None`, 재적용 뒤 복구된 표 이름을 순서대로 확인합니다. 이 절은 실행 시간을 출력하지 않습니다.",
    ),
    "04-커넥션-풀-고갈과-대응": (
        ["연결 풀의 크기·초과 연결·대기 제한이 요청에 미치는 영향을 설명할 수 있습니다.", "유일한 연결을 오래 점유해 두 번째 요청의 TimeoutError를 재현할 수 있습니다.", "연결을 일찍 반환하고 대기 제한을 조정한 뒤 두 작업의 성공을 확인할 수 있습니다."],
        "노트북은 연결 하나와 짧은 `pool_timeout`을 둔 엔진에서 첫 작업이 연결을 점유하게 합니다. 두 번째 작업의 제한 시간 초과를 관찰한 뒤, 짧은 쿼리와 충분한 대기 시간을 사용해 두 작업을 완료합니다.",
        "Before의 `TimeoutError`와 풀 상태, After의 두 결과와 전체 소요 시간을 확인합니다. 성공은 연결을 빌리고 반환한 이 실험 조건을 뜻하며 운영 연결 수의 적정값을 정하지 않습니다.",
    ),
    "05-pgvector-체크포인터-공존과-백업": (
        ["벡터 표와 체크포인터 표가 같은 PostgreSQL에 있을 때 역할과 소유권을 구분할 수 있습니다.", "HNSW 인덱스 존재와 실제 EXPLAIN 계획의 사용 여부를 구분할 수 있습니다.", "논리 덤프를 복원한 데이터베이스에서 문서·체크포인트 행과 인덱스를 확인할 수 있습니다."],
        "노트북은 문서 세 건과 코사인 HNSW 인덱스를 만들고 대표 벡터 검색과 `EXPLAIN` 계획을 확인합니다. 이어 PostgresSaver 체크포인트를 저장하고, 전용 스키마의 논리 덤프를 별도 데이터베이스에 복원합니다.",
        "가장 가까운 문서, Seq Scan 실행 계획, 체크포인트 결과값, 복원 뒤 문서·체크포인트 행 수와 HNSW 인덱스 이름을 확인합니다. 그래프 스레드 재개 자체는 이 노트북의 실행 범위가 아닙니다.",
    ),
}

for slug, (goals, example, look) in CH31.items():
    path = book / "ch31-database/_src" / f"{slug}.html"
    text = path.read_text(encoding="utf-8")
    goals_html = "<h2 id=\"b1\"><span class=\"no\">1</span>학습 목표</h2><div class=\"goal\"><ul>" + "".join(f"<li>{g}</li>" for g in goals) + "</ul></div>"
    text = re.sub(r'<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>.*?</ul></div>', goals_html, text, count=1)
    text = re.sub(r'(<h2 id="b5"><span class="no">5</span>실행 예제</h2>)<p>.*?</p>(\{\{notebook:)', rf'\1<p>{example}</p>\2', text, count=1)
    text = re.sub(r'<p class="look"><b>확인할 점</b> — .*?</p>', f'<p class="look"><b>확인할 점</b> — {look}</p>', text, count=1)
    path.write_text(text, encoding="utf-8")


COMMON_PRIOR = "<p>Ch15의 <code>evaluation-cases.json</code>과 회귀 비교는 이전에 성공했던 답변 품질을 기준선으로 남기는 방법을 보여 주었습니다. Ch29의 에이전트 평가는 최종 답변뿐 아니라 도구 호출 수와 궤적도 확인해야 한다는 점을 다루었습니다. Ch32의 Docker 이미지는 실행 환경을 파일로 고정했습니다. 이 절에서는 그 결과를 자동 검사의 입력으로 사용하며, 원본 평가 자료를 다시 계산했다고 주장하지 않습니다. 공개 실습용 요약 자료의 출처 장과 필드 의미를 README에 기록합니다.</p>"
COMMON_METAPHOR = "<h3>변경을 통과시키는 검사대</h3><p>공항의 수하물은 접수, 보안 검사, 목적지 분류를 차례로 통과합니다. 한 단계가 실패하면 다음 운송 단계로 보내지 않습니다. CI/CD도 변경 하나를 테스트, 정적 검사, 빌드, 평가, 배포 검증의 순서로 처리합니다. 비유에서 검사대는 작업 단계에, 통과 표시는 종료 코드 0에 대응합니다.</p>"
COMMON_FIGURE = "왼쪽의 파란 상자는 입력과 검사를, 가운데의 초록 상자는 통과한 결과를, 오른쪽의 주황 상자는 중단 또는 운영 판단을 나타냅니다. 화살표는 실제 실행 순서입니다. 각 상자 아래의 작은 글자는 이 실습에서 확인하는 파일이나 출력입니다."
COMMON_AFTER_FIGURE = "<p>도식의 화살표를 따라가며 현재 단계가 무엇을 입력으로 받고 무엇을 남기는지 확인합니다. 검사 결과가 실패이면 다음 단계 화살표를 따라가지 않습니다. 운영 환경에서는 승인, 비밀 정보, 네트워크 상태 같은 조건이 더해질 수 있습니다.</p>"

CH33 = {
    "01-테스트-린트-빌드와-GitHub-Actions": {
        "goals": ["pytest·Ruff·wheel 빌드가 서로 다른 결함을 찾는 이유를 설명할 수 있습니다.", "별도 프로세스의 종료 코드로 단계의 성공과 실패를 판정할 수 있습니다.", "검증한 wheel을 다음 배포 단계가 사용하는 산출물로 구분할 수 있습니다."],
        "prior": "<p>Ch2에서 pytest와 패키징을, Ch3에서 PR 검토 흐름을, Ch32에서 Docker 이미지를 만들었습니다. 이 절은 이미 배운 검사를 사람이 기억해서 실행하는 대신, 같은 명령과 순서를 워크플로 파일에 기록하는 방법으로 연결합니다.</p>",
        "metaphor": "<h3>단계마다 다른 검사를 수행하는 생산선</h3><p>제품 생산선에서 치수 검사, 표면 검사, 포장 검사는 서로 다른 결함을 찾습니다. 코드도 pytest가 동작을, Ruff가 정적 규칙을, wheel 빌드가 배포 파일 생성을 확인합니다. 어느 단계든 종료 코드가 0이 아니면 다음 단계로 보내지 않습니다.</p>",
        "figure": "테스트 입력에서 pytest·Ruff·wheel 빌드를 차례로 지나 종료 코드로 진행 여부를 결정하는 순서입니다. 각 초록 상자는 앞 단계가 실제로 성공했을 때만 도달합니다.",
        "after": "<p>세 검사의 결과를 한 문구로 합치지 않고 단계별 종료 코드와 산출물 이름을 남깁니다. 어느 단계에서 멈췄는지 알아야 수정할 파일과 다시 실행할 범위를 정할 수 있습니다.</p>",
        "look": "pytest와 Ruff의 종료 코드 0, 생성된 wheel 한 개를 확인합니다. 임시 실패 테스트는 0이 아닌 코드를, 수정본은 0을 반환하는지 비교합니다.",
    },
    "02-평가-회귀를-CI에-연결하기": {
        "goals": ["승인된 평가 기준선과 현재 결과의 역할을 구분할 수 있습니다.", "Groundedness와 추가 도구 호출 수를 독립 기준으로 판정할 수 있습니다.", "허용 범위를 벗어난 결과를 0이 아닌 종료 코드로 CI에 전달할 수 있습니다."],
        "prior": "<p>Ch15에서 근거성 평가와 기준선을, Ch29에서 최종 답뿐 아니라 도구 호출 궤적을 확인했습니다. 앞 절에서 CI가 종료 코드로 다음 단계 진행 여부를 결정한다는 점을 배웠습니다. 이 절은 두 평가 기준을 그 종료 코드에 연결합니다.</p>",
        "metaphor": "<h3>승인한 견본과 새 결과 비교</h3><p>인쇄소는 새 인쇄물을 승인된 견본과 나란히 놓고 색과 위치를 각각 검사합니다. 평가 회귀도 승인된 기준선과 현재 결과를 비교하되, 답의 근거성과 도구 호출 효율을 한 점수로 섞지 않습니다.</p>",
        "figure": "기준선과 현재 결과가 두 비교기로 들어가 Groundedness와 추가 호출 수를 각각 판정한 뒤 하나의 종료 코드로 합쳐지는 흐름입니다.",
        "after": "<p>기준선 변경과 모델 변경이 동시에 일어나면 실패 원인을 구분하기 어렵습니다. 기준선은 별도 리뷰로 갱신하고, 같은 평가 입력에서 후보 변경만 비교합니다.</p>",
        "look": "정상 자료의 두 PASS와 종료 코드 0을 확인합니다. 임시 실패 자료에서는 두 FAIL과 0이 아닌 종료 코드가 함께 나오는지 비교합니다.",
    },
    "03-레지스트리-다이제스트와-클라우드-배포": {
        "goals": ["이동 가능한 이미지 태그와 로컬 이미지 ID의 차이를 설명할 수 있습니다.", "두 리비전 빌드가 서로 다른 로컬 이미지 ID를 만드는지 확인할 수 있습니다.", "레지스트리 manifest digest와 클라우드 배포가 이 실습의 미실행 범위임을 구분할 수 있습니다."],
        "prior": "<p>Ch32에서 Dockerfile로 이미지를 만들었고 앞 절에서 검사를 통과한 변경만 다음 단계로 보냈습니다. 이 절은 그 결과물을 어떤 식별자로 기록해야 이전 배포를 다시 선택할 수 있는지 다룹니다.</p>",
        "metaphor": "<h3>진열 이름과 창고 물품 번호</h3><p>매장의 ‘신상품’ 표시는 다른 상품으로 옮겨 갈 수 있지만 창고 물품 번호는 특정 재고를 가리킵니다. Docker 태그는 이동 가능한 이름이고, 이 실습에서 확인하는 로컬 이미지 ID는 현재 Docker 데몬의 특정 이미지 구성을 식별합니다.</p>",
        "figure": "같은 태그 설명 아래 v1·v2를 빌드하고 서로 다른 로컬 이미지 ID를 얻어 교육용 배포 기록에 저장하는 범위입니다. 레지스트리 push 단계는 도식의 미실행 경계로 읽습니다.",
        "after": "<p>레지스트리에 push하면 manifest digest가 별도로 생기며 다중 플랫폼 목록에서는 적용 단위가 다시 달라질 수 있습니다. 이번 JSON의 `digest` 필드명은 교육용이지만 실제로 담긴 값은 로컬 이미지 ID입니다.</p>",
        "look": "v1과 v2의 로컬 이미지 ID가 다른지, 교육용 배포 JSON이 v1의 로컬 ID를 저장했는지 확인합니다. 레지스트리 manifest digest는 출력되지 않습니다.",
    },
    "04-모니터링과-알림": {
        "goals": ["오류율과 p95 지연을 각 시간 구간에서 계산할 수 있습니다.", "한 번의 초과와 두 구간 연속된 이상 상태를 구분할 수 있습니다.", "지속 조건을 만족한 경보를 종료 코드로 후속 검증에 전달할 수 있습니다."],
        "prior": "<p>Ch29에서 운영 지표를 정의했고 Ch34에서 p95 계산을 더 자세히 다룹니다. 앞 절의 배포 식별자는 어떤 변경 뒤 지표가 달라졌는지 연결하는 기준이 됩니다. 이 절은 네 구간의 고정 자료로 지속 조건을 먼저 학습합니다.</p>",
        "metaphor": "<h3>한 번의 체온과 이어지는 발열</h3><p>체온이 한 번 높게 측정된 경우와 여러 번 이어진 발열은 대응 기준이 다릅니다. 운영 경보도 한 구간의 임계값 초과와 일정 시간 계속된 이상을 구분해 순간 변동으로 인한 호출을 줄입니다.</p>",
        "figure": "1분부터 4분까지 오류율과 p95를 함께 비교합니다. 두 조건이 동시에 참인 구간이 3분과 4분에 이어질 때만 FIRING으로 이동합니다.",
        "after": "<p>경보는 원인을 확정하지 않습니다. 지속 조건이 충족됐다는 사실을 조사 시작 신호로 보내며, 실제 원인은 로그·트레이스·최근 배포 기록과 함께 확인합니다.</p>",
        "look": "각 분의 오류율·p95·조건 결과를 읽고 3·4분만 동시에 참인지 확인합니다. 검사 프로세스의 FIRING과 종료 코드 1은 이 지속 조건의 결과입니다.",
    },
    "05-롤백과-복구-검증": {
        "goals": ["배포 이력에서 이전 리비전과 식별자를 선택할 수 있습니다.", "실패 신호 뒤 롤백 사건을 새 기록으로 추가할 수 있습니다.", "활성 식별자와 실제 HTTP 응답으로 복구 결과를 확인할 수 있습니다."],
        "prior": "<p>앞 절에서 두 구간 연속 이상을 FIRING으로 판정했고 03절에서 배포 결과를 로컬 이미지 ID로 기록했습니다. 이 절은 그 신호와 기록을 연결해 이전 결과물을 선택하고, 선택 뒤 서비스 응답을 다시 확인합니다.</p>",
        "metaphor": "<h3>이전 조리법으로 되돌린 뒤 다시 맛보기</h3><p>새 조리법의 결과가 나쁘면 기록에서 이전 조리법을 선택할 수 있습니다. 그러나 종이의 번호만 바꿔서는 음식이 회복됐는지 알 수 없습니다. 롤백도 이전 배포를 활성화한 뒤 실제 요청을 보내 복구를 확인해야 합니다.</p>",
        "figure": "v2의 경보와 HTTP 503에서 이전 v1 식별자를 선택하고, 새 롤백 사건을 남긴 뒤 HTTP 200을 확인하는 순서입니다. 기존 실패 기록은 삭제하지 않습니다.",
        "after": "<p>활성 식별자 확인은 제어 상태를, HTTP 응답은 실행 상태를 보여 줍니다. 두 결과를 함께 확인해야 기록만 바뀌었거나 프로세스만 우연히 살아 있는 경우를 구분할 수 있습니다.</p>",
        "look": "v1·v2 배포 기록, 경보 종료 코드 1, 새 롤백 사건과 활성 v1 식별자를 순서대로 확인합니다. 마지막 HTTP 검사가 복구된 응답을 반환하는지도 확인합니다.",
    },
}

for slug, data in CH33.items():
    path = book / "ch33-cicd/_src" / f"{slug}.html"
    text = path.read_text(encoding="utf-8")
    goals_html = "<h2 id=\"b1\"><span class=\"no\">1</span>학습 목표</h2><div class=\"goal\"><ul>" + "".join(f"<li>{g}</li>" for g in data["goals"]) + "</ul></div>"
    text = re.sub(r'<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>.*?</ul></div>', goals_html, text, count=1, flags=re.S)
    text = text.replace(COMMON_PRIOR, data["prior"], 1)
    text = text.replace(COMMON_METAPHOR, data["metaphor"], 1)
    text = text.replace(COMMON_FIGURE, data["figure"], 1)
    text = text.replace(COMMON_AFTER_FIGURE, data["after"], 1)
    text = re.sub(r'<p class="look"><b>확인할 점</b> — .*?</p>', f'<p class="look"><b>확인할 점</b> — {data["look"]}</p>', text, count=1)
    path.write_text(text, encoding="utf-8")


path = book / "ch33-cicd/_src/03-레지스트리-다이제스트와-클라우드-배포.html"
text = path.read_text(encoding="utf-8")
text = text.replace(
    "<p>이미지 레지스트리(image registry)는 컨테이너 이미지를 저장하고 배포 환경에 전달하는 서비스입니다. 태그(tag)는 `v1`이나 `latest`처럼 사람이 읽기 좋은 이름이지만 같은 태그가 새 이미지로 이동할 수 있습니다. 다이제스트(digest)는 이미지 내용에서 계산한 식별자이므로 `sha256:...` 형식으로 정확한 내용을 가리킵니다. 클라우드 배포에서는 CI가 이미지를 빌드하고 레지스트리에 push한 뒤, 배포 시스템이 승인된 다이제스트를 pull하도록 구성할 수 있습니다. 이 연결에는 레지스트리 인증과 클라우드 권한이 필요하므로 실습에서는 로컬 파일의 SHA-256과 JSON 배포 이력으로 경계를 확인합니다.</p>",
    "<p>이미지 레지스트리(image registry)는 컨테이너 이미지를 저장하고 배포 환경에 전달하는 서비스입니다. 태그(tag)는 <code>v1</code>이나 <code>latest</code>처럼 사람이 읽기 좋은 이름이며 새 이미지로 이동할 수 있습니다. 로컬 이미지 ID는 현재 Docker 데몬이 빌드한 이미지 구성을 식별합니다. 레지스트리 manifest digest는 push된 매니페스트의 내용을 식별하며, 다중 플랫폼 이미지에서는 목록과 플랫폼별 매니페스트의 적용 단위도 구분해야 합니다. 이 실습은 로컬 이미지 ID와 JSON 이력까지만 확인하고 레지스트리 digest는 생성하지 않습니다.</p>",
    1,
)
text = text.replace(
    "<p>이미지 태그는 사람이 읽기 좋은 이동 가능한 이름이고, 다이제스트는 이미지 내용으로 결정되는 식별자입니다. 같은 <code>latest</code>라는 태그도 시간이 지나면 다른 이미지를 가리킬 수 있지만 <code>sha256:...</code> 다이제스트는 특정 바이트를 가리킵니다. 실습은 v1과 v2 이미지를 빌드해 서로 다른 식별자를 확인하고 배포 기록에 v1 다이제스트를 저장합니다.</p>",
    "<p>이미지 태그는 이동 가능한 이름입니다. 노트북의 <code>docker image inspect ... {{.Id}}</code>는 레지스트리 digest가 아니라 로컬 이미지 ID를 반환합니다. 실습은 v1과 v2 이미지의 로컬 ID가 다른지 확인하고, 교육용 JSON의 <code>digest</code> 필드에 v1의 로컬 ID를 저장합니다. 필드 이름만 보고 레지스트리 매니페스트를 검증했다고 해석하지 않습니다.</p>",
    1,
)
text = text.replace("v1과 v2는 같은 태그 이름을 사용할 수 있지만 계산된 다이제스트는 서로 달랐습니다.", "v1과 v2는 같은 태그 이름을 사용할 수 있지만 로컬 Docker가 반환한 이미지 ID는 서로 달랐습니다.", 1)
text = text.replace("다이제스트를 저장하면 롤백 때 이전 내용 식별자를 다시 선택할 수 있습니다.", "이 실습은 로컬 이미지 ID를 저장해 롤백에서 이전 로컬 결과를 다시 선택합니다.", 1)
path.write_text(text, encoding="utf-8")

print("localized 29 notebooks and corrected P7-01 through P7-09 source issues")
