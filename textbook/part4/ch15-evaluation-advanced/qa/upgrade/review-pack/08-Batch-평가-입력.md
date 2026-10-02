# 08-Batch-평가-입력

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 1h | 코드 notebooks/08-Batch-평가-입력.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>판정 요청을 네 칸짜리 요청 한 줄로 만들어 JSONL 입력 파일에 쓸 수 있습니다.</li>
<li>과정의 모델 설정을 요청 본문의 칸으로 옮겨 적을 수 있습니다.</li>
<li>제출 전에 네 칸·모델·겹친 요청 식별자를 검사할 수 있습니다.</li>
<li>결과 줄을 요청 식별자로 원래 요청과 이을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>07절 회귀 스위트는 판이 바뀔 때마다 같은 사례를 다시 판정합니다. 사례가 늘면 요청을 하나씩 보내고 받는 횟수도 늘어납니다. 요청을 파일 하나에 담아 한꺼번에 맡기면 결과도 나중에 파일로 한꺼번에 받습니다.</p><p>OpenAI 안내(2026-09-21 확인)에는 이 방식의 처리 기한이 24시간이라고 적혀 있습니다. 비용은 동기 요청보다 50% 싸다고도 적혀 있습니다. 한꺼번에 맡기려면 파일이 맞는 모양인지 먼저 봐야 합니다. 결과가 오면 어느 요청의 결과인지도 가려야 합니다. 이 절은 그 입력 파일을 만들고 검사합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>07절은 이전 판과 이후 판의 답을 같은 머리글 <code>rag-judge-v1.0.0</code>으로 판정했습니다. 두 판마다 사례 세 건이라 판정 요청은 여섯 번이었고, 한 번에 하나씩 보냈습니다. 요청 글은 파일로 남기지 않았습니다. 이후 판의 답 두 개는 07절에서 만든 답입니다.</p><p>판정 요청 글은 02절 함수 <code>build_judge_prompt</code>가 머리글 뒤에 두 칸을 이어 붙여 만듭니다. 모델은 02~07절 모두 <code>init_chat_model()</code>에 <code>temperature=0</code>과 <code>reasoning_effort="none"</code>을 주어 만들었습니다.</p><p>파일 형식 JSONL은 Ch 9 06절에서 배웠고, 한 줄에 JSON 하나를 둡니다. Ch 9 06절은 기록 한 줄을 <code>json.dumps()</code>로 바꿔 <code>with open(…, "w", encoding="utf-8")</code>로 썼습니다. 폴더가 없으면 <code>os.makedirs()</code>로 만들었습니다.</p><p>이 절은 02절 함수 <code>build_judge_prompt</code>를 다시 씁니다. 앞에서 배운 함수는 <code>rag_tools.py</code>에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(<code>notebooks/</code>)에 있는 파일입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>07절까지는 바구니를 하나씩 저울에 올려 바로 눈금을 읽었습니다. 이번에는 바구니 여섯 개를 나무 궤짝 하나에 담아 한꺼번에 맡깁니다. 바구니마다 색이 다른 이름표를 달아 둡니다. 결과가 나중에 오면 이름표를 보고 어느 바구니의 결과인지 찾습니다.</p><p>이 절은 궤짝에 바구니를 담고 이름표를 확인하는 데까지 합니다. 저울에는 아직 아무것도 올리지 않았습니다.</p>
{{img:08-5-궤짝에-담은-이름표-바구니|흰 바탕에 탁자가 있고 왼쪽에 뚜껑이 뒤로 열린 나무 궤짝 안에 짚 바구니 여섯 개가 두 줄로 세 개씩 놓여 바구니마다 빨간 사과가 한 알씩 들어 있으며 손잡이마다 하늘색 초록 노랑 분홍 주황 보라 빈 이름표가 하나씩 달려 있고 오른쪽에는 접시가 빈 둥근 눈금판 부엌 저울 하나가 서 있는 그림|바구니 여섯 개에 색이 다른 이름표를 달아 궤짝 하나에 담았고, 저울 접시는 아직 비어 있습니다.}}
<p class="look"><b>그림 읽기</b> — 뚜껑이 열린 나무 궤짝 안에 짚 바구니 여섯 개가 두 줄로 세 개씩 놓여 있습니다. 바구니마다 빨간 사과가 한 알씩 들어 있고, 손잡이에 빈 이름표가 하나씩 달려 있습니다. 여섯 이름표는 하늘색·초록·노랑·분홍·주황·보라로 색이 모두 다릅니다. 오른쪽 저울의 접시는 비어 있습니다. 바구니를 담고 이름표를 단 데까지가 이 절이고, 저울에는 아직 올리지 않았습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>일괄 처리(Batch API)</td><td>요청 여러 개를 파일 하나에 담아 한꺼번에 맡기고, 결과는 나중에 파일로 받는 방식입니다. 사과 바구니 여러 개를 궤짝 하나에 담아 맡기는 것과 같습니다.</td></tr><tr><td>요청 식별자(custom_id)</td><td>입력 파일의 요청 한 줄마다 붙이는 겹치지 않는 이름입니다. 궤짝 속 바구니마다 단 색이 다른 이름표와 같습니다.</td></tr><tr><td>요청 주소(url)</td><td>요청을 받을 서비스 기능의 주소입니다. 같은 가게에서도 창구마다 맡는 일이 다른 것과 같습니다.</td></tr><tr><td>요청 본문(body)</td><td>그 주소에 보낼 모델 이름·설정·메시지를 담은 칸입니다. 주문서에서 주문 내용을 적는 칸과 같습니다.</td></tr></tbody></table>
<p>새 용어를 이 절 코드에서 보면 이렇습니다. 일괄 처리의 입력은 요청 여섯 줄을 담은 <code>batch-eval-input.jsonl</code>입니다. 요청 식별자는 <code>old-Q002</code>처럼 판 표시와 질문 번호를 이은 이름입니다. 요청 주소는 <code>/v1/chat/completions</code>입니다. 요청 본문은 설정 세 칸과 메시지 목록입니다.</p>
{{mermaid:08-1-판정-요청-여섯-개를-입력-파일로|위에서 아래로 읽는 그림으로 초록 상자 평가 사례 세 건 이전 판 답 자료 파일과 초록 상자 이후 판 답 둘 Q002 Q090 07절에서 만든 답이 파란 상자 make_prompts 판정 요청 글 여섯 개 07절과 같은 글로 모이고, 파란 상자 make_batch_lines old new 판 표시와 질문 번호로 요청 식별자, 초록 상자 runs/batch-eval-input.jsonl 요청 여섯 줄, 노란 상자 제출 전 검사 네 칸 POST 주소 모델 어긋난 것 없음 겹친 요청 식별자 없음으로 이어진 뒤 점선을 따라 회색 상자 올리기 일괄 작업 만들기 결과 파일 받기 이번에 하지 않음으로 가는 그림|07절 판정 요청 여섯 개에 요청 식별자를 붙여 입력 파일에 쓰고 제출 전에 검사합니다. 올리기와 결과 받기는 하지 않았습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자 둘은 두 판의 답이고, 파란 <code>make_prompts</code>가 판정 요청 글 여섯 개를 만듭니다. 파란 <code>make_batch_lines</code>가 요청 식별자를 붙이고, 초록 입력 파일에 여섯 줄로 씁니다. 노란 상자는 노트북 6절에서 출력으로 확인한 검사입니다. 점선 끝 회색 상자는 제출 뒤에 할 일이고, 이 절에서는 하지 않았습니다.</p>
<h3>모델 설정을 본문 칸으로</h3><p>02~07절의 모델은 LangChain 함수 <code>init_chat_model()</code>로 만들었습니다. 이 과정의 LangChain 판은 그 요청을 주소 <code>/v1/chat/completions</code>로 보냅니다. 설정 <code>temperature=0</code>과 <code>reasoning_effort="none"</code>은 같은 이름의 본문 칸에 들어갑니다. 요청을 보내지 않고 설치한 판의 소스로 확인했습니다.</p><p>OpenAI 안내에는 요청 본문에 그 주소가 받는 칸을 그대로 적는다고 되어 있습니다. 그래서 본문에 <code>"temperature": 0</code>과 <code>"reasoning_effort": "none"</code>을 그대로 적었습니다. 모델 설명 문서에는 <code>gpt-5.4-mini</code>의 추론 설정 기본값이 <code>none</code>이라고 적혀 있습니다. 이 본문이 일괄 처리에서 받아들여지는지는 제출하지 않아 확인하지 않았습니다.</p>
<h3>제출 뒤의 차례 — 이번에 하지 않음</h3><p>OpenAI 안내에 적힌 차례는 이렇습니다. 입력 파일을 용도 <code>batch</code>로 올리고, 요청 주소와 처리 기한 <code>24h</code>를 정해 일괄 작업을 만듭니다. 상태를 확인하다가 끝나면 결과 파일과 오류 파일을 받습니다. 결과 줄에는 요청 식별자가 들어 있고, 줄 차례는 입력과 다를 수 있습니다. 이 절은 이 가운데 어느 것도 실행하지 않았습니다.</p>
<h3>다른 상황에 적용</h3><p>Ch 14의 RAG 흐름에서 질문 여러 개의 답을 한꺼번에 판정할 때도 같은 모양을 씁니다. 요청 식별자에 판 표시와 질문 번호를 넣어 두면 결과를 사례에 다시 이을 수 있습니다. 안내에 적힌 한도는 파일 하나에 요청 50,000개와 크기 200MB입니다. 이 절의 파일은 요청 여섯 줄입니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 07절 판정 요청 여섯 개를 같은 글로 다시 만듭니다. 요청마다 요청 식별자를 붙여 <code>runs/batch-eval-input.jsonl</code>에 여섯 줄로 씁니다. 파일을 다시 읽어 네 칸과 방식·주소·모델, 겹친 요청 식별자를 검사합니다. 마지막에 손으로 적은 결과 줄 다섯 개를 요청 식별자로 요청과 잇습니다.</p><p>모델 요청과 임베딩 요청은 0번이고 API 키를 쓰지 않습니다. 파일을 올리거나 일괄 작업을 만드는 요청도 보내지 않습니다. 새로 쓰는 파일은 입력 파일 하나입니다.</p>
{{mermaid:08-2-입력-파일-한-줄의-네-칸|왼쪽에서 오른쪽으로 읽는 그림으로 왼쪽 칸 입력 파일 첫 줄 네 칸에는 초록 상자 custom_id old-Q002, method POST, url /v1/chat/completions, body 요청 본문이 위에서 아래로 놓이고 왼쪽 칸에서 화살표가 오른쪽 칸 body 칸 안으로 이어지며 그 안에 초록 상자 model gpt-5.4-mini temperature 0 reasoning_effort none 02~07절 모델 설정과 같은 값과 초록 상자 messages 사용자 메시지 하나 판정 요청 글 3161자가 위아래로 놓인 그림|입력 파일 한 줄은 네 칸이고, 본문 칸에는 02~07절과 같은 설정 세 칸과 판정 요청 글 3161자가 들어 있습니다.}}
<p class="look"><b>도식 읽기</b> — 왼쪽에서 오른쪽으로 읽습니다. 왼쪽 칸은 입력 파일 첫 줄의 네 칸이고 모두 이 절이 쓴 값이라 초록입니다. 화살표를 따라 오른쪽 칸으로 가면 칸 <code>body</code> 안의 두 상자가 있습니다. 위 상자는 02~07절과 같은 설정 세 칸이고, 아래 상자는 판정 요청 글을 담은 메시지입니다.</p>
{{notebook:08-Batch-평가-입력}}
<p class="look"><b>확인할 점</b> — 2절 표 <code>Q002 | 3161 | 3160 | True</code>로 07절 요청 글과 같은지 봅니다. 5절 출력 <code>다시 읽은 줄 수: 6</code>과 <code>첫 줄의 칸: ['custom_id', 'method', 'url', 'body']</code>를 확인합니다. 6절 출력 <code>겹친 요청 식별자: []</code>와 8절의 겹친 세 이름도 봅니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 판의 판정 요청 글은 이전 판 3161·3183·5093자, 이후 판 3160·3183·5117자였습니다. 07절 노트북 출력의 글자 수와 모두 같았습니다. 요청 글을 07절과 같은 코드로 만들었으므로 같은 요청을 파일에 담은 것입니다.</p><p>입력 파일은 여섯 줄이었고, 다시 읽은 목록은 쓴 목록과 같았습니다. 여섯 줄 모두 네 칸이 맞았고 방식·주소·모델에 어긋난 것이 없었습니다. 겹친 요청 식별자도 없었습니다. 첫 줄은 3384자였습니다. 요청 글 안의 줄바꿈이 <code>\n</code>으로 적혀 요청 하나가 한 줄에 들어갔습니다.</p>
{{mermaid:08-3-판-표시를-뺀-요청-식별자|위쪽에 칸 둘이 나란히 있고 아래에 회색 상자 하나가 있는 그림으로 왼쪽 칸 판 표시 old new에는 파란 상자 make_batch_lines old-Q002부터 new-Q090에서 노란 상자 요청 식별자 여섯 개 겹친 요청 식별자 없음 네 칸 POST 주소 모델 어긋난 것 없음 파일에 씀으로, 오른쪽 칸 값 바꿔 보기 두 판 모두 judge에는 파란 상자 make_batch_lines judge-Q002부터 judge-Q090에서 노란 상자 겹친 요청 식별자 세 개 judge-Q002 judge-Q006 judge-Q090 파일에 쓰지 않음으로 이어지고, 맨 아래 회색 상자에 두 칸에서 같음 판정 요청 글 여섯 개 본문 설정 세 칸이 적힌 그림|요청 글과 본문은 그대로 두고 판 표시만 judge로 같게 바꾸자 요청 식별자 세 개가 겹쳤습니다.}}
<p class="look"><b>도식 읽기</b> — 두 칸의 제목이 판 표시입니다. 왼쪽 칸은 파일에 쓴 요청 식별자이고, 노란 상자는 겹친 것이 없다는 검사 결과입니다. 오른쪽 칸은 값 바꿔 보기이고, 노란 상자에 겹친 세 이름이 있습니다. 맨 아래 회색 상자는 두 칸에서 같은 요청 글과 본문 설정입니다.</p>
<p>값 바꿔 보기에서 두 판에 같은 표시 <code>judge</code>를 붙이자 요청 식별자 세 개가 두 번씩 나왔습니다. 겹친 이름은 <code>judge-Q002</code>·<code>judge-Q006</code>·<code>judge-Q090</code>이었습니다. 요청 글과 본문은 그대로였고 요청 식별자만 달라졌습니다. 이런 파일은 결과를 받아도 어느 판의 판정인지 가를 수 없습니다.</p><p>손으로 적은 결과 줄 다섯 개에서 결과가 없는 요청은 <code>old-Q006</code> 하나였습니다. 요청에 없는 결과는 없었습니다. 결과 줄 차례가 입력과 달라도 요청 식별자로 짝을 찾았습니다.</p>
{{mermaid:08-4-결과-줄을-요청-식별자로-잇기|위에서 아래로 읽는 그림으로 초록 상자 입력 파일의 요청 식별자 여섯 개 old-Q002 old-Q006 old-Q090 new-Q002 new-Q006 new-Q090과 초록 상자 손으로 적은 결과 줄 다섯 개 new-Q090부터 차례가 다름이 파란 상자 ids_not_in 인자 차례를 바꿔 두 번으로 모이고, 거기서 노란 상자 결과가 없는 요청 old-Q006과 노란 상자 요청에 없는 결과 없음으로 갈라지며, 맨 아래 회색 상자에 OpenAI 안내 결과 줄 차례는 입력과 다를 수 있음 실패한 요청은 오류 파일에 적힘 이번에 받은 결과 아님이 적힌 그림|손으로 적은 결과 줄 다섯 개는 차례가 달랐지만, 요청 식별자로 짝을 찾아 결과가 없는 old-Q006을 찾았습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 두 상자는 입력 파일의 요청 식별자와 손으로 적은 결과 줄입니다. 파란 <code>ids_not_in</code>을 인자 차례를 바꿔 두 번 부르면 노란 두 상자가 나옵니다. 맨 아래 회색 상자는 OpenAI 안내에 적힌 사실이고, 이번에 받은 결과가 아니라는 메모입니다.</p>
<p>새 커널로 두 번 실행했을 때 모든 셀의 출력이 같았고, 쓴 입력 파일도 바이트까지 같았습니다. 모델을 부르지 않고 정한 값만 쓰는 절이기 때문입니다. 형식 검사를 통과한 입력 파일은 제출 성공을 뜻하지 않습니다. 판정 결과와 비용도 이 파일만으로는 알 수 없습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절은 입력 파일까지 만들고 제출은 하지 않았습니다. 파일 올리기, 일괄 작업 만들기, 완료 기다리기, 결과 파일 받기는 이번에 실행하지 않았습니다.</li><li>처리 기한 24시간과 비용 50% 할인은 OpenAI 안내(2026-09-21 확인)에 적힌 사실입니다. 실제 걸린 시간과 청구 금액은 확인하지 않았습니다.</li><li>요청 본문의 칸 이름은 OpenAI 안내와 설치한 판의 소스로 확인했습니다. 이 본문이 일괄 처리에서 받아들여지는지는 확인하지 않았습니다.</li><li>요청 주소를 <code>/v1/responses</code>로 바꾸면 본문 모양도 달라집니다. OpenAI 추론 안내에 따르면 추론 설정은 칸 <code>reasoning</code> 안의 <code>effort</code>로 적습니다. 이 절은 그 모양으로 파일을 만들지 않았습니다.</li><li>일괄 처리로 받은 판정이 07절처럼 하나씩 보낸 판정과 같은지는 알 수 없습니다. 07절에서도 같은 요청의 판정이 실행한 때에 따라 달라질 수 있다고 적었습니다.</li><li>이후 판의 답 두 개는 07절에서 만든 답이고 자료 파일에 없습니다. 실제 새 판의 답이 아닙니다.</li><li>7절의 결과 줄 다섯 개는 흐름을 보여 주려고 손으로 적은 요청 식별자입니다. 실제 결과 줄에는 요청 식별자 말고도 응답과 오류를 담는 칸이 있습니다(OpenAI 안내).</li><li>겹친 요청 식별자가 든 파일을 실제로 올렸을 때 서비스가 어떻게 하는지는 실행하지 않았습니다. 안내에는 요청 식별자가 겹치면 안 된다고 적혀 있습니다.</li><li>입력 파일에는 API 키나 개인 정보를 넣지 않습니다. 이 파일에는 판정 머리글·답·근거 문서와 모델 설정만 들어 있습니다.</li><li>정한 값에서 나온 줄 수와 요청 식별자에만 <code>assert</code>를 썼습니다. 이 절에는 모델이 쓴 글이 없습니다.</li><li>모델 요청이 없어 비용이 들지 않았습니다. 일괄 처리에서 걸리는 시간은 재지 않았습니다.</li><li>노트북을 다시 실행하면 같은 이름의 입력 파일을 같은 내용으로 새로 씁니다.</li><li>LangSmith 화면과 업로드는 이번에 실행하지 않았습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>07절 판정 요청 여섯 개를 네 칸짜리 요청 한 줄씩 JSONL 입력 파일에 담았습니다.</li><li>제출 전에 네 칸·모델·겹친 요청 식별자를 검사했고, 판 표시를 빼면 세 개가 겹쳤습니다.</li><li>결과 줄은 차례가 달라도 요청 식별자로 원래 요청과 잇습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 09절은 이 챕터를 마무리하는 실습 절입니다. 이 입력 파일에서 두 줄씩 골라 평가 모델에 보내고 판정과 예상 비용을 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 입력 파일 한 줄에 들어가는 네 칸은 무엇입니까?</p><p class="quiz-a">요청 식별자(custom_id), 요청 방식(method), 요청 주소(url), 요청 본문(body)입니다. 이 절에서는 방식이 모두 POST이고 주소가 /v1/chat/completions였습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 02~07절의 모델 설정은 요청 본문에 어떻게 적었습니까?</p><p class="quiz-a">같은 이름의 본문 칸에 temperature 0과 reasoning_effort none을 적었습니다. 모델 이름은 앞의 openai: 없이 gpt-5.4-mini입니다. 틀렸다면 「핵심 개념」의 「모델 설정을 본문 칸으로」를 다시 읽습니다.</p><p class="quiz-q">3. 두 판에 같은 표시 judge를 붙여 요청 식별자를 만들면 무엇이 문제입니까?</p><p class="quiz-a">두 판의 같은 사례가 같은 이름을 받아 세 이름이 두 번씩 나옵니다. 결과 줄을 받아도 어느 판의 판정인지 가를 수 없습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p><p class="quiz-q">4. 제출 전 검사를 통과했다면 일괄 처리가 성공했다고 말할 수 있습니까?</p><p class="quiz-a">아닙니다. 이 절은 파일 모양과 요청 식별자만 확인했습니다. 파일 올리기, 완료, 결과, 비용은 실행하지 않았습니다. 틀렸다면 「주의할 점과 실무 메모」를 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://developers.openai.com/api/docs/guides/batch">Batch API</a></div>확인 2026-09-21 · 한 줄의 네 칸과 요청 식별자, 파일 하나에 모델 하나를 적은 안내입니다. 용도 batch, 처리 기한 24h, 50% 할인, 결과 줄 차례와 오류 파일도 적혀 있습니다.</li><li><div><a href="https://developers.openai.com/api/docs/models/gpt-5.4-mini">GPT-5.4 mini</a></div>확인 2026-09-21 · 추론 설정 기본값 none, 일괄 처리 지원.</li><li><div><a href="https://developers.openai.com/api/docs/guides/reasoning">Reasoning models</a></div>확인 2026-09-21 · Responses 주소의 추론 설정 모양 reasoning.effort.</li><li>Ch 9 06절 — JSONL과 기록 한 줄 쓰기, <code>os.makedirs()</code>.</li><li>07절 — 회귀 스위트와 판정 요청 여섯 개.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# Batch 평가 입력

**이 노트북에서 할 일**

1. 07절의 판정 요청 여섯 개를 같은 글로 다시 만듭니다.
2. 요청마다 요청 식별자를 붙여 입력 파일에 한 줄씩 씁니다.
3. 파일을 다시 읽어 네 칸·방식·주소·모델과 겹친 요청 식별자를 검사합니다.
4. 손으로 적은 결과 줄을 요청 식별자로 요청과 잇습니다.

**준비물** — 이 절은 OpenAI API 키를 쓰지 않습니다.
모델 요청과 임베딩 요청이 모두 0번이라 드는 비용이 없습니다.
요청을 보내지 않고, 한꺼번에 맡길 입력 파일만 만드는 절입니다.
파일을 서비스에 올리거나 일괄 작업을 만드는 요청도 보내지 않습니다.

읽는 파일은 이 챕터 자료 파일 하나입니다.
새로 쓰는 파일은 실습 폴더의 `runs/batch-eval-input.jsonl` 하나입니다.
교재 출력을 만든 실행에서는 노트북 전체가 몇 초 안에 끝났습니다.

**기준 버전** — 이 절은 Python에 들어 있는 기능과 도구 파일만 씁니다.
따로 설치할 패키지가 없어 설치 셀을 두지 않았습니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~6절을 읽습니다.
07절 요청 글을 다시 만들고, 입력 파일을 쓰고 검사하는 자리입니다.
7절은 결과 줄을 요청 식별자로 잇는 자리입니다.
8절은 값 바꿔 보기이고 7절과 함께 실습 시간에 실행합니다.

실습 폴더 `labs/part4/ch15-evaluation-advanced`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 그림으로 초록 상자 평가 사례 세 건 이전 판 답 자료 파일과 초록 상자 이후 판 답 둘 Q002 Q090 07절에서 만든 답이 파란 상자 make_prompts 판정 요청 글 여섯 개 07절과 같은 글로 모이고, 파란 상자 make_batch_lines old new 판 표시와 질문 번호로 요청 식별자, 초록 상자 runs/batch-eval-input.jsonl 요청 여섯 줄, 노란 상자 제출 전 검사 네 칸 POST 주소 모델 어긋난 것 없음 겹친 요청 식별자 없음으로 이어진 뒤 점선을 따라 회색 상자 올리기 일괄 작업 만들기 결과 파일 받기 이번에 하지 않음으로 가는 그림](attachment:08-1-판정-요청-여섯-개를-입력-파일로.png)

위에서 아래로 읽습니다. 초록 두 상자의 답으로 판정 요청 글 여섯 개를 만들고, 요청 식별자를 붙여 입력 파일에 씁니다.
노란 상자가 이 절에서 출력으로 확인한 검사이고, 점선 끝 회색 상자는 이 절에서 하지 않은 일입니다.

### [2] markdown {}

## 1. 준비

이 절은 따로 설치할 패키지가 없습니다.
첫 셀은 이 절에서 쓸 이름을 불러오고 Python 판을 출력합니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
이 노트북은 02절 `build_judge_prompt()` 하나만 가져옵니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.184716Z', 'iopub.status.busy': '2026-09-21T18:36:13.184507Z', 'iopub.status.idle': '2026-09-21T18:36:13.192236Z', 'shell.execute_reply': '2026-09-21T18:36:13.191481Z'}, 'lesson_role': 'setup'}

```python
# 입력 파일 쓰기·폴더 확인에 쓸 이름을 불러오고 Python 판을 출력합니다
import json
import os
import platform

# Ch 15 02절 함수 하나를 도구 파일에서 가져옵니다
from rag_tools import build_judge_prompt

print("불러온 이름:", "json", "os", "platform")
print("Python 판:", platform.python_version())
```

출력:
```
불러온 이름: json os platform
Python 판: 3.12.13

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `Python 판: 3.12.13`이 교재 출력을 만든 판입니다.
이름 `json`은 요청을 JSON 글로 바꿀 때, `os`는 폴더를 찾고 만들 때 씁니다.
도구 파일에서 가져온 함수는 출력하지 않습니다.
이 노트북의 출력은 2026-09-21에 실행한 결과입니다.

다음 셀은 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다.
01~07절과 같은 자리 찾기 셀입니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.193678Z', 'iopub.status.busy': '2026-09-21T18:36:13.193566Z', 'iopub.status.idle': '2026-09-21T18:36:13.197145Z', 'shell.execute_reply': '2026-09-21T18:36:13.196467Z'}, 'lesson_role': 'setup'}

```python
# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part4/ch15-evaluation-advanced/data"):
        root_path = candidate
        break
print("찾은 프로젝트 맨 위:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."
```

출력:
```
찾은 프로젝트 맨 위: .

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `찾은 프로젝트 맨 위:` 뒤에 점 하나나 위로 올라가는 자리가 보입니다.

## 2. 07절 판정 요청 글 다시 만들기

07절은 두 판의 답을 사례 세 건씩 판정해 판정 요청이 여섯 번이었습니다.
요청은 한 번에 하나씩 보냈고, 요청 글은 파일로 남기지 않았습니다.
이 절은 그 여섯 요청을 파일 하나에 담습니다.
먼저 07절과 같은 방법으로 이 챕터 자료 파일을 읽습니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.198489Z', 'iopub.status.busy': '2026-09-21T18:36:13.198371Z', 'iopub.status.idle': '2026-09-21T18:36:13.202843Z', 'shell.execute_reply': '2026-09-21T18:36:13.202346Z'}}

```python
# 이 챕터 자료 파일을 읽어 평가 사례 목록을 만들고 질문 번호를 모읍니다(읽기만 합니다)
data_path = root_path + "/labs/part4/ch15-evaluation-advanced/data"
with open(data_path + "/evaluation-cases.json", encoding="utf-8") as file:
    case_file = json.loads(file.read())
cases = case_file["cases"]
case_qids = []
for case in cases:
    case_qids.append(case["qid"])
print("평가 사례 수:", len(cases))
print("질문 번호:", case_qids)
```

출력:
```
평가 사례 수: 3
질문 번호: ['Q002', 'Q006', 'Q090']

```

### [8] markdown {}

**결과 읽기** — 출력 줄 `평가 사례 수: 3`으로 사례는 세 건입니다.
출력 줄 `질문 번호: ['Q002', 'Q006', 'Q090']`이 입력 파일에 담을 세 사례입니다.

다음 셀은 02절 근거 충실도의 판정 머리글을 다시 적습니다.
07절에서 다시 적은 머리글과 같은 코드입니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.204033Z', 'iopub.status.busy': '2026-09-21T18:36:13.203937Z', 'iopub.status.idle': '2026-09-21T18:36:13.206822Z', 'shell.execute_reply': '2026-09-21T18:36:13.206316Z'}}

```python
# 02절 근거 충실도의 두 칸 짝과 판정 머리글 rag-judge-v1.0.0을 다시 적습니다
ground_pair = {"답": "response", "근거 문서": "context"}
ground_rule = "답이 근거 문서로 뒷받침되면 1, 아니면 0을 판정하세요."
output_rule = 'JSON만 출력하세요: {"score": 0 또는 1, "reason": "한 문장"}.'
judge_version = "rag-judge-v1.0.0"
judge_head = ground_rule + "\n" + output_rule
print("판 이름:", judge_version)
print("머리글:")
print(judge_head)
```

출력:
```
판 이름: rag-judge-v1.0.0
머리글:
답이 근거 문서로 뒷받침되면 1, 아니면 0을 판정하세요.
JSON만 출력하세요: {"score": 0 또는 1, "reason": "한 문장"}.

```

### [10] markdown {}

**결과 읽기** — 출력 줄 `판 이름: rag-judge-v1.0.0`은 02절이 붙인 판 이름입니다.
라벨 줄 `머리글:` 아래 두 줄이 기준 문장과 출력 모양입니다.

다음 셀은 07절 이후 판에서 바뀐 답 두 개를 다시 적습니다.
07절과 같은 코드이고, 두 답은 자료 파일에 없는 07절에서 만든 답입니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.207794Z', 'iopub.status.busy': '2026-09-21T18:36:13.207704Z', 'iopub.status.idle': '2026-09-21T18:36:13.209961Z', 'shell.execute_reply': '2026-09-21T18:36:13.209563Z'}}

```python
# 이후 판에서 바뀐 답 두 개를 적습니다(이 절에서 만든 답이고, 나머지 사례의 답은 이전 판 그대로입니다)
new_answers = {}
new_answers["Q002"] = "도서는 한 번에 5권까지 빌릴 수 있고, 대출 기간은 7일입니다. [E01]"
new_answers["Q090"] = "계약서 본문에는 갑과 을 두 회사만 당사자로 적혀 있고 입회인은 적혀 있지 않습니다. 서명면은 스캔본으로 따로 첨부된다고만 적혀 있습니다. [H01]"
changed_qids = list(new_answers.keys())
print("답을 바꾼 사례:", changed_qids)
```

출력:
```
답을 바꾼 사례: ['Q002', 'Q090']

```

### [12] markdown {}

**결과 읽기** — 출력 줄 `답을 바꾼 사례: ['Q002', 'Q090']`이 이후 판에서 답이 바뀐 두 사례입니다.
사례 Q006의 답은 이후 판에서도 이전 판 그대로입니다.

다음 셀은 07절처럼 사례마다 복사본을 만듭니다.
바뀐 답이 있는 사례만 답 칸을 바꿔 이후 판 사례 목록을 만듭니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.211029Z', 'iopub.status.busy': '2026-09-21T18:36:13.210934Z', 'iopub.status.idle': '2026-09-21T18:36:13.213767Z', 'shell.execute_reply': '2026-09-21T18:36:13.213302Z'}}

```python
# 사례마다 복사본을 만들고, 바뀐 답이 있는 사례만 답 칸을 바꿔 이후 판 사례 목록을 만듭니다
new_cases = []
for case in cases:
    new_case = case.copy()
    if case["qid"] in new_answers:
        new_case["response"] = new_answers[case["qid"]]
    new_cases.append(new_case)
print("이후 판 사례 수:", len(new_cases))
```

출력:
```
이후 판 사례 수: 3

```

### [14] markdown {}

**결과 읽기** — 출력 줄 `이후 판 사례 수: 3`으로 이후 판도 사례 세 건입니다.
원래 목록 `cases`의 답은 그대로 남아 있습니다.

다음 셀은 사례 목록 하나로 판정 요청 글을 모두 만드는 함수입니다.
02절 함수 `build_judge_prompt()`를 사례마다 한 번씩 부릅니다.
모델에 보내지 않고 글만 만듭니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.214618Z', 'iopub.status.busy': '2026-09-21T18:36:13.214540Z', 'iopub.status.idle': '2026-09-21T18:36:13.216836Z', 'shell.execute_reply': '2026-09-21T18:36:13.216376Z'}}

```python
# 판정 머리글과 두 칸 짝으로 사례마다 판정 요청 글을 만들어 질문 번호별로 모읍니다(요청은 보내지 않습니다)
def make_prompts(judge_head, pair, case_list):
    prompts = {}
    for case in case_list:
        prompts[case["qid"]] = build_judge_prompt(judge_head, pair, case)
    return prompts
```

출력:
```

```

### [16] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `make_prompts`는 질문 번호가 키이고 판정 요청 글이 값인 딕셔너리를 만듭니다.
07절 `score_cases()`는 요청 글을 만들어 곧바로 보냈습니다.
이 함수는 글을 모으기만 합니다.

다음 셀은 두 판의 요청 글을 만들고 07절 노트북 5절 출력의 글자 수와 견줍니다.
07절 글자 수는 그 출력에서 옮겨 적은 값입니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.217660Z', 'iopub.status.busy': '2026-09-21T18:36:13.217590Z', 'iopub.status.idle': '2026-09-21T18:36:13.220193Z', 'shell.execute_reply': '2026-09-21T18:36:13.219840Z'}}

```python
# 두 판의 판정 요청 글을 만들고, 07절 노트북 5절 출력에 있던 글자 수와 견줍니다
old_prompts = make_prompts(judge_head, ground_pair, cases)
new_prompts = make_prompts(judge_head, ground_pair, new_cases)
old_lengths_07 = {"Q002": 3161, "Q006": 3183, "Q090": 5093}
new_lengths_07 = {"Q002": 3160, "Q006": 3183, "Q090": 5117}
print("질문 번호 | 이전 판 글자 수 | 이후 판 글자 수 | 07절과 같은가")
for qid in case_qids:
    old_length = len(old_prompts[qid])
    new_length = len(new_prompts[qid])
    same = old_length == old_lengths_07[qid] and new_length == new_lengths_07[qid]
    print(qid, "|", old_length, "|", new_length, "|", same)
```

출력:
```
질문 번호 | 이전 판 글자 수 | 이후 판 글자 수 | 07절과 같은가
Q002 | 3161 | 3160 | True
Q006 | 3183 | 3183 | True
Q090 | 5093 | 5117 | True

```

### [18] markdown {}

**결과 읽기** — 라벨 줄 `질문 번호 | 이전 판 글자 수 | 이후 판 글자 수 | 07절과 같은가` 아래 세 줄이 두 판의 요청 글입니다.
줄 `Q002 | 3161 | 3160 | True`처럼 세 줄 모두 07절 글자 수와 같았습니다.
사례 Q006은 두 판의 답이 같아 요청 글도 `3183`자로 같습니다.

글자 수가 같다고 글이 같다는 보장은 아닙니다.
이 절은 머리글, 두 칸 짝, 바뀐 답을 07절과 같은 코드로 적었습니다.
그래서 여섯 요청 글은 07절이 보낸 요청 글과 같은 글입니다.

## 3. 요청 한 줄의 모양

일괄 처리(Batch API)는 요청 여러 개를 파일 하나에 담아 한꺼번에 맡기는 방식입니다.
결과도 나중에 파일로 받습니다.
사과 바구니 여러 개를 궤짝 하나에 담아 맡기고 나중에 결과를 받는 것과 같습니다.
이 절에서는 판정 요청 여섯 개를 입력 파일 `batch-eval-input.jsonl` 하나에 담습니다.

입력 파일은 Ch 9 06절에서 배운 JSONL 형식이고, 한 줄에 요청 하나를 JSON으로 적습니다.
OpenAI 안내(2026-09-21 확인)에 따르면 한 줄에는 칸 네 개가 들어갑니다.
요청 식별자(`custom_id`), 요청 방식(`method`), 요청 주소(`url`), 요청 본문(`body`)입니다.

### [19] markdown {}

OpenAI 안내에 따르면 요청 본문에는 그 요청 주소가 받는 칸을 그대로 적습니다.
02~07절은 `init_chat_model()`에 `temperature=0`과 `reasoning_effort="none"`을 주었습니다.
이 과정의 LangChain 판은 이 설정의 요청을 주소 `/v1/chat/completions`로 보냅니다.

두 설정은 같은 이름의 본문 칸에 들어갑니다. 설치한 판의 소스로 확인했습니다.
다음 셀은 같은 주소와 같은 칸 이름을 적습니다.

### [20] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.221095Z', 'iopub.status.busy': '2026-09-21T18:36:13.221020Z', 'iopub.status.idle': '2026-09-21T18:36:13.223348Z', 'shell.execute_reply': '2026-09-21T18:36:13.222882Z'}}

```python
# 02~07절 모델 설정과 같은 값을 요청 본문의 칸 이름으로 적고, 요청을 보낼 주소도 적습니다
model_settings = {"model": "gpt-5.4-mini", "temperature": 0, "reasoning_effort": "none"}
request_url = "/v1/chat/completions"
print("본문 설정:", model_settings)
print("요청 주소:", request_url)
```

출력:
```
본문 설정: {'model': 'gpt-5.4-mini', 'temperature': 0, 'reasoning_effort': 'none'}
요청 주소: /v1/chat/completions

```

### [21] markdown {}

**결과 읽기** — 출력 줄 `본문 설정: {'model': 'gpt-5.4-mini', 'temperature': 0, 'reasoning_effort': 'none'}`이 본문에 넣을 설정 세 칸입니다.
출력 줄 `요청 주소: /v1/chat/completions`가 여섯 요청 모두의 요청 주소입니다.

모델 이름 앞의 `openai:`는 LangChain이 제공자를 고르는 표시라 본문에는 넣지 않습니다.
다음 셀은 요청 한 줄을 만드는 함수입니다.

### [22] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.224393Z', 'iopub.status.busy': '2026-09-21T18:36:13.224315Z', 'iopub.status.idle': '2026-09-21T18:36:13.226695Z', 'shell.execute_reply': '2026-09-21T18:36:13.226194Z'}}

```python
# 요청 식별자·주소·본문 설정·판정 요청 글로 입력 파일 한 줄에 들어갈 요청 하나를 만듭니다
def make_batch_line(custom_id, url, settings, prompt_text):
    body = settings.copy()
    body["messages"] = [{"role": "user", "content": prompt_text}]
    line = {"custom_id": custom_id, "method": "POST", "url": url, "body": body}
    return line
```

출력:
```

```

### [23] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `make_batch_line`은 요청 한 줄을 딕셔너리 하나로 만듭니다.
본문은 설정 딕셔너리의 복사본에 메시지 목록을 더한 것입니다.
메시지는 사용자 메시지 하나이고, 내용이 판정 요청 글입니다.

요청 방식은 모든 줄이 `POST`이고, 서버에 내용을 보내 처리를 맡기는 방식입니다.
설치판 소스로 보면 02~07절의 `invoke()`도 같은 주소에 사용자 메시지 하나로 보냈습니다.
다음 셀은 이전 판 Q002 요청 하나를 만들어 칸을 봅니다.

### [24] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.227578Z', 'iopub.status.busy': '2026-09-21T18:36:13.227491Z', 'iopub.status.idle': '2026-09-21T18:36:13.229963Z', 'shell.execute_reply': '2026-09-21T18:36:13.229550Z'}}

```python
# 이전 판 Q002 요청 하나를 만들어 한 줄의 칸과 본문의 칸을 봅니다(요청은 보내지 않습니다)
one_line = make_batch_line("old-Q002", request_url, model_settings, old_prompts["Q002"])
line_keys = list(one_line.keys())
body_keys = list(one_line["body"].keys())
print("요청 식별자:", one_line["custom_id"])
print("한 줄의 칸:", line_keys)
print("본문의 칸:", body_keys)
print("요청 글 글자 수:", len(one_line["body"]["messages"][0]["content"]))
print("설정 딕셔너리 칸 수:", len(model_settings))
```

출력:
```
요청 식별자: old-Q002
한 줄의 칸: ['custom_id', 'method', 'url', 'body']
본문의 칸: ['model', 'temperature', 'reasoning_effort', 'messages']
요청 글 글자 수: 3161
설정 딕셔너리 칸 수: 3

```

### [25] markdown {}

**결과 읽기** — 출력 줄 `요청 식별자: old-Q002`가 이 요청의 이름입니다.
출력 줄 `한 줄의 칸: ['custom_id', 'method', 'url', 'body']`가 한 줄의 네 칸입니다.
출력 줄 `본문의 칸: ['model', 'temperature', 'reasoning_effort', 'messages']`처럼 본문에는 설정 세 칸과 메시지 목록이 있습니다.
출력 줄 `요청 글 글자 수: 3161`은 2절 이전 판 Q002 요청 글과 같습니다.

출력 줄 `설정 딕셔너리 칸 수: 3`으로 원래 설정은 그대로입니다.
함수 안에서 `copy()`로 복사본을 만들어 메시지를 더했기 때문입니다.
04절에서 딕셔너리 `copy()`를 쓴 까닭과 같습니다.

## 4. 요청 여섯 줄

요청 식별자(custom_id)는 요청 한 줄마다 붙이는 겹치지 않는 이름입니다.
궤짝에 담은 바구니마다 색이 다른 이름표를 달아 두는 것과 같습니다.
OpenAI 안내에는 결과 파일의 줄 차례가 입력 차례와 다를 수 있다고 적혀 있습니다.
그래서 결과 줄마다 붙어 오는 요청 식별자로 원래 요청을 찾습니다.

이 절은 판 표시와 질문 번호를 이어 요청 식별자를 만듭니다.
이전 판은 `old`, 이후 판은 `new`를 앞에 붙입니다.
다음 셀은 판정 요청 글 모음 하나로 요청 줄 목록을 만드는 함수입니다.

### [26] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.230878Z', 'iopub.status.busy': '2026-09-21T18:36:13.230795Z', 'iopub.status.idle': '2026-09-21T18:36:13.232899Z', 'shell.execute_reply': '2026-09-21T18:36:13.232462Z'}}

```python
# 판 표시와 질문 번호를 이어 요청 식별자를 붙이고, 판정 요청 글마다 요청 한 줄씩 만듭니다
def make_batch_lines(version_tag, prompts, url, settings):
    lines = []
    for qid in prompts:
        custom_id = version_tag + "-" + qid
        lines.append(make_batch_line(custom_id, url, settings, prompts[qid]))
    return lines
```

출력:
```

```

### [27] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `make_batch_lines`는 판정 요청 글마다 요청 식별자를 붙여 `make_batch_line()`을 부릅니다.
요청 식별자는 판 표시, 줄표 `-`, 질문 번호를 이어 붙인 글입니다.
요청 줄은 질문 번호 차례대로 목록에 모입니다.

다음 셀은 두 판의 요청 줄을 만들어 한 목록으로 잇습니다.
목록 두 개를 `+`로 이으면 앞 목록 뒤에 뒤 목록을 붙인 새 목록이 됩니다.

### [28] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.233665Z', 'iopub.status.busy': '2026-09-21T18:36:13.233601Z', 'iopub.status.idle': '2026-09-21T18:36:13.235879Z', 'shell.execute_reply': '2026-09-21T18:36:13.235515Z'}}

```python
# 이전 판에는 old, 이후 판에는 new를 붙여 요청 여섯 줄을 만들고 요청 식별자를 차례로 봅니다
old_lines = make_batch_lines("old", old_prompts, request_url, model_settings)
new_lines = make_batch_lines("new", new_prompts, request_url, model_settings)
batch_lines = old_lines + new_lines
print("요청 수:", len(batch_lines))
print("요청 식별자:")
for line in batch_lines:
    print(line["custom_id"])
```

출력:
```
요청 수: 6
요청 식별자:
old-Q002
old-Q006
old-Q090
new-Q002
new-Q006
new-Q090

```

### [29] markdown {}

**결과 읽기** — 출력 줄 `요청 수: 6`으로 요청은 여섯 줄입니다.
라벨 줄 `요청 식별자:` 아래 여섯 줄이 요청 식별자이고, `old-Q002`부터 `new-Q090`까지입니다.

사례 Q006은 두 판의 요청 글이 같아 본문도 같습니다.
그래도 요청 식별자가 `old-Q006`과 `new-Q006`으로 달라 두 줄로 따로 들어갑니다.
07절 회귀 스위트처럼 두 판의 사례를 모두 판정하려는 것이라 빼지 않았습니다.

## 5. 입력 파일 쓰기와 다시 읽기

이 챕터에서 파일을 쓰는 것은 이 절이 처음입니다.
Ch 9 06절처럼 요청 하나를 `json.dumps()`로 JSON 글 한 줄로 바꾸고 줄바꿈을 붙입니다.
인자 `ensure_ascii=False`는 한글을 알아볼 수 있는 글자 그대로 적게 합니다.

파일은 `with open(…, "w", encoding="utf-8")`로 엽니다.
이미 있는 파일이면 내용을 지우고 새로 씁니다.
다음 셀은 요청 목록을 JSONL 파일로 쓰는 함수입니다.

### [30] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.236774Z', 'iopub.status.busy': '2026-09-21T18:36:13.236709Z', 'iopub.status.idle': '2026-09-21T18:36:13.238904Z', 'shell.execute_reply': '2026-09-21T18:36:13.238520Z'}}

```python
# 요청 목록을 받아 요청 하나를 JSON 글 한 줄로 바꿔 파일에 차례로 씁니다(파일이 있으면 새 내용으로 바꿔 씁니다)
def write_jsonl(file_path, lines):
    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(json.dumps(line, ensure_ascii=False) + "\n")
```

출력:
```

```

### [31] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `write_jsonl`은 파일 하나를 열고 요청마다 JSON 글 한 줄을 씁니다.
줄마다 끝에 줄바꿈 `\n`을 붙여 요청 하나가 한 줄이 되게 합니다.
들여 쓴 `with` 블록이 끝나면 파일이 닫힙니다.

다음 셀은 실습 폴더의 runs 폴더에 입력 파일을 씁니다.
폴더가 없으면 Ch 9 06절처럼 `os.makedirs()`로 먼저 만듭니다.
쓴 파일은 이름만 출력합니다.

### [32] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.239716Z', 'iopub.status.busy': '2026-09-21T18:36:13.239653Z', 'iopub.status.idle': '2026-09-21T18:36:13.246915Z', 'shell.execute_reply': '2026-09-21T18:36:13.246429Z'}}

```python
# 실습 폴더의 runs 폴더에 입력 파일을 씁니다(폴더가 없으면 먼저 만듭니다)
runs_path = root_path + "/labs/part4/ch15-evaluation-advanced/runs"
if not os.path.exists(runs_path):
    os.makedirs(runs_path)
batch_path = runs_path + "/batch-eval-input.jsonl"
write_jsonl(batch_path, batch_lines)
print("쓴 파일 이름:", "batch-eval-input.jsonl")
print("파일이 있는가:", os.path.exists(batch_path))
```

출력:
```
쓴 파일 이름: batch-eval-input.jsonl
파일이 있는가: True

```

### [33] markdown {}

**결과 읽기** — 출력 줄 `쓴 파일 이름: batch-eval-input.jsonl`이 이 절이 쓴 파일입니다.
출력 줄 `파일이 있는가: True`로 파일이 생긴 것을 확인했습니다.
파일은 실습 폴더의 `runs/` 안에 있습니다.

노트북을 다시 실행하면 같은 이름의 파일을 같은 내용으로 새로 씁니다.
요청을 보내지 않고 정한 값만 쓰기 때문입니다.
다음 셀은 JSONL 파일을 읽는 함수입니다.

### [34] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.247680Z', 'iopub.status.busy': '2026-09-21T18:36:13.247613Z', 'iopub.status.idle': '2026-09-21T18:36:13.249883Z', 'shell.execute_reply': '2026-09-21T18:36:13.249460Z'}}

```python
# JSONL 파일을 읽어 빈 줄을 뺀 줄마다 JSON으로 읽고 딕셔너리 목록을 만듭니다
def read_jsonl(file_path):
    with open(file_path, encoding="utf-8") as file:
        text_lines = file.read().split("\n")
    rows = []
    for text_line in text_lines:
        if text_line != "":
            rows.append(json.loads(text_line))
    return rows
```

출력:
```

```

### [35] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `read_jsonl`은 파일 글을 줄바꿈으로 나눈 뒤 줄마다 `json.loads()`로 읽습니다.
파일 끝 줄바꿈 뒤에는 빈 글이 하나 남아 `!= ""`로 건너뜁니다.
Ch 9 06절에서 JSONL 파일을 `split("\n")`으로 나눠 읽은 방법과 같습니다.

다음 셀은 방금 쓴 파일을 다시 읽습니다.
쓴 대로 읽히는지 보려면 파일을 다시 읽어 봐야 합니다.

### [36] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.250615Z', 'iopub.status.busy': '2026-09-21T18:36:13.250552Z', 'iopub.status.idle': '2026-09-21T18:36:13.253256Z', 'shell.execute_reply': '2026-09-21T18:36:13.252907Z'}}

```python
# 방금 쓴 파일을 다시 읽어 줄 수와 첫 줄의 칸을 보고, 쓴 목록과 같은지 견줍니다
loaded_lines = read_jsonl(batch_path)
first_keys = list(loaded_lines[0].keys())
print("다시 읽은 줄 수:", len(loaded_lines))
print("첫 줄의 칸:", first_keys)
print("쓴 목록과 같은가:", loaded_lines == batch_lines)
assert len(loaded_lines) == len(batch_lines)
```

출력:
```
다시 읽은 줄 수: 6
첫 줄의 칸: ['custom_id', 'method', 'url', 'body']
쓴 목록과 같은가: True

```

### [37] markdown {}

**결과 읽기** — 출력 줄 `다시 읽은 줄 수: 6`으로 파일에는 요청 여섯 줄이 있습니다.
출력 줄 `첫 줄의 칸: ['custom_id', 'method', 'url', 'body']`가 첫 줄의 네 칸입니다.
출력 줄 `쓴 목록과 같은가: True`로 쓴 요청 목록과 읽은 목록이 같습니다.
줄 수는 정한 값에서 나온 결과라 `assert`로도 확인했습니다.

다음 셀은 파일 글을 그대로 읽어 JSONL 한 줄이 어떻게 생겼는지 봅니다.
글의 메서드 `count()`는 괄호 안에 준 글이 몇 번 나오는지 셉니다.

### [38] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.254024Z', 'iopub.status.busy': '2026-09-21T18:36:13.253960Z', 'iopub.status.idle': '2026-09-21T18:36:13.256844Z', 'shell.execute_reply': '2026-09-21T18:36:13.256425Z'}}

```python
# 파일 글을 그대로 읽어 줄바꿈 수와 첫 줄의 글자 수, 첫 줄의 앞부분을 봅니다
with open(batch_path, encoding="utf-8") as file:
    file_text = file.read()
first_text = file_text.split("\n")[0]
print("줄바꿈 수:", file_text.count("\n"))
print("첫 줄 글자 수:", len(first_text))
print("첫 줄 앞부분:")
print(first_text[:154])
```

출력:
```
줄바꿈 수: 6
첫 줄 글자 수: 3384
첫 줄 앞부분:
{"custom_id": "old-Q002", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5.4-mini", "temperature": 0, "reasoning_effort": "none",

```

### [39] markdown {}

**결과 읽기** — 출력 줄 `줄바꿈 수: 6`으로 파일은 여섯 줄입니다.
출력 줄 `첫 줄 글자 수: 3384`는 첫 줄 전체의 글자 수입니다.
라벨 줄 `첫 줄 앞부분:` 아래는 첫 줄의 앞 154글자이고, 칸 `"messages"` 앞까지입니다.

첫 줄은 요청 글 3161자보다 깁니다.
요청 글 안의 줄바꿈이 파일에서는 `\n` 두 글자로 적히기 때문입니다.
글 안의 큰따옴표도 `\"` 두 글자로 적히고, 칸 이름도 함께 들어갑니다.
그래서 요청 글에 줄바꿈이 있어도 요청 하나는 파일에서 한 줄로 남습니다.

## 6. 제출 전 검사

OpenAI 안내에는 입력 파일 하나에 모델 하나만 쓸 수 있다고 적혀 있습니다.
요청 식별자는 파일 안에서 겹치면 안 된다고도 적혀 있습니다.
이 절은 파일을 올리지 않으므로, 이 두 가지를 우리 코드로 먼저 검사합니다.
다음 셀은 요청 한 줄의 방식·주소·모델이 정한 값과 같은지 보는 함수입니다.

### [40] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.257619Z', 'iopub.status.busy': '2026-09-21T18:36:13.257560Z', 'iopub.status.idle': '2026-09-21T18:36:13.259563Z', 'shell.execute_reply': '2026-09-21T18:36:13.259268Z'}}

```python
# 요청 한 줄의 방식·주소·모델이 정한 값과 같은지 보고, 어긋난 것의 이름을 목록으로 모읍니다(네 칸이 있는 줄만 넣습니다)
def line_problems(line, url, model_name):
    problems = []
    if line["method"] != "POST":
        problems.append("방식이 POST가 아님")
    if line["url"] != url:
        problems.append("주소가 다름")
    if line["body"]["model"] != model_name:
        problems.append("모델이 다름")
    return problems
```

출력:
```

```

### [41] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `line_problems`는 방식이 `POST`인지, 주소와 모델이 정한 값과 같은지 봅니다.
어긋난 것이 있으면 그 이름을 목록에 모으고, 없으면 빈 목록 `[]`를 냅니다.
네 칸이 모두 있는 줄만 넣습니다. 칸이 빠진 줄이면 그 칸을 읽는 자리에서 `KeyError`가 납니다.

다음 셀은 다시 읽은 여섯 줄을 한 줄씩 검사합니다.
네 칸의 이름과 차례가 맞는지도 함께 봅니다.

### [42] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.260378Z', 'iopub.status.busy': '2026-09-21T18:36:13.260310Z', 'iopub.status.idle': '2026-09-21T18:36:13.262764Z', 'shell.execute_reply': '2026-09-21T18:36:13.262456Z'}}

```python
# 다시 읽은 여섯 줄마다 네 칸이 맞는지와 어긋난 것을 보고, 요청 글 글자 수도 봅니다
expected_keys = ["custom_id", "method", "url", "body"]
print("요청 식별자 | 네 칸이 맞는가 | 어긋난 것 | 요청 글 글자 수")
for line in loaded_lines:
    keys_ok = list(line.keys()) == expected_keys
    problems = line_problems(line, request_url, model_settings["model"])
    content = line["body"]["messages"][0]["content"]
    print(line["custom_id"], "|", keys_ok, "|", problems, "|", len(content))
```

출력:
```
요청 식별자 | 네 칸이 맞는가 | 어긋난 것 | 요청 글 글자 수
old-Q002 | True | [] | 3161
old-Q006 | True | [] | 3183
old-Q090 | True | [] | 5093
new-Q002 | True | [] | 3160
new-Q006 | True | [] | 3183
new-Q090 | True | [] | 5117

```

### [43] markdown {}

**결과 읽기** — 라벨 줄 `요청 식별자 | 네 칸이 맞는가 | 어긋난 것 | 요청 글 글자 수` 아래 여섯 줄이 검사 결과입니다.
줄 `old-Q002 | True | [] | 3161`처럼 여섯 줄 모두 네 칸이 맞고 어긋난 것이 없습니다.
끝 칸의 글자 수는 `3161`부터 `5117`까지 2절 표의 글자 수와 같습니다.

파일에 쓰고 다시 읽어도 요청 글이 바뀌지 않았다는 뜻입니다.
모델도 여섯 줄 모두 같아 입력 파일 하나에 모델 하나라는 조건을 지켰습니다.
다음 셀은 이름 목록에서 두 번 이상 나온 이름을 찾는 함수입니다.

### [44] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.263537Z', 'iopub.status.busy': '2026-09-21T18:36:13.263479Z', 'iopub.status.idle': '2026-09-21T18:36:13.265574Z', 'shell.execute_reply': '2026-09-21T18:36:13.265161Z'}}

```python
# 이름 목록을 앞에서부터 보며 두 번 이상 나온 이름을 한 번씩만 모읍니다
def duplicate_ids(id_list):
    seen = []
    duplicates = []
    for custom_id in id_list:
        if custom_id in seen and custom_id not in duplicates:
            duplicates.append(custom_id)
        seen.append(custom_id)
    return duplicates
```

출력:
```

```

### [45] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `duplicate_ids`는 이름을 앞에서부터 보며 이미 본 이름을 목록 `seen`에 모읍니다.
이미 본 이름이 다시 나오면 겹친 이름 목록에 넣습니다.
같은 이름이 세 번 나와도 겹친 이름 목록에는 한 번만 들어갑니다.

다음 셀은 다시 읽은 줄에서 요청 식별자만 모아 겹친 것이 있는지 봅니다.

### [46] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.266431Z', 'iopub.status.busy': '2026-09-21T18:36:13.266369Z', 'iopub.status.idle': '2026-09-21T18:36:13.268407Z', 'shell.execute_reply': '2026-09-21T18:36:13.268074Z'}}

```python
# 다시 읽은 줄에서 요청 식별자만 모아 겹친 것이 있는지 봅니다(정한 값에서 나온 결과라 assert로 확인합니다)
request_ids = []
for line in loaded_lines:
    request_ids.append(line["custom_id"])
print("요청 식별자 목록:", request_ids)
print("겹친 요청 식별자:", duplicate_ids(request_ids))
assert duplicate_ids(request_ids) == []
```

출력:
```
요청 식별자 목록: ['old-Q002', 'old-Q006', 'old-Q090', 'new-Q002', 'new-Q006', 'new-Q090']
겹친 요청 식별자: []

```

### [47] markdown {}

**결과 읽기** — 출력 줄 `요청 식별자 목록:` 뒤가 파일 차례대로 모은 요청 식별자 여섯 개입니다.
출력 줄 `겹친 요청 식별자: []`로 겹친 요청 식별자가 없습니다.
정한 값에서 나온 결과라 `assert`로도 확인했습니다.

이 검사를 통과했다고 제출이 성공한다는 뜻은 아닙니다.
판정 결과나 비용도 이 검사로는 알 수 없습니다.
이 절은 입력 파일까지 만들고 제출은 하지 않았습니다.

## 7. 결과를 요청 식별자로 잇기

OpenAI 안내에 따르면 일괄 작업이 끝나면 결과 파일을 따로 받습니다.
결과 파일도 JSONL이고, 성공한 요청 하나가 한 줄입니다.
결과 줄마다 요청 식별자가 들어 있고, 실패한 요청은 오류 파일에 따로 적힙니다.
결과 줄 차례는 입력 차례와 다를 수 있어 요청 식별자로 짝을 찾습니다.

### [48] markdown {}

이 절은 제출하지 않아 받은 결과가 없습니다.
그래서 결과 줄 다섯 개의 요청 식별자를 손으로 적어 짝 찾기만 연습합니다.
다음 셀은 첫째 목록에만 있는 이름을 찾는 함수입니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.269156Z', 'iopub.status.busy': '2026-09-21T18:36:13.269088Z', 'iopub.status.idle': '2026-09-21T18:36:13.271002Z', 'shell.execute_reply': '2026-09-21T18:36:13.270593Z'}}

```python
# 첫째 목록에는 있고 둘째 목록에는 없는 이름을 첫째 목록 차례대로 모읍니다
def ids_not_in(first_ids, second_ids):
    missing = []
    for custom_id in first_ids:
        if custom_id not in second_ids:
            missing.append(custom_id)
    return missing
```

출력:
```

```

### [50] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `ids_not_in`은 첫째 목록의 이름 가운데 둘째 목록에 없는 이름을 차례대로 모읍니다.
요청 목록을 첫째로 넣으면 결과가 오지 않은 요청을 찾습니다.
인자 차례를 바꾸면 요청에 없는 결과를 찾습니다. 07절 `broken_cases()`에서 쓴 방법입니다.

다음 셀은 손으로 적은 결과 줄 다섯 개의 요청 식별자로 짝을 찾습니다.
실제로 받은 결과가 아니라 흐름을 보여 주려고 정한 값입니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.271762Z', 'iopub.status.busy': '2026-09-21T18:36:13.271696Z', 'iopub.status.idle': '2026-09-21T18:36:13.273717Z', 'shell.execute_reply': '2026-09-21T18:36:13.273427Z'}}

```python
# 손으로 적은 결과 줄 다섯 개의 요청 식별자입니다(실제로 받은 결과가 아니라 흐름을 보여 주려고 정한 값입니다)
result_ids = ["new-Q090", "old-Q002", "new-Q006", "old-Q090", "new-Q002"]
print("결과 줄 수:", len(result_ids))
print("결과 줄 차례:", result_ids)
print("결과가 없는 요청:", ids_not_in(request_ids, result_ids))
print("요청에 없는 결과:", ids_not_in(result_ids, request_ids))
assert ids_not_in(request_ids, result_ids) == ["old-Q006"]
assert ids_not_in(result_ids, request_ids) == []
```

출력:
```
결과 줄 수: 5
결과 줄 차례: ['new-Q090', 'old-Q002', 'new-Q006', 'old-Q090', 'new-Q002']
결과가 없는 요청: ['old-Q006']
요청에 없는 결과: []

```

### [52] markdown {}

**결과 읽기** — 출력 줄 `결과 줄 수: 5`와 라벨 `결과 줄 차례:` 뒤 목록이 손으로 적은 결과입니다.
출력 줄 `결과가 없는 요청: ['old-Q006']`이 결과 줄이 오지 않은 요청입니다.
출력 줄 `요청에 없는 결과: []`로 모르는 요청 식별자는 없습니다.
손으로 정한 값이라 두 결과를 `assert`로 확인했습니다.

결과 줄은 `new-Q090`부터 적어 입력 차례와 다르게 두었습니다.
차례가 달라도 요청 식별자로 찾으면 빠진 요청을 알 수 있습니다.
실제 결과라면 빠진 요청은 오류 파일에서 찾아봅니다.

다음 셀은 요청 식별자를 판 표시와 질문 번호로 나눠 읽습니다.
글의 `split("-")`는 줄표 자리에서 글을 나눠 목록으로 만듭니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.274539Z', 'iopub.status.busy': '2026-09-21T18:36:13.274479Z', 'iopub.status.idle': '2026-09-21T18:36:13.276572Z', 'shell.execute_reply': '2026-09-21T18:36:13.276281Z'}}

```python
# 요청 식별자를 줄표로 나눠 판 표시와 질문 번호를 읽고, 결과 줄이 있는지 입력 차례대로 봅니다
print("판 표시 | 질문 번호 | 결과 줄이 있는가")
for custom_id in request_ids:
    parts = custom_id.split("-")
    print(parts[0], "|", parts[1], "|", custom_id in result_ids)
```

출력:
```
판 표시 | 질문 번호 | 결과 줄이 있는가
old | Q002 | True
old | Q006 | False
old | Q090 | True
new | Q002 | True
new | Q006 | True
new | Q090 | True

```

### [54] markdown {}

**결과 읽기** — 라벨 줄 `판 표시 | 질문 번호 | 결과 줄이 있는가` 아래 여섯 줄이 입력 차례입니다.
줄 `old | Q006 | False`만 결과 줄이 없고, 나머지 다섯 줄은 `True`입니다.

요청 식별자만 보고도 어느 판의 어느 사례인지 알 수 있습니다.
결과를 사례에 다시 이을 때도 이 두 값으로 짝을 찾습니다.

## 8. 값 바꿔 보기 · 판 표시를 뺀 요청 식별자

바꿀 값은 판 표시 두 개입니다. 이전 판과 이후 판 모두 `judge`를 붙입니다.
두 판의 요청 식별자는 질문 번호로만 갈리게 됩니다.

실행 전에 예상해 봅니다.
두 판의 같은 사례가 같은 요청 식별자를 받아 세 개가 겹칠 것입니다.
이 셀은 요청 목록만 만들고 파일에는 쓰지 않습니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-21T18:36:13.277305Z', 'iopub.status.busy': '2026-09-21T18:36:13.277246Z', 'iopub.status.idle': '2026-09-21T18:36:13.279486Z', 'shell.execute_reply': '2026-09-21T18:36:13.279084Z'}}

```python
# 바꿀 값은 판 표시 두 개입니다: 두 판 모두 judge를 붙여 요청 여섯 줄을 다시 만듭니다(파일에는 쓰지 않습니다)
same_old = make_batch_lines("judge", old_prompts, request_url, model_settings)
same_new = make_batch_lines("judge", new_prompts, request_url, model_settings)
same_ids = []
for line in same_old + same_new:
    same_ids.append(line["custom_id"])
print("요청 식별자 목록:", same_ids)
print("겹친 요청 식별자:", duplicate_ids(same_ids))
assert duplicate_ids(same_ids) == ["judge-Q002", "judge-Q006", "judge-Q090"]
```

출력:
```
요청 식별자 목록: ['judge-Q002', 'judge-Q006', 'judge-Q090', 'judge-Q002', 'judge-Q006', 'judge-Q090']
겹친 요청 식별자: ['judge-Q002', 'judge-Q006', 'judge-Q090']

```

### [56] markdown {}

**결과 읽기** — 라벨 `요청 식별자 목록:` 뒤 여섯 개에서 `judge-Q002`처럼 같은 이름이 두 번씩 나옵니다.
출력 줄 `겹친 요청 식별자: ['judge-Q002', 'judge-Q006', 'judge-Q090']`이 겹친 세 이름입니다.
마지막 줄의 `assert`도 통과했습니다.

예상대로 세 사례 모두 두 판의 요청 식별자가 겹쳤습니다.
이런 파일은 결과 줄이 와도 어느 판의 판정인지 가를 수 없습니다.
그래서 요청 식별자에는 요청 하나를 가르는 값인 판 표시와 질문 번호를 모두 넣습니다.
겹친 파일을 실제로 올렸을 때 서비스가 어떻게 하는지는 이번에 실행하지 않았습니다.

## 정리

1. 07절 판정 요청 여섯 개를 같은 글로 만들어 입력 파일에 한 줄씩 적었습니다.
2. 네 칸·방식·주소·모델과 겹친 요청 식별자를 제출 전에 검사했습니다.
3. 판 표시를 빼면 요청 식별자 세 개가 겹쳐 결과를 판별로 가를 수 없었습니다.

09절은 이 챕터를 마무리하는 실습 절입니다. 이 입력 파일에서 두 줄씩 골라 평가 모델에 보내고 판정과 예상 비용을 봅니다.

## 그림

### 08-1-판정-요청-여섯-개를-입력-파일로.mmd

```mermaid
flowchart TB
  %% classes
  cases["평가 사례 세 건<br>이전 판 답<br>자료 파일"]:::tool
  answers["이후 판 답 둘<br>Q002 · Q090<br>07절에서 만든 답"]:::tool
  prompts["make_prompts<br>판정 요청 글 여섯 개<br>07절과 같은 글"]:::flow
  lines["make_batch_lines<br>판 표시 old · new와<br>질문 번호로 요청 식별자"]:::flow
  file["runs/<br>batch-eval-input.jsonl<br>요청 여섯 줄"]:::tool
  check["제출 전 검사<br>네 칸 · POST · 주소 · 모델<br>어긋난 것 없음<br>겹친 요청 식별자 없음"]:::measure
  later["올리기 · 일괄 작업 만들기<br>결과 파일 받기<br>이번에 하지 않음"]
  cases --> prompts
  answers --> prompts
  prompts --> lines
  lines --> file
  file --> check
  check -.-> later
```

07절 판정 요청 여섯 개에 요청 식별자를 붙여 입력 파일에 쓰고 제출 전에 검사합니다. 올리기와 결과 받기는 하지 않았습니다.

### 08-2-입력-파일-한-줄의-네-칸.mmd

```mermaid
flowchart LR
  %% classes
  subgraph row["입력 파일 첫 줄 · 네 칸"]
    direction TB
    k1["custom_id<br>old-Q002"]:::tool
    k2["method<br>POST"]:::tool
    k3["url<br>/v1/chat/completions"]:::tool
    k4["body<br>요청 본문"]:::tool
    k1 ~~~ k2
    k2 ~~~ k3
    k3 ~~~ k4
  end
  subgraph inside["body 칸 안"]
    direction TB
    b1["model gpt-5.4-mini<br>temperature 0<br>reasoning_effort none<br>02~07절 모델 설정과<br>같은 값"]:::tool
    b2["messages<br>사용자 메시지 하나<br>판정 요청 글 3161자"]:::tool
    b1 ~~~ b2
  end
  row --> inside
```

입력 파일 한 줄은 네 칸이고, 본문 칸에는 02~07절과 같은 설정 세 칸과 판정 요청 글 3161자가 들어 있습니다.

### 08-3-판-표시를-뺀-요청-식별자.mmd

```mermaid
flowchart TB
  %% classes
  subgraph tagged["판 표시 old · new"]
    direction TB
    t1["make_batch_lines<br>old-Q002부터<br>new-Q090까지"]:::flow
    t2["요청 식별자 여섯 개<br>겹친 요청 식별자 없음<br>네 칸 · POST · 주소 · 모델<br>어긋난 것 없음 · 파일에 씀"]:::measure
    t1 --> t2
  end
  subgraph plain["값 바꿔 보기 · 두 판 모두 judge"]
    direction TB
    p1["make_batch_lines<br>judge-Q002부터<br>judge-Q090까지"]:::flow
    p2["겹친 요청 식별자 세 개<br>judge-Q002 · judge-Q006<br>judge-Q090<br>파일에 쓰지 않음"]:::measure
    p1 --> p2
  end
  same["두 칸에서 같음<br>판정 요청 글 여섯 개<br>본문 설정 세 칸"]
  tagged ~~~ same
  plain ~~~ same
```

요청 글과 본문은 그대로 두고 판 표시만 judge로 같게 바꾸자 요청 식별자 세 개가 겹쳤습니다.

### 08-4-결과-줄을-요청-식별자로-잇기.mmd

```mermaid
flowchart TB
  %% classes
  req["입력 파일의<br>요청 식별자 여섯 개<br>old-Q002 · old-Q006<br>old-Q090 · new-Q002<br>new-Q006 · new-Q090"]:::tool
  res["손으로 적은 결과 줄 다섯 개<br>new-Q090부터<br>입력과 차례가 다름"]:::tool
  fn["ids_not_in<br>인자 차례를 바꿔 두 번"]:::flow
  miss["결과가 없는 요청<br>old-Q006"]:::measure
  unk["요청에 없는 결과<br>없음"]:::measure
  note["OpenAI 안내<br>결과 줄 차례는<br>입력과 다를 수 있음<br>실패한 요청은<br>오류 파일에 적힘<br>이번에 받은 결과 아님"]
  req --> fn
  res --> fn
  fn --> miss
  fn --> unk
  miss ~~~ note
  unk ~~~ note
```

손으로 적은 결과 줄 다섯 개는 차례가 달랐지만, 요청 식별자로 짝을 찾아 결과가 없는 old-Q006을 찾았습니다.

### 08-5-궤짝에-담은-이름표-바구니.prompt.md

# 08-5-궤짝에-담은-이름표-바구니 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 07절까지는 바구니를 하나씩 저울에 올려 바로 눈금을 읽었습니다. 이번에는 바구니 여섯 개를 나무 궤짝 하나에 담아 한꺼번에 맡깁니다. 바구니마다 색이 다른 이름표를 달아 둡니다. 결과가 나중에 오면 이름표를 보고 어느 바구니의 결과인지 찾습니다. 이 절은 궤짝에 바구니를 담고 이름표를 확인하는 데까지 합니다. 저울에는 아직 아무것도 올리지 않았습니다.

구성 요소와 배치: 흰 바탕의 탁자 위에 뚜껑이 열린 **나무 궤짝 하나**(= 입력 파일 하나). 궤짝 안에 **짚 바구니 여섯 개**가 두 줄로 세 개씩(= 판정 요청 여섯 개, 뒷줄 = 이전 판·앞줄 = 이후 판으로 읽어도 되지만 본문은 줄의 뜻을 정하지 않음). 바구니마다 **빨간 사과 한 알**(= 판정받을 답, 아직 재지 않아 모두 같은 빨간 사과). 바구니 손잡이마다 **글자 없는 빈 이름표 하나**, 여섯 이름표 색이 모두 다름(= 겹치지 않는 요청 식별자). 궤짝 오른쪽에 **접시가 빈 부엌 저울 하나**(= 평가 모델, 이번 절에서는 요청을 보내지 않음). 숫자·글자 없이 개수·색·빈 접시로만 읽히게 했습니다.

시선 순서: 궤짝 하나 → 안의 바구니 여섯 → 손잡이마다 색이 다른 이름표 → 오른쪽의 빈 저울 접시.

검수 기준: 그림만 보고 「궤짝 하나에 바구니 여럿」, 「바구니마다 이름표, 이름표 색이 모두 다름」, 「저울 접시가 비어 있음」이 읽히는가. 글자·숫자가 없는가.

비유 계열: 01절이 정한 **바구니·사과·저울**. handoff 공통 제안 「08 묶음 제출 → 이름표 달린 바구니들」과 §07→§08 9번 제안(한 궤짝에 담아 한꺼번에 보내기, 이름표 = 요청 식별자)을 그렸습니다. 개선 전 08의 「택배 운송장」 비유는 쓰지 않았습니다.

## 프롬프트 (1차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos.

One large open wooden crate stands on a plain table, seen from the front and slightly above so the inside is visible. Inside the crate, six small woven baskets sit in two rows of three: a back row and a front row. Each basket holds exactly one red apple. Each basket has one small blank paper tag tied to its handle with string; the six tags are six different plain colors (blue, green, yellow, pink, orange, purple) and have no marks on them. To the right of the crate on the same table stands one plain kitchen scale with a round dial and an empty pan with nothing on it.

No hands, no people, no screens, no arrows, no charts.
```

## 상태

- 2026-09-21 · `nano_banana_pro`(응답 모델 이름 `nano_banana_2`) · 16:9 · 2k · `use_unlim: false` · 장당 2크레딧. 생성 전 잔액 2649 → 생성 뒤 **2647**.
- **1차 job `e3767412-fff9-42d8-b035-c4d81cffb88c` 채택**(재생성 없음). 원본 `03d373fc038ac8d509bced62911ce1e970899b788fbe6d0c51782091d74cde4a`(2752 × 1536, RGB). 생성에서 결과까지 약 45초.
- **그림에서 확인한 것(그림 읽기·alt·캡션에 반영)**: 탁자 위 왼쪽에 뚜껑이 뒤로 열린 나무 궤짝 하나, 안에 짚 바구니 여섯 개가 뒷줄 셋·앞줄 셋으로 놓임, 바구니마다 빨간 사과 한 알. 손잡이마다 끈으로 묶은 빈 이름표 하나 — 뒷줄 하늘색·초록·노랑, 앞줄 분홍·주황·보라로 여섯 색이 모두 다름. 탁자 오른쪽에 접시가 빈 부엌 저울 하나(둥근 눈금판은 숫자 없는 짧은 선, 바늘은 맨 위). 글자·숫자·사람 손은 없습니다. 프롬프트의 개수와 배치가 그대로 그려졌습니다.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아 `uv run --no-project --with pillow`로 RGB로 바꾸고 폭 1100px로 줄여 `figures/08-5-궤짝에-담은-이름표-바구니.png`(1100 × 614, `4eb498ffa9f5f77503ac7f7ed976ad5e8d7082803b5197f84135212c210fbf53`)로 저장. 원본 2752px는 저장하지 않았습니다. 결과 URL을 다시 받아(같은 해시 `03d373fc…`) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조해 차이가 없음을 확인했습니다(`ImageChops.difference` bbox `None`, 세 칸 extrema 모두 `(0, 0)`, 규격 §5-4). 저장 PNG와 같은 파일(`.cache/ch15-08/illu-job1.png`)을 직접 열어 그림 읽기를 썼습니다.

