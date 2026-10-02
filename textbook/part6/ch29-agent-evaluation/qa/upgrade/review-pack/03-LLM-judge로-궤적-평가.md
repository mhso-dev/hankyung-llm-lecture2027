# 03-LLM-judge로-궤적-평가

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 0.75h | 실습 1.25h | 코드 notebooks/03-LLM-judge로-궤적-평가.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>궤적 맞춰 보기의 모드와 평가 모델(judge)이 궤적에서 보는 것을 출력으로 견줘 말할 수 있습니다.</li>
<li>평가받는 에이전트를 실제로 실행해 만든 궤적을, 모드와 평가 모델로 함께 판정할 수 있습니다.</li>
<li>답 글 하나만 바꾼 궤적에서 두 판정이 어떻게 갈리는지 설명하고, 모델 요청 수를 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href="01-에이전트-평가-세-전략.html">01절</a>과 <a href="02-궤적-매칭-네-모드.html">02절</a>의 궤적 맞춰 보기는 도구 요청의 이름과 인자를 코드 규칙으로 짝지었습니다. 그래서 도구를 기준대로 부르고 답만 틀린 궤적도 참이었습니다. 답이 맞는지, 단계가 뜻이 통하는지는 궤적을 글로 읽어야 판정할 수 있습니다. Ch 15에서 배운 평가 모델이 그 일을 맡습니다.</p><p>이 절은 먼저 모델을 부르지 않고, 평가 모델이 궤적을 어떤 글로 받는지 봅니다. 이어서 이 챕터에서 처음으로 에이전트를 실제 모델로 실행해 궤적을 만듭니다. 그 궤적을 02절의 모드와 평가 모델로 함께 판정하고, 답 글 하나만 바꿔 두 판정을 견줍니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="01-에이전트-평가-세-전략.html">01절</a>에서는 최종 답 평가·한 단계 평가·궤적 평가를 견줬습니다. 도구 요청이 기준과 같고 답 글만 틀린 궤적은 모드 <code>strict</code>에서 참이었습니다. 01절은 뜻을 보는 판정을 이 절의 평가 모델 몫으로 남겼습니다. <a href="02-궤적-매칭-네-모드.html">02절</a>에서는 네 모드와 짝짓기, 인자 비교 방식과 도구별 덮어쓰기를 봤습니다. 이 절은 두 절에서 처음 적은 함수를 도구 파일에서 가져옵니다.</p><p><a href="../../part4/ch15-evaluation-advanced/01-실패-로그와-평가-대상.html">Ch 15 01절</a>에서는 다른 모델이 쓴 답을 읽고 판정하는 모델을 평가 모델이라고 불렀습니다. <a href="../../part4/ch15-evaluation-advanced/02-4대-RAG-평가자.html">02절</a>은 판정 기준을 적은 글을 판정 머리글, 판정할 내용을 끼운 글을 판정 요청 글이라고 불렀습니다. <a href="../../part4/ch15-evaluation-advanced/03-judge-프롬프트와-편향.html">03절</a>은 평가 모델의 판정이 치우칠 수 있다는 것을 봤습니다. Ch 15는 판정 머리글을 손으로 적었고, 이 절은 라이브러리가 적어 둔 머리글을 씁니다.</p><p><a href="../../part5/ch19-model-tools/01-tool과-Ch4-함수-재사용.html">Ch 19 01절</a>에서는 <code>@tool</code> 줄로 도구를 만들고 메서드 <code>invoke</code>로 불렀습니다. <a href="../ch21-create-agent/01-create-agent와-ReAct-루프.html">Ch 21 01절</a>에서는 함수 <code>create_agent</code>에 모델 객체와 도구 목록을 넘겨 에이전트를 만들었습니다. <a href="../ch22-middleware/04-호출-한도와-재시도-폴백.html">Ch 22 04절</a>의 호출 한도는 Ch 26~28에서 모델을 부르는 에이전트마다 붙였습니다. <a href="../ch27-deepagents/02-create-deep-agent와-도구.html">Ch 27 02절</a>처럼 요청 수는 「도구를 요청한 응답 수 + 1」로 셉니다. 실행 한도를 주는 설정 딕셔너리는 <a href="../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html">Ch 20 03절</a>에서 봤습니다.</p><p><a href="../ch21-create-agent/06-같은-평가셋으로-RAG-비교.html">Ch 21 06절</a>에서는 두 흐름의 답을 평가 모델로 판정했고, 판정 여섯이 모두 1이었습니다. 그 절은 답을 판정했고, 이 절은 도구를 부른 차례까지 담은 궤적을 판정합니다. 요청 수는 <a href="../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html">Ch 19 05절</a>의 <code>sum_usage</code>로, 예상 비용은 <a href="../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html">Ch 6 06절</a>의 <code>estimate_cost</code>로 셉니다. 목록을 복사하는 <code>copy()</code>는 <a href="../../part1/ch02-python/03-자료구조.html">Ch 2 03절</a>에서 배웠습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01·02절에서는 오르골 종이띠의 구멍을 기준 띠에 대 봤습니다. 두 띠를 겹쳐 보면, 구멍이 같은 자리에 같은 수만큼 있는지는 바로 보입니다. 그러나 겹쳐 보는 것만으로는 곡이 어떻게 들리는지 모릅니다. 기준 곡과 같은 노래인지 보려면, 띠를 오르골 기계에 넣어 울려 봐야 합니다.</p><p>겹쳐 보는 쪽이 궤적 맞춰 보기의 모드이고, 울려 보는 쪽이 궤적 글을 읽는 평가 모델입니다. 구멍 자리는 도구 요청이고, 울려 나는 곡은 답 글까지 담은 궤적의 뜻입니다. 비유와 다른 점도 있습니다. 오르골은 같은 띠를 넣으면 늘 같은 곡이 나지만, 평가 모델은 같은 궤적에도 판정이 달라질 수 있습니다. 그래서 이 절은 평가 모델의 점수를 노트북 밖에서 다섯 번 더 확인하고 씁니다.</p>
{{img:03-5-겹쳐-보기와-울려-보기|흰 바탕 왼쪽에 크림색 종이띠 둘이 조금 비켜 겹쳐 비스듬히 놓여 있고, 띠마다 둥근 구멍이 한 줄로 뚫려 있어 구멍 줄 둘이 나란히 보입니다. 오른쪽에는 상자 없이 드러난 오르골 기계 둘이 나란히 서 있습니다. 기계마다 금색 틀 안에 원통과 빗 모양 쇠붙이가 있고 옆에 작은 손잡이가 달렸으며, 구멍 뚫린 종이띠가 하나씩 위에서 아래로 기계를 지나갑니다. 사람·귀·손·글자·숫자·음표·화살표는 없는 그림|왼쪽에서는 종이띠 둘을 겹쳐 놓고, 오른쪽에서는 종이띠를 하나씩 오르골 기계에 넣어 울립니다.}}
<p class="look"><b>그림 읽기</b> — 왼쪽에 종이띠 둘이 조금 비켜 겹쳐 놓였고, 오른쪽에는 띠가 하나씩 지나가는 오르골 기계 둘이 있습니다. 겹쳐 놓은 두 띠는 구멍 자리를 대 보는 궤적 맞춰 보기의 모드이고, 두 기계는 두 궤적 글을 함께 읽는 평가 모델입니다. 오른쪽 두 띠가 실제 궤적과 기준 궤적이고, 기계가 띠를 울려 곡을 내듯 평가 모델은 답 글까지 담은 궤적의 뜻을 봅니다. 구멍의 수, 띠의 기울기와 길이, 짙게 칠한 구멍, 기계의 손잡이는 어떤 값과도 짝짓지 않습니다.</p>
<h3>평가 모델이 받는 글</h3><p>평가 모델에 궤적을 넘기면, 라이브러리가 메시지마다 역할 태그로 감싸 한 덩어리 글로 바꿉니다. 도구 요청은 이름과 인자를, 도구 메시지는 호출 ID와 결과 글을, 마지막 응답은 답 글을 그대로 담습니다. 이 글을 이 절에서는 궤적 글이라고 부릅니다. 실제 궤적 글과 기준 궤적 글은 판정 머리글의 두 자리에 끼워져, 요청 글 하나가 됩니다.</p><p>판정 머리글 <code>TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE</code>에는 판정 기준 네 줄이 있습니다. 단계 사이가 논리적으로 이어지는가, 한 단계씩 나아가는가를 봅니다. 완벽하지 않아도 되지만 필요 없는 단계가 적은가, 기준 궤적과 뜻이 같은가도 봅니다. 평가 모델은 이 네 기준으로 참·거짓 하나와 판정 까닭을 냅니다.</p><p>평가 함수를 만들 때 인자 <code>judge=</code>에 모델 객체를 넘겼습니다. 인자 <code>model=</code>에 모델 이름 글만 넘기면, 설치판은 온도·추론 설정 없이 모델을 만듭니다. 설치판 openevals 0.2.0 <code>llm.py</code> 251~254행이 그 줄입니다. 그래서 과정 표준 설정(<code>temperature=0</code>·<code>reasoning_effort="none"</code>)의 모델 객체를 만들어 넘겼습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>궤적 글</td><td>궤적의 메시지를 역할 태그로 감싸 한 덩어리로 이은 글입니다. 평가 모델은 궤적을 메시지 목록이 아니라 이 글로 받습니다. 연극 대본에 대사마다 말한 사람의 이름을 붙여 적은 것과 같습니다. 이 절에서는 설치판 함수 <code>_format_inputs</code>가 만든 글을 노트북 2절에서 출력했습니다.</td></tr><tr><td>판정 까닭</td><td>평가 모델이 점수와 함께 적어 내는, 그렇게 판정한 까닭 글입니다. 결과 딕셔너리의 칸 <code>comment</code>에 담깁니다. 시험 채점표에서 점수 옆에 적는 한 줄 평과 같습니다. 이 절의 판정 까닭은 영어로 왔고, 실행마다 글이 조금씩 달라져 결론에 쓰지 않았습니다.</td></tr><tr><td>평가받는 에이전트</td><td>평가할 궤적을 만드는 에이전트입니다. 평가 모델과는 따로 실행되고, 요청 수도 따로 셉니다. 요리 대회에서 요리를 만드는 참가자와 맛을 보는 심사위원을 나누는 것과 같습니다. 이 절에서는 도구 둘과 호출 한도 4를 붙인 <code>library_agent</code>입니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 궤적 글은 <code>_format_inputs(wrong_answer, reference)</code>가 내놓은 튜플의 <code>[0]</code>입니다. 판정 까닭은 평가 함수 결과의 칸 <code>comment</code>이고, 평가받는 에이전트는 <code>library_agent</code>입니다. 평가받는 에이전트의 요청은 <code>sum_usage</code>로 세고, 평가 모델의 요청은 판정을 부른 횟수로 따로 셉니다.</p>
{{mermaid:03-1-모드와-평가-모델이-보는-것|위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 둘은 답만 틀린 궤적과 기준 궤적입니다. 답만 틀린 궤적은 도구 요청 둘이 기준과 같고 답 글이 7일, 기준 궤적은 답 글이 14일입니다. 두 상자에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 평가 모델에는 회색 상자 _format_inputs, 메시지마다 태그로 감싼 궤적 글에서 노란 상자 답 글·검색 결과 글·호출 ID 모두 들어 있음 True로 화살표가 갑니다. 그 아래 점선 테두리의 회색 상자 평가 모델, 3절에서 만들기만 함으로 점선 화살표가 이어집니다. 오른쪽 칸 궤적 맞춰 보기에는 파란 상자 모드 넷, 도구 요청의 이름과 인자만 짝지음에서 노란 상자 네 모드 모두 True로 화살표가 가는 그림|네 모드는 답만 틀린 궤적을 모두 참으로 봤고, 평가 모델이 받는 궤적 글에는 답 글과 도구 결과 글이 들어 있었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자 둘은 노트북 2절에서 코드로 적은 두 궤적입니다. 오른쪽 칸은 2절에서 네 모드로 견준 결과이고, 왼쪽 칸은 같은 궤적을 평가 모델이 받는 글로 바꾼 결과입니다. 노란 상자 둘은 2절 셀 출력입니다. 앞 절반에서는 평가 모델을 부르지 않아, 점선 테두리의 회색 상자로 두었습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 01절의 답만 틀린 궤적을 네 모드로 견주고, 같은 궤적의 궤적 글을 출력합니다. 3절은 판정 기준 줄과 요청 글의 글자 수를 보고, 평가 함수를 만들기만 합니다. 4절은 도구 둘을 붙인 에이전트를 실제 모델로 한 번 실행하고, 요청 수를 셉니다. 5절은 그 궤적을 모드와 평가 모델로 판정하고, 6절은 답 글 하나만 바꿔 다시 판정합니다. 7절은 평가 모델 요청까지 더한 요청 수와 예상 비용을 봅니다.</p><p>모델 요청은 4~6절에서만 나갑니다. 교재 출력에서는 에이전트 요청 3번과 평가 모델 요청 2번, 모두 5번이었습니다. 예상 비용은 요금표로 어림해 약 0.003달러이고, 청구 금액과는 다를 수 있습니다. 읽는 파일은 <code>.env</code>와 도구 파일 <code>eval_tools.py</code>이고, 쓰는 파일은 없습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:03-LLM-judge로-궤적-평가}}
<p class="look"><b>확인할 점</b> — 노트북 2절에서 <code>답만 틀림: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}</code>와 궤적 글의 태그를 봅니다. 3절에서 <code>요청 글의 글자 수: 1694</code>와 <code>평가 함수의 종류: function</code>을 찾습니다. 4절에서는 <code>시스템 메시지가 들어 있는가: False</code>와 <code>모델 요청 수 = 도구를 요청한 응답 수 + 1: True</code>를 확인합니다.</p>
{{mermaid:03-2-평가-모델이-받는-요청-글|위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 답만 틀린 궤적과 기준 궤적, 메시지 여섯씩에서 회색 상자 _format_inputs 설치판 함수로 화살표가 갑니다. 이어서 노란 상자 궤적 글 둘, user·assistant·tool 태그로 화살표가 가고, 다시 노란 상자 요청 글 하나, 글자 수 1694로 화살표가 갑니다. 회색 상자 판정 머리글, 판정 기준 네 줄과 궤적 글 자리 둘에서도 요청 글 상자로 화살표가 들어옵니다. 요청 글 상자에서 점선 테두리의 회색 상자 평가 모델, 이 칸에서는 부르지 않음으로 점선 화살표가 가고, 다시 회색 상자 결과 딕셔너리, key·score·comment·metadata, 설치판 소스로 본 모양으로 점선 화살표가 가는 그림|두 궤적 글을 판정 머리글에 끼우자 글자 수 1694의 요청 글이 되었고, 평가 모델은 이 글과 답할 모양을 함께 받습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자는 노트북 2절에서 코드로 적은 궤적이고, 회색 상자 셋은 라이브러리가 정한 것입니다. 노란 상자 둘은 2절과 3절 셀 출력이고, 점선 두 개와 점선 테두리 상자는 앞 절반에서 실행하지 않은 차례입니다. 결과 딕셔너리의 칸 이름은 설치판 소스로 본 것이고, 노트북은 5절에서 처음 받습니다. 요청 글과 함께 가는 답할 모양은 따로 그리지 않았고, 그 칸 reasoning이 결과의 칸 comment가 됩니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>답만 틀린 궤적은 네 모드 모두 참이었습니다. 네 모드는 도구 요청의 이름과 인자를 짝지을 뿐, 답 글을 견주지 않기 때문입니다. 같은 궤적의 궤적 글에는 답 글과 도구 결과 글이 모두 들어 있었습니다. 평가 모델은 모드가 보지 않는 글까지 받습니다.</p><p>평가받는 에이전트는 검색 → 출처 확인 → 답의 차례로 움직였고, 모델 요청은 3번이었습니다. 요청 수는 도구를 요청한 응답 수 2에 1을 더한 값과 같았습니다. 검색 도구의 인자만 빼고 보자, 네 모드 모두 이 궤적을 참으로 봤습니다. 평가 모델도 이 궤적을 참으로 판정했습니다. 이 값들은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.</p>
{{mermaid:03-3-에이전트-궤적과-두-판정|위에서 아래로 읽는 흐름도입니다. 맨 위 파란 상자 평가받는 에이전트, 도구 둘, 호출 한도 4, 실행 한도 20에서 보라 상자 gpt-5.4-mini 에이전트 요청 3번으로 화살표가 갑니다. 이어서 노란 상자 에이전트 궤적, search_documents, check_source, 답, 메시지 여섯으로 화살표가 갑니다. 궤적 상자에서 아래 두 갈래로 화살표가 나뉩니다. 왼쪽은 파란 상자 모드 넷, search_documents 인자만 ignore, 기준 궤적과 견줌에서 노란 상자 네 모드 모두 True로 갑니다. 오른쪽은 보라 상자 평가 모델 gpt-5.4-mini, 판정 머리글, 요청 1번에서 노란 상자 칸 score True로 가는 그림|노트북 밖 다섯 번과 두 커널에서 모두, 에이전트 궤적을 검색어를 뺀 네 모드와 평가 모델이 참으로 판정했습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 파란 상자는 노트북 4절에서 만든 에이전트이고, 보라 상자 둘은 이 노트북이 실제로 부른 모델입니다. 노란 상자는 4절과 5절 셀 출력입니다. 궤적 상자 아래 두 갈래는 같은 궤적을 서로 다른 방법으로 판정한 것이고, 서로의 차례가 아닙니다. 요청 수·도구 차례·두 판정은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.</p>
<p>에이전트 궤적의 답 글 하나만 01절의 틀린 답으로 바꾸자, 모드 <code>strict</code>는 참 그대로였고 평가 모델만 거짓을 냈습니다. 평가 모델의 이 거짓도 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다. 모드는 규칙을 코드로 적어 같은 궤적에 늘 같은 판정을 내지만, 답 글은 보지 않습니다. 평가 모델은 답 글까지 읽지만, 판정은 모델이 내는 값이라 실행마다 달라질 수 있습니다. 그래서 차례·도구·인자처럼 코드로 적을 수 있는 것은 모드로, 뜻은 평가 모델로 봅니다.</p>
<p>아래 표는 노트북 2·5·6절의 판정을 모은 것입니다.</p>
<table><thead><tr><th>궤적</th><th>궤적 맞춰 보기</th><th>평가 모델</th><th>노트북</th></tr></thead><tbody><tr><td>답만 틀린 궤적(코드로 적음)</td><td>네 모드 모두 <code>True</code></td><td>부르지 않음</td><td>노트북 2절</td></tr><tr><td>에이전트 궤적</td><td>네 모드 모두 <code>True</code>(검색어 뺌)</td><td><code>True</code></td><td>노트북 5절</td></tr><tr><td>에이전트 궤적에서 답 글만 틀리게 바꿈</td><td>모드 <code>strict</code> <code>True</code>(검색어 뺌)</td><td><code>False</code></td><td>노트북 6절</td></tr></tbody></table>
{{mermaid:03-4-답-글-하나만-바꾸기|위에서 아래로 읽는 그림입니다. 맨 위 회색 상자 도구 요청과 도구 결과 글은 에이전트 궤적 그대로에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 에이전트 궤적 그대로에는 노란 상자 답 글, 에이전트가 쓴 답에서 노란 상자 모드 strict True, 평가 모델 True로 화살표가 갑니다. 오른쪽 칸 마지막 답 글만 바꿈에는 파란 상자 답 글, 일반 도서는 7일 동안 빌릴 수 있습니다에서 노란 상자 모드 strict True, 평가 모델 False로 화살표가 가는 그림|노트북 밖 다섯 번과 두 커널에서 모두, 마지막 답 글 하나만 바꾸자 모드 strict는 참 그대로였고 평가 모델만 거짓을 냈습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 회색 상자는 두 칸에 같이 쓴 도구 요청과 도구 결과 글입니다. 오른쪽 칸의 파란 상자가 노트북 6절에서 바꾼 값 하나이고, 노란 상자는 5절과 6절 셀 출력입니다. 모드 strict는 도구 요청 가운데 검색 도구의 인자만 보지 않는 평가 함수입니다. 두 칸은 서로 다른 궤적이라 화살표 없이 나란히 두었고, 두 판정은 노트북 밖 다섯 번과 새 커널 두 번에서 같았습니다.</p>
<p>아래 표는 에이전트 실행에서 나온 값과, 그 값을 어디까지 믿을 수 있는지입니다. 모델이 쓴 값과 토큰은 결론에 쓰지 않았습니다.</p>
<table><thead><tr><th>값</th><th>교재 출력</th><th>성격</th></tr></thead><tbody><tr><td>도구 차례</td><td><code>search_documents</code> → <code>check_source</code></td><td>다섯 번·두 커널 같음</td></tr><tr><td>모델 요청 수</td><td><code>3</code> = 도구를 요청한 응답 수 <code>2</code> + 1</td><td>다섯 번·두 커널 같음</td></tr><tr><td>검색어</td><td>「일반 도서 대출 기간 며칠」</td><td>교재 출력(모델이 쓴 값)</td></tr><tr><td>마지막 답 글</td><td>기준 답과 글자까지 같음</td><td>교재 출력(모델이 쓴 값)</td></tr><tr><td>에이전트 토큰·예상 비용</td><td>입력 933 · 출력 63 · 0.000983달러</td><td>교재 출력(요금표 어림)</td></tr><tr><td>평가 모델 토큰(판정 한 번)</td><td>입력 679~682 · 출력 87~104</td><td>노트북 밖 판정 10번</td></tr></tbody></table>
<p>새 커널로 두 번 실행해 견주자, 코드 셀 스물여덟 가운데 스물여섯의 출력이 같았습니다. 다른 두 셀은 평가 모델의 판정 까닭 글만 달랐고, 칸 <code>score</code>는 두 번 모두 같았습니다.</p>
<p class="look"><b>확인할 점</b> — 노트북 5절에서 <code>칸 score: True</code>를, 6절에서 <code>평가 모델 칸 score: False</code>와 두 줄 표를 확인합니다. 7절에서 <code>모두 합한 모델 요청 수: 5</code>를 봅니다. 판정 까닭 글과 토큰은 다시 실행하면 달라질 수 있습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>에이전트의 도구 차례와 평가 모델의 점수는 모델이 내는 값입니다. 노트북에 넣기 전에 같은 실행을 노트북 밖에서 다섯 번 해 보니, 도구 차례·요청 수·네 모드·두 점수가 모두 같았습니다. 그래도 같은 요청이 늘 같은 판정을 낸다고 할 수는 없습니다. 같은 요청도 실행한 때에 따라 판정이 달라질 수 있습니다.</li><li>판정 까닭은 영어로 왔고, 노트북 밖 다섯 번에서도 글이 조금씩 달랐습니다. 이 절은 판정 까닭의 줄거리만 결과 읽기 둘째 단락에 적었고, 결론에는 점수만 썼습니다.</li><li>평가받는 에이전트와 평가 모델은 같은 모델 객체 gpt-5.4-mini를 썼습니다. 제가 만든 궤적을 제가 판정하는 셈이라, Ch 15 03절에서 본 치우침이 끼어들 수 있습니다. 다른 모델로 판정하는 장면은 이 절에서 실행하지 않았습니다.</li><li>검색 도구는 어떤 검색어에도 같은 글을 내놓는 교재용 함수입니다. 시스템 메시지 글에는 검색 뒤 출처를 확인하는 차례를 적었고, 기준 궤적도 그 차례로 정했습니다. 흐름을 보여 주려고 실행 전에 정한 예이고, 결과를 보고 바꾸지 않았습니다.</li><li>호출 한도 4와 실행 한도 20은 요청 3번인 이 절의 실행에 드는 값보다 넉넉히 잡은 값입니다. 이 실행이 그래프 단계를 몇 번 거쳤는지는 이번에 세지 않았습니다. 이 노트북에서 두 한도에 닿은 실행은 없었습니다.</li><li>평가 모델 요청 수 2는 판정을 부른 횟수를 손으로 적은 값입니다. 판정 한 번에 요청 1번이라는 것은 설치판 openevals 0.2.0 <code>llm.py</code> 256~272행으로 봤습니다. 평가 모델 요청의 토큰은 노트북에서 세지 않았습니다. 노트북 밖 판정 10번에서 한 번은 입력 679~682, 출력 87~104토큰이었습니다.</li><li>교재 출력의 에이전트 예상 비용은 0.000983달러였습니다. 평가 모델 두 번을 노트북 밖 토큰으로 어림하면 약 0.0019달러라, 노트북 한 번에 약 0.003달러입니다. 요금표는 2026-09-17 mini 값이고, 청구 금액과는 다를 수 있습니다.</li><li>궤적 글에는 호출 ID가 들어갑니다. 에이전트의 호출 ID는 모델 서비스가 정한 값이라 실행마다 달라, 평가 모델이 받는 글도 조금씩 달라집니다. 노트북 밖에서는 평가 모델 입력 토큰도 679~682로 조금씩 달랐습니다.</li><li>함수 <code>_format_inputs</code>처럼 밑줄로 시작하는 이름은 라이브러리가 안에서 쓰는 함수입니다. 판이 바뀌면 이름이나 모양이 바뀔 수 있어, 평가 모델이 받는 글을 보는 데만 썼습니다.</li><li>인자 <code>continuous=True</code>를 주면 점수가 0~1 사이 소수가 되고, 인자 <code>choices</code>를 주면 정한 값 가운데 하나가 됩니다. 기준 궤적 없이 판정하는 머리글 <code>TRAJECTORY_ACCURACY_PROMPT</code>도 있습니다. 셋 모두 설치판 소스와 공식 설명으로 본 것이고, 이 노트북에서는 실행하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>네 모드는 답만 틀린 궤적을 모두 참으로 봤습니다. 평가 모델이 받는 궤적 글에는 답 글과 도구 결과 글이 들어 있었습니다.</li><li>평가받는 에이전트는 요청 3번으로 검색 → 출처 확인 → 답의 궤적을 만들었습니다. 검색어를 뺀 네 모드와 평가 모델이 모두 참으로 판정했습니다.</li><li>답 글 하나만 바꾸자, 모드 <code>strict</code>는 참 그대로였고 평가 모델만 거짓을 냈습니다. 둘째·셋째 줄의 값은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="04-운영-지표와-Ch18-궤적-비교.html">04절</a>에서는 모델을 부르지 않고, 앞 챕터가 저장한 실행 기록을 읽어 운영 지표를 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 답만 틀린 궤적을 네 모드로 견주면 어떻게 되고, 까닭은 무엇인가요?</p><p class="quiz-a">네 모드 모두 참입니다. 네 모드는 도구 요청의 이름과 인자를 짝지을 뿐, 답 글을 견주지 않습니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. 에이전트 궤적에서 답 글 하나만 틀린 글로 바꾸자, 모드 <code>strict</code>와 평가 모델의 판정은 어떻게 되었나요?</p><p class="quiz-a">모드 <code>strict</code>는 참 그대로였고, 평가 모델만 거짓을 냈습니다. 평가 모델은 답 글까지 담은 궤적 글을 읽기 때문입니다. 이 거짓은 노트북 밖 다섯 번과 새 커널 두 번에서 같았지만, 모델이 내는 값이라 늘 같다고 할 수는 없습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 평가 함수를 <code>model="openai:gpt-5.4-mini"</code>로 만들자고 합니다. 이 절과 무엇이 달라지나요?</p><p class="quiz-a">설치판은 이름 글만 받으면 온도·추론 설정 없이 모델을 만듭니다. 이 절은 <code>temperature=0</code>·<code>reasoning_effort="none"</code>을 준 모델 객체를 인자 <code>judge=</code>로 넘겼습니다. 틀렸다면 본문 「평가 모델이 받는 글」을 다시 읽습니다.</p><p class="quiz-q">4. 에이전트가 도구를 세 번 요청한 뒤 답하고, 그 궤적을 평가 모델로 두 번 판정했다면 모델 요청은 모두 몇 번일까요?</p><p class="quiz-a">6번입니다. 에이전트 요청은 도구를 요청한 응답 셋에 답을 쓴 응답 하나를 더한 4번이고, 평가 모델 요청은 판정 두 번에 2번입니다. 에이전트 요청 4번은 호출 한도 4 안입니다. 틀렸다면 노트북 4절과 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/test/evals">LangChain Agent evals</a></div>확인 2026-09-29 · 평가 모델로 궤적을 판정하는 함수 <code>create_trajectory_llm_as_judge</code>를 적습니다. 기준 궤적 없이도 판정할 수 있고, 기준 궤적이 있으면 <code>TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE</code>를 쓴다고 적습니다. 예시는 인자 <code>model=</code>에 모델 이름 글을 넘깁니다.</li><li><div><a href="https://github.com/langchain-ai/agentevals">agentevals (GitHub)</a></div>확인 2026-09-29 · 인자 <code>judge</code>에 LangChain 채팅 모델이나 OpenAI 클라이언트를 넘길 수 있다고 적습니다. 결과 예시의 칸은 <code>key</code>·<code>score</code>·<code>comment</code>입니다.</li><li><div><a href="https://github.com/langchain-ai/openevals">openevals (GitHub)</a></div>확인 2026-09-29 · LangChain 채팅 모델 객체를 <code>judge</code>로 바로 넘길 수 있다고 적습니다. 그 모델은 구조화 출력을 지원해야 합니다. 인자 <code>continuous</code>·<code>choices</code>·<code>use_reasoning</code>의 뜻도 적습니다.</li><li>설치판 agentevals 0.0.9 <code>trajectory/llm.py</code> 27~49행은 기준 궤적을 넣는 판정 머리글이고, 30~36행이 판정 기준입니다. 77~95행은 궤적 글을 만드는 함수, 98~173행은 평가 함수를 만드는 함수입니다.</li><li>설치판 openevals 0.2.0 <code>llm.py</code> 70~117행은 출력 형식(칸 <code>reasoning</code>·<code>score</code>)입니다. 251~254행은 모델 이름 글만 받았을 때 모델을 만드는 줄이고, 256~272행은 요청 한 번입니다. <code>utils.py</code> 427~454행은 메시지를 태그로 감싸는 줄입니다.</li><li>설치판 langchain 1.4.0 <code>agents/factory.py</code> 1451~1452행은 시스템 메시지 글을 요청 때만 앞에 붙이는 줄입니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# LLM judge로 궤적 평가

**이 노트북에서 할 일**

1. 01절의 답만 틀린 궤적으로, 모드와 평가 모델이 궤적에서 무엇을 보는지 견줍니다.
2. 도구 둘을 붙인 에이전트를 실제 모델로 한 번 실행해 궤적을 만듭니다.
3. 그 궤적을 02절의 모드와 평가 모델로 함께 판정하고, 답 글 하나만 바꿔 다시 판정합니다.

**준비물** — 프로젝트 폴더의 `.env`에 `OPENAI_API_KEY`가 있어야 합니다.
모델 요청은 4~6절에서만 나갑니다.
교재 출력에서는 에이전트 요청 3번과 평가 모델 요청 2번, 모두 5번이었습니다.
예상 비용은 요금표로 어림해 약 0.003달러이고, 청구 금액과는 다를 수 있습니다.
2~3절은 모델 요청 없이, 코드로 적은 궤적과 라이브러리 함수만 씁니다.

읽는 파일은 `.env`와 같은 폴더의 도구 파일 `eval_tools.py`이고, 쓰는 파일은 없습니다.
걸린 시간은 재지 않았습니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 agentevals 0.0.9와 langchain 1.4.0입니다.
모델을 부르는 langchain-openai는 1.6.0, 키를 읽는 python-dotenv는 1.2.3입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~5절을 읽습니다.
평가 모델이 받는 글을 보고, 실제 에이전트 궤적을 두 방법으로 판정하는 자리입니다.
6~7절은 답 글 하나만 바꿔 다시 판정하고 요청 수를 세는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch29-agent-evaluation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 둘은 답만 틀린 궤적과 기준 궤적입니다. 답만 틀린 궤적은 도구 요청 둘이 기준과 같고 답 글이 7일, 기준 궤적은 답 글이 14일입니다. 두 상자에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 평가 모델에는 회색 상자 _format_inputs, 메시지마다 태그로 감싼 궤적 글에서 노란 상자 답 글·검색 결과 글·호출 ID 모두 들어 있음 True로 화살표가 갑니다. 그 아래 점선 테두리의 회색 상자 평가 모델, 3절에서 만들기만 함으로 점선 화살표가 이어집니다. 오른쪽 칸 궤적 맞춰 보기에는 파란 상자 모드 넷, 도구 요청의 이름과 인자만 짝지음에서 노란 상자 네 모드 모두 True로 화살표가 가는 그림](attachment:03-1-모드와-평가-모델이-보는-것.png)

위에서 아래로 읽습니다.
맨 위 초록 상자 둘은 노트북 2절에서 코드로 적은 두 궤적입니다.
오른쪽 칸은 2절에서 네 모드로 견준 결과이고, 왼쪽 칸은 같은 궤적을 평가 모델이 받는 글로 바꾼 결과입니다.
노란 상자 둘은 2절 셀 출력입니다.
앞 절반에서는 평가 모델을 부르지 않아, 점선 테두리의 회색 상자로 두었습니다.

### [2] markdown {}

## 1. 준비

01·02절은 궤적을 코드 규칙으로 맞춰 봤습니다.
이 절은 모델이 궤적을 읽고 판정하는 평가 모델(judge)을 쓰고, 이 챕터에서 처음으로 에이전트를 실제로 실행합니다.
뜻과 구성은 본문 「핵심 개념」에서 풉니다.

첫 셀은 패키지 넷을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:21.401007Z', 'iopub.status.busy': '2026-09-29T02:26:21.400933Z', 'iopub.status.idle': '2026-09-29T02:26:22.311227Z', 'shell.execute_reply': '2026-09-29T02:26:22.310653Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "agentevals==0.0.9" "langchain==1.4.0" "langchain-openai==1.6.0" "python-dotenv==1.2.3"
from importlib.metadata import version

print("agentevals:", version("agentevals"))
print("langchain:", version("langchain"))
print("langchain-openai:", version("langchain-openai"))
print("python-dotenv:", version("python-dotenv"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
agentevals: 0.0.9
langchain: 1.4.0
langchain-openai: 1.6.0
python-dotenv: 1.2.3

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `agentevals: 0.0.9`, `langchain: 1.4.0`, `langchain-openai: 1.6.0`, `python-dotenv: 1.2.3`이 보입니다.
넷 모두 실습 폴더 잠금과 같은 판입니다.
패키지 langchain-openai는 모델을 부를 때, python-dotenv는 키를 읽을 때 씁니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
함수 `create_trajectory_llm_as_judge`는 평가 모델로 궤적을 판정하는 평가 함수를 만듭니다.
이름 `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE`는 라이브러리가 적어 둔 판정 머리글입니다.
함수 `_format_inputs`처럼 밑줄로 시작하는 이름은 라이브러리가 안에서 쓰는 함수입니다.
판이 바뀌면 달라질 수 있어, 이 절은 평가 모델이 받는 글을 볼 때만 씁니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:22.312426Z', 'iopub.status.busy': '2026-09-29T02:26:22.312297Z', 'iopub.status.idle': '2026-09-29T02:26:23.101708Z', 'shell.execute_reply': '2026-09-29T02:26:23.101298Z'}, 'lesson_role': 'setup'}

```python
# 궤적을 맞춰 보는 평가 함수·평가 모델로 판정하는 평가 함수를 만드는 함수와 판정 머리글을 가져옵니다
from agentevals.trajectory.llm import TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE, _format_inputs, create_trajectory_llm_as_judge
from agentevals.trajectory.match import create_trajectory_match_evaluator
# 에이전트·호출 한도·모델·메시지 클래스·도구를 등록하는 줄을 가져옵니다(Ch 6·13·19·21·22)
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool
# 앞에서 배운 함수는 도구 파일에서 가져옵니다
from eval_tools import called_tool_names, estimate_cost, four_modes, make_trajectory, show_messages, sum_usage, tool_call_names, trajectory_pass

print("도구 파일에서 가져온 함수:", "called_tool_names, estimate_cost, four_modes, make_trajectory, show_messages, sum_usage, tool_call_names, trajectory_pass")
```

출력:
```
도구 파일에서 가져온 함수: called_tool_names, estimate_cost, four_modes, make_trajectory, show_messages, sum_usage, tool_call_names, trajectory_pass

```

### [6] markdown {}

**결과 읽기** — 라벨 `도구 파일에서 가져온 함수:` 뒤에 `four_modes`·`sum_usage`·`estimate_cost` 등 함수 여덟의 이름이 보입니다.
앞에서 배운 함수는 `eval_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.

노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

함수 `four_modes(messages, reference, evaluators)`는 02절 노트북에서 처음 적은 함수이고, 이 절부터 도구 파일에서 가져옵니다.
도구 파일에는 02절 셀의 주석과 본문을 글자 그대로 옮겼고, 인자도 02절과 같습니다.
함수 `sum_usage(messages)`와 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`는 Ch 19 05절과 Ch 6 06절에서 배웠습니다.
두 함수는 Ch 21 도구 파일 `runner_tools.py`의 함수와 설명 주석·본문이 같습니다.

### [7] markdown {}

API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [8] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:23.102522Z', 'iopub.status.busy': '2026-09-29T02:26:23.102450Z', 'iopub.status.idle': '2026-09-29T02:26:23.108470Z', 'shell.execute_reply': '2026-09-29T02:26:23.108172Z'}, 'lesson_role': 'setup'}

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
temperature 값을 0으로 두어 매번 비슷한 답을 고르게 합니다.

### [10] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:23.109219Z', 'iopub.status.busy': '2026-09-29T02:26:23.109157Z', 'iopub.status.idle': '2026-09-29T02:26:24.274400Z', 'shell.execute_reply': '2026-09-29T02:26:24.273940Z'}}

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
이 노트북의 출력은 2026-09-29에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장과 판정이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
이 모델 객체 하나를 3절의 평가 모델과 4절의 에이전트에 함께 넘깁니다.

## 2. 모드와 평가 모델이 보는 것

01절에서 본 것처럼, 모드 `strict`는 도구 차례가 같고 답 글만 틀린 궤적을 참으로 봤습니다.
이 절의 앞 절반은 모델을 부르지 않고, 같은 궤적을 평가 모델이 어떤 글로 받는지 봅니다.
다음 셀은 01절과 같은 질문·기준 답·결과 글을 정합니다.
4절에서 만들 도구 함수도 이 결과 글을 내놓습니다.

### [12] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.275226Z', 'iopub.status.busy': '2026-09-29T02:26:24.275160Z', 'iopub.status.idle': '2026-09-29T02:26:24.277168Z', 'shell.execute_reply': '2026-09-29T02:26:24.276875Z'}}

```python
# 질문과 기준 답, 도구마다 돌아올 결과 글을 정합니다(01절과 같은 글 — 4절의 도구 함수도 이 글을 내놓음)
question = "일반 도서는 며칠 동안 빌릴 수 있나요?"
reference_answer = "일반 도서는 14일 동안 빌릴 수 있습니다."
tool_results = {
    "search_documents": "[LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.",
    "check_source": "LIB-001 문서가 있습니다. 제목: 도서 대출 기간",
}
print("질문:", question)
print("기준 답:", reference_answer)
print("결과 글을 정한 도구:", list(tool_results))
```

출력:
```
질문: 일반 도서는 며칠 동안 빌릴 수 있나요?
기준 답: 일반 도서는 14일 동안 빌릴 수 있습니다.
결과 글을 정한 도구: ['search_documents', 'check_source']

```

### [13] markdown {}

**결과 읽기** — 출력 줄 `기준 답: 일반 도서는 14일 동안 빌릴 수 있습니다.`가 보입니다.
라벨 `결과 글을 정한 도구:` 뒤에는 `'search_documents'`와 `'check_source'`가 있습니다.

다음 셀은 01절과 같은 도구 요청 둘로 기준 궤적을 만듭니다.
함수 `make_trajectory`와 `called_tool_names`는 01절에서 처음 적은 함수입니다.

### [14] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.277824Z', 'iopub.status.busy': '2026-09-29T02:26:24.277765Z', 'iopub.status.idle': '2026-09-29T02:26:24.279921Z', 'shell.execute_reply': '2026-09-29T02:26:24.279608Z'}}

```python
# 01절과 같은 도구 요청 둘로 기준 궤적을 만들고, 도구 차례와 메시지 수를 봅니다
search_args = {"query": "도서 대출 기간"}
source_args = {"doc_id": "LIB-001"}
reference_calls = [
    {"name": "search_documents", "args": search_args, "id": "call_1", "type": "tool_call"},
    {"name": "check_source", "args": source_args, "id": "call_2", "type": "tool_call"},
]
reference = make_trajectory(question, reference_calls, tool_results, reference_answer)
print("기준 궤적의 도구 차례:", called_tool_names(reference))
print("메시지 수:", len(reference))
```

출력:
```
기준 궤적의 도구 차례: ['search_documents', 'check_source']
메시지 수: 6

```

### [15] markdown {}

**결과 읽기** — 출력 줄 `기준 궤적의 도구 차례: ['search_documents', 'check_source']`와 `메시지 수: 6`이 보입니다.
01·02절의 기준 궤적과 같은 요청이고, 메시지 수도 같습니다.

다음 셀은 01절처럼 도구 요청은 기준과 같고, 답 글만 「7일」로 틀린 궤적을 만듭니다.

### [16] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.280460Z', 'iopub.status.busy': '2026-09-29T02:26:24.280411Z', 'iopub.status.idle': '2026-09-29T02:26:24.282119Z', 'shell.execute_reply': '2026-09-29T02:26:24.281842Z'}}

```python
# 01절처럼 도구 요청은 기준과 같고 답 글만 틀린 궤적을 만듭니다
wrong_text = "일반 도서는 7일 동안 빌릴 수 있습니다."
wrong_answer = make_trajectory(question, reference_calls, tool_results, wrong_text)
print("도구 차례:", called_tool_names(wrong_answer))
print("최종 답:", wrong_answer[-1].content)
```

출력:
```
도구 차례: ['search_documents', 'check_source']
최종 답: 일반 도서는 7일 동안 빌릴 수 있습니다.

```

### [17] markdown {}

**결과 읽기** — 출력 줄 `최종 답: 일반 도서는 7일 동안 빌릴 수 있습니다.`가 보입니다.
라벨 `도구 차례:` 뒤의 목록은 기준 궤적과 같습니다.

다음 셀은 02절처럼 모드 넷마다 평가 함수를 하나씩 만들어, 딕셔너리 `evaluators`에 모읍니다.
02절에서는 답만 틀린 궤적을 네 모드로 견주지 않았습니다.

### [18] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.282624Z', 'iopub.status.busy': '2026-09-29T02:26:24.282577Z', 'iopub.status.idle': '2026-09-29T02:26:24.284574Z', 'shell.execute_reply': '2026-09-29T02:26:24.284102Z'}}

```python
# 02절처럼 모드 넷마다 궤적을 맞춰 보는 평가 함수를 하나씩 만들어, 모드 이름을 키로 모읍니다
modes = ["strict", "unordered", "subset", "superset"]
evaluators = {}
for mode in modes:
    evaluators[mode] = create_trajectory_match_evaluator(trajectory_match_mode=mode)
print("평가 함수를 만든 모드:", list(evaluators))
```

출력:
```
평가 함수를 만든 모드: ['strict', 'unordered', 'subset', 'superset']

```

### [19] markdown {}

**결과 읽기** — 출력 줄 `평가 함수를 만든 모드: ['strict', 'unordered', 'subset', 'superset']`이 보입니다.

다음 셀은 답만 틀린 궤적을 네 모드로 견줍니다.
함수 `four_modes`는 모드 이름을 키로 한 점수 딕셔너리를 내놓습니다.
실행 전에 예상해 봅니다.
답 글이 틀렸다는 것을 잡는 모드가 있을까요?

### [20] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.285321Z', 'iopub.status.busy': '2026-09-29T02:26:24.285257Z', 'iopub.status.idle': '2026-09-29T02:26:24.287605Z', 'shell.execute_reply': '2026-09-29T02:26:24.287262Z'}}

```python
# 답만 틀린 궤적을 02절 함수 four_modes로 네 모드 모두에 견줍니다
wrong_row = four_modes(wrong_answer, reference, evaluators)
print("답만 틀림:", wrong_row)
```

출력:
```
답만 틀림: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}

```

### [21] markdown {}

**결과 읽기** — 출력 줄 `답만 틀림: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}`가 보입니다.
네 모드 모두 참이었습니다.

네 모드는 도구 요청의 이름과 인자를 짝지을 뿐, 메시지 글은 견주지 않습니다.
그래서 답이 틀린 궤적도 도구를 기준대로 불렀다면 참입니다.
답 글까지 보려면, 궤적을 글로 읽는 쪽이 있어야 합니다.

다음 셀은 평가 모델이 받을 궤적 글을 만듭니다.
함수 `_format_inputs`에 실제 궤적과 기준 궤적을 넣으면, 두 궤적을 글로 바꾼 값 둘을 튜플로 내놓습니다.
번호 `[0]`이 실제 궤적 글이고, 번호 `[1]`이 기준 궤적 글입니다.

### [22] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.288180Z', 'iopub.status.busy': '2026-09-29T02:26:24.288129Z', 'iopub.status.idle': '2026-09-29T02:26:24.289796Z', 'shell.execute_reply': '2026-09-29T02:26:24.289568Z'}}

```python
# 평가 모델이 받을 궤적 글을 만듭니다(설치판 함수 _format_inputs — 실제 궤적 글과 기준 궤적 글을 튜플로 내놓음)
formatted = _format_inputs(wrong_answer, reference)
judge_text = formatted[0]
print("실제 궤적 글:")
print(judge_text)
```

출력:
```
실제 궤적 글:
<user>
일반 도서는 며칠 동안 빌릴 수 있나요?
</user>

<assistant>
<tool_call>
<name>search_documents</name>
<arguments>{"query": "도서 대출 기간"}</arguments>
</tool_call>
</assistant>

<tool>
<tool_result>
<id>call_1</id>
<content>[LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.</content>
</tool_result>
</tool>

<assistant>
<tool_call>
<name>check_source</name>
<arguments>{"doc_id": "LIB-001"}</arguments>
</tool_call>
</assistant>

<tool>
<tool_result>
<id>call_2</id>
<content>LIB-001 문서가 있습니다. 제목: 도서 대출 기간</content>
</tool_result>
</tool>

<assistant>
일반 도서는 7일 동안 빌릴 수 있습니다.
</assistant>

```

### [23] markdown {}

**결과 읽기** — 라벨 줄 `실제 궤적 글:` 아래가 평가 모델이 받는 궤적 글입니다.
메시지마다 `<user>`·`<assistant>`·`<tool>` 같은 태그로 감쌌습니다.
도구 요청은 `<tool_call>` 안에 이름과 인자를, 도구 메시지는 `<tool_result>` 안에 호출 ID와 글을 담았습니다.
마지막 `<assistant>` 태그 안에는 답 글 `일반 도서는 7일 동안 빌릴 수 있습니다.`가 그대로 있습니다.

이처럼 궤적의 메시지를 태그로 감싸 한 덩어리로 이은 글을, 이 절에서는 궤적 글이라고 부릅니다.
설치판 agentevals 0.0.9 `trajectory/llm.py` 77~95행이 이 함수입니다.
메시지를 태그로 감싸는 줄은 설치판 openevals 0.2.0 `utils.py` 427~454행에 있습니다.

다음 셀은 이 궤적 글에 답 글·검색 결과 글·호출 ID가 들어 있는지 봅니다.
셋 모두 모드 `strict`가 견주지 않는 것입니다.

### [24] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.290495Z', 'iopub.status.busy': '2026-09-29T02:26:24.290444Z', 'iopub.status.idle': '2026-09-29T02:26:24.292213Z', 'shell.execute_reply': '2026-09-29T02:26:24.291914Z'}}

```python
# 궤적 글에 답 글·검색 결과 글·호출 ID가 들어 있는지 봅니다(모드는 셋 다 견주지 않음)
print("답 글이 들어 있는가:", wrong_text in judge_text)
print("검색 결과 글이 들어 있는가:", tool_results["search_documents"] in judge_text)
print("호출 ID가 들어 있는가:", "call_1" in judge_text)
print("기준 궤적 글에 기준 답이 들어 있는가:", reference_answer in formatted[1])
```

출력:
```
답 글이 들어 있는가: True
검색 결과 글이 들어 있는가: True
호출 ID가 들어 있는가: True
기준 궤적 글에 기준 답이 들어 있는가: True

```

### [25] markdown {}

**결과 읽기** — 네 줄 모두 `True`입니다.
출력 줄 `답 글이 들어 있는가: True`와 `검색 결과 글이 들어 있는가: True`가 보입니다.

평가 모델은 도구 요청뿐 아니라 답 글과 도구 결과 글까지 한 글로 받습니다.
그래서 답 글의 「7일」이 검색 결과 글의 「14일」과 맞지 않는다는 것도 글에 드러납니다.
호출 ID도 글에 들어갑니다.
4절 에이전트의 호출 ID는 모델 서비스가 정한 값이라, 실행마다 궤적 글이 조금씩 달라집니다.

## 3. 판정 기준과 평가 모델

Ch 15 02절에서는 판정할 기준을 적은 글을 판정 머리글이라고 불렀습니다.
이름 `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE`는 라이브러리가 적어 둔 영어 판정 머리글입니다.
머리글 안에는 판정 기준과, 두 궤적 글을 끼울 자리 둘이 있습니다.
다음 셀은 판정 기준 줄을 출력하고, 2절의 두 궤적 글을 끼운 요청 글의 글자 수를 셉니다.
글 메서드 `startswith`와 `format`은 처음 쓰는 이름이라, 셀 주석에 한 줄씩 풀었습니다.

### [26] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.292816Z', 'iopub.status.busy': '2026-09-29T02:26:24.292758Z', 'iopub.status.idle': '2026-09-29T02:26:24.294436Z', 'shell.execute_reply': '2026-09-29T02:26:24.294171Z'}}

```python
# 판정 머리글에서 판정 기준 네 줄을 보고, 두 궤적 글을 끼운 요청 글의 글자 수를 셉니다
print("판정 기준:")
for line in TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE.splitlines():
    # 글의 메서드 startswith는 글이 괄호 안의 글로 시작하면 참을 냅니다
    if line.startswith("  - "):
        print(line)
# 글의 메서드 format은 머리글 속 {outputs}·{reference_outputs} 자리에 같은 이름의 인자 값을 채웁니다
request_text = TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE.format(outputs=judge_text, reference_outputs=formatted[1])
print("요청 글의 글자 수:", len(request_text))
```

출력:
```
판정 기준:
  - Makes logical sense between steps
  - Shows clear progression
  - Is relatively efficient, though it does not need to be perfectly efficient
  - Is semantically equivalent to the provided reference trajectory
요청 글의 글자 수: 1694

```

### [27] markdown {}

**결과 읽기** — 라벨 줄 `판정 기준:` 아래 네 줄이 판정 기준입니다.
출력 줄 `요청 글의 글자 수: 1694`가 보입니다.

네 줄은 차례대로 이렇게 풉니다.
단계와 단계가 논리적으로 이어지는가, 한 단계씩 나아가는가를 봅니다.
완벽하지 않아도 되지만 필요 없는 단계가 적은가, 기준 궤적과 뜻이 같은가도 봅니다.
평가 모델은 이 요청 글을 받아, 네 기준에 맞는지 참·거짓 하나로 판정합니다.

다음 셀은 평가 모델로 궤적을 판정하는 평가 함수를 만듭니다.
인자 `judge=`에는 1절에서 만든 모델 객체를, 인자 `prompt=`에는 판정 머리글을 넣습니다.
이 셀도 평가 함수를 만들기만 하고, 모델 요청은 보내지 않습니다.

### [28] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.295070Z', 'iopub.status.busy': '2026-09-29T02:26:24.294999Z', 'iopub.status.idle': '2026-09-29T02:26:24.296575Z', 'shell.execute_reply': '2026-09-29T02:26:24.296260Z'}}

```python
# 모델 객체와 판정 머리글로, 평가 모델이 궤적을 판정하는 평가 함수를 만듭니다(아직 요청은 보내지 않음)
accuracy_judge = create_trajectory_llm_as_judge(judge=model, prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE)
print("평가 함수의 종류:", type(accuracy_judge).__name__)
```

출력:
```
평가 함수의 종류: function

```

### [29] markdown {}

**결과 읽기** — 출력 줄 `평가 함수의 종류: function`이 보입니다.
01절의 궤적 맞춰 보기처럼, 만든 것은 부를 수 있는 함수입니다.

설치판 openevals 0.2.0 `llm.py`를 보면, 이 함수를 부를 때마다 모델에 요청을 1번 보냅니다.
모델은 칸 `reasoning`(글)과 칸 `score`(참·거짓)를 담은 JSON 형식으로 답합니다.
이 답할 모양도 요청 글과 함께 모델에 넘어갑니다.
모양의 설명 글에는 칸 `reasoning`을 「Thus, the score should be」로 끝내라는 말이 적혀 있습니다.
그래서 5절 판정 출력의 끝에 그 문장이 보입니다.

평가 함수는 이를 칸 `key`·`score`·`comment`·`metadata`의 딕셔너리로 내놓습니다.
칸 `comment`에 든 글, 곧 평가 모델이 그렇게 판정한 까닭을 판정 까닭이라고 부르겠습니다.
이 모양은 설치판 소스로 본 것이고, 노트북에서는 5절에서 처음 부릅니다.

## 4. 실제 에이전트로 궤적 만들기

지금까지의 궤적은 모두 코드로 적은 메시지 목록이었습니다.
이 절의 뒤 절반은 도구 둘을 붙인 에이전트를 실제 모델로 한 번 실행해, 그 결과를 궤적으로 씁니다.
이처럼 평가할 궤적을 만드는 에이전트를 평가받는 에이전트라고 부르겠습니다.

다음 셀은 검색 도구를 만듭니다.
Ch 19 01절처럼 `@tool` 줄은 아래 함수를 도구로 등록하고, 독스트링은 모델이 읽는 도구 설명이 됩니다.
이 검색 도구는 교재용이라, 어떤 검색어에도 2절 결과 글 딕셔너리의 검색 결과 글을 내놓습니다.

### [30] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.297164Z', 'iopub.status.busy': '2026-09-29T02:26:24.297106Z', 'iopub.status.idle': '2026-09-29T02:26:24.299526Z', 'shell.execute_reply': '2026-09-29T02:26:24.299173Z'}}

```python
# 검색 도구를 만듭니다(교재용 — 어떤 검색어에도 2절 결과 글 딕셔너리의 검색 결과 글을 내놓음)
@tool
def search_documents(query: str):
    """도서관 규정 문서를 검색어로 찾아, 문서 ID를 붙인 글로 내놓습니다."""
    return tool_results["search_documents"]
```

출력:
```

```

### [31] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
매개변수 뒤의 `: str`은 Ch 19 01절에서 본 힌트로, 도구의 입력이 글이라고 알립니다.

다음 셀은 출처 확인 도구를 만듭니다.
문서 ID가 `LIB-001`이면 2절의 출처 확인 결과 글을, 아니면 그 문서가 없다는 글을 내놓습니다.

### [32] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.300187Z', 'iopub.status.busy': '2026-09-29T02:26:24.300098Z', 'iopub.status.idle': '2026-09-29T02:26:24.302592Z', 'shell.execute_reply': '2026-09-29T02:26:24.302176Z'}}

```python
# 출처 확인 도구를 만듭니다(문서 ID가 LIB-001일 때만 문서가 있다고 내놓음)
@tool
def check_source(doc_id: str):
    """문서 ID로 그 문서가 있는지 확인하고, 있으면 제목을 내놓습니다."""
    if doc_id == "LIB-001":
        return tool_results["check_source"]
    return doc_id + " 문서가 없습니다."
```

출력:
```

```

### [33] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 두 도구를 모델 없이 직접 불러 봅니다.
Ch 19 01절처럼 메서드 `invoke`에 인자 딕셔너리를 넣습니다.

### [34] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.303219Z', 'iopub.status.busy': '2026-09-29T02:26:24.303159Z', 'iopub.status.idle': '2026-09-29T02:26:24.307622Z', 'shell.execute_reply': '2026-09-29T02:26:24.307352Z'}}

```python
# 두 도구를 인자 딕셔너리로 직접 불러 봅니다(모델 요청 없음)
print("검색:", search_documents.invoke({"query": "책 대출 기간"}))
print("출처 확인:", check_source.invoke({"doc_id": "LIB-001"}))
print("없는 문서:", check_source.invoke({"doc_id": "LIB-002"}))
```

출력:
```
검색: [LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.
출처 확인: LIB-001 문서가 있습니다. 제목: 도서 대출 기간
없는 문서: LIB-002 문서가 없습니다.

```

### [35] markdown {}

**결과 읽기** — 라벨 `검색:` 뒤에는 검색어 「책 대출 기간」과 상관없이 `[LIB-001]`로 시작하는 검색 결과 글이 있습니다.
출력 줄 `없는 문서: LIB-002 문서가 없습니다.`가 보입니다.
두 도구 모두 정해진 글을 내놓는 평범한 Python 함수라, 다시 실행해도 같은 글이 나옵니다.

다음 셀은 평가받는 에이전트를 만듭니다.
Ch 21 01절처럼 함수 `create_agent`에 모델 객체와 도구 목록, 시스템 메시지 글을 넘깁니다.
Ch 22 04절의 호출 한도 4를 붙여, invoke 한 번에 모델 요청이 4번을 넘지 않게 합니다.
Ch 20 03절의 설정 딕셔너리로 실행 한도 20도 줍니다.
시스템 메시지 글에는 검색한 뒤 출처를 확인하고 답하라는 차례를 적었습니다.

### [36] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.308149Z', 'iopub.status.busy': '2026-09-29T02:26:24.308103Z', 'iopub.status.idle': '2026-09-29T02:26:24.315747Z', 'shell.execute_reply': '2026-09-29T02:26:24.315450Z'}}

```python
# 도구 둘·시스템 메시지 글·호출 한도 4로 평가받는 에이전트를 만듭니다(Ch 21 01절·Ch 22 04절 모양)
call_limit = ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")
agent_rule = "도서관 규정 질문에는 먼저 search_documents로 문서를 찾고, 찾은 문서 ID로 check_source를 불러 문서가 있는지 확인한 뒤, 확인한 문서의 글만 근거로 한국어 한 문장으로 답하세요."
library_agent = create_agent(model, tools=[search_documents, check_source], system_prompt=agent_rule, middleware=[call_limit])
# 실행 한도는 Ch 20 03절의 설정 딕셔너리로 줍니다(그래프 단계 수 상한)
run_config = {"recursion_limit": 20}
print("에이전트의 종류:", type(library_agent).__name__)
print("실행 한도:", run_config["recursion_limit"])
```

출력:
```
에이전트의 종류: CompiledStateGraph
실행 한도: 20

```

### [37] markdown {}

**결과 읽기** — 출력 줄 `에이전트의 종류: CompiledStateGraph`와 `실행 한도: 20`이 보입니다.
Ch 21 01절에서 본 것처럼, 에이전트는 컴파일된 그래프입니다.

호출 한도는 모델 요청 수의 상한이고, 실행 한도는 그래프 단계 수의 상한입니다.
두 한도는 서로 다른 것이고, 둘 다 이 절의 실행에 드는 값보다 조금 크게 잡은 교재용 값입니다.

다음 셀에서 모델 요청이 처음 나갑니다.
질문 한 줄을 넣어 에이전트를 한 번 실행하고, 결과의 칸 `messages`를 궤적으로 씁니다.
Ch 19 06절 함수 `show_messages`로 메시지를 차례대로 봅니다.
실행 전에 예상해 봅니다.
에이전트는 시스템 메시지 글대로 도구 둘을 차례로 부를까요?

### [38] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:24.316311Z', 'iopub.status.busy': '2026-09-29T02:26:24.316263Z', 'iopub.status.idle': '2026-09-29T02:26:26.904858Z', 'shell.execute_reply': '2026-09-29T02:26:26.904180Z'}}

```python
# 에이전트를 한 번 실행해 궤적을 만들고, 메시지를 차례대로 봅니다(모델 요청은 여기서 처음 나감)
first_input = {"messages": [HumanMessage(content=question)]}
result = library_agent.invoke(first_input, run_config)
agent_messages = result["messages"]
show_messages(agent_messages)
```

출력:
```
HumanMessage
AIMessage | 도구 호출 요청: ['search_documents']
ToolMessage | 결과 상태: success | 내용: [LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.
AIMessage | 도구 호출 요청: ['check_source']
ToolMessage | 결과 상태: success | 내용: LIB-001 문서가 있습니다. 제목: 도서 대출 기간
AIMessage | 도구 호출 요청: []

```

### [39] markdown {}

**결과 읽기** — 출력 줄 `AIMessage | 도구 호출 요청: ['search_documents']`와 `AIMessage | 도구 호출 요청: ['check_source']`가 보입니다.
두 줄 뒤에는 `ToolMessage | 결과 상태: success`로 시작하는 줄이 하나씩 이어집니다.
마지막 줄 `AIMessage | 도구 호출 요청: []`는 도구를 요청하지 않은 응답, 곧 답입니다.
에이전트는 검색 → 출처 확인 → 답의 차례로 움직였습니다.

도구를 몇 번, 어떤 차례로 부를지는 모델이 고르는 값입니다.
노트북 밖에서 같은 실행을 다섯 번 해 보니 다섯 번 모두 이 차례였고, 새 커널 두 번에서도 같았습니다.

다음 셀은 결과 메시지의 종류를 모아, 시스템 메시지가 들어 있는지 봅니다.
결과에 시스템 메시지가 있으면, 기준 궤적과 메시지 수가 어긋나 모드 `strict`가 거짓이 됩니다.

### [40] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:26.905681Z', 'iopub.status.busy': '2026-09-29T02:26:26.905602Z', 'iopub.status.idle': '2026-09-29T02:26:26.907644Z', 'shell.execute_reply': '2026-09-29T02:26:26.907180Z'}}

```python
# 결과 메시지의 종류를 차례대로 모으고, 시스템 메시지가 들어 있는지 봅니다
kinds = []
for message in agent_messages:
    kinds.append(type(message).__name__)
print("메시지 수:", len(kinds))
print("시스템 메시지가 들어 있는가:", "SystemMessage" in kinds)
# 시스템 메시지 글은 모델에 보낼 때만 앞에 붙고 결과 목록에는 남지 않습니다(라이브러리 동작이라 assert로 확인)
assert "SystemMessage" not in kinds
```

출력:
```
메시지 수: 6
시스템 메시지가 들어 있는가: False

```

### [41] markdown {}

**결과 읽기** — 출력 줄 `시스템 메시지가 들어 있는가: False`가 보이고, `assert`도 오류 없이 지나갔습니다.
출력 줄 `메시지 수: 6`으로, 메시지 수는 기준 궤적과 같습니다.

함수 `create_agent`는 시스템 메시지 글을 모델에 보낼 때만 메시지 목록 앞에 붙입니다.
설치판 langchain 1.4.0 `agents/factory.py` 1451~1452행이 그 줄이고, 결과 목록에는 남기지 않습니다.
그래서 결과의 칸 `messages`를 기준 궤적과 그대로 견줄 수 있습니다.

Ch 26~28에서는 모델 요청 수를 「도구를 요청한 응답 수 + 1」로 셌습니다.
다음 셀은 도구를 요청한 응답 수를 세고, Ch 19 05절 함수 `sum_usage`로 센 요청 수와 견줍니다.

### [42] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:26.908394Z', 'iopub.status.busy': '2026-09-29T02:26:26.908328Z', 'iopub.status.idle': '2026-09-29T02:26:26.910562Z', 'shell.execute_reply': '2026-09-29T02:26:26.910205Z'}}

```python
# 도구를 요청한 응답 수를 세고, Ch 19 05절 함수 sum_usage로 센 모델 요청 수와 견줍니다
asked_responses = 0
for message in agent_messages:
    if type(message).__name__ == "AIMessage":
        if len(tool_call_names(message)) > 0:
            asked_responses = asked_responses + 1
run_usage = sum_usage(agent_messages)
print("도구를 요청한 응답 수:", asked_responses)
print("모델 요청 수:", run_usage["requests"])
print("모델 요청 수 = 도구를 요청한 응답 수 + 1:", run_usage["requests"] == asked_responses + 1)
```

출력:
```
도구를 요청한 응답 수: 2
모델 요청 수: 3
모델 요청 수 = 도구를 요청한 응답 수 + 1: True

```

### [43] markdown {}

**결과 읽기** — 출력 줄 `도구를 요청한 응답 수: 2`와 `모델 요청 수: 3`이 보입니다.
출력 줄 `모델 요청 수 = 도구를 요청한 응답 수 + 1: True`로, 셈이 맞았습니다.

도구를 요청한 응답 둘에, 답을 쓴 응답 하나가 더해졌습니다.
호출 한도 4 안이라 실행이 끝까지 갔습니다.
함수 `sum_usage`는 결과 목록의 응답만 세므로, 평가 모델 요청은 이 셈에 들어가지 않습니다.

다음 셀은 도구 차례와 모델이 쓴 도구 인자, 마지막 답 글을 봅니다.
인자와 답 글은 모델이 쓴 값이라 실행마다 달라질 수 있습니다.

### [44] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:26.911235Z', 'iopub.status.busy': '2026-09-29T02:26:26.911174Z', 'iopub.status.idle': '2026-09-29T02:26:26.913089Z', 'shell.execute_reply': '2026-09-29T02:26:26.912724Z'}}

```python
# 에이전트의 도구 차례, 모델이 쓴 도구 인자, 마지막 답 글을 봅니다(인자와 답 글은 실행마다 달라질 수 있음)
print("도구 차례:", called_tool_names(agent_messages))
for message in agent_messages:
    if type(message).__name__ == "AIMessage":
        for call in message.tool_calls:
            print("도구 인자:", call["args"])
print("마지막 답 글:", agent_messages[-1].content)
```

출력:
```
도구 차례: ['search_documents', 'check_source']
도구 인자: {'query': '일반 도서 대출 기간 며칠'}
도구 인자: {'doc_id': 'LIB-001'}
마지막 답 글: 일반 도서는 14일 동안 빌릴 수 있습니다.

```

### [45] markdown {}

**결과 읽기** — 출력 줄 `도구 차례: ['search_documents', 'check_source']`가 보입니다.
라벨 `도구 인자:` 뒤에는 검색어와 문서 ID가, 라벨 `마지막 답 글:` 뒤에는 에이전트가 쓴 답이 있습니다.

교재 출력에서는 검색어가 「일반 도서 대출 기간 며칠」로, 기준 궤적의 「도서 대출 기간」과 달랐습니다.
문서 ID는 `LIB-001`로 기준과 같았고, 답 글은 기준 답과 글자까지 같았습니다.
02절 7절에서 본 것처럼, 인자 비교 방식이 기본값 `exact`면 검색어 하나만 달라도 네 모드 모두 거짓입니다.

## 5. 두 판정: 모드와 평가 모델

검색어는 모델이 고르는 값이라, 기준 궤적의 검색어와 다를 수 있습니다.
그래서 02절 7절의 도구별 덮어쓰기로 검색 도구의 인자만 보지 않고, 차례와 출처 문서 ID는 그대로 견줍니다.
다음 셀은 이런 평가 함수를 모드 넷마다 만들어 딕셔너리 `search_free`에 모읍니다.

### [46] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:26.913917Z', 'iopub.status.busy': '2026-09-29T02:26:26.913850Z', 'iopub.status.idle': '2026-09-29T02:26:26.915829Z', 'shell.execute_reply': '2026-09-29T02:26:26.915411Z'}}

```python
# 검색 도구의 인자만 보지 않는 평가 함수를 모드 넷마다 만듭니다(02절 7절의 도구별 덮어쓰기)
search_free = {}
for mode in modes:
    search_free[mode] = create_trajectory_match_evaluator(
        trajectory_match_mode=mode,
        tool_args_match_overrides={"search_documents": "ignore"},
    )
print("평가 함수를 만든 모드:", list(search_free))
```

출력:
```
평가 함수를 만든 모드: ['strict', 'unordered', 'subset', 'superset']

```

### [47] markdown {}

**결과 읽기** — 출력 줄 `평가 함수를 만든 모드: ['strict', 'unordered', 'subset', 'superset']`이 보입니다.
네 평가 함수 모두 검색 도구 요청의 인자는 보지 않고, 출처 확인 요청의 인자는 기본값 `exact`로 견줍니다.

다음 셀은 에이전트 궤적을 이 네 평가 함수로 견줍니다.
모드 판정은 코드 규칙이라, 같은 궤적이면 늘 같은 판정이 나옵니다.

### [48] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:26.916785Z', 'iopub.status.busy': '2026-09-29T02:26:26.916731Z', 'iopub.status.idle': '2026-09-29T02:26:26.919679Z', 'shell.execute_reply': '2026-09-29T02:26:26.919199Z'}}

```python
# 에이전트 궤적을 검색어를 빼고 네 모드로 견줍니다(같은 궤적이면 늘 같은 판정)
agent_row = four_modes(agent_messages, reference, search_free)
print("에이전트 궤적:", agent_row)
```

출력:
```
에이전트 궤적: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}

```

### [49] markdown {}

**결과 읽기** — 출력 줄 `에이전트 궤적: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}`가 보입니다.
네 모드 모두 참이었습니다.

검색어를 빼고 보면, 에이전트는 기준 궤적과 같은 도구를 같은 차례·같은 횟수로 불렀습니다.
출처 확인의 문서 ID도 기준과 같았습니다.
이 판정은 궤적이 정해지면 늘 같지만, 궤적을 만든 쪽은 모델이라 궤적은 실행마다 달라질 수 있습니다.

다음 셀은 3절에서 만든 평가 함수로 에이전트 궤적을 판정합니다.
평가 모델 요청이 1번 나갑니다.
칸 `key`·`score`는 한 줄씩, 판정 까닭은 라벨 줄 아래에 출력합니다.
실행 전에 예상해 봅니다.
검색어가 기준과 다른 이 궤적을, 평가 모델은 참으로 볼까요?

### [50] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:26.920338Z', 'iopub.status.busy': '2026-09-29T02:26:26.920289Z', 'iopub.status.idle': '2026-09-29T02:26:28.349047Z', 'shell.execute_reply': '2026-09-29T02:26:28.348233Z'}}

```python
# 평가 모델이 에이전트 궤적을 기준 궤적과 견줘 판정합니다(평가 모델 요청 1번)
agent_judged = accuracy_judge(outputs=agent_messages, reference_outputs=reference)
print("칸 key:", agent_judged["key"])
print("칸 score:", agent_judged["score"])
print("판정 까닭:")
print(agent_judged["comment"])
```

출력:
```
칸 key: trajectory_accuracy
칸 score: True
판정 까닭:
The actual trajectory follows the same logical sequence as the reference: it searches for the loan period, retrieves the same supporting document stating that general books can be borrowed for 14 days, verifies the source document, and then answers with the same final statement. The wording of the search query and tool call IDs differ, but these are inconsequential and the trajectory remains semantically equivalent and efficient. Thus, the score should be: true.

```

### [51] markdown {}

**결과 읽기** — 출력 줄 `칸 key: trajectory_accuracy`와 `칸 score: True`가 보입니다.
평가 모델도 에이전트 궤적을 참으로 판정했습니다.

라벨 줄 `판정 까닭:` 아래 글은 평가 모델이 영어로 쓴 판정 까닭입니다.
교재 출력의 판정 까닭은, 검색어 글과 호출 ID는 다르지만 판정에 상관없고 뜻이 같다는 줄거리였습니다.
판정 까닭의 글은 실행마다 조금씩 달라져, 이 절은 결론에 쓰지 않습니다.
점수 `True`는 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

## 6. 값 바꿔 보기: 답 글 하나만 틀리게

이제 값 하나만 바꿔 봅니다.
바꿀 값은 에이전트 궤적의 마지막 답 글이고, 01절의 틀린 답 「7일」로 바꿉니다.
도구 요청과 도구 결과 글은 그대로 둡니다.
다음 셀은 궤적을 Ch 2 03절에서 배운 목록 메서드 `copy()`로 복사하고, 복사본의 마지막 자리 `[-1]`에 새 `AIMessage`를 넣습니다.

### [52] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:28.350610Z', 'iopub.status.busy': '2026-09-29T02:26:28.350503Z', 'iopub.status.idle': '2026-09-29T02:26:28.353865Z', 'shell.execute_reply': '2026-09-29T02:26:28.353044Z'}}

```python
# 값 바꿔 보기: 에이전트 궤적을 복사해, 복사본의 마지막 답 글 하나만 01절의 틀린 답으로 바꿉니다
wrong_run = agent_messages.copy()
wrong_run[-1] = AIMessage(content=wrong_text)
print("바꾸기 전 답:", agent_messages[-1].content)
print("바꾼 뒤 답:", wrong_run[-1].content)
print("도구 차례가 같은가:", called_tool_names(wrong_run) == called_tool_names(agent_messages))
```

출력:
```
바꾸기 전 답: 일반 도서는 14일 동안 빌릴 수 있습니다.
바꾼 뒤 답: 일반 도서는 7일 동안 빌릴 수 있습니다.
도구 차례가 같은가: True

```

### [53] markdown {}

**결과 읽기** — 출력 줄 `바꾼 뒤 답: 일반 도서는 7일 동안 빌릴 수 있습니다.`와 `도구 차례가 같은가: True`가 보입니다.
라벨 `바꾸기 전 답:` 뒤에는 에이전트가 쓴 답이 있습니다.

복사본만 바꿨으므로, 목록 `agent_messages`의 답 글은 그대로입니다.
다음 셀은 이 궤적을 모드 `strict`(검색어 뺌)와 평가 모델로 판정합니다.
평가 모델 요청이 1번 나갑니다.
실행 전에 예상해 봅니다.
두 판정 가운데 답 글이 바뀐 것을 잡는 쪽은 어느 쪽일까요?

### [54] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:28.355200Z', 'iopub.status.busy': '2026-09-29T02:26:28.355048Z', 'iopub.status.idle': '2026-09-29T02:26:29.736972Z', 'shell.execute_reply': '2026-09-29T02:26:29.735878Z'}}

```python
# 답 글만 바꾼 궤적을 모드 strict(검색어 뺌)와 평가 모델로 판정합니다(평가 모델 요청 1번)
wrong_strict = trajectory_pass(wrong_run, reference, search_free["strict"])
wrong_judged = accuracy_judge(outputs=wrong_run, reference_outputs=reference)
print("모드 strict:", wrong_strict)
print("평가 모델 칸 score:", wrong_judged["score"])
print("판정 까닭:")
print(wrong_judged["comment"])
```

출력:
```
모드 strict: True
평가 모델 칸 score: False
판정 까닭:
The trajectory follows the same logical tool-use pattern as the reference: it searches for the loan period, verifies the source document, and then answers. However, the final answer is semantically incorrect because the reference states that general books can be borrowed for 14 days, while the actual trajectory answers 7 days. Since the final response does not match the reference trajectory's conclusion, the trajectory is not accurate. Thus, the score should be: false.

```

### [55] markdown {}

**결과 읽기** — 출력 줄 `모드 strict: True`와 `평가 모델 칸 score: False`가 보입니다.
답 글 하나만 바꾸자, 평가 모델의 판정만 참에서 거짓으로 바뀌었습니다.

모드 `strict`는 2절에서 본 것처럼 답 글을 견주지 않아, 바꾸기 전과 같은 참이었습니다.
평가 모델은 답 글까지 읽고, 기준 궤적과 뜻이 다르다고 판정했습니다.
교재 출력의 판정 까닭은, 도구를 부른 차례는 같지만 답이 14일이 아니라 7일이라 뜻이 맞지 않다는 줄거리였습니다.
점수 `False`는 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

다음 셀은 5절과 이 절에서 담아 둔 판정을 한 표로 모읍니다.
앞 셀들의 값을 출력만 하므로 새 요청은 없습니다.

### [56] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:29.739671Z', 'iopub.status.busy': '2026-09-29T02:26:29.739462Z', 'iopub.status.idle': '2026-09-29T02:26:29.743122Z', 'shell.execute_reply': '2026-09-29T02:26:29.742316Z'}}

```python
# 두 궤적의 두 판정을 한 표로 봅니다(앞 셀들이 담아 둔 값을 출력만 함 — 새 요청 없음)
print("궤적 | 모드 strict(검색어 뺌) | 평가 모델")
print("에이전트 궤적 |", agent_row["strict"], "|", agent_judged["score"])
print("답 글만 틀림 |", wrong_strict, "|", wrong_judged["score"])
```

출력:
```
궤적 | 모드 strict(검색어 뺌) | 평가 모델
에이전트 궤적 | True | True
답 글만 틀림 | True | False

```

### [57] markdown {}

**결과 읽기** — 라벨 줄 `궤적 | 모드 strict(검색어 뺌) | 평가 모델` 아래 두 줄이 보입니다.
줄 `에이전트 궤적 | True | True`와 `답 글만 틀림 | True | False`입니다.

두 줄은 답 글만 다르고, 모드는 두 줄을 가르지 못했습니다.
평가 모델만 두 줄을 갈랐습니다.
반대로 모드는 판정 규칙을 코드로 적어, 같은 궤적에는 늘 같은 판정을 냅니다.
두 방법은 서로를 대신하지 않고, 보려는 것에 맞춰 함께 씁니다.

## 7. 요청 수와 예상 비용

이 노트북은 에이전트 실행 한 번과 평가 모델 판정 두 번에서 모델을 불렀습니다.
평가 모델 요청은 에이전트 결과 목록에 남지 않아, 함수 `sum_usage`로 셀 수 없습니다.
설치판 소스대로 판정 한 번을 요청 1번으로 보고, 판정 횟수 2를 손으로 적어 더합니다.
다음 셀은 요청 수를 모두 더하고, 에이전트 요청의 토큰과 예상 비용을 봅니다.
요금은 2026-09-17 요금표의 mini 값(100만 토큰당 달러)을 씁니다.

### [58] code {'execution': {'iopub.execute_input': '2026-09-29T02:26:29.744820Z', 'iopub.status.busy': '2026-09-29T02:26:29.744688Z', 'iopub.status.idle': '2026-09-29T02:26:29.748072Z', 'shell.execute_reply': '2026-09-29T02:26:29.747540Z'}}

```python
# 평가 모델 요청까지 더한 요청 수를 세고, 에이전트 요청의 토큰과 예상 비용을 봅니다(요금표 2026-09-17, 100만 토큰당 달러)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
agent_cost = estimate_cost(run_usage, input_rate, cached_input_rate, output_rate)
judge_requests = 2
print("에이전트 요청 수:", run_usage["requests"], "| 평가 모델 요청 수:", judge_requests)
print("모두 합한 모델 요청 수:", run_usage["requests"] + judge_requests)
print("에이전트 입력 토큰:", run_usage["input_tokens"], "| 출력 토큰:", run_usage["output_tokens"])
print("에이전트 예상 비용(달러):", round(agent_cost, 6))
```

출력:
```
에이전트 요청 수: 3 | 평가 모델 요청 수: 2
모두 합한 모델 요청 수: 5
에이전트 입력 토큰: 933 | 출력 토큰: 63
에이전트 예상 비용(달러): 0.000983

```

### [59] markdown {}

**결과 읽기** — 출력 줄 `에이전트 요청 수: 3 | 평가 모델 요청 수: 2`와 `모두 합한 모델 요청 수: 5`가 보입니다.
에이전트 요청 수는 4절에서 센 값과 같습니다.

교재 출력에서는 에이전트 입력 토큰이 933, 출력 토큰이 63이었고, 예상 비용은 0.000983달러였습니다.
평가 모델 요청의 토큰은 이 노트북에서 세지 않았습니다.
노트북 밖에서 센 값으로는, 판정 한 번에 입력 679~682토큰, 출력 87~104토큰이었습니다.
토큰과 비용은 실행마다 달라질 수 있고, 청구 금액과도 다를 수 있습니다.

## 정리

1. 네 모드는 답만 틀린 궤적을 모두 참으로 봤습니다. 평가 모델이 받는 궤적 글에는 답 글과 도구 결과 글이 들어 있었습니다.
2. 평가받는 에이전트는 요청 3번으로 검색 → 출처 확인 → 답의 궤적을 만들었습니다. 검색어를 뺀 네 모드와 평가 모델이 모두 참으로 판정했습니다.
3. 답 글 하나만 바꾸자, 모드 `strict`는 참 그대로였고 평가 모델만 거짓을 냈습니다. 2·3번의 값은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

04절에서는 모델을 부르지 않고, 앞 챕터가 저장한 실행 기록을 읽어 운영 지표를 견줍니다.

## 그림

### 03-1-모드와-평가-모델이-보는-것.mmd

```mermaid
flowchart TB
  %% classes
  wr["답만 틀린 궤적<br>도구 요청 둘은 기준과 같음<br>답 글 7일"]:::tool
  rf["기준 궤적<br>답 글 14일"]:::tool
  subgraph lane1["궤적 맞춰 보기"]
    direction TB
    md["모드 넷<br>도구 요청의 이름과<br>인자만 짝지음"]:::flow
    mr["네 모드 모두 True"]:::measure
    md --> mr
  end
  subgraph lane2["평가 모델"]
    direction TB
    fm["_format_inputs<br>메시지마다 태그로<br>감싼 궤적 글"]
    fr["답 글·검색 결과 글·<br>호출 ID 모두<br>들어 있음 True"]:::measure
    jd["평가 모델<br>3절에서 만들기만 함"]
    fm --> fr
    fr -.-> jd
  end
  wr --> md
  rf --> md
  wr --> fm
  rf --> fm
  style jd stroke-dasharray: 5 5
```

네 모드는 답만 틀린 궤적을 모두 참으로 봤고, 평가 모델이 받는 궤적 글에는 답 글과 도구 결과 글이 들어 있었습니다.

### 03-2-평가-모델이-받는-요청-글.mmd

```mermaid
flowchart TB
  %% classes
  tr["답만 틀린 궤적과 기준 궤적<br>메시지 여섯씩"]:::tool
  fm["_format_inputs<br>설치판 함수"]
  tx["궤적 글 둘<br>user·assistant·tool 태그"]:::measure
  hd["판정 머리글<br>판정 기준 네 줄과<br>궤적 글 자리 둘"]
  rq["요청 글 하나<br>글자 수 1694"]:::measure
  jd["평가 모델<br>이 칸에서는 부르지 않음"]
  rs["결과 딕셔너리<br>key·score<br>comment·metadata<br>설치판 소스로 본 모양"]
  tr --> fm
  fm --> tx
  tx --> rq
  hd --> rq
  rq -.-> jd
  jd -.-> rs
  style jd stroke-dasharray: 5 5
```

두 궤적 글을 판정 머리글에 끼우자 글자 수 1694의 요청 글이 되었고, 평가 모델은 이 글과 답할 모양을 함께 받습니다.

### 03-3-에이전트-궤적과-두-판정.mmd

```mermaid
flowchart TB
  %% classes
  ag["평가받는 에이전트<br>도구 둘 · 호출 한도 4<br>실행 한도 20"]:::flow
  am["gpt-5.4-mini<br>에이전트 요청 3번"]:::model
  tr["에이전트 궤적<br>search_documents<br>check_source<br>답 · 메시지 여섯"]:::measure
  mo["모드 넷<br>search_documents 인자만<br>ignore · 기준 궤적과 견줌"]:::flow
  mr["네 모드 모두 True"]:::measure
  jd["평가 모델 gpt-5.4-mini<br>판정 머리글 · 요청 1번"]:::model
  jr["칸 score True"]:::measure
  ag --> am
  am --> tr
  tr --> mo
  tr --> jd
  mo --> mr
  jd --> jr
```

노트북 밖 다섯 번과 두 커널에서 모두, 에이전트 궤적을 검색어를 뺀 네 모드와 평가 모델이 참으로 판정했습니다.

### 03-4-답-글-하나만-바꾸기.mmd

```mermaid
flowchart TB
  %% classes
  base["도구 요청과 도구 결과 글은<br>에이전트 궤적 그대로"]
  subgraph keep["에이전트 궤적 그대로"]
    direction TB
    k1["답 글<br>에이전트가 쓴 답"]:::measure
    k2["모드 strict True<br>평가 모델 True"]:::measure
    k1 --> k2
  end
  subgraph swap["마지막 답 글만 바꿈"]
    direction TB
    s1["답 글<br>일반 도서는 7일 동안<br>빌릴 수 있습니다."]:::flow
    s2["모드 strict True<br>평가 모델 False"]:::measure
    s1 --> s2
  end
  base --> keep
  base --> swap
```

노트북 밖 다섯 번과 두 커널에서 모두, 마지막 답 글 하나만 바꾸자 모드 strict는 참 그대로였고 평가 모델만 거짓을 냈습니다.

### 03-5-겹쳐-보기와-울려-보기.prompt.md

# 03-5-겹쳐-보기와-울려-보기 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 01·02절에서는 오르골 종이띠의 구멍을 기준 띠에 대 봤습니다. 두 띠를 겹쳐 보면, 구멍이 같은 자리에 같은 수만큼 있는지는 바로 보입니다. 그러나 겹쳐 보는 것만으로는 곡이 어떻게 들리는지 모릅니다. 기준 곡과 같은 노래인지 보려면, 띠를 오르골 기계에 넣어 울려 봐야 합니다. … 겹쳐 보는 쪽이 궤적 맞춰 보기의 모드이고, 울려 보는 쪽이 궤적 글을 읽는 평가 모델입니다.

구성 요소와 배치: 흰 바탕 **왼쪽에 겹쳐 놓은 종이띠 둘**(= 모드: 구멍 자리를 대 봄) · **오른쪽에 상자 없이 드러난 오르골 기계 둘**(빗 모양 쇠붙이·핀 박힌 원통·작은 손잡이, = 평가 모델), **기계마다 종이띠 하나씩**(= 실제 궤적 글·기준 궤적 글을 함께 읽음). 비유 계열 **「오르골 종이띠」**(챕터 리드 결정 9 — 03 후보 「띠를 겹쳐 대 보는 것만으로는 모르는 것을 곡조를 듣고 판정하는 장면」, 사람·귀 없이). **01 소품(닫힌 나무 오르골 상자·돋보기)·02 소품(띠 다섯·둥근/네모/세모 구멍) 되풀이 없음.** 금지 소품(저울·도장·쟁반·바구니·서랍 등 handoff 목록) 없음. 사람·손·귀·글자·숫자·음표·화살표·화면 없음.

시선 순서: 왼쪽 겹친 두 띠(정지한 채 대 봄) → 오른쪽 두 기계(띠가 지나가며 울림).

검수 기준: 그림만 보고 「왼쪽은 띠 둘을 겹쳐 놓았고, 오른쪽은 띠를 하나씩 기계에 넣었다」가 읽히는가. 띠 넷(왼쪽 둘·오른쪽 하나씩)·기계 둘이 정확한가. 글자·숫자·음표·사람·손·귀·화살표·닫힌 나무 상자·돋보기가 없는가.

## 프롬프트 (1차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. On the left, exactly two long cream paper strips with one row of round punched holes lie on top of each other, the upper strip shifted slightly down so both edges show, their holes lined up. On the right, exactly two small bare music box mechanisms stand side by side, each a brass comb with a pinned metal cylinder and a tiny crank, with no box around them, and each has one cream punched paper strip feeding into it. Objects are large and fill the frame. No wooden box, no magnifying glass, no people, no hands, no ears, no musical notes, no arrows, no screens.
```

## 상태

- 2026-09-29 · `generate_image` 한 번, `params` = `{"model":"nano_banana_pro","prompt":…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `generate_image` 응답 모델 `nano_banana_pro`, **`jobs_wait` 응답 모델 표시 `nano_banana_2`**(요청한 모델과 다름 — 01·02·Ch 25~28 삽화와 같은 표시, 거래 기록 표시는 「Nano Banana Pro」, 기록만).
- 생성 전 잔액 **2301**, 바로 앞 거래 2026-09-29T01:53:17.398658Z 「Nano Banana Pro −2」는 02절 몫(이 절이 요청하기 전).
- **1차 job `7bed63f6-84ce-4326-ab58-cbdc5fd7bba9` 채택** — 거래 **2026-09-29T02:29:22.794779Z 「Nano Banana Pro −2」**(결과 파일 이름 `hf_20260929_022922_7bed63f6…`와 같은 시각). 이 절 몫은 거래 한 줄, **2크레딧**(잔액 2301 → 2299). 재생성 0회. 결과 원본 `037603caa5fb22b2a8212badc52524b5559b48dab41da35e629e526c247b026a`(2752 × 1536).
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕 왼쪽에 크림색 종이띠 **둘**이 비스듬히, 조금 비켜 겹쳐 놓임(띠마다 둥근 구멍 한 줄 — 구멍 줄 둘이 나란히 보임, 프롬프트의 「구멍이 한 자리에 겹침」과는 다름). 오른쪽에 상자 없이 금색 틀만 있는 오르골 기계 **둘**(원통·빗 모양 쇠붙이·옆 손잡이 하나씩), 기계마다 구멍 뚫린 종이띠 **하나**가 위에서 아래로 지나감(띠 모두 **넷**). 기계 아래쪽 띠 구멍 몇 개가 짙게 칠해짐. 글자·숫자·음표·사람·손·귀·화살표·화면·닫힌 나무 상자·돋보기 없음.
- 검수: 「왼쪽은 띠 둘을 겹쳐 놓았고, 오른쪽은 띠를 하나씩 기계에 넣었다」가 그림만으로 읽힘 → 채택. 왼쪽 두 띠의 구멍이 한 자리에 겹치지 않고 나란히 보이는 점은 그림 읽기에 「조금 비켜 겹쳐」로 적고, 구멍 수·기울기·짙은 구멍·손잡이는 짝짓지 않는다고 밝힘(강사 확인 대상에 한 줄).
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch29-03/illu/illu-1-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/03-5-겹쳐-보기와-울려-보기.png`(1100 × 614, `bfa70e99950b666316cba23fd95ef274e348090bccd48dba320ed3f49837cc02`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-1-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG와 같은 사본(`.cache/ch29-03-view/illu-1-1100.png`, 해시 같음)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

