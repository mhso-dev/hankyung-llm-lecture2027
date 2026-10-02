# 03-Alembic-적용과-롤백

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 2h | 코드 notebooks/03-Alembic-적용과-롤백.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>실습 폴더의 판 파일을 임시 폴더에 복사하고, 환경 변수로 접속 글을 넘겨 Alembic으로 첫 판을 올릴 수 있습니다.</li>
<li>줄이 든 표에 기본값 없는 NOT NULL 칸을 더하는 판이 막힌 뒤, 판 번호와 칸이 그대로인 것을 확인할 수 있습니다.</li>
<li>서버 기본값을 준 판으로 고쳐 올리고, 판을 내렸다 다시 올리면 없어지는 값을 출력으로 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>서비스를 고쳐 나가다 보면, 이미 줄이 든 표에 칸을 더해야 할 때가 옵니다. 예를 들어 상담 질문 표에 담당자 칸을 더하는 일입니다. 노트북 셀에서 SQL 글로 표를 고치면, 다른 컴퓨터의 데이터베이스는 그 바뀜을 모릅니다. 바뀜을 차례가 있는 파일로 적어 두면, 어느 데이터베이스에서나 같은 차례로 적용할 수 있습니다.</p><p>절 제목의 Alembic은 SQLAlchemy 위에서 표의 모양 바꾸기를 파일로 관리하는 도구입니다. 제목의 롤백은 이 절에서 판 내리기를 뜻합니다. <a href="02-트랜잭션과-원자성.html">02절</a>의 취소(롤백)는 한 묶음 작업 안의 변경을 없던 일로 하는 것이라, 뜻이 다릅니다. 이 절은 판 올리기가 막히는 장면과 판 내리기를 함께 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="01-SQLAlchemy-비동기-PostgreSQL.html">01절</a>에서는 설정 셀에서 접속 글을 정하고, 엔진과 블록 <code>engine.begin()</code>으로 이름 공간과 표를 만들었습니다. <a href="02-트랜잭션과-원자성.html">02절</a>에서는 블록 하나가 한 묶음 작업이고, 오류가 나면 블록 안의 변경이 모두 취소되는 것을 봤습니다. 받은 오류 <code>IntegrityError</code>와 오류 코드 SQLSTATE도 02절에서 읽었습니다. 이 절의 엔진은 <code>await</code> 없이 쓰는 동기 엔진이지만, 블록과 오류를 읽는 방법은 같습니다.</p><p><a href="../../part6/ch23-persistence/02-PostgresSaver-준비와-스키마.html">Ch 23 02절</a>에서는 체크포인터가 메서드 <code>setup()</code>으로 제 표를 만들었습니다. 어디까지 실행했는지는 표 만들기 기록에 판 번호로 적었습니다. 이 절의 판 기록 표 <code>alembic_version</code>도 같은 생각입니다. 다만 이 절은 표를 만들고 고치는 판 파일을 우리가 직접 씁니다.</p><p><a href="../../part6/ch21-create-agent/04-0x에서-1x로-마이그레이션.html">Ch 21 04절</a>의 옮기기(마이그레이션)는 옛 버전 라이브러리에 맞춘 코드를 새 버전에서 돌게 고치는 일이었습니다. 영어 이름만 같고, 이 절의 표 구조 바꾸기와는 뜻이 다릅니다. 파일 위치 셀은 <a href="../ch30-fastapi-serving/01-비동기-라우팅과-스키마.html">Ch 30 01절</a>의 셀에서 후보 이름과 찾을 파일만 바꿨고, 환경 변수는 <a href="../../part6/ch28-mcp/03-stdio와-원격-전송-권한-경계.html">Ch 28 03절</a>에서 본 말입니다. NOT NULL 제약은 <a href="../../part1/ch04-data-tools/03-SQL로-조회-함수-만들기.html">Ch 4 03절</a>의 제약과 같은 갈래입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>옛 전화 교환대의 판 하나를 떠올려 봅니다. 판에는 꽂는 자리가 가로 세 줄, 세로 두 줄로 놓여 있고, 자리마다 주황 꽂이가 꽂혀 있습니다. 가로 한 줄이 표의 줄 하나이고, 세로 한 줄이 칸 하나입니다. 이 교환대에는 모든 자리에 무언가가 꽂혀 있어야 한다는 규칙이 있다고 해 봅니다.</p><p>세로 한 줄을 더하려고 빈 자리 셋짜리 새 판을 가져왔습니다. 빈 자리는 규칙에 맞지 않아, 새 판은 붙지 못하고 앞에 놓인 채 남습니다. 옛 판은 세로 두 줄 그대로입니다. 새 판의 자리마다 회색 마개를 먼저 꽂아 오면 규칙에 맞아, 세로 세 줄짜리 판이 됩니다.</p><p>새 판을 덧대는 일이 판 올리기이고, 빈 자리를 허용하지 않는 규칙이 NOT NULL 제약입니다. 회색 마개는 서버 기본값입니다. 비유와 다른 점도 있습니다. 실제로는 붙지 못하고 남는 판이 없습니다. 막힌 SQL 문장은 칸을 만들지 않았고, 도구는 판 번호도 적지 않았습니다.</p>
{{img:03-6-빈-자리-판과-마개를-꽂은-판|흰 바탕에 옅은 회색 탁자가 있고, 그 위에 크림색 교환대 판 둘이 나란히 서 있습니다. 왼쪽 판은 세로 두 줄이고, 줄마다 꽂는 자리 셋에 주황 꽂이가 모두 꽂혀 주황 꽂이가 여섯입니다. 왼쪽 판 앞 탁자 위에는 빈 구멍 셋이 뚫린 가늘고 긴 크림색 판 하나가 어디에도 붙지 않은 채 누워 있습니다. 오른쪽 판은 세로 세 줄이고, 앞의 두 줄에는 주황 꽂이 여섯이, 셋째 줄에는 같은 모양의 회색 둥근 마개 셋이 꽂혀 있습니다. 선·불·사람·손·글자·숫자·화살표는 없는 그림|빈 자리 셋짜리 새 판은 붙지 못하고 탁자에 남았고, 회색 마개 셋을 꽂은 판은 세로 세 줄짜리 판이 되었습니다.}}
<p class="look"><b>그림 읽기</b> — 왼쪽 크림색 판은 세로 두 줄에 주황 꽂이 여섯이 꽂혀 있습니다. 그 앞 탁자에는 빈 구멍 셋이 뚫린 가는 판 하나가 붙지 못한 채 누워 있습니다. 오른쪽 판은 세로 세 줄이고, 셋째 줄의 세 자리에는 회색 마개가 꽂혀 있습니다. 왼쪽이 기본값 없는 새 칸을 붙이지 못한 Before 판, 오른쪽이 서버 기본값으로 새 칸을 채운 After 판의 모습입니다.</p>
<h3>표 구조 바꾸기와 판</h3><p>도구 Alembic은 표 구조 바꾸기 한 번을 판 파일 하나로 적습니다. 판 파일에는 이 판의 번호 <code>revision</code>과 바로 앞 판의 번호 <code>down_revision</code>, 함수 <code>upgrade</code>와 <code>downgrade</code>가 들어 있습니다. 판 파일들은 앞 판 번호로 한 줄로 이어지고, 이 줄을 판 사슬이라고 부릅니다. 이 절에서 「판」은 표 구조의 판만 가리키고, 패키지와 서버는 「버전」이라고 적습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>표 구조 바꾸기(마이그레이션, migration)</td><td>데이터베이스 표에 칸을 더하거나 빼는 것처럼, 표의 모양을 바꾸는 일입니다. 학급 출석부에 연락처 칸을 새로 그어 넣는 일과 같습니다. 이 절에서는 표 <code>tickets</code>에 담당자 칸 <code>owner</code>를 더합니다.</td></tr><tr><td>판(리비전, revision)</td><td>표 구조 바꾸기 한 번을 적은 파일 하나와, 그 파일에 붙인 판 번호입니다. 책의 개정판이 앞 판에서 바뀐 것을 적어 두는 것과 같습니다. 이 절의 판은 <code>20260911_01</code>과 <code>20260929_02</code> 둘이고, 둘째 판 파일에는 앞 판 번호가 <code>down_revision</code>으로 적혀 있습니다.</td></tr><tr><td>판 올리기(upgrade)와 판 내리기(downgrade)</td><td>판 파일의 함수 <code>upgrade</code>를 불러 다음 판으로 가는 일과, 함수 <code>downgrade</code>를 불러 앞 판으로 가는 일입니다. 계단을 한 칸씩 오르내리는 것과 같습니다. 이 절에서는 <code>command.upgrade(alembic_cfg, "head")</code>와 <code>command.downgrade(alembic_cfg, "-1")</code>로 부릅니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 첫 판 <code>20260911_01</code>은 실습 폴더에 있던 판 파일이고, 표 <code>tickets</code>를 만듭니다. 둘째 판 <code>20260929_02</code>는 노트북이 사본에 쓴 판 파일이고, 칸 <code>owner</code>를 더합니다. 데이터베이스가 지금 어느 판인지는 판 기록 표 <code>alembic_version</code>에 한 줄로 적힙니다.</p>
{{mermaid:03-1-판-사슬과-판-기록-표|위에서 아래로 읽는 흐름도입니다. 맨 위 회색 상자 빈 자리 판 없음에서 판 올리기 화살표가 회색 상자 첫 판 20260911_01 실습 폴더 판 파일 표 tickets 만들기로 갑니다. 다시 판 올리기 화살표가 파란 상자 둘째 판 20260929_02 노트북이 사본에 쓴 판 파일 칸 owner 더하기로 이어지고, 둘째 판에서 첫 판으로 판 내리기 점선 화살표가 있습니다. 맨 아래 노란 상자는 판 기록 표 alembic_version이고, 첫 판 뒤 20260911_01과 After 뒤 20260929_02가 적힌 그림|판 파일은 앞 판 번호를 적어 한 줄로 이어지고, 판 기록 표에는 지금 판 번호 하나가 적힙니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 회색 상자 둘은 빈 자리와 실습 폴더에 있던 첫 판이고, 파란 상자는 이 노트북이 사본에 쓰는 둘째 판입니다. 실선 화살표는 판 올리기, 점선 화살표는 판 내리기입니다. 노란 상자는 판 기록 표에 적힌 판 번호로, 노트북 5절과 7절 출력입니다.</p>
<h3>판 올리기도 한 묶음 작업 안에서</h3><p>PostgreSQL에서는 표를 만들고 칸을 더하는 SQL 문장도 한 묶음 작업 안에서 돕니다. 도구 Alembic은 이런 서버를 만나면 판 올리기를 한 묶음 작업으로 감쌉니다. 판을 올릴 때 찍히는 진행 기록 <code>Will assume transactional DDL.</code>이 그 뜻입니다. 문서대로라면 판 파일에 SQL 문장이 여럿일 때, 한 문장이 막히면 앞 문장도 02절처럼 함께 취소됩니다. 이 절의 판은 문장이 하나라, 그 모습은 이번에 실행하지 않았습니다.</p><p>줄이 든 표에 칸을 더하면, 이미 있는 줄의 새 칸에는 기본값이 들어갑니다. PostgreSQL 문서는 기본값을 적지 않으면 빈 값(<code>NULL</code>)이 쓰인다고 적습니다. 새 칸에 NOT NULL 제약이 있으면, 그 빈 값 때문에 서버가 SQL 문장을 막습니다. 서버 기본값을 적으면 이미 있는 줄에 그 값이 들어가, 제약을 지킵니다.</p><h3>이 절의 판 내리기와 02절의 취소</h3><p>판 내리기는 판 파일의 함수 <code>downgrade</code>를 불러, 이미 확정한 표 구조를 앞 판의 모양으로 바꾸는 일입니다. <a href="02-트랜잭션과-원자성.html">02절</a>의 취소는 블록이 오류로 끝날 때, 블록 안의 변경을 확정하지 않는 일이었습니다. 둘 다 영어로 rollback이라 부를 때가 있지만, 이 교재에서는 말을 나눠 씁니다. 판 내리기가 칸을 빼면, 그 칸에 적었던 값도 함께 없어집니다.</p><h3>접속 글은 env.py가 정한다</h3><p>도구 Alembic은 설정 파일 <code>alembic.ini</code>를 읽은 뒤, 판 파일 폴더의 <code>env.py</code>를 실행해 서버에 붙습니다. 이 실습 폴더의 <code>env.py</code>는 환경 변수 <code>CH31_SYNC_URL</code>을 읽고, 없으면 <code>localhost</code>가 든 기본 글을 씁니다. 그래서 설정 객체에 접속 글을 적어도 쓰이지 않습니다. 이 절은 <code>env.py</code>를 고치지 않고, 환경 변수에 01절과 드라이버 이름만 다른 접속 글을 넣습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 01절과 드라이버 이름만 다른 접속 글을 정하고, 실습 폴더를 찾습니다. 3절은 파일 <code>env.py</code>가 읽는 환경 변수에 접속 글을 넣습니다. 4절은 <code>alembic.ini</code>와 <code>migrations/</code>를 임시 폴더에 복사하고, 사본으로 설정 객체를 만듭니다. 5절은 첫 판을 올리고, 표에 상담 질문 세 줄을 넣습니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 데이터베이스 서버는 01절과 같은 Docker 컨테이너 <code>kdt-ch31-postgres</code>입니다. 실습 폴더의 파일은 고치지 않고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:03-Alembic-적용과-롤백|example}}
<p class="look"><b>확인할 점</b> — 노트북 3절에서 <code>env.py</code>의 <code>os.getenv("CH31_SYNC_URL", …)</code> 줄을 찾습니다. 4절의 <code>사본의 판 파일: ['20260911_01_create_tickets.py']</code>와 <code>판 파일 폴더가 사본 안인가: True</code>를 봅니다. 5절에서 <code>판 번호: 20260911_01</code>과 <code>넣은 줄 수: 3</code>을 확인합니다.</p>
{{mermaid:03-2-사본으로-첫-판-올리기|위에서 아래로 읽는 흐름도입니다. 맨 위 회색 상자 실습 폴더 alembic.ini와 migrations에서 파란 상자 임시 폴더 사본, 폴더 이름 ch31-03-, 판 파일 하나로 갑니다. 그 오른쪽 초록 상자 환경 변수 CH31_SYNC_URL, postgresql+psycopg 접속 글과 사본 상자가 함께 회색 상자 사본의 env.py 12~15행, 환경 변수로 접속 글을 정함으로 이어집니다. 이어서 파란 상자 try_upgrade, command.upgrade 목표 head를 지나 마지막 노란 상자 판 번호 20260911_01, 칸 id와 question으로 가는 그림|실습 폴더를 사본으로 복사하고 환경 변수로 접속 글을 넘기자, 첫 판 20260911_01이 표 tickets를 만들었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 회색 상자 둘은 실습 폴더와, 사본에 든 파일 env.py입니다. 파란 상자 둘은 노트북이 한 일이고, 초록 상자는 3절에서 환경 변수에 넣은 접속 글입니다. 사본의 env.py가 이 값으로 서버에 붙고, 노란 상자는 노트북 5절 출력입니다.</p>
<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2><p>아래 Before 셀은 줄 셋이 든 표 <code>tickets</code>에 담당자 칸 <code>owner</code>를 더하는 둘째 판을 올립니다. 새 칸은 NOT NULL이고, 기본값은 적지 않았습니다. After 셀은 같은 판 파일에 서버 기본값 한 곳만 더해 다시 올립니다. 그 뒤 판을 내렸다가 다시 올리고, 값 하나를 바꿔 봅니다.</p>
{{notebook:03-Alembic-적용과-롤백|failure}}
{{mermaid:03-3-기본값-없는-NOT-NULL-칸의-Before|위에서 아래로 여섯 상자가 한 줄로 이어진 흐름도입니다. 회색 상자 판 20260911_01, 줄 셋 환불 배송 결제에서 파란 상자 Before 판 20260929_02, 칸 owner nullable=False, 기본값 없음으로 갑니다. 이어서 회색 상자 Alembic이 보낸 SQL 글 ALTER TABLE ADD COLUMN owner VARCHAR(50) NOT NULL, 회색 상자 서버가 SQL 문장을 막음 판 함수가 끝나지 않아 판 번호를 적지 않음, 노란 상자 받은 오류 IntegrityError NotNullViolation 23502, 마지막 빨간 상자 판 번호 20260911_01 그대로, 칸 id와 question 그대로로 이어지는 그림|기본값 없는 NOT NULL 칸을 더하는 SQL 문장이 막히자, 칸이 생기지 않고 판 번호도 적히지 않아 그대로 남았습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 회색 상자는 Before 판을 올리기 전의 판과 줄이고, 파란 상자는 노트북이 사본에 쓴 Before 판 파일입니다. 가운데 회색 상자 둘은 Alembic이 만든 SQL 글과, 서버가 그 문장을 막아 판 번호까지 가지 못한 일입니다. 판 번호를 판 함수가 끝난 뒤에 적는다는 것은 설치판 소스(10블록)에서 확인했습니다. 노란 상자는 노트북 6절에서 받아 출력한 오류이고, 빨간 상자는 그 뒤에 남은 판 번호와 칸입니다.</p>
{{mermaid:03-4-기본값-없는-판과-서버-기본값-판-견주기|위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자 두 판 같음, 판 20260911_01에서 시작, 줄 셋이 든 표, 둘째 판 20260929_02 칸 owner 더하기에서 두 칸으로 화살표가 갑니다. 왼쪽 칸 Before 기본값 없음에는 파란 상자 nullable=False만, 노란 상자 받은 오류 IntegrityError 23502, 빨간 상자 판 번호 20260911_01 칸 id와 question이 차례로 있습니다. 오른쪽 칸 After 서버 기본값에는 파란 상자 nullable=False server_default=미정 아래 노란 상자 받은 오류 None, 판 번호 20260929_02, 세 줄 owner 미정이 있는 그림|같은 표에 같은 둘째 판을 올렸는데, 기본값 없는 Before는 첫 판에 머물고 서버 기본값을 준 After는 둘째 판까지 올라갔습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 회색 상자는 두 판에서 같았던 시작 판·줄 셋·둘째 판 번호입니다. 왼쪽 Before 칸과 오른쪽 After 칸의 파란 상자가 두 판 파일에서 다른 한 곳입니다. 왼쪽 노란 상자는 Before에서 받은 오류이고, 빨간 상자는 Before 판의 결함 결과입니다. 오른쪽 노란 상자는 After 판의 결과이고, 두 칸의 값은 노트북 6절과 7절 출력입니다.</p>
<table><thead><tr><th>견준 것</th><th>Before(기본값 없음)</th><th>After(서버 기본값)</th></tr></thead><tbody><tr><td>판 파일의 칸 <code>owner</code></td><td><code>nullable=False</code>만</td><td><code>nullable=False</code>와 <code>server_default="미정"</code></td></tr><tr><td>받은 오류</td><td><code>IntegrityError</code> · <code>23502</code></td><td><code>None</code></td></tr><tr><td>판 올리기 뒤 판 번호</td><td><code>20260911_01</code></td><td><code>20260929_02</code></td></tr><tr><td>판 올리기 뒤 칸</td><td><code>['id', 'question']</code></td><td><code>['id', 'question', 'owner']</code></td></tr><tr><td>세 줄의 새 칸</td><td>칸이 없음</td><td>모두 <code>'미정'</code></td></tr></tbody></table>
<p>두 판 파일은 서버 기본값 한 곳만 달랐습니다. Before 판은 오류 코드 <code>23502</code>로 막혔고, After 판은 오류 없이 <code>20260929_02</code>까지 올라갔습니다.</p><p>Before 판에서 도구 Alembic은 <code>ALTER TABLE ch31_migration.tickets ADD COLUMN owner VARCHAR(50) NOT NULL</code>을 서버에 보냈습니다. 이미 있는 세 줄의 새 칸에는 빈 값이 들어가야 했고, NOT NULL 제약이 그 빈 값을 막았습니다. 막힌 문장은 칸을 만들지 않았고, 판 함수가 끝나지 못해 도구는 판 번호를 적지 않았습니다. 그래서 판 번호는 <code>20260911_01</code>, 칸은 <code>['id', 'question']</code> 그대로였습니다. 판 사슬에는 둘째 판이 있는데 데이터베이스는 첫 판에 머문 것이 이 절의 Before 결함입니다.</p><p>After 판은 세 줄의 새 칸을 <code>'미정'</code>으로 채워, 제약을 지키며 칸을 더했습니다. 판 번호가 아직 첫 판이었으므로, 같은 판 번호의 파일을 고쳐 다시 올릴 수 있었습니다.</p><p>판을 하나 내리자 칸 <code>owner</code>가 빠지고 판 번호는 <code>20260911_01</code>이 되었습니다. 줄 셋은 남았지만, 1번 줄에 적었던 <code>'민지'</code>는 칸과 함께 없어졌습니다. 다시 올리자 칸은 다시 생겼지만 1번 줄의 담당자는 서버 기본값 <code>'미정'</code>이었습니다.</p>
{{mermaid:03-5-판-내리기와-다시-올리기|위에서 아래로 다섯 상자가 한 줄로 이어진 흐름도입니다. 노란 상자 판 20260929_02, owner 민지 미정 미정에서 파란 상자 command.downgrade 목표 -1, 칸 owner 빼기로, 다시 노란 상자 판 20260911_01, 칸 id question, 줄 셋으로 갑니다. 이어서 파란 상자 try_upgrade 같은 판 파일로 다시 올리기, 마지막 노란 상자 판 20260929_02, owner 미정 미정 미정으로 이어지는 그림|판을 내리자 칸 owner가 값과 함께 빠졌고, 다시 올리자 1번 줄의 담당자는 민지가 아니라 미정이었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 노란 상자 셋은 노트북 8절에서 차례로 출력한 판 번호와 칸·줄입니다. 파란 상자 둘은 판을 내린 줄과 다시 올린 줄입니다. 맨 위와 맨 아래 상자는 판 번호가 같지만, 1번 줄의 담당자가 다릅니다.</p>
<p>노트북 9절에서 Before 글의 <code>nullable=False</code>만 <code>True</code>로 바꾸자, 기본값이 없어도 판 올리기가 막히지 않았습니다. 세 줄의 새 칸은 모두 <code>None</code>이었습니다. NOT NULL 제약이 막은 것은 이미 든 세 줄의 새 칸에 들어갈 빈 값이었습니다. 빈 표에서는 막히지 않는 것을 노트북 밖에서 확인했고, 7블록에 적었습니다.</p><p>새 커널로 두 번 실행해 견주자, 코드 셀 서른하나의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 모델을 부르지 않아, 이 절의 출력은 판 파일과 서버에 남은 표로 정해집니다.</p>
<p class="look"><b>확인할 점</b> — Before 판에서 <code>오류 코드(SQLSTATE): 23502</code>와 <code>판 번호: 20260911_01</code>을 봅니다. After 판에서 <code>받은 오류: None</code>과 <code>판 번호: 20260929_02</code>를 확인합니다. 8절 다시 올리기 뒤 1번 줄의 담당자와, 9절의 <code>None</code> 세 개도 찾습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>새 판 파일은 임시 폴더의 사본에만 썼습니다. 실습 폴더의 <code>migrations/versions/</code>에 두면, 다음에 노트북을 실행할 때 첫 판 올리기가 둘째 판까지 이어져 출력이 달라집니다. 노트북 끝에서 실습 폴더에 새 판 파일이 없는 것을 확인했습니다.</li><li>이 실습 폴더의 <code>env.py</code>는 설정 객체의 접속 글을 환경 변수 값이나 기본 글로 늘 덮어씁니다. 그래서 설정 객체에 접속 글을 적는 방법은 쓰지 않았습니다. 파일 <code>env.py</code>와 <code>alembic.ini</code>는 고치지 않았습니다.</li><li>이 절은 판 올리기와 내리기를 파이썬 함수 <code>command.upgrade</code>·<code>command.downgrade</code>로 불렀습니다. 터미널 명령 <code>alembic upgrade head</code>도 같은 함수를 부르지만, 이 절에서는 실행하지 않았습니다. 파이썬 함수로 부르면 명령을 찾는 위치(PATH)에 기대지 않습니다.</li><li>명령 <code>alembic revision --autogenerate</code>는 코드의 표 정의와 데이터베이스를 견줘 판 파일 초안을 만듭니다. 이 실습 폴더의 <code>env.py</code>에는 그 표 정의가 이어져 있지 않아, 자동 생성은 실행하지 않았습니다. Alembic 문서는 자동 생성한 판 파일을 사람이 반드시 읽고 고치라고 적습니다.</li><li>명령으로 판 파일을 만들면 판 번호는 무작위 글로 정해집니다. 설치된 alembic 1.16.5 소스에서 확인했고, 이 절에서는 실행하지 않았습니다. 이 절은 출력이 매번 같도록 판 번호 <code>20260929_02</code>를 직접 정했습니다.</li><li>노트북 밖에서 빈 표에 같은 Before 판을 올려 보자, 막히지 않고 <code>20260929_02</code>가 되었습니다. 이 결함은 줄이 든 표에서만 드러나, 빈 데이터베이스로만 시험하면 보이지 않습니다.</li><li>판 내리기가 칸을 빼면 그 칸의 값도 없어집니다. 값을 남겨 두는 방법의 하나로, 판을 내리기 전에 데이터베이스를 파일로 남기는 백업이 있습니다. 백업은 <a href="05-pgvector-체크포인터-공존과-백업.html">05절</a>에서 봅니다.</li><li>칸 이름을 모으는 SQL 글에서 <code>::text</code>를 빼면, 칸 목록이 파이썬 목록이 아니라 <code>{id,question}</code> 같은 글 하나로 옵니다. 노트북 밖에서 확인했습니다. 자리 <code>information_schema.columns</code>의 칸 이름이 PostgreSQL의 따로 정한 자료형이라, 글로 바꿔 모았습니다.</li><li>도구 Alembic의 진행 기록은 오류 출력(stderr) 쪽으로 찍힙니다. 한 셀에서 보통 출력과 섞이면 찍히는 차례가 실행마다 바뀔 수 있어, 판을 올리고 내리는 셀과 결과를 출력하는 셀을 나눴습니다.</li><li>노트북을 쓰기 전에 노트북 밖에서 같은 장면을 파이썬 파일로 다섯 번 실행했고, 출력이 다섯 번 모두 같았습니다. 판 번호·칸·줄·오류 코드·오류 글 모두 실행할 때마다 같은 값입니다.</li><li>교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다. 그 서버는 Docker 컨테이너가 아니라 같은 접속 글로 켠 서버입니다. Docker 이미지로 켜면 버전 번호의 끝자리가 다를 수 있습니다. 다른 버전과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>실습 폴더의 판 파일을 임시 폴더에 복사하고, 환경 변수로 접속 글을 넘겨 첫 판 <code>20260911_01</code>을 올렸습니다.</li><li>줄 셋이 든 표에 기본값 없는 NOT NULL 칸을 더하는 판은 오류 코드 <code>23502</code>로 막혔고, 판 번호와 칸이 그대로였습니다.</li><li>서버 기본값을 준 판은 <code>20260929_02</code>까지 올라갔고, 판을 내렸다 다시 올리자 1번 줄의 담당자 값은 남지 않았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="04-커넥션-풀-고갈과-대응.html">04절</a>에서는 연결 풀에 빈 연결이 없을 때 무슨 일이 생기는지 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 이 절이 새 판 파일을 실습 폴더가 아니라 임시 폴더의 사본에 쓴 까닭은 무엇인가요?</p><p class="quiz-a">실습 폴더에 두면 판 사슬이 바뀌어, 다음에 실행할 때 첫 판 올리기가 둘째 판까지 이어지기 때문입니다. 설정 파일의 <code>%(here)s</code>가 사본 폴더를 가리켜, 도구는 사본의 판 파일만 읽었습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">2. 설정 객체에 접속 글을 적지 않고 환경 변수 <code>CH31_SYNC_URL</code>을 정한 까닭은 무엇인가요?</p><p class="quiz-a">실습 폴더의 <code>env.py</code> 12~15행이 그 환경 변수나 기본 글로 접속 글을 늘 새로 정하기 때문입니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">3. Before 판 올리기가 막힌 뒤, 판 번호와 칸은 무엇이었고 그 까닭은 무엇인가요?</p><p class="quiz-a">판 번호는 <code>20260911_01</code>, 칸은 <code>['id', 'question']</code>이었습니다. 판 파일의 SQL 문장이 막혀 칸이 생기지 않았고, 판 번호는 판 함수가 끝난 뒤에 적으므로 적히지 않았습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">4. 1번 줄의 담당자를 <code>'민지'</code>로 바꾼 뒤 판을 내렸다 다시 올리면, 1번 줄의 담당자는 무엇이 되었나요?</p><p class="quiz-a">담당자는 <code>'미정'</code>이 되었습니다. 판 내리기가 칸 <code>owner</code>를 빼며 값도 없어졌고, 다시 올릴 때는 서버 기본값이 들어갔습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p><p class="quiz-q">5. 동료가 「02절의 취소와 이 절의 판 내리기는 영어 이름이 같으니 같은 일이다」라고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 02절의 취소는 오류로 끝난 블록의 변경을 확정하지 않는 일입니다. 판 내리기는 이미 확정한 표 구조를 앞 판의 모양으로 바꾸는 새 작업이고, 뺀 칸의 값도 없어집니다. 틀렸다면 본문 4블록을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://alembic.sqlalchemy.org/en/latest/tutorial.html">Alembic Tutorial</a></div>확인 2026-09-29 · 문서 버전은 1.20이고, 교재 출력은 1.16.5입니다. 판 올리기는 판 기록 표 <code>alembic_version</code>부터 확인하고, 없으면 만든다고 적습니다. 상대 목표 <code>-1</code>과 맨 처음을 뜻하는 <code>base</code>도 적습니다.</li><li><div><a href="https://alembic.sqlalchemy.org/en/latest/api/commands.html">Alembic Commands</a></div>확인 2026-09-29 · 명령마다 함수가 있고, 모두 첫 인자로 설정 객체 <code>Config</code>를 받는다고 적습니다.</li><li><div><a href="https://alembic.sqlalchemy.org/en/latest/api/runtime.html">Alembic Runtime Objects</a></div>확인 2026-09-29 · 인자 <code>transactional_ddl</code>의 기본값은 서버가 지원하는지에 따른다고 적습니다. 기본으로는 여러 판 올리기를 한 묶음 작업 하나로 감싼다고 적습니다.</li><li><div><a href="https://alembic.sqlalchemy.org/en/latest/autogenerate.html">Alembic Auto Generating Migrations</a></div>확인 2026-09-29 · 자동 생성은 <code>env.py</code>가 표 정의에 닿아야 쓸 수 있다고 적습니다. 자동 생성은 완벽하지 않아, 사람이 늘 읽고 고쳐야 한다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/sql-altertable.html">PostgreSQL 17 ALTER TABLE</a></div>확인 2026-09-29 · 칸을 더하며 기본값을 적으면, 이미 있는 모든 줄에 그 값이 쓰인다고 적습니다. 기본값을 적지 않으면 빈 값이 쓰인다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/ddl-constraints.html">PostgreSQL 17 Constraints</a></div>확인 2026-09-29 · NOT NULL 제약은 칸이 빈 값을 가질 수 없다는 조건이라고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/errcodes-appendix.html">PostgreSQL 17 Error Codes</a></div>확인 2026-09-29 · 갈래 23은 제약 위반이고, <code>23502</code>는 <code>not_null_violation</code>이라고 적습니다.</li><li>설치판 alembic 1.16.5 소스 <code>runtime/migration.py</code> 211~218행은 진행 기록 <code>Context impl PostgresqlImpl.</code>과 <code>Will assume transactional DDL.</code>을 남기는 자리입니다. 620~632행은 <code>Running upgrade</code> 기록을 남긴 뒤 판 파일의 함수를 부르고, 그다음에 판 번호를 적습니다. <code>ddl/postgresql.py</code> 84행이 PostgreSQL에 <code>transactional_ddl = True</code>를 둡니다.</li><li>설치판 <code>config.py</code> 241~245행은 설정 파일이 있는 폴더를 <code>here</code>로 정합니다. <code>util/langhelpers.py</code> 232~233행은 명령이 만드는 판 번호를 무작위 글 열두 자로 정합니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# Alembic 적용과 롤백

**이 노트북에서 할 일**

1. 실습 폴더의 판 파일을 임시 폴더에 복사하고, Alembic으로 첫 판을 올려 표를 만듭니다.
2. 줄이 든 표에 기본값 없는 NOT NULL 칸을 더하는 판을 올리면, 판 번호와 칸이 그대로인 것을 봅니다.
3. 서버 기본값을 준 판으로 고쳐 올리고, 판을 내렸다가 다시 올리면 무엇이 남는지 확인합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.

01절과 같은 PostgreSQL 서버가 `127.0.0.1:55431`에서 켜져 있어야 합니다.
서버는 01절 준비물의 Docker 컨테이너 `kdt-ch31-postgres`입니다.
꺼져 있으면 터미널에서 `docker start kdt-ch31-postgres`로 다시 켭니다.
컨테이너를 아직 만들지 않았다면, 01절 노트북 맨 위 준비물의 `docker run` 명령을 먼저 실행합니다.

노트북은 데이터베이스 `ch31_lab` 안에 이름 공간 `ch31_migration`을 만들어 쓰고, 끝에서 지웁니다.
실습 폴더의 파일 `alembic.ini`와 폴더 `migrations/`는 읽기만 하고 고치지 않습니다.
새 판 파일은 운영체제 임시 폴더에 만든 사본에만 씁니다.
걸린 시간은 재지 않습니다.

**기준 버전** — 첫 셀에서 패키지 셋을 설치합니다.
버전은 sqlalchemy 2.0.43, psycopg 3.3.3, alembic 1.16.5이고, 실습 폴더 잠금과 같습니다.
이 노트북에서 「판」은 표 구조의 판만 가리키고, 패키지와 서버는 「버전」이라고 적습니다.
교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다.
그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다.

Docker 이미지로 켜면 서버 버전 번호의 끝자리가 다를 수 있습니다.
다른 버전과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~5절을 읽습니다.
판과 판 올리기, Alembic 설정을 처음 보는 자리입니다.
6·7절은 Before와 After이고, 8절은 판 내리기, 9절은 값 바꿔 보기입니다.
6~9절은 실습 시간에 실행하고, 10절은 만든 이름 공간을 지우는 정리입니다.

실습 폴더 `labs/part7/ch31-database`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 흐름도입니다. 맨 위 회색 상자 빈 자리 판 없음에서 판 올리기 화살표가 회색 상자 첫 판 20260911_01 실습 폴더 판 파일 표 tickets 만들기로 갑니다. 다시 판 올리기 화살표가 파란 상자 둘째 판 20260929_02 노트북이 사본에 쓴 판 파일 칸 owner 더하기로 이어지고, 둘째 판에서 첫 판으로 판 내리기 점선 화살표가 있습니다. 맨 아래 노란 상자는 판 기록 표 alembic_version이고, 첫 판 뒤 20260911_01과 After 뒤 20260929_02가 적힌 그림](attachment:03-1-판-사슬과-판-기록-표.png)

위에서 아래로 읽습니다.
회색 상자 둘은 빈 자리와 실습 폴더에 있던 첫 판이고, 파란 상자는 이 노트북이 사본에 쓰는 둘째 판입니다.
실선 화살표는 판 올리기, 점선 화살표는 판 내리기입니다.
노란 상자는 판 기록 표에 적힌 판 번호로, 노트북 5절과 7절 출력입니다.

### [2] markdown {}

## 1. 준비

01절과 02절에서는 노트북 셀에서 SQL 글로 표를 만들었습니다.
서비스를 고쳐 나가다 보면, 이미 줄이 든 표에 칸을 더해야 할 때가 옵니다.
이 절은 표의 모양을 바꾸는 일을 파일로 적어 두고, 차례대로 적용하는 방법을 봅니다.

절 제목의 Alembic은 SQLAlchemy 위에서 표의 모양 바꾸기를 파일로 관리하는 도구입니다.
제목의 롤백은 이 절에서 「판 내리기」를 뜻하고, 8절에서 봅니다.
02절의 취소(롤백)는 한 묶음 작업 안의 변경을 없던 일로 하는 것이라, 뜻이 다릅니다.

첫 셀은 이 절이 쓰는 패키지 셋을 설치하고, 설치된 버전 번호를 출력합니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:42.782082Z', 'iopub.status.busy': '2026-09-29T17:09:42.781926Z', 'iopub.status.idle': '2026-09-29T17:09:43.392513Z', 'shell.execute_reply': '2026-09-29T17:09:43.391876Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "sqlalchemy==2.0.43" "psycopg[binary]==3.3.3" "alembic==1.16.5"
from importlib.metadata import version

print("sqlalchemy:", version("sqlalchemy"))
print("psycopg:", version("psycopg"))
print("alembic:", version("alembic"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
sqlalchemy: 2.0.43
psycopg: 3.3.3
alembic: 1.16.5

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `sqlalchemy: 2.0.43`, `psycopg: 3.3.3`, `alembic: 1.16.5`가 보입니다.
세 버전 모두 실습 폴더 잠금과 같습니다.
드라이버 psycopg는 01절의 asyncpg처럼 파이썬과 서버 사이에서 말을 주고받습니다.
다만 `await` 없이 쓰는 동기 드라이버입니다.
이 실습 폴더의 Alembic 설정이 동기 엔진으로 서버에 붙기 때문에, 이 절은 psycopg를 씁니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `os`·`shutil`·`tempfile`은 Python에 들어 있는 기능 묶음입니다.
함수 모음 `command`와 설정 클래스 `Config`는 패키지 alembic에서 가져옵니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.393689Z', 'iopub.status.busy': '2026-09-29T17:09:43.393580Z', 'iopub.status.idle': '2026-09-29T17:09:43.593014Z', 'shell.execute_reply': '2026-09-29T17:09:43.592588Z'}, 'lesson_role': 'setup'}

```python
# 파일 복사·임시 폴더·환경 변수에 쓸 모듈과, Alembic·SQLAlchemy 이름을 가져옵니다
import os
import shutil
import tempfile
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

print("가져온 이름:", "command", "Config", "create_engine", "text", "IntegrityError")
```

출력:
```
가져온 이름: command Config create_engine text IntegrityError

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `가져온 이름: command Config create_engine text IntegrityError`가 보입니다.
이 노트북에는 API 키를 확인하는 셀이 없습니다.
모델을 부르지 않기 때문입니다.

## 2. 표 구조 바꾸기와 판

표 구조 바꾸기(마이그레이션, migration)는 데이터베이스 표에 칸을 더하거나 빼는 것처럼, 표의 모양을 바꾸는 일입니다.
학급 출석부에 연락처 칸을 새로 그어 넣는 일과 비슷합니다.
이 절에서는 표 `tickets`에 담당자 칸 `owner`를 더합니다.
Ch 21 04절의 옮기기(마이그레이션)는 옛 버전 라이브러리에 맞춘 코드를 새 버전에서 돌게 고치는 일이었습니다.
영어 이름만 같고, 이 절의 표 구조 바꾸기와는 뜻이 다릅니다.

판(리비전, revision)은 표 구조 바꾸기 한 번을 적은 파일 하나와, 그 파일에 붙인 판 번호입니다.
책의 개정판이 앞 판에서 무엇이 바뀌었는지 적어 두는 것과 비슷합니다.
판 파일마다 바로 앞 판의 번호를 적어 두어, 판들이 첫 판부터 한 줄로 이어집니다.
이 이어진 줄을 판 사슬이라고 부릅니다.

판 올리기(upgrade)는 판 파일의 함수 `upgrade`를 불러 다음 판으로 가는 일입니다.
판 내리기(downgrade)는 함수 `downgrade`를 불러 앞 판으로 가는 일입니다.
계단을 한 칸씩 오르내리는 것과 비슷합니다.
도구 Alembic은 데이터베이스가 지금 어느 판인지를 표 하나에 판 번호로 적어 둡니다.
이 표를 이 교재에서는 판 기록 표라고 부릅니다.

다음 셀은 연습용 접속 글을 정합니다.
01절 2절의 설정 셀과 견주면, 드라이버 이름 `asyncpg`가 `psycopg`로 바뀐 한 곳만 다릅니다.
서버 주소·계정·데이터베이스는 01절과 같고, 이 노트북도 `.env` 파일을 읽지 않습니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.593672Z', 'iopub.status.busy': '2026-09-29T17:09:43.593619Z', 'iopub.status.idle': '2026-09-29T17:09:43.595341Z', 'shell.execute_reply': '2026-09-29T17:09:43.595006Z'}}

```python
# 데이터베이스 접속 글을 정합니다(비밀번호 postgres는 이 실습에서만 쓰는 연습용 값입니다)
database_url = "postgresql+psycopg://postgres:postgres@127.0.0.1:55431/ch31_lab"
# 비밀번호가 찍히지 않게, 글을 @에서 나눠 앞의 드라이버 부분과 뒤의 서버 부분만 출력합니다
url_parts = database_url.split("@")
print("드라이버 부분:", database_url.split("://")[0])
print("서버 주소와 데이터베이스:", url_parts[1])
```

출력:
```
드라이버 부분: postgresql+psycopg
서버 주소와 데이터베이스: 127.0.0.1:55431/ch31_lab

```

### [8] markdown {}

**결과 읽기** — 출력 줄 `드라이버 부분: postgresql+psycopg`가 보입니다.
라벨 `서버 주소와 데이터베이스:` 뒤의 `127.0.0.1:55431/ch31_lab`은 01절과 같은 서버와 데이터베이스입니다.
비밀번호가 든 가운데 부분은 출력하지 않았습니다.

이 절은 실습 폴더의 파일 `alembic.ini`와 폴더 `migrations/`를 읽습니다.
노트북을 어디서 열었는지에 따라 이 파일을 가리키는 글이 달라집니다.
다음 셀은 Ch 30 01절의 파일 위치 셀처럼 후보 셋을 차례로 보고, 처음 있는 것을 고릅니다.
후보 이름과 찾을 파일만 이 챕터에 맞게 바꿨습니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.595959Z', 'iopub.status.busy': '2026-09-29T17:09:43.595911Z', 'iopub.status.idle': '2026-09-29T17:09:43.598047Z', 'shell.execute_reply': '2026-09-29T17:09:43.597710Z'}}

```python
# 노트북을 연 자리에서 본 실습 폴더의 위치를 후보 셋 가운데에서 고릅니다
candidates = ["..", ".", "labs/part7/ch31-database"]
lab_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/alembic.ini"):
        lab_path = candidate
        break
print("실습 폴더를 찾았는가:", lab_path is not None)
assert lab_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."
```

출력:
```
실습 폴더를 찾았는가: True

```

### [10] markdown {}

**결과 읽기** — 출력 줄 `실습 폴더를 찾았는가: True`가 보입니다.
첫 후보 `..`는 `notebooks/` 폴더에서 열었을 때 맞는 자리입니다.
둘째 `.`는 실습 폴더 맨 위, 셋째는 프로젝트 맨 위에서 열었을 때 맞습니다.
학생 묶음을 풀어 `notebooks/`에서 열어도 첫 후보가 맞습니다.
고른 후보는 연 자리마다 달라서 출력하지 않습니다.

## 3. env.py가 읽는 환경 변수

도구 Alembic은 설정 파일 `alembic.ini`를 읽고, 폴더 `migrations/`의 파일 `env.py`를 실행합니다.
서버에 붙는 접속 글은 이 `env.py`가 정합니다.
다음 셀은 이 실습 폴더 `env.py`의 12~15행을 읽어 출력합니다.
메서드 `replace`는 글에서 앞의 글을 찾아, 뒤의 글로 바꾼 새 글을 내놓습니다.
접속 글 속 비밀번호 자리는 이 메서드로 가리고 출력합니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.598659Z', 'iopub.status.busy': '2026-09-29T17:09:43.598607Z', 'iopub.status.idle': '2026-09-29T17:09:43.600944Z', 'shell.execute_reply': '2026-09-29T17:09:43.600548Z'}}

```python
# 실습 폴더 env.py의 12~15행을 읽어, 접속 글 속 비밀번호 자리만 가리고 출력합니다
with open(lab_path + "/migrations/env.py", encoding="utf-8") as env_file:
    env_lines = env_file.read().splitlines()
print("env.py 12~15행:")
# 목록의 11번 자리가 12행이라, [11:15]가 12행부터 15행까지입니다
for line in env_lines[11:15]:
    print(line.replace(":postgres@", ":(비밀번호)@"))
```

출력:
```
env.py 12~15행:
config.set_main_option(
    "sqlalchemy.url",
    os.getenv("CH31_SYNC_URL", "postgresql+psycopg://postgres:(비밀번호)@localhost:55431/ch31_lab"),
)

```

### [12] markdown {}

**결과 읽기** — 라벨 `env.py 12~15행:` 아래에 네 줄이 찍혔습니다.
함수 `os.getenv`는 이름이 `CH31_SYNC_URL`인 환경 변수를 읽고, 없으면 뒤에 적은 기본 글을 씁니다.
기본 글의 서버 주소는 `localhost`로, 이 챕터의 접속 글과 적은 모양이 다릅니다.
이 네 줄은 `alembic.ini`나 설정 객체에 무엇을 적든, 접속 글을 새로 정합니다.
그래서 이 절은 `env.py`를 고치지 않고, 환경 변수 `CH31_SYNC_URL`로 접속 글을 넘깁니다.

환경 변수는 Ch 28 03절에서 본 것처럼, 프로그램이 받는 이름과 값의 목록입니다.
파이썬에서는 딕셔너리처럼 쓰는 `os.environ`으로 읽고 넣습니다.
여기에 넣은 값은 이 노트북 커널 안에서 이어 쓰입니다.
다음 셀은 이 이름에 2절의 접속 글을 넣습니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.601562Z', 'iopub.status.busy': '2026-09-29T17:09:43.601517Z', 'iopub.status.idle': '2026-09-29T17:09:43.603323Z', 'shell.execute_reply': '2026-09-29T17:09:43.602962Z'}}

```python
# env.py가 읽는 환경 변수 CH31_SYNC_URL에 이 절의 접속 글을 넣습니다(값은 출력하지 않습니다)
os.environ["CH31_SYNC_URL"] = database_url
print("환경 변수 CH31_SYNC_URL을 정했는가:", os.environ["CH31_SYNC_URL"] == database_url)
```

출력:
```
환경 변수 CH31_SYNC_URL을 정했는가: True

```

### [14] markdown {}

**결과 읽기** — 출력 줄 `환경 변수 CH31_SYNC_URL을 정했는가: True`가 보입니다.
비밀번호가 든 값은 출력하지 않고, 넣은 값이 접속 글과 같은지만 봤습니다.
실습 폴더의 파일은 하나도 바뀌지 않았습니다.

## 4. 실습 폴더 사본과 Alembic 설정

다음 셀은 표를 읽고 쓸 엔진을 만들고, 이 절의 이름 공간 `ch31_migration`을 지웁니다.
함수 `create_engine`은 01절의 `create_async_engine`처럼 엔진을 만들되, 동기 엔진을 만듭니다.
그래서 블록도 `async with` 대신 `with`로 쓰고, `await`를 붙이지 않습니다.
블록 `engine.begin()`이 끝에서 확정하는 것은 01절과 같습니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.603949Z', 'iopub.status.busy': '2026-09-29T17:09:43.603902Z', 'iopub.status.idle': '2026-09-29T17:09:43.679308Z', 'shell.execute_reply': '2026-09-29T17:09:43.678977Z'}}

```python
# 동기 엔진을 만들고, 이름 공간 ch31_migration을 안의 표까지 지워 빈 자리에서 시작합니다
engine = create_engine(database_url)
with engine.begin() as conn:
    conn.execute(text("DROP SCHEMA IF EXISTS ch31_migration CASCADE"))
    result = conn.execute(text("SELECT to_regnamespace('ch31_migration')"))
    left_namespace = result.scalar_one()
print("엔진의 종류:", type(engine).__name__)
print("남은 이름 공간:", left_namespace)
```

출력:
```
엔진의 종류: Engine
남은 이름 공간: None

```

### [16] markdown {}

**결과 읽기** — 출력 줄 `엔진의 종류: Engine`과 `남은 이름 공간: None`이 보입니다.
이 절의 이름 공간이 없는 빈 자리에서 시작합니다.
판을 올릴 때 `env.py`가 이 이름 공간을 다시 만들고, 판 기록 표도 그 안에 둡니다.

다음 셀은 실습 폴더의 `alembic.ini`와 `migrations/` 폴더를 운영체제 임시 폴더에 복사합니다.
이 절은 새 판 파일을 만드는데, 실습 폴더에 두면 판 사슬이 바뀌어 다음 실행의 출력이 달라집니다.
그래서 Ch 23처럼 새 파일은 임시 폴더에만 씁니다.
함수 `tempfile.mkdtemp`는 임시 폴더 안에 새 폴더를 만들고, 그 위치를 글로 내놓습니다.
함수 `shutil.copy`는 파일 하나를, `shutil.copytree`는 폴더 하나를 통째로 복사합니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.679981Z', 'iopub.status.busy': '2026-09-29T17:09:43.679933Z', 'iopub.status.idle': '2026-09-29T17:09:43.685133Z', 'shell.execute_reply': '2026-09-29T17:09:43.684714Z'}}

```python
# 운영체제 임시 폴더에 새 폴더를 만들고, 실습 폴더의 alembic.ini와 migrations 폴더를 복사합니다
copy_folder = tempfile.mkdtemp(prefix="ch31-03-")
shutil.copy(lab_path + "/alembic.ini", copy_folder)
# 파이썬이 만든 __pycache__ 폴더는 빼고 복사합니다
skip_names = shutil.ignore_patterns("__pycache__")
shutil.copytree(lab_path + "/migrations", copy_folder + "/migrations", ignore=skip_names)
print("사본 폴더 이름에 ch31-03-이 들어 있는가:", "ch31-03-" in copy_folder)
print("사본에 alembic.ini가 있는가:", os.path.exists(copy_folder + "/alembic.ini"))
print("사본의 판 파일:", os.listdir(copy_folder + "/migrations/versions"))
```

출력:
```
사본 폴더 이름에 ch31-03-이 들어 있는가: True
사본에 alembic.ini가 있는가: True
사본의 판 파일: ['20260911_01_create_tickets.py']

```

### [18] markdown {}

**결과 읽기** — 출력 줄 `사본 폴더 이름에 ch31-03-이 들어 있는가: True`가 보입니다.
출력 줄 `사본에 alembic.ini가 있는가: True`도 보입니다.
라벨 `사본의 판 파일:` 뒤에는 첫 판 파일 `20260911_01_create_tickets.py` 하나가 있습니다.
인자 `ignore=`에 넘긴 값은 파이썬이 만든 `__pycache__` 폴더를 빼고 복사하게 합니다.
사본 폴더의 위치는 컴퓨터마다 달라서 출력하지 않았습니다.

다음 셀은 사본의 `alembic.ini`로 Alembic 설정 객체를 만듭니다.
설정 파일에는 판 파일 폴더가 `script_location = %(here)s/migrations`로 적혀 있습니다.
글 `%(here)s`는 설정 파일이 있는 폴더를 뜻해, 판 파일 폴더도 사본 안을 가리킵니다.
메서드 `get_main_option`은 설정 파일에서 이름에 맞는 값을 꺼냅니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.685717Z', 'iopub.status.busy': '2026-09-29T17:09:43.685670Z', 'iopub.status.idle': '2026-09-29T17:09:43.687766Z', 'shell.execute_reply': '2026-09-29T17:09:43.687404Z'}}

```python
# 사본의 alembic.ini로 Alembic 설정 객체를 만들고, 판 파일 폴더가 사본 안인지 봅니다
alembic_cfg = Config(copy_folder + "/alembic.ini")
script_location = alembic_cfg.get_main_option("script_location")
print("설정 객체의 종류:", type(alembic_cfg).__name__)
print("판 파일 폴더가 사본 안인가:", "ch31-03-" in script_location)
```

출력:
```
설정 객체의 종류: Config
판 파일 폴더가 사본 안인가: True

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `설정 객체의 종류: Config`와 `판 파일 폴더가 사본 안인가: True`가 보입니다.
이제 Alembic은 사본의 판 파일만 읽고, 실습 폴더의 `migrations/`는 건드리지 않습니다.
판을 올릴 때 파이썬이 판 파일을 읽으며 만드는 파일도 사본 안에만 생깁니다.

## 5. 첫 판 올리기

다음 셀은 지금 판의 모습을 볼 SQL 글 셋을 정합니다.
표 `alembic_version`이 Alembic의 판 기록 표이고, 지금 판 번호 한 줄이 들어 있습니다.
Ch 23 02절의 표 만들기 기록처럼, 어디까지 실행했는지를 판 번호로 남깁니다.
자리 `information_schema.columns`는 데이터베이스의 모든 표에 대해 칸 이름과 차례를 보여 줍니다.
SQL 함수 `array_agg`는 여러 줄의 값을 목록 하나로 모읍니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.688329Z', 'iopub.status.busy': '2026-09-29T17:09:43.688279Z', 'iopub.status.idle': '2026-09-29T17:09:43.690186Z', 'shell.execute_reply': '2026-09-29T17:09:43.689835Z'}}

```python
# 판 번호·칸 이름·줄을 읽는 SQL 글 셋을 정합니다
version_sql = "SELECT version_num FROM ch31_migration.alembic_version"
columns_sql = """SELECT array_agg(column_name::text ORDER BY ordinal_position)
FROM information_schema.columns
WHERE table_schema = 'ch31_migration' AND table_name = 'tickets'"""
rows_sql = "SELECT * FROM ch31_migration.tickets ORDER BY id"
print("칸 이름을 읽는 SQL 글:")
print(columns_sql)
```

출력:
```
칸 이름을 읽는 SQL 글:
SELECT array_agg(column_name::text ORDER BY ordinal_position)
FROM information_schema.columns
WHERE table_schema = 'ch31_migration' AND table_name = 'tickets'

```

### [22] markdown {}

**결과 읽기** — 라벨 `칸 이름을 읽는 SQL 글:` 아래에 SQL 글 세 줄이 찍혔습니다.
글 `column_name::text`는 칸 이름을 글 자료형으로 바꿔, 파이썬에서 목록으로 받게 합니다.
글 `ORDER BY ordinal_position`은 칸을 표에 만든 차례대로 모으라는 뜻입니다.
조건 `WHERE`는 이름 공간 `ch31_migration`의 표 `tickets`만 고릅니다.
나머지 두 글은 판 번호와 표의 모든 줄을 읽고, 글 `SELECT *`의 별표는 모든 칸을 뜻합니다.

다음 셀은 이 세 글로 판 번호·칸·줄을 한꺼번에 출력하는 함수를 정의합니다.
메서드 `scalar_one`은 01절처럼, 결과가 한 줄일 때 그 줄의 첫 칸 값을 꺼냅니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.690715Z', 'iopub.status.busy': '2026-09-29T17:09:43.690670Z', 'iopub.status.idle': '2026-09-29T17:09:43.692446Z', 'shell.execute_reply': '2026-09-29T17:09:43.692074Z'}}

```python
# 판 기록 표의 판 번호와, 표 tickets의 칸 이름·줄을 읽어 출력하는 함수를 정의합니다
def show_state():
    with engine.connect() as conn:
        version = conn.execute(text(version_sql)).scalar_one()
        columns = conn.execute(text(columns_sql)).scalar_one()
        rows = conn.execute(text(rows_sql)).fetchall()
    print("판 번호:", version)
    print("칸:", columns)
    print("줄:", rows)
```

출력:
```

```

### [24] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수는 불릴 때마다 연결을 빌려 세 글을 보내고, 블록이 끝나면 연결을 풀에 다시 넣습니다.
판 기록 표에는 줄이 하나뿐이라, 판 번호 하나가 나옵니다.

다음 셀은 판 올리기를 해 보는 함수를 정의합니다.
함수 `command.upgrade`는 설정 객체와 목표 판을 받아, 지금 판에서 목표 판까지 차례로 올립니다.
목표 `"head"`는 판 사슬의 맨 끝에 있는, 가장 새 판을 뜻합니다.
오류를 받는 모양은 02절처럼 `except IntegrityError as error:`입니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.693026Z', 'iopub.status.busy': '2026-09-29T17:09:43.692967Z', 'iopub.status.idle': '2026-09-29T17:09:43.694439Z', 'shell.execute_reply': '2026-09-29T17:09:43.694127Z'}}

```python
# 가장 새 판까지 올려 보고, IntegrityError를 받으면 그 오류를, 받지 않으면 None을 내놓는 함수를 정의합니다
def try_upgrade():
    try:
        command.upgrade(alembic_cfg, "head")
    except IntegrityError as error:
        return error
    return None
```

출력:
```

```

### [26] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
02절은 받은 오류를 그 자리에서 출력했지만, 이 함수는 오류를 내놓아 다음 셀에서 봅니다.
도구 Alembic은 진행 기록을 오류 출력(stderr) 쪽으로 따로 내보냅니다.
한 셀에서 두 출력이 섞이면 찍히는 차례가 실행마다 바뀔 수 있어, 셀을 나눕니다.

다음 셀은 이 함수로 첫 판을 올립니다.
사본의 판 파일은 하나뿐이라, 가장 새 판은 첫 판 `20260911_01`입니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.694995Z', 'iopub.status.busy': '2026-09-29T17:09:43.694943Z', 'iopub.status.idle': '2026-09-29T17:09:43.706628Z', 'shell.execute_reply': '2026-09-29T17:09:43.706286Z'}}

```python
# 사본의 판 파일로 가장 새 판까지 올립니다(Alembic의 진행 기록만 찍힙니다)
first_error = try_upgrade()
```

출력:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 20260911_01, 상담 티켓 표 구조를 변경합니다.

```

### [28] markdown {}

**결과 읽기** — Alembic의 진행 기록 세 줄이 찍혔습니다.
편집기에 따라 이 기록은 바탕색이 다르게 보일 수 있지만, 오류가 아닙니다.
기록 `Will assume transactional DDL.`은 표 구조 바꾸기도 한 묶음 작업 안에서 한다는 뜻입니다.
기록 `Running upgrade  -> 20260911_01`은 빈 자리에서 첫 판으로 올렸다는 뜻입니다.

기록 끝의 글은 첫 판 파일 맨 위에 적힌 설명 글입니다.
설명 글은 표 구조를 바꾼다고 적었지만, 이 판은 표 `tickets`를 새로 만듭니다.
다음 셀에서 받은 오류와 판 번호를 봅니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.707174Z', 'iopub.status.busy': '2026-09-29T17:09:43.707144Z', 'iopub.status.idle': '2026-09-29T17:09:43.711386Z', 'shell.execute_reply': '2026-09-29T17:09:43.711067Z'}}

```python
# 첫 판 올리기에서 받은 오류와, 판 번호·칸·줄을 봅니다
print("받은 오류:", first_error)
show_state()
```

출력:
```
받은 오류: None
판 번호: 20260911_01
칸: ['id', 'question']
줄: []

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `받은 오류: None`과 `판 번호: 20260911_01`이 보입니다.
라벨 `칸:` 뒤의 `['id', 'question']`은 첫 판이 만든 표의 두 칸입니다.
출력 줄 `줄: []`처럼 표는 아직 비어 있습니다.

다음 셀은 표 `tickets`에 상담 질문 세 줄을 넣습니다.
질문 글은 01절 표 `requests`의 문의 세 줄과 같은 환불·배송·결제입니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.711906Z', 'iopub.status.busy': '2026-09-29T17:09:43.711872Z', 'iopub.status.idle': '2026-09-29T17:09:43.715227Z', 'shell.execute_reply': '2026-09-29T17:09:43.714996Z'}}

```python
# 표 tickets에 상담 질문 세 줄을 넣고, 판 번호·칸·줄을 다시 봅니다
insert_sql = "INSERT INTO ch31_migration.tickets (id, question) VALUES (1, '환불'), (2, '배송'), (3, '결제')"
with engine.begin() as conn:
    inserted = conn.execute(text(insert_sql))
print("넣은 줄 수:", inserted.rowcount)
show_state()
```

출력:
```
넣은 줄 수: 3
판 번호: 20260911_01
칸: ['id', 'question']
줄: [(1, '환불'), (2, '배송'), (3, '결제')]

```

### [32] markdown {}

**결과 읽기** — 출력 줄 `넣은 줄 수: 3`과 `판 번호: 20260911_01`이 보입니다.
라벨 `줄:` 뒤에 `(1, '환불')`부터 `(3, '결제')`까지 세 줄이 있습니다.
이 세 줄이 든 표에, 다음 절에서 새 칸을 더합니다.

### [33] markdown {'lesson_part': 'before'}

## 6. 기본값 없는 NOT NULL 칸을 더하는 판 (Before)

이번에는 표 `tickets`에 담당자 칸 `owner`를 더하는 둘째 판을 만듭니다.
새 칸에는 NOT NULL 제약을 겁니다.
이 제약은 그 칸이 빈 값(`NULL`)을 가질 수 없다는 조건입니다.
Ch 4 03절에서 본 제약처럼, 어기는 줄은 서버가 막습니다.
다음 셀은 Before 판 파일의 글을 변수에 담습니다.

### [34] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.715708Z', 'iopub.status.busy': '2026-09-29T17:09:43.715678Z', 'iopub.status.idle': '2026-09-29T17:09:43.717321Z', 'shell.execute_reply': '2026-09-29T17:09:43.717046Z'}, 'lesson_part': 'before'}

```python
# Before: 담당자 칸 owner를 기본값 없이 NOT NULL로 더하는 판 파일의 글을 정합니다
before_text = """from alembic import op
import sqlalchemy as sa

revision = "20260929_02"
down_revision = "20260911_01"

def upgrade():
    owner = sa.Column("owner", sa.String(length=50), nullable=False)
    op.add_column("tickets", owner, schema="ch31_migration")

def downgrade():
    op.drop_column("tickets", "owner", schema="ch31_migration")
"""
```

출력:
```

```

### [35] markdown {'lesson_part': 'before'}

**결과 읽기** — 글을 변수에 담기만 해서 출력이 없습니다.
변수 `revision`은 이 판의 번호이고, `down_revision`은 바로 앞 판의 번호입니다.
함수 `upgrade`는 판 올리기에서, `downgrade`는 판 내리기에서 Alembic이 부릅니다.
함수 `op.add_column`은 표에 칸을 더하고, `op.drop_column`은 칸을 뺍니다.
인자 `nullable=False`가 NOT NULL 제약이고, 기본값은 적지 않았습니다.

판 번호 `20260929_02`는 출력이 매번 같도록 이 교재가 정한 글입니다.
실습 폴더의 첫 판 파일도 변수 둘과 함수 둘로 이루어져 있습니다.
다음 셀은 이 글을 사본의 `versions` 폴더에 판 파일로 씁니다.
파일 쓰기는 Ch 2 05절의 `with open(…, "w", encoding="utf-8")` 모양입니다.

### [36] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.717855Z', 'iopub.status.busy': '2026-09-29T17:09:43.717830Z', 'iopub.status.idle': '2026-09-29T17:09:43.719860Z', 'shell.execute_reply': '2026-09-29T17:09:43.719487Z'}, 'lesson_part': 'before'}

```python
# 사본의 versions 폴더에 Before 판 파일을 씁니다(실습 폴더의 migrations는 그대로 둡니다)
revision_path = copy_folder + "/migrations/versions/20260929_02_add_owner.py"
with open(revision_path, "w", encoding="utf-8") as revision_file:
    revision_file.write(before_text)
lab_revision = lab_path + "/migrations/versions/20260929_02_add_owner.py"
print("사본에 새 판 파일이 있는가:", os.path.exists(revision_path))
print("실습 폴더에 새 판 파일이 있는가:", os.path.exists(lab_revision))
```

출력:
```
사본에 새 판 파일이 있는가: True
실습 폴더에 새 판 파일이 있는가: False

```

### [37] markdown {'lesson_part': 'before'}

**결과 읽기** — 출력 줄 `사본에 새 판 파일이 있는가: True`가 보입니다.
출력 줄 `실습 폴더에 새 판 파일이 있는가: False`도 보입니다.
새 판 파일은 사본에만 생겼습니다.

사본의 판 사슬은 이제 첫 판에서 둘째 판으로 이어집니다.
다음 셀은 이 판까지 올려 봅니다.
실행 전에 예상해 봅니다.
줄 셋이 든 표에 빈 값을 허용하지 않는 칸을 더하면, 판 번호는 무엇이 될까요?

### [38] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.720324Z', 'iopub.status.busy': '2026-09-29T17:09:43.720293Z', 'iopub.status.idle': '2026-09-29T17:09:43.728411Z', 'shell.execute_reply': '2026-09-29T17:09:43.728079Z'}, 'lesson_part': 'before'}

```python
# Before 판 파일로 가장 새 판까지 올려 보고, 받은 오류를 변수에 담아 둡니다
before_error = try_upgrade()
```

출력:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20260911_01 -> 20260929_02

```

### [39] markdown {'lesson_part': 'before'}

**결과 읽기** — 진행 기록 세 줄 가운데 마지막 줄은 `Running upgrade 20260911_01 -> 20260929_02`입니다.
이 기록은 둘째 판을 올리기 시작했다는 뜻이고, 끝났다는 뜻은 아닙니다.
설치된 alembic 1.16.5는 판 파일의 함수를 부르기 전에 이 기록을 남깁니다.
셀은 끝까지 갔고, 받은 오류는 변수 `before_error`에 담겼습니다.

다음 셀은 받은 오류의 이름과 오류 코드, Alembic이 서버에 보낸 SQL 글을 봅니다.
속성 `statement`에는 오류가 난 SQL 글이 들어 있습니다.

### [40] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.728945Z', 'iopub.status.busy': '2026-09-29T17:09:43.728915Z', 'iopub.status.idle': '2026-09-29T17:09:43.730890Z', 'shell.execute_reply': '2026-09-29T17:09:43.730539Z'}, 'lesson_part': 'before'}

```python
# Before 판 올리기에서 받은 오류의 이름·오류 코드와, Alembic이 서버에 보낸 SQL 글을 봅니다
print("받은 오류:", type(before_error).__name__)
print("드라이버의 오류 이름:", type(before_error.orig).__name__)
print("오류 코드(SQLSTATE):", before_error.orig.sqlstate)
print("Alembic이 보낸 SQL 글:", before_error.statement)
print("드라이버가 받은 오류 글:")
print(before_error.orig)
```

출력:
```
받은 오류: IntegrityError
드라이버의 오류 이름: NotNullViolation
오류 코드(SQLSTATE): 23502
Alembic이 보낸 SQL 글: ALTER TABLE ch31_migration.tickets ADD COLUMN owner VARCHAR(50) NOT NULL
드라이버가 받은 오류 글:
column "owner" of relation "tickets" contains null values

```

### [41] markdown {'lesson_part': 'before'}

**결과 읽기** — 출력 줄 `받은 오류: IntegrityError`와 `오류 코드(SQLSTATE): 23502`가 보입니다.
드라이버 psycopg가 붙인 오류 이름은 `NotNullViolation`입니다.
PostgreSQL 문서는 `23502`를 NOT NULL 위반(not_null_violation)이라고 적습니다.
라벨 `Alembic이 보낸 SQL 글:` 뒤의 글은 함수 `op.add_column`이 만든 SQL 문장입니다.
라벨 줄 아래 오류 글은 칸 `owner`에 빈 값이 들어 있다는 뜻입니다.

새 칸을 더하면, 이미 있는 세 줄의 새 칸에는 기본값이 들어갑니다.
기본값을 적지 않았으므로, 세 줄 모두 빈 값이 됩니다.
그런데 NOT NULL 제약이 빈 값을 허용하지 않아, 서버가 SQL 문장을 막았습니다.

다음 셀은 판 올리기가 끝난 뒤의 판 번호·칸·줄을 봅니다.

### [42] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.731491Z', 'iopub.status.busy': '2026-09-29T17:09:43.731463Z', 'iopub.status.idle': '2026-09-29T17:09:43.734128Z', 'shell.execute_reply': '2026-09-29T17:09:43.733900Z'}, 'lesson_part': 'before'}

```python
# Before 판 올리기가 끝난 뒤, 판 번호·칸·줄을 봅니다
show_state()
```

출력:
```
판 번호: 20260911_01
칸: ['id', 'question']
줄: [(1, '환불'), (2, '배송'), (3, '결제')]

```

### [43] markdown {'lesson_part': 'before'}

**결과 읽기** — 출력 줄 `판 번호: 20260911_01`이 보입니다.
라벨 `칸:` 뒤는 `['id', 'question']`으로, 칸 `owner`가 없습니다.
판 사슬에는 둘째 판이 있는데, 데이터베이스는 첫 판에 머물렀습니다.
이것이 이 절의 Before 결함입니다.

이 판의 함수 `upgrade`에는 SQL 문장이 하나뿐이라, 문장이 막히자 칸이 생기지 않았습니다.
도구 Alembic은 판 번호를 판 함수가 끝난 뒤에 적으므로, 판 번호를 적는 데까지 가지 않았습니다.
문서대로라면 판 파일에 문장이 여럿일 때, 앞 문장도 한 묶음 작업으로 함께 취소됩니다.
그 장면은 이번에 실행하지 않았습니다.
하지만 새 칸 `owner`를 읽도록 고친 코드가 있다면, 그 코드는 칸이 없는 표를 만납니다.

### [44] markdown {'lesson_part': 'after'}

## 7. 서버 기본값을 준 판 (After)

After 판은 같은 판 파일에서 한 곳만 고칩니다.
인자 `server_default="미정"`을 더해, 빈 칸에 서버가 넣을 기본값을 정합니다.
서버 기본값은 새 칸을 더할 때, 이미 있는 줄에도 들어갑니다.

판 번호 `20260929_02`는 그대로 두고, 파일 내용만 고쳐 씁니다.
Before 판 올리기가 막혀, 데이터베이스는 아직 이 판을 올리지 않았기 때문입니다.
3절에서 쓴 메서드 `replace`로, Before 글의 한 곳을 바꾼 새 글을 만듭니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.734696Z', 'iopub.status.busy': '2026-09-29T17:09:43.734665Z', 'iopub.status.idle': '2026-09-29T17:09:43.736322Z', 'shell.execute_reply': '2026-09-29T17:09:43.736142Z'}, 'lesson_part': 'after'}

```python
# After: Before 글의 nullable=False 뒤에 서버 기본값 "미정"을 더해, 같은 판 파일에 고쳐 씁니다
after_text = before_text.replace("nullable=False)", 'nullable=False, server_default="미정")')
with open(revision_path, "w", encoding="utf-8") as revision_file:
    revision_file.write(after_text)
# 고친 글에서 server_default가 든 줄만 골라 출력합니다
for line in after_text.splitlines():
    if "server_default" in line:
        print("고친 줄:", line.strip())
```

출력:
```
고친 줄: owner = sa.Column("owner", sa.String(length=50), nullable=False, server_default="미정")

```

### [46] markdown {'lesson_part': 'after'}

**결과 읽기** — 라벨 `고친 줄:` 뒤에 `server_default="미정"`이 더해진 줄이 보입니다.
나머지 줄은 Before 판 파일과 같습니다.

다음 셀은 고친 판 파일로 다시 올려 봅니다.
실행 전에 예상해 봅니다.
이번에는 판 번호와 세 줄의 새 칸이 어떻게 될까요?

### [47] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.736849Z', 'iopub.status.busy': '2026-09-29T17:09:43.736821Z', 'iopub.status.idle': '2026-09-29T17:09:43.745079Z', 'shell.execute_reply': '2026-09-29T17:09:43.744854Z'}, 'lesson_part': 'after'}

```python
# 고친 판 파일로 가장 새 판까지 다시 올려 봅니다
after_error = try_upgrade()
```

출력:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20260911_01 -> 20260929_02

```

### [48] markdown {'lesson_part': 'after'}

**결과 읽기** — 진행 기록의 마지막 줄은 Before 판과 같은 `Running upgrade 20260911_01 -> 20260929_02`입니다.
기록만으로는 판 올리기가 끝났는지 가를 수 없습니다.
다음 셀에서 받은 오류와 판 번호를 봅니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.745592Z', 'iopub.status.busy': '2026-09-29T17:09:43.745565Z', 'iopub.status.idle': '2026-09-29T17:09:43.748317Z', 'shell.execute_reply': '2026-09-29T17:09:43.748085Z'}, 'lesson_part': 'after'}

```python
# After 판 올리기에서 받은 오류와, 판 번호·칸·줄을 봅니다
print("받은 오류:", after_error)
show_state()
```

출력:
```
받은 오류: None
판 번호: 20260929_02
칸: ['id', 'question', 'owner']
줄: [(1, '환불', '미정'), (2, '배송', '미정'), (3, '결제', '미정')]

```

### [50] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `받은 오류: None`과 `판 번호: 20260929_02`가 보입니다.
라벨 `칸:` 뒤는 `['id', 'question', 'owner']`로, 칸 `owner`가 더해졌습니다.
라벨 `줄:` 뒤에서 세 줄 모두 새 칸 값이 `'미정'`입니다.

Before 판과 After 판의 파일은 서버 기본값 한 곳만 달랐습니다.
그 한 곳이 이미 있는 세 줄의 새 칸을 채워, NOT NULL 제약을 지키게 했습니다.

## 8. 판 내리기와 다시 올리기

절 제목의 롤백은 판 내리기입니다.
이 절의 둘째 판은 판 내리기에서 함수 `op.drop_column`으로 칸 `owner`를 뺍니다.
02절의 취소는 한 묶음 작업이 오류로 끝날 때, 그 안의 변경을 확정하지 않는 일이었습니다.
판 내리기는 이미 확정한 표 구조를, 새 한 묶음 작업으로 앞 판의 모양으로 바꾸는 일입니다.

다음 셀은 먼저 1번 줄의 담당자를 `민지`로 바꿉니다.
판을 내렸다가 다시 올리면 이 값이 남는지 보려는 것입니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.748826Z', 'iopub.status.busy': '2026-09-29T17:09:43.748799Z', 'iopub.status.idle': '2026-09-29T17:09:43.752090Z', 'shell.execute_reply': '2026-09-29T17:09:43.751763Z'}, 'lesson_part': 'after'}

```python
# 1번 줄의 담당자를 민지로 바꾸고, 판 번호·칸·줄을 봅니다
update_sql = "UPDATE ch31_migration.tickets SET owner = '민지' WHERE id = 1"
with engine.begin() as conn:
    updated = conn.execute(text(update_sql))
print("바꾼 줄 수:", updated.rowcount)
show_state()
```

출력:
```
바꾼 줄 수: 1
판 번호: 20260929_02
칸: ['id', 'question', 'owner']
줄: [(1, '환불', '민지'), (2, '배송', '미정'), (3, '결제', '미정')]

```

### [52] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `바꾼 줄 수: 1`과 `판 번호: 20260929_02`가 보입니다.
라벨 `줄:` 뒤에서 1번 줄의 담당자만 `'민지'`이고, 나머지 두 줄은 `'미정'`입니다.

다음 셀은 판을 하나 내립니다.
함수 `command.downgrade`의 목표 `"-1"`은 지금 판에서 한 판 아래라는 뜻입니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.752573Z', 'iopub.status.busy': '2026-09-29T17:09:43.752545Z', 'iopub.status.idle': '2026-09-29T17:09:43.760131Z', 'shell.execute_reply': '2026-09-29T17:09:43.759852Z'}, 'lesson_part': 'after'}

```python
# 판을 하나 내립니다(목표 -1은 지금 판에서 한 판 아래라는 뜻입니다)
command.downgrade(alembic_cfg, "-1")
```

출력:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 20260929_02 -> 20260911_01

```

### [54] markdown {'lesson_part': 'after'}

**결과 읽기** — 진행 기록의 마지막 줄 `Running downgrade 20260929_02 -> 20260911_01`이 보입니다.
둘째 판에서 첫 판으로 내려간다는 기록입니다.
다음 셀에서 판 번호·칸·줄을 봅니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.760667Z', 'iopub.status.busy': '2026-09-29T17:09:43.760636Z', 'iopub.status.idle': '2026-09-29T17:09:43.763313Z', 'shell.execute_reply': '2026-09-29T17:09:43.763082Z'}, 'lesson_part': 'after'}

```python
# 판을 내린 뒤, 판 번호·칸·줄을 봅니다
show_state()
```

출력:
```
판 번호: 20260911_01
칸: ['id', 'question']
줄: [(1, '환불'), (2, '배송'), (3, '결제')]

```

### [56] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `판 번호: 20260911_01`이 보입니다.
라벨 `칸:` 뒤는 `['id', 'question']`으로, 칸 `owner`가 빠졌습니다.
세 줄은 남았지만, 1번 줄의 `'민지'`는 칸과 함께 없어졌습니다.

다음 셀은 같은 판 파일로 다시 올립니다.
실행 전에 예상해 봅니다.
다시 올리면 1번 줄의 담당자는 무엇일까요?

### [57] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.763835Z', 'iopub.status.busy': '2026-09-29T17:09:43.763804Z', 'iopub.status.idle': '2026-09-29T17:09:43.771604Z', 'shell.execute_reply': '2026-09-29T17:09:43.771320Z'}, 'lesson_part': 'after'}

```python
# 같은 판 파일로 가장 새 판까지 다시 올립니다
reup_error = try_upgrade()
```

출력:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20260911_01 -> 20260929_02

```

### [58] markdown {'lesson_part': 'after'}

**결과 읽기** — 진행 기록의 마지막 줄은 `Running upgrade 20260911_01 -> 20260929_02`입니다.
다음 셀에서 받은 오류와 판 번호·칸·줄을 봅니다.

### [59] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.772088Z', 'iopub.status.busy': '2026-09-29T17:09:43.772060Z', 'iopub.status.idle': '2026-09-29T17:09:43.774836Z', 'shell.execute_reply': '2026-09-29T17:09:43.774482Z'}, 'lesson_part': 'after'}

```python
# 다시 올린 뒤 받은 오류와, 판 번호·칸·줄을 봅니다
print("받은 오류:", reup_error)
show_state()
```

출력:
```
받은 오류: None
판 번호: 20260929_02
칸: ['id', 'question', 'owner']
줄: [(1, '환불', '미정'), (2, '배송', '미정'), (3, '결제', '미정')]

```

### [60] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `받은 오류: None`과 `판 번호: 20260929_02`가 보입니다.
라벨 `줄:` 뒤에서 1번 줄의 담당자는 `'민지'`가 아니라 `'미정'`입니다.
칸은 다시 생겼지만, 판 내리기에서 없어진 값은 다시 생기지 않았습니다.
이 판의 판 내리기는 칸을 빼는 함수라, 뺀 칸의 값을 남겨 두지 않습니다.

## 9. 값 바꿔 보기: nullable

값 하나만 바꿔 봅니다.
바꿀 것은 Before 판 글의 `nullable=False`이고, `True`로 바꿔 빈 값을 허용합니다.
기본값은 Before처럼 적지 않습니다.

다음 셀은 판을 하나 내린 뒤, 바꾼 글로 판 파일을 고쳐 쓰고 다시 올립니다.
실행 전에 예상해 봅니다.
이번에도 판 올리기가 막힐까요?

### [61] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.775327Z', 'iopub.status.busy': '2026-09-29T17:09:43.775298Z', 'iopub.status.idle': '2026-09-29T17:09:43.790208Z', 'shell.execute_reply': '2026-09-29T17:09:43.789980Z'}, 'lesson_part': 'after'}

```python
# 값 바꿔 보기: 판을 하나 내리고, Before 글의 nullable=False만 True로 바꿔 쓴 뒤 다시 올립니다
command.downgrade(alembic_cfg, "-1")
vary_text = before_text.replace("nullable=False", "nullable=True")
with open(revision_path, "w", encoding="utf-8") as revision_file:
    revision_file.write(vary_text)
vary_error = try_upgrade()
```

출력:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 20260929_02 -> 20260911_01
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20260911_01 -> 20260929_02

```

### [62] markdown {'lesson_part': 'after'}

**결과 읽기** — 진행 기록 여섯 줄이 찍혔습니다.
앞 세 줄은 판 내리기, 뒤 세 줄은 판 올리기의 기록입니다.
마지막 줄은 `Running upgrade 20260911_01 -> 20260929_02`입니다.
다음 셀에서 받은 오류와 판 번호·칸·줄을 봅니다.

### [63] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.790676Z', 'iopub.status.busy': '2026-09-29T17:09:43.790649Z', 'iopub.status.idle': '2026-09-29T17:09:43.793356Z', 'shell.execute_reply': '2026-09-29T17:09:43.793126Z'}, 'lesson_part': 'after'}

```python
# 바꾼 판을 올린 뒤 받은 오류와, 판 번호·칸·줄을 봅니다
print("받은 오류:", vary_error)
show_state()
```

출력:
```
받은 오류: None
판 번호: 20260929_02
칸: ['id', 'question', 'owner']
줄: [(1, '환불', None), (2, '배송', None), (3, '결제', None)]

```

### [64] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `받은 오류: None`과 `판 번호: 20260929_02`가 보입니다.
라벨 `줄:` 뒤에서 세 줄 모두 새 칸 값이 `None`입니다.
빈 값을 허용하자, 기본값이 없어도 판 올리기가 막히지 않았습니다.
NOT NULL 제약이 막은 것은, 6절 오류 글 `contains null values`처럼 이미 든 세 줄의 새 칸에 들어갈 빈 값이었습니다.
빈 표에서는 막히지 않는 것을 노트북 밖에서 확인했습니다.

## 10. 정리: 이름 공간 지우기

다음 셀은 이름 공간 `ch31_migration`을 판 기록 표까지 지우고, 엔진의 연결을 닫습니다.
PostgreSQL 함수 `to_regnamespace`는 01절처럼, 이름 공간이 없으면 빈 값을 내놓습니다.
임시 폴더의 사본은 실습 폴더 밖에 있어 그대로 둡니다.

### [65] code {'execution': {'iopub.execute_input': '2026-09-29T17:09:43.793879Z', 'iopub.status.busy': '2026-09-29T17:09:43.793853Z', 'iopub.status.idle': '2026-09-29T17:09:43.797224Z', 'shell.execute_reply': '2026-09-29T17:09:43.796982Z'}, 'lesson_part': 'after'}

```python
# 끝 정리: 이름 공간 ch31_migration을 판 기록 표까지 지우고, 남았는지 물은 뒤 엔진의 연결을 닫습니다
with engine.begin() as conn:
    conn.execute(text("DROP SCHEMA ch31_migration CASCADE"))
    result = conn.execute(text("SELECT to_regnamespace('ch31_migration')"))
    left_namespace = result.scalar_one()
engine.dispose()
print("남은 이름 공간:", left_namespace)
print("실습 폴더에 새 판 파일이 있는가:", os.path.exists(lab_revision))
```

출력:
```
남은 이름 공간: None
실습 폴더에 새 판 파일이 있는가: False

```

### [66] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `남은 이름 공간: None`과 `실습 폴더에 새 판 파일이 있는가: False`가 보입니다.
이 노트북을 처음부터 다시 실행하면, 4절이 이름 공간을 지우고 새 사본을 만들어 같은 출력이 나옵니다.

## 정리

1. 실습 폴더의 판 파일을 임시 폴더에 복사하고, 환경 변수로 접속 글을 넘겨 첫 판 `20260911_01`을 올렸습니다.
2. 줄 셋이 든 표에 기본값 없는 NOT NULL 칸을 더하는 판은 오류 코드 `23502`로 막혔고, 판 번호와 칸이 그대로였습니다.
3. 서버 기본값을 준 판은 `20260929_02`까지 올라갔고, 판을 내렸다 다시 올리자 1번 줄의 담당자 값은 남지 않았습니다.

04절에서는 연결 풀에 빈 연결이 없을 때 무슨 일이 생기는지 봅니다.

## 그림

### 03-1-판-사슬과-판-기록-표.mmd

```mermaid
flowchart TB
  %% classes
  base["빈 자리<br>판 없음"]
  r1["첫 판 20260911_01<br>실습 폴더 판 파일<br>표 tickets 만들기"]
  r2["둘째 판 20260929_02<br>노트북이 사본에 쓴 판 파일<br>칸 owner 더하기"]:::flow
  ver["판 기록 표 alembic_version<br>첫 판 뒤 20260911_01<br>After 뒤 20260929_02"]:::measure
  base -->|판 올리기| r1
  r1 -->|판 올리기| r2
  r2 -.->|판 내리기| r1
  r2 ~~~ ver
```

판 파일은 앞 판 번호를 적어 한 줄로 이어지고, 판 기록 표에는 지금 판 번호 하나가 적힙니다.

### 03-2-사본으로-첫-판-올리기.mmd

```mermaid
flowchart TB
  %% classes
  lab["실습 폴더<br>alembic.ini · migrations"]
  cpy["임시 폴더 사본<br>폴더 이름 ch31-03-<br>판 파일 하나"]:::flow
  envv["환경 변수<br>CH31_SYNC_URL<br>postgresql+psycopg<br>접속 글"]:::tool
  envpy["사본의 env.py 12~15행<br>환경 변수로 접속 글을 정함"]
  up["try_upgrade<br>command.upgrade<br>목표 head"]:::flow
  out["판 번호 20260911_01<br>칸 id · question"]:::measure
  lab --> cpy --> envpy
  envv --> envpy
  envpy --> up --> out
```

실습 폴더를 사본으로 복사하고 환경 변수로 접속 글을 넘기자, 첫 판 20260911_01이 표 tickets를 만들었습니다.

### 03-3-기본값-없는-NOT-NULL-칸의-Before.mmd

```mermaid
flowchart TB
  %% classes
  st["판 20260911_01<br>줄 셋 환불 · 배송 · 결제"]
  rev["Before 판 20260929_02<br>칸 owner nullable=False<br>기본값 없음"]:::flow
  sql["Alembic이 보낸 SQL 글<br>ALTER TABLE …<br>ADD COLUMN owner<br>VARCHAR(50) NOT NULL"]
  tx["서버가 SQL 문장을 막음<br>판 함수가 끝나지 않아<br>판 번호를 적지 않음"]
  err["받은 오류 IntegrityError<br>NotNullViolation · 23502"]:::measure
  res["판 번호 20260911_01 그대로<br>칸 id · question 그대로"]:::fail
  st --> rev --> sql --> tx --> err --> res
```

기본값 없는 NOT NULL 칸을 더하는 SQL 문장이 막히자, 칸이 생기지 않고 판 번호도 적히지 않아 그대로 남았습니다.

### 03-4-기본값-없는-판과-서버-기본값-판-견주기.mmd

```mermaid
flowchart TB
  %% classes
  same["두 판 같음<br>판 20260911_01에서 시작<br>줄 셋이 든 표<br>둘째 판 20260929_02<br>칸 owner 더하기"]
  subgraph bf["Before · 기본값 없음"]
    direction TB
    b1["nullable=False만"]:::flow
    b2["받은 오류 IntegrityError<br>23502"]:::measure
    b3["판 번호 20260911_01<br>칸 id · question"]:::fail
    b1 --> b2 --> b3
  end
  subgraph af["After · 서버 기본값"]
    direction TB
    a1["nullable=False<br>server_default=미정"]:::flow
    a2["받은 오류 None<br>판 번호 20260929_02<br>세 줄 owner 미정"]:::measure
    a1 --> a2
  end
  same --> bf
  same --> af
```

같은 표에 같은 둘째 판을 올렸는데, 기본값 없는 Before는 첫 판에 머물고 서버 기본값을 준 After는 둘째 판까지 올라갔습니다.

### 03-5-판-내리기와-다시-올리기.mmd

```mermaid
flowchart TB
  %% classes
  s1["판 20260929_02<br>owner 민지 · 미정 · 미정"]:::measure
  dn["command.downgrade<br>목표 -1 · 칸 owner 빼기"]:::flow
  s2["판 20260911_01<br>칸 id · question · 줄 셋"]:::measure
  up2["try_upgrade<br>같은 판 파일로 다시 올리기"]:::flow
  s3["판 20260929_02<br>owner 미정 · 미정 · 미정"]:::measure
  s1 --> dn --> s2 --> up2 --> s3
```

판을 내리자 칸 owner가 값과 함께 빠졌고, 다시 올리자 1번 줄의 담당자는 민지가 아니라 미정이었습니다.

### 03-6-빈-자리-판과-마개를-꽂은-판.prompt.md

# 03-6-빈-자리-판과-마개를-꽂은-판 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 옛 전화 교환대의 판 하나를 떠올려 봅니다. 판에는 꽂는 자리가 가로 세 줄, 세로 두 줄로 놓여 있고, 자리마다 주황 꽂이가 꽂혀 있습니다. … 세로 한 줄을 더하려고 빈 자리 셋짜리 새 판을 가져왔습니다. 빈 자리는 규칙에 맞지 않아, 새 판은 붙지 못하고 앞에 놓인 채 남습니다. 옛 판은 세로 두 줄 그대로입니다. 새 판의 자리마다 회색 마개를 먼저 꽂아 오면 규칙에 맞아, 세로 세 줄짜리 판이 됩니다.

구성 요소와 배치: **왼쪽 판**(세로 두 줄 × 가로 세 줄, 주황 꽂이 여섯 — 표 `tickets`의 칸 둘·줄 셋, Before 뒤 그대로) · **왼쪽 판 앞 탁자 위 가는 판**(빈 구멍 셋 — 기본값 없는 새 칸, 붙지 못함) · **오른쪽 판**(세로 세 줄, 주황 꽂이 여섯 + 회색 마개 셋 — 서버 기본값을 채운 새 칸, After). 비유 계열 **「전화 교환대」**(01이 엶). **01·02 소품과 다르게**: 01 = 같은 갈색 나무 판 둘·금색 테두리 자리 셋·짧은 검은 곧은 선·노랑/회색 불 · 02 = 짙은 초록 금속 판 하나·은색 한 구멍 자리 여섯·파란 천 선·초록/회색 불·나무 선반 → 03 = 크림색 판 둘·검은 둥근 자리·주황 짧은 꽂이·회색 마개·회색 탁자, **선과 불 없음**. 금지 소품(콘센트·전원 플러그 등 handoff 목록) 없음. 사람·손·글자·숫자·화살표·전화기·화면 없음.

시선 순서: 왼쪽 판(세로 두 줄, 주황 꽂이 여섯) → 그 앞 탁자 위 가는 판(빈 구멍 셋, 붙지 않음) → 오른쪽 판(세로 세 줄, 셋째 줄 회색 마개 셋).

검수 기준: 그림만 보고 「세로 두 줄 판 + 붙지 못한 빈 판」과 「마개를 꽂아 세로 세 줄이 된 판」이 세어서 읽히는가. 왼쪽 판에 빈 자리가 없는가(빈 자리가 판에 붙어 있으면 「빈 칸이 붙었다」로 읽혀 Before와 반대). 오른쪽 판이 정확히 세로 세 줄인가. 선·불·콘센트·전원 플러그·글자·숫자·사람·화살표가 없는가.

## 프롬프트 (1차, 탈락)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Close-up of two old telephone switchboard panels side by side on a light grey tabletop, filling the frame. Both panels are cream-colored painted metal with rounded corners. Left panel: exactly two columns and three rows of round black jack holes, six holes in total, and every hole holds one short orange cylindrical plug sticking straight out. In front of the left panel, lying flat on the tabletop and not attached to it, one narrow cream metal strip with exactly three empty round black holes in a single column. Right panel: slightly wider, exactly three columns and three rows of round black jack holes, nine in total; the two left columns hold short orange cylindrical plugs, and the third column holds three identical small round grey caps. No cords, no wires, no lamps, no power outlets, no power plugs, no people, no hands, no arrows, no screens, no telephones.
```

## 프롬프트 (2차, 채택 — 재생성 1회)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Close-up of two old telephone switchboard panels side by side on a light grey tabletop, filling the frame. Both panels are cream-colored painted metal with rounded corners, and no panel has any empty hole. Left panel is narrow: it has only two columns of holes, three holes in each column, six in total, and every hole holds one short orange cylindrical plug sticking straight out. Right panel is wider: it has exactly three columns, three holes in each column; the first two columns hold short orange cylindrical plugs and the third column holds three identical small round grey caps. In front of the left panel, lying flat on the tabletop and not attached to anything, one narrow cream metal strip with three empty round holes in a row. No cords, no wires, no lamps, no power outlets, no power plugs, no people, no hands, no arrows, no screens, no telephones.
```

## 상태

- 2026-09-29 · `generate_image` 두 번, `params` = `{"model":"nano_banana_pro","prompt":…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `generate_image` 응답 모델 `nano_banana_pro`, **`jobs_wait` 응답 모델 표시 `nano_banana_2`**(01·02와 같은 표시, 거래 표시는 「Nano Banana Pro」 — 기록만).
- 생성 전 잔액 **2257**, 바로 앞 거래 2026-09-29T16:34:28.831637Z는 02절 몫(이 절 아님).
- **1차 job `3f28a43c-9acd-41f1-9909-c447a826efe2` 탈락** — 거래 2026-09-29T17:13:40.325207Z 「Nano Banana Pro −2」. 원본 `f243543c9f12f1c9d05f25e29caf19be5149c0f5f1d831993d99ad2ed622fa14`(2752 × 1536, RGB). 탁자 위 빈 구멍 셋짜리 판은 맞았으나, **왼쪽 판이 세로 세 줄(주황 꽂이 둘 줄 + 빈 자리 한 줄)**이라 「빈 칸이 판에 붙었다」로 읽혀 Before와 반대이고, **오른쪽 판이 세로 네 줄(주황 둘·빈 자리 하나·회색 마개 하나)**이라 셈이 맞지 않음.
- **2차 job `1f2ce2ae-15dd-40f0-9127-7bb7fcca1fef` 채택** — 거래 2026-09-29T17:14:39.983621Z 「Nano Banana Pro −2」. 원본 `01e294677d4c15efa4ca42b6868d9ccc26080909b06dc7fe0cf9f5bdb7fe1d2b`(2752 × 1536, RGB). **이 절 몫 거래 두 줄, 4크레딧**(잔액 2257 → 2253), 재생성 1회. 2차에서 효과가 있었던 문구: 「no panel has any empty hole」·「Left panel is narrow: it has only two columns」.
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕 · 옅은 회색 탁자 · 크림색 판 **둘**이 나란히 섬(오른쪽 판이 더 넓고 조금 큼) · 왼쪽 판: 세로 **두** 줄(줄마다 둥근 테두리), 줄마다 주황 둥근 꽂이 **셋** — 주황 꽂이 **여섯**, 빈 자리 0 · 왼쪽 판 앞 탁자 위: 가늘고 긴 크림색 판 **하나**가 누워 있고 빈 둥근 구멍 **셋**이 가로 한 줄, 어느 판에도 붙지 않음 · 오른쪽 판: 세로 **세** 줄(줄마다 둥근 테두리), 앞 두 줄에 주황 꽂이 **여섯**, 셋째 줄에 같은 모양의 회색 둥근 마개 **셋**, 빈 자리 0. 선·불·사람·손·글자·숫자·화살표·전화기·화면·콘센트·전원 플러그 없음.
- 검수: 「세로 두 줄 판과 붙지 못한 빈 판」·「회색 마개를 꽂아 세로 세 줄이 된 판」이 그림만으로 세어서 읽힘 → 채택. **그림과 프롬프트의 차이**: 가는 판의 구멍은 세로가 아니라 가로 한 줄(누워 있어서 — 비유 글은 「빈 자리 셋짜리 새 판」이라 맞음) · 줄마다 둥근 테두리가 더 그려짐 · 거의 흰 가로줄 64/614(위쪽 — 01의 172·02의 106보다 적음).
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch31-03/illu/r2.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/03-6-빈-자리-판과-마개를-꽂은-판.png`(1100 × 614, `d0c618371c1424aca03c1aa03c6fbf6aff0734d523bb0ef45762c6ee2ed0b99c`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`r2-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`). 저장 PNG와 바이트가 같은 사본(`.cache/ch31-03-view/r2-1100.png`·`saved-03-6.png`)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

