from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def md(s): return {"cell_type":"markdown","id":"","metadata":{},"source":s.splitlines(keepends=True)}
def code(s):
    return {"cell_type":"code","execution_count":None,"id":"","metadata":{},"outputs":[],"source":s.splitlines(keepends=True)}

INSTALL='''%pip install -q langchain==1.4.0 langchain-openai==1.6.1 python-dotenv==1.2.3 numpy==2.5.3
import sys
print("준비 완료:", sys.version.split()[0])'''
ENV='''# 현재 폴더에서 가까운 .env를 찾되 비밀 값은 출력하지 않습니다.
import os, time
from dotenv import find_dotenv, load_dotenv
env_path=find_dotenv(usecwd=True)
load_dotenv(env_path)
print("OPENAI_API_KEY:","있음" if os.getenv("OPENAI_API_KEY") else "없음")'''
DATA='''# 배포 묶음에서도 같은 상대 경로를 찾도록 프로젝트 루트를 거슬러 올라갑니다.
import json
from pathlib import Path
import numpy as np
root=next(p for p in [Path.cwd(),*Path.cwd().parents] if (p/"labs").is_dir())
data_dir=root/"labs/part4/ch14-rag-patterns/data"
docs=json.loads((data_dir/"documents.json").read_text(encoding="utf-8"))
queries=json.loads((data_dir/"queries.json").read_text(encoding="utf-8"))
print("문서·질문:",len(docs),len(queries))'''
MODELS='''# 256차원은 Ch12와 같은 비교 조건이며 행 하나가 문서 하나입니다.
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
chat=init_chat_model("gpt-4.1-mini",model_provider="openai",temperature=0)
embedder=OpenAIEmbeddings(model="text-embedding-3-small",dimensions=256)
vectors=np.array(embedder.embed_documents([d["text"] for d in docs]))
print("임베딩 배열:",vectors.shape)'''
HELPERS='''# 코사인 유사도는 내적을 두 벡터의 길이로 나누어 계산합니다.
from typing import Any
usage_log: list[dict[str, float | int]] = []

def search(question: str, k: int = 3) -> list[tuple[dict[str, Any], float]]:
    q=np.array(embedder.embed_query(question))
    scores=vectors@q/(np.linalg.norm(vectors,axis=1)*np.linalg.norm(q))
    # argsort 결과를 뒤집어 점수가 큰 문서부터 k개를 고릅니다.
    return [(docs[i],float(scores[i])) for i in np.argsort(scores)[::-1][:k]]
def ask(prompt: str) -> tuple[str, int, float]:
    started=time.perf_counter()
    msg=chat.invoke(prompt)
    usage=msg.usage_metadata or {}
    details=usage.get("input_token_details", {})
    input_tokens=usage.get("input_tokens", 0)
    cached_tokens=details.get("cache_read", 0)
    output_tokens=usage.get("output_tokens", 0)
    tokens=usage.get("total_tokens", 0)
    # 2026-09-10 gpt-4.1-mini 공개 단가로 추정하며 실제 청구액과 다를 수 있습니다.
    usd=((input_tokens-cached_tokens)*0.40+cached_tokens*0.10+output_tokens*1.60)/1_000_000
    usage_log.append({"input":input_tokens,"cached":cached_tokens,"output":output_tokens,"usd":usd})
    return msg.text,tokens,round((time.perf_counter()-started)*1000,1)

def show_hits(hits: list[tuple[dict[str, Any], float]]) -> list[tuple[str, float]]:
    return [(d["doc_id"],round(score,3)) for d,score in hits]'''

def nb(title,question,steps):
    cells=[md(f"# {title}\n\n{question}"),md("## 실행 환경 준비\n\n고정한 Python 패키지를 확인합니다."),code(INSTALL),md("## .env 찾기\n\n가까운 .env에서 키를 읽고 존재 여부만 표시합니다."),code(ENV),md("## 공통 데이터\n\nCh12의 축소 데이터와 Ch11 방식의 정답 문서 ID를 사용합니다."),code(DATA),md("## 모델과 임베딩\n\n모델과 256차원 문서 벡터를 준비합니다."),code(MODELS),md("## 검색·생성 함수\n\n검색 점수, 토큰, 시간, 추정 비용을 같은 방식으로 기록합니다."),code(HELPERS)]
    for heading,source in steps:
        notes = {
            "## 히스토리가 없는 검색":"대명사가 남은 후속 질문을 그대로 검색합니다. 출력에서 LIB-004의 기준선 순위를 확인합니다.",
            "## 모델로 독립 질문 만들기":"대화 기록과 후속 질문을 모델에 입력해 독립 질문을 만듭니다. 복원된 대상과 재작성 뒤 문서 순위를 비교합니다.",
            "## 검색 결과로 답하기":"재작성 질문으로 찾은 원문만 모델에 전달합니다. 답의 대출 기간과 인용 문서 ID를 확인합니다.",
            "## 기준선 검색":"원 질문 하나로 상위 두 문서를 검색합니다. 두 정답 문서 가운데 빠진 문서가 있는지 확인합니다.",
            "## 세 검색 질문 생성":"원 질문을 세 가지 검색 표현으로 바꿉니다. 출력 질문이 원래 대상과 조건을 유지하는지 확인합니다.",
            "## 후보 합치기":"원 질문과 변형 질문의 결과를 문서 ID로 합칩니다. 병합 후보와 두 정답 문서의 포함 여부를 확인합니다.",
            "## 복합 질문 검색":"두 이용 조건이 들어 있는 질문을 나누기 전에 검색합니다. 기준선 상위 문서 두 건을 기록합니다.",
            "## 하위 질문 생성":"복합 질문을 사실별 질문 두 개로 나눕니다. 전자자료와 일반 도서 조건이 각각 남았는지 확인합니다.",
            "## 각 질문을 따로 검색":"각 하위 질문에서 1위 원문을 고릅니다. 중복을 제거한 근거 문서 수가 늘었는지 확인합니다.",
            "## 구체 질문 검색":"날짜와 시각을 포함한 질문으로 먼저 검색합니다. FAC-003의 순위와 유사도를 기준선으로 기록합니다.",
            "## 넓은 질문 생성":"세부 질문을 일반 운영 규칙 질문으로 바꾸고 다시 검색합니다. 생성 토큰·시간과 넓은 검색 점수를 확인합니다.",
            "## 두 문맥으로 답하기":"두 검색의 문서를 ID로 합쳐 최종 답을 생성합니다. 폐관 시각 판단과 두 번째 생성 호출의 비용을 확인합니다.",
            "## 질문 임베딩 기준선":"원 질문을 바로 임베딩해 상위 세 문서를 찾습니다. 정답 ACC-003의 기준선 순위를 기록합니다.",
            "## 가상 문서 생성":"질문에서 가상 안내문을 만들고 그 문장을 임베딩해 검색합니다. 가상 내용과 실제 문서 순위를 구분해 확인합니다.",
            "## 결과 범위 확인":"두 검색에서 정답 ACC-003의 순위를 계산합니다. 순위가 1위에서 3위로 낮아졌는지 확인합니다.",
            "## 첫 검색과 품질 점수":"원 질문의 첫 검색 결과에서 최고 유사도를 읽습니다. 0.55 임계값과 비교할 0.322를 확인합니다.",
            "## 임계값에 따른 보정":"최고 점수가 임계값 미만이면 질문을 한 번 보정해 재검색합니다. 보정 질문과 바뀐 1위 문서를 확인합니다.",
            "## 반복 상한":"실제로 실행한 재검색 횟수를 상한과 비교합니다. 한 번을 넘으면 검사가 실패합니다.",
            "## 검색하고 초안 생성":"전자책 규정을 검색해 첫 답을 생성합니다. 대출 권수·기간과 인용 ID가 원문에 있는지 확인합니다.",
            "## 근거 충실도 평가":"초안에 통제 오류 문장을 붙여 근거 점수를 요청합니다. 숫자를 0~1로 제한한 뒤 0.5가 나온 과정을 확인합니다.",
            "## 한 번만 수정":"점수가 0.9 미만이면 원문에 없는 문장을 한 번 제거합니다. 최종 답과 세 호출의 합계 사용량을 확인합니다.",
            "## 범주별 묶음":"각 원문을 category 값으로 묶습니다. library·facility·account에 각각 네 건이 들어가는지 확인합니다.",
            "## 요약 노드 직접 생성":"범주별 원문을 요약하고 하위 문서 ID를 함께 저장합니다. 세 요약의 내용과 오프라인 생성 토큰·시간을 확인합니다.",
            "## 계층 검색":"질문과 가장 가까운 요약을 고른 뒤 그 범주의 원문만 검색합니다. facility 오선택과 하위 문서 ID를 확인합니다.",
            "## 비교 함수":"질문 한 건과 패턴 이름을 입력받아 검색부터 답 생성까지 실행합니다. 반환할 후보·정답 순위·사용량 필드를 확인합니다.",
            "## 세 패턴 실행":"같은 세 질문을 기준선·Multi-Query·HyDE로 실행합니다. 질문별 검색 후보와 답, 전체 지연 시간을 행 단위로 확인합니다.",
            "## Recall·토큰·시간 집계":"패턴별 세 행을 모아 Recall@3과 평균 토큰·시간·추정 비용을 계산합니다. 한 지표만 좋아진 경우도 그대로 비교합니다.",
            "## 공개 실행 로그 저장":"문서·질문 해시와 아홉 실행 행을 JSON으로 저장합니다. 다음 챕터가 같은 입력과 결과를 추적할 필드가 모두 있는지 확인합니다.",
        }
        comments = {
            "## 히스토리가 없는 검색":"# 대명사만 있는 후속 질문을 그대로 검색해 기준선을 만듭니다.",
            "## 모델로 독립 질문 만들기":"# 대화 기록에서 전자책이라는 대상을 복원해 검색 질문을 만듭니다.",
            "## 검색 결과로 답하기":"# 검색된 원문과 문서 ID만 답변 근거로 전달합니다.",
            "## 기준선 검색":"# 원문 질문 하나로 검색한 결과를 비교 기준으로 저장합니다.",
            "## 세 검색 질문 생성":"# 같은 의도를 다른 표현으로 바꾼 검색 질문을 최대 세 개 만듭니다.",
            "## 후보 합치기":"# 문서 ID로 중복을 제거하고 문서별 최고 유사도를 보존합니다.",
            "## 복합 질문 검색":"# 두 사실이 들어 있는 질문을 나누기 전에 한 번 검색합니다.",
            "## 하위 질문 생성":"# 전자자료와 일반 도서 조건을 각각 묻는 두 질문으로 나눕니다.",
            "## 각 질문을 따로 검색":"# 하위 질문마다 가장 가까운 근거 문서를 하나씩 고릅니다.",
            "## 구체 질문 검색":"# 날짜와 시각을 포함한 원 질문으로 먼저 운영 규정을 검색합니다.",
            "## 넓은 질문 생성":"# 세부 시각에서 한 단계 물러나 시설 운영 규칙을 묻습니다.",
            "## 두 문맥으로 답하기":"# 원 질문과 넓은 질문의 문서를 ID로 합쳐 답변 근거를 만듭니다.",
            "## 질문 임베딩 기준선":"# 짧은 원 질문의 임베딩으로 정답 문서 순위를 측정합니다.",
            "## 가상 문서 생성":"# 가상 안내문은 검색용으로만 생성하고 사실 근거로 사용하지 않습니다.",
            "## 결과 범위 확인":"# 기준선과 HyDE에서 정답 문서의 순위가 바뀌었는지 비교합니다.",
            "## 첫 검색과 품질 점수":"# 첫 검색의 최고 유사도를 고정 임계값과 비교할 값으로 저장합니다.",
            "## 임계값에 따른 보정":"# 기준 미만일 때만 질문을 풀어 쓰고 재검색을 한 번 실행합니다.",
            "## 반복 상한":"# 재검색 횟수가 코드에 정한 한 번을 넘지 않았는지 검사합니다.",
            "## 검색하고 초안 생성":"# 검색된 전자책 규정만 전달해 출처가 있는 첫 답을 만듭니다.",
            "## 근거 충실도 평가":"# 원문에 없는 문장을 넣은 검사 초안으로 낮은 점수 경로를 확인합니다.",
            "## 한 번만 수정":"# 점수가 기준 미만이면 근거 없는 문장을 한 번 제거합니다.",
            "## 범주별 묶음":"# category가 같은 문서를 한 목록에 모읍니다.",
            "## 요약 노드 직접 생성":"# 요약마다 원문 ID를 함께 저장해 나중에 원문을 찾습니다.",
            "## 계층 검색":"# 선택된 범주 안에서 원 질문과 가까운 문서 세 개를 고릅니다.",
            "## 비교 함수":"# 패턴별 검색·답변·사용량을 같은 필드로 반환합니다.",
            "## 세 패턴 실행":"# 같은 세 질문을 기준선, Multi-Query, HyDE에 차례로 실행합니다.",
            "## Recall·토큰·시간 집계":"# 패턴마다 정답 포함률과 전체 호출 비용을 평균·합계로 계산합니다.",
            "## 공개 실행 로그 저장":"# 데이터 해시와 질문별 원자료를 JSON 실행 로그로 저장합니다.",
        }
        cells += [md(f"{heading}\n\n{notes[heading]}"),code(comments[heading]+"\n"+source)]
    for i,c in enumerate(cells,1):
        c["id"]=f"cell-{i:02d}"
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.12"},"lesson_format":"experiment"},"nbformat":4,"nbformat_minor":5}

L={
"01-대화-히스토리와-질문-재작성":nb("대화 히스토리와 질문 재작성","대명사가 들어간 후속 질문을 독립 검색 질문으로 바꾸면 검색 결과가 달라지는지 확인합니다.",[
("## 히스토리가 없는 검색",'''history=["사용자: 일반 도서 대출 기간은?","도우미: 14일이며 한 번 연장할 수 있습니다."]
follow_up="그거 말고 전자책은?"
before=search(follow_up)
print("Before:",show_hits(before))'''),
("## 모델로 독립 질문 만들기",'''prompt=f"""대화 기록을 참고해 마지막 질문을 한 문장의 독립 검색 질문으로 바꾸세요.
대화 기록: {history}
마지막 질문: {follow_up}
질문만 출력하세요."""
rewritten,tokens,latency=ask(prompt)
after=search(rewritten)
print("재작성:",rewritten)
print("After:",show_hits(after),"토큰:",tokens,"ms:",latency)'''),
("## 검색 결과로 답하기",'''context="\\n".join(f"[{d['doc_id']}] {d['text']}" for d,_ in after)
answer,tokens,latency=ask(f"근거만 사용해 답하고 [문서ID]를 쓰세요.\\n{context}\\n질문:{rewritten}")
print(answer)
print("토큰·ms:",tokens,latency)''')]),
"02-Multi-Query":nb("Multi-Query","표현이 다른 여러 질문의 후보를 합치면 두 근거를 함께 찾는지 확인합니다.",[
("## 기준선 검색",'''question="책을 빌리는 기간과 늦게 반납했을 때 조치를 알려 주세요."
baseline=search(question,k=2)
print("기준선:",show_hits(baseline))'''),
("## 세 검색 질문 생성",'''text,tokens,latency=ask(f"검색 관점을 달리한 한국어 질문 3개를 줄마다 하나씩 쓰세요. 원문:{question}")
alternatives=[x.lstrip("-123. ") for x in text.splitlines() if x.strip()][:3]
print(alternatives,"토큰:",tokens,"ms:",latency)'''),
("## 후보 합치기",'''pool={}
for q in [question,*alternatives]:
    for doc,score in search(q,k=2):
        pool[doc["doc_id"]]=(doc,max(score,pool.get(doc["doc_id"],(doc,-1))[1]))
merged=sorted(pool.values(),key=lambda x:x[1],reverse=True)
print("통합 후보:",show_hits(merged))
print("정답 포함:",{"LIB-001","LIB-002"}.issubset(pool))''')]),
"03-질의-분해":nb("질의 분해","두 조건을 묻는 질문을 하위 질문으로 나누어 각 근거를 찾습니다.",[
("## 복합 질문 검색",'''question="휴학생은 전자자료와 일반 도서를 각각 이용할 수 있나요?"
print("한 번 검색:",show_hits(search(question,k=2)))'''),
("## 하위 질문 생성",'''text,tokens,latency=ask(f"다음 질문을 사실 하나씩 묻는 하위 질문 2개로 나누고 줄마다 쓰세요:{question}")
subquestions=[x.lstrip("-12. ") for x in text.splitlines() if x.strip()][:2]
print(subquestions,"토큰:",tokens,"ms:",latency)'''),
("## 각 질문을 따로 검색",'''evidence=[]
for sub in subquestions:
    hit=search(sub,k=1)[0]
    evidence.append(hit)
    print(sub,"->",hit[0]["doc_id"],round(hit[1],3))
print("서로 다른 근거 수:",len({d["doc_id"] for d,_ in evidence}))''')]),
"04-Step-back":nb("Step-back","구체 질문과 한 단계 넓힌 질문의 결과를 함께 사용합니다.",[
("## 구체 질문 검색",'''question="토요일 오후 6시에 자료실에 가도 되나요?"
specific=search(question,k=2)
print("구체 질문:",show_hits(specific))'''),
("## 넓은 질문 생성",'''step_back,tokens,latency=ask(f"세부 시각 판단에 필요한 일반 규칙을 찾도록 더 넓은 검색 질문 하나를 쓰세요:{question}")
broad=search(step_back,k=2)
print("Step-back:",step_back)
print("넓은 검색:",show_hits(broad),"토큰:",tokens,"ms:",latency)'''),
("## 두 문맥으로 답하기",'''unique={d["doc_id"]:d for d,_ in specific+broad}
context="\\n".join(f"[{k}] {v['text']}" for k,v in unique.items())
answer,tokens,latency=ask(f"근거로만 답하세요.\\n{context}\\n질문:{question}")
print(answer,"\\n토큰·ms:",tokens,latency)''')]),
"05-HyDE":nb("HyDE","가상의 정답 문서를 임베딩하면 검색 순위가 달라지는지 확인합니다.",[
("## 질문 임베딩 기준선",'''question="카드를 잃어버렸는데 계정을 보호하려면 무엇을 해야 하나요?"
baseline=search(question,k=3)
print("질문 검색:",show_hits(baseline))'''),
("## 가상 문서 생성",'''hypothesis,tokens,latency=ask(f"다음 질문에 답할 법한 도서관 안내문을 2문장으로 가상 작성하세요. 사실 확인용 답이 아닙니다.\\n{question}")
hyde=search(hypothesis,k=3)
print("가상 문서:",hypothesis)
print("HyDE 검색:",show_hits(hyde),"토큰:",tokens,"ms:",latency)'''),
("## 결과 범위 확인",'''gold="ACC-003"
print("기준선 순위:",next((i for i,(d,_) in enumerate(baseline,1) if d["doc_id"]==gold),None))
print("HyDE 순위:",next((i for i,(d,_) in enumerate(hyde,1) if d["doc_id"]==gold),None))''')]),
"06-CRAG":nb("CRAG식 교정 검색","검색 점수가 기준보다 낮을 때만 질문을 보정해 다시 검색합니다.",[
("## 첫 검색과 품질 점수",'''question="노쇼하면 방이 언제 풀리나요?"
first=search(question,k=2)
quality=first[0][1]
threshold=0.55
print("첫 검색:",show_hits(first),"최고 점수:",round(quality,3))'''),
("## 임계값에 따른 보정",'''if quality<threshold:
    corrected,tokens,latency=ask(f"도서관 규정 검색에 알맞게 용어를 풀어 질문 하나로 바꾸세요:{question}")
    final=search(corrected,k=3)
    action="재검색"
else: corrected,tokens,latency,final,action=question,0,0.0,first,"유지"
print(action,corrected)
print("최종:",show_hits(final),"토큰:",tokens,"ms:",latency)'''),
("## 반복 상한",'''max_retries=1
retry_count=1 if action=="재검색" else 0
print("재검색 횟수:",retry_count,"/ 상한:",max_retries)
assert retry_count<=max_retries''')]),
"07-Self-RAG":nb("Self-RAG에서 영감 받은 근거 검사","초안의 근거 점수를 평가하고 기준 미만일 때 한 번 수정합니다.",[
("## 검색하고 초안 생성",'''question="전자책은 몇 권까지 며칠 동안 빌릴 수 있나요?"
hits=search(question,k=2)
context="\\n".join(f"[{d['doc_id']}] {d['text']}" for d,_ in hits)
draft,gen_tokens,gen_ms=ask(f"근거로 답하고 [문서ID]를 쓰세요.\\n{context}\\n질문:{question}")
print("초안:",draft)'''),
("## 근거 충실도 평가",'''# 수정 분기를 확인하도록 원문에 없는 연체료 문장을 고정 초안에 추가합니다.
import re
draft_for_check=draft+" 연체료는 500원입니다."
score_text,judge_tokens,judge_ms=ask(f"근거로 확인되는 답의 비율을 0~1 숫자 하나로 쓰세요.\\n근거:{context}\\n답:{draft_for_check}")
match=re.search(r"(?:0(?:\\.\\d+)?|1(?:\\.0+)?)",score_text)
score=max(0.0,min(1.0,float(match.group()) if match else 0.0))
threshold=0.9
print("검사 초안:",draft_for_check)
print("근거 점수:",score,"기준:",threshold)'''),
("## 한 번만 수정",'''if score<threshold:
    final,revise_tokens,revise_ms=ask(f"근거 없는 내용을 빼고 답을 다시 쓰세요.\\n근거:{context}\\n답:{draft_for_check}")
else: final,revise_tokens,revise_ms=draft,0,0.0
print("최종:",final)
print("전체 토큰·ms:",gen_tokens+judge_tokens+revise_tokens,gen_ms+judge_ms+revise_ms)''')]),
"08-RAPTOR-계층-요약":nb("RAPTOR 축소 계층 요약","원문을 범주별로 묶고 요약 노드를 직접 만들어 계층 검색을 실행합니다.",[
("## 범주별 묶음",'''groups={}
for doc in docs:
    groups.setdefault(doc["category"],[]).append(doc)
print({name:len(items) for name,items in groups.items()})'''),
("## 요약 노드 직접 생성",'''summaries=[]
total_tokens=0
total_ms=0.0
for category,items in groups.items():
    source="\\n".join(d["text"] for d in items)
    text,tokens,latency=ask(f"다음 {category} 규정의 공통 주제를 3문장으로 요약하세요.\\n{source}")
    child_ids=[item["doc_id"] for item in items]
    summaries.append({"doc_id":f"SUM-{category}","category":category,"child_doc_ids":child_ids,"text":text})
    total_tokens+=tokens
    total_ms+=latency
print([(s["doc_id"],s["text"]) for s in summaries])
print("요약 토큰·ms:",total_tokens,round(total_ms,1))'''),
("## 계층 검색",'''summary_vectors=np.array(embedder.embed_documents([s["text"] for s in summaries]))
question="휴학이나 졸업 뒤 이용 권한은 어떻게 달라지나요?"
q=np.array(embedder.embed_query(question))
scores=summary_vectors@q/(np.linalg.norm(summary_vectors,axis=1)*np.linalg.norm(q))
chosen=summaries[int(np.argmax(scores))]["category"]
chosen_summary=next(s for s in summaries if s["category"]==chosen)
leaf_hits=[(d,s) for d,s in search(question,k=len(docs)) if d["category"]==chosen][:3]
print("선택한 요약 범주:",chosen)
print("요약의 하위 문서:",chosen_summary["child_doc_ids"])
print("하위 문서:",show_hits(leaf_hits))''')]),
"09-패턴-비교와-선택":nb("패턴 비교와 선택","같은 질문·문서·정답·모델로 기준선, Multi-Query, HyDE를 비교합니다.",[
("## 비교 함수",'''def run_variant(item: dict, variant: str) -> dict:
    started=time.perf_counter()
    usage_start=len(usage_log)
    if variant=="baseline":
        hits=search(item["question"],3)
    elif variant=="multi":
        text,_,_=ask(f"검색 질문 2개를 줄마다 쓰세요:{item['question']}")
        qs=[x.lstrip("-12. ") for x in text.splitlines() if x.strip()][:2]
        rrf={}
        found={}
        for q in qs:
            for rank,(doc,score) in enumerate(search(q,3),1):
                found[doc["doc_id"]]=(doc,score)
                rrf[doc["doc_id"]]=rrf.get(doc["doc_id"],0)+1/(60+rank)
        ids=sorted(rrf,key=rrf.get,reverse=True)[:3]
        hits=[found[doc_id] for doc_id in ids]
    else:
        text,_,_=ask(f"가상 안내문 2문장:{item['question']}")
        hits=search(text,3)
    context="\\n".join(d["text"] for d,_ in hits)
    answer,_,_=ask(f"근거로만 짧게 답하세요.\\n{context}\\n질문:{item['question']}")
    used=usage_log[usage_start:]
    ids=[d["doc_id"] for d,_ in hits]
    return {"pattern":variant,"qid":item["qid"],"question":item["question"],"gold":item["gold_doc_id"],"retrieved_ids":ids,"answer":answer,"rank":next((i for i,x in enumerate(ids,1) if x==item["gold_doc_id"]),None),"input_tokens":sum(x["input"] for x in used),"cached_tokens":sum(x["cached"] for x in used),"output_tokens":sum(x["output"] for x in used),"usd":sum(x["usd"] for x in used),"ms":round((time.perf_counter()-started)*1000,1)}'''),
("## 세 패턴 실행",'''sample=[queries[i] for i in [1,3,7]]
rows=[]
for variant in ["baseline","multi","hyde"]:
    for item in sample:
        rows.append(run_variant(item,variant))
for row in rows:
    print(row)'''),
("## Recall·토큰·시간 집계",'''for variant in ["baseline","multi","hyde"]:
    part=[r for r in rows if r["pattern"]==variant]
    recall=sum(r["rank"] is not None for r in part)/len(part)
    avg_tokens=sum(r["input_tokens"]+r["output_tokens"] for r in part)/len(part)
    avg_ms=sum(r["ms"] for r in part)/len(part)
    total_usd=sum(r["usd"] for r in part)
    print(variant,{"Recall@3":round(recall,3),"평균_토큰":round(avg_tokens,1),"평균_ms":round(avg_ms,1),"USD":round(total_usd,6)})'''),
("## 공개 실행 로그 저장",'''import hashlib
document_hash=hashlib.sha256((data_dir/"documents.json").read_bytes()).hexdigest()
query_hash=hashlib.sha256((data_dir/"queries.json").read_bytes()).hexdigest()
log={"source_provenance":"Ch12 core 축소 문서 12건·질문 8건","chat_model":"gpt-4.1-mini","embedding_model":"text-embedding-3-small","embedding_dimensions":256,"document_hash":document_hash,"query_hash":query_hash,"rows":rows}
runs=data_dir.parent/"runs"
runs.mkdir(exist_ok=True)
path=runs/"pattern-comparison.json"
path.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding="utf-8")
print("저장:",path.relative_to(root),"행:",len(rows))''')])}

for slug,book in L.items():
    path=HERE/"notebooks"/f"{slug}.ipynb"
    path.write_text(json.dumps(book,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
    print("wrote",path.name)
