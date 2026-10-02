# 03-메타데이터-필터와-iterative-scan

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 3h | 코드 notebooks/03-메타데이터-필터와-iterative-scan.ipynb | 새 용어 5 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>이 절을 마치면 범주 칸을 조건으로 붙인 벡터 검색을 SQL 한 문장으로 쓸 수 있습니다.</li><li>조건에 맞는 행이 표에 있는데도 받아 온 줄이 비는 까닭을 설명할 수 있습니다.</li><li>설정 <code>hnsw.iterative_scan</code>을 바꿔 받아 온 줄 수가 어떻게 달라지는지 확인할 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>사용자별 문서나 날짜 범위, 공개 등급처럼 조건을 붙이면 검색 대상이 줄어듭니다. 그런데 색인은 가까운 후보를 먼저 고르고 조건은 그다음에 검사합니다. 조건에 맞는 문서가 표에 있어도 그 후보 안에 없으면 한 줄도 받지 못합니다.</p><p>받아 온 줄이 비었을 때 「맞는 문서가 없다」로 읽으면 잘못된 답을 만듭니다. 이 절은 그 장면을 실행으로 만들고 설정 하나로 고칩니다. 조건을 붙일 때 무엇을 함께 기록해야 하는지도 정합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>01절에서 문서 12개와 질문 8개를 숫자 256개짜리 벡터로 바꿨습니다. 첫 질문의 상위 3개는 <code>LIB-004</code>와 <code>LIB-001</code>, <code>LIB-003</code>이었습니다. 02절은 같은 벡터를 pgvector 표에 넣고 거리 연산자 <code>&lt;=&gt;</code>로 같은 순서를 받았습니다.</p><p>02절에서 색인을 만들어도 계획기가 색인 경로를 고른다고 보장하지 않는 것을 봤습니다. 행이 12개뿐인 표에서 계획기는 차례로 읽는 쪽을 골랐습니다. 그래서 이 절도 설정 <code>enable_seqscan</code>을 off로 두고 색인 경로를 봅니다.</p><p>Ch 4 03절에서 조건에 맞는 행만 고르는 <code>WHERE</code>를 배우고 값은 자리표시자로 넘겼습니다. 이 절은 그 조건을 거리 정렬과 한 문장에 함께 씁니다. Ch 11과 01·02절에서 쓴 정답 자리와 재현율, 질문 평균 함수도 그대로 이어 씁니다.</p><p>노트북은 앞에서 배운 함수 열 개를 실습 폴더의 도구 파일 <code>notebooks/rag_tools.py</code>에서 한 줄로 가져옵니다. 01절 거리 함수 두 개와 02절 데이터베이스 함수 네 개, Ch 11 지표 함수 네 개입니다. 02절 함수는 커서와 SQL을 인자로 받는 판입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>서가 두 칸에 같은 책이 같은 자리로 서 있습니다. 두 칸 모두 왼쪽에는 옅은 회색 책이 빽빽하고 오른쪽에 주황 책이 있습니다. 왼쪽 칸은 책을 잇는 끈이 회색 책에서 멈춰 있고 오른쪽 칸은 그 끈이 주황 책까지 이어져 있습니다. 끈이 멈춘 칸에서는 주황 책을 한 권도 집지 못합니다.</p>
{{img:03-5-끈과-빈-쟁반|나란히 놓인 나무 서가 두 칸에 같은 책이 같은 자리로 서 있고 왼쪽은 옅은 회색 책이며 오른쪽은 주황 책인데 왼쪽 칸은 책을 잇는 가는 끈이 회색 책에서 멈춰 있고 그 아래 나무 쟁반이 비어 있으며 오른쪽 칸은 같은 끈이 주황 책을 지나 칸 밖까지 이어져 있고 그 아래 쟁반에 주황 책이 눕혀 쌓여 있는 그림|끈이 회색 책에서 멈춘 왼쪽 칸의 쟁반은 비어 있고 끈이 주황 책까지 이어진 오른쪽 칸의 쟁반에는 주황 책이 쌓여 있습니다.}}
<p class="look"><b>그림 읽기</b> — 서가 한 칸이 표 하나이고 책 한 권이 표의 행 하나입니다. 옅은 회색 책은 조건에 맞지 않는 행이고 주황 책은 조건에 맞는 행입니다. 책과 책을 잇는 가는 끈은 색인이 미리 이어 둔 이웃 관계입니다. 왼쪽 칸은 끈이 회색 책에서 멈춰 살펴본 책이 모두 회색이라 아래 쟁반이 비어 있습니다. 오른쪽 칸은 끈이 주황 책을 지나 칸 밖까지 이어지고 아래 쟁반에 주황 책이 쌓여 있습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>메타데이터 필터(metadata filter)</td><td>범주나 날짜, 권한처럼 벡터 밖의 칸 값으로 행을 제한하는 조건입니다.</td></tr><tr><td>나중 걸러 내기(post-filtering)</td><td>색인이 고른 후보에 조건을 그다음에 적용하는 처리입니다.</td></tr><tr><td>선택도(selectivity)</td><td>표의 전체 행 가운데 조건을 통과하는 행의 비율입니다.</td></tr><tr><td>반복 탐색(iterative scan)</td><td>필요한 줄을 얻거나 볼 줄 수 한도에 이를 때까지 색인을 더 살펴보는 기능입니다. 설정 이름은 <code>hnsw.iterative_scan</code>이고 값은 <code>off</code>와 <code>strict_order</code>, <code>relaxed_order</code> 세 가지입니다.</td></tr><tr><td>채움 행</td><td>걸러 내는 순서를 보려고 질문 벡터를 본떠 규칙으로 만든 행입니다. 이 절에서만 쓰는 연습용 행입니다.</td></tr></tbody></table>
{{mermaid:03-1-후보를-고른-뒤-조건-검사|위에서 아래로 내려가는 흐름도로 초록 상자 표 ch12_core_filter 412행에서 파란 상자 색인이 가까운 후보부터 고르기 후보 목록 크기 40과 파란 상자 범주 조건을 나중에 검사와 파란 상자 조건을 통과한 줄만 남기기를 지나 맨 아래 노란 상자 받아 온 줄 수가 받아 올 줄 수보다 적어짐으로 이어지는 그림|색인 경로는 가까운 후보를 먼저 고르고 범주 조건을 나중에 검사하므로 받아 온 줄 수가 받아 올 줄 수보다 적어질 수 있습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 초록 상자가 이 절에서 만드는 표입니다. 그 아래 파란 상자 세 개가 색인 경로의 처리 순서이고 위에서 아래로 읽습니다. 조건 검사가 후보를 고른 다음에 온다는 점이 이 절의 핵심입니다. 맨 아래 노란 상자는 노트북 출력으로 확인한 결과입니다.</p>
<h3>조건을 붙인 검색이 비는 까닭</h3><p>색인 경로는 표의 행을 모두 보지 않습니다. 설정 <code>hnsw.ef_search</code>가 정한 크기만큼 후보를 고르고 그 후보만 넘깁니다. 넘어온 후보에 조건 검사를 적용하면 통과한 줄이 받아 올 줄 수보다 적을 수 있습니다.</p><p>통과 비율이 낮을수록 이 일이 자주 생깁니다. 이 절의 표는 412행인데 조건 <code>category = 'library'</code>를 통과하는 행이 4개뿐입니다. 후보 40개가 모두 다른 범주였다면 받아 온 줄은 0개입니다.</p>
<h3>반복 탐색이 하는 일</h3><p>설정 <code>hnsw.iterative_scan</code>은 후보가 모자랄 때 색인을 더 살펴보게 합니다. 값 <code>strict_order</code>는 받아 온 줄을 거리 순서대로 냅니다. 값 <code>relaxed_order</code>는 순서가 조금 달라질 수 있는 대신 줄을 더 받을 수 있습니다.</p><p>더 살펴보는 일도 끝이 있습니다. 설정 <code>hnsw.max_scan_tuples</code>가 볼 줄 수 한도를 정하고 노트북 출력에서 기본값 <code>20000</code>을 확인했습니다. 그래서 반복 탐색을 켜도 받아 올 줄 수를 늘 채운다고 볼 수 없습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>01절과 같은 문서 12개를 범주 칸과 함께 표 <code>ch12_core_filter</code>에 넣습니다. 질문 벡터를 본떠 규칙으로 만든 채움 행 400개도 같은 표에 넣습니다. 채움 행은 질문 벡터에서 숫자 한 개만 조금 키운 벡터라 질문에 아주 가깝습니다.</p><p>이 합성 자료는 걸러 내는 순서를 보려고 만든 것이고 임베딩 품질을 나타내지 않습니다. 설정 <code>enable_seqscan</code>을 off로 두어 색인 경로로 읽게 하고, 조건은 <code>category = 'library'</code>, 받아 올 줄 수는 3으로 고정합니다. 임베딩 요청은 문서 한 번과 질문 여덟 번으로 모두 아홉 번입니다.</p>
{{mermaid:03-2-표에-넣은-두-가지-행|위에서 아래로 내려가는 흐름도로 초록 상자 질문 8개에서 규칙으로 벡터 만들기 화살표를 지나 초록 상자 채움 행 400개로 가고 초록 상자 교육용 문서 12개에서 임베딩 요청 1번 화살표를 지나 초록 상자 문서 벡터 12개로 간 뒤 두 갈래가 초록 상자 표 ch12_core_filter 412행에 모이고 CREATE INDEX 화살표를 지나 초록 상자 HNSW 색인으로 갔다가 맨 아래 노란 상자 범주별 행 수로 이어지는 그림|질문에서 규칙으로 만든 채움 행 400개와 교육용 문서 벡터 12개를 한 표에 넣어 412행으로 만들고 그 벡터 칸에 HNSW 색인을 만듭니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 왼쪽 갈래가 채움 행이고 오른쪽 갈래가 교육용 문서입니다. 초록 상자 여섯 개가 이 절에서 만드는 자료와 표, 색인입니다. 화살표 라벨은 그 단계에서 하는 일과 실행하는 SQL 문장입니다. 맨 아래 노란 상자는 범주마다 세어 본 행 수입니다.</p>
{{notebook:03-메타데이터-필터와-iterative-scan|example}}
{{mermaid:03-3-두-경로의-질문-평균|가로축이 자리 1과 자리 2와 자리 3이고 세로축이 질문 평균 재현율 0에서 1까지인 꺾은선 그림으로 초록 선은 자리 1에서 0.75이고 자리 2와 자리 3에서 0.875로 올라가며 주황 선은 세 자리 모두 0.375로 평평한 그림|초록 선 정확 검색은 자리 1에서 0.75와 자리 3에서 0.875인데 주황 선 색인 경로는 세 자리 모두 0.375입니다.}}
<p class="look"><b>도식 읽기</b> — 가로축이 자르는 자리이고 세로축이 질문 평균 재현율입니다. 초록 선은 파이썬으로 낸 정확 검색이고 주황 선은 색인 경로입니다. 초록 선은 자리를 늘리면 <code>0.75</code>에서 <code>0.875</code>로 올라갑니다. 주황 선은 세 자리 모두 <code>0.375</code>로 평평합니다. 받아 온 줄이 없으면 자르는 자리를 늘려도 값이 오르지 않기 때문입니다.</p>
<p class="look"><b>확인할 점</b> — 표에 들어간 행은 412개이고 조건을 통과하는 행은 4개입니다. 필터 없는 검색의 상위 3개는 모두 채움 행이고 거리가 <code>0.0</code>입니다. 정확 검색 상위 3개는 <code>1 | LIB-004 | 0.43</code>과 <code>2 | LIB-001 | 0.56</code>, <code>3 | LIB-003 | 0.62</code>로 01·02절과 같은 값입니다. 색인 경로는 질문 여덟 개 가운데 한 질문도 받아 올 줄 수 3을 채우지 못했습니다.</p>
<h2 id="b6"><span class="no">6</span>실패 확인</h2><p>아래 Before 셀은 반복 탐색이 꺼진 기본 설정에서 첫 질문에 범주 조건을 붙여 검색합니다. 조건을 통과하는 문서가 네 건 있는데도 받아 온 줄 수가 0이었습니다. 이어지는 After 셀은 자료와 질문, 조건, 받아 올 줄 수, 후보 목록 크기를 그대로 둡니다. 설정 <code>hnsw.iterative_scan</code>만 <code>strict_order</code>로 바꿉니다.</p>
{{notebook:03-메타데이터-필터와-iterative-scan|failure}}
{{mermaid:03-4-설정-하나만-바꾼-뒤|나란히 놓인 두 칸의 흐름도로 왼쪽 반복 탐색 off 칸에서는 파란 상자 같은 필터 검색 SQL이 빨간 상자 받아 온 줄 수 0으로 내려가고 오른쪽 반복 탐색 strict_order 칸에서는 같은 파란 상자가 노란 상자 받아 온 줄 수 3과 문서 LIB-004와 LIB-001과 LIB-003으로 내려가며 두 칸이 맨 아래 회색 상자 두 칸의 SQL과 넘긴 값은 같고 받아 온 줄 수만 갈림으로 모이는 그림|설정 하나만 off에서 strict_order로 바꾸니 받아 온 줄 수가 0에서 3으로 늘고 그 칸의 세 문서가 정확 검색 상위 세 개와 같아집니다.}}
<p class="look"><b>도식 읽기</b> — 두 칸의 제목이 바꾼 설정 값입니다. 왼쪽 칸이 반복 탐색 off이고 오른쪽 칸이 반복 탐색 <code>strict_order</code>입니다. 두 칸의 파란 상자는 같은 SQL 한 문장이고 넘긴 값도 같습니다. 왼쪽 칸의 빨간 상자가 Before가 받은 결과이고 오른쪽 칸의 노란 상자가 After가 받은 결과입니다. 맨 아래 회색 상자는 두 칸에서 모두 확인한 사실입니다.</p>
<p>받지 못한 까닭은 조건에 맞는 문서가 없어서가 아니라 후보를 고르는 폭이 좁아서입니다. 값 <code>relaxed_order</code>로 한 번 더 실행했을 때도 같은 세 줄을 같은 순서로 받았습니다. 조건에 맞는 문서가 네 건뿐이라 두 값의 차이가 드러나지 않았습니다. 큰 자료에서 두 값을 견주는 일은 이번에 실행하지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>받아 온 줄 수가 0이라고 조건에 맞는 문서가 없다고 볼 수 없습니다. 조건을 통과하는 행 수를 <code>count(*)</code>로 따로 세어 봅니다.</li><li>조건을 붙인 검색은 받아 올 줄 수와 함께 받아 온 줄 수를 기록합니다. 이 절 기록 한 줄에도 <code>받아 온 줄 수</code> 칸을 두었습니다.</li><li>반복 탐색을 켜도 받아 올 줄 수를 늘 채운다고 볼 수 없습니다. 노트북 출력의 <code>반복 탐색이 볼 줄 수 한도: 20000</code>이 그 한도이고 조건을 통과하는 행 수도 함께 봅니다.</li><li>이 절은 첫 질문 하나로만 반복 탐색을 확인했습니다. 반복 탐색을 켠 채로 질문 여덟 개를 모두 재는 일은 이번에 실행하지 않았습니다.</li><li>채움 행 수와 바꿀 숫자의 크기는 탐색 실행 뒤 정했습니다. 질문마다 50개씩 만들어 모두 400개로 두면 여덟 질문 모두 후보가 채움 행으로 찼습니다. 흐름을 보여 주려고 정한 예이고 실제 말뭉치의 비율이 아닙니다.</li><li>이 절은 검색 시간을 재지 않았습니다. 반복 탐색은 색인을 더 살펴보므로 걸린 시간이 늘 수 있고, 그 값은 함께 재야 합니다.</li><li>통과 비율이 아주 낮을 때 쓰는 다른 방법도 있습니다. 조건 칸에 만드는 색인이나 조건을 미리 걸어 만드는 색인, 표를 나누는 방법이 그렇고 이번에 실행하지 않았습니다.</li><li>교재 출력은 pgvector 0.8.1이 든 PostgreSQL 17.11에서 만들었습니다. 실습 폴더 안내는 <code>pgvector/pgvector:0.8.2-pg17</code> 이미지를 씁니다. 그 이미지에서는 확장 판이 0.8.2입니다. 이번 교재 출력은 그 환경에서 만들지 않았습니다. 판 번호가 달라도 이 절에서 쓰는 기능은 같습니다.</li><li>같은 SQL을 여러 번 실행하면 psycopg가 그 문장을 미리 준비해 두고 계획을 다시 씁니다. 그래서 이 절은 <code>enable_seqscan</code>을 절 안에서 다시 켜지 않고 색인 경로로만 실행합니다.</li><li>이 절은 파일을 쓰지 않습니다. 만든 표 <code>ch12_core_filter</code>는 지우지 않고 그대로 남깁니다.</li><li>이 절의 문서 12개와 질문 8개는 01·02절과 같은 교육용 자료입니다. 채움 행이 섞여 있어 01·02절 재현율과 이 절 색인 경로 값을 같은 뜻으로 읽지 않습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>색인 경로는 후보를 먼저 고르고 조건을 나중에 검사하므로 받아 온 줄이 비거나 모자랄 수 있습니다.</li><li>이번 실행에서는 자리 1에서 정확 검색 <code>0.75</code>에 색인 경로 <code>0.375</code>였고 색인 경로는 세 자리가 모두 같았습니다.</li><li>설정 <code>hnsw.iterative_scan</code>만 <code>strict_order</code>로 바꾸니 세 줄을 받고 정확 검색 상위 3개와 같았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 04절에서는 벡터 거리가 아니라 한국어 낱말로 문서를 찾습니다. 형태소 분석기로 낱말을 가르고 낱말이 겹치는 정도로 순위를 냅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 받아 올 줄 수를 3으로 주었는데 받아 온 줄 수가 0일 수 있는 까닭은 무엇입니까?</p><p class="quiz-a">색인이 먼저 고른 후보에 조건 검사를 나중에 적용해 통과한 줄이 없을 수 있기 때문입니다. 틀렸다면 「조건을 붙인 검색이 비는 까닭」을 다시 읽습니다.</p><p class="quiz-q">2. 설정 <code>hnsw.iterative_scan</code>의 값 <code>strict_order</code>는 무엇을 지킵니까?</p><p class="quiz-a">받아 온 줄을 거리 순서대로 내는 것을 지킵니다. 값 <code>relaxed_order</code>는 순서가 조금 달라질 수 있습니다. 틀렸다면 「반복 탐색이 하는 일」을 다시 읽습니다.</p><p class="quiz-q">3. Before와 After에서 바꾼 것은 무엇입니까?</p><p class="quiz-a">설정 <code>hnsw.iterative_scan</code> 하나를 off에서 <code>strict_order</code>로 바꿨습니다. 자료와 질문, 조건, 받아 올 줄 수, 후보 목록 크기는 그대로입니다. 틀렸다면 「실패 확인」을 다시 읽습니다.</p><p class="quiz-q">4. 반복 탐색을 켰으므로 받아 올 줄 수를 늘 채운다고 말할 수 있습니까?</p><p class="quiz-a">말할 수 없습니다. 볼 줄 수 한도가 있고 조건을 통과하는 행 수 자체가 적을 수 있습니다. 틀렸다면 「주의할 점과 실무 메모」를 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://github.com/pgvector/pgvector/tree/v0.8.6#iterative-index-scans">pgvector Iterative Index Scans</a></div>반복 탐색 설정과 볼 줄 수 한도 설명 · 확인 2026-09-18</li><li><div><a href="https://github.com/pgvector/pgvector/tree/v0.8.6#filtering">pgvector Filtering</a></div>조건을 붙인 검색과 색인 고르기 설명 · 확인 2026-09-18</li><li><div><a href="https://www.postgresql.org/docs/17/using-explain.html">PostgreSQL Using EXPLAIN</a></div>실행 계획 읽는 법 · 확인 2026-09-18</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# 메타데이터 필터와 iterative scan

**이 노트북에서 할 일**

1. 01절과 같은 문서 12개와 규칙으로 만든 채움 행 400개를 한 표에 넣습니다.
2. 범주 조건을 붙인 검색이 받아 올 줄 수를 채우지 못하는 장면을 봅니다.
3. 질문 여덟 개를 정확 검색과 색인 경로로 재어 재현율을 견줍니다.
4. 설정 `hnsw.iterative_scan`만 바꿔 같은 검색을 다시 실행합니다.

**준비물** — 프로젝트 맨 위 `.env` 파일의 `OPENAI_API_KEY`가 필요합니다.
pgvector 확장이 든 PostgreSQL이 `127.0.0.1:55432`에서 켜져 있어야 합니다.
실습 폴더 `README.md`의 Docker 명령으로 데이터베이스를 먼저 켭니다.
읽는 자료는 01·02절과 같은 문서 파일과 질문 파일 두 개입니다.

임베딩 요청은 문서 한 번과 질문 여덟 번으로 모두 아홉 번입니다.
보내는 글은 900자 아래이고 예상 비용은 0.01달러 아래입니다.
실행 시간은 60초 안팎입니다.

**데이터** — 두 파일 모두 실습 묶음에 들어 있습니다.

- 문서 `labs/part3/ch12-retrieval-tuning/data/core-documents.json`(12개)
- 질문 `labs/part3/ch12-retrieval-tuning/data/core-queries.json`(8개)

**강의와 실습 범위** — 강의 시간에는 5~7절과 9~11절, 14~16절을 읽습니다.
정답 문서의 범주 찾기, 채움 행 만들기, 표에 넣고 색인 만들기입니다.
이어서 실행 1과 색인 경로 설정, 정확 검색 상위 세 개를 봅니다.
14~16절은 Before와 After, 값 바꿔 보기입니다.
2~4절과 8절, 12~13절은 함께 실행하고 실습 시간에 다시 읽습니다.

**기준 버전** — 첫 셀에서 psycopg 3.3.5와 python-dotenv 1.2.3을 설치합니다.
패키지 langchain-openai 1.6.1과 numpy 2.5.3도 함께 설치합니다.
데이터베이스는 pgvector 확장이 든 PostgreSQL 17을 씁니다.
필수 최소는 pgvector 0.8.0입니다. 반복 탐색 설정이 그 판에서 생겼습니다.

교재 출력은 PostgreSQL 17.11과 pgvector 0.8.1에서 만들었습니다.
실습 폴더 안내대로 Docker 이미지를 쓰면 확장 판 번호가 0.8.2로 나옵니다.
참고 자료로 적은 공식 문서는 v0.8.6 기준입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch12-retrieval-tuning`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 내려가는 흐름도로 초록 상자 표 ch12_core_filter 412행에서 파란 상자 색인이 가까운 후보부터 고르기 후보 목록 크기 40과 파란 상자 범주 조건을 나중에 검사와 파란 상자 조건을 통과한 줄만 남기기를 지나 맨 아래 노란 상자 받아 온 줄 수가 받아 올 줄 수보다 적어짐으로 이어지는 그림](attachment:03-1-후보를-고른-뒤-조건-검사.png)

맨 위 초록 상자가 이 절에서 만드는 표이고 파란 상자 세 개가 색인 경로의 처리 순서입니다.
위에서 아래로 읽습니다. 조건 검사가 후보를 고른 다음에 옵니다.
맨 아래 노란 상자는 이 노트북의 출력으로 확인한 결과입니다.

### [2] markdown {}

## 1. 준비

첫 셀은 패키지 네 개를 설치하고 설치된 버전을 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:12.127073Z', 'iopub.status.busy': '2026-09-21T07:40:12.126859Z', 'iopub.status.idle': '2026-09-21T07:40:12.633216Z', 'shell.execute_reply': '2026-09-21T07:40:12.632568Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "psycopg[binary]==3.3.5" "python-dotenv==1.2.3" "langchain-openai==1.6.1" "numpy==2.5.3"
from importlib.metadata import version

print("psycopg:", version("psycopg"))
print("python-dotenv:", version("python-dotenv"))
print("langchain-openai:", version("langchain-openai"))
print("numpy:", version("numpy"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
psycopg: 3.3.5
python-dotenv: 1.2.3
langchain-openai: 1.6.1
numpy: 2.5.3

```

### [4] markdown {}

**결과 읽기** — 설치가 끝나면 `psycopg: 3.3.5`와 `python-dotenv: 1.2.3`이 보입니다.
출력에는 `langchain-openai: 1.6.1`과 `numpy: 2.5.3`도 함께 보입니다. 네 줄이 모두 보이면 다음 셀로 넘어갑니다.
패키지 NumPy는 도구 파일이 코사인 거리를 계산할 때 씁니다.

다음 셀은 이 절에서 쓸 이름을 불러옵니다. 패키지 이름은 02절과 같은 세 개입니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 01·02절 함수 여섯 개와 Ch 11 지표 함수 네 개를 가져옵니다.
01절 `cosine_distance()`·`rank_by_distance()`, 02절 `run_search()`·`print_hits()`·`find_scan_line()`·`set_seqscan()`입니다.
Ch 11 함수는 `unique_doc_ids()`·`find_gold_rank()`·`recall_at()`·`mean_score()`입니다.
인자 모양이 앞 절 판과 다른 함수는 쓰는 자리에서 설명합니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:12.634446Z', 'iopub.status.busy': '2026-09-21T07:40:12.634341Z', 'iopub.status.idle': '2026-09-21T07:40:13.673323Z', 'shell.execute_reply': '2026-09-21T07:40:13.673137Z'}, 'lesson_role': 'setup'}

```python
# 자료 파일 읽기·데이터베이스 접속·임베딩에 쓸 이름을 불러옵니다
import json

import psycopg
from langchain_openai import OpenAIEmbeddings
# 01·02절과 Ch 11 01·02절 함수 열 개를 도구 파일에서 가져옵니다
from rag_tools import cosine_distance, find_gold_rank, find_scan_line, mean_score, print_hits
from rag_tools import rank_by_distance, recall_at, run_search, set_seqscan, unique_doc_ids

print("불러온 이름:", "json", "psycopg", "OpenAIEmbeddings")
```

출력:
```
불러온 이름: json psycopg OpenAIEmbeddings

```

### [6] markdown {}

**결과 읽기** — 출력 줄은 `불러온 이름: json psycopg OpenAIEmbeddings` 하나입니다.
도구 파일에서 가져온 함수 열 개는 출력하지 않습니다.

다음 셀은 API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:13.675955Z', 'iopub.status.busy': '2026-09-21T07:40:13.675856Z', 'iopub.status.idle': '2026-09-21T07:40:13.679433Z', 'shell.execute_reply': '2026-09-21T07:40:13.679279Z'}, 'lesson_role': 'setup'}

```python
# .env 파일에서 OpenAI API 키를 읽습니다(키 값은 출력하지 않습니다)
import os
from dotenv import find_dotenv, load_dotenv

env_path = find_dotenv(usecwd=True)
load_dotenv(env_path)
has_key = os.getenv("OPENAI_API_KEY") is not None
print("OPENAI_API_KEY 설정 여부:", has_key)
assert has_key, "프로젝트 폴더의 .env 파일에 OPENAI_API_KEY를 적어 주세요."
```

출력:
```
OPENAI_API_KEY 설정 여부: True

```

### [8] markdown {}

**결과 읽기** — 출력 줄은 `OPENAI_API_KEY 설정 여부: True`입니다.
키 값은 출력하지 않습니다.

다음 셀은 프로젝트 맨 위 폴더를 찾습니다. 01·02절과 같은 코드입니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:13.679917Z', 'iopub.status.busy': '2026-09-21T07:40:13.679842Z', 'iopub.status.idle': '2026-09-21T07:40:13.681384Z', 'shell.execute_reply': '2026-09-21T07:40:13.681241Z'}, 'lesson_role': 'setup'}

```python
# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch12-retrieval-tuning/data"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."
```

출력:
```
고른 경로: .

```

### [10] markdown {}

**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. `assert`도 통과했습니다.

다음 셀은 01·02절이 쓴 문서 파일과 질문 파일을 그대로 읽습니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:13.681798Z', 'iopub.status.busy': '2026-09-21T07:40:13.681727Z', 'iopub.status.idle': '2026-09-21T07:40:13.683848Z', 'shell.execute_reply': '2026-09-21T07:40:13.683705Z'}, 'lesson_role': 'setup'}

```python
# 01·02절과 같은 문서 파일과 질문 파일을 불러옵니다
data_path = root_path + "/labs/part3/ch12-retrieval-tuning/data"
with open(data_path + "/core-documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/core-queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))
```

출력:
```
문서 수: 12
질문 수: 8

```

### [12] markdown {}

**결과 읽기** — `문서 수: 12`와 `질문 수: 8`이 보입니다.
문서 열두 개는 범주가 세 가지이고 범주마다 네 건입니다.
이 절은 그 범주 칸을 검색 조건으로 씁니다.

## 2. 데이터베이스에 붙기

접속 글에는 사용자 이름과 암호, 서버 주소와 포트, 데이터베이스 이름이 들어갑니다.
이 암호는 수업 전용이라 다른 곳에 쓰지 않습니다. 접속 글은 출력하지 않습니다.
표 이름은 02절 표와 다른 `ch12_core_filter`입니다. 이 절은 새 표를 따로 만듭니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:13.684251Z', 'iopub.status.busy': '2026-09-21T07:40:13.684181Z', 'iopub.status.idle': '2026-09-21T07:40:13.685529Z', 'shell.execute_reply': '2026-09-21T07:40:13.685395Z'}}

```python
# 데이터베이스 접속 글과 이 절에서 쓸 표·색인 이름을 정합니다
database_url = "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab"
table_name = "ch12_core_filter"
index_name = "ch12_core_filter_idx"
print("표 이름:", table_name)
print("색인 이름:", index_name)
```

출력:
```
표 이름: ch12_core_filter
색인 이름: ch12_core_filter_idx

```

### [14] markdown {}

**결과 읽기** — `표 이름: ch12_core_filter`와 `색인 이름: ch12_core_filter_idx`가 보입니다.
이 절은 새 표를 만들고 02절 표는 건드리지 않습니다.

다음 셀은 벡터의 숫자 개수와 받아 올 줄 수, 자르는 자리를 정합니다.
숫자 `256`은 01·02절과 같은 벡터의 숫자 개수입니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:13.685899Z', 'iopub.status.busy': '2026-09-21T07:40:13.685859Z', 'iopub.status.idle': '2026-09-21T07:40:13.687212Z', 'shell.execute_reply': '2026-09-21T07:40:13.687075Z'}}

```python
# 벡터의 숫자 개수와 받아 올 줄 수, 자르는 자리를 정합니다
vector_dimensions = 256
top_three = 3
cutoff_values = [1, 2, 3]
print("벡터의 숫자 개수:", vector_dimensions)
print("받아 올 줄 수:", top_three)
print("자르는 자리 세 가지:", cutoff_values)
```

출력:
```
벡터의 숫자 개수: 256
받아 올 줄 수: 3
자르는 자리 세 가지: [1, 2, 3]

```

### [16] markdown {}

**결과 읽기** — `벡터의 숫자 개수: 256`과 `받아 올 줄 수: 3`이 보입니다.
출력 줄 `자르는 자리 세 가지: [1, 2, 3]`의 값은 뒤에서 재현율을 낼 때 씁니다.

다음 셀은 채움 행을 만드는 규칙과 이름을 정합니다.
채움 행은 필터가 걸리는 순서를 보려고 규칙으로 만드는 행입니다.
값 `0.02`와 `0.0001`은 채움 벡터의 숫자 하나를 얼마나 바꿀지 정한 기준입니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:13.687586Z', 'iopub.status.busy': '2026-09-21T07:40:13.687514Z', 'iopub.status.idle': '2026-09-21T07:40:13.689078Z', 'shell.execute_reply': '2026-09-21T07:40:13.688938Z'}}

```python
# 채움 행을 만드는 규칙과 범주 이름·경로 이름을 정합니다
filler_per_query = 50
shift_base = 0.02
shift_step = 0.0001
filler_category = "other"
category_names = ["library", "facility", "account", "other"]
path_names = ["정확 검색", "색인 경로"]
print("질문마다 만드는 채움 행 수:", filler_per_query)
print("채움 행의 숫자를 바꿀 기준과 간격:", shift_base, shift_step)
print("범주 이름 네 가지:", category_names)
print("견줄 경로 두 가지:", path_names)
```

출력:
```
질문마다 만드는 채움 행 수: 50
채움 행의 숫자를 바꿀 기준과 간격: 0.02 0.0001
범주 이름 네 가지: ['library', 'facility', 'account', 'other']
견줄 경로 두 가지: ['정확 검색', '색인 경로']

```

### [18] markdown {}

**결과 읽기** — `질문마다 만드는 채움 행 수: 50`이 보입니다.
`범주 이름 네 가지: ['library', 'facility', 'account', 'other']` 줄에서 앞 세 가지가 문서의 범주입니다.
마지막 `other`는 채움 행에 붙일 범주입니다.
`견줄 경로 두 가지: ['정확 검색', '색인 경로']` 줄의 두 이름으로 뒤에서 기록을 나눕니다.

다음 셀은 데이터베이스에 붙습니다. 02절과 같은 방법입니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:13.689454Z', 'iopub.status.busy': '2026-09-21T07:40:13.689416Z', 'iopub.status.idle': '2026-09-21T07:40:13.698257Z', 'shell.execute_reply': '2026-09-21T07:40:13.698055Z'}}

```python
# 데이터베이스에 붙어 pgvector 확장을 켜고 두 판 번호를 봅니다
conn = psycopg.connect(database_url, autocommit=True)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
cur.execute("SELECT current_setting('server_version')")
print("PostgreSQL 판:", cur.fetchone()[0])
cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
print("pgvector 확장 판:", cur.fetchone()[0])
```

출력:
```
PostgreSQL 판: 17.11
pgvector 확장 판: 0.8.1

```

### [20] markdown {}

**결과 읽기** — `PostgreSQL 판: 17.11`과 `pgvector 확장 판: 0.8.1`이 보입니다.
교재 출력을 만든 데이터베이스의 확장 판은 위 줄에 보이는 번호입니다.
실습 폴더 안내대로 Docker 이미지를 쓰면 확장 판 번호가 0.8.2로 나옵니다.
판 번호가 달라도 이 절에서 쓰는 기능은 같습니다.

## 3. 문서와 질문을 벡터로 바꾸기

01·02절과 같은 모델과 같은 숫자 개수로 벡터를 만듭니다.
같은 벡터를 써야 01·02절 순위와 대조할 수 있습니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:13.701188Z', 'iopub.status.busy': '2026-09-21T07:40:13.701136Z', 'iopub.status.idle': '2026-09-21T07:40:14.082102Z', 'shell.execute_reply': '2026-09-21T07:40:14.081677Z'}}

```python
# 01·02절과 같은 임베딩 모델과 벡터의 숫자 개수를 씁니다(요청은 아직 보내지 않습니다)
embedding_model_name = "text-embedding-3-small"
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
```

출력:
```
임베딩 모델 이름: text-embedding-3-small
벡터의 숫자 개수 설정: 256

```

### [22] markdown {}

**결과 읽기** — `임베딩 모델 이름: text-embedding-3-small`과 `벡터의 숫자 개수 설정: 256`이 보입니다.
이 셀은 객체만 만들므로 요청을 보내지 않습니다.
이 노트북의 출력은 2026-09-21에 이 모델로 실행한 결과입니다.

다음 셀은 문서 12개를 한 번에 임베딩합니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:14.082901Z', 'iopub.status.busy': '2026-09-21T07:40:14.082818Z', 'iopub.status.idle': '2026-09-21T07:40:14.356398Z', 'shell.execute_reply': '2026-09-21T07:40:14.355429Z'}}

```python
# 문서 12개의 제목과 본문을 이어 붙여 한 번에 임베딩합니다(임베딩 요청 1번)
doc_texts = []
doc_ids = []
for doc in docs:
    doc_texts.append(doc["title"] + " " + doc["text"])
    doc_ids.append(doc["doc_id"])
doc_vectors = embedding_model.embed_documents(doc_texts)
print("문서 벡터 수:", len(doc_vectors))
print("첫 문서 벡터의 숫자 개수:", len(doc_vectors[0]))
```

출력:
```
문서 벡터 수: 12
첫 문서 벡터의 숫자 개수: 256

```

### [24] markdown {}

**결과 읽기** — `문서 벡터 수: 12`와 `첫 문서 벡터의 숫자 개수: 256`이 보입니다.
문서 열두 개를 한 번에 보냈으므로 임베딩 요청은 한 번입니다.

다음 셀은 질문 8개를 하나씩 임베딩합니다.
질문 벡터는 채움 행을 만들 때와 검색할 때 모두 씁니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:14.358191Z', 'iopub.status.busy': '2026-09-21T07:40:14.358046Z', 'iopub.status.idle': '2026-09-21T07:40:15.533308Z', 'shell.execute_reply': '2026-09-21T07:40:15.529460Z'}}

```python
# 질문 8개를 하나씩 임베딩해 질문 벡터 목록을 만듭니다(임베딩 요청 8번)
query_vectors = []
for query in queries:
    query_vectors.append(embedding_model.embed_query(query["question"]))
first_question_vector = query_vectors[0]
print("질문 벡터 수:", len(query_vectors))
print("첫 질문:", queries[0]["qid"], "|", queries[0]["question"])
```

출력:
```
질문 벡터 수: 8
첫 질문: C01 | 책을 빌릴 수 있는 기간은 며칠인가요?

```

### [26] markdown {}

**결과 읽기** — `질문 벡터 수: 8`이 보입니다.
`첫 질문: C01 | 책을 빌릴 수 있는 기간은 며칠인가요?`도 보입니다.
질문은 하나씩 보내므로 요청이 여덟 번입니다. 여기까지 요청은 모두 아홉 번입니다.

## 4. 01절 거리 함수 이어 쓰기

01절에서 만든 함수 `cosine_distance()`를 준비 셀에서 가져왔습니다.
코사인 거리는 코사인 유사도를 가장 큰 값 1에서 뺀 값이고 작을수록 가깝습니다.
이 절에서 쓸 pgvector의 `<=>` 연산자가 내는 값도 같은 코사인 거리입니다.
6절에서 채움 행이 문서보다 질문에 가까운지 이 함수로 확인합니다.

## 5. 정답 문서의 범주 찾기

질문 파일은 정답 문서 ID만 적고 범주는 적지 않습니다.
그래서 문서 파일에서 그 문서를 찾아 범주 이름을 읽습니다.
이 범주가 검색에 걸 조건이 됩니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.535735Z', 'iopub.status.busy': '2026-09-21T07:40:15.535618Z', 'iopub.status.idle': '2026-09-21T07:40:15.537940Z', 'shell.execute_reply': '2026-09-21T07:40:15.537516Z'}}

```python
# 문서 ID를 받아 그 문서의 범주 이름을 반환하는 함수를 정의합니다
def find_category(doc_id):
    category_name = ""
    for doc in docs:
        if doc["doc_id"] == doc_id:
            category_name = doc["category"]
            break
    return category_name
```

출력:
```

```

### [28] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
빈 글로 시작해 문서를 찾으면 바꾸고 `break`로 멈춥니다. Ch 11 01절과 같은 모양입니다.

다음 셀은 첫 질문의 정답 문서와 그 범주를 봅니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.538643Z', 'iopub.status.busy': '2026-09-21T07:40:15.538594Z', 'iopub.status.idle': '2026-09-21T07:40:15.541023Z', 'shell.execute_reply': '2026-09-21T07:40:15.540111Z'}}

```python
# 첫 질문의 정답 문서가 어느 범주에 있는지 찾습니다
first_gold_doc_id = queries[0]["gold_doc_id"]
first_category = find_category(first_gold_doc_id)
print("첫 질문의 정답 문서 ID:", first_gold_doc_id)
print("그 문서의 범주:", first_category)
```

출력:
```
첫 질문의 정답 문서 ID: LIB-001
그 문서의 범주: library

```

### [30] markdown {}

**결과 읽기** — `첫 질문의 정답 문서 ID: LIB-001`과 `그 문서의 범주: library`가 보입니다.
첫 질문에 답하는 문서가 범주 `library`에 있다는 뜻입니다.
이 절은 그 질문에 `library` 조건을 붙여 검색합니다.

## 6. 채움 행 만들기

나중 걸러 내기를 보려면 조건에 맞지 않는 행이 질문에 더 가까워야 합니다.
그래서 질문 벡터를 본떠 아주 가까운 벡터를 규칙으로 만듭니다.
메서드 `copy()`는 목록을 하나 더 만듭니다. Ch 2 03절에서 배운 이름입니다.
기호 `%`는 나눈 뒤 남는 값을 내고 숫자 개수보다 큰 번호도 칸 번호로 바꿉니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.542618Z', 'iopub.status.busy': '2026-09-21T07:40:15.542466Z', 'iopub.status.idle': '2026-09-21T07:40:15.545842Z', 'shell.execute_reply': '2026-09-21T07:40:15.545101Z'}}

```python
# 질문 벡터 하나에서 아주 가까운 채움 벡터를 규칙으로 만들어 목록으로 반환합니다
def make_filler_vectors(base_vector, count):
    vectors = []
    for number in range(count):
        vector = base_vector.copy()
        # 반복 번호를 숫자 개수로 나눈 나머지 자리 하나만 조금 키웁니다
        position = number % vector_dimensions
        vector[position] = vector[position] + shift_base + shift_step * number
        vectors.append(vector)
    return vectors
```

출력:
```

```

### [32] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
난수를 쓰지 않으므로 다시 실행해도 같은 채움 벡터가 나옵니다.

다음 셀은 질문 여덟 개마다 채움 벡터를 만들어 한 목록에 모읍니다.
질문마다 만드는 까닭은 질문이 바뀌어도 가까운 채움 행이 있게 하려는 것입니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.547847Z', 'iopub.status.busy': '2026-09-21T07:40:15.547693Z', 'iopub.status.idle': '2026-09-21T07:40:15.551585Z', 'shell.execute_reply': '2026-09-21T07:40:15.551091Z'}}

```python
# 질문 여덟 개마다 채움 벡터 50개를 만들어 한 목록에 모읍니다
filler_vectors = []
for query_index in range(len(queries)):
    made_vectors = make_filler_vectors(query_vectors[query_index], filler_per_query)
    for vector in made_vectors:
        filler_vectors.append(vector)
print("채움 벡터 수:", len(filler_vectors))
print("첫 채움 벡터의 숫자 개수:", len(filler_vectors[0]))
```

출력:
```
채움 벡터 수: 400
첫 채움 벡터의 숫자 개수: 256

```

### [34] markdown {}

**결과 읽기** — `채움 벡터 수: 400`이 보입니다. 질문 여덟 개에 50을 곱한 수입니다.
`첫 채움 벡터의 숫자 개수: 256`도 보입니다. 문서 벡터와 숫자 개수가 같습니다.

다음 셀은 채움 벡터가 문서 벡터보다 첫 질문에 가까운지 파이썬으로 확인합니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.552953Z', 'iopub.status.busy': '2026-09-21T07:40:15.552818Z', 'iopub.status.idle': '2026-09-21T07:40:15.556427Z', 'shell.execute_reply': '2026-09-21T07:40:15.555835Z'}}

```python
# 첫 질문에서 채움 벡터와 문서 벡터가 얼마나 떨어져 있는지 파이썬으로 잽니다
filler_distance = cosine_distance(first_question_vector, filler_vectors[0])
first_doc_vector = doc_vectors[0]
doc_distance = cosine_distance(first_question_vector, first_doc_vector)
print("첫 채움 벡터의 코사인 거리:", round(filler_distance, 2))
print("첫 문서 ID:", doc_ids[0])
print("첫 문서의 코사인 거리:", round(doc_distance, 2))
```

출력:
```
첫 채움 벡터의 코사인 거리: 0.0
첫 문서 ID: LIB-001
첫 문서의 코사인 거리: 0.56

```

### [36] markdown {}

**결과 읽기** — `첫 채움 벡터의 코사인 거리: 0.0`이고 `첫 문서의 코사인 거리: 0.56`입니다.
`첫 문서 ID: LIB-001` 줄의 문서는 01·02절에서도 같은 거리 값이었습니다.
채움 행이 훨씬 가깝기 때문에 색인은 채움 행을 먼저 고릅니다.
이 합성 자료는 걸러 내는 순서를 보려고 만든 것이고 임베딩 품질을 나타내지 않습니다.

## 7. 표에 넣고 색인 만들기

표에는 문서 ID 칸과 범주 칸, 벡터 칸을 둡니다.
02절 표와 칸 이름이 같고 표 이름만 다릅니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.557591Z', 'iopub.status.busy': '2026-09-21T07:40:15.557487Z', 'iopub.status.idle': '2026-09-21T07:40:15.584150Z', 'shell.execute_reply': '2026-09-21T07:40:15.583624Z'}}

```python
# 범주 칸과 벡터 칸이 있는 표를 새로 만듭니다(같은 이름의 옛 표는 먼저 지웁니다)
cur.execute("DROP TABLE IF EXISTS " + table_name)
create_sql = "CREATE TABLE " + table_name + " (doc_id text PRIMARY KEY, category text,"
create_sql = create_sql + " embedding vector(" + str(vector_dimensions) + "))"
cur.execute(create_sql)
print("표 만들기 SQL:")
print(create_sql)
```

출력:
```
표 만들기 SQL:
CREATE TABLE ch12_core_filter (doc_id text PRIMARY KEY, category text, embedding vector(256))

```

### [38] markdown {}

**결과 읽기** — 라벨 줄 아래에 `CREATE TABLE ch12_core_filter (doc_id text PRIMARY KEY, category text, embedding vector(256))`가 보입니다.
칸 `category`에 넣는 값이 이 절의 검색 조건입니다.

다음 셀은 채움 행과 문서를 표에 넣습니다.
채움 행의 문서 ID는 `OTH-`와 번호를 이어 만듭니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.585020Z', 'iopub.status.busy': '2026-09-21T07:40:15.584946Z', 'iopub.status.idle': '2026-09-21T07:40:15.766150Z', 'shell.execute_reply': '2026-09-21T07:40:15.765785Z'}}

```python
# 채움 행 400개와 문서 12개를 표에 한 줄씩 넣고 들어간 행 수를 셉니다
insert_sql = "INSERT INTO " + table_name + " VALUES (%s, %s, %s)"
for i in range(len(filler_vectors)):
    filler_id = "OTH-" + str(i + 1)
    cur.execute(insert_sql, (filler_id, filler_category, str(filler_vectors[i])))
for i in range(len(docs)):
    cur.execute(insert_sql, (docs[i]["doc_id"], docs[i]["category"], str(doc_vectors[i])))
cur.execute("SELECT count(*) FROM " + table_name)
print("표에 들어간 행 수:", cur.fetchone()[0])
```

출력:
```
표에 들어간 행 수: 412

```

### [40] markdown {}

**결과 읽기** — `표에 들어간 행 수: 412`가 보입니다. 채움 행 400개와 문서 12개를 더한 수입니다.
값을 넘기는 자리표시자는 02절과 같은 `%s`입니다.
벡터는 `str(목록)`으로 바꾼 글을 값으로 넘깁니다.

다음 셀은 범주마다 행이 몇 개인지 셉니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.766775Z', 'iopub.status.busy': '2026-09-21T07:40:15.766712Z', 'iopub.status.idle': '2026-09-21T07:40:15.768908Z', 'shell.execute_reply': '2026-09-21T07:40:15.768635Z'}}

```python
# 범주마다 몇 행인지 세어 조건을 통과하는 행의 비율을 봅니다
print("범주 | 행 수")
for category_name in category_names:
    cur.execute("SELECT count(*) FROM " + table_name + " WHERE category = %s", (category_name,))
    print(category_name, "|", cur.fetchone()[0])
```

출력:
```
범주 | 행 수
library | 4
facility | 4
account | 4
other | 400

```

### [42] markdown {}

**결과 읽기** — 라벨 줄 아래 네 줄에서 `library | 4`와 `other | 400`이 보입니다.
범주 `facility`와 `account`도 각각 4입니다.
조건 `library`를 통과하는 행은 412개 가운데 4개뿐입니다.
이렇게 통과 비율이 낮을 때 나중 걸러 내기가 문제가 됩니다.

다음 셀은 벡터 칸에 HNSW 색인을 만듭니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.769505Z', 'iopub.status.busy': '2026-09-21T07:40:15.769448Z', 'iopub.status.idle': '2026-09-21T07:40:15.826377Z', 'shell.execute_reply': '2026-09-21T07:40:15.826059Z'}}

```python
# 코사인 거리에 맞는 연산자 클래스로 HNSW 색인을 만듭니다(02절과 같은 문장)
index_sql = "CREATE INDEX " + index_name + " ON " + table_name
index_sql = index_sql + " USING hnsw (embedding vector_cosine_ops)"
cur.execute(index_sql)
print("색인 만들기 SQL:")
print(index_sql)
```

출력:
```
색인 만들기 SQL:
CREATE INDEX ch12_core_filter_idx ON ch12_core_filter USING hnsw (embedding vector_cosine_ops)

```

### [44] markdown {}

**결과 읽기** — 라벨 줄 아래에 `CREATE INDEX ch12_core_filter_idx ON ch12_core_filter USING hnsw (embedding vector_cosine_ops)`가 보입니다.
02절과 같은 연산자 클래스라 검색 SQL의 `<=>`와 짝이 맞습니다.

## 8. 검색 SQL 두 가지

첫 SQL은 02절과 같은 필터 없는 검색입니다.
둘째 SQL은 그 문장에 `WHERE category = %s`를 더한 것입니다.
조건 값도 자리표시자로 넘깁니다. Ch 4 03절에서 배운 규칙과 같습니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.827037Z', 'iopub.status.busy': '2026-09-21T07:40:15.826978Z', 'iopub.status.idle': '2026-09-21T07:40:15.828752Z', 'shell.execute_reply': '2026-09-21T07:40:15.828441Z'}}

```python
# 필터 없는 검색 SQL과 범주 조건을 붙인 검색 SQL을 만듭니다
search_sql = "SELECT doc_id, embedding <=> %s FROM " + table_name
search_sql = search_sql + " ORDER BY embedding <=> %s LIMIT %s"
filter_sql = "SELECT doc_id, embedding <=> %s FROM " + table_name + " WHERE category = %s"
filter_sql = filter_sql + " ORDER BY embedding <=> %s LIMIT %s"
print("필터 없는 검색 SQL:")
print(search_sql)
print("범주 조건을 붙인 검색 SQL:")
print(filter_sql)
```

출력:
```
필터 없는 검색 SQL:
SELECT doc_id, embedding <=> %s FROM ch12_core_filter ORDER BY embedding <=> %s LIMIT %s
범주 조건을 붙인 검색 SQL:
SELECT doc_id, embedding <=> %s FROM ch12_core_filter WHERE category = %s ORDER BY embedding <=> %s LIMIT %s

```

### [46] markdown {}

**결과 읽기** — 첫 라벨 줄 아래에 `SELECT doc_id, embedding <=> %s FROM ch12_core_filter ORDER BY embedding <=> %s LIMIT %s`가 보입니다.
둘째 라벨 줄 아래 문장에는 `WHERE category = %s`가 더 있습니다.
둘째 문장의 자리표시자는 네 개이고 순서는 벡터·범주·벡터·줄 수입니다.

필터 없는 검색은 준비 셀에서 가져온 02절 함수 `run_search()`로 실행하고 `print_hits()`로 출력합니다.
계획 줄은 02절 함수 `find_scan_line()`으로 고릅니다.
도구 파일의 두 함수는 02절 판이 노트북에서 바로 읽던 커서와 SQL을 인자로 받습니다.
계획 줄 함수는 넘길 값도 받습니다. 이 절은 SQL이 두 가지이기 때문입니다.

## 9. 실행 1 — 필터 없는 검색

실행 전에 예상해 봅니다. 채움 행이 질문에 가장 가까우니 상위 세 개가 모두 채움 행일 것입니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.829244Z', 'iopub.status.busy': '2026-09-21T07:40:15.829199Z', 'iopub.status.idle': '2026-09-21T07:40:15.832039Z', 'shell.execute_reply': '2026-09-21T07:40:15.831768Z'}}

```python
# 실행 1: 필터를 걸지 않고 첫 질문에 가까운 행 세 개를 받아 옵니다
first_vector_text = str(first_question_vector)
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(cur, search_sql, (first_vector_text, first_vector_text, top_three)))
no_filter_hits = run_search(cur, search_sql, first_question_vector, top_three)
print("받아 온 줄 수:", len(no_filter_hits))
print_hits(no_filter_hits)
```

출력:
```
실행 계획의 읽기 방법 줄:
->  Seq Scan on ch12_core_filter  (cost=0.00..65.18 rows=412 width=48)
받아 온 줄 수: 3
순위 | 문서 ID | 코사인 거리
1 | OTH-1 | 0.0
2 | OTH-2 | 0.0
3 | OTH-3 | 0.0

```

### [48] markdown {}

**결과 읽기** — 계획 줄에 `Seq Scan on ch12_core_filter`가 적혀 있습니다.
행이 412개뿐이라 계획기가 차례로 읽는 쪽을 골랐습니다. 02절 12행 표에서도 같았습니다.
괄호 안의 비용 어림 값과 행 수 어림은 실행 환경에 따라 달라집니다.

`받아 온 줄 수: 3`이고 라벨 줄 아래 세 줄은 `1 | OTH-1 | 0.0`, `2 | OTH-2 | 0.0`, `3 | OTH-3 | 0.0`입니다.
문서 열두 건은 한 건도 앞자리에 오지 않았습니다.
채움 행의 거리가 문서보다 작기 때문입니다.

## 10. 색인 경로로 읽게 하기

이 절은 색인이 후보를 고르는 순서를 보려고 색인 경로로 읽게 합니다.
02절에서 쓴 설정 `enable_seqscan`을 off로 두면 계획기가 순차 스캔을 고르지 못합니다.
설정은 준비 셀에서 가져온 02절 함수 `set_seqscan()`으로 바꿉니다. 커서를 첫 인자로 받는 점만 02절 판과 다릅니다.

다음 셀은 설정을 바꾸고 색인 설정 두 개와 계획 줄을 봅니다.
설정 `hnsw.max_scan_tuples`는 반복 탐색이 볼 수 있는 줄 수 한도입니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.832611Z', 'iopub.status.busy': '2026-09-21T07:40:15.832565Z', 'iopub.status.idle': '2026-09-21T07:40:15.834745Z', 'shell.execute_reply': '2026-09-21T07:40:15.834453Z'}}

```python
# 색인 경로로 읽게 설정을 바꾸고 색인 설정 두 개와 계획 줄을 봅니다
print("enable_seqscan 설정:", set_seqscan(cur, "off"))
cur.execute("SHOW hnsw.ef_search")
print("후보 목록 크기:", cur.fetchone()[0])
cur.execute("SHOW hnsw.max_scan_tuples")
print("반복 탐색이 볼 줄 수 한도:", cur.fetchone()[0])
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(cur, filter_sql, (first_vector_text, first_category, first_vector_text, top_three)))
```

출력:
```
enable_seqscan 설정: off
후보 목록 크기: 40
반복 탐색이 볼 줄 수 한도: 20000
실행 계획의 읽기 방법 줄:
->  Index Scan using ch12_core_filter_idx on ch12_core_filter  (cost=246.02..524.25 rows=2 width=48)

```

### [50] markdown {}

**결과 읽기** — `enable_seqscan 설정: off`이고 `후보 목록 크기: 40`입니다.
`반복 탐색이 볼 줄 수 한도: 20000`도 보입니다. 두 값은 모두 기본값입니다.
계획 줄이 `Index Scan using ch12_core_filter_idx`로 바뀌었습니다.
이제 범주 조건을 붙인 검색이 색인 경로로 읽습니다.

## 11. 받아야 하는 답 — 정확 검색

색인 경로의 결과를 견줄 답이 필요합니다.
01절 정확 검색을 범주 하나에만 적용해 파이썬으로 순위를 냅니다.
문서가 열두 건뿐이라 모두 재도 값이 금방 나옵니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.835244Z', 'iopub.status.busy': '2026-09-21T07:40:15.835199Z', 'iopub.status.idle': '2026-09-21T07:40:15.836988Z', 'shell.execute_reply': '2026-09-21T07:40:15.836685Z'}}

```python
# 문서 12개 가운데 한 범주만 남겨 코사인 거리가 가까운 순서로 반환합니다
def rank_in_category(question_vector, category_name, top_count):
    picked_vectors = []
    picked_ids = []
    for i in range(len(docs)):
        if docs[i]["category"] == category_name:
            picked_vectors.append(doc_vectors[i])
            picked_ids.append(docs[i]["doc_id"])
    # 고른 문서만 01절 순위 함수에 넘겨 코사인 거리가 가까운 순서로 받습니다
    return rank_by_distance(question_vector, picked_vectors, picked_ids, top_count)
```

출력:
```

```

### [52] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
범주에 든 문서의 벡터와 ID만 골라 준비 셀에서 가져온 `rank_by_distance()`에 넘깁니다.

도구 파일의 `rank_by_distance()`는 01절 판과 인자 모양이 다릅니다.
01절 판은 문서 ID 목록과 거리 목록을 받아 차례만 매겼습니다.
도구 파일 판은 질문 벡터·문서 벡터 목록·문서 ID 목록·남길 개수를 받아 코사인 거리까지 잽니다.

다음 셀은 첫 질문과 범주 `library`로 정확 검색 상위 세 개를 냅니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.837566Z', 'iopub.status.busy': '2026-09-21T07:40:15.837520Z', 'iopub.status.idle': '2026-09-21T07:40:15.839391Z', 'shell.execute_reply': '2026-09-21T07:40:15.839082Z'}}

```python
# 첫 질문과 그 범주로 정확 검색 상위 세 개를 내어 받아야 하는 답을 정합니다
exact_hits = rank_in_category(first_question_vector, first_category, top_three)
print("걸 범주:", first_category)
print_hits(exact_hits)
```

출력:
```
걸 범주: library
순위 | 문서 ID | 코사인 거리
1 | LIB-004 | 0.43
2 | LIB-001 | 0.56
3 | LIB-003 | 0.62

```

### [54] markdown {}

**결과 읽기** — `걸 범주: library`이고 라벨 줄 아래 세 줄은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.
01·02절 상위 세 개와 문서 ID·순서·거리 값이 모두 같습니다.
이 질문에서는 범주 `library` 밖 문서가 앞 세 자리에 없었기 때문입니다.
이 세 줄이 색인 경로가 받아 오기를 바라는 답입니다.

## 12. 질문 여덟 개를 잴 함수 준비

질문 하나로는 두 경로의 차이를 말할 수 없습니다.
지표 함수 네 개는 준비 셀에서 가져온 Ch 11 함수를 그대로 씁니다.
정답 자리는 고유 문서 목록에서 정답 문서가 몇 번째인지 센 값입니다.

다음 셀은 범주 조건을 붙인 검색을 실행하는 함수입니다.
02절 `run_search()`와 본문 모양이 같고 범주 이름을 하나 더 넘깁니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.839952Z', 'iopub.status.busy': '2026-09-21T07:40:15.839890Z', 'iopub.status.idle': '2026-09-21T07:40:15.841327Z', 'shell.execute_reply': '2026-09-21T07:40:15.841044Z'}}

```python
# 질문 벡터와 범주 이름으로 표를 검색해 문서 ID와 코사인 거리 목록을 반환합니다
def run_filtered_search(question_vector, category_name, top_count):
    # 벡터와 범주 이름을 모두 %s 자리에 값으로 넘깁니다
    vector_text = str(question_vector)
    cur.execute(filter_sql, (vector_text, category_name, vector_text, top_count))
    hit_list = []
    for row in cur.fetchall():
        hit_list.append({"doc_id": row[0], "거리": round(row[1], 2)})
    return hit_list
```

출력:
```

```

### [56] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 반복 탐색 설정을 바꾸는 함수입니다.
설정 `hnsw.iterative_scan`은 값이 `off`·`strict_order`·`relaxed_order` 세 가지입니다.

### [57] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.841846Z', 'iopub.status.busy': '2026-09-21T07:40:15.841806Z', 'iopub.status.idle': '2026-09-21T07:40:15.843465Z', 'shell.execute_reply': '2026-09-21T07:40:15.843102Z'}}

```python
# 반복 탐색 설정을 바꾸고 바뀐 값을 반환합니다
def set_iterative_scan(setting_value):
    cur.execute("SELECT set_config('hnsw.iterative_scan', %s, false)", (setting_value,))
    cur.execute("SHOW hnsw.iterative_scan")
    return cur.fetchone()[0]
```

출력:
```

```

### [58] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
02절 `set_seqscan()`과 본문 모양이 같고 바꾸는 설정 이름만 다릅니다.

다음 셀은 반복 탐색을 기본값 off로 두고 시작합니다.

### [59] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.844057Z', 'iopub.status.busy': '2026-09-21T07:40:15.844011Z', 'iopub.status.idle': '2026-09-21T07:40:15.845522Z', 'shell.execute_reply': '2026-09-21T07:40:15.845281Z'}}

```python
# 반복 탐색을 기본값 off로 두고 시작합니다
print("반복 탐색 설정:", set_iterative_scan("off"))
```

출력:
```
반복 탐색 설정: off

```

### [60] markdown {}

**결과 읽기** — `반복 탐색 설정: off`가 보입니다. 이 값이 pgvector 기본값입니다.
14절에서 이 값을 바꿔 같은 검색을 다시 실행합니다.

다음 셀은 질문 하나를 한 경로로 검색해 앞 세 자리를 내는 함수입니다.

### [61] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.846104Z', 'iopub.status.busy': '2026-09-21T07:40:15.846063Z', 'iopub.status.idle': '2026-09-21T07:40:15.847657Z', 'shell.execute_reply': '2026-09-21T07:40:15.847329Z'}}

```python
# 질문 하나를 한 경로로 검색해 앞 세 자리 목록을 반환합니다
def pick_hits(query_index, path_name):
    question_vector = query_vectors[query_index]
    gold_doc_id = queries[query_index]["gold_doc_id"]
    category_name = find_category(gold_doc_id)
    if path_name == path_names[0]:
        hit_list = rank_in_category(question_vector, category_name, top_three)
    else:
        hit_list = run_filtered_search(question_vector, category_name, top_three)
    return hit_list
```

출력:
```

```

### [62] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
경로 이름이 `정확 검색`이면 파이썬으로, 아니면 데이터베이스로 검색합니다.

다음 셀은 그 결과로 기록 한 줄을 만드는 함수입니다.
받아 온 줄 수를 칸으로 둔 점이 02절 기록과 다릅니다.

### [63] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.848158Z', 'iopub.status.busy': '2026-09-21T07:40:15.848118Z', 'iopub.status.idle': '2026-09-21T07:40:15.849843Z', 'shell.execute_reply': '2026-09-21T07:40:15.849520Z'}}

```python
# 질문 하나를 한 경로로 재어 기록 한 줄을 만듭니다
def score_one(query_index, path_name):
    query = queries[query_index]
    gold_doc_ids = [query["gold_doc_id"]]
    hit_list = pick_hits(query_index, path_name)
    found_ids = unique_doc_ids(hit_list)
    row = {"경로": path_name, "질문": query["qid"]}
    row["받아 온 줄 수"] = len(found_ids)
    row["정답 자리"] = find_gold_rank(found_ids, gold_doc_ids)
    for cutoff in cutoff_values:
        row["자리 " + str(cutoff)] = recall_at(found_ids, gold_doc_ids, cutoff)
    return row
```

출력:
```

```

### [64] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 13. 두 경로의 재현율 견주기

질문 여덟 개를 두 경로로 모두 잽니다.
질문 벡터를 이미 만들어 두었으므로 임베딩 요청이 늘지 않습니다.

### [65] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.850340Z', 'iopub.status.busy': '2026-09-21T07:40:15.850292Z', 'iopub.status.idle': '2026-09-21T07:40:15.854367Z', 'shell.execute_reply': '2026-09-21T07:40:15.854052Z'}}

```python
# 질문 여덟 개를 두 경로로 모두 재어 기록 줄을 담습니다(임베딩 요청은 더 보내지 않습니다)
score_rows = []
for path_name in path_names:
    for query_index in range(len(queries)):
        score_rows.append(score_one(query_index, path_name))
print("담은 기록 줄 수:", len(score_rows))
```

출력:
```
담은 기록 줄 수: 16

```

### [66] markdown {}

**결과 읽기** — `담은 기록 줄 수: 16`이 보입니다. 질문 여덟 개에 경로 두 가지를 곱한 수입니다.

다음 셀은 담은 줄을 표로 출력합니다.

### [67] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.854903Z', 'iopub.status.busy': '2026-09-21T07:40:15.854857Z', 'iopub.status.idle': '2026-09-21T07:40:15.856782Z', 'shell.execute_reply': '2026-09-21T07:40:15.856536Z'}}

```python
# 경로·질문·받아 온 줄 수·정답 자리·자리 1·자리 3을 라벨 줄 아래에 차례로 출력합니다
print("경로 | 질문 | 받아 온 줄 수 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율")
for row in score_rows:
    print(row["경로"], "|", row["질문"], "|", row["받아 온 줄 수"], "|", row["정답 자리"], "|", row["자리 1"], "|", row["자리 3"])
```

출력:
```
경로 | 질문 | 받아 온 줄 수 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율
정확 검색 | C01 | 3 | 2 | 0.0 | 1.0
정확 검색 | C02 | 3 | 0 | 0.0 | 0.0
정확 검색 | C03 | 3 | 1 | 1.0 | 1.0
정확 검색 | C04 | 3 | 1 | 1.0 | 1.0
정확 검색 | C05 | 3 | 1 | 1.0 | 1.0
정확 검색 | C06 | 3 | 1 | 1.0 | 1.0
정확 검색 | C07 | 3 | 1 | 1.0 | 1.0
정확 검색 | C08 | 3 | 1 | 1.0 | 1.0
색인 경로 | C01 | 0 | 0 | 0.0 | 0.0
색인 경로 | C02 | 0 | 0 | 0.0 | 0.0
색인 경로 | C03 | 0 | 0 | 0.0 | 0.0
색인 경로 | C04 | 0 | 0 | 0.0 | 0.0
색인 경로 | C05 | 1 | 1 | 1.0 | 1.0
색인 경로 | C06 | 1 | 1 | 1.0 | 1.0
색인 경로 | C07 | 0 | 0 | 0.0 | 0.0
색인 경로 | C08 | 1 | 1 | 1.0 | 1.0

```

### [68] markdown {}

**결과 읽기** — 라벨 줄 아래 앞 여덟 줄이 정확 검색이고 받아 온 줄 수가 모두 `3`입니다.
뒤 여덟 줄은 색인 경로이고 받아 온 줄 수가 `0` 또는 `1`입니다.
질문 `C05`·`C06`·`C08`만 한 줄을 받았고 그 한 줄이 정답 문서였습니다.
질문 `C02`는 두 경로 모두 정답 자리가 `0`입니다.

질문 `C02`의 정답 문서 `LIB-002`는 범주 안 넷 가운데 넷째라 앞 세 자리에 들어오지 않았습니다.
다음 셀은 자르는 자리마다 질문 평균 재현율을 견줍니다.

### [69] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.857276Z', 'iopub.status.busy': '2026-09-21T07:40:15.857235Z', 'iopub.status.idle': '2026-09-21T07:40:15.859121Z', 'shell.execute_reply': '2026-09-21T07:40:15.858771Z'}}

```python
# 두 경로의 질문 평균 재현율을 자르는 자리마다 견줍니다
print("경로 | 자르는 자리 | 질문 평균 재현율")
for path_name in path_names:
    picked = []
    for row in score_rows:
        if row["경로"] == path_name:
            picked.append(row)
    for cutoff in cutoff_values:
        scores = []
        for row in picked:
            scores.append(row["자리 " + str(cutoff)])
        print(path_name, "|", cutoff, "|", mean_score(scores))
```

출력:
```
경로 | 자르는 자리 | 질문 평균 재현율
정확 검색 | 1 | 0.75
정확 검색 | 2 | 0.875
정확 검색 | 3 | 0.875
색인 경로 | 1 | 0.375
색인 경로 | 2 | 0.375
색인 경로 | 3 | 0.375

```

### [70] markdown {}

**결과 읽기** — 라벨 줄 아래 여섯 줄이 나옵니다.
정확 검색은 자리 1에서 `0.75`, 자리 2와 자리 3에서 `0.875`입니다.
색인 경로는 세 자리 모두 `0.375`입니다.
받아 온 줄이 없으면 자르는 자리를 늘려도 재현율이 오르지 않습니다.

### [71] markdown {'lesson_part': 'before'}

## 14. 반복 탐색을 끈 채로 검색하기

Before 셀은 「조건에 맞는 문서가 네 건 있으니 세 줄은 받을 것」이라고 보는 자리입니다.
첫 질문에 범주 `library` 조건을 붙여 한 번 더 검색합니다.
표에 조건을 통과하는 행이 네 개 있는 것은 7절에서 확인했습니다.

### [72] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.859623Z', 'iopub.status.busy': '2026-09-21T07:40:15.859582Z', 'iopub.status.idle': '2026-09-21T07:40:15.861199Z', 'shell.execute_reply': '2026-09-21T07:40:15.860900Z'}, 'lesson_part': 'before'}

```python
# 반복 탐색이 꺼져 있는지 확인하고 이 검색의 조건을 다시 적습니다
cur.execute("SHOW hnsw.iterative_scan")
print("반복 탐색 설정:", cur.fetchone()[0])
print("받아 올 줄 수:", top_three)
print("걸 범주:", first_category)
```

출력:
```
반복 탐색 설정: off
받아 올 줄 수: 3
걸 범주: library

```

### [73] markdown {'lesson_part': 'before'}

**결과 읽기** — `반복 탐색 설정: off`이고 `받아 올 줄 수: 3`, `걸 범주: library`입니다.
세 값은 13절 색인 경로를 잴 때와 같습니다.

다음 셀은 이 설정으로 첫 질문을 검색합니다.

### [74] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.861663Z', 'iopub.status.busy': '2026-09-21T07:40:15.861619Z', 'iopub.status.idle': '2026-09-21T07:40:15.863441Z', 'shell.execute_reply': '2026-09-21T07:40:15.863118Z'}, 'lesson_part': 'before'}

```python
# 반복 탐색을 끈 채로 첫 질문에 범주 조건을 붙여 검색합니다
before_hits = run_filtered_search(first_question_vector, first_category, top_three)
print("받아 온 줄 수:", len(before_hits))
print_hits(before_hits)
```

출력:
```
받아 온 줄 수: 0
순위 | 문서 ID | 코사인 거리

```

### [75] markdown {'lesson_part': 'before'}

**결과 읽기** — `받아 온 줄 수: 0`이고 라벨 줄 아래에 결과 줄이 한 줄도 없습니다.
조건을 통과하는 문서가 네 건 있는데도 한 줄도 받지 못했습니다.
색인이 먼저 고른 후보 40개가 모두 채움 행이었고, 그 뒤에 범주 조건을 검사했기 때문입니다.
받아 온 줄 수가 0이라고 조건에 맞는 문서가 없다고 볼 수 없습니다.

### [76] markdown {'lesson_part': 'after'}

## 15. 설정 하나만 바꿔 다시 실행하기

바꿀 것은 설정 `hnsw.iterative_scan` 하나입니다. off에서 `strict_order`로 바꿉니다.
이 값은 필요한 줄을 얻거나 볼 줄 수 한도에 이를 때까지 색인을 더 살펴보게 합니다.
값 `strict_order`는 받아 온 줄을 거리 순서대로 냅니다.

자료·질문·조건·받아 올 줄 수·후보 목록 크기는 그대로 둡니다.
실행 전에 예상해 봅니다. 세 줄을 받고 그 세 줄이 정확 검색 상위 세 개와 같을 것입니다.

### [77] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.864005Z', 'iopub.status.busy': '2026-09-21T07:40:15.863963Z', 'iopub.status.idle': '2026-09-21T07:40:15.866207Z', 'shell.execute_reply': '2026-09-21T07:40:15.865817Z'}, 'lesson_part': 'after'}

```python
# 설정 하나만 strict_order로 바꿔 같은 검색을 다시 실행합니다
print("반복 탐색 설정:", set_iterative_scan("strict_order"))
after_hits = run_filtered_search(first_question_vector, first_category, top_three)
print("받아 온 줄 수:", len(after_hits))
print_hits(after_hits)
assert len(after_hits) >= len(before_hits)
```

출력:
```
반복 탐색 설정: strict_order
받아 온 줄 수: 3
순위 | 문서 ID | 코사인 거리
1 | LIB-004 | 0.43
2 | LIB-001 | 0.56
3 | LIB-003 | 0.62

```

### [78] markdown {'lesson_part': 'after'}

**결과 읽기** — `반복 탐색 설정: strict_order`이고 `받아 온 줄 수: 3`입니다.
라벨 줄 아래 세 줄은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.
11절 정확 검색 상위 세 개와 문서 ID·순서·거리 값이 모두 같습니다. `assert`도 통과했습니다.
받지 못한 까닭이 자료가 아니라 후보를 고르는 폭이었다는 뜻입니다.

## 16. 값 바꿔 보기 — relaxed_order

바꿀 값은 반복 탐색 설정 하나입니다. `strict_order`에서 `relaxed_order`로 바꿉니다.
값 `relaxed_order`는 거리 순서가 조금 달라질 수 있는 대신 줄을 더 받을 수 있습니다.
실행 전에 예상해 봅니다. 받아 온 줄 수는 세 줄일 것이고 순서는 알 수 없습니다.

### [79] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.866775Z', 'iopub.status.busy': '2026-09-21T07:40:15.866730Z', 'iopub.status.idle': '2026-09-21T07:40:15.869042Z', 'shell.execute_reply': '2026-09-21T07:40:15.868639Z'}, 'lesson_part': 'after'}

```python
# 반복 탐색 값만 relaxed_order로 바꿔 한 번 더 실행합니다
print("반복 탐색 설정:", set_iterative_scan("relaxed_order"))
relaxed_hits = run_filtered_search(first_question_vector, first_category, top_three)
print("받아 온 줄 수:", len(relaxed_hits))
print_hits(relaxed_hits)
```

출력:
```
반복 탐색 설정: relaxed_order
받아 온 줄 수: 3
순위 | 문서 ID | 코사인 거리
1 | LIB-004 | 0.43
2 | LIB-001 | 0.56
3 | LIB-003 | 0.62

```

### [80] markdown {'lesson_part': 'after'}

**결과 읽기** — `반복 탐색 설정: relaxed_order`이고 `받아 온 줄 수: 3`입니다.
라벨 줄 아래 세 줄은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.
이번 실행에서는 `strict_order`와 순서까지 같았습니다.
조건에 맞는 문서가 네 건뿐이라 두 값의 차이가 드러나지 않았습니다.
큰 자료에서 두 값을 견주는 일은 이번에 실행하지 않았습니다.

다음 셀은 바꾼 설정 두 개를 기본값으로 되돌리고 연결을 닫습니다.

### [81] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:15.869539Z', 'iopub.status.busy': '2026-09-21T07:40:15.869498Z', 'iopub.status.idle': '2026-09-21T07:40:15.871316Z', 'shell.execute_reply': '2026-09-21T07:40:15.871049Z'}, 'lesson_part': 'after'}

```python
# 바꾼 설정 두 개를 기본값으로 되돌리고 연결을 닫습니다
print("반복 탐색 설정:", set_iterative_scan("off"))
print("enable_seqscan 설정:", set_seqscan(cur, "on"))
conn.close()
print("연결 닫힘:", conn.closed)
```

출력:
```
반복 탐색 설정: off
enable_seqscan 설정: on
연결 닫힘: True

```

### [82] markdown {'lesson_part': 'after'}

**결과 읽기** — `반복 탐색 설정: off`와 `enable_seqscan 설정: on`이 보입니다.
마지막 줄 `연결 닫힘: True`는 연결이 닫혔다는 뜻입니다.

검색에 쓴 표 `ch12_core_filter`는 지우지 않고 그대로 남깁니다.

## 정리

1. 범주 조건을 붙인 색인 경로 검색이 첫 질문에서 `0`줄을 냈습니다. 조건을 통과하는 문서는 네 건 있었습니다.
2. 질문 여덟 개 질문 평균 재현율은 정확 검색 자리 1에서 `0.75`인데 색인 경로는 세 자리 모두 `0.375`였습니다.
3. 설정 `hnsw.iterative_scan`만 `strict_order`로 바꾸니 세 줄을 받고 정확 검색 상위 세 개와 같았습니다.

04절에서는 벡터 거리가 아니라 한국어 낱말로 문서를 찾습니다.
형태소 분석기로 낱말을 가르고 낱말이 겹치는 정도로 순위를 냅니다.

## 그림

### 03-1-후보를-고른-뒤-조건-검사.mmd

```mermaid
flowchart TB
  %% classes
  table["표 ch12_core_filter<br>412행"]:::tool
  pick["색인이 가까운 후보부터 고르기<br>후보 목록 크기 40"]:::flow
  check["범주 조건을 나중에 검사"]:::flow
  keep["조건을 통과한 줄만 남기기"]:::flow
  fewer["받아 온 줄 수가<br>받아 올 줄 수보다 적어짐"]:::measure
  table --> pick
  pick --> check
  check --> keep
  keep --> fewer
```

색인 경로는 가까운 후보를 먼저 고르고 범주 조건을 나중에 검사하므로 받아 온 줄 수가 받아 올 줄 수보다 적어질 수 있습니다.

### 03-2-표에-넣은-두-가지-행.mmd

```mermaid
flowchart TB
  %% classes
  queries["질문 8개<br>01절과 같은 자료"]:::tool
  filler["채움 행 400개<br>질문마다 50개"]:::tool
  docs["교육용 문서 12개<br>범주 세 가지"]:::tool
  vectors["문서 벡터 12개<br>숫자 256개씩"]:::tool
  table["표 ch12_core_filter<br>412행"]:::tool
  index["HNSW 색인<br>vector_cosine_ops"]:::tool
  counts["범주별 행 수<br>library 4 · other 400"]:::measure
  queries -->|규칙으로 벡터 만들기| filler
  docs -->|임베딩 요청 1번| vectors
  filler --> table
  vectors --> table
  table -->|CREATE INDEX| index
  index --> counts
```

질문에서 규칙으로 만든 채움 행 400개와 교육용 문서 벡터 12개를 한 표에 넣어 412행으로 만들고 그 벡터 칸에 HNSW 색인을 만듭니다.

### 03-3-두-경로의-질문-평균.mmd

```mermaid
---
config:
  themeVariables:
    xyChart:
      plotColorPalette: '#22c55e, #f59e0b'
---
xychart-beta
  title "두 경로의 질문 평균 재현율"
  x-axis ["자리 1", "자리 2", "자리 3"]
  y-axis "질문 평균 재현율" 0 --> 1
  line [0.75, 0.875, 0.875]
  line [0.375, 0.375, 0.375]
```

초록 선 정확 검색은 자리 1에서 0.75와 자리 3에서 0.875인데 주황 선 색인 경로는 세 자리 모두 0.375입니다.

### 03-4-설정-하나만-바꾼-뒤.mmd

```mermaid
flowchart TB
  %% classes
  subgraph off_case["반복 탐색 off"]
    direction TB
    off_sql["같은 필터 검색 SQL"]:::flow
    off_out["받아 온 줄 수 0"]:::fail
  end
  subgraph strict_case["반복 탐색 strict_order"]
    direction TB
    strict_sql["같은 필터 검색 SQL"]:::flow
    strict_out["받아 온 줄 수 3<br>LIB-004 · LIB-001 · LIB-003"]:::measure
  end
  off_sql --> off_out
  strict_sql --> strict_out
  off_out --> same["두 칸의 SQL과 넘긴 값은 같음<br>받아 온 줄 수만 갈림"]
  strict_out --> same
```

설정 하나만 off에서 strict_order로 바꾸니 받아 온 줄 수가 0에서 3으로 늘고 그 칸의 세 문서가 정확 검색 상위 세 개와 같아집니다.

### 03-5-끈과-빈-쟁반.prompt.md

# 03-5-끈과-빈-쟁반 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 한 칸은 책을 잇는 끈이 회색 책에서 멈춰 있고 다른 칸은 그 끈이 주황 책까지 이어져 있으며, 끈이 멈춘 칸에서는 주황 책을 한 권도 집지 못합니다.

구성 요소와 배치(저장한 그림 기준): 나란히 놓인 나무 서가 두 칸에 같은 책이 같은 자리로 서 있습니다(= 같은 표의 같은 행). 두 칸 모두 앞쪽은 옅은 회색 책이 빽빽하고 뒤쪽은 주황 책입니다(= 조건에 맞지 않는 채움 행과 조건에 맞는 문서). 왼쪽 칸에서는 책을 잇는 가는 끈이 회색 책 구간에서 멈춰 있고 아래 나무 쟁반이 비어 있습니다(= 반복 탐색 off, 받아 온 줄 수 0). 오른쪽 칸에서는 같은 끈이 주황 책을 지나 칸 밖까지 이어지고 아래 쟁반에 주황 책이 눕혀 쌓여 있습니다(= 반복 탐색 strict_order, 받아 온 줄 수 3).

시선 순서: 왼쪽 칸의 멈춘 끈 → 왼쪽 빈 쟁반 → 오른쪽 칸의 이어진 끈 → 오른쪽 쟁반의 주황 책.

검수 기준: 그림만 보고 「왼쪽 칸은 끈이 회색 책에서 멈춰 쟁반이 비었고, 오른쪽 칸은 끈이 주황 책까지 이어져 쟁반에 주황 책이 있다」가 읽히는가.

Ch 9~Ch 12 비유 계열과의 관계: 책과 책등 = 문서와 문서 ID(Ch 11 01-6, Ch 12 01-5), 나무 쟁반 = 받아 온 후보 목록(Ch 11 02-5), 책 사이의 끈 = 색인의 이웃 관계(Ch 12 02-5에서 정한 뜻을 이어 씀). 02절 삽화는 「끈이 있는 칸과 없는 칸」이었고 이 절은 「같은 끈이 어디까지 이어지는가」로 뜻을 좁혀 씁니다. 빈 쟁반 = 받아 온 줄 수 0은 이 절에서 새로 정한 뜻입니다. 카드 상자(Ch 9 색인)·흰 카드(Ch 9 문서 청크)·봉투(Ch 10 출처 기록)·서랍(Ch 10 벡터 캐시)은 뜻이 정해져 있어 쓰지 않았습니다.

## 프롬프트 (1차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette,
clean outlines, plain everyday objects, no text, no letters, no numbers, no logos.

Two identical wooden shelf compartments stand side by side. Each compartment holds
the same row of upright books in the same order: a dense group of pale grey books on
the left half, then three books with orange spines on the right half. A thin grey cord
threads through the books from the left. In the left compartment the cord threads only
through the pale grey books and stops before the first orange book, and the small
wooden tray below that compartment is completely empty. In the right compartment the
same cord threads through the pale grey books and continues all the way to the three
orange books, and the small wooden tray below that compartment holds exactly three
orange books lying flat in a stack. No hands, no people, no monitors, no screens,
no arrows.
```

## 상태

- 2026-09-18 · `nano_banana_pro`(응답 모델 이름 `nano_banana_2`) · 16:9 · 2k · `use_unlim: false` · 장당 2크레딧 · 1회 생성 2크레딧 · 생성 전 잔액 2735.
- 1차 job `d1fdbff2-70a9-4f3a-ac71-f9c8476ed4f8` **채택**: 검수 기준의 두 관계가 모두 읽힙니다. 원본 해시 `81ca56a11914d26e684af66ec9a9f1c21ee314a6cdc992861224cc2a2666ebeb`.
- **프롬프트와 그림이 다른 점(그림 읽기에 반영)**: 프롬프트는 쟁반에 「세 권」을 적었지만 저장한 그림의 쌓인 책은 맨 아래 한 권이 쟁반 테두리에 가려 권수가 또렷하지 않습니다. 그래서 본문 비유·alt·캡션·「그림 읽기」에 책 수를 적지 않고 「주황 책이 쌓여 있다」로만 썼습니다. 받아 온 줄 수 3은 Mermaid `03-4`와 노트북 출력이 보여 줍니다. 끈도 가는 줄이 아니라 곧은 막대처럼 그려졌지만 「어디까지 이어지는가」는 그대로 읽힙니다.
- 저장: 폭 1100px로 줄여 `figures/03-5-끈과-빈-쟁반.png`(1100 × 614). 원본 2752px는 저장하지 않았습니다. 저장 PNG를 채택 job 결과에서 같은 폭으로 줄인 그림과 픽셀 단위로 대조해 차이가 없음을 확인했습니다(`ImageChops.difference` 범위 `None`, 규격 §5-4).

