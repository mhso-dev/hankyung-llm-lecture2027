# 08-LangGraph-실습

## _src 본문 (HTML 원본)

```html
<!--meta: 실습 30분 | 코드 notebooks/08-LangGraph-실습.ipynb | 새 용어 0 -->

<h2 id="b1"><span class="no">1</span>학습 목표</h2>
<div class="goal"><ul>
<li>이 절을 마치면 01~07절에서 만든 부품을 그래프 하나에 함께 붙일 수 있습니다.</li>
<li>검색이 낸 점수로 노드가 다음 길을 고르게 만들 수 있습니다.</li>
<li>설정 칸의 값 하나만 바꿔 같은 그래프를 다시 실행할 수 있습니다.</li>
<li>두 실행에서 같은 값과 갈린 값을 나누어 읽을 수 있습니다.</li>
</ul></div>

<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2>
<p>01절부터 07절까지 그래프 부품을 하나씩 익혔습니다. 상태와 노드와 엣지를 적었고 규칙과 갈래와 이동을 만들었습니다. 마지막에는 Ch 12 검색을 노드로 나눠 붙였습니다.</p>
<p>실제로 안내 창구를 만들 때는 이 부품이 한 그래프 안에 함께 들어갑니다. 검색이 값을 내고 그 값으로 길이 갈리며 오간 말이 한 칸에 쌓입니다.</p>
<p>이번 실습은 그 세 가지를 한 번에 붙입니다. 06절 이동과 04절 메시지 칸과 07절 검색을 한 그래프에 담습니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~07절에서 쓴 이름과 문법만 쓰고 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 검색이 낸 점수를 견주는 기준값 한 자리만 바꾸면 그래프는 어느 길로 갈까요?</p>

<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2>
<p>이번 실습은 아래 절에서 배운 것을 그대로 가져옵니다.</p>
<table><thead><tr><th>절</th><th>배운 것</th><th>실습에서 쓰는 곳</th></tr></thead><tbody>
<tr><td>01절</td><td><code>StateGraph</code>와 <code>add_node</code>·<code>add_edge</code>·<code>compile</code>, 노드 <code>normalize</code></td><td>노트북 8절 첫 노드, 9절 조립</td></tr>
<tr><td>02절</td><td>칸에 적는 규칙 <code>Annotated[list[str], operator.add]</code></td><td>노트북 7절 실행 흔적 칸</td></tr>
<tr><td>03절</td><td>기준값으로 길 가르기, 답 글 <code>자료를 더 찾아야 합니다</code></td><td>노트북 8절 노드 <code>route</code>·<code>ask_more</code></td></tr>
<tr><td>04절</td><td>메시지 리듀서 <code>add_messages</code>와 <code>print_messages()</code></td><td>노트북 7절 메시지 칸, 10·11절 출력</td></tr>
<tr><td>06절</td><td><code>Command(update=, goto=)</code>와 <code>add_node(..., destinations=(...))</code></td><td>노트북 8절 노드 <code>route</code>, 9절 등록</td></tr>
<tr><td>07절</td><td>Ch 12 함수를 노드 안에서 부르기, 설정을 담는 칸</td><td>노트북 5·6절 함수, 8절 노드 <code>search_docs</code></td></tr>
<tr><td>Ch 12 05·06절</td><td>순위 목록 둘과 순위 합치기 <code>fuse_rank()</code>, 순위 상수 60</td><td>노트북 5절 함수, 8절 노드 <code>search_docs</code></td></tr>
<tr><td>Ch 12 07·08절</td><td><code>unique_chunk_ids()</code>·<code>parent_ids_of()</code>와 보고 자리 5</td><td>노트북 5절 함수, 10·11절 부모 문서 차례</td></tr>
</tbody></table>
<p>읽는 파일은 07절과 같은 Ch 12 문서 파일 하나입니다. 부모 문서 6건에서 만든 문서 청크 175개를 그대로 씁니다. 이번 실습에서 새로 만든 데이터는 없습니다.</p>
<p>05절 <code>Send</code>는 이번 실습에서 쓰지 않습니다. 기능을 더 붙이면 30분과 요청 네 번 안에 들어오지 않기 때문입니다. 03절 조건부 엣지도 06절 <code>Command</code>와 같은 일을 하므로 하나만 골랐습니다.</p>
<p>07절과 다른 점은 질문입니다. 07절은 Ch 12 기록의 질문을 읽었고 이번 실습은 01절 질문 <code>  대출 기간은 며칠인가요?  </code>를 씁니다. 앞뒤에 빈칸이 있어 노드 <code>normalize</code>가 할 일이 남아 있습니다.</p>
<p>새로 정의하는 함수는 없습니다. 출력 함수 <code>print_state()</code>와 기록 함수 <code>run_row()</code>는 이 절 칸에 맞춰 줄을 바꿨습니다. 처음 상태를 만드는 <code>new_state()</code>는 03·06·07절과 같은 모양입니다.</p>
<p>Ch 12 「1차 검색」은 합친 차례의 앞 여덟 개였습니다. 이 실습은 그 앞에서 다시 다섯 개를 남기므로 합친 차례의 앞 다섯 개와 같은 자리입니다. 그래서 여덟 개를 자르는 단계를 따로 두지 않았습니다.</p>

<h2 id="b4"><span class="no">4</span>핵심 개념</h2>
<h3>비유로 시작하기</h3>
<p>01절부터 쓴 나무 길과 작업대를 그대로 씁니다. 01절 길에는 작업대가 둘이었고 07절 길에는 다섯이 한 줄로 놓였습니다.</p>
<p>이번 길은 작업대 셋을 지난 뒤 갈라집니다. 셋째 작업대 위에 놓인 표지판이 어느 갈래로 갈지 정합니다. 갈래마다 작업대가 하나씩 더 있고 길은 그 자리에서 끝납니다.</p>
{{img:08-4-갈림길이-생긴-긴-길|흰 바탕에 왼쪽에서 오른쪽으로 뻗은 나무 널판 길 하나가 연장이 놓인 같은 모양 나무 작업대 셋을 차례로 지나고 셋째 작업대 위에 글자 없는 나무 표지판이 서 있으며 그 작업대 뒤에서 길이 위아래 두 갈래로 갈라져 갈래마다 끝에 작업대가 하나씩 놓인 그림|작업대 셋을 지난 길이 셋째 작업대 위 표지판 뒤에서 둘로 갈라집니다.}}
<p class="look"><b>그림 읽기</b> — 먼저 왼쪽 길을 봅니다. 널판을 이어 붙인 길 하나가 오른쪽으로 곧게 뻗어 있습니다. 그 길 위에 같은 모양 작업대 셋이 한 줄로 놓여 있고 작업대마다 연장이 있습니다.</p>
<p class="look">다음으로 셋째 작업대를 봅니다. 그 위에 글자 없는 나무 표지판이 서 있습니다. 표지판은 길가가 아니라 작업대 위에 있습니다.</p>
<p class="look">마지막으로 오른쪽을 봅니다. 셋째 작업대 뒤에서 길이 위아래 두 갈래로 갈라집니다. 갈래 끝마다 작업대가 하나씩 놓여 있습니다. 작업대 셋은 <code>normalize</code>와 <code>search_docs</code>와 <code>route</code>이고 갈래 끝 둘은 <code>make_reply</code>와 <code>ask_more</code>입니다.</p>

<h3>실습 조립의 구성</h3>
{{mermaid:08-1-조립도|위에서 아래로 놓인 상자 일곱으로 맨 위 회색 상자 가상 시작점 START에서 화살표가 파란 상자 노드 normalize 질문 칸을 다듬음으로 이어지고 다시 파란 상자 노드 search_docs 보고 자리 칸과 점수 칸과 파란 상자 노드 route 판단 이유 칸과 다음 노드로 이어진 뒤 점선 화살표 둘이 파란 상자 노드 make_reply 모델을 부르는 노드와 파란 상자 노드 ask_more 적어 둔 안내 글로 갈라지고 두 상자가 맨 아래 회색 상자 가상 끝점 END로 모이는 그림|01~07절에서 만든 부품을 노드 다섯으로 잇고 가운데 노드가 다음 길을 스스로 고릅니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 회색 상자가 입력이 들어오는 자리이고 맨 아래 회색 상자가 끝나는 자리입니다. 두 상자는 라이브러리가 주는 이름이라 회색입니다.</p>
<p class="look">가운데 파란 상자 다섯이 이 실습에서 만드는 노드입니다. 상자마다 그 노드가 채우는 칸 이름이 함께 적혀 있습니다.</p>
<p class="look">셋째 상자에서 점선 화살표 둘이 갈라집니다. 점선은 노드가 낸 <code>Command</code>가 정하는 이동입니다. 나머지 실선 다섯은 우리가 적은 고정 엣지입니다.</p>
<table><thead><tr><th>노드</th><th>하는 일</th><th>가져온 곳</th></tr></thead><tbody>
<tr><td><code>normalize</code></td><td>질문 칸의 앞뒤 빈칸을 없앰</td><td>02절 노드를 도구 파일에서 가져옴</td></tr>
<tr><td><code>search_docs</code></td><td>두 순위를 합쳐 보고 자리 다섯을 남기고 점수 칸을 채움</td><td>07절 노드 넷을 하나로 모음</td></tr>
<tr><td><code>route</code></td><td>점수 칸과 기준값을 견줘 갱신과 다음 노드를 함께 냄</td><td>06절(같은 모양)</td></tr>
<tr><td><code>make_reply</code></td><td>앞 세 자리 본문을 넣어 모델에게 답을 받음</td><td>07절 노드 이름과 같음</td></tr>
<tr><td><code>ask_more</code></td><td>적어 둔 안내 글을 메시지 하나로 만듦</td><td>03·06절 이름과 글이 같음</td></tr>
</tbody></table>

<h3>점수는 어디에서 오나</h3>
<p>03절과 06절에서는 점수를 손으로 상태에 넣었습니다. 이번에는 노드 <code>search_docs</code>가 점수를 채웁니다. 낱말 순위 1위의 점수를 그대로 점수 칸에 담습니다.</p>
<p>그 점수는 질문 낱말이 문서 청크에 얼마나 겹치는지를 나타냅니다. 답이 맞는지를 재는 값이 아닙니다. 답 정확성을 판정하는 일은 Ch 15 몫입니다.</p>

<h3>두 번의 실행</h3>
<p>실행 1은 기준값 <code>5.0</code>입니다. 실행 2는 기준값만 <code>9.0</code>으로 올립니다.</p>
<p>질문과 문서 청크 175개, 두 순위에 줄 몫 <code>[1.0, 1.0]</code>, 보고 자리 5, 넣을 자리 3, 모델은 두 실행에서 같게 둔 조건입니다. 기준값은 상태의 설정 칸에 담으므로 그래프를 고치지 않습니다.</p>
<p>기준값 두 개는 탐색 실행 뒤에 정했습니다. 낱말 순위 1위의 점수가 <code>7.64</code>여서 그 위와 아래로 하나씩 잡았습니다. 두 길이 모두 보이게 하려고 정한 예입니다.</p>

<h2 id="b5"><span class="no">5</span>실행 예제</h2>
<p>노트북은 먼저 Ch 12 자료를 읽고 값을 정합니다. 앞 절 함수 일곱 개는 실습 폴더의 도구 파일 <code>notebooks/rag_tools.py</code>에서 한 줄로 가져옵니다. 그다음 BM25 모델과 문서 청크 벡터를 만듭니다. 마지막으로 상태와 기록 장치와 노드 다섯을 만들고 실행 1, 실행 2, 두 실행 비교를 차례로 합니다.</p>
<p>정의 셀은 여덟 개이고 하나는 상태 형식, 일곱은 이 절이 만든 함수입니다. 가져온 함수 일곱 개는 02절 노드 <code>normalize</code>와 07절에서 쓴 Ch 12 검색 함수 여섯 개입니다. 9~12절의 출력 두 벌과 표를 강사와 함께 읽습니다.</p>
<p>실제 OpenAI 모델을 부릅니다. 이 페이지의 출력은 2026-09-21에 실행한 결과입니다. 서비스 요청은 모두 네 번이고 임베딩 세 번과 답을 쓰는 모델 한 번입니다. 예상 비용은 네 번을 합쳐 미화 0.01달러 아래입니다.</p>
{{notebook:08-LangGraph-실습}}
<p class="look"><b>확인할 점</b> — 9절 출력에서 구조 문자열의 실선 다섯 줄과 점선 두 줄을 봅니다. 10·11절 출력에서 점수 칸과 기준값 칸과 판단 이유 칸을 견줍니다. 두 실행의 실행 흔적 칸에서 마지막 이름이 어떻게 달라졌는지 읽고 12절 표에서 같은 값과 갈린 값을 나눕니다.</p>

<h3>실행 1의 실제 순서</h3>
{{mermaid:08-2-실행1-순서|위에서 아래로 내려가는 흐름도로 맨 위 초록 상자 질문 칸 대출 기간은 며칠인가요?와 그 아래 노란 상자 search_docs가 낸 점수 칸 7.64가 있고 오른쪽 초록 상자 설정 칸에 넣은 기준값 5.0과 함께 노란 상자 route의 판단 이유 칸 자료가 넉넉함으로 모인 뒤 보라 상자 모델 gpt-5.4-mini를 지나 맨 아래 노란 상자 메시지 칸의 메시지 수 둘로 이어지는 그림|실행 1에서 검색이 낸 점수 7.64가 기준값 5.0을 넘어 모델을 부르는 길로 갔습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 왼쪽 위 초록 상자가 다듬은 질문이고 그 아래 노란 상자가 검색이 낸 점수입니다.</p>
<p class="look">가운데 노란 상자로 화살표 둘이 모입니다. 하나는 왼쪽 위 점수 칸에서 오고 하나는 오른쪽 초록 상자에서 옵니다. 그 초록 상자가 우리가 설정 칸에 넣은 기준값입니다.</p>
<p class="look">그 아래 보라 상자가 이 실습에서 부른 모델입니다. 맨 아래 노란 상자가 답까지 담긴 메시지 칸입니다. 이 흐름에서 임베딩 요청은 검색 자리 한 번뿐입니다.</p>

<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2>
<p>두 실행의 검색 결과는 같았습니다. 점수 칸은 두 번 모두 <code>7.64</code>였고 보고 자리 칸도 같았습니다. 기준값만 달라서 판단 이유 칸과 마지막에 지난 노드가 갈렸습니다.</p>
<table><thead><tr><th>실행</th><th>기준값 칸</th><th>점수 칸</th><th>판단 이유 칸</th><th>마지막에 지난 노드</th><th>메시지 수</th></tr></thead><tbody>
<tr><td>실행 1</td><td>5.0</td><td>7.64</td><td>자료가 넉넉함</td><td><code>make_reply</code></td><td>2</td></tr>
<tr><td>실행 2</td><td>9.0</td><td>7.64</td><td>자료가 모자람</td><td><code>ask_more</code></td><td>2</td></tr>
</tbody></table>
<p>메시지 수는 두 실행 모두 둘이었습니다. 처음 상태에 담은 사람 말 하나에 길 끝 노드가 메시지 하나를 더했기 때문입니다. 다만 그 하나가 실행 1에서는 모델이 쓴 답이고 실행 2에서는 우리가 적어 둔 안내 글입니다.</p>
{{mermaid:08-3-두-실행-비교|왼쪽부터 오른쪽으로 놓인 칸 두 개와 회색 상자 하나로 왼쪽 칸 제목은 기준값 5.0을 넣은 실행이고 그 안에 초록 상자 넣은 기준값 5.0과 노란 상자 판단 이유 칸 자료가 넉넉함과 노란 상자 마지막에 지난 노드 make_reply가 있으며 가운데 칸 제목은 기준값 9.0을 넣은 실행이고 그 안에 초록 상자 넣은 기준값 9.0과 노란 상자 판단 이유 칸 자료가 모자람과 노란 상자 마지막에 지난 노드 ask_more가 있고 오른쪽에 회색 상자 두 실행 모두 점수 칸 7.64와 보고 자리 칸이 같음이 놓인 그림|기준값 한 자리만 바꿨더니 판단 이유 칸과 마지막에 지난 노드가 갈렸습니다.}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 기준값을 낮게 둔 실행이고 가운데 칸이 높게 둔 실행입니다. 칸마다 맨 위 초록 상자가 우리가 넣은 값입니다.</p>
<p class="look">그 아래 노란 상자 둘이 출력으로 확인한 값입니다. 두 칸에서 판단 이유 칸과 마지막에 지난 노드가 갈렸습니다.</p>
<p class="look">오른쪽 회색 상자는 두 칸에서 모두 확인한 값입니다. 한 실행의 결과가 아니라서 어느 칸에도 넣지 않았습니다.</p>
<p>보고 자리 다섯의 부모 문서 차례는 두 실행 모두 <code>['E01', 'E02', 'H01']</code>이었습니다. 다섯 자리가 세 문서에서 왔다는 뜻입니다. 낱말 순위 1위 하나만 보는 기준값은 이렇게 섞인 자리를 가려내지 못합니다.</p>
<p>실행 1의 답에는 도서 대출 기간이 들어 있었고 끝에 출처 표시가 붙었습니다. 모델에 넣은 세 자리 가운데 대출 기간이 적힌 자리는 하나였습니다. 그 자리 수는 자료 파일에서 확인한 사실이고 노트북은 세 문서 청크의 본문을 출력하지 않았습니다. 모델 문장은 실행마다 달라질 수 있어 낱말을 확인 줄로 보지 않았습니다.</p>
<p>결론은 이렇습니다. 검색이 낸 값을 상태에 담아 두면 노드가 그 값으로 다음 길을 고를 수 있습니다. 설정 칸의 기준값 한 자리만 바꿔도 같은 검색 결과에서 지난 길이 갈립니다. 이 결과는 질문 하나·문서 청크 175개·기준값 두 값·한 번의 실행 범위입니다.</p>

<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2>
<ul>
<li><strong>점수는 낱말이 겹치는 정도입니다.</strong> 낱말 순위 1위의 점수는 질문 낱말이 그 문서 청크에 얼마나 겹치는지를 나타냅니다. 답이 맞는지, 근거가 있는지를 재는 값이 아닙니다.</li>
<li><strong>기준값 두 개는 탐색 실행 뒤 정한 예입니다.</strong> 점수가 <code>7.64</code>라는 것을 먼저 보고 <code>5.0</code>과 <code>9.0</code>을 잡았습니다. 두 길이 모두 보이게 하려고 정한 값이고 무엇을 재서 얻은 기준이 아닙니다.</li>
<li><strong>보고 자리가 섞여 있었습니다.</strong> 다섯 자리의 부모 문서가 셋이었습니다. 섞인 자리를 걸러 내는 방법은 이 실습에서 다루지 않습니다.</li>
<li><strong>답 두 개 가운데 하나만 모델 답입니다.</strong> 실행 2의 마지막 메시지는 우리가 손으로 만든 것입니다. 04절에서 본 것처럼 모델 역할 메시지라고 모두 모델이 쓴 답은 아닙니다.</li>
<li><strong>메시지 번호는 출력하지 않았습니다.</strong> 번호를 적지 않은 메시지에는 라이브러리가 번호를 붙이고 그 값은 실행마다 달라집니다.</li>
<li><strong>구조 문자열의 줄 차례는 실행 차례가 아닙니다.</strong> 실제로 지난 차례는 실행 흔적 칸에서 읽습니다. 06절에서 본 것과 같습니다.</li>
<li><strong>리랭커와 MMR은 쓰지 않았습니다.</strong> Ch 12 07·08절 리랭커는 모델 파일을 올리는 데 메모리와 시간이 들어 30분 실습에 넣지 않았습니다. 보고 자리는 합친 차례의 앞자리를 그대로 썼습니다.</li>
<li><strong>pgvector도 쓰지 않았습니다.</strong> Ch 12 01~03절 실습에는 Docker가 필요합니다. 이 실습은 07절과 같은 재료만으로 구성해 준비물을 줄였습니다.</li>
<li><strong>이 실습은 파일을 쓰지 않습니다.</strong> Ch 12 문서 파일은 읽기만 하고 고치지 않았습니다. 결과는 화면에만 냈습니다.</li>
<li><strong>걸린 시간은 이번에 재지 않았습니다.</strong> 노드로 나눠서 빨라졌는지 느려졌는지 적지 않습니다.</li>
<li><strong>임베딩 값은 호출마다 조금씩 달라집니다.</strong> 소수 자리까지 같다고 보지 말고 차례만 읽습니다. 낱말 겹침 점수는 모델을 부르지 않아 같은 질문에서 같은 값이 나옵니다.</li>
<li><strong>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.</strong> 패키지는 langgraph 1.2.11과 langchain 1.4.0, langchain-openai 1.6.1입니다. 패키지 kiwipiepy는 0.23.2이고 rank-bm25는 0.2.2, python-dotenv는 1.2.3입니다. 도구 파일이 쓰는 numpy는 2.5.3입니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li>
</ul>

<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2>
<ul>
<li>01절 노드와 07절 검색과 06절 <code>Command</code>와 04절 메시지 칸을 한 그래프에 붙였습니다.</li>
<li>노드 다섯과 고정 엣지 다섯으로 조립했고 갈래 두 자리는 <code>Command</code>가 정했습니다.</li>
<li>검색이 낸 점수 <code>7.64</code>를 기준값과 견줘 노드가 다음 길을 스스로 골랐습니다.</li>
<li>기준값을 <code>5.0</code>에서 <code>9.0</code>으로 바꾸자 판단 이유 칸과 마지막에 지난 노드가 갈렸습니다.</li>
<li>점수 칸과 보고 자리 칸은 두 실행에서 같았고 메시지 수도 둘로 같았습니다.</li>
</ul>
<p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 13이 끝납니다. Ch 14에서는 검색 앞뒤에 붙이는 RAG 패턴을 배웁니다. 질문 재작성과 여러 질문 만들기가 그 예입니다.</p>
<p>이 실습에서 고른 것은 길이고 답 품질은 재지 않았습니다. 답이 맞는지, 근거가 있는지, 출처 표기가 옳은지를 판정하는 일은 Ch 15 몫입니다. 들어온 글과 나가는 글을 막는 일은 Ch 16 몫입니다.</p>

<h2 id="b9"><span class="no">9</span>복습 문제</h2>
<details class="quiz" open><summary>문제 5개 · 해설 포함</summary>
<p class="quiz-q">1. [하] 두 실행에서 바꾼 값은 무엇입니까?</p>
<p class="quiz-a">설정 칸에 담은 기준값입니다. 실행 1은 <code>5.0</code>이고 실행 2는 <code>9.0</code>입니다. 질문과 문서, 두 순위에 줄 몫, 보고 자리 5, 모델은 같게 두었습니다.</p>
<p class="quiz-q">2. [중] 점수 칸은 누가 채웁니까?</p>
<p class="quiz-a">노드 <code>search_docs</code>가 채웁니다. 낱말 순위 1위의 점수를 그대로 담습니다. 03·06절에서는 같은 자리에 사람이 점수를 손으로 넣었습니다.</p>
<p class="quiz-q">3. [중] 고정 엣지가 다섯인데 길이 갈린 까닭은 무엇입니까?</p>
<p class="quiz-a">노드 <code>route</code>가 낸 <code>Command</code>가 다음 노드 이름을 함께 날랐기 때문입니다. 등록할 때 적은 목적지 둘은 구조 문자열에서 점선 두 줄로 나옵니다. 고정 엣지 수에는 들어가지 않습니다.</p>
<p class="quiz-q">4. [중] 두 실행의 보고 자리 칸이 같은데 답이 달라진 까닭은 무엇입니까?</p>
<p class="quiz-a">검색은 두 번 모두 같았지만 지난 노드가 달랐기 때문입니다. 실행 1은 <code>make_reply</code>로 가서 모델이 답을 썼고 실행 2는 <code>ask_more</code>로 가서 적어 둔 안내 글을 담았습니다.</p>
<p class="quiz-q">5. [상] 동료가 「점수가 기준값을 넘었으니 이 답은 믿을 만하다」라고 적었습니다. 이 절 출력으로 무엇이라고 답하나요?</p>
<p class="quiz-a">그 점수는 낱말이 겹치는 정도만 나타낸다고 답합니다. 이번 실행에서 보고 자리 다섯의 부모 문서는 <code>['E01', 'E02', 'H01']</code> 셋이었고 모델에 넣은 세 자리 가운데 대출 기간이 적힌 자리는 하나였습니다. 그 자리 수는 자료 파일에서 확인한 사실이고 노트북은 세 문서 청크의 본문을 출력하지 않았습니다. 답이 맞는지 판정하는 일은 Ch 15에서 따로 봅니다.</p>
</details>

<h2 id="b10"><span class="no">10</span>참고 자료</h2>
<ul>
<li><div><a href="https://docs.langchain.com/oss/python/langgraph/graph-api">LangGraph Graph API Command</a></div>확인 2026-09-19 · 1.2.11 기준 · 노드가 갱신과 다음 노드를 함께 내는 방법.</li>
<li><div><a href="https://reference.langchain.com/python/langgraph/graph/message/">LangGraph add_messages 리듀서</a></div>확인 2026-09-19 · 1.2.11 기준 · 메시지 목록 칸에 적는 리듀서 설명.</li>
<li><div><a href="https://developers.openai.com/api/docs/models/text-embedding-3-small">OpenAI text-embedding-3-small 모델 안내</a></div>확인 2026-09-19 · 문서 청크와 질문을 벡터로 바꿀 때 쓴 모델과 차원 수 설정.</li>
<li>06절 Command의 갱신과 이동 — 이 실습이 쓴 이동 방법과 목적지 적기를 정한 자리.</li>
<li>07절 RAG 통합과 시각화 — 이 실습이 노드 안에서 부른 Ch 12 검색 부품을 붙인 자리.</li>
<li>기준 버전은 langgraph 1.2.11과 langchain 1.4.0, langchain-openai 1.6.1입니다. 패키지 kiwipiepy는 0.23.2이고 rank-bm25는 0.2.2, python-dotenv는 1.2.3입니다. 도구 파일이 쓰는 numpy는 2.5.3입니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.</li>
</ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# LangGraph 기초 실습: 자료를 보고 답할지 되물을지 정하기

**이 노트북에서 할 일**

1. Ch 12 문서 청크로 도서관 안내 창구 그래프를 하나 만듭니다.
2. 검색이 낸 점수와 기준값을 견줘 노드가 다음 길을 스스로 고르게 합니다.
3. 기준값 한 자리만 바꿔 다시 실행하고 두 실행이 지난 길을 견줍니다.

**준비물** — 프로젝트 맨 위 폴더의 `.env`에 `OPENAI_API_KEY`가 있어야 합니다.
서비스 요청은 모두 네 번입니다.
임베딩은 문서 청크 한 번과 질문 두 번이고 답을 쓰는 모델은 실행 1에서 한 번입니다.
예상 비용은 네 번을 합쳐 미화 0.01달러 아래입니다.
실행 시간은 패키지 설치를 빼면 1분 안팎입니다.

**데이터** — 읽는 파일은 07절과 같은 Ch 12 문서 파일 하나입니다.

- `labs/part3/ch12-retrieval-tuning/data/advanced-documents.json`(부모 문서 6건·문서 청크 175개)

**이 노트북은 파일을 쓰지 않습니다** — 결과는 화면에만 냅니다.
Ch 12 파일은 읽기만 하고 고치지 않습니다.

**강의와 실습 범위** — 이 절은 이 챕터의 실습입니다.
강사와 함께 첫 셀부터 차례로 실행하고 따로 내는 과제는 없습니다.
9~12절의 출력 두 벌과 표를 함께 읽습니다.

정의 셀은 여덟 개이고 하나는 상태 형식, 일곱은 이 절이 만든 함수입니다.
앞 절에서 배운 함수 일곱 개는 도구 파일에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 일곱 개를 고정한 판으로 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part4/ch13-langgraph-basics`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 놓인 상자 일곱으로 맨 위 회색 상자 가상 시작점 START에서 화살표가 파란 상자 노드 normalize 질문 칸을 다듬음으로 이어지고 다시 파란 상자 노드 search_docs 보고 자리 칸과 점수 칸과 파란 상자 노드 route 판단 이유 칸과 다음 노드로 이어진 뒤 점선 화살표 둘이 파란 상자 노드 make_reply 모델을 부르는 노드와 파란 상자 노드 ask_more 적어 둔 안내 글로 갈라지고 두 상자가 맨 아래 회색 상자 가상 끝점 END로 모이는 그림](attachment:08-1-조립도.png)

위에서 아래로 읽습니다. 맨 위 회색 상자가 입력이 들어오는 자리입니다.

그 아래 파란 상자 다섯이 이 실습에서 만들 노드입니다.
셋째 상자에서 점선 화살표 둘이 갈라집니다.
점선은 노드가 낸 `Command`가 정하는 이동이고 실선은 우리가 적은 고정 엣지입니다.

### [2] markdown {}

## 1. 준비

첫 셀은 패키지 일곱 개를 설치하고 설치된 판 번호를 출력합니다.
07절과 같은 일곱 개입니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:24.411880Z', 'iopub.status.busy': '2026-09-21T09:06:24.411672Z', 'iopub.status.idle': '2026-09-21T09:06:24.875153Z', 'shell.execute_reply': '2026-09-21T09:06:24.874533Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langgraph==1.2.11" "langchain==1.4.0" "langchain-openai==1.6.1" "python-dotenv==1.2.3" "kiwipiepy==0.23.2" "rank-bm25==0.2.2" "numpy==2.5.3"
from importlib.metadata import version

print("langgraph:", version("langgraph"))
print("langchain:", version("langchain"))
print("langchain-openai:", version("langchain-openai"))
print("python-dotenv:", version("python-dotenv"))
print("kiwipiepy:", version("kiwipiepy"))
print("rank-bm25:", version("rank-bm25"))
print("numpy:", version("numpy"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langgraph: 1.2.11
langchain: 1.4.0
langchain-openai: 1.6.1
python-dotenv: 1.2.3
kiwipiepy: 0.23.2
rank-bm25: 0.2.2
numpy: 2.5.3

```

### [4] markdown {}

**결과 읽기** — 설치가 끝나면 판 번호 일곱 줄이 보입니다.
줄 `langgraph: 1.2.11`과 `rank-bm25: 0.2.2`가 보이면 다음 셀로 넘어갑니다.
마지막 줄 `numpy: 2.5.3`은 도구 파일이 벡터 계산에 쓰는 패키지입니다.
이 노트북의 출력은 2026-09-21에 이 판으로 실행한 결과입니다.

다음 셀은 이 실습이 쓸 이름 열여섯 개를 불러오고 도구 파일에서 함수 일곱 개를 가져옵니다.
01~06절에서 쓴 이름이 열하나이고 07절에서 쓴 이름이 다섯입니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 02절 노드 `normalize`와 07절에서 쓴 Ch 12 함수 여섯 개를 가져옵니다.
인자 모양은 5절에서 설명합니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:24.876244Z', 'iopub.status.busy': '2026-09-21T09:06:24.876158Z', 'iopub.status.idle': '2026-09-21T09:06:25.754111Z', 'shell.execute_reply': '2026-09-21T09:06:25.753605Z'}, 'lesson_role': 'setup'}

```python
# 01~06절 그래프 이름과 07절 검색 도구 이름을 함께 불러옵니다
import json
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langchain.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Command
from kiwipiepy import Kiwi
from rank_bm25 import BM25Okapi
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
# 02절 노드와 Ch 12 검색 함수 여섯 개를 도구 파일에서 가져옵니다
from rag_tools import fuse_rank, kiwi_terms, normalize, parent_ids_of
from rag_tools import rank_chunks_by_bm25, rank_chunks_by_distance, unique_chunk_ids

print("이 실습이 함께 쓰는 이름:", "add_messages", "Command", "OpenAIEmbeddings")
```

출력:
```
이 실습이 함께 쓰는 이름: add_messages Command OpenAIEmbeddings

```

### [6] markdown {}

**결과 읽기** — 출력 줄에 이 실습이 함께 쓰는 이름 셋이 보입니다.
리듀서 `add_messages`는 04절, 이동을 담는 `Command`는 06절, 임베딩을 만드는 `OpenAIEmbeddings`는 07절 이름입니다.
한 노트북에서 세 절 이름을 함께 쓰는 것이 이 실습의 자리입니다.
도구 파일에서 가져온 함수 일곱 개는 출력하지 않습니다.

## 2. 키와 모델 준비

이 챕터에서 모델을 부른 절은 07절 하나였습니다.
이 실습이 두 번째이자 마지막입니다.

### [7] markdown {}

API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [8] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:25.754962Z', 'iopub.status.busy': '2026-09-21T09:06:25.754864Z', 'iopub.status.idle': '2026-09-21T09:06:25.758364Z', 'shell.execute_reply': '2026-09-21T09:06:25.757996Z'}, 'lesson_role': 'setup'}

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

### [9] markdown {}

실습에 쓸 모델을 준비합니다.
temperature 값을 0으로 두어 매번 비슷한 문장을 고르게 합니다.
설정 `reasoning_effort="none"`은 답을 쓰기 전에 따로 생각하는 단계를 두지 않게 합니다.

### [10] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:25.759016Z', 'iopub.status.busy': '2026-09-21T09:06:25.758952Z', 'iopub.status.idle': '2026-09-21T09:06:25.835625Z', 'shell.execute_reply': '2026-09-21T09:06:25.835278Z'}}

```python
# 실습에 쓸 모델을 준비합니다
model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
)
print("모델 이름:", model.model_name)
print("temperature:", model.temperature)
```

출력:
```
모델 이름: gpt-5.4-mini
temperature: 0.0

```

### [11] markdown {}

**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 2026-09-21에 이 모델로 실행한 결과입니다.

### [12] markdown {}

## 3. 실습 주제 — 되물을지 답할지 노드가 정하기

작은 도서관 안내 창구를 맡았다고 봅니다.
이용자가 질문을 적으면 창구는 자료를 찾아보고 답을 씁니다.
찾은 자료에 질문 낱말이 거의 겹치지 않으면 답을 쓰는 대신 자료를 더 찾자고 적습니다.

이 판단을 노드 하나가 맡습니다.
06절 `Command`는 상태 갱신과 다음 노드 이름을 함께 냈습니다.
03·06절에서는 그 점수를 손으로 넣었지만 이번에는 검색이 낸 점수를 씁니다.

바꿔 볼 값은 기준값 한 자리입니다.
실행 1은 기준값을 낮게 두고 실행 2는 높게 둡니다.
질문과 문서와 두 순위에 줄 몫은 두 실행에서 같게 둡니다.

## 4. 재료 만들기 — Ch 12 자료와 값

먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다.
Ch 10~12와 07절에서 쓴 코드와 같습니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:25.836307Z', 'iopub.status.busy': '2026-09-21T09:06:25.836243Z', 'iopub.status.idle': '2026-09-21T09:06:25.838275Z', 'shell.execute_reply': '2026-09-21T09:06:25.837997Z'}, 'lesson_role': 'setup'}

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

### [14] markdown {}

**결과 읽기** — 출력 줄 `고른 경로` 뒤에 점 하나나 위로 올라가는 경로가 보입니다.
후보 셋 가운데 Ch 12 자료 폴더가 있는 자리를 고릅니다.

다음 셀은 Ch 12 문서 파일 하나를 읽습니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:25.838914Z', 'iopub.status.busy': '2026-09-21T09:06:25.838848Z', 'iopub.status.idle': '2026-09-21T09:06:25.841609Z', 'shell.execute_reply': '2026-09-21T09:06:25.841300Z'}, 'lesson_role': 'setup'}

```python
# Ch 12가 남긴 문서 파일을 읽습니다(읽기만 하고 고치지 않습니다)
chapter12_path = root_path + "/labs/part3/ch12-retrieval-tuning"
with open(chapter12_path + "/data/advanced-documents.json", encoding="utf-8") as file:
    documents = json.loads(file.read())
parents = documents["parents"]
chunks = documents["chunks"]
print("부모 문서 수:", len(parents))
print("문서 청크 수:", len(chunks))
```

출력:
```
부모 문서 수: 6
문서 청크 수: 175

```

### [16] markdown {}

**결과 읽기** — 출력 줄 `부모 문서 수: 6`과 `문서 청크 수: 175`가 07절과 같습니다.
Ch 12 07~13절이 쓴 자료와 같은 파일입니다.
07절이 함께 읽던 통합 기록 파일은 이번에 읽지 않습니다.
이 실습은 Ch 12 질문 대신 01절 질문을 씁니다.

다음 셀은 Ch 12에서 정한 값을 그대로 다시 적습니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:25.842160Z', 'iopub.status.busy': '2026-09-21T09:06:25.842115Z', 'iopub.status.idle': '2026-09-21T09:06:25.844095Z', 'shell.execute_reply': '2026-09-21T09:06:25.843707Z'}}

```python
# Ch 12 04~08절에서 정한 값을 그대로 다시 적습니다
keep_tags = ["NNG", "NNP", "NNB", "NR", "VV", "VA", "MAG", "SN", "SL"]
rank_constant = 60
report_place = 5
context_count = 3
equal_weights = [1.0, 1.0]
print("순위 상수:", rank_constant, "| 보고 자리:", report_place)
print("모델에 넣을 자리 수:", context_count)
print("두 순위에 줄 몫:", equal_weights)
```

출력:
```
순위 상수: 60 | 보고 자리: 5
모델에 넣을 자리 수: 3
두 순위에 줄 몫: [1.0, 1.0]

```

### [18] markdown {}

**결과 읽기** — 출력 줄 `순위 상수: 60 | 보고 자리: 5`는 Ch 12 06·08절 값입니다.
출력 줄 `모델에 넣을 자리 수: 3`은 보고 자리 앞에서 모델에 넣을 문서 청크 수입니다.
출력 줄 `두 순위에 줄 몫: [1.0, 1.0]`은 거리 순위와 낱말 순위를 같은 몫으로 합친다는 뜻입니다.
07절에서는 이 몫을 바꿔 봤지만 이번 실습에서는 두 실행 모두 같게 둡니다.

다음 셀은 이 실습이 쓸 질문과 기준값 두 개를 정합니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:25.844699Z', 'iopub.status.busy': '2026-09-21T09:06:25.844652Z', 'iopub.status.idle': '2026-09-21T09:06:25.846427Z', 'shell.execute_reply': '2026-09-21T09:06:25.846114Z'}}

```python
# 이 실습이 쓸 질문과 안내 글과 이번에 바꿔 볼 기준값 두 개를 정합니다
first_question = "  대출 기간은 며칠인가요?  "
notice_text = "자료를 더 찾아야 합니다"
low_gate = 5.0
high_gate = 9.0
prompt_head = "아래 자료만 보고 질문에 한국어로 답하세요.\n"
prompt_head = prompt_head + "답 끝에 [문서ID p.쪽] 모양으로 출처를 적으세요.\n\n"
print("첫 질문:", first_question)
print("첫 질문의 글자 수:", len(first_question))
print("실행 1 기준값:", low_gate, "| 실행 2 기준값:", high_gate)
print("자료가 모자랄 때 적어 둘 글:", notice_text)
```

출력:
```
첫 질문:   대출 기간은 며칠인가요?  
첫 질문의 글자 수: 17
실행 1 기준값: 5.0 | 실행 2 기준값: 9.0
자료가 모자랄 때 적어 둘 글: 자료를 더 찾아야 합니다

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `첫 질문의 글자 수: 17`은 01절부터 쓴 질문 그대로입니다.
앞뒤에 빈칸이 있어 노드 `normalize`가 할 일이 남아 있습니다.
출력 줄 `실행 1 기준값: 5.0 | 실행 2 기준값: 9.0`이 이번에 바꿀 자리입니다.
출력 줄 `자료가 모자랄 때 적어 둘 글: 자료를 더 찾아야 합니다`는 03·06절 답 칸 글과 같습니다.

다음 셀은 문서 청크마다 제목과 본문을 이어 붙이고 ID로 찾을 짝을 만듭니다.
07절과 같은 코드입니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:25.846953Z', 'iopub.status.busy': '2026-09-21T09:06:25.846894Z', 'iopub.status.idle': '2026-09-21T09:06:25.848992Z', 'shell.execute_reply': '2026-09-21T09:06:25.848755Z'}, 'lesson_role': 'setup'}

```python
# 문서 청크마다 제목과 본문을 이어 붙이고 ID로 부모와 쪽과 본문을 찾을 짝을 만듭니다
chunk_texts = []
chunk_ids = []
parent_by_chunk = {}
page_by_chunk = {}
text_by_chunk = {}
for chunk in chunks:
    chunk_text = chunk["title"] + " " + chunk["text"]
    chunk_texts.append(chunk_text)
    chunk_ids.append(chunk["chunk_id"])
    parent_by_chunk[chunk["chunk_id"]] = chunk["parent_id"]
    page_by_chunk[chunk["chunk_id"]] = chunk["page"]
    text_by_chunk[chunk["chunk_id"]] = chunk_text
all_chunk_count = len(chunk_ids)
print("이어 붙인 글 수:", all_chunk_count)
```

출력:
```
이어 붙인 글 수: 175

```

### [22] markdown {}

## 5. 앞 절 함수의 인자 확인하기

앞 절 함수 일곱 개는 준비 셀에서 도구 파일로부터 가져왔습니다.
02절 노드 `normalize`는 8절 조립에서 첫 노드로 그대로 씁니다.
Ch 12 함수 여섯 개는 07절과 같은 것을 같은 인자로 부릅니다.
노트북에서 만든 값은 함수 안에서 읽지 않고 인자로 넘깁니다.

함수 `rank_chunks_by_distance()`는 질문 벡터, 문서 청크 벡터 목록, 문서 청크 ID 목록, 남길 개수를 받습니다.
함수 `rank_chunks_by_bm25()`는 BM25 모델, 질문의 검색 낱말 목록, 문서 청크 ID 목록, 남길 개수를 받습니다.
질문의 검색 낱말은 `kiwi_terms()`에 형태소 분석기와 남길 품사 표시 목록을 함께 넘겨 만듭니다.
함수 `fuse_rank()`는 순위 상수를, `parent_ids_of()`는 부모 문서 짝을 인자로 받습니다.

리랭커와 MMR은 이 실습에서 쓰지 않아 가져오지 않았습니다.
보고 자리 다섯 개는 합친 차례의 앞자리를 그대로 씁니다.

## 6. 검색 재료 마무리 — BM25 모델과 문서 청크 벡터

다음 셀은 문서 청크의 검색 낱말 목록으로 BM25 모델을 만듭니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:25.849527Z', 'iopub.status.busy': '2026-09-21T09:06:25.849483Z', 'iopub.status.idle': '2026-09-21T09:06:27.198199Z', 'shell.execute_reply': '2026-09-21T09:06:27.197763Z'}}

```python
# 형태소 분석기를 만들고 문서 청크마다 검색 낱말 목록을 만들어 BM25 모델을 만듭니다
kiwi = Kiwi()
kiwi_corpus = []
for text_value in chunk_texts:
    kiwi_corpus.append(kiwi_terms(kiwi, text_value, keep_tags))
bm25_model = BM25Okapi(kiwi_corpus)
print("검색 낱말 목록 수:", len(kiwi_corpus))
print("BM25 모델이 본 문서 청크 수:", bm25_model.corpus_size)
```

출력:
```
검색 낱말 목록 수: 175
BM25 모델이 본 문서 청크 수: 175

```

### [24] markdown {}

**결과 읽기** — 출력 줄 `BM25 모델이 본 문서 청크 수: 175`가 문서 청크 수와 같습니다.
문서 청크 하나마다 검색 낱말 목록 하나를 만들었습니다.
이 셀은 서비스 요청을 보내지 않습니다.

다음 셀은 문서 청크를 벡터로 바꿉니다.
이 실습에서 서비스에 보내는 첫 요청입니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.198886Z', 'iopub.status.busy': '2026-09-21T09:06:27.198820Z', 'iopub.status.idle': '2026-09-21T09:06:27.561565Z', 'shell.execute_reply': '2026-09-21T09:06:27.560727Z'}}

```python
# Ch 12·07절과 같은 모델로 문서 청크를 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
chunk_vectors = embedding_model.embed_documents(chunk_texts)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 청크 벡터 수:", len(chunk_vectors))
```

출력:
```
임베딩 모델 이름: text-embedding-3-small
벡터의 숫자 개수 설정: 256
문서 청크 벡터 수: 175

```

### [26] markdown {}

**결과 읽기** — 출력 줄 `임베딩 모델 이름: text-embedding-3-small`은 Ch 9~12·07절과 같은 모델입니다.
출력 줄 `벡터의 숫자 개수 설정: 256`도 Ch 10~12와 같은 값입니다.
출력 줄 `문서 청크 벡터 수: 175`로 문서 청크마다 벡터 하나를 받았습니다.
벡터 안의 숫자는 호출마다 아주 조금씩 달라져 소수 자리까지 같다고 보지 않습니다.

## 7. 상태 형식과 결과를 볼 기록 장치

이 실습 상태에는 검색 결과와 판단과 대화가 모두 담깁니다.
칸 구성이 01~07절과 달라 형식 이름도 새로 붙입니다.
실행 흔적 칸에는 02절 규칙을, 메시지 칸에는 04절 리듀서를 적습니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.563274Z', 'iopub.status.busy': '2026-09-21T09:06:27.563136Z', 'iopub.status.idle': '2026-09-21T09:06:27.566359Z', 'shell.execute_reply': '2026-09-21T09:06:27.565855Z'}}

```python
# 이 실습 그래프가 쓸 상태 형식을 칸 일곱 개로 적습니다
class GuideState(TypedDict):
    question: str
    gate: float
    score: float
    picked_ids: list[str]
    decision: str
    messages: Annotated[list[AnyMessage], add_messages]
    trace: Annotated[list[str], operator.add]
```

출력:
```

```

### [28] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `gate`가 이번에 바꿔 볼 설정 자리이고 07절에서 「설정 칸」이라고 불렀습니다.
칸 `messages`와 칸 `trace`에만 규칙을 적었고 나머지 다섯 칸은 덮어쓰기가 됩니다.
한 상태에 칸마다 다른 리듀서를 적을 수 있다는 것은 04절에서 보았습니다.

다음 셀은 결과를 볼 기록 장치 둘입니다.
칸을 적는 함수와 메시지 목록을 적는 함수를 한 셀에 담았습니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.567811Z', 'iopub.status.busy': '2026-09-21T09:06:27.567684Z', 'iopub.status.idle': '2026-09-21T09:06:27.571465Z', 'shell.execute_reply': '2026-09-21T09:06:27.570811Z'}, 'upgrade_allow': ['multiple_defs_in_cell']}

```python
# 상태의 칸 일곱 개를 적는 함수와 메시지 목록을 적는 함수를 만듭니다
def print_state(label, state):
    print(label)
    print("질문 칸 |", state["question"])
    print("기준값 칸 |", state["gate"])
    print("점수 칸 |", state["score"])
    print("보고 자리 칸 |", state["picked_ids"])
    print("판단 이유 칸 |", state["decision"])
    print("메시지 칸의 메시지 수 |", len(state["messages"]))
    print("실행 흔적 칸 |", state["trace"])


def print_messages(label, messages):
    print(label)
    for message in messages:
        print(message.type, "|", message.text)
```

출력:
```

```

### [30] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
보고 자리 칸은 다섯 개라 값을 그대로 적고 메시지 칸은 개수만 적습니다.
여러 줄로 나오는 메시지 목록은 04절처럼 따로 출력합니다.
메시지 번호는 실행마다 달라져 출력하지 않습니다.

다음 셀은 실행 하나를 기록 한 줄로 만드는 함수입니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.572565Z', 'iopub.status.busy': '2026-09-21T09:06:27.572467Z', 'iopub.status.idle': '2026-09-21T09:06:27.575249Z', 'shell.execute_reply': '2026-09-21T09:06:27.574730Z'}}

```python
# 실행 한 번을 기록 한 줄로 만듭니다
def run_row(run_name, state):
    row = {"실행": run_name}
    row["기준값 칸"] = state["gate"]
    row["점수 칸"] = state["score"]
    row["판단 이유 칸"] = state["decision"]
    row["마지막에 지난 노드"] = state["trace"][-1]
    row["메시지 수"] = len(state["messages"])
    return row
```

출력:
```

```

### [32] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
06절 판과 견주면 기준값 칸과 메시지 수가 들어왔습니다.
이 실습이 견주는 값이 그 둘과 판단 이유 칸이기 때문입니다.

다음 셀은 기준값만 바꿔 처음 상태를 만드는 함수입니다.
03·06·07절에서 쓴 `new_state`와 같은 모양입니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.576379Z', 'iopub.status.busy': '2026-09-21T09:06:27.576282Z', 'iopub.status.idle': '2026-09-21T09:06:27.578841Z', 'shell.execute_reply': '2026-09-21T09:06:27.578284Z'}}

```python
# 기준값 칸만 다른 처음 상태를 만들어 냅니다
def new_state(gate_value):
    state = {"question": first_question, "gate": gate_value}
    state["score"] = 0.0
    state["picked_ids"] = []
    state["decision"] = ""
    state["messages"] = [HumanMessage(first_question)]
    state["trace"] = []
    return state
```

출력:
```

```

### [34] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
메시지 칸에는 이용자가 적은 글을 그대로 담습니다.
검색에 쓸 질문 칸은 노드 `normalize`가 다듬습니다.
나머지 칸은 빈 값으로 두고 노드가 채우게 합니다.

## 8. 노드 다섯 만들기

부품 하나를 노드 하나로 옮깁니다.
노드마다 자기가 채울 칸과 실행 흔적 칸에 자기 이름만 담아 냅니다.
02절이 정한 약속을 다섯 노드가 모두 지킵니다.

첫 노드 `normalize`는 02절에서 만든 노드를 도구 파일에서 가져왔습니다.
질문 칸의 앞뒤 빈칸을 없애고 메시지 칸은 건드리지 않습니다.
이 절에서 새로 만드는 노드는 나머지 넷입니다.
다음 노드가 07절 검색 부품 넷을 한 자리에 모읍니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.580003Z', 'iopub.status.busy': '2026-09-21T09:06:27.579913Z', 'iopub.status.idle': '2026-09-21T09:06:27.582774Z', 'shell.execute_reply': '2026-09-21T09:06:27.582207Z'}}

```python
# 두 순위를 합쳐 보고 자리를 남기고 낱말 순위 1위의 점수를 점수 칸에 담아 냅니다
def search_docs(state):
    question_vector = embedding_model.embed_query(state["question"])
    distance_hits = rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, all_chunk_count)
    question_terms = kiwi_terms(kiwi, state["question"], keep_tags)
    word_hits = rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, all_chunk_count)
    ranking_list = [unique_chunk_ids(distance_hits), unique_chunk_ids(word_hits)]
    fused_ids = fuse_rank(ranking_list, equal_weights, rank_constant)
    top_hit = word_hits[0]
    return {"picked_ids": fused_ids[:report_place], "score": top_hit["점수"], "trace": ["search_docs"]}
```

출력:
```

```

### [36] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드 안에서 질문 하나를 벡터로 바꾸는 요청이 한 번 나갑니다.
두 순위를 합친 차례에서 앞자리 다섯을 보고 자리 칸에 담습니다.
낱말 순위 1위의 점수를 점수 칸에 담아 다음 노드가 읽게 합니다.

다음 노드가 이 실습의 가운데입니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.583816Z', 'iopub.status.busy': '2026-09-21T09:06:27.583711Z', 'iopub.status.idle': '2026-09-21T09:06:27.586235Z', 'shell.execute_reply': '2026-09-21T09:06:27.585818Z'}}

```python
# 점수 칸과 설정 칸의 기준값을 견줘 갱신과 다음 노드 이름을 함께 담아 냅니다
def route(state):
    if state["score"] >= state["gate"]:
        return Command(update={"decision": "자료가 넉넉함", "trace": ["route"]}, goto="make_reply")
    return Command(update={"decision": "자료가 모자람", "trace": ["route"]}, goto="ask_more")
```

출력:
```

```

### [38] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드는 점수 칸과 설정 칸을 읽어 `Command` 하나를 냅니다.
담긴 갱신은 판단 이유 칸과 실행 흔적 칸이고 담긴 다음 노드 이름은 둘 가운데 하나입니다.
비교 `>=`는 기준값과 같은 점수를 넉넉한 쪽으로 보냅니다.

다음 노드가 자료가 넉넉할 때 지나는 길 끝입니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.587361Z', 'iopub.status.busy': '2026-09-21T09:06:27.587270Z', 'iopub.status.idle': '2026-09-21T09:06:27.589850Z', 'shell.execute_reply': '2026-09-21T09:06:27.589347Z'}}

```python
# 보고 자리 앞 세 자리의 본문과 출처 표시를 넣어 모델에게 답을 받습니다(모델 요청 1번)
def make_reply(state):
    context_text = ""
    for chunk_id in state["picked_ids"][:context_count]:
        source_label = "[" + parent_by_chunk[chunk_id] + " p." + str(page_by_chunk[chunk_id]) + "]"
        context_text = context_text + source_label + "\n" + text_by_chunk[chunk_id] + "\n\n"
    prompt_text = prompt_head + "질문: " + state["question"] + "\n\n자료:\n" + context_text
    reply = model.invoke(prompt_text)
    return {"messages": [reply], "trace": ["make_reply"]}
```

출력:
```

```

### [40] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
보고 자리 앞 세 자리의 본문과 출처 표시를 이어 붙여 넣습니다.
넣는 것은 쪽 전체가 아니라 문서 청크 본문입니다.
받은 답은 모델이 만든 메시지 그대로 메시지 칸에 담습니다.

다음 노드가 자료가 모자랄 때 지나는 길 끝입니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.590695Z', 'iopub.status.busy': '2026-09-21T09:06:27.590615Z', 'iopub.status.idle': '2026-09-21T09:06:27.592629Z', 'shell.execute_reply': '2026-09-21T09:06:27.592209Z'}}

```python
# 자료가 모자랄 때 지날 노드로 적어 둔 안내 글을 메시지 칸에 담아 냅니다
def ask_more(state):
    notice = AIMessage(notice_text)
    return {"messages": [notice], "trace": ["ask_more"]}
```

출력:
```

```

### [42] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드는 모델을 부르지 않고 적어 둔 글을 메시지 하나로 만듭니다.
그 메시지는 우리가 손으로 만든 것이고 모델이 쓴 답이 아닙니다.
04절에서 쓴 모양과 같습니다.

## 9. 조립과 구조 확인

설계 객체를 만들고 노드 다섯을 등록합니다.
노드 `route`에는 갈 수 있는 자리를 함께 적습니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.593555Z', 'iopub.status.busy': '2026-09-21T09:06:27.593481Z', 'iopub.status.idle': '2026-09-21T09:06:27.596519Z', 'shell.execute_reply': '2026-09-21T09:06:27.595995Z'}}

```python
# 설계 객체를 만들고 노드 다섯 개를 등록하면서 route의 목적지를 함께 적습니다
builder = StateGraph(GuideState)
builder.add_node("normalize", normalize)
builder.add_node("search_docs", search_docs)
builder.add_node("route", route, destinations=("make_reply", "ask_more"))
builder.add_node("make_reply", make_reply)
builder.add_node("ask_more", ask_more)
print("등록한 노드 수:", len(builder.nodes))
```

출력:
```
등록한 노드 수: 5

```

### [44] markdown {}

**결과 읽기** — 출력 줄 `등록한 노드 수: 5`가 보입니다.
07절과 같은 다섯이지만 갈래가 하나 있는 점이 다릅니다.

다음 셀은 고정 엣지만 적고 컴파일합니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.597546Z', 'iopub.status.busy': '2026-09-21T09:06:27.597462Z', 'iopub.status.idle': '2026-09-21T09:06:27.603525Z', 'shell.execute_reply': '2026-09-21T09:06:27.602993Z'}}

```python
# 고정 엣지 다섯 개를 적고 컴파일합니다
builder.add_edge(START, "normalize")
builder.add_edge("normalize", "search_docs")
builder.add_edge("search_docs", "route")
builder.add_edge("make_reply", END)
builder.add_edge("ask_more", END)
graph = builder.compile()
print("고정 엣지로 적은 수:", len(builder.edges))
print("컴파일 결과의 종류:", type(graph))
```

출력:
```
고정 엣지로 적은 수: 5
컴파일 결과의 종류: <class 'langgraph.graph.state.CompiledStateGraph'>

```

### [46] markdown {}

**결과 읽기** — 출력 줄 `고정 엣지로 적은 수: 5`가 보입니다.
노드가 낸 `Command`가 정하는 이동은 이 수에 들어가지 않습니다.
출력 줄의 종류 이름 `CompiledStateGraph`는 01절부터 같습니다.

다음 셀은 그래프가 스스로 그린 구조 문자열을 봅니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.604397Z', 'iopub.status.busy': '2026-09-21T09:06:27.604321Z', 'iopub.status.idle': '2026-09-21T09:06:27.609359Z', 'shell.execute_reply': '2026-09-21T09:06:27.608888Z'}}

```python
# 그래프가 스스로 그린 구조 문자열에서 화살표가 있는 줄만 골라 출력합니다
structure_text = graph.get_graph().draw_mermaid()
print("구조 문자열에서 화살표가 있는 줄")
for line in structure_text.split("\n"):
    if "-->" in line or "-.->" in line:
        print(line.strip())
```

출력:
```
구조 문자열에서 화살표가 있는 줄
__start__ --> normalize;
normalize --> search_docs;
route -.-> ask_more;
route -.-> make_reply;
search_docs --> route;
ask_more --> __end__;
make_reply --> __end__;

```

### [48] markdown {}

**결과 읽기** — 라벨 줄 아래 일곱 줄이 나옵니다.
실선 다섯 줄이 우리가 적은 고정 엣지입니다.
점선 두 줄 `route -.-> ask_more;`와 `route -.-> make_reply;`가 목적지를 적어 둔 자리입니다.
줄이 나온 차례는 실행 차례가 아니므로 아래 실행 흔적 칸과 함께 읽습니다.

## 10. 실행 1 · 기준값을 낮게

실행 전에 예상해 봅니다.
질문 낱말이 그대로 있는 문서 청크가 있어 점수가 기준값 5.0을 넘을 것입니다.
그러면 노드 `make_reply`로 가서 모델이 답을 쓸 것입니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:27.610328Z', 'iopub.status.busy': '2026-09-21T09:06:27.610253Z', 'iopub.status.idle': '2026-09-21T09:06:28.679844Z', 'shell.execute_reply': '2026-09-21T09:06:28.679096Z'}}

```python
# 기준값을 낮게 넣고 그래프를 실행합니다(임베딩 요청 1번·모델 요청 1번)
run1_state = new_state(low_gate)
run1_result = graph.invoke(run1_state)
print_state("실행 1 결과", run1_result)
run1_parents = parent_ids_of(run1_result["picked_ids"], parent_by_chunk)
print("보고 자리의 부모 문서 차례:", run1_parents)
print_messages("실행 1 메시지 칸", run1_result["messages"])
```

출력:
```
실행 1 결과
질문 칸 | 대출 기간은 며칠인가요?
기준값 칸 | 5.0
점수 칸 | 7.64
보고 자리 칸 | ['E01-P03-C02', 'E02-P05-C02', 'E02-P05-C01', 'E02-P03-C04', 'H01-P04-C01']
판단 이유 칸 | 자료가 넉넉함
메시지 칸의 메시지 수 | 2
실행 흔적 칸 | ['normalize', 'search_docs', 'route', 'make_reply']
보고 자리의 부모 문서 차례: ['E01', 'E02', 'H01']
실행 1 메시지 칸
human |   대출 기간은 며칠인가요?  
ai | 도서 대출 기간은 14일입니다. 영상 자료는 7일입니다. [E01 p.3]

```

### [50] markdown {}

**결과 읽기** — 출력 줄 `점수 칸 | 7.64`가 낱말 순위 1위의 점수입니다.
기준값 `5.0`보다 커서 출력 줄 `판단 이유 칸 | 자료가 넉넉함`이 나왔습니다.
출력 줄 `실행 흔적 칸 | ['normalize', 'search_docs', 'route', 'make_reply']`에 이름 넷이 남았습니다.
출력 줄 `보고 자리의 부모 문서 차례: ['E01', 'E02', 'H01']`로 보고 자리 다섯이 세 문서에서 왔습니다.
라벨 줄 `실행 1 메시지 칸` 아래 둘째 줄이 모델이 쓴 답이고 끝에 출처 표시가 붙었습니다.

## 11. 실행 2 · 기준값 한 자리만 올려서

바꿀 값은 기준값 하나입니다.
그래프도 노드도 질문도 그대로 두고 설정 칸만 바꿉니다.

실행 전에 예상해 봅니다.
점수는 같은 `7.64`인데 기준값이 9.0으로 올라 모자란 쪽으로 갈 것입니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:28.681720Z', 'iopub.status.busy': '2026-09-21T09:06:28.681603Z', 'iopub.status.idle': '2026-09-21T09:06:28.832834Z', 'shell.execute_reply': '2026-09-21T09:06:28.832300Z'}}

```python
# 기준값 한 자리만 올려 같은 그래프를 다시 실행합니다(임베딩 요청 1번)
run2_state = new_state(high_gate)
run2_result = graph.invoke(run2_state)
print_state("실행 2 결과", run2_result)
run2_parents = parent_ids_of(run2_result["picked_ids"], parent_by_chunk)
print("보고 자리의 부모 문서 차례:", run2_parents)
print_messages("실행 2 메시지 칸", run2_result["messages"])
```

출력:
```
실행 2 결과
질문 칸 | 대출 기간은 며칠인가요?
기준값 칸 | 9.0
점수 칸 | 7.64
보고 자리 칸 | ['E01-P03-C02', 'E02-P05-C02', 'E02-P05-C01', 'E02-P03-C04', 'H01-P04-C01']
판단 이유 칸 | 자료가 모자람
메시지 칸의 메시지 수 | 2
실행 흔적 칸 | ['normalize', 'search_docs', 'route', 'ask_more']
보고 자리의 부모 문서 차례: ['E01', 'E02', 'H01']
실행 2 메시지 칸
human |   대출 기간은 며칠인가요?  
ai | 자료를 더 찾아야 합니다

```

### [52] markdown {}

**결과 읽기** — 출력 줄 `점수 칸 | 7.64`는 실행 1과 같습니다.
기준값 `9.0`보다 작아서 출력 줄 `판단 이유 칸 | 자료가 모자람`이 나왔습니다.
출력 줄 `실행 흔적 칸 | ['normalize', 'search_docs', 'route', 'ask_more']`의 마지막 이름이 달라졌습니다.
라벨 줄 `실행 2 메시지 칸` 아래 둘째 줄은 적어 둔 안내 글이고 모델을 부르지 않았습니다.
출력 줄 `보고 자리 칸 | ['E01-P03-C02', 'E02-P05-C02', 'E02-P05-C01', 'E02-P03-C04', 'H01-P04-C01']`은 실행 1과 같습니다.

## 12. 두 실행을 기록 한 줄씩으로

마지막으로 두 실행의 기록을 한 표로 모읍니다.

실행 전에 예상해 봅니다.
점수 칸과 보고 자리 칸은 같고 판단 이유 칸과 마지막 노드만 갈릴 것입니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-21T09:06:28.833769Z', 'iopub.status.busy': '2026-09-21T09:06:28.833685Z', 'iopub.status.idle': '2026-09-21T09:06:28.836316Z', 'shell.execute_reply': '2026-09-21T09:06:28.835861Z'}}

```python
# 두 실행의 기록을 담아 라벨 줄 아래에 한 줄씩 출력합니다
run_rows = []
run_rows.append(run_row("실행 1", run1_result))
run_rows.append(run_row("실행 2", run2_result))
print("실행 | 기준값 칸 | 점수 칸 | 판단 이유 칸 | 마지막에 지난 노드 | 메시지 수")
for row in run_rows:
    print(row["실행"], "|", row["기준값 칸"], "|", row["점수 칸"], "|", row["판단 이유 칸"], "|", row["마지막에 지난 노드"], "|", row["메시지 수"])
print("두 실행의 점수 칸이 같은가:", run1_result["score"] == run2_result["score"])
print("두 실행의 보고 자리 칸이 같은가:", run1_result["picked_ids"] == run2_result["picked_ids"])
print("두 실행의 실행 흔적 칸이 같은가:", run1_result["trace"] == run2_result["trace"])
```

출력:
```
실행 | 기준값 칸 | 점수 칸 | 판단 이유 칸 | 마지막에 지난 노드 | 메시지 수
실행 1 | 5.0 | 7.64 | 자료가 넉넉함 | make_reply | 2
실행 2 | 9.0 | 7.64 | 자료가 모자람 | ask_more | 2
두 실행의 점수 칸이 같은가: True
두 실행의 보고 자리 칸이 같은가: True
두 실행의 실행 흔적 칸이 같은가: False

```

### [54] markdown {}

**결과 읽기** — 라벨 줄 아래 두 줄이 나옵니다.
두 줄의 점수 칸은 `7.64`로 같고 기준값 칸과 판단 이유 칸이 갈렸습니다.
출력 줄 `두 실행의 보고 자리 칸이 같은가: True`로 검색 결과는 같았습니다.
출력 줄 `두 실행의 실행 흔적 칸이 같은가: False`가 갈린 자리입니다.

## 정리

1. 01절 노드와 07절 검색과 06절 `Command`와 04절 메시지 칸을 한 그래프에 붙였습니다.
2. 검색이 낸 점수가 기준값을 넘는지에 따라 노드가 다음 길을 스스로 골랐습니다.
3. 설정 칸의 기준값 한 자리만 바꾸자 같은 검색 결과에서 지난 길이 갈렸습니다.

이 절로 Ch 13이 끝납니다. Ch 14에서는 검색 앞뒤에 붙이는 RAG 패턴을 배웁니다.

## 그림

### 08-1-조립도.mmd

```mermaid
flowchart TB
  %% classes
  s0["가상 시작점 START"]
  n1["normalize<br>질문 칸을 다듬음"]:::flow
  n2["search_docs<br>보고 자리 칸과 점수 칸"]:::flow
  n3["route<br>판단 이유 칸과 다음 노드"]:::flow
  n4["make_reply<br>모델을 부르는 노드"]:::flow
  n5["ask_more<br>적어 둔 안내 글"]:::flow
  e0["가상 끝점 END"]
  s0 --> n1
  n1 --> n2
  n2 --> n3
  n3 -.-> n4
  n3 -.-> n5
  n4 --> e0
  n5 --> e0
```

01~07절에서 만든 부품을 노드 다섯으로 잇고 가운데 노드가 다음 길을 스스로 고릅니다.

### 08-2-실행1-순서.mmd

```mermaid
flowchart TB
  %% classes
  q1["질문 칸<br>대출 기간은 며칠인가요?"]:::tool
  r1["search_docs가 낸<br>점수 칸 7.64"]:::measure
  g1["설정 칸에 넣은<br>기준값 5.0"]:::tool
  r2["route의 판단 이유 칸<br>자료가 넉넉함"]:::measure
  m1["모델 gpt-5.4-mini"]:::model
  r3["메시지 칸의<br>메시지 수 둘"]:::measure
  q1 --> r1
  r1 --> r2
  g1 --> r2
  r2 --> m1
  m1 --> r3
```

실행 1에서 검색이 낸 점수 7.64가 기준값 5.0을 넘어 모델을 부르는 길로 갔습니다.

### 08-3-두-실행-비교.mmd

```mermaid
flowchart LR
  %% classes
  subgraph run1["기준값 5.0을 넣은 실행"]
    direction TB
    a1["넣은 기준값<br>5.0"]:::tool
    a2["판단 이유 칸<br>자료가 넉넉함"]:::measure
    a3["마지막에 지난 노드<br>make_reply"]:::measure
    a1 ~~~ a2
    a2 ~~~ a3
  end
  subgraph run2["기준값 9.0을 넣은 실행"]
    direction TB
    b1["넣은 기준값<br>9.0"]:::tool
    b2["판단 이유 칸<br>자료가 모자람"]:::measure
    b3["마지막에 지난 노드<br>ask_more"]:::measure
    b1 ~~~ b2
    b2 ~~~ b3
  end
  same["두 실행 모두<br>점수 칸 7.64와<br>보고 자리 칸이 같음"]
  run1 ~~~ run2
  run2 ~~~ same
```

기준값 한 자리만 바꿨더니 판단 이유 칸과 마지막에 지난 노드가 갈렸습니다.

### 08-4-갈림길이-생긴-긴-길.prompt.md

# 08-4-갈림길이-생긴-긴-길 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 01절 길에는 작업대가 둘이었고 07절 길에는 다섯이 한 줄로 놓였습니다. 이번 길은 작업대 셋을 지난 뒤 셋째 작업대 위 표지판에서 둘로 갈라집니다. 갈래마다 작업대가 하나씩 더 있고 길은 그 자리에서 끝납니다.

구성 요소와 배치: 흰 바탕에 왼쪽에서 오른쪽으로 뻗은 나무 널판 길 하나가 있습니다(= 고정 엣지 다섯). 그 길 위에 같은 모양 작업대 **셋**이 한 줄로 놓입니다(= `normalize`·`search_docs`·`route`). 셋째 작업대 위에 글자 없는 나무 표지판이 서 있습니다(= 노드가 내놓는 `Command`의 다음 노드 이름). 그 작업대 뒤에서 길이 **둘**로 갈라지고 갈래마다 작업대가 하나씩 놓입니다(= `make_reply`와 `ask_more`).

시선 순서: 왼쪽 길 시작 → 작업대 셋 → 셋째 작업대 위 표지판 → 둘로 갈라진 길 → 갈래 끝 작업대 둘.

검수 기준: 그림만 보고 「작업대 셋이 한 줄로 있다」와 「셋째 작업대 위에 표지판이 있다」와 「그 뒤에서 길이 둘로 갈라져 작업대가 하나씩 더 있다」가 읽히는가.

01~07절 비유와의 관계: 01절 삽화의 나무 길과 작업대를 그대로 이어 씁니다. 03절은 길가 표지판, 06절은 작업대 위 표지판, 07절은 한 갈래 길에 작업대 다섯이었습니다. 이 절은 06절 표지판과 07절 긴 길을 함께 씁니다. Ch 9~12가 쓴 카드·봉투·서랍·쟁반·끈·단추·관과 깔때기는 뜻이 정해져 있어 쓰지 않았습니다. 02~06절 메모대로 프롬프트를 짧게 두고 세어서 읽히는 관계(작업대 셋 · 갈래 둘)로 잡았습니다.

## 프롬프트 (1차)

```text
Simple flat educational illustration, white background, limited soft palette,
clean outlines, plain everyday objects, no text, no letters, no numbers, no logos.

One wooden path runs from left to right and passes exactly three small wooden
workbenches standing in a single row. A blank wooden signboard stands on top of
the third workbench. Just behind that workbench the path splits into two
branches, and each branch ends at one more workbench.

No hands, no people, no screens, no monitors, no arrows.
```

## 상태

- 2026-09-19 · `nano_banana_pro`(응답 모델 이름 `nano_banana_2`) · 16:9 · 2k · `use_unlim: false` · 장당 2크레딧.
- **1차 job `6b2dd10a-680d-4338-afbf-bf97365639ce` 채택**: 검수 기준 세 가지가 모두 읽힙니다. 원본 해시 `93ce7016300f2583b3aa853f7abc9fbd5d49a24c64740833cef3ff3d8b98f80a`(2752 × 1536). 잔액 2691 → 2689.
- 02~07절 메모대로 프롬프트를 짧게 유지하고 세어서 읽히는 관계(작업대 셋 · 갈래 둘)로 잡았더니 한 번에 끝났습니다. 생성에서 결과까지 3분이 걸리지 않았습니다.
- **그림에서 확인한 것(그림 읽기·alt·캡션에 반영)**: 널판을 이어 붙인 길 하나가 왼쪽에서 오른쪽으로 뻗어 있고 같은 모양 작업대 **셋**이 그 위에 한 줄로 놓여 있습니다. 작업대마다 망치와 렌치 같은 연장이 놓여 있습니다(프롬프트에 적지 않은 요소라 「연장이 놓인」으로 alt에 적었습니다). 셋째 작업대 위에 글자 없는 나무 표지판이 서 있습니다. 그 작업대 뒤에서 길이 위아래 **두** 갈래로 갈라지고 갈래 끝마다 작업대가 하나씩 있습니다. 갈래 끝 작업대 둘은 길에서 조금 떨어져 놓였습니다. 글자·숫자는 없습니다.
- 저장: 폭 1100px로 줄여 `figures/08-4-갈림길이-생긴-긴-길.png`(1100 × 613). 원본 2752px는 저장하지 않았습니다. 저장 PNG를 채택 job 결과에서 같은 폭으로 줄인 그림과 픽셀 단위로 대조해 차이가 없음을 확인했습니다(`ImageChops.difference` bbox `None`, 세 칸 extrema 모두 `(0, 0)`, 규격 §5-4).

